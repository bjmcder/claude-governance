"""Rehearsable adoption script: STND.MPI 1.0 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content_mpi as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-24T08:38:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.MPI": "Adoption of STND.MPI, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's"
 " directions of 2026-10-23 and of 2026-10-24 on determinism (STND.VVUQ.82, STND.VVUQ.83): 25 provisions on the use of the Message Passing Interface in every language, platform,"
 " implementation, and tool agnostic, naming no MPI implementation, launcher, checker, platform, or revision of the"
 " MPI standard, which is taken at the revision that the work's implementation documents. Facilities of the MPI"
 " standard and recorded extensions (STND.MPI.1); the implementation, the library loaded at run time, process count"
 " and placement, thread support level, and settings in the record of each result (STND.MPI.2, HW.3); the thread"
 " support level requested, stated, compared with the level provided, and honored (STND.MPI.3); error handlers"
 " stated, files and errors that belong to no object included (STND.MPI.4); each error that MPI reports answered,"
 " with nonblocking and persistent operations and access epochs completed where errors return, binding"
 " (STND.MPI.5, PRIME.4, HW.8); the halt of one process ending the others of its parallel execution, or reaching"
 " them as notice to which they respond as PRIME.4 requires, after the write of its diagnosis is completed, binding"
 " (STND.MPI.6, PRIME.4, HW.8); the behavior of the implementation when a process ends without finalizing, and"
 " whether the fatal handler writes a diagnosis, stated in the hardware contract, a limit on runs without that"
 " assurance, and a persistent diagnosis (STND.MPI.7); libraries that take communicators from their callers, keep"
 " their callers' error handlers, leave the world model and process-wide settings to the program, and free the"
 " handles they own and no predefined one (STND.MPI.8, STND.MPI.9, STND.MPI.10, STND.MPI.11); stated message"
 " protocols with an argument of completion that relies on no progress beyond the MPI standard's, or a deadlock"
 " check, no reliance on buffering with a test run of synchronous sends, matching type signatures, nondeterministic"
 " matching declared, and the lifetime of nonblocking operations (STND.MPI.12, STND.MPI.13, STND.MPI.14,"
 " STND.MPI.15, STND.MPI.16); collective call order, creation and freeing included, results that depend on process"
 " count or reduction order declared, and reductions in a fixed or order-independent combination, judged by"
 " identical bits, where bitwise identity across process counts is an acceptance criterion, as STND.VVUQ.2 provides"
 " (STND.MPI.17, STND.MPI.18, STND.MPI.19); window synchronization (STND.MPI.20); shared file access and portable"
 " file representation (STND.MPI.21, STND.MPI.22); threads sharing MPI objects (STND.MPI.23); and tests at no fewer"
 " than three process counts that the protocol admits, among them the smallest that it admits, or each where it admits fewer, within a tolerance of a tier of"
 " STND.VVUQ.1, and run-time correctness checks (STND.MPI.24, STND.MPI.25). STND.MPI.5 and STND.MPI.6 ask only for"
 " outcomes that PRIME.4 and HW.8 already require and leave every response that PRIME.4 admits, at the cost of at"
 " most one error handler, a completion call where a request would otherwise be freed while active, one call that"
 " ends the other processes, and the completion of one write of the diagnosis, and so raise no floor"
 " (GOV.11), as the custodian rules; all processes of one run are read as one execution path of HW.8. Transition (GOV.42): none. Review of STND.HARN.28 by the"
 " command pairs and by reading, a cold review, a pair review, and cold verifications; record"
 " claude/drafts/review-records-ledger106-109.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/MPI"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS_MPI:
        adopt(Path(root), d)
