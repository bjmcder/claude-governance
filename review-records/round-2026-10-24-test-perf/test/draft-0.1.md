# Testing methods standard (STND.TEST) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 143 (2026-10-24). This reading copy is composed from the per-provision files in STND/TEST/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the method of testing that holds for every language, test framework, and build tool: how the work structures its tests, selects the tests that a change runs, reuses verdicts, and reads the verdicts that its tests give. RSRC.11 and RSRC.12 hold the obligation to run the smallest set of checks that establishes the evidence that a change requires and to defer the rest to the latest decision point at which its result is still needed; this standard gives the method by which the work meets them, and adds to VV, QA, STND.CODE, STND.WPROC, and STND.BUILD only what that method makes necessary. It covers the structure of the suite (STND.TEST.1 and STND.TEST.2); the selection of tests, its widening with the integration depth, the full suite, the reuse of verdicts, and the record of a run (STND.TEST.3 to STND.TEST.9); runs between merges (STND.TEST.10); the reading of verdicts (STND.TEST.11 to STND.TEST.14); oracles, generated inputs, adequacy measures, and acceptance tests (STND.TEST.15 to STND.TEST.18); and tests changed with the code that they judge (STND.TEST.19).

No provision binds. Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The honest report of verdicts binds at every class through PRIME.2, VV.7, AGENT.4, AGENT.5, and AGENT.47, and this standard adds nothing to that floor. The standard is agnostic of language, test framework, build tool, and vendor: its provisions name none of them, and no granularity of analysis, tier size, or threshold (GOV.18). The comparisons, tolerances, and stochastic tests of numerical results belong to STND.VVUQ.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Acceptance criteria, Component, Reference, Regression guard, Test, and Unit of work have the meanings that the Lexicon gives them. Repository configuration and Execution setting have the meanings that STND.CODE gives them; Branch, Merge, Main line, and Development line have the meanings that STND.WPROC gives them; Build description, Build configuration, Toolchain, and Generated file have the meanings that STND.BUILD gives them; and Integrity digest has the meaning that STND.DEPS gives it, used here also of a verdict input. The verdict of a test is whether it passes or fails on one run.

| Term | Definition |
| --- | --- |
| Full suite | Every test of the work that the repository configuration states, in every tier. |
| Tier | A class of the tests of the work that the repository configuration states by a bound on the time and the resources that each of its tests uses and by the reach of what each exercises, from code in one process to code on more than one host. |
| Verdict input | Of a test: each file, datum, tool, execution setting, variable of the environment, random seed, and other test whose change is able to change its verdict, the code that it exercises, its harness, and its fixtures included. |
| Selection | The tests that one run of tests runs, drawn from the full suite. |
| Selection rule | The procedure, stated in the repository configuration under a revision, by which a selection is derived from a change and from the verdict inputs of the tests. |
| Integration depth | Of a merge, the number of merges by which a change on its target branch reaches the development line: 0 for a merge into the development line, 1 for a merge into a branch made from the development line, and one more for each further branch below. |
| Verdict key | Of a verdict of a test, the record of the revision or the integrity digest of each verdict input of the test at the run that gave the verdict. |
| Flaky test | A test whose verdict differs between runs under one verdict key. |
| Quarantine | The state of a flaky test on whose verdict no merge and no release relies, for a recorded bound. |
| Partial oracle | A check that each correct output of a test meets and that at least one incorrect output fails, and that does not give the expected output: a property of each output, a relation between the outputs for related inputs, or the agreement of independent implementations. |
| Adequacy measure | A measure of how thoroughly a set of tests exercises the code or detects changes to it, the coverage of the code of a stated kind and the score of a mutation analysis among them. |
| Acceptance test | A test whose stated behavior is an acceptance criterion of a unit of work, or a part of one. |

## Notes

