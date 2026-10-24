"""Structural check of ``verify``: the ledger chain, pins, and signatures.

The hash chain is intact, each entry's sequence number is its position,
and each transaction's pinned ``corpus_hash`` still matches its scope,
so an edit made outside the ledger is reported (GOV.36). A pin holds
until the next transaction of the same scope. Every signature verifies
against the signer register ``SIGNR`` where one exists, every entry the
register requires to be signed is signed, and every change to the
register after its founding is signed.

The check computes on the snapshot of the corpus and reads no file;
verifying a signature runs ``gpg`` through ``ledger/gpg.py``.
"""

from __future__ import annotations

from pathlib import PurePosixPath

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.core.corpus import Tree, has_directory, scope_hash
from govharness.core.entry import DOC_FILE
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.register import REGISTER_ID, read_register
from govharness.ledger.signatures import check_signatures
from govharness.ledger.transactions import (
    GOVERNANCE,
    Transaction,
    entry_problems,
)

FAMILY = "ledger"


def ledger_problems(
    tree: Tree, entries: list[Transaction], config: SignerConfig
) -> list[str]:
    """Return chain breaks, edits outside the ledger, and bad signatures.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus, whose files the pins are compared with
        and which holds the signer register, if there is one.
    entries : list[Transaction]
        The corpus ledger, in order.
    config : SignerConfig
        Signer anchor and ``gpg`` path.

    Returns
    -------
    list[str]
        One line per failure: for each entry its sequence, chain, and
        scope problems, then the signature failures, then the stale
        pins.
    """
    errors: list[str] = []
    previous = None
    latest_scope_hash: dict[tuple[str, ...], tuple[int, str]] = {}
    for position, entry in enumerate(entries, start=1):
        errors += entry_problems(entry, position, previous)
        previous = entry.get("hash")
        for path in entry.get("scope") or []:
            if not has_directory(tree, path):
                errors.append(
                    f"seq {entry.get('seq')}: scope {path} does not exist"
                )
        if entry.get("scope"):
            latest_scope_hash[tuple(sorted(entry["scope"]))] = (
                entry["seq"],
                entry["corpus_hash"],
            )
    register_file = PurePosixPath(REGISTER_ID, DOC_FILE)
    register = (
        read_register(tree.text(register_file), config.gpg)
        if register_file in tree.files
        else None
    )
    errors += check_signatures(entries, register, GOVERNANCE, config)
    for scope, (seq, pinned) in latest_scope_hash.items():
        if scope_hash(tree, list(scope)) != pinned:
            errors.append(
                f"content changed outside the ledger since seq {seq}: "
                f"{', '.join(scope)}"
            )
    return errors


def ledger_intact(ctx: CheckContext) -> Verdict:
    """Check ledger: chain, pins, and signatures hold.

    The signer configuration comes from the context; without one there
    is no anchor, so a signer register fails its founding check.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per failure.
    """
    config = ctx.signer_config or SignerConfig()
    problems = ledger_problems(ctx.require_tree(), ctx.ledger or [], config)
    return Verdict("FAIL" if problems else "PASS", problems)


CHECKS: tuple[Check, ...] = (
    Check(
        "ledger",
        FAMILY,
        "The ledger chain is intact, its pins hold, and its signatures verify",
        ("GOV.36",),
        ledger_intact,
    ),
)
