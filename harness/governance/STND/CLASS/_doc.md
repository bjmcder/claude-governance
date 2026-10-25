---
id: "STND.CLASS"
level: "LVL2"
kind: "standard"
title: "Consequence-class criteria"
status: "adopted"
revision: "1.3.1"
adopted: "2026-10-09"
adopted_by: "The Custodian"
instantiates: ["GOV.12", "GOV.11", "QA.8", "GOV.47"]
rank: null
waivable: false
withdrawn: ["STND.CLASS.8", "STND.CLASS.9", "STND.CLASS.11", "STND.CLASS.12", "STND.CLASS.13", "STND.CLASS.14", "STND.CLASS.15", "STND.CLASS.16"]
---

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

Work of CSQ3 meets the seven proportioned Articles as LVL0 writes them. The table of STND.CLASS.10 lists what waits for a more severe class and what a more severe class adds. The table holds no part of Simplicity (SIMPL). Work of CSQ4 meets only the floor, which includes the mechanisms of GOV.21, because GOV belongs to the floor. The five classes resemble the software levels A to E of DO-178C and the graded approach of nuclear quality assurance; no obligation follows from the resemblance.

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
| SIMPL | Simplicity |
| STND.DRAFT | Drafting standard |
| VV | Correctness |

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
