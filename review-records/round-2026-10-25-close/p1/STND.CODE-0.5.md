# Coding standard (STND.CODE) 1.2

Adopted by The Custodian as revision 1.0 in ledger entry 92 (2026-10-20); revised to 1.1 in entry 102 (2026-10-23) and 1.2 in entry 148 (2026-10-25). This reading copy is composed from the per-provision files in STND/CODE/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the coding practice that applies to source in every language, hardware descriptions included, as outcomes that a tool or a reviewer decides from the source, its repository configuration, and its record of checks. It adds to DSGN, SIMPL, INTPR, REPRO, VV, QA, PRIME.2, and PRIME.4 only what makes their outcomes checkable at each change. The language standards of LVL2 add the conventions of each language, and the form that its constructs give an outcome of this standard. Beside structure, checking, tests, and source, it states the responses to a failure that PRIME.4 lists, the declarations that keep a returned failure from being ignored, and the checks that no setting or definition removes (STND.CODE.14, STND.CODE.15, and STND.CODE.16), and recommends against an assumption of finite values in code that holds such a check (STND.CODE.21). For the code that a release of work of CSQ1 or CSQ0 delivers or runs to produce a reported result, it asks for conformance to the high-assurance coding standard that the work adopts, claims of that conformance limited to what was checked, an edition that the standard covers and the toolchain is validated for, and recorded deviations (STND.CODE.17, STND.CODE.18, STND.CODE.19, and STND.CODE.20). STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, and STND.CODE.16 instantiate PRIME.4, and STND.CODE.18 instantiates PRIME.2, so these six are binding and apply at every class; every other provision is a default (GOV.19) and a recommendation, which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7, PRIN.10). No provision names a language, tool, or method (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Safety-related component has the meaning that STND.CLASS gives it.

| Term | Definition |
| --- | --- |
| Repository configuration | The versioned files of the work that set how its tools build, check, format, and test it, apart from its governance. |
| Static check | A check of source or of a build that the means of the work make without running the work. |
| Execution setting | An option, flag, or variable of a compiler, interpreter, build, or run that changes which code executes. |
| Untrusted input | Data that reaches the work from outside its own code, the arguments of each function of its interface for outside use included, other than data from a source that the threat model of the project records as trusted. The interface for outside use of the work is each function that its documentation or its repository configuration names for use by code outside the work, together with each function that the standard of the language of that function places in its public interface. A function, in this term, is a function, procedure, subroutine, method, or other unit of code that a call enters. |
| High-assurance code | The code of the work that a release of work of CSQ1 or CSQ0 delivers, or runs to produce a reported result, each file that such code includes or imports included. Tests, development tools, and external code that the work incorporates are not high-assurance code. |
| High-assurance coding standard | A coding standard for a language of the work written for safety-related or mission-critical software, published or of the work's own making, with a procedure for recording deviations from its rules, its own or one that the decision record adopting it sets. |

## Notes

Each default provision asks for the cheapest evidence that keeps an outcome of LVL0 from failing silently. A tool that looks for cycles at each change keeps DSGN.7 true as the code grows (STND.CODE.1). Inputs that change between runs, the source of randomness and the run settings included, arrive through the interface, so that DSGN.14, DSGN.16, and DSGN.17 are visible at the call; a named constant, a hardware parameter fixed at synthesis, and a fixed configuration of a constrained target are not such inputs (STND.CODE.2). A contract stated at the declaration, or a citation of the one place that declares its units and conventions, puts DSGN.1 and INTPR.4 where every reader of the interface passes (STND.CODE.3).

The repository configuration names the static checks that the languages of the work offer, and each change passes them; a finding left in place is suppressed where it occurs, with its reason, so that the reason is the decision record of REPRO.7 (STND.CODE.4). A suppression records an accepted finding; it is not a way to pass a check (PRIME.2, AGENT.47). An agent that weakens a check or a setting in the change that the check judges records the two apart (AGENT.5) and states the weakening in its work report (AGENT.47). A layout that a named tool produces and confirms costs the reviewer nothing (STND.CODE.5).

STND.CODE.6 and STND.CODE.7 rest on PRIME.4 and bind at every class, CSQ4 included, a tightening of PRIME.4 at the cost of one look at one location (PRIME.15). A check of untrusted input that an execution setting removes, as an assertion compiled out of an optimized build is, lets invalid input pass silently in the builds that run in production. A failure of a kind that PRIME.4 lists is never discarded (STND.CODE.7). Another failure that code discards carries, at that location, the reason the results stay correct, which a reviewer checks (STND.CODE.12, a default). HW.8 and HDES.14 add the responses that hardware asks for.

Untrusted input. The term is defined here once, and the language standards import it (GOV.31). The arguments of a function of the interface for outside use come from code that the work does not see, so they are untrusted unless the threat model of GUARD.16 records their source as trusted, and the check that STND.CODE.6 governs is at the entry of that function. The clause on the standard of the language keeps the public interfaces that STND.PY, STND.JL, STND.RUST, and STND.FTN define by the constructs of their languages. The clause on the documentation and the repository configuration widens each of them by the functions that those name and the language standard does not place: in Python, a documented function outside library code or with a leading underscore; in Julia, a documented function that the package does not declare public; in Rust, a documented function of a crate that is not a library; in Fortran, a documented external procedure. Through STND.CODE.6, the term also reaches the documented functions of C, C++, Lean, and hardware descriptions. In C and C++, an assertion on an argument of such a function is a check that a setting removes, and so a form that STND.CODE.6 excludes. A Lean function whose precondition a proof establishes carries no run-time check, and STND.CODE.6 constrains only the checks that code makes, so the reach adds nothing there. In a hardware description, the ports of the top-level design carry data from outside the work's own code under the first clause, and a function or task of the description is reached only where the documentation names it for outside use. The reach constrains only the form of a check that the code makes and adds no check: PRIME.4 already excludes the silent continuation of invalid input, and DSGN.2 already asks for its check where it enters, so the cost is the wording of an existing check as a test with its response (GOV.11). The custodian's ruling of 2026-10-23 on the reach was made for STND.PY and STND.JL, and the ratification of 2026-10-24 extended it to STND.RUST and STND.FTN; no ruling yet covers the widening by documentation, or the reach in C, C++, Lean, and hardware descriptions.

Responses. STND.CODE.14 lists the responses that PRIME.4 admits, together with the pass of the condition to a caller, in its result, in an argument that the caller passes to receive it, or by a mechanism of its language that propagates it, which STND.CODE.7 keeps from discarding it and which STND.CODE.14 binds in turn. A condition that a mechanism of the language carries past every caller ends the program; no provision of this standard asks that end to carry a diagnosis, PRIME.4 states that outcome, and STND.RUST.13, STND.PY.32, and STND.CXX.32 give the forms of their languages for a panic hook, an exception hook, and a terminate handler, with STND.CXX.33 the default for a C++ program that installs no handler. A status argument, the form of STND.FTN.29, is an argument that the caller passes to receive the condition. A Rust panic propagates the condition under the unwinding strategy and halts under the aborting one, so it is a response under either. Each language standard gives the forms of its language: STND.PY.22, STND.JL.15, STND.RUST.13, STND.FTN.29, and STND.LEAN.25 name them, the status argument of Fortran and the error of a Lean monad among them. Where a language standard adds to them, its sentences stand as ruled or adopted and tighten what counts as a visible degradation or a diagnosis in its language: the warning categories and the logger of STND.PY.22, the levels of the logging macros of STND.JL.15, the panic hook of STND.RUST.13, the exception hook of STND.PY.32, the report through errno that STND.STDC.2 excludes, and the terminate handler of STND.CXX.32. In a hardware description, the condition passes to the caller as a status at the interface, the form that HDES.14 asks for saturation and overflow. STND.CODE.14 asks only the responses that PRIME.4 already requires, with the pass to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism of its language that propagates it, the forms that the first sentences of those provisions name, and so raises no floor in any language (GOV.11); the custodian's rulings of 2026-10-23 that the same list raises no floor were made for C++, Python, and Julia, and the argument for the other languages is the one given here.

Ignored results. STND.CODE.15 asks one declaration for each function that returns a listed failure, in a language or toolchain that provides a form of declaration for one function, or for the type of its result, under which a call that ignores the result is diagnosed. A rule of a static check that reports every ignored result, whatever the declaration, is not such a form, because it is not a declaration of the function; this reading lowers the reach that STND.RUST 1.0 and the C reading of STND.STDC 1.0 gave the outcome, which accepted any compiler or static check that diagnoses an ignored value; in Rust the must_use attribute is the form of the declaration. The nodiscard attribute of C and C++, the equivalent attribute of a compiler, and the must_use attribute of Rust are such forms; on the type of the result, the attribute also covers indirect calls (unverified for each compiler). The corpus records no such form for Python, Julia, Fortran, Lean, or SystemVerilog (unverified for each toolchain), where the provision asks nothing until the means of the work include one, and STND.CODE.7 still forbids discarding a listed failure. The cost is one declaration for each such function, without which a listed failure that a function returns passes silently where a caller ignores it; where no form exists, the cost is nothing, so the provision raises no floor (GOV.11). The custodian's ruling of 2026-10-23 on this outcome was made for C++; STND.STDC and STND.RUST, adopted on 2026-10-24, condition it on a compiler or static check among the means of the work, and this provision conditions it on a form of declaration that the language or those means provide.

Required checks. The first sentence of STND.CODE.16 carries STND.CODE.6 to the checks that CPS.5 and CPS.9 require of work that commands hardware, where those provisions apply to the work at its class: a check that an execution setting removes is absent from each build and each run under that setting, where CPS.5 or CPS.9 still requires it. Its second sentence reaches a check that a definition that the source gives to conditional compilation turns off, which is not an execution setting and which STND.CODE.6 therefore does not reach. The assert macro of C expands to an expression that does nothing where NDEBUG is defined at the point at which its header is included, whether an option of the compiler or a line of the source before that inclusion defines it, and is defined again at each inclusion of the header (research note round-addenda/a2-language-facts.md, which cites the working draft of C, 7.2); the same for the header of C++ is unverified. A definition after the last inclusion turns nothing off and is outside the second sentence. A check under a directive of conditional compilation on a macro that the source defines is removed in the same way; the two sentences exclude these forms for a check of untrusted input and for a check that CPS.5 or CPS.9 requires. In Python and Julia, the first sentence extends to the checks of CPS.5 and CPS.9 the forms that STND.PY.25 and STND.JL.13 exclude for untrusted input: an assert statement, which the optimizing mode of the interpreter removes, and in Julia `@assert` and a `@boundscheck` block. The second sentence adds nothing in Python, which has no conditional compilation, and a check under an ordinary condition on a constant of the source is not reached; in Julia it reaches a check under `@static if` on a constant that the source defines. In Rust, a condition of compilation is set by the build configuration, an execution setting that STND.CODE.6 and STND.RUST.15 already reach, so the sentence adds nothing there. In Fortran, standard source has no conditional compilation (unverified), and the sentence reaches only source that a preprocessor reads, where a definition in the file guards a check. In SystemVerilog, it reaches a check under a conditional compilation directive on a macro that the source defines. Lean has no conditional compilation of its own (unverified), so the sentence adds nothing there. The sentence reaches only a build that holds the code the check guards, so code compiled out together with its check leaves no input unchecked and is outside it. Each sentence keeps in every build a check that STND.CODE.6, CPS.5, or CPS.9 already requires, at the cost of the form of that check, so neither raises the floor in any language (GOV.11). The two sentences have one subject, the form of a required check, and apply together. The custodian's ruling of 2026-10-23 on the first sentence was made for C++, and the ratification of 2026-10-24 accepted it for C and for Rust (STND.RUST.15); the argument for the other languages, and for the second sentence in every language, is the one given here.

Finite values. An execution setting or an annotation that, by the documentation of its compiler, lets the compiler assume finite floating-point values licenses the deletion of tests for not-a-number and infinite values. The documentation of two compilers states the assumption and names no test that it deletes (the same research note), so whether a given compiler deletes them is unverified, and the Notes of STND.FTN record the hazard as unverified for Fortran compilers. STND.CODE.21 is therefore a default in every language. The binding form of its first sentence stays with the languages for which it was ruled or ratified: STND.CXX.18 for C++ and STND.STDC.40 for C, while STND.CODE.21 holds it as a default for Fortran, as for every other language without a binding form. In Julia, the annotation is the `@fastmath` macro and the setting a mode of the compiler; the Python language has neither, and a compiler of Python code that offers such an option is reached by the first sentence. Where a setting does remove the check, STND.CODE.6 or the first sentence of STND.CODE.16 already excludes it, in every language. STND.CODE.21 instantiates the check of DSGN.2 where untrusted data enters, rests on no row of STND.CLASS.10, and applies from CSQ3.

High assurance. High-assurance coding standards restrict a language to a subset that analyzers are able to check, commonly by limiting dynamic allocation, recursion, unbounded loops, the mechanisms of exceptions, casts, and the preprocessor, and each sets a procedure for recording deviations. Published ones exist for C and C++; for a language without one, the term admits a standard of the work's own making. The provisions name no standard, because standards and their editions change, and accept any that a decision record of the work adopts, the custodian's ruling for C++. Restrictions of this kind make the proof or exhaustive checking of the CSQ0 row of STND.CLASS.10 and the bounds of HW.20 and HW.EMBED.3 attainable in every language. Conformance reduces undefined and unspecified behavior by a mechanical check (DSGN.3); it is not evidence that a result is correct (VV.1). STND.CODE.18 keeps a claim of conformance to what was checked, by an analyzer, by a reviewer, or by both, so that no claim rests on a check that did not run (PRIME.2).

The custodian ruled for C++ that for high assurance the validation status is more important than the language standard. STND.CODE.19 therefore takes an edition that the adopted standard covers and for which the toolchain holds the validation or qualification that the work requires, which is often older than the newest, and admits one later feature at a time by decision record. The edition of a language is a revision of its definition, or, for a language that its implementation defines, a release of that implementation. For a hardware description, the toolchain includes the tools that synthesize and simulate it. STND.CXX.2 names STND.CODE.19 among the editions that it yields to; another language standard that asks for the newest edition yields to it where its own text says so. A check that runs the tests on a newest release without blocking a change, as STND.RUST.1 and STND.JL.3 ask, builds no delivered code, and so is outside STND.CODE.19. High-assurance code is all the delivered code of CSQ1 and CSQ0 work, so that no code of CSQ0 work gets less than code of CSQ1 work, and the provisions are required for the safety-related components of CSQ0 and recommended elsewhere. Code built into CSQ0 work is used at CSQ0 (GOV.14), so a file that a CSQ0 controller and a CSQ3 simulation share is high-assurance code; the human owner may record a less severe class for a component shown to be isolated (GOV.13). External code that high-assurance code incorporates is governed by STND.DEPS and DSGN.5, with the contract and the wrapper that isolates it recorded. An analyzer is installed only under a recorded authorization (PRIME.7) and is listed in the tool record of STND.DEPS.9. An analysis too costly for each change is deferred to the release under RSRC.12, recorded in the unit record as STND.WPROC.9 provides. The deviation marker of STND.CODE.20 lets the release record of STND.WPROC.13 list each deviation by a search. A deviation is a decision record under REPRO.7, not a waiver, and code explains it by its technical reason (STND.DOCS.5).

STND.CODE.17 and STND.CODE.19 are defaults that apply from CSQ1 to high-assurance code, required for the safety-related components of work of CSQ0 and recommended for other high-assurance code; they tighten the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 applies at CSQ0 under DSGN.3, and VV.1, whose CSQ0 row the restricted subset serves, and those rows hold in every language alike. STND.CODE.20 asks the record of each deviation wherever such a standard is adopted (REPRO.7). A project replaces each of the three by a recorded decision with an alternative that meets the same outcome, so they block no work in a language for which no standard is published. These onsets depart from STND.CLASS.10. STND.CODE.17 and STND.CODE.19 apply from CSQ1, earlier than the CSQ0 rows of DSGN.3 and VV.1 that they tighten, and STND.CODE.20 applies wherever a high-assurance coding standard is adopted, CSQ4 included, though STND.CLASS.10 lets work of CSQ4 omit an obligation above the floor. The custodian ratified these onsets for C++ with STND.CXX.28, STND.CXX.30, and STND.CXX.31, and for C through STND.STDC.1. For the other languages the argument is this: the onset of CSQ1 follows the term High-assurance code, which starts at CSQ1 in every language because reliance by a party outside the project starts there; each of the three is a default, a tightening above the floor that a recorded decision replaces (PRIME.15, GOV.19), so none raises the floor; and the record of STND.CODE.20 reaches work of CSQ4 only where that work has chosen to adopt a high-assurance coding standard, at the cost of one record for each deviation from it. The three sentences of STND.CODE.19 concern one edition of one body of code and apply together. The custodian's rulings on high assurance were made for C++, and STND.STDC applied them to C on 2026-10-24; for the other languages the argument is the one just given. STND.CODE.18 adds to PRIME.2 only the naming of the means that checked a claim of conformance, at the cost of one sentence for each claim, and concerns claims and not the constructs of a language, so the argument holds in each language; it reaches only high-assurance code, which is never below CSQ1. The custodian ruled at the ratification of 2026-10-23 that the same provision raises no floor for C++ (GOV.11, PRIN.10).

A test added for each fixed defect (STND.CODE.8) is a regression guard unless its reference is independent of the code it judges (VV.7); either way it lets VV.8 detect the defect's return. A test whose verdict changes between runs of the same revision, seeds included, gives no evidence, and a test whose reference is local needs no network access, which would otherwise call for an authorization (PRIME.7) (STND.CODE.9). A constant that a measurement, a published reference, or a recorded choice fixes carries its unit, source, and revision once (STND.CODE.10), while a literal of a formula, a loop bound, and an index origin are not such constants; a measured or calibrated constant is also versioned data under REPRO.6, whose calibration states the conditions and the interval over which it holds (MEAS.5). Code disabled by turning it into a comment is neither active nor retired; the source history keeps it (STND.CODE.11, SIMPL.8). The custodian directs that code be laid out by the logical grouping of its instructions, so that a reader follows a computation step by step: a blank line ends a step, and a comment names a step whose purpose its code does not show (STND.CODE.13, INTPR.1).

Under STND.CLASS.10, each default provision other than STND.CODE.17, STND.CODE.19, STND.CODE.20, and STND.CODE.21 instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or QA and applies from CSQ3; work of CSQ4 omits it. The onsets of STND.CODE.17, STND.CODE.19, STND.CODE.20, and STND.CODE.21 are stated above. No default provision raises the floor (GOV.11). Hardware descriptions are code under this standard; HDES.6 governs what their verification shows.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES | Hardware design |
| HW | Execution hardware |
| HW.EMBED | Embedded controllers |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.FTN | Fortran standard |
| STND.JL | Julia standard |
| STND.LEAN | Lean standard |
| STND.PY | Python standard |
| STND.RUST | Rust standard |
| STND.STDC | C standard |
| STND.WPROC | Work process standard |
| VV | Correctness |

## Provisions

### Structure

#### STND.CODE.1 Mechanical cycle check

Default. Instantiates DSGN.7.

At each change to the dependency structure of the work's components, a tool SHOULD check that structure for cycles (DSGN.7).

#### STND.CODE.2 Inputs through interfaces

Default. Instantiates DSGN.14, DSGN.16, DSGN.17.

Each function that computes a result SHOULD receive through its interface each input that affects that result and changes between runs, its source of randomness and its run settings included (DSGN.14, DSGN.16, DSGN.17).

#### STND.CODE.3 Contracts at declarations

Default. Instantiates DSGN.1, INTPR.4.

Each interface that another component uses SHOULD state, at its declaration, what it requires, guarantees, and preserves, with the units and conventions of the data it exchanges or a citation of the one place that declares them (DSGN.1, INTPR.4).

### Checking

#### STND.CODE.4 Static checks per change

Default. Instantiates DSGN.3, REPRO.7.

Where the tools of a language of the work offer static checking of types, units, or contracts, the repository configuration SHOULD name that checking (DSGN.3). Each change SHOULD pass the static checks that the repository configuration names, at the settings that it records (DSGN.3). Each finding of those checks that a change does not resolve SHOULD be suppressed at its location with its reason (REPRO.7).

#### STND.CODE.5 Mechanical source layout

Default. Instantiates INTPR.1.

The repository configuration SHOULD name, for each language of the work, a tool that produces the layout of its source (INTPR.1). At each change, each such tool SHOULD confirm that the source has the layout that it produces (INTPR.1).

### Failures

#### STND.CODE.6 Unremovable input checks

Binding. Instantiates PRIME.4, DSGN.2.

A check that rejects invalid untrusted input where that input enters SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2).

