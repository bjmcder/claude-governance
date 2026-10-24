"""Tests of the read-only queries ``show``, ``find``, and ``context``.

The reference is the live corpus, read once into memory: the fields and
text of its files, which a reader can confirm by hand, and the outcomes
of STND.HARN.1 to STND.HARN.3.
"""

from __future__ import annotations

import unittest

from govharness.core.corpus import Corpus
from govharness.query.graph import build_graph, lineage
from govharness.query.retrieval import (
    MATCHES,
    context,
    find,
    show,
    stem,
)
from tests.support import live_entries

CORPUS = Corpus(live_entries())
GRAPH = build_graph(CORPUS)


def found(query: str, in_force: bool = False) -> list[str]:
    """Return the nodes ``find`` returns for a query.

    Parameters
    ----------
    query : str
        Words.
    in_force : bool
        Whether to keep only adopted and ratified nodes.

    Returns
    -------
    list[str]
        Identifiers and locators, best first.
    """
    return [m.node for m in find(CORPUS, GRAPH, query, 10, in_force)]


def cited_by_dflt(item: str) -> list[str]:
    """Return STND.DFLT and its sections among the nodes citing an item.

    Parameters
    ----------
    item : str
        Identifier.

    Returns
    -------
    list[str]
        Nodes of STND.DFLT's own text that ``cited_by`` lists.
    """
    citing = GRAPH.cited_by.get(item, [])
    return [n for n in citing if n.partition("#")[0] == "STND.DFLT"]


class Show(unittest.TestCase):
    """``show`` returns an item or section with its cross references."""

    def test_lineage_and_citations(self) -> None:
        """Behavior: STND.INSTR.4 is governed by GOV.48 and GUARD.6,
        also cites STND.DFLT.24, and GUARD.6 is cited by STND.DFLT.24.

        Reference: the fields ``instantiates`` and ``refers_to`` of
        STND.INSTR.4 and STND.DFLT.24 (STND.HARN.1).
        """
        text = show(CORPUS, GRAPH, "STND.INSTR.4")
        upward = text.split("Governed by:")[1].split("Also cites:")[0]
        self.assertIn("GOV.48 — Agents bound", upward)
        self.assertIn("GUARD.6 — Bulk actions", upward)
        self.assertIn("STND.DFLT.24 — Scope enumeration", text)
        self.assertIn("STND.DFLT.24", GRAPH.cited_by["GUARD.6"])

    def test_lineage_by_level(self) -> None:
        """Behavior: lineage stops at LVL0, whose ``cites`` are related
        provisions; a term is governed by its provision, a sub-profile
        by its profile, and a provision citing a locator by that
        section.

        Reference: GUARD.6 cites PRIME.6; LEX.bulk-action, HW.ASIC, and
        STND.DRAFT.1 name GUARD.6, HW, and LVL0#normative-language in
        ``governed_by``, ``parent``, and ``instantiates``.
        """
        self.assertEqual(lineage(CORPUS, GRAPH, "GUARD.6"), [])
        self.assertIn("GUARD.6", lineage(CORPUS, GRAPH, "STND.DFLT.24"))
        self.assertEqual(
            lineage(CORPUS, GRAPH, "LEX.bulk-action"), ["GUARD.6"]
        )
        self.assertEqual(lineage(CORPUS, GRAPH, "HW.ASIC"), ["HW"])
        self.assertEqual(
            lineage(CORPUS, GRAPH, "STND.DRAFT.1"), ["LVL0#normative-language"]
        )

    def test_locator_shows_its_section(self) -> None:
        """Behavior: a locator shows its section only, and lists the
        items that cite that section; an unknown one raises KeyError.

        Reference: the sections of LVL0 and the field ``instantiates``
        of STND.DRAFT.1 (STND.IDENT.15, STND.HARN.1).
        """
        text = show(CORPUS, GRAPH, "LVL0#normative-language")
        self.assertIn("## LVL0#normative-language — Normative Language", text)
        self.assertNotIn("## Preamble", text)
        self.assertNotIn("This constitution states the principles", text)
        self.assertIn("STND.DRAFT.1 — Modal set", text.split("Cited by:")[1])
        for missing in ("LVL0#no-such-heading", "GUARD.999"):
            with self.assertRaises(KeyError):
                show(CORPUS, GRAPH, missing)

    def test_document_is_named_by_parts(self) -> None:
        """Behavior: a document shows its lead text, then names its
        sections by locator and its items, and returns no section text.

        Reference: the headings and provisions of STND.DFLT (GOV.39,
        STND.HARN.3).
        """
        text = show(CORPUS, GRAPH, "STND.DFLT")
        self.assertIn("- STND.DFLT#terms — Terms", text)
        self.assertIn("- STND.DFLT.7 — Criteria before work", text)
        self.assertNotIn("| Checkpoint |", text)

    def test_cited_by_skips_records_and_contents(self) -> None:
        """Behavior: a revision history and a document's mention of its
        own items are not listed as citing, though the section itself
        lists what it names; another section's citation is listed.

        Reference: the revision history of STND.DFLT names GOV.41 and
        STND.DFLT.15; its Mechanisms table names STND.DFLT.7 and
        PRIME.14 (STND.HARN.1).
        """
        for item in ("GOV.41", "STND.DFLT.7", "STND.DFLT.15"):
            self.assertEqual(cited_by_dflt(item), [], item)
        self.assertIn("GOV.41", GRAPH.cites["STND.DFLT#revision-history"])
        self.assertIn(
            "STND.DFLT#mechanisms-and-their-provisions",
            GRAPH.cited_by["PRIME.14"],
        )


