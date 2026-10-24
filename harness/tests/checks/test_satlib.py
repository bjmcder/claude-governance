"""Tests of the built-in solver of the proofs (checks f)."""

from __future__ import annotations

import sys
import unittest

from govharness.checks.logic.satlib import ClauseSet, solve_builtin

DEFAULT_LIMIT = 1000  # CPython's default recursion limit
SPLITS = 1500  # more case splits than that limit


class BuiltinSolver(unittest.TestCase):
    """DPLL finds models and cores without touching interpreter state."""

    def test_deep_search_leaves_the_recursion_limit(self) -> None:
        """Behavior: a search with more case splits than the default
        recursion limit finds a model under that limit, and leaves the
        limit unchanged.

        Reference: the clauses ``x_i or y_i`` for 1500 values of i, which
        unit propagation cannot settle, so each needs one split; ``False``
        is tried first, so the model sets every ``x_i`` false and every
        ``y_i`` true. The flat solver recursed once per split and raised
        the limit for the rest of the process (defect 5 of unit 0001,
        fixed by review 0001). The test sets the default limit itself,
        since an earlier test may have run the flat solver, and restores
        the previous value.
        """
        clauses = ClauseSet()
        for i in range(SPLITS):
            clauses.add(f"c{i}", (f"x{i}", True), (f"y{i}", True))
        before = sys.getrecursionlimit()
        sys.setrecursionlimit(DEFAULT_LIMIT)
        try:
            result = solve_builtin(clauses)
            self.assertEqual(sys.getrecursionlimit(), DEFAULT_LIMIT)
        finally:
            sys.setrecursionlimit(before)
        self.assertTrue(result.satisfiable)
        self.assertEqual(
            result.model,
            {
                **{f"x{i}": False for i in range(SPLITS)},
                **{f"y{i}": True for i in range(SPLITS)},
            },
        )

    def test_contradiction_yields_its_core(self) -> None:
        """Behavior: an unsatisfiable set gives the fact clauses that
        contradict, and only those.

        Reference: the facts ``a`` and ``b`` with the axiom ``not a or
        not b``, beside an unrelated fact ``c`` and a free clause.
        """
        clauses = ClauseSet()
        clauses.add("fact:a", ("a", True))
        clauses.add("fact:b", ("b", True))
        clauses.add("fact:c", ("c", True))
        clauses.add("free", ("d", True), ("e", True))
        clauses.add("exclusive", ("a", False), ("b", False))
        result = solve_builtin(clauses)
        self.assertFalse(result.satisfiable)
        self.assertEqual(result.core, ["fact:a", "fact:b"])


if __name__ == "__main__":
    unittest.main()
