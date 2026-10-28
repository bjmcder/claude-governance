# Round c of 2026-10-28: classes, the expected class, promotion, and the round trips below CSQ2

This round carries rulings C1 to C6 and C8 of `review-records/deep-review-2026-10-28/rulings.md`, each on the reading given in its section "Rulings of the custodian, 2026-10-28", and the register entries R2.2 to R2.7, R3.1 to R3.4, and R7.3. The module is `tools/amendment-scripts/apply_round_c_2026_10_28.py`, with the helpers `round_c_class.py` (LVL0, STND.CLASS, STND.PROJ) and `round_c_rest.py` (the rest), run through `apply_rounds_2026_10_28.py` after rounds a and d. Twenty-one transactions, in citation order: LVL0 1.7, STND.CLASS 1.4, STND.PROJ 1.4, STND.CODE 1.5, HW 1.2, HW.CPU 1.1, HW.GPU 1.1, HW.QPU 1.1, HW.EMBED 1.1, HW.FPGA 1.1, HW.ASIC 1.1, NUMER 1.4, STND.CONC 1.1.2, AGENT 1.3, STND.CREW 1.2, STND.THRT 1.1, STND.WPROC 1.2, STND.JL 1.4.1, STND.PY 1.3.1, STND.RUST 1.3.1, STND.STDC 1.3.1. Nothing here is in force until the custodian ratifies it and the script runs.

## The LVL0 amendment

LVL0 goes from 1.6 to 1.7 by a transaction in the form of entries 30 and 46 of `harness/governance/ledger.jsonl`: type `amend`, actor The Custodian, role custodians, authority GOV.40, targets LVL0 with GOV.13 and QA.11, scope the thirteen LVL0 folders, and a rationale that states the reading, the alternatives weighed, the class, the lower governance affected, and the proposal (GOV.40). The LVL0 text that changes:

**GOV.13, Class assignment**, old: "The human owner sets the project's consequence class at inception, as the most severe class of its intended uses, and MAY revise it throughout the project's life. The human owner MAY record a less severe class for a component shown to be isolated from the more severe outputs. No class is assumed by default: where none is recorded, an agent that needs it halts that line of work and refers (PRIME.14)."

New:

> The human owner sets the project's consequence class at inception, as the most severe class of the uses then made of its outputs, and MAY revise it throughout the project's life. Where a more severe use is planned, the classification records the class of that use as the expected class, adopted with the classification (GOV.24) and setting no class before that use begins (GOV.14). The human owner MAY record a less severe class for a component shown to be isolated from the more severe outputs. No class is assumed by default: where none is recorded, the work meets the floor (GOV.10), and an agent that needs the class to promote, release, deploy, or drive physical hardware halts that line of work and refers (PRIME.14).

Why it is minor and lowers no floor: the first sentence changes which uses set the class at inception, from "its intended uses" to "the uses then made of its outputs"; a planned use no longer sets the class now, but GOV.14 is unchanged and still has every obligation of a class met before the work is relied upon at that class, so the obligations of the planned class arrive before anyone relies on the work at it. The second sentence adds one entry to the classification, which the human owner adopts in the same act (GOV.24, GOV.50), and gives it no force until the use begins. The last sentence names the trigger of "needs it" (CC9): unclassified work meets the floor (GOV.10), which it met anyway, and nothing relies on an unpromoted result beyond its author (QA.11), so letting floor-level work proceed before the classification lowers nothing; the agent still halts before a promotion, a release, a deployment, or a command to hardware. No prime directive or principle changes in motivation or intent (STND.IDENT.3, minor).

**QA.11, Promotion**, one sentence inserted before "An agent MAY propose a promotion.":

> For work of CSQ3 or CSQ4, the adopted classification is the promotion of each result that meets its acceptance criteria (QA.1), for reliance by its author or immediate team alone, feeding work that is verified later (GOV.12).

Why it is minor and lowers no floor: QA.11 is outside the floor (GOV.10). The standing promotion reaches only reliance within the CSQ3 test as GOV.12 writes it, by a result that meets the acceptance criteria that QA.1, in the floor, records before the work at every class; a result that fails them is not promoted, and reliance beyond the immediate team, or not through verified work, still needs its own promotion. The rest of QA.11 is unchanged, so "relying on one beyond its author is a blocking defect" now reads with the classification as the promotion of team reliance.

