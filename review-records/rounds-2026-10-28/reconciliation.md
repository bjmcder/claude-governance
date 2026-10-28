# Rounds of 2026-10-28: reconciliation review across rounds a, d, c, o, and e

Reviewer of another configuration, cold, on branch `rounds-2026-10-28` at 7af63d3. The per-round records (`round-{a,d,c,o,e}/decisions.md`, `review.md`, `verify.md`) were read after the standing process, the rulings, and the brief; nothing of the drafting was seen. The question here is only what those records could not see: the five rounds taken together.

## What I ran

- All five rounds applied through `apply_rounds_2026_10_28.py` (no `ROUNDS`) to `/tmp/claude-1000/rvx/governance`: entries 203 to 321, 119 transactions, in the driver's order a, d, c, o, e.
- `verify` on the copy: every check PASS (`ids`, `mnemonics`, `references`, `manifests`, `ledger`, `unpinned`, `templates`, `status`, `checked-by`, `onset`, `logic`), with only the g.18 warning the corpus already carries.
- `references --check`: PASS.
- `onset` for each class: CSQ0 2, CSQ1 22, CSQ2 157, CSQ3 618, as round e's verification states.
- `compose --all` of the live corpus to `/tmp/claude-1000/rvx/before` and of the applied copy to `/tmp/claude-1000/rvx/rendered`: 71 reading copies each; 53 differ (the 48 revised documents, the four LVL0 article copies, and the root `STND.md`). The changed lines of every differing copy were read; those of STND.CLASS, STND.PROJ, STND.DFLT, STND.DEPS, STND.HARN, STND.INSTR, AGENT, and LVL0 were read whole against the five records.
- `rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`: 119 entries appended (203 to 321); every check PASS, `onset: PASS`, logic PASS with only the g.18 warning the corpus carries; "source unchanged: 1610 files and directories"; exit 0.
- Greps over the applied copy: the nineteen identifiers that rounds d and e withdraw survive only in `withdrawn` fields and revision rows; no Notes paragraph still states an onset by sentence; no text names a round ("round o", "this round") outside one revision row (Should-fix 3); the attributions "The custodian ruled" occur in the STND.DFLT Notes (Optional 3) and in the pre-existing STND.CODE and STND.CXX Notes.
- Revision bookkeeping: the 2026-10-28 rows of all 48 revised documents, read from the applied copy, step monotonically (for instance STND.CODE 1.4 M, 1.5 M, 1.6 M, 1.7 M; STND.PY 1.3 M, 1.3.1 E, 1.4 M, 1.5 M; LVL0 1.7 M, 1.7.1 E), each class agrees with its content under STND.IDENT.3 as far as the records argue it, and the `v` checks pass. The LVL0 transactions (223 and 288) have the form of entries 30 and 7: type `amend`, authority GOV.40, targets LVL0 with the provisions changed, the thirteen LVL0 folders as scope. The root STND transaction (300) has the form of entry 186. The field `revision` of each document equals its last row.

The rulings' chain of anchors holds: every `replace_text` and `swap_para` of rounds d, c, o, and e applied on top of the earlier rounds, which the build proves, since each refuses a text that does not occur exactly once.

## Rulings coverage (check 4)

Every ruling of Parts A to F other than F3 is carried by a round or explicitly disposed of:

| Ruling | Round | Carried as |
| --- | --- | --- |
| A1 to A5, B1, B2 | a | STND.DFLT.33, .34, .35, .17, .23, term Assured work, term Working bounds, STND.INSTR.11, term Tool memory store |
| C1 to C6, C8 | c | GOV.13, QA.11, STND.CLASS.3, .5, .21, .22, .23, .18, .19, the HW, HW.CPU, NUMER reports, AGENT.23, the term Main line; PRIME.13 kept (C8) |
| C7 | o | STND.CLASS.10, the field `onset`, the cores of STND.VVUQ, STND.WFLOW, STND.TEST, HW |
| D1 | d | STND.CODE.21, .27 to .35, STND.CODE.14; named documents and revision numbers out of the Notes |
| E1 | e | STND.HARN.24, .28, unit 0024 |
| F1 | a, c, d, e | R1.3 to R1.7, AD5 (a); R2.2, R2.5 (c); R5.3, R5.4, R6, R7 (d, e) |
| F2 | driver | The order of application, with one departure (Should-fix 2) |

