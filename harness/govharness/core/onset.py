"""The front-matter field ``onset``: the class from which a provision applies.

STND.CLASS.10 has each part of a provision below LVL0 apply from the
class that the field gives; STND.DRAFT#representation-in-the-harness
defines the field. Its value is a class, ``"CSQ3"``, for the whole
provision, or a list whose first item is the class of the provision and
each further item a pair ``[PART, CLASS]`` that gives a named part a
more severe class: ``["CSQ3", ["sentence 2", "CSQ2"]]``. A part is
``sentence N``, the Nth sentence of the body outside its tables, or
``row CELL``, the row of a table of the body whose first cell is CELL.
The class of the provision is CSQ4 only in the list form, where the
provision applies at every class but a part does not; a provision that
applies at every class whole, and every binding provision, carries no
field (unit 0023).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from govharness.core.entry import Entry
from govharness.core.tables import parse_tables
from govharness.core.text import without_tables

FIELD = "onset"
# The classes from the most severe to the least; a lower index is a
# more severe class, from which less work applies.
CLASSES = ("CSQ0", "CSQ1", "CSQ2", "CSQ3", "CSQ4")
# The classes a whole provision, or a named part, may start at.
STARTS = CLASSES[:-1]
# A sentence of a body ends at terminal punctuation, as a reader counts
# sentences; semicolons and colons do not end one here, unlike the
# drafting checks' finer cut.
TERMINAL_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\"“`])")
SENTENCE_PART = re.compile(r"sentence ([1-9][0-9]*)")
ROW_PART = re.compile(r"row (\S.*)")


@dataclass(frozen=True)
class Onset:
    """The parsed value of a field ``onset``.

    Parameters
    ----------
    base : str
        The class from which the provision applies.
    parts : tuple[tuple[str, str], ...]
        Each named part and the more severe class it applies from.
    """

    base: str
    parts: tuple[tuple[str, str], ...] = ()

    def classes(self) -> set[str]:
        """Return every class from which some part applies.

        Returns
        -------
        set[str]
            The base class and the class of each named part.
        """
        return {self.base, *(cls for _, cls in self.parts)}


def parse_onset(value: object) -> Onset:
    """Read the value of a field ``onset``.

    Parameters
    ----------
    value : object
        The JSON value of the field.

    Returns
    -------
    Onset
        The class of the provision and of each named part.

    Raises
    ------
    ValueError
        If the value is neither a class of CSQ0 to CSQ3 nor a list of a
        class of CSQ0 to CSQ4 followed by at least one pair of a part
        and a more severe class, or if a part is named twice.
    """
    if isinstance(value, str):
        if value not in STARTS:
            raise ValueError(f"{value!r} is not a class of CSQ0 to CSQ3")
        return Onset(value)
    if not isinstance(value, list) or len(value) < 2:
        raise ValueError("neither a class nor a list of a class and parts")
    base = value[0]
    if base not in CLASSES:
        raise ValueError(f"{base!r} is not a class")
    parts: list[tuple[str, str]] = []
    for item in value[1:]:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not all(isinstance(x, str) for x in item)
        ):
            raise ValueError(f"{item!r} is not a pair of a part and a class")
        part, cls = item
        if not (SENTENCE_PART.fullmatch(part) or ROW_PART.fullmatch(part)):
            raise ValueError(f"{part!r} names no sentence and no row")
        if cls not in STARTS or CLASSES.index(cls) >= CLASSES.index(base):
            raise ValueError(f"{part}: {cls!r} is not a class after {base}")
        if part in dict(parts):
            raise ValueError(f"{part} is named twice")
        parts.append((part, cls))
    return Onset(base, tuple(parts))


def sentences(body: str) -> list[str]:
    """Return the sentences of a body outside its tables.

    Parameters
    ----------
    body : str
        Markdown body of a provision.

    Returns
    -------
    list[str]
        The sentences, in order, each ending at terminal punctuation;
        the lines of a list belong to the sentence that leads into it.
    """
    prose = " ".join(without_tables(body).split())
    return [s for s in TERMINAL_RE.split(prose) if s.strip()]


def row_keys(body: str) -> list[str]:
    """Return the first cell of each data row of each table of a body.

    Parameters
    ----------
    body : str
        Markdown body of a provision.

    Returns
    -------
    list[str]
        The first cells, in order.
    """
    return [row[0] for _, rows in parse_tables(body) for row in rows if row]


def part_exists(body: str, part: str) -> bool:
    """Return whether a part names a sentence or a row of a body.

    Parameters
    ----------
    body : str
        Markdown body of a provision.
    part : str
        ``sentence N`` or ``row CELL``.

    Returns
    -------
    bool
        True when the body has an Nth sentence, or a row whose first
        cell is CELL.
    """
    number = SENTENCE_PART.fullmatch(part)
    if number:
        return int(number.group(1)) <= len(sentences(body))
    row = ROW_PART.fullmatch(part)
    return bool(row) and row.group(1) in row_keys(body)


def onset_problems(entry: Entry) -> list[str]:
    """Return what is wrong with the field ``onset`` of one entry.

    Parameters
    ----------
    entry : Entry
        Any entry of the corpus.

    Returns
    -------
    list[str]
        Nothing where the entry has no field. Otherwise one line where
        the value is malformed, where the entry is not a provision below
        LVL0, where the provision is not waivable (it binds at every
        class), and for each part that names no sentence or row of its
        body.
    """
    meta = entry.meta
    if FIELD not in meta:
        return []
    name = meta.get("id")
    try:
        onset = parse_onset(meta[FIELD])
    except ValueError as error:
        return [f"- {name}: malformed onset: {error}"]
    if meta.get("kind") != "provision" or meta.get("level") == "LVL0":
        return [
            f"- {name}: an onset on an item other than a provision below LVL0"
        ]
    if meta.get("waivable") is not True:
        return [f"- {name}: an onset on a provision that binds at every class"]
    return [
        f"- {name}: onset names {part}, which its body does not hold"
        for part, _ in onset.parts
        if not part_exists(entry.body, part)
    ]


def onset_of(entry: Entry) -> Onset | None:
    """Return the onset of an entry, or ``None`` where it has none.

    Parameters
    ----------
    entry : Entry
        Any entry of the corpus.

    Returns
    -------
    Onset | None
        The parsed field; ``None`` where the entry has no field or a
        malformed one, which ``verify`` reports.
    """
    if FIELD not in entry.meta:
        return None
    try:
        return parse_onset(entry.meta[FIELD])
    except ValueError:
        return None


def describe(onset: Onset) -> str:
    """Write an onset as a reader reads it beside the mode.

    Parameters
    ----------
    onset : Onset
        A parsed field.

    Returns
    -------
    str
        ``from CSQ3``, then ``sentence 2 from CSQ2`` for each part;
        a provision of class CSQ4 reads ``at every class``.
    """
    head = "at every class" if onset.base == "CSQ4" else f"from {onset.base}"
    return "; ".join(
        [head, *(f"{part} from {cls}" for part, cls in onset.parts)]
    )


def _numbered(entry: Entry) -> tuple[str, int]:
    """Return the sort key of a provision: its directory, then its number.

    Parameters
    ----------
    entry : Entry
        A numbered provision.

    Returns
    -------
    tuple[str, int]
        The directory and the number of the file.
    """
    stem = entry.path.stem
    return (entry.path.parent.as_posix(), int(stem) if stem.isdigit() else 0)


def applying_from(
    entries: list[Entry], cls: str
) -> list[tuple[Entry, str | None]]:
    """Return the provisions and the parts that apply from one class.

    Parameters
    ----------
    entries : list[Entry]
        The corpus entries.
    cls : str
        A class of CSQ0 to CSQ3.

    Returns
    -------
    list[tuple[Entry, str | None]]
        Each provision whose field gives the class to the whole
        provision, with ``None``, and each named part given the class,
        with its name; by document, then by number, so a
        reclassification to the class adds exactly these.
    """
    found: list[tuple[Entry, str | None]] = []
    for entry in sorted(entries, key=_numbered):
        onset = onset_of(entry)
        if onset is None:
            continue
        if onset.base == cls:
            found.append((entry, None))
        found.extend((entry, part) for part, c in onset.parts if c == cls)
    return found
