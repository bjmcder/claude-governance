# Harness specification (STND.HARN) 1.3

Adopted by The Custodian as revision 1.0 in ledger entry 43 (2026-10-10); revised to 1.1 in entry 53 (2026-10-11), 1.2 in entry 141 (2026-10-24), and 1.3 in entry 175 (2026-10-25). This reading copy is composed from the per-provision files in STND/HARN/ of the governance harness; the harness files are the system of record.

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

STND.HARN.29 states when a derived configuration relies on an authorization under the row remote-write of STND.HARN.18; its two sentences are a bundle that is never applied apart. Its rows are tested when the configuration is derived, and the expiry again at each write, because the configuration is installed where the agent is unable to alter it and reads no ledger. A revocation therefore reaches a configuration only when the configuration is derived again and installed; until then, a derivation that still names the revoked authorization stops with the reason, one that no longer names it differs from the installed configuration, which the check of STND.HARN.21 reports, and the coverage report of STND.HARN.19 states the interval. Only an expiry bounds that interval, since the row Dates tests it again at each write, and an authorization that lapses only when revoked leaves the interval unbounded. A harness that refuses at the derivation an authorization whose expiry lies beyond a horizon that the harness states, or that lapses only when revoked, still meets STND.HARN.29, because it then derives no configuration that relies on that authorization, and a configuration that refers the writes of an authorization meets STND.HARN.18. An authorization per action is never relied on: a configuration that lets one write pass is unable to tell that write from a repetition of it, so the write is referred and the human owner's answer to the referral confirms it (PRIME.7, PRIME.14). A standing authorization of an irrevocable remote write has no effect (GUARD.11), and STND.HARN.29 relies on none. GUARD.11 voids only the irrevocable write, so the row Standing is tested for each entry and kind of write: an irrevocable one opens nothing and its writes are referred, and the other entries of the same authorization stand. A malformed entry fails the row Form, and nothing of that authorization is relied on, because the record then does not state what the human owner granted. The row Extension applies GUARD.12: an authorization reaches a directed agent only where it says so, and a configuration is derived for one role or agent. The row Record is narrower than STND.DFLT.23, which for work that is not assured also accepts an agent's own entry of a grant (STND.DFLT.17): an agent is able to append such an entry, so a configuration that relied on it would let an agent open its own writes (PRIME.7), and the write is referred instead, which STND.HARN.18 allows. The row Signature asks for a signature wherever a signer register exists or existed, since an unsigned entry is then one that anyone with write access to the ledger is able to make. An entry that carries a signature, or whose scope lies at or under the directory of the register, shows that a register was founded, so a register that the ledger records and the corpus lacks was removed, and its absence lifts no signature. An entry whose form keeps a harness from reading those signs is able to hide them, so the row asks for a signature there as well. An agent that rewrites the ledger from its first entry on, with the chain recomputed, removes those signs too; the anchor file lies outside the agent's reach, so where an anchor file exists the signature stays required although the register is missing. Where none of these holds, an agent able to append to the ledger is able to append an unsigned authorize that names the human owner, although STND.DFLT.5 forbids it, and the row Record then does not show who granted the authorization. STND.HARN.30 therefore has a configuration rely on such an authorization only where the human owner accepts it unsigned at the derivation, after reading what it opens and before the configuration is installed where the agent is unable to alter it, and has the coverage report name it (PRIME.7, GUARD.10). The acceptance authenticates nothing, since an agent that runs a derivation is able to state it; it makes the reliance a stated act in place of a default, and a signer register removes the need for it. STND.HARN.30 is meant to require no decision of the human owner other than an assigned one (STND.DRAFT.42): without the acceptance, a harness derives no configuration that relies on the authorization, or one that refers its writes, and the acceptance, where the human owner gives it, is read as part of the grant that GUARD.10 reserves to the human owner, made once for each derivation and not for each write. Whole values are compared because a pattern, or a comparison of a prefix, admits a destination that the human owner never named; a write whose destination a configuration is unable to read from the action itself is referred. A configuration that refers a write which an authorization in force names still meets STND.HARN.18, and its coverage report states each kind of write that it refers so (STND.HARN.19). STND.HARN.29 binds, because it instantiates GOV.48, GUARD.2, GUARD.11, and GUARD.12, and raises no floor (GOV.11): it asks of a harness only the reliance on an authorization as the record states it, entry by entry, which GUARD.2 and GUARD.11 already ask of an agent, at the cost of wording and of the checks the harness makes: reading each named authorization file, the ledger that pins it, and the anchor file, verifying signatures where they are required, and comparing each remote write with the authorizations relied on. A configuration that refers every remote write meets STND.HARN.18, so each case in which the row Signature asks for a signature only narrows the writes that pass without referral. STND.HARN.30 binds, because it instantiates GUARD.10 and PRIME.7, and raises no floor (GOV.11). Relying on an authorization is never required, so a harness that never relies on one meets STND.HARN.30, and the human owner who withholds the acceptance bears only the referrals that STND.HARN.18 already makes. Where the human owner gives it, STND.HARN.30 asks of a harness a refusal and a line of its coverage report, at the cost of one acceptance for each derivation where no signer register is founded, in place of a referral of each write. STND.HARN.30 does not change what an agent accepts under STND.DFLT.23: it limits what a configuration relies on, and STND.HARN.18 lets a configuration refer the rest. STND.DFLT.5 forbids an agent to append an entry that names the human owner as actor, and nothing in the record shows that none did, so a configuration that relied on such an entry unaccepted would rest on the conduct of the agents that the configuration constrains (PRIME.7).

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

