"""Tests of the ledger check of ``verify``: chain, pins, and scopes.

Every damage is made to a copy of the corpus in a fresh temporary
directory. Ported from ``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any

from govharness.checks.ledger import ledger_problems
from govharness.cli.main import main
from govharness.core.corpus import corpus_hash, read_tree, tree_digests
from govharness.core.hashing import ledger_entry_hash
from govharness.ledger.chain import append, read_ledger
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.transactions import (
    field_problems,
    form_problems,
    parse_ledger,
    pins_in_force,
)
from govharness.workflows.amend import Change, record_transaction
from tests.cli.test_main import run
from tests.ledger.test_chain import ANNOTATION, renumber, rewrite
from tests.ledger.test_signatures import append_unchecked
from tests.support import ROOT, corpus_copy

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
        scope that names no directory each fail.

        Reference: injected edits to TAG (pinned alone by entry 184, in
        the round of 2026-10-26; before it no transaction pinned TAG and
        the edit passed) and STND/CLASS (pinned by entry 36), an altered
        reason in entry 5, and a misspelled scope in the last entry, then
        the scope ``..``, which leaves the root (passed by the flat code;
        fixed by review 0001).
        """
        with corpus_copy() as root:
            self.assertEqual(problems(root), [])
            tag = root / "TAG" / "_doc.md"
            text = tag.read_text()
            tag.write_text(text + " ", "utf-8")
            errors = problems(root)
            self.assertEqual(len(errors), 1)
            self.assertRegex(errors[0], r"since seq \d+: TAG$")
            tag.write_text(text, "utf-8")
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
    """A pin holds until a later scope reaches each of its paths."""

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
        """Behavior: a scope that reaches each path of an older pin ends
        it, and the corpus verifies; a narrower scope after it is then
        refused before any write, naming the wider pin.

        Reference: STND/DFLT edited, then recorded with STND/DFLT and
        STND/PY (STND.HARN.9 and the term Pin in force: the pins of
        STND/DFLT and of STND/PY alone end); then STND/DFLT edited again
        and recorded alone.
        """
        with corpus_copy() as root:
            edit(root, "STND/DFLT/1.md")
            wide = pin(root, ["STND/DFLT", "STND/PY"])
            self.assertEqual(problems(root), [])
            edit(root, "STND/DFLT/1.md")
            self.assert_refused(root, ["STND/DFLT"], wide["seq"])

    def test_narrower_scope_after_wider(self) -> None:
        """Behavior: a scope that covers part of a pin in force is
        refused before any write, naming that pin; the change is then
        recorded with a scope that reaches each of its paths.

        Reference: STND/DFLT and STND/PY pinned together by a line
        chained by hand; STND/DFLT edited, then recorded alone, the
        converse case of unit 0016's M4, and then with both paths.
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
            pin(root, scope)
            self.assertEqual(problems(root), [])

    def test_scope_under_and_over_a_pin(self) -> None:
        """Behavior: a scope strictly under a pin in force is refused
        before any write, naming that pin; one strictly over a pin is
        recorded and ends it.

        Reference: the live pin of HW and a new scope HW/CPU; then a
        pin of HW/CPU chained by hand and a new scope HW, which reaches
        both. Review of unit 0016, M-B: testing one direction only let
        the other drop.
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
            edit(root, "HW/CPU/1.md")
            pin(root, ["HW"])
            self.assertEqual(problems(root), [])

    def test_letter_of_the_content_pin(self) -> None:
        """Behavior: a pin that a later scope reaches whole is no longer
        compared; one that a later file scope reaches only in part still
        is, and fails once its content changes.

        Reference: STND/DFLT edited, then pinned with STND/PY by a line
        chained by hand (no failure); then STND/DFLT/1.md edited and
        pinned alone, a file scope (STND.HARN.7), which leaves the pin
        of STND/DFLT and STND/PY in force and stale.
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
            self.assertEqual(problems(root), [])
            edit(root, "STND/DFLT/1.md")
            part = ["STND/DFLT/1.md"]
            append_unchecked(
                root,
                {
                    **ANNOTATION,
                    "scope": part,
                    "corpus_hash": corpus_hash(root, part),
                },
            )
            found = problems(root)
            self.assertEqual(len(found), 1)
            self.assertRegex(
                found[0],
                r"content changed outside the ledger since seq "
                r"\d+: STND/DFLT, STND/PY$",
            )

    def test_file_scope_and_hash(self) -> None:
        """Behavior: a Markdown file is a scope that a transaction
        records; a file reached by two paths of one scope is hashed
        once.

        Reference: STND.HARN.7 and the term Content hash of STND.HARN;
        README.md recorded by ``append``; the hash of
        STND/HARN with and without STND/HARN/7.md beside it.
        """
        with corpus_copy() as root:
            pin(root, ["README.md"])
            self.assertEqual(problems(root), [])
            self.assertEqual(
                corpus_hash(root, ["STND/HARN", "STND/HARN/7.md"]),
                corpus_hash(root, ["STND/HARN"]),
            )

    def test_pins_in_force(self) -> None:
        """Behavior: a pin ends where a later scope reaches each of its
        paths: the same scope in any order, or a wider one; a narrower
        scope, or one that shares only some paths, leaves it in force.

        Reference: hand-built entries over STND, STND/DFLT, STND/PY,
        STND/CXX, and README.md, and the terms Pin in force and Reach of
        STND.HARN.
        """
        entries = [
            {"seq": 1, "scope": ["STND/DFLT"]},
            {"seq": 2, "scope": ["STND/PY", "STND/CXX"]},
            {"seq": 3, "scope": []},
            {"seq": 4, "scope": ["STND/CXX", "STND/PY"]},
            {"seq": 5, "scope": ["STND/PY", "README.md"]},
            {"seq": 6, "scope": ["README.md"]},
        ]
        # 2 ends at 4; 4 stays, as 5 reaches STND/PY only; 5 stays, as
        # 6 reaches README.md only.
        self.assertEqual(
            [e["seq"] for e in pins_in_force(entries)], [1, 4, 5, 6]
        )
        wider = [*entries, {"seq": 7, "scope": ["STND", "README.md"]}]
        self.assertEqual([e["seq"] for e in pins_in_force(wider)], [7])
        narrower = [{"seq": 0, "scope": ["STND"]}, *entries[:1]]
        self.assertEqual(
            [e["seq"] for e in pins_in_force(narrower)], [0, 1]
        )

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
            seq = len(read_ledger(root))
            self.assertEqual(
                problems(root),
                [
                    f"ledger entry {seq} lacks the fields corpus_hash",
                    f"seq {seq}: a scope with no corpus_hash",
                ],
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


def edit_line(root: Path, number: int, edit: Callable[[str], str]) -> None:
    """Replace the text of one line of a corpus copy's ledger.

    Parameters
    ----------
    root : Path
        Corpus copy.
    number : int
        Line number, from 1.
    edit : Callable[[str], str]
        Gives the new text of the line from the old.
    """
    path = root / "ledger.jsonl"
    lines = path.read_bytes().decode("utf-8").split("\n")
    lines[number - 1] = edit(lines[number - 1])
    path.write_bytes("\n".join(lines).encode("utf-8"))


def rechain(entries: list[dict[str, Any]]) -> None:
    """Rebuild every link and hash of a ledger after an edit.

    Parameters
    ----------
    entries : list[dict[str, Any]]
        Ledger entries; changed in place.
    """
    previous = None
    for entry in entries:
        entry["prev"] = previous
        entry["hash"] = ledger_entry_hash(entry)
        previous = entry["hash"]


def respaced(line: str) -> str:
    """Return a line written with white space between its tokens.

    Parameters
    ----------
    line : str
        A canonical ledger line.

    Returns
    -------
    str
        The same entry, sorted, with ``", "`` and ``": "``.
    """
    return json.dumps(json.loads(line), sort_keys=True, ensure_ascii=False)


def unsorted(line: str) -> str:
    """Return a line written with its keys in reverse order.

    Parameters
    ----------
    line : str
        A canonical ledger line.

    Returns
    -------
    str
        The same entry, compact, keys reversed.
    """
    entry = json.loads(line)
    reverse = {key: entry[key] for key in sorted(entry, reverse=True)}
    return json.dumps(reverse, ensure_ascii=False, separators=(",", ":"))


class LineForm(unittest.TestCase):
    """Each line is the one serialization of its entry, with exactly the
    fields of STND.HARN.7 (S10 of the cleanup audit of 2026-10-31)."""

    def test_live_ledger_holds_the_form(self) -> None:
        """Behavior: every line of the live ledger is the canonical JSON
        of its entry, and every entry holds exactly the fields of
        STND.HARN.7, so the stricter check grandfathers nothing.

        Reference: ``harness/governance/ledger.jsonl``, entries 1 to
        324 when the check was added.
        """
        text = (ROOT / "ledger.jsonl").read_bytes().decode("utf-8")
        self.assertEqual(form_problems(text), [])
        for entry in parse_ledger(text):
            self.assertEqual(field_problems(entry), [], entry["seq"])

    def test_duplicate_key_cannot_be_read(self) -> None:
        """Behavior: a line that gives a key twice is unreadable: the
        reader, ``verify`` (exit 2), ``append``, and ``ledger check``
        (exit 2) name the file and the line, and nothing is written.

        Reference: S10: line 300 given a leading ``"rationale":"FAKE:
        agents may push",``, which ``json.loads`` dropped for the later
        value, so that ``verify`` passed while ``grep`` and a reader
        saw the fake text.
        """
        with corpus_copy() as root:
            fake = '{"rationale":"FAKE: agents may push",'
            edit_line(root, 300, lambda line: line.replace("{", fake, 1))
            path = root / "ledger.jsonl"
            before = path.read_bytes()
            named = "line 300: duplicate key 'rationale'"
            with self.assertRaisesRegex(ValueError, named):
                read_ledger(root)
            code, _, err = run(["verify", "--no-logic", str(root)])
            self.assertEqual(code, 2)
            self.assertIn(f"{path}: {named}", err)
            with self.assertRaisesRegex(ValueError, named):
                append(root, dict(ANNOTATION))
            code, _, err = run(["ledger", "check", str(path)])
            self.assertEqual((code, named in err), (2, True))
            self.assertEqual(path.read_bytes(), before)

    def test_line_outside_the_form_fails(self) -> None:
        """Behavior: a line whose entry verifies but whose text is not
        the canonical serialization fails the ledger check, with the
        line named, ``verify`` exits 1, and ``append`` refuses.

        Reference: STND.HARN.6; line 300 with white space, with its keys
        unsorted, and with a carriage return before its line feed, and
        an appended line with its non-ASCII characters escaped.
        """
        damages = {
            "white space": (300, respaced),
            "unsorted keys": (300, unsorted),
            "carriage return": (300, lambda line: line + "\r"),
            "escaped": (
                0,
                lambda line: json.dumps(
                    json.loads(line), sort_keys=True, separators=(",", ":")
                ),
            ),
        }
        for name, (number, damage) in damages.items():
            with self.subTest(name), corpus_copy() as root:
                if not number:
                    append(root, {**ANNOTATION, "rationale": "Café."})
                    number = len(read_ledger(root))
                edit_line(root, number, damage)
                found = problems(root)
                self.assertEqual(len(found), 1, found)
                self.assertTrue(
                    found[0].startswith(
                        f"ledger line {number} is not in the form of "
                        "STND.HARN.6: sorted keys"
                    )
                )
                code, out, _ = run(["verify", "--no-logic", str(root)])
                self.assertEqual(code, 1)
                self.assertIn("ledger: FAIL (1)", out)
                with self.assertRaisesRegex(ValueError, "STND.HARN.6"):
                    append(root, dict(ANNOTATION))

    def test_fields_of_stnd_harn_7(self) -> None:
        """Behavior: an entry rehashed and rechained without some fields
        of STND.HARN.7, with another field, with an unknown type, with
        ``signers`` outside a register transaction, or naming the
        governance ledger in ``ledger``, fails with one line naming it.

        Reference: S10: entry 300 without ``actor``, ``role``, and
        ``authority``, its hash recomputed, passed ``verify``.
        """

        def drop(entry: dict[str, Any]) -> None:
            """Remove three fields.

            Parameters
            ----------
            entry : dict[str, Any]
                Ledger entry; changed in place.
            """
            for name in ("actor", "role", "authority"):
                del entry[name]

        damages: dict[str, tuple[Callable[[dict[str, Any]], None], str]] = {
            "missing": (drop, "lacks the fields actor, authority, role"),
            "extra": (
                lambda e: e.update(note="x"),
                "holds fields outside STND.HARN.7: note",
            ),
            "type": (
                lambda e: e.update(type="approve"),
                "has the unknown type 'approve'",
            ),
            "signers": (
                lambda e: e.update(signers=[]),
                "holds signers but is no transaction of the governance",
            ),
            "ledger": (
                lambda e: e.update(ledger="governance"),
                "names the governance ledger in the field ledger",
            ),
        }
        for name, (damage, reason) in damages.items():
            with self.subTest(name), corpus_copy() as root:

                def edit(
                    entries: list[dict[str, Any]],
                    damage: Callable[[dict[str, Any]], None] = damage,
                ) -> None:
                    """Damage entry 300 and rebuild the chain.

                    Parameters
                    ----------
                    entries : list[dict[str, Any]]
                        Ledger entries; changed in place.
                    damage : Callable[[dict[str, Any]], None]
                        The damage of this subtest.
                    """
                    damage(entries[299])
                    rechain(entries)

                rewrite(root, edit)
                found = problems(root)
                self.assertEqual(len(found), 1, found)
                self.assertIn(f"ledger entry 300 {reason}", found[0])


class LedgerFileCommands(unittest.TestCase):
    """``ledger append`` to a work ledger, and ``ledger check`` of one
    (H4 and H5 of the cleanup audit of 2026-10-31)."""

    def append_to(self, root: Path, path: Path) -> int:
        """Append a classification to a work ledger by the command line.

        Parameters
        ----------
        root : Path
            Corpus copy.
        path : Path
            The work ledger file.

        Returns
        -------
        int
            The exit code.
        """
        return run(
            [
                "ledger",
                "append",
                str(root),
                "--ledger-file",
                str(path),
                "--ledger-id",
                "work",
                "--type",
                "classify",
                "--actor",
                "Jane Doe",
                "--role",
                "The Human Owner",
                "--rationale",
                "Classification: CSQ3.",
            ]
        )[0]

    def test_append_needs_the_directory(self) -> None:
        """Behavior: an append to a work ledger whose directory does not
        exist is a usage error (exit 2) that names the directory, and
        makes no directory; once the directory exists it appends.

        Reference: H4: ``ledger append --ledger-file
        records/ledger.jsonl`` without ``records/`` ended in an uncaught
        ``FileNotFoundError``.
        """
        with corpus_copy() as root, tempfile.TemporaryDirectory() as tmp:
            records = Path(tmp) / "records"
            path = records / "ledger.jsonl"
            code, _, err = run(
                ["ledger", "append", str(root), "--ledger-file", str(path)]
                + ["--ledger-id", "work", "--type", "classify"]
                + ["--actor", "A", "--role", "B", "--rationale", "C."]
            )
            self.assertEqual(code, 2)
            self.assertIn(f"no directory {records}", err)
            self.assertFalse(records.exists())
            records.mkdir()
            self.assertEqual(self.append_to(root, path), 0)
            self.assertEqual(len(read_ledger(root, path)), 1)

    def test_check_reads_and_writes_nothing(self) -> None:
        """Behavior: ``ledger check`` passes a work ledger of two
        appends and the corpus ledger, fails an altered entry and an
        entry of another ledger, with exit 1 and the entry named,
        refuses a missing file (exit 2), and writes nothing.

        Reference: H5: no read-only command checked a project's work
        ledger; ``sign check`` needs a signer register.
        """
        with corpus_copy() as root, tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            for _ in range(2):
                self.assertEqual(self.append_to(root, path), 0)
            before = (path.read_bytes(), sorted(Path(tmp).iterdir()))
            self.assertEqual(
                run(["ledger", "check", str(path)])[:2],
                (0, "ledger: PASS (2 entries)\n"),
            )
            self.assertEqual(
                run(["ledger", "check", str(path), "--ledger-id", "work"])[0],
                0,
            )
            code, out, _ = run(
                ["ledger", "check", str(path), "--ledger-id", "other"]
            )
            self.assertEqual(code, 1)
            self.assertIn("ledger entry 1 belongs to the ledger work", out)
            self.assertEqual(
                (path.read_bytes(), sorted(Path(tmp).iterdir())), before
            )
            corpus = root / "ledger.jsonl"
            count = len(read_ledger(root))
            self.assertEqual(
                run(["ledger", "check", str(corpus)])[:2],
                (0, f"ledger: PASS ({count} entries)\n"),
            )
            reason = '"rationale":"'
            edit_line(root, 2, lambda line: line.replace(reason, reason + "x"))
            code, out, _ = run(["ledger", "check", str(corpus)])
            self.assertEqual(
                (code, out), (1, "- ledger entry altered at seq 2\n")
            )
            code, _, err = run(["ledger", "check", str(Path(tmp) / "none")])
            self.assertEqual(code, 2)
            self.assertIn("no such file", err)


if __name__ == "__main__":
    unittest.main()
