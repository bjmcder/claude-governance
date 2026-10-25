"""Propositional clause sets with a built-in solver and optional z3.

The logic checks encode the corpus's structural claims as clauses
(disjunctions of literals) and prove claims by refutation. The built-in
DPLL solver (Davis-Putnam-Logemann-Loveland: unit propagation plus case
splitting) needs no installation; its unit propagation watches two
literals of each clause, so that it visits only the clauses an
assignment can make unit or false (unit 0009). ``z3`` is used only when
it is already importable and the caller has not asked for the built-in
solver; both give the same verdicts.
"""

from __future__ import annotations

import importlib.util
import itertools
from dataclasses import dataclass, field
from typing import Any

Literal = tuple[str, bool]  # (variable name, polarity)
FACT_PREFIXES = ("fact:", "NEG[")
BUILTIN = "builtin-dpll"
_Z3: Any = None
if importlib.util.find_spec("z3") is not None:
    import z3 as _Z3  # type: ignore[import-not-found]


@dataclass
class ClauseSet:
    """A named set of clauses.

    Parameters
    ----------
    clauses : list[tuple[str, list[Literal]]]
        Each clause has a name that identifies it in an unsatisfiable
        core. Names starting with ``fact:`` or ``NEG[`` mark clauses
        that come from the corpus or from a claim, as opposed to fixed
        axioms.
    """

    clauses: list[tuple[str, list[Literal]]] = field(default_factory=list)

    def add(self, name: str, *literals: Literal) -> None:
        """Add a clause.

        Parameters
        ----------
        name : str
            Name of the clause.
        *literals : Literal
            Its literals, of which at least one holds.
        """
        self.clauses.append((name, list(literals)))

    def fact(self, name: str, variable: str, value: bool = True) -> None:
        """Add a unit clause fixing a variable to a value.

        Parameters
        ----------
        name : str
            Name of the clause.
        variable : str
            Variable fixed.
        value : bool
            Value it takes.
        """
        self.add(name, (variable, value))

    def implies(self, name: str, antecedent: str, consequent: Literal) -> None:
        """Add the clause for ``antecedent -> consequent``.

        Parameters
        ----------
        name : str
            Name of the clause.
        antecedent : str
            Variable that, when true, forces the consequent.
        consequent : Literal
            Literal forced.
        """
        self.add(name, (antecedent, False), consequent)

    def at_most_one(self, name: str, variables: list[str]) -> None:
        """Add pairwise exclusion among variables.

        Parameters
        ----------
        name : str
            Prefix of the clause names.
        variables : list[str]
            Variables of which at most one is true.
        """
        for left, right in itertools.combinations(variables, 2):
            self.add(f"{name}:{left}|{right}", (left, False), (right, False))

    def variables(self) -> list[str]:
        """Return the variable names in order of first appearance.

        Returns
        -------
        list[str]
            Every variable of every clause, once.
        """
        seen: dict[str, None] = {}
        for _, literals in self.clauses:
            for variable, _ in literals:
                seen.setdefault(variable, None)
        return list(seen)

    def copy(self) -> ClauseSet:
        """Return an independent copy.

        Returns
        -------
        ClauseSet
            A set with the same clauses in a new list.
        """
        return ClauseSet(list(self.clauses))


@dataclass
class SolveResult:
    """Outcome of one satisfiability call.

    Parameters
    ----------
    satisfiable : bool
        True when a model exists.
    model : dict[str, bool]
        Variable values of one model when satisfiable.
    core : list[str]
        Names of fact clauses that suffice for a contradiction when not.
    backend : str
        Solver that produced the result.
    positions : list[int]
        Position in the clause set of each clause of ``core``, in the
        same order; two clauses may share a name, and a position names
        one of them.
    """

    satisfiable: bool
    model: dict[str, bool] = field(default_factory=dict)
    core: list[str] = field(default_factory=list)
    backend: str = ""
    positions: list[int] = field(default_factory=list)


def _encode(clauses: list[list[Literal]]) -> tuple[list[str], list[list[int]]]:
    """Number the variables and code each literal as an integer.

    Variables are numbered in order of first appearance, and the literal
    ``(variable, polarity)`` is coded as ``2 * number + polarity``, so
    that ``code ^ 1`` is its negation and ``code >> 1`` its variable.

    Parameters
    ----------
    clauses : list[list[Literal]]
        Clauses to code.

    Returns
    -------
    tuple[list[str], list[list[int]]]
        The variable names by number, and the coded clauses, each with
        its literals in the given order, duplicates included.
    """
    numbers: dict[str, int] = {}
    coded = []
    for clause in clauses:
        codes = []
        for variable, polarity in clause:
            number = numbers.setdefault(variable, len(numbers))
            codes.append(2 * number + int(polarity))
        coded.append(codes)
    return list(numbers), coded


