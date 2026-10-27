# Review A, round of 2026-10-27: STND.CODE 1.3, STND.DEPS 1.1, STND.STDC 1.2, STND.CXX 1.3, editorial STND.FTN, STND.MPI, STND.OMP

## Verified by running

- Rehearsal of `apply_round_2026_10_27.py` exits 0. On a kept copy (entries 188 to 197), `verify` passes every check; the only warning is the g.18 warning the corpus already carries (it now lists STND.CODE.24, which has three modals).
- Grep of the copy: no citation of STND.CXX.20, .22, STND.STDC.36, STND.PY.33, .34, .36, .37, STND.JL.4, .37, .40, .41 remains outside revision rows and the field `withdrawn`. No "foreign function interface" remains. The term Foreign interface is defined once (STND.CODE) and Lock file once (STND.DEPS). Every `govharness pairs` row for STND.CODE.22 to .26 and STND.DEPS.12 (44) equals the 44 rows of `pairs-changed.md` for them.
- Onsets checked against STND.CLASS.10: DSGN.4 and DSGN.5 from CSQ2, DSGN.14 on no row, so CSQ3. Correct for STND.CODE.22 to .26 and STND.DEPS.12.
- Pairs read: HW.13, HW.14, HDES.5, NUMER.5 address the layout and ownership of what crosses a boundary; STND.CODE.22, .23, .25 add the software side. No conflict. HW.14 asks a check on each crossing or a build record, which STND.CODE.22's "by a test" does not replace; they stay consistent because STND.CODE.22 is a minimum. CPS.3, CPS.4, CPS.8, HDES.12, HW.18 (STND.CODE.24) and HDES.3, HW.3, MEAS.4, ML.3 (STND.DEPS.12) address other matters. No other adopted document addresses lock files.

## Defect

None found.

## Should-fix

1. **The structured block drags STND.CODE.22, .23, .25, .26 onto every parallel region.** Text at fault, the term: "and a structured block of a compiler directive for parallel execution are foreign interfaces." Data and resources that cross a block have no "contract of the interface" that fixes size, strides, or an owner, so STND.CODE.22, .23, .25 are undecidable there. The old terms of STND.CXX and STND.STDC served only the exception rule (STND.CXX.22). Replacement: end the term at "...are foreign interfaces." with "A function that the work declares for such code or loads from it, a function of the work that such code invokes, and a thread that a runtime of such code starts in code of the work are foreign interfaces." Then STND.CODE.24, first sentence: "...each failure raised in code of the work that the interface invokes, or in a structured block of a compiler directive for parallel execution, and propagated by a mechanism of the language of that code, ..." Rationale 188, 193, 197 then say "the structured block among the constructs of STND.CODE.24". If the custodian wants the block in the term (the brief assumes so), see the question below.

2. **Term reaches calls between processes.** Text: "calls, or is called by, code that does not follow the rules of that language ..., code written in another language among it." A subprocess or a network service in another language is "code written in another language", though the old terms (STND.PY, STND.JL, STND.RUST) meant calls inside one process. Replacement for the first sentence: "An interface through which code of the work in one language calls, or is called by, code in the same process that does not follow the rules of that language for ownership, lifetime, and the propagation of failures, code written in another language among it."

3. **Notes claim that bundles are not applied apart, yet they are.** STND.CODE Notes: "STND.CODE.25 gives each resource that crosses one owner ... its two sentences are one rule for one resource." The first sentence of STND.CODE.25 applies to a resource that the interface does not create, where the second does not. Same for the second sentence of STND.CODE.22 (a type with no declared layout). Replacement: "The second sentence of STND.CODE.25 applies to a resource that the interface creates, the first to every resource that crosses; neither is applied without the first. The second sentence of STND.CODE.22 applies to a layout that the work declares, and is not applied without the first."

4. **Rationales understate the widening for C.** 193: "STND.CODE.23, which keeps the order of dimensions and the origin of indexes in the contract and admits a test of the call". STND.CODE.23 also asks the element type and the strides, and reaches arrays of one dimension (STND.STDC.36 asked only arrays of more than one); STND.CODE.22 adds the alignment and the compared layouts. Add to 193: "STND.CODE.22 and STND.CODE.23 ask C source more than STND.STDC.36 did: the alignment, the compared layouts of a structure, the element type and the strides of an array, and arrays of one dimension." Add to 188's list of what is asked more: "in C, C++, and Rust, the arrays of STND.CODE.23, with the element type and the strides".

5. **STND.STDC Purpose omits the rules that C still holds.** STND.CXX Purpose adds "and the rules of each foreign interface (STND.CODE.22 to STND.CODE.26)"; STND.STDC Purpose ends "and recorded deviations (... and STND.CODE.20)." with STND.STDC.36 gone. Replacement: "...and STND.CODE.20), and the rules of each foreign interface (STND.CODE.22 to STND.CODE.26)." (add the `refers_to` entries).

6. **Indicative obligation and a wrong citation in the STND.CODE Notes.** Text: "the C, Fortran, and Lean source of the work, and a hardware description, take them for each foreign interface that they declare, beside what STND.STDC, STND.FTN, and STND.LEAN state of their own." STND.LEAN holds no provision on a foreign interface (its Notes say the foreign code is governed by its own standard). Replacement: "STND.CODE.22 to STND.CODE.26 apply to the C, Fortran, and Lean source of the work, and to a hardware description, for each foreign interface that it declares, beside what STND.FTN.27 and STND.FTN.28 state."

## Optional

7. STND.CODE.25 loses the explicit prohibition of STND.CXX.20 on releasing a resource "that the foreign interface predefines". Rationale 197 rests it on "released only by that owner", which holds only if the library is the stated owner of a predefined handle. Consider adding to the Notes: "A resource that the interface predefines has the interface as its owner."
8. STND.PY.34 asked the Python source to declare the type of each argument (ctypes). STND.CODE.22 asks the size and representation but not the declaration. Reviewer B should confirm that the rationale of 194 says so.
9. STND.CODE.24, third sentence: "after the invocation returns" has no referent for a structured block (see 1). With 1 applied, replace "after the invocation returns" by "after the invocation or the block returns".
10. STND.CXX Terms restate the term in part: "a C or vendor library interface, and a callback or a thread that such a library or a runtime starts, are foreign interfaces". Acceptable under decision 1 (each standard names its constructs); STND.STDC names none, so consider "a callback, or a thread that a runtime of another language starts in C source".

## What the drafting decided (draft-status)

Custodian-bound: (a) STND.CODE.24 relaxes STND.CXX.22 and STND.JL.39 by the contract clause; (b) STND.CODE.25 adds the pass-to-owner for Python and Julia and for C, Fortran, Lean; (c) STND.DEPS.12 drops the MAY sentence that decision 3 states ("may leave its lock file uncommitted"). I judge (c) equivalent in effect, and the Notes say so. The five-provision split and the interrupt rules are consistent: STND.PY.35 and STND.JL.39 say "in place of its conversion", so they do not conflict with STND.CODE.24's second sentence.

## Question for the custodian

Should a structured block of a parallel directive stay in the one term Foreign interface (as the brief and the rationales assume), with STND.CODE.22, .23, .25, .26 then reaching every parallel region, or belong only to STND.CODE.24 (finding 1)?
