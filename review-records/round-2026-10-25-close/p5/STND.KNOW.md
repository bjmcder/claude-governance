# Knowledge base and tags (STND.KNOW) 1.0.1

Adopted by The Custodian as revision 1.0 in ledger entry 94 (2026-10-20); revised to 1.0.1 in entry 151 (2026-10-25). This reading copy is composed from the per-provision files in STND/KNOW/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard fixes what a knowledge entry states, its kinds and form, the evidence levels and the reliance ceiling of each, how an entry is established, revalidated, superseded, and retracted, how an entry drawn from a project's workbench is made and reconciled, and the permanence and use of tags (GOV.32 to GOV.34, GOV.37). GOV.33 assigns the ceiling of each evidence level to a LVL2 standard; STND.KNOW.5 sets it. Every provision but STND.KNOW.12 and STND.KNOW.14 is binding, because it instantiates GOV, which the floor holds (GOV.10), or a prime directive, and a knowledge base shared across projects is read the same way by each of them; STND.KNOW.12 and STND.KNOW.14 are defaults (GOV.19) that apply from CSQ3. A provision imposes nothing on work that keeps and consults no knowledge entry. No provision names a tool (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Lesson, Research note, Reusable finding, and Workbench have the meanings that AGENT gives them; Protected data has the meaning that STND.THRT gives it.

| Term | Definition |
| --- | --- |
| Drawn entry | A knowledge entry whose claim a workbench entry or a research note of a project stated first. |
| Establishing review | The review of GOV.34 by which a knowledge entry becomes established. |
| Revalidation | A confirmation, after an entry is established, that its evidence still meets its evidence level over its domain of validity. |
| Facet | One part of the tag vocabulary, holding the tags of one kind of subject. |

## Notes

The evidence levels follow the names the Lexicon gives them, and each asks of its evidence what STND.CLASS.10 asks of VV.1 at the class of its ceiling. EVD0 asks that an actor other than the author regenerate the evidence from its records, as QA.9 asks from CSQ1. EVD1 holds evidence that meets VV.1 as applied at CSQ2, over the entry's whole domain of validity, a cited source confirmed under VV.2 included, which VV.1 counts as evidence. EVD2 holds partial evidence and sources not yet confirmed. EVD3 holds the rest. The ceilings step one class per level, from CSQ1 for EVD0 to CSQ4 for EVD3. No level carries reliance at CSQ0 without fresh verification, because STND.CLASS.10 asks safety-related components for proof, exhaustive checking, or an independent reference, which a knowledge entry is not. The independence of the establishing review also caps the ceiling (STND.KNOW.7), following the rows of STND.CLASS.18 read for the review of an entry: a human reviewer admits CSQ1, an agent of another configuration that the author does not direct admits CSQ2, and every other reviewer CSQ3, whatever the evidence. Because STND.CLASS.10 gives VV.1 the same content at CSQ1 and CSQ2, EVD0 and EVD1 differ by the regeneration of the evidence by another actor. Reliance above a ceiling needs the evidence that VV asks at the class concerned (GOV.33); the entry still informs the work.

STND.KNOW.6 never blocks work. An entry not yet established, one whose revalidation is overdue, and one relied on outside its stated domain of validity keep informing exploratory work and are relied on above CSQ4 only with fresh evidence. The step to CSQ4 on an overdue revalidation is deliberate: it costs nothing until reliance is sought, and then asks only the revalidation that restores the ceiling. The recommended interval of revalidation, at most 24 months, is a recommendation inside a binding provision; a knowledge base that records another interval departs from it by a recorded decision (PRIN.10). An entry is never altered in place (GOV.34), so its status follows from the records that cite it: the establishing review, each revalidation, whose stated next date governs over the earlier one, and each entry that supersedes or retracts it. A listing generated from those records shows that status for lookup, and is informative (GOV.39). Each supersession and retraction is notified to everything that relies on the entry (GOV.34, QA.13).

The workbench has the reach of one project (AGENT). A drawn entry therefore carries its evidence with it, or cites a record that every reader of the knowledge base retrieves, and names its source project by a reference that is not protected data, so that a reader of another project judges it without that project's records (STND.KNOW.10). No knowledge entry carries a secret, information from which a secret is inferred, or the protected data of the project it comes from (STND.KNOW.11), because a knowledge base reaches readers whom that project's threat model does not name (AGENT.43). An entry cites external material rather than reproducing it, so that the license terms of the material govern only its source. Once a knowledge base establishes an entry that a workbench held under AGENT.30, an agent of the project that learns of it records that fact by a new workbench entry (STND.KNOW.12), because AGENT.34 forbids altering the old one; later work relies on the established entry as knowledge, and on the workbench entry only as evidence. A proposal held in a workbench carries the project's name and a number of that workbench, and takes an identifier of the knowledge base only on establishment (STND.KNOW.3), so that two projects never number the same identifier.

