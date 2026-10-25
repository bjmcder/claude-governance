# Verification of the fixes to unit 0010 (commit 4712619)

Suite from `WT/harness`: 198 tests, OK (302 s). Scratch: `/tmp/claude-1000/verify-0010/`.

## Verdict

M2, L1 and L2 are fixed. M1 is fixed for the case it names, but two gaps remain and one new fault was introduced. No finding is High. Nothing widens what the hook allows compared with `eceabea`: `signed` can only become more true, `verified` is false where the register was removed, and the unsigned path stays under `not signed`.

## Findings

### Medium

**N1. New uncaught exception before the chain check.** `register_recorded` (`derive/environment/authorizations.py`) iterates `e.get("scope")` and runs before `chain_problems`. A ledger line whose `scope` is a number or a boolean (`5`, `true`, `1.5`) raises `TypeError`, which `run_environment` does not catch (it catches `LookupError` and `ValueError`). I ran `environment ... --accept-unsigned` on such a ledger: `eceabea` exits 1 with "the ledger's chain is broken"; `4712619` dies with a traceback. It still fails closed, but it has no reason, against the unit's criterion 1. Fix: check `isinstance(scope, list)` and `isinstance(s, str)`, and treat a malformed entry as "register recorded" (fail closed). Add a test with a non-list scope.

**M1-residual. A rewritten ledger hides the register.** `register_recorded` reads only the ledger, and the agent can rewrite it (appends and edits are permitted; the chain has no outside anchor). Drop the founding and signed entries, recompute the chain, remove `SIGNR/`, append an unsigned `authorize`: `register_recorded` is false, the chain is intact, and the owner's habitual `--accept-unsigned` accepts it. Truncating only the tail keeps the detection; only a rewrite from the founding entry on defeats it. Fix: the verifier configuration (`read_config()`, `/etc/governance/signer.json`, which the agent cannot write) already holds the anchor key that founds the register. Treat `read_config().anchor` set and no `SIGNR/` as removed, in addition to the ledger test. The ledger test then remains as a second signal. Say in the record that the ledger test alone is not tamper-proof.

### Low

**N2. Order of checks.** The detection does not rely on an intact chain: `register_recorded` runs on the raw ledger, and `chain_problems` runs later per authorization (`record_problems`). This is harmless for the removed case, since a broken chain refuses anyway, but it is the cause of N1. State the order in the record.

**N3. Forced refusal.** An appended entry with any non-empty signature string (even `" "`) makes `register_recorded` true for good, because the ledger is append-only. An agent can then block every unsigned derivation until the owner founds a register. This fails closed, so it is a nuisance only. The record could name it.

**N4. Spellings.** Tested by calling `register_recorded` directly. It matches `SIGNR`, `SIGNR/`, `./SIGNR`, `SIGNR/_doc.md`, `SIGNR/x/y`. It does not match `/SIGNR`, `a/../SIGNR`, `signr`, a scope given as the bare string `"SIGNR"`, or a nested list. This matches what `check_signatures` and `covers` already accept (exact `SIGNR` in a list), and the founding entry is written by the tool, so the miss is theoretical. An empty signature (`""`, `None`, `0`, `False`) is not counted, as it should not be: it is not a signature.

## Checks as asked

- **M1 does what was asked:** a signed entry, or a scope under `SIGNR`, with the corpus lacking the register, gives `signed` true, `verified` false, and a refusal that starts with `REGISTER_REMOVED`, also with the option. Subject to N1 and the residual above.
- **M2:** the coverage gap and the draft entry rationale name each authorization relied on unsigned, and nothing is added otherwise. Mutants (note dropped from the entry, or from the coverage) fail 2 tests each.
- **L1:** README colon restored; the unit clause follows the list.
- **L2:** the survivor `verified = signed` now fails `test_command_verifies_signatures`.
- **Mutants in my copies** (`m/1` to `m/6`): removed-detection off (2 fail), scope test dropped (3), `removed` left out of `signed` (2), M2 entry note dropped (2), M2 coverage note dropped (2), `verified = signed and not removed` (1). All are caught.
- **Throwaway keyring:** `tests/gpgkeys.py` makes `/tmp/gXXXX` with mode 0700, passes `--homedir` on every call, kills its agent and removes the directory. Verification uses a temporary keyring (`gpg.py`), and the test patches `read_config`, so `/etc/governance/signer.json` is not read. I listed `~/.gnupg` and `/etc` (1105 files, names, mtimes, sizes) before and after the suite: identical. No `/tmp/g*` or `/tmp/sg*` directory remained.

## STND.HARN.29 wording

- **Modals.** The proposed third sentence holds two SHALL ("SHALL rely ... and SHALL name"), which breaks one modal per sentence, and the provision would hold four. Propose a new provision, for example STND.HARN.30 "Unsigned reliance accepted" (binding; instantiates GUARD.10 and PRIME.7; refers to STND.HARN.29 and STND.HARN.19), with two sentences: "Where the work is not assured and neither the corpus nor its ledger records a signer register, a derived configuration SHALL rely on an unsigned authorization only after the human owner accepts it at the derivation (GUARD.10, PRIME.7). Where a derived configuration relies on an unsigned authorization, its coverage report SHALL name that authorization (STND.HARN.19)." This leaves HARN.29 with two modals and a changed row only. Every cited ID must also appear in `instantiates` or `refers_to` (PRIME.7 and STND.HARN.19 are not there now).
- **Negation.** "SHALL rely on no unsigned authorization that ... has not accepted" is a double negative; the positive form above avoids it.
- **Conditions first.** The row and the new sentences put conditions first. The proposed Notes sentence ends "...where an entry carries a signature or a transaction's scope holds the register": a trailing where-clause; recast as "Where an entry carries a signature or a scope holds the register, the ledger records one."
- **Banned words.** None found in the proposed row, sentence, or Notes.
- **STND.DRAFT.42.** The record's reading is arguable, not settled. In its favor: the derivation is the owner's configure act (STND.DFLT.22), and the acceptance restates a grant LVL0 assigns. Against: the second sentence of 42 says a provision SHALL accept a standing authorization (GUARD.11), yet this refuses one without a further act of the owner; and a bare flag is not proof of the owner's act (an agent that runs the derivation can pass it). The record names the alternatives; the custodian decides, and the provision should not be amended before then.

## Not checked

No end-to-end run of the rewritten-ledger attack (argued from the code, with the `register_recorded` calls above). The real `/etc` anchor path was not exercised. Ruff was not rerun. Whether a case-insensitive filesystem lets `signr/` stand for `SIGNR/` in `present` was not tested.
