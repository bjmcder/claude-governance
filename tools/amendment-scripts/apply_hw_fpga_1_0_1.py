"""Rehearsable editorial amendment: HW.FPGA 1.0.1, the References of HW.FPGA made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_hw_fpga_1_0_1.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:10:00+00:00"

EDITS = [
    ('HW/FPGA/_doc.md', [
        (('so HW.EMBED does not bind its firmware.'),
         ('so HW.EMBED does not bind its firmware (HW.EMBED.1).')),
    ]),
]

READING = ('the informative Notes cite HW.EMBED.1, the selector of HW.EMBED, where they state that HW.EMBED does '
           'not bind the firmware of a processor realized in programmable logic, and References lists HW.EMBED')

ROW = (f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of HW.FPGA, revision 1.0.1, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the Notes cite the selector of the sub-profile '
             'they already name, whose attribute the Terms of HW define to exclude programmable logic, and the '
             'wording of every provision stays as it was, so it alters no obligation, permission, or defined '
             'meaning. Transition (GOV.42): none, because no obligation changes. Review: record '
             'review-records/round-2026-10-25-close/p5/.'
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
    raise_revision(root, "HW/FPGA", "1.0", "1.0.1", ROW)
    write_references(root, ["HW.FPGA"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["HW.FPGA"], scope=["HW/FPGA"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "HW.FPGA 1.0.1")
