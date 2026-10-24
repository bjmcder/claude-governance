# Dispositions: STND.LEAN draft 0.1 to draft 0.2 (2026-10-24)

Reviews answered: `review-cold.md` (cold) and `review-pairs.md` (pairs, STND.HARN.28). Lead decisions L1 to L7 of 2026-10-24 applied. Draft 0.2: `draft-0.2.md`; pairs: `pairs-0.2.md` (1,046 pairs, the same count as 0.1). Rehearsal `/tmp/rehearsal-xujs1cj_/governance`: verify passes all eight checks; `findings.py` reports one g.18 notice (STND.LEAN.21, argued in the Notes). Module: `tools/amendment-scripts/content_lean.py`; draft 0.1 module kept at `.scratch/lean/content_lean_v01.py`.

## Defects

| Finding | Disposition |
| --- | --- |
| Cold D1, pairs D1 / C1: LEAN.5 S2 asks a build of everything; condition trails | Accepted (L1). S2 now reads: "Other than in a report that states which declarations its check did not cover, a report that a theorem is proved SHALL rest on a check, at the reported revision of the source, of each declaration of the work on which the theorem depends (PRIME.2)." "Checked", not "built"; "of the work"; condition first. Notes: "reported as proved" means without qualification; declarations of the toolchain and of fetched build products stay with STND.LEAN.15 and STND.DEPS.6; floor argument corrected (cost: wording and one sentence of the report; nothing beyond PRIME.2 and AGENT.4), sent to the custodian as a decision. |
| Cold D2, pairs SF1 / C2: LEAN.7 against LEAN.14 | Accepted (L2). LEAN.7 S1 adds "the axiom declarations of native evaluation that a record of STND.LEAN.14 covers". Notes: these are trust in the compiler, an assumption of the evidence stated in the record, not an Axiom under VV.9. |
| Cold D3: LEAN.21 S1 has two conditions | Accepted: "Before an untrusted author begins the proof of a relied-on theorem, its trusted statement and the accepted axiom list SHOULD be fixed, in files that the author does not change (VV.3)." S2: "The verdict on a proof that an untrusted author wrote ...". |
| Cold D4 (R11): References lack STND.CXX, STND.PY | Accepted. The Notes cite STND.CXX.14, STND.CXX.16, STND.PY.1, STND.PY.22, STND.JL.6, STND.JL.15 by provision; the derived References now carry STND.CXX, STND.PY, and NUMER. |

## Should-fix