## Provisions

### Retrieval

#### STND.HARN.1 Item retrieval

Binding. Instantiates GOV.38.

Given an identifier or locator, a harness SHALL return what it names, with the identifier and title of each item it cites and of each provision, term, knowledge entry, and tag that cites it (GOV.38).

#### STND.HARN.2 Topic retrieval

Binding. Instantiates GOV.38.

Given words and a size, a harness SHALL return the best-matching items and sections within that size (GOV.38).

#### STND.HARN.3 Whole text

Binding. Instantiates GOV.39.

A harness SHALL return each text whole or by its identifier or locator alone (GOV.39).

### Corpus

#### STND.HARN.4 Item files

Binding. Instantiates GOV.35, GOV.37.

Each item SHALL be one UTF-8 file at its "id" with dots read as directory separators, plus "/_doc.md" for a document or register and ".md" otherwise. It SHALL open with its fields, one per line as name, colon, space, and JSON value, between two lines of "---", then its Markdown text (GOV.35, GOV.37).

#### STND.HARN.5 Files read as items

Binding. Instantiates GOV.35.

A harness SHALL read as items only ".md" files outside template directories, except "README.md" files (GOV.35).

### Ledger

#### STND.HARN.6 Ledger file

Binding. Instantiates GOV.36.

Each ledger SHALL be a UTF-8 file of one transaction per line, each a JSON object with sorted keys, no white space between tokens, and non-ASCII characters unescaped; the governance ledger is the root "ledger.jsonl" (GOV.36).

#### STND.HARN.7 Transaction fields

Binding. Instantiates GOV.36.

Each transaction SHALL hold exactly the fields "seq" (position, from one), "type" (adopt, amend, retire, classify, set-class, promote, authorize, revoke, register, waive, rule, declare-axiom, release, review, configure, or annotate), "actor" (role label or name), "role", "authority" (authorizing identifiers), "targets", "scope" (corpus directories whose content it pins), "rationale", "at" (timestamp), "corpus_hash" (content hash of a nonempty scope, or null), "prev" (previous entry hash, or null), "signature" (armored detached OpenPGP signature over the entry digest, or empty), "signers" (only on a governance-ledger transaction scoping the signer register: the keys the register then leaves open, by fingerprint), "ledger" (only outside the governance ledger: its identifier), and "hash" (entry hash) (GOV.36).

#### STND.HARN.8 Chain integrity

Binding. Instantiates GOV.36.

