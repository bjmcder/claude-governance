"""Tests of the solve cache on disk and of its commands (unit 0011).

Each test names its own cache directory under a fresh temporary
directory; the corpus read is the live one, never written, or a copy.
"""

from __future__ import annotations

import contextlib
import io
import multiprocessing
import os
import stat
import tempfile
import time
import types
import unittest
from collections.abc import Iterator
from pathlib import Path
from unittest import mock

from govharness.cli.main import main
from govharness.workflows import solve_store
from govharness.workflows.rehearse import rehearse
from govharness.workflows.solve_store import (
    ENV_DIRECTORY,
    ENV_DISABLE,
    MAX_ENTRY,
    XDG_CACHE,
    SolveStore,
    open_store,
    solver_version,
)
from govharness.workflows.verification import verify_corpus
from tests.support import ROOT, corpus_copy
from tests.workflows.test_rehearse import AMENDMENT, write_script

KEY = "ab" + "0" * 62
OTHER = "cd" + "1" * 62
WRITERS = 4
WRITES = 60
PAYLOAD = 1 << 18  # bytes of each entry a concurrent writer writes


@contextlib.contextmanager
def scratch() -> Iterator[Path]:
    """Yield a fresh temporary directory, removed afterwards.

    Yields
    ------
    Path
        The directory.
    """
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


def run(argv: list[str]) -> tuple[int, str, str]:
    """Run the command line in this process.

    Parameters
    ----------
    argv : list[str]
        Arguments after the program name.

    Returns
    -------
    tuple[int, str, str]
        Exit code, standard output, and standard error.
    """
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def entries(directory: Path) -> dict[str, tuple[int, int]]:
    """Return the inode and modification time of each cache entry.

    Parameters
    ----------
    directory : Path
        Cache directory.

    Returns
    -------
    dict[str, tuple[int, int]]
        By file name; a rewritten entry has a new inode, since writes
        rename a new file over the old.
    """
    return {
        p.name: (p.stat().st_ino, p.stat().st_mtime_ns)
        for p in directory.rglob("*.json")
    }


def write_many(directory: str, payload: bytes) -> None:
    """Write one entry many times; the body of a concurrent writer.

    Parameters
    ----------
    directory : str
        Cache directory.
    payload : bytes
        Entry to write.
    """
    store = SolveStore(Path(directory), "v")
    for _ in range(WRITES):
        store.save({KEY: payload})


class Store(unittest.TestCase):
    """Entries are written whole and read only when plainly readable."""

    def test_round_trip_and_modes(self) -> None:
        """Behavior: a saved entry loads as written, in a private
        directory with mode 0600, and leaves no temporary file; a key
        not saved and a malformed key load nothing.

        Reference: one entry saved and loaded.
        """
        with scratch() as tmp:
            store = SolveStore(tmp / "cache", "v")
            store.save({KEY: b"entry", "../escape": b"x"})
            self.assertEqual(
                store.load([KEY, OTHER, "../escape", "AB" * 32]),
                {KEY: b"entry"},
            )
            path = store.path(KEY)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
            self.assertEqual(
                sorted(p.name for p in (tmp / "cache").rglob("*")),
                [KEY[:2], path.name],
            )

    def test_unreadable_entries_are_skipped(self) -> None:
        """Behavior: an entry that is a symbolic link, a named pipe, a
        directory, larger than the limit, or under a linked directory is
        not loaded, and loading does not block.

        Reference: one planted object of each kind.
        """
        with scratch() as tmp:
            store = SolveStore(tmp / "cache", "v")
            store.save({KEY: b"real"})
            target = tmp / "target.json"
            target.write_bytes(b"planted")
            keys = {
                "link": "01" + "2" * 62,
                "pipe": "02" + "2" * 62,
                "directory": "03" + "2" * 62,
                "large": "04" + "2" * 62,
            }
            for label, key in keys.items():
                path = store.path(key)
                path.parent.mkdir(parents=True, exist_ok=True)
                if label == "link":
                    path.symlink_to(target)
                elif label == "pipe":
                    os.mkfifo(path)
                elif label == "directory":
                    path.mkdir()
                else:
                    path.write_bytes(b"x" * (MAX_ENTRY + 1))
            linked = "05" + "2" * 62
            (tmp / "elsewhere").mkdir()
            (tmp / "elsewhere" / f"{linked}.json").write_bytes(b"planted")
            (tmp / "cache" / "05").symlink_to(tmp / "elsewhere")
            self.assertEqual(
                store.load([*keys.values(), linked, KEY]), {KEY: b"real"}
            )
            store.save({linked: b"new"})
            self.assertEqual(
                (tmp / "elsewhere" / f"{linked}.json").read_bytes(),
                b"planted",
            )

    def test_concurrent_writers_leave_a_whole_entry(self) -> None:
        """Behavior: four processes writing one key 60 times each, with
        two different entries, never let a reader see a partial entry,
        and leave one of the two and no temporary file.

        Reference: entries of 256 KiB, read in a loop while the writers
        run.
        """
        payloads = [bytes([65 + n % 2]) * PAYLOAD for n in range(WRITERS)]
        with scratch() as tmp:
            directory = tmp / "cache"
            context = multiprocessing.get_context("spawn")
            writers = [
                context.Process(target=write_many, args=(str(directory), p))
                for p in payloads
            ]
            for writer in writers:
                writer.start()
            store = SolveStore(directory, "v")
            seen: set[bytes] = set()
            deadline = time.monotonic() + 120
            while any(w.is_alive() for w in writers):
                self.assertLess(time.monotonic(), deadline)
                seen |= set(store.load([KEY]).values())
            for writer in writers:
                writer.join()
                self.assertEqual(writer.exitcode, 0)
            self.assertTrue(seen)
            self.assertLessEqual(seen, set(payloads))
            self.assertIn(store.load([KEY])[KEY], set(payloads))
            self.assertEqual(
                [p.name for p in directory.rglob("*") if p.is_file()],
                [f"{KEY}.json"],
            )


