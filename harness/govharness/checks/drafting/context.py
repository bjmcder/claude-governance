"""The units the drafting checks scan, and what every check shares.

The corpus is scanned in four groups of subjects:

* ``self``: the drafting standard itself; a defect fails;
* ``lower``: other numbered provisions below LVL0; a defect fails when
  the standard is adopted and the provision enforced is binding, and
  warns otherwise;
* ``draft``: documents not yet divided into numbered provisions,
  scanned as if their whole body were provisions; findings form a punch
  list;
* ``lvl0``: LVL0 provisions, to which the standard does not apply; the
  expression, qualifier, quantifier, role-word, and style findings form
  an advisory list for the next amendment.

A finding of class ``defect`` is certain by the standard's own words;
one of class ``review`` is a candidate that a reader decides.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from govharness.checks.base import CheckContext
from govharness.checks.drafting.tables import (
    StandardTables,
    expression_pattern,
    read_standard_tables,
)
from govharness.checks.lineage.derivation import lower_provisions
from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.tables import parse_tables, section_text
from govharness.core.text import sentences_of, unquoted

STANDARD_ID = "STND.DRAFT"
ALL_GROUPS = {"self", "lower", "draft", "lvl0"}
BELOW = {"self", "lower", "draft"}
FIRM_TABLE_ROWS = (
    "Mandatory",
    "Strongly recommended",
    "Permitted",
    "Permission or exemption",
)
IMPERATIVE_VERBS = frozenset(
    """add apply ask check choose close commit complete confirm copy create
    define delete describe document ensure exclude fill follow give halt
    identify include keep label list make mark move name note open place
    provide put read record refer remove replace report review run save
    see select send set specify start state stop store take tell test
    update use verify write""".split()
)
NOT_IMPERATIVE_SECOND = frozenset(
    "of is are and or for in on to as with by at".split()
)
TableRow = tuple[list[str], str]


@dataclass
class Finding:
    """One result of a drafting check.

    Parameters
    ----------
    subject : str
        Identifier of the entry concerned.
    group : str
        ``self``, ``lower``, ``draft``, or ``lvl0``.
    cls : str
        ``defect`` (certain) or ``review`` (a reader decides).
    text : str
        What was found.
    """

    subject: str
    group: str
    cls: str
    text: str


@dataclass
class Unit:
    """A body cut into sentences, with where it comes from.

    Parameters
    ----------
    subject : str
        Identifier of the entry.
    group : str
        ``self``, ``lower``, ``draft``, or ``lvl0``.
    kind : str
        ``provision``, ``informative`` (a document's own text), or
        ``body`` (an undivided draft).
    level : str
        Level of the entry.
    sentences : list[str]
        Sentences of its prose.
    mode : str | None
        ``binding`` or ``default`` for a provision below LVL0.
    body : str
        The Markdown body.
    """

    subject: str
    group: str
    kind: str
    level: str
    sentences: list[str]
    mode: str | None = None
    body: str = ""


@dataclass
class DraftingContext:
    """Everything the drafting checks share.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    tables : StandardTables
        Tables read from the standard.
    adopted : bool
        Whether the standard is adopted or ratified.
    units : list[Unit]
        The corpus cut into units.
    rules : list[Entry]
        Numbered provisions of the standard.
    modals : list[str]
        The modal set.
    lowercase : dict[str, str]
        Class of each modal written in lowercase.
    firm_rows : list[TableRow]
        Rows of the LVL0 Normative Language table that state a force.
    status_patterns : list[re.Pattern[str]]
        Patterns of the table's status words (``is``, ``has`` forms).
    """

    corpus: Corpus
    tables: StandardTables
    adopted: bool = False
    units: list[Unit] = field(default_factory=list)
    rules: list[Entry] = field(default_factory=list)
    modals: list[str] = field(default_factory=list)
    lowercase: dict[str, str] = field(default_factory=dict)
    firm_rows: list[TableRow] = field(default_factory=list)
    status_patterns: list[re.Pattern[str]] = field(default_factory=list)

    def units_for(
        self, groups: set[str], kinds: set[str] | None = None
    ) -> list[Unit]:
        """Return the units of some groups, and optionally some kinds.

        Parameters
        ----------
        groups : set[str]
            Groups wanted.
        kinds : set[str] | None
            Kinds wanted, or ``None`` for every kind.

        Returns
        -------
        list[Unit]
            Matching units, in corpus order.
        """
        return [
            u
            for u in self.units
            if u.group in groups and (kinds is None or u.kind in kinds)
        ]

    def modal_re(self) -> re.Pattern[str]:
        """Return the regular expression for the capitalized modals.

        Returns
        -------
        re.Pattern[str]
            Matches any modal of the set, longest first.
        """
        ordered = sorted(self.modals, key=len, reverse=True)
        return re.compile(
            r"\b(?:"
            + "|".join(m.replace(" ", r"\s+") for m in ordered)
            + r")\b"
        )


def lvl0_table(corpus: Corpus) -> list[TableRow]:
    """Return the (words, meaning) rows of the Normative Language table.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    list[TableRow]
        Words of each row, parenthesized notes dropped, and the meaning.
    """
    section = section_text(corpus.body("LVL0"), "Normative Language")
    rows = []
    for header, data in parse_tables(section or ""):
        if header[:2] != ["Word or phrase", "Meaning"]:
            continue
        for row in data:
            words = [
                w.strip()
                for w in row[0].split(",")
                if w.strip() and "(" not in w
            ]
            rows.append((words, row[1]))
    return rows


def build_context(corpus: Corpus) -> DraftingContext | None:
    """Build the shared context of the drafting checks.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    DraftingContext | None
        The context, or ``None`` when the corpus holds no drafting
        standard.
    """
    standard = corpus.by_id.get(STANDARD_ID)
    if standard is None:
        return None
    tables = read_standard_tables(corpus, STANDARD_ID)
    ctx = DraftingContext(corpus, tables)
    ctx.modals = [r["Modal"] for r in tables.tables.get("modal-set", [])]
    ctx.lowercase = {
        r["Modal"].lower(): r["Lowercase"]
        for r in tables.tables.get("modal-set", [])
    }
    ctx.adopted = standard.meta.get("status") in {"adopted", "ratified"}
    ctx.rules = [
        e
        for e in lower_provisions(corpus)
        if str(e.meta["id"]).startswith(f"{STANDARD_ID}.")
    ]
    table = lvl0_table(corpus)
    ctx.firm_rows = [(w, m) for w, m in table if m.startswith(FIRM_TABLE_ROWS)]
    ctx.status_patterns = [
        expression_pattern(w)
        for words, meaning in table
        if not meaning.startswith(FIRM_TABLE_ROWS)
        for w in words
        if w.startswith(("is ", "has "))
    ]
    ctx.units = cut_units(corpus)
    return ctx


def drafting_context(ctx: CheckContext) -> DraftingContext | None:
    """Return the drafting context of a run, built once.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    DraftingContext | None
        As ``build_context``.
    """
    return ctx.shared(_build_for_run)


def _build_for_run(ctx: CheckContext) -> DraftingContext | None:
    """Build the drafting context of a run's corpus.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    DraftingContext | None
        As ``build_context``.
    """
    return build_context(ctx.corpus)


def _unit(entry: Entry, group: str, kind: str, mode: str | None) -> Unit:
    """Cut one entry into a unit.

    Parameters
    ----------
    entry : Entry
        The entry.
    group : str
        Its group.
    kind : str
        Its kind of unit.
    mode : str | None
        Its binding mode, for a provision below LVL0.

    Returns
    -------
    Unit
        The unit with the entry's sentences.
    """
    return Unit(
        str(entry.meta["id"]),
        group,
        kind,
        str(entry.meta.get("level")),
        sentences_of(entry.body),
        mode,
        entry.body,
    )


def cut_units(corpus: Corpus) -> list[Unit]:
    """Cut the corpus into units for scanning.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    list[Unit]
        LVL0 provisions, provisions below LVL0, the informative text of
        documents that hold provisions, and the bodies of undivided
        drafts; Lexicon terms and planned stubs are left out.
    """
    units: list[Unit] = []
    documents_with_rules = {
        str(e.meta["id"]).rsplit(".", 1)[0] for e in lower_provisions(corpus)
    }
    for entry in corpus.entries:
        pid = str(entry.meta["id"])
        level = str(entry.meta.get("level"))
        kind = entry.meta.get("kind")
        in_standard = pid == STANDARD_ID or pid.startswith(f"{STANDARD_ID}.")
        group = "self" if in_standard else "lower"
        if kind == "provision" and level == "LVL0":
            units.append(_unit(entry, "lvl0", "provision", None))
        elif kind == "provision":
            units.append(
                _unit(entry, group, "provision", entry.meta.get("mode"))
            )
        elif level in {"LVL1", "LVL2", "LVL3"} and kind not in {"term"}:
            if pid in documents_with_rules or in_standard:
                units.append(_unit(entry, group, "informative", None))
            elif entry.meta.get("status") != "planned" and entry.body.strip():
                units.append(_unit(entry, "draft", "body", None))
    return units


def modals_in(ctx: DraftingContext, sentence: str) -> list[str]:
    """Return the capitalized modals used, not mentioned, in a sentence.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.
    sentence : str
        One sentence.

    Returns
    -------
    list[str]
        Each modal found, whitespace collapsed.
    """
    if not ctx.modals:
        return []
    return [
        re.sub(r"\s+", " ", m)
        for m in ctx.modal_re().findall(unquoted(sentence))
    ]


def is_status(ctx: DraftingContext, sentence: str) -> bool:
    """Return True when a sentence states a Normative Language status.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.
    sentence : str
        One sentence.

    Returns
    -------
    bool
        Whether a status word of the LVL0 table occurs outside quotes.
    """
    return any(p.search(unquoted(sentence)) for p in ctx.status_patterns)


def is_imperative(sentence: str) -> bool:
    """Return True when a sentence looks imperative (a heuristic).

    Parameters
    ----------
    sentence : str
        One sentence.

    Returns
    -------
    bool
        Whether it opens with ``do``, ``never``, ``please``, or a listed
        verb not followed by a word that marks a noun phrase.
    """
    words = re.findall(r"[A-Za-z'-]+", unquoted(sentence))
    if not words:
        return False
    first = words[0].lower()
    if first in {"do", "never", "please"}:
        return True
    if first not in IMPERATIVE_VERBS:
        return False
    return len(words) < 2 or words[1].lower() not in NOT_IMPERATIVE_SECOND
