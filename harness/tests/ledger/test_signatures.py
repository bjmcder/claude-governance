"""Tests of ledger signatures and the signer register SIGNR.

Keys are generated in a throwaway keyring; every corpus is a copy in a
fresh temporary directory; the anchor is passed as a parameter, so the
owner's configuration under ``/etc`` is never read. Ported from
``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest import mock

from govharness.checks.ledger import ledger_problems
from govharness.cli.main import main
from govharness.core.corpus import corpus_hash, read_tree, tree_digests
from govharness.core.hashing import canonical_json, ledger_entry_hash
from govharness.ledger.chain import append, read_ledger
from govharness.ledger.gpg import SignerConfig, parse_status, read_config
from govharness.ledger.register import (
    SignerRegister,
    active_signers,
    read_register,
    skeleton,
    with_signer,
    with_signer_closed,
)
from govharness.ledger.signatures import _valid_for, check_signatures
from govharness.workflows.signers import (
    add_signer,
    close_signer,
    found_register,
    require_signature,
)
from tests.gpgkeys import keyring, make_key
from tests.support import ROOT, corpus_copy


def register_entry(root: Path, scope: str) -> dict[str, Any]:
    """Return the fields of a register transaction pinning one scope.

    Parameters
    ----------
    root : Path
        Corpus copy.
    scope : str
        Scope pinned.

    Returns
    -------
    dict[str, Any]
        Transaction fields for ``append``.
    """
    return {
        "at": "2026-10-10T00:00:00+00:00",
        "type": "register",
        "actor": "The Custodian",
        "role": "custodians",
        "authority": ["GOV.36"],
        "targets": [scope],
        "scope": [scope],
        "corpus_hash": corpus_hash(root, [scope]),
        "rationale": "Test.",
        "signature": "",
    }


def append_unchecked(root: Path, entry: dict[str, Any]) -> None:
    """Chain an entry onto the ledger by hand, past ``append``.

    An agent that can write the ledger file can add an entry that
    ``append`` refuses; ``verify`` must still see it.

    Parameters
    ----------
    root : Path
        Corpus copy.
    entry : dict[str, Any]
        Transaction fields without ``seq``, ``prev``, or ``hash``.
    """
    entries = read_ledger(root)
    chained = {"seq": len(entries) + 1, **entry, "prev": entries[-1]["hash"]}
    chained["hash"] = ledger_entry_hash(chained)
    path = root / "ledger.jsonl"
    path.write_text(path.read_text() + canonical_json(chained) + "\n")


def signed_corpus(root: Path, home: Path) -> tuple[str, str, Path]:
    """Found a signer register in a corpus copy, signed by a new key.

    Parameters
    ----------
    root : Path
        Corpus copy.
    home : Path
        Keyring directory.

    Returns
    -------
    tuple[str, str, Path]
        The owner's fingerprint, its armored key, and the register
        file. The key signs for ``The Custodian`` on the governance
        ledger and for ``The Human Owner`` on ``work-a``; two signed
        register transactions record the register.
    """
    owner, owner_key = make_key(home, "Owner")
    mnem = root / "MNEM" / "_doc.md"
    if "| SIGNR |" not in mnem.read_text():
        mnem.write_text(
            mnem.read_text().rstrip("\n")
            + "\n| SIGNR | none | Signer register | none | none "
            "| active |\n",
            "utf-8",
        )
    register = found_register(root, "2026-10-10")
    add_signer(register, "governance", "The Custodian", "O", owner_key)
    add_signer(register, "work-a", "The Human Owner", "O", owner_key)
    append(root, register_entry(root, "MNEM"), signer=(owner, home))
    append(root, register_entry(root, "SIGNR"), signer=(owner, home))
    return owner, owner_key, register


GPG = shutil.which("gpg") or "/usr/bin/gpg"
# "The Custodian" with a Cyrillic "о": NFKC keeps it, so only the rule
# that an actor is ASCII refuses it.
LOOKALIKE = "The Cust\u043edian"
CONFIG_FIELDS = {
    "anchor": "B" * 40,
    "gpg": GPG,
    "head": {"seq": 3, "hash": "h"},
}


def renumber_last(root: Path, seq: int) -> None:
    """Give the last ledger entry another number and rehash it.

    Its link stays intact, so only a check of the sequence numbers sees
    the change, and a requirement "from entry N" no longer covers it.

    Parameters
    ----------
    root : Path
        Corpus copy.
    seq : int
        Number the entry claims.
    """
    entries = read_ledger(root)
    entries[-1]["seq"] = seq
    entries[-1]["hash"] = ledger_entry_hash(entries[-1])
    text = "".join(canonical_json(e) + "\n" for e in entries)
    (root / "ledger.jsonl").write_text(text, encoding="utf-8")


class Signatures(unittest.TestCase):
    """Signing, the signer chain, required signatures, and forgery."""

    def test_ledger_signatures(self) -> None:
        """Behavior: each forgery or gap in the signer chain fails, and a
        properly signed ledger passes.

        Reference: injected defects, one per case: an intruder's
        signature, an intruder registering itself, a register edited
        outside the ledger, a missing required signature, a look-alike
        actor, an unsigned entry renumbered below the entry from which
        its actor must sign (passed by the flat code, which compared no
        sequence number with its position; fixed by review 0001), a
        register founded by a key other than the anchor, and a signature
        replayed into another ledger.
        """
        with keyring() as home, corpus_copy() as root:
            self._check_signatures(root, home)

    def _check_signatures(self, root: Path, home: Path) -> None:
        """Run the signature cases in one corpus copy.

        Parameters
        ----------
        root : Path
            Corpus copy.
        home : Path
            Keyring directory.
        """
        owner, _, register = signed_corpus(root, home)
        intruder, intruder_key = make_key(home, "Intruder")
        config = SignerConfig(owner, GPG)

        def problems(settings: SignerConfig = config) -> str:
            """Return the ledger check's failures as one text.

            Parameters
            ----------
            settings : SignerConfig
                Signer configuration.

            Returns
            -------
            str
                Failure lines joined by newlines.
            """
            return "\n".join(
                ledger_problems(read_tree(root), read_ledger(root), settings)
            )

        self.assertEqual(problems(), "")
        ledger = root / "ledger.jsonl"
        clean = ledger.read_text(), register.read_text()
        unsigned = {**register_entry(root, "MNEM"), "scope": []}
        cases: dict[str, tuple[Callable[[], object], str]] = {
            "intruder signs": (
                lambda: append(root, unsigned, signer=(intruder, home)),
                "does not verify",
            ),
            "intruder registers itself": (
                lambda: (
                    add_signer(
                        register,
                        "governance",
                        "The Custodian",
                        "I",
                        intruder_key,
                    ),
                    append(
                        root,
                        register_entry(root, "SIGNR"),
                        signer=(intruder, home),
                    ),
                ),
                "signer listed before",
            ),
            "register edited outside the ledger": (
                lambda: add_signer(
                    register, "governance", "The Custodian", "I", intruder_key
                ),
                "differ from those",
            ),
            "required signature missing": (
                lambda: (
                    require_signature(
                        register, "governance", "The Custodian", 1
                    ),
                    append(
                        root,
                        register_entry(root, "SIGNR"),
                        signer=(owner, home),
                    ),
                ),
                "must sign from entry 1",
            ),
            "actor imitates a label": (
                lambda: append(root, {**unsigned, "actor": "The Custodian "}),
                "imitates a label",
            ),
            "actor with a non-ASCII letter": (
                lambda: append(root, {**unsigned, "actor": LOOKALIKE}),
                "imitates a label",
            ),
            "signed after the key's last entry": (
                lambda: (
                    close_signer(
                        register,
                        "governance",
                        owner,
                        len(read_ledger(root)),
                    ),
                    append(root, unsigned, signer=(owner, home)),
                ),
                f"key {owner} may not sign",
            ),
            "renumbered to evade a requirement": (
                lambda: (
                    require_signature(
                        register,
                        "governance",
                        "The Custodian",
                        len(read_ledger(root)) + 2,
                    ),
                    append(
                        root,
                        register_entry(root, "SIGNR"),
                        signer=(owner, home),
                    ),
                    append_unchecked(root, unsigned),
                    renumber_last(root, 3),
                ),
                "sequence broken",
            ),
        }
        for name, (mutate, reason) in cases.items():
            with self.subTest(name):
                mutate()
                self.assertIn(reason, problems())
                ledger.write_text(clean[0], "utf-8")
                register.write_text(clean[1], "utf-8")
        with self.subTest("sign check sees a renumbered entry"):
            append(root, unsigned)
            renumber_last(root, 3)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(
                    [
                        "sign",
                        "check",
                        str(ledger),
                        "--ledger-id",
                        "governance",
                        "--corpus",
                        str(root),
                    ]
                )
            self.assertEqual(code, 1)
            self.assertIn("- ledger sequence broken at entry", out.getvalue())
            ledger.write_text(clean[0], "utf-8")

            self.assertIn(
                "anchor", problems(SignerConfig(intruder, config.gpg))
            )
        with self.subTest("signature replayed into another ledger"):
            work = root.parent / "work-a.jsonl"
            grant = {
                **unsigned,
                "actor": "The Human Owner",
                "type": "authorize",
            }
            append(root, grant, (owner, home), work, "work-a")
            parsed = read_register(register.read_text(), config.gpg)
            entries = read_ledger(root, work)
            self.assertEqual(
                check_signatures(entries, parsed, "work-a", config), []
            )
            self.assertIn(
                "belongs to work-a",
                "\n".join(check_signatures(entries, parsed, "work-b", config)),
            )
        self.assertEqual(problems(), "")

    def test_gpg_status(self) -> None:
        """Behavior: only one good, valid, unrevoked signature counts.

        Reference: hand-written ``gpg --status-fd`` outputs: a good one,
        a failed run, a revoked key, a doubled signature, unprefixed
        lines, and a malformed ``all`` requirement row.
        """
        fpr = "A" * 40
        good = (
            "[GNUPG:] GOODSIG 1 Owner\n"
            f"[GNUPG:] VALIDSIG {fpr} 2026-10-10 1 0 4 0 22 10 00 {fpr}\n"
        )
        self.assertEqual(parse_status(good, 0), fpr)
        self.assertIsNone(parse_status(good, 1))
        self.assertIsNone(parse_status(good + "[GNUPG:] REVKEYSIG 1 O\n", 0))
        self.assertIsNone(parse_status(good + good, 0))
        self.assertIsNone(parse_status(good.replace("[GNUPG:] ", ""), 0))
        text = (
            "| Ledger | Actor | From entry |\n| --- | --- | --- |\n"
            "| all | The Human Owner | 5 |\n"
        )
        self.assertIn("starts at 1", "\n".join(read_register(text).problems))


class SignCheckCommand(unittest.TestCase):
    """``sign check`` on a corpus that has no signer register."""

    def test_no_register_is_a_failure_not_a_traceback(self) -> None:
        """Behavior: ``sign check`` prints that the corpus has no signer
        register and exits 1.

        Reference: the live corpus, which has no ``SIGNR``; the flat
        code ended here in ``FileNotFoundError`` (defect 3 of unit 0001,
        fixed by review 0001). Nothing is written.
        """
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(
                [
                    "sign",
                    "check",
                    str(ROOT / "ledger.jsonl"),
                    "--ledger-id",
                    "governance",
                    "--corpus",
                    str(ROOT),
                ]
            )
        self.assertEqual(code, 1)
        self.assertEqual(
            out.getvalue(),
            "- no signer register SIGNR/_doc.md in the corpus\n",
        )


class SignCheckWithoutLedger(unittest.TestCase):
    """``sign check`` on a corpus with a register and no ledger file."""

    def test_missing_ledger_is_a_failure_line(self) -> None:
        """Behavior: ``sign check`` exits 1 with a failure line, not a
        traceback, when the corpus holds a register and no ledger.

        Reference: a copy with a skeleton SIGNR and ``ledger.jsonl``
        removed. Review of unit 0016, M-B: reading the file with
        ``read_ledger_file`` again, which raises ``FileNotFoundError``,
        passed every test.
        """
        with corpus_copy() as root:
            found_register(root, "2026-10-10")
            (root / "ledger.jsonl").unlink()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(
                    [
                        "sign",
                        "check",
                        str(root / "ledger.jsonl"),
                        "--ledger-id",
                        "governance",
                        "--corpus",
                        str(root),
                    ]
                )
            self.assertEqual(code, 1)
            self.assertEqual(
                out.getvalue(), "- SIGNR is not founded by a transaction\n"
            )


class SignerRows(unittest.TestCase):
    """Which register rows let a key sign an entry (unit 0016)."""

    KEY = "A" * 40

    def register(self, *rows: tuple[str, str]) -> SignerRegister:
        """Return a register of rows for one key and ``The Custodian``.

        Parameters
        ----------
        *rows : tuple[str, str]
            Ledger and last entry of each row.

        Returns
        -------
        SignerRegister
            The register; no key is checked.
        """
        return SignerRegister(
            signers=[
                {
                    "Ledger": ledger,
                    "Role label": "The Custodian",
                    "Name": "O",
                    "Fingerprint": self.KEY,
                    "Last entry": last,
                }
                for ledger, last in rows
            ]
        )

    def valid(self, register: SignerRegister, seq: int, ledger: str) -> bool:
        """Return whether the key may sign entry ``seq`` of a ledger.

        Parameters
        ----------
        register : SignerRegister
            The register.
        seq : int
            Sequence number of the entry.
        ledger : str
            Ledger identifier.

        Returns
        -------
        bool
            The verdict of ``_valid_for``.
        """
        entry = {"actor": "The Custodian", "seq": seq}
        return _valid_for(register, self.KEY, entry, ledger)

    def test_key_window(self) -> None:
        """Behavior: a closed key signs up to its last entry, not after.

        Reference: one governance row closed at 5; entries 5 and 6, and
        an open row. QA.8 part B, M6: deleting the window clause of
        ``_valid_for`` passed every test.
        """
        closed = self.register(("governance", "5"))
        self.assertTrue(self.valid(closed, 5, "governance"))
        self.assertFalse(self.valid(closed, 6, "governance"))
        self.assertTrue(
            self.valid(self.register(("governance", "none")), 6, "governance")
        )

    def test_signer_row_names_its_ledger(self) -> None:
        """Behavior: a signer row accepts its key on its own ledger
        only, and a row closed on one ledger leaves the key open only
        where another row of it is open, as the term Accepted signature
        of STND.HARN reads.

        Reference: rows ``governance | 5`` and ``work-a | none``; QA.8
        part B, M1, where a closing row of one ledger seemed to retire
        a key that an ``all`` row kept open.
        """
        register = self.register(("governance", "5"), ("work-a", "none"))
        self.assertTrue(self.valid(register, 5, "governance"))
        self.assertFalse(self.valid(register, 10, "governance"))
        self.assertTrue(self.valid(register, 10, "work-a"))
        self.assertFalse(self.valid(register, 1, "work-b"))
        self.assertEqual(active_signers(register), [])
        self.assertEqual(
            active_signers(self.register(("governance", "none"))), [self.KEY]
        )

    def test_no_signer_row_for_all(self) -> None:
        """Behavior: a signer row for ``all`` is a register problem and
        accepts nothing; the helpers refuse to add or close one, citing
        STND.HARN.10, and a key registered on each of two ledgers closes
        on one and stays open on the other.

        Reference: a skeleton register with one key; an ``all`` row
        written by hand, as the helpers wrote it before unit 0021.
        """
        everywhere = self.register(("all", "none"))
        self.assertFalse(self.valid(everywhere, 1, "governance"))
        self.assertEqual(active_signers(everywhere), [])
        hand = (
            "| Ledger | Role label | Name | Fingerprint | Last entry |\n"
            "| --- | --- | --- | --- | --- |\n"
            f"| all | The Custodian | O | {self.KEY} | none |\n"
        )
        self.assertIn(
            "names one ledger (STND.HARN.10)",
            "\n".join(read_register(hand).problems),
        )
        text = skeleton("2026-10-10")
        with self.assertRaisesRegex(ValueError, "STND.HARN.10"):
            with_signer(text, "all", "The Custodian", "O", "KEY", self.KEY)
        with self.assertRaisesRegex(ValueError, "no open row"):
            with_signer_closed(text, "all", self.KEY, 5)
        armored = (
            "-----BEGIN PGP PUBLIC KEY BLOCK-----\nx\n"
            "-----END PGP PUBLIC KEY BLOCK-----"
        )
        both = text
        for ledger in ("governance", "work-a"):
            both = with_signer(
                both, ledger, "The Custodian", "O", armored, self.KEY
            )
        self.assertEqual(both.count(f"### {self.KEY}"), 1)
        closed = with_signer_closed(both, "governance", self.KEY, 5)
        row = f"| The Custodian | O | {self.KEY} |"
        self.assertIn(f"| governance {row} 5 |", closed)
        self.assertIn(f"| work-a {row} none |", closed)


class SignerConfigFile(unittest.TestCase):
    """``read_config`` trusts only a file the account cannot alter."""

    def test_alterable_file_is_ignored(self) -> None:
        """Behavior: a configuration the running user can write gives
        no anchor and no head pin, names the file as ignored, and the
        ledger check reports it; a missing file is not reported.

        Reference: a file in a fresh temporary directory, which the
        user owns. QA.8 part B, M6: removing the ``unalterable`` gate
        passed every test, since every caller patches ``read_config``.
        Review of unit 0016, L-b: the head pin was dropped without a
        word.
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signer.json"
            self.assertEqual(read_config(path), SignerConfig())
            path.write_text(json.dumps(CONFIG_FIELDS), encoding="utf-8")
            config = read_config(path)
            self.assertEqual(config, SignerConfig(ignored=str(path)))
            found = ledger_problems(read_tree(ROOT), read_ledger(ROOT), config)
            self.assertEqual(
                found,
                [
                    (
                        f"the signer configuration {path} can be altered "
                        "by this account, so its anchor and head pin are "
                        "ignored"
                    )
                ],
            )

    def test_unalterable_file_is_read(self) -> None:
        """Behavior: from a file the user cannot alter, the anchor, the
        ``gpg`` path, and the head pin are read as given.

        Reference: the same file with ``unalterable`` patched to hold,
        standing for a file under ``/etc`` that only root writes.
        """
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch("govharness.ledger.gpg.unalterable", return_value=True),
        ):
            path = Path(tmp) / "signer.json"
            path.write_text(json.dumps(CONFIG_FIELDS), encoding="utf-8")
            self.assertEqual(
                read_config(path),
                SignerConfig("B" * 40, GPG, {"seq": 3, "hash": "h"}),
            )


