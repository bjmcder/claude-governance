# Review 0009: QA.8 review of the whole harness

The code review of the whole harness that item 9 of the definition of done of 2026-10-25 asks for, held under QA.8 after units 0009 to 0014 were merged. Reviewers: three agents of another configuration (Claude Sonnet) than the authors, each over one disjoint part (`review-records/harness/qa8-brief.md`). Each fix unit was reviewed again, independently, before its merge.

## Parts, findings, and fix units

| Part | Code | Report | Findings | Fixed by | Unit review |
| --- | --- | --- | --- | --- | --- |
| A | `hooks/`, `derive/environment/` | `review-records/harness/qa8-part-a.md` | 7 High, 7 Medium, 3 Low | unit 0015 | `review-unit-0015.md` (rejected; N1 to N8), `rereview-unit-0015.md` (rejected; R1 to R10) |
| B | `ledger/`, `core/`, `cli/`, `workflows/`, `derive/*.py`, `query/` | `review-records/harness/qa8-part-b.md` | 3 High, 6 Medium, 8 Low | unit 0016 | `review-unit-0016.md` (accepted; M-A, M-B fixed) |
| C | `checks/` | `review-records/harness/qa8-part-c.md` | 2 High, 5 Medium, 9 Low | unit 0017 | `review-unit-0017.md` (accepted; M-A, M-B fixed) |

The records of the fixes are `harness/records/units/0015-guard-fixes.md`, `0016-ledger-fixes.md`, and `0017-checks-fixes.md`.

## Outcome

- **Part B and part C:** every High and Medium finding is fixed and verified, or handled by the ruling below. The fix units' reviews found no High finding; their Medium findings were test gaps and one unsigned register path, and each is fixed and its mutant rerun.
- **Part A:** every High and Medium finding of the QA.8 report is fixed, and so are the first unit review's findings N1 to N8 and the re-review's timing regression R1.
  - The re-review's other findings, R2 to R10, are not fixed. Each is a further way to write a command that the guard does not read, most of them unread on main as well.
  - On 2026-10-25 the custodian decided to stop the guard work at this bounded point. R2 to R10 stand as known limits of the guard, named in record 0015, in the guard's coverage table, and in the README.
  - The guard is one layer: the sandbox and the session's permission rules stand behind it.
- **Ruling of the lead, applied in units 0016 and 0017:** the harness implements the corpus as written. Where a finding showed the corpus wrong or silent (STND.HARN.9 pins, the term Accepted signature, STND.IDENT.12 for drafts, files under no scope, and others), the code follows the letter, and the question goes to `OPEN-ITEMS.md` for a later round, with draft wording in the unit record.

## Not checked

z3, which is not installed. The installed hook under a real Claude Code session, which is the human owner's step (`tools/install-tests.md`).

## Conduct

- Two reviewers of the guard each once ran probe lines in their own shell, through a here-document whose body held its delimiter. The lead checked each time: `~/.gitconfig` held only its `[user]` section, the repository has no remote, and main and the worktrees were unchanged.
- During the fourth pass a safety classifier stopped the implementer, which was running bypass inputs through a sandboxed shell. From then on, inputs were passed to the guard only as data.
