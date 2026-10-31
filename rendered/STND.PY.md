# Python standard (STND.PY) 1.5.1

Adopted by The Custodian as revision 1.0 in ledger entry 104 (2026-10-23); revised to 1.0.1 in entry 119 (2026-10-24), 1.1 in entry 155 (2026-10-25), 1.2 in entry 194 (2026-10-27), 1.3 in entry 222 (2026-10-28), 1.3.1 in entry 242 (2026-10-28), 1.4 in entry 279 (2026-10-28), 1.5 in entry 322 (2026-10-28), and 1.5.1 in entry 334 (2026-10-31). This reading copy is composed from the per-provision files in STND/PY/ of the governance harness; the harness files are the system of record. Withdrawn identifiers, never reused: STND.PY.33, STND.PY.34, STND.PY.36, STND.PY.37, STND.PY.16, STND.PY.17, STND.PY.19, STND.PY.20, STND.PY.32, and STND.PY.14.

## Purpose and scope

This standard holds the conventions of Python source that the language-neutral practice of STND.CODE and STND.DOCS leaves to the language. They cover style from the style guide that the repository configuration names, enforced by tools at each change (STND.PY.1 and STND.PY.2); annotations under strict type checking (STND.PY.3 to STND.PY.9); docstrings in the docstring format that the repository configuration names, with the examples of the documentation run as doctests (STND.PY.10, STND.PY.11, and STND.PY.12); the declared releases of Python and of the work's dependencies (STND.PY.13), which STND.DEPS.14 checks; random number generators and stable streams (STND.PY.15 and STND.PY.18); reporting from library code (STND.PY.21 and STND.PY.22); idioms of Python source (STND.PY.23 and STND.PY.24); the handling of failures (STND.PY.25 to STND.PY.31); and the interrupts of the operator in code that a foreign interface invokes (STND.PY.35). STND.PY.22, STND.PY.25, STND.PY.27, and STND.PY.30 instantiate PRIME.4, and STND.PY.4 instantiates GOV.48 and binds agents alone, by its own force (GOV.48); STND.INSTR.10 carries it into the agent instructions. These five are binding and apply at every class. STND.CODE.14 states the one set of responses to a condition that PRIME.4 lists, and the other provisions refer to it; STND.PY.22 adds the categories of warnings that count as visible. The provisions of STND.CODE hold for Python as for every language, and the Notes give their Python forms. Every other provision is a default (GOV.19) and a recommendation, which a project replaces by a recorded decision with an alternative that meets the same higher outcome (REPRO.7, PRIN.10). The standard is agnostic of platform, version, and tool: the provisions state what a tool or a reviewer decides, and the project chooses its versions and tools in its repository configuration and its dependency record (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, High-assurance coding standard, Foreign interface, and Owned resource have the meanings that STND.CODE gives them, and a function of a compiled extension module, a function that the work loads from a shared library while it runs, and a Python callable that the work passes to such code are foreign interfaces; Lock file has the meaning that STND.DEPS gives it; Work documentation has the meaning that STND.DOCS gives it.

| Term | Definition |
| --- | --- |
| Style guide | The published guide of the conventions of Python source that the repository configuration names. |
| Typing specification | The specification of the Python type system at typing.python.org that the Typing Council maintains under PEP 729, read, on a matter it leaves open, with the typing PEP that it cites. |
| Annotation | A type that Python source states for a parameter, a return value, a variable, or an attribute, in the syntax of the typing specification. |
| Strict type checking | Type checking of Python source against the typing specification that reports each function defined without a complete annotation, each generic type used without its type arguments, each call from annotated code into an unannotated function, each return of a value of the dynamic type "Any" from a function annotated with another return type, and each suppression comment that suppresses nothing. |
| Docstring format | The published format of docstrings, with its sections and their order, that the repository configuration names. |
| Library code | Python source in the importable packages of the work, other than its test modules and the modules that hold entry points. A test, a script run directly, and a notebook are not library code. |
| Entry point | The function or module that starts a program, a test, or a script run directly, and each cell of a notebook. |
| Public interface | Each module, class, function, method, and module-level name of library code that the "__all__" of its module lists, or, in a module without "__all__", each of them whose own name and enclosing names carry no leading underscore. Each function and method of the public interface belongs to the public interface that the term Untrusted input of STND.CODE takes in. |
| Distributed package | A package of the work that the work distributes for other work to import. |

## Notes

The custodian's directions of 2026-10-22 are four: use the PEP standards for style and idioms, enforced with mechanical tools wherever possible; always use types and type checking; use the numpydoc docstring style; and format code so that it reads by the logical grouping of its instructions. The custodian's rulings of 2026-10-23 add that the standards are platform and compiler agnostic and that the project chooses its versions and tools. Each provision therefore states an outcome that a tool or a reviewer decides from the source and the repository configuration, and names no version, platform, or tool (GOV.18). Where a Note names a library function, it does so to show the hazard that a provision guards against. The note research/round-addenda/a2-language-facts.md (a2 below) confirms facts of these Notes from the documentation of Python, from PEP 751, and from the specification of the pylock.toml file, and the keys S1 to S10 that the Notes cite after a2 are entries of its table of sources.

