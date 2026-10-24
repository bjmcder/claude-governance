"""Rehearsable adoption script: STND.DOCS 1.0 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content8 as C
import build as B
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

AT = "2026-10-23T11:30:00+00:00"
AT_INSTR = "2026-10-23T11:31:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.INSTR": "Minor amendment of STND.INSTR to revision 1.4, ratified by the custodian on " + C.DATE + ", conforming on the adoption of STND.DOCS: new STND.INSTR.10 has an agent meet each binding provision of another adopted LVL2 standard that applies to its work, as far as a sentence of it has an agent or a role that an agent holds as its actor, so that agent instructions drawn from this standard carry the binding agent provisions of the other LVL2 standards, STND.DOCS.10 among them (GOV.48, STND.DFLT.21). Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading, a cold review, and cold verifications; record claude/drafts/review-records-ledger100-105.md.",
 "STND.DOCS": "Adoption of STND.DOCS, revision 1.0, ratified by the custodian on " + C.DATE + ": 14 provisions on the writing that people read, drafted from the custodian's direction of 2026-10-22: work documentation written for a reader who knows the domain but not the code, as one person explaining the work to another (binding, INTPR.2); terms defined on first use and examples; no agents, agent conduct, notes to anyone but its human readers, narration of edits, or citations of process records in it, except where governance or agents are the work's subject, where a law, license, contract, or publisher's policy requires a statement of agent use, and in changelogs, release, migration, and deprecation notes; American spelling and usage in human-facing writing and in names in the source not fixed outside the work; plain and specific statement without the habits of generated text, restated from the Wikipedia editors' field guide 'Signs of AI writing' in the copy the custodian supplied on 2026-10-22; documentation changed with the work and consistent with it and with itself, one name per concept, checked examples, and review of the writing a change touches. STND.DOCS.10 holds every agent at every class to STND.DOCS.3, STND.DOCS.4, STND.DOCS.5, STND.DOCS.8, and STND.DOCS.9 and to correcting or recording each disagreement it knows of (GOV.48); the other provisions are defaults from CSQ3. Transition (GOV.42): text that a change adds or alters conforms; text in append-only records, superseded decision records, and past commit messages stays as written. Review of STND.HARN.28 by the command pairs and by reading, a cold review, and cold verifications; record claude/drafts/review-records-ledger100-105.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/DOCS"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def instr(root):
    root = Path(root)
    (root / "STND/INSTR/10.md").write_text(B.provision_text("STND.INSTR", C.INSTR10, "adopted", C.DATE))
    B.derive_fields(root, ["STND.INSTR.10"])
    replace_text(root, "STND/INSTR/_doc.md", C.INSTR_DOC_EDITS)
    raise_revision(root, "STND/INSTR", "1.3", "1.4", C.INSTR_ROW)
    B.write_references(root, ["STND.INSTR"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT_INSTR,
                                          authority=["GOV.41"], targets=["STND.INSTR"], scope=["STND/INSTR"],
                                          rationale=RATIONALE["STND.INSTR"] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), "STND.INSTR")


def apply(root: Path) -> None:
    for d in C.NEW_DOCS8:
        adopt(Path(root), d)
    instr(root)
