"""STND.DOCS draft 0.2: after the cold review and the STND.HARN.28 pair review of 0.1, with the
custodian's copy of the Wikipedia field guide (2026-10-22)."""
from content3 import P, NORMATIVE, TERMS_LEAD

DATE = "2026-10-22"

USAGE_TABLE = """| Not used | Used |
| --- | --- |
| learnt, spelt, dreamt | learned, spelled, dreamed |
| licence (noun), practise (verb), enquiry | license, practice, inquiry |
| analogue, mould, sceptic, storey, cheque, draught, manoeuvre, speciality | analog, mold, skeptic, story, check, draft, maneuver, specialty |
| aluminium, sulphur, maths, per cent | aluminum, sulfur, math, percent |
| tyre, kerb, plough, spanner, torch, aerial | tire, curb, plow, wrench, flashlight, antenna |
| earth (electrical), mains, crocodile clip | ground, line power, alligator clip |
| full stop, round brackets, square brackets, curly brackets | period, parentheses, brackets, braces |
| different to, in future (meaning "from now on"), at the weekend | different from, in the future, on the weekend |
| fortnight, Monday to Friday | two weeks, Monday through Friday |
| the team are, the committee have | the team is, the committee has |
| 22 October 2026, in prose | October 22, 2026, or 2026-10-22 |
| a comma or period outside the closing quotation mark, in prose | the comma or period inside it, a quoted literal keeping its exact characters |"""

PATTERN_TABLE = """| Pattern | Forms to watch |
| --- | --- |
| Importance claimed for a detail | "stands as", "is a testament to", "a pivotal moment", "a crucial role", "a vital part", "underscores its importance", "reflects broader trends", "an enduring legacy", "sets the stage for", "marks a shift", "an evolving landscape", "deeply rooted"; a statement that a detail represents or contributes to something larger, with nothing shown |
| Notability by citation count | "independent coverage", "featured in", "profiled in", "a leading expert", "widely used", "trusted by"; a list of outlets, users, or adopters with nothing of what they say or do |
| Analysis by trailing participle | a closing "highlighting ...", "underscoring ...", "emphasizing ...", "ensuring ...", "reflecting ...", "contributing to ...", "fostering ...", "enhancing ..."; "valuable insights"; "aligns with", "resonates with" |
| Promotional language | "boasts", "vibrant", "rich", "profound", "showcasing", "exemplifies", "commitment to", "nestled", "in the heart of", "groundbreaking", "renowned", "a diverse array", "seamless", "powerful", "cutting-edge", "state-of-the-art" |
| Vague connection | "in connection with", "associated with", "connected to", where the relation itself is known and unstated |
| Vague attribution | "experts argue", "observers have noted", "industry reports", "studies show", "several sources" where one is cited, a marker of an incomplete list before a list that is complete |
| Formula of challenges and prospects | "despite its ..., it faces challenges", "despite these challenges", a closing section on challenges, legacy, or future outlook that says nothing particular to the work |
| Vocabulary of generated text | "additionally" opening a sentence, "align with", "bolstered", "crucial", "deep dive", "delve", "emphasizing", "enduring", "enhance", "fostering", "garner", "highlight" as a verb, "interplay", "intricate", "landscape" as an abstract noun, "meticulous", "pivotal", "showcase", "tapestry", "testament", "underscore" as a verb, "valuable", "leverage", "multifaceted", "prioritize", "utilize" where "use" serves |
| A copula avoided | "serves as", "stands as", "functions as", "represents", "marks", "boasts", "features", "offers", "maintains", where "is" or "has" is meant; "refers to" opening the definition of a thing rather than a word |
| Negative parallelism | "not just X, but Y", "not only X but also Y", "it's not X, it's Y", "no X, no Y, just Z", "Y rather than X", where no reader holds the view denied |
| Reflexive groups of three | three adjectives, nouns, or phrases where the content has another number of members |
| One thing under several names | a function, quantity, or concept renamed from sentence to sentence for variety |
| Headings by formula | title case in headings; a heading that repeats the document's title; skipped heading levels; a heading over no text of its own; "X and Y" headings by reflex |
| Decoration of plain text | bold scattered through prose; a list of items each opening with a bold label and a colon, where prose serves; emoji as markers; a small table that a sentence serves; a rule between every pair of sections; curly and straight quotation marks mixed |
| Address to a requester | "Certainly!", "Of course!", "You're absolutely right!", "I hope this helps", "Would you like ...", "Let me know if ...", "Here is a ...", "a more detailed breakdown"; advice or prewriting meant for the person who asked, left in the text |
| Disclaimers that fill gaps | "while specific details are limited", "not widely documented", "based on available information", "should be treated as ... rather than ...", "does not by itself establish", "should not be confused with", "it is important to note", "it is crucial to differentiate" |
| Placeholders left in | "[Your Name]", "[insert ...]", "2025-xx-xx", "PASTE_URL_HERE", "add if available", "TBD" |
| Markup of another medium | markup that the medium does not render; fenced blocks around content; broken markup |
| Residue of generating tools | "contentReference[oaicite:", "oai_citation", "turn0search0", "[cite: 1]", "(start_span)", "grok_card", "【85†L261-269】", "[attached_file:1]", "utm_source=", ":::writing" |
| References that do not check | links that never resolved, an invalid ISBN or DOI, a DOI that leads to another work, a book cited without a page for a specific claim |
| Change descriptions by formula | "improved clarity and flow", "enhanced", "streamlined", "refined", "ensured compliance with", "preserved", "retained", "avoided", "addressed reviewer feedback", "added sourced content"; a list of what was not changed |
| Service register | "I have carefully reviewed", apology for an inconvenience that "may have" occurred, "please point out ...", "I respectfully request", "I hope this message finds you well" |
| Stock summaries and refusals | "in summary", "in conclusion", "overall" opening a paragraph that repeats the text above it; "as of my last knowledge update"; "as an AI language model" |
| Punctuation by formula | spaced em dashes in place of commas, colons, or parentheses; prose in uniform short sentences joined only by commas and periods |"""

