"""Round d of 2026-10-28: STND.CODE 1.4 and STND.DEPS 1.2, the provisions that the language standards cite."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import rounds_common as F  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

REC = "review-records/rounds-2026-10-28/round-d/decisions.md"

# ---------------------------------------------------------------- STND.CODE 1.4

CODE_NEW = [
    P(27, "Finite-value annotations near checks", "Failures", """
Code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs SHOULD NOT carry an annotation in its source that, by its documentation, lets the compiler assume that floating-point values are finite in the code that holds the check (DSGN.2).
""", ["DSGN.2"], refs=["STND.CODE.6", "STND.CODE.16"]),
    P(28, "Names under a stated convention", "Source", """
Each name that the source of the work declares SHOULD follow the convention of names that the standard of its language gives (INTPR.1). Where the standard of its language gives none, each such name SHOULD follow the convention that the repository configuration names (INTPR.1). Under each convention that this provision or the standard of a language asks a name to follow, a name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).
""", ["INTPR.1", "INTPR.4"], refs=["NUMER.4", "STND.DOCS.12"]),
    P(29, "Seeded random generators", "Randomness", """
Other than a generator derived for a part of divided work, each generator of random numbers that the work constructs SHOULD be constructed at an entry point, from a seed that the record of the run holds (DSGN.17, REPRO.1). Where an entry point seeds a generator from fresh entropy, it SHOULD record that entropy with the run (REPRO.1). Where work divided into parts draws random numbers, each part SHOULD draw from a stream that a spawning, jump-ahead, or counter-based facility of its generator library derives from the root seed of the run and the index of the part, as STND.VVUQ.62 recommends (DSGN.17, REPRO.3).
""", ["DSGN.17", "REPRO.1", "REPRO.3"], refs=["STND.VVUQ.62"]),
    P(30, "Hash values outside results", "Randomness", """
Where the documentation of a hash function leaves the values that it returns free to change between runs or between releases, each output, each record of data, and each test reference of the work SHOULD exclude those values (REPRO.3, REPRO.6). Where the documentation of a collection leaves its order of iteration free to change between runs or between releases, each reported result on whose path the collection lies SHOULD be independent of that order (REPRO.3).
""", ["REPRO.3", "REPRO.6"]),
    P(31, "Tolerances stated at comparisons", "Source", """
Each comparison of floating-point values within a tolerance, by a function or by an expression, SHOULD state the parameters of its tier of STND.VVUQ.1, the relative and the absolute part of STND.VVUQ.5 for the rounding and numerical-error tiers, and its treatment of a NaN under STND.VVUQ.3 (NUMER.11, VV.3, SIMPL.6). Each such tolerance SHOULD be a named constant that carries its basis under NUMER.11, as STND.CODE.10 recommends (NUMER.11, REPRO.7). A comparison of exact values, or one that the bitwise tier of STND.VVUQ.1 admits, MAY use the equality operators of its language (VV.3).
""", ["NUMER.11", "VV.3", "SIMPL.6", "REPRO.7"], refs=["STND.VVUQ.1", "STND.VVUQ.5", "STND.VVUQ.3", "STND.CODE.10"]),
    P(32, "Language provisions in static checks", "Checking", """
The static checks that the repository configuration names under STND.CODE.4 SHOULD decide each provision of this standard and of the standard of each language of the work whose compliance a static check among the means of the work is able to decide (DSGN.3).
""", ["DSGN.3"], refs=["STND.CODE.4"]),
    P(33, "Diagnoses from installed failure handlers", "Failures", """
Where the work replaces or installs a hook or a handler that its language or runtime runs on a failure that a mechanism of the language propagates, or is unable to propagate, that hook or handler SHALL deliver to the operator, or to the record of the run, a diagnosis of each condition that PRIME.4 lists, that such a failure carries to it, and that no other response of STND.CODE.14 answers (PRIME.4, STND.CODE.14).
""", ["PRIME.4"], refs=["STND.CODE.14"], mode="binding"),
    P(34, "Claims of absent undefined behavior", "Checking", """
Each claim, in a report, in the record of a result or of a release, or in a review, that code of the work is free of undefined behavior or of a kind of it, or that no use of an interface of the work is able to cause undefined behavior, SHALL state each means by which that was checked and the code, the code of dependencies included, that each means covered (PRIME.2). Such a claim SHALL NOT extend beyond the code and the executions that those means covered (PRIME.2).
""", ["PRIME.2"], mode="binding"),
    P(35, "Dependency failure results diagnosed", "Failures", """
