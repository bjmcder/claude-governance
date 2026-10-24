# Rust standard (STND.RUST) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 118 (2026-10-24). This reading copy is composed from the per-provision files in STND/RUST/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the coding practice that is specific to Rust. It adds to STND.CODE, STND.CONC, STND.DEPS, and STND.DOCS only what the language makes necessary. It covers the edition, the toolchain, and the build settings that change what code means (STND.RUST.1 and STND.RUST.2); unsafe code: the safety argument at each unsafe construct, the safety conditions that unsafe functions and traits state, sound modules, the list of modules that hold unsafe code, and the conditions on which no safety argument rests (STND.RUST.3 to STND.RUST.8); panics: the panic strategy, panic safety, catching, destructors, and locks after a panic (STND.RUST.9 to STND.RUST.13); failures and their reporting (STND.RUST.14 to STND.RUST.18); integer arithmetic and conversions (STND.RUST.19, STND.RUST.20, and STND.RUST.21); unsafe code across threads, and asynchronous code (STND.RUST.22, STND.RUST.23, and STND.RUST.24); foreign interfaces (STND.RUST.25 to STND.RUST.28); build-time code, features, and lock files (STND.RUST.29 to STND.RUST.32); and the checks of Rust code, unsafe code among it, with the claims that rest on them (STND.RUST.33 to STND.RUST.36).

STND.RUST.14, STND.RUST.15, and STND.RUST.16 instantiate PRIME.4, STND.RUST.36 instantiates PRIME.2, and STND.RUST.7 instantiates GOV.48 and binds agents alone; these five are binding at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is agnostic of toolchain release, platform, vendor, and tool: its provisions name constructs of the language and of its core and standard libraries, and no particular release, edition, compiler, linter, detector, package index, or build tool, which the repository configuration and the dependency record of each work choose (GOV.18). The rules of concurrency that hold for every model are in STND.CONC, and the rules for dependencies in STND.DEPS; this standard gives their Rust forms only where Rust sets a trap of its own.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them; Dependency record has the meaning that STND.DEPS gives it; Concurrent task, Asynchronous operation, Shared mutable object, Protection, Data race, Lock, and Suspension point have the meanings that STND.CONC gives them. Each thread and each task that the work spawns is a concurrent task, each future is an asynchronous operation, and each await of a future is a suspension point. The panic strategy, overflow checks, and debug assertions of a build are execution settings.

| Term | Definition |
| --- | --- |
| Crate | The unit that the Rust compiler compiles at one time: a library or a program, with the modules that its root file declares. |
| Library code | The Rust source of the crates of the work that other crates use, other than their tests, examples, benchmarks, and build-time code. |
| Untrusted input | Data that reaches the work from outside its own code, including the arguments of each function that library code makes visible outside its crate, other than data from a source that the threat model of the project records as trusted. |
| Undefined behavior | Behavior that the Rust Reference, at the release of the toolchain that builds the code, states to be undefined, and behavior that the specification of another language states to be undefined in code of that language that the work calls. |
| Unsafe operation | An operation that the language admits only within an unsafe block or within the body of an unsafe function. |
| Unsafe attribute | An attribute whose use the language makes the obligation of its author to keep free of undefined behavior, an attribute that exports a symbol under a fixed name among them. |
| Unsafe construct | An unsafe block, an unsafe function, an unsafe trait, an unsafe implementation of a trait, a use of an unsafe attribute, and a block that declares foreign functions or foreign statics. |
| Safety condition | Of an unsafe operation, an unsafe function, an unsafe trait, or an unsafe attribute: a condition that the language or the documentation of the item states, that its caller, its implementor, or the author of the attribute establishes, and without which the program has undefined behavior. |
| Safety argument | A comment at an unsafe construct that states each safety condition on which the construct relies and why that condition holds there. |
| Sound module | A module of the work through whose visible items no code outside the module, other than code that holds an unsafe construct of its own, is able to cause undefined behavior, whatever values it passes and in whatever order it calls them. |
| Panic strategy | Of a build: whether a panic unwinds the stack of its thread, running the destructors of the values that the stack holds, or ends the process at once. |
| Future | A value of a type that implements the `Future` trait of the core library. |
| Cancellation safe | Of a future: such that dropping it at each of its suspension points before it completes loses no data that it has taken from another object, and leaves each object that it reaches in a state that the invariants of that object admit. |
| Foreign interface | An interface through which Rust code of the work calls, or is called by, code that does not follow the Rust rules of ownership, borrowing, and unwinding: a function that a block of foreign declarations declares, a function of the work exported with a foreign ABI, and a callback that the work passes to such code. |
| Build-time code | A build script or a procedural macro, of the work or of a dependency: code that a build compiles and runs on the machine of the build before or while it compiles the crate that uses it. |
| Feature | A named option of conditional compilation that a crate declares in its package metadata, and that the crate or the crates that depend on it enable. |
| Lock file | The file that records, for a set of crates that the work builds together, the exact revision and the integrity digest of each package that their builds resolve. |

## Notes

Direction and sources. The direction of 2026-10-24 for this standard asks for the coding practice that Rust makes necessary, agnostic of toolchain release and timeless, citing STND.CONC for every model-neutral rule of concurrency and STND.CODE and STND.DEPS for what they hold. The custodian's standing directions keep it agnostic of platform, compiler, vendor, implementation, framework, and tool, and keep strict determinism an option where it is feasible and not a requirement unless the acceptance criterion or the consequence class demands it (STND.VVUQ.82, STND.VVUQ.83). Each provision therefore names a construct of the language or of its core and standard libraries, and states an outcome that a reviewer or a check decides; the Notes name a tool or a library only to explain a hazard. The source is the research note research/rust-notes/rs1-rust-language.md (rs1 below), whose sources are the Rust Reference, the Rustonomicon, the documentation of the standard library and of the build and package tool that the Rust project distributes, the API guidelines, the documentation of one asynchronous runtime, an experience report of one company, and peer-reviewed studies. Most of them were read as extracts that a retrieval tool wrote, and the Reference and the guides are living documents read at their current text. A fact that rs1 does not support is marked unverified.

