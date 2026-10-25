# Reconciliation review C (records and integrity), closing round of 2026-10-25

Reviewer C. Scratch: /tmp/claude-1000/recC. I changed no file but this report and `decisions-draft.md`.

## What I ran

- `rehearse governance apply_round_2026_10_25_close.py` from `harness/`: 28 entries, 148 to 175, in the order CODE, STDC, CXX; the 15 P5 documents; PY, JL; RUST, FTN, SV, LEAN; OFFLD, MPI, OMP, HARN. Copy: /tmp/rehearsal-grbnjzpy/governance. Source unchanged.
- `verify` on the copy: all eight checks PASS. One warning, g.18, carried from entry 147.
- `findings.py '.'`: 242 findings, every one of class review, none defect. Against the live corpus the only differences are three new g.18 notices (STND.CODE.19, STND.PY.35, STND.JL.39), each argued as one bundle in its Notes, and one fewer (the withdrawn STND.CXX.30).
- `check_refs.py` on the copy: 48 documents, 0 with missing rows. On the live corpus it reports 16, not the 22 of the brief (see decision 22).
- Harness suite: 247 tests, OK, 204 s.
- By script over all 28 entries: each rationale ends with the fixed tail exactly once; none cites an entry of this round (the only other entry cited is the pre-existing entry 53 in HARN); each header revision equals the revision in its rationale and in the single history row; each bump is the right segment for its class (minor raises the minor segment; editorial the editorial one); each history row opens with the class word of the rationale.
- Every new or changed provision (60 files): one modal per sentence, at most three per provision, no banned word, titles of six words or fewer and distinct, body IDs equal `instantiates` plus `refers_to`.
- Pairs: I regenerated `pairs` for all 13 amended standards. The pair files of P1, P2, P3, and P4 contain every computed pair of the changed provisions (P1 93, 44, 69; P2 62, 66), none missing.
- Reading copies: I composed the last copy of every amended standard from the copy and compared it with the last record copy (CODE, STDC, CXX 0.3; PY, JL, RUST, FTN, SV, LEAN 0.4; OFFLD, MPI, OMP, HARN 0.2). All are identical except the entry numbers. The P5 copies are not (S2).

## Blocking

**B1. STND.BUILD 1.0.2 (entry 165) has no review record (definition of done, item 3).**
`p5/review.md` covers the first 14 documents; `p5/dispositions.md` and `p5/gaps.md` do not mention BUILD, and the lead added the amendment after the review. I read it as a cold reviewer: the class (editorial) is right, the Notes-only change leaves every provision as it was, and the rationale matches the document. One Should-fix (S1). No pair review is possible, since no provision changes.
Fix: record this read in `p5/dispositions.md` as BUILD's cold review, and take or decline S1.

No other blocking item. Every blocking finding of every package review is closed in the text (checked below).

## Review records

