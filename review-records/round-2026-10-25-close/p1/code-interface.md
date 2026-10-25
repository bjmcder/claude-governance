# P1 interface: what STND.CODE 1.2 holds for the P2 and P3 drafters

Status: fixed for drafting (2026-10-25). Source: `tools/amendment-scripts/apply_code_1_2.py`. Rehearse it first, before any P2 or P3 script; `apply_close_p1.py` applies P1 in the order STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2. The texts below are copied from the rehearsed copy. If a reviewer's finding changes one of them, this file is updated and says so at the top.

## The term

STND.CODE Terms, new row (import it as "Untrusted input has the meaning that STND.CODE gives it"):

| Untrusted input | Data that reaches the work from outside its own code, the arguments of each function of the public interface of the work included, other than data from a source that the threat model of the project records as trusted. The public interface of the work is each function that its documentation or its repository configuration names for use by code outside the work, together with each function that the standard of the language of that function places in that interface. |

What this means for your standard:
- The last clause keeps the reach that your current definition gives. When you delete your own row, keep what places functions in the public interface, as a Term or a sentence of your own, so that the reach stays the same. Examples: STND.PY's term Public interface (`__all__` and leading underscores, library code); STND.JL's `export` and `public`; STND.RUST's public interface of a crate of library code; STND.FTN's module-public procedures and BIND procedures, excluding external procedures. Do not define "Public interface" again where STND.PY already defines it.
- STND.JL's second sentence, about an index that `eachindex`, `axes`, or `CartesianIndices` produces being valid by construction, is Julia content. Keep it as a sentence of your own, in Notes or Terms.
- STND.CODE.6 now reads "invalid untrusted input where that input enters", so it uses the term.

Two other new terms in STND.CODE, for every language: **High-assurance code** (code that a release of work of CSQ1 or CSQ0 delivers, or runs to produce a reported result, with each file that it includes or imports; tests, development tools, and incorporated external code are excluded) and **High-assurance coding standard** (a coding standard for a language of the work, written for safety-related or mission-critical software, published or the work's own, with a deviation procedure). STND.CODE imports Safety-related component from STND.CLASS.

## New and changed provisions of STND.CODE

### STND.CODE.6 Unremovable input checks

Binding. Instantiates PRIME.4, DSGN.2. Section: Failures.

A check that rejects invalid untrusted input where that input enters SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2).

### STND.CODE.14 Responses to listed failures

Binding. Instantiates PRIME.4. Refers to PRIME.13. Section: Failures.

Where code detects a condition that PRIME.4 lists, it SHALL halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, degrade visibly with a diagnosis, or pass the condition to its caller, in a result that the contract of the code names for it or by a mechanism of its language, an exception among them, that propagates the condition to the caller (PRIME.4).

### STND.CODE.15 Ignored failure results diagnosed

Binding. Instantiates PRIME.4. Section: Failures.

Where the language, or a compiler or a static check among the means of the work, provides a form of declaration for a function, or for the type of its result, under which each call that ignores that result is diagnosed, each function of the work that returns a failure of a kind that PRIME.4 lists SHALL be declared in such a form (PRIME.4).

### STND.CODE.16 Required checks in every build

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9. Refers to STND.CODE.6. Section: Failures.

Where CPS.5 or CPS.9 applies to the work, each check that it requires, with its response, SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2, CPS.5, CPS.9). A check that STND.CODE.6 or the first sentence of this provision governs SHALL NOT be written in a form that a definition in the source of the work turns off (PRIME.4, DSGN.2). Code that holds a check of a floating-point value that STND.CODE.6 or this provision governs SHALL NOT be compiled under an execution setting that, by the documentation of its compiler, lets the compiler assume that floating-point values are finite (PRIME.4).

### STND.CODE.17 Adopted high-assurance coding standard

Default. Instantiates DSGN.3, REPRO.7. Section: High assurance.

The high-assurance code of each safety-related component of work of CSQ0 SHALL conform to a high-assurance coding standard for its language that a decision record of the work adopts, the record naming the standard, its revision, and its deviation procedure (DSGN.3, REPRO.7). Other high-assurance code SHOULD conform to a high-assurance coding standard for its language that a decision record of the work so adopts (DSGN.3, REPRO.7).

### STND.CODE.18 High-assurance conformance claims

Binding. Instantiates PRIME.2. Section: High assurance.

Each claim that high-assurance code conforms to its high-assurance coding standard SHALL state each means by which that conformance was checked and the rules that each means covered (PRIME.2). A claim of conformance SHALL NOT extend beyond the rules that those means checked (PRIME.2).

### STND.CODE.19 High-assurance language edition

Default. Instantiates DSGN.3, VV.1, REPRO.7. Refers to STND.CODE.17. Section: High assurance.

Other than for a feature that a decision record admits under this provision, the high-assurance code of each safety-related component of work of CSQ0 SHALL be compiled or run at an edition of its language that its high-assurance coding standard covers, and for which each compiler, interpreter, and library implementation that builds or runs that code has the validation or qualification that the decision record of STND.CODE.17 states the work requires (DSGN.3, VV.1). Other high-assurance code SHOULD be compiled or run at such an edition (DSGN.3). Where a decision record states, for one feature of a later edition, why the high-assurance coding standard and the validation of the toolchain still give the evidence on which the work relies, high-assurance code MAY use that feature and no other feature of that edition (REPRO.7).

