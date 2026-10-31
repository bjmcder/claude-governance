---
id: "STND.DOCS"
level: "LVL2"
kind: "standard"
title: "Documentation standard"
status: "adopted"
revision: "1.0.3"
adopted: "2026-10-23"
adopted_by: "The Custodian"
instantiates: ["GOV.19", "GOV.48"]
rank: null
waivable: false
---

## Purpose and scope

This standard governs two things. The first is the work documentation: the comments, docstrings, and documents of the work, and the messages it presents to people. Work documentation is written by one person for another. It explains the work, and it leaves the agents that helped write it and the governance under which they worked to the records, except where STND.DOCS.6 and STND.DOCS.7 admit them (STND.DOCS.1 to STND.DOCS.7). The second is the language of all human-facing writing, reports and records included: American English, and plain, specific statements free of the habits of generated text (STND.DOCS.8 and STND.DOCS.9). Work documentation agrees with the work and with itself (STND.DOCS.11 to STND.DOCS.14). STND.DOCS.1 instantiates the floor obligation of INTPR.2 and STND.DOCS.10 instantiates GOV.48, and both are binding at every class. STND.DOCS.10 holds every agent, at every class, to STND.DOCS.3, STND.DOCS.4, STND.DOCS.5, STND.DOCS.8, and STND.DOCS.9, and to correcting or recording each disagreement of the work documentation that it knows of. Every other provision is a default (GOV.19). Conventions for docstrings and comments in a particular language belong to the standard for that language. The standard names no tool or format (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Agent, Author, Record, and Human-facing documentation have the meanings the Lexicon gives them; Session, Work report, and Workbench have the meanings that AGENT gives them.

| Term | Definition |
| --- | --- |
| Work documentation | The human-facing documentation of the work: each comment and docstring in its source, each document written for the people who use, maintain, or read the work, and each message that the work itself presents to a person. The working-notes workspace, the workbench, the records, work reports, knowledge entries, governance text and project instruments, instructions and briefs addressed to agents, and outputs with their provenance are not work documentation. |
| Human-facing writing | Work documentation, and each other text that an actor writes for a person to read: a work report, a referral, a record, a commit message, and the text of governance. |
| Agent conduct | The instructions, sessions, and actions of an agent that works on the work. |
| Process record | A record of how the work is governed, built, reviewed, or released rather than of what the work is or does: a provision, a ledger entry, a waiver, a ruling, an authorization, a register, a unit record, a referral, a work report, a release record, an incident record, and a record of review or audit. Requirements, specifications, the hazard analysis, the safe ranges of actuation, defect tracking, dependency records, and decision records under REPRO.7 describe the work and are not process records. |

## Notes

The custodian's direction of 2026-10-22 asks that documentation read as one person talking to another: no notes an agent leaves for itself, no references to governance or ledgers, and no account of what an agent did. STND.DOCS.1 states the reader and the voice. STND.DOCS.2 adds what makes documentation teach: terms defined on first use and examples where the use is not evident. The reasons for the design, its assumptions, and its limits are asked by INTPR.2 and INTPR.10 themselves, from the onsets those provisions set, and this standard does not restate them.

Three provisions keep out the content that does not belong. STND.DOCS.3 removes agents and their conduct, and it has work documentation address only its human readers, which excludes a note to its author, to a later session, or to an agent reading the text; STND.INSTR.8 already keeps an agent's plans, notes, and session account out of documentation, and STND.DOCS.3 adds the naming of agents and their instructions and extends the rule to every author. STND.DOCS.4 removes narration of edits, which the version history holds (REPRO.5): "Changed to a stable sort" is history, and "A stable sort keeps equal keys in input order, which the merge step relies on" is documentation. A changelog, release note, migration note, or deprecation notice is written for those moving between revisions (DSGN.6, QA.13), and a statement of the alternatives weighed and the reason for the choice, which REPRO.7 lets a comment hold, is documentation: "Backward Euler is used because the explicit method is unstable above step h." STND.DOCS.5 removes citations of process records. A known defect or limit is stated as a fact about the work, with its identifier in defect tracking where it has one (QA.4), and a suppressed warning or a deviation is explained by its technical reason, not by the waiver or ruling behind it. The explanation that AGENT.2 asks of an agent belongs in its work report or commit message, which are human-facing writing and not work documentation.

The Process record term draws the line by subject. A record of what the work is or does stays citable: a constant's source under STND.CODE.10, a command limit traced to its safe range (PRIME.13), a requirement, a hazard, or a defect. A record of how the work is governed, built, reviewed, or released does not appear in its documentation. A statement of the consequence class and its limits, which INTPR.10 and PRIME.3 call for, is a fact about the work and not a citation. STND.DOCS.6 admits governance and agents where they are the subject of the work, as in a governance harness. STND.DOCS.7 admits a statement that agents were used where a law, a license, a contract, or a publisher's policy requires one; the requirement carries the duty on its own terms, and the statement says what the requirement asks. Attribution of each change stays in the version history in every case (REPRO.5, STND.WPROC.2).

The language provisions apply to all human-facing writing, the custodian's words being "everywhere and at all times": documentation, reports to the human owner, commit messages, records, and governance text, whose provisions STND.DRAFT.33 already covers, with the spelling table of STND.DOCS.8, which the drafting check of American spelling reads. The two tables of STND.DOCS.8 list common differences between British and American English and are not exhaustive; the rule is American spelling, punctuation, and usage in full. Where two American spellings are current, the dictionary that a project instrument names decides; where none is named, either current spelling conforms. Names in the source follow the same spelling, so that names agree across the custodian's projects, except a name that a dependency, a file format, an external interface, a persisted record, or a published interface of the work fixes; renaming such a name would break what depends on it.

STND.DOCS.9 rests on the field guide "Signs of AI writing" that Wikipedia editors keep, in the copy that the custodian supplied on 2026-10-22, and restates its signs in this standard's own words. The guide is descriptive: its signs are symptoms of writing that has drifted from specific facts toward generic, inflated statements, and it warns against treating the signs alone as the problem. The provision therefore states the underlying rule first, a specific, plain statement of each point with its source, and lists the patterns second. Each row names a habit; the words listed are typical of it, and a word in its technical sense is correct: an energy landscape, robust statistics, statistical leverage, a leading underscore, a cryptographic key, a statistically powerful test, a fuel-rich mixture. A list of three that has three members, an occasional em dash, a code block, a required label or warning, the marks of AGENT.3 and the label of PRIME.3, an agent's reply that asks the human owner a question, and a structure that governance prescribes are also correct. The guide's own caution holds: no single pattern shows that text was generated, people use every one of them, and neither people nor detectors reliably tell the two apart, so the table is a tool for editing and says nothing about who wrote a text. The guide also names what reads as written by a person: plain "is" and "has," plain words such as "used" for "utilized" and "wrote" for "authored," definite statements, and the ordinary qualifiers of speech. A fabricated reference breaches PRIME.2, and a citation not confirmed breaches VV.2.

STND.DOCS.10 is the agent rule of the standard. It binds by its own force (GOV.48), for the reason of uniformity across projects that its field `binding_reason` records (GOV.19); STND.INSTR.10 carries it into agent instructions drawn from STND.INSTR, and a project's own agent instructions carry it by citation. Every agent, at every class, writes all of its text in American spelling and usage, writes its work documentation without the content that STND.DOCS.3, STND.DOCS.4, and STND.DOCS.5 keep out and its human-facing writing without the patterns of STND.DOCS.9, and corrects or records each statement of the work documentation that it knows, or that a search for the names its change alters shows, to disagree with the work or with another statement. The danger it guards against is the one the custodian names in STND.DRAFT: silent misalignment, where the human owner and the reviewers verify agent-written text against the work (INTPR.1) and inflated or generic prose, notes about the agent, and known false statements defeat that check. Its cost is the agent's choice of words, the naming of sources, and a record, not additional documentation, so binding it at every class raises no floor (GOV.11), as STND.INSTR.8 does for an agent's notes. For other authors, and for agents in the other provisions, the content, language, and consistency provisions other than STND.DOCS.1 are defaults, and STND.DOCS.6 and STND.DOCS.7 are permissions.

The direction asks for its rules everywhere and at all times, and this standard departs from that wording in four places, each for a reason. First, for authors other than agents, every provision other than STND.DOCS.1 is a default from CSQ3: binding them at CSQ4 would raise the floor that GOV.11 fixes, while an agent is bound at every class by STND.DOCS.10, whose cost is wording alone. Second, STND.DOCS.4 admits changelogs, release notes, migration notes, and deprecation notices, whose readers move between revisions and need the account of what changed (DSGN.6, QA.13). Third, STND.DOCS.6 admits governance and agents where they are the subject of the work, which its documentation cannot describe without them, and STND.DOCS.7 admits a statement of agent use that a law, a license, a contract, or a publisher's policy requires, because the requirement governs that statement. Fourth, a statement of the consequence class and its limits stays, because INTPR.10 and PRIME.3 call for it and it describes the work rather than its governance; and STND.DOCS.8 exempts quotations, titles, proper names, literals, words mentioned as words, and names fixed outside the prose, because changing them would misquote a source or break what depends on the name.

Documentation and the work change together (STND.DOCS.11). For work under STND.WPROC, a change is the change that a unit branch carries to its parent, so documentation edits are made on the unit branch and conflicts between them are resolved when the branch is updated from its parent (STND.WPROC.8). A statement outside the version history is recorded in defect tracking and reported as QA.5 asks when the change makes it false,. A statement agrees with the work at the revision it describes, so that a migration note describing an earlier revision is not in conflict. The direction's "globally consistent" means consistent across the whole of the work documentation. STND.DOCS.12 keeps one name for each concept; a mathematical symbol declared once and mapped to a name in the code is one name (INTPR.4, NUMER.4). STND.DOCS.13 runs the examples the documentation shows, within the checking environment and a stated tolerance, so that they fail when the work changes under them; a failing example is repaired with the work or corrected where it was wrong, and its shown result is not replaced by the output of the run that failed. These runs check the documentation and are not evidence for a claim of correctness. STND.DOCS.14 has the reviewer of each change look for the statements the change makes false, which a search for the names it alters finds.

Under STND.CLASS.10, each default applies from the class that its field `onset` gives, which work of CSQ4 may omit, and STND.DOCS.6 and STND.DOCS.7 are permissions, which STND.CLASS.10 does not stage and which carry the value null. STND.DOCS.8 and STND.DOCS.9 cite INTPR.12, as STND.DRAFT.33 does for spelling, because a successor reads the work most readily in one variety of English and plain prose. STND.DOCS.1 fixes how the floor documentation of INTPR.2 is written and asks for no documentation that the floor does not already require. Text that a change adds or alters conforms; text in an append-only record, a superseded decision record, or a past commit message stays as written (PRIME.5, GOV.36), and the transition is recorded in the ledger entry of adoption.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.DRAFT | Drafting standard |
| STND.INSTR | Agent instructions |
| STND.WPROC | Work process standard |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-23 | Adopted. |
| 1.0.1 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-28 | Editorial amendment (GOV.41): STND.DOCS.8 holds the spelling table that STND.DRAFT.33 held, beside its own table of usage, so that the corpus keeps one spelling table; its first sentence cites the tables of this provision alone, and the Notes say which table the drafting check reads; no obligation, permission, or defined meaning changes. |
| 1.0.3 | 2026-10-31 | Editorial amendment (GOV.41): STND.DOCS.10 records in its field binding_reason why uniformity across projects requires it to bind (GOV.19), for the custodians to adopt with this revision, and the Notes cite the field; no obligation, permission, or defined meaning changes. |
