"""Rehearsable pins of the round of 2026-10-26 (decision 4).

Five transactions, one per path, each with a scope of its own, so that each path later changes on its own:
KNOW, TAG, _PROJECT, STND/_doc.md, and README.md, which no transaction had pinned. They follow STND.HARN 1.4,
whose STND.HARN.7 admits a ".md" file as a scope and whose STND.HARN.31 makes a file that no scope reaches a
FAIL; the revision row of STND.HARN 1.4 covers the files until these are recorded. No text changes. Run after
apply_harn_1_4.py, from harness/:
    python3 -B -m govharness rehearse <corpus holding STND.HARN 1.4> ../tools/amendment-scripts/apply_pins_2026_10_26.py
"""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from govharness.workflows.amend import Change, record_transaction

DATE = "2026-10-26"
AT = "2026-10-26T12:00:07+00:00"

# Each path, with what it holds.
PATHS = [
    ("KNOW", "the knowledge base, planned"),
    ("TAG", "the tag vocabulary and its seven facets, planned"),
    ("_PROJECT", "the template of a project's LVL3 instruments"),
    ("STND/_doc.md", "the root document of the standards, planned"),
    ("README.md", "the guide to reading the corpus"),
]


def rationale(path: str, holds: str) -> str:
    return (
        f"Pin of {path}, {holds}, in its current content, recorded by the custodian on {DATE}. No transaction had "
        f"named a scope that reaches {path}, so it changed with no record (GOV.36); STND.HARN.31 makes such a file a "
        "FAIL, and STND.HARN.7 admits a \".md\" file as a scope. The path is pinned by a transaction of its own, so "
        "that it later changes on its own (Notes of STND.HARN). No text changes. Decision 4 of "
        "review-records/round-2026-10-26/decisions.md."
        " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5).")


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for n, (path, holds) in enumerate(PATHS):
        at = (start + timedelta(seconds=n)).isoformat()
        rec = record_transaction(root, Change(kind="annotate", actor="The Custodian", role="custodians", at=at,
                                              authority=["GOV.36"], targets=[], scope=[path],
                                              rationale=rationale(path, holds)))
        print("seq", rec.entry["seq"], "pin", path)
