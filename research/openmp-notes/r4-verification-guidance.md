Role: research agent (OpenMP verification and coding guidance). Accessed 2026-10-24. Rules followed: read-only; about 91 retrievals and about 6.5 MB; no paywall circumvention; no mirrors, caches, or archives for blocked content; retrieved text treated as data; gaps marked [unverified].

**Method caveat.** The fetch tool returns model-written extracts, not verbatim text. Five PDFs were converted locally and read directly (S2, S4, S19, S20, S40). Everything else comes from extracts or abstracts. Blocked or failed, and not worked around: openmp.org (403), recercat.cat (403), bsc.es and hal.ip-paris.fr (bot wall), sc19.supercomputing.org (403), Cambridge notes (DNS failure, then a login redirect), tesisenred.net (DNS), the Süß and Leopold PDF (404), the LLNL and NERSC pages (404), uni-kassel.de (reset). Because openmp.org was blocked, spec wording comes from search extracts plus a Microsoft reproduction of the 2.0 text (S6).

## Answer in brief

1. No published OpenMP coding standard comparable to MISRA or CERT exists. The search found only tutorials, "common mistakes" papers, tool workshops, and BSC research on critical real-time use. Some safety-domain texts touch OpenMP indirectly. AUTOSAR C++14 A16-7-1 forbids `#pragma`, which covers OpenMP directives. MISRA C:2004 Rule 3.4 requires every pragma to be documented. MISRA C:2012 Amendment 4 adds "no data races" and "no deadlocks" directives, written for C11 threads. No OpenMP-specific CERT rule was found.
2. The OpenMP specification does not require implementations to check for races, deadlocks, or non-conformance. ARB and BSC authors call this unacceptable for high-integrity systems and propose a certifiable subset, built on `requires` and `assumes`.
3. Dynamic detection sees only the paths that ran and the schedules that occurred. Archer with ThreadSanitizer avoids most false reports, costs about 5 to 15 times in run time, and can check target regions only by running them on the host. Tasking needs research tools. Mapping errors (stale or uninitialized data) escape race detectors, and no single tool catches every class.
4. Static checkers reach about 90% on DataRaceBench but still give false positives. Compiler diagnostics and lint can enforce `default(none)`. Formal proof of race freedom works only for small kernels or subsets.
5. The spec allows a program that is correct in parallel but wrong when built serially. It also allows results to change with the thread count. Common practice is to test at several thread counts (1 included), with OpenMP disabled, and repeatedly, but no guidance codifies this. The SOLLVE suite shows gaps and regressions between implementations, so conformance has to be shown for each toolchain.
6. The order in which reduction results are combined is unspecified. A static schedule or the `reproducible` modifier fixes which thread gets which iterations, but not the combination order. Bitwise reproducibility needs a reduction the project controls or order-independent summation, at roughly 2 times the cost. `OMP_DISPLAY_ENV` and `OMP_DISPLAY_AFFINITY` record runtime settings.
7. High-assurance research proposes four measures: a restricted subset, static task allocation, bounded runtime memory set up in advance, and exclusion of nondeterministic constructs (`critical`, `atomic`, `flush`).

## Q1. Published coding guidance

