# C standard (STND.STDC) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 125 (2026-10-24). This reading copy is composed from the per-provision files in STND/STDC/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the coding practice that is specific to C. It adds to STND.CODE, STND.DOCS, and STND.CONC only what the language makes necessary. It applies to C source each provision of STND.CXX whose outcome holds for C, in a C reading that its Terms define, in place of restating it (STND.STDC.1 and STND.STDC.2), records each lowering of the edition of a translation unit (STND.STDC.3), and asks a test of each conditional feature that a unit uses (STND.STDC.4). It states how code without destructors releases what it owns, passes sequences with their extent, and keeps each access within its object and the lifetime of that object (STND.STDC.5 to STND.STDC.10). It excludes the classes of undefined behavior that optimizers exploit and keeps the correctness of code independent of options that define them (STND.STDC.11 to STND.STDC.16), and covers integer conversions and the types of sizes (STND.STDC.17 and STND.STDC.18), strings and buffers (STND.STDC.19 to STND.STDC.22), the preprocessor (STND.STDC.23, STND.STDC.24, and STND.STDC.25), restrict-qualified pointers and variable-length arrays (STND.STDC.26 and STND.STDC.27), failures, errno, and ignored results (STND.STDC.28 to STND.STDC.32), signal handlers and bit-fields shared between threads (STND.STDC.33, STND.STDC.34, and STND.STDC.35), data that crosses to other languages (STND.STDC.36), and the checks of C code (STND.STDC.37 and STND.STDC.38). Through STND.STDC.1 and STND.STDC.2, the high-assurance provisions of STND.CXX apply to C: conformance to the high-assurance coding standard that a decision record of the work adopts, claims of conformance limited to what was checked, an edition that the standard covers and the toolchain is validated for, and recorded deviations.

STND.STDC.2 instantiates PRIME.4 and PRIME.2, and STND.STDC.28 instantiates PRIME.4; these two are binding at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is compiler, edition, platform, and tool agnostic: its provisions name the constructs of C and no edition, compiler, library to depend on, platform, or tool, and the repository configuration or a project instrument chooses them (GOV.18). It sets no edition for C; the repository configuration states the edition of each translation unit. The build matter that it holds is that of two applied provisions, the C reading of STND.CXX.4, which states the edition, disables extensions, and states the options that change what a unit means, and the C reading of STND.CXX.25, which records a set of compiler warnings and fails a change on each; the second sentence of STND.STDC.16 adds a test in a checking build of STND.BUILD.13. The rules of concurrency that hold for every language are in STND.CONC, which applies to C by its own scope and which this standard cites and does not restate.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration and Static check have the meanings that STND.CODE gives them. Translation unit, Toolchain matrix, and Owned resource have the meanings that STND.CXX gives them, and Edition in force the meaning that STND.CXX gives it in its C reading. Concurrent task, Shared mutable object, and Protection have the meanings that STND.CONC gives them; a signal handler is a concurrent task. Checking build has the meaning that STND.BUILD gives it.

| Term | Definition |
| --- | --- |
| C source | Source of the work in C: each file that a compiler of the work translates as C, and each header that such a file includes, other than a header of the implementation or of a dependency, and other than external code that the work incorporates and keeps apart as STND.DEPS.11 recommends. A header that C and C++ translation units both include is C source and C++ source. |
| Foreign interface | Of C source: an interface through which C source calls, or is called by, code written in another language; a callback or a thread that a runtime of another language starts in C source; or a structured block of a compiler directive for parallel execution. |
| C reading | Of a provision or a term of STND.CXX, at the revision of STND.CXX in force: that provision or term applied to C source, with C, the ISO C standard, the C standard library, and an implementation of the C standard library in place of C++, the ISO C++ standard, the C++ standard library, and a standard library implementation; with each term that this standard defines in place of the term of STND.CXX of the same name; with each other term of STND.CXX, and each provision of STND.CXX that it cites, taken in the same reading; and with the change that the row of that provision in the table of STND.STDC.1 or STND.STDC.2 gives. |
| Conditional feature | A feature of an edition of the ISO C standard that the edition lets an implementation omit, and whose presence or absence the implementation reports by a predefined macro that the edition names. |
| Undefined behavior | Behavior for which the ISO C standard, at the edition in force, imposes no requirements. |
| Signal-safe function | A function that the ISO C standard, or the documentation of the platform on which the code runs, states as one that a signal handler is able to call. |
| Untrusted input | Data that reaches the work from outside its own code, other than data from a source that the threat model of the project records as trusted. |

## Notes

The standard is agnostic of compiler, edition, platform, implementation, and tool, states practice that has held across the editions of C, and cites the provision that holds an outcome in place of restating it (GOV.31). It is modeled on STND.CXX, in the form of STND.PY and STND.JL. Each provision states the outcome that a tool or a reviewer decides from the source, the repository configuration, and the record of checks, and names the constructs of C, which GOV.18 admits at LVL2; the Notes name a compiler, a library function, or a coding standard only to show a hazard that a provision guards against. The source is the project's research note research/c-notes/c1-c-language.md (cited as c1). A fact that c1 does not support is marked unverified.

C reading. STND.CXX holds practice specific to C++, and much of it holds for C, because the two languages share a model of compilation, the kinds of their undefined behavior, and the failures at the boundary of a library. STND.STDC.1 and STND.STDC.2 apply those provisions to C source in their C reading, so that each keeps one text and its mode, and this standard holds only what C adds (GOV.31). Each row of STND.STDC.1 carries the class from which it applies, which is the onset that the Notes of STND.CXX give its provision, and a project replaces one row by a recorded decision without replacing the others. The reading follows the revision of STND.CXX in force, as its Term states; where a provision of STND.CXX cites STND.CONC, the cited provision applies to C by the scope of STND.CONC. A header that C and C++ units both include meets both readings when it keeps to the part of the two languages that they share; the linkage of a constant object and of an inline function differs between them (c1 does not discuss it; unverified).

