# Julia standard (STND.JL) 1.2

Adopted by The Custodian as revision 1.0 in ledger entry 105 (2026-10-23); revised to 1.1 in entry 120 (2026-10-24) and 1.2 in entry 156 (2026-10-25). This reading copy is composed from the per-provision files in STND/JL/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the conventions of Julia source that the language-neutral practice of STND.CODE and STND.DOCS leaves to the language. They cover the version of Julia that the work tracks, its bounds, checks, manifests, and run records (STND.JL.1 to STND.JL.5); names (STND.JL.6 and STND.JL.7); interfaces between packages (STND.JL.8, STND.JL.9, and STND.JL.10); types that the compiler infers (STND.JL.11 and STND.JL.12); failures (STND.JL.13 to STND.JL.18); arithmetic state and comparisons (STND.JL.19, STND.JL.20, and STND.JL.21); random numbers (STND.JL.22 to STND.JL.26); state shared between tasks (STND.JL.27); docstrings and doctests (STND.JL.28 to STND.JL.31); the checks that confirm them at each change, and the bounds checks of the production configuration (STND.JL.32 to STND.JL.36); and foreign interfaces (STND.JL.37 to STND.JL.41). The rules of concurrency that hold for every language are in STND.CONC, which this standard cites and does not restate. Its basis is the reference manual, the Julia manual of the reference version. STND.JL.13 gives STND.CODE.6, STND.JL.15 gives STND.CODE.14, and STND.JL.14 and STND.JL.15 give STND.CODE.7, their forms in Julia's constructs; STND.JL.16 and STND.JL.21 apply STND.CODE.12 and STND.CODE.10 to Julia's exceptions and tolerances. STND.JL.13, STND.JL.14, and STND.JL.15 instantiate PRIME.4, so they are binding and apply at every class; every other provision is a default (GOV.19) and a recommendation, which a project replaces by a recorded decision with an alternative that meets the same higher outcome (REPRO.7, PRIN.10). The provisions name Julia's constructs and files and no version, package, or tool; the repository configuration of each work selects its versions and tools (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and High-assurance coding standard have the meanings that STND.CODE gives them; each function that a package of the work declares by `export` or by `public` belongs to the public interface that the term Untrusted input of STND.CODE takes in, and an index that `eachindex`, `axes`, or `CartesianIndices` of the indexed array produces is valid by construction and is not untrusted input; Qualified revision has the meaning that STND.DEPS gives it; Work documentation has the meaning that STND.DOCS gives it; Numerical method, Numerical result, and Performance approximation have the meanings that NUMER gives them.

| Term | Definition |
| --- | --- |
| Reference version | The minor version of Julia that the repository configuration names as the one on which the work is written and checked. |
| Reference manual | The Julia manual of the reference version, at the address under https://docs.julialang.org/en/ that its publisher gives for that version. |
| Library code | Julia source in the modules of the packages of the work, including their package extensions, other than their tests and the files that hold entry points. |
| Entry point | The function or file that starts a program, a test, a script run directly, or a documentation example. |
| Production configuration | The Julia revision, and the command-line options, environment variables, and package preferences of Julia, with which the work produces its reported results. |
| Numerical kernel | A function that the repository configuration lists as one that carries out, on the path of a numerical result, the repeated arithmetic of a numerical method. |
| Type-stable call | A call of a function in which inference finds no call that dispatch resolves at run time, and for which it infers a result of one concrete type or of a union of one concrete type with `Nothing` or `Missing`. |
| Mutating function | A function that changes the state of at least one of its arguments other than an `IO` stream or a random number generator. |
| Owned type | A type that a module of the work defines, the type `Type{T}` of such a type `T`, and a type that has such a type among its parameters. |
| Type piracy | The definition of a method of a function that no module of the work defines, with no owned type among the types of its arguments. |
| Foreign interface | An interface through which Julia code of the work calls, or is called by, code written in another language, a call by `ccall` or `@ccall` and a Julia function that the work passes to such code by a pointer that `@cfunction` makes among them. |

## Notes

Direction and sources. The custodian's direction for Julia reads: "for Julia, refer to https://docs.julialang.org/en/v1/. use the latest version available". The custodian's ruling of 2026-10-23 adds, for every language standard, "we are platform and compiler agnostic" and "versions and tools can be selected by the project owner", and for Julia, "Don't pin the version or tools; use the latest". The provisions therefore name no version of Julia, no interval, and no package or tool; the repository configuration of each work selects them (GOV.18), and the Notes name a package only where an example explains a hazard. The address of the direction is a moving alias for the manual of the latest release, so the manual that governs the work is the one of its reference version (the term Reference manual). Each provision states an outcome that a tool or a reviewer decides from the source, the repository configuration, and the record of checks. The grouping of statements into steps is governed by STND.CODE.13 for Julia as for each language. A fact marked unverified is one that the documentation consulted did not confirm. The note research/round-addenda/a2-language-facts.md (a2 below) confirms facts of these Notes from the manual of Julia, and the keys S11 to S14 that the Notes cite after a2 are entries of its table of sources.

Departures from the reference manual. Function, macro, and variable names separate words with underscores (STND.JL.6), the rule of Blue Style, which the SciML style guide and YASGuide share; the custodian's ruling of 2026-10-23 keeps it (PRIN.10). The manual prefers lowercase names with the words joined and uses underscores where joining hurts reading, a judgment that a reviewer makes case by case; the underscore rule is decided by reading the name, and it matches the PEP 8 names of the custodian's Python source. A method of a function that another package defines keeps that function's name, `Base.iterate` and `Base.push!` among them. The manual names the docstring headings `# Arguments`, `# Examples`, `# Implementation`, and `# Extended help`; STND.JL.30 adds `# Fields`, `# Returns`, `# Throws`, and `# Notes`, so that the contract of STND.CODE.3 has a fixed place, and fixes their order; the custodian's ruling of 2026-10-23 keeps the manual's names (PRIN.10). Blue Style also names `# Returns` and `# Throws`. Explicit imports (STND.JL.9) come from Blue Style, where the manual permits a bare `using`, because a bare `using` hides which package supplies a name (SIMPL.6). The manual prescribes no layout tool; STND.CODE.5 asks for one, and the repository configuration names it. The manual's order of arguments stays guidance, because Base departs from it and no tool decides it; STND.JL.22 uses it only to place the generator.

