"""Profile combination: selector tables, shared matters, and review pairs.

The readers serve checks m.1 and m.2 (STND.HARN.26, STND.HARN.27) and
the ``pairs`` command (STND.HARN.28). They read the tables that
STND.DRAFT.35 and STND.DRAFT.39 name, by the ``defines`` field of the
provision that holds each and by its column headings, never by
position. Nothing here reads a file: every function takes the corpus.
"""

from __future__ import annotations

from dataclasses import dataclass

from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.tables import read_table, section_text
from govharness.core.text import ids_in, normalise_term

SELECTOR = "selector"
SELECTOR_HEADER = ("Attribute", "Defined by")
SHARED = "shared-matters"
SHARED_HEADER = ("Matter", "Owning profile", "Provisions")
TERMS_HEADER = ("Term", "Definition")
PROFILE_KINDS = ("profile", "sub-profile")
IN_FORCE = ("adopted", "ratified")
# LVL0 parts whose common instantiation does not make a pair
# (STND.HARN.28): GOV and the Governing Principles.
UNPAIRED_PARTS = ("GOV", "PRIN")


@dataclass(frozen=True)
class SelectorRow:
    """One row of a selector table.

    Parameters
    ----------
    document : str
        Identifier of the profile or sub-profile that holds the table.
    provision : str
        Identifier of the provision that holds it.
    attribute : str
        The attribute the selector tests.
    defined_by : str
        Identifier of the document that defines the attribute.
    """

    document: str
    provision: str
    attribute: str
    defined_by: str


@dataclass(frozen=True)
class MatterRow:
    """One row of a shared-matters table.

    Parameters
    ----------
    document : str
        Identifier of the document that holds the table.
    provision : str
        Identifier of the provision that holds it.
    matter : str
        Name of the shared matter.
    owner : str
        Identifier of the owning profile.
    provisions : tuple[str, ...]
        Provisions the row gives for the matter.
    """

    document: str
    provision: str
    matter: str
    owner: str
    provisions: tuple[str, ...]


@dataclass(frozen=True)
class Pair:
    """One pair of provisions listed for review (STND.HARN.28).

    Parameters
    ----------
    first : str
        Provision of the changed side.
    second : str
        Provision of another document, which may also lie on the
        changed side.
    bases : tuple[str, ...]
        Why the pair is listed: ``matter: NAME`` for a shared matter,
        or a LVL0 identifier both instantiate where the other provision
        lies in a document that the change touches.
    """

    first: str
    second: str
    bases: tuple[str, ...]


def document_id(corpus: Corpus, entry: Entry) -> str:
    """Return the identifier of the document an entry belongs to.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    entry : Entry
        Any entry.

    Returns
    -------
    str
        The identifier of the ``_doc.md`` in its directory, or of the
        entry itself when the directory has none.
    """
    doc = corpus.document_of(entry)
    return str((doc or entry).meta["id"])


def in_force(entry: Entry | None) -> bool:
    """Return True when an entry is adopted or ratified.

    Parameters
    ----------
    entry : Entry | None
        A document or provision.

    Returns
    -------
    bool
        Whether its status is in force.
    """
    return entry is not None and entry.meta.get("status") in IN_FORCE


def is_profile(corpus: Corpus, ident: str) -> bool:
    """Return True when an identifier names a profile or sub-profile.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    ident : str
        Identifier of a document.

    Returns
    -------
    bool
        Whether the document's kind is profile or sub-profile.
    """
    entry = corpus.by_id.get(ident)
    return entry is not None and entry.meta.get("kind") in PROFILE_KINDS


def _defining(corpus: Corpus, name: str) -> list[Entry]:
    """Return the provisions whose ``defines`` field names a table.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    name : str
        Table name.

    Returns
    -------
    list[Entry]
        Provisions in path order.
    """
    return [
        p for p in corpus.provisions() if name in (p.meta.get("defines") or [])
    ]


def selector_rows(
    corpus: Corpus, adopted_only: bool = True
) -> list[SelectorRow]:
    """Return the rows of every selector table of a profile.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    adopted_only : bool
        Keep only tables of profiles and sub-profiles in force.

    Returns
    -------
    list[SelectorRow]
        Rows in path order of their provisions.
    """
    rows: list[SelectorRow] = []
    for prov in _defining(corpus, SELECTOR):
        did = document_id(corpus, prov)
        if not is_profile(corpus, did):
            continue
        if adopted_only and not in_force(corpus.by_id.get(did)):
            continue
        for row in read_table(prov.body, SELECTOR_HEADER):
            rows.append(
                SelectorRow(
                    did,
                    str(prov.meta["id"]),
                    row.get("Attribute", "").strip(),
                    row.get("Defined by", "").strip(),
                )
            )
    return rows


def defined_terms(corpus: Corpus, ident: str) -> set[str]:
    """Return the normalised terms of a document's Terms section.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    ident : str
        Identifier of a document.

    Returns
    -------
    set[str]
        Terms of the table under its ``Terms`` heading; empty when it
        has none.
    """
    text = section_text(corpus.body(ident), "Terms") or ""
    return {
        normalise_term(r.get("Term", ""))
        for r in read_table(text, TERMS_HEADER)
    }


