"""Rehearsable editorial amendment: STND.KNOW 1.0.1, the References of STND.KNOW made complete.

One transaction. The text named a document without citing it, so that the derived References table left it out
(tools/check_refs.py); the informative text now cites it, and the table is derived again. Applied on top of ledger
entry 147 by apply_close_p5.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_know_1_0_1.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:03:00+00:00"

EDITS = [
    ('STND/KNOW/_doc.md', [
        (('The space KNOW of the governance corpus, with one directory per domain (STND.IDENT.15), and the tag '
          "vocabulary TAG, with one directory per facet, are the custodians' shared knowledge base and tags."),
         ('The space of the governance corpus for knowledge entries (KNOW), with one directory per domain '
          "(STND.IDENT.15), and the tag vocabulary of that corpus (TAG), with one directory per facet, are the custodians' shared "
          'knowledge base and tags.')),
        (('The facet TAG.COMP is local to a project.'),
         ('The component facet (TAG.COMP) is local to a project.')),
    ]),
]

READING = ('the informative Notes cite the knowledge space KNOW, the tag vocabulary TAG, and the facet TAG.COMP of '
           'the governance corpus, which they named, and References lists KNOW, TAG, and TAG.COMP')

ROW = (f"| 1.0.1 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of STND.KNOW, revision 1.0.1, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the Notes cite by identifier the knowledge space, '
             'tag vocabulary, and facet they already name, with the same content, and the wording of every '
             'provision stays as it was, so it alters no obligation, permission, or defined meaning. Transition '
             '(GOV.42): none, because no obligation changes. Review: record '
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
    raise_revision(root, "STND/KNOW", "1.0", "1.0.1", ROW)
    write_references(root, ["STND.KNOW"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.KNOW"], scope=["STND/KNOW"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.KNOW 1.0.1")
