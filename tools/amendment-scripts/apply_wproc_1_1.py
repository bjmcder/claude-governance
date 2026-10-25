"""Rehearsable minor amendment: STND.WPROC 1.1, citing STND.TEST (one transaction).

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
AT = "2026-10-25T20:10:00+00:00"

# STND.WPROC.9: the exception widens from a check deferred to the release to a check deferred to a later merge or
# to the release, and to a test in quarantine; the record may be a run record that the unit record cites.
WPROC9 = [
    ('refers_to: ["STND.WPROC.8"]', 'refers_to: ["STND.WPROC.8", "STND.TEST.13", "STND.TEST.9"]'),
    ("Before a branch is merged into its parent branch, each check that the change is able to affect, other than a "
     "check deferred to the release under RSRC.12 and recorded in the unit record, SHOULD pass on the branch as "
     "updated under STND.WPROC.8 (VV.8, RSRC.11, RSRC.12).",
     "Before a branch is merged into its parent branch, each check that the change is able to affect, other than a "
     "check deferred under RSRC.12 to a later merge or to the release, or a test in quarantine under STND.TEST.13, "
     "and recorded in the unit record or in a record of STND.TEST.9 that the unit record cites, SHOULD pass on the "
     "branch as updated under STND.WPROC.8 (VV.8, RSRC.11, RSRC.12, STND.TEST.13, STND.TEST.9)."),
]

DOC = [
    ("A check too costly for every merge, such as a long stochastic run or a synthesis, is deferred to the release "
     "under RSRC.12, recorded in the unit record, and run on the revision released.",
     "A check too costly for every merge, such as a long stochastic run or a synthesis, is deferred to the release "
     "under RSRC.12, recorded in the unit record, and run on the revision released. STND.TEST.3 and STND.TEST.5 "
     "have a test of a tier that the selection of a merge does not draw on run at the first merge nearer the "
     "development line whose depth draws on its tier, and at the latest at the merge into the development line, "
     "a deferral under RSRC.12 like the one to the release; a test in quarantine under STND.TEST.13 is one on "
     "whose verdict no merge relies, and QA.6 still has an actor restore a check that its own change broke. "
     "STND.WPROC.9 has the unit record state each such test, or cite the record of the run under STND.TEST.9 that "
     "states it. STND.TEST holds the selection of the checks that a change is able to affect, and the full-suite "
     "run before a release."),
]

READING = ("STND.WPROC.9 excepts from the checks that pass before a merge a check deferred under RSRC.12 to a later "
           "merge or to the release, and a test in quarantine under STND.TEST.13, each recorded in the unit record "
           "or in a record of STND.TEST.9 that the unit record cites, where it excepted a check deferred to the "
           "release only; the Notes say how STND.TEST.5 defers the tests of a tier to a nearer merge, that QA.6 "
           "still applies to a check that the change broke, and that STND.TEST governs the selection and the "
           "full-suite run; References lists STND.TEST")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.WPROC to revision 1.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.TEST: {READING}. The change is minor under the test of STND.IDENT.3 because it alters a permission: the "
    "exception of STND.WPROC.9 widens, so that a merge may proceed with more checks deferred or in quarantine; it "
    "alters no prime directive or governing principle, so it is not major. "
    "Without it, a merge that draws its selection from the tiers of its integration depth under STND.TEST.5, or "
    "that relies on no verdict of a quarantined test under STND.TEST.13, departs from STND.WPROC.9 and so loses "
    "the authority of STND.WPROC.11 to merge without a decision of the human owner. RSRC.12 already defers verification to the latest decision point at "
    "which its result is still needed and never lets deferral become omission (GOV.7), and STND.TEST.5 has every "
    "tier drawn at the merge into the development line and STND.TEST.6 a full-suite run before each release. "
    "STND.WPROC.9 still instantiates VV.8, RSRC.11, and RSRC.12, rests on no row of STND.CLASS.10, and applies from "
    "CSQ3. No floor is raised (GOV.11), and STND.WPROC.12 and STND.WPROC.13 do not change. Transition (GOV.42): "
    "none, because no project instrument relies on the narrower exception. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-24-test-perf/test/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/WPROC/9.md", WPROC9)
    B.derive_fields(root, ["STND.WPROC.9"])
    replace_text(root, "STND/WPROC/_doc.md", DOC)
    raise_revision(root, "STND/WPROC", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.WPROC"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.WPROC"], scope=["STND/WPROC"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.WPROC 1.1")
