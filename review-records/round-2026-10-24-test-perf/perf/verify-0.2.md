# Cold verification of STND.PERF 0.2 (2026-10-25)

**Verdict: not ready. Three small defects (D1 to D3); the rest is Should-fix and Optional.** No conflict and no unowned matter found.

## Checked by script
- `verify`: eight of eight PASS. `findings.py 'STND\.PERF'`: none (the one g.18 warning is STND.OFFLD.7).
- The 26 bodies equal `content_perf.py`, the rehearsed copy and `draft-0.2.md`. At most two modals, one per sentence; no banned word; body IDs equal `instantiates` plus `refers_to`; titles 2 to 5 words, unique in the corpus; an LVL0 ancestor each; every named document is in References.
- RATIONALE ends with the fixed tail.
- Pairs: regenerated list equals `pairs-0.2.md` (590). Against `pairs.md` (596), exactly 13 are added (the delta file) and 19 dropped (all PERF.5).

## Dispositions
All rows do what they say; I read the changed text for each. Only PERF.5 changed title. The Notes are 2,766 words, as claimed.

**O4 (PRIME.2): the rejection holds.** The harness forces the binding mark when the `instantiates` closure reaches PRIME, and fails a non-waivable default (GOV.17). Citing PRIME.2 would make PERF.21 binding, against the all-default direction (OPEN-ITEMS line 18). It would also raise the floor beyond NUMER.26, which reaches stochastic results only (GOV.11). GOV.19 says "binding only where", so the forcing is the lineage rule. Optional: cite GOV.17 and GOV.11 in the disposition, not only the custodian.

## Defects
- **D1. Obligations in the indicative in the Notes, with no provision** (as OFFLD B4).
  - "A fallback, a throttle, or another event of HW.9 during a sample enters the exclusion criterion of STND.PERF.18 or the record of the sample."
  - "Variation of time within the practical threshold ... is no defect, by the reasoning by which STND.VVUQ.82 ..." p1 lists the reach to time as open.
  - "the plan of the parallel work sequences a unit that needs the machine alone ..." Pair S4 asked for it in the provision.
  - Fix: recast as reasons; mark the VVUQ.82 point as an analogy that PERF does not adopt; cut the sequencing sentence or put it in PERF.26 s1.
- **D2. PERF.21 s2 has two conditions in one sentence** (OFFLD B3). Fix: "After the removal of a cause outside the code that the record of a failed check of performance states, the check MAY be repeated (VV.3)."
- **D3. PERF.23 s2 has a trailing condition** ("or, while the history is too short ..."). Fix: "Where the history shows the variation of a quantity, each regression guard on it SHOULD judge new measurements against that history by a criterion recorded before it runs (VV.3, RSRC.2). While the history is too short to show that variation, the guard SHOULD judge against the performance requirement and state that (VV.3, RSRC.2)."

## Should-fix
1. **The Term "Performance evaluation" lets an evaluation escape.** An unplanned measurement is not "systematic", so PERF.3, 8 and 11 never reach it. Pair S6 fixed the same flaw for Benchmark. The Term also duplicates PERF.3 s1. Fix: end the Term "... about the performance of that code; STND.PERF.3 and STND.PERF.8 state what makes it systematic."
2. **PERF.23 calls a check against the requirement a "regression guard".** The Lexicon defines a guard as a comparison with prior output. Fix: call the short-history case "a check".
3. **The onset paragraph omits PERF.13 s2**, which instantiates VV.1 like PERF.11 s2 and PERF.16 s2. Name it with them.
4. **Notes sources.**
   - "threefold until a reboot" is p1 H1, not H2.
   - The top-down sentence is uncited, and p2 marks its source secondary and unread.
   - "an average of ratios has no unit that a run measured" is inference; p1 H4 calls the geometric-mean debate unresolved.
   - The requested-clock and single-binary sentence is uncited (p1 items 6, 7).
   - The profiler study is secondary (p1 S12).
   - Fix: cite, or mark as inference or secondary.
5. **RATIONALE.** It says provisions cite STND.VVUQ.77; only the Notes do. It states PERF.21 without the cause-removed exception.
6. **PERF.7 s1's "three" is unverified.** It is marked and has an exit; list it as a custodian decision, with the number-free form, in the delivery.

## Optional
- DOCS.9: "serve as models"; "Several sources".
- PERF.13 s2 names a means ("interleave or randomize"); the outcome is an order that favors neither side.
- PERF.5 s2 ends "whether or not ..."; PERF.4 s2 says "rate" for a bound that may not be a rate.

## Class onsets (STND.CLASS.10)
PERF.7 s2 at CSQ2 (INTPR.10) is right. PERF.11 s2 and PERF.16 s2 at CSQ3 are right (no oracle). PERF.26 at CSQ3 is right (AGENT.40 instantiates RSRC.8 only).

**PERF.22 at CSQ3 holds.** It rests on REPRO.1 and RSRC.2, neither in the table. Revision, path, factors and design are inputs of a tracked point. It asks for neither REPRO.4 provenance at production nor RSRC.3 per-run records. No floor is raised.

## Pair review: 13 delta pairs
`/tmp/claude-1000/verify-perf/record.py` parsed `pairs-0.2-delta.md`, asserted numbers 402 to 406, 411, 412, 415 to 418, 421, 478, one record each; it passed.

| Pairs | Reading | Result |
| --- | --- | --- |
| 402 AGENT.5 | PERF.24 s2 keeps the criterion in the record (VV.3), as AGENT.5 has changes to checks recorded apart. | No conflict |
| 403 HDES.4, 404 HW.16, 405 HW.17, 406 HW.18 | Verification of results. HW.18 lowers a path's limit by a decision, the only exit when a value fails the requirement; complementary to PERF.24 s2. | No conflict; owner HW |
| 411 MEAS.7 | Exclusion of observations. | No conflict |
| 412 NUMER.11, 415 .19, 416 .25, 417 .26, 418 .28, 421 .7 | Numerical tolerances and stochastic results; shared base VV.3 only. | No conflict |
| 478 AGENT.13 | RSRC.6 only. | No conflict |

None is unowned or a restatement. I did not re-review the 577 retained pairs, including those of the 17 provisions whose text changed.

## Could not check
- Primary sources behind p1 and p2 (extract-based).
- Whether the custodian's direction covers every phrase of the RATIONALE (OPEN-ITEMS lines 18 to 20 cover three points).
