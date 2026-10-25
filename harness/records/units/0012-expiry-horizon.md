# Unit 0012: expiry horizon

The security verification of unit 0008 (`review-records/round-2026-10-24/harn-auth/verify-security.md`, M-c, "unbounded expiry by default"; M-b of `OPEN-ITEMS.md`) found that `environment --expiry-horizon` had no default, so an authorization whose expiry is `until revoked`, or lies years ahead, was accepted unbounded. A revocation reaches an installed configuration only when it is derived again; until then only an expiry, which the guard tests at each write, ends the reliance. Unit 0010 closed the other residual of M-c. The definition of done of 2026-10-25 (`review-records/round-2026-10-25-close/definition-of-done.md`, item 7) asks for a default of 90 days, unless the custodian names another, and for `--expiry-horizon none` to lift it.

## Definition of done

1. `environment --expiry-horizon` defaults to 90 days. Where `--authorization` names an authorization whose expiry lies more than the horizon after the derivation, or that lapses only when revoked, the derivation exits 1, writes nothing, and prints the reason, beside every other reason of STND.HARN.29; it raises no uncaught exception.
2. `--expiry-horizon none` lifts the bound, and only then is `until revoked` accepted. An explicit number of days bounds as before.
3. A value that is neither whole days from 1 nor `none` is refused with the reason, and no exception escapes.
4. The summary line of each authorization names the horizon in force.
5. Each criterion has a test; every earlier test passes, and a test that relied on there being no default is changed with the reason stated; ruff at 79 columns adds no finding on the changed files.
6. The README, unit 0008, and decision 0002 record the change, and this record states whether STND.HARN.29 needs an amendment.

## Record

- Done, in `derive/environment/authorizations.py`:
  - `DEFAULT_HORIZON` (90 days) and `NO_HORIZON` (`none`).
  - `parse_horizon` takes `none`, or one to nine ASCII digits whose value is at least 1, and raises `ValueError` with the reason otherwise. Nine digits is at most `timedelta.max.days`, so no value overflows. Zero is refused rather than read as no bound: it would admit no expiry, and an owner who means "no bound" by it would get the opposite of what was meant.
  - `horizon_text` names the horizon for the summary and the reasons.
  - `read_authorizations` now defaults `horizon` to `DEFAULT_HORIZON`, so a library caller that names none gets the bound too; None still means no bound. It refuses a horizon of zero or less with the reason. In `read_one`, `until revoked` under a bound is refused with "beyond the expiry horizon of N days (--expiry-horizon none lifts it)", and an expiry beyond it with the expiry, the horizon, and the two ways on. The comparison is `moment - now > horizon`, not `moment > now + horizon`, so no horizon overflows the calendar.
  - The summary line reads `...; expires X, under the expiry horizon of N days; ...`, or `under no expiry horizon (--expiry-horizon none)`.
- Done, in `cli/environment.py`: `--expiry-horizon` takes `expiry_horizon`, a type that wraps `parse_horizon` and raises `argparse.ArgumentTypeError`, so a malformed value is a usage error (exit 2) with the reason, as `corpus_root` does for the root. Its default is `DEFAULT_HORIZON` and its metavar `DAYS|none`. `authorized` passes the parsed value through.
- Backward compatibility: an explicit number of days keeps its meaning, from the derivation, with the same boundary (an expiry exactly the horizon away is accepted). What changes:
  - A derivation that named an authorization expiring more than 90 days ahead, or `until revoked`, without the option now exits 1 and needs `--expiry-horizon N` or `none`. That is the fix.
  - `int` used to accept `0`, `-5`, `+90`, ` 90`, `9_0`, and digits of other scripts. Zero and negatives already refused every authorization; the others are now usage errors.
  - A value of 2.9 million days or more ended the command with an `OverflowError` traceback, from `timedelta` or from `now + horizon`. Up to nine digits now works; more is a usage error.
  - `--check` needs the horizon its derivation was given, since it derives the configuration afresh.
- Tests, in `tests/derive/test_authorizations.py`, the class `Horizon`:
  - `test_default_bound`: with no horizon passed to `read_authorizations`, an expiry 91 days after the derivation is refused with the horizon named; 89 days and exactly 90 days are accepted; the summary names the horizon.
  - `test_until_revoked_needs_none`: `until revoked` is refused under the default, with the way to lift it, and accepted under none, whose summary says so.
  - `test_explicit_horizon`: 30 days refuses an expiry 100 days ahead, 120 days accepts it, and the summary names 120 days. The longest horizon (`999999999`) accepts an expiry in 9999 without overflow and still refuses `until revoked`.
  - `test_parse_horizon`: `none`, `1`, and `090` parse; `""`, `0`, `000`, `-5`, `+90`, `9.5`, `90d`, `1e3`, blanks before or after, `None`, `NONE`, Arabic-Indic digits, `9_0`, and ten digits are refused with the reason.
  - `test_horizon_not_positive`: a horizon of zero or less given to the library stops it with the reason.
  - `test_command_horizon`: the command on a corpus copy, against the real clock. By default, an expiry 200 days ahead and `until revoked` each exit 1 with the reason and write nothing. `--expiry-horizon 365` accepts the first and `--expiry-horizon none` the second. An expiry 30 days ahead passes by default. The printed summary names the horizon in force each time.
  - `test_command_malformed_horizon`: `abc`, `0`, `-5`, `None`, and twelve digits each exit 2 with the reason and write nothing.
