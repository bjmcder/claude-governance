"""Rehearsable round: MNEM gains CONC, then STND.CONC 1.0 is adopted (two transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_conc  # noqa: E402
import apply_mnem_conc  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_conc.apply(root)
    apply_conc.apply(root)
