# Documentation

This repository holds a governance corpus for computational and cyber-physical systems whose outputs or actions are relied upon, and for the people and AI agents who build them, together with a small Python harness that reads and checks the corpus. The corpus states what a project owes at each consequence class, from CSQ4, work that nothing relies on yet, to CSQ0, work whose errors could cause injury or death. Its levels are a constitution (LVL0), profiles (LVL1), standards (LVL2), and the instruments of a project (LVL3).

The corpus in `harness/governance/` is the system of record. Every adoption and amendment is an entry of its hash-chained ledger, `harness/governance/ledger.jsonl`.

## Guides

| Guide | For | What it covers |
| --- | --- | --- |
| [installation.md](installation.md) | Anyone setting up a project | Each way to install the governance: the Claude Code plugin, a project's committed settings, the harness alone, a vendored copy, and no software at all |
| [adoption.md](adoption.md) | The human owner of a project | Setting and raising the consequence class, what the human is asked to do at each class, and the known limitations of the corpus as it stands |
| [operating.md](operating.md) | People and agents working in a project | Querying the corpus, updating the plugin, and pinning a revision |
| [custodian-guide.md](custodian-guide.md) | The custodian | How the corpus is amended and how a round of review runs |

## Reading copies

Two sets of reading copies sit beside the corpus. Both are composed from it, and the corpus governs where they differ.

- `rendered/`, at the root of the repository, is the full reading copy: one Markdown file per document, named by identifier, such as [`rendered/STND.DFLT.md`](../rendered/STND.DFLT.md). Start with [`rendered/LVL0.md`](../rendered/LVL0.md).
- `harness/rendered/` holds the copies of six standards that the harness command `compose` writes, under descriptive names. The plugin carries only this set, because a plugin installs only the files under `harness/`.

## Other parts of the repository

| Path | What it is |
| --- | --- |
| [`harness/README.md`](../harness/README.md) | The harness: its commands, the checks that `verify` runs, and how to read and check the corpus by hand |
| [`harness/governance/README.md`](../harness/governance/README.md) | How to find any provision by its identifier, without software |
| [`for-agents/`](../for-agents/README.md) | Material for agents that work on this repository |
| `review-records/`, `harness/records/` | The records of each round of review and of each unit of work on the harness |
| `research/` | Research notes that the Notes of the standards cite |
| [`OPEN-ITEMS.md`](../OPEN-ITEMS.md) | Work the custodian has directed, and items that ratified rounds left open |
