# Research note C4: parallel programming model landscape

Role: research agent (delegated). Date accessed for all web sources: 2026-10-24. Retrieval rules followed: read-only retrieval; 61 web items (searches and page fetches), well under the 10,000 item and 10,000 MB caps; no paywalled, mirrored, cached, or archived content; two blocked or empty fetches (openshmem.org) were not worked around; retrieved text treated as data. Unconfirmed items are marked **[unverified]**.

Method caveat: the fetch tool returns a model-written extract of each page, not the page, and search results arrive as summaries. Some long pages were read only in part. Where a fact came only from a search summary, the source row says so. Hazards that I state from general knowledge rather than from a retrieved page are marked **[unverified]**. Background on MPI, OpenMP, CUDA, and HIP 7.0 comes from the earlier note `research/parallel-models.md` (accessed 2026-10-22), cited here as S50.

## Answer in brief

1. Most models need no standard of their own. Language-integrated features (C++ execution policies and `std::execution`, Fortran `do concurrent` and coarrays, C11 threads and atomics, Rust `Send`/`Sync`, Python threading/multiprocessing/asyncio and free threading, Julia tasks) belong in the matching language standard. POSIX threads belong in the C standard, with POSIX named as the platform interface.
2. HIP, SYCL device code, OpenCL, OpenACC, and offloaded C++ or Fortran standard parallelism belong in the model-neutral offload standard. Their distinct hazards fit as short per-model annexes, since the offload standard is LVL2 and may name them.
3. Library models (Kokkos, RAJA, oneTBB, Rayon, Tokio, HPX, Charm++, UPC++, Legion), OpenSHMEM, and Chapel should enter through STND.DEPS with a hardware contract until a project adopts them.
4. Thirteen hazards recur across models (races, asynchronous completion, lost errors, captured-data lifetime, memory spaces, forward progress, blocking in pools, task migration, cancellation, reduction order, oversubscription, fork after threads, tool gaps). They belong in one model-neutral rule set.
5. I found no published cross-model standard or guideline for parallel correctness. DOE reports from 2017 and 2023 are research agendas. ISO/IEC 24772-1 has a language-independent concurrency vulnerability catalogue at thread level. MISRA C and CERT C cover C threads only. The ECP successors (CASS, HPSF) publish sustainability practice, not concurrency rules.
6. Ranked additions: (a) a model-neutral concurrency rule set holding item 4; (b) a Kokkos standard, drafted only when a project adopts Kokkos; (c) an OpenACC standard, only on adoption, otherwise an offload annex; (d) a SYCL annex inside the offload standard, promoted to a standard only on adoption. Python, C++, Rust, Julia, C, and Fortran need concurrency amendments, not new standards.

## Landscape table

Status key: standard (formal spec by a standards body or consortium), de facto (one dominant implementation or project), declining, new. Status labels are my judgment from the sources, not a claim by the owner.

