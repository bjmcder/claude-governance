"""Rehearsable editorial amendment: CPS 1.0.1, the References of CPS made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_cps_1_0_1.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:05:00+00:00"

EDITS = [
    ('CPS/_doc.md', [
        (('MEAS binds them as well once a reported result rests on them.'),
         ('MEAS binds them as well once a reported result rests on them (MEAS.1).')),
    ]),
]

READING = ('the informative Selector text cites MEAS.1, the selector by which MEAS binds observations once a '
           'reported result rests on them, and References lists MEAS, whose term Observation the Terms import')

ROW = (f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of CPS, revision 1.0.1, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the Selector text cites the selector of the '
             'profile it already names as binding those observations, and the wording of every provision and term '
             'stays as it was, so it alters no obligation, permission, or defined meaning. Transition (GOV.42): '
             'none, because no obligation changes. Review: record review-records/round-2026-10-25-close/p5/.'
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
    raise_revision(root, "CPS", "1.0", "1.0.1", ROW)
    write_references(root, ["CPS"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["CPS"], scope=["CPS"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "CPS 1.0.1")