Departures from the directions. The directions for style, docstrings, and layout are matters of form, so their provisions are defaults (GOV.19), whatever the verb of the direction. The direction "always" for types is met in two parts. Writing an annotation costs an agent only the form of the code it writes, not a tool or added work, so STND.PY.4 binds every agent at every class by its own force (GOV.48), for the reason of uniformity across projects that its field `binding_reason` records (GOV.19), and STND.INSTR.10 carries it into the agent instructions; that it raises no floor (GOV.11) is the custodian's ruling of 2026-10-23 (PRIN.10). Annotations that no checker reads are able to drift from the code (INTPR.3), and a type checker is a tool that the provisioned environment holds only under an authorization of the human owner (PRIME.7), which a standing authorization of STND.PROJ.3 gives (STND.DRAFT.42). A run of a tool is not bound at CSQ4 (GOV.11), so the checking and the remaining annotations are defaults from CSQ3.

Style. The style guide and the docstring format are documents that the repository configuration names (STND.PY.1, STND.PY.10), and the custodian's directions name the style PEPs, PEP 8 and PEP 257, and the numpydoc format. PEP 8 and PEP 257 are active, and PEP 8 leaves choices to a project, the length of a line among them, which the repository configuration settles (STND.PY.1). The idioms of this standard come from the Programming Recommendations of PEP 8, from PEP 257, from the typing PEPs through the typing specification, and, for scientific code, from SPEC 7 of the Scientific Python project and the logging guide of the Python documentation. The Zen of Python, PEP 20, informs review and decides nothing mechanically, so the standard does not cite it. STND.PY.2 asks the linter to check the agreement of documented parameters and return values with each function; agreement of the documented exceptions is left to review. STND.CODE.32 has the static checks decide each provision of this standard that a static check among the means of the work is able to decide.

Names from notation. PEP 8 names constants and classes by case, and NUMER.4 asks for names that map to the notation of the equations, so a matrix "A" or an operator "K" keeps its case (STND.CODE.28, STND.DOCS.12). A list of those names in the settings of the naming rules of the linter keeps each use free of a suppression comment, and a long line of displayed mathematics in a docstring takes a coded suppression (STND.PY.8).

Grouping. STND.CODE.13 groups the statements of each function body into blocks of one step each, and applies to Python as to every language. PEP 8 asks for blank lines in functions "sparingly, to indicate logical sections", which is the same rule. A formatter that keeps single blank lines inside a function keeps the grouping that the author makes; one that inserts a blank line before a nested definition inserts it under the exception of STND.CODE.13. A table of constants or a matrix kept in aligned columns is excluded from formatting at that statement only, by the suppression comment of the formatter.

Strict type checking. The term lists the findings by outcome, so that the project's choice of checker meets it by its settings. A dependency that carries no annotations makes the values it returns of the dynamic type, so the repository configuration gives the checker stubs, which are development tools in the dependency record (STND.DEPS.9), or a per-module override that relaxes that report for that dependency alone, with its reason (STND.PY.5). Existing source that does not pass is listed once by module in the repository configuration, and the list shrinks as changes touch the modules (STND.PY.6); the change that adopts strict checking writes the first list. Notebooks are outside the checking of STND.PY.5, because type checkers read them only through an added tool; this departure from "always" is the custodian's ruling of 2026-10-23, and a module that a notebook imports is library code and is checked. "Any" is the type that the checker does not check; STND.PY.8 asks for the reason at each use, and for "object" where every value is accepted, as the typing best practices advise. A suppression comment that names its rule code does not hide a finding that it was not written for. The py.typed marker of PEP 561 tells the checkers of dependents to read the annotations of a distributed package (STND.PY.7).

Arrays. An array library's type for inputs that a function converts often admits strings and carries no element type, as NumPy's ArrayLike does, which is why STND.PY.9 admits a narrower type, an array of a concrete scalar type, for a numeric input. A concrete scalar type also avoids a type argument that a generic scalar type would need under strict checking. Annotations of shape are checked at run time only where the project adds a run-time checker.

Docstrings. The numpydoc format, where the repository configuration names it, fixes the sections and their order, from the short summary to Examples (STND.PY.10), and its format guide says nothing of annotations. STND.PY.11 departs from the practice of major scientific libraries, which state each parameter's type in the docstring as well, by the custodian's ruling of 2026-10-23: a type restated in a Parameters entry is documentation that merely restates the code (INTPR.2) and drifts from it unchecked (INTPR.3), while the annotation is checked. The Returns and Yields sections keep a type, because the numpydoc format requires one there and reads a one-line entry as a type; that type is written as the annotation writes it, and review compares the two. A docstring validator that reads parameter types from the docstring alone is set not to require them, and the documentation build takes the types from the annotations. The units, shape, and range of valid values of an item appear in its entry only where the item has them (STND.PY.10, STND.CODE.3, INTPR.4).

