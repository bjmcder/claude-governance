# Verification of STND.WFLOW draft 0.2

**Verdict: ready. No blocking item.** Four Should-fix corrections (N1 to N4) are cheap and worth making in `content_wflow.py` before the coalesce; the rehearsal has to run again if any is made.

## Scripted checks
- `govharness verify` on the rehearsed copy: 8 of 8 PASS. `findings.py 'STND\.WFLOW'`: one g.18 notice, STND.WFLOW.7 (three modals); the Notes say its sentences apply together, which meets the brief.
- All 40 provisions: default, one modal per sentence, titles at most six words, body identifiers equal `instantiates` plus `refers_to`, bodies verbatim in `draft-0.2.md`, no word of the STND.DRAFT.13 or .17 tables, no product or version in a body.
- `govharness pairs` regenerated equals `pairs-0.2.md` (481). The 0.1 to 0.2 mapping is correct. The live `apply_conc_1_0_1.py` cites STND.WFLOW.32 and `apply_build_1_0_1.py` cites STND.WFLOW.6; both match 0.2.

## Findings to status
| Finding | Status |
| --- | --- |
| Cold D1 (conditions) | Verified (10, 19, 21, 22, 3, 2). 22 reads ambiguously (N3). |
| Cold D2 (onset) | Verified: DSGN.2 ancestor of 3, 21, 22, 33; REPRO.4 of 24; paragraph rewritten. Residue N4. |
| Cold D3 (WPROC) | Verified. |
| S4 (BUILD boundary) | Verified in Purpose and Notes; consistent with BUILD draft 0.2 (N5). |
| S5, S7, S10, S11, S12 | Verified. |
| S6 (Step) | Verified; the Purpose list for manual steps is incomplete (N7). |
| S8 (37.1) | Partly: additions only, but the sentence calls them items REPRO asks (N2). |
| S9 (QA.14) | Verified as argued; decision 3. |
| Optionals; cuts of 31, 39, 8, 40 | Verified. The monotonic-clock rule now lives in the Notes only (review had suggested a STND.CONC amendment); lead's choice. |
| Pairs 1 to 18, 20, 22, 23, 24 | Verified. |
| Pairs 19, 25, 26 | Declined or inherent; reasons hold. |
| Pair 21 (Terms) | Partly: Concurrent task and Asynchronous operation appear in Terms and Notes, in no provision. Optional. |

## New findings, ranked
No Defect.

**Should-fix**
- N1. Notes, partial outputs: "two attempts of one step ... two writers unless STND.WFLOW.7 publishes only one of them (STND.WFLOW.9)". Atomic rename does not make one attempt publish, and WFLOW.9 concerns distinct steps. Fix: cite STND.WFLOW.5 and STND.WFLOW.36 (jobs not known to have ended); drop the claim about WFLOW.7.
- N2. STND.WFLOW.35 sentence 1: "Among the items that REPRO.1 and REPRO.4 ask ..., that provenance SHOULD give the reuse key ... resource request". Fix: "Beyond the items that REPRO.1 and REPRO.4 ask ..., that provenance SHOULD also give ...".
- N3. STND.WFLOW.22: "Before each process ... has written and checked" reads as "any one". Fix: "every process".
- N4. The onset paragraph puts WFLOW.35 on REPRO.4 at CSQ2 and every other sentence at CSQ3. Sentence 2 of 35 rests on REPRO.12 and INTPR.9 and is at CSQ2 only through the bundle the Notes state. This narrows (no floor raised), but the paragraph contradicts itself. Name that sentence as bundled.

**Optional**
- N5. The BUILD boundary is informative only; a compile step still meets WFLOW.1, .6, .35 and BUILD.1, .23, .25 in the bodies. Same direction, no conflict.
- N6. WFLOW.11 sentence 2 "rests on DSGN.5" (a contract row) but states a backoff rule; if the row does not hold, CSQ3. Add to the custodian's list or move.
- N7. Purpose names 1, 3, 36 for manual steps; 3 asks an exit status that a manual step lacks.
- N8. WFLOW.4: "by not running again an attempt" should read "by not running the step again after an attempt that made the effect".
- N9. WFLOW.7 sentence 2 ends "write after it a marker", a second condition after its clause (STND.DRAFT.16). Fix: "or mark it complete with a marker that the step writes last".

## Tighten-only, floor, conflicts
No changed sentence raises a floor, restates an owner, or requires a decision of the human owner; onsets only narrow. No conflict with STND.CONC.1 to .29, STND.DFLT (Checkpoint avoided; Attempt distinguished), REPRO, INTPR, STND.VVUQ.82 and .83 (38 and 40 state the agreement; none asks identity), PRIME.13 (safe point set apart), or BUILD draft 0.2. Sentences that refuse without a possible check (25 sentence 2, 27) are defaults.

## New pairs (44 of 481, by mapping)
13 with 18 provisions (INTPR.9: HW.9, HW.EMBED.6, HW.QPU.4 and .6, MEAS.6, ML.5, NUMER.8 to .10, .13 to .15, .18, .20 to .23, .29); 17 with AGENT.39, HDES.11, HW.11 (DSGN.15); 3, 21, 22 each with CPS.5, CPS.9, ML.6 (DSGN.2); 24 with CPS.7, MEAS.3 (REPRO.4); 38 and 40 each with AGENT.5, HDES.4, HW.18, MEAS.7, NUMER.3, NUMER.26 (VV.3). None conflicts; none is unowned.

## Class-onset paragraph and the three decisions
Every sentence is correct except as N4 and N6 note. Decision 1 follows the DSGN.2 row (recommend yes). Decision 2 (25, 27 at CSQ3) is a sound reading, since DSGN.2 sentence 1 has no row; 27 (digest, controlled storage) goes beyond "untrusted data" as a default. Decision 3 (2 sentence 2, 6 sentence 1 at CSQ3, not the QA.14 row) tightens the row, because rerunning dependents needs them known; the Notes' reason ("the engine of every class does") is unsupported.

## Not checked
Primary sources behind w1 and c3; the final BUILD text; a rehearsal with the live `apply_conc_1_0_1.py` (the rehearsal used a scratch variant that differs in two OpenMP lines).
