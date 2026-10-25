"""Rehearsal round for the P5 amendment of STND.BUILD 1.0.2, which cites STND.CODE.16 of package P1.

Applies package P1 (apply_close_p1.py) and then apply_build_1_0_2.py, on top of ledger entry 147. It is for
rehearsal only: the lead orders the packages at the coalesce, with STND.BUILD 1.0.2 after P1.
Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p5_build.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = ["apply_close_p1", "apply_build_1_0_2"]


def apply(root: Path) -> None:
    root = Path(root)
    for name in ORDER:
        importlib.import_module(name).apply(root)
