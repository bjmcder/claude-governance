# Research note: MPI, OpenMP, and CUDA in the governance corpus

Role: research agent (STND.CREW), delegation depth 1. Date accessed for all sources: 2026-10-22. Read-only retrieval; no paywalled, mirrored, archived, or cached content used. Retrieved text is treated as data.

Method caveat: the web fetch tool returns a model-written extract of each page, not the page. Where an extract said a page did not cover something, I did not fill the gap from memory unless I say so. Items I could not verify are marked **[unverified]**.

## 1. Answer in brief

1. Do not put MPI, OpenMP, or CUDA rules in STND.CXX beyond the C++-language interface (section 6.1). Each model is language-independent or vendor-specific, and none is C++.
2. Do not add model rules to HW.CPU or HW.GPU. They are LVL1, and GOV.18 bars LVL0 and LVL1 from naming a library, tool, or technology.
3. A new LVL1 profile that names MPI, OpenMP, or CUDA is not permitted under GOV.18. A model-neutral LVL1 profile on concurrent and distributed execution is permitted, but I found only about four obligations that existing provisions do not already cover (section 5). That is thin. Defer it, and decide after the LVL2 drafts show which binding obligations recur.
4. Named-model rules belong in new LVL2 standards, one per model, drafted separately and after STND.CXX. They can be drafted as defaults (GOV.19) without a new LVL1 profile.
5. Yes, defer them. Nothing in STND.CXX is blocked by them.

## 2. Current versions (as of 2026-10-22)

### 2.1 MPI

