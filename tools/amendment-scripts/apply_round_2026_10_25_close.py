"""Rehearsable closing round of 2026-10-25: every package in ledger order.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_25_close.py

The order matters: STND.CODE 1.2 and STND.STDC 1.1 first, since the later amendments cite the new provisions
of STND.CODE; then P3 (STND.RUST, STND.FTN, STND.SV, STND.LEAN), which retargets its citations of the STND.CXX
provisions that STND.CXX 1.2 withdraws, before STND.CXX 1.2 withdraws them; then STND.CXX 1.2 and P2 (STND.PY,
STND.JL); then the editorial References amendments of P5 and STND.BUILD 1.0.2; then P4 (STND.OFFLD, STND.MPI,
STND.OMP, STND.HARN). No state of the round leaves a document citing a withdrawn identifier. The amendments of
a sub-profile take the scope of its family (HW, HDES), so that each state of the round verifies. The lead sets each transaction's time here, the time at which it is applied; the package scripts
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
    assert p1 == ["apply_code_1_2", "apply_stdc_1_1", "apply_cxx_1_2"], p1
    return [*p1[:2], *p3, p1[2], *p2, *p5, "apply_build_1_0_2", *p4]


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
