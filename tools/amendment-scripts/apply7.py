"""Rehearsable adoption script: STND.DOCS 1.0 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content7 as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-22T12:00:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.DOCS": "Adoption of STND.DOCS, revision 1.0, ratified by the custodian on " + C.DATE + ": 11 provisions on the writing that people read, drafted from the custodian's direction of 2026-10-22: work documentation written for a reader who knows the domain but not the code, as one person explaining the work to another; no agents, their instructions, sessions, or actions, notes to the writer or a later session, narration of edits, or citations of process records in it, except where they are the work's subject or a law, license, contract, or publisher's policy requires a statement of agent use; American spelling and usage in human-facing writing and in names in the source not fixed outside the work; plain and specific statement without the habits of generated text, restated from the Wikipedia editors' field guide 'Signs of AI writing' in the copy the custodian supplied on 2026-10-22; all of this binding on agents at every class (GOV.48), and for other writers defaults from CSQ3 with one name per concept, documentation changed with the work, checked examples, and review of the writing a change touches. Transition (GOV.42): existing text conforms when a change next touches it; text in append-only records stays as written. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/docs-review.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/DOCS"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS7:
        adopt(Path(root), d)
