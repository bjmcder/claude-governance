"""Rehearsable amendment script for the LVL2 round (one transaction per document)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import importlib
import content as C
import build as B
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

AT = "2026-10-20T07:55:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {}  # filled below
ONLY = None  # set of doc ids to apply, None = all


def tx(root, kind, target, scope, rationale, authority=("GOV.41",)):
    rec = record_transaction(root, Change(kind=kind, actor="The Custodian", role="custodians", at=AT,
                                          authority=list(authority), targets=[target], scope=[scope],
                                          rationale=rationale + TAIL))
    v = rec.verification
    ok = getattr(v, "ok", None)
    print(f"seq {rec.entry['seq'] if isinstance(rec.entry, dict) else getattr(rec.entry,'seq','?')}: {target} verify ok={ok}")
    return rec


def dflt(root):
    for p in C.DFLT_NEW:
        (root / "STND/DFLT" / f'{p["n"]}.md').write_text(B.provision_text("STND.DFLT", p, "adopted", C.DATE))
    replace_text(root, "STND/DFLT/17.md", [(C.DFLT17_OLD, C.DFLT17_NEW), (C.DFLT17_OLD_INST, C.DFLT17_NEW_INST)])
    B.derive_fields(root, [f'STND.DFLT.{p["n"]}' for p in C.DFLT_NEW] + ["STND.DFLT.17"])
    replace_text(root, "STND/DFLT/_doc.md", C.DFLT_EDITS)
    raise_revision(root, "STND/DFLT", "1.4", "1.5", C.DFLT_ROW)
    B.write_references(root, ["STND.DFLT"])
    return tx(root, "amend", "STND.DFLT", "STND/DFLT", RATIONALE["STND.DFLT"])


def instr(root):
    p = C.INSTR9
    (root / "STND/INSTR/9.md").write_text(B.provision_text("STND.INSTR", p, "adopted", C.DATE))
    B.derive_fields(root, ["STND.INSTR.9"])
    replace_text(root, "STND/INSTR/_doc.md", C.INSTR_EDITS)
    raise_revision(root, "STND/INSTR", "1.2", "1.3", C.INSTR_ROW)
    B.write_references(root, ["STND.INSTR"])
    return tx(root, "amend", "STND.INSTR", "STND/INSTR", RATIONALE["STND.INSTR"])


def adopt(root, d):
    B.write_new_doc(root, d)
    scope = "/".join(d["id"].split("."))
    return tx(root, "adopt", d["id"], scope, RATIONALE[d["id"]])


def apply(root: Path) -> None:
    root = Path(root)
    steps = [("STND.DFLT", dflt), ("STND.INSTR", instr)] + [(d["id"], (lambda r, d=d: adopt(r, d))) for d in C.NEW_DOCS]
    for ident, fn in steps:
        if ONLY is None or ident in ONLY:
            fn(root)


RATIONALE.update({
 "STND.DFLT": "Minor amendment of STND.DFLT to revision 1.5, ratified by the custodian on " + C.DATE + ", conforming on the adoption of AGENT (GOV.42): new STND.DFLT.28 makes the workbench of AGENT.35 the directory workbench of the records directory, its tools in its subdirectory tools; new STND.DFLT.29 to STND.DFLT.31 make the store of non-credential secrets of AGENT.44, where the human owner provides one, the temporary directory secrets at the top of the work, one secret per file, have an agent confirm before its first write in a session that version control excludes it and that no other unprivileged account reads it, restoring either condition where it fails and referring only where it is still unable to confirm, and keep it out of archives, backups, transfers, and unauthorized recursive or pattern-selected operations (PRIME.10); the term Working bounds admits each file of the store only to an agent authorized to handle its secret; STND.DFLT.17 enters a grant in the ledger without the secrets it contains; the term Temporary location admits working copies of items whose source lies outside the work. Class: minor, because obligations are added; none is relaxed. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
 "STND.INSTR": "Minor amendment of STND.INSTR to revision 1.3, ratified by the custodian on " + C.DATE + ", conforming on the adoption of AGENT (GOV.42): new STND.INSTR.9 keeps research notes, the findings of AGENT.32, and the entries held under AGENT.30 in the workbench and not only in the working-notes workspace. Class: minor, because an obligation is added. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
 "STND.CODE": "Adoption of STND.CODE, revision 1.0, ratified by the custodian on " + C.DATE + ": 12 provisions of coding practice for every language, stated as checkable outcomes independent of language and tool; STND.CODE.6 (input checks that no execution setting removes) and STND.CODE.7 (no discard of a failure that PRIME.4 lists) instantiate PRIME.4 and are binding at every class; the other ten, STND.CODE.12 on reasons for other discards among them, are defaults (GOV.19) that apply from CSQ3. Replaces the undivided draft 0.1, whose restatements of DSGN are dropped. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
 "STND.THRT": "Adoption of STND.THRT, revision 1.0, ratified by the custodian on " + C.DATE + ": 9 provisions fixing the form and minimum content of a project's threat model (GUARD.16): the table of assets, threats, sources, and protection with the rows of STND.DFLT.18 and a protected row for supply-chain compromise of fetched components; protected data, including the store of AGENT.44, and those trusted with secrets; the secret-report channel (PRIME.10); detection of record alteration (PRIME.5); exposure events, on which the actor records the event and proposes the change; the sensitive part kept apart (GUARD.18); the recoverable copy of irreplaceable data (default); and two secure practices (GUARD.17). Replaces the undivided draft 0.1. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
 "STND.KNOW": "Adoption of STND.KNOW, revision 1.0, ratified by the custodian on " + C.DATE + ": 14 provisions on knowledge entries and tags (GOV.32 to GOV.34, GOV.37), 12 binding and 2 defaults: entry content, kinds, and form; the evidence levels EVD0 to EVD3, each tied to what STND.CLASS.10 asks of VV.1 at its ceiling, and the reliance ceilings CSQ1 to CSQ4, which GOV.33 assigns to a LVL2 standard; a ceiling of CSQ4 before establishment, while a revalidation is overdue, and outside the domain of validity; a ceiling capped by the establishing reviewer: a human, CSQ1; an independent agent of another configuration, CSQ2; another actor, CSQ3; revalidation and supersession; entries drawn from a workbench, which name their project and carry their evidence; no secret or protected data in any entry; and tag permanence. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
 "STND.DEPS": "Adoption of STND.DEPS, revision 1.0, ratified by the custodian on " + C.DATE + ": 11 provisions of dependency policy (REPRO.9, SIMPL.4): selection weighed from stated evidence without a decision of the human owner (STND.DRAFT.42), initial revision, review at each release, at most every 12 months, and on each change, contract tests on update, toolchain revisions as inputs, the dependency record, package files as that record, and incorporated material; STND.DEPS.6 (verification against the publisher's digest or the first fetch's) and STND.DEPS.7 (advisories before release, with unchecked dependencies recorded) instantiate GUARD.17 and are binding. Replaces the undivided draft 0.2. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
 "STND.PROJ": "Adoption of STND.PROJ, revision 1.0, ratified by the custodian on " + C.DATE + ": 4 provisions fixing the sections of a project constitution (GOV.20, GOV.21), including the workbench, knowledge base, store of secrets, access descriptors, and research-retrieval authorization that AGENT leaves to the project, with parts that STND.CLASS.10 defers stated as not applying; adoption of LVL2 provisions by citation; the standing authorizations a drafting agent proposes at the project's start, each scoped to reach no reserved action (STND.DRAFT.42); and the instrument files of the project template (default). Replaces the undivided draft 0.2. Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading; record claude/drafts/lvl2-round-review.md.",
})
