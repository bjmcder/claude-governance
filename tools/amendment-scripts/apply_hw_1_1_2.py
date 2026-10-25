"""Rehearsable editorial amendment: HW 1.1.2, the References of HW made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_hw_1_1_2.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:11:00+00:00"

EDITS = [
    ('HW/_doc.md', [
        (('HW.1 states the selector: one attribute per hardware type, each defined here.'),
         ('HW.1 states the selector: one attribute per hardware type, each defined here, which the sub-profiles '
          'each give one of (HW.CPU.1, HW.GPU.1, HW.QPU.1, HW.EMBED.1, HW.FPGA.1, HW.ASIC.1, STND.DRAFT.36).')),
    ]),
]

READING = ('the informative Selector text cites the selectors of the six sub-profiles that the Purpose names, each '
           'of which gives one attribute of HW.1 (STND.DRAFT.36), and References lists HW.ASIC, HW.CPU, HW.EMBED, '
           'HW.FPGA, HW.GPU, and HW.QPU')

ROW = (f"| 1.1.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of HW, revision 1.1.2, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the Selector text cites the selectors of the '
             'sub-profiles that the Purpose already names, each of which already gives one attribute of HW.1, and '
             'the wording of every provision stays as it was, so it alters no obligation, permission, or defined '
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
    raise_revision(root, "HW", "1.1.1", "1.1.2", ROW)
    write_references(root, ["HW"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["HW"], scope=["HW"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "HW 1.1.2")
