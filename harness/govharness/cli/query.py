"""The read-only commands ``show``, ``find``, ``context``, ``pairs``, and
``onset``.

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
from govharness.core.onset import STARTS, applying_from, describe, onset_of
from govharness.query.combination import document_id, review_pairs
from govharness.query.graph import build_graph
from govharness.query.retrieval import (
    context,
    find,
    label,
    resolve_ref,
    show,
    stems,
)

ROOT_HELP = "corpus root; else $GOVHARNESS_ROOT, else ./governance"


def add_query(sub: argparse._SubParsersAction) -> None:
    """Add the ``show``, ``find``, ``context``, ``pairs``, and ``onset``
    commands.

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
    pairs.add_argument(
        "ident", metavar="ID", help="a changed document or provision"
    )
    pairs.add_argument(
        "--amends",
        nargs="+",
        action="extend",
        default=[],
        metavar="LVL0_ID",
        help="LVL0 provisions the change amends",
    )
    pairs.add_argument(
        "--with",
        dest="also",
        nargs="+",
        action="extend",
        default=[],
        metavar="ID",
        help="other documents or provisions that the change adopts or amends",
    )
    pairs.set_defaults(run=lambda a, _: run_pairs(a))
    onset = sub.add_parser(
        "onset",
        help="the provisions and parts that apply from a class (unit 0023)",
    )
    onset.add_argument("root", nargs="?", type=corpus_root, help=ROOT_HELP)
    onset.add_argument(
        "cls", metavar="CSQn", choices=STARTS, help="CSQ0 to CSQ3"
    )
    onset.set_defaults(run=lambda a, _: run_onset(a))


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

    Each ``ID`` names a document below LVL0 or a provision below LVL0;
    a LVL0 document, such as an article, is admitted as ``ID`` only with
    ``--amends``, which names LVL0 provisions alone.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``ident``, ``amends``, and ``also``, the other
        documents or provisions of the same change.

    Returns
    -------
    int
        1 when an identifier names nothing that the command takes, or
        when the change puts no pair to review, with the message on the
        standard error; 2 when no root is known; else 0. An identifier
        in the wrong case names its item, as it does for ``show``.
    """
    corpus = load("pairs", args.root)
    if corpus is None:
        return 2
    graph = build_graph(corpus)
    lower_docs = {
        document_id(corpus, p)
        for p in corpus.provisions()
        if p.meta.get("level") not in (None, "LVL0")
    }
    amends: list[str] = []
    for given in args.amends:
        ident = resolve_ref(corpus, graph, given)
        entry = corpus.by_id.get(ident or "")
        if entry is None or not (
            entry.meta.get("kind") == "provision"
            and entry.meta.get("level") == "LVL0"
        ):
            print(
                f"pairs: --amends {given} is not a LVL0 provision",
                file=sys.stderr,
            )
            return 1
        amends.append(str(ident))
    named: list[str] = []
    for given in [args.ident, *args.also]:
        ident = resolve_ref(corpus, graph, given)
        entry = corpus.by_id.get(ident or "")
        lower = entry is not None and (
            ident in lower_docs
            or (
                entry.meta.get("kind") == "provision"
                and entry.meta.get("level") not in (None, "LVL0")
            )
        )
        lvl0_doc = (
            entry is not None
            and entry.meta.get("level") == "LVL0"
            and entry.meta.get("kind") != "provision"
        )
        if not lower and not (lvl0_doc and amends):
            what = (
                "a LVL0 document, given without --amends"
                if lvl0_doc
                else "not a document or provision below LVL0"
            )
            print(f"pairs: {given} is {what}", file=sys.stderr)
            return 1
        if ident not in named:
            named.append(str(ident))
    found = review_pairs(corpus, tuple(named), tuple(amends))
    names = ", ".join(named)
    if not found:
        print(
            f"pairs: no pair to review before a change of {names}",
            file=sys.stderr,
        )
        return 1
    print(f"# Pairs for review before a change of {names} (STND.HARN.28)")
    print()
    print(f"{len(found)} pair(s).")
    print()
    print("| # | Changed side | Other provision | Bases |")
    print("| --- | --- | --- | --- |")
    for number, pair in enumerate(found, start=1):
        bases = ", ".join(pair.bases)
        print(f"| {number} | {pair.first} | {pair.second} | {bases} |")
    return 0


def run_onset(args: argparse.Namespace) -> int:
    """Run ``onset``: list what a reclassification to a class adds.

    Parameters
    ----------
    args : argparse.Namespace
        ``root`` and ``cls``.

    Returns
    -------
    int
        1 when no provision or part applies from the class, 2 when no
        root is known, else 0. Each line names a provision, or a part of
        one, with its title; a provision whose field gives other parts a
        more severe class names them after its title.
    """
    corpus = load("onset", args.root)
    if corpus is None:
        return 2
    found = applying_from(corpus.provisions(), args.cls)
    if not found:
        print(f"onset: no provision applies from {args.cls}", file=sys.stderr)
        return 1
    print(f"# Provisions and parts that apply from {args.cls}")
    print()
    print(f"{len(found)} item(s).")
    print()
    for entry, part in found:
        ident = entry.meta["id"]
        name = ident if part is None else f"{ident}, {part}"
        line = f"- {name} — {entry.meta.get('title', '')}"
        onset = onset_of(entry)
        if part is None and onset is not None and onset.parts:
            line += f" ({describe(onset)})"
        print(line)
    return 0
