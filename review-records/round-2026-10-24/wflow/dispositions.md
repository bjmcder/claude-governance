# Dispositions of the reviews of STND.WFLOW draft 0.1

Draft 0.2 is in `draft-0.2.md`, its pairs are in `pairs-0.2.md` (481 pairs), and the content module is `tools/amendment-scripts/content_wflow.py`. The rehearsal applied `apply_build_round.py`, then `apply_wflow_round.py`, then `apply_conc_1_0_1.py` with STND.WFLOW.34 changed to STND.WFLOW.32 (scratch copy `.scratch/wflow/apply_conc_1_0_1_renum.py`). All eight checks of verify pass. `findings.py 'STND\.WFLOW'` reports one g.18 notice, for STND.WFLOW.7: its three sentences are the steps of one publication, and the Notes say they apply together. STND.WFLOW now cites STND.BUILD, so its round has to run after the round of STND.BUILD.

## Numbers from 0.1 to 0.2

| 0.1 | 0.2 | 0.1 | 0.2 |
| --- | --- | --- | --- |
| 1 to 6 | 1 to 6 | 23 | 22 |
| 7, 8 | 7 | 24 | 23 |
| 9 | 8 | 25 | 24 |
| 10 | 9 | 26 | 25 |
| 11 | 10 | 27 | 26 |
| 12 | 11 | 28 | 27 |
| 13 | 12 | 29 | 28 |
| 14 | 13 | 30 | 29 |
| 15 | 14 | 31 | cut |
| 16, and 40 sentence 2 | 15 | 32 | 30 |
| 17 sentence 1, 18 sentence 2 | 16 | 33 | 31 |
| 18 sentence 1, and a new sentence 2 | 17 | 34 | 32 (cited by STND.CONC 1.0.1) |
| 19 | 18 | 35 | 33 |
| 20 | 19 | 36 | 34 |
| 21 | 20 | 37 | 35 |
| 22 | 21 | 38, 39 | 36 |
| 17 sentence 2 | Notes | 40 sentence 1 | Notes |
| 41 to 44 | 37 to 40 | | |

## Lead decisions

| Item | Disposition |
| --- | --- |
| 1 Build boundary (R2) | Done. The sentence "a build system is a workflow engine" is gone. Purpose and Notes now state the rule: the steps that build software are governed by STND.BUILD, and STND.WFLOW governs the publication, retry, restart, storage, and resumption around them. The Notes cite STND.BUILD.1, .3, .23, and .25, and name STND.BUILD.23 as the build form of STND.WFLOW.6. Each overlap is resolved in one direction, with STND.WFLOW deferring to STND.BUILD for build steps: .1 with BUILD.1, .6 with BUILD.23, .2 with BUILD.3, and .35 with BUILD.25. |
| 2 Class onsets (R8) | Done. Parts that rest on a row of STND.CLASS.10 apply from that row's class. CSQ1: 3 sentence 2, 21 sentence 2, 22, and 33 (DSGN.2 postconditions). CSQ2: 24 sentence 2 and 35 (REPRO.4). STND.WFLOW.25 and .27 stay at CSQ3, argued as precondition checks where data enters (DSGN.2, sentence 1); that is the row's own reading, not a departure. One argued departure goes to the custodian: 2 sentence 2 and 6 sentence 1 stay at CSQ3 and do not move to the QA.14 row. The Notes give the reason: they state which steps run again and ask for no tracking mechanism. |
| 3 Proportion | Done. 31 is cut. 39 is merged into 36, 8 into 7, and the event-ordering sentence of 40 into 15; the clock point of 40 is in the Notes only. The table above maps the numbers. |
| 4 Terms (R12) | Done. Part is replaced by Step set and Set member, and "portion" is used elsewhere. Step now includes steps performed by people and agents, and Purpose says which provisions reach them. Job (defined by its limit on duration) and Scheduler (one that grants a limit on duration, for a computing system or a platform) no longer define each other. Generation is "meant to be complete". Safe point is defined, and the Notes set it apart from PRIME.13. Temporary item: the Notes say which records cite which items. Restart state is tied to the "checkpoint" of STND.VVUQ.2 and of the Notes of STND.VVUQ, in Terms and in Notes. Attempt is distinguished from STND.DFLT's "attempt without progress". The unused imports Capacity and Operator are dropped. |
| 5 Notes | Done. The PRIME.7 sentence and the agent's enumeration are now citations: "PRIME.7 governs a write to a remote system by an agent", and "GUARD.5 and GUARD.6 govern ..., and STND.DFLT.14 and STND.DFLT.24 govern the scope". The "only" of STND.DFLT.15 is corrected, and the claim "work directories are records" and the VVUQ.1 tier clause are deleted. STND.WPROC is cited through STND.WPROC.1 and now appears in References. Narration of drafting: none remains. The Notes also lost three more sentences that read as indicative obligations (staging, test size, PRIME.4 at the attempt); each is now a citation. |
| 6 Means unavailable (R10) | Checked every provision. 7 sentence 2 now admits a marker of completion where storage offers no atomic naming. 4 sentence 2 states how an effect is made once, by a key or by not running again an attempt that made it, so a receiving system without keys blocks nothing. 30 checks the quotas "that each such file system reports". No other provision depends on a means that is able to be missing. |

