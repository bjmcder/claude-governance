# Lean standard (STND.LEAN) 1.0.1

Adopted by The Custodian as revision 1.0 in ledger entry 138 (2026-10-24); revised to 1.0.1 in entry 153 (2026-10-25). This reading copy is composed from the per-provision files in STND/LEAN/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the practice of work in Lean, both as a proof assistant whose checked proofs the work relies on as evidence and as a programming language. It adds to VV, DSGN, AGENT, STND.CODE, STND.DEPS, STND.DOCS, and STND.VVUQ only what Lean makes necessary. It covers the Lean toolchain, the Lean packages, and their upgrades (STND.LEAN.1, STND.LEAN.2, and STND.LEAN.3); the record of a claim that rests on a proof, the status of a proof, the axiom declarations of each relied-on theorem, and statements held for a later proof (STND.LEAN.4 to STND.LEAN.8); trusted statements, held apart from their proofs, compared after the build, reviewed, and shown not to be vacuous (STND.LEAN.9 to STND.LEAN.13); native evaluation and the checkers of a proof (STND.LEAN.14, STND.LEAN.15, and STND.LEAN.16); definitions and the code that runs (STND.LEAN.17 to STND.LEAN.20); proofs from untrusted authors and their review (STND.LEAN.21 and STND.LEAN.22); arithmetic (STND.LEAN.23 and STND.LEAN.24); Lean programs (STND.LEAN.25, STND.LEAN.26, and STND.LEAN.27); and the maintenance of proofs (STND.LEAN.28 to STND.LEAN.31). The Notes give this standard's reading of how a Lean proof meets the rows of STND.CLASS.10 that ask for proof at CSQ0, and of the statement of correspondence that STND.CONC.28 asks of a model.

STND.LEAN.5 instantiates PRIME.2 and STND.LEAN.25 instantiates PRIME.4, so these two are binding and apply at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard names the constructs of the Lean language and no release of the Lean toolchain, library, checker, tactic, option, or other tool (GOV.18); the repository configuration of each work selects them.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration has the meaning that STND.CODE gives it; Advisory and Integrity digest have the meanings that STND.DEPS gives them; Safety-related component has the meaning that STND.CLASS gives it; Clean build and Build step have the meanings that STND.BUILD gives them.

| Term | Definition |
| --- | --- |
| Lean | The functional programming language and proof assistant of that name that the Lean reference manual describes, at each release of the Lean toolchain. |
| Lean toolchain | The compiler, kernel, build tool, and core library of Lean of one release. |
| Lean package | A unit of Lean source that the build tool of the Lean toolchain fetches and builds as a dependency of the work, at the revision that a manifest gives. |
| Lean environment | The declarations that Lean holds after it elaborates a module and the modules that the module imports. |
| Kernel | The part of the Lean toolchain that type-checks each declaration before a Lean environment admits it. |
| Checker | A program that checks the declarations of a Lean environment against the rules of the type theory of Lean. The kernel is a checker. |
| Independent checker | A checker whose source was written apart from the source of the kernel, and not by translation of that source, and that runs on no part of the runtime of the Lean toolchain. |
| Relied-on theorem | A theorem of a Lean environment on whose proof a claim of correctness of the work rests as evidence. |
| Trusted statement | Of a relied-on theorem: the proposition that the theorem is required to prove, written in Lean source apart from its proof. It is the acceptance criterion of that proof. |
| Axiom declaration | A declaration that adds to a Lean environment a constant of a stated type without a definition or a proof, whether the `axiom` command of the source or the Lean toolchain makes it. |
| Logical axiom declaration | An axiom declaration that the core library of Lean makes as part of the logic of Lean, other than one by which a placeholder or native evaluation enters a Lean environment. |
| Placeholder | A term or a tactic that closes a goal of a proof without proving it, and that the Lean toolchain records by an axiom declaration. |
| Axiom inventory | Of a theorem: the axiom declarations on which its type or its proof depends, directly or through other declarations, as the Lean toolchain reports them from the Lean environment. |
| Accepted axiom list | The list, in the repository configuration, of the axiom declarations that the axiom inventory of a relied-on theorem is admitted to hold. |
| Native evaluation | Evaluation of a term by code that the compiler of the Lean toolchain produced, whose result a Lean environment admits in a proof through an axiom declaration. |
| Total definition | A definition without the `partial` or `unsafe` modifier, whose recursion, where it recurses, is structural or well-founded. |
| Replaced implementation | Code that runs in place of the code compiled from the body of a definition, by the `implemented_by` or `extern` attribute of that definition. |
| Lean model | Lean definitions that state the behavior of code that runs, written apart from that code. |
| Untrusted author | A language model, a tool that searches for or generates proofs, or an actor whom the threat model of the project does not trust, as the author of Lean source. |

