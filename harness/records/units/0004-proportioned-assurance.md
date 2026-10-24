# Unit 0004: assurance in proportion to the class of the work

## Deviation

As in unit 0003, this definition of done was written after the code it audits, contrary to STND.DFLT.7; the custodian's direction ("optional for anything but CSQ0 or 1") was the specification. Recorded and reported (STND.INSTR.7).

## Definition of done

1. `environment --assured` derives a configuration that fails closed: the hook ends in `|| exit 2`, the guard denies on a fault, and the sandbox must start (STND.HARN.29).
2. Without `--assured`, a guard that cannot run or faults lets the call proceed and tells the human owner and the agent; the sandbox may be unavailable.
3. A call the guard cannot read is denied at every class.
4. The tests, the architecture and convention tests, ruff, and `verify` pass.

## Record

- Done: `hooks/guard.py` (`denial`, `fault_answer`, `--assured`, event type check); `derive/environment/claude_code.py` (`hook_command`, `UNGUARDED`, sandbox start by class, report and install text); `inputs.Inputs.assured`; `cli/environment.py` (`--assured`); tests `test_policy_fault_by_class`, `test_hook_failure_by_class`; decision 0002 adjustment.
- Audit: 1 to 3 met by those tests and `test_odd_input_fails_closed`; 4 met: 112 tests OK, ruff clean, verify PASS.

## Review 0005

The independent review found that criteria 2 and 3 split faults by kind, not by cause: a call nested too deep to parse made the guard fail, and work that is not assured let it through. Criteria 2 and 3 now read "a guard that cannot run, or cannot read its policy" and "a call the guard cannot read, or whose reading faults". Audit: `test_odd_input_fails_closed` covers both classes and that call; `test_hook_failure_by_class` runs the hook command through the shell with the interpreter missing. 112 tests OK, ruff clean, verify PASS.
