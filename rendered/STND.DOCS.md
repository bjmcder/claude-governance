# Documentation standard (STND.DOCS) 1.0.2

Adopted by The Custodian as revision 1.0 in ledger entry 100 (2026-10-23); revised to 1.0.1 in entry 269 (2026-10-28) and 1.0.2 in entry 291 (2026-10-28). This reading copy is composed from the per-provision files in STND/DOCS/ of the governance harness; the harness files are the system of record.

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

STND.DOCS.10 is the agent rule of the standard. It binds by its own force (GOV.48); STND.INSTR.10 carries it into agent instructions drawn from STND.INSTR, and a project's own agent instructions carry it by citation. Every agent, at every class, writes all of its text in American spelling and usage, writes its work documentation without the content that STND.DOCS.3, STND.DOCS.4, and STND.DOCS.5 keep out and its human-facing writing without the patterns of STND.DOCS.9, and corrects or records each statement of the work documentation that it knows, or that a search for the names its change alters shows, to disagree with the work or with another statement. The danger it guards against is the one the custodian names in STND.DRAFT: silent misalignment, where the human owner and the reviewers verify agent-written text against the work (INTPR.1) and inflated or generic prose, notes about the agent, and known false statements defeat that check. Its cost is the agent's choice of words, the naming of sources, and a record, not additional documentation, so binding it at every class raises no floor (GOV.11), as STND.INSTR.8 does for an agent's notes. For other authors, and for agents in the other provisions, the content, language, and consistency provisions other than STND.DOCS.1 are defaults, and STND.DOCS.6 and STND.DOCS.7 are permissions.

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

## Provisions

### Content

#### STND.DOCS.1 Voice of documentation

Binding. Instantiates INTPR.1, INTPR.2.

Work documentation SHALL be written for a human reader who knows the domain of the work but not its code, as one person explaining the work to another (INTPR.1, INTPR.2).

#### STND.DOCS.2 Explanatory content

Default, from CSQ3. Instantiates INTPR.1.

Work documentation SHOULD define each term of art on its first use and give an example of each element whose use is not evident (INTPR.1).

#### STND.DOCS.3 Agents kept out of documentation

Default, from CSQ3. Instantiates INTPR.5.

Other than as STND.DOCS.6 and STND.DOCS.7 permit, work documentation SHOULD NOT name an agent that works on the work (INTPR.5). Other than as STND.DOCS.6 and STND.DOCS.7 permit, work documentation SHOULD NOT describe agent conduct (INTPR.5). Work documentation SHOULD address only its human readers (INTPR.5).

#### STND.DOCS.4 Edit narration kept out

Default, from CSQ3. Instantiates INTPR.5.

Other than in a changelog, a release note, a migration note, or a deprecation notice, work documentation SHOULD NOT narrate the edits that brought the work to its present state, which the version history holds (INTPR.5, REPRO.5).

#### STND.DOCS.5 Process records kept out

Default, from CSQ3. Instantiates INTPR.5.

Other than as STND.DOCS.6 permits, work documentation SHOULD NOT cite a process record (INTPR.5).

#### STND.DOCS.6 Governance as subject

Default, at every class. Instantiates INTPR.5.

Where the subject of the work is governance or the conduct of agents, its work documentation MAY name agents, describe agent conduct, and cite the process records that belong to that subject (INTPR.5).

#### STND.DOCS.7 Required statements of agent use

Default, at every class. Instantiates INTPR.5.

Where a law, a license, a contract, or a publisher's policy requires of the work a statement of the use of agents, its work documentation MAY carry that statement in the words and in the place that the requirement names (INTPR.5, PRIN.2). Where such a requirement names no place, the statement MAY stand in the document that it concerns (INTPR.5, PRIN.2).

### Language

#### STND.DOCS.8 American English

Default, from CSQ3. Instantiates INTPR.12, INTPR.1.

Other than in a quotation, a title, a proper name, a literal, a word mentioned as a word, or a name fixed outside the prose, human-facing writing SHOULD use American spelling, punctuation, and usage, of which the tables of this provision list a part (INTPR.12). Where a project instrument names a dictionary, human-facing writing SHOULD use, of two current American spellings, the first that the dictionary lists (INTPR.12). Other than a name that a dependency, a file format, an external interface, a persisted record, or a published interface of the work fixes, each name in the source of the work SHOULD use American spelling (INTPR.1).

| Not used | Used |
| --- | --- |
| learnt, dreamt, spelt (verb) | learned, dreamed, spelled |
| licence (noun), practise (verb), enquiry | license, practice, inquiry |
| mould, sceptic, storey, cheque, draught, manoeuvre, speciality | mold, skeptic, story, check, draft, maneuver, specialty |
| aluminium, sulphur, maths, per cent | aluminum, sulfur, math, percent |
| tyre, kerb, plough | tire, curb, plow |
| torch (a hand lamp), aerial (an antenna), spanner (a wrench) | flashlight, antenna, wrench |
| earth (electrical), mains (electrical), crocodile clip | ground, line power, alligator clip |
| full stop, round brackets | period, parentheses |
| different to, in future (meaning "from now on"), at the weekend, fortnight | different from, in the future, on the weekend, two weeks |
| the committee have, the government are | the committee has, the government is |
| 22 October 2026, in prose | October 22, 2026, or 2026-10-22 |
| a comma or period outside the closing quotation mark, in prose | the comma or period inside it |