## Notes

Direction and sources. Lean is one of the standards in the custodian's order of 2026-10-24, and the custodian's standing directions ask that each standard be agnostic of platform, compiler, vendor, implementation, framework, and tool, and timeless. The provisions therefore name the constructs of the language and no release of the Lean toolchain, library, checker, tactic, option, or command; a Note names one only to show a hazard (research/lean-notes/l1-lean4.md, "Timeless versus moving"). The research note, l1 below, read its sources as extracts that a retrieval tool wrote and ran no Lean; its central source is the chapter of the Lean reference manual on validating proofs (l1, S1). A fact that l1 does not support is marked unverified, and no provision rests on one. The provisions rest on what l1 finds timeless across proof assistants: a checked proof is relative to its statement, its axioms, and its checker; placeholders and axioms are listed, not trusted by default; evaluation by compiled code is a lower level of trust than checking by the kernel; a model and the code that runs are joined by a stated link; checkers that derive from one another share defects; and proofs that a machine generates come from an untrusted author and are checked against a trusted statement.

What a checked proof establishes. A proof that the kernel accepts establishes that a term of the stated type exists, relative to the axiom declarations that it uses and to the soundness of the logic, of the kernel, and of the runtime and host that ran the check. It establishes nothing about whether the statement means what the claim needs, whether the code that runs computes what the definitions compute, or whether the check covered the dependencies of the theorem (l1, practices 1, 2, and 4); native evaluation adds the compiler to the base (l1, S1, S2). VV.1 asks that evidence state its assumptions and show them met. The soundness of the logic and of each checker, and the logical axiom declarations, are assumptions that no check shows met, so the Assumptions row of STND.LEAN.4 has each stated as assumed; a check that no checker makes is not able to show them met, and the record that states them assumed tells a reader what the evidence does not cover. The rows of STND.LEAN.4 are the items that l1 gives a reviewer (practice 22), and its statement in words is work documentation under STND.DOCS.2, STND.DOCS.9, and STND.DOCS.12. The proof verifies the code against the trusted statement, and the review of STND.LEAN.11 validates the statement against the claim, which keeps the two apart as VV.4 and VV.5 ask.

Status of a proof. The editor's mark that the current theorem checked appears even where a dependency holds a placeholder (l1, S1). A report that a theorem is proved, where it rests on a placeholder or on a check that did not cover its dependencies, claims a check that was not run, which PRIME.2 forbids at every class; STND.LEAN.5 states that in the terms of Lean. In its first sentence, reported as proved means proved without qualification, so a report that names the placeholder misstates nothing. Its second sentence asks a check of each declaration on which the theorem depends, those of Lean packages included, other than those of the Lean toolchain, and admits a report that names the declarations its check did not cover; a work that takes a Lean package from fetched build products that no checker of the work replayed names that package. STND.LEAN.15 and STND.DEPS.6 govern the check and the integrity of those products. STND.LEAN.5 costs its wording and a sentence of the report, and the Notes argue that it forbids nothing that PRIME.2 and AGENT.4 do not, so that it raises no floor (GOV.11).

Axioms and placeholders. An Axiom of the Lexicon is an assumption that the human owner declares, and VV.9 and GOV.50 reserve its declaration to the human owner; an axiom declaration of Lean states such an Axiom only where the human owner declared it. The logical axiom declarations, at present propositional extensionality, the axiom of choice, and the soundness of quotients, belong to the logic of Lean and are accepted across its community (l1, S2). This standard reads them as assumptions of the evidence under VV.1, as the soundness of the kernel is, and not as Axioms of the work, so that STND.LEAN.7 asks no decision of the human owner; a standing declaration of the logic of Lean by the human owner under VV.9, cited by each relied-on theorem, would meet VV.1 as well, at the cost of a decision of the human owner for each work. The axiom declarations of native evaluation that a record of STND.LEAN.14 covers are trust in the compiler, an assumption that the record states, and STND.LEAN.7 admits them on that reading. Lean does not check that a new axiom declaration is consistent, and the declaration by which a placeholder enters proves every proposition (l1, S2). The `#print axioms` command gives the axiom inventory at present, and STND.LEAN.6 rests on a list in the repository configuration because the names that native evaluation uses have changed between releases (l1, S1). A proposition held as a definition gives a later proof nothing to use as a lemma, while a theorem that a placeholder proves does; an audit of benchmarks recommends such a form (l1, S15) (STND.LEAN.8). Placeholders stay admitted in work in progress, and a release states its own for the decision of QA.10.

