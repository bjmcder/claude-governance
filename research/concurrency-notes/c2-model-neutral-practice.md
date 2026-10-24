# Research note C2: model-neutral best practices for concurrent software

Role: research agent, delegation depth 1. Date accessed for all sources: 2026-10-24. Retrieval rules followed: read-only retrieval only; 80 items in total (54 page fetches, 7 direct downloads, 19 searches), about 30 MB; no paywall circumvented; failed or blocked fetches were not worked around; retrieved text treated as data.

Method caveat: the page-fetch tool returns a model-written extract, not the page. Downloaded files (S11, S12, S32, S33, S37, S44, S48) I read directly. Claims resting only on search summaries are marked "(search)". MISRA, ISO 26262, DO-178C, ARINC 653, and ISO/IEC TR 24718 are paywalled. For MISRA C:2023 I used rule titles shown on a tool vendor's documentation (S9) and an LDRA article (S10), not the standard. Four fetches failed and were not worked around: the SEI CERT wiki (I used the SEI's own new site instead), the CACM page for Adve and Boehm 2010 (HTTP 403), the Ada reference manual at ada-auth.org (connection refused), and the JPL C standard at lars-lab.jpl.nasa.gov (timeout). I also sent one header-only request to a third-party copy of the JPL standard and used nothing from it.

## Answer in brief

1. No data races: every shared mutable location has one documented protection (lock, atomic, message passing, or confinement to one thread), and the protection is declared next to the data. (S2, S9 Dir 5.1, S12 CP.2 and CP.50, S13, S14, S17)
2. Atomics use sequentially consistent ordering by default. Any weaker ordering is justified in writing and reviewed. `volatile`-style qualifiers are never used for synchronization. (S9 Rule 21.25, S11 HIC++ 18.3.6, S12 CP.8, CP.100, CP.200, S16)
3. Shared writable state is minimized: prefer confinement, immutability, and passing data by value or by message. (S12 CP.3, CP.4, CP.31, S13)
4. There is a documented, acyclic global lock order. Code takes several locks at once only through a deadlock-avoiding primitive, and never relocks a non-recursive lock. (S1 CON35-C, S3 CON53-CPP and CON56-CPP, S4 LCK07-J, S9 Dir 5.2 and Rule 22.18, S11 HIC++ 18.3.2, S12 CP.21, S31)
5. No code calls unknown code (callbacks, overridable methods, user hooks) or blocks while holding a lock, and critical sections are short. (S12 CP.22 and CP.43, S4 LCK09-J)
6. Locks are released on every path, including errors and exceptions. Acquisition is scoped, and the thread that locks is the thread that unlocks. (S3 CON51-CPP, S4 LCK08-J, S12 CP.20, S9 Rules 22.16 and 22.17)
7. Every condition wait sits in a loop that tests a predicate, and notification preserves liveness. (S1 CON36-C, CON38-C, CON41-C, S3 CON54-CPP and CON55-CPP, S6 THI02-J and THI03-J, S12 CP.42, S9 Rule 22.19)
8. Every thread or task has an owner, and the owner joins it before the owner's scope ends. There is no detached or fire-and-forget work and no double join. (S12 CP.23 to CP.26, S1 CON39-C, S9 Rule 22.11, S20 to S23, S26)
9. Every failure in a child task reaches its owner. No task fails silently, and every thread entry point catches otherwise unhandled errors. (S7 TPS03-J, S11 A15-3-3, S22, S24, S25)
10. Cancellation is cooperative, propagates to all children, and is not swallowed. Every wait that can stall has a timeout or a cancellation path. (S6 THI04-J and THI05-J, S7 TPS02-J, S21, S24)
11. Asynchronous code does no blocking or long computation on an event-loop thread, and holds no lock across a suspension point. Every started operation is awaited or owned. (S12 CP.52, S24, S25, S27)
12. Queues and pools are bounded and apply backpressure. Interdependent tasks never share a bounded pool. (S7 TPS00-J and TPS01-J, S28)
13. Synchronization objects are initialized before use and destroyed only after every user has finished. Objects are fully constructed before they are shared. (S9 Rules 22.13 to 22.15 and 22.20, S1 CON31-C and CON34-C, S3 CON50-CPP, S5 TSM01-J and TSM03-J)
14. Verification of concurrent code combines methods, each with its limits stated: dynamic race detection on multithreaded tests, systematic or randomized schedule exploration, and, for critical protocols, a model-checked design. (S12 CP.9, S32 to S37, S41)
15. Results do not depend on scheduling unless the project declares that they may. Parallel random streams are keyed by logical task identity, not thread identity. Where bitwise identity is required, reductions use a fixed or order-independent order. (S44 to S47, S50)

