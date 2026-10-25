"""Rehearsable package P4 of the closing round of 2026-10-25, on top of ledger entry 147.

Four transactions, one per document: STND.OFFLD 1.0.1, STND.MPI 1.0.1, STND.OMP 1.0.2, STND.HARN 1.3. None cites
a change of another, so the order is free; it follows the order of the package. Each script keeps its placeholder
time; the lead sets the real times at the coalesce. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p4.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SCRIPTS = ["apply_offld_1_0_1", "apply_mpi_1_0_1", "apply_omp_1_0_2", "apply_harn_1_3"]


def apply(root: Path) -> None:
    root = Path(root)
    for name in SCRIPTS:
        importlib.import_module(name).apply(root)
