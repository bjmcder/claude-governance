"""Checks l.1 to l.5: the lineage of every provision below LVL0.

They apply to every provision below LVL0 and fail, because PRIME.15,
GOV.17, and GOV.19 state them.
"""

from __future__ import annotations

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.lineage.derivation import (
    LEVEL_ORDER,
    Derived,
    derive_all,
    level_of,
    lower_provisions,
    references,
)
from govharness.checks.logic.facts import facts_of
from govharness.core.locators import reference_resolves
from govharness.core.report import capped

FAMILY = "lineage"
MODES = ("binding", "default")


def derived_of(ctx: CheckContext) -> dict[str, Derived]:
    """Return the derived values of every lower provision, once per run.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    dict[str, Derived]
        Derived values by provision identifier.
    """
    return ctx.shared(_derive_lower)


def _derive_lower(ctx: CheckContext) -> dict[str, Derived]:
    """Derive the lower provisions with the floor of the run's facts.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    dict[str, Derived]
        Derived values by provision identifier.
    """
    floor_ids = set(facts_of(ctx)["waivers"]["floor_ids"])
    return derive_all(ctx.corpus, floor_ids)


def declared(ctx: CheckContext) -> Verdict:
    """Check l.1: each provision instantiates something that resolves.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a provision with no ``instantiates`` or a reference
        that resolves to nothing.
    """
    provisions = lower_provisions(ctx.corpus)
    missing, dangling = [], []
    for entry in provisions:
        pid = str(entry.meta["id"])
        if not entry.meta.get("instantiates"):
            missing.append(f"- {pid}: no `instantiates` (PRIME.15)")
        for ref in references(entry):
            if not reference_resolves(ref, ctx.corpus.by_id):
                dangling.append(f"- {pid}: `{ref}` resolves to nothing")
    return Verdict(
        "FAIL" if missing or dangling else "PASS",
        capped(missing + dangling)
        or [f"{len(provisions)} provision(s) checked."],
    )


def upward(ctx: CheckContext) -> Verdict:
    """Check l.2: instantiation reaches LVL0 directly and only upward.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a provision that names no LVL0 ancestor, a cyclic
        closure, or an ancestor that is not at a higher level.
    """
    derived = derived_of(ctx)
    shape = []
    for entry in lower_provisions(ctx.corpus):
        pid = str(entry.meta["id"])
        info = derived[pid]
        if entry.meta.get("instantiates") and not info.direct_lvl0:
            shape.append(f"- {pid}: names no LVL0 ancestor directly")
        if info.cycle:
            shape.append(f"- {pid}: `instantiates` closure is cyclic")
        own_level = LEVEL_ORDER.get(str(entry.meta.get("level")), 9)
        for ref in entry.meta.get("instantiates") or []:
            level = level_of(ctx.corpus, ref)
            if level is not None and LEVEL_ORDER.get(level, 9) >= own_level:
                shape.append(f"- {pid}: instantiates `{ref}`, not higher")
    return Verdict(
        "FAIL" if shape else "PASS",
        capped(shape) or ["Every closure is well formed."],
    )


def grades(ctx: CheckContext) -> Verdict:
    """Check l.3: stored rank and waivability equal the derived values.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a rank that differs, or a waivability that is missing
        or wider than derived.
    """
    derived = derived_of(ctx)
    found = []
    for entry in lower_provisions(ctx.corpus):
        pid = str(entry.meta["id"])
        info = derived[pid]
        stored_rank = entry.meta.get("rank")
        stored_waiv = entry.meta.get("waivable")
        if stored_rank != info.rank:
            found.append(
                f"- {pid}: rank {stored_rank!r}, derived {info.rank!r} "
                "(GOV.17)"
            )
        if stored_waiv is None or (stored_waiv and not info.waivable):
            found.append(
                f"- {pid}: waivable {stored_waiv!r}, derived "
                f"{info.waivable!r} (GOV.17)"
            )
    return Verdict(
        "FAIL" if found else "PASS",
        capped(found) or ["Rank and waivability follow the ancestors."],
    )


def modes(ctx: CheckContext) -> Verdict:
    """Check l.4: every LVL2 provision is binding or default consistently.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on an unknown mode, a non-waivable default, or a binding
        mark that nothing forces and no ``binding_reason`` explains.
    """
    derived = derived_of(ctx)
    found = []
    for entry in lower_provisions(ctx.corpus):
        if entry.meta.get("level") != "LVL2":
            continue
        pid = str(entry.meta["id"])
        info = derived[pid]
        mode = entry.meta.get("mode")
        reason = str(entry.meta.get("binding_reason") or "").strip()
        if mode not in MODES:
            found.append(f"- {pid}: mode {mode!r}, not binding/default")
        elif not info.waivable and mode != "binding":
            found.append(
                f"- {pid}: derived non-waivable but marked default "
                "(GOV.17, GOV.19)"
            )
        elif mode == "binding" and not info.forced and not reason:
            found.append(
                f"- {pid}: binding, reaches no PRIME/GUARD/GOV/floor "
                "provision, records no `binding_reason` (GOV.19)"
            )
    return Verdict(
        "FAIL" if found else "PASS",
        capped(found) or ["Marks and reasons agree with the lineage."],
    )


def prime_children(ctx: CheckContext) -> Verdict:
    """Check l.5: an instantiator of a prime directive is non-waivable.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a waivable provision that reaches a prime directive.
    """
    derived = derived_of(ctx)
    primes = [
        f"- {e.meta['id']}: instantiates a prime directive (GOV.45)"
        for e in lower_provisions(ctx.corpus)
        if derived[str(e.meta["id"])].primes and e.meta.get("waivable")
    ]
    return Verdict(
        "FAIL" if primes else "PASS",
        capped(primes) or ["No waivable instantiator of a prime directive."],
    )


CHECKS: tuple[Check, ...] = (
    Check(
        "l.1",
        FAMILY,
        "Every provision below LVL0 declares what it instantiates, and "
        "every reference resolves",
        ("PRIME.15",),
        declared,
    ),
    Check(
        "l.2",
        FAMILY,
        "Instantiation reaches LVL0 directly, acyclically, and only upward",
        ("PRIME.15", "GOV.16"),
        upward,
    ),
    Check(
        "l.3",
        FAMILY,
        "Stored rank and waivability agree with the derived values",
        ("GOV.17",),
        grades,
    ),
    Check(
        "l.4",
        FAMILY,
        "Every LVL2 provision is marked binding or default consistently",
        ("GOV.19",),
        modes,
    ),
    Check(
        "l.5",
        FAMILY,
        "A provision that instantiates a prime directive is non-waivable",
        ("GOV.45",),
        prime_children,
    ),
)
