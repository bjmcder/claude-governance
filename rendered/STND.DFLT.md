# Defaults (STND.DFLT) 1.5.3

Adopted by The Custodian as revision 1.0 in ledger entry 33 (2026-10-10); revised to 1.0.1 in entry 37 (2026-10-10), 1.0.2 in entry 39 (2026-10-10), 1.1 in entry 40 (2026-10-10), 1.2 in entry 42 (2026-10-10), 1.3 in entry 50 (2026-10-11), 1.4 in entry 56 (2026-10-11), 1.5 in entry 90 (2026-10-20), 1.5.1 in entry 159 (2026-10-25), 1.5.2 in entry 176 (2026-10-26), and 1.5.3 in entry 200 (2026-10-27). This reading copy is composed from the per-provision files in STND/DFLT/ of the governance harness; the harness files are the system of record.

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

The work keeps a store of non-credential secrets only where the human owner chooses to provide one, by an instruction or a ledger entry; STND.DFLT.29 to STND.DFLT.31 then apply, and otherwise ask nothing. The choice is the human owner's own and no provision asks for it (STND.DRAFT.42). Without a store, an agent that an authorization permits to handle such a secret writes it to no location (AGENT.44). Where provided, the store (STND.DFLT.29) sits at the top of the work, outside "records", "notes", and version control, as AGENT.44 asks; an authentication credential never enters it (AGENT.45). It holds working copies of the secrets that the work is authorized to use, one per file, so that the working bounds admit each file only to an agent authorized to handle its secret: such an agent reads and writes it without a referral, and every other agent that reaches for it halts and refers (STND.DFLT.25). The directory is a temporary location, as the term now admits for working copies whose source lies outside the work, so that removing a secret the work no longer needs, as AGENT.44 asks, is the removal of a temporary item (STND.DFLT.15) rather than a reserved action; for the same reason no record cites a file of the store, and a record names a secret by a description that is itself no secret. The store holds only working copies whose source is the grantor of the secret, so AGENT.37 is met. Before its first write in a session an agent confirms that version control excludes the directory and that no other unprivileged account reads it, restores either condition that fails, which is a reversible local action, and refers rather than writing only where it is still unable to confirm (STND.DFLT.30). Archives, backups, and transfers leave the directory out, so the archive of STND.DFLT.4 carries no secret, and recursive and pattern-selected operations skip it unless authorized for it, so that a search of the work neither reads a secret nor halts on one (STND.DFLT.31). A grant that contains a secret is entered in the ledger without that secret (STND.DFLT.17). A project constitution states its own locations, or adopts these by citation.

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
| STND.INSTR | Agent instructions |

## Provisions

### Application

#### STND.DFLT.1 Scope of application

Binding. Instantiates GOV.22.

Each other provision of this standard SHALL apply only to work that has no project constitution (GOV.22).

#### STND.DFLT.22 Environment configuration

Binding. Instantiates GOV.22, GUARD.2.

Where the work is assured and an operative configuration that the agent is unable to alter enforces the outcome of a provision of this standard, as an entry that STND.DFLT.23 accepts records, that provision SHALL NOT apply (GOV.22). An agent SHALL NOT rely on a configuration it is able to alter to settle the tier of an action (GOV.22, GUARD.2).

### Records

#### STND.DFLT.2 Records directory

Binding. Instantiates GOV.22, REPRO.12.

Each record of a mechanism of GOV.21 SHALL be kept under version control in the directory "records" at the top of the work, or at a path that a file in it names (GOV.22, REPRO.12).

#### STND.DFLT.3 Records format

Binding. Instantiates GOV.22, REPRO.12.

Each record, and each result that a record cites, SHALL be plain text or in a publicly specified format (GOV.22, REPRO.12).

#### STND.DFLT.4 Records retention

Binding. Instantiates GOV.22, REPRO.12, REPRO.14.

Each record, and each result that a record cites or the recorded inputs that regenerate it (REPRO.1), SHALL be kept until the work is retired (GOV.22, REPRO.12). At retirement, they SHALL be archived with the work (GOV.22, REPRO.14).

#### STND.DFLT.5 Work ledger

Binding. Instantiates GOV.22, GOV.36, PRIME.7.

Each transaction that GOV.36 lists SHALL be appended to "records/ledger.jsonl" as an entry stating its actor, role, authority, reason, and the SHA-256 hash of the previous entry (GOV.22, GOV.36). An agent SHALL NOT append an entry that names the human owner as actor (GOV.22, PRIME.7).

#### STND.DFLT.6 Workspace directory

Binding. Instantiates GOV.22, INTPR.5.

The working-notes workspace SHALL be the directory "notes" at the top of the work (GOV.22, INTPR.5).

#### STND.DFLT.23 Accepted entries

Binding. Instantiates GOV.22, GOV.36.

