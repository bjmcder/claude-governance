"""Rehearsable adoption script: STND.ANNEX 1.0 (one transaction), replacing the undivided draft 0.6."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content_annex as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-24T08:35:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.ANNEX": "Adoption of STND.ANNEX, revision 1.0, ratified by the custodian on " + C.DATE + ", with the custodian's"
 " directions that the default contracts be general and limit no performance, that they be agnostic of platform and"
 " vendor, and that the defaults for programmable logic and integrated circuits stay free of technology, with their"
 " specifics at LVL3: 10 default provisions (GOV.19), none binding. A hardware contract of an execution path MAY cite"
 " the default contract for its hardware type, naming the revision of this standard, in place of stating what that"
 " default states under HW.4 and HW.5 (STND.ANNEX.1); the citing contract states each item that the default leaves"
 " to it and each property that differs from the default, for the rows of HW.5, HW.12, and HW.EMBED.4 from CSQ3, with further reliance on arithmetic and"
 " variation (STND.ANNEX.2)"
 " and for the rows of HW.4 from CSQ2, with other further reliance (STND.ANNEX.3); the"
 " citation is no evidence under HW.6, and a documented accuracy without a stated proven bound is marked as a tested"
 " maximum (STND.ANNEX.4). One default contract, as a table of the matters that HW.4, HW.5, HW.6, and HW.12 ask a"
 " contract to state, each row naming its basis, for each of general-purpose processors (STND.ANNEX.5), accelerators"
 " (STND.ANNEX.6), quantum processors (STND.ANNEX.7), embedded controllers (STND.ANNEX.8), programmable logic"
 " (STND.ANNEX.9), with the documentation of the supplier for a configuration whose design record the project does"
 " not hold, and integrated circuits (STND.ANNEX.10); where a source states nothing, the property is not"
 " established. Each provision instantiates only DSGN.5, REPRO.2, REPRO.3, VV.1, HW.4, HW.5, HW.6, and HW.12, and"
 " refers without instantiating to HW.8, HW.9, HW.20, HW.GPU.3, HW.QPU.3, HW.QPU.5, HW.EMBED.4, HW.FPGA.4, HW.ASIC.4,"
 " HDES.4, HDES.5, HDES.7, HDES.10, HDES.12, HDES.15, HDES.ASIC.5, HDES.ASIC.11, HDES.ASIC.12, STND.ANNEX.5, and"
 " STND.ANNEX.8, so no provision is forced to binding; every obligation arises only for a contract that cites a"
 " default; no provision raises the floor (GOV.11). The informative section on how the defaults are written becomes"
 " the Notes, and its rules of adoption and tightening become STND.ANNEX.1, STND.ANNEX.2, STND.ANNEX.3, and"
 " STND.ANNEX.4. Replaces the undivided draft 0.6. Transition (GOV.42): none, because no project instrument cites the"
 " draft and each provision binds only a contract that chooses to cite it. Review of STND.HARN.28 by the command"
 " pairs and by reading, a cold review, and a pair review; record claude/drafts/review-records-ledger106-109.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/ANNEX"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS_ANNEX:
        adopt(Path(root), d)
