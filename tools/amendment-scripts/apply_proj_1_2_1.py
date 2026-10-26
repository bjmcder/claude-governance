"""Rehearsable editorial amendment: STND.PROJ 1.2.1, round of 2026-10-26 (decision 5).

One transaction. STND.PROJ.6 and STND.PROJ.7 stay, as the fields of a written remote-write authorization that a
reader decides; the Notes stop explaining them by a configuration that a harness derives, since STND.HARN 1.4
withdraws STND.HARN.18 and STND.HARN.29. Runs before apply_harn_1_4.py. Run from harness/, so that govharness
imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_proj_1_2_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import write_references  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-26"
AT = "2026-10-26T12:00:01+00:00"

NOTES = [
    ("STND.PROJ.6 and STND.PROJ.7 give an authorization of a remote write a form that a reader and a harness decide "
     "alike, so that a derived configuration is able to let a write that the authorization names by destination and "
     "kind proceed without referral (STND.HARN.18, STND.HARN.29).",
     "STND.PROJ.6 and STND.PROJ.7 give an authorization of a remote write a form that a reader decides by comparison, "
     "naming what it covers by destination, kind of write, and branch (GUARD.10)."),
    ("and a list of names is what a configuration is able to compare. Whether the update of a branch publishes or "
     "deploys is the human owner's record, not something a configuration is able to see;",
     "and a list of names is what a reader is able to compare. Whether the update of a branch publishes or deploys "
     "is the human owner's record;"),
    ("a standing authorization of a marked kind has no effect (GUARD.11, STND.HARN.29).",
     "a standing authorization of a marked kind has no effect (GUARD.11)."),
    ("The field `expires` holds a time, which a harness compares with the time of each write, or `until revoked`,",
     "The field `expires` holds a time, or `until revoked`,"),
    ("a condition of lapse in the scope, such as a repository that stops meeting the human owner's record, is not "
     "something a harness is able to test, and a time stated with it bounds the authorization for a harness.",
     "a condition of lapse in the scope, such as a repository that stops meeting the human owner's record, does not "
     "show in the authorization itself, and a time stated with it still bounds the authorization."),
    ("The kind other keeps the list closed while letting an authorization cover a write that no other row names; a "
     "derived configuration that does not know a kind refers its writes, which STND.HARN.18 allows.",
     "The kind other keeps the list closed while letting an authorization cover a write that no other row names."),
    ("work of CSQ4 may keep its authorizations in another form, whose remote writes a derived configuration then "
     "refers.",
     "work of CSQ4 may keep its authorizations in another form."),
]

READING = ("the Notes explain STND.PROJ.6 and STND.PROJ.7 as the form of an authorization that a reader decides by "
           "comparison, and no longer by a configuration that a harness derives, since STND.HARN 1.4 withdraws "
           "the provisions on such a configuration")
ROW = (f"| 1.2.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined meaning "
       "changes. |")

RATIONALE = (
    f"Editorial amendment of STND.PROJ, revision 1.2.1, ratified by the custodian on {DATE}: {READING}. The change "
    "is editorial under STND.IDENT.3 because only the Notes change: the fields and kinds of STND.PROJ.6 and "
    "STND.PROJ.7, their marks of irrevocable effect, and their onset stay as they are, so no obligation, permission, "
    "or defined meaning changes. Transition (GOV.42): none. Decision 5 of "
    "review-records/round-2026-10-26/decisions.md."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/PROJ/_doc.md", NOTES)
    raise_revision(root, "STND/PROJ", "1.2", "1.2.1", ROW)
    write_references(root, ["STND.PROJ"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.PROJ"], scope=["STND/PROJ"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.PROJ 1.2.1")
