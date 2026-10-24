Role: research agent (build systems, for a planned LVL2 standard BUILD). Accessed 2026-10-24. Retrieval: about 64 requests (53 page and file fetches, of which 9 returned HTTP 429 and 1 returned 404; 10 searches), roughly 12 MB of text and PDF, far inside 1,500 items and 1,500 MB. Rules followed: read-only retrieval; no paywalls circumvented; no mirrors, caches, or archives; no workaround after a failed fetch; retrieved text treated as data (none of it contained instructions); primary sources preferred; unconfirmed items marked [unverified].

# Build systems: hazards and outcome-level practices for a tool-agnostic, timeless standard

**Method caveat.** Most pages came through a fetch tool that returns a model-written extract of the page, not its text. Quotes marked as such below are the extract's quotation of the page, and I could not check them against the page itself. Five PDFs the tool could not read were saved and converted with a text extractor, so I read them in full: Bezemer et al. 2017 (S20), Lyu et al. 2024 (S21), Miller 1998 (S22), Bentley et al. 2018 (S28), and Hilton et al. 2016 (S31, skimmed). The GNU Make and Autoconf manuals returned HTTP 429 on every attempt, including after a pause, so I did not read them and did not seek a copy elsewhere; what I say of them rests on a search extract (S8) and my own knowledge, marked [unverified]. Search extracts are secondary. CMake, the Autotools, and Make are evidence here, not subjects: each hazard is stated so that it holds under any tool.

## Answer in brief

1. Every input that can change an output is a declared prerequisite of it: the generator of a generated file, the compiler and flags, the headers a source reads. An undeclared input gives an incremental build that is wrong without an error, and a parallel build that races (S20, S22, S21).
2. A build wrong only in parallel or incrementally has a defect in its declarations, not in the scheduler. The check compares clean with incremental and serial with parallel builds, within the declared tolerance (S20, S22).
3. Header and other discovered dependencies come from the tool that reads the file, not from a hand-kept list, which drifts (S20, S21, S23).
4. A change of flags, compiler, or configuration rebuilds what it affects; the command line is an input of each output (S23, S26).
5. Builds run out of source; the source tree is not written, and several configurations of one tree coexist (S12, S18).
6. Configuration is decided at a stated time and its result is recorded. A detected property that changes results is required or recorded as absent, and is overridable. Detection by running a program is impossible in a cross build, so such a property has a declared value or a non-running test (S8 [unverified], S9, S23).
7. The toolchain is named, not found by chance: compilers, linker, libraries, sysroot, build host, run host, and build-host generators are inputs of the result (S9; STND.DEPS.8).
8. A flag that changes results (optimization, contraction, fast-math, finiteness assumptions, precision of intermediates, assertion removal, bounds checks) is set in one place per unit and recorded. Defaults differ by compiler and language mode, so an unstated flag is not a known one (S5, S13, S28).
9. A flag set at link time can change process-wide floating-point state for every library in the process (S5, S13).
10. A check of untrusted input is not removed by a build type (S10; STND.CODE.6).
11. Warnings are errors in the checks of a change; they are not errors by default in a release that others build with compilers the project has not seen (S25, S13).
12. Reproducibility is relative to the stated source, environment, and instructions; the project states what the environment holds (S1, S1b).
13. Time enters a build through one channel, an instant taken from the source revision, not the clock (S2).
14. Order does not come from the file system or the locale; inputs to an order-sensitive step are sorted by a fixed rule (S4, S7).
15. The build path is either fixed as part of the environment or removed from outputs by a prefix map, and the record says which (S3, S5b).
16. No network is used inside the build step. A fetch is a separate, pinned, digest-checked step before it, and a missing input stops the build (S3b, S17, S18; STND.DEPS.6).
17. A release is built from the revision it names; files in a release archive and not in the repository, such as generated configuration scripts, come from a recorded step or are compared with its output (S16).
18. A generated source has its generator and inputs as prerequisites, is regenerated or checked for currency, and is not edited by hand (S20 5.1, S17).
19. A cache hit gives the result of running the step: the key holds every input; only trusted builds write; a poisoned cache is discarded whole (S18b, S19, S26).
20. Debug, release, and checking builds (sanitizers, race detection) are named configurations with recorded settings; a result is reported from the configuration it was measured in (S10b, S11).
21. A build for several accelerator architectures records each real target and each load-time-compiled target; a mismatch with the installed device is found at build or start (S24, S9d; STND.OFFLD.24).
22. The build record lets a result be traced to its revision, configuration, toolchain, flags, environment, resolved dependencies with digests, host, and output digests, and the build writes it (S6, S19; REPRO.4).
23. A continuous-integration matrix lists the axes that change results and the combinations not run (S29; STND.PY.14).

