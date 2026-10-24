"""Rehearsable adoption script: STND.CREW 1.0 (draft 0.6) and STND.PROJ 1.1 (one transaction each)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content5 as C
import build as B
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

AT = "2026-10-21T12:05:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.CREW": "Adoption of STND.CREW, revision 1.0, ratified by the custodian on " + C.DATE + ": 23 provisions on the roles of agents in work under STND.WPROC, drafted from the custodian's model and revised at the custodian's direction of 2026-10-21: a lead agent that delegates, does not author changes where the class requires a reviewer it does not direct, keeps one record of pending decisions presented in batches (PRIME.14), and records governance findings with amendment proposals for the human owner (GOV.46); research and planning by level, replanning after the second attempt without progress with the stopping count inherited and with the examination and assistance of agents holding little or no prior context; plan content, with the kind of each unit and the highest capability level for which its estimate provides; estimates of cost and time that name the comparable units whose records they use and the prediction of a cost model kept as a workbench tool, refitted at each milestone; self-review; out-of-scope findings; one merging agent per parent branch; the role and delegation depth stated in each brief, research agents designated by the lead, planning, or research agents, and, as a recommendation, an agent that has made research retrieval changing only records in the same session, the confinement of research retrieval to research agents being set at LVL3 through STND.PROJ.3 (GOV.18); no limit on the number or depth of delegation, a recorded check of the authorized estimate or operating envelope before depth 3, and of machine capacity where parallel units share a machine, and reconciliation of delegated results by the directing agent, which carries its agents' referrals up unchanged; cold review with findings checked and dispositioned by the lead agent; a release audit along stated dimensions, in full from CSQ2 and on the dimensions bearing on the changes at CSQ3, by an auditor of STND.CLASS.19 at a capability level ranked at or above each agent author; and escalation of the capability level within the authorized estimate, the operating envelope, and the owner's discipline (GUARD.14), confined to the subunits that need it, with a ruling of the human owner on an assignment beyond the cost or capability levels of the authorized estimate or to a level that the discipline marks, the referral stating the unit's count and bound and the subunits concerned waiting meanwhile. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/wproc-crew-review.md, revision of 2026-10-21.",
 "STND.PROJ": "Minor amendment of STND.PROJ to revision 1.1, ratified by the custodian on " + C.DATE + ", conforming on the adoption of STND.CREW at the custodian's direction of 2026-10-21: the section Authorizations states the agents or roles to which each authorization extends (GUARD.12) and the capability levels that the cost discipline marks for ruling (STND.PROJ.1); each proposed standing authorization states the roles to which it extends, read-only research retrieval to research agents alone, a proposal that limits network access for research only where the human owner adopts it in the constitution, at LVL3 (GOV.18) (STND.PROJ.3); new STND.PROJ.5 proposes a discipline for the operating cost of agents stating the capability levels whose assignment needs the human owner's ruling and keeping AGENT.6 in force for every unit and AGENT.10 for every assignment to an unmarked level (GUARD.14, STND.DRAFT.42). Transition (GOV.42): constitutions adopted before this revision keep their authorizations, which extend as their text says (GUARD.12); one silent on roles extends to no directed agent until the human owner amends it. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/wproc-crew-review.md, revision of 2026-10-21.",
}


def tx(root, kind, target, scope, rationale):
    rec = record_transaction(root, Change(kind=kind, actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[target], scope=[scope],
                                          rationale=rationale + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), target)
    return rec


def crew(root):
    B.write_new_doc(root, C.CREW, adopted=C.DATE)
    return tx(root, "adopt", "STND.CREW", "STND/CREW", RATIONALE["STND.CREW"])


def proj(root):
    (root / "STND/PROJ/5.md").write_text(B.provision_text("STND.PROJ", C.PROJ5, "adopted", C.DATE))
    replace_text(root, "STND/PROJ/1.md", C.PROJ1_EDITS)
    replace_text(root, "STND/PROJ/3.md", C.PROJ3_EDITS)
    B.derive_fields(root, ["STND.PROJ.5", "STND.PROJ.1", "STND.PROJ.3"])
    replace_text(root, "STND/PROJ/_doc.md", C.PROJ_DOC_EDITS)
    raise_revision(root, "STND/PROJ", "1.0", "1.1", C.PROJ_ROW)
    B.write_references(root, ["STND.PROJ"])
    return tx(root, "amend", "STND.PROJ", "STND/PROJ", RATIONALE["STND.PROJ"])


ONLY = None


def apply(root: Path) -> None:
    root = Path(root)
    for ident, fn in [("STND.CREW", crew), ("STND.PROJ", proj)]:
        if ONLY is None or ident in ONLY:
            fn(root)