#### STND.CODE.7 Discarded failures

Binding. Instantiates PRIME.4.

Code SHALL NOT discard a failure of a kind that PRIME.4 lists (PRIME.4).

#### STND.CODE.12 Reasoned discards

Default. Instantiates REPRO.7.

Where code discards a failure that it detects or receives and that PRIME.4 does not list, it SHOULD state at that location why discarding it leaves the results of the work correct (REPRO.7).

#### STND.CODE.14 Responses to listed failures

Binding. Instantiates PRIME.4.

Where code detects a condition that PRIME.4 lists, it SHALL halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, degrade visibly with a diagnosis, or pass the condition to its caller, in its result, in an argument that the caller passes to receive it, or by a mechanism of its language, an exception among them, that propagates the condition to the caller (PRIME.4).

#### STND.CODE.15 Ignored failure results diagnosed

Binding. Instantiates PRIME.4.

Where the language, or a compiler or a static check among the means of the work, provides a form of declaration for a function, or for the type of its result, under which each call that ignores that result is diagnosed, each function of the work that returns a failure of a kind that PRIME.4 lists SHALL be declared in such a form (PRIME.4).

#### STND.CODE.16 Required checks in every build

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9.

Where CPS.5 or CPS.9 applies to the work, each check that it requires, with its response, SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2, CPS.5, CPS.9). Where a build holds the code that a check of STND.CODE.6 or of the first sentence of this provision guards, that check SHALL NOT be turned off in that build by a definition that the source of the work gives to conditional compilation (PRIME.4, DSGN.2).

