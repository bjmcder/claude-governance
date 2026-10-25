# Review of unit 0017 (checks fixes of QA.8 part C)

Reviewer: independent, QA.8. Unit commit 0769aee on bc65b95. Scratch: `/tmp/claude-1000/review-0017/` (probes `p/`, mutation runs `mut.py`, `mut2.py`, logs `mut.log`, `mut2.log`). Only this report was written; the scratch merge worktree is removed and pruned.

## Verdict

**Accept.** No High finding. Two Medium findings, both gaps in the tests, not in the code; the unit should close them in a follow-up. The code follows the ruling: where the corpus is silent it keeps the letter and puts the question in Open.

## Merged state

- `git merge --no-commit --no-ff` of the branch into a detached worktree of main (then 8d450ff) is **clean**; only `README.md` and `checks/ledger.py` auto-merged.
- `tests/checks` (discover): 90 tests, OK (227 s).
- `tests.test_architecture`, `tests.test_conventions`, `tests.cli.test_main`: 16 tests, OK.
- `verify governance`: exit 0. `unpinned: WARN (5)` (KNOW/, README.md, STND/_doc.md, TAG/, _PROJECT/), the g.18 warning as before, every other section PASS. Entries: 1455.

## 1. The findings

Reran the original reproductions on the merged corpus (in-memory copies, all non-proof families).

| Finding | Result |
| --- | --- |
| H1 | Closed. Deleting STND.PERF.26 fails v.8 with one line naming the citer. Deleted and listed passes. Deleting the highest GOV provision (GOV.51) fails v.8 (and l.1, e.2). |
| H2 | Closed for the repro: `doesn’t` appended to STND.DRAFT.2 fails g.21. |
| M1 | Handled as ruled: `unpinned` WARN, never FAIL. The ledger check is untouched. Open 1 states a real question. |
| M2 | Closed. The lone row `\| x \| The code may not run \|` in STND.PERF.1 or AGENT.1 fails g.5 and d.1; the same row in GOV.5 fails d.1 only (lvl0 group is INFO for g.5); in STND.DRAFT.17 (which has `defines`) it passes; a quoted cell passes. |
| M3 | Closed. The 13 review passes and 8 controls are refused. I added 24 more cases (socket, ctypes, pickle, tempfile, shutil, logging, `from os import path`, `__import__`, `import x as y`, `print`, `.open`, `.send`, `os.path`, `importlib.util` outside satlib, and others): all refused. |
| M4 | Handled as ruled: the draft with no adopter still fails v.5; the field is now per kind (`ratified_by` for the constitution). Letter of STND.IDENT.12. Open 2 states a real question. |
| M5 | Mostly closed (see section 5). The review's mutation sites are killed. |
| L1, L3, L4, L7 | Done and sound (below). L5, L9: left as ruled, in Open 7 and 8. |

## 2. New errors from the fixes

**H1, v.8 resolution.** Probes:
- Example identifier in quotes (`"GOV.998"`), in code (`` `GOV.997` ``), in Revision History: pass.
- Identifier of a document (`STND.PERF`), `GOV.12.3`, `GOV.5(a)`: pass.
- Foreign scheme (`ES.11`): pass, by the first-mnemonic rule.
- Italic or link-text citation of a missing id: fails, correctly (it is a dangling citation).
- LVL0: deleting GOV.51 and listing it in LVL0 `withdrawn` gives "`GOV.51` is not its identifier" plus the unresolved line. A deleted but cited part provision therefore has no way to pass. The unit says so (Open 5).
- False passes: a dangling id in a References section or an Example-column table (not read, by the g.25 rule); a typo in the mnemonic (`STNP.PERF.5`) is read as another scheme. Both are Low (L-a below).
- v.8 now enforces "a cited identifier resolves", which is STND.DRAFT.22, under the key and the provision STND.IDENT.14 names. The unit discloses it (Open 6); it is a reading the corpus does not state, but it is the fix the review proposed and it has no false failure on the live corpus.

**M2, cells.** No valid table fails; live corpus adds INFO findings only. Tables of a provision with `defines` are unread (Open 3 states it). Two small notes:
- `table_cells` does not skip an Example column, though g.25 does: a table of examples in a non-defining provision, with a modal used in a cell, fails g.5 and d.1 (Low).
- A provision with two tables, one defined, reads neither (Low; none live).

**M3, allowlist.** Complete for the code as it stands (merged tests pass). I found no forbidden effect that passes: dunder attributes, `getattr`, `__import__`, aliases, and `from x import y as z` are refused. `.eval`, `.loads`, `.check` are allowed as attribute names; each needs an import that is refused, so none is an effect today.

**H2.** The patterns are right for `’`. Other apostrophe-like characters (U+2018, U+02BC, U+00B4) are not read (Low).

