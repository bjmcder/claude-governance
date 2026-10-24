# Cold review of STND.OMP (rehearsed copy)

Verified by script on all 27 files: all default; the `instantiates` closure reaches no PRIME, GUARD, GOV, REPRO.5, QA.1, INTPR.2 or VV.7; body IDs equal `instantiates` plus `refers_to`; titles at most six words and unique; no excluded word; at most three modals each; no vendor or revision number in a provision. One modal per sentence: reading only.

## Findings

### Defect
1. **OMP.19 S2** restates STND.CXX.22: the CXX term "Foreign interface" includes "a structured block of a compiler directive for parallel execution". It also contradicts the Purpose. Fix: delete it.
2. **OMP.19 S3** puts two prohibitions in one sentence, with a disguised negation (DRAFT.15), under an unrelated title. Fix: a new provision (DSGN.15), "A signal handler SHOULD NOT contain an OpenMP directive. A signal handler SHOULD NOT call an OpenMP routine."
3. **OMP.22 S3**, read literally, requires an update construct or `always` for every copy-back, including the ordinary `from` map released at region end (r3: copy back at reference-count release). Fix: "Where a result relies on data copied back from a device, the copy SHOULD be one that the reference count of that data does not suppress: the release of the last mapping of that data, an update construct, or an `always` modifier (HW.13)."
4. **OMP.23 S1** restates HW.4 and never mentions `requires`. Fix: "Each compilation unit with a target region of a component that relies on memory shared between the host and a device SHOULD declare that reliance in a `requires` directive, and the component SHOULD state it in the hardware contract of its execution path (DSGN.5, HW.4)." (r3: all units with device code declare the same requirements.)

### Should-fix
5. **OMP.14 S1**: "repeated creation" exceeds r2 ("recursive task creation"); a fixed-size task loop is routine. Limit to recursive creation. Merging applies only to a `mergeable` task; fix S2 and the Notes.
6. **OMP.1 vs Term "OpenMP specification"**: the term takes the earliest revision, so "not deprecated" is judged at the oldest revision, defeating the Notes' point. Fix: "...that no later revision marks as deprecated". SIMPL.6 is a weak citation fit (DRAFT.23).
7. **OMP.7**: `copyin` restores only the primary thread's value; use "or keep it in storage that is not threadprivate". r2 rule 8 (values not surviving a scheduling point, even in a tied task) is absent.
8. **OMP.10 S1** also covers reads by the writing thread, which r2 does not support. Restrict to reads by another thread, with the reduction and lastprivate case kept.
9. **Titles vs content (DRAFT.28)**: OMP.12 S3 (locks across contention groups) and OMP.13 S3 (detach) are outside their titles. Retitle or split.
10. **OMP.17**: not every property has a clause (maximum active levels, dynamic adjustment, wait policy). Add "through the clauses that those constructs admit".
11. **OMP.8**: a barrier is valid only if every thread reaches it (OMP.9) and not from inside a task. Drop it or add that condition. The CONC.5/CONC.12 overlap is marginal: the only OpenMP content is the names of the waits.
12. **Term "Offload policy"**: it is an environment variable and control variable, not an implementation setting, and "host alone" applies with devices present. Reword: "The setting of the OpenMP runtime that decides whether target regions run on the host: ending the run if no device is available, running on the host alone, or deciding by default."
13. **Notes overstate the research**:
    - "no compiler documents full support" and "one accepts syntax 6.0 removed": r1 says no page read claimed it, and an implementation "may" accept it.
    - "the leading cause of offload defects": r4 says wrong `map` and `nowait` were the main mapping causes in one study.
    - `default(none)` "makes each omission an error at compilation": r2 says "checkable".
    - Nested same-name critical "deadlocks": r2 says forbidden.
    - The `fork` sentence is r2 inference, unverified.
14. **Notes, narration and obligations**: paragraph one narrates drafting (custodian's directions, "the research found") and uses revision numbers outside a hazard. Indicative obligations appear: "a component states whether it builds…", "Tests of offloaded code run once under…", "a program that combines OpenMP with MPI requests…", "this standard is to cite…". Recast as hazard facts or delete.
15. **Class-onset paragraph**:
    - OMP.14 instantiates RSRC.1, which the "only DSGN, SIMPL, REPRO, VV or HW" sentence omits.
    - OMP.23 S2 cites HW.19 (CSQ3 in HW's Notes) yet sits at CSQ2, after HW.19 parts are listed as CSQ3.
    - HW.5 is CSQ3 in HW's Notes, so OMP.25 rests at CSQ2 on DSGN.5 alone; say so.
    - The "STND.OMP.2, which rests on…" sentence is unparseable; split it.
16. **Coverage**:
    - Cancellation (r2): `cancel` is a silent no-op unless enabled, a PRIME.4 silent default where a failure response relies on it, and none of CONC.1, CONC.2, CODE.7, HW.8 or HW.GPU.3 reaches it. Suggested: "Where code answers a failure by a cancel construct, the run SHOULD enable cancellation, and the tests SHOULD cover cancellation both enabled and disabled."
    - Other gaps: atomic mixed with plain access, and `critical` not excluding atomics (r2 rule 6); `declare target` globals diverging between host and device; matched release of `omp_target_alloc`; validated device numbers (r3); tests under every schedule and binding in use (r4).
    - The Purpose's "already bound" claim holds for allocation NULLs, error termination and silent host fallback (HW.8 covers detected capacity shortfalls; OMP.20 the rest). It fails for cancellation.

### Optional
- "Builds" in the OMP.4 title reads as a verb; use "Serial builds".
- Undefined terms in bodies: "device construct", "reference count", "merged".
- NUMER is in the Purpose but not in References.

## Overlaps

| Draft ID | Existing ID | Verdict |
| --- | --- | --- |
| OMP.19 S2 | STND.CXX.22 | Restatement; delete |
| OMP.23 S1 | HW.4 | Restatement; add `requires` content |
| OMP.8 | CONC.5, CONC.12 | Marginal |
| OMP.20 report clause | HW.19, HW.9 | Partial; policy and in-region check are specific |
| OMP.26 comparison | HW.16, VVUQ.1 | Partial; policy runs are specific |
| OMP.7, OMP.11, OMP.12 S3, OMP.14, OMP.15, OMP.16 S2, OMP.18, OMP.25, OMP.27 | CONC.16, CONC.4, CONC.8, CONC.14, CONC.21/22, HW.CPU.3, CONC.25 | Acceptable; each adds OpenMP content |
| OMP.17 | CONC.17 | Acceptable (per-task control variable) |

## Verdict
Not ready as drafted. Fix defects 1 to 4 and items 13 to 15 before adoption; the rest are improvements. Default status, tighten-only, owner decisions and agnosticism hold in the provisions. The "already bound" claim fails only for cancellation (item 16).
