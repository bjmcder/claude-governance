# Review of unit 0019 (QA.8)

Reviewer: independent of the author. Branch round-2026-10-26, commit d58c8cd against 761c50d.

## What I ran

- Read the unit record, the diff of `harness/govharness` and `harness/tests`, and the corpus text for STND.HARN.7, .9, .31, .32 and the terms Content hash, Pin in force and Reach; STND.IDENT.12 and .24; STND.DRAFT.3 and the terms Sentence and Cited document.
- On the live tree: `verify governance` (PASS; only the g.18 warnings), `references governance --check` (PASS), `compose governance --check` (stale: 0).
- The nine test modules named in the brief: 82 tests, OK, 134 s. I did not run the full suite.
- `ruff check govharness tests`: 26 findings both at 761c50d and now, none in the changed files except the two pre-existing SIM905 ones.
- Recomputed `pins_in_force` on the live ledger: entries 1 to 175 give 41 pins under both the old and the new rule, with the same seq numbers. The record's claim is true. The full ledger gives 46 pins, the last five being entries 183 to 187.
- Probed v.8 in memory: deleting DSGN.3, GOV.41 (the highest in its part) or QA.8 fails; listing the identifier on LVL0 passes; a listed identifier still in use, a foreign prefix, and a list on a non-constitution document all fail. DSGN, a document of kind article, is not double-reported.
- In a scratch copy (`/tmp/claude-1000/rev19/`), I put back the old behavior one fix at a time, 25 mutations, and ran the relevant test or module (`mut.py` there).
- In another scratch copy I patched `table_cells` to read defining tables minus the word columns. `verify` then fails g.3 and adds g.8 and g.13 warnings. This confirms item 7's account.

## Correctness by case

- `pins_in_force`, `_shared_pins`, `reaches`: correct for same scope in any order, wider, narrower, partial overlap, multi-path and file scopes. A scope that names nothing is never a pin (`scope_key` is empty), and the check reports it as missing.
- `scope_hash`: lists each file once under the first sorted prefix that reaches it, which is what the term Content hash says.
- `unpinned` now fails and uses `reaches`.
- `checked-by`: `known_keys` is set in `run_checks`, which every path uses (verify structure, verify logic, and the logic workflow). The `check` command runs only logic checks, so it never runs `checked-by`. Not a defect.
- v.5 is right: a field that is present is still validated, and a missing field fails only for adopted or ratified documents.
- v.8 by part is right (see probes).
- The bare-name derivation moved without a change of exclusions: LVL1 to LVL3 only, LVL0, Revision History, Example tables, References, code, quotes, and the document's own name.
- `withdrawn_by` is correct.
- Item 8: the new `TERMINAL_RE` agrees with the term for the live corpus. Reverting it to split at semicolons and colons fails one test in `tests.checks.test_drafting`, so the record's "tests pass unchanged" is true and the change is covered.
- Items 7 and 8 match the record.

## Mutation results

Killed: scope_hash dedupe, `has_scope_path`, `pins_in_force` as same-scope-only and as any-overlap, `_shared_pins` (three variants), unpinned WARN, the unpinned test of file scopes, `checked-by` without `review`, `checked-by` never failing, v.5 (three variants), v.8 using the document's own identifier, `withdrawn_by`, bare names not cited, LVL0 counted, levels not limited, history, Example tables, quotes and self-naming not excluded, and the semicolon split.

Survives: `is_scope_path` reverted to directories only (see Medium 1).

## Findings

### High

None.

### Medium

1. `govharness/core/corpus.py` `is_scope_path` (about line 334) is untested. Item 1 says `ledger append` and `record_transaction` accept a Markdown file. That check lives in `cli/records.py:94` and `workflows/amend.py:~246`. Every new test calls `chain.append` directly (`pin()` in `tests/checks/test_ledger.py:126`). With `is_scope_path` put back to `is_dir()` only, all 82 tests still pass. In that state `ledger append --scope README.md` is refused, and the repair path for `unpinned` would be broken with no test failing. The record cites `test_file_scope_and_hash` for item 1; it does not reach this code. Fix: add a test that calls `record_transaction` with `Change(scope=["README.md"])` and succeeds. Add a case for a missing path and for a non-Markdown file (such as `STND/MANIFEST.csv`), both refused with "scope names no directory or Markdown file". Add a case that `has_scope_path` reports a scope that names a non-`.md` file.

### Low

1. `govharness/ledger/chain.py:7`: the reflowed module docstring leaves a 92-character line ("Markdown files whose content it pins; their combined hash ..."). Ruff and `test_conventions` do not flag it. Rewrap it.
2. `govharness/checks/fields.py:141`: `check_keys_known` fails every key when `ctx.known_keys` is empty, which is the dataclass default if the check is called outside `run_checks`. The test sets it by hand. Fix: fall back to `registered_keys()` when the set is empty, or raise.
3. `govharness/checks/drafting/context.py` (`TERMINAL_RE`): the term Sentence excludes a mark inside an abbreviation, but the rule has no abbreviation list. "e.g. The" would split. It did not before either, and the live corpus has no such case. Add a comment, or an abbreviation guard, when the first case appears.
4. The report-only gap in item 7 is real. STND.DRAFT.3 now asks for more than the harness checks, because a provision with `defines` contributes no cell. The record says why (my patch confirms g.3 fails and g.8 and g.13 add findings) and OPEN-ITEMS holds the question. The Definition of done allows this. Cost: the binding text is not enforced until a round decides which columns are data.

## Item 7 and 8 accounts

- Item 7 (not done): true. The check reads no cell of a `defines` table (`drafting/tables.py:table_cells`). Reading them breaks `verify` as described.
- Item 8 (done): true as far as the drafting checks go. The logic checks keep the old split, and the record says so.

## Verdict

Accepted. Medium 1 is a missing test, not a wrong behavior; fix it before the next unit.
