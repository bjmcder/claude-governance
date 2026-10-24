# Constitution for Computational and Cyber-Physical Systems (LVL0) 1.6

Adopted as revision 1.0 in ledger entry 1 (2026-10-08); revised to 1.0.1 in entry 2 (2026-10-09), 1.0.2 in entry 3 (2026-10-09), 1.0.3 in entry 4 (2026-10-09), 1.1 in entry 5 (2026-10-09), 1.2 in entry 6 (2026-10-09), 1.2.1 in entry 7 (2026-10-09), 1.3 in entry 17 (2026-10-09), 1.4 in entry 23 (2026-10-10), 1.5 in entry 30 (2026-10-10), and 1.6 in entry 46 (2026-10-11). This reading copy is composed from the per-provision files in LVL0/ of the governance harness; the harness files are the system of record.

## Preamble

This constitution states the principles for conceiving, building, verifying, operating, and retiring computational and cyber-physical systems whose outputs or actions are relied upon. Such systems are software, workflows, and the hardware they drive, read, or execute on, where a computation, a measurement, or an action on the physical world bears on a result, a decision, or safety. This document binds such systems whatever their purpose, whatever problem they pose, and whatever hardware runs them. General business and web software are outside its scope until a profile brings them in (GOV.30).

This constitution governs how such systems are built, verified, operated, and maintained. It does not govern the choice or merit of the questions they serve, the ethics of the purposes to which they are applied, publication, authorship, or credit, law and regulation (including data protection, export control, and licensing), or personnel and organizational matters, including who serve as human owners or custodians and how they are appointed, qualified, or succeeded, and whether any decision requires the concurrence of a person other than the human owner. Where those impose obligations on a system, parallel governance outside this document carries them.

The principles are meant to outlive any language, library, tool, technology, platform, process, or method. No provision requires one or is satisfied only by adopting one; a provision demands an outcome, and the implementer chooses the least costly means to it. Every obligation is written so that a human skilled in the art is able to meet it, and judge compliance, without any particular automation. When automation fails, the work remains understandable and resumable by a human (INTPR.12).

This constitution is LVL0, the root of a four-level structure (GOV.16). It holds the Governing Principles (PRIN); fifteen prime directives (PRIME) that bind at every consequence class and are never waived; the General Articles, whose obligations other than the safeguards are proportioned to consequence class; and the Governance Article (GOV), which sets authority, precedence, consequence classes, derivation, profiles, knowledge, governance records, and change. Domain obligations are held in LVL1 profiles, which bind a project when its classification selects them. All lower governance derives from this document under PRIME.15. Every normative word carries the meaning fixed in Normative Language, and every defined term the meaning fixed in the Lexicon, here and at every lower level.

## Normative Language

This document capitalizes normative words (SHALL, SHALL NOT, NEVER, SHOULD, SHOULD NOT, MAY). Capitalization marks a word as normative and does not change its meaning; lowercase forms in the table carry the same force.

Normative force attaches to the bodies of the Governing Principles and of numbered provisions. This section and the Lexicon fix meanings and bind wherever their words and terms are used; a Lexicon definition is normative as to meaning and imposes no obligation. Otherwise the Preamble, Article and section opening paragraphs, and provision titles are informative, except a sentence among them that uses a capitalized normative word.

An expression not in the table carries no normative force. For example, "may not" is ambiguous between a prohibition and an absence of permission; it is NEVER used, and SHALL NOT is written instead. At every lower level, an imperative sentence carries the force of SHALL. A drafting standard at LVL2 governs how normative words are written below LVL0 and which further confounding expressions are excluded. A lower provision that uses an excluded expression is read as the strictest word in the table that fits it and flagged for correction; it NEVER loses force.

