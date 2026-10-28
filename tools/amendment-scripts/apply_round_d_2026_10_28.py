"""Round d of 2026-10-28: ruling D1 and the restatement cleanups of the code and systems standards (R6.2, R6.3).

Fifteen transactions, one per document, in citation order:
- STND.CODE 1.4 and STND.DEPS 1.2 add the provisions for every language that the language standards then cite;
  STND.BUILD 1.0.3 follows STND.CODE at once, so that its Notes describe STND.CODE.21 as binding;
- STND.CONC 1.1.1 drops its citations of STND.PY.17, STND.JL.24, and STND.MPI.18, .19, and .24;
- STND.PERF 1.1 drops the carve-out of STND.PERF.12 before STND.OFFLD 1.2 drops the second sentence of
  STND.OFFLD.31, so that no state leaves the costs of first use of offloaded work unstated;
- STND.MPI 1.1 withdraws STND.MPI.18, .19, and .24 for STND.CONC.21, .22, and .24;
- STND.OMP 1.0.4 drops the revision numbers of its Notes;
- STND.FTN 1.2, STND.LEAN 1.1, STND.CXX 1.4, STND.STDC 1.3, STND.JL 1.4, and STND.PY 1.3 drop their copies and
  their citations of the provisions that later documents withdraw; STND.RUST 1.3 comes last, after STND.CODE,
  STND.DEPS, STND.CXX, and STND.PY drop their citations of STND.RUST.13 and STND.RUST.30.
No state of the round cites a withdrawn identifier. STND.CXX.18, STND.STDC.39, STND.STDC.40, STND.LEAN.27, and
STND.PY.14 stay, because the Notes of STND.BUILD or STND.SV cite them (round e); STND.RUST.34 stays, binding
STND.CODE.34 for Rust. Run from harness/:
    ROUNDS=apply_round_d_2026_10_28 python3 -B -m govharness rehearse governance \\
        ../tools/amendment-scripts/apply_rounds_2026_10_28.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import round_d_code as C  # noqa: E402
import round_d_langs as L  # noqa: E402
import round_d_systems as S  # noqa: E402

AT = "2026-10-28T12:00:00+00:00"

STEPS = [
    C.apply_code, S.apply_build, C.apply_deps,
    S.apply_conc, S.apply_perf, S.apply_offld, S.apply_mpi, S.apply_omp,
    L.apply_ftn, L.apply_lean, L.apply_cxx, L.apply_stdc, L.apply_jl, L.apply_py, L.apply_rust,
]
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, step in enumerate(STEPS):
        step(root, (start + timedelta(seconds=k)).isoformat())
