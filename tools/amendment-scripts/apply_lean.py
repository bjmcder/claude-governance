"""Rehearsable adoption script: STND.LEAN 1.0 (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_lean as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.LEAN, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's order of standards"
    " of 2026-10-24, which names a standard for Lean, and the custodian's standing directions that each standard be"
    " agnostic of platform, compiler, vendor, implementation, framework, and tool, and timeless. In the drafters'"
    " design, the standard holds the practice of work in Lean, as a proof assistant whose checked proofs the work"
    " relies on as evidence and as a programming language, agnostic of Lean toolchain release, library revision,"
    " checker, tactic, and tool, and cites VV, DSGN, AGENT, STND.CODE, STND.DEPS, STND.DOCS, and STND.VVUQ for what"
    " they hold: 31 provisions, of which 2 are binding and 29 are defaults. No theorem whose axiom"
    " inventory holds a placeholder reported as proved, and a report of a proof resting on a check of each declaration"
    " on which the theorem depends other than those of the Lean toolchain, or naming those its check did not cover, binding"
    " (STND.LEAN.5, PRIME.2); each condition that PRIME.4 lists answered by a result of a type that carries it, by"
    " an error raised in a monad whose caller receives it, by a halt with a diagnosis,"
    " by the designed safe state, or by visible degradation with a diagnosis, binding (STND.LEAN.25, PRIME.4). Both"
    " ask only what PRIME.2 and PRIME.4 already require, at the cost of their wording and one sentence of a report,"
    " so neither raises the floor (GOV.11). The Lean toolchain, each checker, and"
    " each Lean package pinned and used unchanged, upgrades rebuilt from source with their checks repeated, and a"
    " relied-on theorem accepted again by a checker free of a published soundness defect, or the record stating that"
    " none was available (STND.LEAN.1 to"
    " STND.LEAN.3); the record of each claim that rests on a relied-on theorem, the status of a proof, the axiom"
    " inventory checked against an accepted axiom list of logical axiom declarations, axioms that the human owner"
    " declared under VV.9, and recorded native evaluation, and statements held for later proof as definitions"
    " (STND.LEAN.4 to STND.LEAN.8); trusted statements held apart from their proofs, compared with the proved type in"
    " a process apart from the build, reviewed against a table of hazards with implicit variables declared, and shown"
    " not to be vacuous (STND.LEAN.9 to STND.LEAN.13); native evaluation avoided or recorded, the Lean environment"
    " replayed apart from the build, and an independent checker, where the means of the work include one, for"
    " safety-related components (STND.LEAN.14 to"
    " STND.LEAN.16); total definitions under claims, replaced implementations stated and tested, the link between a"
    " theorem and the code that runs stated with what it trusts, and separate implementations compared with their"
    " Lean models (STND.LEAN.17 to STND.LEAN.20); proofs from untrusted authors checked against fixed criteria in a"
    " process that runs none of their code, and review of a proof's correctness by checks set before the change"
    " (STND.LEAN.21 and STND.LEAN.22); the floating-point model and rounding bound stated, and truncating operations"
    " and substituted values kept off the path of a result (STND.LEAN.23 and STND.LEAN.24); listed failures, unsafe"
    " and replaced code explained, and naming by the repository configuration with names of the documented notation"
    " kept (STND.LEAN.25 to STND.LEAN.27); and raised elaboration limits, lemma sets, library definitions reached"
    " through lemmas, and deprecations in builds (STND.LEAN.28 to STND.LEAN.31). Transition (GOV.42): none, because"
    " no project instrument cites a draft of it. Review of STND.HARN.28 by the command pairs and by reading, a cold"
    " review, a pair review, and a verification of each revised draft; record review-records/round-2026-10-24/lean/."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_LEAN:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/LEAN"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
