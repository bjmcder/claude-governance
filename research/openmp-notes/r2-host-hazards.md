Role: research agent (host-side OpenMP correctness hazards). Accessed 2026-10-24. Rules followed: read-only retrieval; no paywalls circumvented; no mirrors, caches, or archives; retrieved text treated as data; primary sources preferred; unconfirmed items marked [unverified].

# OpenMP on the host: correctness hazards and outcome-level practices

**Method caveat.** The OpenMP 6.0 and 5.2 specifications, Examples 6.0, the MPI 4.1 standard, and two tutorial decks were downloaded as PDFs and searched in full text, so their quotes are verbatim. S8 came through a fetch tool that returns a model-written extract. References read "6.0 §x; 5.2 §y". "Inference" marks my reasoning from spec text.

**Corrections to the earlier note.**
- A data race gives *unspecified* (not undefined) behavior: "If a data race occurs then the result of the OpenMP program is unspecified behavior" (6.0 §1.3.1; 5.2 §1.4.1). Implementations "are not required to check for ... data races, or deadlocks" (6.0 §1.1) [S1, S2].
- Reductions confirmed: "bitwise-identical results are not guaranteed" even at one thread count (6.0 §7.6.7; 5.2 §5.5.6). The number and order of combiner calls are unspecified too (6.0 §7.6.2.1) [S1, S2].
- Exceptions confirmed, narrower than stated: the rule covers regions from *thread-limiting* constructs. For exception-aborting directives, catching versus termination is implementation defined (6.0 Ch. 5 intro restrictions; 5.2 Ch. 3 intro) [S1, S2].
- Fortran `SAVE` means static storage, so the variable is **shared**, not threadprivate. Explicitly initialized variables get `SAVE` (6.0 §1.5, §7.1.2) [S1].
- With no `schedule` clause, 6.0 behaves as `auto` (§13.6.3). In 5.2 the schedule is implementation defined (§11.5) [S1, S2].

## Answer in brief

1. Code is free of data races: conflicting accesses are ordered by OpenMP synchronization or are atomic. A race makes the program's result unspecified, and nothing is required to detect it (6.0 §1.1, §1.3.1) [S1].
2. Every variable referenced in `parallel`, `task`, `taskloop`, or `teams` has a visible data-sharing attribute; `default(none)` makes this checkable (6.0 §7.1.1, §7.5.1) [S1, S3 §10.2].
3. No private copy is read before it is written, and no original variable is relied on after privatization unless `lastprivate`, `reduction`, or `copyprivate` defines it (6.0 §7.4, §7.5.5) [S1].
4. No test requires bitwise-identical `reduction`, `scan`, or atomic accumulation. Results required to match across runs or thread counts use an order the program fixes itself (6.0 §1.2, §7.6.7, §7.7; 5.2 §1.3) [S1, S2].
5. All threads of a team meet the same sequence of worksharing and barrier regions; none sits in thread-divergent control flow (6.0 §13, §17.3.1) [S1].
6. Cross-thread signalling uses acquire/release (or `seq_cst`) atomics, `critical`, locks, or barriers. `atomic` defaults to `relaxed`; `flush` with a list is not used (6.0 §17.8.5, §17.8.6; S3 §11.1) [S1, S3].
7. No task outlives the storage it shares: a function that shares locals with tasks waits for them (`taskwait`, `taskgroup`, barrier) before returning (6.0 §1.3.1, §17.4, §17.5) [S1].
8. Untied tasks never access threadprivate storage, and no task assumes threadprivate values or thread identity survive a scheduling point (6.0 §7.3, §14.14; 5.2 §5.2) [S1, S2].
9. Libraries leave the caller's ICVs (`omp_set_num_threads`, `omp_set_dynamic`) unchanged, and programs use the thread count they actually get (6.0 §3.4, §12.1.1, §21.1, §21.7) [S1].
10. The program builds and behaves correctly without OpenMP, or its record says it does not; any thread-count dependence is documented and tested at several counts (6.0 §5.3; 5.2 §1.3) [S1, S2].

