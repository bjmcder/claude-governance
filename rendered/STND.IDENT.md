# Identifier scheme and mnemonic register (STND.IDENT) 1.6

Adopted by The Custodian as revision 1.0 in ledger entry 10 (2026-10-09); revised to 1.1 in entry 18 (2026-10-09), 1.2 in entry 25 (2026-10-10), 1.3 in entry 27 (2026-10-10), 1.3.1 in entry 35 (2026-10-10), 1.3.2 in entry 45 (2026-10-10), 1.3.3 in entry 157 (2026-10-25), 1.4 in entry 182 (2026-10-26), 1.5 in entry 295 (2026-10-28), and 1.6 in entry 339 (2026-10-31). This reading copy is composed from the per-provision files in STND/IDENT/ of the governance harness; the harness files are the system of record.

## Purpose and scope

The section Revisions fixes what the segments of the revision number of a constitution, profile, sub-profile, or standard mean, which change raises which segment, and how a revision is recorded in the document and in the ledger (GOV.43, GOV.40). The section Identifiers fixes the forms of identifiers, locators, slugs, and mnemonics, the mnemonic register and its changes, and withdrawn identifiers (GOV.37). Every provision is binding, because a revision number and an identifier each have to mean the same thing in every project (GOV.42, GOV.37).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Every other part of this document is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Revision number | The number that names one exact state of a constitution, profile, sub-profile, or standard, written as major.minor or as major.minor.editorial, as in 1.0 or 1.0.2. |
| Major segment | The first whole number of a revision number. It is zero until the document is first adopted. |
| Minor segment | The second whole number of a revision number. |
| Editorial segment | The third whole number of a revision number, shown only when it is above zero. |
| Revision history | The table of a document's revisions, in order, each with its date and a change entry. |
| Role label | The name of a role that the Lexicon defines, with the word The before it, as in The Custodian or The Human Owner. A plural Lexicon term gives the singular label. |
| Number | A whole number from 1, written without leading zeros. |
| Grade | A mnemonic of an ordinal scale followed by one digit, as in CSQ0. |
| Parent | The mnemonic before a mnemonic in an identifier; none for a first mnemonic; project for the mnemonic that follows the mnemonic of a project. |
| Letter distance | The least number of letters inserted, deleted, or substituted that turns one mnemonic into another. |
| Retired item | An item whose field `status` is retired, a provision that a field `withdrawn` lists, or a deprecated tag. |

## Reading the three classes

A major change is large and fundamental: it alters a prime directive or a governing principle in its motivation or intent, or restructures the articles wholesale. A minor change is an ordinary amendment: it adds, alters, or removes an obligation, permission, or defined meaning, and leaves the fundamental motivation and intent of the governance as they were. An editorial change alters no obligation, permission, or defined meaning. Correcting a typographical slip and rewording a sentence without changing what it requires are editorial changes. So is defining a term for a sense that provisions already use, because the definition alters no meaning that the provisions rely on. Revision 1.0.2 of the constitution, which defined the roles Author, Adopter, and Auditor, is an example.

## Examples of identifiers

| Item | Example |
| --- | --- |
| Constitution | LVL0 |
| Document | STND.CLASS, HW.FPGA |
| Space of tags | TAG.METH |
| Provision | GOV.12, STND.CLASS.20 |
| Lexicon term | LEX.relying-party |
| Tag | TAG.METH.monte-carlo |
| Knowledge entry in a space NUMER | KNOW.NUMER.4 |
| Waiver of a project NAME | NAME.WAIV.3 |
| Locator | LVL0#normative-language |

## Representation in the harness

Each provision is one file, `STND/IDENT/<n>.md`, with the fields the drafting standard fixes. The provision that holds the table of revision classes names it `revision-classes` in the field `defines`, and the harness reads the table by that name and by its column headings. A document of kind constitution, profile, sub-profile, or standard carries the field `revision`; a project instrument does not. The mnemonic register (MNEM) is the file `MNEM/_doc.md`. It holds the mnemonics of the corpus and of each kind of LVL3 instrument, which the custodians register. The mnemonic of a project is held in the project's own ledger instead, by a transaction that its human owner makes before the project's first instrument that carries it, under the defaults by an act that an agent enters under STND.DFLT.17 (STND.IDENT.23), so that a project names itself without an act of the custodians. The transaction is of type register, in the project's ledger, with the mnemonic as its one target and the words "project mnemonic" in its rationale, so that a harness given that ledger reads it. The mnemonic meets the form of STND.IDENT.17 and the choice of STND.IDENT.18, and one that MNEM already holds is not chosen, so that no identifier of the project reads as one of the corpus. A project that adopts no such instrument registers nothing.

