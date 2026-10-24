# Cold review of STND.LEAN draft 0.1

## Verified by script
- Rehearsal `/tmp/rehearsal-d13ud3p5/governance`: `govharness verify` passes all eight checks. `findings.py 'STND\.LEAN'` gives only two g.18 review notes (three modals in LEAN.1 and LEAN.21).
- All 31 per-provision files: every body line appears in the reading copy; one provision binding (LEAN.5), 30 default; titles at most six words and distinct corpus-wide; IDs in each body equal instantiates plus refers_to; one modal per sentence; none of the STND.DRAFT.17, .13, .7 words; none of the STND.DOCS.9 forms except "rather than" twice in the Notes.
- Terms use: every defined term appears in the provisions. "Execution setting" (imported) appears nowhere else.
- Not scripted: conditions (read by hand), onsets, overlaps, research accuracy.

## Defects
1. **LEAN.5 sentence 2 raises the floor above PRIME.2, and the condition trails its clause (STND.DRAFT.16).** PRIME.2 forbids claiming a check that was not run. "Only on a check ... that built each declaration on which the theorem depends" permits one honest report only: a build of everything. A report that says "proved; the imported library was taken as published and not rebuilt here" claims no check that was not run, and PRIME.2 allows it; LEAN.5 forbids it. Declarations of the core library and fetched build products are never built by a local check, so the sentence is also unsatisfiable as written, and LEAN.15 sentence 2 (a default) asks the same coverage as an option. A binding provision may not ask what a default asks (GOV.19). The cost is a build, not wording. Fix: "Other than where the report states which declarations the check did not build, a report that a theorem is proved SHALL NOT rest on a check that did not build each declaration of the work on which the theorem depends, at the reported revision of its source (PRIME.2)." Sentence 1 stays: a placeholder-dependent theorem reported as proved misstates status. Add to the Notes that "reported as proved" means unqualified, so "proved except for the placeholder in X" is allowed.
2. **LEAN.7 and LEAN.14 contradict each other.** LEAN.14 admits native evaluation with a record. Its axiom declaration is not a logical axiom declaration (the Term excludes it) and no owner declared it, so LEAN.7 keeps it off the accepted axiom list, and LEAN.6 sentence 2 then fails every such theorem. Fix: LEAN.7 sentence 1 adds "and the axiom declarations of native evaluation that a record under STND.LEAN.14 covers"; add the same to the Term Accepted axiom list.
3. **LEAN.21 sentence 1 has two conditions** ("Where an untrusted author writes ...", "before that author begins ..."). Fix: "Before an untrusted author begins the proof of a relied-on theorem, its trusted statement SHOULD be fixed, in files that the author does not change (VV.3)." Sentence 2 then reads "The verdict on a proof that an untrusted author wrote SHOULD come from ...".
4. **References omit STND.CXX and STND.PY**, cited in the Notes (naming paragraph). STND.DRAFT.34 is binding: add both rows.

