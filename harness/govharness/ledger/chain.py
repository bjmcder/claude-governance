"""Read ledger files and append hash-chained transactions.

This is the one module that reads or appends a ledger file (decision
0001, DSGN.16). The ledger (``ledger.jsonl``) is append-only: each entry
records the hash of the previous entry and its own hash over every
other field. A transaction's ``scope`` names the directories whose
content it pins; their combined hash is stored as ``corpus_hash``. With
a signer, the signer's ``gpg`` key signs the entry digest before the
entry is hashed; without one the ``signature`` field is empty. Another
ledger, such as the ledger of a piece of work, carries its identifier
in the field ``ledger``.

An append first checks the whole existing chain (sequence numbers,
``prev`` links, and entry hashes) and refuses a broken one, so that a
new entry never seals a damaged history. It writes one line, then
flushes and syncs the file, so that a crash cannot leave the entry half
written in the operating system's buffers. The protocol for concurrent
appends (DSGN.15): each holds an exclusive ``flock`` on the ledger file
from reading the chain to syncing its line, so two appends never take
the same sequence number.
"""

from __future__ import annotations

import fcntl
import os
from pathlib import Path
from typing import Any

from govharness.core.corpus import read_text
from govharness.core.entry import DOC_FILE, LEDGER_FILE
from govharness.core.hashing import canonical_json, ledger_entry_hash
from govharness.ledger.gpg import sign_digest
from govharness.ledger.register import (
    REGISTER_ID,
    active_signers,
    read_register,
)
from govharness.ledger.transactions import (
    GOVERNANCE,
    TYPES,
    Transaction,
    chain_problems,
    entry_digest,
    ledger_of,
    parse_ledger,
)

Signer = tuple[str, Path | None]


def read_ledger_file(path: Path) -> list[Transaction]:
    """Return the entries of a ledger file.

    Parameters
    ----------
    path : Path
        Ledger file.

    Returns
    -------
    list[Transaction]
        Entries in order.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    return parse_ledger(path.read_text(encoding="utf-8"))


def read_ledger(root: Path, path: Path | None = None) -> list[Transaction]:
    """Return a ledger's entries, or none when it has no file yet.

    Parameters
    ----------
    root : Path
        Corpus root.
    path : Path | None
        Ledger file; ``None`` is the corpus ledger.

    Returns
    -------
    list[Transaction]
        Entries in order; empty if the file does not exist.
    """
    path = path or root / LEDGER_FILE
    if not path.exists():
        return []
    return read_ledger_file(path)


def append(
    root: Path,
    entry: dict[str, Any],
    signer: Signer | None = None,
    path: Path | None = None,
    ledger: str = GOVERNANCE,
) -> Transaction:
    """Chain, optionally sign, and append one transaction.

    Parameters
    ----------
    root : Path
        Corpus root.
    entry : dict[str, Any]
        Transaction fields without ``seq``, ``prev``, or ``hash``.
    signer : Signer | None
        Key and keyring directory that sign the entry, or ``None``.
    path : Path | None
        Ledger file; ``None`` is the corpus ledger.
    ledger : str
        Identifier of the ledger; any other than ``governance`` is
        written into the entry, so that its signature binds to that
        ledger.

    Returns
    -------
    Transaction
        The entry as written.

    Raises
    ------
    ValueError
        If the transaction type is unknown, the ledger file holds
        another ledger, or its chain is broken.
    """
    if entry["type"] not in TYPES:
        raise ValueError(f"unknown transaction type: {entry['type']}")
    path = path or root / LEDGER_FILE
    with path.open("a+", encoding="utf-8") as handle:
        # Held until the line is synced: a concurrent append waits, then
        # reads the chain this one extended.
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        text = handle.read()
        written = _chained(root, entry, parse_ledger(text), path, ledger)
        if signer is not None:
            written["signature"] = sign_digest(entry_digest(written), *signer)
        written["hash"] = ledger_entry_hash(written)
        # A last line without its newline would merge with the new one.
        separator = "\n" if text and not text.endswith("\n") else ""
        handle.write(separator + canonical_json(written) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return written


def _chained(
    root: Path,
    entry: dict[str, Any],
    history: list[Transaction],
    path: Path,
    ledger: str,
) -> Transaction:
    """Return an entry numbered and linked after an intact history.

    Parameters
    ----------
    root : Path
        Corpus root, which holds the signer register.
    entry : dict[str, Any]
        Transaction fields without ``seq``, ``prev``, or ``hash``.
    history : list[Transaction]
        The entries already in the ledger file.
    path : Path
        The ledger file, named in a refusal.
    ledger : str
        Identifier of the ledger.

    Returns
    -------
    Transaction
        The entry with ``seq``, ``prev``, and, where they apply, the
        ``ledger`` identifier or the open ``signers`` of the register.

    Raises
    ------
    ValueError
        If the file holds another ledger or its chain is broken.
    """
    if any(ledger_of(old) != ledger for old in history):
        raise ValueError(f"{path} holds entries of another ledger")
    broken = chain_problems(history)
    if broken:
        raise ValueError(
            f"{path} has a broken chain; nothing appended: "
            + "; ".join(broken)
        )
    chained = {
        "seq": len(history) + 1,
        **entry,
        "prev": history[-1]["hash"] if history else None,
    }
    if ledger != GOVERNANCE:
        chained["ledger"] = ledger
    elif REGISTER_ID in (entry.get("scope") or []):
        register = read_register(read_text(root / REGISTER_ID / DOC_FILE))
        chained["signers"] = active_signers(register)
    return chained
