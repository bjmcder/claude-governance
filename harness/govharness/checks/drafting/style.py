"""Findings about style: person, contractions, and spelling.

Checks g.21 and g.22.
"""

from __future__ import annotations

import re

from govharness.checks.drafting.context import (
    ALL_GROUPS,
    DraftingContext,
    Finding,
)
from govharness.core.text import snippet, unquoted

CONTRACTION_RE = re.compile(r"\b\w+(?:n't|'ll|'re|'ve|'d|'m)\b", re.I)


def person(ctx: DraftingContext) -> list[Finding]:
    """g.21: third person, and no contractions.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Defects for each person word of the table and each contraction.
    """
    found = []
    for row in ctx.tables.tables.get("person-words", []):
        word = row["Word"]
        pattern = re.compile(
            rf"(?<![\w'-]){re.escape(word)}(?![\w'-])",
            0 if word.isupper() or len(word) == 1 else re.IGNORECASE,
        )
        for unit in ctx.units_for(ALL_GROUPS, {"provision", "body"}):
            for sentence in unit.sentences:
                text = unquoted(sentence)
                for match in pattern.finditer(text):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect",
                            f"person word `{match.group(0)}`: "
                            f"…{snippet(text, *match.span())}…",
                        )
                    )
    for unit in ctx.units_for(ALL_GROUPS, {"provision", "body"}):
        for sentence in unit.sentences:
            for match in CONTRACTION_RE.finditer(unquoted(sentence)):
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "defect",
                        f"contraction `{match.group(0)}`",
                    )
                )
    return found


def spelling(ctx: DraftingContext) -> list[Finding]:
    """g.22: American spelling.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Defects naming the American spelling.
    """
    found = []
    for row in ctx.tables.tables.get("spelling", []):
        pattern = re.compile(
            rf"\b{re.escape(row['British'])}(?:s|d|ed|ing)?\b", re.I
        )
        for unit in ctx.units_for(ALL_GROUPS, {"provision", "body"}):
            for sentence in unit.sentences:
                for match in pattern.finditer(unquoted(sentence)):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect",
                            f"`{match.group(0)}`, write {row['American']}",
                        )
                    )
    return found
