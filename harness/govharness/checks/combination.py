"""Checks m.1 and m.2: how profiles combine (STND.HARN.26, STND.HARN.27).

m.1 fails on an attribute of an adopted selector table that the
document its Defined by column names does not define in its Terms
section. m.2 fails on a shared matter with more than one owning
profile, on a row naming a matter that another profile owns whose
provision cites no provision of that owner, and on a row giving a
provision that does not exist. Both read only documents in force.
"""

from __future__ import annotations

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.core.report import capped
from govharness.core.text import normalise_term
from govharness.query.combination import (
    cited,
    defined_terms,
    matter_key,
    matter_rows,
    selector_rows,
)

FAMILY = "combination"


def selectors_defined(ctx: CheckContext) -> Verdict | None:
    """Check m.1: each selector attribute is defined where its table says.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict | None
        FAIL on an undefined attribute; ``None`` when no profile in
        force holds a selector table.
    """
    rows = selector_rows(ctx.corpus)
    if not rows:
        return None
    problems = []
    for row in rows:
        if row.defined_by not in ctx.corpus.by_id:
            problems.append(
                f"- {row.provision}: `{row.attribute}` names unknown "
                f"document `{row.defined_by}`"
            )
        elif normalise_term(row.attribute) not in defined_terms(
            ctx.corpus, row.defined_by
        ):
            problems.append(
                f"- {row.provision}: `{row.attribute}` is not defined in "
                f"the Terms of {row.defined_by}"
            )
    return Verdict(
        "FAIL" if problems else "PASS",
        capped(problems) or [f"{len(rows)} selector attribute(s) defined."],
    )


def matters_owned(ctx: CheckContext) -> Verdict | None:
    """Check m.2: one owner per shared matter, cited where built on.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict | None
        FAIL on a matter with two owners, an uncited owner, or an
        unknown provision; ``None`` when no document in force holds a
        shared-matters table.
    """
    rows = matter_rows(ctx.corpus)
    if not rows:
        return None
    problems: list[str] = []
    owners: dict[str, set[str]] = {}
    for row in rows:
        owners.setdefault(matter_key(row.matter), set()).add(row.owner)
    problems += [
        f"- shared matter `{name}` has owners {', '.join(sorted(found))}"
        for name, found in sorted(owners.items())
        if len(found) > 1
    ]
    prefix_of = {row.owner: f"{row.owner}." for row in rows}
    for row in rows:
        for pid in row.provisions:
            entry = ctx.corpus.by_id.get(pid)
            if entry is None:
                problems.append(f"- {row.provision}: `{pid}` does not exist")
                continue
            if row.owner == row.document:
                continue
            prefix = prefix_of[row.owner]
            if not any(
                ref.startswith(prefix) and ref.count(".") == prefix.count(".")
                for ref in cited(entry)
            ):
                problems.append(
                    f"- {pid}: addresses `{row.matter}`, owned by "
                    f"{row.owner}, and cites no provision of it"
                )
    return Verdict(
        "FAIL" if problems else "PASS",
        capped(problems)
        or [f"{len(owners)} shared matter(s), one owner each."],
    )


CHECKS = (
    Check(
        "m.1",
        FAMILY,
        "Selector attributes are defined where their tables say",
        ("STND.HARN.26", "STND.DRAFT.35"),
        selectors_defined,
    ),
    Check(
        "m.2",
        FAMILY,
        "Each shared matter has one owner, cited where built on",
        ("STND.HARN.27", "STND.DRAFT.39"),
        matters_owned,
    ),
)
