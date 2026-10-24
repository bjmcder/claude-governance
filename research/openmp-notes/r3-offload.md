Role: research agent. Date accessed: 2026-10-24. Retrieval rules followed: read-only retrieval; 27 items (20 fetches including probes and failures, 7 web searches) and about 26 MB in total; no paywalls touched; blocked fetches (HTTP 403 on openmp.org HTML pages, a certificate failure on cvw.cac.cornell.edu) were not worked around and no mirrors, caches, or archives were used; retrieved text treated as data; unconfirmed items marked [unverified].

# R3: Correctness hazards and best practices of OpenMP device offload

## Method caveat

The OpenMP 5.2 and 6.0 specifications, TR15 (the 6.1 public comment draft of July 9, 2026), and the 6.0 Examples were downloaded as PDFs from openmp.org and converted to text locally, so spec citations come from the full text. Section numbers are given as "5.2 §x / 6.0 §y". TR15 renumbers many chapters (for example, map becomes §11.5). Vendor and HPC pages were read through a fetch tool that returns a model-written extract, so those findings are paraphrase. Implementation names appear only as examples of behavior a standard should not rely on.

## Answer in brief

1. Every offloaded region has a recorded expectation of where it runs, and production and test runs enforce it. The spec runs regions on the host when the device is absent or unsupported, or when `if` is false. Under the default policy this happens silently (5.2 §1.3 / 6.0 §1.2, §15.8) [S1, S2].
2. Correctness tests run at least twice: once with offload required (`mandatory`) and once host-only (`disabled`, where supported). Both must match a host reference within stated tolerances (5.2 §21.2.8 / 6.0 §4.3.9) [S1, S2, S4].
3. Every variable a target region reads or writes has an explicit data attribute. `defaultmap(none)` is a mechanically checkable way to enforce this (6.0 §7.9.9) [S2].
4. No result is read on the host before a defined synchronization: a `from` map at refcount release, `target update from`, `taskwait`, or a dependence (6.0 §7.9.6, §15.9, §17.5) [S2].
5. Each unstructured mapping has exactly one matching release on every path, including error paths. Code that relies on copy-back states the reference count it assumes (6.0 §7.9.6) [S2].
6. Pointers and structures in a region are mapped so that their targets are present and attached. Host addresses are never dereferenced on a device with separate memory (5.2 §5.8.6 / 6.0 §7.9.3, §7.9.6) [S1, S2].
7. Code that depends on `requires unified_shared_memory` or `self_maps` states so, is tested on devices without that capability, and treats "no qualifying device" as a failure rather than a silent host run (6.0 §10.5.1) [S2, S7].
8. Device floating-point results are compared to the host with tolerances, not bit equality. Reduction order is unspecified (6.0 §7.6.7), and the floating-point environment is unspecified across a target boundary (6.0 §15.8). Device math and contraction behavior differ from the host [S2, S5, S8].
9. Atomics that synchronize host and device threads state the memory scope they need. The default is the device only (6.0 §17.8.4, §17.8.5) [S2].
10. Device allocation results are checked: `omp_target_alloc` returns NULL on failure. The program defines what it does on runtime error termination. The spec says nothing about device faults (6.0 §25.3, §1.2) [S2].

## Q1. Silent host fallback

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| No device, or device unsupported | 5.2 §1.3 / 6.0 §1.2 | "all target regions associated with that device execute on the host device," with no diagnostic required | Runs that claim offload record evidence that regions ran on a device | S1, S2 |
| `if` clause false | 6.0 §15.8: acts as `device(omp_initial_device)` | Region silently runs on host; `if` on `target update` skips the copy (6.0 §15.9) | Every `if` on a device construct has a documented host path that is tested | S2 |
| Requirement not met by a device | 6.0 Glossary "supported device" includes `requires` requirements | A device without unified memory becomes unsupported and work falls back to host; one implementation removes such devices, "possibly leaving only the initial device" | Builds using `requires` verify a qualifying device at startup | S2, S7 |
| `OMP_TARGET_OFFLOAD` | 5.2 §21.2.8 / 6.0 §4.3.9; ICV init 6.0 §3 | `mandatory`: unavailable device acts as `omp_invalid_device`, giving runtime error termination (6.0 §15.2). `disabled`: host only, support implementation defined. `default`: silent fallback | Offload tests run with `mandatory`, and the reference run uses host-only execution | S1, S2, S4 |
| Detecting where code ran | 6.0 §24.9 `omp_is_initial_device`, §24.3 `omp_get_num_devices` (unspecified inside a target region, §15.8) | Calling `omp_get_num_devices` inside a region gives unspecified results | Placement is checked by calling `omp_is_initial_device` inside the region and returning the result to the host | S2 |
| Device selection | 6.0 §15.2, §3; TR15 §1.2 adds `omp_default_device` as an alias for the default-device ICV | A non-conforming device number with `mandatory` terminates; otherwise behavior depends on ICV | Device numbers come from a validated range or `omp_default_device`, never a hard-coded constant | S2, S3 |