What the corpus already holds. The standard adds Rust content to provisions that already hold the outcome, and does not restate them (GOV.31). STND.CODE.3 asks for the contract at each declaration, and the sections of a Rust documentation comment on safety, panics, and errors are its form (STND.RUST.4, STND.RUST.17). STND.CODE.4 and STND.CODE.5 name the static checks, the suppression of a finding at its location with its reason, and the layout tool, so the lints and the formatter of Rust, and an attribute that allows a lint with its reason, need no provision here beyond STND.RUST.33. STND.CODE.6 keeps each check of untrusted input in every build, and STND.RUST.16 gives its Rust forms. STND.CODE.7 forbids discarding a failure that PRIME.4 lists, which reaches a `Result` bound to the wildcard pattern, a conversion that drops its error, and a caught panic left unanswered; STND.CODE.12 asks the reason of each other discard. STND.CODE.13 groups the statements of each body by step in Rust as in every language. The naming conventions of the language are checked by lints of its compiler, which STND.CODE.4 covers. STND.DOCS.13 runs the examples of the work documentation, and the documentation tests of Rust are one form of it. STND.DEPS.6 verifies each fetched component against its integrity digest, which the lock file records; STND.DEPS.7 checks advisories before each release, which a database of advisories for the packages of the language publishes (rs1, section 10); STND.DEPS.8 records the revision of the compiler with each result; STND.DEPS.10 lets the package metadata and the lock file serve as the dependency record where they carry each package's reason and license identity; and STND.DEPS.1 and STND.DEPS.4 govern the adoption and the review of each dependency. The concurrency and numerical provisions that apply are named in the paragraphs on them. STND.CODE.9 concerns tests that reach outside the provisioned environment, and not build-time code, which is why STND.RUST.29 holds the rule on the network for build-time code.

Builds. The edition is chosen for each crate, crates of different editions interoperate, and a crate whose package metadata names no edition is compiled at the oldest one (rs1, section 9). A declared oldest release of the toolchain makes the build tool report an error on an older release, and a declaration that no check confirms drifts from the code, so STND.RUST.1 builds and tests at that release, as STND.JL.3 does for Julia. Editions have moved defaults that concern unsafe code, the marking of unsafe attributes and the treatment of unsafe operations in the body of an unsafe function among them, and which edition moved each is unverified (rs1, section 9); a change of edition is therefore a change of the computational environment under HW.7 and of a pinned revision under STND.DEPS.5, reviewed under STND.DEPS.4. The settings of STND.RUST.2 change what code means: the panic strategy decides whether destructors run after a panic and whether a panic is able to be caught; overflow checks decide whether an integer operation panics or wraps on overflow; debug assertions decide whether `debug_assert!` runs; an enabled target feature lets the compiler emit instructions that a processor without the feature does not execute, which is undefined behavior; and features select the code that a crate compiles (rs1, sections 3, 6, 10, and 11). The target instruction set changes delivered arithmetic, which HW.5 states, and a setting that targets the processor of the build machine ties the program to processors that have its features (rs1, section 11).

Unsafe code. An unsafe block states that the obligations of the operations inside it are met; the keyword moves the duty to avoid undefined behavior from the compiler to the author (rs1, section 1, from the Reference). STND.RUST.3 puts the argument at the construct, where a reviewer checks it against the operations, which is the convention of a comment opening with "SAFETY:" that lints of one linter check; the descriptions of those lints are unverified (rs1, section 11). The safety conditions follow the validity rules of the Reference: producing a value with an invalid bit pattern, a null or dangling reference, or a second live mutable reference to the same bytes is undefined behavior even without an access; uninitialized memory stays in the type that the standard library provides for it until it is written; and a reinterpretation of bits or an all-zero value is valid only for a type that admits that pattern (rs1, sections 1 and 2). A call of a function compiled with a target feature has the safety condition that the processor has the feature, which a check at run time or a build restricted to such processors establishes; an attribute that exports a symbol under a fixed name has the condition that no other symbol takes that name; and each operation whose name marks it unchecked, unchecked integer arithmetic and the assertion that a branch is unreachable among them, is undefined behavior where the condition it assumes fails (rs1, sections 1, 2, and 11). STND.RUST.3 is therefore also the Rust form of what STND.CXX.24 asks of an assumption stated to a C++ compiler. The language has admitted unsafe operations in the body of an unsafe function without a block of their own at some editions, and a lint asks for the block; the second sentence of STND.RUST.3 asks for it in either case. The Reference states that the list of undefined behavior is able to grow or shrink and that the rules of aliasing are not settled, and rs1 reports two experimental models of aliasing, the newer of which rejects fewer programs; a safety argument that holds under the stricter reading holds under both, and STND.RUST.35 has the record of a check name the rules that the check applied (rs1, sections 1, 11, and 12). STND.RUST.4 asks for the "Safety" section that the API guidelines name; one study found the documentation of the unsafe functions of the standard library inconsistent and insufficient, and defined 19 safety properties over 416 of them (rs1, section 12, S57).

