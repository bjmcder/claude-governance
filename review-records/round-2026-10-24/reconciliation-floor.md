# Reconciliation review B: modes, floor, and class onsets (round of 2026-10-24)

Method. I read the rehearsed copy `.scratch/amendments/round/governance` (139 entries; no script or harness file is newer than its ledger), composed reading copies in `/tmp/rvB/rd/`, scripted the mode-against-modal check (only STDC.1 is new in holding SHALL in a default, beside CXX.28, .30, .31) and the list of row-ancestors of STND.CLASS.10 per provision, and read every dispositions file. I did not re-run `verify`.

## Blocking

1. **STND.HARN.29, row Standing (binding).** One irrevocable entry voids the whole authorization (Notes: "rather than being read apart"). GUARD.11 voids only the irrevocable write. The provision therefore refers writes the owner did authorize, which its floor argument (reliance "as the record states it") does not cover, and which GOV.11 and STND.DRAFT.42 ("halt only the line of work") weigh against. Fix: test the row for each entry and honor the others (change the code and `test_irrevocable_standing`), or state this strictness as a decision for the custodian.
2. **STND.BUILD.13 s2 (R8).** It makes each checking build state "each part of the work that it links without that check". That is a stated limit of a verification (INTPR.10), which the Notes of CONC, STDC, and RUST start at CSQ2 (CONC.27, STDC.38, RUST.33), and BUILD.13 s2 is the provision that makes CONC.27 specific. BUILD puts it at CSQ3 on "rests on no row" and lists no departure. Fix: add INTPR.10 and start it at CSQ2, or list it as a departure for the custodian, as SV does.
3. **STND.WFLOW class paragraph (R8).** (a) It says provisions on INTPR.12 "rest on no row". INTPR.12 is the CSQ0 row (a recorded exercise). WFLOW.36 asks only a record, so CSQ3 holds, but the paragraph must say that. (b) WFLOW.35 s2 rests on no row yet starts at CSQ2 "as one bundle", a departure from the reading used elsewhere, unlisted. Fix: state both reasons, or list (b) as a departure.
4. **R10: provisions that block where the means is unavailable.** STND.LEAN.3 requires the next release to rest on a checker "free of that defect", so no release is possible where none exists. STND.LEAN.16 is a default that the Notes say every CSQ0 Lean project must replace until a strict independent checker exists. Fix: LEAN.3, "or the record states that none was available"; LEAN.16, "Where an independent checker is among the means of the work".

## Should-fix

1. **STND.RUST class paragraph.** It lists RUST.13 (binding) among provisions a project "replaces whole by a decision"; GOV.19 allows only tightening. The Notes also never say that the PY/JL rulings (2026-10-23) were not made for Rust. FTN and STDC say it; RUST should say the same of RUST.6, .13 s2, .15, and .34.
2. **DSGN.3 reading missing** from the class paragraphs of STDC, BUILD (BUILD.12 s1), and WFLOW. CXX, PY, JL, RUST, FTN, and LEAN state that mechanical checking of contracts at CSQ0 stays with its row. Add one sentence each.
3. **R10, unconditional demands of a tool** (defaults, so replaceable, but the pattern of SV.24 to .26 and RUST.32 is "where the means of the work include"): SV.17, FTN.36 (halting may be unsupported, FTN.16), RUST.5 s2, RUST.23, RUST.31 s1, STDC.22 s2, STDC.29 s1. The binding RUST.14, and CXX.17 as read by STDC.2, accept "the compiler or a static check", yet Static check is defined as what the means of the work make: where neither exists the SHALL cannot be met. Fix: "where the means of the work include one", with STND.CODE.7 holding the floor.
4. **Pending decisions written into Notes:** STDC ("decision 2 of the dispositions", "decision 3": a dangling reference outside the corpus), FTN, SV (three), LEAN (seven). They go stale at ratification and narrate drafting (STND.DOCS). Move them to `decisions-for-the-custodian.md`.
5. **LEAN.25 (binding)** names `Except`, `Option`, and `throw`, which the Notes say l1 "does not discuss"; the Purpose of LEAN says no provision rests on an unverified fact. Verify, or state the response by outcome ("a result type that carries the condition").
6. **SV Notes** say "this round applies" NUMER 1.3 "before STND.SV" (narration), and that VVUQ.64, .65, and NUMER.26 "are read not to govern" constrained random tests while "these Notes do not narrow NUMER.26". Both cannot stand. Keep decision 4 out of the Notes.
7. **WFLOW Terms** make "each step that runs while another has not completed" a concurrent task, and a Step includes human steps. That extends the reach of the binding CONC.1 and CONC.2 to people. Say "each step that software runs".
8. **Rationales (entries 123, 125, 128, 134, 136)** put the lead's design (which standards to cite, "evidence and not subjects", "citing HDES.11") inside "on the custodian's directions of 2026-10-24 that ...". End the attribution after "timeless" (the HANDOFF order names only the subjects). Entry 121's "as the custodian assigned" is supported by entry 112 and stands.

## Binding provisions of the round