## 1. Data sharing

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Implicit `shared` | 6.0 §7.1.1: in `parallel`, unlisted variables are shared; static and heap objects are shared | Races on scratch variables declared outside | Explicit or predetermined attribute for each variable, enforced by `default(none)` | S1, S3 §10.2 |
| C/C++ inner loop index | 6.0 §7.1.1: only loops *associated with* the directive get private indices; a C/C++ inner index declared outside stays shared (Fortran indices inside `parallel` are private) | Race on the index | Indices declared in the loop or listed private | S1, S3 §10.4 |
| `default(private)` / `default(firstprivate)` | 6.0 §7.5.1: allowed in C/C++. Variables at namespace or global scope must still be listed explicitly | Developers assume globals become private | Globals referenced under these defaults appear in explicit clauses | S1 |
| Uninitialized private copy | 6.0 §7.4: a new item "has an undefined initial value, as if it had been locally declared without an initializer". Fortran private pointers start undefined | Garbage values; result depends on the run | No read of a private item before a write. Use `firstprivate` when the entry value is needed | S1 |
| Original variable after privatization | 6.0 §7.4: references to the original inside the region are unspecified, and so is its value after the region | Stale or partly updated values | Code does not depend on originals after the region unless a defining clause sets them | S1 |
| `lastprivate` gaps | 6.0 §7.5.5: if the sequentially last iteration does not assign the item, its value is unspecified. With `nowait`, it is defined only after a later synchronization | Wrong "last" value | Every `lastprivate` item is assigned in the last iteration, or uses `conditional`. With `nowait`, nothing reads it before a barrier | S1 |
| `threadprivate` persistence | 6.0 §7.3: values persist across regions only if neither is nested, team size and affinity match, `dyn-var` is false, and no pause or `teams` intervenes | Values reset silently | Persistence relied on only under those conditions; otherwise `copyin` | S1 |
| Untied task touching threadprivate | 6.0 §7.3: "an untied task accesses threadprivate memory" is non-conforming (5.2 §5.2 is the same) | Data read from another thread's copy | Untied tasks never touch threadprivate data, `_Thread_local`/`thread_local` data, or library state kept per thread | S1, S2 |
| Task default firstprivate | 6.0 §7.1.1: variables not shared in the enclosing context become firstprivate | Task's updates lost | Task outputs explicitly shared, with lifetime guaranteed | S1, S3 §5.1 |
| Stack variable after parent returns | 6.0 §1.3.1: the programmer "must use synchronization that ensures that the lifetime of the variable does not end before completion of the explicit task region sharing it" | Dangling reference; memory corruption | Any function that shares its locals with tasks waits for those tasks before it returns | S1 |

## 2. Reductions and reproducibility

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Unspecified combination order | 6.0 §7.6.7; 5.2 §5.5.6: no bitwise identity, even at the same thread count. Floating-point exceptions may differ | Golden-file tests fail at random; results drift | Tests use tolerances justified by error analysis, or the program fixes the reduction order itself | S1, S2 |
| Thread-count dependence | 5.2 §1.3 and 6.0 §1.2: different thread counts "may result in different numeric results" | Results change with deployment | Thread-count-independent results come from a fixed partition into blocks combined in a fixed order (inference) | S1, S2 |
| User-defined reductions | 6.0 §7.6.2.1: combiner call count and order unspecified; §7.6.2.2: initializer uses only `omp_priv`/`omp_orig` and must not modify `omp_orig` | Non-associative combiners give schedule-dependent results | Each `declare reduction` records why its combiner is associative and commutative and its initializer an identity | S1 |
| `task_reduction` / `in_reduction` | 6.0 §7.6.10–7.6.12: an unspecified number of extra copies; the result is defined only after the region ends. Original items must live past the final synchronization | Reading partial sums; dangling originals | Nothing reads the reduction result before the scoping region completes | S1, S3 §10.10.2 |
| `scan` | 6.0 §7.7: defined by a prefix sum whose split point j is arbitrary | Prefix results differ in the low-order bits | Same tolerance rule as reductions | S1 |
| `schedule(static)` for reproducibility | 6.0 §13.6, §6.4.4: static (without `simd`) or `order(reproducible:...)` gives a reproducible iteration-to-thread mapping for equal thread and iteration counts | It does not fix reduction combining order (inference from §7.6.7) | Mapping relied on only under §6.4.4/§13.6 conditions, never for reduction order | S1 |
| No schedule clause | 6.0 §13.6.3: as if `auto`. 5.2 §11.5: implementation defined | Any dependence on the schedule breaks when the implementation changes | Code that depends on the schedule names an explicit reproducible schedule | S1, S2 |
| `ordered` | 6.0 §17.10: ordered regions run in iteration order | Gives a deterministic order but serializes that part of the loop | Use `ordered` only where serial order is required, and record the performance cost | S1 |