Doctests. STND.DOCS.13 compares the shown result of an example within a stated tolerance, and the doctest module of the standard library compares text exactly. A test runner that compares each floating-point number to the precision written in the expected output makes the written digits the tolerance; an example that needs another tolerance shows a value that it rounds itself, or the result of a comparison that states its tolerances, the forms in Python of the comparison within a stated tolerance of STND.DOCS.13. An example that shows an exception compares its type and not its message, which changes between Python releases. The test runner also collects the examples of documents outside docstrings.

Versions. The project chooses the releases of Python and of its dependencies that it declares, under STND.DEPS.3 and STND.DEPS.4, and the repository configuration records them (STND.PY.13). A distributed package declares the oldest releases it supports so that its dependents know what they are able to combine with it, and its checks run on the oldest declared combination and on the newest combination that its declared ranges admit (STND.DEPS.14). A new Python release is able to precede the releases of dependencies that support it, which is why the newest combination is limited to releases consistent with one another. An application or an archived study that no other work imports pins its interpreter and packages as dependencies, and a qualified revision stays fixed under STND.DEPS.3. A change of the Python release on which the work runs is a change of the runtime of each execution path under HW.7 and of a pinned revision under STND.DEPS.5, and each run records the exact Python and library revisions (STND.DEPS.8); the lock file of the package installer is the exact record of those revisions (STND.DEPS.10). STND.DEPS.12 keeps a lock file that the tools of the work write under version control wherever an environment of the work produces reported results, so that the revisions of a run are those of its source; it asks for no lock file where the tools write none. A distributed package whose own environment produces no reported result leaves its dependents to resolve their own environments, and its checks run on the combinations of STND.DEPS.14; that such a package commits no lock file is common practice (unverified). PEP 751, a standard of status Final, specifies a common format for lock files, named pylock.toml (a2, S9 and S10); which installers read or write it is unverified, and a format of a project tool's own is a lock file in the sense of the term where it records each exact revision, as a requirements file that pins the exact revision of each package that the environment installs, its transitive dependencies included, does. STND.CODE.19 fixes, for high-assurance code, a release of Python that its high-assurance coding standard covers and for which each tool that runs that code holds the validation that the work requires; that release is a qualified revision, which STND.DEPS.3 leaves fixed, and STND.DEPS.14 yields to it by its own text. Running the checks of STND.DEPS.14 at release, and not at each change, is a deferral of verification under RSRC.12.

Randomness. STND.CODE.2 already asks that the source of randomness arrive through the interface; STND.PY.15 gives its Python form, a generator object passed through a parameter named rng as SPEC 7 names it, and keeps library code off the global random states of its libraries and of the random module, which are hidden global state (DSGN.14). SPEC 7 also lets the rng parameter accept a seed or None; STND.CODE.29 keeps that conversion at the entry point, because an integer passed to two functions gives them identical streams and None draws entropy that nobody records. Streams for parallel parts derive from the root seed and the part index through spawning, jump-ahead, or counter-based keys (STND.CODE.29, STND.VVUQ.62); a stream chosen by worker or process identity, or copied into forked processes, differs between runs. STND.CODE.29 states the rule of STND.CONC.23, which keys each stream of a computation divided among concurrent tasks to a part defined independently of the number of tasks and of the task that computes it, for each division of work into parts, parts run as separate runs included, which STND.CONC.23 does not reach. NUMER.24 governs the evidence that the streams are independent.

Stable values. A generator library is able to keep the stream of a bit generator fixed for a seed while the sampling methods built on it change their output between releases, as the methods of NumPy's Generator have done. A test reference of exact drawn values therefore draws through a stable stream or holds stored data (STND.PY.18). A test whose verdict depends on a seeded stream states in advance how it is repeated after an upgrade of its generator library, because NUMER.26 forbids reseeding as the remedy for a failure without such a rule. The built-in hash of a str or bytes object varies between runs with the hash seed of the interpreter, and with it the iteration order of a set of strings (STND.CODE.30).

Comparisons. STND.VVUQ.1 sets the tier of each comparison, STND.VVUQ.5 the relative and absolute parts of the rounding and numerical-error tiers, and STND.VVUQ.3 the agreement of NaNs; STND.CODE.31 asks that the comparison state those parameters where the code makes it, through a library function or an expression. Defaults differ between comparison functions: math.isclose defaults to an absolute tolerance of zero, and NumPy's assert_allclose treats NaNs as equal while its isclose does not, so a comparison that relies on defaults decides for a reason the reader does not see. Each tolerance is a named constant with its basis beside it (STND.CODE.10, NUMER.11), so that a copied value without a basis stands out in review.

