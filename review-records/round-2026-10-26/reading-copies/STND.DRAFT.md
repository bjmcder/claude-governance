# Drafting standard (STND.DRAFT) 1.5

This reading copy is composed from the per-provision files in STND/DRAFT/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard fixes how normative words are written below LVL0 and which expressions are excluded, the two functions the Lexicon gives a drafting standard. It also sets the form of numbered provisions: precision, citation, structure, roles and terms, and style. The provisions that write and exclude normative words are binding, because Normative Language assigns them to this standard and every project reads each word the same way. The provisions of citation that rest on PRIME.15, GOV.19, and the Lexicon preface are binding for the reasons those provisions record. The remaining provisions are defaults (GOV.19) that a project instrument replaces by recorded decision (REPRO.7) with an alternative that meets the same outcome. The provisions on profiles fix how a profile states its selector, names the subjects of its provisions, allocates shared matters, places obligations at the boundaries between domains, and asks for evidence, so that the profiles a project selects combine without conflict (GOV.25, GOV.26); they are binding because they instantiate GOV, which the floor holds (GOV.10), and each records why uniformity requires it. A provision about a domain item imposes nothing where no such item occurs (GOV.25). A citation of another profile's provision does not select that profile; where a provision requires what a cited provision of another profile states, that requirement binds wherever the citing provision binds, and the citing provision adds only its domain's increment. Where an owning profile is adopted after a profile that addresses its matter, the earlier profile conforms within the transition period that the later adoption records (GOV.42). STND.DRAFT.42 serves the aim of governance below LVL0: work that agents carry out unattended, to a quality the human owner trusts, with the human owner asked only for what LVL0 requires of or reserves to the human owner, and with standing authorizations given once in place of per-action requests wherever LVL0 permits them. Lower governance spends its obligations on two dangers: an immediate unsafe or insecure action, and silent misalignment that leaves work of poor quality, fragile, or latently incorrect.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Every other part of this document, including this section, is informative. A sentence with a modal is normative wherever it stands, so the informative parts of this document contain none.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Modal | One of the five words in the table of STND.DRAFT.1. |
| Excluded expression | An expression of the table of STND.DRAFT.7. |
| Sentence | Text that ends at a period, a question mark, or an exclamation point, or at the end of a paragraph, a list item, or a table cell, not counting a mark inside an identifier, a number, an abbreviation, or quotation marks. |
| Informative sentence | A sentence that states no obligation, prohibition, recommendation, or permission. |
| Imperative sentence | A sentence whose main verb is in the imperative mood and names no actor. |
| Status word | A phrase of the Normative Language table that states a status of an artifact, such as "is a defect" or "has no authority". |
| Locator | A reference to one heading of a document, in the form that STND.IDENT.15 gives, as in "LVL0#normative-language". |
| Instantiated provision | A higher provision that a provision makes more specific and does not relax, listed in the field `instantiates`. |
| Referred provision | A provision that a provision names without instantiating it, listed in the field `refers_to`. |
| Attribute | A yes-or-no fact about the work that the classification records and a selector tests. |
| Assigned decision | A decision of the human owner that a LVL0 provision requires of the human owner or reserves to the human owner. |
| Decision of the human owner | An adoption, authorization, approval, ruling, or other act of the human owner, and a referral that awaits one. |
| Domain item | A thing of a profile's domain that its provisions govern, such as a computed result, an acquisition, or an actuation command. |
| Execution path | The term that HW defines. |
| Owning profile | The profile whose shared-matters table gives a shared matter as its own. |
| Shared matter | A subject of obligations that one profile owns and that other profiles address by citing the owning profile's provisions, such as the uncertainty of a computed result or a safe state. |
| Subject | The thing that a provision's obligation concerns, named in the provision. |
| Cited document | A document other than the citing one, named, itself or through one of its provisions, terms, or locators, in a citation or a reference field of the citing document or of its provisions, or named in their text by its identifier alone. A name by identifier alone does not count inside quotation marks, a code span, a table with a column headed Example, the section References, or the revision history, and the identifier LVL0 alone never counts. |

