# Consequence-class criteria (STND.CLASS) 1.3

Adopted by The Custodian as revision 1.0 in ledger entry 14 (2026-10-09); revised to 1.1 in entry 16 (2026-10-09), 1.1.1 in entry 21 (2026-10-10), 1.2 in entry 22 (2026-10-10), 1.2.1 in entry 24 (2026-10-10), 1.2.2 in entry 36 (2026-10-10), and 1.3 in entry 58 (2026-10-11). This reading copy is composed from the per-provision files in STND/CLASS/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.CLASS.8, STND.CLASS.9, STND.CLASS.11, STND.CLASS.12, STND.CLASS.13, STND.CLASS.14, STND.CLASS.15, and STND.CLASS.16.

## Purpose and scope

This standard fixes the criteria that place work in a consequence class (GOV.12), how the classification records and revises a class (GOV.13, GOV.14, GOV.24), what each class requires above the floor (GOV.11), the independence of review by class (QA.8), and the interval of compliance audit (GOV.47). STND.CLASS.10 and STND.CLASS.18 are defaults (GOV.19): a project constitution replaces one by a recorded decision (REPRO.7) with an alternative that meets the same outcome. The others, STND.CLASS.17 included, are binding, because they instantiate GOV or a prime directive, which belong to the floor (GOV.10).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Every other part of this document is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Credible consequence | A consequence reached from an error in the work by a chain of events, each of which is able to occur in the intended use of the work or in a foreseeable misuse of it. |
| Isolated component | A component whose outputs reach an output of a more severe class only through a check verified at that class to detect and reject every error of the component able to cause a consequence of that class, and that shares no resource whose exhaustion or corruption by it is able to impair a component of the more severe class. |
| Safety-related component | A component an error in which has a credible consequence of class CSQ0. |
| Agent configuration | The model, the instruction revision, and the tools of an agent, as REPRO.11 records them. |

## Reading the standard

The consequence test and the reliance test are independent, and the more severe one sets the class. A class attaches to a use of the work, not to its code (GOV.14): the same code is CSQ4 in a notebook, CSQ2 once an actor other than its author builds on it, and CSQ1 once a relying party outside the project does. Growth of reliance includes the promotion of a result for a new use, the first output that leaves the project, and the first command to physical hardware.

| Work | Class | What sets the class |
| --- | --- | --- |
| Software that computes trip setpoints for the protection system of a research reactor | CSQ0 | An error is able to defeat a protective action. |
| Firmware of a radiation survey instrument whose reading decides whether an area is entered | CSQ0 | A safety decision rests on the reading. |
| Control software for a cryostat, where a fault destroys a detector but cannot injure a person | CSQ1 | Loss of equipment. |
| A kinetics code whose results appear in a journal article | CSQ2 | An error leads to a wrong published result. |
| A file-format converter checked when the analysis it feeds is verified | CSQ3 | That verification detects an error. |
| A notebook that explores a new numerical method | CSQ4 | Nothing relies on it before promotion. |

Work of CSQ3 meets the seven proportioned Articles as LVL0 writes them. The table of STND.CLASS.10 lists what waits for a more severe class and what a more severe class adds. Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor. The five classes resemble the software levels A to E of DO-178C and the graded approach of nuclear quality assurance; no obligation follows from the resemblance.

Revision 0.2 withdrew identifiers 8, 9, and 11 to 16, which are not reused (GOV.37). Each provision is one file, `STND/CLASS/<n>.md`, and each table is named in the field `defines`. The lineage and drafting checks read every provision, but no check yet tests a project's classification against this standard, so each provision is checked by a reader for its content. Promotion (QA.11) governs every report of a result at every class, as Normative Language requires; work of CSQ4 needs no review until it is promoted or released, because it leaves CSQ4 when another actor relies on it.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| STND.DRAFT | Drafting standard |
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
| CSQ1 | A credible consequence of an error is a major, hard-to-reverse loss, including destroyed equipment, loss of irreplaceable data or samples, a failed campaign, or a cost above the amount of STND.CLASS.3. | A relying party outside the project, or a system that acts unattended, relies on the output. |
| CSQ2 | A credible consequence of an error is a wrong decision, design, or reported result that is acted on before the error is detected, and whose correction needs rework beyond the unit of work that produced it. | An actor other than its author relies on the output, beyond the reliance that the test of CSQ3 allows. |
| CSQ3 | A credible consequence of an error is effort or money lost beyond the author's own time, or a wrong output that the verification of the work it feeds detects before reliance. | Only the author, or actors of the same unit of work, rely on the output, and only through work that is verified before it is relied upon. |
| CSQ4 | Work that meets no test of a more severe row; nothing relies on it before promotion (QA.11). | None. |

