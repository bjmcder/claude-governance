# Open items

This file lists the work the custodian has directed, and the items a ratified round left open. It replaces the open items of the former HANDOFF.md (see git history). To close an item, do it and remove its line. The record of the work stays in git and in `review-records/`.

## Harness, in the custodian's order

1. **Installation, the custodian's own step.** The steps are in `tools/install-tests.md`:
   1. Install `socat`. The sandbox needs it, and `environment --check` reports it missing.
   2. Derive the configuration from the merged harness, and install it as root, as INSTALL.md states.
   3. Run the three installation tests, and record the results in unit 0008.
   4. Append the configure entry that ends the transition of ledger entry 53 for STND.HARN.18.
   5. In `/etc/governance/signer.json`, set a `head` pin, and move it forward after each transaction that must not be lost, such as a revocation (unit 0016; the command is in harness/README.md, Signatures). Without it, the end of the ledger can be cut and `verify` still passes. When SIGNR is founded, found it and set `anchor` together, the register first.

   Whether the transition of entry 53 for STND.HARN.26 to .28 has ended is also for the custodian to record.

Known limits, not scheduled (custodian, 2026-10-25): the guard does not read the forms R2 to R10 of `review-records/harness/rereview-unit-0015.md`. These are computed or patterned program words, `env -S`, and git settings or variables given in other forms; `merge-file` operands; `ed` and `ex` scripts; aliases; sed's `w` and `e`. They are listed in `harness/records/units/0015-guard-fixes.md` and the guard's coverage table. A later unit may take them up if the custodian asks.

## Corpus, for a later round

The first two the custodian deferred on 2026-10-25; the others arose from units 0013, 0016, and 0017, which made the harness follow the corpus as written. Each unit record holds draft wording.

- **Foreign interfaces in STND.CODE.** Add one STND.CODE provision on foreign interfaces, with one definition of Foreign interface (now defined in five standards) and one of Lock file (in STND.PY and STND.RUST). It replaces the callback, ownership, and lock-file rules that now stand alike in several language standards (GOV.31). This is decision 26 of `review-records/round-2026-10-25-close/decisions-final.md`.
- **STND.OFFLD.31 and the first filling of caches and memory**, which STND.PERF.12 names. Consider it at STND.OFFLD's next minor amendment (decision 27).
- **STND.DRAFT and g.25 (unit 0013).** An editorial amendment of STND.DRAFT's informative text on the harness, saying that g.25 also fails when the text names a document by its bare identifier without citing it. With it, the custodian decides whether the Terms should say that a document named in the text, or written alone in parentheses, is a cited document; g.25's defect class rests on the reading of STND.DRAFT.34 given in decision 22 (`harness/records/units/0013-references-bare-names.md`).
- **STND.HARN.9, pins of overlapping scopes (unit 0016).** As written, a transaction of another scope over the same files does not replace a pin, so a pinned scope cannot be widened or narrowed, and `append` refuses such a transaction. Whether a later pin over the same files should replace the older one is for the custodian; the draft wording is in `harness/records/units/0016-ledger-fixes.md`.
- **The term Accepted signature, with STND.HARN.10 (unit 0016).** As written, an open `all` row accepts its key on every ledger and cannot be closed, so a key registered for `all` cannot be retired short of removing its row. Whether a row for one ledger should override the `all` row is for the custodian; draft wording in the same record.
- **Files under no ledger scope (unit 0017, M1).** `KNOW/`, `TAG/`, `_PROJECT/`, `STND/_doc.md`, and `README.md` change with no transaction; the check `unpinned` warns. Whether STND.HARN should make such a file FAIL; one transaction pinning them would come first.
- **Drafts and the adopter field (unit 0017, M4).** STND.IDENT.12 asks every document to name its adopter, a draft included, and v.5 follows it. Whether it should read "that is adopted or ratified".
- **Expression columns and STND.DRAFT.3 (unit 0017, M2).** An exception for table columns that list expressions, so that the harness can read the prose cells of defining tables too.
- **An uncited trailing withdrawal (unit 0017, H1).** v.8 now catches a cited identifier that no longer resolves, but not a last provision that nothing cites. A `last_provision` field (STND.IDENT.14), or history rows that name each withdrawn identifier, would close it.
- **Withdrawn LVL0 provisions (unit 0017).** LVL0 has no `withdrawn` field, and STND.IDENT.14 does not say where a withdrawn part provision is listed. A cited, deleted LVL0 provision would now fail v.8 with no way to list it.
- **STND.DRAFT.22's `checked_by` (unit 0017).** It should name v.8 beside l.1, since v.8 now resolves cited identifiers.
- **`checked_by` keys (unit 0017, L5).** A STND.HARN rule that every `checked_by` key names a registered check, outside STND.DRAFT and STND.IDENT too.
- **STND.DRAFT, section Checks (unit 0017, L9).** Reword "the provision concerned" as "the provision of this standard that the check enforces", the reading the harness uses.
- **The term Sentence (unit 0017, L3).** A defined term in STND.DRAFT, which g.4 and g.18 count by.