**Lexicon**, two terms added, in the group Governance: *Expected class*, "The consequence class, more severe than the class of the work, of a use of the work that the classification records as planned; it sets no class before that use begins." (governed by GOV.13, GOV.14); *Reclassification*, "A revision of the classification that moves the consequence class of the work, or of a component, to another class." (governed by GOV.14, GOV.24). GOV.13 introduces the first term, and lower governance uses a Lexicon term without redefining it; the second fixes the word that new text uses for a change of class, keeping "promotion" for a result (CP19). Defining a term for a sense the provisions use is editorial on its own (STND.IDENT.3); it rides on the minor amendment.

## Rulings carried

### C1. Class at inception and the expected class (R3.1)

**Reading drafted.** Option (a): the class at inception is that of the uses then made; a planned more severe use is recorded in the classification as the expected class, drafted by an agent and adopted with the classification, with no separate act; unclassified work meets the floor until its first promotion, release, deployment, or actuation (CC9); STND.CLASS.5 and the Classification row of STND.PROJ.1 gain the expected class; STND.CLASS.3's money threshold applies from CSQ2 (CC10). GOV.13 as above.

**STND.CLASS.5, second sentence added:** "Where a more severe use of the project or of a component is planned, the classification SHALL state its expected class and the use that would occasion it (GOV.13, GOV.24)."

**STND.CLASS.3:** "Where the classification records CSQ2 or a more severe class for the project or a component, the classification SHALL state the amount of money above which a loss counts as a cost for the consequence test of CSQ1 in the table of STND.CLASS.1 (GOV.24)."

**STND.PROJ.1, Classification row:** "… the consequence class (GOV.13); where a more severe use is planned, the expected class and the use that would occasion it (GOV.13); the proportionality judgment (GOV.11)". The STND.PROJ Notes say the entry is drafted by an agent with the rest of the classification and adopted with it, sets no class until the use begins, and is what STND.CLASS.21 and STND.CLASS.23 read.

The STND.CLASS Notes say that a project that plans a published result begins at CSQ4 or CSQ3 and reaches CSQ2 by reclassification before the result is relied upon at that class; that the expected class is drafted with the classification and adopted with it in one act (GOV.50); and that the human owner's entry of it is the recorded project decision naming the consequence that GOV.11 asks before lower governance raises the floor (C4).

### C2. Design for the expected class (R3.2)

**Reading drafted.** Option (a): one STND.CLASS default, cited by STND.CODE, HW, and STND.CONC; where the classification records an expected class, design does not preclude the parts of that class (contracts, schemas, provenance, edition, subset, failure channel, dependencies, hardware, reduction order, a kept reference path); the reason for each choice the expected class drives goes in a decision record; no record of the expected class is owed before reclassification; the custodian's "minimize the upfront burden but enable design for upgrade". The deviation record of STND.CODE.20 moves to CSQ1, and only its marker is kept earlier.

**New STND.CLASS.21, Design for the expected class (default: DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7):**

> Where the classification records an expected class, the design of the work SHOULD admit, without rework of the design, the parts of the table of STND.CLASS.10 that apply from that class, and the contracts, schemas, provenance, language edition and subset, failure channel, dependencies, hardware, reduction order, and kept reference path that the obligations of that class ask of the work, with the reason for each choice that the expected class drives recorded in a decision record (DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7). Before the reclassification, the work MAY omit each record that only an obligation of the expected class requires, other than the records of STND.CLASS.23 (GOV.11).

"Admit, without rework of the design" is the ruling's "does not preclude" in the positive, because "SHOULD NOT preclude … nor …" over a list is a negated list (STND.DRAFT.15, g.11); it is also DSGN.13's word. The parts are named generically, not by the LVL2 provisions that hold them, so that STND.CLASS cites no language or systems standard; the citing documents name their own parts. STND.CLASS.10 excepts STND.CLASS.21 from what work of CSQ4 omits (see C4), because most work with an expected class starts at CSQ4 and a default that CSQ4 omits would enable nothing.

**STND.CODE.20, Recorded high-assurance deviations:**

