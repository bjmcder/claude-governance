"""Tests of the command-line parser."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from govharness.cli.main import main

ROOT_COMMANDS = (
    ["verify"],
    ["check"],
    ["manifests", "--check"],
    ["references", "--check"],
    ["compose", "--check"],
)


class CorpusRoot(unittest.TestCase):
    """A corpus root that is not a directory is a usage error."""

    def test_missing_root_is_refused(self) -> None:
        """Behavior: each command that reads a corpus exits 2 with a
        usage message naming the root when no directory exists there.

        Reference: a path inside a fresh empty temporary directory, so
        it cannot exist. Before review 0001, ``verify`` on such a path
        reported ``entries: 0`` and one stale manifest (defect 4 of
        unit 0001; the flat ``verify.py`` ended in a traceback).
        """
        with tempfile.TemporaryDirectory() as tmp:
            missing = str(Path(tmp) / "absent")
            for command in ROOT_COMMANDS:
                with self.subTest(command[0]):
                    err = io.StringIO()
                    with (
                        contextlib.redirect_stderr(err),
                        self.assertRaises(SystemExit) as stop,
                    ):
                        main([command[0], missing, *command[1:]])
                    self.assertEqual(stop.exception.code, 2)
                    self.assertIn(
                        f"{missing}: no such directory", err.getvalue()
                    )


if __name__ == "__main__":
    unittest.main()
