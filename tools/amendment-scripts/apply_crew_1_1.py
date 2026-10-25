"""Rehearsable minor amendment: STND.CREW 1.1, citing STND.TEST (one transaction).

Applied after the adoption of STND.TEST. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_test_round.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:15:00+00:00"

# STND.CREW.9: the self-review runs the tests that STND.TEST.10 selects.
CREW9 = [
    ('refers_to: []', 'refers_to: ["STND.TEST.10"]'),
    ("Before an implementing agent hands a change to review, it SHOULD examine the change against its acceptance "
     "criteria and fix each finding (QA.2, VV.8).",
     "Before an implementing agent hands a change to review, it SHOULD examine the change against its acceptance "
     "criteria, run the tests that STND.TEST.10 selects for the change, and fix each finding (QA.2, VV.8, "
     "STND.TEST.10)."),
]

# STND.CREW.15: the review agent also receives the run records on which the change relies.
CREW15 = [
    ('refers_to: ["AGENT.2", "AGENT.47"]', 'refers_to: ["AGENT.2", "AGENT.47", "STND.TEST.9"]'),
    ("and the ambiguous instructions acted on that the author's work report states under AGENT.47, and only the "
     "other context needed to judge them (QA.7, QA.8).",
     "and the ambiguous instructions acted on that the author's work report states under AGENT.47, the record of "
     "STND.TEST.9 of each run of tests on which the change relies, and only the other context needed to judge them "
     "(QA.7, QA.8, STND.TEST.9)."),
]

DOC = [
    ("and reviews its own change before handing it to review (STND.CREW.9); that self-review is not the review of "
     "QA.7.",
     "and reviews its own change before handing it to review, running the tests that STND.TEST.10 selects for it "
     "(STND.CREW.9); that self-review is not the review of QA.7."),
    ("so that it judges the change as a cold reader would (STND.CREW.15).",
     "so that it judges the change as a cold reader would (STND.CREW.15). It also receives the record of each run "
     "of tests on which the change relies, which shows what was selected, reused, omitted, and excluded, so that the "
     "review of STND.TEST.19 compares the change and its runs with what the work report states."),
]

READING = ("STND.CREW.9 has the implementing agent run, in its self-review, the tests that STND.TEST.10 selects for "
           "the change; STND.CREW.15 gives the review agent the record of STND.TEST.9 of each run of tests on which "
           "the change relies; the Notes say so; References lists STND.TEST")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.CREW to revision 1.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.TEST: {READING}. The change is minor and not editorial because the text of two defaults changes, and "
    "with it what a project replaces when it replaces them (REPRO.7). The self-review of STND.CREW.9 already "
    "examines the change against its acceptance criteria under VV.8; the tests that STND.TEST.10 selects are the "
    "smallest set that does so between merges (RSRC.11), so the citation adds a named run and no other obligation. "
    "STND.CREW.15 already gives the review agent the checks that the work report states as skipped or weakened; the "
    "run record adds what the runs show apart from the report, which the review of STND.TEST.19 uses to find a "
    "test removed or loosened by the change itself. Both still instantiate QA.2, VV.8, QA.7, and QA.8 as before, "
    "rest on no row of STND.CLASS.10, and apply from CSQ3. No floor is raised (GOV.11). Transition (GOV.42): none, "
    "because the run records are those that STND.TEST.9 already asks. Review of STND.HARN.28 by the command pairs; "
    "record review-records/round-2026-10-24-test-perf/test/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/CREW/9.md", CREW9)
    replace_text(root, "STND/CREW/15.md", CREW15)
    B.derive_fields(root, ["STND.CREW.9", "STND.CREW.15"])
    replace_text(root, "STND/CREW/_doc.md", DOC)
    raise_revision(root, "STND/CREW", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.CREW"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CREW"], scope=["STND/CREW"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CREW 1.1")