Provisions of STND.CXX that apply to C. STND.CXX.4 states the edition, disables extensions, and states the options that change what a unit means. The default dialect of one compiler enables its extensions, even where they change the meaning of the base standard (c1, practice 1, S2), which the second sentence of STND.CXX.4 disables, with the term Foreign interface defined for C. The row of STND.CXX.4 adds the options that define a behavior that the language leaves undefined, which the third sentence of STND.CXX.4 does not name; STND.BUILD.11 also states each setting that is able to change a result, for every language. A compiler's name for the newest edition has changed between its releases, and its default is a dialect and not an edition (c1, Editions), which is why the edition that the repository configuration states is one of the ISO C standard. STND.CXX.7 holds for C with its row: a register is reached through a volatile-qualified object (c1, What the corpus already holds), and the layer that holds its address is where CPS.5 puts its limit check; a type alias in C names the same type as the type it aliases, so a distinct type for a pointer into device memory is a pointer to a distinct type or a structure that wraps the pointer. STND.CXX.9 holds for C because results of the C library also depend on behavior that the ISO C standard leaves to the implementation; c1 lists STND.CXX.8 to STND.CXX.10 as not carrying and does not discuss the C library, and the examples of such behavior, the sequence of its pseudo-random generator, the order of equal elements after its sort, and the accuracy of its mathematical functions, are unverified. STND.CXX.12 is checked in C by static assertions; c1 lists it among the provisions on templates that do not carry and, in its section on the preprocessor, as one that does, and its text names no C++ facility. STND.CXX.15 gives the ownership contract that C needs most (c1, What the corpus already holds), and STND.STDC.6 adds the function that releases what a declaration returns, since C has no destructor that names it. STND.CXX.16 keeps every response but a C++ exception, and its row states that a report through errno alone is not a return of the condition in the result. STND.CXX.17 is met by the attribute that an edition provides for a result that is not to be discarded, or by a compiler's equivalent attribute and its warning (c1, Error reporting and ignored returns). STND.CXX.18 holds for C as written: an assertion is removed by defining NDEBUG, and a test for non-finite values by an option that lets the compiler assume finite values. STND.CXX.23 gives the C type for an object that a signal handler shares, beside a lock-free atomic object. STND.CXX.24 covers the unreachable marker of an edition that has one, and the builtins of a compiler. STND.CXX.25, STND.CXX.26, and STND.CXX.27 give the warnings, the run-time detection that fails at its first detection, and the library checks in production, the last for a C library that offers checks of the buffers that its functions write; STND.BUILD.12 holds the failing warning for every language. STND.CXX.28, STND.CXX.29, STND.CXX.30, and STND.CXX.31 apply nearly as written, because they refer to the high-assurance coding standard that a decision record adopts, and that term reads "for C" in its C reading.

Provisions of STND.CXX that do not apply to C. STND.CXX.1 names the Core Guidelines, which concern C++. STND.CXX.2 takes the custodian's direction for the latest edition of C++, which concerns C++, so this standard sets no edition for C; the repository configuration states one under the C reading of STND.CXX.4, and STND.DEPS.4 reviews it with the pinned revisions. STND.CXX.3 forbids an agent to lower the edition below the one that STND.CXX.2 gives; STND.STDC.3 asks the record of a lowering for C, a default. STND.CXX.5 and STND.CXX.20 rest on destructors and resource handles, which C lacks, and STND.STDC.5 states their outcome for C. STND.CXX.6 rests on view types, which C lacks, so STND.STDC.7 has a pointer travel with its extent and STND.STDC.8 keeps each access within its object. STND.CXX.8 compares the C++ standard library with other facilities by reasons specific to C++, and STND.CXX.10 holds the custodian's preference for C++ libraries delivered as headers. STND.CXX.11 and STND.CXX.13 concern templates and metaprogramming. The naming table of STND.CXX.14 is the custodian's convention for C++, and names in C follow STND.DOCS.12 and the layout tool of STND.CODE.5. STND.CXX.19 asks whether C++ exceptions are enabled, and STND.STDC.31 states the channel of failure for C. STND.CXX.21 holds its outcomes through a resource handle and a destructor; STND.STDC.29 and STND.STDC.30 state them for C. STND.CXX.22 binds the C++ side of a boundary; c1 leaves unverified that the ISO C standard defines a nonlocal jump only within C frames, so no provision binds the C side, and STND.OMP.21 keeps such a jump out of a structured block of OpenMP.

What the corpus already holds. STND.CODE.3 asks for the contract at each declaration, STND.CODE.4 for the static checks and a suppression at the location of each finding left in place, STND.CODE.5 for a layout tool, STND.CODE.6 and STND.CODE.7 for checks of untrusted input that no setting removes and for no discarded failure of a kind that PRIME.4 lists, STND.CODE.11 for no code disabled in comments, a block under a condition that is always false among them, STND.CODE.12 for the reason of each other discard, and STND.CODE.13 for statements grouped by step. STND.CONC applies to C by its own scope: a thread of the C library or of the platform, and a signal handler, is a concurrent task, and the protection of each shared mutable object (STND.CONC.3), the sequentially consistent order of atomic operations or a stated reason for a weaker one (STND.CONC.4), publication and lifetimes (STND.CONC.5), concurrent calls in contracts (STND.CONC.6), lock order and conduct (STND.CONC.7 and STND.CONC.8, the release of a lock on every path among them), the parent that joins the threads it starts (STND.CONC.12), a library that leaves signal handling unchanged (STND.CONC.17), a child process of a threaded program (STND.CONC.19), and race detection in tests (STND.CONC.25) apply unchanged. STND.DEPS.8 records the revision of each compiler with each result, STND.DEPS.9 lists each analyzer, and STND.DEPS.11 keeps a library that a C project copies into its tree apart, which is why the term C source leaves it out. STND.DOCS.13 runs the examples of documentation comments. NUMER.16 and NUMER.17 govern an option that relaxes floating-point semantics or contracts multiply and add on the path of a numerical result, NUMER.5 and NUMER.16 a narrowing of a floating-point value, HW.5 the delivered arithmetic, and HW.CPU.3 the confirmation of the floating-point control state and its restoration where code changes it, which C does through the functions of its floating-point environment; whether such code also needs the pragma by which C lets a unit access that environment is not in c1 and is unverified.

