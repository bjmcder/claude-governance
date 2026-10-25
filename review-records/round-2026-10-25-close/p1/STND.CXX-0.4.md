# C++ standard (STND.CXX) 1.2

Adopted by The Custodian as revision 1.0 in ledger entry 103 (2026-10-23); revised to 1.1 in entry 118 (2026-10-24), 1.1.1 in entry 128 (2026-10-24), and 1.2 in entry 150 (2026-10-25). This reading copy is composed from the per-provision files in STND/CXX/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.CXX.16, STND.CXX.17, STND.CXX.28, STND.CXX.29, STND.CXX.30, and STND.CXX.31.

## Purpose and scope

This standard holds the coding practice that is specific to C++. It adds to STND.CODE and STND.DOCS only what the language makes necessary. It takes the C++ Core Guidelines as the reference for the work's practice and sets the language edition and the build settings that change what code means (STND.CXX.1, STND.CXX.2, STND.CXX.3, and STND.CXX.4). It states who owns memory and other owned resources and how sequences and hardware memory are passed (STND.CXX.5, STND.CXX.6, and STND.CXX.7). It puts the standard library and header-only code first and keeps results that depend on the library implementation reproducible (STND.CXX.8, STND.CXX.9, and STND.CXX.10), and recommends generic code and metaprogramming that a reader is able to follow (STND.CXX.11, STND.CXX.12, and STND.CXX.13). It fixes names and declaration comments (STND.CXX.14 and STND.CXX.15). It covers failures, including the option that assumes finite values, the boundaries to code that does not follow C++ rules, and the terminate handler (STND.CXX.18, STND.CXX.19, STND.CXX.20, STND.CXX.21, STND.CXX.22, STND.CXX.23, STND.CXX.24, STND.CXX.32, and STND.CXX.33), and the mechanical checks of C++ code (STND.CXX.25, STND.CXX.26, and STND.CXX.27). STND.CODE holds for C++, as for every language, the responses to a failure that PRIME.4 lists, the declarations that keep a returned failure from being ignored, and the checks that no setting or definition removes, and, for the code that a release of work of CSQ1 or CSQ0 delivers or runs to produce a reported result, conformance to the high-assurance coding standard that the work adopts, honest claims of that conformance, an edition that the standard covers and the toolchain is validated for, and recorded deviations (STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.17, STND.CODE.18, STND.CODE.19, STND.CODE.20, and STND.CODE.21); the Notes give their C++ forms.

STND.CXX.18 and STND.CXX.32 instantiate PRIME.4, and STND.CXX.3 instantiates GOV.48 and binds agents alone; these three are binding at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is platform and compiler agnostic: it names no version, compiler, platform, library to depend on, or tool, and the repository configuration or a project instrument chooses them (GOV.18). It holds no rules for message passing, directive-based threading, or device offload, only the C++ rules at their boundaries. The rules of concurrency that hold for every language are in STND.CONC, which this standard cites and does not restate.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and High-assurance coding standard have the meanings that STND.CODE gives them; Safety-related component has the meaning that STND.CLASS gives it.

| Term | Definition |
| --- | --- |
| Translation unit | A source file together with the headers it includes, as a compiler translates it. |
| Toolchain matrix | Of a translation unit: the compilers and the standard library implementations, each at its pinned revision, that the repository configuration names as building that unit. |
| Edition in force | Of a translation unit: the edition of the ISO C++ standard at which the repository configuration states that the unit is compiled. |
| Owned resource | Memory, a file, a lock, a handle that a foreign interface issues, or another facility that code acquires and has to release. |
| Resource handle | An object whose type owns one owned resource, releases it in its destructor, and defines or deletes its copy and move operations. |
| Foreign interface | An interface through which C++ code of the work calls, or is called by, code that does not follow the C++ rules of ownership and exceptions: a C or vendor library interface, a callback or thread that such a library or a runtime starts, and a structured block of a compiler directive for parallel execution. |
| Standard-library-like type | A class or struct that models a named requirement or concept of the standard library by providing its member names (`value_type`, `iterator`, `begin`, `size`), or that is a type trait or a tag used with standard facilities. |
| Metaprogramming facility | A concept, a type trait, an alias template, or a function template whose purpose is to compute a type or a value during compilation, or a constexpr or consteval function intended for evaluation during compilation. |

## Notes

The custodian's directions of 2026-10-22 name the C++ Core Guidelines and their repository as the reference for C++, ask for a high-assurance standard at CSQ1 and CSQ0, take aspects of the house-style gist by b7r6 as an example, prefer the standard library, ask when raw pointers are right, give the naming convention, ask where the models of message passing, directive-based threading, and device offload belong, prefer generic and header-only code, recommend metaprogramming that a person is able to read, and ask for the latest C++ standard always. The custodian's rulings of 2026-10-23 add that the work is platform and compiler agnostic and that versions and tools are selected by the project, so the provisions state outcomes and the Notes name a compiler, library, or tool only to show a hazard that a provision guards against. Most provisions answer one of these; the rest apply the failure, reproducibility, and checking provisions of LVL0 and STND.CODE to C++. The sources are the project's research notes cxx-practice.md, cxx-high-assurance.md, and parallel-models.md, with the addendum a2-language-facts.md for Julia's bounds checks; a fact that they do not support is marked unverified.

