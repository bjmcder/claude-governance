# Cold verification of STND.OMP draft 0.3

**Verdict: not ready.** Blocking: B1 to B5. All are short edits. No new conflict was found apart from B1, which is a wording gap.

Mechanical checks are clean. `verify` passes. `findings.py` shows only the nine expected g.18 bundle notices (OMP.6, 7, 12, 13, 14, 15, 16, 25, 26). The 33 rehearsed bodies, titles, and modes match the reading copy, and the non-provision paragraphs of `_doc.md` match it too. A script found one modal per sentence, no banned word, titles of six words or fewer, and an LVL0 ancestor in every provision. The `pairs` command still gives 477 pairs, and `pairs-OMP-0.3.md` is identical to the 0.2 file.

## Findings to status

| Finding | Status | Reason |
| --- | --- | --- |
| verify D1 (OMP.28) | verified | "A requires directive with the same clauses"; S2 "meets the requires directive". HW.4 is dropped from the front matter and the Notes cite it. |
| D2 (OMP.16 S1/S2) | verified | The exception is in S1. "Other than" is arguably a second condition (see should-fix). |
| D3 (class paragraph) | verified | OMP.11 S2 is listed apart. OMP.16 is split by sentence. The VV.1 tests are given a reason. OMP.33 is placed. I checked all 33 provisions and each bundle. |
| D4 (Notes claims) | partly | The `copyin`, `if`, and "final public draft" items are fixed. Other unmarked claims remain (B2, B3, S3 to S5). |
| D5 (RATIONALE) | partly | The 0.2 pair review now exists. The RATIONALE is stale (B5). |
| S1, S2, S3, S4, S5 | verified | The one new indicative obligation is the handler sentence (S2). |
| Optional items | verified | OMP.8 was deliberately kept. |
| Pair conflict OMP.12/OMP.22 | partly | S3 resolves it only on one reading (B1). |
| Pair obs 2, 3, 4, 7, 8, 10, 12, 13 | verified | |
| Pair obs 6 | partly | The null check and "after its last use" are done. "The default device is set by the environment" is unsupported (S3). |
| Pair obs 9 | partly | The provision is fixed. The Notes attribute the qualifier to r2 (S4). |
| Pair obs 5, 11, 14, 15; GOV.31 on OMP.12 S1 | verified | The reasons given hold. |

## Blocking defects

- **B1. OMP.12 S3.** "Code SHOULD NOT access a storage location that a signal handler accesses by an atomic construct." "By an atomic construct" can attach to the handler. A handler SHOULD NOT contain a directive (OMP.22), so on that reading S3 is vacuous and S1 against OMP.22 stays open for a handler that uses a language atomic. The disposition means "code SHOULD NOT use an atomic construct to access a location that a signal handler accesses". Say that.
- **B2. Notes, paragraph 2.** "Revision 6.0 removed every feature that 5.0, 5.1, and 5.2 deprecated." r1 records that 6.0 undeprecated `destroy` on `depobj`, deprecated in 5.2, and says deprecation is not one-way. Say "removed the features ... with one exception", or "nearly every". Then "a removal waiting to happen" needs softening.
- **B3. Notes, paragraph 2.** "The initial values of the internal control variables are implementation defined." r2 §5 lists seven ICVs. It also says `cancel-var` starts false, which paragraph 5 of the Notes states. Say "of several".
- **B4. Notes, last tests paragraph.** "STND.CONC.24 asks for tests at several numbers of threads, among them one." CONC.24 asks for at least three numbers, "among them the smallest that it admits". Correct it.
- **B5. RATIONALE.** It still says "declared in the same requires directive" (0.3: "a requires directive with the same clauses") and "each run-time schedule and binding in use" (0.3: schedule and binding set through internal control variables). The last sentence is cut off: "no matter that no shared-matters table gives" lacks "to an owner". The claim "no conflict that remains" holds only once B1 is fixed. I could confirm the 0.2 pair review's other 143 pair verdicts only through its record, not by rereading the pairs.

## Should-fix

- S1. OMP.12 title ("Atomic locations kept atomic") does not cover S3. The 0.1 cold review retitled for the same reason.
- S2. The Notes handler sentence ("a location that a handler accesses is left to the atomic operations of the base language") is an obligation in the indicative. It also has no OMP.12 cite. Recast it as the provision's reason.
- S3. "The default device is itself set by the environment" is not in r1 to r4 (r3 has only the ICV and the TR15 alias). Mark it unverified or cut it.
- S4. "No task keeps a threadprivate value across a task scheduling point, at which another task is able to run on its thread (r2, rule 8)". r2 has no qualifier. The qualifier is the provision's inference, so mark it so.
- S5. The `fork` sentence is attributed to "the guidance of the specification". r2 takes it from the Examples (§12.12). Elsewhere the Notes say "the Examples".
- S6. The Notes say OMP.1 judges "by every later revision". The provision adds "published or in public draft".
- S7. OMP.16 S1: "other than a test run with cancellation disabled" is an exclusion beside the "Where" condition. Under DRAFT.16 it is arguable. VVUQ.82 and CONC.15 use "other than" the same way, and g.12 passes. Alternatively, move it to S2.

## Optional

- OMP.16 S2 ("does not pass over the disabled state silently") is vaguer than the pair review's "finds the disabled state and halts or reports".
- OMP.24 S2 "after its last use" partly repeats CONC.5. The paired routine is the OpenMP content.
- The `copyin` sentence is now orphaned, since the provision no longer mentions `copyin`.
- The method sentence in the Notes is kept in short form. The STND.MPI Notes have the same convention.
- OMP.24 S1 would literally require a check on `omp_default_device`, a TR15 draft alias. It is unimplemented and not a defect.

## Class-onset paragraph

Every sentence of every provision is placed, and the placements match the CLASS.10 rows and the HW Notes. Specifically:

- The CSQ2 parts: OMP.2, OMP.11 S1, OMP.24 S2, OMP.25 and OMP.26 (bundles, all CSQ2), OMP.27 both sentences, OMP.28 both sentences, OMP.29, OMP.30, and OMP.32.
- The CSQ3 parts: the bundles OMP.6, 7, 12, 13, 14, 15, and 16 (each sentence at CSQ3).
- OMP.2 S2 is a test but cites DSGN.5, so CSQ2 is consistent.
- No floor is raised. OMP.30 at CSQ2 rests on the DSGN.5 row, though HW.5 is at CSQ3.

## Not checked

- I did not read the OpenMP specification. Claims were checked against r1 to r4 only.
- I did not reread the 477 pairs. I checked only that the list is unchanged.
- I did not recompute the 0.2 pair review's grouped verdicts for OMP.24 and the 0.1 provisions.