class Location(unittest.TestCase):
    """The options and the environment name or turn off the cache."""

    def test_precedence(self) -> None:
        """Behavior: ``--no-cache`` turns the cache off; ``--cache-dir``
        overrides the environment; ``GOVHARNESS_NO_CACHE`` turns it off
        unless empty or ``0``; ``GOVHARNESS_CACHE_DIR`` names it; else
        it lies under an absolute ``XDG_CACHE_HOME`` or ``~/.cache``.

        Reference: each setting in turn, with the environment patched.
        """
        clean = {
            k: v
            for k, v in os.environ.items()
            if k not in {ENV_DIRECTORY, ENV_DISABLE, XDG_CACHE}
        }
        with mock.patch.dict(os.environ, clean, clear=True):
            self.assertIsNone(open_store(False, Path("/x")))
            given = open_store(True, Path("/x/c"))
            self.assertEqual(given.directory, Path("/x/c"))
            with mock.patch.dict(os.environ, {ENV_DISABLE: "1"}):
                self.assertIsNone(open_store())
                self.assertIsNotNone(open_store(True, Path("/x")))
            with mock.patch.dict(os.environ, {ENV_DISABLE: "0"}):
                self.assertIsNotNone(open_store())
            with mock.patch.dict(os.environ, {ENV_DIRECTORY: "/y"}):
                self.assertEqual(open_store().directory, Path("/y"))
            with mock.patch.dict(os.environ, {XDG_CACHE: "/z"}):
                self.assertEqual(
                    open_store().directory, Path("/z/govharness/solves")
                )
            with mock.patch.dict(os.environ, {XDG_CACHE: "relative"}):
                self.assertEqual(
                    open_store().directory,
                    Path.home() / ".cache" / "govharness" / "solves",
                )

    def test_version_follows_the_solver_source(self) -> None:
        """Behavior: the version is a digest of the solver's source, so
        an edit of a source file gives a new version, and an unreadable
        source turns the cache off.

        Reference: two stand-in modules whose files are edited.
        """
        self.assertRegex(solver_version() or "", r"^[0-9a-f]{64}$")
        with scratch() as tmp:
            files = [tmp / "a.py", tmp / "b.py"]
            for path in files:
                path.write_text("x = 1\n", encoding="utf-8")
            modules = tuple(
                types.SimpleNamespace(__file__=str(p), __name__=p.stem)
                for p in files
            )
            with mock.patch.object(solve_store, "SOURCES", modules):
                before = solver_version()
                files[1].write_text("x = 2\n", encoding="utf-8")
                self.assertNotEqual(solver_version(), before)
                files[0].unlink()
                self.assertIsNone(solver_version())
                self.assertIsNone(open_store(True, tmp / "cache"))

    def test_cache_inside_the_corpus_is_refused(self) -> None:
        """Behavior: a cache directory inside the corpus is refused, by
        the workflow with ``ValueError`` and by the commands with exit 2,
        and nothing is written there.

        Reference: a copy of the corpus with ``--cache-dir`` under it.
        """
        with corpus_copy() as root:
            inside = root / "STND" / "cache"
            store = open_store(True, inside)
            with self.assertRaises(ValueError):
                verify_corpus(root, cache=store)
            for command in ("verify", "check"):
                with self.subTest(command):
                    code, _, err = run(
                        [command, str(root), "--cache-dir", str(inside)]
                    )
                    self.assertEqual(code, 2)
                    self.assertIn("inside the corpus", err)
            self.assertFalse(inside.exists())


