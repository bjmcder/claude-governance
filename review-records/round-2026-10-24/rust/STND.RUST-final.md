# Rust standard (STND.RUST) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 132 (2026-10-24). This reading copy is composed from the per-provision files in STND/RUST/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the coding practice that is specific to Rust. It adds to STND.CODE, STND.CONC, STND.DEPS, STND.BUILD, and STND.DOCS only what the language makes necessary. It covers the edition, the toolchain, and the build settings that change what code means (STND.RUST.1 and STND.RUST.2); unsafe code: the soundness argument at each unsafe construct and the soundness conditions that unsafe functions and traits state, sound modules, the list of modules that hold unsafe code, and the conditions on which no soundness argument rests (STND.RUST.3 to STND.RUST.7); panics: the panic strategy, panic safety, catching, destructors, and locks after a panic (STND.RUST.8 to STND.RUST.12); failures and their reporting (STND.RUST.13 to STND.RUST.17); integer arithmetic and conversions (STND.RUST.18, STND.RUST.19, and STND.RUST.20); manual implementations of `Send` and `Sync`, and asynchronous code (STND.RUST.21, STND.RUST.22, and STND.RUST.23); foreign function interfaces (STND.RUST.24 to STND.RUST.27); build scripts of dependencies, crate features, and lock files (STND.RUST.28, STND.RUST.29, and STND.RUST.30); and the checks of Rust code, unsafe code among it, with the claims that rest on them (STND.RUST.31 to STND.RUST.34).

STND.RUST.13, STND.RUST.14, and STND.RUST.15 instantiate PRIME.4, STND.RUST.34 instantiates PRIME.2, and STND.RUST.6 instantiates GOV.48 and binds agents alone; these five are binding at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is agnostic of toolchain release, platform, vendor, and tool: its provisions name constructs of the language and of its core and standard libraries, and no particular release, edition, compiler, linter, detector, package index, or build tool, which the repository configuration and the dependency record of each work choose (GOV.18). The rules of concurrency that hold for every model are in STND.CONC, the rules for dependencies in STND.DEPS, and the rules of building in STND.BUILD; this standard gives their Rust forms only where Rust sets a trap of its own.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them; Dependency record has the meaning that STND.DEPS gives it; Concurrent task, Asynchronous operation, Protection, Data race, Lock, and Suspension point have the meanings that STND.CONC gives them; Build script, Build configuration, Reporting build, Checking build, and Compilation unit have the meanings that STND.BUILD gives them. Each thread and each task that the work spawns is a concurrent task, each future is an asynchronous operation, and each await of a future is a suspension point. The build script that the build tool of the language compiles and runs before it builds a package, and a procedural macro, are build scripts. The panic strategy, the overflow checks, the debug assertions, and the crate features of a build are execution settings.

| Term | Definition |
| --- | --- |
| Crate | The unit that the Rust compiler compiles at one time: a library or a program, with the modules that its root file declares. |
| Library code | The Rust source of the crates of the work that other crates use, other than their tests, examples, benchmarks, and build scripts. |
| Public interface | Of a crate: each item that code outside the crate is able to name through a path of items that the crate declares public. |
| Untrusted input | Data that reaches the work from outside its own code, including the arguments of each function of the public interface of a crate of library code, other than data from a source that the threat model of the project records as trusted. |
| Undefined behavior | Behavior that the Rust Reference, at the release of the toolchain that builds the code, states to be undefined, and behavior that the specification of another language states to be undefined in code of that language that the work calls. |
| Unsafe operation | An operation that the language admits only within an unsafe block or within the body of an unsafe function. |
| Unsafe attribute | An attribute that the language requires, at the edition of its crate, to be written as unsafe, and an attribute that exports a symbol under a fixed name. |
| Unsafe construct | An unsafe block, an unsafe function, an unsafe trait, an unsafe implementation of a trait, a use of an unsafe attribute, and a block that declares foreign functions or foreign statics. |
| Soundness condition | Of an unsafe operation, an unsafe function, an unsafe trait, or an unsafe attribute: a condition that the language or the documentation of the item states, that its caller, its implementor, or the author of the attribute establishes, and without which the program has undefined behavior. |
| Soundness argument | A comment at an unsafe construct that states each soundness condition on which the construct relies and why that condition holds there. |
| Sound module | A module of the work, with its submodules, through whose visible items no code outside it, other than code that holds an unsafe construct of its own, is able to cause undefined behavior, whatever values it passes and in whatever order it calls them. |
| Panic | A response to a failure in Rust code, raised by that code or by an operation of the language, a slice index out of bounds or a division by zero among them, that carries a payload and unwinds the stack of its thread or ends the process, as the panic strategy of the build decides. |
| Panic strategy | Of a build: whether a panic unwinds the stack of its thread, running the destructors of the values that the stack holds, or ends the process at once. |
| Future | A value of a type that implements the `Future` trait of the core library. |
| Cancellation safe | Of a future: such that dropping it at each of its suspension points before it completes loses no data that it has taken from another object, and leaves each object that it reaches in a state that the invariants of that object admit. |
| Foreign function interface | An interface through which Rust code of the work calls, or is called by, code that does not follow the Rust rules of ownership, borrowing, and unwinding: a function that a block of foreign declarations declares, a function of the work exported with a foreign ABI, and a callback that the work passes to such code. |
| Crate feature | A named option of conditional compilation that a crate declares in its package metadata, and that the crate or the crates that depend on it enable. |
| Lock file | The file that records, for a set of crates that the work builds together, the exact revision of each package that their builds resolve and, where the source of a package gives one, its integrity digest. |

