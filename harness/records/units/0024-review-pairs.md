# Unit 0024: the narrowed review pairs, a drafting table held by a cited provision, and b.5

Ruling E1 of the deep review of 2026-10-28 (`review-records/deep-review-2026-10-28/rulings.md`, option (a)) narrows the pairs that STND.HARN.28 lists for review to those that rest on a shared matter, plus those whose two provisions are in documents that the change touches (HR-12 of `review-records/deep-review-2026-10-28/harness.md`). Round e (`review-records/rounds-2026-10-28/round-e/decisions.md`) drafts the narrowed STND.HARN.28; under R6.4 (CP26) it moves the spelling table of STND.DRAFT.33 into STND.DOCS.8; and under R6.1 (CC23) it drops the last sentence of GOV.48, on agents granting themselves waivers, which PRIME.1 holds. This unit makes `pairs` follow the drafted STND.HARN.28, lets the drafting check of American spelling (g.22) read its table where STND.DRAFT.33 cites it, and lets the logic check b.5 read the bar on a self-granted waiver from PRIME.1 where GOV.48 no longer states it. Nothing in the live corpus changes, and no verdict of `verify` on it changes: `pairs` is a query, not a check; on the live corpus STND.DRAFT.33 still holds its table, and b.5 still reads GOV.48.

## Definition of done

1. `review_pairs` puts on the changed side each provision of a document named, each provision named, and, for a change of LVL0, each provision below LVL0 that instantiates a LVL0 provision the change amends. A pair joins provisions of two documents, at least one a profile or sub-profile, and is listed on a shared matter as before, or on a common instantiation only where both provisions lie in documents that the change touches: documents named, or the documents of provisions named. A provision reached only through `--amends` pairs on shared matters alone, so a change of LVL0 alone lists only such pairs.
2. `pairs [ROOT] ID [--with ID ...] [--amends LVL0_ID ...]`: `--with` names the other documents, or provisions, of the same change. Each `ID` names a document or a provision below LVL0, or a LVL0 document (an article) given with `--amends`; each `--amends` identifier names a LVL0 provision. Anything else exits 1 with one line on the standard error, and so does a change that lists no pair, as `docs/operating.md` states for every query. `--with` and `--amends` take one or more identifiers each and may precede `ID`.
3. The drafting tables of STND.DRAFT are read from its provisions and, for a table name the harness knows, from a provision of another document that a provision of STND.DRAFT refers to; g.22 reads the spelling table from STND.DOCS.8 once round e is applied, and from STND.DRAFT.33 on the live corpus.
4. b.5 reads the bar on a self-granted waiver from GOV.48, citing the waiver clause, where GOV.48 states it, and otherwise from the reservation of PRIME.1, which names waivers among the acts that an agent never performs.
5. Tests for each change; the architecture and conventions tests pass; the README row of `pairs` and the row of the skill `consulting-governance` describe the command.

## Record

