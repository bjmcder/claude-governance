# Deep review of 2026-10-28: verified register

## Method

I verified the four corpus reviews: CC (core), CP (process), CL (code), and CS (systems), 108 findings in all. I checked each claim against `rendered/` and against `govharness show`. I checked every Blocker, every High finding, and every finding that raises a custodian question, and I spot-checked at least one in three of the rest. For each finding I looked for a provision, term, default, or exemption that dissolves it.

| Status | Count |
| --- | --- |
| Confirmed | 59 |
| Partly (the residue that holds is stated) | 20 |
| Refuted | 1 |
| Unchecked (Medium or Low, no custodian question) | 28 |

Unchecked: CC23, CC24, CC29, CC30, CC31; CP11, CP20, CP21, CP25, CP26, CP27; CL7, CL8, CL9, CL10, CL13, CL16, CL18, CL20, CL24, CL25; CS4, CS5, CS6, CS11, CS17, CS18, CS22.

## Rounds

Rounds are listed in priority order for CSQ3 and CSQ4 work. The class is the expected revision class under STND.IDENT.3. "Q" refers to the numbered questions at the end of this register.

| Round | Change | Documents | LVL0 / floor | Class | Entries | Q |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Default blockers on ordinary work | STND.DFLT, STND.PROJ | None under the recommended options | Minor | R1.1–R1.7 | 1, 2 |
| 2 | Human round trips at CSQ3 and CSQ4 | STND.DFLT, AGENT, QA, STND.CLASS, STND.THRT, STND.CREW, HW, STND.WPROC | LVL0 (QA.11, not floor); PRIME.13 stays | Minor | R2.1–R2.7 | 3, 4, 5, 11 |
| 3 | Expected class and the promotion path | GOV.13, STND.CLASS, STND.PROJ, STND.CODE, STND.CXX, HW, STND.CONC | LVL0 floor (GOV.13), without raising it | Minor | R3.1–R3.4 | 6, 7, 8, 9 |
| 4 | One onset rule, onsets per provision | STND.CLASS, STND.DRAFT, every profile and methods standard | None | Minor (editorial where an onset only moves out of the Notes) | R4.1–R4.2 | 10 |
| 5 | Harness dependence and ledger form | STND.HARN, STND.DFLT, STND.INSTR | None | Minor | R5.1–R5.4 | 3 |
| 6 | Restatement cleanups (GOV.31) | PRIME, GOV, GUARD, AGENT, STND.CODE and the language standards, STND.MPI, STND.OFFLD, STND.PERF, STND.WPROC, STND.DOCS | LVL0 floor text, no change of meaning | Editorial; minor where a mode or cadence changes | R6.1–R6.4 | 12 |
| 7 | The rest | Various | None | Mostly editorial | R7.1–R7.3 | 12 |

## Round 1: default blockers on ordinary work

Under the defaults, these halt or reserve routine work at every class. Each fix is in STND.DFLT and leaves GUARD and PRIME as they are.