The spec does not separately address a device that exists but fails to initialize at run time. Whether an implementation treats that as "unavailable" (and falls back) is [unverified].

## Q2. Data mapping

Confirmation of the earlier note: (a) Non-scalars are implicitly `tofrom`. Other scalars are `firstprivate`, so device writes are lost. Fortran scalars with TARGET, ALLOCATABLE, or POINTER are `tofrom`. C++ members referenced in member functions map through `this[:1]` (5.2 §5.8.1 / 6.0 §7.9.3). Confirmed. (b) Pointers: 5.2 maps them as a zero-length array section. 6.0 rewords this as "the array base of a zero-offset assumed-size array" with the `storage` map type. That attaches only if the pointee is already mapped and copies no pointee data. If no match is found, "the pointer retains its original value as per the firstprivate semantics" (5.2 §5.8.6), so the device holds a host address. Confirmed and sharpened. (c) Reference counting: confirmed (6.0 §7.9.6). A `from` copies back only when the count reaches release or with `always` or `delete`. (d) Shared storage race: confirmed (6.0 §1.3.2, §7.9.6). (e) Partial array: correction. The "smaller than the whole array, referencing the whole array is unspecified" rule is a Fortran-only restriction (5.2 §5.8.3 / 6.0 §7.9.6). In C and C++, accessing storage that is not mapped is unspecified generally (6.0 §1.3.2). An implicit map of an array already partly mapped maps only the existing part (6.0 §7.9.6). (f) `present` with an absent item: confirmed, runtime error termination (6.0 §7.9.6, §7.10).

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Implicit attributes | 6.0 §7.9.3, §7.9.9 | Lost scalar writes; whole arrays copied both ways | Every referenced variable has an explicit attribute; `defaultmap(none)` makes omissions compile errors | S2 |
| Absent item in `target update` | 6.0 §7.10 | "no assignment occurs," silently | Updates of data that must be present use the `present` modifier | S2 |
| Structures | 6.0 §15.8 restrictions | Mapping one member and referencing another is non-conforming | Either the whole structure or every referenced member is mapped | S2 |
| Pointer attachment | 6.0 §7.9.6; TR15 §11.5.5 `attach(always\|auto\|never)`, absent means `auto` | Pointer member not attached, or attached pointer modified while mapped (prohibited) | Pointee and pointer are mapped on the same construct, or attachment is explicit; attached pointers are unchanged while mapped | S2, S3 |
| `declare target enter` variables | 6.0 §7.9.7 | Device copy initialized once at an unspecified point and never removed; host and device diverge | Host-to-device consistency of global data is maintained by explicit `target update` | S2 |
| `link` variables | 6.0 §7.9.8 | Not mapped by the directive; absent unless mapped | Each `link` variable is mapped before use | S2 |
| Unstructured lifetimes | 6.0 §15.5, §15.6, §7.9.6 | Unbalanced enter/exit leaves stale data, leaks, or frees early | Enter and exit pairs are balanced on every path, verified by a runtime mapping report or a test | S2 |
| `always`, `close` | 6.0 §7.9.6 | `close` is only a hint; omitting `always` skips copies when refcount is above one | Correctness never depends on `close`; refreshes inside an outer data region use `always` or `update` | S2 |
| C++ polymorphism | 6.0 §15.8, §7.9.6 | Virtual calls on objects built on another device are unspecified; static and dynamic type mismatch on first map is unspecified | Polymorphic objects used on a device are constructed there, or mapped with matching static type, as in the Examples | S2, S4 |
| Fortran allocatables and pointers | 6.0 §7.9.6, §15.8; `automap` §7.9.7 | Allocating, deallocating, or reshaping while mapped is prohibited; pointer association must not change across a region | Allocation state of mapped Fortran objects is unchanged while mapped | S2 |
| Concurrent mapping | 6.0 §7.9.6: entry and exit steps act "as if ... a single atomic operation" | One implementation lets users disable map atomicity for speed | Configuration never weakens spec atomicity guarantees | S2, S6 |

