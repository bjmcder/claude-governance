"""The check value, its verdict, and the context checks run in.

A check is a ``Check`` value: a key that ``checked_by`` fields cite, the
family it belongs to, a title, the provisions it enforces, and a
function from the context to a verdict (DSGN.11). A family module lists
its checks in a tuple named ``CHECKS``; ``registry`` lists the family
modules.

Work that several checks share, such as the extracted facts, is computed
once per context through ``CheckContext.shared``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar

from govharness.checks.logic.solvecache import SolveCache
from govharness.core.corpus import Corpus, Tree
from govharness.core.report import Report
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.transactions import Transaction

T = TypeVar("T")


@dataclass
class Verdict:
    """What one check found.

    Parameters
    ----------
    status : str
        ``PASS``, ``FAIL``, ``WARN``, or ``INFO``.
    details : list[str]
        Evidence lines.
    fields : dict[str, str]
        Values for the placeholders of a title that depends on the
        corpus, such as the identifier of the precedence clause.
    """

    status: str
    details: list[str] = field(default_factory=list)
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class CheckContext:
    """The inputs of one run of checks, and the results so far.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus, which may be held in memory only.
    ledger : list[Transaction] | None
        Ledger entries in order; ``None`` when no ledger is supplied.
    tree : Tree | None
        Snapshot of the files under the root, needed only by the
        structural checks.
    signer_config : SignerConfig | None
        Signer anchor and ``gpg`` path for the ledger check; ``None``
        means no anchor.
    use_z3 : bool
        Whether the proofs may use z3 when it is importable.
    solve_cache : SolveCache | None
        Solver results loaded before the run and made in it; ``None``
        solves every time (unit 0011).
    report : Report
        Results reported so far in this run.
    known_keys : frozenset[str]
        Key of every registered check, whichever families this run
        includes; ``registry.run_checks`` sets it, so that a check of
        citations (g.23) does not depend on the order of the run.
    memo : dict[Callable[..., Any], Any]
        Values computed once per run by ``shared``.
    """

    corpus: Corpus
    ledger: list[Transaction] | None = None
    tree: Tree | None = None
    signer_config: SignerConfig | None = None
    use_z3: bool = True
    solve_cache: SolveCache | None = None
    report: Report = field(default_factory=Report)
    known_keys: frozenset[str] = frozenset()
    memo: dict[Callable[..., Any], Any] = field(default_factory=dict)

    def shared(self, compute: Callable[[CheckContext], T]) -> T:
        """Return a value that several checks use, computed once.

        Parameters
        ----------
        compute : Callable[[CheckContext], T]
            Pure function of the context.

        Returns
        -------
        T
            Its value for this context.
        """
        if compute not in self.memo:
            self.memo[compute] = compute(self)
        return self.memo[compute]

    def require_tree(self) -> Tree:
        """Return the file snapshot of a run of structural checks.

        Returns
        -------
        Tree
            The snapshot.

        Raises
        ------
        ValueError
            If the run was given no snapshot.
        """
        if self.tree is None:
            raise ValueError("this check needs the file snapshot")
        return self.tree


@dataclass(frozen=True)
class Check:
    """One registered check.

    Parameters
    ----------
    key : str
        Stable key that ``checked_by`` fields cite; it never changes.
    family : str
        Family the check belongs to.
    title : str
        What the check establishes; placeholders in braces are filled
        from the verdict's fields.
    enforces : tuple[str, ...]
        Identifiers of the provisions or documents it enforces.
    run : Callable[[CheckContext], Verdict | None]
        Computes the verdict, or ``None`` when the check does not apply
        to this corpus.
    """

    key: str
    family: str
    title: str
    enforces: tuple[str, ...]
    run: Callable[[CheckContext], Verdict | None]

    def heading(self, verdict: Verdict) -> str:
        """Return the title with the verdict's fields filled in.

        Parameters
        ----------
        verdict : Verdict
            Verdict of this check.

        Returns
        -------
        str
            The title as reported.
        """
        if not verdict.fields:
            return self.title
        return self.title.format(**verdict.fields)
