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
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from govharness.cli.main import main
from govharness.core.corpus import Corpus
from govharness.derive.environment import claude_code
from govharness.derive.environment.inputs import Inputs
from govharness.derive.environment.outcomes import read_outcomes
from govharness.workflows.environment import installed_problems
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
