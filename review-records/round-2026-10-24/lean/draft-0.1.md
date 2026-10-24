# Lean standard (STND.LEAN) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 118 (2026-10-24). This reading copy is composed from the per-provision files in STND/LEAN/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice of work in Lean, both as a proof assistant whose checked proofs the work relies on as evidence and as a programming language. It adds to VV, DSGN, AGENT, STND.CODE, STND.DEPS, STND.DOCS, and STND.VVUQ only what Lean makes necessary. It covers the toolchain, the Lean packages, and their upgrades (STND.LEAN.1, STND.LEAN.2, and STND.LEAN.3); the record of a claim that rests on a proof, the status of a proof, the axiom declarations of each relied-on theorem, and statements held for a later proof (STND.LEAN.4 to STND.LEAN.8); trusted statements, held apart from their proofs, compared after the build, reviewed, and shown not to be vacuous (STND.LEAN.9 to STND.LEAN.13); native evaluation and the checkers of a proof (STND.LEAN.14, STND.LEAN.15, and STND.LEAN.16); definitions and the code that runs (STND.LEAN.17 to STND.LEAN.20); proofs from untrusted authors and their review (STND.LEAN.21 and STND.LEAN.22); arithmetic (STND.LEAN.23 and STND.LEAN.24); Lean programs (STND.LEAN.25, STND.LEAN.26, and STND.LEAN.27); and the maintenance of proofs (STND.LEAN.28 to STND.LEAN.31). The Notes state how a Lean proof meets the rows of STND.CLASS.10 that ask for proof at CSQ0, and the statement of correspondence that STND.CONC.28 asks of a model.

STND.LEAN.5 instantiates PRIME.2, so it is binding and applies at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard names the constructs of the Lean language and no release of its toolchain, library, checker, tactic, option, or other tool (GOV.18); the repository configuration of each work selects them.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration and Execution setting have the meanings that STND.CODE gives them; Advisory and Integrity digest have the meanings that STND.DEPS gives them; Safety-related component has the meaning that STND.CLASS gives it.

| Term | Definition |
| --- | --- |
| Lean | The functional programming language and proof assistant of that name in its fourth major form, whose source files carry the extension `.lean`, at each release of its toolchain. |
| Toolchain | The compiler, kernel, build tool, and core library of Lean of one release. |
| Lean package | A unit of Lean source that the build tool of the toolchain fetches and builds as a dependency of the work, at the revision that a manifest gives. |
| Lean environment | The declarations that Lean holds after it elaborates a module and the modules that the module imports. |
| Kernel | The part of the toolchain that type-checks each declaration before a Lean environment admits it. |
| Checker | A program that checks the declarations of a Lean environment against the rules of the type theory of Lean. The kernel is a checker. |
| Independent checker | A checker whose source was written apart from the source of the kernel, and not by translation of that source, and that runs on no part of the runtime of the toolchain. |
| Relied-on theorem | A theorem of a Lean environment on whose proof a claim of correctness of the work rests as evidence. |
| Trusted statement | Of a relied-on theorem: the proposition that the theorem is required to prove, written in Lean source apart from its proof. It is the acceptance criterion of that proof. |
| Axiom declaration | A declaration that adds to a Lean environment a constant of a stated type without a definition or a proof, whether the `axiom` command of the source or the toolchain makes it. |
| Logical axiom declaration | An axiom declaration that the core library of Lean makes as part of the logic of Lean, other than one by which a placeholder or native evaluation enters a Lean environment. |
| Placeholder | A term or a tactic that closes a goal of a proof without proving it, and that the toolchain records by an axiom declaration. |
| Axiom inventory | Of a theorem: the axiom declarations on which its type or its proof depends, directly or through other declarations, as the toolchain reports them from the Lean environment. |
| Accepted axiom list | The list, in the repository configuration, of the axiom declarations that the axiom inventory of a relied-on theorem is admitted to hold. |
| Native evaluation | Evaluation of a term by code that the compiler of the toolchain produced, whose result a Lean environment admits in a proof through an axiom declaration. |
| Total definition | A definition without the `partial` or `unsafe` modifier, whose recursion, where it recurses, is structural or well-founded. |
| Replaced implementation | Code that runs in place of the code compiled from the body of a definition, by the `implemented_by` or `extern` attribute of that definition. |
| Lean model | Lean definitions that state the behavior of code that runs, written apart from that code. |
| Untrusted author | An author of Lean source that the work builds before a review of that source, among them a language model, a tool that searches for or generates proofs, and an actor whom the threat model of the project does not trust. |

## Notes

