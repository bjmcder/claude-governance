"""Verify a corpus: the structural checks, then the logic checks.

The structural checks run here, as data, on a snapshot of the corpus
and its ledger; ``workflows.verification`` loads them from a root and
runs the logic checks after them, with the solve cache. The command
line renders the result, and the workflows run it after a change. Only
a ``FAIL`` fails the verification; ``WARN`` results, of the structural
checks and of the logic checks, are carried for a reader.
"""

from __future__ import annotations

from dataclasses import dataclass

from govharness.checks.base import CheckContext
from govharness.checks.registry import STRUCTURE, run_checks
from govharness.core.corpus import Corpus, Tree, load_entries
from govharness.core.report import Report
from govharness.ledger.gpg import SignerConfig
from govharness.ledger.transactions import Transaction


@dataclass
class Verification:
    """The results of verifying one corpus.

    Parameters
    ----------
    entries : int
        Number of entries loaded.
    structure : Report
        Results of the structural checks, one per check name.
    logic : Report | None
        Results of the logic checks, or ``None`` when they were skipped.
    """

    entries: int
    structure: Report
    logic: Report | None = None

    def sections(self) -> dict[str, list[str]]:
        """Return the failure lines of each part of the verification.

        Returns
        -------
        dict[str, list[str]]
            Failure lines by structural check name, then ``logic`` (one
            line per failed logic check) when the logic checks ran.
        """
        found = {
            r.key: r.details if r.status == "FAIL" else []
            for r in self.structure.results
        }
        if self.logic is not None:
            found["logic"] = [
                f"{r.key} {r.title}" for r in self.logic.failures()
            ]
        return found

    def cautions(self) -> dict[str, list[str]]:
        """Return the warning lines of each structural check that warns.

        Returns
        -------
        dict[str, list[str]]
            Detail lines by structural check name, for each ``WARN``
            result, such as the files that no scope pins.
        """
        return {
            r.key: r.details
            for r in self.structure.results
            if r.status == "WARN"
        }

    def warnings(self) -> list[str]:
        """Return one line per logic check that warns.

        Returns
        -------
        list[str]
            Key and title of each ``WARN`` result.
        """
        if self.logic is None:
            return []
        return [f"{r.key} {r.title}" for r in self.logic.warnings()]

    def passed(self) -> bool:
        """Return True when no check failed.

        Returns
        -------
        bool
            Whether every section is free of failures.
        """
        return not any(self.sections().values())


def verify_structure(
    tree: Tree,
    ledger: list[Transaction],
    signer_config: SignerConfig | None = None,
) -> tuple[Corpus, Verification]:
    """Run the structural checks on a corpus.

    Parameters
    ----------
    tree : Tree
        Snapshot of every file under the corpus root.
    ledger : list[Transaction]
        The corpus ledger, in order.
    signer_config : SignerConfig | None
        Signer anchor and ``gpg`` path; ``None`` means no anchor.

    Returns
    -------
    tuple[Corpus, Verification]
        The corpus the snapshot holds, for the logic checks, and the
        results, with no logic results yet.
    """
    corpus = Corpus(load_entries(tree))
    structure = run_checks(
        STRUCTURE,
        CheckContext(corpus, ledger, tree=tree, signer_config=signer_config),
    )
    return corpus, Verification(len(corpus.entries), structure)
