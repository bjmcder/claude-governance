# Harness specification (STND.HARN) 1.5

Adopted by The Custodian as revision 1.0 in ledger entry 43 (2026-10-10); revised to 1.1 in entry 53 (2026-10-11), 1.2 in entry 141 (2026-10-24), 1.3 in entry 175 (2026-10-25), 1.4 in entry 180 (2026-10-26), and 1.5 in entry 202 (2026-10-28). This reading copy is composed from the per-provision files in STND/HARN/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.HARN.18, STND.HARN.19, STND.HARN.20, STND.HARN.21, STND.HARN.22, STND.HARN.23, STND.HARN.29, and STND.HARN.30.

## Purpose and scope

A harness serves governance read-only: it fetches what applies and checks conformance. No work depends on it (GOV.38).

## Terms

| Term | Definition |
| --- | --- |
| Accepted signature | A valid signature over a transaction's entry digest by a key whose row among signers has Ledger its ledger, Role label its actor, and Last entry "none" or at least its "seq". |
| Anchor file | A file outside the corpus, unalterable by the checking account, naming the founding key of the signer register. |
| Content hash | The digest of the UTF-8 lines "path:digest", one for each ".md" file that a "scope" reaches, with "/"-separated paths from the corpus root, ordered by the first, in code-point order, of the paths of the "scope" that reach the file, then part by part in code-point order, joined by line feeds without a final one. |
| Digest | The lowercase hexadecimal SHA-256 of a byte sequence. |
| Entry digest | The entry hash of a transaction with an empty "signature". |
| Entry hash | The digest of a transaction without its "hash", serialized as STND.HARN.6 requires. |
| FAIL | A check's report that its property is violated. |
| Item | A document, register, provision, knowledge entry, Lexicon term, or tag. |
| Pin in force | A governance-ledger transaction with a nonempty "scope", for which no later governance-ledger transaction has a "scope" that reaches each path of the earlier "scope". |
| Reach | A "scope" reaches a path where one of its paths is that path or a directory above it. |
| Rehearsal | A script run on a fresh corpus copy, then the checks of that copy. |
| Template directory | A directory whose name begins with "_", or one under it. |
| Timestamp | An ISO 8601 time with its UTC offset. |

## Notes

Signer register has the meaning of STND.DFLT. Attribute, owning profile, and shared matter have the meanings they have in the drafting standard (STND.DRAFT). The checks of section Profile combination find what is mechanical; whether two listed provisions conflict is decided in review, because provisions are prose. An agent of a different agent configuration from the author performs that review (QA.8), and the adopter sees only its summary. Two provisions conflict where, for one classification and one consequence class, both apply to one domain item and one requires, permits, or recommends what the other prohibits. A conflict found in use is resolved meanwhile under GOV.25, GOV.5, and GOV.6: the more restrictive governs, an agent halts and refers (PRIME.14), and the concession is recorded; the human owner rules (GOV.3), and the project reports the conflict to the custodians (GOV.47) as a defect under GOV.26. The anchor file defaults to "/etc/governance/signer.json". A transaction of type configure records a configuration for STND.DFLT.22. STND.DRAFT and STND.IDENT name the commands of the harness package that report their checks, among them the revision checks, which read the revision history of each adopted document (STND.IDENT.6).

A later transaction whose "scope" reaches each path of an earlier one ends the earlier pin, so that a scope is widened by one transaction over the wider paths (STND.HARN.9). A transaction over part of a pinned scope ends no pin, so the wider pin goes stale once that part changes, and a transaction over the whole wider scope is what records the change. Two scopes that share a path, neither reaching each path of the other, both stay in force, and a change of the shared path stales both until one transaction reaches both. A transaction over several paths pins them as one content hash, so each later change of one of them takes a transaction over all of them, while a path pinned by a transaction of its own changes on its own. A "scope" names a directory or a ".md" file, so that a file directly under a directory whose subdirectories other transactions pin, and the "README.md" of the corpus root, are each pinned without the files beside them (STND.HARN.7). STND.HARN.31 makes a ".md" file that no transaction pins a FAIL, because GOV.36 makes a change made outside the ledger a defect and STND.HARN.9 sees only the scopes that transactions name. It reaches each ".md" file, including the "README.md" files and the files of template directories that STND.HARN.5 does not read as items, because the ledger pins files, not items. It binds, because it instantiates GOV.36, and raises no floor (GOV.11): it asks of a harness one comparison of the paths of the corpus with the scopes of the ledger; it asks no decision of the human owner and no new act of a project, and of the custodians only the transactions that pin the files now outside every scope, because the transaction that GOV.36 already asks for each change records a scope that reaches the file, as an adoption records the directory of the document it adopts. STND.HARN.32 binds, because it instantiates GOV.37, and raises no floor (GOV.11): a key in the field "checked_by" identifies a check, and one that names no check resolves to nothing; the provision asks of a harness one comparison of field values with its own keys, and nothing of the human owner or of a project. This standard sets no form for a configuration of an agent's environment; STND.DFLT.22 states when such a configuration displaces a provision.

A harness reads the signer register as it stands, so a key leaves only by the closing of its row: a row removed would leave each signature that the key made without an accepted signature. Each ledger numbers its own entries, so a Last entry closes a key on one ledger, and a row for "all" ledgers would stay open on each ledger begun after its closing; STND.HARN.10 therefore has each row among signers name one ledger. A row of required signatures for "all" ledgers closes nothing and stays. The keys that the register leaves open, for the field "signers" and STND.HARN.13, are those open on the governance ledger, which alone records a change of the register. STND.HARN.10 binds, because it instantiates GOV.36, and raises no floor (GOV.11): it asks nothing of a project that has founded no signer register, and of one that founds it only a row for each ledger that a key signs, in place of one row for all; it asks no decision of the human owner.

