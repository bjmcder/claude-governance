# C standard (STND.STDC) 1.2

Adopted by The Custodian as revision 1.0 in ledger entry 130 (2026-10-24); revised to 1.1 in entry 149 (2026-10-25) and 1.2 in entry 193 (2026-10-27). This reading copy is composed from the per-provision files in STND/STDC/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.STDC.36.

## Purpose and scope

This standard holds the coding practice that is specific to C. It adds to STND.CODE, STND.DOCS, and STND.CONC only what the language makes necessary. It applies to C source each default of STND.CXX whose outcome holds for C, in a C reading that its Terms define, in place of restating it (STND.STDC.1), states the C form of the responses to a failure that PRIME.4 lists (STND.STDC.2), states for C the binding form of STND.CXX.18 on the option that assumes finite values (STND.STDC.40), records each lowering of the edition of a translation unit (STND.STDC.3), and asks a test of each conditional feature that a unit uses (STND.STDC.4). It states how code without destructors releases what it owns, passes sequences with their extent, and keeps each access within its object and the lifetime of that object (STND.STDC.5 to STND.STDC.10). It excludes the classes of undefined behavior that optimizers exploit and keeps the correctness of code independent of options that define them (STND.STDC.11 to STND.STDC.16), and covers integer conversions and the types of sizes (STND.STDC.17 and STND.STDC.18), strings and buffers (STND.STDC.19 to STND.STDC.22), the preprocessor (STND.STDC.23, STND.STDC.24, and STND.STDC.25), restrict-qualified pointers and variable-length arrays (STND.STDC.26 and STND.STDC.27), stream errors, failures, errno, and ignored results (STND.STDC.28 to STND.STDC.32), signal handlers and bit-fields shared between threads (STND.STDC.33, STND.STDC.34, and STND.STDC.35), the checks of C code (STND.STDC.37 and STND.STDC.38), and names (STND.STDC.39). STND.CODE holds for C, as for every language, the responses to a failure that PRIME.4 lists, the declarations that keep a returned failure from being ignored, the checks that no execution setting and no definition in the source removes, and the high-assurance provisions: conformance to the high-assurance coding standard that a decision record of the work adopts, claims of conformance limited to what was checked, an edition that the standard covers and the toolchain is validated for, and recorded deviations (STND.CODE.14, STND.CODE.15, STND.CODE.16, STND.CODE.17, STND.CODE.18, STND.CODE.19, and STND.CODE.20), and the rules of each foreign interface (STND.CODE.22 to STND.CODE.26).

STND.STDC.2 and STND.STDC.40 instantiate PRIME.4 and are binding at every class. Every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same higher-level outcome (REPRO.7). The standard is compiler, edition, platform, and tool agnostic: its provisions name the constructs of C and no edition, compiler, library to depend on, platform, or tool, and the repository configuration or a project instrument chooses them (GOV.18). It sets no edition for C; the repository configuration states the edition of each translation unit. The build matter that it holds is that of two applied provisions, the C reading of STND.CXX.4, which states the edition, disables extensions, and states the options that change what a unit means, and the C reading of STND.CXX.25, which records a set of compiler warnings and fails a change on each; the second sentence of STND.STDC.16 adds a run of the tests in a build named apart as STND.BUILD.13 provides. The rules of concurrency that hold for every language are in STND.CONC, which applies to C by its own scope and which this standard cites and does not restate.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, High-assurance coding standard, and Foreign interface have the meanings that STND.CODE gives them. Translation unit, Toolchain matrix, and Owned resource have the meanings that STND.CXX gives them, and Edition in force the meaning that STND.CXX gives it in its C reading. Concurrent task, Shared mutable object, and Protection have the meanings that STND.CONC gives them; a signal handler is a concurrent task.

| Term | Definition |
| --- | --- |
| C source | Source of the work in C: each file that a compiler of the work translates as C, and each header that such a file includes, other than a header of the implementation or of a dependency, and other than external code that the work incorporates and keeps apart as STND.DEPS.11 recommends. A header that C and C++ translation units both include is C source and C++ source. |
| C reading | Of a provision or a term of STND.CXX, at the revision of STND.CXX in force: that provision or term applied to C source, with C, the ISO C standard, the C standard library, and an implementation of the C standard library in place of C++, the ISO C++ standard, the C++ standard library, and a standard library implementation; with each term that this standard defines in place of the term of STND.CXX of the same name; with each other term of STND.CXX, and each provision of STND.CXX that it cites, taken in the same reading; and with the change, if any, that the row of that provision in the table of STND.STDC.1 gives. |
| Conditional feature | A feature of an edition of the ISO C standard that the edition lets an implementation omit, and whose presence or absence the implementation reports by a predefined macro that the edition names. |
| Undefined behavior | Behavior for which the ISO C standard, at the edition in force, imposes no requirements. |
| Signal-safe function | A function that the ISO C standard, or the documentation of the platform on which the code runs, states as one that a signal handler is able to call. |