Reporting. Library code writes diagnostics through a module logger and leaves the handlers to the program that imports it (STND.PY.21). A null handler on a library logger also stops the last-resort output of Python, so a warning written only to that logger is silent when the program configures nothing. STND.CODE.14 therefore keeps a record from library code from being the only visible degradation; an entry point whose handler shows the record degrades visibly through it. A warning of a category that the default filters hide, DeprecationWarning outside the main module, PendingDeprecationWarning, ImportWarning, and ResourceWarning among them, is silent and does not count (STND.PY.22). An exception other than SystemExit that is raised and not caught reaches the hook that the sys module holds for it, just before the program exits, and one that the run method of a thread raises reaches the hook that the threading module holds; the default hooks print the traceback and the exception to the standard error stream (a2, S1 and S2). STND.CODE.33 asks a hook that the work installs in their place, to write the exception to a log or to a report among them, to deliver the diagnosis of each listed condition that reaches it, and work that keeps the default hooks meets it unchanged. The hook of the sys module that the interpreter calls when an exception has occurred and Python has no way to handle it is such a hook, run for a failure that the runtime is unable to propagate (a2, S1).

Idioms. Python evaluates a default value once, at definition, so a mutable default is state shared across calls (STND.PY.23); None is the usual default, with the object built in the body. The default text encoding of Python has depended on the platform, so a file opened without its encoding is able to read differently on different machines, and an error handler of "ignore" or "replace" substitutes characters silently (STND.PY.24). File system paths held as path objects of the pathlib module are clearer to read than strings joined by hand, and the linter's rules for them are a choice of configuration.

Assertions. STND.CODE.14 admits the pass of a condition to the caller in its result, in an argument that the caller passes to receive it, or by a mechanism of the language, an exception among them, that propagates the condition to the caller; in Python a raised exception is that mechanism, and a returned result the first form. STND.PY.25, STND.PY.27, and STND.PY.30 are the Python forms of STND.CODE.6 and STND.CODE.7, each limited to the conditions that PRIME.4 lists. STND.CODE.15 asks nothing of Python until a form of declaration under which an ignored result is diagnosed is among the means of the work, and STND.CODE.7 still forbids discarding a listed failure. The interpreter removes assert statements under its optimizing mode, an execution setting, so an assertion that checks untrusted input lets invalid input through in that mode (STND.PY.25). An argument of the public interface is untrusted input unless the threat model of GUARD.16 records otherwise, so a shape check of an argument raises an exception in place of an assertion; that this reaches every function of the public interface at every class, as PRIME.4 does, is the custodian's ruling of 2026-10-23 (PRIN.10). STND.CODE defines the term once, and the term Public interface places the functions and methods of that interface in the public interface that the term takes in, so the reach of the ruling is kept; STND.CODE adds the functions that the documentation or the repository configuration names for use outside the work. The optimizing mode, set by an option of the command line or by an environment variable, removes assert statements and the code that depends on the value of __debug__ (a2, S3 and S5). A run-time check of an invariant or postcondition that the work relies on is written as a raise statement for the same reason (STND.PY.26), and STND.CODE.16 binds the same for each check that CPS.5 or CPS.9 requires where those apply. STND.JL.13 binds a check of each index that derives from untrusted input, because an annotation or an execution setting of Julia removes the bounds checks of its indexing. A built-in sequence raises IndexError for an index outside its range (a2, S6 and S7), a response that STND.CODE.14 admits, and the optimizing mode leaves that check in place, since it removes only assert statements and code that depends on __debug__; whether each array library checks its indices in the same way is unverified. This standard therefore has no counterpart of that sentence. A negative index from minus the length to minus one selects from the end of a sequence and raises nothing, and a slice raises nothing whatever its bounds (a2, S6); where the contract of a function excludes it, only a check of the function under DSGN.2 rejects it. Code that a compiler translates from Python source is able to index without bounds checks, by default or by an option (unverified for each compiler); STND.PY.31 asks the reason for each such use, and STND.CODE.6 keeps an execution setting from removing a check of untrusted input there.

Handlers. MemoryError and RecursionError derive from Exception, so a handler of Exception, of BaseException, or of every exception catches the resource exhaustion that PRIME.4 lists, and a suppression context with those classes discards it with no handler at all (STND.PY.27). A handler meets STND.PY.27 by raising the same exception, by raising another one from it, by halting, or by a visible fallback, a computation in smaller pieces with a warning among them. KeyboardInterrupt and SystemExit are the operator's stop and the program's exit, which PRIME.4 does not list, so STND.PY.28 raises them again as a default; a handler that stores an exception to raise it in another thread raises it again there.

