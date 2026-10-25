"""Mutation tests of the lineage (l) and drafting (g) checks.

Each case damages an in-memory copy of the corpus in one known way and
asserts that the named check reports at least the stated severity.
Nothing is written to disk. The clean corpus must report no failure and
no warning in the l and g families, other than the g.18 review findings
of confirmed bundles, which is the standard's self-conformance. Ported
from ``archive/tools-flat/test_drafting.py``.
"""

from __future__ import annotations

import unittest
from collections.abc import Callable
from pathlib import PurePosixPath

from govharness.checks.base import CheckContext
from govharness.checks.drafting import expressions, modals, roles
from govharness.checks.drafting import family as drafting
from govharness.checks.drafting.context import (
    Finding,
    build_context,
    is_imperative,
)
from govharness.checks.drafting.family import Finder
from govharness.checks.lineage import family as lineage
from govharness.checks.registry import run_checks
from govharness.core.entry import Entry
from tests.support import Index, corpus_of, live_index

Mutation = Callable[[Index], None]
RANK = {"PASS": 0, "INFO": 1, "WARN": 2, "FAIL": 3}
# Provisions of STND.DRAFT with exactly three modals, whose bundles were
# reviewed and ratified as never applied apart (ledger entry 52). g.18
# reports each as a review finding, which in the standard's own group is
# a warning; no record in the corpus clears it.
CONFIRMED_BUNDLES = {"STND.DRAFT.35", "STND.DRAFT.39", "STND.DRAFT.42"}


def statuses(mutation: Mutation) -> dict[str, str]:
    """Apply a mutation to a copy of the corpus; return status by key.

    Parameters
    ----------
    mutation : Mutation
        Damages the index in place.

    Returns
    -------
    dict[str, str]
        Status of each l and g check.
    """
    index = live_index()
    mutation(index)
    ctx = CheckContext(corpus_of(index))
    report = run_checks((lineage, drafting), ctx)
    return {r.key: r.status for r in report.results}


def _append(rule: str, text: str) -> Mutation:
    """Return a mutation that appends a sentence to a standard entry.

    Parameters
    ----------
    rule : str
        Identifier of the entry.
    text : str
        Sentence appended; a document gets it as a new paragraph.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(e: Index) -> None:
        """Append the sentence.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        e[rule].body += "\n\n" + text if rule.endswith("DRAFT") else " " + text

    return apply


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

    def apply(e: Index) -> None:
        """Set the fields.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        e[rule].meta.update(fields)

    return apply


def _body_replace(rule: str, old: str, new: str) -> Mutation:
    """Return a mutation that rewrites part of a body.

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

    def apply(e: Index) -> None:
        """Replace the text.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        assert old in e[rule].body, old
        e[rule].body = e[rule].body.replace(old, new)

    return apply


def _new_lvl1(text: str, status: str = "draft") -> Mutation:
    """Return a mutation that adds a LVL1 provision and sets a status.

    Parameters
    ----------
    text : str
        Body of the new provision AGENT.1.
    status : str
        Status given to the drafting standard.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(e: Index) -> None:
        """Add AGENT.1 and set the standard's status.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        meta = {
            "id": "AGENT.1",
            "level": "LVL1",
            "kind": "provision",
            "title": "Probe rule",
            "status": "draft",
            "instantiates": ["PRIME.1"],
            "refers_to": [],
            "rank": 0,
            "waivable": False,
        }
        e["AGENT.1"] = Entry(PurePosixPath("AGENT/1.md"), meta, text)
        e["STND.DRAFT"].meta["status"] = status

    return apply


def _drop_modal_row(e: Index) -> None:
    """Remove the row for ``must`` from the excluded-expression table.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    body = e["STND.DRAFT.7"].body
    e["STND.DRAFT.7"].body = "\n".join(
        line for line in body.splitlines() if not line.startswith("| must |")
    )


def _drop_table(e: Index) -> None:
    """Remove the table of the quantifier provision.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    body = e["STND.DRAFT.17"].body
    e["STND.DRAFT.17"].body = body.split("\n\n|")[0]


def _retitle_twice(e: Index) -> None:
    """Give two provisions the same title.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["STND.DRAFT.2"].meta["title"] = e["STND.DRAFT.1"].meta["title"]


