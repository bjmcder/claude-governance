"""Rehearsable editorial amendment: STND.OMP 1.0.2, naming the OpenMP form of STND.CONC.30.

One transaction. STND.CONC.30 reaches the threads and tasks of OpenMP; the Notes list it among the provisions of
STND.CONC that hold for OpenMP and name the constructs that fix an order of output or leave it to the schedule.
Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_omp_1_0_2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:02:00+00:00"

LIST = ("tests at several numbers of threads (STND.CONC.24), and run-time detection of data races (STND.CONC.25).",
        "tests at several numbers of threads (STND.CONC.24), run-time detection of data races (STND.CONC.25), and "
        "the order of the writes of concurrent tasks to one output or one record (STND.CONC.30).")

SCHED_OLD = "and 5.2 leaves the schedule implementation defined (STND.OMP.18)."
SCHED_NEW = SCHED_OLD + (
    " The writes that the threads of a team make to one output appear in the order in which the threads reach them, "
    "and a static schedule or the reproducible modifier fixes which thread runs each iteration and not when it runs, "
    "so neither fixes that order (by inference from STND.OMP.18). An ordered region runs in the order of the "
    "iterations of its loop, so the writes inside it appear in that order, at the cost of serializing that part of "
    "the loop (r2); a critical construct or a lock keeps two writes from interleaving and leaves their order to the "
    "schedule (by inference). An ordered region, or a single thread that writes what the others computed, is a "
    "protocol that fixes the order of output, and the record of the output declares each other order as a "
    "variation (STND.CONC.30). No provision of this standard asks for or forbids an order of output, so "
    "STND.CONC.30 applies to OpenMP without an OpenMP form.")

READING = ("the Notes list STND.CONC.30 among the provisions of STND.CONC that hold for the threads and tasks of "
           "OpenMP, and name its OpenMP form: neither a static schedule nor the reproducible modifier fixes the order "
           "of the writes of a team to one output; an ordered region fixes it, at the cost of serializing that part "
           "of the loop, and a single thread that writes what the others computed fixes it too; a critical construct "
           "or a lock prevents interleaving without fixing the order; and no provision of the standard conflicts "
           "with STND.CONC.30")

ROW = f"| 1.0.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation changes. |"

RATIONALE = (
    f"Editorial amendment of STND.OMP, revision 1.0.2, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.CONC.30 by STND.CONC 1.1: {READING}; no obligation changes. The change is editorial because it alters "
    "only the informative Notes, and no provision, mode, citation of a provision, class onset, defined term, or "
    "References row, since References already lists STND.CONC (STND.IDENT.3). No provision is added: STND.CONC.30 "
    "already reaches the threads and tasks of OpenMP, which the Notes read as concurrent tasks, and the ordered "
    "construct is a protocol under its own words, so OpenMP sets no trap that a further outcome would close. No "
    "provision of STND.OMP conflicts with STND.CONC.30: STND.OMP.18 fixes the mapping of iterations to threads and "
    "says that it does not fix the order of a reduction, and STND.OMP.13 governs critical constructs and locks as "
    "protections, neither of which fixes or forbids an order of output. That an ordered region runs in the order "
    "of the iterations, and serializes that part of the loop, is in research/openmp-notes/r2-host-hazards.md; the "
    "statements on schedules and critical constructs are marked as inferences. Transition (GOV.42): none, because "
    "no obligation changes. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-25-close/p4/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/OMP/_doc.md", [LIST, (SCHED_OLD, SCHED_NEW)])
    raise_revision(root, "STND/OMP", "1.0.1", "1.0.2", ROW)
    B.write_references(root, ["STND.OMP"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.OMP"], scope=["STND/OMP"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.OMP 1.0.2")
