"""Extract the logical facts the governance corpus asserts about itself.

The facts come from front-matter fields (``rank``, ``waivable``,
``cites``, ``governed_by``) and the provision text. Each structural role
(the precedence clause, the non-waivable clause, and so on) is found by
a configured identifier confirmed against a title pattern, falling back
to a title search, so the checks survive renumbering. Nothing here
judges the facts; ``authority``, ``language``, and ``proofs`` do.
"""

from __future__ import annotations

import re
from typing import Any

from govharness.checks.base import CheckContext
from govharness.checks.lineage.derivation import derive_all
from govharness.checks.logic.tiers import extract_tiers
from govharness.checks.logic.wording import (
    extract_excluded,
    extract_normative,
    extract_terms,
    scan_phrases,
)
from govharness.core.corpus import Corpus, provision_key
from govharness.core.text import ids_in, split_sentences

Facts = dict[str, Any]
Roles = dict[str, dict[str, Any]]
ROLE_HINTS: dict[str, tuple[str, str]] = {
    "precedence": ("GOV.5", r"precedence"),
    "concession": ("GOV.6", r"concession"),
    "floor": ("GOV.10", r"^floor$"),
    "amendment": ("GOV.40", r"^amendment$"),
    "waiver": ("GOV.44", r"^waiver$"),
    "non_waivable": ("GOV.45", r"non-waivable"),
    "agents_bound": ("GOV.48", r"agents bound"),
    "loud_failure": ("PRIME.4", r"loud failure"),
    "reserved": ("PRIME.6", r"reserved action"),
    "authorization": ("PRIME.7", r"authorization"),
    "safe_state": ("PRIME.13", r"physical safety"),
    "halt_refer": ("PRIME.14", r"halt"),
    "tighten": ("PRIME.15", r"tighten"),
}
PART_ALIASES = {"Governing Principles": "PRIN", "Prime Directives": "PRIME"}
GRANT_RE = re.compile(r"\bMAY\s+(?:be waived|relieve)\b", re.IGNORECASE)


def resolve_roles(corpus: Corpus) -> Roles:
    """Map each structural role to a provision identifier.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    Roles
        Role to ``{"id", "how"}``; ``how`` is ``configured``,
        ``search``, or ``missing``.
    """
    resolved: Roles = {}
    for role, (preferred, pattern) in ROLE_HINTS.items():
        regex = re.compile(pattern, re.IGNORECASE)
        entry = corpus.by_id.get(preferred)
        if entry and regex.search(str(entry.meta.get("title", ""))):
            resolved[role] = {"id": preferred, "how": "configured"}
            continue
        found = [
            str(e.meta["id"])
            for e in sorted(corpus.provisions(), key=provision_key)
            if regex.search(str(e.meta.get("title", "")))
        ]
        resolved[role] = {
            "id": found[0] if found else None,
            "how": "search" if found else "missing",
        }
    return resolved


def extract_precedence(corpus: Corpus, clause_id: str | None) -> Facts:
    """Extract the ranked parts from the precedence clause.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    clause_id : str | None
        The precedence clause.

    Returns
    -------
    Facts
        ``ranks`` (letter, text, part), ``ranked`` (highest first, prime
        directives included when the clause says they outrank all),
        ``declared_unranked``, ``unranked`` (parts neither ranked nor
        declared), and ``front_matter_ranks``.
    """
    facts: Facts = {
        "clause": clause_id,
        "ranks": [],
        "ranked": [],
        "declared_unranked": [],
        "unranked": [],
        "front_matter_ranks": {},
    }
    body = corpus.body(clause_id)
    for letter, text, part in re.findall(
        r"\(([a-z])\)\s+([^()]+?)\s+\(([A-Z]{2,5})\)", body
    ):
        facts["ranks"].append({"letter": letter, "text": text, "part": part})
    top = re.search(r"prime directives outrank every other", body, re.I)
    facts["ranked"] = (["PRIME"] if top else []) + [
        r["part"] for r in facts["ranks"]
    ]
    if re.search(r"Governing Principles are not ranked", body):
        facts["declared_unranked"].append("PRIN")
    if re.search(r"\bGOV\b[^.]*\bnot ranked", body):
        facts["declared_unranked"].append("GOV")
    facts["unranked"] = [
        p
        for p in corpus.parts
        if p not in facts["ranked"] and p not in facts["declared_unranked"]
    ]
    for entry in corpus.provisions():
        if entry.meta.get("level") != "LVL0":
            continue
        part = entry.path.parts[0]
        facts["front_matter_ranks"].setdefault(part, set()).add(
            entry.meta.get("rank")
        )
    facts["front_matter_ranks"] = {
        p: sorted(v, key=lambda r: -1 if r is None else r)
        for p, v in facts["front_matter_ranks"].items()
    }
    return facts


