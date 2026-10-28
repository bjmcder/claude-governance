"""Tests of the command-line parser, the default root, and exit codes."""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path
from unittest import mock

from govharness.cli.arguments import ENV_ROOT, split_root
from govharness.cli.main import main
from tests.support import ROOT, corpus_copy

ROOT_COMMANDS = (
    ["verify"],
    ["check"],
    ["manifests", "--check"],
    ["references", "--check"],
    ["compose", "--check"],
)
# The read-only commands, each with its positional form after the root.
QUERIES = (
    ["show", "GOV.38"],
    ["find", "remote", "write"],
    ["context", "remote", "write"],
    ["pairs", "NUMER"],
    ["verify", "--no-logic"],
)


def run(argv: list[str]) -> tuple[int, str, str]:
    """Run the command line in this process.

    Parameters
    ----------
    argv : list[str]
        Arguments after the program name.

    Returns
    -------
    tuple[int, str, str]
        Exit code, standard output, and standard error; a parser exit
        gives its code.
    """
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as stop:
            code = int(stop.code or 0)
    return code, out.getvalue(), err.getvalue()


@contextlib.contextmanager
def working_directory(path: Path) -> Iterator[None]:
    """Run the body in another working directory.

    Parameters
    ----------
    path : Path
        The directory.

    Yields
    ------
    None
        With the working directory changed, restored afterwards.
    """
    here = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(here)


class DefaultRoot(unittest.TestCase):
    """The read-only commands take the root from the environment."""

    def test_root_from_the_environment(self) -> None:
        """Behavior: with ``GOVHARNESS_ROOT`` set and no root given,
        each read-only command runs on that corpus, from any working
        directory, and prints what the positional form prints.

        Reference: the live corpus, named by the variable, from an
        empty temporary directory (unit 0022, HR-5).
        """
        with (
            tempfile.TemporaryDirectory() as tmp,
            working_directory(Path(tmp)),
        ):
            for query in QUERIES:
                with self.subTest(query[0]):
                    with mock.patch.dict(os.environ, {ENV_ROOT: str(ROOT)}):
                        short = run(query)
                    long = run([query[0], str(ROOT), *query[1:]])
                    self.assertEqual(short[0], 0)
                    self.assertEqual(short, long)

    def test_root_from_the_working_directory(self) -> None:
        """Behavior: with the variable unset, ``./governance`` is the
        root when it exists.

        Reference: a copy of the corpus under a temporary directory,
        which is the working directory (unit 0022, HR-5).
        """
        env = {k: v for k, v in os.environ.items() if k != ENV_ROOT}
        with (
            corpus_copy() as root,
            working_directory(root.parent),
            mock.patch.dict(os.environ, env, clear=True),
        ):
            for query in QUERIES:
                with self.subTest(query[0]):
                    self.assertEqual(run(query)[0], 0)

    def test_no_root_is_a_usage_error(self) -> None:
        """Behavior: with the variable unset and no ``./governance``,
        each read-only command exits 2 with one line on the standard
        error naming the variable; a variable naming no directory does
        the same.

        Reference: an empty temporary directory (unit 0022, HR-5).
        """
        env = {k: v for k, v in os.environ.items() if k != ENV_ROOT}
        with (
            tempfile.TemporaryDirectory() as tmp,
            working_directory(Path(tmp)),
        ):
            for query in QUERIES:
                with self.subTest(query[0]):
                    with mock.patch.dict(os.environ, env, clear=True):
                        code, out, err = run(query)
                    self.assertEqual((code, out), (2, ""))
                    self.assertEqual(len(err.splitlines()), 1)
                    self.assertIn(ENV_ROOT, err)
                    bad = {ENV_ROOT: str(Path(tmp) / "absent")}
                    with mock.patch.dict(os.environ, bad):
                        code, out, err = run(query)
                    self.assertEqual((code, out), (2, ""))
                    self.assertIn(f"{ENV_ROOT}=", err)
                    self.assertIn("no such directory", err)

    def test_first_word_is_the_root_only_when_a_directory(self) -> None:
        """Behavior: for ``find`` and ``context``, the first positional
        argument is the root where a directory of that name exists,
        and the first word otherwise.

        Reference: ``split_root`` on a temporary directory and on a
        word that names none (unit 0022, HR-5).
        """
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                split_root(tmp, ["remote"]), (Path(tmp), ["remote"])
            )
            absent = str(Path(tmp) / "remote")
            self.assertEqual(
                split_root(absent, ["write"]), (None, [absent, "write"])
            )
        self.assertEqual(split_root(None, ["write"]), (None, ["write"]))


