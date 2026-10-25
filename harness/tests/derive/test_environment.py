"""Tests of the environment derivation (STND.HARN.18 to STND.HARN.21).

The reference is the outcome table of STND.HARN.18 and the protected
locations of STND.INSTR.3 in the live corpus, read from a copy in
memory; the tests change that copy to show that an amendment of either
table reaches the configuration without a change of code. Agreement is
exact: the rendered text or JSON holds the stated value.
"""

from __future__ import annotations

import contextlib
import io
import json
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from govharness.cli.environment import HARNESS
from govharness.cli.main import main
from govharness.core.corpus import Corpus
from govharness.derive.environment import claude_code
from govharness.derive.environment.inputs import Inputs
from govharness.derive.environment.outcomes import read_outcomes
from govharness.workflows.environment import installed_problems
from tests.derive.test_authorizations import (
    IDENT,
    ROLE,
    frozen_clock,
    no_anchor,
    record,
    write_authorization,
)
from tests.support import corpus_copy, live_entries

INPUTS = Inputs(work="/srv/work", home="/home/agent", domains=("pypi.org",))


def live_corpus() -> Corpus:
    """Return an indexed copy of the live corpus held in memory.

    Returns
    -------
    Corpus
        A corpus that a test may change freely.
    """
    return Corpus(live_entries())


def rendered(corpus: Corpus, inputs: Inputs = INPUTS) -> dict:
    """Render the Claude Code files for a corpus.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    dict
        Text by path relative to the output directory.
    """
    return claude_code.render(corpus, inputs, "# guard\n")


