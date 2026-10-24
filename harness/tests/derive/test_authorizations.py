"""Tests of the authorizations a derivation honors (unit 0008).

The reference is STND.PROJ.6 and STND.PROJ.7 (the form of an
authorization of a remote write, and its kinds), STND.HARN.29 (when a
derived configuration relies on one), and GUARD.11 (an irrevocable
remote write only per action). Each test writes an authorization file
and a ledger into a temporary corpus root, so no test reads or writes
the live corpus. Agreement is exact: the writes returned, or the reason
an authorization is not in force, are the ones stated. Unit 0010 adds
the refusal of unsigned authorizations where no signer register exists
and the work is not assured, unless the owner accepts them unsigned.
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from govharness.cli.main import main
from govharness.core.corpus import Corpus, corpus_hash, read_corpus, read_tree
from govharness.derive.environment import claude_code
from govharness.derive.environment.authorizations import (
    Reading,
    read_authorizations,
    register_recorded,
)
from govharness.derive.environment.inputs import Inputs, RemoteWrite
from govharness.ledger.chain import Signer, append, read_ledger
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.transactions import parse_ledger
from govharness.workflows.signers import add_signer, found_register
from tests.gpgkeys import keyring, make_key
from tests.support import corpus_copy, live_entries

NOW = datetime(2026, 10, 24, 12, 0, tzinfo=timezone.utc)
REPO = "https://git.example.org/team/work.git"
IDENT = "WORK.AUTH.1"
ROLE = "Implementing agent"
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


def record(
    root: Path,
    kind: str = "authorize",
    signer: Signer | None = None,
    **fields: object,
) -> None:
    """Append the transaction that pins the authorization.

    Parameters
    ----------
    root : Path
        Corpus root.
    kind : str
        Transaction type.
    signer : Signer | None
        Key and keyring that sign the transaction, or None.
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
    append(root, entry, signer=signer)


def reading(
    root: Path,
    assured: bool = False,
    verified: bool = False,
    role: str = ROLE,
    horizon: timedelta | None = None,
    accept_unsigned: bool = True,
) -> tuple[tuple[RemoteWrite, ...], tuple[str, ...]]:
    """Read the authorization of a root at ``NOW``.

    The tests of the rows of STND.HARN.29 accept an unsigned
    authorization by default, as the owner does with
    ``--accept-unsigned``, so that each tests its row alone; the class
    ``Unsigned`` tests the refusal without it.

    Parameters
    ----------
    root : Path
        Corpus root.
    assured : bool
        Whether a verified signature is required, as for assured work.
    verified : bool
        Whether the ledger's signatures verify.
    role : str
        The role the configuration is derived for.
    horizon : timedelta | None
        The owner's bound on the time to expiry.
    accept_unsigned : bool
        Whether the owner accepts the authorization unsigned.

    Returns
    -------
    tuple[tuple[RemoteWrite, ...], tuple[str, ...]]
        The writes opened and the lines still referred.
    """
    found = full_reading(
        root, assured, verified, role, horizon, accept_unsigned
    )
    return found.writes, found.referred


