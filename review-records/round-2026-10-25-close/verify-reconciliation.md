# Verification of the reconciliation fixes (closing round of 2026-10-25)

Cold verifier. Scratch and scripts: `/tmp/claude-1000/verify-recon/`. No file of REPO was edited but this report.

## Runs

- **Fresh rehearsal** (copy `/tmp/rehearsal-q_aihb_7/governance`): 28 entries, 148 to 175, in the order CODE, STDC, CXX, PY, JL, RUST, FTN, SV, LEAN, 14 P5 documents, BUILD, OFFLD, MPI, OMP, HARN.
  - `verify`: eight families PASS, g.18 warning only.
  - `findings.py .`: 242 findings, all class review, none defect.
  - `check_refs.py`: 48 documents, 0 with missing rows.
  - `references --check`: PASS.
- **`WITHDRAW_RUST14 = False`** (scratch copy of the scripts): verify PASS, findings 0 defect, check_refs 0 missing.
- **`OPTION = "c"`**: the same results. STND.HARN.30 is absent, and the row Signature stays.
- **Prefixes.** I rehearsed all 28 prefixes of the order, with `verify` on each. All pass except six states (after entries 163 to 167 and 169), which fail the ledger check "content changed outside the ledger: HW" or "HDES". The order of 99d5b57 fails the same way at its 16th state. This comes from the P5 family scripts and is not new. Every final state passes.

## Blocking items of A, B, and C

| Item | Verdict |
| --- | --- |
| A1, FTN.18 | Closed. The `withdrawn` field lists it, the file is deleted, and the Purpose is retargeted. It is cited nowhere outside the history row. |
| A2, RUST.14 | Closed as a decision. The default withdraws it. `WITHDRAW_RUST14 = False` keeps it with the citation, and both forms verify. Minor point (S5) on the keep form. |
| B1, HARN.30 | Closed as a decision. The rationale and `decisions-final.md` item 21 put (a), (b), and (c) to the custodian, and `OPTION = "c"` builds. Minor point (S6) on the `c` rationale. |
| B2, CODE Notes, finite values | Closed. They read "STND.CXX.18 for C++ and STND.STDC.40 for C". |
| C B1, BUILD record | Closed. `p5/dispositions.md` records the cold read and S1. BUILD cites STDC.40 and lists STND.STDC in References. |

## Blocking

**B1. The CODE Notes cite three withdrawn identifiers.**
- The fix for floor Should-fix 4 added "ratified these onsets for C++ with STND.CXX.28, STND.CXX.30, and STND.CXX.31" to the paragraph on the onsets of STND.CODE.17, .19, and .20.
- Those three are withdrawn by entry 150, and the CODE Notes keep citing them in the final state. This breaks the rule that no citation of a withdrawn identifier remains outside histories (brief A; item 5).
- It is the only such citation in the final corpus. I searched for all eight withdrawn identifiers, in both variants.
- Fix: in `apply_code_1_2.py`, write "with the provisions that STND.CXX 1.1 held on high-assurance code (moved here by this amendment)". The identifiers may stay in the history row.

**B2. STND.RUST.1 sentence 3 does not put its condition first.**
- The fix reads "At the interval ..., a check ... SHOULD build and test the work, other than its high-assurance code whose edition and toolchain STND.CODE.19 fixes, with the newest stable release". The exception follows the modal.
- STND.JL.3 sentence 3 got it right: "Other than for code whose version of Julia STND.CODE.19 fixes, a check ...".
- Fix in `apply_rust_1_1.py`: "Other than for its high-assurance code whose edition and toolchain STND.CODE.19 fixes, a check that reports its failure without blocking a change SHOULD, at the interval that the repository configuration sets, build and test the work with ...". The modal count and the body IDs stay the same.

## Should-fix

- **S1. The reordering does not do what the script header says.**
  - The header of `apply_round_2026_10_25_close.py` says no entry leaves a document citing an identifier that CXX 1.2 withdraws.
  - After entry 150, STND.RUST (until 153), STND.FTN (154), and STND.LEAN (156) still cite STND.CXX.16 or .17 in their Notes. These are old citations, and the other states are free of them.
  - Fix: apply P3 between STDC and CXX. I tested the order CODE, STDC, RUST, FTN, SV, LEAN, CXX, then the rest. It leaves no stale citation at any state except B1, and verify passes.
  - Otherwise, correct the header and say that the end state is the guarantee.
