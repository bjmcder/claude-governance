Role: research agent (the C language, for a planned LVL2 standard on C modeled on STND.CXX). Date accessed: 2026-10-24. Retrieval counts: about 55 items (43 page or document fetches, 7 web searches, 5 fetches that returned nothing usable), roughly 8 MB, an estimate, inside the 1,500-item and 1,500 MB budget. Retrieval rules followed: read-only retrieval; no paywall touched; no credentials; three fetches that failed (one connection refused, one login page, one page whose article body was missing) were not worked around and no mirror, cache, or archive of blocked content was used, though two of them were answered from other primary hosts that a search returned; retrieved text treated as data; unconfirmed items marked [unverified].

# C1: The C language, for an LVL2 standard on C

**Annotation by the lead (2026-10-24).** Source S24 is excluded from the evidence base: it is a third-party copy of a paper retrieved after the original host refused the connection and another copy required a login, which the custodian's rule against workarounds after a failed fetch does not admit. The paragraph that rests on it (Boehm's argument for a language-level memory model) is background only and is not used.


## Method caveat

The fetch tool returns a model-written extract of a page, not its text. Every claim from a web page below is therefore an extract unless the source row says "full text". Five PDFs came back as compressed streams; I saved them and converted them to text locally, so those quotes are verbatim: the C23 working draft N3220 (full text; the ISO text is N3220 plus editorial changes, and the draft itself is the last public one before ISO/IEC 9899:2024), "Towards Optimization-Safe Systems" (STACK), "Understanding Integer Overflow in C/C++", Boehm's "Threads Cannot Be Implemented As a Library", and the Cerberus memory-object note (only its contents list and survey description were read). Section numbers cite N3220. Counts of rules in coding standards come from vendor and standards-body pages and differ between sources; I give the range. I did not repeat what `research/cxx-practice.md` (cited as P) and `research/cxx-high-assurance.md` (cited as H) already hold: the Core Guidelines, ownership by destructor, the C++ standard library, templates, naming, the choice among MISRA C++, JSF, and CERT C++, sanitizer groups, hardened library modes, and the rule that the edition is the newest supported one outside high assurance (P section 7, H section 4.2). Where a C matter reduces to one of those, I cite it and add only the C difference. Vendor and tool names appear only as evidence of a hazard or as an example.

## Answer in brief

Each practice is stated as an outcome that a tool or reviewer decides. Brackets give the sources of the sources table; "corpus" means the provision named in the section "What the corpus already holds".

1. Each translation unit is built at a stated edition of the C standard with compiler extensions off, and the build stops if the compiler lacks the edition. The default dialect of at least one widely used compiler enables its extensions, "even when those features change the meaning" of the base standard. This is STND.CXX.2 and .4 read for C. [S2, S3, corpus]
2. No signed integer operation overflows, and no correctness argument rests on a wrapping option. Operands from outside the function have a range established before the operation, or the operation is a checked one (C23 adds a checked-arithmetic header). A test for overflow is itself written without overflow. [S1, S5, S6, S7]
3. Every array access and every pointer arithmetic result lies inside the object, established by a check that precedes the access or by an argument recorded at the access. A pointer that crosses an interface travels with its extent, in a structure or a paired parameter that the interface documents. [S1, S4, S9, S10]
4. No pointer is used after the end of the lifetime of the object it designates. Each allocation has one stated owner at each point, and the contract of each function says who releases what it returns or keeps. [S1, S8, S9, S10]
5. Every object is initialized before it is read, and an object whose bytes leave the process (a structure written to a file, a socket, or a buffer) has had its padding set. A read of an indeterminate value is a defect even where the standard does not call it undefined. [S1, S2, S11]
6. An object is accessed only through an lvalue of a compatible type or a character type. Reinterpretation of representation goes through a copy of the bytes or a union, as the edition states. A project that compiles with the aliasing assumption off declares it as a build setting, and the code is still correct without that option. [S1, S4, S12, S3]
7. No expression modifies a scalar twice, or modifies and reads it, without a sequencing relation. A compiler or analyzer diagnoses the common forms, and the rest fall to review. [S1]
8. Every shift has a count in the range of zero to one less than the width of the promoted left operand, and a left shift of a signed value is replaced by an operation on an unsigned value. [S1, S5]
9. Each implicit conversion that can change a value is replaced by an explicit one with a range argument, and no comparison mixes signed and unsigned operands. Sizes, counts, and indexes have the unsigned size type or a type shown to hold them. A size computed for an allocation is checked for overflow before the call. [S5, S6, S13, S14]
10. Division and remainder have a divisor shown nonzero, and the quotient of the most negative value by minus one is excluded. [S1]
11. Each function that acquires more than one resource releases every one it holds on every path out of it, error paths included, in an order stated once. A pattern with one exit region per function, or a wrapper that owns the release, meets this. A release that can fail and affect a result returns its failure to the caller. [S15, S13]
12. Each function that can fail reports the failure in its result, and a compiler or analyzer diagnoses each call whose result is ignored. A list of library functions whose results are ignorable is short, stated, and justified by the standard's own text. [S13, S16, corpus]
13. `errno` is set to zero before a library call that signals only through it, read immediately after the call, saved and restored by a signal handler, and never taken as evidence of success. [S1, S17]
14. Every string or buffer operation has a destination size that the code knows and tests, a termination that the code establishes, and a truncation that is a detected failure. A function that cannot bound its write is not called on external data. [S15, S13, S18]
15. A format string is a constant or has been checked against its arguments, and the compiler diagnoses a mismatch. [S19]
16. A macro with side effects in its arguments, a macro that evaluates an argument twice, and conditional compilation that no test configuration builds are each absent or recorded. Constants and small functions replace macros where the language allows. [S13, S14]
17. A pointer qualified `restrict` has a contract that states which ranges do not overlap, and a test or an entry assertion checks it. A violation is undefined behavior, and removing the qualifier from a conforming program leaves its meaning unchanged, so a run without it is a check. [S1, S20]
18. No variable-length array object has automatic storage with a size from untrusted or unbounded input; where one is used, its bound is checked before the declaration. Pointers to variably modified types as parameters are allowed in the edition that makes them mandatory. [S1, S15, S21]
19. A signal handler assigns to `volatile sig_atomic_t` or lock-free atomic objects, calls only functions that the platform lists as async-signal-safe, restores `errno`, and leaves its work to the interrupted code. [S1, S22, S23]
20. Code that runs in more than one thread is free of data races as the C memory model defines them, orders conflicting accesses by atomics or by library synchronization, and treats a bit-field and its neighbors as one location. Sequentially consistent ordering is the default, as STND.CONC.4 asks. [S1, S24, S25, corpus]
21. Where C threads and a platform's own thread library exist together, one object is not synchronized by both unless the platform documents that the two cooperate. The optional threads and atomics of the language are tested for in the build. [S1, S25]
22. Each interface to another language fixes the widths, layouts, and order of dimensions of what it exchanges, states ownership and lifetime for each pointer, passes no exception or jump across it, and checks every status return. [S26, S27, corpus]
23. The high-assurance coding standard that a decision record adopts covers the edition in force, and the record states what a checker covers and what it does not. A standard whose published coverage ends below the newest edition fixes the edition, as STND.CXX.30 provides. [S28, S29, corpus]
24. The tests of each change run in a build that detects invalid memory access and the kinds of undefined behavior that the repository configuration lists, and fail at the first detection. A detector that also reports defined behavior (unsigned wraparound, implicit conversion) is run with each accepted report suppressed at its location. [S30, S31, corpus]
25. Static analysis for C is run as a bug-finder whose result is not a proof; a claim that code is free of a class of defect names the sound means that supports it. [S32, S33, corpus]

