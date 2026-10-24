"""Rehearsable round of 2026-10-24: amendments citing STND.CONC and STND.OFFLD (five transactions).

STND.OMP 1.0.1, STND.CXX 1.1, STND.PY 1.0.1, STND.JL 1.1, and NUMER 1.3, in that order.
Run from harness/:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24_amend.py
STND.CONC 1.0.1 (apply_conc_1_0_1.py) is applied separately, after STND.WFLOW is adopted.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_cxx_1_1  # noqa: E402
import apply_jl_1_1  # noqa: E402
import apply_numer_1_3  # noqa: E402
import apply_omp_1_0_1  # noqa: E402
import apply_py_1_0_1  # noqa: E402


def apply(root: Path) -> None:
    apply_omp_1_0_1.apply(root)
    apply_cxx_1_1.apply(root)
    apply_py_1_0_1.apply(root)
    apply_jl_1_1.apply(root)
    apply_numer_1_3.apply(root)
