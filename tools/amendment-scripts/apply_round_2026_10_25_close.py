"""Rehearsable closing round of 2026-10-25: every package in ledger order.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_25_close.py

The order matters: P1 (STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2) before every amendment that cites the new
provisions of STND.CODE; then the editorial References amendments of P5 and STND.BUILD 1.0.2; then P2
(STND.PY, STND.JL), P3 (STND.RUST, STND.FTN, STND.SV, STND.LEAN), and P4 (STND.OFFLD, STND.MPI, STND.OMP,
STND.HARN). The lead sets each transaction's time here, the time at which it is applied; the package scripts
keep their placeholder times for their own rehearsals.
"""
from __future__ import annotations

import importlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _order() -> list[str]:
    p1 = importlib.import_module("apply_close_p1").ORDER
    p5 = importlib.import_module("apply_close_p5").AMENDMENTS
    p2 = [n for n in importlib.import_module("apply_close_p2").ORDER if n != "apply_close_p1"]
    p3 = [n for n in importlib.import_module("apply_close_p3").ORDER if n != "apply_close_p1"]
    p4 = importlib.import_module("apply_close_p4").SCRIPTS
    return [*p1, *p5, "apply_build_1_0_2", *p2, *p3, *p4]


def _times():
    # The time of application, to the second; the next transaction waits for the next second.
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
    for name in _order():
        module = importlib.import_module(name)
        module.AT = next(clock)
        module.apply(root)
