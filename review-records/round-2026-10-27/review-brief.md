# Cold and STND.HARN.28 pair review of the round of 2026-10-27: brief

Two reviewers, each over one package. You are an agent of another configuration than the author, and you have not seen the drafting. Read cold: judge the text against the corpus and the custodian's decisions, not against the author's reasons.

## Before you start

- REPO is `/home/brianm/projects/utils/governance-harness`.
- Read `REPO/CUSTODIAN.md` (the standing process and directions), then `REPO/review-records/round-2026-10-27/decisions.md` (what the custodian decided) and `draft-status.md` (what is drafted, and what the drafting decided beyond the decisions).
- Write only your report. Do not edit the corpus, the scripts, or any other file. Keep scratch files in your own new subdirectory of `/tmp/claude-1000/`. Use no network.

## The round

`REPO/tools/amendment-scripts/apply_round_2026_10_27.py` applies ten transactions in ledger order, entries 188 to 197 in rehearsal. Each amendment's script holds its text, revision row, and rationale.

From `REPO/harness/`:

1. Rehearse: `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_27.py`. It prints the path of the rehearsed copy, which is deleted afterwards; to keep one, make a directory `<dir>`, copy `governance/` into `<dir>/governance`, and run `python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_round_2026_10_27 as R; R.apply('<dir>/governance')"`.
2. On a copy: `python3 -B -m govharness verify <copy>`, `python3 -B -m govharness show <copy> ID`, `python3 -B -m govharness find <copy> WORDS`, and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`.
3. Reading copies after the round: `REPO/review-records/round-2026-10-27/reading-copies/`. The documents before the round: `REPO/rendered/`. The pairs of STND.HARN.28: `pairs/` and `pairs-changed.md`.
4. A provision of the live corpus, before the round: `python3 -B -m govharness show governance ID`.

## What every reviewer checks

- **Decisions.** Each amendment does what `decisions.md` records, no more and no less. Report each change that `draft-status.md` lists under "What the drafting decided" that you judge should go to the custodian.
- **No outcome lost.** For each withdrawn provision and each removed sentence, find the outcome in the text after the round, in STND.CODE, STND.DEPS, or what the language standard keeps. Say where an outcome is lost, narrowed, or widened, and whether the rationale says so truly.
- **No restatement (GOV.31).** What a language standard keeps adds language content to STND.CODE or STND.DEPS and does not restate it.
- **STND.DRAFT.** In each new or changed provision: one modal per sentence, and at most three per provision, in a bundle never applied apart (STND.DRAFT.28); each condition before its clause, one per sentence; none of the body words "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any"; titles of six words or fewer, not verb-initial, distinct across the corpus; body identifiers equal `instantiates` plus `refers_to`. Is each provision decidable by a reviewer from the source and the contract of the interface?
- **Notes.** No obligation stated in the indicative, no narration of drafting, American English, nothing that names a tool or a version in a provision. Each fact of a Note is one that the earlier Notes stated with its source, or is marked unverified.
- **Class and record.** The class under STND.IDENT.3 is right; the revision row and the rationale say what changed, and nothing more; the rationale does not write that the custodian has ruled something not yet ruled (CUSTODIAN.md, item 3); the class onsets are right under STND.CLASS.10.
- **Pairs (STND.HARN.28).** Confirm `pairs-changed.md` for your package. For each listed pair, say whether the two provisions address the same matter and whether they conflict. For each changed provision, say whether another adopted document addresses its matter, and whether the two conflict.
- **Citations.** No citation of a withdrawn identifier remains anywhere in the corpus outside revision histories and the field `withdrawn`, no References table is wrong, and the term Foreign interface and the term Lock file are each defined once.

## Reviewer A: STND.CODE 1.3, STND.DEPS 1.1, STND.STDC 1.2, STND.CXX 1.3, and the editorial amendments of STND.FTN, STND.MPI, STND.OMP

- **The term Foreign interface.** It covers each part of the five terms that it replaces (STND.CXX, STND.STDC, STND.PY, STND.JL, and the Foreign function interface of STND.RUST, all in `REPO/rendered/`), the structured block of a parallel directive among them, and reads sensibly for C, Fortran, Lean, and a hardware description.
- **STND.CODE.22 to .26.** Precise and decidable; each sentence's reach in each language; the argument of each bundle (STND.DRAFT.28); the condition "Unless the contract of a foreign interface states that the interface carries a failure across the foreign code and on to code of the work"; and whether STND.CODE.24 and the Python and Julia interrupt rules (STND.PY.35, STND.JL.39) conflict.
- **STND.DEPS.12 and the term Lock file.** The term fits a Julia manifest, a Python lock file, and a Rust lock file; the rule leaves nothing that STND.PY.33 and STND.JL.4 asked; what it drops from STND.RUST.30 is what decision 3 asks.
- **STND.STDC and STND.CXX.** The C reading of STND.STDC.1 still reads correctly without a C term Foreign interface; STND.CXX.5, .21, and the Notes read coherently without STND.CXX.20 and .22; the Notes of STND.MPI, STND.OMP, and STND.FTN cite the right provision of STND.CODE.

Write `REPO/review-records/round-2026-10-27/review-a.md`.

## Reviewer B: STND.PY 1.2, STND.RUST 1.2, STND.JL 1.3

- **What each language keeps.** STND.PY.35, STND.RUST.24, .25, .27, .30, and STND.JL.38, .39: each keeps only language content, reads correctly beside the STND.CODE provision that it cites, and keeps the outcome that it had for its language.
- **The Rust term.** Each use of "foreign function interface" in STND.RUST is gone or rightly replaced, and the section of STND.RUST.24 to .27 is renamed.
- **Lock files.** STND.JL Terms' "the manifest file of an environment is its lock file", the Notes on versions in STND.PY and STND.JL, and the Notes on packages in STND.RUST, against STND.DEPS.12 and the remaining STND.RUST.30.
- **Notes.** The rewritten Notes on foreign interfaces of the three standards keep each sourced fact with its source, and cite STND.CODE.22 to .26 correctly by sentence.
- **Onsets.** STND.PY.35 and STND.JL.39 from CSQ2, STND.JL.38 and STND.RUST.27 from CSQ3, and the class onset paragraphs of the three standards.

Write `REPO/review-records/round-2026-10-27/review-b.md`.

## Report

Under 900 words. Start with what you verified by running something. Then findings in three groups, Defect, Should-fix, and Optional, each numbered, each with the exact text at fault and the exact replacement wording you propose. End with any question that only the custodian can answer.