#### STND.CODE.21 Finite-value assumptions near checks

Default. Instantiates DSGN.2.

Code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs SHOULD NOT be compiled under an execution setting that, by the documentation of its compiler, lets the compiler assume that floating-point values are finite (DSGN.2). Such code SHOULD NOT carry an annotation in its source that, by its documentation, lets the compiler assume that floating-point values are finite in the code that holds the check (DSGN.2).

### Tests

#### STND.CODE.8 Regression test per fix

Default. Instantiates VV.8, QA.4.

Each fix of a defect in code SHOULD add a test that fails on the revision before the fix and passes on the revision after it (VV.8, QA.4).

#### STND.CODE.9 Repeatable test verdicts

Default. Instantiates REPRO.3, REPRO.1.

Each test SHOULD give the same verdict on every run against the same revision and recorded inputs, its random seeds included (REPRO.3). Where a test's reference is inside the provisioned environment, the test SHOULD NOT reach outside it (REPRO.1, REPRO.3).

### Source

#### STND.CODE.10 Named domain constants

Default. Instantiates INTPR.4, REPRO.6.

Each numeric constant that a measurement, a published reference, or a recorded choice fixes, and on which a reported result depends, SHOULD be defined once, by a name, with its unit, its source, and its revision, and used by that name (INTPR.4, REPRO.6).