## Q3. Unified and shared memory

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Assuming USM makes data coherent | 5.2 §8.2 / 6.0 §10.5.1.5 | "Values stored into memory by one device may not be visible to another device until synchronization" | Host and device accesses to shared data are ordered by synchronization | S1, S2 |
| Scalars under USM | 5.2 §8.2; Examples §6.7 | Scalars are still firstprivate; device writes are lost | Same explicit-attribute rule applies with or without USM | S1, S4 |
| `unified_address` only | 6.0 §10.5.1.4 | Dereferencing host pointers on device "remains unspecified behavior" | Code distinguishes unified addressing from shared access | S2 |
| `self_maps` (new in 6.0) | 6.0 §10.5.1.6, §7.9.6 | All maps become self maps; error termination if storage not accessible or already mapped elsewhere | Self-map builds are tested on target hardware | S2 |
| Implementation-defined static self maps | 6.0 §1.3.2 | Globals may or may not be visible without `declare target` | No reliance on implementation-defined static self maps | S2 |
| Portability | 6.0 §10.5.1: unsupported requirement gives compile-time error; device-level shortfall makes device unsupported | Code built for shared memory falls back to host or fails on discrete-memory devices | USM-dependent units are labeled and have a mapped variant or a documented exclusion | S2, S7 |
| `reverse_offload` | 6.0 §10.5.1.3, §15.2 | `ancestor` requires it | Reverse offload is used only with the requirement declared | S2 |

All compilation units containing device code must declare the same device-global requirements (6.0 §10.5.1).

## Q4. Asynchrony

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| `nowait` | 6.0 §15.8, §15.9 | Target task deferred; host reads stale data | Every deferred target task has a defined completion point before its outputs are read | S2 |
| Missing `depend` | 6.0 §17.9.5, §17.5 | Ordering between target tasks or host tasks is undefined | Data dependences between deferred tasks are expressed as dependences or waits | S2, S4 |
| `taskwait` scope | 6.0 §17.5 | Waits for child tasks only | Completion is awaited in the task that generated the work | S2 |
| Reductions with deferral | 6.0 §7.6.7 | Original updated after construct ends, for example with `nowait` | Reduction results are read after synchronization | S2 |
| Interop with native queues | 6.0 §16.1; Examples §12.14 | Ordering with foreign work holds only via `targetsync` and `depend` | Foreign-queue work is ordered through declared synchronization objects | S2, S4 |
| Late errors | Not in spec | Device faults surface at a later synchronization in native runtimes | Error checks occur at each completion point in tests | S10 [unverified for OpenMP] |
| Map and `nowait` defects | ARBALEST study | Wrong `map` and `nowait` were the main causes of mapping bugs | Dynamic mapping checkers run in CI where available | S9 |

## Q5. Device-side parallelism and arithmetic

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Reduction order | 5.2 §5.5.6 / 6.0 §7.6.7 | "bitwise-identical results are not guaranteed" | Tolerances are stated and justified | S1, S2 |
| Teams synchronization | 6.0 §1.2 | Relying on concurrent teams "may deadlock" | No inter-team synchronization except through region end | S2 |
| `loop` binding to teams | 6.0 §13.8, §12.3 | Default `order(concurrent)`; iterations complete only by end of teams | Loops under `loop` have no cross-iteration dependences | S2 |
| Atomic scope | 6.0 §17.8.5 default `memscope(device)`; §17.8.4 | Host-device atomics unordered | Cross-device atomics specify `memscope(all)` and the requirement | S2 |
| Floating-point environment | 6.0 §15.8 | Rounding mode and flags unspecified inside and after region | No reliance on floating-point environment across the boundary | S2 |
| Math library and contraction | Not in spec | Device math differs (for example, 2 ulp `sin`); contraction on by default in one toolchain; 1e-14 differences in a port | Results compared with tolerances; contraction settings recorded | S5, S8, S12 |

