"""Rehearsable adoption script: STND.STDC 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_c as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "PLACEHOLDER: adoption of STND.STDC, revision 1.0, ratified by the custodian on " + C.DATE + ": the C standard,"
    " 38 provisions, two binding (STND.STDC.2 and STND.STDC.28) and the rest defaults,"
    " compiler, edition, platform, and tool agnostic; it applies the provisions of STND.CXX whose outcome holds for C"
    " in a C reading, and cites STND.CODE, STND.CONC, STND.DEPS, STND.DOCS, STND.BUILD, and NUMER. The lead sets this rationale"
    " at the coalesce."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_STDC:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/STDC"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
