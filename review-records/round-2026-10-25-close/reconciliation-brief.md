# Reconciliation review of the closing round of 2026-10-25: brief

Three reviewers each read the whole round on one dimension.

**Before you start.**
- REPO is `/home/brianm/projects/utils/governance-ledger109`.
- Read `REPO/tools/round-brief-2026-10-25.md` and what it points to: `CUSTODIAN.md`, the definition of done, and the Review agents section of the 2026-10-24 brief.
- Do not edit any file except your report. Keep scratch files in your own new subdirectory of `/tmp/claude-1000/`.

## The round

The script `REPO/tools/amendment-scripts/apply_round_2026_10_25_close.py` applies the round in ledger order: 28 transactions, entries 148 to 175 in rehearsal.

**Rehearse it from `REPO/harness/`:**
1. Run `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_25_close.py`. It prints the path of the rehearsed copy.
2. On that copy, run `python3 -B -m govharness verify <copy>`, `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`, and `PYTHONPATH=. python3 -B ../tools/check_refs.py <copy>`.
3. Compose reading copies with `compose(read_corpus(root), read_ledger(root), ReadingCopy(id, name))`. The imports are `govharness.derive.reading_copy`, `govharness.cli.derived.read_corpus`, and `govharness.ledger.chain.read_ledger`. The live documents before the round are in `REPO/rendered/`.

**The packages.** Each package's drafts, reviews, verifications, and `dispositions.md` are in `REPO/review-records/round-2026-10-25-close/<p1..p5>/`.

| Package | Amendments |
| --- | --- |
| P1 | STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2 (the shared rules moved; Untrusted input defined once; STND.CODE.14 to .21; STND.CXX.16, .17, .28 to .31 withdrawn; STND.CXX.32, .33; STND.STDC.39, .40) |
| P2 | STND.PY 1.1, STND.JL 1.2 |
| P3 | STND.RUST 1.1, STND.FTN 1.1, STND.SV 1.1, STND.LEAN 1.0.1 |
| P4 | STND.OFFLD 1.0.1, STND.MPI 1.0.1, STND.OMP 1.0.2, STND.HARN 1.3 (STND.HARN.30) |
| P5 | Editorial References amendments of 14 documents, and STND.BUILD 1.0.2 |

**Facts.** The fact notes for this round are `REPO/research/round-addenda/a1-confirmations.md` and `a2-language-facts.md`.

## Reviewer A: alignment across documents

Check across all amended documents:

- **Terms.** Each is defined once and imported elsewhere, with no clash. Check above all:
  - Untrusted input, "interface for outside use", and each language's Public interface;
  - High-assurance code;
  - Panic and Language edition, which are not to change.
- **No restatement (GOV.31).** No provision restates another. Cover:
  - the language provisions against STND.CODE.14 to .21;
  - the callback rule in four standards (STND.CXX.22, STND.RUST.25, STND.PY.35, STND.JL.39);
  - STND.FTN.18 against STND.CODE.21;
  - STND.RUST.14 against STND.CODE.15.
- **Same question, same answer.** The language standards now give the same answer to each shared question:
  - responses to listed failures;
  - ignored results;
  - checks no setting removes;
  - the finite-value option;
  - terminate handlers and hooks;
  - naming (R18);
  - foreign interfaces;
  - lock files;
  - checks in shipped builds;
  - untrusted input and its reach.
- **The sibling list.** Every item has an amendment or a reasoned "no change" (definition of done, item 1).
- **Citations.** No citation of a withdrawn identifier remains anywhere in the corpus, outside revision histories.
- **References.** References are complete by `tools/check_refs.py`.

Write `REPO/review-records/round-2026-10-25-close/reconciliation-alignment.md`.

## Reviewer B: modes, floor, and class onsets

Check across all amended documents:

- **Binding provisions.** List every binding provision that is new, moved, or changed, with the PRIME, GUARD, GOV, or floor provision it instantiates. For each, say whether it asks more of any language than that provision does, at the cost of wording or one record (GOV.11, GOV.19, R22). Read each against the rulings of 2026-10-23 for PY and JL, and the ratification of 2026-10-24 for the other languages. Above all, check:
  - STND.CODE.6, .14, .15, .16, and .18;
  - STND.CXX.32 and STND.STDC.40;
  - STND.PY.32;
  - STND.HARN.30 and the Signature row of STND.HARN.29.
- **High-assurance defaults.** STND.CODE.17, .19, and .20 now reach every language.
- **The widened reach of Untrusted input**, through STND.CODE.6, into C, C++, Lean, hardware descriptions, documented Rust functions outside library code, documented Fortran external procedures, and the ruled STND.PY.25 and STND.JL.13.
- **Class onsets.** Every class-onset statement of a changed provision agrees with STND.CLASS.10, and each departure is argued.
- **Tools.** No provision blocks work where a tool or means is unavailable.
- **Owner decisions.** No owner decision is required that LVL0 does not assign (STND.DRAFT.42; STND.HARN.30).
- **Rulings.** No ruling is attributed to the custodian that the custodian has not made.

Write `REPO/review-records/round-2026-10-25-close/reconciliation-floor.md`.

## Reviewer C: records and integrity

Check:

- **The round as a whole.** It rehearses and verifies. `findings.py` shows no defect, and `check_refs.py` reports 0 documents with missing rows.
- **Rationales.** Each is accurate against its document and its review record. Each ends with the corpus's fixed tail and cites no entry of this round by number. The class of each amendment is right under STND.IDENT.3, and each history row and revision number is correct.
- **Withdrawals.** The withdrawn identifiers follow the convention of STND.CLASS.
- **Review records.** Each package's record is complete: reviews, verifications, and dispositions. Each blocking finding is closed. Note that P4's and P5's last fixes and P2's and P3's last revisions have had no verification of their own. Verify them.
- **The harness suite** passes (`cd REPO/harness && python3 -B -m unittest discover -s tests`).
- **The definition of done**, items 1 to 5: say which hold.
- **Decisions for the custodian.** Compile, from every `dispositions.md` and every drafter's list, one numbered list of decisions, each with its recommendation, with duplicates removed. Include the decisions that reviewers say a drafter missed.

Write `REPO/review-records/round-2026-10-25-close/reconciliation-records.md` and `REPO/review-records/round-2026-10-25-close/decisions-draft.md`.

## All reviewers

Rank findings Blocking (a broken rule, a factual error, a conflict, or an item of the definition of done not met) and Should-fix. Give each with the document, the provision, and the fix. Keep the report under 1,600 words. In your final message, give the blocking items.
