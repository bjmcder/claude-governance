"""Checks v.1 to v.4: revision numbers, histories, and their ledger.

v.1 every document carries a well-formed revision number; v.2 the major
segment agrees with the document status; v.3 the revision history
agrees with the revision number and steps by the class of each change;
v.4 the ledger holds one transaction per revision, of the right type.
"""

from __future__ import annotations

from typing import Any

from govharness.checks.base import CheckContext, Verdict
from govharness.checks.revisions.classes import (
    ADOPTED,
    PRE_ADOPTION,
    ClassTable,
    History,
    Revision,
    classes_of,
    documents,
    history_of,
    opens_with,
    parse_revision,
    step_class,
)
from govharness.core.entry import Entry
from govharness.ledger.transactions import revision_named


def well_formed(ctx: CheckContext) -> Verdict:
    """Check v.1: every document carries a well-formed revision.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on an absent or malformed revision number.
    """
    form = [
        f"- {doc.meta['id']}: revision `{doc.meta.get('revision')}` is "
        "absent or malformed"
        for doc in documents(ctx.corpus)
        if parse_revision(doc.meta.get("revision")) is None
    ]
    return Verdict("FAIL" if form else "PASS", form)


def major_status(ctx: CheckContext) -> Verdict:
    """Check v.2: the major segment agrees with the document status.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a draft at 1.0 or more, or an adopted document below
        1.0.
    """
    status: list[str] = []
    for doc in documents(ctx.corpus):
        pid = str(doc.meta["id"])
        parsed = parse_revision(doc.meta.get("revision"))
        if parsed is None:
            continue
        state = str(doc.meta.get("status"))
        if state in PRE_ADOPTION and parsed[0] != 0:
            status.append(
                f"- {pid}: {state} but revision is already 1 or more"
            )
        if state in ADOPTED and parsed[0] == 0:
            status.append(f"- {pid}: {state} but revision is below 1.0")
    return Verdict("FAIL" if status else "PASS", status)


def step_problems(
    pid: str,
    label: str,
    previous: Revision | None,
    current: Revision,
    row: dict[str, str],
    classes: ClassTable,
) -> list[str]:
    """Return problems in one history step at or after adoption.

    Parameters
    ----------
    pid : str
        Document identifier.
    label : str
        Revision of the row, as written.
    previous : Revision | None
        Revision of the row above, if any.
    current : Revision
        Revision of this row.
    row : dict[str, str]
        The history row.
    classes : ClassTable
        Revision classes.

    Returns
    -------
    list[str]
        A line when the step is not valid, or the change entry does not
        open with the words of its class.
    """
    if previous is None or previous[0] == 0:
        kind = "adoption" if current == (1, 0, 0) else None
    else:
        kind = step_class(previous, current)
    if kind is None:
        return [f"- {pid}: {label} is not a valid step from the row above"]
    wanted = classes.rows.get(kind)
    if wanted is not None and not opens_with(row["Change"], wanted.openers):
        words = " or ".join(wanted.openers)
        return [f"- {pid}: {label} is a {kind} step; entry must open {words}"]
    return []


def history_problems(
    doc: Entry, rows: History, classes: ClassTable
) -> list[str]:
    """Return problems in one document's revision history.

    Parameters
    ----------
    doc : Entry
        A document carrying a revision.
    rows : History
        Its history rows.
    classes : ClassTable
        Revision classes.

    Returns
    -------
    list[str]
        One line per problem.
    """
    pid = str(doc.meta["id"])
    problems: list[str] = []
    if str(doc.meta.get("status")) in ADOPTED and not rows:
        return [f"- {pid}: adopted but keeps no revision history"]
    previous: Revision | None = None
    for row in rows:
        current = parse_revision(row["Revision"])
        if current is None:
            problems.append(f"- {pid}: history revision `{row['Revision']}`")
            continue
        label = row["Revision"]
        if previous is not None and current <= previous:
            problems.append(f"- {pid}: {label} does not follow the row above")
        elif current[0] >= 1:
            problems += step_problems(
                pid, label, previous, current, row, classes
            )
        previous = current
    last = rows[-1]["Revision"] if rows else ""
    if rows and str(doc.meta.get("revision")) != last:
        problems.append(
            f"- {pid}: revision `{doc.meta.get('revision')}` is not the "
            f"last history row `{last}`"
        )
    return problems


def judged(doc: Entry, rows: History) -> bool:
    """Return True when v.3 and v.4 judge a document's history.

    Parameters
    ----------
    doc : Entry
        A document carrying a revision.
    rows : History
        Its history rows.

    Returns
    -------
    bool
        Whether it keeps a history or is adopted, so must keep one.
    """
    return bool(rows) or str(doc.meta.get("status")) in ADOPTED


