# Operating with the governance

This guide covers day-to-day use once a project has installed the governance ([installation.md](installation.md)) and recorded its class ([adoption.md](adoption.md)): looking up what applies, checking the corpus, and moving to a new revision.

## Looking up what applies

In Claude Code with the plugin, the skill `consulting-governance` gives an agent the commands that retrieve provisions, and Claude can load it on its own when a question of governance comes up. You can also call it yourself with `/governance:consulting-governance`. The skill `orienting-to-governance` describes where the project's records are, and `classifying-work` drafts a classification on request; Claude never calls that one on its own.

At a terminal, with `GOVHARNESS_ROOT` set as in [installation.md](installation.md#3-the-harness-alone), these commands answer most questions. None of them changes anything.

| Question | Command |
| --- | --- |
| What does a provision say, and what cites it? | `govharness show PRIME.6` |
| What does a provision say, with the text of what it cites? | `govharness show PRIME.6 --expand` |
| What does a standard require, in full? | `govharness show STND.PY --all` |
| Which provisions use these words? | `govharness find destructive action --in-force` |
| What governs this topic, within a size limit? | `govharness context remote write --in-force --budget 6000` |
| What does a term mean? | `govharness show LEX.remote-write` |
| What applies from a given class? | `govharness show STND.CLASS.10` |

`find` and `context` match words and their inflected forms, not meanings, so the corpus's own terms work best: "remote write" rather than "push", "destructive action" rather than "delete". Provisions and Lexicon terms rank above the explanatory Notes. `--in-force` keeps only adopted and ratified items.

For reading at length, [`rendered/`](../rendered/LVL0.md) has a reading copy of every document.

## Checking the corpus

```bash
govharness verify
```

`verify` checks every file against its manifest, the hash chain of the ledger, the identifiers and references, and the logical consistency of the constitution's precedence and waivers. It takes a few seconds. On an unchanged corpus it passes with one warning, g.18, on three provisions of STND.DRAFT whose bundles of three modals were reviewed and ratified. A failure means the copy differs from what the ledger pinned, and the message names the file.

## Knowing which revision is in use

| Installation | How to see the revision |
| --- | --- |
| Plugin | `claude plugin list`: the version is the commit it was installed from |
| Harness alone or vendored copy | `git -C <clone> log -1 --format='%H %d'` |
| Committed project settings | The `ref` or `sha` in `.claude/settings.json` |

The last line of `harness/governance/ledger.jsonl` is the newest governance transaction in that revision; its `seq` is the entry number that the headers of the reading copies cite, and that a tag such as `ledger-202` names.

## Moving to a new revision

Every change to the corpus is a ledger transaction with a stated rationale, so the ledger is the change log. Before moving a pinned project forward, list what changed between the two revisions:

```bash
git -C <clone> diff ledger-202 <new tag> -- harness/governance/ledger.jsonl
```

Each added line names its type (`adopt`, `amend`, and so on), its targets, and its rationale. `git -C <clone> diff --stat ledger-202 <new tag> -- harness/governance` lists the files that changed.

Then move the pin:

- Plugin from a marketplace that follows a branch: `claude plugin marketplace update governance-harness`, then `claude plugin update governance@governance-harness`, then `/reload-plugins` or a new session.
- Plugin pinned in `.claude/settings.json`: change `ref` or `sha`, commit, and have members start a new session.
- Harness alone or vendored copy: check out the new tag in the clone or submodule and commit, as [installation.md](installation.md#4-a-vendored-copy) shows.

A project's own records, class, and constitution stay as they are; a new revision of the corpus does not change them.

## Recording what agents relied on

REPRO.11 records, for each step an agent performs, the agent's identity, configuration, and instruction revision. The pinned revision of the governance, a tag or a commit, is the value to record for the governance part of the instruction revision.
