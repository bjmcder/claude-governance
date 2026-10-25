"""Transaction types and the links of the hash chain.

Each ledger entry records the hash of the entry before it (``prev``) and
its own hash over every other field (``hash``), so that an edit to an
entry, or a removed or reordered entry, breaks the chain (GOV.36).
"""

from __future__ import annotations

import json
import re
from pathlib import PurePosixPath
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

    Lines end at a line feed only. The ledger is written with Unicode
    unescaped, so a text field may hold U+2028, U+2029, or U+0085,
    which ``str.splitlines`` would also take for line ends.

    Parameters
    ----------
    text : str
        Contents of a ``.jsonl`` ledger.

    Returns
    -------
    list[Transaction]
        Entries in file order; blank lines are skipped.

    Raises
    ------
    ValueError
        If a line is not JSON; the message names its line number.
    """
    entries: list[Transaction] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except ValueError as error:
            raise ValueError(f"line {number}: {error}") from error
    return entries


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


def head_problems(entries: list[Transaction], head: object) -> list[str]:
    """Return how a ledger lacks the entry its head pin names, if it does.

    Any prefix of an intact chain is an intact chain, so only a record
    of the head kept where the agent cannot write it shows that entries
    were cut from the end. The human owner keeps it in the signer
    configuration (``gpg.read_config``).

    Parameters
    ----------
    entries : list[Transaction]
        The ledger, in order.
    head : object
        The head pin, ``{"seq": N, "hash": H}``, or ``None`` for none.

    Returns
    -------
    list[str]
        A line when the pin is malformed, or when entry N is missing or
        its hash is not H; the entries after N are not pinned.
    """
    if head is None:
        return []
    seq = head.get("seq") if isinstance(head, dict) else None
    pinned = head.get("hash") if isinstance(head, dict) else None
    if (
        not isinstance(seq, int)
        or isinstance(seq, bool)
        or seq < 1
        or not isinstance(pinned, str)
    ):
        problem = f"the signer configuration's head pin is malformed: {head}"
    elif seq > len(entries):
        problem = (
            f"the ledger ends at entry {len(entries)}, before entry {seq}, "
            "which the signer configuration pins: entries were cut"
        )
    elif entries[seq - 1].get("hash") != pinned:
        problem = (
            f"ledger entry {seq} is not the one the signer configuration "
            "pins: the ledger was rewritten"
        )
    else:
        return []
    return [problem]


def covers(outer: str, inner: str) -> bool:
    """Return True when one scope path holds another.

    Parameters
    ----------
    outer : str
        Scope path, such as ``STND``.
    inner : str
        Scope path, such as ``STND/DFLT``.

    Returns
    -------
    bool
        Whether ``inner`` is ``outer`` or lies under it.
    """
    parts = PurePosixPath(outer).parts
    return PurePosixPath(inner).parts[: len(parts)] == parts


def scope_key(entry: Transaction) -> tuple[str, ...]:
    """Return the scope of an entry as the key of its pin.

    Parameters
    ----------
    entry : Transaction
        Ledger entry.

    Returns
    -------
    tuple[str, ...]
        Its scope paths, sorted; empty when it pins nothing.
    """
    return tuple(
        sorted(s for s in entry.get("scope") or [] if isinstance(s, str))
    )


def latest_pins(entries: list[Transaction]) -> list[Transaction]:
    """Return the latest transaction of each scope, in ledger order.

    A pin holds until the next transaction of the same scope, the same
    paths in any order (STND.HARN.9: "the latest governance-ledger
    transaction with that scope"); a transaction of another scope does
    not replace it, even where it covers the same files.

    Parameters
    ----------
    entries : list[Transaction]
        The ledger, in order.

    Returns
    -------
    list[Transaction]
        For each scope that some entry pins, its last entry.
    """
    latest: dict[tuple[str, ...], tuple[int, Transaction]] = {}
    for position, entry in enumerate(entries):
        if scope_key(entry):
            latest[scope_key(entry)] = (position, entry)
    return [entry for _, entry in sorted(latest.values(), key=_first)]


def _first(pair: tuple[int, Transaction]) -> int:
    """Return the position of a (position, entry) pair.

    Parameters
    ----------
    pair : tuple[int, Transaction]
        Position in the ledger and the entry.

    Returns
    -------
    int
        The position.
    """
    return pair[0]
