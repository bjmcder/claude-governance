"""The registered check families and the runner.

The families are listed here explicitly, with no discovery (SIMPL.6).
Adding a family means adding one module and one line here (DSGN.11).
The order of each list is the order of the report.
"""

from __future__ import annotations

from types import ModuleType

from govharness.checks import combination, fields, ledger, manifests, structure
from govharness.checks.base import CheckContext
from govharness.checks.drafting import family as drafting
from govharness.checks.lineage import family as lineage
from govharness.checks.logic import authority, language, proofs
from govharness.checks.revisions import family as revisions
from govharness.core.report import Report

# The structural checks of ``verify``, in the order it prints them.
STRUCTURE: tuple[ModuleType, ...] = (structure, manifests, ledger, fields)
# The logic checks of ``check`` and ``verify``; the proofs come last.
LOGIC: tuple[ModuleType, ...] = (
    authority,
    language,
    lineage,
    drafting,
    revisions,
    combination,
    proofs,
)


def registered_keys() -> frozenset[str]:
    """Return the key of every registered check.

    Returns
    -------
    frozenset[str]
        Keys of the structural and the logic checks.
    """
    return frozenset(
        check.key for family in (*STRUCTURE, *LOGIC) for check in family.CHECKS
    )


def run_checks(families: tuple[ModuleType, ...], ctx: CheckContext) -> Report:
    """Run every check of some families in a fresh context.

    The context's ``known_keys`` is set to every registered key before
    the first check runs.

    Parameters
    ----------
    families : tuple[ModuleType, ...]
        Family modules, each with a tuple ``CHECKS``.
    ctx : CheckContext
        Context that no run has used.

    Returns
    -------
    Report
        One result per check that applies, in registry order.

    Raises
    ------
    ValueError
        If the context already holds results.
    """
    if ctx.report.results:
        raise ValueError("a context serves one run of checks")
    ctx.known_keys = registered_keys()
    for family in families:
        for check in family.CHECKS:
            verdict = check.run(ctx)
            if verdict is not None:
                ctx.report.add(
                    check.key,
                    check.heading(verdict),
                    verdict.status,
                    verdict.details,
                )
    return ctx.report
