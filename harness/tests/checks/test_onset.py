"""Tests of the field ``onset`` (unit 0023): its reading, its check, its
rendering beside the mode, and the command ``onset``.

The live corpus carries no field yet, so each test adds one to a copy:
STND.CODE.22, a default of two sentences; STND.STDC.1, a default with a
table; STND.CODE.6, a binding provision; and VV.1, a provision of LVL0.
"""

from __future__ import annotations

import unittest

from govharness.checks.base import CheckContext
from govharness.checks.fields import onsets_valid
from govharness.core.onset import (
    Onset,
    applying_from,
    describe,
    onset_problems,
    parse_onset,
    part_exists,
    sentences,
)
from govharness.derive.reading_copy import ReadingCopy, compose
from govharness.query.graph import build_graph
from govharness.query.retrieval import show
from tests.cli.test_main import run
from tests.support import corpus_copy, corpus_of, live_index, live_ledger

PARTED = ["CSQ3", ["sentence 2", "CSQ2"]]


def fielded() -> dict:
    """Return the live index with ``"CSQ3"`` on each waivable provision
    below LVL0, as a corpus that uses the field gives each one.

    Returns
    -------
    dict
        Entries by identifier.
    """
    index = live_index()
    for entry in index.values():
        meta = entry.meta
        if (
            meta.get("kind") == "provision"
            and meta.get("level") != "LVL0"
            and meta.get("waivable") is True
        ):
            meta["onset"] = "CSQ3"
    return index


class Reading(unittest.TestCase):
    """The value of the field is read, or refused with its reason."""

    def test_forms_read(self) -> None:
        """Behavior: a class reads as the whole provision; a list as the
        class of the provision and each named part; ``null`` as every
        class.

        Reference: the field `onset` of
        STND.DRAFT#representation-in-the-harness.
        """
        self.assertEqual(parse_onset("CSQ2"), Onset("CSQ2"))
        self.assertEqual(
            parse_onset(PARTED), Onset("CSQ3", (("sentence 2", "CSQ2"),))
        )
        self.assertEqual(
            parse_onset(["CSQ3", ["row STND.CXX.24", "CSQ1"]]).classes(),
            {"CSQ3", "CSQ1"},
        )
        self.assertEqual(parse_onset(None), Onset("CSQ4"))

    def test_malformed_values_refused(self) -> None:
        """Behavior: each malformed value is refused: CSQ4 or no class
        alone, a list without parts, a part of no form, a part at the
        class of the provision or a less severe one, a part named twice.

        Reference: the field `onset`: one class for the whole provision,
        a later class for a named part, nothing at every class.
        """
        bad = [
            "CSQ4",
            "CSQ5",
            3,
            ["CSQ3"],
            ["CSQ3", "sentence 2"],
            ["CSQ3", ["clause 2", "CSQ2"]],
            ["CSQ3", ["sentence 0", "CSQ2"]],
            ["CSQ2", ["sentence 2", "CSQ2"]],
            ["CSQ2", ["sentence 2", "CSQ3"]],
            ["CSQ3", ["sentence 2", "CSQ2"], ["sentence 2", "CSQ1"]],
            ["CSQX", ["sentence 2", "CSQ2"]],
            ["CSQ4", ["sentence 1", "CSQ1"]],
            {"CSQ3": "sentence 2"},
        ]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_onset(value)

    def test_parts_name_sentences_and_rows(self) -> None:
        """Behavior: a sentence ends at terminal punctuation, outside the
        tables; a row is named by its first cell.

        Reference: STND.CODE.22 has two sentences; STND.STDC.1 has two
        sentences and a row for STND.CXX.24.
        """
        index = live_index()
        code = index["STND.CODE.22"].body
        stdc = index["STND.STDC.1"].body
        self.assertEqual(len(sentences(code)), 2)
        self.assertTrue(part_exists(code, "sentence 2"))
        self.assertFalse(part_exists(code, "sentence 3"))
        self.assertEqual(len(sentences(stdc)), 2)
        self.assertTrue(sentences(stdc)[1].endswith("(REPRO.7)."))
        self.assertTrue(part_exists(stdc, "row STND.CXX.24"))
        self.assertFalse(part_exists(stdc, "row STND.CXX.99"))
        self.assertFalse(part_exists(stdc, "row CSQ2"))
        self.assertFalse(
            part_exists(
                stdc,
                "row The type volatile std::sig_atomic_t is read as "
                "volatile sig_atomic_t",
            )
        )
        class10 = index["STND.CLASS.10"].body
        self.assertFalse(part_exists(class10, "row CSQ2"))

    def test_sentences_as_a_reader_counts(self) -> None:
        """Behavior: a period inside a sentence before a lower-case word,
        a semicolon, and the markers of a numbered list end no sentence.

        Reference: the field `onset`, "counted at terminal punctuation".
        """
        body = (
            "The work SHALL do one thing, e.g. the first; and more:\n"
            "1. Item one;\n2. Item two.\nThe work SHOULD do another."
        )
        found = sentences(body)
        self.assertEqual(len(found), 2)
        self.assertTrue(found[0].endswith("Item two."))

    def test_described_beside_the_mode(self) -> None:
        """Behavior: an onset reads "from CSQ3; sentence 2 from CSQ2",
        and ``null`` "at every class".

        Reference: the onset rendered beside the mode (ruling C7).
        """
        self.assertEqual(
            describe(parse_onset(PARTED)), "from CSQ3; sentence 2 from CSQ2"
        )
        self.assertEqual(describe(parse_onset(None)), "at every class")


