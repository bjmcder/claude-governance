# C standard (STND.STDC) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 118 (2026-10-24). This reading copy is composed from the per-provision files in STND/STDC/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the coding practice that is specific to C. It adds to STND.CODE, STND.DOCS, and STND.CONC only what the language makes necessary. It applies to C source each provision of STND.CXX whose outcome holds for C, in a C reading that its Terms define, in place of restating it (STND.STDC.1, STND.STDC.2, and STND.STDC.3), and asks a test of each conditional feature that a translation unit uses (STND.STDC.4). It states how code without destructors releases what it owns, passes sequences with their extent, and keeps each access within its object and the lifetime of that object (STND.STDC.5 to STND.STDC.10). It excludes the classes of undefined behavior that optimizers exploit and keeps the correctness of code independent of options that define them (STND.STDC.11 to STND.STDC.16), and covers integer conversions and the types of sizes (STND.STDC.17 and STND.STDC.18), strings and buffers (STND.STDC.19 to STND.STDC.22), the preprocessor (STND.STDC.23, STND.STDC.24, and STND.STDC.25), restrict-qualified pointers and variable-length arrays (STND.STDC.26 and STND.STDC.27), failures, errno, and ignored results (STND.STDC.28 to STND.STDC.33), signal handlers and bit-fields shared between threads (STND.STDC.34, STND.STDC.35, and STND.STDC.36), data that crosses to other languages (STND.STDC.37), and the checks of C code (STND.STDC.38, STND.STDC.39, and STND.STDC.40). Through STND.STDC.1 and STND.STDC.2, the high-assurance provisions of STND.CXX apply to C: conformance to the high-assurance coding standard that a decision record of the work adopts, claims of conformance limited to what was checked, an edition that the standard covers and the toolchain is validated for, and recorded deviations.

STND.STDC.2 instantiates PRIME.4 and PRIME.2, STND.STDC.28 and STND.STDC.29 instantiate PRIME.4, and STND.STDC.3 instantiates GOV.48 and binds agents alone; these four are binding at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is compiler, edition, platform, and tool agnostic: its provisions name the constructs of C and no edition, compiler, library to depend on, platform, or tool, and the repository configuration or a project instrument chooses them (GOV.18). It holds no provision on building; the settings that the repository configuration states for a translation unit of C are those of the C reading of STND.CXX.4. The rules of concurrency that hold for every language are in STND.CONC, which applies to C by its own scope and which this standard cites and does not restate.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration and Static check have the meanings that STND.CODE gives them. Translation unit, Toolchain matrix, and Owned resource have the meanings that STND.CXX gives them, and Edition in force the meaning that STND.CXX gives it in its C reading. Concurrent task, Shared mutable object, and Protection have the meanings that STND.CONC gives them; a signal handler is a concurrent task.

| Term | Definition |
| --- | --- |
| C source | Source of the work in C: each file that a compiler of the work translates as C, and each header that such a file includes, other than a header of the implementation or of a dependency. A header that C and C++ translation units both include is C source and C++ source. |
| C reading | Of a provision or a term of STND.CXX: that provision or term applied to C source, with C, the ISO C standard, the C standard library, and an implementation of the C standard library in place of C++, the ISO C++ standard, the C++ standard library, and a standard library implementation; with each term that STND.CXX defines and each provision of STND.CXX that it cites taken in the same reading; and with the change that the row of that provision in the table of STND.STDC.1 or STND.STDC.2 gives. |
| Conditional feature | A feature of an edition of the ISO C standard that the edition lets an implementation omit, and whose absence the implementation reports by a predefined macro that the edition names. |
| Undefined behavior | Behavior for which the ISO C standard, at the edition in force, imposes no requirements. |
| Signal-safe function | A function that the ISO C standard, or the documentation of the platform on which the code runs, states as one that a signal handler is able to call. |
| Untrusted input | Data that reaches the work from outside its own code, other than data from a source that the threat model of the project records as trusted. |

## Notes

The standard follows the custodian's standing directions for the round of 2026-10-24: it is agnostic of compiler, edition, platform, implementation, and tool, states practice that has held across the editions of C, raises no floor (GOV.11), and cites the provision that holds an outcome rather than restating it (GOV.31). It is modeled on STND.CXX, in the form of STND.PY and STND.JL. Each provision states the outcome that a tool or a reviewer decides from the source, the repository configuration, and the record of checks, and names the constructs of C, which GOV.18 admits at LVL2; the Notes name a compiler, a library function, or a coding standard only to show a hazard that a provision guards against. The source is the project's research note research/c-notes/c1-c-language.md (cited as c1). Its quotations of the working draft of the newest edition of the ISO C standard and of three papers are full text, and its other sources were read as extracts that a retrieval tool wrote; its source S24 is excluded from the evidence, and the argument that rests on it is not used. A fact that c1 does not support is marked unverified.

C reading. STND.CXX holds practice specific to C++, and much of it holds for C, because the two languages share a model of compilation, the kinds of their undefined behavior, and the failures at the boundary of a library. STND.STDC.1, STND.STDC.2, and STND.STDC.3 apply those provisions to C source in their C reading, so that each keeps one text, its mode, and its class onset, and this standard holds only what C adds (GOV.31). A provision so applied is a default or binding for C as it is for C++, and a project replaces the C reading of a default by a recorded decision as it replaces any default (REPRO.7). The citation follows the revision of STND.CXX in force. Where a provision of STND.CXX cites STND.CONC, the cited provision applies to C by the scope of STND.CONC and needs no reading.

