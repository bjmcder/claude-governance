"""Verify the corpus at a root: load it, then run every check.

The checks compute on data (``checks.verification``); this module reads
the snapshot of the corpus, its ledger, and the signer configuration
that the human owner keeps (``ledger/gpg.py``). The logic checks reuse
the solver results of the solve cache (``workflows.solve_store``, unit
0011): the entries of the keys a run will use are loaded before it, and
the results it computed are saved after it.
"""

from __future__ import annotations

from pathlib import Path

from govharness.checks.base import CheckContext
from govharness.checks.logic.proofs import planned_keys
from govharness.checks.logic.solvecache import SolveCache
from govharness.checks.registry import LOGIC, run_checks
from govharness.checks.verification import Verification, verify_structure
from govharness.core.corpus import read_tree
from govharness.core.report import Report
from govharness.ledger.chain import read_ledger
from govharness.ledger.gpg import read_config
from govharness.workflows.solve_store import SolveStore, open_store


def run_logic(ctx: CheckContext, store: SolveStore | None) -> Report:
    """Run the logic checks, reusing and saving solver results.

    Parameters
    ----------
    ctx : CheckContext
        A fresh context of the logic checks.
    store : SolveStore | None
        The solve cache; ``None`` solves every time.

    Returns
    -------
    Report
        The results, the same with or without the cache. The keys of
        entries refused are added to ``store.rejected``.
    """
    if store is None:
        return run_checks(LOGIC, ctx)
    ctx.solve_cache = SolveCache(store.version)
    ctx.solve_cache.known = store.load(planned_keys(ctx))
    report = run_checks(LOGIC, ctx)
    store.rejected.update(ctx.solve_cache.rejected)
    store.save(ctx.solve_cache.fresh)
    return report


def usable_store(root: Path, cache: SolveStore | bool) -> SolveStore | None:
    """Return the solve cache for a run on a root, or None.

    Parameters
    ----------
    root : Path
        Corpus root.
    cache : SolveStore | bool
        A store; ``True`` for the one the environment names
        (``open_store``); ``False`` for none.

    Returns
    -------
    SolveStore | None
        The store.

    Raises
    ------
    ValueError
        If the store's directory lies inside the corpus, which the
        cache's files would then change, or the environment names a
        relative directory. A workflow that writes calls this before
        its first write.
    """
    store = open_store() if cache is True else cache or None
    if store is None:
        return None
    if store.inside(root):
        raise ValueError(
            f"the solve cache {store.directory} lies inside the corpus "
            f"{root}; name another directory or use --no-cache"
        )
    return store


def verify_corpus(
    root: Path,
    logic: bool = True,
    use_z3: bool = True,
    cache: SolveStore | bool = False,
) -> Verification:
    """Load the corpus at a root and verify it.

    Parameters
    ----------
    root : Path
        Corpus root.
    logic : bool
        Whether to run the logic checks.
    use_z3 : bool
        Whether the proofs may use z3 when it is importable.
    cache : SolveStore | bool
        The solve cache: a store, ``True`` for the one the environment
        names, or ``False``, the default, for none, so that a library
        caller writes no cache unless it asks. The results are the same
        in every case.

    Returns
    -------
    Verification
        The results.

    Raises
    ------
    ValueError
        If the solve cache lies inside the corpus.
    """
    store = usable_store(root, cache) if logic else None
    tree = read_tree(root)
    ledger = read_ledger(root)
    corpus, found = verify_structure(tree, ledger, read_config())
    if logic:
        ctx = CheckContext(corpus, ledger, use_z3=use_z3)
        found.logic = run_logic(ctx, store)
    return found
