"""Read ledger files and append hash-chained transactions.

This is the one module that reads or appends a ledger file (decision
0001, DSGN.16). The ledger (``ledger.jsonl``) is append-only: each entry
records the hash of the previous entry and its own hash over every other
field. A transaction's ``scope`` names the directories and Markdown
files whose content it pins; their combined hash is stored as
``corpus_hash``. With a signer, the signer's ``gpg`` key signs the entry
digest before the entry is hashed; without one the ``signature`` field
is empty. Another ledger, such as the ledger of a piece of work, carries
its identifier in the field ``ledger``.

An append first checks the whole existing ledger (the form of each
line, the fields of each entry, sequence numbers, ``prev`` links, and
entry hashes; ``transactions.file_problems``) and refuses a broken one,
so that a new entry never seals a damaged history. It makes no
directory: the ledger file's directory must exist. It also refuses, before
writing, an entry that would itself fail ``verify`` for good, since an
entry is never edited: an unsigned entry that the signer register
requires to be signed, an unsigned register transaction, a register
transaction that records a register with problems, a scope that shares
content with a pin in force without reaching each of its paths, and a
line that does not read back as the entry. It writes one line, then
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

from govharness.core.corpus import read_optional_text
from govharness.core.entry import DOC_FILE, LEDGER_FILE
from govharness.core.hashing import canonical_json, ledger_entry_hash
from govharness.ledger.gpg import sign_digest
from govharness.ledger.register import (
    SignerRegister,
    active_signers,
    read_register,
)
from govharness.ledger.signatures import required_of
from govharness.ledger.transactions import (
    GOVERNANCE,
    REGISTER_ID,
    TYPES,
    Transaction,
    covers,
    entry_digest,
    file_problems,
    ledger_of,
    parse_ledger,
    pins_in_force,
    reaches,
    scope_key,
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
    ValueError
        If a line is not JSON; the message names the file and line.
    """
    return _parsed(path.read_text(encoding="utf-8"), path)


def _parsed(text: str, path: Path) -> list[Transaction]:
    """Parse a ledger file's text, naming the file in a refusal.

    Parameters
    ----------
    text : str
        Contents of the file.
    path : Path
        The file.

    Returns
    -------
    list[Transaction]
        Entries in order.

    Raises
    ------
    ValueError
        If a line is not JSON. A line cut short by a crash during an
        append is one; the README says how to recover.
    """
    try:
        return parse_ledger(text)
    except ValueError as error:
        raise ValueError(f"{path}: {error}") from error


