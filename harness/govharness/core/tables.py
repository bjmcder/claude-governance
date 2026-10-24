"""Read Markdown tables and named sections from a body.

The harness reads every table by its column headings, never by its
position, so rewording a sentence cannot empty a list.
"""

from __future__ import annotations

import re

from govharness.core.text import TABLE_LINE_RE

Table = tuple[list[str], list[list[str]]]
# The heading of the revision history that ends each divided standard.
HISTORY_HEADING = "## Revision History"


def parse_tables(body: str) -> list[Table]:
    """Return every Markdown table in a body as (header, rows).

    Parameters
    ----------
    body : str
        Markdown text.

    Returns
    -------
    list[Table]
        Each table's heading cells and data rows; separator rows are
        dropped.
    """
    tables: list[Table] = []
    current: list[list[str]] = []
    for line in [*body.splitlines(), ""]:
        if TABLE_LINE_RE.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(set(c) <= set("-: ") and c for c in cells):
                current.append(cells)
        elif current:
            tables.append((current[0], current[1:]))
            current = []
    return tables


def read_table(body: str, header: tuple[str, ...]) -> list[dict[str, str]]:
    """Return the rows of the first table whose headings equal a header.

    Parameters
    ----------
    body : str
        Markdown text.
    header : tuple[str, ...]
        Column headings, in order.

    Returns
    -------
    list[dict[str, str]]
        Rows mapping each heading to its cell; empty when no table has
        those headings.
    """
    for found, rows in parse_tables(body):
        if tuple(found) == header:
            return [dict(zip(header, row, strict=False)) for row in rows]
    return []


def section_text(body: str, heading: str) -> str | None:
    """Return the text under a second-level heading, or None.

    Parameters
    ----------
    body : str
        Markdown text.
    heading : str
        Heading text after ``## ``.

    Returns
    -------
    str | None
        Everything up to the next second-level heading, or ``None``
        when the body has no such heading.
    """
    found = re.search(
        rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    return found.group(1) if found else None
