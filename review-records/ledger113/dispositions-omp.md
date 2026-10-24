# Dispositions: STND.OMP 0.1 to 0.2

Reviews of draft 0.1: review-cold-omp.md (cold review) and review-pairs-omp.md (STND.HARN.28 pair review). The reading copy of 0.1 is labeled revision 1.0 because it is composed as it would be adopted; the drafts are 0.1 and 0.2.

Draft 0.2 has 33 provisions, renumbered. Six are new: 12, 16, 22, 24, 27, and 33. The provisions of 0.1 map to 0.2 as follows: 1 to 11 keep their numbers; 12 is 13; 13 is 14; 14 is 15; 15 is 17; 16 is 18; 17 is 19; 18 is 20; 19 is 21, and its third sentence is 22; 20 is 23; 21 is 25; 22 is 26; 23 is 28; 24 is 29; 25 is 30; 26 is 31; 27 is 32. Findings below cite the 0.1 numbers, and dispositions cite the 0.2 numbers.

## Cold review

| Finding | Disposition |
| --- | --- |
| 1: OMP.19 S2 restates STND.CXX.22 | Accepted. Deleted; STND.OMP.21 keeps only the exit through the end of the block, and the Notes say that STND.CXX.22 governs exceptions. |
| 2: OMP.19 S3 puts two prohibitions in one sentence, with a disguised negation, under an unrelated title | Accepted. New STND.OMP.22, "Signal handlers without OpenMP", with two SHOULD NOT sentences on DSGN.15. |
| 3: OMP.22 S3 asks for an update or `always` for every copy back | Accepted as suggested: the copy is one that the reference count does not suppress, namely the release of the last mapping, an update construct, or an `always` modifier (STND.OMP.26). |
| 4: OMP.23 S1 restates HW.4 and omits `requires` | Accepted in part. The first sentence of STND.OMP.28 now asks that each compilation unit with device code declare the reliance in the same requires directive (r3: all units with device code declare the same requirements). The suggested second clause, stating the reliance in the hardware contract, is HW.4 itself, so it is dropped and the Notes cite HW.4. |
| 5: OMP.14 "repeated creation" exceeds r2; merging applies only to a `mergeable` task | Accepted. STND.OMP.15 limits the cutoff to recursive creation and gives the merged case its own sentence for a task with a mergeable clause; the Notes follow. |
| 6: OMP.1 judges deprecation at the earliest revision; SIMPL.6 is a weak fit | Accepted. "No later revision of the specification marks as deprecated"; the citation is SIMPL.4, whose weighing of a dependency includes its active support. The Notes explain why every later revision is used. |
| 7: OMP.7 `copyin` remedy wrong for per-thread values; r2 rule 8 absent | Accepted. The `copyin` alternative is removed from the provision; the Notes say that `copyin` restores only the primary thread's value, so such a value belongs in storage that is not threadprivate. A third sentence covers values across a task scheduling point. |
| 8: OMP.10 S1 covers reads by the writing thread | Accepted. Limited to reads by another thread, with reads of lastprivate and reduction results kept. |
| 9: titles of OMP.12 and OMP.13 do not cover their third sentences | Accepted. Retitled "Critical names and lock scope" (STND.OMP.13) and "Task dependences, waits, and events" (STND.OMP.14). |
| 10: OMP.17 assumes every property has a clause | Accepted. "Set a property of a region that it creates only through a clause of its own construct" (STND.OMP.19); the Notes name the properties that have no clause. |
| 11: OMP.8 offers a barrier, which is not always valid | Accepted. The barrier is dropped; the Notes say why. The overlap with STND.CONC.5 and STND.CONC.12 stays marginal: the provision gives the OpenMP waits. |
| 12: the term "Offload policy" is misdefined | Accepted. Redefined as the setting of the OpenMP runtime, with its three settings, and a new term, Mandatory offload, used by STND.OMP.23 and STND.OMP.31. The Notes say that a false if clause still runs a region on the host under mandatory offload. |
| 13: the Notes overstate the research | Accepted. Full support is now what no documentation read claims (r1); the claim that one implementation accepts removed syntax is deleted; "leading cause" becomes the main causes of mapping errors in one study (r4); `default(none)` makes omissions checkable; nested same-name critical regions do not conform, and the specification warns that this is not sufficient to prevent deadlock; the `fork` sentence is the guidance of the specification as r2 reports it, with STND.CONC.19 governing. |
| 14: narration and indicative obligations in the Notes | Accepted. Paragraph one states the basis without the drafting history. The component, test, MPI, and planned-standard sentences are recast as hazard facts or as citations of the provision that governs. |
| 15: class-onset paragraph | Accepted. RSRC.1 is listed; STND.OMP.28 S2 is placed at CSQ2 because it rests on DSGN.5, and the paragraph says so although it cites HW.19; STND.OMP.30 is placed at CSQ2 on DSGN.5, with HW.5 at CSQ3 noted; the sentence on STND.OMP.2 is split. The paragraph now places every provision, the new ones included. |
| 16: cancellation not covered | Accepted. New STND.OMP.16, "Cancellation enabled and tested": cancellation enabled where code answers a failure by a cancel construct; tests with cancellation enabled and disabled; locks released before a cancellation point. The Purpose names PRIME.4 among the provisions that already bind, and the Notes give the facts from r2. |
| 16, other gaps | Accepted: atomic and plain access, alignment, and critical constructs that do not exclude atomics (STND.OMP.12); device copies of global variables and static self maps (STND.OMP.27); device numbers and the matched release of device allocations (STND.OMP.24); tests under each run-time schedule and binding in use (STND.OMP.33). |
| Optional: OMP.4 title reads as a verb | Accepted: "Correctness with OpenMP disabled". |
| Optional: undefined terms | Accepted: device construct, reference count, merged task, task scheduling point, and cancellation point added to the terms that the OpenMP specification defines. |
| Optional: NUMER in the Purpose but not in References | Accepted: NUMER removed from the Purpose; no provision rests on it. |
| Overlaps table | OMP.19 S2 and OMP.23 S1 resolved by findings 1 and 4. OMP.8 is marginal and kept for the OpenMP waits. The report clause of STND.OMP.23 and the comparison of STND.OMP.31 add the policy runs and the in-region check, which HW.19, HW.9, HW.16, and STND.VVUQ.1 do not give. The rest the review marks acceptable. |

