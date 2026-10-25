# From P1 to P2 and P3, through the lead (2026-10-25)

P1 0.2 resolves these items in the language standards. Each is in your package's documents, so P1 does not edit them. The IDs are those of `code-interface.md` 0.2.

## Restatements of STND.CODE (pair review F6)

| Provision | Restates | Suggested change | Package |
| --- | --- | --- | --- |
| STND.PY.22 s1 | STND.CODE.14 | Cite STND.CODE.14 and name the Python mechanism (an exception is the pass to the caller). Keep s2 and s3 as ruled (decision 7). | P2 |
| STND.JL.15 s1 | STND.CODE.14 | As PY.22. Keep s2 as ruled. | P2 |
| STND.RUST.13 s1 | STND.CODE.14 | Cite STND.CODE.14 and name panic as the mechanism. Keep s2 and s3. | P3 |
| STND.FTN.29 | STND.CODE.14 | Cite STND.CODE.14 and keep the status argument as the Fortran form. | P3 |
| STND.LEAN.25 | STND.CODE.14 | Cite STND.CODE.14 and keep the forms of Lean (a result type, a monad error). | P3 |
| STND.RUST.14 | STND.CODE.15 | Its trigger is wider: any compiler or static check that diagnoses an ignored value. Cut it to its delta and cite STND.CODE.15, or keep it as the wider Rust form and say so in the Notes. | P3 |
| STND.FTN.18 | STND.CODE.21 (default) | Same mode now. Cite STND.CODE.21, or withdraw STND.FTN.18. The Notes sentence on STND.CXX.18 stays true. | P3 |
| STND.PY.25, STND.JL.13, STND.RUST.15 s1, STND.FTN.31 | forms of STND.CODE.6 and .16 | Stand as language forms. RUST.15's CPS part may cite STND.CODE.16 s1. | P2, P3 |

## Other items

1. **Fortran external procedures (F5).** Drop the exclusion of external procedures from the reach of Untrusted input. A documented one is in the interface for outside use under STND.CODE. The STND.CODE Notes list this widening as a decision for the custodian. (P3)
2. **The term's wording (F4).** STND.CODE now says "interface for outside use", and "places in its public interface" for the language clause. PY, RUST, and FTN keep their Public interface Terms in meaning. Wherever you write "the public interface of the work under the term Untrusted input", write "the public interface that the term Untrusted input of STND.CODE takes in". The term now defines "function" to include procedures, subroutines, and methods, so FTN may drop "a procedure is a function". (P2, P3)
3. **Newest edition against STND.CODE.19 (cold item 5).** Add to the body of STND.JL.1 and STND.PY.14 the clause "other than for an edition that STND.CODE.19 fixes", as STND.CXX.2 has. The STND.CODE Notes no longer decide the conflict, and say each standard yields "where its own text says so". (P2)
4. **SV Purpose (F12).** It says the standard "adds nothing to that floor" and names HDES.14 and STND.CONC only. Add STND.CODE.14 and STND.CODE.16, which now reach hardware descriptions. (P3)
5. **Citations of withdrawn IDs.**
   - STND.CXX.16 and .17 in the FTN, LEAN, and RUST Notes: retarget to STND.CODE.14 and .15.
   - The RUST Notes citation of STND.CXX.18 for the checks of CPS.5 and CPS.9: retarget to STND.CODE.16 sentence 1.
   - Citations of STND.CXX.18 for the finite-value option (FTN, BUILD) stay valid. (P3; BUILD is P5)
6. **STND.JL.36 (P2's new default).** The STND.CXX 1.2 Notes describe it in words, as "the Julia standard holds in a default of its own the bounds checking of the production configuration", with no ID. CXX 1.2 is applied before JL.36 exists. (P2: information only)
