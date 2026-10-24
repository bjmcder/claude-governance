"""Checks 0 and a to c: roles, precedence, waivers, and authority tiers.

Each check judges facts from ``facts``. A ``FAIL`` means a structural
claim the corpus makes about itself is violated; ``WARN`` and ``INFO``
direct a human reader.
"""

from __future__ import annotations

import re
from typing import Any

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.logic.facts import facts_of
from govharness.core.corpus import Corpus, provision_key
from govharness.core.report import capped
from govharness.core.text import ids_in

FAMILY = "logic"
INCOMPATIBLE_TIERS = [
    ("free", "authorized"),
    ("free", "reserved"),
    ("free", "never"),
    ("authorized", "never"),
    ("standing_covers", "reserved"),
    ("standing_covers", "never"),
]


def roles_resolve(ctx: CheckContext) -> Verdict:
    """Check 0: every structural role resolves to a provision.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a role has no provision; the details list each role.
    """
    roles = facts_of(ctx)["roles"]
    missing = [r for r, info in roles.items() if info["id"] is None]
    return Verdict(
        "FAIL" if missing else "PASS",
        [f"- {r}: {i['id']} ({i['how']})" for r, i in roles.items()],
    )


def precedence_order(ctx: CheckContext) -> Verdict:
    """Check a.1: the precedence clause is a strict total order.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on non-contiguous letters, a repeated or foreign part, or
        no ranks at all.
    """
    prec = facts_of(ctx)["precedence"]
    ranked = prec["ranked"]
    problems: list[str] = []
    letters = [r["letter"] for r in prec["ranks"]]
    if letters != [chr(97 + i) for i in range(len(letters))]:
        problems.append(f"rank letters not contiguous: {letters}")
    repeats = sorted({p for p in ranked if ranked.count(p) > 1})
    if repeats:
        problems.append(f"ranked more than once: {repeats}")
    foreign = [p for p in ranked if p not in ctx.corpus.parts]
    if foreign:
        problems.append(f"ranked but not a part of LVL0: {foreign}")
    if not ranked:
        problems.append("no ranks found")
    return Verdict(
        "FAIL" if problems else "PASS",
        [f"Order, highest first: {' > '.join(ranked)}", *problems],
        {"clause": str(prec["clause"])},
    )


def parts_ranked(ctx: CheckContext) -> Verdict:
    """Check a.2: every part is ranked or declared unranked, never both.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a part is in neither set or in both.
    """
    prec = facts_of(ctx)["precedence"]
    left = prec["unranked"]
    declared = prec["declared_unranked"]
    both = sorted(set(declared) & set(prec["ranked"]))
    return Verdict(
        "FAIL" if left or both else "PASS",
        [
            f"Declared unranked: {', '.join(declared) or 'none'}",
            f"Neither ranked nor declared: {left or 'none'}",
            f"Ranked and declared unranked: {both or 'none'}",
        ],
    )


def ranks_agree(ctx: CheckContext) -> Verdict:
    """Check a.3: front-matter ``rank`` fields agree with the text.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a part's stored ranks differ from its place in the
        order.
    """
    prec = facts_of(ctx)["precedence"]
    expected = {p: i for i, p in enumerate(prec["ranked"])}
    mismatches = []
    for part, values in prec["front_matter_ranks"].items():
        want = expected.get(part)
        stray = [v for v in values if v != want]
        if stray:
            mismatches.append(f"- {part}: front matter {values}, text {want}")
    return Verdict(
        "FAIL" if mismatches else "PASS",
        mismatches or ["Every provision's rank field matches its part."],
    )


def non_waivable_exists(ctx: CheckContext) -> Verdict:
    """Check b.1: everything the non-waivable clause names exists.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a named part or floor obligation is missing, or no
        floor obligation is found.
    """
    w = facts_of(ctx)["waivers"]
    corpus = ctx.corpus
    expected = set(w["expected_non_waivable"])
    missing = [
        x
        for x in [*w["non_waivable_parts"], *w["floor_ids"]]
        if x not in corpus.by_id and x not in corpus.parts
    ]
    return Verdict(
        "FAIL" if missing or not w["floor_ids"] else "PASS",
        [
            f"Parts: {', '.join(w['non_waivable_parts'])}",
            f"Floor: {', '.join(w['floor_ids']) or 'none found'}",
            f"Instantiators of a prime directive included: "
            f"{w['instantiators_included']}",
            f"Expanded set: {len(expected)} provisions; missing: "
            f"{missing or 'none'}",
        ],
        {"clause": str(w["non_waivable_clause"])},
    )


