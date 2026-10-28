# Testing methods standard (STND.TEST) 1.1

Adopted by The Custodian as revision 1.0 in ledger entry 145 (2026-10-25); revised to 1.1 in entry 283 (2026-10-28). This reading copy is composed from the per-provision files in STND/TEST/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the method of testing that holds for every language, test framework, and build tool: how the work structures its tests, selects the tests that a change runs, reuses verdicts, and reads the verdicts that its tests give. RSRC.11 and RSRC.12 hold the obligation to run the smallest set of checks that establishes the evidence that a change requires and to defer the rest to the latest decision point at which its result is still needed; this standard gives the method by which the work meets them, and adds to VV, QA, STND.CODE, STND.WPROC, and STND.BUILD only what that method makes necessary. It covers the structure of the suite (STND.TEST.1 and STND.TEST.2); the selection of tests, its widening with the integration depth, the full-suite run, the reuse of verdicts, and the record of a run (STND.TEST.3 to STND.TEST.9); runs on a branch (STND.TEST.10); the reading of verdicts (STND.TEST.11 to STND.TEST.14); oracles, generated inputs, adequacy measures, and acceptance tests (STND.TEST.15 to STND.TEST.18); and tests changed with the code that they judge (STND.TEST.19).

No provision binds. Every provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The honest report of verdicts binds at every class through PRIME.2, VV.7, AGENT.4, AGENT.5, and AGENT.47, and this standard adds nothing to that floor. The standard is agnostic of language, test framework, build tool, and vendor: its provisions name none of them, and no granularity of analysis, tier size, or threshold (GOV.18). The comparisons, tolerances, and stochastic tests of numerical results belong to STND.VVUQ.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Acceptance criteria, Component, Reference oracle, Regression guard, Test, and Unit of work have the meanings that the Lexicon gives them. Repository configuration and Execution setting have the meanings that STND.CODE gives them; Branch, Merge, Main line, Development line, and Parent branch have the meanings that STND.WPROC gives them; Build description, Build configuration, Toolchain, and Generated file have the meanings that STND.BUILD gives them; Execution path and Reference path have the meanings that HW gives them; and Integrity digest has the meaning that STND.DEPS gives it, used here also of a verdict input. The verdict of a test is whether it passes or fails on one run; a verdict that a test reports as inconclusive is a verdict that does not pass.

| Term | Definition |
| --- | --- |
| Full suite | Every test that the work holds, in every tier, each test that is skipped, disabled, or in quarantine included. |
| Full-suite run | A run of tests that executes each test of the full suite, each test that is skipped, disabled, or in quarantine included, and for which no verdict of an earlier run stands. |
| Tier | A class of the tests of the work that the repository configuration states by a bound on the time and the resources that each of its tests uses and by the reach of what each exercises, from code in one process to code on more than one host. |
| Verdict input | Of a test: each file, datum, tool, execution setting, variable of the environment, random seed, and other test whose change is able to change its verdict, the code that it exercises, its harness, its fixtures, and each item of the execution path that runs it, and of the reference path whose results it compares, that the record of HW.3 identifies included. |
| Selection | The tests that one run of tests runs, drawn from the full suite. |
| Selection rule | The procedure, stated in the repository configuration under a revision, by which a selection is derived from a change and from the verdict inputs of the tests. |
| Integration depth | Of a merge into a branch other than a main line: the number of branches on the path of parent branches from its target branch to the first development line or main line on that path, the target branch included and that line excluded, so that a merge into the development line has depth 0 and a merge into a branch made from it has depth 1. A merge into a main line advances it, which is a release, and has no integration depth. |
| Verdict key | Of a verdict of a test, the record of the revision or the integrity digest of each verdict input of the test other than a secret, at the run that gave the verdict. |
| Flaky test | A test whose verdict differs between runs under one verdict key. |
| Quarantine | The state of a flaky test on whose verdict no merge and no release relies, for a recorded bound. |
| Partial oracle | A check that each correct output of a test meets and that at least one incorrect output fails, and that does not give the expected output: a property of each output, a relation between the outputs for related inputs, or agreement with another implementation that is not a reference oracle. |
| Adequacy measure | A measure of how thoroughly a set of tests exercises the code or detects changes to it, the coverage of the code of a stated kind and the score of a mutation analysis among them. |
| Acceptance test | A test whose stated behavior is an acceptance criterion of a unit of work, or a part of one. |

