Role: research agent. Date accessed: 2026-10-24. Retrieval counts: 22 items (15 page or document fetches, of which 5 failed or returned nothing usable, and 7 web searches) and roughly 8 MB, an estimate, well inside the 1,500-item and 1,500 MB budget. Retrieval rules followed: read-only retrieval; no paywall touched; fetches that failed (two hosts unreachable, two HTTP 404, one parse error, one IEEE page that returned empty) were not worked around and no mirrors, caches, or archives of the blocked item were used; no credentials; retrieved text treated as data; unconfirmed items marked [unverified].

# P2: The questions a performance evaluation asks, and how a method is chosen

## Method caveat

The page-fetch tool returns a model-written extract of a page, so quotations from S1 and S8 are extracts and may paraphrase. Five papers (S2 to S6) came back as undecodable PDFs; I saved and converted them locally, and statements attributed to them are from the paper text. Not read: Amdahl 1967 (HTTP 404) and the top-down method paper (empty page, then a parse error). S7 therefore rests on a search extract of the abstract and kernel documentation text in search results. S9 to S13 rest on search-result summaries only. All of these are marked secondary. I did not repeat measurement design and statistics (note p1). Tool and product names appear only as the subject of a hazard or the name of a documented interface.

## Answer in brief

1. The question fixes the method: absolute (against a budget or bound), relative (against a baseline or alternative), scaling (with size, task count, hardware). State the question, then choose the cheapest sufficient method (RSRC.11), and record both. [S2, S3, S12]
2. An absolute claim names its yardstick: a stated budget at a stated problem size, or a bound derived from the work and the hardware. A figure with neither is a number, not a verdict. [S3 rule 11; corpus RSRC.1, RSRC.2]
3. Where a bound can be derived, attainable rate is the lower of the peak compute rate and the peak data-movement rate times the operations performed per byte moved from the limiting level of memory. Achieved rate as a fraction of the bound shows the room left and the limiting resource. [S2, S3]
4. A vendor peak is a ceiling that no code reaches. Where it is far from reality, a measured ceiling from a controlled microbenchmark serves, and the record says which was used. [S3, S2]
5. Asymptotic cost bounds growth, not time. It is stated (RSRC.5), checked across sizes, and never converted to time without a measured constant. [S6; corpus RSRC.5]
6. A relative claim compares like with like: same work, accuracy, sizes, and conditions, against the best reasonable alternative. Both sides are measured, and the baseline's absolute figures are reported with the ratio. [S3 rule 1; corpus HW.22, SIMPL.7]
7. Scaling with problem size is judged from runs at several sizes over a range wide enough to separate growth rates, with the fit and its quality reported; a fitted trend is not extrapolated far beyond the sizes measured. [S6]
8. Strong scaling (fixed total work) and weak scaling (work per task fixed) answer different questions and are named. Amdahl bounds strong scaling by the serial fraction; Gustafson's scaled speedup answers the question when the problem grows with the machine. Each is a model with an assumption, and the assumption is stated. [S4, S12]
9. Efficiency is reported against a named baseline at the smallest feasible scale, with that baseline's absolute time (RSRC.8). Super-linear scaling signals a changed resource, such as cache capacity, and is explained. A scaling study covers the whole node or allocation it claims, and reports where scaling stops. [S3; corpus RSRC.8]
10. The experimentally determined serial fraction, computed per task count, separates a limit from lack of parallelism (roughly constant) from one from overhead (growing). It is a diagnostic, not a derivation. [S12, secondary]
11. Memory and communication scale too: peak memory per task and total, bytes and messages per task. A code can scale in time and fail in memory at the next size. [S3, S8]
12. Method classes answer different questions: wall-clock timing (how long); sampling profile (where, statistically); trace (order, waiting, imbalance); hardware event counts (what the processor did); memory profile (how much, when); I/O and communication records (what moved); energy (what it cost); models (what would happen at a scale not run). [S1, S3, S5, S10]
13. A hardware event count is an estimate. Events outnumbering counters make the kernel time-share them, so a count is scaled from the fraction of time it ran; events are attributed to a later instruction (skid); some events overcount or vary run to run even in controlled conditions; generalized event names can measure different things on different hardware; access can be restricted. The record states events, interval, scaling, and conditions. [S1, S5]
14. A sampling profile is as unbiased as its sampling points: profilers that sample only where the runtime can stop disagreed about the hot methods in a published study. A finding from one profile is checked by a second method before an optimization rests on it (RSRC.4). [S10, secondary]
15. A time measurement ends at an observed completion and states whether first-run costs (initialization, compilation, cache fill) are included. The corpus holds this for offload (STND.OFFLD.31); it holds for any asynchronous or lazily initialized system. [corpus; S3]
16. Memory is several quantities: peak resident size, largest allocation, allocation rate, footprint at the data size. "Peak" is defined by the reporting interface; for example, the peak of terminated children is the largest child, not the tree's sum. [S8]
17. Energy is measured at a stated boundary (device, socket, node, wall) and read against that boundary's accuracy; an on-chip estimate tracked wall power in a published study, with counter rollover and non-atomic updates as stated limits. Energy and time are reported together. [S9, secondary]
18. A model answers what cannot be run. It states its parameters and fitted range, and is compared with at least one measurement before reliance. Measurement and model are combined, not substituted. [S3 section 5.1, S11 secondary]
19. Bottleneck analysis is top-down: classify the dominant limit coarsely (instruction supply, data, wasted speculation, useful work; or communication, I/O, imbalance), then descend only into the dominant branch. [S7 secondary, S2]
20. Declaring a work performance-sensitive is a recorded statement with its reason (deadline, cost bound, scale target, shared resource). It triggers evaluation and does not choose the method. A performance requirement states the quantity, problem size or range, hardware and conditions, statistic judged, baseline if relative, and margin; it is the budget of RSRC.1. [corpus RSRC.1, RSRC.2, HW.20]
21. Evaluation is itself an expenditure. A scaling study at large scale falls under PRIME.8 and RSRC.8; the smallest sufficient experiment runs first. [corpus]