## Pair review

| Finding | Disposition |
| --- | --- |
| Conflict outside the list: OMP.14 S2 against STND.VVUQ.82 (deferral changes the order in which task reductions combine) | Accepted as suggested: "the same, within the agreement that the acceptance criterion fixes" (STND.OMP.15, citing STND.VVUQ.82); the Notes name the order of task reductions as a declared variation. |
| Observation: OMP.11 met by a declared relaxed default | Accepted: "a default memory order that orders them and that a requires directive of its compilation unit declares". |
| Observation: OMP.3 records only start-of-run values | Not changed. HW.3 already asks for the settings able to affect the result, a change during the run included, and the Notes now say so; STND.OMP.19 has libraries leave the caller's settings alone. |
| Observation: OMP.19 silent on `cancel` | Resolved by cold finding 16 (STND.OMP.16). |
| Observation: OMP.19 S2 restates STND.CXX.22 | Resolved by cold finding 1. |
| Observation: no route for a failure of a task or a target region to reach its parent | Not changed. STND.CONC.1, STND.CONC.2, and HW.GPU.3 bind at every class and give the outcome; the routes are general to concurrent tasks, which the Purpose cites. |
| Observation: HW.3, HW.CPU.4, HW.CPU.5, and HW.GPU.4 in no row of a shared-matters table | No action for STND.OMP: HW is the only profile that addresses them, as the review finds. |
| Onsets of OMP.9 to OMP.13 and OMP.19 at CSQ3 against the DSGN.15 verification row | Kept, as the reviewer leaves it: they state what a protocol uses, not how its invariants are verified, as in STND.CONC. The class paragraph says so. |
| Revision label | The reading copy is composed as revision 1.0, the revision of adoption; the drafts are numbered 0.1 and 0.2. |

## Pairs of 0.2

The command pairs gives 477 pairs for 0.2 (pairs-OMP-0.2.md). 144 of them are new, from STND.OMP.12, STND.OMP.16, STND.OMP.22, STND.OMP.27, and STND.OMP.33; the rest map to pairs of 0.1 reviewed in review-pairs-omp.md. The new pairs, and the provisions of 0.1 whose text changed, go to a delta pair review (review-pairs-omp-0.2.md).

