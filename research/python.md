# Research note: Python language standard (LVL2) inputs

Role: research agent (STND.CREW), delegation depth 1.
Date of research: 2026-10-22. All URLs were accessed on that date.
Scope: read-only retrieval. No paywalled pages, mirrors, archives, or caches were used.

## 0. How to read this note

- The fetch tool returns a processed summary of each page, not the raw page. Where a fact matters for a normative choice, I marked it **[verify]** if the summary was thin, truncated, or came from a secondary source.
- Items marked **[local test]** were checked by running Ruff 0.16.8 and Black 26.5.1 already installed on this machine, on throwaway files in the scratchpad. No project file was touched.
- The custodian's four directions are cited as D1 to D4:
  - D1: use PEP standards for style and idioms, enforced mechanically where possible.
  - D2: always use types and typechecking.
  - D3: use numpy docstring style.
  - D4: format code to be readable according to logical grouping of instructions.

## 1. Summary of the main findings

1. PEP 8 (Active), PEP 257 (Active), and PEP 20 (Active) are all still the style and idiom PEPs. PEP 8 was last modified 2025-04-04. PEP 8 and PEP 257 contain exactly the allowances the custodian needs: a team may raise the code line limit to 99, and blank lines inside functions are explicitly allowed "sparingly, to indicate logical sections" (D4).
2. Python 3.15.0 was released 2026-10-09. 3.14 is the previous release, 3.10 reached end of life 2026-10-01, and 3.11 through 3.13 are in security-only status. SPEC 0 (which supersedes NEP 29) says to drop Python 3.12 in 2026 Q4 and NumPy 2.2 in 2026 Q4. NumPy 2.5.0 supports Python 3.12 to 3.14.
3. The typing PEPs through 3.15 are all Final (including 649/749, 728, 747, 800). Several new drafts exist but none should be relied on yet. The typing specification at typing.python.org is maintained by the Typing Council (PEP 729). I could not find an explicit statement that it is "normative". Type checkers are explicitly free to deviate. The safe wording is "the typing specification is the current reference, PEPs are the history".
4. Ruff is the single tool that can enforce most of D1, D3, and D4 (lint, format, imports, docstring conventions). It does not type check. A real type checker is needed for D2. Current state:
   - Ruff 0.16.x is current.
   - mypy 2.4.0 is current.
   - pyright is at 1.1.414.
   - basedpyright 1.40.x.
   - Pyrefly reached 1.0.0 on 2026-05-12.
   - ty is still 0.0.x (0.0.81 on 2026-09-14).
5. **Ruff's pydocstyle numpy convention does not check that documented parameters match the signature.** It disables D417. Checking that requires either Ruff's preview `DOC` rules (pydoclint) or numpydoc's own validator (PR01 to PR03). **[local test]** confirms: with `convention = "numpy"`, an undocumented parameter produced no error, while `--preview --select DOC` caught a missing Returns section and an extraneous documented parameter.
6. numpydoc's format guide says nothing about how docstring types relate to signature annotations. The numpydoc validator (main branch source) raises PR04 ("Parameter has no type") from the docstring only, so an annotation alone does not satisfy it. The custodian must decide between types in both places and types only in annotations (section 6).
7. Ruff and Black both collapse runs of blank lines inside a function to one blank line and keep a single blank line. **[local test]** Deliberate grouping with one blank line therefore survives formatting. `# fmt: skip`, `# fmt: off`, and the magic trailing comma give further control.
8. Not mechanizable: whether the grouping is logical, whether names and comments are good, whether docstring prose is clear and consistent with the code, whether types are as precise as they could be, and the idiom choices in section 8 that depend on intent. Section 9 lists these.

## 2. PEPs and standards, with status

Status was read from each PEP page on 2026-10-22.

### 2.1 Style and idiom

| PEP | Title | Status | Notes |
|---|---|---|---|
| 8 | Style Guide for Python Code | Active (Process) | Last modified 2025-04-04. 79 columns for code and 72 for comments and docstrings. A team may raise code to 99 if comments and docstrings stay at 72. Consistency within a module and project outranks the guide. |
| 257 | Docstring Conventions | Active (Informational) | Triple double quotes, summary line, blank line, description. It leaves section formatting to other conventions (numpydoc in our case). |
| 20 | The Zen of Python | Active (Informational) | Non-binding. Cannot be enforced mechanically. |

Quote from PEP 8 relevant to D4: "Use blank lines in functions, sparingly, to indicate logical sections." It also says to keep imports at the top, grouped as standard library, third party, local, with a blank line between groups.

### 2.2 Typing PEPs (all read from https://peps.python.org/topic/typing/)

| PEP | Title | Status | Python |
|---|---|---|---|
| 484 | Type Hints | Final | 3.5 |
| 526 | Variable annotations | Final | 3.6 |
| 544 | Protocols | Final | 3.8 |
| 561 | Distributing type information (py.typed, -stubs) | Final | 3.7 |
| 585 | Generics in standard collections | Final | 3.9 |
| 604 | X \| Y unions | Final | 3.10 |
| 612 | ParamSpec | Final | 3.10 |
| 646 | Variadic generics (TypeVarTuple) | Final | 3.11 |
| 655 | Required / NotRequired | Final | 3.11 |
| 673 | Self | Final | 3.11 |
| 692 | TypedDict for \*\*kwargs | Final | 3.12 |
| 695 | Type parameter syntax (`class Box[T]`, `type X = ...`) | Final | 3.12 |
| 696 | Type parameter defaults | Final | 3.13 |
| 698 | `@override` | Final | 3.12 |
| 702 | `@deprecated` | Final | 3.13 |
| 705 | ReadOnly TypedDict items | Final | 3.13 |
| 742 | TypeIs | Final | 3.13 |
| 563 | Postponed evaluation of annotations | Superseded | 3.7 |
| 649 | Deferred evaluation via descriptors | Final | 3.14 |
| 749 | Implementing PEP 649 | Final | 3.14 |
| 728 | TypedDict with typed extra items | Final | 3.15 |
| 747 | Annotating type forms (TypeForm) | Final | 3.15 |
| 800 | Disjoint bases | Final | 3.15 |
| 729 | Typing governance process | Active (Process) | n/a |