def matter_rows(corpus: Corpus, adopted_only: bool = True) -> list[MatterRow]:
    """Return the rows of every shared-matters table.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    adopted_only : bool
        Keep only tables of documents in force.

    Returns
    -------
    list[MatterRow]
        Rows in path order of their provisions.
    """
    rows: list[MatterRow] = []
    for prov in _defining(corpus, SHARED):
        did = document_id(corpus, prov)
        if adopted_only and not in_force(corpus.by_id.get(did)):
            continue
        for row in read_table(prov.body, SHARED_HEADER):
            rows.append(
                MatterRow(
                    did,
                    str(prov.meta["id"]),
                    row.get("Matter", "").strip(),
                    row.get("Owning profile", "").strip(),
                    tuple(ids_in(row.get("Provisions", ""))),
                )
            )
    return rows


def matter_key(name: str) -> str:
    """Return the comparison key of a matter's name.

    Parameters
    ----------
    name : str
        Matter as a table gives it.

    Returns
    -------
    str
        Lower case with single spaces.
    """
    return " ".join(name.lower().split())


def cited(entry: Entry) -> set[str]:
    """Return the identifiers a provision instantiates or refers to.

    Parameters
    ----------
    entry : Entry
        A provision.

    Returns
    -------
    set[str]
        Its ``instantiates`` and ``refers_to`` values.
    """
    return {
        str(x)
        for x in [
            *(entry.meta.get("instantiates") or []),
            *(entry.meta.get("refers_to") or []),
        ]
    }


def lvl0_bases(corpus: Corpus, entry: Entry) -> set[str]:
    """Return the LVL0 provisions outside GOV and PRIN a provision
    instantiates.

    Parameters
    ----------
    corpus : Corpus
        The corpus.
    entry : Entry
        A provision.

    Returns
    -------
    set[str]
        Identifiers of LVL0 provisions in its ``instantiates`` field.
    """
    found: set[str] = set()
    for ref in entry.meta.get("instantiates") or []:
        target = corpus.by_id.get(str(ref))
        if target is None or target.meta.get("level") != "LVL0":
            continue
        if target.meta.get("kind") != "provision":
            continue
        if str(ref).split(".")[0] in UNPAIRED_PARTS:
            continue
        found.add(str(ref))
    return found


def review_pairs(
    corpus: Corpus,
    changed: str | tuple[str, ...],
    amends: tuple[str, ...] = (),
) -> list[Pair]:
    """Return the pairs STND.HARN.28 lists before a change.

    The changed side holds the provisions that the change adopts or
    amends: each provision of a document named whole, each provision
    named, and every provision below LVL0 that instantiates a LVL0
    provision the change amends. The other side holds the provisions
    below LVL0 of every document in force or touched by the change. A
    pair joins provisions of two documents, at least one of them a
    profile or sub-profile, and is listed on a shared matter when a
    shared-matters table gives both for one matter, and on a common
    instantiation when the other provision lies in a document that the
    change touches, a document named whole or the document of a
    provision named, and both instantiate one LVL0 provision outside GOV
    and the Governing Principles. A change of LVL0 alone touches no
    document below LVL0, so its pairs rest on shared matters.

    Parameters
    ----------
    corpus : Corpus
        The corpus, holding each changed document at its new text.
    changed : str | tuple[str, ...]
        Identifier of the changed document, or of each document or
        provision that one change adopts or amends. A provision's
        identifier puts that provision alone on the changed side, and
        its document among those that the change touches, for a change
        that amends some provisions of a document and not the others.
    amends : tuple[str, ...]
        LVL0 provisions the change amends, for a change of LVL0.

    Returns
    -------
    list[Pair]
        Pairs sorted by their two identifiers.
    """
    named = {changed} if isinstance(changed, str) else set(changed)
    lower = [
        p
        for p in corpus.provisions()
        if p.meta.get("level") not in (None, "LVL0")
    ]
    doc_of = {str(p.meta["id"]): document_id(corpus, p) for p in lower}
    by_id = {str(p.meta["id"]): p for p in lower}
    provisions = named & set(by_id)
    docs = (named - provisions) | {doc_of[pid] for pid in provisions}
    amended = set(amends)
    side = {
        pid
        for pid, p in by_id.items()
        if pid in provisions
        or doc_of[pid] in named
        or amended & {str(x) for x in p.meta.get("instantiates") or []}
    }
    others = {
        pid
        for pid in by_id
        if in_force(corpus.by_id.get(doc_of[pid])) or doc_of[pid] in docs
    }
    matters: dict[str, set[str]] = {}
    for row in matter_rows(corpus, adopted_only=False):
        if in_force(corpus.by_id.get(row.document)) or row.document in docs:
            matters.setdefault(matter_key(row.matter), set()).update(
                row.provisions
            )
    bases = {pid: lvl0_bases(corpus, by_id[pid]) for pid in by_id}
    found: dict[tuple[str, str], set[str]] = {}
    for first in sorted(side):
        for second in sorted(others):
            if doc_of[first] == doc_of[second]:
                continue
            if not (
                is_profile(corpus, doc_of[first])
                or is_profile(corpus, doc_of[second])
            ):
                continue
            why = {
                f"matter: {name}"
                for name, members in matters.items()
                if first in members and second in members
            }
            if doc_of[second] in docs:
                why |= bases[first] & bases[second]
            if why:
                key = (
                    (min(first, second), max(first, second))
                    if second in side
                    else (first, second)
                )
                found.setdefault(key, set()).update(why)
    return [
        Pair(a, b, tuple(sorted(why))) for (a, b), why in sorted(found.items())
    ]