## 1. Declared dependencies and the hazards of undeclared ones

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Unspecified (undeclared) dependency | A dependency that exists in what the build does and not in what the build declares. Bezemer et al. found more than 1.2 million such dependencies, in six root causes, in four mature projects (GLib, OpenLDAP, Linux, Qt). They give two consequences: an incremental build omits commands that are needed, so changes "will not be completely reflected in the deliverables"; a parallel build runs in an order the declarations do not fix (S20 §1) | Wrong outputs with no error. The failures show only in testing, "at which time the link to incorrect build specifications is hard to make" | The declared graph is checked against the graph the build exercises; a difference is a defect | S20, S21 | Holds for any build tool that schedules from a declared graph |
| Missing generator dependency | A target depends on generated code but not on the generator. In GLib 21 cases, so a changed generator does not rebuild the output "built and shipped using outdated contents" (S20 §5.1) | Stale generated source shipped | The generator is a prerequisite of what it generates | S20 | General |
| Race in a parallel build | In the Linux kernel case Bezemer cites, one target consumed another that no rule declared, so the first was invalid "at random times, depending on the execution order" under parallel build (S20 §1). Miller: "Incomplete Makefiles are wrong Makefiles" (S22 §4) | Intermittent failure; a result that depends on the schedule | A true race in a build is a defect of the declarations (STND.VVUQ.82 sense). Serial and parallel builds are compared | S20, S22 | General |
| Prevalence | Lyu et al. cite that 52.68% of build errors in C projects are dependency-related (from Seo et al.), and call missing and redundant dependencies "the most prevalent" build script errors (S21). Seo et al. studied 26.6 million builds at one company, found about one third failing, and found dependency errors the leading kind (S27 search extract) | Wasted time and a loss of trust in the build | The build is checked for missing and redundant declarations as a routine | S20, S21, S27 | The figures are of C and C++ and Java at specific organizations and times; the kind of failure is general |

## 2. Out-of-source builds

- A build tree apart from the source tree keeps the source tree "pristine"; CMake's manual calls an in-source build "supported, but discouraged" (S12 extract). Bazel lists "writing to the source tree during the build, which can make later builds of other targets fail" as non-hermetic (S18 extract). The Autotools' separate-directory (VPATH) build: manual not read [unverified].
- Outcome: two configurations (release, checking, a second target) build from one source tree without cleaning; deleting a build tree is the way to clean; the source tree stays a faithful copy of the revision that REPRO.1 names. An out-of-source build puts the build path into outputs unless it is mapped (section 6).

## 3. Configuration detected at build time versus declared, and its record

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Detection result varies with the machine | Configure-time tests find libraries, headers, and features of the machine, so the same source yields different builds on different hosts. Ninja's design excludes such decisions from the build step: it "is intended to be used with a separate program generating its input files", since "making decisions is slow" (S23 extract) | The build depends on what happens to be installed; a silent feature loss when a library is missing | The result of each detection is stored in the build record, and a detected property that changes the result is either required (stop if missing) or recorded as absent | S23, S19 | General |

