"""STND.PY draft 0.4: the Python standard, after the custodian's rulings of 2026-10-23
(platform and tool agnostic; versions and tools chosen in the repository configuration),
on STND.DOCS, STND.INSTR 1.4, and STND.CODE 1.1 as apply8 and apply9 rehearse them."""
from content3 import P, NORMATIVE, TERMS_LEAD

DATE = "2026-10-23"

PURPOSE = """This standard holds the conventions of Python source that the language-neutral practice of STND.CODE and STND.DOCS leaves to the language. They cover style from the Python Enhancement Proposals, enforced by tools at each change (STND.PY.1 and STND.PY.2); annotations under strict type checking (STND.PY.3 to STND.PY.9); docstrings in the numpydoc format, with the examples of the documentation run as doctests (STND.PY.10, STND.PY.11, and STND.PY.12); the declared and checked releases of Python and of the work's dependencies (STND.PY.13 and STND.PY.14); random number generators and values that vary between runs (STND.PY.15 to STND.PY.19); comparisons within a tolerance (STND.PY.20); reporting from library code (STND.PY.21 and STND.PY.22); idioms of Python source (STND.PY.23 and STND.PY.24); and the handling of failures (STND.PY.25 to STND.PY.31). STND.PY.22, STND.PY.25, STND.PY.27, and STND.PY.30 instantiate PRIME.4, and STND.PY.4 instantiates GOV.48 and binds agents alone, by its own force (GOV.48); STND.INSTR.10 carries it into the agent instructions. These five are binding and apply at every class. STND.PY.22 states the one set of responses to a condition that PRIME.4 lists, and the other provisions refer to it. Every other provision is a default (GOV.19) and a recommendation, which a project replaces by a recorded decision with an alternative that meets the same higher outcome (REPRO.7, PRIN.10). The standard is agnostic of platform, version, and tool: the provisions state what a tool or a reviewer decides, and the project chooses its versions and tools in its repository configuration and its dependency record (GOV.18)."""

TERMS = TERMS_LEAD + """ Repository configuration and Static check have the meanings that STND.CODE gives them; Work documentation has the meaning that STND.DOCS gives it.

| Term | Definition |
| --- | --- |
| Style PEPs | PEP 8, Style Guide for Python Code, and PEP 257, Docstring Conventions, in the revisions current at the change. |
| Typing specification | The specification of the Python type system at typing.python.org that the Typing Council maintains under PEP 729, read, on a matter it leaves open, with the typing PEP that it cites. |
| Annotation | A type that Python source states for a parameter, a return value, a variable, or an attribute, in the syntax of the typing specification. |
| Strict type checking | Type checking of Python source against the typing specification that reports each function defined without a complete annotation, each generic type used without its type arguments, each call from annotated code into an unannotated function, each return of a value of the dynamic type "Any" from a function annotated with another return type, and each suppression comment that suppresses nothing. |
| Numpydoc standard | The docstring format that the format guide of the numpydoc project defines, with its sections and their order. |
| Library code | Python source in the importable packages of the work, other than its test modules and the modules that hold entry points. A test, a script run directly, and a notebook are not library code. |
| Entry point | The function or module that starts a program, a test, or a script run directly, and each cell of a notebook. |
| Public interface | Each module, class, function, method, and module-level name of library code that the "__all__" of its module lists, or, in a module without "__all__", each of them whose own name and enclosing names carry no leading underscore. |
| Distributed package | A package of the work that the work distributes for other work to import. |
| Untrusted input | Data that reaches the work from outside its own code, including the arguments of each function of the public interface, other than data from a source that the threat model of the project records as trusted. |"""

