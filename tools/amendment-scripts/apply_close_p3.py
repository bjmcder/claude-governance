"""Rehearsable package P3 of the closing round of 2026-10-25: P1 first, then STND.RUST 1.1, STND.FTN 1.1,
STND.SV 1.1, and STND.LEAN 1.0.1.

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p3.py

P3 cites the new provisions of STND.CODE 1.2 and replaces citations of the provisions that STND.CXX 1.2 withdraws,
so apply_close_p1.py runs first, unchanged. No document of P3 cites a provision that another document of P3 adds,
so their order among themselves is free. Each script keeps its placeholder time; the lead sets the real times at the
coalesce.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = ["apply_close_p1", "apply_rust_1_1", "apply_ftn_1_1", "apply_sv_1_1", "apply_lean_1_0_1"]


def apply(root: Path) -> None:
    root = Path(root)
    for name in ORDER:
        importlib.import_module(name).apply(root)