The provisions rest on what the literature of regression testing and of test verdicts has shown for decades and what holds across languages and tools: a selection is safe when it holds every test whose verdict the change is able to alter, and only under controlled conditions; declared dependencies give a conservative reach and observed ones narrow it, while every input that the observer does not see widens it; the cost of testing grows with the rate of change times the size of the suite; a verdict is reusable only under a key that holds every input; dependent tests give verdicts that change with order; a rerun turns an intermittent defect green; the oracle problem has weaker remedies, invariants, metamorphic relations, and differential comparison among them; and coverage shows what no test exercised, not what an assertion constrains (research/test-notes/t1-selection-and-budget.md and research/test-notes/t2-tests-and-verdicts.md, "Timeless versus moving"). The figures that the notes quote come from studies of particular languages, companies, and benchmarks, are examples and not norms, and no provision adopts them. Several sources were read as extracts that a retrieval tool wrote, and the notes mark what they did not confirm.

The custodian decided on 2026-10-24 that this standard sits at LVL2 with every provision a default, that the obligation stays with RSRC.11 and RSRC.12, which bind at LVL0, and that the evaluation of performance, the regression guard on time included, belongs to the performance evaluation standard drafted beside this one. The custodian's concern is that agents run the full suite by habit, at a cost in time, power, and other budgets, where a smaller set of tests establishes the correctness of the code before it merges into the next unit up, so that a subfeature that merges into a feature carries a lighter burden than a merge that releases. On 2026-10-25 the custodian ruled, in the terms of STND.WPROC, that the full suite runs before each advance of the main line, which is a release; that merges into the development line run a wider selection of the affected tests; that the full suite also runs on the development line at a cadence that the project states, which audits the selection; and that merges below the development line run selections that widen with the level of integration. STND.TEST.5 and STND.TEST.6 hold that ruling.

The standard cites what the corpus already holds and does not restate it (GOV.31). RSRC.11 asks for the smallest set of checks that establishes the evidence, with broader checking where the reach of the change requires it or at release; RSRC.12 defers verification to the latest decision point at which its result is needed and never lets deferral become omission; VV.8 re-verifies each change against the evidence that it is able to affect, identified from the record. STND.WPROC.9 has each check that the change is able to affect pass on the branch as updated under STND.WPROC.8, other than a check deferred to the release and recorded in the unit record, and STND.WPROC.13 and STND.WPROC.14 carry the skipped, disabled, and weakened checks and the outcome of the checks run to the release record. VV.6 gives the levels of verification and localizes a failure to the lowest level at which it is detectable, VV.7 labels a regression guard, STND.CODE.8 adds a test for each fix, and STND.CODE.9 asks the same verdict on every run against one revision and its recorded inputs, its seeds included. RSRC.7 admits reuse only where it preserves correctness and reproducibility, and STND.BUILD.23 keys a build cache on every input of a step; STND.BUILD.1, STND.BUILD.4, and STND.BUILD.11 declare the inputs, generators, and settings from which a selection derives its reach, and STND.BUILD.26 states the build configurations that the checks build and test. QA.4 tracks defects, QA.6 restores a broken check, and RSRC.3 and AGENT.24 record the time and cost of each run and each unit, from which the cost of a run of the full suite is known. STND.VVUQ.17 treats the failure of a numerical regression guard, STND.VVUQ.18 and NUMER.6 order the reference oracles of numerical methods, STND.VVUQ.64 and NUMER.26 hold fixed-seed and fresh-seed tests and forbid reseeding to pass, STND.VVUQ.78 is the numerical instance of RSRC.11 and RSRC.12, and STND.VVUQ.82 and STND.VVUQ.83 keep a declared variation within the agreement of its acceptance criterion from being a defect.

