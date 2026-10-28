"""Tests of the read-only queries ``show``, ``find``, and ``context``.

The reference is the live corpus, read once into memory: the fields and
text of its files, which a reader can confirm by hand, and the outcomes
of STND.HARN.1 to STND.HARN.3.
"""

from __future__ import annotations

import unittest
from pathlib import PurePosixPath

from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.query.graph import Graph, build_graph, lineage
from govharness.query.retrieval import (
    ITEM,
    MATCHES,
    PROSE,
    TERMS,
    block,
    context,
    find,
    items_below,
    kind_of,
    names_below,
    resolve_ref,
    show,
    stem,
    stems,
)
from tests.support import live_entries

CORPUS = Corpus(live_entries())
GRAPH = build_graph(CORPUS)


def case_twins() -> tuple[Corpus, Graph]:
    """Return a corpus of one document and two items alike but for case.

    Returns
    -------
    tuple[Corpus, Graph]
        GOV, with a Terms and a Notes section, holding GOV.1 and gov.1.
    """
    meta = {"kind": "provision", "status": "adopted"}
    entries = [
        Entry(
            PurePosixPath("GOV/_doc.md"),
            {"id": "GOV", "title": "Governance", "status": "adopted"},
            "Lead text.\n\n## Terms\n\nA term.\n\n## Notes\n\nOn GOV.1.\n",
        ),
        Entry(PurePosixPath("GOV/1.md"), {**meta, "id": "GOV.1"}, "Upper."),
        Entry(PurePosixPath("GOV/1l.md"), {**meta, "id": "gov.1"}, "Lower."),
    ]
    corpus = Corpus(entries)
    return corpus, build_graph(corpus)


