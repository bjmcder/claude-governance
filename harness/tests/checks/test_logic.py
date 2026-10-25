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
from types import ModuleType
from unittest import mock

from govharness.checks.base import CheckContext
from govharness.checks.logic import authority, language, proofs
from govharness.checks.logic.facts import Facts
from govharness.checks.logic.satlib import ClauseSet
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


def _replace(rule: str, old: str, new: str) -> Mutation:
    """Return a mutation that rewrites part of a body.

    Parameters
    ----------
    rule : str
        Identifier of the entry.
    old, new : str
        Text replaced, which occurs in the body, and its replacement.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(e: Index) -> None:
        """Replace the text.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        assert old in e[rule].body, old
        e[rule].body = e[rule].body.replace(old, new)

    return apply


def _table_row(rule: str, text: str) -> Mutation:
    """Return a mutation that adds a one-row table to a provision.

    Parameters
    ----------
    rule : str
        Identifier of the provision.
    text : str
        Text of the row's second cell.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(e: Index) -> None:
        """Add the table.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        table = "| Item | Rule |\n| --- | --- |\n"
        e[rule].body += f"\n\n{table}| x | {text} |\n"

    return apply


def _drop_floor_provision(e: Index) -> None:
    """Delete VV.7, which GOV.10 places in the floor.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    del e["VV.7"]


def _unlink_loud_failure(e: Index) -> None:
    """Drop the citation of the safe state from loud failure.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["PRIME.4"].meta["cites"] = []


def _term_without_group(e: Index) -> None:
    """Drop the group of a Lexicon term.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    del e["LEX.agent"].meta["group"]


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
    "missing floor provision": (_drop_floor_provision, {"b.1"}),
    "self-grant cites nothing that resolves": (
        _replace("GOV.48", "waivers (GOV.44)", "waivers (GOV.999)"),
        {"b.5"},
    ),
    "procedures waivable": (
        _replace("GOV.45", "GUARD, GOV,", "GUARD,"),
        {"b.6"},
    ),
    "loud failure unlinked": (_unlink_loud_failure, {"c.3"}),
    "term without group": (_term_without_group, {"e.1"}),
    "prime directives unranked": (
        _replace(
            "GOV.5", "The prime directives outrank every other provision. ", ""
        ),
        {"f.4"},
    ),
    "nothing barred": (
        _replace("LVL0", '"may not" is', "may not is"),
        {"d.0"},
    ),
    "barred expression in a table row": (
        _table_row("STND.PERF.1", "The code may not run."),
        {"d.1"},
    ),
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


def results(
    mutation: Mutation, families: tuple[ModuleType, ...]
) -> dict[str, tuple[str, list[str]]]:
    """Apply a mutation and return each check's status and details.

    Parameters
    ----------
    mutation : Mutation
        Damages the index in place.
    families : tuple[ModuleType, ...]
        Family modules to run.

    Returns
    -------
    dict[str, tuple[str, list[str]]]
        Status and detail lines by check key.
    """
    index = live_index()
    mutation(index)
    report = run_checks(families, CheckContext(corpus_of(index)))
    return {r.key: (r.status, r.details) for r in report.results}


def unchanged(e: Index) -> None:
    """Leave the corpus as it is.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier.
    """


def _uncite_reserved(e: Index) -> None:
    """Remove GUARD.5's citation of PRIME.6; its text still says reserved.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["GUARD.5"].meta["cites"] = []


def _unlink_reserved(e: Index) -> None:
    """Remove GUARD.5's citation of PRIME.6 and the word reserved.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    _uncite_reserved(e)
    e["GUARD.5"].body = e["GUARD.5"].body.replace(
        "each is reserved (PRIME.6)", "each is listed"
    )


def _listed_words(e: Index) -> None:
    """Use SHOULD and prefer, add a table word, and oblige a term.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["GUARD.5"].body += " An agent SHOULD prefer a copy."
    row = "| is a defect |"
    e["LVL0"].body = e["LVL0"].body.replace(
        row, "| is frobbed | x | y |\n" + row
    )
    e["LEX.agent"].body += " An agent SHALL act."


