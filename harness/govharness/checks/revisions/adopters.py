"""Owner fields name role labels: check v.5 and the project templates.

A document names its adopter by role label in ``adopted_by``
(``ratified_by`` for the constitution), as in The Custodian; project
template owner fields read The Human Owner (STND.IDENT.12).
"""

from __future__ import annotations

import re
from typing import Any

from govharness.checks.base import CheckContext, Verdict
from govharness.checks.revisions.classes import documents
from govharness.core.corpus import Corpus

ADOPTER_FIELDS = ("ratified_by", "adopted_by")
# The statuses under which STND.IDENT.12 asks for the adopter field.
IN_FORCE = ("adopted", "ratified")
TEMPLATE_FIELDS = (
    "human_owner",
    "adopted_by",
    "declared_by",
    "decided_by",
    "grantor",
    "authorized_by",
)


def normalize_label(text: str) -> str:
    """Return a role label in lowercase without The or a plural s.

    Parameters
    ----------
    text : str
        A role label or a Lexicon term.

    Returns
    -------
    str
        The form used to compare labels with terms.
    """
    lowered = re.sub(r"^the\s+", "", text.strip().lower())
    return lowered.removesuffix("s")


def role_labels(corpus: Corpus) -> set[str]:
    """Return the normalized names of the roles the Lexicon defines.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    set[str]
        Names of the terms of the group Roles.
    """
    return {
        normalize_label(str(t.meta.get("term")))
        for t in corpus.terms()
        if t.meta.get("group") == "Roles"
    }


def _not_a_role(value: str, roles: set[str]) -> bool:
    """Return True when an owner field does not name a defined role.

    Parameters
    ----------
    value : str
        Field value.
    roles : set[str]
        Normalized role names.

    Returns
    -------
    bool
        Whether the value lacks the opening ``The `` or names no role.
    """
    return not value.startswith("The ") or normalize_label(value) not in roles


def adopter_field(meta: dict[str, Any]) -> str:
    """Return the field in which a document names its adopter.

    Parameters
    ----------
    meta : dict[str, Any]
        Front matter of a document.

    Returns
    -------
    str
        ``ratified_by`` for the constitution, else ``adopted_by``
        (STND.IDENT.12).
    """
    return (
        "ratified_by" if meta.get("kind") == "constitution" else "adopted_by"
    )


def adopters_named(ctx: CheckContext) -> Verdict:
    """Check v.5: adopter fields name a role that the Lexicon defines.

    STND.IDENT.12 names the field for each kind, ``ratified_by`` for the
    constitution and ``adopted_by`` for the others, and requires it of
    a document that is adopted or ratified; a draft or a planned
    document names no adopter yet. A field that is present names a role
    label whatever the status.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on an adopted or ratified document without the adopter
        field of its kind, or on a document with an adopter field that
        is not a role label.
    """
    roles = role_labels(ctx.corpus)
    problems: list[str] = []
    for entry in documents(ctx.corpus):
        wanted = adopter_field(entry.meta)
        in_force = entry.meta.get("status") in IN_FORCE
        if in_force and wanted not in entry.meta:
            problems.append(
                f"- {entry.meta['id']}: names no adopter in `{wanted}`"
            )
        named = [f for f in ADOPTER_FIELDS if f in entry.meta]
        for name in named:
            value = str(entry.meta[name] or "")
            if _not_a_role(value, roles):
                problems.append(
                    f"- {entry.meta['id']}: `{name}` is `{value}`, not a "
                    "role label"
                )
    return Verdict("FAIL" if problems else "PASS", problems)


def template_problems(
    templates: dict[str, dict[str, Any]], roles: set[str]
) -> list[str]:
    """Return owner fields of project templates that name no role.

    Parameters
    ----------
    templates : dict[str, dict[str, Any]]
        Front matter by path, for each file of a project template.
    roles : set[str]
        Normalized role names, from ``role_labels``.

    Returns
    -------
    list[str]
        One line per owner field that is blank or not a role label.
    """
    problems: list[str] = []
    for path, meta in sorted(templates.items()):
        for name in TEMPLATE_FIELDS:
            if name not in meta:
                continue
            value = str(meta[name] or "")
            if _not_a_role(value, roles):
                problems.append(
                    f"template {path}: `{name}` is `{value}`, not a role label"
                )
    return problems