Ownership without destructors. C has no destructor, so an owned resource is released by code that each path out of a function reaches (c1, Resource management without destructors). One kernel coding style gives the reasons for one exit region per function, reached by jumps to labels that release in reverse order: the code is easier to follow, nesting is reduced, and a change cannot update one exit point and miss another (c1, S15). A wrapper that owns the release, and takes a callback or a table of acquired items, is the other form that STND.STDC.5 admits. Some compilers offer a cleanup attribute on a variable as an extension, and a deferred-release facility was on the agenda of the committee of the language (unverified); neither is part of a published edition. The result of a reallocation assigned to the only pointer to the original block loses that block when the reallocation fails, which is a path on which the block is not released (STND.STDC.5). A size computed as a count times the size of an element wraps (STND.STDC.18; c1, S21). A pointer set to null at the release lets a later check of it find that its object is gone (STND.STDC.9; c1, hazard table). An allocation whose result code uses without a test discards a failure that PRIME.4 lists, which STND.CODE.7 forbids.

Undefined behavior. The overview annex of the working draft of the newest edition lists 221 circumstances of undefined behavior (c1, S1; the count was not compared with the published text and is unverified for it). A compiler is allowed to assume that none of them occurs, and an optimizer removes code that is correct only if one does: a test that x + 1 exceeds x becomes true, and a dereference ahead of a test for null lets the test go (c1, S4). A crash is not a guaranteed symptom. A check that relies on the undefined operation itself is the common casualty: a test of a pointer plus a length against the pointer, written to detect wraparound, is removed (c1, S6) (STND.STDC.13); the same study found 160 bugs of code that an optimizer is able to discard, which the projects confirmed and fixed, and estimated that such code exists in 40 percent of 8,575 packages of one distribution that contain C or C++. STND.STDC.8 to STND.STDC.15 cover the classes that c1 finds behind most defects. Two's complement became the only representation of signed integers in the newest edition, and signed overflow stayed undefined (c1, hazard table). A read of an uninitialized automatic object that could have been declared register is undefined, and another such read gives an unspecified value or a trap representation, and compilers treat both as license (c1, hazard table); an option that initializes automatic storage is a defense, and STND.STDC.10 still asks the initialization. The padding of a structure written out of the process discloses what memory held before and makes two runs on the same input write different bytes (STND.STDC.10, REPRO.3). A survey of 323 people who write C found that practice, the behavior of compilers, and the text of the standard do not agree on pointer provenance, uninitialized values, padding, and effective types (c1, S11), so STND.STDC.14 states what the standard defines. One operating-system kernel builds with the aliasing assumption off, signed overflow treated as wrapping, the removal of null checks off, and automatic variables initialized (c1, S3 and S12). The C reading of STND.CXX.4 states such an option, and STND.STDC.16 keeps the correctness of the code from resting on it, so that the code stays correct on a compiler or at a setting that lacks the option; its second sentence makes that checkable in a checking build of STND.BUILD.13 without the option, whose record states that it lacks it; the build that detects undefined behavior under the C reading of STND.CXX.26 serves, since its detector reports what the option hides. Unsigned arithmetic wraps by definition; a wraparound that the code intends, in a hash or a generator of random numbers among them, is no defect, and a detector that reports it has the report suppressed at its location with its reason (STND.CODE.4).

Showing an operation safe. STND.STDC.8 and STND.STDC.11 admit a check before the operation, a static check that proves the range, a comment that states the argument, and, for arithmetic, a checked operation. c1 asks a range for the operands that come from outside the function (practice 2), which STND.STDC.11 follows; an operand that the function computes inside itself is covered by the argument for that computation. An index from untrusted input is checked where the input enters, as the binding STND.CODE.6 requires, so a comment is no substitute there. The newest edition adds checked-arithmetic functions, which meet the last alternative of STND.STDC.11 and the second sentence of STND.STDC.18.

Integers. C promotes each integer type narrower than int before arithmetic and converts operands of mixed signedness to an unsigned type, so a narrow unsigned operand is overflowed or shifted as a signed int, a negative value compared with an unsigned one becomes large, and a value stored in a narrower type is truncated with a result that the implementation defines (c1, Integer conversions and promotions). STND.STDC.12 therefore judges the left operand of a shift by its type after the promotions. A study found intentional and unintentional, defined and undefined overflow all common, and undefined overflows in about a dozen mature projects (c1, S5), so a check of integer arithmetic is not a plain report of every overflow.

