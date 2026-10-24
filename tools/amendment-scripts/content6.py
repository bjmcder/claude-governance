"""STND.DOCS draft 0.1: the documentation standard, from the custodian's direction of 2026-10-22."""
from content3 import P, NORMATIVE, TERMS_LEAD

DATE = "2026-10-22"

USAGE_TABLE = """| Not used | Used |
| --- | --- |
| whilst, amongst | while, among |
| towards, afterwards, forwards | toward, afterward, forward |
| learnt, spelt, dreamt | learned, spelled, dreamed |
| licence (noun), practise (verb) | license, practice |
| enquiry, tyre, kerb, plough | inquiry, tire, curb, plow |
| aluminium, sulphur, maths | aluminum, sulfur, math |
| different to | different from |
| in future (meaning "from now on") | in the future |
| at the weekend | on the weekend |
| fortnight | two weeks |
| 22 October 2026, in running text | October 22, 2026 |
| 'quoted', with the period outside | "quoted," with the comma or period inside |"""

PATTERN_TABLE = """| Pattern | Typical forms |
| --- | --- |
| Importance asserted rather than shown | "plays a pivotal role", "a testament to", "crucial", "vital", "key", "landmark", "enduring legacy", attached to a fact whose importance the text does not demonstrate |
| Promotional adjectives in place of measured claims | "powerful", "seamless", "robust", "cutting-edge", "state-of-the-art", "groundbreaking", "elegant", "rich", "vibrant" |
| Inflated vocabulary where a plain word serves | "delve", "tapestry", "intricate", "underscore", "showcase", "foster", "garner", "landscape", "realm", "navigate", "leverage", "utilize", "interplay", "multifaceted", "holistic", "embark", "unlock" |
| A copula avoided | "serves as", "stands as", "acts as", "boasts", "features" where "is" or "has" is meant |
| A trailing participle that claims significance | a closing "highlighting ...", "underscoring ...", "reflecting ...", "ensuring ...", "showcasing ..." that names no consequence |
| Negative parallelism for emphasis | "not just X, but Y", "it's not X, it's Y", "not only X but also Y", where no reader holds the view being denied |
| Reflexive groups of three | three adjectives, nouns, or clauses where the content has some other number of items |
| False ranges | "from X to Y" where X and Y are not the ends of one scale |
| One thing under several names | a function, quantity, or concept renamed from sentence to sentence to avoid repeating a word |
| Editorial asides | "it is important to note", "it is worth mentioning", "notably", "interestingly", "importantly", "crucially" |
| Vague attribution | "experts say", "studies show", "it is widely regarded", "many believe", with no source named |
| Stacked hedges and filler | "may potentially", "it could be argued", "in order to", "a variety of", "various", "it should be noted" |
| Summaries that restate | a closing "in summary", "in conclusion", or "overall" paragraph that repeats the text above it; a closing section on challenges and future directions that says nothing particular to the work |
| Conversation addressed to a requester | "Certainly!", "Great question", "I hope this helps", "Let me know if", "Here is what you asked for", praise of the reader, a statement of the writer's knowledge cutoff or nature |
| Gaps covered by speculation or placeholders | "while details are limited", "it is likely that" where the writer has not checked, "[insert ...]", "TBD" left in finished text |
| Decoration of plain text | bold scattered through prose, headings over a sentence or two, title case in headings, lists of bold term and description where prose reads better, emoji, markup that the medium does not render |
| Dashes in place of ordinary punctuation | an em dash in place of a comma, colon, or parentheses, more than once in a paragraph |
| Residue of generating tools | citation tokens, tracking parameters in links, mixed straight and curly quotation marks, references that do not resolve |"""

