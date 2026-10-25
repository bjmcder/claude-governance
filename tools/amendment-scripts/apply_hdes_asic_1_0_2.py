"""Rehearsable editorial amendment: HDES.ASIC 1.0.2, the References of HDES.ASIC made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_hdes_asic_1_0_2.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:12:00+00:00"

EDITS = [
    ('HDES/ASIC/_doc.md', [
        (('are governed by HW and its sub-profile HW.ASIC, and by MEAS where it binds.'),
         ('are governed by HW and its sub-profile HW.ASIC (HW.6, HW.ASIC.4), and by MEAS where it binds (MEAS.1).')),
    ]),
]

READING = ('the informative Selector text cites HW.6 and HW.ASIC.4, which govern the evidence obtained from '
           'fabricated devices, and MEAS.1, the selector of MEAS, and References lists HW.ASIC and MEAS')

ROW = (f"| 1.0.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of HDES.ASIC, revision 1.0.2, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the Selector text cites the provisions of the '
             'documents it already names as governing validation after fabrication, as its table of where the rest '
             'lives already does, and the wording of every provision stays as it was, so it alters no obligation, '
             'permission, or defined meaning. Transition (GOV.42): none, because no obligation changes. Review: '
             'record review-records/round-2026-10-25-close/p5/.'
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
    raise_revision(root, "HDES/ASIC", "1.0.1", "1.0.2", ROW)
    write_references(root, ["HDES.ASIC"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["HDES.ASIC"], scope=["HDES/ASIC"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "HDES.ASIC 1.0.2")