The Core Guidelines are the reference for all C++ work (STND.CXX.1). They have several hundred rules and no releases, so the recorded revision is a commit of their repository, and the list of rules not followed holds those the checks exclude and those the work deviates from knowingly, not every rule left unchecked. Several of their rules carry what this standard leaves to them: a parameter that is never null is a reference or a pointer type that rejects null, and a smart pointer is a parameter only to take, share, or reseat ownership (F.7, F.23, R.30 to R.37); compile-time values come from `constexpr` functions rather than recursive template instantiation (T.123); `volatile` orders nothing between threads (CP.8); and initialization, const-correctness, casts, conversions, include hygiene, and ABI are covered. This standard departs from them in three places: a failure that the caller is designed to handle is returned rather than thrown (STND.CXX.19), against the preference of E.2 for exceptions, because the return keeps the failure in the signature where the caller sees it; header-only delivery is the default for all library code (STND.CXX.10), beyond what SF.2 asks; and the naming table extends their underscore style (NL.10) with CamelCase for classes, which the custodian uses. The gist agrees with them on passing small types by value, returning by value, views for sequences, `const` by default, and concepts over template gymnastics. Its other choices, explicit types over `auto`, a project result type, `#pragma once`, snake_case for every type, and a minimum name length, are not adopted: the first two conflict with the Core Guidelines (ES.11, E.2), the third is a vendor extension that SF.8 replaces by include guards, and the last two conflict with the custodian's convention and with NL.7.

The custodian asks for the latest standard always, and rules that outside high assurance the edition is "the latest possible that's supported by the compiler". STND.CXX.2 takes the newest edition that every compiler and standard library of the unit's matrix documents as supported, and admits each later feature that every one of them documents, one at a time under its feature-test macro. An edition or a feature that the documentation marks as experimental is not stated as supported. Code that uses a feature one compiler lacks fails to build there, so units built by different compilers sit at different editions, and a header that they share compiles at the lowest. The edition is reviewed with the pinned revisions under STND.DEPS.4, which also covers each unit of work that changes a compiler; a change of edition is a change of the computational environment that HW.7 and STND.DEPS.5 verify, and STND.DEPS.8 records each compiler revision with each result. Modules are not required; headers remain the interface. STND.CXX.3 holds agents to the level in force: an agent that meets a compiler error by lowering the edition, or creates a unit at an older one, loses the custodian's direction silently, while the decision record that the provision accepts costs one sentence. STND.INSTR.10 carries it into the agent instructions. STND.CXX.4 keeps the extensions that a foreign interface requires, those of a compiler for device code among them. STND.BUILD.11 and STND.BUILD.12 are the general rules for the settings of each compilation and for the warnings that fail the checks of a change, of which STND.CXX.4 and STND.CXX.25 are the C++ forms, and they reach further, to the settings of each link step and to each tool of the toolchain. An option that lets the compiler assume floating-point values are finite allows it to delete tests for not-a-number and infinite values (unverified), which is why STND.CXX.18 forbids such an option for a unit holding a required check of that kind. Options that relax floating-point semantics, contract multiply and add, or select an instruction set change delivered arithmetic, which HW.5 states; an option that trades accuracy for speed is a performance approximation, verified under NUMER.17. Compilers differ in whether they contract multiply and add by default (unverified), so each unit states its choice.

STND.CXX.5, STND.CXX.6, and STND.CXX.7 apply the Core Guidelines on ownership (R.3, I.11, F.60, I.13, ES.42). Something that is created and destroyed is a value, a container, or a `std::unique_ptr`; `std::shared_ptr` is for owners with independent lifetimes. An owning raw pointer appears only inside a resource handle or in the wrapper of STND.CXX.20, declared through a type alias that the checks recognize, so that a static check finds each other owning raw pointer. Explicit `new`, `delete`, `malloc`, and `free` therefore appear only there. Outside those places a plain `T*` points to one object it does not own, or is null, and a member that has to be reassignable is a pointer rather than a reference. A floating-point environment guard that restores the state of HW.CPU.3 on every return is a resource handle in this sense. A sequence is a `std::span` or `std::mdspan` at the editions that provide them, and a view type of the work at an edition without them; `std::span::operator[]` is unchecked unless the library checks of STND.CXX.27 are on. A register is reached most simply through an `extern volatile` object that the linker places, which needs no cast; otherwise one conversion of an integer to a pointer sits in the register layer with its suppression and reason, and a high-assurance coding standard treats such a conversion as a deviation. The register layer is where a command reaches the hardware, which is where CPS.5 puts its limit check. Ordinary data in a mapped region is reached by `std::start_lifetime_as` at an edition that provides it.

STND.CXX.8 prefers the standard library and records the reason and the evidence for each other choice. A measured shortfall covers speed and memory; the accuracy of a faster replacement is verified under NUMER.17. Within the standard library, `std::array`, `std::pmr` resources over a fixed buffer, and, at an edition that provides it, `std::inplace_vector` meet most limits on allocation; a `std::pmr::monotonic_buffer_resource` falls back to the free store unless its upstream is `std::pmr::null_memory_resource()`. A third-party replacement is a dependency under STND.DEPS. STND.CXX.9 covers what differs between standard library implementations for the same source: the distributions of `<random>`, the iteration order of unordered containers and `std::hash`, and the order of combination of `std::reduce` and the parallel algorithms. C++ written as a hardware description is code under this standard, and HDES governs its realization, whose design record HDES.3 asks.

