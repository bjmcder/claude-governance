# Cold verification of the round of 2026-10-26

## Verified by running

- Applied the round to a scratch copy (`/tmp/claude-1000/verify26/gov`): entries 176 to 182, `verify` passes with the two known warnings (`unpinned`, g.18). The same on each intermediate state, after every one of the six scripts: all pass, so no state of the round cites a withdrawn identifier.
- `findings.py` on the whole corpus, before and after: the only difference is the two g.8 findings on the withdrawn STND.HARN.29 (as `draft-status.md` says).
- Searched the copy for STND.HARN.18 to .23, .29, .30 in every form: they remain only in the STND.HARN field `withdrawn` and revision rows (and in the ledger). The terms Derived configuration and Refer, and the HARN terms that only they used, are gone with no remaining use in STND.HARN. Outside the corpus they remain in `harness/README.md`, `OPEN-ITEMS.md`, `docs/CORPUS.md` and unit records (the README is owed).
- Pins: from the rehearsed ledger, the old set (latest entry per scope) and the Pin in force set are both 41 and identical. The one multi-path scope (entry 46) overlaps nothing.
- `pairs` on STND.HARN, STND.DRAFT, and STND.IDENT: no changed provision on a changed side; `pairs-changed.md` is confirmed.
- Re-split every provision below LVL0 by the new term Sentence: no sentence holds more than one modal (the one hit is a table row, which the term splits by cell).
- v.8, run on a copy: a citation in a body of STND.HARN.99 fails; the description in the IDENT Checks is true.

## Dispositions

All 22 rows read on the copy as stated and answer their finding: A1 to A11, B-D1, D2, S1 to S7, O1, O2. Two qualifications: B-S1 and B-D1 are fixed in the term but leave the contradiction in Defect 1 below; B-S4 is as the row says (code differences owed).

## Defect

1. **The term Cited document and the section Checks disagree on what a bare name needs.** The term: "or named in their text by its identifier alone"; so a document named bare is cited and DRAFT.34 asks for its row. Checks: "g.25 also fails where the text names a document by its bare identifier and cites it nowhere; a citation of the document fixes the table". By the term the name is already a citation; and a row added with no citation fails g.25 ("not cited"). Decision 1 asked: "g.25 fails on a document so named that the References table does not list". The 181 rationale ("asks of a document only a row of its References table") is also wrong under the code: the fix is a citation, then the row. Replace the last sentence of Checks with: "That command derives a row only from a citation, by a provision, a locator, a reference field, or the document's identifier written alone in parentheses, so g.25 also fails where the text names a document by its identifier alone and no such citation backs the name; the citation derives the row." In the rationale, replace "asks of a document only a row of its References table for each document that its text names" with "asks of a document a citation, and so a row of its References table, for each document that its text names". Question 1 below.

## Should-fix

1. **Content hash order.** "ordered by the first path of the "scope" that reaches the file" does not say first in what order. The code sorts the paths. Replace with "ordered by the first, in code-point order, of the paths of the "scope" that reach the file".
2. **Entry 53 and STND.HARN.23.** Entry 53's transition also names STND.HARN.23, which 1.4 withdraws. In the row, replace "and for STND.HARN.18 because it is withdrawn" with "and for STND.HARN.18 and STND.HARN.23 because they are withdrawn".
3. **Notes of STND.HARN, Reach used on scopes.** "neither reaching the other" applies the term to a scope, not a path. Replace with "neither reaching each path of the other".
4. **STND.HARN.32 and STND.HARN.31 on their own text.** Until the code makes the check `checked-by`, STND.HARN.32's `checked_by` key is one the harness does not make, so the provision fails itself; the same for the unpinned files until the five pins. The row has a transition for the files only. Either apply after the code (`draft-status.md`, owed 3 and 4, then names that order), or add to the row: "the check `checked-by` applies from the revision of the harness that makes it".

## Optional

1. `OPEN-ITEMS.md` line 6 says each item "is drafted as that record says, except Accepted signature"; H1 (`last_provision`) is not drafted (`draft-status.md`), and L9 follows the harness's reading, not the line's wording. Correct when the item is closed.
2. "Reach" beside STND.DFLT.25 ("Bounds of reach"): no clash. The term is defined in STND.HARN only, in the sense of a scope and a path; DFLT.25 and the Lexicon ("privileges and reach") use the word of ordinary speech for access, and STND.HARN uses it only in the defined sense. The AGENT column "Reach" is a heading. Keep.
3. The rationales of 180 to 182 say the floor arguments "are put to the custodian at ratification"; recorded at ratification, that reads as stale. Drop the clause; the arguments stand in the Notes and rationale.
4. STND.HARN.32 instantiates GOV.38; GOV.37 (stable check keys, as STND.HARN.16) fits no better. Custodian's choice (review A, 10).

## Checked and sound

HARN.31 (reached by no scope, for that file), Pin in force, Reach, the HARN.9 and .7 text, HW.GPU and HW.QPU (the sentence follows PRIME.7 and PRIME.14, restating only the referral), STND.PROJ Notes (STND.PROJ.6 and .7 explained truly, no derived configuration), STND.DFLT Notes, DRAFT.3 and the columns of DRAFT.1 and .7 it exempts, DRAFT.22 with v.8, IDENT.12 (adopted or ratified, every kind; planned and draft exempt, as decision 2's words give), IDENT.24 (with GOV.37 and IDENT.14), classes, titles (unique, short), modals, banned words, identifiers equal to `instantiates` plus `refers_to`, no ruling written that is not made. Reading copies match the rehearsed text.

## For the custodian

1. Defect 1: must a bare name be backed by a citation (design ii, as the harness is and as the draft says), or does a row alone satisfy STND.DRAFT.34 (design i, as decision 1 reads)? The text must follow the answer.
2. The list at the end of `dispositions.md` omits two matters: the `last_provision` field (H1, left out of the round), and the basis GOV.38 of STND.HARN.32. Add both.
