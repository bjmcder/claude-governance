# Cold verification of package P1, revision 0.2 (2026-10-25)

Verifier with no stake in the amendments. I changed no file except this report. Scratch: `/tmp/claude-1000/verify-p1/` (`rules.py`, `rehearse.txt`).

## Fresh rehearsal and scripts

- `rehearse governance ../tools/amendment-scripts/apply_close_p1.py` from `harness/`: entries 148 (CODE 1.2), 149 (STDC 1.1), 150 (CXX 1.2) appended on 147. `verify`: ids, mnemonics, references, manifests, ledger, templates, status, logic all PASS; one g.18 warning (CODE.19). The source corpus is unchanged.
- `findings.py` on `STND\.(CODE|CXX|STDC)`: no defect class. Review class only: g.11 on CXX.3 (text unchanged) and g.18 on CODE.4, .13, .19 and CXX.2, .4, .5, .10, .11, .19 to .22 (all old except CODE.19).
- `check_refs.py`: 0 missing rows for the three documents (the other 15 documents listed are not in P1).
- My rule script ran over all 22 new or changed provision files. No sentence has two modals. No provision has more than three. No banned word appears. Body IDs equal instantiates plus refers_to everywhere. No trailing condition.
- The reading copies match the rehearsed files: every body and every Notes, Purpose, and Terms paragraph was found verbatim.
- All three rationales end with the fixed tail, which is the same as the 50 earlier entries. No entry of this round is cited by number.
- Withdrawn IDs: CXX lists 16, 17, 28, 29, 30, 31 in `withdrawn`, and the files are gone. CXX.32, STDC.39, STDC.40 and CODE.14 to .21 reuse none. The old IDs appear only in the front matter and the Revision Histories. STDC.2 keeps its ID with a new title and a narrower body, and the history row says no ID is reused.

## Dispositions

All hold in the text.

- **CODE.14.** The body ends "in its result or by a mechanism of its language, an exception among them, that propagates the condition to the caller". The contract clause is gone.
- **CODE.16.** Sentence 2 reads "a definition that the source of the work gives to conditional compilation". Sentence 3 is gone. The Notes state the reach in Python (none) and Julia (`@static if`).
- **CODE.21.** It is a default (DSGN.2, CSQ3). Sentence 2 covers an annotation in the source. The Notes say FTN.18 stays a default and CXX.18 and STDC.40 keep the binding forms.
- **CXX.18.** Kept, with one sentence and a ref to CODE.21. Its history is consistent.
- **CXX.32.** It opens "Where the work installs a terminate handler". The Notes call it the counterpart of RUST.13 s2.
- **CODE.19.** It names "each tool that compiles, synthesizes, interprets, simulates, or runs". The CXX.2 s2 carve-out is present.
- **Terms.** The term reads "interface for outside use" and "places in its public interface". "Function" includes procedure, subroutine, method, or other unit of code that a call enters.
- **NDEBUG.** The CODE Notes give the reasoning once, with a2 7.2. They say the effect needs the define before the inclusion of the header, that the macro is an expression that does nothing, and that it is redefined at each inclusion. CXX points to CODE.

## Floor

No change raises it beyond what the reviews accepted. The finite-value default is the only demotion (FTN.18 stays a default), and CODE.14 widens a permission. STDC.40 is the C reading of the binding CXX.18. Ledger entry 130 recorded the custodian's ruling that the extension to C raises no floor. That is a separate act for C, not a carry-over of the C++ ruling. The weakness is in the Notes (S3).

## Pairs

The pair lists hold 93, 41, and 69, against 90, 38, and 63. The new pairs are CODE.21 with CPS.5, CPS.9, and ML.6 (3); STDC.40 with HDES.14, HW.8, and HW.GPU.3 (3); and CXX.18 with CPS.5, CPS.9, ML.6, HDES.14, HW.8, and HW.GPU.3 (6). The numbers are contiguous, no row repeats, and each new pair appears once. I read each other side.