Where the work is assured, only an entry that names the human owner as actor and carries the human owner's signature, which a verifier that the agent is unable to alter confirms by a key that the signer register lists for that owner and ledger, SHALL be accepted (GOV.22, GOV.36). Where the work is not assured, each entry that names the human owner as actor or records a grant under STND.DFLT.17 SHALL be accepted (GOV.22, GOV.36).

#### STND.DFLT.28 Workbench directory

Binding. Instantiates GOV.22, AGENT.35, AGENT.36, REPRO.12, REPRO.10, INTPR.13.

The workbench SHALL be the directory "workbench" in the directory of STND.DFLT.2, with each tool of AGENT.36 in its subdirectory "tools" and each other entry outside that subdirectory (GOV.22, AGENT.35, AGENT.36, REPRO.12, REPRO.10, INTPR.13).

### Process

#### STND.DFLT.7 Criteria before work

Binding. Instantiates GOV.22, QA.1.

The definition of done and acceptance criteria of a unit of work SHALL be committed before its first attempt (GOV.22, QA.1).

#### STND.DFLT.8 Contents of records

Binding. Instantiates GOV.22, QA.2, QA.7, QA.13.

Each record in the table of this provision SHALL state what its row lists (GOV.22).

| Record | Contents |
| --- | --- |
| Unit of work (QA.2) | Plan, what was done, and audit against the definition of done. |
| Review (QA.7) | Revision reviewed, reviewer, findings, and verdict. |
| Correction (QA.13) | Dependents found, relying parties notified, and the disposition of each dependent. |

#### STND.DFLT.9 Stopping bound

Binding. Instantiates GOV.22, QA.3.

A unit of work SHALL halt at its third consecutive attempt without progress (GOV.22, QA.3). Work continuing a halted unit SHALL begin only on a recorded decision of the human owner (GOV.22, QA.3).

#### STND.DFLT.10 Defect schedule

Binding. Instantiates GOV.22, QA.4.

Where the human owner records no other schedule, a tracked defect SHALL be resolved before a unit of work that changes what it affects is judged done (GOV.22, QA.4).

#### STND.DFLT.11 Dependency review

Binding. Instantiates GOV.22, REPRO.9.

Where a unit of work changes a dependency, its actor SHALL review the pinned revision of every direct dependency before the unit is judged done (GOV.22, REPRO.9).

#### STND.DFLT.12 Governance failure report

Binding. Instantiates GOV.22, QA.15.

The human owner SHALL report to the custodians each governance failure that an incident record states, from a report that an agent drafts, no later than the project's next compliance report (GOV.22, QA.15, GOV.47).

#### STND.DFLT.13 Classification location

Binding. Instantiates GOV.22, GOV.24.

The classification SHALL be a record that the human owner adopts by a ledger transaction (GOV.22, GOV.24).

### Safeguards

#### STND.DFLT.14 Bulk size

Binding. Instantiates GOV.22, GUARD.6.

The reserved-action register SHALL set no size for GUARD.6 (GOV.22, GUARD.6).

#### STND.DFLT.15 Register exemptions

Binding. Instantiates GOV.22, GUARD.4, GUARD.7.

The exempt classes of the reserved-action register SHALL be only these (GOV.22, GUARD.4, GUARD.7):

- change or removal of a file whose prior state is committed and verified recoverable;
- change or removal of an item whose prior state a snapshot or backup outside the action's scope holds, verified restorable beforehand;
- change or removal of content regenerable from recorded inputs (REPRO.1);
- change or removal of a temporary item;
- change or removal of an item that a checkpoint covers, where an entry that STND.DFLT.23 accepts records the mechanism that takes the checkpoint and the actions it covers, and that mechanism is operative.

#### STND.DFLT.16 Authorization record

Binding. Instantiates GOV.22, GUARD.10.

The ledger entry of an authorization SHALL state its grantor, action or class of actions, scope, duration, whether it is standing or per action, and date (GOV.22, GUARD.10).

#### STND.DFLT.17 Authorization reliance

Binding. Instantiates GOV.22, GUARD.2, GUARD.10, PRIME.10.

An agent SHALL enter each authorization that the human owner gives it directly as a ledger entry with itself as actor and the grant quoted without each secret that the grant contains (GOV.22, GUARD.10, PRIME.10). An agent SHALL rely only on an authorization given it directly in its current session, extended to it under GUARD.12, or carried by an entry that STND.DFLT.23 accepts (GOV.22, GUARD.2).

#### STND.DFLT.18 Threat-model table

Binding. Instantiates GOV.22, GUARD.16.

The threat model SHALL be the table of this provision (GOV.22, GUARD.16).