class Refusals(unittest.TestCase):
    """``append`` refuses an entry that would fail ``verify`` for good."""

    def test_unsigned_entry_the_register_requires(self) -> None:
        """Behavior: an unsigned entry that the register requires to be
        signed is refused, naming ``ledger append --sign``, and nothing
        is written; signed, it is appended and the ledger verifies.

        Reference: a register that requires ``The Custodian`` from the
        entry after its own transaction. QA.8 part B, M3: the entry
        went in and the corpus never verified again.
        """
        with keyring() as home, corpus_copy() as root:
            owner, _, register = signed_corpus(root, home)
            seq = len(read_ledger(root)) + 2
            require_signature(register, "governance", "The Custodian", seq)
            append(root, register_entry(root, "SIGNR"), signer=(owner, home))
            note = {**register_entry(root, "MNEM"), "scope": []}
            before = tree_digests(root)
            with self.assertRaisesRegex(ValueError, "ledger append --sign"):
                append(root, note)
            self.assertEqual(tree_digests(root), before)
            append(root, note, signer=(owner, home))
            self.assertEqual(
                ledger_problems(
                    read_tree(root),
                    read_ledger(root),
                    SignerConfig(owner, GPG),
                ),
                [],
            )

    def test_unsigned_register_change(self) -> None:
        """Behavior: an unsigned transaction of the register is refused,
        naming ``ledger append --sign``, and nothing is written; signed
        by a listed key, it is appended and the ledger verifies.

        Reference: review of unit 0016, M-A (``p/m3.py``): a second
        signer added, then the register recorded unsigned; the entry
        went in and failed "changes SIGNR without the signature of a
        signer listed before the change" for good.
        """
        with keyring() as home, corpus_copy() as root:
            owner, _, register = signed_corpus(root, home)
            _, other_key = make_key(home, "Other")
            add_signer(register, "governance", "The Steward", "S", other_key)
            before = tree_digests(root)
            with self.assertRaisesRegex(
                ValueError, "SIGNR must be signed.*ledger append --sign"
            ):
                append(root, register_entry(root, "SIGNR"))
            self.assertEqual(tree_digests(root), before)
            append(root, register_entry(root, "SIGNR"), signer=(owner, home))
            self.assertEqual(
                ledger_problems(
                    read_tree(root),
                    read_ledger(root),
                    SignerConfig(owner, GPG),
                ),
                [],
            )

    def test_register_with_problems(self) -> None:
        """Behavior: a transaction that records a register with problems
        is refused, and nothing is written.

        Reference: a requirement row whose first entry is not a number.
        QA.8 part B, M3: ``_chained`` listed the signers and ignored the
        problems.
        """
        with keyring() as home, corpus_copy() as root:
            owner, _, register = signed_corpus(root, home)
            text = register.read_text()
            register.write_text(
                text.replace(
                    "| Ledger | Actor | From entry |\n| --- | --- | --- |\n",
                    "| Ledger | Actor | From entry |\n| --- | --- | --- |\n"
                    "| governance | The Custodian | soon |\n",
                ),
                encoding="utf-8",
            )
            before = tree_digests(root)
            with self.assertRaisesRegex(ValueError, "SIGNR has problems"):
                append(
                    root, register_entry(root, "SIGNR"), signer=(owner, home)
                )
            self.assertEqual(tree_digests(root), before)


