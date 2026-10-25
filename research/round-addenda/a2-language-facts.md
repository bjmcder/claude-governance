Role: research agent (confirmations a2: Python, Julia, C assert, finite-math options, Rust case lints). Date accessed: 2026-10-25. Retrieval counts: 21 items (all raw page text or PDF through curl) and about 9.2 MB, against a budget of 80 items and 150 MB. Rules followed: read-only retrieval; no paywall; no fetch failed, so no workaround, mirror, cache, or archive; no credentials; retrieved text treated as data.

## Method caveat

All sources were fetched with curl, stripped of tags (the PDF with pdftotext), and searched locally; quotations are verbatim. The pages are current editions (Julia 1.13.2, Python 3.15 notes); older releases were not read.

## 1. Python

### 1a. sys.excepthook and threading.excepthook: Confirmed, narrowed

S1: "When an exception other than SystemExit is raised and uncaught, the interpreter calls sys.excepthook with three arguments ... in a Python program this happens just before the program exits." and "This function prints out a given traceback and exception to sys.stderr." S2: "Handle uncaught exception raised by Thread.run()." ... "If exc_type is SystemExit, the exception is silently ignored. Otherwise, the exception is printed out on sys.stderr." Unraisable (S1): "Called when an exception has occurred but there is no way for Python to handle it."
Narrowing: S1 says "uncaught", not "main thread"; SystemExit is exempt; the threading hook is "Added in version 3.8".
Supports: `apply_py_1_1.py`, Reporting note, "An exception that no handler catches ends the main thread through the hook that the sys module holds ... the default hooks write the traceback to the standard error stream (unverified)" and the last sentence on the hook for an exception the interpreter is unable to raise (unverified). Both marks can go; write "reaches the hook", not "ends the main thread".

### 1b. -O and PYTHONOPTIMIZE: Confirmed

S3: "-O: Remove assert statements and any code conditional on the value of __debug__." and "PYTHONOPTIMIZE: If this is set to a non-empty string it is equivalent to specifying the -O option." S5: "The current code generator emits no code for an assert statement when optimization is requested at compile time."
Versions: S5 says "current implementation"; others [unverified].
Supports: the Assertions note of `apply_py_1_1.py`.

### 1c. Index out of range: Confirmed for built-in sequences

S6: "including built-in sequences, interpret negative subscripts by adding the sequence length. For example, a[-2] equals a[n-2] ... The resulting value must be a nonnegative integer less than the number of items in the sequence. If it is not, an IndexError is raised." S7: "An IndexError is raised if i is outside the sequence range."
A negative index from -len to -1 selects from the end and raises nothing; slices never raise. That -O leaves the check in place is my reading (S3 lists only assert and `__debug__` code). Array libraries and compiled Python: not covered.
Supports: `apply_py_1_1.py`, "The interpreter checks each index of a built-in sequence in every mode and raises IndexError" and "A negative index selects from the end of a sequence and raises nothing".

### 1d. ctypes

- Mismatched argtypes/restype: Confirmed. S8: "ctypes cannot determine a function's calling convention or signature. ... Without argtypes, the number of arguments is not checked. Calling a function with an incorrect calling convention or with incorrect arguments can corrupt memory or crash Python." and "By default functions are assumed to return the C int type." Pointer truncation is an inference; keep its mark.
- Exception in a callback: Not confirmed. S8 has no sentence on an exception raised in a callback (searched "exception", "unraisable", "ignored", "traceback"). The claim "reports it as unraisable and returns a default value" has no source here; keep "(unverified)" or drop the clause and keep the rule of STND.PY.35.
- Keep references: Confirmed for callbacks. S8: "Make sure you keep references to CFUNCTYPE() objects as long as they are used from C code. ctypes doesn't, and if you don't, they may be garbage collected, crashing your program when a callback is made." For buffers no sentence was found; keep the mark for them.
Supports: `apply_py_1_1.py`, Foreign interfaces note, marks at lines 157, 159, 165, 169.

### 1e. Lock files: Confirmed

S9: "PEP 751 – A file format to record Python dependencies for installation reproducibility", "Status: Final", "Type: Standards Track". S10: "A lock file MUST be named pylock.toml". Which installers read it: not stated; keep that mark.
Supports: `apply_py_1_1.py`, STND.PY.33 note, "PEP 751 specifies a common format for lock files": cite S9 and S10; status Final on 2026-10-25.

## 2. Julia

### 2a. @inbounds and --check-bounds: Confirmed

S12: "--check-bounds={yes|no|auto*} Emit bounds checks always, never, or respect @inbounds declarations". So yes: always; no: never; auto (the default): respect @inbounds. S11: "Using @inbounds may return incorrect results/crashes/corruption for out-of-bounds indices. The user is responsible for checking it manually."
Supports: `apply_jl_1_2.py`, the STND.JL.13 sentence on annotations and execution settings.

### 2b. ccall type mismatch: Confirmed in general; two clauses corrected

S13: "It is critical to exactly match the declared C type with its declaration in Julia. Inconsistencies can cause code that works correctly on one system to fail or produce indeterminate results on a different system." and "no C header files are used anywhere in the process of calling C functions: you are responsible for making sure that your Julia types and call signatures accurately reflect those in the C header file."
Corrections: (1) the page says "indeterminate results", not "a wrong value without an error"; use its wording. (2) Refuted for `Cint`: S13 lists "int ... Cint Int32" under "System Independent Types"; only "Clong Int (UNIX), Int32 (Windows)", "Culong", "Cchar", and "Cwchar_t" are system dependent. Write "`Clong` and `Cwchar_t` among them", not `Cint`. Column-major and strides: not found; keep that mark.
Supports: `apply_jl_1_2.py`, Foreign interfaces note, lines 123-126.

