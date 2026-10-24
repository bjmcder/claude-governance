"""Tests of ledger signatures and the signer register SIGNR.

Keys are generated in a throwaway keyring; every corpus is a copy in a
fresh temporary directory; the anchor is passed as a parameter, so the
owner's configuration under ``/etc`` is never read. Ported from
``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import contextlib
import io
import shutil
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any

from govharness.checks.ledger import ledger_problems
from govharness.cli.main import main
from govharness.core.corpus import corpus_hash, read_tree
from govharness.core.hashing import canonical_json, ledger_entry_hash
from govharness.ledger.chain import append, read_ledger
from govharness.ledger.gpg import SignerConfig, parse_status
from govharness.ledger.register import read_register
from govharness.ledger.signatures import check_signatures
from govharness.workflows.signers import (
    add_signer,
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
        owner, owner_key = make_key(home, "Owner")
        intruder, intruder_key = make_key(home, "Intruder")
        config = SignerConfig(owner, shutil.which("gpg") or "/usr/bin/gpg")
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
                    append(root, unsigned),
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


if __name__ == "__main__":
    unittest.main()
