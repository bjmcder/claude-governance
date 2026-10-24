# Reconciliation review C (records and integrity), round of 2026-10-24

Reviewer C. Scratch: /tmp/recC. I changed no file but this report and the decisions list.

## What I ran

- Full rehearsal from harness/ (`rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24.py`): 23 entries, 117 to 139, in the order the brief names, clock 22:00 to 22:22. Rehearsed copy: /tmp/rehearsal-knjnjxt1/governance. The live corpus was left unchanged ("source unchanged").
- `verify` on that copy: all eight checks PASS; one warning, g.18, carried by the live corpus.
- `findings.py` on OMP, CXX, PY, JL, NUMER, BUILD, WFLOW, STDC, RUST, FTN, SV, LEAN, CONC, PROJ, HARN, MNEM: 52 findings, none of class defect. One g.6 (HARN.28) and one g.11 (CXX.3) are old; 50 are g.18 notices. New standards: RUST .1 .7 .11 .13 .22 .24 .25 .30, LEAN.21, SV.5 and .18, WFLOW.7, each argued as a bundle in its onset paragraph. BUILD, STDC, FTN: none.
- Harness suite: 186 tests, OK, 227 s. (HANDOFF.md still says 129.)
- `pairs` regenerated for the seven new standards equals each `pairs-0.3.md` byte for byte (BUILD 284, WFLOW 457, STDC 349, RUST 267, FTN 174, SV 941, LEAN 1,046 pairs, as the lists count them).
- Scripts: rationale tails, entries cited, mnemonic letter distance, provision modes and counts, References by name, Terms defined twice.

## Blocking

**B1. References incomplete (R11, STND.DRAFT.34).** `verify` passes because it reads body identifiers only. By script, each document below names a document in its Purpose, Terms, or Notes that its References table lacks:

| Document | Names, not listed |
| --- | --- |
| STND.STDC | STND.PY, STND.JL (Purpose: "in the form of") |
| STND.WFLOW | STND.OFFLD (Purpose), AGENT (Notes on STND.WPROC) |
| STND.LEAN | STND.CODE (Purpose, Terms) |
| STND.RUST, STND.FTN, STND.SV | STND.DOCS |
| STND.BUILD | HDES (Notes, the design record of a realization) |

Fix: add the rows to `content_*.py` (or move the sentence into a citation already listed). STND.CXX also names HDES and STND.HARN names STND.IDENT; both are old text, Should-fix. R11 is therefore not closed.

No other blocking item. Rationales, class of each amendment, register rows, and the harness are sound (below).

## Should-fix

1. **Dispositions claim a fix the script lacks.** build/dispositions.md (draft 0.3, SF2) says `apply_build_1_0_1.py` now reads "proposed for ratification". Entry 126 reads "ratified by the custodian on 2026-10-24", like all 23. The convention holds only if the round is applied after ratification (START in the round script says so). Either correct the disposition, or set the wording once for all entries.
2. **Rationale of entry 139 (HARN 1.2)** says the floor argument is "a ruling the custodian makes with this amendment". It is a decision (D3 of the list). Say "the custodian decides the floor argument on ratification".
3. **Rationale of entry 128 (STDC)** points to "decision 2 of the dispositions", a file the ledger does not hold. State the decision in the entry or drop the pointer.
4. **Notes with pending decisions.** SV (three sentences "a decision for the custodian"), LEAN (three), and FTN (STND.FTN.31 "depends on the custodian's decision") keep decisions in adopted Notes. Once ratified they go stale and read as process narration (STND.DOCS). Reword to the argument alone.
5. **Verification of the 0.3 drafts.** Each new standard has a verify-0.2.md only. STDC (two defects) and RUST (one defect) were closed in 0.3 by the lead's check. I confirmed the closures in the rehearsed text: STDC.28 now a default that tests the result and the indicator, STDC Notes on CODE.11 corrected, STDC.12 "left shift", STDC.27 limited to untrusted sizes; RUST.13 S2 limited to a panic no other response answers, and the overflow sentence (Obs 4) present in the Notes. The amendments folder has no verification file; harn-auth has no dispositions.md (its dispositions are in unit 0008).
6. **Unit 0008 record contradicts itself.** `harness/records/units/0008-remote-write-authorizations.md`: "Definition of done" 3 and the "Done" list say the ask rule `Bash(git push *)` is dropped and name `AUTHORIZED_RULES`; code and decision 0002 (last adjustments table) keep the rule and `AUTHORIZED_RULES` is gone. "Review: none yet" is stale (security review, cold and pair review, two verifications). The later sections say they supersede; edit the first part to say what the code does. README and decisions 0001 and 0002 agree with the code (option names, kept ask rules, plain-words rule, git metadata in `denyWrite`, clock admitted to hooks).
7. **Ruff.** The unit says guard.py gains one TRY004. Ruff at 79 columns reports 7 on guard.py (four TRY004, SIM114, SIM102, B023); the new files and tests are clean. I have no baseline to count the old ones.
8. **g.18 note on STND.WFLOW.7** and the bundles above stay as argued; no action.

