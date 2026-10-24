"""Tests of checks m.1 and m.2 and of the review pairs (STND.HARN.26 to 28).

Each test damages an in-memory copy of the live corpus and asserts the
named check reaches FAIL, so that a pass on the clean corpus is
evidence. The pair listing is compared with the review of NUMER 1.0,
whose 61 pairs an agent listed by reading before the code existed.
"""

from __future__ import annotations

import unittest

from govharness.checks.base import CheckContext
from govharness.checks.combination import matters_owned, selectors_defined
from govharness.query.combination import review_pairs
from tests.support import corpus_of, live_index

# The pairs listed by hand for the adoption of NUMER (ledger entry 59),
# counted once per pair; claude/drafts/numer-1.0-harn28-review.md.
NUMER_REVIEWED = 61


def status_of(index: dict, check: object) -> str:
    """Return the status a check reaches on a corpus index.

    Parameters
    ----------
    index : dict
        Entries by identifier.
    check : object
        A check function of the combination family.

    Returns
    -------
    str
        The verdict's status, or ``NONE`` when the check does not apply.
    """
    verdict = check(CheckContext(corpus_of(index)))  # type: ignore[operator]
    return "NONE" if verdict is None else verdict.status


class Combination(unittest.TestCase):
    """The combination checks pass the live corpus and catch damage."""

    def test_live_corpus_passes(self) -> None:
        """Behavior: m.1 and m.2 pass the live corpus.

        Reference: NUMER 1.0, adopted with its attribute defined and one
        owner per shared matter (ledger entry 59).
        """
        index = live_index()
        self.assertEqual(status_of(index, selectors_defined), "PASS")
        self.assertEqual(status_of(index, matters_owned), "PASS")

    def test_undefined_attribute_fails(self) -> None:
        """Behavior: m.1 fails when the Terms lose the attribute.

        Reference: STND.HARN.26; the NUMER Terms row for Numerical is
        renamed.
        """
        index = live_index()
        doc = index["NUMER"]
        doc.body = doc.body.replace("| Numerical |", "| Numeric work |", 1)
        self.assertEqual(status_of(index, selectors_defined), "FAIL")

    def test_second_owner_fails(self) -> None:
        """Behavior: m.2 fails on a matter with two owning profiles.

        Reference: STND.HARN.27; a NUMER row is copied with AGENT as
        its owner.
        """
        index = live_index()
        prov = index["NUMER.2"]
        row = (
            "| Precision a result requires | NUMER "
            "| NUMER.5, NUMER.12, NUMER.17 |"
        )
        self.assertIn(row, prov.body)
        prov.body = prov.body.replace(
            row, row + "\n| Precision a result requires | AGENT | NUMER.5 |", 1
        )
        self.assertEqual(status_of(index, matters_owned), "FAIL")

    def test_uncited_owner_fails(self) -> None:
        """Behavior: m.2 fails when a provision addressing another
        profile's matter cites no provision of it.

        Reference: STND.HARN.27; AGENT.1 is given for a NUMER matter in
        an AGENT table, and cites no NUMER provision.
        """
        index = live_index()
        agent = index["AGENT.1"]
        agent.meta["defines"] = ["shared-matters"]
        agent.body += (
            "\n\n| Matter | Owning profile | Provisions |\n"
            "| --- | --- | --- |\n"
            "| Precision a result requires | NUMER | AGENT.1 |\n"
        )
        self.assertEqual(status_of(index, matters_owned), "FAIL")

    def test_pairs_match_the_numer_review(self) -> None:
        """Behavior: the pairs for NUMER, other than those with
        STND.VVUQ or HW, are the pairs listed by hand at its adoption.

        Reference: the review record of NUMER 1.0 (61 pairs), made
        before STND.VVUQ and HW were adopted.
        """
        later = ("STND.VVUQ.", "HW.")
        pairs = [
            p
            for p in review_pairs(corpus_of(live_index()), "NUMER")
            if not any(s.startswith(later) for s in (p.first, p.second))
        ]
        self.assertEqual(len(pairs), NUMER_REVIEWED)

    def test_pairs_need_a_profile(self) -> None:
        """Behavior: no pair joins two provisions outside profiles.

        Reference: STND.HARN.28; every pair for a change of STND.DFLT
        has a profile provision on one side.
        """
        for pair in review_pairs(corpus_of(live_index()), "STND.DFLT"):
            with self.subTest(pair):
                self.assertTrue(
                    pair.first.startswith(("AGENT", "NUMER"))
                    or pair.second.startswith(("AGENT", "NUMER"))
                )


if __name__ == "__main__":
    unittest.main()
