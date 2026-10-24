"""Tests of the ledger check of ``verify``: chain, pins, and scopes.

Every damage is made to a copy of the corpus in a fresh temporary
directory. Ported from ``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from govharness.checks.ledger import ledger_problems
from govharness.core.corpus import read_tree
from govharness.ledger.chain import read_ledger
from govharness.ledger.gpg import SignerConfig
from tests.ledger.test_chain import renumber, rewrite
from tests.support import corpus_copy

NO_ANCHOR = SignerConfig()


def problems(root: Path) -> list[str]:
    """Return the ledger check's failures for a corpus copy.

    Parameters
    ----------
    root : Path
        Corpus copy.

    Returns
    -------
    list[str]
        Failure lines; the signer configuration names no anchor, so no
        file outside the copy is read.
    """
    return ledger_problems(read_tree(root), read_ledger(root), NO_ANCHOR)


class LedgerCheck(unittest.TestCase):
    """Pins, unpinned edits, altered entries, and bad scopes."""

    def test_ledger_pins(self) -> None:
        """Behavior: an edit outside the ledger, an altered entry, and a
        scope that names no directory each fail; an unpinned edit does
        not.

        Reference: injected edits to TAG (pinned by no
        transaction) and STND/CLASS (pinned by entry 36), an altered
        reason in entry 5, and a misspelled scope in the last entry, then
        the scope ``..``, which leaves the root (passed by the flat code;
        fixed by review 0001).
        """
        with corpus_copy() as root:
            self.assertEqual(problems(root), [])
            unpinned = root / "TAG" / "_doc.md"
            unpinned.write_text(unpinned.read_text() + " ", "utf-8")
            self.assertEqual(problems(root), [])
            pinned = root / "STND" / "CLASS" / "1.md"
            pinned.write_text(pinned.read_text() + " ", "utf-8")
            errors = problems(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("STND/CLASS", errors[0])
            path = root / "ledger.jsonl"
            lines = path.read_text().splitlines()
            entry = json.loads(lines[4])
            entry["rationale"] += " altered"
            lines[4] = json.dumps(entry)
            path.write_text("\n".join(lines) + "\n", "utf-8")
            self.assertIn(
                "ledger entry altered at seq 5", "\n".join(problems(root))
            )
            entry = json.loads(lines[-1])
            entry["scope"] = ["STND/CLAS"]
            lines[-1] = json.dumps(entry)
            path.write_text("\n".join(lines) + "\n", "utf-8")
            self.assertIn("does not exist", "\n".join(problems(root)))
            entry["scope"] = [".."]
            lines[-1] = json.dumps(entry)
            path.write_text("\n".join(lines) + "\n", "utf-8")
            self.assertIn("scope .. does not exist", "\n".join(problems(root)))

    def test_renumbered_entry(self) -> None:
        """Behavior: an entry whose number is not its position fails,
        even with every link and hash rebuilt.

        Reference: entry 3 renumbered 4 with the chain rebuilt, the
        damage ``ledger append`` refuses (unit 0002 criterion 1). The
        flat ``verify`` compared links and hashes only and passed it;
        review 0001 made the check of ``verify`` the check of ``append``.
        """
        with corpus_copy() as root:
            rewrite(root, renumber)
            self.assertEqual(
                problems(root), ["ledger sequence broken at entry 3: seq 4"]
            )


if __name__ == "__main__":
    unittest.main()
