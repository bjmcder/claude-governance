# Cold verification of unit 0023 as revised (bfa2b68)

Reviewer: another configuration. Runs on a scratch clone of HEAD under `/tmp/claude-1000/rev0023/v2/`, offline; round e's uncommitted edits were not in the clone.

## What I ran

- `verify` and `check --out-dir` on the live corpus: byte-identical to the outputs of 145d511, which differ from 842282e only by the line `onset: PASS`. No verdict changes.
- Ambiguous row: `["CSQ3", ["row CSQ2", "CSQ2"]]` on STND.CLASS.10 now fails `verify`, `names row CSQ2, which no one sentence or row of its body is`; a unique row on STND.STDC.1 passes.
- The missing-field rule: one field on STND.CODE.22 makes `verify` fail every other waivable provision below LVL0 (777 lines); `null` passes on STND.CODE.22 and `show` reads `at every class`, `onset CSQ3` lists it not; `null` on STND.CODE.6 (binding) and on VV.1 fails; CSQ4 opening a list is refused. Rounds a, d, c, o re-applied on the clone (765 classes, 9 `null`): `verify --no-logic` all PASS, so no waivable provision below LVL0 lacks the field there; `onset CSQ0..3` list 2, 22, 157, 620.
- Mutants on a copy: the two earlier survivors (row matched by any cell; sentences split at any whitespace) now fail `test_parts_name_sentences_and_rows` and `test_sentences_as_a_reader_counts`; five more (shared row, missing field unchecked, list markers kept, `null` refused, the rule firing without a field) also fail. Sentence counts of every live provision are unchanged.
- Skill row: `onset ROOT CSQn`, then `show ROOT ID`; STND.CLASS.22 is gone. README says "at a more severe class" and that the listing does not filter by status; `docs/operating.md` names `null`.
- `tests.checks.test_onset` (16), `test_structure`, `test_reading_copy`, architecture, conventions: 47 OK; fast subset 46 OK in 11 s. Ruff at 79 with E501: changed files clean; the package's two findings, `tests/checks/test_drafting.py:839` and `:843`, predate the unit.

## Findings

No finding.
