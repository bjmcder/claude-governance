"""Rehearsable adoption script: STND.CREW 1.0 from draft 0.5 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content4 as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-21T10:40:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.CREW": "Adoption of STND.CREW, revision 1.0, ratified by the custodian on " + C.DATE + ": 21 provisions on the roles of agents in work under STND.WPROC, drafted from the custodian's model and revised at the custodian's direction of 2026-10-21: a lead agent that delegates, does not author changes where the class requires a reviewer it does not direct, keeps one record of pending decisions presented in batches (PRIME.14), and records governance findings with amendment proposals for the human owner (GOV.46); research and planning by level, replanning after the second attempt without progress with the stopping count inherited and with examination by agents without prior context; plan content; effort estimates grounded in the records of comparable units, through a cost model kept as a workbench tool and refitted at each milestone; self-review; out-of-scope findings; one merging agent per parent branch; network access confined to research agents unless an authorization extends it; no limit on the number or depth of delegation, a check of capacity and budget beyond depth 2, and reconciliation of delegated results by the directing agent; cold review with findings checked and dispositioned by the lead agent; a release audit along stated dimensions, in full from CSQ2 and on the dimensions bearing on the changes at CSQ3, by an auditor of STND.CLASS.19 at a capability level no lower than each agent author; and escalation of the capability level within the estimate, the operating envelope, and the owner's discipline (GUARD.14), confined to the subunits that need it, with a ruling of the human owner on an escalation beyond the authorized estimate or to a level the discipline marks. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/wproc-crew-review.md.",
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    scope = "/".join(d["id"].split("."))
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=[scope],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS4:
        adopt(Path(root), d)
