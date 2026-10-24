# Decisions for the custodian, round of 2026-10-24

Compiled by reviewer C from the dispositions.md of build, wflow, c, rust, fortran, hdl, lean, and amendments; the cold, pair, and security reviews and verifications; unit 0008; and the queue items R14, R17, R19, R23 that the round left to the reconciliation. The drafters' and reviewers' final messages are not on disk; items that the files cite as "in the report" are rebuilt from the Notes and dispositions (marked *). Duplicates are merged. Each decision has a recommendation. Reviewers A and B may refine items 4, 6, 7, 9, 10, 11, and 12.

The round is applied only after ratification (the round script sets its clock then). Items 1 to 17 do not block application unless the custodian says so.

1. **Mnemonics.** BUILD, WFLOW, STDC (alternative CC), RUST, FTN, SV (alternative HDL; distance 2 from PY), LEAN (alternative LEA). Recommend the proposed set: each meets STND.IDENT.17 and .18 and none reads as another common term in covered work.

2. **Class-onset departures from the rows of STND.CLASS.10.**
   (a) BUILD.24 s2 at CSQ3 on QA.13, and BUILD.10 at CSQ3 on SIMPL.6: neither asks a tracking mechanism or a hardware behavior. Recommend CSQ3.
   (b) WFLOW.3 s2, .21 s2, .22, .33 at CSQ1 following the DSGN.2 row; WFLOW.25 and .27 at CSQ3 as preconditions where data enters. Recommend both as read.
   (c) SV.3 s1, SV.18 s1, SV.20, SV.21 apply their INTPR.10 content from CSQ3, the onset of the HDES.6 and HDES.8 records they add to; SV.18 s3 from CSQ3. Recommend CSQ3 so one record does not carry two onsets.
   (d) SV.26 s1 from CSQ1 on QA.9, where a second simulator is available, with proof admitted in its place. Recommend yes.
   WFLOW.2 s2 and WFLOW.6 s1 now follow the QA.14 row (CSQ2); that earlier question is withdrawn.

3. **Floor (GOV.11): binding provisions.** STDC.2 (the C reading of CXX.16, .17, .18, .29; PRIME.4, PRIME.2); RUST.13, .14, .15 (PRIME.4) and .34 (PRIME.2); RUST.6 (GOV.48, agents only; cost one comment at each unsafe construct); FTN.29, .30, .31 (PRIME.4, CODE.6, CODE.7); LEAN.5 (PRIME.2) and LEAN.25 (PRIME.4); HARN.29 (GUARD.2, .11, .12; cost: the checks the harness makes). Each Notes argues that it asks only what the named provision asks, at the cost of wording or one record. Recommend: yes for all. The ruling for STDC.2 includes the errno clause of the CXX.16 row and the static check where the toolchain has no attribute (CXX.17 row), both new text for C.

4. **Reach of Untrusted input (R15)*.** PY and JL: arguments of each public function (ruling of 2026-10-23). RUST: each function of a library crate's public interface, so debug_assert! on preconditions is barred in a workspace's internal crates (RUST.15). FTN: each module-public procedure, public by default (FTN.31). STDC: data from outside, other than sources the threat model trusts. Recommend one reach for all: the public interface that the documentation or repository configuration names, unless the threat model records otherwise; extend the 2026-10-23 ruling to RUST and FTN on that basis.

5. **Edition or revision in force (R22).** The rulings for C++ (newest edition, CXX.3 to agents) are not extended to C, Fortran, or Rust. Recommend: no newest-edition rule for these three; STDC.3 (lowered editions recorded), RUST.1 (edition and oldest toolchain declared), and FTN's revision rule stay defaults. Ask for the direction when a project needs it.

6. **STDC.28 (stream errors) and the agent rule.** Recommend STDC.28 stays a default (no binding until the stream facts are confirmed from the standard) and STDC.3 stays a default (CXX.3 as a binding agent rule for C only on a direction on C's edition).

7. **Logging as the only visible degradation (R16, R23).** PY.22 s3 and RUST.13 s3 bar it; JL.15 s2 admits a record at the levels that the default logger shows. FTN and LEAN.25 follow the PRIME.4 list. Recommend keeping the adopted PY and JL as ruled, and no amendment this round.

8. **Shared rules for compiled languages (R17).** Move CXX.16 to .18 and .28 to .31 to STND.CODE, or keep the C and Fortran readings. Recommend keep the reading now (a minor amendment of CODE and CXX is a round of its own) and move the rules in the next round.

9. **Naming conventions (R18).** CXX.14, PY, JL have tables; STDC, FTN, and LEAN.27 leave naming to the repository configuration. Recommend one rule: a language standard fixes names only where the language's own convention is checkable; otherwise the repository configuration governs (LEAN.27 form, with the NUMER.4 notation allowance). Do not apply the CXX.14 table to C.

10. **Other differences between adopted PY, JL, CXX (R23).** An unchecked index from untrusted input (binding in JL.13); checks in shipped builds (CXX.27 against JL.34). Recommend: list as an open item for the next amendment round; no change now.

11. **Order of output from concurrent tasks (R14).** STND.CONC has no model-neutral rule; FTN.26 states the Fortran cases. Recommend leave FTN.26 standing, keep CONC 1.0.1 editorial, and record the gap for CONC's next minor revision.

12. **STND.VVUQ.63 names a test battery (R19)** against GOV.18 and the agnostic direction. Recommend a minor amendment of VVUQ outside this round (state the outcome; the battery moves to the Notes as an example). Record it as an open item meanwhile.

13. **PY.17 and JL.24 cite STND.CONC.23 in the Notes only.** A body citation makes PY a minor amendment. Recommend Notes only.

14. **NUMER.2 matter name:** "Random streams of a computation divided among concurrent tasks" (follows the assignment at the adoption of CONC). Recommend keep.

15. **Lean.**
    (a) Logical axiom declarations read as assumptions of the evidence, and VV.1's "shown to be met" read as "stated as assumed" for the soundness of the logic and each checker. Alternative: a standing owner declaration of the logic (VV.9). Recommend the reading.
    (b) CSQ0 reading and the strict Term Independent checker: no known checker meets it, so every CSQ0 Lean project would replace LEAN.16. Recommend the weaker alternative (source written apart, any runtime, relation to the kernel stated).
    (c) LEAN.22 consistent with QA.7. Recommend yes.

16. **Constrained random tests of a deterministic design** are read not to be tests of stochastic results under VVUQ.64, .65 and NUMER.26 (SV Notes). Recommend yes; the NUMER wording stays as is.

17. **Harness (unit 0008).**
    (a) Install only after the two installation tests: an allow of the guard outranking the kept ask rule for `git push` and `gh` posts; a narrower `allowRead` winning over the store's `denyRead`. Until they pass, authorized writes may still be referred. Recommend: require both and record the results.
    (b) A QA.8 code review of the harness, by an agent of another configuration, before installation; the transition of entry 53 for HARN.18 ends then. Recommend yes. Whether the entry-53 transition for HARN.26 to .28 has ended is yours to record; the amendment leaves it open.
    (c) Security residuals M-b and M-c: default `--expiry-horizon` to a stated bound (for example 90 days) and refuse an unsigned authorization when no signer register exists; cap the body of an authorized post. Recommend M-c yes now; M-b later.

18. **Procedure.** Apply the round only after ratification, since every entry says "ratified". Recommend archiving HANDOFF.md (archive first) once decisions 17 and 12 are moved to a successor open-items file, and rebuilding `rendered/` and `SHA256SUMS` after application.