## 3. Synchronization and the memory model

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Divergent barriers | 6.0 §17.3.1, §13: barriers are reached "by all threads in a team or by none at all", in the same sequence | Deadlock | No barrier or worksharing construct depends on thread number or thread-varying data | S1 |
| `nowait` | 6.0 §13, §17.6: threads proceed "without performing a flush operation"; `lastprivate` and reduction results pending | Reading partial data | Each `nowait` names the later synchronization protecting its consumers | S1, S3 §3.7 |
| Missing implicit flushes | 6.0 §17.8.7: no flush at entry to worksharing regions or at entry to or exit from `masked` | Stale data after `masked` | Data produced in `masked` is consumed only after a barrier or other synchronization | S1 |
| Atomic default ordering | 6.0 §17.8.5: with no memory-order clause, "the effect is as if the relaxed memory-order clause is specified" (5.2 §15.8.4 is the same) | A flag set by atomic write does not publish the data written before it | Atomics used to signal carry `release`/`acquire` (or `seq_cst`), or a `requires atomic_default_mem_order` is recorded (6.0 §10.5.1.1) | S1, S3 §9.8 |
| Mixing atomic with plain access; misalignment | 6.0 §17.8.5: "all accesses ... that could potentially occur in parallel must be protected with an atomic construct"; `critical` and locks do not exclude atomics; a location that is not size-aligned is implementation defined | Torn or lost updates | Atomically accessed locations are naturally aligned and accessed only atomically during concurrency | S1 |
| Spin-wait on a plain variable | S3 §11.1: the write to and read from `flag` "must be atomic to avoid a data race" | Endless loop or premature reads | Flag read by acquire atomic, written by release atomic | S1, S3 |
| `flush` with a list | 6.0 §17.8.6: it does not order accesses to other variables. S3 §11.1: "extremely error prone and users are strongly discouraged" | Reordering breaks the protocol | Code has no `flush` with a list. Ordering comes from memory-order clauses or higher-level constructs | S1, S3 |
| Unnamed or nested `critical` | 6.0 §17.2: all unnamed criticals share one name; nesting a critical inside another with the same name is forbidden, and "not sufficient to prevent deadlock" | Unexpected serialization or deadlock | Critical sections are named by the resource they protect, and no same-name nesting is possible | S1 |
| Simple lock re-acquired | 6.0 §28.3.1: setting a lock the task already owns causes deadlock. Unsetting a lock another task owns is non-conforming (Ch. 28) | Deadlock or unspecified state | Simple locks are never re-acquired by their owner. A global lock order is documented. Every lock is destroyed after its last use | S1 |
| Locks across contention groups | 6.0 Ch. 28: using one lock in different contention groups gives unspecified behavior | Mutual exclusion fails | Locks are used only inside one contention group (relevant when threads are made outside OpenMP) | S1 |

