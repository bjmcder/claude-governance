"""Amendment primitives: edit, raise a revision, record the transaction.

An amendment script applies them in order to the root it is given:
``replace_text`` for each text change, ``raise_revision`` for each
document whose revision changes, and ``record_transaction`` once per
ledger transaction. Every primitive takes the corpus root as a
parameter and holds no path of its own, so the same script can be
rehearsed on a copy (``rehearse``) before it runs on the live corpus.
Each refuses, with ``ValueError``, an edit it cannot make exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from govharness.checks.verification import Verification
from govharness.core.corpus import (
    corpus_hash,
    is_directory,
    read_text,
    read_tree,
)
from govharness.core.entry import DOC_FILE
from govharness.core.tables import HISTORY_HEADING
from govharness.derive.manifests import stale_manifests
from govharness.ledger.chain import append
from govharness.ledger.transactions import Transaction
from govharness.workflows.verification import usable_store, verify_corpus


@dataclass(frozen=True)
class Change:
    """The fields of one unsigned ledger transaction.

    Parameters
    ----------
    kind : str
        Transaction type, such as ``amend``.
    actor : str
        Role label of the actor, such as ``The Custodian``.
    role : str
        Role that acts, such as ``custodians``.
    at : str
        Time of the transaction, ISO 8601.
    authority : list[str]
        Provisions that authorize it.
    targets : list[str]
        Identifiers it changes or concerns.
    scope : list[str]
        Directories whose content it pins.
    rationale : str
        Reason, naming the revision it records.
    """

    kind: str
    actor: str
    role: str
    at: str
    authority: list[str]
    targets: list[str]
    scope: list[str]
    rationale: str


@dataclass
class Recorded:
    """A transaction appended by ``record_transaction``.

    Parameters
    ----------
    entry : Transaction
        The ledger entry as written.
    verification : Verification
        The verification run after the append.
    """

    entry: Transaction
    verification: Verification


def _inside(root: Path, rel: str) -> Path:
    """Return the path of a file under the root, refusing any other.

    Parameters
    ----------
    root : Path
        Corpus root.
    rel : str
        Path relative to the root, with ``/`` separators.

    Returns
    -------
    Path
        ``root / rel``.

    Raises
    ------
    ValueError
        If the path is absolute or climbs out of the root.
    """
    pure = PurePosixPath(rel)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"{rel}: not a path inside the corpus")
    return root / pure


def replace_text(root: Path, rel: str, pairs: list[tuple[str, str]]) -> None:
    """Replace exact texts, each occurring once, in one corpus file.

    The replacements apply in order, each to the text the previous one
    left; the file is written only when every one applies.

    Parameters
    ----------
    root : Path
        Corpus root.
    rel : str
        File path relative to the root, such as ``STND/DFLT/15.md``.
    pairs : list[tuple[str, str]]
        Old and new text of each replacement.

    Raises
    ------
    ValueError
        If the path leaves the root, or an old text does not occur
        exactly once.
    """
    path = _inside(root, rel)
    text = read_text(path)
    for old, new in pairs:
        count = text.count(old)
        if count != 1:
            raise ValueError(
                f"{rel}: {old[:80]!r} occurs {count} times, not once"
            )
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def _history_end(lines: list[str]) -> int:
    """Return the index of the last row of the Revision History table.

    Parameters
    ----------
    lines : list[str]
        Lines of a document file.

    Returns
    -------
    int
        Index of the last table row whose first cell is a revision
        number, between the heading and the next heading.

    Raises
    ------
    ValueError
        If the document has no such section or row.
    """
    if HISTORY_HEADING not in lines:
        raise ValueError(f"no section {HISTORY_HEADING[3:]}")
    start = lines.index(HISTORY_HEADING)
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("#")),
        len(lines),
    )
    rows = [
        i
        for i in range(start + 1, end)
        if lines[i].startswith("| ")
        and lines[i].split("|")[1].strip()[:1].isdigit()
    ]
    if not rows:
        raise ValueError(f"no row under {HISTORY_HEADING[3:]}")
    return rows[-1]


def raise_revision(
    root: Path, document: str, old: str, new: str, row: str
) -> None:
    """Raise a document's revision field and add its history row.

    Parameters
    ----------
    root : Path
        Corpus root.
    document : str
        Directory of the document, such as ``STND/DFLT``; its
        ``_doc.md`` is edited.
    old : str
        Current revision, such as ``1.1``.
    new : str
        New revision, such as ``1.1.1``.
    row : str
        Markdown row added after the last row of the Revision History,
        such as ``| 1.1.1 | 2026-10-10 | Editorial amendment ... |``.

    Raises
    ------
    ValueError
        If the path leaves the root, the field does not read ``old``
        exactly once, or the document keeps no revision history.
    """
    rel = f"{document.rstrip('/')}/{DOC_FILE}"
    path = _inside(root, rel)
    text = read_text(path)
    field = f'revision: "{old}"'
    if text.count(field) != 1:
        raise ValueError(f"{rel}: the field {field} does not occur once")
    lines = text.replace(field, f'revision: "{new}"').rstrip("\n").split("\n")
    lines.insert(_history_end(lines) + 1, row)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def record_transaction(root: Path, change: Change) -> Recorded:
    """Rebuild the manifests, append the transaction, and verify.

    The entry is not signed; a signed entry goes through ``ledger
    append --sign``.

    Parameters
    ----------
    root : Path
        Corpus root.
    change : Change
        The transaction's fields.

    Returns
    -------
    Recorded
        The entry as written and the verification after it, which
        reuses the solve cache the environment names (unit 0011).

    Raises
    ------
    ValueError
        If a scope names no directory, the ledger refuses the entry, or
        the solve cache cannot be used (``usable_store``); the cache and
        the scopes are checked before anything is written.
    """
    missing = [s for s in change.scope if not is_directory(root, s)]
    if missing:
        raise ValueError(f"scope names no directory: {', '.join(missing)}")
    store = usable_store(root, True)
    for rel, text in stale_manifests(read_tree(root)).items():
        (root / rel).write_text(text, encoding="utf-8")
    scope = list(change.scope)
    entry = append(
        root,
        {
            "at": change.at,
            "type": change.kind,
            "actor": change.actor,
            "role": change.role,
            "authority": list(change.authority),
            "targets": list(change.targets),
            "scope": scope,
            "corpus_hash": corpus_hash(root, scope) if scope else None,
            "rationale": change.rationale,
            "signature": "",
        },
    )
    return Recorded(entry, verify_corpus(root, cache=store or False))
