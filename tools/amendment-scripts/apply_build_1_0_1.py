"""Rehearsable editorial amendment: STND.BUILD 1.0.1, the boundary with STND.WFLOW stated by citation.

Applied after STND.WFLOW is adopted. Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_build_1_0_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T21:20:00+00:00"

PURPOSE_OLD = ("The steps that build software are governed by this standard; the standard for computational workflows"
               " governs the publication, retry, restart, storage, and resumption around them.")
PURPOSE_NEW = ("The steps that build software are governed by this standard; STND.WFLOW governs the publication, retry,"
               " restart, storage, and resumption around them.")

NOTES_OLD = ("Between this standard and the standard for computational workflows the rule is this: the steps that build"
             " software are governed by STND.BUILD, and the standard for computational workflows governs the"
             " publication, retry, restart, storage, and resumption around them. A build that runs as one step of a"
             " larger workflow is a step of that workflow under that standard, and its own build steps are governed"
             " here. STND.BUILD.23 keys a stored output on the content of the inputs of its step, as a workflow keys a"
             " stored output of one of its steps, and adds")
NOTES_NEW = ("Between this standard and STND.WFLOW the rule is this: the steps that build software are governed by"
             " STND.BUILD, and STND.WFLOW governs the publication, retry, restart, storage, and resumption around"
             " them. A build that runs as one step of a larger workflow is a step of that workflow under STND.WFLOW,"
             " and its own build steps are governed here. STND.BUILD.23 is the build form of STND.WFLOW.6: it keys a"
             " stored output on the content of the inputs of its step, as STND.WFLOW.6 keys a stored output of a"
             " workflow step, and adds")

READING = ("the Purpose and the Notes cite STND.WFLOW where they named the standard for computational workflows in"
           " words, the Notes name STND.BUILD.23 as the build form of STND.WFLOW.6, and References lists STND.WFLOW;"
           " no obligation changes")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}. |"

RATIONALE = (f"Editorial amendment of STND.BUILD, revision 1.0.1, ratified by the custodian on {DATE}: {READING}."
             " The change is editorial because it"
             " replaces a description of the standard for computational workflows by citations of that standard,"
             " adopted after STND.BUILD 1.0, and changes no provision and no defined term."
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/BUILD/_doc.md", [(PURPOSE_OLD, PURPOSE_NEW), (NOTES_OLD, NOTES_NEW)])
    B.write_references(root, ["STND.BUILD"])
    raise_revision(root, "STND/BUILD", "1.0", "1.0.1", ROW)
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.BUILD"], scope=["STND/BUILD"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.BUILD 1.0.1")
