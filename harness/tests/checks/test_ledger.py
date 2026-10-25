"""Tests of the ledger check of ``verify``: chain, pins, and scopes.

Every damage is made to a copy of the corpus in a fresh temporary
directory. Ported from ``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path
from typing import Any

from govharness.checks.ledger import ledger_problems
from govharness.cli.main import main
from govharness.core.corpus import corpus_hash, read_tree, tree_digests
from govharness.core.hashing import ledger_entry_hash
from govharness.ledger.chain import append, read_ledger
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.transactions import latest_pins
from govharness.workflows.amend import Change, record_transaction
from tests.ledger.test_chain import ANNOTATION, renumber, rewrite
from tests.ledger.test_signatures import append_unchecked
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


def edit(root: Path, rel: str) -> None:
    """Add a blank to the end of one file of a corpus copy.

    Parameters
    ----------
    root : Path
        Corpus copy.
    rel : str
        File path relative to the copy.
    """
    path = root / rel
    path.write_text(path.read_text() + " ", "utf-8")


def pin(root: Path, scope: list[str]) -> dict[str, Any]:
    """Append an annotation that pins a scope as it is now.

    Parameters
    ----------
    root : Path
        Corpus copy.
    scope : list[str]
        Scope paths.

    Returns
    -------
    dict[str, Any]
        The entry as written.
    """
    return append(
        root,
        {
            **ANNOTATION,
            "scope": scope,
            "corpus_hash": corpus_hash(root, scope),
        },
    )


class Pins(unittest.TestCase):
    """A pin holds until the next transaction of its scope (unit 0016)."""

    def assert_refused(self, root: Path, scope: list[str], seq: int) -> None:
        """Assert that recording a scope is refused, the tree unchanged.

        Parameters
        ----------
        root : Path
            Corpus copy, edited.
        scope : list[str]
            Scope of the transaction.
        seq : int
            Entry whose pin the refusal must name.
        """
        change = Change(
            kind="annotate",
            actor="The Custodian",
            role="custodians",
            at="2026-10-25T00:00:00+00:00",
            authority=[],
            targets=[],
            scope=scope,
            rationale="Test.",
        )
        before = tree_digests(root)
        with self.assertRaisesRegex(
            ValueError, f"entry {seq} pins the scope .*record the change"
        ):
            record_transaction(root, change)
        self.assertEqual(tree_digests(root), before)

    def test_wider_scope_after_narrower(self) -> None:
        """Behavior: a scope that covers an older pin of another scope
        is refused before any write, naming that pin; the change is
        recorded with the older scope, and the corpus verifies.

        Reference: STND/DFLT edited, then recorded with STND/PY, then
        under STND. QA.8 part B, M4: the append went in, and the older
        pin of STND/DFLT alone went stale, as STND.HARN.9 reads.
        """
        with corpus_copy() as root:
            seq = max(
                e["seq"]
                for e in read_ledger(root)
                if e.get("scope") == ["STND/DFLT"]
            )
            edit(root, "STND/DFLT/1.md")
            self.assert_refused(root, ["STND/DFLT", "STND/PY"], seq)
            self.assert_refused(root, ["STND"], seq)
            pin(root, ["STND/DFLT"])
            self.assertEqual(problems(root), [])

    def test_narrower_scope_after_wider(self) -> None:
        """Behavior: a scope that covers part of an older pin of another
        scope is refused before any write, naming that pin.

        Reference: STND/DFLT and STND/PY pinned together by a line
        chained by hand, as before this unit an append could write it;
        STND/DFLT edited, then recorded alone, the converse case of M4.
        Its record with the wider scope is refused too, since the pins
        of STND/DFLT and STND/PY alone share its content: two scopes
        over the same files leave no transaction that records a change
        of them, which is why ``append`` refuses a scope that shares
        content with another at all.
        """
        with corpus_copy() as root:
            scope = ["STND/DFLT", "STND/PY"]
            append_unchecked(
                root,
                {
                    **ANNOTATION,
                    "scope": scope,
                    "corpus_hash": corpus_hash(root, scope),
                },
            )
            wide = len(read_ledger(root))
            self.assertEqual(problems(root), [])
            edit(root, "STND/DFLT/1.md")
            self.assert_refused(root, ["STND/DFLT"], wide)
            narrow = max(
                e["seq"]
                for e in read_ledger(root)
                if e.get("scope") == ["STND/DFLT"]
            )
            self.assert_refused(root, scope, narrow)

    def test_scope_under_and_over_a_pin(self) -> None:
        """Behavior: a scope strictly under a pin of another scope, and
        one strictly over it, are each refused before any write, naming
        that pin.

        Reference: the live pin of HW and a new scope HW/CPU; then a
        pin of HW/CPU chained by hand and a new scope HW. Review of unit
        0016, M-B: testing one direction only let the other drop.
        """
        with corpus_copy() as root:
            seq = max(
                e["seq"] for e in read_ledger(root) if e.get("scope") == ["HW"]
            )
            self.assert_refused(root, ["HW/CPU"], seq)
        with corpus_copy() as root:
            append_unchecked(
                root,
                {
                    **ANNOTATION,
                    "scope": ["HW/CPU"],
                    "corpus_hash": corpus_hash(root, ["HW/CPU"]),
                },
            )
            self.assert_refused(root, ["HW"], len(read_ledger(root)))

    def test_letter_of_the_content_pin(self) -> None:
        """Behavior: the latest pin of each scope is compared, even
        where a later transaction of another scope covers its files.

        Reference: STND/DFLT edited, then pinned with STND/PY by a line
        chained by hand. STND.HARN.9 fails "the latest governance-ledger
        transaction with that scope", here the pin of STND/DFLT alone.
        """
        with corpus_copy() as root:
            edit(root, "STND/DFLT/1.md")
            scope = ["STND/DFLT", "STND/PY"]
            append_unchecked(
                root,
                {
                    **ANNOTATION,
                    "scope": scope,
                    "corpus_hash": corpus_hash(root, scope),
                },
            )
            found = problems(root)
            self.assertEqual(len(found), 1)
            self.assertRegex(
                found[0],
                r"content changed outside the ledger since seq "
                r"\d+: STND/DFLT$",
            )

    def test_latest_pins(self) -> None:
        """Behavior: the latest entry of each scope, the paths in any
        order, is kept, in ledger order.

        Reference: hand-built entries over STND, STND/DFLT, STND/PY,
        and STND/CXX.
        """
        entries = [
            {"seq": 1, "scope": ["STND/DFLT"]},
            {"seq": 2, "scope": ["STND/PY", "STND/CXX"]},
            {"seq": 3, "scope": []},
            {"seq": 4, "scope": ["STND/CXX", "STND/PY"]},
            {"seq": 5, "scope": ["STND"]},
            {"seq": 6, "scope": ["STND/DFLT"]},
        ]
        self.assertEqual([e["seq"] for e in latest_pins(entries)], [4, 5, 6])
        self.assertEqual([e["seq"] for e in latest_pins(entries[:3])], [1, 2])

    def test_scope_without_corpus_hash(self) -> None:
        """Behavior: an entry with a scope and no ``corpus_hash`` is a
        failure line, not a traceback.

        Reference: the last entry given the scope STND/DFLT and its
        ``corpus_hash`` removed, the chain rebuilt (QA.8 part B, L1).
        """
        with corpus_copy() as root:
            pin(root, ["STND/DFLT"])

            def unhash(entries: list[dict[str, Any]]) -> None:
                """Drop the last entry's pin and rehash it.

                Parameters
                ----------
                entries : list[dict[str, Any]]
                    Ledger entries; changed in place.
                """
                del entries[-1]["corpus_hash"]
                entries[-1]["hash"] = ledger_entry_hash(entries[-1])

            rewrite(root, unhash)
            self.assertEqual(
                problems(root),
                [f"seq {len(read_ledger(root))}: a scope with no corpus_hash"],
            )

    def test_control_character_in_a_name(self) -> None:
        """Behavior: a file name with a control character under a pinned
        scope fails the check and is refused by ``corpus_hash``.

        Reference: QA.8 part B, M5: ``D/a.md:<digest of a>`` and
        ``D/b.md`` joined by a line feed in one file name hashed as the
        two files. The encoding is kept, so that every recorded pin
        stays valid, and such a name is refused instead: a line feed,
        and a tab, since the rule takes every control character.
        """
        for name in ("a\nb.md", "a\tb.md"):
            with self.subTest(repr(name)), corpus_copy() as root:
                (root / "STND" / "DFLT" / name).write_text("x", "utf-8")
                self.assertIn("control character", "\n".join(problems(root)))
                with self.assertRaisesRegex(ValueError, "control character"):
                    corpus_hash(root, ["STND/DFLT"])


class TrustedConfiguration(unittest.TestCase):
    """The signer configuration is trusted over the corpus (unit 0016)."""

    def test_anchor_without_register(self) -> None:
        """Behavior: where the configuration names an anchor and the
        corpus has no SIGNR, the check fails.

        Reference: the live corpus, which has no SIGNR, with an anchor
        of 40 hex digits. QA.8 part B, H2: a ledger rewritten without
        its signatures, once SIGNR was removed, passed.
        """
        with corpus_copy() as root:
            anchored = SignerConfig(anchor="C" * 40)
            found = ledger_problems(
                read_tree(root), read_ledger(root), anchored
            )
            self.assertEqual(
                found,
                [
                    (
                        "the signer configuration names an anchor key, but "
                        "the corpus holds no SIGNR"
                    )
                ],
            )

    def test_head_pin(self) -> None:
        """Behavior: the ledger must hold the entry the head pin names:
        cut or rewritten, it fails; a later entry does not.

        Reference: the head pinned at the last live entry; that entry
        cut, then rewritten with its links rebuilt; one entry appended
        after it; and malformed pins. QA.8 part B, H3: any prefix of
        the chain passed.
        """
        with corpus_copy() as root:
            last = read_ledger(root)[-1]
            config = SignerConfig(
                head={"seq": last["seq"], "hash": last["hash"]}
            )
            tree = read_tree(root)
            self.assertEqual(
                ledger_problems(tree, read_ledger(root), config), []
            )
            append(root, dict(ANNOTATION))
            self.assertEqual(
                ledger_problems(tree, read_ledger(root), config), []
            )
            cut = read_ledger(root)[:-2]
            self.assertIn(
                "entries were cut",
                "\n".join(ledger_problems(tree, cut, config)),
            )

            def alter(entries: list[dict[str, Any]]) -> None:
                """Change the pinned entry and rebuild every hash after it.

                Parameters
                ----------
                entries : list[dict[str, Any]]
                    Ledger entries; changed in place.
                """
                entries[last["seq"] - 1]["rationale"] += " altered"
                previous = entries[last["seq"] - 2]["hash"]
                for entry in entries[last["seq"] - 1 :]:
                    entry["prev"] = previous
                    entry["hash"] = ledger_entry_hash(entry)
                    previous = entry["hash"]

            rewrite(root, alter)
            self.assertEqual(
                ledger_problems(tree, read_ledger(root), SignerConfig()), []
            )
            self.assertIn(
                "was rewritten",
                "\n".join(ledger_problems(tree, read_ledger(root), config)),
            )
            for head in (
                {"seq": "1", "hash": "h"},
                {"seq": True, "hash": "h"},
                {"seq": 0, "hash": "h"},
                {"seq": 1},
                [1, "h"],
            ):
                with self.subTest(head):
                    self.assertIn(
                        "head pin is malformed",
                        "\n".join(
                            ledger_problems(
                                tree,
                                read_ledger(root),
                                SignerConfig(head=head),
                            )
                        ),
                    )

    def test_missing_ledger(self) -> None:
        """Behavior: a missing or empty ledger fails where the corpus
        holds content to pin, and ``verify`` exits 1.

        Reference: a copy with ``ledger.jsonl`` removed, then empty.
        QA.8 part B, H3: ``verify --no-logic`` passed every check.
        """
        with corpus_copy() as root:
            self.assertIn(
                "the ledger is missing or empty",
                "\n".join(
                    ledger_problems(read_tree(root), [], SignerConfig())
                ),
            )
            for text in (None, ""):
                with self.subTest(text):
                    path = root / "ledger.jsonl"
                    if text is None:
                        path.unlink(missing_ok=True)
                    else:
                        path.write_text(text, "utf-8")
                    out = io.StringIO()
                    with contextlib.redirect_stdout(out):
                        code = main(["verify", "--no-logic", str(root)])
                    self.assertEqual(code, 1)
                    self.assertIn("ledger: FAIL (1)", out.getvalue())


if __name__ == "__main__":
    unittest.main()