Nothing fell between rounds. The items one round left to another were each picked up: round a's STND.DEPS Notes sentence (round d, decision 19); round d's copies 1b, 3a, 16, and CL7 (round e); round c's CS9 residual and the pairs listing (round e); round o's reading 9 (round e, reading 6).

## Defects

None. No provision amended by two rounds carries a contradiction, and no later round silently undoes an earlier round's fix. The provisions touched by more than one round were read in their final text:

- STND.CLASS.10: round c's second sentence (the CSQ4 exceptions) and round o's first sentence (the field) sit together; STND.CLASS.21 and .23 carry `null` ("at every class"), which is what the exception needs.
- STND.CLASS.21: round o's clause ("and of the provisions below LVL0 whose field `onset` gives that class") is inside round c's sentence, modals unchanged.
- STND.PROJ.1: round c's expected-class item and round e's removal of the execution paths are both in the Classification row; the Architecture row names where the paths are recorded; HW and its six sub-profiles say the same.
- STND.CODE.20: round c's two sentences; round o's field `["CSQ3", ["sentence 1", "CSQ1"]]`; the STND.CODE Notes agree (the record from CSQ1, the marker where such a standard is adopted).
- STND.DEPS.13: round d's exception, widened by round e to the checks of STND.DEPS.14.
- STND.CODE.21: binding for every language (round d); its C++ and C copies withdrawn (round e); the STND.BUILD, STND.CXX, and STND.STDC Notes cite STND.CODE.21.
- AGENT.6 (round a) and AGENT.39 (round c): coherent, with one wording to tighten (Optional 1).
- GOV.13, QA.11 (round c) and GOV.11, GOV.24, GOV.48, GUARD.4, GUARD.15 (round e): disjoint provisions; the STND.CLASS Notes' GOV.11 argument for C4 reads the unchanged clause of GOV.11.

## Should-fix

1. **Reading a.1 would be a ruling without a record.** Round a asks the custodian to adopt, as an interpretation of PRIME.7 under GOV.3, that "installs software or dependencies" means adding software to the environment or a dependency to the work, not reproducing the recorded set within the working bounds. STND.DFLT.34's MAY rests on it. No round records a `rule` transaction (STND.HARN.7 lists the type), so if the custodian adopts it, the interpretation lives only in `round-a/decisions.md`, and a reader of STND.DFLT.34 cannot find it. Fix: the lead records the ruling as one transaction of type `rule`, authority GOV.3, target PRIME.7, quoting the custodian's words, right after ratification; the STND.DFLT Notes already describe the reading and need no change.

2. **The driver departs from the ruled order and says it does not.** Ruling F2 ("Agree", "Rounds in the recommended order") puts Part C before D1. The driver applies d before c, and its docstring says "The rounds run in the order of ruling F2: the defaults and instruction authority, then the language and systems standards, then classes and promotion, then the onset rule, then the harness's place in the corpus". The departure is harmless, since every later round is anchored on the earlier ones and the result is one packet; but the docstring asserts a conformance the custodian did not get, which the standing process forbids. Fix, in `tools/amendment-scripts/apply_rounds_2026_10_28.py`: replace "The rounds run in the order of ruling F2: the defaults and instruction authority, then the language and systems standards, then classes and promotion, then the onset rule, then the harness's place in the corpus and the rest." with "The rounds run in the order a, d, c, o, e: ruling F2's order, except that the language and systems standards (D1) come before classes and promotion (C1 to C6), because round c's edits to STND.CODE and the language standards are anchored on round d's text. The custodian is told of the departure at ratification." Also one line in the ratification packet.