class Commands(unittest.TestCase):
    """``verify`` and ``check`` print the same with or without a cache."""

    def test_verify_is_identical_cold_warm_and_without(self) -> None:
        """Behavior: ``verify`` of the live corpus prints the same with a
        cold cache, a warm one, and ``--no-cache``; the warm run writes
        no entry, and ``--no-cache`` writes none.

        Reference: three runs with one cache directory.
        """
        with scratch() as tmp:
            cache = ["--cache-dir", str(tmp / "cache")]
            cold = run(["verify", str(ROOT), *cache])
            written = entries(tmp / "cache")
            warm = run(["verify", str(ROOT), *cache])
            self.assertEqual(entries(tmp / "cache"), written)
            with mock.patch.dict(os.environ, {ENV_DIRECTORY: str(tmp / "n")}):
                bare = run(["verify", str(ROOT), "--no-cache"])
            self.assertFalse((tmp / "n").exists())
            self.assertEqual(cold[0], 0)
            self.assertEqual(len(written), 8)
            self.assertEqual(warm, cold)
            self.assertEqual(bare, cold)

    def test_check_reports_are_identical(self) -> None:
        """Behavior: ``check --out-dir`` prints and writes the same
        report, facts, and punch list with a cold cache, a warm one, and
        none.

        Reference: three runs into three output directories.
        """
        with scratch() as tmp:
            outputs = {}
            for label, extra in (
                ("cold", ["--cache-dir", str(tmp / "cache")]),
                ("warm", ["--cache-dir", str(tmp / "cache")]),
                ("none", ["--no-cache"]),
            ):
                out = tmp / label
                printed = run(
                    ["check", str(ROOT), "--out-dir", str(out), *extra]
                )
                files = {p.name: p.read_bytes() for p in out.iterdir()}
                outputs[label] = (printed, files)
            self.assertEqual(len(outputs["cold"][1]), 3)
            self.assertEqual(outputs["warm"], outputs["cold"])
            self.assertEqual(outputs["none"], outputs["cold"])

    def test_corrupt_entry_is_named_and_rewritten(self) -> None:
        """Behavior: a corrupt entry leaves the output of ``verify`` as
        it was, is named on the standard error, and is rewritten whole.

        Reference: every entry of a warm cache truncated to half.
        """
        with scratch() as tmp:
            cache = ["--cache-dir", str(tmp / "cache")]
            code, expected, _ = run(["verify", str(ROOT), *cache])
            good = {p: p.read_bytes() for p in (tmp / "cache").rglob("*.json")}
            for path, data in good.items():
                path.write_bytes(data[: len(data) // 2])
            again, printed, err = run(["verify", str(ROOT), *cache])
            self.assertEqual((again, printed), (code, expected))
            self.assertEqual(err.count("refused (not JSON); recomputed"), 8)
            self.assertEqual({p: p.read_bytes() for p in good}, good)


class Rehearsals(unittest.TestCase):
    """A rehearsal reuses the entries of another copy of the corpus."""

    def test_rehearsals_on_two_copies_share_entries(self) -> None:
        """Behavior: two rehearsals of one amendment, each on its own
        copy, verify alike; the second writes no entry, since every
        solve of its transaction and of its verify hits; and without
        the cache it verifies alike too.

        Reference: the editorial amendment of STND.INSTR of
        ``test_rehearse``, which leaves the authority-tier statements
        unchanged, rehearsed on fresh copies of the corpus.
        """
        with corpus_copy() as source, scratch() as tmp:
            script = write_script(tmp, AMENDMENT)
            done = []
            settings = (
                {ENV_DIRECTORY: str(tmp / "cache")},
                {ENV_DIRECTORY: str(tmp / "cache")},
                {ENV_DISABLE: "1"},
            )
            seen = []
            for number, setting in enumerate(settings):
                (tmp / f"copy{number}").mkdir()
                with mock.patch.dict(os.environ, setting):
                    done.append(
                        rehearse(source, script, tmp / f"copy{number}")
                    )
                seen.append(entries(tmp / "cache"))
            self.assertEqual(len(seen[0]), 8)
            self.assertEqual(seen[1], seen[0])
            self.assertEqual(seen[2], seen[0])
            for other in done[1:]:
                self.assertEqual(other.verification, done[0].verification)
            self.assertTrue(done[0].verification.passed())


if __name__ == "__main__":
    unittest.main()
