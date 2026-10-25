"""check_refs.py with the exclusions proposed for unit 0013 (a demonstration, not a harness change).

Usage (from REPO/harness): PYTHONPATH=. python3 -B ../review-records/round-2026-10-25-close/p5/check_refs_0013.py <root> [DOC ...]
Differences from tools/check_refs.py:
  1. Only documents at LVL1 to LVL3 are read, the documents STND.DRAFT.34 asks to hold References and
     g.25 checks; LVL0 and its parts, and entries of level null (MNEM, KNOW, TAG and its facets), are not.
  2. The section Revision History is removed with the heading the harness uses (core.tables.HISTORY_HEADING);
     the pattern of check_refs.py, "Revision history", never matches it.
  3. A table whose header names a column Example is a table of mentioned identifiers, and none of its rows
     is read.
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