| Entry | Sources (status) | Verified | Change |
| --- | --- | --- | --- |
| R1.1 Operating cost without an authorized estimate | CC1 (Confirmed), CC21 (Confirmed) | GUARD.14 makes the agent's own operating cost implicit expenditure. PRIME.8 lets it proceed only on an estimate that the human owner authorizes. GOV.22 bars a default from authorizing one, and the STND.DFLT Notes say "Without a cap adopted under STND.DFLT.26, PRIME.8 requires an authorized estimate." No text dissolves this. | Q1. Make AGENT.6 conditional on the cost being measurable (CC21). |
| R1.2 Builds, generators, and incremental edits are reserved | CC2 (Partly), CC14 (Partly) | CC2 holds for writes that cannot be named in advance, such as caches and installs. An output directory can already be listed, because a directory "counts as its contents" (term Bulk item). CC14 holds unless an entry records a checkpoint mechanism, which the fifth exempt class of STND.DFLT.15 accepts. | Q2. GUARD.5 and GUARD.6 stay. |
| R1.3 Working bounds leave out caches, tool state, and the system temporary directory | CC3 (Confirmed) | Writes are bounded "by default, the top directory of the work". A configuration that the agent is unable to alter can open more, but the default opens nothing else. | Add CC3's text to the term Working bounds. |
| R1.4 A first install or retrieval halts with no proposal of the set | CC8 (Partly), CC18 (Confirmed) | PRIME.7 makes the first halt inherent. PRIME.14 already lets the referral recommend a standing authorization, so the gap is only that no provision asks for the set. The STND.PROJ.3 table has no row for reading from a private remote. | New STND.DFLT provision: the first referral for an action of a class in the table of STND.PROJ.3 proposes each standing authorization in that table that the work needs. It cites the table and does not copy it. Add a row to STND.PROJ.3 for reading from a recorded private remote. |
| R1.5 An unlisted asset halts work | CC29 (Unchecked) | — | Cite the STND.THRT term Asset, and limit STND.DFLT.19 to irreplaceable data, hardware, and outside systems written to. |
| R1.6 Dependency review of every direct dependency | CC13 (Confirmed) | STND.DFLT.11: "every direct dependency". | Change to "each dependency that the unit changes". |
| R1.7 Citation in STND.DFLT.5 | CC27 (Refuted) | See the table of refuted findings. | Optional: add PRIME.2 to the citations. |

## Round 2: human round trips at CSQ3 and CSQ4

| Entry | Sources (status) | Verified | Change |
| --- | --- | --- | --- |
| R2.1 The owner writes ledger lines by hand | CC6 (Confirmed) | Under STND.DFLT.5, an agent "SHALL NOT append an entry that names the human owner as actor". Only grants have the scribe route of STND.DFLT.17. Classification (STND.DFLT.13), continuation (STND.DFLT.9), promotion, and release each need an entry in the owner's name, and GOV.38 means no work may depend on the harness to write it. | Q3. Generalize STND.DFLT.17 and STND.DFLT.23 as CC6 proposes. |
| R2.2 The first parallel delegation needs a baseline or an owner decision | CP8 (Confirmed), CC16 (Confirmed) | AGENT.39 asks for "a measured baseline or a recorded decision of the human owner". The AGENT Notes bind AGENT.39 at every class "until the custodians interpret GOV.11". | Add "an estimate grounded under STND.CREW.7" as a basis (CP8). LVL1 only. |
| R2.3 Per-result promotion at CSQ3 | CC5 (Partly), CP19 (Partly), CC17 (Confirmed) | QA.11 makes relying on an unpromoted result "beyond its author" a blocking defect. A Result is "a number, dataset, figure, or deployed configuration", so code that teammates build on goes through review, not promotion; that part of CC5 is overstated. GOV.12 sets the CSQ3 boundary at the "immediate team", while STND.CLASS.1 sets it at "actors of the same unit of work". | Q4. Use "reclassification" for a change of class in new text, and keep "promotion" for results (CP19). |
| R2.4 Who counts as an independent reviewer | CP9 (Confirmed), CP10 (Confirmed), CP21 (Unchecked) | The term Agent configuration covers "the model, the instruction revision, and the tools", so a change of tools alone meets the CSQ2 row. Whether a second session of one configuration is "an actor other than the author" (CSQ3 row) is not stated. | Q5. Define the terms in STND.CLASS. |
| R2.5 Owner attention that the next report can carry | CC15 (Confirmed), CC22 (Confirmed), CP11 (Unchecked), CP14 (Confirmed), CP20 (Unchecked), CS9 (Confirmed) | STND.CLASS.7 asks for a reassessment at each reported scenario. STND.THRT.6 asks for a proposal at each new source. HW.1 has six attributes, each a change of the classification. STND.CREW.23 makes a new session after each retrieval. | Apply the reviewers' fixes: reassess before the next reliance at a more severe class (CC15); treat a proposal as an item of the next work report (CC22); batch QA.5 reports (CP11); accept a fresh context as a new session (CP14); send findings with the GOV.47 report (CP20); reduce HW.1 to one attribute (CS9). |
| R2.6 Run-time reports, network records, and release by team use | CS8 (Confirmed), CC19 (Confirmed), CP16 (Confirmed) | STND.CLASS.10 starts reports to the operator (INTPR.7) at CSQ1, but HW.19, HW.21, HW.CPU.5, and NUMER.18 apply them from CSQ3, and an unattended run has no operator. AGENT.23 asks for a seven-item record of each access from CSQ3. Whether a branch that the team pulls from is a main line is undefined. | Q11. |
| R2.7 Revisions of the hazard analysis | CS13 (Confirmed) | PRIME.13 has the owner adopt the hazard analysis before hardware is first driven. The fix would touch the floor. | Q11 recommends keeping it: physical safety is a prime directive. |