Provisions of STND.CXX that apply to C. STND.CXX.2, STND.CXX.3, and STND.CXX.4 give the edition, the agent's duty not to lower it, and the stated build settings. The default dialect of at least one widely used compiler enables its extensions, even where they change the meaning of the base standard (c1, practice 1), which the second sentence of STND.CXX.4 disables. A compiler's name for the newest edition has changed between its releases, and its default is a dialect and not an edition (c1, Editions), so the repository configuration names an edition by the standard it denotes and by the value of the version macro that the edition defines. The row of STND.CXX.2 names, in place of its feature-test macro, the predefined macro or the preprocessor test by which each implementation reports a feature, the means by which the editions of C report features (c1, Editions). STND.CXX.7 holds for C as written: a register is reached through a volatile-qualified object (c1, What the corpus already holds), and the layer that holds its address is where CPS.5 puts its limit check. STND.CXX.9 holds for C as written; which facilities of the C library leave a reported result to the implementation, the sequence of its pseudo-random generator, the order of equal elements after its sort, and the accuracy of its mathematical functions among them, is not in c1 and is unverified. STND.CXX.12 is checked in C by static assertions; c1 lists it among the provisions on templates that do not carry and, in its section on the preprocessor, as one that does, and its text names no C++ facility. STND.CXX.15 gives the ownership contract that C needs most (c1, What the corpus already holds); its row keeps the pointers and error values of the comment, since C has no reference, view, iterator, or C++ exception, and STND.STDC.6 adds the function that releases what a declaration returns, since C has no destructor that names it. STND.CXX.16 keeps every response but a C++ exception. STND.CXX.17 is met by the attribute that an edition provides for a result that is not to be discarded, or by a compiler's equivalent attribute and the warning for it (c1, Error reporting and ignored returns). STND.CXX.18 holds for C as written: an assertion is removed by defining NDEBUG, and a test for non-finite values by an option that lets the compiler assume finite values. STND.CXX.23 gives the C type for an object that a signal handler shares. STND.CXX.24 covers the unreachable marker of an edition that has one, and the builtins of a compiler. STND.CXX.25, STND.CXX.26, and STND.CXX.27 give the warnings, the run-time detection that fails at its first detection, and the library checks in production, the last for a C library that offers checks of the buffers that its functions write; the row of STND.CXX.25 drops the checks of the Core Guidelines and of the names of STND.CXX.14. STND.CXX.28 to STND.CXX.31 apply nearly as written, because they refer to the high-assurance coding standard that a decision record adopts; the term reads "for C" in its C reading.

Provisions of STND.CXX that do not apply to C. STND.CXX.1 names the Core Guidelines, which concern C++. STND.CXX.5 and STND.CXX.20 rest on destructors and resource handles, which C lacks, and STND.STDC.5 states their outcome, release on every path, for C. STND.CXX.6 rests on view types, and C has no standard one, so STND.STDC.7 has a pointer travel with its extent and STND.STDC.8 keeps each access within its object. STND.CXX.8 compares the C++ standard library with other facilities by reasons that are specific to C++, and STND.CXX.10 holds the custodian's preference for libraries of C++ delivered as headers, which c1 finds does not carry. STND.CXX.11 and STND.CXX.13 concern templates and metaprogramming. The naming table of STND.CXX.14 is the custodian's convention for C++, and no convention for C has been given, so names in C follow STND.DOCS.12 and the layout tool of STND.CODE.5. STND.CXX.19 asks whether C++ exceptions are enabled, and its other sentences have no subject without them; STND.STDC.32 states the channel of failure for C. STND.CXX.21 holds its outcomes through a resource handle and a destructor, which C lacks; STND.STDC.30 and STND.STDC.31 state them for C. STND.CXX.22 is the rule that the C++ side of a boundary obeys; c1 leaves unverified the statement that the ISO C standard defines a nonlocal jump only within C frames, so no provision rests on it, and STND.OMP.21 already keeps such a jump out of a structured block of OpenMP.

What the corpus already holds. STND.CODE.3 asks for the contract at each declaration, STND.CODE.4 for the static checks and a suppression at the location of each finding left in place, STND.CODE.5 for a layout tool, STND.CODE.6 and STND.CODE.7 for checks of untrusted input that no setting removes and for no discarded failure of a kind that PRIME.4 lists, STND.CODE.12 for the reason of each other discard, and STND.CODE.13 for statements grouped by step; each applies to C as to every language. STND.CONC applies to C by its own scope: a thread of the C library or of the platform, and a signal handler, is a concurrent task, and the protection of each shared mutable object (STND.CONC.3), the sequentially consistent order of atomic operations or a stated reason for a weaker one (STND.CONC.4), publication and lifetimes (STND.CONC.5), concurrent calls in contracts (STND.CONC.6), lock order and conduct (STND.CONC.7 and STND.CONC.8), the parent that joins the threads that it starts (STND.CONC.12), a library that leaves signal handling unchanged (STND.CONC.17), a child process of a threaded program (STND.CONC.19), and race detection in tests (STND.CONC.25) apply unchanged. STND.DEPS.4 reviews the edition with the pinned revisions, STND.DEPS.8 records the revision of each compiler with each result, STND.DEPS.9 lists each analyzer, and STND.DEPS.11 keeps a library that a C project copies into its tree apart, with its origin, revision, and license identity. STND.DOCS.13 runs the examples of documentation comments. NUMER.16 and NUMER.17 govern an option that relaxes floating-point semantics or contracts multiply and add on the path of a numerical result, HW.5 records the delivered arithmetic, and HW.CPU.3 has a path that changes its floating-point control state, which C does through the functions of its floating-point environment, confirm and restore it; whether such code also needs the pragma by which C lets a translation unit access that environment is not in c1 and is unverified. STND.MPI.11 states the release of MPI handles, which in C have no destructor.

