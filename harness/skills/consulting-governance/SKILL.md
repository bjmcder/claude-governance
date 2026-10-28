---
name: consulting-governance
description: Retrieves from the governance corpus the provisions that govern an action or a question, each with its full text, through the read-only govharness commands. Relevant before a destructive action, a remote write, a network retrieval, an installation, a delegation, a promotion, or a release, and whenever a reserved action, an authorization, a record, a referral, a term, or the consequence class is in question.
---

# Consulting the governance corpus

## Where the corpus is

The corpus of this plugin is the directory `${CLAUDE_PLUGIN_ROOT}/governance`. It is the authoritative text (GOV.35): one directory per document, one Markdown file per provision, and the hash-chained ledger `ledger.jsonl`. `${CLAUDE_PLUGIN_ROOT}/governance/README.md` maps each identifier to its file, so `GOV.12` is `GOV/12.md` and `STND.DFLT` is `STND/DFLT/_doc.md`. The corpus changes when the plugin updates, and the plugin keeps no other state.

The harness package `govharness` is in `${CLAUDE_PLUGIN_ROOT}`. It needs Python 3.11 or later and nothing outside the standard library. Every command on this page reads and changes nothing. No work depends on the harness (GOV.38): the files of the corpus answer every question that the commands answer.

## Running the commands

Without installation, each command runs as:

```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -B -m govharness show "${CLAUDE_PLUGIN_ROOT}/governance" GOV.38
```

Where the package is installed, `govharness` is on the `PATH`, and where `GOVHARNESS_ROOT` names a corpus, `show`, `find`, `context`, `pairs`, and `onset` take that corpus when no root is given:

```bash
govharness show GOV.38
```

A corpus that `GOVHARNESS_ROOT` names may be a different revision from the plugin's. Naming the root, as in the first form, removes the doubt.

## What each command returns

In this table, ROOT is `"${CLAUDE_PLUGIN_ROOT}/governance"`, or nothing where `GOVHARNESS_ROOT` is set.

| Command | Returns |
| --- | --- |
| `show ROOT ID` | The item's full text and status, what governs it, what it cites, and what cites it. `ID` is an identifier (`PRIME.6`, `LEX.remote-write`) or a section locator (`LVL0#normative-language`) |
| `show ROOT ID --expand` | The same, with the full text of each item it cites |
| `show ROOT DOC` | A document's lead text and the names of its sections and items |
| `show ROOT DOC --all` | A document's provisions in full, in reading order |
| `find ROOT WORD... [--in-force]` | One line per matching item, best first: provisions and terms rank above Notes. Exit status 1 when no item holds a word |
| `context ROOT WORD... [--budget N] [--in-force]` | The best matches and the items they cite, each whole while the budget of characters lasts, then the names of the rest |
| `pairs ROOT DOC [--with ID ...] [--amends LVL0_ID ...]` | The pairs of provisions that STND.HARN.28 puts to review before a change of `DOC` |
| `onset ROOT CSQn` | One line per provision, or named part of a provision, that applies from the class CSQn by its field `onset`. `show` prints the same onset beside the mode of each provision |

`find` and `context` match words and their inflected forms, not meanings. The corpus's own terms match best: "remote write" finds the provisions on pushing, where "push" finds only the provisions that use that word. `--in-force` keeps only adopted and ratified items.

## Questions and the commands that answer them

| Question | Commands |
| --- | --- |
| What applies to this action? | `context ROOT WORDS --in-force`, then `show ROOT ID` for each provision relied on |
| What does this term mean? | `find ROOT WORDS`, then `show ROOT LEX.<slug>` |
| What applies to code in language X? | `show ROOT STND.<X> --all` (STND.PY, STND.CXX, STND.RUST, STND.STDC, STND.FTN, STND.JL, STND.LEAN, STND.SV) |
| Which actions are reserved to the human owner? | `show ROOT PRIME.6`, `show ROOT GUARD.6`, `show ROOT LEX.reserved-action` |
| Which actions need a recorded authorization? | `show ROOT PRIME.7`, `show ROOT GUARD.10`, `show ROOT GUARD.13` |
| Before a remote write or a push | `context ROOT remote write --in-force`, `show ROOT LEX.remote-write` |
| Before a destructive action | `context ROOT destructive action --in-force`, `show ROOT STND.DFLT.24` |
| Before a build, an install, or a test run | `show ROOT STND.DFLT.34`, `show ROOT STND.DFLT.35`, `show ROOT STND.DFLT.25` |
| When a line of work halts | `show ROOT PRIME.14`, `show ROOT STND.DFLT.20`, `show ROOT AGENT.15` |
| Before a delegation | `show ROOT AGENT.11`, `show ROOT GUARD.12` |
| What the agent instructions are | `show ROOT STND.INSTR --all` |
| Under the defaults, where records go | `show ROOT STND.DFLT --all` |
| What a class requires, and from which class | `show ROOT STND.CLASS.10`, `show ROOT STND.CLASS.18`, `show ROOT STND.CLASS.19` |
| What a reclassification to a more severe class owes | `show ROOT GOV.14`, `show ROOT STND.CLASS.22`, `show ROOT STND.CLASS.19` |
| What does reclassification to CSQn add? | `onset ROOT CSQn`, then `show ROOT ID` for each provision relied on |
| Before a promotion or a release | `show ROOT QA.11`, `show ROOT QA.10`, `show ROOT GOV.50` |

GOV.39 asks that a provision be read in full before it is relied on; `show` prints the full text, and a line of `find` names an item without its text.

## Reading the files directly

Where Python is not available, each identifier is a file under `${CLAUDE_PLUGIN_ROOT}/governance/`, as its `README.md` maps them. The front matter between the `---` lines is an index; the text below it is normative and governs where they disagree. `${CLAUDE_PLUGIN_ROOT}/rendered/` holds reading copies of six standards (STND.DFLT, STND.INSTR, STND.DRAFT, STND.IDENT, STND.CLASS, and STND.HARN) under descriptive names, such as `defaults.md` for STND.DFLT.
