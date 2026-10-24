---
id: "STND.DRAFT"
level: "LVL2"
kind: "standard"
title: "Drafting standard"
status: "adopted"
revision: "1.4"
adopted: "2026-10-09"
adopted_by: "The Custodian"
instantiates: ["LVL0#normative-language", "LEX.drafting-standard", "GOV.11", "GOV.24", "GOV.25", "GOV.26", "GOV.27", "GOV.31", "GOV.50", "GUARD.11"]
rank: null
waivable: false
---

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
| Cited document | A document other than the citing one, named, itself or through one of its provisions, terms, or locators, in a citation or a reference field of the citing document or of its provisions. |

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

The harness reports the lineage checks (family l) and the drafting checks (family g) with `python -m govharness check`. A finding in this standard fails. A finding in another document fails when this standard is adopted and the provision concerned is binding, and warns otherwise. Findings in LVL0 and in documents not yet divided into numbered provisions form an advisory punch list and never fail, because this standard governs below LVL0 and numbered provisions. The check g.25 compares each references table with the cited documents that `python -m govharness references` derives from the corpus and writes.

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
