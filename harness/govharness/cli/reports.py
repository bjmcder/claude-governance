"""The commands that run checks: ``verify`` and ``check``.

``verify`` runs the structural checks and, unless told not to, the
logic checks; only a ``FAIL`` fails the run, and ``WARN`` results are
printed. ``check`` runs the logic checks, prints one line per check,
and with ``--out-dir`` writes ``logic_report.md``, ``logic_facts.json``,
and ``drafting_punch_list.md`` there; nothing is written inside the
corpus. Both reuse checked solver results from the solve cache where
``--cache DIR`` or ``GOVHARNESS_CACHE`` names one (units 0011 and
0022); what they print is the same either way, and an entry the cache
refused is named on the standard error. Without a cache, ``verify``
writes nothing anywhere.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from govharness.checks.base import CheckContext
from govharness.checks.drafting.family import all_findings, punch_list
from govharness.checks.logic.facts import facts_of
from govharness.checks.logic.proofs import solver_backend
from govharness.checks.verification import Verification
from govharness.cli.arguments import default_root
from govharness.core.corpus import read_corpus
from govharness.core.report import Report
from govharness.ledger.chain import read_ledger
from govharness.workflows.solve_store import SolveStore, open_store
from govharness.workflows.verification import (
    run_logic,
    usable_store,
    verify_corpus,
)

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


def _store(args: argparse.Namespace) -> SolveStore | None:
    """Return the solve cache that a command's options name.

    Parameters
    ----------
    args : argparse.Namespace
        ``cache``.

    Returns
    -------
    SolveStore | None
        The store, or ``None`` when neither the option nor the
        environment names one.
    """
    return open_store(args.cache)


def _report_refused(store: SolveStore | None) -> None:
    """Name each cache entry a run skipped or refused, on stderr.

    Parameters
    ----------
    store : SolveStore | None
        The store of the run.
    """
    if store is None:
        return
    for key, reason in sorted(store.skipped.items()):
        print(
            f"solve cache: entry {key} skipped ({reason}); recomputed",
            file=sys.stderr,
        )
    for key, reason in sorted(store.rejected.items()):
        print(
            f"solve cache: entry {key} refused ({reason}); recomputed",
            file=sys.stderr,
        )


def _refused(error: ValueError) -> int:
    """Report a cache that cannot be used or a file that cannot be read.

    Parameters
    ----------
    error : ValueError
        The reason.

    Returns
    -------
    int
        2, a usage error.
    """
    print(f"refused: {error}", file=sys.stderr)
    return 2


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
        failure lines, or the first warning lines of a structural check
        that warns, and the warnings of the logic checks.
    """
    lines = [f"entries: {found.entries}"]
    cautions = found.cautions()
    for name, errors in found.sections().items():
        noted = cautions.get(name, [])
        if errors:
            status = f"FAIL ({len(errors)})"
        else:
            status = f"WARN ({len(noted)})" if noted else "PASS"
        lines.append(f"{name}: {status}")
        lines += [f"  {line}" for line in (errors or noted)[:SHOWN_PER_CHECK]]
    lines += [f"  warn: {warning}" for warning in found.warnings()]
    return lines


def run_verify(args: argparse.Namespace) -> int:
    """Run ``verify`` and print its summary.

    Parameters
    ----------
    args : argparse.Namespace
        ``root`` (``None`` for the default root), ``no_logic``,
        ``no_z3``, and ``cache``.

    Returns
    -------
    int
        1 if any check failed, 2 if no root is known, the cache cannot
        be used (inside the corpus, or a relative ``GOVHARNESS_CACHE``)
        or a file cannot be read (front matter or a ledger line that
        does not parse; the message names the file), else 0.
    """
    try:
        root = args.root if args.root is not None else default_root()
        # Without the logic check nothing is solved, so no cache is opened.
        store = None if args.no_logic else _store(args)
        found = verify_corpus(
            root,
            logic=not args.no_logic,
            use_z3=not args.no_z3,
            cache=store or False,
        )
    except ValueError as error:
        return _refused(error)
    print("\n".join(summary_lines(found)))
    _report_refused(store)
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
        ``root``, ``out_dir``, ``no_z3``, and ``cache``.

    Returns
    -------
    int
        1 if any check failed, 2 if the cache cannot be used (inside
        the corpus, or a relative ``GOVHARNESS_CACHE``), else 0.
    """
    try:
        store = usable_store(args.root, _store(args) or False)
    except ValueError as error:
        return _refused(error)
    ctx = _logic_context(args.root, not args.no_z3)
    report = run_logic(ctx, store)
    for item in report.results:
        print(f"[{item.status:4}] {item.key:4} {item.title}")
    print(f"solver: {solver_backend(ctx)}")
    if args.out_dir is not None:
        _write_outputs(args.out_dir, args.root, ctx, report)
    _report_refused(store)
    return 1 if report.failures() else 0
