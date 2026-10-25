"""Derive the References table of each document below LVL0.

STND.DRAFT.34 requires each document below LVL0 to hold a section
``References`` whose table lists, by identifier and title, every other
document that it cites. A document is cited when an identifier or
locator of it, or of one of its provisions or terms, appears in the
document's text, in the text of its provisions, or in their reference
fields. Check g.25 compares each table with this derivation.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from govharness.core.corpus import Corpus, Tree
from govharness.core.entry import DOC_FILE, Entry
from govharness.core.locators import cited_in_text
from govharness.core.tables import HISTORY_HEADING
from govharness.core.text import unquoted

HEADER = ("Identifier", "Title")
SECTION = "References"
FIELDS = ("cites", "governed_by", "instantiates", "refers_to")
SECTION_RE = re.compile(
    rf"^## {SECTION}\s*\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL
)


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
    named: set[str] = set()
    for entry in members_of(corpus, doc_id):
        text = without_section(entry.body)
        named |= cited_in_text(corpus.by_id, unquoted(text))
        for name in FIELDS:
            named |= {str(v) for v in entry.meta.get(name) or []}
    found = {document_of(corpus, ident) for ident in named}
    return sorted(d for d in found if d and d != doc_id)


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
