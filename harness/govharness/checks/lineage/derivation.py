"""Derive rank, waivability, and binding status of provisions below LVL0.

A provision below LVL0 declares what it instantiates in the front-matter
field ``instantiates`` (identifiers or section locators) and what it
only mentions in ``refers_to``. The closure of ``instantiates`` reaches
LVL0. From that closure this module derives:

* the rank, which is the highest rank among the LVL0 provisions reached
  (GOV.5, GOV.17);
* the waivability, which is waivable only when every LVL0 node reached
  is waivable (GOV.17, GOV.45); a section, document, or Lexicon term is
  not waivable;
* whether the binding mark is forced (a prime directive, a GUARD
  provision, or a floor obligation is reached; GOV.19). GOV.10 names
  the prime directives, GUARD, and GOV as part of the floor, so a
  provision of any of the three forces the mark.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from govharness.core.corpus import Corpus
from govharness.core.entry import Entry
from govharness.core.locators import reference_resolves

LEVEL_ORDER = {"LVL0": 0, "LVL1": 1, "LVL2": 2, "LVL3": 3}
# GOV.10 places the prime directives, GUARD, and GOV in the floor; this
# part list is the one hand-kept list, because GOV.10 names parts.
FORCING_PARTS = {"PRIME", "GUARD", "GOV"}
Node = tuple[int | None, bool, bool, bool]


@dataclass
class Derived:
    """What the closure of ``instantiates`` implies for one provision.

    Parameters
    ----------
    lvl0 : list[str]
        LVL0 references reached, in discovery order.
    rank : int | None
        Highest authority (lowest number) among the LVL0 provisions
        reached, or ``None`` when none carries a rank.
    waivable : bool
        True only when every LVL0 node reached is waivable.
    forced : bool
        True when a prime directive, a GUARD provision, a GOV provision,
        or a floor obligation is reached.
    primes : bool
        True when a prime directive is reached.
    cycle : bool
        True when the closure revisits a provision.
    unresolved : list[str]
        References that resolve to nothing.
    direct_lvl0 : bool
        True when the provision itself lists a LVL0 reference.
    """

    lvl0: list[str] = field(default_factory=list)
    rank: int | None = None
    waivable: bool = False
    forced: bool = False
    primes: bool = False
    cycle: bool = False
    unresolved: list[str] = field(default_factory=list)
    direct_lvl0: bool = False


def level_of(corpus: Corpus, ref: str) -> str | None:
    """Return the level of the entry a reference names.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    ref : str
        Identifier or locator.

    Returns
    -------
    str | None
        The entry's ``level`` as text, or ``None`` when the reference
        names no entry.
    """
    entry = corpus.by_id.get(ref.partition("#")[0])
    return str(entry.meta.get("level")) if entry else None


def references(entry: Entry) -> list[str]:
    """Return the ``instantiates`` then the ``refers_to`` of an entry.

    Parameters
    ----------
    entry : Entry
        Any entry.

    Returns
    -------
    list[str]
        The references, in field order.
    """
    return [
        *(entry.meta.get("instantiates") or []),
        *(entry.meta.get("refers_to") or []),
    ]


def _lvl0_node(corpus: Corpus, ref: str, floor_ids: set[str]) -> Node:
    """Return (rank, waivable, forcing, prime) for a LVL0 reference.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    ref : str
        Identifier or locator of a LVL0 node.
    floor_ids : set[str]
        Floor obligations (GOV.10).

    Returns
    -------
    Node
        What the node contributes; a locator contributes nothing.
    """
    entry = corpus.by_id.get(ref.partition("#")[0])
    if entry is None or "#" in ref:
        return None, False, False, False
    rank = entry.meta.get("rank")
    waivable = bool(entry.meta.get("waivable", False))
    part = ref.split(".")[0]
    forcing = part in FORCING_PARTS or ref in floor_ids
    return (
        rank if isinstance(rank, int) else None,
        waivable,
        forcing,
        part == "PRIME",
    )


def derive(
    corpus: Corpus,
    entry: Entry,
    floor_ids: set[str],
    _stack: tuple[str, ...] = (),
) -> Derived:
    """Derive rank, waivability, and forcing for one lower entry.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    entry : Entry
        A provision or document below LVL0.
    floor_ids : set[str]
        Floor obligations (GOV.10).
    _stack : tuple[str, ...]
        Identifiers on the path so far, to stop at a cycle.

    Returns
    -------
    Derived
        The derived values; ``waivable`` is False when nothing resolves.
    """
    own = str(entry.meta["id"])
    result = Derived()
    if own in _stack:
        result.cycle = True
        return result
    nodes: list[Node] = []
    for ref in entry.meta.get("instantiates") or []:
        if not reference_resolves(ref, corpus.by_id):
            result.unresolved.append(ref)
            continue
        if level_of(corpus, ref) == "LVL0":
            result.direct_lvl0 = True
            result.lvl0.append(ref)
            nodes.append(_lvl0_node(corpus, ref, floor_ids))
            continue
        parent = derive(
            corpus,
            corpus.by_id[ref.partition("#")[0]],
            floor_ids,
            (*_stack, own),
        )
        result.cycle |= parent.cycle
        result.unresolved += parent.unresolved
        result.lvl0 += [x for x in parent.lvl0 if x not in result.lvl0]
        nodes.append(
            (parent.rank, parent.waivable, parent.forced, parent.primes)
        )
    ranks = [n[0] for n in nodes if n[0] is not None]
    result.rank = min(ranks) if ranks else None
    result.waivable = bool(nodes) and all(n[1] for n in nodes)
    result.forced = any(n[2] for n in nodes)
    result.primes = any(n[3] for n in nodes)
    return result


def lower_provisions(corpus: Corpus) -> list[Entry]:
    """Return the provisions below LVL0, sorted by identifier.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    list[Entry]
        Provisions whose level is not LVL0, numbered segments compared
        as numbers.
    """
    return sorted(
        (e for e in corpus.provisions() if e.meta.get("level") != "LVL0"),
        key=lambda e: [
            int(p) if p.isdigit() else 0 for p in str(e.meta["id"]).split(".")
        ],
    )


def derive_all(corpus: Corpus, floor_ids: set[str]) -> dict[str, Derived]:
    """Derive every provision below LVL0.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    floor_ids : set[str]
        Floor obligations (GOV.10).

    Returns
    -------
    dict[str, Derived]
        Derived values by provision identifier.
    """
    return {
        str(e.meta["id"]): derive(corpus, e, floor_ids)
        for e in lower_provisions(corpus)
    }