> For work of CSQ1 or CSQ0, each deviation from a rule of the high-assurance coding standard of STND.CODE.17 SHALL be recorded as the deviation procedure of that standard requires, at its location under one marker that the repository configuration names or in a decision record that the location cites, with the identifier of the rule, the reason, and the evidence that the code stays correct (REPRO.7). Other work that adopts such a standard SHOULD mark each deviation at its location under that marker (REPRO.7).

**This revisits an onset the custodian ratified.** The STND.CODE Notes said: "STND.CODE.20 applies wherever a high-assurance coding standard is adopted, CSQ4 included, though STND.CLASS.10 lets work of CSQ4 omit an obligation above the floor. The custodian ratified these onsets for C++ with the provisions on high-assurance code that STND.CXX 1.1 held … and for C through STND.STDC.1." The Notes now say that the record applies from CSQ1 with STND.CODE.17 and STND.CODE.19, that the marker alone applies wherever such a standard is adopted, that the record was ratified as applying wherever such a standard is adopted, and that revision 1.5 moves it to CSQ1 under the custodian's ruling of 2026-10-28 (CL21, CL26). The rationale says the same. The Notes also cite STND.CLASS.21 for the subset, the edition, the failure channel, and the dependencies, and say that the marker is the one thing kept earlier, so that the reclassification finds each deviation by a search and writes the record STND.CLASS.22 then owes once.

**HW Notes** cite STND.CLASS.21 for the hardware, the reference path (HW.15), the reduction order, and the bounds (HW.20). **STND.CONC Notes** (editorial) cite it for the combination order of STND.CONC.22 where an acceptance criterion of the expected class asks bitwise identity across numbers of tasks. The citations are in the Notes, because the default applies to every project by STND.CLASS itself and a provision that repeated it would restate (GOV.31).

### C3. What a reclassification owes (R3.3)

**Reading drafted.** Option (a): one STND.CLASS provision, met before reliance at the new class: regenerate results that lack recorded inputs; label "unverified" the results judged by criteria set after they were seen (QA.12); one review of the accumulated changes at the new independence; an audit only on a move to CSQ2 or a more severe class; each check tied to an event repeated before reliance; form-only defaults met when a change next touches the code. STND.CLASS.19's audit is limited accordingly. The transition rule of the four language Notes is replaced by a citation, since round d left those paragraphs.

**New STND.CLASS.22, Reclassification obligations (binding: GOV.14, REPRO.1, QA.12, QA.7, GOV.47, GOV.42):**

> Before work is relied upon at a more severe class, the obligations of that class SHALL be met for the work done at the less severe class by these steps (GOV.14):
>
> - the regeneration of each result whose record lacks an input of REPRO.1 (REPRO.1);
> - the label unverified on each result judged against criteria set after it was seen (QA.12);
> - one review, at the independence of the row of the new class in the table of STND.CLASS.18, of the changes made since the last review at that independence, taken as one change (QA.7);
> - the audit that STND.CLASS.19 requires before the reliance (GOV.47);
> - the repetition, before the reliance, of each check that an obligation of the new class ties to an event that preceded the reclassification (GOV.14);
> - the conformance of existing source to each default of form or style that first reaches it, at the next change that touches that source (GOV.42).

One modal: the list is what the reclassification owes for past work, and no more; the obligations of the new class apply to each later change as STND.CLASS.10 gives them. GOV.14 is met because every step is taken before the reliance.

**STND.CLASS.19, second sentence:** "Before work is relied upon at CSQ2 or a more severe class, the project SHALL be audited by the auditor of that class (GOV.47)." The step from CSQ4 to CSQ3 no longer needs an audit (CC11); GOV.47 asks only an interval proportioned to the class.

**The four language Notes** (STND.JL, STND.PY, STND.RUST, STND.STDC, each editorial): "Existing Julia source that a default of form or style first reaches conforms as STND.CLASS.22 provides, at the next change that touches it; GOV.42 governs the transition for every other provision." STND.PY keeps its exception for the strict checking of STND.PY.5. The last item of STND.CLASS.22 says "first reaches", so that it covers the adoption of a standard as well as a reclassification, which the Notes sentence covered; it instantiates GOV.42 for that reach, and the custodians' adoption of the provision is the recorded transition period for defaults of form or style. STND.FTN has no such sentence (CL12 counted five; four hold).

### C4. Cheap records below the expected class (R3.4)

