# Dispositions: STND.TEST 0.1 to 0.2

Reviews of draft 0.1: review-cold.md (cold review) and review-pairs.md (STND.HARN.28 pair review). The reading copies are labeled revision 1.0 because they are composed as the standard would be adopted; the drafts are 0.1 and 0.2. Numbering is unchanged from 0.1. The lead directed the strict reading of the full-suite run, the amendments of STND.WPROC and STND.CREW in this round, the date 2026-10-25, the definition of integration depth, and the execution path as a verdict input. New in this round: tools/amendment-scripts/apply_wproc_1_1.py and apply_crew_1_1.py, applied after STND.TEST by apply_test_round.py; reading copies STND.WPROC-0.2.md and STND.CREW-0.2.md; pair lists pairs-0.2.md, pairs-0.2-delta.md, and pairs-amended-0.2.md.

## Cold review

| Finding | Disposition |
| --- | --- |
| D1: reuse lets a verdict stand for the release run | Accepted, strict reading (lead). New Term Full-suite run: executes each test of the full suite other than a skipped or disabled test, quarantined tests included, and no verdict of an earlier run stands for it. STND.TEST.6 asks a full-suite run both before an advance and at the development-line cadence. STND.TEST.8 limits reuse to "a later run of a test in a selection". The Notes give the reason (the run audits the derivation from which keys are computed; AGENT.4). Decision 5 of 0.1 is dropped. |
| D2: STND.TEST.3 s1 against s2 and STND.TEST.5; STND.TEST.4 against STND.TEST.5 | Accepted. STND.TEST.3 s1 and STND.TEST.4 s1 hold their tests "in the tiers from which STND.TEST.5 draws the selection"; STND.TEST.4 s2 holds its tests (new, changed, last failed, underived, declared dependences) "from every tier", as pair finding 3 proposes. A test that a row reaches outside the drawn tiers is an omission recorded under STND.TEST.3 s2 and runs at the first merge that draws on its tier, at the latest at depth 0. The choice of tier-bounded rows over rows regardless of tier goes to the custodian (decision 3). |
| D3: STND.TEST.5 against STND.WPROC.9; STND.WPROC.11 lost | Accepted. STND.WPROC 1.1, a minor amendment (GOV.41): STND.WPROC.9 excepts "a check deferred under RSRC.12 to a later merge or to the release, or a test in quarantine under STND.TEST.13, and recorded in the unit record or in a record of STND.TEST.9 that the unit record cites". The Notes of STND.WPROC say how the deferral and quarantine work. Applied in the same round after STND.TEST. |
| D4: integration depth undefined for a release, a merge into a main line, a parent merged into a descendant; circular | Accepted (lead). The Term counts the branches on the path of parent branches from the target branch to the first development line or main line, the target included; a merge into a main line advances it, a release, and has no depth. STND.TEST.5 applies to the merge of a branch into its parent, by a rule that covers every depth. The TEST.9 Revision row reads "the merge, with its integration depth, or the release". The Notes treat parent-into-descendant merges, flat hierarchies, and the limits of depth as a proxy. |
| S1: means unavailable | Accepted. STND.TEST.2 admits a statement of the repository configuration beside a tool, and the Notes give the fallback: STND.TEST.4 s2 holds every test that no derivation covers. No fixed fallback rule is added to STND.TEST.3, because STND.TEST.4 s2 already fails safe. |
| S2: no row for the build description | Accepted: new row "The build description: each test of each output of each build step whose declaration the change alters, and of each output that depends on those outputs". The Notes claim on STND.TEST.10 now rests on that row. |
| S3: platform missing from Verdict input | Accepted, with pair finding 6 (lead): the Term adds each item of the execution path that runs the test that the record of HW.3 identifies; STND.TEST.4 has a row for an item of an execution path or of its reference path; the TEST.9 Revision row adds the execution path. |
| S4: STND.TEST.12 s1 has no end | Accepted: s1 opens "Until a diagnosis names the cause of a failure". |
| S5: "every order", "every subset" not checkable | Accepted: "alone and in each order that a full-suite run uses"; s2 keeps each declared dependence. The Notes mark the evidence for shuffled order as summaries and extracts. |
| S6: no-threshold rule generalizes | Accepted: STND.TEST.17 s2 is limited to coverage of the code. The Notes say a project that wants a coverage gate records it under REPRO.7, and that a mutation score is an indicator with no rule on its threshold. Kept as decision 5. |
| S7: overlaps | (a) STND.TEST.19 s2 drops "or be labeled a regression guard" and asks the source of the expected value and whether it is independent; VV.7 keeps the label. (b) STND.TEST.12 s1 keeps only the case of a rerun under the same key or one that differs in a seed or a drawn input. (c) The Excluded tests row of STND.TEST.9 keeps the counts only, and the Notes cite AGENT.47 and STND.WPROC.13 for the reasons. (d) The Notes say STND.TEST.6 makes the broader checking of RSRC.11 at release the full suite, on the ruling. |
| S8: Notes facts | Accepted, each: "recently failing" removed from the claim about tools (only new tests run unconditionally, S15; the rest rest on safe selection); isolation conditioned on the build enforcing it (S19); rerun arithmetic, the constant-function limit, and the omitted requirement marked as t2's inferences; mutant detection marked as a search summary of an unread study; agent-benchmark rates marked as search summaries and a secondary excerpt; "27 reported bugs in three tools, 14 of them confirmed or already known"; the 170 and 10,000 figures marked as from studies whose methods t2 did not read. |
| S9: release timing; "full suite" scope | Accepted: STND.TEST.6 s1 completes the run "before the release record of an advance of a main line is presented under STND.WPROC.13", on the revision that the proposal names. The Term Full suite holds every test that the work holds, skipped, disabled, and quarantined tests included, so that a configuration listing fewer tests does not narrow it; the Notes say how skipped and quarantined tests are reported. The Optional item that the suite passes is left to STND.WPROC.14, as the review proposes. |
| S10: Terms | Accepted: "Reference oracle" is imported by its Lexicon name, and STND.TEST.15 uses it. Tier and Selection keep their names; there is no clash in scope. |
| S11: onset | Accepted: the INTPR.7 comparison is dropped, and the Notes say STND.TEST.12 rests on VV.1, QA.6, and VV.5. The reading of STND.TEST.2 against the QA.14 row is stated as a reading and goes to the custodian (decision 4). |
| S12: date | Accepted: DATE is 2026-10-25 in every script; the AT values are placeholders on 2026-10-25 for the lead. |
| Optional: "by habit" and "power" | Not changed: these are the custodian's own words ("agents have a habit of excessively running the full test suite, which is a major source of excessive time, power, and other budgets"). The dated narration of the rulings is removed (lead), and only the ruling of 2026-10-25 is named, as the source of STND.TEST.6. |
| Optional: long Notes; indicative obligations | Partly accepted: the restating paragraph of the Notes is reduced to a list of citations; "The full suite runs on the revision ..." is now the content of the ruling and of STND.TEST.6; the deferral to a nearer merge is stated as the consequence of STND.TEST.3 and STND.TEST.5. The paragraphs keep their length, one per group of provisions. |
| Optional: cadence unbounded | No action, as the review advises: the ruling has the project state it. |

