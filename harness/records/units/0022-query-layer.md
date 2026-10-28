# Unit 0022: the harness as an optional query layer

The deep review of 2026-10-28 (`review-records/deep-review-2026-10-28/harness.md`) judged the harness as an optional, lightweight, read-only query layer for an agent in a CSQ3 or CSQ4 project, and found its weakness at the surface an agent touches: the ranking of `find` and `context`, no command that prints a document whole, no installation, a cache written to the home directory by default, and three exit codes for one error. This unit makes the changes the review's convenience-layer recommendations ask, other than the `onset` command (HR-3), which waits on a corpus decision, and the README restructuring, which another unit does.

## Definition of done

1. HR-1, ranking. `find` and `context` rank provisions, terms, entries, tags, and Terms sections above Notes and other prose sections; in `context`, a section larger than the budget is cut with a marker, not dropped. "python code CSQ3 project" and "remote write authorization" return provisions first.
2. HR-2, whole documents. `show ROOT DOC --all` prints each provision of a document whole, in order, under its heading; a document identifier given to `find` also matches its provisions by prefix.
3. HR-5, installation. `harness/pyproject.toml`, standard library only, Python 3.11 or later, the console script `govharness`, packages `govharness*`; `pip install --no-deps -e harness` and a `pipx`-style install work in a scratch venv. The root is optional on `show`, `find`, `context`, `pairs`, and `verify`: `$GOVHARNESS_ROOT`, else `./governance` where it exists, else exit 2 with one line naming the variable. Each existing positional form still works.
4. HR-4, no writes by default. The solve cache is opt-in, through `--cache DIR` or `GOVHARNESS_CACHE`; the read-only commands write nothing anywhere by default. A test runs with an empty `HOME`.
5. HR-6, reading copies. `compose ROOT --all DIR [--check]` writes or checks a reading copy `<ID>.md` of every document, composed as the repository's `rendered/` was built by hand; `compose harness/governance --all rendered --check` from the repository root reports no stale copy.
6. HR-10, exit codes. Across `show`, `find`, `context`, and `pairs`: 0 when something was found, 1 for not found with the message on the standard error, 2 for a usage error; `show` resolves an identifier in the wrong case.
7. HR-11, shorter `show`. "Cited by" lists provisions, terms, entries, and tags one per line and folds the citing sections into one line per document, dropping none of what STND.HARN.1 asks for.
8. HR-13, dead code. `verify_snapshot`, `sentences_of`, `is_directory`, and `has_directory` are deleted, grep confirming that nothing calls them.
9. HR-14, fast tests. The docstring of `tests/__init__.py` names the directory it runs from; a fast subset under 10 s is documented as an exact command; `tests.test_conventions` covers any new top-level directory.
10. Each change has a test, and a scratch revert of each change alone makes a test fail. The full suite passes; `verify governance` passes as before, with the g.18 warning only; ruff adds no finding on the changed files. The README's command table rows and the sentences on what changed are updated, and the two unit 0018 leftovers of HR-7 are removed.

## Record

