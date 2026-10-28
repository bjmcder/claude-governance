"""The signer register ``SIGNR``: its tables, keys, and text edits.

The register (``SIGNR/_doc.md``) holds a signer table
``Ledger | Role label | Name | Fingerprint | Last entry``, a table
``Ledger | Actor | From entry`` of required signatures, and the armored
public key of each signer under a heading ``### <FPR>``. A ledger is
``governance`` or the identifier of a work ledger; a required
signature may also name ``all``, from entry 1. A key verifies an entry
only for the ledger of its row, its role label, and sequence numbers up
to its last entry (``none`` while open). A signer row names one ledger
(STND.HARN.10), since each ledger numbers its own entries and a row for
``all`` could never be closed; a key that signs on several ledgers has
a row for each.

The edit functions here return new register text; writing it is the
caller's effect.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from govharness.core.tables import read_table
from govharness.ledger.gpg import DEFAULT_GPG, key_fingerprint
from govharness.ledger.transactions import ALL_LEDGERS, GOVERNANCE

REGISTER_ID = "SIGNR"
SIGNER_HEADER = ("Ledger", "Role label", "Name", "Fingerprint", "Last entry")
REQUIRE_HEADER = ("Ledger", "Actor", "From entry")
FINGERPRINT_RE = re.compile(r"^[0-9A-F]{40}$")
KEY_RE = re.compile(
    r"^### ([0-9A-F]{40})\s*\n+```\n(-----BEGIN PGP PUBLIC KEY BLOCK-----"
    r".*?-----END PGP PUBLIC KEY BLOCK-----)\n```",
    re.MULTILINE | re.DOTALL,
)
SKELETON = """---
id: "SIGNR"
level: null
kind: "register"
title: "Signer register"
status: "adopted"
adopted: "{date}"
---

The keys whose signatures on ledger entries the harness verifies (GOV.36).

## Signers

| Ledger | Role label | Name | Fingerprint | Last entry |
| --- | --- | --- | --- | --- |

## Required signatures

| Ledger | Actor | From entry |
| --- | --- | --- |

