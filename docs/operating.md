# Operating with the governance

This guide covers day-to-day use once a project has installed the governance ([installation.md](installation.md)) and recorded its class ([adoption.md](adoption.md)): looking up what applies, checking the corpus, and moving to a new revision.

## Looking up what applies

In Claude Code with the plugin, the skill `consulting-governance` gives an agent the commands that retrieve provisions, and Claude can load it on its own when a question of governance comes up. You can also call it yourself with `/governance:consulting-governance`. The skill `orienting-to-governance` describes where the project's records are, and `classifying-work` drafts a classification on request; Claude never calls that one on its own.

At a terminal, with `GOVHARNESS_ROOT` set as in [installation.md](installation.md#3-the-harness-alone), these commands answer most questions. None of them changes or writes anything. An agent or a person may use them in place of reading or searching the corpus files; the files answer the same questions without any software (GOV.38).

| Question | Command |
| --- | --- |
| What does a provision say, and what cites it? | `govharness show PRIME.6` |
| What does a provision say, with the text of what it cites? | `govharness show PRIME.6 --expand` |
| What does one section of a document say? | `govharness show LVL0#normative-language` |
| What sections and provisions does a document hold? | `govharness show STND.DFLT` |
| What does a standard require, in full? | `govharness show STND.PY --all` |
| Which provisions use these words? | `govharness find destructive action --in-force` |
| What governs this topic, within a size limit? | `govharness context remote write --in-force --budget 6000` |
| What does a term mean? | `govharness find remote write`, then `govharness show LEX.remote-write` |
| What applies from a given class? | `govharness show STND.CLASS.10` |

The skill `consulting-governance` lists more questions with the commands that answer them: before a destructive action, a remote write, a delegation, a promotion, or a release, and when a line of work halts.

### What the commands return

`show` takes an identifier (`PRIME.6`, `LEX.remote-write`) or a section locator (`LVL0#normative-language`), in any case. For an item or a section it prints the full text and status, what governs it, what it cites, and what cites it. For a document it prints the lead text and the names of its sections and items; `--all` adds each provision in full, in order. `--expand` adds the full text of each item the shown item cites.

`find` prints one line per matching item, best first, and `context` prints the best matches and the items they cite, each in full while the budget of characters lasts, then lists the rest under "Also relevant, not shown". Each text is printed whole or not at all, so a section larger than the remaining budget is listed by name. Both commands match words and their inflected forms, not meanings: "deleting" finds "deletion", but "push" finds only the passages that use that word. The corpus's own terms work best, "remote write" rather than "push" and "destructive action" rather than "delete". Items that hold every word come first. Provisions, Lexicon terms, and Terms sections rank above Notes and other prose, and a document identifier among the words matches the provisions and sections of that document. `--in-force` keeps only adopted and ratified items.

`show`, `find`, `context`, and `pairs` exit with status 0 when something was found, 1 when nothing was, with the message on the standard error, and 2 for a usage error.

With no corpus on the command line, a command reads the corpus that `GOVHARNESS_ROOT` names, or else `./governance` where that directory exists. With neither, it exits with status 2 and a line naming the variable. A corpus can also be named as the first argument, as in `govharness show path/to/governance GOV.38`; for `find` and `context`, the first argument is taken as the corpus only where it is a directory that holds `LVL0/_doc.md`, so a query word that happens to name a directory of the project stays a word.

Without installing the harness, the same commands run from a clone of this repository. From its `harness/` directory, name the corpus `governance`:

```bash
python3 -B -m govharness show governance PRIME.6
python3 -B -m govharness context governance remote write --budget 6000 --in-force
```

From any other directory, `PYTHONPATH` names the directory that holds `govharness/`:

```bash
PYTHONPATH=governance-harness/harness python3 -B -m govharness show governance-harness/harness/governance GOV.38
```

For reading at length, [`rendered/`](../rendered/LVL0.md) has a reading copy of every document.

## Checking the corpus

A quick check that the harness is installed and finds its corpus:

```bash
govharness show GOV.38
govharness verify
```

`show` prints GOV.38, the provision on the harness itself. `verify` checks every file against its manifest, the hash chain of the ledger, the identifiers and references, and the logical consistency of the constitution's precedence and waivers. It takes a few seconds and writes nothing. On an unchanged corpus it passes with one warning, g.18, on three provisions of STND.DRAFT whose bundles of three modals were reviewed and ratified. A failure means the copy differs from what the ledger pinned, and the message names the file. [`harness/README.md`](../harness/README.md#what-verify-checks) lists each check.

## Knowing which revision is in use

| Installation | How to see the revision |
| --- | --- |
| Plugin | `claude plugin list`: the version is the commit it was installed from |
| Harness alone, or vendored copy as a submodule | `git -C <clone> log -1 --format='%H %d'` |
| Vendored copy as a subtree | The `git-subtree-split` line of the squash commit, as [installation.md](installation.md#verify-update-and-remove-1) shows |
| Committed project settings | The `ref` or `sha` in `.claude/settings.json` |

The last line of `harness/governance/ledger.jsonl` is the newest governance transaction in that revision; its `seq` is the entry number that the headers of the reading copies cite.

The custodian tags each published state of the corpus `ledger-N`, where N is the `seq` of the last ledger entry it includes: `ledger-202` is the state whose ledger ends at entry 202. A project pins by such a tag, or by a full commit hash wherever the mechanism accepts one:

| Installation | Accepts |
| --- | --- |
| Plugin, through a marketplace source | A tag or branch, in `#ref` or `ref` |
| Plugin, through a plugin source in `.claude/settings.json` | A full 40-character commit hash, in `sha` |
| Harness alone, from a clone | A tag or a commit hash, given to `git checkout` |
| Vendored copy as a submodule | A tag or a commit hash, checked out inside the submodule |
| Vendored copy as a subtree | A tag or branch |

[installation.md](installation.md#before-you-start) shows each form. Here and below, `<clone>` is a clone of this repository, and `<new tag>` is the tag of the revision to move to.

## Moving to a new revision

Every change to the corpus is a ledger transaction with a stated rationale, so the ledger is the change log. Before moving a pinned project forward, list what changed between the two revisions:

```bash
git -C <clone> diff ledger-202 <new tag> -- harness/governance/ledger.jsonl
```

Each added line names its type (`adopt`, `amend`, and so on), its targets, and its rationale. `git -C <clone> diff --stat ledger-202 <new tag> -- harness/governance` lists the files that changed.

Then move the pin:

- Plugin from a marketplace that follows a branch: `claude plugin marketplace update governance-harness`, then `claude plugin update governance@governance-harness`, then `/reload-plugins` or a new session.
- Plugin pinned in `.claude/settings.json`: change `ref` to the new tag, or `sha` to its commit hash (`git -C <clone> rev-parse '<new tag>^{commit}'`), commit, and have members start a new session.
- Harness alone or submodule: fetch, check out the new tag or its commit hash in the clone or submodule, and, for a submodule, commit the change.
- Subtree: run `git subtree pull` with the new tag, as [installation.md](installation.md#verify-update-and-remove-1) shows.

A project's own records, class, and constitution stay as they are; a new revision of the corpus does not change them.

## Recording what agents relied on

REPRO.11 records, for each step an agent performs, the agent's identity, configuration, and instruction revision. The pinned revision of the governance, a tag or a commit, is the value to record for the governance part of the instruction revision.