## Notes

Directions and sources. The custodian's standing directions keep this standard platform, compiler, vendor, implementation, framework, and tool agnostic, prefer timeless practice to current practice, and keep strict determinism an option where it is feasible, not a requirement unless the acceptance criterion or the consequence class demands it (STND.VVUQ.82, STND.VVUQ.83). Each provision therefore names a construct of the language or of its core and standard libraries and states an outcome that a reviewer or a check decides, and the Notes name a tool or a library only to explain a hazard. The sources are the research note research/rust-notes/rs1-rust-language.md (rs1 below), which rests on the Rust Reference, the Rustonomicon, the documentation of the standard library and of the build tool, and peer-reviewed studies, and the note research/round-addenda/a1-confirmations.md (a1 below), which confirms the facts on the panic hook and the panic handler from the documentation of the standard library and the Rust Reference.

What the corpus already holds. The standard adds Rust content to provisions that already hold the outcome, and does not restate them (GOV.31). STND.CODE.3 asks for the contract at each declaration, and the sections of a Rust documentation comment on safety, panics, and errors are its form (STND.RUST.3, STND.RUST.16). A documentation comment is work documentation, which STND.DOCS governs, and STND.DOCS.11 keeps it in step with the code that it describes. STND.CODE.7 forbids discarding a failure that PRIME.4 lists, which reaches a `Result` bound to the wildcard pattern, a conversion that drops its error, and a caught panic left unanswered. STND.DEPS.6 verifies each fetched component against its integrity digest, STND.DEPS.7 checks advisories before each release, and STND.DEPS.10 lets the package metadata and the lock file serve as the dependency record where they carry each package's reason and license identity. STND.BUILD holds the rules of building for every language, among them declared inputs (STND.BUILD.1), outputs only into the build tree (STND.BUILD.6), and fetching apart from building (STND.BUILD.7). Build scripts of the work and procedural macros are build scripts under those provisions, so this standard holds no rule on where they write, what they declare, or what they fetch.

Builds. A crate whose package metadata names no edition is compiled at the oldest one (rs1, section 9). A declared oldest release that no check confirms drifts from the code, so STND.RUST.1 tests at that release and at the release that builds results and releases, and runs a non-blocking check at the newest stable release and the newest revisions of the dependencies, as STND.PY.14 and STND.JL.3 do; STND.DEPS.8 still records the revision that built each result. STND.RUST.1 sets no rule for the newest edition, as STND.CXX.2 does for C++, because an edition of Rust is chosen for each crate and crates of different editions interoperate (rs1, section 9), so that the edition of one crate holds no other back. Editions have moved defaults that concern unsafe code (rs1, section 9), so a change of edition is a change of the computational environment under HW.7 and of a pinned revision under STND.DEPS.5. The settings of STND.RUST.2 are the Rust part of what STND.BUILD.11 states: the panic strategy decides whether destructors run after a panic and whether a panic is able to be caught; overflow checks decide whether an integer operation panics or wraps; debug assertions decide whether `debug_assert!` runs; an enabled target feature lets the compiler emit instructions that a processor without it does not execute, which is undefined behavior; and crate features select the code that a crate compiles (rs1, sections 3, 6, 10, and 11).

Unsafe code. An unsafe block states that the obligations of the operations inside it are met; the keyword moves the duty to avoid undefined behavior from the compiler to the author (rs1, section 1). The language's own forms are the "Safety" section of a documentation comment and a comment that opens with "SAFETY:"; the Terms call them soundness conditions and soundness arguments because safety in this corpus names freedom from harm, as in PRIME.13 and the term Safety-related component, and a soundness argument is no part of a hazard analysis. A value with an invalid bit pattern, a null or dangling reference, or a second live mutable reference to the same bytes is undefined behavior even without an access, and each operation whose name marks it unchecked is undefined behavior where the condition that it assumes fails (rs1, sections 1 and 2). For those operations STND.RUST.3 corresponds to STND.CXX.24, with one difference: STND.CXX.24 asks for a check or a recorded proof and rests on DSGN.2, while STND.RUST.3 asks for an argument and rests on DSGN.1, because most soundness conditions, aliasing and validity among them, are not checkable at run time. The Reference states that the list of undefined behavior is able to grow or shrink and that the rules of aliasing are not settled; an argument that holds under the stricter reading of the two experimental models that rs1 reports holds under both (rs1, sections 1, 11, and 12).

Soundness is a property of the interface of a module. The Reference calls unsafe code sound where no safe code that uses it is able to reach undefined behavior through it, and a module whose interface admits undefined behavior is unsound even where no present caller reaches it (rs1, section 1). Privacy keeps code outside a module and its submodules from changing its private fields, so an argument that rests on an invariant of those fields rests on all of that code (STND.RUST.4). In a study of 186 reports of memory-safety vulnerabilities in Rust through 2020, each required unsafe code, and many were soundness defects that no present caller triggered (rs1, section 12, S42). An unsafe construct outside the modules that STND.RUST.5 lists is admitted by an entry in the list and not by a suppression at its location. One study found unsafe code in the call chain of more than three quarters of the libraries it examined (rs1, section 12, S56), hence the dependencies in STND.RUST.34.

