# Dispositions: STND.CONC 0.1 to 0.2

Reviews of draft 0.1: review-cold-conc.md (cold review) and review-pairs-conc.md (STND.HARN.28 pair review). The reading copy of 0.1 is labeled revision 1.0 because it is composed as it would be adopted; the drafts are 0.1 and 0.2.

## Cold review

| Finding | Disposition |
| --- | --- |
| D1: the second sentence of STND.CONC.1 (report of operations pending at the end of a run) raises the floor at CSQ4 | Accepted. Moved to STND.CONC.12 as a default on DSGN.14: the record of the run states each operation left pending. Resting it on DSGN.14 keeps the three sentences of STND.CONC.12 one bundle with one onset (CSQ3). STND.CONC.1 keeps only the observation of completion before reliance. |
| D2: the first sentence of STND.CONC.2 narrows PRIME.4 (only "reach the parent" or "end the run"); a handler has no parent | Accepted: "Where the parent of a concurrent task relies on a result of that task, each failure of a kind that PRIME.4 lists that the task detects SHALL reach the parent." The task's own response stays every one that PRIME.4 admits; a handler whose result no parent relies on is outside it. |
| D3: an obligation in the Notes (high-assurance profile) | Accepted: "Such a profile is one means of meeting STND.CONC.7, STND.CONC.20, and STND.CONC.28." |
| S4: sourcing and STND.DOCS.9 patterns in the Notes | Accepted: POSIX named with "unverified"; Mars Pathfinder named; the qualifier claim marked unverified; the captured-data hazard attributed to c4 as found; the unbounded-queue claim tied to c2's backpressure sources. |
| S5: drafting narration, stale ratification text, standards not yet adopted | Accepted: first Notes sentence states the scope; "put to the custodian at ratification" removed; the Purpose says "planned". |
| S6: STND.CONC.10 too broad | Accepted: limited to waits for another concurrent task or a condition that one makes true; the Notes say a blocking read of a file or a device is outside it. |
| S7: STND.CONC.25 without an escape where no detector exists | Accepted: "Where the means of the work include a check that detects data races at run time, ...". |
| S8: STND.CONC.8 ambiguous | Accepted: split; "While it holds a lock, code SHOULD NOT reach a suspension point." |
| S9: hazard 6 of c4 (no forward progress between tasks of one construct) missing | Accepted: third sentence of STND.CONC.11, with a Note. |
| S10: class paragraph | Accepted: STND.CONC.11 applies from CSQ3 (its argument concerns completion, not the invariants of DSGN.15); STND.CONC.18, STND.CONC.20, and STND.CONC.21 take their onset from DSGN.14, RSRC.1, and REPRO.3; STND.CONC.12 applies from CSQ3 as one bundle. |
| O11: STND.CONC.20 title gerund-initial | Accepted: "Worst-case blocking time". |
| O12: the second sentence of STND.CONC.4 is not about atomic ordering | Accepted: moved to STND.CONC.3. |
| Overlaps table | Each overlap that the review marks as a restatement in part (STND.CONC.3 with DSGN.15; the protection rule with STND.CXX.23; STND.CONC.16 with STND.JL.27; STND.CONC.23 with STND.PY.17 and STND.JL.24) is the model-neutral form of which the language provision is the language form, as the Notes state; none restates a higher provision without content of its own. |

## Pair review

| Finding | Disposition |
| --- | --- |
| #48: STND.CONC.2 against HW.8 | Resolved by D2. |
| #339: the protection rule against HW.11 (and STND.CXX.23) | Accepted: "Where the protection of a shared mutable object orders accesses by synchronization, that synchronization SHOULD be a facility that the memory model of its language or library, or the ordering model that the hardware contract of its execution path states, defines as ordering accesses between concurrent tasks (DSGN.15, HW.11)." Confinement and immutability need no facility. |
| #79: the keying and construction of random streams for divided computation is in no shared-matters table; proposed owner NUMER | Put to the custodian: record NUMER as the owner and add the row to the shared-matters table of NUMER.2 at NUMER's next revision. |
| Optional 1: the behavior of a full queue or pool to be visible | Accepted: "a stated behavior that loses no work silently". |
| Optional 2: STND.CONC.21 covers runs that differ in task counts | Already stated in the Notes. |
| Optional 3: the model of STND.CONC.28 uses the ordering model of HW.11 | Accepted as a Note. |
| Optional 4: locks, waits, lifecycle, and pools have no profile provision | No change; noted for a later profile, if one is drafted. |

## Cold verification of 0.2 (verify-conc.md), giving 0.3

| Finding | Disposition |
| --- | --- |
| S1: the third sentence of STND.CONC.12 rests on DSGN.14 only to keep one onset; its content is INTPR.8 | Accepted: new STND.CONC.29 "Pending operations recorded", in a new section Records, instantiating INTPR.8 and applying from CSQ1. STND.CONC.12 is back to its two sentences. Purpose, class paragraph, and rationale updated. |
| S2: the second sentence of STND.CONC.11 requires a deadlock check from CSQ3 that STND.CONC.25 asks only where the means exist, from CSQ2 | Accepted by removal: STND.CONC.25 already runs the tests of all concurrent code under deadlock detection wherever the means exist, so the sentence added nothing; the Notes say that detection is the evidence left where no argument is stated. |
| S3: "wait only to acquire another lock" in STND.CONC.8 bars the condition wait of STND.CONC.9 | Accepted: "... or for a condition through a facility that releases that lock for the wait". The class paragraph states that the sentences of each three-modal provision share one onset. |
| S4: the class paragraph on STND.CONC.19 | Accepted: "STND.CONC.19, which instantiates only DSGN.5, from CSQ2". |
| S5: the class paragraph on the third sentence of STND.CONC.3 | Accepted: it states what a protection uses, not how its invariants are verified, and applies from CSQ3. |
| S6: the reading of PRIME.4 under the first sentence of STND.CONC.2; PRIME.4 still governs operations that STND.CONC.1 does not reach | Accepted: both stated in the Notes. |
| S7: c3 cited but not listed; the detached-thread claim unsourced | Accepted: c3 listed among the sources; the claim marked unverified. |
| Optional: STND.CONC.25 cites DSGN.3 | Accepted: it instantiates DSGN.15 only. |
| Optional: figures | Accepted: "22 percent"; "92 percent of the 105 defects studied". |
| Optional: stacked clauses in STND.CONC.2 | No change; the sentence passes the drafting checks. |
| Optional: module header | Accepted. |
| Rationale mismatches 1 to 6 | Accepted: the rationale is rewritten for 0.3, provision by provision. |
| 7 and pair #79 | Put to the custodian at ratification. |
