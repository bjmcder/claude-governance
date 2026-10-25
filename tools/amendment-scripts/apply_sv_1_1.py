"""Rehearsable minor amendment: STND.SV 1.1, adding the naming rule (one transaction).

New: STND.SV.28. STND.SV uses no term of untrusted input, so it imports none. apply_close_p3.py runs it after
apply_close_p1.py. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_sv_1_1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from content3 import P  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-25"
AT = "2026-10-25T20:25:00+00:00"

NEW28 = P(28, "Verilog and SystemVerilog naming conventions", "Names", """
Each name that the source files of a design and of its verification set declare SHOULD follow the naming convention that the repository configuration names (INTPR.1). A name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4).
""", ["INTPR.1", "INTPR.4"], refs=["NUMER.4", "STND.DOCS.12"])

DOC = [
    # Purpose: the floor
    ("bind at every class through STND.CONC.1 and STND.CONC.2; this standard adds nothing to that floor.",
     "bind at every class through STND.CONC.1 and STND.CONC.2, as the responses to a failure that PRIME.4 lists bind "
     "through STND.CODE.14 and the checks that CPS.5 or CPS.9 requires are not removable by an execution setting "
     "through STND.CODE.16; "
     "this standard adds nothing to that floor."),
    # Terms
    ("Repository configuration, Static check, and Execution setting have the meanings that STND.CODE gives them,",
     "Repository configuration, Static check, Execution setting, and High-assurance code have the meanings that "
     "STND.CODE gives them,"),
    # Notes: what STND.CODE already holds
    ("and statements grouped by step in each process (STND.CODE.13) already apply.",
     "and statements grouped by step in each process (STND.CODE.13) already apply, and for high-assurance code the "
     "coding standard, the claims of conformance, the edition with the validation of each tool that synthesizes or "
     "simulates it, and the deviations (STND.CODE.17 to STND.CODE.20)."),
    # Purpose
    ("and the classes of finding that the static checks report, a second route for the check of the netlist and for "
     "the verdicts of simulation, and comparisons between simulators (STND.SV.24 to STND.SV.27).",
     "the classes of finding that the static checks report, a second route for the check of the netlist and for the "
     "verdicts of simulation, and comparisons between simulators (STND.SV.24 to STND.SV.27); and the conventions of "
     "names (STND.SV.28)."),
    # Notes: names, before the paragraph on matters without provisions
    ("The research note retrieved no primary text on the coding of state machines,",
     "Names. The research note retrieved no convention of names that the language definition fixes, and that none "
     "exists is unverified, so STND.SV.28 leaves the convention to the repository configuration, as STND.STDC.39 and STND.LEAN.27 do, "
     "keeps the names that the notation of NUMER.4 fixes, as STND.DOCS.12 permits, and adds no table.\n\n"
     "The research note retrieved no primary text on the coding of state machines,"),
    # Notes: class onset
    ("STND.SV.27 instantiates REPRO.3 and applies from CSQ3.",
     "STND.SV.27 instantiates REPRO.3 and applies from CSQ3. STND.SV.28 instantiates INTPR.1 and INTPR.4, rests on "
     "no row, and applies from CSQ3."),
]

READING = (
    "new STND.SV.28 (default, from CSQ3) leaves the convention of names in the source files of a design and of its "
    "verification set to the repository configuration and keeps the names that the notation of NUMER.4 fixes, the "
    "rule of decision 9 of 2026-10-24; the Purpose lists it and names STND.CODE.14 and STND.CODE.16 among the "
    "provisions that bind at every class; Terms import High-assurance code from STND.CODE; the Notes cite "
    "STND.CODE.17 to STND.CODE.20 for high-assurance code and give the reason for the naming rule and its class "
    "onset")

ROW = f"| 1.1 | {DATE} | Minor amendment (GOV.41): {READING}. |"

RATIONALE = (
    f"Minor amendment of STND.SV to revision 1.1, ratified by the custodian on {DATE}: {READING}. The change is "
    "minor because it adds a default; the citations of STND.CODE add no obligation, since STND.CODE applies to "
    "hardware descriptions by its own scope. STND.SV.28 states for hardware descriptions and their verification the rule "
    "that STND.STDC.39 and STND.LEAN.27 state for C and Lean, in the words of STND.STDC.39. Class onsets: STND.SV.28 rests on "
    "no row of STND.CLASS.10 and applies from CSQ3; no other onset changes. Floor (GOV.11): STND.SV.28 is a "
    "default and instantiates only INTPR, so no floor is raised; no provision of this standard binds. Transition "
    "(GOV.42): existing source conforms when a change next touches it. Review of STND.HARN.28 by the command pairs; "
    "record review-records/round-2026-10-25-close/p3/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    (root / "STND/SV/28.md").write_text(B.provision_text("STND.SV", NEW28, "adopted", DATE), encoding="utf-8")
    res = B.derive_fields(root, ["STND.SV.28"])
    if res["STND.SV.28"].unresolved or res["STND.SV.28"].forced:
        raise ValueError(f"STND.SV.28: {res['STND.SV.28']}")
    replace_text(root, "STND/SV/_doc.md", DOC)
    raise_revision(root, "STND/SV", "1.0", "1.1", ROW)
    B.write_references(root, ["STND.SV"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.SV"], scope=["STND/SV"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.SV 1.1")
