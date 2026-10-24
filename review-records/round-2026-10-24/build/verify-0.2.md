# Verification of STND.BUILD draft 0.2 (with 1.0.1)

**Verdict: PASS, with four should-fix items. No defect, no blocking item.** Every disposition is carried out. The four items can be fixed in the coalesce by wording alone, none changes an obligation.

## Checks run
- I ran `rehearse_build_wflow_101.py` (entries 117 to 121) on a fresh copy. `verify`: all eight checks PASS (1213 entries). `findings.py 'STND\.BUILD'`: no finding. For `'STND\.WFLOW'` the only finding is the g.18 notice already on STND.WFLOW.7.
- The reading copy composed from my rehearsal is identical to `draft-0.2-with-1.0.1.md`. The provision files of the 1.0 rehearsal and the 1.0.1 rehearsal are identical; 1.0.1 changes only `_doc.md` and the manifest. STND.BUILD 1.0 alone also verifies.
- `govharness pairs` on the rehearsed copy equals `pairs-0.2.md` byte for byte (284).

## Findings to status
| Finding | Status in 0.2 |
| --- | --- |
| Cold D1 (BUILD.3 and the record row) | Carried out. The row now covers any kind of build, with kinds and extent. |
| Cold SF1 (BUILD.12 S2) | Carried out (SIMPL.6, CSQ3, operable, no "by default"). |
| Cold SF2 a, b, c | Carried out. BUILD.21 at CSQ2 on REPRO.10; D1 and D2 argued in the onset paragraph (see part 4). The QA.9 clause is present. |
| Cold SF3 (WFLOW) | Carried out. Rule in words in 1.0, cited in 1.0.1; consistent with WFLOW 0.2 Purpose and Notes. |
| Cold SF4 (CXX.4, .25) | Carried out in Purpose and Notes. |
| Cold SF5 (Reporting build) | Carried out. The term is defined and used in Checking build, BUILD.13, BUILD.25. |
| Cold SF6 (narration) | Carried out. No narration found in the Notes. |
| Cold SF7 a, b, c | Carried out (BUILD.2, .9, .21, Terms, Notes). |
| Cold SF8 (HW.7, isolation, REPRO.2) | Carried out. |
| Cold Optional (toolchain matrix) | Taken. The "where there is one" argument is sound. |
| Pairs C1 (BUILD.5, .20) | Carried out, with REPRO.3 in Instantiates. |
| Pairs C2 (BUILD.14 to 18) | Carried out, one obligation with an alternative each. |
| Pairs C3 (PRIME.10) | Carried out for the Environment row and BUILD.23, but see new finding 1. |
| Pairs C4 (cache disposal) | Carried out in the provision; the Notes need a qualifier (new finding 3). |
| Pairs Obs 1, 2, 3, 6, 10, 12 | Carried out. Cites to VVUQ.82 and .83 now match their text. |
| Pairs Obs 4, 5, 8, 9, 13 to 17, 19 | Carried out in the Notes (NUMER.11, RSRC.12, JL.5 and the others exist). |
| Pairs Obs 11 (BUILD.26 S2, range interior) | Answered in the Notes only (see optional 4). |
| Pairs Obs 7, 18, 20 | Out of scope, as the dispositions say. |

## Fresh reading (task 2)
No new conflict with STND.WFLOW 0.2 (WFLOW.1, .2, .6, .35, .36, .37 and the build paragraph are consistent), STND.CXX (CXX.4 and .25 are narrower, CXX.26 and .27 fit the Reporting build term), or STND.DEPS (DEPS.6 untouched, BUILD.7 adds timing only). No floor raised; all 26 are defaults; BUILD.20 correctly stays a default. VVUQ.82 and .83 and REPRO.3: BUILD.14 to 18 admit a declared difference, so an agent has no duty to remove one. GUARD.5 and PRIME.6: BUILD.24 keeps the cache. The b1 figures I spot-checked (1.2 million, 21 cases, 1,086, five examples, twofold) match the note. No product, tool, or version name in a provision.