Where the "seq", "prev", or "hash" of a ledger transaction violates STND.HARN.7, a harness SHALL report FAIL. A harness SHALL NOT append to such a ledger (GOV.36).

#### STND.HARN.9 Content pin

Binding. Instantiates GOV.36.

Where the content hash of a "scope" differs from the "corpus_hash" of the latest governance-ledger transaction with that "scope", a harness SHALL report FAIL (GOV.36).

#### STND.HARN.10 Signer register form

Binding. Instantiates GOV.36.

The signer register SHALL hold a table of signers (Ledger, Role label, Name, Fingerprint, Last entry), a table of required signatures (Ledger, Actor, From entry), and each listed key, armored, under its fingerprint as heading. A row for "all" ledgers SHALL have Last entry "none" among signers and From entry "1" among required signatures (GOV.36).

#### STND.HARN.11 Signature acceptance

Binding. Instantiates GOV.36, GUARD.2.

Where a transaction that carries a signature, or that a row of required signatures names by ledger or "all", actor, and a From entry not above its "seq", lacks an accepted signature, a harness SHALL report FAIL (GOV.36, GUARD.2).

#### STND.HARN.12 Look-alike actors

Binding. Instantiates GOV.36, GUARD.2.

Where the signer register exists and a transaction's actor holds a non-ASCII character or equals a role label or actor of the register only after NFKC normalization, trimming, and case folding, a harness SHALL report FAIL (GOV.36, GUARD.2).

#### STND.HARN.13 Register chain

Binding. Instantiates GOV.36, GUARD.2.

Where a governance-ledger transaction scoping the signer register lacks an accepted signature by the anchor file's key, for the first, or by a key in the previous one's "signers", a harness SHALL report FAIL. Where the signer register exists without such a transaction, or the keys it leaves open differ from the last one's "signers", a harness SHALL report FAIL (GOV.36, GUARD.2).

### Checks

#### STND.HARN.14 Manifest form

Binding. Instantiates GOV.39.

Each corpus directory outside template directories SHALL hold a "MANIFEST.csv" with columns id, kind, level, title, status, path, sha256, and bytes, and one row per item and non-template subdirectory it holds (GOV.39).

#### STND.HARN.15 Stale content

Binding. Instantiates GOV.35, GOV.39.

A harness SHALL report each manifest, references table, and reading copy that differs from what it would generate (GOV.35, GOV.39).

#### STND.HARN.16 Stable check keys

Binding. Instantiates GOV.37.

A harness SHALL keep each check key fixed and unique across all checks, past and present (GOV.37).

#### STND.HARN.17 Failure status

Binding. Instantiates PRIME.4.

Where a check reports FAIL, the harness SHALL end its run with a nonzero exit status (PRIME.4).

### Environment

#### STND.HARN.18 Environment outcomes

Binding. Instantiates GOV.48.

Where a harness derives a configuration, it SHALL derive it from the outcomes and responses of the table of this provision (GOV.48).

| Key | Outcome | Source | Response |
| --- | --- | --- | --- |
| protected-locations | No location of STND.INSTR.3 is deleted, moved, or emptied | STND.INSTR.3 | Refuse |
| history-rewrite | No version-control history is rewritten or force-overwritten | PRIME.6 | Refuse |
| record-entries | No ledger or record entry is changed or removed | PRIME.5 | Refuse |
| elevated-privilege | No elevated privilege is used | PRIME.9 | Refuse |
| write-bounds | No write leaves the working bounds | STND.DFLT.25 | Refuse |
| read-bounds | No read leaves the working bounds | STND.DFLT.25 | Refer |
| network-bounds | No network request leaves the working bounds | STND.DFLT.25 | Refuse |
| remote-write | No remote write is made that no authorization in force names by destination and kind of write | PRIME.7, GUARD.11 | Refer |
| selective-destruction | No destructive action selects items by pattern, recursion, computation, or a value unknown beforehand | STND.DFLT.24 | Refer |
| enforcing-configuration | No agent alters this configuration | STND.DFLT.22 | Refuse |

