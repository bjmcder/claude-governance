"""The commands that append to or check a ledger, and the signer register.

``ledger append`` appends one transaction to a ledger file whose
directory exists; it makes no directory. Only a human owner or the
custodians sign adoption-type transactions. Any transaction's scope may
name a subpath such as ``STND/DRAFT``, or a Markdown file such as
``README.md`` (STND.HARN.7); a scope that names neither, or leaves the
corpus, is refused. A ``review`` transaction
records an independent review (QA.7) and is not a revision. An
``annotate`` transaction adds facts about earlier transactions, because
an entry is never edited. ``ledger check`` reads a ledger file, such
as a project's work ledger, and reports each break of its form, fields,
and chain; it writes nothing and needs no signer register.

``sign`` founds the signer register, adds, closes, or requires signers,
and checks the signatures of a ledger.

``rehearse`` runs an amendment script on a fresh copy of the corpus,
prints the entries it appended and the verification of the copy, and
confirms that the source corpus is unchanged.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from govharness.cli.reports import summary_lines
from govharness.core.corpus import (
    corpus_hash,
    is_scope_path,
    read_optional_text,
)
from govharness.core.entry import DOC_FILE, LEDGER_FILE
from govharness.core.hashing import canonical_json
from govharness.ledger.chain import append, check_ledger_file
from govharness.ledger.gpg import read_config
from govharness.ledger.register import read_register
from govharness.ledger.signatures import check_signatures
from govharness.ledger.transactions import (
    ALL_LEDGERS,
    GOVERNANCE,
    REGISTER_ID,
    Transaction,
    head_problems,
)
from govharness.workflows.rehearse import SourceChanged, rehearse
from govharness.workflows.signers import (
    add_signer,
    close_signer,
    found_register,
    require_signature,
)


def _split(text: str) -> list[str]:
    """Split a comma-separated option into its non-empty items.

    Parameters
    ----------
    text : str
        Option value.

    Returns
    -------
    list[str]
        The items, in order.
    """
    return [item for item in text.split(",") if item]


def run_append(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> int:
    """Run ``ledger append``: chain and append one transaction.

    Parameters
    ----------
    args : argparse.Namespace
        The transaction's fields and the signing options.
    parser : argparse.ArgumentParser
        Parser that reports a usage error.

    Returns
    -------
    int
        0 after printing the entry as written; 1 when the ledger
        refuses it, such as when its chain is broken.
    """
    if args.ledger_file is not None and args.ledger_id in {
        GOVERNANCE,
        ALL_LEDGERS,
    }:
        parser.error("a work ledger needs its own --ledger-id")
    if args.ledger_file is not None and not args.ledger_file.parent.is_dir():
        parser.error(
            f"--ledger-file {args.ledger_file}: no directory "
            f"{args.ledger_file.parent}; make it first"
        )
    scope = _split(args.scope)
    missing = [s for s in scope if not is_scope_path(args.root, s)]
    if missing:
        parser.error(
            "scope names no directory or Markdown file: "
            + ", ".join(missing)
        )
    try:
        written = _append_entry(args, scope)
    except ValueError as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 1
    print(canonical_json(written))
    return 0


def _append_entry(args: argparse.Namespace, scope: list[str]) -> Transaction:
    """Append the transaction that the arguments describe.

    Parameters
    ----------
    args : argparse.Namespace
        The transaction's fields and the signing options.
    scope : list[str]
        Scope paths, each a directory of the corpus.

    Returns
    -------
    Transaction
        The entry as written.

    Raises
    ------
    ValueError
        If the ledger refuses the entry.
    """
    return append(
        args.root,
        {
            "at": args.at,
            "type": args.type,
            "actor": args.actor,
            "role": args.role,
            "authority": _split(args.authority),
            "targets": _split(args.targets),
            "scope": scope,
            "corpus_hash": corpus_hash(args.root, scope) if scope else None,
            "rationale": args.rationale,
            "signature": "",
        },
        signer=(args.sign, args.gnupg_home) if args.sign else None,
        path=args.ledger_file,
        ledger=args.ledger_id,
    )


def _check_signatures(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> int:
    """Run ``sign check``: verify a ledger's signatures.

    Parameters
    ----------
    args : argparse.Namespace
        ``ledger``, ``ledger_id``, ``corpus``, and ``signer_config``.
    parser : argparse.ArgumentParser
        Parser that reports a usage error.

    Returns
    -------
    int
        1 when a ledger is broken (the form of a line, the fields of an
        entry, sequence numbers, links, or hashes), the corpus ledger
        lacks the head that the signer configuration pins, a signature
        fails, or the corpus has no signer register; else 0.
    """
    corpus_ledger = (args.corpus / LEDGER_FILE).resolve()
    if (
        args.ledger_id in {GOVERNANCE, ALL_LEDGERS}
        and args.ledger.resolve() != corpus_ledger
    ):
        parser.error("a work ledger needs its own --ledger-id")
    config = read_config(args.signer_config)
    text = read_optional_text(args.corpus / REGISTER_ID / DOC_FILE)
    if text is None:
        # Nothing can be verified without the register; fail closed.
        print(f"- no signer register {REGISTER_ID}/{DOC_FILE} in the corpus")
        return 1
    register = read_register(text, config.gpg)
    corpus_entries, broken = (
        check_ledger_file(corpus_ledger, GOVERNANCE)
        if corpus_ledger.exists()
        else ([], [])
    )
    failures = [f"- {line}" for line in broken]
    if config.ignored is not None:
        failures.append(
            f"- the signer configuration {config.ignored} can be altered "
            "by this account, so its anchor and head pin are ignored"
        )
    failures += [
        f"- {line}" for line in head_problems(corpus_entries, config.head)
    ]
    failures += check_signatures(corpus_entries, register, GOVERNANCE, config)
    if args.ledger_id != GOVERNANCE:
        entries, broken = check_ledger_file(args.ledger, args.ledger_id)
        failures += [f"- {args.ledger_id}: {line}" for line in broken]
        failures += check_signatures(
            entries, register, args.ledger_id, config
        )
    print("\n".join(failures) or "signatures: PASS")
    return 1 if failures else 0


def run_check_ledger(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> int:
    """Run ``ledger check``: report each break of a ledger file.

    Parameters
    ----------
    args : argparse.Namespace
        ``ledger``, the file, and ``ledger_id``, or ``None`` for the
        ledger of its first entry.
    parser : argparse.ArgumentParser
        Parser that reports a usage error.

    Returns
    -------
    int
        0 when the file passes; 1 when a line is not in the form of
        STND.HARN.6, an entry does not hold exactly the fields of
        STND.HARN.7 or belongs to another ledger, or the chain is
        broken; 2 when the file does not exist or cannot be read.
    """
    try:
        entries, problems = check_ledger_file(args.ledger, args.ledger_id)
    except FileNotFoundError:
        parser.error(f"{args.ledger}: no such file")
    except ValueError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    if problems:
        print("\n".join(f"- {line}" for line in problems))
        return 1
    print(f"ledger: PASS ({len(entries)} entries)")
    return 0


def run_sign(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Run one ``sign`` subcommand.

    Parameters
    ----------
    args : argparse.Namespace
        ``sign_command`` and its options.
    parser : argparse.ArgumentParser
        Parser that reports a usage error.

    Returns
    -------
    int
        The exit code.
    """
    if args.sign_command == "check":
        return _check_signatures(args, parser)
    key: Path | None = getattr(args, "key_file", None)
    armored = key.read_text(encoding="utf-8") if key else ""
    if args.sign_command == "found":
        path = found_register(args.root, args.date)
        print(add_signer(path, GOVERNANCE, args.role, args.name, armored))
    elif args.sign_command == "add-signer":
        print(
            add_signer(
                args.register, args.ledger, args.role, args.name, armored
            )
        )
    elif args.sign_command == "close-signer":
        close_signer(
            args.register, args.ledger, args.fingerprint, args.last_entry
        )
    elif args.sign_command == "require":
        require_signature(
            args.register, args.ledger, args.actor, args.from_entry
        )
    return 0


def run_rehearse(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> int:
    """Run ``rehearse``: an amendment script on a copy of the corpus.

    Parameters
    ----------
    args : argparse.Namespace
        ``root`` and ``script``.
    parser : argparse.ArgumentParser
        Parser that reports a usage error.

    Returns
    -------
    int
        0 when the copy verifies and the source is unchanged; 1 when
        the copy fails a check, the source changed, or the script is
        refused (it defines no ``apply``, or a primitive refuses an
        edit).
    """
    try:
        done = rehearse(args.root, args.script)
    except SourceChanged as changed:
        print(f"FAIL: {changed}", file=sys.stderr)
        return 1
    except ValueError as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 1
    print(f"copy: {done.copy}")
    print(f"appended: {len(done.appended)}")
    for entry in done.appended:
        print(f"  {canonical_json(entry)}")
    print("\n".join(summary_lines(done.verification)))
    print(f"source unchanged: {done.source_paths} files and directories")
    return 0 if done.verification.passed() else 1
