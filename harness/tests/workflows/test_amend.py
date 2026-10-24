"""Tests of the amendment primitives (unit 0002 criterion 2).

Every amendment is made to a copy of the corpus in a fresh temporary
directory.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from govharness.ledger.chain import read_ledger
from govharness.workflows.amend import (
    Change,
    raise_revision,
    record_transaction,
    replace_text,
)
from tests.support import corpus_copy, live_revision, next_editorial

INSTR = "STND/INSTR/_doc.md"
OLD = live_revision("STND.INSTR")
NEW = next_editorial(OLD)
ROW = f"| {NEW} | 2026-10-24 | Editorial amendment (GOV.40): a test. |"
EDITORIAL = Change(
    kind="amend",
    actor="The Custodian",
    role="custodians",
    at="2026-10-24T12:00:00+00:00",
    authority=["GOV.40"],
    targets=["STND.INSTR"],
    scope=["STND/INSTR"],
    rationale=f"Editorial amendment of STND.INSTR, revision {NEW}: a test.",
)


def text_of(root: Path, rel: str) -> str:
    """Return the text of one file of a corpus copy.

    Parameters
    ----------
    root : Path
        Corpus copy.
    rel : str
        File path relative to the copy.

    Returns
    -------
    str
        Its contents.
    """
    return (root / rel).read_text(encoding="utf-8")


class AmendmentPrimitives(unittest.TestCase):
    """Each primitive makes its edit exactly or refuses it."""

    def test_replace_text_once(self) -> None:
        """Behavior: a text that occurs once is replaced; a text that
        occurs never or twice, or a path outside the root, is refused
        and the file is left as it was.

        Reference: the opening words of STND.INSTR (once), a text it
        lacks (never), the word "the" (many times), and ``../x``.
        """
        with corpus_copy() as root:
            before = text_of(root, INSTR)
            opening = "This standard gives"
            replace_text(root, INSTR, [(opening, "This standard states")])
            self.assertIn("This standard states", text_of(root, INSTR))
            changed = text_of(root, INSTR)
            for pairs in ([("no such text", "x")], [("the", "a")]):
                with self.subTest(pairs[0][0]):
                    with self.assertRaises(ValueError):
                        replace_text(root, INSTR, pairs)
                    self.assertEqual(text_of(root, INSTR), changed)
            with self.assertRaises(ValueError):
                replace_text(root, "../outside.md", [("a", "b")])
            self.assertNotEqual(before, changed)

    def test_raise_revision(self) -> None:
        """Behavior: the revision field changes and the history row goes
        after the last row; a stale old revision is refused.

        Reference: STND.INSTR raised from its live revision to the next
        editorial one, then a second raise that still names the old one.
        """
        with corpus_copy() as root:
            raise_revision(root, "STND/INSTR", OLD, NEW, ROW)
            text = text_of(root, INSTR)
            self.assertIn(f'revision: "{NEW}"', text)
            self.assertTrue(text.endswith(ROW + "\n"))
            with self.assertRaises(ValueError):
                raise_revision(
                    root, "STND/INSTR", OLD, next_editorial(NEW), ROW
                )

    def test_history_row_stays_in_its_section(self) -> None:
        """Behavior: the new row follows the last row of the Revision
        History table, not a numbered row of a later section.

        Reference: STND.INSTR with a section after its history holding a
        table whose first cell is a number. Before review 0001 the row
        went after that later table's last row.
        """
        with corpus_copy() as root:
            later = (
                "\n## Appendix\n\n| No. | Item |\n| --- | --- |\n| 1 | x |\n"
            )
            path = root / INSTR
            path.write_text(text_of(root, INSTR) + later, encoding="utf-8")
            raise_revision(root, "STND/INSTR", OLD, NEW, ROW)
            text = text_of(root, INSTR)
            self.assertTrue(text.endswith("| 1 | x |\n"))
            self.assertIn(ROW + "\n\n## Appendix", text)

    def test_record_transaction_verifies(self) -> None:
        """Behavior: recording rebuilds the manifests, appends one
        unsigned entry with the given actor and role, and the corpus
        verifies afterwards.

        Reference: a complete editorial amendment of STND.INSTR in a
        copy; without the record, verify would fail on the stale
        manifests and on the edit outside the ledger.
        """
        with corpus_copy() as root:
            count = len(read_ledger(root))
            raise_revision(root, "STND/INSTR", OLD, NEW, ROW)
            recorded = record_transaction(root, EDITORIAL)
            self.assertEqual(recorded.entry["seq"], count + 1)
            self.assertEqual(recorded.entry["actor"], "The Custodian")
            self.assertEqual(recorded.entry["signature"], "")
            self.assertEqual(len(read_ledger(root)), count + 1)
            self.assertEqual(recorded.verification.sections()["logic"], [])
            self.assertTrue(recorded.verification.passed())

    def test_record_refuses_a_missing_scope(self) -> None:
        """Behavior: a scope that names no directory is refused before
        anything is written.

        Reference: the misspelled scope ``STND/INST``.
        """
        with corpus_copy() as root:
            ledger = text_of(root, "ledger.jsonl")
            change = Change(**{**EDITORIAL.__dict__, "scope": ["STND/INST"]})
            with self.assertRaises(ValueError):
                record_transaction(root, change)
            self.assertEqual(text_of(root, "ledger.jsonl"), ledger)


if __name__ == "__main__":
    unittest.main()