## 4. Tasking

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| `depend` on overlapping storage | 6.0 §17.9.5: dependences link dependence-compatible (mainly sibling) tasks; items "must indicate identical storage locations or disjoint storage locations" | Missed ordering | Dependences name identical or disjoint storage; non-siblings ordered by `taskwait`/`taskgroup` | S1, S3 §5.3 |
| `taskwait` vs `taskgroup` vs barrier | 6.0 §17.5: `taskwait` waits for *child* tasks only; §17.4: `taskgroup` waits for the taskgroup set; §17.3.1: barriers complete all bound explicit tasks | Grandchildren still running | The wait chosen covers every task writing the consumed data | S1 |
| Locks or `critical` across scheduling points | 6.0 §14.14 note: "deadlock is possible" | Deadlock | No lock held across a task scheduling point unless shown deadlock-free | S1, S3 §5.1 |
| Assumptions about scheduling | 6.0 §14.14: "A program must behave correctly and consistently with all conceivable scheduling sequences" | Bugs that come and go | Tests include runs at 1 thread and at several thread counts | S1 |
| `mergeable` | 6.0 §14.5; S3 §5.1: a merged task may share the parent's data environment. With `firstprivate` data, "it can print two different values" | Result depends on the implementation | `mergeable` is used only when the result is the same whether or not the task is merged | S3 |
| Task explosion, recursion depth | S3 §5.1: the implementation "may reach its limit on unassigned tasks". 6.0 §14.7: tasks inside a final task are included; §14.4: `untied` is ignored for them | Memory or stack exhaustion; code assuming deferral | Recursive task creation has a recorded cutoff (`final`, `if`, or a threshold), and correctness does not depend on deferral | S1, S3 |
| `detach` | 6.0 §14.11: the encountering task must not be final; the event handle is not otherwise listed in data clauses | Task never completes (hang) | Every detached task's event is fulfilled on every path, including error paths | S1 |
| Cancellation | 6.0 §18.2: ignored unless `cancel-var` is true (initially false, §3.2); `lastprivate`/`reduction` values undefined; locks not released | Silent no-op; leaked locks | `cancel` code tested with cancellation on and off, and releases locks first | S1, S3 §12.5 |

## 5. Runtime configuration and global state

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Implementation-defined initial ICVs | 6.0 §3.2: `nthreads-var`, `dyn-var`, `bind-var`, `max-active-levels-var`, `stacksize-var`, `wait-policy-var`, `place-partition-var` | Behavior varies by system | Run records capture effective settings (`OMP_DISPLAY_ENV`, §4.7; `omp_display_env`, §30.4) | S1 |
| Fewer threads than requested | 6.0 §12.1.1: the thread count depends on `dyn-var`, `thread-limit-var`, `max-active-levels-var`. `num_threads(strict:...)` causes runtime error termination if the count cannot be met (§12.1.2) | Code that indexes by thread number fails | Code sizes per-thread arrays from `omp_get_num_threads()` inside the region, or uses `strict` | S1 |
| Libraries changing ICVs | 6.0 §21.1/§21.7: these routines set the ICV "of the current task". §3.4: generated tasks inherit it | A library call changes every later parallel region in the caller | Libraries restore any ICV they change, or use clauses (`num_threads`) instead of routines | S1 |
| Nesting and oversubscription | 6.0 §1.2 (nested teams); §4.1.3 (a list raises `max-active-levels-var`); §4.3.3 (active waiting consumes cycles) | Threads far exceed cores; severe slowdown (inference) | Total threads across levels and libraries bounded and recorded | S1 |
| Threaded libraries | S8: an already multi-threaded application "will conflict with OpenBLAS multi-threading"; calls from parallel regions need an OpenMP build "to avoid possible deadlocks" | Oversubscription, deadlock | Each dependency's threading mode and count recorded and tested from inside parallel regions | S8 |
| Other native threads | 6.0 §1.2: base-language concurrency semantics "apply to OpenMP threads"; OpenMP in foreign threads is not otherwise defined [unverified] | Unspecified interactions | Mixing recorded and tested on each supported implementation | S1 |
| MPI | MPI 4.1 §11.2.1: `MPI_INIT_THREAD` levels SINGLE < FUNNELED < SERIALIZED < MULTIPLE. The `provided` level may be lower than required | MPI calls from worker threads that the provided level does not permit | Programs request the level their OpenMP use needs and stop with an error if `provided` is lower | S5 |
| `fork()` after initialization | S3 §12.12: runtime resources "may cause unexpected side effects for the subsequent fork call"; use `omp_pause_resource` (6.0 §30.2.1) | Child misbehaves [symptom unverified] | No `fork` after initialization unless resources are paused first, or the child only calls `exec` (inference) | S3, S1 |
| Thread stack size | 6.0 §4.3.2: `OMP_STACKSIZE` sets worker stacks, not the initial thread's; unmet sizes are implementation defined | Overflow only in workers | Large private arrays on the heap, or required stack size recorded | S1 |