## Checks

The harness reports the revision checks (family v) with `python -m govharness check` and `verify`. Each fails, because a revision record that disagrees with itself or with the ledger defeats its purpose. The checks read the table of revision classes, the revision history of each adopted document, and the ledger. Whether a change was given the class its content warrants is a judgment, and whether each redraft of a draft raised the minor segment by one is not readable from the files, because a draft keeps no revision history. A reader therefore checks the provisions on classing a change and on redrafting. The check v.8 compares the numbered provisions of each document with its field `withdrawn`, and those of each part of the constitution with the field `withdrawn` of the constitution: a gap in the numbering that the field does not list, a listed identifier that names a provision or is not the document's own, or a cited identifier that names no provision and is not listed, fails. The check v.9 compares the identifier of every item, and every identifier in its fields, with the form for its kind, and the slug of every Lexicon term with its term. The check v.10 reads the mnemonic register, confirms that the identifier of every item that is not retired uses only active mnemonics and registered grades, and lists for a reader each pair of siblings at a letter distance of 1 that are not established acronyms. The check v.11 confirms that every transaction with the scope MNEM is of type register and made by the custodians.

## References

| Identifier | Title |
| --- | --- |
| GOV | Governance |
| LEX | Lexicon |
| LVL0 | Constitution for Computational and Cyber-Physical Systems |
| MNEM | Mnemonic register |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |

## Provisions

### Revisions

#### STND.IDENT.1 Revision number

Binding. Instantiates GOV.43.

A constitution, profile, sub-profile, or standard SHALL carry a revision number made of a major segment and a minor segment, followed by an editorial segment after the first editorial amendment (GOV.43). Each segment SHALL be a whole number written without leading zeros (GOV.43).

#### STND.IDENT.2 Zero editorial segment

Binding. Instantiates GOV.43.

A revision number SHALL NOT show an editorial segment of zero (GOV.43).

#### STND.IDENT.3 Revision classes

Binding. Instantiates GOV.40, GOV.41.

A change to a constitution, profile, sub-profile, or standard SHALL be classed by the first row of the table of this provision whose test the change meets (GOV.40, GOV.41).

| Class | Segment raised | Ledger type | Opening words | Test |
| --- | --- | --- | --- | --- |
| Adoption | major | adopt | Adopted, Ratified | The document is adopted for the first time. |
| Major | major | amend | Major amendment | The change alters a prime directive or a governing principle in its fundamental motivation or intent, or restructures the articles wholesale. |
| Minor | minor | amend | Minor amendment | The change adds, alters, or removes an obligation or permission, or alters a defined meaning, without altering the fundamental motivation or intent of the governance. |
| Editorial | editorial | amend | Editorial amendment | The change alters no obligation, permission, or defined meaning. Defining a term for a sense that provisions already use is editorial. |

#### STND.IDENT.4 Doubtful class

Binding. Instantiates GOV.40, GOV.41.

A change whose class is in doubt SHALL take the class nearer the top of the table of STND.IDENT.3. The adopter of the document SHALL record the reason for the class in the text that gives the reason of the ledger transaction (STND.IDENT.8, GOV.40, GOV.41).

#### STND.IDENT.5 Segment step

Binding. Instantiates GOV.43.

A change SHALL raise the segment that the table of STND.IDENT.3 names for its class by one. The change SHALL set every segment to the right of that segment to zero (GOV.43).

#### STND.IDENT.6 Revision history

Binding. Instantiates REPRO.5.

A document of a kind listed in STND.IDENT.1 that has been adopted SHALL keep a revision history, a table whose rows run in order of revision and give the revision number, the date, and a change entry (REPRO.5). The change entry SHALL open with the opening words that the table of STND.IDENT.3 gives for the class of the change (REPRO.5). The change entry of an amendment SHALL cite GOV.40 for LVL0 and GOV.41 for every other document (REPRO.5).

#### STND.IDENT.7 Revision field

