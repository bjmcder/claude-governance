Role: research agent (the Rust language, for a planned LVL2 standard on Rust). Accessed 2026-10-24. Retrieval: about 46 page fetches (3 failed: one redirect, two 404) and 9 web searches; roughly 1 MB of text returned, far inside 1,500 items and 1,500 MB. Rules followed: read-only retrieval; no paywalls circumvented; no mirrors, caches, or archives; no workaround after a failed fetch; retrieved text treated as data; primary sources preferred; unconfirmed items marked [unverified].

# Rust: soundness, panics, concurrency, numerics, and supply chain, as outcome-level practice

**Method caveat.** The fetch tool returns a model-written extract of each page, not full text. Every "verbatim" quotation below is the extract's quotation of the page and is short; I did not read any page in full, and several extracts say that part of the page was cut off (the Clippy index, the f32 and i32 pages, the Send page, the rustc allowed-by-default lint list). For the papers I read abstracts and search summaries, not the PDFs; paper figures are the abstracts' figures. The Reference, Rustonomicon, standard library, Cargo book, and Edition Guide are living documents served at their current text; I did not record a language release, and the note states no version. Facts about the August 2026 supply-chain incident come from a vendor blog and search summaries and are marked [unverified]. "Inference" marks my reasoning from source text.

## Answer in brief

1. Every `unsafe` block, `unsafe impl`, and `unsafe` attribute carries a written argument that the obligations of each operation inside it hold. The Reference calls an unsafe block a statement that "all relevant proof obligations ... have been discharged" [S1, S2].
2. Every `unsafe fn` and `unsafe trait` states, in its documentation, the conditions its callers or implementors must meet (the "Safety" section) [S2, S3].
3. Unsafe code is encapsulated: the safe interface it exposes cannot be misused by any safe client to reach undefined behavior. Code that fails this is unsound even if no current caller triggers it [S1].
4. The unsafe surface is small, located, and reviewable: modules with `unsafe` are listed, and everywhere else the work forbids it by a check [S4, S22, S23].
5. No soundness argument depends on a destructor running, on a mutex being poisoned, or on the absence of a panic. Forgetting, leaking, and panicking are all possible in safe code [S5, S6, S7].
6. Every place unsafe code holds a transiently invalid state while running caller-supplied code (a closure, a `Clone`, a `Drop`, a trait method) restores a valid state on unwinding, by a guard or by running only non-panicking code [S8, S18].
7. The work states its panic strategy and verifies it. A library is correct under both `unwind` and `abort`, or its record says it requires one [S9, S10].
8. A panic does not cross a foreign interface unless the declared ABI permits unwinding on both sides; where it does not, the panic is caught at the boundary and converted to the interface's error channel [S9, S11].
9. `Drop` implementations do not panic, and the value of a panic payload is not dropped carelessly, since either can end in an abort [S12, S13].
10. Manual `Send` or `Sync` implementations carry a safety comment that names the invariant making cross-thread transfer or sharing sound, with bounds on type parameters [S14, S15].
11. Safe code is race-free in the data-race sense by construction; the work still argues the absence of race conditions (ordering, atomicity of check-then-act, deadlock) as it would in any language [S16, S17].
12. Async code is written so that a drop at any `.await` leaves every invariant restored; each future that is not cancellation safe is documented as such [S19, S20, S21].
13. No lock whose guard is not async-aware is held across an `.await`, and no blocking call runs on an executor thread [S19, S22, S21].
14. The async runtime and its scheduler are configuration chosen at the application boundary, not baked into library code [S19].
15. Arithmetic whose overflow would be a defect either uses an explicit checked, saturating, or wrapping operation by name, or is shown to stay in range; the build profile does not change what the program computes [S23, S24, S25].
16. Failures that a caller can handle are returned as `Result`; `unwrap` and `expect` in library code appear only where the code establishes that the failure is impossible, with the reason stated [S26, S27].
17. Types at a C or C++ interface have a defined layout, nullable pointers use an option form, and each resource has one stated owner on each side of the boundary [S11, S28].
18. The minimum supported toolchain and the edition are declared in the manifest and checked at each change; a build on an older toolchain fails with a clear message [S29, S30].
19. The lockfile is committed where the build is meant to be reproducible; each dependency, feature, build script, and procedural macro is treated as code that runs with the builder's authority [S31, S32, S33, S34].
20. Tests of unsafe code run under an interpreter or sanitizer that detects undefined behavior, and the record states what that run does not establish [S35, S36].
21. Floating-point results do not depend on NaN bit patterns, on the precision of library transcendental functions, or on a rounding mode the program changed [S37, S38].
22. Code that selects a vector instruction set checks at run time that the processor supports it, or the build is restricted to processors that do [S38].

## What the corpus already holds

The drafter should cite these and restate none of them. Titles and sentences are from `REPO/rendered/`.

