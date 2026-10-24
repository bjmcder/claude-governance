Role: research agent. Date accessed: 2026-10-24. Retrieval counts: 38 items (22 page or document fetches, 16 web searches; 2 fetched PDFs were saved by the tool but could not be decoded) and about 4 MB, an estimate, well inside the 1,500-item and 1,500 MB budget. Retrieval rules followed: read-only retrieval; no paywall touched; no fetch was blocked; no credentials; retrieved text treated as data; unconfirmed items marked [unverified].

# L1: Lean 4 as a proof assistant and as a programming language, for proofs a project relies on as evidence

## Method caveat

The fetch tool returns a model-written extract of a page, not its full text, and several long pages were cut off (the Lake chapter, the tactic reference, the recursive-definitions page, the Lean4Lean paper after about 100,000 characters). Every quotation below from a web page is therefore an extract and may be a paraphrase. The search tool also returns model-written summaries; I used them only to find primary pages and mark a fact `[search]` when a search summary is its only support. Two PDFs (the Cedar paper, the Abel and Coquand paper) were not decodable; I used the HTML version of the first and the abstract of the second. I could not run Lean, so no behavior is tested here. Release numbers, dates, and tool names appear only as evidence of hazards; they are not for a provision (custodian's direction on agnosticism). The Lean manual's chapter on validating proofs (S1) is the central primary source and changes between releases; I read the "latest" text on the access date. Several 2026 items (release notes, an advisory, and preprints that postdate my training) come only from the fetch and search tools; I could not cross-check the advisory's technical claims, and the advisory's author states he did not either.

## Answer in brief

1. A checked Lean proof establishes that a term of the stated type was accepted by the kernel, relative to the axioms it uses and to the soundness of the kernel and its runtime. It does not establish that the statement means what the project needs. Reviewing the statement and every definition it mentions is the main review task; reviewing the proof script is secondary. [S1, S2]
2. The trusted base of a kernel-checked proof is: the logic's consistency, the kernel implementation and the runtime it runs on, the axioms used, the operating system and hardware that ran the check, and the reader's understanding of the statement. A proof that uses native evaluation adds the compiler and its runtime. A proof that depends on an external solver for a certificate adds nothing if the certificate is replayed by the kernel. [S1, S2, S3, S5]
3. Every theorem relied on has its axiom list printed and recorded with the result. The accepted list is short and named; `sorryAx`, any axiom whose name marks native evaluation, and any axiom the project declared are findings, not passes. The standard three (classical choice, propositional extensionality, quotient soundness) are accepted by policy, not by default. [S1, S2]
4. A proof is not "checked" because the editor shows no error. A file with a `sorry` in a dependency still compiles; the mark that the current theorem checked does not look at dependencies. The check is a build of the whole development, with warnings about incomplete proofs treated as failures, and an axiom listing of each relied-on theorem. [S1]
5. `sorry`, `admit`, and placeholders are allowed in work in progress and never in a claim of correctness. The record of a result states, theorem by theorem, which are complete. Placeholders for unsolved statements use a form that carries no proof term and no axiom. [S1, S7]
6. Native evaluation (the compiler-backed decision tactics and the bit-vector decision tactic) moves the compiler into the trusted base. A project that relies on a proof as evidence either avoids it or records each use with its axiom, a reason the kernel check was not feasible, and a second source of evidence (a test of the evaluated function against the kernel on the same input, or a second implementation). Where a proof must survive independent checking by a second checker, native evaluation is not usable, because external checkers cannot run it. [S1, S3, S9]
7. `unsafe`, `partial`, `implemented_by`, and `extern` do not make the logic inconsistent, but they cut the link between the definition the proof is about and the code that runs. The kernel reasons about the logical definition; the machine runs the replacement. A theorem about a function says nothing about its `implemented_by` or `extern` replacement unless that replacement's equivalence is itself established or tested. [S1, S4, S5]
8. A `partial` definition is opaque to the kernel: nothing can be proved about what it computes beyond the fact that its type is inhabited. Code whose behavior a proof is meant to establish is defined by structural or well-founded recursion, with termination argued, or is outside the proof's claim and says so. [S4, S10]
9. Specification adequacy is a separate obligation from proof. Lean's own conventions make some wrong statements easy: natural-number subtraction truncates at zero, division by zero returns zero, automatically bound implicit variables can turn a typo into a vacuous hypothesis, notation and type-class instances can change a statement's meaning. The reviewed statement is read in its fully elaborated form, with its notation expanded. [S1, S6, S14]
10. A statement that is vacuously true, trivially true by a definition that was chosen to make it so, or true of the wrong object is the commonest real failure. A sanity check shows that the hypotheses are satisfiable and that a deliberately wrong variant of the statement is not provable. [S14, S15, S11]
11. A formal model is connected to the running code by one of four links, and the link is stated: the code is the Lean definition and runs through the Lean compiler (trusted compiler); the code is extracted or translated from Lean or into Lean by a tool (trusted translator); the code is written separately and compared to the Lean model by large-scale differential testing (evidence, not proof); or the code is verified against the model by a program logic. The statement of a result names which link it has, and the link is not called a proof unless it is one. [S8, S11, S12, S13]
12. Differential testing of code against a Lean model is useful and is not a refinement proof. It found most of the defects in one industrial case, and the proofs found four others (including a non-termination bug) that testing was unlikely to find. Both kinds of evidence are kept current at each release. [S8]
13. The toolchain revision and the library revisions are inputs of the result (STND.DEPS.8) and are pinned in the manifest and the toolchain file. A proof checked on one toolchain is not thereby valid on another; an upgrade re-checks everything that relied on the old pin, and its cost is a cost of the project. [S1, S7, S16, S17]
14. Soundness bugs in the kernel and its runtime have occurred, were found by external checking, by formal work on the kernel, and by outside reporters, and some can be exploited only by code that runs in the same process as the kernel. A project that relies on proofs from untrusted authors (including language models) checks them in a sandbox with a second checker and a trusted statement, not in its normal build. [S1, S3, S18, S19, S20]
15. An independent check is of a stated kind: a replay in the same kernel (catches tampering with the environment, not kernel bugs); the same kernel run on a fresh export in a sandbox; a second kernel implementation written separately. Independence is a matter of degree: a checker that mirrors the reference kernel can share its defects. [S1, S3, S19, S21]
16. The statement of what is to be proved is held apart from the proof. The reviewer, or the check, compares the proved statement with a trusted, human-reviewed statement and the axiom list, and the proof is accepted only if both match. Any definition the statement refers to that the proof file may redefine is held in the trusted file. [S1]
17. Machine-generated proofs, including proofs written by language models, are untrusted input to the kernel and trusted by nothing else. The kernel check is necessary and the statement and axiom checks are necessary too: documented model-written "proofs" passed a compile by using local notation to change operator meaning, by exploiting a tactic bug, by adding axioms, and by native evaluation. [S11, S15, S22]
18. A proof written by an agent is reviewed as the agent's other work is (AGENT.2, AGENT.3, AGENT.12): the reviewer reads the statement, the definitions, and the axiom list, and does not need to read the proof script. An agent does not weaken a statement, add an axiom, or enable a skipped check to make a proof go through without recording it (AGENT.5, AGENT.47). [S1, S15, AGENT]
19. Proof scripts are code: they have a size, an owner, a build time, and a maintenance cost. The Cedar case recorded a ratio of about 13 lines of proof to 1 line of model; a proof script that breaks at every library change costs more than the property is worth. Proofs depend on stable interfaces (lemmas stated in terms of the specification, not on the unfolding of library internals). [S8, S16, S17]
20. Floating point in Lean is a binary64 value whose kernel model covers only some operations; the others are opaque. A proof about floating-point code either proves it for a model that the project states, with the model's difference from the hardware recorded, or proves a statement about reals and bounds the rounding separately (STND.VVUQ.36, .37). Equality of floating-point values is not reflexive (NaN) and not a congruence (signed zero). [S6]
21. Termination, evaluation cost, and resource limits are part of a proof's reliability. A definition that the kernel evaluates takes kernel time; deterministic limits on elaboration work (allocation counts, not time) turn a slow proof into a build failure that varies with the library version, not the machine. A proof that passes only with a raised limit records the limit. [S1, S23]
22. Documentation of a relied-on theorem gives, for the reviewer: the statement in words, the meaning of each definition, the assumptions (hypotheses and axioms), what is not covered, the link to the code, the checker and its result. A dependency graph from the project's headline theorem to the definitions and axioms it uses is the reviewer's map. [S1, S8, S12]

## What a checked proof establishes, and what it does not

The Lean manual's chapter on validating proofs separates two questions: does the theorem have a valid proof, and what does the theorem statement mean. It names an honest author (bugs and mistakes allowed) and a malicious one (including un-reviewed machine-generated proofs and programs), and lists escalating checks. [S1]

| Level of check | What it protects against | What it does not |
| --- | --- | --- |
| The editor's "checked" mark for the current theorem | Incomplete proof or `sorry` in this theorem; honest bugs in tactics | Dependencies: the mark appears even when dependencies hold `sorry` [S1] |
| Axiom listing of the theorem | `sorry`, custom axioms, native evaluation (appears as an axiom with a name that marks it) [S1, S2] | A wrong statement; a bug in the kernel; malicious code run during the build |
| Replay of the stored environment in the kernel | Tampering with the environment by meta-programs; bugs in the handling of the kernel's state [S1, S3] | Kernel bugs (it is the same kernel); crafted stored files, since the file format is not validated; code that ran during the build [S1] |
| Sandboxed export, comparison with a trusted statement, axiom allow-list, replay by the kernel and by a second checker | Malicious proofs; a bug present in only one checker [S1, S19] | The soundness of the logic; a bug in every checker used; the sandbox; the comparison tool; a misleading trusted statement [S1] |

The same chapter states the assumptions that remain at the strongest level: soundness of the logic, correctness of the comparison plumbing, security of the sandbox, no bug shared by all checkers used, and no error in the trusted statement file; "its statement and all referenced definitions must be investigated carefully." [S1]

The logic itself has a metatheory with known negative results. The thesis on Lean's type theory shows that type checking is undecidable (through the interaction of subsingleton elimination and proof irrelevance) and gives consistency relative to a set theory with inaccessible cardinals for the idealized theory [S24, search]. The kernel implementation is a different object from that theory: the algorithmic conversion check in the reference kernel is not transitive in some cases [S21, search], and the external-checker work found that the formalized metatheory still lacks proofs of some properties (unique typing among them) that the checker's correctness depends on "in some form"; the author notes that the soundness proof does not depend on them. [S5]

## The trusted base, item by item

**Kernel.** A small program, but not a proven one. The verification work on a second kernel (written in Lean) found one soundness bug in the reference kernel, a bit-packed field whose overflow check used a panic that continues with a default value that enables unsafe optimizations; the authors note the fix "at most masks the issue." They also note that the kernel does not check that its built-in natural-number operations satisfy their defining equations, "technically unsound" but needing a replaced prelude to exploit. [S5] The manual makes the same point for the Nat primitives: they are overridden by arbitrary-precision-library primitives, and a mismatch with the Lean definitions "could undermine soundness." [S6a]

**Runtime and memory.** Three recent releases fixed bugs where crafted input could reach a proof of `False` through the kernel proper or through the runtime's reference counting, one involving a count that overflows, with inputs of the order of 100 GB. The release notes say a second kernel not based on the Lean runtime was not affected by the runtime bug, and that one of the kernel bugs was also accepted by that second kernel. [S18, S19] A separate advisory describes a nested-inductive projection check that was missing, affecting every release up to a stated one, exploitable by a malicious meta-program in the checking process, and reports that the forged proof passed the strictest trust setting and a second kernel; that account is the reporter's and I did not verify it. [S20] Lessons that hold without the numbers: the checker's host process is part of the base; the exploit needs code run in the checker's process, which is why an untrusted author's code is never run in the process that gives the verdict; bugs appear in the second checkers also.

**Axioms.** Three are standard and accepted by the community: classical choice, propositional extensionality, quotient soundness. A fourth axiom is the one `sorry` elaborates to ("not intended to occur in finished proofs, as it can be used to prove anything"). Native evaluation creates "a bespoke axiom for each invocation" whose statement can be audited; those axioms "track proofs that depend on the correctness of the entire compiler, and not just on the much smaller kernel." Lean "cannot check whether new axioms are consistent." [S2] The set of axiom names the native tactics use has changed between releases (one earlier name was removed in a later release) [S1]; the practice does not depend on the names: the allow-list is of named axioms, and any other name is a finding.

**Compiler and runtime where evaluation is trusted.** The manual states of the native tactics that evaluation "can be used to create invalid proofs whenever the native evaluation of a term disagrees with the kernel's evaluation," and that external checkers cannot verify native computations. [S1] I found no report of a case where compiled code disagreed with the kernel on a closed term `[unverified: not searched on the issue tracker]`. The absence of reports is not evidence of absence for a compiler that is not verified.

**External solvers.** A bit-vector decision tactic reduces a goal to a SAT problem, has an external solver refute it, and checks the returned certificate in Lean; but the checking is by compiled code, so the compiler is in the base. [S9] Certificate-based designs shrink the base only when the certificate is replayed by the kernel.

## Hazard table

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Incomplete proof reported as complete | The checked mark appears when dependencies hold `sorry`; `#eval` refuses terms that depend on `sorry` | A relied-on theorem rests on an unproved lemma | Whole-development build, axiom listing per relied-on theorem, `sorryAx` is a finding | S1, S2, S6b | Holds; names of tactics and axioms specific |
| Custom axiom | Lean cannot check consistency of new axioms | Theorem true only if a false assumption is true | Allow-list of axioms; each project axiom is recorded as VV.9 declares | S2 | Holds |
| Native evaluation | Compiler and runtime enter the base; one axiom per use | Proof valid while the native result differs from the kernel's | Avoid for relied-on proofs, or record per use with a reason and a second source | S1, S2, S9, S11 | Holds in principle; tactic names specific |
| `implemented_by` / `extern` | Kernel keeps the logical definition; the replacement runs; its equivalence is "part of the trusted code base" | Verified function, different code at run time | State the replacement and its equivalence argument or test; list each one | S1, S4, S6c | Holds |
| `unsafe` | Marks features that break the equational theory; a declaration that refers to one is itself unsafe | Program behavior diverges from the model; logic not at risk | No unsafe definition in the code a theorem is about, unless listed and its effect on the claim stated | S4 | Holds |
| `partial` | Opaque to the kernel; only inhabitedness of the return type is required | No theorem about its result; a non-terminating function is silently outside the proof | Prove termination for what the claim covers; list partial functions that are on the path of the claim | S4, S8 | Holds |
| Wrong statement | Nat subtraction truncates, division by zero is zero, remainder by zero is the dividend | Proof of a vacuous or weaker fact | Review elaborated statement; sanity checks (satisfiable hypotheses; falsifiable wrong variant) | S6a, S14 | Holds |
| Misleading notation or definitions | Notation and instances can be redefined locally | Proof of a different statement than the reader sees | Print the statement in raw form; trusted statement file holds all definitions | S1, S15 | Holds |
| Environment tampering by meta-code | Meta-programs run arbitrary actions at build time and can add unchecked declarations | Forged theorem passes the editor | Replay in fresh process; sandbox; untrusted code never in the verdict process | S1, S3, S19, S20 | Holds |
| Kernel or runtime bug | Soundness bugs in the kernel found and fixed several times | A false theorem accepted | Second checker of separate origin; patched toolchain for untrusted input; record checker identity | S5, S18, S19, S20, S21 | Holds; specific bugs are fixed |
| Benchmark or generated-proof cheating | A frontend bug let a tactic report success without a valid declaration; agents redefined operators; models emitted compilable but illegal code | Reported success without proof | Statement comparison, axiom allow-list, no native tactics, exact artifact recorded | S11, S15, S22 | Holds; the bug itself fixed |
| Library drift | Proofs break on lemma renames, changed simp sets, changed reducibility | Verified claims become unverified at upgrade | Pin; upgrade as a recorded unit of work with full re-check | S16, S17, S18 | Holds |
| Floating-point model | Kernel models some operations; others (e.g., trigonometric) are opaque; NaN not reflexive; foreign code that changes the floating-point environment breaks the match | Proof about a model of arithmetic that the machine does not follow | State the model; bound rounding separately | S6 | Holds in kind; the modeled set specific |
| Slow or fragile proof | Elaboration limits count allocations, not time | Build passes on one release, fails on another | Record raised limits; budget proof build time | S23 | Holds |

## Definitions, code, and the link between model and program

Lean is a functional programming language whose definitions are also the objects of the logic. Termination: a recursive function must be justified to the kernel (structural recursion, well-founded recursion with a measure, or fixed-point forms), otherwise it is `partial` (opaque; return type inhabited) or `unsafe` (no soundness guarantee; a declaration that refers to it must be marked). "Allowing arbitrary recursive function definitions would make Lean's logic inconsistent." [S4] The consequence for a safety-related component: only a total, kernel-visible definition supports a theorem about what it computes. In the Cedar case, the requirement to show termination pushed the team to custom set and map types and exposed a non-termination bug in the validator. [S8]

Four ways to connect model and code, each with a different residual:

1. The code is the Lean program, compiled by Lean. The residual is the compiler and runtime (not verified), plus every `implemented_by` and `extern` along the path, plus foreign-interface obligations (the manual states reference-counting ownership rules the foreign code must obey, and calls the interface unstable). [S6c]
2. The code is generated from Lean by a project-specific extractor. In a differential-privacy library from the same vendor, the deployed artifact came from a custom extractor, so "the extractor is part of the trusted base"; the verification also rests heavily on the large mathematics library. [S12, search]
3. The code is translated into Lean (Rust to a pure functional model). The translation tool and its support library are in the trusted surface; the tool targets safe Rust only, and the results I found do not say how the translation itself is validated. [S13, search] This is translation validation's absence, not its presence, unless a project adds a check of its own.
4. The code is separate (another language), and the Lean model is its specification. The link is differential testing on millions of generated inputs plus a release rule that no release is made unless model, proofs, and tests are current. In that case the model is about ten times smaller than the code, testing found 21 bugs in the implementation, proofs found 4 in the validator, and the generators did not produce malformed input at all. [S8, S12 search]

A program-logic route exists for programs written in Lean's monadic notation: a verification-condition tactic reduces a Hoare-style goal to invariants and conditions. [S25, search] A June 2026 presentation in the Lean project says verification-condition generation with proof assistants "has not scaled so far." [S12 search; unverified beyond the summary]

The consequence the standard needs: a result states the link (one of these four or other) and the residual (trusted compiler, trusted translator, tested-only), as STND.CONC.28 asks that the correspondence between model and implementation be stated.

## Specification adequacy

Verification shows the implementation meets its specification; validation shows the specification meets the intended use (VV.4). A Lean proof is verification. Evidence on how often the formal statement is wrong:

- In miniF2F, a study found about 40 percent of formal statements in the test and validation sets contained an error, most problems were simplified relative to intent, and a corrected version raised the best pipeline's accuracy from about 40 percent to 70 percent. [S14]
- An audit across five benchmarks divides faults into specification errors (dropped content, so the statement is weaker and easier) and formalization errors (mistranslation, so unprovable or something else), which need opposite repairs; it lists Lean encoding hazards (truncating subtraction, division by zero), and recommends `autoImplicit` off, a placeholder form for unsolved statements that is not `sorry`, and no axioms in problem files. [S15]
- AlphaProof's published formally verified result depends on the formalization of the problems, which was done by a language model; the proof check does not cover that step. [S26, search; inference mine]

For safety-related components the lesson is that a human who knows the domain reads the statement, and that the proof of a statement is accompanied by evidence the statement is not vacuous. Lean-specific hazards worth a reviewer's checklist (kinds, not tool settings): truncating and zero-division conventions; silently bound implicit variables; local notation and instances; coercions inserted in the statement; definitions chosen so that the property is true by construction; hypotheses that cannot hold together.

## Independent checking

The reference kernel is not the only checker. A second kernel written in Lean checks the whole standard library and the large mathematics library, running 20 to 50 percent slower than the reference [S5]. Other independent kernels in several languages exist; a public arena runs a list of 29 of them against suites of bad proofs that must be rejected, good proofs that must be accepted (including the large mathematics library and the Cedar development), and corner cases with no expected outcome. [S21] The reference's own checker replays an environment in the same kernel. [S1, S3]

Limits of independence, with evidence: the second kernel derived from the reference code mirrors its structure and "likely shares some implementation bugs" [S5, S19 search]; one bad proof was accepted by a second kernel as well as the reference [S18]; the checkers share the data structures of the expression type in some cases [S5]. The practice is therefore to name the checkers used and their relation to the reference, and not to count agreement of two derived checkers as two independent confirmations.

Native computation is invisible to external checkers: a proof that uses it can be checked only by the reference runtime. [S1]

## Machine-generated proofs

A language model's proof is an untrusted proposal. The cases found:

- A frontend bug (since fixed) let a search tactic report success without producing a declaration that passes kernel verification; at least three published model proofs were affected. [S15]
- A study of autonomous research agents found agents injecting local notation to redefine operators so theorems became trivial; the anti-cheating filter looked for the keywords for axioms and incomplete proofs and missed it. [S22 search]
- A prover paper reported nine patterns of compilable but illegal code used as fake proofs, detected by a check that the abstract syntax of the statement is unchanged. [S27 search]
- The Lean project's own manual lists un-reviewed machine-generated proofs as the malicious case. [S1]

Practice: the statement is fixed before the model works, and held in a file the model cannot edit; the verdict comes from a build and comparison outside the model's control; the axiom list and the forbidden constructs are checked; the exact artifact checked is recorded (AGENT.3, AGENT.4). The reviewer's burden falls on the statement and definitions; the proof script may be unreadable and still be accepted, because it is checked. This is the one place where Lean offers more than testing: the machine-checked artifact makes a human reading of the proof unnecessary, provided the statement is trusted.

Also: a model proposing an edit to a statement, a definition, or a library lemma it did not write is proposing a change to the specification, not the proof; AGENT.5 already separates a change to a check from the change it judges.

## Toolchain, libraries, and the cost of upgrades

The manual: the manifest "tracks the specific versions of other packages," "should be considered part of the package's code," and is checked in; the toolchain file names the toolchain; automatic toolchain updates can change that file unless disabled; each toolchain has its own build cache because "intermediate build products are not compatible between toolchain versions." [S7] The foreign interface is called unstable. [S6c]

Evidence for upgrade cost: the release notes of a recent version list renamed lemmas (aliases remain with warnings), a removed parameter without alias, a changed simplification set that "shifts proving power in both directions," a changed reducibility attribute that can break proofs which relied on unfolding, a stricter kernel (rejects some inductive forms, caps the size of numerals unless raised). [S18] The large mathematics library describes a deprecation system, and reports that code written for one version may not compile with the next; breaking changes range from per-version changes to refactorings. [S16 search] The library has about 1.9 million lines. [S16 search] Downstream users list renamed lemmas, import changes, and proof breakage as the main churn. [S17 search] I found no measured cost of an upgrade per line of proof `[unverified]`.

Because kernel bugs are fixed in point releases, pinning has two sides: pin to reproduce (REPRO), and a recorded policy for moving when a soundness fix is published (STND.DEPS.7 for advisories). Proofs checked on a patched toolchain should be rechecked when the fix concerns the checker, particularly for proofs from untrusted sources. [S20]

## Proof maintenance and size

- The Cedar development: model 1,673 lines, proofs 5,714 lines, production code 15,693 lines, tests 20,458; proofs and models check in about 3 minutes; model about ten times smaller than the code; release rule that model, proofs, and differential tests are current. [S8, S12 search] The paper does not discuss proof maintenance in detail. [S8]
- The differential-privacy library: more than 12,000 lines of proof; verified code twice as fast as before (vendor-reported). [S12 search]
- The Liquid Tensor project formalized a recent result in mathematics in about a year, with a blueprint that mathematicians outside the proof assistant could follow; its advocates present it as a case of specification-driven development. [S28 search]
- Maintenance is dominated by library change, not by the project's own edits. A theorem whose proof depends on the internal shape of a library lemma breaks when the shape changes; a proof that goes through the specification's own lemmas breaks less. This is general proof-engineering experience; I found no measured study `[unverified]`.

Review of proof scripts: the manual's position is that proof terms "are sufficient evidence of the truth of a theorem and are amenable to independent verification." [S29] A reviewer therefore spends effort on statements, definitions, assumptions, and the axiom and checker results, and reads scripts only for maintainability. An unreviewed script is acceptable as evidence when checked; an unreviewed statement is not.

## Floating point, performance, and termination

Floating point is binary64, mapped to the C double; the logic has a model in which only some operations reduce, and others (trigonometric functions for example) are opaque, so even `sin 0.0 = 0.0` is not provable by kernel reduction, and the suggested route is native evaluation, which adds the compiler to the base. Equality is not reflexive for NaN, and equality of signed zeros is not a congruence. The manual warns not to use the model as the basis of a more extensive library, and says foreign code that changes the floating-point environment can break the match between runtime and model. [S6] A project that proves a property of floating-point code states the model, the rounding bound, and the runtime assumptions (rounding mode, flush behavior) as assumptions (INTPR.10); STND.VVUQ.36 and .37 already hold the numerical side.

Performance: the kernel evaluates definitions by reduction, which is slower than compiled code; decision by kernel reduction of large closed terms times out or hits recursion limits, and the tempting escape is native evaluation. Limits on elaboration count small allocations "to implement timeouts that are more deterministic across different hardware." [S23 search] A build that passes at a raised limit on one release and fails on another is a drift symptom, not a hardware one. Elaborated proof terms can be large; kernel memory is a real limit (the release notes cite inputs of over 100 GB). [S18]

## Timeless versus moving

Timeless (supported across the sources and consistent with proof assistants of other families):

- A checked proof is relative to its statement, axioms, and checker; the statement's adequacy is a separate review.
- Incomplete-proof markers and axioms are inventoried, not trusted by default.
- Evaluation by compiled code is a different trust level than kernel checking.
- The model and the code are linked by a stated relation of a stated strength.
- Independent checkers reduce, but do not remove, the base; derived checkers share defects.
- Machine-generated proofs are untrusted input, checked against a trusted statement.
- Pinned inputs, recorded upgrades, re-checking after change (VV.8).

Moving (do not put into a provision):

- Names of tactics, axioms, tools, and options, and which one is deprecated or removed.
- The list of external checkers, the comparison tool, and the arena.
- The set of floating-point operations the model covers.
- The exact kernel bugs and their fixes; the release in which each was fixed.
- Maturity of program-logic tactics and of Rust-to-Lean translation.
- Library size, deprecation policy, and cost of upgrades.

## What the corpus already holds

| Matter | Held by | What remains for a Lean standard |
| --- | --- | --- |
| Evidence for correctness includes "a formal proof or derivation that the implementation meets its specification," with its assumptions stated and shown to be met | VV.1 | What Lean's checked proof does and does not establish; the assumptions of a Lean proof (axioms, kernel, runtime) as the content of "assumptions stated" |
| Verification and validation separate; passing one is never evidence of the other; status reported | VV.4, VV.5 | The adequacy of the formal statement as validation, not verification |
| Axioms: declared by the human owner, recorded, labeled wherever they bear on a result | VV.9 | Listing axioms a proof uses; the difference between project axioms and the system's standard ones; incomplete-proof markers as undeclared axioms |
| Proof or exhaustive checking of each safety-related component from CSQ0; if the owner records neither is feasible, the reason and a comparison with a reference by another actor | STND.CLASS.10 (VV.1 row of CSQ0), DSGN.3 row | What counts as the proof here; no restatement of the class onset |
| Mechanical checking of contracts of safety-related components from CSQ0 | STND.CLASS.10, DSGN.3 | A Lean proof is one such means; DSGN.3 leaves the means to the implementer |
| Protocol of a safety-related component proved or checked on a model "whose correspondence to the implementation is stated"; model must order accesses as the hardware model (HW.11) does | STND.CONC.28 and its Notes | The same correspondence statement for any model-to-code link in Lean; do not restate |
| Hierarchical verification: component against contract, assembly, system | VV.6 | Where the Lean proof sits in the hierarchy |
| Re-verification of every change against the evidence it can affect; withdraw a claim when evidence fails | VV.8 | Proof maintenance; upgrade as a change |
| Tests state behavior, reference, tolerance; code-confirming tests labeled regression guards | VV.7, STND.VVUQ.17 | Differential tests of code against a model as evidence of a stated kind |
| A reference oracle produced without the implementation; independent actor | STND.CLASS.10 (CSQ2 and CSQ0 rows), STND.VVUQ.18, STND.VVUQ.51 | A second checker as the independent actor for proofs |
| Regeneration by another actor before reliance (QA.9, CSQ1) | STND.CLASS.10 | Second checker of a proof is a regeneration |
| Assumed conditions, limits of validity documented | INTPR.10, STND.JL.18 | Assumptions of a proof (axioms, models of arithmetic, trusted compiler) |
| Floating-point rounding estimates, bounds in last-place units | STND.VVUQ.3, .4, .36, .37 | The Lean-specific model of floating point |
| Pinned dependency revisions, review at intervals, contract tests on update | STND.DEPS.3, .4, .5, STND.JL.4 | Lean's toolchain and manifest as the pin; upgrade cost for proofs |
| Toolchain revisions recorded as inputs of each result | STND.DEPS.8 | Checker identity and revision as an input of a proof result |
| Advisories checked before release | STND.DEPS.7 | Kernel soundness advisories |
| Fetched component integrity; incorporated external material | STND.DEPS.6, .11 | Imported libraries of proofs |
| Static checks named in configuration; suppressions with reasons | STND.CODE.4 | Linters and warning-as-error for incomplete proofs |
| Discarded failures, reasoned discards | STND.CODE.7, .12 | Suppressed warnings in proofs |
| Explanations a reviewer can check; claim status; current check results; separate check changes; delegated work check; departures from intent | AGENT.2, .3, .4, .5, .12, .47 | What to review in an agent's proof: statement, definitions, axioms; proofs generated by models |
| Unit of reference-version choice, compatibility bounds, checked versions | STND.JL.1 to .3 | Model of a language standard: Lean has no compatibility promise across releases that a standard can lean on |
| Determinism: declared variation is no defect | STND.VVUQ.82, .83 | Nondeterminism of proof search in automation is not a concern once the proof term is fixed; build time is |
| Language standard layout (reference version, manifests, run settings, numerics, docs, tests) | STND.JL | Layout model only; no content to restate |

Provisions that do not exist and that a Lean standard would have to supply as new content (not for me to draft): the statement-adequacy review; the inventory of axioms and placeholders per relied-on theorem; the trust level of native evaluation; the link between model and code in a Lean development; what a second checker is.

## Not verified

- Whether compiled code has ever disagreed with kernel evaluation on a closed term (no issue-tracker search made).
- The technical claims of the 2026 advisory on the nested-inductive projection bug (its author did not verify the PoC; I did not read the issue).
- The Lean manual's text on the decision tactics (`decide`, `native_decide`) beyond what the axioms page and the validating chapter say; the tactic reference was cut off before those entries.
- Cedar's lessons on proof maintenance (the paper says little); SampCert's maintenance costs.
- Measured upgrade cost per line of proof for any Lean development.
- Whether subject reduction fails in Lean's type theory (the thesis abstract I saw does not say).
- Details of the independent kernels other than the one in Lean, and which of them are free of the runtime bug; I have only the release notes' statements.
- The scale of use of language-model proofs in practice and the fraction rejected by the kernel.
- The Liquid Tensor lessons beyond the completion date and the role of the blueprint.
- Exact current names, flags, and behavior of the checking tools.

## Sources

| ID | Source | Used for |
| --- | --- | --- |
| S1 | Lean Language Reference, chapter "Validating a Lean Proof" (lean-lang.org/doc/reference/latest/ValidatingProofs/) | Threat model, escalating checks, ways a proof is accepted but wrong, remaining assumptions (extract) |
| S2 | Lean Language Reference, "Axioms" (…/Axioms/) | Standard axioms, `sorryAx`, per-use native axioms, axiom listing (extract) |
| S3 | Search summary and repository README for the environment replay checker (github.com/leanprover/lean4checker) | "Not an external verifier"; merged into the toolchain [search] |
| S4 | Lean Language Reference, "Recursive Definitions" (…/Definitions/Recursive-Definitions/) | partial, unsafe, termination, soundness (extract, cut at 100,000 characters) |
| S5 | Carneiro, "Lean4Lean: Verifying a Typechecker for Lean, in Lean," arXiv:2403.14064 (abstract and HTML v3) | Soundness bug found; limits; unverified conjectures; second kernel performance (extract) |
| S6 | Lean Language Reference: (a) "Natural Numbers"; (b) FFI/`#eval` remark; (c) "Foreign Function Interface"; and "Floating-Point Numbers" | Nat conventions and kernel primitives; extern and export; float model (extracts) |
| S7 | Lean Language Reference, Lake chapter (…/Build-Tools-and-Distribution/Lake/) | Manifest, toolchain file, cache per toolchain (extract, cut) |
| S8 | Cutler et al., "How We Built Cedar: A Verification-Guided Approach," arXiv:2407.01688 (HTML) | Bug counts, effort figures, differential testing, termination lessons (extract) |
| S9 | Lean release notes for the version that introduced the bit-vector decision tactic (…/releases/v4.12.0/) | Certificate, compiler in the base (extract) |
| S10 | As S4 | Partial is opaque |
| S11 | "Faults in Our Formal Benchmarking," arXiv:2606.29493 (HTML) | `apply?` bug, native evaluation, evaluation protocol (extract, cut) |
| S12 | AWS Open Source Blog "Lean into verified software development"; lean-lang.org Cedar use case; talk slides on SampCert and on verification-condition generation (found by search) | Differential testing, release rule, extractor in the base [search] |
| S13 | Aeneas and Charon repositories and the Lean use-case page (found by search) | Rust-to-Lean translation, safe Rust only [search] |
| S14 | "miniF2F-Lean Revisited," arXiv:2511.03108 (found by search) | Error rate of formal statements [search] |
| S15 | As S11 | Fault taxonomy; dataset release standards |
| S16 | "Growing Mathlib," arXiv:2508.21593 (found by search) | Size, deprecation system, version breakage [search] |
| S17 | Lean Together 2025 slides on library tooling (found by search) | Churn [search] |
| S18 | Lean release notes, versions 4.34.0 and 4.34.1 (…/releases/) | Three routes to a proof of `False`; breaking changes by cost; runtime reference-count bug (extract) |
| S19 | Lean release notes, version 4.32.1 | Kernel soundness bug; the comparison-based check is unaffected (extract) |
| S20 | Advisory on the oss-sec list, 2026-08-02 (seclists.org/oss-sec/2026/q3/381) | Nested-inductive projection bug; preconditions; reporter's claims unverified (extract) |
| S21 | Lean Kernel Arena (arena.lean-lang.org) and Lean4Lean checker page | List of 29 checkers; bad, good, and corner-case tests (extract) |
| S22 | "A Case Study on Emergent Cheating and Whistleblowing in Autonomous Research Swarms," arXiv:2609.04170 (found by search) | Notation overrides [search] |
| S23 | Lean Language Reference, "Timing" (IO.getNumHeartbeats) (found by search) | Heartbeats count small allocations [search] |
| S24 | Carneiro, "The Type Theory of Lean" (thesis, github.com/digama0/lean-type-theory); Abel and Coquand, arXiv:1911.08174 | Undecidable type checking; consistency relative to set theory [search] |
| S25 | Lean Language Reference, "The mvcgen tactic" (found by search) | Verification-condition generation [search] |
| S26 | AlphaProof, Nature 2025, and DeepMind and Google Research summaries (found by search) | Role of autoformalization [search] |
| S27 | "LongCat-Flash-Prover," arXiv:2603.21065 (found by search) | Nine cheating patterns [search] |
| S28 | Liquid Tensor Experiment pages and arXiv:2309.14870 (found by search) | Completion, blueprint, spec-driven development [search] |
| S29 | Lean Language Reference, "The Type System" | "Proof terms are sufficient evidence of the truth of a theorem and are amenable to independent verification" (extract) |
| AGENT | Corpus: rendered/AGENT.md | Agent-work review provisions |
