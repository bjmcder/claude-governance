"""Tests of remote writes that an authorization in force names (unit 0008).

The reference is the remote-write row of STND.HARN.18 and STND.HARN.29:
a remote write that a standing authorization in force names by
destination and kind proceeds without referral, and every other remote
write is referred. Each test builds a repository's git metadata by hand
in a temporary directory, with the account's home and the system's git
configuration pointed into it and the variables of git and gh cleared,
so that no test reads the running account's configuration or runs git.
Agreement is exact: the set of outcomes reached is the one stated.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from typing import ClassVar
from unittest import mock

from govharness.hooks import guard
from tests.hooks.test_guard import POLICY

REPO = "https://git.example.org/team/work.git"
TRACKER = "https://git.example.org/team/work"
LATER = "2999-01-01T00:00:00+00:00"
EARLIER = "2000-01-01T00:00:00+00:00"


def grant(**fields: object) -> dict:
    """Return one entry of the policy's ``remote_writes``.

    Parameters
    ----------
    **fields : object
        Fields that replace those of a commit to ``main`` of ``REPO``.

    Returns
    -------
    dict
        The entry in JSON form.
    """
    entry = {
        "authorization": "WORK.AUTH.1",
        "kind": "commit",
        "destination": REPO,
        "branches": ["main"],
        "expires": LATER,
    }
    return {**entry, **fields}


POST = grant(kind="post", destination=TRACKER, branches=[])


class Repository:
    """A work with hand-made git metadata, and the guard's view of it.

    Parameters
    ----------
    config : str
        Text of the repository's ``.git/config``.
    grants : list[dict]
        Entries of ``remote_writes``.
    """

    def __init__(self, config: str, grants: list[dict]) -> None:
        """Make the work in a temporary directory.

        Parameters
        ----------
        config : str
            Text of the repository's ``.git/config``.
        grants : list[dict]
            Entries of ``remote_writes``.
        """
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name).resolve()
        self.home = base / "home"
        self.work = base / "work"
        (self.home).mkdir()
        (self.work / ".git" / "refs" / "tags").mkdir(parents=True)
        (self.work / ".git" / "config").write_text(config, encoding="utf-8")
        self.system = base / "gitconfig"
        self.policy = {
            **POLICY,
            "work": str(self.work),
            "writable": [str(self.work), "/dev/null"],
            "protected": [str(self.work)],
            "remote_writes": grants,
        }
        clean = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith(("GIT_", "GH_")) and k != "XDG_CONFIG_HOME"
        }
        self.patches = [
            mock.patch.dict(os.environ, {**clean, "HOME": str(self.home)},
                            clear=True),
            mock.patch.object(guard, "GIT_SYSTEM_CONFIG", str(self.system)),
        ]
        for patch in self.patches:
            patch.start()

    def close(self) -> None:
        """Undo the patches and remove the directory."""
        for patch in reversed(self.patches):
            patch.stop()
        self.tmp.cleanup()

    def outcomes(self, command: str, cwd: str | None = None) -> set:
        """Return the outcome keys a shell command reaches in the work.

        Parameters
        ----------
        command : str
            The command line.
        cwd : str | None
            Directory it runs in; the work when None.

        Returns
        -------
        set
            Keys of the outcomes reached.
        """
        event = {
            "tool_name": "Bash",
            "tool_input": {"command": command},
            "cwd": cwd or str(self.work),
        }
        found = guard.check_call(event, guard.read_policy(self.policy))
        return {key for key, _ in found.reached}


ORIGIN = f'[core]\n\tbare = false\n[remote "origin"]\n\turl = {REPO}\n'


class RepositoryCase(unittest.TestCase):
    """A test with a repository whose origin is ``REPO``."""

    CONFIG = ORIGIN
    GRANTS: ClassVar[list[dict]] = [grant()]

    def setUp(self) -> None:
        """Make the repository."""
        self.repo = Repository(self.CONFIG, list(self.GRANTS))
        self.addCleanup(self.repo.close)


class AuthorizedPush(RepositoryCase):
    """A push that an authorization names proceeds without referral."""

    def test_named_push_passes(self) -> None:
        """Behavior: pushes of an authorized branch to the authorized
        repository, named by its remote or by its address, reach no
        outcome.

        Reference: STND.HARN.18, row remote-write; STND.HARN.29.
        """
        for command in (
            "git push origin main",
            "git push -u origin main",
            "git push --quiet origin main:main",
            "git push origin HEAD:refs/heads/main",
            f"git push {REPO} main",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.repo.outcomes(command), set())

    def test_without_grants_every_push_is_referred(self) -> None:
        """Behavior: with no authorization in the policy, a push reaches
        remote-write, as before this unit.

        Reference: STND.HARN.18; the transition of ledger entry 53.
        """
        self.repo.policy["remote_writes"] = []
        self.assertEqual(
            self.repo.outcomes("git push origin main"), {"remote-write"}
        )

    def test_unattended_answer(self) -> None:
        """Behavior: unattended, an authorized push gets no answer and an
        unauthorized one is denied.

        Reference: STND.HARN.22.
        """
        self.repo.policy["unattended"] = True
        policy = guard.read_policy(self.repo.policy)
        for command, expected in (
            ("git push origin main", None),
            ("git push origin other", guard.DENY),
        ):
            event = {
                "tool_name": "Bash",
                "tool_input": {"command": command},
                "cwd": str(self.repo.work),
            }
            answer = guard.decide(guard.check_call(event, policy), policy)
            with self.subTest(command=command):
                decision = (
                    answer["hookSpecificOutput"]["permissionDecision"]
                    if answer
                    else None
                )
                self.assertEqual(decision, expected)

    def test_forced_push_is_still_refused(self) -> None:
        """Behavior: a forced or deleting push of an authorized branch
        reaches history-rewrite, which is refused.

        Reference: STND.HARN.18, row history-rewrite; PRIME.6.
        """
        for command in (
            "git push --force origin main",
            "git push origin +main",
            "git push origin :main",
            "git push -d origin main",
        ):
            with self.subTest(command=command):
                self.assertIn("history-rewrite", self.repo.outcomes(command))


class ExactDestination(RepositoryCase):
    """A destination matches only as the whole address."""

    GRANTS: ClassVar[list[dict]] = [
        grant(destination=f"{REPO}x"),
        grant(destination=REPO[:-4]),
    ]

    def test_near_addresses_are_referred(self) -> None:
        """Behavior: an address that differs from the authorized one by
        a suffix, a trailing slash, a host, a case, or a scheme reaches
        remote-write, as does a remote whose address is a prefix of an
        authorized one.

        Reference: the custodian's direction for this unit: destinations
        match exactly, never by a pattern that admits another.
        """
        for address in (
            REPO,
            f"{REPO}/",
            "https://git.example.org.evil.net/team/work.git",
            "https://GIT.example.org/team/work.git",
            "http://git.example.org/team/work.git",
            "https://git.example.org/team/work.gi",
        ):
            with self.subTest(address=address):
                found = self.repo.outcomes(f"git push {address} main")
                self.assertEqual(found, {"remote-write"})
        self.assertEqual(
            self.repo.outcomes("git push origin main"), {"remote-write"}
        )

    def test_kind_must_match(self) -> None:
        """Behavior: a post authorization at an address does not cover a
        push to it.

        Reference: STND.HARN.18 names destination and kind of write.
        """
        self.repo.policy["remote_writes"] = [
            grant(kind="post", destination=REPO, branches=[])
        ]
        self.assertEqual(
            self.repo.outcomes("git push origin main"), {"remote-write"}
        )


class PushShape(RepositoryCase):
    """Only a push whose effect is read from the call alone passes."""

    def test_branches_outside_the_grant(self) -> None:
        """Behavior: a branch the authorization does not name, or one of
        several, reaches remote-write.

        Reference: STND.PROJ.6, the branches of a commit.
        """
        for command in (
            "git push origin release",
            "git push origin main release",
            "git push origin main:release",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.repo.outcomes(command), {"remote-write"})

    def test_unclear_refspecs_and_options(self) -> None:
        """Behavior: a push with no refspec, a computed or tag refspec, a
        pattern, or an option outside the short list reaches remote-write.

        Reference: STND.HARN.29; git pushes tags, every branch, and
        submodules for these options, and takes the branch of ``HEAD``
        from the repository.
        """
        for command in (
            "git push origin",
            "git push",
            "git push origin HEAD",
            "git push origin main~1",
            "git push origin 'refs/heads/*'",
            "git push origin v1:refs/tags/v1",
            "git push origin refs/tags/v1:main",
            "git push --tags origin main",
            "git push --follow-tags origin main",
            "git push --all origin",
            "git push --recurse-submodules=on-demand origin main",
            "git push --receive-pack=evil origin main",
            "git push --repo=origin main",
            "git push -o ci.skip origin main",
            "git push origin -- main",
        ):
            with self.subTest(command=command):
                self.assertIn("remote-write", self.repo.outcomes(command))

    def test_not_the_sole_command(self) -> None:
        """Behavior: an authorized push with another command in its line,
        under a launcher, after an assignment, or with a global option of
        git reaches remote-write.

        Reference: STND.HARN.29; another command of the line may change
        the configuration or the refs after the guard has read them.
        """
        for command in (
            "git add -A && git push origin main",
            "git push origin main; echo done",
            "git push origin main | cat",
            "timeout 60 git push origin main",
            "bash -c 'git push origin main'",
            "X=1 git push origin main",
            "GIT_SSH_COMMAND=evil git push origin main",
            "git -c core.sshCommand=evil push origin main",
            "git -C . push origin main",
            "echo $(git push origin main)",
            "if true; then git push origin main; fi",
        ):
            with self.subTest(command=command):
                self.assertIn("remote-write", self.repo.outcomes(command))

    def test_tag_named_as_branch(self) -> None:
        """Behavior: a short refspec that names a local tag, loose or
        packed, reaches remote-write.

        Reference: git gives a short destination the type of its source,
        so such a push may create a tag of that name.
        """
        tags = self.repo.work / ".git" / "refs" / "tags"
        (tags / "main").write_text("0" * 40 + "\n", encoding="utf-8")
        self.assertEqual(
            self.repo.outcomes("git push origin main"), {"remote-write"}
        )
        (tags / "main").unlink()
        (self.repo.work / ".git" / "packed-refs").write_text(
            f"{'0' * 40} refs/tags/main\n", encoding="utf-8"
        )
        self.assertEqual(
            self.repo.outcomes("git push origin main"), {"remote-write"}
        )

    def test_environment_variable_of_git(self) -> None:
        """Behavior: while the account's environment sets a variable of
        git, an authorized push reaches remote-write.

        Reference: such a variable can name another configuration file
        or a program for the transport.
        """
        with mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": "/x"}):
            found = self.repo.outcomes("git push origin main")
        self.assertEqual(found, {"remote-write"})


class Redirection(unittest.TestCase):
    """Configuration that may send a push elsewhere leaves it referred."""

    def test_repository_configuration(self) -> None:
        """Behavior: a repository configuration that rewrites addresses,
        sets a push address, gives two addresses, includes another file,
        pushes tags or submodules, names a transport program, or is not
        readable leaves an authorized push referred.

        Reference: STND.HARN.29; git reads each of these settings for a
        push.
        """
        for extra in (
            (
                '[url "https://evil.example.net/"]\n'
                "\tpushInsteadOf = https://git.example.org/\n"
            ),
            (
                '[url "https://evil.example.net/"]\n'
                "\tinsteadOf = https://git.example.org/\n"
            ),
            '[remote "origin"]\n\tpushurl = https://evil.example.net/x\n',
            f'[remote "origin"]\n\turl = {REPO}\n',
            "[include]\n\tpath = other\n",
            '[includeIf "gitdir:/"]\n\tpath = other\n',
            "[push]\n\tfollowTags = true\n",
            "[push]\n\trecurseSubmodules = on-demand\n",
            "[submodule]\n\trecurse\n",
            "[core]\n\tsshCommand = evil\n",
            "[http]\n\tproxy = http://evil.example.net\n",
            '[remote "origin"]\n\treceivepack = evil\n',
            "[core] bare = false\n",
            "[core]\n\teditor = vi \\\n",
            '[core]\n\teditor = "vi\n',
        ):
            repo = Repository(ORIGIN + extra, [grant()])
            try:
                with self.subTest(extra=extra):
                    found = repo.outcomes("git push origin main")
                    self.assertEqual(found, {"remote-write"})
            finally:
                repo.close()

    def test_account_and_system_configuration(self) -> None:
        """Behavior: a rewriting of addresses in the account's or the
        system's configuration leaves an authorized push referred; a
        harmless setting there does not.

        Reference: STND.HARN.29; git reads both files.
        """
        rewrite = (
            '[url "https://evil.example.net/"]\n'
            "\tpushInsteadOf = https://git.example.org/\n"
        )
        repo = Repository(ORIGIN, [grant()])
        try:
            (repo.home / ".gitconfig").write_text(
                '[user]\n\tname = "A ; B"\n', encoding="utf-8"
            )
            self.assertEqual(repo.outcomes("git push origin main"), set())
            for path in (
                repo.home / ".gitconfig",
                repo.home / ".config" / "git" / "config",
                repo.system,
            ):
                with self.subTest(path=path):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(rewrite, encoding="utf-8")
                    found = repo.outcomes("git push origin main")
                    self.assertEqual(found, {"remote-write"})
                    path.unlink()
        finally:
            repo.close()

    def test_linked_worktree(self) -> None:
        """Behavior: in a linked worktree the guard reads the common
        configuration, so an authorized push passes and a rewriting
        there leaves it referred.

        Reference: git reads ``config`` of the common directory and
        ``config.worktree`` of the worktree's git directory.
        """
        repo = Repository(ORIGIN, [grant()])
        try:
            linked = repo.work.parent / "linked"
            gitdir = repo.work / ".git" / "worktrees" / "linked"
            gitdir.mkdir(parents=True)
            (gitdir / "commondir").write_text("../..\n", encoding="utf-8")
            linked.mkdir()
            (linked / ".git").write_text(
                f"gitdir: {gitdir}\n", encoding="utf-8"
            )
            self.assertEqual(
                repo.outcomes("git push origin main", str(linked)), set()
            )
            (gitdir / "config.worktree").write_text(
                "[core]\n\tsshCommand = evil\n", encoding="utf-8"
            )
            self.assertEqual(
                repo.outcomes("git push origin main", str(linked)),
                {"remote-write"},
            )
        finally:
            repo.close()


class GrantForm(RepositoryCase):
    """An entry of the policy that is expired or malformed refers."""

    def test_expired_and_malformed(self) -> None:
        """Behavior: an expired entry, one without a UTC offset, one of
        an irrevocable kind, one with a missing field, and a commit
        without branches each leave the push referred.

        Reference: STND.HARN.29: an authorization relied on is in force
        at the time of the write; GUARD.11.
        """
        for entry in (
            grant(expires=EARLIER),
            grant(expires="2999-01-01T00:00:00"),
            grant(expires="never"),
            grant(kind="publish"),
            grant(branches=[]),
            {k: v for k, v in grant().items() if k != "expires"},
            {**grant(), "extra": 1},
            "WORK.AUTH.1",
        ):
            with self.subTest(entry=entry):
                self.repo.policy["remote_writes"] = [entry]
                self.assertEqual(
                    self.repo.outcomes("git push origin main"),
                    {"remote-write"},
                )

    def test_remote_writes_not_a_list(self) -> None:
        """Behavior: a policy whose ``remote_writes`` is no list is not
        read.

        Reference: the guard's other list fields; a fault of the policy
        follows the class (STND.HARN.23).
        """
        policy = {**POLICY, "remote_writes": {"kind": "commit"}}
        with self.assertRaises(ValueError):
            guard.read_policy(policy)


class TrackerPost(RepositoryCase):
    """A tracker post that an authorization names proceeds."""

    GRANTS: ClassVar[list[dict]] = [POST]

    def test_named_posts_pass(self) -> None:
        """Behavior: an issue, an issue comment, and a change comment on
        the authorized tracker, named by ``--repo HOST/OWNER/REPO``,
        reach no outcome.

        Reference: STND.HARN.18, row remote-write; STND.PROJ.7, kind post.
        """
        for command in (
            "gh issue create -R git.example.org/team/work -t T -b B",
            "gh issue comment 12 --repo=git.example.org/team/work -b x",
            "gh pr comment 3 -Rgit.example.org/team/work --body-file a.md",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.repo.outcomes(command), set())

    def test_other_posts_are_referred(self) -> None:
        """Behavior: another tracker, a short or missing ``--repo``, an
        address operand, an option outside the list, a write that edits
        or closes, and a post that is not the sole command reach
        remote-write.

        Reference: STND.PROJ.7: a post adds without editing, closing, or
        deleting.
        """
        for command in (
            "gh issue create -R git.example.org/team/other -t T -b B",
            "gh issue create -R team/work -t T -b B",
            "gh issue create -t T -b B",
            (
                "gh issue create -R git.example.org/team/work "
                "-R git.example.org/team/other -t T"
            ),
            (
                "gh issue comment https://git.example.org/x/y/issues/1 "
                "-R git.example.org/team/work -b x"
            ),
            "gh issue comment 1 -R git.example.org/team/work --edit-last",
            "gh issue create -R git.example.org/team/work --web",
            "gh issue close 1 -R git.example.org/team/work",
            "gh pr create -R git.example.org/team/work --fill",
            "gh issue -R git.example.org/team/work create -t T",
            "GH_HOST=x gh issue create -R git.example.org/team/work -t T",
            "gh issue create -R git.example.org/team/work -t T && echo",
        ):
            with self.subTest(command=command):
                self.assertIn("remote-write", self.repo.outcomes(command))

    def test_sent_file_is_read(self) -> None:
        """Behavior: a body file outside the working bounds reaches
        read-bounds even where the post is authorized.

        Reference: STND.DFLT.25; the file's content is sent.
        """
        found = self.repo.outcomes(
            "gh issue create -R git.example.org/team/work -t T "
            "-F /home/other/notes"
        )
        self.assertEqual(found, {"read-bounds"})


if __name__ == "__main__":
    unittest.main()