#### STND.HARN.19 Coverage report

Binding. Instantiates GOV.48, GUARD.2.

A harness SHALL report how far each derived configuration enforces each outcome of STND.HARN.18: fully, partly with each gap, or not at all, with its conditions (GOV.48, GUARD.2).

#### STND.HARN.20 Configuration entry

Binding. Instantiates GOV.36, GUARD.2.

A "configure" entry that a harness drafts for STND.DFLT.22 SHALL name only the outcomes enforced fully. It SHALL name each installed file with its digest and each checkpoint mechanism of STND.DFLT.15 with its actions (GOV.36, GUARD.2).

#### STND.HARN.21 Installed configuration

Binding. Instantiates GUARD.2.

A harness SHALL report each installed file or program of a derived configuration that is missing, differs from its rendering, or is alterable by the harness's account (GUARD.2).

#### STND.HARN.22 Unattended referral

Binding. Instantiates GOV.48, PRIME.14.

In a session the human owner records as unattended, a derived configuration SHALL refuse each action that reaches a Refer outcome of STND.HARN.18 (GOV.48, PRIME.14).

#### STND.HARN.23 Configuration failure

Binding. Instantiates PRIME.4.

Where the work is assured, a derived configuration SHALL refuse each action for which a program it runs is missing or fails. Otherwise, it SHALL report the failure to the agent, which states it in its work report, and let the action proceed (PRIME.4).

#### STND.HARN.29 Authorizations a configuration honors

Binding. Instantiates GOV.48, GUARD.2, GUARD.11, GUARD.12.

Where a derived configuration lets a remote write proceed without referral under STND.HARN.18, it SHALL rely only on an authorization in an instrument file of the form of STND.PROJ.6 that meets each row of the table of this provision at the derivation of the configuration, and the row Dates also at the time of the write (GOV.48, GUARD.2, GUARD.11, GUARD.12). A derived configuration SHALL compare the destination, kind, and branches of a remote write with those that the authorization names as whole values, without patterns (GUARD.2).

| Test | The authorization meets it when |
| --- | --- |
| Status | Its status is adopted |
| Grantor | Its grantor is the human owner |
| Extension | Its field delegable_to names the role or agent for which the configuration is derived |
| Record | The chain of the ledger of the corpus that holds the file is intact; the latest transaction of that ledger whose scope holds the file is of type authorize, names the human owner as actor and the authorization among its targets, and pins the file's current content; and no later transaction of type revoke names it |
| Signature | Where the work is assured, the corpus holds a signer register, an entry of its ledger carries a signature or has a scope at or under the directory of the signer register, an entry of its ledger is not an object or has a scope that is not a list of paths or a signature that is not text, or an anchor file exists, the transaction of the row Record carries a signature that STND.HARN.11 accepts |
| Dates | Its date recorded is no later than that transaction and than the derivation, and its expiry, where it has one, is later than the write |
| Standing | It is standing, and the table of STND.PROJ.7 does not mark irrevocable the kind of the remote write at the destination of the entry that names it; each entry and kind is tested apart from the others |
| Form | Each field holds a value of the form that STND.PROJ.6 gives |

#### STND.HARN.30 Unsigned reliance accepted

Binding. Instantiates GUARD.10, PRIME.7.

Where the row Signature of STND.HARN.29 requires no signature, a derived configuration SHALL rely under STND.HARN.29 only on an authorization that the human owner accepts unsigned at the derivation of the configuration (GUARD.10, PRIME.7). Where a derived configuration relies on an authorization that the human owner accepted unsigned, the coverage report of that configuration SHALL name the authorization (STND.HARN.19).

### Rehearsal

#### STND.HARN.24 Rehearsal before application

Binding. Instantiates GOV.36.

Before applying a script that changes a corpus, an actor SHALL obtain a rehearsal of it in which no check reports FAIL (GOV.36).

#### STND.HARN.25 Rehearsal isolation

Binding. Instantiates GOV.36.

A harness SHALL report FAIL for a rehearsal that changes the source corpus (GOV.36).

