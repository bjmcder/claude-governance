# Unit 0006: profile combination checks and review pairs

## Definition of done

1. Check m.1 fails on each attribute of the selector table of a profile or sub-profile in force that the document its Defined by column names does not define in its Terms (STND.HARN.26).
2. Check m.2 fails on a shared matter with more than one owning profile, on a provision that a shared-matters table gives for another profile's matter and that cites no provision of that profile, and on a listed provision that does not exist (STND.HARN.27).
3. `pairs ROOT ID [--amends LVL0_ID ...]` lists the pairs of STND.HARN.28 as a Markdown table, and reproduces the 61 pairs that the review of NUMER 1.0 listed by reading.
4. The readers sit in layer 2 (`govharness.query.combination`), the checks in `govharness.checks.combination`, the command in layer 4; nothing new reads or writes a file.
5. The new tests, ruff, black at 79 columns, the convention audit, and `verify` pass.

## Record

- Done: `govharness/query/combination.py`, `govharness/checks/combination.py` (registered after the revision family), `run_pairs` in `govharness/cli/query.py`; `tests/checks/test_combination.py` (6 tests); README rows for m.1, m.2, and `pairs`.
- Audit: 1 and 2 met by four damage tests and the clean-corpus test; 3 met by `test_pairs_match_the_numer_review` (the same 61 unique pairs, 66 rows by basis in the record); 4 met by inspection of the imports and calls; 5 met: 6 tests OK, ruff and black clean, verify PASS. The full suite was not run in this session, because the test tree is held only in the project; it is owed with the next commit.
- Not done: STND.HARN.18 remote-write row. The derived configuration refers every remote write, which meets the row under the transition of ledger entry 53; letting a write that an authorization names by destination and kind proceed without referral needs an authorization format that STND.PROJ does not yet fix.
- First use: the pairs for STND.VVUQ 1.0 (1607) were listed after its adoption, which entry 61 had recorded as having none; the review found one conflict and four unowned matters (claude/drafts/vvuq-1.0-harn28-review.md).
