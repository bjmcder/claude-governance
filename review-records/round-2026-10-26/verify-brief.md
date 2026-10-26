# Cold verification and reconciliation review of the round of 2026-10-26: brief

Two reviewers, of another configuration than the author, who have not seen the drafting or the first reviews' discussion.

## Before you start

- REPO is `/home/brianm/projects/utils/governance-harness`.
- Read `REPO/CUSTODIAN.md`, then in `REPO/review-records/round-2026-10-26/`: `decisions.md`, `draft-status.md`, `review-brief.md` (what the first reviewers checked), `review-a.md`, `review-b.md`, and `dispositions.md`.
- Write only your report. Do not edit the corpus, the scripts, or any other file. Keep scratch files in your own new subdirectory of `/tmp/claude-1000/`. Use no network.
- The harness code does not yet implement the new text; that is owed at the end of the round (`draft-status.md`). Report a mismatch with the code only where the text is wrong or unclear.

## Tools

From `REPO/harness/`:

- Rehearse: `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_26.py`. To keep a copy, copy `governance/` into your scratch directory and run `python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_round_2026_10_26 as R; R.apply('<copy>')"`.
- On a copy: `python3 -B -m govharness verify <copy>`, `show <copy> ID`, `find <copy> WORDS`, and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`.
- Reading copies after the round: `review-records/round-2026-10-26/reading-copies/`. Before the round: `REPO/rendered/`.
- The scripts that hold the text, rows, and rationales: `REPO/tools/amendment-scripts/apply_{dflt_1_5_2,proj_1_2_1,hw_remote_1_0_2,harn_1_4,draft_1_5,ident_1_4}.py`.

## Verifier

For each row of `dispositions.md`: confirm on a rehearsed copy that the text now reads as the disposition says, and that the fix answers the finding. Then read every changed or new provision, term, Note, revision row, and rationale of the round afresh against the checks of "What every reviewer checks" in `review-brief.md`, and report anything the fixes broke or the first reviews missed.

Write `REPO/review-records/round-2026-10-26/verify.md`.

## Reconciler

Read the round as a whole, and against the rest of the corpus:

- **Terms.** The new or changed terms (Reach, Pin in force, Content hash in STND.HARN; Sentence and Cited document in STND.DRAFT) are each defined once, clash with no term of the Lexicon or of another document (search the Terms sections and `LEX/`), and are used in the round in the sense defined. Say whether "Reach" sits badly beside the bounds of reach of STND.DFLT.25.
- **Agreement.** STND.HARN.7, .9, .31, and the terms agree with one another; STND.DRAFT's section Checks agrees with STND.DRAFT.34, the term Cited document, and STND.HARN; STND.IDENT.12, .14, and .24 agree.
- **No restatement (GOV.31).** No new text restates a provision held elsewhere.
- **Withdrawal.** No citation of STND.HARN.18 to .23, .29, or .30 remains anywhere outside revision histories and the ledger; nothing in the corpus still depends on them or on the removed terms Derived configuration and Refer.
- **Records.** The revision rows and rationales are consistent with one another and with `decisions.md`; the order of transactions leaves no state of the round citing a withdrawn identifier; nothing writes that the custodian has ruled what is still to be ruled.
- **The questions for the custodian** at the end of `dispositions.md` are complete, and each is stated fairly.

Write `REPO/review-records/round-2026-10-26/reconciliation.md`.

## Report

Under 800 words. Start with what you verified by running something. Then findings as Defect, Should-fix, and Optional, numbered, each with the exact text at fault and the exact replacement wording. End with any question that only the custodian can answer.
