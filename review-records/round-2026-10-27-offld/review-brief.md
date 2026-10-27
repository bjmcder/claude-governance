# Cold and pair review of the round of 2026-10-27 on offloaded work: brief

You are an agent of another configuration than the author, and you have not seen the drafting. Read cold.

- REPO is `/home/brianm/projects/utils/governance-harness`. Read `REPO/CUSTODIAN.md`, then `REPO/review-records/round-2026-10-27-offld/decisions.md`, then the script `REPO/tools/amendment-scripts/apply_offld_round_2026_10_27.py`.
- From `REPO/harness/`: rehearse with `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_offld_round_2026_10_27.py`. To keep a copy, make `<dir>`, copy `governance/` into `<dir>/governance`, and run `python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_offld_round_2026_10_27 as R; R.apply('<dir>/governance')"`. On a copy: `verify`, `show <copy> ID`, `find <copy> WORDS`, `pairs <copy> STND.OFFLD`, and `PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex>'`. The documents before the round: `REPO/rendered/STND.OFFLD.md` and `REPO/rendered/STND.PERF.md`.
- Write only your report. Edit no other file. Keep scratch files in a new subdirectory of `/tmp/claude-1000/`. Use no network.

Check:

1. **The change.** STND.OFFLD.31 now names the costs that STND.PERF.12 names, and the two read consistently, with STND.PERF.14 and STND.OFFLD.26 to .30. Say whether "costs of first use" in place of "costs of a first submission" changes the reach beyond what decision 27 names, and whether that is sound. Say whether "the first filling of caches and memory" is decidable for offloaded work, and whether the Notes of STND.OFFLD on memory that migrates on demand still read truly.
2. **STND.DRAFT.** One modal per sentence; condition before clause; none of the body words "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any"; body identifiers equal `instantiates` plus `refers_to`.
3. **Notes.** No obligation in the indicative, no narration of drafting, American English; each fact sourced or marked unverified.
4. **Class and record.** Minor for STND.OFFLD and editorial for STND.PERF under STND.IDENT.3; the revision rows and the rationales say what changed and nothing more; the rationale writes nothing as ruled that the custodian has not ruled; onsets right under STND.CLASS.10.
5. **Pairs (STND.HARN.28).** The five pairs of STND.OFFLD.31 (HW.22, HW.CPU.4, HW.GPU.4, HW.QPU.8, NUMER.17): same matter, and any conflict. Any other adopted document that addresses the costs of first use of offloaded work.
6. **Citations.** No References table is wrong.

Write `REPO/review-records/round-2026-10-27-offld/review.md`, under 600 words: what you ran, then findings as Defect, Should-fix, and Optional, numbered, each with the exact text at fault and the exact replacement wording; end with any question that only the custodian can answer.
