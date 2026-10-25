"""Reuse of solver results whose inputs are unchanged (unit 0011).

A solve is keyed by a SHA-256 digest of everything its result depends
on: a format tag, the version of the solver code, the backend (the
built-in solver, or z3 and its version), and every clause of the set in
order, its name and its literals in order. The built-in solver's model
and core depend on the order of the clauses and of their literals (the
split order, the numbering of variables, the order of the core
minimisation), and z3 receives the clauses in that order, so the key
keeps every order; a claim enters the key as the clause of its negation,
whose name is the claim's title.

This module computes on data. The caller loads the entries of the keys
a run will use (``SolveCache.known``) before the run, and saves the
entries the run computed (``SolveCache.fresh``) after it; the checks
read and write no file. An entry holds the status, the backend, the
model as one bit a variable, and the core as positions in the clause
set: no text of the corpus. An entry is reused only after a check that
a planted entry cannot pass with a wrong verdict: a model must satisfy
every clause, and the axioms with a core's facts must be unsatisfiable;
for the built-in solver the core must also be exactly the one its
minimisation finds, so a reused core is the fresh one. A model is
checked only for satisfying the clauses, not for being the model a
fresh solve finds; no check, report, or output shows a model. Any
entry that is malformed, of another key, format, or backend, or fails
its check, is ignored, recorded in ``rejected``, and recomputed.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from govharness.checks.logic.satlib import (
    BUILTIN,
    ClauseSet,
    SolveResult,
    backend_name,
    confirms_core,
    satisfies,
    solve,
)
from govharness.core.hashing import canonical_json

FORMAT = 1  # raised whenever the key or the entry changes meaning
TAG = "govharness-solve"
KEY_LENGTH = 64


@dataclass
class SolveCache:
    """Solver results of one run: those found before it and those made.

    Parameters
    ----------
    version : str
        Digest of the solver code; it enters every key, so that a change
        of the code that computes a result is a new key.
    known : dict[str, bytes]
        Entries loaded before the run, by key.
    fresh : dict[str, bytes]
        Entries computed in the run, by key, for the caller to save.
    hits : list[str]
        Keys whose loaded entry was checked and reused.
    rejected : dict[str, str]
        Keys whose loaded entry was ignored, with the reason.
    """

    version: str
    known: dict[str, bytes] = field(default_factory=dict)
    fresh: dict[str, bytes] = field(default_factory=dict)
    hits: list[str] = field(default_factory=list)
    rejected: dict[str, str] = field(default_factory=dict)


def key_start(version: str, backend: str) -> Any:
    """Return a digest that has taken in everything but the clauses.

    Parameters
    ----------
    version : str
        Digest of the solver code.
    backend : str
        Backend that solves (``satlib.backend_name``).

    Returns
    -------
    Any
        A ``hashlib`` SHA-256 object; ``add_clauses`` extends it.
    """
    digest = hashlib.sha256()
    digest.update(canonical_json([TAG, FORMAT, version, backend]).encode())
    digest.update(b"\n")
    return digest


def add_clauses(digest: Any, clause_set: ClauseSet, start: int = 0) -> Any:
    """Extend a key digest with clauses, one canonical line each.

    Parameters
    ----------
    digest : Any
        A digest from ``key_start`` or from an earlier call; extended in
        place.
    clause_set : ClauseSet
        The clauses.
    start : int
        Position of the first clause to add, so that a set that extends
        another by a clause extends a copy of the other's digest.

    Returns
    -------
    Any
        The same digest. Each clause is the canonical JSON of its name
        and literals, which escapes every line feed, so the lines
        delimit the clauses and the key determines the ordered set.
    """
    for name, literals in clause_set.clauses[start:]:
        line = canonical_json([name, [[v, p] for v, p in literals]])
        digest.update(line.encode())
        digest.update(b"\n")
    return digest


def solve_key(clause_set: ClauseSet, version: str, backend: str) -> str:
    """Return the key of solving a clause set.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses.
    version : str
        Digest of the solver code.
    backend : str
        Backend that solves.

    Returns
    -------
    str
        Hexadecimal SHA-256.
    """
    return add_clauses(key_start(version, backend), clause_set).hexdigest()


def encode_entry(key: str, result: SolveResult) -> bytes:
    """Serialize a solver result as a cache entry.

    Parameters
    ----------
    key : str
        Key of the solve.
    result : SolveResult
        Its result.

    Returns
    -------
    bytes
        Canonical JSON: the format, the key, the status, the backend,
        and the model as a string of ``0`` and ``1`` in the order of its
        variables, or the core as positions in the clause set.
    """
    entry: dict[str, Any] = {
        "format": FORMAT,
        "key": key,
        "satisfiable": result.satisfiable,
        "backend": result.backend,
    }
    if result.satisfiable:
        entry["model"] = "".join(
            "1" if v else "0" for v in result.model.values()
        )
    else:
        entry["core"] = list(result.positions)
    return canonical_json(entry).encode()


def decode_entry(
    data: bytes, key: str, clause_set: ClauseSet, backend: str
) -> tuple[SolveResult | None, str]:
    """Rebuild a result from an entry, if it passes its check.

    Parameters
    ----------
    data : bytes
        The entry as loaded.
    key : str
        Key it was loaded under.
    clause_set : ClauseSet
        The clauses the key names.
    backend : str
        Backend the run would use.

    Returns
    -------
    tuple[SolveResult | None, str]
        The result, or ``None`` with the reason it was refused.
    """
    try:
        entry = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None, "not JSON"
    if not isinstance(entry, dict):
        return None, "not an object"
    if entry.get("format") != FORMAT:
        return None, "another format"
    if entry.get("key") != key:
        return None, "another key"
    if entry.get("backend") != backend:
        return None, "another backend"
    status = entry.get("satisfiable")
    if status is True:
        return _model_result(entry, clause_set, backend)
    if status is False:
        return _core_result(entry, clause_set, backend)
    return None, "no status"


def _model_result(
    entry: dict[str, Any], clause_set: ClauseSet, backend: str
) -> tuple[SolveResult | None, str]:
    """Rebuild a satisfiable result whose model satisfies every clause.

    Parameters
    ----------
    entry : dict[str, Any]
        Parsed entry.
    clause_set : ClauseSet
        The clauses.
    backend : str
        Backend of the entry.

    Returns
    -------
    tuple[SolveResult | None, str]
        The result, or ``None`` with the reason.
    """
    bits = entry.get("model")
    names = clause_set.variables()
    if (
        not isinstance(bits, str)
        or len(bits) != len(names)
        or set(bits) - {"0", "1"}
        or "core" in entry
    ):
        return None, "malformed model"
    model = {n: b == "1" for n, b in zip(names, bits, strict=True)}
    if not satisfies(clause_set, model):
        return None, "the model fails a clause"
    return SolveResult(True, model, [], backend), ""


def _core_result(
    entry: dict[str, Any], clause_set: ClauseSet, backend: str
) -> tuple[SolveResult | None, str]:
    """Rebuild an unsatisfiable result whose core is confirmed.

    Parameters
    ----------
    entry : dict[str, Any]
        Parsed entry.
    clause_set : ClauseSet
        The clauses.
    backend : str
        Backend of the entry; the built-in solver's core must be exactly
        the one it finds.

    Returns
    -------
    tuple[SolveResult | None, str]
        The result, or ``None`` with the reason.
    """
    positions = entry.get("core")
    if (
        not isinstance(positions, list)
        or not all(type(p) is int for p in positions)
        or "model" in entry
    ):
        return None, "malformed core"
    if not confirms_core(clause_set, positions, exact=backend == BUILTIN):
        return None, "the core is not confirmed"
    core = [clause_set.clauses[p][0] for p in positions]
    return SolveResult(False, {}, core, backend, list(positions)), ""


def solve_cached(
    clause_set: ClauseSet,
    use_z3: bool,
    cache: SolveCache | None,
    key: str | None = None,
) -> SolveResult:
    """Solve, reusing a checked entry of the cache when one is known.

    Parameters
    ----------
    clause_set : ClauseSet
        The clauses to solve.
    use_z3 : bool
        Whether z3 may be used.
    cache : SolveCache | None
        Entries of the run; ``None`` always solves.
    key : str | None
        Key of the solve when the caller has computed it; ``None``
        computes it.

    Returns
    -------
    SolveResult
        The result of ``satlib.solve``, or the same result rebuilt from
        a checked entry.
    """
    if cache is None:
        return solve(clause_set, use_z3)
    backend = backend_name(use_z3)
    if key is None:
        key = solve_key(clause_set, cache.version, backend)
    data = cache.known.get(key)
    if data is not None:
        result, reason = decode_entry(data, key, clause_set, backend)
        if result is not None:
            cache.hits.append(key)
            return result
        cache.rejected[key] = reason
    result = solve(clause_set, use_z3)
    cache.fresh[key] = encode_entry(key, result)
    return result
