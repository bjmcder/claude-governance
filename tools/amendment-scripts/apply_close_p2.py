"""Rehearsable package P2 of the closing round of 2026-10-25: STND.PY 1.1 and STND.JL 1.2, on top of package P1.

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p2.py

The order matters. Package P1 comes first (STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2), because both amendments
cite the new provisions of STND.CODE. STND.PY 1.1 comes next, because the Notes of STND.JL 1.2 name its new
STND.PY.35, and the Notes of STND.PY 1.1 name STND.JL.39, which an unknown identifier in Notes does not fail. Each
script keeps its placeholder time; the lead sets the real times at the coalesce.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = ["apply_close_p1", "apply_py_1_1", "apply_jl_1_2"]


def apply(root: Path) -> None:
    root = Path(root)
    for name in ORDER:
        importlib.import_module(name).apply(root)
