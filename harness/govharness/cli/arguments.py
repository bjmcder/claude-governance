"""Argument types shared by the commands."""

from __future__ import annotations

import argparse
from pathlib import Path


def corpus_root(text: str) -> Path:
    """Parse a corpus root argument, refusing one that is no directory.

    Parameters
    ----------
    text : str
        The argument.

    Returns
    -------
    Path
        The root as given.

    Raises
    ------
    argparse.ArgumentTypeError
        If no directory exists there, so that a mistyped root is a
        usage error (exit 2) rather than an empty corpus.
    """
    root = Path(text)
    if not root.is_dir():
        raise argparse.ArgumentTypeError(f"{text}: no such directory")
    return root
