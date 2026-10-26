# Unit 0018: the environment derivation and the guard dropped

The harness is meant to be installed into a code project as a fast, mechanical interface between an agent and the corpus: the agent fetches what applies (`show`, `find`, `context`, `pairs`) instead of loading corpus files into its context, and `verify` and the derived tables keep the corpus aligned. The environment derivation of units 0003, 0007, 0008, 0010, 0012, and 0014, and the guard of unit 0015, served another aim: enforcing the governance on an agent through Claude Code's sandbox, permission rules, and a pre-action hook. On 2026-10-26 the human owner dropped them. The installation step that was open for them is dropped with them.

STND.HARN.18 to STND.HARN.23 and STND.HARN.29 govern a configuration that a harness derives, so none of them applies once the harness derives none, and the provisions of STND.DFLT that such a configuration would displace (STND.DFLT.22) apply in full. `harness/governance/` is unchanged.

## Definition of done

1. `govharness/hooks/`, `govharness/derive/environment/`, `govharness/workflows/environment.py`, `govharness/cli/environment.py`, their tests, and `tools/install-tests.md` are removed, and the command `environment` with them.
2. Nothing else in the package or the tests imports what was removed; `tests/test_architecture.py` no longer admits effects to `govharness.hooks`.
3. The signer register, signatures, and the head pin of `/etc/governance/signer.json` stay: they are part of the ledger check of `verify`, and they are dormant until the owner founds `SIGNR`.
4. Every remaining test passes, and `verify`, `references --check`, and `compose --check` pass on the live corpus as before.
5. The README, decisions 0001 and 0002, and `OPEN-ITEMS.md` describe the change.

## Record

- Removed: about 7 200 lines of package code (`hooks/guard.py` 4 929; `derive/environment/` 2 288, with the Claude Code adapter, the authorization reader of STND.HARN.29, and the secret store of unit 0007) and about 5 700 lines of tests (`tests/hooks/`, `tests/derive/test_authorizations.py`, `tests/derive/test_environment.py`).
- `cli/main.py` drops the subcommand. In `tests/test_architecture.py`, the layer `hooks`, the prefix `HOOKS`, the test `test_hooks_stand_alone`, and the hook's places among the read, write, environment, print, and clock effects are removed; the clock stays admitted to the CLI, for the default time of `ledger append`.
- `ledger/gpg.unalterable` stays, since the signer configuration still uses it.
- The README states in its opening that the harness enforces nothing on an agent, and loses the layout lines, the command row, and the three bullets of "Not yet built" on the adapter, the guard, and remote writes. Decision 0002 is marked withdrawn; decision 0001 notes that its rows on `govharness.hooks` are history.
- `OPEN-ITEMS.md` loses the custodian's installation step and the guard's known limits R2 to R10.
- The records of units 0003 to 0015 and their reviews stay as written; the code they describe is in git history before this unit.
- Audit: see the work report of this unit for the suite run and the verify output.
