"""Rehearsable adoption script: STND.WFLOW 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_wflow as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.WFLOW, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's order of"
    " standards of 2026-10-24, which places a separate standard for workflows and the resilience of long runs after"
    " STND.OFFLD, and the custodian's standing directions that each standard be agnostic and timeless. In the drafters'"
    " design, the standard holds the practice of computational workflows and the resilience of long runs and cites"
    " STND.CONC for concurrency inside a program, STND.MPI for the halt of a job of several processes, and STND.BUILD"
    " for the steps that build software: 40 provisions, all"
    " defaults, agnostic of workflow engine, scheduler, file system, platform, and tool. The declarations of steps,"
    " with their inputs and outputs, the reuse of steps whose outputs vary, completion judged by checks of outputs,"
    " effects made once over all attempts, and steps repeatable after an interruption (STND.WFLOW.1 to STND.WFLOW.5);"
    " a stated staleness rule decided from a reuse key over content (STND.WFLOW.6); outputs published atomically and"
    " durably, partial outputs told from completed ones, and distinct output names (STND.WFLOW.7 to STND.WFLOW.9);"
    " failures classified for retry, bounded retries with backoff, one retrying layer, no retry unchanged after an"
    " exhausted resource, retries counted and followed, and the record of each attempt (STND.WFLOW.10 to"
    " STND.WFLOW.15); the notice of end and the grace period stated, the response to a notice, signal handlers that"
    " defer, and engine records valid after a forced end (STND.WFLOW.16 to STND.WFLOW.19); restart state written at a"
    " stated interval, in generations valid only when every writing process has written its portion, with its contents,"
    " identity, and format version stated and checked before use, and loaded from controlled storage where it executes"
    " code (STND.WFLOW.20 to STND.WFLOW.27); the completed members of a step set decided from checked outputs and the"
    " needs of their consumers stated (STND.WFLOW.28 and STND.WFLOW.29); storage, file count, and quotas in the run"
    " budget, storage purged by policy, the guarantees of shared file systems relied upon, staged copies verified, and"
    " the state of work directories stated (STND.WFLOW.30 to STND.WFLOW.34); the provenance of step outputs and the"
    " resumption record (STND.WFLOW.35 and STND.WFLOW.36); and tests of a run from a clean work directory, of"
    " interrupted attempts, of restarts, and of resumption, judged at the tier of STND.VVUQ.1 (STND.WFLOW.37 to"
    " STND.WFLOW.40). The parts that rest on a row of STND.CLASS.10 apply from the class of that row, and the Notes"
    " give the onset of each provision and sentence. No provision binds and none raises the floor (GOV.11): the"
    " completion of jobs and steps, the failures of set members and processes, the exhaustion of resources, storage"
    " included, and discarded failures are governed by STND.CONC.1, STND.CONC.2, STND.MPI.6, HW.8, STND.CODE.7, and"
    " PRIME.4, which already bind at every class. Transition (GOV.42): none, because no project instrument cites a"
    " draft of it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and a"
    " verification of draft 0.2; record review-records/round-2026-10-24/wflow/. The review found no conflict and no"
    " matter left without an owner in a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_WFLOW:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/WFLOW"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