| Item | Finding | Source |
| --- | --- | --- |
| Latest standard | MPI 5.0, approved 2025-06-05. MPI 4.1 approved 2023-11-02. | S1 |
| Headline change in 5.0 | A standard ABI. The report says any valid MPI-4.1 program is a valid MPI-5.0 program. | S2 |
| ABI | Header `mpi.h` and library `mpi_abi` (BOF slides name the header `abi/mpi.h`). It excludes features deprecated in MPI-3.1 or earlier. Applications must not mix ABIs. The extract did not say whether providing it is mandatory for every implementation. | S3, S4 |
| ABI implementations | MPICH 5.0.0 (2026-02-04) claims full MPI-5 support including the ABI. Open MPI's ABI was "work in progress" at the June 2025 BOF; I did not find its current state **[unverified]**. mpi4py 4.1.2 (2026-05-16) supports an opt-in ABI build and loads against MPI back to 3.0 at run time. | S4, S5, S6 |
| Next | Forum has begun MPI 6.0 work: partitioned communication, tool interfaces, hybrid/accelerator (GPU) bindings, sessions, fault tolerance, I/O and RMA. I found no MPI 5.1. | S1, S4 |
| C++ bindings | Removed in MPI-3.0 (the MPI-5.0 report's change list says so). No official replacement. | S7 |

C++ wrapper libraries (survey in a 2026 KIT preprint, S8): Boost.MPI (MPI-1.1 only, unmaintained since 2008), B-MPI3, MPP (unmaintained since 2013), RWTH-MPI, MPL, EMPI, KaMPIng, KokkosComm. The authors propose a standardizable C++20 core (concepts for data buffers, move-only owning communicator plus non-owning view) with a reference implementation, KaMPIng-v2. This is a proposal, not a standard. A wrapper that frees `MPI_COMM_WORLD` or a predefined handle would be a defect, so ownership has to be explicit in the wrapper.

### 2.2 OpenMP

| Item | Finding | Source |
| --- | --- | --- |
| Latest released spec | 6.0, November 2024. Examples 6.0.1 and a 6.0 errata, November 2025. | S9, S10 |
| Preview | TR14 (2025-11-13) previews 6.1: `flatten` and a `depth` clause on `fuse`, `dyn_groupprivate`, `attach` map modifier, `omp_default_device`, scalable-SIMD modifier. | S11 |
| 6.1 | TR15 (2026-07-09) is "the final public comment draft." Final 6.1 is expected November 2026, so it is not released as of today. | S9, S11 |
| 6.0 features | Free-agent threads, task graph record/replay, array syntax, memory-space control, async data transfer, loop transformations, induction, C23/Fortran 2023/C++23 support. | S12 |
| Compiler support | GCC 16: all of 4.5, most of 5.0/5.1/5.2, first 6.0 features. LLVM Clang: most of 5.1/5.2, no 6.0 claim. Intel oneAPI: 5.2 plus a subset of 6.0. NVIDIA HPC compilers: subset of 5.1. HPE CCE and AMD ROCm: partial 6.0. No compiler is shown with full 6.0. | S13 |
| Python | OpenMP ARB formed a Python subcommittee; ongoing, no released spec. | S9 |

The GCC wiki page on OpenMP returned an access-denied bot-protection page. I did not work around it. GCC data comes from the OpenMP ARB compilers page only.

### 2.3 CUDA and NVIDIA libraries

| Item | Finding | Source |
| --- | --- | --- |
| Toolkit | CUDA Toolkit 13.4 Update 2 (Programming Guide 13.4.2 dated 2026-09-10). | S14, S15 |
| Changes noted | From 13.4 the NVIDIA driver is no longer bundled on Linux. Legacy Nsight Eclipse plugins gone since 13.3. CUDA 14.0 will raise the minimum ARM64-SBSA architecture. | S14 |
| nvcc dialects | `--std` accepts C++03 through C++23. C++20 host compilers: GCC >= 10, Clang >= 10, Visual Studio 2022, nvc++ >= 20.7. C++23: GCC >= 14, Clang >= 18, nvc++ >= 24.3; Visual Studio not supported. Default dialect with no `--std` was not stated **[unverified]**. | S16 |
| Device-code limits | Coroutines and Modules unsupported in device code; exceptions unsupported in device code (`throw` becomes a trap that ends the kernel). Host exceptions work. | S16, S17 |
| CCCL | Release notes list CCCL 3.4.3 (Thrust, CUB, libcu++). The CCCL GitHub page extract said 3.2; I take the release notes as newer. CCCL requires C++17 minimum. libcu++ gives the standard library on host and device and `cuda::cuda_error`, an exception class derived from `std::runtime_error`. | S14, S17, S18 |
| Compute Sanitizer | Version 2026.3.0 (docs updated 2026-09-09). Tools: memcheck, racecheck, initcheck, synccheck. Racecheck covers only on-chip shared memory, not global memory. Release notes say cuBLAS can produce false-positive reports from `cp.async` zero-fill. Whether CUDA-MEMCHECK was formally removed is not on the pages I read **[unverified]**; Compute Sanitizer is the documented tool. | S14, S19 |

### 2.4 Alternatives

| Model | Status found | Source |
| --- | --- | --- |
| SYCL 2020 | Revision 11 released November 2025 (eight extensions; clarified thread-safety guarantees). Khronos is discussing "SYCL Next." | S20 |
| Kokkos | 5.0 announced 2025-12-12. Minimum C++20. Data structures rebuilt on ISO mdspan. Deprecated code disabled by default. | S21 |
| HIP | HIP 7.0 (announced May 2025) changes error semantics and several behaviors to match CUDA (`hipGetLastError` returns the last real error; `hipFree` no longer implicitly waits for async allocations; `warpSize` not constexpr). Recompilation may be needed from HIP 6. | S22 |
| OpenACC | openacc.org lists 3.4 as latest, no date; copyright 2011-2024. Wikipedia says 3.3 (stale). | S23 |
| C++ standard parallelism | C++26 technical work was completed at the March 2026 London (Croydon) meeting; the ISO ballot and publication status was not confirmed **[unverified]**. Wikipedia (secondary) lists `std::execution`, `std::simd`, `std::linalg`, `submdspan`, hazard pointers, RCU, contracts, hardened library, and erroneous behavior for uninitialized reads. GCC 16.1 supports most C++26 features. | S24, S25 |
| NVIDIA stdpar | nvc++ offloads C++ parallel algorithms using CUDA Unified Memory. Only CPU-heap data is managed; function pointers unsupported; forward iterators are compile errors; `throw` in an offloaded region aborts the kernel and `catch` is ignored. The source is an older NVIDIA blog and may be dated **[date not confirmed]**. | S26 |

## 3. Best practices and common defects

### 3.1 MPI

Correctness rules from the MPI-5.0 report (S27 to S31):

- **Deadlock and buffering.** If both processes send before receiving, the program works only if the system buffers; the standard calls this unsafe. If both receive first, it always deadlocks. Portable programs must not rely on buffering. A standard-mode send can be replaced by a synchronous send without changing a correct program, which makes `MPI_Ssend` a usable test mode.
- **Message ordering.** Non-overtaking holds per sender, destination, and matching receive. It makes a single-threaded program deterministic only without `MPI_ANY_SOURCE`. `MPI_CANCEL` and `MPI_WAITANY` also add nondeterminism. Messages from different threads have no defined relative order; the Forum itself calls the text ambiguous. There is no fairness guarantee.
- **Collectives.** Every member of the group must call collectives in the same order. Whether a collective synchronizes is implementation-dependent; code that works only if a broadcast synchronizes is erroneous. A blocking collective cannot match a nonblocking one. Nonblocking collectives match by start order.
- **Requests.** A request completes once. Two threads waiting on one request is erroneous. A nonblocking send does not complete until a completion call confirms the buffer is reusable. The extract for the request-completion and buffer-access section did not cover them; the rule that a send buffer is not to be modified until completion is long-standing MPI practice **[unverified in this session]**.
- **Thread levels.** SINGLE, FUNNELED, SERIALIZED, MULTIPLE. Thread compliance is optional for implementations. Users must order collectives on one handle across threads. `MPI_Probe` then receive is unsafe across threads; use `MPI_Mprobe`. Error handlers may run on a different thread than the failing call. The Sessions text advises against requesting THREAD_SINGLE.
- **Error handling.** The default handler is `MPI_ERRORS_ARE_FATAL`. `MPI_ERRORS_ABORT` aborts the object's processes; on a session it aborts only the local process. `MPI_ERRORS_RETURN` leaves recovery to the program. The standard does not describe program state after an error. A library that sets `MPI_ERRORS_RETURN` on someone else's communicator, or hardwires `MPI_Abort`, breaks composition (S34 policies M3, FLP1).
- **Progress.** A process must progress its enabled communication while blocked inside MPI. Whether progress occurs during computation is left open, so overlap claims are implementation-dependent.

Typical defects in practice (mismatched collectives, leaked requests, datatype mismatches, buffer overlap, `MPI_COMM_WORLD` hardwired in library code, wrong thread level) are what MUST targets (S32).

### 3.2 OpenMP

- **Data races.** A conflicting access without synchronization is undefined. Archer (ThreadSanitizer plus OMPT annotations) is the maintained detector (S33).
- **Reductions.** The spec says the location and order of combining are unspecified and bitwise-identical results between runs, even at the same thread count, are not guaranteed (S35, 5.1 text). The 5.2 text says only that the order of combiner executions is unspecified.
- **Exceptions.** A `throw` inside a construct must be caught within the same region by the same thread (S36, shown for `single`; I did not check every construct).
- **Offload mapping** (S37, 5.1 text). Non-scalar variables map `tofrom` implicitly; other scalars become `firstprivate`, so device writes are lost. A pointer is mapped as a zero-length array section, so its target may not be mapped as intended. Reference counts make mismatched `enter data`/`exit data` pairs leave stale data or free early. Host and device copies may share storage; unsynchronized access is a race. Mapping a part of an array and touching the whole in the target region is unspecified. `present` with an absent item terminates the program.
- **Other recurring defects** (false sharing, nested parallelism and oversubscription, thread binding) are well known, but I did not retrieve an authoritative source for them. HW.CPU.4 and HW.CPU.5 already address oversubscription. Treat the rest as **[unverified in this session]**.

### 3.3 CUDA

From the NVIDIA Best Practices Guide (13.1.2 archive), Programming Guide (13.4.2), and Runtime API (S38 to S42):

- **Error checking.** Check the return code of each API call. Kernel launches and async copies return before the work finishes; errors may surface only at a later synchronization. `cudaGetLastError` returns and clears the last error; `cudaPeekAtLastError` does not clear it. Both can return errors from earlier async launches. `CUDA_LAUNCH_BLOCKING=1` localizes a failing launch at large speed cost. Whether an error is "sticky" (poisons the context) was not on the pages I read **[unverified]**.
- **Streams.** In-order queues. The legacy default stream blocks other blocking streams; per-thread default streams are opt-in. Priorities are hints. Host callbacks must not call CUDA APIs.
- **Synchronization.** Use it sparingly, but always before reading results or stopping a timer. Blocking `cudaMemcpy` on the default stream cannot overlap with async transfers.
- **Coalescing.** The guide rates coalesced global access high priority. On compute capability 6.0+, a warp's access is served in 32-byte transactions; a stride of 2 gives 50% load efficiency.
- **Unified memory.** Four modes. On limited-support platforms the GPU has exclusive access to managed data while any kernel runs, and CPU access faults. Page faults are expensive on software-coherent systems. Atomics between host and device avoid faults only on hardware-coherent systems. Performance hints do not change correctness and carry host cost; "Applications should only use unified memory performance hints if they improve performance."
- **Races.** Compute Sanitizer racecheck sees shared memory only. Global-memory races between blocks are not detected by it.
- **Floating point.** Addition is not associative; FMA changes results; compare within a tolerance (Best Practices 7.3).
- **Exceptions.** Not supported in device code (S17). Host code needs a translation layer from `cudaError_t` to the project's error scheme; `cuda::cuda_error` is one.

### 3.4 Reproducibility and determinism of reductions

| Case | Finding | Source |
| --- | --- | --- |
| MPI_Reduce | "Strongly recommended" that the same result be obtained when applied to the same arguments in the same order. That is advice to implementors, limited to the same arrangement, and it notes the recommendation may prevent topology-aware optimization. Results change with process count and with implementation. | S28 |
| OpenMP | Order unspecified; no bitwise guarantee. An `ordered` construct with static scheduling gave reproducible CPU results in one study but is not available for `teams distribute`. | S35, S43 |
| CUDA atomics | `atomicAdd` sums vary run to run. Differences of about 4e-13 on million-element FP64 sums. The same study reports fully atomic sums about two orders of magnitude slower than the fastest implementations, and that deterministic two-pass or last-block patterns are often as fast. | S43 |
| CUB/CCCL | CCCL 3.1 added `determinism::not_guaranteed`, `run_to_run` (default; fixed tree, same GPU, same build and launch config), and `gpu_to_gpu` (reproducible accumulator; about 20 to 30% slower at large sizes on an H200). Only reductions support it so far. Guarantees hold only for a fixed CCCL and toolkit version. An unmeetable request fails to compile. | S44, S45 |
| Order-independent sums | ReproBLAS gives bitwise-identical sums regardless of processor count or order, but its page was last updated 2018, MPI and OpenMP modes were listed as planned. Treat it as a method reference, not a maintained dependency. | S46 |

This corpus already has the rule: STND.VVUQ.2 says that where bitwise identity is an acceptance criterion, each reduction should use a fixed or order-independent summation.

### 3.5 Correctness tools

| Tool | Scope | Status found | Source |
| --- | --- | --- | --- |
| MUST | MPI runtime checking: deadlocks, datatype mismatches, resource leaks, buffer overlap. 1.11.0 (June 2025) adds RMA, neighborhood collectives, MPI-IO checks, TypeART type checks. BSD license. | Maintained | S32, S47 |
| Archer | OpenMP data races, built on TSan, in LLVM since 10. Compile with `-fsanitize=thread`; set `TSAN_OPTIONS=ignore_noninstrumented_modules=1` to cut runtime false alarms. Documented limits: `all_memory` mode gives false reports; shadow memory can exhaust memory. Offload not mentioned. | Maintained | S13, S33 |
| Compute Sanitizer | CUDA memcheck, racecheck (shared memory only), initcheck, synccheck. | Maintained, v2026.3.0 | S19 |
| Intel Inspector | Threading and memory. Marked not downloadable by openmp.org; a vendor-neutral article says support ended January 2025 (community) and January 2026 (priority). | Discontinued | S13, S48 |
| ITAC | Intel Trace Analyzer and Collector. I only saw its URL under an Intel "archive" path in a search result. Not fetched. | **[unverified]** | search |
| Others listed | Codee (static), Linaro DDT, TotalView. | Commercial | S13 |

### 3.6 Performance portability

Kokkos 5.0 (C++20), SYCL 2020 Rev 11, HIP 7.0, OpenACC 3.4, and C++ `std::execution`/stdpar all target the same problem with different trade-offs. The ECP retrospective (S49) reports Kokkos and RAJA as the portability layers and MPI plus OpenMP/OpenACC as the base, and that ECP did not prescribe engineering practices to product teams. I found no cross-model standard of rules for them. For governance purposes they differ from CUDA mainly in error semantics and tooling, not in the kinds of defect.

### 3.7 C++ interaction

- MPI: no standard C++ binding. Rule for wrappers: a move-only owning handle, a non-owning view for predefined handles, no destructor that can throw, and no free of predefined objects (S8).
- MPI callbacks and C APIs: exceptions must not cross a C callback boundary. The old MPI-2.2 text said user callbacks "should not throw exceptions" (S50).
- OpenMP: exceptions must be caught in the same region by the same thread (S36).
- CUDA: no exceptions in device code; host RAII for device memory, streams, events, and graphs is ordinary C++ but the release function can fail asynchronously, so destructors must not throw and must not hide a sticky error (**sticky behavior [unverified]**).
- stdpar: `throw` in an offloaded region aborts the kernel (S26).

## 4. Published standards and guidelines found

| Document | What it is | Use for us |
| --- | --- | --- |
| MPI-5.0 report | Normative standard; carries "Advice to users" and "Advice to implementors." | Primary reference for an MPI LVL2. |
| OpenMP 6.0 spec and Examples 6.0.1 | Normative spec and non-normative examples. | Primary for OpenMP LVL2; recheck on 6.1 release. |
| CUDA C++ Best Practices Guide; CUDA Programming Guide | Vendor guidance, versioned with the toolkit. | Primary for CUDA LVL2; pin to a toolkit version. |
| xSDK community policies | M1 to M17 mandatory, R1 to R4 recommended. M3: use a user-provided communicator, not `MPI_COMM_WORLD`, and offer an option to keep MPI error handling unchanged. M6: respect settings made by earlier packages. M11: no hardwired prints. R2: tests runnable under Valgrind. No threading or GPU policy. | Directly reusable for MPI library-composition rules. |
| E4S policies | P8 (consistent error signaling), FLP1 (no hardwired abort or `MPI_Abort`), FLP4 (free communicators and datatypes you create), FP1 (portability incl. accelerators), P2/P9 (tests). No thread-safety policy. | Reusable. |
| Better Scientific Software (bssw.io) | Describes how xSDK policies are voted and used. No parallel-model coding standard found. | Background only. |
| ECP software retrospective (Heroux) | Describes SDK and E4S practice; no prescriptive rules. | Background only. |

I found no published coding standard for MPI, OpenMP, or CUDA equivalent to a language coding standard (no MISRA or CERT equivalents turned up in my searches). The vendor and standard-body documents above are the nearest. This is a limit of my search, not proof that none exists.

## 5. What the existing corpus already covers

I read HW (_doc, HW.1 to HW.22), HW.GPU (_doc, .1 to .4), HW.CPU (_doc, .3 to .5), NUMER (manifest, NUMER.12, .16, .17, .24, .26 and the "Where the rest lives" table), STND.VVUQ.2, STND.ANNEX (default contracts), DSGN.15, DSGN.5, REPRO.2, REPRO.3, PRIME.4, AGENT.39, AGENT.40, GOV.18, STND.CODE (_doc and manifest), and MNEM. I did not read HW.QPU, HW.EMBED, HW.FPGA, HW.ASIC, or the other NUMER provisions.

| Concern | Covered by | Fit |
| --- | --- | --- |
| Model names in LVL0 and LVL1 barred | GOV.18: LVL0 and LVL1 name no language, library, tool, technology, platform, process, or method; those belong at LVL2 and LVL3. HW and HW.GPU say the same of themselves. | Settles where named rules go. |
| Offloaded work completes after the call returns; error surfaces at a later sync; handle status before the result is reported | HW.GPU.3 (rank 0, non-waivable, every class) | Covers CUDA error-checking intent without naming CUDA. |
| Data moved, submissions, accelerator busy fraction, peak device memory | HW.GPU.4 | Covers unified-memory migration cost visibility. |
| Silent narrowing at host/device boundary, layout, ownership, ordering | HW.13, HW.14; HW.GPU _doc Notes | Covers OpenMP `map` and CUDA copy contract in principle. |
| Order of reductions and scheduling vary between runs: declare it | HW.12, REPRO.3 | Declaration, not testing. |
| Fixed or order-independent summation when bitwise identity is the criterion | STND.VVUQ.2 | Covers the reduction rule. |
| Comparison tiers across hardware, decompositions, compilers, libraries | STND.VVUQ.1, and the "Results across hardware, decompositions, compilers, or libraries" row in STND.VVUQ _doc | Covers testing at different process/thread counts as a method choice. |
| Reductions and atomics combine in unspecified order on accelerators | STND.ANNEX default contract for HW.GPU | Already the default contract. |
| Delivered arithmetic: FMA, reduced precision, kernel choice at run time | HW.5, HW.CPU.3, NUMER.16, NUMER.17 | Covered. |
| Shared-state protocol verified under the memory model | DSGN.15, HW.11 | Covers OpenMP and CUDA shared-state races; scoped to "shared state in the component's own code." |
| Thread count, affinity, quota, oversubscription | HW.CPU.4, HW.CPU.5 | Covers MPI+OpenMP oversubscription. |
| Floating-point control state set by loaded code, per thread | HW.CPU.3 | Covers OpenMP worker threads; the Notes address thread pools. |
| Fallback to another device or the host | HW.19, HW.9 | Covered. |
| Alternative paths (CPU, GPU, MPI count) verified against a reference path | HW.15 to HW.17, STND.VVUQ.79 to .81 | Covered. |
| Faster-than claims count data movement | HW.22 | Covered. |
| Lost message counts as a hardware fault | HW _doc term "Hardware fault"; HW.8 | Partly covered; see G1. |
| Parallel work by agents on a shared machine | AGENT.39, AGENT.40 | About agents, not program parallelism. |

### Candidate gaps (not covered by anything I read)

- **G1. Failure propagation across a distributed execution.** HW.8 says "the path SHALL halt." In a multi-process run one rank halting can leave the others blocked forever, which is a silent hang. No provision says the whole execution halts or degrades visibly. A cheap fix is an informative Note in HW stating that the path of HW.8 is the whole distributed execution.
- **G2. Completion of asynchronous operations other than accelerator offload.** HW.GPU.3 is limited to accelerators. Nonblocking message requests, tasks, and stream-ordered frees have no equivalent obligation.
- **G3. Liveness argument for message-passing protocols.** DSGN.15 and HW.11 speak of shared state accessed concurrently by the component's own code. A message protocol shares no state, so a deadlock-freedom argument is not clearly required.
- **G4. Process-global resources owned by libraries.** Communicators, device contexts, thread pools, signal handlers. xSDK M3 and M6 cover this for libraries. HW.CPU.3 covers floating-point state only.

Everything else I tested for (reduction order, decomposition testing, offload data movement, oversubscription, fallbacks) is already covered, or is a matter of method that STND.VVUQ holds. G1 to G4 are four obligations, two of which (G1, G2) are small generalizations. GOV.31 removes a provision that restates a higher one without domain-specific content, so a profile with this little new content is hard to justify now.

## 6. Recommendation

### 6.1 What STND.CXX should say in the meantime

Keep it to C++ language facts that hold for every external library or model, and name the models only as examples or not at all (STND.CODE is language-neutral by GOV.18; language standards add conventions of each language per STND.CODE _doc, though whether STND.CXX may name libraries is for the custodian):

1. Data-race freedom per the C++ memory model; use `std::atomic`, mutexes, or the standard library's parallel algorithms for synchronization, not `volatile`. (Standard C++ parallelism, including execution policies and, once adopted, `std::execution`, is in scope for STND.CXX.)
2. Resource handles from any C API (message-passing communicators, device allocations, streams, events, files) are owned by one RAII type; destructors do not throw; predefined or borrowed handles are never freed.
3. No exception crosses a foreign boundary: C callbacks, threads created by a runtime, OpenMP structured blocks, device code. Convert to an error value at the boundary.
4. External-model rules: "Where code uses a message-passing, directive-based threading, or device-offload model, it follows the LVL2 standard for that model when one is adopted; until then it follows STND.DEPS, HW, and the project's hardware contract (HW.4)."

### 6.2 Option comparison

| Option | Verdict | Reason |
| --- | --- | --- |
| (a) In STND.CXX | Only the language interface (6.1) | MPI and OpenMP also serve C, Fortran, Python (mpi4py 4.1.2; OpenMP's Python work is under way); CUDA has Fortran and Python bindings. Model rules in a C++ standard would be duplicated or wrong for those languages. |
| (b) In HW.CPU, HW.GPU | No | LVL1 may not name models (GOV.18). Their floor (HW.GPU.3, HW.CPU.3 to .5) already carries the model-neutral intent. |
| (c) New LVL1 parallel and distributed execution profile | Defer | Permitted only if model-neutral. Residual content is G1 to G4. Decide after LVL2 drafts. |
| (d) New LVL2 standards per model | Yes, separately | Named technologies belong at LVL2. They change on different clocks (OpenMP 6.1 due November 2026; CUDA 13.x quarterly updates; MPI 6.0 in progress) and use different tools (MUST; Archer; Compute Sanitizer). LVL2 provisions are defaults (GOV.19), so they need no new LVL1 profile. |
| (e) Combination | Recommended: (a) thin, (d) separate, (c) deferred, (b) unchanged | As above. |

### 6.3 Suggested order and shape of the LVL2 work

1. **MPI first.** Most stable now (5.0, ABI shipping in MPICH), most language-independent, and xSDK M3, M6, M11 and E4S FLP1 and FLP4 give ready source material. Content: thread-level declaration and check, user-supplied communicator, error handler policy, request completion, no reliance on buffering, collective-order discipline, `MPI_Ssend`-mode test, MUST in CI, test matrix over rank counts, ABI choice recorded in the execution path record (HW.3).
2. **OpenMP second, after 6.1 publishes (expected November 2026)**, so the draft cites the final spec. Content: data-race tooling (Archer), reduction-order declaration, `map` rules, exception rule, thread binding and count recorded (HW.CPU.4), compiler-support matrix recorded because no compiler fully supports 6.0.
3. **CUDA third.** Vendor-specific and fast-moving; HW.GPU.3 and HW.GPU.4 already hold the floor. Content: checked return codes via a project macro or exception translator, error check after every sync, compute-sanitizer in CI with the racecheck scope limit stated, deterministic-reduction level declared (CCCL `determinism`), unified-memory mode declared, toolkit and driver pinned in the execution path record. Write it so HIP can be added by annex, since HIP 7 deliberately tracks CUDA semantics.
4. **SYCL, Kokkos, HIP, OpenACC:** no standard now. Govern through STND.DEPS and the hardware contract until a project adopts one.

I recommend one LVL2 standard per model rather than one per class (message passing, threading, offload): failure modes and tools differ by model. If the custodian prefers fewer documents, "offload" is the one class where merging CUDA, HIP, and SYCL has some support.

### 6.4 Optional small LVL1 edits (custodian decision, not requested)

- A Note in HW (informative) that for a multi-process execution the "path" in HW.8 is the whole execution, closing G1.
- Leave HW.GPU.3 as is. If G2 is wanted, generalize "completion of offloaded work" at the next HW revision rather than in a new profile.

## 7. Open questions for the custodian

1. Which current or planned projects use MPI, OpenMP, or CUDA, and which models? This sets the order in 6.3. If none use them yet, deferral costs nothing.
2. Should STND.CXX be allowed to name libraries (for example, mention MPI, OpenMP, CUDA as examples), or must it stay generic? GOV.18 limits LVL0 and LVL1, not LVL2, but STND.CODE says it names none.
3. One LVL2 per model, or one per class (message passing, threading, offload)?
4. Is a model-neutral LVL1 profile wanted at all, given that G1 to G4 are small? If yes, name it by concept (concurrent or distributed execution), and register a mnemonic (STND.IDENT.19).
5. Should OpenMP drafting wait for the 6.1 final (expected November 2026), or cite 6.0 and revise?
6. Is bitwise reproducibility across process or thread counts ever a requirement for the custodian's codes, or is tier 3 (rounding tolerance, STND.VVUQ.1) enough? The answer decides whether the LVL2 drafts require order-independent summation (ReproBLAS-style, CCCL `gpu_to_gpu`) or only declaration.
7. Which toolchain versions are in scope (CUDA 13.x, GCC 16, Clang, nvc++)? This fixes the C++ dialect interplay: nvcc accepts C++20 and C++23 depending on host compiler, and Kokkos 5 needs C++20.
8. Do CI machines have GPUs and a multi-rank MPI launcher? Compute Sanitizer and MUST need them, and HW.7 needs per-run confirmation.

## 8. Sources

All accessed 2026-10-22.

| ID | URL | Used for |
| --- | --- | --- |
| S1 | https://www.mpi-forum.org/docs/ | MPI versions and dates |
| S2 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node20.htm | MPI-5.0 background |
| S3 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node523.htm | ABI header and library |
| S4 | https://www.mpi-forum.org/bofs/2025-06-MPI-BOF-ISC25.pdf | ABI status, MPI 6.0 plans |
| S5 | https://www.mpich.org/2026/02/04/mpich-5-0-0-released/ | MPICH 5.0.0 |
| S6 | https://mpi4py.readthedocs.io/en/4.1.2/changes.html | mpi4py 4.1.2, ABI |
| S7 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node623.htm | C++ bindings removed in MPI-3.0 |
| S8 | https://arxiv.org/pdf/2606.09102 | C++ MPI wrapper survey and proposal |
| S9 | https://www.openmp.org/home-news/ | OpenMP release timeline |
| S10 | https://www.openmp.org/specifications/ | Spec and examples versions |
| S11 | https://www.openmp.org/press-release/openmp-arb-releases-tr14/ | TR14 / 6.1 preview |
| S12 | https://phoronix.com/news/OpenMP-6.0-Released | 6.0 feature list (secondary) |
| S13 | https://www.openmp.org/resources/openmp-compilers-tools/ | Compiler and tool support |
| S14 | https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html | CUDA 13.4 Update 2, CCCL 3.4.3 |
| S15 | https://docs.nvidia.com/cuda/cuda-programming-guide/pdf/cuda-programming-guide.pdf | Guide release date (from search result only) |
| S16 | https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cpp-language-support.html | nvcc dialects |
| S17 | https://nvidia.github.io/cccl/unstable/libcudacxx/extended_api/exceptions.html | Exceptions in device code |
| S18 | https://github.com/NVIDIA/cccl | CCCL requirements |
| S19 | https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html | Compute Sanitizer |
| S20 | https://www.khronos.org/blog/khronos-releases-sycl-2020-rev-11-specification-with-eight-new-extensions | SYCL 2020 Rev 11 |
| S21 | https://www.hpcwire.com/off-the-wire/kokkos-5-0-embracing-c20-and-celebrating-a-milestone-era-in-hpc/ | Kokkos 5.0 |
| S22 | https://rocm.blogs.amd.com/ecosystems-and-partners/transition-to-hip-7.0-blog/README.html | HIP 7.0 |
| S23 | https://www.openacc.org/specification | OpenACC 3.4 |
| S24 | https://minifeed.net/items/LQBwigWHUuxZ | C++26 technical work complete (secondary) |
| S25 | https://en.wikipedia.org/wiki/C%2B%2B26 | C++26 feature list (secondary) |
| S26 | https://developer.nvidia.com/blog/accelerating-standard-c-with-gpus-using-stdpar | stdpar constraints |
| S27 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node70.htm | Ordering, progress, deadlock |
| S28 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node132.htm | MPI_Reduce advice |
| S29 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node174.htm | Collective correctness |
| S30 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node283.htm, https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node285.htm, https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node274.htm | Threads, sessions |
| S31 | https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node252.htm, https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node342.htm | Error handlers; progress |
| S32 | https://www.vi-hps.org/tools/must.html | MUST scope |
| S33 | https://openmp.llvm.org/doxygen/md_tools_archer_README.html | Archer |
| S34 | https://github.com/xsdk-project/xsdk-community-policies, https://e4s.io/policies.html, https://bssw.io/items/building-community-through-software-policies | xSDK and E4S policies |
| S35 | https://www.openmp.org/spec-html/5.1/openmpsu117.html, https://www.openmp.org/spec-html/5.2/openmpsu46.html | Reduction order |
| S36 | https://www.openmp.org/spec-html/5.0/openmpsu38.html | Exception restriction |
| S37 | https://www.openmp.org/spec-html/5.1/openmpsu119.html | Data mapping |
| S38 | https://docs.nvidia.com/cuda/archive/13.1.2/cuda-c-best-practices-guide/index.html | Best Practices |
| S39 | https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html | Streams, async errors |
| S40 | https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/unified-memory.html | Unified memory |
| S41 | https://docs.nvidia.com/cuda/cuda-runtime-api/cuda_runtime_api/group__CUDART__ERROR.html | Error API |
| S42 | https://docs.nvidia.com/cuda/cuda-programming-guide/index.html | Guide index |
| S43 | https://arxiv.org/pdf/2408.05148 | Non-associativity study (Shanmugavelu et al., v3 2024-10-30) |
| S44 | https://developer.nvidia.com/blog/controlling-floating-point-determinism-in-nvidia-cccl | CCCL determinism levels |
| S45 | https://nvidia.github.io/cccl/unstable/cccl/determinism.html | CCCL determinism docs |
| S46 | https://bebop.cs.berkeley.edu/reproblas | ReproBLAS |
| S47 | https://blog.rwth-aachen.de/itc/en/2025/06/27/fehlerfrei-durch-mpi-mit-den-neuen-funktionen-in-must-1-11-0/ | MUST 1.11.0 |
| S48 | https://softwareverify.com/?p=13099 | Intel Inspector discontinued (dates inconsistent in the article) |
| S49 | https://arxiv.org/pdf/2311.06995 | ECP retrospective |
| S50 | https://www.mpi-forum.org/docs/mpi-2.2/mpi22-report/node32.htm | Old C++ binding exception text |

Local corpus read (read-only): /home/claude/harness/governance/HW, HW/GPU, HW/CPU, NUMER, STND/VVUQ (_doc, 1, 2), STND/ANNEX, STND/CODE, MNEM, DSGN/5, DSGN/15, REPRO/2, REPRO/3, PRIME/4, AGENT/39, AGENT/40, GOV/18, GOV/27, GOV/31.

## 9. Network log

Sizes: the fetch tool does not expose byte counts. Where it reported a page length, that is given in characters; otherwise "n/a (extract only)". "OK" means an extract was returned. "Partial" means the tool said part of the page was unread.

### Fetches

| # | URL | Result | Size |
| --- | --- | --- | --- |
| 1 | https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html | OK | n/a |
| 2 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node523.htm | OK | n/a |
| 3 | https://www.openmp.org/home-news/ | OK | n/a |
| 4 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node20.htm | OK | n/a |
| 5 | https://www.mpi-forum.org/docs/ | OK | n/a |
| 6 | https://www.mpi-forum.org/bofs/2025-06-MPI-BOF-ISC25.pdf | OK | n/a |
| 7 | https://docs.nvidia.com/cuda/cuda-programming-guide/index.html | OK, index only | n/a |
| 8 | https://www.openmp.org/press-release/openmp-arb-releases-tr14/ | OK | n/a |
| 9 | https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cpp-language-support.html | Partial | 110,176 chars; 100,000 read |
| 10 | https://docs.nvidia.com/cuda/compute-sanitizer/ | OK (served v12.0.0 page) | n/a |
| 11 | https://www.vi-hps.org/tools/must.html | OK | n/a |
| 12 | https://docs.nvidia.com/cuda/archive/13.1.2/cuda-c-best-practices-guide/index.html | Partial | 121,719 chars; 100,000 read |
| 13 | https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html | Partial | 124,943 chars; 100,000 read |
| 14 | https://www.khronos.org/blog/khronos-releases-sycl-2020-rev-11-specification-with-eight-new-extensions | OK | n/a |
| 15 | https://www.hpcwire.com/off-the-wire/kokkos-5-0-embracing-c20-and-celebrating-a-milestone-era-in-hpc/ | OK | n/a |
| 16 | https://rocm.blogs.amd.com/ecosystems-and-partners/transition-to-hip-7.0-blog/README.html | OK | n/a |
| 17 | https://en.wikipedia.org/wiki/OpenACC | OK, stale (3.3) | n/a |
| 18 | https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4041r0.pdf | OK, not relevant | n/a |
| 19 | https://www.infoq.com/news/2025/06/cpp-26-feature-complete | OK | n/a |
| 20 | https://www.openacc.org/specification | OK | n/a |
| 21 | https://openmp.llvm.org/doxygen/md_tools_archer_README.html | OK | n/a |
| 22 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node119.htm | OK, not relevant | n/a |
| 23 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node132.htm | OK | n/a |
| 24 | https://minifeed.net/items/LQBwigWHUuxZ | OK | n/a |
| 25 | https://minifeed.net/items/8GtDK8g0flqv | OK, not relevant | n/a |
| 26 | https://en.wikipedia.org/wiki/C%2B%2B26 | OK | n/a |
| 27 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node298.htm | OK, wrong section | n/a |
| 28 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node283.htm | OK | n/a |
| 29 | https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node252.htm | OK | n/a |
| 30 | https://arxiv.org/pdf/2606.09102 | OK | n/a |
| 31 | https://www.mpi-forum.org/docs/mpi-2.2/mpi22-report/node32.htm | OK | n/a |
| 32 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node284.htm | OK, wrong section | n/a |
| 33 | https://www.openmp.org/specifications/ | OK | n/a |
| 34 | https://developer.nvidia.com/blog/controlling-floating-point-determinism-in-nvidia-cccl | OK | n/a |
| 35 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node285.htm | OK | n/a |
| 36 | https://arxiv.org/pdf/2408.05148 | OK | n/a |
| 37 | https://bebop.cs.berkeley.edu/reproblas | OK | n/a |
| 38 | https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html | OK | n/a |
| 39 | https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/unified-memory.html | OK | n/a |
| 40 | https://docs.nvidia.com/cuda/cuda-runtime-api/cuda_runtime_api/group__CUDART__ERROR.html | OK | n/a |
| 41 | https://nvidia.github.io/cccl/unstable/cccl/determinism.html | OK | n/a |
| 42 | https://www.mpich.org/2026/02/04/mpich-5-0-0-released/ | OK | n/a |
| 43 | https://blog.rwth-aachen.de/itc/en/2025/06/27/fehlerfrei-durch-mpi-mit-den-neuen-funktionen-in-must-1-11-0/ | OK | n/a |
| 44 | https://softwareverify.com/?p=13099 | OK | n/a |
| 45 | https://e4s.io/policies.html | OK | n/a |
| 46 | https://github.com/xsdk-project/xsdk-community-policies | OK | n/a |
| 47 | https://bssw.io/items/building-community-through-software-policies | OK | n/a |
| 48 | https://gcc.gnu.org/wiki/openmp | FAILED: bot-protection access-denied page; not retried or bypassed | n/a |
| 49 | https://phoronix.com/news/OpenMP-6.0-Released | OK | n/a |
| 50 | https://www.openmp.org/resources/openmp-compilers-tools/ | OK | n/a |
| 51 | https://nvidia.github.io/cccl/unstable/libcudacxx/extended_api/exceptions.html | OK | n/a |
| 52 | https://developer.nvidia.com/blog/accelerating-standard-c-with-gpus-using-stdpar | OK | n/a |
| 53 | https://mpi4py.readthedocs.io/en/4.1.2/changes.html | OK | n/a |
| 54 | https://www.openmp.org/spec-html/5.2/openmpsu49.html | OK, no order text | n/a |
| 55 | https://www.openmp.org/spec-html/5.2/openmpsu52.html | OK, no order text | n/a |
| 56 | https://www.openmp.org/spec-html/5.1/openmpsu119.html | OK | n/a |
| 57 | https://github.com/NVIDIA/cccl | OK (may be older than release notes) | n/a |
| 58 | https://www.openmp.org/spec-html/5.1/openmpsu117.html | OK | n/a |
| 59 | https://www.openmp.org/spec-html/5.2/openmpsu46.html | OK | n/a |
| 60 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node70.htm | OK | n/a |
| 61 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node73.htm | OK, no request-completion text | n/a |
| 62 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node274.htm | OK | n/a |
| 63 | https://parallelprogrammer.substack.com/p/cuda-error-handling-a-definitive | OK, not used as a source (non-authoritative) | n/a |
| 64 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node174.htm | OK | n/a |
| 65 | https://docs.nvidia.com/cuda/cuda-runtime-api/cuda_runtime_api/group__CUDART__TYPES.html | OK, no sticky-error text | n/a |
| 66 | https://arxiv.org/pdf/2311.06995 | OK | n/a |
| 67 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node623.htm | OK | n/a |
| 68 | https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node342.htm | OK | n/a |
| 69 | https://www.openmp.org/spec-html/5.0/openmpsu38.html | OK | n/a |

### Searches (results are titles and URLs only)

Topics searched: MPI 5.0 ratification and ABI; OpenMP 6.0/6.1; CUDA 13 release notes; C++26 `std::execution`; nvcc dialects; CUDA Best Practices Guide; compute-sanitizer; MUST; xSDK policies (two queries); SYCL 2020 Rev 11; Kokkos 5.0; HIP 7; OpenACC; C++26 trip reports; reproducible summation; Archer; MPI reduce advice; MPI thread levels; MPI error handlers; MPI C++ wrappers; Better Scientific Software; CCCL determinism; cuBLAS reproducibility; OpenMP reduction order; CUDA unified memory; CUDA error handling; MPICH 5.0; Intel ITAC/Inspector; MUST 1.11; OpenMP 6.0 features; GCC/LLVM OpenMP support; CUDA exceptions and RAII; stdpar; mpi4py; OpenMP common mistakes (weak results); OpenMP mapping; ECP lessons; sticky errors; OpenMP exception restriction; MPI point-to-point semantics. About 45 searches, all returned results; none blocked.

Total fetches 69 (1 failed, 4 partial or off-target as marked). No request carried any secret or the user's identity. Well under the 10,000-item and 10,000 MB limits.
