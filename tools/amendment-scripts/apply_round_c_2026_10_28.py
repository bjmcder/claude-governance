"""Round c of 2026-10-28: classes, the expected class, promotion, and the human round trips below CSQ2 (rulings C1
to C6 and C8; register entries R2.2 to R2.7, R3.1 to R3.4, R7.3).

Twenty-one transactions, one per document, in citation order:
- LVL0 1.7 (minor, GOV.40): GOV.13 sets the class at inception from the uses then made, records a planned more
  severe use as the expected class, and has unclassified work meet the floor until an agent needs the class to
  promote, release, deploy, or drive hardware (C1); QA.11 makes the adopted classification the promotion of each
  result relied upon within the CSQ3 test of GOV.12 (C5); the Lexicon defines Expected class and Reclassification.
- STND.CLASS 1.4: the expected class (STND.CLASS.5), the money threshold from CSQ2 (STND.CLASS.3), design for the
  expected class (new STND.CLASS.21), what a reclassification owes (new STND.CLASS.22, STND.CLASS.19), the records
  kept below the expected class (new STND.CLASS.23, STND.CLASS.10), the CSQ3 reliance test (STND.CLASS.1), who
  counts as another actor (STND.CLASS.18), and the reassessment (STND.CLASS.7).
- STND.PROJ 1.4: the Classification row holds the expected class.
- STND.CODE 1.5: the deviation record of STND.CODE.20 from CSQ1, the marker earlier; the Notes cite STND.CLASS.21.
- HW 1.2 and its six sub-profiles at 1.1: one selector attribute (CS9); HW.19, HW.21, and HW.CPU.5 report into the
  record of an unattended run (CS8); the HW Notes cite STND.CLASS.21.
- NUMER 1.4: NUMER.18 reports into the record of an unattended run (CS8).
- STND.CONC 1.1.2 (editorial): the Notes cite STND.CLASS.21.
- AGENT 1.3: AGENT.39 accepts an effort estimate that states its basis (CP8); AGENT.23 accepts an unedited session
  transcript (CC19).
- STND.CREW 1.2: STND.CREW.3 (CP20), STND.CREW.10 (CP11), STND.CREW.23 (CP14, R7.3).
- STND.THRT 1.1: STND.THRT.6 proposes in the next report (CC22).
- STND.WPROC 1.2: a branch drawn on only within development is not a main line (CP16).
- STND.JL 1.4.1, STND.PY 1.3.1, STND.RUST 1.3.1, STND.STDC 1.3.1 (editorial): the Notes cite STND.CLASS.22.
PRIME.13 is unchanged: the human owner still adopts each revision of the hazard analysis (CS13).

Run from harness/, through the driver, on top of the finished rounds:
    ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28,apply_round_c_2026_10_28 \\
        python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import round_c_class as C  # noqa: E402
import round_c_rest as R  # noqa: E402

AT = "2026-10-28T21:00:00+00:00"

STEPS = [
    C.apply_lvl0, C.apply_class, C.apply_proj,
    R.apply_code, R.apply_hw, *R.subprofile_steps(), R.apply_numer, R.apply_conc,
    R.apply_agent, R.apply_crew, R.apply_thrt, R.apply_wproc, *R.lang_steps(),
]
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, step in enumerate(STEPS):
        step(root, (start + timedelta(seconds=k)).isoformat())
