"""Rehearsable round of 2026-10-28 on the reach of GOV.20: LVL0 1.8 and STND.DFLT 1.6.1.

Two transactions, one per document, in citation order:
- LVL0 1.8 (minor, GOV.40): GOV.20 gives a project constitution to a project that promotes a result other than
  through its adopted classification (QA.11), releases software, or drives physical hardware, so that the standing
  promotion of QA.11 at CSQ3 and CSQ4 asks no constitution, as before LVL0 1.7;
- STND.DFLT 1.6.1 (editorial, GOV.41): the Notes say how far work without a project constitution is relied upon.

AT is the time of application, taken when the module is loaded; transaction k takes AT plus k seconds, and each
revision row is dated by its transaction. Run from harness/:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_constitution_round_2026_10_28.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

AT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
RECORD = "review-records/round-2026-10-28-constitution/decisions.md"
LVL0_SCOPE = ["LVL0", "PRIN", "PRIME", "GUARD", "VV", "REPRO", "INTPR", "DSGN", "SIMPL", "RSRC", "QA", "GOV", "LEX"]
RULING = ("The custodian ruled on 2026-10-28, on the recommendation to have GOV.20 apply only to promotions beyond the "
          "one QA.11 makes at classification: \"i agree with the recommendation on the open items. proceed\".")
PROPOSAL = (f"Proposal: the recommendation of 2026-10-28 quoted in {RECORD}, on the item of OPEN-ITEMS.md, "
            "\"Corpus, for a later round\".")

# ----------------------------------------------------------------------------------------------------------- LVL0 1.8

GOV20 = [
    ("Every project that promotes a result, releases software, or drives physical hardware has a project "
     "constitution:",
     "Every project that promotes a result other than through its adopted classification (QA.11), releases "
     "software, or drives physical hardware has a project constitution:"),
    ('cites: ["PRIME.15"]', 'cites: ["QA.11", "PRIME.15"]'),
]

LVL0_READING = (
    "GOV.20 gives a project constitution to every project that promotes a result other than through its adopted "
    "classification, releases software, or drives physical hardware, so that the adopted classification, which "
    "QA.11 makes the promotion of each result of work of CSQ3 or CSQ4 that meets its acceptance criteria, asks no "
    "project constitution")


def lvl0_rationale(date: str) -> str:
    return (
        f"Minor amendment, revision 1.8, ratified by the custodian on {date}: {LVL0_READING}. Reason: read with the "
        "sentence that revision 1.7 gave QA.11, GOV.20 gave a project constitution to every project of CSQ3 or CSQ4 "
        "with a result that meets its acceptance criteria, although rulings C1 to C8 of "
        "review-records/deep-review-2026-10-28/rulings.md lowered the ceremony of work at those classes and added "
        "none, and the Notes of STND.DFLT kept the reach that GOV.20 had before revision 1.7 (OPEN-ITEMS.md, "
        f"\"Corpus, for a later round\"). {RULING} Alternatives weighed: a ruling under GOV.3 that reads GOV.20 so "
        "without a text change (rejected: under GOV.9 the more restrictive reading of the text would keep governing "
        "every reader who has not seen the ruling); withdrawing the "
        "sentence of QA.11, or making the classification something other than a promotion (rejected: it undoes "
        "rulings C1 and C5, under which no result is promoted one by one below CSQ2); keying GOV.20 to the "
        "consequence class (rejected: a class does not decide whether a project releases software or drives "
        "hardware, and a promotion at CSQ3 beyond the classification's still calls for a constitution). Class: "
        "minor under STND.IDENT.3, because the reach of an obligation changes while no prime directive or principle "
        "changes in motivation or intent. Floor (GOV.11): the change narrows a LVL0 obligation of the floor, on the "
        "custodian's ruling under GOV.40, which GOV.11 does not bar, since GOV.11 bars lower governance from raising "
        "the floor; a project that promotes a result by its human owner's recorded act, releases software, or drives "
        "physical hardware has a project constitution, as at ledger entry 202, and a project of CSQ3 or CSQ4 whose "
        "results are relied upon only as QA.11 admits has none, where at entry 202 that reliance needed a promotion "
        "by recorded act and so a constitution; the reliance that the classification admits is the "
        "reliance that QA.11 and the CSQ3 test of GOV.12 bound, by the author or immediate team alone, feeding work "
        "verified later, and work without a constitution meets it under the defaults (GOV.22), which provide every "
        "mechanism of GOV.21; the prime directives and every other provision of the floor are unchanged. Lower "
        "governance affected: the Notes of STND.DFLT, amended in the same round; STND.PROJ, STND.INSTR, the "
        "template of a project constitution, and the Lexicon terms Project and Project constitution cite GOV.20 for "
        "what a constitution is and holds, which is unchanged. Transition (GOV.42): none; no lower provision needs "
        "conforming, and a project constitution adopted under revision 1.7 or 1.7.1 stays in force. " + PROPOSAL
        + F.AUTHOR)


def apply_lvl0(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "GOV/20.md", GOV20)
    raise_revision(root, "LVL0", "1.7.1", "1.8", f"| 1.8 | {date} | Minor amendment (GOV.40): {LVL0_READING}. |")
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.40"], targets=["LVL0", "GOV.20"], scope=LVL0_SCOPE,
                                          rationale=lvl0_rationale(date)))
    print("seq", rec.entry["seq"], "LVL0 1.8")


# ----------------------------------------------------------------------------------------------------- STND.DFLT 1.6.1

DFLT_NOTE = [(
    "No class is set by default (GOV.13); work without a project constitution is relied upon by no one beyond its "
    "author (GOV.20), so the rows of STND.CLASS.18 and STND.CLASS.19 have no occasion to act until the human owner "
    "records one.",
    "No class is set by default (GOV.13), so the rows of STND.CLASS.18 and STND.CLASS.19 have no occasion to act "
    "until the human owner records one. A project without a project constitution promotes a result only through "
    "its adopted classification (GOV.20), so its work is relied upon beyond its author only as QA.11 admits for "
    "work of CSQ3 or CSQ4.")]

DFLT_READING = (
    "the Notes say that a project without a project constitution promotes a result only through its adopted "
    "classification, so that its work is relied upon beyond its author only as QA.11 admits for work of CSQ3 or "
    "CSQ4, in place of saying that work without one is relied upon by no one beyond its author, which the sentence "
    "that LVL0 1.7 gave QA.11 "
    "made untrue; they say apart from it that no class is set by default, so that the rows of STND.CLASS.18 and "
    "STND.CLASS.19 have no occasion to act until the human owner records one")


def apply_dflt(root: Path, at: str) -> None:
    date = at[:10]
    replace_text(root, "STND/DFLT/_doc.md", DFLT_NOTE)
    row = (f"| 1.6.1 | {date} | Editorial amendment (GOV.41): {DFLT_READING}; no obligation, permission, or defined "
           "meaning changes. |")
    rationale = (
        f"Editorial amendment of STND.DFLT, revision 1.6.1, ratified by the custodian on {date}: {DFLT_READING}. "
        "The change is editorial under STND.IDENT.3 because only the Notes change, and no obligation, permission, "
        "or defined meaning of this document changes; the Note follows GOV.20 as LVL0 1.8 reads. Transition "
        f"(GOV.42): none. {RULING} {PROPOSAL}" + F.AUTHOR)
    F.finish(root, "STND/DFLT", "STND.DFLT", "1.6", "1.6.1", row, rationale, at)


STEPS = [apply_lvl0, apply_dflt]
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, step in enumerate(STEPS):
        step(root, (start + timedelta(seconds=k)).isoformat())
