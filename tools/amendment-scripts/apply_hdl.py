"""Rehearsable adoption script: STND.SV 1.0, the Verilog and SystemVerilog standard (one transaction)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import content_hdl as C  # noqa: E402
from govharness.workflows.amend import Change, record_transaction  # noqa: E402

AT = "2026-10-24T20:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = (
    "Adoption of STND.SV, revision 1.0, ratified by the custodian on " + C.DATE + ", on the custodian's directions"
    " of 2026-10-24 that a standard hold the practice of Verilog and SystemVerilog for design and for verification,"
    " agnostic of simulator, synthesis tool, checker, vendor, and target and timeless, holding only what these"
    " languages make necessary beside HDES, STND.CODE, STND.CONC, STND.VVUQ, and STND.DEPS, and citing HDES.11 for"
    " clock-domain crossings: 27 provisions, all defaults. The edition in force, the construct subset with the"
    " constructs each tool does not support, the settings of simulation, and verification constructs kept out of the"
    " synthesized set (STND.SV.1 to STND.SV.4); race freedom by construction, with nonblocking assignment for"
    " clocked state that another process reads, one writing process per variable, order from the scheduling of the"
    " language and not from delays, and no verdict that depends on the order at time zero, as the form of the"
    " protection that STND.CONC.3 asks (STND.SV.5 to STND.SV.8); agreement of simulation and synthesis through"
    " constructs that state intent, latches only by decision, checked selection qualifiers, no wildcard on unknown"
    " values, no behavior resting on simulation-only constructs and no directive that changes selection logic,"
    " explicit width and sign, and initial values not counted as evidence under HDES.12 (STND.SV.9 to STND.SV.15);"
    " intended unknown values stated and shown harmless, masked unknown values detected, and the equivalence mode"
    " recorded with the strict mode run and its failures resolved (STND.SV.16 to STND.SV.18); concurrent assertions"
    " for clocked properties that write no design state, the records of assertions and proof assumptions, what"
    " coverage counts on unknown values and what it excludes, and functional coverage from the contract"
    " (STND.SV.19 to STND.SV.22); random streams keyed to parts of the stimulus and derived from the recorded seed,"
    " citing STND.CONC.23, STND.VVUQ.62, and NUMER.24 (STND.SV.23); and the classes of finding of the static checks,"
    " a simulation of the netlist after a check of equivalence, a second simulator or a proof before reliance, and"
    " no comparison between simulators on one seed (STND.SV.24 to STND.SV.27). No provision binds and none raises"
    " the floor (GOV.11): silent saturation and wrap-around bind at every class through HDES.14 and PRIME.4, and the"
    " completion and failure of concurrent tasks of a testbench through STND.CONC.1 and STND.CONC.2, and the"
    " standard adds nothing to that floor. Transition (GOV.42): none, because no project instrument cites a draft"
    " of it. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and a"
    " verification of the revised draft; record review-records/round-2026-10-24/hdl/. The review found no conflict"
    " left unresolved and no matter left without an owner in a shared-matters table."
)


def apply(root: Path) -> None:
    root = Path(root)
    for d in C.NEW_DOCS_SV:
        B.write_new_doc(root, d, adopted=C.DATE)
        rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                              authority=["GOV.41"], targets=[d["id"]], scope=["STND/SV"],
                                              rationale=RATIONALE + TAIL))
        print("seq", rec.entry["seq"], d["id"])
