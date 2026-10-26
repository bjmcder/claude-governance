# Cold and STND.HARN.28 pair review of the round of 2026-10-26: brief

Two reviewers, each over one package. You are an agent of another configuration than the author, and you have not seen the drafting. Read cold: judge the text against the corpus and the custodian's decisions, not against the author's reasons.

## Before you start

- REPO is `/home/brianm/projects/utils/governance-harness`.
- Read `REPO/CUSTODIAN.md` (the standing process and directions), then `REPO/review-records/round-2026-10-26/decisions.md` (what the custodian decided) and `draft-status.md` (what is drafted, what is left out, and what the harness code will follow at the end).
- Write only your report. Do not edit the corpus, the scripts, or any other file. Keep scratch files in your own new subdirectory of `/tmp/claude-1000/`. Use no network.
- The harness code does not yet implement the new text; that is planned for the end of the round (`draft-status.md`, "Owed after the text"). Report a mismatch between new text and current code only where the text is wrong or unclear, not because the code lags.

## The round

`REPO/tools/amendment-scripts/apply_round_2026_10_26.py` applies seven transactions in ledger order, entries 176 to 182 in rehearsal. Each amendment's script holds its text, revision row, and rationale.

From `REPO/harness/`:

1. Rehearse: `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_26.py`. It prints the path of the rehearsed copy, which is deleted afterwards; to keep one, copy `governance/` into your scratch directory and run `python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_round_2026_10_26 as R; R.apply('<copy>')"`.
2. On a copy: `python3 -B -m govharness verify <copy>`, `python3 -B -m govharness show <copy> ID`, and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`.
3. Reading copies after the round are in `REPO/review-records/round-2026-10-26/reading-copies/`; the documents before the round are in `REPO/rendered/`. The pairs of STND.HARN.28 are in `pairs/` and `pairs-changed.md`.
4. To fetch a provision of the live corpus: `python3 -B -m govharness show governance ID`, or `context governance WORDS --budget 6000`.

## What every reviewer checks

- **Decisions.** Each amendment does what `decisions.md` records, no more and no less.
- **STND.DRAFT.** In each new or changed provision: one modal per sentence and at most three per provision; each condition before its clause, one per sentence; none of the body words "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any"; titles of six words or fewer, not verb-initial, distinct across the corpus; body identifiers equal `instantiates` plus `refers_to`.
- **Notes.** No obligation stated in the indicative, no narration of drafting, American English, nothing that names a tool or a version in a provision.
- **Class and record.** The class under STND.IDENT.3 is right; the revision row and the rationale say what changed; the rationale does not write that the custodian has ruled something not yet ruled (CUSTODIAN.md, item 3); floor arguments for new binding provisions are present and sound (GOV.11).
- **Pairs (STND.HARN.28).** Confirm `pairs-changed.md`: that no listed pair has a changed or new provision on its changed side. For each changed provision, say whether it addresses a matter that another adopted document also addresses, and whether the two conflict.
- **Citations.** No citation of a withdrawn identifier remains anywhere in the corpus outside revision histories, and no References table is wrong.

## Reviewer A: STND.HARN 1.4, with STND.DFLT 1.5.2, STND.PROJ 1.2.1, HW.GPU 1.0.2, HW.QPU 1.0.2

- **Withdrawal (decision 5).** STND.HARN.18 to .23, .29, and .30 are gone cleanly: the field `withdrawn`, the terms that only they used, the Notes on them, the document's `instantiates`, and every citation in other documents. Search the whole corpus. Check that STND.DFLT.22 and .23, STND.INSTR, and the remaining STND.HARN provisions still read coherently without them (for example the transaction type `configure`).
- **Pins (decision 3).** The term Pin in force and STND.HARN.9 together state that a later transaction whose scope holds each path of an earlier one ends the earlier pin. Test the wording on cases: the same scope twice; a wider scope after a narrower; a narrower after a wider; two overlapping scopes; scopes of several paths; file scopes. Confirm the Notes describe the effect of each truly, and that on the live ledger the new rule compares the same pins as the old one.
- **Files and STND.HARN.31 (decision 4).** STND.HARN.7, the term Content hash, and STND.HARN.31 agree on what a scope names and holds. Check STND.HARN.31 against STND.HARN.5 (README.md files and template directories) and say whether its reach is what decision 4 asks.
- **STND.HARN.32.** Precise, checkable, and its floor argument sound.
- **Entry 53.** The revision row's statement of the end of the transition is accurate against ledger entry 53 and the harness.
- **The editorial amendments.** Each is editorial under STND.IDENT.3; the rewritten Notes of STND.PROJ still explain STND.PROJ.6 and .7 truly and coherently; the new sentence of HW.GPU and HW.QPU follows from PRIME.7 and PRIME.14.

Write `REPO/review-records/round-2026-10-26/review-a.md`.

## Reviewer B: STND.DRAFT 1.5 and STND.IDENT 1.4

- **Cited document (decision 1).** The widened term matches what g.25 reads, in `REPO/harness/govharness/checks/drafting/citations.py` (`named_documents`, `naming_text`) and `REPO/harness/govharness/derive/references.py`: its exclusions, parentheses, and the word LVL0. Say whether a document of the corpus now fails STND.DRAFT.34 under the widened term. Check the new sentences of the section Checks against the code.
- **Sentence.** The new term against STND.DRAFT.4 and .16, the other provisions that count by sentences, and how the g checks split sentences (`REPO/harness/govharness/core/text.py`, `checks/drafting/`). Say what the term changes in practice.
- **STND.DRAFT.3.** "A column of a table whose entries are expressions" is decidable by a reader, and the provision is clearer for it.
- **STND.DRAFT.22, and the section Checks (L9).** The field and the wording against the code.
- **STND.IDENT.12 (decision 2).** The constitution is ratified; check that the wording covers it and every kind of STND.IDENT.1.
- **STND.IDENT.24.** Consistent with STND.IDENT.14 and GOV.37; the section Checks describes v.8 truly.

Write `REPO/review-records/round-2026-10-26/review-b.md`.

## Report

Under 900 words. Start with what you verified by running something. Then findings in three groups, Defect, Should-fix, and Optional, each numbered, each with the exact text at fault and the exact replacement wording you propose. End with any question that only the custodian can answer.
