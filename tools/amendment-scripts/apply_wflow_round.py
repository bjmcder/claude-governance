"""Rehearsable round: MNEM gains WFLOW, then STND.WFLOW 1.0 is adopted (two transactions).

Apply after apply_build_round.py: STND.WFLOW cites STND.BUILD in its Purpose and Notes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_mnem_wflow  # noqa: E402
import apply_wflow  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_wflow.apply(root)
    apply_wflow.apply(root)
