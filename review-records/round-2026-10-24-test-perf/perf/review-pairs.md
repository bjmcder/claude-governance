# STND.HARN.28 pair review: STND.PERF 0.1 (2026-10-24)

Scope: the 596 pairs of `pairs.md`, read against the rehearsed copy `.scratch/perf/rehearsed` (STND/PERF 1 to 26 and `_doc.md`) and the reading copy `draft-0.1.md`. I read all 102 distinct other provisions in full; the LVL0 provisions the bases name (RSRC.1 to .6, .8, .11, VV.1, .3, .7, .8, REPRO, INTPR, PRIME.2); STND.VVUQ.17, .35, .77, .82, .83, STND.OFFLD.31, STND.CONC.1, AGENT.24; the shared-matters tables of HW, NUMER, MEAS; and the Lexicon terms Baseline, Budget, and Regression guard. Method follows `ledger115/review-pairs-offld.md`: conflict means one provision can be met only by failing the other; unowned means a matter both touch that no table or provision gives an owner; restatement means the same outcome stated twice (GOV.31). 

## Result

- Conflicts: none among the 596 pairs, and none in the hand checks.
- Unowned matters: 5 (U1 to U5), touching 15 listed pairs.
- Restatements: 4 (R1 to R4) in 9 listed pairs, plus R5 outside the list.
- No Defect. Six Should-fix, five Optional.
- The remaining 573 pairs share only a base (VV.1, VV.3, INTPR.9, INTPR.10, DSGN or REPRO) with a provision on an unrelated subject: hardware-design verification, quantum, embedded, numerical-method and learned-model rules. They are grouped in the coverage table.

## Should-fix

**S1. PERF.22 drops the case RSRC.2 exists for (U1; pairs 365, 366, 369, 370, 373).** RSRC.2 asks that an unknown budget be stated and that resource use be measured and tracked from the first run, and the Notes say the record of PERF.22 "is the tracking of RSRC.2". PERF.22 keeps a history only of "each quantity that its performance requirements bound". Performance-sensitive code with no requirement yet (the Term allows it: resource use material with a reason) has no history under PERF, and RSRC.2 holds nothing on how. Fix: PERF.22 sentence 1: "of each quantity that its performance requirements bound or, where no budget is stated, that its record states as material".

**S2. What licenses optimization is unclear for a ratio or derived bound (U2; pairs 334, 441, 442).** RSRC.4 licenses optimization only against a shortfall from a stated Budget (Lexicon: a limit on a resource at a stated size) or an adverse trend. PERF.2 sentence 2 lets a performance requirement be a ratio to a comparison base, which is not a limit on a resource. PERF.4 lets an absolute question judge against a bound derived from work and hardware, and RSRC.2 bars a claim of inadequacy without a budget or tracked record. A reader can take the gap to a derived bound, or a ratio miss, as the shortfall RSRC.4 needs. Fix: add to PERF.4 sentence 2 "; the fraction states the room left and is no claim of adequacy or shortfall without a budget or tracked record (RSRC.2, RSRC.4)", and in Terms say that a ratio bound is a Budget when it names its comparison base and problem size.

**S3. A comparison of two paths not in a reported result or release is owned by nothing (U3; pair 470).** HW.22 binds claims "stated in a reported result or a release". PERF.5 excludes any comparison not "on one execution path". A path comparison in a decision record or task report therefore has no stated conditions (data movement and dispatch counted, contention, power, thermal state, fraction of peak). PERF.1 and PERF.19 still apply, but not those conditions. Fix: PERF.5 sentence 1 ends "...; where the comparison base runs on another execution path, the conditions of HW.22 apply whether or not the claim is reported (HW.22)".

**S4. PERF.26 rests on an unstated reading of AGENT.40 (U4; pairs 412, 413).** AGENT.40 starts a unit when the resources "the units already running leave free" can serve it. A measuring unit that states it needs cores it does not use (shared cache, sibling threads) does not hold them, so a literal AGENT.40 starts another unit there. The Notes assume the statement reserves them. Two further gaps: nothing sequences a unit that needs the machine alone against a steady stream of units that AGENT.40 starts "as soon as" they fit, so it can starve; and AGENT.40 and PERF.26 name only processors, memory, and accelerators. Fix: PERF.26 sentence 1 adds "and plan the unit so that the resources so stated are not left free by it (AGENT.40, AGENT.22)", with a Note that the plan sequences such a unit and that a stated resource is held, not free. Name "each other resource" or leave it to PERF.13 in the Notes.

**S5. PERF.12 sentence 2 and PERF.14 sentence 2 restate STND.OFFLD.31 for offloaded work (R5, outside the list).** OFFLD.31 is the same two outcomes (time ends at an observed completion; state whether first-use costs, "initialization and compilation at load", are included), with the same example list. The Notes say OFFLD.31 "holds the timing of offloaded work" and that PERF.12's second sentence "is its form for all code", so two defaults hold one outcome for offloaded work, which GOV.31 forbids. Fix: add to the Notes of PERF "OFFLD.31 is the case of PERF.12 and PERF.14 for offloaded work; one record meets both", and list at the next OFFLD amendment that OFFLD.31 cites STND.PERF.12 and STND.PERF.14 (a custodian-timed change; PERF need not wait).

**S6. The Term Benchmark makes "versioned" part of its definition.** An unversioned timing harness is then not a Benchmark and escapes PERF.16, though REPRO.10 requires it versioned. Fix: Term "A program, with its inputs and problem sizes, whose runs a performance evaluation measures; REPRO.10 holds that it is versioned."

