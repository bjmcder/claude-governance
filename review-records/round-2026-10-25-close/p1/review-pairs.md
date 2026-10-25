# STND.HARN.28 pair review of package P1 (2026-10-25)

Scope: the 191 listed pairs (CODE 90, STDC 38, CXX 63) and the same-level pairs below, read against the three reading copies and `rendered/`. I read the body of each of the 95 distinct other-side provisions and the Terms, Notes, and changed provisions of the drafts. I did not recompute the pair list or rehearse the scripts. Tests are those of `ledger115/review-pairs-offld.md`. Where a hardware provision lists fewer responses than STND.CODE.14, the response chosen is the intersection (the RUST review's precedent).

## Result in short

- Listed pairs: no conflict, no unowned matter, no restatement in any of the 191. Most share only a base (VV.1, DSGN.5, REPRO.7, PRIME.2). The substantive ones (CODE.6, .14, .15, .16 against CPS.5, CPS.9, HW.8, HW.GPU.3, HDES.14, ML.6) are supportive and can be met together. Two observations attach to pairs: F9 (CXX 52-54) and F10 (CODE 27-46).
- Twelve findings, all in same-level pairs or Notes. F5 would become a conflict if left.

## Findings

**F1. STND.CODE.14, "in a result that the contract of the code names for it" (floor, narrowing).** CXX.16, PY.22, JL.15, RUST.13, FTN.29, and LEAN.25 all say "return the condition in its result". CODE.14 is stricter, and binds at CSQ4, where CODE.3 (contracts at declarations, from CSQ3) is omitted. Code that returns an unnamed sentinel meets the language provision and fails CODE.14; the Notes' floor argument does not cover the clause. Fix: end the sentence "or pass the condition to its caller, in its result or by a mechanism of its language, an exception among them, that propagates the condition to the caller". If the clause is wanted, put it to the custodian as a floor decision. STDC.2 can keep "an object that its contract names".

**F2. STND.CODE.16 sentence 2, "a definition in the source of the work".** Read literally it reaches any constant that gates a check, not only the conditional-compilation case the Notes describe. Fix: "in a form that a definition that the source of the work gives to conditional compilation turns off".

**F3. Unowned matter: a finite-value assumption set by annotation.** CODE.16 sentence 3 reaches an execution setting only. Julia `@fastmath` (the JL Notes record that it assumes no NaN) and a compiler pragma or attribute in C or C++ give the same license from the source; neither is a setting or a definition, so CODE.6, CODE.16, and JL.13 miss them, and NUMER.16 and NUMER.17 govern the speed, not the removed check. Fix: "compiled under an execution setting, or carry an annotation in its source, that, by the documentation of its compiler, lets the compiler assume that floating-point values are finite". Owner: CODE.16 (PRIME.4).

**F4. "Public interface" is now two meanings.** The CODE row for Untrusted input defines "the public interface of the work" by documentation or configuration; STND.PY, STND.RUST, and STND.FTN keep a Term "Public interface" by construct, and PY uses it for docstrings (library code only). Fix: in the CODE row call the first notion "the interface for outside use" and say "together with each function that the standard of its language places in its public interface"; P2 and P3 keep their Terms unchanged in meaning.

**F5. FTN external procedures (conflict if kept).** `code-interface.md` tells P3 to keep "excluding external procedures". The CODE term is a union: a documented external procedure is in the interface under CODE and out under FTN. The STDC Notes give the reason it is unneeded (documentation or configuration names the interface). Fix: P3 drops the exclusion.

**F6. Restatement by the language standards.** PY.22 s1, JL.15 s1, RUST.13 s1, FTN.29, and LEAN.25 restate CODE.14 (GOV.31). FTN.18 (SHOULD NOT) restates CODE.16 s3 (SHALL NOT) at a weaker mode, and the FTN Notes sentence "no binding provision rests on the hazard" is now false. RUST.14 restates CODE.15 with a wider trigger (any check that reports an ignored value, which CODE.15 excludes). PY.25, JL.13, RUST.15 s1, and FTN.31 are language forms and stand. Fix for P2 and P3: replace each first sentence by a citation plus the language mechanism ("an exception is the mechanism of passing"); withdraw FTN.18; cut RUST.14 to its delta or cite CODE.15; keep PY.22 s2-s3 and JL.15 s2 as ruled (decision 7).

**F7. The NDEBUG reasoning is stated three times** (CODE Notes, CXX Notes on CODE.16, STDC Notes). Fix: keep the CODE Notes; in CXX and STDC keep only the language fact (the header that `assert` comes from, the options) and cite it.

**F8. CXX Notes on STND.JL.34 and STND.RUST.20 are inexact.** They say Julia "checks each index in every build unless code removes the check". The JL Notes record that `--check-bounds=no` removes `@boundscheck` checks globally. The "no change" holds for another reason: JL.13 s3 keeps an untrusted index check unremovable, and JL.34 s1 runs the tests once under the production setting. Fix: state that reason and record it with the custodian's "no change".

**F9. STND.CXX.32 is not the exact counterpart of STND.RUST.13 s2.** RUST.13 binds only where the work replaces the hook, because the default hook prints (verified); CXX.32 binds unconditionally and rests on an unverified default. Pairs CXX 52-54 (HW.8, HDES.14, HW.GPU.3) are compatible. Fix: say in the Notes that it is stricter and why; add that for a program that commands hardware the handler enters the designed safe state (PRIME.13, HW.EMBED.4), the point of RUST Observation 3. List both as custodian decisions.

**F10. CODE.19 and hardware descriptions.** "compiler, interpreter, and library implementation" omits the synthesis and simulation tools that build or run HDL code, which CODE says it covers (pairs CODE 27-46). Fix: "each tool that compiles, synthesizes, interprets, or runs that code". CXX.2 sentence 2 (MAY use any supported later feature) has no carve-out for CODE.19 sentence 3 (that feature only); add "other than high-assurance code under STND.CODE.19".

**F11. STDC.** The Notes say CODE.14 "admits every response but an exception, which C does not have"; a nonlocal jump is a mechanism that propagates (STDC.31 s2). Fix: "but a C++ exception; STDC.31 governs the jump". STDC.31 s1 repeats STDC.2 for any failure; add "as STND.STDC.2 binds for a listed condition".

**F12. Widened reach (decision list).** The term now adds the arguments of documented functions: new for C, C++, Lean, and HDL; wider for PY (entry-point modules), RUST (binary crates), FTN (external procedures), JL (unexported). For C, STDC.21 asks a length "against the extent of the object", which a pointer argument does not carry; it can be met only where the contract states the extent or a limit (STDC.27). Fix: add that sentence to the STDC Notes. SV Purpose says it "adds nothing to that floor" and names HDES.14 and CONC only; P3 adds CODE.14 and CODE.16.

## Same-level pairs

| Language provision | Against STND.CODE | Verdict |
| --- | --- | --- |
| PY.22, JL.15 | .14 | Restate s1 (F6); later sentences narrow; no conflict |
| PY.25, JL.13 | .6, .16 | Forms of .6, wider in use; .16 adds CPS checks and F2, F3 to both; reach widened (F12); no conflict |
| RUST.13 | .14 | Restates s1; s2-s3 narrow; CXX.32 differs (F9) |
| RUST.14 | .15 | Restates with wider trigger (F6) |
| RUST.15 | .6, .16 | Form of both; its CPS part is .16 s1 (F6) |
| FTN.18 | .16 s3 | Restates at a weaker mode (F6) |
| FTN.29 | .14 | Restates (F6) |
| FTN.31 | .6, .16 | Form of .6; .16 s2 now reaches Fortran source with conditional compilation; term clash (F5) |
| LEAN.5, RUST.34, FTN.30 | .18, .7 | Different claims or unaffected |
| LEAN.25 | .14 | Restates (F6) |
| SV | .14-.16, .19 | Widened: binds HDL; SV.13 and SV.19 do not conflict; SV.1 compatible with .19; F10, F12 |
| BUILD.11 | .16 s3 | Compatible: states the option, .16 forbids it for check code |
| BUILD.12, .13 | .6, .16 | Compatible; BUILD Notes still cite CXX.18 (P5) |
| CXX.2, .3 | .19 | Compatible; F10 |
| CXX.8 (table), .21, .22 | .17, .15, .14 | Cite, do not restate; compatible |
| CXX.27 | .6 | Compatible: Notes call library checks a second layer; a library check that is the only check of an untrusted argument cannot be budgeted out |

## C reading, STDC.1 and STDC.2 against STND.CODE

- The ten kept rows (CXX.4, 7, 9, 12, 15, 23, 24, 25, 26, 27) cite no withdrawn identifier; the Instantiates list equals their union; withdrawn identifiers appear in STDC only in the Revision History.
- STDC.2 narrows CODE.14 for C (no report through errno alone); it is binding and rests on PRIME.4. Consistent.
- CODE.6 and .16 reach the assert macro (option or source `#define`); the Notes say so, but see F7.
- CODE.15 and STDC.29 agree: STDC.29 is wider (library functions) and conditioned.
- STDC.1 adds no floor. STDC.39 matches LEAN.27 and NUMER.4; compatible.
- Findings that touch C: F2, F3, F7, F11, F12.

## Coverage table

Every row below: conflict no, unowned no, restatement no, except as the Note says. Script check: every listed pair read from the three `pairs-*.md` files once, numbers 1-90, 1-38, 1-63 contiguous with no repeat or gap, 191 in all, each assigned to exactly one row.

**STND.CODE** (90 pairs)

| Changed provision | Group of the other document | Pairs | Count | Note |
| --- | --- | --- | --- | --- |
| STND.CODE.14 | HDES | 1 | 1 | intersection with HDES.14 (status at interface) |
| STND.CODE.14 | HW | 2 | 1 | HW.8 narrows to its three; compatible by intersection |
| STND.CODE.14 | HW.GPU | 3 | 1 | as HW.8; compatible |
| STND.CODE.15 | HDES | 4 | 1 |  |
| STND.CODE.15 | HW | 5 | 1 |  |
| STND.CODE.15 | HW.GPU | 6 | 1 |  |
| STND.CODE.16 | CPS | 7-8 | 2 | F2, F3 (same-level) |
| STND.CODE.16 | HDES | 9 | 1 |  |
| STND.CODE.16 | HW | 10 | 1 |  |
| STND.CODE.16 | HW.GPU | 11 | 1 |  |
| STND.CODE.16 | ML | 12 | 1 |  |
| STND.CODE.17 | AGENT | 13 | 1 |  |
| STND.CODE.17 | NUMER | 14-16 | 3 |  |
| STND.CODE.18 | AGENT | 17-20 | 4 |  |
| STND.CODE.18 | NUMER | 21 | 1 |  |
| STND.CODE.19 | AGENT | 22-23 | 2 |  |
| STND.CODE.19 | CPS | 24-26 | 3 |  |
| STND.CODE.19 | HDES | 27-34 | 8 | F10 |
| STND.CODE.19 | HDES.ASIC | 35-44 | 10 | F10 |
| STND.CODE.19 | HDES.FPGA | 45-46 | 2 | F10 |
| STND.CODE.19 | HW | 47-52 | 6 |  |
| STND.CODE.19 | HW.ASIC | 53 | 1 |  |
| STND.CODE.19 | HW.EMBED | 54-55 | 2 |  |
| STND.CODE.19 | HW.FPGA | 56 | 1 |  |
| STND.CODE.19 | HW.QPU | 57-59 | 3 |  |
| STND.CODE.19 | ML | 60-61 | 2 |  |
| STND.CODE.19 | NUMER | 62-80 | 19 |  |
| STND.CODE.20 | AGENT | 81 | 1 |  |
| STND.CODE.20 | NUMER | 82-84 | 3 |  |
| STND.CODE.6 | CPS | 85-86 | 2 |  |
| STND.CODE.6 | HDES | 87 | 1 |  |
| STND.CODE.6 | HW | 88 | 1 |  |
| STND.CODE.6 | HW.GPU | 89 | 1 |  |
| STND.CODE.6 | ML | 90 | 1 |  |

**STND.STDC** (38 pairs)

| Changed provision | Group of the other document | Pairs | Count | Note |
| --- | --- | --- | --- | --- |
| STND.STDC.1 | AGENT | 1-2 | 2 |  |
| STND.STDC.1 | CPS | 3-4 | 2 |  |
| STND.STDC.1 | HDES | 5-7 | 3 |  |
| STND.STDC.1 | HDES.ASIC | 8 | 1 |  |
| STND.STDC.1 | HDES.FPGA | 9 | 1 |  |
| STND.STDC.1 | HW | 10-17 | 8 |  |
| STND.STDC.1 | HW.ASIC | 18 | 1 |  |
| STND.STDC.1 | HW.CPU | 19-20 | 2 |  |
| STND.STDC.1 | HW.FPGA | 21 | 1 |  |
| STND.STDC.1 | HW.GPU | 22 | 1 |  |
| STND.STDC.1 | HW.QPU | 23-24 | 2 |  |
| STND.STDC.1 | ML | 25-26 | 2 |  |
| STND.STDC.1 | NUMER | 27-34 | 8 |  |
| STND.STDC.2 | HDES | 35 | 1 | F11 |
| STND.STDC.2 | HW | 36 | 1 | F11 |
| STND.STDC.2 | HW.GPU | 37 | 1 | F11 |
| STND.STDC.39 | NUMER | 38 | 1 |  |

**STND.CXX** (63 pairs)

| Changed provision | Group of the other document | Pairs | Count | Note |
| --- | --- | --- | --- | --- |
| STND.CXX.2 | HDES | 1 | 1 |  |
| STND.CXX.2 | ML | 2 | 1 |  |
| STND.CXX.2 | NUMER | 3 | 1 |  |
| STND.CXX.21 | CPS | 4-6 | 3 |  |
| STND.CXX.21 | HDES | 7-12 | 6 |  |
| STND.CXX.21 | HDES.ASIC | 13-16 | 4 |  |
| STND.CXX.21 | HDES.FPGA | 17-18 | 2 |  |
| STND.CXX.21 | HW | 19-24 | 6 |  |
| STND.CXX.21 | HW.CPU | 25 | 1 |  |
| STND.CXX.21 | HW.EMBED | 26 | 1 |  |
| STND.CXX.21 | NUMER | 27 | 1 |  |
| STND.CXX.22 | CPS | 28-30 | 3 |  |
| STND.CXX.22 | HDES | 31-36 | 6 |  |
| STND.CXX.22 | HDES.ASIC | 37-40 | 4 |  |
| STND.CXX.22 | HDES.FPGA | 41-42 | 2 |  |
| STND.CXX.22 | HW | 43-48 | 6 |  |
| STND.CXX.22 | HW.CPU | 49 | 1 |  |
| STND.CXX.22 | HW.EMBED | 50 | 1 |  |
| STND.CXX.22 | NUMER | 51 | 1 |  |
| STND.CXX.32 | HDES | 52 | 1 | F9 |
| STND.CXX.32 | HW | 53 | 1 | F9 |
| STND.CXX.32 | HW.GPU | 54 | 1 | F9 |
| STND.CXX.8 | AGENT | 55 | 1 |  |
| STND.CXX.8 | HW | 56 | 1 |  |
| STND.CXX.8 | HW.CPU | 57 | 1 |  |
| STND.CXX.8 | HW.GPU | 58 | 1 |  |
| STND.CXX.8 | HW.QPU | 59 | 1 |  |
| STND.CXX.8 | NUMER | 60-63 | 4 |  |
