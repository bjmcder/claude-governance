"""Rehearsable adoption script: STND.RUST 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_rust as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "PLACEHOLDER: adoption of STND.RUST, revision 1.0, to be ratified by the custodian on " + C.DATE + ", on the"
    " placeholder: a standard that holds the coding practice that Rust makes necessary, agnostic of"
    " toolchain release and timeless, citing STND.CONC, STND.CODE, STND.DEPS, and STND.BUILD for what they hold: 33"
    " provisions, five binding (STND.RUST.6, STND.RUST.13, STND.RUST.14, STND.RUST.15, and STND.RUST.33) and the rest"
    " defaults."
    " The lead sets this rationale at the coalesce."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_RUST:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/RUST"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
