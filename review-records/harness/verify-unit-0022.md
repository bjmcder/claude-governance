# Verification of the revision of unit 0022 (76a0afc, 695e65e)

Verifier: another configuration than the author. Clones of dee64ca and HEAD (695e65e) under `/tmp/claude-1000/ver0022/`, offline.

## What I ran

| Finding | dee64ca | HEAD |
| --- | --- | --- |
| High 1, `find`/`context tests coverage`, `tests/notes.md` present, `GOVHARNESS_ROOT` set | exit 2; with `tests/` empty, exit 1 | exit 0, equal to the positional form |
| High 2, `context … remote write authorization --in-force` | two cut Notes; GUARD.10, .12, .13, REPRO.12 named | the four whole; Notes named; no marker |
| Medium 2, `show STND.CLASS.10 \| wc -l` | 102 | 65 |
| Low 1, `show STND --all` | 419 284 bytes | 1474, as `show STND` |
| Low 3, `compose --all a/b --write` | FileNotFoundError | 71 written |
| Low 4, `pairs governance numer` | exit 1 | exit 0, equal to `NUMER` |

- Medium 3 was already fixed at dee64ca (`docs/installation.md:232` describes `--cache`). Medium 4: `harness/README.md:9` reads as recorded. Low 5: `git check-ignore` matches both paths.
- Whole texts: I took 38 `context` blocks from five queries, with budgets from 3000 to 100 000. Each is a prefix of its `show` output, and what follows it there is "Governed by", "Also cites", "Cited by", or nothing. No block carries a cut marker. STND.HARN.3 holds.
- Verdicts: the output of `verify governance` and of `check --out-dir`, with its three files, is byte-identical at both commits (PASS, g.18).
- Mutants killed by their named tests: 6, 10, 12, High 1, and Low 4. The tests pass unmutated, and so do the three targeted modules (42 tests).
- Ruff, run `--isolated --line-length 79 --extend-select E501` on the seven changed Python files: at HEAD it reports only the earlier FURB167 (`tests/derive/test_reading_copy.py:101`). The E501 at `retrieval.py:647` is gone, and `ruff format --check` passes.

## Findings

Every review finding is fixed. One Low finding concerns the record only:

1. `harness/records/units/0022-query-layer.md:69` and `:70` say that `docs/operating.md` still describes the old root rule and the cut. 695e65e corrected both (`docs/operating.md:29`, `:33`). `:73` calls Medium 3 out of scope, though it was fixed at dee64ca. Fix: state both facts.

A side note: `pairs governance NUMER.1` exits 0 with "0 pair(s)", taking an item for a document. dee64ca behaves the same, and the review did not raise it.
