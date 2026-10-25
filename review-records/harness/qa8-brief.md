# QA.8 review of the whole harness: brief

This is the code review of the whole harness that item 9 of the definition of done of 2026-10-25 asks for (`review-records/round-2026-10-25-close/definition-of-done.md`), after units 0009 to 0014 were merged. It is held under QA.8 (review independence): the reviewers are agents of another configuration than the authors. Three reviewers each read one disjoint part of the code at main (6391253 or later).

**Before you start.**
- REPO is `/home/brianm/projects/utils/governance-harness`, and the harness is `REPO/harness/` (standard library only; run from `harness/`).
- Read `harness/README.md`, `REPO/CUSTODIAN.md`, and the unit records of your part in `harness/records/units/`. Earlier reviews are in `harness/records/reviews/` and `review-records/harness/`: do not report again a finding that they record as fixed, unless it has come back.
- **Do not edit any file except your report.** Keep scratch files, copies, and mutated trees in your own new directory `/tmp/claude-1000/qa8-<part>/`. To test a change, copy the tree there.
- **Tests:** run the tests of your part (`python3 -B -m unittest tests.<module>`), and the ones a probe needs. Do not run the full suite; the lead runs it.
- **Never:** read credentials, keys, or secret stores (`~/.ssh`, `~/.gnupg`, any token or `.env` file, the secret store the configuration names); use the network; run anything as root or with sudo; write under `/etc` or `~/.claude`; push or post anything. z3 is not installed; its path is tested by stubs only.

## Severity

- **High:**
  - a check passes a corpus that breaks the rule it checks, or fails a valid corpus, on input the corpus can hold;
  - a guard or derived configuration admits an action it is meant to deny or refer;
  - the ledger or a signature can be altered without `verify` failing;
  - data is lost.
- **Medium:**
  - a defect on a reachable path that has a workaround;
  - a test that does not hold a behavior its record or the README claims (show the surviving mutation);
  - a loud-failure or fail-closed rule that fails open.
- **Low:** the rest, including clarity, dead code, and documentation that disagrees with the code.

Give each finding with its file and line, a concrete input or reproduction, and the fix. Do not report a style preference as a finding. Say what you checked and found sound, briefly.

## Parts

| Part | Code (`harness/govharness/`) | Tests (`harness/tests/`) | Focus |
| --- | --- | --- | --- |
| A | `hooks/`, `derive/environment/` | `hooks/`, `derive/test_environment.py`, `derive/test_authorizations.py` | The guard: every bypass of a deny or a referral (shell parsing, quoting, git configuration and environment variables, path forms, symbolic links), and fail-closed behavior on malformed input. The derived configuration against INSTALL.md and STND.HARN (unit 0014). |
| B | `ledger/`, `core/`, `cli/`, `workflows/`, `derive/*.py`, `query/` | `ledger/`, `cli/`, `workflows/`, `query/`, `derive/test_reading_copy.py` | Ledger integrity: the hash chain, signatures, `--accept-unsigned` and the signer register (unit 0010), `record_transaction`, rehearse, and the expiry horizon (unit 0012). Corpus reading, the reading copies, the solve store, and retrieval. |
| C | `checks/` | `checks/`, `equivalence/`, `test_architecture.py`, `test_conventions.py` | Each check against the provision that it says it checks. The solver (unit 0009) and the solve cache (unit 0011): soundness of each reused result. g.25 (unit 0013). Registry and severity models. |

Write `REPO/review-records/harness/qa8-part-<a|b|c>.md`, under 1,800 words. In your final message, give your High and Medium findings, one line each.
