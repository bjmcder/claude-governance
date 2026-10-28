# Round e of 2026-10-28: cold verification of the review fixes

Reviewer of another configuration, on commits d1778f9 and dae121c.

## What I ran

Rounds a, d, c, o, and e applied to `/tmp/claude-1000/rve2/governance` (seq 287 to 321, 35 transactions, as `decisions.md` states). `verify`: every check PASS, `onset: PASS`, logic PASS with the standing g.18 warning. `references --check`: PASS. `onset`: CSQ3 618, CSQ2 157, CSQ1 22, CSQ0 2, as before the fixes. `compose --all`: the 35 documents of the round and the root `STND.md` differ from the base, and no other; the sentence-level diff of every reading copy against the first draft and against the base was read whole. `pairs` with the 23 changed provisions and `--amends GOV.11 GOV.24 GOV.48 GUARD.4 GUARD.15`: 44 pairs, the same list as `pairs-changed.md`; the three new changed-side provisions (AGENT.11, STND.DOCS.10, STND.DRAFT.42) instantiate GOV.48 and lie in touched documents, and the 16 pairs of untouched STND.CREW and STND.VVUQ provisions are gone, as the new row of STND.HARN.28 says. `tools/findings.py` over GOV, GUARD, STND.HARN, STND.PROJ, and the six sub-profiles against the base: no new finding; only the g.18 notice of STND.HARN.28 goes. `tests.checks.test_logic`, `test_combination`, `test_drafting`, `tests.cli.test_main`, and the architecture and conventions tests pass.

## Defects 1 and 2

- D1 closed as to reach. STND.HARN.24 now asks "each property whose absence a check of a harness that meets this standard reports as FAIL, as the documentation of that harness states the property (GOV.36)", with the rehearsal as the MAY; the Notes say it reaches "the checks of defaults, the logic checks, and the check of onsets". The floor is neither raised nor lowered: the reach equals the old text's (any FAIL), and no decision of the human owner enters. Decidable where a harness and its documentation exist (`harness/README.md` lists each check with its property). Where none exists, no check reports FAIL and the sentence asks nothing, the lapse CP7 found in the old .28; the record says so in reading 1. See Should-fix 1.
- D2 closed. Six editorial transactions (seq 303 to 308) after HW, in identifier order, each `amend` under GOV.41 with scope `HW`, as entries 68 to 179 record a sub-profile; HW.ASIC, HW.CPU, HW.FPGA 1.2 → 1.2.1, HW.EMBED, HW.GPU, HW.QPU 1.1.1 → 1.1.2. Each Note now reads "its provisions reach a component through the execution paths of that component, recorded by hardware type where the section Architecture of the constitution names (STND.PROJ.1)", and each References gains STND.PROJ. No "classification lists" survives.

## Should-fix 1 to 5

- 1 (the root transaction) closed. Entry 300 is `annotate`, authority GOV.36, targets `[]`, scope `STND/_doc.md`, rationale "Change of STND/_doc.md, the root document of the standards, planned, ratified and pinned by the custodian on 2026-10-28: ..."; the composed `STND.md` prints no revision line.
- 2 (GOV.48) closed, and the editorial class holds. GOV.48 ends "... for every action." and cites `["PRIME.15", "INTPR.11"]`; PRIME.1 (rank 0) holds the bar: only the human owner performs "granting authorizations and waivers", and "An agent MAY draft and propose these acts and NEVER performs them". Entry 288 names GOV.48 among its targets, and its rationale states the change, the reason, the alternatives weighed, and the lower governance affected, as GOV.40 asks; of the sixteen provisions that instantiate GOV.48 (STND.INSTR.1 to .10, STND.CXX.3, STND.DOCS.10, STND.DFLT.21, STND.PY.4, STND.RUST.6, STND.VVUQ.83), none rests on the waiver sentence. Logic check b.5 reads the bar from GOV.48 where it states it and otherwise from PRIME.1 (role `owner`, title "Accountable owner"); PASS on the rehearsed copy, and the live verdict is unchanged.
- 3 (CL7 cadence) closed: reading 3 gives (a) each release and (b) round d's wording, states what both do for Rust and Julia, and separates the strength (SHOULD or MAY), with a recommendation.
- 4 (round o's reading 9) closed: reading 6 gives (a) CSQ3 by the fields and (b) the rows of STND.STDC.1, with a recommendation; the drafted text matches (a).
- 5 (STND.PROJ.2) closed as to decidability: the provision names fifteen sections, and the Notes give the provisions of STND.DFLT for each, naming the seven stated in full. See Should-fix 2 below.

## Optional 1 to 3

Closed: STND.STDC Notes "(a2), and the removal of a test by isnan or isfinite under it is unverified."; "now" gone from STND.STDC (twice) and STND.CXX; GOV.11 "both of which the proportionality judgment states (GOV.50)".

## Readings

Six, each a true choice with options and a recommendation. Reading 1 (STND.HARN.24) offers the drafted text and the first draft only; see Should-fix 1. Reading 2 (the unit of a change) now rests on the tightened row, "Both provisions are in documents of which the change adopts or amends a provision", which the code, the Notes, and the 44 pairs all follow. Readings 3 to 6 are as above.

## Findings

No defect.

Should-fix:

1. **Reading 1 omits the option that rests on the corpus alone.** CP7's own text names the corpus: "confirm that the copy meets each provision of STND.HARN, STND.IDENT, and STND.DRAFT that the change is able to affect". With "and the field `onset` of each provision (STND.CLASS.10)" added, it keeps the reach of every check but the logic checks, which read LVL0's own structure, and asks something even where no harness exists. Add it as option (c) of reading 1, and say in the reading that under the drafted text a change applied where no harness exists owes nothing under STND.HARN.24.
2. **Four of the fifteen sections are only partly provided by STND.DFLT.** For Review and release, STND.DFLT.8 gives the review record alone, not who reviews and with what independence (QA.7, QA.8), regeneration (QA.9), promotion (QA.11), or the release decision and its gate (QA.10); for Correction, the record alone, not the mechanism (QA.13); for Incidents, STND.DFLT.12 gives the governance failure report, not the incident mechanism (QA.15); for Records, STND.DFLT.2 to .5 give no independent copy of irreplaceable data (REPRO.13). A constitution that takes the permission as written cites STND.DFLT "as the content of its sections" and so leaves those items of the rows of STND.PROJ.1 (binding) unstated. Fix in STND.PROJ.2: "... Agent instructions, and Configuration, and, for Review and release, Correction, Incidents, and Records, as the content of the items of their rows that STND.DFLT provides, and state in full only its other sections, each of these whose content departs from STND.DFLT, and the items that STND.DFLT does not provide (GOV.21, GOV.22)", with the Notes' "whose records STND.DFLT.8 gives" extended to name the items that remain to be stated or marked as not applying under the second sentence of STND.PROJ.1.
