"""Rehearsable minor amendment: STND.DRAFT 1.5, round of 2026-10-26 (decision 1 and unit 0017).

One transaction.
- Decision 1: the term Cited document covers a document named by its identifier in the text, alone or in
  parentheses, outside the spans that g.25 does not read; the section Checks says that g.25 fails on such a
  name that no citation backs.
- Unit 0017, M2: STND.DRAFT.3 does not ask for quotation marks in a table column whose entries are expressions.
- Unit 0017, L1: STND.DRAFT.22 names v.8 among its checks.
- Unit 0017, L9: the section Checks names the provision of this standard whose mode decides whether a finding
  fails.
- Unit 0017, L3: new term Sentence.
Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_draft_1_5.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import write_references  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-26"
AT = "2026-10-26T12:00:05+00:00"

TERMS = [
    ("| Informative sentence |",
     "| Sentence | Text that ends at a period, a question mark, or an exclamation point, or at the end of a "
     "paragraph, a list item, or a table cell, not counting a mark inside an identifier, a number, an abbreviation, "
     "or quotation marks. |\n| Informative sentence |"),
    ("in a citation or a reference field of the citing document or of its provisions. |",
     "in a citation or a reference field of the citing document or of its provisions, or named in their text by "
     "its identifier alone. A name by identifier alone does not count inside quotation marks, a code span, a table "
     "with a column headed Example, the section References, or the revision history, and the identifier LVL0 alone "
     "never counts. |"),
]

CHECKS = [
    ("A finding in another document fails when this standard is adopted and the provision concerned is binding, and "
     "warns otherwise.",
     "A finding in another document fails when this standard is adopted and a binding provision of this standard "
     "names the check in its field `checked_by`, and warns otherwise."),
    ("The check g.25 compares each references table with the cited documents that `python -m govharness references` "
     "derives from the corpus and writes.",
     "The check g.25 compares each references table with the cited documents that `python -m govharness references` "
     "derives from the corpus and writes. The command derives a row for each document that the text names by its "
     "identifier alone, as for a citation, and g.25 fails where the table lacks it, whether or not a citation backs "
     "the name."),
]

DRAFT3 = [("A modal or an excluded expression that a provision mentions without using it SHALL be enclosed in "
           "quotation marks (LVL0#normative-language).",
           "Outside a column whose entries are modals or excluded expressions, a modal or an excluded expression "
           "that a provision mentions without using it SHALL be enclosed in quotation marks "
           "(LVL0#normative-language).")]

DRAFT22 = [('checked_by: ["l.1"]', 'checked_by: ["l.1", "v.8"]')]

READING = (
    "the term Cited document also covers a document named in the text by its identifier alone, outside quotation "
    "marks, code spans, tables with a column headed Example, the section References, and the revision history, and "
    "never by the identifier LVL0 alone; new term Sentence; STND.DRAFT.3 asks for no quotation marks in a column "
    "whose entries are modals or excluded expressions; STND.DRAFT.22 names v.8 among its checks; the section Checks "
    "says that a finding in another document fails where a binding provision of this standard names the check, "
    "and that a document named by its identifier alone has its row derived, so that g.25 fails where the table "
    "lacks it")
ROW = f"| 1.5 | {DATE} | Minor amendment (GOV.41): {READING}. Transition (GOV.42): none. |"

RATIONALE = (
    f"Minor amendment of STND.DRAFT, revision 1.5, ratified by the custodian on {DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because the term Cited document widens a defined meaning and STND.DRAFT.3 removes an "
    "obligation from the cells of a column of expressions. The term Sentence defines the sense that STND.DRAFT.4 and "
    "STND.DRAFT.16 already count by, and the field and the section Checks change no obligation; alone they would be "
    "editorial, and they ride in this amendment. The widened term makes a document that the text names by its "
    "identifier alone a cited document, whose row STND.DRAFT.34 asks for and a row alone meets; until now the "
    "harness asked for a citation behind such a name (unit 0013, decision 22 of the closing round of 2026-10-25). "
    "The closing round backed every bare name by a citation, so no document of the corpus changes with it. v.8 verifies STND.DRAFT.22 in part: it "
    "fails a cited identifier that names no provision unless the document lists it as withdrawn, and l.1 checks the "
    "reference fields. Neither change raises the floor (GOV.11): the widened term asks of a document only a row of "
    "its References table for each document that its text names, which is the traceability PRIME.15 already asks "
    "of a citation; it asks no decision of the human owner and no new act of a project, because the command "
    "references writes the row. STND.DRAFT.3 removes an obligation. Transition (GOV.42): none. Decision 1 "
    "of review-records/round-2026-10-26/decisions.md; records harness/records/units/0013-references-bare-names.md "
    "and harness/records/units/0017-checks-fixes.md."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/DRAFT/_doc.md", [*TERMS, *CHECKS])
    replace_text(root, "STND/DRAFT/3.md", DRAFT3)
    replace_text(root, "STND/DRAFT/22.md", DRAFT22)
    raise_revision(root, "STND/DRAFT", "1.4", "1.5", ROW)
    write_references(root, ["STND.DRAFT"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.DRAFT"], scope=["STND/DRAFT"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.DRAFT 1.5")
