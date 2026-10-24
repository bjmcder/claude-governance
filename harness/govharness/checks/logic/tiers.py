"""Classify the authority tier that each sentence of an action states.

A sentence of a prime directive, a GUARD provision, or a numbered
provision below LVL0 may say that an action is free, needs an
authorization, is reserved to the human owner, or is never done. The
signals are read by wording, so a sentence carries every tier its words
match.
"""

from __future__ import annotations

import re
from typing import Any

from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.text import ids_in, split_sentences, without_tables

TIER_PARTS = {"PRIME", "GUARD"}
HAZARD_RE = re.compile(r"\bhazardous\b|\birreversible\b", re.IGNORECASE)
TIER_PATTERNS: dict[str, list[str]] = {
    "free": [
        r"\b(?:is|are) free\b",
        r"\bwithout further authorization\b",
        r"\bneeds? no authorization\b",
    ],
    "authorized": [
        r"\bonly (?:under|with|within|on)\b[^.;]*?\bauthoriz",
        r"\brequires? (?:an? )?(?:express |explicit |recorded |per-action )?"
        r"authorization\b",
        r"\bper-action authorization\b",
    ],
    "reserved": [r"\breserved\b(?!-)", r"\bonly the human owner executes\b"],
    "never": [
        r"\bnever\b",
        r"\bshall not\b",
        r"\b(?:is|are) prohibited\b",
    ],
    "standing_covers": [
        r"\b(?:within|under|covered by) a standing authorization\b"
    ],
    "standing_excluded": [
        r"\bnever authorized\b[^.;]*\bstanding\b",
        r"\bnever covered by a standing authorization\b",
    ],
}


def classify_sentence(sentence: str) -> set[str]:
    """Return the authority-tier signals present in one sentence.

    Parameters
    ----------
    sentence : str
        One sentence.

    Returns
    -------
    set[str]
        Names of the tiers its wording matches; a standing exclusion
        overrides the authorized and standing-cover signals.
    """
    low = sentence.lower()
    signals = {
        tier
        for tier, patterns in TIER_PATTERNS.items()
        if any(re.search(p, low) for p in patterns)
    }
    if "standing_excluded" in signals:
        signals -= {"authorized", "standing_covers"}
    return signals


def _is_action_provision(entry: Entry) -> bool:
    """Return True for provisions whose sentences state action authority.

    Parameters
    ----------
    entry : Entry
        Any entry.

    Returns
    -------
    bool
        True for LVL0 provisions of PRIME or GUARD and for numbered
        entries below LVL0.
    """
    stem = entry.path.stem
    if entry.meta.get("level") == "LVL0":
        return (
            entry.meta.get("kind") == "provision"
            and entry.path.parts[0] in TIER_PARTS
        )
    return stem.isdigit()


def _exclusions_in(
    provision: str, sentences: list[str], index: int
) -> list[dict[str, Any]]:
    """List what a standing-excluded sentence excludes from standing cover.

    The excluded items are the identifiers named in the sentences up to
    it (the definition of the reserved class), with a ``hazardous``
    qualifier where the item's own clause is limited to hazardous cases.

    Parameters
    ----------
    provision : str
        Identifier of the provision.
    sentences : list[str]
        Its sentences.
    index : int
        Position of the standing-excluded sentence.

    Returns
    -------
    list[dict[str, Any]]
        One record per excluded clause: source, clause, and qualifier.
    """
    found: list[dict[str, Any]] = []
    for sentence in sentences[: index + 1]:
        for item in sentence.split(";"):
            for ref in ids_in(item):
                if ref == provision:
                    continue
                found.append(
                    {
                        "source": provision,
                        "clause": ref,
                        "qualifier": "hazardous"
                        if HAZARD_RE.search(item)
                        else None,
                    }
                )
    return found


def extract_tiers(corpus: Corpus) -> dict[str, Any]:
    """Classify the authority tier of every sentence in action provisions.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    dict[str, Any]
        ``statements`` (id, provision, sentence, tiers, hazardous, refs,
        cites), ``standing_exclusions``, and ``provision_tiers``.
    """
    statements: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    for entry in corpus.entries:
        if not _is_action_provision(entry):
            continue
        pid = str(entry.meta["id"])
        sentences = split_sentences(without_tables(entry.body))
        for index, sentence in enumerate(sentences):
            signals = classify_sentence(sentence)
            if not signals:
                continue
            if "standing_excluded" in signals:
                exclusions.extend(_exclusions_in(pid, sentences, index))
            statements.append(
                {
                    "id": f"{pid}#s{index + 1}",
                    "provision": pid,
                    "sentence": sentence,
                    "tiers": sorted(signals),
                    "hazardous": bool(HAZARD_RE.search(sentence)),
                    "refs": ids_in(sentence),
                    "cites": list(entry.meta.get("cites", [])),
                }
            )
    provision_tiers: dict[str, set[str]] = {}
    for item in statements:
        provision_tiers.setdefault(item["provision"], set()).update(
            item["tiers"]
        )
    return {
        "statements": statements,
        "standing_exclusions": exclusions,
        "provision_tiers": {
            k: sorted(v) for k, v in sorted(provision_tiers.items())
        },
    }