PURPOSE = """This standard governs two things. The first is the work documentation: the comments, docstrings, and documents of the work and the messages it presents to people. Work documentation is written by one person for another. It explains the work and says nothing about the agents that helped write it or the governance under which they worked, which the records hold (STND.DOCS.1, STND.DOCS.2, STND.DOCS.3, and STND.DOCS.4). The second is the language of all human-facing writing, reports and records included: American spelling and usage, and plain, specific statements free of the habits of generated text (STND.DOCS.5 and STND.DOCS.6). Work documentation agrees with the work and with itself (STND.DOCS.8). STND.DOCS.1, STND.DOCS.3, STND.DOCS.4, and STND.DOCS.7 instantiate the floor obligation of INTPR.2 or GOV.48 and are binding at every class; STND.DOCS.7 holds every agent to the language and consistency provisions at every class. Every other provision is a default (GOV.19). Conventions for docstrings and comments in a particular language belong to the standard for that language. The standard names no tool or format (GOV.18)."""

TERMS = TERMS_LEAD + """ Agent, Record, and Human-facing documentation have the meanings the Lexicon gives them; Session has the meaning that AGENT gives it.

| Term | Definition |
| --- | --- |
| Work documentation | The human-facing documentation of the work: each comment and docstring in its source, each document written for its users, maintainers, or readers, and each message that the work itself presents to a person. The working-notes workspace, the workbench, the records, knowledge entries, governance text and project instruments, instructions and briefs addressed to agents, and outputs with their provenance are not work documentation. |
| Human-facing writing | Work documentation, and each other text that an actor writes for a person to read: a report, a referral, a record, a commit message, and the text of governance. |
| Process record | A record of how the work is governed, built, or reviewed rather than of what the work is or does: a provision, a ledger entry, a waiver, a ruling, an authorization, a register, a classification, a unit record, a referral, a work report, and a record of review or audit. Requirements, specifications, the hazard analysis, the safe ranges of actuation, defect tracking, dependency records, and decision records under REPRO.7 describe the work and are not process records. |"""

