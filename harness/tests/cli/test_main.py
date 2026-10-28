"""Tests of the command-line parser, the default root, and exit codes."""

from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path
from unittest import mock

from govharness.cli.arguments import ENV_ROOT, split_root
from govharness.cli.main import entry, main
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

    def test_first_word_is_the_root_only_when_a_corpus(self) -> None:
        """Behavior: for ``find`` and ``context``, the first positional
        argument is the root where a directory of that name holds
        ``LVL0/_doc.md``, and the first word otherwise, a word naming
        a directory of the project included; so run from a project
        with ``tests/``, with the variable set, ``find tests coverage``
        searches the corpus for both words.

        Reference: ``split_root`` on the live corpus, on a temporary
        directory, and on a word that names none; a working directory
        holding ``tests/notes.md`` (unit 0022, HR-5; its review, High
        1, where ``tests/`` was read as the corpus).
        """
        self.assertEqual(split_root(str(ROOT), ["remote"]), (ROOT, ["remote"]))
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                split_root(tmp, ["remote"]), (None, [tmp, "remote"])
            )
            absent = str(Path(tmp) / "remote")
            self.assertEqual(
                split_root(absent, ["write"]), (None, [absent, "write"])
            )
            tests = Path(tmp) / "tests"
            tests.mkdir()
            (tests / "notes.md").write_text("# Notes\n", encoding="utf-8")
            with (
                working_directory(Path(tmp)),
                mock.patch.dict(os.environ, {ENV_ROOT: str(ROOT)}),
            ):
                for command in ("find", "context"):
                    with self.subTest(command):
                        short = run([command, "tests", "coverage"])
                        long = run([command, str(ROOT), "tests", "coverage"])
                        self.assertEqual(short[0], 0)
                        self.assertEqual(short, long)
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

    def test_show_and_pairs_resolve_case(self) -> None:
        """Behavior: ``show`` of an identifier in the wrong case prints
        the item, and ``pairs`` of one prints the pairs of the
        document, under its identifier as the corpus writes it.

        Reference: ``stnd.py`` for STND.PY, ``numer`` for NUMER (unit
        0022, HR-10; its review, Low 4).
        """
        code, out, _ = run(["show", str(ROOT), "stnd.py"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("## STND.PY — Python standard"))
        lower = run(["pairs", str(ROOT), "numer"])
        self.assertEqual(lower[0], 0)
        self.assertEqual(lower, run(["pairs", str(ROOT), "NUMER"]))
        self.assertIn("change of NUMER (STND.HARN.28)", lower[1])

    def test_pairs_with_other_documents_of_the_change(self) -> None:
        """Behavior: ``pairs ROOT NUMER --with HW`` lists the pairs of a
        change of both documents, more than of NUMER alone, under a
        heading that names both; an unknown document after ``--with``
        exits 1.

        Reference: STND.HARN.28 (unit 0024): pairs of common
        instantiation are listed where both provisions are in documents
        that the change adopts or amends.
        """
        alone = run(["pairs", str(ROOT), "NUMER"])
        both = run(["pairs", str(ROOT), "NUMER", "--with", "hw"])
        self.assertEqual(both[0], 0)
        self.assertIn("change of NUMER, HW (STND.HARN.28)", both[1])
        self.assertGreater(len(both[1]), len(alone[1]))
        code, out, err = run(["pairs", str(ROOT), "NUMER", "--with", "NOPE"])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("pairs: NOPE is not a document or provision", err)

    def test_pairs_refuses_what_it_does_not_take(self) -> None:
        """Behavior: ``pairs`` exits 1 with one line on the standard
        error, and nothing on the standard output, for a LVL0 provision
        given as ``ID``, a LVL0 article given without ``--amends``, an
        ``--amends`` identifier that names no LVL0 provision, and a
        change that puts no pair to review; a LVL0 article with
        ``--amends`` and options before ``ID`` are taken.

        Reference: unit 0024, review Should-fix 2 and 3 and Optional 4;
        docs/operating.md: exit 1 when nothing is found.
        """
        refused = (
            (["VV.1"], "VV.1 is not a document or provision below LVL0"),
            (["GOV"], "GOV is a LVL0 document, given without --amends"),
            (["NUMER", "--amends", "NOPE"], "--amends NOPE is not a LVL0"),
            (["NUMER", "--amends", "NUMER.11"], "--amends NUMER.11 is not"),
            (["STND.VVUQ"], "no pair to review before a change of STND.VVUQ"),
            (["QA", "--amends", "QA.11"], "no pair to review"),
        )
        for argv, message in refused:
            with self.subTest(argv):
                code, out, err = run(["pairs", str(ROOT), *argv])
                self.assertEqual((code, out), (1, ""))
                self.assertEqual(len(err.splitlines()), 1)
                self.assertIn(message, err)
        code, out, _ = run(["pairs", str(ROOT), "LVL0", "--amends", "VV.1"])
        self.assertEqual(code, 0)
        self.assertIn("339 pair(s).", out)
        first = run(["pairs", "--with", "HW", "--", str(ROOT), "NUMER"])
        last = run(["pairs", str(ROOT), "NUMER", "--with", "HW"])
        self.assertEqual(first[0], 0)
        self.assertEqual(first, last)

    def test_best_hold_is_the_most_any_match_holds(self) -> None:
        """Behavior: where no item holds every word, ``find`` reports
        the most words any match holds, which may exceed what the
        first match holds, since items rank before prose.

        Reference: "evidence level assignment reproducibility zyzzyva"
        on the live corpus: STND.KNOW.4 holds three words and is
        first, the Notes of STND.CXX hold four (unit 0022, HR-1; its
        review, mutant 12).
        """
        words = ["evidence", "level", "assignment", "reproducibility"]
        code, out, _ = run(["find", str(ROOT), *words, "zyzzyva"])
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(lines[0], "(no item holds every word; best hold 4)")
        self.assertEqual(lines[1], "- STND.KNOW.4 — Evidence level assignment")
        self.assertIn("- STND.CXX#notes — Notes", lines)

    def test_entry_exits_with_the_code(self) -> None:
        """Behavior: the console script's entry point exits with the
        code of the command, 1 for an item not found and 0 for one
        found.

        Reference: ``show`` of STND.NOPE.1 and of GOV.38 through
        ``entry`` with the arguments in ``sys.argv`` (unit 0022, HR-5;
        its review, mutant 14).
        """
        for ident, expected in (("STND.NOPE.1", 1), ("GOV.38", 0)):
            with self.subTest(ident):
                argv = ["govharness", "show", str(ROOT), ident]
                with (
                    mock.patch.object(sys, "argv", argv),
                    contextlib.redirect_stdout(io.StringIO()),
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit) as stop,
                ):
                    entry()
                self.assertEqual(stop.exception.code, expected)

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