**Reading drafted.** Option (a): where the classification records an expected class, CSQ4 work keeps, as SHOULD defaults, the tolerance basis, seeds and environment identity, lock files and toolchain revisions, the sources of expected test values, and raw observations and quantum-processor jobs that cannot be repeated; the provisions that hold each record at CSQ3 are cited, not restated; the human owner's entry of an expected class is the "recorded project decision naming the consequence" of GOV.11.

**New STND.CLASS.23, Records below the expected class (default: REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3):**

> Where the classification records an expected class, and a provision of the table of this provision would apply to the work at that class, work of CSQ4 SHOULD keep the record of that row as the provision describes it (REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3).
>
> | Record | Provision |
> | --- | --- |
> | The basis of each tolerance | NUMER.11 |
> | The random seeds and the identity of the computational environment of each result | REPRO.1 |
> | Each lock file | STND.DEPS.12 |
> | Each toolchain revision | STND.DEPS.8 |
> | The source of each expected test value | STND.TEST.19 |
> | Each observation that is unable to be acquired again, as acquired, with its acquisition record | MEAS.3, MEAS.4 |
> | Each job on a quantum processor, with its execution record | HW.QPU.3 |

"Would apply to the work at that class" keeps a profile's record (NUMER.11, MEAS.3, HW.QPU.3) to work whose expected class and selection would bring that profile; REPRO.1 applies at CSQ3 by STND.CLASS.10.

**STND.CLASS.10, second sentence:** "Work of CSQ4 MAY omit every obligation of these Articles above the floor, other than STND.CLASS.21 and the records of STND.CLASS.23 (GOV.11)." Without the exception the two defaults would be omitted at CSQ4 by the provision that defines CSQ4's omission.

**The GOV.11 argument.** GOV.11: "lower governance SHALL NOT raise the floor except by a recorded project decision naming the consequence that warrants it." STND.CLASS.21 and STND.CLASS.23 reach work of CSQ4 only where the classification records an expected class. That entry is recorded (GOV.36), it is the human owner's own act (GOV.50, GOV.13), and it names the consequence: the class the work is expected to reach, which is the consequence class of the planned use. So the two defaults apply at CSQ4 by a recorded project decision naming the consequence, as GOV.11 allows, and work with no expected class stays as light as before. The STND.CLASS Notes and the rationale say so.

### C5. Promotion at CSQ3 (R2.3)

**Reading drafted.** Option (a): QA.11 as above; STND.CLASS.1 aligned with GOV.12; "reclassification" for a change of class, "promotion" for results (CP19).

**STND.CLASS.1, CSQ3 reliance test:** "Only the author, or the actors of the author's immediate team, rely on the output, and only through work that is verified before it is relied upon." The STND.CLASS Terms define *Team*: "The actors, persons and agents alike, that act on the work under the direction of its human owner; an author's immediate team is the team of the work on which the author acts." GOV.12 uses the words without defining them; the term is "Team" rather than "Immediate team" because STND.DRAFT.29 lists "team" as an undefined role word that a document's own Terms may define (g.19), and the definition is put to the custodian below.

The STND.CLASS Notes say that for work of CSQ3 or CSQ4 the adopted classification is the promotion of each result that meets its acceptance criteria for reliance within the CSQ3 test as GOV.12 writes it, so that no result is promoted one by one below CSQ2, and that reliance beyond that test needs its own promotion. STND.CLASS.20 is unchanged: a promotion still cites the classification entry, and the standing promotion is that entry.

### C6. Who counts as another actor (R2.4)

**Reading drafted.** Option (a): at CSQ3, any agent session other than the author's counts, its configuration included; at CSQ2, a different model or a different instruction revision, since a difference of tools alone does not suffice. The terms CP9 and CP10 show undefined are fixed in STND.CLASS, where STND.CLASS.18 uses them.

**STND.CLASS.18, CSQ3 row:** "An actor other than the author: a human, or an agent in an agent session other than each session of the author, of the author's agent configuration or another (QA.7)." **CSQ2 row:** "An actor not directed by the author performs the review; where the author is an agent, that actor is a human or an agent whose agent configuration differs from the author's in its model or in its instruction revision, whatever its tools." **Term Agent session** (STND.CLASS): "One run of an agent from its start to its end, whose context holds nothing of another run except what it reads from the records of the work." The Notes give the reasons: a session that holds nothing of the author's reasoning examines the change cold; a difference of tools alone leaves the same model reasoning under the same instructions.

