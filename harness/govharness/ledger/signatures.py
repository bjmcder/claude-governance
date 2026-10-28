"""Verify the signatures of a ledger against the signer register.

A signature is an armored OpenPGP detached signature over the entry
digest: the entry hash computed with an empty ``signature`` field. The
digest covers the entry's sequence number, the hash of the entry before
it, and, outside the governance ledger, the ``ledger`` identifier, so a
signature cannot be replayed onto another entry or another ledger. The
entry's own ``hash`` then covers the signature.

A key's window and a required signature compare the ``seq`` an entry
claims, so they hold only for a ledger whose sequence numbers equal the
positions of its entries. The callers (``verify`` and ``sign check``)
therefore check the chain, ``transactions.chain_problems``, as well.

Each transaction of the governance ledger whose scope names the register
lists, in its field ``signers``, the open fingerprints after the change.
The founding transaction is signed by the anchor key, every later one by
a key the previous one lists, and the register agrees with the last
list.
"""

from __future__ import annotations

import unicodedata

from govharness.ledger.gpg import SignerConfig, signing_fingerprint
from govharness.ledger.register import (
    REGISTER_ID,
    SignerRegister,
    active_signers,
    applies,
)
from govharness.ledger.transactions import (
    GOVERNANCE,
    Transaction,
    entry_digest,
    ledger_of,
)


def normalize(label: str) -> str:
    """Return a label folded for comparison of look-alike spellings.

    Parameters
    ----------
    label : str
        Role label or actor.

    Returns
    -------
    str
        NFKC-normalized, stripped, case-folded text.
    """
    return unicodedata.normalize("NFKC", label).strip().casefold()


def _valid_for(
    register: SignerRegister, fpr: str, entry: Transaction, ledger: str
) -> bool:
    """Return True when a key may sign this entry of this ledger.

    Parameters
    ----------
    register : SignerRegister
        The signer register.
    fpr : str
        Fingerprint that made the signature.
    entry : Transaction
        The signed entry.
    ledger : str
        Ledger the entry belongs to.

    Returns
    -------
    bool
        Whether a row of that ledger grants that key this actor and
        entry, as the term Accepted signature of STND.HARN reads.
    """
    return any(
        row["Fingerprint"] == fpr
        and row["Ledger"] == ledger
        and row["Role label"] == entry.get("actor")
        and (
            row["Last entry"] == "none"
            or int(entry.get("seq", 0)) <= int(row["Last entry"])
        )
        for row in register.signers
    )


def required_of(
    register: SignerRegister, entry: Transaction, ledger: str
) -> list[str]:
    """Return the requirements that oblige an entry to be signed.

    Parameters
    ----------
    register : SignerRegister
        The signer register.
    entry : Transaction
        The entry, with its ``seq`` and ``actor``.
    ledger : str
        Ledger the entry belongs to.

    Returns
    -------
    list[str]
        The ``From entry`` of each well-formed row that requires the
        entry's actor to sign it.
    """
    return [
        row["From entry"]
        for row in register.required
        if applies(row, ledger)
        and row.get("Actor") == entry.get("actor")
        and row.get("From entry", "").isdigit()
        and int(entry.get("seq") or 0) >= int(row["From entry"])
    ]


def _spoofed(register: SignerRegister, actor: str) -> bool:
    """Return True when an actor imitates a registered label.

    Parameters
    ----------
    register : SignerRegister
        The signer register.
    actor : str
        Actor of an entry.

    Returns
    -------
    bool
        Whether the actor differs from every label but folds to one.
    """
    labels = {r["Role label"] for r in register.signers}
    labels |= {r["Actor"] for r in register.required}
    return actor not in labels and normalize(actor) in {
        normalize(label) for label in labels
    }


