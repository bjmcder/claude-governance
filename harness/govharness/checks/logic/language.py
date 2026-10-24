"""Checks d and e: normative words and the Lexicon.

The drafting standard's own expression lists are checked by the g
family; these checks cover what LVL0 states about its own words.
"""

from __future__ import annotations

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.logic.facts import facts_of
from govharness.core.report import capped

FAMILY = "logic"
NORMATIVE_LANGUAGE = "LVL0#normative-language"


def barred_listed(ctx: CheckContext) -> Verdict:
    """Check d.0: LVL0 names the expressions it bars.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when no barred expression is found, since then d.1 checks
        nothing.
    """
    strict = facts_of(ctx)["excluded"]["strict"]
    return Verdict(
        "PASS" if strict else "FAIL",
        [
            f"Barred by LVL0: {sorted(strict)}",
            "The drafting standard's own tables are checked by the g family.",
        ],
    )


def barred_unused(ctx: CheckContext) -> Verdict:
    """Check d.1: no corpus text uses an expression LVL0 bars.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a use outside quotation marks and tables.
    """
    facts = facts_of(ctx)
    strict = [
        h
        for h in facts["excluded_hits"]
        if h["phrase"] in facts["excluded"]["strict"]
    ]
    fmt = "- {source}: “{phrase}” … {snippet} …".format_map
    return Verdict(
        "FAIL" if strict else "PASS",
        capped([fmt(h) for h in strict]) or ["No occurrences."],
    )


def _uses_of(ctx: CheckContext, key: str) -> Verdict:
    """List the uses of one word in provisions.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.
    key : str
        ``should`` or ``prefer``.

    Returns
    -------
    Verdict
        INFO with one line per use.
    """
    hits = facts_of(ctx)["normative"][key]
    return Verdict(
        "INFO",
        capped([f"- {h['source']}: …{h['snippet']}…" for h in hits])
        or ["None."],
    )


def should_uses(ctx: CheckContext) -> Verdict:
    """Check d.3: list the uses of SHOULD in provisions.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        INFO with one line per use.
    """
    return _uses_of(ctx, "should")


def prefer_uses(ctx: CheckContext) -> Verdict:
    """Check d.4: list the uses of prefer and its forms in provisions.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        INFO with one line per use.
    """
    return _uses_of(ctx, "prefer")


def unused_words(ctx: CheckContext) -> Verdict:
    """Check d.5: list the normative-table words no provision uses.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        INFO with the unused words.
    """
    words = facts_of(ctx)["normative"]["unused_words"]
    return Verdict("INFO", [", ".join(repr(w) for w in words) or "All used."])


def definitions_unforced(ctx: CheckContext) -> Verdict:
    """Check d.6: Lexicon definitions impose no obligation.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        WARN when a definition holds a capitalized normative word.
    """
    stray = facts_of(ctx)["normative"]["term_obligations"]
    return Verdict(
        "WARN" if stray else "PASS",
        [f"- {s['source']}: {s['word']}" for s in stray]
        or ["No capitalized normative word in any definition."],
    )


def terms_complete(ctx: CheckContext) -> Verdict:
    """Check e.1: every term has a name, a group, and a target.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL when a term lacks one of them.
    """
    terms = facts_of(ctx)["terms"]
    return Verdict(
        "FAIL" if terms["incomplete"] else "PASS",
        [
            f"Terms: {terms['count']}; "
            f"incomplete: {terms['incomplete'] or 'none'}"
        ],
    )


def term_targets(ctx: CheckContext) -> Verdict:
    """Check e.2: every ``governed_by`` target exists and is no term.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a bad target.
    """
    bad = facts_of(ctx)["terms"]["bad_targets"]
    return Verdict(
        "FAIL" if bad else "PASS", [f"Bad targets: {bad or 'none'}"]
    )


def terms_unique(ctx: CheckContext) -> Verdict:
    """Check e.3: no term is defined twice.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a duplicate.
    """
    dup = facts_of(ctx)["terms"]["duplicates"]
    return Verdict(
        "FAIL" if dup else "PASS",
        [f"- {k}: {', '.join(v)}" for k, v in dup.items()] or ["None."],
    )


def terms_unused(ctx: CheckContext) -> Verdict:
    """Check e.4: list the terms no provision body uses by name.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        INFO with the unused terms.
    """
    unused = facts_of(ctx)["terms"]["unused"]
    return Verdict(
        "INFO",
        capped([f"- {t}" for t in unused]) or ["All terms used."],
    )


CHECKS: tuple[Check, ...] = (
    Check(
        "d.0",
        FAMILY,
        "Excluded expressions found in the Normative Language",
        (NORMATIVE_LANGUAGE,),
        barred_listed,
    ),
    Check(
        "d.1",
        FAMILY,
        "No corpus text uses an expression LVL0 bars",
        (NORMATIVE_LANGUAGE,),
        barred_unused,
    ),
    Check(
        "d.3",
        FAMILY,
        "Uses of SHOULD in provisions",
        (NORMATIVE_LANGUAGE,),
        should_uses,
    ),
    Check(
        "d.4",
        FAMILY,
        "Uses of prefer* in provisions",
        (NORMATIVE_LANGUAGE,),
        prefer_uses,
    ),
    Check(
        "d.5",
        FAMILY,
        "Normative-table words that no provision body uses",
        (NORMATIVE_LANGUAGE,),
        unused_words,
    ),
    Check(
        "d.6",
        FAMILY,
        "Lexicon definitions impose no obligation (no capitalized "
        "normative word)",
        ("LEX",),
        definitions_unforced,
    ),
    Check(
        "e.1",
        FAMILY,
        "Every Lexicon term has a name, a group, and a governing target",
        ("LEX",),
        terms_complete,
    ),
    Check(
        "e.2",
        FAMILY,
        "Every `governed_by` target exists and is not itself a term",
        ("LEX",),
        term_targets,
    ),
    Check("e.3", FAMILY, "No term is defined twice", ("LEX",), terms_unique),
    Check(
        "e.4",
        FAMILY,
        "Terms no provision body uses by name (inflected forms may escape "
        "the match)",
        ("LEX",),
        terms_unused,
    ),
)
