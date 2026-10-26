"""Tests of the structural checks of ``verify``.

Identifiers, mnemonics, status, references, the verdict of the ledger
check, and the files that no scope pins. Ported in part from
``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import unittest
from pathlib import PurePosixPath

from govharness.checks.base import CheckContext
from govharness.checks.fields import check_keys_known, status_problems
from govharness.checks.ledger import ledger_intact, unpinned_files
from govharness.checks.registry import registered_keys
from govharness.checks.revisions.identifiers import read_register
from govharness.checks.structure import (
    id_problems,
    mnemonic_problems,
    reference_problems,
)
from govharness.core.corpus import Corpus, Tree, read_tree
from govharness.core.entry import Entry
from govharness.ledger.gpg import SignerConfig
from tests.support import (
    ROOT,
    corpus_of,
    live_entries,
    live_index,
    live_ledger,
)

# The paths that no transaction pinned before the round of 2026-10-26.
UNPINNED = {"KNOW", "README.md", "STND/_doc.md", "TAG", "_PROJECT"}


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

    def test_ids_match_paths(self) -> None:
        """Behavior: an entry whose ``id`` differs from its path is
        reported, and no live entry is.

        Reference: GOV.37; QA.8 part C, M5, which found no test of the
        check ids.
        """
        self.assertEqual(id_problems(live_entries()), [])
        bad = Entry(PurePosixPath("GOV/1.md"), {"id": "GOV.2"}, "")
        self.assertEqual(
            id_problems([bad]), ["id mismatch: GOV/1.md declares GOV.2"]
        )

    def test_mnemonics(self) -> None:
        """Behavior: a top-level directory is a mnemonic of two to five
        uppercase letters, or a grade the register lists; templates are
        skipped.

        Reference: STND.IDENT.17 and GOV.37, with the register row of
        LVL (grades 0 to 3); QA.8 part C, M5 (no test of the check
        mnemonics) and L4 (a digit admitted for any mnemonic).
        """
        register, _ = read_register(Corpus(live_entries()))
        self.assertEqual(mnemonic_problems(read_tree(ROOT), register), [])
        names = ["STND", "LVL0", "LVL3", "_PROJECT", "LVL4", "STND1", "Ab"]
        names += ["ABCDEF", "A"]
        tree = Tree(tuple(PurePosixPath(n) for n in [".", *names]))
        self.assertEqual(
            mnemonic_problems(tree, register),
            [f"bad mnemonic: {n}" for n in names[4:]],
        )

    def test_ledger_verdict(self) -> None:
        """Behavior: the ledger check passes the live corpus and fails
        a ledger with an altered entry.

        Reference: GOV.36; QA.8 part C, M5, the verdict of
        ``ledger_intact`` inverted, which the tests of ``ledger_problems``
        did not see.
        """
        tree = read_tree(ROOT)
        ledger = live_ledger()

        def verdict() -> str:
            """Return the ledger check's status for the ledger as it is.

            Returns
            -------
            str
                ``PASS`` or ``FAIL``.
            """
            ctx = CheckContext(
                Corpus([]), ledger, tree=tree, signer_config=SignerConfig()
            )
            return ledger_intact(ctx).status

        self.assertEqual(verdict(), "PASS")
        ledger[4]["rationale"] += " altered"
        self.assertEqual(verdict(), "FAIL")

    def test_unpinned_files(self) -> None:
        """Behavior: each Markdown file that no scope reaches fails, a
        directory none of whose files is reached named once; the failure
        goes once a scope reaches them, a file scope included.

        Reference: STND.HARN.31 and the term Reach of STND.HARN; QA.8
        part C, M1. The live ledger without the transactions that pin
        KNOW, TAG, the project template, STND/_doc.md, and README.md.
        """
        tree = read_tree(ROOT)
        ledger = [
            e
            for e in live_ledger()
            if not set(e.get("scope") or []) & UNPINNED
        ]
        ctx = CheckContext(corpus_of(live_index()), ledger, tree=tree)
        found = unpinned_files(ctx)
        self.assertEqual(found.status, "FAIL")
        self.assertEqual(
            found.details,
            [
                "- KNOW/ (1 file)",
                "- README.md",
                "- STND/_doc.md",
                "- TAG/ (8 files)",
                "- _PROJECT/ (9 files)",
            ],
        )
        ledger += [{"scope": [path]} for path in sorted(UNPINNED)]
        found = unpinned_files(CheckContext(Corpus([]), ledger, tree=tree))
        self.assertEqual((found.status, found.details), ("PASS", []))

    def test_check_keys_known(self) -> None:
        """Behavior: a ``checked_by`` key that names no registered check
        fails, naming the entry and the key; ``review`` and every key of
        the live corpus pass.

        Reference: STND.HARN.32; the key of STND.HARN.9 changed to a
        key no check has.
        """
        index = live_index()
        ctx = CheckContext(corpus_of(index), live_ledger())
        ctx.known_keys = registered_keys()
        self.assertEqual(check_keys_known(ctx).status, "PASS")
        index["STND.HARN.9"].meta["checked_by"] = ["review", "ledgr"]
        ctx = CheckContext(corpus_of(index), live_ledger())
        ctx.known_keys = registered_keys()
        found = check_keys_known(ctx)
        self.assertEqual(
            (found.status, found.details),
            ("FAIL", ["- STND.HARN.9: `ledgr` names no check"]),
        )


if __name__ == "__main__":
    unittest.main()
