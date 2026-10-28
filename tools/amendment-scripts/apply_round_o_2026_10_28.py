"""Round o of 2026-10-28: one onset rule and an onset field in each provision (ruling C7; register entries R4.1
and R4.2, with CS1, CS2, CS4, CS5, CS6, CS18, CP4, CP5, CP6, CP12, CL1, and CL2).

Forty-three transactions, one per document, in citation order: STND.DRAFT defines the field `onset`; STND.CLASS
gives it force in STND.CLASS.10 and states the one rule in its Notes; then every profile and standard with a
waivable provision carries the field on each such provision, from the table of `round_o_fields`, and its Notes on
class onset become one sentence citing STND.CLASS.10 and the fields (`round_o_text`).

Each revision is computed from the field `revision` as the earlier rounds leave it, and each edit of text from the
paragraph and the sentences it opens with, so that the module runs again after a revision of round c.

Run from harness/, through the driver, on top of the finished rounds:
    ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28,apply_round_c_2026_10_28,apply_round_o_2026_10_28 \\
        python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction  # noqa: E402
import round_o_fields as FL  # noqa: E402
import round_o_text as T  # noqa: E402

AT = "2026-10-28T22:00:00+00:00"
RECORD = "review-records/rounds-2026-10-28/round-o/decisions.md"
SOURCES = "entries R4.1 and R4.2 of the register"

FIELDS = ("each provision proportioned to class carries the field onset, with the class from which it applies "
          "under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields")
EDITORIAL_BECAUSE = ("every onset that a field states is the onset that the Notes gave under STND.CLASS.10, and the "
                     "Notes are informative, so no obligation, permission, or defined meaning of this document changes")
CODE_FORM_FLOOR = (
    "Each move to CSQ3 asks work of CSQ3 for something it did not owe before, and rests on the reading of ruling C7 "
    "that the form of code and the catch of a failure at a foreign frame move to CSQ3; the burden is proportionate, "
    "since each asks a type, an attribute, a declaration, or a catch at the time the code is written, which costs "
    "nothing then and a rewrite of each interface when it is added at a reclassification, and work of CSQ4 may still "
    "omit it")
LIGHTER_FLOOR = ("Each move to CSQ2 removes an obligation from work of CSQ3 and leaves work of CSQ4 as it was, while "
                 "the obligations of LVL0 that the moved provisions serve apply at CSQ3 in full")

# document: (class, reading, floor argument, onset, transition, sources); None marks an editorial amendment.
MINOR = {
    "STND.CLASS": (
        "STND.CLASS.10 applies each part of a provision below LVL0 from the class that the field onset of the "
        "provision gives, and the Notes state the one rule by which the fields are set: a part applies from the row "
        "of the table whose named item it asks for, and otherwise from CSQ3",
        "No floor is raised (GOV.11): STND.CLASS.10 stays a default, a class that a field gives reaches only work of "
        "CSQ3 or a more severe class, work of CSQ4 may still omit every obligation above the floor, and the rule "
        "moves no onset by itself, each move standing in the transaction of the document that makes it",
        "unchanged; STND.CLASS.10 gives the fields their force",
        "a document keeps the onsets that its Notes gave until its own transaction of this round sets the field",
        "CS1, CP12"),
    "HW": (
        "HW.5, HW.6, and HW.7 apply from CSQ2, with the contract of HW.4 that they fill, and HW.3 and HW.12 stay at "
        f"CSQ3; {FIELDS}",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}",
        "HW.5, HW.6, and HW.7 from CSQ2, where they applied from CSQ3; the others as before",
        "a contract, its evidence, or its confirmation that work of CSQ3 holds is kept; work reclassified to CSQ2 "
        "owes them under STND.CLASS.22",
        "CS1, CS2"),
    "HW.CPU": (
        f"HW.CPU.3 applies from CSQ2, with the delivered arithmetic of HW.5 that it confirms; {FIELDS}",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}",
        "HW.CPU.3 from CSQ2, where it applied from CSQ3; the others as before",
        "a confirmation that work of CSQ3 makes is kept; work reclassified to CSQ2 owes it under STND.CLASS.22",
        "CS1, CS2"),
    "HW.FPGA": (
        f"HW.FPGA.4 applies from CSQ2, the class from which its trigger, a property that the design record marks "
        f"under HDES.5, exists; {FIELDS}",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}; at CSQ3 the provision asked nothing, since HDES.5 applies "
        "from CSQ2",
        "HW.FPGA.4 from CSQ2, where it applied from CSQ3; the others as before",
        "none",
        "CS1, CS18"),
    "HW.ASIC": (
        f"HW.ASIC.4 applies from CSQ2, the class from which its trigger, a property that the design record marks "
        f"under HDES.5, exists; {FIELDS}",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}; at CSQ3 the provision asked nothing, since HDES.5 applies "
        "from CSQ2",
        "HW.ASIC.4 from CSQ2, where it applied from CSQ3; the others as before",
        "none",
        "CS1, CS18"),
    "STND.CODE": (
        "the first sentence of STND.CODE.22, STND.CODE.23, STND.CODE.24, and STND.CODE.35 apply from CSQ3, as rules "
        f"of the form of code and the catch at a foreign frame, and the comparison of layouts stays at CSQ2; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}; STND.CODE.35, a rule of the same kind that the lists of the "
        "review do not name, is put to the custodian",
        "the first sentence of STND.CODE.22, STND.CODE.23, STND.CODE.24, and STND.CODE.35 from CSQ3, where they "
        "applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CL1, CL2"),
    "STND.CONC": (
        f"STND.CONC.19 applies from CSQ3, as a rule of the form of code; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}; the move is put to the custodian, since the lists of the "
        "review do not name it",
        "STND.CONC.19 from CSQ3, where it applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CS5"),
    "STND.FTN": (
        "STND.FTN.6, the first sentence of STND.FTN.12, STND.FTN.24, and the second sentence of STND.FTN.27 apply "
        f"from CSQ3, as rules of the form of code; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}",
        "STND.FTN.6, the first sentence of STND.FTN.12, STND.FTN.24, and the second sentence of STND.FTN.27 from "
        "CSQ3, where they applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CL1"),
    "STND.JL": (
        f"STND.JL.39 applies from CSQ3, with the catch of STND.CODE.24 at a foreign frame; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}",
        "STND.JL.39 from CSQ3, where it applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CL2"),
    "STND.MPI": (
        "STND.MPI.14 and the second sentence of STND.MPI.17 apply from CSQ3, as rules of the form of code, and the "
        "argument of completion in the second sentence of STND.MPI.12 applies from CSQ3, with that of STND.CONC.11, "
        f"while the tests under the check of deadlock stay at CSQ2; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}; the argument of completion costs one argument for each "
        "message protocol, which STND.CONC.11 already asks of every protocol by which concurrent tasks wait at CSQ3; "
        "the three moves are put to the custodian, since the lists of the review do not name them",
        "STND.MPI.14, the second sentence of STND.MPI.12, and the second sentence of STND.MPI.17 from CSQ3, where "
        "they applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it, and an existing protocol carries its argument "
        "at the next change of the protocol (STND.CLASS.22)",
        "CS1, CS5"),
    "STND.OFFLD": (
        "STND.OFFLD.7, the first sentence of STND.OFFLD.12, and the second sentence of STND.OFFLD.17 apply from CSQ3, "
        f"as rules of the form of code, and STND.OFFLD.14 follows HW.5 to CSQ2; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}; the three moves are put to the custodian, since the lists "
        "of the review do not name them",
        "STND.OFFLD.7, the first sentence of STND.OFFLD.12, and the second sentence of STND.OFFLD.17 from CSQ3, "
        "where they applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CS6"),
    "STND.OMP": (
        f"STND.OMP.28 applies from CSQ3, as a rule of the form of code, with HW.19; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}; the move is put to the custodian, since the lists of the "
        "review do not name it",
        "STND.OMP.28 from CSQ3, where it applied from CSQ2; STND.OMP.30 stays at CSQ2, now with HW.5; the others as "
        "before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CS6"),
    "STND.PY": (
        f"STND.PY.35 applies from CSQ3, with the catch of STND.CODE.24 at a foreign frame; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}",
        "STND.PY.35 from CSQ3, where it applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CL2"),
    "STND.RUST": (
        "STND.RUST.24, STND.RUST.25, and STND.RUST.26 apply from CSQ3, as rules of the form of code and of unwinding "
        f"at a foreign frame; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}",
        "STND.RUST.24, STND.RUST.25, and STND.RUST.26 from CSQ3, where they applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CL1, CL2"),
    "STND.STDC": (
        "STND.STDC.7 and the row of STND.CXX.7 in the table of STND.STDC.1 apply from CSQ3, as rules of the form of "
        f"code; {FIELDS}",
        f"No floor is raised (GOV.11). {CODE_FORM_FLOOR}",
        "STND.STDC.7 and the C reading of STND.CXX.7 from CSQ3, where they applied from CSQ2; the others as before",
        "existing source conforms at the next change that touches it (STND.CLASS.22)",
        "CS1, CL1"),
    "STND.TEST": (
        "the records of the standard start at CSQ2: STND.TEST.1, STND.TEST.5, the record of an omission in the "
        "second sentence of STND.TEST.3, the rows Selection, Reused verdicts, and Omitted tests of STND.TEST.9, and "
        "the reason of the third sentence of STND.TEST.10; the statement route of STND.TEST.2 stands at CSQ3, and "
        f"the Notes no longer put it to the custodian; {FIELDS}",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}",
        "STND.TEST.1 and STND.TEST.5, the second sentence of STND.TEST.3, three rows of STND.TEST.9, and the third "
        "sentence of STND.TEST.10 from CSQ2, where they applied from CSQ3; the others as before",
        "records that work of CSQ3 keeps are kept; work reclassified to CSQ2 keeps them from its next run",
        "CS1, CP6, CP12"),
    "STND.VVUQ": (
        "a core of STND.VVUQ.1, STND.VVUQ.3, STND.VVUQ.5, STND.VVUQ.7, STND.VVUQ.13, STND.VVUQ.17, STND.VVUQ.62, "
        "STND.VVUQ.64, and STND.VVUQ.82 applies from CSQ3, and every other default from CSQ2; the Notes state the "
        "onset of the standard, which they did not before",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}",
        "the core from CSQ3, as every default applied through NUMER before; every other default from CSQ2",
        "evidence that work of CSQ3 holds by the moved provisions is kept; work reclassified to CSQ2 meets them "
        "under STND.CLASS.22",
        "CS1, CP5"),
    "STND.WFLOW": (
        "the run machinery starts at CSQ2: the second sentence of STND.WFLOW.6, with its first, and STND.WFLOW.19, "
        "STND.WFLOW.30, STND.WFLOW.34, STND.WFLOW.36, STND.WFLOW.37, and STND.WFLOW.40, while STND.WFLOW.15 stays at "
        f"CSQ1 and the two sentences of STND.WFLOW.35 stand together at CSQ2; {FIELDS}",
        f"No floor is raised (GOV.11). {LIGHTER_FLOOR}",
        "the second sentence of STND.WFLOW.6 and STND.WFLOW.19, STND.WFLOW.30, STND.WFLOW.34, STND.WFLOW.36, "
        "STND.WFLOW.37, and STND.WFLOW.40 from CSQ2, where they applied from CSQ3; the others as before",
        "records and tests that work of CSQ3 keeps are kept; work reclassified to CSQ2 meets the moved provisions "
        "under STND.CLASS.22",
        "CS1, CP4, CP12"),
}

EDITORIAL_READING = {
    "STND.DRAFT": ("the section Representation in the harness defines the field onset, and each waivable provision "
                   "carries it with CSQ3, the onset that STND.CLASS.10 gave it"),
    "STND.SV": f"{FIELDS}, and the tightening of the five sentences that add to a verdict or a figure is kept",
}
EDITORIAL_SOURCES = {"STND.DRAFT": "CS1", "ML": "CS1, CS4", "CPS": "CS1, CS4"}


def next_revision(revision: str, minor: bool) -> str:
    parts = [int(x) for x in revision.split(".")]
    if minor:
        return f"{parts[0]}.{parts[1] + 1}"
    if len(parts) == 2:
        return f"{revision}.1"
    return f"{parts[0]}.{parts[1]}.{parts[2] + 1}"


def revision_of(root: Path, folder: str) -> str:
    text = (Path(root) / folder / "_doc.md").read_text(encoding="utf-8")
    found = re.findall(r'^revision: "([0-9.]+)"$', text, flags=re.M)
    if len(found) != 1:
        raise ValueError(f"{folder}: {len(found)} revision fields")
    return found[0]


def entry_of(doc_id: str, old: str) -> tuple[str, str, str]:
    """Return the new revision, the history row, and the rationale of one document."""
    if doc_id in MINOR:
        reading, floor, onset, transition, sources = MINOR[doc_id]
        new = next_revision(old, True)
        row = f"| {new} | {F.DATE} | Minor amendment (GOV.41): {reading}. |"
        rationale = (
            f"Minor amendment of {doc_id}, revision {new}, ratified by the custodian on {F.DATE}: {reading}. The "
            "change is minor under STND.IDENT.3 because it alters when obligations apply, without altering the "
            f"motivation or intent of the governance. {floor}. Class onset: {onset}. Transition (GOV.42): "
            f"{transition}. Ruling C7 of {F.RECORD}; {SOURCES}, with {sources}; {RECORD}." + F.AUTHOR)
        return new, row, rationale
    reading = EDITORIAL_READING.get(doc_id, FIELDS)
    sources = EDITORIAL_SOURCES.get(doc_id, "CS1")
    new = next_revision(old, False)
    row = (f"| {new} | {F.DATE} | Editorial amendment (GOV.41): {reading}; no obligation, permission, or defined "
           "meaning changes. |")
    rationale = (
        f"Editorial amendment of {doc_id}, revision {new}, ratified by the custodian on {F.DATE}: {reading}. The "
        f"change is editorial under STND.IDENT.3 because {EDITORIAL_BECAUSE}. No floor is raised (GOV.11): no onset "
        "moves. Class onset: unchanged, each now stated in the field onset. Transition (GOV.42): none. Ruling C7 of "
        f"{F.RECORD}; {SOURCES}, with {sources}; {RECORD}." + F.AUTHOR)
    return new, row, rationale


def order() -> list[str]:
    rest = [d for d in FL.documents() if d not in ("STND.DRAFT", "STND.CLASS")]
    return ["STND.DRAFT", "STND.CLASS", *rest]


def apply_document(root: Path, doc_id: str, at: str) -> None:
    folder = doc_id.replace(".", "/")
    T.apply_notes(root, doc_id)
    FL.apply_fields(root, doc_id)
    old = revision_of(root, folder)
    new, row, rationale = entry_of(doc_id, old)
    if "/" in folder and not folder.startswith("STND/"):
        finish_subprofile(root, folder, doc_id, old, new, row, rationale, at)
    else:
        F.finish(root, folder, doc_id, old, new, row, rationale, at)


def finish_subprofile(root: Path, folder: str, doc_id: str, old: str, new: str, row: str, rationale: str,
                      at: str) -> None:
    """Record a sub-profile under the scope of its profile's directory, as every earlier transaction did."""
    raise_revision(root, folder, old, new, row)
    B.write_references(root, [doc_id])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.41"], targets=[doc_id], scope=[folder.split("/")[0]],
                                          rationale=rationale))
    print("seq", rec.entry["seq"], doc_id, new)


STEPS = order()
TRANSACTIONS = len(STEPS)


def apply(root: Path) -> None:
    root = Path(root)
    start = datetime.fromisoformat(AT)
    for k, doc_id in enumerate(STEPS):
        apply_document(root, doc_id, (start + timedelta(seconds=k)).isoformat())
