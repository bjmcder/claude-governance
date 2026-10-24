"""Identifiers, section locators, and whether a reference resolves.

A locator is a document identifier, a number sign, and a heading slug,
as in ``LVL0#normative-language`` (STND.IDENT.15, STND.IDENT.16).
"""

from __future__ import annotations

import re
from collections.abc import Container, Mapping

from govharness.core.entry import Entry

ID_RE = re.compile(
    r"\b(?:[A-Z]{2,5})(?:\.(?:[A-Z]{2,5}))*\.(?:\d+|[a-z0-9-]+)\b"
)
LOCATOR_RE = re.compile(
    r"\b[A-Z]{2,5}\d?(?:\.[A-Z]{2,5})*#[a-z0-9]+(?:-[a-z0-9]+)*\b"
)
HEADING_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$", re.M)
DOCUMENT_IN_PARENS_RE = re.compile(r"\(([A-Z]{2,5}\d?(?:\.[A-Z]{2,5})*)\)")


def heading_slug(heading: str) -> str:
    """Return the locator slug of a heading.

    Parameters
    ----------
    heading : str
        Heading text such as ``Normative Language``.

    Returns
    -------
    str
        Lowercase words joined by hyphens (``normative-language``).
    """
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def heading_slugs(body: str) -> set[str]:
    """Return the slugs of every second-level or deeper heading.

    Parameters
    ----------
    body : str
        Markdown text.

    Returns
    -------
    set[str]
        Slugs of the headings ``##`` to ``######``.
    """
    return {heading_slug(h) for h in HEADING_RE.findall(body)}


def reference_resolves(ref: str, entries: Mapping[str, Entry]) -> bool:
    """Return True when a reference names an entry or a section of one.

    Parameters
    ----------
    ref : str
        A stable identifier (``GOV.12``) or a section locator
        (``LVL0#normative-language``).
    entries : Mapping[str, Entry]
        Entries by identifier.

    Returns
    -------
    bool
        Whether the identifier or the locator's heading exists.
    """
    if "#" not in ref:
        return ref in entries
    document, _, slug = ref.partition("#")
    entry = entries.get(document)
    return entry is not None and slug in heading_slugs(entry.body)


def cited_in_text(known: Container[str], text: str) -> set[str]:
    """Return the identifiers and locators a text names.

    Parameters
    ----------
    known : Container[str]
        Identifiers of the corpus, used to accept a document identifier
        written alone in parentheses.
    text : str
        Provision text.

    Returns
    -------
    set[str]
        Stable identifiers (``GOV.12``, ``LEX.agent``), locators
        (``LVL0#normative-language``), and known document identifiers
        written alone in parentheses (``(LEX)``).
    """
    found = set(LOCATOR_RE.findall(text)) | set(ID_RE.findall(text))
    found |= {
        doc for doc in DOCUMENT_IN_PARENS_RE.findall(text) if doc in known
    }
    return found
