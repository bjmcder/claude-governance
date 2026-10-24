Role: research agent. Date accessed: 2026-10-24. Retrieval rules followed: read-only retrieval; about 26 requests and about 16 MB in total; no paywalls touched; blocked pages (HTTP 403 on openmp.org HTML pages) were not worked around and no mirrors, caches, archives, or wire-service reprints of them were used; retrieved text treated as data; unconfirmed items marked [unverified].

# R1: Trajectory of the OpenMP specification and what 6.1 is expected to change

## Method caveat

The four specification PDFs (5.2, 6.0, TR14, TR15) were downloaded from openmp.org and converted to full text locally, so quotations from them are from the full documents. Vendor pages and the news article were read through a fetch tool that returns a model-written extract, not the full page; those findings are paraphrase and may omit detail. Every openmp.org HTML page tried returned HTTP 403, so the ARB's news text and compilers list could not be read. Claims resting only on search summaries are marked.

## Answer in brief

1. Between 5.0 and 6.0 the correctness-relevant changes are mostly syntax deprecations (5.0, 5.1, 5.2) that 6.0 then removed outright, plus a few semantic changes to defaults: nonmonotonic default scheduling for non-static schedules (5.0), firstprivate fallback for unmatched mapped pointers (5.2), default map types on enter/exit data (5.2), reference-count semantics for `use_device_ptr` and `use_device_addr` (6.0), and new non-conformance for `ordered` inside an unroll factor of one (6.0). The memory model was rebuilt in 5.0 (flush kinds, happens-before, acquire/release) and has only been extended since. `master` (deprecated 5.1) and its combined forms are gone from 6.0 [S1, S2].
2. TR15 (2026-07-09) is additive. Its feature-history appendix lists one new deprecation (a conditional-update-capture atomic form with no capture statement), no removals, and about 30 additions: multidimensional execution spaces, hierarchical `OMP_PLACES`, `dyn_groupprivate`, `flatten`, `fuse` `depth`, `attach`, per-thread reductions, scalable `simdlen`, `omp_default_device`. Two items relax or alter existing semantics (schedule `simd` chunking; `taskwait`-implied dependences). The document was also reorganized (42 to 49 chapters), so section numbers move [S3].
3. Stable across 5.0 to 6.1: the core fork-join, worksharing, tasking, data-sharing clause, reduction, atomic, and flush model; `requires` causing a compile-time error for unsupported requirements; `OMP_TARGET_OFFLOAD=mandatory`. Moving: anything device- or affinity-related added in 6.0 or 6.1, loop transformations, and all syntax that 5.2 or 6.0 deprecated.
4. No implementer page read claims full 5.2 or 6.0 support. Clang: "fully supports OpenMP 4.5, almost all of 5.0 and most of 5.1/2" [S6]. GCC tracks per-feature status, with many 5.x and 6.0 items "No" [S5]. Intel: 5.0, most of 5.1 and 5.2, some 6.0 [S7, search extract]. NVIDIA: "a subset" focused on 5.0 [S8]. A rule must therefore be checked per feature against the specific toolchain, not by version number.
5. A news article reports a Python Language Subcommittee aiming at OpenMP 7.0, planned for 2029 [S9]; the ARB's own announcement was blocked (403). No published post-6.1 cadence was confirmed.

## Findings

### 1. Correctness-relevant changes from 5.0 to 6.0