STND.RUST.7 states what the language does not promise. Safe code is able to leak or forget a value, so its destructor does not run (rs1, section 1, S5); the destructor of a guard that the module keeps to itself runs during unwinding, which is why STND.RUST.9 admits a guard. Poisoning is advisory: unsafe code does not rely on it, a panic during the unwinding of another leaves a lock unpoisoned, and a read-write lock is poisoned only by a panic of a writer (rs1, section 3). One static analyzer found 264 previously unknown memory-safety defects in the public register of Rust packages in three patterns: panic safety, higher-order invariants, and missing bounds on `Send` and `Sync` (rs1, section 12, S46).

Agents and unsafe code. STND.RUST.6 binds every agent at every class by its own force (GOV.48), and STND.INSTR.10 carries it into the agent instructions. Unsafe code without an argument compiles and passes its tests, and its defect stays latent until another caller, an optimizer, or a stricter model of aliasing reaches it, so an absent argument leaves a reviewer nothing to check the code against.

Panics. A build either unwinds on a panic or aborts, the default depends on the target, and under the aborting strategy a catch of a panic does nothing and no destructor runs after it (rs1, section 3), which STND.RUST.8 has a crate that relies on unwinding state. A safe state that the destructor of a handle sets is therefore not reached on such a halt, and CPS.4 and HW.EMBED.4 are not met by that design. Unsafe code that duplicates a value and then calls a caller-supplied clone, which is free to panic, reads uninitialized memory or frees a value twice after such a panic (rs1, section 3, S8), which STND.RUST.9 answers. Catching a panic is not a general mechanism for handling errors and might not catch every panic (rs1, section 3, S12), hence STND.RUST.10. A destructor that panics during unwinding is likely to end the process (S13), and a destructor has no way to return a failure, so STND.RUST.11 asks for a release operation that returns it, as STND.CXX.21 does for C++. A lock that does not poison leaves the next holder no sign of a broken state, so STND.RUST.12 lets the protected object carry its own mark.

Failures. STND.RUST.13 lists the responses that PRIME.4 admits in Rust, and the other provisions refer to it. A panic is the Rust form of raising an exception: under the unwinding strategy it ends its thread unless it is caught, and a spawned thread that panics returns the payload to the handle that joins it, while a dropped handle detaches the thread, which STND.CONC.1 and STND.CONC.2 govern (rs1, section 3, S44). A program with the standard library is able to replace its panic hook, which runs when a thread panics and before the panic runtime, and so under both panic strategies; the default hook prints a message to standard error (a1, fact 1). A binary or a linked library built without the standard library requires a panic handler, one function in its dependency graph that defines the behavior of a panic and never returns (a1, fact 2). The second sentence of STND.RUST.13 keeps a replaced hook from removing the diagnosis that PRIME.4 asks of a panic that ends in a halt, and has a handler deliver that diagnosis, since the language supplies no handler to such a build; a panic that is caught and answered by a returned error or a visible degradation carries its diagnosis through that response. The third sentence follows STND.PY.22: a record written through a logging interface reaches no person unless the program installs something that shows it; STND.JL.15 instead admits a record at the levels that the default logger of Julia shows. The three sentences of STND.RUST.13 together define what counts as a response, as those of STND.PY.22 do. STND.RUST.14 is the Rust form of STND.CXX.17, with its two means. STND.RUST.15 is the Rust form of STND.CODE.6, and of STND.CXX.18 for the checks of CPS.5 and CPS.9: `debug_assert!` does not run where debug assertions are off, code compiled only under the debug-assertion flag or a crate feature is absent from a build without it, and overflow checks are on by default only where debug assertions are on, a build without them being free to panic or to wrap silently (rs1, section 6). The term Untrusted input reaches the arguments of each function of the public interface of a crate of library code, as the terms of STND.PY and STND.JL reach the arguments of their public interfaces. The Notes of STND.JL record the custodian's ruling of 2026-10-23 that the reach of its term to the arguments of each declared public function raises no floor, and the Notes of STND.PY record the ruling of that date that a shape check of an argument reaches every function of the public interface at every class. Both rulings were made for those standards and not for this one; the reach of the term here rests on the argument for STND.RUST.15 in the paragraph on the floor. STND.RUST.16 and STND.RUST.17 follow the book of the Rust project and the API guidelines: a failure that a caller causes by its data and is able to handle is returned as a `Result`, a panic answers a broken precondition or invariant that the "Panics" section states, and `unwrap` and `expect` stand where the code shows the failure impossible, a message of `expect` that states the reason meeting STND.RUST.17 (rs1, section 7).

