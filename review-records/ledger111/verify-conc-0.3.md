# Verification of STND.CONC 0.3 (change from 0.2 only)

## Findings

Defect: none. Mechanical checks over all 29 provision files of the rehearsed corpus found: one modal per sentence; at most three per provision (three in 3, 5, 8, 13, 24); no banned words in bodies; titles of six words or fewer, none verb-initial, none duplicated in the corpus; body IDs equal instantiates plus refers_to; Notes hold no modal. Every body in the corpus is present verbatim in conc-0.3-draft.md. Conditions precede clauses in 8, 11, 12, 19, 25, 29. `verify` was not re-run (read-only); the brief says it passes.

Should-fix (apply_conc.py RATIONALE, mismatches with 0.3; none is a wrong claim about a provision, mostly silent omissions):
1. Line 48: "Review of STND.HARN.28 ..." names a standard that is not CONC. Fix: STND.CONC.
2. CONC.19: rationale says children are started "by a facility that starts a new program"; the body also admits a facility the runtime documentation states as safe. Add it.
3. CONC.17: rationale says pools "taken from the caller"; the body also admits stating pools and sizing settings in the contract.
4. CONC.14: second sentence (tasks that wait on one another not in one bounded pool) is absent.
5. CONC.15: second sentence (reach a loop's objects only through the loop library's facility) is absent.
6. CONC.12: early-end sentence (parent cancels and waits) is absent.
7. CONC.13: rationale gives only sentence 1; sentences 2 and 3 (release resources and pass on; observe cancellation at stated points) are absent.
8. CONC.7 (reentrant lock sentence), CONC.9 (notification sentence), CONC.22 (identical-bits comparison sentence and order-independent alternative), CONC.24 (uneven division; tolerance tier), CONC.16 (thread identity sentence) are absent.
Fix: add each clause, or state that the rationale lists headline obligations only.

Optional:
- Class paragraph justifies only the third sentence of CONC.3 as not a DSGN.15 verification part. Sentences 1 and 2 of CONC.3, sentence 1 of CONC.5, and all of CONC.8 carry DSGN.15 on the same reasoning. The blanket "protections, orderings, and lock rules of 3 to 9, from CSQ3" covers them, so no defect; consider one clause.
- Rationale does not mention that CONC.29 applies from CSQ1 (not required).

Class paragraph for the seven named provisions (checked against STND.CLASS.10): 3 from CSQ3 (bundle, no row); 10 sentence 2 from CSQ1 (INTPR.7), sentence 1 CSQ3; 11 from CSQ3 (DSGN.1/DSGN.15, completion not invariants); 12 from CSQ3 (DSGN.14); 19 from CSQ2 (DSGN.5 only, row "contract for each external component"); 25 from CSQ2 (DSGN.15 only, row "verification of invariants"); 29 from CSQ1 (INTPR.8, row "diagnostics captured by default"). All correct. Three-modal provisions 3, 5, 8, 13, 24 each fall to one onset (CSQ3).

## Dispositions checked

| Item | Result | Evidence |
| --- | --- | --- |
| S1 CONC.29, CONC.12 back to two sentences | Resolved | 29.md instantiates INTPR.8, section Records; 12.md two sentences; Purpose lists 29; class paragraph CSQ1; Notes cite 29 |
| S2 delete CONC.11 sentence 2 | Resolved | 11.md has two sentences; Notes sentence on CONC.25 added |
| S3 CONC.8 condition wait | Resolved | 8.md "or for a condition through a facility that releases that lock"; bundle sentence in class paragraph |
| S4 CONC.19 | Resolved | paragraph: "CONC.19, which instantiates only DSGN.5, from CSQ2" |
| S5 CONC.3 sentence 3 | Resolved | paragraph clause present, CSQ3 |
| S6 PRIME.4 reading | Resolved | Notes on CONC.1/2 hold both statements |
| S7 c3, unverified | Resolved | c3 listed; "(unverified)" added |
| Optional DSGN.3 | Resolved | 25.md instantiates DSGN.15 only |
| Optional figures | Resolved | "22 percent"; "92 percent of the 105 defects" |
| Optional header | Resolved | content_conc.py docstring says draft 0.3 |
| Stacked clauses | Not changed, as dispositioned | 2.md unchanged |
| Rationale 1 to 6 | Resolved in part | rewritten and accurate on every claim, but omissions above |
| 7 and pair #79 | Deferred to ratification | not checked |

## Verdict

Ready to present for ratification, no defect. Apply the should-fix edits to the RATIONALE in apply_conc.py (item 1 at least) before application.
