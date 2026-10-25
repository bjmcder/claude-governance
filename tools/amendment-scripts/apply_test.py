"""Rehearsable adoption script: STND.TEST 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_test as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-25T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.TEST, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's directions"
    " of 2026-10-24 that a standard at LVL2, every provision a default, give the method by which the work meets"
    " RSRC.11 and RSRC.12, which keep the obligation, and leave the evaluation of performance to a separate"
    " standard, and on the custodian's ruling of 2026-10-25 that the full suite run before each advance of the main"
    " line and at a stated cadence on the development line, that merges into the development line run a wider"
    " selection of the affected tests, and that merges below it run selections that widen with the level of"
    " integration: 19 provisions, all defaults, language, test framework, build tool, and vendor agnostic. Tiers and"
    " levels of tests stated, and verdict inputs, the execution path that runs a test included, derivable"
    " (STND.TEST.1 and STND.TEST.2); selections derived from the change and the verdict inputs within the tiers of"
    " their integration depth, with each omission recorded and run at a later merge or the release, the inputs that"
    " widen a selection, tiers that widen as the integration depth falls to every tier at the development line, a"
    " full-suite run, which executes every test and for which no reused verdict stands, completed before the release"
    " record is presented and at a stated cadence on the development line, misses of a selection recorded as"
    " defects of its rule, verdicts reused in selections only under an unchanged key and never for a failure, a"
    " flaky test, or a test that reads a secret, and the record of a run (STND.TEST.3 to STND.TEST.9); runs between"
    " merges limited to the tests that the changes and the last failures reach, and runs before a merge to the"
    " selection of STND.TEST.5, a full-suite run excepted (STND.TEST.10); the evidence of a"
    " failure kept before a rerun, a pass after a failure reported as unexplained until diagnosed, flaky tests"
    " tracked as defects and quarantine recorded with a bound, and tests independent of order (STND.TEST.11 to"
    " STND.TEST.14); partial oracles with their limits, generated inputs, adequacy measures reported and no"
    " threshold on coverage, and acceptance tests traced to acceptance criteria (STND.TEST.15 to STND.TEST.18); and"
    " tests changed with their code identified from the change and the source of each expected value stated"
    " (STND.TEST.19). No provision binds and none raises the floor (GOV.11): each asks only what RSRC, VV, REPRO,"
    " INTPR, or QA already ask, at the cost of wording, a statement in the repository configuration, a run, or one"
    " record, and the honest report of verdicts already binds through PRIME.2, VV.7, AGENT.4, AGENT.5, and AGENT.47."
    " Transition (GOV.42): none, because no project instrument cites a draft of it. STND.WPROC 1.1 and STND.CREW 1.1,"
    " adopted after it, cite it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair"
    " review, and a verification of each revised draft; record review-records/round-2026-10-24-test-perf/test/."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_TEST:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/TEST"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