## Keys
"""


@dataclass
class SignerRegister:
    """Parsed signer register.

    Parameters
    ----------
    signers : list[dict[str, str]]
        Rows of the signer table.
    required : list[dict[str, str]]
        Rows of the required-signature table.
    keys : dict[str, str]
        Armored public key by fingerprint.
    problems : list[str]
        Malformed rows or keys.
    """

    signers: list[dict[str, str]] = field(default_factory=list)
    required: list[dict[str, str]] = field(default_factory=list)
    keys: dict[str, str] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)


def read_register(text: str, gpg: str = DEFAULT_GPG) -> SignerRegister:
    """Parse the text of a signer register.

    Parameters
    ----------
    text : str
        Markdown text of the register.
    gpg : str
        Absolute path of the ``gpg`` binary, used to check each key.

    Returns
    -------
    SignerRegister
        Its tables, keys, and problems.
    """
    register = SignerRegister(
        signers=read_table(text, SIGNER_HEADER),
        required=read_table(text, REQUIRE_HEADER),
        keys={m[1]: m[2] + "\n" for m in KEY_RE.finditer(text)},
    )
    for heading, armored in register.keys.items():
        if key_fingerprint(armored, gpg) != heading:
            register.problems.append(f"- key under `{heading}` is not it")
    for row in register.signers:
        fpr, last = row.get("Fingerprint", ""), row.get("Last entry", "")
        if not FINGERPRINT_RE.match(fpr):
            register.problems.append(f"- fingerprint `{fpr}` is malformed")
        elif fpr not in register.keys:
            register.problems.append(f"- no public key for `{fpr}`")
        if last != "none" and not last.isdigit():
            register.problems.append(f"- `{fpr}`: last entry `{last}`")
    for row in register.required:
        if not row.get("From entry", "").isdigit():
            register.problems.append(f"- requirement `{row}` is malformed")
        if row.get("Ledger") == ALL_LEDGERS and row.get("From entry") != "1":
            register.problems.append(f"- `{row}`: an `all` row starts at 1")
    for row in register.signers:
        if row.get("Ledger", "").casefold() == ALL_LEDGERS:
            register.problems.append(
                f"- `{row}`: a signer row names one ledger (STND.HARN.10)"
            )
    return register


def applies(row: dict[str, str], ledger: str) -> bool:
    """Return True when a row of required signatures applies to a ledger.

    Parameters
    ----------
    row : dict[str, str]
        Row of the required-signature table.
    ledger : str
        Ledger identifier.

    Returns
    -------
    bool
        Whether the row names that ledger or ``all``.
    """
    return row.get("Ledger") in {ledger, ALL_LEDGERS}


def active_signers(register: SignerRegister) -> list[str]:
    """Return the sorted fingerprints left open on the governance ledger.

    Parameters
    ----------
    register : SignerRegister
        The signer register.

    Returns
    -------
    list[str]
        Fingerprints whose last entry is ``none``.
    """
    return sorted(
        row["Fingerprint"]
        for row in register.signers
        if row.get("Last entry") == "none" and row.get("Ledger") == GOVERNANCE
    )


def append_row(text: str, header: tuple[str, ...], row: str) -> str:
    """Insert a row after the last row of the table with a header.

    Parameters
    ----------
    text : str
        Register text.
    header : tuple[str, ...]
        Column headings of the table.
    row : str
        Markdown row to insert.

    Returns
    -------
    str
        The new text.

    Raises
    ------
    ValueError
        If the text holds no table with that header.
    """
    lines = text.split("\n")
    start = lines.index("| " + " | ".join(header) + " |")
    end = start + 2
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    lines.insert(end, row)
    return "\n".join(lines)


def skeleton(date: str) -> str:
    """Return the text of an empty register adopted on a date.

    Parameters
    ----------
    date : str
        Adoption date, ``YYYY-MM-DD``.

    Returns
    -------
    str
        Register text with empty tables.
    """
    return SKELETON.format(date=date)


def _refuse_all(ledger: str) -> None:
    """Refuse a signer row for the ledger ``all``.

    Parameters
    ----------
    ledger : str
        Ledger of the row.

    Raises
    ------
    ValueError
        If the ledger is ``all``, in any case.
    """
    if ledger.casefold() == ALL_LEDGERS:
        raise ValueError(
            "a signer row names one ledger (STND.HARN.10); add a row for "
            "each ledger the key signs"
        )


def with_signer(
    text: str, ledger: str, role: str, name: str, armored: str, fpr: str
) -> str:
    """Return register text with a signer row and its public key added.

    The key is added once: a key already under its heading is kept,
    and must be the armor given.

    Parameters
    ----------
    text : str
        Register text.
    ledger : str
        Ledger the key signs for: ``governance`` or a work ledger.
    role : str
        Role label the key signs as.
    name : str
        Name of the person who holds the key.
    armored : str
        Armored public key.
    fpr : str
        The key's fingerprint.

    Returns
    -------
    str
        The new text.

    Raises
    ------
    ValueError
        If the ledger is ``all``, in any case: a signer row names one
        ledger (STND.HARN.10); or the register holds the key under its
        heading with another armor.
    """
    _refuse_all(ledger)
    kept = [m[2] for m in KEY_RE.finditer(text) if m[1] == fpr]
    if kept and kept[0].strip() != armored.strip():
        raise ValueError(f"the register holds {fpr} with another armor")
    row = f"| {ledger} | {role} | {name} | {fpr} | none |"
    text = append_row(text, SIGNER_HEADER, row)
    if kept:
        return text
    block = f"\n### {fpr}\n\n```\n{armored.strip()}\n```\n"
    return text.rstrip("\n") + "\n" + block


def with_signer_closed(
    text: str, ledger: str, fingerprint: str, last_entry: int
) -> str:
    """Return register text with the open rows of a key on a ledger closed.

    Each open row of that ledger and key is closed, whatever its role
    label.

    Parameters
    ----------
    text : str
        Register text.
    ledger : str
        Ledger of the row to close.
    fingerprint : str
        Fingerprint of the key.
    last_entry : int
        Last sequence number the key may sign.

    Returns
    -------
    str
        The new text.

    Raises
    ------
    ValueError
        If the ledger is ``all``, in any case (STND.HARN.10), or no open
        row of that ledger names the key.
    """
    _refuse_all(ledger)
    cell = r"\|[^|\n]*"
    pattern = (
        rf"^(\| {re.escape(ledger)} {cell}{cell}"
        rf"\| {re.escape(fingerprint)} \| )none( \|)$"
    )
    new, count = re.subn(
        pattern, rf"\g<1>{last_entry}\g<2>", text, flags=re.MULTILINE
    )
    if count == 0:
        raise ValueError(f"no open row for {fingerprint}")
    return new


def with_requirement(
    text: str, ledger: str, actor: str, from_entry: int
) -> str:
    """Return register text that requires an actor's signature.

    Parameters
    ----------
    text : str
        Register text.
    ledger : str
        Ledger the requirement applies to.
    actor : str
        Role label of the actor.
    from_entry : int
        First sequence number the requirement covers.

    Returns
    -------
    str
        The new text.
    """
    row = f"| {ledger} | {actor} | {from_entry} |"
    return append_row(text, REQUIRE_HEADER, row)
