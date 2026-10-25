# P1 interface: what STND.CODE 1.2 holds for the P2 and P3 drafters (revision 0.3)

Status: revised after the cold review, the pair review, and the verification of 0.2 (2026-10-25); see `dispositions.md`. Source: `tools/amendment-scripts/apply_code_1_2.py`. Apply P1 first; `apply_close_p1.py` runs STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2 in that order. The texts below are copied from the rehearsed copy.

## Changes from 0.2

Changes after the verification of 0.2 (`verify-0.2.md`).

| ID | Change | What a citer does |
| --- | --- | --- |
| **STND.CODE.14** | **Text change.** The pass to the caller now reads "in its result, in an argument that the caller passes to receive it, or by a mechanism of its language, an exception among them, that propagates the condition to the caller". This names the status argument of FTN.29 (P3's O5) and widens the permission. | **P2 and P3:** where a first sentence is restated or cited, cite this whole clause. A Fortran status argument, a Rust panic, an exception of Python or Julia, and an error of a Lean monad all fall within it. |
| STND.CODE Notes | Two changes. The Notes no longer say that STND.CODE.14 asks the end of a program to carry a diagnosis; PRIME.4 states that outcome (S1). The NDEBUG fact is stated for C, with C++ marked unverified (S2, O1). | None. |
| STND.CXX.33 (new) | A default from CSQ1 (INTPR.8). Where the implementation's terminate handler writes no diagnosis of a listed condition, the program installs a handler or catches the exception in its entry point (S1). It is outside the binding STND.CXX.32. | None. |
| STND.STDC.40 | Restated in C words: "A translation unit of C source ... SHALL NOT be compiled with an option that lets the compiler assume that floating-point values are finite". It now instantiates PRIME.4, DSGN.2, CPS.5, and CPS.9, refers to STND.CODE.6 and STND.CODE.21, and no longer refers to STND.CXX.18 (O5). The STDC Floor states the C hazard (S3). | None. |
| STND.CODE.15, .16, .17 to .21, term | Unchanged since 0.2. | None. |

## Changes from 0.1

| ID | Change | What a citer does |
| --- | --- | --- |
| Term Untrusted input | Three changes: "public interface of the work" is now "interface for outside use"; the language clause reads "places in its public interface"; and "function" now includes procedure, subroutine, method, and other callable units. | P2 and P3 keep their own Public interface Terms unchanged in meaning. FTN can drop "a procedure is a function". FTN drops the exclusion of external procedures, because a documented one is in the interface (pair F5). |
| STND.CODE.14 | Text change. "in a result that the contract of the code names for it" was dropped (F1). The pass to the caller is "in its result or by a mechanism of its language that propagates it". | None needed. P2 relied on the outcome, not on the dropped clause. |
| STND.CODE.16 | Narrowed and split. Sentence 1 (CPS.5 and CPS.9) is unchanged. Sentence 2 now reads "a definition that the source of the work gives to conditional compilation". The old sentence 3 (finite-value options) is removed and becomes STND.CODE.21. | Citations of "the first sentence of STND.CODE.16" stand. Retarget citations of the finite-value sentence to STND.CODE.21. |
| STND.CODE.19 | Text change. The toolchain is now "each tool that compiles, synthesizes, interprets, simulates, or runs that code, and each library implementation that the code uses", so hardware descriptions are covered. | None. |
| **STND.CODE.21 (new)** | Finite-value assumptions near checks. A **default** (DSGN.2, from CSQ3) covering an execution setting and an annotation in the source (Julia `@fastmath`). | STND.FTN.18 now states the same default for Fortran, with the annotation left out. P3 may cite STND.CODE.21 from it, or withdraw it. The FTN Notes sentence on CXX.18 stays true. |
| STND.CODE.6, .15, .17, .18, .20 | Unchanged since 0.1. | None. |

Changes outside STND.CODE that touch citers:
- **STND.CXX.18 is no longer withdrawn.** It keeps its second sentence only: the binding C++ form of CODE.21, as ruled. The BUILD and FTN Notes that cite CXX.18 for the finite-value option stay correct. The first sentence of CXX.18 is now CODE.16 sentence 1.
- Withdrawn from STND.CXX: .16, .17, .28, .29, .30, .31.
- STND.CXX.32 is now conditioned, as RUST.13 sentence 2 is: "Where the work installs a terminate handler".
- New STND.STDC.40 (binding) applies the C reading of STND.CXX.18 to C.

## The term

| Untrusted input | Data that reaches the work from outside its own code, the arguments of each function of its interface for outside use included, other than data from a source that the threat model of the project records as trusted. The interface for outside use of the work is each function that its documentation or its repository configuration names for use by code outside the work, together with each function that the standard of the language of that function places in its public interface. A function, in this term, is a function, procedure, subroutine, method, or other unit of code that a call enters. |

- Import it as "Untrusted input has the meaning that STND.CODE gives it".
- Keep, as a Term or a sentence of your own, what places functions in your language's public interface: PY's Public interface, JL's `export` and `public`, RUST's library crate, FTN's module-public and BIND procedures.
- JL's sentence on `eachindex`, `axes`, and `CartesianIndices` stays in STND.JL as Julia content.
- The documentation clause widens each language. The custodian decides that widening (see the STND.CODE Notes).

Other new terms in STND.CODE: High-assurance code, High-assurance coding standard. STND.CODE imports Safety-related component from STND.CLASS.

## New and changed provisions of STND.CODE

### STND.CODE.6 Unremovable input checks

Binding. Instantiates PRIME.4, DSGN.2. Section: Failures.

A check that rejects invalid untrusted input where that input enters SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2).

### STND.CODE.14 Responses to listed failures