def check_signatures(
    entries: list[Transaction],
    register: SignerRegister | None,
    ledger: str,
    config: SignerConfig,
) -> list[str]:
    """Return the signature failures of one ledger.

    Parameters
    ----------
    entries : list[Transaction]
        Ledger entries in order.
    register : SignerRegister | None
        The signer register; ``None`` when the corpus has none.
    ledger : str
        Identifier the entries must carry.
    config : SignerConfig
        Anchor and ``gpg`` path, read by the caller (``gpg.read_config``)
        or given by a test.

    Returns
    -------
    list[str]
        One line per failure, sorted, without repeats.
    """
    if register is None:
        signed = [e.get("seq") for e in entries if e.get("signature")]
        if signed:
            return [f"- seq {signed}: signed, but no signer register"]
        return []
    if register.problems:
        return sorted(register.problems)
    failures: list[str] = []
    listed: list[str] | None = None
    for entry in entries:
        found, fpr = _entry_failures(register, entry, ledger, config)
        failures += found
        scope = entry.get("scope") or []
        if ledger != GOVERNANCE or REGISTER_ID not in scope:
            continue
        failures += _register_change(entry.get("seq"), fpr, listed, config)
        listed = list(entry.get("signers") or [])
    if ledger == GOVERNANCE and listed is None:
        failures.append(f"- {REGISTER_ID} is not founded by a transaction")
    elif ledger == GOVERNANCE and sorted(listed) != active_signers(register):
        failures.append(
            f"- the open signers of {REGISTER_ID} differ from those its "
            "last transaction lists"
        )
    return sorted(set(failures))


def _entry_failures(
    register: SignerRegister,
    entry: Transaction,
    ledger: str,
    config: SignerConfig,
) -> tuple[list[str], str | None]:
    """Check one entry's ledger, actor, signature, and required signer.

    Parameters
    ----------
    register : SignerRegister
        The signer register, free of problems.
    entry : Transaction
        The entry.
    ledger : str
        Identifier the entry must carry.
    config : SignerConfig
        Anchor and ``gpg`` path.

    Returns
    -------
    tuple[list[str], str | None]
        Failure lines, and the fingerprint of a key that verifiably
        signed the entry and may sign it here, or ``None``.
    """
    failures: list[str] = []
    seq, actor = entry.get("seq"), str(entry.get("actor", ""))
    if ledger_of(entry) != ledger:
        failures.append(f"- seq {seq}: belongs to {ledger_of(entry)}")
    if not actor.isascii() or _spoofed(register, actor):
        failures.append(f"- seq {seq}: actor `{actor}` imitates a label")
    fpr = signing_fingerprint(
        entry_digest(entry),
        entry.get("signature", ""),
        register.keys,
        config.gpg,
    )
    if entry.get("signature") and fpr is None:
        failures.append(f"- seq {seq}: signature does not verify")
    elif fpr and not _valid_for(register, fpr, entry, ledger):
        failures.append(
            f"- seq {seq}: key {fpr} may not sign for `{actor}` here"
        )
        fpr = None
    if fpr is None:
        failures += [
            f"- seq {seq}: `{actor}` must sign from entry {start}"
            for start in required_of(register, entry, ledger)
        ]
    return failures, fpr


def _register_change(
    seq: object,
    fpr: str | None,
    listed: list[str] | None,
    config: SignerConfig,
) -> list[str]:
    """Check who signed a transaction that changes the signer register.

    Parameters
    ----------
    seq : object
        Sequence number of the transaction, for the message.
    fpr : str | None
        Key that verifiably signed it, or ``None``.
    listed : list[str] | None
        Open signers the previous register transaction listed; ``None``
        when this transaction founds the register.
    config : SignerConfig
        Holds the anchor key that must found the register.

    Returns
    -------
    list[str]
        A line when the founding is not signed by the anchor, or a
        later change by no key listed before it.
    """
    if listed is None:
        if config.anchor is None or fpr != config.anchor:
            return [
                f"- seq {seq}: {REGISTER_ID} is not founded by the "
                "anchor key of the signer configuration"
            ]
        return []
    if fpr is None or fpr not in listed:
        return [
            f"- seq {seq}: changes {REGISTER_ID} without the signature "
            "of a signer listed before the change"
        ]
    return []