## Pair review

| Finding | Disposition |
| --- | --- |
| 1 (Defect): STND.TEST.5 and STND.TEST.3 s2 against STND.WPROC.9 | Resolved by cold D3: STND.WPROC 1.1. The unit record states the deferral or cites the record of STND.TEST.9, in the amended STND.WPROC.9, as the lead directs, rather than in STND.TEST.3. |
| 2: quarantine against STND.WPROC.9 | Accepted: STND.WPROC.9 1.1 excepts a test in quarantine under STND.TEST.13. STND.TEST.13 cites QA.6, and the Notes of STND.TEST and of STND.WPROC say that quarantine is not the restoration that QA.6 asks for a check the change broke. |
| 3: STND.TEST.4 against STND.TEST.5 | Accepted as cold D2. |
| 4: deferred checks and AGENT.47 / STND.WPROC.13 | Accepted in the Notes: an omitted affected test is a check deferred under RSRC.12 and, until a run holds it, a skipped check under AGENT.47; the run that holds it closes the deferral, so STND.WPROC.13 carries only an open deferral. No body text is added, because AGENT.47 binds already. |
| 5: Partial oracle against NUMER.6, STND.VVUQ.18, VV.7 (pair 160) | Accepted: the Term reads "agreement with another implementation that is not a reference oracle"; STND.TEST.15 s1 has the test state the partial oracle and its kind "as the reference of the test"; the Notes say that an implementation produced without the code is a reference oracle and one that shares code, data, or method is a partial oracle. |
| 6: hardware as a verdict input | Accepted as cold S3 (lead). |
| 7: reseeding outside numerical comparisons (pair 254) | Accepted: STND.TEST.12 s1 also covers a key that differs only in a random seed or a drawn input. The Notes say NUMER.26 still bars a reseeded stochastic comparison during the experiments of STND.TEST.11; no body clause is added there, since NUMER.26 binds. |
| 8: changed expected value (pairs 283 to 285, 297, 306) | Accepted: STND.TEST.19 s1 adds "or gives another expected value or reference". The Notes cite STND.VVUQ.17 for numerical guards. |
| 9: STND.TEST.8 and STND.TEST.9 against STND.BUILD.23 s2 | Accepted: STND.TEST.8 s2 adds "or reads a secret" (PRIME.10 in refers_to); the Term Verdict key leaves out a secret. The Notes give the reason. |
| 10: STND.TEST.6 and the release decision | Accepted as cold S9. |
| 11: integration depth | Accepted as cold D4. |
| 12 (Optional): inconclusive verdict (HDES.6) | Accepted: the Terms say that a verdict reported as inconclusive is a verdict that does not pass. |
| 13 (Optional): restatements | (a) As cold S7. (b) Kept: the key is defined by verdict inputs, which add seeds, other tests, and the execution path to what STND.BUILD.23 holds; the Notes call STND.TEST.8 the test form of STND.BUILD.23. (c) STND.TEST.10 s1 is kept because the custodian's scope asks for it explicitly; it adds the limit "only" and the tests that failed at their last run. The restating Notes paragraph is cut to citations. |
| 14 (Optional): facts | Accepted: STND.CREW.17 audits CSQ3 work too, along the dimensions the lead agent records; STND.VVUQ.64 and NUMER.26 are cited apart. The dates are consistent at 2026-10-25. The copy reads 1.0 and its entry number by composition, as above. |