Drafts (not for use in a standard yet): 718 (subscriptable functions, 3.16), 746 (Annotated metadata checking, 3.15), 764 (inline typed dicts, 3.15), 767 (read-only attributes, 3.15), 781 (TYPE_CHECKING built-in, 3.15), 821 (unpacked TypedDict in Callable, 3.15), 827 (type manipulation, 3.16), 835 (Annotated shorthand, 3.16), 846 (docstrings for type aliases, 3.16), 849 (expressive type expressions, 3.16). Rejected or withdrawn: 677, 724, 727. Listed target versions on drafts can change.

PEP 649/749 details that affect a Python standard:
- In 3.14, annotations are evaluated lazily and forward references no longer need quotes. Introspection goes through the new `annotationlib` module.
- `from __future__ import annotations` still works in 3.14. Per PEP 749, it is deprecated no sooner than the first release after Python 3.13 reaches end of life (October 2029), and removed at least two releases after that. A project with a floor of 3.13 or lower still needs either quotes or the future import for forward references.
- Runtime consumers of annotations (pydantic, beartype, typeguard, dataclass-like tools) can break on stringized annotations. This is a design point for the custodian (open question Q4).

PEP 695 notes: `typing.TypeAlias` is proposed for deprecation in favor of the `type` statement. Module-level `TypeVar` is not deprecated. Ruff has rules UP040, UP046, and UP047 (confirmed present in Ruff 0.16.8 **[local test]**) that flag the old forms when the target version is 3.12 or later.

