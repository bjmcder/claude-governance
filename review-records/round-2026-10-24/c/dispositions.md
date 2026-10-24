# Dispositions: STND.STDC 0.1 to 0.2

Draft 0.2 answers the cold review (`review-cold.md`) and the pair review (`review-pairs.md`) of draft 0.1, under the lead's decisions of 2026-10-24. It is rehearsed on the live corpus (entry 116) after the amendment round (`apply_round_2026_10_24_amend.py`, STND.CXX 1.1 among them) and the BUILD round, then the C round. The rehearsal record is `.scratch/c-draft/rehearse_02.py`; verify passes all eight checks; `findings.py 'STND\.STDC'` returns nothing. Reading copy `draft-0.2.md`, pair list `pairs-0.2.md`.

## Numbering

STDC.28 (errno alone) is folded into the STDC.2 table, and STDC.38 and .39 are merged, so the draft has 38 provisions. Map from 0.1 to 0.2: 1 to 27 unchanged in number; 28 withdrawn into 2; 29 to 28; 30 to 29; 31 to 30; 32 to 31; 33 to 32; 34 to 33; 35 to 34; 36 to 35; 37 to 36; 38 and 39 to 37; 40 to 38. Binding: STDC.2 and STDC.28.

## Lead decisions

| # | Decision | Disposition |
| --- | --- | --- |
| 1 | Rehearse on STND.CXX 1.1; check rows; fix instantiates | Done. CXX.15 row: "without the words reference, view, iterator, and C++ exception" (fits 1.1, which cites STND.CONC.6). CXX.23 row: only the name volatile std::sig_atomic_t is read, so the lock-free atomic alternative stays. STDC.2 instantiates PRIME.4, PRIME.2, DSGN.2, CPS.5, CPS.9 (from CXX.18). STDC.1 does not add HW.11: under 1.1, CXX.23 instantiates DSGN.15 alone and cites STND.CONC.3, which carries HW.11; adding it would put a CSQ2 ancestor on a CSQ3 row. HW.11 is cited in the Notes on bit-fields. |
| 2 | Keep the C reading; revision rule in the Term; onset column; shared provisions as a decision | The Term reads "at the revision of STND.CXX in force". STDC.1 has an "Applies from" column, a body that applies each row from its class "each sentence keeping its modal and the provision its mode", and a MAY sentence that lets a project replace one row and keep the others (REPRO.7). Shared provisions in STND.CODE: decision 1 below, no change this round. |
| 3 | No extension of C++ rulings without argument; no newest-edition rule | The CXX.2 row is dropped: the standard sets no edition for C, and the C reading of CXX.4 states one. STDC.3 is now a default, "Lowered C editions recorded" (DSGN.3, REPRO.7): a change that lowers the edition carries a decision record naming its reason. STDC.2 is argued in the Notes from PRIME.4 and PRIME.2 alone, row by row; the extension of the rulings is decision 2. |
| 4 | STDC.28 folded; STDC.29 order, facts, argument; PRIME.4 list; STDC.29 against STDC.30 and CXX.25 | Errno alone is a change in the CXX.16 row of STDC.2. New STDC.28: the error indicator is tested before the stream is closed, then the result of the flush or the close. The two stream facts are marked unverified. The provision is argued from the last sentence of PRIME.4 and is decision 3. The Notes state PRIME.4's four kinds and say that a full volume is resource exhaustion and another output error is not in the list. STDC.29 (was 30) gains a sentence: a call whose failure the test of STDC.28, or an error handler that ends the run, receives carries the suppression of STND.CODE.4 with its reason, which the warning of the C reading of CXX.25 then accepts. |
| 5 | STDC.12 shift; CXX.4 row | STDC.12 judges the left operand by its type after the integer promotions. CXX.4 row: "The options stated include each option that defines a behavior that the ISO C standard leaves undefined". |
| 6 | Terms | Foreign interface defined for C, without reference to C rules. C source leaves out external code that the work incorporates and keeps apart (STND.DEPS.11). The C reading takes a term of this standard in place of the STND.CXX term of the same name. |
| 7 | Onsets by the table | The Notes read the DSGN.2 row once, as STND.CXX reads it: checks of untrusted input where it enters from CSQ3; retained checks of other preconditions, postconditions, and invariants from CSQ1 (CXX.24, CXX.27). STDC.11, .12, .13, .18 now instantiate DSGN.1 alone (show the operation safe by any listed means) and apply from CSQ3; STDC.21, .22, .27 check untrusted input, CSQ3. STDC.37 (was 39) is at CSQ3 by DSGN.3, with its second sentence in effect where CXX.26 applies (CSQ2); the Notes list STDC.8, 9, 10, 11, 12, 14, 27 and say why STDC.13 adds no kind. |
| 8 | Build | STDC.16, second sentence, cites STND.BUILD.13 (checking build without the option). The Purpose names the build matter held through the C reading of CXX.4 and CXX.25; the Notes name STND.BUILD.11 and .12 as the language-neutral forms. |
| 9 | The rest | STDC.8 and STDC.11 admit a static check; STDC.11 applies to operands from outside the function (c1 practice 2). STDC.5 sentence 2 admits a function of the work that owns the release. STDC.35 (was 36) covers accesses with at least one write. STDC.20 reads "a string or a sequence of bytes", and the Notes leave numerical narrowing to NUMER. CXX.7 row: a distinct type is a pointer to a distinct type or a wrapping structure, not a type alias. STDC.16 and STDC.26 compare within the tolerance of the acceptance criterion. Notes: the version-macro obligation, the "widely used compiler" claim, the standing-directions sentence, and the narration of how c1 was read are gone; the 40 percent figure is attributed to unstable code in general. STDC.38 and .39 are merged as STDC.37. STDC.31 (now 30) leaves the closing of a stream to STDC.28. |