Direction and sources. Lean is one of the standards in the custodian's order of 2026-10-24, and the custodian's standing directions ask that each standard be agnostic of platform, compiler, vendor, implementation, framework, and tool, and timeless. The provisions therefore name the constructs of the language, its keywords, modifiers, and attributes, and no release of the toolchain, library, checker, tactic, option, or command; a Note names one only to show a hazard, and the names of tactics, axioms, options, and checkers change between releases (research/lean-notes/l1-lean4.md, "Timeless versus moving"). The research note, l1 below, read its sources as extracts that a retrieval tool wrote and ran no Lean; its central source is the chapter of the Lean reference manual on validating proofs (l1, S1). A fact that l1 does not support is marked unverified. The provisions rest on what l1 finds timeless and consistent with proof assistants of other families: a checked proof is relative to its statement, its axioms, and its checker, and the adequacy of the statement is a separate review; placeholders and axioms are listed and not trusted by default; evaluation by compiled code is a lower level of trust than checking by the kernel; a model and the code that runs are joined by a stated link of a stated strength; checkers that derive from one another share defects; proofs that a machine generates are untrusted input, checked against a trusted statement; and inputs are pinned and checked again after each change.

What a checked proof establishes. A proof that the kernel accepts establishes that a term of the stated type exists, relative to the axiom declarations that the proof uses and to the soundness of the logic, of the kernel, and of the runtime and host that ran the check. It establishes nothing about whether the statement means what the claim needs, whether the code that runs computes what the definitions compute, or whether the check covered the dependencies of the theorem (l1, practices 1, 2, and 4). Native evaluation adds the compiler and its runtime to that base (l1, S1, S2). VV.1 asks that evidence state its assumptions and show them met; the record of STND.LEAN.4 states them for a Lean proof, and its rows are the items that l1 gives a reviewer (l1, practice 22). The statement in words is work documentation, which defines its terms of art and states each point specifically, as STND.DOCS.2 and STND.DOCS.9 ask, and keeps one name for each concept, as STND.DOCS.12 asks. The record keeps verification and validation apart, as VV.5 asks: the proof verifies the code against the trusted statement, and the review of STND.LEAN.11 validates the trusted statement against the claim (VV.4). The editor's mark that the current theorem checked appears even where a dependency holds a placeholder, so the status of a proof rests on a build of every declaration on which it depends (l1, S1). A report that a theorem is proved, where it rests on a placeholder or on a check that did not build its dependencies, claims a check that was not run, which PRIME.2 forbids at every class; STND.LEAN.5 states that in the terms of Lean, at the cost of its wording, and AGENT.4 holds the same of an agent's statement that a check passes. STND.LEAN.5 asks nothing that PRIME.2 does not already forbid, so it raises no floor (GOV.11), which the custodian decides.

Axioms and placeholders. An Axiom of the Lexicon is an assumption that the human owner declares, and VV.9 and GOV.50 reserve its declaration to the human owner; an axiom declaration of Lean states such an Axiom only where the human owner declared it. The logical axiom declarations, at present propositional extensionality, the axiom of choice, and the soundness of quotients, belong to the logic of Lean and are accepted across its community (l1, S2); they enter the record of STND.LEAN.4 as assumptions of the evidence under VV.1, as the soundness of the kernel does, and not as Axioms of the work, so STND.LEAN.7 asks no decision of the human owner for them, and a project that wants a narrower logic removes them from its accepted axiom list. Lean does not check that a new axiom declaration is consistent, and the axiom declaration by which a placeholder enters a Lean environment proves every proposition (l1, S2). The listing of the axioms of a declaration, at present the `#print axioms` command, gives the axiom inventory, and native evaluation makes an axiom declaration for each use whose statement is open to audit (l1, S1, S2). STND.LEAN.6 rests on a list in the repository configuration, so that each name outside it is a finding, because the names that native evaluation uses have changed between releases (l1, S1). A proposition held for a later proof as a definition adds nothing that a later proof is able to use as a lemma, while a theorem that a placeholder proves does, and an audit of benchmarks recommends a form of that kind for unsolved statements (l1, S15) (STND.LEAN.8). Placeholders remain in work in progress; STND.LEAN.6 keeps them out of relied-on theorems, and the second sentence of STND.LEAN.8 out of each release.

Trusted statements. A statement that does not mean what the claim needs is the commonest failure that l1 found: one study found an error in about 40 percent of the formal statements of a public benchmark, most of them simplified relative to their intent, and an audit of five benchmarks separates statements weaker than intended from statements that mistranslate, which need opposite repairs (l1, S14, S15). Holding the trusted statement in files that hold no proof of the theorem, and comparing the proved type with it in a process apart from the build, defends against a proof file that redefines a definition, a notation, or an instance that the statement uses (l1, S1, practice 16) (STND.LEAN.9 and STND.LEAN.10). The definitions whose behavior a theorem verifies are code of the work, reviewed as code, and STND.LEAN.10 compares the theorem's type with a trusted statement that names them. The trusted statement is the acceptance criterion of its proof, so VV.3 already has a change of it after the proof begins made by a recorded decision that keeps the earlier statement, and AGENT.5 has an agent record such a change apart from the change that it judges; the second sentence of STND.LEAN.9 gives the form of those for Lean source. The hazards of the table of STND.LEAN.11 are the kinds that l1 lists (practice 9, S6a, S15): subtraction of natural numbers truncates at zero, division by zero gives zero, remainder by zero gives the dividend, an implicit variable that elaboration binds automatically turns a misspelled name into a new variable over which the statement quantifies, and local notation, instances, and coercions change what a symbol means. A study of autonomous research agents found agents that redefined operators by local notation so that theorems became trivial, past a filter that looked only for the keywords of axioms and placeholders (l1, S22, from a search summary). The setting of STND.LEAN.12, at present an option that turns off automatically bound implicit arguments, is one that the audit recommends (l1, S15). A statement whose hypotheses do not hold together is vacuous evidence, which PRIME.2 forbids, and STND.LEAN.13 gives the means of showing that a statement is not vacuous: an instance of its hypotheses, and a proof that an implementation that the claim excludes lacks the property, so that the statement is shown to tell a correct implementation from a wrong one (l1, practice 10). STND.LEAN.13 is a default, because the outcome that it serves binds already through PRIME.2.

