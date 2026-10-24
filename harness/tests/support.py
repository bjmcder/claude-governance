"""Shared fixtures of the tests: copies of the live corpus.

Nothing here writes to the live corpus: tests damage deep copies held
in memory, or copies under a fresh temporary directory.
"""

from __future__ import annotations

import copy
import shutil
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.core.entry import Entry
from govharness.ledger.chain import read_ledger
from govharness.ledger.transactions import Transaction

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "governance"
Index = dict[str, Entry]
_LIVE: list[Entry] = []


def live_entries() -> list[Entry]:
    """Return a deep copy of the live corpus entries, read once.

    Returns
    -------
    list[Entry]
        Entries that a test may change freely.
    """
    if not _LIVE:
        _LIVE.extend(load_entries(read_tree(ROOT)))
    return copy.deepcopy(_LIVE)


def live_index() -> Index:
    """Return a copy of the live corpus entries by identifier.

    Returns
    -------
    Index
        Entries that a test may change freely.
    """
    return {str(e.meta["id"]): e for e in live_entries()}


def live_ledger() -> list[Transaction]:
    """Return a copy of the live ledger.

    Returns
    -------
    list[Transaction]
        Entries that a test may change freely.
    """
    return copy.deepcopy(read_ledger(ROOT))


def next_editorial(revision: str) -> str:
    """Return the editorial revision that follows a revision.

    Parameters
    ----------
    revision : str
        Revision number, such as ``1.4`` or ``1.1.1``.

    Returns
    -------
    str
        The next editorial revision, such as ``1.4.1`` or ``1.1.2``.
    """
    parts = revision.split(".")
    if len(parts) == 2:
        return f"{revision}.1"
    return ".".join([*parts[:2], str(int(parts[2]) + 1)])


def live_revision(document: str) -> str:
    """Return the revision of a document in the live corpus.

    Amendment tests raise a live document; reading its revision keeps
    them true after the corpus is amended.

    Parameters
    ----------
    document : str
        Identifier of the document, such as ``STND.INSTR``.

    Returns
    -------
    str
        Its revision field.
    """
    return str(live_index()[document].meta["revision"])


def corpus_of(index: Index) -> Corpus:
    """Return the corpus view of a (damaged) index.

    Parameters
    ----------
    index : Index
        Entries by identifier.

    Returns
    -------
    Corpus
        The indexed view.
    """
    return Corpus(list(index.values()))


@contextmanager
def corpus_copy() -> Iterator[Path]:
    """Copy the live corpus into a fresh temporary directory.

    Yields
    ------
    Path
        Root of the copy, removed afterwards.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "governance"
        shutil.copytree(ROOT, root)
        yield root
