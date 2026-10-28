"""Round e of 2026-10-28: the harness's place in the corpus, the LVL0 and process cleanups, and the rest (ruling E1;
the smaller entries under ruling F1: register entries R5.1, R5.3, R6.1, R6.4, R7.1, and R7.2, with AD9; the copies
that round d left; the residual of CS9 that round c left).

Thirty-five transactions, one per document, in citation order:
- STND.HARN: STND.HARN.24 and STND.HARN.28 as outcomes that a reader checks with or without a harness, the pairs
  narrowed to those on a shared matter and those of common instantiation within the change (E1, HR-12, CP7, CP23);
  the Purpose names the transactions that a harness enters (CP22).
- LVL0 (editorial, GOV.40) and AGENT (editorial): each rule kept once and cited elsewhere (CC23 to CC26, CC31).
- STND.DOCS, then STND.DRAFT: one spelling table, in STND.DOCS.8 (CP26); STND.DRAFT.10 reaches governance (CP27).
- STND.WFLOW (CP13), STND.WPROC (CP26, CP15), STND.IDENT (CP28), STND.INSTR (AD9), STND.VVUQ (CP17, CP25),
  STND.MPI (CS21), HDES (CS20), HDES.ASIC (CS22), the root document STND (CP24, a pin of its file by GOV.36).
- STND.PROJ (CC20; the execution paths leave the classification, the residual of CS9), then HW and its six
  sub-profiles, then STND.CLASS (CC30), which cites STND.PROJ.2; STND.PERF (CS17).
- STND.FTN (CL19, CL20); STND.DEPS (one default for checks across declared ranges, CL7; CL20); STND.CODE (CL19);
  STND.BUILD; STND.SV, STND.STDC, STND.LEAN, and STND.CXX withdraw the copies of STND.CODE.21 and STND.CODE.28 after
  every citing document drops them; STND.JL (CL7, CL22); STND.RUST (CL7, CL9); STND.PY withdraws STND.PY.14 last.

Run from harness/, through the driver, on top of the finished rounds:
    ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28,apply_round_c_2026_10_28,\\
apply_round_o_2026_10_28,apply_round_e_2026_10_28 python3 -B -m govharness rehearse governance \\
../tools/amendment-scripts/apply_rounds_2026_10_28.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import round_e_base as E  # noqa: E402
import round_e_code as C  # noqa: E402
import round_e_harness as H  # noqa: E402
import round_e_process as P  # noqa: E402

AT = "2026-10-28T23:00:00+00:00"


def step(item):
    """Return a callable of (root, at) for a Step or a function that records its own transaction."""
    if isinstance(item, E.Step):
        return lambda root, at: E.run(root, item, at)
    return item


STEPS = [step(x) for x in [
    H.HARN, H.apply_lvl0, H.AGENT,
    *P.STEPS, P.apply_stnd, *P.LATER,
    *C.STEPS,
]]
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, run in enumerate(STEPS):
        run(root, (start + timedelta(seconds=k)).isoformat())
