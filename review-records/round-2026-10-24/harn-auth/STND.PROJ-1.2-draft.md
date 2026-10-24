# Project constitution template (STND.PROJ) 1.2

Adopted by The Custodian as revision 1.0 in ledger entry 96 (2026-10-20); revised to 1.1 in entry 99 (2026-10-21) and 1.2 in entry 117 (2026-10-24). This reading copy is composed from the per-provision files in STND/PROJ/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard fixes what a project constitution holds (GOV.20, GOV.21): one section for each mechanism that LVL0 requires of every project, the classification and its judgments, the places where the work's notes, workbench, knowledge, and secrets are kept, the authorizations in force, and, for work that drives physical hardware, its safety instruments. A filled copy is a LVL3 instrument that the project's human owner adopts (GOV.41). A section states its content in full or adopts by citation the provisions of an adopted LVL2 standard (STND.PROJ.2), so that a project takes the defaults, the agent instructions, the dependency policy, and the threat-model template without restating them, and a section whose content the project's class does not yet ask for says so (STND.PROJ.1). STND.PROJ.3 recommends the standing authorizations that let routine work run unattended, and the roles to which each extends, and STND.PROJ.5 a discipline for the operating cost of agents, each proposed once at the project's start (STND.DRAFT.42). STND.PROJ.1 to STND.PROJ.3 and STND.PROJ.5 are binding, because each instantiates GOV or GUARD, which the floor holds (GOV.10); STND.PROJ.3 and STND.PROJ.5 are recommendations within a binding provision. STND.PROJ.4, on the form of the files, and STND.PROJ.6 and STND.PROJ.7, on the form of an authorization of a remote write and its kinds, are defaults (GOV.19). The standard names no tool or method (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Capability level, Lead agent, Implementing agent, and Research agent have the meanings that STND.CREW gives them.

| Term | Definition |
| --- | --- |
| Section | A part of a project constitution under one heading, named by a row of the table of STND.PROJ.1. |
| Project template | The directory `_PROJECT/NAME` of the governance corpus, which holds the document file of a project constitution and one example file of each kind of project instrument. |

## Notes

The sections follow GOV.21 and the conforming work that AGENT left to this template: the workbench, the knowledge base, the store of non-credential secrets, the vocabulary of access descriptors, and the authorization for read-only research retrieval. A section that adopts a provision of STND.DFLT by citation adopts its content as the project's own; STND.DFLT.1 still keeps the defaults themselves from applying once a constitution exists. A standing authorization for research retrieval that the human owner has granted is entered once in each covered project's own ledger and cited in the section Authorizations; its bounds are the human owner's, at LVL3 (GOV.18).

The sections ask for what each mechanism is, not for a plan of the work. Every row other than its parts that STND.CLASS.10 defers is required at every class, because GOV.21 requires each mechanism of every project; a part that STND.CLASS.10 applies only from a class more severe than the project's, such as regeneration before reliance (QA.9) below CSQ1, is stated as not applying, so the template raises no floor (GOV.11). A verification and validation plan, budgets, and the other content that a profile asks for are recorded where that profile asks. The project template holds the files for authorizations, axioms, hazards, safe ranges of actuation, rulings, waivers, and the reserved-action register, so that each such instrument is a file the ledger pins (STND.PROJ.4).

The standing authorizations of STND.PROJ.3 are those the custodian found needed for unattended routine work, each scoped so that it reaches no reserved action. Removal of a dependency is covered only where reinstalling its pinned revision from a named source restores it, so that the removal is recoverable (GUARD.5). Machine-local settings are covered only where the prior value is recorded and restorable, and never for the store of secrets, the configuration that settles an agent's tier, a setting that enables a security or integrity check, a setting that selects a source or destination of network access or runs a program without a request, or a conventional location of secrets or credentials, so that no setting widens another authorization. Commits to a private remote repository never rewrite or delete history, a branch, or a tag, never reach a release branch or a branch whose update publishes or deploys, and lapse when the repository no longer meets the human owner's record. Every release, publication, and other remote write whose effect is irrevocable stays with the human owner or is authorized per action (PRIME.6, GUARD.5, GUARD.6, GUARD.11); no standing authorization covers one. A request made under the research authorization carries no secret (AGENT.43).

Each proposed authorization states the roles of STND.CREW to which it extends, because an authorization reaches a directed agent only where it says so (GUARD.12). At the custodian's direction of 2026-10-21, the authorization for research retrieval extends to research agents alone, so that, unless the human owner authorizes otherwise, research agents are the only agents that make network access to retrieve information for research, and the agents that install dependencies or add commits to a remote repository reach the network only under those authorizations. The extension is a proposal: it limits network access made for research only where the human owner adopts it in the project constitution, at LVL3 (GOV.18), and a human owner who wants another extension states it there, in the field of the authorization file that names the agents to which it is delegable. Reviewers and auditors that need a source confirmed, and the preparer of a release that checks advisories under STND.DEPS.7, ask the lead agent for a research agent; an audit that needs a dependency installed asks the lead agent likewise. Where the work has no delegation, the human owner extends the research authorization to the lead agent in the constitution. A constitution adopted before this revision keeps its authorizations, which extend as their text says; one silent on roles extends to no directed agent (GUARD.12) until the human owner amends it.

STND.PROJ.5 lets the human owner mark, once, the capability levels whose assignment needs a ruling, the most capable and costly levels in particular, so that an assignment to one waits for the ruling while every other assignment proceeds within the authorized estimate (STND.CREW.21). A discipline that only marks levels would otherwise set aside AGENT.6 and AGENT.10, which apply where no discipline is set, so the proposed discipline keeps the estimate in force for every unit and AGENT.10 for every assignment to a level it does not mark. The choice of discipline is the human owner's under GUARD.14; the proposal asks for no decision that LVL0 does not assign (STND.DRAFT.42).

STND.PROJ.6 and STND.PROJ.7 give an authorization of a remote write a form that a reader and a harness decide alike, so that a derived configuration lets a write that the authorization names by destination and kind proceed without referral (STND.HARN.18, STND.HARN.29). A destination is named by its whole address, as in `https://git.example.org/team/work.git` for a repository or `https://git.example.org/team/work` for its tracker, and a write is matched to it only as a whole, so that no address that merely begins or ends like it is covered. The branches of the kind commit are named for the same reason: STND.PROJ.3 proposes commits only to branches other than release branches and branches whose update publishes or deploys, and a list of names is what a configuration is able to compare. An address carries no credential, because delegating access is the human owner's and a record never holds one (AGENT.45, PRIME.10). The field `provisioned` records the human owner's judgment that STND.PROJ.3 asks for a private remote repository; a write to a destination outside the provisioned environment is a transmission beyond it, which GUARD.11 authorizes only per action, so the table of STND.PROJ.7 marks every kind irrevocable there. Publication and release are irrevocable wherever they go (GUARD.11). The marks restate no rule: they apply GUARD.11 to each kind, and a standing authorization that covers a marked kind has no effect (GUARD.11, STND.HARN.29). The field `expires` is a time, because a harness compares it with the time of each write; an authorization whose duration is a condition, such as lapsing when a repository stops meeting the human owner's record, states a time as well, and lapses at the earlier of the two. The kind other keeps the list closed while letting an authorization cover a write that no other row names; a harness that does not know a kind refers its writes (STND.HARN.19). STND.PROJ.6 and STND.PROJ.7 are defaults with the onset of REPRO.12 and INTPR.12 under STND.CLASS.10: they apply from CSQ3, and work of CSQ4 may keep its authorizations in another form, whose remote writes a derived configuration then refers. Neither raises the floor (GOV.11): GUARD.10 already asks that an authorization name its class of actions, its scope, and its duration, and the fields state those for a remote write at the cost of one record.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CREW | Agent roles standard |
| STND.DEPS | Dependency policy |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.HARN | Harness specification |

## Provisions

### Contents

#### STND.PROJ.1 Constitution sections

Binding. Instantiates GOV.20, GOV.21, GOV.11.

A project constitution SHALL hold one section for each row of the table of this provision, stating the content that its row gives (GOV.20, GOV.21). Where STND.CLASS.10 applies the obligation that a part of a row's content instantiates only from a class more severe than the project's, the section MAY state that the part does not apply (GOV.11).

| Section | Content |
| --- | --- |
| Identity | The project's name, purpose, and non-goals (SIMPL.10); a reference to the governance that designates the human owner (PRIN.1); the collaborators, and the route by which external contributions are accepted (QA.7); the software that the human owner classifies as agents or as automation (GOV.51); the owner of each interface shared beyond the project (DSGN.6) |
| Classification | The value of each attribute that the selector table of an adopted profile gives; the profiles selected, and each profile applied by analogy with its analogue (GOV.24, GOV.29); the components that hold domain items of each selected profile, with the execution paths of each by hardware type; the consequence class (GOV.13); the proportionality judgment (GOV.11) |
| Work process | How each unit of work is planned, executed, reviewed, and audited (QA.2); the stopping rule (QA.3) |
| Defects | Where defects are recorded, how blocking defects are marked, and the schedule of tracked ones (QA.4) |
| Review and release | Who reviews, and the independence that each class requires (QA.7, QA.8); regeneration before reliance (QA.9); promotion (QA.11); the release decision and its gate (QA.10) |
| Correction | The mechanism of correction propagation (QA.13) |
| Incidents | The incident mechanism (QA.15) |
| Dependencies | The dependency management mechanism (REPRO.9) |
| Records | The locations of the decision record, provenance, environment captures, and the ledger; the retention of records and their formats (REPRO.12); the independent copy of irreplaceable data (REPRO.13) |
| Working notes | The location of the working-notes workspace (INTPR.5) |
| Workbench | The location of the workbench, under version control and apart from the working-notes workspace (AGENT.35, AGENT.36) |
| Knowledge base | The knowledge base designated for the work, or the statement that none is designated (AGENT.30) |
| Secret store | The location of the store of AGENT.44, outside version control, every record, and the working-notes workspace; the accounts that read it; its protection under the threat model; and that no archive, backup, or transfer of the work carries it; or the statement that the work keeps none |
| Access descriptors | The vocabulary of access descriptors (AGENT.23), or the statement that the work makes no network access |
| Threat model | The threat model (GUARD.16) |
| Reserved actions | The reserved-action register and its exempt classes (GUARD.4, GUARD.7) |
| Authorizations | The authorization mechanism (GUARD.10); each standing authorization in force, with its scope, its duration, and the agents or roles of agents to which it extends (GUARD.11, GUARD.12); the authorization for read-only research retrieval, with its purpose, its scope, its bounds on items and volume per research effort, and the agents or roles of agents to which it extends, or the statement that none is granted (GUARD.8, GUARD.13); the discipline for the operating cost of agents, with the capability levels that it marks for the human owner's ruling or the statement that it marks none, or the statement that no discipline is set (GUARD.14) |
| Agent instructions | The agent instructions, and the form of the findings and justification statement (GOV.48, PRIME.14) |
| Configuration | The configuration, unalterable by an agent, that settles the tier of an agent's actions, or the statement that none does (GUARD.2); the other configuration of agents and tools, and who changes it (GOV.49) |
| Architecture | The recorded dependency structure of the components (DSGN.7) |
| Physical hardware | Where the work drives physical hardware, the hazard analysis, the safe state, and the safe range of actuation (PRIME.13) |
| Exceptions | The logs of waivers (GOV.44), exceptions (PRIN.10), dissent (REPRO.8), and rulings (GOV.3) |

#### STND.PROJ.2 Sections adopted by citation

Binding. Instantiates GOV.21.

A section MAY state its content by citing each provision of an adopted LVL2 standard that it adopts as the project's own (GOV.21).

### Authorizations

#### STND.PROJ.3 Proposed standing authorizations

Binding. Instantiates GUARD.10, GUARD.11, GUARD.12.

An agent that drafts a project constitution SHOULD propose to the human owner, in its section Authorizations, each standing authorization of the table of this provision, with its scope, its duration, and the agents to which it extends (GUARD.10, GUARD.11, GUARD.12).

| Class of actions | Scope | Extends to |
| --- | --- | --- |
| Installing, updating, and removing dependencies | Only from the sources that the authorization names, within the number of packages and the volume per change that it states, each verified under STND.DEPS.6 and installed without elevated privilege, and each removal restorable by reinstalling its pinned revision from a named source | The lead agent and implementing agents |
| Changing machine-local settings | Within the provisioned privilege, for a setting whose prior value is recorded and restorable, other than the store of AGENT.44, a configuration that settles the tier of an agent's actions, a setting that enables a check of security or integrity, a setting that selects a source or destination of network access, a setting that runs a program without a request, and a location that holds secrets or credentials by convention | The lead agent and implementing agents |
| Read-only research retrieval | For a stated purpose, from sources of a stated kind, within bounds on items and volume per research effort | Research agents alone |
| Adding commits to a private remote repository | Where the human owner records that repository as part of the provisioned environment and as readable only by those whom the threat model trusts, to branches other than release branches and branches whose update publishes or deploys, without rewriting or deleting history, a branch, or a tag, and lapsing when the repository no longer meets that record | The lead agent, implementing agents, and each agent that merges into a branch of the work |

#### STND.PROJ.5 Proposed cost discipline

Binding. Instantiates GUARD.14.

An agent that drafts a project constitution SHOULD propose to the human owner, in its section Authorizations, a discipline for the operating cost of agents that states the capability levels whose assignment needs the human owner's ruling and keeps the effort estimate of AGENT.6 in force for every unit of work and the assignment of AGENT.10 in force for every assignment to a level that it does not mark (GUARD.14).

### Form

#### STND.PROJ.4 Constitution files

Default. Instantiates REPRO.12, INTPR.12.

A project constitution SHOULD be kept as a copy of the project template, with its sections in the document file and the reserved-action register and each authorization, axiom, hazard, safe range of actuation, ruling, and waiver in an instrument file of its kind (REPRO.12, INTPR.12).

#### STND.PROJ.6 Remote-write authorization fields

Default. Instantiates REPRO.12, INTPR.12.

Where an authorization covers a remote write, its instrument file SHOULD hold the fields of the table of this provision, each with a value of the form that its row gives (REPRO.12, INTPR.12).

| Field | Value |
| --- | --- |
| status | `draft` until the human owner grants the authorization, `adopted` while it is granted, and `retired` once it is revoked or lapses |
| grantor | The role label of the human owner |
| recorded | The date of the grant, as an ISO 8601 date |
| expires | The time at which the authorization lapses, as an ISO 8601 time with its UTC offset |
| standing | `true` for a standing authorization, and `false` for one per action |
| remote_writes | A list of one object per destination, with `destination`, the address by which the write reaches the destination, in full and without a credential; `kinds`, the kinds of write of the table of STND.PROJ.7 that the authorization covers there; `branches`, the name of each branch that the kind commit covers there, or an empty list where the kinds omit commit; and `provisioned`, `true` where the human owner records the destination as part of the provisioned environment and as readable only by those whom the threat model trusts, and otherwise `false` |

#### STND.PROJ.7 Kinds of remote write

Default. Instantiates REPRO.12, INTPR.12.

An authorization file SHOULD name each kind of remote write that it covers by a word of the table of this provision, whose last column marks the kinds whose effect is irrevocable (REPRO.12, INTPR.12, GUARD.11).

| Kind | Remote write | Effect irrevocable |
| --- | --- | --- |
| commit | Adding commits to a named branch of a remote repository, without rewriting or deleting history, a branch, or a tag | At a destination not recorded as provisioned |
| post | Adding an issue, a comment, or a review to a remote tracker, without editing, closing, or deleting one | At a destination not recorded as provisioned |
| publish | Publication or release | Always |
| transmit | Transmission of data beyond the provisioned environment, other than publication or release | Always |
| other | A remote write of another kind, which the scope of the authorization describes | As the scope states, and always at a destination not recorded as provisioned |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.1 | 2026-10-21 | Minor amendment (GOV.41), conforming on the adoption of STND.CREW: the section Authorizations states the agents or roles to which each authorization extends and the capability levels that the cost discipline marks for ruling (STND.PROJ.1); each proposed standing authorization states the roles to which it extends, read-only research retrieval to research agents alone (STND.PROJ.3); new STND.PROJ.5 proposes a discipline for the operating cost of agents that states the capability levels whose assignment needs the human owner's ruling and keeps AGENT.6 in force for every unit and AGENT.10 for every assignment to an unmarked level. Constitutions adopted before this revision keep their authorizations and discipline as their text says (GUARD.12, GUARD.14), and state the new content of the section Authorizations at their next amendment. |
| 1.2 | 2026-10-24 | Minor amendment (GOV.41): new STND.PROJ.6 gives the fields of an authorization file that covers a remote write (status, grantor, date recorded, expiry as a time with its UTC offset, standing or per action, and one entry per destination naming its whole address without a credential, its kinds of write, the branches of a commit, and whether the human owner records it as provisioned), and new STND.PROJ.7 the closed kinds commit, post, publish, transmit, and other, marking publication, release, transmission, and every kind at a destination not recorded as provisioned as irrevocable (GUARD.11); both are defaults; the authorization file of the project template gains the field remote_writes. |
