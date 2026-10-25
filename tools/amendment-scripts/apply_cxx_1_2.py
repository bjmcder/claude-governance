"""Rehearsable minor amendment: STND.CXX 1.2, withdrawing or narrowing the shared rules that STND.CODE 1.2 now holds for every
language, citing them, and adding the C++ counterpart of the second sentence of STND.RUST.13 (one transaction).

Withdrawn: STND.CXX.16, .17, .28, .29, .30, and .31, whose outcomes are STND.CODE.14, .15, and .17 to .20.
STND.CXX.18 keeps its second sentence, the binding C++ form of STND.CODE.21; its first is STND.CODE.16. New:
STND.CXX.32. It applies after STND.CODE 1.2, which it cites, and after STND.STDC 1.1, which no longer refers to
the withdrawn provisions: apply_close_p1.py runs it third. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse <corpus holding STND.CODE 1.2 and STND.STDC 1.1> \
        ../tools/amendment-scripts/apply_cxx_1_2.py
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:10:00+00:00"

WITHDRAWN = [16, 17, 28, 29, 30, 31]
# STND.CXX.18 stays, holding only the binding C++ form of STND.CODE.21; its first sentence moves to STND.CODE.16.
MOVED_TO = {16: 14, 17: 15, 28: 17, 29: 18, 30: 19, 31: 20}


def swap_paragraphs(root: Path, rel: str, swaps: list[tuple[str, str, str]]) -> None:
    """Replace whole paragraphs, each found by its opening words and checked by the digest of its text.

    Each swap is (opening words, sha256 of the old paragraph, new paragraph or "" to remove it); a paragraph that
    is missing, not unique, or not the text the digest names is refused with ValueError, and nothing is written.
    """
    path = root / rel
    paras = path.read_text(encoding="utf-8").split("\n\n")
    for start, digest, new in swaps:
        hits = [i for i, p in enumerate(paras) if p.startswith(start)]
        if len(hits) != 1:
            raise ValueError(f"{rel}: {start[:60]!r} opens {len(hits)} paragraphs, not one")
        if hashlib.sha256(paras[hits[0]].encode("utf-8")).hexdigest() != digest:
            raise ValueError(f"{rel}: the paragraph {start[:60]!r} is not the text this amendment was written for")
        paras[hits[0]] = new
    path.write_text("\n\n".join(p for p in paras if p), encoding="utf-8")


# ------------------------------------------------------------------ provisions

NEW32 = P(32, "Diagnoses from terminate handlers", "Failures", """
Where the work installs a terminate handler, that handler SHALL deliver to the operator, or to the record of the run, a diagnosis of each condition that PRIME.4 lists and that a C++ exception carries to it (PRIME.4, STND.CODE.14).
""", ["PRIME.4"], refs=["STND.CODE.14"], mode="binding")

CXX18 = [
    ('refers_to: ["STND.CODE.6"]', 'refers_to: ["STND.CODE.6", "STND.CODE.21"]'),
    ("Where CPS.5 or CPS.9 applies to the work, each check that it requires SHALL run, with its response, in every "
     "build of the work, as STND.CODE.6 requires of a check of untrusted input (PRIME.4, DSGN.2). A translation unit",
     "A translation unit"),
    ("lets the compiler assume that floating-point values are finite (PRIME.4).",
     "lets the compiler assume that floating-point values are finite (PRIME.4, DSGN.2, STND.CODE.21)."),
]

CXX2 = [
    ('refers_to: ["STND.CXX.30", "STND.DEPS.4"]', 'refers_to: ["STND.CODE.19", "STND.DEPS.4"]'),
    ("Other than for an edition that STND.CXX.30, a hardware contract,",
     "Other than for an edition that STND.CODE.19, a hardware contract,"),
    ("toolchain matrix states support for a feature of a later edition, a unit MAY be compiled",
     "toolchain matrix states support for a feature of a later edition, a unit other than one of high-assurance code "
     "that STND.CODE.19 governs MAY be compiled"),
]
CXX8 = [
    ('refers_to: ["STND.CXX.28", "REPRO.3"]', 'refers_to: ["STND.CODE.17", "REPRO.3"]'),
    ("the rule of the high-assurance coding standard of STND.CXX.28,",
     "the rule of the high-assurance coding standard of STND.CODE.17,"),
]
CXX21 = [
    ('refers_to: ["PRIME.4", "STND.CXX.17", "STND.CXX.16", "STND.CODE.12"]',
     'refers_to: ["PRIME.4", "STND.CODE.15", "STND.CODE.14", "STND.CODE.12"]'),
    ("called through a function of the work that STND.CXX.17 covers (DSGN.5).",
     "called through a function of the work that STND.CODE.15 covers (DSGN.5)."),
    ("SHOULD respond to it as STND.CXX.16 or STND.CODE.12 provides,",
     "SHOULD respond to it as STND.CODE.14 or STND.CODE.12 provides,"),
]
CXX22 = [
    ('refers_to: ["STND.CXX.16"]', 'refers_to: ["STND.CODE.14"]'),
    ("and answered there as STND.CXX.16 requires (DSGN.5).", "and answered there as STND.CODE.14 requires (DSGN.5)."),
]

# ------------------------------------------------------------------ the document

FRONT = [("waivable: false\n---",
          "waivable: false\nwithdrawn: [" + ", ".join(f'"STND.CXX.{n}"' for n in WITHDRAWN) + "]\n---")]

PURPOSE_1 = (
    "This standard holds the coding practice that is specific to C++. It adds to STND.CODE and STND.DOCS only what "
    "the language makes necessary. It takes the C++ Core Guidelines as the reference for the work's practice and "
    "sets the language edition and the build settings that change what code means (STND.CXX.1, STND.CXX.2, "
    "STND.CXX.3, and STND.CXX.4). It states who owns memory and other owned resources and how sequences and hardware "
    "memory are passed (STND.CXX.5, STND.CXX.6, and STND.CXX.7). It puts the standard library and header-only code "
    "first and keeps results that depend on the library implementation reproducible (STND.CXX.8, STND.CXX.9, and "
    "STND.CXX.10), and recommends generic code and metaprogramming that a reader is able to follow (STND.CXX.11, "
    "STND.CXX.12, and STND.CXX.13). It fixes names and declaration comments (STND.CXX.14 and STND.CXX.15). It covers "
    "failures, including the option that assumes finite values, the boundaries to code that does not follow C++ "
    "rules, and a terminate handler of the work (STND.CXX.18, STND.CXX.19, STND.CXX.20, STND.CXX.21, STND.CXX.22, STND.CXX.23, "
    "STND.CXX.24, and STND.CXX.32), and the mechanical checks of C++ code (STND.CXX.25, STND.CXX.26, and "
    "STND.CXX.27). STND.CODE holds for C++, as for every language, the responses to a failure that PRIME.4 lists, "
    "the declarations that keep a returned failure from being ignored, and the checks that no setting or definition "
    "removes, and, for the code that a release of work of CSQ1 or CSQ0 delivers or runs to produce a reported "
    "result, conformance to the high-assurance coding standard that the work adopts, honest claims of that "
    "conformance, an edition that the standard covers and the toolchain is validated for, and recorded deviations "
    "(STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.17, STND.CODE.18, STND.CODE.19, STND.CODE.20, and "
    "STND.CODE.21); the Notes give their C++ forms.")
PURPOSE_1_SHA = "0ccb1d4398a3769b53d0469bf55618a4313bc2bee75db3c127a575bd204582c1"

PURPOSE_2_OLD = ("STND.CXX.16, STND.CXX.17, and STND.CXX.18 instantiate PRIME.4, STND.CXX.29 instantiates PRIME.2, and "
                 "STND.CXX.3 instantiates GOV.48 and binds agents alone; these five are binding at every class.")
PURPOSE_2_NEW = ("STND.CXX.18 and STND.CXX.32 instantiate PRIME.4, and STND.CXX.3 instantiates GOV.48 and binds agents "
                 "alone; these three are binding at every class.")

TERMS = [
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them;",
     "Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and "
     "High-assurance coding standard have the meanings that STND.CODE gives them;"),
    ("\n| High-assurance coding standard | A coding standard for C++ written for safety-related or mission-critical "
     "software, published or of the work's own making, with a procedure for recording deviations from its rules, its "
     "own or one that the decision record adopting it sets. |\n"
     "| High-assurance code | The code of the work, its headers included, that is compiled into a translation unit "
     "which a release of work of CSQ1 or CSQ0 delivers or runs to produce a reported result. Tests, development "
     "tools, and external code that the work incorporates are not high-assurance code. |", ""),
]

NOTES = [
    ("The sources are the project's research notes cxx-practice.md, cxx-high-assurance.md, and parallel-models.md;",
     "The sources are the project's research notes cxx-practice.md, cxx-high-assurance.md, and parallel-models.md, "
     "with the addendum a2-language-facts.md for Julia's bounds checks;"),
    # the checking paragraph: the reason for STND.CXX.27 beside STND.JL.34 and STND.RUST.20
    ("Hardening against memory corruption by attack is governed by GUARD.17 and the threat model.",
     "Hardening against memory corruption by attack is governed by GUARD.17 and the threat model. STND.JL.34 and "
     "STND.RUST.20 have no counterpart of STND.CXX.27, for reasons of their languages. In Julia an index is checked "
     "unless `@inbounds` or the execution setting `--check-bounds=no`, under which no bounds check is emitted, removes "
     "the check (a2-language-facts.md); STND.JL.13 keeps the check "
     "of an index from untrusted input from either, STND.JL.18 asks the reason at each `@inbounds`, the first sentence "
     "of STND.JL.34 runs the tests once under the production setting, and the Julia standard holds in a default of "
     "its own the bounds checking of the production configuration. In safe Rust, indexing is checked in every build "
     "(unverified here), and STND.RUST.20 concerns overflow checks and debug assertions. The C++ standard library "
     "checks no precondition unless a check mode of it is chosen, so STND.CXX.27 asks for that mode in each reporting "
     "build, and the checking builds of STND.CXX.26 are the counterpart of the forced checks of STND.JL.34. A test "
     "under the settings of the reporting build is the evidence that HW.7 asks wherever a claim rests on the "
     "delivered arithmetic that those settings fix, in C++ as in Julia."),
]

FAILURES = (
    "STND.CODE.14 lists the responses that PRIME.4 admits, a thrown C++ exception among them, and the provisions of "
    "this standard that need a response refer to it. STND.CODE.15 asks for the declaration under which an ignored "
    "returned failure is diagnosed, and the nodiscard attribute meets it; on the return type it also covers indirect "
    "calls, through `std::function` among them, which lose an attribute on the function (unverified). A cast to "
    "`void` or an assignment to `std::ignore` discards the result, which STND.CODE.7 forbids for these failures and "
    "STND.CODE.12 governs for others. STND.CODE.6 keeps a check of untrusted input in every build, and STND.CODE.16 "
    "extends that to the checks of CPS.5 and CPS.9 where those apply. The settings that remove a check in C++ "
    "include `NDEBUG` for `assert`, the evaluation semantic of a contract assertion, the check mode of the library, "
    "and the contract settings of a support library; `NDEBUG` defined in the source before `<cassert>` is included "
    "is the case of the second sentence of STND.CODE.16, whose Notes give the reasoning for `assert` in C and C++. "
    "STND.CXX.18 keeps the binding C++ form of STND.CODE.21 for a translation unit that holds a required check of a "
    "floating-point value, as ruled for C++. Library checks therefore remain a second layer that STND.CXX.27 lets a "
    "budget remove. Each build that STND.BUILD calls a reporting build is a build from which the work reports a "
    "result or makes a release, and so a build that STND.CXX.27 reaches. A C++ exception that no handler catches, "
    "or that leaves a function declared `noexcept`, ends the program through `std::terminate`, whose default handler "
    "calls `std::abort` (unverified); whether an implementation of the standard library writes a diagnosis first is "
    "unverified for each implementation. STND.CXX.32 is the counterpart of the second sentence of STND.RUST.13 for a "
    "panic, and is conditioned as that sentence is: where the work installs a terminate handler, the handler "
    "delivers the diagnosis of a listed condition that an exception carries to it, and where the work installs "
    "none, STND.CODE.14 still asks the halt to carry its diagnosis, which a catch in the entry point of the program "
    "is one way to give. In a program that commands hardware, the end of the program through a terminate handler is "
    "a loss of the commanding software that CPS.4 verifies, and the designed safe state of PRIME.13 is reached on "
    "it, which HW.EMBED.4 states for each output. With C++ exceptions disabled, each throw that remains in the "
    "library ends the program (unverified for each library), which is a halt under STND.CODE.14 once the abort "
    "handler writes a diagnosis. A destructor does not let a C++ exception escape, which the language makes the "
    "default; a failure it detects goes to the response of STND.CODE.14, and the explicit release operation of "
    "STND.CXX.21 lets the caller see the failure first.")

FAILURES_OLD_HEAD = (
    "STND.CXX.16 lists the responses that PRIME.4 admits in C++, and the other provisions that need a response refer "
    "to it. STND.CXX.17 and STND.CXX.18 rest on PRIME.4, STND.CODE.6, and STND.CODE.7, and keep to PRIME.4's list. "
    "The nodiscard attribute meets STND.CXX.17; on the return type it also covers indirect calls, through "
    "`std::function` among them, which lose an attribute on the function (unverified). A cast to `void` or an "
    "assignment to `std::ignore` discards the result, which STND.CODE.7 forbids for these failures and STND.CODE.12 "
    "governs for others. STND.CODE.6 already keeps a check of untrusted input in every build; STND.CXX.18 extends "
    "that to the checks of CPS.5 and CPS.9 where those apply, and the settings that remove a check in C++ include "
    "`NDEBUG` for `assert`, the evaluation semantic of a contract assertion, the check mode of the library, and the "
    "contract settings of a support library. Library checks therefore remain a second layer that STND.CXX.27 lets a "
    "budget remove. Each build that STND.BUILD calls a reporting build is a build from which the work reports a "
    "result or makes a release, and so a build that STND.CXX.27 reaches. With C++ exceptions disabled, each throw "
    "that remains in the library ends the program (unverified for each library), which is a halt under STND.CXX.16 "
    "once the terminate or abort handler writes a diagnosis. A destructor does not let a C++ exception escape, which "
    "the language makes the default; a failure it detects goes to the response of STND.CXX.16, and the explicit "
    "release operation of STND.CXX.21 lets the caller see the failure first.")

HIGH_ASSURANCE = (
    "High assurance. STND.CODE.17 to STND.CODE.20 hold the high-assurance provisions for every language, on the "
    "custodian's rulings for C++ that they accept any high-assurance coding standard that a decision record of the "
    "work adopts, and that for high assurance \"the validation status is more important than the language "
    "standard\". High-assurance coding standards for safety-related C++ restrict the language to a subset that "
    "analyzers are able to check, commonly by limiting dynamic allocation, recursion, unbounded loops, C++ "
    "exceptions, casts, unions, and the preprocessor. An assertion that such a standard keeps in production builds "
    "responds as STND.CODE.14 provides, entering the designed safe state of PRIME.13 for a component that commands "
    "hardware, which CPS.4 verifies and HW.EMBED.4 states for each output, and halting with a diagnosis for one that "
    "does not, such as a criticality or shielding calculation. In C++, the edition of STND.CODE.19 is an edition of "
    "the ISO C++ standard that the adopted standard covers and for which each compiler and standard library "
    "implementation of the toolchain matrix of the unit holds the validation or qualification that the work "
    "requires; it is often older than the edition of STND.CXX.2, which yields to it, and the provisions of this "
    "standard that name idioms of later editions give the forms for earlier ones. A header that a CSQ0 controller "
    "and a CSQ3 simulation share is high-assurance code (GOV.14); the human owner may record a less severe class for "
    "a component shown to be isolated (GOV.13), which keeps a simulation's large dynamic arrays out of a rule on "
    "allocation.")
HA_1_SHA = "bd2bd7732a1efe56340cc89a8cbddb017e71e04f30ace5b03cf0954bf0f6af42"
HA_2_SHA = "e0a2fef37369ddcd1c30e1ede272f2a50ff225445f418f80faa31a08ec2e3f61"

CLASS = (
    "Under STND.CLASS.10, each default instantiates only VV, REPRO, INTPR, DSGN, SIMPL, RSRC, or a provision of HW, "
    "CPS, or NUMER, and applies from CSQ3; work of CSQ4 may omit it. Several apply earlier than the part of LVL0 they "
    "instantiate, and so tighten above the floor (PRIME.15). STND.CXX.6 and STND.CXX.7 instantiate DSGN.4, and "
    "STND.CXX.21 and STND.CXX.22 DSGN.5, which STND.CLASS.10 applies from CSQ2. STND.CXX.13 takes the expected "
    "results of its assertions from a stated requirement, the reference independent of the implementation that "
    "STND.CLASS.10 asks of VV.1 from CSQ2. STND.CXX.26 instantiates the verification of DSGN.15, applied from CSQ2. "
    "The provisions of STND.CONC that STND.CXX.15 and STND.CXX.23 cite, and of which the Notes give STND.CXX.26 as a "
    "form, take the same onsets, STND.CONC.3 and STND.CONC.6 from CSQ3 and STND.CONC.25 from CSQ2, so the citations "
    "move no rule to another class. STND.CXX.24 and STND.CXX.27 instantiate the checking of DSGN.2 that "
    "STND.CLASS.10 applies from CSQ1. Each asks for a type, a check that a tool runs, or a statement. The provisions "
    "of STND.CODE that the defaults cite keep their own onsets: STND.CODE.17 and STND.CODE.19 from CSQ1 for "
    "high-assurance code, the record of STND.CODE.20 wherever such a standard is adopted, and the binding "
    "STND.CODE.14 and STND.CODE.15 at every class, so the citations move no rule to another class. STND.CXX.18 and "
    "STND.CXX.32 bind at every class, CSQ4 included. STND.CXX.18 costs one choice of compiler option for a unit that "
    "holds a required check. STND.CXX.32 reaches only a terminate handler that the work installs and a listed "
    "condition that already ends the program there, and asks only for the actionable diagnosis that PRIME.4 names, "
    "at the cost of the wording of that handler; without it a handler of the work is able to end the program "
    "without a diagnosis. It asks for no work that PRIME.4 does not, so it raises no floor (GOV.11); no ruling of the "
    "custodian covers it, and the argument is the one that the ratification of 2026-10-24 accepted for the second "
    "sentence of STND.RUST.13, which is conditioned in the same way. STND.CXX.3 asks an "
    "agent for one decision record when it lowers an edition, or creates a unit below the edition of STND.CXX.2 or "
    "its project alternative, which at CSQ4, where STND.CXX.2 may be omitted, costs one sentence; without it the "
    "custodian's direction on the edition is lost silently. That STND.CXX.3 and STND.CXX.18 raise no floor (GOV.11) is "
    "the custodian's ruling of 2026-10-23 (PRIN.10). Work moved to CSQ1 or CSQ0 meets STND.CODE.17, STND.CODE.18, "
    "STND.CODE.19, and STND.CODE.20 before it is relied upon at that class (GOV.14).")
CLASS_SHA = "e11adfe59013f4f3289e20710348d1f819d07c622c77d430a9a9d2c604829d22"

READING = (
    "STND.CXX.16, STND.CXX.17, STND.CXX.28, STND.CXX.29, STND.CXX.30, and STND.CXX.31 are withdrawn, their outcomes "
    "now STND.CODE.14, STND.CODE.15, STND.CODE.17, STND.CODE.18, STND.CODE.19, and STND.CODE.20 for every language, "
    "and the front matter lists them as withdrawn; STND.CXX.18 drops its first sentence, now the first sentence of "
    "STND.CODE.16, and keeps its second, the binding C++ form of the default STND.CODE.21, as ruled; STND.CXX.2, "
    "STND.CXX.8, STND.CXX.21, and STND.CXX.22 cite the provisions of STND.CODE in their place, and the second "
    "sentence of STND.CXX.2 leaves the later features of high-assurance code to STND.CODE.19; new STND.CXX.32 "
    "(binding, PRIME.4) has a terminate handler that the work installs deliver the diagnosis of each listed "
    "condition that a C++ exception carries to it, the C++ counterpart of the second sentence of STND.RUST.13 and "
    "conditioned as it is; Terms import Untrusted input, High-assurance code, and High-assurance coding standard "
    "from STND.CODE and drop this standard's own definitions of the last two; the Purpose and the Notes cite "
    "STND.CODE for the moved rules and for the reasoning on `assert`, give the reason why STND.CXX.27 has no "
    "counterpart in STND.JL.34 and STND.RUST.20, and state the floor argument and the onset of STND.CXX.32")

ROW = f"| 1.2 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.CXX to revision 1.2, ratified by the custodian on {DATE}, on STND.CODE 1.2: {READING}. "
    "The change is minor because it removes six provisions and a sentence, alters the second sentence of "
    "STND.CXX.2, and adds one binding provision. The obligations of C++ code that the withdrawn provisions and "
    "sentence held stay in force through STND.CODE.14 to STND.CODE.20 and STND.CXX.18, with two changes that the Notes "
    "of STND.CODE argue: STND.CODE.15 applies where a form of declaration that diagnoses an ignored result exists, "
    "which the nodiscard attribute gives C++ at each edition that has it, and the second sentence of STND.CODE.16 "
    "reaches a definition of NDEBUG in the source, which STND.CXX.18 did not. The carve-out in STND.CXX.2 keeps a "
    "permission of a default from widening one that STND.CODE.19 limits to one feature. The withdrawn identifiers "
    "are listed in the field withdrawn and are never given to another provision (STND.IDENT.14). The citations in "
    "STND.CXX.2, STND.CXX.8, STND.CXX.21, and STND.CXX.22 change their target and not their outcome. Class onsets: "
    "STND.CXX.32 binds at every class; no other onset changes. Floor (GOV.11): STND.CXX.32 reaches only a terminate "
    "handler that the work installs and a listed condition that already ends the program there, and asks only for "
    "the actionable diagnosis that PRIME.4 names, at the cost of the wording of that handler; no ruling covers it, "
    "and the custodian decides it (R22). STND.CXX.27 is unchanged, a reasoned no change: Julia checks an index "
    "unless `@inbounds` or `--check-bounds=no` removes the check and keeps the check of an untrusted index from both "
    "(STND.JL.13), safe Rust checks indexing, and the C++ standard library checks nothing unless a check mode is "
    "chosen. Transition (GOV.42): existing code meets STND.CXX.32 when a change next touches its terminate handler. "
    "Review of STND.HARN.28 by the command pairs, a cold review, and their dispositions; record "
    "review-records/round-2026-10-25-close/p1/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    for n in WITHDRAWN:
        (root / f"STND/CXX/{n}.md").unlink()
    replace_text(root, "STND/CXX/2.md", CXX2)
    replace_text(root, "STND/CXX/18.md", CXX18)
    replace_text(root, "STND/CXX/8.md", CXX8)
    replace_text(root, "STND/CXX/21.md", CXX21)
    replace_text(root, "STND/CXX/22.md", CXX22)
    (root / "STND/CXX/32.md").write_text(B.provision_text("STND.CXX", NEW32, "adopted", DATE), encoding="utf-8")
    replace_text(root, "STND/CXX/_doc.md", FRONT + [(PURPOSE_2_OLD, PURPOSE_2_NEW)] + TERMS + NOTES
                 + [(FAILURES_OLD_HEAD, FAILURES)])
    swap_paragraphs(root, "STND/CXX/_doc.md", [
        ("This standard holds the coding practice that is specific to C++", PURPOSE_1_SHA, PURPOSE_1),
        ("High-assurance coding standards for safety-related", HA_1_SHA, HIGH_ASSURANCE),
        ("The custodian rules that for high assurance", HA_2_SHA, ""),
        ("Under STND.CLASS.10, each default instantiates only VV", CLASS_SHA, CLASS),
    ])
    res = B.derive_fields(root, ["STND.CXX.2", "STND.CXX.8", "STND.CXX.18", "STND.CXX.21", "STND.CXX.22", "STND.CXX.32"])
    for ident, r in res.items():
        if r.unresolved:
            raise ValueError(f"{ident}: {r}")
    if not res["STND.CXX.32"].forced:
        raise ValueError("STND.CXX.32: not binding")
    raise_revision(root, "STND/CXX", "1.1.1", "1.2", ROW)
    B.write_references(root, ["STND.CXX"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CXX"], scope=["STND/CXX"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CXX 1.2")