### C8. Reports to the operator, network records, main lines, the hazard analysis (R2.6, R2.7)

**Reading drafted.** Option (a) for the first three; PRIME.13 kept.

**Reports to the operator (CS8).** HW.19, HW.21, HW.CPU.5, and NUMER.18 each report "to the operator of a run during which one acts and otherwise in the record of the run". The clause is worded without a condition word after the modal (STND.DRAFT, g.12); one wording in four provisions rather than a defined term, because a term would fix the meaning of a verb phrase. HW.19: "the path SHALL report the fallback at its first occurrence in the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.7)." HW.21: "… and report each overrun to the operator of a run during which one acts and otherwise in the record of the run (RSRC.2, RSRC.3, INTPR.7)." HW.CPU.5: "the path SHALL report the excess at its first occurrence in the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.7, RSRC.2)." NUMER.18: "the departure SHALL be reported during the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.10, INTPR.7)." The HW, HW.CPU, and NUMER Notes say that an unattended run has no operator to receive a message and its record is what a reader examines afterward.

**Network record (CC19). AGENT.23, second sentence:** "Where the provisioned environment records a network access with these items in a record that the agent is unable to alter, or a transcript of its session that the agent did not edit shows the access, with each of these items that the transcript lacks stated once for the session or beside the access, an agent MAY cite that record or transcript in place of its own (REPRO.11)." The AGENT Notes say that a transcript shows each access with its address, its time, and the direction of transfer, and that the items it lacks, the authorization relied on and the access descriptor among them, hold for every access of the session and are stated once, so that an agent at CSQ3 writes no seven-item record before each next step.

**Main line (CP16).** Defined where the term is defined, the STND.WPROC Terms: "Main line | Each branch from which the work is released or deployed; a branch drawn on only within development, for the reliance that the CSQ3 reliance test of STND.CLASS.1 admits, is not one." The Notes say that a push to such a branch is no release decision and that an agent merges into it as STND.WPROC.11 provides; they avoid the word "team", which STND.DRAFT.29 flags outside a document that defines it (g.19).

**PRIME.13 (CS13).** Kept: the human owner still adopts each revision of the hazard analysis; CPS.3 is unchanged. The ruling keeps it because physical safety is a prime directive.

## Register entries carried