## Representation in the harness

Each provision is one file, `STND/DRAFT/<n>.md`, whose identifier is `STND.DRAFT.<n>` and never changes (GOV.37). Besides the common fields, a provision carries:

- `mode`: `binding` or `default` (GOV.19).
- `binding_reason`: the uniformity reason, present when a binding provision reaches no prime directive, GUARD provision, or floor obligation.
- `instantiates` and `refers_to`: identifiers and locators, as the provisions on citation fix.
- `rank` and `waivable`: derived from the closure of `instantiates` (GOV.5, GOV.17); the harness verifies them and does not choose them.
- `defines`: the name of a table that the provision holds. The harness reads each table by this name and by its column headings, so rewording a sentence cannot empty a list.
- `checked_by`: the checks that verify the provision. The value `review` means a reader decides.

A profile's tables named selector and shared-matters are read by the harness by their column headings: Attribute and Defined by; Matter, Owning profile, and Provisions. The Provisions column gives each provision by its full identifier, separated by commas. A selector provision states, for example, that the profile binds a project whose classification makes at least one attribute of its table true; a shared-matters provision states that each matter of its table is governed in the document by the provisions that the table gives for it.

## Checks

The harness reports the lineage checks (family l) and the drafting checks (family g) with `python -m govharness check`. A finding in this standard fails. A finding in another document fails when this standard is adopted and a binding provision of this standard names the check in its field `checked_by`, and warns otherwise. Findings in LVL0 and in documents not yet divided into numbered provisions form an advisory punch list and never fail, because this standard governs below LVL0 and numbered provisions. The check g.25 compares each references table with the cited documents that `python -m govharness references` derives from the corpus and writes. The command derives a row for each document that the text names by its identifier alone, as for a citation, and g.25 fails where the table lacks it, whether or not a citation backs the name.

## References

| Identifier | Title |
| --- | --- |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| INTPR | Interpretability |
| LEX | Lexicon |
| LVL0 | Constitution for Computational and Cyber-Physical Systems |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| STND.IDENT | Identifier scheme and mnemonic register |

## Provisions

### Normative words

#### STND.DRAFT.1 Modal set

Binding. Instantiates LVL0#normative-language.