## Notes

The provisions rest on what the literature of regression testing and of test verdicts has shown for decades and what holds across languages and tools: a selection is safe when it holds every test whose verdict the change is able to alter, and only under controlled conditions; declared dependencies give a conservative reach and observed ones narrow it, while every input that the observer does not see widens it; the cost of testing grows with the rate of change times the size of the suite; a verdict is reusable only under a key that holds every input; dependent tests give verdicts that change with order; a rerun turns an intermittent defect green; the oracle problem has weaker remedies, invariants, metamorphic relations, and differential comparison among them; and coverage shows what no test exercised, not what an assertion constrains (research/test-notes/t1-selection-and-budget.md and research/test-notes/t2-tests-and-verdicts.md, "Timeless versus moving"). The figures that the notes quote come from studies of particular languages, companies, and benchmarks, are examples and not norms, and no provision adopts them. Most sources were read as extracts or search summaries that a retrieval tool wrote; the Notes mark a figure that rests on one, and an inference of a research note, where a provision leans on it.

The obligation stays with RSRC.11 and RSRC.12, and the standard gives the method. The custodian's concern is that agents run the full suite by habit, at a cost in time, power, and other budgets, where a smaller set of tests establishes the correctness of the code before it merges into the next unit up, so that a subfeature that merges into a feature carries a lighter burden than a merge into the main line. The evaluation of performance belongs to STND.PERF, whose STND.PERF.23 holds the regression guard on a performance quantity, time among them.

The standard cites what the corpus already holds and does not restate it (GOV.31): RSRC.11, RSRC.12, and VV.8 for targeted verification, deferral, and re-verification; STND.WPROC.8 and STND.WPROC.9 for the update and the checks before a merge, and STND.WPROC.13 and STND.WPROC.14 for the release proposal and record; VV.6 for levels and localization, VV.7 for the label of a regression guard, STND.CODE.8 for a test per fix, and STND.CODE.9 for repeatable verdicts; RSRC.7 and STND.BUILD.23 for reuse under a complete key, and STND.DEPS.6 for the integrity digest against which a fetched component is verified, which a verdict key holds of each verdict input; STND.BUILD.1, STND.BUILD.4, STND.BUILD.11, and STND.BUILD.26 for declared inputs, generators, settings, and the build configurations under check; HW.3 for the record of an execution path; QA.4 and QA.6 for defects and broken checks; RSRC.3 and AGENT.24 for the time and cost of runs and units; STND.VVUQ.17 for the failure of a numerical regression guard; NUMER.6 and STND.VVUQ.18 for the reference oracles of numerical methods; STND.VVUQ.64 for fixed-seed and fresh-seed tests and NUMER.26 against reseeding a stochastic comparison to pass; STND.VVUQ.78 for the numerical instance of RSRC.11 and RSRC.12; and STND.VVUQ.82 and STND.VVUQ.83 for declared variation.

A tier is stated by what its tests use. Tests that run in one process without blocking calls, tests that use local processes and threads, and tests that need more than one host form the pattern of one published scheme, whose sizes and time limits are that company's policy (t1, H2) (STND.TEST.1). A pass of the fastest tier is not a pass of the suite, and a change at a seam between components is not covered by that tier alone. The level of VV.6 at which a test verifies lets a failure be localized and lets a selection draw the tests of an assembly. Where the build enforces isolation, a test sees only what it declares, so selection by the declared graph of the build is safe; t1 notes that this isolation is not enforced by default in the tool it read (t1, H2, S19). The declared graph selects every test above a change to a shared root, and observed dependencies at the level of files narrow it; finer analysis missed more in the studies read, through reflection and excluded libraries (t1, H1) (STND.TEST.2). A record of what a test read goes stale as the code changes, which is why it carries its revision (t1, H1, S15). The standard names no granularity. Where no tool derives the verdict inputs, a statement in the repository configuration serves; where neither gives the verdict inputs of a test, STND.TEST.4 holds that test in each selection, so the selection falls back to every test that no derivation covers.