Error settings. A process-wide setting of the floating-point error handling of a numerical library, numpy.seterr among them, or of the warnings filters changes the behavior of every other component in the process, which is hidden shared state (STND.PY.29); an entry point is the place for such a setting, and the reason for each suppression is stated at its location (STND.CODE.12). Where the suppressed report signals a condition that PRIME.4 lists, a convergence warning among them, STND.CODE.7 still forbids discarding the condition, so the code detects it by another means, a convergence flag or a check of the result, and responds as STND.CODE.14 gives (STND.PY.30); an entry point that ignores invalid-value reports for the whole process and checks each result for finite values meets it.

Relaxed checks. Functions that substitute values, numpy.nan_to_num and numpy.clip among them, are silent defaults under PRIME.4 where the value they replace is invalid input, and STND.CODE.7 governs them there. An argument that disables a finiteness check, check_finite=False of SciPy among them, a compiler option for fast floating-point arithmetic, and a disabled bounds check remove a check or relax the arithmetic, so each carries its reason (STND.PY.31). Where code compiled under such an option holds a check of a floating-point value that STND.CODE.6 governs, STND.CODE.21 recommends against an option that lets the compiler assume finite values, beside the reason that STND.PY.31 asks. On the path of a numerical result, a relaxation of floating-point semantics is a performance approximation, which NUMER.16 and NUMER.17 govern.

Foreign interfaces. STND.CODE.22 to STND.CODE.26 hold for Python the types, the layouts, and the arrays that cross a foreign interface, the failures kept from crossing it, and the owner and the lifetime of what crosses it, and STND.PY.35 adds the Python form of the interrupts of the operator (DSGN.4, DSGN.5, DSGN.14). A compiled extension module is built against the declarations of the foreign code, so that its compiler checks the types of each call (unverified for each build tool). A library that loads a shared library while the program runs reads no header, and takes the types of each call from what the Python source declares to it, or from defaults where it is given none (unverified for each library). The ctypes module of the standard library is unable to determine the signature of a foreign function, checks no number of arguments where none are declared, and assumes that a function returns a C int unless its result type is declared; incorrect arguments are able to corrupt memory or crash the interpreter (a2, S8). These hazards are why, where an interface checks no call against the foreign declaration, a declaration of the type of each argument and of the result in the Python source is the means by which each type that crosses has the representation that STND.CODE.22 asks, and why its second sentence reaches the layout of each structure that the source declares. A slice of an array is a view whose elements are not always adjacent in memory (unverified for each array library), and STND.CODE.23 reaches the strides of an array passed by a pointer to its elements. What a foreign interface does with an exception that a Python callback raises is unverified for each interface, so STND.CODE.24 asks for the catch unless the contract of the interface, its documentation among it, states that the exception is passed on. KeyboardInterrupt and SystemExit are the stop of the operator and the exit of the program, so STND.PY.35 stores them in place of their conversion and raises them again after the foreign call returns, as STND.PY.28 asks of a handler; each other exception so caught is answered as STND.CODE.14 gives. The ctypes module keeps no reference to a callback object, which the garbage collector is then able to free while C code still holds it, crashing the program when the callback is made (a2, S8); whether a buffer passed to foreign code is kept alive is unverified for each interface. STND.CODE.26 asks the work to keep each such object reachable, a buffer and a callable among them, and STND.CODE.25 gives each owned resource that foreign code creates one owner.

Floor. STND.PY.22 keeps a warning that the default filters hide from counting as a visible degradation, and STND.PY.25, STND.PY.27, and STND.PY.30 ask only for a response that STND.CODE.14 gives, or forbid a construct that leaves a listed condition without one, so none of them asks for work that PRIME.4 does not; that these raise no floor is the custodian's ruling of 2026-10-23 (PRIN.10). They bind at every class, CSQ4 included, as PRIME.4 does.

Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, RSRC, or a provision of NUMER, and applies from the class that its field `onset` gives, which work of CSQ4 may omit, the store of STND.PY.35 at CSQ3 with the catch of STND.CODE.24. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no provision raises the floor (GOV.11).

Existing source conforms when a change next touches it, other than the strict checking of STND.PY.5, which existing modules reach through the list of STND.PY.6; on a reclassification, STND.CLASS.22 governs.

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
| PRIN | Governing Principles |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.CONC | Concurrency standard |
| STND.DEPS | Dependency policy |
| STND.DOCS | Documentation standard |
| STND.DRAFT | Drafting standard |
| STND.INSTR | Agent instructions |
| STND.JL | Julia standard |
| STND.PROJ | Project constitution template |
| STND.RUST | Rust standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Style

#### STND.PY.1 Configured style guide as baseline

Default, from CSQ3. Instantiates INTPR.1.

Python source SHOULD follow the conventions of the style guide, with each choice that the style guide leaves to a project settled once in the repository configuration (INTPR.1).

