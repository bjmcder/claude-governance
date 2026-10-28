# Consequence-class criteria (STND.CLASS) 1.5.1

Adopted by The Custodian as revision 1.0 in ledger entry 14 (2026-10-09); revised to 1.1 in entry 16 (2026-10-09), 1.1.1 in entry 21 (2026-10-10), 1.2 in entry 22 (2026-10-10), 1.2.1 in entry 24 (2026-10-10), 1.2.2 in entry 36 (2026-10-10), 1.3 in entry 58 (2026-10-11), 1.3.1 in entry 158 (2026-10-25), 1.4 in entry 225 (2026-10-28), 1.5 in entry 246 (2026-10-28), and 1.5.1 in entry 310 (2026-10-28). This reading copy is composed from the per-provision files in STND/CLASS/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.CLASS.8, STND.CLASS.9, STND.CLASS.11, STND.CLASS.12, STND.CLASS.13, STND.CLASS.14, STND.CLASS.15, and STND.CLASS.16.

## Purpose and scope

This standard fixes the criteria that place work in a consequence class (GOV.12), how the classification records and revises a class (GOV.13, GOV.14, GOV.24), what each class requires above the floor (GOV.11), the expected class and what it brings before the work reaches it (GOV.13), what a reclassification owes (GOV.14), the independence of review by class (QA.8), and the interval of compliance audit (GOV.47). STND.CLASS.10, STND.CLASS.18, STND.CLASS.21, and STND.CLASS.23 are defaults (GOV.19): a project constitution replaces one by a recorded decision (REPRO.7) with an alternative that meets the same outcome. The others, STND.CLASS.17 and STND.CLASS.22 included, are binding, because they instantiate GOV or a prime directive, which belong to the floor (GOV.10).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Every other part of this document is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Session has the meaning that AGENT gives it.

| Term | Definition |
| --- | --- |
| Credible consequence | A consequence reached from an error in the work by a chain of events, each of which is able to occur in the intended use of the work or in a foreseeable misuse of it. |
| Isolated component | A component whose outputs reach an output of a more severe class only through a check verified at that class to detect and reject every error of the component able to cause a consequence of that class, and that shares no resource whose exhaustion or corruption by it is able to impair a component of the more severe class. |
| Safety-related component | A component an error in which has a credible consequence of class CSQ0. |
| Agent configuration | The model, the instruction revision, and the tools of an agent, as REPRO.11 records them. |
| Team | The actors, persons and agents alike, that act on the work under the direction of its human owner; an author's immediate team is the team of the work on which the author acts. |

## Reading the standard

The consequence test and the reliance test are independent, and the more severe one sets the class. A class attaches to a use of the work, not to its code (GOV.14): the same code is CSQ4 in a notebook, CSQ3 once the author's immediate team builds on it through work verified before reliance, CSQ2 once an actor beyond that team builds on it, and CSQ1 once a relying party outside the project does. Growth of reliance includes the promotion of a result for a new use, the first output that leaves the project, and the first command to physical hardware. The class at inception is that of the uses then made of the work's outputs (GOV.13), so a project that plans a published result begins at CSQ4 or CSQ3 and reaches CSQ2 by reclassification before the result is relied upon at that class; the plan is recorded as the expected class (STND.CLASS.5), which an agent drafts with the classification and the human owner adopts with it in one act (GOV.50), and which sets no class until the use begins. Where an expected class is recorded, STND.CLASS.21 has the design leave open the parts of that class that are costly to add later, with the reason for each choice the expected class drives in a decision record, and STND.CLASS.23 has work of CSQ4 keep the records that a later reclassification is unable to reconstruct, each as the provision that holds it at CSQ3 describes it; the human owner's entry of the expected class is the recorded project decision naming the consequence that GOV.11 asks before lower governance raises the floor, so STND.CLASS.10 excepts the two from what work of CSQ4 omits, and work with no expected class stays as light as before. Nothing else is owed before the reclassification. Work that reaches a more severe class meets the obligations of that class for the work done at the less severe class through the steps of STND.CLASS.22, before it is relied upon there: past changes are reviewed once as one change at the new independence, against the obligations of the new class, an audit is held only on a move to CSQ2 or a more severe class, and each check tied to an event that has passed is repeated; GOV.14 is met, because every obligation of the new class is met before the reliance, and the one deferral is a default of form or style on whose outcome no reliance turns, which existing source meets at the next change that touches it. Reclassification names a change of class; promotion names the human owner's act on a result (QA.11).

