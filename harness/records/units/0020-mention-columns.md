# Unit 0020: the drafting checks read the cells of defining tables

The round of 2026-10-27 on defining tables (`review-records/round-2026-10-27-tables/`) amends STND.DRAFT to 1.6, with the term Mention column, and STND.DFLT to 1.5.3. This unit makes the harness follow it, closing item 7 of unit 0019, which left the cells of a table that a provision names in `defines` unread.

## Definition of done

1. `table_cells` reads each data cell of every table in a provision, a defining table included, other than a cell of a mention column, found by the headings that STND.DRAFT names in its section Representation in the harness; the header row of a defining table is data and is not read.
2. g.8 takes a listed verb alone, without terminal punctuation, for a label and not an imperative.
3. With the round applied, `verify`, `references --check`, and `compose --check` pass on the live corpus with no new defect, and the drafting standard passes its own checks with no new warning.
4. Each change has a test; every test passes; the README describes the change.

## Record

- 1, in `checks/drafting/tables.py` (`MENTION_COLUMNS`, `table_cells`). The logic checks keep `table_rows_kept` as it was: they classify authority tiers by wording, which STND.DRAFT does not govern, and a defining table holds no rule of conduct for them. Tests: `test_table_cells` now expects a used modal in a table of STND.DRAFT.17 to fail; `test_mention_columns` adds a column to the table of STND.DRAFT.17, which fails under the heading Note and passes under the heading Expression, and finds no quantifier in its column Word.
- 2, in `checks/drafting/context.py` (`is_imperative`). Test: `test_imperative_heuristic` keeps "Record." an imperative and adds "review" as a label.
- 3: the trial with the round applied finds no defect; its review notices are judged in `review-records/round-2026-10-27-tables/decisions.md`.

## Review

`review-records/harness/review-unit-0020.md`, by an agent of another configuration: no High finding; of four changes reverted one at a time, one survived (the header row of a defining table read).

- M1, fixed: `test_mention_columns` adds a heading that holds a modal to the table of STND.DRAFT.17 and expects no finding; with the header row read again, it fails.
- M2, fixed: a cell beyond the width of the header is read, as before the unit.
- L1, fixed: the header row of a table that no provision names in `defines` is read whole, as before, mention columns included.
- L2, fixed: a lone listed verb is imperative when its terminal punctuation stands before closing quotation marks or parentheses; "Record!" and 'Record."' are imperative, "Record?" is a question. The test pins each.
- L3, fixed: the line length and the annotation of `out`.