def _redefine(e: Index) -> None:
    """Define the Lexicon term Agent in the standard's Terms section.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["STND.DRAFT"].body = e["STND.DRAFT"].body.replace(
        "| Modal |", "| Agent | A thing that acts. |\n| Modal |"
    )


def _same_level(e: Index) -> None:
    """Make a provision instantiate a provision of its own level.

    Parameters
    ----------
    e : Index
        Copy of the corpus entries by identifier; changed in place.
    """
    e["STND.DRAFT.2"].meta["instantiates"] = ["STND.DRAFT.1"]


# Each case: mutation, then {check key: least severe status expected}.
CASES: dict[str, tuple[Mutation, dict[str, str]]] = {
    "lowercase modal": (
        _append("STND.DRAFT.2", "An actor shall record it."),
        {"g.3": "FAIL"},
    ),
    "two modals": (
        _append("STND.DRAFT.2", "An actor SHALL record and SHALL report it."),
        {"g.4": "FAIL"},
    ),
    "excluded exact": (
        _append("STND.DRAFT.2", "An actor must record it."),
        {"g.5": "FAIL"},
    ),
    "excluded inflection": (
        _append("STND.DRAFT.2", "Edits are not allowed after release."),
        {"g.5": "FAIL"},
    ),
    "excluded review": (
        _append("STND.DRAFT.2", "The tool will halt."),
        {"g.6": "WARN"},
    ),
    "modal outside provision": (
        _append("STND.DRAFT", "An actor SHALL read this."),
        {"g.7": "FAIL"},
    ),
    "imperative": (
        _append("STND.DRAFT.2", "Record the decision."),
        {"g.8": "WARN"},
    ),
    "example in body": (
        _append("STND.DRAFT.2", "For instance, a snapshot is a record."),
        {"g.9": "FAIL"},
    ),
    "vague exact": (
        _append("STND.DRAFT.2", "An actor SHALL log events and so on."),
        {"g.10": "FAIL"},
    ),
    "vague review": (
        _append("STND.DRAFT.2", "An actor SHALL act as needed."),
        {"g.10": "WARN"},
    ),
    "negated list": (
        _append("STND.DRAFT.2", "An actor SHALL NOT delete or overwrite."),
        {"g.11": "WARN"},
    ),
    "late condition": (
        _append("STND.DRAFT.2", "An actor SHALL halt if the check fails."),
        {"g.12": "WARN"},
    ),
    "quantifier": (
        _append("STND.DRAFT.2", "Any actor SHALL halt."),
        {"g.13": "FAIL"},
    ),
    "number": (
        _append("STND.DRAFT.2", "An actor SHALL retry 5 times."),
        {"g.14": "WARN"},
    ),
    "citation range": (
        _append("STND.DRAFT.2", "See PRIME.1 to PRIME.4."),
        {"g.15": "FAIL", "g.16": "FAIL"},
    ),
    "citation position": (
        _append("STND.DRAFT.2", "See the provision above."),
        {"g.15": "FAIL"},
    ),
    "unlisted identifier": (
        _append("STND.DRAFT.2", "See GOV.1."),
        {"g.16": "FAIL"},
    ),
    "reference missing": (
        _body_replace("STND.CLASS", "| VV | Correctness |\n", ""),
        {"g.25": "FAIL"},
    ),
    "reference not cited": (
        _body_replace(
            "STND.DFLT",
            "| GOV | Governance |",
            "| GOV | Governance |\n| SIMPL | Simplicity |",
        ),
        {"g.25": "FAIL"},
    ),
    "long title": (
        _meta("STND.DRAFT.2", title="A title with far more than six words"),
        {"g.17": "FAIL"},
    ),
    "duplicate title": (_retitle_twice, {"g.17": "FAIL"}),
    "four modals": (
        _append(
            "STND.DRAFT.2",
            "An actor SHALL a. An actor SHALL b. An actor SHALL c.",
        ),
        {"g.18": "FAIL"},
    ),
    "retired word": (
        _append("STND.DRAFT.2", "The user SHALL record it."),
        {"g.19": "FAIL"},
    ),
    "undefined role": (
        _append("STND.DRAFT.2", "The maintainer SHALL record it."),
        {"g.19": "WARN"},
    ),
    "lexicon redefinition": (_redefine, {"g.20": "FAIL"}),
    "contraction": (
        _append("STND.DRAFT.2", "The tool doesn't halt."),
        {"g.21": "FAIL"},
    ),
    "typographic contraction": (
        _append("STND.DRAFT.2", "The tool doesn\u2019t halt."),
        {"g.21": "FAIL"},
    ),
    # ``core.text`` ends a sentence at a semicolon only before a capital,
    # so the second clause opens with one (QA.8 part C, L3).
    "two modals joined by a semicolon": (
        _append(
            "STND.DRAFT.2",
            "An actor SHALL record it; X SHALL read it.",
        ),
        {"g.4": "FAIL"},
    ),
    "excluded expression in a table row": (
        lambda e: setattr(
            e["STND.PERF.1"],
            "body",
            e["STND.PERF.1"].body + "\n\n| x | The code may not run |\n",
        ),
        {"g.5": "FAIL"},
    ),
    "lowercase modal in a table cell": (
        lambda e: setattr(
            e["STND.PERF.1"],
            "body",
            e["STND.PERF.1"].body
            + "\n\n| Item | Rule |\n| --- | --- |\n| x | It shall run. |\n",
        ),
        {"g.3": "FAIL"},
    ),
    "first person": (
        _append("STND.DRAFT.2", "We SHALL record it."),
        {"g.21": "FAIL"},
    ),
    "spelling": (
        _append("STND.DRAFT.2", "The behaviour SHALL be recorded."),
        {"g.22": "FAIL"},
    ),
    "missing table": (_drop_table, {"g.1": "FAIL", "g.23": "FAIL"}),
    "uncovered table form": (_drop_modal_row, {"g.2": "FAIL"}),
    "check never named": (
        _meta("STND.DRAFT.5", checked_by=[]),
        {"g.23": "FAIL"},
    ),
    "unknown check": (
        _meta("STND.DRAFT.5", checked_by=["g.99"]),
        {"g.23": "FAIL"},
    ),
    "no instantiates": (
        _meta("STND.DRAFT.2", instantiates=[]),
        {"l.1": "FAIL"},
    ),
    "dangling locator": (
        _meta("STND.DRAFT.2", instantiates=["LVL0#no-such-section"]),
        {"l.1": "FAIL"},
    ),
    "same level": (_same_level, {"l.2": "FAIL"}),
    "waivable prime child": (
        _meta("STND.DRAFT.19", waivable=True),
        {"l.3": "FAIL", "l.5": "FAIL"},
    ),
    "wrong rank": (_meta("STND.DRAFT.19", rank=3), {"l.3": "FAIL"}),
    "default but non-waivable": (
        _meta("STND.DRAFT.1", mode="default"),
        {"l.4": "FAIL"},
    ),
    "binding without reason": (
        _meta("STND.DRAFT.1", binding_reason=None),
        {"l.4": "FAIL"},
    ),
    "draft standard warns only": (
        _new_lvl1("An actor must record it.", "draft"),
        {"g.5": "WARN"},
    ),
    "adopted standard fails": (
        _new_lvl1("An actor must record it.", "adopted"),
        {"g.5": "FAIL"},
    ),
}


class DraftingChecks(unittest.TestCase):
    """Each injected defect is caught; the clean corpus is not flagged."""

    def test_floor_forcing(self) -> None:
        """Behavior: GOV forces the binding mark and PRIN does not.

        Reference: GOV.10 places GOV in the floor; a binding provision
        that reaches only PRIN needs a recorded reason (GOV.19).
        """
        forced = statuses(_meta("STND.DRAFT.25", binding_reason=None))
        self.assertEqual(forced["l.4"], "PASS")
        unforced = statuses(_meta("STND.CLASS.19", instantiates=["PRIN.1"]))
        self.assertEqual(unforced["l.4"], "FAIL")

    def test_clean_corpus_conforms(self) -> None:
        """Behavior: the standard passes its own checks with no warning
        other than the g.18 review findings of its confirmed bundles.

        Reference: the live corpus, whose adoption of STND.DRAFT
        recorded self-conformance (ledger entry 9 and later), and the
        three-modal provisions that entry 52 added.
        """
        ctx = CheckContext(corpus_of(live_index()))
        report = run_checks((lineage, drafting), ctx)
        bad = {
            r.key: r.status
            for r in report.results
            if r.status in {"FAIL", "WARN"} and r.key != "g.18"
        }
        self.assertEqual(bad, {})
        (atomicity,) = [r for r in report.results if r.key == "g.18"]
        warned = {
            line.split()[3]
            for line in atomicity.details
            if line.startswith("- WARN ")
        }
        self.assertEqual(warned, CONFIRMED_BUNDLES)
        self.assertFalse(
            [line for line in atomicity.details if "at most three" in line]
        )

    def test_mutations_are_caught(self) -> None:
        """Behavior: each injected defect reaches its stated severity.

        Reference: the defect each case injects (CASES), and the
        severity model of the drafting family.
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

    def test_traceability_knows_every_registered_key(self) -> None:
        """Behavior: g.23 accepts a key of any registered check, whatever
        families the run includes, and still fails on an unknown key.

        Reference: the registry. The flat code counted as known only the
        keys reported earlier in the same run, so a drafting provision
        citing a v or f key failed g.23 (defect 2 of unit 0001, fixed by
        review 0001). Here STND.DRAFT.1 cites v.1 and f.1, whose families
        this run of l and g does not include, and then an unregistered
        key.
        """
        cited = list(live_index()["STND.DRAFT.1"].meta["checked_by"])
        known = statuses(_meta("STND.DRAFT.1", checked_by=[*cited, "v.1"]))
        self.assertEqual(known["g.23"], "PASS")
        known = statuses(_meta("STND.DRAFT.1", checked_by=[*cited, "f.1"]))
        self.assertEqual(known["g.23"], "PASS")
        unknown = statuses(_meta("STND.DRAFT.1", checked_by=[*cited, "z.9"]))
        self.assertEqual(unknown["g.23"], "FAIL")

    def test_draft_and_lvl0_never_fail(self) -> None:
        """Behavior: drafts and LVL0 only ever produce INFO findings.

        Reference: the severity model, under which the standard does
        not apply to LVL0 and undivided drafts form a punch list.
        """
        self.assertEqual(statuses(lambda e: None)["g.24"], "INFO")


