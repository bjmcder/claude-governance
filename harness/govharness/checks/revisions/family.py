"""The revision family v.1 to v.11, with checks v.6 to v.8.

v.6 the table of revision classes is present and well formed; v.7 every
provision of the standard names its checks, and every check enforces a
provision; v.8 withdrawn identifiers are listed and never reused.
"""

from __future__ import annotations

import re

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.revisions import adopters, history, identifiers
from govharness.checks.revisions.classes import (
    STANDARD_ID,
    class_problems,
    classes_of,
    documents,
)

FAMILY = "revisions"
# The keys a provision of STND.IDENT may name; v.7 checks the naming
# itself, so it is not among them.
CITABLE_KEYS = (
    "v.1",
    "v.2",
    "v.3",
    "v.4",
    "v.5",
    "v.6",
    "v.8",
    "v.9",
    "v.10",
    "v.11",
)


def classes_formed(ctx: CheckContext) -> Verdict:
    """Check v.6: the table of revision classes is well formed.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a problem in the table.
    """
    problems = class_problems(classes_of(ctx))
    return Verdict(
        "FAIL" if problems else "PASS", [f"- {p}" for p in problems]
    )


def traced(ctx: CheckContext) -> Verdict:
    """Check v.7: provisions and checks refer to each other both ways.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a provision with no or an unknown check, or a check
        that no provision names.
    """
    problems: list[str] = []
    used: set[str] = set()
    prefix = f"{STANDARD_ID}."
    valid = {*CITABLE_KEYS, "review"}
    for pid, entry in sorted(ctx.corpus.by_id.items()):
        if not pid.startswith(prefix) or entry.meta.get("kind") != "provision":
            continue
        listed = entry.meta.get("checked_by") or []
        if not listed:
            problems.append(f"- {pid}: no `checked_by`")
        for key in listed:
            used.add(key)
            if key not in valid:
                problems.append(f"- {pid}: unknown check {key}")
    problems += [
        f"- check {key} enforces no provision"
        for key in CITABLE_KEYS
        if key not in used
    ]
    return Verdict("FAIL" if problems else "PASS", problems)


def withdrawn(ctx: CheckContext) -> Verdict:
    """Check v.8: withdrawn identifiers are listed and never reused.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a listed identifier of another document or in use, or
        a gap in a document's numbering that is not listed.
    """
    corpus = ctx.corpus
    problems: list[str] = []
    for doc in documents(corpus):
        did = str(doc.meta["id"])
        listed = [str(w) for w in doc.meta.get("withdrawn") or []]
        pattern = re.compile(rf"{re.escape(did)}\.(\d+)")
        gone: set[int] = set()
        for ident in listed:
            found = pattern.fullmatch(ident)
            if found is None:
                problems.append(f"- {did}: `{ident}` is not its identifier")
                continue
            gone.add(int(found[1]))
            if ident in corpus.by_id:
                problems.append(f"- {did}: withdrawn `{ident}` is in use")
        numbers = {
            int(m[1])
            for e in corpus.provisions()
            if (m := pattern.fullmatch(str(e.meta["id"])))
        }
        if numbers:
            gaps = set(range(1, max(numbers) + 1)) - numbers - gone
            problems += [
                f"- {did}: {did}.{n} is missing and not listed as withdrawn"
                for n in sorted(gaps)
            ]
    return Verdict("FAIL" if problems else "PASS", problems)


IDENT = (STANDARD_ID,)
CHECKS: tuple[Check, ...] = (
    Check(
        "v.1",
        FAMILY,
        "Every document carries a well-formed revision number",
        IDENT,
        history.well_formed,
    ),
    Check(
        "v.2",
        FAMILY,
        "The major segment agrees with the document status",
        IDENT,
        history.major_status,
    ),
    Check(
        "v.3",
        FAMILY,
        "The revision history agrees with the revision number and steps "
        "by the class of each change",
        IDENT,
        history.histories_step,
    ),
    Check(
        "v.4",
        FAMILY,
        "The ledger holds one transaction per revision, of the right type",
        IDENT,
        history.transactions_recorded,
    ),
    Check(
        "v.5",
        FAMILY,
        "Adopter fields name a role that the Lexicon defines",
        IDENT,
        adopters.adopters_named,
    ),
    Check(
        "v.6",
        FAMILY,
        "The table of revision classes is present and well formed",
        IDENT,
        classes_formed,
    ),
    Check(
        "v.7",
        FAMILY,
        "Every revision provision names its checks and every check "
        "enforces a provision",
        IDENT,
        traced,
    ),
    Check(
        "v.8",
        FAMILY,
        "Withdrawn identifiers are listed and never reused",
        ("STND.IDENT.14",),
        withdrawn,
    ),
    Check(
        "v.9",
        FAMILY,
        "Every identifier and locator has the form of STND.IDENT.15",
        ("STND.IDENT.15", "STND.IDENT.16"),
        identifiers.identifier_forms,
    ),
    Check(
        "v.10",
        FAMILY,
        "Mnemonics are well formed, registered once, and active where used",
        ("STND.IDENT.17", "STND.IDENT.18", "STND.IDENT.19", "STND.IDENT.22"),
        identifiers.register_usage,
    ),
    Check(
        "v.11",
        FAMILY,
        "Only the custodians change the register, by register transactions",
        ("STND.IDENT.20", "STND.IDENT.23"),
        identifiers.register_changes,
    ),
)
