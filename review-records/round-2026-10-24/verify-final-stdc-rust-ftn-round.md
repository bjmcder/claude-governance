# Final verification: STDC, RUST, FTN, the amendment texts, and the round

Cold verifier, 2026-10-24. Rehearsal copy: /tmp/rehearsal-eenkewe8/governance. Scratch: /tmp/claude-1000/verify-final-c/. No file other than this report was written.

## Part 2 results (the whole round)

| Check | Result |
| --- | --- |
| `rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24.py` | 25 entries, seq 117 to 141, times 22:00 to 22:24, monotonic; source unchanged |
| `verify` on the copy | all eight checks PASS; one warning, the g.18 that the live corpus carries; rc 0 |
| `findings.py` (the 17-pattern filter) | 142 findings, all class review, none defect. Outside VVUQ: 50 g.18, one g.11 (CXX.3), one g.6 (HARN.28), as before the passes. RUST g.18: .1 .7 .11 .13 .22 .24 .25 .30, each argued in the class paragraph |
| `check_refs.py` | 16 round documents: 0 with missing rows. Run on all 69 documents: 22 gaps, all old text (STND.IDENT, STND.KNOW, STND.MPI, and others) |
| Harness suite | 189 tests, OK (251 s) |
| Rationales, by script on the ledger of the copy | all 25 end with the fixed tail; entries cited are 15, 53, 112, 114, 116 only; no number from 117 to 141 appears; no corpus file cites entries 117 to 141 |
| MNEM rows | OFFLD, then BUILD (entry 123), WFLOW (125), STDC (129), RUST (131), FTN (133), SV (135), LEAN (137): ledger order |
| Bodies of STDC, RUST, FTN, HARN.29, by script | no banned word, one modal per sentence, at most three per provision, titles six words or fewer, no title repeated in the corpus; `verify` ids and logic PASS |
| Reading copies | every provision and every Notes paragraph of the three `-final.md` files equals the rehearsed corpus |

`check_refs.py` does what it claims for a bare identifier outside quotes, code, and the history table. It cannot see a document named by description (the CXX 1.1 phrase "the standard for building software" is the case it missed, and a person found it). It skips quoted spans. Run without arguments it reports old gaps, so only the 16-document run is a test of the round.

## Defect (broken rule)

**D1. STND.RUST.13 sentence 2 (binding) rests on a fact that rs1 does not support and the Notes do not mark.** The Notes (Failures) say that "a program with the standard library is able to replace the hook that runs at a panic, and a program without it defines the handler". rs1 has neither "hook" nor a panic-handler fact; it holds only a row with "a handler turns it into a diagnosis [inference]" (rs1 line 153). The sentence has no citation and no unverified mark, and the provision is binding. The test is a Notes fact that rests on its note or is marked unverified, and no provision rests on an unverified fact. Fix: either have a research agent confirm both facts and add the source, or mark both `(unverified)` and make sentence 2 a default. Nothing else of RUST.13 depends on it.

## Should-fix

**S1. RUST rationale and Notes do not hand the floor questions to the custodian.** The rationale says "so none raises the floor (GOV.11)". The Floor paragraph argues RUST.6 only as "costs an agent one comment". It does not say what GOV.48 or another floor provision already requires that the argument covers. The PY.4 ruling of 2026-10-23 was made for PY, and the Notes say so only for the reach of Untrusted input (RUST.15). Reconciliation B says the same of RUST.6, RUST.13 sentence 2, and RUST.34. The STDC, FTN, and HARN rationales do say "the custodian decides on ratification". Fix: add that clause to the RUST rationale for RUST.6, RUST.13 sentence 2, RUST.15 (reach), and RUST.34 (reach). Add one sentence to the Floor paragraph that no ruling covers RUST.6.

**S2. CXX 1.1.1 (editorial) states a reading of STND.CXX.27 that the Notes of STND.BUILD do not share.** The new sentence says the words of CXX.27 reach "a build from which the work reports only the verdict of a test". The BUILD Notes say "STND.CXX.27 keeps the library's production checks in reporting builds; a verdict of a test that a checking build runs ... the term Reporting build leaves it out". fixpass-2 says the two agree. They differ on the test-verdict build. The sentence also states which builds an obligation reaches, and a reader may take it as a change of scope, which is minor, not editorial. Fix: drop the clause after the semicolon and say only that each reporting build is a build CXX.27 reaches. Or make BUILD's Notes say that CXX.27 reaches test-verdict builds too, and record the doubt about the class.

**S3. STND.STDC.28 rests on facts the Notes call unverified.** These are that a failed write sets the error indicator, and that a flush or close reports the failure of buffered data. The Notes keep it a default because "no binding provision rests on an unverified fact". The test says no provision. Fix: confirm both from the ISO text with a short research note and drop the mark, or add the condition "where the documentation of the library states that" to the second sentence.

## Optional