#### STND.CLASS.2 Doubtful test

Binding. Instantiates GOV.12.

Where it is in doubt whether work meets a test of the table of STND.CLASS.1, the work SHALL be treated as meeting it (GOV.12).

#### STND.CLASS.3 Cost threshold

Binding. Instantiates GOV.24.

The classification SHALL state the amount of money above which a loss counts as a cost for the consequence test of CSQ1 in the table of STND.CLASS.1 (GOV.24).

#### STND.CLASS.4 Harm scenarios

Binding. Instantiates GOV.15.

An agent SHALL report to the human owner each scenario it identifies in which an error in the work is able to cause physical harm (GOV.15).

### Assignment

#### STND.CLASS.5 Classification record

Binding. Instantiates GOV.24.

The classification SHALL state, for the project and for each component given a less severe class, the class, the credible consequence and the reliance that set it, and the row of the table of STND.CLASS.1 whose test each meets (GOV.24).

#### STND.CLASS.6 Isolated components

Binding. Instantiates GOV.13.

Where a component receives a class less severe than the project's, the classification SHALL record evidence (VV.1) that it is an isolated component, including the coverage of each check through which its outputs reach an output of a more severe class (GOV.13).

#### STND.CLASS.7 Reclassification events

Binding. Instantiates GOV.14.

Whenever reliance on the work or its exposure grows, an agent reports a scenario under STND.CLASS.4, or an incident shows a credible consequence that the classification omits, the human owner SHALL reassess the class (GOV.14). Until the human owner records the reassessment, the work SHALL NOT be relied upon in the use that occasioned it (GOV.14).

#### STND.CLASS.20 Proportionality judgment

Binding. Instantiates GOV.11.

The proportionality judgment for a result SHALL be the entry of the classification for the project or component that produced it (GOV.11). A promotion SHALL cite that entry (QA.11).

### Application by class

#### STND.CLASS.10 Application by class

Default. Instantiates VV.1, VV.2, VV.4, VV.6, VV.10, REPRO.4, REPRO.10, REPRO.12, INTPR.6, INTPR.7, INTPR.8, INTPR.10, INTPR.11, INTPR.12, DSGN.2, DSGN.3, DSGN.4, DSGN.5, DSGN.15, QA.9, QA.14, RSRC.3.

Above the floor, work of CSQ3 and of every more severe class SHALL meet every obligation of VV, REPRO, INTPR, DSGN, SIMPL, RSRC, and QA in full, except each part in the table of this provision, which applies from the class that the table gives (GOV.11). Work of CSQ4 MAY omit every obligation of these Articles above the floor (GOV.11).

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

### Review independence

#### STND.CLASS.18 Reviewer independence

Default. Instantiates QA.8, QA.7.

A change SHALL be reviewed with the independence of the row of its class in the table of this provision and of every less severe row (QA.8).

| Class | Reviewer |
| --- | --- |
| CSQ0 | A human who did not author the change reviews each change to a safety-related component. |
| CSQ1 | A human reviews, before each promotion or release, the changes since the previous such review that affect a contract or a reported result, with the review record of each change and the departures that work reports state under AGENT.47. |
| CSQ2 | An actor not directed by the author performs the review; where the author is an agent, that actor is a human or an agent of a different agent configuration. |
| CSQ3 | An actor other than the author; an agent is eligible (QA.7). |

### Compliance audit

#### STND.CLASS.19 Audit interval

Binding. Instantiates GOV.47.

A project SHALL be audited at the interval, and by the auditor, of the row of its class in the table of this provision (GOV.47). Before work is relied upon at a more severe class, the project SHALL be audited by the auditor of that class (GOV.47).

| Class | Interval | Auditor |
| --- | --- | --- |
| CSQ0 | Before each release, and at most 6 months after the previous audit | A human who is not an author of the audited work |
| CSQ1 | Before the first release, and at most 12 months after the previous audit | An actor who is not an author of the audited work; an agent auditor has an agent configuration different from that of every authoring agent |
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
