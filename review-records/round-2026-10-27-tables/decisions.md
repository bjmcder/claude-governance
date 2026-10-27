# Round of 2026-10-27 on defining tables: decisions and drafting

The custodian directed on 2026-10-27 that the open item of unit 0019 go ahead: the drafting checks read no cell of a table that a provision names in `defines`, though STND.DRAFT makes a table in a provision normative.

## Decided, for this round

1. **Mention columns.** A term of STND.DRAFT marks the columns whose entries a provision mentions, STND.DRAFT.3 uses it, and the harness finds such a column by its heading, which STND.DRAFT names; no field of the front matter changes.
2. **"Any actor" in STND.DFLT.18** becomes "Every actor", an editorial amendment.

## Drafted, for ratification

- STND.DRAFT defines Mention column, a column of a table in a provision whose entries are the words, expressions, spellings, forms, or patterns that the provision names rather than uses; STND.DRAFT.3 reads "Outside a mention column"; the section Representation in the harness names the headings Modal, Normative Language entry, Expression, Read as, Qualifier, Word, British, American, Not used, Used, and Opening words, and says that a column whose entries are mentioned in part is no mention column, its mentioned entries being quoted.
- STND.DFLT 1.5.3 (editorial) and STND.DRAFT 1.6 (minor): `tools/amendment-scripts/apply_tables_round_2026_10_27.py`, entries 200 and 201 in rehearsal; every check passes with the g.18 warning that the corpus already carries. The change of STND.DRAFT.3 relaxes a binding provision and raises no floor.
- The harness (unit 0020, `harness/records/units/0020-mention-columns.md`): `table_cells` reads each data cell of a defining table other than a cell of a mention column, by the headings that STND.DRAFT names; g.8 takes a listed verb alone, without terminal punctuation, for a label.

## Trial of the reading

With the round applied and the cells of defining tables read, other than those of mention columns, the drafting checks find no defect. They add these review notices, judged here:

| Check | Provision | Cell | Judgment |
| --- | --- | --- | --- |
| g.12 | STND.PROJ.3 | "Where the human owner records that repository as part of the provisioned environment and as readable only by those whom the threat model trusts" | One condition: one record of the human owner, of two facts. No change. |
| g.14 | STND.CLASS.19 | "at most 6 months", "at most 12 months", "at most 24 months", "at most 36 months" | Each states its unit and an inclusive bound (STND.DRAFT.18). No change. |
| g.8 | STND.DFLT.8 | "Review (QA.7)" | The name of a record, a noun. No change. |
| g.8 | STND.DRAFT.7, STND.DRAFT.13 | "review" | A value of the column Class, a noun. No change. |
| g.8 | STND.IDENT.15 | "Document, register, or space of knowledge entries or tags" | A noun phrase in the column Item. No change. |
| g.6 | STND.DOCS.9 | "A copula avoided" | A label in the column Pattern, which names a pattern of prose; it states no prohibition. No change. |

The trial reads the cells of the columns that are mentioned in part, Replace with, Allowed compounds, Pattern, Forms to watch, Lowercase, and Form among them, and finds nothing more: each mentioned entry of those columns is quoted, or is a word that no check reads as used. With g.8 as unit 0020 leaves it, the lone words "review" of the columns Class and Lowercase of STND.DRAFT.1, .7, and .13 are labels. Unit 0019 also listed STND.IDENT.3 and STND.KNOW.4; under the present checks their cells give no finding, the single words of their columns Ledger type and Name being labels.

## Review

`review.md`, by an agent of another configuration: no defect.

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | Not every named heading is a mention column: Lowercase, Pattern, and Form hold used entries; Replace with and Allowed compounds are mixed | Fixed: the list is Modal, Normative Language entry, Expression, Read as, Qualifier, Word, British, American, Not used, Used, and Opening words; a column mentioned in part is no mention column, and its mentioned entries are quoted, which the corpus already does. The trial of the narrower list finds no defect. |
| S2 | The rationale of STND.DRAFT 1.6 overstates the relaxation and lists STND.IDENT.15 | Fixed: "as in the tables of STND.DRAFT.13, STND.DRAFT.17, STND.DRAFT.33, and STND.DOCS.8 ... no cell of the corpus now holds one unquoted". |
| O3 | Heading (STND.JL.30) and Field (STND.PROJ.6) are unnamed mention columns | Not taken: their cells are read and give no finding; a heading is added when one does. |
| O4 | The trial drops STND.IDENT.3 and STND.KNOW.4 | Explained above. |
| O5 | The heading list belongs under what is drafted | Taken. |
| Q1 | Did the custodian rule the term and the list? | The custodian ruled the term in STND.DRAFT with headings that the harness reads (decision 1); the list itself is drafted, for ratification. |
| Q2 | Is a column mentioned in part a mention column? | No, as the section Representation in the harness now says; for ratification. |

## Ratification of 2026-10-27

The custodian ratified STND.DRAFT 1.6, with the heading list and the reading of a column mentioned in part, STND.DFLT 1.5.3, and unit 0020, as drafted.