class Check(unittest.TestCase):
    """``verify`` fails a malformed onset and an onset where none fits."""

    def verdict(self, ident: str, value: object) -> tuple[str, list[str]]:
        """Return the verdict of the check with one field set.

        Parameters
        ----------
        ident : str
            The item that carries the field.
        value : object
            Its value.

        Returns
        -------
        tuple[str, list[str]]
            Status and details of the check.
        """
        index = fielded()
        index[ident].meta["onset"] = value
        found = onsets_valid(CheckContext(corpus_of(index), live_ledger()))
        return found.status, found.details

    def test_missing_field_fails_once_the_field_is_used(self) -> None:
        """Behavior: once one entry carries the field, a waivable
        provision below LVL0 without it fails; ``null`` passes on a
        waivable provision and fails on a binding one.

        Reference: the field `onset`; an omitted field is not read as
        an onset (review of round o, item 6).
        """
        index = fielded()
        del index["STND.CODE.22"].meta["onset"]
        found = onsets_valid(CheckContext(corpus_of(index), live_ledger()))
        self.assertEqual(
            (found.status, found.details),
            (
                "FAIL",
                ["- STND.CODE.22: a waivable provision without an onset"],
            ),
        )
        self.assertEqual(self.verdict("STND.CODE.22", None)[0], "PASS")
        status, details = self.verdict("STND.CODE.6", None)
        self.assertEqual(status, "FAIL")
        self.assertIn("binds at every class", details[0])

    def test_live_corpus_passes(self) -> None:
        """Behavior: the live corpus, which carries no field, passes.

        Reference: no verdict on the live corpus changes (unit 0023).
        """
        found = onsets_valid(CheckContext(corpus_of(live_index()), []))
        self.assertEqual(found.status, "PASS")

    def test_well_formed_fields_pass(self) -> None:
        """Behavior: a whole class, a sentence, and a row pass.

        Reference: STND.CODE.22 and STND.STDC.1, both waivable.
        """
        self.assertEqual(self.verdict("STND.CODE.22", PARTED)[0], "PASS")
        self.assertEqual(self.verdict("STND.CODE.22", "CSQ2")[0], "PASS")
        row = ["CSQ3", ["row STND.CXX.24", "CSQ1"]]
        self.assertEqual(self.verdict("STND.STDC.1", row)[0], "PASS")

    def test_each_problem_fails(self) -> None:
        """Behavior: a malformed value, a part the body lacks, a binding
        provision, a provision of LVL0, and a document each fail, naming
        the item.

        Reference: the field `onset`, which a waivable provision below
        LVL0 alone carries.
        """
        cases = [
            ("STND.CODE.22", "CSQ9", "STND.CODE.22: malformed onset"),
            (
                "STND.CODE.22",
                ["CSQ3", ["sentence 3", "CSQ2"]],
                "names sentence 3, which no one sentence or row",
            ),
            (
                "STND.CLASS.10",
                ["CSQ3", ["row CSQ2", "CSQ2"]],
                "names row CSQ2, which no one sentence or row",
            ),
            ("STND.CODE.6", "CSQ3", "a provision that binds at every class"),
            ("VV.1", "CSQ3", "an item other than a provision below LVL0"),
            ("STND.CODE", "CSQ3", "an item other than a provision below"),
        ]
        for ident, value, message in cases:
            with self.subTest(ident=ident, value=value):
                status, details = self.verdict(ident, value)
                self.assertEqual(status, "FAIL")
                self.assertEqual(len(details), 1)
                self.assertIn(message, details[0])

    def test_problems_name_nothing_without_a_field(self) -> None:
        """Behavior: an item without the field has no problem.

        Reference: nothing where the provision binds or applies at every
        class.
        """
        self.assertEqual(onset_problems(live_index()["STND.CODE.6"]), [])


