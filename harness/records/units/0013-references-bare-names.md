# Unit 0013: References and bare document names

The check of References, g.25, compared each References table with the table derived from the document's citations: the identifiers and locators in its text, its provisions, and their reference fields, and a document identifier written alone in parentheses, such as `(AGENT)`. A document named by its bare identifier, as in "MEAS binds them" (CPS), was not read, so g.25 passed where `tools/check_refs.py` reported a gap (`review-records/round-2026-10-25-close/p5/gaps.md`). The closing round closed every such gap by a citation (ledger entries 148 to 175). The definition of done of 2026-10-25 (`review-records/round-2026-10-25-close/definition-of-done.md`, item 8) and the first item of `OPEN-ITEMS.md` ask that g.25 also read bare document names, so that the table and the check agree. It is a defect-class check, and `verify` passes on the live corpus. The scope is P5's, which the custodian accepted as decision 22 of `review-records/round-2026-10-25-close/decisions-final.md`:

- read only the documents that STND.DRAFT.34 asks to hold References, LVL1 to LVL3;
- leave out the Revision History, found by the harness's heading `core.tables.HISTORY_HEADING`;
- leave out every row of a table whose header names a column Example;
- leave out quoted spans and code spans.

## Definition of done

1. Under the design chosen, a bare document name with no row is caught: g.25 fails, class defect (design ii), or the row is derived (design i). The choice and its reason are recorded here.
2. A name inside a Revision History, a table with a column Example, a quoted span, or a code span is ignored.
3. A document of LVL0 is not read.
4. On the live corpus at entry 175, `verify` passes and `tools/check_refs.py` reports 0 documents with missing rows.
5. `tools/check_refs.py` is a thin wrapper of the harness check, or is retired in favor of `verify`. The commands that the briefs and records give for it still work, and `tools/round-brief-2026-10-25.md` says what it now is.
6. Each criterion has a test; every earlier test passes; ruff adds no finding on the changed files. The README's check table describes g.25. `harness/governance/` is unchanged.

## Record

- Design: (ii). The derivation stays as it is, and g.25 fails, class defect, when the text names a document by its bare identifier and does not cite it. The reasons:
  - STND.DRAFT.34 asks for a row for each cited document. The Terms of STND.DRAFT define Cited document as one named "in a citation or a reference field", and STND.DRAFT.20 says that a citation names a provision by its identifier or a section by its locator. A bare name such as "HDES" is neither. Under (i) the table would list documents that the text does not cite in the standard's sense, and g.25's "not cited" test would lose its meaning. Under (ii) the derived table keeps exactly the cited documents, and every bare name must be backed by a citation.
  - A bare name is not always a reference the document means to make. P5 found two cases where the row would have been false: HW.CPU and HW.EMBED named SIMPL in a sentence about the Articles their provisions instantiate, and none of those provisions instantiates SIMPL. The fix was to change the sentence (`p5/gaps.md`, rows HW.CPU, HW.EMBED, HW.GPU, HW.QPU). Under (i) the harness would have added the false row silently. Under (ii) it stops, and the author decides between a citation and a rewording.
  - The closing round closed all 16 gaps by citations, from which the rows were derived (decision 22). Design (ii) asks for the same fix, so it adds no new kind of edit.
  - No derived output changes by construction. On the live corpus `references --check` prints `references: PASS` and `compose --check` prints `stale: 0`, before and after the change.
