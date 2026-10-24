# Decision 0002: derive an agent's environment from governance

Status: proposed with the STND.HARN 0.1 draft (REPRO.7). Author: Claude, agent.

## Context

The human owner wants agents to run unattended, without approving routine actions, and without risking irreversible mass deletion. STND.INSTR names no tool or method (GOV.18). It states that environment means are derived from it and from STND.DFLT and are recorded under STND.DFLT.22.

## Decision

- **Outcomes live in governance.** STND.HARN.21 holds a table of outcomes, each with a key, a source provision, and a response (Refuse or Refer). The protected locations stay in STND.INSTR.3.
- **Adapters live in code.** An adapter renders those tables into one environment's configuration. An amendment of either table therefore reaches the configuration without a change of code. An outcome or a row the adapter does not know shows up as a gap in the coverage report, never as a silent pass.
- **The Claude Code adapter has three layers:**
  - the sandbox, enforced by the operating system, confines shell writes and network;
  - a pre-action guard that reads each tool call;
  - text permission rules as a second line.

  Managed settings make the managed rules and hooks the only ones that apply.
- **Routine actions run without a prompt.** Shell commands inside the sandbox and the file and read tools are allowed, so an unattended agent is not stopped by routine work. An allow rule is no authorization (STND.DFLT.16).
- **In an unattended session, Refer becomes deny.** The guard refuses what it would refer, with a reason that tells the agent to halt the line of work and refer it (PRIME.14). Nobody is there to answer a prompt.
- **Coverage is reported honestly.** The draft entry of STND.DFLT.22 names only outcomes enforced in full, so a provision whose outcome is enforced in part still binds the agent.
- **The checkpoint mechanism is recorded.** Claude Code's checkpoints cover only edits by its file tools in the main session. Its documentation states that changes made by shell commands are not tracked. The draft entry records exactly that coverage for the fifth exempt class of STND.DFLT.15.

## Alternatives weighed

| Alternative | Reason rejected |
| --- | --- |
| Write Claude Code rules into STND.INSTR or STND.DFLT | Names a tool in governance, against the custodian's direction and GOV.18 |
| Text permission rules alone | A rule matches the command as written, not its effect; the vendor documentation says so |
| A guard that refers everything it cannot parse | Stops unattended work on harmless commands; the sandbox already bounds what an unparsed command can reach |
| Claim full coverage where the guard parses commands | A program that deletes by itself is not seen; claiming more would make an agent rely on what the record does not settle (GUARD.2) |

## Adjustments made by review 0003

| Rule as decided above | Adjustment | Reason |
| --- | --- | --- |
| The sandbox confines shell writes | The sandbox also denies writes to every location of the enforcing configuration (`denyWrite`), including `<work>/.claude` and `<work>/.mcp.json` | The work is writable, and a program run by the shell could rewrite the project settings, which can widen the sandbox or run a command outside it |
| Coverage is reported honestly | No outcome is reported full: enforcing-configuration is partial | The file tools run outside the sandbox as the agent's account; only path checks before the call keep them off the user and project settings, and a symbolic link changed in between defeats those |
| The guard does not refer everything it cannot parse | The guard refers an item it cannot resolve (a variable, a substitution, an unknown directory), a computed program name, a shell fed by a pipe, and a command over 100 000 characters; a program it does not know still passes, after a search of its arguments for a command it knows | Such an item cannot be listed before the action (STND.DFLT.24), and the sandbox does not protect the work's records or version control, which lie inside the writable work |
| The hook runs the guard | The hook command ends in `\|\| exit 2` | Any exit other than 0 and 2 is a non-blocking error, so a guard that cannot start would let the call proceed |
| `environment` takes the agent's home with a default | `--home` is required, and the adapter registry, `--adapter`, and `--install-root` are removed | The default was the running account's home, wrong when the owner generates the files; the options had no consumer (SIMPL.5) |

## Adjustments made for proportioned assurance (unit 0004)

| Rule as decided above | Adjustment | Reason |
| --- | --- | --- |
| The hook command ends in `\|\| exit 2`; the sandbox must start | Only for assured work (`--assured`, CSQ0 or CSQ1). For other work, a guard that cannot run prints a notice to the human owner (`systemMessage`) and to the agent (`additionalContext`) and lets the call proceed, and Claude Code runs without the sandbox and says so | The custodian judged that fail-closed mechanisms at every class cause friction that invites circumvention; a visible degradation meets PRIME.4, and STND.DFLT 1.2 keeps every provision in force while the configuration is not operative |
| A guard fault denies the call | A call the guard cannot read is still denied at every class, since it is untrusted input (DSGN.2); a fault of the guard or its policy follows the class | Malformed input is the agent's or an attacker's, not the environment's |

## Adjustments made by review 0005

| Rule as adjusted for unit 0004 | Adjustment | Reason |
| --- | --- | --- |
| Only a call that raises `ValueError` is denied at every class; any other fault follows the class | Once the policy is read, every fault is denied at every class; only a guard that cannot run, or cannot read its policy, follows the class | A command nested too deep to parse raised `RecursionError`, which work that is not assured let through, so a call could choose to go unguarded |
| The notice sits in hand-written single quotes | `shlex.quote` | The quoting held only while the notice had no single quote |
| STND.DFLT 1.2 keeps every provision in force while the configuration is not operative | For work that is not assured, a configuration displaces no provision (STND.DFLT.22 as review 0005 revises it) | A lost configuration shows nothing, and a guard or sandbox that fails open lets an action through first, so "shown failing by nothing" left provisions displaced with nothing enforcing them |

