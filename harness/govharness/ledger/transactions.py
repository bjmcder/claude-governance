"""Transaction types and the links of the hash chain.

Each ledger entry records the hash of the entry before it (``prev``) and
its own hash over every other field (``hash``), so that an edit to an
entry, or a removed or reordered entry, breaks the chain (GOV.36).
"""

from __future__ import annotations

import json
import re
from typing import Any

from govharness.core.hashing import ledger_entry_hash

GOVERNANCE = "governance"
ALL_LEDGERS = "all"
# The types of STND.HARN.7.
TYPES = {
    "adopt",
    "amend",
    "retire",
    "classify",
    "set-class",
    "promote",
    "authorize",
    "revoke",
    "register",
    "waive",
    "rule",
    "declare-axiom",
    "release",
    "review",
    "configure",
    "annotate",
}
Transaction = dict[str, Any]
REVISION_NAMED_RE = re.compile(r"revision (\d+(?:\.\d+)+)", re.IGNORECASE)


def parse_ledger(text: str) -> list[Transaction]:
    """Parse the lines of a ledger file.

    Parameters
    ----------
    text : str
        Contents of a ``.jsonl`` ledger.

    Returns
    -------
    list[Transaction]
        Entries in file order; blank lines are skipped.
    """
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def ledger_of(entry: Transaction) -> str:
    """Return the ledger identifier of an entry.

    Parameters
    ----------
    entry : Transaction
        Ledger entry.

    Returns
    -------
    str
        Its field ``ledger``, or ``governance`` when absent.
    """
    return str(entry.get("ledger", GOVERNANCE))


def entry_digest(entry: Transaction) -> str:
    """Return the digest a signature covers.

    Parameters
    ----------
    entry : Transaction
        Ledger entry, with or without ``hash``.

    Returns
    -------
    str
        The entry hash computed with an empty ``signature`` field.
    """
    return ledger_entry_hash({**entry, "signature": ""})


def revision_named(rationale: str) -> str | None:
    """Return the revision number a transaction's reason names.

    Parameters
    ----------
    rationale : str
        The ``rationale`` field, such as ``Minor amendment of STND.DRAFT,
        revision 1.1, ...``.

    Returns
    -------
    str | None
        The first revision number named, or ``None``.
    """
    found = REVISION_NAMED_RE.search(rationale)
    return found[1] if found else None


def chain_problems(entries: list[Transaction]) -> list[str]:
    """Return every break of a ledger's chain.

    Parameters
    ----------
    entries : list[Transaction]
        Ledger entries in file order.

    Returns
    -------
    list[str]
        The lines of ``entry_problems`` for every entry, in order.
    """
    problems: list[str] = []
    previous = None
    for position, entry in enumerate(entries, start=1):
        problems += entry_problems(entry, position, previous)
        previous = entry.get("hash")
    return problems


def entry_problems(
    entry: Transaction, position: int, previous: str | None
) -> list[str]:
    """Return how one entry breaks the chain at its position, if it does.

    The sequence number must equal the position: signer windows ("Last
    entry") and required signatures ("From entry") compare the ``seq``
    an entry claims, so an entry renumbered with its links rebuilt
    would otherwise escape them.

    Parameters
    ----------
    entry : Transaction
        Ledger entry.
    position : int
        Its position in the file, from 1.
    previous : str | None
        Hash of the entry before it, or ``None`` for the first entry.

    Returns
    -------
    list[str]
        A line when ``seq`` is not the position, then the lines of
        ``link_problems``.
    """
    problems: list[str] = []
    if entry.get("seq") != position:
        problems.append(
            f"ledger sequence broken at entry {position}: "
            f"seq {entry.get('seq')}"
        )
    return problems + link_problems(entry, previous)


def link_problems(entry: Transaction, previous: str | None) -> list[str]:
    """Return how one entry breaks the chain, if it does.

    Parameters
    ----------
    entry : Transaction
        Ledger entry.
    previous : str | None
        Hash of the entry before it, or ``None`` for the first entry.

    Returns
    -------
    list[str]
        A line when ``prev`` is not the previous hash, and a line when
        ``hash`` is not the entry's own hash.
    """
    problems: list[str] = []
    if entry.get("prev") != previous:
        problems.append(f"ledger chain broken at seq {entry.get('seq')}")
    if entry.get("hash") != ledger_entry_hash(entry):
        problems.append(f"ledger entry altered at seq {entry.get('seq')}")
    return problems