Ownership without destructors. C has no destructor, so an owned resource is released by code that each path out of a function reaches, and ownership is a convention that the code and its contracts carry (c1, Resource management without destructors). One coding style of an operating-system kernel gives the reasons for one exit region per function, reached by jumps to labels that release what has been acquired in reverse order: the code is easier to follow, nesting is reduced, and the error of a change that leaves one of several exit points without its update is prevented; it asks that each label be named for what it does (c1, S15). A wrapper that owns the release and takes a callback, or a table of acquired items, meets STND.STDC.5 as well. Some compilers offer a cleanup attribute on a variable as an extension, and a deferred-release facility was on the agenda of the committee of the language (unverified); neither is part of a published edition, so STND.STDC.5 states the outcome and not the mechanism. The result of a reallocation assigned to the only pointer to the original block loses that block when the reallocation fails, which is a path on which the block is not released (STND.STDC.5); a reallocation to size zero is undefined in the newest edition (c1, S1). A size computed as a count times the size of an element wraps (STND.STDC.18; c1, S21). Setting a persisting pointer to null at the release lets a later check of that pointer find that its object is gone (STND.STDC.9; c1, hazard table).

Undefined behavior. The overview annex of the working draft of the newest edition lists 221 circumstances of undefined behavior (c1, S1, full text; the count was not compared with the published text and is unverified for it). A compiler is allowed to assume that none of them occurs, and an optimizer removes code that is correct only if one does: a test that x + 1 exceeds x becomes true, a signed loop counter lets the compiler assume a trip count, a dereference ahead of a test for null lets the test go, and a type-based aliasing assumption turns a loop into one call that fills memory (c1, S4, extract). The language defines no trap for these cases, so a crash is not a guaranteed symptom. A check that relies on the undefined operation itself is the common casualty: a test of a pointer plus a length against the pointer, written to detect wraparound, is removed, and a static checker for such code found 160 bugs that the projects confirmed and fixed and estimated that such code exists in 40 percent of 8,575 packages of one distribution that contain C or C++ (c1, S6, full text) (STND.STDC.13). STND.STDC.8 to STND.STDC.15 cover the classes that c1 finds behind most defects: out-of-bounds access, use after the end of a lifetime, uninitialized reads, signed overflow, division, shifts, aliasing, and unsequenced modification. Two's complement became the only representation of signed integers in the newest edition, and signed overflow stayed undefined (c1, hazard table). A read of an uninitialized automatic object that could have been declared register is undefined, and another such read gives an unspecified value or a trap representation, and compilers treat both as license (c1, hazard table); an option that initializes automatic storage is a defense and not a reason to leave an object uninitialized (STND.STDC.10). The padding of a structure written out of the process discloses what memory held before and makes two runs on the same input write different bytes (STND.STDC.10, REPRO.3). A survey of 323 people who write C found that practice, the behavior of compilers, and the text of the standard do not agree on pointer provenance, uninitialized values, padding, and effective types, and a provenance-aware memory object model has been issued as a technical specification (status unverified) (c1, S11); a provision therefore states what the standard defines, and does not hold an idiom correct because one compiler accepts it (STND.STDC.14). One operating-system kernel builds with the aliasing assumption off, signed overflow treated as wrapping, the removal of null checks off, and automatic variables initialized (c1, S3 and S12, extract). That is a project decision recorded in a build file, which the C reading of STND.CXX.4 states, and STND.STDC.16 keeps the correctness of the code from resting on it, so that the code stays correct on a compiler or at a setting that lacks the option; its second sentence makes that checkable by a test. Unsigned arithmetic wraps by definition; a wraparound that the code intends, in a hash or a generator of random numbers among them, is no defect, and a detector that reports it has the report suppressed at its location with its reason (STND.CODE.4).

Integers. C promotes each integer type narrower than int before arithmetic and converts operands of mixed signedness to an unsigned type, so a narrow unsigned operand is overflowed or shifted as a signed int, a negative value compared with an unsigned one becomes large, and a value stored in a narrower type is truncated with a result that the implementation defines (c1, Integer conversions and promotions). A study of integer overflow found more than 200 distinct locations of overflow in one benchmark suite, with intentional and unintentional, defined and undefined overflow all common, and undefined overflows in about a dozen mature projects (c1, S5, full text). Intentional wraparound therefore exists, and a check of integer arithmetic cannot be a plain report of every overflow (STND.STDC.11, STND.STDC.17). The newest edition adds checked-arithmetic functions, which meet the last alternative of STND.STDC.11 and the second sentence of STND.STDC.18. c1 gives the unsigned size type of the language, or a type shown to hold the values, for sizes, counts, and indexes (practice 9); STND.STDC.18 states the outcome, which the size type meets for the size of an object.