# Dispositions: STND.OMP 0.2 to 0.3

Cold verification of draft 0.2: verify-omp-0.2.md. Numbering is unchanged from 0.2.

| Finding | Disposition |
| --- | --- |
| D1: STND.OMP.28 S2 "that requirement" has no antecedent; "the same requires directive" imprecise | Accepted: S1 "by a requires directive with the same clauses"; S2 "Where no device that a run uses meets the requires directive of a component that relies on shared memory". |
| D2: STND.OMP.16 S1 against S2 | Accepted: "each run of that code, other than a test run with cancellation disabled, SHOULD have cancellation enabled". |
| D3: class paragraph | Accepted. Rewritten: the second sentence of STND.OMP.11 is listed apart from its first; the first and third sentences of STND.OMP.16 are protocol rules and its second is a test under VV.1; the tests of STND.OMP.4, 16, 31, and 33 are said to rest on no row because none compares with an oracle produced without the implementation it judges, the host reference of STND.OMP.31 being the reference path of HW.15; every provision is placed, and the onset of each bundle is stated. |
| D4: Notes claims not in r1 to r4 | Accepted. The `copyin` fact is marked unverified; the barrier clause and the sentence on properties without a clause are deleted; the false if clause under mandatory offload is marked an inference from r3; "final public draft" becomes "the latest technical report toward 6.1, its second preview"; the full-text claim is deleted. |
| D5: RATIONALE claims a review of 0.2 that is not recorded | The delta pair review (review-pairs-omp-0.2.md) was running at the time of the verification; the rationale is checked against its result before ratification. STND.OMP.24 produced no listed pairs and is in the delta review's hand checks. |
| S1: narration and restatement of STND.VVUQ.82 | Accepted: the sentence now says that STND.VVUQ.82 governs the variation; the repetition in the schedule paragraph and the method sentence are deleted. |
| S2: obligations in the indicative | Accepted: the requirements of the specification are stated as such (barriers and worksharing, atomic access, depend items, requires in every unit, signal handlers); the sentences on the team size, the paired release routine, and the scope of atomics are recast as facts. |
| S3: the high-assurance subset as a means of meeting STND.CONC.28 and STND.OMP.2 | Accepted: cut; the Notes say that the literature proposes the subset as the basis of certification (r4). |
| S4: STND.OMP.27 S1 allows only an update construct | Accepted: "by an update construct, or by a map with an always modifier". |
| S5: the Notes read HW.3 as covering a change during the run | Accepted: the reading is removed, and STND.OMP.3 records each internal control variable at the start of the run and after each change that the code makes to it. |
| Pair obs 4 partly: STND.OMP.21 and cancellation | Accepted: the Notes say that a cancellation transfers control to the end of the canceled region, which STND.OMP.21 admits (marked unverified). |
| Hand notes not in the dispositions (CONC.16 implicit tasks, CONC.10) | Wording notes of the 0.1 pair review; no change, because STND.CONC.16 and STND.CONC.10 apply to every concurrent task and an OpenMP thread or task is one. |
| Optional: STND.OMP.24 S1 rejects the initial device | Accepted: "the default device, the host device, or one that the code has checked". |
| Optional: "run-time schedule" in STND.OMP.33 | Accepted: "each schedule and each binding of threads to places that the runs of the work set through internal control variables". |
| Optional: STND.OMP.8 overlap | Kept, as in 0.2. |

## Delta pair review of 0.2

Review: review-pairs-omp-0.2.md (144 new pairs, STND.OMP.24 and the changed provisions by hand). No listed pair conflicts and no matter is unowned. Its findings are answered in 0.3 as follows.

