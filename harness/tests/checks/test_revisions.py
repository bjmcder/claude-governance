"""Mutation tests of the revision and identifier checks (family v).

Each case damages an in-memory copy of the corpus or the ledger in one
known way and asserts that the named check reports at least the stated
severity. Nothing is written to disk. The undamaged corpus must report
no failure and no warning in the v family. Ported from
``archive/tools-flat/test_revisions.py``.
"""

from __future__ import annotations

import unittest
from collections.abc import Callable
from typing import Any

from govharness.checks.base import CheckContext
from govharness.checks.registry import run_checks
from govharness.checks.revisions import family as revisions
from govharness.checks.revisions.adopters import role_labels, template_problems
from govharness.checks.revisions.identifiers import (
    form_problem,
    read_register,
    usage_problems,
)
from govharness.core.entry import Entry
from tests.support import Index, corpus_of, live_index, live_ledger

Ledger = list[dict[str, Any]]
Mutation = Callable[[Index, Ledger], None]
RANK = {"PASS": 0, "INFO": 1, "WARN": 2, "FAIL": 3}


def statuses(mutation: Mutation) -> dict[str, str]:
    """Apply a mutation to copies of the corpus and ledger.

    Parameters
    ----------
    mutation : Mutation
        Damages the index or the ledger in place.

    Returns
    -------
    dict[str, str]
        Status of each v check.
    """
    index = live_index()
    ledger = live_ledger()
    mutation(index, ledger)
    ctx = CheckContext(corpus_of(index), ledger)
    report = run_checks((revisions,), ctx)
    return {r.key: r.status for r in report.results}


def result(mutation: Mutation, key: str) -> tuple[str, list[str]]:
    """Apply a mutation and return one v check's status and details.

    Parameters
    ----------
    mutation : Mutation
        Damages the index or the ledger in place.
    key : str
        Key of the check, such as ``v.3``.

    Returns
    -------
    tuple[str, list[str]]
        Its status and detail lines.
    """
    index = live_index()
    ledger = live_ledger()
    mutation(index, ledger)
    ctx = CheckContext(corpus_of(index), ledger)
    report = run_checks((revisions,), ctx)
    (found,) = [r for r in report.results if r.key == key]
    return found.status, found.details


def _meta(rule: str, **fields: object) -> Mutation:
    """Return a mutation that sets front-matter fields.

    Parameters
    ----------
    rule : str
        Identifier of the entry.
    **fields : object
        Field values set.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(index: Index, ledger: Ledger) -> None:
        """Set the fields.

        Parameters
        ----------
        index : Index
            Copy of the corpus entries by identifier; changed in place.
        ledger : Ledger
            Copy of the ledger entries; changed in place.
        """
        index[rule].meta.update(fields)

    return apply


def _replace(rule: str, old: str, new: str) -> Mutation:
    """Return a mutation that rewrites every occurrence of a text.

    Parameters
    ----------
    rule : str
        Identifier of the entry.
    old, new : str
        Text replaced and its replacement.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(index: Index, ledger: Ledger) -> None:
        """Replace the text.

        Parameters
        ----------
        index : Index
            Copy of the corpus entries by identifier; changed in place.
        ledger : Ledger
            Copy of the ledger entries; changed in place.
        """
        assert old in index[rule].body, old
        index[rule].body = index[rule].body.replace(old, new)

    return apply


def _history_row(row: str) -> Mutation:
    """Return a mutation that appends a row to the LVL0 history.

    Parameters
    ----------
    row : str
        Markdown row.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(index: Index, ledger: Ledger) -> None:
        """Append the row.

        Parameters
        ----------
        index : Index
            Copy of the corpus entries by identifier; changed in place.
        ledger : Ledger
            Copy of the ledger entries; changed in place.
        """
        index["LVL0"].body = index["LVL0"].body.rstrip("\n") + "\n" + row

    return apply


def _latest(ledger: Ledger) -> dict[str, Any]:
    """Return the latest transaction that records a revision.

    Parameters
    ----------
    ledger : Ledger
        Ledger entries.

    Returns
    -------
    dict[str, Any]
        The last ``adopt`` or ``amend`` entry.
    """
    return [e for e in ledger if e["type"] in {"adopt", "amend"}][-1]


def _drop_transaction(index: Index, ledger: Ledger) -> None:
    """Remove the transaction of the latest revision.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    ledger.remove(_latest(ledger))