| Entry | Sources | Drafted |
| --- | --- | --- |
| R2.2 | CP8, CC16 | AGENT.39: "… and, from a measured baseline, an effort estimate under AGENT.6 that states its basis, or a recorded decision of the human owner, that running the units together takes less time or operating cost …". CP8 proposed "an estimate grounded under STND.CREW.7"; no LVL1 provision cites an LVL2 provision, so AGENT.39 names the estimate of AGENT.6 that states its basis, which STND.CREW.7 is what grounds wherever STND.CREW applies, and the AGENT Notes say so. The Notes sentence "until the custodians interpret GOV.11 for such provisions" now adds that the question is closed for AGENT.39, since an estimate that states its basis is a basis the agent itself supplies at every class, so that the provision binding at every class asks no measured baseline and no decision of the human owner. |
| R2.3 | CC5, CP19, CC17 | C5 above. |
| R2.4 | CP9, CP10 | C6 above. CP21 (the lead agent at CSQ2) is not carried: it is Unchecked and no ruling names it. |
| R2.5, CC15 | checked: STND.CLASS.7 read "the human owner SHALL reassess the class (GOV.14)" at each occasion | STND.CLASS.7, first sentence: "… the human owner SHALL reassess the class before the work is next promoted, released, or relied upon at a more severe class (GOV.14)." The second sentence stays, so the use that occasioned a reassessment waits for it. |
| R2.5, CC22 | checked: STND.THRT.6 read "propose to the human owner each change of the threat model that the event calls for", and the Notes "the human owner adopts the revised threat model" | STND.THRT.6: "… the actor SHALL record the event and propose to the human owner, as an item of its next report, each change of the threat model that the event calls for (GUARD.16)." Notes: the proposal is an item of the next report, not a referral; until the human owner adopts the change, the model as adopted governs. |
| R2.5, CP11 (Unchecked) | checked: QA.5 "reports the defect to the human owner" sets no time; the STND.CREW Notes said "recorded … in defect tracking, as QA.5 asks, together with its report to the human owner". Confirmed. | STND.CREW.10, second sentence: "The lead agent SHOULD assign to a unit of work each defect recorded under QA.5 that the finder does not fix, and each such change, and present the reports of those defects that QA.5 asks to the human owner together, in its next report (QA.4, QA.5)." One modal; the Notes say QA.5 sets no time. |
| R2.5, CP14, and R7.3 | checked: STND.CREW.23 is marked binding (PRIME.11, GUARD.16) and reads SHOULD; the Notes call it a recommendation | STND.CREW.23: "An agent that has made a network access under an authorization for read-only research retrieval SHALL change no part of the work, other than records, in the session in which it made that access (PRIME.11, GUARD.16). A context that holds none of the retrieved content, other than through a research note, SHALL count as a session other than that one (PRIME.11)." SHALL, because the provision instantiates PRIME.11 and GUARD.16, which force the binding mode (GOV.19), so it cannot be a default; the fresh-context sentence keeps the cost at a context change, with no round trip to the human owner. The Notes' floor argument now says that it states how PRIME.11 is met for retrieved content. |
| R2.5, CP20 (Unchecked) | checked: STND.CREW.3 read "an amendment proposal for the human owner to send to its adopter". Confirmed; GOV.47 has the project report to the custodians, and GOV.46 makes each finding an amendment proposal. | STND.CREW.3, second sentence: "The lead agent SHOULD draft, for each such provision, an amendment proposal, which goes to the provision's adopter with the report of GOV.47 (GOV.46, GOV.47, GOV.49)." |
| R2.5, CS9 | checked: HW.1 gave six attributes, each "true when the classification records that a component … executes, or is admitted to execute, on" one type, and the HW Notes said that adding a type revises the classification | HW.1 gives one attribute, *Hardware execution*: "An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on a hardware type." The six attribute terms are removed; *Hardware type* names the six kinds for which the profile holds a sub-profile. STND.DRAFT.36 has a profile's selector give each attribute of its sub-profiles' selectors, so the six sub-profile selectors give Hardware execution as well (one row each, with the `selector` field and the Notes sentence), and path scope alone decides which provisions reach a component (STND.DRAFT.38). The HW Notes say that no selector tests the type, and that the execution paths the Classification section lists by hardware type (STND.PROJ.1) are the record a new path changes. |
| R2.6 | CS8, CC19, CP16 | C8 above. |
| R2.7 | CS13 | PRIME.13 kept. |
| R3.1 | CC4, CC32, CP1, CL26, CS12, CC9, CC10 | C1 above. |
| R3.2 | CC32, CL26, CS12, CL21 | C2 above. |
| R3.3 | CC7, CP2, CL12, CS11, CC11 | C3 above. |
| R3.4 | CC12, CP3, CL11, CS3, CS10 | C4 above. CS10's numerical specification is the tolerance basis row (NUMER.11); CC12's informative sentence is in the STND.CLASS Notes. |

## Floor arguments (GOV.11)

- **GOV.13, QA.11:** above, under the LVL0 amendment.
- **STND.CLASS.5:** one entry in a record the human owner adopts anyway, in the same act; it sets no class.
- **STND.CLASS.22:** states how GOV.14, which already has every obligation of a class met before reliance at that class, is met for past work, at less cost than a review of each past change; it falls on the work and asks no decision of the human owner beyond the reassessment GOV.14 assigns.
- **STND.CLASS.21, STND.CLASS.23, and the STND.CLASS.10 exception:** under C4; applied at CSQ4 by the human owner's recorded entry of the expected class, which names the consequence.
- **STND.CLASS.3, STND.CLASS.7, STND.CLASS.19:** narrow an obligation.
- **STND.CLASS.1, STND.CLASS.18:** widen the CSQ3 reliance test to GOV.12's words and widen who counts as a reviewer; no obligation added.
- **STND.PROJ.1:** one line of a section the human owner adopts anyway.
- **STND.CODE.20:** the record is owed later; the marker is one token at each deviation.
- **HW.1 and the six selectors:** the profile and its sub-profiles bind where they bound, since a component on one of the six types made one of the six attributes true, and a provision about a path on one type still imposes nothing on a component with no such path.
- **HW.19, HW.21, HW.CPU.5, NUMER.18:** a report into the record asks less of an unattended run than a message no one receives; INTPR.7 is met by the record where no operator acts.
- **AGENT.39, AGENT.23:** widen a permission; AGENT.39 binds at every class as before and now accepts a basis the agent supplies.
- **STND.CREW.3, STND.CREW.10:** take two round trips to the human owner out of ordinary work; GOV.47 and QA.5 set no time.
- **STND.CREW.23:** states how PRIME.11 is met for retrieved content, at the cost of a fresh context; no decision of the human owner, no halted line of work.
- **STND.THRT.6:** the proposal still reaches the human owner, in the next report; GUARD.16 asks a review, not a halt.
- **STND.WPROC, term Main line:** a release stays the human owner's decision; team use within development, which CSQ3 admits, is not a release.

