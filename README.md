# Governance corpus and harness

A governance corpus for computational and cyber-physical systems whose outputs or actions are relied upon, and for the people and AI agents who build them, with a small Python harness that queries and checks it. The corpus is plain Markdown in `harness/governance/`, and every adoption and amendment is an entry of its hash-chained ledger, `harness/governance/ledger.jsonl`. A project can install the harness, or the Claude Code plugin built on it, so that its agents look up the provisions that apply. Nothing depends on that software: the corpus is complete and readable without it.

## Where to start

| You are | Start at |
| --- | --- |
| Setting up a project to use the governance | [docs/installation.md](docs/installation.md) |
| The human owner of a project | [docs/adoption.md](docs/adoption.md) |
| Working day to day in a project | [docs/operating.md](docs/operating.md) |
| The custodian of the corpus | [docs/custodian-guide.md](docs/custodian-guide.md) |
| An agent working on this repository | [for-agents/README.md](for-agents/README.md) |
| Reading the governance itself | [rendered/LVL0.md](rendered/LVL0.md), then the other reading copies in `rendered/` |

[docs/README.md](docs/README.md) indexes the documentation.

## Layout

| Path | What it is |
| --- | --- |
| `harness/` | The Claude Code plugin and the harness: the corpus in `governance/`, the Python package `govharness/`, its tests, its skills, and the records of its development ([harness/README.md](harness/README.md)) |
| `.claude-plugin/marketplace.json` | The marketplace that lists the plugin |
| `rendered/` | A reading copy of every document, named by identifier |
| `docs/` | Documentation for people |
| `for-agents/` | Material for agents working on this repository; not part of the plugin |
| `CLAUDE.md`, `AGENTS.md`, `CUSTODIAN.md` | Short pointers to `for-agents/`; `CUSTODIAN.md` keeps the path that earlier records cite |
| `review-records/` | The records of each round of review |
| `research/` | Research notes that the Notes of the standards cite |
| `tools/` | The amendment scripts that produced the ledger entries, and two checking scripts |
| `OPEN-ITEMS.md` | Work the custodian has directed, and items that ratified rounds left open |

## Quick check

From `harness/`, with Python 3.11 or later:

```bash
python3 -B -m govharness verify governance
python3 -B -m govharness show governance GOV.38
```
