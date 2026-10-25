"""The signer register ``SIGNR``: its tables, keys, and text edits.

The register (``SIGNR/_doc.md``) holds a signer table
``Ledger | Role label | Name | Fingerprint | Last entry``, a table
``Ledger | Actor | From entry`` of required signatures, and the armored
public key of each signer under a heading ``### <FPR>``. A ledger is
``governance``, the identifier of a work ledger, or ``all``. A key
verifies an entry only for its ledger, its role label, and sequence
numbers up to its last entry (``none`` while open). A row for the
ledger ``all`` requires signatures from entry 1. A signer row for
``all`` stays open (STND.HARN.10), and while it is open it accepts the
key on every ledger, whatever row of one ledger names the same key and
role label (the term Accepted signature of STND.HARN). Such a key
cannot be closed, so ``with_signer`` and ``with_signer_closed`` refuse
a row that would seem to close it; a key meant to be closable is
registered per ledger.

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
        if (
            row.get("Ledger") == ALL_LEDGERS
            and row.get("Last entry") != "none"
        ):
            register.problems.append(
                f"- `{row}`: close an `all` key per ledger"
            )
    return register


def applies(row: dict[str, str], ledger: str) -> bool:
    """Return True when a register row applies to a ledger.

    Parameters
    ----------
    row : dict[str, str]
        Row of either register table.
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
        if row.get("Last entry") == "none" and applies(row, GOVERNANCE)
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


def _refuse_beside_all_row(
    text: str, ledger: str, fpr: str, roles: set[str]
) -> None:
    """Refuse a signer row that an ``all`` row of its key would override.

    Parameters
    ----------
    text : str
        Register text.
    ledger : str
        Ledger of the row to add or close.
    fpr : str
        Fingerprint of the key.
    roles : set[str]
        Role labels of the row.

    Raises
    ------
    ValueError
        If the row is for one ledger and an open ``all`` row names the
        same key and a role label of the row, or the row is for ``all``
        and a row of one ledger names them.
    """
    for row in read_table(text, SIGNER_HEADER):
        if row.get("Fingerprint") != fpr or row.get("Role label") not in roles:
            continue
        if ledger == ALL_LEDGERS and row.get("Ledger") != ALL_LEDGERS:
            raise ValueError(
                f"{fpr} has a row for {row.get('Ledger')}; an `all` row for "
                "it would stay open (STND.HARN.10) and accept it there "
                "after that row is closed"
            )
        if (
            ledger != ALL_LEDGERS
            and row.get("Ledger") == ALL_LEDGERS
            and row.get("Last entry") == "none"
        ):
            raise ValueError(
                f"{fpr} signs as `{row.get('Role label')}` for all "
                "ledgers, and STND.HARN.10 keeps an `all` row open, so a "
                f"row for {ledger} cannot close it; register a key meant "
                "to be closable per ledger"
            )


def with_signer(
    text: str, ledger: str, role: str, name: str, armored: str, fpr: str
) -> str:
    """Return register text with a signer row and its public key added.

    Parameters
    ----------
    text : str
        Register text.
    ledger : str
        Ledger the key signs for: ``governance``, a work ledger, or
        ``all``.
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
        If an open ``all`` row names the key and role label of a row
        for one ledger, or a row for one ledger those of an ``all`` row
        (``_refuse_beside_all_row``).
    """
    _refuse_beside_all_row(text, ledger, fpr, {role})
    row = f"| {ledger} | {role} | {name} | {fpr} | none |"
    block = f"\n### {fpr}\n\n```\n{armored.strip()}\n```\n"
    return append_row(text, SIGNER_HEADER, row).rstrip("\n") + "\n" + block


def with_signer_closed(
    text: str, ledger: str, fingerprint: str, last_entry: int
) -> str:
    """Return register text with the open row of a key closed.

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
        If no open row of that ledger names the key, the ledger is
        ``all``, whose rows stay open (STND.HARN.10), or an open ``all``
        row names the key and the role label of the row
        (``_refuse_beside_all_row``).
    """
    if ledger == ALL_LEDGERS:
        raise ValueError(
            "STND.HARN.10 keeps an `all` row open; a key meant to be "
            "closable is registered per ledger"
        )
    _refuse_beside_all_row(
        text,
        ledger,
        fingerprint,
        {
            row.get("Role label", "")
            for row in read_table(text, SIGNER_HEADER)
            if row.get("Ledger") == ledger
            and row.get("Fingerprint") == fingerprint
            and row.get("Last entry") == "none"
        },
    )
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
