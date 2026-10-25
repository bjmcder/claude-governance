# Cold review of STND.TEST draft 0.1

## Verified by script
- I rehearsed `apply_test_round.py` (copy at /tmp/rehearsal-4y63_5s3/governance). `govharness verify`: all eight checks PASS. `findings.py` for `STND\.TEST`: no finding. The one g.18 warning in verify is not from STND.TEST (all 19 provisions have at most two modals).
- The reading copy equals a fresh compose of the rehearsal.
- All 19 provisions are defaults. Titles have six words or fewer and are distinct corpus-wide. Body IDs equal `instantiates` plus `refers_to`. No banned body word appears.
- By hand only: conditions, onsets, overlaps, and the facts in the Notes against t1 and t2.

## Not checked
- The proposed amendments of STND.WPROC.9 and STND.CREW are not in the files I was given. I judge their need from the draft and the adopted text.
- Primary sources. t1 and t2 are extract-based; I tested the Notes against the notes only.
- The STND.PERF draft, which I did not read.

## The custodian's ruling
- **Dev-line cadence, widening by depth, and the pre-release full suite.** TEST.5 and TEST.6 carry these. TEST.5 widens monotonically (every tier at depth 0, and tiers drawn at a depth are drawn at each smaller depth). This is weak widening: a project that states every tier at every depth complies. The standard cannot force distinct tiers, so I leave it as is.
- **Skipping the full suite before an advance.** TEST.5, .6, .8 and .10 do let an agent do it, by four routes (D1, D2, S5, S9 below).

## Defects

**D1. TEST.8 lets reuse stand for the release run. My reading: it does not meet "the full suite before each main-line advance", and the draft should say so.**
- The only statement that reuse covers the release run is in the Notes: "a verdict whose key is unchanged ... stands for the run before the release under STND.TEST.8". Notes are informative, so the body is silent and ambiguous, and no Term says whether a "run" executes each test.
- Reasons against it:
  - The full run before release audits the selection and the derivation (t1 answer 18, and H3 "Stages": the last stage before use runs everything). A key derives from the same STND.TEST.2 derivation whose misses the audit exists to catch, so the audit would be circular.
  - t1 answer 1 says safety holds only under controlled conditions, and key completeness cannot be shown.
  - t1 marks the carry of a verdict across a branch merge as an unconfirmed synthesis. The Notes admit this, yet the release reading rests on it.
  - AGENT.4 (binding) forbids stating that a check passes without a run against the revision described. WPROC.14 asks for "the outcome of the checks run on that revision". A reused verdict was not run on that revision.
- Fix:
  - Add to TEST.8: "Each test of the full suite that TEST.6 asks to run before an advance of a main line SHOULD run, and no reused verdict SHOULD stand for it."
  - Add a Term: "A run of the full suite executes each test."
  - For the cadence run, which also audits, say that a reused verdict stands for it only if a no-reuse full run covered the same key. Alternatively forbid reuse there too.
- The custodian may decide that hermetic builds justify release reuse. That is a decision for the custodian. I recommend the stricter text, since releases are rare and human-gated.

**D2. TEST.3 s1 contradicts TEST.3 s2 and TEST.5, and TEST.4 and TEST.5 have no stated precedence.**
- s1 says a selection SHOULD hold each test the change is able to affect. s2 and TEST.5 allow omitting affected tests in tiers the depth does not draw on.
- TEST.4 says each selection SHOULD hold the tests of its second column, but not whether that overrides the tier limit. Read literally, a toolchain change at depth 3 pulls in slow-tier tests.
- Fix: "Subject to STND.TEST.5, a selection ... SHOULD hold each test whose verdict inputs the change alters, as the derivation of STND.TEST.2 gives them." Then state that TEST.4 rows count as altered inputs and are held regardless of tier. Or say they are held only within the drawn tiers, with the rest recorded as omissions under TEST.3 s2. The custodian should choose; I recommend regardless of tier, since this is the fail-safe.

