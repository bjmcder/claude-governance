# Open items

This file lists the work the custodian has directed, and the items a ratified round left open. It replaces the open items of the former HANDOFF.md (see git history). To close an item, do it and remove its line. The record of the work stays in git and in `review-records/`.

## Corpus, for a later round

The first the custodian deferred on 2026-10-25; the second on 2026-10-26, with signatures in general; the third arose from unit 0019. The round of 2026-10-27 closed decision 26 of 2026-10-25, on foreign interfaces and lock files (`review-records/round-2026-10-27/`). The round of 2026-10-26 closed the other questions of units 0013, 0016, 0017, and 0018 (`review-records/round-2026-10-26/`), and the custodian dropped the field `last_provision` (unit 0017, H1).

- **STND.OFFLD.31 and the first filling of caches and memory**, which STND.PERF.12 names. Consider it at STND.OFFLD's next minor amendment (decision 27).
- **The term Accepted signature, with STND.HARN.10 (unit 0016).** As written, an open `all` row accepts its key on every ledger and cannot be closed, so a key registered for `all` cannot be retired short of removing its row. Deferred until a signer register is founded, since the work's assurance does not now require signatures; draft wording in `harness/records/units/0016-ledger-fixes.md`.
- **The prose cells of defining tables (unit 0019).** STND.DRAFT makes a table in a provision normative, but the harness reads no cell of a table that a provision names in `defines`. Reading the cells of every column except those that list words would find, among others, lowercase modals in the column Normative Language entry of STND.DRAFT.1 (defects in STND.DRAFT itself), "Any actor" in the tables of STND.DFLT.18 and STND.THRT.2, and imperative-looking words in STND.DRAFT.7, .13, STND.DFLT.8, STND.IDENT.3, and STND.KNOW.4 (`harness/records/units/0019-round-2026-10-26.md`). A round would decide which columns are data, for example by naming them in STND.DRAFT, and fix the prose cells.