def _mnemonics_in(text: str, parts: list[str]) -> list[str]:
    """Return the part mnemonics a text names, by mnemonic or by title.

    Parameters
    ----------
    text : str
        Sentence to scan.
    parts : list[str]
        Parts of LVL0, in order.

    Returns
    -------
    list[str]
        Named parts in the order of ``parts``.
    """
    found = [p for p in parts if re.search(rf"\b{p}\b(?!\.\d)", text)]
    found += [
        mnemonic
        for title, mnemonic in PART_ALIASES.items()
        if re.search(title, text, re.IGNORECASE)
    ]
    return sorted(set(found), key=parts.index)


def extract_waivers(corpus: Corpus, roles: Roles) -> Facts:
    """Extract the waiver and non-waivable facts.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    roles : Roles
        Resolved roles.

    Returns
    -------
    Facts
        Declared non-waivable parts and floor identifiers, parts the
        waiver clause can relieve, the expected non-waivable
        identifiers, provisions whose text grants a waiver path, and the
        waiver paths.
    """
    nw_id = roles["non_waivable"]["id"]
    nw_body = corpus.body(nw_id)
    floor_id = roles["floor"]["id"]
    floor_first = re.split(r"(?<=\.)\s", corpus.body(floor_id))[0]
    floor_ids = ids_in(floor_first)
    nw_sentence = next(
        (s for s in split_sentences(nw_body) if "waived" in s), ""
    )
    parts = _mnemonics_in(nw_sentence, corpus.parts)
    instantiators = bool(
        re.search(r"instantiates a prime directive", nw_sentence)
    )
    waiver_sentence = next(
        (
            s
            for s in split_sentences(corpus.body(roles["waiver"]["id"]))
            if GRANT_RE.search(s)
        ),
        "",
    )
    relieved = _mnemonics_in(
        waiver_sentence.split(", or of a lower")[0], corpus.parts
    )
    expected = {
        str(e.meta["id"])
        for e in corpus.provisions()
        if e.path.parts[0] in parts
    } | set(floor_ids)
    if instantiators:
        derived = derive_all(corpus, set(floor_ids))
        expected |= {pid for pid, info in derived.items() if info.primes}
    waiver_id = roles["waiver"]["id"]
    granting = [
        str(e.meta["id"])
        for e in corpus.provisions()
        if str(e.meta["id"]) != waiver_id
        and any(GRANT_RE.search(s) for s in split_sentences(e.body))
    ]
    reachable = {
        str(e.meta["id"])
        for e in corpus.provisions()
        if e.path.parts[0] in relieved
    } - set(floor_ids)
    return {
        "non_waivable_clause": nw_id,
        "non_waivable_sentence": nw_sentence,
        "non_waivable_parts": parts,
        "floor_ids": floor_ids,
        "instantiators_included": instantiators,
        "waiver_clause": roles["waiver"]["id"],
        "waiver_sentence": waiver_sentence,
        "relievable_parts": relieved,
        "expected_non_waivable": sorted(expected),
        "waiver_granting": granting,
        "waiver_paths": sorted(reachable | set(granting)),
    }


def all_facts(corpus: Corpus) -> Facts:
    """Extract every fact family into one dictionary.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    Facts
        Roles, precedence, waivers, tiers, excluded expressions and
        their uses, normative words, and Lexicon terms.
    """
    roles = resolve_roles(corpus)
    excluded = extract_excluded(corpus)
    return {
        "roles": roles,
        "precedence": extract_precedence(corpus, roles["precedence"]["id"]),
        "waivers": extract_waivers(corpus, roles),
        "tiers": extract_tiers(corpus),
        "excluded": excluded,
        "excluded_hits": scan_phrases(
            corpus, {**excluded["advisory"], **excluded["strict"]}
        ),
        "normative": extract_normative(corpus),
        "terms": extract_terms(corpus),
    }


def facts_of(ctx: CheckContext) -> Facts:
    """Return the facts of a run's corpus, extracted once per run.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Facts
        As ``all_facts``.
    """
    return ctx.shared(_facts_of_corpus)


def _facts_of_corpus(ctx: CheckContext) -> Facts:
    """Extract the facts of a context's corpus.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Facts
        As ``all_facts``.
    """
    return all_facts(ctx.corpus)