Evaluation and checkers. The decision tactics that evaluate by compiled code, at present `native_decide` and the decision procedure for bit vectors, admit their results through an axiom declaration, so the compiler and its runtime enter the trusted base, and a checker other than the toolchain's runtime is unable to check those results (l1, S1, S2, S9). A certificate that an external solver produces adds nothing to the trusted base where the kernel replays it, and adds the compiler where compiled code checks it (l1, S9). STND.LEAN.14 admits native evaluation with a record, because a check by the kernel of a large closed term is at times infeasible within the limits of recursion and time (l1, S23), and STND.LEAN.16 removes that latitude for safety-related components. l1 found no report of a disagreement between compiled code and the kernel on a closed term, and searched no issue tracker (unverified); the hazard rests on the absence of a verification of the compiler. The checks escalate in what they catch (l1, table of levels of check): the axiom inventory catches placeholders, project axioms, and native evaluation; a replay of the Lean environment in a fresh process catches tampering by meta-programs that ran during the build, but not a defect of the kernel, since the same kernel replays it; and a second checker of separate origin catches a defect present in one checker only. Meta-programs run arbitrary actions at build time and are able to add declarations that no checker saw, which is why STND.LEAN.15 puts its check in a process apart from the build (l1, S1, S3). A build that takes build products fetched from outside, as a downloaded cache of a large library supplies them, holds declarations that the local kernel did not check, by inference from l1 (S7) and unverified; the second sentence of STND.LEAN.15 covers them, and STND.DEPS.6 covers the integrity of what is fetched. Soundness defects of the kernel and its runtime have been found more than once: one by formal work on a second kernel, and others, fixed in recent releases or reported in an advisory, by external checking and by outside reporters; one bad proof was accepted by a second kernel as well as by the reference, and a checker derived from the source of the reference kernel mirrors its structure and is likely to share its defects (l1, S5, S18, S19, S20). The term Independent checker therefore excludes a checker translated from the kernel and a checker that runs on the runtime of the toolchain, which one runtime defect reached (l1, S18); STND.LEAN.4 records of each checker whether it is one, so that the agreement of two derived checkers is not read as two confirmations. A second kernel written in Lean checks the large mathematics library 20 to 50 percent slower than the reference (l1, S5), and an arena runs 29 checkers against suites of proofs to accept, proofs to reject, and corner cases (l1, S21); which of them is free of a given defect is what l1 leaves unverified. A defect fixed in a later release is the occasion of STND.LEAN.3, which is the form for a checker of the check of advisories that STND.DEPS.7 asks before each release; l1 has a proof from an untrusted author checked again on a toolchain whose checker defect is fixed (S20).

Definitions and the code that runs. A `partial` definition is opaque to the kernel, which requires only that its return type be inhabited, so no theorem states what it computes; an `unsafe` definition is outside the equational theory of Lean, and a declaration that refers to one is itself unsafe (l1, S4). Neither makes the logic inconsistent, and each cuts the link between what a theorem states and what runs (l1, practices 7 and 8) (STND.LEAN.17). In one industrial case, the need to show termination exposed a defect of non-termination in a validator (l1, S8). The `implemented_by` and `extern` attributes leave the definition for the kernel and run other code, and the reference manual counts their equivalence as part of the trusted code base (l1, S4, S6c) (STND.LEAN.18). The kernel itself computes its operations on natural numbers by an arbitrary-precision library without checking that they satisfy their defining equations, which the manual says could undermine soundness on a mismatch (l1, S5, S6a); that is part of the trusted base of every check, and not a replaced implementation of the work. A substitution whose equality with the definition the work proves, as an attribute of the compiler admits at present, is not a replaced implementation in the sense of the term (unverified: l1 does not describe that attribute). The links of the table of STND.LEAN.19 are the four of l1 (practice 11; S8, S12, S13); a program logic for the monadic programs of Lean is a means of proof within the first link, and the verification of code of another language against a semantics of that language in Lean falls under the third. In the industrial case of l1, the Lean model was about ten times smaller than the code, differential testing on millions of generated inputs found 21 defects in the implementation, and proof found 4 that testing was unlikely to find; the generators produced no malformed input at all (l1, S8). The code of a separate implementation is therefore verified by comparison with its Lean model, and STND.LEAN.20 asks that comparison at each change and records what its generator does not reach. That case's rule that no release is made unless the model, the proofs, and the tests are current is the condition of QA.10 that evidence be current for the released revision. STND.LEAN.19 is the statement of correspondence that STND.CONC.28 asks where the model of a protocol is a Lean model, and the Notes of STND.CONC still ask that such a model order accesses as the hardware model of HW.11 does.

