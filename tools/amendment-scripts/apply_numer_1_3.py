"""Rehearsable minor amendment: NUMER 1.3, the shared matter of random streams of divided computations.

Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_numer_1_3.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-24"
AT = "2026-10-24T19:04:00+00:00"

MATTER = "Random streams of a computation divided among concurrent tasks"

NUMER2 = [
    ('"NUMER.22", "NUMER.23", "NUMER.25"', '"NUMER.22", "NUMER.23", "NUMER.24", "NUMER.25"'),
    ("| Derivatives of a computed result | NUMER | NUMER.27, NUMER.28, NUMER.29 |",
     "| Derivatives of a computed result | NUMER | NUMER.27, NUMER.28, NUMER.29 |\n"
     f"| {MATTER} | NUMER | NUMER.24 |"),
]

DOC = [
    ("NUMER owns six shared matters and addresses two that HW owns and one that MEAS owns (NUMER.2).",
     "NUMER owns seven shared matters and addresses two that HW owns and one that MEAS owns (NUMER.2)."),
    ("This profile absorbs the NUMER problem-type entries of the hardware type annex (STND.ANNEX), which are removed "
     "from it on adoption.",
     "This profile absorbs the NUMER problem-type entries of the hardware type annex (STND.ANNEX), which are removed "
     "from it on adoption. NUMER owns the random streams of a computation divided among concurrent tasks, as the "
     "custodian assigned at the adoption of STND.CONC: NUMER.24 has the record of a stochastic method that draws from "
     "more than one source hold evidence that the sources are free of dependence that affects the result, and the "
     "LVL2 standards give the default means, STND.CONC.23 keying each stream to a part of the computation defined "
     "independently of the number of tasks and of the task that computes it, and STND.VVUQ.62 the construction of "
     "the streams. The row of NUMER.2 assigns the matter and adds no obligation of the work, so it raises no floor "
     "(GOV.11)."),
]

READING = (f"NUMER.2 gains the matter {MATTER}, owned by NUMER and given by NUMER.24, as the custodian assigned at "
           "the adoption of STND.CONC; the Notes count seven owned matters and cite STND.CONC.23 and STND.VVUQ.62 "
           "for the keying and construction of the streams; References lists STND.CONC and STND.VVUQ")

ROW = f"| 1.3 | {DATE} | Minor amendment (GOV.41), conforming on the adoption of STND.CONC: {READING}. |"

RATIONALE = (
    f"Minor amendment of NUMER to revision 1.3, ratified by the custodian on {DATE}, conforming on the adoption of "
    f"STND.CONC in ledger entry 112 (STND.DRAFT.39): {READING}. The change is minor because the table of NUMER.2 "
    "is normative and allocates a shared matter, so it alters what NUMER.2 asks of the governance documents that "
    "address the matter (STND.DRAFT.39). It adds no obligation of the work and relaxes none: NUMER.24 is unchanged "
    "and keeps its onset, and the keying and construction of streams stay defaults of STND.CONC.23 and "
    "STND.VVUQ.62, so no floor is raised (GOV.11). Transition (GOV.42): none, because no obligation of the work "
    "changes. Review of STND.HARN.28 by the command pairs, for the changed NUMER.2; record "
    "review-records/round-2026-10-24/amendments/."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "NUMER/2.md", NUMER2)
    replace_text(root, "NUMER/_doc.md", DOC)
    raise_revision(root, "NUMER", "1.2", "1.3", ROW)
    B.write_references(root, ["NUMER"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["NUMER"], scope=["NUMER"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "NUMER 1.3")
