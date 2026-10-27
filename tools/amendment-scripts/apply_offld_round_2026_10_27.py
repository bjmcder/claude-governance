"""Rehearsable round of 2026-10-27 on offloaded work: STND.OFFLD 1.1 and STND.PERF 1.0.1 (decision 27 of 2026-10-25).

Two transactions. STND.OFFLD.31 names, among the costs of first use of offloaded work, the first filling of caches
and memory that STND.PERF.12 names for every other measurement, so that the measurements that STND.PERF.12 leaves
to it state the same costs. The Notes of STND.PERF drop a clause that STND.OFFLD 1.0.1 made stale. Run from
harness/:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_offld_round_2026_10_27.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

AT = "2026-10-27T18:00:00+00:00"
RECORD = "review-records/round-2026-10-27-offld/decisions.md"

OFFLD31 = [(
    "Each such measurement SHOULD state whether it includes the costs of a first submission, among them "
    "initialization and compilation at load (RSRC.4, STND.PERF.12).",
    "Each such measurement SHOULD state whether it includes the costs of first use, among them initialization, "
    "compilation at load, and the first filling of caches and memory (RSRC.4, STND.PERF.12).")]

OFFLD_NOTES = [(
    "The costs of first use that the two name differ: STND.PERF.12 names the first filling of caches and memory "
    "among them, and STND.OFFLD.31 names initialization and compilation at load only, so a record of offloaded work "
    "that states those two meets STND.OFFLD.31.",
    "The two name the same costs of first use: initialization, compilation at load, and the first filling of caches "
    "and memory, so one record of offloaded work that states them meets both.")]

PERF_NOTES = [(
    "and one record meets both standards; a later amendment of STND.OFFLD could have STND.OFFLD.31 cite them",
    "and one record meets both standards")]

OFFLD_READING = (
    "the second sentence of STND.OFFLD.31 asks a measurement of offloaded work to state whether it includes the "
    "costs of first use, among them initialization, compilation at load, and the first filling of caches and "
    "memory, the costs that STND.PERF.12 names for every other measurement, in place of the costs of a first "
    "submission, among them initialization and compilation at load; the Notes say that the two name the same costs")
OFFLD_ROW = f"| 1.1 | {F.DATE} | Minor amendment (GOV.41): {OFFLD_READING}. |"
OFFLD_RATIONALE = (
    f"Minor amendment of STND.OFFLD, revision 1.1, ratified by the custodian on {F.DATE}: {OFFLD_READING}. The "
    "change is minor under STND.IDENT.3 because it adds to an obligation: a measurement of offloaded work states "
    "one more cost of first use, and the costs reached are those of first use, not of the first submission alone. "
    "STND.PERF.12 leaves offloaded work to STND.OFFLD.31, so before this amendment a measurement of offloaded work "
    "stated less than each other measurement of a performance evaluation. STND.OFFLD.31 is a default, which a "
    "recorded decision replaces (GOV.19), and asks one more statement in a record that it already asks, so it raises "
    "no floor (GOV.11). Class onset: from CSQ3, as before and as STND.PERF.12. Transition (GOV.42): a measurement "
    "recorded before this amendment needs no new statement. Decision 27 of "
    "review-records/round-2026-10-25-close/decisions-final.md, from item 18 of that record; "
    f"{RECORD}." + F.AUTHOR)

PERF_READING = ("the Notes drop the clause that a later amendment of STND.OFFLD could have STND.OFFLD.31 cite "
                "STND.PERF.12 and STND.PERF.14, which STND.OFFLD 1.0.1 did")
PERF_ROW = (f"| 1.0.1 | {F.DATE} | Editorial amendment (GOV.41): {PERF_READING}; no obligation, permission, or "
            "defined meaning changes. |")
PERF_RATIONALE = (
    f"Editorial amendment of STND.PERF, revision 1.0.1, ratified by the custodian on {F.DATE}: {PERF_READING}. The "
    "change is editorial under STND.IDENT.3 because it removes an informative clause, so no obligation, permission, "
    f"or defined meaning changes. Transition (GOV.42): none. {RECORD}." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    replace_text(root, "STND/OFFLD/31.md", OFFLD31)
    F.check_fields(root, ["STND.OFFLD.31"])
    replace_text(root, "STND/OFFLD/_doc.md", OFFLD_NOTES)
    F.finish(root, "STND/OFFLD", "STND.OFFLD", "1.0.1", "1.1", OFFLD_ROW, OFFLD_RATIONALE, start.isoformat())
    replace_text(root, "STND/PERF/_doc.md", PERF_NOTES)
    F.finish(root, "STND/PERF", "STND.PERF", "1.0", "1.0.1", PERF_ROW, PERF_RATIONALE,
             (start + timedelta(seconds=1)).isoformat())