The custodian prefers generic and header-only code. STND.CXX.11 writes an algorithm once as a constrained template where the work uses it for more than one type or where NUMER.27 asks that it admit derivative types; this departs from an unconditional preference because DSGN.12 and SIMPL.3 admit generality only for a present need, and NUMER.27 supplies that need for numerical methods. STND.CXX.10 delivers each library as headers, `inline` making that possible for non-template code, and departs from that only where the library wraps a foreign interface whose headers would reach each translation unit that includes it, or holds state of the whole process. Explicit instantiation in a source file with `extern template` declarations is a measured optimization that keeps the definition in the header, so a dual-number, interval, or extended-precision instantiation stays possible (NUMER.27). A header-only library is compiled with the options of each unit that includes it, so it states the edition and floating-point options it supports and stops with `#error` under an option that the source sees, testing the value of a predefined macro such as `__FINITE_MATH_ONLY__` rather than whether it is defined, since compilers define it as 0 or 1 (unverified). Contraction and the choice of instruction set often set no macro, so the library states them in its contract (STND.CXX.15).

The custodian recommends metaprogramming whose behavior a person is able to read. STND.CXX.12 recommends it for every property decidable at compile time, and STND.CXX.11 and STND.CXX.13 keep it readable, following the Core Guidelines (T.10, T.11, T.120, T.123, T.150): constraints are named concepts, which move a failed constraint to the call site and name it, rather than `std::enable_if`; compile-time values come from `constexpr` and `consteval` functions, `if constexpr`, folds, and pack expansion; and each facility carries its meaning and is tested by `static_assert`s whose expected results come from its stated requirement, since an assertion that restates the definition is tautological evidence (PRIME.2). The comment refers to those assertions rather than copying one, so the example does not drift from the code (STND.DOCS.13). A `static_assert` that rejects a caller's argument says in its message which requirement failed and what to change. At an edition without concepts, a constraint is a named trait checked by `static_assert`, with `std::enable_if` on that trait only where overloads have to be selected. A floating-point value computed during compilation uses the compiler's arithmetic, which is able to differ from the target's, so it is compared within a tolerance whose basis NUMER.11 gives.

The table of STND.CXX.14 holds the custodian's convention for variables, functions, classes, and structs, and snake_case for a type used like a standard-library feature, which the term Standard-library-like type makes a test; the custodian's ruling of 2026-10-23 keeps the other rows as drafted. They follow the standard library and the Core Guidelines (NL.8, NL.9, P1851R0), so that names in a call read as the standard library's do. Examples: `neutron_flux` and `advance_step` for variables and functions, `PointKineticsSolver` for a class, `ring_buffer` for a standard-library-like type, `is_unit_v` for a trait, `BoundaryKind` and `reflective` for an enumeration and an enumerator, `Value` or `T` for a template parameter, and a project-prefixed macro. A name is classified when it is introduced; a type that later gains `begin` keeps its name, as the published-interface exemption allows (DSGN.6). A naming check that sees only the kind of declaration is unable to separate the second, third, and fourth rows, since a standard-library-like type and a trait are classes or structs to it, so review applies the test; names fixed by the notation of NUMER.4 (`Λ`, `β_eff`) are exempted in its configuration. A short name in a small scope (`x`, `dt`, `n`) is admissible (NL.7). Statements are grouped by step as STND.CODE.13 recommends.

STND.CODE.3 asks for the contract at each declaration. In C++ the declaration is in a header, so its documentation sits there in a form a documentation tool extracts, and the definition does not repeat it (STND.CXX.15). That contract includes the statement of STND.CONC.6, whether concurrent calls to the interface are safe and the condition under which they are, which STND.CXX.15 cites and does not restate (GOV.31). The provision adds what a caller has to know that the type does not say, for arguments the function keeps beyond the call and for what it returns; an argument borrowed only for the call needs no statement. STND.DOCS governs how the comment is written.

