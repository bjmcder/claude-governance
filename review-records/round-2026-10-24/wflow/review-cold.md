# Cold review of STND.WFLOW draft 0.1

## Verified by script
- `govharness verify` on the rehearsal: all checks PASS. The one g.18 warning (modals per provision) also appears on the live corpus, so it is not WFLOW's. `findings.py 'STND\.WFLOW'` prints nothing.
- All 44 provisions: mode default, `binding_reason` null; titles at most six words and distinct corpus-wide; one modal per sentence; body identifiers equal `instantiates` plus `refers_to`; ancestors only DSGN, SIMPL, REPRO, RSRC, INTPR, VV.
- No word from the STND.DRAFT.13 or .17 tables. No engine, scheduler, file system, format, or product is named in a provision.
- None of the 20 new terms clashes with the Lexicon or another Terms table.
- Every W and S identifier in the Notes exists in w1 and c3; every row the research marks search extract, unverified, or not read is marked so in the draft; the figures cited match the research. HANDOFF supports the custodian's order of standards.
- Condition scan (STND.DRAFT.16): defect 1.
- By hand only: overlaps, onsets, Notes accuracy. Not checked: the primary sources behind w1 and c3.

## Defects
1. **Conditions after their clause or doubled (STND.DRAFT.16).**
   - WFLOW.11 sentence 2, "only after a failure". Fix: "After a failure that its declaration classifies as one that a retry is able to clear, a workflow SHOULD retry the step."
   - WFLOW.20, "remain valid after a forced end". Fix: "After a forced end at each point at which a workflow run writes them, each record of completed steps, cache, and index that a later run reads SHOULD be valid."
   - WFLOW.22 sentence 2, "keep ... until". Fix: "Before a job has checked a newer generation, it SHOULD NOT remove its last valid generation."
   - WFLOW.23 has "Where" and "only after" in one sentence. Fix: "After each process that writes a part of a generation has written and checked it, that generation SHOULD count as valid."
2. **The onset paragraph is false for sentences that check a postcondition.** It says the postcondition checking that DSGN.2 asks from CSQ1 is not among the provisions. WFLOW.3 (both sentences) has the workflow check each output as complete. WFLOW.35 has the staging step check its own copy. WFLOW.22 sentence 2 and WFLOW.23 have the writer check its own write. The CSQ1 row of STND.CLASS.10 covers all of these. WFLOW.25 (run identity written with each generation) is provenance written with an output, the CSQ2 row of REPRO.4, yet it sits at CSQ3 with no argument. Fix, either way: move these sentences to the row's class and add DSGN.2 or REPRO.4 as an ancestor. Or keep CSQ3, delete the false sentence, and argue in the Notes on the HW pattern (applies from a less severe class than its row, tightening above the floor, PRIME.15), and send the argument to the custodian as a decision.
3. **STND.WPROC is cited in Purpose and Notes but is missing from the References table** (binding STND.DRAFT.34). `verify` misses it because the citation carries no provision number. Add the row.

## Should-fix
4. **Boundary with the parallel STND.BUILD draft.** WFLOW Notes make a build system that runs workflow steps "a workflow engine under this standard". BUILD draft 0.1 defines Build as the workflow that turns source into outputs, and holds BUILD.1 (declared inputs of build steps), BUILD.3, BUILD.23 (cache keys), and BUILD.25 (record). A compile step is then under two rules on declared inputs (WFLOW.1, BUILD.1) and two on keys (WFLOW.6, BUILD.23). Fix: delete the "build system is a workflow engine" sentence. In Purpose here and in the BUILD Notes, state one rule: a step whose work is building software has its declared inputs, cache keys, and output equivalence under STND.BUILD, and this standard governs publication, retry, restart, storage, and resumption around it. A build tool that runs data or analysis steps is a workflow engine.
5. **The defined term Part is used in other senses.** WFLOW.23 ("parts of one generation"), WFLOW.24 ("each part of that state"), and WFLOW.12 ("a random part") do this, and so do the Step and Declaration definitions. Fix: rename the term "Set member", and use "portion" elsewhere.
6. **Step is narrower than the Lexicon's Workflow** (automated, manual, or agent-performed; REPRO.10 counts manual steps). Fix: say in Purpose that a manual or agent-performed step has its inputs and outputs declared (WFLOW.1) and its completion recorded (WFLOW.38), or that it is out of scope.
7. **Job and Scheduler are circular and too narrow.** A job is what a scheduler starts, and a scheduler grants jobs. Purpose covers "a platform", but the reclaim notice of rented capacity reaches a process that no scheduler started. Fix: define Scheduler as "software of a computing system or a platform that grants...", and define Job by its limit on duration.
8. **WFLOW.37 sentence 1 restates REPRO.1** (input content, code revision, parameters, environment identity). Fix: list only the additions, the reuse key, resource request, attempt, and start and end times.
9. **QA.14 (dependency tracking, CSQ2) is not cited.** WFLOW.2 sentence 2 and WFLOW.6 sentence 1 are that mechanism. Fix: cite it and place them at CSQ2, or say in the Notes that they add only the stated rule.
10. **Vocabulary split.** VVUQ.1 and .2 use "checkpoint" for restart state. Fix: one Terms sentence saying so.
11. **Notes errors.**
    - The VVUQ.1 row says restarts from a checkpoint holding the complete state are tier 1. It does not add "share their numbers of processes". Delete that clause.
    - "The agent enumerates and verifies the scope before it removes anything" and "a retry repeats it within the scope of that authorization" are obligations in the indicative and restate GUARD.6 and PRIME.7. Replace the first with "GUARD.5 and GUARD.6 govern the removal by an agent"; delete the second.
    - "Work directories are records only where a record cites them" is unsupported; delete it.
