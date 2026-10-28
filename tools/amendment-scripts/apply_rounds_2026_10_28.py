"""Rehearsable rounds of 2026-10-28: every amendment that carries the custodian's rulings on the deep review.

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py

The rounds run in the order of ruling F2: the defaults and instruction authority, then the language and systems
standards, then classes and promotion, then the onset rule, then the harness's place in the corpus and the rest.
Each module sets TRANSACTIONS, the number of ledger transactions it records; the lead gives each its time of
application, a second apart.

A round not yet written is skipped. The variable ROUNDS, a comma-separated list of module names, limits the run to
those modules, in the order of ORDER, so that a round in drafting is rehearsed on top of the finished rounds alone.
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
    "apply_round_a_2026_10_28",  # A1 to A5, B1, B2, and the smaller entries of the defaults and instructions
    "apply_round_d_2026_10_28",  # D1 and the restatement cleanups of the code and systems standards
    "apply_round_c_2026_10_28",  # C1 to C6, C8, and the human round trips of classes and promotion
    "apply_round_o_2026_10_28",  # C7, the onset rule
    "apply_round_e_2026_10_28",  # E1, the harness's place in the corpus, the LVL0 and process cleanups, the rest
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
    chosen = os.environ.get("ROUNDS")
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