A tier is stated by what its tests use: tests that run in one process without blocking calls, tests that use local processes and threads, and tests that need more than one host form the pattern of one published scheme, whose sizes and time limits are that company's policy (t1, H2) (STND.TEST.1). A pass of the fastest tier is not a pass of the suite, and a change at a seam between components is not covered by that tier alone. The level of VV.6 at which a test verifies is what lets a failure be localized and lets a selection draw the tests of an assembly. Selection by the declared graph of the build is safe because a test sees only what it declares, and it selects every test above a change to a shared root; observed dependencies at the level of files narrow it, and finer analysis missed more in the studies read, through reflection and excluded libraries (t1, H1) (STND.TEST.2). A record of what a test read goes stale as the code changes, which is why it carries its revision (t1, H1, S15). The standard names no granularity, which is the project's choice within its budget.

A selection that holds every test whose verdict the change is able to alter is safe under controlled conditions, the same environment, inputs, and seeds, and no procedure finds exactly the tests that would fail (t1, answer 1) (STND.TEST.3). A selection that rests on a prediction, a window of recent failures, or a distance in the dependency graph is not safe; in the documented case it relied on a full run every few hours, and the second sentence of STND.TEST.3 records what it omits and where the omission is covered (t1, answers 17 and 18). The rows of STND.TEST.4 are the inputs that the studies show a selector to miss: a setting or a tool not registered as an input, files that are not source, fixtures and generators without a dependency edge, code reached across a language or a process, and the selector itself, of which three tools had 27 defects in one study (t1, H1, S5, S6, S7, S20). A module-level selector selected every module in 65 percent of commits until a reviewed list excluded the kinds of file that cannot change a verdict, which is the list that the last row of the table admits (t1, H1, S6). New tests, recently failing tests, and tests without a current record of what they read run unconditionally in the tools described (t1, answer 6).

The integration depth turns the custodian's level of integration into a number that a reader of the history decides. A merge into a feature far from the development line draws on the fastest tiers; each step toward the development line draws on the tiers of the step below and on more; and a merge into the development line draws on every tier, so that the selection there is wider than below it while still a selection (STND.TEST.5). The change that a merge brings grows as it moves up, because it holds the merged work of each unit below, and STND.WPROC.9 already selects for the whole of it on the branch as updated. A test that the change is able to affect, in a tier that the depth of a merge does not draw on, runs at the first merge nearer the development line whose depth draws on its tier, and the record of STND.TEST.3 states it; STND.WPROC.9 excepts only a check deferred to the release, and this deferral to a nearer merge rests on RSRC.12 in the same way. This mapping of staged practice at two large companies and of the two-phase studies onto the branch hierarchy of STND.WPROC is a synthesis and not a published rule; both companies abandoned a full run for each change because its cost grew with the rate of change times the size of the suite (t1, answer 9 and the finding on terms). The full suite runs on the revision that an advance of the main line names, which is the revision whose evidence QA.10 asks to be current, and on the development line at the stated cadence (STND.TEST.6); the cadence is stated as a number of merges or a span of time so that it is decidable, and a verdict whose key is unchanged since a run at the cadence stands for the run before the release under STND.TEST.8. A failure that a full run finds after the selections passed is either a miss of the selection rule, which is a defect of that rule and widens it once corrected, or an interaction between merged changes, which the identification of the causing change separates (t1, answer 18) (STND.TEST.7). Changes that touch different files are able to fail a test together.

STND.TEST.8 is the test form of STND.BUILD.23: a verdict stands for a later run only under a key that holds every verdict input, and a merge makes a new revision without changing the key of a test whose inputs it does not touch, which t1 gives as its synthesis and marks unconfirmed for a branch merge. Failed runs are not taken from a cache by default in the tool documentation read, and a test that reads an undeclared input or whose output varies is kept from incremental reuse (t1, H2, S18, S19, S20); that test is a flaky test or has verdict inputs that STND.TEST.2 does not give, and the second sentence of STND.TEST.8 leaves it to run, and the record of STND.TEST.9 names each verdict that stood. The record of STND.TEST.9 shows a reviewer what was selected, what was reused, and what was left out, which is what the release record of STND.WPROC.14 and the review of STND.WPROC.10 need; its count of tests not run shows a suite that shrinks between runs, which a pass count alone hides (t2, answer 15). The time and cost of the run stay with RSRC.3, and a budget for testing at each depth is a budget under RSRC.1.

