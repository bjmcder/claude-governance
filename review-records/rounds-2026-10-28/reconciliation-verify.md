# Rounds of 2026-10-28: cold verification of the reconciliation fixes

Reviewer of another configuration, on commit 2f5c8d1, against the findings of `reconciliation.md` and the dispositions appended to it.

## What I ran

- All five rounds applied through `apply_rounds_2026_10_28.py` to a fresh copy, `/tmp/claude-1000/rvx2/governance`: entries 203 to 322, 120 transactions (a 6, d 15, c 21, o 43, e 35).
- `verify`: every check PASS (`ids` to `logic`, `onset: PASS`), with only the standing g.18 warning. `references --check`: PASS. `onset`: CSQ0 2, CSQ1 22, CSQ2 157, CSQ3 618, unchanged.
- `rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`: 120 entries appended (203 to 322); every check PASS, `onset: PASS`, logic PASS with only g.18; "source unchanged: 1610 files and directories"; exit 0.
- Greps over the fresh copy: no ledger rationale from entry 203 on says "put to the custodian"; no corpus text says "this round", "under AGENT.6" in the sense found before (the three remaining hits, STND.CREW.6, the AGENT Notes, and the STND.DFLT Notes, name the estimate that AGENT.6 asks for, which is right), or "STND.CLASS.22 then owes".
- The diff of 2f5c8d1 was read whole: four modules, the driver, and five records.

## Should-fix

1. **Closed.** Entry 204 of the fresh copy: type `rule`, actor The Custodian, role custodians, authority `["GOV.3"]`, targets `["PRIME.7"]`, scope `[]`, `corpus_hash` null, rationale opening "Interpretation of the custodian under GOV.3, adopted 2026-10-28: for PRIME.7, an agent installs software or dependencies where it adds software to its provisioned environment or a dependency to the work, and not where, within the working bounds, it reproduces the set of packages that the configuration recorded for the work under version control already names.", quoting ruling A2 whole, citing STND.DFLT.34 and .35, reading 1 of the round record, and the authorship sentence. That is the form of entries 47 and 48 field for field (they too have scope `[]`, `corpus_hash` null, one LVL0 target, and the opening "Interpretation of the custodian under GOV.3, adopted <date>: for <ID>, …"). It sits after STND.DFLT 1.6 (entry 203), whose provisions it cites; `TRANSACTIONS = 6`; `round-a/decisions.md` says it is drafted and is removed under the alternative. Every later entry moves one place, and nothing in the corpus or the rationales cites a sequence number of these rounds.
2. **Closed.** The driver's docstring now reads "The rounds run in the order a, d, c, o, e: ruling F2's order, except that the language and systems standards (D1) come before classes and promotion (C1 to C6), because round c's edits to STND.CODE and the language standards are anchored on round d's text. The custodian is told of the departure at ratification." The packet line is the lead's.
3. **Closed.** The seven rationales (entries 264 STND.CODE, 265 STND.CONC, 266 STND.CREW, 274 STND.MPI, 275 STND.OFFLD, 276 STND.OMP, 287 STND.WPROC) now say that "the lists of the review do not name the move[s], which [are] of reading 2 of review-records/rounds-2026-10-28/round-o/decisions.md, ratified by the custodian" (STND.MPI: the code-form moves of reading 2 and the argument of completion of reading 3, "each ratified by the custodian"). Nothing in them is false once the script runs after ratification under option (a) of o.2 and o.3, which is the same convention as "ratified by the custodian on 2026-10-28" in every rationale; `round-o/decisions.md` says that under option (b) the module changes before it runs. Reading numbers 2 and 3 are the current ones.
4. **Closed.** STND.BUILD 1.0.5 row: "which STND.CXX 1.5 and STND.STDC 1.5 withdraw"; no "this round" in the document.
5. **Closed.** STND.CLASS Notes: "Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor, and, where the classification records an expected class, STND.CLASS.21 and the records of STND.CLASS.23. A mechanism of GOV.21 …". Round e's CLASS_DOC anchor was re-pointed and applied (the CC30 sentence follows). Reading c.2 quotes it.
6. **Closed.** Reading e.3 ends: "Under the working bounds of STND.DFLT, the setting that schedules the check is the human owner's to make, so the SHOULD costs a project one act of the human owner, or one recorded decision to replace the default; CL7's MAY costs none."

## Optional

