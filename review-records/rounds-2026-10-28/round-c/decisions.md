# Round c of 2026-10-28: classes, the expected class, promotion, and the round trips below CSQ2

This round carries rulings C1 to C6 and C8 of `review-records/deep-review-2026-10-28/rulings.md`, each on the reading given in its section "Rulings of the custodian, 2026-10-28", and the register entries R2.2 to R2.7, R3.1 to R3.4, and R7.3. The module is `tools/amendment-scripts/apply_round_c_2026_10_28.py`, with the helpers `round_c_class.py` (LVL0, STND.CLASS, STND.PROJ) and `round_c_rest.py` (the rest), run through `apply_rounds_2026_10_28.py` after rounds a and d. Twenty-one transactions, in citation order: LVL0 1.7, STND.CLASS 1.4, STND.PROJ 1.4, STND.CODE 1.5, HW 1.2, HW.CPU 1.1, HW.GPU 1.1, HW.QPU 1.1, HW.EMBED 1.1, HW.FPGA 1.1, HW.ASIC 1.1, NUMER 1.4, STND.CONC 1.1.2, AGENT 1.3, STND.CREW 1.2, STND.THRT 1.1, STND.WPROC 1.2, STND.JL 1.4.1, STND.PY 1.3.1, STND.RUST 1.3.1, STND.STDC 1.3.1. The round was reviewed cold (`review.md`), revised, and verified cold (`verify.md`); the section "Review and dispositions" gives each finding's fate. Nothing here is in force until the custodian ratifies it and the script runs.

## The LVL0 amendment

LVL0 goes from 1.6 to 1.7 by a transaction in the form of entries 30 and 46 of `harness/governance/ledger.jsonl`: type `amend`, actor The Custodian, role custodians, authority GOV.40, targets LVL0 with GOV.13 and QA.11, scope the thirteen LVL0 folders, and a rationale that states the reading, the alternatives weighed, the class, the lower governance affected, and the proposal (GOV.40). The LVL0 text that changes:

**GOV.13, Class assignment**, old: "The human owner sets the project's consequence class at inception, as the most severe class of its intended uses, and MAY revise it throughout the project's life. The human owner MAY record a less severe class for a component shown to be isolated from the more severe outputs. No class is assumed by default: where none is recorded, an agent that needs it halts that line of work and refers (PRIME.14)."

New:

> The human owner sets the project's consequence class at inception, as the most severe class of the uses then made of its outputs, and MAY revise it throughout the project's life. Where a more severe use is planned, the classification records the class of that use as the expected class, adopted with the classification (GOV.24) and setting no class before that use begins (GOV.14). The human owner MAY record a less severe class for a component shown to be isolated from the more severe outputs. No class is assumed by default: where none is recorded, the work meets the floor (GOV.10), and an agent that needs the class to promote, release, deploy, or drive physical hardware halts that line of work and refers (PRIME.14).

Why it is minor and lowers no floor: the first sentence changes which uses set the class at inception, from "its intended uses" to "the uses then made of its outputs"; a planned use no longer sets the class now, but GOV.14 is unchanged and still has every obligation of a class met before the work is relied upon at that class, so the obligations of the planned class arrive before anyone relies on the work at it. The second sentence adds one entry to the classification, which the human owner adopts in the same act (GOV.24, GOV.50), and gives it no force until the use begins. The last sentence names the trigger of "needs it" by the four events of ruling C1 (CC9): unclassified work meets the floor (GOV.10), which it met anyway, and nothing relies on an unpromoted result beyond its author (QA.11), so letting floor-level work proceed before the classification lowers nothing; the agent still halts before a promotion, a release, a deployment, or a command to hardware. No prime directive or principle changes in motivation or intent (STND.IDENT.3, minor).

**QA.11, Promotion**, one sentence inserted before "An agent MAY propose a promotion.":

> For work of CSQ3 or CSQ4, the adopted classification is the promotion of each result that meets its acceptance criteria (QA.1), for reliance by its author or immediate team alone, feeding work that is verified later (GOV.12).