| British | American |
| --- | --- |
| behaviour | behavior |
| colour | color |
| favour | favor |
| honour | honor |
| labour | labor |
| neighbour | neighbor |
| centre | center |
| metre | meter |
| litre | liter |
| fibre | fiber |
| analyse | analyze |
| organise | organize |
| recognise | recognize |
| minimise | minimize |
| maximise | maximize |
| optimise | optimize |
| utilise | utilize |
| standardise | standardize |
| authorise | authorize |
| initialise | initialize |
| serialise | serialize |
| normalise | normalize |
| catalogue | catalog |
| defence | defense |
| offence | offense |
| grey | gray |
| programme | program |
| artefact | artifact |
| judgement | judgment |
| ageing | aging |
| modelling | modeling |
| labelling | labeling |
| cancelled | canceled |
| travelling | traveling |
| fulfil | fulfill |
| enrol | enroll |
| whilst | while |
| amongst | among |

#### STND.DOCS.9 Specific statements

Default, from CSQ3. Instantiates INTPR.12.

Human-facing writing SHOULD state each point specifically and plainly, and name the source of each point that rests on one (INTPR.12). Other than in a term of art in its technical sense, a quotation, a label or warning that another provision requires, or a structure that governance prescribes, human-facing writing SHOULD NOT carry a pattern of the table of this provision (INTPR.12).

| Pattern | Forms to watch |
| --- | --- |
| Importance claimed for a detail | "stands as", "is a testament to", "a pivotal moment", "a crucial role", "a vital part", "underscores its importance", "reflects broader trends", "an enduring legacy", "sets the stage for", "marks a shift", "an evolving landscape", "deeply rooted"; a statement that a detail represents or contributes to something larger, with nothing shown |
| Claimed notability and coverage | "independent coverage", "featured in", "profiled in", "a leading expert", "widely used" or "trusted by" with no source; a list of outlets or adopters with nothing of what they say or do |
| Analysis by trailing participle | where it claims an importance or effect that it does not state, a closing "highlighting ...", "underscoring ...", "emphasizing ...", "ensuring ...", "reflecting ...", "contributing to ...", "fostering ...", "enhancing ..."; "valuable insights"; "aligns with", "resonates with" |
| Promotional language | "boasts", "vibrant", "rich", "profound", "showcasing", "exemplifies", "commitment to", "nestled", "in the heart of", "groundbreaking", "renowned", "a diverse array", "seamless", "powerful", "cutting-edge", "state-of-the-art", "robust" as praise |
| Vague connection | "in connection with", "associated with", "connected to", where the relation itself is known and unstated |
| Vague attribution | "experts argue", "observers have noted", "industry reports", "studies show", "several sources" where one is cited; "including" before a list that is complete |
| Formula of challenges and prospects | "despite its ..., it faces challenges", "despite these challenges", a closing section on challenges, legacy, or future outlook that says nothing particular to the work |
| Vocabulary of generated text | "additionally" opening a sentence, "align with", "bolstered", "crucial", "deep dive", "delve", "emphasizing", "enduring", "enhance", "fostering", "garner", "highlight" as a verb, "interplay", "intricate", "landscape" as an abstract noun, "meticulous", "pivotal", "showcase", "tapestry", "testament", "underscore" as a verb, "valuable", "leverage", "multifaceted", "prioritize", "quietly", "steady", "what matters", "practical" as vague approval, "utilize" where "use" serves |
| A copula avoided | "serves as", "stands as", "functions as", "represents", "marks", "boasts", "features", "offers", "maintains", where "is" or "has" is meant; "refers to" opening the definition of a thing rather than a word |
| Negative parallelism | "not just X, but Y", "not only X but also Y", "not X, but Y", "it's not X, it's Y", "no X, no Y, just Z", "Y rather than X", where no reader holds the view denied |
| Reflexive groups of three | three adjectives, nouns, or phrases where the content has another number of members |
| Synonym cycling | a function, quantity, or concept renamed from sentence to sentence for variety |
| Headings by formula | title case in headings; a heading that repeats the document's title; skipped heading levels; a heading over no text of its own where no structure prescribes it; "X and Y" headings by reflex |
| Decoration of plain text | bold scattered through prose; items each opening with a bold label and a colon where prose serves; emoji as markers; a small table that a sentence serves; a rule between every pair of sections; curly quotation marks or apostrophes in a medium whose convention is straight ones |
| Address to a requester | "Certainly!", "Of course!", "You're absolutely right!", "I hope this helps", "a more detailed breakdown"; advice or prewriting meant for the person who asked, left in a document |
| Disclaimers that fill gaps | "while specific details are limited", "not widely documented", "based on available information"; where no specific limit or confusion is named, "should be treated as ... rather than ...", "does not by itself establish", or "should not be confused with"; "it is important to note", "it is crucial to differentiate" |
| Placeholders left in | "[Your Name]", "[insert ...]", "2025-xx-xx", "PASTE_URL_HERE", "add if available", "TBD" |
| Markup of another medium | markup that the medium does not render; a fence around the whole text or around prose; broken markup |
| Residue of generating tools | "contentReference[oaicite:", "oai_citation", "turn0search0", "[cite: 1]", "(start_span)", "grok_card", "【85†L261-269】", "[attached_file:1]", "utm_source=", ":::writing" |
| References that do not check | links that never resolved, an invalid ISBN or DOI, a DOI that leads to another work, a book cited without a page for a specific claim |
| Change descriptions by formula | "improved clarity and flow", "enhanced", "streamlined", "refined", "ensured compliance with", "preserved", "retained", "avoided", "addressed reviewer feedback", "added sourced content", in a description of a change that names nothing it did |
| Service register | "I have carefully reviewed", apology for an inconvenience that "may have" occurred, "please point out ...", "I respectfully request", "I hope this message finds you well" |
| Stock summaries and refusals | "in summary", "in conclusion", "overall" opening a paragraph that repeats the text above it; "as of my last knowledge update"; "as an AI language model"; a refusal that offers an unrequested alternative |
| Punctuation by formula | em dashes, spaced or not, in place of commas, colons, or parentheses, more than occasionally |
| Text cut off | a sentence, list, or table that ends unfinished |

