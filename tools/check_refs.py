"""Check that every document named in a document's text is in its References.

Usage (from REPO/harness): PYTHONPATH=. python3 -B ../tools/check_refs.py <root> [DOC ...]
A document is named when its identifier appears as a bare word (e.g. "HDES", "STND.DOCS")
outside quoted spans, or through a provision identifier. Reports names missing from the
derived References (references.cited_documents).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from govharness.core.corpus import read_corpus
from govharness.core.entry import DOC_FILE
from govharness.core.text import unquoted
from govharness.derive.references import cited_documents, without_section

HISTORY = re.compile(r"^## Revision history\s*\n.*?(?=^## |\Z)", re.M | re.S)


def main() -> int:
    root = Path(sys.argv[1])
    corpus = read_corpus(root)
    docs = sorted(str(e.meta["id"]) for e in corpus.entries if e.path.name == DOC_FILE)
    docset = set(docs)
    wanted = sys.argv[2:] or docs
    pat = re.compile(r"(?<![A-Za-z0-9.])((?:[A-Z]{2,5}\d?)(?:\.[A-Z]{2,5})*)(?![A-Za-z0-9])")
    bad = 0
    for doc_id in wanted:
        doc = corpus.by_id[doc_id]
        members = [doc] + [e for e in corpus.entries
                           if e.path.parent == doc.path.parent and e.path.name != DOC_FILE]
        named = set()
        for e in members:
            text = unquoted(HISTORY.sub("", without_section(e.body)))
            text = re.sub(r"`[^`]*`", " ", text)
            for m in pat.finditer(text):
                name = m.group(1)
                # strip a trailing provision part is not possible here; bare names only
                if name in docset and name != doc_id and name != "LVL0":
                    named.add(name)
        cited = set(cited_documents(corpus, doc_id))
        missing = sorted(named - cited)
        if missing:
            bad += 1
            print(f"{doc_id}: named but not in References: {', '.join(missing)}")
    print(f"checked {len(wanted)} documents; {bad} with missing rows")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