#### STND.PY.2 Python linter coverage

Default, from CSQ3. Instantiates INTPR.1, INTPR.3, DSGN.3.

The static checks that the repository configuration names for Python under STND.CODE.4 SHOULD include a linter that checks the conventions of the style guide that the layout tool of STND.CODE.5 leaves open, the structure of each docstring against the docstring format, and the agreement of the parameters and return values that each docstring documents with its function (INTPR.1, INTPR.3, DSGN.3).

### Types

#### STND.PY.3 Annotation coverage

Default, from CSQ3. Instantiates DSGN.1, DSGN.3.

Other than a parameter named self or cls, each parameter and the return value of each function and method that a def statement defines SHOULD carry an annotation (DSGN.1, DSGN.3). Other than a member of an enumeration, each module-level name and each class attribute whose type the type checker does not infer from its assigned value SHOULD carry an annotation (DSGN.1).

#### STND.PY.4 Agent annotations

Binding. Instantiates GOV.48, DSGN.1.

An agent SHALL write an annotation of each parameter and return value that STND.PY.3 covers in each Python function and method that it writes or changes, or the form that an alternative adopted by a project instrument in place of STND.PY.3 requires (GOV.48, DSGN.1).

#### STND.PY.5 Strict type checking

Default, from CSQ3. Instantiates DSGN.3, REPRO.7.

The static checks that the repository configuration names for Python under STND.CODE.4 SHOULD include strict type checking of the library code, the tests, and the scripts of the work (DSGN.3). Where a dependency of the work carries no annotations, the repository configuration SHOULD give the type checker stubs for it that the dependency record lists, or an override for the modules of that dependency that names the finding it relaxes and its reason (DSGN.3, REPRO.7).

#### STND.PY.6 Modules exempted from strict checking

Default, from CSQ3. Instantiates REPRO.7, DSGN.3.

Where a module of the work does not pass strict type checking, the repository configuration SHOULD name it, with its reason, in one list of exempted modules (REPRO.7). Other than a module that a change of a dependency or the change that adopts strict checking makes fail, a change SHOULD NOT add a module to that list (DSGN.3).

#### STND.PY.7 Typed package marker

Default, from CSQ3. Instantiates DSGN.1.

Each distributed package SHOULD include a py.typed marker file in its distribution (DSGN.1).

#### STND.PY.8 Reasoned dynamic types and suppressions

Default, from CSQ3. Instantiates REPRO.7, DSGN.1.

Where an annotation uses the dynamic type "Any", a comment at that annotation SHOULD state why the typing specification does not express the type (REPRO.7). Where a parameter accepts every value, its annotation SHOULD be object (DSGN.1). Each comment that suppresses a finding of the linter or of the type checker SHOULD name the code of each rule that it suppresses, beside the reason that STND.CODE.4 asks for (REPRO.7).

#### STND.PY.9 Array annotations

Default, from CSQ3. Instantiates DSGN.1.

Each parameter that a function converts to an array SHOULD be annotated with the type that its array library gives for inputs convertible to an array, or with a narrower type (DSGN.1). Each other parameter, return value, module-level name, and class attribute that holds an array SHOULD be annotated with the array type of its array library and the scalar type of its elements (DSGN.1).

### Docstrings

#### STND.PY.10 Docstrings in the configured format

Default, from CSQ3. Instantiates INTPR.1, INTPR.3, DSGN.1, INTPR.4.

Each module, class, function, and method of the public interface SHOULD carry a docstring in the docstring format, with its sections in the order that the format gives, that documents each parameter, each returned or yielded value, and each exception that the function raises with the condition under which it raises it (INTPR.1, INTPR.3). Each docstring of an interface that STND.CODE.3 covers SHOULD state its contract in the entries of its items, with the units, the shape, and the range of valid values that each item has and that its annotation does not carry (DSGN.1, INTPR.4).

#### STND.PY.11 Parameter types in annotations

Default, from CSQ3. Instantiates INTPR.3.

Each entry of a docstring that documents a parameter or an attribute SHOULD describe its item without restating the type that the annotation of the item gives (INTPR.3). Where the docstring format has a position for the type of a returned or yielded value, each entry that documents such a value SHOULD give there the type that the return annotation states for that value (INTPR.3).

#### STND.PY.12 Doctest examples

Default, from CSQ3. Instantiates INTPR.3, VV.8.

Each example of the work documentation that STND.DOCS.13 runs SHOULD be a doctest example that the test runner collects (INTPR.3, VV.8).

### Versions

#### STND.PY.13 Declared Python releases

Default, from CSQ3. Instantiates REPRO.9.

Each distributed package SHOULD declare in its package metadata the oldest release of Python and of each dependency that it supports, as chosen under STND.DEPS.3 and reviewed under STND.DEPS.4 (REPRO.9).