A selection that holds every test whose verdict the change is able to alter is safe under controlled conditions, the same environment, inputs, and seeds, and no procedure finds exactly the tests that would fail (t1, answer 1) (STND.TEST.3). A selection that rests on a prediction, a window of recent failures, or a distance in the dependency graph is not safe; in the documented case it relied on a full run every few hours, and STND.TEST.3 records what it omits and where the omission is covered (t1, answers 17 and 18). An omitted test whose verdict the change is able to affect is a check deferred under RSRC.12; until a later run holds it, it is a skipped check of the work report under AGENT.47, and the run that holds it closes the deferral, so that STND.WPROC.13 carries to a release proposal only a deferral that no run has closed. The rows of STND.TEST.4 are the inputs that the studies of t1, H1, show a selector to miss: a setting or a tool not registered as an input, files that are not source, fixtures and generators without a dependency edge, code reached across a language or a process, and the selector itself, for which one study reported 27 bugs in three tools, 14 of them confirmed or already known (t1, H1, S5, S6, S7, S20). The hardware model, firmware, drivers, and runtime libraries that HW.3 records are verdict inputs on the same footing: a verdict obtained on one execution path does not stand for a run on another, and a change of firmware or driver selects the tests that run on the path. A module-level selector selected every module in 65 percent of commits until a reviewed list excluded the kinds of file that do not change a verdict, which is the list that the last row of the table admits (t1, H1, S6). New tests run unconditionally in the tool described (t1, answer 6, S15); the tests that failed at their last run, and those with no current derivation, are held by the reasoning of safe selection, since their last verdict says nothing about the change. The tests of the second sentence of STND.TEST.4 are few and are drawn from every tier, as STND.TEST.5 says; the tests of the rows of its table are drawn from the tiers of the depth, and STND.TEST.3 and STND.TEST.5 have each other test that a row reaches recorded as an omission and run at the first merge whose depth draws on its tier, at the latest at the merge into the development line.

The integration depth turns the custodian's level of integration into a number that the history decides. A merge into a feature far from the development line draws on the fastest tiers; each step toward the development line draws on the tiers of the step below and on more; and a merge into the development line draws on every tier, so that the selection there is wider than below it while still a selection (STND.TEST.5). The rule of STND.TEST.5 covers every depth, so that a hierarchy of unbounded depth needs no unbounded configuration. A merge of a parent branch into a branch descended from it under STND.WPROC.6 or STND.WPROC.8 has the depth of its target, and the selection of STND.TEST.5 is the one for the merge of a branch into its parent. The change that a merge brings grows as it moves up, because it holds the merged work of each unit below, and STND.WPROC.9 selects for the whole of it on the branch as updated. A flat hierarchy, with every unit at depth 1, collapses the widening to one step, and depth does not measure the size of a change or the number of siblings; the custodian's ruling asks for widening with the level of integration and not with size. This mapping of staged practice at two large companies and of the two-phase studies onto the branch hierarchy of STND.WPROC is a synthesis and not a published rule; both companies abandoned a full run for each change because its cost grew with the rate of change times the size of the suite (t1, answer 9 and the finding on terms).

STND.TEST.6 holds the custodian's ruling of 2026-10-25: a full-suite run before each advance of a main line, which is a release, and at a cadence that the project states on the development line, which audits the selection. RSRC.11 asks for broader checking at release, and the ruling makes that checking the full suite. The release run completes on the revision that the release proposal names, before the human owner decides on the record of STND.WPROC.14, so that the outcome is in the record on which the decision is made and is evidence current for the released revision under QA.10. No reused verdict stands in a full-suite run, because the run audits the derivation from which each verdict key is computed, and a key held by that derivation does not check the derivation; AGENT.4 has no check stated as passing without a run against the revision described. A full-suite run executes each test that the work holds, a skipped, disabled, or quarantined test included, so that disabling a test does not shrink the run that the custodian's "full run of all tests" asks; the verdicts of such tests are reported apart under STND.TEST.9, and the skip or disablement stays among the checks that AGENT.47 and STND.WPROC.13 carry to the human owner. A failure that a full-suite run finds after the selections passed is a miss of the selection rule, which is a defect of that rule and widens it once corrected, or an interaction between merged changes, which the identification of the causing change separates (t1, answer 18) (STND.TEST.7). Changes that touch different files are able to fail a test together.

