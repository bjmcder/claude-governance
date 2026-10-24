# Cold verification: STND.CONC 0.2

Checked by script on the 28 rehearsal files: one modal per sentence, at most three per provision, no excluded words ("such as", "can", "will", "must", "any", "significant", "need not", "is to"), one condition per sentence (STND.DRAFT.16), titles (six words or fewer, not verb-initial, distinct corpus-wide), body IDs equal `instantiates` plus `refers_to`, no modals in `_doc.md`. All pass. Ledger entry 112 matches the rehearsal ledger. Not checked: that `verify` passes, the pair listing beyond the 354 count, and the c4 facts beyond hazard 6.

## Findings

### Defect

None.

### Should-fix

1. **STND.CONC.12, third sentence (STND.DRAFT.28, DRAFT.23).** Disposition D1 says the sentence rests on DSGN.14 "to keep one bundle with one onset". The content is a record of pending operations, which is INTPR.8 (diagnostics captured by default; CSQ1 row of CLASS.10), not DSGN.14. It is also applied apart from sentences 1 and 2: it matters when a task is detached. The title no longer covers it. Fix: remove it from CONC.12 and adopt it as STND.CONC.29, "Pending operations recorded", instantiating INTPR.8: "Where a run ends while an asynchronous operation that it started has not completed, the record of the run SHOULD state that operation (INTPR.8)." Update Purpose, the class paragraph (CSQ1), the rationale, and the pair list. If the count must stay 28, delete the sentence and the Notes line that cites it.
2. **STND.CONC.11, second and third sentences.** Sentence 2 requires, from CSQ3, tests under "the detection of deadlock of STND.CONC.25", but CONC.25 applies from CSQ2 and only where the means detect deadlock. Sentence 3 is separable from 1 and 2. Fix sentence 2: "Where the means of the work detect a deadlock at run time, each test that runs a protocol whose statement carries no such argument SHOULD run under that detection (DSGN.15)." Keep the `refers_to` entry for CONC.25 only if the text still names it. The class paragraph should say why a CSQ3 default uses a CSQ2 check.
3. **STND.CONC.8, first sentence.** "While it holds a lock, code SHOULD ... wait only to acquire another lock" bars the routine condition wait that CONC.9 requires, because the mutex is held when the wait begins. Fix: "...and wait only to acquire another lock in the stated order, or on a condition through a facility that releases that lock for the wait (DSGN.15)." The provision is now a three-sentence bundle of separable rules; STND.CONC.3, CONC.8, and CONC.12 should each state in the class paragraph that their sentences share one onset.
4. **Class paragraph, STND.CONC.19.** It says "the reliance on the documentation of runtimes" applies from CSQ2, as if the rest applied from CSQ3. The provision is one sentence and instantiates only DSGN.5. Fix: "STND.CONC.19, which instantiates only DSGN.5, applies from CSQ2."
5. **Class paragraph, STND.CONC.3.** Its third sentence cites HW.11, which is verification (CSQ2 through DSGN.15). Add: "The third sentence of STND.CONC.3 states what the stated protection uses, not the verification of its invariants, and applies from CSQ3."
6. **Notes, STND.CONC.2 first sentence (PRIME.15).** PRIME.4 does not name the parent. The text "reach the parent" is within PRIME.4 only on the reading that a parent relying on a failed result without learning of the failure continues silently past an error. Add that sentence to the Notes. Sentence 2 rests on HW.8 as the HW Notes (1.1.1) and STND.MPI.6 read it. STND.CONC.1 stays within PRIME.4: PRIME.4 still governs unobserved operations, which the Notes should say once.
7. **Notes, sources.** "(c1, item 8; c3, section 6)" cites c3, which the first Notes paragraph does not list. Add c3 to the list. "the same holds of a detached thread whose failure ends only that thread" has no source in the notes; add "(unverified)".

### Optional

