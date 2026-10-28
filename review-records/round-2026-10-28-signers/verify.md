# Verification of the fixes (STND.HARN 1.5, unit 0021)

## What I ran

Read decisions.md, review.md, review-unit-0021.md, the script, and `git diff HEAD~1 HEAD`. Copied `harness/governance` to `/tmp/claude-1000/v1/governance`, applied the script: `verify` passes (g.18 warning only, as in the corpus), and `show` of STND.HARN.7, .10, .13 reads as the script says. Diffed the applied `_doc.md` against HEAD: only revision, the term, one Notes paragraph, and the 1.5 row changed; 8 files differ in the corpus copy as expected. `python3 -B -m unittest tests.ledger.test_signatures`: 14 tests, OK. On a scratch copy I reverted four code fixes one at a time (armor check, `_refuse_all` in `with_signer_closed`, casefold in `read_register`, `applies` for required `all` rows): each fails a test. The repo is unedited except this file.

## Checks

1. Dispositions: S1, O3, O4, S2 and findings 1 to 4, 6, 13 are done as the table says; finding 5 is rightly not taken. Finding 3 is documented in the docstring and the README row. Nothing else changed in the code diff.
2. Wording: "open on the governance ledger" in HARN.7 and HARN.13 matches `active_signers` (Last entry "none" and Ledger governance) and `signatures.py` line 187. The Notes sentence is true: a register change is a governance-ledger transaction (HARN.13). Consistent with HARN.10 and the term (no "all"). Drafting rules: modals per sentence and per provision are within limits, conditions come first, and none of the banned words appears in the three bodies.
3. Revision row and rationale: they claim only decision 1 as the custodian's decision. The S1 reading is stated as the harness's existing reading, not as a ruling.
4. Code: correct and tested. The README (step 6 and the `close-signer` row) matches the code.

## Findings

No Defect and no Should-fix.

Optional 1. The rationale begins "ratified by the custodian on 2026-10-28" over the whole READING, which includes the S1 reading that the custodian has not yet ruled. The text is true only because the script is applied after ratification (S2, CUSTODIAN.md step 7). No change is needed if that order holds. Otherwise replace "ratified by the custodian on {DATE}" with "adopted on {DATE}".

Optional 2. The unit 0021 record says "each reverted alone on a scratch copy, now fail a test"; I confirmed this for four of the guards. I did not check the remaining mutations.