## 6. Error handling

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| No diagnostics required | 6.0 §1.1 | Silent corruption | Correctness shown by tests and race checking | S1 |
| `error` directive | 6.0 §10.1: shows an implementation defined message; `fatal` at execution aborts the program | Unclear message content | Fatal error paths are designed and tested; message text is not parsed | S1 |
| Allocation failure | 6.0 §8.2: `null_fb` returns zero; host default `default_mem_fb`; `omp_default_mem_alloc` uses `null_fb`; §8.5: `allocate` directive treats `null_fb` as `abort_fb` | Null dereference | Each OpenMP allocation is checked, or abort fallback chosen deliberately | S1 |
| Exceptions | 6.0 Ch. 5 intro restrictions; §6.3: `throw` must not break structured-block entry/exit; same region, same thread | Termination or undefined unwinding | No exception leaves a structured block; each region catches its own exceptions | S1 |
| Early exit, `setjmp`/`longjmp` | 6.0 §6.3: no branch in or out; `setjmp` not the entry point; `longjmp` must respect entry/exit. `exit`, `abort`, `STOP` allowed | Corrupted team state | No `return`, `goto`, `break`, or `longjmp` leaves a region | S1 |
| Signals | 6.0 §1.2: "A signal handler may only execute directives and routines that have the async-signal-safe property". In 6.0 only OMPT tool entry points have that property (inference from a property search) | Deadlock inside the runtime | Signal handlers contain no OpenMP directives or routines | S1 |

## 7. Serial equivalence and conditional compilation

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| Parallel-only correctness | 5.2 §1.3: a conforming program "may execute correctly as a parallel program but not as a sequential program" | Serial builds wrong | Serial-build support stated; if supported, CI builds and tests it | S2 |
| `_OPENMP` misuse | 6.0 §5.3: `_OPENMP` = yyyymm; user code must not define or undefine it. Fortran uses `!$` sentinels | Wrong feature path | Version-dependent code tests `_OPENMP` values, and the minimum version is recorded | S1 |
| Thread-count dependence | 6.0 §1.2; §1.5: concurrent library calls are correct "although not necessarily the same as serial execution results" | Output differs by count | Tests at 1 and at least two other counts; accepted differences documented | S1 |
| Side effects in clause expressions | 6.0 Ch. 5 intro: programs must not depend on the order or side effects of clause expression evaluation | Results vary between compilers | Clause expressions have no side effects | S1 |

## 8. Performance hazards that become correctness or reproducibility issues

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| False sharing, sub-word writes | 6.0 §1.3.1: writes below the implementation's minimum size, and C/C++ bit-fields, may rewrite a larger unit. S7: elements "on the same cache line" make it "slosh back and forth" | Lost updates (bit-fields); performance collapse | No unsynchronized concurrent writes to one unit; per-thread accumulators padded or private | S1, S7 |
| NUMA first touch | S6: pages placed "close to the CPU causing the page fault" | Slowdown, timing variation | Parallel initialization with the compute loops' schedule and binding; `OMP_PROC_BIND`/`OMP_PLACES` (6.0 §4.1.6-4.1.7) recorded | S6, S1 |

## 9. Language specifics

