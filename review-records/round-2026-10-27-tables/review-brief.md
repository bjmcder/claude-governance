# Cold and pair review of the round of 2026-10-27 on defining tables: brief

You are an agent of another configuration than the author, and you have not seen the drafting. Read cold.

- REPO is `/home/brianm/projects/utils/governance-harness`. Read `REPO/CUSTODIAN.md`, then `REPO/review-records/round-2026-10-27-tables/decisions.md`, then the script `REPO/tools/amendment-scripts/apply_tables_round_2026_10_27.py`.
- From `REPO/harness/`: rehearse with `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_tables_round_2026_10_27.py`. To keep a copy, make `<dir>`, copy `governance/` into `<dir>/governance`, and run `python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_tables_round_2026_10_27 as R; R.apply('<dir>/governance')"`. On a copy: `verify`, `show <copy> ID`, `find <copy> WORDS`, `pairs <copy> STND.DRAFT`, and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`. The documents before the round: `REPO/rendered/STND.DRAFT.md` and `REPO/rendered/STND.DFLT.md`.
- The harness does not yet read the cells (unit 0020 follows the text); judge the text, and report a mismatch with the code only where the text is wrong or unclear.
- Write only your report. Edit no other file. Keep scratch files in a new subdirectory of `/tmp/claude-1000/`. Use no network.

Check:

1. **The term Mention column.** Decidable by a reader; covers each column of the defining tables of the corpus whose entries are mentioned (list the provisions with a field `defines` on a copy, and read each table), and no column whose entries are used. Say whether each heading that the section Representation in the harness names is a mention column in every table where it occurs, and whether a mention column of the corpus has a heading that it does not name.
2. **STND.DRAFT.3.** Reads correctly with the term; what it relaxes, and that the rationale says so truly.
3. **STND.DFLT.18.** "Every actor" keeps the meaning of "Any actor" in the column Source; the amendment is editorial under STND.IDENT.3.
4. **The trial judgments** in `decisions.md`: each is sound.
5. **STND.DRAFT.** One modal per sentence; condition before clause; none of the body words "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any"; body identifiers equal `instantiates` plus `refers_to`; titles unchanged.
6. **Class and record.** The revision rows and rationales say what changed and nothing more; nothing written as ruled that the custodian has not ruled; no floor raised.
7. **Pairs (STND.HARN.28).** For STND.DRAFT.3 and STND.DFLT.18, any pair whose changed side is a changed provision, and any conflict.

Write `REPO/review-records/round-2026-10-27-tables/review.md`, under 600 words: what you ran, then findings as Defect, Should-fix, and Optional, numbered, each with the exact text at fault and the exact replacement; end with any question that only the custodian can answer.