def _without(
    prefixes: tuple[str, ...],
) -> Callable[[Facts, list[str]], ClauseSet]:
    """Return a base builder that drops the clauses of some prefixes.

    Parameters
    ----------
    prefixes : tuple[str, ...]
        Starts of the names of the clauses dropped.

    Returns
    -------
    Callable[[Facts, list[str]], ClauseSet]
        A replacement for ``proofs.build_base``.
    """
    build = proofs.build_base

    def without(facts: Facts, parts: list[str]) -> ClauseSet:
        """Build the base, then drop the clauses.

        Parameters
        ----------
        facts : Facts
            Extracted facts.
        parts : list[str]
            Parts of LVL0.

        Returns
        -------
        ClauseSet
            The base without those clauses.
        """
        base = build(facts, parts)
        base.clauses = [
            c for c in base.clauses if not c[0].startswith(prefixes)
        ]
        return base

    return without


def _forced(facts: Facts, parts: list[str]) -> ClauseSet:
    """Build the base and rank GUARD above PRIN and GOV.

    Parameters
    ----------
    facts : Facts
        Extracted facts.
    parts : list[str]
        Parts of LVL0.

    Returns
    -------
    ClauseSet
        The base with the two facts.
    """
    base = BUILD_BASE(facts, parts)
    for free in ("PRIN", "GOV"):
        base.fact(f"fact:probe GUARD above {free}", f"lt[GUARD<{free}]")
    return base


BUILD_BASE = proofs.build_base
# The clauses of the base whose removal leaves each claim unforced: the
# top part reaches every ranked part through transitivity or the fact
# that PRIME outranks every other part, and a statement leaves standing
# cover through the exclusion facts or through being forbidden.
FORCING = {
    "f.2": ("trans:", "fact:PRIME outranks every other"),
    "f.3": ("asym:",),
    "f.5": ("axiom:non_waivable->no_waiver_path",),
    "f.6": ("fact:PRIME.6 bars standing cover", "axiom:standing->authorized"),
    "f.7": ("axiom:reserved->forbidden",),
}


