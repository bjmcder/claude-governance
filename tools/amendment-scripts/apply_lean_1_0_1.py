"""Rehearsable editorial amendment: STND.LEAN 1.0.1, citing STND.CODE.14 in place of STND.CXX.16
(one transaction).

It applies after STND.CODE 1.2 and STND.CXX 1.2: apply_close_p3.py runs it after apply_close_p1.py. Run from
harness/, so that govharness imports:
    python3 -B -m govharness rehearse <corpus holding P1> ../tools/amendment-scripts/apply_lean_1_0_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:30:00+00:00"

LEAN25 = [
    ('refers_to: ["PRIME.13"]', 'refers_to: ["PRIME.13", "STND.CODE.14"]'),
    ("enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade visibly with a "
     "diagnosis (PRIME.4).",
     "enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade visibly with a "
     "diagnosis (PRIME.4, STND.CODE.14)."),
]

DOC = [
    ("and proofs that a machine generates are untrusted input, checked against a trusted statement.",
     "and proofs that a machine generates come from an untrusted author and are checked against a trusted "
     "statement."),
    ("STND.LEAN.25 states by their outcome the forms by which Lean code gives each response that PRIME.4 admits, as "
     "STND.CXX.16, STND.PY.22, and STND.JL.15 do in their languages:",
     "STND.LEAN.25 states by their outcome the forms by which Lean code gives each response that PRIME.4 admits, the "
     "Lean form of STND.CODE.14, whose pass of the condition to the caller in its result, in an argument that the "
     "caller passes to receive it, or by a mechanism of the language that propagates it takes in Lean two forms, as "
     "STND.PY.22 and STND.JL.15 give the forms of their languages:"),
    ("the custodian's ruling of 2026-10-23 on that argument was made for STND.JL.",
     "the custodian's ruling of 2026-10-23 on that argument was made for STND.JL, and the ratification of 2026-10-24 "
     "accepted it for STND.LEAN.25."),
]

READING = (
    "STND.LEAN.25 cites STND.CODE.14, of which it is the Lean form, with its text otherwise unchanged; the Notes cite STND.CODE.14 in place of STND.CXX.16, which STND.CXX 1.2 withdraws, record "
    "that the ratification of 2026-10-24 accepted the floor argument for STND.LEAN.25, and say that proofs that a "
    "machine generates come from an untrusted author, the term of this standard, in place of calling them "
    "untrusted input, a term of STND.CODE that this standard does not use")

ROW = f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Editorial amendment of STND.LEAN to revision 1.0.1, ratified by the custodian on {DATE}, on STND.CODE 1.2 and "
    f"STND.CXX 1.2: {READING}. The change is editorial because it alters no obligation, permission, or defined "
    "meaning. The citation in STND.LEAN.25 names the provision of STND.CODE that already binds Lean code and leaves "
    "the responses of STND.LEAN.25 as ratified. STND.LEAN.27, already in the form of the naming rule of decision 9 of "
    "2026-10-24, is unchanged. The Notes change their citations and not their reasons. Class onsets "
    "unchanged. No floor is raised (GOV.11). Transition (GOV.42): none, because no obligation of the work changes. "
    "Review of STND.HARN.28 by the command pairs; record review-records/round-2026-10-25-close/p3/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/LEAN/25.md", LEAN25)
    res = B.derive_fields(root, ["STND.LEAN.25"])
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    if not res["STND.LEAN.25"].forced:
        raise ValueError("STND.LEAN: a mode differs from the one this amendment states")
    replace_text(root, "STND/LEAN/_doc.md", DOC)
    raise_revision(root, "STND/LEAN", "1.0", "1.0.1", ROW)
    B.write_references(root, ["STND.LEAN"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.LEAN"], scope=["STND/LEAN"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.LEAN 1.0.1")
