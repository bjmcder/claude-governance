# Governance corpus and harness

A governance corpus for computational and cyber-physical systems whose outputs or actions are relied upon, and for the people and AI agents who build them, with a small Python harness that queries and checks it. The corpus is plain Markdown in `harness/governance/`, and every adoption and amendment is an entry of its hash-chained ledger, `harness/governance/ledger.jsonl`. A project can install the harness, or the Claude Code plugin built on it, so that its agents look up the provisions that apply. Nothing depends on that software: the corpus is complete and readable without it.

## Where to start

| You are | Start at |
| --- | --- |
| Setting up a project to use the governance | [docs/installation.md](docs/installation.md) |
| The human owner of a project | [docs/adoption.md](docs/adoption.md) |
| Working day to day in a project | [docs/operating.md](docs/operating.md) |
| The custodian of the corpus | [docs/custodian-guide.md](docs/custodian-guide.md) |
| Maintaining the repository or the harness | [docs/architecture.md](docs/architecture.md), then [harness/README.md](harness/README.md) |
| An agent working on this repository | [for-agents/README.md](for-agents/README.md) |
| Reading the governance itself | [rendered/LVL0.md](rendered/LVL0.md), then the other reading copies in `rendered/` |

[docs/README.md](docs/README.md) indexes the documentation.

## Layout

`harness/` holds the corpus, the harness package, and the Claude Code plugin; `docs/` holds the documentation for people, and `for-agents/` the material for agents working on this repository. [docs/architecture.md](docs/architecture.md) describes each part of the repository and of the harness package.

## Quick check

From `harness/`, with Python 3.11 or later:

```bash
python3 -B -m govharness verify governance
python3 -B -m govharness show governance GOV.38
```
