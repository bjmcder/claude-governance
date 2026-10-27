# Cold and pair review: round of 2026-10-27 on offloaded work

## What I ran
Read CUSTODIAN.md, decisions.md, and the script. Ran `rehearse` (entries 198 and 199; all checks pass, with the g.18 warning the corpus already carries). Applied the script to a copy in /tmp/claude-1000/review-offld-2026-10-27/ and ran `verify`, `show` (OFFLD.26 to .31, PERF.12, PERF.14, HW.22, HW.CPU.4, HW.GPU.4, HW.QPU.8, NUMER.17), `pairs STND.OFFLD` (pairs 495 to 499 are the five named), `findings.py`, and a recursive diff of the copy against the corpus. Only STND/OFFLD/31.md, the two _doc.md files, manifests, and the ledger change.

## Checks that pass
- STND.DRAFT: OFFLD.31 has one SHOULD per sentence, no banned word; body IDs equal `instantiates` plus `refers_to`.
- Notes: no indicative obligation, no narration, American English.
- Class: minor and editorial fit STND.IDENT.3. Onset: OFFLD.31 rests on no row and applies from CSQ3, as PERF.12 and PERF.14 do; no floor is raised.
- Pairs: no conflict. HW.22 counts data movement whatever first use is stated; HW.GPU.4 records data moved on demand (complementary); HW.CPU.4, HW.QPU.8, and NUMER.17 share only the RSRC.4 base. No other adopted document addresses costs of first use of offloaded work.
- Citations: both References tables are right.

## Findings

### Defect
None.

### Should-fix
1. **The rationale writes a ruling the custodian has not made.** Text: "ratified by the custodian on 2026-10-27" and "Transition (GOV.42): a measurement recorded before this amendment needs no new statement." decisions.md records that the custodian directed the item to go ahead, not that the draft or a transition was ruled. The transition is not in "Drafted, for ratification". Replacement: add to decisions.md item 1 the sentence "Transition (GOV.42): a measurement recorded before this amendment needs no new statement, for ratification." The ratification wording is the standard template and is true once the custodian ratifies and the script is applied.
2. **The Notes sentence on migration no longer reads alone.** Text: "the first access to memory that migrates on demand is likely to pay for migration as well, which o3 did not retrieve and is unverified". It is still true and still marked unverified. But OFFLD.31 now names "the first filling of caches and memory", and a reader cannot tell whether that migration is such a filling. Replacement, appended after "is unverified": "; if it is a first filling of memory, the second sentence of STND.OFFLD.31 names it". That adds no obligation and keeps the unverified mark on the fact.

### Optional
3. Notes, new sentence: "The two name the same costs of first use: initialization, compilation at load, and the first filling of caches and memory, so one record of offloaded work that states them meets both." The colon before "so" reads heavily. Replacement: "The two name the same costs of first use, which are initialization, compilation at load, and the first filling of caches and memory, so one record of offloaded work that states them meets both."

## Answers to check 1
- Reach: "costs of first use" in place of "costs of a first submission" widens the reach. "Submission" is a defined Term (one request); "first use" is undefined and can cover the first use of a context, a module, a kernel, or a buffer, not only the first request. Decision 27 names only caches and memory. The widening is sound: PERF.12 uses the same words for every other measurement, the Notes say the two name the same costs, and the rationale states the widening ("not of the first submission alone"). The ratification record should state it as well (see the question).
- Decidability: the obligation is to state whether a measurement includes the cost, so it is decidable by reading the record. Whether a run in fact includes the first filling of hardware caches is often not observable to the program. PERF.12 has the same limit; the Notes need no change for it.
- Migration Notes: they read truly (see finding 2).

## Question for the custodian
Does the custodian accept that "costs of first use" reaches beyond the first submission (the first use of a context, module, or buffer), as PERF.12 already does, and is that to be said in decisions.md before ratification?