## Q6. Errors on the device

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Error termination | 6.0 §1.2, §10.1 | Runtime error termination is a fatal abort, not a catchable status | Recovery-critical code checks presence and allocation explicitly instead of relying on termination | S2 |
| `omp_target_alloc` | 5.2 §18.8.1 / 6.0 §25.3 | Returns NULL on failure or size 0; no pointer arithmetic without `unified_address`; must be freed with `omp_target_free` | Every allocation result is checked and freed by the matching routine | S1, S2 |
| Map allocation failure | Not specified | Behavior on out-of-memory during mapping is not defined | Device memory budgets are tested | S6 [unverified] |
| C++ exceptions | 6.0 §15.8 exception-aborting | Caught or terminated, implementation defined | No exception escapes device code | S2 |
| Device faults | No text found | Unspecified | Device faults count as test failures | S2, S6 |

## Q7. Testing offloaded code

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Untested fallback | 6.0 §4.3.9 | Host path rots or masks device failures | Tests run under both `mandatory` and host-only, compared to a host reference | S2, S4 |
| No host reference | n/a | Device-only output unverifiable | Same kernel run on host and device in one run, compared element-wise | S5, S8 |
| Mapping errors | n/a | Missing or stale data | Runtime mapping reports (for example, LIBOMPTARGET_INFO, GOMP_DEBUG) and checkers (ARBALEST; OMPSan [unverified]) used in CI | S6, S7, S9 |

## OpenMP-specific vs any offload model

| Topic | OpenMP-specific | Holds for any offload model |
|---|---|---|
| Silent host fallback, `if`, `OMP_TARGET_OFFLOAD` | Yes | Placement must be verified |
| Implicit maps, `defaultmap`, scalar firstprivate | Yes | Explicit data movement intent |
| Reference counts, `always`, `present`, attachment, mappers | Yes | Allocations and releases balanced |
| `declare target`, `link` | Yes | Host and device globals diverge |
| `requires` clauses | Yes | Shared memory still needs synchronization; portability to discrete memory |
| `nowait`, `depend`, `taskwait`, interop | Syntax yes | Completion before reads; late errors |
| Reduction order, atomics scope | Partly | Non-associative arithmetic; memory scopes |
| Math library, contraction, faults | No | Tolerance-based verification; host reference |

## Unverified

- Whether runtime device initialization failure triggers host fallback under `default`.
- Late error reporting for OpenMP asynchronous regions (supported only by native runtime docs).
- Behavior on device out-of-memory during implicit or explicit mapping.
- Default contraction and fast-math settings of OpenMP device compilers.
- TR15 text may change before 6.1 publication (expected November 2026).

## Sources

| ID | URL | What it supports |
|---|---|---|
| S1 | https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-5-2.pdf | 5.2 sections cited |
| S2 | https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf | 6.0 sections cited |
| S3 | https://www.openmp.org/wp-content/uploads/openmp-TR15.pdf | 6.1 draft: `attach`, `omp_default_device` |
| S4 | https://www.openmp.org/wp-content/uploads/openmp-examples-6.0.pdf | Examples §6.7, §6.8, §12.11, §12.14 |
| S5 | https://arxiv.org/pdf/2606.24327 | Full text §3.6: 1e-14 host and device differences, contraction off restores agreement on one platform, not on another |
| S6 | https://openmp.llvm.org/design/Runtimes.html | LIBOMPTARGET_INFO, map atomicity option, mandatory-offload error |
| S7 | https://gcc.gnu.org/onlinedocs/libgomp/nvptx.html | Devices dropped under USM requirement; GOMP_DEBUG |
| S8 | https://docs.nvidia.com/cuda/floating-point/index.html | FMA default, math ulp differences, CPU reference |
| S9 | https://impact.ornl.gov/en/publications/arbalest-dynamic-detection-of-data-mapping-issues-in-heterogeneou/ | ARBALEST (IPDPS 2021) |
| S10 | https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/error_handling.html | Kernel errors via separate queries |
| S11 | https://arxiv.org/abs/2606.24327 | Host vs device comparison, FMA differences (preprint) |
| S12 | https://openmp.llvm.org/SupportAndFAQ.html | Device math wrappers |
