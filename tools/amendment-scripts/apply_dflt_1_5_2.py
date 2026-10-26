"""Rehearsable editorial amendment: STND.DFLT 1.5.2, round of 2026-10-26 (decision 5).

One transaction. The Notes drop the sentence on how a harness that derives an environment under STND.HARN.18
maps the secret store, since STND.HARN 1.4 withdraws STND.HARN.18. Runs before apply_harn_1_4.py, so that no
state of the round cites a withdrawn identifier. Run from harness/, so that govharness imports:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_dflt_1_5_2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import write_references  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

DATE = "2026-10-26"
AT = "2026-10-26T12:00:00+00:00"

STORE = [(
    " A project constitution states its own locations, or adopts these by citation. A harness that derives an "
    "environment under STND.HARN.18 maps the bounds of the store as STND.DFLT.29 and the working bounds state them.",
    " A project constitution states its own locations, or adopts these by citation.",
)]

READING = ("the Notes no longer say how a harness that derives an environment maps the bounds of the secret store, "
           "since STND.HARN 1.4 withdraws the provisions on a configuration that a harness derives")
ROW = (f"| 1.5.2 | {DATE} | Editorial amendment (GOV.41): {READING}; no obligation, permission, or defined meaning "
       "changes. |")

RATIONALE = (
    f"Editorial amendment of STND.DFLT, revision 1.5.2, ratified by the custodian on {DATE}: {READING}. The change "
    "is editorial under STND.IDENT.3 because it removes one informative sentence; STND.DFLT.29 and the working bounds "
    "state the bounds of the store as before, so no obligation, permission, or defined meaning changes. "
    "STND.DFLT.22 cites no withdrawn provision and is unchanged. Transition "
    "(GOV.42): none. Decision 5 of review-records/round-2026-10-26/decisions.md."
    " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
    " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/DFLT/_doc.md", STORE)
    raise_revision(root, "STND/DFLT", "1.5.1", "1.5.2", ROW)
    write_references(root, ["STND.DFLT"])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=AT,
                                          authority=["GOV.41"], targets=["STND.DFLT"], scope=["STND/DFLT"],
                                          rationale=RATIONALE))
    print("seq", rec.entry["seq"], "STND.DFLT 1.5.2")
