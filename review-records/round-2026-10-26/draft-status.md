# Round of 2026-10-26: draft status

The text of the round is drafted, rehearsed, and reviewed once (`review-a.md`, `review-b.md`); the fixes are in `dispositions.md`. Nothing is applied to the live corpus. The custodian's decisions are in `decisions.md`.

## Amendments, in ledger order

| Seq (rehearsed) | Document | Revision | Class | Script | Decisions and items |
| --- | --- | --- | --- | --- | --- |
| 176 | STND.DFLT | 1.5.1 to 1.5.2 | Editorial | `apply_dflt_1_5_2.py` | 5: the Notes drop the sentence on a harness that maps the secret store |
| 177 | STND.PROJ | 1.2 to 1.2.1 | Editorial | `apply_proj_1_2_1.py` | 5: the Notes explain STND.PROJ.6 and STND.PROJ.7 as a written form, without a derived configuration |
| 178, 179 | HW.GPU, HW.QPU | 1.0.1 to 1.0.2 | Editorial | `apply_hw_remote_1_0_2.py` | 5: the Notes cite PRIME.7 and PRIME.14 for the referral of a submission, in place of STND.HARN.18 |
| 180 | STND.HARN | 1.3 to 1.4 | Minor | `apply_harn_1_4.py` | 5: STND.HARN.18 to .23, .29, .30 withdrawn; 3: terms Pin in force and Reach, STND.HARN.9; 4: STND.HARN.7 file scopes, term Content hash, new STND.HARN.31 with a transition until the five pins; L5: new STND.HARN.32; 6: end of the transition of entry 53, in the revision row |
| 181 | STND.DRAFT | 1.4 to 1.5 | Minor | `apply_draft_1_5.py` | 1: term Cited document, section Checks on g.25; M2: STND.DRAFT.3; L1: STND.DRAFT.22; L9: section Checks; L3: term Sentence |
| 182 | STND.IDENT | 1.3.3 to 1.4 | Minor | `apply_ident_1_4.py` | 2: STND.IDENT.12; new STND.IDENT.24 on withdrawn LVL0 provisions |

The scripts are in `tools/amendment-scripts/`; `apply_round_2026_10_26.py` runs them in this order. Rehearsal: `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_26.py` appends entries 176 to 182, every check passes with the two warnings the corpus already carries (`unpinned`, g.18), and the source is unchanged. Against the live corpus the drafting findings differ only by two g.8 review findings on STND.HARN.29, which is withdrawn.

`reading-copies/` holds a reading copy of each changed document, and `pairs/` the pairs of STND.HARN.28 for each: STND.HARN 6, STND.DRAFT 19, STND.IDENT 0, STND.DFLT 53, STND.PROJ 12, HW.GPU 78, and HW.QPU 932. The amendments of STND.DFLT, STND.PROJ, HW.GPU, and HW.QPU change only Notes, so their pairs are unchanged by the round; the pair review reads those that touch a changed provision.

## Left out of the round

- **A `last_provision` field (unit 0017, H1).** Adding the field means editing the front matter of every document, so one transaction per document scope; it closes only a withdrawal of a last provision that nothing cites. Not drafted; for the custodian.
- **Accepted signature (decision 7).** Deferred with signatures in general.

## Owed after the text, by the harness (code at the end of the round)

1. File scopes: `ledger append` and `record_transaction` accept a `.md` file as a scope (STND.HARN.7), and the content hash lists each file once, under the first path of the scope that reaches it (term Content hash).
2. Pins in force: the ledger check drops a pin that a later transaction's scope covers, and `append` refuses only a scope that overlaps an older pin without covering each of its paths (STND.HARN.9).
3. The check `unpinned` fails instead of warning (STND.HARN.31).
4. A new check `checked-by`: every `checked_by` key is `review` or a check key (STND.HARN.32).
5. v.5 tests the adopter field only where `status` is adopted or ratified (STND.IDENT.12).
6. v.8 reads the field `withdrawn` of LVL0 for the provisions of its parts (STND.IDENT.24).
7. The drafting checks read the cells of defining tables, except the columns whose entries are expressions, named by heading (STND.DRAFT.3).
8. The checks that end a sentence at a semicolon or a colon, or that do not end one at a period before a lowercase letter or a backtick, follow the term Sentence, or the record says why not.
9. `references` derives a row for a document named by its identifier alone, with the exclusions of the term Cited document, and g.25 fails only where the table lacks it, no longer asking for a citation behind the name (decision 1, as clarified). Also: a citation of a withdrawn identifier counts for the document that withdrew it. The rehearsal showed the gap: a revision row that cited STND.HARN.18 in another document counted as a citation of STND.HARN until STND.HARN 1.4 withdrew it, and then left a row that nothing cited. The drafts avoid it by not citing withdrawn identifiers in other documents.
10. Then the five transactions that pin `KNOW`, `TAG`, `_PROJECT`, `STND/_doc.md`, and `README.md`, each with its own scope, after STND.HARN 1.4 (decision 4).
11. The harness README and the reading copies in `rendered/`.

## Order of application

The harness code of the items above lands before the round is applied, so that STND.HARN.32 does not fail on its own key `checked-by` and the check of each new provision exists when the provision does. Then the seven transactions of the round, then the five pins of item 10, then item 11.

## Reviews

Done: the cold and STND.HARN.28 pair reviews A and B, and their fixes. Done: the cold verification (`verify.md`) and the reconciliation review (`reconciliation.md`), and their fixes (`dispositions.md`).
