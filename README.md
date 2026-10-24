# Governance corpus

The working governance corpus of the custodian, with the harness that verifies, composes, and amends it. The system of record is `harness/governance/`, whose hash-chained ledger `harness/governance/ledger.jsonl` records every adoption and amendment. `harness/README.md` gives the current state, the commands, and the checks.

| Path | What it is |
| --- | --- |
| `harness/` | The runnable harness: `governance/` (the corpus), `govharness/` (Python 3.11 or later, standard library only), `tests/`, and `records/` (units, reviews, and decisions of the harness) |
| `rendered/` | A reading copy of each document, composed from the corpus by `govharness.derive.reading_copy.compose` |
| `research/` | Research notes behind the standards, cited from their Notes |
| `review-records/` | The review record of each round: drafts, reviews, verifications, dispositions, and pair lists |
| `tools/` | Briefs for drafting, review, and rounds; `findings.py`; `check_refs.py`; `lvl0.txt`; and `amendment-scripts/`, the content modules and apply scripts that produced the ledger entries |
| `docs/` | Documents carried over from the former online project |
| `CUSTODIAN.md` | The custodian's standing process and directions |
| `OPEN-ITEMS.md` | Work the custodian has directed, and items left open by ratified rounds |

## Quick check

```bash
cd harness
python3 -B -m govharness verify governance          # every check passes
python3 -B -m govharness references governance --check
python3 -B -m govharness compose governance --check
python3 -B -m unittest discover -s tests
```