NOTES = """The custodian's direction of 2026-10-22 asks that documentation read as one person talking to another: no notes an agent leaves for itself, no references to governance or ledgers, and no account of what an agent did. STND.DOCS.1 states the reader and the voice, and STND.DOCS.2 the content that makes documentation teach: terms defined on first use, examples where the use is not evident, the reasons behind the design, and its assumptions and limits. STND.DOCS.3 removes three kinds of content. The first is the agents themselves, their instructions, sessions, and actions, and notes addressed to the writer or to a later session; agents already keep these out under STND.INSTR.8, and the provision extends the rule to every writer. The second is narration of edits, which the version history holds (REPRO.5): "Changed to a stable sort" is history, while "A stable sort keeps equal keys in input order, which the merge step relies on" is documentation. A changelog, release note, migration note, or deprecation notice is written for users moving between revisions (DSGN.6, QA.13) and is documentation. The third is citation of process records. A known defect or limit is stated as a fact about the work, with its identifier in defect tracking where it has one (QA.4), and a suppressed warning or a deviation is explained by its technical reason, not by the waiver or ruling behind it. The explanation that AGENT.2 asks of an agent belongs in its work report or commit message.

The Process record term draws the line by subject. A record of what the work is or does stays citable: a constant's source under STND.CODE.10, a command limit traced to its safe range (PRIME.13), a requirement, a hazard, or a defect. A record of how the work is governed or reviewed does not appear in its documentation. STND.DOCS.4 covers the two cases that need the excluded content. Where the work's subject is its own governance or the conduct of agents, as in a governance harness, its documentation describes them and cites them because they are what the work is about. Where a law, a license, a contract, or a publisher's policy requires a statement that agents were used, the statement appears where the requirement puts it and says what the requirement asks, because the requirement binds on its own terms. Attribution of each change stays in the version history in every case (REPRO.5, STND.WPROC.2).

The language provisions apply to all human-facing writing, the custodian's words being "everywhere and at all times": documentation, reports to the human owner, commit messages, records, and governance text, whose provisions STND.DRAFT.33 already covers. The tables of STND.DRAFT.33 and STND.DOCS.5 list the commonest differences between British and American English; the rule is American spelling, punctuation, and usage in full, and where two spellings are current, the first that a standard American dictionary lists. Quotations, titles, proper names, literals, and names fixed outside the prose keep their own characters. Names in the source follow the same spelling, so that names agree across the custodian's projects, except a name that a dependency, a file format, an external interface, a persisted record, or a published interface of the work fixes; renaming such a name would break what depends on it.

STND.DOCS.6 rests on the field guide "Signs of AI writing" that Wikipedia editors keep, in the copy that the custodian supplied on 2026-10-22, and restates its signs in this standard's own words. The guide is descriptive: its signs are symptoms of writing that has drifted from specific facts toward generic, inflated statements, and it warns against treating the signs alone as the problem. The provision therefore states the underlying rule first, a specific, plain statement of each point with its source, and lists the patterns second. Each row names a habit; the words listed are typical of it, and a word in its technical sense is correct: an energy landscape, robust statistics, a leading underscore, a cryptographic key, a statistically powerful test. A list of three that has three members, an em dash in an aside, a required label, a hazard warning, and a structure that governance prescribes are also correct. The guide's own caution holds: no single pattern shows that text was generated, people use every one of them, and neither people nor detectors reliably tell the two apart, so the table is a tool for editing and says nothing about who wrote a text. The guide also lists what reads as written by a person: plain "is" and "has", plain words ("used", not "utilized"; "wrote", not "authored"), definite statements, and the ordinary qualifiers of speech. A fabricated or unresolvable reference also breaches PRIME.2.

Documentation and the work change together (STND.DOCS.8). For work under STND.WPROC, a change is the change that a unit branch carries to its parent, so documentation edits are made on the unit branch and conflicts between them are resolved when the branch is updated from its parent (STND.WPROC.8). A statement outside the version history, or in an instrument that only the human owner adopts, is recorded in defect tracking and referred when the change makes it false, because the writer of the change does not edit it. A statement agrees with the work at the revision it describes, so that a migration note describing an earlier revision is not in conflict. STND.DOCS.9 keeps one name for each concept; a mathematical symbol declared once and mapped to a name in the code is one name (INTPR.4, NUMER.4). STND.DOCS.10 runs the examples the documentation shows, within the checking environment and a stated tolerance, so that they fail when the work changes under them; a failing example is repaired with the work, and its shown result is not recaptured from a run that disagrees. These runs check the documentation and are not evidence for a claim of correctness. STND.DOCS.11 has the reviewer of each change look for the statements the change makes false, which a search for the names it alters finds.

STND.DOCS.7 is the floor of the standard. Every agent, at every class, writes in American spelling and usage, writes plainly and specifically without the patterns of STND.DOCS.6, and leaves no statement in the work documentation that it knows to be false of the work or of the documentation without recording it in defect tracking (GOV.48). These cost an agent its choice of words and a record, not additional documentation, so they raise no floor (GOV.11); the judgment is the custodian's, recorded here (PRIN.10). For people, the language and consistency provisions are defaults: STND.DOCS.2 and STND.DOCS.5 to STND.DOCS.11 instantiate provisions of the Articles that STND.CLASS.10 applies in full from CSQ3 and apply from CSQ3, INTPR.10 itself asking for the limits from CSQ2; work of CSQ4 may omit them. STND.DOCS.5 and STND.DOCS.6 cite INTPR.12, as STND.DRAFT.33 does for spelling, because a successor reads the work most readily in one variety of English without decoration. STND.DOCS.1, STND.DOCS.3, and STND.DOCS.4 fix how the floor documentation of INTPR.2 is written and ask for no documentation that the floor does not already require.

Existing text conforms when a change next touches it. Text in an append-only record, a superseded decision record, or a past commit message stays as written (PRIME.5, GOV.36)."""

