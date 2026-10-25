"""Structural checks of ``verify``: identifiers, mnemonics, references.

ids: every entry's ``id`` matches its path. mnemonics: every top-level
directory is a well-formed mnemonic, two to five uppercase letters
(STND.IDENT.17), or a grade of an ordinal scale that the register MNEM
lists, its mnemonic and one digit (GOV.37; LVL0). references: every
identifier or section locator named in ``cites``, ``governed_by``,
``instantiates``, or ``refers_to`` resolves.
"""

from __future__ import annotations

from govharness.checks.base import Check, CheckContext, Verdict
from govharness.checks.revisions.identifiers import (
    GRADE_RE,
    MNEMONIC_RE,
    Register,
    read_register,
    usage_problems,
)
from govharness.core.corpus import Tree
from govharness.core.entry import TEMPLATE_PREFIX, Entry, path_to_id
from govharness.core.locators import heading_slug, reference_resolves

FAMILY = "structure"
REFERENCE_FIELDS = ("cites", "governed_by", "instantiates", "refers_to")


def failing(problems: list[str]) -> Verdict:
    """Return the verdict of a structural check from its problems.

    Parameters
    ----------
    problems : list[str]
        One line per problem.

    Returns
    -------
    Verdict
        FAIL with the problems, or PASS when there are none.
    """
    return Verdict("FAIL" if problems else "PASS", problems)


def id_problems(entries: list[Entry]) -> list[str]:
    """Return the entries whose ``id`` does not match their path.

    Parameters
    ----------
    entries : list[Entry]
        The loaded corpus.

    Returns
    -------
    list[str]
        One line per mismatch.
    """
    return [
        f"id mismatch: {e.path} declares {e.meta.get('id')}"
        for e in entries
        if e.meta.get("id") != path_to_id(e.path)
    ]


def mnemonic_problems(tree: Tree, register: Register) -> list[str]:
    """Return the top-level directories that are not mnemonics.

    Parameters
    ----------
    tree : Tree
        Snapshot of the corpus files.
    register : Register
        Rows of the mnemonic register, from which a grade such as
        ``LVL0`` is read.

    Returns
    -------
    list[str]
        One line per directory name that is neither a mnemonic nor a
        registered grade; templates are skipped.
    """
    problems = []
    for d in tree.directories:
        if len(d.parts) != 1 or d.name.startswith(TEMPLATE_PREFIX):
            continue
        if MNEMONIC_RE.match(d.name):
            continue
        if GRADE_RE.match(d.name) and not usage_problems(d.name, register):
            continue
        problems.append(f"bad mnemonic: {d.name}")
    return problems


def reference_problems(entries: list[Entry]) -> list[str]:
    """Return the cited identifiers and locators that resolve to nothing.

    A bare LVL0 section name, as the Lexicon's governing column uses,
    resolves against the headings of LVL0.

    Parameters
    ----------
    entries : list[Entry]
        The loaded corpus.

    Returns
    -------
    list[str]
        One line per dangling reference.
    """
    known = {e.meta["id"]: e for e in entries}
    errors: list[str] = []
    for entry in entries:
        for field in REFERENCE_FIELDS:
            for ref in entry.meta.get(field) or []:
                if "#" in ref:
                    resolved = reference_resolves(ref, known)
                else:
                    resolved = ref in known or reference_resolves(
                        f"LVL0#{heading_slug(ref)}", known
                    )
                if not resolved:
                    errors.append(
                        f"dangling {field}: {entry.meta['id']} -> {ref}"
                    )
    return errors


def ids_match(ctx: CheckContext) -> Verdict:
    """Check ids: every entry's ``id`` matches its path.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per mismatch.
    """
    return failing(id_problems(ctx.corpus.entries))


def mnemonics_formed(ctx: CheckContext) -> Verdict:
    """Check mnemonics: every top-level directory is a mnemonic.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per bad directory name.
    """
    register, _ = read_register(ctx.corpus)
    return failing(mnemonic_problems(ctx.require_tree(), register))


def references_resolve(ctx: CheckContext) -> Verdict:
    """Check references: every cited identifier or locator resolves.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL with one line per dangling reference.
    """
    return failing(reference_problems(ctx.corpus.entries))


CHECKS: tuple[Check, ...] = (
    Check(
        "ids",
        FAMILY,
        "Every entry's id matches its path",
        ("GOV.37",),
        ids_match,
    ),
    Check(
        "mnemonics",
        FAMILY,
        "Every top-level directory is a well-formed mnemonic",
        ("STND.IDENT.17",),
        mnemonics_formed,
    ),
    Check(
        "references",
        FAMILY,
        "Every cited identifier or section locator resolves",
        ("GOV.37",),
        references_resolve,
    ),
)
