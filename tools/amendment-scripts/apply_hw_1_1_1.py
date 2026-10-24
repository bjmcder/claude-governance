"""Rehearsable editorial amendment: HW 1.1.1, the Note on HW.8 for a run of several processes.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_hw_1_1_1.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T12:00:00+00:00"  # set to the time of application once ratified

ANCHOR = ("HW.8 states how PRIME.4 applies to detected, uncorrected hardware faults and to exhausted capacity, "
          "and binds at every class, adding nothing to the floor that PRIME.4 does not already hold.")
NOTE = (" For a run of several processes that compute one result together, HW.8 is read as asking the whole run "
        "to halt, degrade visibly, or transition to a designed safe state. A process that halts while the others "
        "wait on it leaves a silent hang. STND.MPI.6 states how the halt of one process reaches the others in a "
        "program that uses the Message Passing Interface.")

REF_AFTER = "| STND.DRAFT | Drafting standard |"
REF_ROW = "| STND.MPI | Message Passing Interface standard |"

READING = ("for a run of several processes that compute one result together, HW.8 is read as asking the whole "
           "run to halt, degrade visibly, or transition to a designed safe state, citing STND.MPI.6, and References "
           "lists STND.MPI; no obligation changes")

ROW = f"| 1.1.1 | {DATE} | Editorial amendment (GOV.41): the informative Notes state that, {READING}. |"

RATIONALE = (f"Editorial amendment of HW, revision 1.1.1, ratified by the custodian on {DATE}: the informative Notes "
             f"state that, {READING}. The change is editorial because the Note states a reading of HW.8 that "
             "STND.MPI.6 already applies, and changes no provision and no defined term."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "HW/_doc.md", [(ANCHOR, ANCHOR + NOTE), (REF_AFTER, REF_AFTER + "\n" + REF_ROW)])
    raise_revision(root, "HW", "1.1", "1.1.1", ROW)
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["HW"], scope=["HW"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "HW 1.1.1")
