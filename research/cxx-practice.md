# C++ practice research note for LVL2 (scientific and instrumentation software)

Author: research agent (STND.CREW), delegation depth 1
Date accessed for all sources: 2026-10-22 (today)
Scope: read-only retrieval; no work product other than this note was changed. Scratch downloads (the Core Guidelines markdown) sit in the session scratchpad only.

Confidence tags used below:
- [V] read in a primary source during this session (standard text, project docs, vendor docs, the Core Guidelines source).
- [S] reported by the fetch tool's summarizer from a page; plausible but not read verbatim. Re-check before quoting.
- [K] my own background knowledge, not verified in this session. Treat as a lead.

Retrieved content was treated as data. I saw no embedded instructions in any retrieved page.

---

## 0. Summary of recommended LVL2 rules

These are recommendations for the custodian to accept, change, or reject. Rule IDs in parentheses are Core Guidelines (CG) IDs unless stated.

Standard and toolchain
1. Name the language level per project as the newest ISO standard that every toolchain in the project's support matrix fully supports. Today that is C++23 for any project that builds with NVCC or MSVC, and C++23 or C++26 (partial) for GCC/Clang-only host code. C++26 is technically complete but not yet an ISO publication (section 7). Allow individual C++26 features behind feature-test macros once every toolchain in the matrix has them.
2. Set `CXX_STANDARD`, `CXX_STANDARD_REQUIRED ON`, `CXX_EXTENSIONS OFF`. Review the level after each GCC, Clang, MSVC, and CUDA release, and when ISO publishes C++26.

