# Cold review of unit 0022 (4aef256, judged at e3dafe9)

Reviewer: another configuration. All runs in clones under `/tmp/claude-1000/rev0022/`, offline.

## What I ran

- `verify`/`check --out-dir`: byte-identical at 851bc25 and e3dafe9 (PASS, g.18 only), and so is `pairs` for four documents, so no verdict changed. Full suite: 200 OK, 345 s; fast subset 8.1 s. `compose --all ../rendered --check`: stale 0.
- Read-only: corpus `chmod -R a-w`, `env -i`, empty `HOME`/`XDG_CACHE_HOME`, read-only working directory. `show`, `find`, `context`, `pairs`, and `verify` exit 0, and the tree diff is empty.
- Wheel built offline (copied setuptools, `--no-build-isolation`) into a fresh venv. Run from `/`, `govharness show GOV.38` works with `GOVHARNESS_ROOT` set. The wheel holds only `.py` modules, enough.
- Ties: deterministic under three hash seeds. Ruff: same three default findings.

## Findings

### High

1. **A query word that names a local directory becomes the root** (`cli/arguments.py:101`). With `GOVHARNESS_ROOT` set, in a project with `tests/`, `govharness find tests coverage` reads `tests/` as an empty corpus. It exits 1 with "no item holds a word of: coverage", a false not-found, or exits 2 when `tests/` holds a `.md`. Contradicts README:207. Fix: take the first word as the root only when it holds `LVL0/_doc.md`, or add `--root`. Test it from a directory holding `tests/`.
2. **The `context` cut breaks binding STND.HARN.3 and crowds out provisions** (`query/retrieval.py:15`, `:712`; README:19). A cut text is neither "whole" nor "by its identifier alone". On `context remote write authorization --in-force`, GUARD.10, .12, .13, and REPRO.12 were shown before the unit; now two Notes cuts take the budget and these are only named. Fix: name long prose only, as HR-1 proposed. Cuts need an amendment of STND.HARN.3 first.

### Medium

1. **A cut can be just the heading** (`retrieval.py:649–653`). `CUT_MIN` is tested before the trim to a line end. For `left` from 272 to 835, STND.CODE#notes shows 42 characters plus the marker. Fix: test `CUT_MIN` after the trim.
2. **The fold barely shortens `show`.** `show STND.CLASS.10` went from 104 lines to 102; the record says 62. Forty documents cite it by Notes only. Fix: one line per heading ("Notes of: AGENT, CPS, …"), and correct the record.
3. **`docs/installation.md:230` is stale.** It still describes the `~/.cache` default and `--no-cache`, which now exits 2 (still so at dee64ca). Fix: describe `--cache`.
4. **README:21 `pipx install harness` names a PyPI project.** pip reads a bare `harness` as a requirement, so online it would fetch someone else's package. Fix: `./harness`. Also state that the package holds no corpus and `GOVHARNESS_ROOT` must name a checkout; only `docs/installation.md` implies it.
5. **Ten of sixteen mutants survive** (below).

### Low

1. `show STND --all` prints 415 KB, because `items_below` opens every standard (`retrieval.py:341`). Open only LVL0 parts, or warn.
2. New E501 at `retrieval.py:647` (86 > 79); the record's default-rules ruff run skips E501.
3. `compose --all a/b --write` with `a/` missing gives a traceback (`cli/derived.py:162`). Use `parents=True`.
4. `pairs governance numer` exits 1, though `show` resolves case (`cli/query.py:205`). Use `resolve_ref`.
5. `pip install ./harness` leaves `build/` and `govharness.egg-info/` behind, and `.gitignore` does not cover them. Ignore both.

## Mutations

| # | Change | Result |
|---|---|---|
| 1 | named node sorts first | killed |
| 2 | title-holds-every-word key | killed |
| 3 | Terms ranked as prose | **survived** |
| 4 | locator in `WORD_RE` | killed |
| 5 | `names_below` ignores `#` | **survived** |
| 6 | ambiguous case takes the first match | **survived** (none in the corpus) |
| 7 | `items_below` does not recurse | **survived** |
| 8 | `CUT_MIN` ignored | **survived** |
| 9 | cut any overflowing prose | **survived** |
| 10 | fold drops "lead text" | **survived** |
| 11 | bad `GOVHARNESS_ROOT` falls back | killed |
| 12 | `run_find` uses `matches[0].held` | **survived** |
| 13 | orphans do not fail `--check` | killed |
| 14 | `entry()` drops the exit code | **survived** |
| 15 | env beats `--cache` | killed |
| 16 | no orphan scan in write mode | **survived** |

Mutations 13 and 16 need `../rendered` beside the copy.