- The CPS and ML pairs share DSGN.2. They are supportive: those checks are why NaN must stay testable.
- The three hardware pairs share only PRIME.4 and do not touch the finite-value rule.
- I also read NUMER.16 and NUMER.17, which the script does not pair. They govern the listing and verification of an approximation, so they are compatible.
- No conflict, no unowned matter, no restatement beyond the ratified binding of the default.

## Findings

### Defect
None.

### Should-fix

**S1. The Notes claim an obligation that the body does not hold.**
- The CODE Notes ("Responses") say a condition that no caller answers "ends in a halt, which the provision asks to carry its diagnosis". The CXX Notes say "where the work installs none, STND.CODE.14 still asks the halt to carry its diagnosis". Disposition 3 relies on this to add no default.
- The body allows passing the condition by an exception. An uncaught C++ exception is a complete response, and nothing asks `std::terminate` to write a diagnosis. The Notes say the default is unverified.
- Fix: reword both passages to say that without a handler no provision of STND.CODE or STND.CXX asks the diagnosis of the end of the program, and that PRIME.4 states the outcome. Correct the reason in disposition 3. Alternatively, add the default to CXX.
- Notes must not state an obligation (CUSTODIAN.md).

**S2. The NDEBUG fact is stated for C++ without a source.**
- a2 section 3 reads the C working draft (N3220 7.2) only. The CODE Notes say "the assert macro of C and C++", and the CXX Notes say "defined in the source before `<cassert>` is included". Cold review item 10 asked for such facts to be marked.
- Fix: after the CXX phrase, add "(a2 reads the C header; the same for `<cassert>` is unverified)". Or restrict the CODE sentence to C and mark C++.

**S3. The floor argument for STDC.40 gives the ratification and the cost, not the C hazard.**
- The ruling for C++ was not extended to C without an argument (R22). The ratification is the act that extends it. But the STDC Notes and rationale say only "one choice of option".
- They omit that for C the license is documented (a2: GCC and Clang) and the deletion of tests is unverified.
- Fix: add one sentence to the STDC Floor paragraph. It says the option is a documented license, that the removal of `isnan` or `isfinite` tests is unverified, that the binding form stays by the ratification of 2026-10-24 (entry 130), and that CODE.21 is the default for every other language.

**S4. `code-interface.md` 0.2 and the rationale mis-state CODE.14.**
- Row 10 says the text is "in its result", the words of PY.22 and the rest. The rationale says "in their words". The CODE Notes say "in the words of the first sentences". The body adds "or by a mechanism of its language, an exception among them, that propagates the condition".
- P2 and P3 read these files to align their restatements (F6). Their sentences, such as RUST.13's "panic", may be taken as outside the clause.
- Fix: in all three places, write "in its result or by a mechanism of its language that propagates it (F1)".

### Optional

- **O1.** The CODE rationale says CODE.16 "reaches a definition of NDEBUG in C and C++ source". Add "before the inclusion of the header". The Notes should add that a define after the last inclusion turns nothing off and so is outside sentence 2.
- **O2.** The STDC Notes restate the NDEBUG mechanism in one sentence, though F7 and the dispositions say "once". Keep the language fact and cite CODE.
- **O3.** Two Notes statements are flat: "The C++ standard library checks no precondition unless a check mode of it is chosen" (CXX) and "safe Rust checks indexing" (the CXX rationale). Mark both "(unverified)" as the Notes mark Rust elsewhere.
- **O4.** CODE.19 carries three modals (g.18). Its Notes do not say the three sentences apply together, as CODE.16's do. Add one clause.
- **O5.** STDC.40 states no outcome. It depends on the Term "C reading" and the revision of CXX in force. A later change to CXX.18 changes C silently. This is the pattern of STDC.1, so a Term or Notes sentence would do, or restate the "SHALL NOT be compiled with an option..." sentence in C words.
