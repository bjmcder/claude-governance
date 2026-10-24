"""Rehearsable minor amendment: STND.VVUQ 1.4, the test of generators stated by its outcome (one transaction).

STND.VVUQ.63 named one test battery in a provision; it now states the outcome that a battery decides, and the Notes
give that battery as an example. An editorial change rides with it: STND.VVUQ.2 and its row of the table of common
quantities say in plain words what they called a checkpoint, a word that STND.DFLT defines in another sense. Applied with the amendments at the start of apply_round_2026_10_24.py.
Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_vvuq_1_4.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T19:05:00+00:00"

VVUQ63 = [
    ("Each random number generator SHOULD have passed the TestU01 BigCrush battery, applied within single streams and "
     "across interleaved streams (NUMER.24, DSGN.17, REPRO.3, VV.1).",
     "Each random number generator SHOULD have passed a published battery of statistical tests of randomness, at "
     "least as demanding as the use of the generator requires and named with its revision in the record of the "
     "work, applied within single streams and across interleaved streams (NUMER.24, DSGN.17, REPRO.3, VV.1)."),
]

VVUQ2 = [
    ("A checkpoint whose restart is judged by bitwise identity SHOULD hold the complete state of the computation, its "
     "random number states included (REPRO.3).",
     "Where a computation that continues from state saved by an earlier run is judged by bitwise identity, the saved "
     "state SHOULD hold the complete state of the computation, its random number states included (REPRO.3)."),
]

DOC = [
    ("| Reruns of the same build, and restarts from a checkpoint that holds the complete state | 1 | Asserted |",
     "| Reruns of the same build, and computations continued from saved state that holds the complete state of the "
     "computation | 1 | Asserted |"),
    ("A random number generator that passes a test battery is not thereby proven sound.",
     "A random number generator that passes a test battery is not thereby proven sound. Batteries differ in power: "
     "the TestU01 library holds smaller batteries beside BigCrush, the one that STND.VVUQ.63 named before this revision. A "
     "record that names the battery applied, with its revision, lets the test be repeated as it ran."),
    ("The methods for learned surrogates here cover their numerical side; the ML profile owns learned models and "
     "leaves these methods to this standard. Methods for validation stay here; MEAS states outcomes for measured data "
     "and leaves the choice of validation metric to this standard and to the project.",
     "The methods for learned surrogates here cover their numerical side; the ML profile owns the record, the error, "
     "and the domain of a learned model (ML.2) and leaves these methods to this standard. Methods for validation stay "
     "here; MEAS states outcomes for measured data, their acquisition, calibration, and uncertainty among them "
     "(MEAS.2), and leaves the choice of validation metric to this standard and to the project."),
]

READING = ("STND.VVUQ.63 states the outcome that a test battery decides, a published battery of statistical tests of "
           "randomness at least as demanding as the use of the generator requires, named with its revision in the "
           "record of the work, in place of naming one battery; the Notes say that batteries differ in power, "
           "name BigCrush, the battery that the provision named before, beside the smaller ones of its library, and cite ML.2 and MEAS.2 for the matters that ML and MEAS own; "
           "References lists ML and MEAS; and, as an editorial change, STND.VVUQ.2 and its row of the table of "
           "common quantities speak of a computation that continues from state saved by an earlier run, in place of "
           "a checkpoint and its restart")

ROW = f"| 1.4 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.VVUQ to revision 1.4, ratified by the custodian on {DATE}, on the custodian's standing "
    f"direction that provisions name no product or tool and state the outcome that a tool or a reviewer decides "
    f"(GOV.18): {READING}. The change is minor and not editorial because the text of STND.VVUQ.63, a default, "
    "changes what it asks, and with it what a project replaces when it replaces that default (REPRO.7). The change to STND.VVUQ.2 and its row is "
    "editorial: STND.DFLT defines Checkpoint as a copy of an item's prior state kept before an action, so plain "
    "words take the place of that word in another sense, and what STND.VVUQ.2 asks is unchanged. The text of "
    "STND.VVUQ.63 adds the record of the battery and its revision, at the cost of one entry in the record of the "
    "work, and ties the strength of the battery to the use of the generator in place of naming one, so that a "
    "reviewer decides whether the battery applied is demanding enough for that use (GOV.18). Class onsets unchanged, CSQ3 for STND.VVUQ.63; both provisions stay defaults and raise no "
    "floor (GOV.11). "
    "Transition (GOV.42): none; a work whose generator passed the battery that the old text named meets the new "
    "text where that battery is as demanding as its use requires, once its record names the battery, which it "
    "does when a change next touches the generator. Review of STND.HARN.28 by the command pairs; "
    "records review-records/round-2026-10-24/fixpass.md and fixpass-2.md, from reconciliation items R19 and R12."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/VVUQ/63.md", VVUQ63)
    replace_text(root, "STND/VVUQ/2.md", VVUQ2)
    B.derive_fields(root, ["STND.VVUQ.2", "STND.VVUQ.63"])
    replace_text(root, "STND/VVUQ/_doc.md", DOC)
    raise_revision(root, "STND/VVUQ", "1.3", "1.4", ROW)
    B.write_references(root, ["STND.VVUQ"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.VVUQ"], scope=["STND/VVUQ"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.VVUQ 1.4")
