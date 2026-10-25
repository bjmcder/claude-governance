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

## Decisions for the custodian

1. **Fortran reach to documented external procedures.** Under the STND.CODE 1.2 term, an external procedure that the documentation or the repository configuration names for use by code outside the work is in the interface for outside use; the reach is new. The FTN floor paragraph argues it: STND.FTN.31 asks only the form of a check that DSGN.2 and STND.CODE.6 already ask, at one test per untrusted subscript, and an external procedure that nothing names stays out. Recommend: accept, as one decision with P1's on the term.
2. **Rust reach outside library code.** The same widening for a function outside library code that the documentation or the repository configuration names, an exported foreign function among them; RUST.15 asks only the form of a check. Recommend: accept, with decision 1.
3. **STND.FTN.18 beneath STND.CODE.21.** Both are defaults, and FTN.18 restates the first sentence of CODE.21 for each source file; it now cites CODE.21 and adds no other outcome. Kept on the lead's direction. Recommend: keep now, and retire FTN.18 at the next amendment of STND.FTN (GOV.31).
4. **STND.RUST.14 kept.** Rust provides a form of declaration, so STND.CODE.15 applies to Rust on its own terms and RUST.14 states its Rust form, as ratified on 2026-10-24 with its floor argument. Recommend: keep, with the citation.
5. **Naming rule in RUST, FTN, and SV.** RUST.35, FTN.37, and SV.28 take the STND.LEAN.27 form in the words of STND.STDC.39, with the NUMER.4 allowance, and add no table. Rust's case convention is checkable (a2 fact 5), so decision 9 would admit a Rust table; none is fixed because the lints warn by default and STND.BUILD.12 asks that a change fail on a warning, so a configuration that names the convention gets it checked at no added cost, while that the Rust project publishes the convention is unverified. Fortran and Verilog have no convention that the research retrieved. Recommend: adopt as drafted.
6. **Class of STND.LEAN 1.0.1.** After review item S1, the amendment is a citation in LEAN.25 and Notes edits only, with LEAN.27 unchanged, so it alters no obligation, permission, or defined meaning. Recommend: editorial.

## Review (review.md, cold and STND.HARN.28 pair review)

| Item | Disposition |
| --- | --- |
| S1 LEAN.27 as editorial | Fixed by option (a): the LEAN.27 text edit is reverted, with its clauses in the history row and the rationale; the rationale says LEAN.27, already in the form of decision 9, is unchanged. LEAN.27 drops out of pairs-changed.md. The SV rationale now says "in the words of STND.STDC.39", since LEAN.27 keeps its own words. |
| S2 Rationale overclaims a ruling | Fixed in the RUST and FTN rationales: "the reach that STND.CODE 1.2 gives the term in every language". The clauses that call the library-crate and module-public placement ratified stay, since decision 4 ratified that reach. |
| S3 RUST.14 "wider" | Fixed: the RUST Notes say RUST.14 is kept as ratified, that Rust provides a form of declaration so STND.CODE.15 applies to Rust code on its own terms, and that RUST.14 states its Rust form. |
| O1 FTN.18 restates CODE.21 | Taken: the FTN Notes add that FTN.18 adds no other outcome to STND.CODE.21; decision 3 recommends retiring it later. |
| O2 RUST naming reason | Taken: the Notes say STND.BUILD.12 asks that a change fail on each warning, so the configuration names the convention at no added cost and a fixed table would add nothing. |
| O3 Negative about the research | Taken in FTN and SV: "The research note retrieved no convention of names that ... fixes, and that none exists is unverified". |
| O4 SV Purpose "in every build" | Taken: "are not removable by an execution setting through STND.CODE.16". |
| O5 FTN.29 status argument against CODE.14 | P1's, routed by the lead. No P3 change. |

Results after the fixes: `rehearse governance apply_close_p3.py` appends 7 entries (seq 148 to 154) and every check passes; `findings.py` reports no defect for the four documents (the eleven three-modal review notices carried from 1.0); `check_refs` reports 0 of 4 documents with missing rows. Reading copies `<ID>-0.3.md`; pair lists regenerated.

## Update to P1 0.3 (STND.CODE.14 names an argument that the caller passes)

Each Notes passage that describes STND.CODE.14 now gives its whole pass to the caller, "in its result, in an argument that the caller passes to receive it, or by a mechanism of the language that propagates it": RUST (the returned condition and the panic), FTN Failures (the result of a function and the status argument), FTN Floor (a status argument is such an argument, so STND.FTN.29 admits nothing beyond STND.CODE.14), and LEAN (the result type and the monad error). The Purpose ranges of RUST and FTN and the SV Purpose cite STND.CODE.14 by number only and need no change. No provision text changed. Results: 7 entries, every verify check passes, no defect in findings (11 carried three-modal notices), check_refs 0 of 4. Reading copies `<ID>-0.4.md`; pair lists regenerated, and pairs-changed.md stands, since no changed provision differs.

## Reconciliation review (reconciliation-alignment.md A, reconciliation-floor.md B, reconciliation-records.md C)

