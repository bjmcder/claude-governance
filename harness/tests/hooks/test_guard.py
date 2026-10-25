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



def assert_reaches(
    case: unittest.TestCase, outcome: str, commands: tuple
) -> None:
    """Assert that each command reaches an outcome, one subtest each.

    Parameters
    ----------
    case : unittest.TestCase
        The test.
    outcome : str
        Key of the outcome.
    commands : tuple
        Command lines.
    """
    for command in commands:
        with case.subTest(command=command):
            case.assertIn(outcome, shell(command))


class CommentsAndContinuations(unittest.TestCase):
    """QA.8 H1: a comment or a joined line hides nothing that follows."""

    def test_comment_before_a_later_line(self) -> None:
        """Behavior: a command on the line after a comment is read.

        Reference: QA.8 part A, H1; bash ends a comment at the newline
        and runs the next line (checked in a scratch directory). Before
        unit 0015 each reached no outcome.
        """
        assert_reaches(self, "elevated-privilege", ("ls # note\nsudo id",))
        assert_reaches(
            self,
            "history-rewrite",
            ("ls # note\ngit push --force origin main",),
        )
        assert_reaches(
            self, "record-entries", ("ls # note\nrm /srv/work/ledger.jsonl",)
        )

    def test_hash_inside_a_word(self) -> None:
        """Behavior: a ``#`` that does not begin a word starts no comment.

        Reference: QA.8 part A, H1; bash prints ``a#b``, ``$#``, and
        ``${#x}`` and runs the command after the ``;``.
        """
        assert_reaches(
            self, "record-entries", ("echo a#b; rm /srv/work/ledger.jsonl",)
        )
        assert_reaches(
            self,
            "elevated-privilege",
            ("echo $#; sudo id", "echo ${#x}; sudo id"),
        )

    def test_line_continuation(self) -> None:
        """Behavior: a backslash before a newline joins the two lines.

        Reference: QA.8 part A, H1; bash runs ``sud\\<newline>o id`` as
        ``sudo id``, and ``w\\<newline>#x`` is the word ``w#x``, so the
        ``#`` there starts no comment.
        """
        assert_reaches(
            self,
            "elevated-privilege",
            ("sud\\\no id", "echo w\\\n#x; sudo id"),
        )
        assert_reaches(
            self, "record-entries", ("rm /srv/work/ledg\\\ner.jsonl",)
        )
        assert_reaches(
            self, "history-rewrite", ("git pu\\\nsh --force origin main",)
        )

    def test_quoted_hash_and_continuation(self) -> None:
        """Behavior: a quoted ``#`` is text, and a backslash before a
        newline inside single quotes or ``$'...'`` stays.

        Reference: bash, checked in a scratch directory: ``echo $'a\\
        <newline>b'`` keeps the backslash.
        """
        self.assertEqual(shell("echo '# not a comment'"), set())
        self.assertEqual(shell("echo 'sud\\\no id'"), set())