## Undefined behavior that matters in practice

The C23 text lists 221 circumstances of undefined behavior in its overview annex (J.2), and says that annex "gives an overview" of the matter [S1, full text]. Earlier editions listed fewer [unverified]. A reader of the standard cannot hold that list in mind, and no one needs to: the classes below cause most of the defects that the studies of the section "Studies of C defects" count.

The compiler is allowed to assume that none of these happens. An optimizer then removes code that is correct only if it does. The consequences are not local and not in the order of the source: the LLVM author's account gives the examples that a test of `x + 1 > x` becomes constant true, that a loop bound with a signed counter lets the compiler assume a trip count, that a null dereference earlier in a function lets later null tests go, and that a type-based aliasing assumption turns a 10,000-iteration float loop into one `memset` [S4, extract]. The same account says that the language does not define a trap for these cases, so a crash is not a guaranteed symptom. Checks that rely on the undefined operation itself are the common casualty: a test `buf + len < buf` for pointer wraparound is removed because the wrapped pointer is undefined, and a fragment of this form appeared in several code bases [S6, full text].

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
| --- | --- | --- | --- | --- | --- |
| Signed overflow | An exceptional condition during evaluation is undefined (J.2 item 35); unsigned arithmetic is defined | Overflow checks written as arithmetic are deleted; loop counters mis-optimized; a size wraps and a small buffer is allocated | Range established before the operation, or a checked operation; unsigned for wraparound that is meant (practice 2) | S1, S4, S5, S6 | The rule holds in every edition. Two's complement became the only representation in C23, but overflow stayed undefined. |
| Out-of-bounds access | Subscript outside the array, pointer arithmetic leaving the object and one past, and pointer subtraction across objects are each undefined (J.2 items 43 to 47) | The leading class of memory-safety defects: an out-of-bounds write and read rank 5 and 8 in one weakness ranking of 2025, a stack overflow, a heap overflow, and a classic copy without a size check rank 14, 16, and 11 | Pointer with extent at every interface; access guarded by a check that precedes it (practice 3) | S1, S9, S10, S34 | Holds in every edition. Rankings move; the class does not. |
| Use after free and use of a dead object | A pointer to an object whose lifetime ended has an indeterminate value; using it is undefined (J.2 items 9, 10, 183, 184) | Dominant class of exploited flaws: 17 of 39 memory-corruption zero-days in one count; about half of the memory-safety bugs in one browser project | One owner per allocation; release sets the owner's pointer to null where the owner persists; a sanitizer in tests (practices 4, 24) | S1, S8, S9, S10, S30 | Holds. The counts are specific to their years. |
| Uninitialized read | An automatic object has an indeterminate initial representation (6.2.4). A read of one eligible for `register` is undefined (J.2 item 20); other reads are unspecified or a trap representation. Compilers treat both as license. | Garbage values; disclosure of stack and padding; branches removed | Initialize at the point of declaration; set padding before output; an option that initializes automatic storage is a defense, not a reason to skip initialization (practice 5) | S1, S4, S3, S11 | The text is stable. The option exists in some compilers only. |
| Strict aliasing | A stored value accessed through an lvalue of an incompatible type is undefined (J.2 item 36; effective type, 6.5.1) | Reordered or removed loads and stores after a pointer cast; one compiler enables the assumption at its middle optimization level and above | Copy bytes or use a union; character access is always allowed (practice 6) | S1, S3, S4 | The rule is stable. Whether a given idiom works is a compiler question; the survey of C programmers found that practice and the standard differ in many cases. |
| Sequence points | Two unsequenced side effects on one scalar, or a side effect and a value use, are undefined (J.2 item 34) | Different results at different optimization levels or compilers | One side effect per full expression (practice 7) | S1 | Holds. The C11 wording uses "sequenced before"; the C89 wording used "sequence points"; the rule is the same in effect. |
| Shifts | Count negative or at least the width, and a signed left shift that overflows, are undefined (J.2 items 48, 49) | A shift by the width gives a hardware-dependent value; a mask built by shifting is wrong on one target | Counts in range; unsigned operand (practice 8) | S1, S5 | Holds. |
| Division | Zero divisor and a non-representable quotient are undefined (J.2 items 41, 42) | A trap on one target and a wrong value on another; a published database test for overflow in signed division was removed by the optimizer | Divisor tested first (practice 10) | S1, S6 | Holds. |
| Data race | A conflicting pair of non-atomic accesses in different threads with no happens-before relation is undefined (5.1.2.5) | Torn values, lost updates, a compiler that introduces a store (adjacent fields) | Atomics or library synchronization (practices 20, 21) | S1, S24 | Holds from the edition that has threads. Before it, the platform library defined the rules and the language did not. |
| Restrict violation | An object modified through a restricted pointer is also reached by another pointer: undefined (J.2 items 65, 66) | Vectorized or reordered code that reads stale values | Contract and check (practice 17) | S1, S20 | Holds since the edition that added `restrict`. |

