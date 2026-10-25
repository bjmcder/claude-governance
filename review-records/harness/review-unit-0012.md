# Review of unit 0012 (expiry horizon), commit 489a680

Verdict: the change is correct and fails closed. One Medium and two Low findings; no High.

## Checked and sound

- Default 90 days (`DEFAULT_HORIZON`) in both the CLI and `read_authorizations`; `none` gives `None`; `until revoked` is refused under any bound (authorizations.py `read_one`).
- Boundary: `moment - now > horizon` accepts exactly 90 days, refuses 90 days plus a second. Both datetimes are aware, so offsets such as +14:00 compare correctly; naive expiries are refused by `timestamp`. No overflow: nine digits equal `timedelta.max.days`.
- Malformed values: I ran the CLI with `0 -5 +90 "" " 90" 9_0 ٩٠ 90d NONE` and ten digits. Each exits 2 with the reason and no traceback. `090` and `none` are accepted. `--expiry-horizon -5` as a separate token also works.
- No path bypasses the horizon. `read_one` applies it whatever `--accept-unsigned` says. `--check` re-derives through `authorized`. `rehearse` never reaches the environment code. A direct `read_authorizations` caller gets the default; passing `None` is an explicit opt-out.
- Hook: the commit touches nothing under `govharness/hooks`, and the horizon can only remove writes from the derived policy. Nothing is widened.
- Records: README, unit 0008 (M5 and Cold review), decision 0002, and the unit record match the code. The "no amendment" reasoning for STND.HARN.29 is consistent.
- Mutations I ran on a copy, all caught: `>=`, a one-day-looser bound, a default of 91, zero accepted, CLI default `None`, no positivity check, a loosened "expired" test.

## Backward compatibility

Refusing `0`, `-5`, `+90`, blanks, `9_0` and non-ASCII digits is right. `0` and negatives already refused every authorization. An owner who typed `0` to mean "no bound" now gets a usage error, not a silent opposite. The rest were accidents of `int()`. The behavior change is the intended one (a derivation that relied on an unbounded expiry now exits 1) and the unit record says so.

## Findings

### Medium

**M1. The command tests read the real clock, so they will fail from 2027-01-01.**
`tests/derive/test_authorizations.py`: `FIELDS["expires"]` is `2027-01-01T00:00:00+00:00` (line 69), and the command tests call `main()` while the command uses `datetime.now(timezone.utc)` (cli/environment.py:259). Seven tests are affected: the `@no_anchor()` ones at 718, 848, 965, 1039, 1113 and 1363, plus `test_command_verifies_signatures` (1144, which patches inline). Scenario: after 2027-01-01 they fail as "expired", and `test_command_horizon`, which uses the real `now`, hides the problem.

Fix, standard library only, in the same style as `no_anchor()`. I applied it to a copy at /tmp/claude-1000/review-0012/h. Add near `no_anchor`:

```python
class FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW.astimezone(tz)

def frozen_clock() -> mock._patch:
    return mock.patch("govharness.cli.environment.datetime", FrozenDatetime)
```

Stack `@frozen_clock()` above each `@no_anchor()` and above `test_command_verifies_signatures`. In `test_command_horizon`, use `now = NOW`. The module imports `datetime` only for that one `now()` call, so the patch is narrow. Check: I moved `FIELDS["expires"]` to 2026-10-24T18:00Z (after `NOW`, before the real clock). Unpatched, 4 errors and 1 failure; patched, all pass except one that my own change broke. A cleaner follow-up is a `now` parameter on `authorized`.

### Low

**L1. The tests do not exercise a non-UTC offset against the horizon.**
Mutation `moment.replace(tzinfo=None) - now.replace(tzinfo=None) > horizon` survives (OK, 37 tests). The code is correct today. Fix: add a case to `test_default_bound`, such as `NOW + 90 days` written as `+14:00` (accepted), and the same plus one minute (refused).

**L2. `--check` against a configuration installed with `none` fails under the default.**
Fail-closed and documented in the README and the record, but the failure text is the horizon reason, not "pass the horizon you used". The exit is 1. The reason already names `--expiry-horizon none`, so this is acceptable. Optional: say so in the `--check` help.

## Suite

`python3 -B -m unittest discover -s tests` from WT/harness: 247 tests, OK (203 s), matching the unit record.

Not in scope: `OPEN-ITEMS.md` item M-b stays open until merge, as the record says. The verification file calls the finding M-c; the commit message and record map it to M-b of OPEN-ITEMS correctly.