| Finding | Disposition |
| --- | --- |
| Conflict within the standard: STND.OMP.12 S1 against STND.OMP.22 for a location that a signal handler shares | Accepted. STND.OMP.12 gains a third sentence: code does not access a location that a signal handler accesses by an atomic construct, so S1 does not reach such a location. The Notes leave it to the atomics of the base language (STND.CXX.23 for C++) and say that the interoperation of the two kinds of atomics is not established. |
| Obs 2: STND.OMP.16 S1 against S2; S2 does not say what the disabled run shows | S1 resolved in 0.3 (cold verification D2). S2 now says that the disabled run shows that the code does not pass over the disabled state silently. |
| Obs 3: "answers a failure" too narrow | Accepted: "relies on a cancel construct" in both sentences; the Notes name STND.CONC.10 and STND.CONC.12. The cancellation point in long-running tasks stays with STND.CONC.13. |
| Obs 4: run record omits cancellation, the run-time schedule, and the default device | Accepted: added to STND.OMP.3. |
| Obs 5: STND.OMP.33 vacuous for fixed schedules; bindings a test machine lacks; libraries | Kept: a loop with a fixed schedule adds no run, which is intended, and the settings are those that the runs of the work set. STND.CONC.27 has a verification state what it does not cover. |
| Obs 6: STND.OMP.24 exempts the default device; null check; "exactly once" without "after the last use" | Accepted: the default device is no longer exempt, only the host device; "exactly once, after its last use"; the Notes cite STND.CODE.7, PRIME.4, and HW.8 for the null check. The partial overlap of S2 with DSGN.14 is kept for the paired routine, which is OpenMP content. |
| Obs 7: STND.OMP.28 cites HW.4 but no longer states anything of the hardware contract | Accepted: HW.4 dropped from the provision; the Notes cite it. "With the same clauses" was already in 0.3. |
| Obs 8: STND.OMP.21 and the cancel construct | Answered in the Notes in 0.3 (marked unverified). |
| Obs 9: STND.OMP.7 S3 broader than the Notes | Accepted: "a task scheduling point of that task at which another task is able to run on its thread". |
| Obs 10: STND.OMP.1, drafts of a revision | Accepted: "no later revision of the specification, published or in public draft". |
| Obs 11 | Resolved with the conflict above. |
| Obs 12: under mandatory offload, a false if clause asks no report in the first alternative | Accepted: the Notes say so and name HW.19, HW.9, and the host-path test of S2. |
| Obs 13: STND.OMP.26 S3, release copies back only under from or tofrom | Accepted: "the release of the last mapping of that data under a map type that copies it back". |
| Obs 14, 15 | No action, as for 0.1. |
| GOV.31: STND.OMP.12 S1 in part restates STND.CONC.3 | Kept: the OpenMP content is that the protection of an atomically accessed location is the atomic construct and not a critical construct or a lock, which the Notes give. |

The pairs of 0.3 (pairs-OMP-0.3.md) are the same 477 as those of 0.2.

# Dispositions: STND.OMP 0.3 to 0.4

Cold verification of draft 0.3: verify-omp-0.3.md. Numbering is unchanged.

| Finding | Disposition |
| --- | --- |
| B1: STND.OMP.12 S3 "by an atomic construct" attaches to the handler | Accepted: "Code SHOULD NOT use an atomic construct to access a storage location that a signal handler accesses." |
| B2: 6.0 did not remove every 5.x deprecation (r1: destroy on depobj undeprecated) | Accepted: the exception is stated. |
| B3: not every initial value of an internal control variable is implementation defined | Accepted: "most of the internal control variables that STND.OMP.3 names" (r2 lists seven; cancellation starts false). |
| B4: STND.CONC.24 misquoted | Accepted: three or more numbers, among them the smallest that a component admits. |
| B5: RATIONALE stale and cut off | Accepted: "requires directives with the same clauses", "each schedule and binding of threads that the runs set", "no matter left without an owner in a shared-matters table"; the review list names the pair review of the changes. |
| Title of STND.OMP.12 does not cover S3 | Accepted: "Locations accessed atomically". |
| Handler sentence in the Notes indicative and uncited | Accepted: "STND.OMP.12 keeps atomic constructs off a location that a handler accesses, and the standard of the base language governs the access of the handler to it". |
| Default device set by the environment not in r1 to r4 | Marked unverified. |
| Threadprivate qualifier attributed to r2 | Accepted: the qualifier is stated as an inference from r2, rule 8. |
| `fork` guidance from the Examples | Accepted: "The Examples of the specification warn". |
| STND.OMP.1 "published or in public draft" not in the Notes | Accepted. |
| STND.OMP.16 S1 "other than a test run" a second condition | Accepted: "each run of that code that produces a reported result", a restriction of the subject and no second condition. |