- 1, in `query/combination.py`, `review_pairs(corpus, changed, amends)`: `changed` is a document identifier, as before, or a tuple of document and provision identifiers. The common-instantiation basis is added to a pair only where `doc_of[first]` and `doc_of[second]` are both touched documents. The first draft tested `doc_of[second]` alone, so a provision reached only through `--amends` paired with every provision of every touched document (code review, Should-fix 1); the round's own listing held fifteen such pairs.
- 2, in `cli/query.py`, `run_pairs` checks each identifier after `resolve_ref` (so the case of a document identifier does not matter), refusing an unknown identifier, a LVL0 provision given as `ID`, a LVL0 article given without `--amends`, and an `--amends` identifier that is not a LVL0 provision; an empty listing prints nothing on the standard output and exits 1 (code review, Should-fix 2 and 3). `pairs QA --amends QA.11`, which round c ran, now exits 1, since it lists no pair. The heading names every document and provision; `cli/main.py`'s command list names `--with`.
- 3, in `checks/drafting/tables.py`, `cited_tables` returns the pairs of a provision outside STND.DRAFT and a name of `TABLE_SPECS` that it defines, for each provision that a provision of STND.DRAFT refers to; `read_standard_tables` adds them to the holders. An unknown table name of a cited provision, such as `american-usage` of STND.DOCS.8, is not reported, since the table belongs to that document. The pickup is by name alone, which the module docstring says. The guard against a duplicate holder could never fail and is gone (code review, Optional 2).
- 4, in `checks/logic/facts.py`, the role `owner` (PRIME.1, "Accountable owner"); in `checks/logic/authority.py`, `self_grant` reads each prohibition from the first of its homes that states it: the waiver from GOV.48 citing GOV.44, else from PRIME.1; the authorization from PRIME.7 as before. On the live corpus the first home holds, so the verdict and its detail lines are unchanged.
- 5, `tests/checks/test_combination.py`: `test_pairs_of_one_document_rest_on_a_matter`, `test_common_instantiation_only_within_the_change`, `test_named_provision_alone_on_the_changed_side`, `test_amended_lvl0_provision_pairs_by_matter`, `test_lvl0_amendment_adds_no_pair_outside_the_change` (NUMER and HW with VV.1 amended: a pair on a LVL0 basis has both provisions in NUMER or HW, none a sub-profile reached through VV.1, and none rests on a provision of GOV or PRIN; NUMER with VV.1, 344 pairs), `test_document_in_draft_keeps_its_pairs` (NUMER set to draft keeps 92 pairs, and NUMER.11 with HW.16 its 39), and `test_pairs_need_a_profile`. `test_pairs_match_the_numer_review`, which compared the listing with the 61 pairs listed by hand under the old rule, is gone. `tests/cli/test_main.py`: `test_pairs_with_other_documents_of_the_change` and `test_pairs_refuses_what_it_does_not_take` (the six refusals, `LVL0 --amends VV.1` with 339 pairs, and `--with` before the positionals). `tests/checks/test_drafting.py`: `test_spelling_table_in_a_cited_provision` (the table moved in memory, g.1 and g.22 pass, `cited_tables` returns exactly STND.DOCS.8's table, a British spelling fails g.22, and the move without the citation fails g.1). `tests/checks/test_logic.py`: `test_waiver_self_grant_read_from_prime_1` (GOV.48's sentence dropped: b.5 passes; PRIME.1's waivers dropped too: b.5 fails); the existing case on GOV.48 citing GOV.999 still fails b.5.

Pair counts before and after, from `harness/governance` (the live corpus) and, for the round, the kept copy with rounds a, d, c, o, and e applied:

| Change | Before (rule in force) | After (drafted rule) |
| --- | --- | --- |
| NUMER alone | 4,384 | 92 |
| HW alone | 2,302 | 128 |
| HDES alone | 2,343 | 137 |
| STND.VVUQ alone | 4,921 | 0 (exit 1) |
| AGENT alone | 706 | 0 (exit 1) |
| STND.CODE alone | 166 | 0 (exit 1) |
| NUMER with HW | — | 345 |
| NUMER.11 alone | — | 6 |
| LVL0, amending VV.1 | 12,185 | 339 |
| NUMER, with VV.1 amended | — | 344 |
| Round e, its 23 added or amended provisions and five amended LVL0 provisions | 20,343 in the per-document listings of its 33 documents and of LVL0, 369 of them with a changed provision | 44 |

NUMER lists 92 pairs on a shared matter, not the 19 that HR-12 counted: HR-12 counted the pairs whose only basis is a matter, and 73 pairs rest on a matter and on a common LVL0 provision as well. The ruling's words reach every pair on a shared matter. The code review counted 42 pairs for the round before GOV.48 was amended; AGENT.11 and STND.DOCS.10 instantiate GOV.48 and add one pair each.

## Mutations

Each change was reverted alone on a scratch copy of the package under `/tmp/claude-1000/round-e/mut/`, the corpus linked, and the named test run there.

| Change reverted | Test | Result |
| --- | --- | --- |
| the common LVL0 basis added to every pair, as before | `tests.checks.test_combination` | fails (18,376 failures) |
| the touched document tested on the other provision alone (the first draft) | `tests.checks.test_combination` | fails (4,722 failures) |
| a named provision not put on the changed side | `tests.checks.test_combination` | fails |
| the document of a named provision not counted as touched | `tests.checks.test_combination` | fails |
| `others` without the touched documents not in force | `tests.checks.test_combination` | fails |
| the shared-matters tables of touched documents not in force dropped | `tests.checks.test_combination` | fails |
| GOV and PRIN bases paired | `tests.checks.test_combination` | fails (4 failures) |
| `--with` ignored | `test_pairs_with_other_documents_of_the_change` | fails |
| a LVL0 article admitted without `--amends` | `test_pairs_refuses_what_it_does_not_take` | fails |
| an empty listing exits 0 | `test_pairs_refuses_what_it_does_not_take` | fails (2 failures) |
| an `--amends` that names no LVL0 provision accepted | `test_pairs_refuses_what_it_does_not_take` | fails (2 failures) |
| no table read from a cited provision | `test_spelling_table_in_a_cited_provision` | fails (error) |
| citers scanned outside STND.DRAFT | `test_spelling_table_in_a_cited_provision` | fails (error) |
| b.5 takes the first home whether or not it states the bar | `test_waiver_self_grant_read_from_prime_1` | fails |

Equivalent mutants, which the code review found and no test can kill: requiring both provisions of a pair to be profiles (no listed pair on the live corpus joins a profile to a standard on the rows that the mutant changes), and skipping a reference inside STND.DRAFT in `cited_tables` (no provision of STND.DRAFT defines a table that another provision of it cites). The second guard that the review named is deleted.

## Checks

- Targeted: `tests.checks.test_combination` (11 tests), `tests.cli.test_main`, `tests.checks.test_drafting`, and `tests.checks.test_logic` pass; the fast subset `python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main tests.test_architecture tests.test_conventions` passes. ruff, at the line length of the package (79), adds no finding on the changed files; the four it reports in `authority.py` and `facts.py`, and two long lines of `test_drafting.py`, predate the unit.
- `python3 -B -m govharness verify governance`: as before, every check PASS with the one g.18 warning.
- Round e rehearsed on rounds a, d, c, and o: every check PASS, with the one g.18 warning that the corpus carries; g.22 reads the table from STND.DOCS.8, and b.5 reads PRIME.1.
- The unit touches `query/combination.py`, its CLI wiring, and its tests, and goes further in two places, `checks/drafting/tables.py` and `checks/logic/authority.py` with `facts.py`, because the round moves a table that a drafting check reads and drops a sentence that a logic check read; round e's record says so.
