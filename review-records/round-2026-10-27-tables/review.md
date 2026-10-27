# Cold and pair review: round of 2026-10-27 on defining tables

**Ran.** Read CUSTODIAN.md, decisions.md, the script. Rehearsed (entries 200, 201; all checks pass; the g.18 warning is the existing one). Applied to a copy in /tmp/claude-1000/review-tables-2026-10-27/c and ran verify, show, find, findings, and pairs. Listed the tables of every provision with `defines` (about 40 table shapes) and scanned each column for modals, excluded expressions, and body words. Pairs for STND.DRAFT.3 and STND.DFLT.18: 0, no conflict. STND.DRAFT.3 and the revision rows pass check 5 (one modal; condition first; no banned word; identifiers equal `instantiates`; title unchanged). No floor is raised; DFLT 1.5.3 editorial and DRAFT 1.6 minor are the right classes. "Every actor" keeps the meaning of "Any actor" (each actor is a source) and is the replacement that STND.DRAFT.17 names.

## Defect

None.

## Should-fix

1. **The headings do not all name mention columns.**
   - "Lowercase" (STND.DRAFT.1): its entries are `exact` and `review`, values of a class, as in the column Class that the heading list leaves out and the trial treats as prose. Delete "Lowercase, " from `MENTION_HEADINGS` and from the sentence in `_doc.md`.
   - "Pattern" (STND.DOCS.9): its entries are noun-phrase labels, used, and "Forms to watch" holds the mentions. Delete "Pattern, ".
   - "Form" (STND.IDENT.15, STND.CXX.14): the entries are descriptions in prose ("Mnemonics joined by dots", "Upper case, with the prefix of the project"), used. The cells would go unread. Delete ", and Form" (read "... Forms to watch, and Opening words").
   - "Replace with" and "Allowed compounds" (STND.DRAFT.17, .29, .32) are mixed: `"every" or "at least one"` is mentioned; "a stated number", "a defined role", "none" are used. Keep them only if the custodian accepts that a column is a mention column when any entry is mentioned; otherwise say so in the definition: replace "whose entries are" with "whose entries, or some of them, are".
2. **The rationale of STND.DRAFT 1.6 overstates the relaxation.** Text: "a modal or an excluded expression in a column that lists words, spellings, forms, or patterns, in the tables of STND.DRAFT.13, STND.DRAFT.17, STND.DRAFT.29, STND.DRAFT.32, STND.DRAFT.33, STND.DOCS.8, STND.DOCS.9, and STND.IDENT.3 and STND.IDENT.15 among them, needs no quotation marks, as one in the columns of STND.DRAFT.1 and STND.DRAFT.7 did not." No cell of those tables holds a modal or excluded expression except two in STND.DOCS.9, already quoted ("should", "may have"). Replacement: "...columns that list words, spellings, forms, or patterns, as in the tables of STND.DRAFT.13 and STND.DOCS.9, needs no quotation marks, as one in the columns of STND.DRAFT.1 and STND.DRAFT.7 did not; no cell of the corpus now holds one unquoted." Drop STND.IDENT.15 from the list in any case.
3. **Unnamed mention columns.** STND.JL.30 "Heading" and STND.PROJ.6 "Field" hold names mentioned; no banned word follows, so Optional.

## Optional

4. decisions.md trial: unit 0019 listed STND.IDENT.3 and STND.KNOW.4 among the imperative-looking notices; the trial table drops both without a word. Add "STND.IDENT.3 and STND.KNOW.4: no notice once the column Opening words is left out" if true, or list them.
5. decisions.md, Decided 1: the heading list is an author's draft; move it under "Drafted, for ratification".

## For the custodian

- Did the custodian rule the definition of Mention column and the heading list, or only that the open item of unit 0019 go ahead? The rationales say "ratified by the custodian" and "The custodian decided that a term ... marks the columns" before ratification (the corpus pattern for rehearsal, but the second sentence names a decision of the custodian that decisions.md records only as direction).
- Is a column with some mentioned and some used entries (Replace with) a mention column?
