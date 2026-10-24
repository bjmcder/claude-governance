"""Rehearsable register change: MNEM gains MPI under STND (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
from govharness.workflows.amend import Change, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T08:37:00+00:00"
ROW_AFTER = "| VVUQ | STND | Verification, validation, and uncertainty quantification methods standard | none | Established acronym | active |"
ROW = "| MPI | STND | Message Passing Interface standard | none | The established name of the interface | active |"
RATIONALE = ("Register change, ratified by the custodian on " + DATE + ": MNEM gains MPI under STND, for the standard on the use of the "
             "Message Passing Interface, the first of the separate standards for parallel programming models (STND.IDENT.23)."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "MNEM/_doc.md", [(ROW_AFTER, ROW_AFTER + "\n" + ROW)])
    rec = record_transaction(root, Change(kind="register", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.37", "GOV.41"], targets=["MNEM"], scope=["MNEM"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), "MNEM")