- Done, in `checks/drafting/citations.py`:
  - `NAME_RE`, the bare identifier: two to five capitals, an optional digit, then dotted segments, not preceded by a letter, digit, or period and not followed by a letter or digit. The longest dotted run is taken, so "HDES.FPGA" names HDES.FPGA and not HDES. It is the pattern of `tools/check_refs.py`.
  - `without_example_tables` drops every line of a table whose first line, its header, has a cell `Example`. `tools/check_refs.py` started skipping at the first row with such a cell, header or not; the result is the same on the corpus, where the only such table is in STND.IDENT.
  - `naming_text` removes, in order, the References section (`derive.references.without_section`), the Revision History (`HISTORY_RE`, built from `HISTORY_HEADING`), tables of examples, fenced and inline code (`core.text.FENCE_RE` and `CODE_RE`), and quoted spans (`core.text.unquoted`, straight and curly quotes). Code goes before quotes, so a quote inside a code span cannot hide text after it.
  - `named_documents(corpus, doc_id)` returns the other documents a document names by bare identifier, in its own text and in that of its provisions and terms. It returns nothing for a document whose level is not LVL1 to LVL3, and it never counts the word LVL0, which names a level throughout the corpus (P5's rule 1).
  - `references_problem`, which g.25 and `references --check` share, now also reports the documents named and not cited: "text names X without a citation (cite a provision, or the document in parentheses)". Its earlier messages are unchanged when no bare name is uncited.
  - g.25 keeps its key, title, registration, severity model, and subjects: the documents below LVL0 in the groups `self`, `lower`, and `draft` (`units_for(BELOW, {"informative", "body"})`). The finding is a defect, so it fails in a document whose provision STND.DRAFT.34 binds, and is listed in a draft.
- Done, in `derive/references.py`: `members_of`, a document's entry and those of its directory, taken out of `cited_documents` so that both readings use the same entries. The derivation is otherwise unchanged.
- `tools/check_refs.py` is now a thin wrapper of g.25: it builds the drafting context, runs `references_listed`, and prints each finding as `DOC: reason` and the line `checked N documents; K with missing rows`, exiting 1 when it prints a finding. Its command line is unchanged, and DOC arguments still restrict the report. It reads the documents g.25 reads, so planned stubs are left out: it checks 47 documents on the live corpus where the old script checked 48, the one left out being STND, a planned stub with no text and no References. Unlike `verify`, it prints a finding in a draft too. The briefs and records name the script only in commands, which still work; `tools/round-brief-2026-10-25.md` and the repository README now say that it wraps g.25.
- Checked on the corpus before the round (commit 6943e9a, entry 147): `verify` fails on g.25 alone, and the wrapper reports the same 16 documents and names as P5's model `p5/check_refs_0013.py` (CPS, HDES, HDES.ASIC, HW and its five sub-profiles other than HW.ASIC, ML, STND.CLASS, STND.CODE, STND.DFLT, STND.IDENT, STND.KNOW, STND.MPI). On the live corpus: `verify` passes (the one warning is the g.18 notice the README names), `references --check` passes, `compose --check` finds no stale copy, and the wrapper reports 47 documents, 0 with missing rows.
- Tests, in `tests/checks/test_references.py`. STND.CLASS is the subject (adopted, binding under STND.DRAFT.34, and citing no HDES document); HDES is the name.
  - `test_precondition`: on the live corpus STND.CLASS neither cites nor names HDES.
  - `test_uncited_name_fails`: HDES named in the document's text, or in the text of STND.CLASS.1, fails g.25 with one finding of class defect that names it.
  - `test_citation_derives_the_row`: with the name cited as HDES.1 or as `(HDES)`, the derivation holds HDES, g.25 reports the missing row and no uncited name, and after the table is derived again g.25 passes.
  - `test_longest_name`: HDES.FPGA names HDES.FPGA, not HDES.
  - `test_mentions_are_ignored`: a name in a new Revision History row, a table with a column Example, straight and curly quotes, a code span, and a fenced block is not read, and g.25 passes. The same table with its column renamed is read and fails.
  - `test_lvl0_is_not_read`: names added to LVL0, PRIME (a part of LVL0), and MNEM (of no level) are not read; "below LVL0" names no document.
  - `test_live_corpus_passes`: on the live corpus every document g.25 reads cites each document it names, g.25 passes, and the wrapper, run as a program, exits 0 with "0 with missing rows".
- Mutations, each patched in turn into `citations.py` and checked against the test file. Each fails at least one test:
  - no bare names read: `test_uncited_name_fails`, `test_longest_name`, `test_mentions_are_ignored`;
  - Revision History read: `test_mentions_are_ignored` (revision history);
  - tables of examples read: `test_mentions_are_ignored` (example table), `test_live_corpus_passes` (STND.IDENT), and others;
  - quotes read: `test_mentions_are_ignored` (both kinds of quote);
  - inline code read, or fenced code read: `test_mentions_are_ignored` (code span, fenced code); inline code read also fails `test_live_corpus_passes`;
  - every level read: `test_lvl0_is_not_read` (LVL0, PRIME, MNEM);
  - LVL0 counted as a name: `test_lvl0_is_not_read` and `test_live_corpus_passes`.
- Suite: `cd harness && python3 -B -m unittest discover -s tests` ran 260 tests, OK (237 s). This unit adds seven, in `tests/checks/test_references.py`; no earlier test changed.
- Ruff 0.16.10, with the settings it resolves for the tree, reports no finding on `checks/drafting/citations.py`, `derive/references.py`, `tests/checks/test_references.py`, or `tools/check_refs.py`, and with `--line-length 79 --select E501` none on the first three. It reported one earlier finding on `citations.py`, FURB167 (`re.I`), which is fixed (`re.IGNORECASE`).
- README: the check table now has a row g.25 (and g.1 to g.24 for the rest of the drafting standard), and the row of `references` says that it reports uncited bare names and that `--write` cannot fix them alone. The decision records 0001 and 0002 do not describe g.25, so they are unchanged.
- Not changed:
  - The derivation of References, the reading copies, and `harness/governance/`.
  - `OPEN-ITEMS.md`, whose first item stays until the lead or the custodian closes it at merge.
- Open:
  - The informative text of STND.DRAFT (section on the harness, `_doc.md`) says that g.25 "compares each references table with the cited documents that `python -m govharness references` derives". That is still true, but it does not say that g.25 now also fails on an uncited bare name. An editorial amendment of STND.DRAFT could add it, for a later round; `harness/governance/` is out of this unit's scope.
  - The defect class rests on the reading that P5 and decision 22 gave STND.DRAFT.34, that a document named in the text is one the text cites, rather than on the words of STND.DRAFT.20 and the term Cited document alone. The parenthesized form `(HDES)`, which the harness has counted as a citation since before this unit, is likewise not literally a provision or a section. Whether the Terms should say so is for the custodian.
  - A document named by description, such as "the standard for building software", is still not read (`review-records/round-2026-10-24/verify-final-stdc-rust-ftn-round.md`).
- Audit:
  1. Met: design (ii), recorded above; `test_uncited_name_fails`.
  2. Met: `test_mentions_are_ignored`.
  3. Met: `test_lvl0_is_not_read`.
  4. Met: `test_live_corpus_passes`, and the runs above.
  5. Met: `tools/check_refs.py`, `test_live_corpus_passes`, `tools/round-brief-2026-10-25.md`, and the repository README.
  6. Met: see the tests, mutations, suite, ruff, and README items above; `git diff` shows no change under `harness/governance/`.

## Review

Left to the reviewer.
