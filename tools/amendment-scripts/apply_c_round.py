"""Rehearsable round: MNEM gains STDC, then STND.STDC 1.0 is adopted (two transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_mnem_c  # noqa: E402
import apply_c  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_c.apply(root)
    apply_c.apply(root)
