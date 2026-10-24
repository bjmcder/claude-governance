"""Verify the corpus at a root: load it, then run every check.

The checks compute on data (``checks.verification``); this module reads
the snapshot of the corpus, its ledger, and the signer configuration
that the human owner keeps (``ledger/gpg.py``).
"""

from __future__ import annotations

from pathlib import Path

from govharness.checks.verification import Verification, verify_snapshot
from govharness.core.corpus import read_tree
from govharness.ledger.chain import read_ledger
from govharness.ledger.gpg import read_config


def verify_corpus(
    root: Path,
    logic: bool = True,
    use_z3: bool = True,
) -> Verification:
    """Load the corpus at a root and verify it.

    Parameters
    ----------
    root : Path
        Corpus root.
    logic : bool
        Whether to run the logic checks.
    use_z3 : bool
        Whether the proofs may use z3 when it is importable.

    Returns
    -------
    Verification
        The results.
    """
    return verify_snapshot(
        read_tree(root),
        read_ledger(root),
        logic=logic,
        use_z3=use_z3,
        signer_config=read_config(),
    )