def full_reading(
    root: Path,
    signed: bool = False,
    verified: bool = False,
    role: str = ROLE,
    horizon: timedelta | None = None,
    accept_unsigned: bool = False,
) -> Reading:
    """Read the authorization of a root at ``NOW``, with its summary.

    Parameters
    ----------
    root : Path
        Corpus root.
    signed : bool
        Whether a verified signature is required, as for assured work
        or a corpus with a signer register.
    verified : bool
        Whether the ledger's signatures verify.
    role : str
        The role the configuration is derived for.
    horizon : timedelta | None
        The owner's bound on the time to expiry.
    accept_unsigned : bool
        Whether the owner accepts the authorization unsigned.

    Returns
    -------
    Reading
        The writes opened, the lines still referred, and the summary.
    """
    return read_authorizations(
        read_corpus(root),
        read_tree(root),
        read_ledger(root),
        (IDENT,),
        NOW,
        role,
        signed,
        verified,
        horizon,
        accept_unsigned,
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
        """Behavior: in a standing authorization, an entry of publication
        or transmission, or naming a destination not recorded as
        provisioned, opens nothing and its kind is reported as referred,
        while the authorization stays in force; the same per action
        opens nothing and stays referred.

        Reference: GUARD.11: an irrevocable remote write is authorized
        only per action; STND.HARN.29, row Standing, tested per entry.
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
                writes, referred = reading(root)
                self.assertEqual(writes, ())
                self.assertEqual(len(referred), 1)
                self.assertIn("GUARD.11", referred[0])
                write_authorization(
                    root, remote_writes=[entry], standing=False
                )
                record(root)
                writes, referred = reading(root)
                self.assertEqual(writes, ())
                self.assertIn("per action", referred[0])

    def test_irrevocable_entry_voids_only_its_writes(self) -> None:
        """Behavior: beside an irrevocable entry, or an irrevocable kind
        of the same entry, the revocable commit of a standing
        authorization still opens; only the irrevocable writes are
        referred.

        Reference: GUARD.11 voids the irrevocable write, not the others;
        STND.HARN.29, row Standing, tested for each entry.
        """
        other = "https://git.example.org/team/other.git"
        cases = (
            [ENTRY, {**ENTRY, "kinds": ["publish"], "branches": []}],
            [{**ENTRY, "kinds": ["publish"], "branches": []}, ENTRY],
            [ENTRY, {**ENTRY, "destination": other, "provisioned": False}],
            [{**ENTRY, "destination": other, "provisioned": False}, ENTRY],
            [{**ENTRY, "kinds": ["commit", "transmit"]}],
            [{**ENTRY, "kinds": ["transmit", "commit"]}],
        )
        for entries in cases:
            with self.subTest(entries=entries):
                root = self.root / str(len(list(self.root.iterdir())))
                root.mkdir()
                write_authorization(root, remote_writes=entries)
                record(root)
                writes, referred = reading(root)
                self.assertEqual(
                    writes,
                    (
                        RemoteWrite(
                            IDENT, "commit", REPO, ("main",), FIELDS["expires"]
                        ),
                    ),
                )
                self.assertEqual(len(referred), 1)
                self.assertIn("GUARD.11", referred[0])

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
            {**ENTRY, "kinds": [["commit"]]},
            {**ENTRY, "kinds": [{"commit": 1}]},
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

    def test_malformed_entry_fails_closed(self) -> None:
        """Behavior: a malformed entry beside a well-formed one stops the
        derivation, so the well-formed entry opens nothing either.

        Reference: STND.HARN.29, row Form: the record does not state one
        authorization, so none of it is relied on (fail closed).
        """
        bad = {**ENTRY, "kinds": ["push"]}
        for entries in ([ENTRY, bad], [bad, ENTRY], [ENTRY, bad, ENTRY]):
            with self.subTest(entries=entries):
                root = self.root / str(len(list(self.root.iterdir())))
                root.mkdir()
                write_authorization(root, remote_writes=entries)
                record(root)
                with self.assertRaisesRegex(ValueError, "not in force"):
                    reading(root)

    def test_mixed_entry_branches_by_kind(self) -> None:
        """Behavior: an entry of kinds commit and post opens a commit with
        its branches and a post with none.

        Reference: STND.PROJ.7: branches qualify a commit only.
        """
        write_authorization(
            self.root, remote_writes=[{**ENTRY, "kinds": ["commit", "post"]}]
        )
        record(self.root)
        writes, referred = reading(self.root)
        self.assertEqual(
            writes,
            (
                RemoteWrite(IDENT, "commit", REPO, ("main",), FIELDS["expires"]),
                RemoteWrite(IDENT, "post", REPO, (), FIELDS["expires"]),
            ),
        )
        self.assertEqual(referred, ())

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


class ExtensionAndDuration(unittest.TestCase):
    """GUARD.12 and GUARD.10: to whom, and for how long."""

    def setUp(self) -> None:
        """Make a corpus root with the authorization recorded."""
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_extension_to_the_role(self) -> None:
        """Behavior: an authorization opens writes only for a role that
        its field delegable_to names; another role, no role, and a
        malformed field stop the derivation.

        Reference: STND.HARN.29, row Extension; GUARD.12; PRIME.7, never
        widened by delegation (cold review, Defect 2).
        """
        write_authorization(self.root)
        record(self.root)
        self.assertEqual(len(reading(self.root)[0]), 1)
        for role in ("Research agent", ""):
            with (
                self.subTest(role=role),
                self.assertRaisesRegex(ValueError, "does not extend"),
            ):
                reading(self.root, role=role)
        bad = self.root / "bad"
        bad.mkdir()
        write_authorization(bad, delegable_to="Implementing agent")
        record(bad)
        with self.assertRaisesRegex(ValueError, "delegable_to"):
            reading(bad)

    def test_until_revoked_and_horizon(self) -> None:
        """Behavior: an authorization that lapses only when revoked is in
        force and opens a write with no expiry; an owner's horizon
        refuses it, and refuses an expiry beyond the horizon.

        Reference: STND.PROJ.6, field expires; GUARD.10, a stated
        duration; security review M5, a horizon the owner sets.
        """
        write_authorization(self.root, expires="until revoked")
        record(self.root)
        writes, _ = reading(self.root)
        self.assertEqual(writes[0].expires, "")
        with self.assertRaisesRegex(ValueError, "horizon"):
            reading(self.root, horizon=timedelta(days=90))
        later = self.root / "later"
        later.mkdir()
        write_authorization(later)
        record(later)
        self.assertEqual(len(reading(later, horizon=timedelta(days=90))[0]), 1)
        with self.assertRaisesRegex(ValueError, "beyond the horizon"):
            reading(later, horizon=timedelta(days=30))

    def test_forged_targets_and_dates(self) -> None:
        """Behavior: a pinning transaction whose targets are a string,
        a revoke whose targets are a string, and a date recorded after
        the pinning transaction each stop the derivation.

        Reference: security review L1 and L6.
        """
        cases = (
            ({}, {"targets": IDENT + "0"}, "no authorize"),
            ({"recorded": "2026-10-21"}, {}, "after its transaction"),
        )
        for index, (fields, entry, reason) in enumerate(cases):
            with self.subTest(reason=reason):
                root = self.root / str(index)
                root.mkdir()
                write_authorization(root, **fields)
                record(root, **entry)
                with self.assertRaisesRegex(ValueError, reason):
                    reading(root)
        root = self.root / "revoked"
        root.mkdir()
        write_authorization(root)
        record(root)
        record(root, "revoke", scope=[], targets="anything")
        with self.assertRaisesRegex(ValueError, "revokes it"):
            reading(root)


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
        self.assertIn("Bash(git push *)", settings["permissions"]["ask"])
        self.assertIn("Bash(gh issue comment *)", settings["permissions"]["ask"])
        self.assertIn("Bash(git push --force *)", settings["permissions"]["deny"])
        self.assertIn("one command of plain words", coverage)
        self.assertIn("may outrank a hook's allow", coverage)
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

    def test_git_metadata_denied(self) -> None:
        """Behavior: while a commit is authorized, the sandbox denies
        shell writes to the work's git configuration, worktree
        configuration, and hooks; without one, or with a post alone, it
        does not.

        Reference: security re-verification M-a: a program started
        earlier must not swap what the guard read before the push.
        """
        corpus = read_corpus_live()
        git = "/srv/work/.git"
        metadata = [f"{git}/config", f"{git}/config.worktree", f"{git}/hooks"]

        def denied(*writes: RemoteWrite) -> list[str]:
            """Return the sandbox's denyWrite for some opened writes.

            Parameters
            ----------
            *writes : RemoteWrite
                The writes opened.

            Returns
            -------
            list[str]
                The denied locations.
            """
            inputs = Inputs(
                work="/srv/work", home="/home/agent", remote_writes=writes
            )
            files = claude_code.render(corpus, inputs, "# guard\n")
            settings = json.loads(files[claude_code.SETTINGS])
            return settings["sandbox"]["filesystem"]["denyWrite"]

        commit = RemoteWrite(IDENT, "commit", REPO, ("main",), "2027-01-01")
        post = RemoteWrite(IDENT, "post", "https://e.org/a/b", (), "")
        for path in metadata:
            with self.subTest(path=path):
                self.assertIn(path, denied(commit))
                self.assertNotIn(path, denied())
                self.assertNotIn(path, denied(post))

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
                "--role", ROLE, "--accept-unsigned",
            ]
            shown = io.StringIO()
            with contextlib.redirect_stdout(shown):
                code = main([*args, "--write", str(out)])
            policy = json.loads((out / claude_code.POLICY).read_text())
            register = root / "SIGNR"
            register.mkdir()
            (register / "_doc.md").write_text(
                "---\nid: \"SIGNR\"\n---\n\nNo signers.\n", encoding="utf-8"
            )
            unsigned = io.StringIO()
            with contextlib.redirect_stderr(unsigned):
                signed = main([*args, "--write", str(out)])
            (register / "_doc.md").unlink()
            register.rmdir()
            write_authorization(root, status="draft")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                bad = main([*args, "--write", str(out)])
        self.assertEqual(code, 0)
        self.assertEqual(policy["remote_writes"][0]["branches"], ["main"])
        self.assertIn(f"authorization: {IDENT}: pinned by seq", shown.getvalue())
        self.assertEqual(signed, 1)
        self.assertIn("signature", unsigned.getvalue())
        self.assertIn("--accept-unsigned has no effect", unsigned.getvalue())
        self.assertEqual(bad, 1)
        self.assertIn("not in force", err.getvalue())


class Unsigned(unittest.TestCase):
    """Unit 0010: an unsigned authorization is relied on only by consent.

    Without a signer register, an agent that appends an ``authorize``
    naming the human owner to the ledger and recomputes its chain makes
    a record that the row Record of STND.HARN.29 accepts (security
    verification of unit 0008, M-c).
    """

    def setUp(self) -> None:
        """Make a corpus root with the authorization recorded unsigned."""
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        write_authorization(self.root)
        record(self.root)

    def test_refused_without_register(self) -> None:
        """Behavior: with no signer register and work not assured, the
        derivation is refused with the reason unless the owner accepts
        the authorization unsigned; a reason of the provision is
        reported beside it.

        Reference: unit 0010; PRIME.4, a failure is loud; PRIME.7, an
        agent does not open its own writes.
        """
        with self.assertRaisesRegex(
            ValueError, "no signer register exists.*--accept-unsigned"
        ):
            full_reading(self.root)
        write_authorization(self.root, status="draft")
        record(self.root)
        with self.assertRaises(ValueError) as caught:
            full_reading(self.root)
        self.assertIn("status 'draft'", str(caught.exception))
        self.assertIn("no signer register exists", str(caught.exception))

    def test_accepted_with_the_option(self) -> None:
        """Behavior: with the owner's acceptance, the authorization opens
        its write and the summary says that it was accepted unsigned.

        Reference: unit 0010; STND.HARN.29, row Signature.
        """
        found = full_reading(self.root, accept_unsigned=True)
        self.assertEqual(len(found.writes), 1)
        self.assertEqual(len(found.summary), 2)
        self.assertIn(f"{IDENT}: pinned by seq", found.summary[0])
        self.assertTrue(
            found.summary[1].startswith(f"{IDENT}: accepted unsigned")
        )

    def test_signature_required_regardless(self) -> None:
        """Behavior: where a signature is required, for a signer register
        or assured work, the option does not admit an unsigned or
        unverified transaction, and the reason says it has no effect; a
        verified one is relied on without the line on acceptance.

        Reference: STND.HARN.29, row Signature; STND.HARN.11.
        """
        for verified in (False, True):
            with (
                self.subTest(verified=verified),
                self.assertRaisesRegex(ValueError, "has no effect"),
            ):
                full_reading(
                    self.root,
                    signed=True,
                    verified=verified,
                    accept_unsigned=True,
                )
        signed = self.root / "signed"
        signed.mkdir()
        write_authorization(signed)
        record(signed, signature="-----BEGIN PGP SIGNATURE-----")
        for accept in (False, True):
            with self.subTest(accept=accept):
                found = full_reading(
                    signed,
                    signed=True,
                    verified=True,
                    accept_unsigned=accept,
                )
                self.assertEqual(len(found.writes), 1)
                self.assertEqual(len(found.summary), 1)

    def test_command_refuses_and_accepts(self) -> None:
        """Behavior: ``environment --authorization`` with no signer
        register exits 1 with the reason and writes nothing; with
        ``--accept-unsigned`` it writes the configuration and prints
        that the authorization was accepted unsigned; with
        ``--assured`` the option has no effect and it exits 1.

        Reference: unit 0010; STND.HARN.29, row Signature; PRIME.4.
        """
        with corpus_copy() as root:
            write_authorization(root)
            record(root)
            out = root.parent / "out"
            strict_out = root.parent / "strict"
            args = [
                "environment", str(root), "--work", str(root),
                "--home", str(root), "--authorization", IDENT,
                "--role", ROLE,
            ]
            refused = io.StringIO()
            with contextlib.redirect_stderr(refused):
                code = main([*args, "--write", str(out)])
            written = out.exists()
            shown = io.StringIO()
            with contextlib.redirect_stdout(shown):
                accepted = main(
                    [*args, "--accept-unsigned", "--write", str(out)]
                )
            policy = json.loads((out / claude_code.POLICY).read_text())
            assured = io.StringIO()
            with contextlib.redirect_stderr(assured):
                strict = main(
                    [
                        *args, "--accept-unsigned", "--assured",
                        "--write", str(strict_out),
                    ]
                )
            strict_written = strict_out.exists()
        self.assertEqual(code, 1)
        self.assertFalse(written)
        self.assertIn("no signer register exists", refused.getvalue())
        self.assertIn("--accept-unsigned", refused.getvalue())
        self.assertEqual(accepted, 0)
        self.assertEqual(len(policy["remote_writes"]), 1)
        self.assertIn(
            f"authorization: {IDENT}: accepted unsigned", shown.getvalue()
        )
        self.assertEqual(strict, 1)
        self.assertFalse(strict_written)
        self.assertIn("signature", assured.getvalue())
        self.assertIn("has no effect", assured.getvalue())


class AfterReview(unittest.TestCase):
    """Review of unit 0010: a removed register, the installed trace, and
    the command's verification of signatures.
    """

    def test_register_recorded(self) -> None:
        """Behavior: the ledger shows a register where an entry carries a
        signature or pins a scope at or under SIGNR, and not otherwise.

        Reference: review of unit 0010, M1.
        """
        plain = {"scope": ["WORK/AUTH"], "signature": ""}
        self.assertFalse(register_recorded([plain, {"scope": None}]))
        self.assertTrue(register_recorded([plain, {"signature": "x"}]))
        for scope in (["SIGNR"], ["MNEM", "SIGNR/keys"]):
            with self.subTest(scope=scope):
                self.assertTrue(register_recorded([{"scope": scope}]))
        self.assertFalse(register_recorded([{"scope": ["SIGNRX"]}]))

    def test_removed_register_refuses(self) -> None:
        """Behavior: where the corpus holds no signer register but its
        ledger shows one (a signed entry, or a transaction pinning
        SIGNR), the command exits 1 with the reason even with
        --accept-unsigned, and writes nothing.

        Reference: review of unit 0010, M1: removing a founded register
        must not reduce the check to the owner's statement.
        """
        for case in ("signed entry", "register scope"):
            with self.subTest(case=case), corpus_copy() as root:
                if case == "register scope":
                    register = root / "SIGNR"
                    register.mkdir()
                    (register / "_doc.md").write_text(
                        '---\nid: "SIGNR"\n---\n\nNo signers.\n',
                        encoding="utf-8",
                    )
                    record(
                        root, "register", actor="The Custodian",
                        targets=["SIGNR"], scope=["SIGNR"],
                    )
                    shutil.rmtree(register)
                    write_authorization(root)
                    record(root)
                else:
                    write_authorization(root)
                    record(root, signature="-----BEGIN PGP SIGNATURE-----")
                out = root.parent / "out"
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    code = main(
                        [
                            "environment", str(root), "--work", str(root),
                            "--home", str(root), "--authorization", IDENT,
                            "--role", ROLE, "--accept-unsigned",
                            "--write", str(out),
                        ]
                    )
                self.assertEqual(code, 1)
                self.assertFalse(out.exists())
                self.assertIn("no longer holds", err.getvalue())
                self.assertIn("signature", err.getvalue())

    def test_unsigned_reliance_is_recorded(self) -> None:
        """Behavior: an authorization relied on unsigned is named in the
        coverage report and in the draft entry's rationale; without one,
        neither names it.

        Reference: review of unit 0010, M2; STND.HARN.19, STND.HARN.20.
        """
        corpus = read_corpus_live()
        write = RemoteWrite(IDENT, "commit", REPO, ("main",), "2027-01-01")
        for unsigned in ((IDENT,), ()):
            with self.subTest(unsigned=unsigned):
                inputs = Inputs(
                    work="/srv/work", home="/home/agent",
                    remote_writes=(write,), unsigned=unsigned,
                )
                files = claude_code.render(corpus, inputs, "# guard\n")
                coverage = files[claude_code.COVERAGE]
                entry = json.loads(files[claude_code.ENTRY])
                for shown in (coverage, entry["rationale"]):
                    self.assertEqual(
                        "Relied on unsigned" in shown, bool(unsigned)
                    )
                    self.assertEqual(
                        f"--accept-unsigned where no signer register "
                        f"exists: {IDENT}" in shown,
                        bool(unsigned),
                    )

    def test_command_records_unsigned_reliance(self) -> None:
        """Behavior: the command with --accept-unsigned writes the
        authorization's name into coverage.md and entry-draft.json.

        Reference: review of unit 0010, M2.
        """
        with corpus_copy() as root:
            write_authorization(root)
            record(root)
            out = root.parent / "out"
            with contextlib.redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "environment", str(root), "--work", str(root),
                        "--home", str(root), "--authorization", IDENT,
                        "--role", ROLE, "--accept-unsigned",
                        "--write", str(out),
                    ]
                )
            coverage = (out / claude_code.COVERAGE).read_text()
            entry = json.loads((out / claude_code.ENTRY).read_text())
        self.assertEqual(code, 0)
        self.assertIn(f"exists: {IDENT}", coverage)
        self.assertIn(f"exists: {IDENT}", entry["rationale"])

    def test_command_verifies_signatures(self) -> None:
        """Behavior: with a founded signer register, the command relies on
        an authorize that the human owner's key signed, and names no
        unsigned reliance; a later authorize signed by another key is
        refused, with --accept-unsigned too.

        Reference: STND.HARN.29, row Signature; STND.HARN.11; review of
        unit 0010, L2 (the command must verify, not assume, signatures).
        """
        with keyring() as home, corpus_copy() as root:
            owner, owner_key = make_key(home, "Owner")
            intruder, _ = make_key(home, "Intruder")
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
            add_signer(
                register, "governance", "The Human Owner", "O", owner_key
            )
            for scope in ("MNEM", "SIGNR"):
                record(
                    root, "register", signer=(owner, home),
                    actor="The Custodian", targets=[scope], scope=[scope],
                )
            write_authorization(root)
            record(root, signer=(owner, home))
            out = root.parent / "out"
            args = [
                "environment", str(root), "--work", str(root),
                "--home", str(root), "--authorization", IDENT,
                "--role", ROLE,
            ]
            shown = io.StringIO()
            with (
                mock.patch(
                    "govharness.cli.environment.read_config",
                    return_value=config,
                ),
                contextlib.redirect_stdout(shown),
            ):
                good = main([*args, "--write", str(out)])
            coverage = (out / claude_code.COVERAGE).read_text()
            record(root, signer=(intruder, home))
            err = io.StringIO()
            with (
                mock.patch(
                    "govharness.cli.environment.read_config",
                    return_value=config,
                ),
                contextlib.redirect_stderr(err),
            ):
                forged = main(
                    [
                        *args, "--accept-unsigned",
                        "--write", str(root.parent / "forged"),
                    ]
                )
        self.assertEqual(good, 0)
        self.assertIn(
            f"authorization: {IDENT}: pinned by seq", shown.getvalue()
        )
        self.assertNotIn("accepted unsigned", shown.getvalue())
        self.assertNotIn("Relied on unsigned", coverage)
        self.assertEqual(forged, 1)
        self.assertIn("signature", err.getvalue())
        self.assertIn("has no effect", err.getvalue())


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
