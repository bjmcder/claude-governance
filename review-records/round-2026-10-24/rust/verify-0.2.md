# Verification of STND.RUST draft 0.2

**Verdict: REVISE (small). One Defect: STND.RUST.13 sentence 2 still raises the floor in part. Eight Should-fix items, all wording or Notes.** Cold D2 is carried out only in part, and one pair-review disposition (Observation 4) is claimed and absent.

## Checks run
- Rehearsal copy (BUILD round, then Rust): `verify` passes all eight checks. `findings.py 'STND\.RUST'`: ten g.18 notices (.1, .3, .7, .11, .13, .16, .21, .23, .24, .29), the ten the onset paragraph lists; no defect.
- The composed reading copy equals `draft-0.2.md`; `govharness pairs` equals `pairs-0.2.md` (267). Every STND.BUILD cite and imported Term checks.

## Finding to status
| Finding | Status |
| --- | --- |
| Cold D1 | Carried out (but new 6) |
| Cold D2 | Partly; new 1 |
| Cold D3 | Provision carried out; Floor paragraph overclaims (new 2) |
| Cold SF4 to 9, 11 | Carried out (SF6 as decided; wording new 6) |
| Cold SF10 | Carried out except "the second clause by inference" (new 7) |
| Cold SF12, bundles, Terms, BUILD overlap | Carried out; two bundles weak (new 8) |
| Pairs D1, SF1 to SF8 | Carried out |
| Pairs Optional 1 to 11, Section C, Obs 3, 7 | Carried out (Optional 12 left to the lead) |
| Pairs Observation 4 | **Not carried out.** The dispositions claim a Notes sentence; none exists |

## New findings, ranked
**Defect**
1. **.13 S2 asks more than PY.22 or PRIME.4.** A hook runs at every panic, before any catch. The sentence makes it deliver a diagnosis of each panic that "answers a listed condition", including one that .24 catches and converts to a returned error, or .10 answers at a boundary. PRIME.4 needs a diagnosis of a halt or a degradation, and a returned error carries its own. This is cold D2 case (b), unfixed. Fix: "... of each such panic that no other response of this provision answers".

**Should-fix**
2. **"as STND.CXX.29 does" (Floor, .33).** CXX.29 reaches only high-assurance code, and its Notes record a custodian ruling for that reach. .33 reaches every claim of freedom from undefined behavior in any report, record, or review, with no ruling. Delete the parity clause and carry the question to the custodian in the delivery message, together with .6: an argument at a block is reasoning, where PY.4 costs an annotation. Or limit .33 to claims offered as evidence of a result or release.
3. **Obs 4 sentence missing.** Add one Arithmetic sentence (overflow in trusted arithmetic that computes a command is a defect under PRIME.4 and DSGN.2; CPS.5 does not catch a wrapped value inside its limit), or correct the dispositions.
4. **.15 S1 is garbled**: "a condition that an execution setting decides among them". Fix: "in a form that an execution setting removes: `debug_assert!` and its variants, and code compiled only under a condition that such a setting decides".
5. **Duties in the indicative in the Notes.** "the reviewer and the human owner check unsafe code that an agent writes" is a duty, and a check by the human owner that LVL0 does not assign (STND.DRAFT.42). "a detector with seeded choices records its seed" restates CODE.9 as a duty. Delete the first; write the second as "CODE.9 covers its seed".
6. **Attributed ruling.** "the custodian ruled on 2026-10-23 that this reach raises no floor for STND.PY and STND.JL" is accurate (PY.25 and JL Notes) but contradicts the lead's rule against attributed rulings. Write "STND.PY and STND.JL give the same reach" and carry the Rust question in the delivery message.
7. **"(rs1, section 10, S32; the second clause by inference)"** leaves an unsupported clause marked in the text. No provision needs it; delete it.
8. **Bundle sentence.** .3 (blocks and impls; block in an unsafe function; documentation) and .16 (`Result`; panics section; `unwrap` reason) hold three rules that a project could apply apart. .13 does too (PY.22 is its precedent). Split .16 (34 provisions, inside the lead's range) and fold .3 S2 into S1, or change "one rule for one construct" to what is true.
9. **Onset.** .22 S2 (DSGN.3) is missing from the DSGN.3 sentence. "the row of CSQ2, and apply from CSQ3" for the tests of .1, .8, .28 reads as a contradiction; say they rest on no row.

**Optional.** Notes run 4,101 words against 2,500 to 3,300 in sister standards (trim Numerics, Concurrency). The Xu study was of 186 reports, not "all" vulnerabilities. .2 partly repeats BUILD.11.

## Fresh reading
- **Binding provisions.** .14 equals CXX.17. .15 equals CODE.6 plus CXX.18; its overflow sentence follows from CODE.6. .13 S1 and S3 equal PY.22; S2 is item 1. .6 has the shape of PY.4 (cost: item 2). .33: item 2.
- **No restatement and no new conflict** found against CODE, CONC, DEPS, BUILD (.1 with BUILD.26, .19 with BUILD.13, .29 with BUILD.1 and .7), CXX, PY, JL.
- **Onset paragraph** against STND.CLASS.10: correct for INTPR.8 (.10 S2, CSQ1), DSGN.4 (.23), DSGN.5 (.24, .25), INTPR.10 (.32), DSGN.15 (.12, .20, .22), the DSGN.2 retention parts, and the no-row list (each member's bases checked). Ten bundles: .1, .7, .11, .21, .23, .24, .29 hold; .3, .13, .16 see item 8.
- **rs1 unverified facts.** No provision rests on one; edition facts are hedged; study figures match rs1.

## Pairs against 0.1
No pair is new. 15 are gone: 12 with deleted 0.1 .29, and 3 (.23 with CPS.5, CPS.9, ML.6) because .23 no longer instantiates DSGN.2.

## Not checked
rs1 beyond the cited sections; the 267 row judgments (carried from the 0.1 pair review); the BUILD draft beyond the cited provisions.