Ownership and pointers (section 3 has the full decision set)
3. No owning raw pointers outside resource-handle internals and C-API boundary wrappers (R.3, R.11, I.11). Use values, containers, `std::unique_ptr`; `std::shared_ptr` only for real shared ownership (R.20, R.21).
4. Non-owning, never null: reference. Non-owning, may be null or rebindable: `T*` (F.60). Mark non-null pointers `not_null<T*>` where the pointer form is needed (I.12, F.23).
5. Sequences are `std::span` or `std::mdspan`, never pointer plus count, outside a C-ABI edge (F.24, R.14, I.13, ES.42).
6. Pointer arithmetic only inside container, view, or iterator implementations and documented kernels (ES.42, Bounds.1).
7. Smart-pointer parameters only to express ownership transfer or reseating (F.7, R.30 to R.37, GotW #91).
8. Hardware registers and device pointers get distinct types confined to one adapter layer (CP.200, sections 3.6 and 3.7).

STL preference and limits
9. Default to the standard library (SL.1, SL.2). Leaving it requires a recorded reason from a closed list: freestanding or no-heap target, hard real-time path, measured hot spot (Per.6), ABI or API interop. Name the replacement (`std::pmr`, `std::array`, `std::inplace_vector`, ETL).
10. Use `std::expected` (C++23) rather than a project-specific result type unless exceptions are disabled and `expected` is unavailable on the target.

Generic code and header-only
11. Header-only is the default for templates; non-template code of any size goes in a compiled library. Headers contain only templates, `inline`/`constexpr` entities, and short inline functions (SF.2, T.84).
12. Do not require C++20 modules in LVL2. Provide headers; add module wrappers per project when the whole toolchain matrix supports them.

Template metaprogramming (section 6)
13. Concepts and `requires` clauses, not `enable_if`/SFINAE (T.10, T.11, T.120). Name every non-trivial constraint as a concept.
14. `constexpr`/`consteval` functions and `if constexpr` instead of type-level recursion (T.123). Fold expressions, pack indexing, and expansion statements instead of recursive templates.
15. Every TMP facility has a one-paragraph comment, example input/output, and `static_assert` tests beside it (T.150). `static_assert` messages state what the caller should change.
16. P2996 reflection is allowed in C++26 builds only inside dedicated, tested utility headers, once all toolchains in the matrix support it. Today only GCC 16 does.

Naming (section 8)
17. snake_case for variables, functions, namespaces, concepts, and STL-like types; CamelCase for other classes and structs. Define "STL-like" by a test (section 8.3). Macros ALL_CAPS only (NL.9).

Mechanical enforcement (section 9)
18. Commit `.clang-format` and `.clang-tidy`; CI runs clang-format `--dry-run --Werror`, clang-tidy with a named `cppcoreguidelines-*` subset, warnings as errors in CI only (not in exported INTERFACE flags), ASan+UBSan and TSan jobs, and hardened-library builds (`_GLIBCXX_ASSERTIONS`, `_LIBCPP_HARDENING_MODE_FAST`, `_MSVC_STL_HARDENING=1`).

---

## 1. The C++ Core Guidelines

### 1.1 State of the document and repository

- Document date: "Jun 14, 2026". Editors: Bjarne Stroustrup and Herb Sutter. The introduction says: "Had it been an open-source (code) project, this would have been release 0.8." [V, CppCoreGuidelines.md source, 841,419 bytes, and rendered page]
- Repo `isocpp/CppCoreGuidelines`: default branch `master`; 2,208 commits; 238 open issues; 9 open pull requests; 45.3k stars; Releases section empty. The README says it is a constantly evolving document without a strict release cadence and that the browsable HTML on isocpp.github.io is manually integrated and can lag `master`. [S]
- I could not get per-commit dates: github.com commit history is blocked to the fetcher (robots), and the GitHub API via `gh` returned 403 ("GitHub access to this repository is not enabled for this session"). I did not try to work around that. The June 14, 2026 date is the best evidence of the last editorial release. Open question: whether the custodian wants a pinned commit hash recorded in LVL2.
- Structure (514 rule headings in the source): In, P (Philosophy, P.1 to P.13), I (Interfaces), F (Functions), C (Classes), Enum, R (Resource management), ES (Expressions and statements), Per (Performance), CP (Concurrency), E (Error handling), Con (Constants), T (Templates), CPL (C-style), SF (Source files), SL (Standard library); supporting: A, NR (non-rules and myths), RF (references), Pro (profiles), GSL, NL (naming and layout). [V]
- Gaps that matter to scientific code [V, by reading the source]:
  - Per.14 and Per.15 (minimize allocations; do not allocate on a critical branch) are stubs that say "???".
  - There is no rule section on floating-point semantics, reproducibility, or numerical stability. The word "floating" appears 8 times, none in a rule about numerics. Rules ES.46, ES.100 to ES.105 cover integer conversions and overflow only.
  - Profiles (Pro) are still design statements: Type, Bounds, and Lifetime (the lifetime one links to a PDF design spec). They are not a standard feature.

### 1.2 The GSL (Guidelines Support Library)

- CG says the GSL is header-only, in namespace `gsl`, lightweight, and that "names might be aliases for standard library" names. Components: views (`owner`, `not_null`, `span`, `span_p`, `zstring`/`czstring`), owners (`unique_ptr`, `shared_ptr`, `stack_array`, `dyn_array`), assertions (`Expects`, `Ensures`), utilities (`finally`, `narrow_cast`, `narrow`, `joining_thread`, `index`), and old concept names now covered by C++20. [V]
- Microsoft GSL (github.com/microsoft/GSL): header-only; C++14 through C++23; CMake 3.14+, target `Microsoft.GSL::GSL`; README lists CI on GCC 12 to 14, Clang 16 to 18, Xcode, VS 2019/2022. `owner` is an alias for a raw pointer. `multi_span`, `strided_span`, `string_span` are deprecated; `unique_ptr`, `shared_ptr`, `byte` aliases deprecated in favor of `std`. `Expects`/`Ensures` terminate on failure. Releases page empty; README pins `v5.0.0` in its FetchContent example. [S]
- Practical consequence: `std::span` replaced `gsl::span` (but std::span is not bounds-checked until hardening, section 3.9). `gsl::owner`, `gsl::not_null`, `gsl::narrow`, `gsl::finally`, and `Expects`/`Ensures` are the pieces without a standard equivalent. The clang-tidy check `cppcoreguidelines-owning-memory` needs only a type named `gsl::owner<T*>`; it does not require the real GSL. [V]
- Open question: depend on Microsoft GSL (a dependency to govern) or provide a four-line `owner` alias plus a project `not_null`/`narrow`.

### 1.3 Enforcement

clang-tidy (docs page labeled "Extra Clang Tools 24.0.0git (In-Progress)"): 43 `cppcoreguidelines-*` checks [S, list read from the page]:
avoid-c-arrays, avoid-capturing-lambda-coroutines, avoid-const-or-ref-data-members, avoid-do-while, avoid-goto, avoid-magic-numbers, avoid-non-const-global-variables, avoid-reference-coroutine-parameters, c-copy-assignment-signature, explicit-constructor, explicit-virtual-functions, init-variables, interfaces-global-init, macro-to-enum, macro-usage, misleading-capture-default-by-value, missing-std-forward, narrowing-conversions, no-malloc, no-suspend-with-lock, noexcept-destructor, noexcept-move-operations, noexcept-swap, non-private-member-variables-in-classes, owning-memory, prefer-member-initializer, pro-bounds-array-to-pointer-decay, pro-bounds-avoid-unchecked-container-access, pro-bounds-constant-array-index, pro-bounds-pointer-arithmetic, pro-type-const-cast, pro-type-cstyle-cast, pro-type-member-init, pro-type-reinterpret-cast, pro-type-static-cast-downcast, pro-type-union-access, pro-type-vararg, rvalue-reference-param-not-moved, slicing, special-member-functions, use-default-member-init, use-enum-class, virtual-class-destructor.
- `owning-memory` implements I.11, C.33, R.3, and the GSL.Views section; it is type-based and not flow-sensitive. [V]
- `pro-bounds-avoid-unchecked-container-access` flags `operator[]` on STL containers (default exclusions: map, unordered_map, flat_map), maps to SL.con.3 and Bounds.4, with a fix mode `at` or `function`. [V]
- Other families (counts from the page, approximate): bugprone ~109, modernize ~52, cert ~42, misc ~29, performance ~24, concurrency 2; `hicpp-*` none on this page. [S]
- No `cppcoreguidelines-*` check covers lifetime (Lifetime.1). Clang's separate lifetime-safety analysis does (section 3.9).

MSVC: C++ Core Check, installed with Visual Studio 2017/2019 per the page I could fetch (page content describes VS 2015 to 2019; I could not confirm current VS 2026 packaging). Enable via project property "Enable Code Analysis on Build" or `/analyze` with `/analyze:plugin EspXEngine.dll` and `esp.extensions=cppcorecheck.dll`; rule sets "Native Recommended", "Native Minimum", "C++ Core Check Rules"; groups include Bounds, Lifetime, Type, Owner Pointer, Raw Pointer, Shared Pointer, Unique Pointer, STL, Style; suppress with `[[gsl::suppress("r.11")]]`. [V]

### 1.4 Rules that most directly bear on each custodian direction

| Custodian direction | Most relevant CG rules | Note |
|---|---|---|
| "refer to the Core Guidelines" | P.1 to P.13, esp. P.2 (ISO C++), P.4 and P.5 (static type safety, compile-time checking), P.8 (no leaks), P.10 (prefer immutable), P.12/P.13 (tools, libraries); NL.8 | CG itself says choose a house style and leave imported libraries in their own style (NL.8). |
| Prefer STL unless performance or resources prohibit | SL.1, SL.2, SL.4, ES.1, T.124, P.13; Per.1 to Per.6 (do not optimize without measurement); Per.4, Per.5 (complex or low-level code is not necessarily faster); E.25 to E.27 (no-exceptions fallbacks) | Per.6 is the natural gate for leaving the STL. |
| Raw pointers: when and when not | I.11, I.12, I.13, F.7, F.15 to F.27, F.42 to F.45, F.60, R.1 to R.5, R.10 to R.15, R.20 to R.24, R.30 to R.37, C.32, C.33, ES.42, ES.47, ES.60 to ES.65, Pro.bounds, CP.31, CP.200, I.26, I.30, E.19 | Section 3. |
| Snake_case / CamelCase | NL.5, NL.7, NL.8, NL.9, NL.10, C.100 (follow the STL when defining a container) | NL.10 prefers underscore style but only "if you have a choice" and consistency beats taste. |
| Generic, header-only | T.1 to T.3, T.10 to T.13, T.20 to T.26, T.41, T.43, T.47, T.60, T.62, T.84, T.143, SF.2, SF.7, SF.8, SF.11, SF.21, SF.22, I.9, I.27 | SF.2: headers must not contain object definitions or non-inline function definitions. |
| TMP, human-interpretable | T.120 to T.125, T.150, T.22, T.25, T.48, T.69, T.144, F.4, Per.11, ES.30, ES.31 | T.120: use TMP only when you really need to. T.123: prefer `constexpr` functions. T.101 is a stub ("???"). |
| Latest C++ standard | P.2 (write in ISO Standard C++) | P.2 favors the published ISO standard over extensions. |

---

## 2. The gist

Source: https://gist.github.com/b7r6/5dde648f5dc1dea1e9039f2211f5d40a. Fetched twice. Both results are summaries from the fetch tool, not verbatim text, so every claim below is [S]. The custodian's team should read the original before quoting it in LVL2.

Metadata: file `straylight-cxx-house-style.md` by b7r6, created June 22, 2026, labeled a secret gist, 10 stars, 3 forks; roughly 8,000 to 9,000 words (about 55 KB) of body text.

Purpose: a style and architecture guide for the "straylight" codebase, aimed at agent-heavy development where agents write code quickly and humans read and debug it. Central rule: "Optimize for disambiguation, not brevity."

Content:
- High-level choices: explicit types over `auto` for agent-written code (humans may use `auto` when obvious); fully qualified names, no `using namespace`; C++23; measure before optimizing; grep-friendly unique names; adopt best-in-class libraries.
- Naming: snake_case for everything (including types), acronym case preserved (`BLAKE3_hasher`), full words over abbreviations, domain prefixes, trailing underscore on data members (`socket_fd_`), a "three-letter rule" (abbreviations under four characters are too short), a short approved list (`idx/jdx`, `rxbuf/txbuf`, `ctx`, `fd`, `op/ops`).
- Arguments: small trivially copyable types (`int`, `string_view`, `span`, pointers, enums) by value; read-only by `const T&`; sinks by value then `std::move`; in/out by `T&` with an obvious name; avoid out-parameters; return by value.
- Errors: exceptions are not thrown; recoverable errors return `result<T>`; unrecoverable ones are fatal; construct errors with specific `fail_*` helpers.
- Modern C++23: `std::span` for views, `std::mdspan` for multidimensional data, `constexpr` where it does not complicate things, `const` everything including locals and parameters, `[[nodiscard]]`.
- Templates: concepts used for a machine interface; "template gymnastics without purpose" rejected.
- Headers: `#pragma once`; headers and implementations side by side. No explicit header-only policy.
- Tooling: clang-format, clang-tidy, sanitizers, and warning flags are not covered. It specifies `-O3 -march=native`, clang optimization remarks, nanobench, `nvcc`/`cuobjdump` inspection.
- Architecture: an "extended Mealy machine" pattern `State x Event -> State x [Operation]` for async I/O, replay testing, `stable_ref`/`stable_span` buffer rules, Lean-proven laws and code generation, `std::visit` overload sets.
- Library table (winner over defeated): BLAKE3 over OpenSSL SHA-256; RE2 over `std::regex`; Stringzilla over `std::string` ops; `std::format` over Boost.Format; simdjson over nlohmann-json; llhttp; Ada over Boost.URL; io_uring over epoll; Taskflow over `std::async`; spdlog; nanobench over Google Benchmark; mimalloc over jemalloc/glibc; `absl::flat_hash_map` over `std::unordered_map`; `phmap::parallel_flat_hash_map`; `absl::btree_map` over `std::map`; concurrentqueue; CCCL (Thrust, CUB, libcu++) for CUDA.
- Hardware section: SWAR, auto-vectorization checks, branchless code, warp divergence, mandatory CUDA error checking.
- Collaboration: comment conventions that differ for agents and humans, a "five-minute rule", property-based tests, replay tests, fuzzing parsers.
- Quote reported: "A reference is a pointer you don't have to feel guilty about."
- Raw pointers: no general policy; discourages pointer-plus-size APIs. Smart pointers: used for owning members; move-only sinks (`unique_ptr`) by value.

Alignment and conflict with CG and with the custodian's directions:

| Gist point | Versus CG / custodian | Verdict |
|---|---|---|
| Pass small types by value, `const T&` otherwise | F.16 | Aligns. |
| Avoid out-parameters; return by value | F.20, F.21 | Aligns. |
| `span`/`mdspan` for views | F.24, R.14, ES.42 | Aligns. |
| No `using namespace` | SF.7 (SF.6 allows it for `std` or local scope) | Aligns, stricter. |
| `const` everywhere | Con.1 to Con.5, ES.25 | Aligns. Const by-value parameters are not a CG rule. |
| `constexpr` where it does not complicate | F.4 | Aligns. |
| Concepts, no gymnastics | T.10, T.120 | Aligns. |
| Sink by value then move | F.16/F.18 prefer `const&` plus `&&` overloads, or `X&&`, for efficiency; F.15 prefers simple conventional passing | Minor conflict; by-value costs one extra move and is simpler. Choose one. |
| Explicit types over `auto` for agents | ES.11 and T.12 encourage `auto`; Google style gives a "clearer or safer" test [S] | Conflict with CG; a project-level choice. |
| No exceptions; custom `result<T>` | I.10, E.2, E.5 prefer exceptions; E.25 to E.27 give no-exception fallbacks | Conflict in default; `std::expected` (C++23) is the STL option, which also fits the custodian's STL-first rule. |
| `#pragma once` | SF.8: use include guards; CG notes `#pragma once` is a vendor extension; P.2 | Conflict in letter. All toolchains in the matrix accept it [K]; decide. |
| snake_case for all names including types | Custodian wants CamelCase for classes and structs | Conflict with the custodian. |
| Three-letter rule, no short names | NL.7: name length proportional to scope; CG says short names are fine in small scopes | Conflict for math-heavy code (`x`, `dt`, `n`). |
| Member suffix `_` | NL.8 (consistency), NL.5 (no type encoding) | Compatible; clang-tidy `MemberSuffix` can enforce it. |
| absl, phmap, mimalloc, simdjson, etc. | Custodian: STL unless performance or resources prohibit; SL.2 | Only valid through the performance exemption; the gist's benchmark claims are not independently checked here. |
| `-O3 -march=native` | Not in CG | For scientific code this ties results to the build host and can change floating-point results via FMA contraction and vectorization [K]. Decide separately. |
| No stance on raw pointers, header-only, exceptions policy detail, tooling | n/a | Gist does not settle the custodian's questions. |

The gist does not mention sanitizers or clang-tidy; LVL2 must supply those.

---

## 3. Raw pointers: decision rules

### 3.1 What the Core Guidelines say [V unless marked]

- R.3: a raw pointer `T*` is non-owning. Owning raw pointers are marked `owner<T*>`. Exception: legacy code and C ABIs. `owner<T*>` "has no default semantics beyond `T*`". If an `owner<T*>` is a member, the class needs a destructor (C.33).
- R.4: a raw reference `T&` is non-owning.
- R.2 / I.13 / F.24 / R.14 / ES.42: `T*` denotes an individual object; arrays are a container or `span`. "Flag pointer arithmetic (including `++`) on a pointer that is not part of a container, view, or iterator."
- I.11: never transfer ownership by raw pointer or reference. Return by value, or use `unique_ptr`/`shared_ptr`, or `owner` in old code. "Every object passed as a raw pointer (or iterator) is assumed to be owned by the caller."
- I.12 / F.23: declare a pointer that must not be null `not_null`; this also removes redundant null checks.
- F.7: for general use take `T*` or `T&` rather than smart pointers. A smart-pointer parameter transfers or shares ownership and restricts callers.
- F.22: `T*` or `owner<T*>` designate a single object. F.42: return `T*` only to indicate a position. F.43: never return a pointer or reference to a local. F.60: prefer `T*` over `T&` when "no argument" is valid. F.16: pass cheap types (two or three words) by value. F.17 in/out by non-const reference. F.18 will-move-from by `X&&`.
- R.5: prefer scoped objects. R.10: avoid `malloc`/`free`. R.11: avoid explicit `new`/`delete`. R.12, R.13: hand each allocation to a manager immediately, one allocation per statement.
- R.20 to R.24: use `unique_ptr` or `shared_ptr` for ownership; prefer `unique_ptr` ("simpler, more predictable, and faster, you don't implicitly maintain a use count"); `make_shared`, `make_unique`; `weak_ptr` to break cycles.
- R.30 to R.37: smart pointers as parameters only to express lifetime semantics: `unique_ptr<T>` by value to take ownership (R.32), `unique_ptr<T>&` to reseat (R.33), `shared_ptr<T>` by value to share (R.34), `shared_ptr<T>&` to reseat (R.35), `const shared_ptr<T>&` to maybe retain (R.36). R.37: do not pass a pointer or reference obtained from an aliased smart pointer, because a callee may reset the global and destroy the object.
- C.32: if a class has a raw pointer or reference member, decide whether it owns. C.12: do not make data members `const` or references in copyable or movable types.
- Pro.bounds: no pointer arithmetic (use `span`), constant indexes only, no array-to-pointer decay, no non-bounds-checked library calls. Pro.lifetime: Lifetime.1, "don't dereference a possibly invalid pointer".
- I.26: for a cross-compiler ABI, use a C-style subset. E.19: `final_action` for cleanup when no handle exists.

GotW #89 (Sutter): "unique_ptr by default and shared_ptr if sharing is needed"; `make_shared` allocates object and control block together; "Don't use explicit new, delete, and owning * pointers, except in rare cases." [V, summary of the page]
GotW #91 (Sutter): pass `widget*`/`widget&` for observing (`*` if null is meaningful); `unique_ptr<widget>` by value is a sink; `unique_ptr<widget>&` only to modify the pointer; `shared_ptr<widget>` by value to store or share; `shared_ptr<widget>&` only to modify it; `const shared_ptr<widget>&` only when it might share; avoid `const unique_ptr&`; a `shared_ptr` copy costs an atomic increment and decrement and can contend on the count's cache line. [V]

### 3.2 Costs

- `unique_ptr` with `default_delete`: same size as a raw pointer, no count, same generated code for dereference and release as a hand-written owner [K]. Exceptions: a stateful deleter grows the object, and under the Itanium C++ ABI a by-value `unique_ptr` argument is passed in memory, not in a register, because it has a non-trivial destructor, so it is not free as a parameter [K].
- `shared_ptr`: two words, a control block, atomic count updates when the program is multithreaded [K]; GotW #91 confirms atomic count traffic and scalability cost. `make_shared` merges the allocations (GotW #89). CG R.21 says use `unique_ptr` unless sharing is needed.
- `span`: static extent stores only the pointer; dynamic extent stores pointer plus size. Trivially copyable (C++23). [V, cppreference]
- References compile to pointers; a reference member makes a type non-assignable (C.12), which is one legitimate reason to store `T*` or `not_null<T*>`.

### 3.3 Decision rule set

D1. Ownership: if something is created and destroyed, give it a value, a container, or a `unique_ptr` (R.1, R.5, R.20, R.21). Return by value when the type is movable (I.11, F.20). Use `shared_ptr` only when two or more owners have independent lifetimes, and document who they are.
D2. Observation, never null, no rebinding: `T&` or `const T&` (F.7, F.16, F.60, GotW #91).
D3. Observation that may be null, optional, rebindable, or stored in a copyable/assignable class: `T*`. If it must not be null, `not_null<T*>` or a project equivalent (I.12, F.23). A plain `T*` always means "non-owning, points at one object or null" (R.3, F.22).
D4. A sequence of elements: `std::span<T>` / `std::span<const T>`; multidimensional: `std::mdspan`. A `(T*, n)` pair appears only at a C-ABI edge, converted to `span` immediately (F.24, R.14, I.13).
D5. Pointer arithmetic: only inside implementations of containers, views, iterators, and clearly marked inner kernels, each with a comment stating the bounds invariant (ES.42, Bounds.1). Prefer iterators and ranges.
D6. Smart-pointer parameters follow R.30 to R.37 and GotW #91. If the callee only uses the object, pass `*p` or `p.get()` as `T&`/`T*`. Do not pass a pointer or reference derived from a shared or global smart pointer into code that can reset it (R.37).
D7. Returning a pointer means "position of an existing object that the caller does not own" (F.42). Never return a pointer or reference to a local or to a temporary (F.43). Annotate returns that borrow from an argument with `[[clang::lifetimebound]]` where the compiler supports it (3.9).
D8. Owning raw pointers are allowed in exactly two places: inside the implementation of a resource handle (mark `owner<T*>`), and in a thin wrapper around a C or vendor API that immediately hands the resource to an RAII type, typically `unique_ptr<T, Deleter>` (R.12, R.13, E.19). Each use carries a comment naming the release function.
D9. `nullptr` only (ES.47). Initialize every pointer (ES.20). No `NULL`, no `0`.
D10. No `malloc`/`free`/`new[]`/`delete[]` in new code (R.10, R.11, ES.61).
D11. A class with a raw pointer or reference member states in a comment whether it owns (C.32); if it owns, it has the full special-member set or uses a handle type (C.33, C.21).

### 3.4 C APIs and ABIs

- Keep the C interface at the edge: pointer plus length in, `span` inside. Treat pointers handed back by C code as owners until wrapped (R.12). For `extern "C"` the exposed type must be C-compatible; I.26 says use a C-style subset for a cross-compiler ABI; I.27 suggests Pimpl for a stable library ABI.
- Use `std::unique_ptr<T, D>` with a stateless function-object deleter for handles such as `FILE*`, FFT plans, HDF5 or netCDF IDs [K].
- Variadics (`va_arg`) are banned except to call C (F.55, Type.8).

### 3.5 MPI

- MPI C++ bindings were deprecated in MPI-2.2 and removed in MPI-3.0 [V, MPI-5.0 report section 18.2]. Use the C API. MPI-4.0 and later add `_c` large-count variants taking `MPI_Count`/`MPI_Aint` in place of `int` [V, section 20.2]. MPI buffer arguments are `void*` (or `const void*`) with a count and datatype [K; the pages I read did not state it].
- Rule: one translation unit (or header section) wraps MPI. Public functions take `std::span<T>` (or `mdspan` plus a layout check) and derive `data()`, count, and datatype from `T`. Check that `span::size()` fits the count type with `gsl::narrow`-style checking, or use `_c` calls where the implementation provides them. Raw `void*` never appears outside the wrapper.
- Non-blocking calls keep the buffer alive past the call. The wrapper must carry the buffer's lifetime (a request object that owns or borrows with a documented lifetime), because `span` does not extend lifetime (R.37 logic).

### 3.6 CUDA and device pointers

- A device pointer is not dereferenceable on the host. A plain `T*` for device memory hides that. Rule: use a distinct type (a thin project `device_ptr<T>`, or Thrust/CCCL equivalents) at API boundaries; plain `T*`/`span<T>` only inside kernels and `__host__ __device__` code where the memory space is known [K for the Thrust names].
- libcu++: `cuda::std::` facilities work in host and device code, `cuda::device::` only in device code; `std::` is host-only [S]. Device `malloc`/`new` use a fixed device heap (default 8 MB) and device memory cannot be freed by host calls [V, CUDA guide 13.4.2]. Ownership of device allocations belongs in RAII wrappers with `cudaFree` deleters.
- Device-code limits relevant here: C++20 modules and coroutines unsupported; extended lambdas need `--extended-lambda` [V].
- Check every CUDA runtime return (the gist also requires this).

### 3.7 Memory-mapped hardware registers (embedded)

- CP.200: use `volatile` only to talk to non-C++ memory; CP.8: never use `volatile` for synchronization. cppreference: volatile is for signal handlers, "not suitable for communication with another thread", and some uses are deprecated (C++20: `++`/`--` on a volatile lvalue, direct assignment used as a value, volatile parameters and return types, volatile in structured bindings). [V]
- Rule: one hardware-abstraction header per device defines register types. The address is a `constexpr std::uintptr_t`; the access goes through one `reinterpret_cast<volatile T*>` inside a small class with `read()`/`write()` (not `++=` forms). Callers never see the pointer. The cast from an integer is implementation-defined; document the supported compilers. Static analysis will flag `reinterpret_cast` (`cppcoreguidelines-pro-type-reinterpret-cast`); suppress locally with a reason, in that one layer only (I.30, `[[gsl::suppress]]`).
- For memory regions that hold ordinary data (memory-mapped files, DMA buffers, shared memory, network buffers), use `std::start_lifetime_as<T>` / `start_lifetime_as_array` (C++23, implicit-lifetime types, undefined if misaligned or too small) rather than a bare `reinterpret_cast`. [V, cppreference]
- Pointer-sized math on addresses goes in the register layer, not in application code. `std::bit_cast` for reinterpretation of values [K].

### 3.8 `std::observer_ptr`

- `std::experimental::observer_ptr` is in Library Fundamentals TS v2 (`<experimental/memory>`). It is a non-owning "near drop-in replacement for raw pointer types ... a vocabulary type". cppreference lists it only under Experimental. [V]
- The original proposal is N3840/N4282 "World's Dumbest Smart Pointer" (Walter E. Brown) [S, search results]. I found no sign of adoption into C++20, 23, or 26; the C++26 feature lists I read do not include it. A Boost list thread is titled "We need a proposal to change experimental::observer_ptr" [search title only]. libstdc++ ships `<experimental/memory>` [S, search listing]; I did not verify libc++ or MSVC.
- Recommendation: do not use it. Use `T&`, `T*`, and `not_null<T*>` under rules D2 and D3. Revisit only if it enters an IS.

### 3.9 Hardening, contracts, lifetime

- C++26 hardened standard library (P3471R4): turns selected library preconditions into contract violations. Covered: `span` and `string_view` element access and `front`/`back`/`first`/`last`/`subspan`, sequence-container `operator[]`/`front`/`back`/`pop_*`, `optional`/`expected` access, `mdspan`, `bitset`, `valarray`. Not covered yet: iterator-based `erase`, associative containers, algorithms. [S]
- Reported cost: Google measured about 0.3% average overhead and found over 1,000 bugs in production [S, via Sutter's March 2026 trip report and a secondary blog; not independently verified].
- Vendor switches available today (usable before C++26): libstdc++ `-D_GLIBCXX_ASSERTIONS` (on by default in unoptimized GCC 16.1 builds; at `-O2` set it yourself), `-fhardened` (GCC 14+); libc++ `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_{NONE,FAST,EXTENSIVE,DEBUG}` (FAST recommended for production; define before any include to avoid ODR trouble); MSVC STL `_MSVC_STL_HARDENING=1`. [V for libc++ and OpenSSF; S for others]
- `span::at` was added in C++26 (`__cpp_lib_span` 202311L). `operator[]` on `std::span` is unchecked in C++20/23 unless the library is hardened. [V]
- Contracts (P2900, C++26): `pre`, `post`, `contract_assert`; four evaluation semantics (`ignore`, `observe`, `enforce`, `quick-enforce`) chosen by the implementation, possibly different per evaluation; a violation handler `::handle_contract_violation`; predicates may be evaluated zero or more times, so they must be side-effect-free. [V, cppreference]. They stayed in C++26 over objections; the plenary vote was 114 in favor, 12 against, 3 abstaining, and Stroustrup said he would recommend not using them [S, devclass]. A February 2026 paper (P4009R0) argued for postponing them. Virtual-function support was adopted for the C++29 draft in June 2026 [S]. GCC 16 implements contracts; Clang 23.1's status page shows none; MSVC none listed [S].
- Recommendation: do not make contracts a LVL2 requirement. Allow `Expects`/`Ensures`-style project macros now, with a documented termination policy. Reconsider when two of the three major compilers implement `pre`/`post` and a project can choose the semantic by flag.
- Lifetime profile: not standardized. The committee is working on a type-safety profile (P3984) for C++29 [S]. Clang has a lifetime safety analysis you can turn on: `-Wlifetime-safety-permissive` (recommended starting point), `-Wlifetime-safety`, `-Wlifetime-safety-strict`, `-Wlifetime-safety-suggestions`; annotations `[[clang::lifetimebound]]`, `[[clang::noescape]]`, `[[gsl::Owner]]`, `[[gsl::Pointer]]`; intra-procedural, bug-finding, false positives possible, move semantics not tracked, invalidation checks "highly experimental". [V]
- Hardening is one layer: "C++26 hardening does not suddenly make C++ memory safe" [S, cppstories]. Keep sanitizers and static analysis.

---

## 4. STL preference versus performance and resource limits

### 4.1 When the standard library is unsuitable

- Freestanding implementations: only a subset is required. Fully required headers include `<cstddef>`, `<cstdint>`, `<limits>`, `<new>`, `<exception>`, `<typeinfo>`, `<initializer_list>`, `<compare>`, `<concepts>`, `<type_traits>`, `<ratio>`, `<utility>`, `<tuple>`, `<bit>`, `<atomic>`, `<coroutine>`, `<source_location>`, `<version>`. Partial: `<cstdlib>`, `<memory>`, `<functional>`, `<string>`, `<cstring>`, `<iterator>`, `<ranges>`, `<cmath>`, `<random>`, `<execution>`, `<charconv>`, `<system_error>`. C++26 adds more freestanding items (feature-test macros for `array`, `optional`, `variant`, `expected`, `mdspan`, `string_view`, `tuple`, `utility`, `algorithm`, and others). [V, cppreference freestanding page]. `vector`, `list`, `map`, `deque` will not be freestanding. The page says libc++ and MSVC STL do not support freestanding, and that libstdc++ had build issues before GCC 13 [S].
- No exceptions: STL types report errors by throwing (`bad_alloc`, `out_of_range` from `at()`, `bad_optional_access`). CG E.25 to E.27: if you cannot throw, simulate RAII, fail fast (`abort`), or use error codes systematically; E.28: avoid `errno`-style global state. Google and LLVM both build without exceptions [V for LLVM, S for Google]. With exceptions disabled, throw sites in libstdc++ abort [K]. Plan a "no-exceptions profile" that avoids `at()`, `value()`, and allocation failure recovery.
- No RTTI: LLVM does not use RTTI and uses its own `isa<>`/`cast<>` [V]. Google says avoid RTTI [S]. CG C.146 to C.148 govern `dynamic_cast`. Avoid `typeid`, `dynamic_cast`, and `std::any` in the profile.
- Heap restrictions and deterministic timing: avoid allocation on critical paths. CG Per.15 is a stub ("???") so LVL2 must state the rule itself. Preallocate (`reserve`), use fixed-capacity containers, avoid `std::function` (may allocate) and `std::shared_ptr` creation in loops [K].
- Hard real-time with a general-purpose allocator: the allocator and exceptions are the usual sources of unbounded latency [K].

### 4.2 Alternatives

- `std::array<T,N>`, `std::span`, `std::mdspan`: no heap; `span`/`mdspan` are views.
- `std::inplace_vector<T,N>` (C++26, `<inplace_vector>`, `__cpp_lib_inplace_vector` 202406L): fixed capacity, contiguous, elements constructed on insert. Over-capacity insertion throws `bad_alloc` per cppreference; `try_push_back`/`try_emplace_back` return `std::nullopt` instead of throwing; `unchecked_*` variants exist; constexpr for non-trivial types is a separate macro (202502L). cppreference lists Boost `static_vector`, EASTL `fixed_vector`, Folly `small_vector` as prior art. [V]. Implementation: GCC 16 library per the cppreference C++26 table; no Clang or MSVC entry in that table [S, the table may lag].
- `std::pmr` (C++17, `<memory_resource>`): `monotonic_buffer_resource` (can start on a stack buffer, frees all at once), `unsynchronized_pool_resource` / `synchronized_pool_resource`, `null_memory_resource()` (no allocation; use it to trap unexpected heap use), `new_delete_resource()`, `polymorphic_allocator`. [V]. Costs [K]: a virtual call per allocation, an extra pointer in each pmr container, pmr containers are different types from the default ones (`std::pmr::vector<T>` is not `std::vector<T>`), allocator propagation rules need care.
- ETL (Embedded Template Library, etlcpp.com): header-only, MIT, fixed-capacity containers sized at compile time, "the heap is never used", no STL dependency, no RTTI required, configurable error checking (asserts, exceptions, handlers, or none), compatible with C++03 and later, CI on C++11 to 23, docs show version 20.49.0. [S]
- EASTL (github.com/electronicarts/EASTL): EA's STL replacement, BSD-3-Clause, "emphasis on high performance above all other considerations", used by Frostbite, 483 commits, 78 open issues, 26 open PRs on the page I saw; activity level not verifiable from that page. Its allocator model differs from `std` [K]. Weak fit for scientific code unless there is a measured reason. [S]
- Project-local small containers (SmallVector-style, as in LLVM) when the STL's allocation behavior is the problem; LLVM prefers its `SmallVector` and `DenseMap` over `std::vector` and `std::map` [V].

### 4.3 Recommended rules

S1. Default: standard library, with the standard's own tools (`span`, `array`, `optional`, `expected`, `string_view`, ranges, `mdspan`).
S2. A deviation is recorded next to the code: reason (freestanding target, no heap, hard real-time, measured hot spot, interop), the replacement used, and the measurement or constraint. A benchmark alone justifies a replacement only with the build flags, input sizes, and hardware recorded (Per.6).
S3. Define named execution profiles and attach rules to each. Suggested minimal set: hosted (everything allowed), hosted-restricted (no exceptions, no RTTI, allocation only via named allocators, no iostream), freestanding (only the freestanding subset plus `inplace_vector`/ETL, no heap). Ask the custodian if these should map onto the project's existing execution-hardware material.
S4. In restricted profiles, fixed-capacity containers report overflow through a return value (`try_push_back`, `expected`) or fail fast, never silent truncation.
S5. Prefer `std::pmr` and fixed capacity over a global replacement of `operator new`; a replaced `operator new` affects the whole program.

---

## 5. Generic and header-only libraries

### 5.1 Benefits and costs

Benefits [K unless marked]: templates must be visible anyway; simple distribution (GSL and ETL are header-only [S]); inlining and constant propagation across the API; no ABI or link-order problems; easy to vendor.

Costs:
- Compile time: every translation unit reparses and reinstantiates. Clang's modules documentation states the theory that modules reduce cost from O(n*m) to O(n+m) but that the real benefit depends on optimization level [V].
- ODR: SF.2 says headers must not contain object definitions or non-inline function definitions ("Including entities subject to the one-definition rule leads to linkage errors"). Use `inline` / `constexpr` functions and `inline` variables. Google keeps header definitions to about 10 lines unless performance or technical reasons require otherwise, and requires ODR-safety via `inline` or templates [S]. SF.21: no unnamed namespace in a header; SF.7: no `using namespace` at global scope in a header; SF.11: headers are self-contained; SF.8: include guards.
- Binary size and code bloat: T.62 (put non-dependent members in a non-template base) and T.84 (non-template core for ABI stability) reduce duplication. T.61 warns against over-parameterization.
- Rebuild cost: changing a header recompiles all users.
- Macro leakage and include-order dependence.
- Tooling: clang-tidy only reports on headers matched by `HeaderFilterRegex` [K]; template bodies are checked only when instantiated, so tests must instantiate them.

Mitigations: explicit instantiation for the few types in use (`extern template`), precompiled headers, forward-declaration headers, IWYU, keeping template interfaces thin over non-template implementation, `-ftime-trace` (Clang) or `-ftime-report` (GCC) to find costly headers [K].

### 5.2 C++20 modules, October 2026

- CMake: docs for CMake 4.5.0-rc1 describe C++ modules support (added in 3.28) for Ninja, Ninja Multi-Config, Visual Studio 17 2022, and Visual Studio 18 2026 generators (Ninja 1.11+). Compilers: MSVC 14.34+, Clang 16+, clang-cl 19.1+ (added in 4.4), GCC 14+. `import std` is documented as supported in 4.5 (no longer behind an experimental gate on that page) for Clang 18.1.2+ with libc++ or libstdc++, MSVC 14.36+, GCC 15+ (not macOS; GCC 16+ on macOS), Ninja generators only, C++20 or newer. Header units are not supported with any generator. Ubuntu releases before 26.04 have broken `libstdc++.modules.json`. Module maps for imported targets are per-configuration, which the docs say is planned to improve. [V]
- Clang: modules are on with `-std=c++20`; Reduced BMI is the default as of Clang 22; header units are experimental; `import std` has two experimental routes; known issues include ODR-check false positives and misses, includes after imports only partly supported, ABI differences between module and non-module definitions, and "BMIs are not and should not be treated as an information hiding mechanism". [S]
- GCC: `-fmodules` is required (`-std=c++20` alone does not enable it); header units via `-fmodule-header`; the page lists limits (private module fragment errors, partition-definition visibility not implemented) and does not state the GCC version it describes. [S]
- cppreference C++23 table: `import std`/`std.compat` GCC 15, Clang 17 (partial), MSVC 19.35 (partial)/19.36. [S]
- NVCC: C++20 modules are listed as unsupported in the device-code tables. [V]
- Verdict: usable for pure-host projects on Ninja or Visual Studio with GCC 15+, Clang 18+, or MSVC 14.36+, and fragile for mixed CUDA, Makefile, or header-unit workflows. Header-only libraries remain the lowest-common-denominator interface. Do not make modules mandatory in LVL2.

### 5.3 When to prefer a compiled library

Prefer a compiled library when:
- the code is not a template, or is instantiated for a small closed set of types (typically `float`/`double`) so explicit instantiation in one `.cpp` removes duplicate compilation;
- compile time or binary size exceeds the project's budget;
- a stable ABI or plugin boundary is required (I.26, I.27);
- it holds process-global state, registries, or singletons (I.2, I.3 argue against them anyway);
- it wraps a vendor or system API (MPI, CUDA runtime, drivers, OS) so the vendor headers do not leak into every user;
- the implementation uses compiler flags or intrinsics different from the callers (for example per-ISA multiversioned kernels);
- the code must be closed-source or independently versioned.

Prefer header-only when the code is template-heavy, performance-critical across the call boundary, and instantiated by users with their own types (generic algorithms, small numeric kernels, containers, concepts, traits).

---

## 6. Interpretable template metaprogramming

### 6.1 Core Guidelines basis [V]

- T.120: use TMP only when you really need to ("hard to get right, slows down compilation, and is often very hard to maintain"; "Instead [of `enable_if`], use concepts"; if the result is a value, use a `constexpr` function).
- T.121: use TMP mainly to emulate concepts. T.122: use template aliases to compute types. T.123: use `constexpr` functions to compute values. T.124: prefer standard-library TMP facilities. T.125: beyond that, use an existing library.
- T.10 to T.13: constrain all template arguments; use standard concepts; prefer concept names over `auto` for locals; shorthand notation for simple concepts. T.20: concepts need meaningful semantics, not just syntax. T.21, T.22, T.26: complete operation sets, axioms, use-patterns. T.25: avoid complementary constraints. T.150: check that a class matches a concept with `static_assert`. T.47: avoid highly visible unconstrained templates with common names. T.69: do not make an unqualified non-member call inside a template unless you intend a customization point. T.144: do not specialize function templates. T.48: `enable_if` only if the compiler lacks concepts.

### 6.2 Concrete rules for LVL2

TMP-1. Constrain with concepts. No `std::enable_if` and no SFINAE expression tricks in new code. Put each reusable constraint in a named concept in a `concepts` header (T.10, T.11). Use standard concepts (`std::integral`, `std::floating_point`, `std::ranges::range`, `std::regular_invocable`, ...) before inventing one.
TMP-2. A concept expresses semantics, not only syntax. Its comment states the semantic requirement (T.20, T.22), for example "associative addition" or "strictly positive extent". `requires requires` does not appear in public interfaces; define a named concept. A requires-clause expression must be a primary expression (or `&&`/`||` of them) so wrap calls in parentheses [V, cppreference].
TMP-3. Avoid subsumption surprises. Atomic constraints are compared by source identity, so equivalent-looking constraints written separately do not subsume each other; `N > 0` does not subsume `N >= 0`. Build refined concepts by conjunction of named concepts. [V]
TMP-4. Compute values with `constexpr` functions; use `consteval` when the result must be a compile-time constant; use `if consteval` (C++23) for separate compile-time and run-time paths (T.123, F.4). `constexpr` does not force compile-time evaluation and should not be applied to everything (F.4 enforcement note).
TMP-5. Use `if constexpr` instead of tag dispatch and SFINAE overload sets where one function suffices. Limits: the condition must be value-dependent for discarding to occur in a template; discarded code must still be syntactically valid; use concepts when the signature must change. [V]
TMP-6. Use standard traits via `_v` and `_t` (T.124). A project trait is a noun-phrase or `is_`/`has_` name with `_v`/`_t` helpers, defined once, with `static_assert` tests of positive and negative cases right after it (T.150). Prefer a concept to a trait where the result is only a constraint.
TMP-7. `static_assert` with a message that names the violated requirement and the fix. Where a branch must never be instantiated, use a dependent-false helper (`dependent_false_v<T>`), or plain `static_assert(false, ...)` once CWG2518 is implemented by all matrix compilers. [V, cppreference notes the CWG2518 caveat]
TMP-8. No deep recursion. Use fold expressions, pack expansion, `std::index_sequence`, `constexpr` loops, C++26 pack indexing (`pack...[I]`, P2662; GCC 15, Clang 19 [V per cppreference/clang status]) and expansion statements (`template for`, P1306; GCC 16, Clang 23 partial [V]) instead of recursive instantiation. Recursion depth in any facility is bounded and the bound is documented. Compiler template-depth limits are finite (GCC and Clang defaults are on the order of 900 to 1024 [K]).
TMP-9. Each TMP facility has: a comment stating what it computes and why a function or concept was not enough; at least one worked example with expected result; `static_assert` tests in the same header or a paired test file. A reviewer should be able to verify the behavior without running the compiler on the template. As a rule of thumb for review, more than two levels of template-template parameters or nested trait computation need written justification (judgment, not sourced).
TMP-10. No TMP in public API signatures that a user must read to call the function: public signatures show constraints as named concepts so error messages point to them.
TMP-11. Keep expressions that need ADL customization explicit: qualify calls inside templates, or document the customization-point object (T.69).
TMP-12. Measure compile time of new TMP-heavy headers and record it in the PR (Per.6 applied to builds).

### 6.3 Error-message quality

- Concepts move the diagnostic to the call site and name the unsatisfied constraint. cppreference's example contrasts "50 lines of output" without concepts with "cannot call std::sort ... concept RandomAccessIterator<...> was not satisfied" with them. [V]
- Practices: keep atomic constraints small and named so the compiler names the failed one; put the most informative constraint first; test diagnostics with compile-fail tests (a unit that must not compile) and `static_assert(!concept<T>)` negative checks; use `static_assert` with a message when a constraint cannot express intent. No source I fetched measured diagnostics quality, so this paragraph is practice, not measurement.

### 6.4 C++26 static reflection (P2996)

- Adopted into C++26: reflection operator `^^`, splicer `[: :]`, opaque consteval-only `std::meta::info`, `<meta>` header, consteval metafunctions (`nonstatic_data_members_of`, `identifier_of`, `define_aggregate`, ...). Metafunctions signal errors by failing to be constant expressions until constexpr exceptions (P3068) are available. The paper itself calls this "a reduced initial set of features". Examples in the paper: enum to string, struct member iteration for command-line parsing, struct to tuple, `define_aggregate`. [S, P2996R13]
- Compiler status: GCC 16 with `-freflection`; Clang 23.1 status page shows "No" for P2996; MSVC, Intel, and NVCC show no support in the cppreference table. [S]
- Readability: it replaces macros, code generators, and recursive TMP for enum-to-string, serialization, and struct visitation with ordinary consteval code that reads like a normal function, which is a gain for human interpretation. The cost is new syntax, consteval-only values, and failures that show up as "not a constant expression". [judgment]
- Rules: (a) not required by LVL2 until every toolchain in a project's matrix supports it; (b) when used, confine it to named utility headers with `static_assert` tests, never in application logic; (c) guard with the feature-test macro (`__cpp_impl_reflection`, `__cpp_lib_reflection` [K, exact names unverified]); (d) no code injection beyond `define_aggregate`; (e) each use cites why a plain function or concept was insufficient.

---

## 7. "Latest C++ standard always"

### 7.1 Where the standards stand on 2026-10-22

- Published: C++23 = ISO/IEC 14882:2024, Edition 7, published 2024-10. The ISO page says it is "Expected to be replaced by ISO/IEC DIS 14882 within the coming months". [V]
- C++26 (working draft N5046, May 2026 [S]): feature-complete at Sofia (June 2025); national-body comments from the summer 2025 CD ballot (411 comments) resolved; technical work completed and approved at London Croydon on 2026-03-28; plenary vote 114 for, 12 against, 3 abstaining [S, Sutter, devclass].
- ISO status: DIS registered 2026-06-02; DIS ballot initiated 2026-07-31, 12 weeks, stage 40.20; the ISO page shows no closing date or publication date [V, iso.org/standard/91179.html]. A WG21 business plan dated 2026-07-28 (N5056) says the edition "is now in DIS ballot on schedule to be completed in 2026" and plans another revision in 2029 [V]. A community PR corrects an earlier claim that the ballot closes 27 September: the close is about 2026-10-23, inferred from 12 weeks and from a DIN listing; the ballot was still open on 10 October [S]. So as of today the DIS ballot has not closed and the standard is not published. Publication usually follows ballot approval and final editorial work; C++23 reached ISO publication in October 2024 [V] after technical completion in early 2023 [K], so a wait of months is plausible [inference]. The Wikipedia C++26 page is internally inconsistent on this (says "shipped" 28 March 2026 and also that the DIS "was not completed for ISO ballot" as of May); treat it as stale.
- C++29: schedule adopted; three-year cycle; June 2026 Brno meeting adopted a complete catalog of undefined behavior, contract pre/post for virtual functions, defaulted postfix increment, designated initializers for bases, `.lookup(key)` for associative containers; next meeting Búzios, Brazil, November 2026. [S]

C++26 headline contents [S]: static reflection; contracts; hardened standard library; erroneous behavior for uninitialized reads; `std::inplace_vector`; `std::execution`; `<hive>`, `<hazard_pointer>`, `<rcu>`, `<linalg>`, `<simd>`, `<text_encoding>`, `optional<T&>`, `copyable_function`, `submdspan`; expansion statements; pack indexing; `#embed`. Trivial relocatability was removed.

### 7.2 Compiler support

| Toolchain | Latest seen | C++23 | C++26 |
|---|---|---|---|
| GCC | 16.1 (2026-04-30), 16.2 (2026-08-07) [V]; 15.3 (2026-06-12), 14.4 (2026-06-26) | Features since GCC 11, "experimental" [S]; `import std` in 15 | `-std=c++26` since GCC 14 (experimental); GCC 16: reflection (`-freflection`), contracts, erroneous behavior, expansion statements, constexpr exceptions; `<inplace_vector>` library in 16; pack indexing in 15; default mode is C++20 since GCC 16 [S] |
| Clang | 23.1 (2026-08-25, "partial C++26 with -std=c++2c") [S]; 22 earlier | Most features Clang 13 to 20; gaps include extended floating-point types, `<cmath>` constexpr [S] | Pack indexing 19; expansion statements partial in 23; reflection, contracts, erroneous behavior, `#embed` "No" on the status page [S] (page may be a development snapshot) |
| MSVC | VS 2026 18.6 with MSVC Build Tools 14.51 (production), 14.52 and 14.53 previews [S] | STL "C++23 feature complete" in 14.52 Preview; `flat_map`/`flat_set` in 14.51 [S] | Some library items in 14.50/14.51; hardening partial (19.44/19.50) [S]; no language reflection or contracts listed |
| NVCC (CUDA 13.4.2 docs) | C++03 through C++23 selectable; C++23 from CUDA 13.3 [V] | Host compilers: GCC 14+, Clang 18+, nvc++ 24.3+; Visual Studio not supported for C++23. Device gaps: extended floating-point types, relaxed constexpr (P2448R2) [V] | None listed |
| Intel oneAPI DPC++/C++ | 2026.0 (2026-04-29), 2026.1 (2026-07-07), 2026.1.1 (2026-07-29), 2026.2 (2026-10-15) [S] | Follows its Clang front end: 2026.0 uses the Clang 22 front end; basis for later releases not stated [S] | Whatever Clang 22 provides (no reflection, no contracts) |

Other style guides sit below the newest standard on purpose: Google targets C++20 ("should not use C++23 features") [S]; LLVM uses C++17 [V]; the gist uses C++23 [S].

### 7.3 How to express "latest"

A literal "always the latest standard" means `-std=c++2c` today, which fails for NVCC, is partial in Clang, absent in MSVC for core features, and experimental in GCC. Recommended wording for LVL2:

- "Each project targets the newest ISO-published C++ standard that every compiler in its declared support matrix supports completely. A newer feature may be used earlier when it is gated by its feature-test macro and every compiler in the matrix provides it."
- Record the target and the matrix in the project constitution. Set it in build files with `target_compile_features(... cxx_std_23)` or `CXX_STANDARD`, `CXX_STANDARD_REQUIRED ON`, `CXX_EXTENSIONS OFF`.
- Review trigger: each major GCC, Clang, MSVC, CUDA, and oneAPI release; publication of C++26 by ISO; or a waiver recorded with an expiry.
- Different targets for different translation units are allowed where the toolchain forces it (for example `.cu` files at C++23, host-only files at C++26). Record the split and keep shared headers compilable at the lower level.
- Today's answer for most projects: C++23. Host-only GCC 16 projects may adopt individual C++26 features (contracts, reflection, `inplace_vector`) behind macros if the custodian wants early adoption.

---

## 8. Naming conventions

### 8.1 What the sources say

- CG NL.8: use a consistent naming style; choose a house style and leave imported libraries in their original style. NL.10: prefer `underscore_style` names; "This rule is a default to use only if you have a choice. ... The need for consistency beats personal taste." NL.8 lists three examples: ISO Standard (lowercase and underscores), Stroustrup's variant (standard style with an upper-case initial for your own types and concepts, e.g. `My_map`), and CamelCase (`MyMap`, `myMap`). NL.9: ALL_CAPS for macros only. NL.5: do not encode type in names. NL.7: name length proportional to scope. Avoid `__` and leading underscore plus capital (reserved). GSL names are standard-library style (lowercase with underscores). [V]
- The C++ standard library uses snake_case for types, functions, variables, and (since P1754R1) concepts. P1851R0 gives concept naming rules: snake_case with no prefix or suffix, adjective names for single-capability concepts (`swappable`, `copy_constructible`), noun names for abstractions (`forward_iterator`), trailing preposition for multi-argument constraint concepts (`swappable_with`, `sentinel_for`), `any_<concept>` for type-erased wrappers. [V]
- Google style: CamelCase types, snake_case variables, and an exception allowing STL-style naming for entities analogous to existing C or C++ entities [K; I could not get the Naming section through the fetcher, and direct download was refused by the egress proxy, which I did not circumvent].
- LLVM: types CamelCase, functions camelBack, variables CamelCase; STL-mimicking classes may use STL-style lowercase names [V].
- C++ Best Practices (Jason Turner): use descriptive names; types UpperCamelCase and functions lowerCamelCase in its own recommendation, but "follow the standard library's conventions where they apply", and consistency over specific scheme [S].
- Boost uses all-lowercase with underscores [K]; I could not fetch Boost's guidance (client error).

### 8.2 How the custodian's convention compares

The custodian's rule (snake_case variables and functions; CamelCase classes and structs; snake_case for classes meant to be used like or adapt to an STL feature) matches the practice of LLVM's allowance, Google's analogous-entity exception (from memory), and NL.8 (house style, imported libraries unchanged). It is compatible with CG as long as it is written down and applied consistently. It differs from the gist (snake_case for all types) and from NL.10's default.

### 8.3 Suggested operational test for "STL-like"

A type is STL-like, and snake_case, if any of these hold:
1. It models or extends a standard container, iterator, sentinel, range/view, allocator, memory resource, smart pointer, function-object/callable wrapper, or `std::` utility vocabulary type (`optional`, `variant`, `span`-like), meant to be dropped into standard algorithms or `std::` templates.
2. It is a type trait or metafunction (`is_foo`, `foo_t`, `foo_v` helpers) or a tag type used with standard facilities.
3. It is a concept (follow P1851R0 conventions).
Everything else, including domain objects (`Mesh`, `NeutronPopulation`, `LinearSolver`), service/config classes, and application structs, is CamelCase. If a type needs both snake_case members like `value_type`, `iterator`, `begin()` and domain meaning, it is STL-like.

### 8.4 Gaps in the custodian's convention (see open questions)

Not stated: enumerators, constants (`constexpr` variables), template parameters, type aliases, namespaces, macros, file names, member data suffix or prefix, concept names, test names, and acronym casing. Candidate defaults taken from CG and the standard: namespaces snake_case; macros ALL_CAPS with a project prefix (NL.9, ES.31); template parameters CamelCase (`Value`, `Allocator`) or single capital (`T`) as in the standard wording; concepts snake_case; constants snake_case; enumerators snake_case with `enum class` (Enum.3); files snake_case; data members with trailing `_` for private data if the custodian likes the gist's rule.

### 8.5 Enforcement

`clang-tidy` `readability-identifier-naming` has per-kind options: ClassCase, StructCase, ConceptCase, FunctionCase, VariableCase, ConstexprVariableCase, MemberSuffix, TemplateParameterCase, NamespaceCase, EnumCase/EnumConstantCase, MacroDefinitionCase, TypeAliasCase and more (the page excerpt I saw confirmed Class, Concept, Constant, Constexpr, Enum, Function, Global, Local, Macro, Member kinds; the others I recall [K]). Case styles: lower_case, UPPER_CASE, camelBack, CamelCase, camel_Snake_Back, Camel_Snake_Case, aNy_CasE, Leading_upper_snake_case. Each kind has `IgnoredRegexp`, `Prefix`, `Suffix`, `HungarianPrefix`. [V]
The check cannot know "STL-like". Options: (a) accept both cases for class names with `ClassIgnoredRegexp: '^[a-z][a-z0-9_]*$'` and rely on review for the semantic test; (b) place STL-like types in a designated namespace or directory with its own `.clang-tidy`; (c) require an annotation comment. I did not test any of these. Concept names and trait names are easy to enforce as snake_case.

---

## 9. Mechanical enforcement

### 9.1 Formatting

- `clang-format` with a committed `.clang-format` (generate with `clang-format -style=llvm -dump-config > .clang-format` then edit; set `BasedOnStyle`); CI check `--dry-run --Werror` (the page documents both flags; using them together in CI is my inference); `git-clang-format` formats only touched lines and can be driven by git config. Pin the clang-format version in CI because output differs between versions [K]. [V]

### 9.2 clang-tidy

- Commit `.clang-tidy`; run via `compile_commands.json`; `HeaderFilterRegex` must cover project headers or header-only code goes unchecked [K]. Instantiate templates in tests so their bodies are analyzed [K].
- Suggested starting set: `cppcoreguidelines-*` minus the noisy ones the custodian rejects (examples that often need tuning: `avoid-magic-numbers`, `non-private-member-variables-in-classes` for plain structs, `pro-bounds-constant-array-index`, `avoid-c-arrays` in C interop layers) [judgment], plus `bugprone-*`, `performance-*`, `modernize-*` (selected), `readability-identifier-naming`, `concurrency-*`, `misc-*`, and `clang-analyzer-*`. `cert-*` is an option for safety-critical projects.
- Pin the clang-tidy version; check options and names against that release's docs (the docs I read are for 24.0.0git).
- Rules to map explicitly to checks: I.11/R.3 → `owning-memory`; Bounds → `pro-bounds-*`; R.10 → `no-malloc`; ES.20 → `init-variables`; ES.46 → `narrowing-conversions`; C.21 → `special-member-functions`; ES.31 → `macro-usage`; I.2 → `avoid-non-const-global-variables`; ES.48/ES.49 → `pro-type-*cast`. Lifetime and many T. rules have no check.

### 9.3 include-what-you-use

- Uses Clang to propose adding and removing `#include`s. Release branches match Clang versions (IWYU 0.26 ↔ Clang 22; `master` tracks Clang main). Run through CMake with `CMAKE_CXX_INCLUDE_WHAT_YOU_USE`; pragmas `// IWYU pragma: keep`, `private, include "..."`; mapping files for third-party libraries. It describes itself as experimental, written for Google's tree, and with limited new features; the page does not discuss templates or header-only libraries. [S]
- Recommendation: advisory in CI, not gating, until trial results on the project's header-only code are known (judgment).

### 9.4 Sanitizers [V unless marked]

- ASan and UBSan in one job: `-fsanitize=address,undefined` with `-fno-omit-frame-pointer -g` [K]. UBSan check groups, `-fsanitize-trap` (trap instead of runtime), `-fsanitize-minimal-runtime` (small runtime, no `vptr` check) are documented; some checks are outside the `undefined` group (`float-divide-by-zero`, `unsigned-integer-overflow`, `implicit-conversion`, `local-bounds`, `nullability`), which matter for numerical code.
- TSan: `-fsanitize=thread -O1 -g`; 5x to 15x slowdown and 5x to 10x memory; whole program should be instrumented; no static libc/libstdc++ linking; Linux/Darwin/FreeBSD/NetBSD, 64-bit only; "beta", not for production. Run as its own job; it does not combine with ASan [K]. 
- MSan (clang, needs an instrumented standard library) for uninitialized reads, optional [K].
- `_FORTIFY_SOURCE` is incompatible with sanitizer builds (OpenSSF).
- MPI and CUDA: sanitizers on host code only; device code needs `compute-sanitizer` [K].

### 9.5 Warnings

- OpenSSF compiler-options hardening guide [V]: `-Wall -Wextra`, `-Wformat -Wformat=2`, `-Wconversion -Wsign-conversion` (staged rollout), `-Wimplicit-fallthrough`, `-Werror=format-security`; "`-Werror`: blanket form for development only. Don't use it when distributing source." Runtime: `-D_FORTIFY_SOURCE=3` (needs `-O1`+), `-D_GLIBCXX_ASSERTIONS`, `-fstack-protector-strong`, `-fstack-clash-protection`, `-fhardened` (GCC 14+), `-ftrivial-auto-var-init=zero`, `-fno-delete-null-pointer-checks`, `-fno-strict-overflow -fno-strict-aliasing` for production, libc++ hardening modes.
- Additional warnings often used for C++ [K]: `-Wpedantic -Wshadow -Wnon-virtual-dtor -Woverloaded-virtual -Wold-style-cast -Wcast-align -Wnull-dereference -Wdouble-promotion -Wfloat-conversion`. MSVC: `/W4 /permissive- /WX /analyze`.
- Rule: warnings as errors in the project's own CI and developer builds; never in INTERFACE or install flags consumed by other projects, which matters for header-only libraries; treat third-party headers as system headers (`-isystem` / `SYSTEM` includes) so their warnings do not fail the build.
- Scientific-code additions [K]: avoid `-ffast-math`; decide `-ffp-contract` and `-march` policy for reproducibility; `-Wfloat-equal` only where it helps.

### 9.6 Static analyzers

- Clang Static Analyzer via `clang-analyzer-*` checks in clang-tidy; MSVC `/analyze` with C++ Core Check; Clang lifetime safety flags (section 3.9); cppcheck, GCC `-fanalyzer` (limited for C++ [K]), CodeQL, Coverity as options [K, not fetched]. For safety-related instrumentation software, MISRA C++:2023 or SEI CERT C++ checkers may be required by outside standards [K]; not researched here (see the high-assurance note in this folder if present).

### 9.7 CI layout suggestion

One job per: format check; build with warnings as errors on each compiler in the matrix; clang-tidy; ASan+UBSan tests; TSan tests (if threaded); hardened-library build and tests (`_GLIBCXX_ASSERTIONS`, libc++ FAST or EXTENSIVE, `_MSVC_STL_HARDENING`); lifetime-safety warnings (Clang); IWYU (advisory). Record compiler and tool versions in the repository.

---

## 10. Open questions for the custodian

1. Language level: accept the "newest standard fully supported by the project's toolchain matrix" wording (section 7.3), or require `-std=c++2c` where available? Should CUDA translation units be allowed a lower level than host code?
2. Pin the Core Guidelines to a commit or date (the document is dated 2026-06-14, "release 0.8")? Which rule subset is mandatory, which advisory, which waived?
3. Exceptions: allowed, banned, or per execution profile? If banned, is `std::expected` the standard error channel (the gist uses a custom `result<T>`)?
4. `auto`: follow ES.11 or the gist's "explicit types in agent-written code"?
5. `#pragma once` or include guards (SF.8)?
6. Raw pointers: adopt rules D1 to D11? Provide a project `owner`/`not_null` or depend on Microsoft GSL?
7. Contracts and hardening: require hardened-library builds in CI and production? Adopt `Expects`/`Ensures`-style macros now, or wait for compiler support of C++26 contracts?
8. STL exemptions: which approvals and what evidence (benchmarks, hardware, flags)? Which third-party libraries from the gist's table, if any, are pre-approved?
9. Execution profiles: hosted, hosted-restricted, freestanding. Which deliverables use which, and does `std::pmr` or ETL fit the instrumentation targets?
10. Header-only default vs compiled: acceptable compile-time budget per translation unit? Appetite for module wrappers?
11. TMP: is a hard limit on recursion depth and template-template nesting wanted, or review judgment? Should reflection be allowed once GCC, Clang, and MSVC all ship it?
12. Naming: confirm the "STL-like" test (8.3) and fill in enumerators, constants, template parameters, concepts (snake_case recommended), namespaces, macros, files, member data suffix, acronym casing. Are short math names (`x`, `dt`, `n`) allowed in small scopes (NL.7) or does the gist's three-letter rule apply?
13. Floating-point policy: `-march=native`, `-ffast-math`, FMA contraction, reproducibility across hosts. CG gives no guidance; where should LVL2 put it (this standard, `numerical-computation`, or build rules)?
14. Sanitizer and static-analysis gate: which checks block merges vs advisory? Is Clang required in CI even for GCC/MSVC-primary projects?
15. Comment conventions for agent-written vs human-written code (gist) are outside CG. Adopt, or leave to the crew standards?
16. MPI and CUDA: confirm that wrapper layers (D4 spans, typed device pointers) are required, and which MPI/CUDA versions to support.

---

## 11. Sources (all accessed 2026-10-22)

Core Guidelines and GSL
- https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines (rendered, 109,052 characters as delivered)
- https://raw.githubusercontent.com/isocpp/CppCoreGuidelines/master/CppCoreGuidelines.md (841,419 bytes; read locally)
- https://github.com/isocpp/CppCoreGuidelines
- https://github.com/microsoft/GSL
- https://herbsutter.com/2013/05/29/gotw-89-solution-smart-pointers/
- https://herbsutter.com/2013/06/05/gotw-91-solution-smart-pointer-parameters/

The gist
- https://gist.github.com/b7r6/5dde648f5dc1dea1e9039f2211f5d40a (summaries only)

Enforcement
- https://clang.llvm.org/extra/clang-tidy/checks/list.html
- https://clang.llvm.org/extra/clang-tidy/checks/cppcoreguidelines/owning-memory.html
- https://clang.llvm.org/extra/clang-tidy/checks/cppcoreguidelines/pro-bounds-avoid-unchecked-container-access.html
- https://clang.llvm.org/extra/clang-tidy/checks/readability/identifier-naming.html
- https://learn.microsoft.com/en-us/cpp/code-quality/using-the-cpp-core-guidelines-checkers
- https://clang.llvm.org/docs/ClangFormat.html
- https://github.com/include-what-you-use/include-what-you-use
- https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
- https://clang.llvm.org/docs/ThreadSanitizer.html
- https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html
- https://clang.llvm.org/docs/LifetimeSafety.html
- https://libcxx.llvm.org/Hardening.html
- https://cppstories.com/2026/hardening-experiments
- https://www.sandordargo.com/blog/2026/05/13/cpp26-library-hardening

Standard status and compilers
- https://en.wikipedia.org/wiki/C%2B%2B26 (internally inconsistent; low weight)
- https://herbsutter.com/2026/03/29/c26-is-done-trip-report-march-2026-iso-c-standards-meeting-london-croydon-uk/
- https://www.devclass.com/development/2026/04/01/contracts-are-in-c26-despite-disquiet-over-their-value/5213555
- https://minifeed.net/items/8GtDK8g0flqv (June 2026 Brno, excerpt)
- https://minifeed.net/items/LQBwigWHUuxZ (March 2026 London, excerpt)
- https://shape-of-code.com/2026/08/09/2026-in-the-programming-language-standards-world/
- https://www.iso.org/standard/91179.html (ISO/IEC DIS 14882, stage 40.20)
- https://www.iso.org/standard/83626.html (ISO/IEC 14882:2024)
- https://github.com/wrocpp/wrocpp.github.io/pull/182 (ballot dates; secondary)
- https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5056.pdf (WG21 convenor's report, 2026-07-28)
- https://isocpp.org/files/papers/P1000R6.pdf
- https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4009r0 (contracts concerns)
- https://isocpp.org/files/papers/P2996R13.html
- https://gcc.gnu.org/projects/cxx-status.html ; https://gcc.gnu.org/releases.html
- https://clang.llvm.org/cxx_status.html ; https://phoronix.com/news/LLVM-23.1-Released
- https://github.com/microsoft/STL/wiki/Changelog
- https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cpp-language-support.html
- https://www.intel.com/content/www/us/en/developer/articles/release-notes/oneapi-dpcpp/2026.html
- https://en.cppreference.com/w/cpp/compiler_support/26.html ; https://en.cppreference.com/w/cpp/compiler_support/23.html

Library and language references
- https://en.cppreference.com/w/cpp/freestanding.html
- https://en.cppreference.com/w/cpp/container/inplace_vector.html
- https://en.cppreference.com/w/cpp/header/memory_resource.html
- https://en.cppreference.com/w/cpp/container/span.html
- https://en.cppreference.com/w/cpp/memory/start_lifetime_as.html
- https://en.cppreference.com/w/cpp/language/cv.html
- https://en.cppreference.com/w/cpp/language/constraints.html
- https://en.cppreference.com/w/cpp/language/if.html
- https://en.cppreference.com/cpp/language/contracts
- https://en.cppreference.com/w/cpp/experimental/observer_ptr.html
- https://www.etlcpp.com/docs/
- https://github.com/electronicarts/EASTL
- https://clang.llvm.org/docs/StandardCPlusPlusModules.html
- https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Modules.html
- https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html
- https://www.kitware.com/import-cmake-the-experiment-is-over/ (2023; superseded)
- https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node458.htm ; .../node501.htm
- https://nvidia.github.io/cccl/libcudacxx/

Style guides
- https://google.github.io/styleguide/cppguide.html (Naming section not retrievable through the fetcher)
- https://llvm.org/docs/CodingStandards.html
- https://github.com/lefticus/cppbestpractices/blob/master/03-Style.md
- https://open-std.org/JTC1/SC22/WG21/docs/papers/2019/p1851r0.html

---

## 12. Network log

Approximate sizes are page text lengths reported by the fetch tool or bytes from curl; "n/r" = not reported. Total traffic is a few MB, far below the 10,000 item / 10,000 MB limits (about 110 requests including searches).

| # | URL / query | Result | Size |
|---|---|---|---|
| 1 | gist.github.com/b7r6/5dde6... (2 fetches) | OK, summaries only | ~55 KB page text claimed |
| 2 | github.com/isocpp/CppCoreGuidelines | OK, commit dates blank | n/r |
| 3 | isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines (3 fetches, offsets 0 and 100000) | OK, truncated by tool | 109,052 chars |
| 4 | raw.githubusercontent.com/.../CppCoreGuidelines.md (curl) | OK, HTTP 200 | 841,419 bytes |
| 5 | `gh api` repos/isocpp/CppCoreGuidelines (commits, repo), microsoft/GSL (releases, contents) | FAILED 403, repository access not enabled; not retried | 0 |
| 6 | github.com/isocpp/CppCoreGuidelines/commits/master | FAILED (robots_disallowed) | 0 |
| 7 | github.com/microsoft/GSL | OK | n/r |
| 8 | clang.llvm.org/extra/clang-tidy/checks/list.html | OK | 100,434 chars |
| 9 | clang-tidy owning-memory; pro-bounds-avoid-unchecked-container-access; identifier-naming | OK (3) | n/r |
| 10 | learn.microsoft.com .../using-the-cpp-core-guidelines-checkers | OK | n/r |
| 11 | herbsutter.com GotW 89, GotW 91 | OK (2) | n/r |
| 12 | WebSearch: C++26 published status / Sutter trip report / DIS ballot (3 queries) / ISO/IEC 14882:2026 | OK | n/a |
| 13 | en.wikipedia.org/wiki/C%2B%2B26 | OK, inconsistent | n/r |
| 14 | minifeed.net Brno (8GtDK8g0flqv), London (LQBwigWHUuxZ) | OK, excerpts only | small |
| 15 | iso.org/standard/91251.html | OK but unrelated (ISO/IEC 25706:2026) | small |
| 16 | shape-of-code.com 2026 post | OK (ballot close 27 Sept claim, later disputed) | n/r |
| 17 | devclass.com contracts article | OK | n/r |
| 18 | herbsutter.com/2026/03/29/... trip report | OK | n/r |
| 19 | open-std.org .../2026/n5056.pdf | OK | n/r |
| 20 | iso.org/standard/91179.html (DIS 14882); iso.org/standard/83626.html (14882:2024) | OK (2) | small |
| 21 | github.com/wrocpp/wrocpp.github.io/pull/182 | OK | small |
| 22 | isocpp.org/files/papers/P1000R6.pdf; open-std P4009R0; isocpp.org P2996R13.html | OK (3) | P2996R13 107,618 chars |
| 23 | WebSearch (contracts semantics; observer_ptr x2; MPI; lifetime; MMIO; LLVM 23.1; snake_case; Google naming; intel icpx; modules; hardening; nvcc) | OK; one query with `allowed_domains` rejected by the search proxy (HTTP 400) | n/a |
| 24 | cppreference: compiler_support/26 (117,249 chars), compiler_support/23, freestanding, inplace_vector, memory_resource, span, start_lifetime_as, cv, constraints, if, contracts, observer_ptr | OK (12) | n/r |
| 25 | cppreference .../language/reflection.html | FAILED (client_error) | 0 |
| 26 | gcc.gnu.org/projects/cxx-status.html | OK | 140,231 chars |
| 27 | gcc.gnu.org/releases.html; gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Modules.html | OK (2) | n/r |
| 28 | clang.llvm.org/cxx_status.html; Clang modules doc; LifetimeSafety; UBSan; TSan; ClangFormat | OK (6) | modules doc 100,721 chars |
| 29 | releases.llvm.org | OK, no version list | small |
| 30 | phoronix.com/news/LLVM-23.1-Released | OK | small |
| 31 | github.com/microsoft/STL/wiki/Changelog | OK | n/r |
| 32 | docs.nvidia.com CUDA programming guide C++ language support | OK, truncated | 110,176 chars |
| 33 | intel.com article c-standard-support-in-intel-oneapi-dpcpp-compiler | FAILED (client_error) | 0 |
| 34 | intel.com docs 2026-0 standards-conformance | OK but TOC only, no content | small |
| 35 | intel.com release notes oneapi-dpcpp/2026 | OK | n/r |
| 36 | cmake.org cmake-cxxmodules latest; manpages.debian.org cmake-cxxmodules (older); kitware.com import-cmake (2023) | OK (3) | n/r |
| 37 | etlcpp.com (redirect), etlcpp.com/docs/; github.com/electronicarts/EASTL | OK (3) | n/r |
| 38 | libcxx.llvm.org/Hardening.html; sandordargo.com hardening (2 fetches); cppstories.com hardening | OK (4) | n/r |
| 39 | best.openssf.org compiler options guide | OK, truncated | 114,789 chars |
| 40 | google.github.io/styleguide/cppguide.html (3 fetches, offsets 0, 100000, 110000) | OK, Naming section not delivered | 124,758 chars |
| 41 | curl google.github.io/styleguide/cppguide.html | FAILED, egress proxy 403 (host not allowed); not circumvented, no mirror used | 0 |
| 42 | boost.org libraries.htm | OK, no naming info | small |
| 43 | boost.org contributor-guide naming.html | FAILED (client_error) | 0 |
| 44 | llvm.org/docs/CodingStandards.html | OK | 102,243 chars |
| 45 | open-std P1851R0; lefticus cppbestpractices 03-Style | OK (2) | n/r |
| 46 | github.com/include-what-you-use/include-what-you-use | OK | n/r |
| 47 | mpi-forum.org MPI-5.0 node458, node501 | OK (2) | n/r |
| 48 | nvidia.github.io/cccl/libcudacxx/ | OK, limited | small |
| 49 | Bash (first attempt): read proxy README and proxy status endpoint | DENIED by the permission classifier; I did not retry or work around | 0 |

No paywalled pages were retrieved and no mirrors, archives, or caches of blocked pages were used. Search-result pages I did not fetch (for example the Boost mailing list thread on observer_ptr, the BYU copy of an old Google style PDF, N3840/N4282) are cited only as "search result" in the text.
