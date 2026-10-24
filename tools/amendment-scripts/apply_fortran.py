"""Rehearsable adoption script: STND.FTN 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_fortran as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.FTN, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's order of"
    " standards of 2026-10-24 (Fortran, classic and modern) and the standing directions that each standard be agnostic"
    " and timeless: 36 provisions, three binding and 33 defaults, agnostic of compiler, vendor, platform, tool, and"
    " revision of the Fortran standard, citing STND.BUILD, STND.CONC, STND.MPI, and STND.OMP for their general rules."
    " The revision in force of each file and the options of its compiler stated, and no deleted, extended, or"
    " obsolescent form in new or altered statements (STND.FTN.1 to STND.FTN.3); explicit interfaces checked, IMPLICIT"
    " NONE and declared intent, no assumed-size dummies outside fixed interfaces, the aliasing rule of argument"
    " association, and no pointer to a dummy argument used after the return (STND.FTN.4 to STND.FTN.8); no reference"
    " to an undefined value, the SAVE that initialization implies stated, saved and module state protected under"
    " concurrent calls, and one declaration of each common block (STND.FTN.9 to STND.FTN.12); named kinds, literals"
    " written in the kind they meet, explicit conversion of mixed kinds, checked integer range, stated halting modes"
    " and confirmed IEEE support, IEEE tests of non-finite values, and no finite-value option for a file that holds a"
    " required check (STND.FTN.13 to STND.FTN.18); DO CONCURRENT locality and common blocks in OpenMP clauses"
    " (STND.FTN.19 and STND.FTN.20); the Fortran binding of MPI recorded, ASYNCHRONOUS buffers and the"
    " synchronization of registers, no array section with a subscript triplet as a nonblocking buffer without"
    " support, and MPI datatypes by kind (STND.FTN.21 to STND.FTN.24); unit numbers from one place and no reliance on"
    " the order of parallel output (STND.FTN.25 and STND.FTN.26); C interfaces with the BIND attribute and tests"
    " across C descriptors (STND.FTN.27 and STND.FTN.28); the responses to a listed failure, statuses answered,"
    " untrusted subscripts tested in the code, and halts by ERROR STOP (STND.FTN.29 to STND.FTN.32); a legacy list"
    " that only shrinks and modernizing changes verified, with replacements that are able to change results made"
    " apart (STND.FTN.33 and STND.FTN.34); and run-time checks and a run that halts at floating-point exceptions"
    " (STND.FTN.35 and STND.FTN.36). STND.FTN.29, STND.FTN.30, and STND.FTN.31 instantiate PRIME.4 and bind at every"
    " class; none raises the floor (GOV.11), since each asks only a response that PRIME.4 requires or the check that"
    " STND.CODE.6 makes unremovable, and the reach of the term Untrusted input for Fortran is the custodian's"
    " decision at this ratification. Transition (GOV.42): none, because no project instrument cites a draft of it;"
    " existing source enters the legacy list at the change that adopts the standard. Review of STND.HARN.28 by the"
    " command pairs and by reading, a cold review, a pair review, and a verification of draft 0.2; record"
    " review-records/round-2026-10-24/fortran/. The review found no conflict and no matter left without an owner in"
    " a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_FTN:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/FTN"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