Two further points are specific to C. First, the standard has no defined semantics for pointer provenance beyond the effective-type text. A university group asked about 323 C programmers in a survey (255 of them in systems programming) which idioms they expect to work and found that practice, compiler behavior, and the text of the standard do not agree on provenance, uninitialized values, padding, and effective types [S11, extract of the survey description]. A provenance-aware memory object model has been issued as a technical specification (ISO/IEC TS 6010:2025, status from a third-party registry [unverified]). A standard on C should therefore not claim a code idiom is correct because one compiler accepts it. Second, a project may tell a compiler to define some of these behaviors. The Linux kernel builds with the aliasing assumption off, with signed overflow treated as wrapping, with the null-check removal off, and with automatic variables initialized [S3, S12, extract]. That is a project decision recorded in a build file, which is the shape STND.CXX.4 already asks for.

## Resource management without destructors

C has no destructor, so a resource handle in the sense of STND.CXX (an object whose type releases the resource) does not exist in the language. Ownership is a convention that code and contract carry. The practices that follow from this are three.

First, the contract of each function states who owns what crosses the interface (STND.CXX.15 already asks for the owner and period of validity, and applies unchanged). Second, each function that acquires resources has one place where it releases them. The Linux kernel's coding style gives the reasons for centralized exit through `goto`: unconditional statements are easier to follow, nesting is reduced, an error from not updating each exit point after a change is prevented, and the compiler is saved from optimizing away redundant code. It says to name the labels for what they do (`out_free_buffer`), not `err1` [S15, extract]. Labels in reverse order of acquisition release what has been acquired and fall through to the next. A wrapper function that owns the release and takes a callback or a table of acquired items meets the same outcome. Some compilers offer a cleanup attribute on a variable as an extension; the C2y work includes a `defer` technical specification that was on the committee's agenda in 2026 [S35, unverified in detail]. Neither is part of the language as published, and a standard that is edition-agnostic should state the outcome (release on every path) and not the mechanism. Third, a function whose release can fail returns that failure (the close of a file on a full disk, for example); STND.CXX.21 already asks for it and applies to C unchanged.

Two traps are C-specific. The return of `realloc` assigned to the only pointer loses the block on failure; a test for it is in the CERT rule on library errors [S13]. A zero-size `realloc` became undefined behavior in C23 [S1, M.2]. Allocation sizes computed as `count * size` wrap; the kernel's deprecation list names this and requires two-factor allocators or overflow-checked helpers [S21, extract].

## Error reporting and ignored returns

The standard library reports failure by return value, by `errno`, by a stream's error indicator, or by nothing. The text of C23 on `errno` (7.5) says its value at startup is zero, a library function may set it to nonzero whether or not an error occurred unless the function documents its use, and a library function is not required to set it to zero [S1, full text; 7.5 paragraph 3]. The consequences are the practice 13 items. `errno` is thread-local on platforms with threads (the standard requires one per thread [unverified in the text I read]).