def _flag_problems(corpus: Corpus, expected: set[str]) -> list[str]:
    """Return lines for ``waivable`` fields that disagree with the text.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    expected : set[str]
        Identifiers the non-waivable clause makes non-waivable.

    Returns
    -------
    list[str]
        One line per disagreeing provision.
    """
    lines = []
    for entry in corpus.provisions():
        pid = str(entry.meta["id"])
        flag = entry.meta.get("waivable")
        if entry.meta.get("level") != "LVL0":
            if pid in expected and flag:
                lines.append(
                    f"- {pid}: instantiates a prime directive, flag says "
                    "waivable"
                )
            continue
        if flag is None:
            if pid in expected:
                lines.append(f"- {pid}: non-waivable but has no flag")
            continue
        if pid in expected and flag:
            lines.append(f"- {pid}: non-waivable by text, flag says waivable")
        if pid not in expected and not flag:
            lines.append(f"- {pid}: flag says non-waivable, text does not")
    return lines


def waivable_flags(ctx: CheckContext) -> Verdict:
    """Check b.2: every ``waivable`` field agrees with the clause.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a flag disagrees with the non-waivable set.
    """
    expected = set(facts_of(ctx)["waivers"]["expected_non_waivable"])
    problems = _flag_problems(ctx.corpus, expected)
    return Verdict(
        "FAIL" if problems else "PASS",
        problems or ["Flags and text agree for every provision."],
    )


def waiver_disjoint(ctx: CheckContext) -> Verdict:
    """Check b.3: no part is both waivable and non-waivable.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on an overlap, a non-waivable provision the waiver clause
        reaches, or a waiver clause that does not exclude the floor.
    """
    w = facts_of(ctx)["waivers"]
    expected = set(w["expected_non_waivable"])
    relievable = set(w["relievable_parts"])
    overlap = sorted(relievable & set(w["non_waivable_parts"]))
    granting = sorted(set(w["waiver_paths"]) & expected)
    floor_named = "floor" in w["waiver_sentence"].lower()
    uncovered = [
        p
        for p in ctx.corpus.parts
        if p not in relievable and p not in w["non_waivable_parts"]
    ]
    return Verdict(
        "FAIL" if overlap or granting or not floor_named else "PASS",
        [
            f"Waivable parts: {', '.join(sorted(relievable))}",
            f"Overlap with non-waivable parts: {overlap or 'none'}",
            f"Non-waivable provisions the waiver clause can reach: "
            f"{granting or 'none'}",
            f"Waiver clause excludes the floor: {floor_named}",
            f"Parts in neither set: {uncovered or 'none'}",
        ],
    )


def tighten_cites(ctx: CheckContext) -> Verdict:
    """Check b.4: the tighten-only clause cites both procedures.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL unless it cites the amendment and the waiver clause.
    """
    roles = facts_of(ctx)["roles"]
    tighten = ctx.corpus.by_id.get(roles["tighten"]["id"] or "")
    cited = set(tighten.meta.get("cites", [])) if tighten else set()
    wanted = {roles["amendment"]["id"], roles["waiver"]["id"]}
    return Verdict(
        "PASS" if wanted <= cited else "FAIL",
        [f"Cites: {sorted(cited)}; required: {sorted(wanted)}"],
    )


def self_grant(ctx: CheckContext) -> Verdict:
    """Check b.5: self-grant prohibitions cite what they must.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a prohibition is missing, cites an identifier that
        does not resolve, or omits the waiver clause.
    """
    roles = facts_of(ctx)["roles"]
    corpus = ctx.corpus
    probes = [
        (
            roles["agents_bound"]["id"],
            r"grant themselves",
            roles["waiver"]["id"],
        ),
        (roles["authorization"]["id"], r"for itself", None),
    ]
    lines: list[str] = []
    ok = True
    for pid, pattern, target in probes:
        sentences = [
            s
            for s in re.split(r"(?<=\.)\s", corpus.body(pid))
            if re.search(pattern, s)
        ]
        refs = [r for s in sentences for r in ids_in(s)]
        resolved = all(r in corpus.by_id for r in refs)
        if not sentences or not resolved or (target and target not in refs):
            ok = False
        lines.append(f"- {pid}: {len(sentences)} sentence(s) cite {refs}")
    return Verdict("PASS" if ok else "FAIL", lines)


