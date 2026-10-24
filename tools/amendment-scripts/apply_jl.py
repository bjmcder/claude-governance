"""Rehearsable adoption script: STND.JL 1.0 from draft 0.4 (one transaction, after apply8 and apply9)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content_jl as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-23T11:35:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.JL": "Adoption of STND.JL, revision 1.0, ratified by the custodian on " + C.DATE + ": 35 provisions on source written in Julia, drafted from the custodian's direction 'for Julia, refer to https://docs.julialang.org/en/v1/. use the latest version available' and from the research note of 2026-10-22, with the Julia manual of the reference version as the baseline and each departure from it stated with its reason: a reference version that is the latest stable minor version consistent with the rest of the environment, with qualified revisions kept, and no version, interval, package, or tool named, under the custodian's rulings of 2026-10-23; bounded [compat] entries with the Julia floor at the reference version; checks on the latest patch release of the reference or on a qualified revision, on the earliest admitted version, and, without gating, on the newest stable release and prerelease; committed manifests for work that reports results; recorded run settings; the naming conventions of Blue Style with notation names kept; ! for functions that change an argument; declared public interfaces, explicit imports, and no type piracy; type-stable numerical kernels; failures; scoped subnormal and BigFloat settings; stated comparison tolerances under STND.VVUQ; generators through the interface, seeded at entry points, with parallel streams under STND.VVUQ.62; values that Julia does not keep across versions; shared state between tasks; the manual's docstring layout with fixed headings and doctests; and checks for docstring coverage, package hygiene, test runs with bounds checks forced apart from one run in the production configuration, and deprecation warnings that fail test runs. STND.JL.13, STND.JL.14, and STND.JL.15 instantiate PRIME.4 and bind at every class: no @assert or @boundscheck for checks of untrusted input and an index check that no execution setting removes; a condition that PRIME.4 lists answered by a throw, a halt with a diagnosis, the designed safe state, a visible degradation with a diagnosis, or a returned condition, a log record counting only at the levels Warn and Error; and the same response from a catch block that receives OutOfMemoryError or StackOverflowError. Every other provision is a default from CSQ3. The custodian's rulings of 2026-10-23 hold that the binding provisions and the reach of Untrusted input raise no floor, and keep the underscore naming, the manual's docstring headings, and the Warn and Error log rule. Transition (GOV.42): existing Julia source conforms to the defaults when a change next touches it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and cold verifications; record claude/drafts/review-records-ledger100-105.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/JL"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS_JL:
        adopt(Path(root), d)