Binding. Instantiates REPRO.5.

A document of a kind listed in STND.IDENT.1 SHALL state its current revision number in the front-matter field `revision` (REPRO.5). The field SHALL equal the revision number of the last row of the revision history (REPRO.5).

#### STND.IDENT.8 Revision transaction

Binding. Instantiates REPRO.5.

Each revision of an adopted document of a kind listed in STND.IDENT.1 SHALL be entered in the ledger as one transaction of the type that the table of STND.IDENT.3 names for its class (REPRO.5). The transaction SHALL name the document among its targets and state the revision number in the text that gives its reason (REPRO.5).

#### STND.IDENT.9 No revision reuse

Binding. Instantiates GOV.43.

A revision number SHALL NOT be reused or renumbered (GOV.43).

#### STND.IDENT.10 Revisions before adoption

Binding. Instantiates GOV.43.

A document of a kind listed in STND.IDENT.1 that is not yet adopted SHALL carry a major segment of zero. Each redraft of it SHALL raise its minor segment by one (GOV.43).

#### STND.IDENT.11 First adoption

Binding. Instantiates GOV.41.

The first adoption of a document of a kind listed in STND.IDENT.1 SHALL set its revision number to 1.0 (GOV.41).

#### STND.IDENT.12 Adopter label

Binding. Instantiates GOV.41.

A constitution, profile, sub-profile, or standard that is adopted or ratified SHALL name its adopter in the field `adopted_by`, or in the field `ratified_by` for the constitution, by the label of a role that the Lexicon defines (GOV.41).

#### STND.IDENT.13 Recorded review

Binding. Instantiates GOV.43.

The QA.7 review of each revision of an adopted document SHALL be recorded no later than the ledger transaction of that revision (GOV.43). Where no review transaction precedes the transaction of a revision whose adopter is not its author, the adopter's decision recorded in that transaction MAY serve as the QA.7 review of that revision (GOV.43).

### Identifiers

#### STND.IDENT.14 Withdrawn identifiers

Binding. Instantiates GOV.37.

A document of a kind listed in STND.IDENT.1 SHALL list in its front-matter field `withdrawn` the identifier of each of its provisions that a revision withdraws (GOV.37). A withdrawn identifier SHALL NOT be given to another provision (GOV.37).

#### STND.IDENT.15 Identifier form

Binding. Instantiates GOV.37.

An identifier SHALL take the form that the table of this provision gives for the kind of item it names (GOV.37).

| Item | Form |
| --- | --- |
| Constitution | LVL0 |
| Document, register, or space of knowledge entries or tags | Mnemonics joined by dots |
| Provision | The identifier of its document, a dot, and a number |
| Lexicon term | The mnemonic LEX, a dot, and the slug of the term |
| Tag | The identifier of its facet, a dot, and the slug of the tag |
| Knowledge entry | The identifier of its space, a dot, and a number |
| Project instrument | The mnemonics of the project and of the kind of instrument, and a number, joined by dots |
| Locator | The identifier of a document, a number sign, and the slug of one of its headings |

#### STND.IDENT.16 Slug

Binding. Instantiates GOV.37.

The slug of a Lexicon term, of a tag, or of a heading SHALL be its text in lowercase, with each run of characters other than the letters a to z and the digits 0 to 9 replaced by one hyphen, and with no hyphen at either end (GOV.37).

#### STND.IDENT.17 Mnemonic form

Binding. Instantiates GOV.37.

A mnemonic SHALL be from two to five uppercase letters, both bounds inclusive (GOV.37).

#### STND.IDENT.18 Mnemonic choice

Binding. Instantiates GOV.37.

Where what a new mnemonic names has an established acronym that does not read as another common term of covered work, the mnemonic SHOULD be that acronym (GOV.37). Where a new mnemonic is not an established acronym, it SHOULD be at a letter distance of at least 2 from each mnemonic with the same parent (GOV.37). A new mnemonic SHOULD NOT read as a common term of covered work (GOV.37).

#### STND.IDENT.19 Mnemonic register

Binding. Instantiates GOV.37.

The mnemonic register SHALL be the table in MNEM that has one row for each mnemonic under each parent, giving the mnemonic, its parent, what it names, its grades, the reason for its form, and its status, active or retired, with none in each cell that has nothing to give (GOV.37).

