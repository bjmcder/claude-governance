# Open items

This file lists the work the custodian has directed, and the items a ratified round left open. It replaces the open items of the former HANDOFF.md (see git history). To close an item, do it and remove its line. The record of the work stays in git and in `review-records/`.

## Harness, in the custodian's order

1. **Unit 0013, the References check.** The harness check of References (g.25) also reads bare document names, so that the table and the check agree. It reads the documents that STND.DRAFT.34 asks to hold References (LVL1 to LVL3), and it skips the Revision History and tables of example identifiers, as `tools/check_refs.py` does. It is a defect-class check, and `verify` passes on the live corpus (definition of done of 2026-10-25, item 8).
2. **QA.8 code review of the whole harness**, after unit 0013, by an agent of another configuration. Every High and Medium finding is fixed and verified (item 9).
3. **Installation, the custodian's own step.** The steps are in `tools/install-tests.md`:
   1. Install `socat`. The sandbox needs it, and `environment --check` reports it missing.
   2. Derive the configuration from the merged harness, and install it as root, as INSTALL.md states.
   3. Run the three installation tests, and record the results in unit 0008.
   4. Append the configure entry that ends the transition of ledger entry 53 for STND.HARN.18.

   Whether the transition of entry 53 for STND.HARN.26 to .28 has ended is also for the custodian to record.

## Corpus, for a later round (custodian, 2026-10-25)

- **Foreign interfaces in STND.CODE.** Add one STND.CODE provision on foreign interfaces, with one definition of Foreign interface (now defined in five standards) and one of Lock file (in STND.PY and STND.RUST). It replaces the callback, ownership, and lock-file rules that now stand alike in several language standards (GOV.31). This is decision 26 of `review-records/round-2026-10-25-close/decisions-final.md`.
- **STND.OFFLD.31 and the first filling of caches and memory**, which STND.PERF.12 names. Consider it at STND.OFFLD's next minor amendment (decision 27).