Versions. Julia has no way to write "latest" in a project file, so STND.JL.1 to STND.JL.4 separate the reference version, the bounds, the revisions checked, and the manifests. The reference version is the latest stable minor version consistent with the rest of the computational environment (STND.DEPS.3), because the publisher usually stops patching a minor version, other than a long-term-support line, once the next one ships, and a work left on the previous one runs without its fixes; a move that a dependency or tool of the work does not yet support waits under that clause, and the reviews of STND.DEPS.4 record why. A qualified revision stays, because no other revision is admissible without new evidence; STND.CODE.19 fixes, for high-assurance code, a version of Julia that its high-assurance coding standard covers and for which each tool that runs that code holds the validation that the work requires; STND.JL.1 and the third sentence of STND.JL.3 yield to it by their own text, and its third sentence keeps that version as a qualified revision. A change of the Julia revision, including a patch release, is a change of the runtime of each execution path under HW.7 and of a pinned revision under STND.DEPS.5, and each run records the exact Julia and package revisions (STND.DEPS.8) with the settings of STND.JL.5, which change results without a change of source. In `[compat]`, an entry of a major and minor version admits each later version up to the next major version, exclusive, and for a package below version 1 the next minor version is breaking. The floor at the reference version follows the direction. A package that work outside the custodian's projects imports may replace the second sentence of STND.JL.2 by a recorded decision with a lower floor, and STND.JL.3 then checks the earliest version that its bounds admit as well (GOV.19). The scheduled check on the newest stable release and on the prerelease shows a coming change before the reference version moves; it does not gate a change, because its failure is not yet a defect of the work. `Project.toml` and `Manifest.toml` give the exact revision of each package, and not its reason or license identity, so under STND.DEPS.10 they are the record of revisions, and the dependency record holds the reason and license beside them (REPRO.9). A manifest named for a Julia version is the manifest file of STND.JL.4 where it exists, and its `julia_version` field names the Julia that resolved it. That a package imported by other work commits no manifest is common practice (unverified), because its dependents resolve their own environments.

Names. A name that the documented notation of NUMER.4 fixes, a matrix `A`, an operator `H`, a step `Δt`, or the constant `ħ`, keeps its symbol (STND.JL.6, STND.DOCS.12). A reviewer decides STND.JL.6 and STND.JL.7 where no check of the repository configuration decides them. The `!` suffix makes mutation visible at the interface (DSGN.14). The term Mutating function leaves out a stream and a generator, which change on each call that uses them, so `write` and `rand` carry no `!`, while `Random.seed!` and `take!` keep the `!` that the second sentence of STND.JL.7 admits. A function that changes state outside its arguments has hidden state, which DSGN.14 governs and no naming convention fixes. A leading underscore on an internal name is permitted and not required, because `export` and `public` mark the interface (STND.JL.8).

Interfaces. Julia's semantic versioning counts only exported and public names, with their documented behavior, as the interface of a package, which is why STND.JL.8 asks for the declaration and STND.JL.9 for use of declared names. Declaring one name both exported and public is an error in current versions. Tests are not library code, so they use internals of the work. A package extension is library code, and its use of the package it extends is the one use of internals that STND.JL.9 admits without a reason; other library code that uses an internal of another package carries its reason. Type piracy changes the behavior of code that other packages own, for each package loaded in the same session, which is hidden coupling through the shared method table (DSGN.14, STND.JL.10). A method of `convert`, `promote_rule`, `zero`, or `eltype` on `Type{T}` of a type of the work is not piracy, as the term Owned type states. A wrapper type or a function of the work's own is the remedy that the manual gives.

Types. STND.JL.11 limits type stability to the numerical kernels that the repository configuration lists, because the manual's performance advice concerns hot code and analysis of every call reports noise in setup and input code. Type stability is a choice of representation, which RSRC.5 settles before lower-level optimization, and it lets a mechanical check see each call that a kernel makes (DSGN.3); RSRC.4 governs the optimizations made after it. The term Type-stable call states what the checks decide: a report of each call that dispatch resolves at run time, and a comparison of the inferred return type with the actual one, as the `@inferred` macro of the `Test` standard library makes, whose form with an allowed type admits the small union. A field of a fixed `Float64` type blocks the dual numbers of forward-mode differentiation, which is why a field that outputs are differentiated through takes a type parameter where NUMER.27 applies (STND.JL.12). A `const` binding of a mutable object is still mutable global state, which DSGN.14 and STND.CODE.2 govern.

