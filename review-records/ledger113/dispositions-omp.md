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
