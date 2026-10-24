"""The commands that run checks: ``verify`` and ``check``.

``verify`` runs the structural checks and, unless told not to, the
logic checks; only a ``FAIL`` fails the run, and ``WARN`` results are
printed. ``check`` runs the logic checks, prints one line per check,
and with ``--out-dir`` writes ``logic_report.md``, ``logic_facts.json``,
and ``drafting_punch_list.md`` there; nothing is written inside the
corpus.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from govharness.checks.base import CheckContext
from govharness.checks.drafting.family import all_findings, punch_list
from govharness.checks.logic.facts import facts_of
from govharness.checks.logic.proofs import solver_backend
from govharness.checks.registry import LOGIC, run_checks
from govharness.checks.verification import Verification
from govharness.core.corpus import read_corpus
from govharness.core.report import Report
from govharness.ledger.chain import read_ledger
from govharness.workflows.verification import verify_corpus

SHOWN_PER_CHECK = 20


def _logic_context(root: Path, use_z3: bool) -> CheckContext:
    """Load a corpus and its ledger into a context for the logic checks.

    Parameters
    ----------
    root : Path
        Corpus root.
    use_z3 : bool
        Whether the proofs may use z3.

    Returns
    -------
    CheckContext
        A fresh context.
    """
    return CheckContext(read_corpus(root), read_ledger(root), use_z3=use_z3)


def summary_lines(found: Verification) -> list[str]:
    """Render a verification as the lines ``verify`` prints.

    Parameters
    ----------
    found : Verification
        Results of a verification.

    Returns
    -------
    list[str]
        The entry count, one status line per section with its first
        failure lines, and the warnings.
    """
    lines = [f"entries: {found.entries}"]
    for name, errors in found.sections().items():
        lines.append(
            f"{name}: {'PASS' if not errors else f'FAIL ({len(errors)})'}"
        )
        lines += [f"  {error}" for error in errors[:SHOWN_PER_CHECK]]
    lines += [f"  warn: {warning}" for warning in found.warnings()]
    return lines


def run_verify(args: argparse.Namespace) -> int:
    """Run ``verify`` and print its summary.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``no_logic``, and ``no_z3``.

    Returns
    -------
    int
        1 if any check failed, else 0.
    """
    found = verify_corpus(
        args.root, logic=not args.no_logic, use_z3=not args.no_z3
    )
    print("\n".join(summary_lines(found)))
    return 0 if found.passed() else 1


def _write_outputs(
    out_dir: Path, root: Path, ctx: CheckContext, report: Report
) -> None:
    """Write the report, the facts, and the punch list of a check run.

    Parameters
    ----------
    out_dir : Path
        Directory to write into; created if absent.
    root : Path
        Corpus root, as named on the command line.
    ctx : CheckContext
        Context of the finished run.
    report : Report
        Its results.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    header = [f"Corpus: `{root}`", f"Solver backend: {solver_backend(ctx)}"]
    (out_dir / "logic_report.md").write_text(
        report.render(header), encoding="utf-8"
    )
    (out_dir / "drafting_punch_list.md").write_text(
        punch_list(all_findings(ctx)), encoding="utf-8"
    )
    (out_dir / "logic_facts.json").write_text(
        json.dumps(facts_of(ctx), indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


def run_check(args: argparse.Namespace) -> int:
    """Run ``check``: the logic checks, one line each.

    Parameters
    ----------
    args : argparse.Namespace
        ``root``, ``out_dir``, and ``no_z3``.

    Returns
    -------
    int
        1 if any check failed, else 0.
    """
    ctx = _logic_context(args.root, not args.no_z3)
    report = run_checks(LOGIC, ctx)
    for item in report.results:
        print(f"[{item.status:4}] {item.key:4} {item.title}")
    print(f"solver: {solver_backend(ctx)}")
    if args.out_dir is not None:
        _write_outputs(args.out_dir, args.root, ctx, report)
    return 1 if report.failures() else 0