## 1. Published rules in coding standards

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| CERT C CON | 13 rules, CON30-C to CON43-C. They cover thread-specific storage cleanup, not destroying a locked mutex, bit-field races, thread-safe library calls, storage duration of shared objects, lock ordering, spurious wakeups and failures in loops, no `signal()` in threads, condition-variable liveness, no double join or detach, one reference to an atomic per expression, and no data races. CON43-C is rated "Detectable: No." | Now hosted on the SEI GitHub site, copyright 2026 | S1, S2 |
| CERT C++ CON | CON50-CPP to CON56-CPP: mutex lifetime, release on exceptions, bit-fields, predefined lock order, spurious wakeups, condition-variable liveness, no speculative relock of a non-recursive mutex | Same | S3 |
| CERT Java LCK, VNA, TSM, THI, TPS | Generalizable: one lock order; release on exceptions; no blocking under a lock (LCK09-J); a group of atomic calls is not atomic (VNA03-J); no publishing of partly built objects (TSM03-J); wait in loops; terminable blocking threads, no forced stop (THI04-J, THI05-J); bounded pools without interdependent tasks; no silent task failure (TPS03-J); per-thread state reset in pools (TPS04-J) | Same | S4 to S8 |
| MISRA C:2023 | From Amendment 4 (announced March 2023). Dir 5.1 "There shall be no data races between threads." Dir 5.2 "There shall be no deadlocks between threads." Dir 5.3 "There shall be no dynamic thread creation." Rule 21.25: all memory synchronization operations sequentially consistent. Rules 22.11 to 22.20 cover single join or detach, access only through library functions, storage duration, initialization before access, destruction only after all users end, unlock by the locking thread, no recursive lock of a non-recursive mutex, one mutex per condition variable, and creating thread-specific storage before access. | Paywalled; titles from vendor documentation | S9, S10 |
| AUTOSAR C++14 (R19-03) | No concurrency chapter. Its HIC++ trace table marks HIC++ 18.x concurrency rules "Not yet analyzed... will be addressed in future." Among them: lock nesting forms a DAG (18.3.2), no relaxed atomics (18.3.6), one lock per shared datum (18.2.2), `call_once` rather than double-checked locking (18.2.4). A15-3-3 requires every task main function to catch all exceptions. Release 19-03 added an "obsolete statement." | Free from AUTOSAR; obsolete | S11 |
| MISRA C++:2023 | I found no open description of concurrency rules. | **[unverified]** | search |
| C++ Core Guidelines CP | CP.1 to CP.200. Model-neutral ones: assume code runs multithreaded, avoid races, minimize sharing, think in tasks, use tools (CP.9), scoped locks, multi-lock primitives, no unknown code under a lock, joining threads, no detach, wait with a condition, short critical sections, mutex declared with its data, no locks across coroutine suspension (CP.52), lock-free only when you must, no home-made double-checked locking | Dated Jun 14, 2026; "release 0.8" | S12 |
| JPL C standard (D-60411, 2009) | A search extract says it was written because MISRA C and the Power of Ten do not address multi-threading risks, and puts the threading rules at level LOC-2. I could not retrieve the rule text. | **[unverified]** | search |
| Rust | Data races are undefined behavior and impossible in safe Rust. Race conditions and deadlocks are not prevented and are "safe." `Send` and `Sync` are unsafe marker traits, and implementing them wrongly causes undefined behavior. | Current docs | S17 to S19 |
| Go and Java memory models | Both give sequential consistency to race-free programs (DRF-SC). Racy programs have bounded outcomes, unlike C and C++, but Go multiword races "can cause arbitrary memory corruption." Java `long` and `double` writes may tear. | Go 2022-06-06; Java SE 25 | S13, S14 |

Outcomes that recur across standards: race freedom, ordered locking, release on all paths, predicate loops around waits, owned thread lifetimes, and correct setup and teardown of synchronization objects.