Untrusted authors and agents. The reference manual counts un-reviewed machine-generated proofs among its malicious cases (l1, S1). Documented proofs that language models wrote passed a compile by local notation that redefined an operator, by a defect of a tactic that reported success without a declaration that passed the kernel, by added axioms, and by native evaluation; one prover reported nine patterns of compilable but invalid code, which a check that the statement was unchanged detected (l1, S11, S15, S22, S27, the last two from search summaries). The three sentences of STND.LEAN.21 are one protocol and are never applied apart: a statement fixed first and kept from the author, a verdict from a process that runs none of the author's code, and the exact source of that verdict identified; each leaves open a hazard that the others close. Where the source of an untrusted author runs during its own elaboration, GUARD.17 and the threat model of GUARD.16 govern where it runs. A machine-checked proof makes a human reading of the proof script unnecessary where the statement is trusted (l1, S29, practice 18), which STND.LEAN.22 permits; review of such a change then concerns the trusted statement, the definitions, the axiom inventory, and the record of the checks, and reads the script for its maintenance only. An agent that writes a proof is held by AGENT.2 to explain it in terms that a reviewer checks, by AGENT.3 to mark a claim that no check supports, by AGENT.4 to report a check only after a run of it, by AGENT.5 to record a change of a trusted statement apart from the proof that it judges, and by AGENT.47 to state each placeholder that it adds, each statement that it weakens, and each check that it disables; GOV.50 lets it propose an axiom and not declare one. AGENT.12 has a directing agent check a delegated proof against the acceptance criteria of the delegated unit, which for a proof are its trusted statement and the accepted axiom list. A language model that proposes to change a statement, a definition, or a library lemma that it did not write proposes a change to the specification, which AGENT.5 already separates.

Toolchain and upgrades. Build products of one toolchain do not serve another, the manifest of the build tool gives the exact revision of each Lean package and is part of the code of the package, the toolchain file names the toolchain, and an automatic update of the toolchain changes that file unless it is turned off (l1, S7); the last is the hazard of the third sentence of STND.LEAN.1. The three sentences of STND.LEAN.1 state one pin and apply together. The release notes of one recent release list renamed lemmas, a removed parameter, a simplification set changed so that it "shifts proving power in both directions", a changed reducibility, and a stricter kernel (l1, S18), so a change of the toolchain or of a Lean package is a change under VV.8 whose proofs are rebuilt and whose checks are repeated; STND.LEAN.2 is the form of STND.DEPS.5 for Lean. STND.DEPS.3 and STND.DEPS.4 govern the choice and the review of each revision; a Lean package that the work imports fixes the toolchain with which it builds, so the clause of STND.DEPS.3 on consistency with the rest of the computational environment sets the toolchain of a work that imports it. STND.DEPS.8 records the toolchain revision as an input of each result, and STND.LEAN.4 records the revision of each checker with the claim. Fixes of soundness defects arrive in point releases (l1, S18, S19, S20), so a pin both reproduces a check and keeps the work on a revision with a defect once one is published, which STND.LEAN.3 answers. No measured cost of an upgrade per line of proof was found (l1, unverified).

