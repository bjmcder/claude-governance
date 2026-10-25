"""Rehearsable minor amendment: STND.RUST 1.1, importing Untrusted input from STND.CODE, citing the shared rules
of STND.CODE 1.2, withdrawing STND.RUST.14 in favor of STND.CODE.15, and adding the naming rule (one transaction).

WITHDRAW_RUST14 selects between the two forms that the custodian decides between (P3 dispositions, decision 4):
True (recommended) withdraws STND.RUST.14, whose outcome STND.CODE.15 binds for Rust; False keeps it as ratified,
with a citation of STND.CODE.15.

It applies after STND.CODE 1.2, whose STND.CODE.14 to STND.CODE.16 it cites, and after STND.CXX 1.2, whose withdrawn
provisions its Notes no longer cite: apply_close_p3.py runs it after apply_close_p1.py. Run from harness/, so that
govharness imports:
    python3 -B -m govharness rehearse <corpus holding P1> ../tools/amendment-scripts/apply_rust_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:15:00+00:00"

WITHDRAW_RUST14 = True

# ------------------------------------------------------------------ provisions

RUST13 = [
    ('refers_to: ["PRIME.13"]', 'refers_to: ["PRIME.13", "STND.CODE.14"]'),
    ("halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade "
     "visibly with a diagnosis (PRIME.4).",
     "halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade "
     "visibly with a diagnosis (PRIME.4, STND.CODE.14)."),
]

RUST14 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.15"]'),
    ("diagnoses each call that ignores the returned value (PRIME.4).",
     "diagnoses each call that ignores the returned value (PRIME.4, STND.CODE.15)."),
]

RUST1 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.19"]'),
    ("SHOULD build and test the work with the newest stable release of the toolchain and with the newest revisions "
     "of its dependencies that their declared ranges admit (VV.8).",
     "SHOULD build and test the work, other than its high-assurance code whose edition and toolchain STND.CODE.19 "
     "fixes, with the newest stable release of the toolchain and with the newest revisions of its dependencies that "
     "their declared ranges admit (VV.8, STND.CODE.19)."),
]

RUST15 = [
    ("refers_to: []", 'refers_to: ["STND.CODE.6", "STND.CODE.16"]'),
    ("and code compiled only under a condition that such a setting decides (PRIME.4, DSGN.2, CPS.5, CPS.9).",
     "and code compiled only under a condition that such a setting decides (PRIME.4, DSGN.2, CPS.5, CPS.9, "
     "STND.CODE.6, STND.CODE.16)."),
]

NEW35 = P(35, "Rust naming conventions", "Names", """
Each name that the Rust source of the work declares SHOULD follow the naming convention that the repository configuration names (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).
""", ["INTPR.1", "INTPR.4"], refs=["NUMER.4", "STND.DOCS.12"])

# ------------------------------------------------------------------ Purpose, Terms, Notes

IGNORED_WITHDRAWN = (
    "STND.CODE.15 applies to Rust code directly: the must_use attribute, on a function or on the type of its "
    "result, is a form of declaration that it names, so this standard holds no provision of its own on ignored "
    "results.")
IGNORED_KEPT = (
    "STND.CODE.15 applies to Rust code directly, the must_use attribute, on a function or on the type of its "
    "result, being its form. STND.RUST.14, as ratified, is met where a compiler or a static check of the work "
    "diagnoses each call that ignores the returned value; a work meets STND.CODE.15 as well only by that attribute.")

FLOOR14_OLD = (
    "STND.RUST.14 costs one attribute, one return type, or one check for each function that returns a listed "
    "failure, as STND.CXX.17 does; without it a listed failure is able to pass silently. It applies where the means "
    "of the work include a compiler or a static check that diagnoses an ignored returned value, so that it asks "
    "nothing that the means of the work are unable to give, and where they include none, STND.CODE.7 still forbids "
    "discarding a listed failure. ")
FLOOR14 = ((FLOOR14_OLD, "") if WITHDRAW_RUST14 else
           ("as STND.CXX.17 does;", "as STND.CODE.15 does in every language;"))

FRONT = [("waivable: false\n---", 'waivable: false\nwithdrawn: ["STND.RUST.14"]\n---')]

PURPOSE14 = [
    ("failures and their reporting (STND.RUST.13 to STND.RUST.17);",
     "failures and their reporting (STND.RUST.13 and STND.RUST.15 to STND.RUST.17);"),
    ("STND.RUST.13, STND.RUST.14, and STND.RUST.15 instantiate PRIME.4, STND.RUST.34 instantiates PRIME.2, and "
     "STND.RUST.6 instantiates GOV.48 and binds agents alone; these five are binding at every class.",
     "STND.RUST.13 and STND.RUST.15 instantiate PRIME.4, STND.RUST.34 instantiates PRIME.2, and STND.RUST.6 "
     "instantiates GOV.48 and binds agents alone; these four are binding at every class."),
]

DOC = [
    # Purpose
    ("and the checks of Rust code, unsafe code among it, with the claims that rest on them (STND.RUST.31 to "
     "STND.RUST.34).",
     "the checks of Rust code, unsafe code among it, with the claims that rest on them (STND.RUST.31 to "
     "STND.RUST.34); and the conventions of names (STND.RUST.35)."),
    ("The rules of concurrency that hold for every model are in STND.CONC, the rules for dependencies in STND.DEPS, "
     "and the rules of building in STND.BUILD; this standard gives their Rust forms only where Rust sets a trap of "
     "its own.",
     "The rules of concurrency that hold for every model are in STND.CONC, the rules for dependencies in STND.DEPS, "
     "the rules of building in STND.BUILD, and the rules of code that hold for every language, the responses to a "
     "listed failure and the checks that no execution setting removes among them, in STND.CODE (STND.CODE.14 to "
     "STND.CODE.21); this standard gives their Rust forms only where Rust sets a trap of its own."),
    # Terms
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, and Untrusted input have the meanings that "
     "STND.CODE gives them, and each function of the public interface of a crate of library code is in the public "
     "interface that the term Untrusted input of STND.CODE takes in;"),
    ("\n| Untrusted input | Data that reaches the work from outside its own code, including the arguments of each "
     "function of the public interface of a crate of library code, other than data from a source that the threat "
     "model of the project records as trusted. |", ""),
    # Notes: builds
    ("so that the edition of one crate holds no other back.",
     "so that the edition of one crate holds no other back. The third sentence of STND.RUST.1 leaves out the "
     "high-assurance code whose edition and toolchain STND.CODE.19 fixes, as STND.PY.14 and STND.JL.1 yield to it, "
     "so that a check at the newest stable release does not compile that code with a release that its decision "
     "record has not validated."),
    # Notes: sources
    ("which confirms the facts on the panic hook and the panic handler from the documentation of the standard "
     "library and the Rust Reference.",
     "which confirms the facts on the panic hook and the panic handler from the documentation of the standard "
     "library and the Rust Reference, and the note research/round-addenda/a2-language-facts.md (a2 below), which "
     "confirms the lints that check the case of names from the documentation of the compiler."),
    # Notes: failures
    ("Failures. STND.RUST.13 lists the responses that PRIME.4 admits in Rust, and the other provisions refer to it.",
     "Failures. STND.RUST.13 lists the responses that PRIME.4 admits in Rust, and the other provisions refer to it; "
     "its first sentence is the Rust form of STND.CODE.14, whose pass of the condition to the caller in its result, "
     "in an argument that the caller passes to receive it, or by a mechanism of the language that propagates it "
     "takes in Rust the returned condition and the panic, and its second and third add what Rust needs."),
    ("STND.RUST.14 is the Rust form of STND.CXX.17, with its two means. STND.RUST.15 is the Rust form of "
     "STND.CODE.6, and of STND.CXX.18 for the checks of CPS.5 and CPS.9:",
     (IGNORED_WITHDRAWN if WITHDRAW_RUST14 else IGNORED_KEPT) + " STND.RUST.15 is the Rust form of "
     "STND.CODE.6, and of the first sentence of STND.CODE.16 for the checks of CPS.5 and CPS.9:"),
    ("The term Untrusted input reaches the arguments of each function of the public interface of a crate of library "
     "code, as the terms of STND.PY and STND.JL reach the arguments of their public interfaces. The Notes of STND.JL "
     "record the custodian's ruling of 2026-10-23 that the reach of its term to the arguments of each declared "
     "public function raises no floor, and the Notes of STND.PY record the ruling of that date that a shape check of "
     "an argument reaches every function of the public interface at every class. Both rulings were made for those "
     "standards and not for this one; the reach of the term here rests on the argument for STND.RUST.15 in the "
     "paragraph on the floor.",
     "STND.CODE defines the term Untrusted input once for every language, and the Terms of this standard place each "
     "function of the public interface of a crate of library code in the public interface that the term takes in, "
     "as STND.PY and STND.JL place the functions of their public interfaces. The custodian's ruling of "
     "2026-10-23 that this reach raises no floor was made for STND.PY and STND.JL, and the ratification of "
     "2026-10-24 extended the reach to this standard on the argument for STND.RUST.15 in the paragraph on the "
     "floor."),
    # Notes: names, before numerics
    ("Numerics. NaN bit patterns that are not portable",
     "Names. The compiler checks the case of names by lints that warn by default: snake case for variables, "
     "methods, functions, lifetime parameters, named fields, and modules; camel case for types, variants, traits, "
     "and type parameters; and upper case for static items (a2, fact 5). The source does not say that the lint for "
     "static items covers constants, and that the Rust project publishes a convention of names is unverified. "
     "STND.RUST.35 leaves the convention to the repository configuration, as STND.STDC.39 and STND.LEAN.27 do. A "
     "configuration that names the convention of those lints has them among the static checks of STND.CODE.4, which "
     "report each departure from it, and STND.BUILD.12 asks that a change fail on each of their warnings, so the "
     "configuration names that convention at no added cost and a table fixed by this standard would add nothing. "
     "STND.RUST.35 "
     "keeps the names that the notation of NUMER.4 fixes, as STND.DOCS.12 permits, a lint that reports such a name "
     "being suppressed at its location with its reason under STND.CODE.4, and adds no table.\n\n"
     "Numerics. NaN bit patterns that are not portable"),
    # Notes: class onset
    ("STND.RUST.27, STND.RUST.28, STND.RUST.30, and the first sentence of STND.RUST.5 rest on no row and apply from "
     "CSQ3.",
     "STND.RUST.27, STND.RUST.28, STND.RUST.30, STND.RUST.35, and the first sentence of STND.RUST.5 rest on no row "
     "and apply from CSQ3."),
    # Notes: floor
    ("the reach adds no check beyond those that STND.CODE.6 keeps, only the forms that remove them.",
     "the reach adds no check beyond those that STND.CODE.6 keeps, only the forms that remove them. The term of "
     "STND.CODE also reaches a function outside library code that the documentation or the repository "
     "configuration names for use by code outside the work, a function exported over a foreign function interface "
     "among them, on the same argument: code that the work does not see calls it, and STND.RUST.15 asks only the "
     "form of a check that the code makes, at the cost of that form."),
    FLOOR14,
    ("and the same forms for a check that CPS.5 or CPS.9 already requires, as STND.CXX.18 does.",
     "and the same forms for a check that CPS.5 or CPS.9 already requires, as the first sentence of STND.CODE.16 "
     "does."),
]

READING_14 = (
    "STND.RUST.14 is withdrawn, its outcome bound for Rust by STND.CODE.15, whose form of declaration Rust "
    "provides in the must_use attribute, and the front matter lists it as withdrawn; " if WITHDRAW_RUST14 else "")

READING = (
    READING_14 + "Terms import Untrusted input from STND.CODE, delete this standard's own definition, and place each function of "
    "the public interface of a crate of library code in the public interface that the term takes in, so "
    "that the reach ratified on 2026-10-24 stays; " + (
        "STND.RUST.13 and STND.RUST.15 cite STND.CODE.14, STND.CODE.6, and STND.CODE.16, of which they are the Rust "
        "forms, with their text otherwise unchanged;" if WITHDRAW_RUST14 else
        "STND.RUST.13, STND.RUST.14, and STND.RUST.15 cite STND.CODE.14, STND.CODE.15, STND.CODE.6, and STND.CODE.16, "
        "of which they are the Rust forms, with their text otherwise unchanged;") + " the third sentence of "
    "STND.RUST.1 leaves out the high-assurance code whose edition and toolchain STND.CODE.19 fixes; new STND.RUST.35 (default, from CSQ3) leaves the convention of names to the repository "
    "configuration and keeps the names that the notation of NUMER.4 fixes, the rule of decision 9 of 2026-10-24; "
    "the Purpose cites STND.CODE for the rules of code that hold for every language and lists STND.RUST.35; the "
    "Notes cite STND.CODE.14 and STND.CODE.15 in place of the withdrawn STND.CXX.16 and STND.CXX.17, and the "
    "first sentence of STND.CODE.16 in place of STND.CXX.18 for the checks of CPS.5 and CPS.9, cite a2 for the "
    "lints that check the case of names, state the reach of the term on the ratification of 2026-10-24 with the floor argument for a "
    "function outside library code that the documentation or the repository configuration names, and give the reason for the naming "
    "rule and its class onset")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.RUST to revision 1.1, ratified by the custodian on {DATE}, on STND.CODE 1.2: "
    f"{READING}. The change is minor because it alters the defined meaning of Untrusted input for Rust, adds a "
    "default, narrows a default to yield to STND.CODE.19" + (", and withdraws a binding provision" if WITHDRAW_RUST14
                                                             else "") + "." + (
        " STND.RUST.14 is withdrawn under GOV.31: Rust provides a form of declaration, so STND.CODE.15 binds Rust "
        "code without condition, and a function that meets it meets STND.RUST.14 as well, since a function declared "
        "in a form under which each call that ignores its result is diagnosed is what STND.RUST.14 asks; "
        "the withdrawal removes the one way of meeting STND.RUST.14 that STND.CODE.15 does not admit, a static check "
        "that reports every ignored value without a declaration, which STND.CODE.15 already removes for Rust. The "
        "withdrawn identifier is listed in the field withdrawn and is never given to another provision "
        "(STND.IDENT.14)." if WITHDRAW_RUST14 else "") + " The term of STND.CODE reaches the arguments of each function of the public interface of a crate of "
    "library code, as the term of STND.RUST 1.0 did, and also each function that the documentation or the "
    "repository configuration names for use by code outside the work, the reach that STND.CODE 1.2 gives the term "
    "in every language; for a function outside library code so named, the reach is new, "
    "and the Notes argue that it raises no floor. The binding STND.RUST.13, STND.RUST.15, and STND.RUST.34" + (
        "" if WITHDRAW_RUST14 else ", and STND.RUST.14,") + " keep their obligations: the cited ones gain a citation of the "
    "provision of STND.CODE of which they are the Rust forms, and STND.RUST.34 is unchanged. Class onsets: STND.RUST.35 rests on no row of "
    "STND.CLASS.10 and applies from CSQ3; no other onset changes. Floor (GOV.11): no binding provision changes its "
    "obligation, and the floor argument for the reach of the term is the one that the ratification of 2026-10-24 "
    "accepted for STND.RUST.15, and for a function outside library code that the documentation or the "
    "repository configuration names, the same argument in the Notes, which the custodian decides (R22). Transition (GOV.42): existing Rust source conforms when a change next touches it. "
    "Review of STND.HARN.28 by the command pairs; record review-records/round-2026-10-25-close/p3/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/RUST/1.md", RUST1)
    replace_text(root, "STND/RUST/13.md", RUST13)
    if WITHDRAW_RUST14:
        (root / "STND/RUST/14.md").unlink()
    else:
        replace_text(root, "STND/RUST/14.md", RUST14)
    replace_text(root, "STND/RUST/15.md", RUST15)
    (root / "STND/RUST/35.md").write_text(B.provision_text("STND.RUST", NEW35, "adopted", DATE), encoding="utf-8")
    binding = [13, 15] if WITHDRAW_RUST14 else [13, 14, 15]
    res = B.derive_fields(root, ["STND.RUST.1", "STND.RUST.35"] + [f"STND.RUST.{n}" for n in binding])
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    if res["STND.RUST.35"].forced or res["STND.RUST.1"].forced or not all(
            res[f"STND.RUST.{n}"].forced for n in binding):
        raise ValueError("STND.RUST: a mode differs from the one this amendment states")
    replace_text(root, "STND/RUST/_doc.md", (FRONT + PURPOSE14 if WITHDRAW_RUST14 else []) + DOC)
    raise_revision(root, "STND/RUST", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.RUST"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.RUST"], scope=["STND/RUST"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.RUST 1.1")