NOTES = """The custodian's directions of 2026-10-22 are four: use the PEP standards for style and idioms, enforced with mechanical tools wherever possible; always use types and type checking; use the numpydoc docstring style; and format code so that it reads by the logical grouping of its instructions. The custodian's rulings of 2026-10-23 add that the standards are platform and compiler agnostic and that the project chooses its versions and tools. Each provision therefore states an outcome that a tool or a reviewer decides from the source and the repository configuration, and names no version, platform, or tool (GOV.18). Where a Note names a library function, it does so to show the hazard that a provision guards against.

Departures from the directions. The directions for style, docstrings, and layout are matters of form, so their provisions are defaults (GOV.19), whatever the verb of the direction. The direction "always" for types is met in two parts. Writing an annotation costs an agent only the form of the code it writes, not a tool or added work, so STND.PY.4 binds every agent at every class by its own force (GOV.48), and STND.INSTR.10 carries it into the agent instructions; that it raises no floor (GOV.11) is the custodian's ruling of 2026-10-23 (PRIN.10). Annotations that no checker reads are able to drift from the code (INTPR.3), and a type checker is a tool that the provisioned environment holds only under an authorization of the human owner (PRIME.7), which a standing authorization of STND.PROJ.3 gives (STND.DRAFT.42). A run of a tool is not bound at CSQ4 (GOV.11), so the checking and the remaining annotations are defaults from CSQ3.

Style. PEP 8 and PEP 257 are active, and PEP 8 leaves choices to a project, the length of a line among them, which the repository configuration settles (STND.PY.1). The idioms of this standard come from the Programming Recommendations of PEP 8, from PEP 257, from the typing PEPs through the typing specification, and, for scientific code, from SPEC 7 of the Scientific Python project and the logging guide of the Python documentation. The Zen of Python, PEP 20, informs review and decides nothing mechanically, so the standard does not cite it. STND.PY.2 asks the linter to check the agreement of documented parameters and return values with each function; agreement of the documented exceptions is left to review.

Names from notation. PEP 8 names constants and classes by case, and NUMER.4 asks for names that map to the notation of the equations, so a matrix "A" or an operator "K" keeps its case (STND.PY.1, STND.DOCS.12). A list of those names in the settings of the naming rules of the linter keeps each use free of a suppression comment, and a long line of displayed mathematics in a docstring takes a coded suppression (STND.PY.8).

Grouping. STND.CODE.13 groups the statements of each function body into blocks of one step each, and applies to Python as to every language. PEP 8 asks for blank lines in functions "sparingly, to indicate logical sections", which is the same rule. A formatter that keeps single blank lines inside a function keeps the grouping that the author makes; one that inserts a blank line before a nested definition inserts it under the exception of STND.CODE.13. A table of constants or a matrix kept in aligned columns is excluded from formatting at that statement only, by the suppression comment of the formatter.

Strict type checking. The term lists the findings by outcome, so that the project's choice of checker meets it by its settings. A dependency that carries no annotations makes the values it returns of the dynamic type, so the repository configuration gives the checker stubs, which are development tools in the dependency record (STND.DEPS.9), or a per-module override that relaxes that report for that dependency alone, with its reason (STND.PY.5). Existing source that does not pass is listed once by module in the repository configuration, and the list shrinks as changes touch the modules (STND.PY.6); the change that adopts strict checking writes the first list. Notebooks are outside the checking of STND.PY.5, because type checkers read them only through an added tool; this departure from "always" is the custodian's ruling of 2026-10-23, and a module that a notebook imports is library code and is checked. "Any" is the type that the checker does not check; STND.PY.8 asks for the reason at each use, and for "object" where every value is accepted, as the typing best practices advise. A suppression comment that names its rule code does not hide a finding that it was not written for. The py.typed marker of PEP 561 tells the checkers of dependents to read the annotations of a distributed package (STND.PY.7).

Arrays. An array library's type for inputs that a function converts often admits strings and carries no element type, as NumPy's ArrayLike does, which is why STND.PY.9 admits a narrower type, an array of a concrete scalar type, for a numeric input. A concrete scalar type also avoids a type argument that a generic scalar type would need under strict checking. Annotations of shape are checked at run time only where the project adds a run-time checker.

Docstrings. The numpydoc standard fixes the sections and their order, from the short summary to Examples (STND.PY.10), and its format guide says nothing of annotations. STND.PY.11 departs from the practice of major scientific libraries, which state each parameter's type in the docstring as well, by the custodian's ruling of 2026-10-23: a type restated in a Parameters entry is documentation that merely restates the code (INTPR.2) and drifts from it unchecked (INTPR.3), while the annotation is checked. The Returns and Yields sections keep a type, because the numpydoc standard requires one there and reads a one-line entry as a type; that type is written as the annotation writes it, and review compares the two. A docstring validator that reads parameter types from the docstring alone is set not to require them, and the documentation build takes the types from the annotations. The units, shape, and range of valid values of an item appear in its entry only where the item has them (STND.PY.10, STND.CODE.3, INTPR.4).

Doctests. STND.DOCS.13 compares the shown result of an example within a stated tolerance, and the doctest module of the standard library compares text exactly. A test runner that compares each floating-point number to the precision written in the expected output makes the written digits the tolerance; an example that needs another tolerance shows a value that it rounds itself, or the result of a comparison that states its tolerances (STND.PY.12). An example that shows an exception compares its type and not its message, which changes between Python releases. The test runner also collects the examples of documents outside docstrings.

Versions. The project chooses the releases of Python and of its dependencies that it declares, under STND.DEPS.3 and STND.DEPS.4, and the repository configuration records them (STND.PY.13). A distributed package declares the oldest releases it supports so that its dependents know what they are able to combine with it, and its checks run on the oldest declared combination and on the newest combination that its declared ranges admit (STND.PY.14). A new Python release is able to precede the releases of dependencies that support it, which is why the newest combination is limited to releases consistent with one another. An application or an archived study that no other work imports pins its interpreter and packages as dependencies, and a qualified revision stays fixed under STND.DEPS.3. A change of the Python release on which the work runs is a change of the runtime of each execution path under HW.7 and of a pinned revision under STND.DEPS.5, and each run records the exact Python and library revisions (STND.DEPS.8); the lock file of the package installer is the exact record of those revisions (STND.DEPS.10). Running the checks of STND.PY.14 at release, and not at each change, is a deferral of verification under RSRC.12.

Randomness. STND.CODE.2 already asks that the source of randomness arrive through the interface; STND.PY.15 gives its Python form, a generator object passed through a parameter named rng as SPEC 7 names it, and keeps library code off the global random states of its libraries and of the random module, which are hidden global state (DSGN.14). SPEC 7 also lets the rng parameter accept a seed or None; this standard keeps that conversion at the entry point (STND.PY.16), because an integer passed to two functions gives them identical streams and None draws entropy that nobody records. Streams for parallel parts derive from the root seed and the part index through spawning, jump-ahead, or counter-based keys (STND.PY.17, STND.VVUQ.62); a stream chosen by worker or process identity, or copied into forked processes, differs between runs. NUMER.24 governs the evidence that the streams are independent.

Stable values. A generator library is able to keep the stream of a bit generator fixed for a seed while the sampling methods built on it change their output between releases, as the methods of NumPy's Generator have done. A test reference of exact drawn values therefore draws through a stable stream or holds stored data (STND.PY.18). A test whose verdict depends on a seeded stream states in advance how it is repeated after an upgrade of its generator library, because NUMER.26 forbids reseeding as the remedy for a failure without such a rule. The built-in hash of a str or bytes object varies between runs with the hash seed of the interpreter, and with it the iteration order of a set of strings (STND.PY.19).

Comparisons. STND.VVUQ.1 sets the tier of each comparison, STND.VVUQ.5 the relative and absolute parts of the rounding and numerical-error tiers, and STND.VVUQ.3 the agreement of NaNs; STND.PY.20 asks that the Python comparison state those parameters where the code makes it, through a library function or an expression. Defaults differ between comparison functions: math.isclose defaults to an absolute tolerance of zero, and NumPy's assert_allclose treats NaNs as equal while its isclose does not, so a comparison that relies on defaults decides for a reason the reader does not see. Each tolerance is a named constant with its basis beside it (STND.CODE.10, NUMER.11), so that a copied value without a basis stands out in review.

Reporting. Library code writes diagnostics through a module logger and leaves the handlers to the program that imports it (STND.PY.21). A null handler on a library logger also stops the last-resort output of Python, so a warning written only to that logger is silent when the program configures nothing. STND.PY.22 therefore gives the responses to a condition that PRIME.4 lists, of which a record from library code is no part; an entry point whose handler shows the record degrades visibly through it. A warning of a category that the default filters hide, DeprecationWarning outside the main module, PendingDeprecationWarning, ImportWarning, and ResourceWarning among them, is silent and does not count.

Idioms. Python evaluates a default value once, at definition, so a mutable default is state shared across calls (STND.PY.23); None is the usual default, with the object built in the body. The default text encoding of Python has depended on the platform, so a file opened without its encoding is able to read differently on different machines, and an error handler of "ignore" or "replace" substitutes characters silently (STND.PY.24). File system paths held as path objects of the pathlib module are clearer to read than strings joined by hand, and the linter's rules for them are a choice of configuration.

Assertions. STND.PY.25, STND.PY.27, and STND.PY.30 are the Python forms of STND.CODE.6 and STND.CODE.7, each limited to the conditions that PRIME.4 lists. The interpreter removes assert statements under its optimizing mode, an execution setting, so an assertion that checks untrusted input lets invalid input through in that mode (STND.PY.25). An argument of the public interface is untrusted input unless the threat model records otherwise, so a shape check of an argument raises an exception in place of an assertion; that this reaches every function of the public interface at every class, as PRIME.4 does, is the custodian's ruling of 2026-10-23 (PRIN.10). A run-time check of an invariant or postcondition that the work relies on is written as a raise statement for the same reason (STND.PY.26).

Handlers. MemoryError and RecursionError derive from Exception, so a handler of Exception, of BaseException, or of every exception catches the resource exhaustion that PRIME.4 lists, and a suppression context with those classes discards it with no handler at all (STND.PY.27). A handler meets STND.PY.27 by raising the same exception, by raising another one from it, by halting, or by a visible fallback, a computation in smaller pieces with a warning among them. KeyboardInterrupt and SystemExit are the operator's stop and the program's exit, which PRIME.4 does not list, so STND.PY.28 raises them again as a default; a handler that stores an exception to raise it in another thread raises it again there.

Error settings. A process-wide setting of the floating-point error handling of a numerical library, numpy.seterr among them, or of the warnings filters changes the behavior of every other component in the process, which is hidden shared state (STND.PY.29); an entry point is the place for such a setting, and the reason for each suppression is stated at its location (STND.CODE.12). Where the suppressed report signals a condition that PRIME.4 lists, a convergence warning among them, STND.CODE.7 still forbids discarding the condition, so the code detects it by another means, a convergence flag or a check of the result, and responds as STND.PY.22 gives (STND.PY.30); an entry point that ignores invalid-value reports for the whole process and checks each result for finite values meets it.

Relaxed checks. Functions that substitute values, numpy.nan_to_num and numpy.clip among them, are silent defaults under PRIME.4 where the value they replace is invalid input, and STND.CODE.7 governs them there. An argument that disables a finiteness check, check_finite=False of SciPy among them, a compiler option for fast floating-point arithmetic, and a disabled bounds check remove a check or relax the arithmetic, so each carries its reason (STND.PY.31). On the path of a numerical result, a relaxation of floating-point semantics is a performance approximation, which NUMER.16 and NUMER.17 govern.

Floor. STND.PY.22 asks for the responses that PRIME.4 already requires, and STND.PY.25, STND.PY.27, and STND.PY.30 ask only for a response that STND.PY.22 gives, or forbid a construct that leaves a listed condition without one, so none of them asks for work that PRIME.4 does not; that these raise no floor is the custodian's ruling of 2026-10-23 (PRIN.10). They bind at every class, CSQ4 included, as PRIME.4 does.

Class onset. Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, RSRC, or a provision of NUMER, and applies from CSQ3; work of CSQ4 may omit it. STND.PY.26 instantiates the run-time checking of VV.10 and DSGN.2, which STND.CLASS.10 applies from CSQ1, and applies from CSQ1. STND.PY.5 asks for type checking of all code from CSQ3, and the mechanical checking of each contract of a safety-related component, which STND.CLASS.10 applies from CSQ0 under DSGN.3, stays with that row. No default instantiates a prime directive, GUARD, GOV, or a floor obligation, and no provision raises the floor (GOV.11).

Existing source conforms when a change next touches it, other than the strict checking of STND.PY.5, which existing modules reach through the list of STND.PY.6."""

