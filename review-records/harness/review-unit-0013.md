# Review of unit 0013 (commit b1fce24)

Verdict: accept. No High or Medium finding; three Low findings.

## Held

- **Live corpus.** `verify` on `harness/governance` passes, and its output is identical to main's (e4af2ae), including the one g.18 warning. `check --out-dir` gives identical stdout and report files on both trees, with g.25 `[PASS]`. `references --check` prints `references: PASS` and `compose --check` prints `stale: 0` on both. `harness/governance` is byte-identical to main's.
- **Wrapper against the old script at entry 147 (6943e9a).** The old script reports 16 documents. The new wrapper, run on that corpus, reports the same 16 with the same names for each; only wording and order differ. It checks 47 documents against 48 (the stub STND), as the record says. On the live corpus: 0 with missing rows, rc 0.
- **Suite.** 260 tests, OK (240 s). `tests.test_architecture` and `tests.test_conventions` pass. `ruff check` on the four changed files is clean.
- **Record and README** agree with the code (pattern, skip order, LVL1 to LVL3, 47 versus 48, the g.25 row).

## Name detection (scratch copy, STND.CLASS, name HDES)

- Not read, as intended: inside a word (XHDES, HDESX, aHDES, HDES1x), lowercase, straight and curly quotes, inline code, fenced code, a Revision History row, a References row, an Example table (header rule), the word LVL0, and all text of LVL0 documents.
- Read, as intended: end of sentence ("See HDES."), heading, bold, list item, a table cell outside an Example table, provision Notes, "HDES's", "HDES-style", "(see HDES)" and "(HDES, HW)" (not citations under `DOCUMENT_IN_PARENS_RE`).
- Counted as a citation: "HDES.14", "(HDES)", "(HDES.FPGA)". g.25 then reports only a missing row, never an uncited name, which is consistent with the derivation.
- Two quoted spans on a line hide only their own text. An unclosed or multi-line quote hides nothing.
- A document is judged per document, not per occurrence: a name passes when any text of the document cites it. This is inherited from the old script.

## Findings

### Low 1: an unknown or out-of-scope DOC argument is dropped silently
`tools/check_refs.py` lines 47 to 49. `check_refs.py governance HDES CPS XXX` prints "checked 2 documents; 0 with missing rows", rc 0. A typo, or a DOC at LVL0 or of no level, reads as a pass. The old script checked an LVL0 document or raised.
Fix: after computing `subjects`, print any DOC not in `subjects` to stderr and exit 2.

### Low 2: two skip rules are not pinned by a test
Mutations of a copy of `citations.py`, each run against `tests/checks/test_references.py`:
- Not caught: reading the References section (`naming_text`, `without_section`). It is nearly equivalent, since a row naming an uncited document already fails as "not cited".
- Not caught: deciding the Example skip on any row instead of the header (`without_example_tables`, `skipping = EXAMPLE_COLUMN in cells`). The record calls this a deliberate difference from the old script, but no test fixes it.
Caught: no bare names read, Revision History read, Example tables read, quotes read, inline code read, fenced code read, all levels read, LVL0 counted, self-name counted, longest run lost, lookbehind lost, g.25 not failing on an uncited name.
Fix: add a References-row case and a "Example only in a later row" case to `test_mentions_are_ignored`.

### Low 3: the draft path is untested
Record and README say a bare name is listed, not failed, in a draft. No test covers it. My scratch draft was also inconsistent (status v.2 and ledger), so g.25 failed there and the result is inconclusive.
Fix: a test with a draft subject asserting the listed severity, or a line in the record saying the path is inherited from the severity model and untested here.

## Notes (no action)

- NAME_RE also reads link paths ("../HDES/_doc.md", "HDES.md"), single-quoted words, HTML comments, and indented or tilde code blocks. The corpus holds none; the direction is fail-closed.

## Scratch

/tmp/claude-1000/review-0013/ (`probe.py`, `probe2.py`, `mut1.sh`, outputs). A temporary git worktree used for the old corpus was removed.
