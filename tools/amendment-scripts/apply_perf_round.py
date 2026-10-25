"""Rehearsable round: MNEM gains PERF, then STND.PERF 1.0 is adopted (two transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_mnem_perf  # noqa: E402
import apply_perf  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_perf.apply(root)
    apply_perf.apply(root)