STND.CODE.14 lists the responses that PRIME.4 admits, a thrown C++ exception among them, and the provisions of this standard that need a response refer to it. STND.CODE.15 asks for the declaration under which an ignored returned failure is diagnosed, and the nodiscard attribute meets it; on the return type it also covers indirect calls, through `std::function` among them, which lose an attribute on the function (unverified). A cast to `void` or an assignment to `std::ignore` discards the result, which STND.CODE.7 forbids for these failures and STND.CODE.12 governs for others. STND.CODE.6 keeps a check of untrusted input in every build, and STND.CODE.16 extends that to the checks of CPS.5 and CPS.9 where those apply. The settings that remove a check in C++ include `NDEBUG` for `assert`, the evaluation semantic of a contract assertion, the check mode of the library, and the contract settings of a support library; `NDEBUG` defined in the source before `<cassert>` is included is the case of the second sentence of STND.CODE.16, whose Notes give the reasoning from the C header; that `<cassert>` behaves in the same way is unverified. STND.CXX.18 keeps the binding C++ form of STND.CODE.21 for a translation unit that holds a required check of a floating-point value, as ruled for C++. Library checks therefore remain a second layer that STND.CXX.27 lets a budget remove. Each build that STND.BUILD calls a reporting build is a build from which the work reports a result or makes a release, and so a build that STND.CXX.27 reaches. A C++ exception that no handler catches, or that leaves a function declared `noexcept`, ends the program through `std::terminate`, whose default handler calls `std::abort` (unverified); whether an implementation of the standard library writes a diagnosis first is unverified for each implementation. STND.CXX.32 is the counterpart of the second sentence of STND.RUST.13 for a panic, and is conditioned as that sentence is: where the work installs a terminate handler, the handler delivers the diagnosis of a listed condition that an exception carries to it. Where the work installs none, an exception that no handler catches is a pass to the caller that STND.CODE.14 admits, and no binding provision of this standard or of STND.CODE asks the end of the program to carry a diagnosis; PRIME.4 states that outcome. STND.CXX.33 is the default for that case: where the handler that the implementation provides writes no diagnosis, it recommends that the program install one, or catch the exception in its entry point. It instantiates INTPR.8, the diagnostics captured by default, and applies from CSQ1 by the row of that provision in STND.CLASS.10. In a program that commands hardware, the end of the program through a terminate handler is a loss of the commanding software that CPS.4 verifies, and the designed safe state of PRIME.13 is reached on it, which HW.EMBED.4 states for each output. With C++ exceptions disabled, each throw that remains in the library ends the program (unverified for each library), which is a halt under STND.CODE.14 once the abort handler writes a diagnosis. A destructor does not let a C++ exception escape, which the language makes the default; a failure it detects goes to the response of STND.CODE.14, and the explicit release operation of STND.CXX.21 lets the caller see the failure first. Release calls that report earlier failures include the freeing of device memory and the destruction of a device stream, which report errors of asynchronous work (HW.GPU.3), and the closing of a file, which is able to fail on a full disk (unverified). A factory that takes the creating call puts a resource that a foreign function returns through an out-parameter into its handle before the next call that is able to fail (STND.CXX.20). STND.CXX.22 keeps a C++ exception out of C frames, through which ISO C++ defines no behavior for unwinding, and out of a structured block of a parallel directive, whose specification requires the exception to be caught in the same region by the same thread; a block that carries no error stores a `std::exception_ptr` or a status that the code after the region checks. Declaring an invoked function `noexcept` turns an escaped exception into `std::terminate`. STND.CONC.3 has each shared mutable object, handlers among the tasks that access it, follow one stated protection, and a protection by synchronization use a facility that the memory model of the language or library, or the ordering model of the hardware contract, defines as ordering accesses; in C++ those facilities are atomic operations and the synchronization facilities of the standard library, of the target, and of a library whose contract states its ordering, and `volatile` is none of them (CP.8). C++ adds one rule for handlers: a handler shares lock-free `std::atomic` objects (`is_always_lock_free`) or, for a signal handler, `volatile std::sig_atomic_t`, unless masking interrupts or another facility of the target orders the access (STND.CXX.23). The assumption attribute, `std::unreachable`, and compiler builtins of STND.CXX.24 make a false assumption undefined behavior.

This standard holds no rules for message passing, directive-based threading, or device offload beyond those boundary provisions, because each model is language-independent or vendor-specific and none is C++; STND.CONC holds the rules of concurrency that hold for every model and language, and the standard of each model holds the rules of that model. HW.GPU.3 already requires the completion status of offloaded work, and HW.CPU.3, HW.CPU.4, and HW.CPU.5 cover floating-point control state and thread counts.

The checking provisions state what each check decides; the formatter, the compilers' warning sets, the static checkers, the run-time detectors, and the library check modes are the project's choice in its repository configuration. Three hazards bear on the choice. A run-time detector that recovers after a report lets a test pass after undefined behavior, which STND.CXX.26 excludes by failing at the first detection. The second sentence of STND.CXX.26 is the C++ form of STND.CONC.25: in C++ the check that detects data races is a build of the code, asked wherever the work runs its code in more than one thread, and STND.CONC.25 has those tests fail at its first detection and run under a detection of lock-order inversions and deadlocks where the means of the work include one. Detectors of integer overflow and implicit conversion also report defined behavior, such as the unsigned wraparound of hashes and random-number generators (unverified), so a project that runs them suppresses each accepted report. A library check mode set differently in two units of one program breaks the one-definition rule, so it is set once for the program. Warnings fail the project's own checks and not the builds of code that uses a header-only library, whose dependency headers are treated as system headers. Hardening against memory corruption by attack is governed by GUARD.17 and the threat model. The counterpart of STND.CXX.27 in Julia is a default of the Julia standard, added with this revision, that keeps the bounds checking of the production configuration unless a measurement and a decision record show its cost; STND.JL.34 and STND.RUST.20 concern the runs of the tests. In Julia an index is checked unless `@inbounds` or the execution setting `--check-bounds=no`, under which no bounds check is emitted, removes the check (a2-language-facts.md); STND.JL.13 keeps the check of an index from untrusted input from either, STND.JL.18 asks the reason at each `@inbounds`, the first sentence of STND.JL.34 runs the tests once under the production setting. In safe Rust, indexing is checked in every build (unverified here), and STND.RUST.20 concerns overflow checks and debug assertions. The C++ standard library checks no precondition unless a check mode of it is chosen (unverified), so STND.CXX.27 asks for that mode in each reporting build, and the checking builds of STND.CXX.26 are the counterpart of the forced checks of STND.JL.34. A test under the settings of the reporting build is the evidence that HW.7 asks wherever a claim rests on the delivered arithmetic that those settings fix, in C++ as in Julia.