Soundness is a property of the interface of a module. The Reference calls unsafe code sound where no safe code that uses it is able to reach undefined behavior through it, and a module whose interface admits undefined behavior is unsound even where no present caller reaches it (rs1, section 1). The module is the unit of the argument because the privacy of the language stops code outside a module from changing its private fields, so a safety argument that rests on an invariant of those fields rests on the code of the whole module, and STND.RUST.5 makes the module sound as a whole. A machine-checked proof for a subset of the language states the verification condition that each library with unsafe code meets to be a safe extension, and verified the reference-counted pointers, the cells, and the locks of the standard library against it (rs1, section 1, S40). In a study of all memory-safety vulnerabilities reported for Rust through 2020, each required unsafe code, and many were soundness defects that no present caller triggered (rs1, section 12, S42); another found unsafe code mostly simple and well encapsulated, and used most extensively at interfaces to other languages (S50). STND.RUST.6 makes the unsafe surface a list that a reviewer reads, and the lint of the compiler that rejects unsafe code, which is off by default, makes each other module an exception that the check reports (rs1, section 11). A claim that a crate is safe rests on the unsafe code of its dependencies as well: one study found unsafe code in the call chain of more than three quarters of the libraries it examined (rs1, section 12, S56), which is why STND.RUST.36 has a claim of soundness state the code that its means covered.

STND.RUST.8 states what the language does not promise. A destructor is not guaranteed to run, because safe code is able to leak a value or forget it, and the documentation of the forgetting function states that unsafe code allows for that (rs1, section 1, S5). The destructor of a value that the module keeps to itself, a guard local to one function among them, runs during unwinding, so STND.RUST.10 admits a guard; a value that the module hands to code outside it, an iterator that drains a container among them, is able to be forgotten, so STND.RUST.8 has the module leave its state valid before such a value escapes. Poisoning is advisory: the documentation of the mutual-exclusion lock states that unsafe code does not rely on it for soundness, a panic during the unwinding of another leaves the lock unpoisoned, an exception of another language does not poison it, and a read-write lock is poisoned only by a panic of a writer (rs1, section 3). A panic is able to occur in safe code at each call of code that the module does not define, so STND.RUST.8 rests no argument on its absence there; within the module, an argument that shows a path free of panics rests on that path. Panic safety, higher-order invariants, and missing bounds on implementations of `Send` and `Sync` are the three patterns by which one static analyzer found 264 previously unknown memory-safety defects in the public register of Rust packages (rs1, sections 3 and 12, S46).

Agents and unsafe code. STND.RUST.7 binds every agent at every class by its own force (GOV.48), and STND.INSTR.10 carries it into the agent instructions. Unsafe code without an argument compiles and passes its tests, and its defect stays latent until another caller, an optimizer, or a stricter model of aliasing reaches it; the reviewer and the human owner verify agent-written unsafe code against its argument, and an absent argument defeats that check, which is the silent misalignment that STND.DRAFT names. Its cost is the wording of one comment at each construct that the agent writes or changes, as STND.PY.4 costs one annotation, so its cost is wording alone; that it raises no floor (GOV.11) is a decision for the custodian. A run of a tool is not bound at CSQ4, so the checks of STND.RUST.33 and STND.RUST.34 stay defaults from CSQ3.

Panics. A build either unwinds on a panic or aborts, the default depends on the target, and under the aborting strategy the optimizer assumes that no unwinding crosses Rust frames, so a catch of a panic does nothing and a destructor that a crate relies on after a panic does not run (rs1, section 3). STND.RUST.9 has a crate that relies on unwinding say so, and has the tests run under each strategy that the work ships. The Rustonomicon states that a caller-supplied clone "is totally free to panic", and that unsafe code that reads a duplicated value after such a panic reads uninitialized memory or frees a value twice; it asks for minimal exception safety, which STND.RUST.10 states as an outcome (rs1, section 3, S8). The standard library states that catching a panic is not a general mechanism for handling errors and might not catch every panic, so STND.RUST.11 keeps it at boundaries: the root of a thread or task, a foreign interface (STND.RUST.26), and a component that a design isolates; dropping the payload of a caught panic is able to panic in turn (rs1, section 3, S12). A destructor that panics during unwinding is likely to end the process (rs1, section 3, S13), and a destructor has no way to return a failure, so a release that reports one, the closing of a file or the flush of a buffered writer among them, is lost when the destructor discards it (unverified for each type of the standard library); STND.RUST.12 asks for a release operation that returns the failure, as STND.CXX.21 does for C++. The three sentences of STND.RUST.12 concern one destructor and its release, and apply together. Locks of other libraries do not all poison (unverified for each library), so STND.RUST.13 lets the protected object carry its own mark of a broken state.

Failures. STND.RUST.14 lists the responses that PRIME.4 admits in Rust, and the other provisions that need a response refer to it. A panic is the Rust form of raising an exception: under the unwinding strategy it ends its thread unless it is caught, a catch that leaves it unanswered discards it, which STND.CODE.7 forbids, and a spawned thread that panics returns the payload to the handle that joins it, while a dropped handle detaches the thread, which STND.CONC.1 and STND.CONC.2 govern (rs1, section 3, S44). Under the aborting strategy, a panic halts with the diagnosis that the panic hook writes; that the default hook writes the message and the location of the panic to standard error is unverified in rs1, and the second sentence of STND.RUST.14 keeps a replaced hook from removing the diagnosis that PRIME.4 asks for. STND.RUST.15 is the Rust form of STND.CXX.17. The standard library marks `Result` so that the compiler warns on a call that ignores it (unverified in rs1, which did not retrieve that fact), so a function that returns its failure in a `Result` meets it; a status that a foreign function returns as an integer, and a failure returned as a Boolean value, carry no such mark, and an attribute on the function or a wrapper that returns a `Result` meets it. STND.RUST.16 is the Rust form of STND.CODE.6: `debug_assert!` does not run where debug assertions are off, overflow checks are on by default only where debug assertions are on, and the Reference leaves a build without them free to panic or to wrap silently (rs1, section 6). Its first sentence also reaches the checks of CPS.5 and CPS.9 where those apply, as STND.CXX.18 does for C++, since a check that an execution setting removes does not run in the builds that command the hardware. A signed division of the least value by negative one, and a division by zero, panic in every build, which is a fact for the author and asks nothing (rs1, section 6). STND.RUST.17 follows the book of the Rust project and the API guidelines: a failure that a caller causes by its data and is able to handle is returned as a `Result`, and a panic answers a broken precondition, guarantee, or invariant, which the "Panics" section of the documentation states (rs1, section 7). STND.RUST.18 keeps `unwrap` and `expect` in library code to places where the code shows the failure impossible; the message of `expect` meets it where the message states that reason. Indexing a slice panics on an index out of range, and STND.RUST.17 governs an index that untrusted input gives.