Arithmetic. Integer operators panic on overflow under overflow checks, and otherwise panic or wrap at the discretion of the implementation; methods whose names state checked, wrapping, saturating, and overflowing behavior, and a wrapping integer type, make the intended behavior visible (rs1, section 6). Untrusted input that overflows passes the checks of DSGN.2 undetected in a build without overflow checks, as STND.JL.17 states for Julia, and hashing and generators of random numbers rely on wraparound on purpose (STND.RUST.18). An overflow in trusted arithmetic that computes a command for hardware is a defect under PRIME.4 and DSGN.2, and the check of CPS.5 does not detect a wrapped value that falls inside the command limit. A conversion by `as` truncates an integer, and saturates a floating-point value, a NaN becoming zero, without a report (rs1, sections 2 and 6), which on invalid input is the silent clamping that PRIME.4 forbids (STND.RUST.19); a conversion that changes floating-point precision is recorded under NUMER.5. STND.RUST.20 follows STND.JL.34 and not STND.CXX.27: safe Rust checks each index in every build (rs1, section 2), so the unchecked library preconditions that STND.CXX.27 turns on in the shipped build have no Rust counterpart, and the checks that a Rust setting removes are governed by STND.RUST.15 and STND.RUST.18 where they would pass untrusted input. Its tests run in checking builds under STND.BUILD.13.

Concurrency. Safe Rust excludes data races, and not race conditions, deadlock, or leaks (rs1, sections 2 and 4), which STND.CONC governs; an object behind a lock type of the standard library carries its protection in its type, which meets STND.CONC.3. Send and Sync are unsafe traits that the compiler derives from the fields of a type and that other unsafe code assumes correct, so a wrong manual implementation is undefined behavior (rs1, section 4, S14 and S15). A race condition combined with unsafe code is able to break memory safety, as when unsafe code takes a bound from a value that another thread changes after the check (rs1, section 4, S16), which is why STND.RUST.21 names the protection of STND.CONC.3. Dropping a future cancels it at its current suspension point, and the language has no marker of cancellation safety (rs1, section 5, S49); STND.CONC.13 governs the propagation of the cancellation and the release of resources, and STND.RUST.22 adds the statement and the state at each suspension point that the drop makes necessary, in three sentences on one future. STND.RUST.23 makes STND.CONC.8 mechanical where the means of the work include such a check, since lints for a guard and for a borrow of a cell held across an await exist in one linter (rs1, section 5), and a work without one is not blocked; where no check reports the guard of a lock that an asynchronous library designs to be held across an await, a project replaces its first sentence by a decision. STND.CONC.15, STND.CONC.16, and STND.CONC.17 govern blocking on an executor, state local to a thread, and executors as pools (rs1, section 5).

Foreign function interfaces. The term Foreign function interface is the Rust counterpart of the term Foreign interface of STND.CXX. A structure has the layout of the corresponding C type only under the representation attribute that fixes it (rs1, section 8, S28), and the attribute fixes the rules and not the agreement with a header, so STND.RUST.24 compares the two; its three sentences are the schema of one type at one boundary (DSGN.4). References, owning boxes, and function pointers are never null in Rust, and an empty enumeration used as an opaque foreign type leads the compiler to assume that no value exists (rs1, section 8). An unwinding that reaches a function declared with a non-unwinding ABI ends the process, one that enters Rust frames from such a declaration is undefined behavior, and the Rustonomicon calls the catch of an exception of another language undefined where the Reference calls it unspecified (rs1, section 3); STND.RUST.26 avoids both readings. STND.RUST.25 is the Rust form of STND.CXX.22, and STND.RUST.27 follows STND.CXX.20; a callback that foreign code calls after the Rust data that it reaches is released falls under STND.CONC.5. The term Undefined behavior includes foreign code because its undefined behavior is that of the whole program (rs1, section 8).

Packages. The build tool compiles and runs the build script of each package before it builds the package, and a procedural macro has the resources of the compiler (rs1, section 10, S33 and S34); each runs for each dependency that has one, with the authority of the account that builds. STND.BUILD.21 reviews the build scripts of the work as code, and STND.RUST.28 adds the record and the review for those of dependencies, the evidence on exposure to compromise that STND.DEPS.1 weighs. GUARD.17 governs the security of builds against the supply-chain row that STND.THRT.2 adds to every threat model. The build tool enables the union of the crate features that the crates of a build request of a dependency, so a feature that another crate enables changes the code of this one (rs1, section 10, S32). A project replaces STND.RUST.29 by a decision for crate features that select an alternative path under HW.15 to HW.19, or that exclude each other. The lock file records the exact revision of each package (rs1, section 10, S31), and STND.RUST.30 is the Rust form of STND.JL.4, with its exception for a crate that other work uses and whose builds produce no reported result; STND.DEPS.6 has the first fetch record a digest where the publisher gives none. The check of STND.RUST.1 against newer revisions is the one build of the checks that leaves the lock file, and the three sentences of STND.RUST.30 are one rule for one file.

Checking. STND.RUST.31 is the Rust form of STND.CXX.25 and STND.PY.2, and the warnings of the compiler fail the checks under STND.BUILD.12. An interpreter that runs a program on an abstract machine detects accesses out of bounds and after release, data races, violations of the aliasing rules, and leaks; its documentation states that it does not catch every violation, does not show that code is sound, tests one of many possible executions, and does not run most interfaces of the platform or foreign code (rs1, section 11, S35). STND.RUST.32 asks for the run where the means of the work include such a detector, so that a target that it does not support blocks no work, STND.RUST.33 states its limits as STND.CONC.27 does, and STND.CODE.9 covers the seed of a detector that makes seeded choices. STND.RUST.34 reaches the claims in a report, in the record of a result or of a release, and in a review; a soundness argument at an unsafe construct is not such a claim.

