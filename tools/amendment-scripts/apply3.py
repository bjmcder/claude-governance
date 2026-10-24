"""Rehearsable adoption script: STND.WPROC and STND.CREW 1.0 (one transaction each)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content3 as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-21T08:25:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.WPROC": "Adoption of STND.WPROC, revision 1.0, ratified by the custodian on " + C.DATE + ": 15 provisions of the part of a work process that the version history carries (QA.2), drafted from the custodian's model: unit records of dated entries that travel with their branches, and attributed commits; main lines and a development line, on which the ledger, roadmap, defect tracking, and record of pending decisions are kept and changed one change at a time; a branch per unit made from its parent's branch and merged back only into it, one merge at a time; fixes from the most upstream affected branch, reaching descendants by merges of their parents; before each merge, an update from the parent, the checks the change affects, and the review at the agent rows of STND.CLASS.18 with its findings resolved, the human rows falling before the release; merges below the release without a decision of the human owner (STND.DRAFT.42); each advance of a main line a release that the human owner decides at every class, to an existing revision that the recorded decision names, which authorizes an agent per action and lapses on a new blocking defect or an expired waiver (GOV.50, QA.10, GUARD.11), on a proposal stating what AGENT.47 reports and, from CSQ3, a release record; permanent release names. Departures from the model: no per-merge permission of the human owner into the development line at CSQ2 and above, and the human owner's decision naming the revision in place of the human owner's execution of the merge. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/wproc-crew-review.md.",
 "STND.CREW": "Adoption of STND.CREW, revision 1.0, ratified by the custodian on " + C.DATE + ": 15 provisions on the roles of agents in work under STND.WPROC, drafted from the custodian's model: a lead agent that delegates, does not author changes where the class requires a reviewer it does not direct, keeps one record of pending decisions presented in batches (PRIME.14), and records governance findings with amendment proposals for the human owner (GOV.46); research and planning by level, replanning after the second attempt without progress with the stopping count inherited; plan content; self-review; out-of-scope findings; one merging agent per parent branch; cold review with findings checked and dispositioned by the lead agent; a release audit along stated dimensions, in full from CSQ2 and on the dimensions bearing on the changes at CSQ3, by an auditor of STND.CLASS.19 at a capability level no lower than each agent author; and escalation of the capability level within the estimate, the operating envelope, and the owner's discipline (GUARD.14). Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/wproc-crew-review.md.",
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    scope = "/".join(d["id"].split("."))
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=[scope],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


ONLY = None  # set of document ids to apply; None applies all


def apply(root: Path) -> None:
    for d in C.NEW_DOCS3:
        if ONLY is None or d["id"] in ONLY:
            adopt(Path(root), d)