## Notes

The standard is agnostic of compiler, edition, platform, implementation, and tool, and cites the provision that holds an outcome in place of restating it (GOV.31). It is modeled on STND.CXX, in the form of STND.PY and STND.JL, and its binding provision gives C the responses to a listed failure that STND.PY.22 and STND.JL.15 give Python and Julia. Each provision states an outcome that a tool or a reviewer decides, and names constructs of C, which GOV.18 admits at LVL2; the Notes name a compiler, a library function, or a coding standard only to show a hazard. The source is the research note research/c-notes/c1-c-language.md (cited as c1), with the note research/round-addenda/a1-confirmations.md (cited as a1) for the facts on streams and research/round-addenda/a2-language-facts.md (cited as a2) for the assert macro and the options that assume finite values, and a fact that none of these notes supports is marked unverified.

C reading. Much of STND.CXX holds for C, because the two languages share a model of compilation, the kinds of their undefined behavior, and the failures at the boundary of a library. STND.STDC.1 applies the defaults among those provisions to C source in their C reading, so that each keeps one text and its mode, and this standard holds only what C adds (GOV.31). The rules that C shares with C++ and with every other language, the responses to a listed failure and the high-assurance provisions among them, are in STND.CODE, which applies to C by its own scope, and STND.STDC.2 gives the C form of one of them. Each row of STND.STDC.1 carries the class from which it applies, the onset that the Notes of STND.CXX give its provision, and a project replaces one row without the others. The reading follows the revision of STND.CXX in force; where a provision of STND.CXX cites STND.CONC, the cited provision applies to C by its own scope. A header that C and C++ units both include meets both readings where it keeps to what the two languages share; the linkage of a constant object and of an inline function differs between them (unverified).

Provisions of STND.CXX that apply. STND.CXX.4 states the edition, disables extensions, and states the options that change what a unit means; the default dialect of one compiler enables extensions that change the meaning of the base standard (c1, practice 1). Its row adds the options that define a behavior that the language leaves undefined, which its third sentence does not name. STND.BUILD.11 and STND.BUILD.12 are the general rules for settings and warnings in every language, and the rows of STND.CXX.4 and STND.CXX.25 hold the C items. The edition stated is one of the ISO C standard, since a compiler's default is a dialect and its names for editions change (c1, Editions). STND.CXX.7 holds with its row: a register is reached through a volatile-qualified object (c1, What the corpus already holds), and a type alias in C names the same type, so a distinct type for a pointer into device memory is a pointer to a distinct type or a wrapping structure. STND.CXX.9 holds because results of the C library also depend on behavior that the ISO C standard leaves to the implementation; c1 lists STND.CXX.8 to STND.CXX.10 as not carrying, and the examples of such behavior, the sequence of the pseudo-random generator, the order of equal elements after a sort, and the accuracy of mathematical functions, are unverified. STND.CXX.12 is met in C by static assertions; c1 lists it both as not carrying and, in its section on the preprocessor, as carrying, and its text names no C++ facility. STND.CXX.15 gives the ownership contract that C needs most, and STND.STDC.6 adds the function that releases what a declaration returns. STND.CXX.23 gives the C type for an object that a signal handler shares, beside a lock-free atomic object. STND.CXX.24 covers the unreachable marker of an edition that has one and the builtins of a compiler. STND.CXX.25, STND.CXX.26, and STND.CXX.27 give the warnings, the run-time detection that fails at its first detection, and the library checks in production.

Provisions of STND.CODE for every language. STND.CODE.14 admits every response but a C++ exception; a nonlocal jump is a mechanism of C that carries a condition past its callers, and STND.STDC.31 governs it. STND.STDC.2 adds that a report through errno alone does not pass the condition to the caller. STND.CODE.15 is met by the attribute that an edition provides for a result not to be discarded, or by a compiler's equivalent (c1, Error reporting and ignored returns). The assert macro is the C case of STND.CODE.6 and of the second sentence of STND.CODE.16, whose Notes give the reasoning from the C header (a2, N3220 7.2). An option that assumes finite values may remove a test for non-finite values (a2); STND.CODE.21 recommends against it in every language, and STND.STDC.40 states for C, in the words of STND.CXX.18, the binding form that the table of STND.STDC.2 applied to C in revision 1.0; a later change of STND.CXX.18 does not change it. C places no function in the public interface by a construct of the language, because external linkage also serves the calls between the translation units of one program, so the documentation or the repository configuration names the interface for outside use of the term Untrusted input, and a check of an argument of a function that it names is a check of untrusted input under STND.CODE.6, STND.STDC.21, and STND.STDC.27. Where such an argument is a pointer that carries no extent, the check of STND.STDC.21 is possible only against an extent or a limit that the contract states, as STND.STDC.7 and STND.STDC.27 provide. The two coding standards for C in c1 are high-assurance coding standards in the sense of STND.CODE, and the published coverage of one ends below the newest edition and of the other at an older one (c1, S28, S29, and S40), so STND.CODE.19 fixes the edition of high-assurance code at a covered one unless a decision record admits a feature of a later edition. Conformance reduces undefined behavior by a mechanical check and is not evidence that a result is correct (VV.1).