Trusted statements. A statement that does not mean what the claim needs is the commonest failure that l1 found: one study found an error in about 40 percent of the formal statements of a public benchmark, and an audit of five benchmarks separates statements weaker than intended from statements that mistranslate (l1, S14, S15). Holding the statement apart from the proof, and comparing the proved type with it in a process apart from the build, defends against a proof file that redefines a definition, a notation, or an instance that the statement uses (l1, S1, practice 16) (STND.LEAN.9 and STND.LEAN.10). The definitions whose behavior a theorem verifies are code of the work, which the review of QA.7 covers. The trusted statement and the accepted axiom list are acceptance criteria under VV.3, and the second sentence of STND.LEAN.9 records a change of either apart from the proof that they judge, for every author, as AGENT.5 does for an agent. The hazards of STND.LEAN.11 are the kinds that l1 lists (practice 9, S6a, S15); whether the fixed-width integer types wrap is unverified in l1, and the row of those types holds whatever values they give out of range. A study found agents that redefined operators by local notation so that theorems became trivial, past a filter that looked only for the keywords of axioms and placeholders (l1, S22, from a search summary). The setting of STND.LEAN.12, at present an option that turns off automatically bound implicit arguments, is one the audit recommends (l1, S15). A statement whose hypotheses do not hold together is vacuous evidence, which PRIME.2 already forbids, and STND.LEAN.13 gives the means of showing the opposite, so it is a default (l1, practice 10).

Evaluation and checkers. The decision tactics that evaluate by compiled code, at present `native_decide` and the decision procedure for bit vectors, admit their results through an axiom declaration, so the compiler enters the trusted base and no checker other than the Lean toolchain's runtime is able to check them (l1, S1, S2, S9). STND.LEAN.14 admits them with a record, because a check by the kernel of a large closed term is at times infeasible (l1, S23); l1 found no report of compiled code disagreeing with the kernel and searched no issue tracker (unverified). An axiom inventory catches placeholders, project axioms, and native evaluation; a replay in a fresh process catches tampering by meta-programs that ran during the build, which are able to add declarations that no checker saw, but not a defect of the kernel; a second checker of separate origin catches a defect present in one checker only (l1, table of levels of check; S1, S3) (STND.LEAN.15). A downloaded cache of build products holds declarations that the local kernel did not check, by inference from l1 (S7) and unverified, and the second sentence of STND.LEAN.15 covers them. Soundness defects of the kernel and its runtime have been found more than once, one bad proof was accepted by a second kernel as well, and a checker derived from the reference kernel's source is likely to share its defects (l1, S5, S18, S19, S20). The term Independent checker therefore excludes a checker translated from the kernel and one that runs on the Lean toolchain's runtime, which one runtime defect reached (l1, S18). l1 calls independence a matter of degree, and no checker that it describes is known to meet the strict term: its second kernel is a port written in Lean that runs on the Lean toolchain's runtime (l1, S5), and it does not say which of the 29 checkers of an arena does (l1, S21; unverified). The strict term keeps out the checkers that share a defect with the kernel through its source or its runtime. Where no independent checker is among the means of the work, the first sentence of STND.LEAN.16 does not apply and blocks no work, and the row Checkers of STND.LEAN.4 states whether each checker that accepted the theorem is independent, so that a checker whose source was written apart, on whatever runtime, is recorded with its relation to the kernel. STND.LEAN.3 is the form for checkers of the check of advisories of STND.DEPS.7; where no checker free of the stated defect exists, its record states that none was available, so that no release is blocked for want of one.

Definitions and the code that runs. A `partial` definition is opaque to the kernel, so no theorem states what it computes, and an `unsafe` one is outside the equational theory; neither makes the logic inconsistent, and each cuts the link between the theorem and what runs (l1, S4, practices 7 and 8) (STND.LEAN.17). The `implemented_by` and `extern` attributes leave the definition for the kernel and run other code, whose equivalence the reference manual counts as part of the trusted code base (l1, S4, S6c) (STND.LEAN.18). The kernel's own arbitrary-precision operations on natural numbers are part of the trusted base of every check, not a replaced implementation of the work (l1, S5, S6a). The links of STND.LEAN.19 are the four of l1 (practice 11; S8, S12, S13). Each joins the code of one component to its theorem, the verification of a component against its contract under VV.6; the verification of assemblies, which the CSQ1 row adds, is outside it. In the industrial case of l1, differential testing on generated inputs found 21 defects in the implementation, proof found 4 that testing was unlikely to find, and the generators produced no malformed input at all (l1, S8), which is the reason of the second sentence of STND.LEAN.20. That case's release rule is the condition of QA.10 that evidence be current. STND.LEAN.19 with the row Code that runs of STND.LEAN.4 is the statement of correspondence that STND.CONC.28 asks of a Lean model, and the memory model of that row is the one of HW.11, as the Notes of STND.CONC ask.

