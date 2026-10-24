"""Findings about citations: their form, their index, and References.

Checks g.15, g.16, and g.25.
"""

from __future__ import annotations

import re

from govharness.checks.drafting.context import (
    BELOW,
    DraftingContext,
    Finding,
)
from govharness.core.corpus import Corpus
from govharness.core.locators import ID_RE, LOCATOR_RE, cited_in_text
from govharness.core.tables import read_table
from govharness.core.text import unquoted
from govharness.derive.references import (
    HEADER,
    SECTION,
    SECTION_RE,
    expected_rows,
)

ID = (
    r"(?:[A-Z]{2,5}\d?(?:\.[A-Z]{2,5})*\.(?:\d+|[a-z0-9-]+)"
    r"|[A-Z]{2,5}\d?#[a-z0-9-]+)"
)
RANGE_RE = re.compile(rf"{ID}\s*(?:to|through|–|—|-|\.\.)\s*(?:{ID}|\d+\b)")
POSITION_RE = re.compile(
    r"\b(?:above|below|preceding|previous|following|next|prior)\s+"
    r"(?:provision|section|paragraph|clause|article|rule)s?\b"
    r"|\b(?:provision|section|paragraph|clause|article|rule)s?\s+"
    r"(?:above|below)\b(?!\s+[A-Z]{2,5}\d?\b)",
    re.IGNORECASE,
)
BARE_NUMBER_RE = re.compile(
    r"\b(?:rule|provision|article|clause)\s+\d+\b", re.I
)
FAMILY_RE = re.compile(
    r"\b[A-Z]{2,5}\s+(?:provisions|articles|rules|clauses)\b"
)
PAREN_RE = re.compile(r"\(([^()]*)\)")
CITATION_FORMS = (
    (RANGE_RE, "defect", "range"),
    (BARE_NUMBER_RE, "defect", "bare number"),
    (POSITION_RE, "defect", "position"),
    (FAMILY_RE, "review", "family"),
)


def citation_form(ctx: DraftingContext) -> list[Finding]:
    """g.15: citations are full identifiers or locators, never ranges.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Ranges, bare numbers, positions, families, and parenthesized
        citations not separated by commas.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"provision", "body"}):
        for sentence in unit.sentences:
            text = unquoted(sentence)
            for pattern, cls, what in CITATION_FORMS:
                for match in pattern.finditer(text):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            cls,
                            f"citation by {what}: `{match.group(0)}`",
                        )
                    )
            for inner in PAREN_RE.findall(text):
                refs = ID_RE.findall(inner) + LOCATOR_RE.findall(inner)
                rest = LOCATOR_RE.sub("", ID_RE.sub("", inner))
                if len(refs) > 1 and re.sub(r"[\s,]", "", rest):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect",
                            f"citations not comma-separated: ({inner})",
                        )
                    )
    return found


def listed_identifiers(ctx: DraftingContext) -> list[Finding]:
    """g.16: the identifiers in the text equal those listed.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Provisions whose text and ``instantiates`` plus ``refers_to``
        name different identifiers.
    """
    found = []
    for unit in ctx.units_for({"self", "lower"}, {"provision"}):
        entry = ctx.corpus.by_id[unit.subject]
        listed = set(entry.meta.get("instantiates") or []) | set(
            entry.meta.get("refers_to") or []
        )
        named = cited_in_text(ctx.corpus.by_id, unquoted(unit.body)) - {
            unit.subject
        }
        if named != listed:
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "defect",
                    f"text-only {sorted(named - listed)}, "
                    f"list-only {sorted(listed - named)}",
                )
            )
    return found


def references_problem(corpus: Corpus, doc_id: str) -> str | None:
    """Return why a document's References table is wrong, or None.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the document.

    Returns
    -------
    str | None
        A short reason, or ``None`` when the table is right.
    """
    body = corpus.by_id[doc_id].body
    section = SECTION_RE.search(body)
    if section is None:
        return f"no section {SECTION}"
    have = [
        (r.get("Identifier", ""), r.get("Title", ""))
        for r in read_table(section.group(0), HEADER)
    ]
    want = expected_rows(corpus, doc_id)
    if have == want:
        return None
    missing = sorted({w[0] for w in want} - {h[0] for h in have})
    extra = sorted({h[0] for h in have} - {w[0] for w in want})
    detail = []
    if missing:
        detail.append(f"missing {', '.join(missing)}")
    if extra:
        detail.append(f"not cited {', '.join(extra)}")
    return "references table " + ("; ".join(detail) or "out of order")


def references_listed(ctx: DraftingContext) -> list[Finding]:
    """g.25: each document's References table (STND.DRAFT.34).

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        One defect per document whose table differs from the derived
        one.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"informative", "body"}):
        problem = references_problem(ctx.corpus, unit.subject)
        if problem:
            found.append(Finding(unit.subject, unit.group, "defect", problem))
    return found
