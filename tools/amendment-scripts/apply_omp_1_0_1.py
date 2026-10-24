"""Rehearsable editorial amendment: STND.OMP 1.0.1, citing STND.OFFLD (one transaction).

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_omp_1_0_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T19:00:00+00:00"

PURPOSE_ADDS = ("It adds to STND.CONC, STND.CODE, HW, and STND.VVUQ only what",
                "It adds to STND.CONC, STND.OFFLD, STND.CODE, HW, and STND.VVUQ only what")
PURPOSE_PLANNED = ("the model-neutral rules of accelerator offload belong to a planned standard of their own;",
                   "the model-neutral rules of accelerator offload are in STND.OFFLD;")

OLD_OFFLOAD_END = ("Most of these rules are specific to the directive model of OpenMP. Completion before results are "
                   "read, the movement of data, and device arithmetic hold for every offload model, and belong to the "
                   "planned standard for offload.")
NEW_OFFLOAD_END = (
    "Most of these rules are specific to the directive model of OpenMP. STND.OFFLD holds the rules of offload that "
    "hold for every programming model, and this standard gives their OpenMP forms (GOV.31): "
    "STND.OMP.23 is the OpenMP form of STND.OFFLD.2, and its second sentence of STND.OFFLD.1 and STND.OFFLD.3; the "
    "first sentence of STND.OMP.24 of the second sentence of STND.OFFLD.23, and its second sentence of "
    "STND.OFFLD.10; STND.OMP.25 and STND.OMP.26 of STND.OFFLD.9, STND.OFFLD.10, and STND.OFFLD.11; the first "
    "sentence of STND.OMP.27 of STND.OFFLD.9; the second sentence of STND.OMP.28 of STND.OFFLD.12; STND.OMP.29 of "
    "STND.OFFLD.13; STND.OMP.30 of STND.OFFLD.14; STND.OMP.31 of STND.OFFLD.2 and STND.OFFLD.3; STND.OMP.32 of "
    "STND.OFFLD.30; and the last items of STND.OMP.3, the offload policy and the devices that the run uses, of "
    "STND.OFFLD.25. The second sentence of STND.OMP.27, on static data on a device, and the first sentence of "
    "STND.OMP.28, on the requires directive, have no form in STND.OFFLD: the first is specific to OpenMP, and HW.4 holds the second for every model. STND.OMP.30 reaches "
    "further than STND.OFFLD.14, which concerns device code and a floating-point environment that host code sets, "
    "so it stays a provision and not a citation: the specification leaves the floating-point environment "
    "unspecified inside and after a target region, and STND.OMP.30 governs every target region, so it also covers "
    "a target region that runs on the host, which is not device code in the sense of STND.OFFLD, and an "
    "environment that a target region sets, on which host code after the region would otherwise rely. Each provision of STND.OFFLD "
    "that has an OpenMP form here takes the class onset of that form, so the citations move no rule of this "
    "standard to another class.")

READING = ("the Purpose and the Notes cite STND.OFFLD, adopted in ledger entry 116, in place of a planned standard "
           "for offload; the Notes give the provision of STND.OFFLD of which each of STND.OMP.23 to STND.OMP.32 and "
           "the last items of STND.OMP.3 is the OpenMP form, and state why STND.OMP.30 stays a provision; and "
           "References lists STND.OFFLD")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation changes. |"

RATIONALE = (
    f"Editorial amendment of STND.OMP, revision 1.0.1, ratified by the custodian on {DATE}, on the adoption of "
    f"STND.OFFLD in ledger entry 116: {READING}; no obligation changes. The change is editorial because it alters "
    "only the informative Purpose, Notes, and References, and no provision, mode, citation of a provision, class "
    "onset, or defined term. No provision of STND.OMP is replaced by a citation: each sentence of STND.OMP.3 and "
    "STND.OMP.23 to STND.OMP.32 carries OpenMP content, a directive, clause, modifier, routine, internal control "
    "variable, or the offload policy, and STND.OMP.30, the candidate that the coverage record of "
    "research/offload-notes/o4-corpus-coverage.md names, reaches target regions that run on the host and the "
    "environment after a target region, which STND.OFFLD.14 does not. Numbering unchanged. Transition (GOV.42): "
    "none, because no obligation changes. Review of STND.HARN.28 by the command pairs; record "
    "review-records/round-2026-10-24/amendments/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/OMP/_doc.md", [PURPOSE_ADDS, PURPOSE_PLANNED, (OLD_OFFLOAD_END, NEW_OFFLOAD_END)])
    raise_revision(root, "STND/OMP", "1.0", "1.0.1", ROW)
    B.write_references(root, ["STND.OMP"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.OMP"], scope=["STND/OMP"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.OMP 1.0.1")
