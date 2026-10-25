"""Report the documents whose References the harness check g.25 rejects.

Usage (from REPO/harness): PYTHONPATH=. python3 -B ../tools/check_refs.py <root> [DOC ...]

A thin wrapper of g.25 (`govharness.checks.drafting.citations`, unit 0013), kept so that the
briefs and records that name this script still work; `python3 -B -m govharness verify <root>`
runs the same check with the others. g.25 compares each References table with the one derived
from the document's citations, and fails when the text names a document by its bare identifier
(e.g. "HDES", "STND.DOCS") without citing it. It reads the documents at LVL1 to LVL3, the
documents STND.DRAFT.34 asks to hold References, and leaves out the Revision History, every row
of a table whose header names a column Example, quoted spans, and code.

Unlike `verify`, this script prints every finding of g.25, including those of drafts, which
`verify` only lists. With DOC arguments it prints only the findings of those documents.
Exit status: 1 when it prints a finding, else 0.
"""
from __future__ import annotations

import sys
from pathlib import Path

from govharness.checks.drafting.citations import references_listed
from govharness.checks.drafting.context import BELOW, build_context
from govharness.core.corpus import read_corpus


def main(argv: list[str]) -> int:
    """Print the g.25 findings of a corpus and a summary line.

    Parameters
    ----------
    argv : list[str]
        The corpus root, then optional document identifiers.

    Returns
    -------
    int
        1 when a finding is printed, else 0; 2 on a usage error.
    """
    if not argv:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    drafting = build_context(read_corpus(Path(argv[0])))
    if drafting is None:
        print("no drafting standard in the corpus", file=sys.stderr)
        return 2
    subjects = [u.subject for u in drafting.units_for(BELOW, {"informative", "body"})]
    wanted = argv[1:] or subjects
    findings = [f for f in references_listed(drafting) if f.subject in wanted]
    for finding in findings:
        print(f"{finding.subject}: {finding.text}")
    print(f"checked {len(set(wanted) & set(subjects))} documents; {len(findings)} with missing rows")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