| Hazard | Spec reference | Failure | Practice as an outcome | Source |
|---|---|---|---|---|
| C++ iterator loops | 6.0 §6.4.1: random-access iterators and range-based `for` allowed; range invariant; §7.1.1: range-for variables private | Non-canonical loops | Container loops use random-access iterators; container unchanged during the loop | S1, S3 §3.16 |
| Concurrent container mutation | 6.0 §1.3.1 (race); §1.5 (only base-language library *procedures* must be thread-safe) | Corrupted container | No shared container is modified concurrently without synchronization (C++ library rules [unverified here]) | S1 |
| `new` and RAII | 6.0 §1.5: allocation thread-safe; §7.4: private-copy constructor and destructor order unspecified; §18.2: C++ destruction rules under cancellation | Order-dependent code | Private class objects have no cross-object ordering dependencies | S1 |
| C++ memory model | 6.0 §1.3.5: happens-before includes the base language's; §17.8.6: list-less `flush` equals `atomic_thread_fence` | Mixed models | One synchronization mechanism per shared object (mixing `std::atomic` and `omp atomic` [unverified]) | S1 |
| Fortran `workshare` | 6.0 §13.4: user calls must be pure and elemental; assignments to private variables unspecified | Wrong results | Only pure elemental calls; assignments only to shared data | S1, S3 §3.13 |
| Fortran copy-in/copy-out; storage association | 6.0 §7.1.2: dummy argument sharing is implementation defined for non-contiguous actuals; S3 §10.7, §11.3: temporaries "would cause races". 6.0 §7.4: storage associated with a private variable (`COMMON`, `EQUIVALENCE`) becomes undefined | Races even with `atomic` in the callee; garbage values | Shared sections passed to procedures are contiguous or calls synchronized; privatized variables are not storage-associated | S1, S3 |
| `SAVE` / initialized locals | 6.0 §1.5, §7.1.2: static storage, therefore shared | Hidden races in callees | Procedures called in parallel have no unsynchronized `SAVE` or initialized locals, unless threadprivate | S1 |

**Offload note.** The progress guarantee changes for divergent threads on one progress unit, where spin-synchronization "may deadlock" (6.0 §1.2). Atomic scope and flush thread-sets also differ for `target` regions (6.0 §17.8.7). Those rules belong to the offload note.

## Unverified

- How OpenMP behaves when called from threads it did not create (pthreads, C++ threads). Beyond 6.0 §1.2 and the Ch. 28 contention-group rule, I found no normative text.
- Hangs after `fork()` as a general symptom. S3 says only "unexpected side effects".
- Mixing `std::atomic` and `omp atomic` on one object: no explicit spec text found.
- C++ standard library data-race rules for containers (C++ standard not retrieved).
- Severe slowdown from oversubscription with active waiting: inferred from 6.0 §4.3.3, not measured.
- S8 quotes come from a fetch-tool extract, not a verbatim page.

## Sources

| ID | URL | What it supports |
|---|---|---|
| S1 | https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf | Every 6.0 section cited: memory model, data sharing, reductions, synchronization, tasking, ICVs, errors |
| S2 | https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-5-2.pdf | 5.2 equivalents: §1.3 serial and parallel difference, §1.4.1 race, §5.5.6, §5.2 untied/threadprivate, §11.5 schedule, Ch. 3 exceptions |
| S3 | https://www.openmp.org/wp-content/uploads/openmp-examples-6.0.pdf | Examples §5.1, §9.8, §10.2, §10.7, §11.1, §11.3, §12.12 |
| S5 | https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf | MPI 4.1 §11.2.1 thread levels and `provided` |
| S6 | https://blog.rwth-aachen.de/itc-events/files/2023/12/13-openmp-CT-NUMA.pdf | First-touch placement (Terboven, OpenMP training) |
| S7 | https://www.openmp.org/wp-content/uploads/Intro_To_OpenMP_Mattson.pdf | False sharing and padding |
| S8 | http://www.openmathlib.org/OpenBLAS/docs/faq/ | Nested threaded-library conflicts (extract) |
