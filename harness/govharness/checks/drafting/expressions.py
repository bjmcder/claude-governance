"""Findings about wording that the standard excludes or limits.

Checks g.5, g.6, g.9 to g.14: excluded expressions, informative markers
and fill-in guidance, vague qualifiers, negated lists, conditions,
quantifiers, and numbers.
"""

from __future__ import annotations

import re

from govharness.checks.drafting.context import (
    ALL_GROUPS,
    BELOW,
    DraftingContext,
    Finding,
)
from govharness.checks.drafting.tables import expression_pattern
from govharness.core.locators import ID_RE, LOCATOR_RE
from govharness.core.text import snippet, unquoted

MARKER_RE = re.compile(
    r"\bfor example\b|\bfor instance\b|\be\.g\.|\bi\.e\.|\bsuch as\b"
    r"|\bnote:|\brationale\b",
    re.IGNORECASE,
)
CONDITION_RE = re.compile(r"\b(?:if|when|whenever|where|unless)\b", re.I)
NEGATED_RE = re.compile(r"\b(?:SHALL|SHOULD) NOT\b")
NUMBER_RE = re.compile(r"(?<![\w.#-])\d+(?:\.\d+)?(?![\w#-])")
FILL_IN_LABEL = re.compile(r"\bFill-in guidance:")
# LVL0 itself uses these two in the Normative Language it defines, so
# they are not reported against LVL0.
LVL0_OWN_EXPRESSIONS = {"NEVER", "SHALL NEVER"}


def _scan_excluded(ctx: DraftingContext, cls: str) -> list[Finding]:
    """Scan every unit for the excluded expressions of one class.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.
    cls : str
        ``exact`` or ``review``.

    Returns
    -------
    list[Finding]
        One finding per use, of that class.
    """
    rows = [
        (expression_pattern(r["Expression"]), r)
        for r in ctx.tables.tables.get("excluded-expressions", [])
        if r["Class"] == cls
    ]
    found = []
    for unit in ctx.units_for(ALL_GROUPS, {"provision", "body"}):
        for sentence in unit.sentences:
            text = unquoted(sentence)
            for pattern, row in rows:
                if (
                    unit.group == "lvl0"
                    and row["Expression"] in LVL0_OWN_EXPRESSIONS
                ):
                    continue
                for match in pattern.finditer(text):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect" if cls == "exact" else "review",
                            f"`{match.group(0)}` reads as {row['Read as']}: "
                            f"…{snippet(text, *match.span())}…",
                        )
                    )
    return found


def excluded_exact(ctx: DraftingContext) -> list[Finding]:
    """g.5: no provision uses an excluded expression of class exact.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Defects, one per use.
    """
    return _scan_excluded(ctx, "exact")


def excluded_review(ctx: DraftingContext) -> list[Finding]:
    """g.6: excluded expressions of class review, for substitution.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Review findings, one per use.
    """
    return _scan_excluded(ctx, "review")


def informative_markers(ctx: DraftingContext) -> list[Finding]:
    """g.9: rationale and examples stay out; no fill-in labels remain.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Informative markers in bodies, and fill-in guidance left in a
        LVL3 instrument.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"provision", "body"}):
        for sentence in unit.sentences:
            text = unquoted(sentence)
            for match in MARKER_RE.finditer(text):
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "defect" if unit.kind == "provision" else "review",
                        f"informative marker `{match.group(0)}` in a "
                        "provision body",
                    )
                )
    for unit in ctx.units_for(BELOW):
        if unit.level == "LVL3":
            for sentence in unit.sentences:
                if FILL_IN_LABEL.search(unquoted(sentence)):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect",
                            "fill-in guidance remains in an instantiated "
                            "instrument",
                        )
                    )
    return found


def qualifiers(ctx: DraftingContext) -> list[Finding]:
    """g.10: no vague qualifier without a criterion or a decider.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        One finding per qualifier, of the class its table row gives.
    """
    found = []
    for row in ctx.tables.tables.get("vague-qualifiers", []):
        pattern = expression_pattern(row["Qualifier"])
        for unit in ctx.units_for(ALL_GROUPS, {"provision", "body"}):
            for sentence in unit.sentences:
                text = unquoted(sentence)
                for match in pattern.finditer(text):
                    exact = row["Class"] == "exact"
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect" if exact else "review",
                            f"qualifier `{match.group(0)}`: "
                            f"…{snippet(text, *match.span())}…",
                        )
                    )
    return found


def negated_lists(ctx: DraftingContext) -> list[Finding]:
    """g.11: flag a negated modal over a list joined by or or nor.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Review findings.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"provision", "body"}):
        for sentence in unit.sentences:
            text = unquoted(sentence)
            match = NEGATED_RE.search(text)
            if match and re.search(r"\b(?:or|nor)\b", text[match.end() :]):
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "review",
                        f"negated modal over a list: …{text[:90]}…",
                    )
                )
    return found


def conditions(ctx: DraftingContext) -> list[Finding]:
    """g.12: conditions come first, and a sentence carries at most one.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Review findings for several conditions, or a condition after
        the modal.
    """
    found = []
    modal_re = ctx.modal_re() if ctx.modals else None
    for unit in ctx.units_for(BELOW, {"provision", "body"}):
        for sentence in unit.sentences:
            text = unquoted(sentence)
            starts = [m.start() for m in CONDITION_RE.finditer(text)]
            if len(starts) > 1:
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "review",
                        f"{len(starts)} conditions: …{text[:90]}…",
                    )
                )
            modal = modal_re.search(text) if modal_re else None
            if modal and any(c > modal.start() for c in starts):
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "review",
                        f"condition follows the clause: …{text[:90]}…",
                    )
                )
    return found


def quantifiers(ctx: DraftingContext) -> list[Finding]:
    """g.13: no provision uses a word of the quantifier table.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Defects naming the replacement.
    """
    found = []
    for row in ctx.tables.tables.get("quantifiers", []):
        pattern = expression_pattern(row["Word"])
        for unit in ctx.units_for(ALL_GROUPS, {"provision", "body"}):
            for sentence in unit.sentences:
                text = unquoted(sentence)
                for match in pattern.finditer(text):
                    found.append(
                        Finding(
                            unit.subject,
                            unit.group,
                            "defect",
                            f"quantifier `{match.group(0)}`, write "
                            f"{row['Replace with']}: "
                            f"…{snippet(text, *match.span())}…",
                        )
                    )
    return found


def numbers(ctx: DraftingContext) -> list[Finding]:
    """g.14: numbers in provisions, for the unit and bound test.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Review findings, one per number outside an identifier.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"provision", "body"}):
        for sentence in unit.sentences:
            text = LOCATOR_RE.sub(" ", ID_RE.sub(" ", unquoted(sentence)))
            for match in NUMBER_RE.finditer(text):
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "review",
                        f"number `{match.group(0)}`: "
                        f"…{snippet(text, *match.span())}…",
                    )
                )
    return found