class ExitCodes(unittest.TestCase):
    """One rule: 0 found, 1 not found on stderr, 2 for a usage error."""

    def test_not_found_exits_one_on_stderr(self) -> None:
        """Behavior: ``show``, ``find``, ``context``, and ``pairs`` exit
        1 when nothing is found, with one line on the standard error
        and nothing on the standard output; and 0 when something is.

        Reference: an identifier, a word, and a document absent from
        the live corpus (unit 0022, HR-10; before it ``pairs`` exited 2
        and ``context`` printed to the standard output and exited 0).
        """
        absent = (
            ["show", "STND.NOPE.1"],
            ["find", "zzzqqq"],
            ["context", "zzzqqq"],
            ["pairs", "NOPE"],
        )
        for query in absent:
            with self.subTest(query[0]):
                code, out, err = run([query[0], str(ROOT), *query[1:]])
                self.assertEqual((code, out), (1, ""))
                self.assertEqual(len(err.splitlines()), 1)
                self.assertTrue(err.startswith(f"{query[0]}: "))
        for query in QUERIES[:4]:
            with self.subTest(query[0]):
                code, out, err = run([query[0], str(ROOT), *query[1:]])
                self.assertEqual((code, err), (0, ""))
                self.assertTrue(out)

    def test_show_resolves_case(self) -> None:
        """Behavior: ``show`` of an identifier in the wrong case prints
        the item.

        Reference: ``stnd.py`` for STND.PY (unit 0022, HR-10).
        """
        code, out, _ = run(["show", str(ROOT), "stnd.py"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("## STND.PY — Python standard"))

    def test_show_all_prints_the_provisions(self) -> None:
        """Behavior: ``show DOC --all`` prints each provision of the
        document whole, under its heading, after the document's lists.

        Reference: STND.PY, 33 provisions (unit 0022, HR-2).
        """
        code, out, _ = run(["show", str(ROOT), "STND.PY", "--all"])
        self.assertEqual(code, 0)
        self.assertGreaterEqual(out.count("\n## STND.PY."), 33)
        self.assertIn("\n## STND.PY.1 — ", out.split("Holds:")[1])

    def test_given_root_must_be_a_directory(self) -> None:
        """Behavior: a root given to ``show`` or ``pairs`` that is no
        directory is a usage error, exit 2, as before the root became
        optional.

        Reference: a path inside a fresh temporary directory (unit
        0022, HR-5).
        """
        with tempfile.TemporaryDirectory() as tmp:
            missing = str(Path(tmp) / "absent")
            for command, ident in (("show", "GOV.38"), ("pairs", "NUMER")):
                with self.subTest(command):
                    code, _, err = run([command, missing, ident])
                    self.assertEqual(code, 2)
                    self.assertIn(f"{missing}: no such directory", err)


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


class UnreadableFile(unittest.TestCase):
    """``verify`` names a file it cannot read (unit 0016)."""

    def test_front_matter_error_names_the_file(self) -> None:
        """Behavior: ``verify`` of a corpus with a file whose front
        matter is missing exits 2 and names that file.

        Reference: GOV/36.md with its front matter removed, in a copy.
        QA.8 part B, L2: the message was only ``refused: missing front
        matter``.
        """
        with corpus_copy() as root:
            path = root / "GOV" / "36.md"
            path.write_text(path.read_text().split("---", 2)[2], "utf-8")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = main(["verify", "--no-logic", str(root)])
            self.assertEqual(code, 2)
            self.assertEqual(
                err.getvalue(), "refused: GOV/36.md: missing front matter\n"
            )


if __name__ == "__main__":
    unittest.main()
