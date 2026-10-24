# Cold verification of STND.OMP draft 0.2

**Verdict: not ready.** Blocking: D1 to D5. Mechanical checks are clean: `verify` passes; `findings.py` shows only the eight expected g.18 bundle notices; rehearsal bodies match the reading copy; a script found one modal per sentence, no banned word, and titles of six words or fewer.

## Findings to status

| Finding | Status | Reason |
| --- | --- | --- |
| Cold 1, 2, 3 | verified | OMP.21 keeps only the block exit; OMP.22 has two SHOULD NOT sentences; OMP.26 S3 matches the suggested text. |
| Cold 4 | partly | `requires` content is present and the HW.4 clause is rightly dropped. OMP.28 S2 "that requirement" now has no antecedent (D1). |
| Cold 5, 6, 8, 9, 11, 12 | verified | OMP.15, OMP.1 (SIMPL.4), OMP.10, the retitles, the OMP.8 barrier removal, and the Terms. |
| Cold 7 | partly | Provision fixed. The Notes `copyin` claim is not in r1 to r4 (D4). |
| Cold 10 | partly | Provision fixed. "No clause" for the active levels, dynamic adjustment, and wait policy is not in r1 to r4 (D4). |
| Cold 13 | verified | Each listed overstatement is corrected. |
| Cold 14 | partly | Paragraph one is recast. Narration and indicative obligations remain (S1, S2). |
| Cold 15 | partly | Fixes made, but the range "OMP.9 to OMP.14" contradicts the placement of OMP.11 S1 (D3). |
| Cold 16 | verified | OMP.16 is new and the gaps are covered (OMP.12, 24, 27, 33). OMP.16 S1 and S2 conflict (D2). |
| Cold optional | verified | Retitle, five Terms added, NUMER removed. |
| Pair: VVUQ.82 | verified | OMP.15 S2 is "within the agreement", with the citation and `refers_to`. |
| Pair obs 2 | verified | OMP.11 S1. |
| Pair obs 3 | partly | Not changed. The Notes read HW.3 as covering a mid-run change; its text does not say so. OMP.19 yields to a contract that states otherwise. |
| Pair obs 4 | partly | "Resolved by OMP.16", but OMP.21 S1 is still silent on whether a cancel construct is an allowed exit. |
| Pair obs 5, 6, 7 | verified | CXX.22 restatement deleted; the other two are deliberate no-ops. |
| Pair hand-notes (CONC.16 implicit tasks, CONC.10) | not done | Not in the dispositions. Wording notes, not defects. |

## New defects (blocking)

- **D1. OMP.28 S2.** "That requirement" has no antecedent; S1 says "that reliance" and "requires directive". "The same requires directive" is also imprecise across units. Say "a requires directive with the same clauses" and "meets the requires directive".
- **D2. OMP.16 S1 against S2.** S1 asks that each run have cancellation enabled. S2 asks for test runs with it disabled. Limit S1, for example to each run that produces a reported result.
- **D3. Class paragraph.** "Protocol rules of STND.OMP.9 to STND.OMP.14 ... CSQ3" includes OMP.11, whose S1 is placed at CSQ2 (HW.11). Say OMP.9, 10, 12, 13, 14 and the second sentence of OMP.11. The reason given for OMP.16 ("what a protocol uses") fits S1 and S3 but not S2 (VV.1, a test rule). Say why VV.1 sentences (OMP.16 S2, 31, 33) rest on no CSQ2 row, since OMP.31 compares with a reference. The claim that the paragraph places every provision is untrue for OMP.33, which falls to the default.
- **D4. Notes claims not in r1 to r4 and not marked unverified**, though the Notes promise that marking.
  - A `copyin` clause restores only the primary thread's value. r2 says "otherwise `copyin`".
  - A barrier is no remedy inside a task.
  - Active levels, dynamic adjustment, and wait policy "have no clause", and a library "sets them through routines". Wait policy has no routine as far as I know; I cannot check that against r1 to r4.
  - A false `if` still runs on the host under mandatory offload. This is an inference from two r3 rows.
  - Also: "final public draft of 6.1" (r1 corrected this to "final preview"/"Public Comment Draft"); and r1 to r4 "read ... in full text" (r4 mostly used extracts).
- **D5. RATIONALE.** It says the review found no conflict that remains and no matter without an owner. There is no recorded pair review of 0.2. The delta file lists pairs only for OMP.12, 16, 22, 27, 33 and has none for OMP.24, and `review-pairs-omp-0.2.md` does not exist. Otherwise the RATIONALE describes 0.2 accurately, with the right provision ranges and the 33 count.

## Should-fix

- **S1. Narration.** "The custodian's directions on determinism apply there" is narration. It also restates VVUQ.82, which is repeated again in the schedule paragraph. The sentence "The sources are the research notes r1 to r4 ..." is method narration.
- **S2. Obligations stated in the indicative.** "State kept for each thread is sized from the team" (OMP.20); "storage ... is released by the routine paired with it" (OMP.24); "an atomic ... carries a scope" (OMP.29); "every access ... is itself atomic" (OMP.12). "A signal handler executes only" should be "may execute only"; the specification restricts, and the indicative reads as description.
- **S3. Notes on CONC.28.** "One means for CSQ0 or CSQ1 of meeting STND.CONC.28 and STND.OMP.2" is unsupported. CONC.28 applies from CSQ0 only, and r4 ties the subset to certification, not to implemented-feature checks. Soften or cut.
- **S4. OMP.27 S1.** It allows only an update construct. OMP.26 S3 also allows `always`, and `link` variables are mapped, not updated. Add "or an always modifier".
- **S5. HW.3 reading.** Restate it as the settings in effect when the result is computed, or add that to OMP.3.

## Optional

- OMP.24 S1: a literal reading rejects the initial-device number.
- "Run-time schedule" in OMP.33 may be read as the `runtime` schedule kind. Its r4 basis is a recommendation list, not a finding.
- OMP.8 still overlaps CONC.5 and CONC.12 (GOV.31, marginal).
- Not checked: the OpenMP specification itself. I used only what r1 to r4 report.
