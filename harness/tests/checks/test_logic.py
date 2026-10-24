"""Mutation tests of the logic checks (0, a to f).

Each case damages an in-memory copy of the corpus in one known way (its
mutation's docstring names the injected defect) and asserts that the
named checks fail. Nothing is written to disk. Ported from
``archive/tools-flat/test_logic.py``.
"""

from __future__ import annotations

import copy
import unittest
from collections.abc import Callable
from pathlib import PurePosixPath

from govharness.checks.base import CheckContext
from govharness.checks.registry import LOGIC, run_checks
from tests.support import Index, corpus_of, live_index

Mutation = Callable[[Index], None]


def failed(mutation: Mutation) -> set[str]:
    """Apply a mutation to a copy of the corpus; return the failing keys.

    Parameters
    ----------
    mutation : Mutation
        Damages the index in place.

    Returns
    -------
    set[str]
        Keys of the checks that fail.
    """
    index = live_index()
    mutation(index)
    report = run_checks(LOGIC, CheckContext(corpus_of(index)))
    return {r.key for r in report.failures()}


def duplicate_rank(e: Index) -> None:
    """Rank VV twice and drop QA from the order.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["GOV.5"].body = e["GOV.5"].body.replace("process (QA)", "process (VV)")


def unflagged_prime(e: Index) -> None:
    """Drop the ``waivable`` field of a prime directive.

    The flat code never reported this (defect 1 of unit 0001, fixed by
    review 0001): its branch for a missing flag tested ``level !=
    "LVL0"`` where only LVL0 provisions arrive.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    del e["PRIME.2"].meta["waivable"]


def wrong_front_rank(e: Index) -> None:
    """Give GUARD.3 a rank its part does not have.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["GUARD.3"].meta["rank"] = 2


def waivable_prime(e: Index) -> None:
    """Mark a prime directive waivable.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["PRIME.2"].meta["waivable"] = True


def guard_waivable_by_text(e: Index) -> None:
    """Let the waiver clause relieve GUARD.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["GOV.44"].body = e["GOV.44"].body.replace(
        "obligation of VV,", "obligation of GUARD, VV,"
    )


def tighten_drops_waiver(e: Index) -> None:
    """Remove the waiver citation from the tighten-only clause.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["PRIME.15"].meta["cites"] = ["GOV.3", "GOV.40"]
    e["PRIME.15"].body = e["PRIME.15"].body.replace("(GOV.44)", "")


def free_and_never(e: Index) -> None:
    """Make one sentence both free and never.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["PRIME.2"].body += " An agent is free to push and NEVER pushes."


def standing_cover_irrecoverable(e: Index) -> None:
    """Put an irrecoverable action under a standing authorization.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e[
        "GUARD.2"
    ].body += " Cleanup proceeds within a standing authorization (GUARD.5)."
    e["GUARD.2"].meta["cites"] = [*e["GUARD.2"].meta["cites"], "GUARD.5"]


def bars_expression(e: Index) -> None:
    """Use an expression LVL0 bars.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["VV.1"].body += " An agent may not skip the test."


def unresolved_term_target(e: Index) -> None:
    """Point a Lexicon term at a provision that does not exist.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["LEX.agent"].meta["governed_by"] = ["GOV.999"]


def duplicate_term(e: Index) -> None:
    """Define the same term twice.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    twin = copy.deepcopy(e["LEX.agent"])
    twin.meta["id"] = "LEX.agent-twin"
    twin.path = PurePosixPath("LEX/agent-twin.md")
    e["LEX.agent-twin"] = twin


def uncited_reference(e: Index) -> None:
    """Name an identifier in the text that the index omits.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["VV.1"].body += " See also QA.1."


def waivable_by_text(e: Index) -> None:
    """State that a guard provision MAY be waived.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["GUARD.9"].body += " This MAY be waived."


CASES: dict[str, tuple[Mutation, set[str]]] = {
    "duplicate rank": (duplicate_rank, {"a.1", "a.2"}),
    "front-matter rank": (wrong_front_rank, {"a.3"}),
    "waivable prime": (waivable_prime, {"b.2"}),
    "unflagged prime": (unflagged_prime, {"b.2"}),
    "guard waivable": (guard_waivable_by_text, {"b.3", "f.1"}),
    "tighten drops waiver": (tighten_drops_waiver, {"b.4"}),
    "free and never": (free_and_never, {"c.1", "f.1"}),
    "standing cover": (standing_cover_irrecoverable, {"c.5", "f.1"}),
    "barred expression": (bars_expression, {"d.1"}),
    "bad term target": (unresolved_term_target, {"e.2"}),
    "duplicate term": (duplicate_term, {"e.3"}),
    "uncited reference": (uncited_reference, {"c.2"}),
    "waivable by text": (waivable_by_text, {"b.3", "f.1"}),
}


class LogicChecks(unittest.TestCase):
    """Each injected defect is caught; the clean corpus is not flagged."""

    def test_clean_corpus_has_no_failure(self) -> None:
        """Behavior: the undamaged corpus fails no logic check.

        Reference: the live corpus at the baseline, which the custodian
        verified; a failure here is a false positive.
        """
        self.assertEqual(failed(lambda e: None), set())

    def test_mutations_are_caught(self) -> None:
        """Behavior: each injected defect fails at least its named checks.

        Reference: the defect each case injects (CASES); a pass means
        the checks can fail, which a clean run alone does not show.
        """
        for name, (mutation, expected) in CASES.items():
            with self.subTest(name):
                self.assertTrue(
                    expected <= failed(mutation),
                    f"{name}: expected {expected}",
                )


if __name__ == "__main__":
    unittest.main()
