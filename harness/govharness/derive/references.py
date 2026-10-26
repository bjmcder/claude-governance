"""Derive the References table of each document below LVL0.

STND.DRAFT.34 requires each document below LVL0 to hold a section
``References`` whose table lists, by identifier and title, every other
document that it cites. A document is cited when an identifier or
locator of it, or of one of its provisions or terms, appears in the
document's text, in the text of its provisions, or in their reference
fields, and when the text names it by its identifier alone outside the
parts that ``naming_text`` leaves out (the term Cited document of
STND.DRAFT). An identifier that a document lists as withdrawn cites that
document. Check g.25 compares each table with this derivation.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from govharness.core.corpus import Corpus, Tree
from govharness.core.entry import DOC_FILE, Entry
from govharness.core.locators import cited_in_text
from govharness.core.tables import HISTORY_HEADING
from govharness.core.text import CODE_RE, FENCE_RE, unquoted

HEADER = ("Identifier", "Title")
SECTION = "References"
FIELDS = ("cites", "governed_by", "instantiates", "refers_to")
SECTION_RE = re.compile(
    rf"^## {SECTION}\s*\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
# A document identifier written as a word of its own. The match is the
# longest dotted run, so "HW.CPU" names HW.CPU, not HW.
NAME_RE = re.compile(
    r"(?<![A-Za-z0-9.])([A-Z]{2,5}\d?(?:\.[A-Z]{2,5})*)(?![A-Za-z0-9])"
)
HISTORY_RE = re.compile(
    rf"^{re.escape(HISTORY_HEADING)}\s*\n.*?(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)
# The documents STND.DRAFT.34 asks to hold References, and the word that
# names the level of the constitution rather than citing it.
NAMING_LEVELS = {"LVL1", "LVL2", "LVL3"}
NOT_NAMES = {"LVL0"}
EXAMPLE_COLUMN = "Example"


def document_of(corpus: Corpus, ident: str) -> str | None:
    """Return the identifier of the document an identifier belongs to.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    ident : str
        Identifier or locator.

    Returns
    -------
    str | None
        The document identifier, or ``None`` if the identifier does not
        resolve or its directory holds no document.
    """
    entry = corpus.by_id.get(ident.partition("#")[0])
    if entry is None:
        return None
    if entry.path.name == DOC_FILE:
        return str(entry.meta["id"])
    owner = corpus.document_of(entry)
    return str(owner.meta["id"]) if owner else None


def without_section(body: str) -> str:
    """Return a body without its References section.

    Parameters
    ----------
    body : str
        Markdown body.

    Returns
    -------
    str
        The body with the section removed.
    """
    return SECTION_RE.sub("", body)


def members_of(corpus: Corpus, doc_id: str) -> list[Entry]:
    """Return a document's entry and the entries of its directory.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the document.

    Returns
    -------
    list[Entry]
        The document first, then its provisions and terms; the entries
        of a sub-directory belong to their own document.
    """
    doc = corpus.by_id[doc_id]
    return [doc] + [
        e
        for e in corpus.entries
        if e.path.parent == doc.path.parent and e.path.name != DOC_FILE
    ]


def without_example_tables(text: str) -> str:
    """Drop every row of a table whose header names a column Example.

    Such a table lists identifiers as examples of a form. Its other
    cells mention them too, so the whole table goes.

    Parameters
    ----------
    text : str
        Markdown text.

    Returns
    -------
    str
        The text without those tables.
    """
    kept: list[str] = []
    skipping = in_table = False
    for line in text.split("\n"):
        if line.lstrip().startswith("|"):
            if not in_table:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                skipping = EXAMPLE_COLUMN in cells
            in_table = True
            if skipping:
                continue
        else:
            in_table = skipping = False
        kept.append(line)
    return "\n".join(kept)


def naming_text(body: str) -> str:
    """Return the part of a body in which a bare name cites a document.

    Parameters
    ----------
    body : str
        Markdown body of an entry.

    Returns
    -------
    str
        The body without its References section, its Revision History,
        tables of examples, fenced and inline code, and quoted spans.
    """
    text = HISTORY_RE.sub("", without_section(body))
    text = without_example_tables(text)
    text = CODE_RE.sub(" ", FENCE_RE.sub("\n", text))
    return unquoted(text)


def named_documents(corpus: Corpus, doc_id: str) -> list[str]:
    """Return the other documents a document names by bare identifier.

    Only a document at LVL1 to LVL3 is read, since STND.DRAFT.34 asks
    only those to hold References. Its own text and that of its
    provisions and terms are read, outside the parts that
    ``naming_text`` leaves out.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the naming document.

    Returns
    -------
    list[str]
        Sorted identifiers of the documents named; empty for a document
        at another level.
    """
    if str(corpus.by_id[doc_id].meta.get("level")) not in NAMING_LEVELS:
        return []
    documents = {
        str(e.meta["id"]) for e in corpus.entries if e.path.name == DOC_FILE
    }
    named: set[str] = set()
    for entry in members_of(corpus, doc_id):
        named |= set(NAME_RE.findall(naming_text(entry.body)))
    return sorted((named & documents) - NOT_NAMES - {doc_id})


def cited_documents(corpus: Corpus, doc_id: str) -> list[str]:
    """Return the sorted documents, other than itself, a document cites.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the citing document.

    Returns
    -------
    list[str]
        Identifiers of the cited documents.
    """
    named: set[str] = set(named_documents(corpus, doc_id))
    for entry in members_of(corpus, doc_id):
        text = without_section(entry.body)
        named |= cited_in_text(corpus.by_id, unquoted(text))
        for name in FIELDS:
            named |= {str(v) for v in entry.meta.get(name) or []}
    retired = withdrawn_by(corpus)
    found = {
        document_of(corpus, ident) or retired.get(ident) for ident in named
    }
    return sorted(d for d in found if d and d != doc_id)


def withdrawn_by(corpus: Corpus) -> dict[str, str]:
    """Return the document that lists each withdrawn identifier.

    A revision row that cites a withdrawn provision still cites its
    document, so the derived table keeps the row once the provision is
    gone (STND.IDENT.14).

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    dict[str, str]
        Each identifier of a field ``withdrawn``, with the document
        that lists it.
    """
    return {
        str(ident): str(entry.meta["id"])
        for entry in corpus.entries
        if entry.path.name == DOC_FILE
        for ident in entry.meta.get("withdrawn") or []
    }


def expected_rows(corpus: Corpus, doc_id: str) -> list[tuple[str, str]]:
    """Return the (identifier, title) rows a document's table should hold.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the document.

    Returns
    -------
    list[tuple[str, str]]
        One row per cited document, sorted by identifier.
    """
    return [
        (d, str(corpus.by_id[d].meta.get("title", "")))
        for d in cited_documents(corpus, doc_id)
    ]


def references_table(corpus: Corpus, doc_id: str) -> str:
    """Return the Markdown table of the documents a document cites.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the document.

    Returns
    -------
    str
        Header, separator, and one row per cited document.
    """
    rows = [
        f"| {d} | {corpus.by_id[d].meta.get('title', '')} |"
        for d in cited_documents(corpus, doc_id)
    ]
    return "\n".join(["| Identifier | Title |", "| --- | --- |", *rows])


def with_section(text: str, block: str) -> str:
    """Return file text with its References section set to a block.

    The section replaces an existing one; otherwise it goes before
    ``## Revision History``, or at the end of a document that has none.

    Parameters
    ----------
    text : str
        Text of the document file.
    block : str
        The section, heading included.

    Returns
    -------
    str
        The new file text.
    """
    if SECTION_RE.search(text):
        return SECTION_RE.sub(lambda _: block, text, count=1)
    if "\n" + HISTORY_HEADING in text:
        return text.replace(
            "\n" + HISTORY_HEADING, "\n" + block + HISTORY_HEADING, 1
        )
    return text.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"


def rewrite_sections(
    tree: Tree, corpus: Corpus, doc_ids: list[str]
) -> dict[PurePosixPath, str]:
    """Return the document files with their References sections derived.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.
    corpus : Corpus
        The corpus loaded from that snapshot.
    doc_ids : list[str]
        Documents whose section is written, in order.

    Returns
    -------
    dict[PurePosixPath, str]
        New text of each document file, by path relative to the root.

    Raises
    ------
    KeyError
        If an identifier names no entry.
    """
    written: dict[PurePosixPath, str] = {}
    for doc_id in doc_ids:
        rel = PurePosixPath(corpus.by_id[doc_id].path)
        block = f"## {SECTION}\n\n{references_table(corpus, doc_id)}\n\n"
        written[rel] = with_section(written.get(rel, tree.text(rel)), block)
    return written
