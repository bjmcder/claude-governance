# Verification of STND.LEAN draft 0.2 (2026-10-24)

**Verdict: approve for the custodian with fixes; no blocking item.** Every finding of the two reviews of 0.1 is carried out as dispositioned, with one residual ambiguity in LEAN.5 (S1 below). No new conflict, no floor raised beyond what the custodian decides, no restatement found beyond the LEAN.25 point (S2).

## Scripted
- Rehearsed copy `/tmp/rehearsal-xujs1cj_/governance` (still present): `govharness verify` passes all eight checks; `findings.py 'STND\.LEAN'` gives one g.18 notice (LEAN.21, argued in the Notes).
- All 31 provision files: every body line is in `draft-0.2.md`; each default instantiates only VV, REPRO, INTPR, DSGN, or SIMPL; LEAN.5 and LEAN.25 are binding (PRIME.2, PRIME.4); one modal per sentence; none of the STND.DRAFT.7 or .17 words; titles at most six words; every cited identifier is in References; no csimp, no "unnecessary", no "rather than"; "panic" is in no provision.
- `govharness pairs` regenerated: identical to `pairs-0.2.md`, 1,046 pairs.

## Findings to status

| Finding (0.1) | Status in 0.2 |
| --- | --- |
| Cold D1 / pairs D1, C1 (LEAN.5) | Carried out; residual S1 |
| Cold D2 / pairs SF1, C2 (LEAN.7 vs .14) | Carried out |
| Cold D3 (LEAN.21 conditions) | Carried out |
| Cold D4 (References) | Carried out (CXX, PY, NUMER, HW present) |
| Cold SF1 (recalled facts) | Carried out in provisions; Notes residual S3 |
| Cold SF2 (CSQ0 reading) | Carried out; goes to custodian as decision 5 |
| Cold SF3 / pairs SF1 tail (logical axioms) | Carried out; Optional O6 |
| Cold SF4 (LEAN.22) | Carried out |
| Cold SF5 (untrusted author) | Carried out |
| Cold SF6 (LEAN.1 bundle) | Carried out; g.18 notice gone |
| Cold SF7 (LEAN.9 s2) | Carried out |
| Cold SF8 (onsets) | Carried out; residuals O1 to O3 |
| Cold SF9 (Terms) | Carried out |
| Cold SF10 (Notes indicative, length) | Indicative recast done; length not trimmed (S4) |
| Cold Opt 1 to 4 | Done, moot, or declined with reason (accepted) |
| Pairs SF2 (Statement review row) | Carried out |
| Pairs SF3 / Obs 3 (LEAN.25) | Carried out; S2 |
| Pairs SF4 (Terms) | Carried out |
| Pairs SF5 (LEAN.27) | Carried out; wording equals STND.PY.1 |
| Pairs Opt 1 | Declined, reason sound |
| Pairs Opt 2 to 7 | Carried out (LEAN.22 s2, onsets, CSQ0 note, LEAN.31, LEAN.4 rows, LEAN.8 s2, LEAN.9 s2) |
| Pairs Obs 7, 8, 10 | Not addressed (observations only); see O5 |

## New findings, ranked

No Defect.

**Should-fix**
- **S1. LEAN.5 s2, "of the work".** Undefined. A Lean package is "imported by the work" (LEAN.1) and "a dependency of the work" (Terms), so it is unclear whether its declarations are "of the work". The Notes say a work importing precompiled libraries reports "proved" on a check of its own declarations "with that coverage stated", but the sentence demands that statement only if declarations of the work went uncovered. Fix: "...of each declaration on which the theorem depends other than those of the toolchain" (or define "declaration of the work" as including those of its Lean packages) and let the Notes say what must be stated. The floor argument stands either way: the sentence still forbids only an unqualified "proved" on a partial check, which PRIME.2 and AGENT.4 forbid.
- **S2. LEAN.25 against GOV.31.** It is now the PRIME.4 response list with two added forms, with no Lean-specific content (the panic content was dropped for the unverified facts). The siblings (STND.CXX.16, STND.PY.22, STND.JL.15) name a language construct; this one names none. Tests: floor, no raise (same list as the siblings, and `return` and `throw` are the forms they admit). Counterparts: no conflict. Pair #759 (HW.8) holds: a hardware fault falls to halt, degrade, or safe state, and LEAN.25 permits those. Fix: name the language constructs, or state in decision 3 that GOV.31 is argued by the sibling precedent.
- **S3. Notes, "Arithmetic and programs".** (a) "as the manual describes it and l1 does not" is inconsistent with l1 line 51 and S5, which report a panic that continues with a default value (what l1 lacks is the printed message). (b) "indexing by the form that panics ... the forms that return an optional value or take a proof of the bound" appears nowhere in l1 and is not marked `[unverified]`, against the Notes' own claim that every unsupported fact is marked. No provision rests on either. Fix: mark or delete.
- **S4. Notes length.** The Notes (to the end of Class onset) grew from 4,239 to 4,940 words by my count. The disposition says "not shortened materially"; cold SF10 asked for a trim. The added decisions and onsets are needed; the l1 restatements in "Evaluation and checkers" and "Definitions" are the candidates.

