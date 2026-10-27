"""Rehearsable editorial amendments of the round of 2026-10-27: STND.FTN 1.1.1, STND.MPI 1.0.2, STND.OMP 1.0.3.

Three transactions, one per document. Their Notes cite STND.CODE.22 to STND.CODE.26 in place of STND.CXX.20 and
STND.CXX.22, which STND.CXX 1.3 withdraws. They run after STND.CODE 1.3 and before STND.CXX 1.3, so that no state
of the round cites a withdrawn identifier. Run from harness/, after apply_code_1_3.py:
    python3 -B -m govharness rehearse <corpus holding STND.CODE 1.3> ../tools/amendment-scripts/apply_fi_editorial_2026_10_27.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:02+00:00"

FTN = [
    ("STND.CONC holds the rules of concurrency for every model, STND.MPI and STND.OMP the rules of those models, and "
     "STND.CXX.20, STND.CXX.21, and STND.CXX.22 the C++ side of a foreign boundary.",
     "STND.CONC holds the rules of concurrency for every model, STND.MPI and STND.OMP the rules of those models, "
     "STND.CODE.22 to STND.CODE.26 the rules of each foreign interface, and STND.CXX.21 the C++ side of one."),
    ("A test with an array section of a stride other than one exercises the descriptor where errors of stride hide "
     "(STND.FTN.28).",
     "A test with an array section of a stride other than one exercises the descriptor where errors of stride hide "
     "(STND.FTN.28). STND.FTN.27 and STND.FTN.28 give the Fortran forms of STND.CODE.22 and STND.CODE.23."),
]
MPI = [(
    "In C++, an MPI handle is held by a resource handle under STND.CXX.5 and STND.CXX.20, a failed free is reported "
    "under STND.CXX.21, and a C++ exception does not leave a user-defined reduction operation, an error handler "
    "function, or another callback that MPI invokes (STND.CXX.22).",
    "In C++, an MPI handle is held by a resource handle under STND.CXX.5 and STND.CODE.25, and a failed free is "
    "reported under STND.CXX.21. A C++ exception does not leave a user-defined reduction operation, an error handler "
    "function, or another callback that MPI invokes (STND.CODE.24).")]
OMP = [
    ("STND.CXX.22 governs an exception that reaches the boundary of a structured block in C++,",
     "STND.CODE.24 governs an exception that reaches the boundary of a structured block,"),
    ("which STND.OMP.21 admits; STND.CXX.22 governs exceptions.",
     "which STND.OMP.21 admits; STND.CODE.24 governs exceptions."),
]

DOCS = [
    ("STND.FTN", "STND/FTN", "1.1", "1.1.1", FTN,
     "the Notes cite STND.CODE.22 to STND.CODE.26 for the rules of each foreign interface in place of STND.CXX.20 "
     "and STND.CXX.22, which STND.CXX 1.3 withdraws, and name STND.FTN.27 and STND.FTN.28 the Fortran forms of "
     "STND.CODE.22 and STND.CODE.23"),
    ("STND.MPI", "STND/MPI", "1.0.1", "1.0.2", MPI,
     "the Notes cite STND.CODE.25 and STND.CODE.24 in place of STND.CXX.20 and STND.CXX.22, which STND.CXX 1.3 "
     "withdraws, for the resource handle of an MPI handle and for an exception in a callback that MPI invokes"),
    ("STND.OMP", "STND/OMP", "1.0.2", "1.0.3", OMP,
     "the Notes cite STND.CODE.24 in place of STND.CXX.22, which STND.CXX 1.3 withdraws, for an exception that "
     "reaches the boundary of a structured block"),
]


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for n, (doc_id, folder, old, new, swaps, reading) in enumerate(DOCS):
        replace_text(root, f"{folder}/_doc.md", swaps)
        row = (f"| {new} | {F.DATE} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
               "meaning changes. |")
        rationale = (
            f"Editorial amendment of {doc_id}, revision {new}, ratified by the custodian on {F.DATE}: {reading}. The "
            "change is editorial under STND.IDENT.3 because it alters informative Notes only: the outcomes that the "
            "Notes describe are those of the provisions that STND.CODE 1.3 holds in place of the withdrawn ones, so "
            "no obligation, permission, or defined meaning of this document changes. Transition (GOV.42): none. "
            f"Decision 1 of {F.RECORD}." + F.AUTHOR)
        F.finish(root, folder, doc_id, old, new, row, rationale, (start + timedelta(seconds=n)).isoformat())
