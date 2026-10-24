# Verification of STND.STDC draft 0.2

**Verdict: Revise (minor).** 0.2 carries out nearly every disposition and passes the machine checks. Two defects block adoption: the text of STDC.28, and a misstatement of STND.CODE.11 in the Notes.

## Checks run
- Stored rehearsal (`.scratch/c-draft/rehearsed`): `verify` passes 8 of 8; `findings.py 'STND\.STDC'` prints nothing. The g.18 warning is on the live corpus too. The BUILD scripts changed after that copy, so I re-ran `rehearse_02.py`: same result, STND/STDC byte-identical.
- All 38 bodies appear verbatim in `draft-0.2.md`. The regenerated pair list equals `pairs-0.2.md` (352, each once).

## Findings of the reviews
| Finding | Status |
| --- | --- |
| Cold D1 stream order, facts | Done; facts marked; finding 1 |
| Cold D2 PRIME.4 list; D3 Foreign interface | Done |
| Cold SF1 mechanism | Done; each cell equals the CXX 1.1 Notes except CXX.31 (O1) |
| Cold SF2 rows, instantiates | Done; REPRO.9 left over |
| Cold SF3, SF5 to SF7 | Done |
| Cold SF4 STDC.3, STDC.2 | Done (default; decision 2); finding 5 |
| Cold SF8 DSGN.2 onset | Partial; finding 3 |
| Cold SF9 build overlap | Partial: BUILD.13 cited; the CXX.4 and CXX.25 rows still repeat BUILD.11 and .12 |
| Cold SF10 proportion | Not carried: 38 provisions, 8,771 words against 8,389 |
| Cold SF11 Notes | Done; "offers" and "serves" remain |
| Pairs D1 shift | Done; finding 6 |
| Pairs D2 CXX.4 row | Done |
| Pairs SF1, SF4 to SF10 | Done |
| Pairs SF2, SF3 onsets | Partial; finding 3 |
| Pairs SF11 order | Done; entry numbers and times left to the lead |
| Pairs Optional 1 to 13 | Taken or moot as stated, except 10 (finding 2) |

## Tests
- **Binding.** A C reading of a binding CXX provision is not binding on the CXX rulings, which name CXX.3, .16, .17, .18, .29 for C++. GOV.19 admits the mark through PRIME.4 and PRIME.2, but the floor claim (GOV.11) needs the custodian. Decision 2 carries that, with two gaps (finding 5). STDC.28 exceeds the brief's cost; decision 3 carries it.
- **Rows.** The 13 rows of STDC.1 and 4 of STDC.2 read cleanly against CXX 1.1. No new conflict with CODE.4, .7, .12, CONC, or BUILD (finding 8). STND.PY and STND.JL were not re-read.
- **Pairs against 0.1** (by 0.2 numbers). Ten new: STDC.2 with CPS.5, CPS.9, ML.6; STDC.3 with AGENT.22, NUMER.3, .5, .16; STDC.29 with AGENT.22, NUMER.3, .16. One basis added (STDC.29, NUMER.5). Nine dropped (STDC.11, .13, .18 with CPS.5, CPS.9, ML.6). By hand: no conflict, none unowned.
- **Unverified facts.** The text of STDC.28 can be met whatever the stream facts are; its floor argument cannot, and decision 3 should say so. S24 is not cited.

## New findings, ranked
**Defect**
1. **STDC.28 (binding).** (a) For a stream never closed or only flushed, "before it closes the stream" is empty. (b) It asks a test and no response, so a tested and ignored failure is the silent continuation it claims to prevent. Fix: test the result of the flush or close, and the indicator before the close or after the flush, and respond as the C reading of CXX.16 provides or give the CODE.12 reason; otherwise make it a default.
2. **Notes** say CODE.11 covers "a block under a condition that is always false". It covers code disabled by conversion to a comment. Cite STDC.25 and say such a block is disabled code in the sense of CODE.11.

**Should-fix**
3. **Onsets.** STDC.27 bounds every automatic array, not only sizes from untrusted input, so by the paragraph's own reading its onset is not CSQ3; limit it to such sizes (c1 practice 18). The STDC.37 clause "second sentence has effect from CSQ2" contradicts "applies from CSQ3"; delete it. STDC.29's second sentence has no sentence onset (it rests on CODE.4, CSQ3).
4. **STDC.1** instantiates REPRO.9, which no row serves (STND.DRAFT.19). Remove it; the HDES.3 pair loses that basis.
5. **Floor Notes.** The cost "one attribute per function" for CXX.17 holds only where the toolchain has one; the errno clause of the CXX.16 row is new text. Name both in decision 2.
6. **STDC.12** applies the unsigned-or-nonnegative test to every shift. A right shift of a negative value is implementation-defined, and c1 practice 8 concerns left shifts. Say "left shift".
7. **STDC.30** excludes every stream, yet STDC.28 covers only streams whose writes go untested. A stream with each write tested and an untested close falls between them. Say "other than a stream that STND.STDC.28 governs".
8. **STDC.16** asks for "a checking build" without the option; the BUILD term means a build with run-time checks. Say "a build named apart as STND.BUILD.13 provides".
9. **Not in c1.** The CXX.24 row's "an assumption attribute" (c1 lists no such C attribute; the change from 0.1 is unreported). "Nonzero width" in STDC.35 (c1: "adjacent bit-fields"). "No library function sets errno to zero" (c1: not required to). Mark each unverified or drop it.

**Optional**
- O1. The CXX.31 cell is not a class; the body reads "the class that its row gives".
- O2. Notes say CODE.6 requires the check of an index from untrusted input; DSGN.2 and STDC.21 do.

## Not checked
The ISO text; c1 sources.