| Word or phrase | Meaning | Effect of non-compliance |
| --- | --- | --- |
| shall, must, is required, is (as a statement of obligation) | Mandatory. Every present-tense indicative sentence in a normative part of this document that states what an actor or artifact does or is, singular or plural, is normative. | A defect; relieved only by waiver (GOV.44) or amendment (GOV.40). |
| shall not, shall never, never, is prohibited | Mandatory prohibition. | A defect; not waivable where GOV.45 says so. |
| should, is preferred | Strongly recommended. | Permitted when the deviation and its reason are recorded (PRIN.10). |
| should not | Strongly recommended against. | Permitted when the deviation and its reason are recorded (PRIN.10). |
| may | Permitted at the implementer's discretion. | None. |
| is exempt, is free, is permitted, need not, needs no | Permission or exemption; states no obligation. | None. |
| is a defect | A nonconformance; blocking where it affects a reported result, a release, a deployment to hardware, or a safety property, tracked otherwise. | A blocking defect blocks release, reporting, or deployment of what it affects until resolved; a tracked defect is recorded in defect tracking (QA.4) and resolved on a recorded schedule. |
| is incomplete | The artifact may exist but shall not be reported, released, or relied upon until completed. | Reporting it is a blocking defect under the provision that declares it incomplete. |
| is unverified | A mandatory label on any result lacking the evidence VV requires. | Omitting the label is a defect under PRIME.3. |
| is a correctness failure | Treated under VV, never as a performance shortfall or a style matter. | The precedence of VV applies (GOV.5). |
| is excess, is accidental | Complexity that is removed unless justified in a decision record (REPRO.7). | A defect under SIMPL. |
| has no authority, is void | A lower provision that does not bind and is corrected or removed. | Compliance with it is not required; conflict with a higher provision is resolved in the higher provision's favor (GOV.1, PRIME.15). |
| recorded | Written in a durable, versioned, discoverable form that travels with the artifact it concerns (REPRO). | An unmet obligation to record is a defect under REPRO. |
| stated, explicit | Written down where a reader of the artifact concerned is able to find it. | An unmet obligation to state is a defect under the provision that requires it. |
| declared | Written in the artifact its reader passes through (code, interface, schema, specification, output, or report), not only in a separate document. | Implicitness where a provision requires declaration is a defect. |
| reported, released, deployed | Communicated or used beyond its author as a result to be relied upon; or placed into use on hardware beyond development. A result SHALL NOT be reported before promotion (QA.11). | VV and REPRO apply at the level the consequence class sets (GOV.11); reporting an unpromoted result, or relying on one beyond its author, is a blocking defect (QA.11). |

**Identifiers.** Every provision carries a stable identifier: the mnemonic of its document or Article, a dot, and a number (PRIME.6, VV.3, GOV.12). Lower levels extend the same scheme with further dot-separated segments (GOV.37). An identifier is NEVER reused or renumbered, and the order in which provisions appear carries no rank (GOV.5). The LVL0 mnemonics are PRIN, PRIME, GUARD, VV, REPRO, INTPR, DSGN, SIMPL, RSRC, QA, and GOV.

## Provisions

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-08 | Ratified. |
| 1.0.1 | 2026-10-09 | Editorial amendment (GOV.40): LEX.index states in descriptive words, not with a capitalized normative word, that an index is not authoritative; no obligation changes. |
| 1.0.2 | 2026-10-09 | Editorial amendment (GOV.40): the Lexicon defines three roles that provisions already use, Author (REPRO.5, QA.7, GOV.34), Adopter (GOV.41, GOV.42, GOV.46, GOV.49), and Auditor (QA.2, GOV.47); no obligation changes. |
| 1.0.3 | 2026-10-09 | Editorial amendment (GOV.40): the ratification record names the role that ratified the constitution, The Custodian, in place of a blank; no obligation changes. |
| 1.1 | 2026-10-09 | Minor amendment (GOV.40): Normative Language lists SHOULD NOT and its lowercase form should not beside SHOULD, so that every normative word is fixed in one place; DSGN.13 already used SHOULD NOT with this meaning. |
| 1.2 | 2026-10-09 | Minor amendment (GOV.40): LVL0 conforms to the drafting standard, STND.DRAFT. Forty-two edits across forty provisions replace excluded expressions (prohibited, permitted, ought to, need not, has to, required) with table words, replace the review-class words could and considered, and replace the quantifier any where a plainer word is available. GUARD.18 now names who records what is practical: the human owner. No other obligation changes. |
| 1.2.1 | 2026-10-09 | Editorial amendment (GOV.40): four phrasings introduced in 1.2 (GOV.13, GUARD.12, PRIME.13, QA.3) read at will, and the drafting standard reads will as SHALL; they now read throughout the project's life or whenever the actor chooses; no obligation changes. |
| 1.3 | 2026-10-09 | Minor amendment (GOV.40): the Lexicon defines the roles Reviewer and Standards owner; Promotion makes a result reportable at the level of obligations its proportionality judgment sets, not at an evidence level; Amendment covers every adopted governance document; Auditor covers compliance audits; Normative Language lists NEVER, which LVL0 uses, in place of SHALL NEVER, which it no longer uses. |
| 1.4 | 2026-10-10 | Minor amendment (GOV.40): the Lexicon entry Review keeps its meaning for a change and states that the word carries its ordinary meaning of a re-examination where it is applied to anything else, as in GOV.4, GOV.42, GOV.46, GUARD.16, VV.9, and REPRO.9. |
| 1.5 | 2026-10-10 | Minor amendment (GOV.40): GUARD.7 adds a third ground of exemption, the removal or overwriting of temporary items only; the Lexicon defines Temporary item, and Irrecoverable action excludes an action of an exempt class, so that PRIME.6 no longer reserves an exempt action; GUARD.6 still prevails over every exemption. |
| 1.6 | 2026-10-11 | Minor amendment (GOV.40): GOV.18 reserves to LVL3 any limit, beyond those of LVL0, on the number of agents an agent directs, the depth of delegation, and network access made to retrieve information for research. |
