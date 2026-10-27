"""Rehearsable round of 2026-10-27: every amendment in ledger order.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_27.py

STND.CODE 1.3 and STND.DEPS 1.1 come first, since the others cite their new provisions. The editorial amendments
of STND.FTN, STND.MPI, and STND.OMP, then STND.STDC, STND.PY, STND.RUST, and STND.JL, drop their citations of the
provisions that STND.CXX 1.3 withdraws, and STND.PY and STND.RUST drop theirs of STND.JL.4 before STND.JL 1.3
withdraws it; STND.CXX comes last. No state of the round cites a withdrawn identifier. The lead sets each
transaction's time here, the time at which it is applied.
"""
from __future__ import annotations

import importlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = ["apply_code_1_3", "apply_deps_1_1", "apply_fi_editorial_2026_10_27", "apply_stdc_1_2", "apply_py_1_2",
         "apply_rust_1_2", "apply_jl_1_3", "apply_cxx_1_3"]


def _times():
    # The time of application, to the second; the next transaction waits for the next second, and the editorial
    # module takes three.
    last = None
    while True:
        now = datetime.now(timezone.utc).replace(microsecond=0)
        while last is not None and now <= last:
            time.sleep(0.2)
            now = datetime.now(timezone.utc).replace(microsecond=0)
        last = now
        yield now.isoformat()


def apply(root: Path) -> None:
    root = Path(root)
    clock = _times()
    for name in ORDER:
        module = importlib.import_module(name)
        module.AT = next(clock)
        if name == "apply_fi_editorial_2026_10_27":
            next(clock)
            next(clock)
        module.apply(root)