3. **Seven ledger rationales of round o say the moves "are put to the custodian".** `apply_round_o_2026_10_28.py` (CODE_FORM_FLOOR's users for STND.CODE, STND.CONC, STND.MPI, STND.OFFLD, STND.OMP, and PROTOCOL_FLOOR for STND.CREW and STND.WPROC) writes into a rationale that opens "ratified by the custodian on 2026-10-28" the words "the moves are put to the custodian, since the lists of the review do not name them" (and "the move is put to the custodian", "the three moves are put to the custodian", "STND.CODE.35 ... is put to the custodian"). The live ledger has no rationale of that form; after ratification the sentence is false, since the custodian will have ruled on reading o.2 either way. Fix: once the custodian rules on o.2 and o.3, replace each with the outcome, "the moves were accepted by the custodian at ratification" (or, under option (b), the module changes anyway); seven ledger rationales, from six strings of `apply_round_o_2026_10_28.py` (PROTOCOL_FLOOR serves two documents). The two matching strings of `round_o_fields.py` are the sources column of the review table and reach no record.

4. **One revision row names "this round".** STND.BUILD 1.0.5 (round e): "in place of naming STND.CXX.18 and STND.STDC.40, which a later transaction of this round withdraws". A revision history is read without the round. Fix in `round_e_code.py`, STND.BUILD's reading: "which STND.CXX 1.5 and STND.STDC 1.5 withdraw".

5. **STND.CLASS Notes name one of the two CSQ4 exceptions.** STND.CLASS.10 (round c): "Work of CSQ4 MAY omit every obligation of these Articles above the floor, other than STND.CLASS.21 and the records of STND.CLASS.23". The Notes paragraph "Work of CSQ3 meets the seven proportioned Articles…", as rounds c and e leave it: "Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor, and the records of STND.CLASS.23 where the classification records an expected class." A reader of the Notes concludes that CSQ4 omits STND.CLASS.21, which reading c.2 recommends it should not. Fix in `round_c_class.py`: "…because GOV belongs to the floor, and, where the classification records an expected class, STND.CLASS.21 and the records of STND.CLASS.23."

6. **Reading e.3 omits a cost that round a creates.** STND.DEPS.14's second sentence has a check run "at the interval that the repository configuration sets", which for Python is new (reading e.3). Round a's term Working bounds leaves out for writing "each setting that … runs a program without a request", so an agent cannot set that interval; the human owner sets it, or records the decision that replaces the default (GOV.19), which is itself an act entered under STND.DFLT.17. Either way one act of the human owner per Python project that declares a range. Fix: add to reading e.3 the sentence "Under the working bounds of STND.DFLT, the setting that schedules the check is the human owner's to make, so the SHOULD costs a project one act of the human owner, or one recorded decision to replace the default; CL7's MAY costs none."

## Optional

1. **AGENT.39 names an estimate that AGENT.6 may not ask for.** Round a conditions AGENT.6 on a measurable cost and no discipline under GUARD.14; round c has AGENT.39 accept "an effort estimate under AGENT.6 that states its basis". Where a discipline is set or the cost is not measurable, AGENT.6 asks nothing, and "under AGENT.6" can be read as "that AGENT.6 requires", which would send the first parallel delegation to a measured baseline or a decision of the human owner. Round c's record means the form of AGENT.6, supplied at every class. Fix in `round_c_rest.py` (AGENT39): "an effort estimate in the form of AGENT.6 that states its basis".

2. **STND.CLASS.19's auditor row keeps the term that C6 refined for reviewers.** The CSQ1 and CSQ2 rows: "an agent auditor has an agent configuration different from that of every authoring agent". Under the term Agent configuration (model, instruction revision, tools), a difference of tools alone satisfies the auditor row but, after round c, not the CSQ2 reviewer row of STND.CLASS.18. The ruling C6 spoke of reviewers, so this is a reading to put, not a defect; the Notes could say the auditor row is read as the CSQ2 row of STND.CLASS.18, or the custodian may rule it so.

3. **The STND.DFLT Notes attribute the drafted reading to the custodian.** "The custodian ruled on 2026-10-28 that a build, an install, or a test run in the course of the work is permitted against the recorded configuration or where otherwise authorized, and that the installation of a package the configuration does not name, or a build or test run beyond the working bounds, halts and is referred." The custodian's words were "against the stated configuration" and "beyond the project bounds"; "recorded configuration" and "working bounds" are round a's reading. The review of round a removed the same attribution for A1 (S10). Fix in `apply_round_a_2026_10_28.py`: quote the ruling's words, or replace "The custodian ruled on 2026-10-28 that" with "Under ruling A2," and leave the reading as the Notes' own.

4. **STND.CODE Notes: "the record that STND.CLASS.22 then owes".** Round c: "the marker of STND.CODE.20 is the one thing of this standard kept earlier, so that the reclassification finds each deviation by a search and the record that STND.CLASS.22 then owes is written once." STND.CLASS.22 owes no deviation record; STND.CODE.20's first sentence does, from CSQ1. Fix in `round_c_rest.py` (CODE_DOC): "the record that STND.CODE.20 then owes".

5. **STND.DEPS.14 and STND.DFLT.35.** A check of STND.DEPS.14 installs the oldest or newest revisions that a declared range admits. Such an install adds nothing to the recorded configuration, since the range is the configuration, so STND.DFLT.35 does not halt it and STND.DFLT.34 covers it; but no Note says so, and an agent reading STND.DFLT.35's "a revision of a package" may halt. One sentence in the STND.DEPS Notes (round e): "A revision that a declared range admits is one the configuration names, so a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts."

6. **Round o's reading numbers.** Round o keeps the first draft's numbers (1, 2, 3, 7) and round e's reading 6 refers to "round o's reading 9", which round o's own list no longer carries. Renumber round o's readings 1 to 4 and have round e cite "round o, disposition row 11" instead, so that the packet's register (below) reads without the drafts.

## Net burden (check 5)

**A CSQ4 unit of work**, under the defaults, after the five rounds. The human owner's direction of the work, naming or accepting a plan that names the agents and the configuration, authorizes the operating cost (STND.DFLT.33); the agent enters that direction once (STND.DFLT.17) and states an effort estimate only where the cost is measurable and no discipline is set (AGENT.6). Builds, installs within the recorded configuration, and test runs proceed (STND.DFLT.34); a compiler's cache under the home directory is within the bounds (term Working bounds). The classification, drafted by the agent and adopted by the owner's word, reaches the ledger through the agent (STND.DFLT.17, STND.DFLT.13); until it is recorded, the work meets the floor and halts only at a promotion, release, deployment, or hardware command (GOV.13). Results are relied upon by the author or the immediate team under the standing promotion (QA.11). Records above the floor are omitted (STND.CLASS.10), other than STND.CLASS.21 and the records of STND.CLASS.23 where an expected class is recorded, which the owner's entry of that class justifies (GOV.11). Acts of the human owner that the rounds add: none beyond the direction of the work, which the owner makes anyway. Acts the rounds add that the custodian did not ask for: the one adoption per instruction-file change under reading a.3 (the ruling says "You adopt each file once"), which the reading already states as the choice; and the referral of each package the recorded configuration does not name (STND.DFLT.35), which ruling A2 asks ("Installation of new packages … are a halt and refer"), and which STND.DFLT.32 turns into one standing authorization at the first referral.

**A CSQ3 unit of work** adds: review by an actor in another session (STND.CLASS.18, CSQ3 row; an agent of the same configuration suffices); the network record met by an unedited transcript (AGENT.23); a change of context before editing after a research retrieval (STND.CREW.23, now SHALL, which round c argues and records as heavier than the SHOULD it replaces, at no cost to the human owner); records of the ledger, roadmap, and decisions as commits on the development line (STND.WPROC.16); the code-form rules and the foreign-frame catch (round o's moves to CSQ3, reading o.2); the checks across a declared range at each release (STND.DEPS.14; see Should-fix 6 for the scheduled check). No act of the human owner is added at CSQ3 by any round.

**A promotion from CSQ3 to CSQ2.** The human owner reassesses and revises the classification (STND.CLASS.7, GOV.13), stating the money threshold once (STND.CLASS.3), entered through the agent; the work meets STND.CLASS.22's steps, reviewed at CSQ2 independence (a different model or instruction revision, or a human); the audit of STND.CLASS.19 falls once (an agent auditor is eligible); results relied upon beyond the team are promoted one by one (QA.11, unchanged LVL0). The acts of the human owner are the reclassification and the promotions that LVL0 already assigns.

**Blockers.** None found. GOV.13's halt now names its four triggers; STND.DFLT.9's halt has the owner's decision as resolver, entered through the agent; STND.DFLT.35's halt is resolved by an authorization or the owner's word; STND.CLASS.22's steps are the work's own; the term Team is defined where QA.11's "immediate team" is read (reading c.1). No obligation turns on an undefined term: Expected class and Reclassification are in the Lexicon; Session takes AGENT's meaning; Tool memory store, Instruction file, Main line, and Team are in Terms. No requirement is circular: STND.DFLT.34 needs a configuration under version control, which the agent writes (it is in the work and not a setting that governs the agent), and STND.DFLT.35 halts only an addition to it that no authorization or direct word of the owner covers.

## Floor (check 6)

No net raise without a recorded decision, and no binding provision lowered across rounds:

- Round a's binding additions (STND.DFLT.32 to .35, STND.INSTR.11) are permissions, identifications of a list, or statements of where PRIME.7 and PRIME.14 already halt; round e's STND.HARN.24 keeps the reach of the old text (any FAIL), which round e's review had found lowered in the first draft and the fix restored; STND.HARN.28 drops pairs that the review of their own adoption judged, which round e argues under GOV.26 and QA.7.
- Round c's STND.CLASS.21 and .23 reach CSQ4 only on the owner's entry of an expected class, the recorded decision naming the consequence that GOV.11 asks; round o gives both `null` so that no field contradicts the exception.
- Round o's moves to CSQ3 (code form, the foreign-frame catch, three protocol rules, the completion argument) are defaults from CSQ3 that CSQ4 omits; each is recorded as minor with its argument, and those outside CL1 and CL2 are put to the custodian (o.2, o.3). Round d's STND.CODE.21 binds for every language on the argument ratified for C++ and C; STND.RUST.34 keeps Rust bound at every class by reference.
- Round e's LVL0 1.7.1 deletes text held whole elsewhere at equal or higher rank (GOV.50, PRIME.1, PRIME.8, GOV.6, GOV.9); round c's GOV.13 lowers nothing because GOV.14 still has every obligation met before reliance.
- The one upward step a human reader will notice is STND.CREW.23, SHOULD to SHALL, in a provision already marked binding on PRIME.11 and GUARD.16; round c records it in its floor arguments as "heavier than the SHOULD it replaces" and the review resolved its reading by GOV.19. It adds no act of the human owner.

## Readings register (check 7)

Every "For the custodian at ratification" reading of the five records, with its number as the record now carries it. Round d's 1a, 4a, 6a, 7a, 10a, 13a, and 14a were resolved by its reviewer and kept as readings for ratification, so they are listed; 8a was withdrawn by round d itself and is not.

| Round | Number | Short title | Flag |
| --- | --- | --- | --- |
| a | 1 | PRIME.7 and installs: the interpretation under GOV.3 | needs a `rule` record if adopted (Should-fix 1) |
| a | 2 | GUARD.5 and the agent's own uncommitted edits | — |
| a | 3 | B1: adoption binds path and content | adds one act per file change; ruling says "once" (burden) |
| a | 4 | B1: unadopted files named once | — |
| a | 5 | R1.5: the threat condition of the STND.DFLT.19 halt | — |
| d | 1a | "Elsewhere a default": the annotation, not a new check | — |
| d | 4a | STND.CODE.30 reaches hash order in every language | — |
| d | 6a | STND.LEAN.1 kept beside STND.DEPS.13 | — |
| d | 7a | STND.CODE.32 narrows Rust to the means of the work | — |
| d | 7b | STND.CODE.31 in the class paragraph until round o | settled: round o replaced the paragraph |
| d | 10a | The typing specification, the Julia manual, the OpenMP specification stay | — |
| d | 13a | QA.12 in `refers_to` of STND.PERF.18 | — (round o did not move it; the STND.PERF Notes stay true) |
| d | 14a | STND.OFFLD.27 as STND.CONC.24 for device code | — |
| d | 17a | CL21 is wholly round c's | settled: round c carried CL21 in STND.CODE.20 |
| d | 18 (CL7) | Cadence of the declared-range checks | duplicate: superseded by e.3 |
| d | 18 (CL24) | STND.CXX.3 and STND.STDC's modes stay as they are | — |
| c | 1 | The term Team | — |
| c | 2 | STND.CLASS.21 and .23 at CSQ4 | — (Should-fix 5 aligns the Notes) |
| c | 3 | STND.CODE.20's record from CSQ1 | — (round o fixed the field's form, D3; the confirmation C2 asks stays open) |
| c | 4 | AGENT.39's basis: AGENT.6, not STND.CREW.7 | — (Optional 1) |
| o | 1 | Departures kept as tightenings above the floor | duplicate: includes STND.CXX.24, .26, .27, which e.6 asks again |
| o | 2 | Moves to CSQ3 beyond CL1 and CL2 | — (Should-fix 3 follows its outcome) |
| o | 3 | CS5: completion argument at CSQ3 | — (Should-fix 3 follows its outcome) |
| o | 7 | The VVUQ core without STND.VVUQ.33 | — |
| e | 1 | STND.HARN.24's outcome rests on a harness's documentation | — |
| e | 2 | The unit of a change for STND.HARN.28 | — |
| e | 3 | CL7: cadence at each release, SHOULD for every language | — (Should-fix 6 adds its cost) |
| e | 4 | CS9: execution paths leave the classification | — |
| e | 5 | CL9: build scripts of added Rust dependencies | — |
| e | 6 | Onset of STND.CXX.24, .26, .27 | duplicate of the STND.CXX part of o.1; same recommendation |

Thirty readings listed; two are settled (d.7b, d.17a) and two duplicate another (d.18 CL7 by e.3; e.6 by o.1), so 26 readings are open after deduplication. No two readings conflict: o.1 and e.6 recommend the same option; c.2 (STND.CLASS.21 at CSQ4) and round o's `null` for it agree; e.4 and round c's text agree once round e's HW and sub-profile Notes apply.

## Reconciliation dispositions

By the lead's fixer, on the working tree after f97beb5. Nothing above this section was changed. One row per finding.

| Finding | Disposition |
| --- | --- |
| Should-fix 1, reading a.1 without a record | Fixed in the module, not left to the lead: the harness records a `rule` transaction (`record_transaction`, type `rule`, empty scope, as ledger entries 47 and 48), so `apply_round_a_2026_10_28.py` records one, authority GOV.3, target PRIME.7, right after STND.DFLT 1.6, whose STND.DFLT.34 and STND.DFLT.35 its rationale cites. The rationale states the interpretation and quotes ruling A2 whole. Round a's TRANSACTIONS is 6. `round-a/decisions.md`, reading 1, says the transaction is drafted and applies only if the reading is ratified as drafted; under the alternative it is removed. Every later entry moves one place: the five rounds now append entries 203 to 322. No rationale or record cites a sequence number of these rounds, other than the check lines of the per-round records, which report their own runs. No harness code changed. |
| Should-fix 2, the driver's order | Fixed as proposed, in the docstring of `apply_rounds_2026_10_28.py`. The line for the ratification packet is the lead's. |
| Should-fix 3, "put to the custodian" in round o's rationales | Fixed in the six strings of `apply_round_o_2026_10_28.py` (seven rationales). Each now says that the lists of the review do not name the move or moves, which are "of reading 2 of review-records/rounds-2026-10-28/round-o/decisions.md, ratified by the custodian". STND.MPI's rationale gives the move of the argument of completion to reading 3. `round-o/decisions.md` says that this is true once the script runs after ratification under option (a), and that under option (b) the module changes. |
| Should-fix 4, "this round" in the STND.BUILD 1.0.5 row | Fixed as proposed in `round_e_code.py`: "which STND.CXX 1.5 and STND.STDC 1.5 withdraw". |
| Should-fix 5, the CSQ4 exceptions in the STND.CLASS Notes | Fixed as proposed in `round_c_class.py`. Round e's STND.CLASS Notes edit (`round_e_process.py`, CLASS_DOC) was anchored on the old words, so it now anchors on the new ones. `round-c/decisions.md`, reading 2, quotes the sentence. |
| Should-fix 6, the cost in reading e.3 | Fixed: the proposed sentence is added to `round-e/decisions.md`, reading 3. |
| Optional 1, AGENT.39 "under AGENT.6" | Taken as proposed in AGENT.39, the rationale and revision row, and the AGENT Notes sentence that repeats the phrase (`round_c_rest.py`). `round-c/decisions.md` (R2.2 and reading 4) quotes the new words, and reading 4 says what they mean. |
| Optional 2, the auditor row of STND.CLASS.19 | Drafted in the STND.CLASS Notes (`round_c_class.py`), after the CSQ2 reviewer sentence: "The auditor of the rows CSQ1 and CSQ2 of STND.CLASS.19 is read as the CSQ2 row of STND.CLASS.18 reads the reviewer: an agent whose model or instruction revision differs from that of every authoring agent, or a human who is not an author of the audited work." No provision changes. Put to the custodian as reading c.5, with the alternative of leaving the auditor rows on the bare term Agent configuration. Recommendation: as drafted. |
| Optional 3, the STND.DFLT Notes' attribution | Taken, by quoting: "The custodian ruled on 2026-10-28 that "builds, installs, and tests in the context of the project development" are permitted "if done against the stated configuration or otherwise authorized", and that "installation of new packages or any builds/tests beyond the project bounds" halts and is referred". The Notes then give their own reading: the stated configuration is the one recorded under version control, and the project bounds are the working bounds. Corpus Notes cite no ruling numbers, so "Under ruling A2" was not used. |
| Optional 4, "the record that STND.CLASS.22 then owes" | Taken as proposed in `round_c_rest.py`: "STND.CODE.20". |
| Optional 5, STND.DEPS.14 and STND.DFLT.35 | Taken as proposed: the sentence is in the STND.DEPS Notes, after "owes nothing under STND.DEPS.14" (`round_e_code.py`). `round-e/decisions.md` says so. |
| Optional 6, round o's reading numbers | Taken. Round o's readings are now 1 to 4 (the first draft's 7 is now 4) in `round-o/decisions.md` and `verify.md`. The record's other references to the first draft's numbers are relabeled: R4.1's "point 4" and "point 5", the row Readings, and the sentence on numbering. Round e's reading 6 and its disposition row cite "round o, disposition row 11". The modules and rationales cited no first-draft number. `round_o_fields.py`'s "(reading 1)" is unchanged. The reviewers' own `review.md` files and `round-e/verify.md` keep the numbers they were written with. Also fixed: two stale numbers inside `round-e/decisions.md`, where CL7's strength was cited as reading 2 (it is reading 3) and CS9 as reading 3 (it is reading 4). |

**Readings open after these fixes**, by the numbers the records now carry: a 1 to 5; d 1a, 4a, 6a, 7a, 10a, 13a, 14a, 18 (CL24); c 1 to 5; o 1 to 4; e 1 to 6, of which e.6 duplicates the STND.CXX part of o.1. That is 28 listed and 27 after deduplication: the register above, plus c.5.

**Checks after the fixes.**
- `rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`, all five rounds: 120 entries appended (a 6, d 15, c 21, o 43, e 35). Every check PASS, `onset: PASS`, and logic PASS with only the standing g.18 warning. "Source unchanged: 1610 files and directories"; exit 0.
- Kept copy `/tmp/claude-1000/rfx/kept/governance` (entries 203 to 322, with the `rule` transaction as entry 204): `references --check` PASS; `verify` all PASS, with only the g.18 warning; `onset` CSQ0 2, CSQ1 22, CSQ2 157, CSQ3 618, unchanged.
- Self-check of AGENT.39, the one provision whose body changed: two modals, one per sentence; no condition added; no banned word; title unchanged; body identifiers equal `instantiates` plus `refers_to` (AGENT.6 was already in `refers_to`). The Notes sentences changed (STND.DFLT, STND.CLASS twice, STND.CODE, AGENT, STND.DEPS) and the STND.BUILD row carry no modal, no "such as" or "for example", and no indicative obligation. The STND.DFLT sentence quotes the custodian's own words, including "any" and "permitted". `findings.py` on AGENT.39 and STND.CLASS.19 gives only the notices that the live corpus already carries (g.11 on AGENT.39, g.14 four times on STND.CLASS.19).
