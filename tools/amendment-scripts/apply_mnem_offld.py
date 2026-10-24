"""Rehearsable register change: MNEM gains OFFLD under STND (one transaction)."""
from __future__ import annotations

from pathlib import Path

from govharness.workflows.amend import Change, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T18:00:00+00:00"  # set to the time of application once ratified
ROW_AFTER = ("| OMP | STND | OpenMP standard | none | The prefix that OpenMP gives its own routines and environment variables"
             " | active |")
ROW = "| OFFLD | STND | Accelerator offload standard | none | Reads as offload; offload has no established acronym | active |"
RATIONALE = ("Register change, ratified by the custodian on " + DATE + ": MNEM gains OFFLD under STND, for the standard"
             " on offloading work to accelerators (STND.IDENT.23)."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "MNEM/_doc.md", [(ROW_AFTER, ROW_AFTER + "\n" + ROW)])
    rec = record_transaction(root, Change(kind="register", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.37", "GOV.41"], targets=["MNEM"], scope=["MNEM"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "MNEM")