def procedures_closed(ctx: CheckContext) -> Verdict:
    """Check b.6: the amendment and waiver procedures are non-waivable.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when either is outside the non-waivable set.
    """
    facts = facts_of(ctx)
    roles = facts["roles"]
    expected = set(facts["waivers"]["expected_non_waivable"])
    paths = {roles["waiver"]["id"], roles["amendment"]["id"]}
    open_paths = sorted(p for p in paths if p not in expected)
    return Verdict(
        "FAIL" if open_paths else "PASS",
        [f"Not in the non-waivable set: {open_paths or 'none'}"],
    )


def tiers_compatible(ctx: CheckContext) -> Verdict:
    """Check c.1: no sentence is in two incompatible authority tiers.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a conflict; the details end with the tiers of each
        provision.
    """
    tiers = facts_of(ctx)["tiers"]
    conflicts = []
    for item in tiers["statements"]:
        present = set(item["tiers"])
        for left, right in INCOMPATIBLE_TIERS:
            if left in present and right in present:
                conflicts.append(
                    f"- {item['id']} is both {left} and {right}: "
                    f"{item['sentence']}"
                )
    table = ["| Provision | Tiers |", "| --- | --- |"]
    table += [
        f"| {pid} | {', '.join(t)} |"
        for pid, t in tiers["provision_tiers"].items()
    ]
    return Verdict("FAIL" if conflicts else "PASS", [*conflicts, "", *table])


def _cite_mismatches(corpus: Corpus) -> list[str]:
    """List LVL0 provisions whose text and ``cites`` name different ids.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    list[str]
        One line per provision, with the identifiers only in the text
        and only in the field.
    """
    lines = []
    for entry in sorted(corpus.provisions(), key=provision_key):
        if entry.meta.get("level") != "LVL0":
            continue
        pid = str(entry.meta["id"])
        text = set(ids_in(entry.body)) - {pid}
        index = set(entry.meta.get("cites", []))
        if text != index:
            lines.append(
                f"- {pid}: text-only {sorted(text - index)}, "
                f"index-only {sorted(index - text)}"
            )
    return lines


def cites_match(ctx: CheckContext) -> Verdict:
    """Check c.2: each LVL0 provision's text matches its ``cites``.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a mismatch.
    """
    mismatched = _cite_mismatches(ctx.corpus)
    return Verdict(
        "FAIL" if mismatched else "PASS",
        capped(mismatched) or ["Text and index agree for every provision."],
    )


def loud_failure_safe(ctx: CheckContext) -> Verdict:
    """Check c.3: loud failure links to the designed safe state.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL unless the loud-failure clause cites the safety clause.
    """
    roles = facts_of(ctx)["roles"]
    loud = ctx.corpus.by_id.get(roles["loud_failure"]["id"] or "")
    safe = roles["safe_state"]["id"]
    linked = bool(loud and safe in loud.meta.get("cites", []))
    return Verdict(
        "PASS" if linked else "FAIL",
        [f"{roles['loud_failure']['id']} cites {safe}: {linked}"],
    )


def reserved_back_links(ctx: CheckContext) -> Verdict:
    """Check c.4: the classes the reserved clause lists point back.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        INFO when a link is one-way, which a reader reviews.
    """
    facts = facts_of(ctx)
    reserved_id = facts["roles"]["reserved"]["id"]
    targets = sorted(
        {e["clause"] for e in facts["tiers"]["standing_exclusions"]}
    )
    lines = []
    for target in targets:
        entry = ctx.corpus.by_id.get(target)
        text = entry.body.lower() if entry else ""
        back = bool(
            entry
            and (
                reserved_id in entry.meta.get("cites", [])
                or "reserved" in text
            )
        )
        lines.append(f"- {target}: refers back to {reserved_id}: {back}")
    missing = [x for x in lines if x.endswith("False")]
    return Verdict(
        "INFO" if missing else "PASS",
        [*lines, "A one-way link is not a defect; it is listed for review."],
    )


