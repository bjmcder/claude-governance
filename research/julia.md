# Research note: Julia language standard (LVL2) inputs

Author: research agent (STND.CREW), delegation depth 1.
Date accessed (all sources): 2026-10-22.
Scope: read-only retrieval to inform a custodian adopting a Julia standard. Nothing in the project was changed except this note.

Custodian direction (verbatim): "for Julia, refer to https://docs.julialang.org/en/v1/. use the latest version available".

## How to read this note

- Evidence labels: **[S]** = stated on a page I fetched (URL in the Sources section). **[K]** = my own background knowledge, not verified in this session. Treat [K] items as leads to verify before they become rules.
- Page contents reached me through the fetch tool's summarizer, not as raw text. I did not read any page verbatim. Where two pages disagreed, I say so. Quotes shown are as the tool returned them.
- Four fetches failed: the manual's Profiling page (three attempts, client error), Blue Style's GitHub Pages site, and the TestItems.jl repository page. Gaps from these are listed under Open questions and in the network log.

---

## 1. Which Julia: release status as of 2026-10-22

### Findings

| Item | Value | Source |
|---|---|---|
| Latest stable | **1.13.2** (patch released 14 Oct 2026 per downloads page and endoflife.date; Discourse announcement says 15 Oct) | [S] julialang.org/downloads; endoflife.date; Discourse |
| 1.13.0 release date | 10 Sep 2026 | [S] 1.13 highlights blog |
| LTS | **1.10.12** (released 15 Aug 2026) | [S] downloads; endoflife.date |
| 1.12 | Security support **ended 10 Sep 2026** (when 1.13 shipped) | [S] endoflife.date |
| 1.11 | Support ended 8 Oct 2025 | [S] endoflife.date |
| Manual at `/en/v1/` | Documents **Julia 1.13** (footer: "Using Julia version 1.13.2", built with Documenter 1.19.0) | [S] docs.julialang.org/en/v1/ |
| Upcoming release | None announced on the downloads page | [S] |
| Support pattern | Julia usually stops patching minor 1.x once 1.(x+1) ships; the one cited exception is 1.11.8 after 1.12.2. No formal LTS policy or future LTS plan was stated in the thread I read. | [S] Discourse "Minor versions publications scheme" |

So the URL the custodian named (`/en/v1/`) and "latest version available" currently agree: both mean 1.13.x. The `/en/v1/` URL is a moving alias; it will point to 1.14 when that ships.

### Changes relevant to style and correctness, by version

Julia 1.11 (Oct 2024) [S: 1.11 highlights, HISTORY.md]
- `public` keyword: marks names as API without exporting them. `Base.ispublic` queries it. Needs 1.11+; older versions need Compat.jl or a version guard.
- `Memory` type underlies `Array`; `push!` roughly 2x faster.
- `ScopedValue`: runtime-supported alternative to mutable globals for configuration.
- `[sources]` in Project.toml for unregistered dependencies. Pkg enforces `julia` compat and adds compat entries on `pkg> add`.
- `@main` opt-in entry point. Version-specific manifests (`Manifest-v1.11.toml`; the code-loading page says from 1.10.8).
- `Threads.@threads :greedy` scheduler; `Base.Lockable`.
- Random: negative integer seeds, seeding from strings, `rand` over Tuple and Pair types.
- Coverage and malloc tracking no longer generated during precompilation.
- Standard libraries moved out of the system image and have their own versions.

Julia 1.12 (Oct 2025) [S: 1.12 highlights, HISTORY.md, Pkg docs]
- Default threads: one default worker plus one interactive thread. Thread counts respect CPU affinity (containers, schedulers).
- Bindings take part in world age; constants and structs can be redefined. Marking a name both `public` and `export` is now an error.
- `--trim` (experimental) with JuliaC: removes code not provably reachable from entry points; dynamic dispatch reachable from entry points fails the build.
- `OncePerProcess`, `OncePerThread`, `OncePerTask`.
- `@testset ... rng=` option; a failing testset prints its RNG so the failure can be replayed.
- Pkg workspaces (several projects share one manifest) and Pkg apps (experimental; `[apps]` table, `@main`, shims in `~/.julia/bin`).
- `@atomic` on indexed references; wall-time profiler (`Profile.@profile_walltime`).
- `setprecision` with a function argument became thread safe.
- Macro expansion of `:toplevel` blocks delayed; `FieldError` added.

Julia 1.13 (Sep 2026) [S: NEWS, 1.13 highlights]
- About 30% faster package precompilation than 1.12 (10-20% faster than 1.10), about 20% faster startup, much cheaper full GC.
- New public `@__FUNCTION__`; introspection macros (`@code_warntype`, `@which`, ...) accept `::T` syntax, keyword arguments, and broadcast expressions.
- **Behavior change:** byte hashing is now RapidhashNano; default seed changed, so `hash` values differ from 1.12. Custom `hash` methods should accept the seed and not give it a default. Code or test data that stores hash values breaks.
- **Behavior change:** `Pkg.test` no longer forces `--check-bounds=yes`. Restore with `julia_args=["--check-bounds=yes"]`.
- **Behavior change:** `@doc` returns the documented object instead of a `Docs.Binding`.
- `merge(combine, d::AbstractDict...)` deprecated in favor of `mergewith`.
- Scheduler: `@spawn` wakes one idle thread; interrupt handling fixed; task cancellation planned for 1.14.
- Apple Silicon: `Sys.CPU_THREADS` counts all cores now, which changes default thread counts.
- Test: testset state now in a `ScopedValue`; evaluated arguments shown on `@test` failure; three-argument `@test_throws` (the Test page says 1.12+ in one place and 1.13+ in another; NEWS lists it under 1.13).
- Pkg: manifest format 2.1 (needs 1.13) records registries; `pkg> add` prefers already-loaded versions; zstd downloads. Docs now recommend workspaces over `[extras]`/`[targets]` for test dependencies.
- `--trace-eval`, `PaddedSpinLock`, `Base.@acquire`, `Iterators.findeach`, `nth`.
- Juliaup 1.22+ has a GUI.
- The blog post did not discuss package extensions, binding semantics, or a breaking-changes section. Community reports after release mention VS Code LanguageServer crashes on 1.13, some packages blocking upgrade, and a few compile-latency or benchmark regressions versus 1.10/1.11 [S: Discourse thread].

Package extensions (1.9+), `[weakdeps]`, `[extensions]`: stable, documented, and the manual's Performance Tips recommend them to cut load time [S].

### Expressing "latest version available"

Julia has no way to write "latest" in `Project.toml`; compat is a range, and its lower bound is a floor, not a target. The standard should separate three things:

