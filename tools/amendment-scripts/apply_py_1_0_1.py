"""Rehearsable editorial amendment: STND.PY 1.0.1, citing STND.CONC (one transaction).

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_py_1_0_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T19:02:00+00:00"

ANCHOR = "a stream chosen by worker or process identity, or copied into forked processes, differs between runs."
NOTE = (" STND.PY.17 states for the work in Python the rule of STND.CONC.23, which keys each stream of a computation divided among "
        "concurrent tasks to a part defined independently of the number of tasks and of the task that computes it. "
        "STND.PY.17 reaches further: it governs each division of work into parts, parts run as separate runs "
        "included, which STND.CONC.23 does not reach; both apply from CSQ3.")

READING = ("the informative Notes cite STND.CONC.23 as the model-neutral rule that STND.PY.17 states for the work in "
           "Python, and state the wider scope of STND.PY.17, and References lists STND.CONC")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation changes. |"

RATIONALE = (
    f"Editorial amendment of STND.PY, revision 1.0.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.CONC in ledger entry 112: {READING}; no obligation changes. The change is editorial because it alters "
    "only the informative Notes and References, and no provision or defined term. STND.PY.17 is not replaced by a "
    "citation: it reaches work divided into parts that are not concurrent tasks of one run, which STND.CONC.23 does not, and STND.CONC.23 "
    "adds for concurrent tasks that the part be defined independently of the number of tasks and of the task that "
    "computes it. Class onset unchanged, CSQ3. Transition (GOV.42): none, because no obligation changes. Review of "
    "STND.HARN.28 by the command pairs; record review-records/round-2026-10-24/amendments/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/PY/_doc.md", [(ANCHOR, ANCHOR + NOTE)])
    raise_revision(root, "STND/PY", "1.0", "1.0.1", ROW)
    B.write_references(root, ["STND.PY"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.PY"], scope=["STND/PY"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.PY 1.0.1")