def findings(mutation: Mutation, finder: Finder) -> list[Finding]:
    """Apply a mutation and return one finder's findings.

    Parameters
    ----------
    mutation : Mutation
        Damages the index in place.
    finder : Finder
        A drafting finder, such as ``modals.one_modal``.

    Returns
    -------
    list[Finding]
        Its findings on the damaged copy.
    """
    index = live_index()
    mutation(index)
    ctx = build_context(corpus_of(index))
    assert ctx is not None
    return finder(ctx)


def _instrument(text: str) -> Mutation:
    """Return a mutation that adds an instantiated LVL3 instrument.

    Parameters
    ----------
    text : str
        Body of the waiver DEMO.WAIV.1.

    Returns
    -------
    Mutation
        The mutation.
    """

    def apply(e: Index) -> None:
        """Add DEMO.WAIV.1.

        Parameters
        ----------
        e : Index
            Copy of the corpus entries by identifier; changed in place.
        """
        meta = {
            "id": "DEMO.WAIV.1",
            "level": "LVL3",
            "kind": "waiver",
            "title": "Probe waiver",
            "status": "adopted",
        }
        e["DEMO.WAIV.1"] = Entry(PurePosixPath("DEMO/WAIV/1.md"), meta, text)

    return apply


class HeldBehavior(unittest.TestCase):
    """Behavior that no case above held (QA.8 part C, M2 and M5)."""

    def test_provision_that_imposes_nothing(self) -> None:
        """Behavior: g.4 finds a provision with no modal, status word,
        or imperative, and a status word alone imposes something.

        Reference: STND.DRAFT.4 and STND.DRAFT.5; the status words of
        the Normative Language table (``is a defect``). QA.8 part C,
        M5: the mutations of ``modals.py`` line 190 and of the status
        filter of ``context.py``.
        """
        nothing = "the provision imposes nothing"

        def subjects(body: str) -> list[str]:
            """Return the subjects g.4 finds imposing nothing.

            Parameters
            ----------
            body : str
                Body given to STND.DRAFT.2.

            Returns
            -------
            list[str]
                Subjects of the findings.
            """
            found = findings(
                lambda e: setattr(e["STND.DRAFT.2"], "body", body),
                modals.one_modal,
            )
            return [f.subject for f in found if nothing in f.text]

        self.assertEqual(subjects("This is a note."), ["STND.DRAFT.2"])
        self.assertEqual(subjects("A record without a date is a defect."), [])

    def test_imperative_heuristic(self) -> None:
        """Behavior: an imperative opens with do, never, please, or a
        listed verb not followed by a word that marks a noun phrase.

        Reference: the heuristic of g.8 (README, "Not yet built"); QA.8
        part C, M5, the mutations of ``is_imperative``.
        """
        for sentence in ("Never act.", "Please act.", "Record.", "Record it."):
            with self.subTest(sentence):
                self.assertTrue(is_imperative(sentence))
        for sentence in ("", "Record of it.", "Record of.", "A record."):
            with self.subTest(sentence):
                self.assertFalse(is_imperative(sentence))

    def test_fill_in_guidance_in_instrument(self) -> None:
        """Behavior: fill-in guidance left in an instantiated LVL3
        instrument is a defect, and the label elsewhere is not.

        Reference: STND.DRAFT.11; QA.8 part C, M5, the mutations of
        ``expressions.py`` lines 140 to 142. STND.DRAFT.11 itself
        names the label in quotation marks.
        """
        found = findings(
            _instrument("Fill-in guidance: state the scope."),
            expressions.informative_markers,
        )
        left = [f.subject for f in found if "fill-in guidance" in f.text]
        self.assertEqual(left, ["DEMO.WAIV.1"])
        found = findings(
            _instrument("The scope is stated."),
            expressions.informative_markers,
        )
        self.assertFalse([f for f in found if "fill-in guidance" in f.text])

    def test_conditions(self) -> None:
        """Behavior: g.12 lists a sentence with two conditions, and one
        whose condition follows the modal, and neither a sentence with
        one condition nor one whose conditions come first.

        Reference: STND.DRAFT.16; QA.8 part C, M5, the mutations of the
        bound ``len(starts) > 1`` and of the test of a late condition.
        STND.DRAFT.2 has no g.12 finding of its own.
        """

        def texts(sentence: str) -> list[str]:
            """Return g.12's findings on STND.DRAFT.2 with one sentence.

            Parameters
            ----------
            sentence : str
                Sentence appended to STND.DRAFT.2.

            Returns
            -------
            list[str]
                Text of each finding on STND.DRAFT.2.
            """
            found = findings(
                _append("STND.DRAFT.2", sentence), expressions.conditions
            )
            return [f.text for f in found if f.subject == "STND.DRAFT.2"]

        two = texts(
            "Where a check fails and where a log is full, X SHALL halt."
        )
        self.assertEqual([t[:12] for t in two], ["2 conditions"])
        self.assertEqual(texts("Where a check fails, X SHALL halt."), [])
        late = texts("X SHALL halt where a check fails.")
        self.assertEqual(
            [t[:28] for t in late], ["condition follows the clause"]
        )

    def test_title_bound(self) -> None:
        """Behavior: a title of one to six words passes g.17 and one of
        seven fails.

        Reference: STND.DRAFT.26 (a short noun phrase, the six-word
        bound of the README); QA.8 part C, M5, the mutations of the
        bounds in ``roles.py``.
        """

        def flagged(title: str) -> bool:
            """Return whether g.17 finds STND.DRAFT.2 with a title.

            Parameters
            ----------
            title : str
                Title given to STND.DRAFT.2.

            Returns
            -------
            bool
                Whether a finding names STND.DRAFT.2.
            """
            found = findings(_meta("STND.DRAFT.2", title=title), roles.titles)
            return any(f.subject == "STND.DRAFT.2" for f in found)

        self.assertFalse(flagged("Probe"))
        self.assertFalse(flagged("One two three four five six"))
        self.assertTrue(flagged("One two three four five six more"))

    def test_table_cells(self) -> None:
        """Behavior: the cells of a table in a provision are read as
        prose, a quoted expression in them is a mention, and a table
        that the provision names in ``defines`` is left out.

        Reference: STND.DRAFT, Normative and informative parts ("the
        body of a numbered provision, including a table it contains, is
        normative") and STND.DRAFT.3; QA.8 part C, M2.
        """

        def row(rule: str, text: str) -> Mutation:
            """Return a mutation that adds a table to a provision.

            Parameters
            ----------
            rule : str
                Identifier of the provision.
            text : str
                Text of the second cell of its one row.

            Returns
            -------
            Mutation
                The mutation.
            """

            def apply(e: Index) -> None:
                """Add the table.

                Parameters
                ----------
                e : Index
                    Copy of the corpus entries by identifier; changed in
                    place.
                """
                table = "| Item | Rule |\n| --- | --- |\n"
                e[rule].body += f"\n\n{table}| x | {text} |\n"

            return apply

        used = statuses(row("STND.PERF.1", "The code may not run."))
        self.assertEqual(used["g.5"], "FAIL")
        quoted = statuses(
            row("STND.PERF.1", 'The words "may not" are barred.')
        )
        self.assertEqual(quoted["g.5"], "PASS")
        defined = statuses(row("STND.DRAFT.17", "The code may not run."))
        self.assertEqual(defined["g.5"], "PASS")


if __name__ == "__main__":
    unittest.main()
