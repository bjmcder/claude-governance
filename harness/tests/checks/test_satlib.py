"""Tests of the built-in solver of the proofs (checks f)."""

from __future__ import annotations

import contextlib
import itertools
import random
import signal
import sys
import threading
import unittest
from collections.abc import Iterator
from types import FrameType

from govharness.checks.logic.satlib import (
    FACT_PREFIXES,
    ClauseSet,
    Literal,
    SolveResult,
    prove_entailed,
    solve,
    solve_builtin,
)

DEFAULT_LIMIT = 1000  # CPython's default recursion limit
SPLITS = 1500  # more case splits than that limit
SEED = 9  # seed of the random formulas: unit 0009
FORMULAS = 3000  # random formulas compared with brute force
VARIABLES = ("p", "q", "r", "s", "t", "u")
LARGE_FORMULAS = 500  # larger random formulas compared with the old search
LARGE_SIZES = (2, 4, 8, 8, 5, 3, 2, 1, 1)  # weights of sizes 1 to 9
LIMIT = 10.0  # seconds a solve may take before its test fails


def holds(model: dict[str, bool], literals: list[Literal]) -> bool:
    """Return whether a total assignment satisfies a clause.

    Parameters
    ----------
    model : dict[str, bool]
        A value for every variable of the clause.
    literals : list[Literal]
        Literals of the clause.

    Returns
    -------
    bool
        Whether some literal is true.
    """
    return any(model[variable] == polarity for variable, polarity in literals)


def brute_force(clauses: list[list[Literal]]) -> bool:
    """Return whether clauses are satisfiable, by trying every assignment.

    Parameters
    ----------
    clauses : list[list[Literal]]
        Clauses to satisfy.

    Returns
    -------
    bool
        True when some assignment of the variables satisfies every
        clause; with no variables, when no clause is empty.
    """
    names = sorted({variable for clause in clauses for variable, _ in clause})
    for values in itertools.product((False, True), repeat=len(names)):
        model = dict(zip(names, values, strict=True))
        if all(holds(model, clause) for clause in clauses):
            return True
    return False


def brute_force_core(clause_set: ClauseSet) -> list[str]:
    """Return the core the built-in solver should give, by brute force.

    Parameters
    ----------
    clause_set : ClauseSet
        An unsatisfiable set.

    Returns
    -------
    list[str]
        The fact clauses left when each fact, in order, is dropped
        whenever the axioms and the remaining facts stay unsatisfiable:
        the deletion order of ``solve_builtin``, with every
        satisfiability decided by ``brute_force``.
    """
    is_fact = [
        name.startswith(FACT_PREFIXES) for name, _ in clause_set.clauses
    ]
    axioms = [c for (_, c), f in zip(clause_set.clauses, is_fact) if not f]
    facts = [nc for nc, f in zip(clause_set.clauses, is_fact) if f]
    index = 0
    while index < len(facts):
        trial = facts[:index] + facts[index + 1 :]
        if not brute_force(axioms + [c for _, c in trial]):
            facts = trial
        else:
            index += 1
    return [name for name, _ in facts]


def rescanning_model(clauses: list[list[Literal]]) -> dict[str, bool] | None:
    """Return the model that the solver unit 0009 replaced finds.

    A copy of the search of units 0001 to 0008, kept as the reference of
    the search order: unit propagation rescans every clause until
    nothing changes, and the search splits on the first unassigned
    variable of the first open clause, trying ``False`` first.

    Parameters
    ----------
    clauses : list[list[Literal]]
        Clauses to satisfy.

    Returns
    -------
    dict[str, bool] | None
        The first satisfying assignment found, or ``None``.
    """
    pending: list[tuple[list[list[Literal]], dict[str, bool]]] = [
        (clauses, {})
    ]
    while pending:
        branch_clauses, branch = pending.pop()
        branch = dict(branch)
        if not rescan(branch_clauses, branch):
            continue
        open_clauses = [c for c in branch_clauses if not satisfied(c, branch)]
        if not open_clauses:
            return branch
        variable = next(
            v for clause in open_clauses for v, _ in clause if v not in branch
        )
        pending.append((open_clauses, {**branch, variable: True}))
        pending.append((open_clauses, {**branch, variable: False}))
    return None


def satisfied(clause: list[Literal], assignment: dict[str, bool]) -> bool:
    """Return True when some literal of a clause is already true.

    Parameters
    ----------
    clause : list[Literal]
        Literals of the clause.
    assignment : dict[str, bool]
        Values assigned so far.

    Returns
    -------
    bool
        Whether the assignment satisfies the clause.
    """
    return any(assignment.get(v) == p for v, p in clause if v in assignment)


