"""Check f: encode the structural claims as clauses and prove them.

The precedence order, the non-waivable set, and the authority tiers are
encoded as propositional facts and axioms. Joint consistency is checked
first (f.1); each claim is then proved by refuting its negation. A claim
the corpus gives no material for (no ranked part, say) is not reported,
and no claim is reported when the facts are inconsistent.

The clause sets of a run, the base and one negation per claim, are
built once; when the run has a solve cache, ``planned_keys`` names the
key of each before the run, so that the caller can load the entries,
and each solve reuses a checked entry (``solvecache``, unit 0011).
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.logic.facts import Facts, facts_of
from govharness.checks.logic.satlib import (
    ClauseSet,
    Literal,
    SolveResult,
    backend_name,
    negation,
)
from govharness.checks.logic.solvecache import (
    add_clauses,
    key_start,
    solve_cached,
)
from govharness.core.report import capped

FAMILY = "logic"
TIER_ATOMS = (
    "free",
    "authorized",
    "reserved",
    "never",
    "agent_forbidden",
    "standing_covers",
    "hazardous",
)
TOP_TITLE = "{top} outranks every other ranked part (transitive closure)"
ASYMMETRY_TITLE = "No ranked part outranks one that outranks it (asymmetry)"
UNRANKED_TITLE = "{top} outranks the unranked parts {free}"
NOT_FORCED_TITLE = (
    "{second} is not forced above the unranked parts {free} (conflicts go "
    "to GOV.6)"
)
WAIVER_TITLE = "No non-waivable provision offers a waiver path"
STANDING_TITLE = "No excluded statement is under a standing authorization"
RESERVED_TITLE = "Every reserved statement is closed to agents"


@dataclass
class Claim:
    """A structural claim to prove.

    Parameters
    ----------
    literals : list[Literal]
        Literals whose conjunction is the claim.
    entailed : bool
        Whether the corpus is expected to force the claim.
    fields : dict[str, str]
        Values for the placeholders of the claim's title.
    """

    literals: list[Literal]
    entailed: bool = True
    fields: dict[str, str] = field(default_factory=dict)


def _lt(higher: str, lower: str) -> str:
    """Name the atom meaning one part outranks another.

    Parameters
    ----------
    higher, lower : str
        Part mnemonics.

    Returns
    -------
    str
        The atom name.
    """
    return f"lt[{higher}<{lower}]"


def _encode_order(base: ClauseSet, facts: Facts, parts: list[str]) -> None:
    """Add asymmetry, transitivity, and the ranking facts.

    Parameters
    ----------
    base : ClauseSet
        Receives the clauses.
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.
    """
    for a, b in itertools.permutations(parts, 2):
        base.add(f"asym:{a},{b}", (_lt(a, b), False), (_lt(b, a), False))
    for a, b, c in itertools.permutations(parts, 3):
        base.add(
            f"trans:{a},{b},{c}",
            (_lt(a, b), False),
            (_lt(b, c), False),
            (_lt(a, c), True),
        )
    ranked = facts["precedence"]["ranked"]
    for higher, lower in zip(ranked, ranked[1:], strict=False):
        base.fact(f"fact:rank {higher} above {lower}", _lt(higher, lower))
    if ranked[:1] == ["PRIME"]:
        for part in parts:
            if part != "PRIME":
                base.fact(
                    f"fact:PRIME outranks every other provision ({part})",
                    _lt("PRIME", part),
                )


def _encode_waivers(base: ClauseSet, facts: Facts) -> None:
    """Add non-waivable facts and the axiom that bars a waiver path.

    Parameters
    ----------
    base : ClauseSet
        Receives the clauses.
    facts : Facts
        Extracted facts.
    """
    w = facts["waivers"]
    for pid in w["expected_non_waivable"]:
        base.fact(f"fact:non_waivable({pid})", f"non_waivable[{pid}]")
        base.implies(
            f"axiom:non_waivable->no_waiver_path({pid})",
            f"non_waivable[{pid}]",
            (f"waiver_path[{pid}]", False),
        )
    for pid in w["waiver_paths"]:
        base.fact(f"fact:waiver_path({pid})", f"waiver_path[{pid}]")


def _applies(exclusion: dict[str, Any], item: dict[str, Any]) -> bool:
    """Return True when a standing exclusion reaches a statement.

    Parameters
    ----------
    exclusion : dict[str, Any]
        Standing exclusion: source, clause, qualifier.
    item : dict[str, Any]
        Tier statement.

    Returns
    -------
    bool
        Whether the statement names the excluded clause, in a case the
        qualifier covers.
    """
    scope = {item["provision"], *item["cites"], *item["refs"]}
    if exclusion["clause"] not in scope:
        return False
    return exclusion["qualifier"] is None or item["hazardous"]


def _encode_statement(
    base: ClauseSet, item: dict[str, Any], exclusions: list[dict[str, Any]]
) -> None:
    """Add the tier axioms and facts for one sentence.

    Parameters
    ----------
    base : ClauseSet
        Receives the clauses.
    item : dict[str, Any]
        Tier statement.
    exclusions : list[dict[str, Any]]
        Standing exclusions.
    """
    sid = item["id"]
    atom = {t: f"{t}[{sid}]" for t in TIER_ATOMS}
    base.at_most_one(
        f"axiom:exclusive_tiers({sid})",
        [atom["free"], atom["authorized"], atom["agent_forbidden"]],
    )
    for tier in ("reserved", "never"):
        base.implies(
            f"axiom:{tier}->forbidden({sid})",
            atom[tier],
            (atom["agent_forbidden"], True),
        )
    base.add(
        f"axiom:forbidden->reserved|never({sid})",
        (atom["agent_forbidden"], False),
        (atom["reserved"], True),
        (atom["never"], True),
    )
    base.implies(
        f"axiom:standing->authorized({sid})",
        atom["standing_covers"],
        (atom["authorized"], True),
    )
    for tier in item["tiers"]:
        if tier in atom:
            base.fact(f"fact:{tier}({sid})", atom[tier])
    base.fact(
        f"fact:hazardous({sid})={item['hazardous']}",
        atom["hazardous"],
        item["hazardous"],
    )
    for ex in exclusions:
        if _applies(ex, item):
            base.fact(
                f"fact:{ex['source']} bars standing cover({sid})",
                atom["standing_covers"],
                False,
            )


def build_base(facts: Facts, parts: list[str]) -> ClauseSet:
    """Encode all facts and axioms into one clause set.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    ClauseSet
        Order, waiver, and tier clauses.
    """
    base = ClauseSet()
    _encode_order(base, facts, parts)
    _encode_waivers(base, facts)
    tiers = facts["tiers"]
    for item in tiers["statements"]:
        _encode_statement(base, item, tiers["standing_exclusions"])
    return base


def base_of(ctx: CheckContext) -> ClauseSet:
    """Return the clause set of a run, built once.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    ClauseSet
        As ``build_base``.
    """
    return ctx.shared(_build_base_of)


def _build_base_of(ctx: CheckContext) -> ClauseSet:
    """Build the clause set of a context's corpus.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    ClauseSet
        As ``build_base``.
    """
    return build_base(facts_of(ctx), ctx.corpus.parts)


def _negations_of(
    ctx: CheckContext,
) -> dict[str, tuple[Claim, ClauseSet]]:
    """Build each claim of a run and the clause set of its negation.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    dict[str, tuple[Claim, ClauseSet]]
        By the claim's title template, for each claim the corpus gives
        material for: the claim, and the base with its negation, named
        by the filled title.
    """
    facts, base = facts_of(ctx), base_of(ctx)
    found: dict[str, tuple[Claim, ClauseSet]] = {}
    for _, title, _, build in CLAIMS:
        claim = build(facts, ctx.corpus.parts)
        if claim is not None:
            name = title.format(**claim.fields)
            found[title] = (claim, negation(base, name, claim.literals))
    return found


def _keys_of(ctx: CheckContext) -> dict[str, str]:
    """Return the cache key of each solve of a run.

    The key of a negation extends a copy of the base's digest by its one
    clause, so the base is serialized once.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    dict[str, str]
        By claim title template, and ``""`` for the base; empty when the
        run has no solve cache.
    """
    cache = ctx.solve_cache
    if cache is None:
        return {}
    base = base_of(ctx)
    digest = add_clauses(
        key_start(cache.version, backend_name(ctx.use_z3)), base
    )
    keys = {"": digest.copy().hexdigest()}
    for title, (_, negated) in ctx.shared(_negations_of).items():
        extended = add_clauses(digest.copy(), negated, len(base.clauses))
        keys[title] = extended.hexdigest()
    return keys


def planned_keys(ctx: CheckContext) -> list[str]:
    """Return the cache keys of every solve a run may make.

    Parameters
    ----------
    ctx : CheckContext
        Context of a run with a solve cache, before the run.

    Returns
    -------
    list[str]
        The key of the base and of each claim's negation; a claim is
        solved only when the base is satisfiable, so a key may go unused.
    """
    return list(ctx.shared(_keys_of).values())


def consistency(ctx: CheckContext) -> SolveResult:
    """Return the satisfiability of a run's facts and axioms, once.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    SolveResult
        The outcome and the solver backend.
    """
    return ctx.shared(_solve_base_of)


def _solve_base_of(ctx: CheckContext) -> SolveResult:
    """Solve the clause set of a context.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    SolveResult
        The outcome.
    """
    key = ctx.shared(_keys_of).get("")
    return solve_cached(base_of(ctx), ctx.use_z3, ctx.solve_cache, key)


def solver_backend(ctx: CheckContext) -> str:
    """Return the name of the solver a run used.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    str
        Backend name, such as ``builtin-dpll``.
    """
    return consistency(ctx).backend


def consistent(ctx: CheckContext) -> Verdict:
    """Check f.1: the extracted facts and axioms are jointly consistent.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with a core of facts when they are not.
    """
    base = base_of(ctx)
    outcome = consistency(ctx)
    details = [
        f"Backend: {outcome.backend}; {len(base.clauses)} clauses over "
        f"{len(base.variables())} variables."
    ]
    if outcome.satisfiable:
        details.append("The facts and axioms are jointly satisfiable.")
    else:
        details.append("UNSATISFIABLE. Core facts:")
        details += [f"- {name}" for name in outcome.core]
    return Verdict("PASS" if outcome.satisfiable else "FAIL", details)


def _prove(ctx: CheckContext, title: str) -> Verdict | None:
    """Prove one claim and judge it.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.
    title : str
        Title template of the claim; the filled title names the negated
        claim clause.

    Returns
    -------
    Verdict | None
        PASS when the outcome is the expected one; otherwise FAIL for a
        claim that should be forced and INFO for one that should not.
        ``None`` when the facts are inconsistent or give no claim.
    """
    if not consistency(ctx).satisfiable:
        return None
    planned = ctx.shared(_negations_of).get(title)
    if planned is None:
        return None
    claim, negated = planned
    key = ctx.shared(_keys_of).get(title)
    result = solve_cached(negated, ctx.use_z3, ctx.solve_cache, key)
    entailed = not result.satisfiable
    want = claim.entailed
    status = "PASS" if entailed == want else ("FAIL" if want else "INFO")
    lines = [f"Claim: {len(claim.literals)} literal(s)."]
    if entailed:
        lines.append(f"ENTAILED. Core facts ({len(result.core)}):")
        lines += capped([f"- {n}" for n in result.core])
    else:
        lines.append(
            "NOT ENTAILED: a countermodel exists, so the "
            "corpus does not force it."
        )
    return Verdict(status, lines, claim.fields)


def _free_parts(facts: Facts, parts: list[str]) -> list[str]:
    """Return the parts the precedence clause does not rank.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    list[str]
        Unranked parts, in part order.
    """
    ranked = facts["precedence"]["ranked"]
    return [p for p in parts if p not in ranked]


def top_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.2: the top part outranks every other ranked part.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        The claim, or ``None`` when nothing is ranked.
    """
    ranked = facts["precedence"]["ranked"]
    if not ranked:
        return None
    top = ranked[0]
    return Claim([(_lt(top, o), True) for o in ranked[1:]], True, {"top": top})