Why it is minor and lowers no floor: QA.11 is outside the floor (GOV.10). The standing promotion reaches only reliance within the CSQ3 test as GOV.12 writes it, by a result that meets the acceptance criteria that QA.1, in the floor, records before the work at every class (CP19's own text); a result that fails them, or is judged by criteria set after it was seen (QA.12), is not promoted by the classification, and reliance beyond the immediate team, or not through verified work, still needs its own promotion. The rest of QA.11 is unchanged, so "relying on one beyond its author is a blocking defect" now reads with the classification as the promotion of team reliance.

**Lexicon**, two terms added, in the group Governance: *Expected class*, "The consequence class, more severe than the class of the work, of a use of the work that the classification records as planned; it sets no class before that use begins." (governed by GOV.13, GOV.14); *Reclassification*, "A revision of the classification that moves the consequence class of the work, or of a component, to another class." (governed by GOV.14, GOV.24). GOV.13 introduces the first term, and lower governance uses a Lexicon term without redefining it; the second fixes the word that new text uses for a change of class, keeping "promotion" for a result (CP19). Defining a term for a sense the provisions use is editorial on its own (STND.IDENT.3); it rides on the minor amendment.

## Rulings carried

### C1. Class at inception and the expected class (R3.1)

**Reading drafted.** Option (a): the class at inception is that of the uses then made; a planned more severe use is recorded in the classification as the expected class, drafted by an agent and adopted with the classification, with no separate act; unclassified work meets the floor until its first promotion, release, deployment, or actuation (CC9); STND.CLASS.5 and the Classification row of STND.PROJ.1 gain the expected class; STND.CLASS.3's money threshold applies from CSQ2 (CC10). GOV.13 as above.

**STND.CLASS.5, second sentence added:** "Where a more severe use of the project or of a component is planned, the classification SHALL state its expected class and the use that would occasion it (GOV.13, GOV.24)."

**STND.CLASS.3:** "Where the class of the project or of a component is CSQ2 or a more severe class, the classification SHALL state the amount of money above which a loss counts as a cost for the consequence test of CSQ1 in the table of STND.CLASS.1 (GOV.24)." **STND.CLASS.1, CSQ1 consequence test**, the cost limb: "or a cost above the amount that STND.CLASS.3 has the classification state." Why this is coherent (D5): below CSQ2 the classification states no amount, so the cost limb has no amount to exceed and is not met; STND.CLASS.2 does not count it met, because the doubt it resolves is doubt about the work, not the absence of an amount that the classification is not yet asked to state; the other limbs of the CSQ1 test, destroyed equipment, irreplaceable data or samples, and a failed campaign, still move CSQ3 work to CSQ1 where they hold. The condition reads "the class … is CSQ2", not "records CSQ2", so an expected CSQ2 does not trigger it. The Notes say so.

**STND.PROJ.1, Classification row:** "… the consequence class (GOV.13); where a more severe use is planned, the expected class and the use that would occasion it (GOV.13); the proportionality judgment (GOV.11)". The STND.PROJ Notes say the entry is drafted by an agent with the rest of the classification and adopted with it, sets no class until the use begins, and is what STND.CLASS.21 and STND.CLASS.23 read.

The STND.CLASS Notes say that a project that plans a published result begins at CSQ4 or CSQ3 and reaches CSQ2 by reclassification before the result is relied upon at that class; that the expected class is drafted with the classification and adopted with it in one act (GOV.50); and that the human owner's entry of it is the recorded project decision naming the consequence that GOV.11 asks before lower governance raises the floor (C4).

### C2. Design for the expected class (R3.2)

**Reading drafted.** Option (a): one STND.CLASS default, cited by STND.CODE, HW, and STND.CONC; where the classification records an expected class, design does not preclude the parts of that class (contracts, schemas, provenance, edition, subset, failure channel, dependencies, hardware, reduction order, a kept reference path); the reason for each choice the expected class drives goes in a decision record; no record of the expected class is owed before reclassification; the custodian's "minimize the upfront burden but enable design for upgrade". The deviation record of STND.CODE.20 moves to CSQ1, and only its marker is kept earlier.

**New STND.CLASS.21, Expected class in design (default: DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7):**

> Where the classification records an expected class, the design of the work SHOULD admit, without rework of the design, the parts of the table of STND.CLASS.10 that apply from that class, and the contracts, schemas, provenance, language edition and subset, failure channel, dependencies, hardware, reduction order, and kept reference path that the obligations of that class ask of the work, with the reason for each choice that the expected class drives recorded in a decision record (DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7). Before the reclassification, the work MAY omit each record that only an obligation of the expected class requires, other than the records of STND.CLASS.23 (GOV.11).

"Admit, without rework of the design" is the ruling's "does not preclude" in the positive, because "SHOULD NOT preclude … nor …" over a list is a negated list (STND.DRAFT.15, g.11); it is also DSGN.13's word. The parts are named generically, not by the LVL2 provisions that hold them, so that STND.CLASS cites no language or systems standard; the citing documents name their own parts. STND.CLASS.10 excepts STND.CLASS.21 from what work of CSQ4 omits (see C4), because most work with an expected class starts at CSQ4 and a default that CSQ4 omits would enable nothing.

**STND.CODE.20, Recorded high-assurance deviations:**

> For work of CSQ1 or CSQ0, each deviation from a rule of the high-assurance coding standard of STND.CODE.17 SHALL be recorded as the deviation procedure of that standard requires, at its location under one marker that the repository configuration names or in a decision record that the location cites, with the identifier of the rule, the reason, and the evidence that the code stays correct (REPRO.7). Other work that adopts such a standard SHOULD mark each deviation at its location under that marker (REPRO.7).

**This revisits an onset the custodian ratified.** The STND.CODE Notes said: "STND.CODE.20 applies wherever a high-assurance coding standard is adopted, CSQ4 included, though STND.CLASS.10 lets work of CSQ4 omit an obligation above the floor. The custodian ratified these onsets for C++ with the provisions on high-assurance code that STND.CXX 1.1 held … and for C through STND.STDC.1." The Notes now say that the record applies from CSQ1 with STND.CODE.17 and STND.CODE.19, that the marker alone applies wherever such a standard is adopted, that the record was ratified as applying wherever such a standard is adopted, and that revision 1.5 moves it to CSQ1 under the custodian's ruling of 2026-10-28 (CL21, CL26). The rationale says the same. The Notes also cite STND.CLASS.21 for the subset, the edition, the failure channel, and the dependencies, say that it asks no other record of that class before the reclassification than the records of STND.CLASS.23, and that the marker is the one thing of STND.CODE kept earlier, so that the reclassification finds each deviation by a search and writes the record STND.CLASS.22 then owes once.

**HW Notes** cite STND.CLASS.21 for the hardware, the reference path (HW.15), the reduction order, and the bounds (HW.20). **STND.CONC Notes** (editorial) cite it for the combination order of STND.CONC.22 where an acceptance criterion of the expected class asks bitwise identity across numbers of tasks. Both say it asks no other record of that class before the reclassification than the records of STND.CLASS.23. The citations are in the Notes, because the default applies to every project by STND.CLASS itself and a provision that repeated it would restate (GOV.31).

### C3. What a reclassification owes (R3.3)

**Reading drafted.** Option (a): one STND.CLASS provision, met before reliance at the new class: regenerate results that lack recorded inputs; label "unverified" the results judged by criteria set after they were seen (QA.12); one review of the accumulated changes at the new independence; an audit only on a move to CSQ2 or a more severe class; each check tied to an event repeated before reliance; form-only defaults met when a change next touches the code, which the review and the coordinator limit to form on whose outcome no reliance turns (D1). STND.CLASS.19's audit is limited accordingly. The four language Notes keep their transition sentence and add that STND.CLASS.22 governs on a reclassification (D2).

**New STND.CLASS.22, Reclassification obligations (binding: GOV.14, REPRO.1, QA.12, QA.7, GOV.47, GOV.42):**

> Before work is relied upon at a more severe class, the work done at the less severe class SHALL meet the obligations of that class through these steps (GOV.14):
>
> - the regeneration of each result to be relied upon at the new class whose record lacks an input of REPRO.1 (REPRO.1);
> - the label unverified on each result to be relied upon at the new class that was judged against criteria set after it was seen (QA.12);
> - one review, at the independence of the row of the new class in the table of STND.CLASS.18, of the changes made since the last review at that independence, taken as one change, against the obligations of the new class (QA.7);
> - the audit that STND.CLASS.19 requires before the reliance (GOV.47);
> - the repetition, before the reliance, of each check that an obligation of the new class ties to an event that preceded the reclassification (GOV.14).
>
> Existing source SHALL conform, at the next change that touches it, to each default of form or style that the new class first applies to it and on whose outcome no reliance at the new class turns (GOV.42).

Two modals. GOV.14 is intact: the work done at the less severe class meets the obligations of the new class through the steps, the one review being against those obligations, so a contract or schema the new class asks is found and added before the reliance; the only deferral past reliance is a default of form or style on whose outcome no reliance turns, which is the ruling's "form-only defaults met when a change next touches the code" read as the coordinator directs. Results to be relied upon at the new class are the ones regenerated or labeled, each item naming them on its own (S1, V1).

**STND.CLASS.19, second sentence:** "Before work moved to CSQ2 or a more severe class is first relied upon at that class, the project SHALL be audited by the auditor of that class (GOV.47)." The audit falls once, on the reclassification, then at the interval of the table (D3); the step from CSQ4 to CSQ3 needs none (CC11).

**The four language Notes** (STND.JL, STND.PY, STND.RUST, STND.STDC, each editorial) keep their sentence as it was and append "; on a reclassification, STND.CLASS.22 governs." STND.FTN has no such sentence (CL12 counted five; four hold). STND.CLASS.22 governs a reclassification only; the adoption of a standard stays under the recorded transition of each standard and GOV.42 (D2).

### C4. Cheap records below the expected class (R3.4)

**Reading drafted.** Option (a): where the classification records an expected class, CSQ4 work keeps, as SHOULD defaults, the tolerance basis, seeds and environment identity, lock files and toolchain revisions, the sources of expected test values, and raw observations and quantum-processor jobs that cannot be repeated; the provisions that hold each record at CSQ3 are cited, not restated; the human owner's entry of an expected class is the "recorded project decision naming the consequence" of GOV.11.

**New STND.CLASS.23, Records below the expected class (default: REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3):**

> Where the classification records an expected class, work of CSQ4 SHOULD keep each record of the table of this provision that the provision beside it would ask of the work at that class, as that provision describes it (REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3).
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

One condition (S2). "That the provision beside it would ask of the work at that class" keeps a profile's record (NUMER.11, MEAS.3, HW.QPU.3) to work whose expected class and selection would bring that profile; REPRO.1 applies at CSQ3 by STND.CLASS.10.

**STND.CLASS.10, second sentence:** "Work of CSQ4 MAY omit every obligation of these Articles above the floor, other than STND.CLASS.21 and the records of STND.CLASS.23 (GOV.11)." Without the exception the two defaults would be omitted at CSQ4 by the provision that defines CSQ4's omission.

**The GOV.11 argument.** GOV.11: "lower governance SHALL NOT raise the floor except by a recorded project decision naming the consequence that warrants it." STND.CLASS.21 and STND.CLASS.23 reach work of CSQ4 only where the classification records an expected class. That entry is recorded (GOV.36), it is the human owner's own act (GOV.50, GOV.13), and it names the consequence: the class the work is expected to reach, which is the consequence class of the planned use. So the two defaults apply at CSQ4 by a recorded project decision naming the consequence, as GOV.11 allows, and work with no expected class stays as light as before. The STND.CLASS Notes and the rationale say so.

### C5. Promotion at CSQ3 (R2.3)

**Reading drafted.** Option (a): QA.11 as above; STND.CLASS.1 aligned with GOV.12; "reclassification" for a change of class, "promotion" for results (CP19).

**STND.CLASS.1, CSQ3 reliance test:** "Only the author, or the actors of the author's immediate team, rely on the output, and only through work that is verified before it is relied upon." The STND.CLASS Terms define *Team*: "The actors, persons and agents alike, that act on the work under the direction of its human owner; an author's immediate team is the team of the work on which the author acts." GOV.12 uses the words without defining them; the term is "Team" rather than "Immediate team" because STND.DRAFT.29 lists "team" as an undefined role word that a document's own Terms may define (g.19); the definition is put to the custodian below.

The STND.CLASS Notes say that for work of CSQ3 or CSQ4 the adopted classification is the promotion of each result that meets its acceptance criteria for reliance within the CSQ3 test as GOV.12 writes it, so that no result is promoted one by one below CSQ2, and that reliance beyond that test needs its own promotion. STND.CLASS.20 is unchanged: a promotion still cites the classification entry, and the standing promotion is that entry. **STND.CLASS.7** uses the words the same way (S7): "… the human owner SHALL reassess the class before a result of the work is next promoted, or the work is next released or relied upon at a more severe class (GOV.14)."

### C6. Who counts as another actor (R2.4)

**Reading drafted.** Option (a): at CSQ3, any agent session other than the author's counts, its configuration included; at CSQ2, a different model or a different instruction revision, since a difference of tools alone does not suffice. The terms CP9 and CP10 show undefined are fixed in STND.CLASS, where STND.CLASS.18 uses them; *Session* keeps the meaning AGENT gives it, "one continuous run of an agent and the instructions it received in that run" (D4).

**STND.CLASS.18, CSQ3 row:** "An actor other than the author: a human, or an agent, of the author's agent configuration or another, in a session, other than each session of the author, whose context holds nothing of the author's sessions except what it reads from the records of the work (QA.7)." **CSQ2 row:** "An actor not directed by the author performs the review; where the author is an agent, that actor is a human or an agent whose agent configuration differs from the author's in its model or in its instruction revision, whatever its tools." The STND.CLASS Terms say "Session has the meaning that AGENT gives it." The Notes give the reasons: a session whose context holds nothing of the author's sessions, beyond what the records carry, examines the change cold, and a reset of the author's context inside the authoring run is not such a session, so an author never reviews its own work; a difference of tools alone leaves the same model reasoning under the same instructions, and the auditor of the rows CSQ1 and CSQ2 of STND.CLASS.19 is read as the CSQ2 row of STND.CLASS.18 reads the reviewer (reading 5).

### C8. Reports to the operator, network records, main lines, the hazard analysis (R2.6, R2.7)

**Reading drafted.** Option (a) for the first three; PRIME.13 kept.

**Reports to the operator (CS8).** HW.19, HW.21, HW.CPU.5, and NUMER.18 each report "to the operator of a run during which one acts and otherwise in the record of the run". The clause is worded without a condition word after the modal (STND.DRAFT, g.12); one wording in four provisions rather than a defined term, because a term would fix the meaning of a verb phrase. HW.19: "the path SHALL report the fallback at its first occurrence in the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.7)." HW.21: "… and report each overrun to the operator of a run during which one acts and otherwise in the record of the run (RSRC.2, RSRC.3, INTPR.7)." HW.CPU.5: "the path SHALL report the excess at its first occurrence in the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.7, RSRC.2)." NUMER.18: "the departure SHALL be reported during the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.10, INTPR.7)." The HW, HW.CPU, and NUMER Notes say that an unattended run has no operator to receive a message and its record is what a reader examines afterward.

**Network record (CC19). AGENT.23, second sentence:** "Where the provisioned environment records a network access with these items in a record that the agent is unable to alter, or a transcript of its session that the agent did not edit shows the access, with each of these items that the transcript lacks stated once for the session or beside the access, an agent MAY cite that record or transcript in place of its own (REPRO.11)." The AGENT Notes say that a transcript shows each access with its address, its time, and the direction of transfer, and that the items it lacks, the authorization relied on and the access descriptor among them, are stated once where they hold for every access of the session, and beside the access otherwise (S6), so that an agent at CSQ3 writes no seven-item record before each next step. STND.DFLT.27 still gives the descriptor's form.

**Main line (CP16).** Defined where the term is defined, the STND.WPROC Terms: "Main line | Each branch from which the work is released or deployed; a branch drawn on only within development, for the reliance that the CSQ3 reliance test of STND.CLASS.1 admits, is not one." The Notes say that a push to such a branch is no release decision and that an agent merges into it as STND.WPROC.11 provides; they avoid the word "team", which STND.DRAFT.29 flags outside a document that defines it (g.19). The exclusion is kept in the term rather than the Notes alone (O3), because the brief asks that it be defined where "main line" is defined, and *Development line* names one branch while the exclusion reaches each branch so drawn on.

**PRIME.13 (CS13).** Kept: the human owner still adopts each revision of the hazard analysis; CPS.3 is unchanged. The ruling keeps it because physical safety is a prime directive.

## Register entries carried

| Entry | Sources | Drafted |
| --- | --- | --- |
| R2.2 | CP8, CC16 | AGENT.39: "… and, from a measured baseline, an effort estimate in the form of AGENT.6 that states its basis, or a recorded decision of the human owner, that running the units together takes less time or operating cost …". CP8 proposed "an estimate grounded under STND.CREW.7"; no LVL1 provision cites an LVL2 provision, so AGENT.39 names the estimate of AGENT.6 that states its basis, which STND.CREW.7 is what grounds wherever STND.CREW applies, and the AGENT Notes say so. The Notes sentence "until the custodians interpret GOV.11 for such provisions" now adds that for AGENT.39 the question no longer affects the burden, since an estimate that states its basis is a basis the agent itself supplies at every class, so that the provision binding at every class asks no measured baseline and no decision of the human owner. |
| R2.3 | CC5, CP19, CC17 | C5 above. |
| R2.4 | CP9, CP10 | C6 above. CP21 (the lead agent at CSQ2) is not carried: it is Unchecked and no ruling names it. |
| R2.5, CC15 | checked: STND.CLASS.7 read "the human owner SHALL reassess the class (GOV.14)" at each occasion | STND.CLASS.7, first sentence, as under C5. The second sentence stays, so the use that occasioned a reassessment waits for it. |
| R2.5, CC22 | checked: STND.THRT.6 read "propose to the human owner each change of the threat model that the event calls for", and the Notes "the human owner adopts the revised threat model" | STND.THRT.6: "… the actor SHALL record the event and propose to the human owner, as an item of its next report, each change of the threat model that the event calls for (GUARD.16)." Notes: the proposal is an item of the next report, not a referral; until the human owner adopts the change, the model as adopted governs. The actor may be a human, whose next report is whatever the work process gives. |
| R2.5, CP11 (Unchecked) | checked: QA.5 "reports the defect to the human owner" sets no time; the STND.CREW Notes said "recorded … in defect tracking, as QA.5 asks, together with its report to the human owner". Confirmed. | STND.CREW.10, second sentence: "The lead agent SHOULD assign to a unit of work each defect recorded under QA.5 that the finder does not fix, and each such change, and present to the human owner together, in its next report, the reports of those defects that QA.5 asks (QA.4, QA.5)." One modal; the Notes say QA.5 sets no time. |
| R2.5, CP14, and R7.3 | checked: STND.CREW.23 is marked binding (PRIME.11, GUARD.16) and reads SHOULD; the Notes call it a recommendation | STND.CREW.23: "An agent that has made a network access under an authorization for read-only research retrieval SHALL change no part of the work, other than records, in the session in which it made that access (PRIME.11, GUARD.16). For this provision, a context that holds none of the retrieved content, other than through a research note, SHALL count as a session other than that one (PRIME.11)." SHALL, because the provision instantiates PRIME.11 and GUARD.16, which force the binding mode (GOV.19), so it cannot be a default; the fresh-context sentence is scoped to this provision (D4), in CP14's words, and keeps the cost at a context change with no round trip to the human owner. The Notes' floor argument now says that it states how PRIME.11 is met for retrieved content. |
| R2.5, CP20 (Unchecked) | checked: STND.CREW.3 read "an amendment proposal for the human owner to send to its adopter". Confirmed; GOV.47 has the project report to the custodians, and GOV.46 makes each finding an amendment proposal. | STND.CREW.3, second sentence: "The lead agent SHOULD draft, for each such provision, an amendment proposal, which goes to the provision's adopter with the report of GOV.47 (GOV.46, GOV.47, GOV.49)." |
| R2.5, CS9 | checked: HW.1 gave six attributes, each "true when the classification records that a component … executes, or is admitted to execute, on" one type, and the HW Notes said that adding a type revises the classification | HW.1 gives one attribute, *Hardware execution*: "An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on a hardware type." The six attribute terms are removed; *Hardware type* names the six kinds for which the profile holds a sub-profile. STND.DRAFT.36 has a profile's selector give each attribute of its sub-profiles' selectors, so the six sub-profile selectors give Hardware execution as well (one row each, with the `selector` field and the Notes sentence), and path scope alone decides which provisions reach a component (STND.DRAFT.38). The HW Notes say that no selector tests the type, and that the execution paths the Classification section lists by hardware type (STND.PROJ.1) are the record a new path changes; three Notes sentences that spoke of binding by attribute now speak of provisions reaching a path (S3). |
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
- **STND.CLASS.3, STND.CLASS.7, STND.CLASS.19:** narrow an obligation; the cost limb of STND.CLASS.1 reads the amount the classification states, so no work moves to CSQ1 by doubt and none escapes the other limbs.
- **STND.CLASS.1, STND.CLASS.18:** widen the CSQ3 reliance test to GOV.12's words and widen who counts as a reviewer, while an author's own sessions never count; no obligation added.
- **STND.PROJ.1:** one line of a section the human owner adopts anyway.
- **STND.CODE.20:** the record is owed later; the marker is one token at each deviation.
- **HW.1 and the six selectors:** the profile and its sub-profiles bind where they bound, since a component on one of the six types made one of the six attributes true, and a provision about a path on one type still imposes nothing on a component with no such path.
- **HW.19, HW.21, HW.CPU.5, NUMER.18:** a report into the record asks less of an unattended run than a message no one receives; INTPR.7 is met by the record where no operator acts.
- **AGENT.39, AGENT.23:** widen a permission; AGENT.39 binds at every class as before and now accepts a basis the agent supplies.
- **STND.CREW.3, STND.CREW.10:** take two round trips to the human owner out of ordinary work; GOV.47 and QA.5 set no time.
- **STND.CREW.23:** states how PRIME.11 is met for retrieved content, at the cost of a fresh context, which counts as a new session for this provision alone; no decision of the human owner, no halted line of work. Heavier than the SHOULD it replaces, by that context change.
- **STND.THRT.6:** the proposal still reaches the human owner, in the next report; GUARD.16 asks a review, not a halt.
- **STND.WPROC, term Main line:** a release stays the human owner's decision; team use within development, which CSQ3 admits, is not a release.

## For the custodian at ratification

The rulings, the register's recommendations, and the text decide the rest (see "Review and dispositions"); these five are the choices the rulings leave open, each drafted as recommended.

1. **C5, the term Team.** STND.CLASS defines a team as the actors that act on the work under the direction of its human owner, and an author's immediate team as the team of the work the author acts on, which is what GOV.12 leaves undefined; a larger project with several groups under one human owner is one team, and CSQ2 reliance then means undirected actors or unverified paths. Alternative: leave the words undefined, as GOV.12 does. Recommended: define it, since the width of CSQ3 decides how often a promotion is needed (CC17).
2. **C2 and C4, the two defaults at CSQ4.** STND.CLASS.10 excepts STND.CLASS.21 as well as the records of STND.CLASS.23 from what work of CSQ4 omits, on the GOV.11 argument above, because a design-for-upgrade default that CSQ4 omits enables nothing for work that starts at CSQ4. The STND.CLASS Notes name both: work of CSQ4 meets the floor "and, where the classification records an expected class, STND.CLASS.21 and the records of STND.CLASS.23". Alternative: STND.CLASS.21 from CSQ3 only, the records alone at CSQ4. Recommended: both at CSQ4 where an expected class is recorded. Under the alternative, that Notes sentence drops STND.CLASS.21 with the provision.
3. **C2, STND.CODE.20.** The record from CSQ1, the marker earlier, revisiting the onset ratified for C++ (STND.CXX 1.1) and C (STND.STDC.1). Ruling C2 asks the custodian's confirmation of this change.
4. **R2.2, the basis in AGENT.39.** "an effort estimate in the form of AGENT.6 that states its basis" in place of CP8's "an estimate grounded under STND.CREW.7", since no LVL1 provision cites an LVL2 provision and STND.CREW.7 is what grounds such an estimate wherever STND.CREW applies. Alternative: cite STND.CREW.7 from AGENT. Recommended: as drafted. "In the form of AGENT.6" names the form of the estimate, which the agent supplies at every class, and not an estimate that AGENT.6 requires, since AGENT.6 asks none where the cost is not measurable or a discipline is set under GUARD.14.
5. **C6, the auditor of STND.CLASS.19.** The CSQ1 and CSQ2 rows of STND.CLASS.19 said "an agent auditor has an agent configuration different from that of every authoring agent", which a difference of tools alone meets, while after C6 the CSQ2 reviewer row of STND.CLASS.18 does not. Drafted, in the CSQ1 row (the CSQ2 row keeping "As for CSQ1"): "an agent auditor differs from every authoring agent in its model or in its instruction revision, whatever its tools"; the STND.CLASS Notes say the rows ask the same difference of an agent auditor as the CSQ2 row of STND.CLASS.18 asks of a reviewer, for the same reason. The first draft put this in a Note, which carries no obligation; the verification of the reconciliation (Should-fix 7) moved it into the row. Alternative: leave the auditor rows on the bare term Agent configuration, under which an auditor that differs from every author in its tools alone qualifies, and drop the Note. Recommended: as drafted, since an audit is the later and wider check, and C6's reason, that a difference of tools alone leaves the same model reasoning under the same instructions, holds for it as for a review; the change reaches only work of CSQ2 and more severe classes, and the ratification of this reading is the recorded decision that GOV.11 asks.

## Review and dispositions

The cold review is `review.md`. One row per finding.

| Finding | Disposition |
| --- | --- |
| D1, GOV.14 not intact in STND.CLASS.22 | Fixed as proposed, with the coordinator's limit: lead-in "the work done at the less severe class SHALL meet the obligations of that class through these steps"; the review "against the obligations of the new class"; the next-touch rule its own sentence, reaching only a default of form or style "on whose outcome no reliance at the new class turns"; ", and no more" deleted from the Notes, which now name the one deferral. |
| D2, the language Notes cite STND.CLASS.22 where it does not apply | Fixed as proposed: each old sentence restored, with "; on a reclassification, STND.CLASS.22 governs." appended; the four transactions stay editorial, since the recorded transition is unchanged. |
| D3, STND.CLASS.19 audits before every reliance | Fixed as proposed, with "first": "Before work moved to CSQ2 or a more severe class is first relied upon at that class". The Notes say the audit falls once, then at the interval. |
| D4, self-review after a context reset | Fixed as proposed: STND.CREW.23's sentence begins "For this provision"; the term Agent session is withdrawn for "Session has the meaning that AGENT gives it."; the CSQ3 row reads as the review wrote it; the Notes say a reset inside the authoring run is not such a session. |
| D5, CSQ3 work falls into CSQ1 by doubt | Fixed as proposed: the cost limb of STND.CLASS.1 reads "the amount that STND.CLASS.3 has the classification state", and STND.CLASS.3's condition "Where the class of the project or of a component is CSQ2 or a more severe class". The argument is under C1 and in the Notes. |
| S1, items 1 and 2 of STND.CLASS.22 | Fixed as proposed. |
| S2, two conditions in STND.CLASS.23 | Fixed as proposed. |
| S3, three stale Notes after CS9 | Fixed as proposed, in HW, HW.FPGA, and HW.ASIC. |
| S4, "owes no record of that class" | Fixed as proposed in the HW, STND.CODE, and STND.CONC Notes. |
| S5, CLASS_READING credits | Fixed: Team under C5; the Agent session clause gone; the reading names Session in AGENT's meaning. |
| S6, AGENT Notes | Fixed as proposed, both sentences, and the revision row with them. |
| S7, STND.CLASS.7 | Fixed as proposed. |
| O1, title of STND.CLASS.21 | Taken: "Expected class in design". |
| O2, STND.CREW.10 word order | Taken. |
| O3, Main line exclusion in the Notes alone | Not taken; reason under C8. |
| Readings 1, 2, 4, 7, 8, 9, 10, 11, 12, 15, 16, 17 | Resolved: 1 and 2 by ruling C1 (CC9's four events; option (a) amends GOV.13); 4 by CP19's text; 7 and 8 by D1 and D2; 9 by the brief; 10 by D4; 11, 12, and 16 by the text as revised (S6); 15 by GOV.19, STND.CREW.23 keeping SHALL scoped as D4; 17 merged into C8. Readings 3, 5, 6, and 14 remain, as 1 to 4 above; 13 moved to "Left to the lead" (V3). |
| V1, Defect: item 2 of STND.CLASS.22 inherits item 1's relative clause | Fixed as proposed: "each result to be relied upon at the new class that was judged against criteria set after it was seen". |
| V2, Optional: "whose" in the CSQ3 row can attach to the author | Taken: "in a session, other than each session of the author, whose context holds nothing of the author's sessions". |
| V3, Should-fix: reading 4 is no open choice | Fixed: moved to "Left to the lead", the readings renumbered to four. |

## Notes paragraphs changed, for round o

Each paragraph is named by its opening words in the document as rounds a and d leave it; a selector or Terms change is named as such.

- **STND.CLASS:** Purpose and scope, "This standard fixes the criteria…"; Terms, the intro sentence (Session) and the table (Team); Reading the standard, "The consequence test and the reliance test…", "Work of CSQ3 meets the seven…", and "Revision 0.2 withdrew identifiers…" (its last sentences).
- **STND.PROJ:** "This standard fixes what a project constitution holds…".
- **STND.CODE:** "STND.CODE.17 and STND.CODE.19 are defaults that apply from CSQ1…" (three sentences within it; the class paragraph "Under STND.CLASS.10, each default provision other than…" is untouched).
- **HW:** the `selector` field; the Terms table (six attribute rows removed, Hardware execution added, Hardware type reworded); "HW.1 states the selector…" (four sentences); "HW.8 states how PRIME.4 applies…" (the sentence "Both reports therefore tighten…").
- **HW.CPU, HW.GPU, HW.QPU, HW.EMBED, HW.FPGA, HW.ASIC:** the `selector` field and the paragraph "HW.X.1 states the selector…"; HW.CPU also "Concurrent work that asks for more computing threads…" (the HW.CPU.5 sentence); HW.FPGA also "A processor realized in programmable logic…"; HW.ASIC also the sentence "A device fabricated from a design that the project does not hold…".
- **NUMER:** "Every provision other than NUMER.1, NUMER.2, and NUMER.26…" (one sentence added after the NUMER.26 sentence).
- **STND.CONC:** "Under STND.CLASS.10, each default instantiates only DSGN…" (one sentence added at its end).
- **AGENT:** "AGENT.9 leaves scale to the project…" (two sentences added) and "A provision inherits the rank and waivability…" (one clause added).
- **STND.CREW:** "It keeps one record of everything that awaits the human owner…", "An implementing agent follows the plan…", "Every brief that AGENT.11 requires…", and "Under STND.CLASS.10, each default provision other than STND.CREW.4…" (the STND.CREW.23 clause).
- **STND.THRT:** "The events of STND.THRT.6 always change exposure…".
- **STND.WPROC:** the Terms table (Main line) and "Advancing a main line releases a revision…".
- **STND.JL, STND.PY, STND.RUST, STND.STDC:** the one-sentence paragraph "Existing … source conforms…".

## Checks

- `ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28,apply_round_c_2026_10_28 python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py`, after the review and verification fixes: 41 entries appended (203 to 243, the last 21 this round's); every check PASS, logic PASS with the one g.18 warning the corpus carries; source unchanged.
- Kept copy under `/tmp/claude-1000/round-c-kept4/`: `references --check` PASS; `compose --check` lists the six reading copies as stale because the kept copy has no `rendered/` beside it, which the lead rebuilds after ratification; `pairs` for the twenty changed documents, and `pairs GOV --amends GOV.13` and `pairs QA --amends QA.11` (no pair), with the 460 pairs on a changed side and their verdicts in `pairs-changed.md`, no conflict; `findings.py` over each changed document finds only the notices the live corpus already carries (g.14 numbers in STND.CLASS.19 and STND.PROJ.6, g.12 in STND.PROJ.3 and STND.PROJ.6, g.18 bundles in STND.WPROC and the language standards, g.11 on AGENT.39, whose list predates this round, as a run on the base copy shows). Two notices raised by the first draft were fixed before review: g.11 on STND.CLASS.21, by "SHOULD admit, without rework of the design"; g.19 "undefined role word team", by the term Team in STND.CLASS and by wording the STND.WPROC Note without the word.
- Self-check: one modal per sentence and at most two per provision in every provision this round changes or adds (STND.CLASS.22's list sits under one SHALL, its last sentence under a second); conditions before clauses, with the CS8 clause worded without a condition word after the modal; none of the banned words or quantifiers in a body; titles of at most five words, not verb-initial, distinct across the corpus; body identifiers equal `instantiates` plus `refers_to` (the checks `ids` and `references` pass); every document named in a body listed in References (rebuilt by the script).
- Harness: no code changed; unit 0027 was not needed. No check's verdict on the live corpus changes.

## Left to the lead

- `rendered/` and `OPEN-ITEMS.md` after ratification.
- Round o: the paragraphs listed above, for re-anchoring.
- Round e: the residual of CS9, which this round does not decide: the six sub-profile selectors give the one attribute, as STND.DRAFT.36 requires once HW.1 does, but the Classification section still lists the execution paths of each component by hardware type (STND.PROJ.1), so a path on a new type still changes a record the human owner adopts; whether that list should leave the classification is round e's. Also the pairs listing's size, which E1 narrows.
- Round d is still in review: this round's edits to STND.CODE touch only STND.CODE.20 and three sentences of one Notes paragraph, by exact replacement of text that rounds a and d leave; if round d changes those sentences, the `replace_text` pairs `CODE20` and `CODE_DOC` in `round_c_rest.py` are what to re-anchor.