def rescan(clauses: list[list[Literal]], assignment: dict[str, bool]) -> bool:
    """Apply unit propagation by rescanning every clause, in place.

    Parameters
    ----------
    clauses : list[list[Literal]]
        Clauses to satisfy.
    assignment : dict[str, bool]
        Values assigned so far; extended in place.

    Returns
    -------
    bool
        False on a conflict, else True.
    """
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            if satisfied(clause, assignment):
                continue
            free = [(v, p) for v, p in clause if v not in assignment]
            if not free:
                return False
            if len(free) == 1:
                assignment[free[0][0]] = free[0][1]
                changed = True
    return True


def random_clause_set(rng: random.Random) -> ClauseSet:
    """Draw a small clause set, with duplicate and complementary literals.

    Parameters
    ----------
    rng : random.Random
        Seeded generator.

    Returns
    -------
    ClauseSet
        Up to 14 clauses of up to 4 literals over up to 6 variables,
        drawn with replacement, so a clause may repeat a literal or hold
        both polarities of a variable. About one clause in thirty is
        empty. Each clause is a fact or an axiom at random.
    """
    clause_set = ClauseSet()
    variables = VARIABLES[: rng.randint(1, len(VARIABLES))]
    for index in range(rng.randint(0, 14)):
        size = rng.choices(range(5), weights=(1, 8, 9, 9, 3))[0]
        literals = [
            (rng.choice(variables), rng.random() < 0.5) for _ in range(size)
        ]
        prefix = rng.choice(("fact:", "NEG[", "axiom:"))
        clause_set.add(f"{prefix}{index}", *literals)
    return clause_set


def large_clause_set(rng: random.Random) -> ClauseSet:
    """Draw a larger clause set, past what brute force can try.

    Parameters
    ----------
    rng : random.Random
        Seeded generator.

    Returns
    -------
    ClauseSet
        30 to 60 clauses of 1 to 9 literals over 10 to 30 variables,
        about one in seventeen a unit clause; each further literal repeats
        an earlier literal of its clause with probability 0.3, and is
        otherwise drawn with replacement, so complements also occur.
        Each clause is a fact or an axiom at random.
    """
    clause_set = ClauseSet()
    variables = [f"v{i}" for i in range(rng.randint(10, 30))]
    for index in range(rng.randint(30, 60)):
        size = rng.choices(range(1, 10), weights=LARGE_SIZES)
        literals: list[Literal] = []
        for _ in range(size[0]):
            if literals and rng.random() < 0.3:
                literals.append(rng.choice(literals))
            else:
                literals.append((rng.choice(variables), rng.random() < 0.5))
        prefix = rng.choice(("fact:", "NEG[", "axiom:"))
        clause_set.add(f"{prefix}{index}", *literals)
    return clause_set


def rescanning_core(clause_set: ClauseSet) -> list[str]:
    """Return the core the built-in solver should give, by the old search.

    Parameters
    ----------
    clause_set : ClauseSet
        An unsatisfiable set.

    Returns
    -------
    list[str]
        The fact clauses left by the deletion order of ``solve_builtin``,
        with every satisfiability decided by ``rescanning_model``.
    """
    axioms = [
        c for n, c in clause_set.clauses if not n.startswith(FACT_PREFIXES)
    ]
    facts = [
        nc for nc in clause_set.clauses if nc[0].startswith(FACT_PREFIXES)
    ]
    index = 0
    while index < len(facts):
        trial = facts[:index] + facts[index + 1 :]
        if rescanning_model(axioms + [c for _, c in trial]) is None:
            facts = trial
        else:
            index += 1
    return [name for name, _ in facts]


@contextlib.contextmanager
def time_limit(seconds: float) -> Iterator[None]:
    """Raise ``TimeoutError`` in the block once it has run too long.

    A search that does not end then fails its test, where it would
    otherwise hang the run. The guard uses ``SIGALRM``; where that
    signal is unavailable, or off the main thread, the block runs
    unguarded.

    Parameters
    ----------
    seconds : float
        Wall time allowed.

    Yields
    ------
    None
        Control, for the guarded block.
    """
    alarm = getattr(signal, "SIGALRM", None)
    if (
        alarm is None
        or threading.current_thread() is not threading.main_thread()
    ):
        yield
        return

    def fire(signum: int, frame: FrameType | None) -> None:
        """Raise the timeout.

        Parameters
        ----------
        signum : int
            The signal received.
        frame : FrameType | None
            The frame it interrupted.
        """
        raise TimeoutError(f"no result in {seconds} s")

    previous = signal.signal(alarm, fire)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(alarm, previous)


def solved(clause_set: ClauseSet) -> SolveResult:
    """Solve with the built-in solver within ``LIMIT`` seconds.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses to solve.

    Returns
    -------
    SolveResult
        The result of ``solve_builtin``.
    """
    with time_limit(LIMIT):
        return solve_builtin(clause_set)


