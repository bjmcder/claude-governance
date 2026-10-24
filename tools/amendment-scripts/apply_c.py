"""Rehearsable adoption script: STND.STDC 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_c as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.STDC, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's order of"
    " standards of 2026-10-24, which names a standard for C, and the custodian's standing directions that each"
    " standard be agnostic of platform, compiler, vendor, implementation, framework, and tool, and timeless. In the"
    " drafters' design, the standard holds the practice specific to C, modeled on STND.CXX in the form of STND.PY and"
    " STND.JL, agnostic of compiler, edition, platform, implementation, and tool:"
    " 38 provisions, citing STND.CODE, STND.CONC, STND.DEPS, STND.DOCS, STND.BUILD, and NUMER for what they hold."
    " The provisions of STND.CXX whose outcome holds for C apply to C source in a C reading that the Terms define,"
    " at the revision of STND.CXX in force: the defaults STND.CXX.4, STND.CXX.7, STND.CXX.9, STND.CXX.12, STND.CXX.15,"
    " STND.CXX.23, STND.CXX.24, STND.CXX.25, STND.CXX.26, STND.CXX.27, STND.CXX.28, STND.CXX.30, and STND.CXX.31, each row from the class that its table gives and replaceable alone (STND.STDC.1); and, binding,"
    " the responses to a listed failure other than a C++ exception, with no report through errno alone, failure"
    " results that the compiler or a static check diagnoses when ignored where the means of the work include one,"
    " checks that no option removes, and claims"
    " of conformance to a high-assurance coding standard limited to what was checked (STND.STDC.2, the C reading of"
    " STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29; PRIME.4, PRIME.2). The standard sets no edition for C;"
    " a change that lowers the edition of a unit carries a decision record (STND.STDC.3), and each conditional feature"
    " that a unit uses is tested (STND.STDC.4). Release of owned resources on every path without destructors, release"
    " functions named, extents passed with pointers, accesses within their object and its lifetime, and"
    " initialization and padding set before reads and output (STND.STDC.5 to STND.STDC.10); signed overflow, division"
    " and shifts, guards, aliasing, and unsequenced accesses shown safe, and correctness independent of options that"
    " define undefined behavior, tested in a build named apart under STND.BUILD.13 (STND.STDC.11 to STND.STDC.16);"
    " conversions and sizes (STND.STDC.17, STND.STDC.18); bounded and terminated writes, truncation reported, lengths"
    " from untrusted input checked, and format strings checked, by a static check where the means of the work include"
    " one (STND.STDC.19 to STND.STDC.22); macros, their hygiene,"
    " and conditional compilation under check (STND.STDC.23 to STND.STDC.25); restrict contracts and bounded"
    " variable-length arrays (STND.STDC.26, STND.STDC.27); streams flushed or closed with their failures tested and"
    " answered, library failure results diagnosed where the means of the work include a diagnosis, release failures"
    " tested, the channel of failure, and errno"
    " (STND.STDC.28 to STND.STDC.32); signal handlers and adjacent bit-fields shared between threads (STND.STDC.33 to"
    " STND.STDC.35); data crossing to other languages (STND.STDC.36); and compiler warnings, detected kinds of"
    " undefined behavior, and stated limits of analysis (STND.STDC.37, STND.STDC.38). STND.STDC.2 asks only for"
    " outcomes that PRIME.4 and PRIME.2 already require, at the cost of a response that PRIME.4 asks, one attribute"
    " per function where the edition or the toolchain provides one and otherwise a static check, one choice of"
    " compiler option for a unit that holds a required check, the naming of the means that checked a claim of"
    " conformance, and a return value in place of errno alone for a listed condition, and so raises no floor"
    " (GOV.11); the rulings made for STND.CXX.16, STND.CXX.17, STND.CXX.18, and STND.CXX.29 concern C++, and the"
    " custodian rules at ratification that their extension to C, with the errno clause and the static check where no"
    " attribute exists, raises no floor. Transition (GOV.42): none, because no project instrument cites a draft of it."
    " Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and a verification;"
    " record review-records/round-2026-10-24/c/. The reviews found no conflicting pair and no matter left without an"
    " owner in a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_STDC:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/STDC"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