### 2c. GC.@preserve: Confirmed

S11: "GC.@preserve x1 x2 ... xn expr: Mark the objects x1, x2, ... as being in use during the evaluation of the expression expr. This is only required in unsafe code where expr implicitly uses memory or other resources owned by one of the xs." S13: "unsafe_string(pointer(hostname)) is an unsafe operation as it requires access to the memory allocated for hostname that may have been in the meanwhile garbage collected. The macro GC.@preserve prevents this". For a closure pointer S13: "You must ensure that this return object is kept alive until all uses of it are done."
Supports: `apply_jl_1_2.py`, lines 129-131; the mark can go.

### 2d. Exception in an @cfunction callback: Confirmed in effect, reworded

S13: "Callback functions exposed via @cfunction should not throw errors, as that will return control to the Julia runtime unexpectedly and may leave the program in an undefined state." The page does not say the exception "would unwind through frames"; use its wording.
Supports: `apply_jl_1_2.py`, lines 133-135.

### 2e. export and public: Confirmed, version-limited

S14: "each defines a set of names it exports and marks as public". "To mark a name as public without exporting it ... one can use public instead of export. This marks the public name(s) as part of the public API, but does not have any namespace implications. The public keyword is only available in Julia 1.11 and above."
Holds for 1.11 and later. No sentence says an exported name is public; that is a reading.
Supports: any Notes sentence treating exported and public names as the public interface.

## 3. C: assert and NDEBUG: Confirmed

S15, N3220 (working draft of ISO/IEC 9899:2024), 7.2 paragraph 1: "If NDEBUG is defined as a macro name at the point in the source file where <assert.h> is included, the assert macro is defined simply as #define assert(...) ((void)0)" and "The assert macro is redefined according to the current state of NDEBUG each time that <assert.h> is included."
So a `#define NDEBUG` in a source file turns the assertions off only when it precedes the inclusion; after the last inclusion it does nothing. The expansion is `((void)0)`, not nothing.
Supports: `apply_stdc_1_1.py` line 125, "Where NDEBUG is defined at the point at which the header of the assert macro is included, the macro expands to no check (unverified in c1)": drop the mark, cite N3220 7.2, write "expands to an expression that does nothing".

## 4. Finite-math options (specific to the compilers named)

Verdict: Confirmed that the option licenses the assumption; Not confirmed that tests for NaN are deleted. GCC (S16, -ffinite-math-only): "Allow optimizations for floating-point arithmetic that assume that arguments and results are not NaNs or +-Infs. This option is not turned on by any -O option besides -Ofast since it can result in incorrect output for programs that depend on an exact implementation of IEEE or ISO rules/specifications for math functions." Clang (S17): "-f[no-]finite-math-only: Allow floating-point optimizations that assume arguments and results are not NaNs or +-Inf." Neither page names a test for NaN; the effect follows from the assumption. These option names are specific to GCC and Clang; the standard stays tool-agnostic, so a Note names one only as an example without a version.
Supports: `apply_code_1_2.py`, lines 177-181 ("That assumption licenses the deletion of tests ... whether a given compiler deletes them is unverified": keep the hedge, it is correct) and `apply_stdc_1_1.py` "An option that assumes finite values removes a test for non-finite values": write "may remove".

## 5. Rust case lints: Confirmed

S18: "These lints are all set to the 'warn' level by default." Each of the three entries shows "`#[warn(...)]` (part of `#[warn(nonstandard_style)]`) on by default".
- non_snake_case: "detects variables, methods, functions, lifetime parameters, named fields and modules that don't have snake case names."
- non_camel_case_types: "detects types, variants, traits and type parameters that don't have camel case names."
- non_upper_case_globals: "detects static items that don't have uppercase identifiers."
Narrowing: the third names `static` items; the page does not say `const` items are covered, so do not claim all constants. "The Rust project publishes a convention" is not shown by S18 (no style guide was read); keep that part unverified.
Supports: `apply_rust_1_1.py` line 97, "lints that warn by default (as recalled; unverified in rs1)": replace the mark with the S18 citation.

## Sources

| Id | Source | URL |
|---|---|---|
| S1 | Python: sys | https://docs.python.org/3/library/sys.html |
| S2 | Python: threading | https://docs.python.org/3/library/threading.html |
| S3 | Python: command line | https://docs.python.org/3/using/cmdline.html |
| S4 | Python: constants | https://docs.python.org/3/library/constants.html |
| S5 | Python reference: simple statements | https://docs.python.org/3/reference/simple_stmts.html |
| S6 | Python reference: data model | https://docs.python.org/3/reference/datamodel.html |
| S7 | Python: built-in types | https://docs.python.org/3/library/stdtypes.html |
| S8 | Python: ctypes | https://docs.python.org/3/library/ctypes.html |
| S9 | PEP 751 | https://peps.python.org/pep-0751/ |
| S10 | pylock.toml Specification | https://packaging.python.org/en/latest/specifications/pylock-toml/ |
| S11 | Julia: Essentials | https://docs.julialang.org/en/v1/base/base/ |
| S12 | Julia: command-line interface | https://docs.julialang.org/en/v1/manual/command-line-interface/ |
| S13 | Julia: calling C and Fortran code | https://docs.julialang.org/en/v1/manual/calling-c-and-fortran-code/ |
| S14 | Julia: modules | https://docs.julialang.org/en/v1/manual/modules/ |
| S15 | WG14 N3220, 7.1.2, 7.2 | https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf |
| S16 | GCC: Optimize Options | https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html |
| S17 | Clang: Users Manual | https://clang.llvm.org/docs/UsersManual.html |
| S18 | rustc book: warn-by-default lints | https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html |

Also fetched, not used: the rustc lint-levels page and the Python compound statements page.
