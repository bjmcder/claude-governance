"""Rehearsable round script of package P5 (2026-10-25 close): editorial amendments that complete References.

Applies, on top of ledger entry 147, one editorial amendment per document whose text named a document without
citing it (tools/check_refs.py), in citation order: the standards first, then the profiles and sub-profiles they
are cited by. Each script keeps its placeholder time; the lead sets the real times at the coalesce.
Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_close_p5.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

AMENDMENTS = [
    'apply_ident_1_3_3',
    'apply_class_1_3_1',
    'apply_dflt_1_5_1',
    'apply_know_1_0_1',
    'apply_ml_1_0_1',
    'apply_cps_1_0_1',
    'apply_hw_cpu_1_0_1',
    'apply_hw_gpu_1_0_1',
    'apply_hw_qpu_1_0_1',
    'apply_hw_embed_1_0_2',
    'apply_hw_fpga_1_0_1',
    'apply_hw_1_1_2',
    'apply_hdes_asic_1_0_2',
    'apply_hdes_1_0_2',
]


def apply(root: Path) -> None:
    root = Path(root)
    for name in AMENDMENTS:
        importlib.import_module(name).apply(root)