Arithmetic. Integer operators panic on overflow under overflow checks, and otherwise panic or wrap in two's complement at the discretion of the implementation; methods whose names state checked, wrapping, saturating, and overflowing behavior, a wrapping integer type, and newer methods that panic on overflow in every build make the intended behavior visible, and their names move between releases (rs1, section 6). STND.RUST.19 asks for that visibility where it matters: untrusted input that overflows passes the checks of DSGN.2 undetected in a build without overflow checks, as STND.JL.17 states for Julia, and hashing and generators of random numbers rely on wraparound on purpose. A conversion by `as` truncates an integer, and saturates a floating-point value, a NaN becoming zero, without a report (rs1, sections 2 and 6); applied to invalid input it is the silent clamping that PRIME.4 forbids, which STND.RUST.20 guards against with a stated reason or a fallible conversion. A restriction lint that reports each operation able to overflow exists in one linter, and where it runs is a choice of configuration (STND.CODE.4). STND.RUST.21 is the Rust form of STND.JL.34: tests with overflow checks and debug assertions enabled detect an overflow that a build without them wraps silently, and the evidence that HW.7 asks for comes from the build that produces the result.

Concurrency. Safe Rust excludes data races, and does not exclude race conditions, deadlock, or leaks, which the Reference does not count as unsafe (rs1, sections 2 and 4). STND.CONC governs them, and an object behind a lock type of the standard library carries its protection in its type, which meets the statement of STND.CONC.3 at the declaration. The atomics of Rust follow the C++ memory model without its consume ordering (unverified whether this is fixed), so STND.CONC.4 applies to them unchanged. A lock that its holder acquires again panics or deadlocks, and the priority of a read-write lock between readers and writers is unspecified, so a second read is able to wait behind a writer (rs1, section 4), which STND.CONC.7 covers. Send and Sync are unsafe traits that the compiler derives from the fields of a type, and other unsafe code assumes them correct, so a wrong manual implementation is undefined behavior; a lock guard and a reference-counted pointer without atomic counts are not Send (rs1, section 4, S14 and S15). STND.RUST.22 asks for the argument of each manual implementation, the bounds of its type parameters, and an argument that no other thread changes what a check established, since a race condition combined with unsafe code is able to break memory safety (rs1, section 4, S16). A future does nothing until it is polled, so STND.CONC.1 has each one awaited, spawned, or dropped by a decision (rs1, section 5). Dropping a future cancels it at its current suspension point, the language has no marker of cancellation safety, and one experience report calls each await a point at which the function is able to return (rs1, section 5, S49); STND.CONC.13 governs the propagation of the cancellation, and STND.RUST.23 adds what that mechanism makes necessary. The documentation of one runtime classifies the futures of its own library by cancellation safety, which is the form that the first sentence of STND.RUST.23 asks of the work (rs1, section 5, S19); a drop that the language runs asynchronously is unstable, and its status moves. STND.CONC.8 already recommends against reaching a suspension point while a lock is held; STND.RUST.24 makes that mechanical, since lints for a guard and for a borrow of a cell held across an await exist in one linter, and a guard of the lock of the standard library held across an await makes the future not Send (rs1, section 5). A blocking call or a long computation on an executor thread starves the other tasks of that thread, which STND.CONC.15 governs; the runtime is a library that the application selects, so an executor is a pool under STND.CONC.17 and STND.CONC.18, under which library code takes it from its caller or returns a future; and state local to a thread is lost or shared when a scheduler that steals work moves a task, which STND.CONC.16 governs (rs1, section 5). The run-time detectors and the checkers that explore schedules fit STND.CONC.25, STND.CONC.26, and STND.CONC.27.

Foreign interfaces. A type has the layout of the corresponding C type only under the representation attribute that fixes it, and the absence of that attribute leaves the field order to the compiler (rs1, section 8, S28); a transparent representation fixes a wrapper to the layout of its one field (inference in rs1). STND.RUST.25 has the layout checked against the foreign declaration, since the attribute fixes the rules and not the agreement with a header. References, owning boxes, and function pointers are never null in Rust, so STND.RUST.25 has a null from the foreign side received as a raw pointer or an optional type (rs1, section 8). An empty enumeration used as an opaque foreign type leads the compiler to assume that no value exists, and the guide shows a struct form instead (rs1, section 8). An unwinding that reaches a function declared with a non-unwinding ABI ends the process, and one that enters Rust frames from such a declaration is undefined behavior; the Rustonomicon calls the catch of an exception of another language undefined, and the Reference calls it unspecified, either aborting or returning an opaque error, and both are recorded (rs1, section 3). STND.RUST.26 is the Rust form of STND.CXX.22, and STND.RUST.27 covers the other direction and the nonlocal jump, which runs no destructor of the frames it skips (rs1, section 8). Ownership follows STND.CXX.20: the guide warns against building the owning box over memory of a foreign allocator, and STND.RUST.28 has a wrapper with a destructor receive each foreign resource first (rs1, section 8). A callback that foreign code calls after the Rust data it reaches is released is a use after its lifetime, which STND.CONC.5 governs. Undefined behavior in the foreign code is undefined behavior of the whole program (rs1, section 8), which is why the term Undefined behavior includes it.

