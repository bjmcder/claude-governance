"""The ``environment`` command: derive or check an agent's environment.

``environment ROOT --work PATH --home PATH --write OUT`` renders the
Claude Code configuration of STND.HARN.18 into ``OUT``, with its
coverage report and draft entry. ``--check`` compares the files
installed under ``/`` with a fresh rendering and reports each one that
is missing, differs, or is alterable by the running account
(STND.HARN.21). Each ``--authorization ID`` names an authorization of
the corpus whose remote writes the guard lets proceed without referral
while it is in force (STND.HARN.29); one that is not in force is an
error.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from govharness.checks.ledger import ledger_problems
from govharness.cli.arguments import corpus_root
from govharness.cli.derived import write_files
from govharness.core.corpus import (
    Corpus,
    Tree,
    load_entries,
    read_text,
    read_tree,
)
from govharness.derive.environment import claude_code
from govharness.derive.environment.authorizations import (
    Reading,
    read_authorizations,
)
from govharness.derive.environment.inputs import Inputs, RemoteWrite
from govharness.ledger.chain import read_ledger
from govharness.ledger.gpg import read_config
from govharness.ledger.register import REGISTER_ID
from govharness.workflows.environment import installed_problems

# The guard is installed as a file, so the command reads its source and
# never imports it.
GUARD_SOURCE = Path(__file__).resolve().parents[1] / "hooks" / "guard.py"


def add_environment(sub: argparse._SubParsersAction) -> None:
    """Add the ``environment`` command.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    command = sub.add_parser(
        "environment", help="derive or check an agent's environment"
    )
    command.add_argument("root", type=corpus_root)
    command.add_argument("--work", type=Path, required=True)
    # The agent's home, which the owner may generate from another
    # account, so it has no default.
    command.add_argument("--home", type=Path, required=True)
    command.add_argument("--open", type=Path, action="append", default=[])
    command.add_argument("--domain", action="append", default=[])
    command.add_argument("--tool", action="append", default=[])
    command.add_argument("--search", action="store_true")
    command.add_argument("--unattended", action="store_true")
    command.add_argument(
        "--secret-store",
        action="store_true",
        help="the human owner provides the store of STND.DFLT.29",
    )
    command.add_argument(
        "--secret",
        action="append",
        default=[],
        metavar="NAME",
        help="a file of the store the agent is authorized to handle",
    )
    command.add_argument(
        "--authorization",
        action="append",
        default=[],
        metavar="ID",
        help="an authorization of remote writes that extends to the agent",
    )
    command.add_argument(
        "--role",
        default="",
        help="the role or agent the configuration is derived for (GUARD.12)",
    )
    command.add_argument(
        "--expiry-horizon",
        type=int,
        metavar="DAYS",
        help="refuse an authorization that expires later, or never",
    )
    command.add_argument(
        "--assured",
        action="store_true",
        help="the classification records the work as CSQ0 or CSQ1",
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path, metavar="OUT")
    mode.add_argument("--check", action="store_true")
    command.set_defaults(run=lambda a, _: run_environment(a))


def inputs_of(
    args: argparse.Namespace,
    remote_writes: tuple[RemoteWrite, ...] = (),
    referred: tuple[str, ...] = (),
) -> Inputs:
    """Build the owner's statement of the environment from arguments.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments of ``environment``.
    remote_writes : tuple[RemoteWrite, ...]
        Remote writes that the named authorizations open.
    referred : tuple[str, ...]
        Authorizations named whose writes stay referred.

    Returns
    -------
    Inputs
        Paths made absolute, so that the configuration names fixed
        locations.
    """
    return Inputs(
        work=str(args.work.resolve()),
        home=str(args.home.resolve()),
        open_paths=tuple(str(p.resolve()) for p in args.open),
        domains=tuple(args.domain),
        search=args.search,
        tools=tuple(args.tool),
        unattended=args.unattended,
        assured=args.assured,
        secret_store=args.secret_store,
        secrets=tuple(args.secret),
        remote_writes=remote_writes,
        referred=referred,
    )


def authorized(args: argparse.Namespace, tree: Tree) -> Reading:
    """Read the authorizations named by ``--authorization``.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments of ``environment``.
    tree : Tree
        Snapshot of the corpus at the root, read once with the corpus.

    Returns
    -------
    Reading
        The remote writes opened, the authorizations still referred, and
        a summary for the owner; all empty when none is named.

    Raises
    ------
    ValueError
        If a named authorization is not in force at this moment.
    """
    if not args.authorization:
        return Reading((), (), ())
    ledger = read_ledger(args.root)
    # A signature is required for assured work, and wherever a signer
    # register exists, since an unsigned entry is then the exception.
    signed = args.assured or any(
        p.parts[:1] == (REGISTER_ID,) for p in tree.files
    )
    verified = signed and not ledger_problems(tree, ledger, read_config())
    horizon = (
        None
        if args.expiry_horizon is None
        else timedelta(days=args.expiry_horizon)
    )
    return read_authorizations(
        Corpus(load_entries(tree)),
        tree,
        ledger,
        tuple(args.authorization),
        datetime.now(timezone.utc),
        args.role,
        signed,
        verified,
        horizon,
    )


def run_environment(args: argparse.Namespace) -> int:
    """Run ``environment``: write the configuration, or check it.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments of ``environment``.

    Returns
    -------
    int
        1 when the governance tables or the inputs cannot be read, or
        when checking finds a problem, else 0.
    """
    try:
        tree = read_tree(args.root)
        reading = authorized(args, tree)
        files = claude_code.render(
            Corpus(load_entries(tree)),
            inputs_of(args, reading.writes, reading.referred),
            read_text(GUARD_SOURCE),
        )
    except (LookupError, ValueError) as error:
        print(f"environment: {error}", file=sys.stderr)
        return 1
    # The owner compares what the ledger pins with what was granted.
    for line in reading.summary:
        print(f"authorization: {line}")
    if args.check:
        problems = installed_problems(files, Path("/"), claude_code.PROGRAMS)
        for problem in problems:
            print(problem)
        print(f"environment: {'FAIL' if problems else 'PASS'}")
        return 1 if problems else 0
    for rel in files:
        (args.write / rel).parent.mkdir(parents=True, exist_ok=True)
    write_files(args.write, files)
    print(f"written: {len(files)} files under {args.write}")
    return 0
