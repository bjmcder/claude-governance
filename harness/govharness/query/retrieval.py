"""Fetch items, their cross references, and the governance on a topic.

Three queries answer a reader without loading the corpus into view:

- ``show``: one item or section in full, the higher governance it
  derives from, what else it cites, and what cites it, each named by
  identifier or locator and title; a document shows its lead text and
  names its sections and items;
- ``find``: the items and sections that hold the most words of a query,
  ranked, one line each;
- ``context``: the full text of the best matches and of the items they
  cite, within a budget of characters, the rest named only.

Every text is returned whole or named only (GOV.39).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from govharness.core.corpus import Corpus
from govharness.query.graph import (
    UNCITING,
    Graph,
    id_order,
    is_document,
    lineage,
    split_document,
)

IN_FORCE = {"adopted", "ratified"}
MATCHES = 8
TITLE_WEIGHT = 3
# Text hits of one word count up to BODY_CAP, so a long text does not
# outrank a short one by repetition.
BODY_CAP = 3
# Suffixes and their replacements, tried in order; the first that leaves
# at least STEM_KEEP letters is removed, so "deletion", "deleted", and
# "deletes" all give "delet", and "dependencies" gives "dependency".
SUFFIXES = (
    ("ions", ""),
    ("ion", ""),
    ("ings", ""),
    ("ing", ""),
    ("ies", "y"),
    ("ied", "y"),
    ("ed", ""),
    ("es", ""),
    ("s", ""),
    ("e", ""),
)
STEM_KEEP = 4
# An identifier keeps its dots and hyphens; other words split at hyphens.
WORD_RE = re.compile(r"[a-z0-9]+(?:\.[a-z0-9][a-z0-9-]*)+|[a-z0-9]+")


@dataclass(frozen=True)
class Match:
    """One item or section that a search finds.

    Parameters
    ----------
    node : str
        Identifier or locator.
    held : int
        How many words of the query it holds.
    titled : int
        How many of them its identifier, title, or section holds.
    score : int
        A title hit counts ``TITLE_WEIGHT``, text hits one each up to
        ``BODY_CAP``, summed over the words.
    """

    node: str
    held: int
    titled: int
    score: int


def status_of(corpus: Corpus, node: str) -> str:
    """Return the status of an item, or of a section's document.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    node : str
        Identifier or locator.

    Returns
    -------
    str
        The field ``status``.
    """
    return str(corpus.by_id[node.partition("#")[0]].meta.get("status", ""))


def title_of(corpus: Corpus, graph: Graph, node: str) -> str:
    """Return the title or term of an item, or a section's heading.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    node : str
        Identifier or locator.

    Returns
    -------
    str
        The title, or an empty string.
    """
    if node in graph.sections:
        return graph.sections[node].heading
    meta = corpus.by_id[node].meta
    return str(meta.get("title") or meta.get("term") or "")


def label(corpus: Corpus, graph: Graph, node: str) -> str:
    """Return one line naming a node: identifier, title, and status.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    node : str
        Identifier or locator.

    Returns
    -------
    str
        ``ID — Title`` and, for a node not in force, ``[status]``.
    """
    status = status_of(corpus, node)
    note = "" if status in IN_FORCE else f" [{status}]"
    return f"{node} — {title_of(corpus, graph, node)}{note}"


def text_of(corpus: Corpus, graph: Graph, node: str) -> str:
    """Return the text of a node: a document's lead, a section, an item.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    node : str
        Identifier or locator.

    Returns
    -------
    str
        Markdown, stripped.
    """
    if node in graph.sections:
        return graph.sections[node].text
    entry = corpus.by_id[node]
    if is_document(entry):
        return split_document(entry)[0]
    return entry.body.strip()


def block(corpus: Corpus, graph: Graph, node: str) -> str:
    """Return the heading, attributes, and text of a node.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    node : str
        Identifier or locator.

    Returns
    -------
    str
        Markdown: a heading, then status, level, mode, and rank.
    """
    meta = corpus.by_id[node.partition("#")[0]].meta
    facts = [str(meta[k]) for k in ("status", "level", "mode") if meta.get(k)]
    if meta.get("rank") is not None and "#" not in node:
        facts.append(f"rank {meta['rank']}")
    title = title_of(corpus, graph, node)
    head = f"## {node} — {title}\n\n{' · '.join(facts)}"
    text = text_of(corpus, graph, node)
    return f"{head}\n\n{text}" if text else head


def listing(
    corpus: Corpus, graph: Graph, name: str, nodes: list[str]
) -> list[str]:
    """Return a labeled list of nodes, or nothing for an empty one.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    name : str
        Label of the list.
    nodes : list[str]
        Identifiers or locators.

    Returns
    -------
    list[str]
        Markdown lines.
    """
    if not nodes:
        return []
    lines = (f"- {label(corpus, graph, n)}" for n in nodes)
    return ["", f"{name}:", *lines]


def held_by(corpus: Corpus, doc: str) -> list[str]:
    """Return the items a document holds.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc : str
        Identifier of the document.

    Returns
    -------
    list[str]
        Identifiers one level below it, and for LVL0 its parts, in id
        order.
    """
    depth = doc.count(".") + 1
    held = [
        i
        for i in corpus.by_id
        if i.startswith(f"{doc}.") and i.count(".") == depth
    ]
    held += [str(p) for p in corpus.by_id[doc].meta.get("parts") or []]
    return sorted(held, key=id_order)


def show(corpus: Corpus, graph: Graph, ref: str, expand: bool = False) -> str:
    """Return one item or section with its cross references.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its citation graph.
    ref : str
        Identifier or locator.
    expand : bool
        Whether to append the full text of what it derives from and
        cites.

    Returns
    -------
    str
        Markdown: the text, a document's sections and items, what it
        derives from, what else it cites, and what cites it.

    Raises
    ------
    KeyError
        If no item or section has the identifier or locator.
    """
    if ref not in graph.sections and ref not in corpus.by_id:
        raise KeyError(ref)
    upward = lineage(corpus, graph, ref) if "#" not in ref else []
    lines = [block(corpus, graph, ref)]
    listed = list(upward)
    if ref in corpus.by_id and is_document(corpus.by_id[ref]):
        sections = [s.locator for s in split_document(corpus.by_id[ref])[1]]
        held = held_by(corpus, ref)
        lines += listing(corpus, graph, "Sections", sections)
        lines += listing(corpus, graph, "Holds", held)
        listed += sections + held
    others = [n for n in graph.cites.get(ref, []) if n not in listed]
    lines += listing(corpus, graph, "Governed by", upward)
    lines += listing(corpus, graph, "Also cites", others)
    lines += listing(corpus, graph, "Cited by", graph.cited_by.get(ref, []))
    text = "\n".join(lines)
    if expand:
        text += "".join(
            f"\n\n{block(corpus, graph, n)}" for n in [*upward, *others]
        )
    return text + "\n"


def words_of(text: str) -> list[str]:
    """Return the lower-case words and identifiers of a text.

    Parameters
    ----------
    text : str
        Any text.

    Returns
    -------
    list[str]
        Words, with identifiers such as ``guard.6`` kept whole.
    """
    return WORD_RE.findall(text.lower())


def stem(word: str) -> str:
    """Return the stem of a word, or an identifier or number unchanged.

    Parameters
    ----------
    word : str
        Lower-case word.

    Returns
    -------
    str
        The word with its first fitting suffix of ``SUFFIXES`` replaced
        and a final doubled consonant made single, so that "committed"
        and "commit" share the stem "commit".
    """
    if not word.isalpha():
        return word
    for suffix, ending in SUFFIXES:
        kept = len(word) - len(suffix) + len(ending)
        if word.endswith(suffix) and kept >= STEM_KEEP:
            word = word[: -len(suffix)] + ending
            break
    if (
        len(word) > STEM_KEEP
        and word[-1] == word[-2]
        and word[-1] not in "aeiouy"
    ):
        word = word[:-1]
    return word


def stems(text: str) -> list[str]:
    """Return the stems of the words of a text.

    Parameters
    ----------
    text : str
        Any text.

    Returns
    -------
    list[str]
        One stem per word.
    """
    return [stem(w) for w in words_of(text)]


def searched(corpus: Corpus, graph: Graph) -> list[tuple[str, str, str]]:
    """Return every node a search reads, with its title line and text.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.

    Returns
    -------
    list[tuple[str, str, str]]
        Node, the words that count as its title, and its text. The
        title words are the parts of the identifier, the title or
        heading, and a provision's section; revision histories and
        References sections are not searched.
    """
    found = []
    for entry in corpus.entries:
        ident = str(entry.meta["id"])
        parts = re.sub(r"[.-]", " ", ident)
        title = f"{ident} {parts} {title_of(corpus, graph, ident)}"
        title += f" {entry.meta.get('section') or ''}"
        found.append((ident, title, text_of(corpus, graph, ident)))
        if not is_document(entry):
            continue
        for section in split_document(entry)[1]:
            if section.locator.partition("#")[2] not in UNCITING:
                head = f"{parts} {section.heading}"
                found.append((section.locator, head, section.text))
    return found


def find(
    corpus: Corpus,
    graph: Graph,
    query: str,
    limit: int = 10,
    in_force: bool = False,
) -> list[Match]:
    """Return the nodes that hold the most words of a query, best first.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its sections.
    query : str
        Words; an identifier counts as one word.
    limit : int
        Most matches returned.
    in_force : bool
        Whether to keep only adopted and ratified items and sections.

    Returns
    -------
    list[Match]
        The nodes that hold every word or, where none does, the most
        words any node holds; ranked by the words in the title, then
        score, then the shorter text, then identifier.
    """
    wanted = list(dict.fromkeys(stems(query)))
    ranked: list[tuple[Match, int]] = []
    for node, title, text in searched(corpus, graph):
        if in_force and status_of(corpus, node) not in IN_FORCE:
            continue
        heads, body = set(stems(title)), stems(text)
        counts = [(w in heads, body.count(w)) for w in wanted]
        held = sum(1 for t, b in counts if t or b)
        if held:
            titled = sum(1 for t, _ in counts if t)
            score = sum(TITLE_WEIGHT * t + min(b, BODY_CAP) for t, b in counts)
            ranked.append((Match(node, held, titled, score), len(body)))
    most = max((m.held for m, _ in ranked), default=0)
    ranked = [(m, size) for m, size in ranked if m.held == most]
    ranked.sort(
        key=lambda r: (-r[0].titled, -r[0].score, r[1], id_order(r[0].node))
    )
    return [m for m, _ in ranked[:limit]]


def context(
    corpus: Corpus,
    graph: Graph,
    query: str,
    budget: int = 8000,
    in_force: bool = False,
) -> str:
    """Return the governance on a topic within a budget of characters.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    graph : Graph
        Its citation graph.
    query : str
        Words naming the topic.
    budget : int
        Most characters of text returned in full.
    in_force : bool
        Whether to keep only adopted and ratified items and sections.

    Returns
    -------
    str
        Markdown: the best ``MATCHES`` matches, then the items and
        sections they cite, most cited first, each in full while the
        budget lasts and named otherwise. Citations of a document's text
        are not followed, nor are documents.
    """
    matches = [m.node for m in find(corpus, graph, query, MATCHES, in_force)]
    if not matches:
        return f"No item holds a word of: {query}\n"
    counts: dict[str, int] = {}
    for node in matches:
        if node in graph.sections or is_document(corpus.by_id[node]):
            continue
        for target in graph.cites.get(node, []):
            if target not in matches and not (
                target in corpus.by_id and is_document(corpus.by_id[target])
            ):
                counts[target] = counts.get(target, 0) + 1
    related = sorted(counts, key=lambda n: (-counts[n], id_order(n)))
    if in_force:
        related = [n for n in related if status_of(corpus, n) in IN_FORCE]
    shown: list[str] = []
    named: list[str] = []
    left = budget
    for node in [*matches, *related]:
        text = block(corpus, graph, node)
        if len(text) <= left:
            shown.append(text)
            left -= len(text)
        else:
            named.append(node)
    lines = ["\n\n".join(shown)] if shown else []
    lines += listing(corpus, graph, "Also relevant, not shown", named)
    return "\n".join(lines).lstrip("\n") + "\n"