Untrusted authors and agents. The reference manual counts un-reviewed machine-generated proofs among its malicious cases (l1, S1). Proofs that language models wrote passed a compile by local notation that redefined an operator, by a tactic defect that reported success without a declaration that passed the kernel, by added axioms, and by native evaluation; one prover found nine patterns of compilable but invalid code by checking that the statement was unchanged (l1, S11, S15, S22, S27, the last two from search summaries). The term Untrusted author names kinds of author, so every language model is one, the project's own agents included, and a person whom the threat model trusts is not; GOV.51 also treats tool software that is not shown to execute only a fixed specification as an agent. The three sentences of STND.LEAN.21 are one protocol and are never applied apart: criteria fixed first and kept from the author, a verdict from a process that runs none of the author's code, and the exact source identified; each leaves open a hazard that the others close. The definitions under verification stay open to the author, and the review of QA.7 alone covers them. GUARD.17 and the threat model of GUARD.16 govern where untrusted source runs during its elaboration. A proof term that a checker accepts is open to independent verification (l1, S29), which STND.LEAN.22 lets a reviewer take from checks set before the change, for the correctness of the proof only; the rest of the change, and the judgments of STND.LEAN.17, STND.LEAN.24, STND.LEAN.29, and STND.LEAN.30, stay with the review of QA.7. An agent states each placeholder that it adds, each statement that it weakens, and each check that it disables as departures under AGENT.47, and proposes rather than declares an axiom under GOV.50; for AGENT.12, the acceptance criteria of a delegated proof are its trusted statement and the accepted axiom list.

Lean toolchain and upgrades. Build products of one Lean toolchain do not serve another, the manifest gives the exact revision of each Lean package, and an automatic update of the Lean toolchain changes the file that names the Lean toolchain unless it is turned off (l1, S7), which is the hazard of the second sentence of STND.LEAN.1. The release notes of one recent release list renamed lemmas, a removed parameter, a changed simplification set, a changed reducibility, and a stricter kernel (l1, S18), so an upgrade is a change under VV.8, and STND.LEAN.2 is the form of STND.DEPS.5 for Lean. A clean build meets the first sentence of STND.LEAN.2, and the build of Lean source is otherwise a build under STND.BUILD, whose STND.BUILD.1 counts each tool of the Lean toolchain among the declared inputs of each build step and whose STND.BUILD.23 keys each output that a build cache serves on the revision of each tool that produced it. A Lean package fixes the Lean toolchain with which it builds, so the clause of STND.DEPS.3 on consistency with the rest of the computational environment sets the Lean toolchain of a work that imports it. Fixes of soundness defects arrive in point releases (l1, S18, S19, S20), so a pin also keeps the work on a revision with a published defect, which STND.LEAN.3 answers. No measured cost of an upgrade per line of proof was found (l1, unverified).