## Round 3: expected class and the promotion path

| Entry | Sources (status) | Verified | Change |
| --- | --- | --- | --- |
| R3.1 Class at inception and the expected class | CC4, CC32, CP1, CL26 (where recorded), CS12, CC9 (Partly), CC10 (all Confirmed unless marked) | GOV.13 sets the class "as the most severe class of its intended uses". GOV.14 and the STND.CLASS reading say the class follows present use. Under GOV.9, the restrictive reading of GOV.13 governs. No record holds a class that the work will reach. On CC9, the STND.DFLT Notes already treat unclassified work as relied upon by no one beyond its author, but the trigger "needs it" in GOV.13 stays undefined. STND.CLASS.3 asks every CSQ4 classification for a money threshold. | Q6. Add the expected class to STND.CLASS.5 and to the Classification row of STND.PROJ.1. Limit STND.CLASS.3 to CSQ2 and more severe classes (CC10). |
| R3.2 Design anticipates the expected class | CC32, CL26, CS12 (Confirmed), CL21 (Partly) | No provision lets a known later class shape choices that are costly to change: edition, subset, failure channel, dependencies, hardware, reduction order, a kept reference path. SIMPL.3 defers generality unless the owner records the requirement, which an expected class would do. STND.CODE.20 asks for the deviation record "CSQ4 included", so the severe class's record arrives early (the custodian ratified this onset for C++). | Q7. |
| R3.3 What a reclassification owes | CC7 (Partly), CP2 (Partly), CL12 (Partly), CS11, CC11 | GOV.14: "nothing is grandfathered". No text says whether past changes are reviewed one by one or as one change set. "Change" is undefined, so a review of the cumulative change is not barred, but nothing says so. The transition rule stands in four informative Notes (JL, PY, RUST, STDC), not the five that CL12 counts. Checks tied to an event (a first load, a submission for fabrication) cannot be met after the event. STND.CLASS.19 audits even before CSQ4 work becomes CSQ3. | Q8. |
| R3.4 Cheap records kept below the expected class | CC12, CP3 (Partly), CL11 (Partly), CS3, CS10 (Partly) | QA.1 (floor) already records acceptance criteria before work is executed, at every class, so part of CP3 and CS10 is met. What CSQ4 loses: tolerance bases, seeds and environment identity, lock files outside the source and toolchain revisions (REPRO.5 already keeps the lock files inside the source), sources of expected test values, and raw observations and quantum-processor jobs, which cannot be repeated. | Q9. |

## Round 4: one onset rule with per-provision onsets

| Entry | Sources (status) | Verified | Change |
| --- | --- | --- | --- |
| R4.1 Two onset rules, and readings case by case | CS1, CS4, CS5, CS6, CS18, CP12, CL1, CL2 (Confirmed or Unchecked) | NUMER and the profiles use the whole provision "from the least severe class at which those criteria require an LVL0 obligation it instantiates". The standards apply "the part of a provision that rests on a row … from the class of that row". The DSGN.4 and DSGN.5 rows then put rules of code form (STND.CXX.6, STND.CXX.7, STND.RUST.24, STND.FTN.6) and the catch of a failure that crosses a foreign frame (STND.CODE.24) at CSQ2. The STND.TEST Notes leave "This reading is put to the custodian" in adopted text. | Q10. Each onset becomes a front-matter field that is rendered beside the mode, and each Notes paragraph on class becomes one citation of STND.CLASS.10. |
| R4.2 Methods standards without, or too wide, a CSQ3 tier | CP5 (Confirmed), CP4 (Partly), CP6 (Partly), CS2 (Partly) | STND.VVUQ never cites STND.CLASS. For CP4, the Notes start STND.WFLOW.15 at CSQ1 and the first sentence of STND.WFLOW.6 at CSQ2; the rest is CSQ3 as claimed. For CP6, a full-suite cadence of one merge under STND.TEST.6 already takes each merge out of the selection and its reason, and STND.TEST.5 draws every tier into the development line. For CS2, HW.5 to HW.7 bind only for reported results, and HW.5 fills a contract that HW.4 starts at CSQ2, which is incoherent. | Q10: each standard names a short CSQ3 core in its next round. |