### STND.CODE.20 Recorded high-assurance deviations

Default. Instantiates REPRO.7. Refers to STND.CODE.17. Section: High assurance.

Each deviation from a rule of the high-assurance coding standard of STND.CODE.17 SHALL be recorded as the deviation procedure of that standard requires, at its location under one marker that the repository configuration names or in a decision record that the location cites, with the identifier of the rule, the reason, and the evidence that the code stays correct (REPRO.7).


STND.CODE.6 changed only in wording, from "invalid input where untrusted data enters" to the term. Its title, mode, and instantiates are unchanged.

## Withdrawn or redirected identifiers (P1)

| Old | Becomes | In |
| --- | --- | --- |
| STND.CXX.16 C++ responses to listed failures | withdrawn; STND.CODE.14 | STND.CXX 1.2 |
| STND.CXX.17 Failure results kept visible | withdrawn; STND.CODE.15 | STND.CXX 1.2 |
| STND.CXX.18 Checks no option removes | withdrawn; STND.CODE.16 | STND.CXX 1.2 |
| STND.CXX.28 High-assurance coding standard | withdrawn; STND.CODE.17 | STND.CXX 1.2 |
| STND.CXX.29 Conformance claims | withdrawn; STND.CODE.18 | STND.CXX 1.2 |
| STND.CXX.30 High-assurance language level | withdrawn; STND.CODE.19 | STND.CXX 1.2 |
| STND.CXX.31 High-assurance deviations | withdrawn; STND.CODE.20 | STND.CXX 1.2 |
| (new) STND.CXX.32 | the C++ counterpart of STND.RUST.13 sentence 2: a termination by an uncaught C++ exception that answers a listed condition delivers a diagnosis | STND.CXX 1.2 |
| STND.STDC.2 Binding C++ provisions applied to C | kept under a new title, "C responses to listed failures": a report through errno alone is not the result by which C code passes a listed condition under STND.CODE.14. Its table is removed. | STND.STDC 1.1 |
| STND.STDC.1 rows STND.CXX.28, .30, .31 | removed; STND.CODE.17, .19, and .20 apply to C directly | STND.STDC 1.1 |
| STND.STDC Terms "Untrusted input" | deleted; imported from STND.CODE | STND.STDC 1.1 |
| (new) STND.STDC.39 | C naming conventions, in the STND.LEAN.27 form (R18) | STND.STDC 1.1 |

## What P2 and P3 cite (suggestions; your package decides)

- **Responses.** STND.CODE.14 states the first sentence of STND.PY.22, STND.JL.15, STND.RUST.13, STND.FTN.29, and STND.LEAN.25 in language-neutral form. Their other sentences stand: the warning categories and the logger of PY.22, the levels of JL.15, and RUST.13 sentences 2 and 3. Decision 7 keeps PY.22 and JL.15 as ruled.
- **Ignored results.** STND.RUST.14 is the Rust form of STND.CODE.15. STND.CODE.15 asks nothing of Python, Julia, Fortran, Lean, or SystemVerilog until a per-function (or per-result-type) declaration form exists among the means of the work. STND.FTN.30 (status specifiers) is unaffected.
- **Removable checks.** STND.PY.25, STND.JL.13, STND.RUST.15, and STND.FTN.31 are forms of STND.CODE.6 and STND.CODE.16. STND.RUST.15's CPS.5 and CPS.9 part is the Rust form of STND.CODE.16's first sentence. For Python and Julia, STND.CODE.16 adds only the checks of CPS.5 and CPS.9, plus no check turned off by a definition in the source.
- **STND.FTN.18** (default, finite-value options) states for Fortran what the third sentence of STND.CODE.16 now binds in every language, with the same condition, "by the documentation of its compiler". P1 puts that sentence to the custodian as a floor decision. If the custodian keeps it, P3 may cite STND.CODE.16 from STND.FTN.18 or withdraw STND.FTN.18. The FTN Notes paragraph that says "no binding provision rests on the hazard; STND.CXX.18 binds the same sentence for C++" then needs rewording.
- **STND.BUILD Notes** (P5) cite STND.CXX.18 twice for the finite-value option. Cite STND.CODE.16 instead.
- **Citations to replace.** The following Notes cite IDs that STND.CXX 1.2 withdraws:
  - STND.FTN Notes: STND.CXX.16 ("in the form of STND.CXX.16") and STND.CXX.18. Cite STND.CODE.14 and STND.CODE.16.
  - STND.LEAN Notes: STND.CXX.16. Cite STND.CODE.14.
  - STND.RUST Notes: STND.CXX.17, STND.CXX.18, and STND.CXX.27. Replace the first two with STND.CODE.15 and STND.CODE.16. STND.CXX.27 stays.
  - The harness does not fail on a withdrawn ID in Notes, but the reconciliation review will flag it.
- **High assurance** now reaches every language through STND.CODE.17 to STND.CODE.20. They are defaults from CSQ1, and STND.CODE.18 is binding but reaches only high-assurance code. STND.FTN, STND.RUST, STND.LEAN, and STND.SV need no text unless they want a language note. STND.JL.1 (latest stable version) and STND.PY.14: STND.CODE.19 fixes the edition of high-assurance code where a language standard asks for the newest. STND.CXX.2 says so in its body; for JL.1, its qualified-revision clause is the nearest place, and the change is optional.
