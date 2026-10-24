"""Rehearsable register change: MNEM gains BUILD under STND (one transaction)."""
from __future__ import annotations

from pathlib import Path

from govharness.workflows.amend import Change, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T20:00:00+00:00"
ROW_AFTER = "| OFFLD | STND | Accelerator offload standard | none | Reads as offload; offload has no established acronym | active |"
ROW = "| BUILD | STND | Build standard | none | Reads as build, the subject of the standard, as CODE reads as code | active |"
RATIONALE = ("Register change, ratified by the custodian on " + DATE + ": MNEM gains BUILD under STND, for the standard"
             " on building software (STND.IDENT.23). Building has no established acronym; BUILD reads as the subject"
             " of the standard, as CODE reads as code, and lies at a letter distance of at least 3 from each"
             " mnemonic under STND (STND.IDENT.17, STND.IDENT.18)."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "MNEM/_doc.md", [(ROW_AFTER, ROW_AFTER + "\n" + ROW)])
    rec = record_transaction(root, Change(kind="register", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.37", "GOV.41"], targets=["MNEM"], scope=["MNEM"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "MNEM")
