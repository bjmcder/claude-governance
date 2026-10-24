"""The drafting checks g.0 to g.25 and their severity model.

A finding in a draft or in LVL0 is listed (INFO). In the standard itself
a defect fails and a review finding warns. In another provision below
LVL0 a defect fails when the standard is adopted and a binding provision
names the check, and warns otherwise; a review finding is listed. g.23
checks that provisions and checks name each other, and g.24 tallies the
advisory punch list.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.drafting import (
    citations,
    expressions,
    modals,
    roles,
    style,
)
from govharness.checks.drafting.context import (
    STANDARD_ID,
    DraftingContext,
    Finding,
    drafting_context,
)
from govharness.checks.drafting.tables import TABLE_SPECS
from govharness.core.report import capped

FAMILY = "drafting"
ORDER = {"FAIL": 3, "WARN": 2, "INFO": 1, "PASS": 0}
ADVISORY = {"draft", "lvl0"}
DETAIL_CAP = 15
Finder = Callable[[DraftingContext], list[Finding]]
Findings = dict[str, list[Finding]]

FINDERS: tuple[tuple[str, str, Finder], ...] = (
    (
        "g.1",
        "The standard's tables are present, well formed, and tied to "
        "Normative Language",
        modals.tables_tied,
    ),
    (
        "g.2",
        "Every Normative Language form of force is a modal or an "
        "excluded expression",
        modals.forms_covered,
    ),
    ("g.3", "Modals are written in capital letters", modals.capitals),
    (
        "g.4",
        "Each sentence has at most one modal, and each provision "
        "imposes something",
        modals.one_modal,
    ),
    (
        "g.5",
        "No provision uses an excluded expression of class exact",
        expressions.excluded_exact,
    ),
    (
        "g.6",
        "Excluded expressions of class review (substitution test)",
        expressions.excluded_review,
    ),
    (
        "g.7",
        "No sentence outside a numbered provision carries a modal",
        modals.outside_provisions,
    ),
    ("g.8", "Sentences that look imperative", modals.imperatives),
    (
        "g.9",
        "Rationale and examples stay out of provision bodies",
        expressions.informative_markers,
    ),
    ("g.10", "Vague qualifiers", expressions.qualifiers),
    ("g.11", "Negated modals over lists", expressions.negated_lists),
    (
        "g.12",
        "Conditions precede the clause; one per sentence",
        expressions.conditions,
    ),
    ("g.13", "Quantifier words", expressions.quantifiers),
    ("g.14", "Numeric limits (unit and inclusive bound)", expressions.numbers),
    (
        "g.15",
        "Citation form: no ranges, positions, or bare numbers",
        citations.citation_form,
    ),
    (
        "g.16",
        "Identifiers in the text equal the listed ones",
        citations.listed_identifiers,
    ),
    ("g.17", "Titles are short noun phrases and distinct", roles.titles),
    (
        "g.18",
        "Atomicity: at most three modals per provision",
        modals.atomicity,
    ),
    (
        "g.19",
        "Role words: retired absent, undefined flagged",
        roles.role_words,
    ),
    (
        "g.20",
        "Terms are defined once and never redefine the Lexicon",
        roles.defined_terms,
    ),
    ("g.21", "Third person and no contractions", style.person),
    ("g.22", "American spelling", style.spelling),
    (
        "g.25",
        "Each document lists the documents it cites",
        citations.references_listed,
    ),
)


def all_findings(ctx: CheckContext) -> Findings:
    """Return the findings of every drafting check, computed once.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Findings
        Findings by check key; empty when the corpus has no drafting
        standard.
    """
    return ctx.shared(_find_all)


def _find_all(ctx: CheckContext) -> Findings:
    """Run every finder over a run's drafting context.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Findings
        Findings by check key, in finder order.
    """
    drafting = drafting_context(ctx)
    if drafting is None:
        return {}
    return {key: find(drafting) for key, _, find in FINDERS}


def binding_keys(drafting: DraftingContext) -> set[str]:
    """Return the check keys that at least one binding provision names.

    Parameters
    ----------
    drafting : DraftingContext
        Drafting context.

    Returns
    -------
    set[str]
        Keys from ``checked_by`` of the standard's binding provisions.
    """
    return {
        key
        for rule in drafting.rules
        if rule.meta.get("mode") == "binding"
        for key in rule.meta.get("checked_by") or []
    }


def severity(
    drafting: DraftingContext, finding: Finding, binding: bool
) -> str:
    """Map a finding to a result status under the severity model.

    Parameters
    ----------
    drafting : DraftingContext
        Drafting context.
    finding : Finding
        One finding.
    binding : bool
        Whether a binding provision names the check.

    Returns
    -------
    str
        ``FAIL``, ``WARN``, or ``INFO``.
    """
    if finding.group in ADVISORY:
        return "INFO"
    if finding.group == "self":
        return "FAIL" if finding.cls == "defect" else "WARN"
    if finding.cls != "defect":
        return "INFO"
    return "FAIL" if drafting.adopted and binding else "WARN"


def _judge(ctx: CheckContext, key: str) -> Verdict | None:
    """Judge the findings of one drafting check.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.
    key : str
        Check key.

    Returns
    -------
    Verdict | None
        The worst status of its findings, the findings that are not
        merely listed, and a count by group; ``None`` when the corpus
        has no drafting standard.
    """
    drafting = drafting_context(ctx)
    if drafting is None:
        return None
    items = all_findings(ctx)[key]
    binding = key in binding_keys(drafting)
    statuses = [severity(drafting, f, binding) for f in items]
    status = max(statuses, key=ORDER.__getitem__, default="PASS")
    shown = sorted(
        zip(statuses, items, strict=True),
        key=lambda p: (-ORDER[p[0]], p[1].group, p[1].subject),
    )
    details = [
        f"- {s} {f.group} {f.subject} [{f.cls}]: {f.text}"
        for s, f in shown
        if s != "INFO" or f.group in {"lower"}
    ]
    counts = Counter(f.group for f in items)
    details.append(
        "Findings by group: "
        + (", ".join(f"{g} {n}" for g, n in sorted(counts.items())) or "none")
    )
    return Verdict(status, capped(details, DETAIL_CAP))


def standard_present(ctx: CheckContext) -> Verdict | None:
    """Check g.0: report that the drafting checks are skipped.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict | None
        INFO when the corpus holds no drafting standard; ``None``
        otherwise, when the other drafting checks report.
    """
    if drafting_context(ctx) is not None:
        return None
    return Verdict(
        "INFO",
        [f"No {STANDARD_ID} in the corpus; the drafting checks are skipped."],
    )


def traceability(ctx: CheckContext) -> Verdict | None:
    """Check g.23: provisions and checks name each other both ways.

    A key counts as known when a registered check has it, whether or
    not this run includes that check's family.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict | None
        FAIL on a provision with no or an unknown check, a drafting
        check that no provision names, or an undefined table; ``None``
        when the corpus has no drafting standard.
    """
    drafting = drafting_context(ctx)
    if drafting is None:
        return None
    keys = ctx.known_keys | {"review"}
    used: set[str] = set()
    problems = []
    for rule in drafting.rules:
        listed = rule.meta.get("checked_by") or []
        if not listed:
            problems.append(f"- {rule.meta['id']}: no `checked_by`")
        for key in listed:
            used.add(key)
            if key not in keys:
                problems.append(f"- {rule.meta['id']}: unknown check {key}")
    unused = [k for k, _, _ in FINDERS if k not in used]
    problems += [f"- check {k} enforces no provision" for k in unused]
    unknown = [n for n in TABLE_SPECS if n not in drafting.tables.tables]
    problems += [f"- table `{n}` is not defined" for n in unknown]
    reviewed = [
        str(r.meta["id"])
        for r in drafting.rules
        if "review" in (r.meta.get("checked_by") or [])
    ]
    return Verdict(
        "FAIL" if problems else "PASS",
        [*problems, f"Provisions a reader checks: {', '.join(reviewed)}"],
    )


def punch_table(ctx: CheckContext) -> Verdict | None:
    """Check g.24: tally the advisory findings of drafts and LVL0.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict | None
        INFO with a table of counts per draft and for LVL0; ``None``
        when the corpus has no drafting standard.
    """
    if drafting_context(ctx) is None:
        return None
    table: dict[tuple[str, str], Counter[str]] = {}
    for key, items in all_findings(ctx).items():
        for f in items:
            if f.group in ADVISORY:
                table.setdefault((f.group, f.subject), Counter())[key] += 1
    keys = [k for k, _, _ in FINDERS]
    lines = ["| Group | Subject | " + " | ".join(keys) + " |"]
    lines.append("| --- | --- | " + " | ".join("---" for _ in keys) + " |")
    drafts = sorted(k for k in table if k[0] == "draft")
    lvl0: Counter[str] = Counter()
    for (group, _), counts in table.items():
        if group == "lvl0":
            lvl0.update(counts)
    for group, subject in drafts:
        counts = table[(group, subject)]
        lines.append(
            f"| draft | {subject} | "
            + " | ".join(str(counts.get(k, "")) for k in keys)
            + " |"
        )
    lines.append(
        "| lvl0 | all provisions | "
        + " | ".join(str(lvl0.get(k, "")) for k in keys)
        + " |"
    )
    return Verdict("INFO", lines)


def punch_list(findings: Findings) -> str:
    """Render the drafting findings that never fail as a Markdown list.

    Parameters
    ----------
    findings : Findings
        Findings by check key, from ``all_findings``.

    Returns
    -------
    str
        The punch list of drafts and LVL0.
    """
    lines = ["# Drafting punch list", ""]
    lines.append(
        "Findings in drafts not yet divided into numbered provisions and "
        "in LVL0 (to which the drafting standard does not apply)."
    )
    for key, items in findings.items():
        rows = [f for f in items if f.group in ADVISORY]
        if not rows:
            continue
        lines += ["", f"## {key}", ""]
        lines += [f"- {f.group} {f.subject} [{f.cls}]: {f.text}" for f in rows]
    return "\n".join(lines) + "\n"


def _finder_check(key: str, title: str) -> Check:
    """Return the registered check that judges one finder's findings.

    Parameters
    ----------
    key : str
        Check key.
    title : str
        Check title.

    Returns
    -------
    Check
        The registered value.
    """
    return Check(
        key, FAMILY, title, (STANDARD_ID,), lambda ctx: _judge(ctx, key)
    )


# g.23 and g.24 follow the finders, as the report has always shown them.
CHECKS: tuple[Check, ...] = (
    Check(
        "g.0",
        FAMILY,
        "The corpus holds a drafting standard",
        (STANDARD_ID,),
        standard_present,
    ),
    *(_finder_check(key, title) for key, title, _ in FINDERS),
    Check(
        "g.23",
        FAMILY,
        "Every provision names its checks and every check enforces a "
        "provision",
        (STANDARD_ID,),
        traceability,
    ),
    Check(
        "g.24",
        FAMILY,
        "Advisory punch list: drafts and LVL0 against the drafting standard",
        (STANDARD_ID,),
        punch_table,
    ),
)
