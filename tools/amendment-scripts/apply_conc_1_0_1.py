"""Rehearsable editorial amendment: STND.CONC 1.0.1, citing STND.OMP, STND.OFFLD, and STND.WFLOW (one transaction).

The lead applies it after STND.WFLOW is adopted (apply_wflow_round.py), not in apply_round_2026_10_24_amend.py.
To rehearse it on a copy, apply apply_wflow_round.py to that copy first, then this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T21:30:00+00:00"

DOC = [
    ("and the planned standards for directive-based threading and for accelerator offload hold theirs once adopted.",
     "STND.OMP holds those for directive-based threading, and STND.OFFLD those for accelerator "
     "offload."),
    ("Workflows of many runs, retried tasks, checkpoints, and access to shared files and storage belong to a planned "
     "standard of their own;",
     "Workflows of many runs, retried tasks, checkpoints, and access to shared files and storage belong to "
     "STND.WFLOW, whose STND.WFLOW.32 holds the guarantees of shared file systems on which work relies;"),
    ("the memory of accelerators belongs to HW.GPU and to the standard for offload.",
     "the memory of accelerators belongs to HW.GPU and to STND.OFFLD, whose STND.OFFLD.9 to STND.OFFLD.12 and "
     "STND.OFFLD.21 to STND.OFFLD.23 govern it."),
    ("and the directive-based threading standard has a form for its tasks.",
     "and STND.OMP.7 is its form for the tasks of OpenMP."),
    ("STND.CXX.23 is its form for C++.",
     "STND.CXX.23 is its form for objects that C++ code shares with signal and interrupt handlers."),
    ("Whether concurrent calls to an interface are safe is part of its contract, as STND.CXX.15 already asks of C++ "
     "(STND.CONC.6).",
     "Whether concurrent calls to an interface are safe is part of its contract (STND.CONC.6), and in C++ that "
     "contract is the declaration comment of STND.CXX.15."),
]

READING = ("the Purpose and the Notes cite STND.OMP, adopted in ledger entry 114, STND.OFFLD, adopted in ledger "
           "entry 116, and STND.WFLOW in place of the planned standards for directive-based threading, for "
           "accelerator offload, and for workflows, with STND.WFLOW.32 for the guarantees of shared file systems "
           "and STND.OMP.7 as the OpenMP form of STND.CONC.16, and describe STND.CXX.23 and STND.CXX.15 as they read "
           "after STND.CXX 1.1; References lists STND.OMP, STND.OFFLD, and STND.WFLOW")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation changes. |"

RATIONALE = (
    f"Editorial amendment of STND.CONC, revision 1.0.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.OMP in ledger entry 114, of STND.OFFLD in ledger entry 116, and of STND.WFLOW: {READING}; no obligation changes. The "
    "change is editorial because it alters only the informative Purpose, Notes, and References, and no provision, "
    "mode, class onset, or defined term. It follows STND.CXX 1.1, after which STND.CXX.23 governs only objects "
    "shared with handlers and STND.CXX.15 cites STND.CONC.6. Transition (GOV.42): none, because no obligation changes. "
    "Review of STND.HARN.28 by the command pairs; record review-records/round-2026-10-24/amendments/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/CONC/_doc.md", DOC)
    raise_revision(root, "STND/CONC", "1.0", "1.0.1", ROW)
    B.write_references(root, ["STND.CONC"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CONC"], scope=["STND/CONC"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CONC 1.0.1")
