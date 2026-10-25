"""Rehearsable round of 2026-10-25: STND.PERF and STND.TEST, with STND.WPROC 1.1 and STND.CREW 1.1.

Run from harness/, so that govharness imports:
    python -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_25.py

The order matters: STND.PERF before STND.TEST, whose Notes cite it; STND.TEST before STND.WPROC 1.1 and
STND.CREW 1.1, which cite it. The lead sets each transaction's time here, the time at which it is applied,
and chains the mnemonic rows in the order of adoption; the individual scripts keep their placeholder times
for their own rehearsals.
"""
from __future__ import annotations

import importlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# (mnemonic script, adoption script); the mnemonic rows are chained after LEAN in this order.
STANDARDS = [("apply_mnem_perf", "apply_perf"), ("apply_mnem_test", "apply_test")]
AMENDMENTS = ["apply_wproc_1_1", "apply_crew_1_1"]


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
    after = importlib.import_module("apply_mnem_perf").ROW_AFTER

    def run(name: str) -> None:
        module = importlib.import_module(name)
        module.AT = next(clock)
        module.apply(root)

    for mnem, doc in STANDARDS:
        module = importlib.import_module(mnem)
        module.ROW_AFTER = after
        module.AT = next(clock)
        module.apply(root)
        after = module.ROW
        run(doc)
    for name in AMENDMENTS:
        run(name)