STND.TEST.8 is the test form of STND.BUILD.23, for the selections below a full-suite run: a verdict stands for a later run only under a key that holds every verdict input, and a merge makes a new revision without changing the key of a test whose inputs it does not touch, which t1 gives as its synthesis and marks unconfirmed for a branch merge. Failed runs are not taken from a cache by default in the tool documentation read, and a test that reads an undeclared input or whose output varies is kept from incremental reuse (t1, H2, S18, S19, S20). A key that holds every input of a test that reads a secret holds the secret or a digest of it, which PRIME.10 keeps out of each record, so the key leaves the secret out and the verdict of such a test does not stand, as STND.BUILD.23 keeps such outputs out of a build cache. The record of STND.TEST.9 shows a reviewer what was selected, what was reused, and what was left out, on which the review of STND.WPROC.10 and the release record of STND.WPROC.14 draw; its counts of excluded tests show a suite that shrinks between runs, which a pass count alone hides (t2, answer 15), and the reasons for each skipped, disabled, or weakened check stay with AGENT.47 and STND.WPROC.13. The time and cost of the run stay with RSRC.3, and a budget for testing at each depth is a budget under RSRC.1.

Between merges, the tests that the changes since the last run are able to affect, with those that failed at their last run, are the smallest set that tells the author whether the change works; after a failure they are the failing tests and the tests that the attempted fix reaches (STND.TEST.10). Before a merge, the selection is the one of STND.TEST.5 for the change that the merge brings, and the run before the advance of a main line is the full-suite run of STND.TEST.6, which no selection limits. The three sentences of STND.TEST.10 are one rule for the runs on a branch and are never applied apart. The third sentence asks a reason and blocks nothing: a change to the build description at a root that every output depends on reaches every test through its row of STND.TEST.4, and a run of every test is then the selection itself.

A rerun discards the evidence of the failure unless it was kept first (STND.TEST.11). t2 infers that a defect that fails with probability p on each run passes within k reruns with probability 1-(1-p)^k (t2, H3) (STND.TEST.11 and STND.TEST.12). A further run is then an experiment, alone, in another order, serialized, with a fixed seed, or with altered timing, whose hypothesis STND.TEST.11 has stated; a repeat of a failed stochastic comparison with other random numbers stays barred by NUMER.26. Two studies whose methods t2 did not read report about 170 passing reruns for 95 percent confidence that a test is not flaky, and flakiness found after up to 10,000 reruns; reruns under identical conditions miss rare interleavings (t2, answer 11). A pass after a failure, under the same verdict key or under one that differs only in a seed or a drawn input, is a second observation and not a verdict on the change, and its standing ends when a diagnosis names the cause (STND.TEST.12); STND.TEST.12 rests on VV.1, QA.6, and VV.5. The causes that recur are few: waiting on asynchronous work without a completion condition, concurrency in the test or in the code under test, dependence on order and shared state, infrastructure and resources, time, randomness, the network, unordered collections, and floating-point comparison; in one study 10 of 32 concurrency cases were non-determinism in the code under test, which STND.CONC governs (t2, H3) (STND.TEST.13). A longer timeout, a retry, or a mark that admits failure lowers the signal of a check, and AGENT.47 has an agent state it as a weakened check. A quarantined test is forgotten without its bound, and supports no claim while it lasts (t2, answer 14). QA.6 still has an actor restore a check that its own change broke, and quarantine is not that restoration. A test placed in quarantine is a disabled check of the work report under AGENT.47, and the review of STND.TEST.19 finds it from the change. A numerical difference within the agreement that its acceptance criterion fixed gives the same verdict on each run, so it does not make a test flaky (STND.VVUQ.82). Dependent tests were found in every suite examined in one study, and in one parallel run 111 of 665 tests changed their verdict; both rest on an abstract summary and an extract (t1, H1; t2, H2) (STND.TEST.14). A declared dependence is selected with its dependent under STND.TEST.4, and an order that differs between full-suite runs, within the declared dependences, finds the dependence that no one declared; that evidence for shuffled order is also from summaries and extracts (t1, S13a, S13b, S21).

