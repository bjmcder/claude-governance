"""Rehearsable register change: MNEM gains FTN under STND (one transaction)."""
from __future__ import annotations

from pathlib import Path

from govharness.workflows.amend import Change, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T20:00:00+00:00"
ROW_AFTER = "| OFFLD | STND | Accelerator offload standard | none | Reads as offload; offload has no established acronym | active |"
ROW = ("| FTN | STND | Fortran standard | none | The conventional short form of the name Fortran; avoids FOR, a common"
       " word | active |")
RATIONALE = ("[Placeholder rationale; the lead sets it at the coalesce.] Register change, ratified by the custodian on "
             + DATE + ": MNEM gains FTN under STND, for the Fortran standard (STND.IDENT.23)."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "MNEM/_doc.md", [(ROW_AFTER, ROW_AFTER + "\n" + ROW)])
    rec = record_transaction(root, Change(kind="register", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.37", "GOV.41"], targets=["MNEM"], scope=["MNEM"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "MNEM")
