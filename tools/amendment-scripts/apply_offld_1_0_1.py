"""Rehearsable editorial amendment: STND.OFFLD 1.0.1, citing STND.PERF.12 and STND.PERF.14 at STND.OFFLD.31.

One transaction. STND.PERF, adopted after STND.OFFLD, holds the costs of first use and the end of each timed
asynchronous operation for every measurement in a performance evaluation other than one of offloaded work, which
it leaves to STND.OFFLD.31 by name. STND.OFFLD.31 keeps both of its sentences, since STND.PERF holds neither for
offloaded work, and cites the sentences of STND.PERF of which it is the offload form. Run from harness/, so that
govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_offld_1_0_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:00:00+00:00"

OFFLD31 = [
    ("refers_to: []", 'refers_to: ["STND.PERF.12", "STND.PERF.14"]'),
    ("SHOULD end at an observed completion of that work (RSRC.4).",
     "SHOULD end at an observed completion of that work (RSRC.4, STND.PERF.14)."),
    ("among them initialization and compilation at load (RSRC.4).",
     "among them initialization and compilation at load (RSRC.4, STND.PERF.12)."),
]

PURPOSE = ("It adds to HW, HW.GPU, STND.ANNEX, STND.CONC, and STND.VVUQ only what offload makes necessary.",
           "It adds to HW, HW.GPU, STND.ANNEX, STND.CONC, STND.PERF, and STND.VVUQ only what offload makes "
           "necessary.")

MEASURE_OLD = ("HW.22 governs the claims that rest on such measurements, and a measurement that leaves out data "
               "movement or dispatch does not by itself support a claim that HW.22 governs.")
MEASURE_NEW = MEASURE_OLD + (
    " STND.OFFLD.31 is the form for offloaded work of the second sentences of STND.PERF.12 and STND.PERF.14, which "
    "hold the costs of first use and the end of each timed asynchronous operation for every other measurement in a "
    "performance evaluation and leave offloaded work to it, so one record meets both standards. It reaches each "
    "measurement of the time of offloaded work, in a performance evaluation or not. The first sentences of "
    "STND.PERF.12 and STND.PERF.14, on the criterion of steady state and on the resolution and cost of a timer, reach "
    "offloaded work in a performance evaluation, as they reach all other code, and this standard adds nothing to "
    "them.")

CLASS = ("STND.OFFLD.24, and STND.OFFLD.31 rest on no row and apply from CSQ3. No provision raises the floor (GOV.11).",
         "STND.OFFLD.24, and STND.OFFLD.31 rest on no row and apply from CSQ3. STND.PERF.12 and STND.PERF.14 also "
         "apply from CSQ3, so the citations of STND.OFFLD.31 move no rule to another class. No provision raises the "
         "floor (GOV.11).")

READING = ("STND.OFFLD.31 cites STND.PERF.14 at its first sentence and STND.PERF.12 at its second, the provisions "
           "whose second sentences hold the same outcomes for every other measurement in a performance evaluation "
           "and leave offloaded work to it, and its text is otherwise unchanged; the Purpose names STND.PERF among "
           "the documents to which the standard adds; the Notes state that STND.OFFLD.31 is the offload form of "
           "those sentences, that it reaches measurements outside a performance evaluation, that the first sentences "
           "of STND.PERF.12 and STND.PERF.14 reach offloaded work unchanged, and that the citations move no rule to "
           "another class; References lists STND.PERF")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation changes. |"

RATIONALE = (
    f"Editorial amendment of STND.OFFLD, revision 1.0.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.PERF: {READING}; no obligation changes. The change is editorial because it adds citations of "
    "provisions of the same level to STND.OFFLD.31 and alters the informative Purpose, Notes, and References, and "
    "no obligation, permission, mode, class onset, or defined term (STND.IDENT.3). STND.OFFLD.31 keeps both of its "
    "sentences: the second sentences of STND.PERF.12 and STND.PERF.14 open with \"Other than for offloaded work, "
    "which STND.OFFLD.31 holds\", so STND.PERF holds neither outcome for offloaded work, and dropping either "
    "sentence would leave offloaded work with no provision; STND.OFFLD.31 also reaches each measurement of the time "
    "of offloaded work, where STND.PERF reaches only a performance evaluation. What STND.PERF holds for all code, "
    "the criterion of steady state and the adequacy of a timer in the first sentences of STND.PERF.12 and "
    "STND.PERF.14, STND.OFFLD never stated, and its Notes now cite it. STND.OFFLD.31 rests on no row and applies "
    "from CSQ3, as STND.PERF.12 and STND.PERF.14 do. Transition (GOV.42): none, because no obligation changes. "
    "Review of STND.HARN.28 by the command pairs; record review-records/round-2026-10-25-close/p4/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/OFFLD/31.md", OFFLD31)
    res = B.derive_fields(root, ["STND.OFFLD.31"])
    if res["STND.OFFLD.31"].forced or res["STND.OFFLD.31"].unresolved:
        raise ValueError(f"STND.OFFLD.31: {res['STND.OFFLD.31']}")
    replace_text(root, "STND/OFFLD/_doc.md", [PURPOSE, (MEASURE_OLD, MEASURE_NEW), CLASS])
    raise_revision(root, "STND/OFFLD", "1.0", "1.0.1", ROW)
    B.write_references(root, ["STND.OFFLD"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.OFFLD"], scope=["STND/OFFLD"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.OFFLD 1.0.1")
