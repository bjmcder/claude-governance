"""Rehearsable round: MNEM gains PERF and STND.PERF 1.0 is adopted; then MNEM gains TEST after PERF, STND.TEST 1.0
is adopted, and STND.WPROC 1.1 and STND.CREW 1.1 cite it (six transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_crew_1_1  # noqa: E402
import apply_mnem_perf  # noqa: E402
import apply_mnem_test  # noqa: E402
import apply_perf  # noqa: E402
import apply_test  # noqa: E402
import apply_wproc_1_1  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_perf.apply(root)
    apply_perf.apply(root)
    apply_mnem_test.ROW_AFTER = apply_mnem_perf.ROW
    apply_mnem_test.apply(root)
    apply_test.apply(root)
    apply_wproc_1_1.apply(root)
    apply_crew_1_1.apply(root)