### Profile combination

#### STND.HARN.26 Selector attribute check

Binding. Instantiates GOV.26.

A harness SHALL report FAIL for each attribute that the selector table of an adopted profile or sub-profile gives and that the document its Defined by column names does not define in its Terms section (GOV.26).

#### STND.HARN.27 Shared-matter ownership check

Binding. Instantiates GOV.26, GOV.31.

A harness SHALL report FAIL for each shared matter that the shared-matters tables of adopted documents give with more than one owning profile (GOV.26). A harness SHALL report FAIL for each provision that a shared-matters table gives for a matter that another adopted profile owns and that cites no provision of the owning profile (GOV.26, GOV.31).

#### STND.HARN.28 Conflict candidates

Binding. Instantiates GOV.26, QA.7.

Before each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0, a harness SHALL list for review each pair of provisions of different documents, at least one of them in a profile or sub-profile and at least one of them in the document changed or instantiating a LVL0 provision that the change amends, that the shared-matters tables give for one shared matter or that instantiate one LVL0 provision outside GOV and the Governing Principles (GOV.26). The record of the review of that adoption or amendment SHALL state, for each listed pair, whether the two provisions conflict and whether they address one matter that no shared-matters table gives, with the profile that is to own it (GOV.26, QA.7). The summary of that record given to the adopter SHALL hold only the pairs found to conflict and the matters left without an owning profile, and cite the full record (GOV.26).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-10 | Adopted. |
| 1.1 | 2026-10-11 | Minor amendment (GOV.41): new section Profile combination, STND.HARN.26 to STND.HARN.28: FAIL for an undefined selector attribute, for a shared matter with more than one owning profile, and for an uncited owning profile, and a list of provision pairs for review before each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0, with a verdict recorded for each pair and a summary of conflicts only for the adopter; STND.HARN.18 refers a remote write unless an authorization in force names its destination and kind of write, and STND.HARN.23 reports a configuration failure through the agent's work report (STND.DRAFT.42). Transition (GOV.42): until the harness implements STND.HARN.26 to STND.HARN.28, the QA.7 review of each adoption or amendment of a profile, a sub-profile, a LVL2 standard, or LVL0 checks selector attributes and shared matters, and lists the pairs of STND.HARN.28, by reading. |
| 1.2 | 2026-10-24 | Minor amendment (GOV.41): new STND.HARN.29: a derived configuration that lets a remote write proceed without referral under STND.HARN.18 relies only on a standing authorization in the form of STND.PROJ.6 that, when the configuration is derived, is adopted, granted by the human owner, extends to the role or agent the configuration is derived for (GUARD.12), is pinned in its current content by an authorize transaction of the human owner in an intact ledger and revoked by no later transaction, is signed where the work is assured or a signer register exists, was recorded no later than its transaction and than the derivation, and whose expiry, where it has one, is later than the write; an entry of a kind that STND.PROJ.7 marks irrevocable at its destination opens nothing (GUARD.11), each entry and kind tested apart, so that the other entries of the authorization stand; destination, kind, and branches are compared as whole values; the Notes cite STND.IDENT.6 in place of a stale sentence on scripts; the transition of ledger entry 53 for STND.HARN.18 ends once a reviewed harness that implements STND.HARN.29 is installed. |
| 1.3 | 2026-10-25 | Minor amendment (GOV.41): STND.HARN.29, row Signature: a signature is also required where an entry of the ledger carries a signature, has a scope at or under the directory of the signer register, or has a form that keeps those signs from being read, or where an anchor file exists, and the row names the transaction it tests as that of the row Record, where it said that transaction; new STND.HARN.30: where the row Signature requires no signature, a derived configuration relies under STND.HARN.29 only on an authorization that the human owner accepts unsigned at the derivation, and its coverage report names each one; the Notes give the reasons and the floor arguments, and state that only an expiry bounds the interval in which a configuration relies on a revoked authorization, and that a harness that refuses an expiry beyond a horizon it states still meets STND.HARN.29. Transition (GOV.42): none. |
