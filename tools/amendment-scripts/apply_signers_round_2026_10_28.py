"""Rehearsable round of 2026-10-28 on signer keys: STND.HARN 1.5.

One transaction. STND.HARN.10 has each row among signers name one ledger, so that every key can be closed; a row
for "all" ledgers stays only among required signatures. The term Accepted signature drops "all" accordingly, and the
Notes give the reason and the floor argument. No signer register is founded. The harness follows the text
(unit 0021). Run from harness/:
    python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_signers_round_2026_10_28.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fi_common as F  # noqa: E402
from govharness.workflows.amend import replace_text  # noqa: E402

DATE = "2026-10-28"
AT = "2026-10-28T12:00:00+00:00"
RECORD = "review-records/round-2026-10-28-signers/decisions.md"

HARN10 = [(
    "A row for \"all\" ledgers SHALL have Last entry \"none\" among signers and From entry \"1\" among required "
    "signatures (GOV.36).",
    "The Ledger of each row among signers SHALL name one ledger, not \"all\". A row for \"all\" ledgers among "
    "required signatures SHALL have From entry \"1\" (GOV.36).")]

TERM = [(
    "by a key whose row among signers has Ledger its ledger or \"all\", Role label its actor,",
    "by a key whose row among signers has Ledger its ledger, Role label its actor,")]

NOTE = (
    "A harness reads the signer register as it stands, so a key leaves only by the closing of its row: a row "
    "removed would leave each signature that the key made without an accepted signature. Each ledger numbers its "
    "own entries, so a Last entry closes a key on one ledger, and a row for \"all\" ledgers would stay open on each "
    "ledger begun after its closing; STND.HARN.10 therefore has each row among signers name one ledger, and a key "
    "that signs on several ledgers has a row for each. A row of required signatures for \"all\" ledgers closes "
    "nothing and stays. STND.HARN.10 binds, because it instantiates GOV.36, and raises no floor (GOV.11): it asks "
    "nothing of a project that has founded no signer register, and of one that founds it only a row for each ledger "
    "that a key signs, in place of one row for all; it asks no decision of the human owner.")

NOTES = [(
    "This standard sets no form for a configuration of an agent's environment; STND.DFLT.22 states when such a "
    "configuration displaces a provision.\n",
    "This standard sets no form for a configuration of an agent's environment; STND.DFLT.22 states when such a "
    f"configuration displaces a provision.\n\n{NOTE}\n")]

READING = (
    "STND.HARN.10 has the Ledger of each row among signers name one ledger, not \"all\", where it had a row for "
    "\"all\" ledgers among signers keep Last entry \"none\", and keeps From entry \"1\" for a row of required "
    "signatures for \"all\" ledgers; the term Accepted signature accepts a key only by its row for the ledger of the "
    "transaction; the Notes state that a key leaves only by the closing of its row, why a row for \"all\" ledgers "
    "is never closed, and the floor argument")
ROW = f"| 1.5 | {DATE} | Minor amendment (GOV.41): {READING}. Transition (GOV.42): none. |"

RATIONALE = (
    f"Minor amendment of STND.HARN, revision 1.5, ratified by the custodian on {DATE}: {READING}. The change is "
    "minor under STND.IDENT.3 because it alters an obligation on the form of the signer register and a defined "
    "meaning. As revision 1.4 read, an open row for \"all\" ledgers accepted its key on every ledger and STND.HARN.10 "
    "kept it open, so that such a key was never retired short of removing its row, which would leave each signature "
    "it had made unaccepted (unit 0016, M1). A row of one ledger overriding the row for \"all\" ledgers would close "
    "the key on each ledger already begun and leave it open on each later one, so the custodian decided that each "
    "row among signers names one ledger (decision 1). STND.HARN.10 binds, because it instantiates GOV.36, and "
    "raises no floor (GOV.11), as the Notes argue. No signer register is founded and this amendment founds none; "
    "signatures stay unadopted, as the custodian directed on 2026-10-26 and again on 2026-10-28. Transition "
    f"(GOV.42): none, since no signer register exists. Decision 1 of {RECORD}; the open item of unit 0016, "
    "harness/records/units/0016-ledger-fixes.md; harness/records/units/0021-signer-rows.md." + F.AUTHOR)


def apply(root: Path) -> None:
    root = Path(root)
    replace_text(root, "STND/HARN/10.md", HARN10)
    if F.B.derive_fields(root, ["STND.HARN.10"])["STND.HARN.10"].unresolved:
        raise ValueError("STND.HARN.10: unresolved identifiers")
    replace_text(root, "STND/HARN/_doc.md", TERM + NOTES)
    F.finish(root, "STND/HARN", "STND.HARN", "1.4", "1.5", ROW, RATIONALE, AT)
