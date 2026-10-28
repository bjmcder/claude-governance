# Cold review of unit 0024 (051bde6)

Reviewer: another configuration. Runs in copies under `/tmp/claude-1000/rv24/`, offline. Base for comparison: e0595e9, exported with `git archive`.

## What I ran

- Live corpus with the code of e0595e9 and of 051bde6: `verify governance` byte-identical (every check PASS, the one g.18 warning), exit 0 both.
- Rounds a, d, c, o, e applied to a copy (ledger 272 entries, `seq 315 STND.PY 1.5` last): `verify` with 051bde6 every check PASS, the g.18 warning only; with e0595e9 `logic: FAIL (2)`, g.1 and g.23, the expected failure of a corpus whose spelling table has moved. `cited_tables` on the copy returns `{("STND.DOCS.8", "spelling")}`; owners are the six STND.DRAFT provisions and STND.DOCS.8; no problem. On the live corpus it returns the empty set (STND.DRAFT.38 refers to HW, a document with no `defines`), owners as before. No other provision of either corpus defines a name of `TABLE_SPECS`.
- Counts, live corpus, by `review_pairs` of e0595e9 with the bases classified: NUMER 4,384 pairs, 92 with a matter basis, 19 with a matter basis only, 4,292 on a common LVL0 provision only. HW 2,302/128/70; HDES 2,343/137/57; STND.VVUQ, AGENT, STND.CODE: no matter basis; LVL0 amending VV.1 12,185/339/125. With 051bde6: NUMER 92, HW 128, HDES 137, STND.VVUQ 0, AGENT 0, STND.CODE 0, LVL0 with VV.1 339, NUMER with HW 345 (144 on common instantiation alone, none reaching a third document), HW with NUMER 345 and equal, NUMER.11 6, NUMER.11 with HW.16 39. Each figure of the record reproduces. 92 is right under the drafted rule: the Shared matter row lists a pair the tables give for one matter whatever else it rests on, and HR-12's 19 counted the pairs with no other basis.
- The round as one change on the copy, `pairs COPY STND.HARN.24 --with <the 22 other provisions> --amends GOV.11 GOV.24 GUARD.4 GUARD.15`: 56 pairs, the rows of `round-e/pairs-changed.md`. `pairs COPY LVL0 --amends ...`: 0. Per document on the copy: NUMER 92, HW 128, HDES 137, the three others 0.
- Edge cases on the live corpus: `pairs governance VV.1`, `GOV`, `STND`, `LVL0`, `STND.HARN.28` each print `0 pair(s)` and exit 0; `LEX.1` exits 1; `--amends NOPE` is ignored (92 pairs, exit 0); `NUMER --with` (empty) 92; `NUMER --with NUMER.11 numer` 92 under the heading `NUMER, NUMER.11`; `pairs --with HW governance NUMER` is a usage error (`--with` takes `nargs="*"` and swallows the positionals). NUMER set to draft in memory and named: 92; HW named with NUMER draft and not named: 109 (NUMER's provisions leave the other side, as the rule in force and the drafted rule both want). The corpus holds no provision with status withdrawn, on the live corpus or the copy: withdrawn numbers are absent files (STND.CXX.18 absent after round e). `pairs` prints identifiers and bases only (STND.HARN.3).
- Tests: `tests.checks.test_combination` (9), `tests.cli.test_main`, `tests.checks.test_drafting`, and the fast subset `tests.query.test_retrieval tests.cli.test_main tests.test_architecture tests.test_conventions`: 70 tests, OK, 124 s. `ruff check` at the repository's defaults clean on the seven changed files; at 79 columns with E501 two lines over, `tests/checks/test_drafting.py:881` (80) and `:885` (81).
- Twenty-five hand mutants (table below).

## Findings

### Should-fix

1. **A provision on the changed side only by instantiating an amended LVL0 provision pairs, on common instantiation, with every provision of every touched document** (`govharness/query/combination.py:417`, `if doc_of[second] in docs:`). The condition tests the other provision's document and not the changed-side provision's, so the pair (STND.CREW.13, AGENT.10) on the basis GUARD.14 is listed for the round: STND.CREW.13 instantiates GUARD.15, AGENT holds the amended AGENT.45, and neither provision changes, nor is GUARD.14 amended. Fifteen of the round's 56 pairs are of that kind (STND.CREW.13 and .21 with AGENT.6 to .10, and others), which contradicts `round-e/decisions.md:200` and `pairs-changed.md:70`, "the pairs that hold a changed provision ... 56": 41 hold one. On the live corpus the reading reinflates a mixed change: `pairs governance NUMER --amends VV.1` lists 3,782 pairs, 3,438 on common instantiation alone, and `NUMER.11 --amends VV.1` 3,777, such as (AGENT.12, NUMER.12) on VV.1, where neither provision changes. Ruling E1 says "those where both provisions are in documents the change touches", and the drafted Note says "those of common instantiation within the change"; the drafted table row ("The other provision is in a document of which the change adopts or amends a provision") admits the code's reading, since "the other" is relative to a provision that may qualify only by instantiating what the change amends. Fix, if the ruling's words govern: `if doc_of[first] in docs and doc_of[second] in docs:`, the docstring sentence at `:347` ("when the other provision lies in a document that the change touches" becomes "when both provisions lie in documents that the change touches"), and the DoD's item 1. Under that fix the round lists 42 pairs (41 holding a changed provision, plus (STND.DRAFT.42, AGENT.15) on GUARD.3), NUMER with VV.1 344, NUMER.11 with VV.1 339, and every other count of the record is unchanged; `pairs-changed.md` loses rows 35 to 49 of its kind. If the literal reading is meant, the Note and the record should say that a provision instantiating an amended LVL0 provision pairs with every touched document, and `pairs-changed.md` should drop "hold a changed provision". A test either way: `review_pairs(corpus, ("NUMER",), ("VV.1",))` lists no pair on a LVL0 basis whose first provision is outside NUMER.
2. **An identifier that is a LVL0 provision, an article, a part, or LVL0 itself is accepted and lists nothing** (`govharness/cli/query.py:233–239`; `combination.py:381`). `pairs governance VV.1` and `pairs governance GOV` print `0 pair(s)` and exit 0, since the identifier is in `corpus.by_id` and falls into `docs` as a document with no provisions below LVL0; `--amends NOPE` is ignored. Fix: in `run_pairs`, after `resolve_ref`, an entry of kind `provision` and level `LVL0` goes to `amends`; an entry that is neither a document holding a provision below LVL0 nor such a provision prints `pairs: {given} is not a document or provision below LVL0` and exits 1; each `--amends` identifier must name a LVL0 provision or exit 1 likewise. Test the three in `tests/cli/test_main.py`.
3. **An empty listing exits 0** (`cli/query.py:247`). `docs/operating.md:34` says `pairs` exits 1 when nothing was found, as `onset` does; under the narrowed rule an empty listing is the common case (STND.VVUQ, AGENT, STND.CODE, LVL0 with the round's four amendments). Fix: `if not found: print("pairs: no pair to review", file=sys.stderr); return 1` after the table, or correct `operating.md:34` and the README row; the record should say which.

### Optional

1. **Three mutants survive** (table). (a) `others` without `or doc_of[pid] in docs` (`combination.py:393`): a named provision of a draft document loses its partners in that document, `("NUMER.11", "HW.16")` with NUMER draft gives 20 pairs against 39; (b) `matters` without `or row.document in docs` (`:398`): NUMER draft and named gives 0 pairs; (c) `UNPAIRED_PARTS` ignored (`:325`): NUMER with HW gives 349 pairs. Add to `test_common_instantiation_only_within_the_change` an `assertFalse(any(b.startswith(("GOV.", "PRIN.")) for b in pair.bases))`, and a test that sets `index["NUMER"].meta["status"] = "draft"` and asserts `review_pairs(corpus, "NUMER")` keeps its 92 pairs and `("NUMER.11", "HW.16")` its 39.
2. **One of two guards in `tables.py` is dead** (`:86–88` and `:139`). `cited_tables` skips a target inside the standard and returns a set, so `if pid not in holders.setdefault(name, [])` never fails; the mutants removing either survive. Drop the guard: `holders.setdefault(name, []).append(pid)`.
3. **`cited_tables` is not pinned by a test** (`tests/checks/test_drafting.py:790`). The mutant that scans the provisions outside the standard as citers survives, because some provision outside STND.DRAFT refers to STND.DOCS.8. Add `self.assertEqual(cited_tables(corpus, "STND.DRAFT."), {("STND.DOCS.8", "spelling")})` after the move, and a variant that moves the table without the `refers_to`, asserting g.1 FAIL ("defined by 0 provisions"). The pickup is by name alone: any provision a STND.DRAFT provision refers to that defines a name of `TABLE_SPECS` becomes a holder, so a future provision defining, say, `quantifiers` for its own use and cited from STND.DRAFT would give g.1 two owners; acceptable today, worth a sentence in the module docstring.
4. **`--with` before the positionals swallows them** (`cli/query.py:83–90`): `pairs --with HW governance NUMER` is a usage error. `nargs="+"` with `action="extend"` keeps the list and reads better; or note in the README that the options follow `ID`.
5. **`harness/skills/consulting-governance/SKILL.md:42`** still gives `pairs ROOT DOC`; add `[--with ID ...]`.
6. **Two lines over 79 columns**, `tests/checks/test_drafting.py:881` and `:885`; the repository's ruff defaults pass, the earlier reviews ran at 79.

## Mutations

Each applied alone to a copy of the package under `/tmp/claude-1000/rv24/mut/`, the named tests run there.

| Change | Test | Result |
| --- | --- | --- |
| common basis on every pair (rule in force) | `test_combination` | killed (18,376) |
| touched document tested on the changed-side provision instead of the other | `test_combination` | killed (6,530) |
| document of a named provision not touched | `test_combination` | killed |
| named provision not on the changed side | `test_combination` | killed |
| every provision of the document of a named provision on the changed side | `test_combination` | killed (215) |
| `others` drops touched documents not in force | `test_combination` | **survived** (Optional 1a) |
| matters tables of touched documents not in force dropped | `test_combination` | **survived** (Optional 1b) |
| key always normalised | `test_combination` | killed (105) |
| same-document pairs kept | `test_combination` | killed (291) |
| both provisions must be profiles | `test_combination` | survived, equivalent on the live corpus (no listed pair joins a profile to a standard) |
| GOV and PRIN bases pair | `test_combination` | **survived** (Optional 1c) |
| `amends` ignored | `test_combination` | killed |
| a str `changed` iterated as a tuple | `test_combination` | killed |
| matter basis dropped | `test_combination` | killed |
| every named identifier taken as a provision | `test_combination` | killed (errors) |
| cited holder appended without the guard | `test_spelling_table_in_a_cited_provision`, `test_clean_corpus_conforms` | survived, equivalent (Optional 2) |
| references inside the standard not skipped | same | survived, equivalent (Optional 2) |
| unknown table names of a cited provision taken | same | killed |
| cited tables not read | same | killed |
| the citing provision recorded as holder | same | killed |
| citers scanned outside the standard | same | **survived** (Optional 3) |
| target's `refers_to` read for `defines` | same | killed |
| `--with` ignored; unknown `--with` identifier not fatal; `--with` identifiers not resolved for case | `test_pairs_with_other_documents_of_the_change`, `test_show_and_pairs_resolve_case` | killed (3) |

## Verdict

The code does what the record's definition of done says, every count reproduces, no live verdict changes, and the rehearsal of rounds a, d, c, o, e passes with the spelling table read from STND.DOCS.8. Should-fix 1 is a reading of the drafted row that the ruling's words do not support and that puts fifteen unchanged pairs into the round's own listing; the custodian should settle which reading STND.HARN.28 means before the round is ratified, and the one-line fix follows. Nothing blocks the merge of the unit itself.