## References

| Identifier | Title |
| --- | --- |
| GOV | Governance |
| GUARD | Safeguards |
| PRIME | Prime Directives |
| QA | Process |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.IDENT | Identifier scheme and mnemonic register |
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

Each transaction SHALL hold exactly the fields "seq" (position, from one), "type" (adopt, amend, retire, classify, set-class, promote, authorize, revoke, register, waive, rule, declare-axiom, release, review, configure, or annotate), "actor" (role label or name), "role", "authority" (authorizing identifiers), "targets", "scope" (corpus directories and ".md" files whose content it pins), "rationale", "at" (timestamp), "corpus_hash" (content hash of a nonempty scope, or null), "prev" (previous entry hash, or null), "signature" (armored detached OpenPGP signature over the entry digest, or empty), "signers" (only on a governance-ledger transaction scoping the signer register: the keys the register then leaves open on the governance ledger, by fingerprint), "ledger" (only outside the governance ledger: its identifier), and "hash" (entry hash) (GOV.36).

#### STND.HARN.8 Chain integrity

Binding. Instantiates GOV.36.

Where the "seq", "prev", or "hash" of a ledger transaction violates STND.HARN.7, a harness SHALL report FAIL. A harness SHALL NOT append to such a ledger (GOV.36).

#### STND.HARN.9 Content pin

Binding. Instantiates GOV.36.

Where the content hash of the "scope" of a pin in force differs from its "corpus_hash", a harness SHALL report FAIL (GOV.36).

#### STND.HARN.10 Signer register form

Binding. Instantiates GOV.36.

The signer register SHALL hold a table of signers (Ledger, Role label, Name, Fingerprint, Last entry), a table of required signatures (Ledger, Actor, From entry), and each listed key, armored, under its fingerprint as heading. The Ledger of each row among signers SHALL name one ledger, not "all". A row for "all" ledgers among required signatures SHALL have From entry "1" (GOV.36).

#### STND.HARN.11 Signature acceptance

Binding. Instantiates GOV.36, GUARD.2.

Where a transaction that carries a signature, or that a row of required signatures names by ledger or "all", actor, and a From entry not above its "seq", lacks an accepted signature, a harness SHALL report FAIL (GOV.36, GUARD.2).

#### STND.HARN.12 Look-alike actors

Binding. Instantiates GOV.36, GUARD.2.

Where the signer register exists and a transaction's actor holds a non-ASCII character or equals a role label or actor of the register only after NFKC normalization, trimming, and case folding, a harness SHALL report FAIL (GOV.36, GUARD.2).

#### STND.HARN.13 Register chain

Binding. Instantiates GOV.36, GUARD.2.

Where a governance-ledger transaction scoping the signer register lacks an accepted signature by the anchor file's key, for the first, or by a key in the previous one's "signers", a harness SHALL report FAIL. Where the signer register exists without such a transaction, or the keys it leaves open on the governance ledger differ from the last one's "signers", a harness SHALL report FAIL (GOV.36, GUARD.2).

#### STND.HARN.31 Unpinned files

Binding. Instantiates GOV.36.

Where a ".md" file of the corpus is reached by no "scope" of a governance-ledger transaction, a harness SHALL report FAIL for that file (GOV.36).

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

#### STND.HARN.32 Known check keys

Binding. Instantiates GOV.37.

Where the field "checked_by" of a provision names a key that is neither "review" nor a key of a check that the harness makes, a harness SHALL report FAIL (GOV.37).

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
| 1.4 | 2026-10-26 | Minor amendment (GOV.41): STND.HARN.18 to STND.HARN.23, STND.HARN.29, and STND.HARN.30 are withdrawn with the terms Derived configuration and Refer, and this standard sets no form for a configuration of an agent's environment; STND.HARN.7: a "scope" names directories and ".md" files; STND.HARN.9 compares each pin in force, a new term, so that a later transaction whose "scope" reaches each path of an earlier one ends the earlier pin, with the new term Reach; the term Content hash counts each ".md" file that a "scope" reaches once, under the first, in code-point order, of its paths that reach it; new STND.HARN.31: FAIL for a ".md" file that no "scope" of the governance ledger reaches; new STND.HARN.32: FAIL for a "checked_by" key that names no check of the harness. Transition (GOV.42): the transition of ledger entry 53 ends, for STND.HARN.26 to STND.HARN.28 because the harness implements them, and for STND.HARN.18 because it is withdrawn; a ".md" file that no "scope" reaches is no defect until the transactions that pin KNOW, TAG, _PROJECT, STND/_doc.md, and README.md are recorded. |
| 1.5 | 2026-10-28 | Minor amendment (GOV.41): STND.HARN.10 has the Ledger of each row among signers name one ledger, not "all", where it had a row for "all" ledgers among signers keep Last entry "none", and keeps From entry "1" for a row of required signatures for "all" ledgers; the term Accepted signature accepts a key only by its row for the ledger of the transaction; the field "signers" of STND.HARN.7 and the second sentence of STND.HARN.13 read the keys that the register leaves open on the governance ledger; the Notes state that a key leaves only by the closing of its row, why a row for "all" ledgers is never closed, which keys the register leaves open, and the floor argument. Transition (GOV.42): none. |
