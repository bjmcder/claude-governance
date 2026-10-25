"""Rehearsable editorial amendment: STND.BUILD 1.0.2, the Notes cite STND.CODE.21 beside STND.CXX.18.

One transaction. STND.CODE.21 and STND.CXX 1.2, which now cites it from STND.CXX.18, come from package P1, so this
applies after P1: apply_close_p5_build.py rehearses it that way. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p5_build.py
"""
from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.derive.references import rewrite_sections
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

DATE = "2026-10-25"
AT = "2026-10-25T21:20:00+00:00"

EDITS = [
    ('STND/BUILD/_doc.md', [
        (('and STND.CXX.18 keeps a required check of a floating-point value from a unit compiled under an option '
          'that assumes finite values.'),
         ('and STND.CODE.21 has code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 '
          'governs not compiled under a setting that lets the compiler assume finite values, which STND.CXX.18 '
          'binds for C++.')),
        (('which is why STND.CXX.18 keeps it from a unit that holds a required check of such a value;'),
         ('which is why STND.CODE.21 advises against it for code that holds a required check of such a value, '
          'and STND.CXX.18 keeps it from such C++ code;')),
    ]),
]

READING = ('the informative Notes cite STND.CODE.21, the rule for every language on settings that let the compiler '
           'assume finite floating-point values near a required check, and STND.CODE.16, beside STND.CXX.18, which '
           'binds that rule for C++ and which they cited alone')

ROW = (f"| 1.0.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined "
       "meaning changes. |")

RATIONALE = (f"Editorial amendment of STND.BUILD, revision 1.0.2, ratified by the custodian on {DATE}: {READING}. "
             'The change is editorial under STND.IDENT.3 because the Notes cite the provisions that hold, for '
             'every language, the rule they already describe for C++, with the same content, and the wording of every provision stays as it '
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
    raise_revision(root, "STND/BUILD", "1.0.1", "1.0.2", ROW)
    write_references(root, ["STND.BUILD"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.BUILD"], scope=["STND/BUILD"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.BUILD 1.0.2")
