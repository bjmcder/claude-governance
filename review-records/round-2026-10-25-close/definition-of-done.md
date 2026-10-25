# Definition of done: closing the open items (2026-10-25)

The custodian directed on 2026-10-25: "Define a definition of done for the remaining work. Then proceed as recommended to completion." The remaining work is every item of `OPEN-ITEMS.md`. It is done when each criterion below holds, in this order: the corpus round first, then the harness units, then the installation kit.

## A. Corpus round (one round, under the standing process of CUSTODIAN.md)

The round amends adopted documents only. It runs in five packages, each owned by one drafter over disjoint documents:

| Package | Documents | Content |
| --- | --- | --- |
| P1 | STND.CODE, STND.CXX, STND.STDC | (a) The shared rules for compiled languages, STND.CXX.16 to .18 and .28 to .31, move to STND.CODE in their language-neutral form, with the language forms citing them (R17). (b) STND.CODE defines Untrusted input once, with one reach. (c) STND.STDC takes the naming rule (R18). (d) The `#define NDEBUG` case in source. (e) The STND.CXX items of the sibling list. (f) The References gaps of STND.CODE. |
| P2 | STND.PY, STND.JL | The Untrusted input term imported from STND.CODE, and the PY and JL items of the sibling list. |
| P3 | STND.RUST, STND.FTN, STND.SV, STND.LEAN | The Untrusted input term imported from STND.CODE, the naming rule (R18), and the FTN reading of the moved rules replaced by citations. |
| P4 | STND.OFFLD, STND.MPI, STND.OMP, STND.HARN | STND.OFFLD.31 cites STND.PERF.12 and .14. STND.MPI and STND.OMP name their form of STND.CONC.30. STND.HARN gains STND.HARN.30 (unsigned reliance, unit 0010), with the reading of STND.DRAFT.42 put to the custodian. The References gap of STND.MPI is closed here too. |
| P5 | The other 20 documents with References gaps (`tools/check_refs.py`) | Editorial amendments that add the missing References, through a provision citation where the text names a document. |

P2 and P3 cite the new provisions of STND.CODE, so they start once P1's STND.CODE text is fixed. P4 and P5 run in parallel with P1.

Done when:

1. Every corpus item of `OPEN-ITEMS.md` is either amended, or closed by a decision the custodian records at ratification. This includes each item of the sibling list (R6, R16, R23): either an amendment, or no change, with the reason stated.
2. Each amendment is classed under STND.IDENT.3, and its rationale ends with the fixed tail. Each binding provision that moves or is created carries a floor argument (GOV.11) put to the custodian. No C++ ruling is extended to another language without its own argument (R22).
3. Each package has had a cold review and a STND.HARN.28 pair review, by agents of another configuration, and its findings are fixed and verified.
4. A reconciliation review across the round checks:
   - alignment: terms defined once, no restatement, References complete;
   - modes, floor, and class onsets;
   - records: rehearsal, findings, rationales, and that every queue item is closed.
   Its findings are fixed and verified.
5. The whole round rehearses with `verify` passing, no finding of class defect, and `tools/check_refs.py` reporting 0 documents with missing rows across all of the corpus.
6. The custodian ratifies through AskUserQuestion. Only then is the round applied, each entry with its real time. After that, `verify`, `references --check`, and `compose --check` pass, the reading copies are rebuilt, and the README and OPEN-ITEMS are updated.

## B. Harness units (each in a worktree, reviewed by another configuration, merged only when clean)

7. **Unit 0012, M-b.** `--expiry-horizon` defaults to a stated bound of 90 days, unless the custodian names another, and `--expiry-horizon none` lifts it. Tests are added, and the README and unit 0008 are updated.
8. **Unit 0013, References check.** After the round is applied, the harness check of References (g.25) also reads bare document names, so the table and the check agree. It is a defect-class check, and `verify` passes on the live corpus.
9. **QA.8 code review of the whole harness**, after 0012 and 0013 are merged, by an agent of another configuration. Every High and Medium finding is fixed and verified. The record is in `harness/records/reviews/`.
10. After each merge, the full suite passes on main and the worktree is removed.

## C. Installation kit (the agent's part; the installation itself is the human owner's)

11. A configuration is derived for this machine into a scratch directory with `environment ... --write`, and `INSTALL.md` is read and checked against it.
12. `tools/install-tests.md` gives the three installation tests as steps the human owner runs after installing, each with its command, its expected result, and how to record it in unit 0008. The tests are:
    - an authorized `git push` or `gh` post proceeds, while the ask rules are kept;
    - the secret store's narrower `allowRead` wins over its `denyRead`;
    - a shell write to `.git/config` fails under the M-a `denyWrite`.
13. `OPEN-ITEMS.md` then holds only the custodian's own step: install as root, run the tests, and record the configure entry that ends the transition of ledger entry 53 for STND.HARN.18. Every other item is closed.

## Not in scope

- Anything that needs root, an installation under `/etc`, or a Claude Code session under the installed configuration. Those are the human owner's by design (`derive/environment/claude_code.py`).
- Running z3, which is not installed. Its path stays tested by stubs only.
