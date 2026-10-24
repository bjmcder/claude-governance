# Verification of 8602a67: HARN.29 tested per entry

Verifier cold to the work. Scratch copy and mutations: /tmp/claude-1000/verify-harn29/m. No file edited except this report.

## Result

The behavior matches the intent for well-typed input. One defect (Medium) where a malformed entry raises an exception instead of a fail-closed result; it predates 8602a67. Three test gaps (Low). Nothing widens what a hook allows beyond the intended change.

## Findings

### Medium (defect, pre-existing at 1b8849b, not introduced)

M1. `harness/govharness/derive/environment/authorizations.py:138` (`len(set(kinds))`). A `kinds` list holding an unhashable item (front matter `kinds: [[commit]]` or `[{a: 1}]`) raises `TypeError`. `cli/environment.py:217` catches only `LookupError` and `ValueError`, so the command ends in a traceback. I reproduced this on `entry_problems`. The derivation does stop and no files are rendered (`render` follows `authorized`), so it fails closed in effect. But it gives no reason, and it contradicts "a malformed entry fails closed ... the derivation stops with the reason". `test_malformed_entries` has no unhashable case. Fix: test `all(isinstance(k, str) and k in KINDS for k in kinds)` before `set(kinds)`, and add the case to the test.

### Low (test gaps; mutations that survive)

L1. Position of a malformed entry. Mutation `for item in writes[-1:]` in `read_one` (line 374) passes all 17 tests. `test_malformed_entry_fails_closed` puts the bad entry last. Add a case with the bad entry first (and middle).

L2. Order of kinds and entries. Mutation `continue` to `break` at line 490 passes. Every case in `test_irrevocable_entry_voids_only_its_writes` puts the irrevocable kind or entry after the good one. Add `["transmit","commit"]` and an irrevocable entry first. The `break` would lose a good write (fail-narrow, no widening) but would break the "other entries stay in force" claim.

L3. Mixed entry. Mutation `branches = item["branches"] if kind == "commit" else []` to `item["branches"]` (line 497) passes. No test has `kinds: [commit, post]`. Harmless today, because `read_grant` in guard.py (line 488, `(kind == "commit") != bool(branches)`) drops a post with branches, so the guard refers it. But the guard is the only thing stopping a wrong write, so the module's defense has no test. Add a mixed entry and assert the post write has `branches == ()`.

### Preference

P1. `irrevocable()` is named like a predicate but returns a reason string. Rename to `why_irrevocable`. Cosmetic.

P2. `entry_problems` for bad `kinds` also adds "branches without commit" (the kinds are reset to `[]`). The message is noisy but harmless.

## Check 1: code against intent

Traced `read_one` to `entry_problems` to `read_authorizations`.
- Malformed entry: any problem from any entry goes into `problems`, and the authorization goes to `errors`. `continue` skips its writes and `raise ValueError` follows after the loop. The entire authorization is void, and so are the other named ones (the exit is 1). Verified by mutation: removing the `raise` fails 39 tests.
- Irrevocable: `irrevocable()` runs only after the entry is known well formed (no problems, so `provisioned` is a bool and `kinds` are valid). It runs per kind and before the `MATCHED` test. `publish` and `transmit` are referred with GUARD.11. An unprovisioned destination refers every kind of that entry, including `other`. Other entries and kinds append a `RemoteWrite`.
- Per-action: still referred before the loop. Expiry is carried as before.
- I found no path where an irrevocable or malformed entry opens a write. Mutations disabling either irrevocable test fail 2 and 4 tests. Removing the MATCHED test fails 1.
- Exceptions: only M1.

## Check 3: security

Only `authorizations.py` changed under `govharness/`. `hooks/guard.py`, `claude_code.py` and `cli/` are unchanged, so the guard's matching, the ask rules and the policy shape are as at 1b8849b. The guard reads only the policy's `remote_writes` and re-tests expiry, so it never sees `referred`.
The one change in reach: an authorization that 1b8849b rejected whole because of an irrevocable or unprovisioned entry now opens the commit and post entries that are revocable and provisioned. This is the intended widening, and the owner must name the authorization with `--authorization`. The reference to a kind or entry that the owner "expected to be void" is the risk. The coverage report lists each voided kind (`referred`). `print` of `reading.summary` still lists all entries including the irrevocable ones; the summary line does not mark which are voided. It is a Low preference to mark them there, since the owner compares the summary with what was granted.
Duplicate entries at one destination: each is judged alone, and the guard matches any grant, so one provisioned entry stands beside an unprovisioned one. This agrees with "each entry on its own".

## Check 4: record against code

- Unit 0008 DoD 2, 3, the Revision section and the audit list agree with the code and with `apply_harn_1_2.py` (rows Standing and Form, Notes lines 80-84). The ask rules stay (`claude_code.py:214-224`), and `AUTHORIZED_RULES` does not exist.
- Ruff 0.16.10, line length 79, run by me: no finding on `authorizations.py`, `inputs.py`, `cli/environment.py`, `test_authorizations.py`; 7 on `guard.py` (4 TRY004, SIM102, B023, SIM114); 21 ISC004 on `claude_code.py`. These match the record. I could not check "six were there before" (no git history run of ruff at 917f1b5).
- Review list: all six named files exist.
- The audit names `test_irrevocable_entry_voids_only_its_writes` and `test_malformed_entry_fails_closed`; both exist.
- Stale (Low): `records/decisions/0002-environment-derivation.md:76` still reads "Dropped while an authorization of kind commit is derived", while line 83 states the rule stays. Check that line 76 is marked superseded.
- Unit 0008 item 5 says "see the suite run recorded in the work report" and gives no count. The commit message says 188 tests.

## Check 5: suite

`python3 -B -m unittest discover -s tests` in `harness`: 188 tests OK (228 s). Derive authorization tests alone: 17 OK.

## Not checked

The rehearsal (`govharness rehearse`) and the claims of 25 entries / "verify passes". The HARN.29 text as applied to the governance ledger (I read only the script). Guard tests at the hook level for a policy produced from a mixed authorization. Behavior of Claude Code on `allow` against an ask rule (the unit's open installation test). The ruff history claim.