A numbered provision SHALL express obligation, prohibition, recommendation, recommendation against, and permission only with the modals of the table of this provision (LVL0#normative-language).

| Modal | Expresses | Normative Language entry | Lowercase |
| --- | --- | --- | --- |
| SHALL | obligation | shall | exact |
| SHALL NOT | prohibition | shall not | exact |
| SHOULD | recommendation | should | exact |
| SHOULD NOT | recommendation against | should not | exact |
| MAY | permission | may | review |

#### STND.DRAFT.2 Capital letters

Binding. Instantiates LVL0#normative-language.

A modal SHALL be written in capital letters (LVL0#normative-language).

#### STND.DRAFT.3 Mentioned words

Binding. Instantiates LVL0#normative-language.

Outside a column whose entries are modals or excluded expressions, a modal or an excluded expression that a provision mentions without using it SHALL be enclosed in quotation marks (LVL0#normative-language).

#### STND.DRAFT.4 Explicit modal

Binding. Instantiates LVL0#normative-language.

A sentence of a numbered provision that states an obligation, a prohibition, a recommendation, or a permission SHALL contain exactly one modal (LVL0#normative-language).

#### STND.DRAFT.5 Unmodalized sentences

Binding. Instantiates LVL0#normative-language.

A sentence of a numbered provision that contains no modal, states no status word, and is not an imperative sentence SHALL be read as informative (LVL0#normative-language).

#### STND.DRAFT.6 Normative extent

Binding. Instantiates LVL0#normative-language.

A sentence outside the body of a numbered provision that contains no modal SHALL be read as informative. A sentence outside the body of a numbered provision that contains a modal SHALL be read as normative (LVL0#normative-language).

#### STND.DRAFT.7 Excluded expressions

Binding. Instantiates LVL0#normative-language.

A numbered provision SHALL NOT use an expression of class exact in the table of this provision (LVL0#normative-language).

| Expression | Class | Read as |
| --- | --- | --- |
| must | exact | SHALL |
| must not | exact | SHALL NOT |
| SHALL NEVER | exact | SHALL NOT |
| NEVER | exact | SHALL NOT |
| may not | exact | SHALL NOT |
| is required | exact | SHALL |
| is mandatory | exact | SHALL |
| needs to | exact | SHALL |
| has to | exact | SHALL |
| is expected to | exact | SHALL |
| is supposed to | exact | SHALL |
| is prohibited | exact | SHALL NOT |
| is forbidden | exact | SHALL NOT |
| is not permitted | exact | SHALL NOT |
| is not allowed | exact | SHALL NOT |
| is not acceptable | exact | SHALL NOT |
| is unacceptable | exact | SHALL NOT |
| is not to | exact | SHALL NOT |
| is preferred | exact | SHOULD |
| is recommended | exact | SHOULD |
| is advised | exact | SHOULD |
| is encouraged | exact | SHOULD |
| ought to | exact | SHOULD |
| prefer | review | SHOULD |
| is discouraged | exact | SHOULD NOT |
| avoid | review | SHOULD NOT |
| is permitted | exact | MAY |
| is allowed | exact | MAY |
| is free to | exact | MAY |
| is exempt from | exact | MAY |
| need not | exact | MAY |
| needs no | exact | MAY |
| will | review | SHALL |
| is to | review | SHALL |
| consider | review | SHOULD |
| cannot | review | SHALL NOT |
| can | review | MAY |
| could | review | MAY |

#### STND.DRAFT.8 Reading of excluded expressions

Binding. Instantiates LVL0#normative-language.

A provision that uses an excluded expression SHALL be read with the force of the modal in the Read as column of the table of STND.DRAFT.7. The use SHALL be flagged for correction (LVL0#normative-language).

#### STND.DRAFT.9 Substitution test

Binding. Instantiates LVL0#normative-language.

Where replacing an expression of class review in the table of STND.DRAFT.7 with the modal in its Read as column preserves the meaning of its sentence, the expression SHALL be treated as excluded. Where the replacement changes the meaning, the expression SHALL NOT be treated as excluded (LVL0#normative-language).

#### STND.DRAFT.10 Imperative mood

Default. Instantiates INTPR.12.

A sentence of a document SHALL NOT be written in the imperative mood (INTPR.12).

#### STND.DRAFT.11 Fill-in guidance

Default. Instantiates INTPR.12.

Text that guides the person completing a template SHALL begin with the label "Fill-in guidance:". An instantiated instrument SHALL NOT contain that label (INTPR.12).

#### STND.DRAFT.12 Informative text

Default. Instantiates INTPR.12.

Explanations, notes, and examples SHALL be placed in the informative parts of a document. They SHALL NOT appear in the body of a numbered provision (INTPR.12).

### Precision

#### STND.DRAFT.13 Vague qualifiers

Default. Instantiates INTPR.12.

A sentence that uses a qualifier of class review in the table of this provision SHALL state its criterion or name the decider and the record of the decision. A numbered provision SHALL NOT use a qualifier of class exact in the table of this provision (INTPR.12).

| Qualifier | Class |
| --- | --- |
| etc. | exact |
| and so on | exact |
| and/or | exact |
| best effort | exact |
| appropriate | review |
| adequate | review |
| reasonable | review |
| suitable | review |
| sufficient | review |
| as needed | review |
| as necessary | review |
| as applicable | review |
| where possible | review |
| if possible | review |
| where practical | review |
| as far as possible | review |
| to the extent | review |
| significant | review |
| periodically | review |
| best practice | review |

#### STND.DRAFT.14 Disjunction

Default. Instantiates INTPR.12.

The word "or" in a provision SHALL be read as inclusive. A choice of exactly one alternative SHALL be written with the words "exactly one of" (INTPR.12).

#### STND.DRAFT.15 Negated lists

Default. Instantiates INTPR.12.

A prohibition on more than one item SHALL be written as one sentence for each item (INTPR.12).

#### STND.DRAFT.16 Conditions

Default. Instantiates INTPR.12.

A condition SHALL precede the clause it governs. A sentence SHALL carry at most one condition (INTPR.12).

#### STND.DRAFT.17 Quantifiers

Default. Instantiates INTPR.12.

A provision SHALL NOT use a word of the table of this provision (INTPR.12).

| Word | Replace with |
| --- | --- |
| any | "every" or "at least one" |
| some | "at least one" |
| several | a stated number |
| various | the named items |
| many | a stated number |
| few | a stated number |
| numerous | a stated number |

#### STND.DRAFT.18 Numeric limits

Default. Instantiates INTPR.12.

A numeric limit SHALL state its unit and whether its bound is inclusive (INTPR.12).

### Citation

#### STND.DRAFT.19 Instantiated provisions

Binding. Instantiates PRIME.15.

A provision below LVL0 SHALL list each higher provision that it instantiates, including its LVL0 ancestor (PRIME.15).

#### STND.DRAFT.20 Citation form

Binding. Instantiates PRIME.15.

A citation SHALL name exactly one provision by its full stable identifier, or exactly one section by its locator (PRIME.15).

#### STND.DRAFT.21 Citation by position

Binding. Instantiates PRIME.15.

A citation SHALL NOT name a provision by its position (PRIME.15).

#### STND.DRAFT.22 Resolvable citations

Binding. Instantiates PRIME.15.

A citation SHALL resolve to a provision or a section of the corpus (PRIME.15).

#### STND.DRAFT.23 Citation fit

Binding. Instantiates PRIME.15.

A provision SHALL list as instantiated only a higher provision that it makes more specific without relaxing it (PRIME.15).

#### STND.DRAFT.24 Listed identifiers

Default. Instantiates INTPR.3.

The identifiers and locators in the text of a provision SHALL be exactly those that it lists as instantiated or as referred to (INTPR.3).

#### STND.DRAFT.25 Binding reason

Binding. Instantiates GOV.19.

A provision marked binding that instantiates no prime directive, no provision of GUARD, and no floor obligation SHALL record why uniformity across projects requires it (GOV.19).

#### STND.DRAFT.34 References table

Binding. Instantiates PRIME.15.

Each document below LVL0 SHALL hold, before its revision history, a section References whose table gives the identifier and title of each cited document (PRIME.15).

### Structure

#### STND.DRAFT.26 Title form

Default. Instantiates INTPR.12.

The title of a numbered provision SHALL be a noun phrase of at most six words (INTPR.12).

#### STND.DRAFT.27 Distinct titles

Default. Instantiates INTPR.12.

The title of a numbered provision SHALL differ from the title of every other provision of the corpus (INTPR.12).

#### STND.DRAFT.28 Atomic provision

Default. Instantiates INTPR.12.

A numbered provision SHALL state one obligation, prohibition, recommendation, or permission, or a bundle of at most three whose parts are never applied apart (INTPR.12).

### Roles and terms

#### STND.DRAFT.29 Role names

Default. Instantiates INTPR.12.

A provision SHALL name an actor by a role that the Lexicon or the Terms section of its document defines. A provision SHALL NOT use a word of class retired in the table of this provision, except in a compound that the table allows (INTPR.12).

| Word | Class | Replace with | Allowed compounds |
| --- | --- | --- | --- |
| user | retired | human owner, operator, relying party, or actor | user space, user-defined, user mode |
| registry | retired | register, ledger, manifest, index, or record | none |
| administrator | undefined | a defined role | none |
| client | undefined | a defined role | none |
| contributor | undefined | a defined role | none |
| customer | undefined | a defined role | none |
| developer | undefined | a defined role | none |
| engineer | undefined | a defined role | none |
| maintainer | undefined | a defined role | none |
| manager | undefined | a defined role | none |
| programmer | undefined | a defined role | none |
| stakeholder | undefined | a defined role | none |
| team | undefined | a defined role | none |

#### STND.DRAFT.30 Defined terms

Default. Instantiates INTPR.12.

A term that a document defines SHALL be defined once, in the Terms section of that document (INTPR.12).

#### STND.DRAFT.31 Lexicon terms

Binding. Instantiates LEX.

A document SHALL NOT define a term that the Lexicon defines (LEX).

### Style

#### STND.DRAFT.32 Person and contractions

Default. Instantiates INTPR.12.

A provision SHALL be written in the third person and without contractions (INTPR.12).

| Word | Replace with |
| --- | --- |
| I | the named role |
| me | the named role |
| my | the named role |
| we | the named role |
| us | the named role |
| our | the named role |
| you | the named role |
| your | the named role |

#### STND.DRAFT.33 Spelling

Default. Instantiates INTPR.12.

A provision SHALL use American spelling (INTPR.12).

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

### Profiles

#### STND.DRAFT.35 Selector attributes

Binding. Instantiates GOV.24, GOV.26.

A profile or sub-profile SHALL define in its Terms section each attribute it introduces, with the test by which a classification decides the attribute's value (GOV.24, GOV.26). A profile or sub-profile SHALL state its selector in a numbered provision that either holds a table named selector, with the columns Attribute and Defined by, giving each attribute the selector tests and the document that defines it, or states that the selector is true for every classification (GOV.26). Where a selector tests an attribute, the selector SHALL take the value true for a classification that makes at least one attribute of its selector table true, and the value false for every other classification (GOV.26).

#### STND.DRAFT.36 Sub-profile attributes

Binding. Instantiates GOV.27.

The selector table of a profile SHALL give each attribute that the selector table of one of its sub-profiles gives (GOV.27).

#### STND.DRAFT.37 Domain-item subjects

Binding. Instantiates GOV.25, GOV.26.

Where a provision of a profile or sub-profile governs a domain item, the provision SHALL name that domain item as its subject (GOV.25, GOV.26). Where a provision of a profile or sub-profile governs the whole work, the provision SHALL name the work as its subject (GOV.25, GOV.26).

#### STND.DRAFT.38 Execution-path subjects

Binding. Instantiates GOV.25, GOV.27.

Where a provision of the execution hardware profile (HW) or of one of its sub-profiles governs execution on a hardware type, the provision SHALL name an execution path on that type as its subject (GOV.25, GOV.27).

#### STND.DRAFT.39 Shared-matters table

Binding. Instantiates GOV.26, GOV.31.

Where a profile or sub-profile owns a shared matter or addresses one that another profile owns, it SHALL state, in a numbered provision holding a table named shared-matters with the columns Matter, Owning profile, and Provisions, each such matter, by the name that the owning profile's shared-matters table gives it, its owning profile, and the provisions of the document that address it (GOV.26). Where a provision addresses a shared matter that another profile owns, the provision SHALL cite each adopted provision of the owning profile on which it builds (GOV.26, GOV.31). A shared matter SHALL NOT have more than one owning profile (GOV.26).

#### STND.DRAFT.40 Boundary obligations

Binding. Instantiates GOV.26.

Where a domain item of one profile is an input to a domain item of another profile, the profile of the domain item that takes the input SHALL state each obligation that this domain item places on that input (GOV.26). A provision that states such an obligation SHALL cite each adopted provision of the profile of the input on which it relies (GOV.26).

#### STND.DRAFT.41 Evidence by content

Binding. Instantiates GOV.11, GOV.26.

Where a provision of a profile or sub-profile requires evidence, the provision SHALL state the content that the evidence carries (GOV.11, GOV.26). Where no provision that it instantiates requires the separation, a provision of a profile or sub-profile SHALL NOT require that its evidence be kept apart from evidence that another profile requires (GOV.11).

### Human owner decisions

#### STND.DRAFT.42 Human owner decisions

Binding. Instantiates GOV.11, GOV.50, GUARD.11, PRIME.14, GUARD.3.

A provision at LVL1 or LVL2 SHALL NOT require a decision of the human owner other than an assigned decision (GOV.11, GOV.50). Where a provision at LVL1 or LVL2 rests on an authorization that LVL0 lets a standing authorization give, the provision SHALL accept a standing authorization (GUARD.11). A provision at LVL1 or LVL2 that requires a referral SHALL halt only the line of work that the referral concerns (PRIME.14, GUARD.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-09 | Adopted. |
| 1.0.1 | 2026-10-09 | Editorial amendment (GOV.41): each of the 33 provisions carries the status adopted and the adoption date of the standard, which the adoption of revision 1.0 left at draft; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-10 | Editorial amendment (GOV.41): the table of STND.DRAFT.29 no longer lists reviewer as an undefined role word, because LVL0 revision 1.3 defines Reviewer in the Lexicon; no obligation changes. |
| 1.0.3 | 2026-10-10 | Editorial amendment (GOV.41): the table of STND.DRAFT.29 lists its undefined role words in alphabetical order after the retired words, and gives their replacement as a defined role, which the first sentence of the provision already explains; no obligation changes. |
| 1.1 | 2026-10-10 | Minor amendment (GOV.41): the term Locator takes its form from STND.IDENT.15 and its slug from STND.IDENT.16, which replaces each run of characters other than the letters a to z and the digits 0 to 9 with one hyphen; the slug of a heading with punctuation changes. |
| 1.2 | 2026-10-10 | Minor amendment (GOV.41): new STND.DRAFT.34 requires each document below LVL0 to hold a section References that lists, by identifier and title, each document it cites; the Terms define Cited document; check g.25 enforces the table. |
| 1.2.1 | 2026-10-10 | Editorial amendment (GOV.41): the Checks section names the commands of the harness package instead of the retired scripts; no obligation changes. |
| 1.3 | 2026-10-11 | Minor amendment (GOV.41): new section Profiles, STND.DRAFT.35 to STND.DRAFT.41, fixes selector attributes and their coverage of sub-profiles, the subjects of profile provisions (domain items, and execution paths for HW), the allocation of shared matters to one owning profile, obligations at the boundary between domains, and evidence stated by content; the Terms define Attribute, Domain item, Execution path, Owning profile, Shared matter, Subject, Assigned decision, and Decision of the human owner; new section Human owner decisions, STND.DRAFT.42, bars profiles and LVL2 standards from asking the human owner for a decision that LVL0 neither requires nor reserves, has them accept standing authorizations wherever LVL0 permits, and limits each referral's halt to the line of work it concerns. |
| 1.4 | 2026-10-18 | Minor amendment (GOV.41), conforming on the adoption of HW: the term Execution path takes the definition that HW gives, which adds the hardware models, firmware, drivers, runtime libraries, and settings that a path admits, by reference to HW. |
| 1.5 | 2026-10-26 | Minor amendment (GOV.41): the term Cited document also covers a document named in the text by its identifier alone, outside quotation marks, code spans, tables with a column headed Example, the section References, and the revision history, and never by the identifier LVL0 alone; new term Sentence; STND.DRAFT.3 asks for no quotation marks in a column whose entries are modals or excluded expressions; STND.DRAFT.22 names v.8 among its checks; the section Checks says that a finding in another document fails where a binding provision of this standard names the check, and that a document named by its identifier alone has its row derived, so that g.25 fails where the table lacks it. Transition (GOV.42): none. |
