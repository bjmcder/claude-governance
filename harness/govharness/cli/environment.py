"""The ``environment`` command: derive or check an agent's environment.

``environment ROOT --work PATH --home PATH --write OUT`` renders the
Claude Code configuration of STND.HARN.18 into ``OUT``, with its
coverage report and draft entry. ``--check`` compares the files
installed under ``/`` with a fresh rendering and reports each one that
is missing, differs, or is alterable by the running account
(STND.HARN.21). Each ``--authorization ID`` names an authorization of
the corpus whose remote writes the guard lets proceed without referral
while it is in force (STND.HARN.29); one that is not in force is an
error. Where no signature is required, because the work is not assured
and no signer register exists, the derivation is refused unless the
owner passes ``--accept-unsigned``, and the summary then says that each
authorization was accepted unsigned. ``--expiry-horizon`` bounds the
time from the derivation to an authorization's expiry, 90 days unless
the owner gives another number of days; under a bound, one that lapses
only when revoked is refused, and ``--expiry-horizon none`` lifts the
bound (unit 0012). The summary names the horizon in force. INSTALL.md
prints the check with the corpus root and every option of the
derivation, so that, run as printed, it renders the same files (unit
0014).
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
    ACCEPT_UNSIGNED,
    DEFAULT_HORIZON,
    NO_HORIZON,
    REGISTER_REMOVED,
    Reading,
    ledger_shape,
    parse_horizon,
    read_authorizations,
    register_trace,
)
from govharness.derive.environment.inputs import Inputs, RemoteWrite
from govharness.ledger.chain import read_ledger
from govharness.ledger.gpg import read_config
from govharness.ledger.register import REGISTER_ID
from govharness.workflows.environment import installed_problems

# The guard is installed as a file, so the command reads its source and
# never imports it.
GUARD_SOURCE = Path(__file__).resolve().parents[1] / "hooks" / "guard.py"
# The directory that holds the package, from which ``python3 -m
# govharness`` runs.
HARNESS = Path(__file__).resolve().parents[2]


def expiry_horizon(text: str) -> timedelta | None:
    """Parse ``--expiry-horizon``: whole days from 1, or ``none``.

    Parameters
    ----------
    text : str
        The argument.

    Returns
    -------
    timedelta | None
        The horizon, or None where the owner lifts the bound.

    Raises
    ------
    argparse.ArgumentTypeError
        If the argument is neither, with the reason, so that a mistyped
        horizon is a usage error (exit 2) rather than no bound.
    """
    try:
        return parse_horizon(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


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
        type=expiry_horizon,
        default=DEFAULT_HORIZON,
        metavar="DAYS|none",
        help=(
            "refuse an authorization that expires more than DAYS days "
            "after the derivation, or never (default "
            f"{DEFAULT_HORIZON.days}); {NO_HORIZON} lifts the bound"
        ),
    )
    command.add_argument(
        ACCEPT_UNSIGNED,
        action="store_true",
        help=(
            "rely on unsigned authorizations where no signer register "
            "exists; no effect where a signature is required"
        ),
    )
    command.add_argument(
        "--assured",
        action="store_true",
        help="the classification records the work as CSQ0 or CSQ1",
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path, metavar="OUT")
    mode.add_argument(
        "--check",
        action="store_true",
        help=(
            "compare the installed files with a fresh rendering; give it "
            "the options of the derivation it checks, --expiry-horizon "
            "included, since the default horizon may refuse an "
            "authorization that the derivation accepted; INSTALL.md "
            "prints them"
        ),
    )
    command.set_defaults(run=lambda a, _: run_environment(a))


def inputs_of(
    args: argparse.Namespace,
    remote_writes: tuple[RemoteWrite, ...] = (),
    referred: tuple[str, ...] = (),
    unsigned: tuple[str, ...] = (),
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
    unsigned : tuple[str, ...]
        Authorizations relied on unsigned under ``--accept-unsigned``.

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
        unsigned=unsigned,
    )


def derivation_options(args: argparse.Namespace) -> tuple[str, ...]:
    """Return every option of a derivation, as ``--check`` repeats it.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments of ``environment``.

    Returns
    -------
    tuple[str, ...]
        The options in the order of the parser, each repeated option in
        the order given, and paths made absolute, as the configuration
        names them; ``--write`` and ``--check`` are left out. The
        horizon is named wherever an authorization is, or where it is
        not the default, so that a later default does not change the
        check (unit 0014).
    """
    words = ["--work", str(args.work.resolve())]
    words += ["--home", str(args.home.resolve())]
    for path in args.open:
        words += ["--open", str(path.resolve())]
    for domain in args.domain:
        words += ["--domain", domain]
    for tool in args.tool:
        words += ["--tool", tool]
    words += ["--search"] if args.search else []
    words += ["--unattended"] if args.unattended else []
    words += ["--secret-store"] if args.secret_store else []
    for name in args.secret:
        words += ["--secret", name]
    for ident in args.authorization:
        words += ["--authorization", ident]
    words += ["--role", args.role] if args.role else []
    horizon = args.expiry_horizon
    if args.authorization or horizon != DEFAULT_HORIZON:
        days = NO_HORIZON if horizon is None else str(horizon.days)
        words += ["--expiry-horizon", days]
    words += [ACCEPT_UNSIGNED] if args.accept_unsigned else []
    words += ["--assured"] if args.assured else []
    return tuple(words)


def derivation_of(args: argparse.Namespace) -> claude_code.Derivation:
    """Return how the command derives, for the steps of INSTALL.md.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments of ``environment``.

    Returns
    -------
    claude_code.Derivation
        The harness directory, the corpus root, the options, and the
        output directory, each path absolute.
    """
    return claude_code.Derivation(
        harness=str(HARNESS),
        corpus=str(args.root.resolve()),
        options=derivation_options(args),
        out=str(args.write.resolve()) if args.write else "OUT",
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
        If a named authorization is not in force at this moment, or no
        signature is required and ``--accept-unsigned`` is not given, or
        the ledger or the signer configuration shows a signer register
        that the corpus lacks, or the ledger's shape cannot be read.
    """
    if not args.authorization:
        return Reading((), (), ())
    ledger = read_ledger(args.root)
    # A signature is required for assured work, and wherever a signer
    # register exists, since an unsigned entry is then the exception.
    # Elsewhere an agent could have appended the authorize, so the owner
    # must accept the authorizations unsigned (unit 0010). A register
    # that the ledger or the signer configuration shows and the corpus
    # lacks was removed, or is yet to be founded, so the signature stays
    # required and nothing verifies. The trace is read before the chain
    # is checked and takes any shape of ledger; a ledger it cannot read
    # counts as a trace (fail closed).
    config = read_config()
    present = any(p.parts[:1] == (REGISTER_ID,) for p in tree.files)
    trace = (
        None
        if present
        else register_trace(ledger, config.anchor is not None)
    )
    signed = args.assured or present or trace is not None
    verified = (
        signed
        and trace is None
        and ledger_shape(ledger) is None
        and not ledger_problems(tree, ledger, config)
    )
    try:
        return read_authorizations(
            Corpus(load_entries(tree)),
            tree,
            ledger,
            tuple(args.authorization),
            datetime.now(timezone.utc),
            args.role,
            signed,
            verified,
            args.expiry_horizon,
            args.accept_unsigned,
        )
    except ValueError as error:
        if trace:
            raise ValueError(
                f"{trace}, {REGISTER_REMOVED} | {error}"
            ) from error
        raise


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
            inputs_of(
                args, reading.writes, reading.referred, reading.unsigned
            ),
            read_text(GUARD_SOURCE),
            derivation_of(args),
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
