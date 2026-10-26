"""Rehearsable round of 2026-10-26: every amendment in ledger order.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_26.py

The editorial amendments of STND.DFLT, STND.PROJ, HW.GPU, and HW.QPU come first, since they drop the citations
of the provisions that STND.HARN 1.4 withdraws; no state of the round cites a withdrawn identifier. STND.DRAFT
and STND.IDENT follow. Last come the five transactions that pin KNOW, TAG, _PROJECT, STND/_doc.md, and README.md
(decision 4), each with its own scope, which need STND.HARN 1.4 and a harness that accepts a file as a scope.
The lead sets each transaction's time here, the time at which it is applied.
"""
from __future__ import annotations

import importlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = ["apply_dflt_1_5_2", "apply_proj_1_2_1", "apply_hw_remote_1_0_2", "apply_harn_1_4", "apply_draft_1_5",
         "apply_ident_1_4", "apply_pins_2026_10_26"]


def _times():
    # The time of application, to the second; the next transaction waits for the next second, the HW module
    # takes two, and the pins five.
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
        if name == "apply_hw_remote_1_0_2":
            next(clock)
        if name == "apply_pins_2026_10_26":
            for _ in range(4):
                next(clock)
        module.apply(root)
