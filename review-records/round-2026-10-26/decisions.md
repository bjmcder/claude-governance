# Decisions of the custodian, round of 2026-10-26

The custodian's answers of 2026-10-26 to the questions that units 0013, 0016, 0017, and 0018 left for the corpus (`OPEN-ITEMS.md`). These decide what the round drafts. They do not ratify any text: each amendment is still drafted, self-checked, rehearsed, reviewed, and presented for ratification under the standing process of `CUSTODIAN.md`. Draft wording, where it exists, is in the unit record named.

## Decided, for this round

1. **Cited document (STND.DRAFT; unit 0013).** Widen the term: a document named in the text by its identifier, or written alone in parentheses, is a cited document. Add the editorial note that g.25 fails on a document so named that the References table does not list. Clarified on 2026-10-26, after the verification and reconciliation reviews: a References row alone meets STND.DRAFT.34 for such a name, so the harness derives the row, and g.25 asks for no citation behind the name.
2. **Adopter of a draft (STND.IDENT.12; unit 0017, M4).** Exempt drafts: only a document that is adopted or ratified names its adopter. v.5 follows.
3. **Pins of overlapping scopes (STND.HARN.9; unit 0016, M4).** A pin gives way to any later governance-ledger transaction whose scope covers each of its paths. The harness then drops the superseded pin from the ledger check, and `ledger append` narrows its refusal.
4. **Files under no scope (STND.HARN; unit 0017, M1).** One transaction first pins `KNOW/`, `TAG/`, `_PROJECT/`, `STND/_doc.md`, and `README.md`. Then STND.HARN makes a Markdown file under no scope a FAIL (GOV.36), and the check `unpinned` fails instead of warning.
5. **Provisions on a derived configuration (unit 0018).** Withdraw STND.HARN.18 to STND.HARN.23, STND.HARN.29, and STND.HARN.30, and amend what cites them: STND.DFLT.22, the Notes of STND.DFLT, STND.PROJ, HW.GPU, and HW.QPU. Keep STND.PROJ.6 and STND.PROJ.7, the fields of a written remote-write authorization (PRIME.7).
6. **The transition of ledger entry 53.** Record its end in one transaction, with no change of text: for STND.HARN.26 to STND.HARN.28 because the harness implements them (checks m.1 and m.2, and `pairs`), and for STND.HARN.18 because the harness derives no configuration.

## Deferred

7. **Accepted signature, with STND.HARN.10 (unit 0016, M1).** Deferred until a signer register is founded. The custodian's reason: the work's assurance does not now require signatures, and founding a register would add development overhead, so no register is planned and signature work in general is deferred. Until then the term stands as written, and the harness keeps refusing a row that only seems to close an `all` key.

## Not decisions, also in scope

These items of `OPEN-ITEMS.md` need no ruling and have draft wording in unit 0017: STND.DRAFT.3 and expression columns (M2); a `last_provision` field in STND.IDENT.14 (H1); where LVL0 lists a withdrawn provision of a part; v.8 in STND.DRAFT.22's `checked_by`; a STND.HARN rule that every `checked_by` key names a registered check (L5); the rewording of STND.DRAFT's section Checks (L9); and the term Sentence (L3).

## Answers of 2026-10-26 to the questions of `dispositions.md`

1. **Pins (decision 4).** Five transactions, one per path, after STND.HARN 1.4, with the transition in its revision row.
2. **Entry 53 (decision 6).** Recorded in the revision row and rationale of STND.HARN 1.4.
3. **The section Checks of STND.DRAFT.** A finding in another document fails where a binding provision of STND.DRAFT names the check.
4. **The field `last_provision` (unit 0017, H1).** Dropped.
5. **Floor arguments.** To be the most flexible, with the least burden on the human owner and on project owners. The arguments now state that STND.HARN.31, STND.HARN.32, STND.IDENT.24, and the widened term ask no decision of the human owner and no new act of a project: the transaction that GOV.36 already asks pins a file, the references row is written by the command, and the other two bind only the harness or the custodians.
6. **The basis of STND.HARN.32.** GOV.37.
7. **Ratification.** After one more cold verification of the last fixes, if it finds no defect.