Arithmetic and programs. The floating-point type of Lean is binary64, and its model in the logic reduces only part of its operations: others, the trigonometric functions among them, are opaque, so that even the value of the sine of zero is not provable by reduction; equality is not reflexive for a NaN and not a congruence for signed zeros; and foreign code that changes the floating-point environment breaks the match between the runtime and the model, which the manual warns against using as the basis of a larger library (l1, S6) (STND.LEAN.23). A proof over the reals with a separate bound of the rounding error is the other route, and STND.VVUQ.36 and STND.VVUQ.37 govern the estimate of that bound. In Lean programs the subtraction, division, and remainder of natural numbers give the same values as in statements (l1, S6a), and the fixed-width integer types wrap (unverified in l1) (STND.LEAN.24); a clamp at zero that no check reports is the silent clamping that PRIME.4 forbids where it hides invalid input. A panic in compiled Lean code prints a message and continues with a default value of its result type, as the manual describes and l1 does not (unverified); the kernel defect that l1 reports was a panic of that kind (l1, S5). Indexing by the form that panics on an invalid index is such a panic, and the forms that return an optional value or take a proof of the bound are the alternatives. A setting of the runtime that ends the run at the first panic, at present an environment variable, meets the second sentence of STND.LEAN.25 (unverified). Whether a panic that prints a message and continues is a visible degradation under PRIME.4 the custodian has not ruled, so STND.LEAN.25 is a default. STND.LEAN.26 is the form for Lean of the statement of assumed conditions that STND.JL.18 asks of Julia; the foreign code behind an `extern` attribute is governed by the standard of its language, and the manual states the rules of reference counting that foreign code obeys and calls the foreign interface unstable (l1, S6c). STND.CODE.6 and STND.CODE.7 bind Lean code as they bind all code; STND.CODE.3 puts the contract of an interface in its doc comment; STND.DOCS.13 runs each example of the work documentation among the checks of each change; STND.CODE.4 governs the linters of Lean, with each suppression at its location and with its reason; STND.CONC governs tasks and threads; and STND.CODE.2 and STND.VVUQ.62 govern random numbers. A test that the kernel decides by reduction on a closed instance is a proof about that instance, and a test that compiled code evaluates exercises the compiler as well; both are tests under VV.7 with their references stated. The naming conventions of the Lean libraries form the name of a theorem from its statement, so that a reader predicts the name of a lemma; the convention of the large mathematics library joins capitalized words for types and propositions, joins words with a lowercase first word for other terms, and separates lowercase words by underscores for theorems (as recalled; unverified in l1). STND.LEAN.27 leaves the convention to the repository configuration, which therefore departs from the underscore names of functions that STND.PY, STND.JL, and STND.CXX ask, where a work follows such a convention.

Maintenance. Proof scripts are code with a size and a cost: in the industrial case of l1 the model had 1,673 lines, the proofs 5,714, the production code 15,693, and the tests 20,458, and the proofs and the model checked in about 3 minutes (l1, S8); the ratio of 13 lines of proof to 1 of model in practice 19 of l1 does not follow from those figures, which give about 3.4 to 1. Maintenance cost comes mostly from changes of the libraries rather than from the project's own changes, by general experience and not by a measured study (l1, unverified). A tactic that rewrites by a set of lemmas that a library selects by attribute, the simplifier among them, changes its effect when the library changes that set, so a tactic of that kind that closes its goal fails visibly, and one that names its lemmas does not change (STND.LEAN.29). A proof that reaches a library definition through the lemmas that the library states depends on the stated contract of that library, as DSGN.7 asks, and breaks less often than one that unfolds the definition (STND.LEAN.30). The limits of elaboration count small allocations rather than time, so that a timeout is more deterministic across hardware; a proof that passes only at a raised limit passes on every machine and fails after a library change that makes it slower (l1, S23) (STND.LEAN.28). Elaboration with fixed inputs and limits gives the same verdict on each run, as STND.CODE.9 asks of tests, and a variation of the build time is no defect under STND.VVUQ.82. Lean's deprecation attribute warns on a renamed declaration, and libraries keep aliases with warnings for a period (l1, S16, S18) (STND.LEAN.31, the form for Lean of STND.JL.35). RSRC.3 records the time and the memory of a check, as of each run.

Proof at CSQ0. From CSQ0, STND.CLASS.10 asks the verification of each safety-related component by proof or by exhaustive checking of its state space, and the mechanical checking of each contract of a safety-related component (VV.1, DSGN.3). A Lean proof meets the first of these where its theorem is a relied-on theorem whose trusted statement is the contract or the specification of the component, held and compared under STND.LEAN.9 and STND.LEAN.10 and reviewed under STND.LEAN.11, STND.LEAN.12, and STND.LEAN.13; whose axiom inventory passes STND.LEAN.6 and holds no native evaluation; that an independent checker accepts (STND.LEAN.16); and whose link of STND.LEAN.19 to the code that runs is one of its first three rows, with what the link trusts stated in the record of STND.LEAN.4. An exhaustive check of a finite state space by a decision procedure that the kernel checks is a proof in that sense, and one by native evaluation is not. A separate implementation compared with a Lean model is evidence by comparison, which the same row admits only where the human owner records that neither proof nor exhaustive checking is feasible, a decision that STND.CLASS.10 already assigns. The same theorem, accepted by a checker, is the mechanical checking of the contract that the row of DSGN.3 asks. QA.9 asks from CSQ1 that another actor or system regenerate a reported result before reliance; for a proof, that is a build and check from its records on a system other than the producer's, which is a different check from the replay of STND.LEAN.15 on the producer's own system. This reading of the rows of STND.CLASS.10 is the standard's, for the custodian to confirm.

