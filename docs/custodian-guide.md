# Custodian's guide

This guide is for the custodian of the corpus: who amends it, how a round of amendment runs, what comes to you for decision, and where the records go. The step-by-step process that agents follow in a round, and the standing directions that bind every round, are in [for-agents/standing-process.md](../for-agents/standing-process.md). This guide does not repeat them.

## What the custodian decides

The custodians alone amend the constitution (GOV.40), and they adopt the profiles and the standards (GOV.41). They register each new mnemonic (STND.IDENT.23). A project's human owner adopts that project's own instruments; the custodian does not. Agents draft and propose, and never adopt.

Every change to the corpus is a ledger transaction (GOV.36). An edit to a file without one fails `verify`, because the ledger pins the hash of the content each transaction adopted.

## How a round runs

A round is one set of related amendments, from your direction to the applied ledger entries.

1. You direct a change, or ratify an open item. The direction goes into the round's `decisions.md`.
2. An agent drafts the text and an amendment script, a short Python program that makes the text changes and appends the transaction, and rehearses it on a copy of the corpus.
3. Agents of another configuration from the author review the draft cold, and review the pairs of provisions that STND.HARN.28 lists for the changed documents.
4. The author fixes what the reviews find, and a further agent verifies the fixes cold. A round that spans several documents gets a review across them.
5. The round comes to you for ratification, with the questions that only you can answer.
6. After you ratify, the script is applied to the live corpus, the reading copies are rebuilt, and `OPEN-ITEMS.md` is brought up to date, as is `harness/README.md` where a command or a check that it describes changed.

The full process, with the drafting checks and the rule for when a provision binds, is in [for-agents/standing-process.md](../for-agents/standing-process.md).

## What comes to you

- The decisions of the round, in `review-records/<round>/decisions.md`, for you to confirm or amend.
- Each question that a reviewer marks as yours. Review reports have a column "Custodian decision", which is "no" unless the finding turns on a choice only you can make.
- Any argument that a new binding provision raises no floor (GOV.11), which only you accept.
- The ratification itself. Nothing is applied to the live corpus before it.

## Where the records go

| Record | Place |
| --- | --- |
| A round's briefs, drafts, reviews, verifications, dispositions, decisions, and pair lists | `review-records/<round>/` |
| The amendment script and its content module | `tools/amendment-scripts/` |
| A unit of work on the harness code | `harness/records/units/`, with its reviews in `review-records/harness/` |
| Work you have directed and items a round left open | [`OPEN-ITEMS.md`](../OPEN-ITEMS.md) |
| Templates of the briefs that agents receive | [`for-agents/briefs/`](../for-agents/briefs/drafting.md) |

Records keep the paths they were written with. Where a file has since moved, git history resolves the old path.

## Checking the corpus after a round

From `harness/`:

```bash
python3 -B -m govharness verify governance
python3 -B -m govharness references governance --check
python3 -B -m govharness compose governance --check
python3 -B -m unittest discover -s tests -t .
```

`verify` passes with the g.18 warning on STND.DRAFT.35, .39, and .42. `references --check` and `compose --check` each report nothing stale. The full test suite takes about six minutes.

## Releasing a revision to projects

Projects pin a revision of this repository by tag, branch, or commit ([installation.md](installation.md)). A tag on the commit that applies a ratified round gives them a stable name for it. Naming the tag for the last ledger entry ties the two together:

```bash
tail -n 1 harness/governance/ledger.jsonl | python3 -c 'import json,sys; print(json.load(sys.stdin)["seq"])'
git tag -a ledger-202 -m "Governance at ledger entry 202"
```

A project that follows a branch receives every commit; one that pins a tag moves only when it changes the tag.

## Working with agents in this repository

Agents that work on this repository find their material through the root `CLAUDE.md` and `AGENTS.md`, which point to [for-agents/](../for-agents/README.md). The Claude Code plugin, rooted at `harness/`, is a separate thing: it is what an adopting project installs, and it carries none of this repository's process material.