def check_ledger_file(
    path: Path, ledger: str | None = None
) -> tuple[list[Transaction], list[str]]:
    """Read a ledger file and return its entries and its problems.

    The check of ``ledger check``: it reads the file and writes nothing,
    and needs neither the corpus nor a signer register, so it verifies
    no signature.

    Parameters
    ----------
    path : Path
        Ledger file.
    ledger : str | None
        Identifier of the ledger the file holds; ``None`` takes the
        ledger of its first entry.

    Returns
    -------
    tuple[list[Transaction], list[str]]
        The entries in order, and one line for each problem: of the
        form of a line, of the fields of an entry, or of the chain
        (``transactions.file_problems``), and for each entry of another
        ledger.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is not UTF-8, or a line is not JSON or gives a key
        twice; the message names the file and line.
    """
    try:
        # Bytes as stored, so that a carriage return is seen.
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{path}: {error}") from error
    entries = _parsed(text, path)
    problems = file_problems(text, entries)
    named = ledger or (ledger_of(entries[0]) if entries else GOVERNANCE)
    problems += [
        f"ledger entry {entry.get('seq')} belongs to the ledger "
        f"{ledger_of(entry)}, not {named}"
        for entry in entries
        if ledger_of(entry) != named
    ]
    return entries, problems


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
    FileNotFoundError
        If the directory of the ledger file does not exist.
    ValueError
        If the transaction type is unknown, a line of the file is not
        JSON, the file holds another ledger, the form, fields, or chain
        of the file are broken, or the entry would fail ``verify`` for
        good (see the module); nothing is written then.
    """
    if entry["type"] not in TYPES:
        raise ValueError(f"unknown transaction type: {entry['type']}")
    path = path or root / LEDGER_FILE
    # Untranslated line ends, so that the check sees the file as stored.
    with path.open("a+", encoding="utf-8", newline="") as handle:
        # Held until the line is synced: a concurrent append waits, then
        # reads the chain this one extended.
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        text = handle.read()
        written = _chained(root, entry, text, path, ledger, signer is None)
        if signer is not None:
            written["signature"] = sign_digest(entry_digest(written), *signer)
        written["hash"] = ledger_entry_hash(written)
        line = canonical_json(written)
        if parse_ledger(line) != [written]:
            raise ValueError(
                f"the entry does not read back as written; nothing "
                f"appended: {line[:200]}"
            )
        # A last line without its newline would merge with the new one.
        separator = "\n" if text and not text.endswith("\n") else ""
        handle.write(separator + line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return written


def _chained(
    root: Path,
    entry: dict[str, Any],
    text: str,
    path: Path,
    ledger: str,
    unsigned: bool,
) -> Transaction:
    """Return an entry numbered and linked after an intact history.

    Parameters
    ----------
    root : Path
        Corpus root, which holds the signer register.
    entry : dict[str, Any]
        Transaction fields without ``seq``, ``prev``, or ``hash``.
    text : str
        The contents of the ledger file before the append.
    path : Path
        The ledger file, named in a refusal.
    ledger : str
        Identifier of the ledger.
    unsigned : bool
        Whether the entry goes in without a signature.

    Returns
    -------
    Transaction
        The entry with ``seq``, ``prev``, and, where they apply, the
        ``ledger`` identifier or the open ``signers`` of the register.

    Raises
    ------
    ValueError
        If a line of the file is not JSON, the file holds another
        ledger, its form, fields, or chain are broken, or the entry is
        refused by ``_refusals``.
    """
    history = _parsed(text, path)
    if any(ledger_of(old) != ledger for old in history):
        raise ValueError(f"{path} holds entries of another ledger")
    broken = file_problems(text, history)
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
    text = read_optional_text(root / REGISTER_ID / DOC_FILE)
    register = None if text is None else read_register(text)
    if ledger != GOVERNANCE:
        chained["ledger"] = ledger
    elif register is not None and REGISTER_ID in (entry.get("scope") or []):
        chained["signers"] = active_signers(register)
    refused = _refusals(chained, history, ledger, register, unsigned)
    if refused:
        raise ValueError("; ".join(refused) + "; nothing appended")
    return chained


def _refusals(
    chained: Transaction,
    history: list[Transaction],
    ledger: str,
    register: SignerRegister | None,
    unsigned: bool,
) -> list[str]:
    """Return why an entry, once written, would fail ``verify`` for good.

    Parameters
    ----------
    chained : Transaction
        The entry, numbered and linked.
    history : list[Transaction]
        The entries already in the ledger file, an intact chain.
    ledger : str
        Identifier of the ledger.
    register : SignerRegister | None
        The signer register of the corpus, or ``None``.
    unsigned : bool
        Whether the entry goes in without a signature.

    Returns
    -------
    list[str]
        A reason for each: the register requires the entry's actor to
        sign it; it records the register unsigned, which the anchor key
        must sign for the founding and a listed signer for every later
        change (STND.HARN.13); it records the register while the
        register has problems; or its scope shares content with a pin
        in force without reaching each of its paths (``_shared_pins``).
    """
    reasons: list[str] = []
    scope = [s for s in chained.get("scope") or [] if isinstance(s, str)]
    if register is not None and unsigned:
        reasons += [
            f"`{chained.get('actor')}` must sign entry {chained['seq']} "
            f"(required from entry {start}): use ledger append --sign KEY"
            for start in required_of(register, chained, ledger)
        ]
    if (
        register is not None
        and unsigned
        and ledger == GOVERNANCE
        and REGISTER_ID in scope
    ):
        reasons.append(
            f"a transaction of {REGISTER_ID} must be signed, by the anchor "
            "key for the founding and by a listed signer after it: use "
            "ledger append --sign KEY"
        )
    if register is not None and register.problems and REGISTER_ID in scope:
        reasons.append(
            f"{REGISTER_ID} has problems: " + " ".join(register.problems)
        )
    if ledger == GOVERNANCE and scope:
        reasons += _shared_pins(history, chained)
    return reasons


def _shared_pins(
    history: list[Transaction], chained: Transaction
) -> list[str]:
    """Return the pins in force that an entry's scope would leave stale.

    A later transaction ends a pin only where its scope reaches each
    path of the pin's scope (STND.HARN.9, the term Pin in force), so a
    scope that shares content with a pin in force and does not reach
    each of its paths leaves that pin in force, stale once the shared
    content changes. Refusing only a change that stales one is not
    enough: two such scopes, once both pinned, would make every later
    change of the shared content stale one of them. So an entry's scope
    may share content with a pin in force only by reaching each of its
    paths, which widens it or repeats it.

    Parameters
    ----------
    history : list[Transaction]
        The entries already in the ledger file.
    chained : Transaction
        The new entry, with a scope.

    Returns
    -------
    list[str]
        A reason for each pin in force (``transactions.pins_in_force``)
        that names a path of the entry's scope, or a directory above or
        below one, and some path of which the entry's scope does not
        reach.
    """
    scope = scope_key(chained)
    reasons: list[str] = []
    for old in pins_in_force(history):
        paths = scope_key(old)
        shares = any(
            covers(a, b) or covers(b, a) for a in paths for b in scope
        )
        if shares and not all(reaches(scope, p) for p in paths):
            reasons.append(
                f"entry {old.get('seq')} pins the scope {', '.join(paths)}, "
                "which shares content with this one: record the change "
                "with a scope that reaches each of its paths"
            )
    return reasons