Typing specification (https://typing.python.org/en/latest/spec/):
- It is assembled from the specification sections of PEP 484 and later typing PEPs. It was created after PEP 729 was accepted.
- The Typing Council (3 to 5 members) maintains it and the conformance test suite. Substantive changes need Council approval.
- PEP 729 says the Council "has no direct authority over type checkers" and that checkers may deviate if they document it.
- I did not find the word "normative" on the spec pages I could read. Suggested wording for the standard: "Follow the typing specification at typing.python.org. Where it is silent, follow the cited PEP."

### 2.3 Packaging and environment PEPs

| PEP | Topic | Status | Notes |
|---|---|---|---|
| 517 | Build backend interface | Final | Authoritative text is still the PEP. |
| 518 | `[build-system] requires` | Final | Same. |
| 621 | `[project]` metadata | Final | Historical; canonical spec is the PyPA "pyproject.toml specification". |
| 639 | SPDX `license` expression, `license-files` | Final | Historical; deprecates the `license = {text=...}` / `{file=...}` forms and License classifiers. |
| 735 | `[dependency-groups]` | Final | Historical; spec on PyPA. Fits dev, test, docs, typing groups. |
| 751 | `pylock.toml` lock files | Final | Historical; spec on PyPA. Tool support was not in the PEP text. **[verify]** |
| 723 | Inline script metadata (`# /// script`) | Final | Historical; canonical spec on PyPA. Relevant for single-file scripts only. |
| 668 | Externally managed environments | Final | Use virtual environments; never `--break-system-packages`. |
| 703 | Free-threaded CPython (`--disable-gil`) | Final | 3.13; historical, now the free-threading HOWTO. |
| 779 | Supported status for free-threaded builds | Final | 3.14 enters "Phase II": officially supported, still optional. Phase III (default) needs another PEP. |

Free-threading in practice (docs.python.org HOWTO): supported since 3.13 as experimental, officially supported from 3.14. Single-thread overhead is about 1% to 8%. Extension modules that are not marked safe re-enable the GIL. NumPy 2.5 states support for the free-threaded stable ABI (PEP 803, new in 3.15). For the standard: free-threading is a compatibility test target, not a requirement, unless the custodian says otherwise.

Other 3.15 changes that touch style (from What's New 3.15, **[verify]** since the excerpt I received was truncated before the typing section):
- PEP 686: UTF-8 is the default encoding, but code should still pass `encoding=` to `open()`.
- PEP 810: explicit lazy imports (`lazy import x`).
- PEP 798: unpacking in comprehensions.
- PEP 661: `sentinel`.
- PEP 814: `frozendict`.
- `re.match` is soft-deprecated in favor of `re.prefixmatch`.
- `profile` is deprecated.

Python 3.14: t-strings (PEP 750); PEP 758 allows `except A, B:` without parentheses (Ruff's 2026 style removes the parentheses when the target version is 3.14 or later, which may surprise people on older readers).

## 3. Python and NumPy versions

| Item | Fact | Source |
|---|---|---|
| Python 3.15 | Final released 2026-10-09; status "bugfix"; end of life scheduled 2031-10 | devguide; PEP 790 (schedule) |
| Python 3.14 | Released 2025-10-07; latest bugfix 3.14.8 (2026-10-01); security until 2030-10; last bugfix with installers 3.14.14 (2027-10-05) | devguide; PEP 745 |
| Python 3.13 | Security-only; end of life 2029-10 | devguide |
| Python 3.12 | Security-only; end of life 2028-10 | devguide |
| Python 3.11 | Security-only; end of life 2027-10 | devguide |
| Python 3.10 | End of life 2026-10-01 | devguide |
| Python 3.16 | In development; first release scheduled 2027-10-06 | devguide |
| NumPy | 2.5.0 current (docs built 2026-06-28; SPEC 0 table says June 2026); 2.4.x latest patch 2.4.6. 2.5.0 supports Python 3.12 to 3.14; 3.15 support starts at its first release candidate. | numpy.org release notes |

SPEC 0 (Endorsed by IPython, Matplotlib, NetworkX, NumPy, scikit-image, SciPy, xarray, Zarr-Python) supersedes NEP 29. Rules: drop Python 3 years after its release, and drop core packages 2 years after release. Counts feature releases only.

| Package | Released | Recommended drop quarter |
|---|---|---|
| Python 3.12 | Oct 2023 | 2026 Q4 |
| Python 3.13 | Oct 2024 | 2027 Q4 |
| Python 3.14 | Oct 2025 | 2028 Q4 |
| NumPy 2.2 | Dec 2024 | 2026 Q4 |
| NumPy 2.3 | Jun 2025 | 2027 Q2 |
| NumPy 2.4 | Dec 2025 | 2027 Q4 |
| NumPy 2.5 | Jun 2026 | 2028 Q2 |

Implication for minimum versions: for a project started now, SPEC 0 points to a floor of Python 3.13 and NumPy 2.3. Python 3.13 also gives native `TypeIs`, `ReadOnly`, `warnings.deprecated`, and PEP 696 defaults without `typing_extensions`. A floor of 3.12 is still inside the SPEC 0 window for a few more weeks. This is a custodian decision (Q1).

## 4. Tools and their current state

### 4.1 Ruff (linter and formatter)

- Current: 0.16.6 on the GitHub releases page (2026-09-03). Version 0.16.8 is installed here. Ruff is still 0.x, so the project must pin the version.
- 0.15.0 (the "2026 style guide") changed formatting: one blank line at the start of a function body is now preserved; `# fmt: skip` applies to the whole logical line; lambda layout changed; parentheses around multiple exception types are removed for Python 3.14+ targets; block suppressions `ruff: disable[CODE]` are stable.
- 0.16.0 expanded the default rule set from 59 to 413 rules and removed 18 opinionated E and F rules from the default. It also formats Python code blocks in Markdown. Any config that relies on defaults will change across this boundary, so **select rules explicitly**.
- The Scientific Python guide says rule set `I` (import sorting) is on by default since Ruff 0.16. The 0.16.0 release post I fetched does not confirm this. **[verify]** Do not rely on it; select `I` explicitly.
- Formatter vs Black: designed as a near drop-in. Differences are listed at docs.astral.sh/ruff/formatter/black/ (it formats inside f-string braces, removes blank lines at the start of blocks in some cases, expands statements with trailing comments, and so on). Choose one formatter. Recommendation: Ruff format, because one tool then covers lint, imports, and format, and the format is fast enough for pre-commit.
- Blank lines, magic trailing comma **[local test]**:
  - Input had one blank line after `def f(x):`, a blank line between statements, and a run of three blank lines before `b = a * 2`.
  - Ruff 0.16.8 and Black 26.5.1 gave identical output: the single blank lines were kept, the run of three collapsed to one, and a trailing comma in a list forced one element per line (`[1, 2,]` was exploded).
  - Black's docs state the magic trailing comma and the `-C` / `skip-magic-trailing-comma` option; Ruff's equivalent is `format.skip-magic-trailing-comma`.
- E303 (too many blank lines) is **preview** in Ruff. It is unnecessary when the formatter runs, since the formatter already collapses extra blank lines.
- Line length: the default is 88 (E501 and the formatter). The formatter treats it as a best-effort limit. PEP 8 says 79 and allows up to 99 by team agreement. SciPy uses 88. W505 (`doc-line-too-long`) is stable but only active if `lint.pycodestyle.max-doc-length` is set **[local test]**. PEP 8's 72 for comments and docstrings can therefore be enforced mechanically. numpydoc says 75, so 72 satisfies both.
- Docstring rules `D` (pydocstyle): off by default. With `convention = "numpy"`, Ruff disables these (from `ruff_linter/src/rules/pydocstyle/settings.rs` on main): D107 (init docstring), D203, D212 and D213 (summary line placement; both are ignored, so numpydoc's flexibility is accepted), D402, D413, D415, D416, D417. Note that D417 (undocumented parameter) is off, which is why signature agreement needs another tool.
- Preview `DOC` rules (pydoclint port) confirmed in Ruff 0.16.8 **[local test]**: DOC102 (extraneous documented parameter), DOC201 (missing Returns), DOC202 (extraneous Returns), DOC402/DOC403 (Yields), DOC501/DOC502 (Raises). They need `preview = true` and are unstable.
- Other useful rule families confirmed to exist **[local test]**: ANN001/ANN201/ANN401 (annotations, `Any`), NPY002 (legacy `np.random`), NPY201 (NumPy 2 deprecations), B006 (mutable default), T201 (print), PTH (pathlib), UP040/046/047 (PEP 695 forms), FA102 (future annotations), TC (typing-only imports), ERA001 (commented-out code), PGH (blanket ignores), RUF100 (unused `noqa`).
- Ruff is not a type checker. Its FAQ says to pair it with ty, mypy, pyright, or Pyre.

### 4.2 Type checkers

| Tool | Version / state (2026-10-22) | Notes |
|---|---|---|
| mypy | 2.4.0 stable. 2.0 turned on `--local-partial-types` and `--strict-bytes` by default and dropped targeting 3.9. 2.4 added Python 3.15 syntax support, a native parser, and non-experimental parallel checking. | `--strict` enables 13 flags (below). `--warn-unreachable` and `--disallow-any-explicit` are not part of it. PEP 728 `extra_items` was still missing in the 2.4 notes. |
| pyright | 1.1.414 (September 2026; the year was inferred from the release sequence, **[verify]**). | Modes: off, basic, standard (default), strict. Strict turns on the `reportUnknown*`, `reportMissingTypeStubs`, `reportUnusedImport`, `reportPrivateUsage`, `reportMissingParameterType`, `reportMissingTypeArgument`, and others. |
| basedpyright | 1.40.x documented | Adds modes `recommended` (default) and `all`, plus rules `reportAny`, `reportExplicitAny`, `reportUnusedParameter`, `reportImplicitOverride`. `recommended` turns off `# type: ignore` comments. |
| Pyrefly (Meta) | 1.0.0 released 2026-05-12 ("Status: STABLE"); semantic versioning; monthly minors. Project says conformance went from about 70% (beta) to over 90%. A third-party comparison (pydevtools, July 2026) reports about 96% for Pyrefly 1.1.0 and about 76% for ty 0.0.50. | Presets off, basic, legacy, default, strict. An unconfigured project gets `basic`, which silences most errors, so always set a preset. No mypy plugins. |
| ty (Astral) | Beta announced 2025-12-16; still 0.0.x (0.0.81 on 2026-09-14). Astral said a Stable release was targeted "the following year" (2026). | Breaking changes can land between 0.0.x releases. Gaps cited by the third party: generics, Protocols, aliases. |

mypy `--strict` flags (mypy docs, "may change between releases"): disallow-any-generics, disallow-subclassing-any, disallow-untyped-calls, disallow-untyped-defs, disallow-incomplete-defs, check-untyped-defs, disallow-untyped-decorators, warn-redundant-casts, warn-unused-ignores, warn-return-any, no-implicit-reexport, strict-equality, extra-checks.

Maturity assessment (my judgment, based on the above):
- mypy and pyright/basedpyright are the mature, gating-grade options.
- Pyrefly is stable per its own 1.0 label, but young; good as a second, non-gating checker.
- ty is pre-1.0 and should not gate merges.

### 4.3 numpydoc and doctest tooling

- numpydoc: 1.10.0 stable (2025-12-02); 1.11.0rc0 exists (2026-06-10). Requires Python 3.10+ and Sphinx 6+. The release notes page failed to load, so I could not check what changed between them.
- Validation (`numpydoc validate`, `numpydoc lint` pre-commit hook `numpydoc-validation`, Sphinx `numpydoc_validation_checks`) uses these codes (verbatim from `numpydoc/validate.py` on main): GL01 to GL10, SS01 to SS06, ES01, PR01 to PR10, RT01 to RT05, YD01, SA01 to SA04, EX01. Config lives in `[tool.numpydoc_validation]` with `checks`, `exclude`, `exclude_files`, and `override_<CODE>`. Inline: `# numpydoc ignore=EX01,SA01,ES01`.
- The validator reads types for PR04 from the docstring only; it does not accept annotations. Source states `PR04: Parameter "{param_name}" has no type`. So name-only Parameters entries need PR04 excluded, and then PR06 and others do not apply.
- pytest doctest: `--doctest-modules` runs docstring examples; `doctest_optionflags` (NORMALIZE_WHITESPACE, ELLIPSIS; pytest also adds NUMBER for float comparison at written precision); `doctest_namespace` fixture in `conftest.py` can inject `np`.
- pre-commit: current docs show 4.7.0. Hooks pin `rev`. `pre-commit.ci` can autofix and autoupdate.
- sphinx-autodoc-typehints (tox-dev): reads annotations and writes them into numpydoc Parameters/Returns fields; load numpydoc first. Current docs require Python 3.12+ and Sphinx 9.1+.

## 5. Recommended enforced configuration (D1 to D4)

This is a proposal for the custodian to adopt or amend. It was exercised only in part: the Ruff `[tool.ruff]` block was run against a sample file **[local test]**. The mypy, pytest, and numpydoc blocks were not executed because those tools are not installed here.

```toml
[project]
requires-python = ">=3.13"        # Q1: SPEC 0 says drop 3.12 in 2026 Q4

[dependency-groups]
dev = ["ruff==0.16.*", "mypy>=2.4,<3", "pytest>=9", "numpydoc>=1.10", "pre-commit"]

[tool.ruff]
line-length = 88                  # PEP 8 allows up to 99 for agreed teams; 88 matches formatter default
target-version = "py313"
preview = false                   # use per-rule preview selection below instead

[tool.ruff.format]
docstring-code-format = true      # formats doctest code in docstrings
docstring-code-line-length = "dynamic"
# keep magic trailing comma (default): it is the author's grouping tool

[tool.ruff.lint]
select = [
  "E", "W", "F",                  # pycodestyle, pyflakes (PEP 8 mechanics)
  "I",                            # isort
  "N",                            # pep8-naming
  "D",                            # pydocstyle (numpy convention below)
  "UP",                           # pyupgrade (PEP 585, 604, 695 forms)
  "ANN",                          # annotations required (D2)
  "B", "C4", "SIM", "RET", "PIE", "RUF",
  "NPY", "PTH", "T20", "LOG", "G", "EM", "TC", "FA", "PGH", "ERA",
  "PT",                           # pytest style
  "PL",                           # pylint subset; see ignore list
]
extend-select = ["DOC102", "DOC201", "DOC202", "DOC402", "DOC403", "DOC501", "DOC502"]  # preview rules
preview = true                    # needed only so the DOC rules can be selected; Q6
ignore = ["PLR09", "PLR2004"]     # Scientific Python guide ignores these
# Avoid formatter conflicts: COM812, ISC001 and similar should not be selected.

[tool.ruff.lint.pycodestyle]
max-doc-length = 72               # PEP 8: comments and docstrings; numpydoc says 75
[tool.ruff.lint.pydocstyle]
convention = "numpy"
[tool.ruff.lint.per-file-ignores]
"tests/**" = ["D", "T20", "PLR2004"]    # Q7: tests still need annotations under D2?

[tool.mypy]
files = ["src"]
python_version = "3.13"
strict = true
warn_unreachable = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
# Q3: disallow_any_explicit = true is possible but strict; ANN401 already bans Any in signatures

[tool.pytest.ini_options]         # or [tool.pytest] with strict = true on pytest 9+
minversion = "9.0"
addopts = ["-ra", "--strict-markers", "--strict-config", "--doctest-modules"]
xfail_strict = true
filterwarnings = ["error"]
log_level = "INFO"
testpaths = ["src", "tests"]
doctest_optionflags = ["NORMALIZE_WHITESPACE", "ELLIPSIS"]

[tool.numpydoc_validation]
checks = ["all", "ES01", "SA01", "EX01"]   # "all" except the listed codes; Q5 decides PR04, RT02
exclude = ['\.__init__$', '\.__repr__$']
```

Pre-commit (versions to be pinned at adoption): `ruff-check` with `--fix`, `ruff-format`, `mypy` (local hook so it sees the environment), `numpydoc-validation`, and the standard whitespace and TOML checks. Pre-commit is advisory; CI must run the same commands and fail on any finding. The Scientific Python guide's own example pins `ruff-pre-commit` and uses `args: ["--fix", "--show-fixes"]`.

Alternatives and additions:
- basedpyright `typeCheckingMode = "recommended"` or `"all"` as a second gate. It adds `reportAny`, which is the stricter way to meet "avoid Any". Pyrefly with `preset = "strict"` can run non-gating. ty should be run non-gating or not at all until it is 1.0.
- `sp-repo-review` (Scientific Python guide) as a repository-level check, run with `pipx run 'sp-repo-review[cli]' .`. I could not retrieve its check list or categories. **[verify]**

## 6. Docstrings (D3) and how they relate to annotations

numpydoc format guide (https://numpydoc.readthedocs.io/en/latest/format.html):
- Section order: Short summary, Deprecation warning, Extended summary, Parameters, Returns, Yields, Receives, Other Parameters, Raises, Warns, Warnings, See Also, Notes, References, Examples.
- Short summary: one line; no variable or function names. Extended summary describes functionality, not implementation.
- Parameters: `name : type`, with a space before the colon. Omit the colon if there is no type. Use `optional` or `default ...` for defaults; use braces for fixed value sets; combine parameters with identical type and description (`x1, x2 : array_like`). Keep the leading `*` or `**` for variadics, with no type.
- `array_like` is the numpydoc term for anything convertible to an ndarray.
- Returns and Yields: the type is always required; the name is optional.
- Raises: only for non-obvious or likely errors.
- References: numbered in citation order; avoid web pages as temporary sources.
- Examples: assume `import numpy as np` is already done, and every other import is explicit. Mark random or platform-dependent output with `#random`. Examples illustrate usage; they are not tests.
- Docstring lines: 75 characters.
- Class docstrings take the same sections minus Returns; constructor parameters go in the class docstring; Attributes after Parameters; Methods only when there are many methods.

**Docstring types versus annotations.** The format guide is silent. What I found:

| Approach | Source | Consequence |
|---|---|---|
| A. Types in the docstring and in the signature | NumPy and SciPy practice (the docstring is the documentation; annotations are newer) | Duplicates information, can drift. A checker is needed to keep them consistent, and I found none. |
| B. Annotations only; Parameters entries are names with descriptions | LSST/Documenteer convention (an organization's rule, not a numpydoc standard), implemented with sphinx-autodoc-typehints | Single source of truth. Returns still lists a type when the value needs description. Requires excluding numpydoc PR04, and the Sphinx extension. |
| C. numpydoc fills missing types from signature annotations | numpydoc PR 601 (resolves issue 196) | The PR page did not say if it merged or in which release. **[verify]** |

My suggestion: B, because the custodian's documentation standard asks for "documentation consistent with the code", and duplicated types cannot be kept consistent mechanically. This needs the custodian's confirmation (Q5). If A is chosen, add a project rule that docstring types use the numpydoc vocabulary (`array_like`, `int, optional`) and accept that the two can disagree.

Doc-standard interactions to flag for the custodian (the separate documentation standard requires American English, pedagogical prose, no agent notes or governance references in comments or docstrings):
- Ruff and numpydoc check structure, capitalization, and terminal period. Neither checks spelling variant, so American English needs a spell checker or prose linter. I did not research one (outside this brief). **[open]**
- The "no governance references" rule needs a custom grep-style check (for example `pygrep` hook or Ruff's `PGH`-style regex hook). Nothing standard does it.
- `ERA001` flags commented-out code but not agent notes.

## 7. Typing scientific code (D2)

- `numpy.typing` (NumPy 2.5 manual, 2026-06-28): `ArrayLike` (inputs that can become an array), `DTypeLike`, and `NDArray[ScalarT]` (an alias for `np.ndarray[tuple[Any, ...], np.dtype[ScalarT]]`). `NBitBase` is deprecated since 2.3; use `TypeVar` bounds or `@overload`. The NumPy mypy plugin is deprecated since 2.3; remove it from config.
- Shape typing: `np.ndarray` takes a shape tuple of `int` types, for example `tuple[int, int]` for two dimensions. `Literal` ints are not supported. NumPy 2.5 extends shape typing to many functions (`linspace`, `sum(keepdims=True)`, `linalg`), and says this is still in progress. A custom alias with the `type` statement works: `type Vector[S: np.generic] = np.ndarray[tuple[int], np.dtype[S]]`.
- Convention for public functions: take `ArrayLike` (or `NDArray[np.floating]` when a real array is required) and return `NDArray[...]`. For container arguments, accept wide types (`Sequence`, `Mapping`, `Iterable`) and return concrete ones (Scientific Python guide and typing.python.org best practices).
- jaxtyping: annotations like `Float[Array, "dim1 dim2"]`; works with NumPy, JAX, PyTorch, MLX, TensorFlow; no JAX dependency despite the name; requires Python 3.10+; runtime checks via beartype or typeguard. Static checkers see shapes as strings, so shape errors are found only at runtime.
- nptyping: I could not establish maintenance status or NumPy 2 support from the GitHub page. **[verify]** Not recommended as a dependency without that.
- JAX: `jax.Array` for outputs, `jax.typing.ArrayLike` for inputs; the module is documented as work in progress.
- PyTorch: I did not retrieve PyTorch typing docs. `torch.Tensor` is the annotation; jaxtyping adds shapes. **[not researched]**
- pint: `pint.Quantity[float]` and `pint.Quantity[np.ndarray[...]]` are accepted generics; annotations do not change runtime behavior; `ureg.wraps` with one return unit keeps the Quantity type, otherwise the return is `object`. Keep a single registry instance in one module. Units are not part of the static type, so unit mismatches are runtime errors only.
- Runtime checking: beartype (pure Python; O(1) per call on its own claim; `@beartype` and `beartype.claw` import hooks) and typeguard 4.x (`@typechecked`, import hook that can clash with other hooks). Use them at trust boundaries (file loaders, public API entry points) and in the test suite, not on hot numerical loops. Both are affected by the PEP 649 change if annotations are evaluated lazily; check before adoption.
- `Any`: typing.python.org best practices say use `object` when any value is accepted, and `Any` only when the type system cannot express the type. Ruff ANN401 bans `Any` in signatures; basedpyright `reportAny` / `reportExplicitAny` go further; mypy `--disallow-any-explicit` bans it in annotations.
- Stubs and distribution: add an empty `py.typed` file to typed packages (PEP 561). Prefer inline annotations over `.pyi` files (typing.python.org libraries guide); use `.pyi` for extension modules. Stub-only packages are named `<pkg>-stubs`. Fully annotate the public interface before adding `py.typed`. "Type complete" means every public symbol has fully known types.
- Generics: prefer PEP 695 syntax (`class Box[T]`, `def f[T](x: T) -> T`, `type X = ...`) on Python 3.12+; it infers variance. Do not mix old and new forms in one declaration.

## 8. Idioms for scientific Python (D1)

Each item has a source; items without one are the commonly held view and are marked as such.

- Floating-point comparison: `math.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)`; comparing to zero needs a positive `abs_tol`. `numpy.testing.assert_allclose` (default `rtol=1e-07`, `atol=0` from NumPy's reference, not from the page I fetched) is the NumPy-recommended assert; `assert_array_almost_equal` is listed under "not recommended". The Scientific Python pytest guide prefers `pytest.approx` over `numpy.testing`. Set `atol` explicitly near zero.
- Random numbers: `rng = np.random.default_rng(seed)`; no `np.random.seed`; no `RandomState` in new code (still supported). SPEC 7 (endorsed by IPython, NetworkX, NumPy, PySAL, scikit-image, SciPy) asks that functions take an `rng` keyword argument accepting `None`, int, sequence of ints, `SeedSequence`, `BitGenerator`, or `Generator`, and convert with `default_rng`. NumPy suggests large seeds, for example `secrets.randbits(128)`, and `SeedSequence.spawn` for parallel streams. Ruff NPY002 flags the legacy calls (confirmed **[local test]**). NumPy 2.5 notes say `Generator.binomial` and `multinomial` can give different samples for the same seed, so seed-based expected values in tests need a version note.
- Mutable defaults: use `None` and create the object inside (B006 flags it; its autofix is marked unsafe).
- Logging: libraries use `logging.getLogger(__name__)` and attach only a `NullHandler`; applications configure handlers. `print` is for ordinary command-line output only. Use `warnings.warn` for avoidable problems the caller should fix. Pass arguments to the logger rather than an f-string (Python logging HOWTO). Ruff `T20`, `LOG`, `G` cover part of this.
- Paths: `pathlib` (Ruff `PTH`). Always pass `encoding=` to `open()` or `Path.read_text`; 3.15 makes UTF-8 the default but older versions do not.
- Exceptions: derive from `Exception`, no bare `except:`, no `return`/`break`/`continue` in `finally` (PEP 8; PEP 765 warns on it in 3.14); use `with` for resources. Do not use `assert` for argument validation (Google guide).
- Vectorization: prefer array operations over Python loops. No mechanical check exists; it is a review item.
- Dataclasses, enums, f-strings, context managers: no source retrieved for this note beyond the PEP 8 and Google guide statements above. These are standard idioms; I did not research them further. **[not researched in depth]**
- Imports: PEP 8 grouping, enforced by Ruff `I`. Google's guide prefers importing modules, not symbols; PEP 8 allows both. The scientific convention `import numpy as np` is enforced by Ruff `ICN`.

## 9. D4: "formatted to be readable according to logical grouping of instructions"

What the sources support:
- PEP 8: blank lines inside functions, sparingly, to indicate logical sections (quote above). Two blank lines around top-level definitions, one between methods.
- Google style guide section 3.5: two blank lines between top-level definitions, one between methods, no blank line right after the `def` line, and blank lines inside functions are a matter of judgment.
- Black: keeps single blank lines inside functions; removes blank lines inside parenthesized expressions. **[local test]** (above) shows Ruff and Black collapse a run of several blank lines to one. A `def` followed by a blank line before its first statement was preserved by both tools in my test (Ruff 0.15 notes say this is now intentional).
- Magic trailing comma: a trailing comma in a bracket forces one item per line. Removing it lets the formatter collapse the bracket if it fits. This lets an author keep a parameter list or table of constants vertically grouped.
- Suppression: `# fmt: off` / `# fmt: on` work at statement level; `# fmt: skip` now applies to a whole logical line (Ruff 0.14.13 and later). Use for aligned numeric tables or matrices.
- NumPy, SciPy, and the Scientific Python guide point to PEP 8 and Ruff; SciPy sets 88 columns. None of them give extra rules for grouping code into "paragraphs". I did not find a recognized style guide that defines "paragraphs of code" beyond the PEP 8 sentence.

Mechanizable parts of D4:
- At most one blank line inside a function body, two at module level, and the function-start blank line rule: formatter.
- Import grouping: Ruff `I`.
- Line length and wrapping: formatter.
- Vertical alignment preserved when wanted: `# fmt: skip` and the magic trailing comma.

Not mechanizable:
- Whether each blank-line-delimited group is a coherent step (setup, compute, validate, return).
- Whether the formatter's output remains readable for a particular expression.
- Whether a comment at the head of a group explains why, and not what.
- A custodian rule such as "no blank line inside a group, at least one between groups" can only be reviewed. A lint rule that requires blank lines before `return` exists (flake8-return `RET` does not require it; pylint has no such rule that I confirmed). **[verify]** I did not find one.

Suggested standard wording: "Use a single blank line to separate logical steps within a function. Do not use more than one. Start a group with a short comment when the intent is not obvious from the code. Do not add blank lines inside a group."

## 10. Community standards

- Scientific Python Development Guide (learn.scientific-python.org/development): topical guides for packaging, style, testing, docs, typing, CI; principles (process, design, testing); patterns; and `sp-repo-review` checks, runnable in the browser or with `pipx run 'sp-repo-review[cli]'`. Its Ruff config (reproduced in section 5 in part) extends the default with ARG, B, C4, EM, EXE, FURB, G, ICN, ISC, LOG, NPY, PD, PERF, PGH, PL, PT, PTH, PYI, Q, RET, RSE, RUF, SIM, SLOT, T10, T20, TC, TRY, UP, and ignores PLR09 and PLR2004. Its mypy config: `strict = true`, `warn_unreachable = true`, `enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]`, plus `ignore_missing_imports` for numpy. Its pytest config: strict markers and config, `xfail_strict`, `filterwarnings = ["error"]`, `log_level = "INFO"`, `testpaths`. The guide does not set a line length.
- SPECs (scientific-python.org/specs): SPEC 0 minimum dependencies, SPEC 1 lazy loading, SPEC 4 nightly wheels, SPEC 6 keys to the castle, SPEC 7 seeding, SPEC 8 securing the release process are endorsed by core projects; SPEC 2, 3, 5, 9 are drafts. The "Endorsed" label is my inference from the listing of endorsing projects.
- pyOpenSci Python Package Guide: tutorials and guides for packaging, docs (Sphinx, Read the Docs), tests, and code style; uses Hatch in tutorials. The page I retrieved did not state docstring or type-hint conventions. **[verify]**
- NumPy documentation guide says use the numpydoc standard with the numpydoc Sphinx extension, and keep `versionadded` and `versionchanged` for at least five years.
- Google Python Style Guide: 80 columns, Google-format docstrings (not numpy), type annotation encouraged but not required everywhere. Use only as a source for idioms, since its docstring format conflicts with D3. The last 3,725 characters of this page were not read.

## 11. What cannot be mechanized

- Choosing precise types instead of `Any` or `object`, shape and dtype precision, and unit correctness.
- Docstring prose: clarity, American English, no agent notes, and consistency with the code's behavior (Ruff DOC and numpydoc only check structure and names).
- Whether `Raises` lists the errors a caller should expect (DOC501 and DOC502 only compare the docstring with `raise` statements in the body).
- Logical grouping of statements (D4), naming quality, vectorization, algorithm choice, and API design.
- PEP 20 principles.
- Numerical-correctness decisions: tolerances, seed policy in tests.
- Whether a type-ignore or lint suppression is justified (mechanizable only partly: `ignore-without-code`, `PGH003`, `RUF100` force a code and remove stale ones; a justification comment can be required but not judged).

## 12. Open questions for the custodian

- Q1. Minimum versions: Python 3.13 or 3.12 for new work, and NumPy 2.3 or 2.4? SPEC 0 says 3.12 and NumPy 2.2 go in 2026 Q4. Does the standard follow SPEC 0 literally, with a stated lag?
- Q2. Line length: 88 (Ruff and Black default, SciPy) or 79 or 99 (PEP 8 allowed range)? Comments and docstrings at 72 (PEP 8, W505) or 75 (numpydoc)? The suggestion is 88 and 72.
- Q3. Strictness on `Any`: ANN401 plus mypy strict only, or also `disallow_any_explicit` / basedpyright `reportAny`? What exception process is needed for NumPy and JAX boundary code?
- Q4. `from __future__ import annotations`: allowed, required, or forbidden while the floor is below 3.14? Do any dependencies (pydantic, beartype, typeguard) need runtime annotations?
- Q5. Docstring types: duplicate in docstring and signature (A), annotations only (B), or let numpydoc fill from annotations (C)? B needs numpydoc PR04 off and sphinx-autodoc-typehints. Also: is `Returns` required whenever a function returns a value (DOC201, RT01)?
- Q6. Are preview-only Ruff rules (DOC) acceptable in an enforced standard, given they may change between releases? The alternative is numpydoc validation in pre-commit and CI for the same checks.
- Q7. Do tests and scripts fall under "always use types" and the D rules? If tests are exempt from `D` but not from `ANN`, say so.
- Q8. Primary type checker: mypy or basedpyright? A second non-gating checker (Pyrefly) or none? When, if ever, does ty become eligible (a stable 1.0 release)?
- Q9. Free-threaded Python: required test target, optional, or out of scope?
- Q10. How are American English and "no agent notes or governance references" enforced? The documentation standard needs a check this note did not research.
- Q11. How exactly is "PEP standards" defined in the normative text: PEP 8, 257, and 20 plus the typing specification, with the version policy "current at the time of release"? Should the standard cite the typing spec at typing.python.org or the PEPs?
- Q12. Packaging: is `pyproject.toml` with `[project]`, `[dependency-groups]`, and SPDX `license` the required metadata form? Which build backend? Does the standard require a lock file (`pylock.toml`) or leave it to the project?

## 13. Sources (all accessed 2026-10-22)

PEPs and Python docs
- https://peps.python.org/pep-0008/, pep-0020, pep-0257, pep-0484, pep-0517, pep-0518, pep-0561, pep-0621, pep-0639, pep-0649, pep-0668, pep-0695, pep-0703, pep-0723, pep-0729, pep-0735, pep-0745, pep-0749, pep-0751, pep-0779, pep-0790
- https://peps.python.org/topic/typing/
- https://devguide.python.org/versions/
- https://docs.python.org/3.15/whatsnew/3.15.html
- https://docs.python.org/3.14/whatsnew/3.14.html
- https://docs.python.org/3/howto/free-threading-python.html
- https://docs.python.org/3/howto/logging.html
- https://docs.python.org/3/library/math.html#math.isclose
- https://typing.python.org/en/latest/spec/ and /spec/meta.html and /spec/distributing.html
- https://typing.python.org/en/latest/guides/libraries.html
- https://typing.python.org/en/latest/reference/best_practices.html

Scientific Python, NumPy, ecosystem
- https://scientific-python.org/specs/ , spec-0000/ , spec-0007/
- https://numpy.org/neps/nep-0029-deprecation_policy.html
- https://numpy.org/doc/stable/reference/typing.html
- https://numpy.org/doc/stable/release/2.5.0-notes.html and https://numpy.org/doc/stable/release.html
- https://numpy.org/doc/stable/reference/random/index.html
- https://numpy.org/doc/stable/reference/routines.testing.html
- https://numpy.org/devdocs/dev/howto-docs.html
- https://scipy.github.io/devdocs/dev/contributor/pep8.html
- https://learn.scientific-python.org/development/ , /guides/style/ , /guides/mypy/ , /guides/pytest/ , /guides/repo-review/ , /principles/
- https://www.pyopensci.org/python-package-guide/
- https://google.github.io/styleguide/pyguide.html
- https://docs.kidger.site/jaxtyping/
- https://github.com/ramonhagenaars/nptyping
- https://docs.jax.dev/en/latest/jax.typing.html
- https://pint.readthedocs.io/en/stable/advanced/typing.html
- https://beartype.readthedocs.io/en/latest/
- https://typeguard.readthedocs.io/en/latest/

Tools
- https://docs.astral.sh/ruff/ pages: /rules/ , /formatter/ , /formatter/black/ , /faq/ , /settings/ , and rule pages for line-too-long, doc-line-too-long, too-many-blank-lines, any-type, missing-type-function-argument, missing-return-type-undocumented-public-function, docstring-missing-returns, numpy-legacy-random, mutable-argument-default
- https://astral.sh/blog/ruff-v0.15.0 and https://astral.sh/blog/ruff-v0.16.0
- https://github.com/astral-sh/ruff/releases and https://github.com/astral-sh/ty/releases
- https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff_linter/src/rules/pydocstyle/settings.rs
- https://astral.sh/blog/ty
- https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html
- https://mypy.readthedocs.io/en/stable/command_line.html and /changelog.html
- https://github.com/microsoft/pyright/blob/main/docs/configuration.md and https://github.com/microsoft/pyright/releases
- https://docs.basedpyright.com/latest/configuration/config-files/
- https://github.com/facebook/pyrefly/releases/tag/1.0.0
- https://pydevtools.com/handbook/explanation/ty-vs-pyrefly/ (third-party, secondary)
- https://numpydoc.readthedocs.io/en/latest/format.html , /validation.html , /install.html
- https://raw.githubusercontent.com/numpy/numpydoc/main/numpydoc/validate.py
- https://pypi.org/project/numpydoc/
- https://github.com/numpy/numpydoc/pull/601
- https://github.com/tox-dev/sphinx-autodoc-typehints
- https://developer.lsst.io/v/DM-54027/stack/documenting-code-with-type-annotations.html (organization convention, secondary)
- https://pre-commit.com/
- https://docs.pytest.org/en/stable/how-to/doctest.html

## 14. Network log

The fetch tool returns a processed summary, so byte sizes of the raw pages were not available. "Size" is given only where the tool reported it. All requests were HTTPS GET through the pre-configured proxy; no credentials or secrets were sent. Total: about 100 page fetches (1 failed, 5 clearly partial) and 4 web searches, plus local experiments. The row numbering below groups some fetches, so row counts do not equal fetch counts. This is far below the 10,000-item and 10,000 MB limits.

| # | URL (abbreviated; full list in section 13) | Result | Size |
|---|---|---|---|
| 1 to 22 | peps.python.org: 745, 790, 8, 20, 257, 484, 649, 749, 621, 723, 668, 779, 735, 751, 639, 703, 518, 517, 695, 561, 729, and topic/typing | success | n/r |
| 23 | devguide.python.org/versions/ | success | n/r |
| 24 | scientific-python.org/specs/spec-0000/ | success | n/r |
| 25 | scientific-python.org/specs/ | success | n/r |
| 26 | scientific-python.org/specs/spec-0007/ | success | n/r |
| 27 to 29 | typing.python.org: spec/, spec/meta.html, spec/distributing.html | success; spec/meta did not state normative status | n/r |
| 30 | typing.python.org/en/latest/guides/libraries.html | success | n/r |
| 31 | typing.python.org/en/latest/reference/best_practices.html | success | n/r |
| 32 | docs.python.org/3.15/whatsnew/3.15.html | partial: excerpt cut before the typing and deprecations sections | n/r |
| 33 | docs.python.org/3.14/whatsnew/3.14.html | success | n/r |
| 34 | docs.python.org/3/howto/free-threading-python.html | success | n/r |
| 35 | docs.python.org/3/howto/logging.html | success | n/r |
| 36 | docs.python.org/3/library/math.html#math.isclose | success | n/r |
| 37 | docs.astral.sh/ruff/rules/ | partial: few prefixes listed | n/r |
| 38 | docs.astral.sh/ruff/formatter/ | success | n/r |
| 39 | docs.astral.sh/ruff/formatter/black/ | success | n/r |
| 40 | docs.astral.sh/ruff/formatter/#philosophy | success | n/r |
| 41 | docs.astral.sh/ruff/faq/ | success | n/r |
| 42 | docs.astral.sh/ruff/settings/ | partial: pydocstyle section not in excerpt | n/r |
| 43 | docs.astral.sh/ruff/settings/#lint_pydocstyle_convention | partial: section not returned | n/r |
| 44 to 53 | docs.astral.sh/ruff/rules/ pages: docstring-missing-returns, any-type, line-too-long, missing-type-function-argument, too-many-blank-lines, numpy-legacy-random, doc-line-too-long, mutable-argument-default, missing-return-type-undocumented-public-function (9 pages) plus raw.githubusercontent.com ruff pydocstyle settings.rs | success | n/r |
| 54 | astral.sh/blog/ruff-v0.15.0 | success | n/r |
| 55 | astral.sh/blog/ruff-v0.16.0 | success | n/r |
| 56 | astral.sh/blog/ty | success | n/r |
| 57 | github.com/astral-sh/ruff/releases | success | n/r |
| 58 | github.com/astral-sh/ty/releases | success; no stable/beta statement on the page | n/r |
| 59 | github.com/facebook/pyrefly/releases/tag/1.0.0 | success | n/r |
| 60 | pydevtools.com/handbook/explanation/ty-vs-pyrefly/ | success (third-party) | n/r |
| 61 | mypy.readthedocs.io/en/stable/command_line.html | success | n/r |
| 62 | mypy.readthedocs.io/en/stable/changelog.html | success; no release dates on page | n/r |
| 63 | github.com/microsoft/pyright/blob/main/docs/configuration.md | success | n/r |
| 64 | github.com/microsoft/pyright/releases | success; year inferred | n/r |
| 65 | docs.basedpyright.com/latest/configuration/config-files/ | success; latest version not stated | n/r |
| 66 to 68 | numpydoc.readthedocs.io: format.html, validation.html, install.html | success | n/r |
| 69 | numpydoc.readthedocs.io/en/latest/release_notes.html | **failed** (client error) | 0 |
| 70 | raw.githubusercontent.com/numpy/numpydoc/main/numpydoc/validate.py | success | n/r |
| 71 | pypi.org/project/numpydoc/ | success | n/r |
| 72 | github.com/numpy/numpydoc/pull/601 | success; merge status unclear | n/r |
| 73 | github.com/tox-dev/sphinx-autodoc-typehints | success | n/r |
| 74 | developer.lsst.io/v/DM-54027/stack/documenting-code-with-type-annotations.html | success | n/r |
| 75 | numpy.org/doc/stable/reference/typing.html | success | n/r |
| 76 | numpy.org/doc/stable/release/2.5.0-notes.html | success; release date not stated | n/r |
| 77 | numpy.org/doc/stable/release.html | success; no dates | n/r |
| 78 | numpy.org/neps/nep-0029-deprecation_policy.html | success | n/r |
| 79 | numpy.org/doc/stable/reference/random/index.html | success | n/r |
| 80 | numpy.org/doc/stable/reference/routines.testing.html | success | n/r |
| 81 | numpy.org/devdocs/dev/howto-docs.html | success | n/r |
| 82 | scipy.github.io/devdocs/dev/contributor/pep8.html | success | n/r |
| 83 to 89 | learn.scientific-python.org/development/ plus /guides/style/, /guides/mypy/, /guides/pytest/, /guides/repo-review/, /principles/ | success (6 pages) | n/r |
| 90 | pyopensci.org/python-package-guide/ | success | n/r |
| 91 | google.github.io/styleguide/pyguide.html | partial: page about 103,725 characters; last 3,725 not read | about 104 KB of text |
| 92 | black.readthedocs.io/.../current_style.html | success | n/r |
| 93 | docs.kidger.site/jaxtyping/ | success | n/r |
| 94 | github.com/ramonhagenaars/nptyping | success; status not determinable | n/r |
| 95 | docs.jax.dev/en/latest/jax.typing.html | success | n/r |
| 96 | pint.readthedocs.io/en/stable/advanced/performance.html | success; no typing content | n/r |
| 97 | pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html | success; no typing content | n/r |
| 98 | pint.readthedocs.io/en/stable/advanced/typing.html | success | n/r |
| 99 | beartype.readthedocs.io/en/latest/ | success | n/r |
| 100 | typeguard.readthedocs.io/en/latest/ | success | n/r |
| 101 | pre-commit.com/ | success | n/r |
| 102 | docs.pytest.org/en/stable/how-to/doctest.html | success | n/r |
| S1 to S4 | Web searches: Ruff 2026 releases; ty beta/stable; Pyrefly stable; numpydoc type annotations | success; used only to find URLs | n/r |
| L | Local experiments (ruff 0.16.8, black 26.5.1) in the scratchpad | success | negligible |

n/r = not reported by the tool.