- **S2. Forward references in the CODE Notes.** Verify accepts all of them (8 of 8 at every state).

  | Cited | Exists from |
  | --- | --- |
  | STND.STDC.40 | entry 149 (dangling after 148) |
  | STND.CXX.32, STND.CXX.33 | entry 150 |
  | STND.PY.32 | entry 151 |

  - STND.PY.35 names STND.JL.39 in its Notes between entries 151 and 152.
  - The CXX Notes name JL.36 in words, so no ID dangles. Say in the ratification note that the CODE Notes are only complete from entry 151.
- **S3. CXX.18 sentence 1 became CODE.16 sentence 1 in other words.**
  - Old: "each check ... SHALL run, with its response, in every build".
  - New: "SHALL NOT be removable by an execution setting".
  - The ruled C++ text is reworded. I find the outcome equal for settings, but the two are not identical. Put it to the custodian as part of decision 4 of `decisions-final.md`, or restore the old wording.
- **S4. Reports A S9, A S10, and A S11 are not dispositioned in P1 or P4.**
  - A S9: the CODE Notes do not say that a language with no replaceable hook has no counterpart. Add one sentence.
  - A S10 is in `decisions-final.md` items 18 and 26. The OFFLD Notes still say the PERF second sentences "hold the same outcomes", which is not true of the first filling of caches. Soften it, or record the decline in `p4/dispositions.md`.
  - A S11 is optional. Say so in the dispositions.
- **S5. Keep variant of RUST.14.** The CODE Notes say the reading "lowers the reach that STND.RUST 1.0 ... gave". With RUST.14 kept, Rust is not lowered. Make that clause conditional on `WITHDRAW_RUST14`, as the RUST text already is.
- **S6. `OPTION = "c"` rationale.** It still says "the reading of STND.DRAFT.42 in the Notes are put to the custodian", but the Notes of that variant hold no such reading. Guard the clause with `OPTION == "a"`.
- **S7. `decisions-draft.md` is stale.** It says FTN.18 "stays a default" and RUST.14 "stays as ratified", against `decisions-final.md`. `decisions-final.md` is untracked. Archive the draft and commit the final.
- **S8. CODE Notes, onsets.** The Notes say CODE.17 and CODE.19 are "required for the safety-related components of CSQ0". That is an obligation in the indicative. Write "ask" or "advise".

## Drafting rules

I ran scripts over the 55 provisions that differ from `rendered/`: one modal per sentence, at most three modals, body IDs equal to instantiates plus refers_to, and a binding mode only with an instantiated provision. They found nothing. The condition-first scan found only B2 among the introduced sentences, JL.36 and the foreign-interface exceptions being unchanged forms. The 28 rationales end with the fixed tail (reviewer C checked this, and I did not rerun it). A scan of the added Notes sentences found only the S8 case. The other hits describe other provisions.

## Obligations against `rendered/`

- **Text identical:** RUST.34, FTN.30, LEAN.5.
- **A citation added only:** PY.22, PY.25, JL.13, JL.15, RUST.13, RUST.15, FTN.29, FTN.31, LEAN.25. Modals, modes, and instantiates are unchanged.
- **CXX.18:** sentence 1 moved (S3), sentence 2 kept.
- **STDC.2:** narrowed to the errno clause, retitled, ID kept. Its table rows now sit in CODE.14, .15, .16, .18, and STDC.40. The lowering of CXX.17's reach is disclosed in the CODE Notes.
- **RUST.14:** withdrawn by default, as a decision. FTN.18 is withdrawn by default, with its first sentence now the default CODE.21.

## Verdict

Not ready as it stands. B1 and B2 are small fixes in two scripts, and a rehearsal of the round and of both variants should follow them. S1 to S8 are Should-fix and do not block ratification. Ratification still needs the custodian's decisions on RUST.14, the HARN.30 reading, and the reach of the Untrusted input term.
