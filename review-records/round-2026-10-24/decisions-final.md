# Decisions for the custodian at ratification, round of 2026-10-24

This list supersedes decisions-for-the-custodian.md (reviewer C), which predates the three fix passes (fixpass.md, fixpass-2.md, fixpass-3.md). It merges that list with the drafters' decisions, the reconciliation reports, and the final verifications. Each decision has a recommendation. Ratifying the round "with the recommendations" adopts every recommendation below.

## What ratification applies

Twenty-five transactions, in this order:

1. The amendments STND.OMP 1.0.1, STND.CXX 1.1, STND.PY 1.0.1, STND.JL 1.1, NUMER 1.3 and STND.VVUQ 1.4.
2. STND.BUILD with its mnemonic, then STND.WFLOW with its mnemonic.
3. The amendments STND.BUILD 1.0.1 and STND.CXX 1.1.1.
4. STND.STDC, STND.RUST, STND.FTN, STND.SV and STND.LEAN, each with its mnemonic.
5. The amendments STND.CONC 1.1, STND.PROJ 1.2 and STND.HARN 1.2.

Classes under GOV.41:

| Class | Amendments |
| --- | --- |
| Editorial | OMP 1.0.1, PY 1.0.1, BUILD 1.0.1, CXX 1.1.1 |
| Minor | CXX 1.1, JL 1.1, NUMER 1.3, VVUQ 1.4 (with an editorial part), CONC 1.1, PROJ 1.2, HARN 1.2 |

## Decisions

1. **Mnemonics.** BUILD, WFLOW, STDC (alternative CC), RUST, FTN, SV (alternative HDL), LEAN. Each meets STND.IDENT.17 and .18. Recommend the proposed set.

2. **Class-onset departures from STND.CLASS.10, each argued in its Notes.**
   - BUILD.10 and BUILD.24 sentence 2 at CSQ3.
   - WFLOW.3 sentence 2, .21 sentence 2, .22 and .33 at CSQ1 (the DSGN.2 row). WFLOW.25 and .27 at CSQ3. The bundle of WFLOW.35 sentence 2 at CSQ2, and WFLOW.36 at CSQ3.
   - SV.3 sentence 1, SV.18 sentences 1 and 3, SV.20 and SV.21 at CSQ3, so that one record has one onset. SV.26 sentence 1 at CSQ1 where a second simulator is available, with proof admitted in its place.

   Recommend all as argued.

3. **Floor (GOV.11): the binding provisions.** Each Notes argues that the provision asks only what the provision it instantiates already asks, at the cost of wording or one record:
   - STDC.2, the C reading of CXX.16, .17, .18 and .29. Its CXX.17 row is now conditioned on a compiler or static check being among the means of the work.
   - RUST.6, agents only, with one comment at each unsafe construct. No ruling covers it: the PY.4 ruling was made for PY.
   - RUST.13, including sentence 2 on the panic hook and handler, now confirmed from primary sources.
   - RUST.14, conditioned as STDC.2's CXX.17 row is; RUST.15; RUST.34.
   - FTN.29 to .31.
   - LEAN.5 and LEAN.25. LEAN.25's responses are now stated by outcome.
   - HARN.29, with Standing now tested for each entry.

   Recommend yes for all.

4. **Reach of Untrusted input.** PY and JL use the arguments of each public function (the ruling of 2026-10-23). RUST.15 uses each function of a library crate's public interface. FTN.31 uses each module-public procedure. STDC uses data from outside that the threat model does not trust. Recommend extending the 2026-10-23 reach to RUST and FTN as drafted. One definition across the languages would come in a later amendment of STND.CODE.

5. **Edition in force.** Recommend that the C++ newest-edition rule and the CXX.3 agent rule are not extended to C, Fortran, Rust or Lean. STDC, FTN and RUST give their reasons in the Notes. Ask for a direction when a project needs one.

6. **STDC.28 and STDC.3 stay defaults.** STDC.28's stream facts are now confirmed from the openly posted ISO C working draft. Recommend keeping both as defaults.

7. **Logging as the only visible degradation.** PY.22 sentence 3 and RUST.13 sentence 3 bar it; JL.15 sentence 2 admits a record at the levels the default logger shows. Recommend keeping PY and JL as ruled, with no amendment this round.

8. **Shared rules for compiled languages (R17).** Recommend keeping the C reading of STND.CXX now. Moving CXX.16 to .18 and .28 to .31 to STND.CODE is a later round.

9. **Naming (R18).** Recommend one rule for later rounds: a language standard fixes names only where the language's own convention is checkable; otherwise the repository configuration governs (the LEAN.27 form). No table for C now.

10. **Other differences among sibling standards (R6, R16, R23).** These go on the open list for the next amendment round, with no change now:
    - an unchecked index from untrusted input (binding in JL.13);
    - checks in shipped builds (CXX.27 against JL.34);
    - counterparts of RUST.13 sentence 2 in CXX and PY;
    - a lock-file default for PY;
    - foreign interfaces in PY and JL;
    - the `#define NDEBUG` case in C source, which STND.CODE.6 does not reach.

11. **PY.17 and JL.24 cite STND.CONC.23 in the Notes only.** A body citation would make PY a minor amendment. Recommend Notes only.

12. **NUMER.2 matter name:** "Random streams of a computation divided among concurrent tasks". Recommend keep.

13. **Lean readings.**
    - (a) Logical axiom declarations are read as assumptions of the evidence, and VV.1's "shown to be met" as "stated as assumed" for the soundness of the logic and of each checker. Recommend the reading.
    - (b) The CSQ0 reading: the weaker form of independent checker, conditioned on the means of the work. Recommend it.
    - (c) LEAN.22 is consistent with QA.7. Recommend yes.

14. **Constrained random tests of a deterministic design** are read as neither tests under VVUQ.64 and .65 nor comparisons under NUMER.26 (SV Notes). Recommend yes.

15. **Harness (unit 0008).**
    - (a) **Two installation tests before reliance.** A hook's allow must outrank the kept ask rule for `git push` and `gh` posts. The sandbox's `allowRead` and `denyRead` must behave as unit 0007 assumes for the secret store, and a shell write to `.git/config` must fail under the M-a `denyWrite`. Until these pass, an authorized write may still be referred. Recommend running them, with the results recorded in unit 0008.
    - (b) **A QA.8 code review** of the harness, by an agent of another configuration, before installation. The transition of entry 53 for STND.HARN.18 ends at that installation. Recommend yes.
    - (c) **Residual risks.**
      - M-c: refuse an unsigned authorization where no signer register exists, unless the owner passes an explicit option. Recommend doing it now, as a small unit.
      - M-b: give `--expiry-horizon` a stated default bound. Recommend doing it later.
    - (d) **Credential helpers.** Any `credential.helper` in the git configuration makes every push referred, since the guard reads a credential section as a possible redirection. Recommend keeping that (refer in doubt), with a line in the harness README.

16. **HANDOFF.md.** Once the round is applied, its standing process and directions move to `CUSTODIAN.md`, and its remaining items (15 a to c and the open list of item 10) move to `OPEN-ITEMS.md`. HANDOFF.md and the delivery manifest `SHA256SUMS` are then removed with `git rm`, with git history as the recovery path (the custodian's direction of 2026-10-24).
