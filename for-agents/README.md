# Material for agents working on this repository

This directory holds the material for agents that draft, review, or apply amendments to the corpus in this repository. It is not part of the Claude Code plugin, which is rooted at `harness/` and holds what an adopting project installs. People start at [docs/](../docs/README.md).

| File | What it is for |
| --- | --- |
| [standing-process.md](standing-process.md) | The custodian's standing process for a round of amendment, and the directions that hold for every round: agnosticism, offload, determinism, high-assurance code, no restatement, documentation, security, cleanup, hosting, and the harness |
| [briefs/drafting.md](briefs/drafting.md) | A template of the brief for an agent that drafts an amendment; each round keeps its completed brief in `review-records/<round>/` |

Other places an agent in this repository reads:

| Path | What it holds |
| --- | --- |
| `harness/governance/` | The corpus, the system of record, with its ledger `ledger.jsonl` |
| `rendered/` | A reading copy of every document, named by identifier |
| `harness/README.md` | The harness commands and the checks of `verify` |
| `OPEN-ITEMS.md` | Work the custodian has directed, and items left open |
| `review-records/<round>/` | The records of each round: its decisions, briefs, drafts, reviews, and verifications |
| `tools/amendment-scripts/` | The scripts that produced the ledger entries, and their helpers |
| `tools/findings.py`, `tools/check_refs.py` | The drafting findings of a corpus copy, and the References check g.25 |
| `research/` | Research notes that the Notes of the standards cite |

`review-records/` and `research/` are records and research. The briefs and decisions in them describe past rounds; the standing process and the current round's `decisions.md` are what a new round works from.
