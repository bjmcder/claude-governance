"""Rehearsable minor amendment: STND.FTN 1.1, importing Untrusted input from STND.CODE, citing the shared rules
of STND.CODE 1.2 in place of the withdrawn rules of STND.CXX, and adding the naming rule (one transaction).

New: STND.FTN.37. STND.FTN.18 stays a default, as ratified.
It applies after STND.CODE 1.2 and STND.CXX 1.2: apply_close_p3.py runs it after apply_close_p1.py. Run from
harness/, so that govharness imports:
    python3 -B -m govharness rehearse <corpus holding P1> ../tools/amendment-scripts/apply_ftn_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:20:00+00:00"

# ------------------------------------------------------------------ provisions

FTN29 = [
    ('refers_to: ["PRIME.13"]', 'refers_to: ["PRIME.13", "STND.CODE.14"]'),
    ("degrade visibly with a diagnosis, or return the condition in its result or in a status argument (PRIME.4).",
     "degrade visibly with a diagnosis, or return the condition in its result or in a status argument (PRIME.4, "
     "STND.CODE.14)."),
]

FTN18 = [
    ('refers_to: ["STND.CODE.6", "CPS.5", "CPS.9"]', 'refers_to: ["STND.CODE.6", "CPS.5", "CPS.9", "STND.CODE.21"]'),
    ("lets the compiler assume that floating-point values are finite (DSGN.2).",
     "lets the compiler assume that floating-point values are finite (DSGN.2, STND.CODE.21)."),
]

FTN31 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.6"]'),
    ("at the entry of the untrusted input or at the first point after it at which that bound is known (PRIME.4, "
     "DSGN.2).",
     "at the entry of the untrusted input or at the first point after it at which that bound is known (PRIME.4, "
     "DSGN.2, STND.CODE.6)."),
]

NEW37 = P(37, "Fortran naming conventions", "Names", """
Each name that the Fortran source of the work declares SHOULD follow the naming convention that the repository configuration names (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).
""", ["INTPR.1", "INTPR.4"], refs=["NUMER.4", "STND.DOCS.12"])

# ------------------------------------------------------------------ the document

DOC = [
    # Purpose
    ("legacy source and its modernization without a change of results (STND.FTN.33 and STND.FTN.34); and the checks "
     "of Fortran code at run time (STND.FTN.35 and STND.FTN.36).",
     "legacy source and its modernization without a change of results (STND.FTN.33 and STND.FTN.34); the checks of "
     "Fortran code at run time (STND.FTN.35 and STND.FTN.36); and the conventions of names (STND.FTN.37)."),
    ("STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4, so they are binding and apply at every class.",
     "STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4, so they are binding and apply at every class. "
     "The rules of code that hold for every language, the responses to a listed failure and the checks that no "
     "execution setting removes among them, are in STND.CODE (STND.CODE.14 to STND.CODE.21), and this standard "
     "gives their Fortran forms."),
    # Terms
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them.",
     "Repository configuration, Static check, Execution setting, and Untrusted input have the meanings that "
     "STND.CODE gives them. For the term Untrusted input, the values that a procedure receives through its dummy "
     "arguments are its arguments, and each procedure that a module of the work makes public, by an attribute, by a "
     "statement, or by default, and each procedure of the work with the BIND attribute, is in the public interface "
     "that the term Untrusted input of STND.CODE takes in."),
    ("\n| Untrusted input | Data that reaches the work from outside its own code, including the values that each "
     "procedure that a module of the work makes public, by an attribute, by a statement, or by default, and each "
     "procedure of the work with the BIND attribute, receive through their dummy arguments, other than data from a "
     "source that the threat model of the project records as trusted. |", ""),
    # Notes: floating-point exceptions
    ("STND.FTN.18 is therefore a default, at the cost of one choice of option for a file that holds a required "
     "check, and no binding provision rests on the hazard; STND.CXX.18 binds the same sentence for C++.",
     "STND.FTN.18 is therefore a default, at the cost of one choice of option for a file that holds a required "
     "check, and no binding provision rests on the hazard; STND.CXX.18 binds the same sentence for C++. STND.FTN.18 "
     "is the Fortran form of the first sentence of STND.CODE.21, stated for each source file, since an option of a "
     "Fortran compiler applies to the files that it compiles."),
    # Notes: failures
    ("which a subroutine makes in a status argument because it has no result (STND.FTN.29, in the form of "
     "STND.CXX.16, STND.PY.22, and STND.JL.15).",
     "which a subroutine makes in a status argument because it has no result (STND.FTN.29, the Fortran form of "
     "STND.CODE.14)."),
    ("The term Untrusted input takes the reach of the public interface that STND.PY and STND.JL give it: the values "
     "received by each procedure that a module makes public, an entity of a module being public unless the module "
     "makes it private, and by each procedure with the BIND attribute; it leaves out external procedures, which in "
     "legacy code are the internal structure of a program; the custodian's ruling of 2026-10-23 that this reach "
     "raises no floor was made for STND.PY and STND.JL.",
     "STND.CODE defines the term Untrusted input once for every language, and the Terms of this standard place in "
     "the public interface that the term takes in each procedure that a module makes public, an entity of a module being "
     "public unless the module makes it private, and each procedure with the BIND attribute, as STND.PY and STND.JL "
     "place the functions of their public interfaces. The custodian's ruling of 2026-10-23 that this reach raises no "
     "floor was made for STND.PY and STND.JL, and the ratification of 2026-10-24 extended the reach to this "
     "standard. An external procedure that the documentation or the repository configuration names for use by code "
     "outside the work is in the interface for outside use of STND.CODE, and the paragraph on the floor argues that "
     "reach; an external procedure that nothing names is not, which keeps out the external procedures that in legacy "
     "code are the internal structure of a program."),
    # Notes: names, before the binding provisions
    ("Binding provisions. STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4",
     "Names. The research note holds no convention of names that the Fortran standard fixes and a tool checks, so "
     "STND.FTN.37 leaves the convention to the repository configuration, as STND.STDC.39 and STND.LEAN.27 do, keeps "
     "the names that the notation of NUMER.4 fixes, as STND.DOCS.12 permits, and adds no table.\n\n"
     "Binding provisions. STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4"),
    # Notes: floor
    ("STND.FTN.29 lists the responses that PRIME.4 admits, in the form of STND.CXX.16, STND.PY.22, and STND.JL.15.",
     "STND.FTN.29 lists the responses that PRIME.4 admits, in their Fortran form, and admits none that STND.CODE.14 "
     "does not."),
    ("the custodian's ruling of 2026-10-23 on that reach was made for STND.PY and STND.JL.",
     "the custodian's ruling of 2026-10-23 on that reach was made for STND.PY and STND.JL, and the ratification of "
     "2026-10-24 extended it to this standard on this argument. The same argument holds for an external procedure "
     "that the documentation or the repository configuration names for use by code outside the work, which the term "
     "of STND.CODE adds to that reach: code that the work does not see calls it, and STND.FTN.31 asks, for a "
     "subscript that such a procedure receives, the check that DSGN.2 already asks where untrusted input enters, in "
     "the form that no execution setting removes, at the cost of one test for each such subscript; an external "
     "procedure that nothing names for such use stays outside the reach."),
    # Notes: class onset
    ("each default instantiates only DSGN, SIMPL, REPRO, VV, or a provision of NUMER or HW,",
     "each default instantiates only DSGN, SIMPL, REPRO, VV, INTPR, or a provision of NUMER or HW,"),
]

READING = (
    "Terms import Untrusted input from STND.CODE, delete this standard's own "
    "definition, and place each procedure that a module makes public and each procedure with the BIND attribute in "
    "the public interface that the term takes in, so that the reach ratified on 2026-10-24 stays; "
    "STND.FTN.29, STND.FTN.31, and STND.FTN.18 cite STND.CODE.14, STND.CODE.6, and STND.CODE.21, of which they are "
    "the Fortran forms, with their text otherwise unchanged, STND.FTN.18 staying a default; new STND.FTN.37 (default, from CSQ3) leaves the convention of names to the "
    "repository configuration and keeps the names that the notation of NUMER.4 fixes, the rule of decision 9 of "
    "2026-10-24; the Purpose cites STND.CODE for the rules of code that hold for every language and lists "
    "STND.FTN.37; the Notes cite STND.CODE.14 in place of the withdrawn STND.CXX.16, call STND.FTN.18 the Fortran "
    "form of STND.CODE.21, state the reach of the term on the "
    "ratification of 2026-10-24 with the floor argument for an external procedure that the documentation or the "
    "repository configuration names, give the reason for the naming rule, and add INTPR to the class onsets")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.FTN to revision 1.1, ratified by the custodian on {DATE}, on STND.CODE 1.2: "
    f"{READING}. The change is minor because it adds a default and alters the defined meaning of Untrusted input "
    "for Fortran. STND.FTN.18 stays a default, as ratified on 2026-10-24, beneath the default STND.CODE.21. The term of STND.CODE reaches the values that each module-public procedure and each procedure "
    "with the BIND attribute receive, as the term of STND.FTN 1.0 did, and also each procedure that the "
    "documentation or the repository configuration names for use by code outside the work, the one reach that the "
    "ratification of 2026-10-24 gave the term in every language; for an external procedure so named, the reach is "
    "new, and the Notes argue that it raises no floor. The binding STND.FTN.29, STND.FTN.30, and "
    "STND.FTN.31 keep their obligations: STND.FTN.29 and STND.FTN.31 gain a citation of the provision of STND.CODE "
    "of which they are the Fortran forms, and STND.FTN.30 is unchanged. Class onsets: STND.FTN.37 rests on no row "
    "of STND.CLASS.10 and applies from CSQ3; no other onset changes. Floor (GOV.11): no binding provision of this "
    "standard changes its obligation; the reach of the term to an external procedure that the documentation or the "
    "repository configuration names costs only the form of a check that the code makes, the argument in the Notes, "
    "which the custodian decides (R22). Transition (GOV.42): existing Fortran source conforms when a change next touches it. Review of "
    "STND.HARN.28 by the command pairs; record review-records/round-2026-10-25-close/p3/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/FTN/18.md", FTN18)
    replace_text(root, "STND/FTN/29.md", FTN29)
    replace_text(root, "STND/FTN/31.md", FTN31)
    (root / "STND/FTN/37.md").write_text(B.provision_text("STND.FTN", NEW37, "adopted", DATE), encoding="utf-8")
    res = B.derive_fields(root, ["STND.FTN.18", "STND.FTN.29", "STND.FTN.31", "STND.FTN.37"])
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    if res["STND.FTN.37"].forced or res["STND.FTN.18"].forced or not (res["STND.FTN.29"].forced and res["STND.FTN.31"].forced):
        raise ValueError("STND.FTN: a mode differs from the one this amendment states")
    replace_text(root, "STND/FTN/_doc.md", DOC)
    raise_revision(root, "STND/FTN", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.FTN"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.FTN"], scope=["STND/FTN"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.FTN 1.1")
