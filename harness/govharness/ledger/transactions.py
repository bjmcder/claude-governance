"""Transaction types, the form of a ledger line, and the hash chain.

Each ledger entry records the hash of the entry before it (``prev``) and
its own hash over every other field (``hash``), so that an edit to an
entry, or a removed or reordered entry, breaks the chain (GOV.36). The
hash covers the parsed entry, not the text of its line, so the line is
held to one form as well: a key given twice, a line that is not the
canonical serialization of its entry (STND.HARN.6), and an entry
without exactly the fields of STND.HARN.7 are each reported, since each
lets the text that a person or ``grep`` reads differ from the entry
that the chain verifies.
"""

from __future__ import annotations

import json
import re
from pathlib import PurePosixPath
from typing import Any

from govharness.core.hashing import canonical_json, ledger_entry_hash

GOVERNANCE = "governance"
ALL_LEDGERS = "all"
# The signer register, whose transactions alone carry ``signers``.
REGISTER_ID = "SIGNR"
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
# The fields of STND.HARN.7 that every transaction holds; ``signers``
# and ``ledger`` are held only where that provision says.
FIELDS = frozenset(
    {
        "seq",
        "type",
        "actor",
        "role",
        "authority",
        "targets",
        "scope",
        "rationale",
        "at",
        "corpus_hash",
        "prev",
        "signature",
        "hash",
    }
)
SIGNERS = "signers"
LEDGER = "ledger"
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
        If a line is not JSON, or an object of it gives a key twice,
        which JSON readers resolve differently; the message names its
        line number.
    """
    entries: list[Transaction] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line, object_pairs_hook=_object))
        except ValueError as error:
            raise ValueError(f"line {number}: {error}") from error
    return entries


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build one JSON object of a ledger line, refusing a repeated key.

    Parameters
    ----------
    pairs : list[tuple[str, Any]]
        The object's keys and values, in the order of the text.

    Returns
    -------
    dict[str, Any]
        The object.

    Raises
    ------
    ValueError
        If a key occurs twice; the message names it.
    """
    keys = [key for key, _ in pairs]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise ValueError(f"duplicate key {', '.join(map(repr, repeated))}")
    return dict(pairs)


def form_problems(text: str) -> list[str]:
    """Return each line of a ledger not in the form of STND.HARN.6.

    Parameters
    ----------
    text : str
        Contents of a ledger file, as stored.

    Returns
    -------
    list[str]
        A line for each blank line before the last line feed, and for
        each line other than the canonical JSON of its entry (sorted
        keys, no white space between tokens, non-ASCII characters
        unescaped), so that the hash a person computes from the text
        is the one the chain verifies.
    """
    problems: list[str] = []
    lines = text.split("\n")
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            if number < len(lines):
                problems.append(f"ledger line {number} is blank")
            continue
        try:
            canonical = canonical_json(
                json.loads(line, object_pairs_hook=_object)
            )
        except ValueError:
            # Text that a reader of lines takes apart differently, such
            # as two entries joined by a carriage return.
            canonical = None
        if line != canonical:
            problems.append(
                f"ledger line {number} is not in the form of STND.HARN.6: "
                "sorted keys, no white space, Unicode unescaped"
            )
    return problems


def field_problems(entry: Transaction) -> list[str]:
    """Return how an entry departs from the fields of STND.HARN.7.

    Parameters
    ----------
    entry : Transaction
        Ledger entry.

    Returns
    -------
    list[str]
        A line naming the fields missing; a line naming the fields
        that STND.HARN.7 does not list; a line when ``type`` is none of
        its types; a line when ``signers`` stands on a transaction other
        than one of the governance ledger whose scope names the signer
        register; and a line when ``ledger`` names the governance
        ledger, whose transactions carry no such field.
    """
    seq = entry.get("seq")
    problems: list[str] = []
    missing = sorted(FIELDS - entry.keys())
    if missing:
        problems.append(
            f"ledger entry {seq} lacks the fields {', '.join(missing)}"
        )
    other = sorted(entry.keys() - FIELDS - {SIGNERS, LEDGER})
    if other:
        problems.append(
            f"ledger entry {seq} holds fields outside STND.HARN.7: "
            + ", ".join(other)
        )
    if "type" in entry and entry["type"] not in TYPES:
        problems.append(
            f"ledger entry {seq} has the unknown type {entry['type']!r}"
        )
    scope = entry.get("scope")
    if SIGNERS in entry and (
        LEDGER in entry
        or not isinstance(scope, list)
        or REGISTER_ID not in scope
    ):
        problems.append(
            f"ledger entry {seq} holds signers but is no transaction of "
            f"the governance ledger whose scope names {REGISTER_ID}"
        )
    if entry.get(LEDGER) == GOVERNANCE:
        problems.append(
            f"ledger entry {seq} names the governance ledger in the field "
            "ledger, which only another ledger's entries carry"
        )
    return problems


def file_problems(text: str, entries: list[Transaction]) -> list[str]:
    """Return how a ledger file breaks its form, its fields, or its chain.

    Parameters
    ----------
    text : str
        Contents of the file.
    entries : list[Transaction]
        Its entries, as ``parse_ledger`` reads them from ``text``.

    Returns
    -------
    list[str]
        The lines of ``form_problems``, then, entry by entry, those of
        ``entry_problems`` and ``field_problems``.
    """
    problems = form_problems(text)
    previous = None
    for position, entry in enumerate(entries, start=1):
        problems += entry_problems(entry, position, previous)
        problems += field_problems(entry)
        previous = entry.get("hash")
    return problems


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


def reaches(scope: tuple[str, ...], path: str) -> bool:
    """Return True when a scope reaches a path (the term Reach of STND.HARN).

    Parameters
    ----------
    scope : tuple[str, ...]
        Scope paths of a transaction.
    path : str
        A path, such as a scope path of another transaction or a file.

    Returns
    -------
    bool
        Whether one of the scope's paths is the path or a directory
        above it.
    """
    return any(covers(own, path) for own in scope)


def pins_in_force(entries: list[Transaction]) -> list[Transaction]:
    """Return the pins in force, in ledger order (STND.HARN.9).

    A transaction with a scope is a pin in force unless a later one has
    a scope that reaches each path of its scope (the terms Pin in force
    and Reach of STND.HARN). The same scope again ends a pin, and so
    does a wider one; a narrower scope, or one that shares only some
    paths, leaves it in force.

    Parameters
    ----------
    entries : list[Transaction]
        The ledger, in order.

    Returns
    -------
    list[Transaction]
        Each entry with a scope that no later entry's scope reaches
        whole.
    """
    pinned = [entry for entry in entries if scope_key(entry)]
    return [
        entry
        for position, entry in enumerate(pinned)
        if not any(
            all(reaches(scope_key(later), p) for p in scope_key(entry))
            for later in pinned[position + 1 :]
        )
    ]