An ignored return is the commonest route from a small defect to a large one. The CERT rule on library errors classes the severity High and the likelihood Likely, and shows five cases: an unchecked `calloc` result used as a pointer, a failed `fseek` before a read, a failed `snprintf` leaving an unterminated buffer, a `realloc` result assigned over the only pointer, and an unchecked `setlocale` [S16, extract]. The same rule lists functions whose results may be ignored (the `printf` family to `stdout`, `memcpy` and `memset`, and others) and a conditional exception for writes to `stdout` or `stderr` by cast to `void`. A standard for LVL2 cannot copy that exception list: STND.CODE.7 forbids discarding a failure of a kind PRIME.4 lists, and STND.CODE.12 asks for a reason at each other discard. The exceptions of the CERT rule then become cases for STND.CODE.12, not an exemption. C23 adds the `nodiscard` attribute (6.7.13) and the older compilers have an equivalent extension attribute and a warning for it (`-Wunused-result` for the function attribute `warn_unused_result`) [S1, S36]. STND.CXX.17 asks for exactly that diagnosis; it carries to C with the C attribute.

## Strings and buffers

A C string is a pointer to bytes ended by a zero. The language gives it no length, so each operation either trusts the termination or needs a separate size. The kernel project has removed `strncpy` (it does not terminate, and it pads the destination), deprecated `strcpy` (no bound), and replaced `strlcpy` (it reads the whole source first, so an unterminated source causes an over-read) with its own function that terminates and reports truncation [S21, extract]. The C11 bounds-checking interfaces (Annex K) were an attempt at a standard fix. Two engineers who deployed them reported that adoption was more intrusive than expected, the error paths are hard to test, one process-wide handler suits threaded programs badly, no complete conforming implementation had emerged, and the common library did not ship them; they proposed removal. The interfaces are still optional in C23 [S37, extract; S1]. The outcome that a standard should state is practice 14, and the means (a length-carrying type, a checked copy, a function chosen by the project) are the project's.

The `gets` function was removed in C11 (M.4) because it cannot bound its write [S1]. The Heartbleed flaw in a TLS library (CVE-2014-0160) was a read of memory beyond a received message, present from 2012 until 2014; the source page calls it a programming mistake and says it leaked keys and passwords without trace in logs [S38, extract]. It is a case of practice 3: a length taken from the input and not checked against the object.

## Integer conversions and promotions

C promotes any integer type narrower than `int` to `int` (or unsigned) before arithmetic, and converts operands of mixed signedness to the unsigned type of the same or greater rank (6.3.1.1, 6.3.1.8). Three kinds of defect follow: a narrow unsigned operand promoted to signed `int` and then overflowed or shifted; a signed value converted to an unsigned one in a comparison and so made large; and a value truncated when stored in a narrower type with an implementation-defined result. The empirical study of integer overflow found over 200 distinct locations in one benchmark suite where overflow occurs, with all four combinations of intentional and unintentional, defined and undefined, common in real code; it found and reported undefined overflows in about a dozen mature projects and cites a truncation in a 1996 flight failure [S5, full text]. The consequence for a standard is that the compiler warnings and the detectors cannot be a simple "no overflow" check: intentional wraparound exists, and a project marks it (practice 9, practice 24). C23 adds checked-arithmetic functions (`<stdckdint.h>`) and bit-precise integer types, and removes the sign representations other than two's complement [S1, M.2].

## The preprocessor

The preprocessor is text substitution before the compiler sees the program. The hazards are a macro that evaluates an argument twice, an unparenthesized expression, an include order dependence, and conditional compilation whose branches no test builds. High-assurance C standards restrict it (the Power of 10 rules ask for a limited preprocessor, per H section 3.4). C23 adds `#embed`, `#elifdef`, `#warning`, `__has_include`, and `__VA_OPT__`, and `constexpr` objects and `static_assert` as keywords, so more of what macros did is a language facility [S1, M.2]. STND.CXX.12 (checking at compile time) carries to C through `static_assert`. C has no template, so STND.CXX.11 to .13 do not apply; type-generic code uses `_Generic` and macros, and a standard may ask that each such facility carry its meaning and a test, as STND.CXX.13 asks of a metaprogramming facility (a drafting decision).

## Restrict, variable-length arrays, and the library's conditional features

`restrict` is a promise by the programmer, not a check: if an object accessed through the restricted pointer is modified, every access to it in the block goes through that pointer, and a violation is undefined. The qualifier changes no conforming program's meaning, and `memcpy` has restricted parameters where `memmove` has none [S20, extract; the library point is the extract's own background note, [unverified] against the text]. Variable-length arrays came in C99, became a conditional feature in C11 (`__STDC_NO_VLA__`), and in C23 only the variably modified type (a pointer to a VLA, a parameter of such a type) is mandatory, not the automatic VLA object [S1, 6.10.10.4 and M.2]. The kernel project removed stack VLAs, citing worse machine code and a stack that can grow past the segment [S21, extract]. The conditional features also include complex numbers, atomics, and threads, each with a `__STDC_NO_...__` macro [S1].

## Signals

The language says that a signal handler may refer to an object of static or thread storage duration only if it is a lock-free atomic object or is assigned as `volatile sig_atomic_t`, and may call only a short list of library functions; any other use is undefined (7.14.1.1). A handler that returns after SIGFPE, SIGILL, or SIGSEGV is undefined [S1, full text]. The platform layer adds a longer list of async-signal-safe functions. The reference text says stdio is unsafe because of shared buffers and that a handler must save and restore `errno` [S22, extract]; the POSIX list defines the set that "shall be" safe and says other functions "may be unsafe" [S23, extract]. A static analyzer for C can flag a call in a handler to an unsafe function [S32]. STND.CXX.23 already states the outcome for C++ (lock-free atomic or `volatile std::sig_atomic_t`); the C form names the C types. STND.CONC.17 forbids a library from changing signal handling of the process, and STND.OMP.22 and STND.MPI.10 already carry the rule into their models.