## For the custodian at ratification

Each is a choice the ruling did not fix, drafted as recommended.

1. **C1, GOV.13's trigger.** "an agent that needs the class to promote, release, deploy, or drive physical hardware" names the four events of the ruling; a referral for a halt under another provision (STND.DFLT.13's ledger entry, a profile's selector) is not among them, so unclassified work proceeds at the floor until one of the four. Alternative: keep "an agent that needs it", undefined. Recommended: the four events.
2. **C1, the expected class in LVL0.** GOV.13 itself says that the classification records a planned more severe use as the expected class, adopted with the classification; and the Lexicon defines the term. Alternative: GOV.13 silent, STND.CLASS.5 alone holding the entry (then GOV.13's "uses then made" leaves the plan nowhere in LVL0). Recommended: as drafted, since C2 and C4 read the entry and GOV.11's decision argument rests on it.
3. **C5, the term Team.** STND.CLASS defines a team as the actors that act on the work under the direction of its human owner, and an author's immediate team as the team of the work the author acts on, which is what GOV.12 leaves undefined. A larger project with several groups under one human owner is one team under this definition. Alternative: leave the words undefined, as GOV.12 does. Recommended: define it, since the width of CSQ3 decides how often a promotion is needed (CC17).
4. **C5, which results the classification promotes.** Only those that meet their acceptance criteria (QA.1); a result that fails them, or is judged by criteria set after it was seen (QA.12), is not promoted by the classification. Alternative: every result relied upon within the test, unverified ones labeled. Recommended: as drafted.
5. **C2, STND.CLASS.21 at CSQ4.** STND.CLASS.10 excepts STND.CLASS.21 as well as the records of STND.CLASS.23 from what work of CSQ4 omits, on the same GOV.11 argument, because a design-for-upgrade default that CSQ4 omits enables nothing for work that starts at CSQ4. Alternative: STND.CLASS.21 from CSQ3 only. Recommended: as drafted.
6. **C2, STND.CODE.20.** The record from CSQ1, the marker earlier, revisiting the onset ratified for C++ (STND.CXX 1.1) and C (STND.STDC.1). The custodian's confirmation of that change is what ruling C2 asks.
7. **C3, the reach of the last item of STND.CLASS.22.** "each default of form or style that first reaches it" covers the adoption of a standard as well as a reclassification, instantiating GOV.42, so that the language Notes cite it in place of the transition sentence they held. Alternative: reclassification only, the language Notes keeping their own sentence. Recommended: as drafted, one rule.
8. **C3, "defaults of form or style".** The next-touch rule reaches the defaults GOV.19 calls "of form or style"; every other default of the new class is met before reliance like the rest. Alternative: every default. Recommended: as drafted, which is the ruling's "form-only".
9. **C4, the table.** The records are named by row with the provision that holds each at CSQ3, three of them profile provisions (NUMER.11, MEAS.3 with MEAS.4, HW.QPU.3) that apply only where the expected class and the selection would bring the profile. Alternative: name the records without the citations. Recommended: as drafted, which the brief asks.
10. **C6, the term Agent session.** "One run of an agent from its start to its end, whose context holds nothing of another run except what it reads from the records of the work", so that a second session of the author's configuration counts at CSQ3 and a continuation of the author's context does not. Recommended: as drafted.
11. **C8, CS8 wording.** "to the operator of a run during which one acts and otherwise in the record of the run", in four provisions. Alternative: a defined term in HW and NUMER. Recommended: the wording, since a term would fix the meaning of a verb phrase.
12. **C8, CC19.** The transcript is accepted for each access it shows, with the items it lacks stated once for the session or beside the access. Alternative: the transcript alone. Recommended: as drafted, so every item of REPRO.11 is still recorded.
13. **CS9, the six sub-profile selectors.** STND.DRAFT.36 requires the change once HW.1 gives one attribute; the brief listed HW and HW.CPU. Each sub-profile now binds with HW, and path scope decides what reaches a component. Residual: the Classification section still lists the execution paths of each component by hardware type (STND.PROJ.1), so a path on a new type still changes a record the human owner adopts; whether that list should leave the classification is a question for round e. Recommended: the six selectors as drafted, the residual noted.
14. **R2.2, the basis in AGENT.39.** "an effort estimate under AGENT.6 that states its basis" in place of CP8's "an estimate grounded under STND.CREW.7", since no LVL1 provision cites an LVL2 provision. Alternative: cite STND.CREW.7. Recommended: as drafted.
15. **R7.3, STND.CREW.23.** SHALL, with the fresh-context sentence. Alternatives: a default (impossible while it instantiates PRIME.11, which forces the binding mode under GOV.19); withdraw it and keep the practice in the Notes. Recommended: SHALL.
16. **CC22, "its next report".** The actor of STND.THRT.6 may be a human, whose next report is whatever the work process gives; for an agent it is the work report. Recommended: as drafted.
17. **PRIME.13.** Kept, as the ruling says; nothing to ratify.

## Checks

- `ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28,apply_round_c_2026_10_28 python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`: 41 entries appended (203 to 243, the last 21 this round's); every check PASS, logic PASS with the one g.18 warning the corpus carries; source unchanged. Run twice, before and after the two wording fixes below.
- Kept copy under `/tmp/claude-1000/round-c-kept2/`: `references --check` PASS; `compose --check` lists the six reading copies as stale because the kept copy has no `rendered/` beside it, which the lead rebuilds after ratification; `pairs` for the twenty changed documents, and `pairs GOV --amends GOV.13` and `pairs QA --amends QA.11` (no pair), with the 460 pairs on a changed side and their verdicts in `pairs-changed.md`, no conflict; `findings.py` over each changed document finds only the notices the live corpus already carries (g.14 numbers in STND.CLASS.19 and STND.PROJ.6, g.12 in STND.PROJ.3 and STND.PROJ.6, g.18 bundles in STND.WPROC and the language standards, g.11 on AGENT.39, whose list predates this round, as a run on the base copy shows). Two new notices were raised and fixed: g.11 on STND.CLASS.21 ("SHOULD NOT preclude … nor …" over a list), fixed by "SHOULD admit, without rework of the design"; g.19 "undefined role word team" on STND.CLASS.1, the STND.CLASS Notes, and the STND.WPROC Notes, fixed by the term Team in STND.CLASS and by wording the STND.WPROC Note without the word.
- Self-check: one modal per sentence and at most two per provision in every provision this round changes or adds (STND.CLASS.22's list sits under one SHALL); conditions before clauses, with the CS8 clause worded without a condition word after the modal; none of the banned words or quantifiers in a body; titles of at most five words, not verb-initial, distinct across the corpus; body identifiers equal `instantiates` plus `refers_to` (the checks `ids` and `references` pass); every document named in a body listed in References (rebuilt by the script).
- Harness: no code changed; unit 0027 was not needed. No check's verdict on the live corpus changes.

## Left to the lead

- `rendered/` and `OPEN-ITEMS.md` after ratification.
- Round o: nothing listed; the four language Notes were still in place after round d, so C3's citation is carried here.
- Round e: whether the execution paths by hardware type should leave the Classification section of STND.PROJ.1 (item 13 above), and the pairs listing's size, which E1 narrows.
- Round d is still in review: this round's edits to STND.CODE touch only STND.CODE.20 and three sentences of the Notes paragraphs on high assurance, by exact replacement of text that rounds a and d leave; if round d changes those sentences, the three `replace_text` pairs in `round_c_rest.py` (`CODE20`, `CODE_DOC`) are what to re-anchor.