DOCS = dict(
    id="STND.DOCS", title="Documentation standard",
    instantiates=["GOV.19", "GOV.48"],
    sections=[
        ("Purpose and scope", PURPOSE),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS),
        ("Notes", NOTES),
    ],
    provisions=[
        P(1, "Readers and voice", "Voice and content", """
Work documentation SHALL be written for a human reader who knows the domain of the work but not its code, as one person explaining the work to another (INTPR.1, INTPR.2).
""", ["INTPR.1", "INTPR.2"], mode="binding"),
        P(2, "Explanatory content", "Voice and content", """
Work documentation SHOULD define each term of art on its first use, give an example of each element whose use is not evident, and state why the work is built as it is, the assumptions it makes, and the limits of INTPR.10 (INTPR.1).
""", ["INTPR.1"], refs=["INTPR.10"]),
        P(3, "Content kept out of documentation", "Voice and content", """
Other than as STND.DOCS.4 permits, work documentation SHALL NOT name an agent that works on the work, state the instructions, sessions, or actions of such an agent, or hold a note addressed to its writer or to a later session (INTPR.2, INTPR.5). Other than in a changelog, a release note, a migration note, or a deprecation notice written for its users, work documentation SHALL NOT narrate the edits that brought the work to its present state, which the version history holds (INTPR.2, REPRO.5). Other than as STND.DOCS.4 permits, work documentation SHALL NOT cite a process record (INTPR.2).
""", ["INTPR.2", "INTPR.5"], refs=["STND.DOCS.4", "REPRO.5"], mode="binding"),
        P(4, "Agents and governance as subject", "Voice and content", """
Where the subject of the work is its governance or the conduct of agents, its work documentation MAY describe them and cite process records (INTPR.2). Where a law, a license, a contract, or a publisher's policy requires of the work a statement of the use of agents, its work documentation SHALL carry that statement, in the words and the place that the requirement names (INTPR.2, PRIN.2).
""", ["INTPR.2", "PRIN.2"], mode="binding"),
        P(5, "American spelling and usage", "Language", """
Other than in a quotation, a title, a proper name, a literal, or a name fixed outside the prose, human-facing writing SHOULD use American spelling, punctuation, and usage, those of the tables of STND.DRAFT.33 and of this provision included, and, of two current spellings, the first that a standard American dictionary lists (INTPR.12). Other than a name that a dependency, a file format, an external interface, a persisted record, or a published interface of the work fixes, each name in the source of the work SHOULD use American spelling (INTPR.1).

""" + USAGE_TABLE, ["INTPR.12", "INTPR.1"], refs=["STND.DRAFT.33"]),
        P(6, "Plain and specific statement", "Language", """
Human-facing writing SHOULD state each point specifically and plainly, and name the source of each point that rests on one (INTPR.12). Human-facing writing SHOULD NOT carry a pattern of the table of this provision (INTPR.12). A term of art in its technical sense, a quotation, a label or warning that another provision requires, and a structure that governance prescribes MAY take a form that the table lists (INTPR.12).

""" + PATTERN_TABLE, ["INTPR.12"], defines=["generated-prose-patterns"]),
        P(7, "Agent writing", "Language", """
An agent SHALL write its human-facing writing and the names it gives in the source of the work as STND.DOCS.5 and STND.DOCS.6 recommend, or as the alternatives that a project instrument adopts in their place require (GOV.48). Other than a statement recorded in defect tracking, an agent SHALL NOT leave in the work documentation a statement that it knows to disagree with the work or with another statement of the work documentation (GOV.48, INTPR.3).
""", ["GOV.48", "INTPR.3"], refs=["STND.DOCS.5", "STND.DOCS.6"], mode="binding"),
        P(8, "Documentation in step with the work", "Consistency", """
A change that alters the behavior, an interface, a default, a unit, a limit, or an output of the work SHOULD change, in the same change, each statement of the work documentation in its version history that describes what it alters (INTPR.3). Where such a statement lies outside the version history of the work or in an instrument that only the human owner adopts, the actor making the change SHOULD record the statement in defect tracking and refer it (INTPR.3, QA.4). Each statement of the work documentation SHOULD agree with the work at the revision it describes and with each other statement of the work documentation (INTPR.3).
""", ["INTPR.3", "QA.4"]),
        P(9, "One name per concept", "Consistency", """
Each concept of the work SHOULD carry one name across its code and its work documentation (INTPR.1, INTPR.3). Each name SHOULD carry one meaning (INTPR.1, INTPR.3). A symbol of a notation declared once and mapped to a name in the code MAY stand beside that name as the same name (INTPR.4).
""", ["INTPR.1", "INTPR.3", "INTPR.4"]),
        P(10, "Checked examples", "Consistency", """
Each example in the work documentation that runs in the checking environment without hardware, network access, a secret, or a destructive action SHOULD be run among the checks of each change that affects it, with its shown result compared within a stated tolerance (INTPR.3, VV.8). Where an example fails, its shown result SHOULD change only with a change to the work that the example describes (VV.8).
""", ["INTPR.3", "VV.8"]),
        P(11, "Documentation in change review", "Consistency", """
The review of each change SHOULD examine the human-facing writing that the change adds or alters, and each statement of the work documentation that names an element the change alters, against STND.DOCS.1, STND.DOCS.2, STND.DOCS.3, STND.DOCS.4, STND.DOCS.5, STND.DOCS.6, STND.DOCS.8, and STND.DOCS.9 (QA.7, INTPR.3).
""", ["QA.7", "INTPR.3"], refs=["STND.DOCS.1", "STND.DOCS.2", "STND.DOCS.3", "STND.DOCS.4", "STND.DOCS.5", "STND.DOCS.6", "STND.DOCS.8", "STND.DOCS.9"]),
    ],
)

NEW_DOCS7 = [DOCS]