## 2. Memory models

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Shared core | A data race is two conflicting accesses, at least one a write, not ordered by happens-before and not both atomic. C, C++, Java, Go, and Rust all define it this way. | Current | S2, S13 to S15, S17 |
| DRF-SC | Java: "If a program is correctly synchronized, then all executions of the program will appear to be sequentially consistent." Go states the same property. | Current | S13, S14 |
| Racy programs | C, C++, and Rust: undefined behavior. Java: limited outcomes, though causality rules are still needed to exclude "out of thin air" values. Go: torn values on multiword types. | Current | S13 to S15, S19 |
| Acquire and release | Writes before a release store are visible after the acquire load that reads it, but only between those two threads. Relaxed operations give atomicity only. `consume` is deprecated in C++26. | Current | S16 |
| Practice | Go: "Don't be clever." MISRA requires sequentially consistent atomics; HIC++ bans relaxed ones. | Current | S9, S11, S13 |

Practice that follows: design for race freedom, then reason only about sequentially consistent interleavings. Treat any weaker ordering as an expert exception with written justification.

## 3. Deadlock, livelock, starvation, priority inversion

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Lock ordering | All three CERT standards, MISRA Dir 5.2, and HIC++ (a DAG of lock nesting) require one global acquisition order. | Current | S1, S3, S4, S9, S11 |
| Unknown code under a lock | "If you don't know what a piece of code does, you are risking deadlock" (CP.22). LCK09-J forbids blocking while holding a lock. | Current | S4, S12 |
| Self-deadlock | 22% of deadlocks studied came from one thread acquiring a resource it already held. 97% of deadlocks involved two threads and at most two resources. | 2008 | S32 |
| Showing freedom from deadlock | Three published methods. (a) An ordering argument: a documented lock hierarchy plus a check, static or runtime. A runtime lock-order validator can show that no timing of the lock sequences it has observed can deadlock, but it covers only those sequences. (b) A protocol argument: the priority ceiling protocol prevents deadlock and bounds blocking to one lower-priority critical section. (c) A model-checked design. | 1990 to now | S29 (search), S31, S37 |
| Priority inversion | Mars Pathfinder suffered resets because a mutex was created with priority inheritance off. | 1997 | S30 (search) |
| Livelock and starvation | CERT requires liveness-preserving condition-variable use and terminable blocking threads. I found no standard rule naming livelock. | Current | S1, S6 |
| Message passing | It is not deadlock-free by construction. In 171 Go bugs, message passing caused more blocking bugs than shared memory, and Go's built-in deadlock detector found 2 of the reproduced blocking bugs. | 2019 | S33 |

## 4. Structured concurrency and lifecycle

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Principle | Spawning that outlives its caller is "goto"-like. A nursery cannot exit until all children finish, so resource cleanup holds, errors propagate (siblings cancelled, then re-raised), and cancellation reaches checkpoints. | 2018 essay | S22 |
| Python | `TaskGroup` cancels the remaining tasks on the first failure and raises an `ExceptionGroup`. `asyncio.timeout` turns cancellation into `TimeoutError`. Catching `CancelledError` without re-raising breaks structured concurrency. | Docs 3.15.1 | S24 |
| Java | JEP 543 finalizes structured concurrency, aiming to avoid thread leaks and cancellation delays and to show task trees in thread dumps. It is Integrated with target JDK 28, after seven previews (the seventh, JEP 533, in JDK 27). | 2026 | S23, search |
| Kotlin | Parents wait for children; cancellation recurses. | Current | S26 |
| Rust | Scoped threads are joined before `scope` returns, and a child panic propagates. | Since 1.63 | S20 |
| C++ | `jthread` joins on destruction and offers `stop_token` cooperative cancellation. CP.25 and CP.26 prefer joining threads and forbid `detach`. | C++20 | S12, S21 |
| Backpressure | The receiver should "not [be] forced to buffer arbitrary amounts of data." Use bounded pools for graceful degradation. | 1.0.4, 2022 | S7, S28 |