Class onset. Under STND.CLASS.10, each default instantiates only VV, REPRO, INTPR, DSGN, or SIMPL, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row. The parts that state what a theorem does not establish rest on the documentation of the limits of validity (INTPR.10) and apply from CSQ2: the row Not covered of the table of STND.LEAN.4, the second sentence of STND.LEAN.17, the second sentence of STND.LEAN.20, and STND.LEAN.23. The tests of the second sentence of STND.LEAN.18 and of the first sentence of STND.LEAN.20 compare code with a reference oracle produced without using it, and apply from CSQ2. STND.LEAN.16 applies only to a safety-related component, and so from CSQ0. The mechanical checks of STND.LEAN.6 and STND.LEAN.10 instantiate DSGN.3 and apply from CSQ3; the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 starts at CSQ0, stays with that row, and the regeneration of QA.9 stays with its row at CSQ1. The review of STND.LEAN.11 and the evidence of STND.LEAN.13 validate a specification against its intended use with no real-world referent, and apply from CSQ3. The three sentences of STND.LEAN.1 and of STND.LEAN.21 each share one onset, so that each applies as one bundle. STND.LEAN.5 instantiates PRIME.2 and applies at every class, CSQ4 included. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.JL | Julia standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Toolchain and libraries

#### STND.LEAN.1 Pinned Lean toolchain

Default. Instantiates REPRO.1, REPRO.2, REPRO.9.

The repository configuration SHOULD name the exact revision of the toolchain that builds and checks the work (REPRO.1, REPRO.2). A manifest under version control SHOULD give the exact revision of each Lean package that the work imports, directly or through another Lean package (REPRO.1, REPRO.9). Each build and each check of the work SHOULD use, unchanged, the revisions that the repository configuration and that manifest give (REPRO.1).

#### STND.LEAN.2 Upgrades rebuilt from source

Default. Instantiates VV.8.

Where a change alters the revision of the toolchain or of a Lean package, the checks of that change SHOULD build each relied-on theorem from source, without build products of an earlier revision (VV.8). Those checks SHOULD repeat for each relied-on theorem the checks of STND.LEAN.6, STND.LEAN.10, and STND.LEAN.15 (VV.8).

#### STND.LEAN.3 Checker soundness defects

Default. Instantiates VV.8.

Where an advisory or a release note of the toolchain states a defect of soundness in a checker that accepted a relied-on theorem, the next release that relies on that theorem SHOULD rest on its acceptance by a checker free of that defect (VV.8).

### Proof claims

#### STND.LEAN.4 Relied-on theorem record

Default. Instantiates VV.1, VV.5, INTPR.10.

The record of each claim that rests on a relied-on theorem SHOULD give each item of the table of this provision (VV.1, VV.5, INTPR.10).

| Item | Content |
| --- | --- |
| Theorem | The full name of the theorem and the revision of the source that holds it |
| Statement | The trusted statement, and a statement of it in words that a reader of the claim follows without reading Lean |
| Definitions | The meaning of each definition of the work that the trusted statement uses |
| Assumptions | Each hypothesis of the theorem and each declaration of its axiom inventory |
| Native evaluation | Each use of native evaluation on which the theorem depends, with what STND.LEAN.14 asks of it |
| Code that runs | The link of STND.LEAN.19 to the code that the claim concerns, and each definition of STND.LEAN.17 and each replaced implementation of STND.LEAN.18 on the path of the claim |
| Checkers | Each checker that accepted the theorem, with its revision and whether it is an independent checker |
| Statement review | The review of STND.LEAN.11, with its reviewer and its date |
| Not covered | What the claim needs that the theorem does not establish |

#### STND.LEAN.5 Proof status not overstated

Binding. Instantiates PRIME.2.

A theorem whose axiom inventory holds the axiom declaration of a placeholder SHALL NOT be reported as proved (PRIME.2). A theorem SHALL be reported as proved only on a check, at the reported revision of its source, that built each declaration on which the theorem depends (PRIME.2).

#### STND.LEAN.6 Axiom inventory checked

Default. Instantiates VV.1, DSGN.3.

The checks of each change that affects a relied-on theorem SHOULD obtain the axiom inventory of that theorem from the Lean environment that the build of that change produced (VV.1, DSGN.3). Where that inventory holds an axiom declaration that the accepted axiom list does not hold, those checks SHOULD fail (VV.1, DSGN.3).

#### STND.LEAN.7 Accepted axiom declarations

Default. Instantiates VV.9, VV.1.

The accepted axiom list SHOULD hold only logical axiom declarations and axiom declarations that state an axiom that the human owner declared under VV.9 (VV.9, VV.1). Each axiom declaration of the work that the accepted axiom list holds SHOULD carry, at its declaration, the identifier of the record of its axiom (VV.9).

#### STND.LEAN.8 Statements held for later proof

Default. Instantiates VV.1.

Each proposition that the work holds for a later proof SHOULD be held as a definition of that proposition, and not as a theorem that a placeholder proves or as an axiom declaration (VV.1). The source of each release of the work SHOULD hold no placeholder (VV.1).

### Statements

#### STND.LEAN.9 Trusted statements held apart

Default. Instantiates VV.4, DSGN.8, VV.3.

The trusted statement of each relied-on theorem, and each declaration of the work that it uses other than the definitions whose behavior the theorem verifies, SHOULD be held in source files that hold no proof of that theorem (VV.4, DSGN.8). Each change to those files SHOULD be recorded apart from each change to a proof that they judge, with the earlier statement kept in the record (VV.3).

#### STND.LEAN.10 Statements compared after build

Default. Instantiates VV.1, DSGN.3.