| Work | Class | What sets the class |
| --- | --- | --- |
| Software that computes trip setpoints for the protection system of a research reactor | CSQ0 | An error is able to defeat a protective action. |
| Firmware of a radiation survey instrument whose reading decides whether an area is entered | CSQ0 | A safety decision rests on the reading. |
| Control software for a cryostat, where a fault destroys a detector but cannot injure a person | CSQ1 | Loss of equipment. |
| A kinetics code whose results appear in a journal article | CSQ2 | An error leads to a wrong published result. |
| A file-format converter checked when the analysis it feeds is verified | CSQ3 | That verification detects an error. |
| A notebook that explores a new numerical method | CSQ4 | Nothing relies on it before promotion. |

Work of CSQ3 meets the seven proportioned Articles as LVL0 writes them. The table of STND.CLASS.10 lists what waits for a more severe class and what a more severe class adds. The table holds no part of Simplicity (SIMPL). Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor, and, where the classification records an expected class, STND.CLASS.21 and the records of STND.CLASS.23. A mechanism of GOV.21 whose obligation work of CSQ4 may omit, review (QA.7), incident handling (QA.15), and retention (REPRO.12) among them, costs that work no more than one citation of the defaults (STND.PROJ.2), and the obligation that it serves applies from the class that STND.CLASS.10 gives. The five classes resemble the software levels A to E of DO-178C and the graded approach of nuclear quality assurance; no obligation follows from the resemblance.