## What the corpus already holds

The drafter cites these and does not restate them (GOV.31). Class onsets are those the corpus gives: RSRC.3 from CSQ2 by the row of STND.CLASS.10; the other RSRC and HW performance provisions from CSQ3; CSQ4 may omit them.

| Matter | Provisions | What they hold | Gap or boundary |
|---|---|---|---|
| Stating budgets | RSRC.1 | Each component whose resource use is material states its material budgets; the system states time, memory, energy, and cost budgets, each with the problem size at which it SHALL be met | Holds the budget and the size. Does not say how a budget is evaluated, nor name the percentile or statistic. A performance requirement (answer 23) is RSRC.1 applied |
| Unknown budgets | RSRC.2 | Resource use is measured and tracked from the first run; a budget is stated once the record supports one; no claim of adequacy or inadequacy without a stated budget or tracked record | Governs the claim, whatever the method |
| Recording | RSRC.3, REPRO.4, HW.3 | Time, memory, energy where measurable, and cost recorded with the run; provenance written at production; execution path recorded with hardware model, firmware, drivers, runtime libraries, and settings | The conditions of a measurement (answer 15) are largely HW.3 and REPRO.4 content |
| Measured optimization | RSRC.4, SIMPL.7 | Optimization only against a measured shortfall or adverse trend, aimed at the measured bottleneck, retained only if measurement shows the gap closed without violating VV; an optimized replacement is verified against the clear implementation and shows by measurement it is needed | This is the trigger for top-down bottleneck analysis; the method is not held |
| Algorithm first | RSRC.5 | Asymptotic complexity, rate of convergence, and representation settled before lower-level optimization | Holds that complexity is stated. Does not hold empirical checking of complexity across sizes (answer 8) |
| Scale | RSRC.8 | Parallelism, distribution, specialized hardware, purchased capacity adopted when a measured baseline at the smallest feasible scale shows need; overhead and efficiency measured against that baseline; where the hardware or scale is the object, the baseline serves comparison | Holds the baseline and the efficiency measure. Does not distinguish strong from weak scaling, or say what scaling quantities exist |
| Comparative claims | HW.22 | A claim that one execution path is faster or more efficient rests on measurements of both at a stated problem size, under stated contention, power, and thermal conditions, with data movement and dispatch counted, at shown accuracy; numerical results judged by a NUMER.11 tolerance; where the comparator's hardware states a peak rate, the claim states the comparator's measured or counted rate as a fraction of it | Binds claims between execution paths in a reported result or release. This already holds the relative question for paths, and the absolute fraction-of-peak for the comparator. It does not govern comparison of two versions or two algorithms on one path, except STND.VVUQ.77 for learned versus numerical methods as a default |
| Fair comparison | STND.VVUQ.77 | Equal accuracy or equal cost against an efficient numerical method, under HW.22 conditions | Extends HW.22 conditions to methods compared on one path, for one pair of method families only |
| Offload timing | STND.OFFLD.31 | A time measurement of offloaded work ends at an observed completion and states whether first-submission costs are included | General principle (answer 17) is held for offload only; STND.PERF can cite it and generalize without restating |
| Offload resource record | HW.GPU.4 | In runs that measure resource use under RSRC.2 or RSRC.4: data volume moved between host and accelerator including on-demand movement, number of submissions, fraction of run duration the accelerator executes, peak accelerator memory, or that it cannot be measured without privileges. Applies from CSQ3, only in runs that track or measure | Holds data-movement and utilization quantities for accelerators |
| Processor thread record | HW.CPU.4, HW.CPU.5, STND.CONC.18 | Hardware threads used and permitted by affinity and quota counted by core design, memory paged to storage, placement; oversubscription reported at first occurrence; pool sizes set so concurrent tasks do not exceed permitted threads | Holds the dominant silent slowdown of multicore CPU runs |
| Constrained targets | HW.20, HW.21, STND.CONC.20 | Budgets with margin and evidence under power, thermal, and contention conditions; worst-case execution time bounds where a missed deadline can cause hazard; monitoring of unbounded budgets; blocking time in WCET | Holds real-time bounds. STND.PERF defaults concern throughput and scaling, not deadlines |
| Parallel work on a shared machine | AGENT.39, AGENT.40, PRIME.8 | Parallel work begins only after an assessment from a measured baseline or recorded decision shows it is faster or cheaper; units start as free resources allow; spending proceeds on an authorized estimate | Bounds the cost of an evaluation and the contention that perturbs it |
| Variation | HW.12, STND.CONC.21, REPRO.3 | Execution paths state whether order, scheduling, and run-time implementation choices vary between runs; results that change with task count are declared | Run-to-run variation of results, not of time. Variation of time and its statistics are p1 |
| Tests across task counts | STND.CONC.24, STND.MPI.24, STND.OMP.33 | At least three task counts including the smallest; schedules and bindings tested | Correctness at several counts. A scaling evaluation is a different purpose; STND.CONC.24 is a model for wording |
| Performance approximations | NUMER.16, NUMER.17, STND.VVUQ (approximation effect) | A retained approximation is disclosed and its effect on each reported numerical result is shown within precision | Holds that a speed gain taken from precision is verified |
| Measurement of physical quantities | MEAS (MEAS.3 to MEAS.7) | Raw observations kept, acquisition record, calibration validity, uncertainty with basis, exclusions fixed before the result | MEAS binds work whose results rest on data measured by instruments, sensors, or observers (MEAS Purpose). My reading is that a program's own timing is not such data unless the classification records it so. The drafter should not cite MEAS as binding on timing. MEAS.7 is the model for a rule that excluded runs follow a criterion fixed before the result; that is p1 territory |