| Item | Finding | Source |
|---|---|---|
| Memory model | 5.0 distinguished flush kinds, defined happens-before through synchronizing flushes, and added `acq_rel`, `acquire`, `release` on `atomic` and `flush`. 5.1 allowed `seq_cst` on `flush`. 6.0 added `memscope` on `atomic` and `flush` for multi-device binding sets. Additive since 5.0. | S2 (B.2, B.4, B.5) |
| Nested parallelism default | 5.0 folded nesting control into `max-active-levels-var`, whose default became implementation defined; `OMP_NESTED`, `omp_set_nested`, `omp_get_nested` deprecated (5.0) and removed (6.0). | S1, S2 |
| Schedule default | 5.0 changed the default ordering modifier for non-static schedules without `ordered` to `nonmonotonic`. | S2 (B.5) |
| `order(concurrent)` | 5.2 changed it to affect schedule reproducibility only if a modifier is explicit. 6.0 relaxed which constructs may appear in such regions (including `atomic`). | S2 |
| `master` to `masked` | `masked` added and `master` construct, its combined and composite forms, and the `master` affinity policy deprecated in 5.1. 6.0 removed all 5.x deprecations; the word `master` survives in 6.0 only in the history appendix. | S1, S2 |
| Other 5.x deprecations removed in 6.0 | 5.2: `linear` modifier(list) syntax, the minus reduction operator, comma-less `map` modifiers, `to` on declare target (use `enter`), C/C++ delimited declare target, `default` on metadirective (use `otherwise`), `depend(source/sink)` (use `doacross`), old `uses_allocators` syntax, Fortran `allocate` on `ALLOCATE` (use `allocators`). 5.1: Cray pointers, non-`C_PTR` items in `use_device_ptr`/`is_device_ptr`, `omp_atv_sequential`. 5.0: lock hint names. | S1 (B.1), S2 (B.2) |
| Undeprecation | 6.0 undeprecated the argument-less `destroy` on `depobj`, which 5.2 had deprecated. Deprecation is not always one-way. | S2 (B.2) |
| 6.0 deprecations | Fortran keyword run-together spelling, combiner-in-argument `declare_reduction` syntax, Fortran `omp_lib.h`, several OMPT target callbacks. | S2 (B.1) |
| Data-sharing and mapping defaults | 4.5 made implicit scalars in `target` firstprivate. 5.1 allowed `default(private/firstprivate)` in C/C++. 5.2: unmatched mapped pointers get firstprivate semantics and keep their value; enter/exit data `map` has default to/from types. 6.0: `default` allowed on `target`; `use_device_ptr`/`use_device_addr` on `target_data` now imply reference-count updates; `self` maps and the `self_maps` requirement added. | S2 |
| Reductions and atomics | 5.0 task and `inscan` reductions; 5.1 `compare` and `fail` on `atomic`; 5.2 minus operator deprecated; 6.0 reductions over private variables, `induction`, Fortran atomic extensions. | S2 |
| Error handling | `error` directive added in 5.1. Spec defines compile-time and runtime error termination as equivalent to a fatal `error` directive at compilation or execution. 6.0 added `message` and `severity` to `parallel`. | S2 (B.4, B.2), S3 (ch. 1) |
| `requires` | Added in 5.0. 5.1 deprecated using its clauses as context traits. In 5.2, 6.0, and TR15 the text says an implementation that does not support a requirement "must perform compile-time error termination." 6.0 added `self_maps` and `device_safesync`. | S1, S2, S3 (16.5.1) |
| Offload defaults | `OMP_TARGET_OFFLOAD` added in 5.0. Under the `default` value the default device may be the host; under `mandatory`, an unavailable device acts as `omp_invalid_device`, which leads to runtime error termination. Unchanged in TR15. | S2 (B.5), S3 (3, 4.3.9) |
| New non-conformance in 6.0 | A stand-alone `ordered` inside an `unroll` with factor one is now non-conforming; C/C++ list-form `declare_target` must sit at the scope of the declaration. | S2 (B.2) |
| 5.2 framing | The ARB says 5.2's reorganization "almost always" resolves ambiguities but "may nonetheless have implications for existing implementations and programs." | S2 (B.3) |

### 2. What TR15 adds, changes, deprecates, removes relative to 6.0

TR15 is titled "Version 6.1 Public Comment Draft," dated July 9, 2026, with comments solicited until September 30, 2026 [S3]. It calls itself "the final preview" and, like all technical reports, "non-normative" [S3]. TR14 is confirmed as "a first preview" of 6.1 dated November 13, 2025, comments to June 30, 2026 [S4]. The earlier note called TR15 "the final public comment draft"; the document's own wording is "final preview" and "Public Comment Draft."

| Item | Finding | Source |
|---|---|---|
| Deprecated in 6.1 | One item: "A form for a conditional-update-capture structured block without a capture statement," all base languages. Already present in TR14. | S3, S4 (B.1) |
| Removed in 6.1 | None listed. All 6.0 deprecations remain deprecated, not removed. | S3 (B.1, B.2) |
| Confirmed from TR14 | `flatten`; `depth` on `fuse`; `sizes-selector` on `sizes`; `attach` map modifier; `dyn_groupprivate` plus routines; Fortran `begin declare_variant`; `scaled-modifier` on `simdlen`; `omp_default_device`; `omp_target_is_accessible` wording. Earlier note's TR14 list is correct. | S4 (B.2), S3 (B.2) |
| New in TR15 vs TR14 | Spatial ICVs, `dims-modifier`, multidimensional routines; hierarchical and `structured` `OMP_PLACES` syntax and updated `spread`; `OMP_PROC_BIND` `reset`/`noreset`; Fortran `optional-modifier` on `default`/`defaultmap`; atomic type conversions; `implicit` default-behavior (preferred over `defaultmap` `default`, not deprecating it); `per-thread-modifier` on `reduction`; Fortran polymorphic `map`; `vendor` trait for device selectors; `shift` on `tile`; `depobj-modifier`/`loc-modifier` on `depend`; C++ `omp::allocator::user_mem`; `omp_get_filtered_devices`, `omp_get_device_distances`; two OMPT entry points; Fortran type-bound calls in `target` clarified. | S3 (B.2) |
| Semantic changes to existing features | (a) The restriction on the first chunk under the `simd` schedule modifier was removed, and without `chunk_size` an implementation may base `new_chunk_size` on any subdivided chunk. Code that relied on a particular chunk layout could see different distribution. (b) `taskwait` can now imply dependences between child tasks of an exporting task and a later sibling. This adds ordering rather than removing it. | S3 (B.2) |
| Appendix completeness | The appendix "summarizes the major changes." TR15 also contains a `fallback` modifier (`fb_preserve`, `fb_nullify`) on `use_device_ptr` that is not in the B.2 list, so B.2 is not exhaustive. | S3 (B, 11.x) |
| Document structure | 6.0 has 42 numbered chapters; TR15 has 49 and a new "Data Control" part splitting the old Data Environment chapter. Section numbers for the same feature differ. | S2, S3 (contents) |
| Radical or additive | Additive. Evidence: one deprecation, zero removals, every B.2 item is phrased "was added," "was extended," or "was clarified," and the two behavior changes are narrow. The multidimensional teams model extends `teams`/`parallel` rather than replacing them. A search summary attributes to the ARB the view that 6.1 is a minor release improving the device model and affinity [unverified, ARB page blocked]. | S3 |

