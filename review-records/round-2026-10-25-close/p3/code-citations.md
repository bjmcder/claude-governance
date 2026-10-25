# STND.CODE identifiers that P3 cites (revision 0.2)

Rehearsed against STND.CODE 1.2 as `p1/code-interface.md` 0.2 gives it. Each row gives the outcome cited, so that a later renumbering is retargeted by outcome.

| ID | Outcome cited | Where (body = provision text and `refers_to`) |
| --- | --- | --- |
| STND.CODE.6 | Input checks not removable by an execution setting | Body: STND.RUST.15, STND.FTN.31. Notes: RUST, FTN |
| STND.CODE.14 | Responses to a listed failure | Body: STND.RUST.13, STND.FTN.29, STND.LEAN.25. Notes: RUST, FTN, LEAN; Purpose of SV |
| STND.CODE.15 | Ignored failure results diagnosed | Body: STND.RUST.14. Notes: RUST (failures, floor) |
| STND.CODE.16, sentence 1 | Checks of CPS.5 and CPS.9 not removable | Body: STND.RUST.15. Notes: RUST (failures, floor); Purpose of SV |
| STND.CODE.17 to .20 | High assurance | Notes of SV (tools that synthesize or simulate); Purpose of RUST and FTN, in the range "STND.CODE.14 to STND.CODE.21" |
| STND.CODE.21 | Finite-value assumptions near checks (default) | Body: STND.FTN.18. Notes: FTN (floating-point exceptions); Purpose ranges of RUST and FTN |
| Untrusted input (Term) | Interface for outside use; function includes procedures | Terms of RUST and FTN ("the public interface that the term Untrusted input of STND.CODE takes in") |
| High-assurance code (Term) | | Terms of SV |

Not cited: STND.CODE.16 sentence 2 and STND.CODE.18. Citations of STND.CXX.18 that remain: the FTN Notes, for the finite-value option in C++ (valid: STND.CXX.18 keeps that sentence).