Between merges, the tests that the changes since the last run are able to affect, with those that failed at their last run, are the smallest set that tells the author whether the change works; after a failure they are the failing tests and the tests that the attempted fix reaches (STND.TEST.10). The second sentence of STND.TEST.10 asks a reason and blocks nothing: a change to a root of the build description is able to reach every test, and a full run for it is then the selection itself.

A rerun discards the evidence of the failure unless it was kept first, and a defect that fails with probability p on each run passes within k reruns with probability 1-(1-p)^k, which is t2's arithmetic (t2, H3) (STND.TEST.11 and STND.TEST.12). A further run is then an experiment, alone, in another order, serialized, with a fixed seed, or with altered timing, whose hypothesis the second sentence of STND.TEST.11 has stated. One study estimated about 170 passing reruns for 95 percent confidence that a test is not flaky, and another found flakiness after up to 10,000 reruns; reruns under identical conditions miss rare interleavings (t2, answer 11). A pass after a failure under the same key is a second observation of an unexplained failure, as INTPR.7 records an anomaly that is not followed to its cause (STND.TEST.12). The causes that recur are few: waiting on asynchronous work without a completion condition, concurrency in the test or in the code under test, dependence on order and shared state, infrastructure and resources, time, randomness, the network, unordered collections, and floating-point comparison; in one study 10 of 32 concurrency cases were defects of the code under test, which STND.CONC governs (t2, H3) (STND.TEST.13). A longer timeout, a retry, or a mark that admits failure lowers the signal of a check, and AGENT.47 has an agent state it as a weakened check. A quarantined test is forgotten without its bound, and supports no claim while it lasts (t2, answer 14). A numerical difference within the agreement that its acceptance criterion fixed gives the same verdict on each run, so it does not make a test flaky (STND.VVUQ.82). Dependent tests were found in every suite examined in one study, and in one parallel run 111 of 665 tests changed their verdict (t1, H1; t2, H2) (STND.TEST.14); a declared dependence is selected with its dependent under STND.TEST.4, and an order that differs between runs of the full suite finds the dependence that no one declared.

Where no reference gives the expected output, a test still judges by a check whose defects are known: a property of each output, a metamorphic relation between related runs, or agreement of independent implementations (t2, answers 2 and 3) (STND.TEST.15). A relation is chosen to be violated by a named class of defect, since a constant function satisfies many relations; independent implementations that share a defect agree; and a disagreement within a declared variation is no defect (STND.VVUQ.82). The invariants of VV.10 are one kind of partial oracle, and the reference oracles of numerical methods stay with NUMER.6 and STND.VVUQ.18. A test that draws its inputs at random is meaningless without its distribution, and a failing input kept for replay is the regression test of the defect that it found (t2, H1) (STND.TEST.16); its seed is a recorded input under STND.CODE.2 and STND.CODE.9, and a stochastic result is tested under STND.VVUQ.64.

Across five systems, coverage correlated only weakly to moderately with the effectiveness of a suite once its size was controlled, and its authors advise against coverage as a quality target; mutant detection tracked real-fault detection independently of coverage in another study, but equivalent mutants are undecidable to identify, and a requirement that the code omits has no mutant (t2, H5) (STND.TEST.17). A threshold on either measure invites a suite padded to the number, so STND.TEST.17 has them reported with their kind and exclusions, as a finder of weak tests and of unexercised code. A two-way trace between acceptance criteria and acceptance tests finds the criterion that no test checks, which no adequacy measure finds; STND.CREW.17 audits that coverage before a release of work of CSQ2 or a more severe class, and STND.TEST.18 is the record that the audit reads (t2, answer 19).