12. **Generation is a "complete write", yet WFLOW.22 to .26 speak of incomplete generations.** Fix: "meant to be complete".

## Optional
- WFLOW.40 sentence 1 cites DSGN.5 for clocks; DSGN.16 fits better. Move sentence 2 (INTPR.8, CSQ1) to CSQ3.
- Terms import Capacity, but no provision uses it.
- WFLOW.4 sentence 2 and WFLOW.19 each join alternatives with "or"; split them.

## Overlaps
| Provision | Existing holder | Verdict |
| --- | --- | --- |
| 1, 6 | STND.BUILD.1, .23 (parallel draft) | Duplicate for build steps; finding 4 |
| 2.2, 6.1 | QA.14 | Partial; finding 9 |
| 37.1 | REPRO.1, REPRO.4 | Restates; finding 8 |
| 39 | REPRO.1 | Restates; fold into 38 |
| 24.1 (random streams) | STND.VVUQ.2 | Restates for bitwise identity; the wider scope is an addition; shorten |
| 31 | STND.CONC.14, RSRC.1, AGENT.40 | Thin; cut |
| 40.1 | STND.CONC.10 | No overlap; generic, not workflow-specific |
| 16 | STND.CONC.29, INTPR.8 | Adds the field list |
| 18.1 | STND.CONC.13 | Adds status and safe point |
| 32, 33 | RSRC.1, HW.8, DFLT.4, REPRO.12 | Adds (file count, purge); the PRIME.4 reading of quota is sound |
| 17 to 20, 24.2, 38, 41 | MPI.7, CONC.1, .2, MPI.22, INTPR.12 and .13, QA.9 | Add (notice and grace, non-MPI restart state, record content, clean-area run) |

## Onset paragraph, sentence by sentence
Sentences 1, 2, 3, and 7, and the floor claim, are correct. Sentence 4 is correct for 15.2 and 16 and a stretch for 40.2. Sentence 5 is false for 35, and for 3 by implication (defect 2). Sentence 6 is sound, but 23 also checks the writer's output. The closing list matches the script except for 3, 25, and 35.

## Coverage and proportion
All 22 practices of the w1 answer in brief map to a provision. Practice 21's decision step is correctly left out under STND.DRAFT.42. The draft holds nothing it should not, apart from the build sentence and WFLOW.31.

On 44 provisions, I agree with cutting 31. I would also cut 40 as a provision: move its clock sentence to a STND.CONC amendment and fold the sequence-number sentence into 16. Merge 39 into 38 and 8 into 7, giving 40 provisions. Keep each pair of rule and test (5 and 42; 43 and 44). Do not go below 40; the retry, restart, and storage groups each answer a separate hazard in w1.

## Verdict
Revise before adoption. Research fidelity, tighten-only, and agnosticism are sound. The three defects are the condition errors in 11, 20, 22, and 23; the false postcondition sentence in the onset paragraph (with the unargued tightening of 3, 25, and 35); and the missing STND.WPROC reference. The build boundary (finding 4) needs the lead's coordination with the BUILD draft.
