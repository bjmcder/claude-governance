"""The revision family v.1 to v.11, with checks v.6 to v.8.

v.6 the table of revision classes is present and well formed; v.7 every
provision of the standard names its checks, and every check enforces a
provision; v.8 withdrawn identifiers are listed and never reused, and
every provision identifier the corpus cites is a provision or listed as
withdrawn.
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
from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.text import ids_in
from govharness.derive.references import naming_text

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
# Front-matter fields that hold no citation: the entry's own identifier,
# and the withdrawn identifiers, which v.8 compares with the numbering.
NOT_CITING = ("id", "withdrawn")
CITERS_SHOWN = 3


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
        FAIL on a listed identifier of another document or in use, a
        gap in a document's numbering that is not listed, or a cited
        identifier that is neither a provision nor listed
        (``_unresolved_citations``).
    """
    corpus = ctx.corpus
    problems: list[str] = []
    retired: set[str] = set()
    for doc in documents(corpus):
        did = str(doc.meta["id"])
        listed = [str(w) for w in doc.meta.get("withdrawn") or []]
        patterns = {
            prefix: re.compile(rf"{re.escape(prefix)}\.(\d+)")
            for prefix in numbered_by(doc)
        }
        gone: dict[str, set[int]] = {prefix: set() for prefix in patterns}
        for ident in listed:
            found = next(
                (
                    (prefix, m)
                    for prefix, pattern in patterns.items()
                    if (m := pattern.fullmatch(ident))
                ),
                None,
            )
            if found is None:
                problems.append(f"- {did}: `{ident}` is not its identifier")
                continue
            gone[found[0]].add(int(found[1][1]))
            retired.add(ident)
            if ident in corpus.by_id:
                problems.append(f"- {did}: withdrawn `{ident}` is in use")
        for prefix, pattern in patterns.items():
            numbers = {
                int(m[1])
                for e in corpus.provisions()
                if (m := pattern.fullmatch(str(e.meta["id"])))
            }
            if numbers:
                gaps = set(range(1, max(numbers) + 1))
                gaps -= numbers | gone[prefix]
                problems += [
                    f"- {did}: {prefix}.{n} is missing and not listed as "
                    "withdrawn"
                    for n in sorted(gaps)
                ]
    problems += _unresolved_citations(corpus, retired)
    return Verdict("FAIL" if problems else "PASS", problems)


def numbered_by(doc: Entry) -> list[str]:
    """Return the prefixes by which a document numbers its provisions.

    Parameters
    ----------
    doc : Entry
        A document carrying a revision.

    Returns
    -------
    list[str]
        The parts named in the field ``parts`` for the constitution,
        whose provisions are numbered by part (GOV.37, STND.IDENT.24),
        and the document's own identifier otherwise (STND.IDENT.14).
    """
    if doc.meta.get("kind") == "constitution":
        return [str(part) for part in doc.meta.get("parts") or []]
    return [str(doc.meta["id"])]


def cited_provisions(corpus: Corpus) -> dict[str, set[str]]:
    """Return each numbered identifier the corpus cites, and its citers.

    A body is read as g.25 reads it for bare names (``naming_text``):
    its References section, Revision History, tables with a column
    Example, quoted spans, and code are left out. Every front-matter
    value is read except the entry's own ``id`` and its ``withdrawn``
    list.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    dict[str, set[str]]
        Identifiers such as ``GOV.12``, each with the entries citing it.
    """
    cited: dict[str, set[str]] = {}
    for entry in corpus.entries:
        texts = [naming_text(entry.body)]
        for key, value in entry.meta.items():
            if key in NOT_CITING:
                continue
            values = value if isinstance(value, list) else [value]
            texts += [v for v in values if isinstance(v, str)]
        citer = str(entry.meta["id"])
        for text in texts:
            for ident in ids_in(text):
                cited.setdefault(ident, set()).add(citer)
    return cited


def _unresolved_citations(corpus: Corpus, retired: set[str]) -> list[str]:
    """Return the cited identifiers that name no provision.

    An identifier cited after its provision was deleted, with no entry
    in ``withdrawn``, is a withdrawal the document does not list
    (STND.IDENT.14), even when no gap in the numbering shows it, as for
    the highest number of a document.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    retired : set[str]
        Identifiers that a field ``withdrawn`` lists.

    Returns
    -------
    list[str]
        One line per identifier that is neither an entry of the corpus
        nor listed as withdrawn, with the first entries citing it. An
        identifier whose first mnemonic no entry of the corpus uses
        names an item of another scheme, such as a rule of the C++ Core
        Guidelines (``ES.11``), and is not read.
    """
    mnemonics = {str(e.meta["id"]).split(".")[0] for e in corpus.entries}
    problems = []
    for ident, citers in sorted(cited_provisions(corpus).items()):
        if ident in corpus.by_id or ident in retired:
            continue
        if ident.split(".")[0] not in mnemonics:
            continue
        shown = ", ".join(sorted(citers)[:CITERS_SHOWN])
        more = len(citers) - CITERS_SHOWN
        tail = f" and {more} more" if more > 0 else ""
        problems.append(
            f"- {ident} is cited ({shown}{tail}) but is neither a "
            "provision nor listed as withdrawn"
        )
    return problems


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
        "Withdrawn identifiers are listed and never reused, and every "
        "cited provision exists or is listed as withdrawn",
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
