---
id: "STND.HARN"
level: "LVL2"
kind: "standard"
title: "Harness specification"
status: "adopted"
adopted: "2026-10-10"
revision: "1.2"
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

Assured work, checkpoint, destructive action, session, signer register, and working bounds have the meanings of STND.DFLT. Attribute, owning profile, and shared matter have the meanings they have in the drafting standard (STND.DRAFT). The checks of section Profile combination find what is mechanical; whether two listed provisions conflict is decided in review, because provisions are prose. An agent of a different agent configuration from the author performs that review (QA.8), and the adopter sees only its summary. Work report has the meaning it has in the agent practice profile (AGENT). Two provisions conflict where, for one classification and one consequence class, both apply to one domain item and one requires, permits, or recommends what the other prohibits. A conflict found in use is resolved meanwhile under GOV.25, GOV.5, and GOV.6: the more restrictive governs, an agent halts and refers (PRIME.14), and the concession is recorded; the human owner rules (GOV.3), and the project reports the conflict to the custodians (GOV.47) as a defect under GOV.26. The anchor file defaults to "/etc/governance/signer.json". The code accepts type configure on adoption. STND.DRAFT and STND.IDENT name the commands of the harness package that report their checks, among them the revision checks, which read the revision history of each adopted document (STND.IDENT.6).

STND.HARN.29 states when a derived configuration relies on an authorization under the row remote-write of STND.HARN.18; its two sentences are a bundle that is never applied apart. Its rows are tested when the configuration is derived, and the expiry again at each write, because the configuration is installed where the agent is unable to alter it and reads no ledger. A revocation therefore reaches a configuration only when the configuration is derived again and installed; until then, a derivation that still names the revoked authorization stops with the reason, one that no longer names it differs from the installed configuration, which the check of STND.HARN.21 reports, and the coverage report of STND.HARN.19 states the interval. An authorization per action is never relied on: a configuration that lets one write pass is unable to tell that write from a repetition of it, so the write is referred and the human owner's answer to the referral confirms it (PRIME.7, PRIME.14). A standing authorization of an irrevocable remote write has no effect (GUARD.11), and STND.HARN.29 relies on none. GUARD.11 voids only the irrevocable write, so the row Standing is tested for each entry and kind of write: an irrevocable one opens nothing and its writes are referred, and the other entries of the same authorization stand. A malformed entry fails the row Form, and nothing of that authorization is relied on, because the record then does not state what the human owner granted. The row Extension applies GUARD.12: an authorization reaches a directed agent only where it says so, and a configuration is derived for one role or agent. The row Record is narrower than STND.DFLT.23, which for work that is not assured also accepts an agent's own entry of a grant (STND.DFLT.17): an agent is able to append such an entry, so a configuration that relied on it would let an agent open its own writes (PRIME.7), and the write is referred instead, which STND.HARN.18 allows. The row Signature asks for a signature wherever a signer register exists, since an unsigned entry is then one that anyone with write access to the ledger is able to make. Whole values are compared because a pattern, or a comparison of a prefix, admits a destination that the human owner never named; a write whose destination a configuration is unable to read from the action itself is referred. A configuration that refers a write which an authorization in force names still meets STND.HARN.18, and its coverage report states each kind of write that it refers so (STND.HARN.19). STND.HARN.29 binds, because it instantiates GOV.48, GUARD.2, GUARD.11, and GUARD.12, and raises no floor (GOV.11): it asks of a harness only the reliance on an authorization as the record states it, entry by entry, which GUARD.2 and GUARD.11 already ask of an agent, at the cost of wording and of the checks the harness makes: reading each named authorization file and the ledger that pins it, verifying signatures where they are required, and comparing each remote write with the authorizations relied on.

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
| STND.IDENT | Identifier scheme and mnemonic register |
| STND.INSTR | Agent instructions |
| STND.PROJ | Project constitution template |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-10 | Adopted. |
| 1.1 | 2026-10-11 | Minor amendment (GOV.41): new section Profile combination, STND.HARN.26 to STND.HARN.28: FAIL for an undefined selector attribute, for a shared matter with more than one owning profile, and for an uncited owning profile, and a list of provision pairs for review before each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0, with a verdict recorded for each pair and a summary of conflicts only for the adopter; STND.HARN.18 refers a remote write unless an authorization in force names its destination and kind of write, and STND.HARN.23 reports a configuration failure through the agent's work report (STND.DRAFT.42). Transition (GOV.42): until the harness implements STND.HARN.26 to STND.HARN.28, the QA.7 review of each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0 checks selector attributes and shared matters, and lists the pairs of STND.HARN.28, by reading. |
| 1.2 | 2026-10-24 | Minor amendment (GOV.41): new STND.HARN.29: a derived configuration that lets a remote write proceed without referral under STND.HARN.18 relies only on a standing authorization in the form of STND.PROJ.6 that, when the configuration is derived, is adopted, granted by the human owner, extends to the role or agent the configuration is derived for (GUARD.12), is pinned in its current content by an authorize transaction of the human owner in an intact ledger and revoked by no later transaction, is signed where the work is assured or a signer register exists, was recorded no later than its transaction and than the derivation, and whose expiry, where it has one, is later than the write; an entry of a kind that STND.PROJ.7 marks irrevocable at its destination opens nothing (GUARD.11), each entry and kind tested apart, so that the other entries of the authorization stand; destination, kind, and branches are compared as whole values; the Notes cite STND.IDENT.6 in place of a stale sentence on scripts; the transition of ledger entry 53 for STND.HARN.18 ends once a reviewed harness that implements STND.HARN.29 is installed. |