class HeldBehavior(unittest.TestCase):
    """Behavior that no case above held (QA.8 part C, M2 and M5)."""

    def test_parts_in_neither_set(self) -> None:
        """Behavior: b.3 names the parts that are neither waivable nor
        non-waivable.

        Reference: GOV.44 and GOV.45, which between them name every part
        of the live corpus; QA.8 part C, M5, the mutations of line 258
        of ``authority.py``. Dropping QA from GOV.44 leaves it in
        neither set.
        """
        line = "Parts in neither set: "
        found = results(unchanged, (authority,))["b.3"][1]
        self.assertIn(f"{line}none", found)
        found = results(
            _replace("GOV.44", "RSRC, or QA,", "or RSRC,"), (authority,)
        )["b.3"][1]
        self.assertIn(f"{line}['QA']", found)

    def test_tighten_cites_exactly_the_procedures(self) -> None:
        """Behavior: b.4 passes when the tighten-only clause cites the
        amendment and waiver procedures and nothing else.

        Reference: PRIME.15; QA.8 part C, M5, the mutation of the
        superset test ``<=`` to a strict one.
        """

        def exact(e: Index) -> None:
            """Cite only GOV.40 and GOV.44 from PRIME.15.

            Parameters
            ----------
            e : Index
                Copy of the corpus entries by identifier; changed in
                place.
            """
            e["PRIME.15"].meta["cites"] = ["GOV.40", "GOV.44"]

        self.assertEqual(results(exact, (authority,))["b.4"][0], "PASS")

    def test_reserved_back_links(self) -> None:
        """Behavior: c.4 lists each reserved class that does not point
        back to the reserved clause.

        Reference: PRIME.6 and GUARD.5; QA.8 part C, M5, the mutations
        of lines 485 to 496 of ``authority.py``. In the live corpus
        PRIME.13 is the one class without a link back; GUARD.5 links
        back by citation and by the word reserved, and either suffices.
        """
        back = "- GUARD.5: refers back to PRIME.6: "
        status, details = results(unchanged, (authority,))["c.4"]
        self.assertEqual(status, "INFO")
        self.assertIn("- PRIME.13: refers back to PRIME.6: False", details)
        self.assertIn(f"{back}True", details)
        details = results(_uncite_reserved, (authority,))["c.4"][1]
        self.assertIn(f"{back}True", details)
        details = results(_unlink_reserved, (authority,))["c.4"][1]
        self.assertIn(f"{back}False", details)

    def test_table_rows_in_d1(self) -> None:
        """Behavior: d.1 reads the table rows of a provision, takes a
        quoted expression there as a mention, and leaves out a table
        that the provision names in ``defines``.

        Reference: STND.DRAFT, Normative and informative parts, and
        STND.DRAFT.3; QA.8 part C, M2.
        """
        cases = {
            "quoted": (
                _table_row("STND.PERF.1", 'The words "may not" are barred.'),
                "PASS",
            ),
            "defined table": (
                _table_row("STND.DRAFT.17", "The code may not run."),
                "PASS",
            ),
            "used": (_table_row("STND.PERF.1", "It may not run."), "FAIL"),
        }
        for name, (mutation, want) in cases.items():
            with self.subTest(name):
                status = results(mutation, (language,))["d.1"][0]
                self.assertEqual(status, want)

    def test_listed_words(self) -> None:
        """Behavior: d.0 lists the expressions LVL0 bars, d.3 and d.4
        list uses of SHOULD and prefer, d.5 lists a table word that no
        provision uses, and d.6 warns on an obligation in a definition.

        Reference: LVL0, Normative Language; the README's table of the
        logic checks. QA.8 part C, M5 found no test of d.0 or d.3 to
        d.6.
        """
        clean = results(unchanged, (language,))
        self.assertEqual(clean["d.0"][0], "PASS")
        self.assertIn("Barred by LVL0: ['may not']", clean["d.0"][1])
        self.assertEqual(clean["d.6"][0], "PASS")
        found = results(_listed_words, (language,))
        for key in ("d.3", "d.4"):
            with self.subTest(key):
                status, details = found[key]
                self.assertEqual(status, "INFO")
                self.assertTrue(
                    [d for d in details if d.startswith("- GUARD.5: ")],
                    details,
                )
        self.assertIn("'is frobbed'", found["d.5"][1][0])
        self.assertNotIn("'is frobbed'", clean["d.5"][1][0])
        self.assertEqual(found["d.6"], ("WARN", ["- LEX.agent: SHALL"]))

    def test_claims_proved(self) -> None:
        """Behavior: on the live corpus f.2 to f.7 are entailed and f.8
        is not, and each claim fails, or for f.8 is reported, once the
        clause that forces it is removed or added.

        Reference: GOV.5, GOV.6, GOV.45, and PRIME.6, as the proofs
        encode them; QA.8 part C, M5 found no test of f.2 to f.8. The
        base is changed after it is built, since no damage to the
        corpus removes an axiom.
        """
        clean = results(unchanged, (proofs,))
        for key in ("f.2", "f.3", "f.4", "f.5", "f.6", "f.7"):
            with self.subTest(key):
                self.assertEqual(clean[key][0], "PASS")
                self.assertTrue(clean[key][1][1].startswith("ENTAILED"))
        self.assertEqual(clean["f.8"][0], "PASS")
        self.assertTrue(clean["f.8"][1][1].startswith("NOT ENTAILED"))
        for key, prefixes in FORCING.items():
            with (
                self.subTest(key),
                mock.patch.object(proofs, "build_base", _without(prefixes)),
            ):
                self.assertEqual(results(unchanged, (proofs,))[key][0], "FAIL")
        with mock.patch.object(proofs, "build_base", _forced):
            self.assertEqual(results(unchanged, (proofs,))["f.8"][0], "INFO")


if __name__ == "__main__":
    unittest.main()