Additional boundary points for the drafter:

- STND.TEST is a separate planned standard (OPEN-ITEMS, custodian 2026-10-24). A performance regression test is a test and a performance evaluation; the drafter assigns which standard holds the regression-guard role. VV.8 and STND.CODE.8 hold regression guards for results; none holds a guard on time.
- No existing provision defines "performance-sensitive". RSRC.1 and RSRC.2 make a stated budget the basis of any adequacy claim, so the declaration is a recorded budget or requirement, which costs one record and raises no floor.
- No corpus provision asks for an empirical complexity check, strong or weak scaling, a bound model, a counter-based analysis, memory-profile quantities beyond peak accelerator memory, energy beyond "where measurable," or a performance model. These are the content STND.PERF may add as defaults (all defaults, per the custodian), citing RSRC.4 or RSRC.8 as ancestors.
- Class onset: because every provision of STND.PERF would be a default instantiating RSRC provisions, STND.OFFLD's pattern applies: from CSQ3, CSQ4 may omit, and the Notes state the onset per provision.

## Hazard tables

"Holds" column: ALL means across platforms and tools; SPECIFIC names the limit.

### H1. Absolute performance

| Hazard | Source fact | Failure | Practice | Sources | Holds |
|---|---|---|---|---|---|
| No yardstick | Roofline: attainable rate is the minimum of peak floating-point rate and peak memory bandwidth times operational intensity; the lines are fixed once per computer, not per kernel. Hoefler and Belli: show upper performance bounds to make results interpretable (their rule 11) | A time is reported with no verdict: fast or slow is unknowable | State a budget or derive a bound; report achieved as a fraction of the bound | S2, S3 | ALL; the bound's terms are the work and the hardware's limiting resource |
| Wrong resource in the bound | Roofline defines operational intensity as operations per byte of main-memory traffic after filtering by the cache hierarchy, and says it is general to non-arithmetic operations. Hoefler and Belli generalize to a k-dimensional machine model; memory or network bandwidth, not flop rate, limits many codes | The code is judged against compute peak while a bandwidth, latency, or communication limit binds | Choose the resource(s) that can limit the work; use more than one bound | S2, S3 | ALL |
| Peak is a guarantee not to exceed, not an expectation | Hoefler and Belli: vendor-specified numbers "are only guarantees to not be exceeded"; where far from reality, parametrize with carefully crafted, statistically sound microbenchmarks | A code at 40 percent of a peak that no code reaches is called poor | Name whether the ceiling is specified or measured; record the microbenchmark | S3 | ALL |
| Bound model ignores overheads | Hoefler and Belli: parallel overheads (a reduction cannot run faster than a logarithm of the process count) tighten the ideal-speedup bound; they combine it with Amdahl's law | An ideal line that no implementation can reach is the only reference | Show ideal, serial-overhead, and parallel-overhead bounds where known | S3 | ALL |
| Asymptotic cost taken as time | Empirical-complexity work fits the count of executions of each basic block to a linear or power-law function of workload size, and notes that such fits are good for the most-executed lines but not every line | Big-O stated, but the constant, or a hidden term that dominates at the size of use, is unmeasured | Fit across sizes; state the range; do not extrapolate far | S6 | ALL; the fit family is a choice |