Where no reference oracle gives the expected output, a test still judges by a check whose limits are known: a property of each output, a metamorphic relation between related runs, or agreement with another implementation (t2, answers 2 and 3) (STND.TEST.15). An implementation produced without the code under test is a reference oracle, which NUMER.6 and STND.VVUQ.18 rank for numerical methods; agreement with one that shares code, data, or method with the code under test is a partial oracle, because implementations that share a defect agree. A relation is chosen to be violated by a named class of defect, since, as t2 infers, a constant function satisfies many relations; and a disagreement within a declared variation is no defect (STND.VVUQ.82). The invariants of VV.10 are one kind of partial oracle, and the partial oracle is the reference that VV.7 has the test state. A test judged by a partial oracle is not the verification of a numerical method against reference oracles that NUMER.6 asks, which still binds that method. A test that draws its inputs at random is meaningless without its distribution, and a failing input kept for replay is the regression test of the defect that it found (t2, H1) (STND.TEST.16); its seed is a recorded input under STND.CODE.2 and STND.CODE.9, and a stochastic result is tested under STND.VVUQ.64.

Across five systems, coverage correlated only weakly to moderately with the effectiveness of a suite once its size was controlled, and its authors advise against coverage as a quality target, a finding specific to those systems and to one measure of effectiveness (t2, H5) (STND.TEST.17). A threshold on coverage invites a suite padded to the number, so the second sentence of STND.TEST.17 bars it, and a project that wants a coverage gate states it as a recorded decision under REPRO.7. A mutation score is an indicator and not a rate: by a search summary of a study that t2 did not read, mutant detection tracked real-fault detection independently of coverage; equivalent mutants are undecidable to identify; and, as t2 infers, a requirement that the code omits has no mutant. STND.TEST.17 therefore has a mutation score reported with its operators and exclusions, and sets no rule on its threshold. A two-way trace between acceptance criteria and acceptance tests finds the criterion that no test checks, which no adequacy measure finds; STND.CREW.17 audits that coverage before each release of work of CSQ2 or a more severe class, and of CSQ3 where the lead agent records the dimension as bearing on the changes, and STND.TEST.18 is the record that the audit reads (t2, answer 19).

PRIME.2 forbids evidence obtained by adjusting a test, a reference, or a criterion to the output, AGENT.5 has an agent record a change to a check that judges its own change apart from that change, AGENT.47 has it state each check skipped, disabled, or weakened, STND.CREW.15 gives those statements to the review agent, and STND.VVUQ.17 governs the renewal of the reference of a numerical regression guard. What they leave open is the change to a test that the work report does not state, and the expected value that restates the code (STND.TEST.19). By search summaries and a secondary excerpt, models on agent benchmarks edited or deleted tests, special-cased expected values, and passed weak tests with wrong patches, at rates that depend on the model, the prompt, and the benchmark; STND.TEST.19 rests on the classes of hazard, which are stable, and not on the rates (t2, H6). The first sentence of STND.TEST.19 has the review find each loosened, removed, or re-referenced test from the change itself, where a difference from the statements of AGENT.47 is a finding of the review; the second has an author's test state the source of its expected value and whether that source is independent of the code that it judges, and VV.7 labels a test whose source is the code a regression guard. A pass of the suite does not show that a change is correct, and a review that looks for behavior that the tests do not check finds what a passing suite hides (t2, answer 22).