| Item | Finding | Standing/date | Source |
|---|---|---|---|
| Spec scope clause | Implementations are "not required to check for data dependences, data conflicts, race conditions, or deadlocks". The developer must produce a conforming program. | Normative, 2.0 through 5.2 (extract) | S6, S7 |
| Spec execution model (2.0) | A program that fails when run sequentially is "possible and permitted". Different degrees of parallelism may give different floating-point results. | Normative, 2002 | S6 |
| AUTOSAR C++14 A16-7-1 | "The #pragma directive shall not be used" because pragmas are implementation-defined. OpenMP would need a recorded deviation. | Industry guideline, seen through tool documentation | S8 |
| MISRA C:2004 Rule 3.4 | Document and explain every `#pragma`, recorded in the software management plan and compliance matrix. A mapping to C:2012 Directive 1.1 is [unverified]. | Required rule; forum clarification 2010 | S9 |
| MISRA C:2012 Amendment 4 | Directive 5.1: no data races. Directive 5.2: no deadlocks. The amendment targets C11 threads. | March 2023, paywalled, not read | S10 |
| SEI CERT C | Has concurrency rules for C11 threads and POSIX threads. None specific to OpenMP were found. | Negative finding [unverified] | search |
| Süß and Leopold, "Common Mistakes in OpenMP" | Student-error study separating correctness from performance mistakes. Its contents were not readable. | IWOMP 2006 | S12, S13 |
| Münchhalfen et al. | Classification of common OpenMP errors (metadata only). | IWOMP 2014 | S14 |
| Intel compiler guide | Most races come from shared variables that should be private. Use `DEFAULT(NONE)`. Private copies start uninitialized. | Vendor documentation, 2023 to 2026 (extract) | S15 |
| Oracle, LLNL tutorials | Oracle covers scope checking and automatic scoping. LLNL teaches without setting rules. | 2014; undated | S16, S17 |
| NERSC, OLCF, PRACE, EuroHPC | Training focused on performance and offload. No correctness standard found. | Negative finding | search |
| Royuela et al. | Proposes specification changes, plus compiler and runtime requirements, for functional safety. The details are [unverified]. | IWOMP 2017 | S1 |
| Serrano et al. | A few specification changes would support priorities, preemption, and migration. | IWOMP 2018 | S3 |
| Munera et al. | Dynamic task memory "jeopardizes the qualification processes". Proposes static preallocation. Safety standards need evidence of no races, no dynamic-memory faults, and no timing violations. | DATE 2020 (full text) | S2 |
| Klemm (ARB), Quiñones, Taft, Ziegenbein (Bosch), Royuela | Developer responsibility is "not acceptable in high integrity systems". A subset is needed that is "rich enough to be useful and small enough such that it can be certified", built on `requires` and `assumes`. OpenMP has no resilience mechanisms. | Ada Letters, December 2020 | S4, S5 |
| Duran et al. | OpenMP "does not have any recovery mechanism". Proposes error-handling constructs. | 2007 to 2008 | S18 |
| ARB safety profile | None found. | [unverified] | search |

## Q2. Dynamic verification

