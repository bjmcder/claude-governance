"""Tests of checks m.1 and m.2 and of the review pairs (STND.HARN.26 to 28).

Each test damages an in-memory copy of the live corpus and asserts the
named check reaches FAIL, so that a pass on the clean corpus is
evidence. The pair listing is compared with the pairs that the
shared-matters tables give, and with the rule of common instantiation
within a change (STND.HARN.28 as ruling E1 narrows it, unit 0024).
"""

from __future__ import annotations

import unittest

from govharness.checks.base import CheckContext
from govharness.checks.combination import matters_owned, selectors_defined
from govharness.query.combination import (
    is_profile,
    matter_key,
    matter_rows,
    review_pairs,
)
from tests.support import corpus_of, live_index

PROFILE_KINDS = ("profile", "sub-profile")


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

    def test_pairs_of_one_document_rest_on_a_matter(self) -> None:
        """Behavior: the pairs for a change of NUMER alone are the
        pairs that the shared-matters tables give for one matter, each
        with a provision of NUMER, and no pair rests on a common LVL0
        provision alone.

        Reference: STND.HARN.28, narrowed under ruling E1 (unit 0024);
        the pairs are derived here from the tables, not from the code
        under test.
        """
        index = live_index()
        corpus = corpus_of(index)
        members: dict[str, set[str]] = {}
        for row in matter_rows(corpus):
            members.setdefault(matter_key(row.matter), set()).update(
                row.provisions
            )

        def doc(ident: str) -> str:
            """Return the document of a provision.

            Parameters
            ----------
            ident : str
                Identifier of a provision.

            Returns
            -------
            str
                The identifier without its number.
            """
            return ident.rsplit(".", 1)[0]

        expected = {
            (a, b)
            for group in members.values()
            for a in group
            for b in group
            if doc(a) == "NUMER"
            and doc(b) != "NUMER"
            and (
                is_profile(corpus, doc(a)) or is_profile(corpus, doc(b))
            )
        }
        pairs = review_pairs(corpus, "NUMER")
        self.assertEqual({(p.first, p.second) for p in pairs}, expected)
        for pair in pairs:
            with self.subTest(pair):
                self.assertTrue(
                    any(b.startswith("matter: ") for b in pair.bases)
                )

    def test_common_instantiation_only_within_the_change(self) -> None:
        """Behavior: a change of NUMER and HW together adds the pairs of
        a NUMER and a HW provision that instantiate one LVL0 provision,
        and no pair on that basis alone reaches a third document.

        Reference: STND.HARN.28 (unit 0024): a pair of common
        instantiation is listed where both provisions are in documents
        that the change adopts or amends.
        """
        corpus = corpus_of(live_index())
        alone = review_pairs(corpus, "NUMER")
        both = review_pairs(corpus, ("NUMER", "HW"))
        self.assertGreater(len(both), len(alone))
        inside = ("NUMER.", "HW.")
        for pair in both:
            if all(b.startswith("matter: ") for b in pair.bases):
                continue
            with self.subTest(pair):
                self.assertTrue(pair.first.startswith(inside))
                self.assertTrue(pair.second.startswith(inside))
                self.assertNotEqual(
                    pair.first.split(".")[0], pair.second.split(".")[0]
                )
        same = review_pairs(corpus, ("HW", "NUMER"))
        self.assertEqual(both, same)

    def test_named_provision_alone_on_the_changed_side(self) -> None:
        """Behavior: a change that names one provision of NUMER lists
        only pairs that hold it, a subset of those of the whole
        document; a pair of common instantiation joins it to a provision
        of a document of which the change amends a provision.

        Reference: STND.HARN.28 (unit 0024): the changed side holds the
        provisions that the change adopts or amends.
        """
        corpus = corpus_of(live_index())
        whole = set(review_pairs(corpus, "NUMER"))
        one = review_pairs(corpus, ("NUMER.11",))
        self.assertTrue(one)
        self.assertLessEqual(set(one), whole)
        for pair in one:
            with self.subTest(pair):
                self.assertIn("NUMER.11", (pair.first, pair.second))
        joined = review_pairs(corpus, ("NUMER.11", "HW.16"))
        common = [
            p
            for p in joined
            if not all(b.startswith("matter: ") for b in p.bases)
        ]
        self.assertTrue(common)
        for pair in common:
            with self.subTest(pair):
                self.assertTrue(
                    {"NUMER.11", "HW.16"} & {pair.first, pair.second}
                )
                self.assertTrue(
                    {pair.first.split(".")[0], pair.second.split(".")[0]}
                    <= {"NUMER", "HW"}
                )

    def test_amended_lvl0_provision_pairs_by_matter(self) -> None:
        """Behavior: for a change of LVL0 alone that amends VV.1, each
        pair holds a provision that instantiates VV.1 and rests on a
        shared matter, since such a change touches no document below
        LVL0.

        Reference: STND.HARN.28 (unit 0024): a pair of common
        instantiation needs its other provision in a document that the
        change adopts or amends a provision of.
        """
        index = live_index()
        corpus = corpus_of(index)
        pairs = review_pairs(corpus, "LVL0", ("VV.1",))
        self.assertTrue(pairs)
        for pair in pairs:
            with self.subTest(pair):
                self.assertTrue(
                    any(b.startswith("matter: ") for b in pair.bases)
                )
                self.assertIn(
                    "VV.1", index[pair.first].meta.get("instantiates") or []
                )

    def test_lvl0_amendment_adds_no_pair_outside_the_change(self) -> None:
        """Behavior: with NUMER changed and VV.1 amended, a pair on a
        common LVL0 provision has both provisions in NUMER's change,
        none of them a provision outside NUMER that is on the changed
        side only because it instantiates VV.1; no pair rests on a
        provision of GOV or of the Governing Principles.

        Reference: STND.HARN.28 as ruling E1 narrows it (unit 0024,
        review Should-fix 1): both provisions in documents that the
        change touches.
        """
        corpus = corpus_of(live_index())
        pairs = review_pairs(corpus, ("NUMER", "HW"), ("VV.1",))
        for pair in pairs:
            with self.subTest(pair):
                self.assertFalse(
                    any(b.startswith(("GOV.", "PRIN.")) for b in pair.bases)
                )
                if all(b.startswith("matter: ") for b in pair.bases):
                    continue
                for ident in (pair.first, pair.second):
                    self.assertTrue(ident.startswith(("NUMER.", "HW.")))
                    self.assertNotIn(
                        ident.split(".")[1],
                        ("CPU", "GPU", "QPU", "EMBED", "FPGA", "ASIC"),
                    )
        alone = review_pairs(corpus, ("NUMER",), ("VV.1",))
        self.assertEqual(len(alone), 344)
        for pair in alone:
            with self.subTest(pair):
                if not all(b.startswith("matter: ") for b in pair.bases):
                    self.assertTrue(pair.first.startswith("NUMER."))
                    self.assertTrue(pair.second.startswith("NUMER."))

    def test_document_in_draft_keeps_its_pairs(self) -> None:
        """Behavior: a changed document that is not yet in force keeps
        its pairs: its shared-matters tables and its provisions count,
        92 pairs for NUMER alone and 39 for NUMER.11 with HW.16.

        Reference: STND.HARN.28: the tables of each document that the
        change adopts or amends (unit 0024, review Optional 1).
        """
        index = live_index()
        index["NUMER"].meta["status"] = "draft"
        corpus = corpus_of(index)
        self.assertEqual(len(review_pairs(corpus, "NUMER")), 92)
        self.assertEqual(len(review_pairs(corpus, ("NUMER.11", "HW.16"))), 39)

    def test_pairs_need_a_profile(self) -> None:
        """Behavior: no pair joins two provisions outside profiles.

        Reference: STND.HARN.28; every pair for a change of STND.DFLT
        has a provision of a document whose kind is profile or
        sub-profile on one side.
        """
        index = live_index()
        profiles = tuple(
            f"{ident}."
            for ident, entry in index.items()
            if entry.meta.get("kind") in PROFILE_KINDS
        )
        for pair in review_pairs(corpus_of(index), "STND.DFLT"):
            with self.subTest(pair):
                self.assertTrue(
                    pair.first.startswith(profiles)
                    or pair.second.startswith(profiles)
                )


if __name__ == "__main__":
    unittest.main()