Build-time code and packages. The build tool compiles and runs the build script of each package before it builds the package, and a build script performs whatever its author writes; a procedural macro has the resources of the compiler and the same concerns (rs1, section 10, S33 and S34). Each runs for each dependency that has one, with the authority of the account that builds, whether or not the work calls the dependency. A vendor reported, for 2026-08-20, three packages published from a compromised account with a new dependency whose build script fetched and ran a payload (unverified; one report). GUARD.17 governs the security of builds against the supply-chain row that STND.THRT.2 adds to every threat model, STND.DEPS.6 and STND.DEPS.7 bind at every class, and a build of an unreviewed revision in an environment without secrets and with its network access limited to the fetch of the components that the lock file records is one means of that secure practice, which the threat model of each project decides. STND.RUST.29 and STND.RUST.30 add the record and the review that build-time code makes necessary, so that STND.DEPS.1 weighs the exposure of the work to compromise through the supply chain of each dependency from evidence. The documentation of the build tool asks that features be additive, because it enables the union of the features that each crate of a build requests of a dependency, so a feature that another crate enables changes the code of this one, and a feature that removes a check is enabled for every crate of the build (rs1, section 10, S32; the second clause by inference). STND.RUST.31 tests no features, the defaults, and all features, which detects features that exclude one another; testing each combination costs a number of builds that grows exponentially with the number of features. The lock file records the exact revision of each package (rs1, section 10, S31), and STND.RUST.32 is the Rust form of STND.JL.4; the guidance of the build tool on lock files of libraries was not retrieved (unverified), and the provision commits the lock file for each set of crates that the work builds together, so that the checks of a library are reproducible as STND.CODE.9 asks, while the crates that depend on the library resolve their own.

Checking. STND.RUST.33 is the Rust form of STND.CXX.25 and STND.PY.2. An interpreter that executes a program on an abstract machine detects accesses out of bounds and after release, data races, violations of the aliasing rules, and leaks, and its documentation states that it does not catch every violation, does not show that code is sound, tests one of many possible executions, and has no access to most interfaces of the platform or to foreign code (rs1, section 11, S35). A report of undefined behavior shows a defect, and a clean run shows the absence of a report on the executions observed; STND.RUST.34 asks for the run where the means of the work include such a detector, so that a target that it does not support blocks no work, and STND.RUST.35 states its limits as STND.CONC.27 does for a check of concurrency. Detectors that instrument a compiled build cover foreign code, and their support for Rust is unverified in rs1, so the second sentence of STND.RUST.34 names the outcome. STND.RUST.36 is the Rust form of STND.CXX.29: PRIME.2 already forbids claiming a check that was not run and misrepresenting evidence, and a claim that a crate is sound, resting on a clean run of a detector or on unchecked unsafe code in a dependency, misrepresents what was checked.

Numerics. Primitive floating-point operations round to nearest, ties to even; the bit pattern of a NaN is neither portable nor fully deterministic; the functions of the standard library for powers, exponentials, logarithms, and trigonometry have unspecified precision that varies by platform and by release and is able to vary within one execution, while the square root and the fused multiply-add are exact; and changing the default rounding or exception behavior is in general undefined behavior (rs1, section 11, S37 and S38). These are inputs to provisions that already hold the outcome: NUMER.5 records the working precision with the delivered arithmetic that HW.5 states, NUMER.16 and NUMER.17 govern approximations and fused or vectorized paths retained for speed, STND.VVUQ.3 judges a NaN whatever its payload, and REPRO.3 declares what varies between runs. No provision is needed here. Whether the language offers a mode of relaxed floating-point semantics on its stable releases is unverified.

Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or a provision of HW, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row. STND.RUST.25 rests on DSGN.4, and STND.RUST.26 and STND.RUST.27 on DSGN.5, and they apply from CSQ2, each provision as one bundle. STND.RUST.35 instantiates INTPR.10, whose documentation of limits STND.CLASS.10 starts at CSQ2, and applies from CSQ2, as STND.CONC.27 does. The second sentence of STND.RUST.11 rests on INTPR.8 and applies from CSQ1; its first sentence applies from CSQ3. STND.RUST.2 and the first sentence of STND.RUST.21 instantiate HW.5 or HW.7, each of which also instantiates the contracts of DSGN.5 that STND.CLASS.10 starts at CSQ2; they apply from CSQ3 through the other provisions they instantiate, and so tighten above the floor (PRIME.15) for work that HW binds, at the cost of a record or one run of the tests. STND.RUST.13 and STND.RUST.22 state what a protocol of DSGN.15 uses and not how its invariants are verified, as STND.CONC.3 to STND.CONC.9 do, and apply from CSQ3; STND.RUST.24 is a static check of such a protocol and applies from CSQ3. The first sentence of STND.RUST.19 rests on the checking of preconditions where untrusted data enters, and the second sentence of STND.RUST.21 and the second sentence of STND.RUST.31 on the retention of checks for verification, which DSGN.2 asks from CSQ3, and not on the checking of postconditions that STND.CLASS.10 starts at CSQ1. STND.RUST.33 and STND.RUST.34 ask for mechanical checks (DSGN.3) from CSQ3; the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 starts at CSQ0, stays with that row. The tests of STND.RUST.1, STND.RUST.9, and STND.RUST.31 are tests under VV.1 and VV.8 that compare with no reference oracle produced without the implementation, and apply from CSQ3. Each other default, the provisions on unsafe code among them, rests on no row and applies from CSQ3. STND.RUST.8, STND.RUST.12, STND.RUST.22, STND.RUST.23, STND.RUST.25, STND.RUST.26, STND.RUST.27, STND.RUST.29, STND.RUST.31, and STND.RUST.33 each hold three modals that state one rule for one construct, one interface, or one set of checks, and each is never applied apart: its sentences share one onset, so that the provision applies as one bundle.

