# Deep review of 2026-10-28: documentation and plugin (`review-docs-plugin`, DP)

Reviewer of another configuration, reading cold at commit dee64ca. Scope: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CUSTODIAN.md`, `docs/*.md`, `for-agents/**`, `harness/README.md`, both plugin manifests, the three skills, and `harness/pyproject.toml` as the docs describe it. Only this file was written.

## What I ran

- From a scratch clone under `/tmp/claude-1000/rev/`: every command of `docs/operating.md`, `docs/installation.md`, `docs/custodian-guide.md`, `README.md`, and the three skills (`${CLAUDE_PLUGIN_ROOT}` replaced by a scratch copy of `harness/`): 24 skill commands, all exit 0; every troubleshooting message and exit status reproduced verbatim; `verify` 3.9 s, g.18 warning only, nothing written under a fresh `HOME`; the `sha256sum` manifest check; `references`, `compose`, and `compose --all` checks clean; the test subset, 41 tests in 7.8 s; the `ledger append` command of `docs/adoption.md` on a scratch project and the `grep` lines of `orienting-to-governance` on its output.
- Option 3: `pip install` into a scratch venv, an editable install, `uv tool install` in place of `pipx` (absent here), `GOVHARNESS_ROOT`, `govharness show GOV.38`, `govharness verify`. Option 4: submodule, subtree, and bundle against scratch repositories with a local clone as `REPO`. Option 5 read.
- 10 fetches of code.claude.com (manifest, marketplace, install, loading, CLI, skills, settings, memory).
- The 69 provisions the docs cite, printed with `show`; STND.DOCS.9 vocabulary, British spellings, curly quotes, and em dashes grepped; deleted and moved paths grepped outside the corpus and records.

Only Python 3.14 was available; "3.11 or later" is unverified.

Found correct: both manifests against the documented schema (no `version`, so the version is the commit); no hooks, commands, agents, `bin/`, or `settings.json` under `harness/`; skill frontmatter, `$ARGUMENTS`, and `${CLAUDE_PLUGIN_ROOT}` in the body; every other plugin command, flag, scope, settings shape, and claim in `installation.md` and `operating.md`; `README.md` sends an installer to `docs/installation.md` in its first row; each file serves one audience; nothing proposed is presented as in force; no STND.DOCS.9 vocabulary, British spelling, or em dash. **No imperative addressed to the agent in any skill.**

## Findings

### High

1. **No tag exists, and every pinned option needs one.** `docs/installation.md:23` calls `ledger-202` "An example tag"; `:199` `git -C governance-harness checkout ledger-202` fails: `error: pathspec 'ledger-202' did not match any file(s) known to git`. Same at `:121`, `:134`, `:258`, `:266`. `git tag` on dee64ca lists nothing. Fix: tag the ratified head as `docs/custodian-guide.md:58-63` describes, and say at `:23` "The custodian tags each ratified ledger entry; until a tag exists, use a commit hash" (which `checkout` and a submodule accept; `subtree add` does not, L3).

### Medium

1. **`pip install` and `pipx install` need PyPI.** `harness/pyproject.toml:2` `requires = ["setuptools>=68"]`; `pip install --no-index ./governance-harness/harness` fails: `Could not find a version that satisfies the requirement setuptools>=68`. `docs/installation.md:9` says "Network at install: Yes, for the clone", `:10` "No, once the copy is made", and `:278` sends the vendored copy through option 3. Fix: after `:204`, "The install fetches `setuptools` from the Python Package Index; offline, use the `PYTHONPATH` form"; row 4's column becomes "No, with the `PYTHONPATH` form".
2. **A human guide cites review records.** `docs/adoption.md:70` "The deep review of 2026-10-28 found ... [corpus-core.md](../review-records/...)"; headings `:72-88` carry `(CC1)`, `(AD2)`; `:94-96` `(CC32)`, `(CC5)`, `(CC7)`. STND.DOCS.5 and the documentation direction keep process records out, and the section goes stale at ratification. Fix: state each limitation as a fact with its provisions, and close with "The custodian's review of 2026-10-28 proposes corrections; until they are entered in the ledger, this is the corpus as it stands."
3. **Submodule from a local path is refused.** `:19` lets `REPO` be a local path; `:257` `git submodule add REPO vendor/governance-harness` fails: `fatal: transport 'file' not allowed`. Fix: "For a local `REPO`, run `git -c protocol.file.allow=always submodule add ...`".

### Low

1. `docs/installation.md:298` "The first prints the vendored commit": true for a submodule; in a subtree it prints the project's own commit. Fix: "for a subtree, the squash commit's message names it: `git log --format=%B -- vendor/governance-harness | grep 'from commit'`".
2. `docs/installation.md:59`: `--sparse` is for "`github` and `git` sources only"; with a local-path `REPO` it does nothing. Fix: "for a git URL, `--sparse` ...".
3. `docs/installation.md:266`: `git subtree add ... REPO ledger-202` takes a ref, not a hash (`fatal: couldn't find remote ref dee64ca`); one clause once H1 admits hashes.
4. `docs/adoption.md:62`, CSQ4: "Promoting a result before it is reported (QA.11)". STND.CLASS.10 lets CSQ4 work "omit every obligation of these Articles above the floor", QA.11 among them; STND.CLASS.1's CSQ4 test says "nothing relies on it before promotion". Fix: "Promoting a result before anyone relies on it, which ends CSQ4 (STND.CLASS.1, GOV.50)".
5. `for-agents/standing-process.md:11`: "banned body words ("such as", "for example", "can", "will", ...)". STND.DRAFT.7 marks "can", "will", "is to" as review, not defect, and lists neither "such as" nor "for example". Fix: "the expressions STND.DRAFT.7 excludes and its vague qualifiers and quantifiers, plus "such as" and "for example" by the custodian's direction".
6. `for-agents/standing-process.md:20` "update `harness/README.md`" unconditionally; `docs/custodian-guide.md:20` conditions it on a changed command or check. Fix: align step 8 with the guide.
7. `harness/tests/derive/test_reading_copy.py:237` cites "CUSTODIAN.md step 8", now `for-agents/standing-process.md`. The only stale path outside records.
8. `docs/architecture.md:196`: a shipped test "stops with an error here". Fix: delete `harness/tests/equivalence/` and the paragraph.
9. The plugin is 3.7 MB tracked, 1678 files, and ships `harness/records/` (427 KB of unit, review, and decision records) and `harness/tests/` (356 KB), while `for-agents/README.md:3` says it "holds what an adopting project installs". Fix: say so at `docs/installation.md:34`, or move the records once the ledger-citation question is settled.