Provisions of STND.CXX that do not apply. STND.CXX.1 names the Core Guidelines, which concern C++. STND.CXX.2 carries the custodian's direction for the latest edition of C++, so this standard sets no edition for C, and STND.DEPS.4 reviews the stated one with the pinned revisions; STND.CXX.3 depends on it, and STND.STDC.3 asks the record of a lowering instead. STND.CXX.5 rests on destructors and resource handles, STND.CXX.6 on view types, STND.CXX.8 and STND.CXX.10 on reasons specific to the C++ library and headers, STND.CXX.11 and STND.CXX.13 on templates, and STND.CXX.19 and STND.CXX.21 on C++ exceptions and destructors; STND.STDC.5, STND.STDC.7, STND.STDC.8, STND.STDC.29, STND.STDC.30, and STND.STDC.31 state their outcomes for C. The naming table of STND.CXX.14 is the custodian's convention for C++. C has no convention of names of its own that a tool is able to check, so STND.STDC.39 leaves the convention to the repository configuration, as STND.LEAN.27 does for Lean, keeps the names that the notation of NUMER.4 fixes, and adds no table; STND.DOCS.12 still asks one name for each concept. STND.CODE.24 binds the side of a boundary whose language propagates a failure by a mechanism of its own, an exception or a panic; c1 leaves unverified that the ISO C standard defines a nonlocal jump only within C frames, so no provision binds the C side for such a jump, and STND.OMP.21 keeps such a jump out of a structured block of OpenMP.

What the corpus already holds. STND.CODE.3 to STND.CODE.7, STND.CODE.11 to STND.CODE.13 apply to C as to every language: contracts at declarations, static checks with a suppression and its reason at the location of each finding left in place, a layout tool, unremovable checks of untrusted input, no discarded failure of a kind that PRIME.4 lists, no code disabled in comments, a reason for each other discard, and statements grouped by step. A block under a condition that is always false is disabled code in the sense of STND.CODE.11, and STND.STDC.25 does not count it as a branch to compile. STND.CONC applies to C by its own scope, a thread and a signal handler being concurrent tasks: protection of shared objects (STND.CONC.3), sequentially consistent atomics or a reason (STND.CONC.4), lifetimes (STND.CONC.5), concurrent calls in contracts (STND.CONC.6), lock order and conduct, the release of a lock on every path among them (STND.CONC.7, STND.CONC.8), joined threads (STND.CONC.12), signal handling left unchanged by libraries (STND.CONC.17), child processes (STND.CONC.19), and race detection (STND.CONC.25). STND.DEPS.8 records each compiler revision, STND.DEPS.9 each analyzer, and STND.DEPS.11 keeps a copied library apart, which is why the term C source leaves it out. NUMER.16 and NUMER.17 govern options that relax floating-point semantics, NUMER.5 and NUMER.16 a narrowing of a floating-point value, HW.5 the delivered arithmetic, and HW.CPU.3 the floating-point control state, which C changes through its floating-point environment; whether such code also needs the pragma for access to that environment is unverified.

Ownership without destructors. C has no destructor, so an owned resource is released by code that each path out of a function reaches (c1, Resource management without destructors). One kernel coding style gives the reasons for one exit region per function, reached by jumps to labels that release in reverse order: the code is easier to follow, nesting is reduced, and no change updates one exit point and misses another (c1, S15). A wrapper that owns the release is the other form that STND.STDC.5 admits. A cleanup attribute of some compilers and a deferred-release facility on the agenda of the committee of the language are not part of a published edition (unverified). A reallocation whose result overwrites the only pointer to the block loses the block on failure, a path on which it is not released (STND.STDC.5), and a size computed as a count times an element size wraps (STND.STDC.18; c1, S21). An allocation result used without a test discards a listed failure, which STND.CODE.7 forbids.