| Package | Reviews | Last revision | Verified by me |
| --- | --- | --- | --- |
| P1 | cold, pair, verify-0.2, dispositions | 0.3 (not verified by anyone but P2 and P3's checks) | Yes. S1 to S4 and O1 to O5 hold in the text: CXX.33 exists as a default on INTPR.8 from CSQ1; the Notes of CODE and CXX no longer say that CODE.14 asks a halt to carry a diagnosis; NDEBUG is cited to the C draft and marked unverified for `<cassert>`; STDC.40 states the C hazard; CODE.14 gives the whole caller clause. CXX.33 has no pair row (no other provision shares INTPR.8 with it in the listed bases). |
| P2 | cold with pairs, dispositions | 0.4 | Yes. S1 to S9 hold in the text: PY.32's floor rests on the last sentence of PRIME.4; PY.35 and JL.39 are conditioned and carry the InterruptException and KeyboardInterrupt carve-outs; PY.34/37 and JL.37/38/40/41 are split; PY.36 and JL.40 name one owner; contiguity and strides come from documentation or a test. The ten new pair rows (PY.37, JL.41) repeat the partner set of PY.34 and JL.37, read as compatible there. |
| P3 | cold with pairs, dispositions | 0.4 | Yes. LEAN.27 is unchanged; the RUST and FTN rationales say "the reach that STND.CODE 1.2 gives the term"; RUST.14 is kept as ratified; FTN.18 notes that it adds no other outcome; the naming Notes use the form "retrieved no convention ... unverified"; the SV Purpose reads "execution setting". |
| P4 | cold with pairs, dispositions | 0.2 | Yes. The rationale puts the floor argument and the DRAFT.42 reading to the custodian; the row Signature carries the ledger-form case; the Notes say "derives no configuration that relies on that authorization"; row 1.3 ends "Transition (GOV.42): none."; units 0010 and 0012 exist in `harness/records/units/`. |
| P5 | cold, dispositions | final | Yes for the 14 documents: the garble in the four HW rationales, the DFLT gloss, and the CLASS and KNOW wording are fixed in the scripts and in the corpus. BUILD: B1. No pair review is recorded, and none applies (S5). |

## Rationales

All accurate against their documents and records. Entries 148 to 150 describe their provisions correctly (modes, instantiated outcomes, counts: eight new CODE provisions, four binding; six CXX withdrawals; CXX.18 kept; STDC.2 retitled with its ID kept). The classes are right under STND.IDENT.3: the eleven editorial entries change no obligation, permission, or defined meaning (OFFLD.31 and LEAN.25 gain only a citation); the eight minor entries add provisions, alter a binding row (HARN.29), or alter a defined meaning (Untrusted input; CODE.6). The check scopes of HW.CPU, HW.EMBED, HW.GPU, and HW.QPU drop Article names from informative class-onset sentences; the cold review matched each against the `instantiates` fields.

## Withdrawals

STND.CXX lists 16, 17, 28, 29, 30, and 31 in `withdrawn`; the files are gone; no ID is reused (CXX.32, CXX.33, CODE.14 to .21, STDC.39, STDC.40 are new). The convention of STND.CLASS (front-matter field, deleted file, history row) is followed. The six IDs appear in no provision or Notes of the corpus, only in history rows. STDC.2 keeps its ID with a new title and a narrower body, and its history row says so.

## Should-fix

**S1. STND.BUILD Notes omit the binding C form.** They say the finite-value rule "STND.CXX.18 binds for C++" and "keeps it from such C++ code". STND.STDC.40 binds the same rule for C, and the same paragraph speaks of C. Fix: add "and STND.STDC.40 for C" in both places, add STND.STDC to References, and amend the rationale and row 1.0.2. Also the first sentence "STND.CODE.21 has code ... not compiled" states a default in the indicative; write "advises against".

**S2. Stale P5 reading copies.** `p5/STND.CLASS.md` and `p5/STND.KNOW.md` lack the accepted Optional 1 and 3 ("The table holds no part of Simplicity (SIMPL)."; "the tag vocabulary of that corpus (TAG)"). The corpus is right. Fix: recompose both.

**S3. Order of entries.** Entry 150 (CXX) states in its Notes that the Julia standard "holds in a default of its own the bounds checking of the production configuration", which is true only from entry 167 (JL.36). Entries 150 to 167 also leave RUST, FTN, and LEAN citing the withdrawn CXX.16 and CXX.17 until entries 168 to 171. The end state is clean and no check runs between entries. Fix: accept, and say so in the ratification note; or move RUST, FTN, and LEAN directly after CODE.

**S4. One sibling item, two resolutions.** P1 decision 9 closes "STND.CXX.27 against STND.JL.34" as no change; P2 decision 3 closes it with the new JL.36. The CXX rationale ("a reasoned no change") reads as if no Julia amendment exists. Fix: state it once: CXX.27 unchanged, JL.36 added as its counterpart (decision 11 of the list).

**S5. P5 record.** Say in `p5/dispositions.md` that no pair review applies, since no provision changes, and add BUILD.

**S6. Rationale 175 and its history row** do not mention that the row Signature now names "the transaction of the row Record" in place of "that transaction". Add a clause, or leave: it changes no obligation.

## Definition of done, items 1 to 5

1. Holds, once the custodian records the "no change" decisions (`decisions-draft.md`, items 8, 12, 13, and 19). Every OPEN-ITEMS corpus item is amended or reasoned: R17, Untrusted input, R18, the seven sibling items, OFFLD.31, MPI and OMP, References. The HARN.30 reading goes to the custodian.
2. Holds. Classes and tails are right. Floor arguments stand in the Notes for CODE.6, .14, .15, .16, .18, STDC.2, STDC.40, CXX.32, PY.32, HARN.30, and the widened reach in RUST.15, FTN.31, PY.25, JL.13. No C++ ruling is extended without its own argument.
3. Holds except B1.
4. Holds when this report and reviewers A and B are fixed and verified.
5. Holds, with the scoped checker (decision 22).