1. **Closed.** AGENT.39: "from a measured baseline, an effort estimate in the form of AGENT.6 that states its basis, or a recorded decision of the human owner"; the AGENT Notes sentence and the rationale say the same; reading c.4 explains the words.
2. **Closed as drafted, with one new finding (below).** STND.CLASS Notes: "The auditor of the rows CSQ1 and CSQ2 of STND.CLASS.19 is read as the CSQ2 row of STND.CLASS.18 reads the reviewer: an agent whose model or instruction revision differs from that of every authoring agent, or a human who is not an author of the audited work." Put to the custodian as reading c.5 with the alternative and a recommendation.
3. **Closed.** STND.DFLT Notes: "The custodian ruled on 2026-10-28 that "builds, installs, and tests in the context of the project development" are permitted "if done against the stated configuration or otherwise authorized", and that "installation of new packages or any builds/tests beyond the project bounds" halts and is referred; the stated configuration is read as the configuration that the work records under version control, and the project bounds as the working bounds." The quoted fragments are the ruling's words; the reading is the Notes' own.
4. **Closed.** STND.CODE Notes: "the record that STND.CODE.20 then owes is written once".
5. **Closed.** STND.DEPS Notes: "A revision that a declared range admits is one the configuration names, so a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts." Reading e.3 cites it.
6. **Closed.** `round-o/decisions.md` lists readings 1 to 4 (4 was 7), says so once ("Point 4 was point 7 of the first draft, whose numbers `review.md` uses"), and its R4.1 bullet, disposition rows 8 and Readings, and `verify.md` use the new numbers; `round-e/decisions.md` reading 6 and its disposition row cite "round o, disposition row 11", and its two stale cross-references (CL7's strength, now "reading 3"; CS9, now "reading 4") are corrected. No module or rationale carries a first-draft number; `round_o_fields.py`'s "(reading 1)" is still right. The reviewers' `review.md` files keep their own numbers, as the record says.

## New finding

**Should-fix 7: reading c.5 is a Note that tightens a binding provision.** The sentence "The auditor of the rows CSQ1 and CSQ2 of STND.CLASS.19 is read as the CSQ2 row of STND.CLASS.18 reads the reviewer: an agent whose model or instruction revision differs …" is informative text that narrows "an agent auditor has an agent configuration different from that of every authoring agent", a binding row (GOV.47). Notes carry no obligation (STND.DRAFT.5, STND.DRAFT.12), and the standing directions keep obligations in the indicative out of them; the term Agent configuration still makes a difference of tools alone sufficient for the auditor, so the Note and the row disagree and the row governs. If the custodian takes c.5 as drafted, the text belongs in the rows: in `round_c_class.py`, STND.CLASS.19 (already minor in STND.CLASS 1.4), CSQ1 row, replace "an agent auditor has an agent configuration different from that of every authoring agent" with "an agent auditor differs from every authoring agent in its model or in its instruction revision, whatever its tools", the CSQ2 row keeping "As for CSQ1"; the Note then explains, as the CSQ2 reviewer sentence does. If the custodian takes the alternative, drop the Note. Either way the reading stands as a choice; only its drafted form changes. No other defect was introduced: the rule transaction, the re-anchored CLASS_DOC of round e, and the re-timed round a transactions all apply, as the build and the rehearsal show.

## Readings register after the fixes

Open readings, by the numbers the records now carry. d.7b and d.17a stay settled (round o replaced the paragraph; round c carried CL21) and are not listed; d.18 (CL7) is superseded by e.3 and is not listed.

| Round | Number | Short title | Flag |
| --- | --- | --- | --- |
| a | 1 | PRIME.7 and installs; the `rule` transaction is entry 204 | — |
| a | 2 | GUARD.5 and the agent's own uncommitted edits | — |
| a | 3 | B1: adoption binds path and content | one act per file change; the ruling says "once" |
| a | 4 | B1: unadopted files named once | — |
| a | 5 | R1.5: the threat condition of STND.DFLT.19 | — |
| d | 1a | "Elsewhere a default": the annotation | — |
| d | 4a | STND.CODE.30's reach in every language | — |
| d | 6a | STND.LEAN.1 kept beside STND.DEPS.13 | — |
| d | 7a | STND.CODE.32 narrows Rust to the means of the work | — |
| d | 10a | Typing specification, Julia manual, OpenMP specification stay | — |
| d | 13a | QA.12 in `refers_to` of STND.PERF.18 | — |
| d | 14a | STND.OFFLD.27 as STND.CONC.24 for device code | — |
| d | 18 | CL24: the modes of STND.CXX.3 and STND.STDC stay | — |
| c | 1 | The term Team | — |
| c | 2 | STND.CLASS.21 and .23 at CSQ4 | — |
| c | 3 | STND.CODE.20's record from CSQ1 | — |
| c | 4 | AGENT.39's basis in the form of AGENT.6 | — |
| c | 5 | The auditor of STND.CLASS.19 read as the CSQ2 reviewer | new; see Should-fix 7 for its form |
| o | 1 | Departures kept as tightenings above the floor | duplicated in part by e.6 |
| o | 2 | Moves to CSQ3 beyond CL1 and CL2 | — |
| o | 3 | CS5: completion argument at CSQ3 | — |
| o | 4 | The VVUQ core without STND.VVUQ.33 | — (was 7) |
| e | 1 | STND.HARN.24's outcome rests on a harness's documentation | — |
| e | 2 | The unit of a change for STND.HARN.28 | — |
| e | 3 | CL7: cadence at each release, SHOULD; its cost stated | — |
| e | 4 | CS9: execution paths leave the classification | — |
| e | 5 | CL9: build scripts of added Rust dependencies | — |
| e | 6 | Onset of STND.CXX.24, .26, .27 | duplicate of the STND.CXX part of o.1 |

Twenty-eight listed; 27 after deduplication, as the dispositions say. No two conflict.

## Disposition of Should-fix 7

Fixed by the lead as proposed: in `round_c_class.py`, the CSQ1 row of STND.CLASS.19 reads "an agent auditor differs from every authoring agent in its model or in its instruction revision, whatever its tools", the CSQ2 row keeping "As for CSQ1"; the STND.CLASS Notes say the rows ask the same difference of an agent auditor, for the same reason; the reading, the row, and the rationale of STND.CLASS 1.4 name the change and its floor argument. Reading c.5 in `round-c/decisions.md` states the drafted form. If the custodian takes the alternative, the replacement of the row and the Note sentence are dropped.