Failures. STND.JL.13, STND.JL.14, and STND.JL.15 bind at every class, including CSQ4. Each forbids a construct, or asks for one of the responses that PRIME.4 already allows, for a condition that PRIME.4 lists, so none raises the floor (GOV.11); this is the custodian's ruling of 2026-10-23 (PRIN.10), which also holds that the reach of the term Untrusted input to the arguments of each declared public function raises no floor. STND.CODE defines the term once, and the Terms above place each declared function in the public interface that the term takes in, so the reach of the ruling is kept; STND.CODE adds the functions that the documentation or the repository configuration names for use outside the work. A module exports names and marks names as public, and the keyword `public` marks a name as part of the public API without exporting it, from Julia 1.11 (a2, S14); that an exported name is public is the reading of this standard. STND.CODE.6 states for every language the outcome of which STND.JL.13 gives the Julia forms, `@assert`, a `@boundscheck` block, and an index that `@inbounds` leaves unchecked. STND.CODE.16 keeps in every build each check that CPS.5 or CPS.9 requires where those apply, so a `@boundscheck` block, which `--check-bounds=no` removes, does not hold such a check either. The option emits bounds checks always under `yes`, never under `no`, and under the default `auto` respects `@inbounds`, which is able to return incorrect results, crash, or corrupt memory for an index out of bounds (a2, S11 and S12). STND.PY has no counterpart of the third sentence of STND.JL.13, because the Python interpreter checks each index in every mode, and its Notes say so. The docstring of `@assert` warns that an assert might be disabled at certain optimization levels, and YASGuide keeps `@assert` out of required checks; whether a setting removes one today is unverified, and a check that the language does not promise to keep fails the outcome of STND.CODE.6. A `@boundscheck` block is removed by `@inbounds` at the call and by the execution setting `--check-bounds=no`. An unmarked `A[i]` with an untrusted index is checked today, but an `@inbounds` added later around it removes the check, so the check of STND.JL.13 stands apart from the indexing: `checkbounds(Bool, A, i) || throw(BoundsError(A, i))`. An argument of a declared public function is untrusted input unless the threat model of GUARD.16 records otherwise, and a size check of such an argument throws an `ArgumentError` or a `DimensionMismatch`. STND.JL.15 lists the responses of PRIME.4 once, in the Julia form of STND.CODE.14, and STND.JL.14 refers to it. STND.CODE.14 admits the pass of a condition to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism of the language, an exception among them, that propagates the condition to the caller; in Julia a thrown exception is that mechanism, and a returned result the first form. STND.CODE.15 asks nothing of Julia until a form of declaration under which an ignored result is diagnosed is among the means of the work, and STND.CODE.7 still forbids discarding a listed failure. A Julia `catch` block receives every exception, so it receives `OutOfMemoryError` and `StackOverflowError`, the resource exhaustion that PRIME.4 lists, unless it throws them on (STND.JL.14). The default logger of Julia shows records at the levels `Warn` and `Error`, which is why STND.JL.15 accepts a visible degradation through a logging macro only at those levels, as the custodian's ruling of 2026-10-23 keeps (PRIN.10); a program that installs another logger decides what it shows. A returned convergence flag, the form that solver packages use, meets STND.JL.15, and STND.CODE.7 governs the caller that receives it. `InterruptException` is the operator's stop, which PRIME.4 does not list, so STND.JL.16 rethrows it as a default; an exception that a task stores is thrown again, inside a `TaskFailedException`, by the `fetch` or `wait` that collects the task. Julia integer arithmetic wraps on overflow without an error, so invalid input that overflows passes the checks of DSGN.2 undetected where the operands come from untrusted input (STND.JL.17). STND.JL.18 asks for the reason of each construct that assumes a condition that the compiler does not check: valid indices for `@inbounds` and `@propagate_inbounds`, independent iterations and reorderable reductions for `@simd`, the effects that `@assume_effects` declares, and the validity of pointers and memory for functions named `unsafe_`.

Arithmetic. Under NUMER, a use of `@fastmath`, `@simd`, `muladd`, or `set_zero_subnormals(true)` on the path of a numerical result is a performance approximation, which NUMER.16 and NUMER.17 govern from their own onset. `@fastmath` permits reassociation and contraction, ignores signed zeros, and assumes that no value is NaN or infinite; the manual calls `@simd` experimental, and it permits reordering of floating-point reductions; `muladd` fuses where the hardware allows, so its result depends on the machine. STND.CODE.21 recommends against an annotation that, by its documentation, lets the compiler assume finite values in code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs; whether the documentation of `@fastmath` states that assumption is unverified. `set_zero_subnormals(true)` sets the flushing of subnormal values on the current thread only, and a task started with `Threads.@spawn` migrates between threads, so STND.JL.19 keeps the operations that the setting concerns on threads whose state was set. HW.CPU.3 also requires the state restored before control returns to code that the hardware contract does not cover. Julia has no form of `set_zero_subnormals` scoped to a function; a wrapper that saves `get_zero_subnormals()`, sets the mode, runs operations that do not yield, and restores the mode in a `finally` clause is the remedy. Whether a task migrates only where it yields is unverified. HW.5 and NUMER.5 record the mode in the delivered arithmetic, and STND.VVUQ.4 judges values below the smallest normal number at tier 3 or a less strict tier where flushing is on. `BigFloat` precision and rounding are global state; the forms of `setprecision` and `setrounding` that take a function bound their scope (STND.JL.20), and the form of `setprecision` that takes a function is thread safe in current versions. A precision passed to one `BigFloat` constructor sets the precision of that value alone, and arithmetic on it returns values at the default precision, so it is no remedy; a `big"..."` literal takes its precision when the code is loaded.

Comparisons. STND.VVUQ.1 sets the tier of each comparison, STND.VVUQ.5 its relative and absolute parts, and STND.VVUQ.3 the agreement of NaNs; STND.JL.21 asks that the Julia comparison state them where the code makes it. `isapprox` takes by default a relative tolerance of the square root of the machine epsilon of the less precise type and an absolute tolerance of zero, so `x ≈ 0` holds only for an exact zero, and it treats a NaN as unequal to a NaN unless `nans = true` is passed. On arrays, `isapprox` compares the norm of the difference with the norms of the arrays, so a comparison that STND.VVUQ.5 judges element by element broadcasts it, as `all(isapprox.(a, b; rtol = RTOL, atol = ATOL))`. In a test, `@test a ≈ b atol = ATOL rtol = RTOL` passes the keywords to `isapprox`.