Strings and buffers. A C string is a pointer to bytes ended by a zero, so each operation either trusts the termination or carries a separate size (c1, Strings and buffers). One kernel project has removed a copy function that does not terminate its result and pads the destination, deprecated one that takes no bound, and replaced one that reads the whole source first, so that an unterminated source causes an over-read, with its own that terminates and reports truncation (c1, S21). The optional bounds-checking interfaces of the language were found intrusive to adopt, with error paths that are hard to test and one handler for the whole process, and were not shipped by the common library (c1, S37). STND.STDC.19 to STND.STDC.21 therefore state the outcome, and a length-carrying type, a checked copy, or a function that the project chooses is the means. A function that cannot bound its write fails STND.STDC.19 where its source is unbounded; the function with that property that the language once had was removed from it (c1, S1). STND.STDC.21 is the form for lengths and terminators of STND.CODE.6 and DSGN.2. A format string that comes from data reads and writes through arguments that the call does not pass, and compilers diagnose a mismatch with a literal (STND.STDC.22; c1, S19).

The preprocessor. Macros substitute text before the compiler sees the program, so a macro that evaluates an argument twice repeats its side effect, an unparenthesized parameter or expansion binds to the operators around it, and a branch of conditional compilation that no configuration builds holds code that no check has seen (c1, The preprocessor). The safety coding standards that c1 cites restrict the preprocessor, and later editions moved more of what macros did into the language: constant objects, static assertions, and type inference among them (STND.STDC.23). STND.STDC.24 keeps the hazards of a function-like macro inside its definition; an argument with a side effect stays safe in a macro that evaluates it exactly once, and is reviewed where a macro evaluates it zero times. Generic selection and macros over types are the generic code of C, and the C reading of STND.CXX.12 has each property that they compute and that is decidable during compilation checked then.

Restrict and variable-length arrays. The restrict qualifier is a promise by the author of the code and not a check: where an object reached through a restricted pointer is modified, every access to it in the block goes through that pointer, a violation is undefined, and removing the qualifier from a program that conforms leaves its meaning unchanged, so a build without it is a reference for a test (c1, practice 17; STND.STDC.26). That the copying function of the library with restricted parameters and the moving function without them differ in this way is c1's background note, unverified against the text. The assumption that the qualifier states is one that the compiler relies on, which is why STND.STDC.26 has it stated and checked, as STND.CXX.24 has other assumptions established. Variable-length arrays became a conditional feature after the edition that introduced them, and in the newest edition the variably modified type, a pointer to such an array or a parameter of such a type, is mandatory while the array object with automatic storage is not (c1, S1); one kernel project removed such arrays from its stack, citing worse machine code and a stack that grows past its segment (c1, S21). STND.STDC.27 bounds the automatic object, and STND.STDC.4 tests for it; a parameter of variably modified type carries its extent and meets STND.STDC.7.

Failures. The C library reports failure by a return value, by errno, by the error indicator of a stream, or not at all (c1, Error reporting and ignored returns). The working draft states that errno is zero at startup, that a library function is able to set it to a nonzero value whether or not an error occurred unless its documentation states otherwise, and that no library function sets it to zero (c1, S1, 7.5). STND.STDC.33 follows from those three facts; that each thread has its own errno is unverified in c1. A condition reported in errno alone is lost at the next call that sets errno and escapes the diagnosis of an ignored result that STND.CXX.17 asks, because there is no result to diagnose, which is why STND.STDC.28 has a function of the work return it. A failed write to a stream sets the error indicator of the stream, which stays set until code clears it, so a test of that indicator and of the result of closing the stream, before the output is relied upon, receives each failure of the writes before it; the failure is then not discarded, and STND.STDC.29 is the form of STND.CODE.7 for writes whose results are not tested one by one. Closing a file is able to fail on a full disk (unverified, as the Notes of STND.CXX say), which STND.STDC.31 has the code test.

Ignored results. The rule on detecting and handling the errors of the standard library in the CERT C coding standard rates the omission high in severity and likely, and lists functions whose results it lets code ignore, among them the formatted output functions writing to the standard output, the copying and filling functions of memory, and writes to the standard output and the standard error that a cast to void discards (c1, S16, extract). That list conflicts with STND.CODE.7, which is adopted and binding, and STND.CODE.7 prevails: a failure of a kind that PRIME.4 lists, a failed write of a result among them, is not discarded whatever a coding standard of the work lists, because a coding standard is adopted under a default (STND.CXX.28) and a binding provision is only tightened below it (GOV.19). For a failure that PRIME.4 does not list, each ignored result carries its reason at the call under STND.CODE.12, so an entry of that list is a case for STND.CODE.12 and not an exemption, and a cast to void without a reason meets neither provision. A function whose result reports no failure is outside both provisions. Under STND.STDC.29, a test of a stream before its output is relied upon receives the failure of each formatted write to it, so those writes are not tested one by one. STND.STDC.30 brings the functions of the C library and of other dependencies under the diagnosis of STND.CXX.17; a compiler or an analyzer that knows the library functions meets it without a wrapper.

Signals. A signal handler is allowed to refer to an object of static or thread storage duration only where it is a lock-free atomic object or is assigned as volatile sig_atomic_t, and to call only a short list of library functions; any other use is undefined, and a handler that returns after a signal of a computational exception is undefined (c1, S1, 7.14.1.1, full text). A platform adds a longer list of functions that are safe in a handler, and its reference text says that the standard input and output functions are unsafe because they share buffers and that a handler saves and restores errno (c1, S22 and S23, extract). The object rule is the C reading of STND.CXX.23, and STND.STDC.34 and STND.STDC.35 add the calls, errno, and the return. A static analyzer for C is able to flag an unsafe call in a handler (c1, S32). STND.CONC.17 keeps a library from changing the signal handling of the process.

