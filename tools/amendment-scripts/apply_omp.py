"""Rehearsable adoption script: STND.OMP 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_omp as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T15:05:00+00:00"  # set to the time of application once ratified
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.OMP, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's directions"
    " of 2026-10-24 that a standard hold the practice specific to OpenMP, cite STND.CONC for every model-neutral rule,"
    " and rest on practice stable across the revisions of OpenMP, because the drafts of 6.1 are additive: 33"
    " provisions, all defaults, language, compiler, vendor, implementation, and tool agnostic. Features defined and"
    " not deprecated by a later revision, extensions recorded, features used only where each implementation documents"
    " them and a test exercises them, the OpenMP settings in the record of each run, and the correctness of each"
    " component with OpenMP disabled stated and, where stated, tested (STND.OMP.1 to STND.OMP.4); explicit"
    " data-sharing attributes, private and lastprivate values, threadprivate persistence and tied tasks, and local"
    " variables shared with tasks waited for before return (STND.OMP.5 to STND.OMP.8); worksharing and barrier"
    " regions reached alike by every thread, reads after nowait and masked regions synchronized, memory-order"
    " clauses on atomics that order other data and no flush with a list, locations accessed atomically kept atomic"
    " and aligned, atomic constructs kept from locations that signal handlers access, and named critical sections and locks kept within their contention group (STND.OMP.9 to"
    " STND.OMP.13); task dependences on identical or disjoint storage, waits that cover descendants, and detach"
    " events fulfilled on every path, a cutoff for recursive task creation and results the same within the agreement"
    " of the acceptance criterion whether a task is deferred, included, or merged, and cancellation enabled where code"
    " relies on it, tested enabled and disabled, with locks released before a cancellation point (STND.OMP.14 to"
    " STND.OMP.16); declared reductions justified and reproducible iteration mapping that is not relied on to fix the"
    " order of a reduction (STND.OMP.17, STND.OMP.18); the caller's internal control variables left unchanged by"
    " libraries, state for each thread sized from the team obtained, structured blocks left only through their end,"
    " and no OpenMP in signal handlers (STND.OMP.19 to STND.OMP.22); device placement enforced or confirmed, device"
    " numbers checked and device allocations released by their paired routine, structures and pointers mapped,"
    " balanced mappings, the present modifier, and copies back that the reference count does not suppress, device"
    " copies of global variables kept current, reliance on shared memory declared by requires directives with the same clauses and"
    " answered where no device meets it, memory scopes of atomics between host and device, and no floating-point"
    " environment relied on across the target boundary (STND.OMP.23 to STND.OMP.30); and tests under mandatory"
    " offload and on the host alone against a host reference, mapping checks where the means exist, and tests under"
    " each schedule and binding of threads that the runs set (STND.OMP.31 to STND.OMP.33). No provision binds and none raises the"
    " floor (GOV.11): the failures of OpenMP code are governed by PRIME.4, STND.CONC.1, STND.CONC.2, STND.CODE.7,"
    " HW.8, and HW.GPU.3, which already bind at every class. Transition (GOV.42): none, because no project instrument"
    " cites a draft of it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, pair reviews of the draft and"
    " of its changes, and cold verifications; record review-records/ledger113/. The review found no conflict that remains and no"
    " matter left without an owner in a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_OMP:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/OMP"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
