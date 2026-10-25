# P3 dispositions: update to P1 0.2 (2026-10-25)

Source of the items: `p1/code-interface.md` 0.2 ("Changes from 0.1"), `p1/for-p2-p3.md`, the lead's directions, and `research/round-addenda/a2-language-facts.md` fact 5. Reading copies `<ID>-0.2.md`; the 0.1 copies stay as the earlier state.

| # | Item | Disposition |
| --- | --- | --- |
| 1 | STND.CODE.14 now "in its result" | No text change needed. RUST.13 Notes now name panic as the Rust mechanism that passes the condition to the caller (F6). FTN.29 keeps the status argument, LEAN.25 the result type and the monad error, each citing STND.CODE.14. |
| 2 | STND.CODE.16 split; sentence 2 narrowed to conditional compilation | Citations of "the first sentence of STND.CODE.16" (RUST Notes, RUST.15) stand. No P3 text rests on sentence 2. |
| 3 | New default STND.CODE.21; FTN.18 stays a default | FTN.18 kept as a default, as the lead directed, and now cites STND.CODE.21 in its body (refers_to and parenthesis). The FTN Notes keep the 1.0 sentence "STND.CXX.18 binds the same sentence for C++" and call FTN.18 the Fortran form of the first sentence of STND.CODE.21, stated per source file. The withdrawal of 0.1 is not made. |
| 4 | STND.CXX.18 no longer withdrawn | RUST: the CPS.5 and CPS.9 citation goes to STND.CODE.16 sentence 1. FTN: the finite-value citation of STND.CXX.18 stays. The history rows say so. |
| 5 | STND.CODE.19 names synthesis and simulation tools | SV Terms import High-assurance code. The SV Notes add STND.CODE.17 to STND.CODE.20 to the list of STND.CODE provisions that already apply to hardware descriptions, naming the validation of each tool that synthesizes or simulates them. |
| 6 | Term wording (F4) | RUST and FTN Terms read "is in the public interface that the term Untrusted input of STND.CODE takes in". FTN drops "a procedure is a function" and keeps "the values that a procedure receives through its dummy arguments are its arguments". |
| 7 | FTN external procedures (F5) | The Notes no longer exclude them. A documented external procedure is in the interface for outside use; one that nothing names is not. The floor paragraph argues the new reach. Decision for the custodian. |
| 8 | RUST.14 against STND.CODE.15 (F6) | Kept as ratified, as the wider Rust form. The Notes say so: its condition is any compiler or static check that diagnoses an ignored value, STND.CODE.15's is a form of declaration, which Rust provides, so for Rust the two ask one outcome. |
| 9 | SV Purpose (F12) | The floor sentence names STND.CODE.14 and STND.CODE.16 beside HDES.14 and STND.CONC.1 and .2, and still says this standard adds nothing to that floor. |
| 10 | Withdrawn IDs in Notes | None remain in the provisions or Notes of the four documents; they appear only in the history rows that record the retargeting. |
| 11 | a2 fact 5 (Rust case lints) | The RUST Notes cite a2 for the three lints and their kinds of item, say that the source names static items and not constants, and keep "the Rust project publishes a convention" unverified. The sources paragraph lists a2. |
| 12 | STND.CODE range in the Purposes | RUST and FTN cite "STND.CODE.14 to STND.CODE.21". |

Results: `rehearse governance apply_close_p3.py` appends 7 entries (seq 148 to 154) and every check passes; `findings.py` reports no defect for the four documents (only the eleven three-modal review notices carried from 1.0); `check_refs` reports 0 documents with missing rows for them.