## Amendments

| Amendment | Content | Class |
| --- | --- | --- |
| STND.WPROC 1.1 | STND.WPROC.9: the exception covers a check deferred under RSRC.12 to a later merge or to the release, and a test in quarantine under STND.TEST.13, recorded in the unit record or in a record of STND.TEST.9 that the unit record cites; refers_to adds STND.TEST.13 and STND.TEST.9. Notes: the tier deferral of STND.TEST.5, quarantine and QA.6, and STND.TEST for selection and the full-suite run. | Minor (GOV.41): the text of a default changes, so what a project replaces changes; no obligation grows, since RSRC.12 already admits the deferral and STND.TEST.5 and STND.TEST.6 close it before the development line and the release. Onset stays CSQ3. |
| STND.CREW 1.1 | STND.CREW.9: self-review runs the tests that STND.TEST.10 selects. STND.CREW.15: the review agent receives the record of STND.TEST.9 of each run on which the change relies. Notes updated to match. | Minor (GOV.41): two defaults change their text; the obligations they rest on (VV.8, RSRC.11, QA.7, QA.8) are unchanged. Onset stays CSQ3. |

## 0.2 to 0.3

Cold verification of draft 0.2: verify-0.2.md. New in this step: draft-0.3.md, STND.WPROC-0.3.md, STND.CREW-0.3.md, pairs-0.3.md, pairs-0.3-delta.md. The round script now applies apply_mnem_perf and apply_perf first, then the TEST row after the PERF row (apply_mnem_test.ROW_AFTER is set to apply_mnem_perf.ROW at run time), STND.TEST, STND.WPROC 1.1, and STND.CREW 1.1.