Strings and buffers. A C string is a pointer to bytes ended by a zero, so each operation either trusts the termination or carries a separate size (c1, Strings and buffers). One kernel project has removed or replaced the copy functions that fail to terminate, take no bound, or read past an unterminated source, and the optional bounds-checking interfaces of the language were found intrusive to adopt and were not shipped by the common library (c1, S21 and S37). STND.STDC.19 to STND.STDC.21 state the outcome, and a length-carrying type, a checked copy, or a function that the project chooses is the means. The function that the language once had and that cannot bound its write was removed from it (c1, S1). STND.STDC.20 concerns strings and sequences of bytes; a narrowing of a numerical value is an approximation that NUMER governs. A format string that comes from data reads and writes through arguments that the call does not pass, and compilers diagnose a mismatch with a literal (STND.STDC.22; c1, S19).

The preprocessor. Macros substitute text before the compiler sees the program, so a macro that evaluates an argument twice repeats its side effect, an unparenthesized parameter or expansion binds to the operators around it, and a branch of conditional compilation that no configuration builds holds code that no check has seen (c1, The preprocessor). The safety coding standards that c1 cites restrict the preprocessor, and later editions moved more of what macros did into the language: constant objects, static assertions, and type inference among them (STND.STDC.23). STND.STDC.24 keeps the hazards of a function-like macro inside its definition; an argument with a side effect stays safe in a macro that evaluates it exactly once. A result computed on a branch that STND.STDC.25 records as unchecked has no evidence from the checks of the change (PRIME.3). Generic selection and macros over types are the generic code of C, and the C reading of STND.CXX.12 has each property that they compute and that is decidable during compilation checked then.

Restrict and variable-length arrays. The restrict qualifier is a promise by the author of the code: where an object reached through a restricted pointer is modified, every access to it in the block goes through that pointer, a violation is undefined, and removing the qualifier from a program that conforms leaves its meaning unchanged, so a build without it is a reference for a test (c1, practice 17; STND.STDC.26). The comparison agrees within the tolerance of the acceptance criterion, because a build without the qualifier is able to order floating-point operations differently; a bitwise criterion applies only where the acceptance criterion asks it (STND.VVUQ.82), and NUMER.11 gives the basis of a tolerance on a numerical result. That the copying function of the library with restricted parameters and the moving function without them differ in this way is c1's background note, unverified against the text. Variable-length arrays became a conditional feature after the edition that introduced them, and in the newest edition the variably modified type is mandatory while the array object with automatic storage is not (c1, S1); one kernel project removed such arrays from its stack, citing worse machine code and a stack that grows past its segment (c1, S21). STND.STDC.27 bounds the automatic object, and STND.STDC.4 tests for it.

Failures and PRIME.4. PRIME.4 lists invalid input, detected precondition violations, non-convergence, and resource exhaustion, and its last sentence excludes silent continuation past an error. The C library reports failure by a return value, by errno, by the error indicator of a stream, or not at all (c1, Error reporting and ignored returns). The working draft states that errno is zero at startup, that a library function is able to set it to a nonzero value whether or not an error occurred unless its documentation states otherwise, and that no library function sets it to zero (c1, S1, 7.5), from which STND.STDC.32 follows; that each thread has its own errno is unverified. A condition reported in errno alone is lost at the next call that sets errno and escapes the diagnosis that STND.CXX.17 asks, because there is no result to diagnose, which the row of STND.CXX.16 in STND.STDC.2 states.

Streams. A failed write to a stream sets the error indicator of the stream, which stays set until code clears it, and closing or flushing a stream writes its buffered data and reports a failure of that write (both unverified; c1 does not state them). On those two facts, a test of the indicator before the stream is closed, and a test of the result of the flush or the close, receive each failure of the writes before them, which STND.STDC.28 asks before the output is relied upon. A full volume is resource exhaustion, which PRIME.4 lists; another error of output is not in its list, and a program that reports a result whose writes failed continues silently past an error, which the last sentence of PRIME.4 excludes. STND.STDC.28 rests on that sentence, at the cost of two tests per stream. Under it, the formatted writes to a tested stream are not tested one by one, and STND.STDC.29 has each such call carry the suppression of STND.CODE.4, which a warning of the C reading of STND.CXX.25 then accepts; a call whose failure an error handler that ends the run receives, as STND.MPI.5 admits, carries the same suppression.

Ignored results. The rule on detecting and handling the errors of the standard library in the CERT C coding standard rates the omission high in severity and likely, and lists functions whose results it lets code ignore, among them the formatted output functions writing to the standard output, the copying and filling functions of memory, and writes to the standard output and the standard error that a cast to void discards (c1, S16). That list conflicts with STND.CODE.7, which is adopted and binding, and STND.CODE.7 prevails for each failure of a kind that PRIME.4 lists, because a coding standard is adopted under a default (STND.CXX.28) and a binding provision is only tightened below it (GOV.19). For a failure that PRIME.4 does not list, each ignored result carries its reason at the call under STND.CODE.12, so an entry of that list is a case for STND.CODE.12 and not an exemption, and a cast to void without a reason meets neither. A function whose result reports no failure is outside both. STND.STDC.29 brings the functions of the C library and of other dependencies under the diagnosis of STND.CXX.17; a compiler or an analyzer that knows the library functions meets it without a wrapper. STND.STDC.30 has each release failure that affects a result tested; the closing of a stream is governed by STND.STDC.28.

Signals. A signal handler is allowed to refer to an object of static or thread storage duration only where it is a lock-free atomic object or is assigned as volatile sig_atomic_t, and to call only a short list of library functions; any other use is undefined, and a handler that returns after a signal of a computational exception is undefined (c1, S1, 7.14.1.1). A platform adds a longer list of functions that are safe in a handler, and its reference text says that the standard input and output functions are unsafe because they share buffers and that a handler saves and restores errno (c1, S22 and S23). The object rule is the C reading of STND.CXX.23, whose condition, no facility of the target that orders the accesses, also reaches an interrupt handler of a constrained target; STND.STDC.33 and STND.STDC.34 add the calls, errno, and the return. STND.CONC.17 keeps a library from changing the signal handling of the process.