| Provision | Instantiates | Asks more than it, at wording or one record? | Counterparts |
| --- | --- | --- | --- |
| STDC.2 | PRIME.4, .2, DSGN.2, CPS.5, .9 | Extends CXX.16 to .18 and .29 to C; adds "errno alone is no return". Decision 2. | CXX.16 to .18, .29 |
| RUST.6 | GOV.48, DSGN.1 | Yes: DSGN.1 is not floor; no argument beyond "one comment". Rulings cover CXX.3 and PY.4 only. | CXX.3, PY.4 |
| RUST.13 | PRIME.4 | s2 (hook diagnosis) has no counterpart; s3 follows PY.22 s3, while JL.15 s2 admits `Warn`/`Error` records (same principle: shown by default). | CXX.16, PY.22, JL.15 |
| RUST.14 | PRIME.4 | No. | CXX.17 |
| RUST.15 | PRIME.4, DSGN.2, CPS | Reach of Untrusted input to the public interface (ruled for PY, JL only). | CXX.18, PY.25, JL.13 |
| RUST.34 | PRIME.2 | Reaches every claim at every class; CXX.29 reaches high-assurance code only. | CXX.29 |
| FTN.29, .30 | PRIME.4 | No. | CXX.16, .17 |
| FTN.31 | PRIME.4, DSGN.2 | Same reach question; the Notes say so. | JL.13, PY.25 |
| LEAN.5 | PRIME.2 | s2 ("check of each declaration") is wording beyond "claiming a check not run". | CXX.29, RUST.34 |
| LEAN.25 | PRIME.4 | No. | CXX.16 |
| HARN.29 | GOV.48, GUARD.2, .11, .12 | Blocking 1. | HARN.22 |

Existing binding provisions are unaltered (CXX 1.1 and JL 1.1 change only defaults). BUILD, WFLOW, SV, OMP, and OFFLD hold none. No owner decision outside LVL0 (STND.DRAFT.42) is asked; LEAN.7 relies on VV.9. Unsupported ruling attributions: Should-fix 8 only.

**R16 gaps (counterparts).** LEAN has no counterpart of CXX.18, PY.25, JL.13, or RUST.15 (a check of untrusted input that a setting removes): say why (Lean's rejection of discarded results and the setting question are unverified) or add one. FTN.18 is a default where CXX.18 s2 is binding (hazard unverified for Fortran): leave, as the Notes argue. FTN has no counterpart of CXX.28 to .31 (STDC.1 gives C that reading); RUST has only RUST.34. **Recommendation:** put to the custodian whether FTN and RUST get a "reading" provision (STDC.1 form), not an addition now.

## Class onsets (R8): result

Read the same way in all documents: a part resting on a row starts at the row's class; untrusted-input entry checks of DSGN.2 at CSQ3; retained and postcondition checks at CSQ1; protocol statements (DSGN.15) at CSQ3 and their verification at CSQ2; DSGN.4, DSGN.5, INTPR.10 at CSQ2; tests without an independent oracle at CSQ3. Departures: SV.18 s1, SV.20, SV.21 (CSQ3 for INTPR.10 content; listed, decision 2), SV.18 s3; plus Blocking 2 and 3. Checked and consistent: STDC.1 rows against CXX onsets; LEAN.18 and .20 at CSQ2 (independent model) against OMP.31, STDC.26, BUILD.19 at CSQ3 (same-source references).

## Queue items for B

- **R9:** closed; no document narrows CONC's Concurrent task (SV carve-out gone), subject to Should-fix 7.
- **R10:** closed by Blocking 4 and Should-fix 3.
- **R14 (order of output):** leave FTN.26 standing (the queue says FTN.28) and record the gap for the next minor revision of CONC. Reasons: unordered output is already REPRO.3 variation; a sentence makes 1.0.1 minor, not editorial; the MPI, OpenMP, and Python cases need research.
- **R16, R22:** above. **Decision for the custodian:** extend the PRIME.4 and PRIME.2 binding forms to C, Rust, Fortran, Lean. Recommended yes for STDC.2, RUST.13 to .15, FTN.29 to .31, LEAN.5, LEAN.25 (each asks what PRIME asks); decide separately RUST.6, RUST.13 s2, RUST.34's reach, and the Untrusted-input reach for RUST and FTN. Recommended: keep RUST.6 a default, keep the others.
- **R18 (naming):** STDC Notes say names follow STND.DOCS.12, which gives no form. Recommend one rule for languages without a custodian convention, LEAN.27's form (the repository configuration names the convention; notation names may stay) in STDC, RUST, and FTN; keep the CXX, PY, and JL tables.
- **R19:** STND.VVUQ.63 names "TestU01 BigCrush" in the provision, against the agnostic direction (GOV.18 alone allows a tool at LVL2). Recommend a separate minor amendment of STND.VVUQ (entry after the round, not folded into CONC): "Each random number generator SHOULD have passed a published battery of statistical tests of randomness, named with its revision in the record of the work, applied within single streams and across interleaved streams", with BigCrush as an example in the Notes.
- **R23:** differences stand as the custodian ruled them (PY.22 s3 against JL.15 s2: the same principle; CXX.27 against JL.34 and RUST.20: different hazards). No amendment this round.
