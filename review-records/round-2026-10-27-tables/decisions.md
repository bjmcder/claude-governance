# Round of 2026-10-27 on defining tables: decisions and drafting

The custodian directed on 2026-10-27 that the open item of unit 0019 go ahead: the drafting checks read no cell of a table that a provision names in `defines`, though STND.DRAFT makes a table in a provision normative.

## Decided, for this round

1. **Mention columns.** STND.DRAFT defines Mention column, a column whose entries are the words, expressions, spellings, forms, or patterns that the provision names rather than uses; STND.DRAFT.3 uses the term in place of "a column whose entries are modals or excluded expressions"; the harness finds a mention column by its heading, and the section Representation in the harness names the headings. No field of the front matter changes.
2. **"Any actor" in STND.DFLT.18** becomes "Every actor", an editorial amendment.

## Drafted, for ratification

- STND.DFLT 1.5.3 (editorial) and STND.DRAFT 1.6 (minor): `tools/amendment-scripts/apply_tables_round_2026_10_27.py`, entries 200 and 201 in rehearsal; every check passes with the g.18 warning that the corpus already carries. The change of STND.DRAFT.3 relaxes a binding provision and raises no floor.
- Owed after the text, by the harness (unit 0020): `table_cells` reads each data cell of a defining table other than a cell of a mention column, by the headings that STND.DRAFT names.

## Trial of the reading

With the round applied and the cells of defining tables read, other than those of mention columns, the drafting checks find no defect. They add these review notices, judged here:

| Check | Provision | Cell | Judgment |
| --- | --- | --- | --- |
| g.12 | STND.PROJ.3 | "Where the human owner records that repository as part of the provisioned environment and as readable only by those whom the threat model trusts" | One condition: one record of the human owner, of two facts. No change. |
| g.14 | STND.CLASS.19 | "at most 6 months", "at most 12 months", "at most 24 months", "at most 36 months" | Each states its unit and an inclusive bound (STND.DRAFT.18). No change. |
| g.8 | STND.DFLT.8 | "Review (QA.7)" | The name of a record, a noun. No change. |
| g.8 | STND.DRAFT.7, STND.DRAFT.13 | "review" | A value of the column Class, a noun. No change. |
| g.8 | STND.IDENT.15 | "Document, register, or space of knowledge entries or tags" | A noun phrase in the column Item. No change. |
