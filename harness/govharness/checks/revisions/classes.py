"""Revision numbers, the table of revision classes, and histories.

The identifier standard (STND.IDENT) fixes what the segments of a
revision number mean and how a revision is recorded in a document and in
the ledger. The classes of change come from the table that a provision
of the standard names ``revision-classes``, so rewording a sentence
cannot change what the checks enforce.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from govharness.checks.base import CheckContext
from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.tables import read_table, section_text

STANDARD_ID = "STND.IDENT"
CLASS_TABLE = "revision-classes"
CLASS_HEADER = (
    "Class",
    "Segment raised",
    "Ledger type",
    "Opening words",
    "Test",
)
HISTORY_HEADER = ("Revision", "Date", "Change")
REVISION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.([1-9]\d*))?$")
DOC_KINDS = {"constitution", "profile", "sub-profile", "standard"}
ADOPTED = {"ratified", "adopted"}
PRE_ADOPTION = {"planned", "draft"}
SEGMENTS = ("major", "minor", "editorial")
REQUIRED = ("adoption", "major", "minor", "editorial")
Revision = tuple[int, int, int]
History = list[dict[str, str]]


@dataclass
class RevisionClass:
    """One row of the table of revision classes.

    Parameters
    ----------
    name : str
        Class name in lowercase, such as ``minor``.
    segment : str
        Segment the class raises: ``major``, ``minor``, or
        ``editorial``.
    ledger_type : str
        Ledger transaction type that records the class.
    openers : tuple[str, ...]
        Words a change entry opens with.
    """

    name: str
    segment: str
    ledger_type: str
    openers: tuple[str, ...]


@dataclass
class ClassTable:
    """The classes read from the standard, and the problems found.

    Parameters
    ----------
    rows : dict[str, RevisionClass]
        Classes by lowercase name.
    owner : str
        Identifier of the provision that holds the table.
    problems : list[str]
        Reasons the table could not be read.
    """

    rows: dict[str, RevisionClass] = field(default_factory=dict)
    owner: str = ""
    problems: list[str] = field(default_factory=list)


def parse_revision(text: object) -> Revision | None:
    """Return (major, minor, editorial) for a revision number.

    Parameters
    ----------
    text : object
        Candidate revision number, such as ``1.0.2``.

    Returns
    -------
    Revision | None
        The three segments, or ``None`` when ``text`` is not well
        formed.
    """
    match = REVISION_RE.match(str(text))
    if match is None:
        return None
    return int(match[1]), int(match[2]), int(match[3] or 0)


def read_classes(corpus: Corpus) -> ClassTable:
    """Read the table of revision classes from the standard.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    ClassTable
        Classes by lowercase name, the holding provision, and problems.
    """
    out = ClassTable()
    prefix = f"{STANDARD_ID}."
    holders = [
        pid
        for pid, entry in sorted(corpus.by_id.items())
        if pid.startswith(prefix)
        and CLASS_TABLE in (entry.meta.get("defines") or [])
    ]
    if len(holders) != 1:
        out.problems.append(
            f"table `{CLASS_TABLE}` is defined by {len(holders)} provisions"
        )
        return out
    out.owner = holders[0]
    rows = read_table(corpus.by_id[out.owner].body, CLASS_HEADER)
    if not rows:
        out.problems.append(
            f"{out.owner}: no table with columns {', '.join(CLASS_HEADER)}"
        )
    for row in rows:
        name = row["Class"].lower()
        openers = tuple(w.strip() for w in row["Opening words"].split(","))
        if name in out.rows:
            out.problems.append(f"{out.owner}: class `{name}` listed twice")
        out.rows[name] = RevisionClass(
            name,
            row["Segment raised"].lower(),
            row["Ledger type"].lower(),
            tuple(w for w in openers if w),
        )
    return out


def classes_of(ctx: CheckContext) -> ClassTable:
    """Return the table of revision classes of a run, read once.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    ClassTable
        As ``read_classes``.
    """
    return ctx.shared(_read_classes_of)


def _read_classes_of(ctx: CheckContext) -> ClassTable:
    """Read the class table of a context's corpus.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    ClassTable
        As ``read_classes``.
    """
    return read_classes(ctx.corpus)


def class_problems(table: ClassTable) -> list[str]:
    """Return structural problems in the table of revision classes.

    Parameters
    ----------
    table : ClassTable
        The table read.

    Returns
    -------
    list[str]
        Reading problems, missing classes, unknown segments or ledger
        types, and opening words that are missing or shared.
    """
    problems = list(table.problems)
    where = table.owner or STANDARD_ID
    for name in REQUIRED:
        if table.rows and name not in table.rows:
            problems.append(f"{where}: no class `{name}`")
    seen: dict[str, str] = {}
    for row in table.rows.values():
        if row.segment not in SEGMENTS:
            problems.append(
                f"{where}: `{row.segment}` is not a segment of a revision"
            )
        if row.ledger_type not in {"adopt", "amend"}:
            problems.append(
                f"{where}: `{row.ledger_type}` is not a revision "
                "transaction type"
            )
        if not row.openers:
            problems.append(
                f"{where}: class `{row.name}` has no opening words"
            )
        for word in row.openers:
            if word.lower() in seen:
                problems.append(
                    f"{where}: `{word}` opens both `{seen[word.lower()]}` "
                    f"and `{row.name}`"
                )
            seen[word.lower()] = row.name
    return problems


def documents(corpus: Corpus) -> list[Entry]:
    """Return the entries that are documents carrying a revision.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    list[Entry]
        Constitutions, profiles, sub-profiles, and standards not at
        LVL3.
    """
    return [
        e
        for e in corpus.entries
        if e.meta.get("kind") in DOC_KINDS and e.meta.get("level") != "LVL3"
    ]


def history_of(body: str) -> History:
    """Return the rows of the Revision History section of a body.

    Parameters
    ----------
    body : str
        Markdown body of a document.

    Returns
    -------
    History
        Rows with ``Revision``, ``Date``, and ``Change``.
    """
    section = section_text(body, "Revision History")
    return read_table(section, HISTORY_HEADER) if section is not None else []


def step_class(before: Revision, after: Revision) -> str | None:
    """Return the segment a step from one revision to the next raised.

    Parameters
    ----------
    before : Revision
        Earlier revision.
    after : Revision
        Later revision.

    Returns
    -------
    str | None
        ``major``, ``minor``, or ``editorial`` when the step raises that
        segment by one and resets those to its right; else ``None``.
    """
    if after == (before[0] + 1, 0, 0):
        return "major"
    if after == (before[0], before[1] + 1, 0):
        return "minor"
    if after == (before[0], before[1], before[2] + 1):
        return "editorial"
    return None


def opens_with(change: str, openers: tuple[str, ...]) -> bool:
    """Return whether a change entry opens with one of some words.

    Parameters
    ----------
    change : str
        Text of the change entry.
    openers : tuple[str, ...]
        Opening words of a class.

    Returns
    -------
    bool
        Whether the entry opens with one of them, ignoring case.
    """
    lowered = change.lower()
    return any(lowered.startswith(w.lower()) for w in openers)