def _review_instead(index: Index, ledger: Ledger) -> None:
    """Record the latest revision as a review.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _latest(ledger)["type"] = "review"


def _wrong_type(index: Index, ledger: Ledger) -> None:
    """Record the latest revision under the other revision type.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    entry = _latest(ledger)
    entry["type"] = "amend" if entry["type"] == "adopt" else "adopt"


def _no_revision_named(index: Index, ledger: Ledger) -> None:
    """Strip the revision from a rationale.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _latest(ledger)["rationale"] = "Editorial amendment of the Lexicon."


def _late_date(index: Index, ledger: Ledger) -> None:
    """Move a transaction to another day.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _latest(ledger)["at"] = "2026-11-01T00:00:00+00:00"


def _untargeted(index: Index, ledger: Ledger) -> None:
    """Remove the document from the targets of the latest transaction.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _latest(ledger)["targets"] = ["LEX.author"]


def _drop_class_row(index: Index, ledger: Ledger) -> None:
    """Remove the minor row from the table of revision classes.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    body = index["STND.IDENT.3"].body
    index["STND.IDENT.3"].body = "\n".join(
        line for line in body.splitlines() if not line.startswith("| Minor |")
    )


def _drop_table(index: Index, ledger: Ledger) -> None:
    """Stop the provision from naming the table.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    index["STND.IDENT.3"].meta["defines"] = []


def _clash(index: Index, ledger: Ledger) -> None:
    """Let two classes open with the same words.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    body = index["STND.IDENT.3"].body
    index["STND.IDENT.3"].body = body.replace(
        "Minor amendment", "Editorial amendment"
    )


def _drop_label(index: Index, ledger: Ledger) -> None:
    """Remove the adopter field from a standard.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    del index["STND.DRAFT"].meta["adopted_by"]


def _draft_standard(index: Index) -> Entry:
    """Return a standard that is still a draft, whichever one it is.

    Parameters
    ----------
    index : Index
        Entries by identifier.

    Returns
    -------
    Entry
        The first draft standard.
    """
    drafts = [
        e
        for e in index.values()
        if e.meta.get("kind") == "standard" and e.meta.get("status") == "draft"
    ]
    if drafts:
        return drafts[0]
    # Every standard is adopted (STND.ANNEX, the last draft, since entry
    # 106): turn the first adopted standard into a draft without history.
    adopted = sorted(
        (e for e in index.values() if e.meta.get("kind") == "standard"),
        key=lambda e: str(e.meta.get("id")),
    )
    assert adopted, "the corpus holds no standard"
    doc = adopted[0]
    doc.meta.update(status="draft", revision="0.1")
    doc.meta.pop("adopted", None)
    doc.body = doc.body.split("## Revision History")[0]
    return doc


def _major_draft(index: Index, ledger: Ledger) -> None:
    """Give a draft standard a major segment of one.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _draft_standard(index).meta.update(revision="1.0")


def _add_standard(index: Index, ledger: Ledger) -> None:
    """Make an adopted standard that keeps no history.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _draft_standard(index).meta.update(status="adopted", revision="1.0")


def _unrecorded_minor(index: Index, ledger: Ledger) -> None:
    """Add a minor revision to LVL0 that no transaction records.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _history_row("| 1.1 | 2026-10-10 | Minor amendment (GOV.40): x. |")(
        index, ledger
    )
    index["LVL0"].meta.update(revision="1.1")


RETIRED_DRAFT = (
    "| none | active |\n| DRAFT |",
    "| none | retired |\n| DRAFT |",
)