Where the language, or a compiler or a static check among the means of the work, provides a form of declaration of STND.CODE.15, each function of a dependency that reports in its result a failure of a kind that PRIME.4 lists SHOULD be called through a declaration in such a form, its own or that of a function of the work that wraps it (DSGN.5).
""", ["DSGN.5"], refs=["STND.CODE.15", "PRIME.4"]),
]
CODE_BINDING = {33, 34}

CODE14 = [(
    "or by a mechanism of its language, an exception among them, that propagates the condition to the caller "
    "(PRIME.4).",
    "or by a mechanism of its language, an exception among them, that propagates the condition to the caller "
    "(PRIME.4). A record that library code writes to a log SHALL NOT be the only visible degradation (PRIME.4).")]

CODE21_BODY = (
    "Code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs SHALL NOT be compiled "
    "under an execution setting that, by the documentation of its compiler, lets the compiler assume that "
    "floating-point values are finite (PRIME.4, DSGN.2).")

CODE_DOC = [
    ("It adds to DSGN, SIMPL, INTPR, REPRO, VV, QA, PRIME.2, and PRIME.4 only what makes their outcomes checkable at "
     "each change.",
     "It adds to DSGN, SIMPL, INTPR, REPRO, VV, QA, NUMER.11, PRIME.2, and PRIME.4 only what makes their outcomes "
     "checkable at each change."),
    ("Beside structure, checking, tests, and source, it states the responses to a failure that PRIME.4 lists, the "
     "declarations that keep a returned failure from being ignored, and the checks that no setting or definition "
     "removes (STND.CODE.14, STND.CODE.15, and STND.CODE.16), and recommends against an assumption of finite values "
     "in code that holds such a check (STND.CODE.21).",
     "Beside structure, checking, tests, and source, it states the responses to a failure that PRIME.4 lists, the "
     "declarations that keep a returned failure from being ignored, the checks that no setting or definition "
     "removes, and the settings that let a compiler assume finite values in code that holds such a check "
     "(STND.CODE.14, STND.CODE.15, STND.CODE.16, and STND.CODE.21), recommends against the annotations that do the "
     "same (STND.CODE.27), and has a hook or a handler that the work installs deliver the diagnosis of a listed "
     "condition that reaches it (STND.CODE.33). It states once for every language a convention of names "
     "(STND.CODE.28), seeded generators of random numbers and the values that change between runs (STND.CODE.29 "
     "and STND.CODE.30), the tolerances of comparisons (STND.CODE.31), the static checks of the provisions of the "
     "language standards (STND.CODE.32), claims that code is free of undefined behavior (STND.CODE.34), and the "
     "calls of functions of dependencies that report a listed failure in their results (STND.CODE.35)."),
    ("STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, and STND.CODE.16 instantiate PRIME.4, and STND.CODE.18 "
     "instantiates PRIME.2, so these six are binding and apply at every class;",
     "STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.21, and STND.CODE.33 instantiate "
     "PRIME.4, and STND.CODE.18 and STND.CODE.34 instantiate PRIME.2, so these nine are binding and apply at every "
     "class;"),
    ("| Owned resource | Memory, a file, a lock, a handle that a foreign interface issues, or another facility that "
     "code acquires and has to release. |\n",
     "| Owned resource | Memory, a file, a lock, a handle that a foreign interface issues, or another facility that "
     "code acquires and has to release. |\n"
     "| Library code | Code of the work that other code calls through its interface, other than tests and the code "
     "that holds the entry point of a program; in a language whose standard defines the term, the code that its "
     "definition gives. |\n"),
    # Ignored results: the calls of functions of dependencies.
    ("The custodian's ruling of 2026-10-23 on this outcome was made for C++; STND.STDC and STND.RUST, adopted on "
     "2026-10-24, condition it on a compiler or static check among the means of the work, and this provision "
     "conditions it on a form of declaration that the language or those means provide.",
     "The custodian's ruling of 2026-10-23 on this outcome was made for C++; STND.STDC and STND.RUST, adopted on "
     "2026-10-24, condition it on a compiler or static check among the means of the work, and this provision "
     "conditions it on a form of declaration that the language or those means provide. STND.CODE.35 carries the "
     "same form to each call of the work to a function of a dependency that reports a listed failure in its result: "
     "through the declaration that the dependency gives, which a compiler or an analyzer that knows the functions "
     "of a library also gives, or through a function of the work that wraps the call and is so declared. In C, the "
     "test of STND.STDC.28 or an error handler that ends the run receives some such failures, and STND.STDC.29 has "
     "the call carry the suppression of STND.CODE.4 there. STND.CODE.35 rests on the contract of each external "
     "component (DSGN.5), a row that STND.CLASS.10 applies from CSQ2, and applies from CSQ2."),
    ("and the status returns and releases of STND.CXX.21.", "and the failed releases of STND.CXX.21."),
    # Onset paragraph: the two new defaults whose onsets the Notes state.
    ("Under STND.CLASS.10, each default provision other than STND.CODE.17, STND.CODE.19, STND.CODE.20, STND.CODE.21, "
     "STND.CODE.22, STND.CODE.23, and STND.CODE.24 instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or QA and applies "
     "from CSQ3; work of CSQ4 omits it. The onsets of STND.CODE.17, STND.CODE.19, STND.CODE.20, STND.CODE.21, "
     "STND.CODE.22, STND.CODE.23, and STND.CODE.24 are stated above.",
     "Under STND.CLASS.10, each default provision other than STND.CODE.17, STND.CODE.19, STND.CODE.20, STND.CODE.21, "
     "STND.CODE.22, STND.CODE.23, STND.CODE.24, STND.CODE.31, and STND.CODE.35 instantiates only DSGN, SIMPL, INTPR, "
     "REPRO, VV, or QA and applies from CSQ3; work of CSQ4 omits it. The onsets of STND.CODE.17, STND.CODE.19, "
     "STND.CODE.20, STND.CODE.21, STND.CODE.22, STND.CODE.23, STND.CODE.24, STND.CODE.31, and STND.CODE.35 are "
     "stated above."),
]

CODE_RESPONSES = (
    "Responses. STND.CODE.14 lists the responses that PRIME.4 admits, together with the pass of the condition to a "
    "caller, in its result, in an argument that the caller passes to receive it, or by a mechanism of its language "
    "that propagates it, which STND.CODE.7 keeps from discarding it and which STND.CODE.14 binds in turn. Its forms "
    "in each language are these: in Python and in Julia, a raised or thrown exception, or a returned result; in "
    "Rust, a returned result or a panic, which propagates the condition under the unwinding strategy and halts "
    "under the aborting one, and so is a response under either; in C++, a thrown exception, a returned value, or an "
    "argument that the caller passes; in C, a returned value or an argument that the caller passes, other than a "
    "report through errno alone (STND.STDC.2); in Fortran, which has no exceptions, the result of a function or a "
    "status argument, which is an argument that the caller passes to receive the condition; in Lean, a result of a "
    "type that carries the condition, or an error raised in a monad whose caller receives that error; and in a "
    "hardware description, a status at the interface, the form that HDES.14 asks for saturation and overflow. A "
    "language standard adds to them only where its language sets a trap: the warning categories that the default "
    "filters of Python show (STND.PY.22), the levels at which the default logger of Julia shows a record "
    "(STND.JL.15), and the report through errno that STND.STDC.2 excludes. A record that library code writes to a "
    "log reaches no person unless the program that uses the library installs a handler or a logger that shows it, "
    "so the second sentence of STND.CODE.14 keeps such a record from being the only visible degradation in every "
    "language; an entry point whose handler shows the record degrades visibly through it, and in Julia a record "
    "that other code writes counts at the levels of STND.JL.15. A condition that a mechanism of the language "
    "carries past every caller ends a thread or the program, and PRIME.4 asks that end to carry a diagnosis. The "
    "default exception hooks of Python and panic hook of Rust print the condition (the Notes of STND.PY and "
    "STND.RUST), and STND.CXX.33 recommends a terminate handler where the one that the C++ implementation provides "
    "writes none; STND.CODE.33 has a hook or a handler that the work installs in place of a default deliver the "
    "diagnosis of each listed condition that reaches it and that no other response answers, so work that keeps "
    "the defaults meets it unchanged. A Rust panic that is caught and answered by a returned error or a visible "
    "degradation carries its diagnosis through that response, and a Rust build without the standard library "
    "defines the handler of a panic, which STND.CODE.33 reaches. A language in which the work installs no "
    "replaceable hook or handler for that end gives STND.CODE.33 no subject: Julia, for which the research notes "
    "of the corpus hold no source on such a hook (unverified), and C, Fortran, Lean, and SystemVerilog. "
    "STND.CODE.14 asks only the responses that PRIME.4 already requires, in the forms that each language gives, and "
    "its second sentence only keeps out a form that leaves the condition unseen, so it raises no floor in any "
    "language (GOV.11); the custodian's rulings of 2026-10-23 that the same list raises no floor were made for C++, "
    "Python, and Julia, the ratification of 2026-10-24 accepted the second sentence for Rust, and the custodian "
    "ruled on 2026-10-28 that a record that library code writes to a log is never the only visible sign of a "
    "degraded result, in any language. STND.CODE.33 reaches only a hook or a handler that the work installs and a "
    "listed condition that already ends a thread or the program there, or that the runtime drops, and asks only "
    "for the actionable diagnosis that PRIME.4 names, at the cost of the wording of that hook or handler; a "
    "replaced hook that drops a listed condition without a diagnosis lets the program end or continue past the "
    "error in silence, which the last sentence of PRIME.4 forbids. It asks for no work that PRIME.4 does not, so it "
    "raises no floor (GOV.11), the argument that the ratification of 2026-10-24 accepted for the panic hook of "
    "Rust, and that holds for a hook or a handler of any language, since it concerns what the handler that the "
    "work writes delivers and not a construct of the language.")

CODE_FINITE = (
    "Finite values. An execution setting or an annotation that, by the documentation of its compiler, lets the "
    "compiler assume finite floating-point values licenses the deletion of tests for not-a-number and infinite "
    "values. The documentation of two compilers states the assumption and names no test that it deletes (the same "
    "research note), so whether a given compiler deletes them is unverified, and the Notes of STND.FTN record the "
    "hazard as unverified for Fortran compilers. STND.CODE.21 therefore keeps such a setting from the compilation "
    "of code that holds a check that the floor requires, the check of untrusted input of STND.CODE.6 or a check of "
    "CPS.5 or CPS.9 under STND.CODE.16, in every language, whether or not its compiler is known to delete the "
    "check, and STND.CODE.27 recommends against an annotation in the source that does the same. STND.CXX.18 and "
    "STND.STDC.40 state the rule of STND.CODE.21 for C++ and for C. In Julia, the annotation is the `@fastmath` "
    "macro and the setting a mode of the compiler; the Python language has neither, and a compiler of Python code "
    "that offers such an option is reached by STND.CODE.21. Where a setting does remove the check, STND.CODE.6 or "
    "the first sentence of STND.CODE.16 already excludes it, in every language. STND.CODE.21 costs one choice of "
    "compiler option for code that holds a required check, and asks for no check that the floor does not already "
    "require, so it raises no floor in any language (GOV.11); the custodian ruled so for C++ on 2026-10-23, the "
    "ratification of 2026-10-24 applied it to C, and the custodian ruled on 2026-10-28 that the option binds for "
    "the checks that the floor requires, in every language alike. It binds at every class, CSQ4 included. "
    "STND.CODE.27 instantiates the check of DSGN.2 where untrusted data enters, rests on no row of STND.CLASS.10, "
    "and applies from CSQ3.")

CODE_SHARED = (
    "Rules for every language. A rule that more than one language standard would state in one text, with no "
    "construct of its language, is held here once (GOV.31), and the language standards keep the constructs that "
    "give it a form. STND.CODE.28 has the names of the source follow the convention that the standard of its "
    "language gives, the tables of STND.CXX.14 and STND.JL.6 and the style guide of STND.PY.1 among them, or that "
    "the repository configuration names where the language standard gives none; the research notes of the corpus "
    "retrieved no convention of names that the definition of C, Fortran, or Lean fixes (unverified), and a "
    "convention that the lints of a compiler check, as those of the Rust compiler check the case of names, is "
    "named at no added cost. Its third sentence keeps the case of a symbol of the notation of NUMER.4, a matrix "
    "`A` or an operator `K`, under each such convention, and a lint that reports such a name is suppressed at its "
    "location with its reason under STND.CODE.4. STND.CODE.29 keeps a seed or fresh entropy from entering below "
    "the entry point, where an integer passed to two functions gives them identical streams and an unrecorded draw "
    "of entropy is repeated by no seed; its third sentence keys the stream of each part of divided work, parts run "
    "as separate runs included, to the root seed and the index of the part by a facility of STND.VVUQ.62, and "
    "STND.CONC.23 keys each stream of a computation divided among concurrent tasks to a part in the same way. "
    "STND.PY.15 and STND.JL.22 give the parameter through which a generator arrives in each language. STND.CODE.30 "
    "keeps out of results the values that a hash function leaves free to change, among them the built-in hash of a "
    "string in Python, which varies with the hash seed of each run, and the values of `hash` in Julia, which have "
    "changed between releases, and the iteration orders of the collections built on them, a set of strings in "
    "Python and a `Dict` or a `Set` in Julia (the Notes of STND.PY and STND.JL). STND.CODE.31 has each comparison "
    "within a tolerance state its parameters where the code makes it, since the defaults of comparison functions "
    "differ and a comparison that relies on them decides for a reason that the reader does not see: the isclose "
    "function of the math module of Python takes an absolute tolerance of zero, and `isapprox` of Julia, the "
    "function behind `≈`, a relative tolerance from the machine epsilon and an absolute tolerance of zero, so that "
    "`x ≈ 0` holds only for an exact zero. Each tolerance is a named constant with its basis beside it "
    "(STND.CODE.10, NUMER.11), so that a copied value without a basis stands out in review. STND.CODE.32 has the "
    "static checks that the repository configuration names decide each provision of the language standards that a "
    "static check among the means of the work is able to decide, the linter of STND.PY.2 and the static checks of "
    "STND.RUST.31 among them. STND.CODE.28 to STND.CODE.32 rest on no row of STND.CLASS.10, STND.CODE.31 resting "
    "on NUMER.11 and VV.3 and STND.CODE.32 on the mechanical checks of DSGN.3, whose CSQ0 row for each contract of "
    "a safety-related component stays with that row, so each applies from CSQ3. Each is a default, a tightening "
    "above the floor that a recorded decision replaces (PRIME.15, GOV.19), so none raises the floor (GOV.11).\n\n"
    "Claims of soundness. STND.CODE.34 keeps a claim that code is free of undefined behavior, or of a kind of it, "
    "or that no use of an interface of the work is able to cause it, the claim that a Rust module is a sound "
    "module among them, to what its means checked: a detector observes only the executions that it runs, an "
    "analyzer is documented as sound for a kind of undefined behavior or not, and code of a dependency in the call "
    "chain is code that a claim covers or leaves out (the Notes of STND.RUST and STND.STDC). STND.RUST.33 and "
    "STND.STDC.38 add what the record of such a check states. A soundness argument at an unsafe construct is not "
    "such a claim. PRIME.2 already forbids misrepresenting the status of evidence, and the cost is one sentence for "
    "each such claim, so STND.CODE.34 raises no floor (GOV.11), the argument on which STND.RUST was adopted with "
    "the same rule for Rust on 2026-10-24; it concerns claims and not the constructs of a language, so the argument "
    "holds in every language, and work that makes no such claim owes nothing. It binds at every class, CSQ4 "
    "included.")

CODE_READING = (
    "STND.CODE.14 adds that a record that library code writes to a log is never the only visible degradation, and "
    "Terms define Library code, read in each language whose standard defines the term by that definition; "
    "STND.CODE.21 binds (PRIME.4) for every language that code that holds a check of a floating-point value that "
    "STND.CODE.6 or STND.CODE.16 governs is not compiled under a setting that lets the compiler assume finite "
    "values, and is retitled Finite-value settings near checks; new STND.CODE.27 (default) holds its former second "
    "sentence, on annotations; new STND.CODE.28 to STND.CODE.32 (defaults) state once for every language the "
    "convention of names and the names that the notation of NUMER.4 fixes, seeded generators and the streams of "
    "parts, hash values and iteration orders outside results, the tolerances of comparisons, and the static checks "
    "of the provisions of the language standards; new STND.CODE.33 (binding, PRIME.4) has a hook or a handler that "
    "the work installs deliver the diagnosis of each listed condition that reaches it; new STND.CODE.34 (binding, "
    "PRIME.2) limits each claim that code is free of undefined behavior, or sound, to the means that checked it and "
    "what they covered; new STND.CODE.35 (default, from CSQ2) has each function of a dependency that reports a "
    "listed failure in its result called through a declaration under which an ignored result is diagnosed; the "
    "Purpose lists the new provisions and the binding ones and names NUMER.11; the Notes give the forms of "
    "STND.CODE.14 in each language, and the reasons, the floor arguments, and the onsets of the changed and new "
    "provisions, and the class paragraph adds STND.CODE.31 and STND.CODE.35 to the provisions whose onsets the "
    "Notes state")

CODE_RATIONALE = (
    f"Minor amendment of STND.CODE, revision 1.4, ratified by the custodian on {F.DATE}: {CODE_READING}. The change "
    "is minor under STND.IDENT.3 because it adds nine provisions and one defined meaning, adds an obligation to "
    "STND.CODE.14, and changes the mode of STND.CODE.21 from default to binding. The custodian ruled under D1 that "
    "each outcome is held by one provision of this standard for every language, that the finite-value option binds "
    "only for the checks that the floor requires, that STND.CODE.14 carries the forms of each language, and that a "
    "library log record is never the only visible sign of a degraded result. Floor (GOV.11): the second sentence "
    "of STND.CODE.14 asks no response beyond PRIME.4 and keeps out one form that leaves the condition unseen; "
    "STND.CODE.21 costs one choice of compiler option for code that holds a check that the floor already requires; "
    "STND.CODE.33 asks only the diagnosis that PRIME.4 names, of a hook or a handler that the work installs; "
    "STND.CODE.34 asks one sentence for each claim, where PRIME.2 already forbids misrepresenting the status of "
    "evidence; so none raises the floor, and these four bind at every class. The new defaults ask, against the "
    "language provisions that they replace, these things more: the convention of names, the generators, the hash "
    "values, the tolerances, and the static checks in each language that had no such provision, and the "
    "declaration of a function of a dependency in C++ through the declaration of the dependency or a wrapper in "
    "place of a wrapper alone; and this less: the static checks decide the provisions that a static check among "
    "the means of the work decides, where STND.RUST.31 named each that a static check of Rust source is able to "
    "decide. Each is a tightening above the floor that a recorded decision replaces (PRIME.15, GOV.19). Class "
    "onsets: STND.CODE.27 to STND.CODE.32 apply from CSQ3 and STND.CODE.35 from CSQ2. Transition (GOV.42): "
    "existing code conforms when a change next touches it; a hook or a handler that the work installs, and a claim "
    "made after the amendment, conform at once. Rulings D1 of {F.RECORD}; register entries R6.2 (CL3, CL4, CL5, "
    "CL6, CL10, CL13, CL18, CL23, CL25) of review-records/deep-review-2026-10-28/register.md; decisions 1 to 9 of "
    f"{REC}." + F.AUTHOR)


def apply_code(root: Path, at: str) -> None:
    root = Path(root)
    for p in CODE_NEW:
        (root / f"STND/CODE/{p['n']}.md").write_text(B.provision_text("STND.CODE", p, "adopted", F.DATE),
                                                    encoding="utf-8")
    replace_text(root, "STND/CODE/14.md", CODE14)
    F.set_body(root, "STND/CODE/21.md", CODE21_BODY, title="Finite-value settings near checks", mode="binding",
               instantiates=["PRIME.4", "DSGN.2"])
    F.check_fields(root, [f"STND.CODE.{p['n']}" for p in CODE_NEW if p["n"] not in CODE_BINDING])
    F.check_fields(root, ["STND.CODE.14", "STND.CODE.21", "STND.CODE.33", "STND.CODE.34"], binding=True)
    replace_text(root, "STND/CODE/_doc.md", CODE_DOC)
    F.swap_para(root, "STND/CODE/_doc.md", "Responses. STND.CODE.14 lists the responses", CODE_RESPONSES)
    F.swap_para(root, "STND/CODE/_doc.md", "Finite values. An execution setting", CODE_FINITE)
    path = root / "STND/CODE/_doc.md"
    text = path.read_text(encoding="utf-8")
    anchor = "Foreign interfaces. The terms Foreign interface and Owned resource are defined here once"
    if text.count(anchor) != 1:
        raise ValueError("STND.CODE: the Notes on foreign interfaces are not unique")
    path.write_text(text.replace(anchor, CODE_SHARED + "\n\n" + anchor, 1), encoding="utf-8")
    row = f"| 1.4 | {F.DATE} | Minor amendment (GOV.41): {CODE_READING}. |"
    F.finish(root, "STND/CODE", "STND.CODE", "1.3", "1.4", row, CODE_RATIONALE, at)


# ---------------------------------------------------------------- STND.DEPS 1.2

DEPS_NEW = P(13, "Builds at locked revisions", "Records", """
Other than a check that the standard of its language asks to run against newer revisions, each build of the checks and of each release of the work whose lock file is under version control SHOULD use the revisions that the lock file records, and fail on a lock file that does not match the files that declare its packages (REPRO.1).
""", ["REPRO.1"])

DEPS_DOC = [
    ("the last trigger narrows that of STND.DFLT.11, which reviews every direct dependency, to the pinned revision "
     "that the unit changes.",
     "the last trigger is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit "
     "changes."),
    ("what the dependency record holds, and which lock files are kept under version control.",
     "what the dependency record holds, which lock files are kept under version control, and which revisions the "
     "builds of the checks and of the releases use."),
    ("STND.PY, STND.JL, and STND.RUST name the lock files of their languages, the manifest of a Julia environment "
     "among them, and STND.RUST.30 adds builds from the revisions that a committed lock file records.",
     "STND.PY, STND.JL, and STND.RUST name the lock files of their languages, the manifest of a Julia environment "
     "among them. STND.DEPS.13 has each build of the checks and of each release use the revisions that a committed "
     "lock file records, so that what the checks judged is what the release builds; the check against newer "
     "revisions that STND.RUST.1 and STND.JL.3 ask, which reports its failure without blocking a change, is the one "
     "build of the checks that leaves the lock file. STND.LEAN.1 adds the revisions of the Lean toolchain and of "
     "each checker, which no lock file of packages records."),
]

DEPS_READING = (
    "new STND.DEPS.13 (default, REPRO.1) has each build of the checks and of each release of work whose lock file is "
    "under version control use the revisions that the lock file records, and fail on a lock file that does not "
    "match the files that declare its packages, other than a check that the standard of its language runs against "
    "newer revisions, the rule that STND.RUST.30 held for Rust, for every language; the Purpose names it; the Notes "
    "cite it in place of STND.RUST.30, and describe STND.DFLT.11 as STND.DFLT 1.6 reads it, reviewing each "
    "dependency that the unit changes")
DEPS_RATIONALE = (
    f"Minor amendment of STND.DEPS, revision 1.2, ratified by the custodian on {F.DATE}: {DEPS_READING}. The change "
    "is minor under STND.IDENT.3 because it adds one default provision. The custodian ruled under D1 that each "
    "outcome is held by one provision for every language; the provision asks of Python, Julia, C, C++, Fortran, "
    "and Lean work that commits a lock file what STND.RUST.30 asked of Rust, and asks nothing where no lock file is "
    "under version control. It is a default, a tightening above the floor that a recorded decision replaces "
    "(PRIME.15, GOV.19), so it raises no floor (GOV.11). Class onset: it rests on no row of STND.CLASS.10 and "
    "applies from CSQ3, as STND.RUST.30 did. Transition (GOV.42): the builds of the checks and of the releases "
    "conform from the next change to the repository configuration. The sentence of the Notes on STND.DFLT.11 "
    "describes that provision as STND.DFLT 1.6 reads it, and so follows the amendment of STND.DFLT in the same "
    f"rounds (register entry R1.6). Ruling D1 of {F.RECORD}; register entries R6.2 (CL8) and R1.6 (CC13) of "
    f"review-records/deep-review-2026-10-28/register.md; decisions 6 and 19 of {REC}." + F.AUTHOR)


def apply_deps(root: Path, at: str) -> None:
    root = Path(root)
    (root / "STND/DEPS/13.md").write_text(B.provision_text("STND.DEPS", DEPS_NEW, "adopted", F.DATE),
                                          encoding="utf-8")
    F.check_fields(root, ["STND.DEPS.13"])
    replace_text(root, "STND/DEPS/_doc.md", DEPS_DOC)
    row = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {DEPS_READING}. |"
    F.finish(root, "STND/DEPS", "STND.DEPS", "1.1", "1.2", row, DEPS_RATIONALE, at)