**Optional**
- **O1.** LEAN.24 onset: s1 asks that an operation "gives the value that the result needs", which reads as a check of results (the CSQ1 postcondition row of DSGN.2) as much as of preconditions; the paragraph calls it a precondition check. Its s2 is described as avoiding a response "that hides a failure", but the text also bars a visible substituting response. Reword the onset sentence. "Documented response to a failure" is loose for a caller-supplied default (`getD`); say "that the function chooses".
- **O2.** The LEAN.4 row "Code that runs" asks the memory and ordering model for concurrent code at CSQ3. DSGN.15 starts at CSQ2 and the STND.CONC.28 proof at CSQ0; the onset paragraph is silent. State that the row records an assumption (VV.1).
- **O3.** The onset of LEAN.14 s2 is asserted without reason; its "evidence not resting on the compiler" resembles the reference-oracle row (CSQ2).
- **O4.** The last onset sentence says "no provision raises the floor" as fact while LEAN.5 and LEAN.25 await the custodian; write "the Notes argue that".
- **O5.** The Notes say "the argument that the custodian accepted for STND.JL.15": adoption is on the ledger; "accepted the argument" is an inference, so write "adopted". "AGENT and GOV.51 trust no agent by its role": GOV.51 treats tool software as an agent and says nothing about role; cite it for that only. The AGENT.47 paraphrase (pairs Obs 8) is unchanged: say "as departures".
- **O6.** Decision 4 should say that VV.1 "shown to be met" is read as "stated as assumed" for checker soundness, not only for axioms. LEAN.16 plus the strict Term cannot be met by any checker known to l1, so every CSQ0 Lean project replaces it; the lead has decided this (L3), so it is listed for the custodian only.

## Tasks 3, 4, 5
- **Pairs 0.2 against 0.1.** 1,046 both; four rows differ. #668 (LEAN.22 with ML.5) gains basis VV.4. #758 to #760 (LEAN.25) change basis DSGN.2 to PRIME.4, so CPS.5, CPS.9, and ML.6 leave and HDES.14, HW.8, and HW.GPU.3 enter. All three new pairs are compatible (HDES.14 makes saturation visible; HW.GPU.3 handles accelerator status). The removed CPS and ML pairs also say "the response PRIME.4 requires", which LEAN.25 does not contradict.
- **Class onset, sentence by sentence.** Correct against STND.CLASS.10 for the first through the LEAN.27 to .31 sentences, subject to O1 to O4. All 31 provisions are placed. Placing LEAN.19 at CSQ3 with assemblies left to the VV.6 CSQ1 row is correct.
- **Unverified facts.** No provision rests on wrap, panic behavior, the abort setting, csimp, fetched-product contents, library naming, issue-tracker history, or upgrade cost. LEAN.11 row 3 and LEAN.24 s1 hold either way; LEAN.24 s2 names a documented response; LEAN.15 s2 covers fetched products whatever they are. The "total definition" and "independent checker" Terms rest on l1 S4, S5, S18, which support them.

## Not checked
No Lean run. Sources S1 to S29 not refetched; l1 was grepped, not reread in full. The pairs of 0.2 were not re-reviewed one by one beyond the changed rows.
