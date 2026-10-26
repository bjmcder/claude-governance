"""Rehearsable minor amendment: STND.IDENT 1.4, round of 2026-10-26 (decision 2 and unit 0017).

One transaction.
- Decision 2: STND.IDENT.12 asks the adopter's label only of a document that is adopted or ratified.
- Unit 0017: new STND.IDENT.24 has the constitution list each withdrawn provision of its parts in its field
  withdrawn, which STND.IDENT.14 does not place; the section Checks says that v.8 reads it.
Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_ident_1_4.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-26"
AT = "2026-10-26T12:00:06+00:00"

IDENT12 = [("A constitution, profile, sub-profile, or standard SHALL name its adopter",
            "A constitution, profile, sub-profile, or standard that is adopted or ratified SHALL name its adopter")]

IDENT24 = "\n".join([
    "---",
    'id: "STND.IDENT.24"',
    'level: "LVL2"',
    'kind: "provision"',
    'title: "Withdrawn constitution provisions"',
    'section: "Identifiers"',
    'status: "adopted"',
    f'adopted: "{DATE}"',
    'mode: "binding"',
    "binding_reason: null",
    'instantiates: ["GOV.37"]',
    "refers_to: []",
    "rank: null",
    "waivable: false",
    "defines: []",
    'checked_by: ["v.8"]',
    "---",
    "",
    "The constitution SHALL list in its field `withdrawn` the identifier of each provision of a part named in its "
    "field `parts` that a revision withdraws (GOV.37).",
    "",
])

CHECKS = [("The check v.8 compares the numbered provisions of each document with its field `withdrawn`: a gap in "
           "the numbering that the field does not list, or a listed identifier that names a provision, fails.",
           "The check v.8 compares the numbered provisions of each document with its field `withdrawn`, and those "
           "of each part of the constitution with the field `withdrawn` of the constitution: a gap in the numbering "
           "that the field does not list, a listed identifier that names a provision or is not the document's own, "
           "or a cited identifier that names no provision and is not listed, fails.")]

READING = ("STND.IDENT.12 asks the label of its adopter only of a document that is adopted or ratified, so a draft "
           "or a planned document names none; new STND.IDENT.24: the constitution lists in its field withdrawn each withdrawn provision of "
           "the parts named in its field parts; the section Checks describes v.8 in full, with the field withdrawn of "
           "the constitution")
ROW = f"| 1.4 | {DATE} | Minor amendment (GOV.41): {READING}. Transition (GOV.42): none. |"

RATIONALE = (
    f"Minor amendment of STND.IDENT, revision 1.4, ratified by the custodian on {DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because STND.IDENT.12 removes an obligation from drafts and STND.IDENT.24 adds one. "
    "A draft or a planned document has no adopter yet, and the adoption itself records the role that adopts it. "
    "STND.IDENT.14 asks a document to list its own withdrawn provisions, and the provisions of the constitution are "
    "numbered by part (GOV.37), so it left no place for a withdrawn provision of a part; STND.IDENT.24 gives it the "
    "field of the constitution. STND.IDENT.24 binds, because it instantiates GOV.37, and raises no floor (GOV.11): it "
    "asks the custodians for one list of identifiers, only when a revision withdraws a provision of a part, and asks "
    "nothing of the human owner or of a project. No provision of the constitution is withdrawn, so its front matter does not change. "
    "Transition (GOV.42): none. Decision 2 of review-records/round-2026-10-26/decisions.md; record "
    "harness/records/units/0017-checks-fixes.md."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/IDENT/12.md", IDENT12)
    (root / "STND/IDENT/24.md").write_text(IDENT24, encoding="utf-8")
    res = B.derive_fields(root, ["STND.IDENT.24"])
    if res["STND.IDENT.24"].unresolved or res["STND.IDENT.24"].waivable:
        raise ValueError(f"STND.IDENT.24: {res['STND.IDENT.24']}")
    replace_text(root, "STND/IDENT/_doc.md", CHECKS)
    raise_revision(root, "STND/IDENT", "1.3.3", "1.4", ROW)
    B.write_references(root, ["STND.IDENT"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.IDENT"], scope=["STND/IDENT"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.IDENT 1.4")