Randomness. STND.CODE.2 already asks that the source of randomness arrive through the interface; STND.JL.22 gives its Julia form. Base takes the generator as the first argument of `rand(rng, ...)` and before the mutated array of `rand!(rng, A)`, the place that the style guide gives an `IO` stream. A method that fills in `Random.default_rng()` for a missing generator is library code that draws from a generator it did not receive, so STND.JL.22 excludes it. The default generator has state per task; `Random.seed!` without a generator seeds the current task's state, from which each other package in that task draws (DSGN.14), and its type and streams may change between minor versions. A child task is seeded from its parent at its creation without advancing the parent, so code that draws from the task-local generator in tasks created in a fixed order gets streams independent of the scheduler; library code does not draw from that generator (STND.JL.22), so the parts of parallel work take their streams from a facility of STND.VVUQ.62 (STND.JL.24). STND.JL.24 is the Julia form of STND.CONC.23, which keys each stream of a computation divided among concurrent tasks to a part defined independently of the number of tasks and of the task that computes it; STND.JL.24 reaches each division of work into parts, parts run as separate runs included, which STND.CONC.23 does not reach. Seeding a part with `seed + i` is the arithmetic combination that STND.VVUQ.62 rejects, and a seed derived with `hash` is neither a facility of STND.VVUQ.62 nor stable, since the values of `hash` have changed between minor versions. NUMER.24 governs the evidence that the streams are independent. An entry point, a test or a doctest among them, records its root seed of at least 128 bits (STND.VVUQ.62), and where no seed is given it draws one from the operating system's entropy and records it (STND.JL.23); entropy from the operating system is reproduced by no seed. A generator whose stream for a seed is fixed across versions of Julia meets STND.JL.25 only for the sampling functions whose stability its documentation states. A doctest whose shown output does not depend on the draws holds no exact drawn values and is outside STND.JL.25. A fixed-seed test detects a change, and a test with fresh, logged seeds judges correctness (STND.VVUQ.64); a move of the reference version changes the default streams, so a fixed-seed test that fails then is repeated only by its recorded rule (NUMER.26). A change of the values of `hash` also changes the iteration order of `Dict` and `Set` (STND.JL.26); a sum over `values(d)` changes in its last digits when that order changes.

Concurrency. STND.CONC holds the rules of concurrency that hold for every language, and this standard adds only their Julia forms (GOV.31). STND.JL.27 is the Julia form of the second sentence of STND.CONC.16: tasks migrate between threads, so state chosen by `Threads.threadid()`, including a buffer or a generator, is shared by the tasks that the scheduler moves, and `threadid()` exceeds `nthreads()` while the interactive pool is in use. STND.CONC.3 has each object that one task changes while another reads or changes it follow one stated protection, a lock or atomic operations among them: `push!` and insertion into a `Dict` from two tasks need a lock, and accumulation into a shared scalar inside `Threads.@threads` is a data race; partial results per task, combined after `fetch`, avoid both. Whether a result's partition into parts is fixed independently of the thread count, so that its reductions agree bitwise across thread counts, is declared under HW.12 and REPRO.3. Distributed computing, GPU packages, ahead-of-time compilation with trimming, and Pkg apps are outside this standard. STND.OFFLD and HW.GPU govern offload to accelerators from Julia, from the placement of offloaded work (STND.OFFLD.2) to its completion (HW.GPU.3), and STND.MPI and STND.CONC govern distributed computing where they apply, the halt of one process of a run among it (STND.MPI.6, STND.CONC.2); STND.CODE and the project instruments govern the rest.

Docstrings. STND.JL.28 to STND.JL.31 follow the documentation chapter of the reference manual. The imperative summary is the manual's convention for Julia docstrings; STND.DRAFT.10 concerns governance text. The manual's other conventions are guidance: the opening and closing triple quotes on lines of their own, `raw` strings for text that holds `$` or `\`, a "See also" paragraph with `[name](@ref)` links, a line length, which the repository configuration sets, and `# Arguments` only where the signature and the summary leave an argument unclear. The order of the headings puts what a caller reads ahead of what an implementer reads. `# Arguments` and `# Throws` correspond to the Parameters and Raises sections of numpydoc; one name per concept (STND.DOCS.12) holds within a work, and a work in both languages names the section by the convention of each. STND.DOCS governs the prose of each docstring, and STND.DOCS.13 runs its examples. A doctest matches printed text exactly, so a shown floating-point value is rounded by the example, as `round(x; digits = 6)` rounds it, or matched through a filter that drops the digits beyond the stated tolerance (STND.JL.31). Under STND.DOCS.13 the shown result of a failing example changes only with a change to the work that the example describes, which is the one occasion for an automatic rewrite of the expected output. An example in a README runs only where the documentation build includes the README as a page. Where a package is registered in General, the public register of Julia packages, that register's rule that substantial contributions by language models be disclosed in the package's README is a publisher's policy under STND.DOCS.7.

Checking. A documentation tool that reports docstrings missing from the pages of the documentation does not by that report find a declared name without a docstring, which is why STND.JL.32 has two sentences; the `Docs.undocumented_names` function of Base decides the first. A check of package hygiene that loads the package is a check and not a static check, which is why STND.JL.33 asks for a check; a check that bounds are present leaves the Julia floor of STND.JL.2 to review. The standard command that runs a package's tests no longer forces bounds checking in current versions, which is why STND.JL.34 states the setting. Under the default setting of `--check-bounds`, Julia emits bounds checks other than inside `@inbounds`, whose reason STND.JL.18 asks for at each location, and under `--check-bounds=no` it emits none for the session (a2, S12), where no location states a reason; that the same holds for each array type of a package is unverified. STND.JL.36 is therefore the Julia counterpart of STND.CXX.27, which asks each reporting build of C++ to enable the checks of its standard library: it asks the production configuration to leave bounds checking on, other than inside `@inbounds`, unless a measurement against a stated budget and a decision record show its cost, and STND.JL.34 then tests that configuration as it is. STND.CXX.27 stays unchanged, and STND.JL.36 is its Julia counterpart. Forced bounds checks and coverage change inlining and vectorization, which change the order of reductions and so the delivered arithmetic; the evidence that HW.7 and HW.CPU.3 ask for therefore comes from the run of STND.JL.34 in the production configuration, and the inference and allocation tests run there as well. A deprecation setting of the command line applies to the whole session, so a run that exempts a listed deprecation inside a dependency reports deprecations without failing on them and fails on each record that the list does not hold (STND.JL.35). A text search of the source finds candidate breaches of STND.JL.13, STND.JL.18, STND.JL.20, STND.JL.21, STND.JL.22, and STND.JL.27, among them `@assert` and `@boundscheck` in library code, `threadid(`, and `seed!(` outside entry points; a match is a finding for review, and such a search reports false positives.