class _Search:
    """State of one DPLL search, with two watched literals per clause.

    ``value`` holds -1 for an unassigned variable, else 0 or 1, and
    ``trail`` lists the literals made true, in the order they were made
    true. Each clause of two or more literals keeps a working copy whose
    first two positions are watched: unit propagation visits a clause
    only when one of its watched literals becomes false, so it never
    rescans the whole clause set. A clause is unit when it is not
    satisfied and exactly one of its literal occurrences is unassigned,
    and in conflict when every occurrence is false, as in the rescanning
    solver this replaces: a repeated literal counts once per occurrence,
    so a clause whose one unassigned literal appears twice is not unit,
    and holds or fails only once another clause or a split assigns that
    literal's variable. The watches need no undoing on backtracking: a
    watch moves only to a literal that is not false at that point, and
    unassigning variables makes no literal false.

    Parameters
    ----------
    clauses : list[list[int]]
        Coded clauses to satisfy (see ``_encode``); not modified.
    count : int
        Number of variables; every code is below ``2 * count``.
    """

    def __init__(self, clauses: list[list[int]], count: int) -> None:
        """Start with every variable unassigned and two watches a clause.

        Parameters
        ----------
        clauses : list[list[int]]
            Coded clauses to satisfy.
        count : int
            Number of variables.
        """
        self.clauses = clauses
        self.value = [-1] * count
        self.trail: list[int] = []
        self.head = 0
        watches: list[list[list[int]]] = [[] for _ in range(2 * count)]
        for codes in clauses:
            if len(codes) > 1:
                working = codes[:]
                watches[working[0]].append(working)
                watches[working[1]].append(working)
        self.watches = watches

    def assign(self, code: int) -> None:
        """Make a literal true and queue it for propagation.

        Parameters
        ----------
        code : int
            Literal of an unassigned variable.
        """
        self.value[code >> 1] = code & 1
        self.trail.append(code)

    def roots(self) -> bool:
        """Assign the literal of every one-literal clause.

        Returns
        -------
        bool
            False when the clauses hold an empty clause or two
            one-literal clauses that contradict, else True.
        """
        value = self.value
        for codes in self.clauses:
            if len(codes) > 1:
                continue
            if not codes:
                return False
            code = codes[0]
            if value[code >> 1] == -1:
                self.assign(code)
            elif value[code >> 1] != code & 1:
                return False
        return True

    def propagate(self) -> bool:
        """Apply unit propagation to every literal queued on the trail.

        Returns
        -------
        bool
            False on a conflict, else True.
        """
        value, trail, watches = self.value, self.trail, self.watches
        while self.head < len(trail):
            false = trail[self.head] ^ 1
            self.head += 1
            listed = watches[false]
            kept: list[list[int]] = []
            for position, working in enumerate(listed):
                if working[0] == false:
                    working[0], working[1] = working[1], false
                other = working[0]
                if value[other >> 1] == other & 1:
                    kept.append(working)
                    continue
                for index in range(2, len(working)):
                    candidate = working[index]
                    if value[candidate >> 1] != (candidate & 1) ^ 1:
                        working[1], working[index] = candidate, false
                        watches[candidate].append(working)
                        break
                else:
                    kept.append(working)
                    if value[other >> 1] != -1:
                        kept.extend(listed[position + 1 :])
                        watches[false] = kept
                        return False
                    self.assign(other)
            watches[false] = kept
        return True

    def undo(self, mark: int) -> None:
        """Unassign every literal made true after a point of the trail.

        Parameters
        ----------
        mark : int
            Length of the trail to return to.
        """
        for code in self.trail[mark:]:
            self.value[code >> 1] = -1
        del self.trail[mark:]
        self.head = mark

    def first_open(self, start: int) -> int:
        """Return the position of the first clause not yet satisfied.

        Parameters
        ----------
        start : int
            Position from which to look; every clause before it is
            satisfied.

        Returns
        -------
        int
            Position of the first clause, in the given order, that no
            assigned literal satisfies; the number of clauses when every
            clause is satisfied.
        """
        clauses, value = self.clauses, self.value
        while start < len(clauses):
            if not any(value[c >> 1] == c & 1 for c in clauses[start]):
                return start
            start += 1
        return start