### 3. Implementation support

| Item | Finding | Source |
|---|---|---|
| ARB compilers page | Blocked (HTTP 403). Earlier note's "no compiler showed full 6.0 support" could not be re-confirmed. | none |
| GCC | Per-feature tables for 5.0, 5.1, 5.2, 6.0, and TR15 (described as "the second preview for OpenMP 6.1"). No overall completeness claim for 5.x. Many 6.0 and TR15 rows "No"; `omp_default_device` listed for GCC 16. Disclaimer: "A feature might be only fully supported in a later GCC version than listed." | S5 (extract) |
| Clang/LLVM | "Clang fully supports OpenMP 4.5, almost all of 5.0 and most of 5.1/2." 5.2 rows mostly "unclaimed," including all 5.2 deprecations; about 20 6.0 rows done; some 6.1 rows done or partial. Default `-fopenmp-version` not stated on the page [unverified]. | S6 (extract) |
| Intel oneAPI 2026.0 | Search summary of the developer guide: complies with 5.0, "most of" 5.1 and 5.2, "some" 6.0 TR12 features; release notes mention a 6.1 `fallback` feature. Fetch of the page itself was truncated before the statement [partly unverified]. | S7 |
| NVIDIA HPC SDK 26.9 | "Support a subset of the OpenMP Application Program Interface," documented against 5.0. Not supported: memory allocators and allocator routines, `task` inside `target`, `depend` on GPU targets; `unified_address`/`unified_shared_memory` "accepted but have no effect." | S8 (extract) |

Implication for a "use only what the toolchain implements" rule: support is partial at every vendor and is reported per feature, not per version, and in some cases per language and per device. A version number such as `_OPENMP` or a claimed spec level cannot prove a feature works. The checkable form is per feature: the feature appears as supported in the toolchain's own documentation for the exact release, for every language and target used, and is exercised by a test on each target. Because Clang lists 5.2 deprecations as "unclaimed," an implementation may still accept syntax that 6.0 removed; compiler acceptance is not evidence of conformance. The `requires` directive is the one in-spec mechanism that converts a missing device capability into a compile-time error [S3], though at least one vendor reports accepting some requirement clauses with no effect [S8].

### 4. Direction after 6.1

| Item | Finding | Source |
|---|---|---|
| 6.1 final | TR15 says it is the final preview; final adoption expected November 2026 before SC26 [unverified beyond search summaries; ARB press page blocked]. Not yet released as of 2026-10-24 per search. | S3 |
| Python and 7.0 | Article dated 2026-02-17 (updated 2026-05-12): ARB formed a Python Language Subcommittee to add Python in 7.0, Anaconda joined the ARB, 7.0 planned for 2029. Links to an openmp.org press release that returned 403. | S9 |
| Cadence | No current ARB cadence statement found. The 6.0 to 6.1 gap (two years, with two TRs between) matches the earlier 5.0, 5.1, 5.2 pattern, but that is an inference. | inference |

## Stable vs moving

