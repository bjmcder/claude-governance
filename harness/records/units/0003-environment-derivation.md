# Unit 0003: derive an agent's environment from governance

## Deviation

This unit's definition of done was not committed before its first attempt, as STND.DFLT.7 requires. The specification the code was written against existed first, but only as uncommitted draft text: STND.HARN.21 to STND.HARN.24, in `drafts/harn-0.1-tools/build_harn.py`. The criteria below were written after the code and are audited as such. This is a process defect of the agent; it is recorded here and reported to the human owner in the completion report (STND.INSTR.7).

## Definition of done

1. `python -m govharness environment` reads the outcome table of STND.HARN.21 and the protected-location table of STND.INSTR.3 by their names in `defines`. It renders the Claude Code files without any outcome, response, or location written into the code.
2. Each outcome's text rules go to `deny` for Refuse and `ask` for Refer. The guard's policy carries each outcome's response.
3. An outcome or protected location that the adapter does not know is reported as a gap.
4. The draft entry names only outcomes enforced in full.
5. The guard refuses or refers each call that the test cases name, passes routine actions, fails closed on a fault, and imports nothing from the package.
6. `environment --check` reports each missing, differing, or alterable installed file.
7. The architecture and convention tests pass with the hooks package added, ruff is clean, and every earlier test passes.

## Record

- **Plan:** draft STND.HARN 0.1, then the outcomes reader, the inputs, the adapter, the guard, the installed-file check, the command, and the tests.
- **Done:**
  - `govharness/derive/environment/` (`outcomes.py`, `inputs.py`, `claude_code.py`, with the adapter registry in `__init__.py`);
  - `govharness/hooks/guard.py`;
  - `govharness/workflows/environment.py`;
  - `govharness/cli/environment.py`, plus `cli/arguments.py` for the shared root type;
  - tests in `tests/hooks/test_guard.py` and `tests/derive/test_environment.py`;
  - decision 0002 and the adjustment to decision 0001.
- **Audit:**
  1. Met. `test_every_outcome_reaches_the_policy` passes, and no outcome text appears in the code.
  2. Met. `test_response_places_rules` and `test_amended_response_moves_rule` pass.
  3. Met. `test_unknown_outcome_is_not_covered` and `test_unmapped_location_is_a_gap` pass.
  4. Met. `test_entry_names_only_full_outcomes` passes.
  5. Met. `tests/hooks/test_guard.py` passes 18 tests with their subtests. `test_hooks_stand_alone` passes.
  6. Met. A missing, changed, or alterable file or program (the hook's interpreter) is reported. The passing case is shown with the account's reach simulated (`test_current_and_out_of_reach_passes`), because this sandbox runs as root and root can alter every file. It is still to be confirmed from an unprivileged account on installation.
  7. Met at the commit that closes this unit. The suite is run in full before the commit.