def _dpll(clauses: list[list[int]], count: int) -> list[int] | None:
    """Return the values of a model of coded clauses, or None.

    The search is depth first: after unit propagation it splits on the
    first unassigned variable of the first open clause, in the order the
    clauses and their literals are given, and tries ``False`` before
    ``True``; a conflict returns to the latest split whose ``True``
    branch is untried. Unit propagation reaches the same assignment, or
    a conflict, in whatever order it visits the clauses, so the search
    makes the same splits, and finds the same model, as the solver that
    rescanned every clause on each pass (unit 0009). An explicit stack
    of splits replaces recursion, so the depth of the search is bounded
    by memory, not by the interpreter's recursion limit, which is left
    alone.

    Parameters
    ----------
    clauses : list[list[int]]
        Coded clauses to satisfy (see ``_encode``).
    count : int
        Number of variables.

    Returns
    -------
    list[int] | None
        The value of each variable, by number, in the first model
        found: 1 for true, 0 for false, -1 for a variable the model
        leaves unassigned. ``None`` when no model exists.
    """
    search = _Search(clauses, count)
    if not (search.roots() and search.propagate()):
        return None
    splits: list[tuple[int, int, int]] = []  # trail mark, variable, open
    start = 0
    while True:
        start = search.first_open(start)
        if start == len(clauses):
            return search.value
        variable = next(
            c >> 1 for c in clauses[start] if search.value[c >> 1] < 0
        )
        splits.append((len(search.trail), variable, start))
        search.assign(2 * variable)
        while not search.propagate():
            while splits and splits[-1][1] < 0:
                splits.pop()
            if not splits:
                return None
            mark, variable, start = splits.pop()
            splits.append((mark, -1, start))
            search.undo(mark)
            search.assign(2 * variable + 1)


def solve_builtin(clause_set: ClauseSet) -> SolveResult:
    """Solve with DPLL; shrink an unsatisfiable set to a core of facts.

    The clauses are coded once (``_encode``); each search of the core
    minimisation takes a subset of the coded clauses, in their order.
    The minimisation tries the fact clauses in order and drops each one
    whose removal, from the facts kept so far and every fact after it,
    leaves the clauses unsatisfiable (``confirms_core`` checks a core
    against exactly this rule).

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses to solve.

    Returns
    -------
    SolveResult
        A model, or a core of fact clauses. Axiom clauses are kept fixed
        during core minimisation and are not listed.
    """
    names, coded = _encode([c for _, c in clause_set.clauses])
    values = _dpll(coded, len(names))
    if values is not None:
        full = {n: v == 1 for n, v in zip(names, values, strict=True)}
        return SolveResult(True, full, [], BUILTIN)
    axioms, facts = _split(clause_set, coded)
    index = 0
    while index < len(facts):
        trial = facts[:index] + facts[index + 1 :]
        if _dpll(axioms + [coded[p] for p in trial], len(names)) is None:
            facts = trial
        else:
            index += 1
    core = [clause_set.clauses[p][0] for p in facts]
    return SolveResult(False, {}, core, BUILTIN, facts)


def _split(
    clause_set: ClauseSet, coded: list[list[int]]
) -> tuple[list[list[int]], list[int]]:
    """Return the coded axiom clauses and the positions of the facts.

    Parameters
    ----------
    clause_set : ClauseSet
        The named clauses.
    coded : list[list[int]]
        The same clauses, coded (``_encode``).

    Returns
    -------
    tuple[list[list[int]], list[int]]
        The coded clauses whose names mark no fact, in order, and the
        positions of the fact clauses, in order.
    """
    axioms: list[list[int]] = []
    facts: list[int] = []
    for position, (name, _) in enumerate(clause_set.clauses):
        if name.startswith(FACT_PREFIXES):
            facts.append(position)
        else:
            axioms.append(coded[position])
    return axioms, facts


def satisfies(clause_set: ClauseSet, model: dict[str, bool]) -> bool:
    """Return whether a model assigns every variable and every clause holds.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses.
    model : dict[str, bool]
        A value for each variable.

    Returns
    -------
    bool
        True when the model's variables are those of the clause set, in
        order of first appearance, as a solver reports them, and some
        literal of each clause is true under it.
    """
    if list(model) != clause_set.variables():
        return False
    return all(
        any(model[variable] == polarity for variable, polarity in literals)
        for _, literals in clause_set.clauses
    )


