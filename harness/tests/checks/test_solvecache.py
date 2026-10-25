"""Tests of the reuse of solver results (unit 0011), on data only.

The cache is keyed by a digest of everything a result depends on, and
an entry is reused only after a check. These tests compare reused
results with fresh solves, change each input of the key, damage
entries, and plant wrong ones, on random clause sets and on the live
corpus. Nothing here reads or writes a file of the cache;
``tests/workflows/test_solve_store.py`` tests the store on disk.
"""

from __future__ import annotations

import json
import random
import unittest
from unittest import mock

from govharness.checks.base import CheckContext
from govharness.checks.logic import satlib
from govharness.checks.logic.proofs import (
    _negations_of,
    base_of,
    planned_keys,
)
from govharness.checks.logic.satlib import (
    BUILTIN,
    FACT_PREFIXES,
    ClauseSet,
    SolveResult,
    confirms_core,
    negation,
    solve,
)
from govharness.checks.logic.solvecache import (
    FORMAT,
    SolveCache,
    decode_entry,
    encode_entry,
    solve_cached,
    solve_key,
)
from govharness.checks.registry import LOGIC, run_checks
from govharness.core.report import Report
from tests.checks.test_logic import free_and_never
from tests.checks.test_satlib import random_clause_set
from tests.support import Index, corpus_of, live_index

VERSION = "0" * 64  # a solver version for the tests
SEED = 11  # seed of the random clause sets: unit 0011
FORMULAS = 400


def two_cores() -> ClauseSet:
    """Return an unsatisfiable set with two minimal cores of facts.

    Returns
    -------
    ClauseSet
        Facts ``a``, ``not a``, ``b``, ``not b``; the built-in solver's
        core is the second pair, positions 2 and 3.
    """
    clause_set = ClauseSet()
    clause_set.fact("fact:a", "a")
    clause_set.fact("fact:not-a", "a", False)
    clause_set.fact("fact:b", "b")
    clause_set.fact("fact:not-b", "b", False)
    return clause_set


def entry(key: str, **fields: object) -> bytes:
    """Return an entry with the given fields over well-formed defaults.

    Parameters
    ----------
    key : str
        Key of the entry.
    **fields : object
        Fields to set or override.

    Returns
    -------
    bytes
        The JSON of the entry.
    """
    data: dict[str, object] = {
        "format": FORMAT,
        "key": key,
        "backend": BUILTIN,
    }
    data.update(fields)
    return json.dumps(data).encode()


def logic_report(
    index: Index, cache: SolveCache | None = None
) -> tuple[Report, CheckContext]:
    """Run the logic checks on an index, with a cache if given.

    Parameters
    ----------
    index : Index
        Entries by identifier.
    cache : SolveCache | None
        Entries known before the run; ``None`` for no cache.

    Returns
    -------
    tuple[Report, CheckContext]
        The report and the context of the run.
    """
    ctx = CheckContext(corpus_of(index), use_z3=False, solve_cache=cache)
    return run_checks(LOGIC, ctx), ctx


def rendered(report: Report) -> str:
    """Return a report as ``check --out-dir`` writes it.

    Parameters
    ----------
    report : Report
        Results of a run.

    Returns
    -------
    str
        The Markdown of ``logic_report.md``, with a fixed header.
    """
    return report.render(["Corpus: `governance`"])