Concurrency. The edition that added threads defined a memory model and made threads and atomics optional, and a data race is undefined behavior; a program free of races that uses only mutexes and sequentially consistent atomic operations behaves as an interleaving of its threads, and plain operations on atomic objects take the sequentially consistent order (c1, S1). STND.CONC.3 and STND.CONC.4 apply to C as written, and a volatile qualifier is not a protection in their sense. The same model defines a memory location as a scalar object or a maximal sequence of adjacent bit-fields of nonzero width, so a task that reads one bit-field while another writes its neighbor accesses one location (c1, S1), which STND.STDC.35 has one protection cover; HW.11 verifies the protocol under that model. One platform standard lists the functions of its own threads and of the threads of the C library among those that synchronize memory (c1, S39); whether a mutex of one library works with a condition variable of the other is unverified, and STND.CONC.3 asks that each protection use a facility that the memory model of its library defines as ordering. Whether consume ordering is used in practice is unverified, and STND.CONC.4 asks a reason for each ordering weaker than sequential consistency.

Interfaces to other languages. C is the common binary interface of most languages on a platform, so its hazards are those of each foreign interface (c1, Interfaces to other languages). A Fortran caller sees the order of dimensions of an array reversed and indexes from one, and has no unsigned types (c1, S26), which STND.STDC.36 has the contract state. A Python extension holds references with counted ownership, new or borrowed, which is the owner and period of validity that the C reading of STND.CXX.15 states. That no nonlocal jump crosses a frame of another language, and that a callback that C code passes to a foreign runtime lets no jump or termination escape, rest on a basis that c1 leaves unverified, so they are not provisions.

Checking. Run-time detectors find invalid accesses at about twice the run time and are documented as tools for finding bugs and not for production, and a detector of undefined behavior checks signed overflow, shifts, bounds of arrays of known size, null, alignment, and pointer overflow, while its checks of unsigned overflow and implicit conversion report defined behavior (c1, S30 and S31). The second sentence of STND.STDC.37 lists the kinds that STND.STDC.8, STND.STDC.9, STND.STDC.10, STND.STDC.11, STND.STDC.12, STND.STDC.14, and STND.STDC.27 govern; STND.STDC.13 concerns how a check is written and adds no kind. One compiler's warning for overflow has done nothing for years and is kept for compatibility (c1, S41), so a silent warning is not evidence, and the first sentence of STND.STDC.37 names the diagnostics by what they detect. A compiler's analyzer for C is documented as neither sound nor complete (c1, S32), while a deductive verifier proves contracts written in a specification language for C (c1, S33); STND.STDC.38 has each record of a verification say which of the two it is. Where the verification concerns data races, one record meets STND.STDC.38 and STND.CONC.27.

High assurance. The two coding standards for C that c1 examines are suited to adoption by a decision record under the C reading of STND.CXX.28, because neither requires the corpus to name a revision; the coverage of the edition is the hazard that differs from C++. In the sources of c1, the published coverage of one ends below the newest edition and that of the other at an older edition (c1, S28, S29, and S40), so the C reading of STND.CXX.30 fixes the edition in force for high-assurance code at one that the adopted standard covers, unless a decision record admits one feature of a later edition. Conformance reduces undefined behavior by a mechanical check and is not evidence that a result is correct (VV.1), as the Notes of STND.CXX say for C++.

Floor. STND.STDC.2 and STND.STDC.28 are binding, and each rests on its prime directive alone. The C reading of STND.CXX.16 admits only the responses of PRIME.4 and the return of the condition to a caller that responds, and its row excludes errno alone, which loses the condition at the next call. The C reading of STND.CXX.17 asks one attribute per function, without which a returned listed failure is ignored silently. The C reading of STND.CXX.18 keeps in every build a check that CPS.5, CPS.9, or STND.CODE.6 requires, at the cost of one choice of compiler option. The C reading of STND.CXX.29 asks a claim of conformance to name the means that checked it, which PRIME.2 already asks of every claim. STND.STDC.28 asks two tests per stream before its output is relied upon, without which a failed write passes silently. None asks for work that PRIME.4 or PRIME.2 does not, so none raises the floor (GOV.11). The custodian's rulings that STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29 raise no floor concern C++; the extension of those rulings to C, and the reading of PRIME.4 on which STND.STDC.28 rests, are decisions for the custodian (PRIN.10). Both bind at every class, CSQ4 included; the C reading of STND.CXX.29 reaches only high-assurance code, which is never below CSQ1.

Class onset. Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR, REPRO, RSRC, VV, or a provision of HW, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of the table of STND.CLASS.10 applies from the class of that row. The rows of STND.STDC.1 apply from the classes that its table gives. The row of DSGN.2 in STND.CLASS.10 is read as STND.CXX reads it: a check of untrusted input where it enters applies from CSQ3, with DSGN.2 itself, and the retained checks of other preconditions, of postconditions, and of invariants, among them the assumptions of STND.CXX.24 and the library checks of STND.CXX.27, from CSQ1. STND.STDC.21, STND.STDC.22, and STND.STDC.27 check untrusted input where it enters and apply from CSQ3. STND.STDC.8, STND.STDC.11, STND.STDC.12, STND.STDC.13, and STND.STDC.18 ask that an operation be shown safe by any of their means, which is the obligation of DSGN.1 not to rely on behavior under an unrejected precondition violation, and apply from CSQ3; a run-time check is one of their means and is not required. STND.STDC.7 and STND.STDC.36 rest on DSGN.4 and STND.STDC.29 on DSGN.5, and apply from CSQ2, as STND.CXX.6 and STND.CXX.21 do. STND.STDC.38 rests on INTPR.10 and applies from CSQ2, as STND.CONC.27 does. STND.STDC.37 instantiates DSGN.3 and applies from CSQ3; its second sentence has effect where the C reading of STND.CXX.26 applies, from CSQ2. STND.STDC.33 and STND.STDC.35 state what a protocol uses under DSGN.15, and not how its invariants are verified, so they apply from CSQ3. The tests of STND.STDC.16 and STND.STDC.26 compare with a build of the same code, not with a reference oracle produced without it, so they apply from CSQ3. The other defaults rest on no row and apply from CSQ3. No default raises the floor (GOV.11).

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
| STND.BUILD | Build standard |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.CXX | C++ standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.MPI | Message Passing Interface standard |
| STND.OMP | OpenMP standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Provisions of STND.CXX