## The C11 memory model, atomics, threads, and POSIX threads

The C11 edition added a memory model and optional `<stdatomic.h>` and `<threads.h>` [S1, M.4]. A data race is undefined behavior, and a program free of races that uses only mutexes and sequentially consistent atomics behaves as an interleaving (5.1.2.5, notes 17 and 18) [S1, full text]. Plain loads and stores of atomic objects default to the sequentially consistent order (6.2.6.1 note). Weaker orders are available; consume ordering is defined in the text, but I have not verified the statement that it is discouraged or little implemented [unverified]. STND.CONC.4 already asks for sequential consistency or a stated reason, and it applies to C.

The older argument for a language-level model is Boehm's, written when C threads were a library of a platform: a compiler that does not know of threads may introduce a store to an adjacent field, promote a shared variable to a register around a call, and move a store across a lock call, and none of this breaks the single-threaded standard. His examples are a bit-field update implemented as read-modify-write of the whole word, and a loop with a conditional lock whose variable is promoted to a register [S24, full text]. C11 answered by defining memory locations, with distinct members and bit-fields in separate locations except adjacent bit-fields (3.x note) [S1]. The consequence for a project is that two threads may write adjacent bit-fields only under one lock.

The relation to POSIX threads is that POSIX lists the functions that synchronize memory, and the list includes both the pthread and the C11 forms (`pthread_mutex_lock` and `mtx_lock`, `pthread_once` and `call_once`, the create and join functions of each), and says that applications shall ensure that no thread reads or modifies a location another is modifying, with an unspecified synchronization on an error return [S39, extract]. The C23 text mandates `call_once` and keeps the threads header optional [S1]. Practice 21 follows. Whether a mutex of one library can be used with the condition variable of the other is a question for the platform's documentation [unverified].

## Interfaces to other languages

C is the common binary interface of most languages on a platform, which makes its hazards the hazards of every foreign interface. The C-specific parts are these. A Fortran caller sees reversed order of dimensions (`A(n,m)` is `A[m][n]`), one-based indexes, and no unsigned types or variadics; the interoperability is declared with `BIND(C)` and the kind parameters of its binding module [S26, extract]. A Python extension holds references with counted ownership (new and borrowed), a limited API and a stable binary interface that keep compatibility across minor releases, and the page advises testing against every minor version [S27, extract]. The model-language standards of the corpus already say what a C program does at these edges: STND.CXX.20 and .21 (hand a resource to an owner before the next failing call; call a status-returning function through a checked wrapper), STND.CXX.22 (no exception across), and the MPI and OpenMP standards for their C bindings. A C standard adds that no `longjmp` crosses a foreign frame (the C standard defines its use only within C) [unverified in the text] and that a callback that C code passes to a foreign runtime does not let a jump or a termination escape.

## Editions

| Edition | `__STDC_VERSION__` | What moved or was removed (from M.2 to M.6 of the draft) |
| --- | --- | --- |
| C89/C90 | not defined | Base language. An amendment in 1995 added the version macro (199409L), digraphs, and wide characters. |
| C99 | 199901L | Added `restrict`, VLAs, `long long`, `inline`, designated initializers, compound literals, `//` comments, mixed declarations and statements, fixed-width types, `snprintf`, complex, `<fenv.h>`, the effective-type aliasing rules; removed implicit `int` and implicit function declaration. |
| C11 | 201112L | Added a memory model, `<stdatomic.h>`, `<threads.h>`, `_Static_assert`, `_Noreturn`, alignment, Unicode strings, anonymous members, optional bounds-checking and analyzability annexes; made several C99 features conditional (VLAs, complex, threads, atomics); removed `gets`. |
| C17/C18 | 201710L | Defect corrections only. |
| C23 | 202311L | `bool`, `true`, `false`, `static_assert`, `thread_local` as keywords; `nullptr`; `constexpr` objects; `typeof`; `auto` inference; attributes (`nodiscard`, `deprecated`, `fallthrough`, `maybe_unused`, `noreturn`, `reproducible`, `unsequenced`); `unreachable`; `<stdckdint.h>`; `<stdbit.h>`; `_BitInt`; `#embed`; empty initializer; two's complement only; function definitions with identifier lists (K&R) removed; empty parameter list means `(void)`; zero-size `realloc` undefined; `free_sized`; `memset_explicit`; variably modified types mandatory; trigraphs no longer in the text (the draft contains no trigraph entry; the removal is not in its change list [unverified as a stated change]). |
| C2y | in development | Next edition under way in 2026; a `defer` specification and further work were on 2026 agendas [S35, unverified]. |

A compiler's name for the newest edition has changed between releases (`c2x` deprecated for `c23`) and the default of a compiler is a dialect with extensions, not an edition [S3]. This is why STND.CXX.4 asks that the repository state the edition, and why the edition should be named by the standard it denotes and the macro value it defines, not by a compiler flag.

## High-assurance coding standards for C

