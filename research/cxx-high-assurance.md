# High-assurance C++ coding standard for CSQ1 and CSQ0 projects

Role: research agent (STND.CREW), delegation depth 1. Date of research: 2026-10-22. Read-only retrieval; no paywalls bypassed; no mirrors or caches used. Copyrighted rule text (MISRA, AUTOSAR, JSF, HIC++) is paraphrased, not reproduced.

## 0. Evidence grading

- **[R]** Retrieved this session from the URL cited in section 7. Retrieval used a summarizing fetch tool, so numbers are only as good as that summary.
- **[B]** Background knowledge, not verified this session. Treat as unconfirmed until checked.
- **[J]** My engineering judgment.

Several things the brief asked for could not be retrieved. The SEI CERT wiki and the AUTOSAR R22-11 PDF refused automated fetching (robots). I did not work around that. Section 6 lists these gaps.

## 1. Short answer

Adopt **MISRA C++:2023 (TC1:2026)** as the normative rule set for CSQ1 and CSQ0. It is the only candidate that is current, maintained, aimed at safety-related systems, built on a modern language level (C++17), and supported by several commercial analyzers. [R]

The custodian's three named candidates rank as follows:

- **MISRA:** yes, but specifically MISRA C++:2023, not MISRA C++:2008.
- **JSF AV C++:** no for new work. It is a 2005 C++03 document. Use it only as history. Its useful ideas (no exceptions, no recursion, no allocation after startup) survive in other form.
- **NASA:** there is no NASA C++ coding standard to adopt. The JPL Institutional Coding Standard is for C. "Power of 10" is a short set of process-level restrictions that should be layered on top of MISRA C++:2023 at CSQ0.

Add three layers on top of MISRA C++:2023: (1) project-level restrictions from Power of 10 and JPL practice, (2) SEI CERT C++ as a supplementary security/UB checklist, and (3) C++ Core Guidelines as non-normative design guidance only. None of the three is a substitute for the first.

"Latest standard always" cannot hold for CSQ1 and CSQ0 as an unconditional rule. See section 4.

## 2. Comparison table

