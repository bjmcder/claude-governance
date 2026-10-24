"""Rehearsable round of 2026-10-24: closing the open items (one script, in ledger order).

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_24.py

The order matters: STND.CXX 1.1 before STND.STDC, whose C reading cites the amended text; NUMER 1.3 before
STND.SV, which cites the new row of NUMER.2; STND.BUILD 1.0 before STND.WFLOW, which cites it, and
STND.BUILD 1.0.1 after STND.WFLOW, citing it back; STND.BUILD before the language standards that cite it;
STND.CONC 1.0.1 after every standard it cites; STND.PROJ 1.2 and STND.HARN 1.2 last. The lead sets each
transaction's time here, one minute apart from START, and chains the mnemonic rows in the order of adoption;
the individual scripts keep their placeholder times for their own rehearsals.
"""
from __future__ import annotations

import importlib
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

START = "2026-10-24T22:00:00+00:00"  # set to the time of application once ratified

AMENDMENTS = ["apply_omp_1_0_1", "apply_cxx_1_1", "apply_py_1_0_1", "apply_jl_1_1", "apply_numer_1_3"]
# (mnemonic script, adoption script); the mnemonic rows are chained after OFFLD in this order.
STANDARDS = [("apply_mnem_build", "apply_build")]
AFTER_BUILD = [("apply_mnem_wflow", "apply_wflow")]
LANGUAGES = [("apply_mnem_c", "apply_c"), ("apply_mnem_rust", "apply_rust"),
             ("apply_mnem_fortran", "apply_fortran"), ("apply_mnem_hdl", "apply_hdl"),
             ("apply_mnem_lean", "apply_lean")]
CLOSING = ["apply_conc_1_0_1"]
HARNESS = ["apply_proj_1_2", "apply_harn_1_2"]

OFFLD_ROW = ("| OFFLD | STND | Accelerator offload standard | none | Reads as offload; offload has no "
             "established acronym | active |")


def _times():
    t = datetime.fromisoformat(START)
    while True:
        yield t.isoformat()
        t += timedelta(minutes=1)


def apply(root: Path) -> None:
    root = Path(root)
    clock = _times()
    after = OFFLD_ROW

    def run(name: str) -> None:
        module = importlib.import_module(name)
        module.AT = next(clock)
        module.apply(root)

    def adopt(pairs) -> None:
        nonlocal after
        for mnem, doc in pairs:
            module = importlib.import_module(mnem)
            module.ROW_AFTER = after
            module.AT = next(clock)
            module.apply(root)
            after = module.ROW
            run(doc)

    for name in AMENDMENTS:
        run(name)
    adopt(STANDARDS)
    adopt(AFTER_BUILD)
    run("apply_build_1_0_1")
    adopt(LANGUAGES)
    for name in CLOSING + HARNESS:
        run(name)