## 5. Asynchronous code

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Blocking on the loop | "Blocking (CPU-bound) code should not be called directly." It delays all tasks; offload it to an executor. Node.js treats a blocked loop as a fairness and denial-of-service risk, and recommends bounding input size, partitioning work, and offloading. | Current | S25, S27 |
| Lost tasks | The event loop keeps only weak references, so an unreferenced task "may get garbage collected at any time, even before it's done." | Current | S24 |
| Lost errors | An exception in a future that is never awaited surfaces only as a log line ("Task exception was never retrieved") at garbage collection. A coroutine that is never awaited triggers only a warning. | Current | S25 |
| Locks across suspension | CP.52: do not hold locks across suspension points. | 2026 | S12 |
| Thread affinity | Most event-loop objects are not thread-safe; cross-thread calls use a thread-safe entry. | Current | S25 |

## 6. Verification of concurrent code

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Why testing alone fails | Testing, compile-time checks, and run-time checks "are less effective at finding concurrency errors" than at finding sequential ones. | 2026 | S12 CP.9 |
| Bug shape | 97% of non-deadlock bugs were atomicity or order violations. 96% manifest under some order between 2 threads, and 92% under an order among at most 4 accesses. 34% involve several variables. 73% were not fixed by adding locks. | 105 bugs, 2008 | S32 |
| Happens-before detection | It reports only races in the executions it observes, and is effectively free of false positives. TSan costs 5 to 15 times in time and 5 to 10 times in memory, and uninstrumented code can hide races. In the Go study, 7 of 13 traditional races were detected, some only after about 100 runs. At Uber, more than 2,000 races were found and more than 1,000 fixed over 6 months. | Current; 2019; 2022 | S12, S33, S34, S41 |
| Lockset detection | Finds races outside the observed interleaving, but gives false alarms on fork-join and barrier idioms. | Secondary | S43 (search) |
| Systematic or randomized scheduling | PCT finds a bug of depth d with probability at least 1/(n·k^(d-1)) per run. On 49 benchmarks, PCT with d=3 found every bug the other methods found; a plain random scheduler beat preemption bounding; most bugs needed a bound of 1 or 2. Practical cost: nondeterminism must be removed and all synchronization controlled. | 2010; 2016 | S35, S36 (search) |
| Deterministic simulation | FoundationDB built a deterministic single-process simulator with fault injection before the database. | 2021 | S38 (search) |
| Record and replay | rr records and replays real workloads at low overhead, for "low-parallelism workloads" on specific CPU and OS features. | 2017 | S39 |
| Model checking designs | AWS applied TLA+ to 10 systems and found a data-loss bug whose shortest trace had 35 steps. That bug had passed design reviews, code reviews, and testing. | 2015 | S37 |
| Static and type-based | Annotation-based lock analysis finds missing locks at compile time but is intraprocedural, has no alias analysis, and gives false negatives. RacerD fixed more than 2,500 issues at Facebook, favoring high-confidence reports over proof of absence. Rust's type system excludes data races in safe code only. | Current; 2018 | S17, S40, S42 (search) |
| Practical for scientific teams | My synthesis: a race detector on multithreaded tests, randomized-schedule stress runs, the language's type or annotation checks, and model checking only for novel protocols. | Synthesis | S12, S35, S37 |

## 7. Reproducibility of concurrent scientific computation

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Reduction order | Floating-point non-associativity makes parallel results vary from run to run, and the variation accumulates in iterative methods. Deterministic alternatives to GPU atomics have measured costs. | 2024 | S47 |
| Existing corpus rule | STND.VVUQ.2 already requires a fixed or order-independent summation where bitwise identity is an acceptance criterion. Model-specific detail is in the sibling note. | 2026-10-22 | S50 |
| Counter-based generators | Keyed counter transformations pass BigCrush, give at least 2^64 streams with period 2^128 or more, and need little state. | SC11 | S44 |
| Stream requirements | Most applications need independent streams, sometimes millions of them. | 2017 | S45 (search) |
| Stream splitting | Spawn child streams from a seed sequence, use distinct keys for counter generators, or jump ahead without reuse. Deriving seeds as root plus worker id is "UNSAFE," because nearby root seeds overlap. | Current | S46 |
| Recommended practice | My synthesis: key each stream by a logical work identifier (sample, cell, ensemble member), not a thread id, and record the root seed. | Synthesis | S44, S46 |

## 8. What high-assurance practice adds

