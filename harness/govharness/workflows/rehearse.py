"""Rehearse an amendment script on a fresh copy of the corpus.

A rehearsal copies the corpus into a new temporary directory, runs the
script against the copy, and verifies the copy. It then confirms that
the source corpus, its ledger included, is byte for byte as it was. A
script that writes to the source, as a mistaken path once made a
rehearsal append to the live ledger (ledger entries 30 and 31), is
reported as ``SourceChanged`` instead of passing silently (PRIME.4).

The script is a Python file that defines ``apply(root: Path) -> None``
and changes only the root it is given, typically through
``govharness.workflows.amend``. The copy is kept for inspection.
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from govharness.checks.verification import Verification
from govharness.core.corpus import tree_digests
from govharness.ledger.chain import read_ledger
from govharness.ledger.transactions import Transaction
from govharness.workflows.verification import usable_store, verify_corpus

Script = Callable[[Path], None]


class SourceChanged(RuntimeError):
    """The source corpus changed while a rehearsal ran.

    Parameters
    ----------
    changed : list[str]
        Paths, relative to the source root, of the files or
        directories added or removed and of the files altered.
    """

    def __init__(self, changed: list[str]) -> None:
        """Record the changed paths in the message.

        Parameters
        ----------
        changed : list[str]
            Paths of the files or directories added or removed and of
            the files altered.
        """
        super().__init__(
            "the rehearsal changed the source corpus: " + ", ".join(changed)
        )
        self.changed = changed


@dataclass
class Rehearsal:
    """What a rehearsal did to its copy.

    Parameters
    ----------
    copy : Path
        Root of the copy the script ran against.
    appended : list[Transaction]
        Ledger entries the script appended to the copy.
    verification : Verification
        The verification of the copy after the script.
    source_paths : int
        Number of source files and directories confirmed unchanged.
    """

    copy: Path
    appended: list[Transaction]
    verification: Verification
    source_paths: int


def load_script(script: Path) -> Script:
    """Load the ``apply`` function of an amendment script.

    Parameters
    ----------
    script : Path
        Python file that defines ``apply(root)``.

    Returns
    -------
    Script
        The function.

    Raises
    ------
    ValueError
        If the file cannot be loaded or defines no callable ``apply``.
    """
    spec = importlib.util.spec_from_file_location("rehearsed_script", script)
    if spec is None or spec.loader is None:
        raise ValueError(f"{script}: not a Python file")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    apply = getattr(module, "apply", None)
    if not callable(apply):
        raise ValueError(f"{script}: defines no function apply(root)")
    return apply


def _changed(before: dict[str, str], after: dict[str, str]) -> list[str]:
    """Return the paths whose digest differs between two snapshots.

    Parameters
    ----------
    before, after : dict[str, str]
        Digest by path.

    Returns
    -------
    list[str]
        Paths added, removed, or altered, sorted.
    """
    return sorted(
        path
        for path in before.keys() | after.keys()
        if before.get(path) != after.get(path)
    )


def rehearse(root: Path, script: Path, work: Path | None = None) -> Rehearsal:
    """Run an amendment script on a copy of the corpus and verify it.

    Parameters
    ----------
    root : Path
        Source corpus root; it is read, never written.
    script : Path
        Amendment script defining ``apply(root)``.
    work : Path | None
        Existing directory that receives the copy; ``None`` makes a new
        temporary directory.

    Returns
    -------
    Rehearsal
        The copy, the entries appended to it, its verification, and
        the number of source files and directories confirmed unchanged.

    Raises
    ------
    SourceChanged
        If a file or directory of the source corpus was added or
        removed, or a file was altered.
    ValueError
        If the solve cache the environment names cannot be used
        (``usable_store``): checked against the source before anything
        is copied, and against the copy before the script runs.
    """
    # Absolute, so that a script that changes the working directory
    # cannot make the second snapshot read another tree.
    root = root.absolute()
    store = usable_store(root, True)
    before = tree_digests(root)
    work = (work or Path(tempfile.mkdtemp(prefix="rehearsal-"))).absolute()
    copy = work / root.name
    shutil.copytree(root, copy)
    store = usable_store(copy, store or False)
    already = len(read_ledger(copy))
    try:
        load_script(script.absolute())(copy)
        verification = verify_corpus(copy, cache=store or False)
    finally:
        changed = _changed(before, tree_digests(root))
        if changed:
            raise SourceChanged(changed)
    return Rehearsal(
        copy, read_ledger(copy)[already:], verification, len(before)
    )
