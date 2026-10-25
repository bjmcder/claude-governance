"""Findings about citations: their form, their index, and References.

Checks g.15, g.16, and g.25. g.25 compares each References table with
the one derived from the document's citations, and fails when the text
names a document by its bare identifier ("HDES", "STND.DOCS") without
citing it, so that the derived table cannot miss a document the text
names (unit 0013).
"""

from __future__ import annotations

import re

from govharness.checks.drafting.context import (
    BELOW,
    DraftingContext,
    Finding,
)
from govharness.core.corpus import Corpus
from govharness.core.entry import DOC_FILE
from govharness.core.locators import ID_RE, LOCATOR_RE, cited_in_text
from govharness.core.tables import HISTORY_HEADING, read_table
from govharness.core.text import CODE_RE, FENCE_RE, unquoted
from govharness.derive.references import (
    HEADER,
    SECTION,
    SECTION_RE,
    expected_rows,
    members_of,
    without_section,
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
    r"\b(?:rule|provision|article|clause)\s+\d+\b", re.IGNORECASE
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
# A document identifier written as a word of its own. The match is the
# longest dotted run, so "HW.CPU" names HW.CPU, not HW.
NAME_RE = re.compile(
    r"(?<![A-Za-z0-9.])([A-Z]{2,5}\d?(?:\.[A-Z]{2,5})*)(?![A-Za-z0-9])"
)
HISTORY_RE = re.compile(
    rf"^{re.escape(HISTORY_HEADING)}\s*\n.*?(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)
# The documents STND.DRAFT.34 asks to hold References, and the word that
# names the level of the constitution rather than citing it.
NAMING_LEVELS = {"LVL1", "LVL2", "LVL3"}
NOT_NAMES = {"LVL0"}
EXAMPLE_COLUMN = "Example"


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


def without_example_tables(text: str) -> str:
    """Drop every row of a table whose header names a column Example.

    Such a table lists identifiers as examples of a form. Its other
    cells mention them too, so the whole table goes.

    Parameters
    ----------
    text : str
        Markdown text.

    Returns
    -------
    str
        The text without those tables.
    """
    kept: list[str] = []
    skipping = in_table = False
    for line in text.split("\n"):
        if line.lstrip().startswith("|"):
            if not in_table:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                skipping = EXAMPLE_COLUMN in cells
            in_table = True
            if skipping:
                continue
        else:
            in_table = skipping = False
        kept.append(line)
    return "\n".join(kept)


def naming_text(body: str) -> str:
    """Return the part of a body in which a bare name cites a document.

    Parameters
    ----------
    body : str
        Markdown body of an entry.

    Returns
    -------
    str
        The body without its References section, its Revision History,
        tables of examples, fenced and inline code, and quoted spans.
    """
    text = HISTORY_RE.sub("", without_section(body))
    text = without_example_tables(text)
    text = CODE_RE.sub(" ", FENCE_RE.sub("\n", text))
    return unquoted(text)


def named_documents(corpus: Corpus, doc_id: str) -> list[str]:
    """Return the other documents a document names by bare identifier.

    Only a document at LVL1 to LVL3 is read, since STND.DRAFT.34 asks
    only those to hold References. Its own text and that of its
    provisions and terms are read, outside the parts that
    ``naming_text`` leaves out.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    doc_id : str
        Identifier of the naming document.

    Returns
    -------
    list[str]
        Sorted identifiers of the documents named; empty for a document
        at another level.
    """
    if str(corpus.by_id[doc_id].meta.get("level")) not in NAMING_LEVELS:
        return []
    documents = {
        str(e.meta["id"]) for e in corpus.entries if e.path.name == DOC_FILE
    }
    named: set[str] = set()
    for entry in members_of(corpus, doc_id):
        named |= set(NAME_RE.findall(naming_text(entry.body)))
    return sorted((named & documents) - NOT_NAMES - {doc_id})


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
        A short reason, or ``None`` when the table equals the derived
        one and every document that the text names
        (``named_documents``) is cited.
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
    uncited = sorted(
        set(named_documents(corpus, doc_id)) - {w[0] for w in want}
    )
    if have == want and not uncited:
        return None
    missing = sorted({w[0] for w in want} - {h[0] for h in have})
    extra = sorted({h[0] for h in have} - {w[0] for w in want})
    detail = []
    if missing:
        detail.append(f"missing {', '.join(missing)}")
    if extra:
        detail.append(f"not cited {', '.join(extra)}")
    problems = []
    if have != want:
        problems.append(
            "references table " + ("; ".join(detail) or "out of order")
        )
    if uncited:
        problems.append(
            f"text names {', '.join(uncited)} without a citation (cite a "
            "provision, or the document in parentheses)"
        )
    return "; ".join(problems)


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
        one, or whose text names a document by bare identifier without
        citing it.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"informative", "body"}):
        problem = references_problem(ctx.corpus, unit.subject)
        if problem:
            found.append(Finding(unit.subject, unit.group, "defect", problem))
    return found
