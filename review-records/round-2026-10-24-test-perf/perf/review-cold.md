# Cold review of STND.PERF draft 0.1

## Verified by script
- `govharness verify` on `.scratch/perf/rehearsed`: eight checks PASS (one g.18 warning, not a PERF finding). `findings.py 'STND\.PERF'`: none.
- All 26 provisions: default; at most two modals; no banned body word; no method, tool, event, product, or version named. Roofline, Amdahl, Gustafson, Holm, and top-down appear only in Notes.
- Cited corpus text read and found described correctly (RSRC, HW.22, HW.CPU.4, HW.GPU.4, VV.7, VV.8, STND.VVUQ.17, .35, .77, .82, STND.OFFLD.31, STND.CONC.1, STND.CLASS.10, NUMER.26, MEAS.7, AGENT.39, AGENT.40, GOV.24, GOV.29, Lexicon "Regression guard").
- Research figures found in p1 or p2 as stated: 15 of 39, 43.5 percent, about 33 and almost 300 percent, threefold until reboot, 30 to 40 samples, multiplexing, skid, overcount, four profilers, changepoints, largest terminated child.

## Defects

1. **PERF.12 s2 and PERF.14 s2 restate STND.OFFLD.31.**
   - OFFLD.31 s1 is "end at an observed completion"; s2 is "whether it includes the costs of a first submission, among them initialization and compilation at load".
   - PERF.12 s2 copies the wording and widens the scope. PERF.14 s2 widens the object to every asynchronous operation. Offloaded work is one, so two defaults now say the same about it. STND.CONC.1 also holds the completion.
   - The Notes admit it for PERF.12 and say nothing of PERF.14 s2.
   - Fix: open each with "Other than for offloaded work, which STND.OFFLD.31 holds," and add OFFLD.31 to `refers_to`. Or cite OFFLD.31 and CONC.1 and keep only what is new.

2. **PERF.7: the one number has no source, and a fact is the researcher's synthesis.**
   - The Notes cite "p2, answers 7 and 18" for "three values are the fewest that separate one rate of growth from another" and "a trend fitted to a handful of values says little far beyond them". Answer 7 says "several sizes ... wide enough to separate growth rates"; answer 18 says a model states its fitted range. Neither says three.
   - p2 "Not verified": "The advice not to extrapolate a fitted trend far is my synthesis."
   - The only precedent for three is STND.CONC.24 (p2 line 53), written for correctness; p2 says a scaling evaluation is a different purpose.
   - Fix: in the Notes, name CONC.24 as the analogy, mark "three" and the extrapolation claim as the drafter's inference [unverified], and put the number to the custodian as a decision.

3. **PERF.22 s1 restates RSRC.2 and RSRC.3.** "Keep a performance history of each quantity" is "measured and tracked from the first run so trends are visible" (RSRC.2) and "recorded with the run" (RSRC.3). The onset is also doubtful: the per-point record of revision and environment is provenance written with each output (REPRO.4, CSQ2 row), yet the Notes place it at CSQ3 without saying why. Fix: keep s2 only, cite RSRC.2 and RSRC.3, and state the onset of the record by that row or argue CSQ3.

## Should-fix

4. **"Systematically" is circular.** The Terms define Performance evaluation as a "systematic measurement or analysis". PERF.1 binds to that term, so a reviewer cannot test it. PERF.3 supplies a checkable reading (state which of the three questions are answered, with the reason for each left out). The Notes put it as "considers all three without being made to answer all three" and do not say it is the drafter's reading of the direction, with the stricter alternative (all three required) rejected for blocking work where one is meaningless. Fix: define "systematic" in the Term as "planned before it runs, with its claim and questions stated (STND.PERF.3)", and add the reading to the Notes as a decision for the custodian.

5. **PERF.24 s2 against STND.VVUQ.17 is unargued.** VVUQ.17 treats a guard failure as a defect unless the record said beforehand that the change alters the result. PERF.24 s2 lets a recorded decision accept the new value afterward. A reviewer reads this as a looser rule for time with no reason. Fix: say in the Notes that noise makes a failure possibly a false alarm, or require "the record of the change states that it alters the quantity", and state that acceptance does not rewrite the criterion (VV.3). That "none holds a guard on time" is true of VV.7, VV.8, VVUQ.17.

6. **"Practical threshold" has no home for an absolute-only evaluation.** PERF.13, PERF.14, and PERF.26 test against it, but only PERF.19 s2 requires one, and only where a difference is judged. Fix: have PERF.3 require the threshold with the claim, or add "or the margin of its performance requirement" to the three.