#### STND.STDC.1 C++ defaults applied to C

Default. Instantiates DSGN.1, DSGN.2, DSGN.3, DSGN.4, DSGN.15, DSGN.16, INTPR.1, INTPR.3, REPRO.2, REPRO.3, REPRO.7, REPRO.9, SIMPL.6, RSRC.4, VV.1, HW.5.

The C reading of each provision of STND.CXX that the table of this provision lists SHALL apply to the C source of the work of the class that its row gives and of each more severe class, each sentence keeping its modal and the provision its mode (DSGN.1, DSGN.2, DSGN.3, DSGN.4, DSGN.15, DSGN.16, INTPR.1, INTPR.3, REPRO.2, REPRO.3, REPRO.7, REPRO.9, SIMPL.6, RSRC.4, VV.1, HW.5). A project instrument MAY replace the C reading of one row by a recorded decision with an alternative that meets the same higher-level outcome, and keep the other rows (REPRO.7).

| Provision | Applies from | Change in its C reading |
| --- | --- | --- |
| STND.CXX.4 | CSQ3 | The options stated include each option that defines a behavior that the ISO C standard leaves undefined |
| STND.CXX.7 | CSQ2 | A type distinct from that of a pointer into host memory is a pointer to a distinct type, or a structure that holds the pointer; a type alias is not one |
| STND.CXX.9 | CSQ3 | None |
| STND.CXX.12 | CSQ3 | None |
| STND.CXX.15 | CSQ3 | Without the words reference, view, iterator, and C++ exception |
| STND.CXX.23 | CSQ3 | The type volatile std::sig_atomic_t is read as volatile sig_atomic_t |
| STND.CXX.24 | CSQ1 | The markers of an assumption are an assumption attribute and the unreachable marker of the edition in force, and the builtins of a compiler |
| STND.CXX.25 | CSQ3 | Without the checks of the Core Guidelines and of the names of STND.CXX.14 |
| STND.CXX.26 | CSQ2 | None |
| STND.CXX.27 | CSQ1 | None |
| STND.CXX.28 | CSQ1, for high-assurance code | None |
| STND.CXX.30 | CSQ1, for high-assurance code | None |
| STND.CXX.31 | Each class at which a high-assurance coding standard is adopted | None |

#### STND.STDC.2 Binding C++ provisions applied to C

Binding. Instantiates PRIME.4, PRIME.2, DSGN.2, CPS.5, CPS.9.

The C reading of each provision of STND.CXX that the table of this provision lists SHALL apply to the C source of the work, each sentence keeping its modal (PRIME.4, PRIME.2, DSGN.2, CPS.5, CPS.9).

| Provision | Change in its C reading |
| --- | --- |
| STND.CXX.16 | The responses are those of the provision other than a C++ exception; a report of the condition through errno alone is not a return of the condition in the result |
| STND.CXX.17 | None |
| STND.CXX.18 | None |
| STND.CXX.29 | None |

#### STND.STDC.3 Lowered C editions recorded

Default. Instantiates DSGN.3, REPRO.7.

Other than in a change whose decision record names the compiler, the dependency, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain that requires it, a change SHOULD NOT lower the edition in force for a translation unit of C source (DSGN.3, REPRO.7).

### Language level

#### STND.STDC.4 Conditional features tested

Default. Instantiates DSGN.3, SIMPL.6.

Each translation unit of C source that uses a conditional feature SHOULD hold a preprocessor test that stops its compilation with a diagnostic on an implementation that reports that feature absent (DSGN.3, SIMPL.6).

### Ownership and lifetime

#### STND.STDC.5 Release on every path

Default. Instantiates DSGN.14.

Each owned resource that a function acquires, and does not pass to its caller or to another owner, SHOULD be released on every path out of that function, failure paths included (DSGN.14). Where a function holds more than one owned resource, it SHOULD release them through one sequence of release operations, written once in the function, that each path out of the function enters at the point that matches the resources it holds, or through a function of the work that owns their release (DSGN.14).

#### STND.STDC.6 Release functions named

Default. Instantiates DSGN.1.

In addition to what the C reading of STND.CXX.15 asks, the documentation comment of each declaration that returns or keeps an owned resource SHOULD name the function by which the owner of that resource releases it (DSGN.1).

#### STND.STDC.7 Extents passed with pointers

Default. Instantiates DSGN.4.

Other than at an interface whose form a dependency or a published interface of the work fixes, each pointer to a sequence of objects that crosses an interface of the work SHOULD travel with the extent of that sequence, in one structure with it or in a parameter that the contract of the interface pairs with it (DSGN.4).

#### STND.STDC.8 Accesses within their object

Default. Instantiates DSGN.1, SIMPL.11.

