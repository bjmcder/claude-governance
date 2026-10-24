"""Structural checks of ``verify``: owner fields and status fields.

templates: every owner field of a project template names a role
(STND.IDENT.12); the corpus view leaves templates out, so they are read
from the file snapshot. status: every entry carries the status of the
document in its directory, and an entry of an adopted or ratified
document carries an adoption date, so that adopting a document cannot
leave its provisions at draft.
"""

from __future__ import annotations

from typing import Any

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.revisions.adopters import role_labels, template_problems
from govharness.checks.revisions.classes import ADOPTED
from govharness.checks.structure import failing
from govharness.core.corpus import Tree
from govharness.core.entry import (
    DOC_FILE,
    README_FILE,
    Entry,
    in_template,
    parse_entry,
)

FAMILY = "structure"


def template_fields(tree: Tree) -> dict[str, dict[str, Any]]:
    """Return the front matter of every project template file.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.

    Returns
    -------
    dict[str, dict[str, Any]]
        Front matter by POSIX path; a note without front matter holds
        no owner field and is skipped.
    """
    found: dict[str, dict[str, Any]] = {}
    for rel in tree.markdown():
        if rel.name == README_FILE or not in_template(rel):
            continue
        try:
            found[rel.as_posix()] = parse_entry(tree.text(rel))[0]
        except ValueError:
            continue
    return found


def status_problems(entries: list[Entry]) -> list[str]:
    """Return the entries whose status disagrees with their document.

    Parameters
    ----------
    entries : list[Entry]
        The loaded corpus.

    Returns
    -------
    list[str]
        One line per entry whose ``status`` differs from that of the
        ``_doc.md`` in its directory, or whose document is adopted or
        ratified while the entry carries no ``adopted`` date.
    """
    documents = {e.path.parent: e for e in entries if e.path.name == DOC_FILE}
    errors: list[str] = []
    for entry in entries:
        document = documents.get(entry.path.parent)
        if entry.path.name == DOC_FILE or document is None:
            continue
        expected = document.meta.get("status")
        status = entry.meta.get("status")
        name = entry.meta.get("id")
        if status != expected:
            errors.append(
                f"{name}: status {status!r}, but {document.meta.get('id')} "
                f"is {expected!r}"
            )
        elif expected in ADOPTED and not entry.meta.get("adopted"):
            errors.append(f"{name}: {expected} but carries no adoption date")
    return errors


def templates_named(ctx: CheckContext) -> Verdict:
    """Check templates: project template owner fields name roles.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per owner field that names no role.
    """
    fields = template_fields(ctx.require_tree())
    return failing(template_problems(fields, role_labels(ctx.corpus)))


def statuses_agree(ctx: CheckContext) -> Verdict:
    """Check status: entries carry their document's status.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per disagreeing entry.
    """
    return failing(status_problems(ctx.corpus.entries))


CHECKS: tuple[Check, ...] = (
    Check(
        "templates",
        FAMILY,
        "Every owner field of a project template names a role",
        ("STND.IDENT.12",),
        templates_named,
    ),
    Check(
        "status",
        FAMILY,
        "Every entry carries its document's status and adoption date",
        ("GOV.41",),
        statuses_agree,
    ),
)