## 1.0.1 amendment (task 3)
Editorial under GOV.41 is right: only the informative Purpose and Notes change, plus the References row and history row; no provision file differs. The text is accurate: WFLOW lists the same five activities, its title matches the References row, and WFLOW.6 and BUILD.23 each call the other the build form. Order is clean: BUILD 1.0, then WFLOW (which cites an existing STND.BUILD), then 1.0.1; and BUILD 1.0 stands alone. One defect in the placeholder rationale (new finding 2).

## Class-onset paragraph (task 4)
Sentences 1, 2 (rows), BUILD.21 (REPRO.10, CSQ2), BUILD.25 S2 (REPRO.4, CSQ2), BUILD.26 S2 (INTPR.10, CSQ2), the comparisons clause, BUILD.12 S2, BUILD.11 (HW.5, CSQ3), and the "every other" sentence are right against the table of STND.CLASS.10; I found no further row that reaches a BUILD sentence. The last sentence is inaccurate (finding 4).
- **Departure D1 (BUILD.24 S2 at CSQ3 on QA.13): agree.** QA.13 is not in the table, and the sentence asks to rebuild what a found fault reaches, with no tracking mechanism.
- **Departure D2 (BUILD.10 at CSQ3 on SIMPL.6): agree.** It declares compile targets and states no hardware behavior, which is the DSGN.5 row.

## New findings, ranked
**Should-fix**
1. **BUILD.25 Configuration row has the PRIME.10 exposure of the Environment row.** "Each option that the build was given" can hold a token passed on a command line. Fix: add "other than an option that holds a secret, which the record names without its value (PRIME.10)", or state it once above the table.
2. **The 1.0.1 rationale says "ratified by the custodian on 2026-10-24".** The custodian has not ruled; the WFLOW round says "proposed for ratification". Change both `RATIONALE` and the first words of the entry accordingly in `apply_build_1_0_1.py` (the precedent 1.1.1 does not excuse it).
3. **Notes on BUILD.24: disposal "is an irrecoverable action under GUARD.5, reserved to the human owner (PRIME.6)".** A build cache is content regenerable from recorded inputs, an exempt class of STND.DFLT.15, which WFLOW 0.2 Notes apply to partial outputs. Fix: "unless an exempt class of STND.DFLT.15 applies, and in every case after an archive of it".
4. **Last sentence of the onset paragraph overclaims**: "each asks for a declaration, a statement in the repository configuration, a comparison of builds, or an item of a record". BUILD.4, .6, .7, .13 to .18, .21, .22, .24 ask for something else. Fix: "each is a default that asks only what REPRO, DSGN, RSRC, or QA already ask, at the cost of wording, a setting, or one record" and keep the three already-binding cites.

**Optional**
1. BUILD.13 S2 (limit of a verification) is placed on no row while BUILD.26 S2 (limit of coverage) rests on INTPR.10 at CSQ2. Add one clause saying the basis (VV.1) decides.
2. BUILD.23 S2 forbids serving only; add "or storing", since a store shared between hosts also discloses a keyed digest.
3. Notes on BUILD.12: "The same rule as the default of a release archive fails the build of each party..." is hard to parse, and says the sentence "has the build description declare", which its text does not say. Rewrite both.
4. The BUILD.26 range exception ("stated once, as checked at its ends") exists only in the Notes; the sentence read literally asks the interior to be stated unchecked. One clause in the provision, "or a range whose ends are so built", would remove it.
5. Dispositions cite "STND.FTN.4", which is not in the corpus (a Fortran draft is only at 0.1). Do not carry the cite into any record.
6. `pairs-0.2.md` has no STND.WFLOW pairs by method; the WFLOW round must hold them. Placeholder times in entries 117 to 121 are not monotone (20:05 then 20:00); the lead sets them.

## Not checked
The sources of b1 beyond the figures above; the Fortran, Rust, and C drafts (none cites BUILD); the WFLOW draft outside the provisions and Notes named above.
