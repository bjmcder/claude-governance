"""Rehearsable adoption script: STND.CONC 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_conc as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T13:05:00+00:00"  # set to the time of application once ratified
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.CONC, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's direction"
    " of 2026-10-24 that one model-neutral standard hold the practice of concurrent execution, cited by the standards"
    " of single parallel programming models and of languages, and on the directions of 2026-10-24 on determinism"
    " (STND.VVUQ.82, STND.VVUQ.83): 29 provisions, language, platform, implementation, and tool agnostic. The"
    " completion of each asynchronous operation observed, with its failure answered, before a result relies on it,"
    " binding (STND.CONC.1, PRIME.4); each failure of a kind that PRIME.4 lists reaching the parent that relies on"
    " the task's result, and the tasks that wait on a halted task or compute a part of a result that relies on it"
    " halting or responding to notice of the halt, binding (STND.CONC.2, PRIME.4, HW.8); one stated protection for"
    " each shared mutable object, by synchronization that the memory model of its language or library, or the"
    " ordering model of its hardware contract, defines (STND.CONC.3); sequentially consistent atomic ordering unless"
    " a weaker one is justified (STND.CONC.4); publication of initialized objects and the lifetimes of objects used by"
    " reference and of synchronization objects (STND.CONC.5); thread safety stated in contracts (STND.CONC.6); an"
    " acyclic lock order (STND.CONC.7); only known code, waits for locks in order or for conditions through a"
    " facility that releases the lock, and no suspension under a lock (STND.CONC.8); retested condition waits"
    " (STND.CONC.9); bounded waits on other tasks reported at their bound (STND.CONC.10); a stated completion"
    " argument, and no task waiting on another task of a construct that does not guarantee that its tasks run"
    " concurrently (STND.CONC.11); tasks owned by a parent that waits for them (STND.CONC.12); cancellation that"
    " reaches the tasks a task started (STND.CONC.13); bounded queues and pools that lose no work silently"
    " (STND.CONC.14); event loops given back control (STND.CONC.15); no reliance on the thread that runs a migrating"
    " task (STND.CONC.16); pools taken from the caller and settings of the whole process left unchanged by libraries"
    " (STND.CONC.17); pools sized together on one node (STND.CONC.18); child processes of threaded programs started by"
    " a facility that starts a new program (STND.CONC.19); blocking by tasks of lower priority within the bounds of"
    " HW.20 (STND.CONC.20); results that depend on the number of tasks declared, fixed-order combination where"
    " bitwise identity across numbers of tasks is an acceptance criterion, as STND.VVUQ.2 provides, and random"
    " streams keyed to parts of the computation (STND.CONC.21, STND.CONC.22, STND.CONC.23); tests at three or more"
    " numbers of tasks, run-time detection of data races and deadlocks where the means of the work include it,"
    " varied schedules, stated limits of each verification, and a proved or exhaustively checked design for the"
    " protocols of safety-related components (STND.CONC.24 to STND.CONC.28); and the record of operations left"
    " pending at the end of a run (STND.CONC.29). STND.CONC.1 and STND.CONC.2 ask only for outcomes that PRIME.4"
    " and HW.8 already require, at the cost of one observation of each operation that a result relies on, one handle"
    " by which a parent learns of a failure, and one notice or call that ends the dependent tasks, and so raise no"
    " floor (GOV.11), as the custodian rules. Transition (GOV.42): none, because no project instrument cites a draft"
    " of it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and cold"
    " verifications; record review-records/ledger111/."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_CONC:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/CONC"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
