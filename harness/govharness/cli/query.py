"""The read-only commands ``show``, ``find``, ``context``, and ``pairs``.

They load the corpus, answer one question, and write nothing, so that a
reader fetches the governance it needs without searching the files.
"""

from __future__ import annotations

import argparse
import sys

from govharness.cli.arguments import corpus_root
from govharness.core.corpus import read_corpus
from govharness.query.combination import review_pairs
from govharness.query.graph import build_graph
from govharness.query.retrieval import context, find, label, show, stems


def add_query(sub: argparse._SubParsersAction) -> None:
    """Add the ``show``, ``find``, ``context``, and ``pairs`` commands.

    Parameters
    ----------
    sub : argparse._SubParsersAction
        Subcommand registry of the main parser.
    """
    item = sub.add_parser("show", help="one item and its cross references")
    item.add_argument("root", type=corpus_root)
    item.add_argument("ident", metavar="ID", help="identifier or locator")
    item.add_argument(
        "--expand", action="store_true", help="add the text of cited items"
    )
    item.set_defaults(run=lambda a, _: run_show(a))
    search = sub.add_parser("find", help="items holding the words, ranked")
    search.add_argument("root", type=corpus_root)
    search.add_argument("words", nargs="+")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--in-force", action="store_true")
    search.set_defaults(run=lambda a, _: run_find(a))
    topic = sub.add_parser(
        "context", help="the governance on a topic, within a budget"
    )
    topic.add_argument("root", type=corpus_root)
    topic.add_argument("words", nargs="+")
    topic.add_argument("--budget", type=int, default=8000)
    topic.add_argument("--in-force", action="store_true")
    topic.set_defaults(run=lambda a, _: run_context(a))

    pairs = sub.add_parser(
        "pairs",
        help="provision pairs to review before a change (STND.HARN.28)",
    )
    pairs.add_argument("root", type=corpus_root)
    pairs.add_argument("ident", metavar="ID", help="the changed document")
    pairs.add_argument(
        "--amends",
        nargs="*",
        default=[],
        metavar="LVL0_ID",
        help="LVL0 provisions the change amends",
    )
    pairs.set_defaults(run=lambda a, _: run_pairs(a))


def run_show(args: argparse.Namespace) -> int:
    """Run ``show``: print one item with its cross references.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``ident``, and ``expand``.

    Returns
    -------
    int
        1 when no item has the identifier, else 0.
    """
    corpus = read_corpus(args.root)
    try:
        text = show(corpus, build_graph(corpus), args.ident, args.expand)
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
        1 when no item holds a word of the query, else 0.
    """
    corpus = read_corpus(args.root)
    graph = build_graph(corpus)
    words = " ".join(args.words)
    matches = find(corpus, graph, words, args.limit, args.in_force)
    if not matches:
        print(f"find: no item holds a word of: {words}", file=sys.stderr)
        return 1
    if matches[0].held < len(set(stems(words))):
        print(f"(no item holds every word; best hold {matches[0].held})")
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
        Always 0.
    """
    corpus = read_corpus(args.root)
    print(
        context(
            corpus,
            build_graph(corpus),
            " ".join(args.words),
            args.budget,
            args.in_force,
        ),
        end="",
    )
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
        2 when the changed document is not in the corpus, else 0.
    """
    corpus = read_corpus(args.root)
    if args.ident not in corpus.by_id:
        print(f"pairs: no document {args.ident}", file=sys.stderr)
        return 2
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
