"""Helpers of the rounds of 2026-10-28, which carry the rulings on the deep review of that date."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
from govharness.workflows.amend import Change, raise_revision, record_transaction  # noqa: E402

DATE = "2026-10-28"
RECORD = "review-records/deep-review-2026-10-28/rulings.md"
AUTHOR = (" Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5)."
          " Under the ruling of ledger entry 15, this decision is the QA.7 review.")


def swap_para(root: Path, rel: str, start: str, new: str) -> None:
    """Replace the one paragraph of a file that opens with the given words; refuse if not exactly one does."""
    path = Path(root) / rel
    paras = path.read_text(encoding="utf-8").split("\n\n")
    hits = [i for i, p in enumerate(paras) if p.startswith(start)]
    if len(hits) != 1:
        raise ValueError(f"{rel}: {start[:60]!r} opens {len(hits)} paragraphs, not one")
    paras[hits[0]] = new
    path.write_text("\n\n".join(paras), encoding="utf-8")


def set_body(root: Path, rel: str, body: str, **fields: object) -> None:
    """Replace the body of a provision file, and the front-matter fields given, each written as JSON."""
    path = Path(root) / rel
    text = path.read_text(encoding="utf-8")
    head, sep, _ = text.partition("\n---\n\n")
    if not sep:
        raise ValueError(f"{rel}: no front matter")
    for key, value in fields.items():
        line = f"{key}: {B.q(value)}"
        head, n = re.subn(rf"^{key}: .*$", lambda _m, line=line: line, head, count=1, flags=re.M)
        if n != 1:
            raise ValueError(f"{rel}: no field {key}")
    path.write_text(head + sep + body.strip() + "\n", encoding="utf-8")


def withdraw(root: Path, folder: str, doc_id: str, numbers: list[int]) -> None:
    """Delete the provisions and list them in the field withdrawn of the document, after any already there."""
    root = Path(root)
    for n in numbers:
        (root / folder / f"{n}.md").unlink()
    path = root / folder / "_doc.md"
    text = path.read_text(encoding="utf-8")
    ids = ", ".join(f'"{doc_id}.{n}"' for n in numbers)
    if re.search(r"^withdrawn: \[", text, flags=re.M):
        text = re.sub(r"^(withdrawn: \[.*)\]$", lambda m: f"{m.group(1)}, {ids}]", text, count=1, flags=re.M)
    else:
        text = text.replace("waivable: false\n---", f"waivable: false\nwithdrawn: [{ids}]\n---", 1)
    path.write_text(text, encoding="utf-8")


def check_fields(root: Path, ids: list[str], binding: bool = False) -> None:
    """Refuse unresolved identifiers; refuse a forced binding as well unless the provisions are meant to bind."""
    res = B.derive_fields(Path(root), ids)
    for ident, r in res.items():
        if r.unresolved or (r.forced and not binding):
            raise ValueError(f"{ident}: {r}")


def finish(root: Path, folder: str, doc_id: str, old: str, new: str, row: str, rationale: str, at: str) -> None:
    root = Path(root)
    raise_revision(root, folder, old, new, row)
    B.write_references(root, [doc_id])
    rec = record_transaction(root, Change(kind="amend", actor="The Custodian", role="custodians", at=at,
                                          authority=["GOV.41"], targets=[doc_id], scope=[folder],
                                          rationale=rationale))
    print("seq", rec.entry["seq"], doc_id, new)