def asymmetry_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.3: no ranked part outranks one that outranks it.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        The claim, or ``None`` when nothing is ranked.
    """
    ranked = facts["precedence"]["ranked"]
    if not ranked:
        return None
    return Claim(
        [
            (_lt(low, high), False)
            for high, low in itertools.combinations(ranked, 2)
        ]
    )


def unranked_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.4: the top part outranks the unranked parts.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        The claim, or ``None`` when nothing is ranked or unranked.
    """
    ranked = facts["precedence"]["ranked"]
    free = _free_parts(facts, parts)
    if not ranked or not free:
        return None
    top = ranked[0]
    return Claim(
        [(_lt(top, o), True) for o in free],
        True,
        {"top": top, "free": ", ".join(free)},
    )


def not_forced_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.8: the second part is not forced above the unranked ones.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        A claim expected not to be entailed, or ``None`` when fewer than
        two parts are ranked or none is unranked.
    """
    ranked = facts["precedence"]["ranked"]
    free = _free_parts(facts, parts)
    if not ranked or not free or len(ranked) <= 1:
        return None
    return Claim(
        [(_lt(ranked[1], o), True) for o in free],
        False,
        {"second": ranked[1], "free": ", ".join(free)},
    )


def waiver_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.5: no non-waivable provision offers a waiver path.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        The claim, or ``None`` when the non-waivable set is empty.
    """
    expected = facts["waivers"]["expected_non_waivable"]
    if not expected:
        return None
    return Claim([(f"waiver_path[{p}]", False) for p in expected])


