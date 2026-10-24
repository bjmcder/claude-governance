"""Rehearsable adoption script: STND.PY 1.0 (one transaction)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "/home/claude/pkg"); sys.path.insert(0, "/home/claude/harness")
import content_py as C
import build as B
from govharness.workflows.amend import Change, record_transaction

AT = "2026-10-23T11:34:00+00:00"
TAIL = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
        " Under the ruling of ledger entry 15, this decision is the QA.7 review.")
RATIONALE = {
 "STND.PY": "Adoption of STND.PY, revision 1.0, ratified by the custodian on " + C.DATE + ": 31 provisions on Python source, drafted from the custodian's directions of 2026-10-22 (PEP standards for style and idioms, enforced mechanically; always types and type checking; numpydoc docstrings; layout by logical grouping of instructions) and the rulings of 2026-10-23 (platform, version, and tool agnostic; versions and tools chosen by the project in its repository configuration), adding to STND.CODE and STND.DOCS only what is specific to Python; the grouping of statements is STND.CODE.13. The style PEPs as baseline, with notation names kept, and a linter that covers them (STND.PY.1, STND.PY.2); annotations of each function, binding on agents at every class by its own force (STND.PY.4, GOV.48), which STND.INSTR.10 carries, and for all code a default from CSQ3 with strict type checking of library code, tests, and scripts, stubs or reasoned overrides for unannotated dependencies, one list of exempted modules, py.typed, reasoned dynamic types and coded suppressions, and array annotations (STND.PY.3 to STND.PY.9); numpydoc docstrings whose parameter types the annotations carry, with doctests compared to their shown precision (STND.PY.10 to STND.PY.12); declared releases of distributed packages under STND.DEPS, checked at the oldest and newest declared combinations (STND.PY.13, STND.PY.14); generators passed through an rng parameter and built from recorded seeds at entry points, streams for parallel parts by spawning, jump-ahead, or counter-based keys, stable streams for exact references, and no values of the string hash (STND.PY.15 to STND.PY.19); comparison tolerances stated at the tier of STND.VVUQ.1 as named constants (STND.PY.20); logging for diagnostics (STND.PY.21); immutable defaults and named encodings (STND.PY.23, STND.PY.24); run-time checks without assert, interrupts raised again, scoped error settings, and a reason at each relaxed numerical check (STND.PY.26, STND.PY.28, STND.PY.29, STND.PY.31). Four provisions instantiate PRIME.4 and bind at every class: one set of responses to each condition that PRIME.4 lists (STND.PY.22), no assert for untrusted input (STND.PY.25), that response from handlers of MemoryError and RecursionError and no suppression context that discards them (STND.PY.27), and detection and response where a report of a listed condition is suppressed (STND.PY.30). By the custodian's rulings of 2026-10-23, the agent rule and the PRIME.4 rules raise no floor (PRIN.10). Transition (GOV.42): existing source conforms when a change next touches it; strict checking is reached through the list of exempted modules. Review of STND.HARN.28 by the command pairs and by reading, a cold review, a pair review, and cold verifications; record claude/drafts/review-records-ledger100-105.md."
}


def adopt(root, d):
    B.write_new_doc(root, d, adopted=C.DATE)
    rec = record_transaction(root, Change(kind="adopt", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=[d["id"]], scope=["STND/PY"],
                                          rationale=RATIONALE[d["id"]] + TAIL))
    print("seq", rec.entry["seq"] if isinstance(rec.entry, dict) else getattr(rec.entry, "seq", "?"), d["id"])


def apply(root: Path) -> None:
    for d in C.NEW_DOCS_PY:
        adopt(Path(root), d)