| Matter | Provision | What it already requires |
|---|---|---|
| Static checks, formatter, suppression with reason | STND.CODE.4, STND.CODE.5 | The repository configuration names static checks and the layout tool; each change passes them; an unresolved finding is suppressed at its location with its reason. This covers lints and formatters for Rust without a Rust clause. |
| Input checks no setting removes | STND.CODE.6; STND.CXX.18 | Binding. A check of untrusted input cannot be removed by an execution setting. This is the exact home of "overflow checks off in release": a Rust clause need only apply it to arithmetic on untrusted input. STND.JL.17 does the same with checked integer arithmetic. |
| Failures PRIME.4 lists are not discarded | STND.CODE.7, STND.CODE.12; STND.PY.22; STND.CXX.16, STND.CXX.17 | Binding for the listed failures. Rust's `Result` and `#[must_use]` map onto STND.CXX.17 (a call that ignores the result is diagnosed); a Rust response clause would copy STND.CXX.16 with "return a `Result`", "panic", and so on. |
| Contracts at declarations | STND.CODE.3 | A "Safety", "Errors", and "Panics" section is an instance; no new provision is needed. |
| Edition, build settings, stated in the repository | STND.CXX.2, STND.CXX.4 (edition, language extensions, floating-point options, target instruction set); STND.JL.1 to STND.JL.5 (reference version, compatibility bounds, checked versions, committed manifests, run settings); STND.PY.13, STND.PY.14 | Edition and minimum toolchain are the Rust counterparts of these. The model is STND.JL.2 and STND.JL.3: a declared bound and a check on the declared releases. |
| Toolchain revision as a result input | STND.DEPS.8 | The compiler revision is recorded as an input of each result. |
| Dependencies | STND.DEPS.1 to STND.DEPS.11 | Selection criteria, thin support, pinned-revision review, contract tests on update, digest verification (binding, STND.DEPS.6), advisories before release (binding, STND.DEPS.7), package files with lock files as the dependency record (STND.DEPS.10). The lockfile, advisory database, and registry are all covered; build scripts and procedural macros as code that executes at build time are not named. |
| Shared state, ordering | STND.CONC.3 (one stated protection per shared mutable object), STND.CONC.4 (atomic ordering justified), STND.CONC.5 (publication and lifetimes), STND.CONC.6 (concurrent calls in contracts); STND.CXX.23; STND.JL.27 | A manual `Send` or `Sync` implementation is the Rust form of "stated protection" and a safety argument; STND.CONC.3 already asks for it at the declaration. |
| Locks and waits | STND.CONC.7 (acyclic order), STND.CONC.8 (while holding a lock: no suspension point; release on every path, failures included), STND.CONC.9, STND.CONC.10, STND.CONC.11 | STND.CONC.8 already forbids a suspension point under a lock. Holding a guard across `.await` is a direct instance. |
| Cancellation, event loops, migration | STND.CONC.12 (parent-owned tasks), STND.CONC.13 (cancellation propagation, resources released, observed at stated points), STND.CONC.15 (return to the loop within a bound), STND.CONC.16 (state stays with the task, not the thread) | Cancellation at an await point, blocking an executor thread, and thread-local state under task migration are covered at the level of outcome. Rust adds the drop-as-cancellation mechanism and the lack of a marker for cancellation safety. |
| Failures across tasks | STND.CONC.1, STND.CONC.2 | A panicked spawned thread or task, joined or detached, is an instance. |
| Verification of concurrency | STND.CONC.24 to STND.CONC.28 | Task-count tests, run-time concurrency checks, varied schedules, stated verification limits, checked design of critical protocols. A schedule-exploring checker for Rust fits STND.CONC.26 and STND.CONC.28. |
| Run-time error detection | STND.CXX.26 | Tests run in a build that detects invalid memory accesses and each kind of undefined behavior the repository lists, and race detection when threads are used. This is the home for an interpreter or sanitizer run of unsafe Rust; a Rust version would cite it. |
| Compiler assumptions | STND.CXX.24 | Each assumption stated to the compiler is established by a check or recorded proof. The Rust analogue is `unreachable_unchecked`, `assert_unchecked`, and every `unchecked_*` arithmetic method. |
| Foreign boundaries | STND.CXX.20 (foreign resource handles; do not release what the interface predefines or another component owns), STND.CXX.22 (exceptions caught within code that a foreign interface invokes; converted to the interface's error or stored and checked after return) | Both transfer almost word for word: a `Drop` handle for a foreign resource, and `catch_unwind` at an `extern` boundary. |
| Numerics | NUMER.5 (precision and delivered arithmetic recorded), NUMER.12 (rounding), NUMER.16 (approximations listed); STND.CXX.4 (floating-point and instruction-set options); STND.JL.19 (subnormal flushing scope) | Float semantics are covered at the level of result; the Rust-specific facts (NaN payloads, unspecified library precision, `mul_add`) are inputs to NUMER.5 and need no restatement. |
| Documentation | STND.DOCS.13 (checked examples) | Rust documentation examples that are compiled and run among checks are an instance. |

**Gaps the sources show and the corpus does not hold.**
- Safety arguments for `unsafe` blocks, `unsafe fn`, `unsafe trait`, and `unsafe impl`, and encapsulation (soundness). No existing provision speaks of a proof obligation discharged at a language construct. STND.CXX.24 is the nearest.
- Panic strategy as a build setting that changes what code means, and what a library must be correct under (STND.CXX.19 is the exception analogue for C++; its Rust form differs because panics can abort).
- Panic safety of unsafe code that calls caller code.
- Poisoning as advisory, not a soundness mechanism.
- Build scripts and procedural macros as code executing at build time (STND.DEPS has the lockfile and digests but not this).
- Cancellation safety as a property of each future with no compiler marker.
- Explicit integer-arithmetic form as a named operation, beyond STND.JL.17's untrusted-input case.
- Foreign-interface layout and unwinding ABI.

## 1. Unsafe code and soundness

| Hazard | Source fact | Failure | Practice as an outcome | Sources | Holds across versions? |
|---|---|---|---|---|---|
| Unsafe obligations | "`unsafe` only means that avoiding undefined behavior is on the programmer"; code that is safe for "any safe client" is sound, otherwise unsound (Reference). An unsafe block "states that all relevant proof obligations ... have been discharged" | Unsound library; a safe caller reaches UB | Each unsafe block has an argument, in a comment at the block, that each obligation of each operation inside it holds. Each unsafe function documents its conditions | S1, S2 | Concept holds; the unsafe operation list moves |
| Documentation of conditions | Unsafe traits and functions "should come with documentation explaining what those extra safety conditions are"; the API guidelines ask for a "Safety" section that "explains all invariants", and for "Errors" and "Panics" sections | Callers guess | Every public `unsafe fn` and `unsafe trait` has a Safety section that a reviewer can check against the body | S2, S3 | Holds |
| Unsafe body of unsafe fn | By default the body of an `unsafe fn` is itself an unsafe block; a lint can require explicit blocks | Obligations inside the function are not individually argued | Unsafe operations in an unsafe function sit in their own blocks, each with its argument (outcome of the lint) | S2 | The default has moved across editions [unverified which]; the outcome holds |
| No formal model | "There is no formal model of Rust's semantics for what is and is not allowed in unsafe code"; the list of UB "may grow or shrink" | A program tested today is declared UB later | Unsafe code is justified against the documented rules and the stricter reading of any aliasing model in dispute, and the record names which model a check used | S1, S35 | Moving: the model is still being settled; the practice holds |
| Aliasing | `&mut T` must not be read or written by a pointer not derived from it while live; `&T` must not be mutated outside `UnsafeCell`; "exact aliasing rules are not determined yet" | Optimizer miscompiles code that worked | Raw-pointer code derives each pointer from a live reference or allocation and does not create a second `&mut` to the same bytes; an interpreter checks it | S1, S35, S36 | Rules specific to version; outcome holds |
| Invalid values | Producing an invalid value (a `bool` not 0 or 1, a null reference, a bad enum discriminant, uninitialized integer) "is hence immediate UB"; reading uninitialized memory is allowed only in unions and padding | UB without any access | Uninitialized data lives in `MaybeUninit` until written; `zeroed` and `transmute` appear only for types whose all-zero or source bit pattern is valid, stated at the site | S1, S39 | Holds |
| Dangling, misaligned | UB when a dangling or misaligned place is loaded or stored; reference to it is invalid | Memory corruption | Raw pointers carry the argument for allocation, bounds, alignment, and initialization at each dereference | S1 | Holds |
| Forget and leak | `mem::forget` is safe because destructors are not guaranteed; "any `unsafe` code you write must allow for this possibility" | A guard that restores an invariant on drop never runs | Soundness does not depend on a destructor running; invariants that matter are restored by the code before a value can escape | S5 | Holds |
| Target features | Executing code compiled with unsupported platform features is UB; `-C target-feature` is itself unsafe | Illegal instruction or silent wrong code | See section 11 | S1, S38, S29 | Holds |
| Unsafe attributes | Attributes with extra conditions (`no_mangle`) must be wrapped `unsafe(..)` | Symbol clash is UB | Each such attribute has an argument of non-collision | S2 | Syntax moved with edition |

Encapsulation is the basis of the Rust safety claim. RustBelt proves, for a subset of Rust, that safe code is safe and states "what verification condition" each library with unsafe code "must satisfy in order for it to be deemed a safe extension"; it verified `Arc`, `Rc`, `Cell`, `RefCell`, `Mutex`, `RwLock`, and others (abstract, via a summary) [S40]. This is the source for a requirement that unsafe be argued at the module boundary, not at each block alone.

## 2. Undefined behavior: what safe code excludes

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Safe code is free of UB | "If all you do is write Safe Rust, you will never have to worry about type-safety or memory-safety" (Nomicon) | Over-trust: the guarantee is conditional on every unsafe dependency being sound | The work lists the unsafe code in the work and in its dependencies that it relies on; "safe" claims name that dependency | S4, S22, S23 | Holds |
| Not UB | The Reference lists deadlocks, leaks, exiting without calling destructors as "not considered unsafe", and integer overflow as a programmer "error" with defined results | Treating these as handled | The work argues them as it would in any language | S41, S24 | Holds |
| Overflow is not UB, but `unchecked_*` is | `unchecked_add` "results in undefined behavior" when `checked_add` would return `None` | Silent corruption through an optimizer assumption | Every `unchecked` operation is an unsafe block with the range argument, as STND.CXX.24 asks for assumptions | S25 | Holds |
| Float to integer cast | Saturates; `NaN` gives 0 | Silent clamp | Casts of untrusted floats check range and NaN first | S23 | Holds |
| Slice index, divide by zero | Panic, not UB | Denial of service | See section 3 | S23 | Holds |
| Studies of defects | In 186 memory-safety bug reports through 2020, "all memory-safety bugs require unsafe code", and many are "mild soundness issues" that leave a possibility but no live bug (Xu et al.). Of 170 bugs in the PLDI 2020 study, all memory-safety bugs involved unsafe code (abstract: the study examined 850 unsafe usages and 170 bugs) [unverified: the abstract summary I read does not state this conclusion for the 170] | The claim is conditional, not absolute | Evidence for the encapsulation practice: the defect lives at the unsafe boundary | S42, S43 | Empirical, 2020 corpora |

## 3. Panics

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Panic strategy | `-C panic` selects `unwind` or `abort` (default depends on target); with `abort` "the optimizer may assume that unwinding across Rust frames is impossible" | Code that relies on `catch_unwind` or on `Drop` after a panic silently does nothing | The panic strategy of each build is recorded in the repository configuration, and tests run under every strategy the work ships under | S9, S10 | The set of strategies moves (an immediate-abort form exists in the rustc option list I read); the practice holds |
| `catch_unwind` | "It is **not** recommended ... for a general try/catch mechanism"; "might not catch all Rust panics" | Error handling by panic | `catch_unwind` appears at boundaries (thread roots, foreign interfaces), not for control flow | S12 | Holds |
| Panic in `drop` | "`drop()` may itself be called during unwinding ... if the `drop()` panics in that situation (a 'double panic') this will likely abort the program"; most types "should simply clean up ... and return normally" | Abort mid-recovery; leaked resources | `Drop` bodies do not panic and do not call code that can | S13 | Holds |
| Payload drop | Dropping the `Err` payload of `catch_unwind` "may in turn panic" | Abort at the boundary | Payload is inspected or forwarded, not dropped casually | S12 | Holds |
| Panics across a foreign interface | Wrong ABI: unwinding into Rust from a non-unwinding `extern` is UB; the other direction, a panic reaching a non-unwinding ABI boundary, "will cause the process to safely abort"; catching a foreign exception with `catch_unwind` is UB (Nomicon) or "unspecified: aborts or returns an opaque Err" (Reference) | Process abort or UB | Every `extern` function that Rust exports, and every callback, either cannot panic (caught inside) or uses the unwinding ABI on both sides; the other language's exceptions never enter Rust frames | S9, S11 | The ABI strings are specific; the outcome holds. The two sources differ on foreign-exception catching; I record both |
| Thread panic | Join returns `Err` with the payload; a dropped handle detaches the thread | Panic lost; resource leak | Every spawned thread's result is observed or its loss is argued (STND.CONC.1, STND.CONC.2) | S44 | Holds |
| Poisoning | "Poisoning is only advisory"; "`unsafe` code cannot rely on poisoning for soundness"; double panic in a drop leaves the mutex unpoisoned; foreign exceptions do not poison; `RwLock` poisons only on a writer panic | Invariant violated, lock looks healthy; or recoverable state refused | Code states whether a poisoned lock is propagated (usual `unwrap`) or recovered after the invariant is re-established (`clear_poison`, `into_inner`); no soundness argument rests on poison | S6, S45 | Holds; API names move |
| Panic safety of unsafe code | "Clone is completely out of our control, and is totally free to panic" ... "uninitialized memory will be read!"; require "minimal exception safety" in unsafe code | Double free; read of uninitialized memory | Between creating a transient invalid state and restoring it, only non-panicking code runs, or a guard restores it | S8, S46 | Holds |
| Debug-only panic sources | "On debug builds, every arithmetic operation can panic if it overflows" | Tested in one profile, shipped in another | See section 6 | S8, S24 | Holds |

Panic safety is also the first pattern of the tool Rudra: "user-supplied closure or trait method panics partway through" after `ptr::read` duplicates ownership [S46].

## 4. Send and Sync, data races, race conditions

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Auto traits | Send and Sync are "unsafe traits ... other unsafe code can assume that they are correctly implemented"; auto-derived from fields; "Incorrectly implementing Send or Sync can cause Undefined Behavior" | A wrapper of a raw pointer is silently not Send, so the author writes `unsafe impl` and gets it wrong | Each `unsafe impl Send` or `Sync` has a comment that names the invariant (unique ownership, internal synchronization) and bounds on type parameters (`T: Send`) | S14, S15 | Holds |
| Variance bugs | Rudra's third pattern: "a generic type implements Send or Sync without requiring the correct bounds on its type parameter" | Data race on a type the caller thinks safe | Reviewers and checks compare each manual impl's bounds with the contained types | S46 | Holds |
| Examples of types not Send | `Rc` (non-atomic count); `MutexGuard` "must not implement Send" (release on the acquiring thread); `NonNull` not Send as data "may be aliased" | A guard moved to another thread | Types that hold thread-affine resources (guards, thread-local handles) are not made Send | S15 | Platform detail specific |
| Data race | "Safe Rust guarantees an absence of data races ... A data race has Undefined Behavior"; defined as concurrent, one a write, one unsynchronized | UB in unsafe code | Unsafe code that shares data between threads orders every conflicting access by atomics or a lock; mixed-size atomic access to the same bytes is also UB | S16, S47 | Holds |
| Race condition | "Rust does not prevent general race conditions"; "a race condition cannot violate memory safety ... on its own"; "in conjunction with some other unsafe code" it can | Check-then-act on an atomic index, then `get_unchecked` | Unsafe code does not take its bounds or validity from a value another thread may change after the check | S16 | Holds |
| Deadlock | Not considered unsafe; re-locking a held `Mutex` or `RwLock` "might panic" or deadlock; `RwLock` priority policy is unspecified, so a second `read` can deadlock behind a waiting writer | Hang | See STND.CONC.7 and STND.CONC.8; no recursive locking; no assumption of reader priority | S6, S45 | Holds |
| Memory model | Atomics "follow the same rules as C++20 atomics ... without the 'consume' memory ordering" | `Relaxed` used for publication | STND.CONC.4 applies; Rust adds no weaker model | S47 | Specific to the C++ model of the day [unverified whether this is fixed] |
| Study | Qin et al. (PLDI 2020) examined concurrency bugs among their 170; tools they built found previously unknown ones [abstract only; details unverified] | | | S43 | Empirical |

## 5. Async

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Futures are inert | "Futures alone are inert; they must be actively polled"; `poll` "should not block"; a completed future "may panic, block forever" if polled again, but never cause UB | A future built and never awaited does nothing | Each future is awaited, spawned, or deliberately dropped; STND.CONC.1 (asynchronous completion observed) applies | S48 | Holds |
| Cancellation by drop | Dropping a future stops it at an `.await`; the Oxide guidance calls this "an undocumented behavior" and every `.await` "can be a point where the function returns"; there is no marker for cancellation safety | A lock released with the protected state `None`; lost partial reads; lost place in a queue | Each async function states whether it is cancellation safe; a function that is not is never in a `select!` loop or under a timeout without a recorded argument; invariants broken across an `.await` are restored by a guard | S19, S49 | Holds; async drop is unstable and its status moves |
| Cancel safety, tokio | "If you have a future that has not yet completed, then it must be a no-op to drop that future and recreate it"; `recv` and `accept` listed safe, `read_exact`, `write_all`, `Mutex::lock` not | Data loss in `select!` loops | Library futures are used as their documentation classifies them | S19 | Specific to the library |
| Lock across await | `await_holding_lock` and `await_holding_refcell_ref` lints exist; a guard of the standard mutex is not Send; Oxide calls an async mutex across `.await` "risky" | Deadlock, a future that is not Send, borrow panics | STND.CONC.8 already forbids a suspension point under a lock; the outcome here is that the check is mechanical (a lint) | S19, S22, S49 | Holds |
| Blocking in async | "if one branch blocks the thread, all other expressions will be unable to continue"; blocking work belongs on `spawn_blocking` or a pool; CPU-bound work on a dedicated pool | Executor starvation | STND.CONC.15; blocking calls are named and moved off the executor | S19, S21 | Holds |
| Runtime choice | The runtime is a feature-selected library (`rt` versus `rt-multi-thread`); `std` defines only the `Future` and `Waker` interface | Library code that spawns on a particular runtime cannot be used under another; a thread-local assumption breaks under work stealing | The runtime and its thread count are chosen by the application and recorded as configuration (STND.CONC.17, STND.CONC.18, STND.CONC.21); libraries take executors or return futures; per-task state does not use thread-local state (STND.CONC.16) | S19, S48 | Holds |
| `Send` futures | A future held across `.await` with a non-Send value is not Send | Cannot be spawned on a multi-thread scheduler | Same as guard rule | S19 [inference] | Holds |

## 6. Integer overflow and explicit arithmetic

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Profile-dependent behavior | "Integer operators will panic when they overflow when compiled in debug mode." Other builds "may result in panics or silently wrapped values ... at the implementation's discretion"; wrapping uses two's complement. `-C overflow-checks` defaults on only when debug assertions are on | A program that passes tests in debug wraps in release | The work states `overflow-checks` for each build in the repository configuration; STND.CODE.6 and STND.CXX.18 forbid a setting from removing a check of untrusted input | S23, S24, S10 | Holds as default behavior; stated in the Reference as implementation choice |
| Always-checked cases | Signed `MIN / -1` and `MIN % -1` panic "even when `-C overflow-checks` is disabled"; division by zero panics; shifts by at least the width are overflow | Silent difference | Not a practice; a fact for the author | S23 | Specific |
| Explicit operations | `checked_*` (returns `None`), `wrapping_*`, `saturating_*`, `overflowing_*`, `strict_*` ("always panic on overflow, regardless of whether overflow checks are enabled"), and `Wrapping<T>` | Intent invisible | Arithmetic where overflow is intended wraps by a named operation; arithmetic where it is an error uses `checked_*` or `strict_*` or is argued to be in range; hashing and PRNG code uses the wrapping form on purpose | S24, S25 | `strict_*` is a newer addition [unverified when]; the others are old |
| Casts | `as` truncates between integers; `cast_possible_truncation` is a pedantic lint recommending `try_from` | Silent truncation | Narrowing conversions of untrusted values use the fallible form | S22, S23 | Holds |
| Lint | `arithmetic_side_effects` is a restriction lint (allow by default) that flags overflow-capable arithmetic | Noise if enabled everywhere | Enabled for code that handles untrusted input; the repository configuration says where (STND.CODE.4) | S22 | Lint names move |

## 7. Error handling

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Return versus panic | "returning `Result` is a good default choice"; panic when "an assumption, guarantee, contract, or invariant has been broken" by the caller; for expected failure "more appropriate to return a `Result`" | Library panics on bad data from a file; or returns errors for caller bugs | Failures a caller can cause by data and can handle are returned; violation of a documented precondition may panic, and the documentation says so ("Panics" section) | S26, S3 | Holds |
| `unwrap`, `expect` | Fine in tests and examples; acceptable when manual inspection shows no `Err` and the argument text gives the reason | A panic in a library at runtime from outside input | In library code, each `unwrap` or `expect` carries a reason that the failure cannot occur; none is applied to untrusted input | S26, S3 | Holds |
| `?` and error types | The API guidelines prefer `?` in examples because "unwrapping an error should be a conscious decision"; errors documented in an "Errors" section | Lost context | Error types carry the cause; STND.CODE.7 applies to the listed failures: a `Result` is not discarded (compiler warns on an unused `Result`: a `#[must_use]` fact I did not retrieve [unverified]) | S3 | Holds |
| Lints | `unwrap_used`, `expect_used`, `indexing_slicing`, `panic_in_result_fn` exist in Clippy's restriction family [unverified: not retrieved] | | | S22 | Names move |
| Panic as failure channel | STND.CXX.16-style list: return, halt with diagnosis, safe state, visible degradation | | A Rust response clause names panic as "halt with a diagnosis" only where the panic strategy makes it so (`abort`) or a handler turns it into a diagnosis | S9 [inference] | |

## 8. Interfaces to C and C++

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Layout | Layout compatible with C "only if the `#[repr(C)]` attribute is applied"; `repr(C)` also for enums | Field order differs from the C struct | Each type crossing the boundary is `repr(C)` (or `repr(transparent)`, inference) and its layout is compared with the C declaration by a compile-time assertion or a test | S28 | Holds |
| ABI | The C ABI is default; some targets differ; wrong call ABI is UB | Crash | The ABI string is stated at each declaration | S1, S28 | Holds |
| Nulls | References, `Box`, `fn` pointers are never null; "trying to construct ... these invalid values is undefined behavior"; use `Option<extern "C" fn>` | UB on null from C | Pointers from C are received as raw or `Option` types and checked before conversion to a reference | S28 | Holds |
| Ownership | "Foreign libraries often hand off ownership ... we must use Rust's destructors to provide safety"; `Box` "should not be manually created" for foreign allocators | Double free; free with the wrong allocator | Each handle has one owner, released by the allocator that made it; a Rust `Drop` wrapper receives each foreign resource first (STND.CXX.20) | S28 | Holds |
| Callbacks | Async callbacks into Rust need "proper synchronization", and no callback may run after the Rust object is destroyed | Use after free | STND.CONC.5 (publication and lifetimes) | S28 | Holds |
| Opaque types | An empty enum as FFI type "is a really bad idea"; the opaque struct form is shown | UB from uninhabited-type assumption | Opaque foreign types are not empty enums | S28 | Holds |
| Unwinding | See section 3 | | | S9, S11 | |
| `longjmp` | The runtime "assumes that a Rust stack frame is not deallocated without executing destructors"; `longjmp` can violate this | UB | Foreign code that longjmps over Rust frames is not called | S1 | Holds |
| Whole-program UB | UB in C "means your entire program contains undefined behaviour" | | The record treats the C side as part of the unsafe surface | S1 | Holds |
| Study | Unsafe use is largest at interoperation: the OOPSLA 2020 study finds unsafe "used extensively, especially for interoperability with other languages", with most unsafe code "simple and well encapsulated" | | | S50 | 2020 corpus |

## 9. Editions and the minimum supported toolchain

- Editions are opt-in; "crates in one edition must seamlessly interoperate with those compiled with other editions"; the choice is per crate and "private" [S30]. A missing `edition` key means the oldest edition [S29].
- `rust-version` states the toolchain the package supports. On an older toolchain Cargo "will report that as an error"; a user can override. The resolver may take it into account; the declared version should be verified with automated testing [S29, S51].
- Practice: the manifest declares the edition and the minimum toolchain (STND.JL.2 and STND.CXX.2 are the models); a check builds on the declared minimum at each change (STND.JL.3); a change to either is a decision record. A bump of the minimum toolchain is a compatibility change for users.
- Safety-relevant edition changes exist (the unsafe-attribute wrapping and the default of unsafe-in-unsafe-fn moved with editions) [unverified which edition]; therefore a migration is tested, not assumed, and the review under STND.DEPS.4 includes it.
- Holds: the concept. Moves: edition names, defaults, and the resolver's use of `rust-version`.

## 10. The package manager as supply-chain surface

| Hazard | Source fact | Failure | Practice | Sources | Holds? |
|---|---|---|---|---|---|
| Lockfile | `Cargo.lock` "contains exact information about your dependencies"; "When in doubt, check it into version control" | Build differs by day | The lockfile is committed for each deliverable (STND.DEPS.10 already accepts it as the record); updates are reviewed (STND.DEPS.4); checksum verification in STND.DEPS.6 | S31 | Holds. The official FAQ explaining library versus application practice was not in my extract |
| Features | Features "should be additive"; Cargo "will use the union of all features enabled on that dependency"; resolver 2 stops some unification; mutually exclusive features are a hazard | A feature enabled by another crate changes this crate's behavior, including a feature that removes a safety check (inference) | Features are additive; the set of features enabled for each built artifact is recorded as a build setting (STND.CXX.4 analogue); a safety-relevant feature is off by default | S32 | Holds |
| Build scripts | Cargo compiles and runs `build.rs` "just before building the package"; "may perform any number of tasks"; runs for every dependency, with the builder's authority | Code execution at build time with no call needed | Each dependency with a build script is listed in the dependency record with what the script does; builds of untrusted changes run without secrets or network (see STND.CODE.9 for the network point) | S33 | Holds |
| Procedural macros | "have the same resources that the compiler has"; "the same security concerns that Cargo's build scripts have" | Same | Same | S34 | Holds |
| Incident [unverified] | A vendor report states that on 2026-08-20 three crates were published by a compromised maintainer account with a new dependency on a typosquatted package whose build script downloaded and ran a payload; the Rust security team removed the releases and locked the account (per the vendor). One search summary gives a CVE identifier and a CVSS figure; I did not confirm either | Build-time execution without any use of the dependency | Evidence for the two rows above, one incident, not a trend | S52, S53 | Moving. Not for the standard |
| Advisories | RustSec is a database of advisories for crates, maintained by a working group, exported to OSV and consumed by an auditing tool of `Cargo.lock`; advisory kinds not confirmed | Known-bad version shipped | STND.DEPS.7 | S54 | Holds |
| Vetting | Not retrieved: tools by which an organization records audits of each crate version | | | | [unverified] |

## 11. Lints, formatters, interpreters, sanitizers; floating point and SIMD

**Detecting undefined behavior in unsafe code, as outcomes.**
- An interpreter that executes the program on an abstract machine detects out-of-bounds and use-after-free accesses, data races, some weak-memory effects, aliasing violations, and leaks. Its documentation states that it "does not catch every violation", "cannot ensure that your code is sound", tests "one of many possible executions", and has "no access to most platform-specific APIs or FFI" [S35]. Its aliasing checkers are experimental, and the newer one is "even more experimental" [S35]. A report of UB proves unsoundness; a clean run does not prove soundness.
- The outcome for a provision: tests of unsafe code run under such a detector and fail at the first detection (STND.CXX.26 states exactly this for C++). The record states the limits of the run (STND.CONC.27 form): executed paths, platform and foreign code excluded, and which aliasing model was used. Foreign code needs a sanitizer on the real build; I did not retrieve sanitizer facts for Rust [unverified].
- The compiler's `unsafe_code` lint (allow by default) catches `unsafe` and related constructs; forbidding it in crates that need none makes the unsafe surface a list of exceptions [S23]. Clippy has lints for unsafe blocks without comments and for missing Safety sections, but I did not retrieve their descriptions [unverified].
- A formatter's outcome: the layout it produces is confirmed at each change (STND.CODE.5); no Rust content needed.
- Static analysis at the ecosystem scale: Rudra scanned crates.io (43,000 packages) in 6.5 hours and found 264 previously unknown memory-safety bugs, 76 CVEs, in three patterns [S46, S55]. The project is archived; the patterns remain valid.

**Floating point.**
- Primitive operations are rounded as IEEE 754 roundTiesToEven. NaN is not equal to itself, has no `Ord`, and its bit pattern is "not guaranteed to be portable or even fully deterministic"; the sign of NaN from arithmetic is non-deterministic [S37].
- Many library functions (`powi`, `exp`, `ln`, `sin`, `cbrt`, and others) have "unspecified precision": "it varies by platform, Rust version, and can even differ within the same execution" [S37]. `sqrt` and `mul_add` are specified exactly [S37]. No fast-math flag exists in stable Rust to my knowledge [unverified].
- Reading or writing the floating-point status register: "generally undefined behavior to change the default rounding or exception behavior" [S38].
- Practice: results needed to match across platforms use only operations with specified results, or tolerances under NUMER.11 (tolerance basis); NaN bit patterns are never compared; comparisons of floats that may be NaN use a total order or an explicit check; the numerics record (NUMER.5) names the library functions whose precision is unspecified.

**SIMD.**
- Vendor intrinsics are `unsafe` "unless the caller enables the required target features"; "it is unsafe to call an AVX2 function on a CPU that doesn't actually support AVX2"; run-time detection is by a macro of the standard library; a build with a feature enabled "only [runs] on systems which satisfy the required feature set" [S38]. `-C target-feature` "is unsafe and might result in undefined runtime behavior"; `target-cpu=native` ties the binary to the build host [S10].
- Practice: a function with a target feature is reached only after a run-time check or in a build restricted to processors that have it; the instruction set is a recorded build setting (STND.CXX.4 analogue; HW.5). I did not retrieve the status of the portable SIMD library [unverified].
- Results of vectorized and scalar paths are compared within tolerance by a test (STND.CONC.22 is the fixed-order analogue for reductions).

## 12. Empirical studies

| Study | Finding (abstract level) | Use | Source |
|---|---|---|---|
| Xu et al., all Rust memory-safety CVEs through 2020 | 186 reports; three kinds (automatic reclaim, unsound function, unsound generic or trait); "all memory-safety bugs require unsafe code"; many "mild soundness issues" | Defects sit at unsafe boundaries; drop-time and generic bounds are the classic spots | S42 |
| Qin et al., PLDI 2020 | 850 unsafe usages and 170 bugs studied across projects, libraries, security databases, and the standard library; two detectors found new bugs | Reasons for unsafe; bug classes | S43 |
| Evans et al., ICSE 2020 | Unsafe in "less than 30%" of libraries; over 75% of libraries "cannot be entirely statically checked" because unsafe appears in their call chain | The claim "safe Rust" depends on dependencies | S56 |
| Astrauskas et al., OOPSLA 2020 | "Rust hypothesis" (sparing, reviewable, hidden behind safe abstractions) supported "partially"; unsafe is "simple and well encapsulated" mostly, but extensive for interoperability | Basis for an encapsulation practice and an FFI focus | S50 |
| Bae et al., SOSP 2021 (Rudra) | 264 new bugs in the registry, three patterns: panic safety, higher-order invariants, Send/Sync variance | The three patterns as review checklist | S46, S55 |
| Cui et al., ICSE 2024 | Standard-library unsafe API documentation was "inconsistent and insufficient"; 19 safety properties defined over 416 unsafe APIs; 50 survey responses | Support for uniform Safety sections | S57 |
| Jung et al., POPL 2018 (RustBelt) | Machine-checked safety proof for a Rust subset; per-library verification conditions | Foundation for encapsulation as the unit of argument | S40 |
| Villani et al., PLDI 2025 (Tree Borrows) | A tree-based aliasing model; evaluated on the 30,000 most-used crates; rejects 54% fewer test cases than the earlier model (as reported in search results) | The aliasing rules are moving; code that passes only the permissive model is at risk | S58 |

No retrieved study measured the share of Rust defects that are panics, async cancellations, or overflow; the Oxide document is an experience report of one code base [S49]. I found no peer-reviewed study of cancellation bugs [unverified that none exists].

## Timeless versus moving

**Timeless (state in provisions):** unsafe is an obligation to argue, not permission to skip checks; soundness is a property of the safe interface; no safety argument rests on a destructor, poison flag, or absence of panic; panic safety of code that calls caller code; the panic strategy changes what code means; panics and exceptions do not cross a boundary unless both sides agree; data races versus race conditions; locks across suspension points; cancellation at suspension points; blocking on an event loop; overflow behavior is a build-setting choice and a defect either way; explicit arithmetic forms; the lockfile as record; features as additive configuration; build-time code as authority; interpreters detect some, not all, UB.

**Moving (keep out of provisions; Notes may name as examples without version):** the aliasing model (two experimental models are in use); the unsafe operation list and the validity rules (the Reference says the list "may grow or shrink"); ABI strings and the unwinding rules; the default of unsafe-in-unsafe-fn; names of arithmetic methods and lints (the strict forms are recent); async drop (unstable); portable SIMD status; the resolver's use of the declared toolchain; edition names; the tools themselves; the registry's advisory formats; any single incident.

## Not verified

- Clippy descriptions for `undocumented_unsafe_blocks`, `missing_safety_doc`, `unwrap_used`, `expect_used`, `indexing_slicing`, `float_cmp`, `multiple_unsafe_ops_per_block`, `panic_in_result_fn`; the lint index was too long for the extract and its first fetch redirected (I fetched the redirect target once, as the tool directed).
- The `#[must_use]` behavior of `Result`; the `unsafe_op_in_unsafe_fn` default across editions; when `strict_*` arrived.
- Rust sanitizer support; portable SIMD status; fast-math in stable Rust; tools for recording audits of crate versions.
- The Cargo FAQ on lockfiles for libraries versus applications.
- Qin et al.'s quantitative results and Astrauskas et al.'s numbers (the PDF returned 404; I did not look for another copy).
- The conclusion about unsafe in all 170 bugs of Qin et al.
- The 2026 supply-chain incident's CVE identifier, severity, and exposure window; vendor sources disagree on timing.
- The async working group's current plan for async drop; no RFC number was confirmed.
- Whether the Reference and Nomicon agree on foreign exceptions caught by `catch_unwind` (undefined versus unspecified-abort-or-Err); I report both.
- Sections of the Reference I did not retrieve: the full list of unsafe operations, the reference chapter on destructors and temporaries, and the layout chapter (`repr(transparent)`, `repr(Rust)`).

## Sources

| ID | Source | Kind |
|---|---|---|
| S1 | The Rust Reference, "Behavior considered undefined" (doc.rust-lang.org/reference/behavior-considered-undefined.html) | Language reference |
| S2 | The Rust Reference, "The unsafe keyword" (doc.rust-lang.org/reference/unsafe-keyword.html) | Language reference |
| S3 | Rust API Guidelines, "Documentation" (rust-lang.github.io/api-guidelines/documentation.html) | Guideline |
| S4 | The Rustonomicon, "Meet Safe and Unsafe" (doc.rust-lang.org/nomicon/meet-safe-and-unsafe.html) | Guide |
| S5 | std docs, `mem::forget` | Library reference |
| S6 | std docs, `sync::Mutex` | Library reference |
| S7 | Rust Reference, "Behavior not considered unsafe" (see S41) | Language reference |
| S8 | The Rustonomicon, "Exception Safety" | Guide |
| S9 | The Rust Reference, "Panic" (doc.rust-lang.org/reference/panic.html) | Language reference |
| S10 | rustc book, "Codegen options" (doc.rust-lang.org/rustc/codegen-options/index.html) | Tool reference |
| S11 | The Rustonomicon, "FFI" (see S28) | Guide |
| S12 | std docs, `panic::catch_unwind` | Library reference |
| S13 | std docs, `ops::Drop` | Library reference |
| S14 | The Rustonomicon, "Send and Sync" | Guide |
| S15 | std docs, `marker::Send` | Library reference |
| S16 | The Rustonomicon, "Races" | Guide |
| S17 | (reserved; see S16) | |
| S18 | The Rustonomicon, "Exception Safety" (guard example) (see S8) | Guide |
| S19 | tokio docs: `select!` (cancellation safety) and crate index (blocking, runtime features) (docs.rs/tokio) | Library documentation |
| S20 | (reserved; see S19) | |
| S21 | tokio crate index (see S19) | Library documentation |
| S22 | Clippy lint index (clippy.rust-lang.org/master/index.html), partial extract | Tool reference |
| S23 | The Rust Reference, "Operator expressions" (integer overflow, casts); rustc book allowed-by-default lints (`unsafe_code`, `missing_docs`) | Language and tool reference |
| S24 | The Rust Reference, "Behavior not considered unsafe" (integer overflow section) | Language reference |
| S25 | std docs, primitive `i32` (`checked_add`, `strict_add`, `unchecked_add`), partial | Library reference |
| S26 | The Rust Programming Language, ch. 9.3 "To panic! or Not to panic!" | Book |
| S27 | (reserved; see S26) | |
| S28 | The Rustonomicon, "FFI" (doc.rust-lang.org/nomicon/ffi.html) | Guide |
| S29 | The Cargo Book, "The Manifest" (edition, rust-version) | Tool reference |
| S30 | The Edition Guide, "What are editions?" | Guide |
| S31 | The Cargo Book, "Cargo.toml vs Cargo.lock" | Tool reference |
| S32 | The Cargo Book, "Features" | Tool reference |
| S33 | The Cargo Book, "Build Scripts" | Tool reference |
| S34 | The Rust Reference, "Procedural macros" | Language reference |
| S35 | Miri README (github.com/rust-lang/miri) | Tool documentation |
| S36 | Unsafe Code Guidelines repository (github.com/rust-lang/unsafe-code-guidelines); its README says the reference book is mostly archived and current consensus lives in the Reference and opsem decisions | Working group |
| S37 | std docs, primitive `f32` (NaN, unspecified precision, `mul_add`), partial | Library reference |
| S38 | std docs, `std::arch` | Library reference |
| S39 | std docs, `mem::MaybeUninit` | Library reference |
| S40 | Jung, Jourdan, Krebbers, Dreyer, "RustBelt: Securing the Foundations of the Rust Programming Language," POPL 2018 (abstract via search) | Peer-reviewed paper |
| S41 | The Rust Reference, "Behavior not considered unsafe" | Language reference |
| S42 | Xu, Chen, Sun, Zhou, Lyu, "Memory-Safety Challenge Considered Solved? An In-Depth Study with All Rust CVEs," arXiv:2003.03296 (abstract page) | Study |
| S43 | Qin, Chen, Yu, Song, Zhang, "Understanding Memory and Thread Safety Practices and Issues in Real-World Rust Programs," PLDI 2020 (program page abstract) | Peer-reviewed study |
| S44 | std docs, `thread::spawn` | Library reference |
| S45 | std docs, `sync::RwLock` | Library reference |
| S46 | Bae, Kim, Askar, Lim, Kim, "Rudra," SOSP 2021; project README (github.com/sslab-gatech/Rudra) | Peer-reviewed paper and artifact |
| S47 | std docs, `sync::atomic` | Library reference |
| S48 | std docs, `future::Future` | Library reference |
| S49 | Oxide Computer RFD 397 "Cancel safety" (rfd.shared.oxide.computer/rfd/397); RFD 400 seen only as a search result | Experience report |
| S50 | Astrauskas, Matheja, Poli, Müller, Summers, "How Do Programmers Use Unsafe Rust?," OOPSLA 2020 (abstract via search; the PDF URL returned 404) | Peer-reviewed study |
| S51 | The Cargo Book, "Rust Version" | Tool reference |
| S52 | Socket, "Popular Rust Crates Compromised in Build-Time Supply Chain Attack," 2026-08-20 (socket.dev) | Vendor report [unverified] |
| S53 | Search summaries of the same incident (Cloud Security Alliance note and others) | Secondary [unverified] |
| S54 | RustSec (rustsec.org) | Advisory database |
| S55 | Rudra project documentation (see S46) | Artifact |
| S56 | Evans, Campbell, Soffa, "Is Rust Used Safely by Software Developers?," ICSE 2020 (abstract) | Peer-reviewed study |
| S57 | Cui, Sun, Xu, Zhou, "Is unsafe an Achilles' Heel?," ICSE 2024; arXiv:2308.04785 (search summary) | Peer-reviewed study |
| S58 | Villani, Hostert, Dreyer, Jung, "Tree Borrows," PLDI 2025 (search summary) | Peer-reviewed paper |

Rows S17, S20, and S27 are reserved identifiers that carry no separate source; the claims cited under S16, S19, and S26 respectively stand on those sources.