class Rendering(unittest.TestCase):
    """``show`` and the reading copies print the onset beside the mode."""

    def test_show_prints_the_onset(self) -> None:
        """Behavior: ``show`` prints the onset after the mode, and
        nothing for a provision without one.

        Reference: the facts line of ``show`` (STND.HARN.1).
        """
        index = live_index()
        before = show(
            corpus_of(index), build_graph(corpus_of(index)), "STND.CODE.22"
        )
        self.assertNotIn("from CSQ", before)
        index["STND.CODE.22"].meta["onset"] = PARTED
        corpus = corpus_of(index)
        text = show(corpus, build_graph(corpus), "STND.CODE.22")
        self.assertIn("default · from CSQ3; sentence 2 from CSQ2", text)

    def test_reading_copy_prints_the_onset(self) -> None:
        """Behavior: the reading copy writes the onset after the mode.

        Reference: the reading copies of `compose`.
        """
        index = live_index()
        index["STND.CODE.22"].meta["onset"] = PARTED
        text = compose(
            corpus_of(index),
            live_ledger(),
            ReadingCopy("STND.CODE", "STND.CODE.md"),
        )
        self.assertIn(
            "Default, from CSQ3; sentence 2 from CSQ2. Instantiates DSGN.4.",
            text,
        )

    def test_profile_without_mode_prints_the_onset(self) -> None:
        """Behavior: a provision of a profile, which has no mode, reads
        "From CSQ3." before what it instantiates, and one without the
        field keeps its line as before.

        Reference: HW.3 and HW.9, waivable provisions of HW.
        """
        index = live_index()
        index["HW.3"].meta["onset"] = "CSQ3"
        text = compose(
            corpus_of(index), live_ledger(), ReadingCopy("HW", "HW.md")
        )
        self.assertIn("From CSQ3. Instantiates REPRO.1, REPRO.2.", text)
        self.assertIn("\n. Instantiates INTPR.9.\n", text)


class Command(unittest.TestCase):
    """``onset [ROOT] CSQn`` lists what a reclassification adds."""

    def test_lists_provisions_and_parts(self) -> None:
        """Behavior: CSQ2 lists the part given CSQ2 and the provision of
        CSQ2; CSQ3 lists the provision whose other part waits, naming
        that part; CSQ1 finds nothing and exits 1; CSQ4 is refused.

        Reference: HR-3, "what does reclassification to CSQ2 add" in one
        command.
        """
        with corpus_copy() as root:
            for rel, value in (
                ("STND/CODE/22.md", '["CSQ3", ["sentence 2", "CSQ2"]]'),
                ("STND/CODE/23.md", '"CSQ2"'),
            ):
                path = root / rel
                text = path.read_text(encoding="utf-8")
                text = text.replace("\nrank:", f"\nonset: {value}\nrank:", 1)
                path.write_text(text, encoding="utf-8")
            code, out, _ = run(["onset", str(root), "CSQ2"])
            self.assertEqual(code, 0)
            self.assertIn("2 item(s).", out)
            self.assertIn("- STND.CODE.22, sentence 2 — ", out)
            self.assertIn("- STND.CODE.23 — ", out)
            code, out, _ = run(["onset", str(root), "CSQ3"])
            self.assertEqual(code, 0)
            self.assertIn("(from CSQ3; sentence 2 from CSQ2)", out)
            code, _, err = run(["onset", str(root), "CSQ1"])
            self.assertEqual(
                (code, err.strip()),
                (1, "onset: no provision applies from CSQ1"),
            )
            self.assertEqual(run(["onset", str(root), "CSQ4"])[0], 2)

    def test_verify_fails_a_bad_onset(self) -> None:
        """Behavior: ``verify`` fails, under the check onset, a field on
        a binding provision, and passes the copy before the change.

        Reference: the check onset of ``verify`` (unit 0023).
        """
        with corpus_copy() as root:
            code, out, _ = run(["verify", "--no-logic", str(root)])
            self.assertEqual(code, 0)
            self.assertIn("onset: PASS", out)
            path = root / "STND/CODE/6.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace("\nrank:", '\nonset: "CSQ3"\nrank:', 1),
                encoding="utf-8",
            )
            code, out, _ = run(["verify", "--no-logic", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("onset: FAIL", out)
            self.assertIn("STND.CODE.6: an onset on a provision", out)

    def test_applying_from_keeps_number_order(self) -> None:
        """Behavior: the listing follows the number of each provision
        within its document, STND.CODE.3 before STND.CODE.22, the whole
        provision before its parts.

        Reference: `applying_from`.
        """
        index = live_index()
        index["STND.CODE.22"].meta["onset"] = ["CSQ2", ["sentence 2", "CSQ1"]]
        index["STND.CODE.23"].meta["onset"] = "CSQ1"
        index["STND.CODE.3"].meta["onset"] = "CSQ1"
        entries = corpus_of(index).provisions()
        found = [(e.meta["id"], p) for e, p in applying_from(entries, "CSQ1")]
        self.assertEqual(
            found,
            [
                ("STND.CODE.3", None),
                ("STND.CODE.22", "sentence 2"),
                ("STND.CODE.23", None),
            ],
        )


if __name__ == "__main__":
    unittest.main()
