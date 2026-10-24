# Review 0005: assurance in proportion to class

Independent review (QA.7). Record contents per STND.DFLT.8: revision reviewed, reviewer, findings, and verdict.

| Item | Value |
| --- | --- |
| Revision reviewed | `a4e236b`: the STND.DFLT 1.2 proposal `drafts/dflt-1.2-tools/dflt_12.py`, STND.HARN 0.5 as `drafts/harn-0.1-tools/build_harn.py` generates it, and unit 0004 (guard, adapter, inputs, command, tests, records) |
| Reviewer | Claude (independent review agent); not the author of the change |
| Directives | 1: "In the event the harness code is lost or inoperable, the governance documents still apply." 2: signing and fail-closed mechanisms "seamless or optional for anything but CSQ0 or 1" |
| Scope | GOV.10, 11, 13, 15, 20, 22, 36; PRIME.4, 5, 7, 12; GUARD.2, 5, 10, 11, 16; STND.DFLT (5, 13, 15 to 18, 22 to 26, Terms, Notes), STND.INSTR, STND.HARN (7 to 15, 21 to 29), STND.CLASS, STND.IDENT.3, STND.DRAFT; the code, tests, README.md, pointer.md, and records |

## Findings

Severity: High means a call can defeat a safeguard. Medium means a provision lapses with nothing enforcing it, a defined meaning has no consistent reading, or a provision contradicts the floor. Low means an inexact or stale statement.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | High | The guard denied only `ValueError` at every class. A command nested about 2 000 deep in `$(` raised `RecursionError`, which work that is not assured let through, unguarded: a call could choose to bypass the guard | Fixed: once the policy is read, every fault is denied at every class; only a guard that cannot run, or cannot read its policy, follows the class. The test covers that call at both classes and fails on the old code |
| 2 | Medium | Directive 1 failed. "Operative" for work that is not assured meant "shown missing or failing by nothing". A deleted settings file runs no hook and shows nothing, so the configuration stayed operative and STND.DFLT.24 and STND.DFLT.25 stayed displaced with nothing enforcing them. A guard that fails open lets the failing action through before its notice arrives, and a sandbox that fails open may warn only the human owner | Fixed: STND.DFLT.22 displaces a provision only for assured work, whose configuration fails closed. For other work every provision stays in force and the configuration adds protection. Operative now means found installed in the current session, by a verifier the agent is unable to alter for assured work |
| 3 | Medium | The fifth exempt class of STND.DFLT.15 rested, for work that is not assured, on nothing showing the checkpoint mechanism failing. GUARD.5 needs a verified recoverable prior state at every class, so this broke the floor | Fixed by the same term: the mechanism counts only while found installed in the session. Otherwise STND.INSTR.2 has the agent preserve the state itself, which costs the human owner nothing |
| 4 | Medium | "Assured work" was "work whose classification records CSQ0 or CSQ1", and STND.DFLT.23 accepted unsigned owner entries only when the work is not assured. An unsigned entry recording CSQ1 counts only if the work is not assured, which it then makes assured: there is no consistent reading. An unsigned, forgeable entry lowering the class would also end assurance | Fixed: an entry of the human owner, signed or not, records CSQ0 or CSQ1, and no later entry that STND.DFLT.23 accepts for assured work records a less severe class. Raising needs no signature, and lowering needs one |
| 5 | Medium | The new row of STND.DFLT.18, "Entries of the human owner in work that is not assured, Forgery, An agent, No", declared PRIME.7 and STND.DFLT.5 unprotected, a floor obligation (GOV.10). It contradicted the rows "Evidence, Fabrication, Any actor, Yes" (LEX: a record is evidence) and "Change beyond authority, Yes", and missed the agent's own records of grants, which are not owner entries | Removed. The Notes state the accepted gap: STND.DFLT.5 and PRIME.7 bar a forged entry, but nothing detects one |
| 6 | Low | History row and rationale: the claim "a lost or failing configuration leaves its provisions in force" was false (finding 2); the row listed the threat-table change | Rewritten for the revised text |
| 7 | Low | `hook_command` put the notice in hand-written single quotes, which held only while the notice had no `'`; the test split the string and did not run it | `shlex.quote`; the test runs the command through `/bin/sh` with the interpreter missing. It checks exit 2 for assured work, and otherwise exit 0 with JSON that has `systemMessage` and `additionalContext` and no `permissionDecision` |
| 8 | Low | Stale statements: README step 7 described "confirmed" at every class; README and pointer.md gave STND.HARN as 0.4; `inputs.py` said the bounds widen once the entry is "signed"; the guard docstring treated an unreadable call as a guard fault; decision 0002 and unit 0004 split faults by kind | Updated. Records are appended to, not edited (PRIME.5) |
| 9 | Low | `dflt_12.py` had a line over 79 characters (ruff E501) | Fixed |