Foreign interfaces. STND.JL.37 to STND.JL.41 give the Julia forms of what STND.CXX.20 and STND.CXX.22, STND.RUST.24 to STND.RUST.27, and STND.FTN.27 and STND.FTN.28 state for their languages: types and layouts that match the foreign declaration, memory with a stated lifetime and resources with one owner, and exceptions kept from crossing into foreign code (DSGN.4, DSGN.14, DSGN.5). No C header is used in a call of a C function, so the Julia types and call signatures alone state what the header declares, and an inconsistency is able to work on one system and fail or produce indeterminate results on another (a2, S13). Base names the C types by aliases: `Cint` is `Int32` on every system, while `Clong` and `Cwchar_t` among others differ between systems (a2, S13). A test compares the layout of a struct with the foreign declaration through `sizeof` and `fieldoffset` (unverified); the two sentences of STND.JL.37 are applied apart where the work declares no struct. A C declaration of a pointer to elements states no order of dimensions and no strides, so STND.JL.41 takes them from the documentation of the foreign function or from a test, as STND.FTN.28 tests a section with a stride other than one; that a view of an array is able to have a stride other than one is unverified for each array type. `GC.@preserve` marks objects as in use during an expression, which unsafe code needs where the expression uses memory that one of them owns, and without it the memory behind a pointer taken by `pointer` is able to be collected before its use; the object that `@cfunction` returns for a closure is kept alive by the work until all uses of it are done (a2, S11 and S13). STND.JL.38 asks for both, and STND.JL.40 for one owner of each resource that foreign code creates, as STND.RUST.27 does. STND.JL.18 already asks the reason for each function whose name begins with `unsafe_`, `unsafe_wrap` and `unsafe_load` among them. A callback exposed through `@cfunction` throws no error in the manual's practice, because an error returns control to the Julia runtime unexpectedly and is able to leave the program in an undefined state (a2, S13), so STND.JL.39 catches each exception in the callback. Its three sentences are one remedy and are not applied apart: an exception caught and neither converted nor stored is discarded, which STND.CODE.7 forbids for a listed failure, and an `InterruptException` is thrown again after the foreign call returns, the place where STND.JL.16 is met without a throw through foreign code. STND.CXX.22, STND.RUST.25, STND.PY.35, and STND.JL.39 take the same steps for an exception or a panic in a callback: catch it there, then convert it to the error of the interface or answer it after the foreign call returns.

Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, RSRC, or a provision of NUMER, HW, or HW.CPU, and applies from CSQ3; work of CSQ4 may omit it. The part of each default that rests on NUMER, HW.7, or HW.CPU.3 applies only to work that those profiles bind, and its other parts apply to all work. STND.JL.17, STND.JL.18, and STND.JL.34 instantiate the checking of preconditions where untrusted data enters and the retention of checks for verification under DSGN.2, which apply from CSQ3, not the checking of postconditions that STND.CLASS.10 starts at CSQ1. STND.JL.36 instantiates the checking of DSGN.2 that STND.CLASS.10 applies from CSQ1, as STND.CXX.27 does, and applies from CSQ1. STND.JL.37, STND.JL.39, and STND.JL.41 instantiate the schemas of DSGN.4 and the external contracts of DSGN.5, which STND.CLASS.10 applies from CSQ2, and apply from CSQ2; STND.JL.38 and STND.JL.40 rest on no row and apply from CSQ3. STND.JL.11 and STND.JL.33 ask for mechanical checks (DSGN.3) from CSQ3; the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 starts at CSQ0 under DSGN.3, stays with that row. STND.JL.27, the Julia form of the second sentence of STND.CONC.16, instantiates DSGN.14 as that provision does, rests on no row, and applies from CSQ3; the protection of state that tasks share is STND.CONC.3, and the verification of its invariants, which STND.CLASS.10 starts at CSQ2, stays with DSGN.15. STND.CONC.3, STND.CONC.16, and STND.CONC.23 apply from CSQ3, as STND.JL.27 and STND.JL.24 do, so the citations move no rule to another class. STND.JL.5, STND.JL.19, and STND.JL.34 instantiate NUMER.5, HW.CPU.3, or HW.7, each of which also instantiates the contracts of DSGN.5 that STND.CLASS.10 starts at CSQ2; they apply from CSQ3 through the other provisions they instantiate, and so tighten above the floor (PRIME.15) for work that NUMER or HW binds, at the cost of a record or one run of the tests. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no provision raises the floor (GOV.11).

Existing Julia source conforms to the default provisions when a change next touches it.

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| HW.GPU | Accelerators |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.DRAFT | Drafting standard |
| STND.FTN | Fortran standard |
| STND.MPI | Message Passing Interface standard |
| STND.OFFLD | Accelerator offload standard |
| STND.PY | Python standard |
| STND.RUST | Rust standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Versions

#### STND.JL.1 Reference Julia version

Default. Instantiates REPRO.2, REPRO.9, SIMPL.4.

The repository configuration SHOULD name one reference version (REPRO.2). Other than for a version that STND.CODE.19 fixes, the reference version SHOULD be the latest stable minor version of Julia that is consistent with the rest of the computational environment, as STND.DEPS.3 asks (REPRO.9, SIMPL.4). Where a qualified revision of Julia fixes the reference version, the reference version and the Julia revision of the production configuration MAY stay at that revision (REPRO.9).

#### STND.JL.2 Julia compatibility bounds

Default. Instantiates REPRO.9, DSGN.6.

Each `Project.toml` file of the work SHOULD state in its `[compat]` section a bound for Julia and for each dependency, weak dependency, and test dependency that the file lists, with an upper limit that excludes the next release that semantic versioning marks as breaking (REPRO.9, DSGN.6). The lower limit of the bound for Julia SHOULD be the reference version, inclusive (REPRO.9).

#### STND.JL.3 Checked Julia versions

Default. Instantiates VV.8, REPRO.9.

Other than where a qualified revision fixes it, the Julia revision of the production configuration and of the checks of each change SHOULD be the latest patch release of the reference version (VV.8, REPRO.9). Where the bounds of STND.JL.2 admit a minor version earlier than the reference version, the checks of each change SHOULD also run on the earliest version that they admit (VV.8). Other than for code whose version of Julia STND.CODE.19 fixes, a check that reports its failure without blocking a change SHOULD run the tests, at the interval that the repository configuration sets, on the newest stable release and on the newest prerelease of Julia (VV.8).

