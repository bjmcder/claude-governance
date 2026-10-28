# Unit 0024: the narrowed review pairs, and a drafting table held by a cited provision

Ruling E1 of the deep review of 2026-10-28 (`review-records/deep-review-2026-10-28/rulings.md`, option (a)) narrows the pairs that STND.HARN.28 lists for review to those that rest on a shared matter, plus those whose two provisions are in documents that the change touches (HR-12 of `review-records/deep-review-2026-10-28/harness.md`). Round e (`review-records/rounds-2026-10-28/round-e/decisions.md`) drafts the narrowed STND.HARN.28 and, under R6.4 (CP26), moves the spelling table of STND.DRAFT.33 into STND.DOCS.8. This unit makes `pairs` follow the drafted STND.HARN.28 and lets the drafting check of American spelling (g.22) read its table where STND.DRAFT.33 cites it. Nothing in the live corpus changes, and no verdict of `verify` on it changes: `pairs` is a query, not a check, and on the live corpus STND.DRAFT.33 still holds its table.

## Definition of done

1. `review_pairs` puts on the changed side each provision of a document named, each provision named, and, for a change of LVL0, each provision below LVL0 that instantiates a LVL0 provision the change amends. A pair joins provisions of two documents, at least one a profile or sub-profile, and is listed on a shared matter as before, or on a common instantiation only where the other provision lies in a document that the change touches: a document named, or the document of a provision named. A change of LVL0 alone touches no document below LVL0, so its pairs rest on shared matters.
2. `pairs [ROOT] ID [--with ID ...] [--amends LVL0_ID ...]`: `--with` names the other documents, or provisions, of the same change; an unknown identifier exits 1, as `ID` does. A single `ID` works as before.
3. The drafting tables of STND.DRAFT are read from its provisions and, for a table name the harness knows, from a provision of another document that a provision of STND.DRAFT refers to; g.22 reads the spelling table from STND.DOCS.8 once round e is applied, and from STND.DRAFT.33 on the live corpus.
4. Tests for each change; the architecture and conventions tests pass; the README row of `pairs` describes the command.

## Record

- 1, in `query/combination.py`, `review_pairs(corpus, changed, amends)`: `changed` is a document identifier, as before, or a tuple of document and provision identifiers. The common-instantiation basis is added to a pair only where `doc_of[second]` is a touched document. Docstrings of `review_pairs` and `Pair` state the rule.
- 2, in `cli/query.py`, the option `--with` (`dest="also"`), each identifier resolved as `ID` is (so the case of a document identifier does not matter), the heading naming every document and provision; `cli/main.py`'s command list names the option.
- 3, in `checks/drafting/tables.py`, `cited_tables` returns the pairs of a provision outside STND.DRAFT and a name of `TABLE_SPECS` that it defines, for each provision that a provision of STND.DRAFT refers to; `read_standard_tables` adds them to the holders. An unknown table name of a cited provision, such as `american-usage` of STND.DOCS.8, is not reported, since the table belongs to that document.
- 4, `tests/checks/test_combination.py`: `test_pairs_match_the_numer_review`, which compared the listing with the 61 pairs listed by hand under the old rule at the adoption of NUMER 1.0, is replaced by `test_pairs_of_one_document_rest_on_a_matter` (the pairs of NUMER alone are those that the shared-matters tables give, derived in the test from the tables), `test_common_instantiation_only_within_the_change` (NUMER with HW adds pairs, none of which reaches a third document on a LVL0 basis, and the order of the documents does not matter), `test_named_provision_alone_on_the_changed_side` (NUMER.11 alone lists a subset of the pairs of NUMER, each holding it; with HW.16 its common partners lie in NUMER and HW), and `test_amended_lvl0_provision_pairs_by_matter` (a change of LVL0 that amends VV.1 lists only pairs on a shared matter, each with a provision instantiating VV.1); `test_pairs_need_a_profile` stays. `tests/cli/test_main.py`: `test_pairs_with_other_documents_of_the_change`. `tests/checks/test_drafting.py`: `test_spelling_table_in_a_cited_provision` (the table moved in memory to STND.DOCS.8, g.1 and g.22 pass, and a British spelling in STND.DRAFT.2 fails g.22).

Pair counts before and after, from `harness/governance` (the live corpus) and, for the round, the kept copy with rounds a, d, c, o, and e applied:

| Change | Before (rule in force) | After (drafted rule) |
| --- | --- | --- |
| NUMER alone | 4,384 | 92 |
| HW alone | 2,302 | 128 |
| HDES alone | 2,343 | 137 |
| STND.VVUQ alone | 4,921 | 0 |
| AGENT alone | 706 | 0 |
| STND.CODE alone | 166 | 0 |
| NUMER with HW | — | 345 |
| NUMER.11 alone | — | 6 |
| LVL0, amending VV.1 | 12,185 | 339 |
| Round e, its 23 added or amended provisions and four amended LVL0 provisions | 17,829 in the per-document listings of its 27 documents and of LVL0, 344 of them with a changed provision | 56 |

NUMER lists 92 pairs on a shared matter, not the 19 that HR-12 counted: HR-12 counted the pairs whose only basis is a matter, and 73 pairs rest on a matter and on a common LVL0 provision as well. The ruling's words reach every pair on a shared matter.

## Mutations

Each change was reverted alone on a scratch copy of the package under `/tmp/claude-1000/round-e/mut/`, the corpus linked, and the named test run there.

| Change reverted | Test | Result |
| --- | --- | --- |
| the common LVL0 basis added to every pair, as before | `tests.checks.test_combination` | fails (18,376 failures) |
| the partner of a common instantiation taken from the changed side, so the instantiators of an amended LVL0 provision pair with each other | `tests.checks.test_combination` | fails (9,170 failures) |
| a named provision not put on the changed side | `tests.checks.test_combination` | fails |
| the document of a named provision not counted as touched | `tests.checks.test_combination` | fails |
| `--with` ignored | `test_pairs_with_other_documents_of_the_change` | fails |
| no table read from a cited provision | `test_spelling_table_in_a_cited_provision` | fails (error) |

## Checks

- Targeted: `tests.checks.test_combination` (9 tests), `tests.cli.test_main`, and `tests.checks.test_drafting` pass; the fast subset `python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main tests.test_architecture tests.test_conventions` passes.
- `python3 -B -m govharness verify governance`: as before; `pairs` is no check, and the live STND.DRAFT.33 still holds its table.
- Round e rehearsed on rounds a, d, c, and o: every check PASS, with the one g.18 warning that the corpus carries; g.22 reads the table from STND.DOCS.8.
- The unit touches `query/combination.py`, its CLI wiring, and its tests, and goes further in one place, `checks/drafting/tables.py`, because the round moves a table that a drafting check reads; round e's record says so.
