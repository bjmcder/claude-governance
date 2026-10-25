"""Rehearsable adoption script: STND.PERF 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_perf as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.PERF, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's directions"
    " of 2026-10-24 that a standard separate from the standard on test suites hold the systematic evaluation of the"
    " absolute, relative, and scaling performance of code where a task calls for it or the code is declared"
    " performance-sensitive, that every provision be a default, and that no provision name a method, tool, event,"
    " product, or version: 26 provisions, all defaults, citing RSRC, HW.20, HW.22, STND.VVUQ.77, STND.OFFLD.31,"
    " and AGENT.40 for what they hold. Evaluation where a task calls for it or the code is performance-sensitive, and the"
    " content of a performance requirement (STND.PERF.1 and STND.PERF.2); the question stated, the yardstick of an"
    " absolute question, the conditions of a relative comparison, the scaling variable and baseline, and the range of a scaling"
    " claim (STND.PERF.3 to STND.PERF.7); the method and quantities recorded, the limits of the method, and an"
    " attribution confirmed before an optimization rests on it (STND.PERF.8 to STND.PERF.10); levels of repetition,"
    " steady state and first use, the environment and order of runs, the timer and completion, the timed span, and"
    " the validity of benchmarks (STND.PERF.11 to STND.PERF.16); the summary statistic and dispersion, raw samples"
    " and exclusions, differences against a practical threshold, false alarms across a suite, and no rerun of a"
    " failed check without a rule recorded beforehand (STND.PERF.17 to STND.PERF.21); the record of each point of a performance"
    " history, regression guards on performance, and regressions attributed and resolved (STND.PERF.22 to STND.PERF.24); and"
    " the smallest evaluation first and the resources held for a measurement on a shared machine"
    " (STND.PERF.25 and STND.PERF.26). No provision binds and none raises the floor (GOV.11): each asks only what"
    " RSRC, VV, REPRO, INTPR, SIMPL, or AGENT.40 already ask, at the cost of wording or one record, and PRIME.8"
    " already bounds the spending of every evaluation. Transition (GOV.42): none, because no project instrument"
    " cites a draft of it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review,"
    " and a verification of each revised draft, with dispositions; record review-records/round-2026-10-24-test-perf/perf/."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_PERF:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/PERF"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
