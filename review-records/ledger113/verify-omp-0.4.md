# Delta verification of STND.OMP draft 0.4

**Verdict: not ready.** One blocking item (N1). Three short wording fixes are advised.

Mechanical checks: `verify` passes. `findings.py` shows only the nine expected g.18 notices. The rehearsal bodies and titles of OMP.12 and OMP.16 match the reading copy. All diff hunks are covered. The new text has no banned word.

## Items to status

| Item | Status | Reason |
| --- | --- | --- |
| B1 (OMP.12 S3) | verified | "Use an atomic construct to access a location that a handler accesses" is unambiguous and does not clash with S1 or OMP.22. |
| B2 (undeprecation) | partly | The exception matches r1. "Among them" now attaches to the wrong noun (N2). |
| B3 (ICV values) | verified | "Most (r2)" fits r2's seven ICVs. |
| B4 (CONC.24) | partly | Correct, but it drops the "or each number" alternative (N3). |
| B5 (RATIONALE) | verified | See below. |
| S1, S2, S6 | verified | Title, handler reason, and OMP.1 Notes are fixed. |
| S3 default device | verified | Marked unverified. |
| S4 threadprivate | verified | "Nothing assures" matches r2 rule 8. The qualifier is marked as an inference. |
| S5 fork | partly | The Examples are cited, but the verb disagrees (N4). |
| S7 OMP.16 S1 | not verified | The new wording creates a conflict (N1). |

## Blocking

- **N1. OMP.16 S1 against S2.** S1 now says "each run of that code that produces a reported result SHOULD have cancellation enabled". S2 asks for test runs with cancellation disabled. A test run reports a result, so a reader can place it under S1 and find a conflict. The 0.3 text excluded those runs. "Reported result" is also undefined and unsupported by the research. Restore the exclusion in a form that is not a second condition, for example by moving it into S2 as "except for the run that shows the disabled state".

## Should-fix

- N2. Notes, paragraph 2: "other than one form of the destroy clause ... that it undeprecated, among them the master construct" misattaches "among them". Put the exception last. r1 says "argument-less destroy".
- N4. Notes, fork sentence: "The Examples ... warn ... and points". The verb should be "point".

## Preferences

- N3. Restore CONC.24's alternative: "three or more numbers, or each number the component admits if fewer".

## RATIONALE

It says 33 provisions. Its eight ranges (1 to 4, 5 to 8, 9 to 13, 14 to 16, 17 and 18, 19 to 22, 23 to 30, 31 to 33) cover them exactly. Its wording matches 0.4, and the ending is complete. "No conflict that remains" holds only after N1 is fixed. The review list names the pair review of the changes and the cold verifications. Add this verification if it is to be recorded.