## Adjustments made by review 0006

| Rule as decided above | Adjustment | Reason |
| --- | --- | --- |
| STND.HARN.21 holds the table of outcomes | STND.HARN 0.6 numbers it STND.HARN.24; the table keeps its name `environment-outcomes`. Configuration failure stays STND.HARN.29 | Retrieval provisions come first in the draft (review 0006) |

## Adjustments made by unit 0007

| Rule as decided above | Adjustment | Reason |
| --- | --- | --- |
| The work is writable and readable as a whole | Where the human owner provides the store of STND.DFLT.29 (`--secret-store`), each file under `<work>/secrets` lies outside the working bounds except those an authorization opens (`--secret NAME`). The guard checks the file tools, the shell paths it reads, Grep, and copies, moves, and removals that take in the store, at the real paths of the store and the opened files. The sandbox denies shell reads of the store's entries, allows each opened file by the narrower read path, and denies every shell write in the store | The term Working bounds of STND.DFLT admits a file of the store only to an agent authorized for its secret, and the Notes of STND.DFLT have the harness map it. No permission rule is used, because a deny or ask rule over the store would override an allow rule for an opened file; the documentation does not state that a narrower path reopens one for writing. The denial of shell writes also keeps a shell command from changing the store's permissions or removing a file of it; the agent refers those, as STND.DFLT.30 has it refer what it is unable to restore, rather than letting a program the guard does not read rename or overwrite a closed secret |
| A guard fault denies the call once the policy is read | A store that exists but cannot be listed counts as holding a closed file | Fail closed (review 0007 of unit 0007) |

## Adjustments made by unit 0008

| Rule as decided above | Adjustment | Reason |
| --- | --- | --- |
| Every remote write is referred (the transition of ledger entry 53) | `environment --authorization ID` reads an authorization file of the corpus in the form of STND.PROJ.6 and STND.PROJ.7 and, where it is in force under STND.HARN.29, writes each destination and kind the guard matches into the policy field `remote_writes`. The guard lets a `git push` or a `gh` tracker post proceed only where its destination, kind, and branches equal those of an unexpired entry as whole strings, the call holds no other command, and nothing the guard reads (assignments, global options, push options, the git configuration of the repository, the account, and the system, local tags, variables of git and gh) may send it elsewhere or add to it. An authorization not in force stops the derivation; a per-action one, and the kinds publish, transmit, and other, stay referred and are named in the coverage report | GUARD.2: a configuration relies on an authorization only as the record states it; a configuration cannot count the one action a per-action authorization covers; a pattern or a prefix admits a destination the owner never named |
| The ask rule `Bash(git push *)` refers every push | Dropped while an authorization of kind commit is derived; the guard alone then refers an unauthorized push | A permission rule outranks a hook's answer, so the rule would refer the authorized push too |
| A malformed policy field is a guard fault | A malformed entry of `remote_writes` is left out, so that its write is referred, and the rest of the policy stands | A fault of the policy lets the call proceed unguarded for work that is not assured (STND.HARN.23); one bad entry must not disable the guard |

## Adjustments made by the reviews of unit 0008

| Rule as adjusted above | Adjustment | Reason |
| --- | --- | --- |
| The ask rule `Bash(git push *)` is dropped while a commit is authorized | The rule stays, with ask rules for `gh issue create`, `gh issue comment`, and `gh pr comment`; the guard answers `allow` for a write an authorization names. Whether that answer outranks the ask rule is for an installation test; until then an authorized write may be referred | Security review H1: with the rule dropped, every gap of the guard's parse let a push through. No source authorized for this unit shows that a hook's allow outranks an ask rule, so the design refers in doubt |
| A push passes as the sole command of its call | It passes only as one command of plain words (letters, digits, blanks, quotes, and `_./:@=,+-`), from inside the work, where the first `.git` found is the work's own and valid, no hook is present, and git, gh, and their options are read as the guard models them; `-n` is a dry run only as its own word beside options that take no value | Security review H1, H2, H3, M1, M2: an option's value read as `-n`, a nested `.git`, a here-document's substitution, and a program named `git` each let a write through |
| Writes into the work are free | A write into a `.git` directory by a file tool, a redirection, or a copying or creating command reaches history-rewrite (Refuse) | Security review H2, M2: such a write plants a configuration, a hook, or a ref that a later push reads |
| An authorization extends as the owner names it | `--role` names the role or agent the configuration is derived for; an authorization whose `delegable_to` does not name it is not in force; a signature is required wherever a signer register exists; `--expiry-horizon` bounds the expiry; an expiry of `until revoked` is accepted | Cold review, Defect 2 (GUARD.12) and Should-fix 6; security review M4 and M5 |

## Adjustments made by unit 0010

| Rule as adjusted above | Adjustment | Reason |
| --- | --- | --- |
| A signature is required wherever a signer register exists | Unchanged there and for assured work, where `--accept-unsigned` has no effect and the reason says so. Where the work is not assured and no signer register exists, `environment --authorization` exits 1 with the reason unless the owner passes `--accept-unsigned`; with it, the summary prints for each authorization a line that it was accepted unsigned. The code is stricter than the row Signature of STND.HARN.29, failing closed, since a refused derivation leaves the write referred, which STND.HARN.18 allows | Security verification of unit 0008, M-c: without a register an agent is able to append an unsigned `authorize` naming the human owner and recompute the chain, and appends are permitted writes, so the summary was the only control and nothing asked the owner to read it |