class Keys(unittest.TestCase):
    """A key changes whenever an input of the result changes."""

    def test_any_change_of_an_input_changes_the_key(self) -> None:
        """Behavior: the key changes with each clause, its name, its
        literals and their order, the order of the clauses, the claim,
        the backend, and the solver version; equal inputs give equal
        keys.

        Reference: a base of three clauses and one change of each kind.
        """
        base = ClauseSet()
        base.add("axiom:x", ("a", True), ("b", False))
        base.fact("fact:a", "a")
        base.fact("fact:b", "b")
        key = solve_key(base, VERSION, BUILTIN)
        same = ClauseSet([(n, list(c)) for n, c in base.clauses])
        self.assertEqual(solve_key(same, VERSION, BUILTIN), key)
        changed = {
            "added clause": base.clauses + [("fact:c", [("c", True)])],
            "renamed clause": [("fact:z", base.clauses[0][1])]
            + base.clauses[1:],
            "polarity": [("axiom:x", [("a", True), ("b", True)])]
            + base.clauses[1:],
            "literal order": [("axiom:x", [("b", False), ("a", True)])]
            + base.clauses[1:],
            "clause order": base.clauses[::-1],
            "repeated literal": [
                ("axiom:x", [("a", True), ("b", False), ("b", False)])
            ]
            + base.clauses[1:],
        }
        keys = {key}
        for label, clauses in changed.items():
            with self.subTest(label):
                other = solve_key(ClauseSet(clauses), VERSION, BUILTIN)
                self.assertNotIn(other, keys)
                keys.add(other)
        claims = [
            negation(base, "claim", [("a", True)]),
            negation(base, "another claim", [("a", True)]),
            negation(base, "claim", [("a", True), ("b", True)]),
        ]
        for claim in claims:
            other = solve_key(claim, VERSION, BUILTIN)
            self.assertNotIn(other, keys)
            keys.add(other)
        for backend, version in (
            ("z3 4.13.0", VERSION),
            ("z3 4.13.1", VERSION),
            (BUILTIN, "1" * 64),
        ):
            other = solve_key(base, version, backend)
            self.assertNotIn(other, keys)
            keys.add(other)

    def test_planned_keys_are_the_keys_of_the_solves(self) -> None:
        """Behavior: the keys the proofs plan before a run, by extending
        the base's digest, equal the keys of the clause sets solved.

        Reference: the live corpus; the base and each claim's negation
        keyed whole by ``solve_key``.
        """
        ctx = CheckContext(
            corpus_of(live_index()),
            use_z3=False,
            solve_cache=SolveCache(VERSION),
        )
        sets = [base_of(ctx)] + [
            negated for _, negated in ctx.shared(_negations_of).values()
        ]
        self.assertEqual(
            planned_keys(ctx),
            [solve_key(s, VERSION, BUILTIN) for s in sets],
        )
        self.assertEqual(len(planned_keys(ctx)), 8)


