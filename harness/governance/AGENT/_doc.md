---
id: "AGENT"
level: "LVL1"
kind: "profile"
title: "Agent practice"
status: "adopted"
revision: "1.1"
adopted: "2026-10-11"
selector: "Binds every project (AGENT.1)."
parent: null
adopted_by: "The Custodian"
---

## Purpose and scope

This profile holds the practice that every agent acting on the covered work of a project follows, whatever the domain, hardware, or consequence class. It holds generally applicable behaviors only: how an agent explains and reports its work, estimates and delegates its effort, keeps working without needless interruption, stays within its scope, answers for its own work and its delegates' work when asked, works in parallel safely, keeps secrets undisclosed, and keeps the records, tools, and knowledge that let others audit and build on that work. Agent safeguards stay in the prime directives and GUARD; this profile adds no tier, authorization, or reserved action. It names no language, library, tool, technology, platform, process, or method (GOV.18). Each provision cites the LVL0 provisions it instantiates and only tightens them (PRIME.15).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Access descriptor | A classification of a network access, such as retrieval, search, or refused retrieval, in the vocabulary that the defaults or a project instrument defines or, absent one, in words that state what was attempted and its outcome. |
| Ambiguous instruction | An instruction of the human owner or of a directing agent that admits more than one reading. |
| Assumed claim | A claim that is neither a checked claim nor an inferred claim. |
| Authentication credential | A secret that proves an identity or grants access, such as a password, a key, a token, or a certificate with its private key. |
| Checked claim | A claim supported by evidence (VV.1) that the agent obtained or confirmed and that the work report presenting the claim cites. |
| Directed agent | An agent that another agent directs (GUARD.12). |
| Directing agent | An agent that directs another agent (GUARD.12). |
| Effort estimate | A statement, made before a unit of work begins, of the operating cost the unit is expected to incur and of the number of agents and the configuration of each that it needs, each with its basis and with what the estimate is unable to measure. |
| Inferred claim | A claim, other than a checked claim, that an agent reaches by stated reasoning from checked claims or from other inferred claims. |
| Investigation | A search of sources, an experiment, or an analysis that an agent carries out to answer a question that its unit of work raises, and whose answer bears on a decision, a result, or a finding of that unit. |
| Lesson | A trend seen across units of work, or an insight into how work is done, that bears on the performance or results of work beyond the project that revealed it. |
| Lesson entry | A knowledge entry (GOV.32) that states a lesson. |
| Open alternative | A version of an item, offered by the same or another source without the limit that blocked the item, such as a preprint of a paper whose publisher's version is behind a paywall. |
| Parallel work | Units of work that two or more agents directed under the same human owner carry out at the same time on the same work or on the same machine. |
| Recurring task | A task whose steps the record shows an agent has performed at least twice before in the same project, differing at most in their inputs. |
| Research effort | The retrieval that an agent and every agent it directs make to answer one research question of a unit of work, across every investigation carried out for that question. |
| Research note | A record of an investigation, stating the question, the sources consulted, each identified without a secret, other than a source by which a secret was reached incidentally (PRIME.10), with citations of their network access records, the experiments run and analyses performed, what was found, and what was left open. |
| Reusable finding | A method or practice, tool, research result, negative result, explained anomaly (INTPR.7), or other finding of an agent's work whose domain of validity extends beyond the project that produced it. |
| Routine action | An action of the free tier of GUARD.1 whose tier the record settles (GUARD.2), whose safety is not uncertain (PRIN.8), and for which no condition of PRIME.14 is met. |
| Secret | Information whose disclosure would present a security or privacy risk to a person or an organization, including passwords, keys of application programming interfaces, tokens, private keys, and information about a system, such as a non-public host name, address, account, network layout, open service, or configuration, that would ease the introduction or exploitation of a vulnerability. An identity of hardware or software recorded under REPRO.1, REPRO.2, or REPRO.9, such as a processor, an accelerator, a memory size, or a software revision, is not a secret where the record is read only by those whom the threat model trusts with it, and elsewhere is a secret only where its disclosure would ease the introduction or exploitation of a vulnerability. |
| Session | One continuous run of an agent and the instructions it received in that run. |
| Work report | An account that an agent gives the human owner or a directing agent of its own work or of the work of the agents it directs or has directed. |
| Workbench | The record that a project designates for its research notes, for findings that bear on later work in the project and are not proposed as knowledge entries, for tools used repeatedly within the project, and for proposed knowledge entries that await a knowledge base; absent a designation, those entries kept with the project's other records under AGENT.35. |