Undefined behavior. The overview annex of the working draft of the newest edition lists 221 circumstances of undefined behavior (c1, S1; unverified against the published text). A compiler is allowed to assume that none occurs, so an optimizer removes code that is correct only if one does: a test that x + 1 exceeds x becomes true, and a dereference ahead of a test for null lets the test go (c1, S4). A check that relies on the undefined operation itself is removed, a pointer plus a length compared with the pointer among them (c1, S6; STND.STDC.13); the same study found 160 confirmed bugs of code that an optimizer is able to discard, and estimated that such code exists in 40 percent of 8,575 packages of one distribution. STND.STDC.8 to STND.STDC.15 cover the classes that c1 finds behind most defects. Signed overflow stayed undefined when two's complement became the only representation (c1, hazard table). Compilers treat reads of uninitialized objects as license (c1, hazard table), and an option that initializes automatic storage is a defense beside STND.STDC.10, not a replacement. Padding written out of the process discloses earlier memory and makes two runs write different bytes (REPRO.3). A survey of 323 people who write C found that practice, compilers, and the standard disagree on provenance, uninitialized values, padding, and effective types (c1, S11), so STND.STDC.14 states what the standard defines. One kernel builds with the aliasing assumption off, signed overflow wrapping, null-check removal off, and automatic variables initialized (c1, S3). The C reading of STND.CXX.4 states such an option, and STND.STDC.16 keeps correctness from resting on it; its second sentence runs the tests in a build named apart under STND.BUILD.13 without the option, and the build that detects undefined behavior under STND.CXX.26 is a natural choice, since its detector reports what the option hides. Intended unsigned wraparound, in a hash among them, is no defect, and a detector's report of it is suppressed at its location (STND.CODE.4).

Showing an operation safe. STND.STDC.8, STND.STDC.11, and STND.STDC.18 admit a check before the operation, a static check, a stated argument, and for arithmetic a checked operation, which the newest edition provides (c1, S1). STND.STDC.11 reaches operands from outside the function (c1, practice 2). An index from untrusted input is checked where it enters, as DSGN.2 and STND.STDC.21 ask, and a comment is no substitute there. C promotes integer types narrower than int and converts mixed signedness to unsigned, so a narrow unsigned operand is shifted as a signed int and a negative value compared with an unsigned one becomes large (c1, Integer conversions and promotions); STND.STDC.12 therefore judges a left shift by the promoted type. Intended and unintended, defined and undefined overflow are all common (c1, S5), so a check of integer arithmetic is not a report of every overflow.

Strings, buffers, and macros. A C string has no length, so each operation trusts its termination or carries a size (c1, Strings and buffers). One kernel project removed or replaced the copy functions that fail to terminate, take no bound, or read past an unterminated source, and the optional bounds-checking interfaces of the language were found intrusive and were not shipped by the common library (c1, S21 and S37), so STND.STDC.19 to STND.STDC.21 state the outcome and leave the means to the project. STND.STDC.20 concerns strings and bytes; a narrowing of a numerical value is NUMER's. Compilers diagnose a format string that does not match its arguments (c1, S19). A macro that evaluates an argument twice repeats its side effect, an unparenthesized parameter binds to the operators around it, and a branch that no configuration builds has had no check (c1, The preprocessor); later editions moved constant objects, static assertions, and type inference into the language (STND.STDC.23). A result computed on a branch recorded as unchecked has no evidence from the checks (PRIME.3).

Restrict and variable-length arrays. A violation of a restrict qualifier is undefined, and removing the qualifier from a conforming program leaves its meaning unchanged, so a build without it is a reference for a test (c1, practice 17; STND.STDC.26). That build is able to order floating-point operations differently, so the comparison agrees within the tolerance of the acceptance criterion, bitwise only where the criterion asks it (STND.VVUQ.82), on the basis that NUMER.11 gives. Variable-length array objects are a conditional feature, and one kernel project removed them from its stack, citing worse machine code and a stack that grows past its segment (c1, S1 and S21); STND.STDC.27 bounds a size from untrusted input, and STND.STDC.4 tests for the feature.

Failures. PRIME.4 lists invalid input, detected precondition violations, non-convergence, and resource exhaustion, and its last sentence excludes silent continuation past an error. The C library reports failure by a return value, by errno, by the error indicator of a stream, or not at all (c1, Error reporting and ignored returns). The working draft states that errno is zero at startup, that a library function is able to set it whether or not an error occurred unless its documentation states otherwise, and that no library function is required to set it to zero (c1, S1, 7.5), from which STND.STDC.32 follows; a separate errno for each thread is unverified. A condition in errno alone is lost at the next call that sets errno and escapes the diagnosis of STND.CODE.15, which STND.STDC.2 excludes.

