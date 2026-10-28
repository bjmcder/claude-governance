# Cold verification of the documentation and plugin fixes (`verify-docs-plugin`)

Verifier of another configuration, at commit 695e65e, with a local tag `ledger-202` on HEAD of a scratch clone under `/tmp/claude-1000/verify-dp/`. No network. Only this file was written.

## What I ran

- Option 3 of `docs/installation.md`: clone, `checkout ledger-202`, `pip install --no-index` (fails on `setuptools`, as the text now says), the `PYTHONPATH` form (prints GOV.38), `rev-parse 'ledger-202^{commit}'` on an annotated tag, as `custodian-guide.md:62` makes one (the `^{commit}` note holds), `fetch --tags`, the test subset (46 tests, OK). The `--no-build-isolation` form is unverified: no `setuptools` here, as its condition allows.
- Option 4: `git submodule add <path>` refused with `transport 'file' not allowed`; the `protocol.file.allow=always` form, the tag and full-hash checkouts, add, commit, update, and `git rm`, all as written. `git subtree add` with the tag, `subtree pull`, a full hash (accepted), an abbreviated hash (`couldn't find remote ref`), and the `--grep='git-subtree-dir'` lookup (prints `git-subtree-split: 695e65e…`). Mirror, bundle, and clone. The vendored `show` and `verify` (PASS, g.18 only), and `GOVHARNESS_ROOT` without a corpus argument.
- `docs/operating.md`: the ten table commands, exit 0; the two clone-form commands; `context --budget 100` and `1500` print each item whole or list it by name (`retrieval.py:662`); from a directory holding `remote/` without `LVL0/_doc.md`, `find` and `context remote write` keep `remote` as a word (`arguments.py:20`); exit 1 with the message on stderr for a missing item, 2 for a usage error and for no corpus; the `./governance` fallback.
- `adoption.md` Known limitations against `show` for GUARD.14, PRIME.8, GOV.22, STND.DFLT.5/13/17/23/24/25/26, GUARD.6, PRIME.6, GOV.13/14/50, QA.11, STND.CLASS.1/10/18, and the STND.DFLT terms: each statement matches; no record or finding ID remains; the expected-class anchor exists.
- `standing-process.md:11-13` against STND.DRAFT.7/9/13/17; step 8 against `custodian-guide.md:20`.
- A script over every relative link and fragment in `docs/`, `README.md`, `for-agents/`, `harness/skills/`: 0 problems.
- Grep outside `review-records/` and `harness/records/` for `tests/equivalence`, `run_equivalence`, `CUSTODIAN.md`, `HANDOFF.md`: nothing stale; `CUSTODIAN.md` is a pointer, as `architecture.md:14` says. The "Ported from `archive/tools-flat/…`" docstrings in six tests are provenance.
- Plugin: 1677 tracked files, 3.82 MB. No em dash, curly quote, British spelling, or STND.DOCS.9 vocabulary in the edited files.

High 1, Medium 1 to 3, and Low 1 to 9 are fixed as the review described.

## Findings

### Low

1. `docs/installation.md:250` and `harness/README.md:148`: "runs in under ten seconds". Here, 46 tests took 10.5 to 10.9 s on three runs; the reviewer saw 7.8. Fix: "in about ten seconds".