**D3. TEST.5 conflicts with STND.WPROC.9, and STND.WPROC.11 is lost.**
- WPROC.9 excepts only a check deferred to the release. Deferring an affected check to a nearer merge is outside that exception.
- WPROC.11 lets an agent merge without the human owner only where WPROC.8 to .10 are met. A project that follows TEST.5 therefore loses that authority or must breach WPROC.9.
- The amendment is needed. Minimal text: "other than a check deferred under RSRC.12 to a later merge or to the release and recorded in the unit record". Align the record place with TEST.3 s2 (run record or unit record).
- Class: I read it as minor under GOV.41, since it widens an exception in a default. This is the custodian's call. It must be ratified in the same round, or TEST.5 should not be adopted.

**D4. "Integration depth" is not defined where it is used.**
- The Term defines depth "Of a merge". The TEST.9 table also uses it "of the release". A merge into the main line (a release, or a fix under WPROC.6 whose most upstream branch is the main line) and a merge into a branch made from the main line have no depth.
- The merge of a parent into a descendant (WPROC.8) is a merge with a depth but needs no pre-merge run.
- The definition is also circular ("number of merges by which a change on its target branch reaches the development line").
- Fix: "Of a merge into a branch other than a main line: the number of branches, the target included, on the path from the target up to the development line; 0 for the development line." Drop "or the release" from the table, or say "none for a release". Say that updates under STND.WPROC.8 are not merges for TEST.5.
- Depth is decidable from history and monotone, and it proxies the custodian's "level of integration" acceptably. It ignores change size and sibling count. A flat hierarchy (all units at depth 1) collapses the widening to one step. Both are fine and need only a Note. TEST.5 "for each integration depth" should read "for each depth, and for each depth beyond the deepest stated" so that an unbounded hierarchy does not need unbounded configuration.

## Should-fix

**S1. Means unavailable (TEST.2, TEST.3).**
- TEST.2 requires derivation "by a tool". Where no tool exists, TEST.4 s2 holds every test, which fails safe, but TEST.3 then has no selection rule to cite.
- Fix: "derivable by a tool or by a statement in the repository configuration". Add a fallback to TEST.3: where no rule is stated, the selection is the tests of the components the change touches and of the components that depend on them (the declared graph of STND.BUILD.1).

**S2. TEST.4 has no row for a change to the build description itself** (a new edge, a changed target). The Notes on TEST.10 claim it reaches every test. Add the row ("the build description: every test of each output the changed step builds, and of each output that depends on them"), or drop the Notes claim.

**S3. "Verdict input" omits the platform** (hardware, operating system, device, runtime library) that runs the test. This matters for numerical and hardware work, and for reuse across hosts. Add "the platform that runs it".

**S4. TEST.12 s1 has no end.** A pass after a failure whose cause is later diagnosed (an outage, say) still cannot count as evidence. Lead s1 with "Until a diagnosis names the cause of the failure," as s2 does.

**S5. TEST.14 "every order" and "beside every subset" are not checkable (GOV.18).**
- Fix: "alone and in each order that a run of the full suite uses".
- s2's random order should "respect each declared dependence". Evidence for shuffling is S13a (a search summary) and S13b and S21 (extracts).

**S6. TEST.17 s2 (no threshold) generalizes.** t2 H5 marks the coverage finding SPECIFIC (five systems, one effectiveness measure). For mutation scores, t2 says "indicator, not a rate" and "do not require 100 percent", which is not a ban on a threshold. Restrict s2 to coverage, or mark it as the project's decision with the finding. It could block a project's coverage gate, which is only a default.

**S7. Overlaps (GOV.31).**
- TEST.19 s2 "or be labeled a regression guard" restates VV.7. Drop it and keep the independence statement.
- TEST.12 s1 overlaps STND.CODE.9's Notes (a varying verdict gives no evidence). Keep only the same-key rerun case.
- TEST.9's "Excluded tests" row partly restates AGENT.47 and WPROC.13. Cite them in the Notes and add only the counts.
- TEST.6 s1 adds "full" to RSRC.11's "at release". That is fine, because it is the ruling; say so in the Notes.