| Model | Owner | Version and date | Status | Distinct hazards | Recommended home | Source |
| --- | --- | --- | --- | --- | --- | --- |
| OpenACC | OpenACC organization | 3.4, June 2025 (PDF marked updated October 2025) | Standard; narrower vendor base than OpenMP offload **[unverified judgment]** | Data clauses and the present table: data already present is not recopied unless `always`/`alwaysin`/`alwaysout` is used; `capture` modifier changes behavior on unified-memory systems; `kernels` lets the compiler choose parallelism; async queues; routine parallelism level now partly inferred | Offload standard annex; STND.DEPS; own standard only on adoption | S1, S2 |
| SYCL | Khronos Group | SYCL 2020; khronos.org says Rev 11, registry HTML is Rev 12 built 2026-08-06 | Standard, multiple implementations (DPC++, AdaptiveCpp) | Queues are out-of-order by default; buffer destructors block only when the buffer has attached host memory; USM accesses get no implicit dependencies; asynchronous errors are not reported when they occur but delivered later to a handler | Offload standard annex; C++ standard for host code | S3, S4 |
| Kokkos | HPSF (core project) | 5.2.2, 2026-09-10; 5.x requires C++20 | De facto in DOE C++ codes | Lambdas must capture by value (reference capture violates Kokkos semantics); functors are copied and const, no pointer members; dispatch is asynchronous, fence before host reads; scan bodies may run more than once per index; no loop order | STND.DEPS now; own standard on adoption | S5, S6, S40 |
| RAJA | LLNL | v2026.07.1, 2026-09-28; C++20 required since v2026.07.0 | De facto (LLNL ecosystem) | Several GPU policies deprecated for removal next release; reduction default initialization deprecated; new Kahan-sum reduction "can be undone by fast-math" | STND.DEPS; offload standard | S7 |
| HIP | AMD | HIP 7.16.0 in ROCm Core SDK 10.1.0, 2026-10-05 (ROCm 7.2.x line earlier in 2026) | De facto (AMD) | HIP 7 changed error and free semantics to match CUDA (`hipFree` no longer waits for async allocations; `warpSize` not constexpr); coarse- versus fine-grained memory affects atomics on host-registered memory; WSL2 device faults may hang instead of erroring | Offload standard annex | S8, S50 |
| oneTBB | UXL Foundation (Linux Foundation) | 2023.1.0, 13 July (year 2026 inferred **[unverified]**) | De facto | Work stealing: a waiting thread may run outer-loop tasks during a nested parallel call, which corrupts thread-local state and can deadlock; fix is `this_task_arena::isolate` | C++ standard section on task libraries, or STND.DEPS | S10, S11 |
| C++ standard parallelism | ISO/IEC JTC 1/SC 22/WG21 | C++26 approved by WG21 2026-03-28; DIS ballot closed 2026-09-27, outcome not found **[unverified]** | Standard (C++17 policies); new (`std::execution`) | Policies: an exception from an element function calls `std::terminate`; under `par_unseq`/`unseq` no locks, allocation, or non-lock-free atomics. `std::execution`: a started operation state must outlive the operation at a stable address; continuations run on the completion scheduler, which may not be the caller's; `stopped` is a third completion channel | C++ standard; offload standard when policies are offloaded | S12, S13, S14, S15 |
| Fortran `do concurrent` | ISO/IEC JTC 1/SC 22/WG5 and J3 | Fortran 2023 (ISO/IEC 1539-1:2023 **[unverified]** designation) | Standard; uneven compiler support | Not necessarily concurrent; automatic localization of unspecified variables may be unprovable; written unspecified variables become undefined; `reduce` accepted by ifx, nvfortran, CCE, partial in Flang, not in GCC 14 | Fortran standard; offload standard when offloaded | S16, S17 |
| Fortran coarrays | WG5 and J3 | Fortran 2018/2023 | Standard; Flang lacks coarrays | Ordering between images undefined outside image control statements; failed images detected per team and at different points, so survivors can hang | Fortran standard | S17, S18 |
| OpenSHMEM | OpenSHMEM specification committee **[unverified name]** | 1.6 (latest by 2024, exact date **[unverified]**); 1.7 in planning (SC25 BoF) | Standard, niche | `shmem_fence` orders delivery to one PE but not completion; only `shmem_quiet` or a barrier guarantees completion and visibility; quiet orders only the calling thread; symmetric-heap allocation is collective | STND.DEPS | S19, S20 |
| POSIX threads | IEEE and The Open Group (Austin Group) | POSIX.1-2024 (Issue 8), 2024-06-14; Cor 1 in progress (PAR 2025-02-13) | Standard | Issue 8 adds clock-selecting waits (`pthread_mutex_clocklock`) and mandates `<threads.h>`; fork in a threaded process, async-signal safety, cancellation, spurious wakeups **[unverified, not retrieved]** | C standard, POSIX named as platform contract | S21, S22, S23 |
| C11 threads and atomics | ISO/IEC JTC 1/SC 22/WG14 | C23 (ISO/IEC 9899:2024); next revision planned 2028 | Standard | Both optional (`__STDC_NO_THREADS__`, `__STDC_NO_ATOMICS__`); `ATOMIC_VAR_INIT` and the `thread_local` macro removed in C23 | C standard | S14, S24 |
| Rust | Rust Project; Rayon and Tokio are separate projects | Rayon 1.12.0, 2026-04-14; Tokio 1.54.1, 2026-10-21 | Standard-like (language); de facto (crates) | `unsafe impl Send/Sync` done wrong is UB; safe Rust excludes data races but not deadlocks or general races; Tokio: dropping a non-cancellation-safe future (`read_exact`, `write_all`, `Mutex::lock`) loses data or queue place; a blocking branch stalls `select!` | Rust standard; Rayon and Tokio via STND.DEPS | S25 to S30 |
| Python concurrency | Python Software Foundation (Steering Council) | 3.15.1, 2026-10-21; 3.15.0, 2026-10-09; 3.14.9 | Standard (language); free threading supported but optional | 3.13: free-threaded build experimental. 3.14: officially supported (PEP 779 phase II), overhead about 5 to 10%, `forkserver` replaces `fork` as default start method on Linux, threads inherit the caller's context. GIL can silently re-enable on import of an unmarked extension; compound operations and shared iterators are not atomic; asyncio keeps only weak task references | Python standard (amendment) | S31 to S37 |
| Julia threads and tasks | JuliaLang | Stable docs built with 1.13.2 **[unverified release date]** | Standard-like (language) | Races make Julia memory-unsafe; tasks migrate between threads since 1.7, so `threadid()` must not index buffers; Base collections not thread-safe; finalizers can interrupt any code; non-allocating loops can block GC | Julia standard (amendment) | S38 |
| Chapel | HPSF (LF Projects) | 2.10.0, 24 September 2026 | Niche, active | Task intents decide whether outer variables are shared; locality (`on`, locales) makes remote access implicit **[unverified, not retrieved]** | STND.DEPS | S39, S40 |
| OpenCL | Khronos Group | 3.1.2 (date **[unverified]**) | Standard, declining for HPC **[unverified judgment]** | Explicit event dependencies; optional features in 3.x | Offload standard annex | S41 |
| HPX | HPSF (STE\|\|AR Group) | 1.11.0 stable; 2.0.0-rc1, 28 September (year **[unverified]**) | Niche | C++-standard-style futures across a distributed address space | STND.DEPS | S42 |
| Charm++ | UIUC PPL and Charmworks **[unverified]** | 8.1.0, 13 October (year **[unverified]**); 9.0.0-alpha2 | Niche, used in NAMD | Message-driven objects; migration **[unverified]** | STND.DEPS | S43 |
| UPC++ | LBNL Pagoda group | 2025.10.0 | Niche | One-sided RMA futures and completion **[unverified]** | STND.DEPS | S44 |