Numerics. NaN bit patterns that are not portable and library functions of unspecified precision (rs1, section 11, S37) are inputs to NUMER.5, NUMER.16, NUMER.17, HW.5, and STND.VVUQ.3, so this standard holds no provision on floating point.

Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or a provision of HW, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row, and the part that rests on HW.5 or HW.7 applies only to work that HW binds. STND.RUST.24 rests on DSGN.4 alone (a schema for each data structure crossing an interface), and STND.RUST.25 and STND.RUST.26 on DSGN.5 alone (a contract for each external component), and they apply from CSQ2. STND.RUST.33 instantiates INTPR.10 (documentation of the limits of validity) and applies from CSQ2, as STND.CONC.27 does. The second sentence of STND.RUST.10 rests on INTPR.8 (diagnostics captured by default) and applies from CSQ1; its first sentence applies from CSQ3. STND.RUST.2 and the first sentence of STND.RUST.20 rest on HW.5 or HW.7 and apply from CSQ3 to work that HW binds. STND.RUST.12 and STND.RUST.21 state what a protocol of DSGN.15 uses, and the first sentence of STND.RUST.23 checks that use mechanically; none verifies the invariants of a protocol, which the table starts at CSQ2, and they apply from CSQ3, as STND.CONC.3 to STND.CONC.9 do. The first sentence of STND.RUST.18 rests on the checking of preconditions where untrusted data enters, and the second sentence of STND.RUST.20 and the first sentence of STND.RUST.29 on the retention of checks for verification, which DSGN.2 asks in full from CSQ3, and not on the checking of postconditions that the table starts at CSQ1. The second sentence of STND.RUST.5, both sentences of STND.RUST.23, STND.RUST.31, and STND.RUST.32 ask for mechanical checks (DSGN.3) from CSQ3, and the checking of each contract of a safety-related component that the table starts at CSQ0 stays with that row. The tests of STND.RUST.1, STND.RUST.8, and STND.RUST.29 compare with no reference oracle produced without the implementation, so they rest on no row and apply from CSQ3. STND.RUST.3, STND.RUST.4, STND.RUST.7, STND.RUST.9, STND.RUST.11, STND.RUST.16, STND.RUST.17, STND.RUST.19, STND.RUST.22, STND.RUST.27, STND.RUST.28, STND.RUST.30, and the first sentence of STND.RUST.5 rest on no row and apply from CSQ3. STND.RUST.1, STND.RUST.7, STND.RUST.11, STND.RUST.22, STND.RUST.24, STND.RUST.25, and STND.RUST.30 each hold three modals on one subject: the releases of one crate, what one argument rests on, one destructor and its release, one future, one type at one boundary, one function that a foreign interface invokes, and one file; a project that replaces one of these defaults by a decision replaces the provision whole. STND.RUST.13 holds three modals on the responses to one failure and applies as one; it is binding, so no decision replaces it, and a project instrument only tightens it (GOV.19).

Floor. STND.RUST.13 asks for the responses that PRIME.4 already requires: its second sentence reaches only a panic that answers a listed condition and that no other response answers, and asks only for the actionable diagnosis that PRIME.4 names; its third keeps a record that no person sees from counting as visible, as STND.PY.22 does. STND.RUST.14 costs one attribute, one return type, or one check for each function that returns a listed failure, as STND.CXX.17 does; without it a listed failure is able to pass silently. It applies where the means of the work include a compiler or a static check that diagnoses an ignored returned value, so that it asks nothing that the means of the work are unable to give, and where they include none, STND.CODE.7 still forbids discarding a listed failure. STND.RUST.15 forbids the forms that leave a check of untrusted input removable by an execution setting, which STND.CODE.6 already forbids, and the same forms for a check that CPS.5 or CPS.9 already requires, as STND.CXX.18 does. The term Untrusted input reaches the arguments of each function of the public interface of a crate of library code because code that the crate does not see calls those functions, and the threat model has not recorded that code as trusted; the reach adds no check beyond those that STND.CODE.6 keeps, only the forms that remove them. STND.RUST.34 asks of a claim of soundness in a report, a record, or a review that it state the means that checked it and not extend beyond what they covered; PRIME.2 already forbids misrepresenting the status of evidence, and the cost is one sentence for each such claim. STND.RUST.6 costs an agent one comment at each construct that it writes or changes, the form of the code that it writes and not a tool or added work, the argument on which STND.PY.4 binds agents under GOV.48. No ruling covers STND.RUST.6, since the custodian's ruling of 2026-10-23 that STND.PY.4 raises no floor was made for STND.PY. Each binds at every class, CSQ4 included. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no default raises the floor (GOV.11).

Existing Rust source conforms to the default provisions when a change next touches it.

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| HW.EMBED | Embedded controllers |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.BUILD | Build standard |
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

