"""Tests of the structural checks of ``verify``: status and references.

Ported from ``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import unittest
from pathlib import PurePosixPath

from govharness.checks.fields import status_problems
from govharness.checks.structure import reference_problems
from govharness.core.entry import Entry
from tests.support import live_entries


class StructureChecks(unittest.TestCase):
    """Entry status and reference resolution."""

    def test_entry_status(self) -> None:
        """Behavior: an entry that lags its document's status is found.

        Reference: an adopted document with a draft entry, and with an
        entry that carries no adoption date (the slip of ledger entry
        9, fixed by entry 11); the live corpus has neither.
        """

        def entry(name: str, **meta: str) -> Entry:
            """Build an entry of the standard STND.X.

            Parameters
            ----------
            name : str
                File name in the standard's directory.
            **meta : str
                Front-matter fields.

            Returns
            -------
            Entry
                The entry, with an empty body.
            """
            return Entry(PurePosixPath("STND/X") / name, meta, "")

        doc = entry("_doc.md", id="STND.X", status="adopted")
        good = entry("1.md", id="STND.X.1", status="adopted", adopted="d")
        self.assertEqual(status_problems([doc, good]), [])
        for bad in (
            entry("1.md", id="STND.X.1", status="draft", adopted="d"),
            entry("1.md", id="STND.X.1", status="adopted"),
        ):
            self.assertEqual(len(status_problems([doc, bad])), 1)
        self.assertEqual(status_problems(live_entries()), [])

    def test_strict_references(self) -> None:
        """Behavior: a malformed or unknown reference is reported.

        Reference: an entry that refers to ``Gov.47`` (wrong case) and
        ``LVL1`` (no such entry or LVL0 heading).
        """
        bad = Entry(
            PurePosixPath("X/1.md"),
            {"id": "X.1", "refers_to": ["Gov.47", "LVL1"]},
            "",
        )
        self.assertEqual(len(reference_problems([*live_entries(), bad])), 2)


if __name__ == "__main__":
    unittest.main()