Not checked for version: Legion, Alpaka, Taskflow, StarPU, PaRSEC, Numba, CuPy, JAX, Dask, Ray, mpi4py **[unverified]**; all fit STND.DEPS.

## Question 2: shared versus model-specific hazards

### Shared hazards (model-neutral rule)

Each appears in at least three models. A model-neutral rule states it once; each LVL2 standard maps it to its constructs.

1. **Data races on shared state.** A parallel loop or task construct never makes its body safe. C++ `par`, Kokkos, Julia `@threads`, and free-threaded Python all leave race freedom to the programmer. Rust excludes data races only in safe code (S12, S26, S33, S38).
2. **Asynchronous completion.** Results and buffers are unusable until a completion point: Kokkos fence, SYCL wait or buffer destruction, `shmem_quiet`, `sync_wait`, `await`, CUDA or HIP stream synchronization (S4, S6, S13, S20). The rule: name the completion point for every asynchronous operation whose result or buffer is used.
3. **Deferred or lost errors.** SYCL delivers asynchronous errors later to a handler; asyncio only logs exceptions of unawaited tasks; C++ parallel algorithms call `std::terminate`; HIP under WSL2 may hang instead of reporting a fault (S4, S8, S12, S36). The rule: every asynchronous error channel has a declared consumer.
4. **Lifetime of captured data.** Kokkos forbids reference capture. `std::execution` requires a stable operation-state address until completion. asyncio may garbage-collect an unreferenced task (S6, S13, S36).
5. **Memory-space reachability.** Host versus device memory, the OpenSHMEM symmetric heap, coarrays, Chapel locales, and OpenACC present data all differ on which memory a construct can touch and when it is coherent (S1, S6, S19).
6. **No forward-progress guarantee between iterations.** Kokkos says not all iterations are active at once, so waiting on another iteration is illegal. C++ warns against spinning on another invocation. `do concurrent` need not be concurrent at all (S6, S12, S16).
7. **Blocking inside a worker pool.** oneTBB work stealing breaks thread-local invariants and can deadlock; a blocking Tokio `select!` branch or asyncio call stalls everything else; Rayon `scope` blocks until its tasks finish (S11, S27, S30, S36).
8. **Thread-local state under task migration.** Julia tasks migrate across threads. oneTBB nested parallelism runs other iterations on the same thread (S11, S38).
9. **Cancellation and termination.** Tokio cancellation safety, asyncio `CancelledError` that must not be swallowed, the C++ `stopped` channel, and Fortran failed images that leave survivors waiting (S13, S18, S30, S36).
10. **Nondeterministic reduction and schedule order.** Kokkos promises no loop order. RAJA's Kahan sum can be undone by fast-math. The DOE/NSF report cites summation order and fast-math as a source of irreproducible results (S6, S7, S45). The rule: declare whether a result must be bitwise reproducible or within a stated tolerance, and test under more than one thread count.
11. **Runtime composition and oversubscription.** Default thread counts come from separate environment variables (`RAYON_NUM_THREADS`, `JULIA_NUM_THREADS`, and others) and separate pools (S28, S38). Nesting one runtime inside another needs a declared thread budget. This is a hardware-contract item for STND.DEPS.
12. **Fork after threads.** Python 3.14 made `forkserver` the default on Linux because `fork` is "threading-incompatible" (S31). The POSIX rule behind it is **[unverified, not retrieved]**.
13. **Tool coverage.** Most tools cover one model; hybrid and GPU global-memory race checking is weak (S45). The rule: name the checker per model and record gaps as known risks.