The checks of each change SHOULD confirm, in a process apart from the build, that the type of each relied-on theorem in the built Lean environment is its trusted statement, with each declaration that the files of STND.LEAN.9 hold as those files define it (VV.1, DSGN.3).

#### STND.LEAN.11 Statement review hazards

Default. Instantiates VV.4.

Each review of a trusted statement SHOULD read the statement as elaborated, with its notation, coercions, and implicit arguments shown, against the claim that it serves (VV.4). That review SHOULD confirm, for each hazard of the table of this provision that the statement holds, what the row of that hazard gives (VV.4).

| Hazard | The review confirms |
| --- | --- |
| Subtraction of natural numbers, which gives zero where the difference is negative | That each such subtraction has a second operand no greater than its first, or that the truncated value is what the claim needs |
| Division by zero, which gives zero, and remainder by zero, which gives the dividend | That each divisor is nonzero, or that the value at zero is what the claim needs |
| Arithmetic of fixed-width integers, which wraps | That the operands stay in range, or that the claim concerns the wrapped values |
| Notation, instances, macros, or coercions that the work declares | That each symbol of the statement means what the claim means by it |
| A definition whose name says more than its body | That each definition that the statement uses has, by its body, the meaning that its name gives |
| Hypotheses | That they hold together, as STND.LEAN.13 shows |
| The type of each variable | That each variable ranges over the domain of the claim, among natural numbers, integers, rationals, reals, and floating-point values |
| Equality of floating-point values | That the statement does not rely on that equality being reflexive or a congruence |
| Quantifiers and their order | That each quantifier binds what the claim quantifies, in the order of the claim |

#### STND.LEAN.12 Implicit variables declared

Default. Instantiates SIMPL.6.

The source of each trusted statement SHOULD be elaborated under a setting that rejects each variable that the statement uses without a declaration (SIMPL.6).

#### STND.LEAN.13 Non-vacuous trusted statements

Default. Instantiates VV.4, VV.1.

Where a relied-on theorem has hypotheses, the work SHOULD hold a checked proof that at least one instance satisfies them together, or a record of why they hold together in the regime of use (VV.4, VV.1). Where the trusted statement of a relied-on theorem states a property of an implementation, the work SHOULD hold a checked proof that at least one implementation that the claim excludes lacks that property (VV.4).

### Evaluation and checkers

#### STND.LEAN.14 Native evaluation recorded

Default. Instantiates VV.1, REPRO.7.

A relied-on theorem SHOULD NOT depend on native evaluation (VV.1). Where a relied-on theorem depends on native evaluation, the record of STND.LEAN.4 SHOULD give, for each use, the evaluated term, why the kernel did not check it, and evidence for its result that does not rest on the compiler of the toolchain (VV.1, REPRO.7).

#### STND.LEAN.15 Environment replayed apart from build

Default. Instantiates VV.1.

Before a claim relies on a relied-on theorem, a checker SHOULD accept, in a process apart from the build that produced it, the Lean environment that holds that theorem (VV.1). That check SHOULD cover each declaration on which the theorem depends, those of Lean packages and of fetched build products included (VV.1).

#### STND.LEAN.16 Independent checker for safety components

Default. Instantiates VV.1.

Where a relied-on theorem verifies a safety-related component, an independent checker SHOULD accept the Lean environment that holds that theorem (VV.1). Such a theorem SHOULD NOT depend on native evaluation (VV.1).

### Definitions and running code

#### STND.LEAN.17 Total definitions under claims

Default. Instantiates VV.1, INTPR.10.

Each definition whose behavior a relied-on theorem states SHOULD be a total definition (VV.1). Where code that a claim covers calls a definition that is not a total definition, the record of STND.LEAN.4 SHOULD name that definition and state what the claim does not establish of it (VV.1, INTPR.10).

#### STND.LEAN.18 Replaced implementations stated

Default. Instantiates VV.1, DSGN.1.

Where code that a claim covers runs a replaced implementation, the record of STND.LEAN.4 SHOULD name it and give the evidence that it computes what the definition that it replaces computes in the regime of use (VV.1, DSGN.1). The tests of each change to a replaced implementation SHOULD compare its results with those of the definition that it replaces, reduced by the kernel, on a stated set of inputs (VV.1).

#### STND.LEAN.19 Link to running code

Default. Instantiates VV.1, VV.6.

The record of each claim that a relied-on theorem makes about code that runs SHOULD state which link of the table of this provision joins the definitions of the theorem to that code, and what that link trusts beyond the checkers (VV.1, VV.6). Where the link is a separate implementation, the claim SHOULD state that the code is verified by the comparison of STND.LEAN.20 with its Lean model, and not by proof (VV.1).