#### STND.IDENT.20 Register transaction

Binding. Instantiates GOV.37.

Each change to the mnemonic register SHALL be a ledger transaction of type register that names MNEM as its scope (GOV.37).

#### STND.IDENT.21 Permanent rows

Binding. Instantiates GOV.37.

A row SHALL NOT be removed from the mnemonic register (GOV.37). Where the item that a mnemonic names is retired, the row of the mnemonic SHALL be marked retired (GOV.37).

#### STND.IDENT.22 Mnemonic and grade use

Binding. Instantiates GOV.37.

Where an item is not retired, its identifier SHALL use only the mnemonics that the mnemonic register holds as active and the grades that it gives for their scales (GOV.37).

#### STND.IDENT.23 Registering authority

Binding. Instantiates GOV.41, GOV.37.

The custodians SHALL register each mnemonic other than the mnemonic of a project, the mnemonic of each kind of LVL3 instrument included (GOV.41, GOV.37). Where a project adopts an instrument whose identifier carries a mnemonic of the project, the human owner of the project SHALL first register that mnemonic, one that the mnemonic register does not hold, by a transaction of the project's ledger (GOV.41, GOV.37).

#### STND.IDENT.24 Withdrawn constitution provisions

Binding. Instantiates GOV.37.

The constitution SHALL list in its field `withdrawn` the identifier of each provision of a part named in its field `parts` that a revision withdraws (GOV.37).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-09 | Adopted. |
| 1.1 | 2026-10-09 | Minor amendment (GOV.41): STND.IDENT.13 (Recorded review) requires the QA.7 review of each revision to be recorded no later than its transaction and lets the adopter's recorded decision serve as that review (ruling of ledger entry 15); STND.IDENT.6 fixes the citation of amendments (GOV.40 for LVL0, GOV.41 otherwise); STND.IDENT.3 and STND.IDENT.4 also instantiate GOV.41; STND.IDENT.9 instantiates GOV.43 in place of GOV.37. |
| 1.2 | 2026-10-10 | Minor amendment (GOV.41): STND.IDENT.14 requires each document to list its withdrawn identifiers in the field `withdrawn` and forbids giving one to another provision (GOV.37); check v.8 enforces it. |
| 1.3 | 2026-10-10 | Minor amendment (GOV.41): the section Identifiers gains STND.IDENT.15 to STND.IDENT.23, which fix the forms of identifiers, locators, slugs, and mnemonics, the choice of mnemonics, the mnemonic register MNEM, its transactions and permanent rows, the use of mnemonics and grades, and the custodians' authority to register mnemonics; Terms gains Number, Grade, Parent, Letter distance, and Retired item. |
| 1.3.1 | 2026-10-10 | Editorial amendment (GOV.41): the section References lists the documents this standard cites, as STND.DRAFT.34 requires; no obligation changes. |
| 1.3.2 | 2026-10-10 | Editorial amendment (GOV.41): the Checks section names the commands of the harness package instead of the retired scripts; no obligation changes. |
| 1.3.3 | 2026-10-25 | Editorial amendment (GOV.41): the informative section Representation in the harness cites the mnemonic register MNEM, which STND.IDENT.19 and STND.IDENT.20 name, and References lists MNEM; no obligation, permission, or defined meaning changes. |
| 1.4 | 2026-10-26 | Minor amendment (GOV.41): STND.IDENT.12 asks the label of its adopter only of a document that is adopted or ratified, so a draft or a planned document names none; new STND.IDENT.24: the constitution lists in its field withdrawn each withdrawn provision of the parts named in its field parts; the section Checks describes v.8 in full, with the field withdrawn of the constitution. Transition (GOV.42): none. |
| 1.5 | 2026-10-28 | Minor amendment (GOV.41): the adopter's decision serves as the QA.7 review of a revision only where the adopter is not the author of that revision. |
| 1.6 | 2026-10-31 | Minor amendment (GOV.41): STND.IDENT.23 has the custodians register each mnemonic other than that of a project, the mnemonic of each kind of LVL3 instrument included, and, where a project adopts an instrument whose identifier carries a mnemonic of the project, the human owner first register that mnemonic, one that the mnemonic register does not hold, by a transaction of the project's ledger (R6); the Notes say where the mnemonic of a project is held and fix the form of that transaction. |