## 4. Toolchain selection and cross-compilation

- Three roles: the machine that builds, the machine the result runs on, and, for a compiler build, the machine its output targets (S8 [unverified]). A standard need not use the Autotools' names.
- CMake's toolchain document: the toolchain file is loaded early to set the compilers, a variable marks a cross build, and source and binary directory variables should not be used in it since it is read in contexts where they differ (S9 extract). Lesson: a toolchain description is a self-contained input that does not depend on where the build runs.
- STND.DEPS.8 already makes each compiler's revision an input. A cross build adds the target libraries and headers (sysroot) and the build-host tools that run during the build and generate code; the latter are a separate set from target code, or a generator is compiled for the wrong machine.

## 5. Flags that change results, and where they are set

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Contraction default differs by mode | GCC: "-ffp-contract=off for C in a standards compliant mode ... -ffp-contract=fast otherwise" (S5 extract). Clang: `fast` is the default for CUDA, `fast-honor-pragmas` for HIP, `on` for other languages (S13 extract) | The same source gives different roundings under a different language mode or compiler | The contraction mode is stated per unit (corpus STND.CXX.4 does for C++) and, for device code, per device language | S5, S13 | The defaults are specific to compilers and change; the dependence on mode is the lasting fact |
| Fast-math bundle | GCC: the fast-math option sets several options (no math errno, unsafe math optimizations, finite-math-only, no rounding math, no signaling NaNs, limited complex range, fast excess precision) and defines a macro; it is not on at any level except the "fast" one, "since it can result in incorrect output for programs that depend on an exact implementation of IEEE or ISO rules" (S5 extract). Finite-math-only allows optimizations that "assume that arguments and results are not NaNs or +-Infs" (S5) | A check for NaN is removed; results differ by reassociation | The bundle is not set by an optimization level that someone else chose; each member is set by name where needed | S5, S13 | The bundle's membership is specific to a compiler; the effect is general |
| Link-time effect of fast-math | Clang's manual, as extracted: fast-math "causes crtfastmath.o to be linked" (unless shared or disabled), and that object sets flush-to-zero and denormals-are-zero bits process-wide, affecting all linked libraries (S13 extract). GCC: the unsafe-math option "when used at link time, may include libraries or startup files that change the default FPU control word" (S5 extract) | One unit compiled with fast-math changes the arithmetic of unrelated libraries | The link step is among the places flags are recorded; the numerical record notes process-wide state | S5, S13 | Specific to the linkers and startup files; the class (global state set at link) is general |
| Optimization level changes results | Bentley et al. searched compilations of the MFEM library and examples across several compilers and flag sets and isolated 1,086 instances of result variability; for one, a climate model was said to need weeks of investigation when "a fused-multiply-add instruction" was introduced; a vendor's link step introduced variability "regardless of optimization level or switches" in five examples (S28). A dot-product vectorization changed an iteration norm to 1e-6 where the algorithm stopped at 1e-12 (S28 text, not the poster) | Results change with flags, compilers, and the link step | Result-bearing flags are inputs; a change of any is a change of the result (REPRO.6 sense) and is compared within the tolerance | S28 | The counts are specific to those codes; the finding is general |

Warnings and sanitizers:

- Clang's manual advises against enabling every diagnostic, since newer ones may be lower quality (S13 extract). Maintainers of BIND 10 (2013) and DPDK (2015) decided against warnings-as-errors by default in release archives, since a newer compiler can break a release that built before (S25, secondary, opinions and not studies). Practice: errors where the toolchain is fixed (checks of a change, STND.CXX.25), not as the default of a release that others build.
- Address sanitizing needs the flag at compile and link, and a typical slowdown is 2x (S10b extract). Thread sanitizing "generally requires all code to be compiled with" it, and does not support non-position-independent executables; uninstrumented code gives missed races or false positives (S11 extract). That the two cannot be combined is my knowledge [unverified]. A checking build is a named configuration that states its detectors (STND.CXX.26).

