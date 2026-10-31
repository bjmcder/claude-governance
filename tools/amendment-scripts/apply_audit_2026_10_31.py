"""Rehearsable round of 2026-10-31 on the cleanup audit: every amendment that carries its corpus findings.

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_audit_2026_10_31.py

The parts run in the order lvl0, tech, process: the constitution first, since both other parts cite its new text;
then the profiles and technical standards; then the process standards and AGENT, which conform to the new LVL0.
Each module sets TRANSACTIONS, the number of ledger transactions it records; the lead gives each its time of
application, a second apart.

A part not yet written is skipped. The variable PARTS, a comma-separated list of module names, limits the run to
those modules, in the order of ORDER, so that a part in drafting is rehearsed on top of the finished parts alone.
"""
from __future__ import annotations

import importlib
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ORDER = [
    "apply_audit_lvl0_2026_10_31",  # LVL0: S1 to S3, R1, R3, R5, R8, R9, B2, B3, B10, I1, I3 to I5
    "apply_audit_tech_2026_10_31",  # profiles and technical standards: S7, S8, B8, O3, I2, I6, I7
    "apply_audit_process_2026_10_31",  # process standards and AGENT: R1, R3, R4, R6, R10, B3, B9, O5 to O7, I1, I9
]


def _times():
    last = None
    while True:
        now = datetime.now(timezone.utc).replace(microsecond=0)
        while last is not None and now <= last:
            time.sleep(0.2)
            now = datetime.now(timezone.utc).replace(microsecond=0)
        last = now
        yield now


def apply(root: Path) -> None:
    root = Path(root)
    clock = _times()
    chosen = os.environ.get("PARTS")
    names = [n for n in ORDER if chosen is None or n in chosen.split(",")]
    for name in names:
        if not (Path(__file__).resolve().parent / f"{name}.py").exists():
            continue
        module = importlib.import_module(name)
        start = next(clock)
        module.AT = start.isoformat()
        module.apply(root)
        for _ in range(getattr(module, "TRANSACTIONS", 1)):
            next(clock)