### Model-specific hazards

The "Distinct hazards" column of the landscape table lists them. Each belongs in the model's recommended home, as the concrete construct that discharges a shared rule (for example, OpenSHMEM `shmem_quiet` discharges shared rule 2).

## Question 3: published cross-model guidance

I found no published standard or guideline that sets correctness rules across parallel programming models.

- **Report of the HPC Correctness Summit (2017)**, Gopalakrishnan, Hovland, Laguna, Siegel, and others, arXiv:1705.07478. It calls for research and new correctness tools for the exascale ramp-up and a follow-up workshop. The abstract gives no per-model rules (S46).
- **Report of the DOE/NSF Workshop on Correctness in Scientific Computing (June 2023)**, Gokhale, Gopalakrishnan, and others, arXiv:2312.15640. Findings: treat correctness as a design requirement; hand-written fences are error-prone and vendor documentation unclear; hybrid MPI, OpenMP, and GPU verification tools are needed; GPU race checking is weak; fast-math, FMA, and summation order change results, so determinism modes help testing; differential, metamorphic, and fuzz testing are underused. It proposes no standard (S45).
- **ISO/IEC 24772-1** (WG23, language-independent catalogue of vulnerabilities). Its drafts list concurrency entries for activation [CGA], directed termination [CGT], concurrent data access [CGX], premature termination [CGS], and lock protocol errors [CGM], mapped to CERT C rules such as CON32-C and CON33-C. It is the closest ISO cross-language guidance, but it is thread-level and does not address directive, offload, or PGAS models. Publication status and current text **[unverified]**: I saw only committee drafts (S47).
- **MISRA C:2023 and MISRA C:2025** fold in Amendment 4 (March 2023), which added rules for C11 threads and atomics. Secondary sources list directives D5.1 (no data races), D5.2 (no deadlocks), D5.3 (no dynamic thread creation) and a rule that memory synchronization be sequentially consistent. The text is paid and C-only (S48). SEI CERT C has a CON rule family **[unverified, not retrieved]**.
- **ECP successors.** ECP technical work ended December 2023. CASS (an umbrella of software stewardship organizations, sponsored by DOE ASCR) and HPSF (Linux Foundation, hosting Kokkos, Chapel, HPX, Trilinos, and others) publish community events and sustainability practice. I found no concurrency correctness guideline from either (S40, S49). The xSDK and E4S policies noted in S50 cover build, test, and packaging, not concurrency.
- **IEEE.** POSIX is an interface standard, not a correctness guideline. I found no IEEE cross-model correctness standard.

Implication: the model-neutral rule set would be original work, citing S45 and S47 as rationale, not as standards to conform to.

## Question 4: recommendation

### Ranked additional standards

