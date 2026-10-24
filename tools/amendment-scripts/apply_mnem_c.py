"""Rehearsable register change: MNEM gains STDC under STND (one transaction)."""
from __future__ import annotations

from pathlib import Path

from govharness.workflows.amend import Change, record_transaction, replace_text

DATE = "2026-10-24"
AT = "2026-10-24T20:00:00+00:00"
ROW_AFTER = "| OFFLD | STND | Accelerator offload standard | none | Reads as offload; offload has no established acronym | active |"
ROW = ("| STDC | STND | C standard | none | The prefix that the ISO C standard gives its own predefined macros and"
       " pragmas; avoids C, one letter, and CC (Creative Commons, cubic centimeter) | active |")
RATIONALE = ("Register change, ratified by the custodian on " + DATE + ": MNEM gains STDC under STND, for the standard"
             " on C (STND.IDENT.23). STDC is the prefix that the ISO C standard gives its own predefined macros and"
             " pragmas, which STND.IDENT.18 admits as the established name of what it names, as OMP is for OpenMP;"
             " the one letter of the language is below the two letters that STND.IDENT.17 requires, and CC, the name"
             " of the C compiler in build tools, reads as Creative Commons and as a unit of volume (STND.IDENT.18)."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "MNEM/_doc.md", [(ROW_AFTER, ROW_AFTER + "\n" + ROW)])
    rec = record_transaction(root, Change(kind="register", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.37", "GOV.41"], targets=["MNEM"], scope=["MNEM"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "MNEM")