Each array subscript, and each result of pointer arithmetic, SHOULD lie within the array object into which its pointer points, or one past its last element for a result that code does not dereference (DSGN.1). Each such access SHOULD be shown to lie there by a check that precedes it, by a static check, or by a bounds invariant that a comment at the access states (DSGN.1, SIMPL.11).

#### STND.STDC.9 Objects used within their lifetime

Default. Instantiates DSGN.14.

Code SHOULD NOT access an object through a pointer after the lifetime of that object has ended (DSGN.14). Where the pointer through which the owner of an allocation releases it outlives the release, the owner SHOULD set that pointer to a null pointer at the release (DSGN.14).

#### STND.STDC.10 Initialization before reads

Default. Instantiates DSGN.1, REPRO.3.

Each object SHOULD be initialized or assigned before code reads its value (DSGN.1). Before the bytes of an object of structure or union type leave the process, by a write to a file, to a socket, or to a buffer that another component reads, each padding byte of that object SHOULD be set (REPRO.3).

### Undefined behavior

#### STND.STDC.11 Signed overflow excluded

Default. Instantiates DSGN.1.

Where an operand of an arithmetic operation on signed integers comes from outside the function that performs it, that operation SHOULD be shown not to overflow, by a check of its operands that precedes it, by a static check, by a range argument that a comment at the operation states, or by its replacement with a checked operation that reports overflow (DSGN.1).

#### STND.STDC.12 Division and shift operands

Default. Instantiates DSGN.1.

Each integer division and remainder SHOULD have a divisor shown to be nonzero and, for signed operands, a dividend and a divisor shown not to be the most negative value of their type and minus one together (DSGN.1). Each shift SHOULD have a count shown to be at least zero and less than the width of its promoted left operand, and a left operand whose type after the integer promotions is unsigned, or a nonnegative value whose shifted result that promoted type represents (DSGN.1).

#### STND.STDC.13 Guards free of undefined behavior

Default. Instantiates DSGN.1.

Each check that guards an operation against undefined behavior SHOULD precede that operation on every path that reaches it (DSGN.1). Each such check SHOULD be written without an operation whose behavior is undefined for the values against which it guards, the formation of a pointer outside its object included (DSGN.1).

#### STND.STDC.14 Access through compatible types

Default. Instantiates DSGN.1.

Code SHOULD access the stored value of each object only through an lvalue of a type that the edition in force admits for the effective type of that object, or through an lvalue of a character type (DSGN.1). Code SHOULD reinterpret the representation of an object only through a copy of its bytes, or through a member of a union as the edition in force defines that access (DSGN.1).

#### STND.STDC.15 Sequenced accesses to scalars

Default. Instantiates DSGN.1.

Where at least one of two accesses to one scalar object modifies that object, code SHOULD order the two by a sequencing relation that the edition in force defines (DSGN.1).

#### STND.STDC.16 Settings that define undefined behavior

Default. Instantiates DSGN.1, VV.1.

Where a compiler option defines, for a translation unit, a behavior that the ISO C standard leaves undefined, the argument for the correctness of the code SHOULD NOT rely on that option (DSGN.1). Where the work builds code under such an option, the tests of that code SHOULD also pass, within the tolerance of their acceptance criterion, in a checking build of STND.BUILD.13 that builds that code without the option (VV.1).

### Integers

#### STND.STDC.17 Value-changing conversions made explicit

Default. Instantiates DSGN.1.

Each conversion of an integer value to an integer type that does not represent every value of its source type SHOULD be an explicit conversion, preceded by a check or accompanied by a range argument that shows the value representable in the target type (DSGN.1). The two operands of each relational and equality comparison of integers SHOULD have the same signedness before the usual arithmetic conversions (DSGN.1).

#### STND.STDC.18 Types of sizes and counts

Default. Instantiates DSGN.1.

Each object that holds a size, a count, or an index SHOULD have a type that represents each value that the object takes in the regime of use (DSGN.1). Each size that code computes for an allocation SHOULD be shown not to overflow, by a check before the allocation, by a static check, or by its computation with an operation that reports overflow (DSGN.1).

### Strings and buffers

#### STND.STDC.19 Bounded buffer writes

Default. Instantiates DSGN.1.

Each write into a buffer SHOULD be bounded by the size of that buffer, by the operation that writes or by a check of its source that precedes the write (DSGN.1). Each operation that writes a string into a buffer SHOULD leave that string terminated within the buffer (DSGN.1).

#### STND.STDC.20 Truncation reported or intended

Default. Instantiates DSGN.1, REPRO.7.

Each truncation of a string or of a sequence of bytes to the size of its destination SHOULD be reported to the caller as a failure, or carry at its location a statement that the truncation is intended (DSGN.1, REPRO.7).

#### STND.STDC.21 Lengths from untrusted input

Default. Instantiates DSGN.2.

Each length, count, offset, or index that arrives in untrusted input SHOULD be checked against the extent of the object that it describes before code reads or writes through it (DSGN.2). Each read of a string from untrusted input SHOULD be bounded by the extent of its buffer, independently of a terminator that the input supplies (DSGN.2).

#### STND.STDC.22 Checked format strings

Default. Instantiates DSGN.2, DSGN.3.

The format string of each call to a formatted input or output function SHOULD be a string literal, or a string that the code checks against the number and the types of the arguments of that call before the call (DSGN.2). The static checks of the work SHOULD diagnose each call whose literal format string does not match its arguments (DSGN.3).

### Preprocessor

#### STND.STDC.23 Language facilities over macros

Default. Instantiates INTPR.1, DSGN.3.

Where a constant object, an enumeration constant, an inline function, or a static assertion of the edition in force provides what a macro provides, code SHOULD use that facility in place of the macro (INTPR.1, DSGN.3).

