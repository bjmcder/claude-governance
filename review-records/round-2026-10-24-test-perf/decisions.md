# Decisions for the custodian at ratification: STND.PERF and STND.TEST

The round applies six transactions in this order:

1. the MNEM row PERF, then STND.PERF 1.0 (26 defaults);
2. the MNEM row TEST, then STND.TEST 1.0 (19 defaults);
3. STND.WPROC 1.1, a minor amendment of STND.WPROC.9;
4. STND.CREW 1.1, a minor amendment of STND.CREW.9 and STND.CREW.15.

Each draft went through a cold review, a STND.HARN.28 pair review, and verifications until none had a defect. The records are in `perf/` and `test/` of this folder: drafts, reviews, verifications, dispositions, and pair lists. Each decision below carries a recommendation, and ratifying "with the recommendations" adopts every one.

## STND.PERF

1. **Mnemonic PERF.** It is the established short form of performance, at a letter distance of 3 or more from every STND mnemonic. The alternative is PEVAL. Recommend PERF.
2. **MEAS is left out.** The timing of code is not "measured data" under MEAS, and MEAS is not cited by analogy. STND.PERF.18 gives the outcomes of MEAS.3 and MEAS.7 for performance samples. Recommend yes: reading every timer as an instrument would bring calibration and uncertainty duties to every evaluation.
3. **STND.VVUQ's stochastic-sample provisions and NUMER.25 and .26 serve as models only.** Their numbers were fixed for accepting correctness. STND.PERF.19 to .21 state outcomes instead. Recommend yes.
4. **STND.PERF.7 asks for at least three values of the scaled variable**, with a way out where the variable admits fewer. The number rests on the analogy of STND.CONC.24 and is marked unverified. The alternative is the form with no number: "enough values to distinguish the rates of growth in question". Recommend three.
5. **The reading of STND.PERF.3.** An evaluation considers the absolute, relative, and scaling questions, and gives its reason for leaving one out. It does not have to answer all three. Recommend yes: a question that has no meaning for the work would otherwise block it.
6. **The regression guard on time stays in STND.PERF**, and STND.PERF.24 differs on purpose from STND.VVUQ.17. A failed guard may be resolved by a recorded decision with evidence that the requirements are still met, because timing noise differs from a changed numerical result. Recommend yes.
7. **A later minor amendment of STND.OFFLD** so that STND.OFFLD.31 cites STND.PERF.12 and .14, which generalize it. Recommend it for a later round (open item).

## STND.TEST

8. **Mnemonic TEST.** It reads as the standard's subject, as BUILD does, and is at a letter distance of 2 from RUST and THRT, which STND.IDENT.18 allows. The alternative is SUITE. Recommend TEST.
9. **The full-suite run, under the ruling of 2026-10-25.** A full-suite run executes every test, skipped, disabled, and quarantined tests included, and no reused verdict stands for it. It runs before each main-line advance, completing before the release record is presented under STND.WPROC.13, and on the development line at the project's stated cadence. Below the development line, selections widen with integration depth. Recommend as drafted.
10. **Ratify STND.WPROC 1.1 and STND.CREW 1.1 with STND.TEST.**
    - Without the STND.WPROC.9 amendment, a merge that defers a slower tier under STND.TEST.5 departs from STND.WPROC.9 and loses the agent's authority to merge under STND.WPROC.11.
    - STND.CREW.9 has the author's self-review run the selected tests, and STND.CREW.15 gives the review agent the run records.
    - Recommend both.
11. **The rows of STND.TEST.4 are held within the tiers drawn at each depth.** What they reach outside those tiers is recorded as an omission, and runs at the latest at the merge into the development line. New, changed, last-failed, and underived tests are held from every tier. The cold reviewer preferred holding every row regardless of tier. Recommend as drafted, since the merge into the development line catches every omission.
12. **The onset of STND.TEST.2.** A statement in the repository configuration of what a test reads is no dependency-tracking mechanism, so it applies from CSQ3. A tool that tracks dependencies falls under the QA.14 row from CSQ2. Recommend yes.
13. **No threshold on coverage (STND.TEST.17).** Thresholds on mutation scores are left to each project. Recommend yes.

## Also pending, from the harness units

14. **STND.HARN.30, unsigned reliance.** Unit 0010 proposes it so that the refusal of an unsigned authorization is in the corpus, not only in this harness. The question of how STND.DRAFT.42 reads on an owner's acceptance at derivation goes with it. The proposal is in `harness/records/units/0010-unsigned-authorizations.md` and has not been drafted as a transaction. Recommend drafting it in the next round, through the standing process.