#### STND.CODE.11 Disabled code in comments

Default. Instantiates SIMPL.8.

Source SHOULD NOT hold code disabled by its conversion into a comment (SIMPL.8).

#### STND.CODE.13 Statements grouped by step

Default. Instantiates INTPR.1.

Within the body of a function, a procedure, or a process, statements SHOULD be grouped into blocks that each carry out one step of the computation, with one blank line between consecutive blocks (INTPR.1). Other than a blank line that a tool of STND.CODE.5 inserts, a block SHOULD carry no blank line inside it (INTPR.1). Where the step that a block carries out is not evident from its code, a comment at the head of the block SHOULD state it (INTPR.1).

### High assurance

#### STND.CODE.17 Adopted high-assurance coding standard

Default. Instantiates DSGN.3, REPRO.7.

The high-assurance code of each safety-related component of work of CSQ0 SHALL conform to a high-assurance coding standard for its language that a decision record of the work adopts, the record naming the standard, its revision, and its deviation procedure (DSGN.3, REPRO.7). Other high-assurance code SHOULD conform to a high-assurance coding standard for its language that a decision record of the work so adopts (DSGN.3, REPRO.7).

#### STND.CODE.18 High-assurance conformance claims

Binding. Instantiates PRIME.2.

Each claim that high-assurance code conforms to its high-assurance coding standard SHALL state each means by which that conformance was checked and the rules that each means covered (PRIME.2). A claim of conformance SHALL NOT extend beyond the rules that those means checked (PRIME.2).

