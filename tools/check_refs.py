"""Check that every document named in a document's text is in its References.

Usage (from REPO/harness): PYTHONPATH=. python3 -B ../tools/check_refs.py <root> [DOC ...]
A document is named when its identifier appears as a bare word (e.g. "HDES", "STND.DOCS")
outside quoted spans and code, or through a provision identifier. Reports names missing from
the derived References (references.cited_documents). It reads, by default, only documents at
LVL1 to LVL3, the documents STND.DRAFT.34 asks to hold References; it skips the Revision History
(core.tables.HISTORY_HEADING) and every row of a table whose header names a column Example,
a table of mentioned identifiers.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from govharness.core.corpus import read_corpus
from govharness.core.entry import DOC_FILE
from govharness.core.tables import HISTORY_HEADING
from govharness.core.text import unquoted
from govharness.derive.references import cited_documents, without_section

HISTORY = re.compile(rf"^{re.escape(HISTORY_HEADING)}\s*\n.*?(?=^## |\Z)", re.M | re.S)
NAME = re.compile(r"(?<![A-Za-z0-9.])((?:[A-Z]{2,5}\d?)(?:\.[A-Z]{2,5})*)(?![A-Za-z0-9])")
LEVELS = {"LVL1", "LVL2", "LVL3"}


def without_example_tables(text: str) -> str:
    out, skipping = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not skipping and "Example" in cells:
                skipping = True
            if skipping:
                continue
        else:
            skipping = False
        out.append(line)
    return "\n".join(out)


def main() -> int:
    root = Path(sys.argv[1])
    corpus = read_corpus(root)
    docs = sorted(str(e.meta["id"]) for e in corpus.entries if e.path.name == DOC_FILE)
    docset = set(docs)
    wanted = sys.argv[2:] or [d for d in docs if str(corpus.by_id[d].meta.get("level")) in LEVELS]
    bad = 0
    for doc_id in wanted:
        doc = corpus.by_id[doc_id]
        members = [doc] + [e for e in corpus.entries
                           if e.path.parent == doc.path.parent and e.path.name != DOC_FILE]
        named = set()
        for e in members:
            text = without_example_tables(unquoted(HISTORY.sub("", without_section(e.body))))
            text = re.sub(r"`[^`]*`", " ", text)
            named |= {m.group(1) for m in NAME.finditer(text)
                      if m.group(1) in docset and m.group(1) not in (doc_id, "LVL0")}
        missing = sorted(named - set(cited_documents(corpus, doc_id)))
        if missing:
            bad += 1
            print(f"{doc_id}: named but not in References: {', '.join(missing)}")
    print(f"checked {len(wanted)} documents; {bad} with missing rows")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
