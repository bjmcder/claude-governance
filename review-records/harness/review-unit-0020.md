# Review of unit 0020

## What I ran
- Read unit 0020, the round script (STND.DRAFT.3, term Mention column, MENTION_HEADINGS), and the diff 2dd11d0..HEAD.
- Probed `table_cells` and `is_imperative` directly on a scratch copy (/tmp/claude-1000/review-0020/base).
- Baseline with the round applied: drafting tests OK (13 tests).
- Four single reverts, each with the round applied, drafting tests:
  a. no mention-column exclusion: 5 failures (killed).
  b. defining tables unread again (old early return): test_mention_columns and test_table_cells fail (killed).
  c. header row of a defining table read: **all 13 tests pass (survives)**.
  d. lone listed verb always imperative: test_imperative_heuristic and test_clean_corpus_conforms fail (killed).

## High
None.

## Medium
1. tables.py:~287 (`table_cells`): a revert that reads the header row of a defining table survives. Definition of done 1 says the header is not read, and no test covers it. Fix: in `test_mention_columns` (or a new test) add a defining-table header cell that would fail g.5 (for example change the heading `Note` to `May not`) and assert PASS; the headings that are not mention columns (the new `Note` column) are the case.
2. tables.py:~286: cells beyond the header width are dropped. `| Word | Note |` with the row `| a | b | extra |` yields `['Note','b']`; "extra" was read before this change and is now unread, in defining and non-defining tables alike. The text says every data cell except those of named mention columns. Fix: also read `row[len(header):]` (a column with no heading is no mention column), and add a test with a long row.

## Low
1. tables.py:~285: for non-defining tables the header cells of mention columns (for example the heading `Modal`) are no longer read; before, every header cell was. Harmless for headings, but it is a change from "as before". Fix: for `(header, *rows)` iteration read the header row whole, applying the mention filter only to data rows, or say so in the docstring.
2. context.py:~438: `sentence.rstrip().endswith((".", "!"))` judges the raw string. `Record."` (closing quote after the period) and `Record)` return False; `Record "x"` (a lone verb followed by a quoted word, no period) was imperative and is now False; `Record?` was imperative and is now False. The stated change is only "a lone verb without terminal punctuation"; `?` is terminal punctuation (the standard's sentence end), so `Record?` arguably should keep its verdict. Verdicts observed: `Record!` True, `Record.` True, `record` False, `Record?` False, `Record` False, `Record "x".` True. Fix: test the end of `unquoted(sentence)` stripped of trailing quotes and brackets, and include `?`: `re.search(r"[.!?]\W*$", sentence)`; add `Record?` and `Record!` to the test lists (the tests cover only `Record.` and `review`, so `!` and `?` branches are unpinned: reverting `"!"` away would survive).
3. test_mention_columns: the docstring says "in a table that a provision names in defines" but the quantifier assertion `findings(lambda e: None, ...)` has no stated column; it passes also when Word is read, if the quantifier check ignores table_cells. Fix: confirm it fails under revert a (it did, via other tests), or assert against the Note variant.

## Edge cases (verified)
- Shorter row: cells missing in a mention column skipped without error.
- Duplicate headings (`Word`, `Word`): both excluded.
- Heading with spaces: stripped by `parse_tables`, matches.
- Fenced code table: removed by `FENCE_RE`, no cells.
- Header-only mention filter is case-sensitive and exact; a heading `word` is data.

## Style
Docstrings are numpydoc; the line `kept = [i for i, h in enumerate(header) if h.strip() not in MENTION_COLUMNS]` is 87 columns, longer than the surrounding 79 to 80; wrap it. `h.strip()` is redundant after `parse_tables`. `out` lacks an annotation (`out: list[str] = []`).
