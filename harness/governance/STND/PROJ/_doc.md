---
id: "STND.PROJ"
level: "LVL2"
kind: "standard"
title: "Project constitution template"
status: "adopted"
revision: "1.1"
adopted: "2026-10-20"
adopted_by: "The Custodian"
instantiates: ["GOV.20", "GOV.21"]
rank: null
waivable: false
---

## Purpose and scope

This standard fixes what a project constitution holds (GOV.20, GOV.21): one section for each mechanism that LVL0 requires of every project, the classification and its judgments, the places where the work's notes, workbench, knowledge, and secrets are kept, the authorizations in force, and, for work that drives physical hardware, its safety instruments. A filled copy is a LVL3 instrument that the project's human owner adopts (GOV.41). A section states its content in full or adopts by citation the provisions of an adopted LVL2 standard (STND.PROJ.2), so that a project takes the defaults, the agent instructions, the dependency policy, and the threat-model template without restating them, and a section whose content the project's class does not yet ask for says so (STND.PROJ.1). STND.PROJ.3 recommends the standing authorizations that let routine work run unattended, and the roles to which each extends, and STND.PROJ.5 a discipline for the operating cost of agents, each proposed once at the project's start (STND.DRAFT.42). STND.PROJ.1 to STND.PROJ.3 and STND.PROJ.5 are binding, because each instantiates GOV or GUARD, which the floor holds (GOV.10); STND.PROJ.3 and STND.PROJ.5 are recommendations within a binding provision. STND.PROJ.4, on the form of the files, is a default (GOV.19). The standard names no tool or method (GOV.18).

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

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.1 | 2026-10-21 | Minor amendment (GOV.41), conforming on the adoption of STND.CREW: the section Authorizations states the agents or roles to which each authorization extends and the capability levels that the cost discipline marks for ruling (STND.PROJ.1); each proposed standing authorization states the roles to which it extends, read-only research retrieval to research agents alone (STND.PROJ.3); new STND.PROJ.5 proposes a discipline for the operating cost of agents that states the capability levels whose assignment needs the human owner's ruling and keeps AGENT.6 in force for every unit and AGENT.10 for every assignment to an unmarked level. Constitutions adopted before this revision keep their authorizations and discipline as their text says (GUARD.12, GUARD.14), and state the new content of the section Authorizations at their next amendment. |
