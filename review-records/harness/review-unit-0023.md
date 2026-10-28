# Cold review of unit 0023 (145d511)

Reviewer: another configuration. Runs in clones under `/tmp/claude-1000/rev0023/`, offline.

## What I ran

- Live corpus at 842282e and 145d511: `verify` differs by the one new line `onset: PASS`, every other line identical; `check --out-dir` byte-identical.
- Rounds a, d, c, o on a copy (766 fields): `verify --no-logic` all PASS. `onset CSQ0..3` list 2, 22, 149, 627 items (174 B to 28.6 KB). `show STND.CODE.22`: `default · from CSQ3; sentence 2 from CSQ2 · rank 5`; STND.STDC.1 shows three row parts; HW.3 `from CSQ3` with no mode; STND.CODE.20 `at every class; sentence 1 from CSQ1`; a section locator shows none. `compose --all DIR` exit 0: `Default, from CSQ3. Instantiates …`, `From CSQ3. …` for HW.
- `verify --no-logic` on twenty copies with one field each: `CSQ9`, `csq3`, `["CSQ3"]`, a part at the provision's class, `sentence 0`, `sentence 7` of a two-sentence body, `row X` without a table, a missing row, `"CSQ4"` whole, null, a dict, a field on STND.CODE.6 (binding), on VV.1, on the document STND.CODE: each `onset: FAIL (1)` naming the item. Good values pass.
- `onset`: `GOVHARNESS_ROOT` honored; a bad one, no root at all, and `CSQ4` exit 2 with a message; nothing found exits 1 with `onset: no provision applies from CSQn` on stderr.
- STND.HARN.3: the listing holds identifiers, titles, and part names only, no body text.
- Edge cases: STND.MPI.7 with two parts at CSQ1 lists whole at CSQ2 with its full onset and twice at CSQ1; `sentence 1000000000` refused; the corpus holds no withdrawn entry (withdrawn numbers are absent files); a corpus without fields exits 1.
- Unit module 14 OK; architecture and conventions 14 OK; full suite 219 OK in 347 s; ruff (79, E501 included) on the changed files clean.

## Findings

### High

None.

### Medium

1. **A row part may name several rows** (`core/onset.py:132–168`, `:202–206`). `part_exists` accepts `row CELL` when any data row starts with CELL. STND.CLASS.10 is waivable and eight rows of its table start with `CSQ2`; `["CSQ3", ["row CSQ2", "CSQ2"]]` passes `verify`, and `onset CSQ2` prints `STND.CLASS.10, row CSQ2`, which names no one row; the definition (round_o_text.py:384) assumes one. Fix: in `onset_problems`, fail a row whose first cell `row_keys` holds more than once; test on STND.CLASS.10.
2. **The skill cites a provision the live corpus lacks** (`skills/consulting-governance/SKILL.md:63`). The new row ends `show ROOT STND.CLASS.22 …`; STND.CLASS.22 arrives with round c, and on the live corpus `show governance STND.CLASS.22` exits 1. Fix: drop the clause until round c is ratified, or cite STND.CLASS.19, which exists.

### Low

1. **Two mutants survive** (table). `test_parts_name_sentences_and_rows` names `row STND.CXX.99`, in no cell; add `assertFalse(part_exists(stdc, "row CSQ2"))`, a second-column cell. Nothing exercises the lookahead of `TERMINAL_RE`; add a body with `e.g. the`.
2. **README.md:29 says "a provision whose other parts start later"**; the parts start at a more severe class. `docs/operating.md:28` says it right.
3. **Numbered lists would break the sentence count** (`core/onset.py:35`): `1. Foo` splits after `1.`; no body holds one today. Fix: `(?<![0-9])` in the lookbehind.
4. **`onset` lists draft and planned provisions alike**, with no `--in-force`; say so in the README row.

## Mutations

Each reverted alone on a copy; the unit's module run.

| Change reverted | Result |
| --- | --- |
| a part named twice; a part at the provision's class; `"CSQ4"` whole; any part name; `["CSQ3"]` accepted | killed (5), `test_malformed_values_refused` |
| a field on LVL0 accepted | killed, `test_each_problem_fails` |
| `onset` exits 0 when nothing applies; every part listed; count off by one | killed (3), `test_lists_provisions_and_parts` |
| CSQ4 base reads `from CSQ4` | killed, `test_described_beside_the_mode` |
| profile onset not capitalized | killed, `test_profile_without_mode_prints_the_onset` |
| sentence index off by one | killed (2) |
| listing in path order | killed, `test_applying_from_keeps_number_order` |
| onset shown on a section locator | survived, equivalent on a valid corpus |
| row matched by any cell | **survived** (Low 1) |
| sentences split at any whitespace after punctuation | **survived** (Low 1) |

## Verdict

Definition of done met; no live verdict changes. Medium 1 wants one more check, Medium 2 one line of the skill; neither blocks the merge.
