"""Convention tests: annotations and NumPy-style docstrings everywhere.

Unit 0001 criterion 6 requires every function and class to carry type
annotations and a NumPy-style docstring. The tests read the source of
the package, the tests, and the shims with ``ast``.
"""

from __future__ import annotations

import ast
import unittest
from collections.abc import Iterator
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCES = ("govharness", "tests")
Definition = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


def definitions() -> Iterator[tuple[str, Definition]]:
    """Yield every function and class defined in the sources.

    Yields
    ------
    tuple[str, Definition]
        A ``path:line name`` label and the definition.
    """
    for folder in SOURCES:
        for path in sorted((REPO / folder).rglob("*.py")):
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


if __name__ == "__main__":
    unittest.main()