Floor. STND.RUST.14 asks for the responses that PRIME.4 already requires, and its second sentence only keeps the actionable diagnosis that PRIME.4 names. STND.RUST.15 costs one attribute or one return type for each function that returns a listed failure; without it a listed failure is able to pass silently. STND.RUST.16 forbids two constructs that leave a check of untrusted input removable by an execution setting, which STND.CODE.6 already forbids, and the same construct for a check that CPS.5 or CPS.9 already requires in the builds that command the hardware. STND.RUST.36 asks of a claim of soundness only that it state the means that checked it and not extend beyond what they covered, which PRIME.2 already requires, at the cost of one sentence. STND.RUST.7 costs an agent the wording of a comment. Each binds at every class, CSQ4 included, and none asks for work that PRIME.4, PRIME.2, or GOV.48 does not already ask; that none of them raises the floor (GOV.11) goes to the custodian as a decision. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no default raises the floor (GOV.11).

Existing Rust source conforms to the default provisions when a change next touches it.

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.INSTR | Agent instructions |
| STND.JL | Julia standard |
| STND.PY | Python standard |
| STND.THRT | Threat-model template |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Builds

#### STND.RUST.1 Declared edition and toolchain

Default. Instantiates SIMPL.6, REPRO.9, VV.8.

The package metadata of each crate of the work SHOULD state its edition and the oldest release of the Rust toolchain that it supports (SIMPL.6, REPRO.9). The checks of each change SHOULD build and test each crate of the work with that oldest release (VV.8).

#### STND.RUST.2 Rust build settings stated

Default. Instantiates SIMPL.6, REPRO.2, HW.5.

The repository configuration SHOULD state, for each build from which the work reports a result or makes a release, its panic strategy, whether its overflow checks and its debug assertions are enabled, its target instruction set with each target feature that it enables, and the features that it enables for each crate of the work (SIMPL.6, REPRO.2, HW.5).

### Unsafe code

#### STND.RUST.3 Safety arguments at unsafe code

Default. Instantiates DSGN.1, SIMPL.11, REPRO.7.

Each unsafe block, each unsafe implementation of a trait, and each use of an unsafe attribute SHOULD carry a safety argument at its location (DSGN.1, SIMPL.11, REPRO.7). Within the body of an unsafe function, each unsafe operation SHOULD stand in an unsafe block that carries its safety argument (SIMPL.11).

#### STND.RUST.4 Stated safety conditions

Default. Instantiates DSGN.1.

In addition to what STND.CODE.3 asks, the documentation comment of each unsafe function and each unsafe trait of the work SHOULD state each safety condition that its callers or its implementors establish (DSGN.1).

#### STND.RUST.5 Sound modules

Default. Instantiates DSGN.1, SIMPL.11.

Each module of the work that holds an unsafe construct SHOULD be a sound module (DSGN.1, SIMPL.11). Each safety argument SHOULD rest only on conditions that the module of its unsafe construct establishes for every use of its visible items, and not on the uses that code outside the module makes of them at present (DSGN.1).

#### STND.RUST.6 Listed unsafe modules

Default. Instantiates SIMPL.11, DSGN.3.

The repository configuration SHOULD list each module of the work that holds an unsafe construct (SIMPL.11). A static check SHOULD reject each unsafe construct of the work outside the modules that that list names (DSGN.3).

#### STND.RUST.7 Agent safety arguments

Binding. Instantiates GOV.48, DSGN.1.

An agent SHALL write the safety argument that STND.RUST.3 asks at each unsafe block, unsafe implementation of a trait, and use of an unsafe attribute that it writes or changes, or the form that an alternative adopted by a project instrument in place of STND.RUST.3 requires (GOV.48, DSGN.1). An agent SHALL state the safety conditions that STND.RUST.4 asks in the documentation comment of each unsafe function and unsafe trait that it writes or changes, or the form that an alternative adopted by a project instrument in place of STND.RUST.4 requires (GOV.48, DSGN.1).

#### STND.RUST.8 Soundness without destructors or poisoning

Default. Instantiates DSGN.1.

A safety argument SHOULD NOT rest on the running of the destructor of a value that code outside its module is able to reach (DSGN.1). A safety argument SHOULD NOT rest on the poisoning of a lock (DSGN.1). A safety argument SHOULD NOT rest on the absence of a panic in code that the module of its unsafe construct does not define (DSGN.1).

### Panics

#### STND.RUST.9 Panic strategy relied upon

Default. Instantiates DSGN.1, VV.1.

Where a crate of the work relies on unwinding, to catch a panic or to run a destructor after one, its documentation SHOULD state that it requires the unwinding panic strategy (DSGN.1). The tests of each change SHOULD run under each panic strategy with which the work builds a release or a reported result (VV.1).

#### STND.RUST.10 Panic safety of unsafe code

Default. Instantiates DSGN.1, DSGN.14.

Where unsafe code leaves an object in a state that the validity rules of its type or the invariants of its module do not admit, it SHOULD call code that its module does not define only after it restores an admitted state, or under a guard that restores such a state on each path by which a panic leaves that call (DSGN.1, DSGN.14).

