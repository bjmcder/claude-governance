"""Tests of the authorizations a derivation honors (unit 0008).

The reference is STND.PROJ.6 and STND.PROJ.7 (the form of an
authorization of a remote write, and its kinds), STND.HARN.29 (when a
derived configuration relies on one), and GUARD.11 (an irrevocable
remote write only per action). Each test writes an authorization file
and a ledger into a temporary corpus root, so no test reads or writes
the live corpus. Agreement is exact: the writes returned, or the reason
an authorization is not in force, are the ones stated.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from govharness.cli.main import main
from govharness.core.corpus import Corpus, corpus_hash, read_corpus, read_tree
from govharness.derive.environment import claude_code
from govharness.derive.environment.authorizations import read_authorizations
from govharness.derive.environment.inputs import Inputs, RemoteWrite
from govharness.ledger.chain import append, read_ledger
from govharness.ledger.transactions import parse_ledger
from tests.support import corpus_copy, live_entries

NOW = datetime(2026, 10, 24, 12, 0, tzinfo=timezone.utc)
REPO = "https://git.example.org/team/work.git"
IDENT = "WORK.AUTH.1"
ENTRY = {
    "destination": REPO,
    "kinds": ["commit"],
    "branches": ["main"],
    "provisioned": True,
}
FIELDS = {
    "id": IDENT,
    "level": "LVL3",
    "kind": "auth",
    "title": "Commits to the work repository",
    "status": "adopted",
    "recorded": "2026-10-20",
    "grantor": "The Human Owner",
    "action_class": "Adding commits to a private remote repository",
    "scope": "Branch main of the work repository",
    "items_or_volume": "",
    "standing": True,
    "expires": "2027-01-01T00:00:00+00:00",
    "delegable_to": ["Implementing agent"],
    "spending_envelope": "",
    "remote_writes": [ENTRY],
}


def write_authorization(root: Path, **fields: object) -> None:
    """Write ``WORK/AUTH/1.md`` with the fields given over ``FIELDS``.

    Parameters
    ----------
    root : Path
        Corpus root.
    **fields : object
        Fields that replace those of ``FIELDS``.
    """
    meta = {**FIELDS, **fields}
    lines = ["---", *(f"{k}: {json.dumps(v)}" for k, v in meta.items())]
    folder = root / "WORK" / "AUTH"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "1.md").write_text(
        "\n".join([*lines, "---", "", "Purpose.", ""]), encoding="utf-8"
    )


def record(root: Path, kind: str = "authorize", **fields: object) -> None:
    """Append the transaction that pins the authorization.

    Parameters
    ----------
    root : Path
        Corpus root.
    kind : str
        Transaction type.
    **fields : object
        Fields that replace those of the human owner's transaction.
    """
    entry = {
        "at": "2026-10-20T10:00:00+00:00",
        "type": kind,
        "actor": "The Human Owner",
        "role": "human owner",
        "authority": ["GUARD.10"],
        "targets": [IDENT],
        "scope": ["WORK/AUTH"],
        "rationale": "Grant.",
        "signature": "",
    }
    entry.update(fields)
    scope = list(entry["scope"])
    entry["corpus_hash"] = corpus_hash(root, scope) if scope else None
    append(root, entry)


def reading(
    root: Path, assured: bool = False, verified: bool = False
) -> tuple[tuple[RemoteWrite, ...], tuple[str, ...]]:
    """Read the authorization of a root at ``NOW``.

    Parameters
    ----------
    root : Path
        Corpus root.
    assured : bool
        Whether the work is assured.
    verified : bool
        Whether the ledger's signatures verify.

    Returns
    -------
    tuple[tuple[RemoteWrite, ...], tuple[str, ...]]
        The writes opened and the lines still referred.
    """
    return read_authorizations(
        read_corpus(root),
        read_tree(root),
        read_ledger(root),
        (IDENT,),
        NOW,
        assured,
        verified,
    )


class InForce(unittest.TestCase):
    """STND.HARN.29: an authorization relied on is in force."""

    def setUp(self) -> None:
        """Make an empty corpus root."""
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_granted_standing_authorization(self) -> None:
        """Behavior: an adopted, recorded, unexpired standing
        authorization opens its commit to its branch.

        Reference: STND.HARN.29; STND.PROJ.6.
        """
        write_authorization(self.root)
        record(self.root)
        writes, referred = reading(self.root)
        self.assertEqual(
            writes,
            (RemoteWrite(IDENT, "commit", REPO, ("main",), FIELDS["expires"]),),
        )
        self.assertEqual(referred, ())

    def test_fields_not_in_force(self) -> None:
        """Behavior: a draft or retired file, another grantor, a record
        date after the derivation, an expiry passed or without offset,
        and a standing field that is no boolean each stop the derivation
        with the reason.

        Reference: STND.HARN.29, the rows on status, grantor, and dates.
        """
        for fields, reason in (
            ({"status": "draft"}, "status 'draft'"),
            ({"status": "retired"}, "status 'retired'"),
            ({"grantor": "Implementing agent"}, "grantor"),
            ({"recorded": "2026-11-01"}, "after the derivation"),
            ({"recorded": ""}, "is no date"),
            ({"expires": "2026-10-24T11:59:59+00:00"}, "expired"),
            ({"expires": "2027-01-01T00:00:00"}, "no UTC offset"),
            ({"expires": ""}, "no timestamp"),
            ({"standing": "yes"}, "standing is no boolean"),
            ({"remote_writes": []}, "names no destination"),
        ):
            with self.subTest(fields=fields):
                root = self.root / str(len(list(self.root.iterdir())))
                root.mkdir()
                write_authorization(root, **fields)
                record(root)
                with self.assertRaisesRegex(ValueError, reason):
                    reading(root)

    def test_irrevocable_standing(self) -> None:
        """Behavior: a standing authorization of publication or
        transmission, or naming a destination not recorded as
        provisioned, is not in force; the same per action is, and stays
        referred.

        Reference: GUARD.11: an irrevocable remote write is authorized
        only per action.
        """
        for entry in (
            {**ENTRY, "kinds": ["publish"], "branches": []},
            {**ENTRY, "kinds": ["transmit"], "branches": []},
            {**ENTRY, "provisioned": False},
        ):
            with self.subTest(entry=entry):
                root = self.root / str(len(list(self.root.iterdir())))
                root.mkdir()
                write_authorization(root, remote_writes=[entry])
                record(root)
                with self.assertRaisesRegex(ValueError, "GUARD.11"):
                    reading(root)
                write_authorization(
                    root, remote_writes=[entry], standing=False
                )
                record(root)
                writes, referred = reading(root)
                self.assertEqual(writes, ())
                self.assertIn("per action", referred[0])

    def test_malformed_entries(self) -> None:
        """Behavior: an entry with a missing or extra field, an unknown
        or repeated kind, a credential or a dot segment in the address,
        a commit without branches, a branch with a pattern, or a post to
        an address that is no tracker stops the derivation.

        Reference: STND.PROJ.6 and STND.PROJ.7; AGENT.45, no credential
        in a record.
        """
        for entry in (
            {k: v for k, v in ENTRY.items() if k != "provisioned"},
            {**ENTRY, "extra": 1},
            {**ENTRY, "kinds": ["push"]},
            {**ENTRY, "kinds": ["commit", "commit"]},
            {**ENTRY, "destination": "https://user:pw@git.example.org/x"},
            {**ENTRY, "destination": "https://git.example.org/a/../b"},
            {**ENTRY, "destination": "https://git.example.org/x?y=1"},
            {**ENTRY, "destination": "ext::sh -c evil"},
            {**ENTRY, "branches": []},
            {**ENTRY, "branches": ["release/*"]},
            {**ENTRY, "branches": ["a..b"]},
            {
                **ENTRY,
                "destination": "https://git.example.org/team/work/x",
                "kinds": ["post"],
                "branches": [],
            },
            "https://git.example.org/team/work.git",
        ):
            with self.subTest(entry=entry):
                root = self.root / str(len(list(self.root.iterdir())))
                root.mkdir()
                write_authorization(root, remote_writes=[entry])
                record(root)
                with self.assertRaisesRegex(ValueError, "not in force"):
                    reading(root)

    def test_record_in_the_ledger(self) -> None:
        """Behavior: an authorization that no transaction pins, whose
        pinning transaction is no authorize of the human owner, whose
        content changed after the pin, or that a later transaction
        revokes, is not in force.

        Reference: STND.HARN.29, the row on the record; GUARD.10, an
        authorization is recorded; PRIME.5.
        """
        cases = (
            ("none", "no transaction"),
            ("agent", "no authorize"),
            ("changed", "content changed"),
            ("revoked", "revokes it"),
            ("amended", "no authorize"),
        )
        for case, reason in cases:
            with self.subTest(case=case):
                root = self.root / case
                root.mkdir()
                write_authorization(root)
                if case == "agent":
                    record(root, actor="Implementing agent")
                elif case != "none":
                    record(root)
                if case == "changed":
                    write_authorization(root, scope="Every branch")
                if case == "revoked":
                    record(root, "revoke", scope=[])
                if case == "amended":
                    record(root, "annotate")
                with self.assertRaisesRegex(ValueError, reason):
                    reading(root)

    def test_broken_chain(self) -> None:
        """Behavior: a ledger whose chain is broken records nothing in
        force.

        Reference: STND.HARN.8.
        """
        write_authorization(self.root)
        record(self.root)
        ledger = self.root / "ledger.jsonl"
        entries = parse_ledger(ledger.read_text(encoding="utf-8"))
        entries[0]["rationale"] = "Changed."
        ledger.write_text(
            "\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "chain is broken"):
            reading(self.root)

    def test_assured_work_needs_a_signature(self) -> None:
        """Behavior: for assured work, an unsigned transaction, or a
        signed one whose ledger does not verify, records nothing in
        force; a signed one that verifies does.

        Reference: STND.HARN.29; STND.HARN.11; for work without a
        constitution, STND.DFLT.23.
        """
        write_authorization(self.root)
        record(self.root)
        with self.assertRaisesRegex(ValueError, "signature"):
            reading(self.root, assured=True, verified=True)
        signed = self.root / "signed"
        signed.mkdir()
        write_authorization(signed)
        record(signed, signature="-----BEGIN PGP SIGNATURE-----")
        with self.assertRaisesRegex(ValueError, "signature"):
            reading(signed, assured=True, verified=False)
        writes, _ = reading(signed, assured=True, verified=True)
        self.assertEqual(len(writes), 1)

    def test_kinds_the_adapter_does_not_match(self) -> None:
        """Behavior: a standing authorization of kind other opens no
        write and is reported as referred; a post opens the tracker.

        Reference: STND.HARN.19, coverage states each gap; STND.PROJ.7.
        """
        entries = [
            {**ENTRY, "kinds": ["other"], "branches": []},
            {
                "destination": "https://git.example.org/team/work",
                "kinds": ["post"],
                "branches": [],
                "provisioned": True,
            },
        ]
        write_authorization(self.root, remote_writes=entries)
        record(self.root)
        writes, referred = reading(self.root)
        self.assertEqual([w.kind for w in writes], ["post"])
        self.assertIn("kind other", referred[0])

    def test_unknown_identifier(self) -> None:
        """Behavior: an identifier that names no authorization stops the
        derivation.

        Reference: STND.HARN.29.
        """
        with self.assertRaisesRegex(ValueError, "no authorization"):
            reading(self.root)


class Configuration(unittest.TestCase):
    """The configuration carries the writes the authorizations open."""

    def test_policy_rules_and_coverage(self) -> None:
        """Behavior: an opened commit reaches the guard's policy, drops
        the text rule that refers every push, and is named in the
        coverage report with its conditions; without one, the rule
        stays and the policy's list is empty.

        Reference: STND.HARN.18 and STND.HARN.19; a permission rule
        outranks a hook's answer, so the rule would refer every push.
        """
        corpus = read_corpus_live()
        write = RemoteWrite(IDENT, "commit", REPO, ("main",), "2027-01-01")
        inputs = Inputs(
            work="/srv/work", home="/home/agent", remote_writes=(write,),
            referred=("WORK.AUTH.2: per action",),
        )
        files = claude_code.render(corpus, inputs, "# guard\n")
        policy = json.loads(files[claude_code.POLICY])
        settings = json.loads(files[claude_code.SETTINGS])
        coverage = files[claude_code.COVERAGE]
        self.assertEqual(policy["remote_writes"][0]["destination"], REPO)
        self.assertNotIn("Bash(git push *)", settings["permissions"]["ask"])
        self.assertIn("Bash(git push --force *)", settings["permissions"]["deny"])
        self.assertIn("sole command of its call", coverage)
        self.assertIn("Referred: WORK.AUTH.2: per action.", coverage)
        self.assertIn("git.example.org is no opened domain", coverage)
        plain = claude_code.render(
            corpus, Inputs(work="/srv/work", home="/home/agent"), "# guard\n"
        )
        self.assertEqual(json.loads(plain[claude_code.POLICY])["remote_writes"], [])
        self.assertIn(
            "Bash(git push *)",
            json.loads(plain[claude_code.SETTINGS])["permissions"]["ask"],
        )

    def test_command_option(self) -> None:
        """Behavior: ``--authorization`` opens the writes of an
        authorization in force, and one that is not in force exits 1
        with the reason.

        Reference: STND.HARN.29; PRIME.4, a failure is loud.
        """
        with corpus_copy() as root:
            write_authorization(root)
            record(root)
            out = root.parent / "out"
            args = [
                "environment", str(root), "--work", str(root),
                "--home", str(root), "--authorization", IDENT,
            ]
            with contextlib.redirect_stdout(io.StringIO()):
                code = main([*args, "--write", str(out)])
            policy = json.loads((out / claude_code.POLICY).read_text())
            write_authorization(root, status="draft")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                bad = main([*args, "--write", str(out)])
        self.assertEqual(code, 0)
        self.assertEqual(policy["remote_writes"][0]["branches"], ["main"])
        self.assertEqual(bad, 1)
        self.assertIn("not in force", err.getvalue())


def read_corpus_live() -> Corpus:
    """Return an indexed copy of the live corpus held in memory.

    Returns
    -------
    Corpus
        A corpus that a test may change freely.
    """
    return Corpus(live_entries())


if __name__ == "__main__":
    unittest.main()