## Cold review

| Finding | Disposition |
| --- | --- |
| Defect 1, STDC.29 facts and order | Fixed: lead decision 4. |
| Defect 2, PRIME.4 list | Fixed: lead decision 4; the CERT resolution now rests on "kind that PRIME.4 lists" without the phrase on a failed write. |
| Defect 3, Foreign interface | Fixed: lead decision 6. |
| Should-fix 1, mechanism | Accepted as a citation; lead decision 2. "Each sentence keeping its modal and the provision its mode" replaces "each sentence with its modal". |
| Should-fix 2, rows and instantiates | Fixed: lead decision 1. CXX.28 row is now "None". |
| Should-fix 3, CXX.7, .9, .12 | CXX.7 row added (lead decision 9). CXX.9: the Notes give the reason (C library results that the implementation defines), say that c1 lists CXX.8 to .10 as not carrying, and mark the examples unverified. CXX.12 unchanged. |
| Should-fix 4, STDC.3 and STDC.2 | Lead decision 3: STDC.3 a default; STDC.2 argued from its prime directives; decision 2. |
| Should-fix 5, STDC.28 | Folded into STDC.2 (lead decision 4). STDC.31 sentence 1 ("an object that its contract names") is a default channel for failures the caller handles and does not admit errno alone for a listed condition, which the CXX.16 row governs. |
| Should-fix 6, cost of STDC.8 and .11 | Fixed: lead decision 9. |
| Should-fix 7, STDC.5 | Fixed. |
| Should-fix 8, DSGN.2 onset | Fixed: lead decision 7. |
| Should-fix 9, build overlap | Fixed: lead decision 8. STDC.25 (branches compiled), STDC.26 (a build without the qualifier), and STDC.37 (warning set) remain checks of C source; STDC.37 extends a set that the C reading of CXX.25 and STND.BUILD.12 both record. |
| Should-fix 10, proportion | STDC.28 folded and STDC.38/.39 merged (38 provisions); the Notes are trimmed in the checking, strings, overflow, and kernel passages. STDC.11 with .12 and .33 with .34 stay apart: their instantiates and subjects differ. |
| Should-fix 11, Notes | Fixed: lead decision 9. |

## Pair review