## Should-fix
1. **Facts recalled, unverified in l1, inside normative text.** LEAN.11 row 3 states "which wraps" as fact; LEAN.24 rests on it. LEAN.25 rests on panic behavior (print and continue), and "panic" is not a Term. Nothing rests on csimp, build caches (LEAN.15 only asks coverage), or naming (LEAN.27 delegates). Fixes: row 3 becomes "Arithmetic of fixed-width integers | That the operands stay in range, or that the claim concerns the values the type gives out of range"; add a Term "Panic: a report by running code of a condition it does not handle, which the runtime may answer by continuing"; mark both in the Notes unverified. The Term Replaced implementation excludes csimp on the same unverified recall: drop that Notes sentence or say what the compiled-definitions row trusts.
2. **CSQ0 reading (Notes, "Proof at CSQ0").** Supported in part. The research (practice 15, S5, S18, S19) supports both exclusions in the Term Independent checker as lowering shared defects, but calls independence a matter of degree, and S18 and S20 report a bad proof accepted by a second kernel. It does not support a stricter test than VV.1 for proof in general; practice 14 asks a second checker only for untrusted authors. As written, "meets the first of these only where ... an independent checker accepts" defines proof under STND.CLASS.10 more narrowly than VV.1, yet LEAN.16 is a default a project may replace, so the reading cannot be a condition. The only second kernel the Notes cite (written in Lean, a port of the reference) fails both exclusions, and the Notes name no checker that meets the Term. Fix: reword as "The default of STND.LEAN.16 is how the standard meets the row; a project that replaces it records how its Lean proofs meet VV.1"; say that no checker is known to meet the Term (l1 leaves this unverified), so at CSQ0 the replacement is the likely path; keep "for the custodian to confirm" and number it a decision.
3. **Logical axioms as assumptions of the evidence.** Consistent with the Lexicon (Axiom is what the owner declares) and with GOV.50, and LEAN.7 asks the owner for nothing, so STND.DRAFT.42 is not triggered. Two gaps. VV.1 asks assumptions "shown to be met", which no axiom or kernel-soundness assumption can be. And the reading decides at LVL2 which unproven assumptions need no owner declaration, where VV.9 says "an assumption accepted without demonstration". Fix: put it to the custodian as a numbered decision with the alternative (one standing owner declaration of the logic of Lean, recorded once), and say in LEAN.4 that these assumptions are stated, not shown met.
4. **LEAN.22.** Consistent with QA.7 and AGENT.2 to .5 as a permission about correctness only, but: (a) the checks may be the author's own run; an agent author can disable or alter them (AGENT.47) and the accepted axiom list lives in configuration, not in the files of LEAN.9. Fix: "Where the checks ..., as configured before the change, pass on the reviewed revision in a run that the reviewer confirms, and the change alters neither the accepted axiom list nor those checks, the review of correctness MAY rest ...". (b) The Notes say reading the script is "unnecessary", but LEAN.17, 24, 29, and 30 are judged by reading code; limit the Notes to correctness. (c) LEAN.13 is not among the checks but the review is said to rest on LEAN.11 alone; say so.
5. **Untrusted author.** Counting every language model, the project's agents included, matches AGENT (no agent is trusted by role; GOV.51) and QA.7 (LEAN.21 gives a verdict, not a review). But the head clause "an author of Lean source that the work builds before a review of that source" covers every author, human included, since all source is built before review; "among them" then lists examples. Fix: "A language model, a tool that searches for or generates proofs, or an actor whom the threat model of the project does not trust, as the author of Lean source." Also LEAN.21 fixes only the trusted statement from the author; the accepted axiom list and the definitions under verification (the code, which LEAN.9 excludes) are equally open to an author who wants a trivial proof, and LEAN.10 compares only against the files LEAN.9 holds. Fix: add the accepted axiom list to the files the author does not change, and say in the Notes that the definitions are covered by review (QA.7) only.
6. **LEAN.1 bundle.** A project can adopt the toolchain pin without the manifest pin (REPRO.2 against REPRO.9), so "one pin, applied together" does not meet the test of the OFFLD review. Split sentence 2 off, or argue that sentence 3 needs both. LEAN.21's bundle is defensible as written.
7. **LEAN.9 sentence 2** restates VV.3 ("leaves the original criteria in the record"). Keep only "recorded apart from the change to a proof that it judges", the extension of AGENT.5 to every actor, and cite VV.3.
8. **Onset paragraph incomplete.** LEAN.19 cites VV.6 (CSQ1 row, assemblies; the link of a component is CSQ3): say so. LEAN.24, 25, and 26 cite DSGN.2, whose postcondition checking starts at CSQ1: place each. LEAN.4's Code that runs row names the LEAN.17 definitions, which sentence 2 of LEAN.17 puts at CSQ2; say the row takes that onset for them.
9. **Terms.** Drop Execution setting (unused). "Fourth major form" is a version number (custodian: none); define by the language construct set or note it as a decision. Terms import Advisory and use "advisory" in lower case in LEAN.3: capitalize or drop.
10. **Notes in the indicative as obligation:** "review of such a change then concerns the trusted statement ... and reads the script for its maintenance only" and "The code of a separate implementation is therefore verified by comparison" prescribe; recast as what the provisions do. The Notes run about 5,300 words; the claims are sourced, but trimming restatement of l1 would help STND.DOCS.9.

## Optional
- LEAN.25 sentence 1: "and not respond by a panic" is a prohibition inside a SHOULD; split into a SHOULD NOT sentence.
- LEAN.1 sentence 3 pins every check to one toolchain while LEAN.3 asks a checker at another revision; extend sentence 1 to each checker, as LEAN.4 records it.
- l1 practice 22 (dependency graph from the headline theorem) is unused; "rather than" twice in the Notes (STND.DOCS.9, negative parallelism).
- LEAN.27 adds only a configuration entry to INTPR.1; keep, it costs a line.

## Notes claims against l1
All figures checked: 40 percent, five benchmarks, 29 checkers, 20 to 50 percent, 1,673/5,714 (3.4 to 1, and the 13:1 conflict with practice 19 is correctly flagged), ten times smaller, 21 and 4, nine patterns. The sine of zero, the toolchain-file update, and the nested-unsafe claims match l1. No claim found unsupported and unmarked.

## Overlaps
| Provision | Existing | Verdict |
| --- | --- | --- |
| 1 | REPRO.1, .2, .9; DEPS.8 | Partial restatement (exact revisions); adds manifest and transitivity |
| 2, 3 | VV.8, DEPS.5, DEPS.7 | Adds rebuild from source and re-acceptance; keep |
| 5 | PRIME.2, AGENT.4 | Partial; sentence 2 exceeds (Defect 1) |
| 9 s2 | VV.3, AGENT.5 | Restates VV.3 (Should-fix 7) |
| 13 | PRIME.2 | Adds the means; keep |
| 19 | CONC.28 | Adds link table; no restatement |
| 21 | AGENT.5, GUARD.16/17 | Adds protocol; bundle defensible |
| 22 | QA.7, AGENT.12 | Permission only; see Should-fix 4 |
| 23 | VVUQ.36, .37 | Adds model statement |
| 25 | PRIME.4, CODE.7 | Sentence 1 partly restates the PRIME.4 responses |
| 31 | JL.35, DSGN.6 | Form for Lean; keep |
| Others | none found | No restatement |

## Coverage
l1 practices 1 to 21 each land in a provision; 22 is covered by the LEAN.4 table, except the dependency graph.

## Could not check
No Lean was run. Sources S1 to S29 were not refetched; Notes were checked against the text of l1 only. The 1,046 pairs were not reviewed (pair review is separate).

## Verdict
Revise before adoption: four defects (LEAN.5 floor and wording, LEAN.7 against LEAN.14, LEAN.21 conditions, References), then the should-fix items, of which the CSQ0 reading and the logical-axiom reading go to the custodian as numbered decisions.