#### STND.RUST.11 Panics caught at boundaries

Default. Instantiates SIMPL.6, INTPR.8.

Code SHOULD catch a panic only at the root of a thread or a task, at a foreign interface, or at the boundary of a component that its design isolates from the rest of the process (SIMPL.6). The response to each panic so caught SHOULD carry a diagnosis that holds the message of the panic (INTPR.8).

#### STND.RUST.12 Destructors without panics

Default. Instantiates DSGN.1.

Each `Drop` implementation of the work SHOULD return without a panic on every path (DSGN.1). Where the release of a resource is able to report a failure that affects a result, the type that owns the resource SHOULD provide an operation that releases it and returns that failure, for its owner to call before the result is relied upon (DSGN.1). Where a `Drop` implementation detects a failed release, it SHOULD respond by a response of STND.RUST.14 other than a panic, or as STND.CODE.12 provides (DSGN.1).

#### STND.RUST.13 Locks after a panic

Default. Instantiates DSGN.15.

Where a panic is able to leave the object that a lock protects in a state that its invariants do not admit, the code that next acquires the lock SHOULD detect that state, by the poisoning of the lock or by a mark that the object carries, and re-establish those invariants or pass the failure to its caller before it uses the object (DSGN.15).

### Failures

#### STND.RUST.14 Rust responses to listed failures

Binding. Instantiates PRIME.4.

Where code detects a condition that PRIME.4 lists, it SHALL panic, return the condition in its result, halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade visibly with a diagnosis (PRIME.4). Where the work replaces the hook that runs at a panic, the replacement SHALL deliver the message and the location of each panic to the operator or to the record of the run (PRIME.4).

#### STND.RUST.15 Unignorable failure results

Binding. Instantiates PRIME.4.

Each function of the work that returns a failure of a kind that PRIME.4 lists SHALL return it in a type, or be declared with an attribute, by which the compiler diagnoses each call that ignores the returned value (PRIME.4).

#### STND.RUST.16 Untrusted input and execution settings

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9.

A check of untrusted input, or a check that CPS.5 or CPS.9 requires, SHALL NOT be written with an assertion that an execution setting removes, `debug_assert!` and its variants among them (PRIME.4, DSGN.2, CPS.5, CPS.9). Code SHALL NOT reject untrusted input only by the overflow checks that an execution setting enables (PRIME.4, DSGN.2).

#### STND.RUST.17 Recoverable failures as results

Default. Instantiates DSGN.1.

Where a caller of library code is able to cause a failure by the data that it passes and to handle that failure, the library code SHOULD report the failure by a returned `Result` (DSGN.1). In addition to what STND.CODE.3 asks, the documentation comment of each function that library code makes visible outside its crate SHOULD state each condition under which the function panics and each error that it returns (DSGN.1).

#### STND.RUST.18 Reasoned unwrap in library code

Default. Instantiates DSGN.1, REPRO.7.

In library code, each call of `unwrap`, of `expect`, or of another method that panics on a receiver that holds no value or holds an error SHOULD carry at its location the reason that its receiver holds a value there (DSGN.1, REPRO.7).

### Integer arithmetic

#### STND.RUST.19 Explicit integer arithmetic

Default. Instantiates DSGN.2, SIMPL.6.

Where an integer operation on untrusted input is able to exceed the range of its type, code SHOULD detect that by an operation that reports overflow in every build, or by a check of range before the operation (DSGN.2). Where code relies on the wraparound of an integer operation, it SHOULD use an operation or a type whose name states that it wraps (SIMPL.6).

#### STND.RUST.20 Narrowing conversions stated

Default. Instantiates DSGN.1, SIMPL.6.

Each conversion by `as` that narrows an integer, changes its signedness, or converts a floating-point value to an integer SHOULD carry at its location the reason that the value lies in the range of the target type, or be replaced by a conversion that reports a value outside that range (DSGN.1, SIMPL.6).

#### STND.RUST.21 Checked builds under test

Default. Instantiates VV.8, HW.7, DSGN.2.

Where a build from which the work reports a numerical result disables overflow checks or debug assertions, the tests that carry the evidence of that result SHOULD run at least once in that build (VV.8, HW.7). Other than that run, each run of the tests of each change SHOULD enable overflow checks and debug assertions (DSGN.2, VV.8).

### Concurrency

#### STND.RUST.22 Unsafe code across threads

Default. Instantiates DSGN.15.

Each unsafe implementation of `Send` or `Sync` SHOULD carry a safety argument that names the protection of STND.CONC.3 by which each transfer of a value of the type to another thread, or each access to it from another thread, is free of data races (DSGN.15). Where such an implementation is for a type with type parameters, it SHOULD require of each parameter the bounds that the transfer or the sharing of its values through the type needs (DSGN.15). A safety argument SHOULD NOT rest on a test of a shared mutable object that another concurrent task is able to change between the test and the unsafe operation (DSGN.15).

#### STND.RUST.23 Cancellation safety stated

Default. Instantiates DSGN.1, DSGN.14, REPRO.7.

The documentation of each asynchronous function and each future type that library code makes visible outside its crate SHOULD state whether its future is cancellation safe (DSGN.1). Across each suspension point, an asynchronous function SHOULD leave each object that code outside it is able to reach in a state that the invariants of that object admit, or restore such a state on the drop of its future at that point (DSGN.14). Where code is able to drop a future that is not cancellation safe before the future completes, it SHOULD state at that location why the data and the state that such a drop loses leave the results of the work correct (REPRO.7).

#### STND.RUST.24 Guards across suspension points

Default. Instantiates DSGN.3, DSGN.15.