Arithmetic and programs. The floating-point type of Lean is binary64, and its model in the logic reduces only part of its operations, so that even the value of the sine of zero is not provable by reduction; equality is not reflexive for a NaN and not a congruence for signed zeros; and foreign code that changes the floating-point environment breaks the match between the runtime and the model (l1, S6) (STND.LEAN.23). A proof over the reals with a separate rounding bound is the other route, whose estimate STND.VVUQ.36 and STND.VVUQ.37 govern. In programs, the subtraction, division, and remainder of natural numbers give the values that they give in statements (l1, S6a), and a clamp at zero that no check reports is the silent clamping that PRIME.4 forbids where it hides invalid input (STND.LEAN.24). In this standard a panic is the Lean operation of that name, which, in the kernel defect that l1 reports, continues with a default value and does not end the computation (l1, S5); that the default value is one of the result type, that compiled code also prints a message, and that a setting of the runtime ends the run at the first panic are from the manual as recalled (unverified). Indexing by the form that panics on an invalid index, and the alternatives of a form that returns an optional value and a form that takes a proof of the bound, are likewise unverified in l1. The second sentence of STND.LEAN.24 names a function that chooses its own value in place of its result on a failure, and not a construct, so it holds whatever a panic does; a default that the caller supplies is outside it. STND.LEAN.25 states by their outcome the forms by which Lean code gives each response that PRIME.4 admits, the Lean form of STND.CODE.14, whose pass of the condition to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism of the language that propagates it takes in Lean two forms, as STND.PY.22 and STND.JL.15 give the forms of their languages: a result of a type that carries the condition, and an error raised in a monad whose caller receives it. The core library of Lean names such types `Except` and `Option`, and such an operation `throw`; l1 does not discuss them (unverified), so the provision names none of them. STND.CODE.7 keeps the caller that receives such a result from discarding it. STND.LEAN.25 adds the forms of Lean to PRIME.4 at the cost of its wording, the argument that the Notes of STND.JL give for STND.JL.15; the custodian's ruling of 2026-10-23 on that argument was made for STND.JL, and the ratification of 2026-10-24 accepted it for STND.LEAN.25. STND.LEAN.26 is the form for Lean of STND.JL.18. The foreign code behind an `extern` attribute is governed by the standard of its language, and the manual calls the foreign interface unstable (l1, S6c). A test that the kernel decides by reduction on a closed instance is a proof about that instance, and one that compiled code evaluates exercises the compiler as well; both are tests under VV.7. The convention of the large mathematics library forms the name of a theorem from its statement, so that a reader predicts the names of lemmas (as recalled; unverified in l1); STND.LEAN.27 leaves the convention to the repository configuration, where STND.CXX.14, STND.PY.1, and STND.JL.6 fix one, and keeps the names that the notation of NUMER.4 fixes, as they do.

Maintenance. In the industrial case of l1, the model had 1,673 lines, the proofs 5,714, and the production code 15,693, and the proofs and the model checked in about 3 minutes (l1, S8); the ratio of 13 lines of proof to 1 of model in practice 19 of l1 does not follow from those figures, which give about 3.4 to 1. A tactic that rewrites by a set of lemmas that a library selects by attribute changes its effect when the library changes that set; one that closes its goal fails visibly, and one that names its lemmas does not change (STND.LEAN.29). A proof that reaches a library definition through its stated lemmas depends on the stated contract that DSGN.7 asks (STND.LEAN.30). The limits of elaboration count small allocations, not elapsed time, so a proof that passes only at a raised limit passes on every machine and fails after a library change that makes it slower (l1, S23) (STND.LEAN.28); a variation of build time is no defect under STND.VVUQ.82. Libraries keep aliases of renamed declarations with warnings for a period (l1, S16, S18), and STND.LEAN.31 is the form for builds of STND.JL.35.

Proof at CSQ0. From CSQ0, STND.CLASS.10 asks the verification of each safety-related component by proof or by exhaustive checking of its state space, and the mechanical checking of each contract of a safety-related component (VV.1, DSGN.3). This standard's default for meeting the first with a Lean proof is a relied-on theorem whose trusted statement is the contract or specification of the component, under STND.LEAN.9 to STND.LEAN.13; whose axiom inventory passes STND.LEAN.6 with no native evaluation; that, where the means of the work include one, an independent checker accepts (STND.LEAN.16); and whose link of STND.LEAN.19 is one of its first three rows, with what it trusts in the record of STND.LEAN.4. That is a reading and a default, not a narrowing of VV.1: where no independent checker is among the means of the work, the first sentence of STND.LEAN.16 does not apply, and the record of STND.LEAN.4 states, in its rows Assumptions and Checkers, how the Lean proofs of the work meet VV.1. An exhaustive check by a decision procedure that the kernel checks is a proof on this reading, and exhaustive checking outside Lean meets the row equally. A separate implementation compared with a Lean model is evidence by comparison, which the row admits only where the human owner records that neither proof nor exhaustive checking is feasible. The same theorem, accepted by a checker, is the mechanical checking of the DSGN.3 row. The regeneration of QA.9 from CSQ1 is, for a proof, a build and check from its records on another system, a different check from the replay of STND.LEAN.15.

