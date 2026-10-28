"""Round d of 2026-10-28: the language standards, in citation order.

STND.FTN 1.2, STND.LEAN 1.1, STND.CXX 1.4, STND.STDC 1.3, STND.JL 1.4, STND.PY 1.3, and STND.RUST 1.3. Each keeps
only the sentences that name a construct of its language, cites STND.CODE and STND.DEPS for the rest, and drops
its citations of the provisions that a later document of the round withdraws before that document runs.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

REC = "review-records/rounds-2026-10-28/round-d/decisions.md"
REG = "review-records/deep-review-2026-10-28/register.md"


def body_of(root: Path, rel: str) -> str:
    return (Path(root) / rel).read_text(encoding="utf-8").partition("\n---\n\n")[2]


def edit(root: Path, rel: str, pairs: list[tuple[str, str]], **fields: object) -> None:
    """Replace texts in a provision and set the front-matter fields given."""
    replace_text(root, rel, pairs)
    if fields:
        F.set_body(root, rel, body_of(root, rel), **fields)


def tail(rulings: str) -> str:
    return f" Transition (GOV.42): none. {rulings}" + F.AUTHOR


# ---------------------------------------------------------------- STND.FTN 1.2

FTN_DOC = [
    ("failures (STND.FTN.29 to STND.FTN.32);", "failures (STND.FTN.30, STND.FTN.31, and STND.FTN.32);"),
    ("(STND.FTN.33 and STND.FTN.34); the checks of Fortran code at run time (STND.FTN.35 and STND.FTN.36); and the "
     "conventions of names (STND.FTN.37).",
     "(STND.FTN.33 and STND.FTN.34); and the checks of Fortran code at run time (STND.FTN.35 and STND.FTN.36)."),
    ("STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4, so they are binding and apply at every class. "
     "The rules of code that hold for every language, the responses to a listed failure and the checks that no "
     "execution setting removes among them, are in STND.CODE (STND.CODE.14 to STND.CODE.21),",
     "STND.FTN.30 and STND.FTN.31 instantiate PRIME.4, so they are binding and apply at every class. The rules of "
     "code that hold for every language, the responses to a listed failure, the checks that no execution setting "
     "removes, and the convention of names among them, are in STND.CODE (STND.CODE.14 to STND.CODE.35),"),
    ("which cites the clause numbers of the J3 working document of the 2023 revision (its S1),",
     "which cites the clause numbers of the J3 working document of the latest revision that it read (its S1),"),
    ("confirms the facts on initialization and the SAVE attribute from the J3 working document of the 2023 revision.",
     "confirms the facts on initialization and the SAVE attribute from the same working document."),
    ("STND.VVUQ.1, STND.VVUQ.3, and STND.VVUQ.5 set each comparison within a tolerance, and Fortran has no intrinsic "
     "comparison within a tolerance whose defaults would need a provision, as those of STND.PY.20 and STND.JL.21 do;",
     "STND.VVUQ.1, STND.VVUQ.3, and STND.VVUQ.5 set each comparison within a tolerance, and STND.CODE.31 has the "
     "comparison state their parameters, which Fortran, with no intrinsic comparison within a tolerance, states in "
     "the expression;"),
    ("The list has grown at most revisions, and the 2023 revision added none (S2),",
     "The list has grown at most revisions, and the latest revision that the note read added none (S2),"),
    ("this has held since Fortran 90, and before that it was processor dependent (S1 4.3.8).",
     "this has held since the revision that introduced free source form, and before that it was processor "
     "dependent (S1 4.3.8)."),
    ("that note read the working document of the 2023 revision alone,",
     "that note read the working document of the latest revision alone,"),
    ("The first sentence of STND.CODE.21 keeps code that holds such a check from an option that, by the documentation "
     "of its compiler, lets the compiler assume finite values, as a default for every language, at the cost of one "
     "choice of option for a file that holds a required check; no binding provision rests on the hazard for "
     "Fortran, and STND.CXX.18 binds the same sentence for C++.",
     "STND.CODE.21 keeps code that holds a required check of such a value from an option that, by the documentation "
     "of its compiler, lets the compiler assume finite values, in every language, Fortran included, at the cost of "
     "one choice of option for a file that holds such a check."),
    ("locality specifiers came with the 2018 revision and REDUCE with the 2023 revision (S1 C.1, S2),",
     "locality specifiers came with a recent revision and REDUCE with the revision after it (S1 C.1, S2),"),
    ("(STND.FTN.29, the Fortran form of STND.CODE.14, whose pass of the condition to the caller",
     "(STND.CODE.14, whose pass of the condition to the caller"),
    ("and the return of the condition under STND.FTN.29 remains open there.",
     "and the return of the condition under STND.CODE.14 remains open there."),
    ("so STND.FTN.37 leaves the convention to the repository configuration, as STND.STDC.39 and STND.LEAN.27 do, keeps "
     "the names that the notation of NUMER.4 fixes, as STND.DOCS.12 permits, and adds no table.",
     "so STND.CODE.28 leaves the convention of Fortran source to the repository configuration and keeps the names "
     "that the notation of NUMER.4 fixes, and this standard adds no table."),
    ("STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4 and bind at every class, CSQ4 included. The "
     "argument that none raises the floor (GOV.11) is this. STND.FTN.29 lists the responses that PRIME.4 admits, in "
     "their Fortran form, and admits none that STND.CODE.14 does not: a status argument is an argument that the "
     "caller passes to receive the condition. STND.FTN.30",
     "STND.FTN.30 and STND.FTN.31 instantiate PRIME.4 and bind at every class, CSQ4 included. The argument that "
     "neither raises the floor (GOV.11) is this. STND.CODE.14 admits in Fortran the result of a function and the "
     "status argument, an argument that the caller passes to receive the condition, and admits no other pass to "
     "the caller. STND.FTN.30"),
]
FTN_READING = (
    "STND.FTN.29 is withdrawn, STND.CODE.14 holding the Fortran responses, the status argument among them, and "
    "STND.FTN.37 is withdrawn, its outcome being STND.CODE.28 for every language, and the front matter lists both "
    "as withdrawn; STND.FTN.16 and STND.FTN.30 cite STND.CODE.14 in place of STND.FTN.29; the Purpose, the Notes on "
    "failures, comparisons, names, and the binding provisions follow; the Notes name the revisions of the Fortran "
    "standard by their order in place of their numbers, which ruling D1 takes out of the Notes; References drop "
    "STND.LEAN and STND.STDC")
FTN_RATIONALE = (
    f"Minor amendment of STND.FTN, revision 1.2, ratified by the custodian on {F.DATE}: {FTN_READING}. The change is "
    "minor under STND.IDENT.3 because it removes two provisions. STND.FTN.29 admitted no response that STND.CODE.14 "
    "does not, a status argument being an argument that the caller passes to receive the condition, and "
    "STND.FTN.37 had the text that STND.CODE.28 states for every language, so Fortran code keeps each outcome; "
    "STND.FTN.16 and STND.FTN.30 ask the same response under the new citation. The custodian ruled under D1 that "
    "STND.CODE.14 carries the forms of each language and that one provision holds each outcome. STND.FTN.30 and "
    "STND.FTN.31 stay binding, and nothing binds that did not, so no floor is raised (GOV.11). Class onsets: "
    "unchanged. The withdrawn identifiers are listed in the field withdrawn and are never given to another "
    "provision (STND.IDENT.14)."
    + tail(f"Ruling D1 of {F.RECORD}; register entry R6.2 (CL4, CL5, CL18) and R7.1 of {REG}; decisions 2, 3, 7, "
           f"and 15 of {REC}."))


def apply_ftn(root: Path, at: str) -> None:
    root = Path(root)
    F.withdraw(root, "STND/FTN", "STND.FTN", [29, 37])
    edit(root, "STND/FTN/30.md", [("as STND.FTN.29 requires", "as STND.CODE.14 requires")],
         refers_to=["STND.CODE.14"])
    edit(root, "STND/FTN/16.md", [("by a response that STND.FTN.29 lists", "by a response that STND.CODE.14 lists")],
         refers_to=["STND.CODE.14"])
    F.check_fields(root, ["STND.FTN.16"])
    F.check_fields(root, ["STND.FTN.30"], binding=True)
    replace_text(root, "STND/FTN/_doc.md", FTN_DOC)
    row = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {FTN_READING}. |"
    F.finish(root, "STND/FTN", "STND.FTN", "1.1.1", "1.2", row, FTN_RATIONALE, at)


# ---------------------------------------------------------------- STND.LEAN 1.1

LEAN_DOC = [
    ("Lean programs (STND.LEAN.25, STND.LEAN.26, and STND.LEAN.27);",
     "Lean programs (STND.LEAN.26 and STND.LEAN.27);"),
    ("STND.LEAN.5 instantiates PRIME.2 and STND.LEAN.25 instantiates PRIME.4, so these two are binding and apply at "
     "every class.",
     "STND.LEAN.5 instantiates PRIME.2, so it is binding and applies at every class, and STND.CODE.14 holds for Lean "
     "the responses to a condition that PRIME.4 lists, in the Lean forms that its Notes give."),
    ("STND.LEAN.25 states by their outcome the forms by which Lean code gives each response that PRIME.4 admits, the "
     "Lean form of STND.CODE.14, whose pass of the condition to the caller in its result, in an argument that the "
     "caller passes to receive it, or by a mechanism of the language that propagates it takes in Lean two forms, as "
     "STND.PY.22 and STND.JL.15 give the forms of their languages: a result of a type that carries the condition, "
     "and an error raised in a monad whose caller receives it.",
     "STND.CODE.14 holds for Lean code the responses that PRIME.4 admits, and its pass of the condition to the "
     "caller in its result, in an argument that the caller passes to receive it, or by a mechanism of the language "
     "that propagates it takes in Lean two forms, which the Notes of STND.CODE name: a result of a type that carries "
     "the condition, and an error raised in a monad whose caller receives it."),
    ("l1 does not discuss them (unverified), so the provision names none of them.",
     "l1 does not discuss them (unverified), so no provision names them."),
    ("STND.LEAN.25 adds the forms of Lean to PRIME.4 at the cost of its wording, the argument that the Notes of "
     "STND.JL give for STND.JL.15; the custodian's ruling of 2026-10-23 on that argument was made for STND.JL, and "
     "the ratification of 2026-10-24 accepted it for STND.LEAN.25.",
     "The two forms ask nothing that PRIME.4 does not, so STND.CODE.14 raises no floor for Lean (GOV.11), the "
     "argument that the ratification of 2026-10-24 accepted for the Lean forms."),
    ("STND.LEAN.27 leaves the convention to the repository configuration, where STND.CXX.14, STND.PY.1, and "
     "STND.JL.6 fix one, and keeps the names that the notation of NUMER.4 fixes, as they do.",
     "STND.LEAN.27 leaves the convention to the repository configuration and keeps the names that the notation of "
     "NUMER.4 fixes, the rule that STND.CODE.28 states for every language."),
    ("STND.LEAN.5 instantiates PRIME.2 and STND.LEAN.25 instantiates PRIME.4, and both apply at every class, CSQ4 "
     "included.",
     "STND.LEAN.5 instantiates PRIME.2 and applies at every class, CSQ4 included."),
    ("by the arguments above for STND.LEAN.5 and STND.LEAN.25.", "by the argument above for STND.LEAN.5."),
]
LEAN_READING = (
    "STND.LEAN.25 is withdrawn, STND.CODE.14 holding the Lean responses, a result of a type that carries the "
    "condition and an error raised in a monad among them, and the front matter lists it as withdrawn; the Purpose, "
    "the Notes on programs, and the class paragraph drop it and cite STND.CODE.14; the Notes cite STND.CODE.28 for "
    "the rule that STND.LEAN.27 states; References drop STND.PY")
LEAN_RATIONALE = (
    f"Minor amendment of STND.LEAN, revision 1.1, ratified by the custodian on {F.DATE}: {LEAN_READING}. The change "
    "is minor under STND.IDENT.3 because it removes one provision. STND.LEAN.25 admitted no response that "
    "STND.CODE.14 does not: a result of a type that carries the condition is a pass in the result, and an error "
    "raised in a monad whose caller receives it is a mechanism of the language that propagates the condition, so "
    "Lean code keeps the outcome, bound at every class by STND.CODE.14. The custodian ruled under D1 that "
    "STND.CODE.14 carries the forms of each language. Nothing binds that did not, so no floor is raised (GOV.11). "
    "Class onsets: unchanged. STND.LEAN.27 stays, since the Notes of STND.SV cite it; a later round withdraws it. "
    "The withdrawn identifier is listed in the field withdrawn and is never given to another provision "
    "(STND.IDENT.14)."
    + tail(f"Ruling D1 of {F.RECORD}; register entry R6.2 (CL4) of {REG}; decisions 2 and 3 of {REC}."))


def apply_lean(root: Path, at: str) -> None:
    root = Path(root)
    F.withdraw(root, "STND/LEAN", "STND.LEAN", [25])
    replace_text(root, "STND/LEAN/_doc.md", LEAN_DOC)
    row = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {LEAN_READING}. |"
    F.finish(root, "STND/LEAN", "STND.LEAN", "1.0.1", "1.1", row, LEAN_RATIONALE, at)


# ---------------------------------------------------------------- STND.CXX 1.4

CXX1_BODY = (
    "The repository configuration SHOULD name a published guide of C++ practice, at a recorded revision, as the "
    "reference for the C++ practice of the work, and list each of its rules that the checks of STND.CXX.25 exclude "
    "and each from which the work knowingly deviates, with the reason (INTPR.1, REPRO.7). Where this standard and "
    "that guide differ, the work SHOULD follow this standard (INTPR.1).")
CXX14 = [("A name whose form a dependency, the standard library, a published interface of the work, or the "
          "documented notation of NUMER.4 fixes MAY keep that form (INTPR.1, INTPR.4).",
          "A name whose form a dependency, the standard library, or a published interface of the work fixes MAY keep "
          "that form (INTPR.1).")]
CXX21_BODY = (
    "Where the release of an owned resource is able to report a failure that affects a result, its resource handle "
    "SHOULD provide an operation that releases it and returns that failure, called before the result is relied upon "
    "(DSGN.1). A destructor that detects a failed release SHOULD respond to it as STND.CODE.14 or STND.CODE.12 "
    "provides, without letting a C++ exception escape (DSGN.1).")
CXX25_BODY = (
    "The static checks that the repository configuration names for C++ SHOULD include the warnings of each compiler "
    "of the toolchain matrix at a recorded set, a check of the rules of the guide of STND.CXX.1 that the work "
    "follows, and a check of the names of STND.CXX.14 (DSGN.3).")
CXX_DOC = [
    ("It takes the C++ Core Guidelines as the reference for the work's practice",
     "It takes the guide of C++ practice that the repository configuration names as the reference for the work's "
     "practice"),
    ("It covers failures, including the option that assumes finite values, the status returns and the releases of "
     "foreign functions, and the terminate handler (STND.CXX.18, STND.CXX.19, STND.CXX.21, STND.CXX.23, "
     "STND.CXX.24, STND.CXX.32, and STND.CXX.33),",
     "It covers failures, including the option that assumes finite values, the failed release of an owned resource, "
     "and the terminate handler (STND.CXX.18, STND.CXX.19, STND.CXX.21, STND.CXX.23, STND.CXX.24, and "
     "STND.CXX.33),"),
    ("and the rules of each foreign interface (STND.CODE.22 to STND.CODE.26); the Notes give their C++ forms.",
     "the rules of each foreign interface (STND.CODE.22 to STND.CODE.26), and the rules that STND.CODE.27 to "
     "STND.CODE.35 state for every language; the Notes give their C++ forms."),
    ("STND.CXX.18 and STND.CXX.32 instantiate PRIME.4, and STND.CXX.3 instantiates GOV.48 and binds agents alone; "
     "these three are binding at every class.",
     "STND.CXX.18 instantiates PRIME.4, and STND.CXX.3 instantiates GOV.48 and binds agents alone; these two are "
     "binding at every class."),
    ("The Core Guidelines are the reference for all C++ work (STND.CXX.1). They have several hundred rules",
     "STND.CXX.1 leaves the guide to the repository configuration, which names the C++ Core Guidelines where it "
     "follows the custodian's direction. They have several hundred rules"),
    ("STND.BUILD.11 and STND.BUILD.12 are the general rules for the settings of each compilation and for the warnings "
     "that fail the checks of a change, of which STND.CXX.4 and STND.CXX.25 are the C++ forms, and they reach "
     "further, to the settings of each link step and to each tool of the toolchain.",
     "STND.BUILD.11 and STND.BUILD.12 are the general rules for the settings of each compilation and for the warnings "
     "that fail the checks of a change: STND.CXX.4 is the C++ form of the first, STND.CXX.25 names the warnings of "
     "each compiler at the recorded set on which the second fails a change, and the general rules reach further, to "
     "the settings of each link step and to each tool of the toolchain."),
    ("which is why STND.CXX.18 forbids such an option for a unit holding a required check of that kind.",
     "which is why STND.CXX.18 and STND.CODE.21 forbid such an option for a unit holding a required check of that "
     "kind."),
    ("names fixed by the notation of NUMER.4 (`Λ`, `β_eff`) are exempted in its configuration.",
     "names fixed by the notation of NUMER.4 (`Λ`, `β_eff`), which the third sentence of STND.CODE.28 lets keep "
     "their form, are exempted in its configuration."),
    ("A cast to `void` or an assignment to `std::ignore` discards the result, which STND.CODE.7 forbids for these "
     "failures and STND.CODE.12 governs for others.",
     "A cast to `void` or an assignment to `std::ignore` discards the result, which STND.CODE.7 forbids for these "
     "failures and STND.CODE.12 governs for others. STND.CODE.35 carries the declaration to each function of a C or "
     "vendor library whose status return reports such a failure, through the declaration of the library or through "
     "a function of the work that wraps it and carries the attribute."),
    ("STND.CXX.18 keeps the binding C++ form of STND.CODE.21 for a translation unit that holds a required check of a "
     "floating-point value, as ruled for C++.",
     "STND.CXX.18 states for a translation unit of C++ the rule that STND.CODE.21 binds in every language."),
    ("STND.CXX.32 is the counterpart of the second sentence of STND.RUST.13 for a panic, and is conditioned as that "
     "sentence is: where the work installs a terminate handler, the handler delivers the diagnosis of a listed "
     "condition that an exception carries to it.",
     "STND.CODE.33 reaches a terminate handler that the work installs: the handler delivers the diagnosis of a "
     "listed condition that an exception carries to it."),
    ("STND.CXX.6 and STND.CXX.7 instantiate DSGN.4, and STND.CXX.21 DSGN.5, which STND.CLASS.10 applies from CSQ2.",
     "STND.CXX.6 and STND.CXX.7 instantiate DSGN.4, which STND.CLASS.10 applies from CSQ2."),
    ("STND.CXX.18 and STND.CXX.32 bind at every class, CSQ4 included. STND.CXX.18 costs one choice of compiler "
     "option for a unit that holds a required check. STND.CXX.32 reaches only a terminate handler that the work "
     "installs and a listed condition that already ends the program there, and asks only for the actionable "
     "diagnosis that PRIME.4 names, at the cost of the wording of that handler; without it a handler of the work is "
     "able to end the program without a diagnosis. It asks for no work that PRIME.4 does not, so it raises no floor "
     "(GOV.11); no ruling of the custodian covers it, and the argument is the one that the ratification of "
     "2026-10-24 accepted for the second sentence of STND.RUST.13, which is conditioned in the same way.",
     "STND.CXX.18 binds at every class, CSQ4 included, and costs one choice of compiler option for a unit that holds "
     "a required check."),
]
CXX_READING = (
    "STND.CXX.32 is withdrawn, its outcome being STND.CODE.33 for every language, and the front matter lists it as "
    "withdrawn; STND.CXX.1 has the repository configuration name a published guide of C++ practice, at a recorded "
    "revision, in place of naming the C++ Core Guidelines, and is retitled Reference guide of C++ practice, and "
    "STND.CXX.25 checks the rules of that guide; STND.CXX.25 drops its second sentence, the failure of a change on "
    "each compiler warning, which STND.BUILD.12 holds; STND.CXX.21 drops its first sentence, the call of a foreign "
    "function through a declaration that diagnoses an ignored status, which STND.CODE.35 holds, instantiates "
    "DSGN.1 alone, and is retitled Reported release failures; STND.CXX.14 drops the names that the notation of "
    "NUMER.4 fixes from its exemption, which STND.CODE.28 holds; the Purpose and the Notes follow, and the class "
    "paragraph drops STND.CXX.32 and the onset of the first sentence of STND.CXX.21")
CXX_RATIONALE = (
    f"Minor amendment of STND.CXX, revision 1.4, ratified by the custodian on {F.DATE}: {CXX_READING}. The change is "
    "minor under STND.IDENT.3 because it removes one provision and three sentences and changes what a default "
    "names. The custodian ruled under D1 that one provision holds each outcome for every language and that named "
    "documents move from the provisions to the repository configuration, the Notes keeping the Core Guidelines as "
    "an example without a version. C++ code keeps each outcome: STND.CODE.33 asks of an installed terminate handler "
    "the diagnosis that STND.CXX.32 asked; STND.BUILD.12 fails a change on each warning of the recorded set; "
    "STND.CODE.35 has a C or vendor function that reports a listed failure called through a declaration that "
    "diagnoses an ignored result, its own or that of a wrapper of the work, where STND.CXX.21 asked a wrapper "
    "alone, a relaxation; STND.CODE.28 keeps the form of a name from notation. A project that follows the "
    "custodian's direction names the Core Guidelines in its configuration. STND.CXX.18 stays, since the Notes of "
    "STND.BUILD cite it; a later round withdraws it. The defaults raise no floor, and nothing binds that did not "
    "(GOV.11). Class onsets: STND.CXX.21 now rests on DSGN.1 alone and applies from CSQ3, its first sentence "
    "having moved with the onset of CSQ2 to STND.CODE.35. The withdrawn identifier is listed in the field withdrawn "
    "and is never given to another provision (STND.IDENT.14)."
    + tail(f"Ruling D1 of {F.RECORD}; register entry R6.2 (CL5, CL13, CL14, CL17, CL25) of {REG}; decisions 3, 7, "
           f"8, 9, 10, and 16 of {REC}."))


def apply_cxx(root: Path, at: str) -> None:
    root = Path(root)
    F.withdraw(root, "STND/CXX", "STND.CXX", [32])
    F.set_body(root, "STND/CXX/1.md", CXX1_BODY, title="Reference guide of C++ practice")
    edit(root, "STND/CXX/14.md", CXX14, instantiates=["INTPR.1"], refers_to=[])
    F.set_body(root, "STND/CXX/21.md", CXX21_BODY, title="Reported release failures", instantiates=["DSGN.1"],
               refers_to=["STND.CODE.14", "STND.CODE.12"])
    F.set_body(root, "STND/CXX/25.md", CXX25_BODY, refers_to=["STND.CXX.1", "STND.CXX.14"])
    F.check_fields(root, ["STND.CXX.1", "STND.CXX.14", "STND.CXX.21", "STND.CXX.25"])
    replace_text(root, "STND/CXX/_doc.md", CXX_DOC)
    row = f"| 1.4 | {F.DATE} | Minor amendment (GOV.41): {CXX_READING}. |"
    F.finish(root, "STND/CXX", "STND.CXX", "1.3", "1.4", row, CXX_RATIONALE, at)


# ---------------------------------------------------------------- STND.STDC 1.3

STDC29_BODY = (
    "Where the test of STND.STDC.28, or an error handler that ends the run, receives the failure of a call that "
    "STND.CODE.35 governs, the call SHOULD carry at its location the suppression of STND.CODE.4, with its reason "
    "naming that test or handler (REPRO.7).")
STDC38_BODY = (
    "The record of each verification that finds C code free of a kind of undefined behavior SHOULD state whether "
    "the documentation of each means that STND.CODE.34 has it name states that means as sound for that kind (VV.1, "
    "INTPR.10).")
STDC1 = [("| STND.CXX.25 | CSQ3 | Without the checks of the Core Guidelines and of the names of STND.CXX.14 |",
          "| STND.CXX.25 | CSQ3 | Without the checks of the rules of the guide of STND.CXX.1 and of the names of "
          "STND.CXX.14 |")]
STDC_DOC = [
    ("and the rules of each foreign interface (STND.CODE.22 to STND.CODE.26).",
     "the rules of each foreign interface (STND.CODE.22 to STND.CODE.26), and the rules that STND.CODE.21 and "
     "STND.CODE.27 to STND.CODE.35 state for every language."),
    ("the C reading of STND.CXX.25, which records a set of compiler warnings and fails a change on each;",
     "the C reading of STND.CXX.25, which records a set of compiler warnings, on each of which STND.BUILD.12 fails a "
     "change;"),
    ("(a2, N3220 7.2).", "(a2, 7.2)."),
    ("STND.CODE.21 recommends against it in every language, and STND.STDC.40 states for C, in the words of "
     "STND.CXX.18, the binding form that the table of STND.STDC.2 applied to C in revision 1.0; a later change of "
     "STND.CXX.18 does not change it.",
     "STND.CODE.21 forbids it in every language for code that holds a check that the floor requires, and "
     "STND.STDC.40 states the same for C, in the words of STND.CXX.18."),
    ("STND.CXX.1 names the Core Guidelines, which concern C++.",
     "STND.CXX.1 has the configuration name a guide of C++ practice, which concerns C++."),
    ("so STND.STDC.39 leaves the convention to the repository configuration, as STND.LEAN.27 does for Lean, keeps the "
     "names that the notation of NUMER.4 fixes, and adds no table;",
     "so STND.STDC.39 leaves the convention to the repository configuration and keeps the names that the notation of "
     "NUMER.4 fixes, the rule that STND.CODE.28 states for every language, and adds no table;"),
    ("In the working draft of the 2024 edition of C,", "In the working draft of C that the note read,"),
    ("(a1, WG14 N3220, 7.23.5.1, 7.23.5.2,", "(a1, 7.23.5.1, 7.23.5.2,"),
    ("A compiler or analyzer that knows the library functions meets STND.STDC.29 without a wrapper. STND.STDC.29 and "
     "the second sentence of STND.STDC.22 ask their diagnosis",
     "A compiler or analyzer that knows the library functions meets STND.CODE.35 without a wrapper. STND.CODE.35 and "
     "the second sentence of STND.STDC.22 ask their diagnosis"),
    ("STND.STDC.38 has the record say which a verification is, and for data races one record meets it and "
     "STND.CONC.27.",
     "The record of a verification is a record of a result under STND.CODE.34, which has a claim that rests on a "
     "verification name its means; STND.STDC.38 has the record say which a "
     "verification is, and for data races one record meets STND.STDC.38 and STND.CONC.27."),
    ("and the binding form stays for C by the ratification of 2026-10-24, while STND.CODE.21 is the default for "
     "every other language.",
     "and the ratification of 2026-10-24 kept the binding form for C, which STND.CODE.21 now states for every "
     "language."),
    ("STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, STND.CODE.16, and STND.CODE.18, carry the floor "
     "arguments",
     "STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.18, and STND.CODE.21, carry "
     "the floor arguments"),
    ("STND.STDC.7 rests on DSGN.4 and the first sentence of STND.STDC.29 on DSGN.5, and apply from CSQ2, as "
     "STND.CXX.6 and STND.CXX.21 do; the second sentence of STND.STDC.29 rests on REPRO.7 and STND.CODE.4 and "
     "applies from CSQ3.",
     "STND.STDC.7 rests on DSGN.4 and applies from CSQ2, as STND.CXX.6 does; STND.STDC.29 rests on REPRO.7 and "
     "STND.CODE.4 and applies from CSQ3."),
]
STDC_READING = (
    "STND.STDC.29 drops its first sentence, the call of a function of the C library or of another dependency "
    "through a declaration that diagnoses an ignored result, which STND.CODE.35 holds for every language, keeps the "
    "suppression at a call whose failure the test of STND.STDC.28 or an error handler that ends the run receives, "
    "and is retitled Suppressions where tests receive failures; STND.STDC.38 drops the statement of the means, "
    "which STND.CODE.34 states for every language, and keeps whether the documentation of each means states it as "
    "sound; the row of STND.CXX.25 in the table of STND.STDC.1 names the guide of STND.CXX.1 in place of the Core "
    "Guidelines; the Purpose and the Notes follow, the Notes cite the sources of the facts of C without the numbers "
    "of the drafts of the ISO C standard, which ruling D1 takes out of the Notes, and the class paragraph drops the "
    "onset of the first sentence of STND.STDC.29; References drop STND.LEAN")
STDC_RATIONALE = (
    f"Minor amendment of STND.STDC, revision 1.3, ratified by the custodian on {F.DATE}: {STDC_READING}. The change "
    "is minor under STND.IDENT.3 because it removes the parts of two defaults whose outcomes STND.CODE now holds. "
    "The custodian ruled under D1 that one provision holds each outcome for every language. C code keeps each "
    "outcome: STND.CODE.35 asks the declaration of STND.STDC.29 in the same words, and STND.CODE.34 asks, as a "
    "default from CSQ2 as STND.STDC.38 did, the statement of the means of a claim that C code is free of a kind of "
    "undefined behavior; the Notes read the record of a verification as a record of a result under STND.CODE.34, "
    "so that the record that STND.STDC.38 reached stays reached. STND.STDC.39 and STND.STDC.40 stay, since the Notes of STND.SV and "
    "STND.BUILD cite them; a later round withdraws them. Class onsets: STND.STDC.29 now applies from CSQ3, its "
    "first sentence having moved with the onset of CSQ2 to STND.CODE.35; STND.STDC.38 stays at CSQ2."
    + tail(f"Ruling D1 of {F.RECORD}; register entries R6.2 (CL3, CL10, CL13, CL14, CL17) and R7.1 of {REG}; decisions 1, 7, 8, 9, 10, "
           f"15, and 16 of {REC}."))


def apply_stdc(root: Path, at: str) -> None:
    root = Path(root)
    F.set_body(root, "STND/STDC/29.md", STDC29_BODY, title="Suppressions where tests receive failures",
               instantiates=["REPRO.7"], refers_to=["STND.STDC.28", "STND.CODE.35", "STND.CODE.4"])
    F.set_body(root, "STND/STDC/38.md", STDC38_BODY, refers_to=["STND.CODE.34"])
    edit(root, "STND/STDC/1.md", STDC1,
         refers_to=["STND.CXX.1", "STND.CXX.4", "STND.CXX.7", "STND.CXX.9", "STND.CXX.12", "STND.CXX.14",
                    "STND.CXX.15", "STND.CXX.23", "STND.CXX.24", "STND.CXX.25", "STND.CXX.26", "STND.CXX.27"])
    F.check_fields(root, ["STND.STDC.1", "STND.STDC.29", "STND.STDC.38"])
    replace_text(root, "STND/STDC/_doc.md", STDC_DOC)
    row = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {STDC_READING}. |"
    F.finish(root, "STND/STDC", "STND.STDC", "1.2", "1.3", row, STDC_RATIONALE, at)


# ---------------------------------------------------------------- STND.JL 1.4

JL6 = [("(INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its "
        "symbol, as STND.DOCS.12 permits (INTPR.4). A method",
        "(INTPR.1). A method")]
JL15_BODY = (
    "Under STND.CODE.14, where the visible degradation of a condition that PRIME.4 lists is a record that a logging "
    "macro writes, the level of that record SHALL be `Warn` or `Error` (PRIME.4).")
JL31 = [(" Each floating-point value that such an example shows SHOULD be rounded by the example to the digits that "
         "its stated tolerance admits, or matched by a filter of the doctest that admits that tolerance (INTPR.3, "
         "VV.8).", "")]
JL_DOC = [
    ("arithmetic state and comparisons (STND.JL.19, STND.JL.20, and STND.JL.21); random numbers (STND.JL.22 to "
     "STND.JL.26);",
     "arithmetic state (STND.JL.19 and STND.JL.20); random numbers (STND.JL.22 and STND.JL.25);"),
    ("STND.JL.13 gives STND.CODE.6, STND.JL.15 gives STND.CODE.14, and STND.JL.14 and STND.JL.15 give STND.CODE.7, "
     "their forms in Julia's constructs; STND.JL.16 and STND.JL.21 apply STND.CODE.12 and STND.CODE.10 to Julia's "
     "exceptions and tolerances.",
     "STND.JL.13 gives STND.CODE.6, and STND.JL.14 STND.CODE.7, their forms in Julia's constructs, and STND.JL.15 "
     "adds to STND.CODE.14 the levels at which a logged degradation is visible; STND.JL.16 applies STND.CODE.12 to "
     "Julia's exceptions; STND.CODE.29 to STND.CODE.31 hold for Julia the generators, the hash values, and the "
     "tolerances of comparisons."),
    ("keeps its symbol (STND.JL.6, STND.DOCS.12).", "keeps its symbol (STND.CODE.28, STND.DOCS.12)."),
    ("without exporting it, from Julia 1.11 (a2, S14);", "without exporting it, from a recent release of Julia (a2, "
     "S14);"),
    ("STND.JL.15 lists the responses of PRIME.4 once, in the Julia form of STND.CODE.14, and STND.JL.14 refers to it.",
     "STND.CODE.14 lists the responses of PRIME.4 once, and STND.JL.14 refers to it."),
    ("a program that installs another logger decides what it shows.",
     "a program that installs another logger decides what it shows, which is why a record that library code writes "
     "is never the only visible degradation under STND.CODE.14, as the custodian ruled on 2026-10-28 for every "
     "language, and the levels of STND.JL.15 decide for the records of other code."),
    ("A returned convergence flag, the form that solver packages use, meets STND.JL.15,",
     "A returned convergence flag, the form that solver packages use, meets STND.CODE.14,"),
    ("STND.JL.21 asks that the Julia comparison state them where the code makes it.",
     "STND.CODE.31 asks that the comparison state them where the code makes it."),
    ("so the parts of parallel work take their streams from a facility of STND.VVUQ.62 (STND.JL.24). STND.JL.24 is "
     "the Julia form of STND.CONC.23, which keys each stream of a computation divided among concurrent tasks to a "
     "part defined independently of the number of tasks and of the task that computes it; STND.JL.24 reaches each "
     "division of work into parts, parts run as separate runs included, which STND.CONC.23 does not reach.",
     "so the parts of parallel work take their streams from a facility of STND.VVUQ.62 (STND.CODE.29). STND.CODE.29 "
     "states the rule of STND.CONC.23, which keys each stream of a computation divided among concurrent tasks to a "
     "part defined independently of the number of tasks and of the task that computes it, for each division of "
     "work into parts, parts run as separate runs included, which STND.CONC.23 does not reach."),
    ("draws one from the operating system's entropy and records it (STND.JL.23);",
     "draws one from the operating system's entropy and records it (STND.CODE.29);"),
    ("changes the iteration order of `Dict` and `Set` (STND.JL.26);",
     "changes the iteration order of `Dict` and `Set` (STND.CODE.30);"),
    ("or matched through a filter that drops the digits beyond the stated tolerance (STND.JL.31).",
     "or matched through a filter that drops the digits beyond the stated tolerance, the Julia forms of the "
     "comparison within a stated tolerance of STND.DOCS.13."),
    ("STND.JL.13, STND.JL.18, STND.JL.20, STND.JL.21, STND.JL.22, and STND.JL.27,",
     "STND.JL.13, STND.JL.18, STND.JL.20, STND.JL.22, STND.JL.27, and STND.CODE.31,"),
    ("each other exception so caught is answered as STND.JL.15, the Julia form of STND.CODE.14, gives.",
     "each other exception so caught is answered as STND.CODE.14 gives, at the levels of STND.JL.15."),
    ("STND.CONC.3, STND.CONC.16, and STND.CONC.23 apply from CSQ3, as STND.JL.27 and STND.JL.24 do,",
     "STND.CONC.3 and STND.CONC.16 apply from CSQ3, as STND.JL.27 does,"),
]
JL_READING = (
    "STND.JL.21, STND.JL.23, STND.JL.24, and STND.JL.26 are withdrawn, their outcomes being STND.CODE.31, "
    "STND.CODE.29, and STND.CODE.30 for every language, and the front matter lists them as withdrawn; STND.JL.15 "
    "keeps only the levels `Warn` and `Error` of a degradation that a logging macro records, the responses being "
    "STND.CODE.14, which no longer counts a record of library code as the only visible degradation, and is "
    "retitled Logged degradations at shown levels; STND.JL.14 cites STND.CODE.14 in place of STND.JL.15; "
    "STND.JL.6 drops the names that the notation of NUMER.4 fixes, which STND.CODE.28 holds; STND.JL.31 drops its "
    "second sentence, the comparison of a shown value within its tolerance, which STND.DOCS.13 holds; the Purpose "
    "and the Notes follow, the Notes name a release of Julia without its number, and the class paragraph drops "
    "STND.JL.24")
JL_RATIONALE = (
    f"Minor amendment of STND.JL, revision 1.4, ratified by the custodian on {F.DATE}: {JL_READING}. The change is "
    "minor under STND.IDENT.3 because it removes four provisions and parts of four others. The custodian ruled "
    "under D1 that one provision holds each outcome for every language, that STND.CODE.14 carries the forms of each "
    "language, and that a library log record is never the only visible sign of a degraded result; the last "
    "replaces, for library code, the reading of 2026-10-23 that a record at `Warn` counts, which STND.JL.15 keeps "
    "for other code. That is a tightening of a binding provision that asks no response beyond PRIME.4 (the floor "
    "argument in the Notes of STND.CODE), so no floor is raised (GOV.11). Julia code keeps each other outcome in "
    "the same words in STND.CODE.29 to STND.CODE.31, and STND.DOCS.13 already compares a shown value within its "
    "stated tolerance. Class onsets: the provisions of STND.CODE apply from CSQ3, as the withdrawn ones did. The "
    "withdrawn identifiers are listed in the field withdrawn and are never given to another provision "
    "(STND.IDENT.14)."
    + tail(f"Ruling D1 of {F.RECORD}; register entries R6.2 (CL4, CL5, CL6, CL18, CL23) and R7.1 of {REG}; "
           f"decisions 2, 3, 4, 5, 7, and 15 of {REC}."))


def apply_jl(root: Path, at: str) -> None:
    root = Path(root)
    edit(root, "STND/JL/14.md", [("as STND.JL.15 requires", "as STND.CODE.14 requires")], refers_to=["STND.CODE.14"])
    F.withdraw(root, "STND/JL", "STND.JL", [21, 23, 24, 26])
    edit(root, "STND/JL/6.md", JL6, instantiates=["INTPR.1"], refers_to=[])
    F.set_body(root, "STND/JL/15.md", JL15_BODY, title="Logged degradations at shown levels",
               refers_to=["STND.CODE.14"])
    replace_text(root, "STND/JL/31.md", JL31)
    F.check_fields(root, ["STND.JL.6", "STND.JL.31"])
    F.check_fields(root, ["STND.JL.14", "STND.JL.15"], binding=True)
    replace_text(root, "STND/JL/_doc.md", JL_DOC)
    row = f"| 1.4 | {F.DATE} | Minor amendment (GOV.41): {JL_READING}. |"
    F.finish(root, "STND/JL", "STND.JL", "1.3", "1.4", row, JL_RATIONALE, at)


# ---------------------------------------------------------------- STND.PY 1.3

PY1_BODY = ("Python source SHOULD follow the conventions of the style guide, with each choice that the style guide "
            "leaves to a project settled once in the repository configuration (INTPR.1).")
PY2_BODY = (
    "The static checks that the repository configuration names for Python under STND.CODE.4 SHOULD include a linter "
    "that checks the conventions of the style guide that the layout tool of STND.CODE.5 leaves open, the structure "
    "of each docstring against the docstring format, and the agreement of the parameters and return values that "
    "each docstring documents with its function (INTPR.1, INTPR.3, DSGN.3).")
PY10 = [("SHOULD carry a docstring in the format of the numpydoc standard, with its sections in the order that the "
         "standard gives,",
         "SHOULD carry a docstring in the docstring format, with its sections in the order that the format gives,")]
PY11_BODY = (
    "Each entry of a docstring that documents a parameter or an attribute SHOULD describe its item without "
    "restating the type that the annotation of the item gives (INTPR.3). Where the docstring format has a position "
    "for the type of a returned or yielded value, each entry that documents such a value SHOULD give there the type "
    "that the return annotation states for that value (INTPR.3).")
PY12 = [(" Each floating-point value that such an example shows SHOULD be rounded by the example to the digits that "
         "its stated tolerance admits, or compared by the test runner to the precision that it shows (INTPR.3, "
         "VV.8).", "")]
PY22_BODY = (
    "Under STND.CODE.14, where the visible degradation of a condition that PRIME.4 lists is a warning, its category "
    "SHALL be one that the default warnings filters show (PRIME.4).")
PY_TERMS = [
    ("| Style PEPs | PEP 8, Style Guide for Python Code, and PEP 257, Docstring Conventions, in the revisions current "
     "at the change. |\n",
     "| Style guide | The published guide of the conventions of Python source that the repository configuration "
     "names. |\n"),
    ("| Numpydoc standard | The docstring format that the format guide of the numpydoc project defines, with its "
     "sections and their order. |\n",
     "| Docstring format | The published format of docstrings, with its sections and their order, that the "
     "repository configuration names. |\n"),
]
PY_DOC = PY_TERMS + [
    ("They cover style from the Python Enhancement Proposals, enforced by tools at each change (STND.PY.1 and "
     "STND.PY.2);",
     "They cover style from the style guide that the repository configuration names, enforced by tools at each "
     "change (STND.PY.1 and STND.PY.2);"),
    ("docstrings in the numpydoc format, with the examples of the documentation run as doctests",
     "docstrings in the docstring format that the repository configuration names, with the examples of the "
     "documentation run as doctests"),
    ("random number generators and values that vary between runs (STND.PY.15 to STND.PY.19); comparisons within a "
     "tolerance (STND.PY.20); reporting from library code, and the hooks that report an exception that no handler "
     "catches (STND.PY.21, STND.PY.22, and STND.PY.32);",
     "random number generators and stable streams (STND.PY.15 and STND.PY.18); reporting from library code "
     "(STND.PY.21 and STND.PY.22);"),
    ("STND.PY.22, STND.PY.25, STND.PY.27, STND.PY.30, and STND.PY.32 instantiate PRIME.4,",
     "STND.PY.22, STND.PY.25, STND.PY.27, and STND.PY.30 instantiate PRIME.4,"),
    ("These six are binding and apply at every class. STND.PY.22 states the one set of responses to a condition that "
     "PRIME.4 lists, in the Python form of STND.CODE.14, and the other provisions refer to it.",
     "These five are binding and apply at every class. STND.CODE.14 states the one set of responses to a condition "
     "that PRIME.4 lists, and the other provisions refer to it; STND.PY.22 adds the categories of warnings that "
     "count as visible."),
    ("Style. PEP 8 and PEP 257 are active,",
     "Style. The style guide and the docstring format are documents that the repository configuration names "
     "(STND.PY.1, STND.PY.10), and the custodian's directions name the style PEPs, PEP 8 and PEP 257, and the "
     "numpydoc format. PEP 8 and PEP 257 are active,"),
    ("agreement of the documented exceptions is left to review.",
     "agreement of the documented exceptions is left to review. STND.CODE.32 has the static checks decide each "
     "provision of this standard that a static check among the means of the work is able to decide."),
    ("keeps its case (STND.PY.1, STND.DOCS.12).", "keeps its case (STND.CODE.28, STND.DOCS.12)."),
    ("The numpydoc standard fixes the sections and their order,",
     "The numpydoc format, where the repository configuration names it, fixes the sections and their order,"),
    ("because the numpydoc standard requires one there", "because the numpydoc format requires one there"),
    ("or the result of a comparison that states its tolerances (STND.PY.12).",
     "or the result of a comparison that states its tolerances, the forms in Python of the comparison within a "
     "stated tolerance of STND.DOCS.13."),
    ("this standard keeps that conversion at the entry point (STND.PY.16),",
     "STND.CODE.29 keeps that conversion at the entry point,"),
    ("(STND.PY.17, STND.VVUQ.62);", "(STND.CODE.29, STND.VVUQ.62);"),
    ("STND.PY.17 states for the work in Python the rule of STND.CONC.23, which keys each stream of a computation "
     "divided among concurrent tasks to a part defined independently of the number of tasks and of the task that "
     "computes it. STND.PY.17 reaches further: it governs each division of work into parts, parts run as separate "
     "runs included, which STND.CONC.23 does not reach; both apply from CSQ3.",
     "STND.CODE.29 states the rule of STND.CONC.23, which keys each stream of a computation divided among concurrent "
     "tasks to a part defined independently of the number of tasks and of the task that computes it, for each "
     "division of work into parts, parts run as separate runs included, which STND.CONC.23 does not reach; both "
     "apply from CSQ3."),
    ("the iteration order of a set of strings (STND.PY.19).", "the iteration order of a set of strings (STND.CODE.30)."),
    ("STND.PY.20 asks that the Python comparison state those parameters where the code makes it,",
     "STND.CODE.31 asks that the comparison state those parameters where the code makes it,"),
    ("STND.PY.22 therefore gives the responses to a condition that PRIME.4 lists, of which a record from library "
     "code is no part;",
     "STND.CODE.14 therefore keeps a record from library code from being the only visible degradation;"),
    ("ResourceWarning among them, is silent and does not count.",
     "ResourceWarning among them, is silent and does not count (STND.PY.22)."),
    ("STND.PY.32 is the Python counterpart of the second sentence of STND.RUST.13: it asks a hook",
     "STND.CODE.33 asks a hook"),
    ("and Python has no way to handle it is such a hook (a2, S1).",
     "and Python has no way to handle it is such a hook, run for a failure that the runtime is unable to propagate "
     "(a2, S1)."),
    ("STND.PY.22 is the Python form of STND.CODE.14, which admits the pass", "STND.CODE.14 admits the pass"),
    ("a response that STND.PY.22 admits,", "a response that STND.CODE.14 admits,"),
    ("responds as STND.PY.22 gives (STND.PY.30);", "responds as STND.CODE.14 gives (STND.PY.30);"),
    ("is answered as STND.PY.22, the Python form of STND.CODE.14, gives.", "is answered as STND.CODE.14 gives."),
    ("STND.PY.22 asks for the responses that PRIME.4 already requires, and STND.PY.25, STND.PY.27, and STND.PY.30 ask "
     "only for a response that STND.PY.22 gives,",
     "STND.PY.22 keeps a warning that the default filters hide from counting as a visible degradation, and "
     "STND.PY.25, STND.PY.27, and STND.PY.30 ask only for a response that STND.CODE.14 gives,"),
]
PY_FLOOR_HOOK = (
    " STND.PY.32 reaches only a listed condition whose exception no handler caught, which ends a thread or the "
    "program or is dropped, and asks only for the actionable diagnosis that PRIME.4 names, at the cost of the "
    "wording of a hook that the work installs. A replaced hook that drops a listed condition without a diagnosis "
    "lets the program end or continue past the error in silence, which the last sentence of PRIME.4 forbids; the "
    "default hooks print the exception, so the provision binds only where the work replaces one. It asks for no "
    "work that PRIME.4 does not, so it raises no floor (GOV.11); no ruling of the custodian covers it, and the "
    "argument is the one that the ratification of 2026-10-24 accepted for the second sentence of STND.RUST.13. It "
    "binds at every class, CSQ4 included.")
PY_READING = (
    "STND.PY.16, STND.PY.17, STND.PY.19, STND.PY.20, and STND.PY.32 are withdrawn, their outcomes being "
    "STND.CODE.29, STND.CODE.30, STND.CODE.31, and STND.CODE.33 for every language, and the front matter lists them "
    "as withdrawn; STND.PY.22 keeps only the categories of warnings that the default filters show, the responses "
    "and the record of library code being STND.CODE.14, and is retitled Warnings of shown categories; STND.PY.27 "
    "and STND.PY.30 cite STND.CODE.14 in place of STND.PY.22; Terms define Style guide and Docstring format as the "
    "documents that the repository configuration names, in place of Style PEPs and Numpydoc standard, and "
    "STND.PY.1, STND.PY.2, STND.PY.10, and STND.PY.11 use them, STND.PY.1 being retitled Configured style guide as "
    "baseline and STND.PY.10 Docstrings in the configured format; STND.PY.1 drops the names that the notation of "
    "NUMER.4 fixes, which STND.CODE.28 holds; STND.PY.2 drops its second sentence, which STND.CODE.32 holds; "
    "STND.PY.12 drops its second sentence, which STND.DOCS.13 holds; the Purpose and the Notes follow")
PY_RATIONALE = (
    f"Minor amendment of STND.PY, revision 1.3, ratified by the custodian on {F.DATE}: {PY_READING}. The change is "
    "minor under STND.IDENT.3 because it removes five provisions and parts of five others and alters two defined "
    "meanings. The custodian ruled under D1 that one provision holds each outcome for every language, that "
    "STND.CODE.14 carries the forms of each language, and that named documents move from the provisions to the "
    "repository configuration; the Notes keep the style PEPs and the numpydoc format, which the custodian's "
    "directions of 2026-10-22 name, as examples without a version, and a project that follows those directions "
    "names them in its configuration. Python code keeps each outcome in the same words in STND.CODE.14 and "
    "STND.CODE.29 to STND.CODE.33, and STND.DOCS.13 already compares a shown value within its tolerance; STND.PY.11 "
    "asks the type of a returned value where the format has a position for it, which the numpydoc format has. "
    "STND.PY.22, STND.PY.25, STND.PY.27, and STND.PY.30 stay binding, and nothing binds that did not, so no floor "
    "is raised (GOV.11). Class onsets: unchanged. STND.PY.14 stays, since the Notes of STND.BUILD cite it. The "
    "withdrawn identifiers are listed in the field withdrawn and are never given to another provision "
    "(STND.IDENT.14)."
    + tail(f"Ruling D1 of {F.RECORD}; register entry R6.2 (CL4, CL5, CL6, CL14, CL18, CL23, CL25) of {REG}; "
           f"decisions 2 to 5, 7, 10, and 16 of {REC}."))


def apply_py(root: Path, at: str) -> None:
    root = Path(root)
    for n in (27, 30):
        edit(root, f"STND/PY/{n}.md", [("as STND.PY.22 requires", "as STND.CODE.14 requires")],
             refers_to=["STND.CODE.14"])
    F.withdraw(root, "STND/PY", "STND.PY", [16, 17, 19, 20, 32])
    F.set_body(root, "STND/PY/1.md", PY1_BODY, title="Configured style guide as baseline", instantiates=["INTPR.1"],
               refers_to=[])
    F.set_body(root, "STND/PY/2.md", PY2_BODY)
    edit(root, "STND/PY/10.md", PY10, title="Docstrings in the configured format")
    F.set_body(root, "STND/PY/11.md", PY11_BODY)
    replace_text(root, "STND/PY/12.md", PY12)
    F.set_body(root, "STND/PY/22.md", PY22_BODY, title="Warnings of shown categories", refers_to=["STND.CODE.14"])
    F.check_fields(root, ["STND.PY.1", "STND.PY.2", "STND.PY.10", "STND.PY.11", "STND.PY.12"])
    F.check_fields(root, ["STND.PY.22", "STND.PY.27", "STND.PY.30"], binding=True)
    replace_text(root, "STND/PY/_doc.md", PY_DOC + [(PY_FLOOR_HOOK, "")])
    row = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {PY_READING}. |"
    F.finish(root, "STND/PY", "STND.PY", "1.2", "1.3", row, PY_RATIONALE, at)


# ---------------------------------------------------------------- STND.RUST 1.3

RUST34_BODY = ("Each claim that STND.CODE.34 governs and that concerns Rust code of the work SHALL meet "
               "STND.CODE.34 (PRIME.2).")
RUST31 = [(" Those static checks SHOULD also decide each provision of this standard whose compliance a static check "
           "of Rust source is able to decide (DSGN.3).", "")]
RUST_DOC = [
    ("failures and their reporting (STND.RUST.13 and STND.RUST.15 to STND.RUST.17);",
     "failures (STND.RUST.15, STND.RUST.16, and STND.RUST.17);"),
    ("build scripts of dependencies, crate features, and builds from the revisions that a lock file records "
     "(STND.RUST.28, STND.RUST.29, and STND.RUST.30); the checks of Rust code, unsafe code among it, with the claims "
     "that rest on them (STND.RUST.31 to STND.RUST.34); and the conventions of names (STND.RUST.35).",
     "build scripts of dependencies and crate features (STND.RUST.28 and STND.RUST.29); and the checks of Rust "
     "code, unsafe code among it, with the claims that rest on them (STND.RUST.31 to STND.RUST.34)."),
    ("STND.RUST.13 and STND.RUST.15 instantiate PRIME.4, STND.RUST.34 instantiates PRIME.2, and STND.RUST.6 "
     "instantiates GOV.48 and binds agents alone; these four are binding at every class.",
     "STND.RUST.15 instantiates PRIME.4, STND.RUST.34 instantiates PRIME.2, and STND.RUST.6 instantiates GOV.48 and "
     "binds agents alone; these three are binding at every class."),
    ("in STND.CODE (STND.CODE.14 to STND.CODE.21);", "in STND.CODE (STND.CODE.14 to STND.CODE.35);"),
    ("hence the dependencies in STND.RUST.34.", "hence the dependencies in STND.CODE.34."),
    ("STND.RUST.13 lists the responses that PRIME.4 admits in Rust, and the other provisions refer to it; its first "
     "sentence is the Rust form of STND.CODE.14, whose pass of the condition to the caller in its result, in an "
     "argument that the caller passes to receive it, or by a mechanism of the language that propagates it takes in "
     "Rust the returned condition and the panic, and its second and third add what Rust needs.",
     "STND.CODE.14 lists the responses that PRIME.4 admits, and the other provisions refer to it; its pass of the "
     "condition to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism "
     "of the language that propagates it takes in Rust the returned condition and the panic."),
    ("The second sentence of STND.RUST.13 keeps a replaced hook from removing", "STND.CODE.33 keeps a replaced hook "
     "from removing"),
    ("The third sentence follows STND.PY.22: a record written through a logging interface reaches no person unless "
     "the program installs something that shows it; STND.JL.15 instead admits a record at the levels that the "
     "default logger of Julia shows. The three sentences of STND.RUST.13 together define what counts as a response, "
     "as those of STND.PY.22 do.",
     "A record written through a logging interface reaches no person unless the program installs something that "
     "shows it, so a record that library code writes is never the only visible degradation (STND.CODE.14)."),
    ("is answered as STND.RUST.13, the Rust form of STND.CODE.14, gives.", "is answered as STND.CODE.14 gives."),
    ("STND.RUST.30 has each build of the checks and of each release use the revisions of a committed lock file,",
     "STND.DEPS.13 has each build of the checks and of each release use the revisions of a committed lock file,"),
    ("and the warnings of the compiler fail the checks under STND.BUILD.12.",
     "and the warnings of the compiler fail the checks under STND.BUILD.12; STND.CODE.32 has those checks decide "
     "each provision of this standard that a static check among the means of the work is able to decide."),
    ("STND.RUST.34 reaches the claims in a report, in the record of a result or of a release, and in a review;",
     "STND.CODE.34, which STND.RUST.34 binds for Rust code, reaches the claims in a report, in the record of a "
     "result or of a release, and in a review, a claim that a module is a sound module among them;"),
    ("STND.RUST.35 leaves the convention to the repository configuration, as STND.STDC.39 and STND.LEAN.27 do.",
     "STND.CODE.28 leaves the convention of Rust source to the repository configuration, since this standard gives "
     "none."),
    ("STND.RUST.35 keeps the names that the notation of NUMER.4 fixes, as STND.DOCS.12 permits, a lint that reports "
     "such a name being suppressed at its location with its reason under STND.CODE.4, and adds no table.",
     "STND.CODE.28 keeps the names that the notation of NUMER.4 fixes, a lint that reports such a name being "
     "suppressed at its location with its reason under STND.CODE.4, and this standard adds no table."),
    ("STND.RUST.27, STND.RUST.28, STND.RUST.30, STND.RUST.35, and the first sentence of STND.RUST.5",
     "STND.RUST.27, STND.RUST.28, and the first sentence of STND.RUST.5"),
    (" STND.RUST.13 holds three modals on the responses to one failure and applies as one; it is binding, so no "
     "decision replaces it, and a project instrument only tightens it (GOV.19).", ""),
    ("STND.RUST.13 asks for the responses that PRIME.4 already requires: its second sentence reaches only a panic "
     "that answers a listed condition and that no other response answers, and asks only for the actionable "
     "diagnosis that PRIME.4 names; its third keeps a record that no person sees from counting as visible, as "
     "STND.PY.22 does. ", ""),
    ("STND.RUST.34 asks of a claim of soundness in a report, a record, or a review that it state the means that "
     "checked it and not extend beyond what they covered;",
     "STND.RUST.34 binds for Rust code the claims of STND.CODE.34, that each state the means that checked it and "
     "not extend beyond what they covered;"),
]
RUST_READING = (
    "STND.RUST.13, STND.RUST.30, and STND.RUST.35 are withdrawn, their outcomes being STND.CODE.14, STND.CODE.33, "
    "STND.DEPS.13, and STND.CODE.28 for every language, and the front matter lists them as withdrawn; STND.RUST.34 "
    "keeps the claims of soundness binding for Rust by binding STND.CODE.34, which states them for every language "
    "as a default; STND.RUST.11 cites STND.CODE.14 in place of STND.RUST.13; STND.RUST.31 drops its second "
    "sentence, which STND.CODE.32 holds; the Purpose, the Notes on failures, packages, checking, names, and the "
    "floor, and the class paragraph drop the withdrawn provisions and cite those that hold their outcomes; "
    "References drop STND.LEAN and STND.STDC")
RUST_RATIONALE = (
    f"Minor amendment of STND.RUST, revision 1.3, ratified by the custodian on {F.DATE}: {RUST_READING}. The change "
    "is minor under STND.IDENT.3 because it removes three provisions and one sentence and rewords one binding provision. The custodian ruled under D1 "
    "that one provision holds each outcome for every language and that STND.CODE.14 carries the forms of each "
    "language. Rust code keeps each outcome: the panic and the returned condition are forms of STND.CODE.14, its "
    "second sentence keeps a record of library code from being the only visible degradation, STND.CODE.33 asks of "
    "a replaced panic hook or a defined panic handler the diagnosis that the second sentence of STND.RUST.13 asked, "
    "STND.RUST.34 binds for Rust code STND.CODE.34, which states the claims that STND.RUST.34 stated in the same "
    "words, soundness being the claim that no use of an interface is able to cause undefined behavior, so the claims "
    "bind in Rust as before, at the cost of one sentence for each claim (PRIME.2), STND.DEPS.13 has builds use the locked revisions, and "
    "STND.CODE.28 holds the rule of names. STND.CODE.32 has the static checks decide each provision that a static "
    "check among the means of the work is able to decide, where the withdrawn sentence named each that a static "
    "check of Rust source is able to decide, a narrowing of a default. STND.RUST.6, STND.RUST.15, and STND.RUST.34 stay binding, "
    "and nothing binds that did not, so no floor is raised (GOV.11). Class onsets: unchanged. The withdrawn "
    "identifiers are listed in the field withdrawn and are never given to another provision (STND.IDENT.14)."
    + tail(f"Ruling D1 of {F.RECORD}; register entry R6.2 (CL4, CL5, CL8, CL10, CL18, CL23, CL25) of {REG}; "
           f"decisions 2 to 9 of {REC}."))


def apply_rust(root: Path, at: str) -> None:
    root = Path(root)
    edit(root, "STND/RUST/11.md", [("by a response of STND.RUST.13 other than a panic",
                                    "by a response of STND.CODE.14 other than a panic")],
         refers_to=["STND.CODE.14", "STND.CODE.12"])
    F.withdraw(root, "STND/RUST", "STND.RUST", [13, 30, 35])
    F.set_body(root, "STND/RUST/34.md", RUST34_BODY, refers_to=["STND.CODE.34"])
    replace_text(root, "STND/RUST/31.md", RUST31)
    F.check_fields(root, ["STND.RUST.11", "STND.RUST.31"])
    F.check_fields(root, ["STND.RUST.34"], binding=True)
    replace_text(root, "STND/RUST/_doc.md", RUST_DOC)
    row = f"| 1.3 | {F.DATE} | Minor amendment (GOV.41): {RUST_READING}. |"
    F.finish(root, "STND/RUST", "STND.RUST", "1.2", "1.3", row, RUST_RATIONALE, at)