1. **Floor (compat):** `[compat] julia = "1.13"` means `[1.13.0, 2.0.0)` (caret default) [S: Pkg compat docs]. The General registry requires an upper-bounded `julia` entry; `"1.13"` satisfies this [S: RegistryCI].
2. **Toolchain (what developers and CI run):**
   - Juliaup channel `release` always points at the latest stable; `1.13` tracks patches of that minor; `lts` is 1.10 [S: juliaup README]. Juliaup can pick a channel from the manifest's `julia_version` if `manifestversiondetect` is enabled; it is off by default [S].
   - GitHub Actions `julia-actions/setup-julia@v3`: `version: '1'` is latest v1 release, `'lts'`, `'pre'`, `'nightly'`, and `'min'` (earliest version allowed by compat) [S].
3. **Reproducibility record:** commit `Manifest.toml` (or `Manifest-v1.13.toml`) for applications and analysis codes; its `julia_version` and `project_hash` fields record what ran [S]. Libraries normally do not commit manifests [K].

Suggested wording for the standard (for the custodian to decide): "The reference version is the latest stable Julia minor release at the time a project starts, recorded in the project constitution. Projects move to a new minor release within N months of its release, or record a waiver. Patch releases are taken automatically."

Trade-off the custodian should see: a floor of 1.13 gives access to everything above and matches the manual, but excludes the LTS (1.10) and 1.12, which is now out of security support. Several quality tools were not yet confirmed on 1.13 (see section 4). A floor at the LTS with CI on `1`, `lts`, `pre` is common practice for libraries [S: SciML guide says test LTS and current stable] but conflicts with a strict reading of "latest".

---

## 2. The manual (docs.julialang.org/en/v1/): rules to adopt

Each rule below has an ID for the custodian to cite or drop. "M" = from the manual.

### 2.1 Style Guide chapter [S]

