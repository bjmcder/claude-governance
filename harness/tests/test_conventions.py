"""Convention tests: annotations and NumPy-style docstrings everywhere.

Unit 0001 criterion 6 requires every function and class to carry type
annotations and a NumPy-style docstring. The tests read, with ``ast``,
every Python source under ``harness/``: the package, the tests, and any
top-level directory added later, so that a new directory is covered
without a change here (unit 0022). Hidden directories and the build
products of an installation are left out.
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Directories of ``harness/`` that hold no source of ours: an editable
# installation's metadata and build products.
NOT_SOURCES = {"build", "dist"}
Definition = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


def sources(repo: Path = REPO) -> list[Path]:
    """Return every top-level directory of ``harness/`` holding Python.

    Parameters
    ----------
    repo : Path
        The directory to read, ``harness/`` by default.

    Returns
    -------
    list[Path]
        Each directory, not hidden and not a build product, under which
        a ``.py`` file lies; ``govharness`` and ``tests`` among them.
    """
    return sorted(
        p
        for p in repo.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name not in NOT_SOURCES
        and not p.name.endswith(".egg-info")
        and any(p.rglob("*.py"))
    )


def definitions() -> Iterator[tuple[str, Definition]]:
    """Yield every function and class defined in the sources.

    Yields
    ------
    tuple[str, Definition]
        A ``path:line name`` label and the definition.
    """
    for folder in sources():
        for path in sorted(folder.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(
                    node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
                ):
                    rel = path.relative_to(REPO)
                    yield f"{rel}:{node.lineno} {node.name}", node


def problems(node: Definition) -> list[str]:
    """Return how one definition breaks the conventions.

    Parameters
    ----------
    node : Definition
        A function or class.

    Returns
    -------
    list[str]
        Missing docstring, annotations, or docstring sections.
    """
    doc = ast.get_docstring(node)
    if not doc:
        return ["no docstring"]
    if isinstance(node, ast.ClassDef):
        return []
    found: list[str] = []
    arguments = node.args
    named = [
        a
        for a in [
            *arguments.posonlyargs,
            *arguments.args,
            *arguments.kwonlyargs,
        ]
        if a.arg not in {"self", "cls"}
    ]
    starred = [a for a in (arguments.vararg, arguments.kwarg) if a]
    found += [
        f"{a.arg} unannotated"
        for a in [*named, *starred]
        if a.annotation is None
    ]
    if node.returns is None:
        found.append("no return annotation")
    if (named or starred) and "Parameters\n" not in doc:
        found.append("no Parameters section")
    returns = node.returns
    gives_none = isinstance(returns, ast.Constant) and returns.value is None
    if returns is not None and not gives_none:
        if "Returns\n" not in doc and "Yields\n" not in doc:
            found.append("no Returns section")
    return found


class Conventions(unittest.TestCase):
    """Every definition is annotated and documented."""

    def test_annotated_and_documented(self) -> None:
        """Behavior: each function and class has annotations and a
        NumPy-style docstring with the sections its signature needs.

        Reference: unit 0001 criterion 6 and the code standard of the
        harness.
        """
        for label, node in definitions():
            with self.subTest(label):
                self.assertEqual(problems(node), [])

    def test_audit_finds_a_bare_function(self) -> None:
        """Behavior: the audit reports a function with nothing.

        Reference: a hand-written undocumented, unannotated function,
        so that a pass of the test above is evidence.
        """
        node = ast.parse("def f(x):\n    return x\n").body[0]
        assert isinstance(node, ast.FunctionDef)
        self.assertEqual(problems(node), ["no docstring"])
        node = ast.parse('def f(x):\n    """Do."""\n').body[0]
        assert isinstance(node, ast.FunctionDef)
        self.assertEqual(
            problems(node),
            [
                "x unannotated",
                "no return annotation",
                "no Parameters section",
            ],
        )
        node = ast.parse('def f(x, /):\n    """Do."""\n').body[0]
        assert isinstance(node, ast.FunctionDef)
        self.assertIn("x unannotated", problems(node))

    def test_sources_cover_every_directory(self) -> None:
        """Behavior: the package and the tests are read, and so is any
        other top-level directory that holds Python; a hidden
        directory, a build product, and a directory without Python
        are not.

        Reference: a hand-made tree of seven directories (unit 0022,
        HR-14), and the live ``harness/``, whose sources are
        ``govharness`` and ``tests`` at least.
        """
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for rel in (
                "govharness/a.py",
                "tests/b.py",
                "extra/deep/c.py",
                ".hidden/d.py",
                "build/e.py",
                "govharness.egg-info/f.py",
                "governance/g.md",
            ):
                (repo / rel).parent.mkdir(parents=True, exist_ok=True)
                (repo / rel).write_text("", encoding="utf-8")
            found = [p.name for p in sources(repo)]
        self.assertEqual(found, ["extra", "govharness", "tests"])
        self.assertLessEqual(
            {"govharness", "tests"}, {p.name for p in sources()}
        )


if __name__ == "__main__":
    unittest.main()
