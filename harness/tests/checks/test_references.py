"""Tests of g.25 on bare document names (unit 0013).

g.25 fails when a document at LVL1 to LVL3 names another document by its
bare identifier, outside its Revision History, tables of examples,
quoted spans, and code, without citing it; the derived References table
then lacks the row. Each case changes an in-memory copy of the corpus.
STND.CLASS is the subject: it is adopted, below the drafting standard,
and does not cite HDES, the document the cases name.
"""

from __future__ import annotations

import subprocess
import sys
import unittest

from govharness.checks.base import CheckContext
from govharness.checks.drafting import family as drafting
from govharness.checks.drafting.citations import (
    named_documents,
    references_problem,
)
from govharness.checks.drafting.context import BELOW, build_context
from govharness.checks.registry import run_checks
from govharness.core.corpus import Corpus
from govharness.derive.references import (
    SECTION,
    cited_documents,
    references_table,
    with_section,
)
from tests.support import REPO, ROOT, Index, corpus_of, live_index

SUBJECT = "STND.CLASS"
NAMED = "HDES"
WRAPPER = REPO.parent / "tools" / "check_refs.py"


def inserted(text: str, doc: str = SUBJECT) -> Index:
    """Return a copy of the corpus with text before a References section.

    Parameters
    ----------
    text : str
        Markdown inserted, as paragraphs of its own, in the informative
        text before the section.
    doc : str
        Identifier of the document changed.

    Returns
    -------
    Index
        The changed copy.
    """
    index = live_index()
    entry = index[doc]
    entry.body = entry.body.replace(
        f"## {SECTION}", f"{text}\n\n## {SECTION}", 1
    )
    return index


def g25(index: Index) -> str:
    """Return the status of g.25 on a copy of the corpus.

    Parameters
    ----------
    index : Index
        Entries by identifier.

    Returns
    -------
    str
        ``PASS``, ``INFO``, ``WARN``, or ``FAIL``.
    """
    report = run_checks((drafting,), CheckContext(corpus_of(index)))
    (result,) = [r for r in report.results if r.key == "g.25"]
    return result.status


def rederived(corpus: Corpus, doc: str) -> str:
    """Return a document's body with its References table derived again.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc : str
        Identifier of the document.

    Returns
    -------
    str
        The body, its section set to the derived table.
    """
    block = f"## {SECTION}\n\n{references_table(corpus, doc)}\n\n"
    return with_section(corpus.by_id[doc].body, block)