#### STND.JL.4 Committed manifests

Default. Instantiates REPRO.1, REPRO.9.

Where the work reports results, the manifest file of each environment that produces them SHOULD be under version control with the source that it resolves (REPRO.1, REPRO.9). A package that other work imports, and whose own environment produces no reported result, MAY keep its manifest file out of version control (REPRO.9).

#### STND.JL.5 Recorded run settings

Default. Instantiates REPRO.2, NUMER.5.

Each run that produces a reported result SHOULD record, beside the revisions that STND.DEPS.8 asks for, the number of threads in each thread pool, the BLAS library and its number of threads, and each command-line option and environment variable of Julia that sets optimization, the math mode, the CPU target, or bounds checking (REPRO.2, NUMER.5).

### Names

#### STND.JL.6 Julia naming conventions

Default. Instantiates INTPR.1, INTPR.4.

Each name in the Julia source of the work SHOULD follow the convention that the table of this provision gives for its kind (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4). A method of a function that no module of the work defines MAY keep that function's name, whether or not the name ends in `!` (INTPR.1).

| Name of | Convention |
| --- | --- |
| Module or type | Capitalized words joined without separators |
| Type parameter | One capital letter, or capitalized words joined without separators |
| Function, macro, variable, field, or argument | Lowercase words separated by underscores |
| Global constant other than a module, a type, or a function | Uppercase words separated by underscores |

#### STND.JL.7 Mutation marked in names

Default. Instantiates DSGN.14, INTPR.1.

The name of each mutating function SHOULD end in `!` (DSGN.14). Each function whose name ends in `!` SHOULD change the state of at least one of its arguments, including an `IO` stream or a random number generator (INTPR.1).

### Interfaces

#### STND.JL.8 Declared public interface

Default. Instantiates DSGN.1, DSGN.6.

Each name that the documentation pages of a package of the work present for use outside the module that defines it SHOULD be declared by `export` or by `public` in that module (DSGN.1, DSGN.6).

#### STND.JL.9 Explicit imports

Default. Instantiates SIMPL.6, DSGN.7, REPRO.7.

Each name that a module of library code takes from another package SHOULD appear in the explicit list of an `import` or `using` statement, or be written qualified by its module (SIMPL.6). Outside the use that a package extension makes of the package that it extends, each name that library code uses from another package, including `Base`, SHOULD be one that the package declares by `export` or by `public` (DSGN.7). Where library code uses another name of another package, that use SHOULD carry the reason that STND.CODE.4 asks of a suppressed finding (REPRO.7).

#### STND.JL.10 Methods on owned names

Default. Instantiates DSGN.14, DSGN.7.

Each method that the work defines SHOULD belong to a function that a module of the work defines or have at least one owned type among the types of its arguments (DSGN.14, DSGN.7).

### Types

#### STND.JL.11 Type-stable numerical kernels

Default. Instantiates RSRC.5, DSGN.3.

Each call of a numerical kernel that its tests make SHOULD be a type-stable call (RSRC.5, DSGN.3). At each change that affects a numerical kernel, a test SHOULD confirm that each such call is a type-stable call (DSGN.3).

#### STND.JL.12 Concrete types for inference

Default. Instantiates RSRC.5, NUMER.27.

Each field of a struct, and the element type of each container, that a numerical kernel reads SHOULD be declared by a concrete type or by a type parameter of the struct or container (RSRC.5). Where NUMER.27 applies to a numerical kernel, each field that holds a value through which its outputs are differentiated SHOULD be declared by a type parameter (NUMER.27). Each global binding that a numerical kernel reads SHOULD be declared `const` or declared with a concrete type (RSRC.5).

### Failures

#### STND.JL.13 Untrusted indices and assertions

Binding. Instantiates PRIME.4, DSGN.2.

A check of untrusted input SHALL NOT be written with `@assert` (PRIME.4, DSGN.2, STND.CODE.6). A check of untrusted input SHALL NOT be placed in a `@boundscheck` block (PRIME.4, DSGN.2). Where an index derives from untrusted input, code SHALL reject an invalid value of that index, before the index is used, by a check that no execution setting and no `@inbounds` annotation removes (PRIME.4, DSGN.2).

#### STND.JL.14 Resource exhaustion in catch blocks

Binding. Instantiates PRIME.4.

Where a `catch` block receives an `OutOfMemoryError` or a `StackOverflowError`, it SHALL respond as STND.JL.15 requires (PRIME.4).

#### STND.JL.15 Julia responses to listed failures

Binding. Instantiates PRIME.4.

Where code detects a condition that PRIME.4 lists, it SHALL throw an exception, halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, degrade visibly with a diagnosis, or return the condition in its result (PRIME.4, STND.CODE.14). Where the visible degradation is a record that a logging macro writes, the level of that record SHALL be `Warn` or `Error` (PRIME.4).

#### STND.JL.16 Unhandled exceptions rethrown

Default. Instantiates SIMPL.6.

Each `catch` block SHOULD test the type of the exception that it receives and throw again each exception that it neither handles nor discards with the reason that STND.CODE.12 asks for (SIMPL.6). Where a `catch` block receives an `InterruptException`, it SHOULD throw that exception again (SIMPL.6).

#### STND.JL.17 Checked integer arithmetic

Default. Instantiates DSGN.2.

Where integer arithmetic on untrusted input is able to exceed the range of its type, code SHOULD check it for overflow, by a function of `Base.Checked` or by a check of range before the operation (DSGN.2).

#### STND.JL.18 Assumed conditions stated

Default. Instantiates REPRO.7, DSGN.2.

Each use of `@inbounds`, `@propagate_inbounds`, `@simd`, `@assume_effects`, or a function whose name begins with `unsafe_` SHOULD state, at its location, the condition that it assumes and why that condition holds (REPRO.7, DSGN.2).

### Arithmetic

#### STND.JL.19 Subnormal flushing scope

