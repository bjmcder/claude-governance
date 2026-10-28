# Round o of 2026-10-28: cold review

Reviewer of another configuration; the drafting was not seen.

## What I ran

Rounds a, d, c, and o applied through `apply_rounds_2026_10_28` to `/tmp/claude-1000/rvo/governance` (seq 244 to 286), and rounds a, d, c alone to a second copy. `verify`: every check PASS, `onset: PASS`, logic PASS with the standing g.18 warning. `onset`: CSQ2 149, CSQ1 22, CSQ0 2, CSQ3 627, as `decisions.md` states. `show` on eleven provisions, among them STND.CODE.20, STND.TEST.9, STND.MPI.7, and STND.CLASS.10. `compose --all` on both copies: only mode lines, headers, history rows, and Notes differ; the sentence-level diff of every `_doc.md` was read whole. Grep: "least severe class" and "rests on a row" survive nowhere; "applies from" only in STND.CLASS.10, the rule paragraph, kept reasons, and history rows.

The rule is stated once; every former onset paragraph is a citation; the definition is minimal and decidable, and the harness enforces what it claims. Sample: 227 of 766 rows, every document covered, each read against the body, `instantiates`, the rule, and the pre-round Notes.

## Defects

1. **Hidden moves to a less severe class.** The pre-round Notes applied STND.CREW.11 and STND.WPROC.7 and .8 from CSQ2 ("the verification of the invariants of DSGN.15 ... applies from CSQ2"). The fields give CSQ3 with the false sources `Notes of STND.CREW: CSQ3` and `Notes of STND.WPROC: CSQ3`; both documents are recorded as editorial, and no list names them. CSQ3 is right under the rule (one merge at a time is a protocol rule, not its verification), but the move must be recorded: sources `C7 rule: a protocol rule, not its verification (DSGN.15); was CSQ2`; both documents into `MINOR` with the code-form floor argument; the three added to the moves table and reading 2.
2. **STND.ANNEX.1 is a permission** (its only modal is MAY) and carries `onset: "CSQ3"`, against the definition and the four permissions left without one. Row 'STND.ANNEX.1' → `None, 'a permission, which STND.CLASS.10 does not stage'`.
3. **The CSQ4 form contradicts STND.CLASS.10**, whose second sentence lets work of CSQ4 omit every obligation above the floor but STND.CLASS.21 and .23; a field giving CSQ4 to STND.CODE.20 s2 gives a class the provision does not give force to. Resolve reading 8: STND.CODE.20 → `["CSQ3", ["sentence 1", "CSQ1"]]`; delete "or CSQ4 in a list, for a provision that applies at every class except its named parts" and CSQ4 from `parse_onset`; the STND.CODE Notes keep the marker's reach.

## Should-fix