- Earlier tests changed, with the reason. The helpers `reading` and `full_reading` default `horizon` to `DEFAULT_HORIZON`, as the command does, rather than None. The expiry of `FIELDS` (2027-01-01, 68 days after `NOW`) lies within it, so every test of a row of STND.HARN.29 still tests its row alone. `test_until_revoked_and_horizon` relied on there being no default: its first reading now passes `horizon=None`, the owner's `none`, since `until revoked` is refused under the default. Its last assertion now matches "beyond the expiry horizon of 30 days", because the reason names the horizon.
- Mutations, each checked by patching it in turn and running the test file. Each one fails at least one test:
  - CLI default None: `test_command_horizon`.
  - Library default None: `test_default_bound`.
  - `until revoked` accepted under a bound: four tests.
  - `int` in place of the digit pattern: `test_parse_horizon`, `test_command_malformed_horizon`.
  - `moment > now + horizon` in place of the difference: `test_explicit_horizon`, with an `OverflowError`.
  - Summary without the horizon: four tests.
  - No check that the horizon is positive: `test_horizon_not_positive`.
- Suite: `cd harness && python3 -B -m unittest discover -s tests` ran 247 tests, OK (201 s). Unit 0011 ended at 240; this unit adds seven.
- Ruff 0.16.10, with the settings it resolves for the tree, reports no finding on `derive/environment/authorizations.py`, `cli/environment.py`, or `tests/derive/test_authorizations.py`. With `--line-length 79 --select E501` added, it reports 1 on `authorizations.py` and 6 on the test file. These are the same lines as at ac2e275, where this unit starts, moved down by the lines added above them; the lines this unit adds are within 79 columns.
- STND.HARN.29: no amendment is needed for the harness to conform. The row Dates asks only that an expiry, where there is one, be later than the write, and the field `expires` of STND.PROJ.6 admits `until revoked`. The default makes the code stricter there, failing closed, as unit 0008's record notes for other rows: a refused derivation leaves the write referred, which STND.HARN.18 allows. Under `none` the code relies on exactly what the provision admits. I do not propose that the provision fix 90 days or any other number. That is a parameter of a harness, not a test of an authorization. Making it binding would need a floor argument (GOV.11), and lifting it would be a further act of the human owner, putting STND.DRAFT.42 to the custodian again, as STND.HARN.30 does. The Notes should still say why an expiry matters, since they state the interval a revocation leaves open but not what bounds it. Item for the custodian, for the lead to route to package P4 (which amends STND.HARN for STND.HARN.30), named **P4 routing: STND.HARN.29 Notes, expiry horizon (unit 0012)**. It is an editorial amendment (STND.IDENT.3: it alters no obligation, permission, or defined meaning), and it may ride in P4's minor amendment of STND.HARN. Not made here:
  - Notes of STND.HARN.29, after the sentence that ends "and the coverage report of STND.HARN.19 states the interval.": "Only an expiry bounds that interval, since it is tested again at each write, and an authorization that lapses only when revoked leaves it unbounded. A harness that refuses at the derivation an authorization whose expiry lies beyond a horizon that the harness states, or that lapses only when revoked, still meets STND.HARN.29, because the write is then referred, which STND.HARN.18 allows."
  - Revision row, or a clause of P4's row: "Editorial amendment: STND.HARN.29, Notes: only an expiry bounds the interval in which a configuration relies on a revoked authorization, and a harness that refuses an expiry beyond a horizon it states still meets the provision."
- Not changed:
  - The guard and the policy. The horizon applies at the derivation only; the guard still tests each entry's expiry at each write.
  - The coverage report and the draft entry. They do not name the horizon, so that the rendering, and `--check`, do not depend on it beyond which authorizations are in force.
  - `OPEN-ITEMS.md`. Its item M-b stays until the lead or the custodian closes it at merge.
  - The template `_PROJECT/NAME/AUTH/1.md` (`harness/governance/` is out of scope). Its fill-in guidance still names `until revoked` as a value of `expires`, which stays valid under STND.PROJ.6.
- Open: the command tests read the real clock (`datetime.now`), and the expiry of `FIELDS` is 2027-01-01. From that day on, `test_command_option` and the other command tests that use `FIELDS` fail as expired, as they would have without this unit. `test_command_horizon` computes its expiries from the clock and is not affected. A later unit could pass the time to `authorized`, or patch it in the tests.
- Audit:
  1. Met: `test_default_bound`, `test_command_horizon`.
  2. Met: `test_until_revoked_needs_none`, `test_explicit_horizon`, `test_command_horizon`, `test_until_revoked_and_horizon`.
  3. Met: `test_parse_horizon`, `test_command_malformed_horizon`, `test_horizon_not_positive`.
  4. Met: `test_default_bound`, `test_until_revoked_needs_none`, `test_explicit_horizon`, `test_command_horizon`.
  5. Met: see the tests, mutations, suite, and ruff items above.
  6. Met: README (environment row and the bullet on remote writes), unit 0008 (items M5 and Cold review), decision 0002 (a table for this unit), and the item on STND.HARN.29 above.

## Review

Left for the reviewer.
