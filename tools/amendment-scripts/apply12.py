"""Rehearsable amendment script: STND.VVUQ 1.3 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content12 as C
import build as B
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

AT = "2026-10-24T08:36:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = ("Minor amendment of STND.VVUQ to revision 1.3, ratified by the custodian on " + C.DATE
             + ", from the custodian's direction of the same day for every parallel execution model, that strict determinism be an option where feasible and not a requirement unless the acceptance criterion or the consequence class demands it: "
             "new STND.VVUQ.82, a default from CSQ3 (REPRO.3, VV.3, RSRC.4), treats a difference between compared results whose every source is declared under HW.12 or recorded with the compared runs, and which lies within the agreement that the acceptance criterion fixed under STND.VVUQ.1 before the comparison, as no defect; "
             "discourages a change made only to remove such a difference unless an acceptance criterion or a provision at the consequence class requires bitwise identity; and admits a mode without run-to-run variation as an option; new STND.VVUQ.83, an agent-only rule binding at every class (GOV.48), carried into agent instructions by STND.INSTR.10, forbids an agent to change the work, or extend a unit of work, on its own initiative only to remove such a difference or to make results identical across numbers of threads, numbers of processes, or hardware models where no acceptance criterion asks for bitwise identity, and has it state each difference it leaves in its work report; it costs one line of that report and so raises no floor (GOV.11), as the custodian rules; a true race condition remains a correctness defect under DSGN.15 and HW.11. "
             "Transition (GOV.42): none. Review of STND.HARN.28 by the command pairs and by reading, and a cold verification; record claude/drafts/review-records-ledger106-109.md.")


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/VVUQ/82.md").write_text(B.provision_text("STND.VVUQ", C.VVUQ82, "adopted", C.DATE))
    (root / "STND/VVUQ/83.md").write_text(B.provision_text("STND.VVUQ", C.VVUQ83, "adopted", C.DATE))
    B.derive_fields(root, ["STND.VVUQ.82", "STND.VVUQ.83"])
    replace_text(root, "STND/VVUQ/_doc.md", C.VVUQ_DOC_EDITS)
    raise_revision(root, "STND/VVUQ", "1.2.1", "1.3", C.VVUQ_ROW)
    B.write_references(root, ["STND.VVUQ"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.VVUQ"], scope=["STND/VVUQ"],
                                          rationale=RATIONALE + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), "STND.VVUQ")