def shown_nodes(shown: str) -> list[str]:
    """Return the nodes whose blocks a ``context`` output shows, in order.

    Parameters
    ----------
    shown : str
        The output before "Also relevant, not shown".

    Returns
    -------
    list[str]
        The identifier or locator of each ``## `` heading.
    """
    return [
        line[3:].split(" — ")[0]
        for line in shown.splitlines()
        if line.startswith("## ")
    ]


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

    def test_cited_by_folds_sections_by_heading(self) -> None:
        """Behavior: "Cited by" lists each citing provision on its own
        line and folds the citing sections into one line per heading,
        naming the documents, so that no section or document has a
        line of its own; a citing lead text is one line too.

        Reference: STND.CLASS.10, cited by STND.KNOW.4, STND.PROJ.1,
        STND.CLASS.21, and the Notes of forty-one documents, HDES also
        in "Where the rest lives"; PRIME.3, cited by the lead text of
        VV (STND.HARN.1; unit 0022, HR-11, and its review, Medium 2 and
        mutant 10).
        """
        text = show(CORPUS, GRAPH, "STND.CLASS.10")
        cited = text.split("Cited by:")[1]
        lines = [line for line in cited.splitlines() if line.startswith("- ")]
        self.assertIn("- STND.KNOW.4 — Evidence level assignment", lines)
        self.assertIn("- STND.PROJ.1 — Constitution sections", lines)
        notes = [line for line in lines if line.startswith("- Notes of: ")]
        self.assertEqual(len(notes), 1)
        self.assertIn(", HDES, ", notes[0])
        self.assertIn(", STND.CODE, ", notes[0])
        self.assertIn("- Where the rest lives of: HDES", lines)
        self.assertFalse([line for line in lines if "#" in line])
        citing = GRAPH.cited_by["STND.CLASS.10"]
        headings = {GRAPH.sections[n].heading for n in citing if "#" in n}
        provisions = [n for n in citing if "#" not in n]
        kinds = {CORPUS.by_id[n].meta["kind"] for n in provisions}
        self.assertEqual(kinds, {"provision"})
        self.assertEqual(len(lines), len(provisions) + len(headings))
        self.assertLess(len(text.splitlines()), 70)
        self.assertIn("VV", GRAPH.cited_by["PRIME.3"])
        cited = show(CORPUS, GRAPH, "PRIME.3").split("Cited by:")[1]
        self.assertIn("\n- Lead text of: VV\n", cited)
        self.assertNotIn("\n- VV — ", cited)

    def test_ambiguous_case_is_not_resolved(self) -> None:
        """Behavior: a reference that differs only by case from two
        nodes names neither, so ``show`` raises KeyError, while each
        exact identifier and a section in another case still resolve.

        Reference: a corpus holding GOV.1 and gov.1 (unit 0022, HR-10;
        its review, mutant 6).
        """
        corpus, graph = case_twins()
        self.assertEqual(resolve_ref(corpus, graph, "GOV.1"), "GOV.1")
        self.assertEqual(resolve_ref(corpus, graph, "gov.1"), "gov.1")
        self.assertIsNone(resolve_ref(corpus, graph, "Gov.1"))
        self.assertEqual(resolve_ref(corpus, graph, "gov#TERMS"), "GOV#terms")
        with self.assertRaises(KeyError):
            show(corpus, graph, "Gov.1")

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

    def test_whole_document_opens_parts_only(self) -> None:
        """Behavior: ``whole`` opens a part the document names, so LVL0
        prints the provisions of PRIME and GOV; a document held by
        identifier alone is named, not opened, so STND prints nothing
        beyond its lists.

        Reference: the ``parts`` of LVL0; STND, which holds the
        standards and no provision of its own (unit 0022, HR-2; its
        review, Low 1 and mutant 7).
        """
        below = items_below(CORPUS, "LVL0")
        self.assertLess(set(CORPUS.parts), set(below))
        self.assertIn("PRIME.1", below)
        self.assertIn("GOV.38", below)
        text = show(CORPUS, GRAPH, "LVL0", whole=True)
        self.assertIn("\n## PRIME.1 — ", text)
        self.assertIn(CORPUS.by_id["GOV.38"].body.strip(), text)
        self.assertEqual(items_below(CORPUS, "STND"), [])
        self.assertEqual(
            show(CORPUS, GRAPH, "STND", whole=True),
            show(CORPUS, GRAPH, "STND"),
        )
        self.assertIn("- STND.PY — ", show(CORPUS, GRAPH, "STND"))

    def test_cited_by_skips_records_and_contents(self) -> None:
        """Behavior: a revision history and a document's mention of its
        own items are not listed as citing, though the section itself
        lists what it names; another section's citation is listed.

        Reference: the revision history of STND.DFLT names GOV.41, which
        its Notes also cite, and STND.DFLT.15; its Mechanisms table
        names STND.DFLT.7 and PRIME.14 (STND.HARN.1).
        """
        history = "STND.DFLT#revision-history"
        self.assertIn("GOV.41", GRAPH.cites[history])
        for item in GRAPH.cites[history]:
            with self.subTest(item):
                self.assertNotIn(history, GRAPH.cited_by.get(item, []))
        for item in ("STND.DFLT.7", "STND.DFLT.15"):
            self.assertEqual(cited_by_dflt(item), [], item)
        self.assertEqual(cited_by_dflt("GOV.41"), ["STND.DFLT#notes"])
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
        self.assertGreater(len(provisions), len(found("STND.PY")))
        self.assertLessEqual(set(provisions), set(nodes[: sum(own)]))
        self.assertIn("STND.PY#notes", nodes[: sum(own)])
        self.assertTrue(names_below("stnd.py", "stnd.py#notes"))
        self.assertTrue(names_below("stnd.py", "stnd.py.5"))
        self.assertFalse(names_below("stnd.py", "stnd.pyx.1"))
        self.assertFalse(names_below("stnd", "stnd.py.1"))
        self.assertEqual(stems("STND.DFLT#terms"), ["stnd.dflt#terms"])
        self.assertEqual(found("STND.DFLT#terms")[0], "STND.DFLT#terms")

    def test_terms_sections_rank_between_items_and_prose(self) -> None:
        """Behavior: a Terms section ranks after every provision, term,
        entry, and tag and before every Notes section and lead text,
        whatever its score.

        Reference: "evidence level", where STND.KNOW#terms is the first
        section and would be the sixteenth without its kind; "bulk
        action" and STND.DFLT#terms (unit 0022, HR-1; its review,
        mutant 3).
        """
        self.assertEqual(kind_of(CORPUS, GRAPH, "STND.DFLT#terms"), TERMS)
        self.assertEqual(kind_of(CORPUS, GRAPH, "STND.DFLT#notes"), PROSE)
        for query, section in (
            ("evidence level", "STND.KNOW#terms"),
            ("bulk action", "STND.DFLT#terms"),
        ):
            with self.subTest(query):
                nodes = found(query, limit=100)
                kinds = [kind_of(CORPUS, GRAPH, n) for n in nodes]
                self.assertEqual(kinds, sorted(kinds))
                self.assertIn(PROSE, kinds)
                self.assertEqual(nodes[kinds.index(TERMS)], section)

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

    def test_every_text_shown_is_whole(self) -> None:
        """Behavior: what ``context`` prints before the names is exactly
        the blocks of the nodes it shows, each whole; a section larger
        than the budget is named, never cut, and does not take the
        budget from the provisions behind it.

        Reference: STND.HARN.3; "remote write authorization" in force,
        where each item named is longer than the budget left after the
        texts shown; STND.CODE#notes, above 20 000 characters, named at
        a budget of 3000 and shown whole at 100 000 (unit 0022, HR-1;
        its review, High 2).
        """
        cases = (
            ("remote write authorization", 8000, True),
            ("remote write authorization", 3000, True),
            ("remote write", 1500, False),
            ("STND.CODE#notes", 3000, False),
            ("STND.CODE#notes", 100_000, False),
        )
        for query, budget, in_force in cases:
            with self.subTest(query=query, budget=budget):
                text = context(CORPUS, GRAPH, query, budget, in_force)
                shown, _, rest = text.partition("Also relevant, not shown:")
                nodes = shown_nodes(shown)
                blocks = [block(CORPUS, GRAPH, n) for n in nodes]
                self.assertEqual(shown.rstrip("\n"), "\n\n".join(blocks))
                self.assertLessEqual(sum(map(len, blocks)), budget)
                self.assertNotIn("[cut:", text)
                left = budget - sum(map(len, blocks))
                for line in rest.splitlines():
                    if line.startswith("- "):
                        node = line[2:].split(" — ")[0]
                        size = len(block(CORPUS, GRAPH, node))
                        self.assertGreater(size, left, node)
        text = context(CORPUS, GRAPH, "STND.CODE#notes", budget=3000)
        self.assertNotIn("## STND.CODE#notes", text)
        self.assertIn("\n- STND.CODE#notes — Notes", text)
        whole = context(CORPUS, GRAPH, "STND.CODE#notes", budget=100_000)
        self.assertIn(GRAPH.sections["STND.CODE#notes"].text, whole)


if __name__ == "__main__":
    unittest.main()