PRIME.2 forbids evidence obtained by adjusting a test, a reference, or a criterion to the output, AGENT.5 has an agent record a change to a check that judges its own change apart from that change, AGENT.47 has it state each check skipped, disabled, or weakened, and STND.CREW.15 gives those statements to the review agent. What they leave open is the case that the work report does not state, and the expected value that restates the code (STND.TEST.19). On agent benchmarks, models edited or deleted tests, special-cased expected values, and passed weak tests with wrong patches, at rates that depend on the model, the prompt, and the benchmark; the classes of hazard are stable where the rates are not (t2, H6). The first sentence of STND.TEST.19 has the review find each loosened or removed test from the change itself, where a difference from the statements of AGENT.47 is a finding of the review; the second has an author's test state how its expected value was obtained without the code that it judges, since an expected value computed by the code's own formula is a regression guard under VV.7. A pass of the suite does not show that a change is correct, and a review that looks for behavior that the tests do not check finds what a passing suite hides (t2, answer 22).

Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, RSRC, or QA, and applies from CSQ3; work of CSQ4 may omit it. The part of a provision that rests on a row of the table of STND.CLASS.10 applies from the class of that row. The second sentence of STND.TEST.15 documents a limit of what a verification detects, rests on INTPR.10, and applies from CSQ2, as STND.CONC.27 does. STND.TEST.1 labels each test with a level of VV.6 and asks no verification of an assembly or of the integrated system, which the row of VV.6 starts at CSQ1, so it applies from CSQ3. STND.TEST.2 asks that the verdict inputs of a test be derivable, which VV.8 and RSRC.11 already rest on, and asks for no mechanism that tracks dependencies between results, which the row of QA.14 covers, so it applies from CSQ3. STND.TEST.9 asks for a record kept with the run, and not provenance written into each output at production, which the row of REPRO.4 covers, and the record of time, memory, and cost with each run stays with the row of RSRC.3 at CSQ2. STND.TEST.11 asks for the record of a failure that occurred, and not for diagnostics captured by default, which the row of INTPR.8 starts at CSQ1. STND.TEST.12, STND.TEST.15, STND.TEST.17, and the second sentence of STND.TEST.19 instantiate VV.1 and ask for no comparison against a reference oracle produced without the implementation that it judges, which the row of VV.1 starts at CSQ2, so they apply from CSQ3. Every other provision and sentence rests on no row and applies from CSQ3. No provision binds, and none raises the floor (GOV.11): each is a default that asks only what RSRC.11, RSRC.12, RSRC.7, VV, REPRO, INTPR, or QA already ask, at the cost of wording, a statement in the repository configuration, a run, or one record, and the honest report of verdicts already binds through PRIME.2, VV.7, AGENT.4, AGENT.5, and AGENT.47.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| GOV | Governance |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| STND.BUILD | Build standard |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CREW | Agent roles standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| STND.WPROC | Work process standard |
| VV | Correctness |

## Provisions

### Suite structure

#### STND.TEST.1 Tiers and levels of tests

Default. Instantiates RSRC.11, VV.6.

The repository configuration SHOULD state the tiers of the full suite, the tier of each test, and the level of VV.6 at which each test verifies (RSRC.11, VV.6).

#### STND.TEST.2 Derivable verdict inputs

Default. Instantiates VV.8, RSRC.11.

The verdict inputs of each test SHOULD be derivable by a tool from the build description, from a record of the inputs that the test read that a tool writes at its run, or from both (VV.8, RSRC.11). Each such record SHOULD state the revision of the work at which it was written (VV.8).

### Selection

#### STND.TEST.3 Selection of affected tests

Default. Instantiates RSRC.11, VV.8, RSRC.12.

Where a run of tests holds fewer than every test of the full suite, its selection SHOULD be derived by a selection rule from the change and the verdict inputs of the tests, and hold each test whose verdict the change is able to affect (RSRC.11, VV.8). Where a selection omits a test whose verdict inputs the change alters, the record of the run SHOULD state the omission and the later decision point at which that test runs (RSRC.12).

#### STND.TEST.4 Inputs that widen a selection

Default. Instantiates RSRC.11, VV.8.

