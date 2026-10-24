"""Findings about the modal set and where normative force appears.

Checks g.1 to g.4, g.7, g.8, and g.18: the standard's tables and their
tie to Normative Language, capital letters, one modal per sentence,
modals outside provisions, imperatives, and atomicity.
"""

from __future__ import annotations

import re

from govharness.checks.drafting.context import (
    BELOW,
    STANDARD_ID,
    DraftingContext,
    Finding,
    Unit,
    is_imperative,
    is_status,
    modals_in,
)
from govharness.checks.drafting.tables import table_problems
from govharness.core.text import snippet, unquoted


def tables_tied(ctx: DraftingContext) -> list[Finding]:
    """g.1: tables are present, well formed, and tied to LVL0.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Table problems, and modals whose Normative Language entry the
        LVL0 table does not contain.
    """
    found = [
        Finding(STANDARD_ID, "self", "defect", p)
        for p in table_problems(ctx.tables)
    ]
    words = {w.lower() for ws, _ in ctx.firm_rows for w in ws}
    for row in ctx.tables.tables.get("modal-set", []):
        entry = row["Normative Language entry"].split(",")[0].strip().lower()
        if entry not in words:
            found.append(
                Finding(
                    STANDARD_ID,
                    "self",
                    "defect",
                    f"modal `{row['Modal']}` maps to `{entry}`, which "
                    "the Normative Language table does not contain",
                )
            )
    return found


def forms_covered(ctx: DraftingContext) -> list[Finding]:
    """g.2: each LVL0 form of force is a modal or an excluded expression.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        One finding per form the tables leave uncovered.
    """
    covered = {
        row["Normative Language entry"].split(",")[0].strip().lower()
        for row in ctx.tables.tables.get("modal-set", [])
    }
    excluded = [
        r["Expression"].lower()
        for r in ctx.tables.tables.get("excluded-expressions", [])
    ]
    found = []
    for words, _ in ctx.firm_rows:
        for word in words:
            low = word.lower()
            if low in covered or any(
                e in {low, f"{low} to", f"{low} from"} for e in excluded
            ):
                continue
            found.append(
                Finding(
                    STANDARD_ID,
                    "self",
                    "defect",
                    f"Normative Language form `{word}` is neither a "
                    "modal nor an excluded expression",
                )
            )
    return found


def _scan_lowercase(ctx: DraftingContext, unit: Unit) -> list[Finding]:
    """Find lowercase modals in a unit.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.
    unit : Unit
        Unit to scan.

    Returns
    -------
    list[Finding]
        One finding per lowercase modal; a longer modal is matched first
        and blanked, so ``shall not`` is not also reported as ``shall``.
    """
    found = []
    for sentence in unit.sentences:
        text = unquoted(sentence)
        for low, cls in sorted(
            ctx.lowercase.items(), key=lambda x: -len(x[0])
        ):
            for match in re.finditer(rf"\b{re.escape(low)}\b", text):
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "defect" if cls == "exact" else "review",
                        f"lowercase `{low}`: …{snippet(text, *match.span())}…",
                    )
                )
                text = (
                    text[: match.start()]
                    + " " * len(low)
                    + text[match.end() :]
                )
    return found


def capitals(ctx: DraftingContext) -> list[Finding]:
    """g.3: modals are written in capital letters.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Lowercase modals in provisions and draft bodies below LVL0.
    """
    return [
        f
        for u in ctx.units_for(BELOW, {"provision", "body"})
        for f in _scan_lowercase(ctx, u)
    ]


def one_modal(ctx: DraftingContext) -> list[Finding]:
    """g.4: one modal per sentence, and each provision imposes something.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Sentences with two or more modals, and provisions with no
        modal, status word, or imperative.
    """
    found = []
    for unit in ctx.units_for(BELOW, {"provision", "body"}):
        normative = 0
        for sentence in unit.sentences:
            count = len(modals_in(ctx, sentence))
            if count >= 2:
                found.append(
                    Finding(
                        unit.subject,
                        unit.group,
                        "defect",
                        f"{count} modals in one sentence: …{sentence[:90]}…",
                    )
                )
            if count or is_status(ctx, sentence) or is_imperative(sentence):
                normative += 1
        if unit.kind == "provision" and unit.sentences and not normative:
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "defect",
                    "no sentence carries a modal, a status word, or an "
                    "imperative: the provision imposes nothing",
                )
            )
    return found


def outside_provisions(ctx: DraftingContext) -> list[Finding]:
    """g.7: no sentence outside a numbered provision carries a modal.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Modal sentences in the informative text of documents.
    """
    return [
        Finding(
            u.subject,
            u.group,
            "defect",
            f"normative sentence outside a provision: …{s[:90]}…",
        )
        for u in ctx.units_for({"self", "lower"}, {"informative"})
        for s in u.sentences
        if modals_in(ctx, s)
    ]


def imperatives(ctx: DraftingContext) -> list[Finding]:
    """g.8: sentences that look imperative.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Review findings for imperative-looking sentences with no modal.
    """
    return [
        Finding(
            u.subject, u.group, "review", f"possible imperative: …{s[:90]}…"
        )
        for u in ctx.units_for(BELOW)
        for s in u.sentences
        if not modals_in(ctx, s) and is_imperative(s)
    ]


def atomicity(ctx: DraftingContext) -> list[Finding]:
    """g.18: a provision carries at most three modals.

    Parameters
    ----------
    ctx : DraftingContext
        Drafting context.

    Returns
    -------
    list[Finding]
        Defects above three modals; a review finding at exactly three.
    """
    found = []
    for unit in ctx.units_for({"self", "lower"}, {"provision"}):
        count = sum(len(modals_in(ctx, s)) for s in unit.sentences)
        if count > 3:
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "defect",
                    f"{count} modals; at most three",
                )
            )
        elif count == 3:
            found.append(
                Finding(
                    unit.subject,
                    unit.group,
                    "review",
                    "three modals: confirm the bundle is never applied apart",
                )
            )
    return found
