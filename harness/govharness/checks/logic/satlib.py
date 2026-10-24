"""Propositional clause sets with a built-in solver and optional z3.

The logic checks encode the corpus's structural claims as clauses
(disjunctions of literals) and prove claims by refutation. The built-in
DPLL solver (Davis-Putnam-Logemann-Loveland: unit propagation plus case
splitting) needs no installation. ``z3`` is used only when it is already
importable and the caller has not asked for the built-in solver; both
give the same verdicts.
"""

from __future__ import annotations

import importlib.util
import itertools
from dataclasses import dataclass, field
from typing import Any

Literal = tuple[str, bool]  # (variable name, polarity)
FACT_PREFIXES = ("fact:", "NEG[")
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
    """

    satisfiable: bool
    model: dict[str, bool] = field(default_factory=dict)
    core: list[str] = field(default_factory=list)
    backend: str = ""


def _satisfied(clause: list[Literal], assignment: dict[str, bool]) -> bool:
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


def _propagate(
    clauses: list[list[Literal]], assignment: dict[str, bool]
) -> bool:
    """Apply unit propagation to an assignment in place.

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
            if _satisfied(clause, assignment):
                continue
            free = [(v, p) for v, p in clause if v not in assignment]
            if not free:
                return False
            if len(free) == 1:
                assignment[free[0][0]] = free[0][1]
                changed = True
    return True


def _dpll(
    clauses: list[list[Literal]], assignment: dict[str, bool]
) -> dict[str, bool] | None:
    """Return a model extending an assignment, or None.

    The search is depth first: after unit propagation it splits on the
    first unassigned variable of the first open clause and tries
    ``False`` before ``True``. An explicit stack of pending branches
    replaces recursion, so the depth of the search is bounded by memory,
    not by the interpreter's recursion limit, which is left alone.

    Parameters
    ----------
    clauses : list[list[Literal]]
        Clauses to satisfy.
    assignment : dict[str, bool]
        Values assigned so far; not modified.

    Returns
    -------
    dict[str, bool] | None
        The first satisfying assignment found, or ``None`` when none
        exists.
    """
    pending = [(clauses, assignment)]
    while pending:
        branch_clauses, branch = pending.pop()
        branch = dict(branch)
        if not _propagate(branch_clauses, branch):
            continue
        open_clauses = [
            c for c in branch_clauses if not _satisfied(c, branch)
        ]
        if not open_clauses:
            return branch
        variable = next(
            v for clause in open_clauses for v, _ in clause if v not in branch
        )
        # Pushed in reverse, so that False is tried first.
        pending.append((open_clauses, {**branch, variable: True}))
        pending.append((open_clauses, {**branch, variable: False}))
    return None


def solve_builtin(clause_set: ClauseSet) -> SolveResult:
    """Solve with DPLL; shrink an unsatisfiable set to a core of facts.

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
    model = _dpll([c for _, c in clause_set.clauses], {})
    if model is not None:
        full = {v: model.get(v, False) for v in clause_set.variables()}
        return SolveResult(True, full, [], "builtin-dpll")
    axioms = [
        c for c in clause_set.clauses if not c[0].startswith(FACT_PREFIXES)
    ]
    facts = [c for c in clause_set.clauses if c[0].startswith(FACT_PREFIXES)]
    index = 0
    while index < len(facts):
        trial = facts[:index] + facts[index + 1 :]
        if _dpll([c for _, c in axioms + trial], {}) is None:
            facts = trial
        else:
            index += 1
    return SolveResult(False, {}, [name for name, _ in facts], "builtin-dpll")


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
    backend = f"z3 {_Z3.get_version_string()}"
    if solver.check() == _Z3.sat:
        found = solver.model()
        values = {
            name: bool(_Z3.is_true(found.eval(atom, model_completion=True)))
            for name, atom in atoms.items()
        }
        return SolveResult(True, values, [], backend)
    core = [str(b).split("__", 2)[2] for b in solver.unsat_core()]
    return SolveResult(
        False, {}, [n for n in core if n.startswith(FACT_PREFIXES)], backend
    )


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
    negated = base.copy()
    negated.add(f"NEG[{claim_name}]", *[(v, not p) for v, p in claim])
    result = solve(negated, use_z3)
    return (not result.satisfiable), result
