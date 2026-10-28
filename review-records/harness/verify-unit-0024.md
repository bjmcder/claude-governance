# Cold verification of unit 0024 as revised (d1778f9, dae121c)

Reviewer: another configuration. Runs on the working tree at dae121c and on copies under `/tmp/claude-1000/rv24b/`, offline; the package of e0595e9 (before the unit) exported with `git archive` for comparison.

## What I ran

- `verify governance` on the live corpus: byte-identical to the output of 051bde6, which is byte-identical to that of e0595e9 (every check PASS, the one g.18 warning). `check governance --out-dir`: standard output identical; `logic_facts.json` and `logic_report.md` differ only by the new role line `owner: PRIME.1 (configured)`; b.5's detail lines are unchanged (`GOV.48: 1 sentence(s) cite ['GOV.44']`, `PRIME.7: 1 sentence(s) cite []`). No verdict changes.
- Rounds a, d, c, o, e re-applied to a fresh copy with the revised scripts (ledger 272 entries, `seq 321 STND.PY 1.5` last): `verify` with dae121c every check PASS, the g.18 warning only. With e0595e9 `logic: FAIL (3)`: b.5 (`GOV.48: 0 sentence(s) cite []`), g.1, g.23. On the copy GOV.48 ends at "for every action", and b.5 with dae121c reports `PRIME.1: 1 sentence(s) cite ['GOV.41', 'GOV.41', 'GOV.50']`: the bar is read from PRIME.1's "granting authorizations and waivers" because GOV.48 no longer states it, which is the right reason. `cited_tables` on the copy: `{("STND.DOCS.8", "spelling")}`; g.22 reads the table there.
- Round e as one change on the copy, `pairs COPY STND.HARN.24 --with <the 22 other provisions> --amends GOV.11 GOV.24 GOV.48 GUARD.4 GUARD.15`: 44 pairs, the rows of `round-e/pairs-changed.md`; without GOV.48 among the amendments, 42, my earlier count. The two added are (AGENT.11, STND.PROJ.3) on GUARD.12 and (STND.DOCS.10, AGENT.25) on INTPR.12: AGENT.11 and STND.DOCS.10 instantiate GOV.48, and both provisions of each lie in documents of which the round amends a provision, so the revised rule lists them. Three pairs of the 44 hold no provision the round changes, those two and (STND.DRAFT.42, AGENT.15) on GUARD.3, and `pairs-changed.md:7` now says so. Per document on the copy: NUMER 92, HW 128, HDES 137; STND.VVUQ, AGENT, STND.CODE exit 1 with `pairs: no pair to review before a change of ...`. The record's 369 and 20,343 under the rule in force were not reproduced.
- Live corpus counts with dae121c: NUMER with HW 345, NUMER with VV.1 amended 344 (the record's table). The reading of 051bde6 gave 3,782 for the latter.
- Exit codes on the live corpus, each with nothing on the standard output and one line on the standard error, exit 1: `VV.1` and `STND` and `LEX.1` ("is not a document or provision below LVL0"), `GOV` and `LVL0` ("is a LVL0 document, given without --amends"), `NUMER --amends NOPE` ("--amends NOPE is not a LVL0 provision"), `STND.VVUQ`, `STND.HARN.28`, `QA --amends QA.11`, and `LVL0 --amends GOV.11` ("no pair to review before a change of ..."). `LVL0 --amends VV.1` exits 0 with 339 pairs; `pairs --with HW -- governance NUMER` lists the 345 of `NUMER --with HW`; without the `--`, a usage error, exit 2, as `argparse` has it. These match `docs/operating.md:34` (0 when something was found, 1 when nothing was, with the message on the standard error, 2 for a usage error) and the README row.
- Tests: `tests.checks.test_combination` (11), `tests.cli.test_main`, `tests.checks.test_drafting`, `tests.query.test_retrieval`, `tests.test_architecture`, `tests.test_conventions`: 73 OK in 125 s; `test_waiver_self_grant_read_from_prime_1` and `test_clean_corpus_has_no_failure` OK in 10 s; `test_mutations_are_caught` OK under each surviving mutant below (73 s each). Ruff at the repository's defaults: the two ISC004 findings at `authority.py:168` and `:170` predate the unit; at 79 columns with E501, `tests/checks/test_drafting.py:901`, `:905` (the two of the review, shifted) and `tests/checks/test_logic.py:371` (80 columns, new).
- Mutants on a copy of the package (table). The five survivors of the review (touched documents not in force dropped from the other side and from the matters tables; GOV and PRIN bases pairing; references inside the standard not skipped; citers scanned outside the standard) are all killed now, by `test_document_in_draft_keeps_its_pairs`, `test_lvl0_amendment_adds_no_pair_outside_the_change`, and the two added assertions of `test_spelling_table_in_a_cited_provision`.

## Findings

No finding. Two cosmetic notes, no action asked: b.5's detail line on the copy lists GOV.41 twice, since PRIME.1's sentence cites it twice and `ids_in` keeps repeats; `tests/checks/test_logic.py:371` is one column over 79.

## Mutations

Each applied alone to a copy of the package under `/tmp/claude-1000/rv24b/mut/`, the named tests run there.

| Change | Test | Result |
| --- | --- | --- |
| `others` drops touched documents not in force | `test_combination` | killed, `test_document_in_draft_keeps_its_pairs` |
| matters tables of touched documents not in force dropped | `test_combination` | killed, same |
| GOV and PRIN bases pair | `test_combination` | killed (4), `test_lvl0_amendment_adds_no_pair_outside_the_change` |
| common basis on every pair (rule in force) | `test_combination` | killed (31,232) |
| only the other provision's document tested (the first draft) | `test_combination` | killed (4,722) |
| only the changed-side provision's document tested | `test_combination` | killed (12,819) |
| either document touched | `test_combination` | killed (12,819) |
| references inside the standard not skipped | `test_spelling_table_in_a_cited_provision`, `test_clean_corpus_conforms` | killed (2) |
| citers scanned outside the standard | same | killed |
| cited holder appended twice | same | killed |
| `--with` ignored; unknown identifier admitted | `test_pairs_with_other_documents_of_the_change`, `test_show_and_pairs_resolve_case`, `test_pairs_refuses_what_it_does_not_take` | killed (2) |
| empty listing exits 0; `--amends` not validated; a LVL0 provision admitted as `ID`; a LVL0 article admitted without `--amends`; any document admitted as `ID` | same | killed (5), `test_pairs_refuses_what_it_does_not_take` |
| b.5 fallback home removed | `test_waiver_self_grant_read_from_prime_1`, `test_clean_corpus_has_no_failure`, `test_mutations_are_caught` | killed |
| fallback requires the waiver clause too | same | killed |
| no break: sentences of every home kept | same | killed, `test_mutations_are_caught` (self-grant cites nothing that resolves) |
| homes in the wrong order, PRIME.1 first | same | killed, same |
| fallback pattern loosened to `waiver` | same | survived, equivalent: PRIME.1 holds the word once, and the test removes it |
| fallback added to the authorization group | same | survived, equivalent: PRIME.7 holds its sentence |
| `owner` hint names GOV.48 | same | survived, equivalent: the title search still resolves PRIME.1 |
| `owner` hint pattern matches nothing | same | killed (2) |

## Verdict

The three should-fix findings and the optional ones of the review are fixed as the record says; the counts reproduce, 44 for the round with the two pairs that GOV.48's amendment adds; the live outputs are unchanged but for the new role line; b.5 passes on the rehearsed copy for the stated reason. Nothing blocks the merge.