def histories_of(ctx: CheckContext) -> dict[str, History]:
    """Return the histories that v.3 and v.4 judge, read once per run.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    dict[str, History]
        History rows by identifier, for documents that keep a history
        or are adopted.
    """
    return ctx.shared(_read_histories)


def _read_histories(ctx: CheckContext) -> dict[str, History]:
    """Read the judged histories of a context's corpus.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    dict[str, History]
        As ``histories_of``.
    """
    found: dict[str, History] = {}
    for doc in documents(ctx.corpus):
        rows = history_of(doc.body)
        if judged(doc, rows):
            found[str(doc.meta["id"])] = rows
    return found


def histories_step(ctx: CheckContext) -> Verdict:
    """Check v.3: histories agree with revisions and step by class.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a problem in a judged history.
    """
    classes = classes_of(ctx)
    problems: list[str] = []
    for doc in documents(ctx.corpus):
        rows = history_of(doc.body)
        if judged(doc, rows):
            problems += history_problems(doc, rows, classes)
    return Verdict("FAIL" if problems else "PASS", problems)


def transaction_problems(
    pid: str,
    row: dict[str, str],
    entry: dict[str, Any],
    classes: ClassTable,
) -> list[str]:
    """Return problems in the transaction type for one revision.

    Parameters
    ----------
    pid : str
        Document identifier.
    row : dict[str, str]
        The history row.
    entry : dict[str, Any]
        The transaction that names the revision.
    classes : ClassTable
        Revision classes.

    Returns
    -------
    list[str]
        A line when the type differs from the class's ledger type.
    """
    wanted = next(
        (
            c
            for c in classes.rows.values()
            if opens_with(row["Change"], c.openers)
        ),
        None,
    )
    if wanted is None or entry.get("type") == wanted.ledger_type:
        return []
    return [
        (
            f"- {pid}: revision {row['Revision']} is a {wanted.name} change; "
            f"transaction {entry['seq']} is `{entry.get('type')}`, not "
            f"`{wanted.ledger_type}`"
        )
    ]


def ledger_problems(
    pid: str,
    rows: History,
    ledger: list[dict[str, Any]],
    classes: ClassTable,
) -> tuple[list[str], list[str]]:
    """Return the failures and date warnings of one document's ledger.

    Parameters
    ----------
    pid : str
        Document identifier.
    rows : History
        Its history rows.
    ledger : list[dict[str, Any]]
        Ledger transactions in order.
    classes : ClassTable
        Revision classes.

    Returns
    -------
    tuple[list[str], list[str]]
        Failures, then dates that differ between a row and its
        transaction.
    """
    mine = [
        e
        for e in ledger
        if e.get("type") in {"adopt", "amend"} and pid in e.get("targets", [])
    ]
    named: dict[str, dict[str, Any]] = {}
    failures: list[str] = []
    for entry in mine:
        number = revision_named(str(entry.get("rationale", "")))
        if number is None:
            failures.append(
                f"- {pid}: transaction {entry.get('seq')} names no revision"
            )
        elif number in named:
            failures.append(f"- {pid}: revision {number} has two transactions")
        else:
            named[number] = entry
    dates: list[str] = []
    listed = {r["Revision"] for r in rows}
    for number, entry in named.items():
        if number not in listed:
            failures.append(
                f"- {pid}: transaction {entry['seq']} names revision "
                f"{number}, which the history lacks"
            )
    previous_seq = 0
    for row in rows:
        entry = named.get(row["Revision"])
        if entry is None:
            failures.append(
                f"- {pid}: revision {row['Revision']} has no transaction"
            )
            continue
        failures += transaction_problems(pid, row, entry, classes)
        if int(entry["seq"]) < previous_seq:
            failures.append(
                f"- {pid}: revision {row['Revision']} is out of ledger order"
            )
        previous_seq = int(entry["seq"])
        if not str(entry.get("at", "")).startswith(row["Date"]):
            dates.append(
                f"- {pid}: revision {row['Revision']} is dated "
                f"{row['Date']}, its transaction {entry.get('at')}"
            )
    return failures, dates


def transactions_recorded(ctx: CheckContext) -> Verdict:
    """Check v.4: one transaction of the right type for each revision.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a missing, doubled, misordered, or mistyped
        transaction; WARN when only dates differ; INFO without a
        ledger.
    """
    if ctx.ledger is None:
        return Verdict("INFO", ["No ledger was supplied."])
    classes = classes_of(ctx)
    failures: list[str] = []
    dates: list[str] = []
    for pid, rows in histories_of(ctx).items():
        more, late = ledger_problems(pid, rows, ctx.ledger, classes)
        failures += more
        dates += late
    status = "FAIL" if failures else ("WARN" if dates else "PASS")
    return Verdict(status, [*failures, *dates])