### H2. Relative performance

| Hazard | Source fact | Failure | Practice | Sources | Holds |
|---|---|---|---|---|---|
| Speedup without its base | Hoefler and Belli surveyed 39 papers that reported speedups and found 15 (38 percent) gave no absolute performance of the base case; rule 1 asks to say whether the base is a single parallel process or the best serial execution, with absolute performance | A ratio against a weak or unspecified baseline | Report the absolute figures and name the base | S3 | ALL |
| Unequal accuracy | HW.22 and STND.VVUQ.77 require comparison at an accuracy that both are shown to meet, or equal accuracy or equal cost | A faster path that is less accurate wins | Fix the quality target first | corpus | ALL |
| First-run costs | STND.OFFLD.31: state whether initialization and compilation at load are included | A one-time cost charged to, or hidden from, one side | State inclusion; measure cold and warm where both matter | corpus | ALL for any system with lazy setup |

### H3. Scaling

| Hazard | Source fact | Failure | Practice | Sources | Holds |
|---|---|---|---|---|---|
| Fixed-size assumption | Gustafson: Amdahl's expression assumes the parallel part is independent of the processor count; "in practice, the problem size scales with the number of processors," so "it may be most realistic to assume that run time, not problem size, is constant." Scaled speedup is s' + p' N (equivalently N + (1 - N) s') | A strong-scaling limit is read as a limit on what the machine can do, or a scaled result is read as a strong-scaling result | State which scaling is measured; report both where both questions are real | S4 | ALL; the formulas are models |
| Serial part assumed constant | Gustafson: startup, loading, serial bottlenecks and I/O "do not grow with problem size" as a first approximation. This is an approximation, and his applications had serial fractions of 0.4 to 0.8 percent | The model is applied where the serial part grows with N (communication, I/O, a reduction) | Treat the serial fraction as measured per count, not assumed | S4, S3 | ALL |
| Overhead hidden in the serial fraction | The serial-fraction metric (from measured speedup) separates a roughly constant fraction (limited parallelism) from a growing one (overhead), per a lecture summary of Karp and Flatt | Poor scaling is "optimized" by more parallelism when overhead is the cause | Compute the experimental serial fraction at each count and look at its trend | S12 (secondary) | ALL; a diagnostic |
| Partial machine | "Scaling experiments should always utilize all available resources"; run on all cores even if scaling stops | Scaling stops at a point that the chosen range hid | Include the full node or allocation | S3 | ALL |
| Models fitted to a few counts | Automated empirical models of time versus process count or problem size flag parts of a code that will slow down at larger counts, including parts outside routines normally chosen as kernels | Scalability defects first seen at production scale | Fit per-part models at small counts and read the growth terms | S11 (secondary) | ALL; extrapolation carries the fit's uncertainty |
| Memory and communication scaling | Parallel overheads that grow with count (S3); peak memory per task and total (S8) | Time scales, then memory or message count fails the run | Add per-task memory and communication volume as scaling quantities | S3, S8 | ALL |