def standing_excluded(ctx: CheckContext) -> Verdict:
    """Check c.5: no standing authorization covers an excluded action.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a statement under a standing authorization names a
        clause excluded from standing cover.
    """
    tiers: dict[str, Any] = facts_of(ctx)["tiers"]
    violations = []
    covers = [
        s for s in tiers["statements"] if "standing_covers" in s["tiers"]
    ]
    for item in covers:
        scope = {item["provision"], *item["cites"], *item["refs"]}
        for ex in tiers["standing_exclusions"]:
            if ex["clause"] in scope and (
                ex["qualifier"] is None or item["hazardous"]
            ):
                violations.append(
                    f"- {item['id']} is under a standing authorization but "
                    f"{ex['clause']} is excluded by {ex['source']}"
                )
    listed = ", ".join(
        f"{e['clause']}{' (hazardous only)' if e['qualifier'] else ''}"
        for e in tiers["standing_exclusions"]
    )
    return Verdict(
        "FAIL" if violations else "PASS",
        [
            f"Excluded from standing cover: {listed or 'none'}",
            f"Statements under a standing authorization: {len(covers)}",
            *violations,
        ],
    )


CHECKS: tuple[Check, ...] = (
    Check(
        "0",
        FAMILY,
        "Structural roles resolve to provisions",
        ("LVL0",),
        roles_resolve,
    ),
    Check(
        "a.1",
        FAMILY,
        "Precedence ({clause}) is a strict total order over the parts it "
        "ranks",
        ("GOV.5",),
        precedence_order,
    ),
    Check(
        "a.2",
        FAMILY,
        "Every part is ranked or declared unranked, never both",
        ("GOV.5",),
        parts_ranked,
    ),
    Check(
        "a.3",
        FAMILY,
        "Front-matter `rank` fields agree with the precedence text",
        ("GOV.5", "GOV.17"),
        ranks_agree,
    ),
    Check(
        "b.1",
        FAMILY,
        "Everything {clause} names as non-waivable exists",
        ("GOV.45", "GOV.10"),
        non_waivable_exists,
    ),
    Check(
        "b.2",
        FAMILY,
        "Every `waivable` field agrees with the non-waivable clause",
        ("GOV.45", "GOV.17"),
        waivable_flags,
    ),
    Check(
        "b.3",
        FAMILY,
        "No part is both waivable and non-waivable; the floor is excluded",
        ("GOV.44", "GOV.45"),
        waiver_disjoint,
    ),
    Check(
        "b.4",
        FAMILY,
        "The tighten-only clause cites the amendment and waiver procedures",
        ("PRIME.15",),
        tighten_cites,
    ),
    Check(
        "b.5",
        FAMILY,
        "Self-grant prohibitions resolve to the waiver and authorization "
        "clauses",
        ("GOV.48", "PRIME.7"),
        self_grant,
    ),
    Check(
        "b.6",
        FAMILY,
        "The amendment and waiver procedures are themselves non-waivable",
        ("GOV.40", "GOV.44", "GOV.45"),
        procedures_closed,
    ),
    Check(
        "c.1",
        FAMILY,
        "No sentence places one action in two incompatible authority tiers",
        ("PRIME.6", "PRIME.7"),
        tiers_compatible,
    ),
    Check(
        "c.2",
        FAMILY,
        "Identifiers cited in each LVL0 provision's text match its `cites` "
        "field",
        ("GOV.35",),
        cites_match,
    ),
    Check(
        "c.3",
        FAMILY,
        "Loud failure links to the designed safe state",
        ("PRIME.4", "PRIME.13"),
        loud_failure_safe,
    ),
    Check(
        "c.4",
        FAMILY,
        "Each class the reserved clause lists points back to it",
        ("PRIME.6",),
        reserved_back_links,
    ),
    Check(
        "c.5",
        FAMILY,
        "Standing authorizations never cover an excluded action",
        ("PRIME.6", "PRIME.7"),
        standing_excluded,
    ),
)
