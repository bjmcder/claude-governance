"""Rehearsable round of 2026-10-27 on defining tables: STND.DFLT 1.5.3 and STND.DRAFT 1.6.

Two transactions.
- STND.DFLT 1.5.3 (editorial): the Source column of STND.DFLT.18 reads "Every actor" in place of "Any actor",
  the quantifier that STND.DRAFT.17 forbids, which the drafting checks find once they read that table.
- STND.DRAFT 1.6 (minor): Terms define Mention column; STND.DRAFT.3 uses it; the section Representation in the
  harness says that the drafting checks read each other cell of a table in a provision, and names the headings by
  which the harness finds a mention column.
The harness code that reads the cells follows the text (unit 0020). Run from harness/:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_tables_round_2026_10_27.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T20:00:00+00:00"
RECORD = "review-records/round-2026-10-27-tables/decisions.md"

MENTION_HEADINGS = (
    "Modal, Lowercase, Normative Language entry, Expression, Read as, Qualifier, Word, Replace with, Allowed "
    "compounds, British, American, Not used, Used, Pattern, Forms to watch, Opening words, and Form")

DFLT18 = [
    ("| The work, its records, and its history | Change beyond authority | Any actor | Yes |",
     "| The work, its records, and its history | Change beyond authority | Every actor | Yes |"),
    ("| Secrets the work uses | Disclosure | Any actor | Yes |",
     "| Secrets the work uses | Disclosure | Every actor | Yes |"),
    ("| Evidence | Fabrication or misrepresentation | Any actor | Yes |",
     "| Evidence | Fabrication or misrepresentation | Every actor | Yes |"),
]

DRAFT3 = [("Outside a column whose entries are modals or excluded expressions, a modal",
           "Outside a mention column, a modal")]

DRAFT_DOC = [
    ("| Excluded expression | An expression of the table of STND.DRAFT.7. |\n",
     "| Excluded expression | An expression of the table of STND.DRAFT.7. |\n"
     "| Mention column | A column of a table in a provision whose entries are the words, expressions, spellings, "
     "forms, or patterns that the provision names rather than uses. |\n"),
    ("- `defines`: the name of a table that the provision holds. The harness reads each table by this name and by "
     "its column headings, so rewording a sentence cannot empty a list.",
     "- `defines`: the name of a table that the provision holds. The harness reads each table by this name and by "
     "its column headings, so rewording a sentence cannot empty a list. The drafting checks read each cell of a "
     "table in a provision as prose, other than a cell of a mention column, which the harness finds by its "
     f"heading: {MENTION_HEADINGS}. A table with a mention column under another heading adds that heading to the "
     "harness."),
]

DFLT_READING = ("the Source column of STND.DFLT.18 reads \"Every actor\" in place of \"Any actor\", in its three "
                "rows, the quantifier that STND.DRAFT.17 forbids")
DFLT_ROW = (f"| 1.5.3 | {F.DATE} | Editorial amendment (GOV.41): {DFLT_READING}; no obligation, permission, or "
            "defined meaning changes. |")
DFLT_RATIONALE = (
    f"Editorial amendment of STND.DFLT, revision 1.5.3, ratified by the custodian on {F.DATE}: {DFLT_READING}. The "
    "change is editorial under STND.IDENT.3 because the source of each threat stays each actor, so no obligation, "
    "permission, or defined meaning changes; the drafting checks find the word once they read the cells of the "
    "tables that a provision defines, as STND.DRAFT 1.6 describes. Transition (GOV.42): none. Decision 2 of "
    f"{RECORD}." + F.AUTHOR)

DRAFT_READING = (
    "Terms define Mention column, a column of a table in a provision whose entries are the words, expressions, "
    "spellings, forms, or patterns that the provision names rather than uses; STND.DRAFT.3 uses the term in place of "
    "a column whose entries are modals or excluded expressions, so that a modal or an excluded expression that a "
    "column of words, spellings, forms, or patterns mentions is also left unquoted; the section Representation in "
    "the harness says that the drafting checks read each other cell of a table in a provision, and names the "
    "headings by which the harness finds a mention column")
DRAFT_ROW = f"| 1.6 | {F.DATE} | Minor amendment (GOV.41): {DRAFT_READING}. |"
DRAFT_RATIONALE = (
    f"Minor amendment of STND.DRAFT, revision 1.6, ratified by the custodian on {F.DATE}: {DRAFT_READING}. The "
    "change is minor under STND.IDENT.3 because it adds a defined meaning and narrows the reach of STND.DRAFT.3: a "
    "modal or an excluded expression in a column that lists words, spellings, forms, or patterns, in the tables of "
    "STND.DRAFT.13, STND.DRAFT.17, STND.DRAFT.29, STND.DRAFT.32, STND.DRAFT.33, STND.DOCS.8, STND.DOCS.9, and "
    "STND.IDENT.3 and STND.IDENT.15 among them, needs no quotation marks, as one in the columns of STND.DRAFT.1 and "
    "STND.DRAFT.7 did not. STND.DRAFT.3 stays binding; the change relaxes it and asks nothing new, so it raises no "
    "floor (GOV.11). The custodian decided that a term of this standard, with the headings that the harness reads, "
    "marks the columns that a provision mentions (decision 1). Transition (GOV.42): none. Decision 1 of "
    f"{RECORD}; the open item of unit 0019, harness/records/units/0019-round-2026-10-26.md." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    replace_text(root, "STND/DFLT/18.md", DFLT18)
    F.finish(root, "STND/DFLT", "STND.DFLT", "1.5.2", "1.5.3", DFLT_ROW, DFLT_RATIONALE, start.isoformat())
    replace_text(root, "STND/DRAFT/3.md", DRAFT3)
    replace_text(root, "STND/DRAFT/_doc.md", DRAFT_DOC)
    F.check_fields(root, ["STND.DRAFT.3"])
    F.finish(root, "STND/DRAFT", "STND.DRAFT", "1.5", "1.6", DRAFT_ROW, DRAFT_RATIONALE,
             (start + timedelta(seconds=1)).isoformat())