### H4. Classes of method

| Method class | Answers | Pitfalls | Practice | Sources | Holds |
|---|---|---|---|---|---|
| Wall-clock timing | How long, including waiting | Timer overhead and precision; asynchronous completion; first-run costs; noise from other work | End at an observed completion; many iterations per interval for short work; record conditions | S3, corpus STND.OFFLD.31 | ALL |
| Sampling profile | Where time is spent, statistically | Sampling points biased toward places the runtime can stop; four profilers in one study disagreed on the hot methods; cost grows with rate | Check a profile against a second method; state rate and attribution | S10 (secondary) | Bias is specific to the profiler's mechanism; the lesson ALL |
| Tracing (event log) | Order, overlap, waiting, imbalance | Overhead and volume perturb the run; a trace of a different configuration is not evidence | Trace a representative short run; keep the volume bounded; measure the overhead | S3 (perturbation) | ALL |
| Hardware event counts | What the processor did: instructions, cache and branch events, stalls | Multiplexing: when events outnumber counters, "the kernel time-shares" the counters and a count is estimated from `time_enabled` and `time_running`. Skid: "how many instructions execute between an event of interest happening" and its recording; precise sampling levels exist, and zero skid is requested at the highest. Overcount and run-to-run variation: in a study of eleven x86 implementations, events meant to be exact, such as retired instructions, showed variation and overcount even in controlled conditions, from hardware interrupts, page faults, and floating-point exceptions, and only a few events were deterministic enough to use without adjustment; other architectures were more deterministic. Generalized events "have had wrong values" on some hardware and kernels; the NMI watchdog can occupy a counter; access can be restricted | Count only the events the question needs and fit them to the available counters; read the scaling terms; use precise sampling where attribution matters; validate a counter against a known count before relying on it; record the event names the hardware defines | S1, S5 | Multiplexing and skid ALL for hardware with a fixed number of counters; specific events and their errors are per hardware and moving |
| Memory profile | Peak, allocation rate, footprint, lifetime | "Peak" is defined by the interface (resident set versus allocated; largest child versus tree); sampling at intervals misses short peaks | Report which peak; report per task and total; measure at the data size of use | S8 | ALL; the interface differs |
| I/O and communication analysis | Volume, count, pattern, wait | Counting at the wrong layer; overhead; shared file system contention | Counters of bytes and operations by layer, kept with low overhead so that they can run in production | S13 (secondary), corpus HW.GPU.4 for host-device movement | ALL |
| Energy and power | Cost in joules at a boundary | Boundary and accuracy; counter rollover; non-atomic register updates; energy per run depends on duration as well as power | State the boundary; read accumulating counters with overflow handled; report energy and time together | S9 (secondary) | Specific to the energy interface used; the boundary lesson ALL |
| Analytical and model-based prediction | Behavior at a scale or on hardware not run | Parameters from vendor numbers; unvalidated extrapolation; a model that ignores overheads | Fit from measurement; state the fitted range; compare with at least one measurement | S3, S11 | ALL |