The kinds of STND.KNOW.2 follow the items that AGENT.26 and AGENT.27 ask agents to propose, and add the dependency set that the dependency policy leaves to the knowledge base: a set of external components that has served together across projects, with the regime in which it served. An entry of kind Result states whether its result is promoted and whether it is unverified, as AGENT.27 asks of the proposal (STND.KNOW.1). A knowledge entry for a tool describes the tool and states where it is kept; the tool is not itself an entry (custodians' interpretation of GOV.32, 2026-10-11).

Which knowledge base serves a project is stated in its project constitution or, where none is designated, AGENT.30 holds proposed entries in the workbench. The space of the governance corpus for knowledge entries (KNOW), with one directory per domain (STND.IDENT.15), and the tag vocabulary of that corpus (TAG), with one directory per facet, are the custodians' shared knowledge base and tags. A facet is registered as a mnemonic (STND.IDENT.19); a tag is added by a file in its facet's directory. The component facet (TAG.COMP) is local to a project.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| GOV | Governance |
| INTPR | Interpretability |
| KNOW | Knowledge base |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.IDENT | Identifier scheme and mnemonic register |
| STND.THRT | Threat-model template |
| TAG | Tag vocabulary |
| TAG.COMP | Component (project-local) |
| VV | Correctness |

## Provisions

### Entries

#### STND.KNOW.1 Knowledge entry content

Binding. Instantiates GOV.33, GOV.34, QA.11, PRIME.3.

Each knowledge entry SHALL state its claim, its kind, its evidence, its evidence level, its domain of validity, its author, its date, and the schedule of its revalidation (GOV.33, GOV.34). An entry of kind Result SHALL state whether the result is promoted and whether it is unverified (QA.11, PRIME.3).

#### STND.KNOW.2 Knowledge entry kinds

Binding. Instantiates GOV.32.

The kind of a knowledge entry SHALL be exactly one kind of the table of this provision (GOV.32).

| Kind | Claim |
| --- | --- |
| Lesson | A lesson, with the units of work or the trend that reveal it |
| Method | A method or practice and the regime in which it serves |
| Tool | What a tool does, the regime in which it serves, and where it is kept |
| Result | A research result |
| Negative result | An approach that failed, and the conditions under which it failed |
| Anomaly | An explained anomaly and its cause |
| Dependency set | A set of external components that served together, and the regime in which it served |
| Other finding | A reusable finding of no other kind of this table |

#### STND.KNOW.3 Knowledge entry form

Binding. Instantiates GOV.32, GOV.37, REPRO.12, AGENT.30, INTPR.13.

Each knowledge entry SHALL be kept as a plain-text file under version control (GOV.32, REPRO.12). An entry of a knowledge base SHALL carry an identifier of the form that STND.IDENT.15 gives (GOV.37). An entry that a workbench holds under AGENT.30 SHALL carry the name of its project and a number that no other entry of that workbench carries (GOV.37, AGENT.30, INTPR.13).

### Reliance

#### STND.KNOW.4 Evidence level assignment

Binding. Instantiates GOV.33.

A knowledge entry SHALL take the first evidence level, in the order of the table of this provision, whose evidence the entry's evidence meets (GOV.33).

| Level | Name | Evidence |
| --- | --- | --- |
| EVD0 | Verified | Evidence that meets VV.1, as STND.CLASS.10 applies it at CSQ1, over the whole stated domain of validity, regenerated from its records by an actor other than the entry's author (QA.9) |
| EVD1 | Confirmed | Evidence that meets VV.1, as STND.CLASS.10 applies it at CSQ2, over the whole stated domain of validity |
| EVD2 | Reported | Evidence that meets VV.1 for at least one case within the stated domain of validity, or a cited source not yet confirmed under VV.2 |
| EVD3 | Anecdotal | Every other support, an observation or an experience without a record that meets VV.1 included |

#### STND.KNOW.5 Reliance ceilings by level

Binding. Instantiates GOV.33.

Except as STND.KNOW.6 and STND.KNOW.7 provide, the reliance ceiling of a knowledge entry SHALL be the consequence class that the table of this provision gives for its evidence level (GOV.33).

| Level | Reliance ceiling |
| --- | --- |
| EVD0 | CSQ1 |
| EVD1 | CSQ2 |
| EVD2 | CSQ3 |
| EVD3 | CSQ4 |

#### STND.KNOW.6 Provisional reliance ceiling

Binding. Instantiates GOV.33, GOV.34.

Until a knowledge entry is established, its reliance ceiling SHALL be CSQ4 (GOV.33, GOV.34). While a revalidation of an established knowledge entry is overdue under its schedule, its reliance ceiling SHALL be CSQ4 (GOV.33, GOV.34). For reliance outside its stated domain of validity, the reliance ceiling of a knowledge entry SHALL be CSQ4 (GOV.33).

### Lifecycle

#### STND.KNOW.7 Establishing review record

Binding. Instantiates GOV.33, GOV.34, QA.8.

The establishing review of a knowledge entry SHALL confirm that the entry's evidence meets its evidence level over its stated domain of validity (GOV.33, GOV.34). The record of that review SHALL cite the entry and state the revision reviewed, the reviewer, and the verdict (GOV.34). The reliance ceiling of the entry SHALL be no more severe than the class that the table of this provision gives for the actor that performed its establishing review (GOV.33, QA.8).

| Establishing reviewer | Most severe ceiling |
| --- | --- |
| A human other than the entry's author | CSQ1 |
| An agent not directed by the author and of an agent configuration other than the author's | CSQ2 |
| Another actor other than the author | CSQ3 |

#### STND.KNOW.8 Revalidation schedule

Binding. Instantiates GOV.34.

The schedule of revalidation of a knowledge entry SHALL name the events after which its evidence no longer holds, and the date of its next revalidation (GOV.34). That date SHOULD fall at most 24 months, inclusive, after the entry was established or last revalidated (GOV.34). Each revalidation SHALL be recorded in a record that cites the entry and states the evidence level it confirms and the date of the next revalidation (GOV.34).

#### STND.KNOW.9 Superseded and retracted entries

Binding. Instantiates GOV.34.

Where a revalidation or a later finding shows that the evidence of a knowledge entry no longer meets its evidence level, a new entry SHALL supersede or retract it (GOV.34). The superseding or retracting entry SHALL cite the entry it supersedes or retracts (GOV.34). The superseded or retracted entry SHALL remain in the knowledge base unaltered (GOV.34).

### Workbench entries

#### STND.KNOW.10 Drawn entry sources

Binding. Instantiates GOV.32, GOV.33, AGENT.38.

A drawn entry SHALL name, by a reference that is not protected data, the project whose workbench holds the workbench entry or research note that it cites (GOV.32, AGENT.38). A drawn entry SHALL state its evidence in itself or in a record that each reader of the knowledge base is able to retrieve (GOV.33).

#### STND.KNOW.11 Secrets in knowledge entries

Binding. Instantiates PRIME.10, AGENT.43.

A knowledge entry SHALL NOT contain a secret (PRIME.10). A knowledge entry SHALL NOT contain information from which a secret is able to be inferred (PRIME.10, AGENT.43). A knowledge entry SHALL NOT contain protected data of the project from which it comes, as that project's threat model lists it under STND.THRT.3 (PRIME.10).

#### STND.KNOW.12 Established workbench proposals

Default. Instantiates AGENT.30, INTPR.13.

Where an agent of a project learns that a knowledge base has established an entry that the project's workbench holds under AGENT.30, the agent SHOULD record in that workbench a new entry that cites the identifier of the established entry (AGENT.30, INTPR.13).

### Tags

#### STND.KNOW.13 Tag permanence

Binding. Instantiates GOV.37.

A tag SHALL NOT be removed from the tag vocabulary (GOV.37). A deprecated tag SHALL name the tag that replaces it, or state that no tag replaces it (GOV.37).

#### STND.KNOW.14 Tags on knowledge entries

Default. Instantiates AGENT.28, QA.2.

Each knowledge entry SHOULD carry the tags of the tag vocabulary that name its subject, its method, and each hardware type it concerns (AGENT.28, QA.2).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Notes cite the knowledge space KNOW, the tag vocabulary TAG, and the facet TAG.COMP of the governance corpus, which they named, and References lists KNOW, TAG, and TAG.COMP; no obligation, permission, or defined meaning changes. |