| Item | MISRA C | CERT C | Other |
| --- | --- | --- | --- |
| Current text | MISRA C:2025, March 2025, described as an incremental update to the 2023 third edition, second revision [S28, S29] | The 2016 edition, with a wiki that is a work in progress [S40, extract] | JPL's C standard, with six compliance levels, and the Power of 10 (H section 3.4) |
| C editions covered | C90, C99, C11 and C18 per the publisher and a tool vendor; C23 not covered, a later edition is expected to add it [S29, S28] | C11 and earlier including C99 [S40] | Not retrieved |
| Size | 223 guidelines in two vendors' tallies (22 directives, 201 rules; 22 mandatory, 153 or 154 required, 47 advisory), 224 or 225 in others [S29]. Counts differ by how deleted and disapplied guidelines are counted. | 17 rule categories and 17 recommendation categories (preprocessor, declarations, expressions, integers, floating point, arrays, strings, memory, I/O, environment, signals, error handling, API, concurrency, miscellaneous, POSIX, Windows); per-category rule counts not retrieved [S40] | |
| Cost | Paid, single named-user license, on-screen only, not shareable [S28] | Free to read [S40] | Free |
| Checks | Commercial analyzers state coverage; counts of decidable rules not retrieved | Rules carry severity, likelihood, and remediation cost; the rule on library errors is rated High and Likely [S16] | |

Both are suited to adoption by decision record as STND.CXX.28 asks, because neither requires the corpus to name a version. The coverage of the edition is the one hazard that differs from C++. If the newest edition is C23 and the adopted standard covers C18, STND.CXX.30 applies as written: the edition in force for high-assurance code is the covered one, unless a decision record admits a feature of the later edition. MISRA C:2012 had 143 rules and 16 directives [unverified, from background]. The rules in all of these standards restrict dynamic memory, recursion, unbounded loops, `goto` in some, the preprocessor, and unions in the same way as the C++ ones that H section 3 describes, so the observation in the Notes of STND.CXX that conformance reduces undefined behavior mechanically and is not evidence of correct results holds unchanged for C.

## Sanitizers, static analysis, and warnings, stated as outcomes

A run-time detector for address errors reports out-of-bounds access to heap, stack, and globals, use after free, use after return, use after scope, double free, and (experimentally) leaks; its slowdown is about twofold and its memory use higher, and its documentation says it is a bug-detection tool, not for production [S31, extract]. A detector for undefined behavior has checks for signed overflow, shifts, bounds of arrays whose size is known, null, alignment, unreachable code, a VLA bound that is not positive, invalid enum and bool values, and pointer overflow; unsigned overflow, implicit conversion, and float division by zero are outside the default group, and each reports defined behavior that is often unintended [S30, extract]. Checks can also be built to trap with no runtime library. The compiler warnings that bear on C: uninitialized use, array bounds, format strings, shadowing and implicit fall-through, strict-aliasing, shift overflow, null dereference on a path, and ignored results of marked functions; one compiler's overflow warning has been a no-op for years and is kept for compatibility [S41, extract], so a project does not take its silence as evidence. A compiler's analyzer for C finds double free, use after free, leaks of memory, streams, and descriptors, null dereference, uninitialized values, tainted sizes and indexes, and unsafe calls in a signal handler; its documentation calls it neither sound nor complete, much more costly than ordinary warnings, and in that release suitable for C only [S32, extract]. A deductive verifier proves contracts written in a specification language for C by weakest-precondition computation, and an abstract-interpretation plug-in contributes [S33, extract]. These give the outcomes of practices 24 and 25. The outcome of a check is stated; which check delivers it is the repository configuration's choice (STND.CXX.25 to .27 apply).

## Studies of C defects and vulnerabilities

