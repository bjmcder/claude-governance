"""Rehearsable round: MNEM gains OMP, then STND.OMP 1.0 is adopted (two transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_mnem_omp  # noqa: E402
import apply_omp  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_omp.apply(root)
    apply_omp.apply(root)