High assurance. STND.CODE.17 to STND.CODE.20 hold the high-assurance provisions for every language, on the custodian's rulings for C++ that they accept any high-assurance coding standard that a decision record of the work adopts, and that for high assurance "the validation status is more important than the language standard". High-assurance coding standards for safety-related C++ restrict the language to a subset that analyzers are able to check, commonly by limiting dynamic allocation, recursion, unbounded loops, C++ exceptions, casts, unions, and the preprocessor. An assertion that such a standard keeps in production builds responds as STND.CODE.14 provides, entering the designed safe state of PRIME.13 for a component that commands hardware, which CPS.4 verifies and HW.EMBED.4 states for each output, and halting with a diagnosis for one that does not, such as a criticality or shielding calculation. In C++, the edition of STND.CODE.19 is an edition of the ISO C++ standard that the adopted standard covers and for which each compiler and standard library implementation of the toolchain matrix of the unit holds the validation or qualification that the work requires; it is often older than the edition of STND.CXX.2, which yields to it, and the provisions of this standard that name idioms of later editions give the forms for earlier ones. A header that a CSQ0 controller and a CSQ3 simulation share is high-assurance code (GOV.14); the human owner may record a less severe class for a component shown to be isolated (GOV.13), which keeps a simulation's large dynamic arrays out of a rule on allocation.

Under STND.CLASS.10, each default instantiates only VV, REPRO, INTPR, DSGN, SIMPL, RSRC, or a provision of HW, CPS, or NUMER, and applies from CSQ3; work of CSQ4 may omit it. Several apply earlier than the part of LVL0 they instantiate, and so tighten above the floor (PRIME.15). STND.CXX.6 and STND.CXX.7 instantiate DSGN.4, and STND.CXX.21 and STND.CXX.22 DSGN.5, which STND.CLASS.10 applies from CSQ2. STND.CXX.13 takes the expected results of its assertions from a stated requirement, the reference independent of the implementation that STND.CLASS.10 asks of VV.1 from CSQ2. STND.CXX.26 instantiates the verification of DSGN.15, applied from CSQ2. The provisions of STND.CONC that STND.CXX.15 and STND.CXX.23 cite, and of which the Notes give STND.CXX.26 as a form, take the same onsets, STND.CONC.3 and STND.CONC.6 from CSQ3 and STND.CONC.25 from CSQ2, so the citations move no rule to another class. STND.CXX.24 and STND.CXX.27 instantiate the checking of DSGN.2 that STND.CLASS.10 applies from CSQ1. Each asks for a type, a check that a tool runs, or a statement. The provisions of STND.CODE that the defaults cite keep their own onsets: STND.CODE.17 and STND.CODE.19 from CSQ1 for high-assurance code, the record of STND.CODE.20 wherever such a standard is adopted, and the binding STND.CODE.14 and STND.CODE.15 at every class, so the citations move no rule to another class. STND.CXX.18 and STND.CXX.32 bind at every class, CSQ4 included. STND.CXX.18 costs one choice of compiler option for a unit that holds a required check. STND.CXX.32 reaches only a terminate handler that the work installs and a listed condition that already ends the program there, and asks only for the actionable diagnosis that PRIME.4 names, at the cost of the wording of that handler; without it a handler of the work is able to end the program without a diagnosis. It asks for no work that PRIME.4 does not, so it raises no floor (GOV.11); no ruling of the custodian covers it, and the argument is the one that the ratification of 2026-10-24 accepted for the second sentence of STND.RUST.13, which is conditioned in the same way. STND.CXX.33 is a default that instantiates INTPR.8 and applies from CSQ1, the class from which STND.CLASS.10 asks diagnostics captured by default. STND.CXX.3 asks an agent for one decision record when it lowers an edition, or creates a unit below the edition of STND.CXX.2 or its project alternative, which at CSQ4, where STND.CXX.2 may be omitted, costs one sentence; without it the custodian's direction on the edition is lost silently. That STND.CXX.3 and STND.CXX.18 raise no floor (GOV.11) is the custodian's ruling of 2026-10-23 (PRIN.10). Work moved to CSQ1 or CSQ0 meets STND.CODE.17, STND.CODE.18, STND.CODE.19, and STND.CODE.20 before it is relied upon at that class (GOV.14).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES | Hardware design |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| HW.EMBED | Embedded controllers |
| HW.GPU | Accelerators |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.BUILD | Build standard |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.INSTR | Agent instructions |
| STND.JL | Julia standard |
| STND.RUST | Rust standard |
| VV | Correctness |

## Provisions

### Language level

#### STND.CXX.1 Core Guidelines reference

Default. Instantiates INTPR.1, REPRO.7.

The repository configuration SHOULD name the C++ Core Guidelines, at a recorded revision, as the reference for the C++ practice of the work, and list each of their rules that the checks of STND.CXX.25 exclude and each from which the work knowingly deviates, with the reason (INTPR.1, REPRO.7). Where this standard and the Core Guidelines differ, the work SHOULD follow this standard (INTPR.1).

#### STND.CXX.2 Language edition

Default. Instantiates DSGN.3, INTPR.1, REPRO.9.

Other than for an edition that STND.CODE.19, a hardware contract, or a qualification of the toolchain fixes, each translation unit SHOULD be compiled at the newest edition of the ISO C++ standard that the documentation of each compiler and each standard library implementation of its toolchain matrix states as supported (DSGN.3, INTPR.1). Where the documentation of each compiler and standard library implementation of its toolchain matrix states support for a feature of a later edition, a unit other than one of high-assurance code that STND.CODE.19 governs MAY be compiled at that later edition and use that feature under a test of its feature-test macro whose failure stops the build with a diagnostic (DSGN.3). At each review of STND.DEPS.4, the edition in force for each translation unit SHOULD be reviewed against this provision (REPRO.9).

