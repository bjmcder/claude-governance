"""The commands that check or write derived files.

``manifests`` regenerates every ``MANIFEST.csv`` (``--write``) or lists
the stale ones (``--check``). ``references`` writes the References
section of named documents (``--write``) or reports every adopted
document below LVL0 whose table differs from the derived one
(``--check``). ``compose`` writes the reading copies of the divided
standards into ``rendered/`` beside the corpus root (``--write``) or
lists the stale ones (``--check``).
"""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath

from govharness.checks.drafting.citations import references_problem
from govharness.core.corpus import (
    Corpus,
    load_entries,
    read_corpus,
    read_optional_text,
    read_tree,
)
from govharness.core.entry import DOC_FILE
from govharness.derive.manifests import stale_manifests
from govharness.derive.reading_copy import reading_copies
from govharness.derive.references import rewrite_sections
from govharness.ledger.chain import read_ledger

LOWER_LEVELS = {"LVL1", "LVL2", "LVL3"}
# The reading copies live beside the corpus, not in it: they are derived
# and no ledger transaction pins them.
RENDERED = "rendered"


def write_files(root: Path, files: dict[PurePosixPath, str]) -> None:
    """Write derived files under a root.

    Parameters
    ----------
    root : Path
        Corpus root.
    files : dict[PurePosixPath, str]
        Text by path relative to the root.
    """
    for rel, text in files.items():
        (root / rel).write_text(text, encoding="utf-8")


def run_manifests(args: argparse.Namespace) -> int:
    """Run ``manifests``: write or check every manifest.

    Parameters
    ----------
    args : argparse.Namespace
        ``root`` and ``check`` (else ``write``).

    Returns
    -------
    int
        1 when checking finds a stale manifest, else 0.
    """
    stale = stale_manifests(read_tree(args.root))
    if args.check:
        for path in stale:
            print(f"stale: {path}")
    else:
        write_files(args.root, stale)
    print(f"{'stale' if args.check else 'written'}: {len(stale)}")
    return 1 if args.check and stale else 0


def run_references(args: argparse.Namespace) -> int:
    """Run ``references``: write or check References sections.

    Parameters
    ----------
    args : argparse.Namespace
        ``root`` and either ``write`` (identifiers) or ``check``.

    Returns
    -------
    int
        1 when checking finds a wrong table, else 0.
    """
    tree = read_tree(args.root)
    corpus = Corpus(load_entries(tree))
    if args.write:
        write_files(args.root, rewrite_sections(tree, corpus, args.write))
        return 0
    lower = [
        str(e.meta["id"])
        for e in corpus.entries
        if e.path.name == DOC_FILE
        and e.meta.get("level") in LOWER_LEVELS
        and e.meta.get("status") == "adopted"
    ]
    problems = [
        f"- {d}: {p}"
        for d in lower
        if (p := references_problem(corpus, d)) is not None
    ]
    print("\n".join(problems) or "references: PASS")
    return 1 if problems else 0


def run_compose(args: argparse.Namespace) -> int:
    """Run ``compose``: write or check the reading copies.

    Parameters
    ----------
    args : argparse.Namespace
        ``root`` and ``check`` (else ``write``).

    Returns
    -------
    int
        1 when checking finds a stale copy, else 0.
    """
    copies = reading_copies(read_corpus(args.root), read_ledger(args.root))
    # Resolved, so that a root given as "." still writes beside it.
    folder = args.root.resolve().parent / RENDERED
    stale = {
        name: text
        for name, text in copies.items()
        if read_optional_text(folder / name) != text
    }
    if args.check:
        for name in stale:
            print(f"stale: {RENDERED}/{name}")
    else:
        folder.mkdir(exist_ok=True)
        write_files(folder, stale)
    print(f"{'stale' if args.check else 'written'}: {len(stale)}")
    return 1 if args.check and stale else 0