The package metadata of each crate of the work SHOULD state its edition and the oldest release of the Rust toolchain that it supports (SIMPL.6, REPRO.9). The checks of each change SHOULD build and test each crate of the work with that oldest release, and with the release of the toolchain that builds the reported results and the releases of the work (VV.8). At the interval that the repository configuration sets, a check that reports its failure without blocking a change SHOULD build and test the work with the newest stable release of the toolchain and with the newest revisions of its dependencies that their declared ranges admit (VV.8).

#### STND.RUST.2 Rust build settings stated

Default. Instantiates SIMPL.6, REPRO.2, HW.5.

Among the execution settings that STND.BUILD.11 asks the repository configuration to state for each compilation unit, the repository configuration SHOULD state, for each reporting build, its panic strategy, whether its overflow checks and its debug assertions are enabled, its target instruction set with each target feature that it enables, and the crate features that it enables for each crate of the work (SIMPL.6, REPRO.2, HW.5).

### Unsafe code

#### STND.RUST.3 Soundness arguments and conditions

Default. Instantiates DSGN.1, SIMPL.11, REPRO.7.

Each unsafe block, each unsafe implementation of a trait, and each use of an unsafe attribute SHOULD carry a soundness argument at its location, each unsafe operation in the body of an unsafe function standing in such a block (DSGN.1, SIMPL.11, REPRO.7). In addition to what STND.CODE.3 asks, the documentation comment of each unsafe function and each unsafe trait of the work SHOULD state each soundness condition that its callers or its implementors establish (DSGN.1).

#### STND.RUST.4 Sound modules

Default. Instantiates DSGN.1, SIMPL.11.

Each module of the work that holds an unsafe construct SHOULD be a sound module (DSGN.1, SIMPL.11). Each soundness argument SHOULD rest only on conditions that the module of its unsafe construct establishes for every use of its visible items, and not on the uses that code outside the module makes of them at present (DSGN.1).

#### STND.RUST.5 Listed unsafe modules

Default. Instantiates SIMPL.11, DSGN.3.

The repository configuration SHOULD list each module of the work that holds an unsafe construct (SIMPL.11). Where the means of the work include a static check that locates unsafe constructs, that check SHOULD reject each unsafe construct of the work outside the listed modules (DSGN.3).

#### STND.RUST.6 Agent soundness arguments

Binding. Instantiates GOV.48, DSGN.1.

An agent SHALL write the soundness argument that STND.RUST.3 asks at each unsafe block, unsafe implementation of a trait, and use of an unsafe attribute that it writes or changes, or the form that an alternative adopted by a project instrument in place of STND.RUST.3 requires (GOV.48, DSGN.1). An agent SHALL state the soundness conditions that STND.RUST.3 asks in the documentation comment of each unsafe function and unsafe trait that it writes or changes, or the form that an alternative adopted by a project instrument in place of STND.RUST.3 requires (GOV.48, DSGN.1).

#### STND.RUST.7 Soundness without destructors or poisoning

Default. Instantiates DSGN.1.

A soundness argument SHOULD NOT rest on the running of the destructor of a value that code outside its module is able to reach (DSGN.1). A soundness argument SHOULD NOT rest on the poisoning of a lock (DSGN.1). A soundness argument SHOULD NOT rest on the absence of a panic in code that the module of its unsafe construct does not define (DSGN.1).

### Panics

#### STND.RUST.8 Panic strategy relied upon

Default. Instantiates DSGN.1, VV.1.

Where a crate of the work relies on unwinding, to catch a panic or to run a destructor after one, its documentation SHOULD state that it requires the unwinding panic strategy (DSGN.1). The tests of each change SHOULD run under each panic strategy with which the work builds a release or a reported result (VV.1).

#### STND.RUST.9 Panic safety of unsafe code

Default. Instantiates DSGN.1, DSGN.14.

Where unsafe code leaves an object in a state that the validity rules of its type or the invariants of its module do not admit, it SHOULD call code that its module does not define only after it restores an admitted state, or under a guard that restores such a state on each path by which a panic leaves that call (DSGN.1, DSGN.14).

#### STND.RUST.10 Panics caught at boundaries

Default. Instantiates SIMPL.6, INTPR.8.

Other than in a test, code SHOULD catch a panic only at the root of a thread or a task, at a foreign function interface, or at the boundary of a component that its design isolates from the rest of the process (SIMPL.6). The response to each panic so caught SHOULD carry a diagnosis that holds the message of the panic (INTPR.8).

#### STND.RUST.11 Destructors without panics

Default. Instantiates DSGN.1.

Each `Drop` implementation of the work SHOULD return without a panic that its own code raises (DSGN.1). Where the release of a resource is able to report a failure that affects a result, the type that owns the resource SHOULD provide an operation that releases it and returns that failure, for its owner to call before the result is relied upon (DSGN.1). Where a `Drop` implementation detects a failed release, it SHOULD respond by a response of STND.RUST.13 other than a panic, or as STND.CODE.12 provides (DSGN.1).

#### STND.RUST.12 Locks after a panic

Default. Instantiates DSGN.15.

