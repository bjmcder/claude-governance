# Second cold verification of the round of 2026-10-26

## Ran

- Applied the six scripts to a copy (`/tmp/claude-1000/verify2/gov`): entries 176 to 182; `verify` passes, warnings only `unpinned` (5 paths) and g.18.
- Read on that copy every row of the tables "Verification" and "Reconciliation" of `dispositions.md` and the seven answers of `decisions.md`: each reads as stated (HARN.31 and .32, Pin in force, Reach, Content hash, Sentence, DRAFT.3, DRAFT.22, IDENT.12 and .24, the Checks sentences, the DFLT Notes). Answer 6 holds: HARN.32 instantiates GOV.37. Answer 4 holds: no `last_provision`.
- Grep of the copy: STND.HARN.18 to .23, .29, .30 remain only in HARN `withdrawn` and its revision rows.
- Wrote a script that lists bare document identifiers outside quotes, code spans, References, and revision history, against each References table: the only non-LVL0 hits are an Example table (STND.IDENT) and the template `_PROJECT/NAME`, so the rationale's "no document of the corpus changes" holds.
- Read afresh, against "What every reviewer checks": the DRAFT Checks sentence and rationale 181; the HARN term, Notes, .31, .32, row, and rationale; the IDENT row and rationale; the DFLT rationale. Modals, banned words, titles, classes, and American English pass.

## Defect

None.

## Should-fix

1. **HARN Notes, floor argument of STND.HARN.31, overstates.** Text: "it asks no new act of the human owner, of a project, or of the custodians, because the transaction that GOV.36 already asks for each change pins the file whose scope it reaches". The custodians must record five transactions (the revision row's transition) before the FAIL stops. Also "pins the file whose scope it reaches" reads backward. Replace with: "it asks no decision of the human owner and no new act of a project, and of the custodians only the transactions that pin the files now outside every scope, because the transaction that GOV.36 already asks for each change records a scope that reaches the file, as an adoption records the directory of the document it adopts".
2. **DRAFT rationale, floor argument.** Text: "it asks no decision of the human owner and no act of a project beyond that row." Decision answer 5 says the command writes the row. Replace with: "it asks no decision of the human owner and no new act of a project, because the command references writes the row".
3. **HARN row, Content hash.** Text: "under the first of its paths that reach it". The term says "the first, in code-point order,". Replace with: "under the first, in code-point order, of its paths that reach it".

## Optional

1. **HARN rationale.** "STND.HARN.9 compares the same pins as before wherever no two scopes overlap" is loose: two identical scopes overlap yet compare alike. Replace with: "wherever no scope of a later transaction reaches each path of a different earlier scope".
2. **DRAFT Checks.** Its first clause, "A document that the text names by its identifier alone is a cited document, so", restates the term (GOV.31). Replace the sentence with: "The command derives a row for each document that the text names by its identifier alone, as for a citation, and g.25 fails where the table lacks it, whether or not a citation backs the name."
3. **DFLT rationale** is sound (STND.DFLT.22 unchanged, stated). No change.
4. Entry 53 and STND.HARN.23 (earlier S2) is answered by the row's clause scoping the transition; keep.