Streams. In the working draft of the 2024 edition of C, fflush sets the error indicator of its stream and returns EOF if a write error occurs, fclose delivers the unwritten buffered data of its stream to the host environment to be written and returns EOF if any errors were detected, and a write error in fputc, putc, putchar, or fputwc sets the error indicator of the stream (a1, WG14 N3220, 7.23.5.1, 7.23.5.2, and the character output functions of 7.23.7). The byte output functions, fputs, puts, fwrite, and fprintf among them, write as if by successive calls to fputc, so a write error in any of them sets the indicator as well (a1, 7.23.1 and 7.23.3). The indicator records whether an error has occurred, and clearerr clears it, so a set indicator stays set until code clears it (a1, 7.23.1 and 7.23.10.1). That note read this draft alone, and the text of earlier editions is unverified. STND.STDC.28 asks, as a default, the tests that receive those failures and an answer to each, for every stream whose output a result relies on, closed or only flushed: the result of the flush or the close receives a failure to deliver buffered data, and the error indicator receives the failure of each earlier write that sets it. A full volume is resource exhaustion, which PRIME.4 lists; another output error is not in its list, and a result reported after failed writes continues past an error, which the last sentence of PRIME.4 excludes. STND.STDC.28 stays a default: its tests are one means to the outcome that PRIME.4, STND.CODE.14, and STND.STDC.2 ask, and a project that receives each failure of the output on which a result relies by another means replaces it by a recorded decision (REPRO.7). STND.STDC.29 has a call whose failure the test of STND.STDC.28 receives carry the suppression of STND.CODE.4 that the warning of the C reading of STND.CXX.25 accepts, and a call whose failure an error handler that ends the run receives, as STND.MPI.5 admits, carries the same. For fputs, puts, fwrite, and fprintf, that test receives both a write error that the call itself meets, through the indicator, and a failure to deliver their buffered output at the flush or the close. STND.STDC.30 covers the release of other resources.

Ignored results. The rule on errors of the standard library in the CERT C coding standard lists functions whose results code is let ignore, among them formatted output to the standard output, the copying and filling functions of memory, and writes to the standard output and standard error discarded by a cast to void (c1, S16). For a failure of a kind that PRIME.4 lists, STND.CODE.7 prevails, because a coding standard is adopted under a default (STND.CODE.17) and a binding provision is only tightened below it (GOV.19). For another failure, an ignored result carries its reason under STND.CODE.12, so an entry of that list is a case for STND.CODE.12 and not an exemption. A function whose result reports no failure is outside both. A compiler or analyzer that knows the library functions meets STND.STDC.29 without a wrapper. STND.STDC.29 and the second sentence of STND.STDC.22 ask their diagnosis where the means of the work include one, so that a toolchain without the attribute or the check blocks no work, and STND.CODE.7 still forbids discarding a listed failure.

Signals and concurrency. A signal handler is allowed to refer to an object of static or thread storage duration only where it is a lock-free atomic object or is assigned as volatile sig_atomic_t, and to call only a short list of library functions, and a handler that returns after a signal of a computational exception is undefined (c1, S1, 7.14.1.1). A platform lists more functions that are safe in a handler, says that the standard input and output functions are unsafe because they share buffers, and has a handler save and restore errno (c1, S22 and S23). The object rule is the C reading of STND.CXX.23, whose condition also reaches an interrupt handler of a constrained target; STND.STDC.33 and STND.STDC.34 add the calls, errno, and the return. The edition that added threads defined a memory model under which a data race is undefined and plain operations on atomic objects are sequentially consistent (c1, S1), so STND.CONC.3 and STND.CONC.4 apply as written and a volatile qualifier is not a protection. Adjacent bit-fields share one memory location (c1, S1), which STND.STDC.35 has one protection cover, and HW.11 verifies the protocol under that model. Whether a mutex of the C library works with a condition variable of the platform library, and whether consume ordering is used in practice, are unverified; STND.CONC.3 and STND.CONC.4 govern both.

Interfaces to other languages. C is the common binary interface of most languages on a platform (c1, Interfaces to other languages). A Fortran caller sees the dimensions of an array reversed, indexes from one, and has no unsigned types (c1, S26), which STND.CODE.23 has the contract state; a Python extension holds counted references, new or borrowed, whose owner and period of validity the C reading of STND.CXX.15 states. That no jump crosses a frame of another language rests on a basis that c1 leaves unverified and is not a provision.

Checking. Run-time detectors of invalid accesses run at about twice the time and are documented as tools for finding bugs, and the detector of undefined behavior also reports defined unsigned overflow and implicit conversion (c1, S30 and S31). The second sentence of STND.STDC.37 lists the kinds that STND.STDC.8, STND.STDC.9, STND.STDC.10, STND.STDC.11, STND.STDC.12, STND.STDC.14, and STND.STDC.27 govern; STND.STDC.13 concerns how a check is written and adds none. One compiler's overflow warning has done nothing for years (c1, S41), so the first sentence names diagnostics by what they detect. A compiler's analyzer for C is documented as neither sound nor complete (c1, S32), and a deductive verifier proves contracts (c1, S33); STND.STDC.38 has the record say which a verification is, and for data races one record meets it and STND.CONC.27.