Where a panic is able to leave the object that a lock protects in a state that its invariants do not admit, the code that next acquires the lock SHOULD detect that state, by the poisoning of the lock or by a mark that the object carries, and re-establish those invariants or pass the failure to its caller before it uses the object (DSGN.15).

### Failures

#### STND.RUST.13 Rust responses to listed failures

Binding. Instantiates PRIME.4.

Where code detects a condition that PRIME.4 lists, it SHALL panic, return the condition in its result, halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, or degrade visibly with a diagnosis (PRIME.4). Where the work replaces the hook, or defines the handler, that runs at a panic, that hook or handler SHALL deliver to the operator, or to the record of the run, a diagnosis of each panic that answers a condition that PRIME.4 lists and that no other response of this provision answers (PRIME.4). A record that library code writes through a logging interface SHALL NOT be the only visible degradation (PRIME.4).

#### STND.RUST.14 Unignorable failure results

Binding. Instantiates PRIME.4.

Where the means of the work include a compiler or a static check that diagnoses a call that ignores a returned value, each function of the work that returns a failure of a kind that PRIME.4 lists SHALL be declared so that such a compiler or static check diagnoses each call that ignores the returned value (PRIME.4).

#### STND.RUST.15 Untrusted input and execution settings

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9.

A check of untrusted input, or a check that CPS.5 or CPS.9 requires, SHALL NOT be written in a form that an execution setting removes: `debug_assert!` and its variants, and code compiled only under a condition that such a setting decides (PRIME.4, DSGN.2, CPS.5, CPS.9). Where code rejects untrusted input, or detects a condition that CPS.5 or CPS.9 requires it to check, on an integer overflow, it SHALL detect that overflow by an operation that reports overflow in every build or by a check of range before the operation (PRIME.4, DSGN.2, CPS.5, CPS.9).

#### STND.RUST.16 Failures in library code

Default. Instantiates DSGN.1.

Where a caller of library code is able to cause a failure by the data that it passes and to handle that failure, the library code SHOULD report the failure by a returned `Result` (DSGN.1). In addition to what STND.CODE.3 asks, the documentation comment of each function of the public interface of a crate of library code SHOULD state each condition under which the function panics and each error that it returns (DSGN.1).

#### STND.RUST.17 Reasoned unwrap in library code

Default. Instantiates DSGN.1, REPRO.7.

In library code, each call of `unwrap`, of `expect`, or of another method that panics on a receiver that holds no value or holds an error SHOULD carry at its location the reason that its receiver holds a value there (DSGN.1, REPRO.7).

### Integer arithmetic

#### STND.RUST.18 Explicit integer arithmetic

Default. Instantiates DSGN.2, SIMPL.6.

Where an integer operation on untrusted input is able to exceed the range of its type, code SHOULD detect that by an operation that reports overflow in every build, or by a check of range before the operation (DSGN.2). Where code relies on the wraparound of an integer operation, it SHOULD use an operation or a type whose name states that it wraps (SIMPL.6).

#### STND.RUST.19 Narrowing conversions stated

Default. Instantiates DSGN.1, SIMPL.6.

Each conversion by `as` that narrows an integer, changes its signedness, or converts a floating-point value to an integer SHOULD carry at its location the reason that the value lies in the range of the target type, or be replaced by a conversion that reports a value outside that range (DSGN.1, SIMPL.6).

#### STND.RUST.20 Checked builds under test

Default. Instantiates VV.8, HW.7, DSGN.2.

Where a reporting build of a numerical result disables overflow checks or debug assertions, the tests that carry the evidence of that result SHOULD run at least once in that build (VV.8, HW.7). Other than that run, each run of the tests of each change SHOULD enable overflow checks and debug assertions (DSGN.2, VV.8).

### Concurrency

#### STND.RUST.21 Manual Send and Sync

Default. Instantiates DSGN.15.

Each unsafe implementation of `Send` or `Sync` SHOULD carry a soundness argument that names the protection of STND.CONC.3 by which each transfer of a value of the type to another thread, or each access to it from another thread, is free of data races (DSGN.15). Where such an implementation is for a type with type parameters, it SHOULD require of each parameter the bounds that the transfer or the sharing of its values through the type needs (DSGN.15).

#### STND.RUST.22 Cancellation safety stated

Default. Instantiates DSGN.1, DSGN.14, REPRO.7.

The documentation of each asynchronous function and each future type of the public interface of a crate of library code SHOULD state whether its future is cancellation safe (DSGN.1). Across each suspension point, an asynchronous function SHOULD leave each object that code outside it is able to reach in a state that the invariants of that object admit, or restore such a state on the drop of its future at that point (DSGN.14). Where code is able to drop a future that is not cancellation safe before the future completes, it SHOULD state at that location why the data and the state that such a drop loses leave the results of the work correct (REPRO.7).

#### STND.RUST.23 Guards across suspension points

Default. Instantiates DSGN.3, DSGN.15.

Where the means of the work include a static check of guards held across suspension points, the static checks of the work SHOULD report each guard of a lock that an asynchronous function holds across a suspension point (DSGN.3, DSGN.15). Where the means of the work include a static check of borrows held across suspension points, the static checks of the work SHOULD report each borrow of a cell whose borrows are checked at run time that an asynchronous function holds across a suspension point (DSGN.3).