Concurrency. The edition that added threads defined a memory model and made threads and atomics optional, and a data race is undefined behavior; a program free of races that uses only mutexes and sequentially consistent atomic operations behaves as an interleaving of its threads, and plain operations on atomic objects take the sequentially consistent order (c1, S1, full text). STND.CONC.3 and STND.CONC.4 therefore apply to C as written, and a volatile qualifier is not a protection in their sense. The same model defines a memory location as a scalar object or a maximal sequence of adjacent bit-fields of nonzero width, so two threads that write adjacent bit-fields write one location (c1, S1), which STND.STDC.36 has one protection cover. One platform standard lists the functions of its own threads and of the threads of the C library among those that synchronize memory (c1, S39, extract); whether a mutex of one library works with a condition variable of the other is unverified, and STND.CONC.3 asks that each protection use a facility that the memory model of its library defines as ordering. The threads and atomics of the language are conditional features, which STND.STDC.4 tests. Whether consume ordering is used in practice is unverified, and STND.CONC.4 asks a reason for each ordering weaker than sequential consistency.

Interfaces to other languages. C is the common binary interface of most languages on a platform, so its hazards are those of each foreign interface (c1, Interfaces to other languages). A Fortran caller sees the order of dimensions of an array reversed and indexes from one, and has no unsigned types (c1, S26, extract), which STND.STDC.37 has the contract state. A Python extension holds references with counted ownership, new or borrowed, which is the owner and period of validity that the C reading of STND.CXX.15 states. That no nonlocal jump crosses a frame of another language, and that a callback that C code passes to a foreign runtime lets no jump or termination escape, are c1's practice with a basis that it leaves unverified, so they are not provisions.

Checking. A run-time detector of invalid accesses reports out-of-bounds accesses to the heap, the stack, and globals, uses after release, return, and scope, and double releases, at about twice the run time, and is documented as a tool for finding bugs and not for production (c1, S31, extract). A detector of undefined behavior checks signed overflow, shifts, the bounds of arrays of known size, null, alignment, a variable-length array bound that is not positive, invalid values of enumerations and booleans, and pointer overflow; its checks of unsigned overflow and implicit conversion report defined behavior that is often unintended and are outside its default group (c1, S30, extract). STND.STDC.39 lists the kinds of STND.STDC.8 to STND.STDC.14 and STND.STDC.27 among those of the C reading of STND.CXX.26. One compiler's warning for overflow has done nothing for years and is kept for compatibility (c1, S41), so a silent warning is not evidence; STND.STDC.38 names the diagnostics by what they detect. A compiler's analyzer for C finds double release, use after release, leaks, null dereference, uninitialized values, tainted sizes, and unsafe calls in signal handlers, and its documentation calls it neither sound nor complete (c1, S32), while a deductive verifier proves contracts written in a specification language for C (c1, S33); STND.STDC.40 has each record of a verification say which of the two it is, as STND.CONC.27 does for protocols. Which compiler, detector, or analyzer delivers a check is the choice of the repository configuration (GOV.18).

High assurance. The two coding standards for C that c1 examines are suited to adoption by a decision record under the C reading of STND.CXX.28, because neither requires the corpus to name a revision; the coverage of the edition is the one hazard that differs from C++. In the sources of c1, the published coverage of one of them ends below the newest edition, and that of the other at an older edition (c1, S28, S29, and S40), so the C reading of STND.CXX.30 fixes the edition in force for high-assurance code at one that the adopted standard covers, unless a decision record admits one feature of a later edition. The observation in the Notes of STND.CXX that conformance reduces undefined behavior by a mechanical check, and is not evidence that a result is correct (VV.1), holds for C unchanged, and so do the restrictions of such standards on dynamic memory, recursion, unbounded loops, the preprocessor, and unions.

Floor. STND.STDC.2 applies STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29 to C source, at the cost that they have for C++: a response that PRIME.4 already asks, one attribute per function, one choice of compiler option for a unit that holds a required check, and the naming of the means that checked a claim of conformance. STND.STDC.3 asks an agent for the one decision record that STND.CXX.3 asks. STND.STDC.28 asks one return value per function that reports a listed condition, without which the condition is lost silently, which PRIME.4 forbids. STND.STDC.29 asks one test per stream before its output is relied upon, which STND.CODE.7 already asks in effect, since an untested write discards its failure unless the error indicator is tested. None of them asks for work that PRIME.4, PRIME.2, or GOV.48 does not, so none raises the floor (GOV.11). The custodian's rulings of 2026-10-23 that STND.CXX.3, STND.CXX.16, STND.CXX.17, and STND.CXX.18 raise no floor, and of ratification for STND.CXX.29, concern C++; that their C reading, STND.STDC.28, and STND.STDC.29 raise none is the argument of these Notes and a decision for the custodian (PRIN.10). They bind at every class, CSQ4 included; STND.CXX.29 reaches only high-assurance code, which is never below CSQ1.