Below LVL0, the field `onset` of a provision (STND.DRAFT#representation-in-the-harness) states the class from which each of its parts applies, and STND.CLASS.10 gives the field its force. The fields follow one rule: a part applies from the row of the table of STND.CLASS.10 whose named item the part asks for, a reference oracle, a schema, a contract, a documented limit of validity, or another item of the column Part, and otherwise from CSQ3. A part that instantiates the obligation of a row without asking for its item applies from CSQ3, so that a rule of the form of code that rests on DSGN.4 or DSGN.5, and the catch of a failure before it crosses a foreign frame, apply from CSQ3 with the other defaults of form: each costs nothing when the code is written, and a rewrite of each interface when it first applies at a reclassification. Where a field departs from the rule, the Notes of its document give the reason: a less severe class tightens above the floor (PRIME.15), and a more severe class keeps the methods of a standard beyond its core out of work of CSQ3, while the obligation of LVL0 that such a part serves applies at CSQ3 in full. A binding provision carries no field, and a provision that applies at every class, or a permission, carries the value null.

Revision 0.2 withdrew identifiers 8, 9, and 11 to 16, which are not reused (GOV.37). Each provision is one file, `STND/CLASS/<n>.md`, and each table is named in the field `defines`. The lineage and drafting checks read every provision, but no check yet tests a project's classification against this standard, so each provision is checked by a reader for its content. Promotion (QA.11) governs every report of a result at every class, as Normative Language requires; for work of CSQ3 or CSQ4, the adopted classification is the promotion of each result that meets its acceptance criteria for reliance by the author's immediate team through work verified before reliance, the reliance test of CSQ3 read as GOV.12 writes it, so that no result is promoted one by one below CSQ2, while reliance beyond that test needs its own promotion. Work of CSQ4 needs no review until it is promoted or released, because it leaves CSQ4 when another actor relies on it. The CSQ3 row of STND.CLASS.18 counts an agent in a session other than each of the author's as another actor, of the author's agent configuration or not, because a session whose context holds nothing of the author's sessions, beyond what the records of the work carry, examines the change cold; a reset of the author's context inside the authoring run is not such a session, so an author never reviews its own work. The CSQ2 row asks a different model or a different instruction revision, since a difference of tools alone leaves the same model reasoning under the same instructions. The rows CSQ1 and CSQ2 of STND.CLASS.19 ask the same difference of an agent auditor, for the same reason. STND.CLASS.3 asks the money threshold once the class is CSQ2 or a more severe one, where a reclassification to CSQ1 first comes within reach; below CSQ2 the cost limb of the consequence test of CSQ1 has no stated amount to exceed, so it is not met, and STND.CLASS.2 does not count it met, because the doubt that provision resolves is doubt about the work and not the absence of an amount that the classification is not yet asked to state; the other limbs of the test, destroyed equipment, irreplaceable data or samples, and a failed campaign, still move work of CSQ3 to CSQ1. The audit of STND.CLASS.19 falls once on a move to CSQ2 or a more severe class, before the first reliance there, and then at the interval of its table. STND.CLASS.7 has the reassessment made before the next promotion of a result, release, or reliance at a more severe class, so that reported scenarios accumulate for one act of the human owner, while the use that occasioned a reassessment waits for it.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| HW.QPU | Quantum processors |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.DEPS | Dependency policy |
| STND.DRAFT | Drafting standard |
| STND.PROJ | Project constitution template |
| STND.TEST | Testing methods standard |
| VV | Correctness |

## Provisions

### Criteria

#### STND.CLASS.1 Class criteria

Binding. Instantiates GOV.12, GOV.13.

The human owner SHALL set as the class of work the most severe of these classes (GOV.13):

- the most severe row of the table of this provision whose consequence test or reliance test the work meets;
- the class that a selected profile requires (GOV.12);
- CSQ0, where the human owner states that a credible path to physical harm exists (GOV.15).

| Class | Consequence test | Reliance test |
| --- | --- | --- |
| CSQ0 | A credible consequence of an error is injury or death of a person, or severe environmental harm, directly or through a safety decision the output informs. | None. |
| CSQ1 | A credible consequence of an error is a major, hard-to-reverse loss, including destroyed equipment, loss of irreplaceable data or samples, a failed campaign, or a cost above the amount that STND.CLASS.3 has the classification state. | A relying party outside the project, or a system that acts unattended, relies on the output. |
| CSQ2 | A credible consequence of an error is a wrong decision, design, or reported result that is acted on before the error is detected, and whose correction needs rework beyond the unit of work that produced it. | An actor other than its author relies on the output, beyond the reliance that the test of CSQ3 allows. |
| CSQ3 | A credible consequence of an error is effort or money lost beyond the author's own time, or a wrong output that the verification of the work it feeds detects before reliance. | Only the author, or the actors of the author's immediate team, rely on the output, and only through work that is verified before it is relied upon. |
| CSQ4 | Work that meets no test of a more severe row; nothing relies on it before promotion (QA.11). | None. |

#### STND.CLASS.2 Doubtful test

Binding. Instantiates GOV.12.

Where it is in doubt whether work meets a test of the table of STND.CLASS.1, the work SHALL be treated as meeting it (GOV.12).

#### STND.CLASS.3 Cost threshold

Binding. Instantiates GOV.24.

Where the class of the project or of a component is CSQ2 or a more severe class, the classification SHALL state the amount of money above which a loss counts as a cost for the consequence test of CSQ1 in the table of STND.CLASS.1 (GOV.24).

#### STND.CLASS.4 Harm scenarios

Binding. Instantiates GOV.15.

An agent SHALL report to the human owner each scenario it identifies in which an error in the work is able to cause physical harm (GOV.15).

### Assignment

#### STND.CLASS.5 Classification record

Binding. Instantiates GOV.24, GOV.13.

The classification SHALL state, for the project and for each component given a less severe class, the class, the credible consequence and the reliance that set it, and the row of the table of STND.CLASS.1 whose test each meets (GOV.24). Where a more severe use of the project or of a component is planned, the classification SHALL state its expected class and the use that would occasion it (GOV.13, GOV.24).

#### STND.CLASS.6 Isolated components

Binding. Instantiates GOV.13.

Where a component receives a class less severe than the project's, the classification SHALL record evidence (VV.1) that it is an isolated component, including the coverage of each check through which its outputs reach an output of a more severe class (GOV.13).

#### STND.CLASS.7 Reclassification events

Binding. Instantiates GOV.14.

Whenever reliance on the work or its exposure grows, an agent reports a scenario under STND.CLASS.4, or an incident shows a credible consequence that the classification omits, the human owner SHALL reassess the class before a result of the work is next promoted, or the work is next released or relied upon at a more severe class (GOV.14). Until the human owner records the reassessment, the work SHALL NOT be relied upon in the use that occasioned it (GOV.14).

#### STND.CLASS.20 Proportionality judgment

Binding. Instantiates GOV.11.

The proportionality judgment for a result SHALL be the entry of the classification for the project or component that produced it (GOV.11). A promotion SHALL cite that entry (QA.11).

#### STND.CLASS.21 Expected class in design

Default, at every class. Instantiates DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7.

Where the classification records an expected class, the design of the work SHOULD admit, without rework of the design, the parts of the table of STND.CLASS.10, and of the provisions below LVL0 whose field `onset` gives that class, that apply from that class, and the contracts, schemas, provenance, language edition and subset, failure channel, dependencies, hardware, reduction order, and kept reference path that the obligations of that class ask of the work, with the reason for each choice that the expected class drives recorded in a decision record (DSGN.13, DSGN.4, DSGN.5, REPRO.4, REPRO.7). Before the reclassification, the work MAY omit each record that only an obligation of the expected class requires, other than the records of STND.CLASS.23 (GOV.11).

#### STND.CLASS.22 Reclassification obligations

Binding. Instantiates GOV.14, REPRO.1, QA.12, QA.7, GOV.47, GOV.42.

Before work is relied upon at a more severe class, the work done at the less severe class SHALL meet the obligations of that class through these steps (GOV.14):

- the regeneration of each result to be relied upon at the new class whose record lacks an input of REPRO.1 (REPRO.1);
- the label unverified on each result to be relied upon at the new class that was judged against criteria set after it was seen (QA.12);
- one review, at the independence of the row of the new class in the table of STND.CLASS.18, of the changes made since the last review at that independence, taken as one change, against the obligations of the new class (QA.7);
- the audit that STND.CLASS.19 requires before the reliance (GOV.47);
- the repetition, before the reliance, of each check that an obligation of the new class ties to an event that preceded the reclassification (GOV.14).

Existing source SHALL conform, at the next change that touches it, to each default of form or style that the new class first applies to it and on whose outcome no reliance at the new class turns (GOV.42).

### Application by class

#### STND.CLASS.10 Application by class

Default, at every class. Instantiates VV.1, VV.2, VV.4, VV.6, VV.10, REPRO.4, REPRO.10, REPRO.12, INTPR.6, INTPR.7, INTPR.8, INTPR.10, INTPR.11, INTPR.12, DSGN.2, DSGN.3, DSGN.4, DSGN.5, DSGN.15, QA.9, QA.14, RSRC.3.

Above the floor, work of CSQ3 and of every more severe class SHALL meet every obligation of VV, REPRO, INTPR, DSGN, SIMPL, RSRC, and QA in full, except each part in the table of this provision, which applies from the class that the table gives, and each part of a provision below LVL0 to which the field `onset` of that provision gives a class, which applies from that class (GOV.11). Work of CSQ4 MAY omit every obligation of these Articles above the floor, other than STND.CLASS.21 and the records of STND.CLASS.23 (GOV.11).

| From | Part |
| --- | --- |
| CSQ2 | Comparison of correctness evidence against a reference oracle produced without using the implementation it judges (VV.1). |
| CSQ2 | Confirmation of each cited source (VV.2). |
| CSQ2 | Validation against a real-world referent where one exists (VV.4). |
| CSQ2 | Provenance written with each output at production (REPRO.4). |
| CSQ2 | Versioning and review of each workflow (REPRO.10). |
| CSQ2 | Documentation of the limits of validity (INTPR.10). |
| CSQ2 | A schema for each data structure crossing an interface (DSGN.4). |
| CSQ2 | A contract for each external component and for hardware (DSGN.5). |
| CSQ2 | Verification of the invariants of each protocol for shared state (DSGN.15). |
| CSQ2 | A mechanism that tracks dependencies between results (QA.14). |
| CSQ2 | Time, memory, and cost recorded with each run (RSRC.3). |
| CSQ1 | Verification of each assembly and of the integrated system (VV.6). |
| CSQ1 | Run-time assertion of invariants where checking is cheap (VV.10). |
| CSQ1 | Checking of postconditions and invariants wherever checking costs less than a propagated wrong result (DSGN.2). |
| CSQ1 | Reporting of state and anomalies to the operator (INTPR.6, INTPR.7). |
| CSQ1 | Diagnostics captured by default (INTPR.8). |
| CSQ1 | Recording and verification of automated decisions other than agent actions, which GOV.48 covers at every class (INTPR.11). |
| CSQ1 | Regeneration by another actor or system before reliance (QA.9). |
| CSQ1 | An archived computational environment, so that each result is able to be regenerated after the original environment is gone (REPRO.12). |
| CSQ0 | Verification of each safety-related component by proof or by exhaustive checking of its state space; where the human owner records that neither is feasible, the reason, and evidence that includes comparison against a reference produced by an actor other than the author (VV.1). |
| CSQ0 | Mechanical checking of each contract of a safety-related component (DSGN.3). |
| CSQ0 | A recorded exercise in which a human skilled in the art resumes the work from its artifacts without the automation (INTPR.12). |

#### STND.CLASS.17 Hazard responses

Binding. Instantiates PRIME.13.

For work of CSQ0, the designed response to each hazard of the hazard analysis SHALL be tested (PRIME.13). For work of CSQ0, each change to a safety-related component SHALL be analyzed against the hazard analysis before release (PRIME.13).

#### STND.CLASS.23 Records below the expected class

Default, at every class. Instantiates REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3.

Where the classification records an expected class, work of CSQ4 SHOULD keep each record of the table of this provision that the provision beside it would ask of the work at that class, as that provision describes it (REPRO.1, REPRO.4, REPRO.9, VV.1, VV.3).

| Record | Provision |
| --- | --- |
| The basis of each tolerance | NUMER.11 |
| The random seeds and the identity of the computational environment of each result | REPRO.1 |
| Each lock file | STND.DEPS.12 |
| Each toolchain revision | STND.DEPS.8 |
| The source of each expected test value | STND.TEST.19 |
| Each observation that is unable to be acquired again, as acquired, with its acquisition record | MEAS.3, MEAS.4 |
| Each job on a quantum processor, with its execution record | HW.QPU.3 |

### Review independence

#### STND.CLASS.18 Reviewer independence

Default, at every class. Instantiates QA.8, QA.7.

A change SHALL be reviewed with the independence of the row of its class in the table of this provision and of every less severe row (QA.8).

| Class | Reviewer |
| --- | --- |
| CSQ0 | A human who did not author the change reviews each change to a safety-related component. |
| CSQ1 | A human reviews, before each promotion or release, the changes since the previous such review that affect a contract or a reported result, with the review record of each change and the departures that work reports state under AGENT.47. |
| CSQ2 | An actor not directed by the author performs the review; where the author is an agent, that actor is a human or an agent whose agent configuration differs from the author's in its model or in its instruction revision, whatever its tools. |
| CSQ3 | An actor other than the author: a human, or an agent, of the author's agent configuration or another, in a session, other than each session of the author, whose context holds nothing of the author's sessions except what it reads from the records of the work (QA.7). |

### Compliance audit

#### STND.CLASS.19 Audit interval

Binding. Instantiates GOV.47.

A project SHALL be audited at the interval, and by the auditor, of the row of its class in the table of this provision (GOV.47). Before work moved to CSQ2 or a more severe class is first relied upon at that class, the project SHALL be audited by the auditor of that class (GOV.47).

| Class | Interval | Auditor |
| --- | --- | --- |
| CSQ0 | Before each release, and at most 6 months after the previous audit | A human who is not an author of the audited work |
| CSQ1 | Before the first release, and at most 12 months after the previous audit | An actor who is not an author of the audited work; an agent auditor differs from every authoring agent in its model or in its instruction revision, whatever its tools |
| CSQ2 | Before a result is first relied upon, and at most 24 months after the previous audit | As for CSQ1 |
| CSQ3 | At most 36 months after the classification is adopted or after the previous audit, and when the project is retired | An actor who is not an author of the audited work; an agent is eligible |
| CSQ4 | When the project is retired | As for CSQ3 |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-09 | Adopted. |
| 1.1 | 2026-10-09 | Minor amendment (GOV.41): the reliance tests of STND.CLASS.1 follow GOV.12 (a system that acts unattended; the author or actors of the same unit of work); review drops its CSQ4 row; STND.CLASS.20 ties the proportionality judgment to the classification; reassessment and reference oracle replace review of the class and independent reference; the Terms no longer define Reviewer or Independent reference. |
| 1.1.1 | 2026-10-10 | Editorial amendment (GOV.41): the CSQ3 auditor of STND.CLASS.19 is named as the other rows name theirs, an actor who is not an author of the audited work; no obligation changes. |
| 1.2 | 2026-10-10 | Minor amendment (GOV.41): a credible consequence includes one reached through a foreseeable misuse of the work, so that the term no longer narrows the worst credible consequence of GOV.12 to the intended use. |
| 1.2.1 | 2026-10-10 | Editorial amendment (GOV.41): the front-matter field `withdrawn` lists the identifiers that revision 0.2 withdrew, so that a check is able to keep them from reuse (GOV.37); no obligation changes. |
| 1.2.2 | 2026-10-10 | Editorial amendment (GOV.41): the section References lists the documents this standard cites, as STND.DRAFT.34 requires; no obligation changes. |
| 1.3 | 2026-10-11 | Minor amendment (GOV.41): at CSQ1, STND.CLASS.18 has a human review the changes that affect a contract or a reported result before each promotion or release, rather than each change as it is made; each change still has the review of every less severe row. |
| 1.3.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative section Reading the standard states that the table of STND.CLASS.10 holds no part of Simplicity, citing SIMPL, which STND.CLASS.10 names, and References lists SIMPL; no obligation, permission, or defined meaning changes. |
| 1.4 | 2026-10-28 | Minor amendment (GOV.41): GOV.13 as amended in LVL0 revision 1.7 is carried: STND.CLASS.5 has the classification state the expected class of the project or a component and the use that would occasion it (ruling C1); STND.CLASS.3 asks the money threshold only where the class is CSQ2 or a more severe class, and the cost limb of the CSQ1 test in STND.CLASS.1 reads the amount that STND.CLASS.3 has the classification state (CC10); new STND.CLASS.21, a default, has the design of work with a recorded expected class admit the parts of that class without rework, with the reason for each choice the expected class drives in a decision record, and owes no other record of that class before the reclassification (ruling C2); new STND.CLASS.22, binding, has the work done at the less severe class meet the obligations of the new class before reliance there through one review of the accumulated changes against those obligations, the regeneration or the label unverified of each result to be relied upon, the audit of STND.CLASS.19, and each event-tied check repeated, deferring to the next change that touches the source only a default of form or style on whose outcome no reliance turns, and STND.CLASS.19 audits once before work moved to CSQ2 or a more severe class is first relied upon there (ruling C3); new STND.CLASS.23, a default, has work of CSQ4 with a recorded expected class keep the records of its table as the provisions that hold them at CSQ3 describe them, and STND.CLASS.10 excepts STND.CLASS.21 and those records from what work of CSQ4 omits (ruling C4); the CSQ3 reliance test of STND.CLASS.1 reads the author's immediate team, as GOV.12 does, and the Terms define Team (ruling C5); the CSQ3 row of STND.CLASS.18 counts an agent in a session other than each of the author's, whose context holds nothing of those sessions beyond the records of the work, as another actor, of the author's configuration or not, Session in the meaning of AGENT, and the CSQ2 row asks an agent configuration that differs in its model or its instruction revision, whatever its tools (ruling C6), as the CSQ1 and CSQ2 rows of STND.CLASS.19 now ask of an agent auditor; STND.CLASS.7 has the human owner reassess before a result of the work is next promoted, or the work is next released or relied upon at a more severe class (CC15). |
| 1.5 | 2026-10-28 | Minor amendment (GOV.41): STND.CLASS.10 applies each part of a provision below LVL0 from the class that the field onset of the provision gives, STND.CLASS.21 has the design admit the parts that the fields start at the expected class, and the Notes state the one rule by which the fields are set: a part applies from the row of the table whose named item it asks for, and otherwise from CSQ3. |
| 1.5.1 | 2026-10-28 | Editorial amendment (GOV.41): the Notes say that a mechanism of GOV.21 whose obligation work of CSQ4 may omit costs that work one citation of the defaults, and that the obligation it serves applies from the class that STND.CLASS.10 gives; no obligation, permission, or defined meaning changes. |