1. **A model-neutral concurrency rule set** (LVL1 profile or an unnamed LVL2 standard, custodian's choice). Reason: the 13 shared hazards recur across MPI, OpenMP, offload, five language standards, and every library model. Writing them once avoids drift between six or more standards, and each named-model standard then maps them to concrete constructs. This reverses the earlier note's deferral (S50): with this many models the shared content is no longer thin.
2. **Kokkos, on adoption.** Reason: it is HPSF's core project, it spans host threads and all GPU back ends, and its capture, functor, memory-space, and fence rules fit neither the C++ standard nor a model-neutral offload standard. Draft only when a project adopts it. RAJA can be an annex of the same standard if a project uses both.
3. **OpenACC, on adoption.** Reason: it is a full directive language with its own data-presence semantics, still used in Fortran science codes **[unverified]**. Until adopted, a short annex in the offload standard is enough.
4. **SYCL, as an offload annex first.** Reason: it is a Khronos standard with several implementations, and most of its hazards are offload hazards plus C++. Promote it to its own standard only if a project adopts it as its primary model.

Not new standards but required amendments: Python (free-threading detection, GIL re-enabling, the 3.15 atomicity tables, the 3.14 start-method change, asyncio task references, cancellation), C++ (execution policies, `std::execution` lifetimes and schedulers, oneTBB-style isolation), Rust (`unsafe impl Send/Sync`, deadlocks, async cancellation safety and blocking), Julia (task migration, finalizers), C (optional threads and atomics, POSIX threads), and Fortran (`do concurrent` locality and `reduce`, coarray image control and failed images).

### Models best governed only through STND.DEPS until a project adopts them

RAJA, oneTBB, HIP-specific libraries beyond the offload annex, OpenSHMEM, Chapel, HPX, Charm++, UPC++, Legion, Rayon, Tokio, Taskflow, and Python parallel libraries (Numba, CuPy, JAX, Dask, Ray). Each needs a hardware contract recording thread pool and thread-count source, memory spaces, back end, completion and error points, and correctness tool: the parameters the shared hazards depend on.

## Unverified

1. C++26 DIS ballot outcome (closed 2026-09-27) and ISO publication date.
2. OpenSHMEM 1.6 date and committee name; OpenCL 3.1.2 date; Julia 1.13 date; Rust compiler version.
3. Release years for oneTBB 2023.x (inferred 2026), HPX, and Charm++.
4. OpenACC vendor base and Fortran use; PEP 803 `abi3t` in Python 3.15 (secondary source only).
5. ISO/IEC 24772-1 publication status; MISRA C:2025 numbering; CERT C CON rules; Fortran 2023 ISO designation.
6. POSIX fork, signal, and cancellation hazards; Chapel, Charm++, and UPC++ hazards (general knowledge).
7. ROCm "Core SDK 10.1.0" naming (stated on the release page; earlier 2026 pages used 7.2.x).
8. Status labels such as "declining" and "niche" (my judgment).

## Sources

| ID | URL | What it supports |
| --- | --- | --- |
| S1 | https://www.openacc.org/specification | OpenACC 3.4 is latest |
| S2 | Search summary citing https://en.wikipedia.org/wiki/OpenACC and https://www.openacc.org/sites/default/files/inline-images/Specification/OpenACC-3.4.pdf | 3.4 date (June 2025) and features |
| S3 | https://www.khronos.org/sycl/ | SYCL 2020 Rev 11, implementations |
| S4 | https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html | Rev 12 build date, queue order, buffer destruction, async errors |
| S5 | https://github.com/kokkos/kokkos/releases | Kokkos 5.2.2 |
| S6 | https://kokkos.org/kokkos-core-wiki/ProgrammingGuide/ParallelDispatch.html | Kokkos capture, fence, scan hazards |
| S7 | https://github.com/LLNL/RAJA/releases | RAJA versions, C++20, Kahan sum note |
| S8 | https://rocm.docs.amd.com/en/latest/about/release-notes.html | ROCm 10.1.0, HIP 7.16.0, memory and WSL2 notes |
| S10 | https://github.com/uxlfoundation/oneTBB/releases | oneTBB versions, UXL ownership |
| S11 | https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/work_isolation.html | Work isolation hazard |
| S12 | https://en.cppreference.com/w/cpp/algorithm/execution_policy_tag_t.html | Execution policy rules |
| S13 | https://en.cppreference.com/w/cpp/execution.html | `std::execution` lifetime, schedulers, stopped channel |
| S14 | https://shape-of-code.com/2026/08/09/2026-in-the-programming-language-standards-world/ | C++26 ballot, C revision 2028 |
| S15 | Search summary citing https://theregister.com/2026/03/31/cplusplus26_approved/ | WG21 approval 2026-03-28 |
| S16 | Search summary citing https://llvm.googlesource.com/llvm-project/+/47e4282c19f095075fda1b5ea67b021f3fa2e3dc/flang/docs/DoConcurrent.md and https://www.open-std.org/JTC1/SC22/WG5/6494 | `do concurrent` locality hazard |
| S17 | Search summary citing Intel Fortran conformance pages, https://fortran-lang.discourse.group/t/do-concurrent-reduce-in-gcc/8723, https://gcc.gnu.org/pipermail/fortran/2024-September/061048.html | `reduce` support; Flang lacks coarrays |
| S18 | Search summary citing https://www.intel.com/content/www/us/en/docs/fortran-compiler/developer-guide-reference/2026-1/failed-images.html | Failed images, undefined ordering |
| S19 | Search summary citing https://arxiv.org/pdf/2408.15348 and https://sc25.supercomputing.org/proceedings/bof/bof_pages/bof178.html | OpenSHMEM 1.6, 1.7 planning |
| S20 | Search summary citing https://docs.open-mpi.org/en/main/man-openshmem/man3/shmem_quiet.3.html | Fence versus quiet |
| S21 | Search summary citing https://en.wikipedia.org/wiki/POSIX and https://standards.ieee.org/ieee/1003.1-2024_Cor_1/11920 | POSIX.1-2024 date, Cor 1 |
| S22 | https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_clocklock.html | Added in Issue 8 |
| S23 | https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/threads.h.html | POSIX mandates `<threads.h>` |
| S24 | https://en.cppreference.com/w/c/thread.html | C threads and atomics optional; C23 removals |
| S25 | https://doc.rust-lang.org/nomicon/send-and-sync.html | Send/Sync definitions, UB |
| S26 | https://doc.rust-lang.org/nomicon/races.html | No data races in safe Rust; deadlocks not prevented |
| S27 | https://crates.io/api/v1/crates/rayon, https://docs.rs/rayon/latest/rayon/ | Rayon 1.12.0; scope blocks |
| S28 | https://github.com/rayon-rs/rayon/blob/main/FAQ.md | Default thread count |
| S29 | https://crates.io/api/v1/crates/tokio | Tokio 1.54.1 |
| S30 | https://docs.rs/tokio/latest/tokio/macro.select.html | Cancellation safety, blocking |
| S31 | https://docs.python.org/3.14/whatsnew/3.14.html | 3.14 free threading, start method, context flags |
| S32 | https://peps.python.org/pep-0779/ | PEP 779 phases and criteria |
| S33 | https://docs.python.org/3.15/howto/free-threading-python.html | GIL re-enabling, iterators, limitations |
| S34 | https://docs.python.org/3.15/library/threadsafety.html | Built-in type atomicity |
| S35 | https://www.python.org/downloads/ | Python release dates |
| S36 | https://docs.python.org/3/library/asyncio-task.html | Weak task references, cancellation, TaskGroup |
| S37 | Search summary citing https://byteiota.com/python-3-15-rc2-ships-what-free-threaded-python-means-for-your-code/ | PEP 803 (secondary) |
| S38 | https://docs.julialang.org/en/v1/manual/multi-threading/ | Julia hazards |
| S39 | https://chapel-lang.org/download/, https://github.com/chapel-lang/chapel/releases | Chapel 2.10.0 |
| S40 | https://hpsf.io/projects/ | HPSF project list |
| S41 | https://www.khronos.org/opencl/ | OpenCL 3.1.2 |
| S42 | https://github.com/STEllAR-GROUP/hpx/releases | HPX versions |
| S43 | https://github.com/charmplusplus/charm/releases | Charm++ versions |
| S44 | https://github.com/BerkeleyLab/upcxx/wiki | UPC++ 2025.10.0 |
| S45 | https://arxiv.org/html/2312.15640v2 | DOE/NSF 2023 correctness report |
| S46 | https://arxiv.org/abs/1705.07478 | HPC Correctness Summit 2017 |
| S47 | Search summary citing WG23 drafts at https://www.open-std.org/JTC1/SC22/WG23/docs/ | ISO/IEC 24772-1 concurrency entries |
| S48 | Search summary citing https://ldra.com/ldra-blog/misra-c2012-amendment-4/ and https://www.mathworks.com/help/bugfinder/misra-c-2025-reference.html | MISRA concurrency rules |
| S49 | Search summary citing https://bssw.io/items/introducing-the-consortium-for-the-advancement-of-scientific-software-cass | CASS as ECP successor |
| S50 | Local: research/parallel-models.md (accessed 2026-10-22) | MPI, OpenMP, CUDA, HIP 7.0, xSDK and E4S background |

S9 is intentionally unused.