- A count of 912 high or critical severity bugs since 2015 in one browser project found about 70 percent memory-safety problems, half of them use after free [S10, extract].
- One vendor reports that about 70 percent of the vulnerabilities it assigns a CVE each year are memory safety issues [S9, extract; the class breakdown is not on the page].
- A review of 58 zero-day vulnerabilities exploited in the wild in 2021 found 39 (67 percent) memory corruption: 17 use after free, 6 out-of-bounds read or write, 4 buffer overflow, 4 integer overflow [S8, extract].
- The share of memory-safety flaws in one mobile operating system fell from 76 percent in 2019 to 35 percent in 2022 (223 to 85 a year) as new native code moved to a memory-safe language; the vendor said that correlation is not shown to be cause [S42, secondary search result; the primary post's body was not retrievable].
- A 2025 ranking of weaknesses by frequency and severity lists out-of-bounds write fifth, use after free seventh, out-of-bounds read eighth, buffer copy without size check eleventh, null dereference thirteenth, stack overflow fourteenth, and heap overflow sixteenth [S34, extract].
- A static checker for code that the optimizer may discard found 160 new bugs confirmed and fixed in systems including the Linux kernel and a database, and estimated that unstable code exists in 40 percent of 8,575 Debian packages with C or C++ code (3,471 had a report) [S6, full text].
- The integer-overflow study (above) found undefined overflow in mature projects [S5, full text].
- A US agency's guide advises new product lines in critical infrastructure to use memory-safe languages where alternatives are readily available, and existing C and C++ products to publish a memory-safety roadmap; it applies to products that have no announced end of support before 2030 [S43, extract].

These numbers show the classes and their order. They do not support a claim of a rate for any one project; the methods differ. The corpus does not need them for a provision, since PRIME.4, DSGN.2, and DSGN.14 already require what the practices ask; they serve as the argument in the Notes of the standard.

## Timeless versus moving

Timeless: the classes of undefined behavior and their effect on an optimizer; the absence of destructors and the need for one release region per function; return-value and `errno` conventions; the null-terminated string and the need for a size; promotions and conversions; the preprocessor as text; the data-race definition; async-signal safety; the C ABI as the junction of languages; the idea that a coding standard restricts the language and records deviations.

Moving: the edition and the set of attributes and library functions (C23 added many; C2y will add more); which features are conditional (VLA objects, threads, atomics, complex, Annex K); the edition coverage of each coding standard (MISRA's coverage ends below C23 in the sources I read); the status of the provenance specification and of `defer`; compiler options that initialize automatic storage or define wraparound; tool coverage and the rankings of weakness classes. A provision should state the outcome, name the edition by what the project's repository configuration states, and leave these to it.

## What the corpus already holds

The drafter restates none of these.

STND.CXX provisions that apply to C unchanged, by content (the word "C++" replaced by "C"):
- STND.CXX.2, .3, .4: edition in force, agent edition changes, stated build settings. The terms Translation unit, Toolchain matrix, and Edition in force carry over. The extension-off rule of .4 needs a C wording because the default dialect of a major compiler enables extensions that change meaning [S3].
- STND.CXX.15: the declaration comment states the owner and period of validity of each pointer returned or kept, each error value, and whether concurrent calls are safe. This is the ownership contract that C needs most.
- STND.CXX.16: the listed responses, except "throw a C++ exception", which does not exist in C. C answers with return, halt, safe state, and visible degradation.
- STND.CXX.17: ignored results diagnosed; the C form uses the C attribute of the edition or a compiler's equivalent. The Notes of STND.CXX.17 say a cast to `void` discards, which STND.CODE.7 forbids for listed failures; the CERT exception list therefore needs a decision.
- STND.CXX.18: no check removed by an option. For C the removal mechanism is `NDEBUG` and optimization on undefined behavior, and the floating-point option on finite values is the same.
- STND.CXX.19: failure channel. C has no exception, so the sentence on exceptions disabled does not apply; the first sentence becomes the return value as the one channel.
- STND.CXX.21: status and release failures, with the destructor sentence dropped.
- STND.CXX.23: synchronization of shared state, with the C types named.
- STND.CXX.24: compiler assumptions. C23's `unreachable` and the compiler builtins fall under it.
- STND.CXX.25 to .27: static checks, run-time detection at first detection, and library checks in production. The third applies to a C library that offers fortify-style checks.
- STND.CXX.28 to .31: the high-assurance provisions apply nearly as written, since they refer to "the high-assurance coding standard that a decision record adopts". The term High-assurance coding standard says "for C++" and needs the C wording.

STND.CXX provisions that do not carry: .5 (destructor), .6 (views and ranges; C has no standard view type, so the rule is a structure with a pointer and a length or a paired parameter), .7 (device and register memory; the register layer idea carries but `volatile` access is the C form), .8 to .10 (standard library first; library-defined behavior; header-only delivery), .11 to .13 (templates and metaprogramming), .14 (naming table for C++ kinds), .20 (resource handle: no type owns a resource in C, so the outcome is practice 11), and .22 (exceptions into C frames, which is a rule the C++ side obeys; the C side needs only that no jump crosses).

Other documents:
- STND.CODE: .3 (contracts at declarations), .4 (static checks), .5 (layout), .6 and .7 (binding: unremovable input checks and discarded failures), .12 (reasoned discards), .13 (blocks by step).
- STND.CONC: .1 and .2 (binding), .3 to .6 (protection, ordering, publication and lifetime, concurrent calls in contracts), .7 to .9 (locks), .12 (parent-owned tasks, relevant to thread join), .17 (library leaves signal handling unchanged), .19 (child processes of threaded programs: the POSIX `fork` hazard is the C case), .25 (race detection in tests).
- STND.DEPS: .1 to .5 (selection, thin support, revision, review, contract tests), .6 and .7 (binding), .8 (compiler revision recorded as an input; applies to every C compiler), .11 (incorporated external code, where C projects often copy a library).
- STND.DOCS: .9 table, .13 (checked examples), .12 (one name per concept).
- NUMER: .11 (tolerance basis), .12 (rounding), .16 and .17 (approximations and performance approximations; the C relevance is fast-math style options and `restrict`-enabled reordering).
- HW.CPU: .3 (floating-point control state confirmed in each thread; a C program changes it through `<fenv.h>`), .4 and .5.
- STND.MPI and STND.OMP: MPI has a C binding; STND.MPI.11 (owned handles) states the release rule for a C handle without a destructor. STND.OMP.21 (structured block exits), .22 (signal handlers without OpenMP), and the data-sharing provisions apply to C source directly. STND.CXX.22 is cited by both for the C++ exception; C needs only that no jump leaves a structured block, which STND.OMP.21 states.

What the corpus lacks for C: a single outcome for the lifetime and bounds classes (it is in STND.CXX.5 to .7 by C++ means), the integer-conversion and signed-overflow outcome (no corpus provision names it; NUMER.12 is about rounding of floating-point), the string and format outcomes, the preprocessor, `restrict`, VLAs, and `errno`. Each reduces to PRIME.4, DSGN.2, DSGN.3, or DSGN.14 and so need not raise the floor (GOV.11); the drafter's Notes argue it.

## Not verified

- The count of 221 items in J.2 is read from the draft N3220; I did not compare it with the published ISO text, nor count earlier editions' lists.
- Whether consume ordering is discouraged or unsupported in practice; whether C11 and the platform library mutexes interoperate with each other's condition variables.
- Whether the C standard requires a separate `errno` for each thread; I read the startup sentence only.
- That trigraphs were removed in C23 (they are absent from the draft, and a change entry was not found in its list).
- The status of the provenance technical specification and the `defer` specification; both rest on search results and meeting listings.
- The MISRA C:2012 counts; the CERT C per-category rule counts; the guideline count of MISRA C:2025 (223 to 225 by vendor).
- The Android primary post (body not retrievable); the Heartbleed missing-bounds detail (the page named the bug but not the cause).
- The `memcpy` and `memmove` qualifiers, which the fetch extract gave from its own background.
- Numbers from the studies are those of their years; none was re-run.

## Sources

All accessed 2026-10-24. "Full text" means I converted the PDF to text locally.

| ID | Source | Use |
| --- | --- | --- |
| S1 | open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf (C23 working draft, full text) | J.2, 5.1.2.5, 6.2.4, 6.3, 7.5, 7.14, 7.17, change history M.2 to M.6 |
| S2 | gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html | editions and default dialect |
| S3 | gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html; raw.githubusercontent.com/torvalds/linux/master/Makefile; kernel.org/doc/html/latest/process/programming-language.html | aliasing and null-check options; kernel build flags and dialect |
| S4 | blog.llvm.org/2011/05/what-every-c-programmer-should-know.html | how compilers exploit undefined behavior |
| S5 | users.cs.utah.edu/~regehr/papers/overflow12.pdf (full text) | integer overflow study |
| S6 | pdos.csail.mit.edu/papers/stack:sosp13.pdf (full text) | unstable code, 160 bugs, 40 percent of packages |
| S7 | same as S5 and S6 | time-bomb overflow |
| S8 | projectzero.google/2022/04/the-more-you-know-more-you-know-you.html | 2021 zero-days |
| S9 | microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code | 70 percent of CVEs |
| S10 | chromium.org/Home/chromium-security/memory-safety/ | 70 percent, half use after free |
| S11 | cl.cam.ac.uk/~pes20/cerberus/notes30.pdf (full text, contents and survey description only) | de facto semantics survey |
| S12 | same as S3 | kernel flags |
| S13 | cmu-sei.github.io/secure-coding-standards/ (CERT C, rule pages) | library errors, categories |
| S14 | S1 and S5 | conversions |
| S15 | kernel.org/doc/html/latest/process/coding-style.html | goto cleanup, error codes |
| S16 | cmu-sei.github.io/.../rules/error-handling-err/err33-c | ignored returns |
| S17 | S1 (7.5) and S22 | errno |
| S18 | S21 | string functions |
| S19 | gcc.gnu.org/onlinedocs/gcc/Warning-Options.html | format warnings |
| S20 | en.cppreference.com/w/c/language/restrict | restrict |
| S21 | kernel.org/doc/html/latest/process/deprecated.html | VLAs, strcpy family, allocation arithmetic |
| S22 | man7.org/linux/man-pages/man7/signal-safety.7.html | async-signal-safety |
| S23 | pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html | POSIX signal-safe list, stream locks |
| S24 | Boehm, Threads Cannot Be Implemented As a Library, PLDI 2005, via www.read.seas.harvard.edu/~kohler/class/aosref/boehm05threads.pdf (full text) | memory model argument |
| S25 | pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html | memory synchronization list |
| S26 | gcc.gnu.org/onlinedocs/gfortran/Interoperability-with-C.html | Fortran interoperation |
| S27 | docs.python.org/3/c-api/stable.html | Python C API stability |
| S28 | misra.org.uk/product/misra-c2023/ ; misra.org.uk/misra-c/ | MISRA editions and licensing |
| S29 | search results: docs.scitools.com/codecheck/MISRA_C_2025.html, ldra.com, parasoft.com, perforce.com | MISRA C:2025 counts and coverage |
| S30 | clang.llvm.org/docs/UndefinedBehaviorSanitizer.html | UB detector checks |
| S31 | clang.llvm.org/docs/AddressSanitizer.html | address detector |
| S32 | gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html | compiler analyzer |
| S33 | frama-c.com/html/acsl.html | deductive verification |
| S34 | cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html | weakness ranking |
| S35 | search results: open-std.org/jtc1/sc22/wg14/www/docs/n3954.htm and n3953.htm (minutes) | C2y, defer, TS 6010 |
| S36 | S1 (attributes) and S19 | nodiscard and warn_unused_result |
| S37 | open-std.org/jtc1/sc22/wg14/www/docs/n1967.htm | field experience with Annex K |
| S38 | heartbleed.com | Heartbleed |
| S39 | same as S25 and S23 | POSIX and C threads |
| S40 | cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/ | CERT C structure and edition |
| S41 | same as S19 | warnings |
| S42 | search results summarizing the Android memory-safety post (lwn.net, theregister.com, 9to5google.com) | Android share, secondary |
| S43 | cisa.gov/resources-tools/resources/product-security-bad-practices | memory-safety roadmap guidance |

Also fetched, not used: open-std.org/.../n3128.pdf (an unrelated five-page note; the fetch could not read it), the Boehm copy at courses.cs.washington.edu (a login page), the HP Labs copy (connection refused), and the Google security blog post on Android (page body missing). None was retried by another route.