| Asset | Threat | Source | Protected |
| --- | --- | --- | --- |
| The work, its records, and its history | Change beyond authority | Every actor | Yes |
| The same, other than irreplaceable data | Loss | Host failure | No |
| Secrets the work uses | Disclosure | Every actor | Yes |
| Systems outside the provisioned environment | Action beyond authorization | An agent | Yes |
| Instruction authority | Injected instructions | Content an agent reads | Yes |
| Evidence | Fabrication or misrepresentation | Every actor | Yes |
| The work and the provisioned environment | Compromise | The host, its network, or an agent's provider | No |
| The work | Acts against it | The human owner | No |

#### STND.DFLT.19 Unlisted asset

Binding. Instantiates GOV.22, GUARD.16.

Where the work comes to hold irreplaceable data, or an asset or threat source that the table of STND.DFLT.18 omits, an agent SHALL halt that line of work and refer it (GOV.22, GUARD.16).

#### STND.DFLT.24 Scope enumeration

Binding. Instantiates GOV.22, GUARD.6.

Before a destructive action or remote write, an agent SHALL list each bulk item it affects, by path with symbolic links resolved, and act on that list alone (GOV.22, GUARD.6).

#### STND.DFLT.25 Bounds of reach

Binding. Instantiates GOV.22, PRIME.14.

Where a read or write would reach outside the working bounds, an agent SHALL halt that line of work and refer it (GOV.22, PRIME.14).

#### STND.DFLT.29 Secret store directory

Binding. Instantiates GOV.22, AGENT.44, GUARD.16, GUARD.7.

Where the human owner provides a store of AGENT.44 for the work, that store SHALL be the directory "secrets" at the top of the work, holding each secret in a file of its own whose name contains no secret (GOV.22, AGENT.44, GUARD.16). That directory SHALL be created empty and recorded as a temporary location at its creation (GOV.22, GUARD.7).

#### STND.DFLT.30 Secret store confirmation

Binding. Instantiates GOV.22, PRIME.10, PRIME.14.

Before an agent first writes to the directory of STND.DFLT.29 in a session, it SHALL confirm that version control excludes the directory and that its permissions let no account read it other than the agent's own and accounts with superuser privilege (GOV.22, PRIME.10). Where either condition fails, the agent SHALL restore it within its provisioned privilege (GOV.22, PRIME.10). Where the agent is unable to confirm both after that, it SHALL refer the line of work that needs the store, without writing to the directory (GOV.22, PRIME.14).

#### STND.DFLT.31 Secret store exclusions

Binding. Instantiates GOV.22, PRIME.10.

Each copy of the work that an agent makes for an archive or a backup, or for a transfer beyond the provisioned environment, SHALL exclude the directory of STND.DFLT.29 (GOV.22, PRIME.10). Each recursive or pattern-selected operation that an agent applies to the top directory of the work SHALL exclude that directory, other than one that an authorization permits the agent to apply to the store (GOV.22, PRIME.10).

### Agents

#### STND.DFLT.20 Referral statement

Binding. Instantiates GOV.22, PRIME.14.

A findings and justification statement SHALL state the halted line of work, the condition of PRIME.14 met, what the recommended action would destroy, change, retrieve, or acquire, its exact scope, the alternatives weighed, and how the human owner verifies the state before and after (GOV.22, PRIME.14).

#### STND.DFLT.21 Agent-instructions source

Binding. Instantiates GOV.22, GOV.48.

Where the agent-instructions standard is adopted, the agent instructions SHALL be its provisions, each with its own mode (GOV.22, GOV.48).

#### STND.DFLT.26 Operating-cost discipline

Binding. Instantiates GOV.22, GUARD.14.

Where an entry that STND.DFLT.23 accepts adopts an enforced spending cap as an agent's operating envelope, the agent SHALL use, within it, the least costly configuration capable of the unit of work (GOV.22, GUARD.14).

#### STND.DFLT.27 Access descriptors

Binding. Instantiates GOV.22, AGENT.23, REPRO.11.

The access descriptor of each record of AGENT.23 SHALL be one kind and one outcome of the table of this provision, joined by a colon (GOV.22, AGENT.23, REPRO.11).

| Part | Word | Meaning |
| --- | --- | --- |
| Kind | search | A query to a service that finds items. |
| Kind | retrieve | A request for an identified item. |
| Kind | write | A remote write. |
| Outcome | ok | The remote system served the request in full. |
| Outcome | refused | The remote system declined the request in whole or in part. |
| Outcome | failed | The request did not complete for a reason other than a refusal by the remote system. |

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
| 1.5.2 | 2026-10-26 | Editorial amendment (GOV.41): the Notes no longer say how a harness that derives an environment maps the bounds of the secret store, since STND.HARN 1.4 withdraws the provisions on a configuration that a harness derives; no obligation, permission, or defined meaning changes. |
| 1.5.3 | 2026-10-27 | Editorial amendment (GOV.41): the Source column of STND.DFLT.18 reads "Every actor" in place of "Any actor", in its three rows, the quantifier that STND.DRAFT.17 forbids; no obligation, permission, or defined meaning changes. |