def _retired_item(index: Index, ledger: Ledger) -> None:
    """Retire a mnemonic together with every item that uses it.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    _replace("MNEM", *RETIRED_DRAFT)(index, ledger)
    for key, entry in index.items():
        if key == "STND.CLASS" or key.startswith("STND.CLASS."):
            entry.meta.update(status="retired")


# Each case: mutation, then {check key: least severe status expected}.
CASES: dict[str, tuple[Mutation, dict[str, str]]] = {
    "leading zero": (_meta("STND.DRAFT", revision="0.02"), {"v.1": "FAIL"}),
    "zero editorial": (_meta("STND.DRAFT", revision="1.0.0"), {"v.1": "FAIL"}),
    "missing revision": (_meta("STND.DRAFT", revision=None), {"v.1": "FAIL"}),
    "draft with major one": (_major_draft, {"v.2": "FAIL"}),
    "adopted below one": (
        _meta("LVL0", revision="0.9"),
        {"v.2": "FAIL", "v.3": "FAIL"},
    ),
    "field behind history": (_meta("LVL0", revision="1.0.1"), {"v.3": "FAIL"}),
    "field ahead of history": (
        _meta("LVL0", revision="1.0.9"),
        {"v.3": "FAIL"},
    ),
    "skipped step": (
        _history_row(
            "| 1.0.5 | 2026-10-10 | Editorial amendment (GOV.40): x. |"
        ),
        {"v.3": "FAIL"},
    ),
    "reused revision": (
        _history_row(
            "| 1.0.2 | 2026-10-10 | Editorial amendment (GOV.40): x. |"
        ),
        {"v.3": "FAIL"},
    ),
    "reset forgotten": (
        _history_row("| 1.1.3 | 2026-10-10 | Minor amendment (GOV.40): x. |"),
        {"v.3": "FAIL"},
    ),
    "wrong opening words": (
        _history_row(
            "| 1.1 | 2026-10-10 | Editorial amendment (GOV.40): x. |"
        ),
        {"v.3": "FAIL"},
    ),
    "major without reset": (
        _history_row("| 2.1 | 2026-10-10 | Major amendment (GOV.40): x. |"),
        {"v.3": "FAIL"},
    ),
    "missing transaction": (_drop_transaction, {"v.4": "FAIL"}),
    "wrong ledger type": (_wrong_type, {"v.4": "FAIL"}),
    "review is not a revision": (_review_instead, {"v.4": "FAIL"}),
    "rationale names no revision": (_no_revision_named, {"v.4": "FAIL"}),
    "revision date differs": (_late_date, {"v.4": "WARN"}),
    "document not targeted": (_untargeted, {"v.4": "FAIL"}),
    "unrecorded minor revision": (_unrecorded_minor, {"v.4": "FAIL"}),
    "adopted without history": (_add_standard, {"v.3": "FAIL"}),
    "blank adopter": (_meta("LVL0", ratified_by=""), {"v.5": "FAIL"}),
    "person as adopter": (
        _meta("STND.DRAFT", adopted_by="A. Person"),
        {"v.5": "FAIL"},
    ),
    "undefined role as adopter": (
        _meta("STND.DRAFT", adopted_by="The Maintainer"),
        {"v.5": "FAIL"},
    ),
    "no adopter field": (_drop_label, {"v.5": "FAIL"}),
    "missing class row": (_drop_class_row, {"v.6": "FAIL"}),
    "table not named": (_drop_table, {"v.6": "FAIL"}),
    "opening words clash": (_clash, {"v.6": "FAIL"}),
    "bad ledger type in table": (
        _replace(
            "STND.IDENT.3",
            "| Major | major | amend |",
            "| Major | major | bless |",
        ),
        {"v.6": "FAIL"},
    ),
    "withdrawn list dropped": (
        _meta("STND.CLASS", withdrawn=[]),
        {"v.8": "FAIL"},
    ),
    "withdrawn identifier in use": (
        _meta("STND.CLASS", withdrawn=["STND.CLASS.8", "STND.CLASS.10"]),
        {"v.8": "FAIL"},
    ),
    "withdrawn identifier of another document": (
        _meta("STND.CLASS", withdrawn=["STND.IDENT.99"]),
        {"v.8": "FAIL"},
    ),
    "malformed identifier": (
        _meta("STND.CLASS.1", refers_to=["Stnd.class.3"]),
        {"v.9": "FAIL"},
    ),
    "term slug differs": (_meta("LEX.author", term="Writer"), {"v.9": "FAIL"}),
    "unregistered mnemonic": (
        _replace(
            "MNEM", "| CLASS | STND | Consequence-class criteria |", "| X |"
        ),
        {"v.10": "FAIL"},
    ),
    "grade outside its scale": (
        _replace("MNEM", "| 0 to 3 |", "| 1 to 3 |"),
        {"v.10": "FAIL"},
    ),
    "register changed by another role": (
        lambda index, ledger: ledger.append(
            {"seq": 98, "type": "register", "role": "x", "scope": ["MNEM"]}
        ),
        {"v.11": "FAIL"},
    ),
    "retired mnemonic in use": (
        _replace("MNEM", *RETIRED_DRAFT),
        {"v.10": "FAIL"},
    ),
    "retired item keeps its mnemonic": (_retired_item, {}),
    "register changed by an amendment": (
        lambda index, ledger: ledger.append(
            {"seq": 99, "type": "amend", "scope": ["MNEM"]}
        ),
        {"v.11": "FAIL"},
    ),
    "check never named": (
        _meta("STND.IDENT.1", checked_by=[]),
        {"v.7": "FAIL"},
    ),
    "unknown check": (
        _meta("STND.IDENT.1", checked_by=["v.99"]),
        {"v.7": "FAIL"},
    ),
    "check enforces nothing": (
        _meta("STND.IDENT.12", checked_by=["review"]),
        {"v.7": "FAIL"},
    ),
}


class RevisionChecks(unittest.TestCase):
    """Each injected defect is caught; the clean corpus is not flagged."""

    def test_clean_corpus_conforms(self) -> None:
        """Behavior: the undamaged corpus passes v.1 to v.11, in order.

        Reference: the live corpus and ledger, whose revisions the
        custodian recorded under STND.IDENT.
        """
        found = statuses(lambda index, ledger: None)
        bad = {k: s for k, s in found.items() if s in {"FAIL", "WARN"}}
        self.assertEqual(bad, {})
        self.assertEqual(
            sorted(found, key=lambda k: int(k[2:])),
            [f"v.{n}" for n in range(1, 12)],
        )

    def test_mutations_are_caught(self) -> None:
        """Behavior: each injected defect reaches its stated severity.

        Reference: the defect each case injects (CASES); the case
        "retired item keeps its mnemonic" asserts no new failure.
        """
        for name, (mutation, expected) in CASES.items():
            with self.subTest(name):
                got = statuses(mutation)
                for key, status in expected.items():
                    self.assertGreaterEqual(
                        RANK[got.get(key, "PASS")],
                        RANK[status],
                        f"{name}: {key} is {got.get(key)}, want {status}",
                    )

    def test_template_owner_fields(self) -> None:
        """Behavior: a blank or non-role owner field in a template is found.

        Reference: STND.IDENT.12; the values blank, a person's name, an
        undefined role, and a lower-case label are each injected.
        """
        roles = role_labels(corpus_of(live_index()))
        good = {"_PROJECT/NAME/WAIV/1.md": {"decided_by": "The Human Owner"}}
        self.assertEqual(template_problems(good, roles), [])
        for value in ("", "A. Person", "The Maintainer", "custodians"):
            bad = {"_PROJECT/NAME/WAIV/1.md": {"decided_by": value}}
            self.assertEqual(len(template_problems(bad, roles)), 1, value)

    def test_identifier_forms(self) -> None:
        """Behavior: each form of STND.IDENT.15 and a project parent.

        Reference: the identifier forms of STND.IDENT.15 and
        STND.IDENT.16; each bad form breaks exactly one rule.
        """
        projects = frozenset({"NAME"})
        good = [
            ("LVL0", "constitution"),
            ("LVL0#normative-language", None),
            ("HW.FPGA", "sub-profile"),
            ("GOV.12", "provision"),
            ("LEX.relying-party", "term"),
            ("TAG.METH.monte-carlo", None),
            ("KNOW.NUMER.4", None),
            ("NAME.WAIV.3", None),
        ]
        for ident, kind in good:
            self.assertIsNone(form_problem(ident, kind, projects), ident)
        bad = [
            ("TAG.METH.Neural", None),
            ("KNOW.NUMER.monte-carlo", None),
            ("GOV.foo", None),
            ("GOV.12", "term"),
            ("LEX.Author", "term"),
            ("LVL0.1", None),
            ("CSQ1", None),
        ]
        for ident, kind in bad:
            self.assertIsNotNone(form_problem(ident, kind, projects), ident)
        register = {
            ("none", "NAME"): {"Status": "active", "Grades": "none"},
            ("project", "WAIV"): {"Status": "active", "Grades": "none"},
        }
        self.assertEqual(usage_problems("NAME.WAIV.3", register, projects), [])


def _draft_without_adopter(index: Index, ledger: Ledger) -> None:
    """Make STND.PERF a draft at 0.1 with no adopter, as in QA.8 M4.

    Parameters
    ----------
    index : Index
        Copy of the corpus entries by identifier; changed in place.
    ledger : Ledger
        Copy of the ledger entries; changed in place.
    """
    meta = index["STND.PERF"].meta
    meta.update(status="draft", revision="0.1")
    del meta["adopted_by"]
    meta.pop("adopted", None)


def _cite(document: str, text: str) -> Mutation:
    """Return a mutation that adds a sentence to a document's Purpose.

    Parameters
    ----------
    document : str
        Identifier of the document.
    text : str
        Sentence added at the end of its first section.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(index: Index, ledger: Ledger) -> None:
        """Insert the sentence before the second heading.

        Parameters
        ----------
        index : Index
            Copy of the corpus entries by identifier; changed in place.
        ledger : Ledger
            Copy of the ledger entries; changed in place.
        """
        body = index[document].body
        cut = body.index("\n## ", body.index("## ") + 3)
        index[document].body = f"{body[:cut]} {text}{body[cut:]}"

    return apply


