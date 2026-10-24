---
id: "STND.HARN"
level: "LVL2"
kind: "standard"
title: "Harness specification"
status: "adopted"
adopted: "2026-10-10"
revision: "1.1"
adopted_by: "The Custodian"
instantiates: ["GOV.26", "GOV.35", "GOV.36", "GOV.37", "GOV.38", "GOV.39", "GOV.48", "QA.7"]
rank: null
waivable: false
---

## Purpose and scope

A harness serves governance read-only: it fetches what applies and checks conformance. No work depends on it (GOV.38).

## Terms

| Term | Definition |
| --- | --- |
| Accepted signature | A valid signature over a transaction's entry digest by a key whose row among signers has Ledger its ledger or "all", Role label its actor, and Last entry "none" or at least its "seq". |
| Anchor file | A file outside the corpus, unalterable by the checking account, naming the founding key of the signer register. |
| Content hash | The digest of the UTF-8 lines "path:digest", one per ".md" file under a "scope", with "/"-separated paths from the corpus root, ordered by scope path, then part by part in code-point order, joined by line feeds without a final one. |
| Derived configuration | An agent's environment configuration that a harness derives. |
| Digest | The lowercase hexadecimal SHA-256 of a byte sequence. |
| Entry digest | The entry hash of a transaction with an empty "signature". |
| Entry hash | The digest of a transaction without its "hash", serialized as STND.HARN.6 requires. |
| FAIL | A check's report that its property is violated. |
| Item | A document, register, provision, knowledge entry, Lexicon term, or tag. |
| Refer | The response that holds an action until the human owner decides it. |
| Rehearsal | A script run on a fresh corpus copy, then the checks of that copy. |
| Template directory | A directory whose name begins with "_", or one under it. |
| Timestamp | An ISO 8601 time with its UTC offset. |

## Notes

Assured work, checkpoint, destructive action, session, signer register, and working bounds have the meanings of STND.DFLT. Attribute, owning profile, and shared matter have the meanings they have in the drafting standard (STND.DRAFT). The checks of section Profile combination find what is mechanical; whether two listed provisions conflict is decided in review, because provisions are prose. An agent of a different agent configuration from the author performs that review (QA.8), and the adopter sees only its summary. Work report has the meaning it has in the agent practice profile (AGENT). Two provisions conflict where, for one classification and one consequence class, both apply to one domain item and one requires, permits, or recommends what the other prohibits. A conflict found in use is resolved meanwhile under GOV.25, GOV.5, and GOV.6: the more restrictive governs, an agent halts and refers (PRIME.14), and the concession is recorded; the human owner rules (GOV.3), and the project reports the conflict to the custodians (GOV.47) as a defect under GOV.26. The anchor file defaults to "/etc/governance/signer.json". The code accepts type configure on adoption. Scripts named in STND.DRAFT and STND.IDENT stay entry points until those standards cite `python -m govharness` (GOV.42).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| GOV | Governance |
| GUARD | Safeguards |
| PRIME | Prime Directives |
| QA | Process |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.INSTR | Agent instructions |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-10 | Adopted. |
| 1.1 | 2026-10-11 | Minor amendment (GOV.41): new section Profile combination, STND.HARN.26 to STND.HARN.28: FAIL for an undefined selector attribute, for a shared matter with more than one owning profile, and for an uncited owning profile, and a list of provision pairs for review before each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0, with a verdict recorded for each pair and a summary of conflicts only for the adopter; STND.HARN.18 refers a remote write unless an authorization in force names its destination and kind of write, and STND.HARN.23 reports a configuration failure through the agent's work report (STND.DRAFT.42). Transition (GOV.42): until the harness implements STND.HARN.26 to STND.HARN.28, the QA.7 review of each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0 checks selector attributes and shared matters, and lists the pairs of STND.HARN.28, by reading. |