Binding. Instantiates PRIME.4. Refers to PRIME.13. Section: Failures.

Where code detects a condition that PRIME.4 lists, it SHALL halt with a diagnosis, enter the designed safe state of PRIME.13 of the hardware that it commands, degrade visibly with a diagnosis, or pass the condition to its caller, in its result, in an argument that the caller passes to receive it, or by a mechanism of its language, an exception among them, that propagates the condition to the caller (PRIME.4).

### STND.CODE.15 Ignored failure results diagnosed

Binding. Instantiates PRIME.4. Section: Failures.

Where the language, or a compiler or a static check among the means of the work, provides a form of declaration for a function, or for the type of its result, under which each call that ignores that result is diagnosed, each function of the work that returns a failure of a kind that PRIME.4 lists SHALL be declared in such a form (PRIME.4).

### STND.CODE.16 Required checks in every build

Binding. Instantiates PRIME.4, DSGN.2, CPS.5, CPS.9. Refers to STND.CODE.6. Section: Failures.

Where CPS.5 or CPS.9 applies to the work, each check that it requires, with its response, SHALL NOT be removable by an execution setting (PRIME.4, DSGN.2, CPS.5, CPS.9). A check that STND.CODE.6 or the first sentence of this provision governs SHALL NOT be written in a form that a definition that the source of the work gives to conditional compilation turns off (PRIME.4, DSGN.2).

### STND.CODE.17 Adopted high-assurance coding standard

Default. Instantiates DSGN.3, REPRO.7. Section: High assurance.

The high-assurance code of each safety-related component of work of CSQ0 SHALL conform to a high-assurance coding standard for its language that a decision record of the work adopts, the record naming the standard, its revision, and its deviation procedure (DSGN.3, REPRO.7). Other high-assurance code SHOULD conform to a high-assurance coding standard for its language that a decision record of the work so adopts (DSGN.3, REPRO.7).

### STND.CODE.18 High-assurance conformance claims

Binding. Instantiates PRIME.2. Section: High assurance.

Each claim that high-assurance code conforms to its high-assurance coding standard SHALL state each means by which that conformance was checked and the rules that each means covered (PRIME.2). A claim of conformance SHALL NOT extend beyond the rules that those means checked (PRIME.2).

### STND.CODE.19 High-assurance language edition

Default. Instantiates DSGN.3, VV.1, REPRO.7. Refers to STND.CODE.17. Section: High assurance.

Other than for a feature that a decision record admits under this provision, the high-assurance code of each safety-related component of work of CSQ0 SHALL be compiled or run at an edition of its language that its high-assurance coding standard covers, and for which each tool that compiles, synthesizes, interprets, simulates, or runs that code, and each library implementation that the code uses, has the validation or qualification that the decision record of STND.CODE.17 states the work requires (DSGN.3, VV.1). Other high-assurance code SHOULD be compiled or run at such an edition (DSGN.3). Where a decision record states, for one feature of a later edition, why the high-assurance coding standard and the validation of the toolchain still give the evidence on which the work relies, high-assurance code MAY use that feature and no other feature of that edition (REPRO.7).

### STND.CODE.20 Recorded high-assurance deviations

Default. Instantiates REPRO.7. Refers to STND.CODE.17. Section: High assurance.

Each deviation from a rule of the high-assurance coding standard of STND.CODE.17 SHALL be recorded as the deviation procedure of that standard requires, at its location under one marker that the repository configuration names or in a decision record that the location cites, with the identifier of the rule, the reason, and the evidence that the code stays correct (REPRO.7).

### STND.CODE.21 Finite-value assumptions near checks

Default. Instantiates DSGN.2. Refers to STND.CODE.6, STND.CODE.16. Section: Failures.

Code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs SHOULD NOT be compiled under an execution setting that, by the documentation of its compiler, lets the compiler assume that floating-point values are finite (DSGN.2). Such code SHOULD NOT carry an annotation in its source that, by its documentation, lets the compiler assume that floating-point values are finite in the code that holds the check (DSGN.2).


STND.CODE.6 changed only in wording: "invalid input where untrusted data enters" became the term.

## Identifiers

| Old | Becomes |
| --- | --- |
| STND.CXX.16 | withdrawn; STND.CODE.14 |
| STND.CXX.17 | withdrawn; STND.CODE.15 |
| STND.CXX.18 | kept. Sentence 1 moves to STND.CODE.16 sentence 1. Sentence 2 stays, binding, citing STND.CODE.21. |
| STND.CXX.28 to .31 | withdrawn; STND.CODE.17 to STND.CODE.20 |
| STND.CXX.32 (new) | Diagnoses from terminate handlers (binding, conditioned on a handler that the work installs) |
| STND.STDC.2 | kept, retitled C responses to listed failures (errno rule) |
| STND.STDC.39 (new) | C naming conventions |
| STND.STDC.40 (new) | Finite-value options in C (binding; CXX.18's rule in C words) |
| STND.CXX.33 (new) | Terminate handlers where defaults are silent (default, from CSQ1) |

## What P2 and P3 still need to do

See `for-p2-p3.md`. In short:
- restatements to replace by citations (pair F6);
- the FTN exclusion of external procedures (F5);
- a body clause in JL.1 and PY.14 that yields to STND.CODE.19 (cold item 5);
- the SV Purpose (F12);
- retargets of citations of the withdrawn IDs:
  - STND.CXX.16 and .17 in the FTN, LEAN, and RUST Notes;
  - a RUST Notes citation of STND.CXX.18 for the checks of CPS.5 and CPS.9, which now goes to STND.CODE.16 sentence 1;
  - citations of STND.CXX.18 for the finite-value option stay valid.