**L3.** `A SHALL record it; a reader SHALL read it.` fails (lowercase second clause too, since `whole` splits on terminal punctuation followed by a capital). No false failure on the live corpus. An abbreviation followed by a capital (`e.g. A`) splits a sentence and can hide a second modal: Low, and Open 9 states the term question.

**L4.** `LVL0` and `LVL3` pass; `LVL4`, `STND1`, `Ab`, `ABCDEF`, `A` fail. Matches STND.IDENT.17 (letters) and GOV.37 (grades). The register is read by `read_register`; a corpus without MNEM would fail `LVL0`, which is right.

## 3. Check against provision

- g.21 against STND.DRAFT.32 (no contractions): matches.
- g.4 against STND.DRAFT.4 (one modal per sentence): matches, with "sentence" undefined in the corpus (Open 9).
- v.5 against STND.IDENT.12: matches the letter.
- v.8 against STND.IDENT.14: gap test and the withdrawn-in-use test follow the text; the citation test goes beyond it (above).
- mnemonics against STND.IDENT.17 and GOV.37: matches.
- `unpinned` against GOV.36 and STND.HARN.9: a WARN, as ruled.
- d.1/g.x on cells against STND.DRAFT "Normative and informative parts": matches for provisions without `defines`.

## 4. Documentation

The record, README layout, items 2, 5 and 8, and the d, v and g rows agree with the code. The README says `unpinned` warns at "entry 175"; on main the number may drift, which is a Low. The README check table has no row for the new check key `unpinned` (only prose in item 5); Low. The nine Open items each state a real corpus question; Open 6 and 7 add drafts, which is fine.

## 5. Tests: mutation of the fixes

32 mutations of the new code, one process at a time, on a scratch copy of the merged tree (first against the class that holds each fix, then the survivors against `test_drafting`, `test_logic` and `test_structure` whole).

Killed: v.8 foreign-mnemonic skip, retired skip, body reading (`naming_text`), front-matter exclusion; adopter field per kind and the presence test; header cells; `defines` and kind exclusion in `table_cells`; cells added to the unit; d.1 `defines` exclusion and `keep_tables`; mnemonic grade, template, and depth; `unpinned` coverage, depth, and WARN-not-FAIL.

Survivors:

1. **The apostrophe fix is held for `n’t` only.** Replacing `[’'](ll|re|ve|d|m)` with `'(...)` survives, and so does narrowing the person-word lookbehind to `'`. A curly `we’ll`, `they’re`, `I’ve`, `it’d`, `I’m` is thus unheld. See M-A.
2. **d.1 reads tables outside a provision?** Changing `kind == "provision" and not defines` to `True and not defines` in `table_rows_kept` survives all of `test_logic` and `test_drafting`. The README and the record claim that every table outside a provision is not scanned. See M-B.
3. Low: stripping fences before `parse_tables` (`tables.py`) survives (a table inside a code fence is read as prose if it goes); dropping `is_imperative` from g.4's "imposes nothing" test survives; `TERMINAL_RE` with lowercase allowed survives; `unpinned` plural (`count > 1`) and the `isinstance(s, str)` scope filter survive; v.8 message tail (`more > 0`) and `CITERS_SHOWN` survive.
4. Equivalent: `cautions` `== "WARN"` against `!= "PASS"` (structural results are PASS, WARN or FAIL; only called when none fails).

## Findings

### High

None.

### Medium

**M-A. The H2 fix is held only for `n’t`** (`tests/checks/test_drafting.py:357`; `checks/drafting/style.py:17,42`). Survivor: `[{APOSTROPHE}](?:ll|re|ve|d|m)` to `'(?:ll|re|ve|d|m)` passes all of `tests/checks`. Record Definition of done 2 says g.21 finds a contraction and a person word with either apostrophe. Fix: add cases for `we’ll`, `they’re`, `I’ve`, `it’d`, `I’m` and a person word next to `’`.

**M-B. d.1's "no table outside a provision" is unheld** (`checks/logic/wording.py` `table_rows_kept`; README d.0 to d.6 row; record M2). Survivor: `entry.meta.get("kind") == "provision"` replaced by `True`. Fix: a test that the same unquoted barred phrase in a table of a `_doc.md` body does not fail d.1.

### Low

- L-a. v.8 does not read a References section or an Example-column table, and a mistyped mnemonic is read as another scheme; a dangling id there passes (also section 2).
- L-b. `table_cells` reads Example columns that g.25 skips; a provision with two tables, one defined, reads neither.
- L-c. Survivors of item 3 in section 5 (fence strip, `is_imperative`, plural, scope filter).
- L-d. U+2018, U+02BC, U+00B4 are not read as apostrophes.
- L-e. The README check table has no row for `unpinned`; "entry 175" is a moving number.
- L-f. v.8 carries a DRAFT.22 rule under STND.IDENT.14 (disclosed in Open 6).