| Practice or feature | Stable since | Status | Reason |
|---|---|---|---|
| Explicit data-sharing via `default(none)` and named clauses | 2.5 or earlier [unverified exact]; `none` unchanged through TR15 | Stable | No version changed its meaning; later versions only add categories. |
| `parallel`, worksharing loop, `single`, `critical`, `barrier`, `atomic` basic forms | pre-5.0 | Stable | Not touched by any deprecation list 5.0 to 6.1. |
| Memory model: flush, happens-before, acquire/release | 5.0 | Stable | Only extended (`seq_cst` flush 5.1, `memscope` 6.0). |
| `masked` instead of `master` | 5.1 | Stable | `master` removed in 6.0; `masked` unchanged since. |
| `enter` on declare target, `doacross`, `otherwise`, comma-separated `map` modifiers | 5.2 | Stable replacement | These are the surviving forms after 6.0 removals. |
| `omp_lib.h` in Fortran | n/a | Deprecated (6.0) | Use the `omp_lib` module; removal likely in a later major version [unverified]. |
| `error` directive and `at`/`severity`/`message` | 5.1 | Stable, partial support | Spec stable; implementation coverage varies [S5, S6]. |
| `requires` causing compile-time error when unsupported | 5.2 text confirmed; 5.0 origin | Stable spec, uneven practice | Vendor reports of clauses with no effect [S8]. |
| `OMP_TARGET_OFFLOAD=mandatory` to forbid silent host fallback | 5.0 | Stable | Same semantics in TR15. |
| Implicit firstprivate for scalars in `target` | 4.5 | Stable | Unchanged since. |
| `use_device_ptr`/`use_device_addr` semantics | 6.0 | Moving | Reference-count change in 6.0; `fallback` modifier in 6.1 draft. |
| Reductions and atomics, core operators | pre-5.0 | Stable, minus operator removed | Minus deprecated 5.2, removed 6.0; 6.1 adds per-thread modifier and deprecates one capture form. |
| Loop transformations (`tile`, `unroll`) | 5.1 | Moving | Extended in 6.0 and 6.1; 6.0 added a non-conformance case. |
| `fuse`, `interchange`, `reverse`, `split`, `stripe`, `apply` | 6.0 | Moving, partial | New in 6.0; `fuse` gains `depth` in 6.1. |
| `flatten`, `dyn_groupprivate`, `attach`, multidimensional teams, `omp_default_device` | 6.1 draft | Draft | Non-normative until 6.1 adopted; mostly unimplemented [S5, S6]. |
| `OMP_PLACES` and `OMP_PROC_BIND` syntax beyond basic forms | 6.0 / 6.1 draft | Moving | Extended in both versions. |
| Free-agent threads, `taskgraph`, `groupprivate`, `self_maps`, `memscope` | 6.0 | Moving, partial | New in 6.0, sparse support. |
| Unified shared memory requirements | 5.0 | Stable spec, uneven practice | Vendors differ on effect [S5, S8]. |
| Section numbers of the specification | none | Moving | TR15 renumbers chapters; cite construct names, not section numbers. |

## Unverified

- 6.1 final release date and status as of today; ARB description of 6.1 as "minor" (search summaries only; openmp.org press pages 403).
- Existence of Examples 6.0.1 and the 6.0 errata (November 2025); openmp.org specifications page 403, guessed PDF name 404.
- ARB compilers page contents, including "no compiler showed full 6.0 support."
- ARB's own Python/7.0 announcement and any official cadence; only a secondary article read.
- Intel's exact support wording (search summary of its guide; direct fetch truncated).
- Clang's default `-fopenmp-version`.
- Whether `default(none)` semantics are identical back to 2.5, and the year `requires` text first mandated compile-time error (confirmed for 5.2, 6.0, TR15 only).
- Any future removal date for 6.0 deprecations.

## Sources

| ID | URL | What it supports |
|---|---|---|
| S1 | https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-5-2.pdf | 5.2, 5.1, 5.0 deprecation lists; `requires` compile-time error text in 5.2 |
| S2 | https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf | 6.0 deprecations; removal of all 5.x deprecations; history 4.5 to 6.0; `master` absent |
| S3 | https://www.openmp.org/wp-content/uploads/openmp-TR15.pdf | TR15 date, status, B.1/B.2, `requires`, `OMP_TARGET_OFFLOAD`, error termination, structure |
| S4 | https://www.openmp.org/wp-content/uploads/openmp-TR14.pdf | TR14 date and 6.1 change list |
| S5 | https://gcc.gnu.org/projects/gomp/ | GCC per-feature status, TR15 table, disclaimer |
| S6 | https://clang.llvm.org/docs/OpenMPSupport.html | Clang support statement and status tables |
| S7 | https://www.intel.com/content/www/us/en/docs/dpcpp-cpp-compiler/developer-guide-reference/2026-0/openmp-support.html | Intel 2026.0 support (page truncated; statement from search summary) |
| S8 | https://docs.nvidia.com/hpc-sdk/compilers/hpc-compilers-user-guide/index.html | NVIDIA 26.9 subset and limitations |
| S9 | https://www.admin-it.io/openmp-adds-support-for-python/ (redirected from admin-magazine.com) | Python subcommittee, 7.0 in 2029 |
| Blocked | openmp.org /specifications/, /press-release/, /?p=6240, /resources/openmp-compilers-tools/, /press-release/python-new-member-anaconda/ | HTTP 403, not worked around |
