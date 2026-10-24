"""Rehearsable register change: MNEM gains CONC under STND (one transaction).

Run from harness/:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_conc_round.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.workflows.amend import Change, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T13:17:36+00:00"
ROW_AFTER = "| MPI | STND | Message Passing Interface standard | none | The established name of the interface | active |"
ROW = "| CONC | STND | Concurrency standard | none | Reads as concurrency | active |"
RATIONALE = ("Register change, ratified by the custodian on " + DATE + ": MNEM gains CONC under STND, for the "
             "model-neutral standard on concurrent execution in every language and parallel programming model "
             "(STND.IDENT.23)."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "MNEM/_doc.md", [(ROW_AFTER, ROW_AFTER + "\n" + ROW)])
    rec = record_transaction(root, Change(kind="register", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.37", "GOV.41"], targets=["MNEM"], scope=["MNEM"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "MNEM")