Floor. STND.STDC.2 is binding and rests on PRIME.4 alone. It adds to STND.CODE.14 only that a report of a listed condition through errno alone does not pass it to the caller, without which the condition is lost at the next call that sets errno; the cost is the report of the condition in the return value or in an object that the contract names, which STND.CODE.14 already admits as the response. It asks for no work that PRIME.4 does not, so it raises no floor (GOV.11), the argument that the ratification of 2026-10-24 accepted for the errno clause of STND.STDC 1.0. STND.STDC.40 keeps for C the binding form of STND.CXX.18, which the same ratification applied to C through the table of STND.STDC.2, at the cost of one choice of option for a unit that holds a required check. For C the hazard is this: the documentation of two compilers states the option as a license to assume that arguments and results are not NaNs or infinities (a2), the removal of a test by isnan or isfinite under it is unverified, and the binding form stays for C by the ratification of 2026-10-24, while STND.CODE.21 is the default for every other language. Both bind at every class. The binding provisions of STND.CODE that reach C, STND.CODE.6, STND.CODE.7, STND.CODE.14, STND.CODE.15, STND.CODE.16, and STND.CODE.18, carry the floor arguments that the Notes of STND.CODE give for each language.

Class onset. Under STND.CLASS.10, each default instantiates only DSGN, SIMPL, INTPR, REPRO, RSRC, VV, or a provision of HW, and applies from CSQ3; work of CSQ4 may omit it. The part of a default that rests on a row of that table applies from the class of the row, and the rows of STND.STDC.1 apply from the classes that its table gives. The row of DSGN.2 is read as STND.CXX reads it: a check of untrusted input where it enters applies from CSQ3, with DSGN.2 itself, and the retained checks of other preconditions, of postconditions, and of invariants, among them those of STND.CXX.24 and STND.CXX.27, from CSQ1. STND.STDC.21, STND.STDC.22, and STND.STDC.27 check untrusted input where it enters and apply from CSQ3. STND.STDC.8, STND.STDC.11, STND.STDC.12, STND.STDC.13, and STND.STDC.18 ask that an operation be shown safe by any of their means, the obligation of DSGN.1, and apply from CSQ3. STND.STDC.7 rests on DSGN.4 and the first sentence of STND.STDC.29 on DSGN.5, and apply from CSQ2, as STND.CXX.6 and STND.CXX.21 do; the second sentence of STND.STDC.29 rests on REPRO.7 and STND.CODE.4 and applies from CSQ3. STND.STDC.38 rests on INTPR.10 and applies from CSQ2, as STND.CONC.27 does. STND.STDC.33 and STND.STDC.35 state what a protocol uses under DSGN.15, not how its invariants are verified, and apply from CSQ3. The tests of STND.STDC.16 and STND.STDC.26 compare with a build of the same code, not with a reference oracle produced without it, and apply from CSQ3. STND.STDC.3, STND.STDC.4, the second sentence of STND.STDC.22, STND.STDC.23, STND.STDC.25, and STND.STDC.37 instantiate DSGN.3, rest on no row, and apply from CSQ3; the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 starts at CSQ0, stays with that row. STND.STDC.28 and the other defaults rest on no row and apply from CSQ3. No default raises the floor (GOV.11).

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
| STND.JL | Julia standard |
| STND.LEAN | Lean standard |
| STND.MPI | Message Passing Interface standard |
| STND.OMP | OpenMP standard |
| STND.PY | Python standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Provisions of STND.CXX

#### STND.STDC.1 C++ defaults applied to C

Default. Instantiates DSGN.1, DSGN.2, DSGN.3, DSGN.4, DSGN.15, DSGN.16, INTPR.1, INTPR.3, REPRO.2, REPRO.3, REPRO.7, SIMPL.6, RSRC.4, HW.5.

The C reading of each provision of STND.CXX that the table of this provision lists SHALL apply to the C source of the work of the class that its row gives and of each more severe class, each sentence keeping its modal and the provision its mode (DSGN.1, DSGN.2, DSGN.3, DSGN.4, DSGN.15, DSGN.16, INTPR.1, INTPR.3, REPRO.2, REPRO.3, REPRO.7, SIMPL.6, RSRC.4, HW.5). A project instrument MAY replace the C reading of one row by a recorded decision with an alternative that meets the same higher-level outcome, and keep the other rows (REPRO.7).