| Item | Finding | Standing or date | Source |
| --- | --- | --- | --- |
| Restricted subset | Ravenscar: library-level tasks only, created at startup; protected objects with at most one entry and one queued caller; no abort, select, requeue, relative delay, dynamic priorities, task termination, or implicit heap; FIFO-within-priorities dispatching with ceiling locking. | 2003 guide; profile in the Ada standard | S48 |
| Purpose | "determinism, schedulability analysis and memory-boundedness," a small certifiable run time, and support for static analysis, including model checking | 2003 | S48 |
| Deadlock by construction | Ceiling locking "assures absence of deadlocks" and gives a near-optimal bound on blocking time. | 2003 | S48 |
| Static task set | Schedulability analysis requires a static task set with dependencies only through protected objects. MISRA Dir 5.3 is the C analog. | Current | S9, S48 |
| Partitioning | ARINC 653: each partition has its own address space; partitions run in fixed windows of a cyclic major frame; inter-partition communication is supervised. | Paywalled; secondary | S49 (search) |

## Outcomes a standard could require

1. Every shared mutable object has a declared protection, and a reviewer can confirm that every access respects it. (S2, S9, S13, S14)
2. Atomics are sequentially consistent unless a written justification is approved. (S9, S11, S16)
3. The project documents an acyclic lock order and shows that code follows it, by a check or by an argument. (S1, S9, S31, S32)
4. No lock is held across a call to unknown code, a blocking operation, or a suspension point. (S4, S12)
5. Locks and other resources are released on all exit paths. (S3, S4, S12)
6. Every wait tests its predicate in a loop. (S1, S6, S12)
7. Every started thread or task has an owner that waits for it before the owner exits. (S12, S20 to S23)
8. Every child failure reaches its owner, and no task fails silently. (S7, S11, S24)
9. Cancellation propagates to children and is not suppressed, and every blocking wait has a bound or a cancellation path. (S6, S21, S24)
10. Event-loop threads never perform blocking or unbounded computation. (S25, S27)
11. Queues and pools are bounded, with a defined overload behavior. (S7, S28)
12. Synchronization objects outlive every user, and objects are fully built before they are shared. (S5, S9)
13. Library calls made from concurrent code are documented as thread-safe or serialized. (S1 CON33-C)
14. Concurrency verification evidence names its methods and their blind spots: races found only in observed runs, schedules explored, or a model's bounds. (S12, S35, S37, S41)
15. Critical synchronization protocols have a checked design model or a protocol argument for safety and liveness. (S29, S37, S48)
16. The project states whether results may vary with scheduling. Where they may not, random streams are keyed by logical work identity and reductions have a fixed or order-independent order. (S44, S46, S47, S50)
17. For the highest integrity level, the task set is static and created at startup, locking follows a protocol with bounded blocking, and timing is analyzable. (S9, S48)

## Unverified

- MISRA C++:2023 concurrency rules: no open description found.
- JPL D-60411 LOC-2 tasking rules: the owner's host timed out, so the rule text is not confirmed.
- MISRA C:2023 rule titles come from a vendor's pages, not the MISRA text. The vendor's MISRA C:2012 numbering of Rule 22.16 differs from other sources.
- S29, S30, S35, S36, S38, S42, S43, S45, and S49 rest on search extracts only.
- JEP 543's final release (JDK 28) has not shipped as of the access date.
- Ravenscar restrictions come from the 2003 guide, since Ada RM D.13 could not be fetched; the current standard may differ.
- The scientific-team practice and logical-identity RNG keying are my synthesis.

## Sources

