"""Compose the reading copy of each divided standard from the corpus.

A reading copy puts a standard's own text, its numbered provisions, and
its revision history into one Markdown file for a reader. It is derived:
the per-provision files are the system of record, and the header that
names each revision and its ledger entry is read from the ledger, so a
copy cannot drift from the corpus unnoticed (``compose --check``).

The provisions are grouped under their ``section`` in the order the
sections first appear by number, each with its mode and what it
instantiates. A copy may carry appendices, documents printed after the
revision history, such as the mnemonic register after STND.IDENT.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.tables import HISTORY_HEADING
from govharness.ledger.transactions import Transaction, revision_named

REVISION_TYPES = {"adopt", "amend"}


@dataclass(frozen=True)
class ReadingCopy:
    """One reading copy to compose.

    Parameters
    ----------
    document : str
        Identifier of the divided standard, such as ``STND.DRAFT``.
    file_name : str
        Name of the copy in the rendered directory.
    appendices : tuple[str, ...]
        Identifiers of the documents printed after the history.
    """

    document: str
    file_name: str
    appendices: tuple[str, ...] = ()


READING_COPIES: tuple[ReadingCopy, ...] = (
    ReadingCopy("STND.DFLT", "defaults.md"),
    ReadingCopy("STND.INSTR", "agent-instructions.md"),
    ReadingCopy("STND.DRAFT", "drafting-standard.md"),
    ReadingCopy("STND.IDENT", "identifier-standard.md", ("MNEM",)),
    ReadingCopy("STND.CLASS", "class-criteria.md"),
    ReadingCopy("STND.HARN", "harness-specification.md"),
)


def series(items: list[str]) -> str:
    """Join items as an English series with a serial comma.

    Parameters
    ----------
    items : list[str]
        Phrases.

    Returns
    -------
    str
        ``a``, ``a and b``, or ``a, b, and c``.
    """
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def revision_entries(
    ledger: list[Transaction], document: str
) -> list[Transaction]:
    """Return the ledger entries that record a document's revisions.

    Parameters
    ----------
    ledger : list[Transaction]
        Ledger entries in order.
    document : str
        Identifier of the document.

    Returns
    -------
    list[Transaction]
        Its ``adopt`` and ``amend`` transactions, in ledger order.
    """
    return [
        e
        for e in ledger
        if e.get("type") in REVISION_TYPES
        and document in (e.get("targets") or [])
    ]


def _revision_phrase(entry: Transaction, where: str) -> str:
    """Name the revision an entry records, its entry number, and date.

    Parameters
    ----------
    entry : Transaction
        A revision transaction.
    where : str
        ``ledger entry`` for the first phrase, ``entry`` after it.

    Returns
    -------
    str
        Such as ``1.0.1 in entry 11 (2026-10-09)``.
    """
    number = revision_named(str(entry.get("rationale", ""))) or "a revision"
    date = str(entry.get("at", ""))[:10]
    return f"{number} in {where} {entry.get('seq')} ({date})"


def header(
    doc: Entry, ledger: list[Transaction], appendices: tuple[str, ...]
) -> str:
    """Write the paragraph under a reading copy's title.

    Parameters
    ----------
    doc : Entry
        The standard's document entry.
    ledger : list[Transaction]
        Ledger entries in order.
    appendices : tuple[str, ...]
        Documents printed after the history.

    Returns
    -------
    str
        The adoption and each later revision with its ledger entry and
        date, the system of record, the withdrawn identifiers, and the
        appendices.
    """
    entries = revision_entries(ledger, str(doc.meta["id"]))
    sentences: list[str] = []
    if entries:
        first, later = entries[0], entries[1:]
        adopter = doc.meta.get("adopted_by")
        by = f" by {adopter}" if adopter else ""
        opening = (
            f"Adopted{by} as revision "
            f"{_revision_phrase(first, 'ledger entry')}"
            if first.get("type") == "adopt"
            else f"Revised to {_revision_phrase(first, 'ledger entry')}"
        )
        if later:
            revised = [_revision_phrase(e, "entry") for e in later]
            opening += f"; revised to {series(revised)}"
        sentences.append(opening + ".")
    folder = PurePosixPath(doc.path).parent.as_posix()
    sentences.append(
        "This reading copy is composed from the per-provision files in "
        f"{folder}/ of the governance harness; the harness files are the "
        "system of record."
    )
    withdrawn = [str(w) for w in doc.meta.get("withdrawn") or []]
    if withdrawn:
        sentences.append(
            f"Withdrawn identifiers, never reused: {series(withdrawn)}."
        )
    sentences += [
        f"The register {ident} follows the revision history."
        for ident in appendices
    ]
    return " ".join(sentences)


def provisions_of(corpus: Corpus, doc: Entry) -> list[Entry]:
    """Return a standard's numbered provisions in reading order.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc : Entry
        The standard's document entry.

    Returns
    -------
    list[Entry]
        Provisions grouped by section, the sections in the order they
        first appear by number, and by number within a section.
    """
    folder = doc.path.parent
    numbered = sorted(
        (
            e
            for e in corpus.entries
            if e.path.parent == folder and e.path.stem.isdigit()
        ),
        key=lambda e: int(e.path.stem),
    )
    order: dict[str, int] = {}
    for entry in numbered:
        order.setdefault(str(entry.meta.get("section", "")), len(order))
    return sorted(
        numbered,
        key=lambda e: (
            order[str(e.meta.get("section", ""))],
            int(e.path.stem),
        ),
    )


def _provision_block(entry: Entry, level: str) -> str:
    """Write one provision with its mode and what it instantiates.

    Parameters
    ----------
    entry : Entry
        A numbered provision.
    level : str
        Heading marks, ``###`` or ``####``.

    Returns
    -------
    str
        Heading, mode line, and body, ending in a blank line.
    """
    meta = entry.meta
    mode = str(meta.get("mode", "")).capitalize()
    instantiated = ", ".join(meta.get("instantiates") or [])
    return (
        f"{level} {meta['id']} {meta.get('title', '')}\n\n"
        f"{mode}. Instantiates {instantiated}.\n\n{entry.body}\n\n"
    )


def compose(
    corpus: Corpus, ledger: list[Transaction], copy: ReadingCopy
) -> str:
    """Compose the reading copy of one divided standard.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    ledger : list[Transaction]
        Ledger entries in order.
    copy : ReadingCopy
        The copy to compose.

    Returns
    -------
    str
        Markdown text ending in one newline.

    Raises
    ------
    KeyError
        If the standard or an appendix is not in the corpus.
    """
    doc = corpus.by_id[copy.document]
    main, _, history = doc.body.partition(HISTORY_HEADING)
    out = (
        f"# {doc.meta.get('title', '')} ({copy.document}) "
        f"{doc.meta.get('revision', '')}\n\n"
        f"{header(doc, ledger, copy.appendices)}\n\n"
        f"{main.strip()}\n\n## Provisions\n\n"
    )
    provisions = provisions_of(corpus, doc)
    sectioned = any("section" in e.meta for e in provisions)
    section = None
    for entry in provisions:
        if sectioned and entry.meta.get("section") != section:
            section = entry.meta.get("section")
            out += f"### {section}\n\n"
        out += _provision_block(entry, "####" if sectioned else "###")
    if history:
        out += HISTORY_HEADING + history
    for ident in copy.appendices:
        out = out.rstrip() + f"\n\n## The register {ident}\n\n"
        out += corpus.by_id[ident].body
    return out.rstrip() + "\n"


def reading_copies(
    corpus: Corpus, ledger: list[Transaction]
) -> dict[PurePosixPath, str]:
    """Compose every reading copy.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    ledger : list[Transaction]
        Ledger entries in order.

    Returns
    -------
    dict[PurePosixPath, str]
        Text by file name, relative to the rendered directory.
    """
    return {
        PurePosixPath(copy.file_name): compose(corpus, ledger, copy)
        for copy in READING_COPIES
    }