| Provision | Applies from | Change in its C reading |
| --- | --- | --- |
| STND.CXX.4 | CSQ3 | The options stated include each option that defines a behavior that the ISO C standard leaves undefined |
| STND.CXX.7 | CSQ2 | A type distinct from that of a pointer into host memory is a pointer to a distinct type, or a structure that holds the pointer; a type alias is not one |
| STND.CXX.9 | CSQ3 | None |
| STND.CXX.12 | CSQ3 | None |
| STND.CXX.15 | CSQ3 | Without the words reference, view, iterator, and C++ exception |
| STND.CXX.23 | CSQ3 | The type volatile std::sig_atomic_t is read as volatile sig_atomic_t |
| STND.CXX.24 | CSQ1 | The markers of an assumption are the unreachable marker of the edition in force, where it has one, and the builtins of a compiler |
| STND.CXX.25 | CSQ3 | Without the checks of the Core Guidelines and of the names of STND.CXX.14 |
| STND.CXX.26 | CSQ2 | None |
| STND.CXX.27 | CSQ1 | None |

#### STND.STDC.3 Lowered C editions recorded

Default. Instantiates DSGN.3, REPRO.7.

Other than in a change whose decision record names the compiler, the dependency, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain that requires it, a change SHOULD NOT lower the edition in force for a translation unit of C source (DSGN.3, REPRO.7).

### Failures

#### STND.STDC.2 C responses to listed failures

Binding. Instantiates PRIME.4.

A report of a condition that PRIME.4 lists through errno alone SHALL NOT be taken as passing that condition to the caller in a result under STND.CODE.14 (PRIME.4, STND.CODE.14).

#### STND.STDC.28 Stream errors before reliance

Default. Instantiates DSGN.1.

Before a result that code writes to a stream is reported or relied upon, the code SHOULD flush or close that stream, test the result of that call, and answer a failure that it finds as STND.CODE.14 and STND.STDC.2 provide (DSGN.1). Where code does not test the result of each write to a stream, it SHOULD also test the error indicator of that stream after that flush or before that close, and answer a failure that the indicator shows in the same way (DSGN.1).

#### STND.STDC.29 Library failure results diagnosed

Default. Instantiates DSGN.5, REPRO.7.

Where the means of the work include an attribute of the toolchain or a static check that diagnoses an ignored result, each function of the C library or of another dependency that reports in its result a failure of a kind that PRIME.4 lists SHOULD be called through a declaration, its own or that of a function of the work that wraps it, under which that attribute or check diagnoses each call that ignores that result (DSGN.5). Where the test of STND.STDC.28, or an error handler that ends the run, receives the failure of such a call, the call SHOULD carry at its location the suppression of STND.CODE.4, with its reason naming that test or handler (REPRO.7).

#### STND.STDC.30 Release failures tested

Default. Instantiates DSGN.1.

Before a result is relied upon, each failure that the release of an owned resource reports, other than the flush or close of a stream that STND.STDC.28 governs, and that affects that result, SHOULD be tested and answered as STND.CODE.14 and STND.STDC.2 provide (DSGN.1).

#### STND.STDC.31 C failure channel

Default. Instantiates DSGN.1, DSGN.14.

Each failure that the caller of a function is designed to handle SHOULD be reported by the return value of that function, or by an object that its contract names as its result for failures, as STND.STDC.2 binds for a listed condition (DSGN.1, STND.STDC.2). A nonlocal jump SHOULD NOT leave a function that holds an owned resource that it has not released (DSGN.14).

#### STND.STDC.32 Errno as a report of failure

Default. Instantiates DSGN.1.

Code SHOULD set errno to zero before each call of a library function that reports failure only through errno, and read errno for that call before another call that is able to change it (DSGN.1). Where a function reports failure in its result as well as through errno, code SHOULD read errno for a call of it only after that result indicates failure (DSGN.1).

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

Each integer division and remainder SHOULD have a divisor shown to be nonzero and, for signed operands, a dividend and a divisor shown not to be the most negative value of their type and minus one together (DSGN.1). Each shift SHOULD have a count shown to be at least zero and less than the width of its promoted left operand, and each left shift a left operand whose type after the integer promotions is unsigned, or a nonnegative value whose shifted result that promoted type represents (DSGN.1).

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

Where a compiler option defines, for a translation unit, a behavior that the ISO C standard leaves undefined, the argument for the correctness of the code SHOULD NOT rely on that option (DSGN.1). Where the work builds code under such an option, the tests of that code SHOULD also pass, within the tolerance of their acceptance criterion, in a build that is named apart as STND.BUILD.13 provides and that builds that code without the option (VV.1).

#### STND.STDC.40 Finite-value options in C

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9.

A translation unit of C source that holds a check of a floating-point value that STND.CODE.6, CPS.5, or CPS.9 requires SHALL NOT be compiled with an option that lets the compiler assume that floating-point values are finite (PRIME.4, DSGN.2, STND.CODE.21).

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

The format string of each call to a formatted input or output function SHOULD be a string literal, or a string that the code checks against the number and the types of the arguments of that call before the call (DSGN.2). Where the means of the work include a check of format strings against their arguments, the static checks of the work SHOULD diagnose each call whose literal format string does not match its arguments (DSGN.3).

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