### Randomness

#### STND.PY.15 Generator arguments

Default, from CSQ3. Instantiates DSGN.17, DSGN.16, DSGN.14.

Each function of library code that draws random numbers SHOULD draw them only from a generator object that it receives through a parameter named rng (DSGN.17, DSGN.16, DSGN.14). Library code SHOULD leave unseeded each global random state of its libraries and of the random module of the standard library (DSGN.14).

#### STND.PY.18 Exact values from random draws

Default, from CSQ3. Instantiates REPRO.3, REPRO.6, VV.3.

Each test reference and each documentation example that holds exact values drawn from a random number generator SHOULD draw them through a bit generator and a method whose output for a given seed stays the same across the releases of the generator library that the work supports, or hold the values as recorded data (REPRO.3, REPRO.6). Where the verdict of a test depends on the stream of a seeded generator, the test SHOULD state, before its first failure, the rule by which it is repeated after a change of the release of its generator library, as NUMER.26 requires of a repetition (VV.3).

### Reporting

#### STND.PY.21 Logging in library code

Default, from CSQ3. Instantiates DSGN.16, RSRC.10.

Library code SHOULD write its diagnostics, its progress, and its decisions through a logger of the logging module named for its module, in place of writing to standard output (DSGN.16, RSRC.10). The only handler that library code attaches to its loggers SHOULD be logging.NullHandler (DSGN.16).

#### STND.PY.22 Warnings of shown categories

Binding. Instantiates PRIME.4.

Under STND.CODE.14, where the visible degradation of a condition that PRIME.4 lists is a warning, its category SHALL be one that the default warnings filters show (PRIME.4).

### Source idioms

#### STND.PY.23 Immutable parameter defaults

Default, from CSQ3. Instantiates DSGN.14.

The default value of each parameter SHOULD be immutable (DSGN.14).

#### STND.PY.24 Named text encodings

Default, from CSQ3. Instantiates SIMPL.6, REPRO.3.

Each call that opens, decodes, or encodes text SHOULD name its encoding and leave its error handler strict (SIMPL.6, REPRO.3).

### Failures

#### STND.PY.25 Assertions on untrusted input

Binding. Instantiates PRIME.4, DSGN.2.

Code SHALL NOT check untrusted input with an assert statement (PRIME.4, DSGN.2, STND.CODE.6).

#### STND.PY.26 Run-time checks without assert

Default, from CSQ1. Instantiates VV.10, DSGN.2.

Each run-time check of an invariant or a postcondition that VV.10 or DSGN.2 asks of the work SHOULD be written as a raise statement under a condition, in place of an assert statement (VV.10, DSGN.2).

#### STND.PY.27 Exhaustion caught by handlers

Binding. Instantiates PRIME.4.

Where a handler catches MemoryError or RecursionError by naming it, a class from which it derives, or no class, it SHALL respond as STND.CODE.14 requires (PRIME.4). Each class that a suppression context names SHALL be neither MemoryError, nor RecursionError, nor a class from which either derives (PRIME.4).

#### STND.PY.28 Interrupts raised again

Default, from CSQ3. Instantiates SIMPL.6.

Where an except clause catches KeyboardInterrupt or SystemExit, by naming it, by naming BaseException, or by naming no class, its handler SHOULD raise that exception again (SIMPL.6).

#### STND.PY.29 Scoped error settings

Default, from CSQ3. Instantiates DSGN.14.

Outside an entry point, each change that code makes to the warnings filters, or to the floating-point error handling of a numerical library, SHOULD be confined to a with statement that encloses only the operations it concerns (DSGN.14).

#### STND.PY.30 Suppressed reports of listed failures

Binding. Instantiates PRIME.4.

Where code suppresses a warning or an error report that signals a condition that PRIME.4 lists, it SHALL detect each such condition by another means and respond to it as STND.CODE.14 requires (PRIME.4).

#### STND.PY.31 Relaxed numerical checks

Default, from CSQ3. Instantiates REPRO.7, DSGN.2.

Each use of an argument that disables a finiteness or validity check of a numerical library, of a disabled bounds check, or of a compiler option that relaxes floating-point semantics SHOULD state at its location why each input that it covers is valid (REPRO.7, DSGN.2).

### Foreign interfaces

#### STND.PY.35 Python interrupts in foreign callbacks

Default, from CSQ3. Instantiates DSGN.5.