#### STND.STDC.24 Function-like macro hygiene

Default. Instantiates DSGN.1.

Each function-like macro SHOULD evaluate each of its arguments at most once (DSGN.1). Other than a parameter that is an operand of the # or ## operator or that names a type, each parameter of a function-like macro whose expansion is an expression SHOULD be enclosed in parentheses at each use, and the whole expansion with it (DSGN.1).

#### STND.STDC.25 Conditional compilation under check

Default. Instantiates DSGN.3, VV.8.

Other than a branch for a target that the repository configuration records as unchecked, each branch of conditional compilation in C source SHOULD be compiled by at least one configuration that the checks of each change build (DSGN.3, VV.8).

### Qualifiers and arrays

#### STND.STDC.26 Restrict-qualified pointers

Default. Instantiates DSGN.1, VV.1.

Each pointer that code declares with the restrict qualifier SHOULD have, in the contract of the function of which it is a parameter or in a comment at its declaration, a statement of the objects that code reaches through it and through no other pointer during its block (DSGN.1). Each such statement SHOULD be checked by a check at the entry of the function, or by tests whose results agree, within the tolerance of their acceptance criterion, with the results of a build without the qualifier (VV.1).

#### STND.STDC.27 Bounded variable-length arrays

Default. Instantiates DSGN.2, RSRC.1.

Each object of variable-length array type with automatic storage duration SHOULD have a number of elements that a check preceding its declaration bounds by a limit that its component states (DSGN.2, RSRC.1).

### Failures

#### STND.STDC.28 Stream errors before reliance

Binding. Instantiates PRIME.4.

Before a result that code writes to a stream without testing the result of each write is reported or relied upon, the code SHALL test the error indicator of that stream before it closes the stream, and the result of the call that flushes or closes it (PRIME.4).

#### STND.STDC.29 Library failure results diagnosed

Default. Instantiates DSGN.5, REPRO.7.

Each function of the C library or of another dependency that reports in its result a failure of a kind that PRIME.4 lists SHOULD be called through a declaration, its own or that of a function of the work that wraps it, under which the compiler or a static check diagnoses each call that ignores that result (DSGN.5). Where the test of STND.STDC.28, or an error handler that ends the run, receives the failure of such a call, the call SHOULD carry at its location the suppression of STND.CODE.4, with its reason naming that test or handler (REPRO.7).

#### STND.STDC.30 Release failures tested

Default. Instantiates DSGN.1.

Before a result is relied upon, each failure that the release of an owned resource other than a stream reports, and that affects that result, SHOULD be tested and answered as the C reading of STND.CXX.16 provides (DSGN.1).

#### STND.STDC.31 C failure channel

Default. Instantiates DSGN.1, DSGN.14.

Each failure that the caller of a function is designed to handle SHOULD be reported by the return value of that function, or by an object that its contract names as its result for failures (DSGN.1). A nonlocal jump SHOULD NOT leave a function that holds an owned resource that it has not released (DSGN.14).

#### STND.STDC.32 Errno as a report of failure

Default. Instantiates DSGN.1.

Code SHOULD set errno to zero before each call of a library function that reports failure only through errno, and read errno for that call before another call that is able to change it (DSGN.1). Where a function reports failure in its result as well as through errno, code SHOULD read errno for a call of it only after that result indicates failure (DSGN.1).

### Signals and threads

#### STND.STDC.33 Signal handler calls

Default. Instantiates DSGN.15, DSGN.14.

A signal handler SHOULD call only signal-safe functions (DSGN.15). A signal handler that calls a function able to change errno SHOULD restore, on each return, the value that errno held at its entry (DSGN.14).

#### STND.STDC.34 Computational exception signals

Default. Instantiates DSGN.1.

A handler of a signal that reports a computational exception, an invalid instruction, or an invalid access to memory SHOULD NOT return to the code that the signal interrupted (DSGN.1).

#### STND.STDC.35 Adjacent bit-fields shared

Default. Instantiates DSGN.15.

Where concurrent tasks access bit-fields of one structure, at least one of them by a write, the protection that STND.CONC.3 asks SHOULD cover each maximal sequence of adjacent bit-fields of nonzero width as one shared mutable object (DSGN.15).

### Interfaces to other languages

#### STND.STDC.36 Data crossing to other languages

Default. Instantiates DSGN.4.

Each type of data that crosses a foreign interface SHOULD have a width and a layout that the contract of the interface fixes (DSGN.4). Each array of more than one dimension that crosses a foreign interface SHOULD have the order of its dimensions and the origin of its indexes stated in that contract (DSGN.4).

### Checking

#### STND.STDC.37 C warnings and detected behavior

Default. Instantiates DSGN.3.

Where a compiler of the toolchain matrix offers a diagnostic of a read of an object before its initialization, of a format string that does not match its arguments, of an ignored result of a function so declared, of a comparison of signed and unsigned operands, or of an implicit conversion that changes a value, the recorded set of warnings of the C reading of STND.CXX.25 SHOULD include that diagnostic (DSGN.3). The kinds of undefined behavior that the repository configuration lists under the C reading of STND.CXX.26 SHOULD include each kind that STND.STDC.8, STND.STDC.9, STND.STDC.10, STND.STDC.11, STND.STDC.12, STND.STDC.14, or STND.STDC.27 governs and that a detector among the means of the work detects at run time (DSGN.3).

#### STND.STDC.38 Stated limits of analysis

Default. Instantiates VV.1, INTPR.10.

The record of each verification that finds C code free of a kind of undefined behavior SHOULD state its means, and whether the documentation of that means states it as sound for that kind (VV.1, INTPR.10).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