Each object of variable-length array type with automatic storage duration whose number of elements derives from untrusted input SHOULD have that number checked, before its declaration, against a limit that its component states (DSGN.2, RSRC.1).

### Signals and threads

#### STND.STDC.33 Signal handler calls

Default. Instantiates DSGN.15, DSGN.14.

A signal handler SHOULD call only signal-safe functions (DSGN.15). A signal handler that calls a function able to change errno SHOULD restore, on each return, the value that errno held at its entry (DSGN.14).

#### STND.STDC.34 Computational exception signals

Default. Instantiates DSGN.1.

A handler of a signal that reports a computational exception, an invalid instruction, or an invalid access to memory SHOULD NOT return to the code that the signal interrupted (DSGN.1).

#### STND.STDC.35 Adjacent bit-fields shared

Default. Instantiates DSGN.15.

Where concurrent tasks access bit-fields of one structure, at least one of them by a write, the protection that STND.CONC.3 asks SHOULD cover each sequence of adjacent bit-fields as one shared mutable object (DSGN.15).

### Checking

#### STND.STDC.37 C warnings and detected behavior

Default. Instantiates DSGN.3.

Where a compiler of the toolchain matrix offers a diagnostic of a read of an object before its initialization, of a format string that does not match its arguments, of an ignored result of a function so declared, of a comparison of signed and unsigned operands, or of an implicit conversion that changes a value, the recorded set of warnings of the C reading of STND.CXX.25 SHOULD include that diagnostic (DSGN.3). The kinds of undefined behavior that the repository configuration lists under the C reading of STND.CXX.26 SHOULD include each kind that STND.STDC.8, STND.STDC.9, STND.STDC.10, STND.STDC.11, STND.STDC.12, STND.STDC.14, or STND.STDC.27 governs and that a detector among the means of the work detects at run time (DSGN.3).

#### STND.STDC.38 Stated limits of analysis

Default. Instantiates VV.1, INTPR.10.

The record of each verification that finds C code free of a kind of undefined behavior SHOULD state its means, and whether the documentation of that means states it as sound for that kind (VV.1, INTPR.10).

### Names

#### STND.STDC.39 C naming conventions

Default. Instantiates INTPR.1, INTPR.4.

Each name that the C source of the work declares SHOULD follow the naming convention that the repository configuration names (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
| 1.1 | 2026-10-25 | Minor amendment (GOV.41): STND.STDC.1 no longer lists STND.CXX.28, STND.CXX.30, and STND.CXX.31, whose outcomes STND.CODE.17, STND.CODE.19, and STND.CODE.20 now hold for every language, and drops VV.1, which only those rows needed; STND.STDC.2, retitled C responses to listed failures and moved to the section Failures, replaces its table of the C readings of STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29 by the one change that C needs, that a report of a listed condition through errno alone is not taken as passing it to the caller in a result under STND.CODE.14, and instantiates PRIME.4 alone; it keeps its identifier for the errno clause of its own table, and no identifier is given to another provision; new STND.STDC.40 (binding, PRIME.4) states in C words the row of STND.CXX.18, the option that assumes finite values, which the table of STND.STDC.2 held; the C readings of STND.CXX.16, STND.CXX.17, and STND.CXX.29 give way to STND.CODE.14, STND.CODE.15, and STND.CODE.18; STND.STDC.28 and STND.STDC.30 cite STND.CODE.14 and STND.STDC.2 in place of the C reading of STND.CXX.16, and STND.STDC.31 cites STND.STDC.2 for a listed condition; new STND.STDC.39 (default, from CSQ3) leaves the convention of names to the repository configuration and keeps the names that the notation of NUMER.4 fixes, the rule of decision 9 of 2026-10-24; Terms import Untrusted input, Execution setting, High-assurance code, and High-assurance coding standard from STND.CODE and delete this standard's own definition of Untrusted input, which gains the reach of the interface for outside use that the documentation or the repository configuration names; the Notes cite STND.CODE for the shared rules and for the reasoning on the assert macro, give the C facts, the nonlocal jump, the check of a pointer argument without an extent, and the reason for the naming rule, and restate the floor argument for STND.STDC.2 and STND.STDC.40. |
| 1.2 | 2026-10-27 | Minor amendment (GOV.41): STND.STDC.36 is withdrawn, its outcome being STND.CODE.22 and STND.CODE.23 for every language, and the front matter lists it as withdrawn; Terms import Foreign interface from STND.CODE and drop this standard's own definition; the Purpose drops STND.STDC.36 and names STND.CODE.22 to STND.CODE.26; the Notes cite STND.CODE.23 and STND.CODE.24 in place of STND.STDC.36 and STND.CXX.22, and drop STND.CXX.20 from the provisions of STND.CXX that do not carry to C. |