Default. Instantiates HW.CPU.3, REPRO.2.

Where code calls `set_zero_subnormals(true)`, each operation that the call concerns SHOULD run, for its whole duration, on a thread whose state that call set (HW.CPU.3, REPRO.2).

#### STND.JL.20 Scoped BigFloat settings

Default. Instantiates DSGN.14.

Code SHOULD change the default precision or the rounding mode of `BigFloat` arithmetic only by the forms of `setprecision` and `setrounding` that take a function (DSGN.14).

#### STND.JL.21 Stated comparison tolerances

Default. Instantiates NUMER.11, VV.3, SIMPL.6, REPRO.7.

Each comparison of floating-point values within a tolerance, by `isapprox`, by `≈` with keywords in a test, or by an expression, SHOULD state the parameters of its tier of STND.VVUQ.1, including, at the rounding and numerical-error tiers, the relative and the absolute part of STND.VVUQ.5, and its treatment of a NaN under STND.VVUQ.3 (NUMER.11, VV.3, SIMPL.6). Each such tolerance SHOULD be a named constant that carries its basis under NUMER.11, as STND.CODE.10 recommends (NUMER.11, REPRO.7). A comparison of exact values, or one that the bitwise tier of STND.VVUQ.1 admits, MAY use the equality operators (VV.3).

### Randomness

#### STND.JL.22 Generators through the interface

Default. Instantiates DSGN.17, DSGN.16, DSGN.14.

Each function of library code that draws random numbers SHOULD draw them only from a generator that it receives through its interface, as an argument in the position that the style guide of the reference manual gives an `IO` stream or as a field of an object that it receives (DSGN.17, DSGN.16, DSGN.14). Library code SHOULD NOT seed the default random number generator of `Random` (DSGN.14).

#### STND.JL.23 Generators seeded at entry points

Default. Instantiates DSGN.17, REPRO.1.

Other than a generator that STND.JL.24 derives from another, each generator that the work constructs SHOULD be constructed at an entry point, from a seed that the record of the run holds (DSGN.17, REPRO.1). Where an entry point seeds a generator from fresh entropy, it SHOULD record that entropy with the run (REPRO.1).

#### STND.JL.24 Parallel random streams

Default. Instantiates DSGN.17, REPRO.3.

Where work divided into parts draws random numbers, each part SHOULD draw from a stream that a spawning, jump-ahead, or counter-based facility of its generator library derives from the root seed of the run and the index of the part, as STND.VVUQ.62 recommends (DSGN.17, REPRO.3).

#### STND.JL.25 Stable draws in references

Default. Instantiates REPRO.3, REPRO.6, VV.3.

Each test reference and each documentation example that holds exact values drawn from a random number generator SHOULD draw them from a generator, through a sampling function, whose output for a given seed stays the same across versions of Julia, or hold the values as recorded data (REPRO.3, REPRO.6). Where the verdict of a test depends on the stream of a seeded generator, the test SHOULD state, before its first failure, the rule by which it is repeated after a change of the reference version, as NUMER.26 requires of a repetition (VV.3).

#### STND.JL.26 Values unstable across versions

Default. Instantiates REPRO.3, REPRO.6.

Outputs, recorded data, and test references of the work SHOULD NOT hold values that `hash` returns (REPRO.3, REPRO.6). Each reported result SHOULD be independent of the iteration order of each `Dict` and `Set` on its path (REPRO.3).

### Concurrency

#### STND.JL.27 Shared state between tasks

Default. Instantiates DSGN.14.

Code SHOULD NOT select per-task state by the value of `Threads.threadid()` (DSGN.14, STND.CONC.16).

### Docstrings

#### STND.JL.28 Docstring placement

Default. Instantiates INTPR.1, INTPR.3.

Each docstring SHOULD stand immediately before the object it documents, the docstring of a module before its `module` keyword (INTPR.1). The docstring of each documented generic function SHOULD stand on its most general method or on a declaration of the function without methods (INTPR.3). Where the behavior of a method differs from the docstring of its generic function, that method SHOULD carry a docstring that states the difference (INTPR.3).

#### STND.JL.29 Docstring opening lines

Default. Instantiates INTPR.1.

Each docstring of a function or a method SHOULD open with its signature indented by four spaces, followed by a one-line summary in the imperative mood that ends with a period (INTPR.1). Each other docstring SHOULD open with a one-line summary that ends with a period (INTPR.1).

#### STND.JL.30 Docstring sections

Default. Instantiates INTPR.1, INTPR.3.

Each heading of a docstring SHOULD be a first-level heading of the table of this provision, in the order of the table, holding the content that its row gives (INTPR.1). Each entry under `# Arguments` or `# Fields` SHOULD describe its item without restating a type that the signature or the declaration of the field states (INTPR.3).

| Heading | Content |
| --- | --- |
| `# Arguments` | Each argument and keyword argument whose meaning, units, or range of valid values the signature and the summary leave unstated |
| `# Fields` | Each field of a type, with its meaning, units, and range of valid values |
| `# Returns` | The returned value, with its units, where the summary leaves it unstated |
| `# Throws` | Each exception that the call throws, with the condition under which it throws it |
| `# Notes` | The parts of the contract of STND.CODE.3 that the entries above leave unstated, the equations and approximation of NUMER.4, and the assumptions and limits of STND.DOCS.2 |
| `# Examples` | Examples of use, each runnable one in the form of STND.JL.31 |
| `# Implementation` | What the author of a method that extends the function relies on |
| `# Extended help` | Material that the summary display of the help mode leaves out |

#### STND.JL.31 Julia doctest examples

Default. Instantiates INTPR.3, VV.8.

Each example of the work documentation that STND.DOCS.13 runs SHOULD be a doctest that the documentation build of the work runs, in a docstring or in a page of that build (INTPR.3, VV.8). Each floating-point value that such an example shows SHOULD be rounded by the example to the digits that its stated tolerance admits, or matched by a filter of the doctest that admits that tolerance (INTPR.3, VV.8).

### Checking

#### STND.JL.32 Docstring coverage checks

Default. Instantiates DSGN.1, INTPR.3.