class Find(unittest.TestCase):
    """``find`` ranks the items and sections that hold a query."""

    def test_stems_both_ways(self) -> None:
        """Behavior: forms of a word share a stem, and a word does not
        match a longer word that merely begins with it.

        Reference: "deleting" and "deletion"; "dependencies";
        "referring" and "refers"; "committed" against "commitment";
        "sign" against "signal" and "signature".
        """
        self.assertEqual(stem("deleting"), stem("deletion"))
        self.assertEqual(stem("dependencies"), stem("dependency"))
        self.assertEqual(stem("referring"), stem("refers"))
        self.assertEqual(stem("committed"), stem("commit"))
        self.assertNotEqual(stem("commitment"), stem("commit"))
        self.assertNotIn(stem("sign"), {stem("signal"), stem("signature")})

    def test_every_word(self) -> None:
        """Behavior: "delete files" finds STND.INSTR.3, which says
        "deleted" and "files", and not GUARD.12, which says "delegated".

        Reference: the text of STND.INSTR.3 and GUARD.12.
        """
        self.assertIn("STND.INSTR.3", found("delete files"))
        self.assertNotIn("GUARD.12", found("delete files"))

    def test_most_words_when_none_holds_all(self) -> None:
        """Behavior: where no item holds every word, the items holding
        the most are returned.

        Reference: no file says "zyzzyva"; LEX.remote-write defines
        remote write.
        """
        self.assertEqual(found("zyzzyva"), [])
        self.assertIn("LEX.remote-write", found("zyzzyva remote write"))

    def test_title_ranks_first(self) -> None:
        """Behavior: the item titled "Bulk actions" outranks items that
        only mention the words, and a heading finds its section.

        Reference: the title of GUARD.6 and the heading Normative
        Language of LVL0.
        """
        self.assertEqual(found("bulk actions", in_force=True)[0], "GUARD.6")
        self.assertEqual(
            found("normative language")[0], "LVL0#normative-language"
        )


class Context(unittest.TestCase):
    """``context`` returns whole texts within its budget."""

    def test_budget_and_whole_text(self) -> None:
        """Behavior: the text shown stays within the budget, every item
        shown is whole, and the rest is named.

        Reference: the budget argument (STND.HARN.2, STND.HARN.3); the
        matches for "remote write" that the budget leaves out.
        """
        text = context(CORPUS, GRAPH, "remote write", budget=1500)
        shown, named = text.split("Also relevant, not shown:")
        self.assertLessEqual(len(shown), 1500 + 2)
        self.assertIn(CORPUS.by_id["LEX.remote-write"].body.strip(), shown)
        matches = find(CORPUS, GRAPH, "remote write", MATCHES, False)
        hidden = [m.node for m in matches if f"## {m.node} — " not in shown]
        self.assertTrue(hidden)
        for node in hidden:
            with self.subTest(node):
                self.assertIn(f"\n- {node} — ", named)

    def test_nothing_found(self) -> None:
        """Behavior: a query no item matches says so.

        Reference: a word absent from the corpus.
        """
        self.assertIn("No item", context(CORPUS, GRAPH, "zyzzyva"))


if __name__ == "__main__":
    unittest.main()
