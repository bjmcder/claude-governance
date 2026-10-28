"""Argument types shared by the commands, and the default corpus root.

The read-only commands take the corpus root as an optional positional
argument (unit 0022). When it is omitted, the root is the directory the
environment variable ``GOVHARNESS_ROOT`` names, else ``./governance``
when that directory exists; otherwise the command stops with a usage
error that names the variable. This is the one place the command line
reads the environment (decision 0001, adjustment of unit 0022).
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

ENV_ROOT = "GOVHARNESS_ROOT"
DEFAULT_ROOT = "governance"


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


def default_root() -> Path:
    """Return the corpus root the environment or the working directory names.

    Returns
    -------
    Path
        The directory ``GOVHARNESS_ROOT`` names when the variable is
        set, else ``./governance``.

    Raises
    ------
    ValueError
        If the variable names no directory, or it is unset and no
        ``./governance`` exists; the message names the variable.
    """
    named = os.environ.get(ENV_ROOT, "")
    if named:
        root = Path(named)
        if not root.is_dir():
            raise ValueError(f"{ENV_ROOT}={named}: no such directory")
        return root
    root = Path(DEFAULT_ROOT)
    if root.is_dir():
        return root
    raise ValueError(
        f"no corpus root: give ROOT, set {ENV_ROOT}, "
        f"or run where ./{DEFAULT_ROOT} exists"
    )


def split_root(
    first: str | None, rest: list[str]
) -> tuple[Path | None, list[str]]:
    """Separate an optional root from the words of a query.

    The parser gives the first positional argument of ``find`` and
    ``context`` as the root. It is one only where a directory of that
    name exists; otherwise it is the first word of the query and the
    root is omitted.

    Parameters
    ----------
    first : str | None
        The first positional argument, or ``None`` when only one was
        given.
    rest : list[str]
        The other positional arguments.

    Returns
    -------
    tuple[Path | None, list[str]]
        The root, or ``None`` when omitted, and the words.
    """
    if first is None:
        return None, rest
    if Path(first).is_dir():
        return Path(first), rest
    return None, [first, *rest]
