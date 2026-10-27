# Cold verification and reconciliation review of the round of 2026-10-27: brief

Two reviewers, of another configuration than the author, who have not seen the drafting or the first reviews' discussion.

## Before you start

- REPO is `/home/brianm/projects/utils/governance-harness`.
- Read `REPO/CUSTODIAN.md`, then in `REPO/review-records/round-2026-10-27/`: `decisions.md`, `draft-status.md`, `review-brief.md` (what the first reviewers checked), `review-a.md`, `review-b.md`, and `dispositions.md`.
- Write only your report. Do not edit the corpus, the scripts, or any other file. Keep scratch files in your own new subdirectory of `/tmp/claude-1000/`. Use no network.

## Tools

From `REPO/harness/`:

- Rehearse: `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_27.py`. To keep a copy, make a directory `<dir>`, copy `governance/` into `<dir>/governance`, and run `python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_round_2026_10_27 as R; R.apply('<dir>/governance')"`.
- On a copy: `python3 -B -m govharness verify <copy>`, `show <copy> ID`, `find <copy> WORDS`, `pairs <copy> ID`, and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`.
- Reading copies after the round: `review-records/round-2026-10-27/reading-copies/`. Before the round: `REPO/rendered/`.
- The scripts that hold the text, rows, and rationales: `REPO/tools/amendment-scripts/apply_{code_1_3,deps_1_1,fi_editorial_2026_10_27,stdc_1_2,py_1_2,rust_1_2,jl_1_3,cxx_1_3}.py`.

## Verifier

For each row of `dispositions.md`: confirm on a rehearsed copy that the text now reads as the disposition says, and that the fix answers the finding. Then read every changed or new provision, term, Note, revision row, and rationale of the round afresh against the checks of "What every reviewer checks" in `review-brief.md`, and report anything the fixes broke or the first reviews missed.

Write `REPO/review-records/round-2026-10-27/verify.md`.

## Reconciler

Read the round as a whole, and against the rest of the corpus:

- **Terms.** Foreign interface (STND.CODE) and Lock file (STND.DEPS) are each defined once, clash with no term of the Lexicon (`LEX/`) or of another document, and are used in the sense defined in every document that imports them. The clauses of the language standards that name their constructs, and the clause of STND.RUST on a declaration with an unwinding ABI, add to the term and do not contradict it. The clause "For STND.CODE.24 alone" is sound as a term.
- **Agreement.** STND.CODE.22 to .26 agree with one another, with STND.CODE.7, .12, and .14, with STND.CONC.5, and with what each language standard keeps (STND.PY.35, STND.RUST.24 to .27 and .30, STND.JL.38 and .39, STND.CXX.5 and .21, STND.FTN.27 and .28). STND.DEPS.12 agrees with STND.DEPS.10, STND.RUST.30, and the Notes of STND.PY and STND.JL on lock files and manifests.
- **No restatement (GOV.31).** No new text restates a provision held elsewhere, and what each language standard keeps adds language content.
- **Nothing lost.** Every outcome of the withdrawn provisions (STND.CXX.20, .22; STND.STDC.36; STND.PY.33, .34, .36, .37; STND.JL.4, .37, .40, .41) and of the removed sentences stands in the corpus after the round, or the rationale says truly that it is narrowed.
- **Withdrawal.** No citation of a withdrawn identifier remains anywhere outside revision histories, the field `withdrawn`, and the ledger; the order of transactions leaves no state of the round citing one.
- **Records.** The revision rows and rationales are consistent with one another, with the text, and with `decisions.md`; nothing writes that the custodian has ruled what is still to be ruled.
- **The questions for the custodian** at the end of `dispositions.md` are complete, and each is stated fairly.

Write `REPO/review-records/round-2026-10-27/reconciliation.md`.

## Report

Under 800 words. Start with what you verified by running something. Then findings as Defect, Should-fix, and Optional, numbered, each with the exact text at fault and the exact replacement wording. End with any question that only the custodian can answer.