## Optional

- **O1 (R1; pairs 290, 292).** PERF.18 restates MEAS.3 (raw samples kept as measured) and MEAS.7 (exclusion criterion before the result, or stated with its criterion and when set), nearly verbatim. The Notes argue it (MEAS does not bind a timing; GOV.29 analogy). Where MEAS does bind, there are two statements. Fix: Notes sentence that one record meets both. Also PERF.18's alternative "stated with its criterion and the time" reads weaker than VV.3 ("changing afterward is a recorded decision that leaves the original criteria"); write "recorded as a decision under VV.3, with its criterion and when it was set".
- **O2 (R2; pair 334).** PERF.2's margin and conditions of power, thermal state, and contention duplicate HW.20 for a constrained target (owner HW, HW.2 row 4). Fix: "except a budget of a constrained target, for which HW.20 holds the margin and conditions". PERF.2 also asks a "statistic of the samples" while a deadline that HW.20 or CPS.8 binds needs a bound on worst-case execution time that no sample statistic gives (pairs 441, 266 and the CPS.8 pairs): add "or, for such a deadline, the bound of HW.20".
- **O3 (R4; pairs 367, 368, 372, 374, 375).** PERF.22 sentence 2, "execution path and its environment", overlaps HW.3 and the identity records of HW.ASIC.3, HW.FPGA.3, HW.QPU.3, and MEAS.4 in coarser terms. Fix: "carry the record of HW.3 and of its sub-profile for that path".
- **O4 (R3; pair 358).** PERF.21 is the performance form of NUMER.26, which covers stochastic results only; not a restatement. Optionally cite PRIME.2 beside VV.3, as NUMER.26 does.
- **O5 (U5; pairs 163, 186, 267, 307).** A sample taken across a fallback, throttle, or other HW.9 event is neither barred from the summary nor required to carry the event. Fix: Notes say such events enter the PERF.18 criterion or the record.
- Smaller: PERF.12 sentence 2 may be read to allow "excludes" for the first filling of memory; for a claim under HW.22 the data movement is counted whatever is stated (pair 84). PERF.13 limits the status of factors to those above the practical threshold while REPRO.2 records every factor that affects results; add "in addition to REPRO.2". PERF.24 sentence 2 differs from STND.VVUQ.17 (VVUQ.17 treats a failure as a defect unless the change stated beforehand that it alters the guarded result); the difference is sound, because PERF.24 requires evidence that each requirement is still met, but the Notes call VVUQ.17 the "counterpart" and should state the difference. PERF.14 sentence 1 says "each measurement of time", which reaches the unit timing records of AGENT.24; add "in a performance evaluation".

## Checked, no finding

- HW.22 against PERF.4, .12, .14: PERF.4 states a fraction of a bound (absolute question); HW.22 sentence 3 states the comparator's fraction of its peak. Different questions.
- STND.VVUQ.77 against PERF.5: compatible. The "equal cost" arm judges accuracy and is outside PERF.5.
- NUMER.17: PERF.1, .5, .24 meet it unchanged; a retained approximation is verified there, not in PERF.
- HW.GPU.4 against PERF.9 sentence 2: HW.GPU.4 allows "unable to measure" without a profiler, so a probe-free time run meets both.

## Not checked

The research notes p1 and p2 and the earlier adoption reviews were not read; claims of the Notes quoted from them (study figures) are unchecked. About 570 pairs were judged by the subject of the other provision, read in full, not by an argument each. Onsets were not recomputed; the harness was not run.

## Coverage

Script `/tmp/claude-1000/pairs-perf/record.py` parsed `pairs.md` (596 rows), wrote one record per pair to `/tmp/claude-1000/pairs-perf/record.tsv`, and asserted numbers 1 to 596, no gap, no repeat, equal to the set in `pairs.md`: passed.

| Group of other provision | Pairs | Conflict | Unowned | Restatement | No finding |
| --- | --- | --- | --- | --- | --- |
| AGENT | 23 | 0 | 2 (412, 413) | 0 | 21 |
| CPS | 10 | 0 | 0 | 0 | 10 |
| HDES | 45 | 0 | 0 | 0 | 45 |
| HDES.ASIC | 35 | 0 | 0 | 0 | 35 |
| HDES.FPGA | 7 | 0 | 0 | 0 | 7 |
| HW | 89 | 0 | 10 | 2 | 78 |
| HW.ASIC | 7 | 0 | 0 | 1 | 6 |
| HW.CPU | 18 | 0 | 2 | 0 | 16 |
| HW.EMBED | 21 | 0 | 0 | 0 | 21 |
| HW.FPGA | 7 | 0 | 0 | 1 | 6 |
| HW.GPU | 11 | 0 | 1 | 0 | 10 |
| HW.QPU | 43 | 0 | 0 | 1 | 42 |
| MEAS | 23 | 0 | 0 | 3 | 20 |
| ML | 19 | 0 | 0 | 0 | 19 |
| NUMER | 238 | 0 | 0 | 1 | 237 |
| Total | 596 | 0 | 15 | 9 | 573 |

Pair 334 (PERF.2 with HW.20) is in both the unowned and the restatement column, so 23 distinct pairs carry a finding and 573 none. Findings by pair number: U1 365, 366, 369, 370, 373; U2 334, 441, 442; U3 470; U4 412, 413; U5 163, 186, 267, 307; R1 290, 292; R2 334; R3 358; R4 367, 368, 372, 374, 375.
