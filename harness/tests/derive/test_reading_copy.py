"""Tests of the reading copies (unit 0002 criterion 4)."""

from __future__ import annotations

import contextlib
import io
import os
import re
import unittest
from pathlib import Path

from govharness.cli.main import main
from govharness.core.corpus import read_corpus
from govharness.derive.reading_copy import (
    READING_COPIES,
    ReadingCopy,
    compose,
    series,
)
from tests.support import corpus_copy, corpus_of, live_index, live_ledger

COPIES = len(READING_COPIES)

DFLT = ReadingCopy("STND.DFLT", "defaults.md")
IDENT = next(c for c in READING_COPIES if c.document == "STND.IDENT")


def run(*args: str) -> tuple[int, str]:
    """Run one command and capture what it prints.

    Parameters
    ----------
    *args : str
        Command and arguments.

    Returns
    -------
    tuple[int, str]
        Exit code and standard output.
    """
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(list(args))
    return code, out.getvalue()


class ReadingCopies(unittest.TestCase):
    """Reading copies follow the corpus and the ledger."""

    def test_header_names_each_revision_and_entry(self) -> None:
        """Behavior: the header names the adoption and every later
        revision with its ledger entry and date.

        Reference: the ledger entries of STND.DFLT: adoption 1.0 in
        entry 33, then 1.0.1, 1.0.2, and 1.1 in entries 37, 39, and 40, and
        any later revision.
        """
        text = compose(corpus_of(live_index()), live_ledger(), DFLT)
        first = text.split("\n\n")[1]
        self.assertTrue(
            first.startswith(
                "Adopted by The Custodian as revision 1.0 in ledger entry "
                "33 (2026-10-10); revised to 1.0.1 in entry 37 (2026-10-10), "
                "1.0.2 in entry 39 (2026-10-10), 1.1 in entry 40 "
                "(2026-10-10)"
            ),
            first,
        )
        # Later revisions extend the list; each names its entry.
        self.assertRegex(first, r"\b(\d+\.\d+(\.\d+)?) in entry \d+ ")
        self.assertIn("the harness files are the system of record", first)

    def test_header_follows_the_ledger(self) -> None:
        """Behavior: a new revision transaction appears in the header.

        Reference: an injected ``amend`` entry 42 that names revision
        1.1.1 of STND.DFLT.
        """
        ledger = live_ledger()
        ledger.append(
            {
                "seq": 42,
                "type": "amend",
                "at": "2026-10-11T00:00:00+00:00",
                "targets": ["STND.DFLT"],
                "rationale": "Editorial amendment of STND.DFLT, "
                "revision 1.1.1.",
            }
        )
        text = compose(corpus_of(live_index()), ledger, DFLT)
        self.assertIn("and 1.1.1 in entry 42 (2026-10-11).", text)

    def test_every_provision_once_in_section_order(self) -> None:
        """Behavior: each provision appears once, under its section, and
        the history and text of the standard are kept.

        Reference: the 26 provisions of STND.DFLT in the live corpus.
        """
        index = live_index()
        text = compose(corpus_of(index), live_ledger(), DFLT)
        found = re.findall(r"^#### (STND\.DFLT\.\d+) ", text, re.M)
        wanted = [k for k in index if re.fullmatch(r"STND\.DFLT\.\d+", k)]
        self.assertEqual(sorted(found), sorted(wanted))
        self.assertEqual(len(found), len(set(found)))
        self.assertIn("\n## Revision History\n", text)
        self.assertIn("\n### Application\n", text)

    def test_register_follows_the_identifier_standard(self) -> None:
        """Behavior: the register MNEM is printed after the history of
        STND.IDENT.

        Reference: the reading copy that pointer.md describes, "with the
        register MNEM".
        """
        text = compose(corpus_of(live_index()), live_ledger(), IDENT)
        history = text.index("\n## Revision History\n")
        register = text.index("\n## The register MNEM\n")
        self.assertLess(history, register)
        self.assertIn("| SIGNR | none | Signer register |", text)

    def test_compose_writes_beside_a_root_given_as_dot(self) -> None:
        """Behavior: ``compose . --write`` run inside the corpus writes
        ``rendered/`` beside it, not into it.

        Reference: a corpus copy as the working directory. Before review
        0001, ``Path(".").parent`` is ``.``, so the copies went into the
        corpus, where ``rendered`` is no mnemonic and breaks ``verify``.
        """
        with corpus_copy() as root:
            here = Path.cwd()
            os.chdir(root)
            try:
                code, out = run("compose", ".", "--write")
            finally:
                os.chdir(here)
            self.assertEqual((code, out), (0, f"written: {COPIES}\n"))
            self.assertTrue((root.parent / "rendered").is_dir())
            self.assertFalse((root / "rendered").exists())

    def test_compose_check_finds_a_stale_copy(self) -> None:
        """Behavior: ``compose --write`` writes every copy, ``--check``
        then passes, and an edited provision makes its copy stale.

        Reference: an injected edit of STND/DFLT/1.md in a copy of the
        corpus.
        """
        with corpus_copy() as root:
            rendered = root.parent / "rendered"
            code, out = run("compose", str(root), "--write")
            self.assertEqual((code, out), (0, f"written: {COPIES}\n"))
            self.assertEqual(len(list(rendered.iterdir())), COPIES)
            self.assertEqual(run("compose", str(root), "--check")[0], 0)
            provision = root / "STND" / "DFLT" / "1.md"
            provision.write_text(provision.read_text() + " Edited.")
            code, out = run("compose", str(root), "--check")
            self.assertEqual(code, 1)
            self.assertEqual(out, "stale: rendered/defaults.md\nstale: 1\n")

    def test_series(self) -> None:
        """Behavior: series join with a serial comma.

        Reference: one, two, and three items.
        """
        self.assertEqual(series(["a"]), "a")
        self.assertEqual(series(["a", "b"]), "a and b")
        self.assertEqual(series(["a", "b", "c"]), "a, b, and c")

    def test_rendered_copies_are_current(self) -> None:
        """Behavior: the copies in ``rendered/`` equal the derived ones.

        Reference: the repository's ``rendered/``; regression guard of
        the files written by ``compose --write``.
        """
        root = Path(__file__).resolve().parents[2] / "governance"
        self.assertEqual(run("compose", str(root), "--check")[0], 0)

    def test_compose_all_writes_every_document(self) -> None:
        """Behavior: ``compose ROOT --all DIR`` writes a reading copy
        ``<ID>.md`` of every document into DIR, ``--check`` then
        passes, an edited provision makes its copy stale and the check
        names it, a Markdown file of DIR that no document produces is
        named as an orphan in both modes and fails the check without
        being removed, DIR is created with its parents, and
        ``compose`` without ``--all``, ``--check``, or ``--write`` is
        a usage error.

        Reference: a copy of the corpus, whose documents are its
        ``_doc.md`` files; a DIR two levels below an existing
        directory; an injected edit of STND/DFLT/1.md; a stray
        ``NOPE.md`` (unit 0022, HR-6; its review, Low 3 and mutant
        16).
        """
        with corpus_copy() as root:
            out_dir = root.parent / "all" / "copies"
            documents = sorted(
                str(e.meta["id"])
                for e in read_corpus(root).entries
                if e.path.name == "_doc.md"
            )
            self.assertGreater(len(documents), 70)
            code, out = run("compose", str(root), "--all", str(out_dir))
            self.assertEqual((code, out), (0, f"written: {len(documents)}\n"))
            written = sorted(p.name for p in out_dir.iterdir())
            self.assertEqual(written, sorted(f"{d}.md" for d in documents))
            self.assertEqual(
                run("compose", str(root), "--all", str(out_dir), "--check"),
                (0, "stale: 0\n"),
            )
            provision = root / "STND" / "DFLT" / "1.md"
            provision.write_text(provision.read_text() + " Edited.")
            code, out = run(
                "compose", str(root), "--all", str(out_dir), "--check"
            )
            self.assertEqual(
                (code, out), (1, "stale: STND.DFLT.md\nstale: 1\n")
            )
            code, _ = run("compose", str(root), "--all", str(out_dir))
            self.assertEqual(code, 0)
            (out_dir / "NOPE.md").write_text("stray\n", encoding="utf-8")
            code, out = run(
                "compose", str(root), "--all", str(out_dir), "--check"
            )
            self.assertEqual((code, out), (1, "orphan: NOPE.md\nstale: 0\n"))
            self.assertTrue((out_dir / "NOPE.md").exists())
            code, out = run("compose", str(root), "--all", str(out_dir))
            self.assertEqual((code, out), (0, "orphan: NOPE.md\nwritten: 0\n"))
            self.assertEqual((out_dir / "NOPE.md").read_text(), "stray\n")
            err = io.StringIO()
            with (
                contextlib.redirect_stderr(err),
                self.assertRaises(SystemExit) as stop,
            ):
                main(["compose", str(root)])
            self.assertEqual(stop.exception.code, 2)
            self.assertIn("--all DIR", err.getvalue())

    def test_repository_rendered_copies_are_current(self) -> None:
        """Behavior: ``compose --all`` of the live corpus against the
        repository's ``rendered/`` reports no stale copy and no orphan,
        so the committed set is exactly one copy per document.

        Reference: ``REPO/rendered/``, the reading copies the
        custodian's process rebuilds (CUSTODIAN.md step 8; unit 0022,
        HR-6); regression guard.
        """
        repo = Path(__file__).resolve().parents[3]
        code, out = run(
            "compose",
            str(repo / "harness" / "governance"),
            "--all",
            str(repo / "rendered"),
            "--check",
        )
        self.assertEqual((code, out), (0, "stale: 0\n"))


if __name__ == "__main__":
    unittest.main()