1. RUST Notes (Concurrency): "which meets STND.CONC.3,. Send and Sync". Stray ",." (present since commit 677c691). Fix: "STND.CONC.3."
2. HARN 1.2 history row: "was recorded no later than its transaction" omits "and than the derivation" that the Dates row has. Fix: add the words. The Notes say STND.HARN.29 "binds, because it instantiates GUARD.2, GUARD.11, and GUARD.12"; it also instantiates GOV.48.
3. STDC Terms import Checking build; the text never uses it. Drop the import or use the term.
4. FTN Notes: "the files record no such direction for Fortran" reads as search narration. Fix: "no direction of the custodian asks for the newest revision of Fortran".
5. FTN.10 sentence 1 excepts a variable that only default initialization initializes, on a fact the Notes mark unverified (default initialization does not imply SAVE). The exception narrows the rule, so the risk is low. Mark the exception as resting on an unverified fact, or verify it.
6. CXX 1.1, PY 1.0.1, JL 1.1 and the adoption entries say "ratified by the custodian on 2026-10-24" before ratification. The round driver's START comment covers it only if the round is applied after ratification (reconciliation C, Should-fix 1, not answered in the fix passes).

## HARN.29 against `authorizations.py`

The rows Status, Grantor, Extension, Record, Dates, Standing, and Form match the code.

- **Standing:** `irrevocable(entry, kind)` marks publish and transmit always, and any kind at a destination whose `provisioned` is not true. That is the PROJ.7 table (last column) in the rehearsed corpus. A per-entry, per-kind refer leaves the other entries in force.
- **Standing, per action:** a per-action authorization is referred, not an error, as the row and the Notes say.
- **Form:** a malformed entry fails closed and the derivation stops. This matches the Notes ("nothing of that authorization is relied on"), the docstring, and `test_malformed_entry_fails_closed`.
- **Record:** a `revoke` with no list of targets counts as naming the file. This is stricter than the row and fails closed.
- **Signature:** the code requires that every signature of the ledger verify (`ledger_problems` empty). The row asks only that the transaction of the file carry an accepted signature. Stricter, fails closed.
- **Form, addresses:** the code admits only https or ssh addresses of a fixed shape, distinct kinds, and `expiry-horizon`. PROJ.6 states no such patterns or horizon. Safe, but the row says "the form that STND.PROJ.6 gives".

None of these asks less than the provision. Fix, if wanted: one clause in the Notes saying the harness applies the rows with these further limits.

## Item by item (fixpass.md, fixpass-2.md)

- **Does what was asked:**
  - References rows and the check (fixpass 2).
  - RUST class paragraph and the DSGN.3 reading (fixpass 9).
  - Conditioned tool demands: RUST.5, .23, .31, STDC.22, .29, FTN.36 (fixpass 10).
  - FTN Terms (fixpass 14).
  - Panic term, Language edition, Revision in force, MNEM reason, newest-edition sentence (fixpass-2 2, 3, 4, 5).
  - NDEBUG sentence in STDC (fixpass-2 9).
- **Facts checked:** Panic term (rs1 lines 90-91, 103), edition default and interoperation (rs1 line 172), 186 reports, 264 bugs, 75 percent (rs1), and the c1 facts for 221, 8,575, 323, twofold slowdown, SIGFPE/SIGILL/SIGSEGV. All are supported.
- **Narrowing:**
  - RUST.14 is word for word the old text inside the new condition.
  - The CXX.17 row of STDC.2 only adds a condition.
  - STDC.2 keeps the CXX.16 errno clause as new text. It is argued in the Floor paragraph and the rationale, and handed to the custodian.
- **Attributions:** no sentence attributes an unmade ruling. "Direction for the latest C++" and "the custodian's convention" in STDC and FTN rest on the adopted CXX and JL Notes. The PY/JL rulings are said to be made for PY and JL.
- **Class onsets:** match STND.CLASS.10 (DSGN.4, DSGN.5, INTPR.10 at CSQ2; INTPR.8 at CSQ1; the rest CSQ3), and each departure is argued. The three-modal bundles named in RUST equal the g.18 list.
- **Drafting narration:** none found in the Notes of STDC, RUST, FTN, HARN.
- **Rationales:** STDC, RUST, FTN, CXX 1.1.1, PY, JL, HARN match their final text. "Review of STND.HARN.28 by the command pairs" is the corpus convention (HARN.28 is the conflict-candidate review).

## Could not check

- The other new standards (BUILD, WFLOW, SV, LEAN), CONC 1.1, VVUQ 1.4, PROJ 1.2: not in my scope except by the whole-round scripts.
- About 25 facts of c1, rs1, and f1 spot-checked; not every Notes fact.
- The ISO texts, the Rust Reference, and the MPI standard.
- The installed behavior of the guard hooks (unit 0008 review, QA.8).
- Whether the custodian will rule as the Notes argue.
