"""Rehearsable editorial amendment: HDES 1.0.2, the References of HDES made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_hdes_1_0_2.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:13:00+00:00"

EDITS = [
    ('HDES/_doc.md', [
        (('which the sub-profiles HDES.FPGA and HDES.ASIC each give one of (STND.DRAFT.36).'),
         ('which the sub-profiles HDES.FPGA and HDES.ASIC each give one of (HDES.FPGA.1, HDES.ASIC.1, '
          'STND.DRAFT.36).')),
        (('so its firmware is not bound by HW.EMBED;'),
         ('so its firmware is not bound by HW.EMBED (HW.EMBED.1);')),
        (('HDES.ASIC gives the owner the record on which to decide.'),
         ('HDES.ASIC gives the owner the record on which to decide (HDES.ASIC.12).')),
    ]),
]

READING = ('the informative text cites HDES.FPGA.1 and HDES.ASIC.1, the selectors of its sub-profiles, HW.EMBED.1, '
           'the selector of HW.EMBED, and HDES.ASIC.12, the fabrication readiness record on which the human owner '
           'decides a submission, and References lists HDES.ASIC, HDES.FPGA, and HW.EMBED')

ROW = (f"| 1.0.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of HDES, revision 1.0.2, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the text cites provisions of the documents it '
             'already names, where it already states what they hold, and the wording of every provision stays as it '
             'was, so it alters no obligation, permission, or defined meaning. Transition (GOV.42): none, because '
             'no obligation changes. Review: record review-records/round-2026-10-25-close/p5/.'
             " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
             " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def write_references(root: Path, doc_ids: list[str]) -> None:
    tree = read_tree(root)
    corpus = Corpus(load_entries(tree))
    for rel, text in rewrite_sections(tree, corpus, doc_ids).items():
        (root / rel).write_text(text, encoding="utf-8")


def apply(root: Path) -> None:
    root = Path(root)
    for rel, pairs in EDITS:
        replace_text(root, rel, pairs)
    raise_revision(root, "HDES", "1.0.1", "1.0.2", ROW)
    write_references(root, ["HDES"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["HDES"], scope=["HDES"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "HDES 1.0.2")
