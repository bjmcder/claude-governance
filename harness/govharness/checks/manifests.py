"""Structural check of ``verify``: every manifest is current (GOV.39)."""

from __future__ import annotations

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.derive.manifests import stale_manifests

FAMILY = "manifests"


def manifests_current(ctx: CheckContext) -> Verdict:
    """Check manifests: every manifest equals the derived one.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per stale or missing manifest.
    """
    stale = [
        f"stale manifest: {path}"
        for path in stale_manifests(ctx.require_tree())
    ]
    return Verdict("FAIL" if stale else "PASS", stale)


CHECKS: tuple[Check, ...] = (
    Check(
        "manifests",
        FAMILY,
        "Every manifest is current",
        ("GOV.39",),
        manifests_current,
    ),
)