### Foreign function interfaces

#### STND.RUST.24 Types at foreign interfaces

Default. Instantiates DSGN.4.

Each structure, union, and enumeration that crosses a foreign function interface, by value or behind a pointer, and that the work does not treat as opaque, SHOULD carry a representation attribute that fixes its layout to that of the corresponding type of the foreign side (DSGN.4). The size, the alignment, and the offset of each field of each such type SHOULD be compared with the declaration of the foreign side, by a check during compilation or by a test (DSGN.4). Each pointer or function pointer that the foreign side is able to pass as null SHOULD be received as a raw pointer or an optional type, and checked before its conversion to a reference (DSGN.4).

#### STND.RUST.25 Panics at foreign interfaces

Default. Instantiates DSGN.5.

Each function of the work that a foreign function interface invokes SHOULD catch each panic within that function, or be declared with an ABI under which both sides of the interface admit unwinding (DSGN.5). Where the foreign function interface carries errors, a panic so caught SHOULD be converted to an error that the interface carries (DSGN.5). Where the foreign function interface carries no error, a panic so caught SHOULD be stored in an object that code of the work checks after the invocation returns, and answered there as STND.RUST.13 requires (DSGN.5).

#### STND.RUST.26 Foreign unwinding into Rust

Default. Instantiates DSGN.5.

Where a foreign function that the work calls is able to let an exception of its own language escape, the work SHOULD declare that function with an ABI under which the language admits unwinding, and leave each such exception uncaught by the facilities for catching panics (DSGN.5). Code of the work SHOULD NOT call a foreign function that transfers control by a nonlocal jump across a Rust frame (DSGN.5).

#### STND.RUST.27 Ownership across foreign interfaces

Default. Instantiates DSGN.14.

Each resource that crosses a foreign function interface SHOULD have one owner that the contract of the interface states, and be released by the side and the allocator that the contract names for it (DSGN.14). Each resource that a foreign function interface creates for the work SHOULD pass to a type of the work that owns it and releases it in its `Drop` implementation, before each other operation that is able to fail (DSGN.14).

### Packages

#### STND.RUST.28 Build scripts of dependencies

Default. Instantiates REPRO.9, SIMPL.4.

The dependency record SHOULD identify each dependency that has a build script (REPRO.9). Before a change that alters the lock file is relied upon, its review SHOULD examine each build script that the change adds or alters, those of each dependency that it adds included (SIMPL.4, REPRO.9).

#### STND.RUST.29 Additive crate features

Default. Instantiates DSGN.6, SIMPL.6, DSGN.2, VV.8.

Each crate feature of a crate of the work SHOULD only add items or implementations to the crate, leave unchanged the behavior of each item that the crate provides without it, and disable no check of the crate (DSGN.6, SIMPL.6, DSGN.2). Among the build configurations that STND.BUILD.26 asks the repository configuration to state, the checks of each change SHOULD build and test each crate of the work with no crate features, with its default crate features, and with all of its crate features (VV.8).

#### STND.RUST.30 Committed lock files

Default. Instantiates REPRO.1, REPRO.9.

The lock file of each set of crates that the work builds together SHOULD be under version control with the source that it resolves (REPRO.1, REPRO.9). A crate that other work uses, and whose own builds produce no reported result, MAY keep its lock file out of version control (REPRO.9). Other than the check against newer revisions of STND.RUST.1, each build of the checks and of each release SHOULD use the revisions that the lock file under version control records, and fail on a lock file that does not match the package metadata (REPRO.1).

### Checking

#### STND.RUST.31 Rust static checks

Default. Instantiates DSGN.3.

Where the means of the work include a check that reports each unsafe block without a soundness argument, and each unsafe function or unsafe trait whose documentation comment states no soundness condition, the static checks that the repository configuration names for Rust under STND.CODE.4 SHOULD include that check (DSGN.3). Those static checks SHOULD also decide each provision of this standard whose compliance a static check of Rust source is able to decide (DSGN.3).

#### STND.RUST.32 Undefined behavior detected in tests

Default. Instantiates DSGN.3, SIMPL.11.

Where the means of the work include a detector of undefined behavior that runs a module of the work that holds an unsafe construct, the tests of each change to that module SHOULD run under that detector and fail at its first detection (DSGN.3, SIMPL.11). Where such a module calls foreign code that the detector does not run, its tests SHOULD also run in a build that detects invalid memory accesses at run time and fails the test at the first detection (DSGN.3).

#### STND.RUST.33 Stated limits of unsafe checks

Default. Instantiates VV.1, INTPR.10.

The record of each check of unsafe code by a detector of undefined behavior SHOULD state, as STND.CONC.27 asks of a dynamic check, the executions that the check observed, the code that it did not run, foreign code included, and the rules of aliasing that it applied (VV.1, INTPR.10).

#### STND.RUST.34 Claims of soundness

Binding. Instantiates PRIME.2.

Each claim, in a report, in the record of a result or of a release, or in a review, that code of the work is free of undefined behavior or that a module is a sound module SHALL state each means by which that was checked and the code, the code of dependencies included, that each means covered (PRIME.2). Such a claim SHALL NOT extend beyond the code and the executions that those means covered (PRIME.2).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
