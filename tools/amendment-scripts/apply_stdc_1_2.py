"""Rehearsable minor amendment: STND.STDC 1.2, round of 2026-10-27 (decision 1).

One transaction. STND.STDC.36 is withdrawn, its outcome being STND.CODE.22 and STND.CODE.23 for every language;
Terms import Foreign interface from STND.CODE and drop this standard's own definition; the Notes cite STND.CODE
in place of STND.CXX.20, STND.CXX.22, and STND.STDC.36. Runs after STND.CODE 1.3 and before STND.CXX 1.3. Run
from harness/:
    python3 -B -m govharness rehearse <corpus holding STND.CODE 1.3> ../tools/amendment-scripts/apply_stdc_1_2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T12:00:05+00:00"

SWAPS = [
    ("signal handlers and bit-fields shared between threads (STND.STDC.33, STND.STDC.34, and STND.STDC.35), data "
     "that crosses to other languages (STND.STDC.36), the checks of C code",
     "signal handlers and bit-fields shared between threads (STND.STDC.33, STND.STDC.34, and STND.STDC.35), the "
     "checks of C code"),
    ("Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, and "
     "High-assurance coding standard have the meanings that STND.CODE gives them.",
     "Repository configuration, Static check, Execution setting, Untrusted input, High-assurance code, "
     "High-assurance coding standard, and Foreign interface have the meanings that STND.CODE gives them."),
    ("| Foreign interface | Of C source: an interface through which C source calls, or is called by, code written "
     "in another language; a callback or a thread that a runtime of another language starts in C source; or a "
     "structured block of a compiler directive for parallel execution. |\n", ""),
    ("STND.CXX.5 and STND.CXX.20 rest on destructors and resource handles,",
     "STND.CXX.5 rests on destructors and resource handles,"),
    ("STND.CXX.22 binds the C++ side of a boundary; c1 leaves unverified that the ISO C standard defines a nonlocal "
     "jump only within C frames, so no provision binds the C side,",
     "STND.CODE.24 binds the side of a boundary whose language propagates a failure by a mechanism of its own, an "
     "exception or a panic; c1 leaves unverified that the ISO C standard defines a nonlocal jump only within C "
     "frames, so no provision binds the C side for such a jump,"),
    ("which STND.STDC.36 has the contract state;", "which STND.CODE.23 has the contract state;"),
    ("STND.STDC.7 and STND.STDC.36 rest on DSGN.4 and the first sentence of STND.STDC.29 on DSGN.5,",
     "STND.STDC.7 rests on DSGN.4 and the first sentence of STND.STDC.29 on DSGN.5,"),
]

READING = (
    "STND.STDC.36 is withdrawn, its outcome being STND.CODE.22 and STND.CODE.23 for every language, and the front "
    "matter lists it as withdrawn; Terms import Foreign interface from STND.CODE and drop this standard's own "
    "definition; the Purpose drops STND.STDC.36; the Notes cite STND.CODE.23 and STND.CODE.24 in place of "
    "STND.STDC.36 and STND.CXX.22, and drop STND.CXX.20 from the provisions of STND.CXX that do not carry to C")
ROW = f"| 1.2 | {F.DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.STDC, revision 1.2, ratified by the custodian on {F.DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it removes a provision and alters a defined meaning. The custodian decided "
    "that the shared rules on foreign interfaces move to STND.CODE and that the provisions they cover wholly are "
    "withdrawn (decision 1). C source keeps the outcome of STND.STDC.36 through STND.CODE.22, whose width and layout "
    "fixed by the contract are its size, alignment, and representation, and through STND.CODE.23, which keeps the "
    "order of dimensions and the origin of indexes in the contract and admits a test of the call in place of their "
    "statement there. The term of STND.CODE covers the three parts of the term of this standard: code written in "
    "another language, a callback or a thread that its runtime starts, and a structured block of a compiler "
    "directive for parallel execution. STND.CODE.25 and STND.CODE.26 now reach C source, which no provision of "
    "this standard reached; they are defaults and raise no floor (GOV.11). The withdrawn identifier is listed in "
    "the field withdrawn and is never given to another provision (STND.IDENT.14). Class onsets: STND.CODE.22 and "
    "STND.CODE.23 apply from CSQ2, as STND.STDC.36 did. Transition (GOV.42): none. "
    f"Decision 1 of {F.RECORD}." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    F.withdraw(root, "STND/STDC", "STND.STDC", [36])
    replace_text(root, "STND/STDC/_doc.md", SWAPS)
    F.finish(root, "STND/STDC", "STND.STDC", "1.1", "1.2", ROW, RATIONALE, AT)
