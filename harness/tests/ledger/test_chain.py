"""Tests of ledger appends: the chain is checked before every append.

Unit 0002 criterion 1. Every damage is made to a copy of the corpus in
a fresh temporary directory.
"""

from __future__ import annotations

import contextlib
import io
import json
import threading
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any

from govharness.cli.main import main
from govharness.core.hashing import canonical_json, ledger_entry_hash
from govharness.ledger.chain import append, read_ledger
from govharness.ledger.transactions import chain_problems
from tests.support import corpus_copy

Entries = list[dict[str, Any]]
ANNOTATION = {
    "at": "2026-10-10T00:00:00+00:00",
    "type": "annotate",
    "actor": "The Custodian",
    "role": "custodians",
    "authority": [],
    "targets": [],
    "scope": [],
    "corpus_hash": None,
    "rationale": "Test.",
    "signature": "",
}


def rewrite(root: Path, edit: Callable[[Entries], None]) -> None:
    """Edit the ledger entries of a corpus copy and write them back.

    Parameters
    ----------
    root : Path
        Corpus copy.
    edit : Callable[[Entries], None]
        Changes the entries in place.
    """
    entries = read_ledger(root)
    edit(entries)
    text = "".join(canonical_json(e) + "\n" for e in entries)
    (root / "ledger.jsonl").write_text(text, encoding="utf-8")


def alter_reason(entries: Entries) -> None:
    """Alter the reason of entry 5 without rehashing it.

    Parameters
    ----------
    entries : Entries
        Ledger entries; changed in place.
    """
    entries[4]["rationale"] += " altered"


def drop_entry(entries: Entries) -> None:
    """Remove entry 10, leaving a gap in the sequence and the links.

    Parameters
    ----------
    entries : Entries
        Ledger entries; changed in place.
    """
    del entries[9]


def relink(entries: Entries) -> None:
    """Point entry 7 at a false previous hash and rehash it.

    Parameters
    ----------
    entries : Entries
        Ledger entries; changed in place.
    """
    entries[6]["prev"] = "0" * 64
    entries[6]["hash"] = ledger_entry_hash(entries[6])


def renumber(entries: Entries) -> None:
    """Give entry 3 the number 4 and rebuild every link and hash.

    Parameters
    ----------
    entries : Entries
        Ledger entries; changed in place.
    """
    entries[2]["seq"] = 4
    previous = None
    for entry in entries:
        entry["prev"] = previous
        entry["hash"] = ledger_entry_hash(entry)
        previous = entry["hash"]


DAMAGES: dict[str, tuple[Callable[[Entries], None], str]] = {
    "altered entry": (alter_reason, "ledger entry altered at seq 5"),
    "dropped entry": (drop_entry, "ledger sequence broken at entry 10"),
    "false link": (relink, "ledger chain broken at seq 7"),
    "renumbered entry": (renumber, "ledger sequence broken at entry 3"),
}


