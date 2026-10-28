"""Structural checks of ``verify``: owner fields and status fields.

templates: every owner field of a project template names a role
(STND.IDENT.12); the corpus view leaves templates out, so they are read
from the file snapshot. status: every entry carries the status of the
document in its directory, and an entry of an adopted or ratified
document carries an adoption date, so that adopting a document cannot
leave its provisions at draft. checked-by: every key in a field
``checked_by`` is ``review`` or the key of a registered check
(STND.HARN.32). onset: every field ``onset`` is well formed, sits on a
waivable provision below LVL0, and names parts that its body holds
(STND.CLASS.10, unit 0023).
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
from govharness.core.onset import onset_problems

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


def check_keys_known(ctx: CheckContext) -> Verdict | None:
    """Check checked-by: every ``checked_by`` key names a check.

    A key that names no registered check claims a check that the
    harness does not make (STND.HARN.32); ``review`` names a reader.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run; ``known_keys`` holds the registered keys.

    Returns
    -------
    Verdict | None
        FAIL with one line per entry and unknown key; ``None`` where the
        context holds no registered keys, as outside ``run_checks``.
    """
    if not ctx.known_keys:
        return None
    known = ctx.known_keys | {"review"}
    return failing(
        [
            f"- {entry.meta['id']}: `{key}` names no check"
            for entry in ctx.corpus.entries
            for key in entry.meta.get("checked_by") or []
            if str(key) not in known
        ]
    )


def onsets_valid(ctx: CheckContext) -> Verdict:
    """Check onset: every field ``onset`` is one the field allows.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per malformed field, per field on an item
        that is not a waivable provision below LVL0, and per named part
        that the body does not hold.
    """
    return failing(
        [
            line
            for entry in ctx.corpus.entries
            for line in onset_problems(entry)
        ]
    )


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
    Check(
        "checked-by",
        FAMILY,
        "Every checked_by key names a registered check or review",
        ("STND.HARN.32",),
        check_keys_known,
    ),
    Check(
        "onset",
        FAMILY,
        "Every onset field is well formed and on a proportioned provision",
        ("STND.CLASS.10",),
        onsets_valid,
    ),
)
