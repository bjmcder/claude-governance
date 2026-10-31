"""Structural check of ``verify``: the ledger chain, pins, and signatures.

The hash chain is intact, each entry's sequence number is its position,
each line is the canonical serialization of its entry (STND.HARN.6)
with exactly the fields of STND.HARN.7, and each transaction's pinned
``corpus_hash`` still matches its scope, so an edit made outside the
ledger is reported (GOV.36). A pin holds until a later transaction's
scope reaches each of its paths (STND.HARN.9,
``transactions.pins_in_force``). Every signature verifies
against the signer register ``SIGNR`` where one exists, every entry the
register requires to be signed is signed, and every change to the
register after its founding is signed.

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
from govharness.core.corpus import Tree, has_scope_path, scope_hash
from govharness.core.entry import DOC_FILE, LEDGER_FILE
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.register import read_register
from govharness.ledger.signatures import check_signatures
from govharness.ledger.transactions import (
    GOVERNANCE,
    REGISTER_ID,
    Transaction,
    entry_problems,
    field_problems,
    form_problems,
    head_problems,
    pins_in_force,
    reaches,
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
        pinned, the head pin, each line of the ledger file of the tree
        not in the form of STND.HARN.6, for each entry its sequence,
        chain, field, and scope problems, then the missing register,
        the signature failures, and the stale pins.
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
    ledger_file = PurePosixPath(LEDGER_FILE)
    if ledger_file in tree.files:
        # The bytes as stored: a carriage return before a line feed is
        # outside the form, though a text read would drop it.
        errors += form_problems(tree.files[ledger_file].decode("utf-8"))
    previous = None
    for position, entry in enumerate(entries, start=1):
        errors += entry_problems(entry, position, previous)
        errors += field_problems(entry)
        previous = entry.get("hash")
        seq = entry.get("seq")
        for path in entry.get("scope") or []:
            if not has_scope_path(tree, path):
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
    """Return a line for each pin in force the corpus no longer matches.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus.
    entries : list[Transaction]
        The corpus ledger, in order.

    Returns
    -------
    list[str]
        One line per pin in force (``transactions.pins_in_force``)
        whose ``corpus_hash`` differs from the scope's hash, or whose
        scope holds a file name that cannot be hashed.
    """
    errors: list[str] = []
    for entry in pins_in_force(entries):
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


def unpinned_files(ctx: CheckContext) -> Verdict:
    """Check unpinned: FAIL for each Markdown file that no scope reaches.

    STND.HARN.9 compares only the scopes that transactions name, so a
    file outside every scope could change with no transaction and the
    ledger check still pass; STND.HARN.31 makes such a file a FAIL. A
    directory none of whose Markdown files is reached is named once,
    with its count of files.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per unreached directory or file, else PASS.
    """
    scopes = tuple(
        s
        for entry in ctx.ledger or []
        for s in entry.get("scope") or []
        if isinstance(s, str)
    )
    files = ctx.require_tree().markdown()
    covered = [p for p in files if reaches(scopes, p.as_posix())]
    groups: dict[str, int] = {}
    for path in sorted(set(files) - set(covered)):
        name = path.as_posix()
        for depth in range(1, len(path.parts)):
            top = PurePosixPath(*path.parts[:depth])
            if not any(top in p.parents for p in covered):
                name = f"{top.as_posix()}/"
                break
        groups[name] = groups.get(name, 0) + 1
    lines = [
        f"- {name} ({count} file{'s' if count > 1 else ''})"
        if name.endswith("/")
        else f"- {name}"
        for name, count in sorted(groups.items())
    ]
    return Verdict("FAIL" if lines else "PASS", lines)


CHECKS: tuple[Check, ...] = (
    Check(
        "ledger",
        FAMILY,
        "The ledger chain is intact, its pins hold, and its signatures verify",
        ("GOV.36",),
        ledger_intact,
    ),
    Check(
        "unpinned",
        FAMILY,
        "Every Markdown file lies under a scope that a transaction names",
        ("STND.HARN.31",),
        unpinned_files,
    ),
)
