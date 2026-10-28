# Round o of 2026-10-28: cold verification of the review fixes

Reviewer of another configuration, on commit bfa2b68.

## What I ran

Rounds a, d, c, and o applied to `/tmp/claude-1000/rvo2/governance` (seq 244 to 286). `verify`: every check PASS, logic PASS with the standing g.18 warning. `onset`: CSQ0 2, CSQ1 22, CSQ2 157, CSQ3 620, as `decisions.md` states. All 774 rows match the fields written (765 classes, 9 `null`). `tests.checks.test_onset`: 16 pass. A copy with one field removed fails `verify`: "a waivable provision without an onset".

## D1 to D3

- D1 closed. STND.CREW.11, STND.WPROC.7, and .8 carry CSQ3 with the source "C7 rule: a protocol rule, not its verification (DSGN.15); was CSQ2"; both documents are minor (1.3); the moves table, point 2, and their Notes name them.
- D2 closed. STND.ANNEX.1 is `null`; no other MAY-only provision carries a class.
- D3 closed. The definition admits CSQ0 to CSQ3 and `null`; `parse_onset` refuses CSQ4; STND.CODE.20 is `["CSQ3", ["sentence 1", "CSQ1"]]`, and the STND.CODE Notes say the marker reaches work of CSQ3, agreeing with STND.CLASS.10. STND.CLASS.21 carries the proposed text.

## Re-sample

60 rows: the 8 found wrong; the other rows of their kinds (reports, limits, records, and oracles kept at CSQ3 in AGENT, HW, HW.CPU, NUMER, ML, CPS; the four other permissions; the nine kept hardware forms, four moved STND.ANNEX defaults; STND.OMP.2, STND.CODE.20; seven protocol rules at CSQ3); and nine others. Wrong: none, 0 of 60. Each kept departure's reason now stands in its Notes.

## The hardware forms

Settled: STND.ANNEX.2 and .4 to .10 move to CSQ2 with HW.4 to HW.6 (STND.ANNEX 1.1, minor); STND.ANNEX.1 is a permission; the nine kept at CSQ3 are listed under point 1, each asking a setting, a run, or a scope that needs no contract, with a reason sentence in each of their six documents.

## Readings

Points 1, 2, 3, and 4 (point 7 of the first draft) remain, each a true choice; the rest are settled.

## Findings

No defect, no should-fix. Optional:

1. STND.CONC.3 and STND.MPI.20 (HW.11, CSQ2) at CSQ3, and the row STND.CXX.4 of STND.STDC.1 (HW.5), are forms of the same kind, unchanged by the round, without the reason sentence; add them to point 1 or to their Notes.
2. Row 'HW.CPU.5' keeps the source `Notes of HW.CPU: CSQ3` though point 1 lists it as a kept tightening; use `Notes of HW.CPU: CSQ3, a tightening kept, reason in the Notes: a report (INTPR.7 row)`.
