"""The ``govharness`` command line: one parser, one subcommand each.

Commands::

    show ROOT ID [--expand]               one item and its cross references
    find ROOT WORD... [--limit N] [--in-force]
                                          items holding the words, ranked
    context ROOT WORD... [--budget N] [--in-force]
                                          the governance on a topic
    pairs ROOT ID [--amends LVL0_ID ...]  provision pairs to review before a
                                          change (STND.HARN.28)
    verify [--no-logic] [--no-z3] [--no-cache] [--cache-dir DIR] ROOT
                                          every check; exit 1 on failure
    check ROOT [--out-dir DIR] [--no-z3] [--no-cache] [--cache-dir DIR]
                                          logic checks and their report
    manifests ROOT (--check | --write)    stale or regenerated manifests
    references ROOT (--check | --write ID ...)
                                          References tables (STND.DRAFT.34)
    ledger append ROOT --type ... --rationale ...
                                          append one ledger transaction
    sign {found,add-signer,close-signer,require,check} ...
                                          the signer register SIGNR
    compose ROOT (--check | --write)      reading copies in ROOT/../rendered
    rehearse ROOT SCRIPT                  run an amendment on a copy
    environment ROOT --work PATH (--write OUT | --check)
                                          an agent's environment (STND.HARN)
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from govharness.cli.arguments import corpus_root
from govharness.cli.derived import (
    run_compose,
    run_manifests,
    run_references,
)
from govharness.cli.environment import add_environment
from govharness.cli.query import add_query
from govharness.cli.records import run_append, run_rehearse, run_sign
from govharness.cli.reports import run_check, run_verify
from govharness.ledger.transactions import GOVERNANCE

Runner = Callable[[argparse.Namespace, argparse.ArgumentParser], int]


def _add_cache(command: argparse.ArgumentParser) -> None:
    """Add the options of the solve cache (unit 0011).

    Parameters
    ----------
    command : argparse.ArgumentParser
        Parser of ``verify`` or ``check``.
    """
    group = command.add_mutually_exclusive_group()
    group.add_argument(
        "--no-cache", action="store_true", help="solve every claim afresh"
    )
    group.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="directory of the solve cache, outside the corpus",
    )


def _add_verify(sub: argparse._SubParsersAction) -> None:
    """Add the ``verify`` and ``check`` commands.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    verify = sub.add_parser("verify", help="run every check")
    verify.add_argument("root", type=corpus_root)
    verify.add_argument("--no-logic", action="store_true")
    verify.add_argument("--no-z3", action="store_true")
    _add_cache(verify)
    verify.set_defaults(run=lambda a, _: run_verify(a))
    check = sub.add_parser("check", help="run the logic checks")
    check.add_argument("root", type=corpus_root)
    check.add_argument("--out-dir", type=Path, default=None)
    check.add_argument("--no-z3", action="store_true")
    _add_cache(check)
    check.set_defaults(run=lambda a, _: run_check(a))


def _add_derived(sub: argparse._SubParsersAction) -> None:
    """Add the ``manifests``, ``references``, and ``compose`` commands.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    manifests = sub.add_parser("manifests", help="check or write manifests")
    manifests.add_argument("root", type=corpus_root)
    mode = manifests.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    manifests.set_defaults(run=lambda a, _: run_manifests(a))
    references = sub.add_parser(
        "references", help="check or write References tables"
    )
    references.add_argument("root", type=corpus_root)
    group = references.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", nargs="+", metavar="ID")
    references.set_defaults(run=lambda a, _: run_references(a))
    compose = sub.add_parser(
        "compose", help="check or write the reading copies"
    )
    compose.add_argument("root", type=corpus_root)
    copies = compose.add_mutually_exclusive_group(required=True)
    copies.add_argument("--check", action="store_true")
    copies.add_argument("--write", action="store_true")
    compose.set_defaults(run=lambda a, _: run_compose(a))


def _add_ledger(sub: argparse._SubParsersAction) -> None:
    """Add the ``ledger append`` command.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    ledger = sub.add_parser("ledger", help="append to a ledger")
    actions = ledger.add_subparsers(dest="ledger_command", required=True)
    append = actions.add_parser("append", help="append one transaction")
    append.add_argument("root", type=corpus_root)
    append.add_argument("--type", required=True)
    append.add_argument("--actor", required=True)
    append.add_argument("--role", required=True)
    append.add_argument("--authority", default="")
    append.add_argument("--targets", default="")
    append.add_argument("--scope", default="")
    append.add_argument("--rationale", required=True)
    append.add_argument(
        "--at", default=datetime.now(UTC).isoformat(timespec="seconds")
    )
    append.add_argument("--sign", default=None)
    append.add_argument("--gnupg-home", type=Path, default=None)
    append.add_argument("--ledger-file", type=Path, default=None)
    append.add_argument("--ledger-id", default=GOVERNANCE)
    append.set_defaults(run=run_append, usage_parser=append)


def _add_sign(sub: argparse._SubParsersAction) -> None:
    """Add the ``sign`` command and its subcommands.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    sign = sub.add_parser("sign", help="the signer register SIGNR")
    actions = sign.add_subparsers(dest="sign_command", required=True)
    found = actions.add_parser("found")
    found.add_argument("root", type=corpus_root)
    found.add_argument("--date", required=True)
    add = actions.add_parser("add-signer")
    add.add_argument("register", type=Path)
    add.add_argument("--ledger", default=GOVERNANCE)
    for signer in (found, add):
        signer.add_argument("--role", required=True)
        signer.add_argument("--name", required=True)
        signer.add_argument("--key-file", type=Path, required=True)
    close = actions.add_parser("close-signer")
    close.add_argument("register", type=Path)
    close.add_argument("--ledger", required=True)
    close.add_argument("--fingerprint", required=True)
    close.add_argument("--last-entry", type=int, required=True)
    need = actions.add_parser("require")
    need.add_argument("register", type=Path)
    need.add_argument("--ledger", default=GOVERNANCE)
    need.add_argument("--actor", required=True)
    need.add_argument("--from-entry", type=int, required=True)
    check = actions.add_parser("check")
    check.add_argument("ledger", type=Path)
    check.add_argument("--ledger-id", required=True)
    check.add_argument("--corpus", type=corpus_root, required=True)
    check.add_argument("--signer-config", type=Path, default=None)
    sign.set_defaults(run=run_sign)
    check.set_defaults(usage_parser=check)


def _add_rehearse(sub: argparse._SubParsersAction) -> None:
    """Add the ``rehearse`` command.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    rehearsal = sub.add_parser(
        "rehearse", help="run an amendment script on a copy"
    )
    rehearsal.add_argument("root", type=corpus_root)
    rehearsal.add_argument("script", type=Path)
    rehearsal.set_defaults(run=run_rehearse)


def build_parser() -> argparse.ArgumentParser:
    """Build the parser with every subcommand.

    Returns
    -------
    argparse.ArgumentParser
        The ``govharness`` parser.
    """
    parser = argparse.ArgumentParser(
        prog="python -m govharness",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    add_query(sub)
    _add_verify(sub)
    _add_derived(sub)
    _add_ledger(sub)
    _add_sign(sub)
    _add_rehearse(sub)
    add_environment(sub)
    return parser


def main(argv: list[str]) -> int:
    """Parse the arguments and run one command.

    Parameters
    ----------
    argv : list[str]
        Arguments after the program name.

    Returns
    -------
    int
        The process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    run: Runner = args.run
    # A usage error names the subcommand whose options were wrong.
    return run(args, getattr(args, "usage_parser", parser))
