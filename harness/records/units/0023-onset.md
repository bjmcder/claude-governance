# Unit 0023: the field onset and the command `onset`

Ruling C7 of the deep review of 2026-10-28 (`review-records/deep-review-2026-10-28/rulings.md`) holds the onset of each provision in a front-matter field `onset`, shown beside the mode, and has the harness list what a reclassification to a class adds. Unit 0022 left that command (HR-3 of `review-records/deep-review-2026-10-28/harness.md`) waiting on the ruling. Round o (`review-records/rounds-2026-10-28/round-o/decisions.md`) drafts the field's definition in STND.DRAFT#representation-in-the-harness and sets it on each provision; this unit reads, checks, and renders it. The live corpus carries no field until round o is ratified and applied, so no verdict of `verify` on it changes.

## Definition of done

1. The field is read: a class `"CSQ0"` to `"CSQ3"` for the whole provision, or a list of the class of the provision (`"CSQ0"` to `"CSQ4"`) followed by at least one pair `[PART, CLASS]`, where PART is `sentence N` or `row CELL` and CLASS is more severe than the class of the provision; a part is named once.
2. `verify` fails, under a new structural check `onset`, a malformed value, a field on an item that is not a provision below LVL0, a field on a provision that is not waivable (one that binds at every class), and a part that names a sentence or a row its body does not hold. A provision without the field passes, so the live corpus passes.
3. `show` prints the onset beside the mode (`default · from CSQ3; sentence 2 from CSQ2`), and the reading copies of `compose` and `compose --all` print it on the mode line (`Default, from CSQ3; sentence 2 from CSQ2. Instantiates DSGN.4.`); a profile's provision, which has no mode, reads `From CSQ3.`. An item without the field prints as before.
4. `onset [ROOT] CSQn` lists the provisions, and the named parts, that apply from CSQn, by document and number, with their titles, and a provision whose other parts start later with its whole onset; exit 1 when nothing applies from the class, 2 for a usage error, CSQ4 included.
5. Tests for each change; the architecture and conventions tests pass; the README command table and check list, `docs/operating.md`, and `harness/skills/consulting-governance/SKILL.md` name the command and the onset, the skill with the row "What does reclassification to CSQn add?". Nothing in `rendered/` is rebuilt; the lead does that after ratification.

## Record

- 1 and 2, new `core/onset.py` (layer 0, so that `checks`, `query`, and `derive` share it): `parse_onset` reads the value or raises `ValueError` with the reason; `sentences` counts the sentences of a body outside its tables at terminal punctuation, as a reader does, the lines of a list joining the sentence that leads into them (the drafting checks' finer cut at semicolons and colons is not a reader's count); `row_keys` and `part_exists` name the parts; `onset_problems` gives one line per problem. The check `onset` in `checks/fields.py` calls it over every entry, registered with the provision STND.CLASS.10, which gives the field its force once round o is in force.
- 3, in `query/retrieval.py` the facts line of `render` adds `describe(onset)` after the mode, for an item and not for a section; in `derive/reading_copy.py` `_provision_block` adds it to the mode line, capitalized where a profile has no mode, and leaves the line of a provision without the field as it was.
- 4, in `cli/query.py`: `onset` with `root` (optional, as for `show`) and `CSQn` (choices CSQ0 to CSQ3); `applying_from` in `core/onset.py` sorts by directory and number.
- 5, `tests/checks/test_onset.py`, fourteen tests: the forms read and eleven malformed values refused; parts against STND.CODE.22 and the table of STND.STDC.1; the description; the live corpus passing, three well-formed fields passing, five problems failing; no problem without a field; `show`, the reading copy of a standard, and that of a profile; `verify` failing a field on the binding STND.CODE.6; the command on a copy of the corpus (CSQ2, CSQ3, CSQ1 with exit 1, CSQ4 refused); the order of the listing.

## Mutations

Each change was reverted alone on a scratch copy of the package under `/tmp/claude-1000/roundo/mut/`, the corpus linked, and the named test module run there.

| Change reverted | Test | Result |
| --- | --- | --- |
| the check `onset` returns no verdict | `test_verify_fails_a_bad_onset` | fails |
| a field on a binding provision allowed | `test_each_problem_fails` | fails |
| a field on a provision of LVL0 allowed | `test_each_problem_fails` | fails |
| parts not checked against the body | `test_each_problem_fails`, `test_parts_name_sentences_and_rows` | fails (2) |
| a part at a class no more severe than the provision's | `test_malformed_values_refused` | fails |
| `show` prints no onset | `test_show_prints_the_onset` and one more | fails (2) |
| the reading copy prints no onset | `test_reading_copy_prints_the_onset`, `test_profile_without_mode_prints_the_onset` | fails (2) |
| the command lists no named part | `test_lists_provisions_and_parts` | fails |
| the command names no later part after the title | `test_lists_provisions_and_parts` | fails |
| the listing in path order | `test_applying_from_keeps_number_order` | fails |
| table rows counted as sentences | `test_parts_name_sentences_and_rows` | fails |

The first run found two reverts that survived, the unregistered check and the counting of table rows, since the tests called the check function directly and compared only a count of sentences; `test_verify_fails_a_bad_onset` and an assertion on the end of the last sentence of STND.STDC.1 were added, and both reverts now fail.

## Checks

- Tests: 219 in the full suite (205 before this unit), `python3 -B -m unittest discover -s tests -t .` from `harness/`, all passing in 345 s; the fast subset passes.
- `python3 -B -m govharness verify governance`: every section PASS, `onset: PASS`, logic PASS, with the one warning g.18 as before. The live corpus has no field, so the new check passes and no other verdict changes.
- Round o, rehearsed on rounds a, d, and c: `onset: PASS` with 766 fields set; `onset CSQ0` lists 2 items, `CSQ1` 22, `CSQ2` 149, `CSQ3` 627.
- ruff, at the line length of the package (79), adds no finding on the changed files.