def standing_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.6: no excluded statement is under standing cover.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        The claim, or ``None`` when no exclusion reaches a statement.
    """
    tiers = facts["tiers"]
    barred = [
        s
        for s in tiers["statements"]
        if any(_applies(e, s) for e in tiers["standing_exclusions"])
    ]
    if not barred:
        return None
    return Claim([(f"standing_covers[{s['id']}]", False) for s in barred])


def reserved_claim(facts: Facts, parts: list[str]) -> Claim | None:
    """Build f.7: every reserved statement is closed to agents.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    Claim | None
        The claim, or ``None`` when no statement is reserved.
    """
    reserved = [
        s for s in facts["tiers"]["statements"] if "reserved" in s["tiers"]
    ]
    if not reserved:
        return None
    return Claim([(f"agent_forbidden[{s['id']}]", True) for s in reserved])


def _claim_check(key: str, title: str, enforces: tuple[str, ...]) -> Check:
    """Return the check that proves one claim of ``CLAIMS``.

    Parameters
    ----------
    key : str
        Check key.
    title : str
        Title template of the claim; ``_negations_of`` builds the claim
        it names.
    enforces : tuple[str, ...]
        Provisions it enforces.

    Returns
    -------
    Check
        The registered value.
    """
    return Check(key, FAMILY, title, enforces, lambda ctx: _prove(ctx, title))


ClaimSpec = tuple[
    str, str, tuple[str, ...], Callable[[Facts, list[str]], Claim | None]
]
# The claims are listed in the order the report has always shown them:
# key, title template, provisions enforced, and the builder.
CLAIMS: tuple[ClaimSpec, ...] = (
    ("f.2", TOP_TITLE, ("GOV.5",), top_claim),
    ("f.3", ASYMMETRY_TITLE, ("GOV.5",), asymmetry_claim),
    ("f.4", UNRANKED_TITLE, ("GOV.5",), unranked_claim),
    ("f.8", NOT_FORCED_TITLE, ("GOV.5", "GOV.6"), not_forced_claim),
    ("f.5", WAIVER_TITLE, ("GOV.45",), waiver_claim),
    ("f.6", STANDING_TITLE, ("PRIME.6",), standing_claim),
    ("f.7", RESERVED_TITLE, ("PRIME.6",), reserved_claim),
)
CHECKS: tuple[Check, ...] = (
    Check(
        "f.1",
        FAMILY,
        "All extracted facts and axioms are jointly consistent",
        ("LVL0",),
        consistent,
    ),
    *(_claim_check(key, title, why) for key, title, why, _ in CLAIMS),
)