## 6. Reproducible builds

The Reproducible Builds project defines a build as reproducible "if given the same source code, build environment and build instructions, any party can recreate bit-by-bit identical copies of all specified artifacts" (S1 extract). The definition leaves the build environment to the project; the project's page on the perimeter says its scope "needs to be properly specified" and holds at least "a list of the tools used by the build process and their versions" (S1b extract).

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Timestamps | SOURCE_DATE_EPOCH is "a standardised environment variable" for "the last modification of something, usually the source code", in seconds since the Unix epoch; it is "meant to be already a flag forcing a particular timestamp to be used" in place of the clock (S2 extract). Examples there reject non-digits and clamp to the earliest archive date (S2) | Archives, documentation, and binaries embed the build time | One instant per revision (for example the revision's commit time), passed to each tool that embeds a time. The time-of-day macros are not used | S2, S26 | The variable is a convention of one project, adopted widely; the need is general |
| Order | Directory listings are not in a consistent order, so archives built from a directory differ; sorting depends on the locale; a wildcard in a build rule "can result in unreproducible builds" (S4 extract) | Different byte order of members | Inputs are listed explicitly or sorted in a named locale | S4, S7 | General |
| Locale and time zone | "The locale of the build system might affect the build products": time formats (`LC_CTIME`), collation (`LC_COLLATE`), and encoding (`LC_CTYPE`), with `LC_ALL` overriding; sort in the `C` locale and use `C.UTF-8` where a Unicode locale is needed (S7 extract) | Different sort order, date strings, and text | The build sets locale and time zone itself | S7 | Locale names are specific to POSIX-like systems; the dependence is general |
| Build path | Compilers record source paths in debug information; GCC and Clang accept prefix-map options for debug info, for the file-name macro, and for both (S5b extract). The page notes that post-processing is often needed and that "no good tool currently exists" for debug symbols (S5b extract) | The output differs by directory | Either a fixed path, treated as part of the environment (S3 extract), or a prefix map; the record says which | S3, S5b | The options are compiler specific; the problem is general |

Corpus link: STND.VVUQ.82 and .83 say strict determinism is an option and that declared variation within the agreed tolerance is not a defect. For builds the same holds: bit-identical output is an option, and a build record that states which outputs vary and why meets REPRO.3. A build whose output depends on the clock with no record of it is an undeclared variation.

## 7. Hermeticity, network access, and the supply chain

- Bazel: a hermetic build system "always returns the same output by isolating the build from changes to the host system"; sources of non-hermeticity are arbitrary processing in build files, nondeterministic tools (identifiers, timestamps), host binaries and absolute paths, and writes to the source tree (S18 extract).
- SLSA 1.0: isolation of build steps is required at its third level; "hermetic" ("roughly means that the build ran with no network access") is deferred; external parameters "MUST be fully enumerated" there; completeness of resolved dependencies is "best effort" (S19 extract). Its levels will move; the lasting content is isolation, enumerated parameters, and listed resolved dependencies.
- Debian policy: "required targets must not attempt network access to other hosts", with one archive-area exception (S17 section 4.9, extract). CMake's fetch module advises a commit hash over a branch or tag name, and says its disconnected mode "is not an appropriate way to prevent any network access on the first run" (S9b extract). A pin by name moves; a pin by content does not.
- The xz compromise (CVE-2024-3094, disclosed 2024-03-29): the first stage was in the release tarballs and not the repository; a changed build macro file "injects an obfuscated script to be executed at the end of configure"; the script checked architecture, compiler, and packaging before acting; the payload sat in test files no test used (S16 extract). General lessons: a release archive is not the repository; a generated build script runs with the builder's privileges; test data can carry code; a payload conditioned on the environment is hard for investigators to reproduce.
- Corpus: STND.DEPS.6 and .7 bind. A build standard adds only the point of use: no fetch inside the build step.

## 8. Generated sources, vendored versus fetched dependencies, pinning

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Generated source out of date | GLib generator case (S20 §5.1); Debian policy: edit the template input, not the generated build file, and generated helper files are removed by clean (S17 §4.3, §4.10 extract) | Edits lost; stale generated code | Generated files are marked, are outputs with declared prerequisites, and are not edited | S20, S17 | General |
| Release archive differs from the repository | xz (S16) | Reviewed source is not shipped source | The archive is made by a recorded step from the revision, and a comparison with the repository is available | S16 | General |

## 9. Install and export of build interfaces; build types

- CMake's guide: an exported package "must not reference absolute paths of files on the machine where the package is built"; include directories are relative to the install prefix; dependencies are found through imported targets (S9c extract). Generalized: an exported interface states include paths, definitions, link needs, and the settings users must match (floating-point mode, edition, assertion macro), relative to the install location. A mismatch between how a library was built and how it is used is a hazard the interface should detect; STND.CXX.10 holds the mechanism for header-only libraries. I found no study of how often it occurs.
- A build type is a bundle of flags; its name does not say what is in it, and CMake's default type "is often an empty string" (S12b extract). The build record lists settings, not the type name, and a result is reported from the configuration it was measured in. GCC's highest level "disregard[s] strict standards compliance" (S5 extract): one level name can include a break from the language standard. STND.CXX.27 asks that builds reporting results enable the library's production checks.

## 10. Device code for several accelerator architectures

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Real versus virtual targets | NVIDIA's compiler driver: a virtual architecture governs generation of intermediate code, which "is dynamically compiled by the CUDA runtime system" when no matching binary exists; a real architecture gets "a true binary load image"; a fat binary can hold several of each (S24 extract). CMake's property accepts a list, with `-real` and `-virtual` suffixes, an `all`, and a `native` value, and it is an error to leave it empty for targets with CUDA sources (S9d extract) | Code compiled at load changes first-run time and may change arithmetic by driver (corpus STND.OFFLD, Notes) | The record lists real and virtual targets (corpus STND.OFFLD.24) | S24, S9d | The names are vendor specific; real versus load-time compiled is general |
| `native` target | The build targets the devices present on the build host (S9d extract) | The result is tied to one machine, and a build on a headless builder fails or picks nothing | A `native` build says which host in the record (section 12) | S9d | General |

Corpus STND.OFFLD.24 holds the record of the architectures; STND.OFFLD.25 holds the run record. HW.3 and HW.7 hold the check at the start of a run. This note found nothing beyond them for the build, except the point that `native` and the empty-list error are two ways a build decides its target set without anyone writing it down.

## 11. Caching of build results

| Hazard | Source fact | Failure | Practice | Sources | Holds across versions and implementations, or specific |
|---|---|---|---|---|---|
| Key lacks an input | Bazel's remote cache: tools outside the workspace are not tracked, so "two machines can produce different outputs under the same action hash" and users wrongly share hits; environment variables count only when listed (S18b extract) | A wrong result served as a hit | The cache key holds the tool identity, the command line, the declared environment, and the input digests | S18b, S26 | General |
| Untrusted writers | "Take care in who has the ability to write to the remote cache"; the advice is that only the CI system write (S18b extract) | A compromised cache serves code | Writers are restricted; consumers treat a hit like fetched content | S18b | General |

## 12. The build record

What a result must be traceable to is already in the corpus as REPRO.1, REPRO.2, and REPRO.4. A build adds items. Debian's `.buildinfo` file records the architecture of the build machine, the installed packages that might affect the build (with their recursive dependencies), the environment variables known to affect it, and checksums of "all files that make up the build" (S6 extract). SLSA adds the enumerated external parameters and the resolved dependencies (S19 extract). Collected, a build record can hold:

1. The source revision, and whether the tree had uncommitted changes.
2. The configuration: each option chosen, and each result of detection (section 3).
3. The toolchain: compilers, linker, libraries, their revisions, and the machine the build ran on (and, for a cross build, the target).
4. Settings of section 5: contraction, finite-math, optimization, assertions, checks, sanitizers, target instruction set, device targets.
5. Environment variables and the locale, time zone, and instant used.
6. Resolved dependencies with digests (STND.DEPS.6, .10).
7. Digests of outputs.
8. Cache use and its settings.
9. Whether the build was clean or incremental.

Each is a place where a result can differ; none names a tool.

## 13. Continuous-integration matrices

- A matrix is a declared set of configurations with a rule for what a failure means; GitHub's documentation (extract) has include and exclude rules, a parallel limit, and cancellation of the rest on a failure unless marked to continue (S29).
- Hilton et al. (ASE 2016): 34,544 projects, 1,529,291 builds, 442 survey replies; CI was widely used, about 40% of their breadth corpus, and projects with CI released more often; non-users cited the lack of automated tests (S31, abstract and body, skimmed).
- Axes that follow from this note: oldest and newest declared dependency combinations (STND.PY.14), toolchains, the checking configuration, the host-only build (STND.OMP.4), and device targets. Combinations left out for cost are listed. A hosted runner changes under the project; the build record shows when it did.

## What the corpus already holds

| Matter | Provision | What it holds | Gap for BUILD |
|---|---|---|---|
| Dependency record, pinning, review | REPRO.9; STND.DEPS.1 to .5, .10, .11 | Enumerate with revision, reason, and license; stable revision at adoption; review at each release; lock files may serve | Nothing; the build cites it |
| Integrity of fetched components | STND.DEPS.6 (binding, GUARD.17) | Verify before use against a recorded digest | When in the build the fetch occurs (outside the build step) |
| Toolchain revisions as inputs | STND.DEPS.8; REPRO.1, REPRO.2 | Each compiler, interpreter, synthesis tool, and PDK revision recorded with each result | Linker, libraries, sysroot, build host machine, generators |
| Determinism | REPRO.3; STND.VVUQ.82, .83 | Identical, within tolerance, or declared variation | How the build declares variation (timestamps, order) |
| Provenance written with output | REPRO.4 | Written at production by the producing software | The build record as that provenance for built artifacts |
| Repository configuration term; execution setting term | STND.CODE (Terms) | The versioned files that set how tools build, check, and test; flags that change which code executes | Gives BUILD its vocabulary |
| Untrusted-input checks not removable by a setting | STND.CODE.6; STND.CXX.18 | The check runs in every build | The build-type side of the same fact (section 5) |
| Build settings stated, C++ | STND.CXX.4 | Edition, extensions, floating-point semantics, contraction, instruction set, library check mode, stated per unit in the repository configuration | Language-neutral version |
| Toolchain matrix term | STND.CXX (Terms) | Compilers and library implementations per unit, at pinned revisions | Same idea for other languages |
| Warnings fail checks | STND.CXX.25 | Compiler warnings at a recorded set fail the change's checks | The release-versus-change distinction (section 5) |
| Run-time detector builds | STND.CXX.26 | Tests run in a detecting build; first detection fails | Sanitizer configurations are distinct (section 5) |
| Header-only libraries state edition and options | STND.CXX.10 | Stop with a diagnostic on an unsupported option | Exported interfaces (section 9) |
| Julia manifests and run settings | STND.JL.4, .5; Terms (Production configuration) | Committed manifests when results are reported; thread count, BLAS, options recorded | Same for compiled languages |
| Execution path record | HW.3 | Item-level identification of hardware, firmware, drivers, runtime libraries, and settings | Build host is an execution path of the build |
| Delivered arithmetic | HW.5 | Properties on which working precision depends, with each mode or option that sets them | Flag-level link to the build |
| Contract currency | HW.7 | Evidence current for the model, firmware, drivers, libraries, and settings | None |
| Also relevant | REPRO.2, REPRO.10; STND.CODE.4, .9; STND.CXX.19, .27; STND.PY.13, .14; HW.EMBED.5; STND.CLASS.10 | Environment properties recorded; the workflow that produces a result is a versioned artifact; static checks per change; repeatable test verdicts; exceptions stated per build; production library checks in reporting builds; declared releases and oldest/newest checks; image identity; class onset of default provisions | Class onset of BUILD provisions is for the drafter |
| Device code record | STND.OFFLD.24 | Each accelerator model with compiled code; load-time compilation | None; section 10 is consistent with it |
| OpenMP disabled | STND.OMP.4 | Documentation states whether the component builds and computes within tolerance without OpenMP; checks build and test it | Generalizes to any optional feature of a build |

Everything above that the corpus holds, a BUILD standard cites. What it can add without restating: the build record as a unit (section 12), the rule that undeclared inputs are defects, the rule that no network is used inside the build step, and the rule that a flag that changes results is set and recorded in one place per unit. None of these raises the floor if it asks only for a record and a declaration that REPRO.1, REPRO.2, and REPRO.4 already require; whether a given item needs a floor argument is the custodian's to decide (GOV.11).

## Timeless versus moving

Timeless: a build is a function from inputs to outputs, and an input missing from the declarations makes it wrong; parallel and incremental builds expose missing declarations; time, order, locale, and path are inputs unless removed; a pin by content holds where a pin by name moves; the default of a flag belongs to a compiler and a mode, not the language; a release archive is not the repository; a cache is correct when its key holds all inputs; a build host cannot run target code in a cross build.

Moving, so kept out of provisions: names of variables, options, and macros; defaults of specific compilers, the membership of the fast-math bundle, and sanitizer combinations; accelerator architecture names and compatibility rules; SLSA levels and what it defers; the counts of the 2009 to 2024 studies; hosted CI features.

## Not verified

- GNU Make manual (parallel execution, order-only and automatic prerequisites) and Automake's separate-directory page: HTTP 429 on every attempt; not read. Autoconf cross-compilation text: search extract only.
- The `recording-dependencies` page of the Reproducible Builds site returned 404; `.buildinfo` content came from the Debian manual page extract.
- That address and thread sanitizers cannot be combined: my knowledge.
- Seo et al. (ICSE 2014), McIntosh et al. (2011), BUMP, Ochoa et al.: search extracts and citations in S20 and S21; Hilton et al. beyond the abstract: skimmed.
- Clang pages were cut off before the sanitizer-combination and prefix-map sections; the NVIDIA driver page was read to 180,000 characters.
- Not examined: other build tools (Meson, Nix, Guix, Cargo, language package managers) and their lock and hermetic designs; whether every tool honors the epoch variable; any study of how often library build settings mismatch user settings.

## Sources

| ID | URL | What it supports |
|---|---|---|
| S1 | https://reproducible-builds.org/docs/definition/ | Definition of a reproducible build |
| S1b | https://reproducible-builds.org/docs/perimeter/ | Scope of the build environment |
| S2 | https://reproducible-builds.org/docs/source-date-epoch/ | Epoch variable |
| S3 | https://reproducible-builds.org/docs/deterministic-build-systems/ | Ordering, timestamps, build path, randomness |
| S3b | https://reproducible-builds.org/docs/volatile-inputs/ | Network inputs, lock files, vendoring, snapshots |
| S4 | https://reproducible-builds.org/docs/stable-inputs/ | Stable order |
| S5b | https://reproducible-builds.org/docs/build-path/ | Prefix maps, fixed path |
| S5c | https://reproducible-builds.org/docs/system-images/ | System image hazards |
| S5 | https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html | Contraction default, fast-math members, finite-math, link-time effect (two reads, offset 0 and 100000) |
| S6 | https://manpages.debian.org/unstable/dpkg-dev/deb-buildinfo.5.en.html | Build information fields |
| S7 | https://reproducible-builds.org/docs/locales/ | Locale effects |
| S8 | search extract on the Autoconf manual (Runtime and Specifying Target Triplets pages, gnu.org) | Cross-compilation and test programs; not read directly |
| S9 | https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html | Toolchain files, cross compiling |
| S9b | https://cmake.org/cmake/help/latest/module/FetchContent.html | Pin by hash, disconnected mode |
| S9c | https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html | Relocatable exports |
| S9d | https://cmake.org/cmake/help/latest/prop_tgt/CUDA_ARCHITECTURES.html | Architecture lists, real and virtual, native |
| S10 | https://en.cppreference.com/w/c/error/assert | Assertion removal by macro |
| S10b | https://clang.llvm.org/docs/AddressSanitizer.html | Address sanitizer build requirements |
| S11 | https://clang.llvm.org/docs/ThreadSanitizer.html | Thread sanitizer limits |
| S12 | https://cmake.org/cmake/help/latest/manual/cmake.1.html | Source tree, build tree |
| S12b | https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html | Build types |
| S13 | https://clang.llvm.org/docs/UsersManual.html | Contraction modes, fast-math, process-wide effect, warning advice |
| S16 | https://www.openwall.com/lists/oss-security/2024/03/29/4 | xz compromise (CVE-2024-3094) |
| S17 | https://www.debian.org/doc/debian-policy/ch-source.html | Build-time dependencies, no network, generated files |
| S18 | https://bazel.build/basics/hermeticity | Hermetic builds |
| S18b | https://bazel.build/remote/caching | Remote cache correctness |
| S19 | https://slsa.dev/spec/v1.0/requirements | Isolation, parameters, dependencies, cache identity |
| S20 | https://rebels.cs.uwaterloo.ca/papers/emse2017_bezemer.pdf | Bezemer et al., unspecified dependencies (full text) |
| S21 | https://arxiv.org/pdf/2404.13295 | Lyu et al., ISSTA 2024, build dependency errors (full text) |
| S22 | https://aegis.sourceforge.net/auug97.pdf | Miller, Recursive Make Considered Harmful (full text) |
| S23 | https://ninja-build.org/manual.html | Implicit dependencies, command log, no build-time decisions |
| S24 | https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html | Real and virtual targets, compatibility (two reads) |
| S24b | https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_porting_guide.html | Per-architecture compilation |
| S25 | search results: lists.isc.org (bind10-dev, February 2013) and inbox.dpdk.org (February 2015) | Warnings as errors in release archives (secondary) |
| S26 | https://ccache.dev/manual/latest.html | Cache hazards |
| S27 | https://research.google/pubs/programmers-build-errors-a-case-study-at-google/ (search result) | Seo et al., 26.6 million builds (secondary) |
| S27b | https://swag.uwaterloo.ca/publications/an-empirical-study-of-build-maintenance-effort.html (search result) | McIntosh et al., build maintenance (secondary) |
| S28 | https://arxiv.org/pdf/1811.05618v1 | Bentley et al., compiler-induced variability (full text) |
| S29 | https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs | Matrix semantics |
| S29b | https://arxiv.org/abs/1803.06766 | Ren et al., localizing unreproducible builds |
| S30 | https://arxiv.org/abs/2104.06020 | Lamb and Zacchiroli, reproducible builds |
| S31 | https://cs.uwaterloo.ca/~m2nagapp/courses/CS846/1171/papers/hilton_ase16.pdf | Hilton et al., continuous integration (skimmed) |
| S31b | https://arxiv.org/pdf/2401.09906 (search result) | BUMP (secondary) |
| S31c | https://arxiv.org/pdf/2110.07889 (search result) | Ochoa et al., Maven Central (secondary) |