Class onset. Under STND.CLASS.10, each default instantiates only VV, REPRO, INTPR, DSGN, or SIMPL, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row, sentence by sentence as follows. STND.LEAN.1 to STND.LEAN.3 rest on no row and apply from CSQ3. STND.LEAN.4 applies from CSQ3, except its row Not covered, which documents limits of validity (INTPR.10) and applies from CSQ2, and its row Code that runs as to the definitions of STND.LEAN.17, which takes the onset of the second sentence of STND.LEAN.17; the memory and ordering model of that row records an assumption of the evidence (VV.1) from CSQ3, while the verification of the invariants of a protocol (DSGN.15) stays with its row at CSQ2 and the proof of STND.CONC.28 with the CSQ0 row. STND.LEAN.6 to STND.LEAN.10 and STND.LEAN.12 apply from CSQ3; the mechanical checking of each contract of a safety-related component stays with the CSQ0 row of DSGN.3. STND.LEAN.11 and STND.LEAN.13 apply from CSQ3; where the claim has a real-world referent, the validation against it follows the CSQ2 row of VV.4. The first sentence of STND.LEAN.14 and the record of its second apply from CSQ3; the evidence of that second sentence that does not rest on the compiler is a comparison with a reference produced without the compiled code, and applies from CSQ2 by the row of the reference oracle. Both sentences of STND.LEAN.15 apply from CSQ3; the regeneration of QA.9 stays with its row at CSQ1. STND.LEAN.16 applies only to a safety-related component, and so from CSQ0. The first sentence of STND.LEAN.17 applies from CSQ3, and its second, which states limits of validity (INTPR.10), from CSQ2. The first sentence of STND.LEAN.18 applies from CSQ3; its second compares code with a reference oracle produced without using it and applies from CSQ2. Both sentences of STND.LEAN.19 verify a component against its contract and apply from CSQ3; the verification of assemblies stays with the CSQ1 row of VV.6. Both sentences of STND.LEAN.20 apply from CSQ2, the first by the row of the reference oracle and the second by the row of INTPR.10. The three sentences of STND.LEAN.21 share the onset CSQ3. Both sentences of STND.LEAN.22 apply from CSQ3. Both sentences of STND.LEAN.23 state limits of validity and apply from CSQ2. The first sentence of STND.LEAN.24 is met by a check of the operands before each operation, a check of a precondition, or by a proof or a stated reason, and applies from CSQ3; it does not ask the checking of results after an operation, which the CSQ1 row of DSGN.2 starts. The second sentence of STND.LEAN.24 keeps a function that chooses its own value in place of its result off the path of a result, whether or not that choice is visible, and applies from CSQ3. STND.LEAN.26 states the condition that each construct assumes, as STND.JL.18 does, and applies from CSQ3. STND.LEAN.27 to STND.LEAN.31 rest on no row and apply from CSQ3. STND.LEAN.5 instantiates PRIME.2 and STND.LEAN.25 instantiates PRIME.4, and both apply at every class, CSQ4 included. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no provision raises the floor (GOV.11), by the arguments above for STND.LEAN.5 and STND.LEAN.25.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.BUILD | Build standard |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.JL | Julia standard |
| STND.PY | Python standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Toolchain and libraries

#### STND.LEAN.1 Pinned Lean toolchain

Default. Instantiates REPRO.1, REPRO.2, REPRO.9.

The repository configuration, with a manifest under version control, SHOULD give the exact revision of the Lean toolchain, of each checker, and of each Lean package that the work imports, directly or through another Lean package (REPRO.1, REPRO.2, REPRO.9). Each build and each check of the work SHOULD use those revisions unchanged (REPRO.1).

#### STND.LEAN.2 Upgrades rebuilt from source

Default. Instantiates VV.8.

Where a change alters the revision of the Lean toolchain or of a Lean package, the checks of that change SHOULD build each relied-on theorem from source, without build products of an earlier revision (VV.8). Those checks SHOULD repeat for each relied-on theorem the checks of STND.LEAN.6, STND.LEAN.10, and STND.LEAN.15 (VV.8).

#### STND.LEAN.3 Checker soundness defects

Default. Instantiates VV.8.

Where an advisory or a release note of the Lean toolchain states a defect of soundness in a checker that accepted a relied-on theorem, the next release that relies on that theorem SHOULD rest on its acceptance by a checker free of that defect, or state in its record that no such checker was available (VV.8).

### Proof claims

#### STND.LEAN.4 Relied-on theorem record

Default. Instantiates VV.1, VV.5, INTPR.10.

The record of each claim that rests on a relied-on theorem SHOULD give each item of the table of this provision (VV.1, VV.5, INTPR.10).