class SignCheckHead(unittest.TestCase):
    """``sign check`` compares the head pin of the configuration."""

    def test_cut_entry_fails(self) -> None:
        """Behavior: with the head pinned at the last entry, ``sign
        check`` passes; with that entry cut, it exits 1 and says so.

        Reference: a signed corpus with one unsigned annotation last,
        the kind of entry (empty scope) that QA.8 part B, H3, cut from
        the end with ``verify`` passing.
        """
        with keyring() as home, corpus_copy() as root:
            owner, _, _ = signed_corpus(root, home)
            note = {**register_entry(root, "MNEM"), "scope": []}
            last = append(root, note)
            head = {"seq": last["seq"], "hash": last["hash"]}
            ledger = root / "ledger.jsonl"
            with mock.patch(
                "govharness.cli.records.read_config",
                return_value=SignerConfig(owner, GPG, head),
            ):
                code, out = self.sign_check(root)
                self.assertEqual((code, out), (0, "signatures: PASS\n"))
                lines = ledger.read_text().splitlines(keepends=True)
                ledger.write_text("".join(lines[:-1]), encoding="utf-8")
                code, out = self.sign_check(root)
            self.assertEqual(code, 1)
            self.assertIn("entries were cut", out)

    @staticmethod
    def sign_check(root: Path) -> tuple[int, str]:
        """Run ``sign check`` on the corpus ledger of a copy.

        Parameters
        ----------
        root : Path
            Corpus copy.

        Returns
        -------
        tuple[int, str]
            Exit code and standard output.
        """
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(
                [
                    "sign",
                    "check",
                    str(root / "ledger.jsonl"),
                    "--ledger-id",
                    "governance",
                    "--corpus",
                    str(root),
                ]
            )
        return code, out.getvalue()


if __name__ == "__main__":
    unittest.main()
