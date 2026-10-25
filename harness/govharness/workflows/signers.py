"""Found the signer register and change its rows.

Every change here edits the register file only. The ledger transaction
that pins the change is a separate step (``ledger append`` with the
scope ``SIGNR``), signed by a key the register listed before it.
"""

from __future__ import annotations

from pathlib import Path

from govharness.core.corpus import read_text
from govharness.core.entry import DOC_FILE
from govharness.ledger.gpg import key_fingerprint
from govharness.ledger.register import (
    FINGERPRINT_RE,
    REGISTER_ID,
    skeleton,
    with_requirement,
    with_signer,
    with_signer_closed,
)


def found_register(root: Path, date: str) -> Path:
    """Write an empty signer register into a corpus.

    Parameters
    ----------
    root : Path
        Corpus root.
    date : str
        Adoption date, ``YYYY-MM-DD``.

    Returns
    -------
    Path
        The register file.

    Raises
    ------
    FileExistsError
        If the register already exists.
    """
    path = root / REGISTER_ID / DOC_FILE
    path.parent.mkdir()
    path.write_text(skeleton(date), encoding="utf-8")
    return path


def add_signer(
    path: Path, ledger: str, role: str, name: str, armored: str
) -> str:
    """Add a signer row and its public key to a register file.

    Parameters
    ----------
    path : Path
        Register file.
    ledger : str
        Ledger the key signs for: ``governance``, a work ledger, or
        ``all``.
    role : str
        Role label the key signs as.
    name : str
        Name of the person who holds the key.
    armored : str
        Armored public key.

    Returns
    -------
    str
        The key's fingerprint.

    Raises
    ------
    ValueError
        If the text holds no public key, or an ``all`` row of the key
        conflicts with the row (``register.with_signer``).
    """
    fpr = key_fingerprint(armored.strip())
    if fpr is None:
        raise ValueError("the key text holds no public key")
    text = with_signer(read_text(path), ledger, role, name, armored, fpr)
    path.write_text(text, encoding="utf-8")
    return fpr


def close_signer(
    path: Path, ledger: str, fingerprint: str, last_entry: int
) -> None:
    """Set the last entry of one ledger that a key may sign.

    Parameters
    ----------
    path : Path
        Register file.
    ledger : str
        Ledger of the row to close; an ``all`` row stays open
        (STND.HARN.10) and cannot be closed.
    fingerprint : str
        Fingerprint of the key.
    last_entry : int
        Last sequence number the key may sign.

    Raises
    ------
    ValueError
        If the fingerprint is malformed or names no open row, or the
        row cannot be closed beside an ``all`` row
        (``register.with_signer_closed``).
    """
    if not FINGERPRINT_RE.match(fingerprint):
        raise ValueError(f"malformed fingerprint {fingerprint!r}")
    text = with_signer_closed(read_text(path), ledger, fingerprint, last_entry)
    path.write_text(text, encoding="utf-8")


def require_signature(
    path: Path, ledger: str, actor: str, from_entry: int
) -> None:
    """Require every entry of an actor from a sequence number to be signed.

    Parameters
    ----------
    path : Path
        Register file.
    ledger : str
        Ledger the requirement applies to.
    actor : str
        Role label of the actor.
    from_entry : int
        First sequence number the requirement covers.
    """
    text = with_requirement(read_text(path), ledger, actor, from_entry)
    path.write_text(text, encoding="utf-8")