| Item | Content |
| --- | --- |
| Theorem | The full name of the theorem and the revision of the source that holds it |
| Statement | The trusted statement, and a statement of it in words that a reader of the claim follows without reading Lean |
| Definitions | The meaning of each definition of the work that the trusted statement uses |
| Assumptions | Each hypothesis of the theorem, each declaration of its axiom inventory, and the soundness of each checker that accepted it, each with whether it is shown to hold or stated as assumed |
| Native evaluation | Each use of native evaluation on which the theorem depends, with what STND.LEAN.14 asks of it |
| Code that runs | The link of STND.LEAN.19 to the code that the claim concerns, each definition of STND.LEAN.17 and each replaced implementation of STND.LEAN.18 on the path of the claim, and, for concurrent code, the memory and ordering model that the Lean model assumes |
| Checkers | Each checker that accepted the theorem, with its revision and whether it is an independent checker |
| Statement review | The review of STND.LEAN.11, with its reviewer, its date, and whether it found that the trusted statement says what the claim needs, or the statement that validation does not apply for want of a real-world referent |
| Not covered | What the claim needs that the theorem does not establish |

#### STND.LEAN.5 Proof status not overstated

Binding. Instantiates PRIME.2.

A theorem whose axiom inventory holds the axiom declaration of a placeholder SHALL NOT be reported as proved (PRIME.2). Other than in a report that names the declarations that its check did not cover, a report that a theorem is proved SHALL rest on a check, at the reported revision of the source, of each declaration on which the theorem depends other than those of the Lean toolchain (PRIME.2).

#### STND.LEAN.6 Axiom inventory checked

Default. Instantiates VV.1, DSGN.3.

The checks of each change that affects a relied-on theorem SHOULD obtain the axiom inventory of that theorem from the Lean environment that the build of that change produced (VV.1, DSGN.3). Where that inventory holds an axiom declaration that the accepted axiom list does not hold, those checks SHOULD fail (VV.1, DSGN.3).

#### STND.LEAN.7 Accepted axiom declarations

Default. Instantiates VV.9, VV.1.

The accepted axiom list SHOULD hold only logical axiom declarations, axiom declarations that state an axiom that the human owner declared under VV.9, and the axiom declarations of native evaluation that a record of STND.LEAN.14 covers (VV.9, VV.1). Each axiom declaration of the work that the accepted axiom list holds SHOULD carry, at its declaration, the identifier of the record of its axiom (VV.9).

#### STND.LEAN.8 Statements held for later proof

Default. Instantiates VV.1.

Each proposition that the work holds for a later proof SHOULD be held as a definition of that proposition, and not as a theorem that a placeholder proves or as an axiom declaration (VV.1). Each placeholder that the source of a release holds SHOULD be stated in the record of that release (VV.1).

### Statements

#### STND.LEAN.9 Trusted statements held apart

Default. Instantiates VV.4, DSGN.8, VV.3.

The trusted statement of each relied-on theorem, and each declaration of the work that it uses other than the definitions whose behavior the theorem verifies, SHOULD be held in source files that hold no proof of that theorem (VV.4, DSGN.8). Each change to those files or to the accepted axiom list SHOULD be recorded apart from each change to a proof that they judge (VV.3).

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
| Arithmetic of fixed-width integers | That the operands stay in range, or that the claim concerns the values that the type gives out of range |
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

A relied-on theorem SHOULD NOT depend on native evaluation (VV.1). Where a relied-on theorem depends on native evaluation, the record of STND.LEAN.4 SHOULD give, for each use, the evaluated term, why the kernel did not check it, and evidence for its result that does not rest on the compiler of the Lean toolchain (VV.1, REPRO.7).

#### STND.LEAN.15 Environment replayed apart from build

Default. Instantiates VV.1.

Before a claim relies on a relied-on theorem, a checker SHOULD accept, in a process apart from the build that produced it, the Lean environment that holds that theorem (VV.1). That check SHOULD cover each declaration on which the theorem depends, those of Lean packages and of fetched build products included (VV.1).

#### STND.LEAN.16 Independent checker for safety components

Default. Instantiates VV.1.

Where the means of the work include an independent checker, it SHOULD accept the Lean environment that holds each relied-on theorem that verifies a safety-related component (VV.1). A relied-on theorem that verifies a safety-related component SHOULD NOT depend on native evaluation (VV.1).

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
| Compiled definitions | The definitions of the theorem, compiled by the Lean toolchain | The compiler and runtime of the Lean toolchain, and each replaced implementation on the path of the claim |
| Generated code | Code that a translator generates from the definitions of the theorem | The translator, and the compiler and runtime of the generated code |
| Translated source | Code in another language from which a translator generates the definitions of the theorem | The translator, the semantics that it gives the other language, and the compiler and runtime of that code |
| Separate implementation | Code written apart from the definitions of the theorem, which are its Lean model | The comparison of STND.LEAN.20, which is evidence by comparison |

