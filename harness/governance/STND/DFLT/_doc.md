---
id: "STND.DFLT"
level: "LVL2"
kind: "standard"
title: "Defaults"
status: "adopted"
revision: "1.5.1"
adopted: "2026-10-10"
adopted_by: "The Custodian"
instantiates: ["GOV.22", "GOV.21"]
rank: null
waivable: false
---

## Purpose and scope

This standard provides the mechanisms of GOV.21, and the ledger of GOV.36, for work without a project constitution (GOV.22). It also gives the vocabulary of access descriptors that AGENT.23 leaves to the defaults, and the locations of the workbench and, where the human owner provides one, of the store of non-credential secrets, which AGENT.35 and AGENT.44 leave to the project. Every provision is binding, because it instantiates GOV.22 (GOV.10), and none applies once a project constitution defines its own mechanisms. No provision grants an authorization, adopts a hazard analysis, sets a class, authorizes an estimate (GOV.22), or sets a time limit.

## Normative and informative parts

The body of a numbered provision, including its table, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Assured work | Work for which an entry that names the human owner as actor records CSQ0 or CSQ1 as the consequence class, and no later entry that STND.DFLT.23 accepts for assured work records a less severe class. |
| Attempt without progress | A change to or run of the work, checked against the acceptance criteria, after which no more criteria are met than at the best earlier point of the unit of work. |
| Bulk item | A file, a listed object of a remote store, a database row, or a message; a directory counts as its contents. |
| Checkpoint | A copy of an item's prior state that the provisioned environment keeps outside the scope of an action before the action changes or removes the item. |
| Destructive action | An action that removes or overwrites an item, or alters it other than by appending. |
| Operative | Of a configuration or mechanism that an entry records: found in the current session to be installed as the entry states; for assured work, found so by a verifier that the agent is unable to alter. |
| Session | One continuous run of an agent and the instructions it received in that run. |
| Signer register | The register SIGNR of keys, each listed for the ledgers it signs, against which the harness verifies signatures. |
| Temporary location | A directory created empty for intermediates, or for working copies of items whose source lies outside the work, recorded as temporary at creation, outside "records" and the version-control metadata. |
| Working bounds | The locations, network domains, and retrieval scopes that a configuration the agent is unable to alter, or an entry that STND.DFLT.23 accepts, opens to an agent; by default, the top directory of the work, and for reading also the installed software and the account's files other than the store of AGENT.44, each location that holds secrets or credentials by the convention of its operating system or tool, and each location that the threat model or an entry that STND.DFLT.23 accepts names as holding secrets, credentials, or other data it marks as protected (PRIME.10). A domain is within the bounds only with the purpose and volume an authorization names (GUARD.13). A file of the directory of STND.DFLT.29 is within the bounds only for an agent that an authorization permits to handle the secret that the file holds (PRIME.10). |

## Mechanisms and their provisions

| Mechanism | Provisions |
| --- | --- |
| Work process, stopping rule, defects, review, correction, incidents (QA.2, QA.3, QA.4, QA.7, QA.13, QA.15) | STND.DFLT.7 to STND.DFLT.10, STND.DFLT.12 |
| Dependencies, retention (REPRO.9, REPRO.12) | STND.DFLT.2 to STND.DFLT.4, STND.DFLT.11 |
| Classification (GOV.24) | STND.DFLT.13 |
| Workspace (INTPR.5) | STND.DFLT.6 |
| Workbench (AGENT.35) | STND.DFLT.28 |
| Store of non-credential secrets (AGENT.44) | STND.DFLT.29 to STND.DFLT.31 |
| Threat model (GUARD.16) | STND.DFLT.18, STND.DFLT.19 |
| Reserved-action register (GUARD.4) | PRIME.6 with STND.DFLT.14, STND.DFLT.15, STND.DFLT.24 |
| Authorization (GUARD.10) | STND.DFLT.16, STND.DFLT.17 |
| Agent instructions and cost (GOV.48, PRIME.14, GUARD.14) | STND.DFLT.20, STND.DFLT.21, STND.DFLT.26 |
| Network access records (REPRO.11, AGENT.23) | STND.DFLT.27 |
| Ledger (GOV.36) | STND.DFLT.5, STND.DFLT.23 |

## Notes

An unlisted destructive action is a bulk action and reserved (GUARD.6); listing removes only that status, and each item still needs an exempt class (GUARD.5). The fourth class rests on GUARD.7 as LVL0 1.5 amended it. Command-level practice, such as shell guards and dry runs, belongs to STND.INSTR (STND.INSTR.4, STND.INSTR.5).

No class is set by default (GOV.13); work without a project constitution is relied upon by no one beyond its author (GOV.20), so the rows of STND.CLASS.18 and STND.CLASS.19 have no occasion to act until the human owner records one.

An allow rule in a configuration is not an authorization unless an entry that STND.DFLT.23 accepts adopts it with the content of STND.DFLT.16, and never for an irrevocable remote write (GUARD.11). Without a cap adopted under STND.DFLT.26, PRIME.8 requires an authorized estimate.

Only for assured work does an entry need a signature (STND.DFLT.23) or a configuration displace a provision (STND.DFLT.22); elsewhere a configuration may fail open, so every provision stays in force. No class is assumed (GOV.13): an entry of the human owner, signed or not, makes work assured, and only a signed one ends that. For other work, STND.DFLT.5 and PRIME.7 bar a forged entry, but nothing detects one. The custodians found the signer register with a key whose fingerprint the human owner keeps as the anchor where the agent's account cannot write it; a signature binds to its ledger and position.

