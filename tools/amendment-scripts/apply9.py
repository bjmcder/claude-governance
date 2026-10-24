"""Rehearsable amendment script: STND.CODE 1.1 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content9 as C
import build as B
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text

AT = "2026-10-23T11:32:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = ("Minor amendment of STND.CODE to revision 1.1, ratified by the custodian on " + C.DATE
             + ": new STND.CODE.13, a default from CSQ3 (INTPR.1), groups the statements of each body into blocks that each carry out one step of the computation, "
             "with one blank line between blocks, none inside a block other than those a layout tool inserts, and a comment heading a block whose step is not evident. "
             "The custodian's direction of 2026-10-22 to format Python by logical grouping of instructions was ruled on 2026-10-23 to apply to every language, so it moves here from the draft Python standard. "
             "Transition (GOV.42): text that a change adds or alters conforms. "
             "Review of STND.HARN.28 by the command pairs and by reading, and a cold verification; record claude/drafts/review-records-ledger100-105.md.")


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/CODE/13.md").write_text(B.provision_text("STND.CODE", C.CODE13, "adopted", C.DATE))
    B.derive_fields(root, ["STND.CODE.13"])
    replace_text(root, "STND/CODE/_doc.md", C.CODE_DOC_EDITS)
    raise_revision(root, "STND/CODE", "1.0", "1.1", C.CODE_ROW)
    B.write_references(root, ["STND.CODE"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.CODE"], scope=["STND/CODE"],
                                          rationale=RATIONALE + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), "STND.CODE")