7. **No way out where a means is unavailable.**
   - PERF.23: no history exists at the first revisions. Add a condition: where the history is too short to show its variation, the record says so and the guard judges against the requirement.
   - PERF.13: "with its value or its levels" fails where a factor cannot be read. Copy HW.CPU.4's "or that it is unable to measure it".
   - PERF.14 s1: if no timer meets the threshold, point to PERF.15 s2 (time a block) or let the record state the shortfall.
   - PERF.21: bars a rerun after a fault outside the code (a failed node, other load). Add "unless the record states a cause outside the code and it is removed".
   - PERF.24 s1: revisions that cannot be built. PERF.7 s1: a hardware variable with fewer than three values. Add "or the record states why not".

8. **Partial restatement.**
   - PERF.1 s1 is circular, and s2 repeats RSRC.2 and RSRC.4; s2 is also ungrammatical ("meets its performance requirement, improved, or regressed"). Rewrite s1 and drop or narrow s2.
   - PERF.2 s1 repeats RSRC.1 and Budget on quantity and size. Keep path, conditions, statistic, margin.
   - PERF.4 s2 mirrors HW.22 s3; PERF.5 s1 mirrors HW.22 s1 for one path (argued in Notes); PERF.25 s1 is RSRC.11 applied (admitted). Say so in the Notes for PERF.4.

9. **Method prescribed in three provisions** against "methods need not be prescribed".
   - PERF.16 s2 names two checks (output, growth of time with size). State the outcome and move the checks to the Notes.
   - PERF.24 s1 prescribes remeasurement of the revisions between two points (p1 item 18, from S8). State "identified by measurement".
   - PERF.19 s1 fixes "an interval at a stated confidence". Use "its uncertainty and the basis of that uncertainty".

10. **Notes break STND.DOCS.** They carry obligations in the indicative: "the central value fits the unit ...: the arithmetic mean for costs, the harmonic mean for rates, and no average of ratios"; "the time on which a claim rests comes from runs without them"; "an attribution is confirmed by a second method"; "Whoever states the requirement ... makes the statement". The first is also a method list. Recast as reasons or cut. The Notes run about 3,500 words and retell p1 and p2; cut to reasons and onsets.

11. **PERF.9 s2, Notes: "Probes add work" is unmarked.** p1 line 97: "No primary source with magnitudes retrieved ... [unverified] as to size." The provision does not need a size and stands; mark the Notes sentence.

## Optional
- PERF.7: s1 (span the claimed range) and s2 (claim beyond the values measured) overlap; open s2 "Where a scaling claim covers values beyond those measured". RSRC.5 does not bear on the count; drop it or say why.
- PERF.8 s1 presumes a "resource suspected of limiting the code"; add "where one is suspected".
- PERF.16 s2: an output check against an independent expectation is a VV.1 reference-oracle comparison (CSQ2 row). The Notes put it at CSQ3 without saying the expectation is not independent.
- "Represents" in PERF.16 is the DOCS.9 copula pattern; use "is". Drop "is one method" beside Holm.
- p1 line 132 says memory, cache-miss, and energy design were not retrieved; mark the Notes' memory and energy statements as the drafter's extension.
- The RATIONALE says "ratified by the custodian on 2026-10-24". The custodian ruled only the three listed decisions; the lead resets this at the coalesce. Check that it is changed.

## The drafter's decisions
- **"Systematically":** acceptable reading, not put to the custodian (item 4).
- **Three values:** the number is inference, not in p1 or p2 (item 2). Keep as a default with an escape.
- **MEAS left out:** sound. The selector (MEAS.1, GOV.24) turns on instruments, sensors, or observers, and GOV.29 allows analogy. PERF.18 gives MEAS.3 and MEAS.7 outcomes without citing them in a provision. The reading that a program's own timing is not such data is p2's ("my reading"); the Notes should say so.
- **Regression guard on time:** the gap is real; the divergence from VVUQ.17 needs the argument of item 5.
- **Class onsets:** consistent with STND.CLASS.10 except items 3 and the PERF.16 point. PERF.7 s2 at CSQ2 (INTPR.10) and PERF.26 at CSQ3 are right.

## Could not check
- Primary sources behind p1 and p2 (extract-based).
- A separate list of the drafter's six decisions; I reviewed the Notes and RATIONALE only.
- Pair coverage (`pairs.md`) and title distinctness beyond the harness check.