def check_result(
    case: unittest.TestCase, clause_set: ClauseSet, result: SolveResult
) -> None:
    """Assert that a result agrees with brute force and the old search.

    Parameters
    ----------
    case : unittest.TestCase
        The test making the assertions.
    clause_set : ClauseSet
        The clauses solved.
    result : SolveResult
        The built-in solver's result for them.
    """
    clauses = [c for _, c in clause_set.clauses]
    case.assertEqual(result.satisfiable, brute_force(clauses))
    if result.satisfiable:
        case.assertEqual(list(result.model), clause_set.variables())
        case.assertTrue(all(holds(result.model, c) for c in clauses))
        reference = rescanning_model(clauses)
        case.assertIsNotNone(reference)
        found = reference or {}
        case.assertEqual(
            result.model,
            {v: found.get(v, False) for v in clause_set.variables()},
        )
        case.assertEqual(result.core, [])
    else:
        case.assertEqual(result.model, {})
        case.assertEqual(result.core, brute_force_core(clause_set))
        case.assertIsNone(rescanning_model(clauses))
    case.assertEqual(result.backend, "builtin-dpll")


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
            result = solved(clauses)
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
        result = solved(clauses)
        self.assertFalse(result.satisfiable)
        self.assertEqual(result.core, ["fact:a", "fact:b"])


