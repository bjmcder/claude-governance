# Decisions for the custodian, closing round of 2026-10-25

Compiled by reviewer C, and brought up to date by the lead after the fixes that followed the reconciliation review, from `p1` to `p5/dispositions.md`, the drafters' lists they contain, the cold, pair, and verification reviews, `p5/gaps.md`, and `tools/round-brief-2026-10-25.md`. Duplicates are merged; the source package is in brackets. The round is applied only after ratification, each entry with its real time. Items marked "no change" are the reasoned resolutions of the sibling list that definition of done item 1 asks the custodian to record.

## Floor and reach (GOV.11, R22)

1. **Untrusted input, defined once in STND.CODE, with one reach** [P1 1; P2 1; P3 1, 2]. The union of the placements of the language standards and the interface for outside use that the documentation or the repository configuration names. It widens PY (documented functions outside library code or with an underscore), JL (documented unexported functions), RUST (documented functions outside library crates), and FTN (documented external procedures), and through STND.CODE.6 it newly reaches C, C++, Lean, and hardware descriptions. Floor: the form of an existing check only. Recommend accept. Fallback: delete the documentation clause from the term; PY, JL, RUST, and FTN then hold as ruled.
2. **STND.CODE.14**, the responses to listed failures, including the pass to the caller in a result, in an argument, or by a mechanism of the language [P1 2, 13; P3 5]. Wording only in every language. Recommend accept.
3. **STND.CODE.15**, a declaration under which an ignored failure is diagnosed, conditioned on a form of declaration [P1 3; P3 4]. Recommend accept. **With it, STND.RUST.14 is withdrawn** [P3, reconciliation A2]: RUST.14 can be met by a blanket static check, while CODE.15 asks a declaration (in Rust, `must_use`), so the two binding provisions differ and RUST.14 cannot be aligned without changing its ratified obligation. Recommend withdrawal, since CODE.15 binds Rust in any case. Alternative: keep RUST.14 as ratified (`WITHDRAW_RUST14 = False` in `apply_rust_1_1.py`); a project that meets RUST.14 by a blanket check then still fails CODE.15.
4. **STND.CODE.16**: sentence 1 (CPS.5 and CPS.9 checks kept from removal) for the languages with no ruling; sentence 2 (a definition in the source that turns a check off, the `NDEBUG` case) for every language [P1 4]. Form of a check only. Recommend accept.
5. **STND.CODE.21**, a default in every language [P1 5; P3 3]. The binding forms stay where ruled or ratified (STND.CXX.18, STND.STDC.40); STND.FTN.18, which restated its first sentence, is withdrawn in this round (reconciliation A1; GOV.31). Onset CSQ3, argued as the precondition half of DSGN.2, whose row in STND.CLASS.10 is the postcondition half at CSQ1. Recommend accept, with the withdrawal of STND.FTN.18.
6. **STND.CODE.17, .19, .20 reach every language** [P1 6]. Defaults from CSQ1, replaceable by a recorded decision. Their onsets are argued as departures from STND.CLASS.10 for the languages no ruling covers. Recommend accept; CUSTODIAN.md's line that the high-assurance ruling "was not extended to C, Fortran, Rust, or Lean" is then amended. The alternative opens each with "where the work is high-assurance code in a language whose standard applies the provision".
7. **STND.CODE.18 binding in every language**, one sentence per claim [P1 7]. Recommend accept.
8. **Counterparts of STND.RUST.13 sentence 2** [P1 8, 12; P2 4, 9]. STND.CXX.32 (binding, a terminate handler the work installs; no ruling covers it), STND.CXX.33 (default from CSQ1 on INTPR.8), STND.PY.32 (binding, a hook the work replaces; no ruling covers it). No Julia counterpart, since the repository holds no source for a Julia hook: no change. Recommend accept all.
9. **STND.STDC.2 and STND.STDC.40** keep the floor arguments ratified on 2026-10-24; STND.STDC.2 now holds only the errno clause, reworded so an errno-alone report is not read as a result. STND.STDC.40 restates the binding finite-value rule of STND.CXX.18 in C words by design, so that a later change to CXX.18 does not change C silently [P1 10, 14]. Recommend accept.
10. **Withdrawal** of STND.CXX.16, .17, .28 to .31, with STND.CXX.18 kept for its second sentence [P1 11]. Recommend accept.

## Sibling list (decision 10 of 2026-10-24)

11. **Checks in shipped builds**: STND.CXX.27 unchanged; new default STND.JL.36 from CSQ1 as its counterpart [P1 9; P2 3]. One resolution, replacing P1's "no change". Recommend accept.
12. **Unchecked index from untrusted input, STND.JL.13 against STND.PY.25**: no change. Built-in sequences raise `IndexError` in every mode; array libraries are unverified [P2 2]. Recommend no change.
13. **Logging as the only visible degradation, STND.PY.22 against STND.JL.15**: no change, by decision 7 of 2026-10-24 [P2 5]. Recommend no change.
14. **Lock file and foreign interfaces**: default STND.PY.33; defaults STND.PY.34 to PY.37 and STND.JL.37 to JL.41, from CSQ2 (DSGN.4, DSGN.5) and CSQ3 (DSGN.14) [P2 6, 7]. The callback steps now stand in four standards (CXX.22, RUST.25, PY.35, JL.39); recommend accept, and one STND.CODE provision in a later round (GOV.31).
15. **Release and version clauses**: STND.PY.14 and STND.JL.1 yield to a version that STND.CODE.19 fixes [P2 8]. Recommend accept.