### H5. Top-down bottleneck analysis

| Hazard | Source fact | Failure | Practice | Sources | Holds |
|---|---|---|---|---|---|
| Counter lists without a hierarchy | The top-down method for out-of-order processors classifies pipeline slots into four top-level categories (frontend bound, backend bound, bad speculation, retiring) and drills down recursively into the dominant branch; it is a structured use of designated counters | A secondary effect is chased; stall counts overlap and do not add | Coarse classification first, descend one branch | S7 (secondary) | Method specific to out-of-order processors with the needed counters; the principle (classify, then descend) ALL |

### H6. Declaring sensitivity and stating a requirement

No corpus term defines "performance-sensitive". RSRC.4 needs a measured shortfall from a stated budget, so without a budget there is nothing to optimize against, and RSRC.2 forbids an adequacy claim without a budget or a tracked record. The declaration (or a task that calls for evaluation) is therefore the recorded trigger, and the requirement is the budget of RSRC.1: quantity, problem size or range, hardware and conditions (HW.20, HW.22 name contention, power, and thermal state), the statistic judged, the baseline if relative, and the margin. A requirement without a size or conditions is "fast enough" and cannot be checked. Evaluation effort is proportioned to the requirement (RSRC.6, RSRC.9, RSRC.11).

## Timeless versus moving

Stable for decades:

- The roofline reasoning: attainable rate bounded by compute peak and data movement; the 2009 paper's formula is still the form in use. Bound models, ideal-speedup bounds, and overhead bounds (S2, S3).
- Amdahl and Gustafson: 1967 and 1988 arguments about fixed-size and scaled-size speedup. Each is a model with an assumption (S4).
- Report the base case; report units; do not hide the absolute number (S3 rule 1 and its section on unambiguous units).
- Counting versus sampling as the two modes of an event interface; multiplexing and skid as consequences of a fixed number of counters and of pipelined retirement (S1).
- A sampling profiler's bias comes from where it samples (S10).
- Empirical complexity from runs over a range of sizes, fitted in log-log space (S6).
- Memory "peak" defined by the interface (S8).

Moving: specific counters, event names, and which events are exact (S5 is of old hardware; the corpus must not name events); the top-down categories, defined for one family of out-of-order cores (S7); energy interfaces (S9); and every tool, none of which is recommended. Accelerator-specific counters were not retrieved.

Consequence for a standard: say what a result states (the question, the yardstick, the conditions, the method class with its limits, the base) and not which method or tool.

## Not verified