Where a name that a package of the work declares by `export` or by `public` has no docstring, the tests of each change SHOULD fail (DSGN.1, INTPR.3). Where a docstring of such a name is missing from the pages of the documentation build, the build of each change SHOULD fail (INTPR.3).

#### STND.JL.33 Package hygiene checks

Default. Instantiates DSGN.3, REPRO.9.

The tests of each change SHOULD include a check of each package of the work for method ambiguities, unbound type parameters, exports of undefined names, stale dependencies, the presence of the bounds of STND.JL.2, and type piracy (DSGN.3, REPRO.9). The tests of each change SHOULD include a check of each module of library code against STND.JL.9 (DSGN.3).

#### STND.JL.34 Julia test run settings

Default. Instantiates VV.8, HW.7, DSGN.2.

Each change that affects a reported numerical result SHOULD run the tests that carry its evidence at least once with the production configuration, with bounds checking as that configuration sets it (VV.8, HW.7). Other than that run, each run of the tests SHOULD force bounds checking on for all code, including code inside `@inbounds` (DSGN.2, VV.8).

#### STND.JL.35 Deprecations fail test runs

Default. Instantiates DSGN.6, REPRO.7.

Other than a deprecation warning that the repository configuration lists, with its reason, as raised inside a dependency, each deprecation warning that a run of the tests raises SHOULD fail that run (DSGN.6, REPRO.7).

#### STND.JL.36 Bounds checks in production

Default. Instantiates DSGN.2, RSRC.4, REPRO.7.

The production configuration SHOULD leave bounds checking on for all code other than code inside `@inbounds` (DSGN.2). Where a measurement shows that bounds checking exceeds a stated budget, a decision record SHOULD state the measurement and the setting of the production configuration that turns bounds checking off (RSRC.4, REPRO.7).

### Foreign interfaces

#### STND.JL.37 Julia foreign call types

Default. Instantiates DSGN.4.

The type of each argument and of the result that a `ccall` or `@ccall` of the work states SHOULD have the size and the representation of the type that the foreign declaration of the function gives it (DSGN.4). Each struct whose layout the Julia source declares for a foreign interface SHOULD have its size and the offset of each of its fields compared with the foreign declaration by a test (DSGN.4).

#### STND.JL.38 Julia memory across foreign calls

Default. Instantiates DSGN.14.

Each pointer to memory that Julia manages, which the work takes by `pointer` or by another function that returns the address of such memory, SHOULD be used only inside a `GC.@preserve` block that names each object that owns that memory (DSGN.14). Each Julia object that foreign code is able to use after the call that passed it to that code returns, the object that `@cfunction` returns for a closure among them, SHOULD stay referenced by the work for as long as foreign code is able to use it (DSGN.14).

#### STND.JL.39 Julia exceptions in foreign callbacks

Default. Instantiates DSGN.5.

Each Julia function that foreign code invokes through a pointer that `@cfunction` makes SHOULD catch each exception thrown within it (DSGN.5). Where the foreign interface carries errors, an exception so caught, other than an `InterruptException`, SHOULD be converted to an error that the interface carries (DSGN.5). Each other exception so caught SHOULD be stored in an object that code of the work checks after the foreign call returns, and answered there, an `InterruptException` by being thrown again, as STND.JL.16 asks in place of a throw within the callback, and each other exception as STND.JL.15 requires (DSGN.5).

#### STND.JL.40 Julia owners of foreign resources

Default. Instantiates DSGN.14.

Each resource that foreign code creates for the work SHOULD have one owner that the contract of the interface states, and be released by the function that the contract names, through an object of the work that owns it (DSGN.14).

#### STND.JL.41 Julia arrays at foreign calls

Default. Instantiates DSGN.4.

Each array that the work passes to foreign code by a pointer to its elements SHOULD have, at the call, the element type, the order of dimensions, and the strides that the documentation of the foreign function states, or those that a test of that call confirms (DSGN.4).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-23 | Adopted. |
| 1.1 | 2026-10-24 | Minor amendment (GOV.41): STND.JL.27 drops its second sentence, which stated the lock and atomic case of STND.CONC.3 without Julia content, cites STND.CONC.16, of whose second sentence its first is the Julia form, and instantiates DSGN.14, as STND.CONC.16 does, in place of DSGN.15; the class paragraph states its onset on that basis; the Notes cite STND.CONC.3 for the protection of state that tasks share, with the Julia examples, and STND.CONC.23 as the model-neutral rule of which STND.JL.24 is the Julia form, and cite STND.OFFLD and HW.GPU for offload and STND.MPI and STND.CONC for distributed computing in place of STND.CODE and the project instruments alone, and cite GUARD.16 for the threat model that records a source of input as trusted; References lists STND.CONC, STND.MPI, STND.OFFLD, HW.GPU, and GUARD. |
| 1.2 | 2026-10-25 | Minor amendment (GOV.41): Terms import Untrusted input from STND.CODE and drop this standard's own definition, and place each function that a package of the work declares by `export` or by `public` in the public interface that the term of STND.CODE takes in, and keep the index that `eachindex`, `axes`, or `CartesianIndices` produces as valid by construction; Terms define Foreign interface; STND.JL.13 cites STND.CODE.6, and STND.JL.15 STND.CODE.14, for the rule of which each is the Julia form, and neither changes otherwise; STND.JL.1 and the third sentence of STND.JL.3 yield to a version of Julia that STND.CODE.19 fixes; Terms import High-assurance code and High-assurance coding standard; new STND.JL.36 (default, DSGN.2, RSRC.4, and REPRO.7) has the production configuration leave bounds checking on outside `@inbounds` unless a measurement and a decision record show its cost, the Julia counterpart of STND.CXX.27; new STND.JL.37 to STND.JL.41 (defaults, DSGN.4, DSGN.14, and DSGN.5) give the types and layouts, the lifetime of memory, the exceptions of callbacks, the ownership of resources, and the layout of arrays at foreign interfaces; the Purpose lists them; the Notes cite the provisions of STND.CODE of which this standard gives Julia forms, and state the facts and the onset of each new provision. |
