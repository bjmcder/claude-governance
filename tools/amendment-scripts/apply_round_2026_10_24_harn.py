"""Rehearsable round: STND.PROJ 1.2, then STND.HARN 1.2 (two transactions), closing the open item of STND.HARN.18.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24_harn.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_harn_1_2  # noqa: E402
import apply_proj_1_2  # noqa: E402


def apply(root: Path) -> None:
    apply_proj_1_2.apply(root)
    apply_harn_1_2.apply(root)