- Amdahl 1967 (HTTP 404); the formula is quoted from Gustafson's restatement (S4).
- The top-down paper's text; the serial-fraction paper (1990), whose title I did not confirm; the RAPL paper's error figures; the profiler study beyond its abstract (a 2023 follow-up reports profilers mostly agree on the single hottest method and disagree on the top five); the automated scaling-model paper's model family and limits; the counter set of the I/O tool.
- Accelerator performance analysis, latency-bandwidth network models, and queueing reasoning were not retrieved.
- The definition of any one cache-miss event: the manual extract did not give one. The statement that generalized events differ by hardware rests on the manual's remark that they "have had wrong values."
- The advice not to extrapolate a fitted trend far is my synthesis; I did not locate a limitations section in S6.
- The 5 percent timer overhead and tenfold precision margin are suggestions in S3, not standards, and the corpus does not adopt them.

## Sources

| ID | URL | What it supports |
|---|---|---|
| S1 | https://man7.org/linux/man-pages/man2/perf_event_open.2.html (extract of first 100,000 characters, plus a second extract of the rest) | Counting versus sampling events; multiplexing and `time_enabled`, `time_running`; skid and precise sampling levels; inheritance; privilege restrictions; generalized events with wrong values; NMI watchdog; "Always double-check your results!" |
| S2 | https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf (Williams, Waterman, Patterson, Roofline; read as converted text) | Operational intensity; attainable rate formula; ceilings; ridge point |
| S3 | https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf (Hoefler and Belli, SC15; read as converted text) | Rules 1 to 12; speedup reporting survey; machine-model bounds; parallel overheads; timer overhead; whole-node scaling |
| S4 | https://users.cs.utah.edu/~hari/teaching/paralg/Gustafson88.pdf (Gustafson 1988, CACM; read as converted text) | Amdahl restated; scaled speedup; fixed-time reasoning |
| S5 | https://icl.utk.edu/files/publications/2013/icl-utk-1246-2013.pdf (Weaver, Terpstra, Moore, ISPASS 2013; read as converted text) | Nondeterminism and overcount of counter events on eleven x86 implementations; interrupts and page faults as sources |
| S6 | https://web.stanford.edu/class/archive/cs/cs295/cs295.1086/papers/trend-prof.pdf (Goldsmith, Aiken, Wilkerson, FSE 2007; read as converted text) | Empirical computational complexity: linear and power-law fits over workload sizes; goodness of fit measures |
| S7 | Search result extract: https://rcs.uwaterloo.ca/~ali/cs854-f23/papers/topdown.pdf (Yasin 2014; the paper itself not read) and kernel perf documentation text quoted in search results | Four top-level categories and drill-down (secondary) |
| S8 | https://man7.org/linux/man-pages/man2/getrusage.2.html (extract) | `ru_maxrss` as peak resident set size in KiB; children report the largest terminated child |
| S9 | Search results: https://helda.helsinki.fi/server/api/core/bitstreams/bdc6c9a5-74d4-494b-ae83-860625a665ce/content and summaries (Khan and others, ACM TOMPECS 2018) | On-chip energy readings correlate with wall power; rollover, non-atomic updates (secondary) |
| S10 | Search results: https://plv.colorado.edu/papers/profilers-pldi10.html (Mytkowicz and others, PLDI 2010); https://stefan-marr.de/2023/09/dont-blindly-trust-your-profiler/ | Profilers disagree on hot methods; sampling only at yield points (secondary) |
| S11 | Search results: https://www.unixer.de/publications/index.php?pub=171 (Calotoiu and others, SC13) | Automated empirical models of time against process count (secondary) |
| S12 | Search results: https://en.wikipedia.org/wiki/Karp%E2%80%93Flatt_metric and lecture slides | Experimentally determined serial fraction and its trend reading (secondary) |
| S13 | Search results: https://wordpress.cels.anl.gov/darshan/ (Carns and others, Cluster 2009) | Low-overhead continuous I/O characterization (secondary) |