class Derivation(unittest.TestCase):
    """The configuration follows the tables of governance."""

    def test_every_outcome_reaches_the_policy(self) -> None:
        """Behavior: each outcome of the table has its response in the
        guard's policy.

        Reference: the outcome table of STND.HARN.18 in the live corpus.
        """
        corpus = live_corpus()
        _, outcomes = read_outcomes(corpus)
        policy = json.loads(rendered(corpus)[claude_code.POLICY])
        self.assertEqual(
            policy["responses"], {o.key: o.response for o in outcomes}
        )

    def test_response_places_rules(self) -> None:
        """Behavior: a Refuse outcome's rules deny and a Refer outcome's
        ask; managed rules alone apply and the sandbox must start.

        Reference: STND.HARN.18; history-rewrite is Refuse and
        remote-write Refer in the live table.
        """
        settings = json.loads(rendered(live_corpus())[claude_code.SETTINGS])
        rules = settings["permissions"]
        self.assertIn("Bash(sudo *)", rules["deny"])
        self.assertIn("Bash(git push *)", rules["ask"])
        self.assertTrue(settings["allowManagedPermissionRulesOnly"])

    def test_sandbox_protects_settings(self) -> None:
        """Behavior: the sandbox denies shell writes to the settings and
        server lists, and the file tools are denied them too.

        Reference: STND.DFLT.22; the work is writable in the sandbox and
        holds ``.claude/`` and ``.mcp.json``, which can widen the sandbox
        or start a program outside it. Before review 0003 a program run
        by the shell could rewrite them.
        """
        settings = json.loads(rendered(live_corpus())[claude_code.SETTINGS])
        deny_write = settings["sandbox"]["filesystem"]["denyWrite"]
        for location in (
            "/srv/work/.claude",
            "/srv/work/.mcp.json",
            "/home/agent/.claude",
            "/home/agent/.claude.json",
        ):
            with self.subTest(location=location):
                self.assertIn(location, deny_write)
        deny = settings["permissions"]["deny"]
        self.assertIn("Edit(//srv/work/.mcp.json)", deny)
        self.assertIn("Edit(//srv/work/.claude/**)", deny)

    def test_hook_failure_by_class(self) -> None:
        """Behavior: run by the shell from the settings, a hook whose
        interpreter is missing exits 2, which blocks the call, for
        assured work; for other work it exits 0 with a notice for the
        human owner and the agent and no decision, so that the call
        proceeds. Only assured work needs the sandbox to start.

        Reference: STND.HARN.23; Claude Code treats exit 2 as blocking,
        reads JSON on stdout at exit 0, and applies its own rules where
        the answer holds no ``permissionDecision``.
        """
        for assured in (True, False):
            with self.subTest(assured=assured):
                inputs = Inputs(
                    work="/srv/work",
                    home="/home/agent",
                    domains=("pypi.org",),
                    assured=assured,
                )
                settings = json.loads(
                    rendered(live_corpus(), inputs)[claude_code.SETTINGS]
                )
                hook = settings["hooks"]["PreToolUse"][0]["hooks"][0]
                self.assertEqual(
                    settings["sandbox"]["failIfUnavailable"], assured
                )
                command = hook["command"].replace(
                    claude_code.PYTHON, "/nonexistent/python3", 1
                )
                run = subprocess.run(
                    ["/bin/sh", "-c", command],
                    input="{}",
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if assured:
                    self.assertEqual(run.returncode, 2)
                    self.assertEqual(run.stdout, "")
                    continue
                self.assertEqual(run.returncode, 0)
                answer = json.loads(run.stdout)
                self.assertIn("STND.HARN.23", answer["systemMessage"])
                specific = answer["hookSpecificOutput"]
                self.assertIn("STND.HARN.23", specific["additionalContext"])
                self.assertNotIn("permissionDecision", specific)

    def test_inputs_refused(self) -> None:
        """Behavior: a domain or tool pattern the guard would misread
        is refused.

        Reference: the guard compares lower-case hosts and matches
        patterns against ``mcp__`` tools; settings skip ``mcp__`` rules
        with parentheses.
        """
        for field, value in (
            ("domains", ("PyPI.org",)),
            ("tools", ("Bash",)),
            ("tools", ("mcp__x__y(z)",)),
        ):
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    Inputs(work="/w", home="/h", **{field: value})

    def test_amended_response_moves_rule(self) -> None:
        """Behavior: amending remote-write to Refuse moves its rule to
        deny without a change of code.

        Reference: decision 0002, outcomes live in governance.
        """
        corpus = live_corpus()
        holder = corpus.by_id["STND.HARN.18"]
        (row,) = [
            line
            for line in holder.body.splitlines()
            if line.startswith("| remote-write |")
        ]
        self.assertTrue(row.endswith("| Refer |"))
        refused = row.removesuffix("Refer |") + "Refuse |"
        holder.body = holder.body.replace(row, refused)
        rules = json.loads(rendered(corpus)[claude_code.SETTINGS])[
            "permissions"
        ]
        self.assertIn("Bash(git push *)", rules["deny"])
        self.assertNotIn("Bash(git push *)", rules["ask"])

    def test_unknown_outcome_is_not_covered(self) -> None:
        """Behavior: an outcome the adapter does not know is reported as
        enforced not at all.

        Reference: STND.HARN.19.
        """
        corpus = live_corpus()
        holder = corpus.by_id["STND.HARN.18"]
        holder.body = holder.body.rstrip("\n") + (
            "\n| new-outcome | Something new | GOV.48 | Refuse |\n"
        )
        report = rendered(corpus)[claude_code.COVERAGE]
        self.assertIn("| new-outcome | GOV.48 | Refuse | none |", report)

    def test_unmapped_location_is_a_gap(self) -> None:
        """Behavior: a protected location no rule maps is reported as a
        gap.

        Reference: STND.HARN.19 and the table of STND.INSTR.3.
        """
        corpus = live_corpus()
        holder = corpus.by_id["STND.INSTR.3"]
        holder.body = holder.body.rstrip("\n") + "\n| A new location |\n"
        report = rendered(corpus)[claude_code.COVERAGE]
        self.assertIn("Rows not mapped: A new location.", report)

    def test_entry_names_only_full_outcomes(self) -> None:
        """Behavior: the draft entry names only outcomes enforced in
        full, which for this adapter is none.

        Reference: STND.HARN.20, and the coverage table: every outcome
        has a gap (review 0003 found the one claimed full had one).
        """
        entry = json.loads(rendered(live_corpus())[claude_code.ENTRY])
        self.assertIn("in full by configuration the agent is unable to "
                      "alter: none.", entry["rationale"])
        self.assertEqual(entry["targets"], ["STND.DFLT.15"])
        self.assertEqual(entry["type"], "configure")

    def test_relative_path_refused(self) -> None:
        """Behavior: a relative work path is refused.

        Reference: a relative path moves with the caller, so the
        configuration would name no fixed location.
        """
        with self.assertRaises(ValueError):
            Inputs(work="work", home="/home/agent")


class SecretStore(unittest.TestCase):
    """The store of STND.DFLT.29 maps per file and authorization."""

    STORE = "/srv/work/secrets"
    WITH_STORE = Inputs(
        work="/srv/work", home="/home/agent", secrets=("token",)
    )

    def filesystem(self, inputs: Inputs) -> dict:
        """Return the sandbox's file system settings for some inputs.

        Parameters
        ----------
        inputs : Inputs
            The owner's statement of the environment.

        Returns
        -------
        dict
            The ``sandbox.filesystem`` object of the managed settings.
        """
        files = rendered(live_corpus(), inputs)
        settings = json.loads(files[claude_code.SETTINGS])
        return settings["sandbox"]["filesystem"]

    def test_names_refused(self) -> None:
        """Behavior: a secret name that is no file name of the store is
        refused.

        Reference: unit 0007 criterion 1; each name opens one file.
        """
        for name in ("", ".", "..", "a/b", "../key"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    Inputs(work="/w", home="/h", secrets=(name,))

    def test_no_store_leaves_settings(self) -> None:
        """Behavior: without a store the sandbox has no read rules and
        the policy names no store.

        Reference: unit 0007 criterion 1.
        """
        self.assertEqual(
            set(self.filesystem(INPUTS)), {"allowWrite", "denyWrite"}
        )
        self.assertNotIn(self.STORE, self.filesystem(INPUTS)["denyWrite"])
        policy = json.loads(rendered(live_corpus())[claude_code.POLICY])
        self.assertEqual((policy["store"], policy["secrets"]), ("", []))

    def test_store_in_sandbox_and_policy(self) -> None:
        """Behavior: with a store, the sandbox denies reads of its
        entries, allows the opened file, and denies every write in it;
        the policy names the store and the opened file; no permission
        rule names the store.

        Reference: unit 0007 criteria 2 and 4, and the documented rule
        that the narrower read path wins.
        """
        fs = self.filesystem(self.WITH_STORE)
        self.assertEqual(
            fs["denyRead"], [f"{self.STORE}/*", f"{self.STORE}/.*"]
        )
        self.assertEqual(fs["allowRead"], [f"{self.STORE}/token"])
        self.assertIn(self.STORE, fs["denyWrite"])
        self.assertEqual(fs["allowWrite"], ["/srv/work"])
        files = rendered(live_corpus(), self.WITH_STORE)
        policy = json.loads(files[claude_code.POLICY])
        self.assertEqual(policy["store"], self.STORE)
        self.assertEqual(policy["secrets"], [f"{self.STORE}/token"])
        rules = json.loads(files[claude_code.SETTINGS])["permissions"]
        for kind in ("allow", "ask", "deny"):
            with self.subTest(kind=kind):
                self.assertFalse([r for r in rules[kind] if "secrets" in r])

    def test_store_without_names(self) -> None:
        """Behavior: ``secret_store`` alone closes every file of the
        store.

        Reference: unit 0007 criterion 1; no file is opened.
        """
        inputs = Inputs(work="/srv/work", home="/h", secret_store=True)
        fs = self.filesystem(inputs)
        self.assertEqual(
            fs["denyRead"], [f"{self.STORE}/*", f"{self.STORE}/.*"]
        )
        self.assertEqual(fs["allowRead"], [])
        self.assertIn(self.STORE, fs["denyWrite"])

    def test_coverage_names_the_gaps(self) -> None:
        """Behavior: with a store, the rows of read-bounds and
        write-bounds state the store's gaps, and no row is full.

        Reference: unit 0007 criterion 5; STND.HARN.19.
        """
        files = rendered(live_corpus(), self.WITH_STORE)
        report = files[claude_code.COVERAGE]
        rows = {
            line.split("|")[1].strip(): line
            for line in report.splitlines()
            if line.startswith("| ") and "---" not in line
        }
        for key in ("read-bounds", "write-bounds"):
            with self.subTest(key=key):
                self.assertIn("While the sandbox runs", rows[key])
        self.assertIn("ignores case", rows["read-bounds"])
        self.assertIn("STND.DFLT.30", rows["write-bounds"])
        self.assertNotIn("| full |", report)
        plain = rendered(live_corpus())[claude_code.COVERAGE]
        self.assertNotIn("secret store", plain)

    def test_command_options(self) -> None:
        """Behavior: ``--secret`` reaches the settings, and a name with
        a slash exits 1 with a message.

        Reference: unit 0007 criterion 1.
        """
        with corpus_copy() as root:
            out = root.parent / "out"
            base = ["environment", str(root), "--work", str(root)]
            base += ["--home", str(root), "--write", str(out)]
            with contextlib.redirect_stdout(io.StringIO()):
                code = main([*base, "--secret", "token"])
            settings = json.loads((out / claude_code.SETTINGS).read_text())
            with contextlib.redirect_stdout(io.StringIO()):
                alone = main([*base, "--secret-store"])
            closed = json.loads((out / claude_code.SETTINGS).read_text())
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                bad = main([*base, "--secret", "a/b"])
                empty = main([*base, "--secret", ""])
        self.assertEqual((alone, empty), (0, 1))
        self.assertEqual(closed["sandbox"]["filesystem"]["allowRead"], [])
        self.assertIn(
            f"{root.resolve()}/secrets",
            closed["sandbox"]["filesystem"]["denyWrite"],
        )
        self.assertEqual(code, 0)
        self.assertEqual(
            settings["sandbox"]["filesystem"]["allowRead"],
            [f"{root.resolve()}/secrets/token"],
        )
        self.assertEqual(bad, 1)
        self.assertIn("not a file name of the store", err.getvalue())


class Command(unittest.TestCase):
    """The ``environment`` command reports a governance fault plainly."""

    def test_missing_table_is_an_error(self) -> None:
        """Behavior: a corpus without the outcome table exits 1 with a
        message naming the table, not a traceback.

        Reference: a copy of the live corpus with STND.HARN.18 removed.
        Before review 0003 the command ended in a LookupError traceback.
        """
        with corpus_copy() as root:
            (root / "STND/HARN/18.md").unlink()
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = main([
                    "environment", str(root), "--work", str(root),
                    "--home", str(root), "--write", str(root.parent / "o"),
                ])
        self.assertEqual(code, 1)
        self.assertIn("environment-outcomes", err.getvalue())

    def test_writes_every_file(self) -> None:
        """Behavior: ``--write`` writes the six files of the adapter.

        Reference: the paths named in ``claude_code``; a regression
        guard of the command's wiring, not correctness evidence.
        """
        with corpus_copy() as root:
            out = root.parent / "out"
            with contextlib.redirect_stdout(io.StringIO()):
                code = main([
                    "environment", str(root), "--work", str(root),
                    "--home", str(root), "--write", str(out),
                ])
            written = {
                p.relative_to(out).as_posix()
                for p in out.rglob("*") if p.is_file()
            }
        self.assertEqual(code, 0)
        self.assertIn(str(claude_code.SETTINGS), written)
        self.assertEqual(len(written), 6)


def printed_check(notes: str) -> tuple[str, list[str]]:
    """Return the directory and the command of INSTALL.md's check.

    Parameters
    ----------
    notes : str
        Text of INSTALL.md.

    Returns
    -------
    tuple[str, list[str]]
        The directory its ``cd`` names, and the words of the command
        after ``python3 -B -m govharness``, as the shell splits them.
    """
    block = notes.split("## Check", 1)[1].split("```sh\n", 1)[1]
    block = block.split("```", 1)[0].replace("\\\n", "")
    cd, command = block.strip().split("\n")
    words = shlex.split(command)
    assert words[:4] == ["python3", "-B", "-m", "govharness"], words
    return shlex.split(cd)[1], words[4:]


def install(out: Path, root: Path) -> None:
    """Copy the files under ``out/root`` beneath ``root``, as root would.

    Parameters
    ----------
    out : Path
        Output directory of a derivation.
    root : Path
        Directory standing for ``/``.
    """
    for path in (out / "root").rglob("*"):
        if path.is_file():
            target = root / path.relative_to(out / "root")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    for program in claude_code.PROGRAMS:
        target = root / program.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("", encoding="utf-8")


class PrintedCheck(unittest.TestCase):
    """Unit 0014: INSTALL.md's check, run as printed, checks clean."""

    def check(self, notes: str, root: Path) -> tuple[int, str]:
        """Run the printed check against files installed under ``root``.

        The account's reach is simulated as empty, as in
        ``InstalledCheck``, since the tests may run as root.

        Parameters
        ----------
        notes : str
            Text of INSTALL.md.
        root : Path
            Directory standing for ``/``.

        Returns
        -------
        tuple[int, str]
            Exit status and output.
        """
        directory, argv = printed_check(notes)
        self.assertEqual(Path(directory), HARNESS)
        self.assertEqual(argv[-1], "--check")
        shown = io.StringIO()
        with (
            mock.patch(
                "govharness.cli.environment.installed_problems",
                lambda files, _, programs: installed_problems(
                    files, root, programs
                ),
            ),
            mock.patch("govharness.ledger.gpg.os.access", lambda p, _: False),
            contextlib.redirect_stdout(shown),
        ):
            code = main(argv)
        return code, shown.getvalue()

    @frozen_clock()
    @no_anchor()
    def test_printed_check_passes(self) -> None:
        """Behavior: for a derivation given every option that applies,
        the check that INSTALL.md prints, run as given from the
        directory it names, exits 0 with ``environment: PASS``; the
        check with only ``--work`` and ``--home``, as INSTALL.md printed
        it before, reports that the files differ.

        Reference: installation-kit check of 2026-10-25, finding 1
        (``review-records/round-2026-10-25-close/install-kit.md``).
        Assured work requires a signature, so its derivation names no
        authorization and is a case of its own. The authorization
        expires beyond the default horizon, so that a check without the
        derivation's horizon fails.
        """
        cases = {
            "authorized": [
                "--open", "OPEN", "--domain", "pypi.org",
                "--domain", "api.github.com", "--tool", "mcp__docs__*",
                "--search", "--unattended", "--secret-store",
                "--secret", "token", "--secret", ".hidden",
                "--authorization", IDENT, "--role", ROLE,
                "--expiry-horizon", "200", "--accept-unsigned",
            ],
            "assured": ["--assured", "--secret-store",
                        "--expiry-horizon", "none"],
        }
        for label, options in cases.items():
            with self.subTest(case=label), corpus_copy() as corpus:
                # 128 days after the clock: beyond the default horizon.
                write_authorization(
                    corpus, expires="2027-03-01T00:00:00+00:00"
                )
                record(corpus)
                base = corpus.parent
                (base / "open").mkdir()
                options = [
                    str(base / "open") if o == "OPEN" else o
                    for o in options
                ]
                out, root = base / "out", base / "slash"
                with contextlib.redirect_stdout(io.StringIO()):
                    written = main([
                        "environment", str(corpus), "--work", str(corpus),
                        "--home", str(base), *options, "--write", str(out),
                    ])
                self.assertEqual(written, 0)
                install(out, root)
                notes = (out / claude_code.INSTALL).read_text()
                code, shown = self.check(notes, root)
                self.assertEqual((code, shown.splitlines()[-1]),
                                 (0, "environment: PASS"), shown)
                bare = (
                    f"## Check\n```sh\ncd {HARNESS}\npython3 -B -m "
                    f"govharness environment {corpus} --work {corpus} "
                    f"--home {base} --check\n```\n"
                )
                code, shown = self.check(bare, root)
                self.assertEqual(code, 1)
                self.assertIn("differs from its generation", shown)

    def test_notes_name_the_steps(self) -> None:
        """Behavior: INSTALL.md names the programs the check tests, says
        where to run the installation, and gives the command that
        appends the draft entry to the corpus ledger, with its fields.

        Reference: installation-kit check, findings 2 to 4.
        """
        with corpus_copy() as corpus:
            out = corpus.parent / "out"
            with contextlib.redirect_stdout(io.StringIO()):
                main([
                    "environment", str(corpus), "--work", str(corpus),
                    "--home", str(corpus), "--write", str(out),
                ])
            notes = (out / claude_code.INSTALL).read_text()
            draft = json.loads((out / claude_code.ENTRY).read_text())
        for program in claude_code.PROGRAMS:
            self.assertIn(f"`{program}`", notes)
        self.assertIn("/usr/bin/socat", claude_code.PROGRAMS)
        self.assertIn(shlex.join(["cd", str(out.resolve())]), notes)
        self.assertIn(f"`{corpus.resolve()}/ledger.jsonl`", notes)
        self.assertNotIn("work ledger", notes)
        record = notes.split("## Record", 1)[1]
        append = record.split("```sh\n", 1)[1].split("```", 1)[0]
        words = shlex.split(append.replace("\\\n", ""))
        start = words.index("python3")
        self.assertEqual(
            words[start + 4:start + 7],
            ["ledger", "append", str(corpus.resolve())],
        )
        self.assertIn(draft["rationale"], words)
        self.assertIn(",".join(draft["targets"]), words)
        self.assertNotIn("--sign", words)


class InstalledCheck(unittest.TestCase):
    """STND.HARN.21: installed files must match and be out of reach."""

    def test_missing_and_differing(self) -> None:
        """Behavior: a missing file and a changed file are both reported.

        Reference: STND.HARN.21.
        """
        files = rendered(live_corpus())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            settings = root / "etc/claude-code/managed-settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text("{}", encoding="utf-8")
            problems = installed_problems(files, root)
        self.assertTrue(any(p.startswith("missing:") for p in problems))
        self.assertTrue(any("differs" in p for p in problems))

    def test_alterable_file_reported(self) -> None:
        """Behavior: an installed file this account can write is
        reported.

        Reference: STND.HARN.21; the tests run as root, so every file is
        alterable here and the passing case is not shown.
        """
        files = rendered(live_corpus())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, text in files.items():
                if rel.parts[0] == "root":
                    path = root / rel.relative_to("root")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text, encoding="utf-8")
            problems = installed_problems(files, root)
        self.assertEqual(len(problems), 3)
        self.assertTrue(all(p.startswith("alterable") for p in problems))

    def test_link_to_alterable_file(self) -> None:
        """Behavior: an installed file that links into a place the
        account can alter is reported.

        Reference: STND.HARN.21. The tests run as root, which can alter
        anything, so the account's reach is simulated: only the agent's
        directory counts as alterable. Before review 0003 a link was
        judged by its own directories alone.
        """
        files = rendered(live_corpus())
        with tempfile.TemporaryDirectory() as tmp:
            root, agent = Path(tmp) / "root", Path(tmp) / "agent"
            for rel, text in files.items():
                if rel.parts[0] == "root":
                    real = agent / rel.name
                    real.parent.mkdir(parents=True, exist_ok=True)
                    real.write_text(text, encoding="utf-8")
                    path = root / rel.relative_to("root")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.symlink_to(real)
            reach = str(agent.resolve())
            with mock.patch(
                "govharness.ledger.gpg.os.access",
                lambda p, _: str(p).startswith(reach),
            ):
                problems = installed_problems(files, root)
        self.assertEqual(len(problems), 3)
        self.assertTrue(all(p.startswith("alterable") for p in problems))

    def test_current_and_out_of_reach_passes(self) -> None:
        """Behavior: installed files that match and a program the account
        cannot alter give no problem; a missing program is reported.

        Reference: STND.HARN.21. The account's reach is simulated as
        empty, since the tests run as root.
        """
        files = rendered(live_corpus())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, text in files.items():
                if rel.parts[0] == "root":
                    path = root / rel.relative_to("root")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text, encoding="utf-8")
            program = root / "usr/bin/python3"
            program.parent.mkdir(parents=True)
            program.write_text("", encoding="utf-8")
            with mock.patch(
                "govharness.ledger.gpg.os.access", lambda p, _: False
            ):
                clean = installed_problems(files, root, ("/usr/bin/python3",))
                absent = installed_problems(files, root, ("/usr/bin/nope",))
        self.assertEqual(clean, [])
        self.assertEqual(len(absent), 1)
        self.assertIn("program missing or alterable", absent[0])


if __name__ == "__main__":
    unittest.main()