#### STND.CODE.19 High-assurance language edition

Default. Instantiates DSGN.3, VV.1, REPRO.7.

Other than for a feature that a decision record admits under this provision, the high-assurance code of each safety-related component of work of CSQ0 SHALL be compiled or run at an edition of its language that its high-assurance coding standard covers, and for which each tool that compiles, synthesizes, interprets, simulates, or runs that code, and each library implementation that the code uses, has the validation or qualification that the decision record of STND.CODE.17 states the work requires (DSGN.3, VV.1). Other high-assurance code SHOULD be compiled or run at such an edition (DSGN.3). Where a decision record states, for one feature of a later edition, why the high-assurance coding standard and the validation of the toolchain still give the evidence on which the work relies, high-assurance code MAY use that feature and no other feature of that edition (REPRO.7).

#### STND.CODE.20 Recorded high-assurance deviations

Default. Instantiates REPRO.7.

Each deviation from a rule of the high-assurance coding standard of STND.CODE.17 SHALL be recorded as the deviation procedure of that standard requires, at its location under one marker that the repository configuration names or in a decision record that the location cites, with the identifier of the rule, the reason, and the evidence that the code stays correct (REPRO.7).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.1 | 2026-10-23 | Minor amendment (GOV.41): new STND.CODE.13 groups the statements of each body into blocks, one step of the computation each, set apart by one blank line and headed by a comment where the step is not evident; the custodian's grouping direction, first given for Python, applies to every language. |
| 1.2 | 2026-10-25 | Minor amendment (GOV.41): new STND.CODE.14 to STND.CODE.21 state for every language the shared rules that STND.CXX held for C++ and STND.STDC applied to C in its C reading: STND.CODE.14 (binding, PRIME.4) the responses to a failure that PRIME.4 lists, with the pass to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism of its language that propagates it, from STND.CXX.16; STND.CODE.15 (binding, PRIME.4) a declaration under which an ignored returned failure is diagnosed, from STND.CXX.17, conditioned on a language or toolchain that provides one; STND.CODE.16 (binding, PRIME.4) the checks of CPS.5 and CPS.9 kept from removal by an execution setting, from the first sentence of STND.CXX.18, and a check of STND.CODE.6 not turned off, in a build that holds the code it guards, by a definition that the source gives to conditional compilation, which reaches a definition of NDEBUG in C and C++ source before the inclusion of the header of the assert macro; STND.CODE.21 (default, from CSQ3) no assumption of finite floating-point values, by an execution setting or an annotation, in code that holds a check of a floating-point value, the outcome of the second sentence of STND.CXX.18, whose binding form stays in STND.CXX.18 for C++; STND.CODE.17 to STND.CODE.20 (STND.CODE.18 binding, PRIME.2; the others defaults from CSQ1) the high-assurance coding standard, conformance claims, edition, and deviations, from STND.CXX.28 to STND.CXX.31, STND.CODE.19 naming the tools that synthesize and simulate a hardware description; Terms define Untrusted input once, with the interface for outside use that the documentation, the repository configuration, or the standard of the language names, and with function read to include a procedure, subroutine, or method, and High-assurance code and High-assurance coding standard for every language; STND.CODE.6 uses the term Untrusted input in place of untrusted data; the Purpose lists the new provisions and the binding ones; the Notes give the reasons, the reach of the term and of STND.CODE.16 in each language, the floor argument for each binding provision in each language, and the class onsets, and cite HDES.14, HDES.6, and MEAS.5 where they named HDES and MEAS; References lists CPS, GUARD, HDES, MEAS, and the standards that the Notes cite. |