- M-S1. Indent 4 spaces.
- M-S2. Write functions, not scripts; functions take inputs as arguments rather than reading or changing globals (except constants).
- M-S3. Write docstrings for user-facing objects; use `#` comments only for readers of the code.
- M-S4. Avoid overly specific types (`complex(float(x))`, not `Complex{Float64}(x)`). Use abstract types in arguments, or omit them; add types mainly to resolve ambiguity. Handle argument diversity in the caller by converting.
- M-S5. Avoid strange `Union` types and elaborate container types; avoid unnecessary static parameters.
- M-S6. A constructor for `T` must return a `T`.
- M-S7. Choose instances over types as the concept (`MyType()`); model enumerations as one type with instance values.
- M-S8. Prefer exported methods over direct field access; fields are implementation details.
- M-S9. Argument order: function, IO, mutated input, type, non-mutated input, key, value, other, varargs, keywords.
- M-S10. Do not expose unsafe operations on the normal interface; mark them "unsafe" in the name.
- M-S11. Do not overload base container methods for standard types; **avoid type piracy** (extending Base or other packages' functions on types you do not own). Alternatives: new function name, or a wrapper type of your own.
- M-S12. `!` on functions that mutate arguments (IO and RNG functions are exceptions because they always mutate stream or generator state).
- M-S13. Naming: modules and types CamelCase; constants uppercase with underscores; leading `_` for internal names; functions snake_case (Base sometimes joins words, packages should not); no abbreviations.
- M-S14. Do not overuse try/catch, splatting, macros, or trivial anonymous wrappers; do not parenthesize conditions; use `isa` and `<:` for type tests, not `==` (except against concrete types).
- M-S15. Avoid float literals in generic code (`2.0*x` promotes a `Rational`); use integer literals or `Rational{Int}`.

### 2.2 Performance Tips chapter [S]

- M-P1. Performance-critical code lives in functions. Avoid untyped globals; declare globals `const` or annotate their type.
- M-P2. Measure with `@time` after warm-up, treat unexpected allocation as a defect; use BenchmarkTools.jl for real benchmarks (interpolate with `$`) [S: BenchmarkTools README].
- M-P3. Concrete element types in containers; parametric types, not abstract-typed struct fields; parameterize container fields (`A<:AbstractVector`).
- M-P4. Type stability: return one type for all inputs (`zero(x)`, `oneunit`, `oftype`); do not change a local variable's type.
- M-P5. Function barriers: put the hot loop in its own function.
- M-P6. Closures that capture a variable reassigned elsewhere get boxed; use a `let` block, annotate, or restructure. `@__FUNCTION__` (1.13) can replace self-referencing closures.
- M-P7. `Val` only when the value is known at compile time or behind a barrier; do not encode many distinct values as type parameters.
- M-P8. Pre-allocate outputs and use in-place `.=`; use `view`/`@views`; fuse broadcasts with `@.`; iterate in column-major order; use `eachindex` rather than `1:n`.
- M-P9. `@inbounds` only when indices are certainly valid. `@fastmath` can change results and assumes no NaN or Inf. `@simd` is experimental and wrong if iterations are not independent.
- M-P10. Set `OPENBLAS_NUM_THREADS=1` (or `BLAS.set_num_threads`) when running multithreaded Julia to avoid oversubscription.
- M-P11. Fix deprecation warnings (they cost lookup time).
- M-P12. Named tools: `Profile`, ProfileView.jl, JET.jl, `@allocated`, `--track-allocation=user`, `@code_warntype`, SnoopCompile, PrecompileTools.jl; minimize dependencies and avoid heavy `__init__`.

### 2.3 Documentation chapter (docstring conventions) [S]

- M-D1. A docstring is the string immediately before the object; no blank line or comment between. Markdown by default. Opening and closing `"""` on their own lines. Use `raw"""` when the text contains `$` or `\`.
- M-D2. Four-space-indented signature first (`f(x, y=1)`, optional without default as `f(x[, y])`, `f(x; <keyword arguments>)`).
- M-D3. One imperative-mood summary line ending with a period; do not begin "The function `bar`..."; do not restate argument types already in the signature.
- M-D4. `# Arguments` list (bulleted) only for complex functions; `See also` paragraph with `[`name`](@ref)` links; `# Examples` with `jldoctest`; `# Implementation` for developer-facing notes; `# Extended help` for long material.
- M-D5. Doctest examples are self-contained, avoid `rand` or seed an explicit RNG, and truncate stack traces with `[...]`. Plain `julia` blocks for untestable examples.
- M-D6. Wrap identifiers in backticks; equations in double backticks using Unicode; keep lines to about 92 characters.
- M-D7. Document the most generic method (or `function bar end`), not every method; document specific methods only when behavior differs. Do not document a `const` alias; document the real function.
- M-D8. Module docstring goes above `module M`.
- M-D9. `Docs.hasdoc(module, name)` and `Docs.undocumented_names(module; all)` exist to check coverage. Since 1.11, `@doc` retrieval needs the REPL stdlib loaded.

### 2.4 Modules and Code Loading [S]

- M-M1. `export` only affects `using`. `public` (1.11+) marks API without namespace effect; it is top-level only. Marking a name both `public` and `export` is an error in 1.12+.
- M-M2. Only `import M: f` or qualified names (`M.f(::T) = ...`) add methods to another module's function.
- M-M3. Use relative paths (`.Sub`, `..Sub`) for submodules. A module may span many files via `include`; `include` evaluates in the including module's global scope.
- M-M4. `__init__()` runs at load time, not precompile time; use it only for runtime state (C pointers, `Dict` rehashing). Avoid global state that assumes one load, and do not copy `stdout` into a constant at compile time.
- M-M5. Project files: `name`, `uuid`, `[deps]`, `[compat]`, `[weakdeps]`, `[extensions]` (1.9+), `[workspace]`, entry point `src/X.jl`. Package identity is the UUID, not the name.
- M-M6. Workflow-tip chapter: wrap scratch code in a module so structs can be redefined without restart; use Revise.jl; a package (via PkgTemplates) for anything long-lived [S].

### 2.5 Types and Methods [S]

- M-T1. Default to immutable `struct`; use `mutable struct` only when instances must change independently, and mark never-changing fields `const` (1.8+).
- M-T2. Type parameters are invariant; use `Point{<:Real}` in signatures.
- M-T3. Use `Union{T, Nothing}` for optional values; small unions are handled well (about 4 types by default).
- M-T4. Avoid defining new primitive types; wrap a built-in instead.
- M-T5. Dispatch is on positional arguments only; keyword arguments do not take part (known bug #9498 with keyword vs non-keyword methods).
- M-T6. Resolve ambiguities by defining the intersection method; define it first. `Vararg{T,N}` fixes a count, `T...` does not.
- M-T7. World age: methods defined during execution are invisible to already-running code.
- M-T8. Idioms: traits ("Holy traits") via singleton-returning functions; `eltype(::Type{<:AbstractArray{T}}) where {T}`; `promote_op` for output element type; `function f end` to declare an empty generic function; callable structs.

### 2.6 Multi-threading and Distributed [S]

- M-X1. The programmer is responsible for being data-race free. Guard shared mutable data with one lock per datum (`@lock`, `Base.Lockable`); always unlock in `finally` if manual.
- M-X2. **Do not index buffers by `threadid()`**; tasks migrate between threads. Allocate per task.
- M-X3. `@threads` has no reduction; chunk the work, `@spawn` one task per chunk, `fetch` and combine. `@spawn` scheduling is nondeterministic.
- M-X4. Base collections (`push!`, `Dict` insert) need locking under concurrent modification; use `Threads.Atomic` or `@atomic` for shared scalars.
- M-X5. Finalizers can interrupt any code; keep them away from shared state or protect it.
- M-X6. Do not define types, methods, or modules, or `include` or `eval`, in parallel.
- M-X7. Distributed: code must be loaded on every worker (`@everywhere`); workers do not run `startup.jl`; use the same Julia version on all workers; pass arguments rather than relying on globals; `@distributed` loops cannot write to plain arrays; the cluster cookie and plain TCP mean traffic is not encrypted by default.
- M-X8. The Multi-Threading page does not cover thread-safe RNG or false sharing (see section 5 for RNG).

### 2.7 Profiling

The manual page `manual/profiling/` could not be fetched. From the `Profile` stdlib page [S]: `@profile f()` then `Profile.print()` (`format=:tree` default or `:flat`; `C=true` shows C frames; `mincount`); `Profile.clear()`; `Profile.Allocs.@profile sample_rate=...` for allocations; for `--track-allocation`, run once then `clear_malloc_data`. Warm-up before profiling follows from M-P2 [K for exact wording]. The wall-time profiler is a 1.12 addition [S: 1.12 blog].

---

## 3. Community style guides and formatters

### Comparison

| Topic | Julia manual | Blue Style | SciML Style | YASGuide |
|---|---|---|---|---|
| Status | Official | Maintained by Invenia, used widely [K on usage] | Maintained by SciML org; includes policy beyond formatting | "Work in progress" per README; commit dates not visible; 27 commits |
| Indent / line | 4 spaces; ~92 chars for docstrings | 4 spaces; 92 chars | 4 spaces; 92 chars; LF endings | 4 spaces; soft 80 chars |
| Function names | snake_case for packages; Base joins words | lowercase with underscores, one or two words | snake_case | snake_case |
| Types / modules | CamelCase | UpperCamelCase | CamelCase; `Abstract` prefix | CamelCase; `Abstract` prefix |
| Constants | upper with underscores | ALL_CAPS | SNAKE_CASE | SNAKE_CASE |
| Internal names | leading `_` | leading `_` | double underscore prefix | not stated in the fetch |
| `return` | not required | explicit `return` required in long-form functions | not stated | omit only in short-form |
| `using` vs `import` | not prescribed | prefer `using`, explicit lists, one package per line, sorted | prefer explicit imports | prefer `using` |
| `for` loops | not prescribed | `in`, never `=` or `∈` | `in` | `in` |
| Float literals | avoid in generic code | leading/trailing zero (`0.1`, `2.0`) | same | no trailing decimal (`1.0`) |
| Multi-line calls | not prescribed | brackets at same indent, args one level deeper | same | align to bracket (assumed, not stated in fetch) |
| Docs | docstring conventions in section 2.3 | markdown; Arguments, Keywords, Returns, Throws sections; required for exports | document at highest level; Documenter; tutorial required | not stated |
| Extras | none | none | type stability, mutation, error, safety, test (`@safetestset`), version and compat rules | `where` braces, `@assert` not for required checks |
| Formatter | none | JuliaFormatter `style="blue"` | JuliaFormatter `style="sciml"` (v1.x recommended, see below) | JuliaFormatter `style="yas"` |

Notes:
- Blue states it wins over the manual where they conflict, listing: underscored names, multi-line indentation, `using` over `import`, explicit `return`, `in` in loops [S].
- The manual does not prescribe underscores, `return`, or import style; so manual-only compliance leaves these free, which makes formatter output the effective authority.
- Naming conventions (functions lowercase, types CamelCase, `!` for mutators) are consistent across all four guides, so adopting them carries no conflict [S].
- SciML's guidance on closures ("avoid closures") and "default to out-of-place" is stricter than the manual and is a design opinion, not a correctness rule. I would not adopt it as a mandatory rule [K].

### Formatters

**JuliaFormatter.jl** [S]
- Width-sensitive formatter; styles Default, Blue, SciML, YAS (and Minimal in later releases). Config file `.JuliaFormatter.toml`, searched upward from the file. `format_text` defaults: `indent=4`, `margin=92`, `style=DefaultStyle()`.
- README says the Default and Blue styles should be largely stable from v2.10 on, and that SciML and YAS "still have a number of rough edges" in v2, recommending v1 for those two.
- CLI `jlfmt --check -v src/` exists (since v2.2.0) for CI.
- Latest release shown on GitHub releases page: v2.14.0 (6 Sep; year not shown). v2.13.0 changed Minimal style output, so minor releases can change formatting; pin the version.
- Option defaults beyond indent and margin were not retrievable (docs pages did not list them).

**Runic.jl** [S]
- Built on JuliaSyntax.jl; no configuration at all (gofmt-like). Rules include 4-space indent, spaces around operators, explicit `return` on the last expression of functions (with exceptions), trailing commas in multiline literals, `in` in `for` loops, float-literal normalization, and no trailing whitespace.
- No line-width limit by design. Optional `--docstrings` formats Julia code inside docstrings and also handles `.md` and `.qmd`.
- CLI `runic --check --diff`, pre-commit hook, GitHub Action `fredrikekre/runic-action@v1`. Installable as a Pkg app on Julia 1.12+.
- Its semver policy: patch releases do not change output; minor releases may fix specification bugs that change output; major releases may change formatting. Releases page lists v1.13.0, v1.12.0, v1.11.1 with day and month only; I could not confirm the year or tie them to 2026 [unverified].
- Honors JuliaFormatter's `#! format: off` markers.

**Comparison for a standard**
- Runic: one style, no settings to argue over, deterministic, simple to state as a rule ("code is Runic-formatted"). Cannot enforce a line limit or wrap docstrings.
- JuliaFormatter: configurable; can enforce margin 92, format docstrings, and match Blue or SciML exactly. Cost: config surface, style version drift, and Blue/SciML options that reformat in ways other tools may not agree with.
- The two do not produce identical output; do not run both on the same tree [K].
- Neither checks naming. No command-line linter that checks naming conventions was found; the August 2026 Discourse thread names StaticLint.jl (VS Code only, CLI use unconfirmed), JET (not a style linter), Aqua, ReLint.jl, and Fatou (early-stage) [S]. So naming rules are review-enforced.

---

## 4. Mechanical checking

### Tool notes

| Tool | What it checks | Notes from sources |
|---|---|---|
| **Test stdlib** | Unit tests; `@inferred` (return type equals inferred type); `Test.detect_ambiguities`; `Test.detect_unbound_args`; `@test_throws`; `@test_logs`; testset `rng=` (1.12+); coverage via `--code-coverage` | [S] `Pkg.test` stops forcing `--check-bounds=yes` in 1.13 |
| **Aqua.jl** | Method ambiguities, unbound type parameters, undefined exports, Project extras consistency, stale deps, missing/incorrect compat, obvious type piracy, persistent tasks | [S] `Aqua.test_all(Pkg)`; add as a test dependency only; pin `Aqua = "0.8"`-style compat. Piracy check detects "obvious" cases only. Julia 1.13 support not stated on the pages I read. |
| **JET.jl** | `@report_call`/`@test_call`: possible `MethodError`, undefined names, missing fields, compile-time bounds errors. `@report_opt`/`@test_opt`: runtime dispatch, captured variables. `report_package`/`test_package`: analyze all signatures (noisy). | [S] v0.12 series supports 1.12 and 1.13; Julia 1.11 needs v0.9 series; unsupported Julia gets stubs that throw; `JET_AVAILABLE` flag. Support on 1.10 (LTS) not stated; check before using an LTS floor. Cannot see through dynamic dispatch; "no errors" is not proof. |
| **ExplicitImports.jl** | No implicit imports (`using X` bare), no stale explicit imports, imports/qualified accesses only from the owning module, and only of public names | [S] `test_explicit_imports`, per-check `check_*`/`test_*` functions. Non-public checks pair with the `public` keyword. |
| **Documenter.jl** | `doctest=true` default; `checkdocs` (`:all` default, `:exports`, `:public`, `:none`); `modules=[...]` needed for missing-docstring warnings; `warnonly=false` default; `linkcheck` off by default; `doctest(MyPkg)` callable from tests; `doctest=:fix` or `fix=true` | [S] Doctests in docstrings only run if the module is in `makedocs(modules=...)` and `DocMeta.setdocmeta!` is set. Docs site for Documenter itself ran Documenter 1.19.0 on Julia 1.12.7. |
| **TestItems / ReTestItems / TestItemRunner** | `@testitem` blocks, tags, per-item module isolation, parallel workers | [S] ReTestItems uses distributed processes; items cannot nest. Optional; SciML uses `@safetestset` instead. TestItems.jl page itself could not be fetched. |
| **Coverage** | `pkg> test --coverage`; `.cov` files; julia-runtest `coverage: true` default; 1.13 `--code-coverage=all` discards sysimage caches | [S] No coverage-threshold tool was researched (Codecov/Coveralls and `julia-processcoverage` are [K]). |
| **AllocCheck.jl** | `@check_allocs` statically proves a call cannot allocate (LLVM IR); `ignore_throw=true` default | [S] Wrap only entry points; every call into a checked function behaves like dynamic dispatch; Julia version range not stated; README example output from 1.10.0-rc1. Fit: real-time or inner kernels only. |
| **DispatchDoctor.jl** | `@stable` errors (or warns) on non-concrete inferred return types; mode via Preferences (`dispatch_doctor_mode`) | [S] README says checks are "currently only [1.10.0, 1.13.0) are active." So on 1.13 the checks may be inert; verify before relying on it. Skipped during precompilation, in closures, `@generated`, parameterized constructors, and under Revise. Increases precompile time. |
| **Cthulhu.jl** | Interactive `@descend` for inference problems | [S] Not a CI tool. `@descend foo(::Int)` syntax needs 1.13. |
| **SnoopCompile** | Compile/inference latency, invalidations | [S] Latency tool, not correctness. Aqua's persistent-tasks check and `@time_imports` cover the load-time side. |
| **`@code_warntype`** | Manual inspection of inferred types | [S] Accepts `::T` and kwargs in 1.13. |
| **BenchmarkTools.jl** | Benchmarks | [S] Not a correctness gate; regression tracking needs separate infrastructure. |

### Recommended enforced configuration (proposal, for the custodian to accept or edit)

Gates that fail CI (hard):
1. **Format:** one formatter, pinned. Proposed: Runic (`runic --check --diff .`), because it has no options to disagree about and mirrors the Python plan of "tool-enforced style." Alternative: JuliaFormatter `style="blue"`, `margin=92`, `format_docstrings=true`, version pinned, `jlfmt --check`. (Whether `format_docstrings` exists and works as I describe is [K]; confirm.)
2. **Tests:** `Pkg.test` on `lts` (if the floor allows it), `1`, and `min`; `pre` as informational. Run with `check_bounds: yes` explicitly (julia-runtest default is `yes`, but `Pkg.test` itself no longer sets it in 1.13), `depwarn: error` so deprecations fail [S: action.yml defaults `check_bounds=yes`, `depwarn=yes`, `coverage=true`].
3. **Aqua:** `Aqua.test_all(MyPkg)` with no exclusions by default; each exclusion must be listed with a reason in the project waiver record.
4. **ExplicitImports:** `test_explicit_imports(MyPkg)`; require explicit imports, no stale imports, owner-only and public-only access.
5. **JET:** `test_package(MyPkg; target_modules=(MyPkg,))` or `@test_call` on representative entry points; `@test_opt` on numerical kernels declared type-stable. Pin JET to the series matching the Julia version in CI.
6. **Docs:** `makedocs(; modules=[MyPkg], checkdocs=:public` (or `:exports`)`, doctest=true, warnonly=false)`; `linkcheck=true` in a scheduled job, not on every push. Doctests also run via `doctest(MyPkg)` in the test suite.
7. **Compat:** every dependency, weak dependency, and `julia` has an upper-bounded `[compat]` entry (Aqua checks presence; RegistryCI rules show the bounded form [S]).
8. **Doctest RNG:** doctests that use randomness construct an explicit seeded RNG (M-D5). Mechanical backstop: a small grep for bare `rand(`/`randn(` without an RNG argument inside `jldoctest` blocks [K, custom script].

Soft gates (reported, not failing, until a project opts in): coverage percentage (threshold set per project); AllocCheck on declared allocation-free kernels; DispatchDoctor `@stable` in test mode only (and only after confirming 1.13 behavior); SnoopCompile and `@time_imports` for load time.

Matrix suggestion for CI: Julia `1`, `lts` (if floor permits), `min`, `pre`; OS ubuntu, macOS, windows if portability is claimed; one job with `JULIA_NUM_THREADS=4` (or `auto`) and one with `1` to expose threading assumptions [K for thread matrix].

### What cannot be mechanized (review-enforced)

- Naming quality (descriptive vs abbreviated; `!` correctness: a function that mutates must have `!` and a function with `!` should mutate). No tool found.
- Docstring prose: American English, pedagogical clarity, absence of agent notes or governance references, "imperative mood, one-sentence summary," accuracy of the description. A forbidden-token grep (for example "STND", "agent", "LVL") over docstrings and comments is possible, but only catches known strings [K].
- Docstring/signature consistency: Documenter will fail on a missing docstring and on a failing doctest, but does not check that a hand-typed signature line matches the method, or that argument descriptions match behavior. DocStringExtensions.jl's `$(TYPEDSIGNATURES)` generates signatures from the code and removes one drift source [K, not fetched].
- Type-piracy beyond "obvious" cases; type design (abstract vs concrete, whether a struct should be mutable).
- Whether `@inbounds`, `@fastmath`, `@simd`, `@threads` use is valid: needs a written justification and a test.
- Thread safety and data races (no static detector was found in this research; ThreadSanitizer-style tools exist for Julia builds but I did not research them) [K].
- Numerical correctness and tolerances.

---

## 5. Type stability, performance correctness, reproducibility

### Rules (candidate), with evidence

- R-TS1. Public numerical functions are type stable for their documented input types. Evidence: Performance Tips [S]; check with `@inferred` or `@test_opt`/`@report_opt` [S].
- R-TS2. No non-`const` globals read in functions; configuration passed as arguments or held in `const` / `ScopedValue` [S: Performance Tips, 1.11 blog].
- R-TS3. Struct fields concrete, or parametric; no abstract-typed fields and no bare `Array`/`Vector` field types in hot paths [S].
- R-TS4. Hot loops behind function barriers; loops over values from untyped containers are separated into a kernel [S].
- R-TS5. Avoid captured-and-reassigned variables in closures in hot code (`let` block) [S].
- R-TS6. Small, justified unions only (`Union{T,Nothing}`); document the exception [S].

Where type stability does not apply (I-O, setup code, user callbacks) the rule should say "numerical kernels and public API entry points" rather than "all code"; JET `@report_opt` on all code is noisy [K].

### RNG and reproducibility [S unless marked]

- Default generator: Xoshiro256++ with per-task state; `Random.default_rng()` is thread-safe; its concrete type may change between Julia versions.
- Reproducibility requires an explicit seed. Without one, each session differs.
- Child tasks are seeded from their parent without advancing the parent's state (1.10+). The Random docs say this "permits reproducible multithreaded simulations (barring race conditions), independent of scheduler decisions."
- Streams may change between minor releases; relying on a specific stream in tests is "discouraged." Use StableRNGs.jl (`StableRNG(seed)`, LCG-based, "strives for stability," major-version bump if streams change) when exact values matter in tests. StableRNG must be seeded explicitly.
- `@testset ... rng=Xoshiro(seed)` (1.12+) and failure printout of RNG state help replay.
- `RandomDevice` is OS entropy and cannot be seeded; use it only for security-sensitive randomness (SciML guide agrees).

Proposed rules:
- R-RNG1. Every function that draws random numbers takes an `AbstractRNG` as its first argument (Base convention); no hidden use of the global RNG in library code.
- R-RNG2. Libraries never call `Random.seed!` on the global RNG; applications seed once at the entry point and pass `Xoshiro(seed)` objects down. Record the seed and Julia version in outputs.
- R-RNG3. For parallel work, derive per-task or per-chunk RNGs deterministically from the base seed and the chunk index, not from `threadid()` [K; M-X2 is the sourced part].
- R-RNG4. Tests that need exact sample values use StableRNG; tests that should hold on any sample use a fixed seed and statistical tolerances.
- R-RNG5. Doctest examples seed an explicit RNG (M-D5).

### Floating-point determinism

- IEEE 754 binary types; `Float64` literals are default [S].
- `muladd` may fuse multiply-add and "can differ across machines, and on the same machine due to constant propagation or other optimizations"; `fma` is exact but can be slow [S: Base math page].
- `@fastmath`: allows reassociation and assumes no NaN or Inf; can change results [S]. `@simd`: experimental, reorders float reductions [S for "experimental"; reordering effect is [K]].
- `set_zero_subnormals(true)` breaks some identities and affects only the current thread [S].
- `isapprox`: default `rtol` is `sqrt(eps)` of the less precise type for floats; `atol=0`, so `x ≈ 0` is equivalent to `x == 0` without an explicit `atol` [S]. Tests comparing to zero must pass `atol`.
- Multithreaded reductions: result depends on chunking and order, so bitwise reproducibility requires a fixed chunk layout, not `nthreads()`-dependent splitting [K]. BLAS threading and BLAS vendor (OpenBLAS, MKL, Accelerate) can change last-digit results [K; the sourced part is M-P10 on thread counts].
- BigFloat: precision is global state (`setprecision`), `setrounding` is global and "currently only supported for `T == BigFloat`," and both are described as not thread-safe; `@big_str` fixes precision at load time; `BigFloat(2.1)` starts from a `Float64` [S: Base numbers page]. The 1.12 notes say `setprecision` with a function argument became thread safe [S: HISTORY.md]; the Base page directs callers to `ScopedValue`/`@with` for the three-argument form. Rule: use `setprecision(f, BigFloat, p)`; never call the global setter inside library code; pass precision explicitly where possible.
- Hash values are not stable across Julia minor versions (changed in 1.13) [S]; never persist `hash` output.

---

## 6. Docstring conventions and Documenter

Summary of what is already in section 2.3 plus Documenter behavior:

- Docstring layout (manual): indented signature; imperative one-line summary; optional `# Arguments`; prose; `See also`; `# Examples` with `jldoctest`; `# Extended help` for long material; document the generic function rather than every method.
- SciML and Blue add: Blue wants Arguments, Keywords, Returns, Throws sections; docstrings required for exported functions; SciML wants documentation of exported functions and public fields and discourages documenting commonly overloaded methods like `==` [S].
- Interaction with the documentation standard (in draft): the manual's imperative-mood summary, "do not restate types" and "self-contained examples" rules are compatible with "clear pedagogical prose." The manual says nothing about spelling or governance references. The manual's section names (`# Arguments`, `# Examples`) are Julia's equivalent of numpydoc sections; a mapping table would help the custodian align Python and Julia. Julia has no mandated `# Returns` or `# Throws` heading in the manual; Blue adds them [S].
- Keeping docstrings consistent with methods:
  1. `makedocs(modules=[Pkg], checkdocs=:public|:exports)` fails on public names missing from the manual [S].
  2. `jldoctest` fails when example output changes [S]; run it both in docs build and `doctest(Pkg)` in tests.
  3. `Docs.undocumented_names(Pkg)` in a test for stricter coverage [S].
  4. Signature drift is not caught (section 4); `$(TYPEDSIGNATURES)` mitigates [K].
  5. Doctest `filter`s handle non-deterministic output (addresses, timings) [S].
  6. `doctest=:fix` rewrites expected outputs; use only with review, since a wrong output can be silently accepted [S].
- Site generation: `deploydocs` to GitHub Pages from Actions; `julia-actions/julia-docdeploy@v1` runs the build with `GITHUB_TOKEN` and handles `contents: write` and `statuses: write` permissions [S]. Documenter's `warnonly=false` default means broken cross-references fail the build [S].

---

## 7. Package conventions

- **Project.toml** [S]: `name`, `uuid`, `version` (SemVer), `authors`, `[deps]`, `[weakdeps]` + `[extensions]` (1.9+), `[compat]`, `[sources]` (1.11+), `[workspace]` (1.12+). `[extras]` + `[targets]` are legacy; docs recommend a `test/Project.toml` member of a workspace instead (parent package must be listed via `dev .` and `[sources]`). A `[apps]` table makes executables (experimental).
- **Compat** [S]: caret is default; `"1.2"` means `[1.2.0, 2.0.0)`; `0.x` minors are breaking (`"0.2"` means `[0.2.0, 0.3.0)`); `=` pins; hyphen ranges need spaces. General registry (AutoMerge) requires upper-bounded entries for `julia` and every dependency except JLLs; unbounded `">=3"` and `"0"` fail. SciML guidance: no leading caret, bound everything, lower bound is the last tested version, use CompatHelper. CompatHelper is now in maintenance mode and recommends Dependabot, which "now supports Julia" but not private registries [S]. The Pkg compat page's statement that tilde and caret are equivalent for major version 0 conflicts with its own examples; avoid `~` and use caret for clarity [S, flagged].
- **Semantic versioning** [S]: Julia's variant counts only `export`ed and `public` symbols (with documented behavior) as the API. Patch = fixes; minor = additions; major = breaks, including behavior contradicting documentation. This is the reason to use `public` for non-exported API.
- **Registration** [S]: Registrator (`@JuliaRegistrator register`) opens a PR to General; TagBot makes git tags. New packages wait 3 days; new versions 15 minutes. Name rules: ASCII letters/digits, starts uppercase, at least one lowercase, at least 5 characters, no "julia", no "Ju" prefix, no "jl" suffix; similarity checks. Repo URL ends in `/Name.jl.git`. OSI-approved license file required. Dependencies must be registered. Versions must increment by one step. A breaking release needs release notes mentioning "breaking" or "changelog" or AutoMerge is disabled. The General registry's README also states that packages generated without human review are not allowed and substantial LLM contributions should be disclosed in the package README [S]; this applies if the custodian's projects ever register in General. Private projects can use LocalRegistry.jl/RegistryCI.jl [S].
- **CI** [S]: `julia-actions/setup-julia@v3`, `julia-runtest@v1` (inputs: `check_bounds` default yes, `coverage` default true, `depwarn` default yes, `force_latest_compatible_version` default auto, `inline`, `project` default `@.`, `annotate`, `prefix`), `julia-docdeploy@v1`. Not fetched but common: `julia-buildpkg`, `cache`, `julia-processcoverage` [K]. `force_latest_compatible_version` with `julia-actions` tests the lowest allowed bounds when run as min-compat [K on how it is typically used; the `auto` default applies to Dependabot/CompatHelper PRs per action.yml].
- **Package extensions** [S]: optional dependencies go in `[weakdeps]`; extension code in `ext/`; declare the generic function in the parent (`function plot end`) and add methods in the extension. `[compat]` applies to weakdeps. Do not access extension symbols from third-party packages. SciML says avoid Requires.jl.
- **Precompilation** [S]: `@__DIR__` is baked in; use artifacts for bundled data. Heavy `__init__` slows loading. PrecompileTools.jl for workload precompilation.
- **Trimming / juliac** [S]: experimental in 1.12; 1.13 moved `juliac.jl` into the JuliaC.jl package and trims more constructs. Out of scope for a general standard; mention only if a project ships compiled executables.

---

## 8. Recommended rules mapped to the custodian's direction

| Direction | Proposed standard text | Evidence |
|---|---|---|
| "refer to https://docs.julialang.org/en/v1/" | The manual at `/en/v1/` is the normative reference for language semantics, library behavior, and the style, performance, documentation, module, type, and method chapters, at the version matching the project's reference Julia version. Where the manual's text and a project rule differ, the project rule governs and the difference is recorded. | M-S, M-P, M-D, M-M, M-T, M-X |
| "use the latest version available" | Reference Julia version is the latest stable minor release (1.13 as of 2026-10-22) recorded in the project constitution; `julia` compat floor set to it; CI runs `1`, `min`, and `pre`; projects update within a stated period after each minor release. Whether the LTS (1.10) is also supported is a project decision. | Section 1 |
| Style: tool-enforced | One pinned formatter; Aqua, ExplicitImports, JET, `@inferred` or `@test_opt` in the test suite. Naming per manual (M-S13). | Sections 3-4 |
| Docs: American English, pedagogical prose, no agent or governance references, docs consistent with code | Docstring format per M-D1 to M-D9; doctests mandatory for public functions with examples; `checkdocs` enforced; prose rules by review plus a forbidden-token check. | Sections 2.3, 4, 6 |
| Sibling standards (Python: type checking, PEP tools, numpydoc; C++: Core Guidelines) | Julia analogs: JET + `@inferred` (type checking), Runic or JuliaFormatter (style tool), Documenter + jldoctest (numpydoc and doctest), Aqua and ExplicitImports (package hygiene). Julia has no gradual type annotations enforced by a checker; type stability is checked by inference, which is weaker than a Python type checker's guarantees. | Sections 3-4 |

Rules I recommend as **mandatory**: M-S2, M-S11 (no piracy), M-S12, M-S13, M-P1, M-P3, M-P4 (for kernels), M-X2, M-D1 to M-D3, M-D5, M-D7, M-M2, M-T1, R-RNG1, R-RNG2, explicit RNG in doctests, compat bounds on everything, pinned formatter, Aqua, ExplicitImports, doctests in CI.
Rules I recommend as **guidance** (review judgement): M-S4/M-S5 (type annotation breadth), M-P6 to M-P8, M-T8, SciML's mutation and closure preferences.

---

## 9. Open questions for the custodian

1. **Floor vs "latest."** Does "latest version available" mean the compat floor is 1.13 (strict), or that development and CI use the latest while the floor may be lower (for example the 1.10 LTS)? What is the allowed lag after a new minor release (1.14 is not yet announced)?
2. **Tool readiness on 1.13.** DispatchDoctor's README lists active support as `[1.10.0, 1.13.0)`; JET 0.12 lists 1.12 and 1.13 and uses older series for 1.11, and its status on 1.10 was not stated; Aqua's, AllocCheck's, and ExplicitImports' 1.13 status was not stated. Should the standard wait for a verification run (install each tool on 1.13.2 and run its tests) before naming versions? I did not run any code.
3. **Formatter choice.** Runic (zero configuration, no line limit) or JuliaFormatter (configurable, 92-column Blue style, docstring formatting)? Is a 92-column limit wanted for prose in docstrings, given the documentation standard?
4. **Style authority.** Adopt the manual only, or the manual plus Blue Style (explicit `return`, `using` over `import`, `in` loops)? Blue and Runic agree on explicit `return` and `in`; they may differ elsewhere [K].
5. **`public` policy.** Should every non-exported but supported name be marked `public` (needs 1.11+), and is the semver rule "only `export`ed or `public` names are API" adopted?
6. **Test framework.** Plain `Test` with `include`d files, `@safetestset` (SciML), or `@testitem` (ReTestItems)? Is parallel test execution needed?
7. **Coverage.** Required threshold, or report-only? Which service?
8. **Registration.** Will projects go into the General registry (name, license, bounds, LLM-disclosure rules apply) or stay private?
9. **Distributed and GPU.** Is `Distributed` in scope, or only threads? Is GPU code (CUDA.jl and others) in scope? The manual's GPU coverage was not researched.
10. **Threading and determinism.** Is bitwise reproducibility across thread counts required for any code (for example reactor-physics Monte Carlo), or reproducibility for a fixed thread count only? This decides whether chunk layout must be independent of `nthreads()`.
11. **Trimming/JuliaC and Pkg apps.** In scope for distributing executables, or excluded because they are experimental?
12. **Gaps in this research.** I did not fetch: the manual's Profiling page (fetch failed), Constructors, Interfaces, Metaprogramming, FAQ, Environment variables; JuliaFormatter option defaults; Blue Style's own site (the GitHub README was used); DocStringExtensions; PrecompileTools; PkgTemplates; Dependabot's Julia configuration; ThreadSanitizer-style race detection; BLAS reproducibility documentation. Items tagged [K] rest on background knowledge.

---

## Sources (all accessed 2026-10-22)

Release status
- https://docs.julialang.org/en/v1/
- https://julialang.org/downloads/
- https://endoflife.date/julia
- https://julialang.org/blog/2026/09/julia-1.13-highlights/
- https://julialang.org/blog/2025/10/julia-1.12-highlights/
- https://julialang.org/blog/2024/10/julia-1.11-highlights/
- https://docs.julialang.org/en/v1/NEWS/
- https://raw.githubusercontent.com/JuliaLang/julia/master/HISTORY.md
- https://discourse.julialang.org/t/julia-1-13-2-has-been-released/140035.md
- https://discourse.julialang.org/t/congrats-for-julia-1-13/139343.md
- https://discourse.julialang.org/t/minor-versions-publications-scheme/134328.md
- https://github.com/JuliaLang/juliaup

Manual
- https://docs.julialang.org/en/v1/manual/style-guide/
- https://docs.julialang.org/en/v1/manual/performance-tips/
- https://docs.julialang.org/en/v1/manual/documentation/
- https://docs.julialang.org/en/v1/manual/modules/
- https://docs.julialang.org/en/v1/manual/code-loading/
- https://docs.julialang.org/en/v1/manual/types/
- https://docs.julialang.org/en/v1/manual/methods/
- https://docs.julialang.org/en/v1/manual/multi-threading/
- https://docs.julialang.org/en/v1/manual/distributed-computing/
- https://docs.julialang.org/en/v1/manual/workflow-tips/
- https://docs.julialang.org/en/v1/stdlib/Profile/
- https://docs.julialang.org/en/v1/stdlib/Random/
- https://docs.julialang.org/en/v1/stdlib/Test/
- https://docs.julialang.org/en/v1/base/math/
- https://docs.julialang.org/en/v1/base/numbers/

Community style and formatters
- https://github.com/invenia/BlueStyle
- https://docs.sciml.ai/SciMLStyle/stable/
- https://github.com/jrevels/YASGuide
- https://domluna.github.io/JuliaFormatter.jl/stable/ (and /config/, /api/)
- https://github.com/domluna/JuliaFormatter.jl (and /releases)
- https://github.com/fredrikekre/Runic.jl (and /releases)
- https://discourse.julialang.org/t/is-there-a-ruff-like-linter/130871

Checking tools
- https://github.com/aviatesk/JET.jl ; https://aviatesk.github.io/JET.jl/stable/optanalysis/ ; https://aviatesk.github.io/JET.jl/stable/jetanalysis/
- https://github.com/JuliaTesting/Aqua.jl ; https://juliatesting.github.io/Aqua.jl/stable/
- https://github.com/JuliaTesting/ExplicitImports.jl
- https://github.com/JuliaLang/AllocCheck.jl
- https://github.com/MilesCranmer/DispatchDoctor.jl
- https://documenter.juliadocs.org/stable/ ; /man/doctests/ ; /lib/public/
- https://github.com/julia-vscode/TestItemRunner.jl ; https://github.com/JuliaTesting/ReTestItems.jl
- https://github.com/timholy/SnoopCompile.jl
- https://github.com/JuliaDebug/Cthulhu.jl
- https://github.com/JuliaCI/BenchmarkTools.jl
- https://github.com/JuliaRandom/StableRNGs.jl

Packaging and CI
- https://pkgdocs.julialang.org/v1/compatibility/
- https://pkgdocs.julialang.org/v1/toml-files/
- https://pkgdocs.julialang.org/v1/creating-packages/
- https://pkgdocs.julialang.org/v1/apps/
- https://github.com/JuliaRegistries/General
- https://juliaregistries.github.io/RegistryCI.jl/stable/guidelines/
- https://github.com/JuliaRegistries/CompatHelper.jl
- https://github.com/julia-actions/setup-julia
- https://github.com/julia-actions/julia-runtest ; https://raw.githubusercontent.com/julia-actions/julia-runtest/master/action.yml
- https://github.com/julia-actions/julia-docdeploy

---

## Network log

The fetch tool returns a summary, not the raw page, so byte sizes are not exposed. Sizes below are my estimate of the underlying HTML or markdown page (small = under 100 KB, medium = 100-500 KB). Total retrieved volume is well under 10,000 MB and the item count is 74 requests, under 10,000. No paywalled page was requested, no mirror, archive, or cache was used, and no secrets were sent. All requests went through the configured proxy.

| # | URL | Result | Approx. size |
|---|---|---|---|
| 1 | https://docs.julialang.org/en/v1/ | OK | medium |
| 2 | https://julialang.org/downloads/ | OK | small |
| 3 | WebSearch "Julia 1.13 release 2026" | OK | search results |
| 4 | https://discourse.julialang.org/t/julia-1-13-2-has-been-released/140035.md | OK | small |
| 5 | https://discourse.julialang.org/t/congrats-for-julia-1-13/139343.md | OK | small |
| 6 | https://docs.julialang.org/en/v1/NEWS/ | OK | medium |
| 7 | https://julialang.org/blog/2025/10/julia-1.12-highlights/ | OK | small |
| 8 | https://julialang.org/blog/2024/10/julia-1.11-highlights/ | OK | small |
| 9 | https://raw.githubusercontent.com/JuliaLang/julia/master/HISTORY.md | OK | medium |
| 10 | https://julialang.org/downloads/#supported_platforms | OK | small |
| 11 | WebSearch "Julia 1.13 highlights blog julialang.org" | OK | search results |
| 12 | WebSearch "Julia next LTS release after 1.10..." | OK | search results |
| 13 | https://julialang.org/blog/2026/09/julia-1.13-highlights/ | OK | small |
| 14 | https://endoflife.date/julia | OK | small |
| 15 | https://discourse.julialang.org/t/minor-versions-publications-scheme/134328.md | OK | small |
| 16 | https://docs.julialang.org/en/v1/manual/style-guide/ | OK | small |
| 17 | https://docs.julialang.org/en/v1/manual/performance-tips/ | OK | medium (summary said threading section cut off) |
| 18 | https://docs.julialang.org/en/v1/manual/documentation/ | OK | medium |
| 19 | https://docs.julialang.org/en/v1/manual/modules/ | OK | medium |
| 20 | https://docs.julialang.org/en/v1/manual/code-loading/ | OK | medium |
| 21 | https://docs.julialang.org/en/v1/manual/types/ | OK | medium |
| 22 | https://docs.julialang.org/en/v1/manual/methods/ | OK | medium |
| 23 | https://docs.julialang.org/en/v1/manual/multi-threading/ | OK | small |
| 24 | https://docs.julialang.org/en/v1/manual/distributed-computing/ | OK | medium |
| 25 | https://docs.julialang.org/en/v1/manual/profiling/ | FAIL (client_error), 3 attempts | none |
| 26 | https://docs.julialang.org/en/v1/manual/workflow-tips/ | OK | small |
| 27 | https://docs.julialang.org/en/v1/stdlib/Random/ | OK | medium |
| 28 | https://docs.julialang.org/en/v1/stdlib/Test/ | OK | medium |
| 29 | https://blue-style.github.io/BlueStyle/ | FAIL (client_error) | none |
| 30 | https://docs.sciml.ai/SciMLStyle/stable/ | OK | medium |
| 31 | https://github.com/jrevels/YASGuide | OK | small |
| 32 | https://domluna.github.io/JuliaFormatter.jl/stable/ | OK | small |
| 33 | https://github.com/fredrikekre/Runic.jl | OK | small |
| 34 | https://github.com/domluna/JuliaFormatter.jl | OK | small |
| 35 | https://github.com/invenia/BlueStyle | OK | small |
| 36 | https://domluna.github.io/JuliaFormatter.jl/stable/config/ | OK | small |
| 37 | https://github.com/aviatesk/JET.jl | OK | small |
| 38 | https://github.com/JuliaTesting/Aqua.jl | OK | small |
| 39 | https://github.com/JuliaTesting/ExplicitImports.jl | OK | small |
| 40 | https://github.com/JuliaLang/AllocCheck.jl | OK | small |
| 41 | https://github.com/MilesCranmer/DispatchDoctor.jl | OK | small |
| 42 | https://documenter.juliadocs.org/stable/ | OK | small |
| 43 | https://documenter.juliadocs.org/stable/man/doctests/ | OK | medium |
| 44 | https://documenter.juliadocs.org/stable/lib/public/ | OK | medium |
| 45 | https://pkgdocs.julialang.org/v1/compatibility/ | OK | small |
| 46 | https://pkgdocs.julialang.org/v1/toml-files/ | OK | small |
| 47 | https://pkgdocs.julialang.org/v1/creating-packages/ | OK | medium |
| 48 | https://github.com/JuliaRegistries/General | OK | small |
| 49 | https://github.com/JuliaLang/juliaup | OK | small |
| 50 | https://juliaregistries.github.io/RegistryCI.jl/stable/guidelines/ | OK | small |
| 51 | https://github.com/julia-actions/setup-julia | OK | small |
| 52 | https://github.com/julia-actions/julia-runtest | OK | small |
| 53 | https://github.com/JuliaTesting/TestItems.jl | FAIL (client_error) | none |
| 54 | https://raw.githubusercontent.com/julia-actions/julia-runtest/master/action.yml | OK | small |
| 55 | https://github.com/julia-vscode/TestItemRunner.jl | OK | small |
| 56 | https://github.com/JuliaTesting/ReTestItems.jl | OK | small |
| 57 | https://github.com/timholy/SnoopCompile.jl | OK | small |
| 58 | https://github.com/JuliaDebug/Cthulhu.jl | OK | small |
| 59 | https://docs.julialang.org/en/v1/base/math/ | OK | medium |
| 60 | https://docs.julialang.org/en/v1/base/numbers/ | OK | medium |
| 61 | https://github.com/JuliaRandom/StableRNGs.jl | OK | small |
| 62 | https://github.com/JuliaCI/BenchmarkTools.jl | OK | small |
| 63 | https://github.com/JuliaRegistries/CompatHelper.jl | OK | small |
| 64 | https://aviatesk.github.io/JET.jl/stable/optanalysis/ | OK | small |
| 65 | https://aviatesk.github.io/JET.jl/stable/jetanalysis/ | OK | small |
| 66 | https://juliatesting.github.io/Aqua.jl/stable/ | OK | small |
| 67 | https://domluna.github.io/JuliaFormatter.jl/stable/api/ | OK | small |
| 68 | https://github.com/fredrikekre/Runic.jl/releases | OK | small |
| 69 | https://github.com/domluna/JuliaFormatter.jl/releases | OK | small |
| 70 | https://pkgdocs.julialang.org/v1/apps/ | OK | small |
| 71 | https://github.com/julia-actions/julia-docdeploy | OK | small |
| 72 | https://docs.julialang.org/en/v1/stdlib/Profile/ | OK | small |
| 73 | WebSearch "Julia linter naming conventions ..." | OK | search results |
| 74 | https://discourse.julialang.org/t/is-there-a-ruff-like-linter/130871 | OK | small |

Failures: 5 requests (profiling x3, Blue Style site, TestItems repo). No retries beyond those listed.
