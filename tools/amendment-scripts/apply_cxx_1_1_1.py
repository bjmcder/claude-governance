"""Rehearsable editorial amendment: STND.CXX 1.1.1, citing STND.BUILD for the general rules of settings and warnings
and relating STND.CXX.27 to the Reporting build of STND.BUILD.

One transaction. STND.CXX 1.1 is applied before STND.BUILD is adopted, so it names the general rules in words; this
amendment replaces the words by the citation. It applies after STND.BUILD 1.0.1: apply_round_2026_10_24.py runs it
after apply_build_1_0_1. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_cxx_1_1_1.py
(on a corpus that holds STND.CXX 1.1 and STND.BUILD).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T21:21:00+00:00"

OLD = ("The general rules for the settings of each compilation and for the warnings that fail the checks of a "
       "change, of which STND.CXX.4 and STND.CXX.25 are the C++ forms, belong to the standard for building software, "
       "which holds them for every language.")
NEW = ("STND.BUILD.11 and STND.BUILD.12 are the general rules for the settings of each compilation and for the "
       "warnings that fail the checks of a change, of which STND.CXX.4 and STND.CXX.25 are the C++ forms, and they "
       "reach further, to the settings of each link step and to each tool of the toolchain.")

TERMS = [
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them; "
     "Safety-related component has the meaning that STND.CLASS gives it.",
     "Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them; "
     "Safety-related component has the meaning that STND.CLASS gives it; Reporting build has the meaning that "
     "STND.BUILD gives it."),
]

OLD27 = "Library checks therefore remain a second layer that STND.CXX.27 lets a budget remove."
NEW27 = ("Library checks therefore remain a second layer that STND.CXX.27 lets a budget remove. Each reporting build "
         "is a build from which the work reports a result or makes a release, and so a build that STND.CXX.27 "
         "reaches; the words of STND.CXX.27 do not leave out, as the term Reporting build does, a build from which "
         "the work reports only the verdict of a test.")

READING = ("the informative Notes cite STND.BUILD.11 and STND.BUILD.12 as the general rules of which STND.CXX.4 and "
           "STND.CXX.25 are the C++ forms, where they named the standard for building software in words, and relate "
           "the builds of STND.CXX.27 to the Reporting build of STND.BUILD, a term that the Terms import; References "
           "lists STND.BUILD; no obligation changes")

ROW = f"| 1.1.1 | {DATE} | Editorial amendment (GOV.41): {READING}. |"

RATIONALE = (f"Editorial amendment of STND.CXX, revision 1.1.1, ratified by the custodian on {DATE}, on the adoption "
             f"of STND.BUILD: {READING}. The change is editorial because it replaces a description of STND.BUILD by "
             "a citation of the provisions that the Notes of STND.BUILD already name as the general rules of "
             "STND.CXX.4 and STND.CXX.25, relates the words of STND.CXX.27 to a term of STND.BUILD without changing "
             "what STND.CXX.27 asks, and changes no provision, mode, class onset, or term that this standard defines. Transition "
             "(GOV.42): none, because no obligation changes. Review: the reconciliation reviews of the round, whose "
             "items R3 and R5 this closes; records review-records/round-2026-10-24/fixpass.md and fixpass-2.md."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/CXX/_doc.md", [(OLD, NEW), (OLD27, NEW27)] + TERMS)
    raise_revision(root, "STND/CXX", "1.1", "1.1.1", ROW)
    B.write_references(root, ["STND.CXX"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CXX"], scope=["STND/CXX"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CXX 1.1.1")
