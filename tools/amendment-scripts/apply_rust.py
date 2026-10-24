"""Rehearsable adoption script: STND.RUST 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_rust as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.RUST, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's standing"
    " directions that standards be platform, compiler, vendor, implementation, framework, and tool agnostic and hold"
    " timeless practice, and on the directions on determinism (STND.VVUQ.82, STND.VVUQ.83): 34 provisions, agnostic"
    " of toolchain release, citing STND.CONC for every model-neutral rule of concurrency, STND.CODE and STND.DEPS for"
    " what they hold, and STND.BUILD for the rules of building. The edition and oldest toolchain declared, and tests at"
    " the oldest and the production release with a non-blocking check at the newest (STND.RUST.1); the panic strategy,"
    " overflow checks, debug assertions, target features, and crate features of each reporting build stated among the"
    " settings of STND.BUILD.11 (STND.RUST.2); a soundness argument at each unsafe construct and the soundness"
    " conditions of each unsafe function and trait (STND.RUST.3); sound modules (STND.RUST.4); the modules that hold"
    " unsafe code listed and unsafe code elsewhere rejected by a check (STND.RUST.5); an agent writes the soundness"
    " argument and conditions of the unsafe code that it writes or changes, binding (STND.RUST.6, GOV.48); no"
    " argument resting on a destructor, a poisoned lock, or the absence of a panic in code that the module does not"
    " define (STND.RUST.7); the panic strategy relied upon stated and tested (STND.RUST.8); panic safety of unsafe"
    " code (STND.RUST.9); panics caught only at boundaries, with a diagnosis (STND.RUST.10); destructors without"
    " panics and release operations that return failures (STND.RUST.11); locks after a panic (STND.RUST.12); the"
    " Rust responses to a condition that PRIME.4 lists, a replaced panic hook or a handler that delivers a diagnosis"
    " of each panic that no other response answers, and no record through a logging interface as the only visible"
    " degradation, binding (STND.RUST.13, PRIME.4); each function that returns a listed failure declared so that the"
    " compiler or a static check diagnoses an ignored result, binding (STND.RUST.14, PRIME.4); no check of untrusted"
    " input, or that CPS.5 or CPS.9 requires, in a form that an execution setting removes, and overflow detected by"
    " an operation or a range check that every build keeps, binding (STND.RUST.15, PRIME.4); returned results for"
    " failures that a caller handles, documented panics and errors, and a reason at each unwrap (STND.RUST.16,"
    " STND.RUST.17); explicit integer arithmetic and narrowing conversions (STND.RUST.18, STND.RUST.19); tests with"
    " overflow checks and debug assertions, and once in the reporting build (STND.RUST.20); manual implementations of"
    " Send and Sync argued and bounded (STND.RUST.21); cancellation safety stated and state kept at each suspension"
    " point (STND.RUST.22); guards and checked borrows held across an await reported (STND.RUST.23); layout, unwinding,"
    " and ownership at foreign function interfaces (STND.RUST.24 to STND.RUST.27); build scripts of dependencies"
    " recorded and reviewed, additive crate features, and committed lock files with the exception of STND.JL.4"
    " (STND.RUST.28, STND.RUST.29, STND.RUST.30); and static checks, undefined behavior detected in tests where the"
    " means exist, the limits of those checks stated, and each claim of soundness in a report, a record of a result or"
    " of a release, or a review stating the means that checked it and the code that they covered, binding"
    " (STND.RUST.31 to STND.RUST.34; STND.RUST.34, PRIME.2). STND.RUST.13, STND.RUST.14, and STND.RUST.15 ask only"
    " for responses and checks that PRIME.4, STND.CODE.6, CPS.5, and CPS.9 already require, at the cost of a"
    " diagnosis that a replaced hook keeps, one attribute, return type, or check for each function that returns a"
    " listed failure, and the choice of a form of check that every build keeps; STND.RUST.34 asks of a claim on which"
    " others rely only what PRIME.2 already requires, at the cost of one sentence; and STND.RUST.6 costs an agent one"
    " comment at each construct that it writes or changes; so none raises the floor (GOV.11). Transition (GOV.42):"
    " none, because no project instrument cites a draft of it. Review of STND.HARN.28 by the command pairs and by"
    " reading, a cold review, a pair review, and a verification of each revised draft; record"
    " review-records/round-2026-10-24/rust/. The review found no conflict and no matter left without an owner in a"
    " shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_RUST:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/RUST"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
