"""Tests of rehearsal on a copy of the corpus (unit 0002 criterion 3).

The source of every rehearsal here is itself a copy of the corpus in a
fresh temporary directory, so that even a failing test cannot touch the
live corpus.
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from govharness.cli.main import main
from govharness.core.corpus import tree_digests
from govharness.ledger.chain import read_ledger
from govharness.workflows.rehearse import SourceChanged, rehearse
from tests.support import corpus_copy

AMENDMENT = '''
from pathlib import Path

from govharness.workflows.amend import Change, raise_revision
from govharness.workflows.amend import record_transaction

ROW = "| 1.1.1 | 2026-10-10 | Editorial amendment (GOV.40): a test. |"


def apply(root: Path) -> None:
    """Raise STND.INSTR to 1.1.1 and record it."""
    raise_revision(root, "STND/INSTR", "1.1", "1.1.1", ROW)
    record_transaction(
        root,
        Change(
            kind="amend",
            actor="The Custodian",
            role="custodians",
            at="2026-10-10T00:00:00+00:00",
            authority=["GOV.40"],
            targets=["STND.INSTR"],
            scope=["STND/INSTR"],
            rationale="Editorial amendment of STND.INSTR, revision 1.1.1.",
        ),
    )
'''
STRAY = '''
from pathlib import Path

SOURCE = Path({source!r})


def apply(root: Path) -> None:
    """Append to the source ledger instead of the copy's."""
    with (SOURCE / "ledger.jsonl").open("a", encoding="utf-8") as handle:
        handle.write("{{}}\\n")
'''

EVASIVE = '''
import os
from pathlib import Path

SOURCE = Path({source!r})


def apply(root: Path) -> None:
    """Append to the source ledger, then move to the copy's folder."""
    with (SOURCE / "ledger.jsonl").open("a", encoding="utf-8") as handle:
        handle.write("{{}}\\n")
    os.chdir(root.parent)
'''
NEW_DIRECTORY = '''
from pathlib import Path

SOURCE = Path({source!r})


def apply(root: Path) -> None:
    """Create an empty directory in the source."""
    (SOURCE / "STRAY").mkdir()
'''


def write_script(folder: Path, text: str) -> Path:
    """Write an amendment script into a folder.

    Parameters
    ----------
    folder : Path
        Directory for the script.
    text : str
        Python source defining ``apply(root)``.

    Returns
    -------
    Path
        The script file.
    """
    script = folder / "amendment.py"
    script.write_text(text, encoding="utf-8")
    return script


class Rehearsal(unittest.TestCase):
    """A rehearsal changes only its copy and reports what it did."""

    def test_source_unchanged_copy_gains_entry(self) -> None:
        """Behavior: a script that appends an entry changes the copy
        only; the rehearsal reports the entry and a passing verify.

        Reference: an editorial amendment of STND.INSTR applied by a
        script; the source's digests before and after are compared.
        """
        with corpus_copy() as source, tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            script = write_script(work, AMENDMENT)
            before = tree_digests(source)
            count = len(read_ledger(source))
            (work / "copy").mkdir()
            done = rehearse(source, script, work / "copy")
            self.assertEqual(tree_digests(source), before)
            self.assertEqual(len(read_ledger(source)), count)
            self.assertEqual([e["seq"] for e in done.appended], [count + 1])
            self.assertEqual(len(read_ledger(done.copy)), count + 1)
            self.assertTrue(done.verification.passed())
            self.assertEqual(done.source_paths, len(before))

    def test_write_to_source_is_reported(self) -> None:
        """Behavior: a script that writes to the source corpus makes the
        rehearsal fail with the changed file named.

        Reference: the error of ledger entries 30 and 31, a rehearsal
        that appended to the live ledger, injected here into a copy.
        """
        with corpus_copy() as source, tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            script = write_script(work, STRAY.format(source=str(source)))
            (work / "copy").mkdir()
            with self.assertRaises(SourceChanged) as raised:
                rehearse(source, script, work / "copy")
            self.assertEqual(raised.exception.changed, ["ledger.jsonl"])

    def test_relative_root_survives_a_change_of_directory(self) -> None:
        """Behavior: a script that writes to the source and then changes
        the working directory is still caught, when the root was given
        as a relative path.

        Reference: a source named ``governance``, given as
        ``governance`` from its parent, and a copy also named
        ``governance``. Before review 0001 the second snapshot resolved
        the relative root against the new working directory, read the
        copy, and found nothing changed.
        """
        with corpus_copy() as source, tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            script = write_script(work, EVASIVE.format(source=str(source)))
            (work / "copy").mkdir()
            here = Path.cwd()
            os.chdir(source.parent)
            try:
                with self.assertRaises(SourceChanged) as raised:
                    rehearse(Path(source.name), script, work / "copy")
            finally:
                os.chdir(here)
            self.assertEqual(raised.exception.changed, ["ledger.jsonl"])

    def test_new_directory_in_source_is_reported(self) -> None:
        """Behavior: a script that adds an empty directory to the source
        makes the rehearsal fail.

        Reference: an empty directory ``STRAY`` created in the source;
        before review 0001 only files were compared.
        """
        with corpus_copy() as source, tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            text = NEW_DIRECTORY.format(source=str(source))
            script = write_script(work, text)
            (work / "copy").mkdir()
            with self.assertRaises(SourceChanged) as raised:
                rehearse(source, script, work / "copy")
            self.assertEqual(raised.exception.changed, ["STRAY"])

    def test_command_reports_a_refused_script(self) -> None:
        """Behavior: ``rehearse`` exits 1 with a message, not a
        traceback, for a script that defines no ``apply``.

        Reference: an empty script.
        """
        with corpus_copy() as source, tempfile.TemporaryDirectory() as tmp:
            script = write_script(Path(tmp), "")
            err = io.StringIO()
            with (
                tempfile.TemporaryDirectory() as copies,
                mock.patch.object(tempfile, "tempdir", copies),
                contextlib.redirect_stderr(err),
            ):
                code = main(["rehearse", str(source), str(script)])
            self.assertEqual(code, 1)
            self.assertIn("refused:", err.getvalue())
            self.assertIn("defines no function apply", err.getvalue())

    def test_command_prints_entries_and_summary(self) -> None:
        """Behavior: ``rehearse`` prints the copy, the appended entry,
        the verify summary, and the unchanged source, and exits 0.

        Reference: the editorial amendment script above.
        """
        with corpus_copy() as source, tempfile.TemporaryDirectory() as tmp:
            script = write_script(Path(tmp), AMENDMENT)
            before = tree_digests(source)
            out = io.StringIO()
            # The command makes its own temporary directory for the
            # copy; pointing it into one the test removes keeps no copy.
            with (
                tempfile.TemporaryDirectory() as copies,
                mock.patch.object(tempfile, "tempdir", copies),
                contextlib.redirect_stdout(out),
            ):
                code = main(["rehearse", str(source), str(script)])
            self.assertEqual(code, 0)
            text = out.getvalue()
            self.assertIn("appended: 1", text)
            self.assertIn("logic: PASS", text)
            self.assertIn(
                f"source unchanged: {len(before)} files and directories", text
            )
            self.assertEqual(tree_digests(source), before)


if __name__ == "__main__":
    unittest.main()