Where a Python callable that a foreign interface invokes catches KeyboardInterrupt or SystemExit under STND.CODE.24, that exception SHOULD be stored in place of its conversion, and raised again after the foreign call returns, as STND.PY.28 asks (DSGN.5).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-23 | Adopted. |
| 1.0.1 | 2026-10-24 | Editorial amendment (GOV.41): the informative Notes cite STND.CONC.23 as the model-neutral rule that STND.PY.17 states for the work in Python, and state the wider scope of STND.PY.17, and cite GUARD.16 for the threat model that records a source of input as trusted; References lists STND.CONC and GUARD; no obligation changes. |
| 1.1 | 2026-10-25 | Minor amendment (GOV.41): Terms import Untrusted input, and Execution setting, from STND.CODE and drop this standard's own definition of Untrusted input, and the term Public interface places its functions and methods in the public interface that the term Untrusted input of STND.CODE takes in; Terms import High-assurance code and High-assurance coding standard from STND.CODE and define Lock file, in the wording of the term of STND.RUST, and Foreign interface; STND.PY.22 cites STND.CODE.14, and STND.PY.25 STND.CODE.6, for the rule of which each is the Python form, and neither changes otherwise; STND.PY.14 yields to a release of Python that STND.CODE.19 fixes; new STND.PY.32 (binding, PRIME.4) has a hook that the work installs for an exception that no handler catches, or that the interpreter is unable to raise, deliver the diagnosis of each listed condition, the Python counterpart of the second sentence of STND.RUST.13; new STND.PY.33 (default, REPRO.1 and REPRO.9) keeps the lock file that the tools of the work write for an environment that produces reported results under version control, as STND.JL.4 does for a manifest, and the Notes state how STND.RUST.30 differs; new STND.PY.34 to STND.PY.37 (defaults, DSGN.4, DSGN.5, and DSGN.14) give the types and layouts, the exceptions of callbacks, the lifetime and ownership of memory, and the layout of arrays at foreign interfaces; the Purpose lists them; the Notes cite the provisions of STND.CODE of which this standard gives Python forms, give the reason why this standard has no counterpart of the third sentence of STND.JL.13, and state the facts, the floor argument of STND.PY.32, and the onset of each new provision. |
| 1.2 | 2026-10-27 | Minor amendment (GOV.41): STND.PY.33 is withdrawn, its outcome being STND.DEPS.12 for every language; STND.PY.34, STND.PY.36, and STND.PY.37 are withdrawn, their outcomes being STND.CODE.22, STND.CODE.23, STND.CODE.25, and STND.CODE.26 for every language; the front matter lists the four as withdrawn; STND.PY.35 keeps only the storing of KeyboardInterrupt and SystemExit in place of their conversion, and their raise after the foreign call returns, the Python form of STND.CODE.24, and is retitled Python interrupts in foreign callbacks; Terms import Foreign interface from STND.CODE, naming the Python constructs that are foreign interfaces, and Lock file from STND.DEPS, and drop this standard's own definitions; the Purpose, and the Notes on versions, foreign interfaces, and onsets, follow. |
| 1.3 | 2026-10-28 | Minor amendment (GOV.41): STND.PY.16, STND.PY.17, STND.PY.19, STND.PY.20, and STND.PY.32 are withdrawn, their outcomes being STND.CODE.29, STND.CODE.30, STND.CODE.31, and STND.CODE.33 for every language, and the front matter lists them as withdrawn; STND.PY.22 keeps only the categories of warnings that the default filters show, the responses and the record of library code being STND.CODE.14, and is retitled Warnings of shown categories; STND.PY.27 and STND.PY.30 cite STND.CODE.14 in place of STND.PY.22; Terms define Style guide and Docstring format as the documents that the repository configuration names, in place of Style PEPs and Numpydoc standard, and STND.PY.1, STND.PY.2, STND.PY.10, and STND.PY.11 use them, STND.PY.1 being retitled Configured style guide as baseline and STND.PY.10 Docstrings in the configured format; STND.PY.1 drops the names that the notation of NUMER.4 fixes, which STND.CODE.28 holds; STND.PY.2 drops its second sentence, which STND.CODE.32 holds; STND.PY.12 drops its second sentence, which STND.DOCS.13 holds; the Purpose and the Notes follow. |
| 1.3.1 | 2026-10-28 | Editorial amendment (GOV.41): the Notes keep their sentence on existing source and add that STND.CLASS.22 governs on a reclassification; no obligation, permission, or defined meaning changes. |
| 1.4 | 2026-10-28 | Minor amendment (GOV.41): STND.PY.35 applies from CSQ3, with the catch of STND.CODE.24 at a foreign frame; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
| 1.5 | 2026-10-28 | Minor amendment (GOV.41): STND.PY.14 is withdrawn, STND.DEPS.14 holding the checks of each release on the oldest declared releases and on the newest consistent ones for every language, and the front matter lists it as withdrawn; the Purpose and the Notes cite STND.DEPS.14. |
| 1.5.1 | 2026-10-31 | Editorial amendment (GOV.41): STND.PY.4 records in its field binding_reason why uniformity across projects requires it to bind (GOV.19), for the custodians to adopt with this revision, and the Notes cite the field; no obligation, permission, or defined meaning changes. |
