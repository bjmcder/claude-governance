"""Write the round's documents into a corpus root and derive their fields."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/claude/harness")
from govharness.core.corpus import Corpus, load_entries, read_tree
from govharness.checks.lineage.derivation import derive
from govharness.checks.logic.facts import facts_of  # noqa
from govharness.derive.references import rewrite_sections
try:
    import content as C
except ImportError:
    import content3 as C


def q(v):
    return json.dumps(v, ensure_ascii=False)


def provision_text(doc_id, p, status, adopted, rank=None, waivable=False):
    lines = ["---", f'id: "{doc_id}.{p["n"]}"', 'level: "LVL2"', 'kind: "provision"',
             f'title: {q(p["title"])}', f'section: {q(p["section"])}', f'status: "{status}"']
    if adopted:
        lines.append(f'adopted: "{adopted}"')
    lines += [f'mode: "{p["mode"]}"',
              f'binding_reason: {q(p["binding_reason"]) if p["binding_reason"] else "null"}',
              f'instantiates: {q(p["instantiates"])}', f'refers_to: {q(p["refers_to"])}',
              f'rank: {"null" if rank is None else rank}', f'waivable: {"true" if waivable else "false"}',
              f'defines: {q(p["defines"])}', f'checked_by: {q(p["checked_by"])}', "---", "", p["body"], ""]
    return "\n".join(lines)


def doc_text(d, status, revision, adopted, history_rows):
    lines = ["---", f'id: "{d["id"]}"', 'level: "LVL2"', 'kind: "standard"', f'title: {q(d["title"])}',
             f'status: "{status}"', f'revision: "{revision}"']
    if adopted:
        lines.append(f'adopted: "{adopted}"')
    lines += ['adopted_by: "The Custodian"', f'instantiates: {q(d["instantiates"])}', "rank: null",
              "waivable: false", "---", ""]
    for head, body in d["sections"]:
        lines += [f"## {head}", "", body.strip(), ""]
    lines += ["## References", "", "| Identifier | Title |", "| --- | --- |", "",
              "## Revision History", "", "| Revision | Date | Change |", "| --- | --- | --- |", *history_rows, ""]
    return "\n".join(lines)


def floor_ids(root):
    from govharness.checks.base import CheckContext  # noqa
    # GOV.10 floor list, as facts.py computes it
    return {"REPRO.5", "QA.1", "INTPR.2", "VV.7"}


def derive_fields(root: Path, ids: list[str]):
    """Rewrite rank and waivable of the named provisions from the corpus."""
    corpus = Corpus(load_entries(read_tree(root)))
    fl = floor_ids(root)
    out = {}
    for ident in ids:
        e = corpus.by_id[ident]
        d = derive(corpus, e, fl)
        out[ident] = d
        path = e.path if e.path.is_absolute() else root / e.path
        t = path.read_text()
        import re
        t = re.sub(r"^rank: .*$", f'rank: {"null" if d.rank is None else d.rank}', t, count=1, flags=re.M)
        t = re.sub(r"^waivable: .*$", f'waivable: {"true" if d.waivable else "false"}', t, count=1, flags=re.M)
        path.write_text(t)
    return out


def write_references(root: Path, doc_ids):
    tree = read_tree(root)
    corpus = Corpus(load_entries(tree))
    for rel, text in rewrite_sections(tree, corpus, list(doc_ids)).items():
        (root / rel).write_text(text, encoding="utf-8")


def write_new_doc(root: Path, d, status="adopted", revision="1.0", adopted=C.DATE, rows=None):
    folder = root / Path(*d["id"].split("."))
    folder.mkdir(parents=True, exist_ok=True)
    rows = rows or [f"| 1.0 | {adopted} | Adopted. |"]
    (folder / "_doc.md").write_text(doc_text(d, status, revision, adopted if status == "adopted" else None, rows))
    for p in d["provisions"]:
        (folder / f'{p["n"]}.md').write_text(provision_text(d["id"], p, status, adopted if status == "adopted" else None))
    ids = [f'{d["id"]}.{p["n"]}' for p in d["provisions"]]
    res = derive_fields(root, ids)
    for ident, r in res.items():
        p = next(x for x in d["provisions"] if f'{d["id"]}.{x["n"]}' == ident)
        if r.forced and p["mode"] != "binding":
            raise ValueError(f"{ident}: forced binding but mode {p['mode']}")
        if r.unresolved:
            raise ValueError(f"{ident}: unresolved {r.unresolved}")
    write_references(root, [d["id"]])
    return res