class BareNames(unittest.TestCase):
    """A bare document name needs a citation, outside mentions."""

    def test_precondition(self) -> None:
        """Behavior: the subject neither cites nor names HDES.

        Reference: the live corpus, on which every case below builds.
        """
        corpus = corpus_of(live_index())
        self.assertNotIn(NAMED, cited_documents(corpus, SUBJECT))
        self.assertNotIn(NAMED, named_documents(corpus, SUBJECT))
        self.assertIsNone(references_problem(corpus, SUBJECT))

    def test_uncited_name_fails(self) -> None:
        """Behavior: a bare name with no row fails g.25, class defect, in
        the document's text and in the text of one of its provisions.

        Reference: STND.DRAFT.34 (binding, checked_by g.25), unit 0013
        design (ii), and the gaps of the closing round of 2026-10-25,
        such as "MEAS binds them" in CPS (``p5/gaps.md``).
        """
        cases = {
            "document": inserted(f"The {NAMED} profile is out of scope."),
            "provision": live_index(),
        }
        cases["provision"][f"{SUBJECT}.1"].body += f" {NAMED} differs."
        for name, index in cases.items():
            with self.subTest(name):
                corpus = corpus_of(index)
                self.assertIn(NAMED, named_documents(corpus, SUBJECT))
                problem = references_problem(corpus, SUBJECT) or ""
                self.assertIn(f"text names {NAMED} without", problem)
                self.assertEqual(g25(index), "FAIL")
                ctx = build_context(corpus)
                assert ctx is not None
                found = [
                    f
                    for f in drafting.citations.references_listed(ctx)
                    if f.subject == SUBJECT
                ]
                self.assertEqual([f.cls for f in found], ["defect"])

    def test_citation_derives_the_row(self) -> None:
        """Behavior: once the name is cited, by a provision or by the
        document in parentheses, the derived table holds the row, and
        g.25 passes after the table is derived again.

        Reference: the fix the closing round applied to each gap
        (``p5/gaps.md``), and the derivation of ``derive/references``.
        """
        for citation in (f"{NAMED}.1", f"({NAMED})"):
            with self.subTest(citation):
                index = inserted(f"The {NAMED} profile ({citation}) differs.")
                corpus = corpus_of(index)
                self.assertIn(NAMED, cited_documents(corpus, SUBJECT))
                problem = references_problem(corpus, SUBJECT) or ""
                self.assertIn(f"missing {NAMED}", problem)
                self.assertNotIn("text names", problem)
                index[SUBJECT].body = rederived(corpus, SUBJECT)
                self.assertIsNone(
                    references_problem(corpus_of(index), SUBJECT)
                )
                self.assertEqual(g25(index), "PASS")

    def test_longest_name(self) -> None:
        """Behavior: a dotted name is read whole, so HDES.FPGA names
        HDES.FPGA and not HDES.

        Reference: the identifier form of STND.IDENT, in which a
        sub-profile extends its parent's identifier.
        """
        corpus = corpus_of(inserted("HDES.FPGA differs."))
        named = named_documents(corpus, SUBJECT)
        self.assertIn("HDES.FPGA", named)
        self.assertNotIn(NAMED, named)

    def test_mentions_are_ignored(self) -> None:
        """Behavior: a name in the Revision History, in a table whose
        header names a column Example, in a quoted span, or in code is
        not read, and g.25 passes; a name in another table is read.

        Reference: decision 22 of the closing round of 2026-10-25 and
        the exclusions of ``p5/gaps.md``, rules 2 to 4.
        """
        example = f"| Item | Example |\n| --- | --- |\n| a profile | {NAMED} |"
        history = live_index()
        history[SUBJECT].body = (
            history[SUBJECT].body.rstrip("\n")
            + f"\n| 9.9 | 2026-10-25 | Editorial amendment: {NAMED}. |\n"
        )
        cases = {
            "revision history": history,
            "example table": inserted(example),
            "straight quotes": inserted(f'The word "{NAMED}" is a name.'),
            "curly quotes": inserted(f"The word “{NAMED}” is a name."),
            "code span": inserted(f"The word `{NAMED}` is a name."),
            "fenced code": inserted(f"```text\n{NAMED}\n```"),
        }
        for name, index in cases.items():
            with self.subTest(name):
                corpus = corpus_of(index)
                self.assertNotIn(NAMED, named_documents(corpus, SUBJECT))
                self.assertIsNone(references_problem(corpus, SUBJECT))
                self.assertEqual(g25(index), "PASS")
        read = {
            "other table": inserted(example.replace("Example", "Profile")),
            "Example in a row only": inserted(
                f"| Item | Profile |\n| --- | --- |\n| Example | {NAMED} |"
            ),
        }
        for name, index in read.items():
            with self.subTest(name):
                self.assertIn(
                    NAMED, named_documents(corpus_of(index), SUBJECT)
                )
                self.assertEqual(g25(index), "FAIL")

    def test_references_section_is_not_read(self) -> None:
        """Behavior: a name in the References section is not a bare name
        of the text.

        Reference: ``naming_text``, which leaves out the section that
        g.25 compares with the derived one.
        """
        index = live_index()
        index[SUBJECT].body = index[SUBJECT].body.replace(
            f"## {SECTION}\n", f"## {SECTION}\n\n{NAMED}\n", 1
        )
        corpus = corpus_of(index)
        self.assertNotIn(NAMED, named_documents(corpus, SUBJECT))

    def test_lvl0_is_not_read(self) -> None:
        """Behavior: a document of LVL0, or of no level, is not read for
        bare names, and the word LVL0 names no document.

        Reference: STND.DRAFT.34, which asks References only of the
        documents below LVL0, and the scope of decision 22.
        """
        index = live_index()
        for doc in ("LVL0", "PRIME", "MNEM"):
            index[doc].body += f"\n\n{NAMED} and STND.CLASS differ.\n"
        corpus = corpus_of(index)
        for doc in ("LVL0", "PRIME", "MNEM"):
            with self.subTest(doc):
                self.assertEqual(named_documents(corpus, doc), [])
        self.assertEqual(g25(index), "PASS")
        lvl0 = corpus_of(inserted("Below LVL0 it differs."))
        self.assertNotIn("LVL0", named_documents(lvl0, SUBJECT))


class LiveCorpus(unittest.TestCase):
    """The live corpus names no document it does not cite."""

    def test_live_corpus_passes(self) -> None:
        """Behavior: on the live corpus every document g.25 reads cites
        each document it names, g.25 passes, and the wrapper
        ``tools/check_refs.py`` reports 0 documents with missing rows.

        Reference: the definition of done of 2026-10-25, item 8, and the
        live corpus after ledger entry 175, which closed every gap.
        """
        corpus = corpus_of(live_index())
        ctx = build_context(corpus)
        assert ctx is not None
        subjects = [
            u.subject for u in ctx.units_for(BELOW, {"informative", "body"})
        ]
        self.assertGreater(len(subjects), 40)
        for doc in subjects:
            with self.subTest(doc):
                named = set(named_documents(corpus, doc))
                self.assertLessEqual(named, set(cited_documents(corpus, doc)))
                self.assertIsNone(references_problem(corpus, doc))
        self.assertEqual(g25(live_index()), "PASS")
        run = subprocess.run(
            [sys.executable, "-B", str(WRAPPER), str(ROOT)],
            cwd=REPO,
            env={"PYTHONPATH": str(REPO)},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn(
            f"checked {len(subjects)} documents; 0 with missing rows",
            run.stdout,
        )


if __name__ == "__main__":
    unittest.main()
