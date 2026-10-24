"""Tests of the check registry (decision 0001, DSGN.11)."""

from __future__ import annotations

import unittest

from govharness.checks.base import Check
from govharness.checks.registry import LOGIC, STRUCTURE
from govharness.core.locators import reference_resolves
from tests.support import live_index

FAMILIES = {
    "structure",
    "manifests",
    "ledger",
    "lineage",
    "drafting",
    "revisions",
    "logic",
}


def registered() -> list[Check]:
    """Return every registered check, in registry order.

    Returns
    -------
    list[Check]
        Checks of the structural and the logic families.
    """
    return [c for family in (*STRUCTURE, *LOGIC) for c in family.CHECKS]


class Registry(unittest.TestCase):
    """Every check is registered once, in a decided family."""

    def test_keys_are_unique(self) -> None:
        """Behavior: no two registered checks share a key.

        Reference: ``checked_by`` fields cite keys, so a key names one
        check (decision 0001).
        """
        keys = [c.key for c in registered()]
        self.assertEqual(len(keys), len(set(keys)))

    def test_families_are_decided(self) -> None:
        """Behavior: every check belongs to a family the decision names.

        Reference: the family list of decision 0001.
        """
        for check in registered():
            with self.subTest(check.key):
                self.assertIn(check.family, FAMILIES)

    def test_enforced_provisions_exist(self) -> None:
        """Behavior: what each check enforces resolves in the corpus.

        Reference: the live corpus; an identifier that resolves to
        nothing would make ``enforces`` a dangling citation.
        """
        index = live_index()
        for check in registered():
            for ident in check.enforces:
                with self.subTest(f"{check.key}: {ident}"):
                    self.assertTrue(reference_resolves(ident, index))


if __name__ == "__main__":
    unittest.main()
