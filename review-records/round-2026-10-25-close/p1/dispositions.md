# P1 dispositions of the cold review and the pair review (2026-10-25)

Scope: `review-cold.md` (3 Defects, 7 Should-fix, Optional items), `review-pairs.md` (F1 to F12), `p2/for-p1.md`, and the lead's directions. Facts are now cited from `research/round-addenda/a2-language-facts.md` (a2) where it confirms them. Result: reading copies `<ID>-0.2.md`, `delta-0.1-0.2.md`, pair lists regenerated, `code-interface.md` 0.2.

## Cold review

| Item | Disposition |
| --- | --- |
| D1 CODE.16 s3 binds Fortran | **Fixed.** The finite-value sentence becomes new **STND.CODE.21**, a default (DSGN.2, from CSQ3), so FTN.18 stays a default. The binding form stays where it was ruled or ratified: **STND.CXX.18** keeps that sentence (it is no longer withdrawn), and new **STND.STDC.40** applies its C reading, as STND.STDC.2's table did in 1.0. The CODE Notes say that the hazard is a documented license and that the deletion is unverified (a2). |
| D2 CODE.16 s2 reach in Python and Julia | **Fixed.** s2 now reads "a definition that the source of the work gives to conditional compilation" (F2's wording). The Notes state the added reach: none in Python; in Julia, a check under `@static if` on a source constant. They also state what s1 adds to Python and Julia (the CPS checks in `assert`, `@assert`, and `@boundscheck` forms). The rationale says the same. |
| D3 CXX.32 wider than RUST.13 s2 | **Fixed.** It is now "Where the work installs a terminate handler, that handler SHALL deliver ... a diagnosis of each condition ... that a C++ exception carries to it". The Notes say that without a handler, STND.CODE.14 still asks for the halt's diagnosis. No separate default is added: STND.CODE.14 covers that case. |
| 4 High assurance beyond C++ | **Decision put to the custodian** (rationale and Notes), with the conditioned alternative. The Notes say STND.STDC applied it to C on 2026-10-24. |
| 5 CODE.19 Note orders two defaults | **Fixed.** The Note now says another language standard yields "where its own text says so". The clause for JL.1 and PY.14 goes to P2 (`for-p2-p3.md`). CXX.2 s2 gains a carve-out for high-assurance code under STND.CODE.19 (pair F10). |
| 6 CODE.16 bundle | **Resolved.** Two sentences on one subject, the form of a required check; the Notes say they apply together. |
| 7 CODE.14 contract clause | **Fixed.** Now "in its result" (F1). |
| 8 Term not the exact union | **Fixed.** "Function" now includes procedure, subroutine, and method. The Notes list the widening by documentation per language, as a decision. The FTN exclusion goes to P3 (F5). |
| 9 What CODE.6 newly binds | **Fixed.** The Notes add one sentence each on C and C++ (an `assert` on a documented argument), Lean (nothing: a proved precondition has no run-time check), and hardware descriptions (top-level ports; documented functions and tasks). |
| 10 Unmarked facts | **Fixed.** NDEBUG is cited to a2 (N3220 7.2) in CODE and STDC; CXX cites CODE. The CXX.27 reason for Julia is corrected (`--check-bounds=no`, JL.13, JL.18, JL.34 s1, P2's default in words), and the Rust claim is marked unverified. The CODE.15 Notes say the declaration reading lowers the reach of RUST.14 and of the STDC 1.0 row. |
| Optional | The "Untrusted input" Notes paragraph is trimmed. A sentence says a Rust panic fits CODE.14. The STDC history row says no identifier is reused. Restatements in other packages go to P2 and P3. The two uses of "any" are in Notes and are kept. |

## Pair review

| Finding | Disposition |
| --- | --- |
| F1 | Fixed (cold 7). |
| F2 | Fixed (cold D2). |
| F3 | Fixed. STND.CODE.21 sentence 2 covers an annotation in the source. |
| F4 | Fixed. The term says "interface for outside use" and "places in its public interface". |
| F5 | To P3: drop the exclusion of external procedures. |
| F6 | To P2 and P3 (`for-p2-p3.md`, with a suggested change for each restatement). |
| F7 | Fixed. The reasoning on `assert` is in CODE alone; CXX and STDC keep only the language facts and cite CODE. |
| F8 | Fixed (cold 10, P2's point). |
| F9 | Fixed (cold D3). The CXX Notes add the safe state for a program that commands hardware (CPS.4, HW.EMBED.4, PRIME.13) as a description of what those provisions already ask. |
| F10 | Fixed. STND.CODE.19 names "each tool that compiles, synthesizes, interprets, simulates, or runs that code"; CXX.2 s2 carve-out. |
| F11 | Fixed. The STDC Notes say a nonlocal jump propagates and STND.STDC.31 governs it. STDC.31 s1 cites STND.STDC.2 for a listed condition. |
| F12 | Fixed in STDC. The Notes cover a pointer argument without an extent (the check of STDC.21 against the extent or limit that the contract states, STDC.7 and STDC.27). The widening is listed as a decision in the CODE Notes; the SV Purpose goes to P3. |

## P2's point

The CXX checking paragraph is corrected. It describes P2's new default in words, without an ID, because STND.JL.36 does not exist when CXX 1.2 applies.

## Rehearsal after the fixes

- `apply_close_p1.py` on entry 147: entries 148 to 150, all eight verify families PASS. The only warning is g.18 (three modals), now on CODE.19 alone among the new provisions.
- `findings.py`: no defect anywhere in the corpus. The only review-class item is g.11 on CXX.3, whose text is unchanged.
- `check_refs`: 0 missing rows for STND.CODE, STND.CXX, and STND.STDC.

## Decisions for the custodian (revised)

1. **Untrusted input.**
   - The union of the language placements and the interface for outside use that the documentation or repository configuration names.
   - It widens PY (documented non-library or underscore functions), JL (documented unexported functions), RUST (documented functions of non-library crates), and FTN (documented external procedures).
   - Through CODE.6 it newly reaches C, C++, Lean, and hardware descriptions.
   - Floor: form only. Recommend the union.
2. **CODE.14:** wording only, in every language. Recommend yes.
3. **CODE.15:** conditioned on a declaration form. Recommend yes.
4. **CODE.16 s1** (CPS checks) for the languages with no ruling, and **s2** (conditional compilation, the `#define NDEBUG` case) for every language: form only. Recommend yes.
5. **CODE.21** stays a default in every language. The binding forms of CXX.18 (C++) and STDC.40 (C) are kept as ratified. Recommend yes.
6. **CODE.17, .19, .20 reach every language.** Recommend yes: they are defaults from CSQ1 and replaceable by decision. The alternative is to open each with "Where the work is high-assurance code in a language whose standard applies this provision".
7. **CODE.18:** binding in every language, at one sentence per claim. Recommend yes.
8. **CXX.32:** conditioned as RUST.13 s2. Recommend yes.
9. **CXX.27 against JL.34:** no change, for the reason now in the CXX Notes. Recommend no change.
10. **STDC.2 and STDC.40:** both keep floor arguments ratified on 2026-10-24. **STDC.39** (naming, R18). Recommend yes.
11. **Withdrawal** of CXX.16, .17, and .28 to .31; **CXX.18 kept**. Recommend yes.

## Verification of 0.2 (`verify-0.2.md`): dispositions for 0.3

| Item | Disposition |
| --- | --- |
| S1 | **Option (b).** New **STND.CXX.33**, "Terminate handlers where defaults are silent". It is a default that instantiates INTPR.8, with PRIME.4 and STND.CODE.14 in refers_to, and applies from CSQ1, the row of INTPR.8. Where the implementation's terminate handler writes no diagnosis of a listed condition, each program installs a handler or catches the exception in its entry point. It stays outside the binding STND.CXX.32. The CODE and CXX Notes no longer claim that STND.CODE.14 asks the end of a program to carry a diagnosis: they say no provision of STND.CODE or STND.CXX binds it, and PRIME.4 states the outcome. **Corrected reason for disposition D3:** a separate default is added after all, because no binding provision covered the case. |
| S2 | **Fixed.** The CODE Notes state the NDEBUG fact for C (a2, N3220 7.2) and mark the C++ header unverified. The CXX Notes say that the same for `<cassert>` is unverified. |
| S3 | **Fixed.** The STDC Floor paragraph now states the C hazard: two compilers document a license to assume no NaN or infinity (a2), the removal of an isnan or isfinite test is unverified, the binding form stays for C by the ratification of 2026-10-24, and STND.CODE.21 is the default for every other language. |
| S4 | **Fixed.** The CODE Notes (Responses and the floor sentence), the CODE rationale and history row, and `code-interface.md` 0.3 all state the whole pass-to-the-caller clause. |
| P3 O5 | **Accepted.** STND.CODE.14 now reads "in its result, in an argument that the caller passes to receive it, or by a mechanism of its language ...". This widens a permission, so its floor stays wording only. The Notes name the status argument of STND.FTN.29. |
| O1 | **Fixed.** The rationale says "before the inclusion of the header of the assert macro"; the Notes say a definition after the last inclusion is outside sentence 2. |
| O2 | **Fixed.** The STDC Notes keep the language fact and cite STND.CODE for the reasoning. |
| O3 | **Fixed.** Both statements are marked "(unverified)". |
| O4 | **Fixed.** The CODE Notes say the three sentences of STND.CODE.19 apply together. |
| O5 | **Fixed by restatement.** STND.STDC.40 states the outcome in C words, the text of STND.CXX.18 for C source: instantiates PRIME.4, DSGN.2, CPS.5, and CPS.9; refers to STND.CODE.6 and STND.CODE.21. A later change of STND.CXX.18 does not change C silently, and the Notes say so. |

### Rehearsal of 0.3

- `apply_close_p1.py` on entry 147: all eight verify families PASS, with g.18 warnings only.
- `findings.py`: no defect anywhere in the corpus.
- `check_refs`: 0 missing rows for the three documents.
- Pairs regenerated: CODE 93, STDC 44, CXX 69.
- Reading copies `<ID>-0.3.md`; `delta-0.2-0.3.md`.

### Decisions added for the custodian

12. **STND.CXX.33** as a default from CSQ1 (INTPR.8). Recommend yes. The alternative is an onset of CSQ3.
13. **The status-argument clause of STND.CODE.14**, a widened permission. Its floor is wording only. Recommend yes.

## Reconciliation reviews: dispositions for 0.4

| Item | Disposition |
| --- | --- |
| B blocking 2 | **Fixed.** The CODE Notes (Finite values) read "STND.CXX.18 for C++ and STND.STDC.40 for C". |
| Responses (A S1a, B 5) | **Fixed.** The Notes name STND.RUST.13, STND.PY.32, and STND.CXX.32 as the forms for a hook or handler, and STND.CXX.33 as the C++ default. The IDs are cited as the lead directed; PY.32 and CXX.32 come after entry 148, and their citations resolve once P2 and CXX 1.2 apply. |
| CXX Purpose (A S2) | **Fixed.** It lists STND.CXX.33. |
| CODE.16 s2 (B should-fix 1) | **Fixed.** Rewritten as "Where a build holds the code that a check ... guards, that check SHALL NOT be turned off in that build by a definition that the source of the work gives to conditional compilation". The Notes add the reach per language: Rust nothing (a build-configuration condition is an execution setting already reached), Fortran preprocessed source only (unverified that the standard has none), SystemVerilog conditional compilation directives, Lean nothing (unverified). The floor argument now holds per language. |
| STDC.2 (B should-fix 2) | **Fixed** with B's wording: "A report of a condition that PRIME.4 lists through errno alone SHALL NOT be taken as passing that condition to the caller in a result under STND.CODE.14". |
| HA onsets (B should-fix 4) | **Fixed.** The CODE Notes call the onsets of CODE.17, .19 (CSQ1, before the CSQ0 rows) and CODE.20 (CSQ4 where a standard is adopted) departures from STND.CLASS.10. They cite the ratifications for C++ (CXX.28, .30, .31) and C (STDC.1), and argue them for the other languages. |
| CXX.27 against JL.34 (C S4, A) | **Fixed.** One resolution in the CXX Notes and rationale: STND.CXX.27 is unchanged, and the Julia standard gains its counterpart in the same round, named in words. P1 decision 9 now reads the same way. |
| B should-fix 7 (edition yields) | **Fixed.** The CODE.19 Notes say that a non-blocking newest-release check, as in STND.RUST.1 and STND.JL.3, builds no delivered code and is outside STND.CODE.19. |
| A S7 (STDC.40 restates CXX.18 by design) | **Recorded as a decision** (below). The BUILD Notes citation is P5's. |
| B 3 (CUSTODIAN.md line on high assurance) | If decision 6 is ratified, that line needs amending after ratification. This is the lead's step. |

### Rehearsal of 0.4

- `apply_close_p1.py` on entry 147: all eight verify families PASS, with g.18 warnings only.
- `findings.py`: no defect anywhere in the corpus.
- `check_refs`: 0 missing rows for the three documents.
- Instantiates are unchanged, so the pairs of 0.3 stand.
- Reading copies `<ID>-0.4.md`; `delta-0.3-0.4.md`.

### Decisions revised or added

- **9 (revised).** For CXX.27 against JL.34: CXX.27 is unchanged, and STND.JL.36 is added as its Julia counterpart. Recommend yes.
- **14.** STDC.40 restates CXX.18 in C words by design, so that a later change of CXX.18 does not change C silently. Recommend yes.

## P3's withdrawals (`p3/for-p1.md`): dispositions for STND.CODE 0.5

These are Notes and rationale changes only; no provision text changes. STND.CODE no longer names STND.FTN.18 or STND.RUST.14, so it holds whether the custodian keeps STND.RUST.14 or withdraws it.

- **Ignored results.** The Notes now say the reading lowers the reach that STND.RUST 1.0 and the C reading of STND.STDC 1.0 gave the outcome, and that in Rust the must_use attribute is the form of the declaration.
- **Finite values.** The Notes now say "STND.CODE.21 holds it as a default for Fortran, as for every other language without a binding form".
- **Rationale.** It says "the ratified default for Fortran".

Rehearsal: `apply_close_p1.py` passes all verify families. `findings.py` and `check_refs` are clean for the three documents. Reading copy `STND.CODE-0.5.md`; STND.CXX and STND.STDC are unchanged from 0.4.