| Link | Code that runs | Trusted beyond the checkers |
| --- | --- | --- |
| Compiled definitions | The definitions of the theorem, compiled by the toolchain | The compiler and runtime of the toolchain, and each replaced implementation on the path of the claim |
| Generated code | Code that a translator generates from the definitions of the theorem | The translator, and the compiler and runtime of the generated code |
| Translated source | Code in another language from which a translator generates the definitions of the theorem | The translator, the semantics that it gives the other language, and the compiler and runtime of that code |
| Separate implementation | Code written apart from the definitions of the theorem, which are its Lean model | The comparison of STND.LEAN.20, which is evidence by comparison |

#### STND.LEAN.20 Model comparison tests

Default. Instantiates VV.1, VV.8, INTPR.10.

Where the link of STND.LEAN.19 of a claim is a separate implementation, the tests of each change to the code or to its Lean model SHOULD compare the results of the code with those of the compiled Lean model on generated inputs (VV.1, VV.8). The record of those tests SHOULD state the generator of their inputs, the number of inputs, and the part of the domain of the inputs that the generator does not reach (VV.1, INTPR.10).

### Untrusted authors

#### STND.LEAN.21 Proofs from untrusted authors

Default. Instantiates VV.3, VV.1, REPRO.1.

Where an untrusted author writes the proof of a relied-on theorem, its trusted statement SHOULD be fixed, in files that the author does not change, before that author begins the proof (VV.3). The verdict on that proof SHOULD come from a process that runs no code of the source that the author wrote and that checks the exported Lean environment against the trusted statement and the accepted axiom list (VV.1). The record of that verdict SHOULD identify the checked source by its integrity digest (REPRO.1).

#### STND.LEAN.22 Proof review by checks

Default. Instantiates VV.1.

Where the checks of STND.LEAN.6, STND.LEAN.10, and STND.LEAN.15 pass for a relied-on theorem, the review of the correctness of its proof MAY rest on those checks and on the review of STND.LEAN.11, without a reading of the proof (VV.1).

### Arithmetic

#### STND.LEAN.23 Floating-point model stated

Default. Instantiates VV.1, INTPR.10.

Where a relied-on theorem concerns code that computes in floating point, the record of STND.LEAN.4 SHOULD state the model of floating-point arithmetic that the definitions of the theorem use, and each operation of that code that the model leaves opaque or models otherwise than the hardware that runs the code computes it (VV.1, INTPR.10). Where a relied-on theorem states a property of a computation over the reals that floating-point code carries out, that record SHOULD give a bound of the rounding error between the two, or state that the theorem does not cover the floating-point code (VV.1, INTPR.10).

#### STND.LEAN.24 Truncating and wrapping arithmetic

Default. Instantiates DSGN.2, SIMPL.6.

Where code of the work, on the path of a result, subtracts natural numbers, divides or takes a remainder by a divisor that is able to be zero, or computes in a fixed-width integer type, it SHOULD establish by a check or a proof that each such operation gives the value of the arithmetic that the result needs, or state at that location why the value that it gives is correct (DSGN.2, SIMPL.6).

### Programs

#### STND.LEAN.25 Panics in Lean programs

Default. Instantiates DSGN.2, SIMPL.6.

Where code detects a condition that PRIME.4 lists, it SHOULD return the condition in its result, throw it as an error that its caller receives, or halt with a diagnosis, and not respond by a panic (DSGN.2, SIMPL.6). Each run that produces a reported result SHOULD end at its first panic, or record each panic with that result (DSGN.2).

#### STND.LEAN.26 Unsafe and replaced code explained

Default. Instantiates REPRO.7, DSGN.2.

Each `unsafe` declaration, each `implemented_by` attribute, and each `extern` attribute of the work SHOULD state, at its location, the condition that it assumes and why that condition holds (REPRO.7, DSGN.2).

#### STND.LEAN.27 Lean naming conventions

Default. Instantiates INTPR.1.

The repository configuration SHOULD name the naming convention that the Lean source of the work follows (INTPR.1). Each name of the Lean source of the work SHOULD follow that convention (INTPR.1).

### Maintenance

#### STND.LEAN.28 Raised elaboration limits

Default. Instantiates REPRO.7, SIMPL.6.

Each setting that raises a limit of elaboration or of the kernel SHOULD apply only to the declarations that exceed the default limit, and state at its location its value and its reason (REPRO.7, SIMPL.6).

#### STND.LEAN.29 Tactics over library lemma sets

Default. Instantiates SIMPL.6, VV.8.

A tactic whose effect depends on a set of lemmas that an imported library selects by attribute SHOULD close the goal to which it is applied, or name the lemmas that it uses (SIMPL.6, VV.8).

#### STND.LEAN.30 Library definitions through lemmas

Default. Instantiates DSGN.7.

Each proof of a relied-on theorem SHOULD reach the definitions of an imported library through the lemmas that the library states about them (DSGN.7). A proof MAY unfold a definition whose documentation states that proofs unfold it (DSGN.7).

#### STND.LEAN.31 Deprecations in Lean builds

Default. Instantiates DSGN.6, REPRO.7.

Other than a deprecation warning that the repository configuration lists with its reason, each deprecation warning that a build of the work raises SHOULD fail that build (DSGN.6, REPRO.7).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
