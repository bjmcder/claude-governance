"""Checks v.9 to v.11: identifier forms and the mnemonic register.

v.9 compares the identifier of every item, and every identifier in its
fields, with the form for its kind (STND.IDENT.15), and the slug of
every Lexicon term with its term (STND.IDENT.16). v.10 reads the
mnemonic register MNEM (STND.IDENT.17, STND.IDENT.19), confirms that the
identifier of every item that is not retired uses only active mnemonics
and registered grades (STND.IDENT.22), and lists siblings at a letter
distance of 1 that are not established acronyms (STND.IDENT.18). v.11
confirms that every transaction with the scope MNEM is of type register
and made by the custodians (STND.IDENT.20, STND.IDENT.23).
"""

from __future__ import annotations

import re

from govharness.checks.base import CheckContext, Verdict
from govharness.core.corpus import Corpus
from govharness.core.locators import heading_slug
from govharness.core.tables import read_table

REGISTER_ID = "MNEM"
CONSTITUTION_ID = "LVL0"
REGISTER_HEADER = ("Mnemonic", "Parent", "Names", "Grades", "Form", "Status")
MNEMONIC_RE = re.compile(r"^[A-Z]{2,5}$")
GRADE_RE = re.compile(r"^([A-Z]{2,5})(\d)$")
NUMBER_RE = re.compile(r"^[1-9]\d*$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GRADES_RE = re.compile(r"^(\d) to (\d)$")
REFERENCE_FIELDS = (
    "cites",
    "governed_by",
    "instantiates",
    "refers_to",
    "parent",
    "tags",
    "triggers",
)
STATUSES = {"active", "retired"}
ACRONYM = "Established acronym"
Register = dict[tuple[str, str], dict[str, str]]


def _mnemonics(segments: list[str]) -> bool:
    """Return True when every segment is a mnemonic.

    Parameters
    ----------
    segments : list[str]
        Segments of an identifier.

    Returns
    -------
    bool
        Whether each is two to five uppercase letters.
    """
    return all(MNEMONIC_RE.match(s) for s in segments)


def form_problem(
    ident: str, kind: str | None = None, projects: frozenset[str] = frozenset()
) -> str | None:
    """Return why an identifier or locator breaks STND.IDENT.15, or None.

    Parameters
    ----------
    ident : str
        Identifier, or locator with a number sign.
    kind : str | None
        Kind of the entry the identifier names, when known.
    projects : frozenset[str]
        Mnemonics of the projects in the corpus.

    Returns
    -------
    str | None
        A short reason, or ``None`` when the form is right.
    """
    base, hash_, slug = ident.partition("#")
    if hash_ and not SLUG_RE.match(slug):
        return f"heading slug `{slug}` is not a slug"
    segments = base.split(".")
    head, rest = segments[0], segments[1:]
    if base == CONSTITUTION_ID:
        return None
    if not MNEMONIC_RE.match(head):
        return f"`{head}` is not a mnemonic"
    if head == "LEX" and (rest or kind == "term"):
        ok = len(rest) == 1 and SLUG_RE.match(rest[0])
        return None if ok else "a Lexicon term is LEX and a slug"
    if head in {"TAG", "KNOW"} | projects:
        leaf = SLUG_RE if head == "TAG" else NUMBER_RE
        ok = len(rest) < 2 and _mnemonics(rest)
        ok = ok or (
            len(rest) == 2 and _mnemonics(rest[:1]) and leaf.match(rest[1])
        )
        return None if ok else f"wrong form for an item under {head}"
    if _mnemonics(rest):
        return "a provision needs a number" if kind == "provision" else None
    if _mnemonics(rest[:-1]) and NUMBER_RE.match(rest[-1]):
        return (
            None if kind in {None, "provision"} else f"a {kind} has no number"
        )
    return "a segment is neither a mnemonic nor a number"


def read_register(corpus: Corpus) -> tuple[Register, list[str]]:
    """Return the register rows by (parent, mnemonic), and problems.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    tuple[Register, list[str]]
        Rows keyed by parent and mnemonic, and one line per malformed,
        repeated, or orphaned row.
    """
    entry = corpus.by_id.get(REGISTER_ID)
    if entry is None:
        return {}, [f"- the register {REGISTER_ID} is missing"]
    rows = read_table(entry.body, REGISTER_HEADER)
    register: Register = {}
    problems: list[str] = []
    for row in rows:
        if len(row) != len(REGISTER_HEADER):
            problems.append(f"- a row has {len(row)} cells: `{row}`")
            continue
        mnemonic, parent = row["Mnemonic"], row["Parent"]
        if not MNEMONIC_RE.match(mnemonic):
            problems.append(f"- `{mnemonic}` is not 2 to 5 uppercase letters")
        if row["Status"] not in STATUSES:
            problems.append(f"- `{mnemonic}`: status `{row['Status']}`")
        if row["Grades"] != "none" and not GRADES_RE.match(row["Grades"]):
            problems.append(f"- `{mnemonic}`: grades `{row['Grades']}`")
        if (parent, mnemonic) in register:
            problems.append(f"- `{mnemonic}` appears twice under `{parent}`")
        register[(parent, mnemonic)] = row
    names = {m for _, m in register}
    for parent, mnemonic in register:
        if parent not in {"none", "project"} | names:
            problems.append(f"- `{mnemonic}`: parent `{parent}` is unknown")
    if not rows:
        problems.append(f"- {REGISTER_ID} holds no register table")
    return register, problems


def usage_problems(
    ident: str, register: Register, projects: frozenset[str] = frozenset()
) -> list[str]:
    """Return problems with the mnemonics and grade an identifier uses.

    Parameters
    ----------
    ident : str
        Identifier of an item.
    register : Register
        Register rows.
    projects : frozenset[str]
        Mnemonics of the projects in the corpus.

    Returns
    -------
    list[str]
        A line for an unregistered grade, an unregistered mnemonic, or
        a retired one.
    """
    base = ident.partition("#")[0]
    grade = GRADE_RE.match(base)
    if grade:
        row = register.get(("none", grade[1]))
        span = GRADES_RE.match(row["Grades"]) if row else None
        if not (span and int(span[1]) <= int(grade[2]) <= int(span[2])):
            return [f"- {ident}: `{base}` is not a registered grade"]
        return []
    problems: list[str] = []
    parent = "none"
    for segment in base.split("."):
        if not MNEMONIC_RE.match(segment):
            break  # the leaf
        row = register.get((parent, segment))
        if row is None:
            problems.append(
                f"- {ident}: `{segment}` is not registered under `{parent}`"
            )
            break
        if row["Status"] != "active":
            problems.append(f"- {ident}: `{segment}` is retired")
        if parent == "none" and segment in projects:
            parent = "project"
        else:
            parent = segment
    return problems


def distance(first: str, second: str) -> int:
    """Return the letter (edit) distance between two mnemonics.

    Parameters
    ----------
    first, second : str
        Mnemonics.

    Returns
    -------
    int
        Insertions, deletions, and substitutions needed.
    """
    previous = list(range(len(second) + 1))
    for i, a in enumerate(first, 1):
        current = [i]
        for j, b in enumerate(second, 1):
            current.append(
                min(
                    previous[j] + 1,
                    current[j - 1] + 1,
                    previous[j - 1] + (a != b),
                )
            )
        previous = current
    return previous[-1]


def retired_ids(corpus: Corpus) -> set[str]:
    """Return the identifiers of retired items (STND.IDENT Terms).

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    set[str]
        Entries retired or deprecated, and every withdrawn identifier.
    """
    retired = {
        str(e.meta["id"])
        for e in corpus.entries
        if e.meta.get("status") in {"retired", "deprecated"}
    }
    for entry in corpus.entries:
        retired |= {str(w) for w in entry.meta.get("withdrawn") or []}
    return retired


def _projects(corpus: Corpus) -> frozenset[str]:
    """Return the mnemonics of the projects in the corpus.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    frozenset[str]
        Identifiers of the entries of kind ``project``.
    """
    return frozenset(
        str(e.meta["id"])
        for e in corpus.entries
        if e.meta.get("kind") == "project"
    )


def identifier_forms(ctx: CheckContext) -> Verdict:
    """Check v.9: every identifier and locator has its form.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a malformed identifier or a term slug that differs from
        its term.
    """
    corpus = ctx.corpus
    projects = _projects(corpus)
    form: list[str] = []
    for entry in corpus.entries:
        own = str(entry.meta["id"])
        named = [(own, entry.meta.get("kind"))]
        for field in REFERENCE_FIELDS:
            values = entry.meta.get(field) or []
            if isinstance(values, str):
                values = [values]
            named += [(str(r), None) for r in values]
        for ident, kind in named:
            reason = form_problem(ident, kind, projects)
            if reason:
                form.append(f"- {own}: `{ident}`: {reason}")
    for term in corpus.terms():
        slug = str(term.meta["id"]).partition(".")[2]
        if slug != heading_slug(str(term.meta.get("term", ""))):
            form.append(f"- {term.meta['id']}: slug differs from its term")
    return Verdict("FAIL" if form else "PASS", sorted(set(form)))


def register_usage(ctx: CheckContext) -> Verdict:
    """Check v.10: mnemonics are registered once and active where used.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a register problem or a mnemonic or grade misused;
        INFO listing near siblings otherwise.
    """
    corpus = ctx.corpus
    projects = _projects(corpus)
    register, problems = read_register(corpus)
    retired = retired_ids(corpus)
    for entry in corpus.entries:
        own = str(entry.meta["id"])
        if own not in retired:
            problems += usage_problems(own, register, projects)
    near = sorted(
        f"- `{a}` and `{b}` under `{p}` are at a letter distance of 1"
        for (p, a), first in register.items()
        for (q, b), second in register.items()
        if p == q
        and a < b
        and distance(a, b) < 2
        and ACRONYM not in first["Form"] + second["Form"]
    )
    problems = sorted(set(problems))
    return Verdict(
        "FAIL" if problems else ("INFO" if near else "PASS"),
        problems + near,
    )


def register_changes(ctx: CheckContext) -> Verdict:
    """Check v.11: only the custodians change the register.

    Parameters
    ----------
    ctx : CheckContext
        Context of the run.

    Returns
    -------
    Verdict
        FAIL on a transaction scoped to MNEM that is not a register
        transaction of the custodians; INFO without a ledger.
    """
    if ctx.ledger is None:
        return Verdict("INFO", ["No ledger was supplied."])
    wrong = [
        f"- seq {e.get('seq')}: type `{e.get('type')}`, role "
        f"`{e.get('role')}` changes {REGISTER_ID}"
        for e in ctx.ledger
        if REGISTER_ID in (e.get("scope") or [])
        and (e.get("type") != "register" or e.get("role") != "custodians")
    ]
    return Verdict("FAIL" if wrong else "PASS", wrong)
