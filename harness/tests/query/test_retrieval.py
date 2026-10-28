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
    ITEM,
    MATCHES,
    PROSE,
    context,
    find,
    kind_of,
    show,
    stem,
    stems,
)
from tests.support import live_entries

CORPUS = Corpus(live_entries())
GRAPH = build_graph(CORPUS)


def found(query: str, in_force: bool = False, limit: int = 10) -> list[str]:
    """Return the nodes ``find`` returns for a query.

    Parameters
    ----------
    query : str
        Words.
    in_force : bool
        Whether to keep only adopted and ratified nodes.
    limit : int
        The most nodes to return.

    Returns
    -------
    list[str]
        Identifiers and locators, best first.
    """
    return [m.node for m in find(CORPUS, GRAPH, query, limit, in_force)]


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

    def test_cited_by_folds_sections_by_document(self) -> None:
        """Behavior: "Cited by" lists each citing provision on its own
        line and folds the citing sections into one line per document,
        naming the sections, so that no section has a line of its own.

        Reference: STND.CLASS.10, cited by STND.KNOW.4, STND.PROJ.1,
        and the Notes of more than thirty documents; HDES cites it in
        two sections (STND.HARN.1; unit 0022, HR-11).
        """
        text = show(CORPUS, GRAPH, "STND.CLASS.10")
        cited = text.split("Cited by:")[1]
        lines = [line for line in cited.splitlines() if line.startswith("- ")]
        self.assertIn("- STND.KNOW.4 — Evidence level assignment", lines)
        self.assertIn("- STND.PROJ.1 — Constitution sections", lines)
        self.assertIn("- STND.CODE — Coding standard: Notes", lines)
        self.assertIn(
            "- HDES — Hardware design: Notes, Where the rest lives", lines
        )
        self.assertFalse([line for line in lines if "#" in line])
        citing = GRAPH.cited_by["STND.CLASS.10"]
        docs = {n.partition("#")[0] for n in citing if "#" in n}
        self.assertEqual(len(lines), len(citing) - len(citing) + 2 + len(docs))

    def test_case_insensitive_identifier(self) -> None:
        """Behavior: an identifier or locator in the wrong case shows
        the item, under its identifier as the corpus writes it.

        Reference: STND.CLASS.10 and LVL0#normative-language (unit
        0022, HR-10).
        """
        text = show(CORPUS, GRAPH, "stnd.class.10")
        self.assertTrue(text.startswith("## STND.CLASS.10 — "))
        self.assertEqual(
            show(CORPUS, GRAPH, "lvl0#Normative-Language"),
            show(CORPUS, GRAPH, "LVL0#normative-language"),
        )

    def test_whole_document(self) -> None:
        """Behavior: ``whole`` appends every provision of a document, in
        id order, each under its own heading with its full text; a
        provision alone gains nothing.

        Reference: the provisions of STND.PY in the live corpus, and
        STND.PY.1 (unit 0022, HR-2).
        """
        text = show(CORPUS, GRAPH, "STND.PY", whole=True)
        wanted = sorted(
            (k for k in CORPUS.by_id if k.startswith("STND.PY.")),
            key=lambda k: int(k.rpartition(".")[2]),
        )
        heads = [
            line.split(" — ")[0][3:]
            for line in text.splitlines()
            if line.startswith("## STND.PY.")
        ]
        self.assertEqual(heads, wanted)
        for ident in wanted:
            with self.subTest(ident):
                self.assertIn(CORPUS.by_id[ident].body.strip(), text)
        self.assertEqual(
            show(CORPUS, GRAPH, "STND.PY.1", whole=True),
            show(CORPUS, GRAPH, "STND.PY.1"),
        )

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

        Reference: the text of STND.INSTR.3 and GUARD.12. Every match is
        read, since more provisions now say both words and the rank of
        STND.INSTR.3 among them is not what this test fixes.
        """
        every = found("delete files", limit=10_000)
        self.assertIn("STND.INSTR.3", every)
        self.assertNotIn("GUARD.12", every)

    def test_most_words_when_none_holds_all(self) -> None:
        """Behavior: where no item holds every word, the items holding
        the most are returned.

        Reference: no file says "zyzzyva"; LEX.remote-write defines
        remote write.
        """
        self.assertEqual(found("zyzzyva"), [])
        self.assertIn("LEX.remote-write", found("zyzzyva remote write"))

    def test_provisions_rank_above_notes(self) -> None:
        """Behavior: provisions come before Notes and other prose, which
        hold more words of a long question only by their length.

        Reference: "python code CSQ3 project", which before unit 0022
        returned five Notes sections and no provision; "remote write
        authorization", in force, where six of ten were Notes (HR-1).
        """
        for query in (
            "python code CSQ3 project",
            "remote write authorization",
        ):
            with self.subTest(query):
                nodes = found(query, in_force=True)
                self.assertEqual(kind_of(CORPUS, GRAPH, nodes[0]), ITEM)
                kinds = [kind_of(CORPUS, GRAPH, n) for n in nodes]
                prose = [k == PROSE for k in kinds]
                self.assertEqual(prose, sorted(prose))
                self.assertLess(sum(prose), 6)

    def test_document_identifier_matches_its_provisions(self) -> None:
        """Behavior: a document identifier in the query matches the
        provisions and sections below it, after the document itself.

        Reference: STND.PY and its provisions (unit 0022, HR-2); before
        the unit, ``find STND.PY`` returned Notes of other standards.
        """
        nodes = found("STND.PY", limit=100)
        self.assertEqual(nodes[0], "STND.PY")
        own = [n.startswith("STND.PY") for n in nodes]
        self.assertEqual(own, sorted(own, reverse=True))
        provisions = [k for k in CORPUS.by_id if k.startswith("STND.PY.")]
        self.assertGreater(len(provisions), 30)
        self.assertLessEqual(set(provisions), set(nodes[: sum(own)]))
        self.assertEqual(stems("STND.DFLT#terms"), ["stnd.dflt#terms"])
        self.assertEqual(found("STND.DFLT#terms")[0], "STND.DFLT#terms")

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
        """Behavior: a query no item matches returns nothing, so that
        the command reports it on the standard error and exits 1.

        Reference: a word absent from the corpus (unit 0022, HR-10).
        """
        self.assertEqual(context(CORPUS, GRAPH, "zyzzyva"), "")

    def test_long_section_is_cut_not_dropped(self) -> None:
        """Behavior: a prose section larger than the whole budget is
        shown as far as the budget allows, with a marker naming the cut
        and the command that prints it whole, rather than named only;
        a provision is still shown whole or named.

        Reference: the locator STND.CODE#notes as the query, whose
        best match is that Notes section, above 20 000 characters,
        with a budget of 3000 (unit 0022, HR-1).
        """
        text = context(CORPUS, GRAPH, "STND.CODE#notes", budget=3000)
        shown = text.split("Also relevant, not shown:")[0]
        self.assertTrue(shown.startswith("## STND.CODE#notes — Notes"))
        self.assertLessEqual(len(shown), 3000 + 2)
        self.assertRegex(
            shown,
            r"\[cut: \d+ of \d+ characters; show STND\.CODE#notes "
            r"prints it whole\]",
        )
        whole = context(CORPUS, GRAPH, "STND.CODE#notes", budget=100_000)
        self.assertNotIn("[cut:", whole)
        self.assertIn(GRAPH.sections["STND.CODE#notes"].text, whole)


if __name__ == "__main__":
    unittest.main()
