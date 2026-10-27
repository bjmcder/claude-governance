"""Read the data tables of the drafting standard from its provisions.

A provision of the standard that holds a table names it in the
front-matter field ``defines``. The harness finds the table by that name
and by its column headings, so rewording a sentence cannot empty a list.
Expressions become regular expressions here, with inflections, so that
"is not allowed" also matches "are not allowed".
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.tables import parse_tables, read_table, section_text
from govharness.core.text import CODE_RE, FENCE_RE

TABLE_SPECS: dict[str, tuple[str, ...]] = {
    "modal-set": (
        "Modal",
        "Expresses",
        "Normative Language entry",
        "Lowercase",
    ),
    "excluded-expressions": ("Expression", "Class", "Read as"),
    "vague-qualifiers": ("Qualifier", "Class"),
    "quantifiers": ("Word", "Replace with"),
    "role-words": ("Word", "Class", "Replace with", "Allowed compounds"),
    "person-words": ("Word", "Replace with"),
    "spelling": ("British", "American"),
}
CLASSES = {
    "modal-set": ("Lowercase", {"exact", "review"}),
    "excluded-expressions": ("Class", {"exact", "review"}),
    "vague-qualifiers": ("Class", {"exact", "review"}),
    "role-words": ("Class", {"retired", "undefined"}),
}
VERB_SUFFIX = r"(?:s|d|ed|ing|red|ring)?"
TERMS_HEADER = ("Term", "Definition")


@dataclass
class StandardTables:
    """Tables read from the drafting standard.

    Parameters
    ----------
    tables : dict[str, list[dict[str, str]]]
        Rows by table name; each row maps a column heading to its cell.
    owners : dict[str, str]
        Identifier of the provision that holds each table.
    problems : list[str]
        Reasons a table could not be read.
    """

    tables: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    owners: dict[str, str] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)


def read_standard_tables(corpus: Corpus, standard_id: str) -> StandardTables:
    """Read every named table of a standard.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    standard_id : str
        Identifier of the drafting standard (``STND.DRAFT``).

    Returns
    -------
    StandardTables
        The tables, their owners, and the problems found.
    """
    out = StandardTables()
    holders: dict[str, list[str]] = {}
    prefix = f"{standard_id}."
    for pid, entry in sorted(corpus.by_id.items()):
        if pid.startswith(prefix):
            for name in entry.meta.get("defines") or []:
                holders.setdefault(name, []).append(pid)
    for name, header in TABLE_SPECS.items():
        owners = holders.get(name, [])
        if len(owners) != 1:
            out.problems.append(
                f"table `{name}` is defined by {len(owners)} provisions"
            )
            continue
        rows = read_table(corpus.by_id[owners[0]].body, header)
        if not rows:
            out.problems.append(
                f"{owners[0]}: no table with columns {', '.join(header)}"
            )
            continue
        out.tables[name] = rows
        out.owners[name] = owners[0]
    for name in holders:
        if name not in TABLE_SPECS:
            out.problems.append(f"unknown table name `{name}`")
    return out


def table_problems(tables: StandardTables) -> list[str]:
    """Return structural problems in the tables read.

    Parameters
    ----------
    tables : StandardTables
        Tables read from the standard.

    Returns
    -------
    list[str]
        Reading problems, unknown classes, excluded expressions read as
        no modal of the set, and words listed twice.
    """
    problems = list(tables.problems)
    modals = {r["Modal"] for r in tables.tables.get("modal-set", [])}
    for name, (column, allowed) in CLASSES.items():
        for row in tables.tables.get(name, []):
            if row[column] not in allowed:
                problems.append(
                    f"{tables.owners[name]}: `{row[column]}` is not a class "
                    f"of {column}"
                )
    for row in tables.tables.get("excluded-expressions", []):
        if row["Read as"] not in modals:
            owner = tables.owners["excluded-expressions"]
            problems.append(
                f"{owner}: `{row['Expression']}` is read as "
                f"`{row['Read as']}`, not a modal of the set"
            )
    for name, key in (
        ("excluded-expressions", "Expression"),
        ("vague-qualifiers", "Qualifier"),
        ("role-words", "Word"),
        ("quantifiers", "Word"),
    ):
        seen: set[str] = set()
        for row in tables.tables.get(name, []):
            word = row[key].lower()
            if word in seen:
                problems.append(
                    f"{tables.owners[name]}: `{word}` listed twice"
                )
            seen.add(word)
    return problems


def _token_pattern(token: str, first: bool) -> str:
    """Return the regular expression for one token of an expression.

    Parameters
    ----------
    token : str
        One word of the expression.
    first : bool
        Whether it opens the expression; only an opening ``is`` also
        matches ``are``.

    Returns
    -------
    str
        A pattern that matches the word and its inflections.
    """
    lowered = token.lower()
    special = {
        "is": r"(?:is|are)" if first else "is",
        "has": r"(?:has|have|had)",
        "needs": r"needs?",
        "need": r"needs?",
        "cannot": r"can\s?not",
    }
    if lowered in special and token == lowered:
        return special[lowered]
    return re.escape(token)


def expression_pattern(expression: str) -> re.Pattern[str]:
    """Compile an expression of the tables to a regular expression.

    Parameters
    ----------
    expression : str
        A table entry such as ``is not allowed`` or ``NEVER``.

    Returns
    -------
    re.Pattern[str]
        Matches inflections (``are not allowed``, ``have to``,
        ``prefers``). An entry written in capitals matches capitals only.
    """
    tokens = expression.split()
    if len(tokens) == 1 and tokens[0] in {"prefer", "avoid", "consider"}:
        body = re.escape(tokens[0]) + VERB_SUFFIX
        if tokens[0] == "prefer":
            body += r"|preferably"
    else:
        body = r"\s+".join(
            _token_pattern(t, i == 0) for i, t in enumerate(tokens)
        )
    flags = 0 if expression.isupper() else re.IGNORECASE
    return re.compile(rf"(?<![\w/-])(?:{body})(?![\w/-])", flags)


def terms_section(body: str) -> str:
    """Return the text of a body's Terms section, or an empty string.

    Parameters
    ----------
    body : str
        Markdown body of a document.

    Returns
    -------
    str
        The section text.
    """
    return section_text(body, "Terms") or ""


def terms_of(body: str) -> dict[str, str]:
    """Return the terms a document defines in its Terms section.

    Parameters
    ----------
    body : str
        Markdown body of a document.

    Returns
    -------
    dict[str, str]
        Definition by term; empty when there is no Terms section.
    """
    section = section_text(body, "Terms")
    if section is None:
        return {}
    rows = read_table(section, TERMS_HEADER)
    return {r["Term"]: r["Definition"] for r in rows}


# The headings of the mention columns that STND.DRAFT names in its section
# Representation in the harness: their entries are mentioned, not used.
MENTION_COLUMNS = frozenset({
    "Modal", "Normative Language entry", "Expression", "Read as",
    "Qualifier", "Word", "British", "American", "Not used", "Used",
    "Opening words",
})


def table_cells(entry: Entry) -> list[str]:
    """Return the table cells of a provision that are read as prose.

    The body of a numbered provision, including a table it contains, is
    normative (STND.DRAFT, Normative and informative parts), so each
    data cell is read as prose, its inline code left out. A cell of a
    mention column (STND.DRAFT, term Mention column) is left out, being
    a word that the provision mentions; the harness finds such a column
    by its heading. Header cells are read too, except in a provision that
    names its table in ``defines``, whose headings the harness reads as
    data: elsewhere a row without the delimiter row below it is no table
    in Markdown, but ``parse_tables`` takes it for a header.

    Parameters
    ----------
    entry : Entry
        Any entry.

    Returns
    -------
    list[str]
        Text of each cell, in order; empty for an entry that is not a
        provision.
    """
    if entry.meta.get("kind") != "provision":
        return []
    defines = bool(entry.meta.get("defines"))
    out: list[str] = []
    for header, rows in parse_tables(FENCE_RE.sub("\n", entry.body)):
        mentioned = {
            i for i, h in enumerate(header) if h.strip() in MENTION_COLUMNS
        }
        for n, row in enumerate(rows if defines else (header, *rows)):
            is_header = not defines and n == 0
            for i, cell in enumerate(row):
                if i in mentioned and not is_header:
                    continue
                if text := CODE_RE.sub(" ", cell).strip():
                    out.append(text)
    return out