def confirms_core(
    clause_set: ClauseSet, positions: list[int], exact: bool
) -> bool:
    """Return whether fact clauses are an unsatisfiable core of a set.

    The axioms with the clauses at ``positions`` must be unsatisfiable,
    so the whole set is too: one search. With ``exact``, the positions
    must also be the core that ``solve_builtin`` finds, which takes one
    more search for each position: the minimisation drops a fact exactly
    when the facts kept before it and every fact after it, with the
    axioms, are unsatisfiable. A dropped fact needs no search, since
    those clauses include the core; a kept fact needs them satisfiable.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses.
    positions : list[int]
        Positions of fact clauses in the set.
    exact : bool
        Whether the positions must be the built-in solver's core: in
        increasing order, and minimal by its rule.

    Returns
    -------
    bool
        True when the positions name fact clauses and pass the test.
    """
    total = len(clause_set.clauses)
    if any(not 0 <= p < total for p in positions):
        return False
    if len(set(positions)) != len(positions):
        return False
    if not all(
        clause_set.clauses[p][0].startswith(FACT_PREFIXES) for p in positions
    ):
        return False
    names, coded = _encode([c for _, c in clause_set.clauses])
    axioms, facts = _split(clause_set, coded)
    if _dpll(axioms + [coded[p] for p in positions], len(names)) is not None:
        return False
    if not exact:
        return True
    if positions != sorted(positions):
        return False
    for number, kept in enumerate(positions):
        trial = positions[:number] + [p for p in facts if p > kept]
        if _dpll(axioms + [coded[p] for p in trial], len(names)) is None:
            return False
    return True


def solve_z3(clause_set: ClauseSet) -> SolveResult:
    """Solve with z3, tracking every clause for the unsatisfiable core.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses to solve.

    Returns
    -------
    SolveResult
        A model, or the fact clauses of z3's unsatisfiable core.
    """
    solver = _Z3.Solver()
    solver.set(unsat_core=True)
    atoms = {name: _Z3.Bool(name) for name in clause_set.variables()}
    for index, (name, literals) in enumerate(clause_set.clauses):
        terms = [atoms[v] if p else _Z3.Not(atoms[v]) for v, p in literals]
        solver.assert_and_track(
            _Z3.Or(*terms), _Z3.Bool(f"__track_{index}__{name}")
        )
    backend = backend_name(True)
    if solver.check() == _Z3.sat:
        found = solver.model()
        values = {
            name: bool(_Z3.is_true(found.eval(atom, model_completion=True)))
            for name, atom in atoms.items()
        }
        return SolveResult(True, values, [], backend)
    tracked = [str(b).split("__", 2) for b in solver.unsat_core()]
    kept = [
        (int(index.removeprefix("track_")), name)
        for _, index, name in tracked
        if name.startswith(FACT_PREFIXES)
    ]
    return SolveResult(
        False, {}, [n for _, n in kept], backend, [p for p, _ in kept]
    )


def backend_name(use_z3: bool = True) -> str:
    """Return the backend that ``solve`` reports for a setting.

    Parameters
    ----------
    use_z3 : bool
        Whether z3 may be used.

    Returns
    -------
    str
        ``z3`` and its version when z3 is allowed and importable, else
        ``builtin-dpll``.
    """
    if use_z3 and _Z3 is not None:
        return f"z3 {_Z3.get_version_string()}"
    return BUILTIN


def solve(clause_set: ClauseSet, use_z3: bool = True) -> SolveResult:
    """Solve with z3 when allowed and importable, else with DPLL.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses to solve.
    use_z3 : bool
        Whether z3 may be used.

    Returns
    -------
    SolveResult
        The outcome and the backend that produced it.
    """
    if use_z3 and _Z3 is not None:
        return solve_z3(clause_set)
    return solve_builtin(clause_set)


def negation(
    base: ClauseSet, claim_name: str, claim: list[Literal]
) -> ClauseSet:
    """Return a clause set with the negation of a claim added.

    Parameters
    ----------
    base : ClauseSet
        Facts and axioms; not modified.
    claim_name : str
        Label for the negated claim clause, ``NEG[claim_name]``.
    claim : list[Literal]
        Literals whose conjunction is the claim.

    Returns
    -------
    ClauseSet
        The base followed by one clause, the disjunction of the negated
        literals.
    """
    negated = base.copy()
    negated.add(f"NEG[{claim_name}]", *[(v, not p) for v, p in claim])
    return negated


def prove_entailed(
    base: ClauseSet,
    claim_name: str,
    claim: list[Literal],
    use_z3: bool = True,
) -> tuple[bool, SolveResult]:
    """Check that a clause set entails the conjunction of a claim.

    Parameters
    ----------
    base : ClauseSet
        Facts and axioms.
    claim_name : str
        Label for the negated claim clause.
    claim : list[Literal]
        Literals whose conjunction is the claim.
    use_z3 : bool
        Whether z3 may be used.

    Returns
    -------
    tuple[bool, SolveResult]
        True when the negated claim is unsatisfiable, with the solver
        result (a core when entailed, a countermodel when not).
    """
    result = solve(negation(base, claim_name, claim), use_z3)
    return (not result.satisfiable), result