Class onset. Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR, REPRO, RSRC, VV, or a provision of HW, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row. Each row of STND.STDC.1 applies from the onset that the Notes of STND.CXX give its provision, so that the C reading moves no rule to another class: STND.CXX.7 from CSQ2, STND.CXX.24 and STND.CXX.27 from CSQ1, STND.CXX.26 from CSQ2, STND.CXX.28 and STND.CXX.30 from CSQ1 to high-assurance code, required for the safety-related components of work of CSQ0, STND.CXX.31 wherever a high-assurance coding standard is adopted, and the other rows from CSQ3. STND.STDC.7 and STND.STDC.37 rest on DSGN.4 and STND.STDC.30 on DSGN.5, and apply from CSQ2, as STND.CXX.6 and STND.CXX.21 do. STND.STDC.40 rests on INTPR.10 and applies from CSQ2, as STND.CONC.27 does. STND.STDC.39 extends the list of the C reading of STND.CXX.26 and takes its onset, CSQ2. STND.STDC.11, STND.STDC.13, STND.STDC.18, STND.STDC.21, STND.STDC.22, and STND.STDC.27 instantiate the checking of preconditions under DSGN.2, which applies from CSQ3, and not the checking of postconditions that STND.CLASS.10 starts at CSQ1. STND.STDC.34 and STND.STDC.36 state what a protocol uses under DSGN.15, and not how its invariants are verified, so they apply from CSQ3. The tests of STND.STDC.16 and STND.STDC.26 are tests under VV.1 that compare with a build of the same code, not with a reference oracle produced without it, so they apply from CSQ3. The other defaults rest on no row and apply from CSQ3. No default raises the floor (GOV.11).

Existing C source conforms to the default provisions when a change next touches it.

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
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
| STND.MPI | Message Passing Interface standard |
| STND.OMP | OpenMP standard |
| VV | Correctness |

## Provisions

### Provisions of STND.CXX

#### STND.STDC.1 C++ defaults applied to C

Default. Instantiates DSGN.1, DSGN.2, DSGN.3, DSGN.4, DSGN.15, DSGN.16, INTPR.1, INTPR.3, REPRO.2, REPRO.3, REPRO.7, REPRO.9, SIMPL.6, RSRC.4, VV.1, HW.5.

The C reading of each provision of STND.CXX that the table of this provision lists SHALL apply to the C source of the work, each sentence with its modal (DSGN.1, DSGN.2, DSGN.3, DSGN.4, DSGN.15, DSGN.16, INTPR.1, INTPR.3, REPRO.2, REPRO.3, REPRO.7, REPRO.9, SIMPL.6, RSRC.4, VV.1, HW.5).

| Provision | Change in its C reading |
| --- | --- |
| STND.CXX.2 | A feature of a later edition is admitted under the predefined macro or the preprocessor test by which each implementation of the toolchain matrix reports that feature, in place of a feature-test macro |
| STND.CXX.4 | None |
| STND.CXX.7 | None |
| STND.CXX.9 | None |
| STND.CXX.12 | None |
| STND.CXX.15 | The comment states the owner and the period of validity of each pointer, and each error value by which the declaration reports failure |
| STND.CXX.23 | The type of an object that a signal handler shares is volatile sig_atomic_t |
| STND.CXX.24 | The markers of an assumption are the unreachable marker of the edition in force and the builtins of a compiler |
| STND.CXX.25 | The checks are the warnings of each compiler of the toolchain matrix at a recorded set, without the checks of the Core Guidelines and of the names of STND.CXX.14 |
| STND.CXX.26 | None |
| STND.CXX.27 | None |
| STND.CXX.28 | The coding standard is one written for C |
| STND.CXX.30 | None |
| STND.CXX.31 | None |

#### STND.STDC.2 Binding C++ provisions applied to C

Binding. Instantiates PRIME.4, PRIME.2.

The C reading of each provision of STND.CXX that the table of this provision lists SHALL apply to the C source of the work, each sentence with its modal (PRIME.4, PRIME.2).

| Provision | Change in its C reading |
| --- | --- |
| STND.CXX.16 | The responses are those of the provision other than a C++ exception |
| STND.CXX.17 | None |
| STND.CXX.18 | None |
| STND.CXX.29 | None |

#### STND.STDC.3 Agent C edition changes

Binding. Instantiates GOV.48, DSGN.3.

An agent SHALL meet the C reading of STND.CXX.3 for each translation unit of C source (GOV.48, DSGN.3).

### Language level

#### STND.STDC.4 Conditional features tested

Default. Instantiates DSGN.3, SIMPL.6.

Each translation unit of C source that uses a conditional feature SHOULD hold a preprocessor test that stops its compilation with a diagnostic on an implementation that reports that feature absent (DSGN.3, SIMPL.6).

### Ownership and lifetime

#### STND.STDC.5 Release on every path

Default. Instantiates DSGN.14.

Each owned resource that a function acquires, and does not pass to its caller or to another owner, SHOULD be released on every path out of that function, failure paths included (DSGN.14). Where a function holds more than one owned resource, it SHOULD release them through one sequence of release operations, written once in the function, that each path out of the function enters at the point that matches the resources it holds (DSGN.14).

#### STND.STDC.6 Release functions named

Default. Instantiates DSGN.1.

In addition to what the C reading of STND.CXX.15 asks, the documentation comment of each declaration that returns or keeps an owned resource SHOULD name the function by which the owner of that resource releases it (DSGN.1).

#### STND.STDC.7 Extents passed with pointers

Default. Instantiates DSGN.4.

Other than at an interface whose form a dependency or a published interface of the work fixes, each pointer to a sequence of objects that crosses an interface of the work SHOULD travel with the extent of that sequence, in one structure with it or in a parameter that the contract of the interface pairs with it (DSGN.4).

#### STND.STDC.8 Accesses within their object

Default. Instantiates DSGN.1, SIMPL.11.

Each array subscript, and each result of pointer arithmetic, SHOULD lie within the array object into which its pointer points, or one past its last element for a result that code does not dereference (DSGN.1). Each such access SHOULD be shown to lie there by a check that precedes it, or by a bounds invariant that a comment at the access states (DSGN.1, SIMPL.11).