Where a change alters an input of the first column of the table of this provision, each selection for that change SHOULD hold the tests of its second column (RSRC.11, VV.8). Each selection SHOULD also hold each new or changed test, each test that failed at its last run on the branch, each test whose verdict inputs the derivation of STND.TEST.2 does not give for the revision run, and each test on which a selected test declares a dependence under STND.TEST.14 (VV.8).

| Input changed | Tests that the selection holds |
| --- | --- |
| An execution setting or a variable of the environment that a build step reads | Each test of each output of that build step |
| An execution setting or a variable of the environment that a test reads | That test |
| A tool of a toolchain, or a build configuration | Each test of each output built with that tool or in that build configuration |
| The revision of a dependency | Each test of each component that uses the dependency |
| A generated file, or its generator | Each test of each component that reads the generated file |
| A file of data or of configuration | Each test that reads the file, or, where no record shows which tests read it, every test of the component that holds it |
| The harness of the tests, a fixture, or a helper shared by tests | Each test that uses it |
| Code reached by reflection, by loading at run time, by a call across languages, or in a child process, where the derivation of STND.TEST.2 does not follow that reach | Every test of the component that holds the code |
| The selection rule, or a record from which it derives selections | Every test whose selection the rule or the record decides |
| A file of a kind that the repository configuration does not list as unable to change a verdict, where the derivation of STND.TEST.2 shows no test that reads it | Every test of the component that holds the file |

#### STND.TEST.5 Selection by integration depth

Default. Instantiates RSRC.11, RSRC.12.

The repository configuration SHOULD state, for each integration depth, the tiers from which the selection of a merge at that depth is drawn, with every tier for a merge into the development line (RSRC.11, RSRC.12). Each tier from which the selection at one integration depth is drawn SHOULD also be drawn from at each smaller integration depth (RSRC.11).

#### STND.TEST.6 Full-suite runs

Default. Instantiates VV.8, RSRC.11, RSRC.12.

Before each advance of a main line, the full suite SHOULD run on the revision that the advance names (VV.8, RSRC.11). The full suite SHOULD also run on the development line at a cadence that the repository configuration states as a number of merges or a span of time (VV.8, RSRC.12).

#### STND.TEST.7 Misses of a selection

Default. Instantiates QA.6, QA.4, RSRC.11.

Where a run of the full suite fails a test, the change that caused the failure SHOULD be identified among the changes since the last run in which that test passed (QA.6). Where the selection for that change omitted the test without the record that STND.TEST.3 asks, the omission SHOULD be recorded in defect tracking as a defect of the selection rule (QA.4, RSRC.11).

#### STND.TEST.8 Reuse of test verdicts

Default. Instantiates RSRC.7, REPRO.1, REPRO.3.

Only a passing verdict obtained under an unchanged verdict key SHOULD stand for a later run of a test (RSRC.7, REPRO.1). Where a test is a flaky test, or reads an input outside the verdict inputs that STND.TEST.2 derives for it, its verdicts SHOULD NOT stand for a later run (RSRC.7, REPRO.3).

#### STND.TEST.9 Selection and verdict record

Default. Instantiates VV.5, RSRC.11, REPRO.1.

The record of each run of tests on which a merge or a release relies SHOULD hold the content of the table of this provision (VV.5, RSRC.11, REPRO.1).

| Item | Content |
| --- | --- |
| Revision | The revision run, its branch, and the integration depth of the merge or the release for which the run is made |
| Selection | The selection rule with its revision, and the numbers of tests in the selection and in the full suite |
| Reused verdicts | Each test whose verdict stood for its run under STND.TEST.8, with its verdict key |
| Omitted tests | Each test that the selection omits although the change alters its verdict inputs, with the decision point at which it runs |
| Excluded tests | The numbers of tests skipped, disabled, marked as expected to fail, and in quarantine, with the reason for each such test |
| Verdicts | The verdict of each test run, each unexplained failure under STND.TEST.12 included |
| Order | The order in which the tests ran, or the seed from which that order was drawn |

### Development runs