## Considered, no change

- **GOV.11.** A signature mechanism that depends on the class is not proportioning under GOV.11. GUARD and GOV are not proportioned. The defaults choose a mechanism for GOV.36, GUARD.10, GUARD.2, and PRIME.7, and each class's mechanism meets them. The CSQ0 and CSQ1 mechanism is added above that, and does not raise the floor of every class.
- **GUARD.2 and PRIME.7.** An agent's entry quoting a grant that the human owner gave records the owner's authorization; it grants nothing. Relying on it as the record states, including its actor and the content of STND.DFLT.16, is reliance on the record. The narrow wording "records a grant under STND.DFLT.17" stops such an entry from adopting a cap (STND.DFLT.26), a configuration (STND.DFLT.22), or a checkpoint mechanism (STND.DFLT.15).
- **GOV.13.** "Assured work" is read from the record and assumes no class. No provision needs the class itself, so none makes an agent halt for it.
- **GOV.15 and GOV.20.** Physical harm makes the work CSQ0 only where the human owner states it, and hardware work needs a project constitution, so the defaults then do not apply.
- **GUARD.11.** An agent's record keeps the per-action or standing form (STND.DFLT.16), so no irrevocable remote write gains a standing authorization.
- **Directive 2, elsewhere.** STND.DFLT.5 forbids, and requires no signature. STND.DFLT.13 and STND.DFLT.26 need an accepted entry, which is unsigned for work that is not assured. The terms Working bounds and Signer register impose nothing. STND.HARN.11 to 15 bind only a signature that is present, the governance ledger, or a requirement the owner registers. STND.HARN.21 to 25 bind a harness, and a configuration is optional. STND.INSTR and STND.CLASS require no signature or verifier.
- **STND.HARN.8.** Refusing to append to a broken chain is kept. The repair is a restore from version control, and appending past a break would make that restore lose the new entries.
- **Class.** Minor under STND.IDENT.3: obligations and defined meanings change, and no prime directive or governing principle does. Loosening is not a test of the major class.

## Remaining friction and consequences (not fixed)

| # | Severity | Finding |
| --- | --- | --- |
| C1 | Low | Assured work keeps signatures and fail-closed configuration by design. A guard, policy, interpreter, or sandbox that fails then refuses every call until the human owner repairs it. Making this optional would let a forged entry or an unenforced outcome act on CSQ0 or CSQ1 work |
| C2 | Low | For work that is not assured, STND.DFLT.25 now binds even with a configuration installed. A read outside the working bounds then needs a referral (STND.DFLT.20), not a permission prompt. One grant that the agent records widens the bounds across sessions |
| C3 | Low | `--assured` is the owner's statement. The adapter does not read the work ledger's class, so a missing flag on CSQ0 or CSQ1 work derives a configuration that fails open. `coverage.md` states which was derived |
| C4 | Low | A sandbox that fails open may tell only the human owner, not the agent, which STND.HARN.29 asks of other work. The Claude Code facts given for this review do not settle it. After finding 2, no provision depends on it |
| C5 | Low | A guard that misses its 10 s timeout lets the call proceed at every class (review 0004, finding 3) |
| C6 | Low | Apply DFLT 1.2 before adopting STND.HARN 0.5, whose Notes use its terms |

## Results

| Check | Result |
| --- | --- |
| `rehearse governance drafts/dflt-1.2-tools/dflt_12.py` | all eight checks PASS on the copy; one entry appended (seq 42); source unchanged (640 files and directories) |
| `check <rehearsal copy> --no-z3` | exit 0; no FAIL or WARN; no finding on STND.DFLT in the punch list; `logic_report.md` identical to that of the proposal as presented |
| `check governance --no-z3` | exit 0; no FAIL or WARN; no finding on STND.HARN; l.3, g.16, and g.17 PASS |
| `verify governance` | all PASS; ledger 41 entries |
| `manifests --check`, `references --check` | stale: 0; PASS |
| unit tests | 112 tests, OK |
| `ruff check --select E,F,W,I,UP --line-length 79` | clean |

## Verdict

Accepted for the custodian's decision, with the revised STND.DFLT 1.2 proposal to ratify and apply before STND.HARN 0.5 is adopted. Both directives hold. Only assured work needs a signature or a fail-closed configuration. For other work, no signature, verifier, or fail-closed mechanism is required, and losing the harness or a configuration leaves every provision in force.