#### STND.STDC.9 Objects used within their lifetime

Default. Instantiates DSGN.14.

Code SHOULD NOT access an object through a pointer after the lifetime of that object has ended (DSGN.14). Where the pointer through which the owner of an allocation releases it outlives the release, the owner SHOULD set that pointer to a null pointer at the release (DSGN.14).

#### STND.STDC.10 Initialization before reads

Default. Instantiates DSGN.1, REPRO.3.

Each object SHOULD be initialized or assigned before code reads its value (DSGN.1). Before the bytes of an object of structure or union type leave the process, by a write to a file, to a socket, or to a buffer that another component reads, each padding byte of that object SHOULD be set (REPRO.3).

### Undefined behavior

#### STND.STDC.11 Signed overflow excluded

Default. Instantiates DSGN.1, DSGN.2.

Each arithmetic operation on signed integers SHOULD be shown not to overflow, by a check of its operands that precedes it, by a range argument that a comment at the operation states, or by its replacement with a checked operation that reports overflow (DSGN.1, DSGN.2).

#### STND.STDC.12 Division and shift operands

Default. Instantiates DSGN.1.

Each integer division and remainder SHOULD have a divisor shown to be nonzero and, for signed operands, a dividend and a divisor shown not to be the most negative value of their type and minus one together (DSGN.1). Each shift SHOULD have a count shown to be at least zero and less than the width of its promoted left operand, and a left operand of unsigned type or a nonnegative value whose shifted result its type represents (DSGN.1).

#### STND.STDC.13 Guards free of undefined behavior

Default. Instantiates DSGN.2.

Each check that guards an operation against undefined behavior SHOULD precede that operation on every path that reaches it (DSGN.2). Each such check SHOULD be written without an operation whose behavior is undefined for the values against which it guards, the formation of a pointer outside its object included (DSGN.2).

#### STND.STDC.14 Access through compatible types

Default. Instantiates DSGN.1.

Code SHOULD access the stored value of each object only through an lvalue of a type that the edition in force admits for the effective type of that object, or through an lvalue of a character type (DSGN.1). Code SHOULD reinterpret the representation of an object only through a copy of its bytes, or through a member of a union as the edition in force defines that access (DSGN.1).

#### STND.STDC.15 Sequenced accesses to scalars

Default. Instantiates DSGN.1.

Where at least one of two accesses to one scalar object modifies that object, code SHOULD order the two by a sequencing relation that the edition in force defines (DSGN.1).

#### STND.STDC.16 Settings that define undefined behavior

Default. Instantiates DSGN.1, VV.1.

Where a compiler option defines, for a translation unit, a behavior that the ISO C standard leaves undefined, the argument for the correctness of the code SHOULD NOT rely on that option (DSGN.1). Where the work builds code under such an option, the tests of that code SHOULD also pass in a build of it without that option (VV.1).

### Integers

#### STND.STDC.17 Value-changing conversions made explicit

Default. Instantiates DSGN.1.

Each conversion of an integer value to an integer type that does not represent every value of its source type SHOULD be an explicit conversion, preceded by a check or accompanied by a range argument that shows the value representable in the target type (DSGN.1). The two operands of each relational and equality comparison of integers SHOULD have the same signedness before the usual arithmetic conversions (DSGN.1).

#### STND.STDC.18 Types of sizes and counts

Default. Instantiates DSGN.1, DSGN.2.

Each object that holds a size, a count, or an index SHOULD have a type that represents each value that the object takes in the regime of use (DSGN.1). Each size that code computes for an allocation SHOULD be checked for overflow before the allocation, or computed by an operation that reports overflow (DSGN.2).

### Strings and buffers

#### STND.STDC.19 Bounded buffer writes

Default. Instantiates DSGN.1.

Each write into a buffer SHOULD be bounded by the size of that buffer, by the operation that writes or by a check of its source that precedes the write (DSGN.1). Each operation that writes a string into a buffer SHOULD leave that string terminated within the buffer (DSGN.1).

#### STND.STDC.20 Truncation reported or intended

Default. Instantiates DSGN.1, REPRO.7.

Each truncation of a string or of other data to the size of its destination SHOULD be reported to the caller as a failure, or carry at its location a statement that the truncation is intended (DSGN.1, REPRO.7).

#### STND.STDC.21 Lengths from untrusted input

Default. Instantiates DSGN.2.

Each length, count, or offset that arrives in untrusted input SHOULD be checked against the extent of the object that it describes before code reads or writes through it (DSGN.2). Each read of a string from untrusted input SHOULD be bounded by the extent of its buffer, independently of a terminator that the input supplies (DSGN.2).

#### STND.STDC.22 Checked format strings

Default. Instantiates DSGN.2, DSGN.3.

The format string of each call to a formatted input or output function SHOULD be a string literal, or a string that the code checks against the number and the types of the arguments of that call before the call (DSGN.2). The static checks of the work SHOULD diagnose each call whose literal format string does not match its arguments (DSGN.3).

### Preprocessor

#### STND.STDC.23 Language facilities over macros

Default. Instantiates INTPR.1, DSGN.3.

Where a constant object, an enumeration constant, an inline function, or a static assertion of the edition in force provides what a macro provides, code SHOULD use that facility in place of the macro (INTPR.1, DSGN.3).

#### STND.STDC.24 Function-like macro hygiene

