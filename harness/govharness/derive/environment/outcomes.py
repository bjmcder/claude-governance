"""Read the environment outcomes and protected locations from governance.

STND.HARN.18 holds the table named ``environment-outcomes``: the
outcomes that the configuration of an agent's environment is derived
from, each with a key, its source provision, and its response.
STND.INSTR.3 holds the table named ``protected-locations``. Both are
found by the name in the field ``defines``, never by position, so an
amendment to either reaches every adapter without a change of code.
"""

from __future__ import annotations

from dataclasses import dataclass

from govharness.core.corpus import Corpus
from govharness.core.tables import read_table

OUTCOMES_TABLE = "environment-outcomes"
OUTCOMES_HEADER = ("Key", "Outcome", "Source", "Response")
PROTECTED_TABLE = "protected-locations"
PROTECTED_HEADER = ("Location",)
RESPONSES = ("Refuse", "Refer")


@dataclass(frozen=True)
class Outcome:
    """One outcome of STND.HARN.18.

    Parameters
    ----------
    key : str
        Stable key, such as ``protected-locations``.
    text : str
        The outcome as the table states it.
    source : str
        Identifier of the provision it comes from.
    response : str
        ``Refuse`` or ``Refer``.
    """

    key: str
    text: str
    source: str
    response: str


@dataclass(frozen=True)
class NamedTable:
    """A table that a provision names in its field ``defines``.

    Parameters
    ----------
    holder : str
        Identifier of the provision that holds the table.
    status : str
        Status of that provision, such as ``draft`` or ``adopted``.
    rows : list[dict[str, str]]
        Rows mapping each heading to its cell.
    """

    holder: str
    status: str
    rows: list[dict[str, str]]


def named_table(
    corpus: Corpus, name: str, header: tuple[str, ...]
) -> NamedTable:
    """Return the one table of the corpus that carries a name.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    name : str
        Name in the field ``defines``.
    header : tuple[str, ...]
        Column headings the table must have.

    Returns
    -------
    NamedTable
        The holder, its status, and the rows.

    Raises
    ------
    LookupError
        If no provision or more than one names the table, or the holder
        has no table with those headings.
    """
    holders = [
        entry
        for entry in corpus.entries
        if name in (entry.meta.get("defines") or [])
    ]
    if len(holders) != 1:
        raise LookupError(f"table `{name}` is named by {len(holders)} items")
    holder = holders[0]
    rows = read_table(holder.body, header)
    if not rows:
        raise LookupError(
            f"{holder.meta['id']}: no table with columns {', '.join(header)}"
        )
    return NamedTable(
        str(holder.meta["id"]), str(holder.meta.get("status", "")), rows
    )


def read_outcomes(corpus: Corpus) -> tuple[NamedTable, list[Outcome]]:
    """Return the table of STND.HARN.18 and its outcomes.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    tuple[NamedTable, list[Outcome]]
        The table as read, and one outcome per row.

    Raises
    ------
    LookupError
        If the table is missing or malformed.
    ValueError
        If a key repeats or a response is neither Refuse nor Refer.
    """
    table = named_table(corpus, OUTCOMES_TABLE, OUTCOMES_HEADER)
    outcomes = [
        Outcome(row["Key"], row["Outcome"], row["Source"], row["Response"])
        for row in table.rows
    ]
    keys = [outcome.key for outcome in outcomes]
    if len(set(keys)) != len(keys):
        raise ValueError(f"{table.holder}: an outcome key repeats")
    for outcome in outcomes:
        if outcome.response not in RESPONSES:
            raise ValueError(
                f"{table.holder}: {outcome.key} has response "
                f"{outcome.response!r}"
            )
    return table, outcomes


def read_protected(corpus: Corpus) -> NamedTable:
    """Return the table of protected locations of STND.INSTR.3.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.

    Returns
    -------
    NamedTable
        The table as read; each row names one kind of location.

    Raises
    ------
    LookupError
        If the table is missing or malformed.
    """
    return named_table(corpus, PROTECTED_TABLE, PROTECTED_HEADER)