class GitAliases(unittest.TestCase):
    """QA.8 H2: an alias does not hide what git runs."""

    def test_alias_given_in_the_call(self) -> None:
        """Behavior: ``git -c alias.NAME=...`` is referred, since the
        alias is no command of git, and so is a setting taken from a
        variable, which may name a program git runs.

        Reference: QA.8 part A, H2; the reviewer ran the first against a
        local bare repository and the forced update went through. The
        command an alias stands for is read too (review of unit 0015,
        N8), so a forced push or a rebase through one is refused.
        """
        assert_reaches(
            self,
            "history-rewrite",
            (
                "git -c alias.p=push p --force origin main",
                "git -c alias.q=rebase q -i HEAD~3",
            ),
        )
        self.assertIn(
            "selective-destruction",
            shell("git --config-env=core.pager=PAGER log"),
        )
        assert_reaches(
            self,
            "selective-destruction",
            (
                "git -c alias.p=push p --force origin main",
                "git -c alias.p=push p origin +main",
                "git -c alias.q=rebase q -i HEAD~3",
            ),
        )

    def test_alias_set_by_an_earlier_call(self) -> None:
        """Behavior: ``git config alias.p push`` is referred, and so is
        any subcommand that is not a command of git, such as ``p``.

        Reference: QA.8 part A, H2; two calls did what one cannot.
        """
        assert_reaches(
            self,
            "selective-destruction",
            ("git config alias.p push", "git p --force origin main"),
        )

    def test_plain_settings_pass(self) -> None:
        """Behavior: reading the configuration, and setting the name or
        mail of the author, reach no outcome.

        Reference: decision 0002, routine work runs without a prompt.
        """
        for command in (
            "git config user.email a@b.c",
            "git config --get remote.origin.url",
            "git config -l",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class UnquotedHereDocuments(unittest.TestCase):
    """QA.8 H3: the shell runs substitutions in an unquoted body."""

    def test_substitution_in_the_body(self) -> None:
        """Behavior: ``$(...)`` and backquotes in the body of a
        here-document whose delimiter is not quoted are read.

        Reference: QA.8 part A, H3; bash expands such a body (checked in
        a scratch directory).
        """
        assert_reaches(
            self,
            "elevated-privilege",
            (
                "cat <<EOF\n$(sudo id)\nEOF",
                "cat <<EOF\n`sudo id`\nEOF",
                "cat <<-EOF\n\t$(sudo id)\n\tEOF",
                "echo ok <<EOF\n$(sudo id)\nEOF",
            ),
        )
        assert_reaches(
            self,
            "record-entries",
            ("cat <<EOF\n$(rm /srv/work/ledger.jsonl)\nEOF",),
        )

    def test_quoted_delimiter_is_data(self) -> None:
        """Behavior: the body of a here-document whose delimiter is
        quoted runs nothing.

        Reference: QA.8 part A, H3; bash does not expand it.
        """
        for command in (
            "cat <<'EOF'\n$(sudo id)\nEOF",
            'cat <<"EOF"\n`sudo id`\nEOF',
            "cat <<\\EOF\n$(sudo id)\nEOF",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class WorkBound(unittest.TestCase):
    """QA.8 H4: the guard answers within its own budget."""

    SLOW = (
        ";".join(f"cd /tmp/d{i}" for i in range(15))
        + "; rm "
        + " ".join(["x/{a,b}{c,d}{e,f}{g,h}{i,j}{k,l}"] * 300)
        + "; sudo id"
    )

    def test_too_many_paths_is_referred(self) -> None:
        """Behavior: a line that resolves more than ``MAX_PATHS`` paths
        is referred as too large to read, well inside the timeout.

        Reference: QA.8 part A, H4, the reviewer's ``slow2.py`` input of
        300 operands, which took 6.7 s before unit 0015; the hook's
        timeout is 10 s, after which the call proceeds.
        """
        event = {"tool_name": "Bash", "tool_input": {"command": self.SLOW},
                 "cwd": WORK}
        started = guard.time.monotonic()
        found = guard.check_call(event, guard.read_policy(POLICY))
        spent = guard.time.monotonic() - started
        self.assertIn(
            ("selective-destruction",
             f"command too large to read: more than {guard.MAX_PATHS} paths"),
            found.reached,
        )
        self.assertLess(spent, guard.TIME_BUDGET + 2)

    def test_deadline_is_referred(self) -> None:
        """Behavior: a reading past its deadline stops and is referred.

        Reference: QA.8 part A, H4; the clock is made to pass the budget
        at once, so the test does not depend on the machine's speed.
        """
        clock = iter([0.0] + [guard.TIME_BUDGET + 1] * 100)
        with mock.patch.object(
            guard.time, "monotonic", side_effect=lambda: next(clock)
        ):
            found = shell("ls; ls")
        self.assertEqual(found, {"selective-destruction"})

    def test_assured_answer_is_never_silent(self) -> None:
        """Behavior: under the assured profile the slow line gets an
        answer that refers it, attended, and refuses it, unattended.

        Reference: STND.HARN.23, a call is refused where a program the
        guard runs fails; QA.8 part A, H4.
        """
        event = {"tool_name": "Bash", "tool_input": {"command": self.SLOW},
                 "cwd": WORK}
        for unattended, decision in ((False, "ask"), (True, "deny")):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "policy.json"
                policy = {**POLICY, "unattended": unattended}
                path.write_text(json.dumps(policy), encoding="utf-8")
                out = io.StringIO()
                stdin = io.StringIO(json.dumps(event))
                with mock.patch("sys.stdin", stdin), redirect_stdout(out):
                    guard.main(["guard", str(path), "--assured"])
            answer = json.loads(out.getvalue())["hookSpecificOutput"]
            with self.subTest(unattended=unattended):
                self.assertEqual(answer["permissionDecision"], decision)


class XargsCommands(unittest.TestCase):
    """QA.8 H5: a command fed through xargs is not left unread."""

    def test_launcher_or_replace_string(self) -> None:
        """Behavior: xargs whose program is a launcher, or is named by
        the replace string, is referred.

        Reference: QA.8 part A, H5; each reached no outcome.
        """
        # With the replace string "at", xargs runs "c" + "hmod" + ...,
        # chmod, though the program as written is cat.
        self.assertIn(
            "selective-destruction", shell("echo hmod | xargs -I at cat u+s f")
        )
        assert_reaches(
            self,
            "selective-destruction",
            (
                "echo sudo id | xargs env",
                "echo sudo | xargs -I@ @ id",
                'echo "rm /srv/work/ledger.jsonl" | xargs env',
                'echo "rm /srv/work/ledger.jsonl" | xargs nice',
            ),
        )

    def test_readers_pass(self) -> None:
        """Behavior: xargs feeding a program that only reads passes.

        Reference: decision 0002; these change nothing.
        """
        for command in (
            "find . -name '*.py' | xargs grep -l TODO",
            "find . -name '*.py' | xargs wc -l",
            "ls | xargs -I{} echo {}",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class LinkThenParent(unittest.TestCase):
    """QA.8 H6: ``..`` after a symbolic link is resolved as the system does."""

    def test_writes_through_link_and_parent(self) -> None:
        """Behavior: a write to ``l/../evil``, where ``l`` leads out of
        the work, reaches write-bounds, by the shell and by Write.

        Reference: QA.8 part A, H6; the system resolves ``l/..`` as the
        parent of the link's target, and in a scratch directory
        ``echo x > l/../evil`` wrote ``outside/evil``.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            work, deep = root / "work", root / "outside" / "deep"
            work.mkdir()
            deep.mkdir(parents=True)
            (work / "l").symlink_to(deep)
            policy = {**POLICY, "work": str(work), "writable": [str(work)]}
            for command in (
                "echo x > l/../evil",
                "touch l/../evil",
                "rm l/../evil",
                "cp a l/../evil",
            ):
                with self.subTest(command=command):
                    found = in_work(
                        str(work), policy, "Bash", {"command": command}
                    )
                    self.assertIn("write-bounds", found)
            data = {"file_path": str(work / "l/../evil")}
            found = in_work(str(work), policy, "Write", data)
            self.assertEqual(found, {"write-bounds"})
            inside = {"command": "echo x > sub/../notes.txt"}
            self.assertEqual(in_work(str(work), policy, "Bash", inside), set())


class PatternWrites(unittest.TestCase):
    """QA.8 H7: a pattern in a write target reaches what it may match."""

    def test_pattern_reaches_protected_names(self) -> None:
        """Behavior: a pattern that may match a ledger or a file of
        ``.git`` reaches record-entries or history-rewrite.

        Reference: QA.8 part A, H7; bash expands a pattern in a
        redirection that matches one file, and in a scratch directory
        ``echo hi > ledger.json?`` overwrote ``ledger.jsonl``, as did
        ``ledger.jso[^x]l``.
        """
        assert_reaches(
            self,
            "record-entries",
            (
                "echo x > /srv/work/ledger.json?",
                "cp /dev/null /srv/work/ledger.jso[n]l",
                "tee /srv/work/ledg*.jsonl",
                "echo x > /srv/work/ledger.jso[^x]l",
            ),
        )
        assert_reaches(
            self,
            "history-rewrite",
            (
                "echo x > /srv/work/.gi?/config",
                "echo x > /srv/work/.g*/hooks/pre-push",
            ),
        )
        self.assertIn(
            "enforcing-configuration", shell("echo x > /srv/work/.cl*/s.json")
        )

    def test_ordinary_patterns_pass(self) -> None:
        """Behavior: a pattern that matches no protected name passes.

        Reference: decision 0002; an edit or mode change over the
        sources is routine.
        """
        for command in ("chmod +x scripts/*.sh", "sed -i 's/a/b/' src/*.py"):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class OperandPositions(unittest.TestCase):
    """QA.8 M1: the script and mode options leave the files in view."""

    def test_script_and_reference_options(self) -> None:
        """Behavior: the file of ``sed -i`` with a joined or long
        script option, and of ``chmod --reference``, is checked.

        Reference: QA.8 part A, M1; each dropped ``/etc/passwd``.
        """
        assert_reaches(
            self,
            "write-bounds",
            (
                "sed -i --expression=s/a/b/ /etc/passwd",
                "sed -i -es/a/b/ /etc/passwd",
                "chmod --reference=a /etc/passwd",
            ),
        )

    def test_script_is_no_file(self) -> None:
        """Behavior: a script such as ``/x/d`` is not read as a path.

        Reference: GNU sed takes the first operand as the script when
        no option gives one.
        """
        self.assertEqual(shell("sed -i '/x/d' notes.txt"), set())
        self.assertEqual(shell("sed -i -e '/x/d' notes.txt"), set())


class SetIdModes(unittest.TestCase):
    """QA.8 M2: every form of a set-user or set-group mode is seen."""

    def test_setid_modes(self) -> None:
        """Behavior: a five-digit octal mode and ``u+rs`` or ``u+xs``
        reach elevated-privilege; ``755`` and ``u+x`` do not.

        Reference: QA.8 part A, M2; in a scratch directory both forms
        set the bit.
        """
        assert_reaches(
            self,
            "elevated-privilege",
            ("chmod 04755 f", "chmod u+rs f", "chmod u+xs f"),
        )
        for command in ("chmod 755 f", "chmod u+x,go-w f", "chmod -w f"):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class RemoteSpellings(unittest.TestCase):
    """QA.8 M3: common spellings of a remote write are recognized."""

    def test_remote_spellings(self) -> None:
        """Behavior: each spelling reaches remote-write.

        Reference: QA.8 part A, M3; each reached no outcome.
        """
        assert_reaches(
            self,
            "remote-write",
            (
                "curl -dx https://pypi.org",
                "curl -sd x https://pypi.org",
                "curl -XPOST https://pypi.org",
                "curl -Fa=@f https://pypi.org",
                "curl -Tf https://pypi.org",
                "curl --form-string a=b https://pypi.org",
                "curl -K cfg",
                "ssh host < script.sh",
                "nc host 80",
                "socat - TCP:host:80",
                "gh secret set X",
                "gh label create x",
                "poetry publish",
                "uv publish",
                "git send-email a.patch",
            ),
        )
        # An external command of git is referred as one the guard does
        # not read (H2), which holds the push of git lfs too.
        self.assertIn(
            "selective-destruction", shell("git lfs push origin main")
        )

    def test_reads_pass(self) -> None:
        """Behavior: a plain fetch and the read commands of gh pass.

        Reference: decision 0002; these write nothing remote.
        """
        for command in (
            "curl -sSL https://pypi.org/simple/x/",
            "curl -fsSLo /tmp/x.tgz https://pypi.org/x.tgz",
            "curl -I -H 'Accept: text/html' https://pypi.org",
            "gh pr view 12",
            "gh run list",
            "gh auth status",
            "ssh -T git@github.example",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class StoreReads(unittest.TestCase):
    """QA.8 M4: reads of the store by more programs are seen."""

    def test_reads_of_the_store(self) -> None:
        """Behavior: each program that reads a closed file of the store,
        or takes the store in whole, reaches read-bounds.

        Reference: QA.8 part A, M4; with a store holding a closed and an
        opened file, each reached no outcome.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work, policy = store_work(tmp)
            for command in (
                "grep x secrets/key",
                "grep -r x secrets",
                "sed p secrets/key",
                "awk 1 secrets/key",
                "base64 secrets/key",
                "dd if=secrets/key",
                "find secrets -exec cat {} +",
                "find secrets -exec python3 show.py {} +",
                "tar cf x.tar secrets",
                "rsync -a secrets/ /tmp/k",
                "install -D secrets/key /tmp/k",
            ):
                with self.subTest(command=command):
                    found = in_work(work, policy, "Bash", {"command": command})
                    self.assertIn("read-bounds", found)
            ordinary = {"command": "grep x secrets/token"}
            self.assertEqual(in_work(work, policy, "Bash", ordinary), set())


class WriteDestinations(unittest.TestCase):
    """QA.8 M5: the destination of more writing programs is checked."""

    def test_destinations_outside(self) -> None:
        """Behavior: each destination outside the work reaches
        write-bounds, and ``gzip`` of the ledger reaches record-entries.

        Reference: QA.8 part A, M5; each reached no outcome.
        """
        assert_reaches(
            self,
            "write-bounds",
            (
                "rsync a /etc/x",
                "tar xf a.tar -C /etc",
                "curl -o /etc/x https://pypi.org",
                "wget -O /etc/x https://pypi.org",
                "sort -o /etc/x a",
                "git archive --output=/etc/x HEAD",
                "git config --file /etc/x a.b c",
                "git config --global alias.p push",
                "git init /etc/foo",
                "git clone https://git.example/x /etc/foo",
                "git worktree add /etc/wt",
                "find . -fprint /etc/x",
            ),
        )
        assert_reaches(
            self, "record-entries", ("gzip /srv/work/ledger.jsonl",)
        )


class GitDestructiveForms(unittest.TestCase):
    """QA.8 M6: destructive git forms outside the earlier list."""

    def test_destructive_forms(self) -> None:
        """Behavior: each form reaches selective-destruction or
        history-rewrite.

        Reference: QA.8 part A, M6; the reviewer ran the first, which
        removed an untracked file since the last option wins.
        """
        assert_reaches(
            self,
            "selective-destruction",
            (
                "git clean -n --no-dry-run -f",
                "git restore --staged --worktree .",
            ),
        )
        # Referred, not refused: see the review of unit 0015 in
        # record 0015, and ``check_reset``.
        assert_reaches(
            self,
            "selective-destruction",
            (
                "git reset --keep HEAD~5",
                "git reset HEAD~1",
                "git reset --soft HEAD^",
            ),
        )
        assert_reaches(
            self,
            "history-rewrite",
            (
                "git branch -m a b",
                "git symbolic-ref HEAD refs/heads/x",
                "git fast-import",
            ),
        )

    def test_unstaging_passes(self) -> None:
        """Behavior: unstaging by ``reset`` or ``restore --staged``, and
        reading ``HEAD`` by ``symbolic-ref``, reach no outcome.

        Reference: decision 0002.
        """
        for command in (
            "git reset",
            "git reset HEAD file.txt",
            "git reset -- file.txt",
            "git reset .",
            "git reset src/",
            "git restore --staged file.txt",
            "git symbolic-ref HEAD",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


class LowFindings(unittest.TestCase):
    """QA.8 L1 and L2: CDPATH, and sourcing what the call gives."""

    def test_cdpath(self) -> None:
        """Behavior: after a line sets ``CDPATH``, a ``cd`` to a relative
        name leads to a directory the guard cannot tell.

        Reference: QA.8 part A, L1. The line itself was referred before
        unit 0015 too, but only because a relative ``cd``, read again on
        each pass, grows the directories to ``MAX_DIRECTORIES``; the
        rule is therefore also held on one ``cd``.
        """
        self.assertIn(
            "selective-destruction",
            shell("CDPATH=/etc:. ; cd ssl; echo x > cert"),
        )
        policy = guard.read_policy(POLICY)
        for assigned, expected in (({"CDPATH"}, None), (set(), f"{WORK}/ssl")):
            scan = guard.Scan(
                policy, guard.Findings(), [WORK], "/home/agent", assigned
            )
            guard.enter_directory("ssl", scan)
            with self.subTest(assigned=assigned):
                self.assertEqual(scan.cwds, [WORK, expected])

    def test_sourced_and_substituted_scripts(self) -> None:
        """Behavior: a sourced standard input is read, and a shell or
        ``source`` that runs a process substitution is referred.

        Reference: QA.8 part A, L2.
        """
        self.assertIn(
            "elevated-privilege", shell(". /dev/stdin <<< 'sudo id'")
        )
        assert_reaches(
            self,
            "selective-destruction",
            ("bash <(echo sudo id)", "source <(echo sudo id)"),
        )
        self.assertEqual(shell("diff <(sort a) <(sort b)"), set())
        self.assertEqual(shell("source .venv/bin/activate"), set())


class OrdinaryWork(unittest.TestCase):
    """Unit 0015 adds no friction to ordinary work (design rule 2)."""

    def test_ordinary_commands(self) -> None:
        """Behavior: ordinary agent commands reach no outcome.

        Reference: decision 0002, routine work runs without a prompt.
        ``rm -r build`` stays referred, by STND.INSTR.4, as before.
        """
        for command in (
            "# Build and test\nmake\n# then lint\nruff check .",
            "cd src  # into the sources\npython3 -B -m unittest",
            "grep -rn TODO src/",
            "sed -n '1,20p' README.md",
            "curl -s https://pypi.org/pypi/x/json | head",
            "git status",
            "git log --oneline -5",
            "git diff HEAD~1 -- src",
            "git add -A && git commit -m 'Fix #12'",
            "git commit -m \"$(cat <<'EOF'\nFix: don't break\nEOF\n)\"",
            "cat > notes.md <<'EOF'\n$(sudo id) `rm -rf /`\nEOF",
            "rm build/a.o build/b.o",
            "rmdir build",
            "cp a.txt b.txt",
            "cp -r src backup",
            "echo $(( 1 + 2 )) # sum",
            "tar czf /tmp/out.tgz src",
            "uv run pytest -q",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())



class ReviewOfUnit0015(unittest.TestCase):
    """The findings of the review of unit 0015 (N1 to N8)."""

    def test_hash_after_an_escape(self) -> None:
        """Behavior: a ``#`` after an escaped character starts no comment
        in the guard's reading, and the line is referred as uncertain.

        Reference: review of unit 0015, N1; bash prints ``a #x`` for
        ``echo a\\ #x`` and runs the command after the ``;``.
        """
        for command in (
            "echo a\\ #x; sudo id",
            "echo \\;#x; sudo id",
            "echo \\(#x; sudo id",
            "echo \\ #x; sudo id",
            "echo $x\\ #c; sudo id",
            "echo a\\ #$(sudo id)",
        ):
            with self.subTest(command=command):
                found = shell(command)
                self.assertIn("elevated-privilege", found)
                self.assertIn("selective-destruction", found)

    def test_comment_in_backquotes(self) -> None:
        """Behavior: a comment inside backquotes hides nothing after the
        closing one, and the line is referred as uncertain.

        Reference: review of unit 0015, N2; ``bash -c 'echo `echo A #
        x`; echo B'`` prints A and B.
        """
        assert_reaches(
            self,
            "elevated-privilege",
            ("echo `ls # x`; sudo id", "x=`ls # y`; sudo id"),
        )
        assert_reaches(
            self,
            "record-entries",
            ("echo `echo a # x`; rm /srv/work/ledger.jsonl",),
        )
        self.assertEqual(shell("echo `date`"), set())
        # Read correctly, the line is still referred as uncertain.
        self.assertEqual(shell("echo `ls # x`"), {"selective-destruction"})
        self.assertEqual(shell("echo $(ls # x\n)"), {"selective-destruction"})

    def test_case_in_a_substitution(self) -> None:
        """Behavior: ``case`` inside a command substitution, in a line,
        in double quotes, or in a here-document, and a comment inside
        one in a here-document, are referred.

        Reference: review of unit 0015, N3; the first was a regression
        from main, whose reading reached elevated-privilege.
        """
        assert_reaches(
            self,
            "selective-destruction",
            (
                "echo $(case x in x) sudo id;; esac)",
                "echo $(case x in x|y) sudo id;; esac)",
                "echo $(case x in *) sudo id;; esac)",
                "echo $(case x in x) sudo id ;; esac)",
                "echo $(case x in x) rm /srv/work/ledger.jsonl;; esac)",
                'echo "$(case x in x) sudo id;; esac)"',
                "cat <<EOF\n$(case x in x) sudo id;; esac)\nEOF",
                "cat <<EOF\n$(echo hi # )\nsudo id)\nEOF",
            ),
        )

    def test_second_reading(self) -> None:
        """Behavior: a line whose second, simpler reading finds a known
        program that the first did not read is referred.

        Reference: review of unit 0015, design rule. The first reading
        is made to lose the text after a ``#``, as a mistake in it
        would, so that the second reading alone is held.
        """
        plain = guard.lift_heredocs

        def lossy(
            text: str, bodies: list, expanded: list, doubts: list
        ) -> tuple[str, str]:
            """Lift a line, then drop all of it after its first ``#``.

            Parameters
            ----------
            text : str
                A command line.
            bodies : list
                Receives each body.
            expanded : list
                Receives each expanded body's index.
            doubts : list
                Receives each doubt.

            Returns
            -------
            tuple[str, str]
                The shortened line, and the line with its comments.
            """
            _, kept = plain(text, bodies, expanded, doubts)
            return kept.split("#")[0], kept

        with mock.patch.object(guard, "lift_heredocs", lossy):
            found = shell("echo ok # note\nsudo id")
        self.assertEqual(found, {"selective-destruction"})
        starts = guard.command_starts("echo a # b; rm x\nls; sudo id `cat`")
        self.assertEqual(starts, ["echo", "ls", "sudo", "cat"])

    def test_posix_brackets_and_links(self) -> None:
        """Behavior: a POSIX bracket expression in a write target is
        referred, and a pattern that matches a link to ``.git`` writes
        version-control files.

        Reference: review of unit 0015, N4; in a scratch directory bash
        overwrote ``ledger.jsonl`` with each bracket form.
        """
        assert_reaches(
            self,
            "selective-destruction",
            (
                "echo x > ledger.[[:alpha:]]sonl",
                "echo x > ledger.[[.j.]]sonl",
                "echo x > ledger.[[=j=]]sonl",
                "echo x > ledger.json[[:lower:]]",
            ),
        )
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp).resolve()
            (work / ".git").mkdir()
            (work / ".git" / "config").write_text("", encoding="utf-8")
            (work / "g").symlink_to(work / ".git")
            (work / "g2").symlink_to(work / "g")
            policy = {**POLICY, "work": str(work), "writable": [str(work)]}
            for command in ("echo x > g?/config", "echo x > g*/config"):
                with self.subTest(command=command):
                    found = in_work(
                        str(work), policy, "Bash", {"command": command}
                    )
                    self.assertIn("history-rewrite", found)

    def test_shell_fed_and_programs_run(self) -> None:
        """Behavior: a shell fed by a process substitution, ``rg
        --pre``, and git's output options are seen.

        Reference: review of unit 0015, N5; the xargs form was a
        regression from main.
        """
        assert_reaches(
            self,
            "selective-destruction",
            (
                "sh < <(echo sudo id)",
                "bash <<< \"$(echo sudo id)\"",
                "rg --pre 'sudo id' foo",
                "rg --pre=sudo foo",
                "echo x | xargs rg --pre sudo foo",
                "echo --pre=sudo | xargs rg foo",
            ),
        )
        assert_reaches(
            self,
            "record-entries",
            (
                "git log --output=ledger.jsonl",
                "git diff --output=ledger.jsonl",
                "git show -o ledger.jsonl",
                "git bundle create ledger.jsonl HEAD",
                "git merge-file ledger.jsonl a b",
            ),
        )
        assert_reaches(
            self,
            "write-bounds",
            (
                "git format-patch -o /etc/x HEAD~1",
                "git bugreport -o /etc/x",
                "git fast-export --export-marks=/etc/x HEAD",
                "git init --separate-git-dir=/etc/x",
            ),
        )
        self.assertEqual(shell("git log -p --stat -5"), set())

    def test_surviving_mutants(self) -> None:
        """Behavior: a joined ``$(`` in an unquoted body, the replace
        string of ``xargs -i`` and ``--replace``, and the lexical reading
        of ``cd l/..`` are each held.

        Reference: review of unit 0015, N6; each mutation survived.
        """
        self.assertIn(
            "elevated-privilege", shell("cat <<EOF\n$\\\n(sudo id)\nEOF")
        )
        assert_reaches(
            self,
            "selective-destruction",
            (
                "echo hmod | xargs -iat cat u+s f",
                "echo hmod | xargs --replace=at cat u+s f",
            ),
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            work, deep = root / "work", root / "outside" / "deep"
            (work / "records").mkdir(parents=True)
            deep.mkdir(parents=True)
            (work / "l").symlink_to(deep)
            policy = {
                **POLICY,
                "work": str(work),
                "writable": [str(work)],
                "protected": [str(work), f"{work}/records"],
            }
            (work / "sub").mkdir()
            # bash's cd reads ../l/.. lexically, from sub to the work, so
            # this removes the work's records; the system's reading would
            # lead outside.
            data = {"command": "cd ../l/.. && rm -rf records"}
            found = in_work(str(work / "sub"), policy, "Bash", data)
        self.assertIn("protected-locations", found)

    def test_store_reads(self) -> None:
        """Behavior: computed reads while the store is closed, and the
        reads of zip, xxd, openssl, and pattern files, reach read-bounds.

        Reference: review of unit 0015, N7.
        """
        with tempfile.TemporaryDirectory() as tmp:
            work, policy = store_work(tmp)
            for command in (
                "find secrets | xargs cat",
                "cat $(find secrets -type f)",
                "zip -r /tmp/z secrets",
                "xxd secrets/key",
                "grep -f secrets/key f",
                "sed -f secrets/key f",
                "awk -f secrets/key",
                "openssl enc -in secrets/key",
            ):
                with self.subTest(command=command):
                    found = in_work(work, policy, "Bash", {"command": command})
                    self.assertIn("read-bounds", found)
            plain = {"command": "find src | xargs cat"}
            policy_open = {**policy, "secrets": [f"{work}/secrets/token",
                                                 f"{work}/secrets/key"]}
            self.assertEqual(in_work(work, policy_open, "Bash", plain), set())

    def test_alias_named_like_a_script(self) -> None:
        """Behavior: an alias given in the call is read as the command
        it stands for, even where its name is a command of git.

        Reference: review of unit 0015, N8; where ``git-email`` is not
        installed, git takes the alias ``send-email``.
        """
        found = shell(
            "git -c alias.send-email=push send-email --force origin main"
        )
        self.assertIn("history-rewrite", found)
        self.assertIn("selective-destruction", found)



class LeftoverLows(unittest.TestCase):
    """The Lows of the review of unit 0015 that main also left unread."""

    def test_launcher_before_a_shell(self) -> None:
        """Behavior: a shell behind a launcher reads the standard input
        the launcher was given, so a pipe to it is referred and a
        here-string or here-document to it is read.

        Reference: second review of unit 0015; ``echo ... | env sh``
        runs what the pipe gives.
        """
        launchers = (
            "env", "nice", "command", "time", "timeout 5", "stdbuf -oL",
            "nohup", "setsid", "chrt -o 0", "ionice -c3", "taskset 1",
        )  # fmt: skip
        assert_reaches(
            self,
            "selective-destruction",
            tuple(f"echo sudo id | {launcher} sh" for launcher in launchers)
            + ("env sh < <(echo sudo id)",),
        )
        assert_reaches(
            self,
            "elevated-privilege",
            (
                "env sh -c 'sudo id'",
                "nice bash <<< 'sudo id'",
                "env bash <<EOF\nsudo id\nEOF",
            ),
        )

    def test_git_program_variables(self) -> None:
        """Behavior: a variable of git set in the call is referred, and
        its value read, unless it names only an author or committer; the
        value of a pager or editor variable is read as a command line.

        Reference: second review of unit 0015; git runs the program each
        names. Unit 0014 admits GIT_EDITOR, GIT_SEQUENCE_EDITOR, and
        GIT_PAGER in the guard's environment, since a push runs none.
        """
        for command in (
            "GIT_SSH_COMMAND='sudo id' git fetch",
            "GIT_PROXY_COMMAND='sudo id' git fetch",
            "GIT_EXTERNAL_DIFF='sudo id' git diff",
            "GIT_ASKPASS='sudo id' git fetch",
            "env GIT_SSH_COMMAND='sudo id' git fetch",
            "export GIT_SSH_COMMAND='sudo id'; git fetch",
        ):
            with self.subTest(command=command):
                found = shell(command)
                self.assertIn("selective-destruction", found)
                self.assertIn("elevated-privilege", found)
        self.assertEqual(
            shell("GIT_EDITOR='sudo id' git commit"), {"elevated-privilege"}
        )
        found = shell("GIT_ALLOW_PROTOCOL=ext git fetch x")
        self.assertIn("selective-destruction", found)

    def test_text_arguments_assign_nothing(self) -> None:
        """Behavior: the arguments of a program that takes only text,
        such as grep, are not read as assignments; one in front of it
        still is.

        Reference: second review of unit 0015; decision 0002, a search
        for a variable's name runs without a prompt.
        """
        for command in (
            "grep -rn GIT_SSH_COMMAND= .",
            "echo GIT_DIR=x",
            "rg 'EDITOR=sudo id' src",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())
        found = shell("GIT_SSH_COMMAND='sudo id' grep x f")
        self.assertIn("selective-destruction", found)
        self.assertIn("elevated-privilege", found)
        self.assertIn(
            "selective-destruction", shell("make GIT_SSH_COMMAND=ssh")
        )

    def test_git_program_settings(self) -> None:
        """Behavior: a setting given by ``git -c`` that may name a
        program or a transport is referred, and its value read.

        Reference: second review of unit 0015.
        """
        for command in (
            "git -c core.sshCommand='sudo id' fetch",
            "git -c core.fsmonitor='sudo id' status",
            "git -c diff.external='sudo id' diff",
        ):
            with self.subTest(command=command):
                found = shell(command)
                self.assertIn("selective-destruction", found)
                self.assertIn("elevated-privilege", found)
        assert_reaches(
            self,
            "selective-destruction",
            (
                "git -c core.sshCommand=ssh fetch",
                "git -c diff.x.textconv=cat diff",
                "git -c protocol.allow=always fetch x",
                "git -c protocol.ext.allow=always fetch x",
            ),
        )
        self.assertEqual(
            shell("git -c core.pager='sudo id' log"), {"elevated-privilege"}
        )

    def test_git_program_settings_read_strictly(self) -> None:
        """Behavior: the value of a pager or editor setting is read as a
        command line, so one that does not tokenize is referred, while a
        plain setting with the same value reaches no outcome.

        Reference: second review of unit 0015; git hands the value to
        a shell.
        """
        assert_reaches(
            self,
            "selective-destruction",
            (
                "git -c core.pager='\"' log",
                "git -c core.editor='\"' commit",
                "git -c pager.log='\"' log",
            ),
        )
        self.assertEqual(shell("git -c user.name='\"' log"), set())

    def test_transports_that_run_programs(self) -> None:
        """Behavior: an ``ext::`` or ``fd::`` URL, and a transport program
        named by an option, are referred, and a command they hold read.

        Reference: second review of unit 0015; ``git clone 'ext::sudo
        id'`` runs ``sudo id``.
        """
        assert_reaches(
            self,
            "selective-destruction",
            ("git push ext::x main", "git clone fd::3 x"),
        )
        for command in (
            "git clone 'ext::sudo id'",
            "git fetch 'ext::sh -c sudo% id'",
            "git remote add evil 'ext::sudo id'",
            "git clone --upload-pack='sudo id' x y",
            "git clone -u 'sudo id' x y",
            "git push --receive-pack='sudo id' origin main",
            "git archive --exec='sudo id' --remote=x HEAD",
        ):
            with self.subTest(command=command):
                found = shell(command)
                self.assertIn("selective-destruction", found)
                self.assertIn("elevated-privilege", found)

    def test_writers_of_standard_input(self) -> None:
        """Behavior: ``sponge`` and ``ed`` write the files they name;
        ``sponge -a`` only appends, as ``>>`` does.

        Reference: second review of unit 0015.
        """
        assert_reaches(
            self,
            "record-entries",
            (
                "echo x | sponge ledger.jsonl",
                "printf '1d\\nw\\n' | ed ledger.jsonl",
                "ex -s ledger.jsonl",
            ),
        )
        self.assertIn("write-bounds", shell("echo x | sponge /etc/x"))
        self.assertEqual(shell("echo x | sponge -a ledger.jsonl"), set())

    def test_ordinary_forms_pass(self) -> None:
        """Behavior: launchers, plain git settings and variables, and
        sponge within the work reach no outcome.

        Reference: decision 0002, routine work runs without a prompt.
        """
        for command in (
            "GIT_PAGER=cat git log -3",
            "GIT_AUTHOR_NAME=A git commit -m x",
            "git -c user.name=A -c user.email=a@b.c commit -m x",
            "git -c color.ui=false status",
            "git -c core.pager=cat log -3",
            "env FOO=1 python3 -m pytest",
            "time make",
            "nice -n 10 make -j4",
            "timeout 60 python3 -m pytest",
            "command -v sh",
            "echo x | sponge out.txt",
            "git clone https://git.example/x y",
            "git fetch origin",
        ):
            with self.subTest(command=command):
                self.assertEqual(shell(command), set())


if __name__ == "__main__":
    unittest.main()