#### STND.TEST.10 Runs between merges

Default. Instantiates RSRC.11.

Other than a run before a merge and a run of the full suite under STND.TEST.6, each run of tests on a branch SHOULD hold only the tests that the changes since the previous run on that branch are able to affect and the tests that failed at their last run, as STND.TEST.3 and STND.TEST.4 select them (RSRC.11). Where a run on a branch holds other tests, its record SHOULD state the reason (RSRC.11).

### Verdicts

#### STND.TEST.11 Failure evidence before a rerun

Default. Instantiates REPRO.1, QA.6.

Before a failed test runs again, the record of its failing run SHOULD keep the verdict key, the other tests of the run and their order, the first assertion that failed, and the output that the assertion judged (REPRO.1, QA.6). Until the cause of the failure is found, each further run of that test SHOULD state the hypothesis about that cause that the run tests (QA.6).

#### STND.TEST.12 Pass after an unexplained failure

Default. Instantiates VV.1, QA.6, VV.5.

Where a failed test passes at a later run under the same verdict key, that pass SHOULD NOT be taken as evidence for the change that the test judges (VV.1). Until a diagnosis names the cause of the failure, the record of each run that holds the test SHOULD report it as an unexplained failure, with the numbers of its runs and of its failures since the first failure (QA.6, VV.5).

#### STND.TEST.13 Flaky tests and quarantine

Default. Instantiates QA.4, REPRO.3, REPRO.7.

Each flaky test SHOULD be recorded in defect tracking as a defect of the test or of the code that it judges, with its suspected cause (QA.4, REPRO.3). Where a flaky test is placed in quarantine, the quarantine SHOULD be recorded with its reason, the actor responsible for the repair, and a bound in time or in number of runs at which the test is repaired or retired by a recorded decision (QA.4, REPRO.7).

#### STND.TEST.14 Independence of tests

Default. Instantiates REPRO.3.

Other than a dependence on another test that the repository configuration declares, each test SHOULD give the same verdict alone, in every order, and beside every subset of the full suite (REPRO.3). Each run of the full suite on the development line SHOULD run its tests in an order that differs between runs and that its record states (REPRO.3).

### Oracles and adequacy

#### STND.TEST.15 Partial oracles

Default. Instantiates VV.1, INTPR.10.

Where no reference gives the expected output of a test for its inputs, the test SHOULD judge that output by a partial oracle and state the kind of that oracle (VV.1). Each test that judges by a partial oracle SHOULD state the classes of defect that its oracle does not detect (INTPR.10).

#### STND.TEST.16 Generated test inputs

Default. Instantiates REPRO.1, VV.8.

Each test that draws its inputs from a generator SHOULD state the generator, the distribution from which it draws, and the number of inputs that it draws, and keep each input on which it failed for later runs (REPRO.1, VV.8).

#### STND.TEST.17 Adequacy measures reported

Default. Instantiates INTPR.9, VV.1.

Each report of an adequacy measure SHOULD state its kind, the code and the tests that it measures, what it excludes, and, for a mutation score, its operators and its treatment of mutants equivalent to the code (INTPR.9). An adequacy measure SHOULD NOT be set as a threshold for the acceptance of a change (VV.1).

#### STND.TEST.18 Acceptance tests traced

Default. Instantiates VV.3, QA.2.

Each acceptance test SHOULD name each acceptance criterion that it checks (VV.3, QA.2). The record of each unit of work SHOULD list each of its acceptance criteria that no acceptance test checks, with the means by which that criterion is judged (VV.3, QA.2).

### Changes to tests

#### STND.TEST.19 Tests changed with their code

Default. Instantiates QA.7, VV.1.

The review of each change SHOULD identify, from the change itself, each test that the change removes, skips, disables, marks as expected to fail, or loosens in its assertion or its tolerance (QA.7). Where the author of a change writes or changes a test that judges that change, the test SHOULD state how its expected value was obtained without the code that it judges, or be labeled a regression guard (VV.1).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
