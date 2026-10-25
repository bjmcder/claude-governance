# Dispositions: P5, cold review

Review: review.md (no Defect). The lead made these changes.

| Finding | Disposition |
| --- | --- |
| Should-fix 1: the garbled clause "the Articles that the field instantiates of those provisions lists" in the rationales of HW.CPU, HW.EMBED, HW.QPU, HW.GPU | Accepted: "the `instantiates` fields of those provisions list" (HW.GPU: "the `instantiates` field of HW.GPU.4 lists"). |
| Should-fix 2: the STND.DFLT rationale glosses STND.INSTR.4 and .5 differently from the Notes | Accepted: "which hold the shell guards and dry runs that the Notes assign to STND.INSTR". |
| Optional 1: the loose "them" in STND.CLASS | Accepted: "The table holds no part of Simplicity (SIMPL)." |
| Optional 2: "which the sub-profiles each give one of" in HW.1 | Kept, for parity with HDES. |
| Optional 3: "its tag vocabulary (TAG)" in STND.KNOW | Accepted: "the tag vocabulary of that corpus (TAG)". |

## STND.BUILD 1.0.2: cold review

Review: `../reconciliation-records.md`, item B1. Reviewer C of the reconciliation review read STND.BUILD 1.0.2 as a cold reviewer, and that read is its cold review. It found the class right (editorial), the change confined to the Notes with every provision as it was, and the rationale in agreement with the document. No Defect; one Should-fix (S1).

| Finding | Disposition |
| --- | --- |
| S1: the Notes name only STND.CXX.18 as binding the finite-value rule ("for C++"), and state the default STND.CODE.21 in the indicative ("has code ... not compiled") | Accepted. Both sentences add STND.STDC.40 for C ("which STND.CXX.18 binds for C++ and STND.STDC.40 for C"; "STND.CXX.18 and STND.STDC.40 keep it from such C++ and C code"), which derives the STND.STDC row of References. The first sentence now reads "STND.CODE.21 advises against compiling code that holds a check ...". The history row 1.0.2 and the rationale say so. |

STND.BUILD 1.0.2 applies after package P1, which adds STND.CODE.21 and STND.STDC.40. `apply_close_p5_build.py` rehearses it that way, and the lead orders it at the coalesce.

## Pair review

No STND.HARN.28 pair review applies to P5. Not one of the 15 amendments (the 14 documents of `gaps.md` and STND.BUILD) changes a provision: every edit is to informative text, and the bodies, modes, `instantiates`, and `refers_to` of every provision stay as they were. So no new pair of provisions arises to review.

## Verification after these fixes

- `apply_close_p5.py` (entries 148 to 161) and `apply_close_p5_build.py` (P1, then STND.BUILD) both rehearse on top of entry 147. `verify` passes every family, with one g.18 warning that entry 147 also has.
- The drafting findings on the 14 documents are the same as at entry 147, with none of class defect. STND.BUILD has no finding.
- `check_refs.py` reports no missing row for the 14 documents or for STND.BUILD.
- `STND.CLASS.md`, `STND.KNOW.md`, and `STND.BUILD.md` in this directory are recomposed from these rehearsals (S2). Their entry numbers are those of the rehearsals.