| Item | MISRA C++:2023 (TC1:2026) | AUTOSAR C++14 (R19-03) | JSF AV C++ (Rev C) | NASA / JPL | SEI CERT C++ | HIC++ 4.0 | C++ Core Guidelines |
|---|---|---|---|---|---|---|---|
| Version and date | Published Oct 2023. TC1:2026 adds no new guidelines and is treated as equivalent [R] | Document 839, 2019-03-29. Marked obsolete; handed to MISRA [R] | Doc 2RDU00001 Rev C, Dec 2005 [R] | JPL C standard (2009, D-60411) [R, date via search result title only]; Power of 10, 2006, Holzmann [R] | 2016 edition; rule list last updated 2023-05-23 per a tool vendor's page [R] | 4.0, 2013-10-03 [R] | Living document; page dated 2026-06-14 [R] |
| Language targeted | C++17 (ISO/IEC 14882:2017) [R] | C++14, as a delta on MISRA C++:2008 (C++03) [R] | C++03-era (cites 14882:2002/2003) [R] | JPL standard: C. Power of 10: C. No NASA C++ standard found [R] | C++ (2016 text mentions C++14 lambdas) [R] | C++11 [R] | C++20 primarily; most advice applies to C++11 and later [R] |
| Scope | Implementation-level guidelines for safety-related C++; supersedes MISRA C++:2008 and absorbs AUTOSAR C++14 [R] | Implementation, verification, toolchain, and infrastructure rules for Adaptive AUTOSAR [R] | Air vehicle software (required); recommended elsewhere [R] | JPL: flight software, 6 compliance levels [R]. Power of 10: any critical C code [R] | Security and reliability: UB, memory, containers, exceptions [R] | General high-integrity C++ [R] | Broad design and style guidance, not a certifiable subset [R] |
| Rule count | 179 = 4 directives + 175 rules [R] | Not retrieved. [B] roughly 400 | Numbering to 221 (219 numbered + sub-rules; 233 entries in one tool vendor's list) [R] | JPL: not retrieved. Power of 10: 10 rules [R] | 83 rules; recommendations moved out of the main list [R] | 155 rules (consolidated down from 202) [R] | Several hundred, not counted. Not all enforceable [R] |
| Classification | Mandatory / required / advisory; decidable / undecidable; single-TU / system scope [R] | Required / advisory; automated / partially / non-automated; target (implementation, verification, toolchain, infrastructure) [R] | shall (verified) / will (not verified) / should (advisory) [R] | JPL: compliance levels. Power of 10: none [R] | Severity, likelihood, remediation cost, priority levels [B] | By language clause; no safety tiers [R] | Per-rule enforcement notes, profile membership [R] |
| Licensing | Paid. Single named-user PDF, on-screen only, no sharing. Price not shown on page [R] | Free PDF download from AUTOSAR [B]; site refused automated fetch | Free PDF [R] (hosted at stroustrup.com) | JPL and Power of 10: free [R] | Free [R] | Free to read with attribution to PRQA, but behind a registration/sales wall since at least 2026 [R] | Free, MIT-style license [R] |
| Maintenance | Active; TC1 issued 2026 [R] | Frozen. Superseded by MISRA C++:2023 [R] | Frozen since 2005 [R] | JPL: frozen [J]. Power of 10: static | Slowly maintained; last rule-list update 2023 [R] | Frozen. LLVM discussed removing hicpp checks in 2026 [R] | Active; editors Stroustrup and Sutter [R] |
| Tools | Polyspace (all rules, since R2024b) [R]; Helix QAC (claims 100%) [R]; SonarQube Enterprise/Data Center (claims all 179; IDE covers 174) [R]. Parasoft, CodeSonar, Cppcheck Premium, PVS-Studio: not verified this session. clang-tidy: no misra module in the checks list (trunk 24.0.0git) [R] | Parasoft, CppDepend list AUTOSAR C++14 [R]; Helix QAC [B] | Klocwork has a JSF mapping [R]; Polyspace [R] | Polyspace, Klocwork, VectorCast named in NASA handbook (for C) [R] | clang-tidy cert-* (42 checks) [R]; SciTools CodeCheck covers 73 of 83 [R]; many commercial tools [B] | LLVM hicpp-* checks cover part of it; under removal discussion [R] | clang-tidy cppcoreguidelines-* (43 checks) [R]; Microsoft C++ Core Check [B] |
| Dynamic memory | Discouraged by rule (avoid dynamic memory; if used, manage automatically; no advanced memory management) [R]. Categories not retrieved | `new`/`delete` allowed with limits; `malloc`/`free` banned [R] | Banned after initialization (AV Rule 206: tool mapping lists no non-placement new/delete) [R] | Power of 10 and NASA handbook: no allocation after initialization [R] | Memory-management rules (8) [R] | Not retrieved | Prefers RAII and smart pointers; does not ban the heap [R] |
| Exceptions | Allowed, with 8 rules (catch by reference, top-level catch-all, `noexcept` discipline, no pointer-typed exception objects) [R] | Allowed; function-try-blocks and dynamic exception specs banned [R] | Banned (AV Rule 208) [R] | Not applicable in C | 13 rules on exceptions and error handling [R] | Not retrieved | Prefers exceptions for errors; also covers `noexcept` [R] |
| RTTI | `dynamic_cast` is the allowed way to downcast from a virtual base; `typeid` on a polymorphic expression is restricted [R] | `dynamic_cast` prohibited in the summary I received [R] | `dynamic_cast` not permitted for safety-critical code for now (AV Rule 178) [R] | n/a | Not retrieved | Not retrieved | Discourages casts; permits `dynamic_cast` with care [B] |
| Templates | Allowed. At least one rule bans explicit specialization of function templates [R] | Allowed, including variadic and variable templates [R] | Allowed with review and test of every instantiation (AV Rules 101-106) [R] | n/a | Not retrieved | Not retrieved | Encouraged [R] |
| Recursion | Banned (direct and indirect) [R] | Not retrieved | Banned for safety-critical (AV Rule 119), with a narrow provable-stack exception [R] | Power of 10: banned [R] | Not retrieved | Not retrieved | Allowed |
| STL / std library | No blanket ban. Bans specific C functions, `<cstdarg>`, `<csetjmp>`, `<csignal>`, C I/O. Has rules on `std::move`/`forward`, algorithm results, and moved-from objects [R] | Library coverage incomplete in this edition [R] | C library facilities restricted; library used in safety-critical code must itself be certifiable (AV Rule 16) [R] | Handbook does not address STL [R] | 9 container rules [R] | Not retrieved | Encourages the standard library and GSL [R] |
| Certification relevance | Intended for IEC 61508 / ISO 26262 / similar coding-standard obligations [B]. Not itself a certification | Same, for automotive [B] | DO-178B/C-style use in avionics [J] | NPR 7150.2 SWE-061 (now SWE-961) requires a coding standard; handbook does not mandate a specific one [R] | Evidence for security and UB avoidance [J] | Same as MISRA, older | None; not a certification subset [J] |

## 3. Candidate notes

### 3.1 MISRA C++:2023

- Published October 2023, targets C++17. The publisher's page labels the current document "TC1:2026", which incorporates technical corrigenda and adds no new guidelines. [R]
- It merges MISRA C++:2008 (C++03) and AUTOSAR C++14. AUTOSAR and MISRA announced the merge in January 2019. AUTOSAR's own R19-03 document says maintenance was handed to MISRA. [R]
- 179 guidelines: 4 directives and 175 rules. Directives need human judgment (design intent, documentation). Rules are written so a tool can check them. [R]
- Categories are mandatory (no deviation), required (formal deviation), advisory. I could not retrieve the count per category or the category of individual rules (for example, whether the dynamic memory rule is required or advisory). Check the licensed document. [R for scheme, gap for counts]
- Stance on the custodian's features, from rule titles on the Polyspace page [R]:
  - Dynamic memory: avoid it; if used, manage it automatically; no advanced memory management.
  - Exceptions: allowed, but with a disciplined set of rules.
  - Recursion: banned.
  - Templates and lambdas: allowed, with specific limits (explicit specialization of function templates banned; explicit captures in non-transient lambdas).
  - Casts: C-style casts and `reinterpret_cast` banned; unions banned.
  - Undefined behavior: a rule forbids undefined or critical unspecified behavior.
- It does not cover C++20 or later. No C++20/23 edition of MISRA C++ was found in the sources retrieved. [R, absence of evidence]
- Licensing is paid and per named individual, which affects how a custodian distributes it to projects. Budget a license per engineer, or ask MISRA about other terms. [R]

### 3.2 AUTOSAR C++14

Superseded. AUTOSAR's own document is marked obsolete and says it will be removed from the standard in an upcoming release. [R] Use only to read legacy project claims. Not a target for new work.

### 3.3 JSF AV C++ (2005)

- A real, careful document, and the origin of many later restrictions. Its signature rules are: no exceptions, no recursion (with a narrow exception), no allocation after initialization, and tight limits on casts. [R]
- Problems for this custodian: it targets C++03, so it has no `auto`, lambdas, `constexpr`, move semantics, `std::array`, or smart pointers. It has no coherent position on the STL. It bans exceptions outright, which conflicts with heavy standard-library use. Its rules cite DO-178B and "SEAL" levels, which are Lockheed-specific. [R]
- The rationale behind the bans (exception timing cannot be bounded by current tools) is still valid. A secondary source (December 2025) calls JSF outdated and recommends the Core Guidelines. I do not agree with the second half of that for CSQ0, since the Core Guidelines are not a certifiable subset. [R, secondary]

### 3.4 NASA / JPL

- JPL's Institutional Coding Standard is for C, with six compliance levels. Projects pick a level, adopt another standard, or tailor it. [R]
- The NASA Software Engineering Handbook names the JPL C standard, a GSFC C standard and a GSFC C++ flight software standard, and Power of Ten. It says projects must identify the coding standard they use but does not mandate one. NPR 7150.2 requirement SWE-061 (last used in revision D; replaced by SWE-961 in the software assurance section) asks for secure coding standards. [R]
- The handbook's minimal rule set applies across languages: limit dynamic allocation to one-time initialization, simple control flow, bounded loops, no recursion, small scope for data, validate inputs, check return values. [R]
- Power of 10 (2006, Holzmann) has ten rules covering control flow, loop bounds, no allocation after initialization, short functions, at least two assertions per function, minimal scope, return value checks, a limited preprocessor, restricted pointers, and pedantic warnings plus daily static analysis. [R]
- I did not retrieve the GSFC C++ standard itself or any NASA-owned C++ standard text. The F Prime flight framework is said to carry JSF-derived ideas, but I only have a secondary source for that. [R, secondary]

### 3.5 SEI CERT C++

- 83 rules in the CodeCheck list; recommendations were moved out of the main list and into a holding section. Rule list last updated 2023-05-23 per that page. Categories: concurrency, containers, declarations, exceptions, expressions, I/O, integers, memory, misc, OOP, strings. [R]
- Free. Aimed at security and undefined behavior rather than a safety-critical subset, so it does not by itself restrict dynamic memory, templates, or exceptions. [J]
- The edition is aging. It is a useful checklist and has clang-tidy coverage (42 `cert-*` checks), but it does not track C++17/20. [R for tool count, J for conclusion]
- The SEI wiki would not be fetched (robots). I relied on third-party descriptions.

### 3.6 High Integrity C++ 4.0

- 155 rules, C++11, published 2013 by Programming Research (now Perforce). [R]
- It now sits behind a registration/sales wall. In February to March 2026 the LLVM project discussed removing its clang-tidy `hicpp` checks because the standard is hard to obtain, the attribution terms are awkward, and maintainers cannot verify bug reports. No decision was recorded in the thread. [R]
- Not recommended: frozen at C++11 and effectively unavailable.

### 3.7 C++ Core Guidelines and safety profiles

- Page dated 2026-06-14, editors Stroustrup and Sutter, MIT-style license. The editors say the rules are not fully checked for completeness, consistency, or enforceability. [R]
- Profiles named in the Core Guidelines text: type (no type violations), bounds (no out-of-range access), lifetime (no leaks, double deletes, or invalid-object access). [R]
- **WG21 profiles status:**
  - Profiles did **not** make C++26. [R]
  - A profiles framework paper (P3589R3, 2025-12-01) defines enforce/suppress/require/exempt mechanisms and says profile checks cannot change overload resolution, template instantiation, or SFINAE. It defines no standard profile set. [R]
  - At the June 2026 Brno meeting, the Safety and Security subgroup (SG23) decided to write a Profiles specification. If ready in time it merges into C++29; otherwise it could ship as a white paper. An initialization profile (P4222) was reviewed, and a type-safety profile paper (P3984) is in progress. [R]
  - A Rust-style "Safe C++" proposal (P3390) was discontinued in ISO. [R, secondary]
- Consequence: nothing in the C++26 standard gives a CSQ-grade enforcement mechanism for bounds, type, or lifetime. Core Guidelines checks today come from tools (clang-tidy, 43 `cppcoreguidelines-*` checks) and the GSL, not from the language. [R]

## 4. Recommendation

### 4.1 Rule set

| Layer | Content | Status | Applies to |
|---|---|---|---|
| Normative base | MISRA C++:2023 (TC1:2026), all 179 guidelines | Mandatory | CSQ1, CSQ0 |
| Process restrictions | NASA/JPL/Power of 10 items not already in MISRA: no allocation after initialization, bounded loops, at least two assertions per function, return-value and parameter checks, pedantic warnings at zero, daily analysis | Mandatory at CSQ0; recommended at CSQ1 [J] | CSQ0 (CSQ1 recommended) |
| Supplementary checklist | SEI CERT C++ rules not already covered by MISRA (UB, containers, concurrency, integer handling) | Required for gap review; deviations recorded | CSQ1, CSQ0 |
| Design guidance | C++ Core Guidelines, plus GSL types such as `span`, `not_null` | Non-normative; cite specific rule IDs when relied upon | CSQ1, CSQ0 |
| Historical only | JSF AV C++, AUTOSAR C++14, HIC++ | Do not adopt | none |

Why this combination:

1. MISRA C++:2023 is current, maintained, and written for exactly this use. It has several commercial analyzers with claimed full coverage, which is what reviewers will want as evidence. [R]
2. Its C++17 baseline supports the custodian's wish for STL, generics, and header-only code, because C++17 includes `constexpr if`, fold expressions, `std::optional`, `std::variant`, `std::string_view`, and structured bindings. None of these is banned by anything I retrieved. [R for baseline; J for feature list]
3. It is the intended successor to the two documents (MISRA C++:2008 and AUTOSAR C++14) that were the industry's incumbents. [R]
4. It covers what the NASA material covers (recursion ban, dynamic memory discouraged, casts) but does not by itself impose "no allocation after initialization" or "two assertions per function". Those are project policy, hence the Power of 10 layer. [R for MISRA rules, J for gap]
5. The Core Guidelines cannot be the base: their authors say they are incomplete and not fully enforceable, and they do not restrict the language to a subset. [R]

Trade-offs:

- **Cost.** MISRA C++:2023 is a paid, per-person license. Core Guidelines, CERT, and JPL are free. [R]
- **No C++20/23/26 coverage.** Using a newer language level means deviating from the scope of the standard, not just from individual rules. [R, absence]
- **Overlap and conflict.** MISRA prohibits things the Core Guidelines recommend (for example, some forms of casts, unions, and certain dynamic-allocation idioms). The rule must be that MISRA wins, and Core Guidelines advice is used only where MISRA is silent. [J]
- **Analyzer variance.** Vendors claim full coverage of 179 guidelines, but undecidable guidelines get approximated differently by each tool. Expect different warning sets from different tools. [J]

### 4.2 What this means for each of the custodian's requests

**"Latest C++ standard always" [R unless marked]**

- C++26: WG21 completed technical work at the London meeting on 2026-03-28 and sent it for the international ballot. A secondary source (2026-08-09) says the ballot closes on 2026-09-27, and that the contracts feature put the vote at some risk. I did not find the ballot result. As of 2026-10-22 I cannot confirm that ISO has published C++26. The latest standard I can say is published is C++23 (ISO/IEC 14882:2024) [B].
- Compilers: GCC 16.1 (released 2026-04-30) implements contracts, reflection (behind `-freflection`), and erroneous behavior, and GCC's own page calls C++26 support experimental. GCC 16 defaults to C++20. Clang 23.1 (released 2026-08-25) has only partial C++26; its status page lists contracts, reflection, and erroneous behavior as not supported. MSVC 14.51 (VS 2026 18.6) lists C++23 and C++20 work; I could not confirm C++26 status. The cppreference page is best-effort and lags.
- Consequence: no compiler offers full, stable C++26 today. No safety-qualified toolchain or MISRA edition covers it.
- **Proposed rule [J]:** at CSQ1 and CSQ0, the language level is the highest level that is (a) covered by the adopted rule set, (b) fully implemented and qualifiable in the chosen compiler, and (c) analyzable by the project's static analyzers. Today that is **C++17**. Raise it only by an explicit custodian decision, recorded as a deviation from MISRA's scope with a per-feature justification (for example, C++20 `std::span`, `consteval`, and `std::bit_cast` are likely candidates; coroutines, modules, reflection, and contracts are not). Lower consequence classes may track newer standards.
- Pin the compiler version and flags in the build record. "Latest" means a moving target, which conflicts with the reproducibility that nuclear I&C evidence needs. [J]

**STL [R for rules, J for policy]**

- MISRA C++:2023 does not ban the STL. It bans specific C library functions and constrains dynamic memory.
- Allowed by default: `std::array`, `std::span`, `std::string_view`, `std::optional`, `std::variant`, `<algorithm>`, `<numeric>`, `<cmath>`, `<chrono>`, `<utility>`, `<tuple>`.
- Allowed only with an allocation policy: `std::vector`, `std::string`, `std::map`, `std::unordered_map`, smart pointers, `std::function`. Options: use only during initialization; use with a pre-sized or fixed-buffer allocator (for example `std::pmr` over a static buffer); or substitute a fixed-capacity container.
- Restricted: iostreams (MISRA bans C I/O but the `<iostream>` timing and allocation behavior need project review), `<regex>`, `<thread>`, `<random>` use needs review, anything that throws as its normal error path unless exception policy allows it.
- Check bounds-checked access (`at()`) against the exception policy.

**Templates and header-only code [R for rules, J for policy]**

- MISRA C++:2023 allows templates and has a rule against explicitly specializing function templates. JSF requires review and test of every instantiation. AUTOSAR allows templates including variadic ones. [R]
- At CSQ1 and CSQ0 the issue is verification, not legality: every instantiation that ships needs tests and static analysis, and analyzers often analyze uninstantiated templates poorly. [J]
- Recommended limits: ban recursive template metaprogramming where `constexpr` functions work; set a maximum instantiation depth and a maximum number of template parameters; require the analyzer to run on instantiated code (full build, not just parse); keep SFINAE/`enable_if` out of public interfaces in favor of `static_assert` and `if constexpr` (C++17); require that every header-only library compile warning-free under the project's flags. [J]
- Header-only code increases the ODR and translation-unit-scope surface. MISRA's system-scope rules need whole-program analysis. [J]
- Template metaprogramming that computes values at compile time is an advantage for CSQ0 because it moves checks to build time, as long as the result is reviewable. [J]

**Dynamic allocation [R for MISRA/NASA text, J for tiering]**

- CSQ0: no allocation after initialization (Power of 10 and NASA handbook). During initialization, allocation allowed only through a project-approved allocator and with a recorded failure path. Treat the MISRA dynamic memory rule as having no deviations without custodian sign-off.
- CSQ1: allocation after initialization needs a documented bound on total and peak use, deterministic allocator behavior, and a deviation record.
- Both: heap use must not occur in interrupt context or in any timing-critical path.

**Exceptions [J]**

- MISRA allows exceptions. JSF, JPL-style practice, and the F Prime lineage avoid them because worst-case throw/catch time cannot be bounded with current tools. [R]
- Suggested policy: CSQ0 builds disable exceptions (`-fno-exceptions`) and use explicit error returns (`std::optional`, a result type, or error codes). CSQ1 allows exceptions only in non-real-time, non-safety-function code, with the MISRA rules plus a top-level catch-all.
- This directly constrains STL use (see above) because many standard components report failure by throwing.

**Hardening and erroneous behavior [R]**

- C++26 makes reading an uninitialized local variable "erroneous behavior" rather than undefined behavior, with an opt-out attribute. It also adds a hardened standard library with precondition checks on common types. Both apply on recompilation as C++26. Contracts also arrived, but their safety value is disputed. [R]
- Treat these as defense in depth. They do not make code conform to MISRA, and they are not available in qualified compilers today. For C++17/20 builds, libstdc++ and libc++ have their own assertion/hardening modes [B]. Enabling them with a deterministic fail-stop handler is reasonable at CSQ1/CSQ0. Verify behavior for the chosen compiler version before relying on it. [J]

### 4.3 Certification context

- **IEC 61508, ISO 26262, DO-178C:** none certifies a coding standard. They require the project to define a coding standard or restricted language subset, enforce it, and use tools appropriately. A secondary source says IEC 61508-7 treats C and C++ as particularly recommended up to SIL 4 when a defined subset, coding guidelines, and static analysis tools are used. [R, secondary] DO-178C section 11.8 requires coding standards. [B]
- **Nuclear I&C:** IEC 60880:2006 (edition 2, category A functions) is the current edition on the catalog page I fetched; it sets software requirements including implementation. [R] IEC 62138 (categories B and C) and the specific language-subset clauses of both were not retrieved. [B/gap] NUREG/CR-6463 (1996) is NRC review guidance for programming languages in nuclear safety systems and includes a C/C++ section. It is review guidance, not a coding standard. [R] I found no NRC document that endorses a particular C++ coding standard. [R, absence; searches limited]
- Practical consequence: the custodian's own standard plus MISRA C++:2023 compliance evidence (tool reports, deviation records, review records) is what an assessor will look for. Tool qualification applies to the analyzer and the compiler. [J]

## 5. Open questions for the custodian

1. Is "latest standard always" meant for all consequence classes, or can CSQ1/CSQ0 be pinned to a lower, qualified level (C++17 now) with CSQ2 and below following newer standards?
2. Which compiler(s) and versions will CSQ1/CSQ0 projects use, and is any of them qualified or qualifiable (vendor kit, or in-house qualification evidence)?
3. Will the custodian buy MISRA C++:2023 licenses? How many named users? Is a site or organizational license available?
4. Which static analyzers are available (Polyspace, Helix QAC, SonarQube Enterprise, Parasoft, CodeSonar, Cppcheck Premium, PVS-Studio, clang-tidy)? The retrieved coverage claims are vendor statements; will you run a coverage check of your own against the MISRA documentation?
5. Exception policy at CSQ0 and CSQ1: ban, or allow with rules? This decides how much of the STL is usable.
6. Allocation policy: is a pre-allocated or `pmr` arena acceptable, or must CSQ0 code avoid all heap use including at startup?
7. Do the regulators or customers for these instruments require a specific standard (for example, a licensee's software program plan, or an IEC 60880/62138 compliance claim)? Their requirement overrides this note.
8. How should the custodian treat simulation code (stochastic point kinetics, transport) versus embedded instrument code? Simulation code with CSQ1 consequences (design decisions that affect safety) may need a different subset than real-time firmware. For example, large dynamic arrays are normal in simulation but incompatible with a CSQ0 allocation rule.
9. Which third-party generic libraries (Eigen, Boost, fmt, range-v3, JAX-adjacent C++ code) are expected in CSQ1/CSQ0 code? Heavy template libraries are the hardest case for MISRA conformance and analyzer support, and may need to be treated as isolated, separately qualified, or excluded.
10. What mechanism will the custodian use to reassess when MISRA publishes a C++20/23 edition or when profiles reach a stable specification (C++29 or white paper)?
11. Is two-tool analysis (two independent analyzers) required at CSQ0?

## 6. Gaps and caveats

- Per-category counts (mandatory/required/advisory) and the category of individual MISRA C++:2023 rules were not retrieved. Rule titles come from the Polyspace page, which does not mark categories.
- The AUTOSAR C++14 rule count, the JPL C standard text, the GSFC C++ standard, HIC++ rule text, and the CERT C++ wiki were not retrieved (robots, registration wall, or not attempted).
- JSF AV Rules 206 and 208 were confirmed through a vendor's rule-to-checker mapping, not through the PDF itself, whose text was truncated by the fetch tool.
- Parasoft, CodeSonar, Cppcheck Premium, and PVS-Studio support for MISRA C++:2023 is not verified. The searches returned vendor pages that the fetch tool summarized without MISRA C++:2023 specifics.
- The C++26 ISO ballot result (closing 2026-09-27 per a secondary source) was not found. The Wikipedia summary contained mixed signals on publication status.
- Clang's C++ status page shows entries for Clang 24, so it appears to reflect trunk, not the 23.1 release. I report it as such.
- The fetch tool summarizes pages with a small model. Numbers should be re-checked against the primary source before they go into a standard or a safety case.
- Retrieved content was treated as data. No retrieved page contained instructions directed at me.

## 7. Sources (all accessed 2026-10-22)

MISRA and tools
- https://misra.org.uk/product/misra-cpp2023/ (MISRA C++:2023 TC1:2026 product page: licensing, C++17, TC1)
- https://www.misra.org.uk/misra-cpp/ (MISRA C++ status page)
- https://www.mathworks.com/help/bugfinder/misra-cpp-2023-rules-and-directives.html (Polyspace rule list)
- https://codeant.ai/blogs/misra-c-plus-plus-2023 (counts, categories, lineage; secondary)
- https://www.all-about-industries.com/safety-critical-software-misra-c2023-from-a-to-z-a-b4e8def416835b51d1c27ca7607e14d8/ (secondary)
- https://www.perforce.com/blog/qac/misra-cpp-2023-intro (2023, secondary)
- https://www.cdsaonline.org/2023/12/04/perforce-provides-day-one-access-to-misra-c2023-compliance-module-critical-for-functional-safety-coding-compliance (Helix QAC claim)
- https://www.perforce.com/products/qac/free-static-code-analyzer-trial-misra-cpp-2023 (Helix QAC claim)
- https://www.sonarsource.com/knowledge/languages/cpp/misra-cpp-2023/ (SonarQube claim)
- https://clang.llvm.org/extra/clang-tidy/checks/list.html (clang-tidy checks list)
- https://cppdepend.com/blog/tag/cleancode/ (CppDepend rule sets)
- https://parasoft.com/blog/misra-cpp-2023-guide/ and https://parasoft.com/blog/best-misra-compliance-tools/ (fetched; no MISRA C++:2023 specifics)

AUTOSAR, JSF, HIC++, CERT
- https://www.autosar.org/fileadmin/standards/R19-03/AP/AUTOSAR_RS_CPP14Guidelines.pdf (AUTOSAR C++14 R19-03)
- https://stroustrup.com/JSF-AV-rules.pdf (JSF AV C++ Rev C)
- https://help.klocwork.com/current/en-us/concepts/jsfavrevcmappedtoklocworkcandccheckers.htm (JSF rule mapping)
- https://gigazine.net/gsc_news/en/20251208-f-35-cpp-jsf-standards (secondary, 2025-12-08)
- https://sdtimes.com/major-update-to-high-integrity-c-coding-standard-hic/ (HIC++ 4.0, 2013)
- https://www.perforce.com/blog/qac/high-integrity-cpp-hicpp (HIC++ summary)
- https://discourse.llvm.org/t/rfc-regarding-the-current-status-of-hicpp-checks/89883 (LLVM RFC, 2026)
- https://docs.scitools.com/codecheck/SEI_CERT_C++.html (CERT C++ rule list, 83 rules)
- https://www.helpnetsecurity.com/2017/04/18/secure-coding-c/ (CERT C++ 2016 edition news)

NASA / JPL
- https://swehb.nasa.gov/x/KwFiC (NASA Software Engineering Handbook, coding standards)
- https://swehb.nasa.gov/x/aoJNCg (handbook, SWE-061 note)
- https://en.wikipedia.org/wiki/The_Power_of_10:_Rules_for_Developing_Safety-Critical_Code
- Search result only, not fetched: https://www.slideshare.net/slideshow/jpl-coding-standardc/27790940 (JPL D-60411 reference)

Core Guidelines and profiles
- https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines (page dated 2026-06-14; fetched head only)
- https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3589r3.pdf (profiles framework)
- https://www.wholetomato.com/blog/c26-memory-safety-what-actually-ships-for-existing-code/ (C++26 safety features; profiles slipped; secondary)
- https://herbsutter.com/2026/03/ (C++26 trip report, March 2026)
- https://herbsutter.com/2026/06/13/brno-trip-report/ (Brno, June 2026)
- https://www.devclass.com/development/2026/04/01/contracts-are-in-c26-despite-disquiet-over-their-value/5213555

C++ standard and compilers
- https://en.wikipedia.org/wiki/C%2B%2B26 (mixed signals on publication status)
- https://isocpp.org/std/status (page not updated for C++26)
- https://shape-of-code.com/2026/08/09/2026-in-the-programming-language-standards-world/ (ballot close date; secondary)
- https://gcc.gnu.org/projects/cxx-status.html
- https://phoronix.com/news/GCC-16.1-Released
- https://clang.llvm.org/cxx_status
- https://phoronix.com/news/LLVM-23.1-Released
- https://cppreference.com/cpp/compiler_support
- https://learn.microsoft.com/en-us/cpp/overview/what-s-new-for-msvc

Certification context
- https://www.nrc.gov/reading-rm/doc-collections/nuregs/contract/cr6463/index.html (NUREG/CR-6463)
- https://online.standard.no/en/iec-60880-2006-ed2 (IEC 60880:2006 catalog entry)
- https://www.adesso.de/en/news/blog/programming-languages-in-safety-critical-applications.jsp (secondary)

## 8. Network log

Approximate sizes are the page text length reported by the fetch tool where it reported one; otherwise "summarized, size not reported". Total retrieval was a few MB at most, far under the 10,000 item and 10,000 MB limits (about 60 fetches and 15 searches). Searches returned link lists only.

| URL | Result | Approx. size |
|---|---|---|
| en.wikipedia.org/wiki/C%2B%2B26 | success | not reported |
| gcc.gnu.org/projects/cxx-status.html (offset 0) | success | 140,231 chars total; first 100,000 read |
| gcc.gnu.org/projects/cxx-status.html (offset 100000) | success, no relevant content | 40,231 chars |
| clang.llvm.org/cxx_status | success | not reported |
| perforce.com/blog/qac/misra-cpp-2023-intro | success | not reported |
| mathworks.com/help/bugfinder/misra-cpp-2023-rules-and-directives.html (x2) | success | not reported |
| isocpp.org/std/status | success, no C++26 detail | not reported |
| misra.org.uk/product/misra-cpp2023/ | success | small |
| misra.org.uk/misra-cpp/ | success | small |
| parasoft.com/blog/misra-cpp-2023-guide/ | success, no MISRA specifics | not reported |
| minifeed.net/items/LQBwigWHUuxZ | success (excerpt only) | small |
| minifeed.net/items/8GtDK8g0flqv | success (excerpt only) | small |
| wholetomato.com/blog/c26-memory-safety-... | success | not reported |
| open-std.org/.../2026/p3589r3.pdf | success | not reported |
| herbsutter.com/2026/06/13/brno-trip-report/ | success | not reported |
| devclass.com/.../5213555 | success | not reported |
| codeant.ai/blogs/misra-c-plus-plus-2023 | success | not reported |
| all-about-industries.com/... | success | not reported |
| cdsaonline.org/2023/12/04/... | success | small |
| perforce.com/products/qac/free-static-code-analyzer-trial-misra-cpp-2023 | success | small |
| stroustrup.com/JSF-AV-rules.pdf (offsets 0, 100000, 104000, 125000) | partial: first read ok (to about AV Rule 175 and then 202); AV Rules 203-221 not retrieved; offset 125000 past end | 109,778 chars total |
| sdtimes.com/major-update-to-high-integrity-c-coding-standard-hic/ | success | small |
| perforce.com/resources/qac/high-integrity-cpp-coding-standard | success, no HIC++ detail | small |
| swehb.nasa.gov/x/KwFiC | success | not reported |
| swehb.nasa.gov/x/aoJNCg | success (C-focused page) | not reported |
| en.wikipedia.org/wiki/The_Power_of_10:_... | success | not reported |
| wiki.sei.cmu.edu/.../SEI+CERT+C++ Coding Standard | FAILED: robots_disallowed. Not worked around | 0 |
| isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines (offsets 0 and 100000) | success; Pro section not in the portion returned | 109,052 chars returned |
| help.klocwork.com/.../jsfavrevcmappedtoklocworkcandccheckers.htm | success | not reported |
| autosar.org/.../R22-11/AP/AUTOSAR_RS_CPP14Guidelines.pdf | FAILED: robots_disallowed. Not worked around | 0 |
| en.wikipedia.org/wiki/MISRA_C | success, no MISRA C++ content | not reported |
| autosar.org/.../R19-03/AP/AUTOSAR_RS_CPP14Guidelines.pdf | success (first part only) | not reported |
| parasoft.com/blog/breaking-down-the-autosar-c14-... | success, no counts | small |
| helpnetsecurity.com/2017/04/18/secure-coding-c/ | success | small |
| docs.scitools.com/codecheck/SEI_CERT_C++.html | success | small |
| nrc.gov/.../cr6463/index.html | success | small |
| online.standard.no/en/iec-60880-2006-ed2 | success | small |
| clang.llvm.org/extra/clang-tidy/checks/list.html | success | 100,434 chars |
| phoronix.com/news/GCC-16.1-Released | success | small |
| phoronix.com/news/LLVM-23.1-Released | success | small |
| cppdepend.com/blog/tag/cleancode/ | success, no MISRA C++:2023 detail | small |
| herbsutter.com/2026/03/ | success | not reported |
| cppreference.com/cpp/compiler_support | success (first 100,000 chars) | 128,666 chars total |
| learn.microsoft.com/en-us/cpp/overview/what-s-new-for-msvc | success | not reported |
| discourse.llvm.org/t/rfc-regarding-the-current-status-of-hicpp-checks/89883 | success | not reported |
| perforce.com/blog/qac/high-integrity-cpp-hicpp | success | small |
| adesso.de/en/news/blog/programming-languages-in-safety-critical-applications.jsp | success | small |
| github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md | FAILED to yield content (page chrome only; the raw-file link was not tried) | about 822 KB file, 0 returned |
| shape-of-code.com/2026/08/09/... | success | not reported |
| sonarsource.com/knowledge/languages/cpp/misra-cpp-2023/ | success | small |
| parasoft.com/blog/best-misra-compliance-tools/ | success, no specifics | small |
| gigazine.net/gsc_news/en/20251208-f-35-cpp-jsf-standards | success | small |
| fprime.jpl.nasa.gov/latest/docs/user-manual/overview/fprime-coding-standard/ | FAILED: client_error | 0 |

Proxy status note: at 08:16 UTC the agent proxy logged one 403 policy denial on a CONNECT to en.wikipedia.org:443. The Wikipedia fetches listed above nonetheless returned content through the fetch tool; I did not retry any denied connection or use any alternate route.
