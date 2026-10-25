"""Rehearsable editorial amendment: STND.MPI 1.0.1, naming the MPI form of STND.CONC.30 and closing the
References gap that tools/check_refs.py reports.

One transaction. STND.MPI predates STND.CONC, whose STND.CONC.30 reaches the processes of a parallel execution;
the Notes name the forms that its two outcomes, an order that a protocol fixes and a declared variation, take for
the output of processes and for parallel input and output. The class paragraph names GUARD in words without a
References row; it is reworded so that it names no document without citing it. Run from harness/, so that
govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_mpi_1_0_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:01:00+00:00"

IO_OLD = ("and STND.MPI.22 asks for it, or a description of the file, for a file that another run, platform, or tool "
          "reads.")
IO_NEW = IO_OLD + (
    " STND.CONC.30 has the order in which concurrent tasks write to one output or one record stated, as an order "
    "that a protocol of those tasks fixes or as a variation that the record of that output declares, and the "
    "processes of a parallel execution are concurrent tasks under STND.CONC. The MPI standard leaves to the "
    "implementation and its launcher whether and how the standard output and standard error of each process reach "
    "the operator, and the lines that different processes write arrive there in an order that varies between runs "
    "(unverified); one process that writes the output that the others send it, in an order that the message "
    "protocol of STND.MPI.12 states, fixes that order. A collective write through the shared file pointer of a file "
    "places the data of the processes in the order of their ranks, a noncollective write through it places them in "
    "the order in which the processes reach their writes, and a write at an offset that the protocol computes places "
    "them where the protocol states (unverified). The first and the last fix the order of the records, and the "
    "order that the second gives is a variation that the record of the file declares (STND.CONC.30). Where two "
    "accesses conflict, the atomic mode or the synchronization that STND.MPI.21 asks also fixes their order, so one "
    "statement of the protocol of the file meets both provisions; records written to disjoint parts of a file are "
    "no conflicting accesses, and only STND.CONC.30 reaches their order.")

FLOOR = ("No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no default raises the "
         "floor (GOV.11).",
         "No default instantiates a prime directive, a provision of the Article of safeguards or of GOV, or a floor "
         "obligation, so GOV.19 marks none of them binding, and no default raises the floor (GOV.11).")

READING = ("the Notes name the form of STND.CONC.30 for MPI: the processes of a parallel execution are concurrent "
           "tasks under STND.CONC; the order in which the lines of different processes reach the operator varies "
           "unless one process writes the output that the others send it in an order that the message protocol "
           "states; a collective write through the shared file pointer and a write at an offset that the protocol "
           "computes fix the order of the records of a file, while a noncollective write through the shared file "
           "pointer gives a variation that the record of the file declares; and STND.MPI.21, on conflicting "
           "accesses, and STND.CONC.30 do not conflict, one statement of the protocol of a file meeting both; the "
           "class paragraph names the Article of safeguards in words and cites GOV.19 in place of a bare name that "
           "had no References row; References lists STND.CONC")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation changes. |"

RATIONALE = (
    f"Editorial amendment of STND.MPI, revision 1.0.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.CONC.30 by STND.CONC 1.1: {READING}; no obligation changes. The change is editorial because it alters "
    "only the informative Notes and References, and no provision, mode, citation of a provision, class onset, or "
    "defined term (STND.IDENT.3). No provision is added: STND.CONC.30 already reaches the processes of a parallel "
    "execution, which its Term Concurrent task includes, and the message protocol that STND.MPI.12 has stated and "
    "the protocol of a file that STND.MPI.21 has stated are where the order that a protocol fixes is stated, so "
    "MPI sets no trap that a further outcome would close. The provisions of STND.MPI do not conflict with "
    "STND.CONC.30: STND.MPI.21 orders conflicting accesses, STND.MPI.15 and STND.MPI.18 declare the variation of "
    "matching and of reductions under HW.12, and STND.MPI.6 completes the write of a diagnosis before an abort, "
    "none of which fixes or forbids an order of output that STND.CONC.30 admits. The facts on forwarded output and "
    "on the shared file pointer are marked unverified, since the research note does not hold them. "
    "Transition (GOV.42): none, because no obligation changes. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-25-close/p4/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/MPI/_doc.md", [(IO_OLD, IO_NEW), FLOOR])
    raise_revision(root, "STND/MPI", "1.0", "1.0.1", ROW)
    B.write_references(root, ["STND.MPI"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.MPI"], scope=["STND/MPI"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.MPI 1.0.1")