| Finding | Disposition |
| --- | --- |
| Defect 1, STDC.12 | Fixed: lead decision 5. |
| Defect 2, CXX.4 and UB options | Fixed: CXX.4 row; the Notes no longer say CXX.4 states them as written. |
| Should-fix 1, STDC.29 against STDC.30 and CXX.25 | Fixed: second sentence of STDC.29 (was 30), suppression under STND.CODE.4; the MPI.5 error handler is named. |
| Should-fix 2, STDC.39 onset and list | Fixed: lead decision 7. |
| Should-fix 3, one reading of the DSGN.2 row | Fixed: lead decision 7. |
| Should-fix 4, C source and incorporated code | Fixed: lead decision 6. |
| Should-fix 5, STDC.36 reads | Fixed. |
| Should-fix 6, STDC.20 other data | Fixed. |
| Should-fix 7, CXX.7 type alias | Fixed: row. |
| Should-fix 8, tolerances | Fixed: STDC.16 and STDC.26; the Notes cite STND.VVUQ.82 and NUMER.11. |
| Should-fix 9, STDC.28 restatement | Fixed: folded into the CXX.16 row. |
| Should-fix 10, Notes (a) to (c) | Fixed. |
| Should-fix 11, order and rehearsal | Rehearsed after STND.CXX 1.1 and STND.BUILD; the lead sets entry numbers and times (the C and BUILD scripts both carry the placeholders 20:00 and 20:05, which the rehearsal accepted). |
| Optional 1 (static check; index) | Taken: static check in STDC.8, .11, .18; STDC.21 names an index; the Notes say a comment is no substitute for the binding check of STND.CODE.6. |
| Optional 2 (# and ##, type names) | Taken in STDC.24. |
| Optional 3 (indicator before close) | Taken in STDC.28. |
| Optional 4 (unchecked branch) | Taken in the Notes (PRIME.3). |
| Optional 5 (presence or absence) | Taken in the Term Conditional feature. |
| Optional 6 (locks under CONC.8) | Taken in the Notes. |
| Optional 7 (allocation result) | The Notes say an untested allocation result discards a listed failure, which STND.CODE.7 forbids; no new provision. |
| Optional 8 (pragmas) | Not taken: the pragmas are not in c1; the Notes keep the access pragma unverified. |
| Optional 9 (CXX.2 library documentation) | Moot: the CXX.2 row is dropped. |
| Optional 10 (#if 0) | Taken in the Notes (STND.CODE.11). |
| Optional 11 (CXX.3 no row) | Moot: CXX.3 is not applied; STDC.3 is the C default. |
| Optional 12 (CXX.23 condition) | Taken in the Notes: the condition also reaches an interrupt handler of a constrained target. |
| Optional 13 (mnemonic) | Stays a decision (decision 5). |
| Observation 3 (STDC.40 and CONC.27) | Taken: one record meets both (Notes, now STDC.38). |
| Observation 5 (shared headers) | Taken: one sentence in the Notes; the linkage difference is marked unverified. |

## Decisions for the custodian

1. Shared provisions: whether the language-neutral provisions of STND.CXX that STND.STDC applies (CXX.16, .17, .18, .29 binding; CXX.24, .26, .27, .28, .30, .31 default) move to STND.CODE, so that every compiled language, Fortran among them, cites one text. Recommended for a later round; no change in this one.
2. Whether the rulings that CXX.16, .17, .18, and .29 raise no floor extend to their C reading. Recommended: yes, on the arguments in the Notes of STND.STDC, which rest on PRIME.4 and PRIME.2 alone.
3. STDC.28 (stream errors, binding): whether the last sentence of PRIME.4 reaches a failed write that is not resource exhaustion. Recommended: yes, at the cost of two tests per stream; otherwise make it a default.
4. Whether the agent rule of CXX.3 applies to C as a binding rule (GOV.48). Recommended: keep STDC.3 a default until the custodian gives a direction on the edition of C.
5. Mnemonic: STDC (recommended) or CC.
6. Naming: whether the CXX.14 table applies to C.
