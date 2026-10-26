"""Rehearsable editorial amendments: HW.GPU 1.0.2 and HW.QPU 1.0.2, round of 2026-10-26 (decision 5).

Two transactions, each with the scope of the family HW. The Notes of each state the referral of a submission
that no authorization covers by PRIME.7 and PRIME.14, in place of STND.HARN.18 and the transition of ledger
entry 53, since STND.HARN 1.4 withdraws STND.HARN.18. Run before apply_harn_1_4.py, from harness/:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_hw_remote_1_0_2.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import write_references  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-26"
AT = "2026-10-26T12:00:02+00:00"

OLD = ("Under STND.HARN.18 and the transition of ledger entry 53, each remote write is referred unless an "
       "authorization in force names its destination and kind.")
NEW = "A submission that no authorization in force covers is one that PRIME.7 and PRIME.14 have the agent halt and refer."

READING = ("the Notes state the referral of a submission that no authorization covers by PRIME.7 and PRIME.14, in "
           "place of the provision of STND.HARN on a derived configuration, which STND.HARN 1.4 withdraws")
ROW = (f"| 1.0.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined meaning "
       "changes. |")


def rationale(ident: str) -> str:
    return (
        f"Editorial amendment of {ident}, revision 1.0.2, ratified by the custodian on {DATE}: {READING}. The change "
        "is editorial under STND.IDENT.3 because one informative sentence now cites the prime directives from which "
        "the referral follows for an agent, in place of a provision on a harness; no obligation, permission, or "
        "defined meaning changes. Transition (GOV.42): none. Decision 5 of "
        "review-records/round-2026-10-26/decisions.md."
        " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def _amend(root: Path, folder: str, ident: str, at: str) -> None:
    replace_text(root, f"{folder}/_doc.md", [(OLD, NEW)])
    raise_revision(root, folder, "1.0.1", "1.0.2", ROW)
    write_references(root, [ident])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.41"], targets=[ident], scope=["HW"],
                                          rationale=rationale(ident)))
    print("seq", rec.entry["seq"], ident, "1.0.2")


def apply(root: Path) -> None:
    root = Path(root)
    # The second transaction takes the next second, so that each entry has a time of its own.
    later = (datetime.fromisoformat(AT) + timedelta(seconds=1)).isoformat()
    _amend(root, "HW/GPU", "HW.GPU", AT)
    _amend(root, "HW/QPU", "HW.QPU", later)
