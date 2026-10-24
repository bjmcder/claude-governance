"""The citation graph of the corpus, with documents split into sections.

A node is an item or a section of a document, named by its locator
(``LVL0#normative-language``). An item cites what its reference fields
and its text name. A document cites through its fields and the text
before its first heading; each section cites through its own text.
``cited_by`` leaves out a revision history or References section, which
records or lists rather than cites, and a document's mention of its own
items, which is a table of contents.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from govharness.core.corpus import Corpus
from govharness.core.entry import DOC_FILE, Entry
from govharness.core.locators import HEADING_RE, cited_in_text, heading_slug

REFERENCE_FIELDS = (
    "instantiates",
    "governed_by",
    "parent",
    "refers_to",
    "cites",
)
# The fields that name the higher governance an item derives from.
# ``cites`` of LVL0 names related provisions, not higher ones.
UPWARD_FIELDS = ("instantiates", "governed_by", "parent")
UNCITING = frozenset({"revision-history", "references"})


@dataclass(frozen=True)
class Section:
    """One headed section of a document.

    Parameters
    ----------
    locator : str
        ``DOC#slug``.
    heading : str
        The heading text.
    text : str
        The text up to the next heading.
    """

    locator: str
    heading: str
    text: str


@dataclass
class Graph:
    """Sections and citations of a corpus.

    Parameters
    ----------
    sections : dict[str, Section]
        Every section by locator.
    cites : dict[str, list[str]]
        The nodes each node cites, fields first.
    cited_by : dict[str, list[str]]
        The nodes whose citation of each node counts.
    """

    sections: dict[str, Section] = field(default_factory=dict)
    cites: dict[str, list[str]] = field(default_factory=dict)
    cited_by: dict[str, list[str]] = field(default_factory=dict)


def id_order(node: str) -> list[int | str]:
    """Return a sort key that puts ``GOV.9`` before ``GOV.13``.

    Parameters
    ----------
    node : str
        Identifier or locator.

    Returns
    -------
    list[int | str]
        Text and numbers alternately.
    """
    parts = re.split(r"(\d+)", node)
    return [int(p) if i % 2 else p for i, p in enumerate(parts)]


def is_document(entry: Entry) -> bool:
    """Return whether an item is a document.

    Parameters
    ----------
    entry : Entry
        The item.

    Returns
    -------
    bool
        True for a ``_doc.md`` file.
    """
    return entry.path.name == DOC_FILE


def split_document(entry: Entry) -> tuple[str, list[Section]]:
    """Return a document's text before its first heading, and its sections.

    Parameters
    ----------
    entry : Entry
        The document.

    Returns
    -------
    tuple[str, list[Section]]
        The lead text and the sections in order.
    """
    pieces = HEADING_RE.split(entry.body)
    doc = str(entry.meta["id"])
    sections = [
        Section(f"{doc}#{heading_slug(head)}", head, text.strip())
        for head, text in zip(pieces[1::2], pieces[2::2], strict=True)
    ]
    return pieces[0].strip(), sections


def field_values(entry: Entry, names: tuple[str, ...]) -> list[str]:
    """Return the values of reference fields, lists and single values alike.

    Parameters
    ----------
    entry : Entry
        The item.
    names : tuple[str, ...]
        Field names.

    Returns
    -------
    list[str]
        The values in field order.
    """
    found: list[str] = []
    for name in names:
        value = entry.meta.get(name) or []
        values = [value] if isinstance(value, str) else value
        found += [str(v) for v in values]
    return found


def node_of(corpus: Corpus, graph: Graph, ref: str) -> str | None:
    """Return the node a reference names, or None.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections, at least.
    ref : str
        Identifier or locator.

    Returns
    -------
    str | None
        The locator of a known section, else the identifier of a known
        item (the document, for an unknown section), else None.
    """
    if ref in graph.sections:
        return ref
    base = ref.partition("#")[0]
    return base if base in corpus.by_id else None


def text_refs(corpus: Corpus, text: str) -> list[str]:
    """Return the identifiers and locators a text names, in id order.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    text : str
        Markdown.

    Returns
    -------
    list[str]
        References, resolved or not.
    """
    return sorted(cited_in_text(corpus.by_id, text), key=id_order)


def is_own(target: str, doc: str | None) -> bool:
    """Return whether a document's text names itself or what it holds.

    Parameters
    ----------
    target : str
        The cited node.
    doc : str | None
        The document whose text cites, or None for an item's text.

    Returns
    -------
    bool
        True for the document, its items, and its sections.
    """
    return doc is not None and (
        target == doc or target.startswith((f"{doc}.", f"{doc}#"))
    )


def build_graph(corpus: Corpus) -> Graph:
    """Return the sections and citation graph of a corpus.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    Graph
        Both directions of every citation, ``cited_by`` in id order.
    """
    graph = Graph()
    # (citing node, its fields' references, its text, whether it counts
    # in ``cited_by``, its document or None)
    sources: list[tuple[str, list[str], str, bool, str | None]] = []
    for entry in corpus.entries:
        ident = str(entry.meta["id"])
        fields = field_values(entry, REFERENCE_FIELDS)
        if not is_document(entry):
            sources.append((ident, fields, entry.body, True, None))
            continue
        lead, sections = split_document(entry)
        sources.append((ident, fields, lead, True, ident))
        for section in sections:
            graph.sections[section.locator] = section
            counts = section.locator.partition("#")[2] not in UNCITING
            sources.append((section.locator, [], section.text, counts, ident))
    for node, fields, text, counts, doc in sources:
        cited: list[str] = []
        for ref in fields + text_refs(corpus, text):
            target = node_of(corpus, graph, ref)
            if target and target != node and target not in cited:
                cited.append(target)
        graph.cites[node] = cited
        for target in cited:
            if counts and not is_own(target, doc):
                graph.cited_by.setdefault(target, []).append(node)
    for citing in graph.cited_by.values():
        citing.sort(key=id_order)
    return graph


def lineage(corpus: Corpus, graph: Graph, ident: str) -> list[str]:
    """Return the higher governance an item derives from, nearest first.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    ident : str
        Identifier of the item.

    Returns
    -------
    list[str]
        Every node reached through ``UPWARD_FIELDS``, breadth first;
        from a section, through its document's fields.
    """
    found: list[str] = []
    queue = [ident]
    while queue:
        entry = corpus.by_id.get(queue.pop(0).partition("#")[0])
        if entry is None:
            continue
        for ref in field_values(entry, UPWARD_FIELDS):
            target = node_of(corpus, graph, ref)
            if target and target != ident and target not in found:
                found.append(target)
                queue.append(target)
    return found