class Entries(unittest.TestCase):
    """An entry rebuilds the fresh result exactly, or is refused."""

    def test_round_trip_equals_a_fresh_solve(self) -> None:
        """Behavior: an entry of a fresh result decodes to a result equal
        to the fresh one: status, model, core, positions, backend.

        Reference: 400 seeded random clause sets with duplicate names,
        repeated literals, and empty clauses.
        """
        rng = random.Random(SEED)
        for number in range(FORMULAS):
            clause_set = random_clause_set(rng)
            if rng.random() < 0.3 and clause_set.clauses:
                name, literals = clause_set.clauses[0]
                clause_set.add(name, *literals)  # a repeated name
            fresh = solve(clause_set, use_z3=False)
            key = solve_key(clause_set, VERSION, BUILTIN)
            with self.subTest(formula=number):
                decoded, reason = decode_entry(
                    encode_entry(key, fresh), key, clause_set, BUILTIN
                )
                self.assertEqual(reason, "")
                self.assertEqual(decoded, fresh)
                self.assertEqual(list(decoded.model), list(fresh.model))

    def test_a_hit_solves_nothing_and_a_miss_saves(self) -> None:
        """Behavior: a first solve misses and leaves a fresh entry; a
        second, with that entry known, reuses it and adds none.

        Reference: the two-core set of four facts.
        """
        clause_set = two_cores()
        first = SolveCache(VERSION)
        fresh = solve_cached(clause_set, False, first)
        self.assertEqual(fresh, solve(clause_set, use_z3=False))
        self.assertEqual(len(first.fresh), 1)
        second = SolveCache(VERSION, known=dict(first.fresh))
        self.assertEqual(solve_cached(clause_set, False, second), fresh)
        self.assertEqual(second.hits, list(first.fresh))
        self.assertEqual(second.fresh, {})

    def test_corrupt_entries_are_recomputed(self) -> None:
        """Behavior: a truncated, non-JSON, or malformed entry, or one of
        another key, format, or backend, is refused with a reason and
        the result is computed afresh and saved.

        Reference: the good entry of the two-core set, damaged in each
        way.
        """
        clause_set = two_cores()
        key = solve_key(clause_set, VERSION, BUILTIN)
        fresh = solve(clause_set, use_z3=False)
        good = encode_entry(key, fresh)
        damaged = {
            "truncated": good[: len(good) // 2],
            "empty": b"",
            "binary": b"\xff\xfe\x00",
            "nested": b"[" * 100000,
            "list": b"[]",
            "other key": entry("f" * 64, satisfiable=False, core=[2, 3]),
            "other format": entry(key, format=0, satisfiable=False),
            "other backend": entry(
                key, backend="z3 4.13.0", satisfiable=False, core=[2, 3]
            ),
            "no status": entry(key, core=[2, 3]),
            "status as text": entry(key, satisfiable="false", core=[2, 3]),
            "core as text": entry(key, satisfiable=False, core="2,3"),
            "boolean position": entry(key, satisfiable=False, core=[True]),
            "both fields": entry(
                key, satisfiable=False, core=[2, 3], model="0"
            ),
        }
        for label, data in damaged.items():
            with self.subTest(label):
                cache = SolveCache(VERSION, known={key: data})
                self.assertEqual(solve_cached(clause_set, False, cache), fresh)
                self.assertIn(key, cache.rejected)
                self.assertEqual(cache.fresh, {key: good})


class PlantedEntries(unittest.TestCase):
    """A wrong entry with the right key is refused by its check."""

    def test_wrong_status_is_refused(self) -> None:
        """Behavior: a satisfiable entry for an unsatisfiable set, and an
        unsatisfiable one for a satisfiable set, are refused.

        Reference: the two-core set with an all-false model; its facts
        ``a`` and ``b`` alone, with each core a planter could name.
        """
        unsat = two_cores()
        key = solve_key(unsat, VERSION, BUILTIN)
        planted = entry(key, satisfiable=True, model="00")
        self.assertEqual(
            decode_entry(planted, key, unsat, BUILTIN),
            (None, "the model fails a clause"),
        )
        sat = ClauseSet([unsat.clauses[0], unsat.clauses[2]])
        key = solve_key(sat, VERSION, BUILTIN)
        for core in ([], [0], [0, 1], [1]):
            with self.subTest(core=core):
                planted = entry(key, satisfiable=False, core=core)
                self.assertEqual(
                    decode_entry(planted, key, sat, BUILTIN)[0], None
                )

    def test_another_core_is_refused(self) -> None:
        """Behavior: an unsatisfiable entry whose core is not the one the
        built-in solver finds is refused, though the set is
        unsatisfiable: another minimal core, a core that is not
        minimal, an unordered one, a repeated or out-of-range position,
        or the position of an axiom.

        Reference: the two-core set, whose solver core is positions 2
        and 3, and the same set with an axiom in front.
        """
        clause_set = two_cores()
        self.assertEqual(solve(clause_set, use_z3=False).positions, [2, 3])
        key = solve_key(clause_set, VERSION, BUILTIN)
        for core in ([0, 1], [0, 1, 2, 3], [3, 2], [2, 2, 3], [2, 3, 9]):
            with self.subTest(core=core):
                planted = entry(key, satisfiable=False, core=core)
                self.assertIsNone(
                    decode_entry(planted, key, clause_set, BUILTIN)[0]
                )
        with_axiom = ClauseSet([("axiom:c", [("c", True)])])
        with_axiom.clauses += clause_set.clauses
        self.assertFalse(confirms_core(with_axiom, [0, 3, 4]))
        self.assertFalse(confirms_core(with_axiom, [1, 2]))
        self.assertTrue(confirms_core(with_axiom, [3, 4]))

    def test_z3_cores_are_not_reused(self) -> None:
        """Behavior: an unsatisfiable z3 entry is refused, even one whose
        core refutes, since a fresh z3 run could list other core facts.

        Reference: the two-core set: either pair refutes.
        """
        clause_set = two_cores()
        backend = "z3 4.13.0"
        key = solve_key(clause_set, VERSION, backend)
        for core in ([0, 1], [3, 2], [0]):
            with self.subTest(core=core):
                planted = entry(
                    key, backend=backend, satisfiable=False, core=core
                )
                self.assertEqual(
                    decode_entry(planted, key, clause_set, backend),
                    (None, "a z3 core is not reused"),
                )

    def test_planted_entries_change_no_verdict_of_the_corpus(self) -> None:
        """Behavior: on the live corpus, an entry of the opposite status
        planted under every key of the run, and a core naming every fact
        under the key of each refuted claim, are each refused, and the
        report is the fresh one, byte for byte.

        Reference: the live corpus and a fresh run without a cache. An
        accepted planted entry would turn f.1 or a claim to FAIL, or
        change its core facts.
        """
        fresh, ctx = logic_report(live_index())
        expected = rendered(fresh)
        cache = SolveCache(VERSION)
        keys = planned_keys(
            CheckContext(ctx.corpus, use_z3=False, solve_cache=cache)
        )
        base = base_of(ctx)
        facts = [
            p
            for p, (name, _) in enumerate(base.clauses)
            if name.startswith(FACT_PREFIXES)
        ]
        variables = len(base.variables())
        opposite = {
            keys[0]: entry(keys[0], satisfiable=False, core=facts),
            **{
                k: entry(k, satisfiable=True, model="0" * variables)
                for k in keys[1:]
            },
        }
        every_fact = {
            k: entry(k, satisfiable=False, core=[*facts, len(base.clauses)])
            for k in keys[1:]
        }
        for label, planted in (
            ("opposite", opposite),
            ("every fact", every_fact),
        ):
            with self.subTest(label):
                cache = SolveCache(VERSION, known=dict(planted))
                report, _ = logic_report(live_index(), cache)
                self.assertEqual(rendered(report), expected)
                self.assertEqual(cache.hits, [])
                used = [k for k in planted if k in cache.fresh]
                self.assertEqual(sorted(cache.rejected), sorted(used))
                self.assertGreaterEqual(len(used), 7)

    def test_planted_pass_of_a_damaged_corpus_is_refused(self) -> None:
        """Behavior: a corpus whose facts contradict fails f.1 with its
        core whatever the cache holds: a planted satisfiable entry for
        its base is refused.

        Reference: the mutation of test_logic that puts one action in
        the free and the never tiers, which fails f.1.
        """
        index = live_index()
        free_and_never(index)
        fresh, ctx = logic_report(index)
        self.assertIn("f.1", {r.key for r in fresh.failures()})
        cache = SolveCache(VERSION)
        key = planned_keys(
            CheckContext(ctx.corpus, use_z3=False, solve_cache=cache)
        )[0]
        model = "0" * len(base_of(ctx).variables())
        cache = SolveCache(
            VERSION, known={key: entry(key, satisfiable=True, model=model)}
        )
        damaged = live_index()
        free_and_never(damaged)
        report, _ = logic_report(damaged, cache)
        self.assertEqual(rendered(report), rendered(fresh))
        self.assertEqual(cache.rejected, {key: "the model fails a clause"})


class StubZ3:
    """A stand-in for the z3 module, solving with the built-in solver.

    It offers what ``satlib.solve_z3`` calls. Atoms are their names and a
    tracker is its name, so ``str`` of a core item is the tracking name
    ``solve_z3`` writes, ``__track_<position>__<clause name>``. The core
    it reports is the built-in core with one axiom tracker added, which
    ``solve_z3`` must drop, in reverse order, which it must keep.
    """

    sat = "sat"
    VERSION = "4.99.0"

    @staticmethod
    def Bool(name: str) -> str:
        """Return an atom, its name.

        Parameters
        ----------
        name : str
            Name of the atom or tracker.

        Returns
        -------
        str
            The name.
        """
        return name

    @staticmethod
    def Not(atom: str) -> tuple[str, str]:
        """Return a negated atom.

        Parameters
        ----------
        atom : str
            The atom.

        Returns
        -------
        tuple[str, str]
            ``("not", atom)``.
        """
        return ("not", atom)

    @staticmethod
    def Or(*terms: object) -> tuple[object, ...]:
        """Return a clause, its terms.

        Parameters
        ----------
        *terms : object
            Atoms and negated atoms.

        Returns
        -------
        tuple[object, ...]
            The terms.
        """
        return terms

    @staticmethod
    def is_true(value: object) -> bool:
        """Return whether a model value is true.

        Parameters
        ----------
        value : object
            A value from ``Model.eval``.

        Returns
        -------
        bool
            Whether it is ``True``.
        """
        return value is True

    @classmethod
    def get_version_string(cls) -> str:
        """Return the stub's version.

        Returns
        -------
        str
            ``VERSION``.
        """
        return cls.VERSION

    class Model:
        """A model of the built-in solver, read as z3's.

        Parameters
        ----------
        values : dict[str, bool]
            Value of each variable.
        """

        def __init__(self, values: dict[str, bool]) -> None:
            """Keep the values.

            Parameters
            ----------
            values : dict[str, bool]
                Value of each variable.
            """
            self.values = values

        def eval(self, atom: str, model_completion: bool) -> bool:
            """Return the value of an atom.

            Parameters
            ----------
            atom : str
                The atom.
            model_completion : bool
                Ignored; every atom has a value.

            Returns
            -------
            bool
                Its value.
            """
            return self.values[atom]

    class Solver:
        """A solver over tracked clauses."""

        def __init__(self) -> None:
            """Start with no clause."""
            self.tracked: list[tuple[tuple[object, ...], str]] = []
            self.result: SolveResult | None = None

        def set(self, **options: object) -> None:
            """Accept options.

            Parameters
            ----------
            **options : object
                Ignored.
            """

        def assert_and_track(
            self, clause: tuple[object, ...], tracker: str
        ) -> None:
            """Add a clause with its tracker.

            Parameters
            ----------
            clause : tuple[object, ...]
                Terms of the clause.
            tracker : str
                Tracking name.
            """
            self.tracked.append((clause, tracker))

        def check(self) -> str:
            """Solve the tracked clauses with the built-in solver.

            Returns
            -------
            str
                ``sat`` or ``unsat``.
            """
            clause_set = ClauseSet()
            for clause, tracker in self.tracked:
                literals = [
                    (t[1], False) if isinstance(t, tuple) else (str(t), True)
                    for t in clause
                ]
                clause_set.add(tracker.split("__", 2)[2], *literals)
            self.result = solve(clause_set, use_z3=False)
            return "sat" if self.result.satisfiable else "unsat"

        def model(self) -> StubZ3.Model:
            """Return the model found.

            Returns
            -------
            StubZ3.Model
                The built-in model.
            """
            assert self.result is not None
            return StubZ3.Model(self.result.model)

        def unsat_core(self) -> list[str]:
            """Return the trackers of a core, an axiom's among them.

            Returns
            -------
            list[str]
                Trackers of the built-in core and of the first axiom,
                in reverse order.
            """
            assert self.result is not None
            trackers = [self.tracked[p][1] for p in self.result.positions]
            axioms = [
                t
                for _, t in self.tracked
                if not t.split("__", 2)[2].startswith(FACT_PREFIXES)
            ]
            return (trackers + axioms[:1])[::-1]


class Z3Path(unittest.TestCase):
    """The z3 path runs against a stub, since z3 is not installed."""

    def setUp(self) -> None:
        """Put the stub in place of z3 for each test."""
        patcher = mock.patch.object(satlib, "_Z3", StubZ3)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_core_positions_are_parsed(self) -> None:
        """Behavior: ``solve_z3`` reads each core position and name from
        its tracking names, drops the axioms, and keeps z3's order, even
        for names that hold ``__`` or are shared by two clauses.

        Reference: the two-core set with an axiom in front and a fact
        named with ``__`` repeated; the stub reports the built-in core,
        reversed, with the axiom.
        """
        clause_set = ClauseSet([("axiom:x__y", [("c", True)])])
        clause_set.clauses += two_cores().clauses
        clause_set.fact("fact:b", "b", False)
        result = solve(clause_set, use_z3=True)
        fresh = solve(clause_set, use_z3=False)
        self.assertEqual(result.backend, "z3 4.99.0")
        self.assertFalse(result.satisfiable)
        self.assertEqual(result.positions, fresh.positions[::-1])
        self.assertEqual(result.core, fresh.core[::-1])

    def test_z3_model_is_reused_and_core_is_not(self) -> None:
        """Behavior: with z3, a satisfiable result is saved and reused
        after its model is checked; an unsatisfiable one is not saved,
        so it is solved afresh each time.

        Reference: the two-core set's facts ``a`` and ``b`` alone, and
        the set whole.
        """
        whole = two_cores()
        sat = ClauseSet([whole.clauses[0], whole.clauses[2]])
        first = SolveCache(VERSION)
        fresh = solve_cached(sat, True, first)
        self.assertEqual(fresh.backend, "z3 4.99.0")
        second = SolveCache(VERSION, known=dict(first.fresh))
        self.assertEqual(solve_cached(sat, True, second), fresh)
        self.assertEqual(len(second.hits), 1)
        unsat = SolveCache(VERSION)
        self.assertFalse(solve_cached(whole, True, unsat).satisfiable)
        self.assertEqual(unsat.fresh, {})


class Reuse(unittest.TestCase):
    """A warm run reports exactly what a fresh run reports."""

    def test_warm_report_equals_fresh_report(self) -> None:
        """Behavior: on the live corpus, a run with an empty cache and a
        run reusing its entries give the report of a run without a
        cache; the second solves nothing.

        Reference: three runs of the logic checks on the live corpus.
        """
        fresh, _ = logic_report(live_index())
        cold_cache = SolveCache(VERSION)
        cold, _ = logic_report(live_index(), cold_cache)
        warm_cache = SolveCache(VERSION, known=dict(cold_cache.fresh))
        warm, _ = logic_report(live_index(), warm_cache)
        self.assertEqual(rendered(cold), rendered(fresh))
        self.assertEqual(rendered(warm), rendered(fresh))
        self.assertEqual(warm_cache.fresh, {})
        self.assertEqual(warm_cache.rejected, {})
        self.assertEqual(len(warm_cache.hits), 8)
        backend = next(r for r in warm.results if r.key == "f.1").details[0]
        self.assertTrue(backend.startswith(f"Backend: {BUILTIN};"))

    def test_changed_corpus_misses(self) -> None:
        """Behavior: a change of the authority-tier statements gives new
        keys, so a warm cache of the clean corpus serves none of the
        changed solves and the report is the fresh one.

        Reference: the free-and-never mutation, after a run of the
        clean corpus.
        """
        first = SolveCache(VERSION)
        logic_report(live_index(), first)
        index = live_index()
        free_and_never(index)
        fresh, _ = logic_report(index)
        cache = SolveCache(VERSION, known=dict(first.fresh))
        damaged = live_index()
        free_and_never(damaged)
        report, _ = logic_report(damaged, cache)
        self.assertEqual(rendered(report), rendered(fresh))
        self.assertEqual(cache.hits, [])
        self.assertTrue(cache.fresh)

    def test_no_cache_solves_as_before(self) -> None:
        """Behavior: without a cache, ``solve_cached`` is ``solve``.

        Reference: the two-core set.
        """
        clause_set = two_cores()
        result: SolveResult = solve_cached(clause_set, False, None)
        self.assertEqual(result, solve(clause_set, use_z3=False))


if __name__ == "__main__":
    unittest.main()