#### STND.CXX.3 Agent edition changes

Binding. Instantiates GOV.48, DSGN.3.

Other than in a change whose decision record names the compiler, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain that requires it, an agent SHALL NOT lower the edition in force for a translation unit (GOV.48, DSGN.3). Other than in a change whose decision record names the compiler, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain that requires it, an agent SHALL NOT state for a translation unit that it creates an edition older than the edition that STND.CXX.2, or the alternative that a project instrument adopts in its place, gives (GOV.48, DSGN.3).

#### STND.CXX.4 Stated build settings

Default. Instantiates SIMPL.6, REPRO.2, HW.5.

The repository configuration SHOULD state the edition in force for each translation unit, and stop the build of a unit whose compiler does not provide that edition (SIMPL.6, REPRO.2). Other than an extension that a foreign interface of a unit requires, each language extension of a compiler SHOULD be disabled by the repository configuration (SIMPL.6). The repository configuration SHOULD state, for each translation unit, each option that sets its floating-point semantics, the contraction of its operations, its target instruction set, or the mode of the checks of its standard library (REPRO.2, HW.5).

### Ownership

#### STND.CXX.5 Owned resources

Default. Instantiates DSGN.14, DSGN.3.

Each owned resource SHOULD be released by the destructor of the object that owns it, or of the last of the objects that share its ownership (DSGN.14). A raw pointer SHOULD own the object it points to only inside the implementation of a resource handle, or of a wrapper under STND.CXX.20 (DSGN.14). Each raw pointer that owns the object it points to SHOULD be declared through a type alias that the static checks of STND.CXX.25 recognize as marking ownership (DSGN.3).

#### STND.CXX.6 Sequences and pointer arithmetic

Default. Instantiates DSGN.4, SIMPL.11.

Other than at a foreign interface, each sequence that a function receives without ownership SHOULD be passed as a view or a range that carries its extent (DSGN.4). Pointer arithmetic SHOULD occur only inside the implementation of a container, a view, an iterator, or a loop whose comment states the bounds invariant that keeps each access in range (SIMPL.11).

#### STND.CXX.7 Device and register memory

Default. Instantiates DSGN.4, DSGN.16.

Each pointer into the memory of an accelerator or of a memory-mapped device SHOULD have, at each interface that passes it, a type distinct from that of a pointer into host memory (DSGN.4). Each access to a memory-mapped register SHOULD take place inside the one layer of the work that holds the address of that register (DSGN.16).

### Library use

#### STND.CXX.8 Standard library first

Default. Instantiates SIMPL.4, REPRO.7, RSRC.4.

Where the standard library at the edition in force provides a facility that meets a need of the work within its budgets, the work SHOULD use that facility (SIMPL.4). Where the work uses another facility in its place, a comment at that use, or a decision record that the comment cites, SHOULD state the reason from the table of this provision with the evidence that its row gives (REPRO.7, RSRC.4).

| Reason | Evidence |
| --- | --- |
| Freestanding target | The part of the standard library, atomic operations included, that the implementation for the target provides |
| No dynamic allocation | The constraint of the target, or the rule of the high-assurance coding standard of STND.CODE.17, that forbids allocation on the path |
| Bounded timing | The timing budget of the path, and the measured or analyzed worst case of the standard facility on it |
| C++ exceptions disabled | The build setting that disables C++ exceptions, and the throwing operations of the standard facility that the path reaches |
| Rule of the high-assurance coding standard | The rule, and the operation of the standard facility that it forbids |
| Measured shortfall | The stated budget, and a measurement of both facilities with the compiler, its options, the input sizes, and the hardware recorded |
| Reproducibility across the toolchain matrix | The behavior that the standard leaves implementation-defined or unspecified, and the test of REPRO.3 that the other facility passes |
| Accelerator memory | The memory space of the accelerator that the standard facility does not address |
| Foreign interface | The foreign interface whose types or binary layout the other facility matches |
| Synthesis subset | The facilities that the synthesis tool of a hardware description written in C++ accepts |

#### STND.CXX.9 Implementation-defined library behavior

Default. Instantiates REPRO.2, REPRO.3.

Where a reported result depends on behavior of a standard-library facility that the C++ standard leaves implementation-defined or unspecified, the work SHOULD compute that result with an implementation of the facility that it owns or pins, or record the revision of the standard library implementation with each such result (REPRO.2, REPRO.3).

#### STND.CXX.10 Header-only libraries

Default. Instantiates SIMPL.1, SIMPL.6, REPRO.2, RSRC.4, NUMER.27.

Other than a library that wraps a foreign interface whose headers it keeps from the code that includes it, or that holds state of the whole process, each library of the work SHOULD be delivered as headers alone (SIMPL.1). Each library delivered as headers SHOULD state the minimum edition and the floating-point options that it supports, and stop compilation with a diagnostic under an edition, or an option that the compiler makes visible to the source, that it does not support (SIMPL.6, REPRO.2). Where a measurement shows that compiling a template in each translation unit exceeds a stated budget of build time or binary size, the library SHOULD keep the definition of the template in its header and add explicit instantiations in a source file, with matching extern template declarations (RSRC.4, NUMER.27).

