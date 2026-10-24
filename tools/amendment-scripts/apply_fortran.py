"""Rehearsable adoption script: STND.FTN 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_fortran as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "[Placeholder rationale; the lead sets it at the coalesce.] Adoption of STND.FTN, revision 1.0, ratified by the"
    " custodian on " + C.DATE + ", on the custodian's order of standards of 2026-10-24 (Fortran, classic and modern)"
    " and the standing directions: 36 provisions, three binding under PRIME.4 (STND.FTN.29, STND.FTN.30, and"
    " STND.FTN.31) and 33 defaults, agnostic of compiler, vendor, tool, and revision of the Fortran standard, citing"
    " STND.BUILD, STND.CONC, STND.MPI, and STND.OMP and adding only what Fortran makes necessary."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_FTN:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/FTN"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
