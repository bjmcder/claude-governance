"""Rehearsable adoption script: STND.CXX 1.0 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content_cxx as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-23T11:33:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.CXX": "Adoption of STND.CXX, revision 1.0, ratified by the custodian on " + C.DATE + ", with the custodian's"
 " rulings of 2026-10-23: 31 provisions on the coding practice specific to C++, platform and compiler agnostic,"
 " naming no version, compiler, platform, library dependency, or tool. The C++ Core Guidelines at a recorded"
 " revision as the reference (STND.CXX.1); the newest edition that every compiler and standard library of a unit's"
 " toolchain matrix documents as supported, later features one at a time, and review of the edition with the"
 " pinned revisions (STND.CXX.2); no lowering of an edition, and no new unit below the edition of STND.CXX.2 or its"
 " project alternative, by an agent without a decision record, binding on agents (STND.CXX.3, GOV.48); the edition,"
 " extensions, and floating-point options stated in the build (STND.CXX.4); ownership, with owning raw pointers"
 " marked by a type alias that the checks recognize, sequences, and device and register memory (STND.CXX.5,"
 " STND.CXX.6, STND.CXX.7); the standard library first, implementation-defined library behavior, and header-only"
 " libraries whose template definitions stay visible (STND.CXX.8, STND.CXX.9, STND.CXX.10); constrained generic"
 " code, compile-time checking, and documented metaprogramming facilities (STND.CXX.11, STND.CXX.12, STND.CXX.13);"
 " naming and declaration comments (STND.CXX.14, STND.CXX.15); the responses to a failure that PRIME.4 lists,"
 " failure results diagnosed when ignored, and the checks of CPS.5 and CPS.9 kept in every build where those apply,"
 " binding at every class (STND.CXX.16, STND.CXX.17, STND.CXX.18, PRIME.4); the failure channel, foreign resource"
 " handles, status and release failures, C++ exceptions at foreign boundaries, synchronization, and compiler"
 " assumptions (STND.CXX.19, STND.CXX.20, STND.CXX.21, STND.CXX.22, STND.CXX.23, STND.CXX.24); static checks,"
 " run-time error detection, and library precondition checks (STND.CXX.25, STND.CXX.26, STND.CXX.27); and for"
 " high-assurance code, the code that a release of work of CSQ1 or CSQ0 delivers or runs to produce a reported"
 " result, conformance to the high-assurance coding standard that a decision record of the work adopts, required"
 " for the safety-related components of CSQ0 and recommended elsewhere (STND.CXX.28), claims of conformance limited"
 " to what was checked, binding (STND.CXX.29, PRIME.2), an edition that the adopted standard covers and the"
 " toolchain is validated or qualified for (STND.CXX.30), and recorded deviations (STND.CXX.31). The custodian rules"
 " that STND.CXX.3, STND.CXX.16, STND.CXX.17, and STND.CXX.18 raise no floor (GOV.11, PRIN.10); STND.CXX.29 adds"
 " to PRIME.2 only the naming of the means that checked a claim and reaches only high-assurance code, and the custodian rules at ratification that it raises no floor. Transition (GOV.42): none. Review of STND.HARN.28"
 " by the command pairs and by reading, a cold review, a pair review, and cold verifications; record "
 "claude/drafts/review-records-ledger100-105.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/CXX"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS_CXX:
        adopt(Path(root), d)