PY = dict(
    id="STND.PY", title="Python standard",
    instantiates=["GOV.18", "GOV.19"],
    sections=[
        ("Purpose and scope", PURPOSE),
        ("Normative and informative parts", NORMATIVE),
        ("Terms", TERMS),
        ("Notes", NOTES),
    ],
    provisions=[
        # Style
        P(1, "Style PEPs as baseline", "Style", """
Python source SHOULD follow the conventions of the style PEPs, with each choice that they leave to a project settled once in the repository configuration (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).
""", ["INTPR.1", "INTPR.4"], refs=["NUMER.4", "STND.DOCS.12"]),
        P(2, "Python linter coverage", "Style", """
The static checks that the repository configuration names for Python under STND.CODE.4 SHOULD include a linter that checks the conventions of the style PEPs that the layout tool of STND.CODE.5 leaves open, the structure of each docstring against the numpydoc standard, and the agreement of the parameters and return values that each docstring documents with its function (INTPR.1, INTPR.3, DSGN.3). That linter SHOULD also check each provision of this standard whose compliance a rule of the linter decides (DSGN.3).
""", ["INTPR.1", "INTPR.3", "DSGN.3"], refs=["STND.CODE.4", "STND.CODE.5"]),
        # Types
        P(3, "Annotation coverage", "Types", """
Other than a parameter named self or cls, each parameter and the return value of each function and method that a def statement defines SHOULD carry an annotation (DSGN.1, DSGN.3). Other than a member of an enumeration, each module-level name and each class attribute whose type the type checker does not infer from its assigned value SHOULD carry an annotation (DSGN.1).
""", ["DSGN.1", "DSGN.3"]),
        P(4, "Agent annotations", "Types", """
An agent SHALL write an annotation of each parameter and return value that STND.PY.3 covers in each Python function and method that it writes or changes, or the form that an alternative adopted by a project instrument in place of STND.PY.3 requires (GOV.48, DSGN.1).
""", ["GOV.48", "DSGN.1"], refs=["STND.PY.3"], mode="binding"),
        P(5, "Strict type checking", "Types", """
The static checks that the repository configuration names for Python under STND.CODE.4 SHOULD include strict type checking of the library code, the tests, and the scripts of the work (DSGN.3). Where a dependency of the work carries no annotations, the repository configuration SHOULD give the type checker stubs for it that the dependency record lists, or an override for the modules of that dependency that names the finding it relaxes and its reason (DSGN.3, REPRO.7).
""", ["DSGN.3", "REPRO.7"], refs=["STND.CODE.4"]),
        P(6, "Modules exempted from strict checking", "Types", """
Where a module of the work does not pass strict type checking, the repository configuration SHOULD name it, with its reason, in one list of exempted modules (REPRO.7). Other than a module that a change of a dependency or the change that adopts strict checking makes fail, a change SHOULD NOT add a module to that list (DSGN.3).
""", ["REPRO.7", "DSGN.3"]),
        P(7, "Typed package marker", "Types", """
Each distributed package SHOULD include a py.typed marker file in its distribution (DSGN.1).
""", ["DSGN.1"]),
        P(8, "Reasoned dynamic types and suppressions", "Types", """
Where an annotation uses the dynamic type "Any", a comment at that annotation SHOULD state why the typing specification does not express the type (REPRO.7). Where a parameter accepts every value, its annotation SHOULD be object (DSGN.1). Each comment that suppresses a finding of the linter or of the type checker SHOULD name the code of each rule that it suppresses, beside the reason that STND.CODE.4 asks for (REPRO.7).
""", ["REPRO.7", "DSGN.1"], refs=["STND.CODE.4"]),
        P(9, "Array annotations", "Types", """
Each parameter that a function converts to an array SHOULD be annotated with the type that its array library gives for inputs convertible to an array, or with a narrower type (DSGN.1). Each other parameter, return value, module-level name, and class attribute that holds an array SHOULD be annotated with the array type of its array library and the scalar type of its elements (DSGN.1).
""", ["DSGN.1"]),
        # Docstrings
        P(10, "Numpydoc docstrings", "Docstrings", """
Each module, class, function, and method of the public interface SHOULD carry a docstring in the format of the numpydoc standard, with its sections in the order that the standard gives, that documents each parameter, each returned or yielded value, and each exception that the function raises with the condition under which it raises it (INTPR.1, INTPR.3). Each docstring of an interface that STND.CODE.3 covers SHOULD state its contract in the entries of its items, with the units, the shape, and the range of valid values that each item has and that its annotation does not carry (DSGN.1, INTPR.4).
""", ["INTPR.1", "INTPR.3", "DSGN.1", "INTPR.4"], refs=["STND.CODE.3"]),
        P(11, "Parameter types in annotations", "Docstrings", """
Each entry of the Parameters and Attributes sections of a docstring SHOULD describe its item without restating the type that the annotation of the item gives (INTPR.3). Each entry of the Returns and Yields sections SHOULD give, in the type position that the numpydoc standard requires, the type that the return annotation states for that value (INTPR.3).
""", ["INTPR.3"]),
        P(12, "Doctest examples", "Docstrings", """
Each example of the work documentation that STND.DOCS.13 runs SHOULD be a doctest example that the test runner collects (INTPR.3, VV.8). Each floating-point value that such an example shows SHOULD be rounded by the example to the digits that its stated tolerance admits, or compared by the test runner to the precision that it shows (INTPR.3, VV.8).
""", ["INTPR.3", "VV.8"], refs=["STND.DOCS.13"]),
        # Versions
        P(13, "Declared Python releases", "Versions", """
Each distributed package SHOULD declare in its package metadata the oldest release of Python and of each dependency that it supports, as chosen under STND.DEPS.3 and reviewed under STND.DEPS.4 (REPRO.9).
""", ["REPRO.9"], refs=["STND.DEPS.3", "STND.DEPS.4"]),
        P(14, "Checks on declared releases", "Versions", """
The checks of each release of a distributed package SHOULD run on the oldest declared release of Python with the oldest declared release of each dependency that it uses, and on the newest releases of Python and of those dependencies that its declared ranges admit and that are consistent with one another (VV.8).
""", ["VV.8"]),
        # Randomness
        P(15, "Generator arguments", "Randomness", """
Each function of library code that draws random numbers SHOULD draw them only from a generator object that it receives through a parameter named rng (DSGN.17, DSGN.16, DSGN.14). Library code SHOULD leave unseeded each global random state of its libraries and of the random module of the standard library (DSGN.14).
""", ["DSGN.17", "DSGN.16", "DSGN.14"]),
        P(16, "Generators built at entry points", "Randomness", """
Other than a generator that STND.PY.17 derives, each generator that the work constructs SHOULD be constructed at an entry point, from a seed that the record of the run holds (DSGN.17, REPRO.1). Where an entry point seeds a generator from fresh entropy, it SHOULD record that entropy with the run (REPRO.1).
""", ["DSGN.17", "REPRO.1"], refs=["STND.PY.17"]),
        P(17, "Streams for parallel parts", "Randomness", """
Where work divided into parts draws random numbers, each part SHOULD draw from a generator that a spawning, jump-ahead, or counter-based facility of its generator library derives from the root seed of the run and the index of the part, as STND.VVUQ.62 recommends (DSGN.17, REPRO.3).
""", ["DSGN.17", "REPRO.3"], refs=["STND.VVUQ.62"]),
        P(18, "Exact values from random draws", "Randomness", """
Each test reference and each documentation example that holds exact values drawn from a random number generator SHOULD draw them through a bit generator and a method whose output for a given seed stays the same across the releases of the generator library that the work supports, or hold the values as recorded data (REPRO.3, REPRO.6). Where the verdict of a test depends on the stream of a seeded generator, the test SHOULD state, before its first failure, the rule by which it is repeated after a change of the release of its generator library, as NUMER.26 requires of a repetition (VV.3).
""", ["REPRO.3", "REPRO.6", "VV.3"], refs=["NUMER.26"]),
        P(19, "Values unstable across runs", "Randomness", """
Outputs, recorded data, and test references of the work SHOULD NOT hold values that the built-in hash returns for a string (REPRO.3, REPRO.6). Each reported result SHOULD be independent of the iteration order of each set of strings on its path (REPRO.3).
""", ["REPRO.3", "REPRO.6"]),
        # Comparisons
        P(20, "Tolerance parameters stated", "Comparisons", """
Each comparison of floating-point values within a tolerance, by a function or by an expression, SHOULD state the parameters of its tier of STND.VVUQ.1, the relative and the absolute part of STND.VVUQ.5 for the rounding and numerical-error tiers, and its treatment of a NaN under STND.VVUQ.3 (NUMER.11, VV.3, SIMPL.6). Each such tolerance SHOULD be a named constant that carries its basis under NUMER.11, as STND.CODE.10 recommends (NUMER.11, REPRO.7). A comparison of exact values, or one that the bitwise tier of STND.VVUQ.1 admits, MAY use the equality operators (VV.3).
""", ["NUMER.11", "VV.3", "SIMPL.6", "REPRO.7"], refs=["STND.VVUQ.1", "STND.VVUQ.5", "STND.VVUQ.3", "STND.CODE.10"]),
        # Reporting
        P(21, "Logging in library code", "Reporting", """
Library code SHOULD write its diagnostics, its progress, and its decisions through a logger of the logging module named for its module, in place of writing to standard output (DSGN.16, RSRC.10). The only handler that library code attaches to its loggers SHOULD be logging.NullHandler (DSGN.16).
""", ["DSGN.16", "RSRC.10"]),
        P(22, "Python responses to listed failures", "Reporting", """
Where code detects a condition that PRIME.4 lists, it SHALL raise an exception, halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, degrade visibly with a diagnosis, or return the condition in its result (PRIME.4). Where the visible degradation is a warning, its category SHALL be one that the default warnings filters show (PRIME.4). A record that library code writes to a logger SHALL NOT be the only visible degradation (PRIME.4).
""", ["PRIME.4"], refs=["PRIME.13"], mode="binding"),
        # Source idioms
        P(23, "Immutable parameter defaults", "Source idioms", """
The default value of each parameter SHOULD be immutable (DSGN.14).
""", ["DSGN.14"]),
        P(24, "Named text encodings", "Source idioms", """
Each call that opens, decodes, or encodes text SHOULD name its encoding and leave its error handler strict (SIMPL.6, REPRO.3).
""", ["SIMPL.6", "REPRO.3"]),
        # Failures
        P(25, "Assertions on untrusted input", "Failures", """
Code SHALL NOT check untrusted input with an assert statement (PRIME.4, DSGN.2).
""", ["PRIME.4", "DSGN.2"], mode="binding"),
        P(26, "Run-time checks without assert", "Failures", """
Each run-time check of an invariant or a postcondition that VV.10 or DSGN.2 asks of the work SHOULD be written as a raise statement under a condition, in place of an assert statement (VV.10, DSGN.2).
""", ["VV.10", "DSGN.2"]),
        P(27, "Exhaustion caught by handlers", "Failures", """
Where a handler catches MemoryError or RecursionError by naming it, a class from which it derives, or no class, it SHALL respond as STND.PY.22 requires (PRIME.4). Each class that a suppression context names SHALL be neither MemoryError, nor RecursionError, nor a class from which either derives (PRIME.4).
""", ["PRIME.4"], refs=["STND.PY.22"], mode="binding"),
        P(28, "Interrupts raised again", "Failures", """
Where an except clause catches KeyboardInterrupt or SystemExit, by naming it, by naming BaseException, or by naming no class, its handler SHOULD raise that exception again (SIMPL.6).
""", ["SIMPL.6"]),
        P(29, "Scoped error settings", "Failures", """
Outside an entry point, each change that code makes to the warnings filters, or to the floating-point error handling of a numerical library, SHOULD be confined to a with statement that encloses only the operations it concerns (DSGN.14).
""", ["DSGN.14"]),
        P(30, "Suppressed reports of listed failures", "Failures", """
Where code suppresses a warning or an error report that signals a condition that PRIME.4 lists, it SHALL detect each such condition by another means and respond to it as STND.PY.22 requires (PRIME.4).
""", ["PRIME.4"], refs=["STND.PY.22"], mode="binding"),
        P(31, "Relaxed numerical checks", "Failures", """
Each use of an argument that disables a finiteness or validity check of a numerical library, of a disabled bounds check, or of a compiler option that relaxes floating-point semantics SHOULD state at its location why each input that it covers is valid (REPRO.7, DSGN.2).
""", ["REPRO.7", "DSGN.2"]),
    ],
)

NEW_DOCS_PY = [PY]