DOCS = dict(
    id="STND.DOCS", title="Documentation standard",
    instantiates=["GOV.19", "GOV.48"],
    sections=[
        ("Purpose and scope", """This standard governs the writing that people read: the documentation of the work, which is its comments, docstrings, documents, and messages, and every other text that an actor writes for a person, reports and records included. Documentation is written by one person for another. It says what the work does, how to use it, why it is built as it is, and where it stops being valid, and it says nothing about the agents that helped write it or the governance under which they worked, which belong in the records (STND.DOCS.1 to STND.DOCS.3). All of this writing uses American spelling and usage (STND.DOCS.4) and avoids the habits that mark text as generated rather than written (STND.DOCS.5). Documentation agrees with the work at every revision and with itself (STND.DOCS.6 to STND.DOCS.9). STND.DOCS.1 to STND.DOCS.6 instantiate the floor obligation of INTPR.2 and are binding at every class; STND.DOCS.7 to STND.DOCS.9 are defaults (GOV.19). Conventions for docstrings and comments in a particular language belong to the standard for that language."""),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS_LEAD + """ Agent, Record, and Human-facing documentation have the meanings the Lexicon gives them.

| Term | Definition |
| --- | --- |
| Work documentation | Each comment and docstring in the source of the work, each document written for its users, maintainers, or readers, and each message that the work itself presents to a person. |
| Human-facing writing | Work documentation, and each other text that an actor writes for a person to read: a report, a referral, a record, a commit message, and the text of governance. |
| Governance record | A provision, a ledger entry, a waiver, a ruling, an authorization, a register, or a record of review or audit kept under the governance of the work; the hazard analysis, the requirements, and the defect tracking of the work are engineering records, not governance records. |"""),
        ("Notes", """The custodian's direction of 2026-10-22 asks that documentation read as one person talking to another: no notes an agent leaves for itself, no references to governance or ledgers, and no account of what an agent did. STND.DOCS.1 states the voice. STND.DOCS.2 removes the content that does not belong: names of agents and sessions, their instructions and actions, notes addressed to the writer or to a later session, and narration of edits, all of which the version history and the working-notes workspace already hold (REPRO.5, INTPR.5, STND.INSTR.8); and citations of governance records. A comment explains the code as it stands. "Changed to use a stable sort" is history; "A stable sort keeps equal keys in input order, which the merge step relies on" is documentation. A known defect or limit is stated as a fact about the work, with its identifier in defect tracking where one exists (INTPR.10).

Two cases need the excluded content. Where the work's subject is its own governance or the conduct of agents, as in a governance harness, its documentation describes them because they are what the work is about (STND.DOCS.3). Where a law, a license, or a publisher's policy requires a statement that agents were used, the statement appears where the requirement puts it, because concealing it would be dishonest (PRIN.2). Attribution of each change stays in the version history in every case (REPRO.5).

The language provisions apply to all human-facing writing, the custodian's word being "everywhere and at all times": documentation, reports to the human owner, commit messages, records, and the informative parts of governance, whose provisions STND.DRAFT.33 already covers. The tables of STND.DRAFT.33 and STND.DOCS.4 list the commonest differences; the rule is American spelling and usage in full, and the tables are a reminder. Identifiers follow the same spelling so that names agree across the custodian's projects, except where a dependency, a file format, or another external interface fixes the name.

STND.DOCS.5 draws on the field guide that Wikipedia editors keep on the signs of AI writing. The guide could not be retrieved directly when this standard was drafted; the table rests on published accounts of it and on prior familiarity with its contents, restated in this standard's own words. Each row names a habit; the words listed are typical of it. "Landscape" in an energy landscape, "robust" in robust statistics, a list of three that has three members, and an em dash in an aside are all correct; the provision rejects the word or form where it stands in for content. The guide's own caution applies: no single pattern proves that text was generated, and human writers use every one of them, so the table is a tool for editing and says nothing about who wrote it. A fabricated or unresolvable reference also breaches PRIME.2.

Documentation and the work change together (STND.DOCS.6). A change that alters behavior, an interface, a default, a unit, a limit, or an output updates in the same change every statement that describes it, and no statement may contradict another anywhere in the documentation, which INTPR.3 counts as a defect. STND.DOCS.7 keeps one name for each concept, which is the code-level form of the same rule and removes the synonym cycling of STND.DOCS.5. STND.DOCS.8 runs the examples the documentation shows, so that they fail when the work changes under them, and STND.DOCS.9 has the reviewer of each change look for the statements the change makes false, which a search for the names it alters finds.

Under STND.CLASS.10, STND.DOCS.1 to STND.DOCS.6 apply at every class: each fixes how the documentation that INTPR.2 requires at the floor is written, at the cost of wording and of keeping statements true, and none asks for documentation that the floor does not already require, so binding them raises no floor (GOV.11); the judgment is the custodian's, recorded here (PRIN.10). STND.DOCS.4 also carries the custodians' reason of uniformity across projects for identifiers (GOV.19). STND.DOCS.7 to STND.DOCS.9 instantiate provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and apply from CSQ3; work of CSQ4 omits them. The standard names no language, tool, or format (GOV.18)."""),
    ],
    provisions=[
        P(1, "Voice of documentation", "Voice and content", """
Work documentation SHALL be written as one person explaining the work to another, in the vocabulary of the work's domain, stating what the work does, how to use it, why it is built as it is, and its assumptions and limits (INTPR.1, INTPR.2).
""", ["INTPR.1", "INTPR.2"], mode="binding"),
        P(2, "Content kept out of documentation", "Voice and content", """
Work documentation SHALL NOT name an agent that works on the work, its sessions, its instructions, or its actions, or hold a note addressed to its writer or to a later session (INTPR.2, INTPR.5). Work documentation SHALL NOT recount the edits that brought the work to its present state, which the version history holds (INTPR.2, REPRO.5). Work documentation SHALL NOT cite a governance record (INTPR.2).
""", ["INTPR.2", "INTPR.5"], refs=["REPRO.5"], mode="binding"),
        P(3, "Agents and governance as subject", "Voice and content", """
Where the subject of the work is its governance or the conduct of agents, its documentation MAY describe them as that subject (INTPR.2). Where a law, a license, or a publisher's policy requires of the work a statement of the use of agents, its work documentation MAY carry that statement in the place the requirement names (INTPR.2, PRIN.2).
""", ["INTPR.2", "PRIN.2"], mode="binding"),
        P(4, "American spelling and usage", "Language", """
Human-facing writing SHALL use American spelling and usage, those of the tables of STND.DRAFT.33 and of this provision included (INTPR.2). Other than a name that a dependency, a file format, or another interface outside the work fixes, each identifier in the work SHALL use American spelling (INTPR.1, INTPR.2).

""" + USAGE_TABLE, ["INTPR.2", "INTPR.1"], refs=["STND.DRAFT.33"], mode="binding",
          reason="One spelling across the custodian's projects keeps identifiers, interfaces, and searches compatible between them."),
        P(5, "Habits of generated prose", "Language", """
Human-facing writing SHALL NOT use a pattern of the table of this provision (INTPR.2).

""" + PATTERN_TABLE, ["INTPR.2"], mode="binding", defines=["generated-prose-patterns"]),
        P(6, "Documentation in step with the work", "Consistency", """
A change that alters the behavior, an interface, a default, a unit, a limit, or an output of the work SHALL change, in the same change, each statement of the work documentation that describes what it alters (INTPR.2, INTPR.3). Each statement of the work documentation SHALL agree with the work at the same revision and with each other statement of the work documentation (INTPR.2, INTPR.3).
""", ["INTPR.2", "INTPR.3"], mode="binding"),
        P(7, "One name per concept", "Consistency", """
Each concept of the work SHOULD carry one name across its code and its work documentation (INTPR.1, INTPR.3). Each name SHOULD carry one meaning (INTPR.1, INTPR.3).
""", ["INTPR.1", "INTPR.3"]),
        P(8, "Checked examples", "Consistency", """
Each example in the work documentation that the work is able to run SHOULD be run, with its shown result compared, among the checks of each change that affects it (INTPR.3, VV.8).
""", ["INTPR.3", "VV.8"]),
        P(9, "Documentation in change review", "Consistency", """
The review of each change SHOULD examine the work documentation that the change touches, and each statement elsewhere in the work documentation that names an element the change alters, against STND.DOCS.1, STND.DOCS.2, STND.DOCS.3, STND.DOCS.4, STND.DOCS.5, STND.DOCS.6, and STND.DOCS.7 (QA.7, INTPR.3).
""", ["QA.7", "INTPR.3"], refs=["STND.DOCS.1", "STND.DOCS.2", "STND.DOCS.3", "STND.DOCS.4", "STND.DOCS.5", "STND.DOCS.6", "STND.DOCS.7"]),
    ],
)

NEW_DOCS6 = [DOCS]