| Item | Disposition |
| --- | --- |
| A blocking 1: STND.FTN.18 restates STND.CODE.21 sentence 1 | Withdrawn in FTN 1.1, by the convention of STND.CXX 1.2: the field `withdrawn: ["STND.FTN.18"]`, the file deleted, the ID never reused. The Purpose range reads STND.FTN.13 to STND.FTN.17; the floating-point Notes cite the first sentence of STND.CODE.21 and keep the sentence on STND.CXX.18; the class onset names STND.FTN.15 alone; the history row and the rationale state the withdrawal under GOV.31. No other document of the corpus or of `rendered/` cites STND.FTN.18 except the STND.CODE Notes of P1 (`for-p1.md`, item 2). |
| A blocking 2: STND.RUST.14 against STND.CODE.15 | Not possible without changing the ratified obligation: STND.RUST.14 is met by a compiler or static check that diagnoses every ignored value, with no declaration, and STND.CODE.15 is not; a RUST.14 that names `must_use` and drops its condition would narrow the ways of meeting it and drop its condition, both changes to a ratified binding provision. Stopped, and put to the custodian (decision 4 below). `apply_rust_1_1.py` carries both forms behind `WITHDRAW_RUST14`: True, the recommended form, withdraws STND.RUST.14 (field `withdrawn`, file deleted, Purpose and floor Notes adjusted, Notes say STND.CODE.15 applies to Rust directly with the must_use attribute as its form); False keeps it as ratified with the citation, and its Notes say that a work meets STND.CODE.15 as well only by that attribute. Both forms rehearse with every check passing. The STND.CODE Notes name STND.RUST.14 (`for-p1.md`, item 1). |
| B: RUST.1 sentence 3 yields to STND.CODE.19 | Done in the body: "other than its high-assurance code whose edition and toolchain STND.CODE.19 fixes", citing STND.CODE.19, as STND.PY.14 and STND.JL.1 do; the builds Notes give the reason. RUST.1 stays a default with three modals on one subject. |
| B: RUST.35 as a departure from decision 9 | Listed as decision 5 below, with the reason. |
| A: FTN has no counterpart of STND.CXX.27 or STND.JL.36 | The FTN Notes (Checks) give the reason: Fortran defines no checked mode, the check of subscripts is a compiler facility that the Fortran standard does not require, so STND.FTN.31 keeps the check of each untrusted subscript in the code and STND.FTN.35 runs the compiler's checks in the tests. STND.JL.36 is named in words, since it does not exist where P3 follows P1 directly. |
| A: STND.FTN.26 and STND.CONC.30 | STND.FTN.26 cites STND.CONC.30, and its second sentence admits an order of the records of images that a protocol of the images fixes. The first sentence stays without the clause, because the constraints of DO CONCURRENT forbid image control statements and impure references, so its iterations have no such protocol; the Notes say so. |
| C: order of entries | The lead moves P3 after P1; the scripts need no change. |

Results: `rehearse governance apply_close_p3.py` appends 7 entries (seq 148 to 154) and every check passes; `findings.py` reports no defect for the four documents (11 carried three-modal notices); `check_refs` 0 of 4 documents with missing rows. Reading copies `<ID>-0.5.md`; pair lists regenerated; `pairs-changed.md` has 37 pairs, none missing.

## Decisions for the custodian (as they stand after the reconciliation)

1. **Fortran reach to documented external procedures.** Unchanged from above. Recommend: accept, with P1's decision on the term.
2. **Rust reach outside library code.** Unchanged. Recommend: accept, with decision 1.
3. **STND.FTN.18.** Now withdrawn in the scripts (A blocking 1), its outcome held by the default STND.CODE.21. Recommend: approve the withdrawal. If the custodian keeps it instead, the 0.4 form (FTN.18 citing STND.CODE.21) is the alternative.
4. **STND.RUST.14 against STND.CODE.15.** Both bind; RUST.14 is met by a blanket static check, CODE.15 only by a declaration (must_use, which Rust provides, so CODE.15 binds Rust without condition). Options: (a) withdraw STND.RUST.14, removing no obligation that STND.CODE.15 does not already impose on Rust; (b) keep it as ratified, with the citation, leaving two binding texts with different means; (c) rewrite it with `must_use` and no condition, a change to a ratified binding provision that needs its own floor argument. Recommend (a), the scripts' default.
5. **Naming rule in RUST, FTN, and SV, and the Rust departure from decision 9.** Decision 9 lets a standard fix names where the language's convention is checkable, and Rust's case convention is (a2 fact 5). STND.RUST.35 nonetheless leaves the convention to the repository configuration. Reason: the case lints warn by default and STND.BUILD.12 asks that a change fail on each warning, so a configuration that names the convention has it checked at no added cost, while a table in the standard would restate those lints, and that the Rust project publishes the convention is unverified. FTN and SV have no convention that the research retrieved. Recommend: accept STND.RUST.35 as a reasoned departure, and STND.FTN.37 and STND.SV.28 as the rule.
6. **Class of STND.LEAN 1.0.1.** Editorial (citation in LEAN.25 and Notes only). Recommend: editorial.