| Finding | Disposition |
| --- | --- |
| Cold SF1: recalled facts inside normative text (wrapping, panic, csimp) | Accepted (L5). LEAN.11 row: "Arithmetic of fixed-width integers / ... or that the claim concerns the values that the type gives out of range" (holds whether or not the types wrap). LEAN.24 S1 holds either way; LEAN.24 S2 names a documented response ("lets the run continue with a value that the function substitutes for its result"), not the construct, so it holds whatever a panic does. "Panic" appears in no provision; panic behavior and the abort setting are in the Notes, marked unverified. The csimp sentence is removed. |
| Cold SF2: CSQ0 reading narrower than VV.1; no checker meets the Term | Accepted (L3). Notes "Proof at CSQ0" state the route as this standard's default and reading, "not a narrowing of VV.1"; a project that replaces STND.LEAN.16 records how its Lean proofs meet VV.1; no checker known to l1 meets the strict Term (the Lean-written second kernel is a port on the toolchain runtime), so replacement is the likely CSQ0 path. Strict Term listed as a custodian decision with the weaker alternative (separate source, any runtime, relation stated). Exhaustive checking outside Lean meets the row equally (pairs Opt 4). |
| Cold SF3, pairs SF1 (tail): logical axioms as assumptions of the evidence | Accepted (L3). Notes state it as this standard's reading, for the custodian, with the alternative of one standing owner declaration of the logic under VV.9. LEAN.4 Assumptions row now asks each assumption "with whether it is shown to hold or stated as assumed", and includes the soundness of each checker (pairs Opt 5b). |
| Cold SF4: LEAN.22 checks may be the author's; "unnecessary"; LEAN.13 | Accepted (L4). S1: the permission holds where the change alters neither the accepted axiom list nor the checks of LEAN.6, .10, .15 that the repository configuration set before the change, on a run on the reviewed revision that the reviewer makes or confirms. S2: the review includes LEAN.11 and the evidence of LEAN.13 (VV.4). Notes: "unnecessary" removed; the permission concerns correctness only; the review of other parts and the reading of LEAN.17, .24, .29, .30 stay under QA.7 (pairs Opt 2). |
| Cold SF5: Untrusted author head clause covers every author; definitions under verification open | Accepted (L4). Term: "A language model, a tool that searches for or generates proofs, or an actor whom the threat model of the project does not trust, as the author of Lean source." LEAN.21 S1 fixes the accepted axiom list too. Notes: the definitions under verification are covered by the review of QA.7 only. |
| Cold SF6: LEAN.1 bundle | Accepted. LEAN.1 is two sentences: one pin of toolchain, each checker (cold Opt 2), and each Lean package; one sentence that builds and checks use them unchanged. g.18 notice removed. |
| Cold SF7: LEAN.9 S2 restates VV.3 | Accepted (L7). S2: "Each change to those files or to the accepted axiom list SHOULD be recorded apart from each change to a proof that they judge (VV.3)"; the clause on keeping the earlier statement is dropped. Adds the accepted axiom list (pairs Opt 7b). |
| Cold SF8 (R8), pairs Opt 3: onsets incomplete | Accepted (L7). The class-onset paragraph places each provision sentence by sentence: LEAN.19 (VV.6) at CSQ3 for a component, the assembly verification staying with the CSQ1 row; LEAN.24 and LEAN.26 (DSGN.2) at CSQ3 as precondition checks and stated assumptions, postcondition checking staying with the CSQ1 row; LEAN.25 binding at every class; LEAN.4 row Code that runs takes the onset of LEAN.17 S2 for its definitions; both sentences of LEAN.14 at CSQ3. |
| Cold SF9, pairs SF4: Terms | Accepted (L7). "Fourth major form" removed: Lean is "the language ... that the Lean reference manual describes, at each release of its toolchain". Execution setting import removed. "Advisory" kept in lower case in LEAN.3, as the corpus uses defined terms in bodies (STND.JL "qualified revision", STND.OFFLD "submission"). |
| Cold SF10: Notes prescribe in the indicative; length | Accepted (L7). Recast: the review sentence (now "stay as QA.7 asks" of what LEAN.22 leaves), "The second sentence of STND.LEAN.19 states the code of a separate implementation as verified by comparison". "Rather than" removed twice. Notes not shortened materially; the added decisions and onsets offset the trims. |
| Pairs SF2: LEAN.4 Statement review row lacks outcome (VV.5) | Accepted: the row asks whether the review found that the trusted statement says what the claim needs, or the statement that validation does not apply for want of a real-world referent. |
| Pairs SF3, Obs 3 (R16): LEAN.25 sentences conflict; list narrower than PRIME.4 | Accepted (L5). LEAN.25 is "Lean responses to listed failures", binding through PRIME.4, with the five responses of STND.CXX.16, STND.PY.22, STND.JL.15. The run-ending sentence moved to the Notes (unverified setting); the no-substitution rule is LEAN.24 S2, a default. Binding mode is a custodian decision (R16), argued as for STND.JL.15. |
| Pairs SF5 (R18): LEAN.27 lacks the NUMER.4 allowance | Accepted (L6). LEAN.27 S2: "A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4)." Naming rule across languages goes to the custodian (R18). |

## Optional

| Finding | Disposition |
| --- | --- |
| Cold: LEAN.25 prohibition inside SHOULD | Moot: LEAN.25 rewritten. |
| Cold: LEAN.1 S3 against LEAN.3 (checker revisions) | Accepted: LEAN.1 pins each checker. |
| Cold: practice 22 dependency graph unused | Declined: the LEAN.4 table carries the reviewer's items; a graph is a means. |
| Cold: LEAN.27 thin | Kept, with the NUMER.4 sentence. |
| Pairs Opt 1: LEAN.23 cite HW.5, NUMER.12 | Declined: they bind only work that HW or NUMER selects; STND.VVUQ.36 and .37 are cited in the Notes. |
| Pairs Opt 4 | Accepted (above). |
| Pairs Opt 5a: LEAN.31 exemption for dependencies | Accepted: exemption limited to a warning raised inside a Lean package. |
| Pairs Opt 6: memory model in LEAN.4 | Accepted: row Code that runs adds the memory and ordering model that the Lean model assumes for concurrent code; the Notes tie it to HW.11 and STND.CONC.28. |
| Pairs Opt 7a: LEAN.8 S2 too strict for releases | Accepted: each placeholder in a release is stated in its record, for the QA.10 decision. |

## Decisions now for the custodian

1. Mnemonic LEAN (alternative LEA).
2. STND.LEAN.5 binding through PRIME.2 raises no floor.
3. STND.LEAN.25 binding through PRIME.4 (R16), as for STND.JL.15.
4. Logical axiom declarations read as assumptions of the evidence (alternative: one standing owner declaration of the logic under VV.9); native-evaluation axioms on the accepted list as trust in the compiler.
5. The CSQ0 reading and the strict Term Independent checker (alternative: separate source, any runtime, relation stated), noting no known checker meets the strict Term.
6. LEAN.27 leaves naming to the repository configuration (R18).
7. LEAN.22 as consistent with QA.7.

