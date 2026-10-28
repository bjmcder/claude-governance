# Unit 0021: each signer row names one ledger

The round of 2026-10-28 on signer keys (`review-records/round-2026-10-28-signers/`) amends STND.HARN to 1.5: each row among signers names one ledger, and the term Accepted signature accepts a key only by its row for the ledger of the transaction. This unit makes the harness follow it, closing the item of unit 0016 (M1) on the term. No signer register is founded; the signature feature stays unadopted.

## Definition of done

1. A signer row whose Ledger is `all` is a problem of `read_register`, citing STND.HARN.10, and accepts no signature; a row of required signatures for `all` is read as before.
2. `_valid_for` and `active_signers` read a signer row for its own ledger only.
3. `with_signer` refuses the ledger `all`; the refusals beside an `all` row (`_refuse_beside_all_row`) are removed, since such a row can no longer be written; a key that has rows on several ledgers is written into the register once.
4. Each change has a test; every test passes; `verify governance` passes on the live corpus with its ledger unchanged; ruff adds no finding; the README describes the change.

## Record

- 1 and 2, in `ledger/register.py` (`read_register`, `active_signers`, the docstring of `applies`, now read only for required signatures) and `ledger/signatures.py` (`_valid_for`).
- 3, in `ledger/register.py` (`with_signer`, `with_signer_closed`) and the docstrings of `workflows/signers.py`.
- Tests, in `tests/ledger/test_signatures.py`, class `SignerRows`. `test_signer_row_names_its_ledger` replaces `test_open_all_row_accepts`: rows `governance | 5` and `work-a | none` accept the key on the governance ledger up to entry 5, on `work-a` after it, and on no third ledger, and `active_signers` lists only an open governance row. `test_no_signer_row_for_all` replaces `test_no_row_beside_an_all_row`: an `all` row written by hand is a register problem and accepts nothing; `with_signer` refuses `all`, citing STND.HARN.10; a key added on two ledgers is written once and closes on one, staying open on the other.
- 4: the README step on signatures states the rule; the live corpus has no `SIGNR`, so its verification is unchanged.

## Review

`review-records/harness/review-unit-0021.md`, by an agent of another configuration: no High finding; of 13 mutations, 11 were killed. Each finding is disposed of in `review-records/round-2026-10-28-signers/decisions.md`. In short: `test_required_row_for_all` covers a row of required signatures for `all`; `with_signer` refuses a second armor of a key it holds; `with_signer_closed` refuses `all` and documents that it closes each open row of the key on the ledger; `all` in any case is refused and is a register problem; `test_signer_row_names_its_ledger` refuses a wrong actor. The two surviving mutations and the three new guards, each reverted alone on a scratch copy, now fail a test.
