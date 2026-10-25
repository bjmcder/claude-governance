"""Rehearsable minor amendment: STND.STDC 1.1, citing STND.CODE for the shared rules of compiled languages in
place of the C reading of them, importing Untrusted input, and adding the naming rule (one transaction).

It applies after STND.CODE 1.2, whose STND.CODE.14 to STND.CODE.20 it cites, and before STND.CXX 1.2, which
withdraws the provisions of STND.CXX that STND.STDC.1 and STND.STDC.2 listed until this revision:
apply_close_p1.py runs it second. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse <corpus holding STND.CODE 1.2> ../tools/amendment-scripts/apply_stdc_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:05:00+00:00"

# ------------------------------------------------------------------ provisions

STDC1 = [
    ('"RSRC.4", "VV.1", "HW.5"]', '"RSRC.4", "HW.5"]'),
    (', "STND.CXX.27", "STND.CXX.28", "STND.CXX.30", "STND.CXX.31"]', ', "STND.CXX.27"]'),
    ("REPRO.2, REPRO.3, REPRO.7, SIMPL.6, RSRC.4, VV.1, HW.5).", "REPRO.2, REPRO.3, REPRO.7, SIMPL.6, RSRC.4, HW.5)."),
    ("| STND.CXX.28 | CSQ1, for high-assurance code | None |\n"
     "| STND.CXX.30 | CSQ1, for high-assurance code | None |\n"
     "| STND.CXX.31 | CSQ4, where a high-assurance coding standard is adopted | None |\n", ""),
]

STDC2_OLD_BODY = (
    "The C reading of each provision of STND.CXX that the table of this provision lists SHALL apply to the C source "
    "of the work, each sentence keeping its modal (PRIME.4, PRIME.2, DSGN.2, CPS.5, CPS.9).\n\n"
    "| Provision | Change in its C reading |\n"
    "| --- | --- |\n"
    "| STND.CXX.16 | The responses are those of the provision other than a C++ exception; a report of the condition "
    "through errno alone is not a return of the condition in the result |\n"
    "| STND.CXX.17 | It applies where the means of the work include a compiler or a static check that diagnoses a call "
    "that ignores a returned value |\n"
    "| STND.CXX.18 | None |\n"
    "| STND.CXX.29 | None |\n")
STDC2_NEW_BODY = (
    "Where C code passes a condition that PRIME.4 lists to its caller in a result, as STND.CODE.14 admits, it SHALL "
    "report that condition in its return value or in an object that its contract names for it, and not through "
    "errno alone (PRIME.4, STND.CODE.14).\n")
STDC2 = [
    ('title: "Binding C++ provisions applied to C"', 'title: "C responses to listed failures"'),
    ('section: "Provisions of STND.CXX"', 'section: "Failures"'),
    ('instantiates: ["PRIME.4", "PRIME.2", "DSGN.2", "CPS.5", "CPS.9"]', 'instantiates: ["PRIME.4"]'),
    ('refers_to: ["STND.CXX.16", "STND.CXX.17", "STND.CXX.18", "STND.CXX.29"]', 'refers_to: ["STND.CODE.14"]'),
    (STDC2_OLD_BODY, STDC2_NEW_BODY),
]

STDC28 = [
    ('refers_to: ["STND.CXX.16"]', 'refers_to: ["STND.CODE.14", "STND.STDC.2"]'),
    ("answer a failure that it finds as the C reading of STND.CXX.16 provides (DSGN.1).",
     "answer a failure that it finds as STND.CODE.14 and STND.STDC.2 provide (DSGN.1)."),
]
STDC30 = [
    ('refers_to: ["STND.CXX.16", "STND.STDC.28"]', 'refers_to: ["STND.STDC.28", "STND.CODE.14", "STND.STDC.2"]'),
    ("SHOULD be tested and answered as the C reading of STND.CXX.16 provides (DSGN.1).",
     "SHOULD be tested and answered as STND.CODE.14 and STND.STDC.2 provide (DSGN.1)."),
]

STDC31 = [
    ('refers_to: []', 'refers_to: ["STND.STDC.2"]'),
    ("or by an object that its contract names as its result for failures (DSGN.1).",
     "or by an object that its contract names as its result for failures, as STND.STDC.2 binds for a listed "
     "condition (DSGN.1, STND.STDC.2)."),
]

NEW40 = P(40, "Finite-value options in C", "Undefined behavior", """
A translation unit of C source that holds a check of a floating-point value that STND.CODE.6, CPS.5, or CPS.9 requires SHALL NOT be compiled with an option that lets the compiler assume that floating-point values are finite (PRIME.4, DSGN.2, STND.CODE.21).
""", ["PRIME.4", "DSGN.2", "CPS.5", "CPS.9"], refs=["STND.CODE.6", "STND.CODE.21"], mode="binding")

NEW39 = P(39, "C naming conventions", "Names", """
Each name that the C source of the work declares SHOULD follow the naming convention that the repository configuration names (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).
""", ["INTPR.1", "INTPR.4"], refs=["NUMER.4", "STND.DOCS.12"])

# ------------------------------------------------------------------ Purpose, Terms, Notes

DOC = [
    # Purpose
    ("It applies to C source each provision of STND.CXX whose outcome holds for C, in a C reading that its Terms "
     "define, in place of restating it (STND.STDC.1 and STND.STDC.2), records",
     "It applies to C source each default of STND.CXX whose outcome holds for C, in a C reading that its Terms "
     "define, in place of restating it (STND.STDC.1), states the C form of the responses to a failure that PRIME.4 "
     "lists (STND.STDC.2), states for C the binding form of STND.CXX.18 on the option that assumes finite values "
     "(STND.STDC.40), "
     "records"),
    ("data that crosses to other languages (STND.STDC.36), and the checks of C code (STND.STDC.37 and STND.STDC.38). "
     "Through STND.STDC.1 and STND.STDC.2, the high-assurance provisions of STND.CXX apply to C: conformance to the "
     "high-assurance coding standard that a decision record of the work adopts, claims of conformance limited to "
     "what was checked, an edition that the standard covers and the toolchain is validated for, and recorded "
     "deviations.",
     "data that crosses to other languages (STND.STDC.36), the checks of C code (STND.STDC.37 and STND.STDC.38), and "
     "names (STND.STDC.39). STND.CODE holds for C, as for every language, the responses to a failure that PRIME.4 "
     "lists, the declarations that keep a returned failure from being ignored, the checks that no execution setting "
     "and no definition in the source removes, and the high-assurance provisions: conformance to the high-assurance "
     "coding standard that a decision record of the work adopts, claims of conformance limited to what was checked, "
     "an edition that the standard covers and the toolchain is validated for, and recorded deviations (STND.CODE.14, "
     "STND.CODE.15, STND.CODE.16, STND.CODE.17, STND.CODE.18, STND.CODE.19, and STND.CODE.20)."),
    ("STND.STDC.2 instantiates PRIME.4 and PRIME.2, and is binding at every class.",
     "STND.STDC.2 and STND.STDC.40 instantiate PRIME.4 and are binding at every class."),
    # Terms
    ("Repository configuration and Static check have the meanings that STND.CODE gives them.",
     "Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and "
     "High-assurance coding standard have the meanings that STND.CODE gives them."),
    ("and with the change that the row of that provision in the table of STND.STDC.1 or STND.STDC.2 gives. |",
     "and with the change, if any, that the row of that provision in the table of STND.STDC.1 gives. |"),
    ("\n| Untrusted input | Data that reaches the work from outside its own code, other than data from a source that "
     "the threat model of the project records as trusted. |", ""),
    # Notes: sources
    ("(cited as a1) for the facts on streams, and a fact that neither note supports is marked unverified.",
     "(cited as a1) for the facts on streams and research/round-addenda/a2-language-facts.md (cited as a2) for the "
     "assert macro and the options that assume finite values, and a fact that none of these notes supports is marked "
     "unverified."),
    # Notes: the C reading
    ("STND.STDC.1 and STND.STDC.2 apply those provisions to C source in their C reading, so that each keeps one text "
     "and its mode, and this standard holds only what C adds (GOV.31).",
     "STND.STDC.1 applies the defaults among those provisions to C source in their C reading, so that each keeps one "
     "text and its mode, and this standard holds only what C adds (GOV.31). The rules that C shares with C++ and "
     "with every other language, the responses to a listed failure and the high-assurance provisions among them, are "
     "in STND.CODE, which applies to C by its own scope, and STND.STDC.2 gives the C form of one of them."),
    # Notes: provisions of STND.CXX that apply
    (" STND.CXX.16 keeps every response but a C++ exception, and its row adds that a report through errno alone is "
     "not a return of the condition. STND.CXX.17 is met by the attribute that an edition provides for a result not "
     "to be discarded, or by a compiler's equivalent (c1, Error reporting and ignored returns). STND.CXX.18 holds as "
     "written: NDEBUG removes an assertion, and an option that assumes finite values removes a test for non-finite "
     "values. NDEBUG set by an option of the compiler is an execution setting, so a check of untrusted input written "
     "as an assertion that it removes, the case of STND.PY.25 and STND.JL.13, is a check that STND.CODE.6 forbids in "
     "every language and that STND.CXX.18 cites, and this standard adds no provision for it.", ""),
    (" STND.CXX.28 to STND.CXX.31 refer to the high-assurance coding standard that a decision record adopts, a term "
     "that reads \"for C\" in its C reading.", ""),
    # Notes: new paragraph on STND.CODE, before the provisions of STND.CXX that do not apply
    ("Provisions of STND.CXX that do not apply.",
     "Provisions of STND.CODE for every language. STND.CODE.14 admits every response but a C++ exception; a "
     "nonlocal jump is a mechanism of C that carries a condition past its callers, and STND.STDC.31 governs it. "
     "STND.STDC.2 adds that a report through errno alone does not pass the condition to the caller. STND.CODE.15 is "
     "met by the attribute that an edition provides for a result not to be discarded, or by a compiler's equivalent "
     "(c1, Error reporting and ignored returns). The assert macro is the C case of STND.CODE.6 and of the second "
     "sentence of STND.CODE.16, whose Notes give the reasoning from the C header (a2, N3220 7.2). An option that assumes finite "
     "values may remove a test for non-finite values (a2); STND.CODE.21 "
     "recommends against it in every language, and STND.STDC.40 states for C, in the words of STND.CXX.18, the "
     "binding form that the table of "
     "STND.STDC.2 applied to C in revision 1.0; a later change of STND.CXX.18 does not change it. C places no function in the public interface by a construct of the "
     "language, because external linkage also serves the calls between the translation units of one program, so "
     "the documentation or the repository configuration names the interface for outside use of the term Untrusted "
     "input, and a check of an argument of a function that it names is a check of untrusted input under "
     "STND.CODE.6, STND.STDC.21, and STND.STDC.27. Where such an argument is a pointer that carries no extent, the "
     "check of STND.STDC.21 is possible only against an extent or a limit that the contract states, as STND.STDC.7 "
     "and STND.STDC.27 provide. The two coding standards for C in c1 are high-assurance coding standards in the "
     "sense of STND.CODE, and the published coverage of one ends below the newest edition and of the other at an "
     "older one (c1, S28, S29, and S40), so STND.CODE.19 fixes the edition of high-assurance code at a covered one "
     "unless a decision record admits a feature of a later edition. Conformance reduces undefined behavior by a "
     "mechanical check and is not evidence that a result is correct (VV.1).\n\n"
     "Provisions of STND.CXX that do not apply."),
    # Notes: names
    ("The naming table of STND.CXX.14 is the custodian's convention for C++, and names in C follow STND.DOCS.12 and "
     "the layout tool of STND.CODE.5.",
     "The naming table of STND.CXX.14 is the custodian's convention for C++. C has no convention of names of its own "
     "that a tool is able to check, so STND.STDC.39 leaves the convention to the repository configuration, as "
     "STND.LEAN.27 does for Lean, keeps the names that the notation of NUMER.4 fixes, and adds no table; STND.DOCS.12 "
     "still asks one name for each concept."),
    # Notes: failures, streams, ignored results
    ("escapes the diagnosis of STND.CXX.17, which the row of STND.CXX.16 excludes.",
     "escapes the diagnosis of STND.CODE.15, which STND.STDC.2 excludes."),
    ("its tests are one means to the outcome that PRIME.4 and the C reading of STND.CXX.16 ask,",
     "its tests are one means to the outcome that PRIME.4, STND.CODE.14, and STND.STDC.2 ask,"),
    ("because a coding standard is adopted under a default (STND.CXX.28)",
     "because a coding standard is adopted under a default (STND.CODE.17)"),
    # Notes: high assurance, now in the paragraph on STND.CODE
    ("High assurance. The two coding standards for C in c1 are suited to adoption under the C reading of "
     "STND.CXX.28, and the published coverage of one ends below the newest edition and of the other at an older one "
     "(c1, S28, S29, and S40), so the C reading of STND.CXX.30 fixes the edition of high-assurance code at a covered "
     "one unless a decision record admits a feature of a later edition. Conformance reduces undefined behavior by a "
     "mechanical check and is not evidence that a result is correct (VV.1).\n\n", ""),
    # Notes: floor
    ("Floor. STND.STDC.2 is binding and rests on PRIME.4 and PRIME.2 alone. The C reading of STND.CXX.16 admits only "
     "the responses of PRIME.4 and the return of the condition to a caller that responds; its row's exclusion of "
     "errno alone is text new to this standard, without which the condition is lost at the next call. The C reading "
     "of STND.CXX.17 asks one attribute per function where the edition or the toolchain provides one, and otherwise "
     "a static check that diagnoses the ignored result; without either, a returned listed failure is ignored "
     "silently. Its row has it apply where the means of the work include such a compiler or static check, so that a "
     "toolchain without either blocks no work, and STND.CODE.7 still forbids discarding a listed failure there. The "
     "C reading of STND.CXX.18 keeps in every build a check that CPS.5, CPS.9, or STND.CODE.6 requires, at the cost "
     "of one choice of option. The C reading of STND.CXX.29 asks a claim of conformance to name the means that "
     "checked it, which PRIME.2 asks of every claim. None asks for work that PRIME.4 or PRIME.2 does not, so none "
     "raises the floor (GOV.11). The rulings that STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29 raise no "
     "floor were made for C++; the argument for C, the errno clause and the static check where no attribute exists "
     "included, is the one above. STND.STDC.2 binds at every class; the C reading of STND.CXX.29 reaches only "
     "high-assurance code, never below CSQ1.",
     "Floor. STND.STDC.2 is binding and rests on PRIME.4 alone. It adds to STND.CODE.14 only that a report of a "
     "listed condition through errno alone does not pass it to the caller, without which the condition is lost at "
     "the next call that sets errno; the cost is the report of the condition in the return value or in an object "
     "that the contract names, which STND.CODE.14 already admits as the response. It asks for no work that PRIME.4 "
     "does not, so it raises no floor (GOV.11), the argument that the ratification of 2026-10-24 accepted for the "
     "errno clause of STND.STDC 1.0. STND.STDC.40 keeps for C the binding form of STND.CXX.18, which the same "
     "ratification applied to C through the table of STND.STDC.2, at the cost of one choice of option for a unit that "
     "holds a required check. For C the hazard is this: the documentation of two compilers states the option as a "
     "license to assume that arguments and results are not NaNs or infinities (a2), the removal of a test by "
     "isnan or isfinite under it is unverified, and the binding form stays for C by the ratification of 2026-10-24, "
     "while STND.CODE.21 is the default for every other language. Both bind at every class. The "
     "binding provisions of STND.CODE that reach C, STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, "
     "STND.CODE.16, and STND.CODE.18, carry the floor arguments that the Notes of STND.CODE give for each language."),
]

READING = (
    "STND.STDC.1 no longer lists STND.CXX.28, STND.CXX.30, and STND.CXX.31, whose outcomes STND.CODE.17, "
    "STND.CODE.19, and STND.CODE.20 now hold for every language, and drops VV.1, which only those rows needed; "
    "STND.STDC.2, retitled C responses to listed failures and moved to the section Failures, replaces its table of "
    "the C readings of STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29 by the one change that C needs, that a "
    "listed condition passed to the caller is reported in the return value or in an object that the contract names "
    "and not through errno alone, and instantiates PRIME.4 alone; it keeps its identifier for the errno clause of its "
    "own table, and no identifier is given to another provision; new STND.STDC.40 (binding, PRIME.4) states in C "
    "words the row of STND.CXX.18, the option that assumes finite values, which the table of STND.STDC.2 held; the C "
    "readings of STND.CXX.16, STND.CXX.17, and STND.CXX.29 give way to STND.CODE.14, STND.CODE.15, and STND.CODE.18; "
    "STND.STDC.28 and STND.STDC.30 cite STND.CODE.14 and STND.STDC.2 in place of the C reading of STND.CXX.16, and "
    "STND.STDC.31 cites STND.STDC.2 for a listed condition; new STND.STDC.39 (default, from CSQ3) leaves the "
    "convention of names to the repository configuration and keeps the names that the notation of NUMER.4 fixes, "
    "the rule of decision 9 of 2026-10-24; Terms import Untrusted input, Execution setting, High-assurance code, and "
    "High-assurance coding standard from STND.CODE and delete this standard's own definition of Untrusted input, "
    "which gains the reach of the interface for outside use that the documentation or the repository configuration "
    "names; the Notes cite STND.CODE for the shared rules and for the reasoning on the assert macro, give the C "
    "facts, the nonlocal jump, the check of a pointer argument without an extent, and the reason for the naming "
    "rule, and restate the floor argument for STND.STDC.2 and STND.STDC.40")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.STDC to revision 1.1, ratified by the custodian on {DATE}, on STND.CODE 1.2: {READING}. "
    "The change is minor because it removes obligations from this standard's text that STND.CODE now holds, alters "
    "the binding STND.STDC.2, adds a default, and alters the defined meaning of Untrusted input for C. The "
    "obligations of C source are those of STND.STDC 1.0 with three changes: the term Untrusted input reaches the "
    "arguments of each function of the interface for outside use that the documentation or the repository "
    "configuration names; the second sentence of STND.CODE.16 reaches an assertion that a definition of NDEBUG in "
    "the source turns off, the case that STND.CODE.6 did not reach; and STND.STDC.39 is new. STND.STDC.40 states as a "
    "provision of its own the row of STND.CXX.18 that the table of STND.STDC.2 held, so its obligation does not "
    "change. The C reading of STND.CXX.17 held a condition on the means of the work that STND.CODE.15 states as a "
    "form of declaration. Class onsets: STND.STDC.2 and STND.STDC.40 bind at every class; STND.STDC.39 rests on no "
    "row of STND.CLASS.10 and applies from CSQ3; the onsets of the rows that STND.STDC.1 keeps are unchanged. Floor "
    "(GOV.11): STND.STDC.2 asks only the report of a listed condition that STND.CODE.14 already admits, in a form that "
    "keeps it from being lost, at the cost of its wording, and STND.STDC.40 one choice of option, the arguments that "
    "the ratification of 2026-10-24 accepted for STND.STDC 1.0; the floor arguments for the provisions of STND.CODE "
    "that reach C are in the Notes of STND.CODE, and the custodian decides their reach to C (R22). Transition "
    "(GOV.42): existing C source conforms when a change next touches it. Review of STND.HARN.28 by the command "
    "pairs, a cold review, and their dispositions; record review-records/round-2026-10-25-close/p1/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/STDC/1.md", STDC1)
    replace_text(root, "STND/STDC/2.md", STDC2)
    replace_text(root, "STND/STDC/28.md", STDC28)
    replace_text(root, "STND/STDC/30.md", STDC30)
    replace_text(root, "STND/STDC/31.md", STDC31)
    for p in (NEW39, NEW40):
        (root / f"STND/STDC/{p['n']}.md").write_text(B.provision_text("STND.STDC", p, "adopted", DATE),
                                                      encoding="utf-8")
    res = B.derive_fields(root, ["STND.STDC.1", "STND.STDC.2", "STND.STDC.28", "STND.STDC.30", "STND.STDC.31", "STND.STDC.39",
                                 "STND.STDC.40"])
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    if res["STND.STDC.39"].forced or not res["STND.STDC.2"].forced or not res["STND.STDC.40"].forced:
        raise ValueError("STND.STDC: a mode differs from the one this amendment states")
    replace_text(root, "STND/STDC/_doc.md", DOC)
    raise_revision(root, "STND/STDC", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.STDC"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.STDC"], scope=["STND/STDC"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.STDC 1.1")
