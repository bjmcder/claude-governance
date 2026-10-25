"""Rehearsable editorial amendment: STND.CLASS 1.3.1, the References of STND.CLASS made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_class_1_3_1.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:01:00+00:00"

EDITS = [
    ('STND/CLASS/_doc.md', [
        (('The table of STND.CLASS.10 lists what waits for a more severe class and what a more severe class adds.'),
         ('The table of STND.CLASS.10 lists what waits for a more severe class and what a more severe class adds; '
          'no part of Simplicity (SIMPL) is among them.')),
    ]),
]

READING = ('the informative section Reading the standard states that the table of STND.CLASS.10 holds no part of '
           'Simplicity, citing SIMPL, which STND.CLASS.10 names, and References lists SIMPL')

ROW = (f"| 1.3.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of STND.CLASS, revision 1.3.1, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the sentence states what the table of '
             'STND.CLASS.10 already holds and cites the Article that the provision already names, and the wording '
             'of every provision stays as it was, so it alters no obligation, permission, or defined meaning. '
             'Transition (GOV.42): none, because no obligation changes. Review: record '
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
    raise_revision(root, "STND/CLASS", "1.3", "1.3.1", ROW)
    write_references(root, ["STND.CLASS"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CLASS"], scope=["STND/CLASS"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.CLASS 1.3.1")
