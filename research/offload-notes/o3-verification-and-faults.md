Role: research agent (note O3, verification, testing, faults, and operation of offloaded code). Accessed 2026-10-24. Retrieval: about 40 items (fetches and searches) and about 13 MB, under the 2,000-item and 2,000 MB budgets. Rules followed: read-only; no paywall circumvented; no mirrors, caches, or archives for blocked content; no credentials; retrieved text treated as data; gaps marked [unverified].

# Verification, testing, faults, and operation of offloaded accelerator code

**Annotation by the drafter (2026-10-24).** Source S15 is excluded from the evidence base. It is a third-party copy of source code that quotes the Vulkan specification, retrieved after the specification page was blocked (HTTP 403), which the custodian's rule against mirrors of blocked content does not admit. Claims that rest on S15 alone (the causes of device loss in practice 15 and in the row "Device lost or reset during a run") are not used.

**Method caveat.** The fetch tool returns model-written extracts, not verbatim pages. Four PDFs were converted locally and read directly: the Llama 3 paper (S6), the GPUVerify OOPSLA paper (S3), the NVIDIA gate-level SDC paper (S9, abstract and introduction only; the rest was not read), and the Frontier defective-hardware paper (S12, introduction and outline only). Everything else rests on extracts or search-result text and is marked "extract" in the tables. Fetches that failed or returned only a table of contents, and were not worked around: the OSDI 2026 SDC paper (403), the Vulkan specification page (403), the NVML throttle-reason page (404), the Microsoft GPUVerify page (404), the NVIDIA Xid catalog and the A100 memory-error page (tables of contents only), the CUDA compatibility sub-pages and the nvcc compatibility sections (not reached), the container-toolkit pages (overview only), and the SYCL specification error-handling chapter (not reached). Rows built on those gaps cite the substitute source and are marked. Two earlier notes already cover related ground, so this note points to them instead of repeating them: the OpenMP verification note (r4) for race detectors, static checkers, and reduction order, and the distributed-resilience note (c3) for checkpointing, idempotent retries, and the Google and Meta CPU silent-corruption reports (c3 S20, S21).

## Answer in brief

