"""Rehearsable round: MNEM gains TEST, STND.TEST 1.0 is adopted, and STND.WPROC 1.1 and STND.CREW 1.1 cite it
(four transactions)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_crew_1_1  # noqa: E402
import apply_mnem_test  # noqa: E402
import apply_test  # noqa: E402
import apply_wproc_1_1  # noqa: E402


def apply(root: Path) -> None:
    apply_mnem_test.apply(root)
    apply_test.apply(root)
    apply_wproc_1_1.apply(root)
    apply_crew_1_1.apply(root)