8. STND.CONC.25 cites DSGN.3 (contracts, schemas, units), which fits race detection poorly; drop it or say why it fits.
9. Notes: "a fifth" is 22 percent; "most under an order among at most four accesses" is 92 percent of 105 non-deadlock bugs (c2, S32). State the figures. Two uses of "rather than" (STND.DRAFT patterns, negative parallelism) carry real contrasts and can stay.
10. STND.CONC.2 first sentence has two stacked relative clauses; "each failure that the task detects, of a kind that PRIME.4 lists," reads better.
11. `content_conc.py` line 1 still says "draft 0.1".

## Prior findings

| Finding | Status | Evidence |
| --- | --- | --- |
| D1 CONC.1 raises CSQ4 floor | Resolved | CONC.1 has one sentence. The pending-operation record is a CSQ3 default in CONC.12 (see should-fix 1 for its citation). |
| D2 CONC.2 narrows PRIME.4 | Resolved | Condition "relies on a result"; the sentence demands no end of the run; handlers with no relying parent are outside it. |
| D3 obligation in Notes | Resolved | "Such a profile is one means of meeting ..." |
| S4 sourcing and DOCS.9 | Partly | POSIX marked unverified, Pathfinder named (c2 S30), qualifier claim marked, c4 attribution fixed. Residuals: should-fix 7. |
| S5 narration, stale text | Resolved | No ratification text; "planned" matches HANDOFF order. |
| S6 CONC.10 broad | Resolved | Limited to waits on tasks or their conditions. A join of a worker still falls in; acceptable for a default. |
| S7 CONC.25 no detector | Resolved | Opens with "Where the means of the work include a check". |
| S8 CONC.8 ambiguity | Partly | Split done; new friction (should-fix 3). |
| S9 c4 hazard 6 | Resolved | CONC.11 sentence 3 plus Note; bundle point in should-fix 2. |
| S10 class paragraph | Partly | CONC.11 moved to CSQ3; CONC.18, 20, 21 explained; items 2, 4, 5 remain. |
| O11 title | Resolved | "Worst-case blocking time". |
| O12 CONC.4 second sentence | Resolved | Moved to CONC.3. |
| Overlaps table | Resolved | Notes name CXX.23, JL.27, PY.17, JL.24, MPI forms; each adds model-neutral content. |
| Pair #48 | Resolved | Same as D2. |
| Pair #339 | Resolved | CONC.3 sentence 3 admits the hardware ordering model (HW.11) and excepts confinement and immutability; consistent with CXX.23. |
| Pair #79 | Not | Put to the custodian: NUMER as owner, row at NUMER's next revision. No text, Note, or rationale records a ruling. |
| Pair optionals 1 to 3 | Resolved | CONC.14 wording; Notes on CONC.21 and CONC.28. Optional 4: no change, as stated. |

## Adoption rationale (apply_conc.py) against 0.2

1. Says operations left pending are reported, "binding (STND.CONC.1, PRIME.4)". In 0.2 CONC.1 holds only observation; the record is a CSQ3 default in CONC.12 (or CONC.29).
2. Says a failure reaches "its parent or ending the run". 0.2: failure reaches the parent where the parent relies on the result; the end-the-run option is gone.
3. CONC.1/2 cost sentence lists "one report of operations left pending"; remove it.
4. CONC.3 summary omits the facility rule (memory or hardware ordering model) that was moved there from CONC.4.
5. CONC.11 summary omits the rule against waiting on a task of a construct without a concurrency guarantee. CONC.12 summary omits the pending-operation record. CONC.14 omits "loses no work silently".
6. "run-time detection of data races and deadlocks" omits the condition "where the means of the work include" one.
7. Nothing records the #79 decision.

## Verdict

Not yet ready. There is no defect, and the binding provisions pass on the reading in should-fix 6. Items 1 to 5 change provision text or the class paragraph, and the rationale needs the seven edits above. After them, present for ratification with #79 as an explicit open decision for the custodian.