1. Treat every dynamic checker as a sampler of the runs it saw. The vendor memory-error checker finds out-of-bounds and misaligned accesses, but its hardware-exception reports are "imprecise"; its race checker covers only on-chip shared memory; its uninitialized-read checker covers only global memory by default; its synchronization checker misses threads that never reach a warp barrier (S1). Run each checker as a separate pass, and state in the record which memory spaces and launch configurations were never checked. Holds across models; the tool names do not.
2. Static and formal verification of kernels is real but narrow. The best-known verifier proved or refuted race and barrier-divergence freedom for most of 163 kernels, but excluded kernels with atomics (7) and double-indirect shared writes (12) as out of scope, models floating point abstractly (one false alarm seen), and needed hand-written invariants in some cases (S3). Use it where the kernel fits and claim only what the tool proves, for the sizes and assumptions stated.
3. Device sanitizers may be heavy, partial, or absent on a platform. One vendor's device sanitizer is beta, needs an instrumented runtime or errors may go unreported, and can make device compile time "unacceptable" (S5). A standard should require a documented verification plan per target, not a specific tool.
4. Test the launch geometry, not only the algorithm. Sizes that do not divide the block or work-group size, size 0 and 1, the largest supported size, the last partial block, and several block shapes find the boundary-thread and guard defects; none of this is published as a single rule, so it rests on how the checkers and the verifier define their errors (S1, S3) [the specific defect list is the author's inference].
5. Compare against a host reference with a declared tolerance, and repeat runs. Floating-point order on a device is not fixed by the programming model, and race and synchronization defects are probabilistic (S1, S3; r4 on reduction order).
6. Test with asynchrony on and off. Forcing synchronous launches moves an error to the call that caused it, which helps diagnosis, but it also hides missing synchronization and overlap defects, so a program tested only that way is untested in its production mode (S4).
7. Check every runtime return code, and know that device errors are asynchronous and sticky. A launch call that returns success says the parameters were valid, not that the kernel ran; an execution error appears at a later call and then repeats on every call until cleared (S4). Holds for any queue-based model; specifics differ by API (SYCL uses an asynchronous handler, S19 [not read]).
8. Device code is tied to device architecture. A build holds machine code for named architectures plus optional intermediate code that the driver compiles at load time; if neither matches the device, the program fails or silently takes a slow path (S7, S8). Test on every architecture in the support list, and test the intermediate-code path on purpose with a forced-compile switch (S8).
9. First-run costs and caches distort measurements and reproducibility. Lazy module loading moves code loading to the first launch of each kernel, and the compile cache lives in a per-user directory with a size limit and a switch to disable it (S8). Warm up, then measure, and report whether caches were cold.
10. Time device work by device-side timestamps or after a synchronization, never by a host timer around an asynchronous launch (S4). Report the clock state: the device lowers clocks for thermal, power-cap, and external power-brake reasons and exposes counters for each (S13). Measured run-to-run and device-to-device variation is large: 8% average and up to 22% across identical devices in five centers, with outliers 1.5 times slower (S11).
11. A run record for offload holds at least: device model and count, device identifier, driver version, runtime and compiler versions, library versions, firmware, memory-protection (ECC) state, compute mode, power limit, clock settings, the binary's architecture list, whether intermediate code was compiled at load, and cache state. Why: each of these changes behavior or results (S4, S8, S13, S6). The record contents are a synthesis; no single published checklist was found [unverified].
12. Memory errors are corrected, contained, or uncorrected, and the program must be told which. Field studies show uncorrected memory errors and devices that "fall off the bus" as replacement causes on Titan (S10), and a 3.2 times lower per-device mean time between memory errors on H100 than on A100 at one site (S2). A job that cannot survive a device error should say so and exit with a clear status.
13. Silent corruption is measured, not hypothetical, on accelerators. In 54 days of 16,000-GPU training, 6 of 419 unexpected interruptions were attributed to silent data corruption, and the single largest category was faulty GPUs (S6). A production study reports that standard synthetic tests miss over 60% of defective GPUs [search extract of the abstract, S9b]. Corruption is not mainly NaN or infinity: NaN/infinity were 1.01% of outcomes in gate-level injection (S9).
14. Combine detectors. Algorithm-based checksums protect specific kernels (matrix multiply, factorizations) at lower cost than duplication, but floating point forces rounding-error thresholds (S14); redundant execution costs 2 times to detect and 3 times to correct (S9); periodic single-node self-tests found "bad actor" nodes on an exascale system (S12). Choose by the cost of a wrong answer.
15. On a detected device fault, the safe default is to stop trusting that device's results since the last verified point. Then (a) halt with a distinct status, (b) restart from the last verified checkpoint on a different device, or (c) retry the unit on another device when it is idempotent. Reuse the checkpoint and retry rules in c3. A lost graphics device cannot be reset in place; recovery means creating a new device object, and if the physical device is gone, only another device helps (S15 [search extract]).
16. Treat the deployed stack as part of the program. A newer toolkit can run on an older driver only under stated compatibility modes with feature limits (S16), and containers take the driver from the host, so an image cannot pin the driver (S17 [partial]). Check at startup and fail with a clear message.
17. Expect the fleet to fail in clusters. On Titan, failures rose with heat and position in the cooling path and with a corroded resistor on the boards (S10); on Frontier, failures showed seasonal patterns and a standing group of bad nodes (S12). A fleet needs health screens, not only job-level handling.
18. Performance claims need a stated device state, a warm start, repeated runs with spread, and the cooling, power, and clock conditions. Large-scale training saw a diurnal 1-2% throughput change from mid-day temperature alone (S6).

## Verification methods and blind spots

| Method | What it finds | Blind spots | Holds across models? | Source |
|---|---|---|---|---|
| Dynamic memory checker (vendor) | Out-of-bounds and misaligned accesses in global, local, and shared memory; device heap errors; API failures; leaks (opt-in) | Hardware exceptions "imprecise" (no exact thread or line); only the executed inputs; padding raises memory use and can cause out-of-memory; high tool memory with many concurrent launches | Class holds; tool is specific | S1 (extract) |
| Dynamic race checker (vendor) | Shared-memory write-after-write, read-after-write, write-after-read hazards | "Only supports detecting accesses to on-chip shared memory"; global-memory races across blocks not covered; warp-synchronous hazards reported only as warnings; no memory-error checking, so run the memory checker first | Class holds; coverage differs by tool | S1 (extract) |
| Dynamic uninitialized-read checker | Reads of uninitialized device global memory | Shared memory off by default; no memory-error checking; allocation padding distorts unused-memory reports | Class holds | S1 (extract) |
| Dynamic synchronization checker | Barrier misuse: divergence in a block or warp, invalid arguments | Does not detect threads named in a warp mask that never reach the call; some checks only on one architecture | Class holds | S1 (extract) |
| Compile-time instrumentation (vendor) | Memory errors, with less run-time cost | Only the memory checker supports it | Specific | S1 (extract) |
| Device address sanitizer (another vendor) | Invalid device accesses | Beta; instrumented runtime libraries must be loaded or errors may go unreported; needs unified-memory page-fault support; compile time can become "unacceptable," and the workarounds (skip files, recover mode) reduce coverage | Specific; class holds | S5 (search extract) |
| Abstract-device simulator (OpenCL) | Out-of-bounds, races, barrier divergence, optional uninitialized reads, on an architecture-neutral model | Does not model SIMD or caches, so hardware-dependent timing bugs do not show; a quick mode checks only the first and last work-group; interpreter is slow | Specific to OpenCL, but the idea (check on a neutral model) holds | S18 (search extract) |
| Static verifier for kernels (GPUVerify) | Race and barrier-divergence freedom of OpenCL and CUDA kernels, by reduction to a sequential program; 163 kernels in the evaluation | Atomics (7 kernels) and double-indirect shared writes (12 kernels) removed as out of scope; floating point is abstract, so one false alarm; some kernels needed manual invariants; assumes bounds stated as preconditions; benign races are reported | Method holds across kernel languages; tool is specific | S3 (read) |
| Gate-level fault injection | Shape of hardware corruption, not program defects | Simulation, not field data; one architecture | Hardware-level | S9 (abstract read) |
| Host-run of device code, or serial fallback | Logic errors independent of device behavior | Misses device-only behavior: warp execution, memory model, limits; r4 notes that host-side checking of offloaded regions does not exercise the device | Holds across models | r4 (S19), S18 |
| Formal proof (deductive, model checking) | Race freedom for small kernels or subsets | Bounded sizes or restricted subsets; see r4 Q3 | Holds | r4 |

Common to all rows: no method proves a result is right for floating-point values or finds a miscompiled kernel or a faulty device. Their coverage ends where the tool's memory spaces, architectures, and executed inputs end.

## Test strategies and the defects they find

| Strategy | Defects it finds | Caveat | Holds across models? | Source |
|---|---|---|---|---|
| Sizes that do not divide the launch configuration (for example, one more than a multiple of the block size) | Missing bounds guards, out-of-range accesses by the last partial block, unused-thread logic errors | Memory checker needed to see small out-of-bounds writes; the rule is the author's synthesis [unverified as a published rule] | Holds | S1, S3 (basis) |
| Smallest sizes (0, 1, fewer than one block) and the largest supported size | Zero-size launch errors, index overflow, 32-bit limits, allocation failure | Largest sizes need the memory of the target device | Holds | basis: S1, S3 |
| Boundary threads (first, last, first of block, last of warp) | Off-by-one and partial-warp defects | Warp size is not the same on all devices; do not hard-code it | Holds in principle | S3 (sub-group size discussion) |
| Several launch configurations (block shape, number of blocks, tile size) | Hidden assumptions about block size or resource limits; barrier divergence that depends on shape | Verifier results hold only for the sizes assumed in its preconditions | Holds | S3 |
| Several devices and device generations | Code that works on one architecture's memory model or warp behavior and fails on another; missing architecture images | Needs hardware; emulation is not a substitute | Holds | S3, S7 |
| Host reference with declared tolerance | Wrong arithmetic, wrong indexing, precision loss | Tolerance must be justified; the same bug in both versions escapes | Holds | S6 (basis) |
| Randomized inputs and repeated runs | Races and uninitialized reads that appear only in some schedules | A passing run proves little (r4 S22) | Holds | r4 |
| Asynchronous operations made synchronous for debugging | Locates the failing call; a launch error appears at the call that caused it | Hides missing synchronization, ordering, and overlap defects; the production mode is untested | Holds for queue-based models | S4 |
| Same tests with synchronous mode off, and under stress (many streams or queues) | Missing dependencies between operations | Need the checkers above to see them | Holds | S1, S4 |
| Forced compile of intermediate code | Proves the fallback path exists and works | Slower load; changes timing | Specific to models that ship intermediate code; the principle (test each shipped path) holds | S8 |
| Cold-cache and warm-cache runs | Startup and first-launch behavior; cache-dependent failures | Cache location and size are per user | Holds for models with load-time compilation | S8 |
| Periodic device self-test on production hardware | Marginal or defective devices | Needs idle time or a reserved test slot; tests miss some defects | Holds | S12, S9b |

## Build and deployment hazards

| Hazard | Facts | Holds across models? | Source |
|---|---|---|---|
| Machine code is tied to an architecture | A build names real architectures (machine code) and virtual architectures (intermediate code). The binary can hold several. At launch the runtime picks a matching image. | Holds in concept (SPIR-V, offload bundles, fat binaries); names differ | S7 (extract) |
| No matching image | Embedded intermediate code is compiled by the runtime when no binary image matches the device. If neither exists, launch fails. The failure text is vendor-specific. | Holds | S7 (extract) |
| Native-only builds | A "native" option builds only for the devices visible on the build machine; a build made that way runs only on matching devices | Specific, but the hazard holds | S7 (extract) |
| Intermediate code and its cache | The driver caches compiled intermediate code and finalized binaries in a per-user directory (default size 1 GiB, maximum 4 GiB); entries too large are not cached and old ones are evicted; a switch disables the cache and helps diagnose differences across driver versions | Specific to that vendor; cache pattern common | S8 (extract) |
| Forcing the compile path | A switch makes the driver ignore embedded machine code and compile the intermediate code; documented use: confirm that the intermediate code is present and that forward compatibility works | Specific; practice holds | S8 (extract) |
| Lazy loading | By default code loads at first launch of each kernel, shifting cost to the first launch; an eager mode makes launch overhead more predictable at more startup time and memory | Specific; first-run cost holds | S8 (extract) |
| Driver and toolkit versions | Minor-version compatibility lets an application built on a toolkit run on a sufficiently new driver within one major family, with feature limits. A forward-compatibility package lets a newer toolkit run on an older base driver across families, depending on platform and device support. Rules and error text were not read. | Specific; the need to check holds | S16 (overview only) |
| Containers | The container toolkit injects host driver libraries into the container, so the image cannot control the driver version. Details were not read. | Holds for containers | S17 (partial) [unverified] |
| Debug build behavior | Instrumentation (sanitizer) builds need matching instrumented runtime libraries at run time | Specific; principle holds | S5 |
| Asynchronous-by-default launches | A synchronous-launch switch exists for debugging and slows the program | Holds | S8 |
| Run record fields | Device model; driver, runtime, compiler, library versions; firmware; ECC state; compute mode; power limit; application clocks; architecture list of the binary; cache state; environment switches. Basis: ECC changes usable memory and bandwidth (S4); clocks and power change performance (S11, S13); the switches above change code paths (S8). | Holds | S4, S8, S11, S13 [synthesis] |

## Fault classes, rates, how they surface, and responses

| Fault class | Published rate or finding | How it surfaces | Response | Holds across models? | Source |
|---|---|---|---|---|---|
| Corrected memory error (ECC) | ECC costs about 6.25% of GDDR capacity and about 20% of effective bandwidth in the guide's example; no bandwidth overhead for the high-bandwidth stacked memory it describes | Counter only; no program-visible effect | Monitor the rate; record ECC state in the run record | ECC is hardware-level; applies to all | S4 (extract) |
| Uncorrected memory error | Titan: double-bit errors led to GPU replacement. Delta: H100 has 3.2 times lower per-device mean time between memory errors than A100; existing recovery judged insufficient for larger memory; projected 5% overprovisioning for failures | Job abort, device reset need, or an error code on a later call; the exact codes and containment behavior were not read (A100 memory-error page gave only headings: containment, page offlining, row remapping, flags) | Halt that job; restart from checkpoint on healthy device; retire or repair the device | Holds | S10, S2, S20 (headings only) |
| Device off the bus | Titan: loss of the host's connection to the GPU led to replacement | Device vanishes; calls fail | Drain node; restart elsewhere | Holds | S10 (extract) |
| Device lost or reset during a run | Graphics-API wording (via a code mirror of the spec): lost for reasons such as execution timeout, power management, platform resource management, or implementation error; the lost state cannot be cleared on that device object | Error return on the next call | Create a new device and rebuild all state, or fail over to another device | Holds for queue APIs | S15 (search extract) |
| Stalled loads and stores over device interconnect | In 16,000-GPU training, failures in a remote GPU or interconnect often show as stalled kernel loads or stores without a clear error code | Hang | Watchdog timeouts, flight-recorder traces, straggler search | Holds | S6 |
| Faulty GPU, memory, SRAM, processor | Of 419 unexpected interruptions in 54 days: faulty GPU 148, HBM3 memory 72, SRAM 19, system processor 17, silent data corruption 6, thermal interface and sensor 6 (counts as printed; the printed percentages do not equal count over 419 and are not reproduced). Paper states GPU issues are 58.7% of unexpected issues and about 78% had confirmed or suspected hardware cause | Mostly job interruption; automation handled all but 3 | Automated restart from checkpoint; fast diagnosis tools | Holds | S6 (read) |
| Silent data corruption (accelerator) | 6 of 419 interruptions in Llama 3 pre-training (1.4%); reported weekly or biweekly in another operator's training [from S9 intro, not primary]; gate-level injection: NaN or infinity is 1.01% of outcomes, single-bit flips under 40% of bit-flip events, corruption addresses periodic in warp size | No signal; wrong values; late loss spikes | Checksums, ABFT, redundant execution, self-tests, invariant checks | Holds | S6, S9 |
| Silent data corruption (CPU, for scale) | A few defective cores per several thousand machines; hundreds in hundreds of thousands | See c3 | See c3 | Holds | c3 S20, S21 |
| Defective devices missed by tests | Production LLM-training study: synthetic micro-benchmarks miss over 60% of 23 defective GPUs [abstract via search; full paper blocked] | Corrupt gradients | Test with real workloads, not only synthetic tests | Holds | S9b (search extract) |
| Hardware manufacturing or environment | Titan: corroded board resistor from 2016; heat and position in cooling path raised failure hazard; scheduling also correlated. Frontier: seasonal failure classes; standing set of bad nodes | Increasing failure rate | Screening, replacement, placement policy | Holds | S10, S12 |
| Thermal and power throttling | Reasons exposed as software thermal slowdown, hardware thermal slowdown (clocks halved or worse), software power cap, hardware power brake from an external signal, with cumulative counters. Diurnal 1-2% throughput variation in training from mid-day temperature. Frequency capping gave higher variation than power capping in an SC19 workshop study (extract) | Slower, not wrong | Read counters; record with the run; do not compare runs across clock states | Concept holds; names specific | S13, S6, S21 |
| Variability between identical devices | 8% average, up to 22%, outliers 1.5 times slower; cause: manufacturing variation and power management | Slow stragglers | Screen for stragglers; report spread | Holds | S11 |
| Interrupted by environment | A synchronous job fails on one GPU failure; effective training time above 90% needed fast restart and automation | Job restart | See c3 checkpoint rules | Holds | S6 |

How faults surface, in order of how easily a program can see them: an error return on a later call (asynchronous and sticky, S4); a hang with no error (S6); a slower run (S13); a correct-looking wrong answer (S9, S6). A standard should plan for the last two because the program receives no signal.

Detection and response notes:

- Checksums and algorithm-based checks: encode input with checksum rows and columns, multiply, compare. Cost is generally below the multiply itself, but floating point requires runtime rounding-error bounds to avoid false alarms (S14, search extract; overhead figures not found).
- Redundant execution: detection needs two copies (2 times), correction three (3 times); suspicion-based monitoring of NaN, infinity, or loss spikes has delayed and unreliable rollback (S9).
- Periodic self-tests: Frontier runs single-node screens, in 30 minutes or less, in idle gaps and as an epilog, removes failing nodes, and shrinks failing jobs until one part is isolated (S12, outline read).
- Detected fault, ordered options: stop and report; restart from the last verified checkpoint on another device; retry the idempotent unit on another device. A retry is safe only for deterministic, side-effect-free units (c3).
- Hardware-level tests alone are not enough: real workload tests found defects that synthetic tests missed (S9b, S12).

## Measurement pitfalls

| Pitfall | Fact | Effect on claims | Holds across models? | Source |
|---|---|---|---|---|
| Timing asynchronous work with a host timer | Launches and asynchronous copies return before they finish; synchronize before starting and stopping a host timer, or use device events (about half-microsecond resolution) | A host timer around a launch measures launch cost only | Holds | S4 |
| Stream-level synchronization with other streams active | Other streams' work may be included | Inflated time | Holds | S4 |
| Synchronous-launch switch on | Disables asynchrony; slows the program | Not the production time | Holds | S8 |
| First-run costs | Lazy loading, load-time compilation of intermediate code, cache cold; page migration for managed memory [page migration not read; S4 mentions only pinned-memory requirements] | First iteration slower than steady state | Holds | S8, S4 |
| Clock variability | Throttling by temperature, power cap, external power brake; applications-clock settings; diurnal effect of 1-2% at scale | Same code, different time | Holds | S13, S6 |
| Device-to-device variability | 8% average, up to 22% | A one-device result is not the fleet result | Holds | S11 |
| ECC mode | Changes bandwidth for some memory types | Bandwidth results not comparable across ECC states | Specific to memory type | S4 |
| Power or frequency capping | Frequency capping gave higher variation and anomalous behavior than power capping (extract) | Capped runs need their own baseline | Holds | S21 (extract) |
| Results used as a correctness oracle | A fast wrong answer is still fast | Performance claims need a verified result | Holds | S9, S6 |

What this means for claims: state the device, the clock and power state, the cache state, warm-up, number of runs, spread (not only the best), what is timed (kernel only, or with transfers and initialization), and that the output was verified.

## Timeless versus moving

Timeless (true across models and likely to stay true):

- Device errors reach the program late or not at all; the program must check status explicitly and treat success of a launch as weak evidence (S4).
- Asynchrony hides defects when forced off and hides time when ignored.
- Machine code is tied to a device generation; a shipped binary needs a tested path for each supported device and a defined behavior when none matches.
- Compiled-at-load code and its caches change first-run time and can change results between driver versions.
- Hardware fails in silent, slow, and loud ways; large fleets see all three at a measurable rate (S6, S10, S12).
- No single detector covers a defect class; combine methods and state the gap.
- Timing needs a synchronization point, a warm start, repetition, and a recorded device state.
- A run record is needed because driver, runtime, firmware, clocks, and ECC state change behavior.

Moving (tool and generation specific; a standard should not name them):

- Which memory spaces a checker covers (the race checker's shared-memory limit may change).
- Sanitizer beta status and platform requirements (S5).
- Specific error codes, environment variables, cache sizes, and defaults (S8).
- Compatibility packages and driver rules (S16).
- Memory-error containment and row-remapping features of a given device generation, and error-rate ratios between generations (S2, S20).
- Exact failure rates: they depend on device generation, cooling, and fleet age (S2, S10, S6).
- The share of silent corruption: so far observed from 1.4% of interruptions at one operator to weekly events at another (S6, S9 intro).

## Not verified

- NVIDIA Xid codes and recommended actions; the memory-error page gave only a table of contents. No claim about specific Xid numbers is made.
- Driver-to-toolkit compatibility rules, the error text when the driver is too old, and cache invalidation on driver upgrade: not found in retrieved text.
- Container-toolkit mechanics: overview only.
- Page-migration first-touch costs for managed memory: not retrieved.
- SYCL asynchronous error-handler timing and OpenCL profiling rules: spec text not reached.
- OSDI 2026 SDC paper: abstract only through a search extract; the 60% figure and the 23-device count are unconfirmed.
- Tiwari et al. HPCA 2015 and Ostrouchov et al. SC20 details: abstracts and search extracts only; no error rates were read.
- GPU ABFT overhead figures: not found; only the method and the floating-point difficulty.
- Frontier paper: only the introduction and outline were read; numeric failure rates not used.
- The Llama 3 table prints percentages that do not equal count divided by 419 (for example, 148 is printed as 30.1%); counts are used as printed and percentages avoided.
- The Delta study: abstract only; absolute rates not read.
- The recommended test list (non-divisible sizes and others) is the author's synthesis from checker and verifier definitions, not a published standard. No published GPU testing guideline was found.
- Run-record list: synthesis; no published checklist found.
- Intel and AMD tool specifics beyond the sanitizer page: not retrieved. Evidence skews to one vendor's documentation; counterparts are assumed, not confirmed.

## Sources

| ID | URL | Supports |
|---|---|---|
| S1 | https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html | Memory, race, init, sync checkers and their limits (extract) |
| S2 | https://arxiv.org/abs/2503.11901 | Delta A100/H100 resilience, 3.2 times MTBE, 5% overprovisioning (abstract) |
| S3 | https://www.doc.ic.ac.uk/~afd/papers/2012/OOPSLA.pdf | GPUVerify: scope, 163 kernels, exclusions, floating point, false alarm (read locally) |
| S4 | https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html and https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html | Timing, events, asynchronous and sticky errors, ECC cost (extracts) |
| S5 | https://rocm.docs.amd.com/projects/llvm-project/en/docs-7.2.4/conceptual/using-gpu-sanitizer.html | Device address sanitizer requirements and limits (search extract) |
| S6 | https://arxiv.org/abs/2407.21783 | Llama 3: 466 interruptions, Table 5 counts, SDC, diurnal variation (read locally from PDF) |
| S7 | https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html | Real and virtual architectures, fatbinary, load-time compile (extract) |
| S8 | https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/environment-variables.html | JIT cache, forced JIT, lazy loading, launch-blocking (extract) |
| S9 | https://arxiv.org/pdf/2605.04213 | Gate-level SDC injection, NaN share, redundancy cost (abstract and introduction read) |
| S9b | https://www.usenix.org/conference/osdi26/presentation/zheng | Production SDC-defective GPUs; abstract only through search; page blocked (403) |
| S10 | https://impact.ornl.gov/en/publications/understanding-gpu-errors-on-large-scale-hpc-systems-and-the-impli/ ; https://www.ornl.gov/research-highlight/gpu-lifetimes-titan-supercomputer-survival-analysis-and-reliability | Titan field data, double-bit and off-the-bus failures, corrosion, heat (extracts) |
| S11 | https://arxiv.org/abs/2208.11035 | Variability across identical GPUs (abstract) |
| S12 | https://cug.org/proceedings/cug2024_proceedings/includes/files/pap123s2-file1.pdf | Frontier defective-hardware screens, seasonal failures, bad-actor nodes (introduction read) |
| S13 | https://docs.nvidia.com/deploy/nvml-api/api/group__nvmlClocksEventReasons.html | Clock throttle reasons (search extract; fetch of group page 404) |
| S14 | https://arxiv.org/pdf/2305.01024 and https://www.iti.uni-stuttgart.de/fileadmin/rami/files/publications/2014/DSN_BraunHH2014.pdf | Checksum ABFT on GPUs, rounding thresholds (search extract) |
| S15 | https://opensecura.googlesource.com/3p/openxla/iree/+/2e2fc9ce9be2d8725fd02e70f2ef3b8c609a3ecb/hal/vulkan/status_util.cc | Mirror of the Vulkan device-lost commentary (search extract; spec page blocked, 403) |
| S16 | https://docs.nvidia.com/deploy/cuda-compatibility/index.html | Minor-version and forward compatibility (overview) |
| S17 | https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html | Container toolkit components (overview only) |
| S18 | https://manpages.ubuntu.com/manpages/jammy/man1/oclgrind.1.html | OpenCL abstract-device simulator features (search extract) |
| S19 | https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html | Asynchronous handler exists (section 4.13); content not read |
| S20 | https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/index.html | Headings only: containment, page offlining, row remapping |
| S21 | https://sc19.supercomputing.org/proceedings/workshops/workshop_pages/pec248.html | Power versus frequency capping variation (search extract) |
| r4, c3 | research/openmp-notes/r4-verification-guidance.md ; research/concurrency-notes/c3-distributed-resilience.md | Earlier notes; their source IDs are cited as "r4 Sn" or "c3 Sn" |
