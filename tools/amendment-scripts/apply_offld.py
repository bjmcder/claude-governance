"""Rehearsable adoption script: STND.OFFLD 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_offld as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T17:25:02+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.OFFLD, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's directions"
    " of 2026-10-24 that a standard hold the practice of offloading work to accelerators for every programming model,"
    " agnostic and timeless, with no annex for a particular framework, citing STND.CONC: 31 provisions, all defaults,"
    " language, compiler, vendor, framework, implementation, and tool agnostic. A stated fallback policy, placement"
    " confirmed or enforced, and fallback paths run in tests (STND.OFFLD.1 to STND.OFFLD.3); the order of submissions"
    " relied upon stated and dependences between queues expressed, host storage left unwritten while a transfer reads"
    " it, a mode that attributes each error to its submission, no use of a context that an error leaves unusable, and"
    " failures detected in device code recorded for the host (STND.OFFLD.4 to STND.OFFLD.8); authoritative copies"
    " stated and made current before a read, allocations released once after the last work that uses them completes, addresses used only"
    " where valid, a missing shared memory answered and tested, the memory scope of each synchronization, and no"
    " floating-point environment relied on across the boundary (STND.OFFLD.9 to STND.OFFLD.14); barriers reached by"
    " whole groups, no lockstep or convergence assumed, the participants of group operations named and their width"
    " obtained at run time, concurrent groups only under a guaranteeing facility, guarded indices of sufficient width,"
    " and submissions sized to a duration limit (STND.OFFLD.15 to STND.OFFLD.20); accelerator memory checked before"
    " submission, migration beyond it reported, and shared accelerators stated and chosen by a stated rule"
    " (STND.OFFLD.21 to STND.OFFLD.23); the hardware models of each build and the accelerators, compilation at load,"
    " caches, and settings of each run recorded (STND.OFFLD.24, STND.OFFLD.25); and tests run asynchronously, at edge"
    " sizes, with injected failures, with edge values under the production arithmetic, and under checks of device code"
    " where the means exist, with timing that ends at completion (STND.OFFLD.26 to STND.OFFLD.31). No provision binds"
    " and none raises the floor (GOV.11): the completion of offloaded work and the handling of its errors are"
    " governed by HW.GPU.3, STND.CONC.1, and PRIME.4, which already bind at every class. Transition (GOV.42): none,"
    " because no project instrument cites a draft of it. Review of STND.HARN.28 by the command pairs and by reading,"
    " a cold review, a pair review, and cold verifications; record review-records/ledger115/. The review found no"
    " conflict and no matter left without an owner in a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_OFFLD:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/OFFLD"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