4. **Departures without a reason in the Notes**, which the rule paragraph promises: HW.19 s1 and HW.21 (reports to the operator, INTPR.7 row; the old reason dropped), HW.18 (the contract states a limit, DSGN.5 and INTPR.10 rows), NUMER.6 (reference oracles, VV.1 row; old reason dropped), NUMER.18 s1 (report to the operator), AGENT.20 (status to the owner, INTPR.6 row), AGENT.24 (time and cost of each unit, RSRC.3 row). Add to the HW, NUMER, and AGENT sentences "a field that gives CSQ3 for a report, a limit, or a cost record that the table starts at a more severe class tightens above the floor (PRIME.15), at the cost of one message or one record", or move them.
5. **Eighteen CSQ3 provisions now carry out a CSQ2 provision**: STND.ANNEX.1, .2, .4 to .10, STND.BUILD.11, STND.CXX.4, STND.FTN.16, .17, STND.OFFLD.29, STND.RUST.2 (HW.5); STND.JL.34, STND.RUST.20 (HW.7); STND.JL.19 (HW.CPU.3). The CS6 principle applied to STND.OMP.30, that a form starts no later than what it carries out, is not applied here; reading 10 covers STND.ANNEX only. List them under reading 1 with the reason kept.
6. **The harness checks well-formedness, not presence.** A waivable provision below LVL0 without the field is silent in `onset` and `show`, the accident the decisions say the field prevents; `apply_fields` guards this round only. Let `null` mean "at every class, or a permission", and have check `onset` fail a waivable provision below LVL0 without the key.
7. **STND.CLASS.21** still names "the parts of the table of STND.CLASS.10 that apply from that class"; what a reclassification adds is now the fields. Replace with "the parts of the table of STND.CLASS.10, and of the provisions below LVL0 whose field `onset` gives that class, that apply from that class".
8. **STND.VVUQ.64**, in the core, judges fresh-seed tests "under the criteria of STND.VVUQ.33, STND.VVUQ.34, and STND.VVUQ.35", all now CSQ2. Add STND.VVUQ.33 to the core, or have the Notes say that at CSQ3 the criterion is the one the acceptance criterion states.
9. **STND.OMP.2 s1** ("a feature that the documentation of each implementation states as implemented", DSGN.5) is the kind of STND.CONC.19 and STND.OFFLD.7, which move to CSQ3; reading 2 keeps it at CSQ2 as relying on "a limit the hardware contract states", which it does not. Move it with them, or keep all three.
10. **Residual onset sentence**, STND.CODE Notes: "These onsets depart from STND.CLASS.10. STND.CODE.17 and STND.CODE.19 apply from CSQ1 ... CSQ4 included." Cut to "The fields of STND.CODE.17, STND.CODE.19, and STND.CODE.20 depart from the rule of STND.CLASS#reading-the-standard: they tighten the CSQ0 rows of DSGN.3 and VV.1."
11. **Reading 9 omits STND.CXX.26**: the row of STND.STDC.1 gives it CSQ2, its own field CSQ3, as for STND.CXX.24 and .27.

## Optional

12. STND.OFFLD rationale and row say "STND.OFFLD.14 follows HW.5 to CSQ2"; the old Notes already gave CSQ2. Say "stays at CSQ2, now with HW.5".
13. STND.TEST.3 s1, STND.TEST.4, and STND.TEST.10 s1 and s2 stay at CSQ3 and draw on the tiers (STND.TEST.1) and depth rule (STND.TEST.5), now CSQ2; the Notes should say that at CSQ3 a selection is drawn from the whole suite.

## Sample error rate

227 rows read. Wrong: AGENT.20, AGENT.24, NUMER.18, HW.18 (depart from the rule with no reason anywhere), STND.ANNEX.1 (a permission), STND.CREW.11, STND.WPROC.7, STND.WPROC.8 (false source hiding a move): 8 of 227, 3.5 percent, below 5 percent. Borderline, not counted: NUMER.4 (VV.2 row), STND.OMP.2, STND.MPI.13 s1 (a protocol property at CSQ2 with its tests). Every list value names the right sentence or row. Every move to a more severe class leaves the LVL0 obligation in force at CSQ3 and raises no floor; every listed move to a less severe class rests on C7's reading or is put to the custodian. The cores are short and workable but for items 8 and 13.

## Readings

| Reading | Verdict |
| --- | --- |
| 1 Departures kept | Keep, a true choice; complete the list with items 4 and 5, each with its reason |
| 2 Code form beyond CL1, CL2 | Keep; add item 1's three; settle STND.OMP.2 (item 9) |
| 3 CS5 | Keep |
| 4 CS6 | Merge into 1; (b) is for a later round |
| 5 CS18 | Resolve (a): it follows from the rule; (b) is outside C7 |
| 6 STND.TEST records | Resolve (a): verdict rows are not records of selection; add item 13 |
| 7 VVUQ core | Keep; the choice is whether STND.VVUQ.33 joins (item 8) |
| 8 STND.CODE.20 at CSQ4 | Resolve by item 3 |
| 9 STND.CXX.24, .27 | Resolve by deferral to round e, STND.CXX.26 added |
| 10 STND.ANNEX | Merge into 1 (item 5); STND.ANNEX.1 carries no field (item 2) |
| 11 STND.LEAN.14 | Resolve: it follows from the definition |
