"""Tests of the pre-action guard (STND.HARN.18).

Each test gives the guard one tool call and states the outcome the call
reaches, which is the reference: the outcome table of STND.HARN.18 and
the protected locations of STND.INSTR.3. The policy is built here, so
no test reads or writes outside memory, except the one that makes a
symbolic link in a temporary directory. Agreement is exact: a named
outcome is among those reached, or the set reached is the one stated.
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from govharness.hooks import guard

WORK = "/srv/work"
RESPONSES = {
    "protected-locations": "Refuse",
    "history-rewrite": "Refuse",
    "record-entries": "Refuse",
    "elevated-privilege": "Refuse",
    "write-bounds": "Refuse",
    "read-bounds": "Refer",
    "network-bounds": "Refuse",
    "remote-write": "Refer",
    "selective-destruction": "Refer",
    "enforcing-configuration": "Refuse",
}
POLICY = {
    "work": WORK,
    "writable": [WORK, "/tmp", "/dev/null"],
    "readable": ["/usr"],
    "protected": ["/", "/home/agent", "/root", WORK, f"{WORK}/records",
                  f"{WORK}/.git"],
    "homes": ["/home"],
    "configuration": ["/etc/governance", "/home/agent/.claude",
                      f"{WORK}/.claude"],
    "ledgers": ["ledger.jsonl"],
    "domains": ["pypi.org"],
    "search": False,
    "tools": ["mcp__memory__*"],
    "store": "",
    "secrets": [],
    "remote_writes": [],
    "responses": RESPONSES,
    "unattended": False,
}


def outcomes_of(tool: str, data: dict, policy: dict | None = None) -> set:
    """Return the outcome keys one call reaches.

    Parameters
    ----------
    tool : str
        Tool name.
    data : dict
        Tool input.
    policy : dict | None
        Policy in JSON form; the module policy when None.

    Returns
    -------
    set
        Keys of the outcomes reached.
    """
    event = {"tool_name": tool, "tool_input": data, "cwd": WORK}
    found = guard.check_call(event, guard.read_policy(policy or POLICY))
    return {key for key, _ in found.reached}


def shell(command: str) -> set:
    """Return the outcome keys one shell command reaches.

    Parameters
    ----------
    command : str
        The command line.

    Returns
    -------
    set
        Keys of the outcomes reached.
    """
    return outcomes_of("Bash", {"command": command})


class RoutineActions(unittest.TestCase):
    """Routine actions inside the working bounds reach no outcome."""

    def test_routine_commands(self) -> None:
        """Behavior: commits, builds, listed single-file removals inside
        the work, reads, and redirections to /dev/null reach no outcome.

        Reference: decision 0002, routine work runs unattended without a
        prompt; none of these is a reserved action (STND.DFLT.24 lists a
        named file as its own list).
        """
        for command in (
            "git add -A && git commit -m 'Fix a test'",
            "cd src && python3 -B -m unittest",
            "rm build/a.o build/b.o",
            "ls -la && cat README.md",
            "git status; git log --oneline | head",
            "echo done > /dev/null 2>&1",
            "python -m govharness ledger append governance --type amend",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())

    def test_file_tools_inside_bounds(self) -> None:
        """Behavior: editing inside the work and reading installed
        software reach no outcome.

        Reference: the term Working bounds of STND.DFLT.
        """
        self.assertEqual(
            outcomes_of("Edit", {"file_path": f"{WORK}/src/a.py"}), set()
        )
        self.assertEqual(outcomes_of("Read", {"file_path": "/usr/x"}), set())


class ProtectedLocations(unittest.TestCase):
    """STND.INSTR.3: no protected location is taken out of use."""

    def test_removal_and_move(self) -> None:
        """Behavior: removing, moving, or emptying a protected location
        reaches protected-locations.

        Reference: the table of STND.INSTR.3, mapped to this policy.
        """
        for command in (
            "rm -rf /",
            "rm -rf ~",
            "rm -r .git",
            "mv records /tmp/old",
            "rm -rf /srv/work/*",
            "rmdir /home/someone",
            "find . -delete",
            "cd / && rm -rf /srv",
        ):
            with self.subTest(command=command):
                self.assertIn("protected-locations", shell(command))

    def test_hidden_in_substitution(self) -> None:
        """Behavior: a removal inside a substitution, ``bash -c``, or a
        later line is caught.

        Reference: STND.INSTR.3 and PRIME.12, no effect by indirection.
        """
        self.assertIn("protected-locations", shell("echo $(rm -rf /)"))
        self.assertIn("protected-locations", shell("bash -c 'rm -rf ~'"))
        self.assertIn(
            "protected-locations", shell("echo ok\nrm -rf /srv/work")
        )


class ShellReading(unittest.TestCase):
    """The guard reads a command line as the shell does (review 0003)."""

    def test_compound_commands(self) -> None:
        """Behavior: a removal inside a compound command is caught.

        Reference: STND.INSTR.3; bash runs the command after a reserved
        word. Before review 0003 each of these reached no outcome.
        """
        for command in (
            "if true; then rm -rf /srv/work; fi",
            "while true; do rm -rf /srv/work; done",
            "{ rm -rf /srv/work; }",
            "! rm -rf /srv/work",
        ):
            with self.subTest(command=command):
                self.assertIn("protected-locations", shell(command))

    def test_launchers(self) -> None:
        """Behavior: a program that runs another does not hide it.

        Reference: STND.INSTR.3; each launcher runs the removal that
        follows its options. Before review 0003 options with a value,
        and launchers outside a fixed list, hid the removal.
        """
        for command in (
            "timeout -s KILL 5 rm -rf /srv/work",
            "env -u X rm -rf /srv/work",
            "busybox rm -rf /srv/work",
            "uv run rm -rf /srv/work",
            "watch 'rm -rf /srv/work'",
            "env -C / rm -rf home",
        ):
            with self.subTest(command=command):
                self.assertIn("protected-locations", shell(command))

    def test_directory_changes(self) -> None:
        """Behavior: a relative operand is resolved against each
        directory the line may run in.

        Reference: STND.INSTR.3; after ``cd ..`` from the work, ``work``
        names the work. Before review 0003 relative paths were resolved
        against the starting directory alone.
        """
        for command in (
            "cd .. && rm -rf work",
            "cd / && rm -rf home",
            "(cd records && ls); rm -r .git",
        ):
            with self.subTest(command=command):
                self.assertIn("protected-locations", shell(command))

    def test_expansions(self) -> None:
        """Behavior: known variables, the tilde, and braces are
        expanded; an unknown value makes the item computed.

        Reference: STND.INSTR.3 for the known values; STND.DFLT.24 and
        STND.INSTR.4 for a computed item, which cannot be listed and is
        referred. Before review 0003 ``mv $HOME /tmp/x`` reached nothing.
        """
        for command in (
            "rm -rf $HOME",
            "mv $HOME /tmp/x",
            "rm -rf /srv/work/{records,x}",
            "mv /srv/wor? /tmp/x",
            "rm -rf ~+",
            "mv -t /tmp/x /srv/work/records",
        ):
            with self.subTest(command=command):
                self.assertIn("protected-locations", shell(command))
        for command in ('rm -rf "$BUILD"', "X=rm; $X -rf build"):
            with self.subTest(command=command):
                self.assertIn("selective-destruction", shell(command))

    def test_substitutions_and_input(self) -> None:
        """Behavior: commands in process substitutions, here-strings,
        and here-documents given to a shell are read; a shell fed by a
        pipe is referred.

        Reference: STND.INSTR.3 and STND.INSTR.4. Before review 0003
        the first two reached no outcome and the last passed.
        """
        self.assertIn(
            "protected-locations", shell("cat <(rm -rf /srv/work)")
        )
        self.assertIn(
            "protected-locations", shell("bash <<< 'rm -rf /srv/work'")
        )
        self.assertIn(
            "selective-destruction", shell("echo 'rm -rf x' | sh")
        )

    def test_here_document_is_data(self) -> None:
        """Behavior: a here-document given to a program other than a
        shell is data, so a commit message in one passes.

        Reference: the commit form Claude Code uses, a message in
        ``$(cat <<'EOF' ... EOF)``. Before review 0003 an apostrophe in
        the message left the line unreadable, and an unattended session
        refused the commit.
        """
        command = (
            "git commit -m \"$(cat <<'EOF'\n"
            "Fix: don't break the build\nEOF\n)\""
        )
        self.assertEqual(shell(command), set())

    def test_redirections(self) -> None:
        """Behavior: each redirection that writes is read, and the file
        descriptor before an operator is no operand.

        Reference: bash redirection syntax; ``>&FILE`` writes FILE, and
        in ``cp a /etc/x 2>/dev/null`` the destination is ``/etc/x``.
        """
        self.assertIn(
            "record-entries", shell("echo {} >& records/ledger.jsonl")
        )
        self.assertIn("write-bounds", shell("cp a /etc/x 2>/dev/null"))
        self.assertIn("read-bounds", shell("cat < /etc/shadow"))
        self.assertIn("read-bounds", shell("cat ../../etc/shadow"))

    def test_abbreviated_option(self) -> None:
        """Behavior: an abbreviated long option counts as the option.

        Reference: GNU getopt accepts ``--rec`` for ``--recursive``.
        """
        self.assertIn("selective-destruction", shell("rm --rec build"))

    def test_file_patterns(self) -> None:
        """Behavior: a pattern of non-recursive ``rm`` empties nothing,
        while a recursive one of wildcards alone empties its directory.

        Reference: STND.INSTR.3; ``rm`` without recursion removes files
        alone. Before review 0003 ``rm *.o`` in the work was refused as
        emptying the work.
        """
        self.assertEqual(shell("rm *.o"), {"selective-destruction"})
        self.assertIn("protected-locations", shell("rm -rf *"))


class HistoryAndRecords(unittest.TestCase):
    """PRIME.5: history is not rewritten and entries are not changed."""

    def test_history_rewrites(self) -> None:
        """Behavior: forced pushes and history-rewriting commands reach
        history-rewrite.

        Reference: PRIME.5.
        """
        for command in (
            "git push --force origin main",
            "git push -f",
            "git push origin +main",
            "git rebase -i HEAD~3",
            "git commit --amend -m x",
            "git -C repo filter-branch --all",
            "git branch -D topic",
            "git reflog expire --all",
        ):
            with self.subTest(command=command):
                self.assertIn("history-rewrite", shell(command))

    def test_history_rewrite_forms(self) -> None:
        """Behavior: abbreviated options, pruning pushes, and forced
        moves or deletions of branches, tags, and refs are caught.

        Reference: PRIME.5; git accepts an unambiguous prefix of a long
        option. Before review 0003 each of these reached no
        history-rewrite.
        """
        for command in (
            "git push --prune origin",
            "git push --forc origin main",
            "git commit --am -m x",
            "git branch -f main HEAD~3",
            "git tag -f v1.0",
            "git tag -d v1.0",
            "git update-ref refs/heads/main HEAD~1",
            "git checkout -B main HEAD~1",
        ):
            with self.subTest(command=command):
                self.assertIn("history-rewrite", shell(command))

    def test_git_removals_and_settings(self) -> None:
        """Behavior: ``git rm`` and ``git mv`` of a protected location,
        and a command set through ``git -c``, are caught.

        Reference: STND.INSTR.3; an alias that starts with ``!`` runs a
        shell command. Before review 0003 each reached no outcome.
        """
        for command in (
            "git rm -r records",
            "git mv records old",
            "git -c alias.x='!rm -rf /srv/work' x",
        ):
            with self.subTest(command=command):
                self.assertIn("protected-locations", shell(command))

    def test_dry_runs_pass(self) -> None:
        """Behavior: the dry run of a selective removal passes.

        Reference: STND.INSTR.4 requires the dry run first, so it must
        not itself be referred. Before review 0003 ``git clean -n`` was.
        """
        for command in (
            "git clean -n -d",
            "rsync -an --delete a/ b/",
            "git push --dry-run origin main",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())

    def test_ledger_changes(self) -> None:
        """Behavior: truncating, editing, or removing a ledger reaches
        record-entries.

        Reference: PRIME.5.
        """
        for command in (
            "echo {} > governance/ledger.jsonl",
            "sed -i 1d records/ledger.jsonl",
            "rm records/ledger.jsonl",
        ):
            with self.subTest(command=command):
                self.assertIn("record-entries", shell(command))
        self.assertIn(
            "record-entries",
            outcomes_of("Edit", {"file_path": f"{WORK}/ledger.jsonl"}),
        )

    def test_ledger_append_passes(self) -> None:
        """Behavior: appending to a ledger by redirection reaches no
        outcome of the guard.

        Reference: PRIME.5 allows adding entries. The managed rule
        ``Edit(**/ledger.jsonl)`` still denies a shell redirection to
        it, so in use entries are appended by the harness, in Python.
        """
        self.assertEqual(shell("echo {} >> records/ledger.jsonl"), set())


class PrivilegeAndBounds(unittest.TestCase):
    """PRIME.9 and STND.DFLT.25: privilege and the working bounds."""

    def test_privilege(self) -> None:
        """Behavior: elevating commands and set-user modes reach
        elevated-privilege.

        Reference: PRIME.9.
        """
        for command in ("sudo ls", "env X=1 sudo -u root id", "chmod 4755 x",
                        "chmod u+s x", "doas reboot"):
            with self.subTest(command=command):
                self.assertIn("elevated-privilege", shell(command))

    def test_writes_outside(self) -> None:
        """Behavior: writes outside the writable locations reach
        write-bounds.

        Reference: STND.DFLT.25.
        """
        self.assertIn("write-bounds", shell("cp a.txt /etc/a.txt"))
        self.assertIn("write-bounds", shell("echo x > /opt/x"))
        self.assertIn(
            "write-bounds", outcomes_of("Write", {"file_path": "/etc/x"})
        )

    def test_reads_outside(self) -> None:
        """Behavior: reads outside the readable locations reach
        read-bounds.

        Reference: STND.DFLT.25.
        """
        self.assertIn("read-bounds", shell("cat /etc/shadow"))
        self.assertIn(
            "read-bounds", outcomes_of("Read", {"file_path": "/home/b/x"})
        )

    def test_network(self) -> None:
        """Behavior: a fetch outside the opened domains, a URL whose host
        hides behind user information or a backslash, and search that
        is not opened reach network-bounds; a subdomain passes.

        Reference: STND.DFLT.25 and GUARD.13.
        """
        self.assertEqual(
            outcomes_of("WebFetch", {"url": "https://files.pypi.org/x"}),
            set(),
        )
        self.assertIn(
            "network-bounds",
            outcomes_of("WebFetch", {"url": "https://evil.example/x"}),
        )
        self.assertIn(
            "network-bounds", outcomes_of("WebSearch", {"query": "x"})
        )
        for url in (
            "https://evil.example\\@pypi.org/",
            "https://pypi.org@evil.example/",
            "https://pypi.org.evil.example/",
            "file:///etc/passwd",
        ):
            with self.subTest(url=url):
                self.assertIn(
                    "network-bounds", outcomes_of("WebFetch", {"url": url})
                )

    def test_configuration(self) -> None:
        """Behavior: changing the enforcing configuration reaches
        enforcing-configuration.

        Reference: STND.DFLT.22.
        """
        self.assertIn(
            "enforcing-configuration",
            outcomes_of("Edit", {"file_path": f"{WORK}/.claude/s.json"}),
        )
        self.assertIn(
            "enforcing-configuration", shell("rm /etc/governance/guard.py")
        )


class RemoteAndSelective(unittest.TestCase):
    """PRIME.7 and STND.INSTR.4: remote writes and selected removals."""

    def test_remote_writes(self) -> None:
        """Behavior: pushes, uploads, and unopened tools of other servers
        reach remote-write; an opened one does not.

        Reference: PRIME.7 and GUARD.13.
        """
        for command in (
            "git push origin main",
            "curl -X POST https://pypi.org/x",
            "curl -d a=1 https://pypi.org",
            "scp a host:/b",
            "gh pr create --fill",
            "npm publish",
        ):
            with self.subTest(command=command):
                self.assertIn("remote-write", shell(command))
        self.assertIn("remote-write", outcomes_of("mcp__slack__post", {}))
        self.assertEqual(outcomes_of("mcp__memory__read", {}), set())

    def test_selected_removals(self) -> None:
        """Behavior: recursive, pattern, and computed removals reach
        selective-destruction.

        Reference: STND.INSTR.4.
        """
        for command in (
            "rm -r build",
            "rm *.o",
            "find build -name '*.o' -delete",
            "ls | xargs rm",
            "git clean -fdx",
            "git reset --hard",
            "rsync -a --delete a/ b/",
        ):
            with self.subTest(command=command):
                self.assertIn("selective-destruction", shell(command))


STORE = f"{WORK}/secrets"
STORE_POLICY = {**POLICY, "store": STORE, "secrets": [f"{STORE}/token"]}


def store_work(tmp: str) -> tuple[str, dict]:
    """Make a work with a store in a temporary directory.

    Parameters
    ----------
    tmp : str
        The temporary directory.

    Returns
    -------
    tuple[str, dict]
        The work, whose store holds ``token`` (opened) and ``key``, and
        the policy in JSON form.
    """
    work = str(Path(tmp).resolve())
    store = f"{work}/secrets"
    Path(store).mkdir()
    for name in ("token", "key"):
        Path(f"{store}/{name}").write_text("x", encoding="utf-8")
    policy = {
        **POLICY,
        "work": work,
        "writable": [work, "/dev/null"],
        "store": store,
        "secrets": [f"{store}/token"],
    }
    return work, policy


def in_work(work: str, policy: dict, tool: str, data: dict) -> set:
    """Return the outcome keys one call reaches from a given work.

    Parameters
    ----------
    work : str
        Directory the call runs in.
    policy : dict
        Policy in JSON form.
    tool : str
        Tool name.
    data : dict
        Tool input.

    Returns
    -------
    set
        Keys of the outcomes reached.
    """
    event = {"tool_name": tool, "tool_input": data, "cwd": work}
    found = guard.check_call(event, guard.read_policy(policy))
    return {key for key, _ in found.reached}


class SecretStore(unittest.TestCase):
    """STND.DFLT.29: a file of the store is in bounds only once opened."""

    STORE = STORE

    def store_outcomes(self, tool: str, data: dict) -> set:
        """Return the outcome keys one call reaches with a store.

        Parameters
        ----------
        tool : str
            Tool name.
        data : dict
            Tool input.

        Returns
        -------
        set
            Keys of the outcomes reached.
        """
        return outcomes_of(tool, data, STORE_POLICY)

    def test_closed_file(self) -> None:
        """Behavior: reading or writing a file of the store that is not
        opened reaches read-bounds or write-bounds, by the file tools and
        by the shell.

        Reference: the term Working bounds of STND.DFLT; the file
        ``secrets/key`` is not opened by the policy.
        """
        key = f"{self.STORE}/key"
        self.assertEqual(
            self.store_outcomes("Read", {"file_path": key}), {"read-bounds"}
        )
        self.assertEqual(
            self.store_outcomes("Write", {"file_path": key}), {"write-bounds"}
        )
        for command, outcome in (
            ("cat secrets/key", "read-bounds"),
            ("echo x > secrets/key", "write-bounds"),
            ("echo x >> secrets/key", "write-bounds"),
            ("cp notes.txt secrets/key", "write-bounds"),
        ):
            with self.subTest(command=command):
                found = self.store_outcomes("Bash", {"command": command})
                self.assertIn(outcome, found)

    def test_opened_file_and_directory(self) -> None:
        """Behavior: the opened file, and the directory itself, are in
        bounds.

        Reference: ``secrets/token`` is opened by the policy; the names
        of the store hold no secret (STND.DFLT.29), and STND.DFLT.30 has
        the agent confirm the directory's permissions.
        """
        token = f"{self.STORE}/token"
        for tool in ("Read", "Write", "Edit"):
            with self.subTest(tool=tool):
                found = self.store_outcomes(tool, {"file_path": token})
                self.assertEqual(found, set())
        for command in (
            "cat secrets/token",
            "ls -la secrets",
            "stat secrets",
        ):
            with self.subTest(command=command):
                found = self.store_outcomes("Bash", {"command": command})
                self.assertEqual(found, set())

    def test_link_into_store(self) -> None:
        """Behavior: a symbolic link that leads to a closed file of the
        store reaches read-bounds.

        Reference: paths resolve through links as the guard resolves
        them elsewhere; the link sits in a temporary work.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp).resolve())
            store = f"{work}/secrets"
            Path(store).mkdir()
            Path(f"{store}/key").write_text("x", encoding="utf-8")
            Path(f"{work}/alias").symlink_to(f"{store}/key")
            policy = {
                **POLICY,
                "work": work,
                "writable": [work, "/dev/null"],
                "store": store,
                "secrets": [],
            }
            found = outcomes_of("Read", {"file_path": f"{work}/alias"}, policy)
        self.assertEqual(found, {"read-bounds"})

    def test_search_over_the_store(self) -> None:
        """Behavior: Grep over a directory that holds the store reaches
        read-bounds while the store holds a closed file, and passes when
        it holds only opened files or does not exist; Glob passes.

        Reference: STND.DFLT.31; a store in a temporary work holding
        ``token`` (opened) and, in the first case, ``key``.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp).resolve())
            store = f"{work}/secrets"
            policy = {
                **POLICY,
                "work": work,
                "writable": [work, "/dev/null"],
                "store": store,
                "secrets": [f"{store}/token"],
            }
            grep = {"pattern": "x", "path": work}
            glob = {"pattern": "**/*", "path": work}
            self.assertEqual(outcomes_of("Grep", grep, policy), set())
            Path(store).mkdir()
            Path(f"{store}/token").write_text("x", encoding="utf-8")
            self.assertEqual(outcomes_of("Grep", grep, policy), set())
            Path(f"{store}/key").write_text("x", encoding="utf-8")
            self.assertEqual(
                outcomes_of("Grep", grep, policy), {"read-bounds"}
            )
            inside = {"pattern": "x", "path": store}
            self.assertEqual(
                outcomes_of("Grep", inside, policy), {"read-bounds"}
            )
            elsewhere = {"pattern": "x", "path": f"{work}/src"}
            self.assertEqual(outcomes_of("Grep", elsewhere, policy), set())
            self.assertEqual(outcomes_of("Glob", glob, policy), set())

    def test_store_is_a_link(self) -> None:
        """Behavior: where the store is a symbolic link, its closed files
        are reached where the link leads.

        Reference: unit 0007 criterion 2; review 0007 found the store
        compared as spelled.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work, policy = store_work(tmp)
            Path(f"{work}/secrets").rename(f"{work}/other")
            Path(f"{work}/secrets").symlink_to(f"{work}/other")
            closed = {"file_path": f"{work}/secrets/key"}
            opened = {"file_path": f"{work}/secrets/token"}
            grep = {"pattern": "x", "path": f"{work}/secrets"}
            self.assertEqual(
                in_work(work, policy, "Read", closed), {"read-bounds"}
            )
            self.assertEqual(in_work(work, policy, "Read", opened), set())
            self.assertEqual(
                in_work(work, policy, "Grep", grep), {"read-bounds"}
            )
            direct = {"file_path": f"{work}/other/key"}
            self.assertEqual(
                in_work(work, policy, "Read", direct), {"read-bounds"}
            )

    def test_directory_operands(self) -> None:
        """Behavior: a copy, move, or removal that takes in the store
        while it holds a closed file reaches read-bounds or write-bounds;
        a change of the store's permissions passes.

        Reference: unit 0007 criterion 2; review 0007 found that
        ``cp -r`` and ``mv`` of the directory passed. STND.DFLT.30 has
        the agent restore the directory's permissions.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work, policy = store_work(tmp)
            for command, outcome in (
                ("cp -r secrets other", "read-bounds"),
                ("cp -r . ../copy", "read-bounds"),
                ("mv secrets other", "write-bounds"),
                ("mv secrets/* other", "write-bounds"),
                ("rm -r secrets", "write-bounds"),
            ):
                with self.subTest(command=command):
                    found = in_work(work, policy, "Bash", {"command": command})
                    self.assertIn(outcome, found)
            chmod = {"command": "chmod 700 secrets"}
            self.assertEqual(in_work(work, policy, "Bash", chmod), set())

    def test_unlistable_store(self) -> None:
        """Behavior: a store that exists but cannot be listed counts as
        holding a closed file.

        Reference: review 0007; a store that is a file, and one whose
        listing is refused, are both unknown, so the search is referred.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work, policy = store_work(tmp)
            grep = {"pattern": "x", "path": work}
            with mock.patch.object(
                guard.os, "listdir", side_effect=PermissionError
            ):
                found = in_work(work, policy, "Grep", grep)
            self.assertEqual(found, {"read-bounds"})
        with tempfile.TemporaryDirectory() as tmp:
            work = str(Path(tmp).resolve())
            Path(f"{work}/secrets").write_text("x", encoding="utf-8")
            policy = {
                **POLICY,
                "work": work,
                "writable": [work, "/dev/null"],
                "store": f"{work}/secrets",
                "secrets": [],
            }
            grep = {"pattern": "x", "path": work}
            self.assertEqual(
                in_work(work, policy, "Grep", grep), {"read-bounds"}
            )

    def test_search_inside_and_hidden(self) -> None:
        """Behavior: Grep on a directory under the store, with a glob or
        not, reaches read-bounds; a hidden closed file counts.

        Reference: unit 0007 criterion 3; STND.DFLT.31.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work, policy = store_work(tmp)
            Path(f"{work}/secrets/sub").mkdir()
            sub = {"pattern": "x", "path": f"{work}/secrets/sub"}
            self.assertEqual(
                in_work(work, policy, "Grep", sub), {"read-bounds"}
            )
            Path(f"{work}/secrets/key").unlink()
            Path(f"{work}/secrets/sub").rmdir()
            top = {"pattern": "x", "path": work, "glob": "*.py"}
            self.assertEqual(in_work(work, policy, "Grep", top), set())
            Path(f"{work}/secrets/.key").write_text("x", encoding="utf-8")
            self.assertEqual(
                in_work(work, policy, "Grep", top), {"read-bounds"}
            )

    def test_no_store(self) -> None:
        """Behavior: without a store, a directory named secrets is part
        of the work.

        Reference: STND.DFLT.29 applies only where the human owner
        provides a store.
        """
        key = {"file_path": f"{WORK}/secrets/key"}
        self.assertEqual(outcomes_of("Read", key), set())
        self.assertEqual(outcomes_of("Write", key), set())

    def test_policy_needs_the_fields(self) -> None:
        """Behavior: a policy without the store fields is refused.

        Reference: the guard reads a policy rendered with it; a stale
        policy must not open the store by its silence.
        """
        for name in ("store", "secrets"):
            with self.subTest(name=name):
                stale = {k: v for k, v in POLICY.items() if k != name}
                with self.assertRaises(KeyError):
                    guard.read_policy(stale)
        with self.assertRaises(ValueError):
            guard.read_policy({**POLICY, "store": None})


class Decisions(unittest.TestCase):
    """The answer follows the response of each outcome reached."""

    def test_refuse_wins(self) -> None:
        """Behavior: a call reaching a Refuse and a Refer outcome is
        denied.

        Reference: STND.HARN.18; Refuse is the stronger response.
        """
        policy = guard.read_policy(POLICY)
        found = guard.check_call(
            {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}},
            policy,
        )
        answer = guard.decide(found, policy)
        decision = answer["hookSpecificOutput"]["permissionDecision"]
        self.assertEqual(decision, "deny")

    def test_refer_asks_or_denies_unattended(self) -> None:
        """Behavior: a Refer outcome asks, and is denied with a pointer to
        PRIME.14 when the session is unattended.

        Reference: decision 0002 and PRIME.14.
        """
        event = {"tool_name": "Bash", "tool_input": {"command": "rm -r b"}}
        attended = guard.read_policy(POLICY)
        alone = guard.read_policy({**POLICY, "unattended": True})
        ask = guard.decide(guard.check_call(event, attended), attended)
        deny = guard.decide(guard.check_call(event, alone), alone)
        self.assertEqual(ask["hookSpecificOutput"]["permissionDecision"],
                         "ask")
        self.assertEqual(deny["hookSpecificOutput"]["permissionDecision"],
                         "deny")
        self.assertIn("PRIME.14",
                      deny["hookSpecificOutput"]["permissionDecisionReason"])

    def test_unlisted_outcome_fails_closed(self) -> None:
        """Behavior: an outcome the policy lists no response for is
        refused.

        Reference: GUARD.2, the highest tier that can apply.
        """
        policy = guard.read_policy({**POLICY, "responses": {}})
        found = guard.Findings([("remote-write", "test")])
        answer = guard.decide(found, policy)
        self.assertEqual(answer["hookSpecificOutput"]["permissionDecision"],
                         "deny")

    def test_odd_input_fails_closed(self) -> None:
        """Behavior: input of the wrong form, or a call whose reading
        faults, is denied at every class, not guessed at or let through.

        Reference: PRIME.4 and DSGN.2, untrusted input is rejected where
        it enters. Before review 0003 a command given as a list was
        parsed as its text, an Edit with no ``file_path`` was checked as
        the working directory and passed, and a relative ``cwd``
        defeated every location check. Before review 0005 a command
        nested too deep to parse raised a fault that work that is not
        assured let through.
        """
        nested = "$(" * 2000 + "rm -rf /srv/work/.git" + ")" * 2000
        events = (
            {"tool_name": "Bash", "tool_input": {"command": ["rm"]}},
            {"tool_name": "Edit", "tool_input": {}},
            {"tool_name": "Bash", "tool_input": "rm -rf /"},
            {"tool_name": "Bash", "tool_input": {"command": "ls"},
             "cwd": "work"},
            {"tool_name": "Bash", "tool_input": {"command": nested}},
            [],
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.json"
            path.write_text(json.dumps(POLICY), encoding="utf-8")
            for event in events:
                for flag in ((), ("--assured",)):
                    with self.subTest(event=str(event)[:60], flag=flag):
                        out = io.StringIO()
                        stdin = io.StringIO(json.dumps(event))
                        with mock.patch("sys.stdin", stdin), \
                                redirect_stdout(out):
                            guard.main(["guard", str(path), *flag])
                        answer = json.loads(out.getvalue())
                        self.assertEqual(
                            answer["hookSpecificOutput"][
                                "permissionDecision"
                            ],
                            "deny",
                        )

    def test_long_command_is_referred(self) -> None:
        """Behavior: a command longer than ``MAX_COMMAND`` is referred
        unread.

        Reference: the hook's timeout of 10 s; a guard that does not
        answer in time lets the call proceed, so it must not try.
        """
        command = "echo " + "a" * guard.MAX_COMMAND
        self.assertEqual(shell(command), {"selective-destruction"})

    def test_glob_pattern_outside(self) -> None:
        """Behavior: a Glob pattern that leaves the bounds is referred.

        Reference: STND.DFLT.25. Before review 0003 only ``path`` was
        checked, so ``/home/*/.ssh/*`` from the work passed.
        """
        self.assertIn(
            "read-bounds",
            outcomes_of("Glob", {"pattern": "/home/*/.ssh/*"}),
        )
        self.assertEqual(outcomes_of("Glob", {"pattern": "**/*.py"}), set())

    def test_link_to_configuration(self) -> None:
        """Behavior: a write through a symbolic link is checked where
        the link leads.

        Reference: STND.DFLT.22; a link in the work to the settings of
        the work would otherwise let a file tool change them.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp).resolve()
            (work / ".claude").mkdir()
            (work / ".claude" / "settings.json").write_text("{}")
            (work / "notes.json").symlink_to(work / ".claude/settings.json")
            policy = {
                **POLICY,
                "work": str(work),
                "writable": [str(work)],
                "configuration": [str(work / ".claude")],
            }
            found = outcomes_of(
                "Write", {"file_path": str(work / "notes.json")}, policy
            )
        self.assertIn("enforcing-configuration", found)

    def test_policy_fault_by_class(self) -> None:
        """Behavior: a missing policy denies the call for assured work and
        lets it proceed, with a notice to the owner and the agent, for
        other work; both answer with exit 0.

        Reference: STND.HARN.23 and PRIME.4, a fault never passes
        silently.
        """
        answers = {}
        with tempfile.TemporaryDirectory() as tmp:
            missing = str(Path(tmp) / "absent.json")
            for flag in ((), ("--assured",)):
                out = io.StringIO()
                with mock.patch("sys.stdin", io.StringIO("{}")), \
                        redirect_stdout(out):
                    status = guard.main(["guard", missing, *flag])
                self.assertEqual(status, 0)
                answers[bool(flag)] = json.loads(out.getvalue())
        decision = answers[True]["hookSpecificOutput"]["permissionDecision"]
        self.assertEqual(decision, "deny")
        other = answers[False]
        self.assertNotIn("permissionDecision", other["hookSpecificOutput"])
        self.assertIn("unguarded", other["systemMessage"])
        self.assertIn(
            "STND.HARN.23", other["hookSpecificOutput"]["additionalContext"]
        )


if __name__ == "__main__":
    unittest.main()