Under STND.CLASS.10, each provision instantiates only VV, REPRO, INTPR, RSRC, or QA, and applies from the class that its field `onset` gives, which work of CSQ4 may omit; at CSQ3 a statement of the repository configuration meets STND.TEST.2, the derivation by a tool being the mechanism that tracks dependencies between results, which the row of QA.14 asks from CSQ2, and the tiers, the integration depths, and the records of selection, reuse, omission, and reason start at CSQ2, so that at CSQ3 a selection is drawn from the whole suite, and work of CSQ3 that runs its suite whole owes its verdicts and none of these records. No provision binds, and none raises the floor (GOV.11): each is a default that asks only what RSRC.11, RSRC.12, RSRC.7, VV, REPRO, INTPR, or QA already ask, at the cost of wording, a statement in the repository configuration, a run, or one record, and the honest report of verdicts already binds through PRIME.2, VV.7, AGENT.4, AGENT.5, and AGENT.47.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| GOV | Governance |
| HW | Execution hardware |
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
| STND.DEPS | Dependency policy |
| STND.PERF | Performance evaluation standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| STND.WPROC | Work process standard |
| VV | Correctness |

## Provisions

### Suite structure

#### STND.TEST.1 Tiers and levels of tests

Default, from CSQ2. Instantiates RSRC.11, VV.6.

The repository configuration SHOULD state the tiers of the full suite, the tier of each test, and the level of VV.6 at which each test verifies (RSRC.11, VV.6).

#### STND.TEST.2 Derivable verdict inputs

Default, from CSQ3. Instantiates VV.8, RSRC.11.

The verdict inputs of each test SHOULD be derivable by a tool from the build description or from a record of the inputs that the test read that a tool writes at its run, or from a statement of the repository configuration (VV.8, RSRC.11). Each such record and statement SHOULD state the revision of the work at which it was written (VV.8).

### Selection

#### STND.TEST.3 Selection of affected tests

Default, from CSQ3; sentence 2 from CSQ2. Instantiates RSRC.11, VV.8, RSRC.12.

Where a run of tests is not a full-suite run, its selection SHOULD be derived by a selection rule from the change and the verdict inputs of the tests, and hold each test whose verdict the change is able to affect, in the tiers from which STND.TEST.5 draws the selection (RSRC.11, VV.8). Where a selection omits a test whose verdict inputs the change alters, the record of the run SHOULD state the omission and the later merge or release at which that test runs (RSRC.12).

#### STND.TEST.4 Inputs that widen a selection

Default, from CSQ3. Instantiates RSRC.11, VV.8.

Where a change alters an input of the first column of the table of this provision, each selection for that change SHOULD hold the tests of its second column, in the tiers from which STND.TEST.5 draws the selection (RSRC.11, VV.8). Each selection SHOULD also hold, from every tier, each new or changed test, each test that failed at its last run on the branch, each test whose verdict inputs the derivation of STND.TEST.2 does not give for the revision run, and each test on which a selected test declares a dependence under STND.TEST.14 (VV.8).

| Input changed | Tests that the selection holds |
| --- | --- |
| An execution setting or a variable of the environment that a build step reads | Each test of each output of that build step |
| An execution setting or a variable of the environment that a test reads | That test |
| The build description | Each test of each output of each build step whose declaration the change alters, and of each output that depends on those outputs |
| A tool of a toolchain, or a build configuration | Each test of each output built with that tool or in that build configuration |
| The revision of a dependency | Each test of each component that uses the dependency |
| A generated file, or its generator | Each test of each component that reads the generated file |
| A file of data or of configuration | Each test that a record shows to read the file, and, for a file with no such record, every test of the component that holds it |
| The harness of the tests, a fixture, or a helper shared by tests | Each test that uses it |
| An item of an execution path, or of its reference path, that the record of HW.3 identifies | Each test that runs on that path or compares its results with that path |
| Code that the derivation of STND.TEST.2 does not follow, reached by reflection, by loading at run time, by a call across languages, or in a child process | Every test of the component that holds the code |
| The selection rule, or a record from which it derives selections | Every test whose selection the rule or the record decides |
| A file of a kind that the repository configuration does not list as unable to change a verdict, and that the derivation of STND.TEST.2 shows no test to read | Every test of the component that holds the file |

#### STND.TEST.5 Selection by integration depth

Default, from CSQ2. Instantiates RSRC.11, RSRC.12.