## Round 5: harness dependence and ledger form

| Entry | Sources (status) | Verified | Change |
| --- | --- | --- | --- |
| R5.1 Rehearsal and the review of conflict candidates | CP7 (Partly), CP23 (Confirmed) | STND.HARN.24 binds only "a script", so a change made by hand needs no rehearsal. STND.HARN.28 binds "a harness", so without one it lapses rather than blocks. Both reach only adoptions of governance documents, not project work. The Note "An agent of a different agent configuration … performs that review" is an obligation stated in the indicative. | Restate .24 and .28 as outcomes that a reader is able to check (CP7 text). Replace the Note with a citation of STND.HARN.28. |
| R5.2 STND.HARN reaches the project work ledger | CP18 (Confirmed) | STND.HARN.6: "Each ledger SHALL be …". STND.HARN.7 adds the "ledger" field "only outside the governance ledger", which places every work ledger under the harness schema and serialization, against the lighter STND.DFLT.5. | Q3. |
| R5.3 "Read-only" purpose | CP22 (Confirmed) | The Purpose says "serves governance read-only", but LEX.harness says it "enters transactions". | CP22 text. |
| R5.4 Stale note on derived configuration | CC28 (Confirmed) | STND.INSTR Notes: means "derived from it and from STND.DFLT", which STND.HARN 1.4 withdrew. | CC28 text. |

## Round 6: restatement cleanups (GOV.31)

| Entry | Sources (status) | Change |
| --- | --- | --- |
| R6.1 LVL0 restating itself | CC23, CC24, CC31 (Unchecked); CC25, CC26 (Confirmed) | Keep each rule once (GOV.50, GOV.6, GOV.9, GUARD.15) and cite it elsewhere. This is editorial text in the floor documents. |
| R6.2 Language copies of STND.CODE and STND.DEPS outcomes | CL4, CL5, CL6, CL17, CL23 (Confirmed); CL3 (Partly); CL7, CL8, CL10, CL13, CL16, CL18, CL24, CL25 (Unchecked) | One provision in STND.CODE or STND.DEPS for each outcome. Each language standard keeps only the sentence that names a construct of its language. For CL3, STND.CODE.6 already binds in every language that no execution setting removes an untrusted-input check, which narrows the gap to the checks of CPS.5 and CPS.9. Where the mode differs (CL3, CL23, CL24), see Q12. |
| R6.3 Copies in the systems standards | CS7, CS16, CS19 (Confirmed); CS14 (Partly) | Withdraw STND.MPI.18, .19, and .24 for STND.CONC. Keep the first sentence of STND.OFFLD.31 (completion of offloaded work, which is offload content) and withdraw only its second sentence. Align STND.PERF.18 with MEAS.7. Have STND.OFFLD.27 cite STND.CONC.24. |
| R6.4 Copies in the process standards | CP13 (Confirmed), CP26 (Unchecked) | Scope agent self-records out of STND.WFLOW. Have STND.WPROC.13 cite AGENT.47, and merge the spelling table of STND.DRAFT.33 into STND.DOCS.8. |

## Round 7: the rest