# Dispositions: draft 0.2 to draft 0.3 (2026-10-24)

Review answered: `verify-0.2.md` (no defect; S1 to S4, O1 to O6). Draft 0.3: `draft-0.3.md`; pairs: `pairs-0.3.md` (1,046 pairs). Rehearsal `/tmp/rehearsal-_b49n0is/governance`: verify passes all eight checks; `findings.py` reports only the g.18 notice on STND.LEAN.21. Draft 0.2 module kept at `.scratch/lean/content_lean_v02.py`.

| Finding | Disposition |
| --- | --- |
| S1: LEAN.5 S2 "of the work" undefined | Accepted. S2: "Other than in a report that names the declarations that its check did not cover, a report that a theorem is proved SHALL rest on a check, at the reported revision of the source, of each declaration on which the theorem depends other than those of the toolchain (PRIME.2)." Notes: Lean packages are included; a package taken from fetched build products that no checker of the work replayed is named in the report. PRIME.2 argument kept. |
| S2: LEAN.25 restates PRIME.4 (GOV.31) | Accepted. LEAN.25 names the Lean forms of the responses: a result of `Except` or `Option` type or another type that carries the condition, and `throw` in a monad whose caller receives the error, as STND.CXX.16, STND.PY.22, and STND.JL.15 name theirs. The Notes say these are core-library names that l1 does not discuss. |
| S3: Notes on panics and indexing | Accepted. Panic continuing with a default value now rests on l1 (S5); the printed message and the run-ending setting are marked as recalled and unverified; the indexing forms are marked unverified in l1. |
| S4: Notes length | Accepted. The Notes go from 4,936 to 3,757 words (24 percent less), cutting restatements of l1 in "Evaluation and checkers", "Definitions", "Untrusted authors", and "Maintenance", and the lists of STND.CODE, AGENT, and STND.DEPS provisions that restated the corpus. |
| O1: LEAN.24 onset and "documented response" | Accepted. The onset sentence says S1 is met by a check of the operands before the operation (a precondition) or by a proof or a stated reason, and does not ask the checking of results of the CSQ1 row of DSGN.2; S2 bars a function that chooses its own value in place of its result, visible or not. S2 now reads "a function that, on a failure that it detects, returns a value that the function itself chooses in place of its result", which leaves out a default that the caller supplies. |
| O2: LEAN.4 memory-model row | Accepted. The onset paragraph says the row records an assumption of the evidence (VV.1) from CSQ3, with the DSGN.15 verification at CSQ2 and the STND.CONC.28 proof at CSQ0 left to their rows. |
| O3: LEAN.14 S2 onset | Accepted. The record applies from CSQ3, and the evidence that does not rest on the compiler, a comparison with a reference produced without the compiled code, applies from CSQ2 by the reference-oracle row. |
| O4: floor stated as fact | Accepted. "The Notes argue that no provision raises the floor (GOV.11), which the custodian decides for STND.LEAN.5 and STND.LEAN.25"; the status paragraph uses the same form. |
| O5: wording | Accepted. "The argument that the Notes of STND.JL give for STND.JL.15, which the custodian adopted"; GOV.51 cited only for tool software treated as an agent; the AGENT.47 items are stated "as departures". |
| O6: decision 4 and LEAN.16 | Accepted. The Notes say the reading of VV.1 "shown to be met" as "stated as assumed" covers the soundness of each checker as well as the logical axioms, and that every Lean project at CSQ0 replaces STND.LEAN.16 until a checker meets the strict term. Decisions updated below. |

## Decisions now for the custodian (supersede the list above)

1. Mnemonic LEAN (alternative LEA).
2. STND.LEAN.5 binding through PRIME.2 raises no floor.
3. STND.LEAN.25 binding through PRIME.4 (R16), argued as the Notes of STND.JL argue STND.JL.15.
4. VV.1's "shown to be met" read as "stated as assumed" for the soundness of the logic and of each checker and for the logical axiom declarations, which are assumptions of the evidence and not Axioms (alternative: a standing owner declaration of the logic under VV.9); native-evaluation axioms on the accepted list as trust in the compiler.
5. The CSQ0 reading and the strict term Independent checker (alternative: separate source, any runtime, relation stated); under the strict term every CSQ0 Lean project replaces STND.LEAN.16 until a known checker meets it (lead decision L3, listed for the custodian only).
6. STND.LEAN.27 leaves naming to the repository configuration (R18).
7. STND.LEAN.22 consistent with QA.7.