## Selector

AGENT.1 states the selector, which is true for every classification and for a project without one. Every other provision binds an agent, so the profile asks nothing of work on which no agent acts.

## Where the rest lives

| Subject | Provisions |
| --- | --- |
| Acts reserved to the human owner, and self-adoption | PRIME.1, GOV.48 to GOV.50 |
| Action tiers, reserved actions, authorizations, network access | PRIME.6 to PRIME.9, GUARD.1 to GUARD.13 |
| Delegated authority and circumvention | PRIME.7, PRIME.12, GUARD.12 |
| Halting and the findings and justification statement | PRIME.14, GUARD.3, QA.3, the project's agent instructions |
| Operating cost and spending limits | PRIME.8, GUARD.14, GUARD.15 |
| Instruction authority and injected instructions | PRIME.11, GUARD.16 |
| Secrets and the threat model | PRIME.10, GUARD.16, GUARD.17 |
| Physical hardware | PRIME.13 |
| Records of agent steps and agent-authored changes | REPRO.5, REPRO.11 |
| Knowledge base, evidence levels, and reliance ceilings | GOV.32 to GOV.34 |
| Incidents and their root causes | QA.15 |
| Retention and format of records | REPRO.12 and the project's retention mechanism |
| Working notes, and knowledge held only in agent memory | INTPR.5, INTPR.13 |
| Review independence for agent authors | QA.8, STND.CLASS.18 |

## Notes

The profile derives from three clauses of the unratified revision 0.11 that the pre-1.0 notes assigned to it: V.12 (agent explanations) became AGENT.2; VI.15 (effort estimation) became AGENT.6 to AGENT.10; VI.16 (mechanized recurring work) became AGENT.13. The obligation of VI.16 to make "a good-faith effort" is now a recommendation with a stated trigger: the plan of the unit states further performances of a recurring task, and the estimated cost of mechanizing them is less than that of repeating them (RSRC.6). AGENT.11 and AGENT.12 complete delegation with the brief a directed agent receives and the check its work receives.

AGENT.14 to AGENT.17 serve agents that work for long periods without the human owner present: routine actions proceed without approval, a halt stops only its own line of work, an ambiguous instruction is acted on as far as every one of its readings permits rather than left waiting, and each session resumes from the record and the workspace. A human owner who wants close involvement names the actions to approve in the instructions, and AGENT.14 then yields. None of these provisions widens what an agent is able to do: a routine action excludes every action whose tier the record does not settle, whose safety is uncertain, or that meets a condition of PRIME.14.

AGENT.3 to AGENT.5 make PRIME.2 specific to failure modes common in agents: an inference reported as a finding, a check result carried over from an earlier revision, and a test or criterion adjusted in the same change it judges.

An effort estimate under AGENT.6 is not an authorized estimate under PRIME.8 unless the human owner authorizes it. AGENT.8 reports an overrun without halting; GUARD.15 still halts work before an authorized limit is exceeded.

AGENT.20 and AGENT.21 make agent work observable on demand. The human owner asks the agent it directed; that agent answers for itself and for each agent it directs or has directed, from their answers or, for an agent that has ended, from the record AGENT.21 keeps, so an answer reaches down the whole chain of delegation. In an answer, what a directed agent states and the directing agent has not checked is an assumed claim (AGENT.3).

AGENT.22 to AGENT.25 keep the record of agent work that REPRO.11 calls for: the decisions that alter a plan, each network access other than one that reached a secret, the timing and cost of each unit, each written as the event occurs, so that an agent ended without warning leaves an auditable record. These are records (REPRO), not working notes (INTPR.5). A network access record contains no secret, and an access by which a secret was reached incidentally is reported under PRIME.10 instead of recorded, in a network access record or a research note.

