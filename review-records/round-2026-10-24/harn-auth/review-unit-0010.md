# Review of unit 0010 (commit eceabea, base 7e8e74f)

Verdict: the change does what the record says and fails closed. No High finding. Two Medium, two Low.

## Checked and sound

- Callers: `read_authorizations` is called only from `authorized` in `cli/environment.py`. The change adds a refusal and summary lines; with the option the derived files equal those of 7e8e74f. The guard and policy are untouched, so the hook allows nothing more.
- An unsigned authorization without the option: `authorizations.py` line 547 raises `ValueError`; `run_environment` catches it, prints, exits 1 before any write. A test checks `out` does not exist. The reason is reported beside the row reasons (the `errors` list joins them).
- The option cannot lift a signature: `signed` true leaves line 547 inactive, and the only use of `accept_unsigned` in `record_problems` is wording. I mutated this (option lifts the check): 5 tests fail.
- Register presence (`cli/environment.py` 188-190): any file under top-level `SIGNR` makes `signed` true. An agent cannot make a register "present but empty" to skip the check: a present register only tightens, and an unsigned entry is still refused (a register with no signers was tested at the command level).

## Findings

### Medium

**M1. Deleting a founded register downgrades the check to the option.** `cli/environment.py` 188-190, `ledger/signatures.py` 137-141. `signed` reads only whether `SIGNR/` exists. If an agent can remove `SIGNR/` (appends and edits are permitted writes), the check falls to "not signed", and `ledger_problems`, which would report "signed, but no signer register", is not run. Since no register exists today, the owner must pass `--accept-unsigned` on every derivation, so the flag becomes habit and a later deletion shows only as one extra summary line. Scenario: the agent deletes a founded `SIGNR/` and appends an unsigned `authorize`; the owner's habitual command accepts it. Fix: set `signed` true also when any ledger entry carries a signature or any entry's scope holds `SIGNR`; refuse with "register removed".

**M2. The acceptance leaves no trace in what is installed.** `authorizations.py` 509-514, `cli/environment.py` 236-238. The statement lives only in stdout. The coverage report and `INSTALL.md` do not say that a write relies on an unsigned authorization, so `--check` and a later reader cannot see it, and an agent that runs the derivation can pass the flag itself and discard stdout. Fix: add a line to `coverage.md` (STND.HARN.19 already has the report state what is referred or relied on) naming each authorization relied on unsigned.

### Low

**L1. README colon garbled.** `harness/README.md`, environment row: "where a signature is required, the option has no effect: managed settings, the guard ..." The colon, which once introduced the outputs, now follows the option clause. Fix: restore "...exits 1 with the reason: managed settings..." and put the unit 0010 clause after the list or in a separate sentence.

**L2. Test gap, pre-existing wiring.** `cli/environment.py` 191. Mutating `verified = signed and not ledger_problems(...)` to `verified = signed` leaves the whole module green: no command-level test has a present register with a bad or valid signature. The unit tests pass `verified` by hand. Not introduced here, but the unit's criterion 3 cites the command path. Fix: one command test with a register and a forged signature. Also no test puts a stray file (not `_doc.md`) under `SIGNR/`; it fails closed, so this is a preference.

## Tests

Suite: 193 tests, OK (301 s); the module has 22 (18 before). Mutants in `/tmp/claude-1000/review-0010/m`: refusal dropped, summary line dropped or always shown, option lifting the signature, `signature or verified`, signature without `verified`, register detection off or by last path part, `--assured` ignored, wording dropped, refusal also when signed: each fails 1 to 5 tests. One survivor: `verified` always true at the command (L2).
The helper `reading` accepts by default; this matters only when `signed` is false, where the sole addition is a summary line the earlier row tests do not assert. Signature rows use `assured=True`, where the option is inert. No hidden regression found.

## Record, README, decision 0002

They agree with the code. Ruff: 0 findings with the tree's settings; E501 at 79: 1 on `authorizations.py`, 6 on the test file, 0 on `cli/environment.py`, equal to 7e8e74f. "Every derivation here needs the option" holds: no `SIGNR` in the corpus.

## Proposed STND.HARN.29 amendment

- Needed? Not for conformance of the code, which is stricter. It is needed so the provision does not describe a weaker harness as conforming; the Notes already give the PRIME.7 argument for the row Record. The alternative, to require a signature always, would raise cost; the custodian chooses.
- Floor (GOV.11): it raises no floor, since PRIME.7 and GUARD.2 already bar an agent opening its own writes; it adds a cost, which the record says the closing argument would name. But it adds a step for the human owner (a statement at derivation); check STND.DRAFT.42 (no new owner decision unless LVL0 assigns it) before adopting. GUARD.10/PRIME.7 likely assign it; the Notes should cite them.
- Wording: the row cell is a test of the authorization, yet the statement belongs to the derivation, so it does not fit "meets it when". The cell has no modal and its condition comes first, which keeps the rules; "elsewhere, the human owner states, when the configuration is derived, that..." is a trailing condition inside a clause, which the brief asks to avoid. The Notes sentence has no modal and no banned word, but is long and has two conditions in one sentence ("Where ..." and "so"); split it. Better cell: "Where the work is assured or the corpus holds a signer register, that transaction carries a signature that STND.HARN.11 accepts. Where neither holds, the human owner states at the derivation that the configuration relies on the authorization unsigned." The second sentence has no modal, which is consistent with the table. Related: the amendment does not cover M1 (a removed register).

## Not checked

No real gpg verification was run; the guard was not installed; the hook's `allow` precedence is not tested here.