| Finding | Disposition |
| --- | --- |
| X1: STND.DEPS absent from References | Accepted: the Notes cite STND.DEPS.6 for the integrity digest that a verdict key holds; References now list STND.DEPS. |
| S1: skipped or disabled tests escape the full-suite run | Accepted, as the lead directs: the Term Full-suite run executes each test of the full suite, skipped, disabled, and quarantined tests included. The TEST.9 Verdicts row reports their verdicts apart, and the Notes say the skip or disablement still reaches the human owner through AGENT.47 and STND.WPROC.13. |
| S2: nothing limits a pre-merge run to its selection | Accepted in STND.TEST.10, retitled "Runs on a branch": its second sentence has each run before the merge of a branch into its parent hold only the selection of STND.TEST.3, STND.TEST.4, and STND.TEST.5 for the change that the merge brings. Its three sentences are one rule, and the Notes say so (the g.18 notice stays). |
| S3: TEST.5 does not carve out TEST.4 s2 | Accepted: TEST.5 s1 reads "other than the tests that STND.TEST.4 holds from every tier". |
| S4: TEST.3 s1 catches a full-suite run | Accepted: "Where a run of tests is not a full-suite run". |
| S5: TEST.11 against PRIME.10 | Accepted: "the output that the assertion judged, a secret excluded", with PRIME.10 in refers_to. |
| S6: CREW.9 cites a provision that does not select | Accepted: "the tests that STND.TEST.3 and STND.TEST.4 select for the change", in the body, the Notes, and the rationale; refers_to is STND.TEST.3 and STND.TEST.4. |
| S7: Notes fact | Accepted: "10 of 32 concurrency cases were non-determinism in the code under test". |
| S8: onset sentence | Accepted: "the first sentence of STND.TEST.15" among those from CSQ3. |
| S9: indicative obligations in the Notes | Accepted in all three: the TEST sentence on quarantine is cut and replaced by QA.6 and the reading of quarantine as a disabled check under AGENT.47; the WPROC Notes read "STND.TEST.3 and STND.TEST.5 have a test ... run at the first merge ..." and "STND.WPROC.9 has the unit record state ..."; the CREW Notes read "STND.CREW.15 has it receive the record". |
| S10: CREW.15 list grammar | Accepted: the record of STND.TEST.9 follows the explanation of AGENT.2, ahead of the group that the work report states. |
| S11: TEST.19 omits quarantine | Accepted: "places in quarantine" is added, and the Notes call quarantine a disabled check under AGENT.47. |
| S12: rationales | Accepted: the WPROC rationale reads "loses the authority of STND.WPROC.11 to merge without a decision of the human owner"; both rationales justify the class by the test of STND.IDENT.3 (WPROC alters a permission; CREW alters two obligations of defaults), and the WPROC rationale drops "no obligation grows". |
| TEST.2 onset | The Notes say that a statement of the repository configuration is a record a person reads and keeps, which identifies no affected dependent by itself, so it is no mechanism under the row of QA.14; a deriving tool is such a mechanism, which QA.14 asks from CSQ2. It stays a decision for the custodian. |
| O1: reference path in Verdict input | Accepted. |
| O2: TEST.8 s2 three conditions; trailing "where" in TEST.4 cells | The two cells are rewritten without "where". TEST.8 s2 keeps one condition with three alternatives, read as one condition, and findings flag nothing. |
| O3: partial oracle and NUMER.6 | Accepted in the Notes. |
| O4: source of "the studies" | Accepted: "the studies of t1, H1". |
| Coalesce: STND.PERF | Accepted: the Notes read "The evaluation of performance belongs to STND.PERF, whose STND.PERF.23 holds the regression guard on time"; References list STND.PERF. |

# Dispositions: STND.TEST 0.3, lead's corrections

Delta verification of draft 0.3: verify-0.3.md.

| Finding | Disposition |
| --- | --- |
| D1: STND.TEST.10 s2 limits the run before a release, which STND.TEST.6 makes a full-suite run | Accepted: s2 opens "Other than a full-suite run under STND.TEST.6"; the Notes say the run before the advance of a main line is the full-suite run of STND.TEST.6, which no selection limits. |
| S1: the rationale omits the pre-merge limit | Accepted: "and runs before a merge to the selection of STND.TEST.5, a full-suite run excepted". |
| S2: the secret exclusion in STND.TEST.11 follows only the last item | Accepted: "the first assertion that failed with its message, and the output that the assertion judged, each kept without a secret". |
| O1: STND.TEST.10 s3 has no antecedent | Accepted: "Where a run on a branch, other than a full-suite run under STND.TEST.6, holds tests that the first two sentences leave out". |
| O2: STND.TEST.5 sets a tier against tests | Accepted: "beside the tests that STND.TEST.4 holds from every tier". |
| O3: "the regression guard on time" against STND.PERF.23's "a quantity" | Accepted: "the regression guard on a performance quantity, time among them". |
