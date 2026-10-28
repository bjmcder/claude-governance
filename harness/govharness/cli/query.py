"""The read-only commands ``show``, ``find``, ``context``, and ``pairs``.

They load the corpus, answer one question, and write nothing, so that a
reader fetches the governance it needs without searching the files. The
root is optional (``cli.arguments``). One rule of exit codes holds
across them (unit 0022): 0 when something was found, 1 when nothing
was, with the message on the standard error, and 2 for a usage error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from govharness.cli.arguments import corpus_root, default_root, split_root
from govharness.core.corpus import Corpus, read_corpus
from govharness.query.combination import review_pairs
from govharness.query.graph import build_graph
from govharness.query.retrieval import context, find, label, show, stems

ROOT_HELP = "corpus root; else $GOVHARNESS_ROOT, else ./governance"


def add_query(sub: argparse._SubParsersAction) -> None:
    """Add the ``show``, ``find``, ``context``, and ``pairs`` commands.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    item = sub.add_parser("show", help="one item and its cross references")
    item.add_argument("root", nargs="?", type=corpus_root, help=ROOT_HELP)
    item.add_argument("ident", metavar="ID", help="identifier or locator")
    item.add_argument(
        "--expand", action="store_true", help="add the text of cited items"
    )
    item.add_argument(
        "--all",
        action="store_true",
        help="print each item a document holds, whole, in order",
    )
    item.set_defaults(run=lambda a, _: run_show(a))
    search = sub.add_parser("find", help="items holding the words, ranked")
    search.add_argument("root", nargs="?", help=ROOT_HELP)
    search.add_argument("words", nargs="+")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--in-force", action="store_true")
    search.set_defaults(run=lambda a, _: run_find(a))
    topic = sub.add_parser(
        "context", help="the governance on a topic, within a budget"
    )
    topic.add_argument("root", nargs="?", help=ROOT_HELP)
    topic.add_argument("words", nargs="+")
    topic.add_argument("--budget", type=int, default=8000)
    topic.add_argument("--in-force", action="store_true")
    topic.set_defaults(run=lambda a, _: run_context(a))

    pairs = sub.add_parser(
        "pairs",
        help="provision pairs to review before a change (STND.HARN.28)",
    )
    pairs.add_argument("root", nargs="?", type=corpus_root, help=ROOT_HELP)
    pairs.add_argument("ident", metavar="ID", help="the changed document")
    pairs.add_argument(
        "--amends",
        nargs="*",
        default=[],
        metavar="LVL0_ID",
        help="LVL0 provisions the change amends",
    )
    pairs.set_defaults(run=lambda a, _: run_pairs(a))


def load(command: str, root: Path | None) -> Corpus | None:
    """Read the corpus at a root, or at the default root.

    Parameters
    ----------
    command : str
        The command, named in the message.
    root : Path | None
        The root given, or ``None`` for the default.

    Returns
    -------
    Corpus | None
        The corpus; ``None`` when no root is known, after one line on
        the standard error naming ``GOVHARNESS_ROOT``.
    """
    try:
        return read_corpus(root if root is not None else default_root())
    except ValueError as error:
        print(f"{command}: {error}", file=sys.stderr)
        return None


def run_show(args: argparse.Namespace) -> int:
    """Run ``show``: print one item with its cross references.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``ident``, ``expand``, and ``all``.

    Returns
    -------
    int
        1 when no item has the identifier, 2 when no root is known,
        else 0.
    """
    corpus = load("show", args.root)
    if corpus is None:
        return 2
    try:
        text = show(
            corpus, build_graph(corpus), args.ident, args.expand, args.all
        )
    except KeyError:
        print(f"show: no item {args.ident}", file=sys.stderr)
        return 1
    print(text, end="")
    return 0


def run_find(args: argparse.Namespace) -> int:
    """Run ``find``: print the matching items, one line each.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``words``, ``limit``, and ``in_force``.

    Returns
    -------
    int
        1 when no item holds a word of the query, 2 when no root is
        known, else 0.
    """
    root, words = split_root(args.root, args.words)
    corpus = load("find", root)
    if corpus is None:
        return 2
    graph = build_graph(corpus)
    query = " ".join(words)
    matches = find(corpus, graph, query, args.limit, args.in_force)
    if not matches:
        print(f"find: no item holds a word of: {query}", file=sys.stderr)
        return 1
    best = max(m.held for m in matches)
    if best < len(set(stems(query))):
        print(f"(no item holds every word; best hold {best})")
    for match in matches:
        print(f"- {label(corpus, graph, match.node)}")
    return 0


def run_context(args: argparse.Namespace) -> int:
    """Run ``context``: print the governance on a topic.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``words``, ``budget``, and ``in_force``.

    Returns
    -------
    int
        1 when no item holds a word of the query, 2 when no root is
        known, else 0.
    """
    root, words = split_root(args.root, args.words)
    corpus = load("context", root)
    if corpus is None:
        return 2
    query = " ".join(words)
    text = context(
        corpus, build_graph(corpus), query, args.budget, args.in_force
    )
    if not text:
        print(f"context: no item holds a word of: {query}", file=sys.stderr)
        return 1
    print(text, end="")
    return 0


def run_pairs(args: argparse.Namespace) -> int:
    """Run ``pairs``: list the provision pairs a change puts to review.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``ident``, and ``amends``.

    Returns
    -------
    int
        1 when the changed document is not in the corpus, 2 when no
        root is known, else 0.
    """
    corpus = load("pairs", args.root)
    if corpus is None:
        return 2
    if args.ident not in corpus.by_id:
        print(f"pairs: no document {args.ident}", file=sys.stderr)
        return 1
    found = review_pairs(corpus, args.ident, tuple(args.amends))
    print(f"# Pairs for review before a change of {args.ident} (STND.HARN.28)")
    print()
    print(f"{len(found)} pair(s).")
    print()
    print("| # | Changed side | Other provision | Bases |")
    print("| --- | --- | --- | --- |")
    for number, pair in enumerate(found, start=1):
        bases = ", ".join(pair.bases)
        print(f"| {number} | {pair.first} | {pair.second} | {bases} |")
    return 0