class AgreesWithBruteForce(unittest.TestCase):
    """The watched-literal search decides as trying every assignment does.

    Unit 0009 replaced the rescanning unit propagation; these tests are
    the evidence that no status, model, or core changed.
    """

    def test_random_formulas(self) -> None:
        """Behavior: on 3000 small random clause sets, the status equals
        brute force, a model satisfies every clause and equals the model
        of the rescanning search, and a core equals the core that the
        same deletion order gives with brute force.

        Reference: ``brute_force`` tries every assignment;
        ``rescanning_model`` is the search of units 0001 to 0008. The
        generator is seeded (``SEED``), so the formulas are the same on
        every run; both statuses occur often, so neither is tested only
        trivially.
        """
        rng = random.Random(SEED)
        statuses = []
        for number in range(FORMULAS):
            clause_set = random_clause_set(rng)
            result = solved(clause_set)  # a timeout ends the test
            with self.subTest(formula=number, clauses=clause_set.clauses):
                check_result(self, clause_set, result)
                statuses.append(result.satisfiable)
        self.assertGreater(statuses.count(True), FORMULAS // 5)
        self.assertGreater(statuses.count(False), FORMULAS // 5)

    def test_larger_random_formulas(self) -> None:
        """Behavior: on 500 larger random clause sets, the status, the
        model, and the core equal those of the rescanning search, and a
        model satisfies every clause.

        Reference: ``rescanning_model`` and ``rescanning_core``, the
        search of units 0001 to 0008, seeded as above. These sets keep
        clauses long enough that watches move, are kept, and are carried
        past a conflict, which the small sets seldom need (review 0008,
        M1): dropping a kept watch or the watches left unvisited at a
        conflict fails this test.
        """
        rng = random.Random(SEED + 2)
        statuses = []
        for number in range(LARGE_FORMULAS):
            clause_set = large_clause_set(rng)
            clauses = [c for _, c in clause_set.clauses]
            result = solved(clause_set)  # a timeout ends the test
            with self.subTest(formula=number, clauses=clause_set.clauses):
                reference = rescanning_model(clauses)
                self.assertEqual(result.satisfiable, reference is not None)
                statuses.append(result.satisfiable)
                if reference is None:
                    self.assertEqual(result.core, rescanning_core(clause_set))
                    continue
                self.assertTrue(all(holds(result.model, c) for c in clauses))
                self.assertEqual(
                    list(result.model.items()),
                    [
                        (v, reference.get(v, False))
                        for v in clause_set.variables()
                    ],
                )
        self.assertGreater(statuses.count(True), LARGE_FORMULAS // 5)
        self.assertGreater(statuses.count(False), LARGE_FORMULAS // 5)

    def test_solve_and_entailment_use_the_same_search(self) -> None:
        """Behavior: without z3, ``solve`` and ``prove_entailed`` give
        the built-in result, and a claim is entailed exactly when brute
        force finds the base and the negated claim unsatisfiable.

        Reference: 300 seeded random bases, each with a random claim of
        one to three literals.
        """
        rng = random.Random(SEED + 1)
        for number in range(300):
            base = random_clause_set(rng)
            claim: list[Literal] = [
                (rng.choice(VARIABLES), rng.random() < 0.5)
                for _ in range(rng.randint(1, 3))
            ]
            with time_limit(LIMIT):  # a timeout ends the test
                solved_once = solve(base, use_z3=False)
                built_in = solve_builtin(base)
                entailed, result = prove_entailed(
                    base, "claim", claim, use_z3=False
                )
            with self.subTest(formula=number):
                self.assertEqual(solved_once, built_in)
                negated = [c for _, c in base.clauses] + [
                    [(v, not p) for v, p in claim]
                ]
                self.assertEqual(entailed, not brute_force(negated))
                self.assertEqual(entailed, not result.satisfiable)

    def test_long_chain_propagates(self) -> None:
        """Behavior: a chain of 2000 implications from one fact is settled
        by propagation alone, and its last link is entailed with the
        fact as the whole core.

        Reference: ``x0`` with ``x_i -> x_{i+1}``; the claim ``x2000``.
        """
        base = ClauseSet()
        base.fact("fact:x0", "x0")
        for i in range(2000):
            base.implies(f"link{i}", f"x{i}", (f"x{i + 1}", True))
        with time_limit(LIMIT):
            entailed, result = prove_entailed(
                base, "end", [("x2000", True)], use_z3=False
            )
        self.assertTrue(entailed)
        self.assertEqual(result.core, ["fact:x0", "NEG[end]"])


class EdgeCases(unittest.TestCase):
    """Empty sets and clauses, units, duplicates, and tautologies."""

    def solved(self, *clauses: tuple[str, list[Literal]]) -> SolveResult:
        """Solve clauses with the built-in solver and check the result.

        Parameters
        ----------
        *clauses : tuple[str, list[Literal]]
            Named clauses.

        Returns
        -------
        SolveResult
            The result, already checked by ``check_result``.
        """
        clause_set = ClauseSet(list(clauses))
        result = solved(clause_set)
        check_result(self, clause_set, result)
        return result

    def test_no_clauses(self) -> None:
        """Behavior: the empty set is satisfiable by the empty model.

        Reference: no clauses, so no variables.
        """
        result = self.solved()
        self.assertTrue(result.satisfiable)
        self.assertEqual(result.model, {})

    def test_empty_clause(self) -> None:
        """Behavior: an empty clause is unsatisfiable on its own and among
        other clauses, and is its own core when it is a fact.

        Reference: the empty clause has no literal that could hold.
        """
        self.assertFalse(self.solved(("axiom", [])).satisfiable)
        result = self.solved(
            ("fact:a", [("a", True)]),
            ("fact:empty", []),
            ("free", [("b", True), ("c", False)]),
        )
        self.assertFalse(result.satisfiable)
        self.assertEqual(result.core, ["fact:empty"])

    def test_unit_clauses(self) -> None:
        """Behavior: unit clauses fix their variables, and two that
        contradict are the core.

        Reference: ``a``, ``not b``; then ``a`` and ``not a``.
        """
        result = self.solved(("fact:a", [("a", True)]), ("b", [("b", False)]))
        self.assertEqual(result.model, {"a": True, "b": False})
        result = self.solved(
            ("fact:a", [("a", True)]),
            ("fact:c", [("c", True)]),
            ("fact:not-a", [("a", False)]),
        )
        self.assertFalse(result.satisfiable)
        self.assertEqual(result.core, ["fact:a", "fact:not-a"])

    def test_duplicate_literals(self) -> None:
        """Behavior: a clause that repeats a literal holds it, and conflicts
        only when that literal is false.

        Reference: ``a or a`` alone; with ``not a``; and ``not a or not a
        or b`` with the fact ``a``, which forces ``b``.
        """
        self.assertEqual(
            self.solved(("aa", [("a", True), ("a", True)])).model,
            {"a": True},
        )
        result = self.solved(
            ("aa", [("a", True), ("a", True)]),
            ("fact:not-a", [("a", False)]),
        )
        self.assertFalse(result.satisfiable)
        self.assertEqual(result.core, ["fact:not-a"])
        result = self.solved(
            ("fact:a", [("a", True)]),
            ("rule", [("a", False), ("a", False), ("b", True)]),
        )
        self.assertEqual(result.model, {"a": True, "b": True})

    def test_tautologies(self) -> None:
        """Behavior: a clause holding both polarities of a variable is
        always satisfied, and its variable is false in the model unless
        another clause forces it.

        Reference: ``a or not a`` alone; with the fact ``a``; and ``a or
        not a or b`` with ``not b``.
        """
        tautology = ("taut", [("a", True), ("a", False)])
        self.assertEqual(self.solved(tautology).model, {"a": False})
        self.assertEqual(
            self.solved(tautology, ("fact:a", [("a", True)])).model,
            {"a": True},
        )
        result = self.solved(
            ("taut", [("a", True), ("a", False), ("b", True)]),
            ("fact:not-b", [("b", False)]),
        )
        self.assertEqual(result.model, {"a": False, "b": False})


if __name__ == "__main__":
    unittest.main()
