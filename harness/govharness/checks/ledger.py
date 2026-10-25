"""Structural check of ``verify``: the ledger chain, pins, and signatures.

The hash chain is intact, each entry's sequence number is its position,
and each transaction's pinned ``corpus_hash`` still matches its scope,
so an edit made outside the ledger is reported (GOV.36). A pin holds
until the next transaction of the same scope (STND.HARN.9,
``transactions.latest_pins``). Every signature verifies against the
signer register ``SIGNR`` where one exists, every entry the register
requires to be signed is signed, and every change to the register after
its founding is signed.

The signer configuration, which the agent cannot alter, is trusted over
the corpus: where it names an anchor, a corpus without ``SIGNR`` fails,
and where it pins the head of the ledger, a ledger without that entry
fails. A ledger that is missing or empty fails where the corpus holds
Markdown for a transaction to pin.

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
    head_problems,
    latest_pins,
    scope_key,
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
        One line per failure: a ledger missing where content is to be
        pinned, the head pin, for each entry its sequence, chain, and
        scope problems, then the missing register, the signature
        failures, and the stale pins.
    """
    errors: list[str] = []
    if not entries and tree.markdown():
        errors.append(
            "the ledger is missing or empty, but the corpus holds content "
            "for its transactions to pin"
        )
    if config.ignored is not None:
        errors.append(
            f"the signer configuration {config.ignored} can be altered by "
            "this account, so its anchor and head pin are ignored"
        )
    errors += head_problems(entries, config.head)
    previous = None
    for position, entry in enumerate(entries, start=1):
        errors += entry_problems(entry, position, previous)
        previous = entry.get("hash")
        seq = entry.get("seq")
        for path in entry.get("scope") or []:
            if not has_directory(tree, path):
                errors.append(f"seq {seq}: scope {path} does not exist")
        if entry.get("scope") and not isinstance(
            entry.get("corpus_hash"), str
        ):
            errors.append(f"seq {seq}: a scope with no corpus_hash")
    register_file = PurePosixPath(REGISTER_ID, DOC_FILE)
    register = (
        read_register(tree.text(register_file), config.gpg)
        if register_file in tree.files
        else None
    )
    if register is None and config.anchor is not None:
        errors.append(
            "the signer configuration names an anchor key, but the corpus "
            f"holds no {REGISTER_ID}"
        )
    errors += check_signatures(entries, register, GOVERNANCE, config)
    return errors + _stale_pins(tree, entries)


def _stale_pins(tree: Tree, entries: list[Transaction]) -> list[str]:
    """Return a line for each latest pin the corpus no longer matches.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus.
    entries : list[Transaction]
        The corpus ledger, in order.

    Returns
    -------
    list[str]
        One line per latest pin of a scope (``transactions.latest_pins``)
        whose ``corpus_hash`` differs from the scope's hash, or whose
        scope holds a file name that cannot be hashed.
    """
    errors: list[str] = []
    for entry in latest_pins(entries):
        scope = list(scope_key(entry))
        pinned = entry.get("corpus_hash")
        try:
            changed = isinstance(pinned, str) and (
                scope_hash(tree, scope) != pinned
            )
        except ValueError as refusal:
            errors.append(f"seq {entry.get('seq')}: {refusal}")
            continue
        if changed:
            errors.append(
                "content changed outside the ledger since seq "
                f"{entry.get('seq')}: {', '.join(scope)}"
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
