"""Round e of 2026-10-28: the steps of the round and how each is recorded.

A step edits one document and records one transaction. Its revision is computed from the field `revision` as the
earlier rounds leave it, so that the round runs again after a revision of round o. The rationale follows the form of
the earlier rounds: the reading, the class under STND.IDENT.3 and why, the floor argument (GOV.11), the class onset,
the transition (GOV.42), the rulings and register entries relied on, and the authorship sentence.
"""
from __future__ import annotations

import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import rounds_common as F  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction, replace_text  # noqa: E402

RECORD = "review-records/rounds-2026-10-28/round-e/decisions.md"
REGISTER = "review-records/deep-review-2026-10-28/register.md"
LVL0_SCOPE = ["LVL0", "PRIN", "PRIME", "GUARD", "VV", "REPRO", "INTPR", "DSGN", "SIMPL", "RSRC", "QA", "GOV", "LEX"]
SUBPROFILE_PARENTS = ("HW", "HDES")


@dataclass(frozen=True)
class Step:
    """One document's transaction.

    edit changes the files; minor selects the class; reading is the change in words; because says why it has that
    class; floor is the floor argument; onset the class onset; transition the transition (GOV.42); sources the
    rulings and register entries relied on.
    """

    doc_id: str
    edit: Callable[[Path], None]
    minor: bool
    reading: str
    because: str
    floor: str
    onset: str
    transition: str
    sources: str


def ruling(*items: str) -> str:
    """Return the citation of rulings in the form of the earlier rounds."""
    if len(items) == 1:
        return f"Ruling {items[0]} of {F.RECORD}"
    joined = " and ".join(items) if len(items) == 2 else ", ".join(items[:-1]) + f", and {items[-1]}"
    return f"Rulings {joined} of {F.RECORD}"


def body_of(root: Path, rel: str) -> str:
    return (Path(root) / rel).read_text(encoding="utf-8").partition("\n---\n\n")[2]


def edit(root: Path, rel: str, pairs: list[tuple[str, str]], **fields: object) -> None:
    """Replace texts, each occurring once, in a file, and set the front-matter fields given."""
    if pairs:
        replace_text(root, rel, pairs)
    if fields:
        F.set_body(root, rel, body_of(root, rel), **fields)


def provision(doc_id: str, n: int, title: str, section: str, mode: str, instantiates: list[str],
              refers_to: list[str], body: str, onset: str | None, defines: list[str] | None = None) -> str:
    """Return the file text of a LVL2 provision; rank and waivable are derived afterwards (F.check_fields)."""
    lines = ["---", f'id: "{doc_id}.{n}"', 'level: "LVL2"', 'kind: "provision"', f"title: {B.q(title)}",
             f"section: {B.q(section)}", 'status: "adopted"', f'adopted: "{F.DATE}"', f'mode: "{mode}"']
    if onset is not None:
        lines.append(f'onset: "{onset}"')
    lines += ["binding_reason: null", f"instantiates: {B.q(instantiates)}", f"refers_to: {B.q(refers_to)}",
              "rank: null", "waivable: false", f"defines: {B.q(defines or [])}", 'checked_by: ["review"]', "---",
              "", body, ""]
    return "\n".join(lines)


def add_provision(root: Path, folder: str, text: str) -> None:
    ident = re.search(r'^id: "([^"]+)"$', text, flags=re.M).group(1)
    path = Path(root) / folder / f"{ident.rsplit('.', 1)[1]}.md"
    if path.exists():
        raise ValueError(f"{ident} exists")
    path.write_text(text, encoding="utf-8")


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


def folder_of(doc_id: str) -> str:
    return doc_id.replace(".", "/")


def texts(step: Step, new: str) -> tuple[str, str]:
    """Return the revision row and the rationale of a step."""
    kind = "Minor" if step.minor else "Editorial"
    tail = "" if step.minor else "; no obligation, permission, or defined meaning changes"
    row = f"| {new} | {F.DATE} | {kind} amendment (GOV.41): {step.reading}{tail}. |"
    rationale = (
        f"{kind} amendment of {step.doc_id}, revision {new}, ratified by the custodian on {F.DATE}: {step.reading}. "
        f"The change is {kind.lower()} under STND.IDENT.3 because {step.because}. {step.floor}. Class onset: "
        f"{step.onset}. Transition (GOV.42): {step.transition}. {step.sources}; {RECORD}." + F.AUTHOR)
    return row, rationale


def record(root: Path, doc_id: str, scope: str, rationale: str, at: str, label: str) -> None:
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.41"], targets=[doc_id], scope=[scope],
                                          rationale=rationale))
    print("seq", rec.entry["seq"], doc_id, label)


def run(root: Path, step: Step, at: str) -> None:
    """Apply one step and record its transaction."""
    root = Path(root)
    step.edit(root)
    folder = folder_of(step.doc_id)
    old = revision_of(root, folder)
    new = next_revision(old, step.minor)
    row, rationale = texts(step, new)
    if folder.split("/")[0] in SUBPROFILE_PARENTS and "/" in folder:
        raise_revision(root, folder, old, new, row)
        B.write_references(root, [step.doc_id])
        record(root, step.doc_id, folder.split("/")[0], rationale, at, new)
    else:
        F.finish(root, folder, step.doc_id, old, new, row, rationale, at)