AGENT.26 to AGENT.30 and AGENT.38 carry what an agent learns past its project, through the knowledge base (GOV.32): lessons that improve performance and results over time, such as broad trends and insights into how work is done, but not routine detail confined to one unit or one project; reusable findings, such as methods and practices, tools, research results, negative results, and explained anomalies; consultation before planning; a proposed provision once a defect of a kind a lesson states recurs; and proposals of knowledge entries drawn from the workbench. An item that is both a lesson and a reusable finding is proposed once, under AGENT.27, with the evidence it asks for. A knowledge entry for a tool describes the tool and states where it is kept. An agent drafts entries and provisions; establishing and adopting them belong to others (GOV.34, GOV.49). AGENT.30 keeps a proposed entry in the workbench where no knowledge base is designated, and AGENT.28 consults the workbench with the knowledge base.

AGENT.31 to AGENT.37 keep the workbench, the project's laboratory notebook, whose tools are kept under version control and repaired in place, and keep it distinct from three other places an agent writes:

| Place | Holds | Kind | Reach | Lifetime |
| --- | --- | --- | --- | --- |
| Working-notes workspace (INTPR.5) | Plans, notes for later recovery, the session account, out-of-scope notes (AGENT.19) | Not a record; no instruction authority | One project | As long as the work needs it; not the only copy of what a reader of the code needs |
| Workbench | Research notes, project findings, tools used repeatedly within the project, proposed knowledge entries awaiting a knowledge base | A local project record: dated, attributed, corrected only by later entries except its tools, which are versioned and repaired in place | One project | Retained with the project's records (REPRO.12) |
| Knowledge base (GOV.32) | Knowledge entries, including entries for tools, useful beyond the project | A knowledge base shared across projects, managed apart from any one project | Every project | Superseded or retracted, not altered in place (GOV.34) |
| Temporary items (GUARD.7) | Intermediates of a run, such as files kept in a temporary directory | Neither a record nor working notes | One run | Removable; holds nothing a later session needs (AGENT.37) |

A workbench entry informs later work as evidence; knowledge drawn from it is relied on as knowledge only through a knowledge entry (GOV.32, GOV.33). The records of AGENT.22 to AGENT.25 stay with the project's other records, and a research note cites them rather than repeating them. A change proposed outside scope stays a working note (AGENT.19); the research note that found it records the evidence. The workbench's location is a project choice or, absent a designation, AGENT.35 places it with the project's other records. The custodians adopted an interpretation of GOV.32 on 2026-10-11: "For GOV.32, a project's workbench is a record of that project's work and not a knowledge base; the knowledge base to which the AGENT profile proposes entries is one shared across projects and managed apart from any one of them; the working-notes workspace and temporary items are neither. A tool is not itself a knowledge entry; an entry concerning a tool is a claim about it, as the Lexicon defines a knowledge entry." A tool that AGENT.13 builds for the unit's own steps is a workbench tool; a workbench tool is code, and QA.7 and REPRO.10 apply to it.

AGENT.9 leaves scale to the project. This profile sets no limit on the number of agents directed, on the depth of delegation, or on network access made for an investigation beyond what LVL0 requires and what the host, the transport, or the remote server enforces; a further limit is a project instrument's to set, and GOV.18, as amended in LVL0 revision 1.6, reserves such limits to LVL3. LVL0 requires a recorded authorization for network access that names its purpose, scope, and the items or volume it permits (PRIME.7, GUARD.13), and reserves bulk retrieval (GUARD.8); a standing authorization for read-only research retrieval, which a human owner grants as a project instrument with bounds on items and volume per research effort, meets this without a request for each access (GUARD.11). A bound is the human owner's to raise to a new stated value, since retrieval that no authorization bounds is reserved (GUARD.8, PRIME.6); AGENT.46 has the agent ask for that when a research effort reaches it, in the form of the findings and justification statement the agent instructions define (STND.DFLT.20), and only retrieval beyond the bound waits on the answer, while the agent continues each other line of work that does not depend on that retrieval (AGENT.15). A research effort counts the retrieval of every agent that works on its question, and dividing a question to reset a bound is circumvention (PRIME.12) unless the human owner approves the division, which then makes each part its own research effort. AGENT.41 states the gap and leaves retrieval by hand to the human owner; the authorization's scope and PRIME.7 keep an agent from working around the limit. Working around a limit means a direct attempt to defeat or evade it; searching for and retrieving an open alternative, such as the preprint of a paywalled paper, is ordinary research within the authorization's scope. For a retrieval that a paywall or cap blocks, AGENT.41 governs and only the retrieval of that item stops; AGENT.45 applies only where the agent seeks to use a credential the environment does not let it use. AGENT.23 records each attempt, refused ones included; the vocabulary of access descriptors belongs to the defaults standard or a project instrument. AGENT.39 and AGENT.40 make parallel work safe and efficient: an assessment before it begins, and units started on a shared machine as soon as, and only while, it is able to serve them.

