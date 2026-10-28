# Reflection: the rounds of 2026-10-28

The custodian asked that the work follow the governance and that unexpected blockers be reported. The [reflection on the deep review](../deep-review-2026-10-28/reflection.md) covers the review cycle. This record covers the five amendment rounds that carried its rulings, from drafting to the apply at ledger entry 322.

## What the process caught

1. **A binding provision lowered by a convenience reading.**
   - The first draft of STND.HARN.24 confirmed only the checks that a provision names in `checked_by`.
   - That dropped the default, logic, and onset checks from what a change must pass. The cold review caught it.
   - The lesson of unit 0022 holds again: a change made to fit the harness is checked against the binding text, not only against the harness.
2. **An obligation placed in a Note.**
   - Reading c.5 was first drafted as a Note that tightened the auditor rows of STND.CLASS.19.
   - Notes carry no obligation, so the verification of the reconciliation moved it into the row.
3. **A ruling with no record.**
   - Reading a.1 is an interpretation of PRIME.7 that binds every project, and no round recorded it.
   - The reconciliation review caught this, and the interpretation is now ledger entry 204, of type `rule`.
4. **A reading left with no one.**
   - Round o deferred its reading 9 to round e, and my first direction to round e's drafter sent it back to round o.
   - The cold review of round e caught the gap, and the reading became e.6.
   - Deferrals between rounds need a register that the lead keeps, not only each round's own record.

## Unexpected blockers

1. **Tests that read the live corpus.**
   - The full suite passed before the apply, and 15 tests failed after it.
   - Many tests pin facts of the live corpus: the GOV.48 sentence, the absence of onset fields, the count of provisions in STND.PY, and the place of the spelling table.
   - The rehearsal runs every check on the amended copy, but not the test suite, so these failures surfaced only after ratification.
   - For later rounds: run the suite against the rehearsed copy before ratification, or keep facts of the live corpus out of tests that guard behavior.
2. **A gap the rounds created and no review found.**
   - Round c made the adopted classification at CSQ3 and CSQ4 the promotion of results (QA.11). GOV.20 gives a constitution to every project that promotes a result.
   - The reconciliation review's walk of a CSQ4 and a CSQ3 unit did not catch this. The documentation update found it, when it re-derived the human acts by class from the text.
   - It is listed in `OPEN-ITEMS.md` for a later round, since the fix changes LVL0.
   - For later rounds: a burden walk reads each changed LVL0 provision against every provision that cites the term it changes.
3. **The order of the rounds.** Ruling F2 put classes before the language standards, but round c's edits are anchored on round d's text. The driver departs from the ruled order, and the departure was put to the custodian (item 0.2 of the packet) rather than left in a docstring.

## What went as the process intends

- **Review:** every round had a cold review, a pair review, fixes, and a cold verification, by an agent of another configuration. The reconciliation review read the five rounds together.
- **Rehearsal:** the apply on the live corpus reproduced the rehearsal's final corpus hash exactly.
- **Ratification:** the custodian ruled once, on one packet: 27 readings and 2 confirmations, each with context, options, and a recommendation.