class HeldBehavior(unittest.TestCase):
    """Behavior that no case above held (QA.8 part C, M4, M5, and H1)."""

    def test_duplicate_history_row(self) -> None:
        """Behavior: a history row that repeats the revision above it
        fails v.3 as out of order.

        Reference: STND.IDENT.9 (no reuse); QA.8 part C, M5, the
        mutation of ``history.py`` from ``<=`` to ``<``. LVL0's last
        row, 1.6, is repeated, so the field still equals the last row.
        """
        status, details = result(
            _history_row(
                "| 1.6 | 2026-10-11 | Minor amendment (GOV.40): x. |"
            ),
            "v.3",
        )
        self.assertEqual(status, "FAIL")
        self.assertIn("- LVL0: 1.6 does not follow the row above", details)

    def test_major_step(self) -> None:
        """Behavior: a major step to 2.0 passes v.3.

        Reference: the table of STND.IDENT.3 (Major raises the major
        segment and resets the others); QA.8 part C, M5, the mutation
        of ``classes.py`` that took 1.6 to 3.0 as the major step.
        """

        def major(index: Index, ledger: Ledger) -> None:
            """Raise LVL0 to 2.0 by a major amendment.

            Parameters
            ----------
            index : Index
                Copy of the corpus entries by identifier; changed in
                place.
            ledger : Ledger
                Copy of the ledger entries; changed in place.
            """
            _history_row(
                "| 2.0 | 2026-10-12 | Major amendment (GOV.40): x. |"
            )(index, ledger)
            index["LVL0"].meta["revision"] = "2.0"

        self.assertEqual(result(major, "v.3"), ("PASS", []))

    def test_grade_bounds(self) -> None:
        """Behavior: both ends of a grade span are registered grades.

        Reference: STND.IDENT.22 and the register row of LVL, grades 0
        to 3; QA.8 part C, M5, the mutation of the upper bound.
        """
        register, _ = read_register(corpus_of(live_index()))
        self.assertEqual(usage_problems("LVL0", register), [])
        self.assertEqual(usage_problems("LVL3", register), [])
        self.assertEqual(len(usage_problems("LVL4", register)), 1)

    def test_near_siblings(self) -> None:
        """Behavior: v.10 lists siblings at a letter distance of 1 that
        are not established acronyms, and nothing else.

        Reference: STND.IDENT.18; QA.8 part C, M5, the mutations of the
        sibling filter. The live register has no such pair (CPU, GPU,
        and QPU are established acronyms; CPS and CPU, or JL and ML,
        have different parents). A row GOVX beside GOV adds one.
        """
        self.assertEqual(result(lambda i, x: None, "v.10"), ("PASS", []))
        status, details = result(
            _replace(
                "MNEM",
                "| GOV | none |",
                "| GOVX | none | Probe | none | none | active |\n"
                "| GOV | none |",
            ),
            "v.10",
        )
        self.assertEqual(status, "INFO")
        self.assertEqual(
            details,
            ["- `GOV` and `GOVX` under `none` are at a letter distance of 1"],
        )

    def test_adopter_field_of_each_kind(self) -> None:
        """Behavior: an adopted or ratified document names its adopter,
        the constitution in ``ratified_by`` and every other document in
        ``adopted_by``; a draft or a planned document need not.

        Reference: STND.IDENT.12 as amended in the round of 2026-10-26
        ("that is adopted or ratified"); QA.8 part C, M4, whose draft
        without an adopter now passes.
        """
        cases = {
            "constitution with adopted_by": lambda index, ledger: index[
                "LVL0"
            ].meta.update(adopted_by=index["LVL0"].meta.pop("ratified_by")),
            "standard with ratified_by": lambda index, ledger: index[
                "STND.PERF"
            ].meta.update(
                ratified_by=index["STND.PERF"].meta.pop("adopted_by")
            ),
        }
        for name, mutation in cases.items():
            with self.subTest(name):
                status, details = result(mutation, "v.5")
                self.assertEqual(status, "FAIL")
                self.assertEqual(len(details), 1, details)
                self.assertIn("names no adopter in", details[0])

        def planned(index: Index, ledger: Ledger) -> None:
            """Make STND.PERF planned, with no adopter.

            Parameters
            ----------
            index : Index
                Copy of the corpus entries by identifier; changed in
                place.
            ledger : Ledger
                Copy of the ledger entries; changed in place.
            """
            _draft_without_adopter(index, ledger)
            index["STND.PERF"].meta.update(status="planned")

        for name, mutation in {
            "draft without adopter": _draft_without_adopter,
            "planned without adopter": planned,
        }.items():
            with self.subTest(name):
                self.assertEqual(result(mutation, "v.5")[0], "PASS")

    def test_withdrawn_constitution_provisions(self) -> None:
        """Behavior: the constitution lists in its field ``withdrawn``
        a withdrawn provision of a part; unlisted, the gap fails.

        Reference: STND.IDENT.24; GOV.12 deleted from a copy, with and
        without ``withdrawn: ["GOV.12"]`` on LVL0, and GOV.12's citations
        listed as withdrawn by the same field.
        """

        def deleted(index: Index, ledger: Ledger) -> None:
            """Delete GOV.12 without listing it.

            Parameters
            ----------
            index : Index
                Copy of the corpus entries by identifier; changed in
                place.
            ledger : Ledger
                Copy of the ledger entries; changed in place.
            """
            del index["GOV.12"]

        def listed(index: Index, ledger: Ledger) -> None:
            """Delete GOV.12 and list it on LVL0.

            Parameters
            ----------
            index : Index
                Copy of the corpus entries by identifier; changed in
                place.
            ledger : Ledger
                Copy of the ledger entries; changed in place.
            """
            deleted(index, ledger)
            index["LVL0"].meta["withdrawn"] = ["GOV.12"]

        status, details = result(deleted, "v.8")
        self.assertEqual(status, "FAIL")
        self.assertIn(
            "- LVL0: GOV.12 is missing and not listed as withdrawn", details
        )
        self.assertEqual(result(listed, "v.8"), ("PASS", []))

    def test_cited_provisions_resolve(self) -> None:
        """Behavior: v.8 fails on a provision deleted without being
        listed as withdrawn when the corpus still cites it, even where
        no gap shows it, and on any cited identifier of the corpus's
        mnemonics that names nothing.

        Reference: STND.IDENT.14 and STND.DRAFT.22; QA.8 part C, H1 (the
        highest-numbered provision STND.PERF.26 deleted, which
        STND.PERF cites) and L1 (GOV.999 in a body, AGENT.99 in a
        binding reason). A cited withdrawn identifier, an identifier of
        another scheme (the C++ Core Guidelines' ES.11), and a quoted
        one pass.
        """
        status, details = result(
            lambda index, ledger: index.pop("STND.PERF.26"), "v.8"
        )
        self.assertEqual(status, "FAIL")
        self.assertEqual(
            details,
            [
                (
                    "- STND.PERF.26 is cited (STND.PERF) but is neither a "
                    "provision nor listed as withdrawn"
                )
            ],
        )

        def listed(index: Index, ledger: Ledger) -> None:
            """Delete STND.PERF.26 and list it as withdrawn.

            Parameters
            ----------
            index : Index
                Copy of the corpus entries by identifier; changed in
                place.
            ledger : Ledger
                Copy of the ledger entries; changed in place.
            """
            del index["STND.PERF.26"]
            index["STND.PERF"].meta["withdrawn"] = ["STND.PERF.26"]

        self.assertEqual(result(listed, "v.8"), ("PASS", []))
        status, details = result(
            _cite("STND.PERF", 'See GOV.999, ES.11, and "GOV.998".'),
            "v.8",
        )
        self.assertEqual(status, "FAIL")
        self.assertEqual(len(details), 1, details)
        self.assertIn("GOV.999 is cited (STND.PERF)", details[0])
        status, details = result(
            _meta("STND.PERF.3", binding_reason="As AGENT.99 requires."),
            "v.8",
        )
        self.assertEqual(status, "FAIL")
        self.assertIn("AGENT.99 is cited (STND.PERF.3)", details[0])
        self.assertEqual(
            result(_cite("STND.PERF", "See STND.CXX.16."), "v.8"),
            ("PASS", []),
        )


if __name__ == "__main__":
    unittest.main()