### Agents

#### STND.DOCS.10 Agent writing

Binding. Instantiates GOV.48, INTPR.12, INTPR.3.

An agent SHALL write each text it writes, and each name it gives in the source of the work, as STND.DOCS.8 recommends, or as the alternative that a project instrument adopts in its place requires (GOV.48, INTPR.12). An agent SHALL write its work documentation as STND.DOCS.3, STND.DOCS.4, and STND.DOCS.5 recommend and its human-facing writing as STND.DOCS.9 recommends, or as the alternatives that a project instrument adopts in their place require (GOV.48, INTPR.12). An agent SHALL correct, or record in defect tracking, each statement of the work documentation that it knows, or that a search for the names its change alters shows, to disagree with the work or with another statement of the work documentation (GOV.48, INTPR.3).

### Consistency

#### STND.DOCS.11 Documentation in step with the work

Default, from CSQ3. Instantiates INTPR.3, QA.4, QA.5.

A change that alters the behavior, an interface, a default, a unit, a limit, or an output of the work SHOULD change, in the same change, each statement of the work documentation in its version history that describes what it alters (INTPR.3). Where such a statement lies outside the version history of the work, the actor making the change SHOULD record the statement in defect tracking and report it as QA.5 asks (INTPR.3, QA.4, QA.5). Each statement of the work documentation SHOULD agree with the work at the revision it describes and with each other statement of the work documentation (INTPR.3).

#### STND.DOCS.12 One name per concept

Default, from CSQ3. Instantiates INTPR.1, INTPR.3, INTPR.4.

Each concept of the work SHOULD carry one name across its code and its work documentation (INTPR.1, INTPR.3). Each name SHOULD carry one meaning (INTPR.1, INTPR.3). A symbol of a notation declared once and mapped to a name in the code MAY stand beside that name as the same name (INTPR.4).

#### STND.DOCS.13 Checked examples

Default, from CSQ3. Instantiates INTPR.3, VV.8.

Each example in the work documentation that runs in the checking environment without hardware, network access, a secret, or a destructive action SHOULD be run among the checks of each change that affects it, with its shown result compared within a stated tolerance (INTPR.3, VV.8). Other than after a change to the work that an example describes, or after a reference independent of the failing run confirms another result, the shown result of a failing example SHOULD NOT be replaced by the output of the run that failed (VV.8).

#### STND.DOCS.14 Documentation in change review

Default, from CSQ3. Instantiates QA.7, INTPR.3.

The review of each change SHOULD examine the human-facing writing that the change adds or alters, and each statement of the work documentation that names an element the change alters, against STND.DOCS.1, STND.DOCS.2, STND.DOCS.3, STND.DOCS.4, STND.DOCS.5, STND.DOCS.8, STND.DOCS.9, STND.DOCS.11, and STND.DOCS.12 (QA.7, INTPR.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-23 | Adopted. |
| 1.0.1 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-28 | Editorial amendment (GOV.41): STND.DOCS.8 holds the spelling table that STND.DRAFT.33 held, beside its own table of usage, so that the corpus keeps one spelling table; its first sentence cites the tables of this provision alone, and the Notes say which table the drafting check reads; no obligation, permission, or defined meaning changes. |