## Cold review

| Finding | Disposition |
| --- | --- |
| D1 Conditions after their clause | Fixed: 10 sentence 2 (0.1's 11) is now a negative after a condition placed first; 19 (20) as proposed; 21 sentence 2 (22) as proposed; 22 (23) is "Before each process ... SHOULD NOT count as valid", which keeps "only". Also 3 sentence 2 drops "only on", and 2 sentence 2 carries one condition. |
| D2 False onset sentence; 3, 25, 35 | Fixed under lead decision 2. DSGN.2 is now an ancestor of 3, 21, 22, and 33, and REPRO.4 of 24, and the onset paragraph is rewritten. |
| D3 STND.WPROC missing from References | Fixed: the Notes cite STND.WPROC.1, and References lists STND.WPROC. |
| S4 Build boundary | Fixed (lead decision 1). |
| S5 Part | Fixed: Step set and Set member. |
| S6 Step against Workflow | Fixed: the Step definition and the third paragraph of Purpose. |
| S7 Job and Scheduler | Fixed. |
| S8 37.1 restates REPRO.1 | Fixed: 35 lists only the additions (reuse key, resource request, attempt, times, and the generation continued from) and cites REPRO.1. |
| S9 QA.14 | Argued in the Notes. Sent as decision 3. |
| S10 Checkpoint vocabulary | Fixed in Terms and Notes. Where the Notes use the word, it is the sources' word, in quotation marks on first use. |
| S11 Notes errors | Fixed (lead decision 5). |
| S12 Generation | Fixed. |
| Optional: 40 sentence 1 DSGN.5 | Moot: the sentence is now in the Notes. |
| Optional: Capacity unused | Dropped. |
| Optional: split "or" in 4 sentence 2 and 19 | 4 is rewritten. 18 (0.1's 19) is kept: its alternatives are means to one outcome, and no negation is involved. |
| Overlaps: 24.1 random streams against VVUQ.2 | Kept; the Notes say that 23 reaches every acceptance criterion and VVUQ.2 reaches only bitwise identity. |
| Overlaps: 31 cut; 39 merged; 40.1 to the Notes | Done. |

## Pair review

| Observation | Disposition |
| --- | --- |
| 1 DFLT.15 "only" (Defect) | Fixed: "where the item is a temporary item or belongs to another exempt class ..., content regenerable from recorded inputs among them". |
| 2 Indicative obligations (Defect) | Fixed (lead decision 5). |
| 3 Identity omits the environment | Fixed: 24 sentence 2 adds the identity of the computational environment, and the Notes add it to the reasoning. |
| 4 Key of an effect across a resumption | Fixed: the key identifies the step and its inputs and is the same for each attempt; the Notes say why it survives a resumption. |
| 5 Resumption record | Fixed: 36 adds each job submitted and not known to have ended; 19 adds the resumption record to what stays valid after a forced end. |
| 6 Notice and a job of several processes | Fixed: 17 sentence 2 has the processes that receive a notice pass it to those that write the same generation, and the Notes give the reason. |
| 7 Rerun against the staleness rule | Fixed: 28 reruns members "not completed or not current under the rule of STND.WFLOW.6"; 2 sentence 2 reruns dependents only where the output differs from the stored one. |
| 8 Agreement of tests 42, 44 | Fixed: 38 and 40 compare "within the agreement that the acceptance criterion fixed and at the tier that STND.VVUQ.1 gives" (VV.3). |
| 9 Temporary items and the record | Fixed in the Notes: records cite final outputs and restart state; a step's work area created as a temporary location holds temporary items. |
| 10 Missing member, the floor | Fixed in the Notes: PRIME.4 and INTPR.7 govern the report, and NUMER.22 and NUMER.23 govern selection by outcome. |
| 11 Safe point | Fixed: defined in Terms; the Notes say PRIME.13 governs a step that commands hardware. |
| 12 Retry with less work | Fixed: 13 sentence 2 states the change in the record of each result (INTPR.9); the Notes add PRIME.4 at the attempt. |
| 13 Volume and onset of anomalies | Wording fixed ("reported by step and by class of failure"). The onset stays at CSQ1, the INTPR.7 row, under lead decision 2. |
| 14 Generation continued from | Added to 35. |
| 15 Scheduler and file system in an execution path | Added to the Notes: one statement serves STND.WFLOW.16, STND.WFLOW.32, and HW.4. |
| 16 Manual actions at resumption | Added to 36. |
| 17 Status hides a failed write | Added to the Notes through STND.CODE.7. |
| 18 Size of tests, RSRC.12 | Added to the Notes as a citation of RSRC.12. The points of forced end tried are left to STND.CONC.27. |
| 19 Run-level retry budget | Declined. 11 bounds each step, and GUARD.15 already halts an agent before a limit. |
| 20 VVUQ.1 tier clause | Deleted. |
| 21 Terms imports; Attempt; checkpoint word | Fixed (lead decision 4). |
| 22 HW.13 and HW.5 for restart state across models | Added to the Notes. |
| 23 35 bundled at CSQ2 | Stated in the Notes as the intended choice. |
| 24 Moving figures | Kept as evidence of a hazard. The first paragraph of the Notes now says that they are one product's or one site's values and that no provision relies on them. |
| 25 Reading copy says 1.0 | Inherent to the rehearsal; the lead sets times and rationale at the coalesce. The rationale is still a placeholder. |
| 26 Archive-first direction | Declined for the Notes. It is the custodian's direction to the agents of this round, not adopted governance; the Notes cite GUARD.5, GUARD.6, STND.DFLT.14, and STND.DFLT.24, which govern removal by an agent. |

## Decisions for the custodian added in 0.2

1. Onsets of 3 sentence 2, 21 sentence 2, 22, and 33 at CSQ1, following the DSGN.2 row. Recommend following the row, as STND.CONC and STND.OFFLD do. PRIME.4 still binds a check that is run and fails.
2. STND.WFLOW.25 and .27 at CSQ3, as checks of preconditions where data enters. Recommend this reading.
3. The second sentence of 2 and the first sentence of 6 at CSQ3, not at the QA.14 row. Recommend CSQ3: they state which steps run again, which every workflow engine does, and ask for no tracking mechanism.

## Draft 0.3: the verification of draft 0.2

Draft 0.3 is in `draft-0.3.md`, and its pairs are in `pairs-0.3.md`. The provision numbers are those of 0.2. The rehearsal ran `apply_build_round.py`, then `apply_wflow_round.py`, then the live `apply_conc_1_0_1.py`, which cites STND.WFLOW.32. All eight checks of verify pass. `findings.py 'STND\.WFLOW'` reports one g.18 notice, for STND.WFLOW.7, and its three sentences apply together, as the Notes say. A copy of the 0.2 content is kept in `.scratch/wflow/content_wflow_v02.py`.

| Item | Disposition |
| --- | --- |
| N1 Two completed attempts | Fixed. The Notes no longer claim that STND.WFLOW.7 publishes only one attempt. They say that STND.WFLOW.9 gives each final name one step, and cite STND.WFLOW.5 (later attempts give the outputs of a single attempt) and STND.WFLOW.36 (jobs not known to have ended). |
| N2 WFLOW.35 sentence 1 | Fixed: "Beyond the items that REPRO.1 and REPRO.4 ask ..., that provenance SHOULD also give". |
| N3 WFLOW.22 | Fixed: "Before every process ...". |
| N4 Bundle of WFLOW.35 | Fixed. The onset paragraph names the second sentence of STND.WFLOW.35: it rests on REPRO.12 and INTPR.9, which rest on no row, and it applies with the first sentence from CSQ2, as one bundle. |
| N5 Build boundary in bodies | No change. The direction is the same and there is no conflict, as the verification found. |
| N6 WFLOW.11 sentence 2 | Fixed. The backoff rule now rests on DSGN.1 and applies from CSQ3. The Notes say that the rule of delay is part of what the contract of the retrying step preserves: the shared service that its attempts reach. DSGN.5 is no longer cited there. |
| N7 Manual steps and exit status | Fixed. STND.WFLOW.3 sentence 2 counts a step as completed by the passing of its checks, "and not by the exit status of its last attempt alone", so a manual step without an exit status meets it. Purpose names 1, 3, the first sentence of 4, and 36. |
| N8 WFLOW.4 | Fixed: "by not running the step again after an attempt that made the effect". |
| N9 WFLOW.7 sentence 2 | Fixed: "or mark it complete with a marker that the step writes last". |
| Decision 3 (QA.14) | The row is followed. STND.WFLOW.2 and STND.WFLOW.6 instantiate QA.14. Their sentences that decide the dependent steps, the second of 2 and the first of 6, apply from CSQ2, and the Notes say so. The decision is withdrawn from the custodian's list. |
