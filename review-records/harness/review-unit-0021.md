# Review of unit 0021 (cold)

Ran, from a copy under /tmp/claude-1000/rv: the baseline `python3 -B -m unittest tests.ledger.test_signatures` (13 tests, OK); 13 single mutations (table below); a script for the edge cases; grep of `applies`, `ALL_LEDGERS`, `register.signers` over `govharness/`. REPO was not edited except this file.

## Conformance to the amended text

Conforms. `_valid_for` (signatures.py:82-92) and `active_signers` (register.py:159-163) test `row["Ledger"]` equal to one ledger. `applies` is now used only by `required_of` (signatures.py:114), so a required-signature row for `all` still applies. A signer row for `all` is a register problem (register.py:121-125), and `check_signatures` returns on any problem (signatures.py:173). `with_signer` refuses `all` (register.py:246). The key block is written once (register.py:253-255). No other reader treats a signer row for `all` as accepting: `_spoofed` (signatures.py:136) only collects labels. CLI `sign check` rejects `all` as `--ledger-id` for a non-corpus ledger (records.py:171). The README step 6 and the docstrings match the code.

## High

None.

## Medium

1. Test gap: a required-signature row for `all` is untested. Mutating `applies` to `== ledger` (register.py:143) leaves every test green, yet DoD 1 says such a row "is read as before" and the amended text keeps it. Fix: in `tests/ledger/test_signatures.py` add a case with `required=[{"Ledger": "all", "Actor": ..., "From entry": "1"}]` and assert `required_of` returns it for `governance` and `work-a`, and that `read_register` reports no problem for it.

## Low

2. register.py:253: an existing key heading is kept silently, even if the new `armored` differs. A second add of the same fingerprint with other armor is dropped without notice. Impact is small, since `read_register` checks the kept block against its heading, and `add_signer` derives `fpr` from the armor. Fix: compare the existing block with `armored.strip()` and raise `ValueError` on a mismatch. Add a test.
3. register.py:283-289: `with_signer_closed` closes every open row of the ledger and key. A key with rows for two role labels on one ledger has both closed at once (confirmed by the script), and the CLI has no `--role`. The docstring says "the open row". Fix: either say "every open row of that ledger and key" in the docstring and the README, or add an optional role argument. Test whichever is chosen.
4. register.py:283-289: `with_signer_closed(..., "all", ...)` on a hand-written `all` row succeeds. It closes the row (confirmed), which remains a register problem, so the row is still unusable. The test (test_signatures.py:543) covers only the skeleton, which has no such row. Fix: refuse `all` with the STND.HARN.10 message, or document the behavior. Test the choice.
5. test_signatures.py:521-530: the problem-text assertion needs a register with a key block and a real gpg. The test uses a hand-built register and checks only the substring, so it passes. No defect, but it does not check that the `all` row is the only problem. Optional.
6. Pre-existing: `with_signer` accepts a duplicate open row (same ledger, role, key) and a case variant such as `All`. A row for `All` is accepted by `with_signer` and, being not equal to `all`, is not a register problem. It matches no ledger id, so it accepts nothing in practice, but the problem text never appears. Fix: compare `ledger.lower()`, or validate the ledger against GOVERNANCE or a work-ledger pattern.

## Mutation table

| # | Mutation | Result |
|---|---|---|
| 1 | `_valid_for` accepts `all` rows | killed |
| 2 | `active_signers` accepts `all` | killed |
| 3 | `all` signer row not a problem | killed |
| 4 | problem text drops the STND.HARN.10 citation | killed |
| 5 | `with_signer` no longer refuses `all` | killed |
| 6 | refusal text drops the citation | killed |
| 7 | key block written on every add | killed |
| 8 | `applies` ignores `all` for required rows | SURVIVES (finding 1) |
| 9 | `active_signers` ignores Last entry | killed |
| 10 | close matches rows of any ledger | killed |
| 11 | close no longer raises when no row matches | killed |
| 12 | `_valid_for` window removed | killed |
| 13 | `_valid_for` role label check removed | SURVIVES (pre-existing; unit 0021 did not change it). Fix: assert a wrong actor is refused in `SignerRows`. |
