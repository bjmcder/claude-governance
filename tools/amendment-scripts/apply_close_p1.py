"""Rehearsable package P1 of the closing round of 2026-10-25: STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2.

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p1.py

The order matters. STND.CODE 1.2 comes first, because the other two cite its new provisions. STND.STDC 1.1 comes
next, because it stops referring to the provisions of STND.CXX that STND.CXX 1.2 withdraws. Each script keeps its
placeholder time; the lead sets the real times at the coalesce.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = ["apply_code_1_2", "apply_stdc_1_1", "apply_cxx_1_2"]


def apply(root: Path) -> None:
    root = Path(root)
    for name in ORDER:
        importlib.import_module(name).apply(root)