class ChainedAppend(unittest.TestCase):
    """An append extends an intact chain and refuses a broken one."""

    def test_append_refuses_a_broken_chain(self) -> None:
        """Behavior: an append to a broken ledger raises and writes
        nothing.

        Reference: four injected breaks (DAMAGES): an altered entry, a
        dropped entry, a false link, and a renumbered entry whose links
        and hashes were rebuilt, which only the sequence check sees.
        """
        for name, (damage, reason) in DAMAGES.items():
            with self.subTest(name), corpus_copy() as root:
                rewrite(root, damage)
                before = (root / "ledger.jsonl").read_bytes()
                with self.assertRaisesRegex(ValueError, reason):
                    append(root, dict(ANNOTATION))
                self.assertEqual((root / "ledger.jsonl").read_bytes(), before)

    def test_append_extends_an_intact_chain(self) -> None:
        """Behavior: an append to an intact ledger adds one chained line.

        Reference: the live ledger, copied; after the append the chain
        check finds nothing and the file grew by exactly one line.
        """
        with corpus_copy() as root:
            path = root / "ledger.jsonl"
            before = path.read_bytes()
            written = append(root, dict(ANNOTATION))
            after = path.read_bytes()
            self.assertTrue(after.startswith(before))
            added = after[len(before) :].decode()
            self.assertEqual(added.count("\n"), 1)
            self.assertEqual(json.loads(added), written)
            entries = read_ledger(root)
            self.assertEqual(written["seq"], len(entries))
            self.assertEqual(chain_problems(entries), [])

    def test_append_after_a_missing_final_newline(self) -> None:
        """Behavior: an append to a ledger whose last line lacks its
        newline starts a new line, so both entries stay readable.

        Reference: the live ledger, copied, with its final newline
        removed. Before review 0001 the new entry was written on the
        same line as the last one, and the ledger no longer parsed.
        """
        with corpus_copy() as root:
            path = root / "ledger.jsonl"
            path.write_bytes(path.read_bytes().rstrip(b"\n"))
            count = len(read_ledger(root))
            append(root, dict(ANNOTATION))
            entries = read_ledger(root)
            self.assertEqual(len(entries), count + 1)
            self.assertEqual(chain_problems(entries), [])

    def test_concurrent_appends_keep_the_chain(self) -> None:
        """Behavior: appends running at the same time each take their own
        sequence number and leave an intact chain.

        Reference: eight threads, each appending three entries to one
        copy; the ledger must gain 24 entries and pass the chain check.
        The lock that guarantees it (review 0001) is the stated protocol
        of DSGN.15; without it the race is likely but not certain, so a
        pass is evidence only together with the lock.
        """
        with corpus_copy() as root:
            count = len(read_ledger(root))

            def worker() -> None:
                """Append three annotations."""
                for _ in range(3):
                    append(root, dict(ANNOTATION))

            threads = [threading.Thread(target=worker) for _ in range(8)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            entries = read_ledger(root)
            self.assertEqual(len(entries), count + 24)
            self.assertEqual(chain_problems(entries), [])

    def test_command_refuses_a_broken_chain(self) -> None:
        """Behavior: ``ledger append`` exits 1, says why, and writes
        nothing when the chain is broken.

        Reference: an altered entry 5 in a copy of the ledger.
        """
        with corpus_copy() as root:
            rewrite(root, alter_reason)
            before = (root / "ledger.jsonl").read_bytes()
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                code = main(
                    [
                        "ledger",
                        "append",
                        str(root),
                        "--type",
                        "annotate",
                        "--actor",
                        "The Custodian",
                        "--role",
                        "custodians",
                        "--rationale",
                        "Test.",
                    ]
                )
            self.assertEqual(code, 1)
            self.assertIn("broken chain", errors.getvalue())
            self.assertEqual((root / "ledger.jsonl").read_bytes(), before)

    def test_command_refuses_a_scope_outside_the_root(self) -> None:
        """Behavior: ``ledger append`` refuses, as a usage error, a scope
        that leaves the corpus root, and writes nothing.

        Reference: the scopes ``..`` and an absolute path, both existing
        directories outside a corpus copy. The flat ``ledger.py`` pinned
        them, hashing files outside the corpus (fixed by review 0001).
        """
        with corpus_copy() as root:
            before = (root / "ledger.jsonl").read_bytes()
            for scope in ("..", str(root.parent)):
                with self.subTest(scope):
                    errors = io.StringIO()
                    with (
                        contextlib.redirect_stderr(errors),
                        self.assertRaises(SystemExit) as stop,
                    ):
                        main(
                            [
                                "ledger",
                                "append",
                                str(root),
                                "--type",
                                "annotate",
                                "--actor",
                                "The Custodian",
                                "--role",
                                "custodians",
                                "--scope",
                                scope,
                                "--rationale",
                                "Test.",
                            ]
                        )
                    self.assertEqual(stop.exception.code, 2)
                    self.assertIn(
                        "scope names no directory", errors.getvalue()
                    )
            self.assertEqual((root / "ledger.jsonl").read_bytes(), before)

    def test_chain_problems_names_each_break(self) -> None:
        """Behavior: the chain check names a gap, a false link, and an
        altered entry, and passes an intact chain.

        Reference: a hand-built three-entry chain and one damage of
        each kind.
        """
        chain: Entries = []
        previous = None
        for seq in (1, 2, 3):
            entry: dict[str, Any] = {"seq": seq, "prev": previous}
            entry["hash"] = ledger_entry_hash(entry)
            chain.append(entry)
            previous = entry["hash"]
        self.assertEqual(chain_problems(chain), [])
        self.assertEqual(
            chain_problems([chain[0], chain[2]]),
            [
                "ledger sequence broken at entry 2: seq 3",
                "ledger chain broken at seq 3",
            ],
        )
        altered = [chain[0], {**chain[1], "seq": 2, "note": "x"}, chain[2]]
        self.assertEqual(
            chain_problems(altered), ["ledger entry altered at seq 2"]
        )


if __name__ == "__main__":
    unittest.main()
