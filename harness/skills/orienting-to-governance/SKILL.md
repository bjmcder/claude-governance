---
name: orienting-to-governance
description: Describes where a project that follows the governance corpus keeps its governance records, under its project constitution or under the defaults of STND.DFLT, the ledger, the classification and consequence class recorded, the authorizations in force, the working notes, and the workbench, with the commands that read each. Relevant at the start of a session, after context compaction, and whenever the consequence class or an authorization in force is in question.
---

# Orienting to a project's governance

The corpus of this plugin is `${CLAUDE_PLUGIN_ROOT}/governance`. A project's own records are in the project, not in the plugin. The commands below read and change nothing; ROOT stands for `"${CLAUDE_PLUGIN_ROOT}/governance"`, and each `show` runs as `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -B -P -m govharness show ROOT ID`, or as `govharness show ID` where the package is installed and `GOVHARNESS_ROOT` is set.

## Which mechanisms apply

A project either has a project constitution, a LVL3 instrument that its human owner adopted (GOV.20, STND.PROJ), or works under the defaults of STND.DFLT, which apply only to work without a constitution (STND.DFLT.1).

- With a constitution, its sections name the place of each record: the Records, Working notes, Workbench, Secret store, Authorizations, and Classification rows of the table of STND.PROJ.1. The constitution is a file of the project; the project's `AGENTS.md`, `CLAUDE.md`, or `records/` names where it is.
- Without one, the defaults below hold.

## Locations under the defaults

| Record | Location | Provision |
| --- | --- | --- |
| Records of every mechanism of GOV.21 | `records/` at the top of the work, or a path that a file in it names | STND.DFLT.2 |
| Ledger of the work | `records/ledger.jsonl`, one hash-chained entry per line | STND.DFLT.5 |
| Classification, consequence class, and any expected class | An entry of that ledger that the human owner adopts, appended by the owner or entered by an agent from the owner's direct act | STND.DFLT.13, STND.DFLT.17, STND.CLASS.5 |
| Authorizations, the direction that authorizes operating cost among them | Entries of that ledger, with the content of STND.DFLT.16 | STND.DFLT.16, STND.DFLT.17, STND.DFLT.33 |
| Adopted instruction files | Entries of that ledger that name each file's path and content | STND.INSTR.11 |
| Persons the human owner names to instruct agents, with the scope of each naming | Entries of that ledger | PRIME.11, STND.DFLT.17, STND.DFLT.36 |
| The statement that an environment is isolated, for superuser or administrative privilege | An entry of that ledger naming the environment | PRIME.9, STND.DFLT.37 |
| The accepted point, and the owner's confirmations of foreign entries | Acceptance entries of that ledger, and entries of each confirmation | STND.DFLT.23, STND.DFLT.38 |
| The project's own mnemonic | A `register` entry of that ledger | STND.IDENT.23 |
| Working notes | `notes/` at the top of the work, with each tool memory store | STND.DFLT.6 |
| Workbench | `records/workbench/`, with its tools in `records/workbench/tools/` | STND.DFLT.28 |
| Store of non-credential secrets, where provided | `secrets/` at the top of the work, within the working bounds only as an authorization allows | STND.DFLT.29, STND.DFLT.30 |

STND.DFLT.23 states which entries of the ledger are accepted, and the term Assured work of STND.DFLT states when only signed entries are. An entry of an act of the human owner that lies after the accepted point, the entry that the latest acceptance entry names, and that the agent did not append in its current session, is foreign (the terms Accepted point and Foreign entry of STND.DFLT); before a line of work relies on one, an agent refers every foreign entry in one statement that lists each by its position and hash (STND.DFLT.23). Absent an accepted entry that names another person as the human owner, the person who provisioned the agent's environment and directs it is taken as the owner (STND.DFLT.36).

## Reading the ledger

Each entry states what STND.DFLT.5 lists. In a ledger that the harness reads or appends to, each line of `records/ledger.jsonl` is one JSON object with the fields of STND.HARN.7: `seq`, `type`, `actor`, `role`, `authority`, `rationale`, `at`, and the hash fields. An entry that an agent entered from an act of the human owner names the agent as its actor and the human owner as the actor of the act (STND.DFLT.17). These commands list the entries that record a class and the entries that record or end an authorization:

```bash
grep -E '"type": ?"(classify|set-class)"' records/ledger.jsonl
grep -E '"type": ?"(authorize|revoke)"' records/ledger.jsonl
```

An authorization states its scope and duration (STND.DFLT.16); a standing authorization that an agent proposes also states the agents to which it extends (STND.DFLT.32, GUARD.12).

`PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -B -P -m govharness ledger check records/ledger.jsonl`, or `govharness ledger check records/ledger.jsonl` where the package is installed, reports each line of the ledger whose form, fields, or hash chain is broken, and writes nothing.

## What the corpus says about orientation

| Matter | Provision |
| --- | --- |
| What an agent reads before it first changes the work in a session | AGENT.17 |
| Where no consequence class is recorded: the presumption of CSQ4, and what it never covers | GOV.13, GOV.14, PRIME.14 |
| Which other lines of work continue after a halt | AGENT.15 |
| Which authorizations an agent relies on | STND.DFLT.17, STND.DFLT.23, GUARD.2 |
| Whose instructions count | PRIME.11, STND.DFLT.36 |
| The agent instructions under the defaults | STND.DFLT.21, STND.INSTR |
| The notes workspace and its authority | INTPR.5, PRIME.11 |

Each row's provisions print with `show ROOT ID`, and `show ROOT STND.DFLT --all` prints the defaults whole.