## Checks that pass

- **Rationales.** All 23 end with the fixed tail (R24 closed by script). Entries cited are 15, 53, 112, 114, 116, none of this round. Counts match the documents: BUILD 26, WFLOW 40, STDC 38 (STDC.2 binding), RUST 34 (6, 13, 14, 15, 34 binding), FTN 36 (29, 30, 31), SV 27, LEAN 31 (5, 25). Provision ranges named in the STDC and RUST rationales match the titles. CONC 1.0.1 cites provisions that exist; I checked titles of WFLOW.32, WFLOW.6 and BUILD.23, OMP.7, RUST.21, .33, STDC.38, LEAN.19, SV.23.
- **Class under STND.IDENT (revision section).** Editorial: OMP 1.0.1, PY 1.0.1, BUILD 1.0.1, CONC 1.0.1 (diff against the live corpus: only `_doc.md` and manifest). Minor: CXX 1.1 (CXX.15, CXX.23 text), JL 1.1 (JL.27 text, instantiates), NUMER 1.3 (NUMER.2 table, refers_to), PROJ 1.2 (PROJ.6, .7), HARN 1.2 (HARN.29). Each is right and each rationale gives the reason.
- **Register.** BUILD, WFLOW, STDC, RUST, FTN, SV, LEAN follow OFFLD in the order of adoption; the register is in adoption order. Letter distance: 3 for all but SV (2, from PY, allowed by IDENT.17).
- **Records complete.** Reviews, verifications, and dispositions exist for build, wflow, c, rust, fortran, hdl, lean, with pair lists. No blocking finding in any review stays open: the BUILD cold D1 and pair C items, WFLOW D1 to D3, STDC D1 and D2, RUST D1 and D2, FTN D1 to D3, SV D1 to D3, LEAN D1 to D4 are carried out in the rehearsed text, per the dispositions and my spot checks. harn-auth: High findings H1 to H3 closed per verify-security.md; its Mediums M-a closed (git metadata denied), M-b and M-c remain (decision 17).
- **Harness.** HARN.29 rows (status, grantor, extension, record, signature, dates at derivation and write, standing, form) match `authorizations.py` and the README; PROJ.6 and .7 match the template field.

## Queue R1 to R24

| # | State |
| --- | --- |
| R1 | Closed: entry 137, cites exist |
| R2 | Closed: rule in both Purposes and Notes |
| R3 | Closed: BUILD Notes name CXX.4 and .25 as C++ forms (lead decision 2) |
| R4, R5 | Closed: BUILD.2, .9, .21 and term Reporting build |
| R6, R16, R18, R22, R23 | A and B compare; decisions 5, 6, 7, 9, 10 below |
| R7, R20 | Closed: JL 1.1 (entry 120) |
| R8 | B checks; departures are decision 2 |
| R9 | Closed in SV: carve-out gone (grep) |
| R10, R12, R13, R15 | A and B; decision 4 for the reach of Untrusted input |
| R11 | **Open: B1** |
| R14 | Not closed by a script: decision 11 |
| R17 | Decision 8 (later round) |
| R19 | Decision 12; VVUQ.63 still names a battery |
| R21 | Closed: STDC rehearsed after CXX 1.1 |
| R24 | Closed by script |

## HANDOFF.md "Open items"

- HARN.18 remote write: closed in drafts (entries 138, 139) and unit 0008; remains until the installation tests pass (an allow outranking the kept ask rule; narrower `allowRead` over `denyRead`), a QA.8 review is recorded, and the configure entry records the install. Reason: the guard code is not yet installed.
- NUMER.2, STND.OMP: closed (entries 121, 117).
- Language standards: CXX closed (118); PY and JL closed in the Notes (119, 120); body citation of PY.17 and JL.24 left (decision 13).
- Next standards: all seven adopted by the round.
- Remaining: decisions list, rebuild of `rendered/`, bundle, `SHA256SUMS` after application; HANDOFF then archived first, not deleted.

## Not checked

The drafters' and reviewers' final messages are not on disk, so the decisions list rests on the files. The alignment, floor, and onset readings are for reviewers A and B. I did not run a second rehearsal of 0.3 per standard apart from the round.