- 1, in `query/retrieval.py`: `kind_of` classes a node as `ITEM`, `TERMS`, or `PROSE`; `find` takes the most words held over the items alone, admits a Terms section or prose node that holds at least as many, and sorts by a node the query names, then a title holding every word, then kind, then words held, title hits, score, length, and identifier; `context` cuts a prose section larger than the whole budget with `cut_text`, a marker naming the characters shown and the `show` command, where at least `CUT_MIN` characters remain. `run_find` reports the best count held over every match. Tests: `test_provisions_rank_above_notes` (both queries, in force, a provision first and the prose after every item), `test_long_section_is_cut_not_dropped` (STND.CODE#notes at a budget of 3000, cut with the marker, and whole at 100 000). The cut is removed in the revision below (High 2).
- 2, in `query/retrieval.py`: `show(..., whole=True)` appends `block` of each item of `items_below`, which opens a held document such as a part of LVL0; `names_below` makes a document identifier in the query a title hit of each node below it, and `WORD_RE` keeps a locator whole so that `find STND.DFLT#terms` names its section. `cli/query.py` adds `--all`. Tests: `test_whole_document` (every provision of STND.PY in id order with its full text; a provision alone gains nothing), `test_document_identifier_matches_its_provisions`, and `test_show_all_prints_the_provisions` in `tests/cli/test_main.py`.
- 3, `pyproject.toml` (setuptools, `requires-python = ">=3.11"`, no dependency, `govharness = "govharness.cli.main:entry"`, packages `govharness*`); `cli/main.py` adds `entry`, which `__main__.py` calls. Checked in two scratch venvs under `/tmp/claude-1000/` on a copy of `harness/`: `pip install --no-deps -e` and a plain `pip install --no-deps` (what `pipx` does in its own venv); from `/`, `govharness show GOV.38`, `govharness find remote write`, and `govharness verify --no-logic` run with `GOVHARNESS_ROOT` set, and without it `show` exits 2 with the one line `show: no corpus root: give ROOT, set GOVHARNESS_ROOT, or run where ./governance exists`. Nothing was installed into the user's environment. The root: `cli/arguments.py` holds `default_root` and `split_root`; the root is `nargs="?"` on the five commands, and for `find` and `context` the first positional argument is the root only where a directory of that name exists (narrowed to a directory holding a corpus in the revision below, High 1). `cli/arguments.py` is the one CLI module that reads the environment; `tests/test_architecture.py` and decision 0001 record the adjustment. Tests: `DefaultRoot` in `tests/cli/test_main.py` (the variable, `./governance`, no root, a variable naming no directory, `split_root`), and `test_given_root_must_be_a_directory`.
- 4, in `workflows/solve_store.py`: `ENV_DIRECTORY` is `GOVHARNESS_CACHE`; `default_directory` reads it alone; `open_store(directory)` returns `None` where neither the option nor the variable names a directory; `--no-cache`, `GOVHARNESS_NO_CACHE`, `XDG_CACHE_HOME`, and the `~/.cache` default are gone. `cli/main.py` has `--cache DIR` on `verify` and `check`. `tests/__init__.py` points `GOVHARNESS_CACHE` at a fresh directory so that the suite's verifications share solves. Tests: `test_precedence` (no cache by default, the option over the variable, an empty variable, `XDG_CACHE_HOME` ignored), and `test_verify_is_identical_cold_warm_and_without`, whose fourth run has an environment of `HOME` and `PATH` only, an empty home directory as the working directory, and asserts after `verify`, `show`, `find`, `context`, and `pairs` that the home directory is still empty. Unit 0011's record carries a revision note.
- 5, in `derive/reading_copy.py`: `all_reading_copies` composes `ReadingCopy(ID, ID + ".md")` for every `_doc.md` of the corpus view (71 documents; the project template is not a document of the corpus); `cli/derived.py` takes `--all DIR` and, with `--check`, lists the stale copies by name. From the repository root, `python3 -B -m govharness compose harness/governance --all rendered --check` prints `stale: 0`: no committed copy differs, and none was rewritten. Tests: `test_compose_all_writes_every_document` (every document written, the check passes, an edited provision stales `STND.DFLT.md`, and `compose ROOT` alone is a usage error) and `test_repository_rendered_copies_are_current`.
- 6, in `cli/query.py`: `run_context` returns 1 with the message on the standard error where `context` returns nothing; `run_pairs` returns 1 for an unknown document; `resolve_ref` in `query/retrieval.py` resolves a reference that differs from one node only by case. Tests: `test_not_found_exits_one_on_stderr`, `test_show_resolves_case`, `test_case_insensitive_identifier`, and `test_nothing_found`.
- 7, in `query/retrieval.py`: `listing(..., fold=True)` keeps one line per item and adds one line per citing document naming its lead text and sections. `show STND.CLASS.10` went from 104 lines to 102, not to 62 as this record first said: forty documents cite it by their Notes alone, so a line per document saves almost nothing. The revision below folds by heading instead, to 65 lines (Medium 2). Test: `test_cited_by_folds_sections_by_document`, now `test_cited_by_folds_sections_by_heading` (STND.KNOW.4 and STND.PROJ.1 on their own lines, one `Notes of:` line naming STND.CODE and HDES, `Where the rest lives of: HDES`, no section locator in the list, and `Lead text of: VV` for PRIME.3).
- 8, deleted from `checks/verification.py`, `core/text.py`, and `core/corpus.py`, with the imports they alone used; `grep -rn` over `govharness/`, `tests/`, `tools/`, and `docs/` found each name only at its definition. The import test of `tests/test_architecture.py` and the whole suite cover the deletion.
- 9, `tests/__init__.py` says "Run from `harness/`" and names the fast subset; `tests/test_conventions.py` reads every top-level directory of `harness/` that holds a `.py` file, other than hidden directories and the build products of an installation, and `test_sources_cover_every_directory` checks that on a hand-made tree. The fast subset, `python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main tests.test_architecture tests.test_conventions`, runs in about 8 s.
- 10, below.

## Mutations

Each change was reverted alone on a scratch copy of `harness/` (the package and the tests copied, the corpus and `rendered/` linked), and the named test run there. Every revert fails its test. The first run of the table found one revert that survived, `all_reading_copies` restricted to the STND documents against `test_repository_rendered_copies_are_current`: a check that compares only the copies it composes cannot see a copy that is missing from the composed set. `compose --all --check` now also names a Markdown file of DIR that no document produces as an orphan and fails on it, and the revert fails.

| Change reverted | Test | Result |
| --- | --- | --- |
| 1, `find` takes `most` over every node and sorts without the kind | `test_provisions_rank_above_notes` | fails (2 failures) |
| 1, `context` names a long section instead of cutting it | `test_long_section_is_cut_not_dropped` | fails |
| 2, `show --all` appends nothing | `test_whole_document` | fails |
| 2, a document identifier matches nothing below it | `test_document_identifier_matches_its_provisions` | fails |
| 3, `GOVHARNESS_ROOT` is not read | `test_root_from_the_environment` | fails (5 failures, one per command) |
| 3, `./governance` is no default | `test_root_from_the_working_directory` | fails (5 failures) |
| 3, the first positional of `find` and `context` is always the root | `test_first_word_is_the_root_only_when_a_directory` | fails |
| 4, the `~/.cache` default returns | `test_verify_is_identical_cold_warm_and_without` | fails: the home directory is no longer empty |
| 4, the `~/.cache` default returns | `test_precedence` | fails |
| 5, `--all DIR` is ignored | `test_compose_all_writes_every_document` | fails |
| 5, `--all` composes the STND documents only | `test_repository_rendered_copies_are_current` | fails: 39 orphans |
| 6, `pairs` exits 2 and `context` prints "No item" to the standard output and exits 0 | `test_not_found_exits_one_on_stderr` | fails (2 failures) |
| 6, `show` is case-sensitive | `test_case_insensitive_identifier` | fails (KeyError) |
| 7, "Cited by" is not folded | `test_cited_by_folds_sections_by_document` | fails |
| 9, `test_conventions` reads a fixed list of directories | `test_sources_cover_every_directory` | fails |
| `cli/arguments.py` not admitted to the environment effect | `test_effects_are_confined` | fails |

Item 8 has no revert: putting a dead function back fails no test, by construction; the evidence is the grep. Item 3's `pyproject.toml` has no revert either; its evidence is the two installations above. The docstring of `tests/__init__.py` and the fast-subset command are text.

## Checks

- Tests: 200 in the full suite (183 before the unit), `python3 -B -m unittest discover -s tests -t .` from `harness/`, all passing in 339 s on the final code (341 s on a run before the orphan check of item 5 was added); the fast subset of 41 tests in about 8 s.
- `python3 -B -m govharness verify governance`: every section PASS, logic PASS, with the one warning `g.18 Atomicity: at most three modals per provision` as before; 3.8 s without a cache.
- `python3 -B -m govharness compose governance --all ../rendered --check` from `harness/` (the same as `compose harness/governance --all rendered --check` from the repository root): `stale: 0`, no orphan.
- Ruff, `--isolated --line-length 79`, on the twenty-two changed files against their copies at the previous commit: the same three findings before and after (`FURB167` in `core/text.py` and `tests/derive/test_reading_copy.py`, `SIM102` in `tests/test_conventions.py`), none new; `ruff format --check` passes on the changed files.
- The corpus `harness/governance/`, the ledger, the signature code, and the output of `pairs` are unchanged; no check's verdict changed.
- Not done: the `onset` command (HR-3), which waits on the custodian's answer to the review's question; the README restructuring (HR-8 and the agent section), left to another unit. HR-7's two leftovers are removed from the README.

## Revision after review

The cold review of the unit (`review-records/harness/review-unit-0022.md`, judged at e3dafe9) found two high, five medium, and five low findings, and ten of its sixteen mutants survived. One line per finding:

- High 1, the root argument: `split_root` in `cli/arguments.py` takes the first positional argument of `find` and `context` as the root only where that directory holds `LVL0/_doc.md` (`holds_corpus`); a word naming another directory, such as `tests`, stays a word. `test_first_word_is_the_root_only_when_a_corpus` runs both commands from a directory holding `tests/notes.md` with `GOVHARNESS_ROOT` set and gets what the positional form gets. `docs/operating.md` still says "where a directory of that name exists"; the docs are under another review, so that sentence is left to it.
- High 2, the cut: `cut_text` and `CUT_MIN` are deleted, and `context` names a text that does not fit, whatever its size, so STND.HARN.3 holds; the ranking of HR-1 (items, Terms sections, prose) is unchanged. `context governance remote write authorization --in-force` shows GUARD.10, .12, .13, and REPRO.12 again, at lines 55 to 73 of its output. `test_every_text_shown_is_whole` replaces `test_long_section_is_cut_not_dropped`: for four queries and budgets, the text before the names equals the blocks of the nodes it heads, joined, their lengths within the budget, with no marker; the four provisions are shown; STND.CODE#notes is named at a budget of 3000 and whole at 100 000. `docs/operating.md:29` still describes the cut; the docs are under another review, so that sentence is left to it.
- Medium 1, a cut of only the heading: falls away with the cut.
- Medium 2, the fold: `listing(fold=True)` folds the citing lead texts and sections into one line per heading, `Notes of: AGENT, CPS, …` and `Lead text of: VV`, the documents in id order; every provision, term, entry, and tag stays on its own line (STND.HARN.1). `show STND.CLASS.10`: 102 lines before, 65 after, measured with `wc -l`; the "62" of item 7 was wrong and is corrected above.
- Medium 3, `docs/installation.md`: not in this revision's scope; the docs are under another review.
- Medium 4, the README: the install text had already moved to `docs/installation.md` (dee64ca), which says `pipx install ./governance-harness/harness`. `harness/README.md` now says `pipx install ./harness` from the repository root, that a bare `harness` would name a package of the Python Package Index, that the installed package holds no corpus, and that `GOVHARNESS_ROOT` or a `ROOT` argument names a checkout of `governance/`; its `show` and `context` rows describe the fold by heading, `--all` on STND, and the whole-or-named rule. `grep -n 'no-cache\|~/.cache' harness/README.md` finds nothing.
- Medium 5, the tests: a test for each surviving mutant, in the table below. Mutant 6 has a fixture, `case_twins` in `tests/query/test_retrieval.py`: a corpus of one document holding GOV.1 and gov.1, where `resolve_ref` of `Gov.1` is `None` and `show` raises KeyError, while each exact identifier and `gov#TERMS` resolve.
- Low 1, `show STND --all`: `items_below` opens a held document only where the document's `parts` names it, as LVL0 names PRIME, and leaves out a document held by identifier alone, as STND holds each standard, since `show` names it under Holds. `show governance STND --all` prints 1474 bytes, the same as `show STND`; `show LVL0 --all` prints 198 blocks. `test_whole_document_opens_parts_only`.
- Low 2, E501: the line was the cut's marker and is gone with it. Ruff `--isolated --line-length 79` on the seven changed Python files finds the one `FURB167` of `tests/derive/test_reading_copy.py` that was there before; `--select E501` finds nothing; `ruff format --check` passes.
- Low 3, `compose --all a/b --write`: `folder.mkdir(parents=True, exist_ok=True)`; `test_compose_all_writes_every_document` writes into a directory two levels below an existing one.
- Low 4, `pairs numer`: `run_pairs` resolves the identifier with `resolve_ref`, as `show` does, and prints the resolved identifier; `test_show_and_pairs_resolve_case`.
- Low 5, `.gitignore`: `harness/build/` and `harness/*.egg-info/`.

### Mutations after the revision

Each mutant was applied alone to a fresh scratch copy of `harness/` under `/tmp/claude-1000/rev0022-fix/` (the package and the tests copied, the corpus and `rendered/` linked), and the named test run there. The first nine are the review's survivors, as the review described them (8 and 9 are the cut, which no longer exists), and the last five revert the fixes of this revision. Every one fails its test.

| # | Change | Test | Result |
| --- | --- | --- | --- |
| 3 | `kind_of` returns PROSE for a Terms section | `test_terms_sections_rank_between_items_and_prose` | killed: for "evidence level", STND.KNOW#terms is the first section only through its kind, the sixteenth without |
| 5 | `names_below` tests `word.` alone, not `word#` | `test_document_identifier_matches_its_provisions` | killed: STND.PY#notes not among the nodes below STND.PY |
| 6 | `resolve_ref` returns the first of several case matches | `test_ambiguous_case_is_not_resolved` | killed on the `case_twins` fixture |
| 7 | `items_below` does not recurse | `test_whole_document_opens_parts_only` | killed: `show LVL0 --all` lacks PRIME.1 |
| 7b | `items_below` opens every held document (the code before Low 1) | `test_whole_document_opens_parts_only` | killed: `show STND --all` opens the standards |
| 10 | the fold drops a citing lead text | `test_cited_by_folds_sections_by_heading` | killed: no `Lead text of: VV` under PRIME.3 |
| 12 | `run_find` reports `matches[0].held` | `test_best_hold_is_the_most_any_match_holds` | killed: "best hold 3" for "evidence level assignment reproducibility zyzzyva", where the Notes of STND.CXX hold 4 |
| 14 | `entry()` calls `main` without `sys.exit` | `test_entry_exits_with_the_code` | killed (2 failures: no SystemExit for either code) |
| 16 | the orphan scan runs under `--check` alone | `test_compose_all_writes_every_document` | killed: write mode prints no orphan |
| High 1 | a directory of any kind is the root | `test_first_word_is_the_root_only_when_a_corpus` | killed: `tests/` is read as the corpus |
| High 2 | `context` shows a text that does not fit, cut to what is left | `test_every_text_shown_is_whole` | killed (8 failures) |
| Medium 2 | the fold is one line per document | `test_cited_by_folds_sections_by_heading` | killed |
| Low 3 | `mkdir` without `parents` | `test_compose_all_writes_every_document` | killed (FileNotFoundError) |
| Low 4 | `pairs` takes the identifier as given | `test_show_and_pairs_resolve_case` | killed: `numer` exits 1 |

### Checks after the revision

- Tests: 205 in the full suite (200 before the revision), `python3 -B -m unittest discover -s tests -t .` from `harness/`, all passing in 346 s; the three targeted modules, `tests.query.test_retrieval`, `tests.cli.test_main`, and `tests.derive.test_reading_copy`, 42 tests in 11 s.
- `python3 -B -m govharness verify governance`: every section PASS, logic PASS, the one warning g.18 as before.
- `python3 -B -m govharness compose governance --all ../rendered --check`: `stale: 0`, no orphan.
- The corpus, the ledger, and `rendered/` are unchanged.
