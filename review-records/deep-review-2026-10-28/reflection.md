# Reflection: following the governance while doing this work

The custodian asked that the work of 2026-10-28 follow the governance, and that the unexpected blockers be reported. This record says where the corpus as written would have stopped the work, and what was done instead. Several points are first-hand evidence for the rulings in [rulings.md](rulings.md).

## Where the defaults would have stopped the work

1. **Operating cost (A1).**
   - The work ran about twenty agents on two models. No estimate of their cost was stated beforehand, and none was authorized.
   - Under PRIME.8 and GUARD.14, read strictly, no unit should have started.
   - The custodian's request named the agents and their models, and that was treated as the authorization. That is reading (c) of A1. It is not written anywhere in the corpus.
2. **Write bounds (A5).**
   - Every agent wrote scratch copies, virtual environments, and test clones under the session's scratch area in `/tmp/claude-1000/`, outside the top directory of the work.
   - Under the default working bounds, each of those first writes is a halt and a referral (STND.DFLT.25).
   - The work used the scratch area, because a scratch copy is the safer place for rehearsals and mutation runs.
3. **Bulk and destructive actions (A2).**
   - Builds, test runs, `pip` installs into scratch venvs, and worktree checkouts overwrote outputs that no one listed by path beforehand.
   - Deleting the stale documents and the equivalence guard was a destructive action, enumerated only by the commit that made it. The custodian's standing direction on cleanup covers the deletions, and git history is the recovery path.
   - Nothing in the defaults treats a configuration or a commit as the list that STND.DFLT.24 asks for.
4. **Ledger entries (A3).**
   - Recording the custodian's rulings of this cycle will need entries that name the custodian or the human owner as actor.
   - Only grants have a scribe route today.
   - The rounds of 2026-10-26 and 2026-10-27 recorded ratifications through amendment scripts that the custodian approved. That path stays available, but it is not the light route the defaults should offer.

## Instruction authority (B1)

- **Briefs:** the briefs to the agents direct them. That is allowed under PRIME.11, as direction "within an authority traceable to a directive of the human owner".
- **Skills:** the plugin's skills were written as information, not as directions. As B1 explains, under the literal reading of PRIME.11 a directing skill would have to be listed in every completion report of every adopting project.
- **Repository files:** the root `CLAUDE.md` and `AGENTS.md` of this repository point to `for-agents/` rather than giving rules. They are written that way for the same reason.

## Independence of review

- **Configurations:** QA.8 asks that a reviewer be of another agent configuration. Each review alternated the model of its author: Opus reviewed Fable's work and Fable reviewed Opus's.
- **What C6 would settle:** whether that is the right test at each class is an open question (C6). Within one model, only the brief and the session differed.

## Practical blockers

1. **No validator:** there is no `claude` binary on this machine, so `claude plugin validate` could not run. The manifests were checked against the documented schema by script and by reading the pages.
2. **No remote:** the marketplace install path cannot be exercised end to end. Only local paths were tested (F3).
3. **The offline path:** `pip` and `pipx` installs of `harness/` fetch setuptools unless a build backend is already present. The offline path therefore uses `PYTHONPATH`, with no install.
4. **Rulings before rounds:** the standing process puts the custodian's decisions first in a round. The custodian asked for all rulings together at the end of the cycle. So the corpus amendments are drafted after the rulings, not during this cycle, and nothing in `harness/governance/` changed.
5. **A first fix that broke a binding provision:** the first version of unit 0022 cut long sections in `context` to fit the budget. The code review caught that this broke STND.HARN.3, which asks for each text whole or named. The cut was removed.
   - Lesson: a convenience change to the harness is checked against the binding text of STND.HARN, not only against its tests.

## What went as the process intends

- **Separation of work:** every change was made on a branch, and in an isolated worktree wherever two agents worked at once.
- **Tests and verification:** every change was tested, independently reviewed, fixed, and verified again. `verify governance` passed after each step, with only the warning the corpus already carries.
- **Corpus untouched:** no corpus text changed without ratification.