**S8. Notes facts.**
- "Recently failing tests ... run unconditionally in the tools described (t1, answer 6)". t1 supports unconditional runs only for new tests (S15). Remove "recently failing".
- "A test sees only what it declares" is flat. t1 S19 says this holds where the build enforces isolation, and it is not enforced by default. Add the condition.
- Three t2 inferences are stated as literature without a mark: rerun arithmetic ("t2's arithmetic" is an inference by t2), the constant-function limit of metamorphic relations, and "a requirement the code omits has no mutant". Mark each as inference. TEST.15 s2 and TEST.18 lean on the last two.
- "Mutant detection tracked real-fault detection" rests on a search summary of an unread paper (t2 Not verified). Mark it.
- The test-editing rates on agent benchmarks come from search summaries and a secondary excerpt. Mark them. TEST.19 does not depend on the rates, only on the hazard.
- The "27 defects" figure: 14 of the 27 reported bugs were confirmed or known (t1 H1). Write "27 reported bugs".
- Two studies' headline figures (170 and 10,000 reruns) carry t2's caveat that the method was not read. Say so, or drop them.

**S9. Release timing.**
- TEST.6 s1 says "before each advance". The human decides before the advance, on the release record (WPROC.14).
- Fix: run on the revision that the release proposal names, so the outcome is in the record. Add "and the outcome SHOULD be in the release record" only if the custodian thinks WPROC.14 insufficient.
- TEST.6 does not say the suite passes. WPROC.14 carries the outcome, so I leave this Optional.
- "Full suite" is defined by the repository configuration. A configuration that lists fewer tests would meet TEST.6. Quarantined tests (a Term) are not said to be in the full suite. Say that both are, and that skipped and quarantined tests are reported by TEST.9 and WPROC.13.

**S10. Terms.**
- "Reference" is imported from the Lexicon, which defines no such term (only "Reference oracle"). Name the term or drop it.
- "Integrity digest" is defined for a component; the extension to inputs is stated, which is fine.
- "Tier" and "Selection" share names with STND.VVUQ "Comparison tier" and STND.SV "Selection". There is no clash in scope. Optional rename ("test tier").

**S11. Onset.**
- The Notes compare TEST.12's unexplained failure to INTPR.7, which is a CSQ1 row (reporting anomalies). The onset paragraph does not place it. Either drop the INTPR.7 comparison, or say that TEST.12 s2 rests on VV.5 and QA.6 and not on INTPR.7.
- TEST.2 asks for a tool-written dependency record. The onset paragraph argues it is not the QA.14 CSQ2 row. The argument is arguable. State it as a decision for the custodian: a record of what a test read is a dependency record. If the custodian reads it so, the record route in s1 starts at CSQ2.
- The other onsets follow CLASS.10 (CSQ2 for TEST.15 s2; CSQ3 elsewhere).

**S12. Date.** The rationale and the header say adopted 2026-10-24 and cite a ruling of 2026-10-25. The lead sets times at the coalesce; set both consistently.

## Optional
- The Notes say the custodian's concern is that agents run the full suite "by habit, at a cost in time, power". The task text says "too often". Cut "by habit" and "power" so no concern is attributed beyond the custodian's words.
- Notes style (STND.DOCS): no DOCS.9 pattern found by search. Several paragraphs of 300 to 500 words with sentences over 60 words hurt readers. Two Notes passages state obligations in the indicative: "The full suite runs on the revision...", and "A test ... runs at the first merge nearer ... and the record states it". Put the first in a body or recast it as the ruling's content. The second follows from TEST.3 s2 and TEST.5 (the depth-0 merge includes the whole change), so recast it as a consequence.
- TEST.6 s2 puts no bound on the cadence. That is the ruling ("the project states"), so I leave it.

## Overlap table
| Provision | Existing provision | Verdict |
| --- | --- | --- |
| 3 s1 | VV.8, RSRC.11 | Adds the rule; partial |
| 6 s1 | RSRC.11 "at release" | Adds "full"; justify |
| 8 | STND.BUILD.23, RSRC.7 | Adds the test form; conflicts with AGENT.4 as read (D1) |
| 9 excluded row | AGENT.47, WPROC.13 | Partial; cite |
| 12 s1 | CODE.9 Notes | Partial |
| 19 s2 | VV.7 | Partial restatement of the label |
| 10, 11, 13, 14, 16, 18 | CODE.9, QA.4, VV.3 | Adds method |
| (cited only) | RSRC.11, RSRC.12, VV.8, WPROC.9, CODE.8, CODE.9, PRIME.2, AGENT.5, AGENT.47, CREW.15 | Not restated beyond those above |

## Verdict
Adopt after fixes: four defects, none structural. D1 and D3 need the custodian. The amendment of WPROC.9 is needed. I could not judge the CREW amendment.