The term Secret captures the spirit of PRIME.10 rather than a closed list: it protects information whose disclosure would present a security or privacy risk to a person or an organization, above all information that would ease the introduction or exploitation of a vulnerability. The identity of a machine's processor, accelerators, memory, and software is usually reproducibility and compatibility information, recorded as REPRO.2 requires; where a record holding it is read beyond those the threat model trusts, the threat model states how it is recorded, for example by a reference that is not a secret, and settles borderline cases (GUARD.16). The custodians' interpretation of PRIME.10, adopted 2026-10-11, carries the same reading. AGENT.43 bars committing a secret and disclosing it, directly or by an inferable route, to anyone its authorization does not name; AGENT.44 keeps the non-credential secrets an agent needs in a protected store outside version control, the records, and the working-notes workspace, in practice an untracked file or its equivalent, and handling them still needs an authorization (PRIME.10). AGENT.45 forbids an agent to write an authentication credential anywhere that outlasts the action using it; an agent reads one only as an authorization allows (PRIME.10); delegating access is the human owner's responsibility, for example by provisioning the environment so that the agent uses an access through a means that holds the credential for it. AGENT.42 resolves doubt toward secrecy.

A provision inherits the rank and waivability of the provisions it instantiates (GOV.5, GOV.17): those instantiating a prime directive, GUARD, GOV, or a Governing Principle are non-waivable and bind at every class; those instantiating only VV, REPRO, INTPR, DSGN, SIMPL, RSRC, or QA are proportioned to class (GOV.11). AGENT.5, AGENT.11, AGENT.12, AGENT.14, AGENT.17, AGENT.39, and AGENT.47 instantiate both and bind at every class, a reading resting on GOV.9 and GOV.17 and recorded as a judgment (PRIN.10) until the custodians interpret GOV.11 for such provisions. AGENT.14 adds a prohibition at every class, which lowers exploratory overhead rather than raising it (GOV.11), so that routine work proceeds without approval requests even at CSQ4; each other provision ranked PRIME or GUARD, or unranked, states how a floor obligation of LVL0 is met or, as AGENT.9 and AGENT.38 do, grants a permission within one, and AGENT.17 asks no more at the floor than reading what the agent was told and is authorized to do. Every waivable provision (AGENT.2, AGENT.13, AGENT.18 to AGENT.28, AGENT.30 to AGENT.33, AGENT.35 to AGENT.37, AGENT.40, AGENT.41) is proportioned to class under the project's class criteria, such as STND.CLASS.10, and applies from the least severe class at which the project's criteria require an LVL0 obligation it instantiates. A Governing Principle is cited only where a provision implements that principle's own text (PRIN.4, PRIN.5, PRIN.6, PRIN.8); AGENT.20 rests on INTPR.6 and REPRO.11, not on PRIN.1, so that it is proportioned. The rank and waivability under each title are derived; the harness verifies them.

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-11 | Adopted. |
| 1.1 | 2026-10-11 | Minor amendment (GOV.41): AGENT.15 requires, in place of recommending, that an agent continue each line of work that neither depends on a halted line nor shares the cause of its halt, so that unattended work proceeds past a referral (STND.DRAFT.42); new AGENT.47 has each work report state first every departure from the definition of done, the acceptance criteria, or an instruction, every check skipped, disabled, or weakened, and every ambiguous instruction acted on, including those its directed agents report. |