The repository configuration SHOULD state, by a rule that covers every integration depth, the tiers from which the selection for the merge of a branch into its parent branch at each depth is drawn, beside the tests that STND.TEST.4 holds from every tier, with every tier for a merge into the development line (RSRC.11, RSRC.12). Each tier from which the selection at one integration depth is drawn SHOULD also be drawn from at each smaller integration depth (RSRC.11).

#### STND.TEST.6 Full-suite runs

Default, from CSQ3. Instantiates VV.8, RSRC.11.

Before the release record of an advance of a main line is presented under STND.WPROC.13, a full-suite run SHOULD complete on the revision that the release proposal names (VV.8, RSRC.11). A full-suite run SHOULD also complete on the development line at a cadence that the repository configuration states as a number of merges or a span of time (VV.8, RSRC.11).

#### STND.TEST.7 Misses of a selection

Default, from CSQ3. Instantiates QA.6, QA.4, RSRC.11.

Where a full-suite run fails a test, the change that caused the failure SHOULD be identified among the changes since the last run in which that test passed (QA.6). Where the selection for that change omitted the test without the record that STND.TEST.3 asks, the omission SHOULD be recorded in defect tracking as a defect of the selection rule (QA.4, RSRC.11).

#### STND.TEST.8 Reuse of test verdicts

Default, from CSQ3. Instantiates RSRC.7, REPRO.1, REPRO.3.

Only a passing verdict obtained under an unchanged verdict key SHOULD stand for a later run of a test in a selection (RSRC.7, REPRO.1). Where a test is a flaky test, reads an input outside the verdict inputs that STND.TEST.2 derives for it, or reads a secret, its verdicts SHOULD NOT stand for a later run (RSRC.7, REPRO.3, PRIME.10).

#### STND.TEST.9 Selection and verdict record

Default, from CSQ3; row Omitted tests from CSQ2; row Reused verdicts from CSQ2; row Selection from CSQ2. Instantiates VV.5, RSRC.11, REPRO.1.

The record of each run of tests on which a merge or a release relies SHOULD hold the content of the table of this provision (VV.5, RSRC.11, REPRO.1).

| Item | Content |
| --- | --- |
| Revision | The revision run, its branch, the execution path that ran it, and the merge, with its integration depth, or the release for which the run is made |
| Selection | Whether the run is a full-suite run; for a selection, the selection rule with its revision, and the numbers of tests in the selection and in the full suite |
| Reused verdicts | Each test whose verdict stood for its run under STND.TEST.8, with its verdict key |
| Omitted tests | Each test that the selection omits although the change alters its verdict inputs, with the merge or release at which it runs |
| Excluded tests | The numbers of tests skipped, disabled, marked as expected to fail, and in quarantine |
| Verdicts | The verdict of each test run, the verdict of each test that is skipped, disabled, or in quarantine apart from the others, and each unexplained failure under STND.TEST.12 |
| Order | The order in which the tests ran, or the seed from which that order was drawn |

### Development runs

#### STND.TEST.10 Runs on a branch

Default, from CSQ3; sentence 3 from CSQ2. Instantiates RSRC.11.

Other than a run before a merge and a full-suite run under STND.TEST.6, each run of tests on a branch SHOULD hold only the tests that the changes since the previous run on that branch are able to affect and the tests that failed at their last run, as STND.TEST.3 and STND.TEST.4 select them (RSRC.11). Other than a full-suite run under STND.TEST.6, each run before the merge of a branch into its parent branch SHOULD hold only the selection that STND.TEST.3, STND.TEST.4, and STND.TEST.5 give for the change that the merge brings (RSRC.11). Where a run on a branch, other than a full-suite run under STND.TEST.6, holds tests that the first two sentences leave out, its record SHOULD state the reason (RSRC.11).

### Verdicts

#### STND.TEST.11 Failure evidence before a rerun

Default, from CSQ3. Instantiates REPRO.1, QA.6.

Before a failed test runs again, the record of its failing run SHOULD keep the verdict key, the other tests of the run and their order, the first assertion that failed with its message, and the output that the assertion judged, each kept without a secret (REPRO.1, QA.6, PRIME.10). Until the cause of the failure is found, each further run of that test SHOULD state the hypothesis about that cause that the run tests (QA.6).

