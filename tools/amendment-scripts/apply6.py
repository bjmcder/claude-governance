"""Rehearsable adoption script: STND.DOCS 1.0 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content6 as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-22T12:00:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.DOCS": "Adoption of STND.DOCS, revision 1.0, ratified by the custodian on " + C.DATE + ": 9 provisions on the writing that people read, drafted from the custodian's direction of 2026-10-22: work documentation written as one person explaining the work to another; no agents, sessions, instructions, agent actions, notes to self, narration of edits, or citations of governance records in it, except where they are the work's subject or a law, license, or publisher's policy requires a statement of agent use; American spelling and usage in all human-facing writing and in identifiers not fixed by an external interface; no habits of generated prose, drawn from the Wikipedia editors' guide to signs of AI writing; documentation changed with the work in the same change and consistent with the work and with itself; and, as defaults from CSQ3, one name per concept, checked examples, and review of the documentation a change affects. Transition (GOV.42): existing work documentation conforms at its next change. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/docs-review.md.",
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/DOCS"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS6:
        adopt(Path(root), d)