### Templates

#### STND.CXX.11 Constrained generic code

Default. Instantiates DSGN.11, NUMER.27, DSGN.1, INTPR.1.

Where an algorithm or a data structure of the work applies unchanged to more than one type that the work uses or that NUMER.27 asks it to admit, it SHOULD be written once, as a constrained template (DSGN.11, NUMER.27). Where the edition in force provides concepts, each template SHOULD state the requirements on its arguments in its declaration, by named concepts or by a requires-clause that combines named concepts (DSGN.1, INTPR.1). Where the edition in force does not provide concepts, each template SHOULD state those requirements by static assertions on named type traits, each assertion naming the requirement that it checks (DSGN.1, INTPR.1).

#### STND.CXX.12 Compile-time checking

Default. Instantiates DSGN.3.

Where a property of a type or of a constant on which the work relies is decidable during compilation, code SHOULD check that property during compilation (DSGN.3).

#### STND.CXX.13 Documented metaprogramming facilities

Default. Instantiates INTPR.1, VV.1.

Each metaprogramming facility SHOULD carry a comment that states what it computes and the semantic requirement of each concept that it defines, and that refers to the static assertions that follow it as its examples (INTPR.1). Each metaprogramming facility SHOULD be accompanied, in its header or in a paired test, by static assertions of its result for at least one argument that it accepts and, for a constraint, at least one that it rejects, each expected result taken from the stated requirement (VV.1).

### Source conventions

#### STND.CXX.14 Naming conventions

Default. Instantiates INTPR.1, INTPR.4.

Each name that the work declares in C++ source SHOULD take the form that the table of this provision gives for its kind (INTPR.1). A name whose form a dependency, the standard library, a published interface of the work, or the documented notation of NUMER.4 fixes MAY keep that form (INTPR.1, INTPR.4).

| Kind of name | Form |
| --- | --- |
| Variable, function, data member, namespace | snake_case |
| Class or struct | CamelCase |
| Standard-library-like type | snake_case |
| Concept, type trait, and alias of the result of a trait | snake_case, formed as the standard library forms its own |
| Other type alias | The form of the kind of type that it names |
| Enumeration type | CamelCase |
| Enumerator, and variable declared constexpr or const at namespace scope | snake_case |
| Template parameter | CamelCase, or one capital letter |
| Macro | Upper case, with the prefix of the project |

#### STND.CXX.15 Declaration comments

Default. Instantiates INTPR.1, INTPR.3, DSGN.1.

The documentation comment of each declaration in a header that another component uses SHOULD immediately precede that declaration, in a form that a documentation tool of the work extracts (INTPR.1, INTPR.3). In addition to what STND.CODE.3 and STND.CONC.6 ask, that comment SHOULD state the owner and the period of validity of each pointer, reference, view, and iterator that the declaration returns or keeps beyond the call, and each C++ exception or error value by which it reports failure (DSGN.1).

### Failures

#### STND.CXX.18 Checks no option removes

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9.

A translation unit that holds a check of a floating-point value that STND.CODE.6, CPS.5, or CPS.9 requires SHALL NOT be compiled with an option that lets the compiler assume that floating-point values are finite (PRIME.4, DSGN.2, STND.CODE.21).

#### STND.CXX.19 Failure channel

Default. Instantiates SIMPL.6, DSGN.1.

The repository configuration SHOULD state, for each build, whether C++ exceptions are enabled (SIMPL.6). Where C++ exceptions are enabled, a failure that the caller is designed to handle SHOULD be reported by the return value (DSGN.1). Where C++ exceptions are disabled in a build, code compiled into it SHOULD NOT reach a standard-library operation whose failure the path is designed to handle (DSGN.1).

#### STND.CXX.20 Foreign resource handles

Default. Instantiates DSGN.14.

Each owned resource that a foreign interface creates for the work SHOULD pass to a resource handle of the work before each other operation that is able to fail (DSGN.14). A resource handle SHOULD NOT release a resource that the foreign interface predefines (DSGN.14). A resource handle SHOULD NOT release a resource that another component owns (DSGN.14).

#### STND.CXX.21 Status and release failures

Default. Instantiates DSGN.5, DSGN.1.

Each foreign function whose status return reports a failure of a kind that PRIME.4 lists SHOULD be called through a function of the work that STND.CODE.15 covers (DSGN.5). Where the release of an owned resource is able to report a failure that affects a result, its resource handle SHOULD provide an operation that releases it and returns that failure, called before the result is relied upon (DSGN.1). A destructor that detects a failed release SHOULD respond to it as STND.CODE.14 or STND.CODE.12 provides, without letting a C++ exception escape (DSGN.1).

#### STND.CXX.22 C++ exceptions at foreign boundaries

Default. Instantiates DSGN.5.

Each C++ exception raised in code that a foreign interface invokes SHOULD be caught within that code (DSGN.5). Where the foreign interface carries errors, a C++ exception so caught SHOULD be converted to an error that it carries (DSGN.5). Where the foreign interface carries no error, a C++ exception so caught SHOULD be stored in an object that code outside the interface checks after the invocation returns, and answered there as STND.CODE.14 requires (DSGN.5).

#### STND.CXX.23 Synchronization of shared state

Default. Instantiates DSGN.15.