The static checks of the work SHOULD report each guard of a lock that an asynchronous function holds across a suspension point (DSGN.3, DSGN.15). The static checks of the work SHOULD report each borrow of a cell whose borrows are checked at run time that an asynchronous function holds across a suspension point (DSGN.3).

### Foreign interfaces

#### STND.RUST.25 Types at foreign interfaces

Default. Instantiates DSGN.4, DSGN.3, DSGN.2.

Each type that crosses a foreign interface, by value or behind a pointer, SHOULD carry a representation attribute that fixes its layout to that of the corresponding type of the foreign side (DSGN.4). The size, the alignment, and the offset of each field of each such type SHOULD be compared with the declaration of the foreign side, by a check during compilation or by a test (DSGN.3, DSGN.4). Each pointer or function pointer that the foreign side is able to pass as null SHOULD be received as a raw pointer or an optional type, and checked before its conversion to a reference (DSGN.4, DSGN.2).

#### STND.RUST.26 Panics at foreign interfaces

Default. Instantiates DSGN.5.

Each function of the work that a foreign interface invokes SHOULD catch each panic within that function, or be declared with an ABI under which both sides of the interface admit unwinding (DSGN.5). Where the foreign interface carries errors, a panic so caught SHOULD be converted to an error that the interface carries (DSGN.5). Where the foreign interface carries no error, a panic so caught SHOULD be stored in an object that code of the work checks after the invocation returns, and answered there as STND.RUST.14 requires (DSGN.5).

#### STND.RUST.27 Foreign unwinding into Rust

Default. Instantiates DSGN.5.

Where a foreign function that the work calls is able to let an exception of its own language escape, the work SHOULD declare that function with an ABI under which the language admits unwinding (DSGN.5). Code SHOULD NOT catch an exception of another language by a facility for catching panics (DSGN.5). Code of the work SHOULD NOT call a foreign function that transfers control by a nonlocal jump across a Rust frame (DSGN.5).

#### STND.RUST.28 Ownership across foreign interfaces

Default. Instantiates DSGN.14.

Each resource that crosses a foreign interface SHOULD have one owner that the contract of the interface states, and be released by the side and the allocator that the contract names for it (DSGN.14). Each resource that a foreign interface creates for the work SHOULD pass to a type of the work that owns it and releases it in its `Drop` implementation, before each other operation that is able to fail (DSGN.14).

### Build-time code and packages

#### STND.RUST.29 Build-time code of the work

Default. Instantiates DSGN.16, REPRO.1.

Build-time code of the work SHOULD write only inside the output location that the build gives it (DSGN.16). Build-time code of the work SHOULD declare to the build each file and each environment variable that it reads (REPRO.1). Build-time code of the work SHOULD NOT reach the network (REPRO.1).

#### STND.RUST.30 Build-time code of dependencies

Default. Instantiates REPRO.9, SIMPL.4.

The dependency record SHOULD identify each dependency that runs build-time code (REPRO.9). Before a change that alters the lock file is relied upon, its review SHOULD examine the build-time code that the change adds or alters, that of each dependency that it adds included (SIMPL.4, REPRO.9).

#### STND.RUST.31 Additive features

Default. Instantiates DSGN.6, SIMPL.6, DSGN.2, VV.8.

Each feature of a crate of the work SHOULD only add items or implementations to the crate, and leave unchanged the behavior of each item that the crate provides without it (DSGN.6, SIMPL.6). A crate of the work SHOULD NOT have a feature that disables a check of the crate (DSGN.2). The checks of each change SHOULD build and test each crate of the work with no features, with its default features, and with all of its features (VV.8).

#### STND.RUST.32 Committed lock files

Default. Instantiates REPRO.1, REPRO.9.

The lock file of each set of crates that the work builds together SHOULD be under version control with the source that it resolves (REPRO.1, REPRO.9). Each build of the checks and of each release SHOULD use the revisions that the committed lock file records, and fail on a lock file that does not match the package metadata (REPRO.1).

### Checking

#### STND.RUST.33 Rust static checks

Default. Instantiates DSGN.3.

The static checks that the repository configuration names for Rust under STND.CODE.4 SHOULD include the warnings of the compiler at a recorded set, and a linter that reports each unsafe block without a safety argument and each unsafe function or unsafe trait whose documentation comment states no safety condition (DSGN.3). That linter SHOULD also check each provision of this standard whose compliance a rule of the linter decides (DSGN.3). Each compiler warning on the work's own source SHOULD fail the checks of the change that causes it (DSGN.3).

#### STND.RUST.34 Undefined behavior detected in tests

Default. Instantiates DSGN.3, SIMPL.11.

Where the means of the work include a detector of undefined behavior that runs a module of the work that holds an unsafe construct, the tests of each change to that module SHOULD run under that detector and fail at its first detection (DSGN.3, SIMPL.11). Where such a module calls foreign code that the detector does not run, its tests SHOULD also run in a build that detects invalid memory accesses at run time and fails the test at the first detection (DSGN.3).

#### STND.RUST.35 Stated limits of unsafe checks

Default. Instantiates VV.1, INTPR.10.

The record of each check of unsafe code by a detector of undefined behavior SHOULD state, as STND.CONC.27 asks of a dynamic check, the executions that the check observed, the code that it did not run, foreign code included, and the rules of aliasing that it applied (VV.1, INTPR.10).

#### STND.RUST.36 Claims of soundness

Binding. Instantiates PRIME.2.

Each claim that code of the work is free of undefined behavior, or that a module is a sound module, SHALL state each means by which that was checked and the code, the code of dependencies included, that each means covered (PRIME.2). A claim of soundness SHALL NOT extend beyond the code and the executions that those means covered (PRIME.2).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