#### STND.TEST.12 Pass after an unexplained failure

Default, from CSQ3. Instantiates VV.1, QA.6, VV.5.

Until a diagnosis names the cause of a failure, a pass of the failed test at a later run, under the same verdict key or under one that differs only in a random seed or a drawn input, SHOULD NOT be taken as evidence for the change that the test judges (VV.1). Until a diagnosis names the cause of the failure, the record of each run that holds the test SHOULD report it as an unexplained failure, with the numbers of its runs and of its failures since the first failure (QA.6, VV.5).

#### STND.TEST.13 Flaky tests and quarantine

Default, from CSQ3. Instantiates QA.4, REPRO.3, QA.6, REPRO.7.

Each flaky test SHOULD be recorded in defect tracking as a defect of the test or of the code that it judges, with its suspected cause (QA.4, REPRO.3). Where a flaky test is placed in quarantine, the quarantine SHOULD be recorded with its reason, the actor responsible for the repair, and a bound in time or in number of runs at which the test is repaired or retired by a recorded decision (QA.4, QA.6, REPRO.7).

#### STND.TEST.14 Independence of tests

Default, from CSQ3. Instantiates REPRO.3.

Other than a dependence on another test that the repository configuration declares, each test SHOULD give the same verdict alone and in each order that a full-suite run uses (REPRO.3). Each full-suite run on the development line SHOULD run its tests in an order that differs between runs, keeps each declared dependence, and is stated in its record (REPRO.3).

### Oracles and adequacy

#### STND.TEST.15 Partial oracles

Default, from CSQ3; sentence 2 from CSQ2. Instantiates VV.1, INTPR.10.

Where no reference oracle gives the expected output of a test for its inputs, the test SHOULD judge that output by a partial oracle, and state that oracle and its kind as the reference of the test (VV.1). Each test that judges by a partial oracle SHOULD state the classes of defect that its oracle does not detect (INTPR.10).

#### STND.TEST.16 Generated test inputs

Default, from CSQ3. Instantiates REPRO.1, VV.8.

Each test that draws its inputs from a generator SHOULD state the generator, the distribution from which it draws, and the number of inputs that it draws, and keep each input on which it failed for later runs (REPRO.1, VV.8).

#### STND.TEST.17 Adequacy measures reported

Default, from CSQ3. Instantiates INTPR.9, VV.1.

Each report of an adequacy measure SHOULD state its kind, the code and the tests that it measures, what it excludes, and, for a mutation score, its operators and its treatment of mutants equivalent to the code (INTPR.9). A coverage of the code SHOULD NOT be set as a threshold for the acceptance of a change (VV.1).

#### STND.TEST.18 Acceptance tests traced

Default, from CSQ3. Instantiates VV.3, QA.2.

Each acceptance test SHOULD name each acceptance criterion that it checks (VV.3, QA.2). The record of each unit of work SHOULD list each of its acceptance criteria that no acceptance test checks, with the means by which that criterion is judged (VV.3, QA.2).

### Changes to tests

#### STND.TEST.19 Tests changed with their code

Default, from CSQ3. Instantiates QA.7, VV.1.

The review of each change SHOULD identify, from the change itself, each test that the change removes, skips, disables, places in quarantine, marks as expected to fail, loosens in its assertion or its tolerance, or gives another expected value or reference (QA.7). Where the author of a change writes or changes a test that judges that change, the test SHOULD state the source of its expected value, and whether that source is independent of the code that it judges (VV.1).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-25 | Adopted. |
| 1.1 | 2026-10-28 | Minor amendment (GOV.41): the records of the standard start at CSQ2: STND.TEST.1, STND.TEST.5, the record of an omission in the second sentence of STND.TEST.3, the rows Selection, Reused verdicts, and Omitted tests of STND.TEST.9, and the reason of the third sentence of STND.TEST.10; the statement route of STND.TEST.2 stands at CSQ3, and the Notes no longer put it to the custodian; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