| ID | URL | What it supports |
| --- | --- | --- |
| S1 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/concurrency-con/ | CERT C CON list |
| S2 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/concurrency-con/con43-c/ | CON43-C, not detectable |
| S3 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-cpp-coding-standard/rules/concurrency-con/ | CERT C++ CON |
| S4 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/rules/locking-lck/ | LCK |
| S5 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/rules/thread-safety-miscellaneous-tsm/ | TSM |
| S6 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/rules/thread-apis-thi/ | THI |
| S7 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/rules/thread-pools-tps/ | TPS |
| S8 | https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/rules/visibility-and-atomicity-vna/ | VNA |
| S9 | https://www.mathworks.com/help/bugfinder/ref/misrac2023d5.1.html (and d5.2, d5.3, rule21.25, rule22.11 to rule22.20) | MISRA C:2023 titles (vendor) |
| S10 | https://ldra.com/ldra-blog/misra-c2012-amendment-4/ | Amendment 4 scope |
| S11 | https://www.autosar.org/fileadmin/standards/R19-03/AP/AUTOSAR_RS_CPP14Guidelines.pdf | AUTOSAR; HIC++ trace |
| S12 | https://raw.githubusercontent.com/isocpp/CppCoreGuidelines/master/CppCoreGuidelines.md | CP rules |
| S13 | https://go.dev/ref/mem | Go model, DRF-SC |
| S14 | https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html | Java model |
| S15 | https://en.cppreference.com/w/cpp/language/multithread.html | C++ race, progress |
| S16 | https://en.cppreference.com/w/cpp/atomic/memory_order.html | Orderings |
| S17 | https://doc.rust-lang.org/nomicon/races.html | Rust races |
| S18 | https://doc.rust-lang.org/nomicon/send-and-sync.html | Send, Sync |
| S19 | https://doc.rust-lang.org/reference/behavior-considered-undefined.html | Races are UB |
| S20 | https://doc.rust-lang.org/std/thread/fn.scope.html | Scoped threads |
| S21 | https://en.cppreference.com/w/cpp/thread/jthread.html | jthread, stop_token |
| S22 | https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/ | Nurseries |
| S23 | https://openjdk.org/jeps/543 | Java structured concurrency |
| S24 | https://docs.python.org/3/library/asyncio-task.html | TaskGroup, cancellation |
| S25 | https://docs.python.org/3/library/asyncio-dev.html | Blocking, lost errors |
| S26 | https://kotlinlang.org/docs/coroutines-basics.html | Kotlin scopes |
| S27 | https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop | Event-loop blocking |
| S28 | https://www.reactive-streams.org/ | Backpressure |
| S29 | https://www.math.unipd.it/~tullio/RTS/2009/SRL-1990.pdf (search only) | Priority ceiling |
| S30 | https://www.cs.unc.edu/~anderson/teach/comp790/papers/mars_pathfinder_long_version.html (search only) | Pathfinder |
| S31 | https://docs.kernel.org/locking/lockdep-design.html | Lock-order validation |
| S32 | https://www.cs.columbia.edu/~junfeng/10fa-e6998/papers/concurrency-bugs.pdf | Lu et al. 2008 |
| S33 | https://songlh.github.io/paper/go-study.pdf | Tu et al. 2019 |
| S34 | https://arxiv.org/abs/2204.00764 | Uber race study |
| S35 | https://multicore.doc.ic.ac.uk/publications/topc-16.html (search only) | SCT empirical study |
| S36 | https://www.microsoft.com/en-us/research/?p=158870 (search only) | PCT |
| S37 | https://cdn.amazon.science/67/f9/92733d574c11ba1a11bd08bfb8ae/how-amazon-web-services-uses-formal-methods.pdf | TLA+ at AWS |
| S38 | https://cacm.acm.org/?p=227399 (search only) | FoundationDB simulation |
| S39 | https://arxiv.org/abs/1705.05937 | rr |
| S40 | https://clang.llvm.org/docs/ThreadSafetyAnalysis.html | Annotation analysis |
| S41 | https://clang.llvm.org/docs/ThreadSanitizer.html | TSan limits |
| S42 | https://research.facebook.com/publications/racerd-compositional-static-race-detection/ (search only) | RacerD |
| S43 | https://www.cs.williams.edu/~freund/papers/10-cacm.pdf (search only) | Lockset vs happens-before |
| S44 | https://www.thesalmons.org/john/random123/papers/random123sc11.pdf | Counter-based RNG |
| S45 | https://www.gerad.ca/papers/G-2015-35.pdf (search only) | Parallel RNG requirements |
| S46 | https://numpy.org/doc/stable/reference/random/parallel.html | Stream splitting |
| S47 | https://arxiv.org/abs/2408.05148 | Reduction variability |
| S48 | https://cs.york.ac.uk/rts/static/papers/R:Burns:2003.pdf | Ravenscar guide |
| S49 | https://en.wikipedia.org/wiki/ARINC_653 (search only) | ARINC 653 overview |
| S50 | /home/brianm/projects/utils/governance-ledger109/research/parallel-models.md section 3.4 | Corpus reduction rule |
