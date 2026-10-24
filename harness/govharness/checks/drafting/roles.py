"""Findings about titles, role words, and defined terms.

Checks g.17, g.19, and g.20.
"""

from __future__ import annotations

from collections import Counter

from govharness.checks.drafting.context import (
    ALL_GROUPS,
    IMPERATIVE_VERBS,
    DraftingContext,
    Finding,
)
from govharness.checks.drafting.tables import (
    TERMS_HEADER,
    expression_pattern,
    terms_of,
    terms_section,
)
from govharness.core.tables import parse_tables
from govharness.core.text import normalise_term, unquoted


def titles(ctx: DraftingContext) -> list[Finding]:
    """g.17: titles are short noun phrases and distinct in the corpus.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Titles that are long, end with a period, open with a verb, or
        repeat another provision's title.
    """
    found = []
    seen: dict[str, list[str]] = {}
    for entry in ctx.corpus.provisions():
        seen.setdefault(str(entry.meta.get("title", "")).lower(), []).append(
            str(entry.meta["id"])
        )
    for unit in ctx.units_for({"self", "lower"}, {"provision"}):
        title = str(ctx.corpus.by_id[unit.subject].meta.get("title", ""))
        words = title.split()
        if not 1 <= len(words) <= 6 or title.endswith("."):
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "defect",
                    f"title `{title}` is not a short noun phrase",
                )
            )
        elif words[0].lower() in IMPERATIVE_VERBS:
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "review",
                    f"title `{title}` begins with a verb",
                )
            )
        twins = [i for i in seen.get(title.lower(), []) if i != unit.subject]
        if twins:
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "defect",
                    f"title `{title}` also names {twins}",
                )
            )
    return found


def _defined_roles(ctx: DraftingContext, document: str) -> set[str]:
    """Return the role names the Lexicon or a document defines.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.
    document : str
        Identifier of the document whose Terms section also counts.

    Returns
    -------
    set[str]
        Normalised names.
    """
    names = {
        normalise_term(str(t.meta.get("term", ""))) for t in ctx.corpus.terms()
    }
    entry = ctx.corpus.by_id.get(document)
    if entry is not None:
        names |= {normalise_term(t) for t in terms_of(entry.body)}
    return names


def role_words(ctx: DraftingContext) -> list[Finding]:
    """g.19: retired role words are absent; undefined ones are flagged.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Defects for retired words; review findings for undefined words
        that neither the Lexicon nor the document defines.
    """
    found = []
    for row in ctx.tables.tables.get("role-words", []):
        pattern = expression_pattern(row["Word"])
        compounds = [
            c.strip().lower()
            for c in row["Allowed compounds"].split(",")
            if c.strip() and c.strip().lower() != "none"
        ]
        for unit in ctx.units_for(ALL_GROUPS):
            document = (
                unit.subject.rsplit(".", 1)[0]
                if unit.kind == "provision"
                else unit.subject
            )
            for sentence in unit.sentences:
                text = unquoted(sentence)
                for match in pattern.finditer(text):
                    tail = text[match.start() :].lower()
                    if any(tail.startswith(c) for c in compounds):
                        continue
                    if row["Class"] == "undefined":
                        if (
                            normalise_term(row["Word"])
                            in _defined_roles(ctx, document)
                            or unit.group == "lvl0"
                        ):
                            continue
                        cls = "review"
                    else:
                        cls = "defect"
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            cls,
                            f"{row['Class']} role word `{match.group(0)}`; "
                            f"write {row['Replace with']}",
                        )
                    )
    return found


def defined_terms(ctx: DraftingContext) -> list[Finding]:
    """g.20: terms are defined once and never redefine the Lexicon.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Terms a document defines twice or that the Lexicon defines.
    """
    found = []
    lexicon = {
        normalise_term(str(t.meta.get("term", ""))): str(t.meta["id"])
        for t in ctx.corpus.terms()
    }
    header = list(TERMS_HEADER)
    for unit in ctx.units_for({"self", "lower"}, {"informative"}):
        names = [
            normalise_term(r["Term"])
            for found_header, rows in parse_tables(terms_section(unit.body))
            if found_header == header
            for r in (
                dict(zip(found_header, row, strict=False)) for row in rows
            )
        ]
        for name, count in Counter(names).items():
            if count > 1:
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "defect",
                        f"term `{name}` defined {count} times",
                    )
                )
        for name in names:
            if name in lexicon:
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "defect",
                        f"term `{name}` redefines {lexicon[name]}",
                    )
                )
    return found
