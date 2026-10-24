"""Rehearsable round: MNEM gains OFFLD, then STND.OFFLD 1.0 is adopted (two transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_mnem_offld  # noqa: E402
import apply_offld  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_offld.apply(root)
    apply_offld.apply(root)