Access descriptor has the meaning AGENT gives it. A descriptor is a kind and an outcome joined by a colon, as in "retrieve:refused"; three kinds and three outcomes give nine descriptors from six words, and the list is closed. A refusal includes one that a cap, a paywall, a required credential, a rate limit, or a published access rule causes; a failure includes a timeout, a transport error, an item not found, or a refusal by the provisioned environment.

The workbench (STND.DFLT.28) sits with the other records, so that it is kept under version control and retained with them, as AGENT.35 and AGENT.36 ask; its tools, which are repaired in place, sit apart from its entries, which are never altered (AGENT.34), so that a reviewer and a check of alteration tell them apart.

The work keeps a store of non-credential secrets only where the human owner chooses to provide one, by an instruction or a ledger entry; STND.DFLT.29 to STND.DFLT.31 then apply, and otherwise ask nothing. The choice is the human owner's own and no provision asks for it (STND.DRAFT.42). Without a store, an agent that an authorization permits to handle such a secret writes it to no location (AGENT.44). Where provided, the store (STND.DFLT.29) sits at the top of the work, outside "records", "notes", and version control, as AGENT.44 asks; an authentication credential never enters it (AGENT.45). It holds working copies of the secrets that the work is authorized to use, one per file, so that the working bounds admit each file only to an agent authorized to handle its secret: such an agent reads and writes it without a referral, and every other agent that reaches for it halts and refers (STND.DFLT.25). The directory is a temporary location, as the term now admits for working copies whose source lies outside the work, so that removing a secret the work no longer needs, as AGENT.44 asks, is the removal of a temporary item (STND.DFLT.15) rather than a reserved action; for the same reason no record cites a file of the store, and a record names a secret by a description that is itself no secret. The store holds only working copies whose source is the grantor of the secret, so AGENT.37 is met. Before its first write in a session an agent confirms that version control excludes the directory and that no other unprivileged account reads it, restores either condition that fails, which is a reversible local action, and refers rather than writing only where it is still unable to confirm (STND.DFLT.30). Archives, backups, and transfers leave the directory out, so the archive of STND.DFLT.4 carries no secret, and recursive and pattern-selected operations skip it unless authorized for it, so that a search of the work neither reads a secret nor halts on one (STND.DFLT.31). A grant that contains a secret is entered in the ledger without that secret (STND.DFLT.17). A project constitution states its own locations, or adopts these by citation. A harness that derives an environment under STND.HARN.18 maps the bounds of the store as STND.DFLT.29 and the working bounds state them.

Locations that hold secrets or credentials by convention include the key directories of secure-shell and privacy-guard tools, the credential files of command-line clients for remote services, keyrings and password stores, shell history files, and browser profiles; an agent decides them by their path, without reading them (PRIME.10).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| GOV | Governance |
| GUARD | Safeguards |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.HARN | Harness specification |
| STND.INSTR | Agent instructions |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-10 | Adopted. |
| 1.0.1 | 2026-10-10 | Editorial amendment (GOV.41): the section References lists the documents this standard cites, as STND.DRAFT.34 requires; no obligation changes. |
| 1.0.2 | 2026-10-10 | Editorial amendment (GOV.41): the notes drop a clause that the adoption of the agent-instructions standard made stale; no obligation changes. |
| 1.1 | 2026-10-10 | Minor amendment (GOV.41): STND.DFLT.15 gains a fifth exempt class, a change or removal of an item that a checkpoint of the provisioned environment covers, where a signed entry records the mechanism and the actions it covers; the Terms define Checkpoint. |
| 1.2 | 2026-10-10 | Minor amendment (GOV.41): for assured work (CSQ0, CSQ1), STND.DFLT.23 accepts only signed and confirmed entries of the human owner; for other work, it accepts unsigned ones and an agent's record of a grant (STND.DFLT.17); STND.DFLT.22 displaces a provision only for assured work, and it and the fifth exempt class of STND.DFLT.15 hold only while the configuration or mechanism is operative; the Terms define Assured work and Operative. |
| 1.3 | 2026-10-11 | Minor amendment (GOV.41): new STND.DFLT.27 fixes the access descriptors of network access records (AGENT.23) as one of three kinds (search, retrieve, write) and one of three outcomes (ok, refused, failed). |
| 1.4 | 2026-10-11 | Minor amendment (GOV.41): STND.DFLT.12 has the human owner report a governance failure, from a report an agent drafts, by the next compliance report instead of before the next unit of work; the default working bounds open to reading the account's files other than the secret store and each conventional or named location of secrets or credentials (STND.DRAFT.42); the Notes give examples of conventional locations. | |
| 1.5 | 2026-10-20 | Minor amendment (GOV.41), conforming on the adoption of AGENT: new STND.DFLT.28 places the workbench in the directory "workbench" of the records directory, its tools in "tools"; new STND.DFLT.29 to STND.DFLT.31 place the store of non-credential secrets of AGENT.44, where the human owner provides one, in the temporary directory "secrets" at the top of the work, one secret per file, have an agent confirm before its first write in a session that version control excludes it and that no other unprivileged account reads it, restoring either condition where it fails, and keep it out of archives, backups, transfers, and unauthorized recursive or pattern-selected operations; the working bounds admit each file of the store only to an agent authorized to handle its secret; STND.DFLT.17 enters a grant without the secrets it contains; the term Temporary location admits working copies of items whose source lies outside the work. |
| 1.5.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Notes cite STND.INSTR.4 and STND.INSTR.5, which hold the shell guards and dry runs that the Notes assign to STND.INSTR, and References lists STND.INSTR; no obligation, permission, or defined meaning changes. |