Default. Instantiates DSGN.1.

Each function-like macro SHOULD evaluate each of its arguments at most once (DSGN.1). Each function-like macro whose expansion is an expression SHOULD enclose each use of a parameter, and the whole expansion, in parentheses (DSGN.1).

#### STND.STDC.25 Conditional compilation under check

Default. Instantiates DSGN.3, VV.8.

Other than a branch for a target that the repository configuration records as unchecked, each branch of conditional compilation in C source SHOULD be compiled by at least one configuration that the checks of each change build (DSGN.3, VV.8).

### Qualifiers and arrays

#### STND.STDC.26 Restrict-qualified pointers

Default. Instantiates DSGN.1, VV.1.

Each pointer that code declares with the restrict qualifier SHOULD have, in the contract of the function of which it is a parameter or in a comment at its declaration, a statement of the objects that code reaches through it and through no other pointer during its block (DSGN.1). Each such statement SHOULD be checked by a check at the entry of the function, or by tests that compare the results of the code with its results in a build without the qualifier (VV.1).

#### STND.STDC.27 Bounded variable-length arrays

Default. Instantiates DSGN.2, RSRC.1.

Each object of variable-length array type with automatic storage duration SHOULD have a number of elements that a check preceding its declaration bounds by a limit that its component states (DSGN.2, RSRC.1).

### Failures

#### STND.STDC.28 Listed failures beyond errno

Binding. Instantiates PRIME.4.

A function of the work SHALL NOT report a condition that PRIME.4 lists through errno alone (PRIME.4).

#### STND.STDC.29 Stream errors before reliance

Binding. Instantiates PRIME.4.

Before a result that code writes to a stream without testing the result of each write is reported or relied upon, the code SHALL test the error indicator of that stream and the result of the call that closes or flushes it (PRIME.4).

#### STND.STDC.30 Library failure results diagnosed

Default. Instantiates DSGN.5.

Each function of the C library or of another dependency that reports in its result a failure of a kind that PRIME.4 lists SHOULD be called through a declaration, its own or that of a function of the work that wraps it, under which the compiler or a static check diagnoses each call that ignores that result (DSGN.5).

#### STND.STDC.31 Release failures tested

Default. Instantiates DSGN.1.

Before a result is relied upon, each failure that the release of an owned resource reports, and that affects that result, SHOULD be tested and answered as the C reading of STND.CXX.16 provides (DSGN.1).

#### STND.STDC.32 C failure channel

Default. Instantiates DSGN.1, DSGN.14.

Each failure that the caller of a function is designed to handle SHOULD be reported by the return value of that function, or by an object that its contract names as its result for failures (DSGN.1). A nonlocal jump SHOULD NOT leave a function that holds an owned resource that it has not released (DSGN.14).

#### STND.STDC.33 Errno as a report of failure

Default. Instantiates DSGN.1.

Code SHOULD set errno to zero before each call of a library function that reports failure only through errno, and read errno for that call before another call that is able to change it (DSGN.1). Where a function reports failure in its result as well as through errno, code SHOULD read errno for a call of it only after that result indicates failure (DSGN.1).

### Signals and threads

#### STND.STDC.34 Signal handler calls

Default. Instantiates DSGN.15, DSGN.14.

A signal handler SHOULD call only signal-safe functions (DSGN.15). A signal handler that calls a function able to change errno SHOULD restore, on each return, the value that errno held at its entry (DSGN.14).

#### STND.STDC.35 Computational exception signals

Default. Instantiates DSGN.1.

A handler of a signal that reports a computational exception, an invalid instruction, or an invalid access to memory SHOULD NOT return to the code that the signal interrupted (DSGN.1).

#### STND.STDC.36 Adjacent bit-fields shared

Default. Instantiates DSGN.15.

Where concurrent tasks write bit-fields of one structure, the protection that STND.CONC.3 asks SHOULD cover each maximal sequence of adjacent bit-fields of nonzero width as one shared mutable object (DSGN.15).

### Interfaces to other languages

#### STND.STDC.37 Data crossing to other languages

Default. Instantiates DSGN.4.

Each type of data that crosses an interface between C source and code in another language SHOULD have a width and a layout that the contract of the interface fixes (DSGN.4). Each array of more than one dimension that crosses such an interface SHOULD have the order of its dimensions and the origin of its indexes stated in that contract (DSGN.4).

### Checking

#### STND.STDC.38 C compiler warning coverage

Default. Instantiates DSGN.3.

Where a compiler of the toolchain matrix offers a diagnostic of a read of an object before its initialization, of a format string that does not match its arguments, of an ignored result of a function so declared, of a comparison of signed and unsigned operands, or of an implicit conversion that changes a value, the recorded set of warnings of the C reading of STND.CXX.25 SHOULD include that diagnostic (DSGN.3).

#### STND.STDC.39 Undefined behavior under detection

Default. Instantiates DSGN.3.

The kinds of undefined behavior that the repository configuration lists under the C reading of STND.CXX.26 SHOULD include each kind that STND.STDC.8, STND.STDC.9, STND.STDC.10, STND.STDC.11, STND.STDC.12, STND.STDC.14, or STND.STDC.27 governs and that a detector among the means of the work detects at run time (DSGN.3).

#### STND.STDC.40 Stated limits of analysis

Default. Instantiates VV.1, INTPR.10.

The record of each verification that finds C code free of a kind of undefined behavior SHOULD state its means, and whether the documentation of that means states it as sound for that kind (VV.1, INTPR.10).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