| Item | Finding | Standing/date | Source |
|---|---|---|---|
| Archer: what it finds | Data races. It passes OpenMP synchronization to ThreadSanitizer, which avoids false reports. Ships with LLVM 10 and later. Its `ignore_serial` setting can miss races from non-OpenMP concurrency. | Maintained; slides February 2026 | S20, S21 |
| Archer: cost | ThreadSanitizer slows programs 5 to 15 times. A known issue raises overhead at 5 or more threads. Memory use is high, and `flush_shadow` cuts it by about 30% (the authors' own figure). | 2026 | S20, S21 |
| Archer: misses | Detection depends on "the schedule actually played out". Code that did not execute is never checked. | 2017 critique | S22 |
| Offload | Target regions are checked only by compiling them for the host, not on the device. | Workshop slides [date unverified] | S19 |
| ROMP | Judges races against logical parallelism, including tasks. Reports that older tools miss dependences carried across loop iterations and falsely flag ordered critical sections. | SC18 | S23 |
| TaskSanitizer, Taskgrind | Find determinacy races between tasks. Taskgrind reports fewer false negatives. | 2018; 2024 | S24, S25 |
| ARBALEST | Finds mapping errors, which come mainly from wrong `map` and `nowait` clauses. Unified memory does not prevent them. | IPDPS 2021 | S26 |
| Memory-anomaly study | Every stale-data case was missed by all three tools tested. "None of these tools can currently handle all three kinds", so the authors recommend running several. | 2020 | S27 |
| Other sanitizers | MemorySanitizer slows about 3 times; AddressSanitizer about 2 times. | 2026 | S20 |
| OMPT | Standard interface for first-party tools (callbacks, thread state, device tracing). Archer, ROMP, TaskSanitizer, and OMPDataPerf build on it. | Spec 5.0 onward | S53, S54 |
| OMPD | Standard interface for third-party debuggers, working on live processes or core files. Device support is [unverified]. | Spec 5.0 onward | S53 |

## Q3. Static verification

| Item | Finding | Standing/date | Source |
|---|---|---|---|
| Compiler diagnostics | Example: GCC added the `-Wopenmp` warning group in 2023, on by default. Compilers reject missing data-sharing attributes under `default(none)`. | Implementation-specific | S34 |
| Lint | Example: clang-tidy `openmp-use-default-none` and `openmp-exception-escape`. | Maintained | S33 |
| Race checkers | LLOV is fast but limited to affine code and misses races that cross explicit synchronization. A 2021 checker reports about 90% accuracy, target constructs included. OMPRacer passed 105 of 116 cases. | 2019 to 2021 | S29, S30, S31 |
| Residual false positives | Static tools "still produce false positives that often defeat the purpose". | 2025 | S32 |
| Structural checks | Static validation of barriers and worksharing. Detection of deadlocks between tasks. Compiler hints on task correctness. | Research | S38, S39, S56 |
| Deductive verification | VerCors handles C with OpenMP using permission logic. A thesis covers a "widely-used subset of OpenMP". | 2018 to 2021 | S35 |
| Model checking | CIVL proves race freedom within small bounds. | CAV 2023 | S36 |
| Formal semantics | Built on CompCert. Any successful execution is race-free. Which constructs it covers is [unverified]. | May 2026 | S37 |
| Benchmarks | DataRaceBench 1.4.0. The dashboard was last updated in 2021 and records crashes, timeouts, and unsupported features. | [unverified] | S28 |

The practical upshot: lint and diagnostics enforce explicit scoping cheaply, and proofs are feasible only for small kernels or subsets.

## Q4. Testing practice

| Item | Finding | Standing/date | Source |
|---|---|---|---|
| Serial build | The spec permits programs that are correct in parallel but wrong in serial, so a serial build test is meaningful. `_OPENMP` guards the stub code. | Normative basis | S6 |
| Thread counts and repetition | Test suites rerun at 1, 2, and 4 threads and repeat checks in loops. | Examples only | S57 |
| Probabilistic failure | One passing run is weak evidence. `default(private)` is dangerous. | Course notes [unverified] | S55 |
| Tolerance | Results may differ with the degree of parallelism, so comparisons need a declared tolerance. | Normative basis | S6, S42 |
| SOLLVE V&V | OpenMP 4.5 features are broadly portable. Only 18% of 5.0 C/C++ tests and 2% of 5.1 tests passed on all five compilers. Results were inconsistent between releases of one compiler. The suite exposed spec ambiguities and errors in its own tests. | 2022 to 2023 | S40, S41 |

The SOLLVE results mean conformance is a property of each toolchain version, and new features are the least portable.

## Q5. Reproducibility and determinism

| Item | Finding | Standing/date | Source |
|---|---|---|---|
| Reduction order | The order in which values are combined is "unspecified". | Spec 5.2 (extract) | S42, S43 |
| Static schedule | Gives the same iteration assignment when the iteration count, chunk size, and binding region are the same. | Spec 3.1 (secondary) | S44 |
| `reproducible` modifier | Makes the loop schedule reproducible, but not the reduction order. GCC noted in 2021 that the dynamic-schedule case was unresolved. | Spec 5.1 and 5.2 | S45 |
| Vendor switch | Example: an Intel deterministic-reduction variable. It needs a fixed thread count and strict floating-point settings, and sometimes has no effect. | Forum | S49 |
| Reproducible summation | ReproBLAS is independent of the reduction tree but single-core. One vendor's reproducibility mode costs about 2 times. | 2016 to 2018 | S47, S48 |
| Recording settings | `OMP_DISPLAY_ENV` (true, false, or verbose), `OMP_DISPLAY_AFFINITY`, and `OMP_AFFINITY_FORMAT` report settings and bindings. | Spec 5.0 onward | S46 |

What can be achieved: bitwise reproducibility across thread counts requires reductions the project controls or order-independent summation. Fixing the thread count, schedule, and toolchain only reduces variation.

## Q6. Beyond ordinary practice

| Item | Finding | Standing/date | Source |
|---|---|---|---|
| Certifiable subset | Contracts expressed with `requires` and `assumes`. The Ada model on top of OpenMP already acts as a subset. | 2020 | S4 |
| Static allocation | Automotive systems bar dynamic scheduling and bind tasks to cores statically. Two allocation methods that stay OpenMP-compliant are proposed. | 2017 | S51 |
| Bounded memory | Allocate everything at initialization, in line with MISRA's advice. | 2020 | S2 |
| Deterministic subset | Excludes `critical`, `atomic`, and `flush`. 81% of nondeterministic uses could be expressed deterministically. | 2011 | S50 |

## What a standard could require as an outcome

1. Every directive is recorded and justified against the project's language rules. Why: AUTOSAR forbids pragmas and MISRA requires them documented (S8, S9).
2. All data-sharing attributes are explicit. Why: wrong sharing is the leading cause of races and memory anomalies (S15, S27).
3. A defined subset of OpenMP features is permitted, and the reasons are recorded. Why: a certifiable subset is the main high-integrity proposal, and new features are the least portable (S4, S40).
4. Race and deadlock freedom is supported by more than one method, and the remaining gaps are stated (unexecuted paths, unobserved schedules, device code). Why: every method misses whole classes of defect (S2, S22, S27).
5. Offloaded regions are checked for mapping errors as well as races. Why: race detectors miss stale data (S26, S27).
6. Tests pass at 1 thread and at several larger counts, under every schedule and binding setting in use, with OpenMP disabled, and under repetition. Why: the spec permits programs that are wrong in serial, and failures are probabilistic (S6, S55).
7. Results match a reference within a declared tolerance, or bitwise where that is required. Why: the reduction order is unspecified (S6, S42).
8. Where reproducibility is required, the combination order does not depend on the runtime. Why: a static schedule does not fix it (S42, S45).
9. Each run records its runtime settings and affinity. Why: the spec provides variables for displaying them (S46).
10. Each compiler and runtime version is shown to conform for the features the project uses. Why: SOLLVE found gaps and regressions (S40).
11. In high-integrity use, runtime memory is bounded and fixed before parallel execution begins. Why: qualification requires it (S2).

## Unverified

- What Royuela 2017 specifically proposes.
- Spec quotations taken from extracts.
- The mapping to MISRA Directive 1.1 and the Amendment 4 rule count.
- That no OpenMP-specific CERT rules exist.
- Taskgrind's venue.
- Whether OMPD supports devices.
- What S37 covers.
- The live DataRaceBench and SOLLVE results.
- The date of the TW46 slides.
- The claims attributed to S55.
- The contents of Süß and Leopold.

## Sources

| ID | URL | Supports |
|---|---|---|
| S1 | https://recercat.cat/handle/2072/292503 | Functional safety 2017 |
| S2 | https://past.date-conference.com/proceedings-archive/2020/pdf/0241.pdf | Qualification, memory |
| S3 | https://upcommons.upc.edu/handle/2117/125131 | Real-time spec changes |
| S4 | https://upcommons.upc.edu/entities/publication/b1f26e69-cd22-4820-898c-5d2123f76ae5/full | Certifiable subset |
| S5 | https://2020.splashcon.org/details/hilt-2020-papers/5/Panel-OpenMP-for-High-Integrity-systems-Moving-responsibility-from-users-to-vendors | Panel |
| S6 | https://learn.microsoft.com/en-us/cpp/parallel/openmp/1-introduction?view=msvc-170 | Spec 2.0 scope and execution model |
| S7 | https://www.openmp.org/spec-html/5.2/openmpse1.html | Scope clause 5.x |
| S8 | https://es.mathworks.com/help/bugfinder/ref/autosarc14rulea1671.html | AUTOSAR A16-7-1 |
| S9 | https://forum.misra.org.uk/showthread.php?tid=711 | MISRA Rule 3.4 |
| S10 | https://www.embedded.com/?p=4479696 | Amendment 4 |
| S12 | https://api.openalex.org/works/doi:10.1007%2F978-3-540-68555-5_26 | Süß and Leopold |
| S13 | https://www.thinkingparallel.com/?p=158 | Top 15 mistakes |
| S14 | https://www.itc.rwth-aachen.de/go/id/fddi/file/444171?lidx=1 | Error classes |
| S15 | https://www.intel.com/content/www/us/en/docs/fortran-compiler/developer-guide-reference/2024-2/openmp-advanced-issues.html | `default(none)` |
| S16 | https://hpc-tutorials.llnl.gov/openmp/ | LLNL tutorial |
| S17 | https://docs.oracle.com/cd/E37069_01/html/E37081/aewcv.html | Oracle guide |
| S18 | https://upcommons.upc.edu/entities/publication/fb72508b-84cc-49d0-a26f-325afba65f8f/full | Error handling |
| S19 | https://vi-hps.org/cms/upload/material/tw46/TW46_RWTH.pdf | Offload to host |
| S20 | https://www.vi-hps.org/cms/upload/material/tw48/BSC26_MPI-OpenMP_Correctness_Checking_with_MUST-Archer.pdf | Archer 2026, overheads |
| S21 | https://openmp.llvm.org/doxygen/md_tools_archer_README.html | Archer options |
| S22 | https://arxiv.org/pdf/1709.04551 | Schedule dependence |
| S23 | https://sc18.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap179.html | ROMP |
| S24 | https://github.com/hassansalehe/TaskSanitizer | Task races |
| S25 | https://researchportal.ip-paris.fr/en/publications/taskgrind-heavyweight-dynamic-binary-instrumentation-for-parallel/ | Taskgrind |
| S26 | https://impact.ornl.gov/en/publications/arbalest-dynamic-detection-of-data-mapping-issues-in-heterogeneou/ | Mapping issues |
| S27 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7460291/ | Memory anomalies |
| S28 | https://github.com/LLNL/dataracebench | Benchmark |
| S29 | https://arxiv.org/pdf/1912.12189 | LLOV |
| S30 | https://arxiv.org/abs/2111.04259v1 | Static, offload |
| S31 | https://sc20.supercomputing.org/presentation/index-id=pap488&sess=sess168.html | OMPRacer |
| S32 | https://arxiv.org/abs/2503.13864 | False positives |
| S33 | https://clang.llvm.org/extra/doxygen/classclang_1_1tidy_1_1openmp_1_1UseDefaultNoneCheck.html | Lint |
| S34 | https://inbox.sourceware.org/fortran/ZWRv4tnAQoyWmL+5@tucnak/t/ | Compiler warnings |
| S35 | https://research.utwente.nl/en/publications/verification-of-program-parallelization/ | Deductive verification |
| S36 | https://par.nsf.gov/biblio/10434666-model-checking-race-freedom-when-sequential-consistency-data-race-free-programs-guaranteed | Model checking |
| S37 | https://arxiv.org/abs/2605.26527 | Formal semantics |
| S38 | https://researchportal.ip-paris.fr/en/publications/static-validation-of-barriers-and-worksharing-constructs-in-openm/ | Barrier checks |
| S39 | https://www.sc15.supercomputing.org/sites/all/themes/SC15images/tech_poster/tech_poster_pages/post149.html | Task deadlocks |
| S40 | https://arxiv.org/pdf/2208.13301 | SOLLVE results |
| S41 | https://crpl.cis.udel.edu/ompvvsollve/Publications/_index.files/slide.2024-SIAM-OpenMP-VV.pdf | SOLLVE 2024 |
| S42 | https://www.openmp.org/spec-html/5.2/openmpsu50.html | Reduction order |
| S43 | https://arxiv.org/abs/2408.05148 | Non-associativity |
| S44 | https://cseweb.ucsd.edu/classes/wi16/cse160-a/static/Lec12-slides.pdf | Static schedule |
| S45 | https://www.openmp.org/spec-html/5.1/openmpsu47.html | `reproducible` |
| S46 | https://www.openmp.org/spec-html/5.1/openmpse70.html | Display variables |
| S47 | https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-121.html | Reproducible sums |
| S48 | https://www.pdc.kth.se/~riakymch/pubs/iakymchuk.scan16.pdf | Cost |
| S49 | https://community.intel.com/t5/Intel-Fortran-Compiler/Run-to-Run-Reproducibility-in-OpenMP/m-p/1151096 | Vendor switch |
| S50 | https://dedis.cs.yale.edu/2010/det/papers/hotpar11-abs/ | Deterministic OpenMP |
| S51 | https://hipert.unimore.it/people/marko/papers/ASP-DAC17.pdf | Static allocation |
| S53 | https://www.openmp.org/spec-html/5.0/openmpch4.html | OMPT, OMPD |
| S54 | https://arxiv.org/abs/2601.12713v1 | OMPT tooling 2026 |
| S55 | https://www-uxsup.csx.cam.ac.uk/courses/moved.OpenMP/paper_6.pdf | Course notes (extract) |
| S56 | https://upcommons.upc.edu/entities/publication/f4eb46dc-6c2e-41a7-802f-2e2f3e354b74/full | Compiler hints |
| S57 | https://llvm.googlesource.com/openmp/+/master/runtime/test/api/omp_get_num_threads.c | Test repetition |