#### STND.LEAN.20 Model comparison tests

Default. Instantiates VV.1, VV.8, INTPR.10.

Where the link of STND.LEAN.19 of a claim is a separate implementation, the tests of each change to the code or to its Lean model SHOULD compare the results of the code with those of the compiled Lean model on generated inputs (VV.1, VV.8). The record of those tests SHOULD state the generator of their inputs, the number of inputs, and the part of the domain of the inputs that the generator does not reach (VV.1, INTPR.10).

### Untrusted authors

#### STND.LEAN.21 Proofs from untrusted authors

Default. Instantiates VV.3, VV.1, REPRO.1.

Before an untrusted author begins the proof of a relied-on theorem, its trusted statement and the accepted axiom list SHOULD be fixed, in files that the author does not change (VV.3). The verdict on a proof that an untrusted author wrote SHOULD come from a process that runs no code of the source that the author wrote and that checks the exported Lean environment against the trusted statement and the accepted axiom list (VV.1). The record of that verdict SHOULD identify the checked source by its integrity digest (REPRO.1).

#### STND.LEAN.22 Proof review by checks

Default. Instantiates VV.1, VV.4.

Where a change alters neither the accepted axiom list nor the checks of STND.LEAN.6, STND.LEAN.10, and STND.LEAN.15 that the repository configuration set before the change, the review of the correctness of each proof of a relied-on theorem that the change makes MAY rest, without a reading of that proof, on a run of those checks on the reviewed revision that the reviewer makes or confirms (VV.1). Such a review SHOULD include the review of STND.LEAN.11 of the trusted statement and the evidence of STND.LEAN.13 (VV.4).

### Arithmetic

#### STND.LEAN.23 Floating-point model stated

Default. Instantiates VV.1, INTPR.10.

Where a relied-on theorem concerns code that computes in floating point, the record of STND.LEAN.4 SHOULD state the model of floating-point arithmetic that the definitions of the theorem use, and each operation of that code that the model leaves opaque or models otherwise than the hardware that runs the code computes it (VV.1, INTPR.10). Where a relied-on theorem states a property of a computation over the reals that floating-point code carries out, that record SHOULD give a bound of the rounding error between the two, or state that the theorem does not cover the floating-point code (VV.1, INTPR.10).

#### STND.LEAN.24 Values substituted without failure

Default. Instantiates DSGN.2, SIMPL.6.

Where code of the work, on the path of a result, subtracts natural numbers, divides or takes a remainder by a divisor that is able to be zero, or computes in a fixed-width integer type, it SHOULD establish by a check or a proof that each such operation gives the value of the arithmetic that the result needs, or state at that location why the value that it gives is correct (DSGN.2, SIMPL.6). On the path of a result, code SHOULD NOT call a function that, on a failure that it detects, returns a value that the function itself chooses in place of its result (DSGN.2).

### Programs

#### STND.LEAN.25 Lean responses to listed failures

Binding. Instantiates PRIME.4.

Where code detects a condition that PRIME.4 lists, it SHALL return the condition in a result of a type that carries it, raise it as the error of a monad whose caller receives that error, halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade visibly with a diagnosis (PRIME.4, STND.CODE.14).

#### STND.LEAN.26 Unsafe and replaced code explained

Default. Instantiates REPRO.7, DSGN.2.

Each `unsafe` declaration, each `implemented_by` attribute, and each `extern` attribute of the work SHOULD state, at its location, the condition that it assumes and why that condition holds (REPRO.7, DSGN.2).

#### STND.LEAN.27 Lean naming conventions

Default. Instantiates INTPR.1, INTPR.4.

Each name of the Lean source of the work SHOULD follow the naming convention that the repository configuration names (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).

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

Other than a deprecation warning raised inside a Lean package that the repository configuration lists with its reason, each deprecation warning that a build of the work raises SHOULD fail that build (DSGN.6, REPRO.7).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): STND.LEAN.25 cites STND.CODE.14, of which it is the Lean form, with its text otherwise unchanged; the Notes cite STND.CODE.14 in place of STND.CXX.16, which STND.CXX 1.2 withdraws, record that the ratification of 2026-10-24 accepted the floor argument for STND.LEAN.25, and say that proofs that a machine generates come from an untrusted author, the term of this standard, in place of calling them untrusted input, a term of STND.CODE that this standard does not use. |