Where no synchronization facility of the target orders the accesses to an object that a signal or interrupt handler shares with the code it interrupts, that object SHOULD be a lock-free atomic object or, for a signal handler, an object of type volatile std::sig_atomic_t (DSGN.15, STND.CONC.3).

#### STND.CXX.24 Compiler assumptions

Default. Instantiates DSGN.1, DSGN.2.

Each condition that code states to the compiler as an assumption, by the assume attribute, an unreachable marker, or a builtin of a compiler, SHOULD be established by a check or a recorded proof that precedes the assumption (DSGN.1, DSGN.2).

#### STND.CXX.32 Diagnoses from terminate handlers

Binding. Instantiates PRIME.4.

Where the work installs a terminate handler, that handler SHALL deliver to the operator, or to the record of the run, a diagnosis of each condition that PRIME.4 lists and that a C++ exception carries to it (PRIME.4, STND.CODE.14).

#### STND.CXX.33 Terminate handlers where defaults are silent

Default. Instantiates INTPR.8.

Where the terminate handler that the implementation provides writes no diagnosis of a condition that PRIME.4 lists and that a C++ exception carries to it, each program of the work SHOULD install a terminate handler that writes one, or catch such an exception in its entry point and respond to it as STND.CODE.14 provides (INTPR.8).

### Checking

#### STND.CXX.25 C++ static checks

Default. Instantiates DSGN.3.

The static checks that the repository configuration names for C++ SHOULD include the warnings of each compiler of the toolchain matrix at a recorded set, a check of the rules of the Core Guidelines that the work follows, and a check of the names of STND.CXX.14 (DSGN.3). Each compiler warning on the work's own source SHOULD fail the checks of the change that causes it (DSGN.3).

#### STND.CXX.26 Run-time error detection

Default. Instantiates DSGN.3, DSGN.15.

Among the checks of each change to the C++ code of the work, its tests SHOULD run in a build that detects at run time invalid memory accesses and each kind of undefined behavior that the repository configuration lists, and fails the test at the first detection (DSGN.3). Where the work runs its code in more than one thread, its tests SHOULD also run in a build that detects data races at run time (DSGN.15).

#### STND.CXX.27 Library precondition checks

Default. Instantiates DSGN.2, RSRC.4, REPRO.7.

Each build from which the work reports a result or makes a release SHOULD enable the precondition checks that its implementation of the standard library provides for production use (DSGN.2). Where a measurement shows that those checks exceed a stated budget, a decision record SHOULD state the measurement and each part of the work built without them (RSRC.4, REPRO.7).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-23 | Adopted. |
| 1.1 | 2026-10-24 | Minor amendment (GOV.41): STND.CXX cites STND.CONC for the model-neutral part of its concurrency rules. STND.CXX.23 drops its first sentence, which stated the synchronization case of STND.CONC.3 without C++ content, and keeps its rule for objects shared with signal and interrupt handlers, citing STND.CONC.3 and instantiating DSGN.15 alone; STND.CXX.15 cites STND.CONC.6 in place of restating that the comment states whether concurrent calls are safe; the Notes name the C++ facilities that order accesses, give the second sentence of STND.CXX.26 as the C++ form of STND.CONC.25, describe the standards of other models as adopted, name STND.CXX.4 and STND.CXX.25 as the C++ forms of the general rules for build settings and warnings, and cite HDES.3 for the design record of a realization; References lists STND.CONC and HDES. |
| 1.1.1 | 2026-10-24 | Editorial amendment (GOV.41): the informative Notes cite STND.BUILD.11 and STND.BUILD.12 as the general rules of which STND.CXX.4 and STND.CXX.25 are the C++ forms, where they named the standard for building software in words, and relate each reporting build of STND.BUILD to the builds that STND.CXX.27 reaches; References lists STND.BUILD; no obligation, permission, or defined meaning changes. |
| 1.2 | 2026-10-25 | Minor amendment (GOV.41): STND.CXX.16, STND.CXX.17, STND.CXX.28, STND.CXX.29, STND.CXX.30, and STND.CXX.31 are withdrawn, their outcomes now STND.CODE.14, STND.CODE.15, STND.CODE.17, STND.CODE.18, STND.CODE.19, and STND.CODE.20 for every language, and the front matter lists them as withdrawn; STND.CXX.18 drops its first sentence, now the first sentence of STND.CODE.16, and keeps its second, the binding C++ form of the default STND.CODE.21, as ruled; STND.CXX.2, STND.CXX.8, STND.CXX.21, and STND.CXX.22 cite the provisions of STND.CODE in their place, and the second sentence of STND.CXX.2 leaves the later features of high-assurance code to STND.CODE.19; new STND.CXX.32 (binding, PRIME.4) has a terminate handler that the work installs deliver the diagnosis of each listed condition that a C++ exception carries to it, the C++ counterpart of the second sentence of STND.RUST.13 and conditioned as it is; new STND.CXX.33 (default, from CSQ1) recommends a terminate handler, or a catch in the entry point, where the handler that the implementation provides writes no diagnosis of a listed condition; Terms import Untrusted input, High-assurance code, and High-assurance coding standard from STND.CODE and drop this standard's own definitions of the last two; the Purpose and the Notes cite STND.CODE for the moved rules and for the reasoning on `assert`, give the reason why STND.CXX.27 has no counterpart in STND.JL.34 and STND.RUST.20, and state the floor argument and the onset of STND.CXX.32. |