| Entry | Sources (status) | Change |
| --- | --- | --- |
| R7.1 Stale or broken text | CP17, CS20, CS21, CL15, CL22, CP24, CS15, CL14 (Confirmed); CP25, CS22, CP27 (Unchecked) | Fix or remove the missing research path in STND.VVUQ (no such file exists, now or in history). Correct the MPI path. HDES cites STND.SV. Remove the narration of drafting and the versions in Notes. STND/_doc.md: standards "name no product, vendor, or version". Agnosticism: Q12. |
| R7.2 Small burdens and gaps | CC20, CP15, CP28 (Confirmed); CL19, CL21 (Partly); CC30, CL9, CL20, CS17 (Unchecked) | Adopt STND.DFLT by one citation (CC20). State the protocol for writes to shared records (CP15). Add "where the adopter is not the author" to STND.IDENT.13 (CP28). Open STND.FTN.4 and STND.CODE.5 with "Where the means of the work include" (CL19, a convenience, not a blocker). Correct the Notes on STND.CODE.20 (CL21; handled under Q7). |
| R7.3 Found by this verifier | — | STND.CREW.23 is marked binding but uses "SHOULD". Make it a default, or give it the modal of an obligation. |

## Refuted findings

| Finding | Refuted claim | Reason |
| --- | --- | --- |
| CC27 | "PRIME.7 … says nothing of ledger entries" | PRIME.7 says an authorization is "NEVER granted … by an agent for itself". An entry that names the owner as grantor is how an agent would grant itself one, and the STND.DFLT Notes rely on this ("STND.DFLT.5 and PRIME.7 bar a forged entry"). The citation is apt. Adding PRIME.2 is optional. |
| CL19 (in part) | Kind "blocker" | STND.FTN.4 and STND.CODE.5 are defaults ("SHOULD"). An unmet default halts nothing, and a recorded decision replaces it (GOV.19). The finding holds only as a convenience. |
| CL21 (in part) | STND.CODE.17 and .19 are the one default that uses "SHALL" | STND.CLASS.10 and STND.CLASS.18 are defaults written with "SHALL", and STND.DRAFT sets no modal for defaults. The ambiguity of the STND.CODE.20 Notes holds. |
| CP4 (in part) | STND.WFLOW.15 and the first sentence of .6 apply at CSQ3 | The STND.WFLOW Notes start .15 at CSQ1 (INTPR.8) and the first sentence of .6 at CSQ2 (QA.14). |
| CP6 (in part) | A cheap full suite at CSQ3 must be selected, or each run must give its reason | A cadence of one merge under STND.TEST.6 makes each such run a full-suite run, outside STND.TEST.10. |
| CS14 (in part) | STND.OFFLD.31 repeats STND.PERF | Its first sentence, ending the timing at observed completion, is offload content and holds outside a performance evaluation. |
| CC5 (in part) | Every CSQ3 output that a teammate builds on needs promotion | Promotion governs results (a number, dataset, figure, or deployed configuration). Code is reviewed under QA.7. |
| CL12 (in part) | Five Notes carry the transition rule | Four do (JL, PY, RUST, STDC); STND.FTN has none. |

## Custodian questions

Each question gives the options and my recommendation. Every recommendation keeps the prime directives as written.