## Naming and classes

16. **One naming rule (R18)**: new defaults STND.STDC.39, STND.RUST.35, STND.FTN.37, and STND.SV.28 from CSQ3, in the STND.LEAN.27 form with the NUMER.4 allowance; no table for C; the tables of CXX, PY, and JL stay; Rust's convention is checkable (a2, fact 5), so STND.RUST.35 is a reasoned departure from decision 9: no table, because the case lints and STND.BUILD.12 already ask that a change fail on their warnings [P1 10; P3 5]. Recommend accept.
17. **STND.LEAN 1.0.1 is editorial** (LEAN.27 unchanged, LEAN.25 cites STND.CODE.14) [P3 6]. Recommend accept.

## Editorial amendments and the cross-references

18. **STND.OFFLD.31 keeps both sentences** and cites STND.PERF.14 and STND.PERF.12; those provisions leave offloaded work to it [P4 1]. Content question: STND.PERF.12 also names the first filling of caches and memory, which STND.OFFLD.31 does not [P4 review]. Recommend accept, and no addition now (it would add to an obligation).
19. **STND.MPI and STND.OMP name their form of STND.CONC.30, no provision added**: no change. The OpenMP ordered-region fact is sourced; the MPI facts on forwarded output and the shared file pointer are marked unverified [P4 4]. Recommend no change.

## STND.HARN

20. **STND.HARN.29 row Signature and new STND.HARN.30, binding** [P4 5, 6]. The row asks a signature in more cases (a signed entry, a scope at or under the register, an unreadable form, an anchor file). STND.HARN.30 asks only that reliance rest on an authorization the owner accepts unsigned at the derivation, and that the report name it. The floor argument: it asks no work that GUARD.10 and PRIME.7 do not; a harness that never relies meets it. Recommend accept.
21. **The reading of STND.DRAFT.42 on an owner's acceptance at derivation** [P4 7]. (a) The acceptance is part of the grant that GUARD.10 reserves to the owner, made once per derivation within the configure act, so STND.HARN.30 requires no decision beyond one that LVL0 assigns. (b) Require a signature always, or a founded register: raises the cost of every derivation without a register. (c) Drop STND.HARN.30, keep the row and the expiry note; `OPTION = "c"` in `apply_harn_1_3.py` builds it. Recommend (a). Weakness: the flag authenticates nothing; a signer register removes the need for it.

## References and records

22. **Scope of the References check.** `tools/check_refs.py` was scoped to LVL1 to LVL3, to drop history rows by the heading, and to skip tables of examples (commit 760aabd; definition of done item 5). The live corpus then reports 16 documents, not the 22 of the brief. LVL0 and its four parts, MNEM, and the example table of STND.IDENT keep no rows. The 14 real gaps and those of STND.CODE and STND.MPI are closed. HW.CPU, HW.EMBED, HW.GPU, and HW.QPU drop Article names from informative sentences in place of citing Simplicity, which none of their provisions instantiates. Unit 0013 is to carry the same scope. Recommend accept; no LVL0 amendment is proposed (it would need GOV.40).
23. **Order of entries and family scopes.** The round applies STND.CODE and STND.STDC, then P3, then STND.CXX 1.2 and P2, then P5 and STND.BUILD, then P4, so that no state cites a withdrawn identifier; the amendments of a sub-profile take the scope of its family (HW, HDES), so that the parent's ledger pin stays current. `verify` passes after every one of the 28 transactions. Forward references remain only in Notes (STND.CODE names STND.PY.32, STND.CXX.32, and .33 before they exist), which `verify` accepts. Recommend accept.
24. **STND.BUILD 1.0.2**: reviewer C's cold read is its review record; its one Should-fix (STND.STDC.40 for C) is taken. Recommend accept.

25. **STND.CXX.18 sentence 1 moves to STND.CODE.16 sentence 1 in different words**: "run, with its response, in every build and run" becomes "not removable by an execution setting". The Notes argue the same outcome, and the new words also cover interpreted runs [P1 15]. Recommend keep the new wording; alternative: restore the old words in STND.CODE.16.

## For a later round (left open, by the custodian's choice)

26. **One STND.CODE provision on foreign interfaces**, with one definition of Foreign interface (now defined in five standards) and one of Lock file (in STND.PY and STND.RUST), to replace the callback, ownership, and lock-file rules that now stand alike in several language standards (GOV.31) [P2 10, reconciliation A]. Recommend a later round; it is a restructuring of its own. It stays in OPEN-ITEMS.
27. **STND.OFFLD.31 and the first filling of caches and memory** that STND.PERF.12 names (item 18): recommend no addition now, and an open item for STND.OFFLD's next minor amendment.