1. **Operating cost (R1.1).** Should the agent's own operating cost be authorized by (a) one standing operating envelope that the agent proposes in its first plan and the owner approves once per project, scribed as in Q3; (b) a ruling that an enforced account cap the owner provisioned is that envelope; or (c) an amendment to GUARD.14 that makes the owner's direction to run a unit its authorization? I recommend (a): PRIME.8 and the floor stay as written, at the cost of one act per project.
2. **Builds and edits (R1.2).** Should (a) a versioned tool configuration that names a tool's outputs, within the work or a temporary location, count as the enumeration of STND.DFLT.24, and should the first exempt class read "last committed state verified recoverable"; (b) the term Destructive action exclude regenerable outputs; or (c) nothing change? I recommend (a): GUARD.5 and GUARD.6 are untouched.
3. **Work ledger (R2.1, R5.2).** Should (a) an agent enter each act that the owner gives it directly, quoting the act, with the owner as its actor and the agent as scribe, accepted for work that is not assured, in the form of STND.DFLT.5, with STND.HARN.6 and .7 limited to the governance ledger and to ledgers that a harness is asked to read; (b) the scribe route stay for authorizations only; or (c) (a) with STND.DFLT.5 citing STND.HARN.7? I recommend (a).
4. **Promotion at CSQ3 (R2.3).** Should (a) QA.11 be amended so that, for CSQ3 and CSQ4, the adopted classification entry promotes each result relied upon only within the CSQ3 reliance test, with that test widened to the immediate team as GOV.12 says; or (b) per-result promotion remain, within the unit of work? I recommend (a), a minor LVL0 amendment outside the floor.
5. **Reviewer identity (R2.4).** Should (a) any agent session other than the author's count as another actor at CSQ3, its configuration included, while CSQ2 needs a different model or instruction revision and tools alone do not suffice; (b) CSQ2 need a different model; or (c) a difference of tools suffice? I recommend (a): (b) forces a human review in environments with one model, and (c) empties the CSQ2 row.
6. **Class at inception (R3.1).** Should GOV.13 (a) be amended so that the class at inception is that of the uses then made, a planned more severe use is recorded in the classification as an expected class (drafted by an agent and adopted with the classification, with no separate act), and unclassified work meets the floor until its first promotion, release, deployment, or actuation; (b) be read that way by a ruling under GOV.3; or (c) stand, with a planned use setting the class now? I recommend (a): GOV.14 still has every obligation met before reliance, so the floor is not lowered.
7. **Anticipating design (R3.2).** Should (a) one STND.CLASS default, which STND.CODE, HW, and STND.CONC cite, have design not preclude the parts of the expected class (contracts, schemas, provenance, edition, subset, failure channel, dependencies, hardware, reduction order, reference path), with the reason in a decision record and no record of that class owed before reclassification, and with the deviation record of STND.CODE.20 moved to CSQ1 and only its marker kept earlier; (b) the same through separate provisions in each standard; or (c) advice in the Notes only? I recommend (a), which revisits the onset of STND.CODE.20 that was ratified for C++.
8. **What reclassification owes (R3.3).** Should (a) one STND.CLASS provision require, before reliance at the new class: regeneration of results that lack recorded inputs; the label "unverified" on results judged by criteria set after they were seen (QA.12); one review of the accumulated changes at the new independence; an audit only when the work moves to CSQ2 or a more severe class; each check tied to an event repeated before reliance; and conformance of form-only defaults when a change next touches the code; or (b) should each past change be reviewed and all code brought to the new onsets at once? I recommend (a), which meets GOV.14 because everything is met before reliance.
9. **Cheap records (R3.4).** Should CSQ4 work (a) keep, where the classification records an expected class, the tolerance basis, seeds and environment identity, lock files and toolchain revisions, the sources of expected test values, and raw observations and quantum-processor jobs that cannot be repeated, as SHOULD defaults; (b) get Notes advice only; or (c) keep them always? I recommend (a): the owner's entry of an expected class is the "recorded project decision naming the consequence" that GOV.11 asks for before the floor is raised.
10. **Onset rule (R4).** Should onsets (a) apply per part, from the STND.CLASS.10 row whose named item the part asks for and otherwise from CSQ3, so that code form and the catch at foreign frames move to CSQ3, held in a front-matter field per provision, with each methods standard naming a short CSQ3 core (STND.VVUQ, STND.WFLOW run machinery, STND.TEST records, HW contract evidence to CSQ2); (b) apply to the whole provision from the least severe class of any obligation it instantiates; or (c) stay in the Notes as they are? I recommend (a), which also accepts the STND.WFLOW.35 bundle and the statement route of STND.TEST.2.
11. **Below CSQ1 (R2.6, R2.7).** Should (a) a report to the operator be met by the record of the run where no operator acts during it, a per-access network record be met by a session transcript that the agent did not edit, and a branch drawn on only within development not count as a main line, while the owner keeps adopting revisions of the hazard analysis under PRIME.13; or (b) all of these stay as written? I recommend (a).
12. **Language and agnosticism (R6.2, R7.1).** Should (a) each outcome be ruled once for every language, in one STND.CODE provision, with the finite-value option binding only for checks that the floor requires (PRIME.4), STND.CODE.14 carrying the forms of each language, and a library log record never the only visible degradation, while named documents (Core Guidelines, numpydoc) move to the repository configuration and specification revision numbers leave the Notes; or (b) the per-language rulings and names stay, with a reason in the Notes? I recommend (a).
