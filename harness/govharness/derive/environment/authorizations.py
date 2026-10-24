"""Read the authorizations of remote writes that a derivation honors.

STND.HARN.18 refers each remote write that no authorization in force
names by destination and kind of write. STND.PROJ.6 fixes the fields of
an authorization file that covers a remote write, and STND.PROJ.7 the
kinds of write. STND.HARN.29 states when a derived configuration may
rely on one, tested when the configuration is derived: the file is
adopted, granted by the human owner, extends to the role the
configuration is derived for (GUARD.12), is recorded no later than the
derivation, is pinned in its current content by a transaction of type
``authorize`` of the human owner that no later ``revoke`` names, is
signed where the work is assured or the corpus holds a signer register,
and is standing. The row Standing is tested for each entry and kind:
a kind whose effect is irrevocable at the entry's destination
(GUARD.11) opens nothing, and its writes stay referred, while the
other entries of the same authorization stand. Its expiry, where it
has one, is tested again by the guard at each write; a revocation
reaches the configuration only when it is derived again.

The owner names the authorizations an environment takes, as the owner
names the opened secrets; this module checks each one and returns the
remote writes the guard matches. An authorization that fails a test is
an error, so that the derivation stops with the reason rather than
deriving a configuration that silently refers what the owner expected
to pass. A malformed entry fails closed: the record then does not state
one authorization, so none of its entries is relied on and the
derivation stops. One per action stays referred, because a
configuration cannot tell the one action it covers from a repetition;
the owner's answer to the referral confirms it.

Where the work is not assured and the corpus holds no signer register,
STND.HARN.29 asks for no signature, but nothing then shows that the
human owner, rather than an agent that appended an ``authorize`` to the
ledger and recomputed its chain, recorded the grant: appends are
permitted writes. The derivation is therefore refused unless the owner
states that it accepts the authorizations unsigned, and the summary
then says that each was accepted so. Where a signature is required,
that statement has no effect (security verification of unit 0008,
M-c; unit 0010).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import PurePosixPath
from typing import Any

from govharness.core.corpus import Corpus, Tree, scope_hash
from govharness.derive.environment.inputs import RemoteWrite
from govharness.ledger.transactions import chain_problems

GRANTOR = "The Human Owner"
STATUS = "adopted"
KIND = "auth"
# The value of ``expires`` for an authorization whose stated duration is
# until its revocation (GUARD.10).
UNTIL_REVOKED = "until revoked"
# The kinds of write of STND.PROJ.7; GUARD.11 names publication,
# release, and transmission beyond the environment as irrevocable.
KINDS = ("commit", "post", "publish", "transmit", "other")
IRREVOCABLE = ("publish", "transmit")
# The kinds whose destination the guard reads from the command.
MATCHED = ("commit", "post")
ENTRY_FIELDS = {"destination", "kinds", "branches", "provisioned"}
DOMAIN = r"[a-z0-9-]+(?:\.[a-z0-9-]+)+"
PATH = r"[A-Za-z0-9._~-]+(?:/[A-Za-z0-9._~-]+)*"
# A repository address: https or ssh without credentials, or the short
# form user@host:path. No query, fragment, or password is admitted, so
# that no record holds a credential (AGENT.45).
REPOSITORY_RE = re.compile(
    rf"https://{DOMAIN}(?::[0-9]{{1,5}})?/{PATH}"
    rf"|ssh://(?:[a-z0-9._-]+@)?{DOMAIN}(?::[0-9]{{1,5}})?/{PATH}"
    rf"|[a-z0-9._-]+@{DOMAIN}:{PATH}"
)
# A tracker address, as ``gh --repo HOST/OWNER/REPO`` names it.
TRACKER_RE = re.compile(rf"https://{DOMAIN}/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+")
BRANCH_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._-]*(?:/[A-Za-z0-9._-]+)*")
# The owner's statement that authorizations are relied on unsigned, as
# the command line spells it.
ACCEPT_UNSIGNED = "--accept-unsigned"


def timestamp(value: Any) -> datetime:
    """Return a Timestamp of STND.HARN: ISO 8601 with its UTC offset.

    Parameters
    ----------
    value : Any
        The field value.

    Returns
    -------
    datetime
        The time, aware of its offset.

    Raises
    ------
    ValueError
        If the value is no string, no ISO 8601 time, or has no offset.
    """
    if not isinstance(value, str) or "T" not in value:
        raise ValueError(f"{value!r} is no timestamp")
    moment = datetime.fromisoformat(value)
    if moment.utcoffset() is None:
        raise ValueError(f"{value!r} has no UTC offset")
    return moment


def segments_safe(address: str) -> bool:
    """Return whether no path segment of an address is ``.`` or ``..``.

    Parameters
    ----------
    address : str
        A destination address.

    Returns
    -------
    bool
        Whether the address names one location as written.
    """
    tail = address.split("://", 1)[-1]
    return not any(part in {".", ".."} for part in re.split(r"[/:]", tail))


def entry_problems(entry: Any) -> list[str]:
    """Return how one entry of ``remote_writes`` breaks STND.PROJ.6.

    Parameters
    ----------
    entry : Any
        The entry as the front matter holds it.

    Returns
    -------
    list[str]
        One line per problem; empty when the entry is well formed.
    """
    if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
        return [f"an entry does not hold exactly {sorted(ENTRY_FIELDS)}"]
    destination, kinds = entry["destination"], entry["kinds"]
    branches, provisioned = entry["branches"], entry["provisioned"]
    if not isinstance(destination, str) or not segments_safe(destination):
        return ["a destination is no single address"]
    problems: list[str] = []
    if (
        not isinstance(kinds, list)
        or not kinds
        or not all(isinstance(k, str) and k in KINDS for k in kinds)
        or len(set(kinds)) != len(kinds)
    ):
        problems.append(f"{destination}: kinds are not distinct of {KINDS}")
        kinds = []
    if not isinstance(provisioned, bool):
        problems.append(f"{destination}: provisioned is no boolean")
    if not isinstance(branches, list) or not all(
        isinstance(b, str)
        and BRANCH_RE.fullmatch(b)
        and ".." not in b
        and not b.endswith(".lock")
        for b in branches
    ):
        problems.append(f"{destination}: a branch is no branch name")
        branches = []
    if "commit" in kinds and not REPOSITORY_RE.fullmatch(destination):
        problems.append(f"{destination}: no repository address")
    if "commit" in kinds and not branches:
        problems.append(f"{destination}: commit names no branch")
    if "commit" not in kinds and branches:
        problems.append(f"{destination}: branches without commit")
    if "post" in kinds and not TRACKER_RE.fullmatch(destination):
        problems.append(f"{destination}: no tracker address")
    return problems


def irrevocable(entry: dict[str, Any], kind: str) -> str | None:
    """Return why a kind of a well-formed entry is irrevocable, or None.

    Parameters
    ----------
    entry : dict[str, Any]
        An entry for which ``entry_problems`` returned nothing.
    kind : str
        One of its kinds.

    Returns
    -------
    str | None
        The reason the table of STND.PROJ.7 marks the kind irrevocable
        at the entry's destination, or None where it is revocable.
    """
    if kind in IRREVOCABLE:
        return "its effect is irrevocable (GUARD.11)"
    if entry["provisioned"] is not True:
        return (
            "its destination is not recorded as provisioned, a "
            "transmission beyond the environment (GUARD.11)"
        )
    return None


def covers(scope: list[str], rel: PurePosixPath) -> bool:
    """Return whether a transaction's scope pins a file.

    Parameters
    ----------
    scope : list[str]
        Scope paths of the transaction.
    rel : PurePosixPath
        The file, relative to the corpus root.

    Returns
    -------
    bool
        Whether a scope path is the file's directory or one above it.
    """
    return any(
        rel.parts[: len(PurePosixPath(s).parts)] == PurePosixPath(s).parts
        for s in scope
    )


def record_problems(
    ident: str,
    rel: PurePosixPath,
    tree: Tree,
    ledger: list[dict[str, Any]],
    recorded: date | None,
    signed: bool,
    verified: bool,
    accept_unsigned: bool = False,
) -> tuple[list[str], Any]:
    """Return how the ledger fails to record an authorization in force.

    Parameters
    ----------
    ident : str
        Identifier of the authorization.
    rel : PurePosixPath
        Its file, relative to the corpus root.
    tree : Tree
        Snapshot of the corpus.
    ledger : list[dict[str, Any]]
        The ledger of the corpus, in order.
    recorded : date | None
        The file's date recorded, where it is a date.
    signed : bool
        Whether the transaction must carry a verified signature: for
        assured work, and wherever the corpus holds a signer register.
    verified : bool
        Whether every signature of the ledger verifies against the
        signer register, as the caller checked it.
    accept_unsigned : bool
        Whether the owner stated that it accepts an unsigned
        transaction; it has no effect where ``signed`` holds, and is
        named in the reason only so that the owner learns as much.

    Returns
    -------
    tuple[list[str], Any]
        One line per problem, empty when the ledger's chain is intact,
        the latest transaction that pins the file is the human owner's
        ``authorize`` of it, dated no earlier than the file's date
        recorded, pins its current content, and no later ``revoke``
        names it; and the ``seq`` of that transaction, or None.
    """
    if chain_problems(ledger):
        return ["the ledger's chain is broken (STND.HARN.8)"], None
    pinning = [
        (i, e) for i, e in enumerate(ledger) if covers(e.get("scope") or [], rel)
    ]
    if not pinning:
        return ["no transaction of the ledger pins it"], None
    index, latest = pinning[-1]
    targets = latest.get("targets")
    problems: list[str] = []
    if (
        latest.get("type") != "authorize"
        or latest.get("actor") != GRANTOR
        or not isinstance(targets, list)
        or ident not in targets
    ):
        problems.append(
            f"the latest transaction that pins it, seq {latest.get('seq')}, "
            f"is no authorize of it by {GRANTOR}"
        )
    if scope_hash(tree, list(latest.get("scope") or [])) != latest.get(
        "corpus_hash"
    ):
        problems.append("its content changed after the ledger pinned it")
    try:
        if recorded and recorded > timestamp(latest.get("at")).date():
            problems.append("its date recorded is after its transaction")
    except ValueError:
        problems.append("its transaction carries no timestamp")
    if any(
        e.get("type") == "revoke"
        and (not isinstance(e.get("targets"), list) or ident in e["targets"])
        for e in ledger[index + 1 :]
    ):
        problems.append("a later transaction revokes it")
    if signed and not (latest.get("signature") and verified):
        problems.append(
            "its transaction carries no signature that the signer register "
            "verifies (STND.HARN.11)"
            + (
                f", and {ACCEPT_UNSIGNED} has no effect where the work is "
                "assured or a signer register exists"
                if accept_unsigned
                else ""
            )
        )
    return problems, latest.get("seq")


def read_one(
    corpus: Corpus,
    ident: str,
    now: datetime,
    role: str,
    horizon: timedelta | None,
) -> tuple[dict[str, Any], PurePosixPath, date | None, list[str]]:
    """Return an authorization's fields, its file, and its problems.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus.
    ident : str
        Identifier of the authorization.
    now : datetime
        Time of the derivation, aware of its offset.
    role : str
        The role or agent for which the configuration is derived.
    horizon : timedelta | None
        The longest time from the derivation to an expiry that the owner
        accepts, or None for no bound.

    Returns
    -------
    tuple[dict[str, Any], PurePosixPath, date | None, list[str]]
        The front matter, the path relative to the root, the date
        recorded where it is one, and one line per field that keeps it
        from being in force (STND.HARN.29).

    Raises
    ------
    ValueError
        If the corpus holds no authorization of that identifier.
    """
    entry = corpus.by_id.get(ident)
    if entry is None or entry.meta.get("kind") != KIND:
        raise ValueError(f"{ident}: no authorization of the corpus")
    meta = entry.meta
    problems: list[str] = []
    if meta.get("status") != STATUS:
        problems.append(f"status {meta.get('status')!r}, not {STATUS!r}")
    if meta.get("grantor") != GRANTOR:
        problems.append(f"grantor {meta.get('grantor')!r}, not {GRANTOR!r}")
    recorded = None
    try:
        recorded = date.fromisoformat(str(meta.get("recorded")))
        if recorded > now.date():
            problems.append(f"recorded {recorded} is after the derivation")
    except ValueError:
        problems.append(f"recorded {meta.get('recorded')!r} is no date")
    expires = meta.get("expires")
    if expires == UNTIL_REVOKED:
        if horizon is not None:
            problems.append("it lapses only when revoked, beyond the horizon")
    else:
        try:
            moment = timestamp(expires)
            if moment <= now:
                problems.append(f"expired at {expires}")
            elif horizon is not None and moment > now + horizon:
                problems.append(f"its expiry {expires} is beyond the horizon")
        except ValueError as error:
            problems.append(f"expires: {error}")
    delegable = meta.get("delegable_to")
    if not isinstance(delegable, list) or not all(
        isinstance(r, str) and r for r in delegable
    ):
        problems.append("delegable_to is no list of roles")
    elif role not in delegable:
        problems.append(
            f"it does not extend to {role or 'an unnamed role'} (GUARD.12)"
        )
    standing = meta.get("standing")
    if not isinstance(standing, bool):
        problems.append("standing is no boolean")
    writes = meta.get("remote_writes")
    if not isinstance(writes, list) or not writes:
        problems.append("remote_writes names no destination")
    else:
        for item in writes:
            problems += entry_problems(item)
    return meta, PurePosixPath(entry.path.as_posix()), recorded, problems


@dataclass(frozen=True)
class Reading:
    """The remote writes that the named authorizations open.

    Parameters
    ----------
    writes : tuple[RemoteWrite, ...]
        One per destination and matched kind of each standing
        authorization in force.
    referred : tuple[str, ...]
        One line per authorization, or kind, whose writes stay referred.
    summary : tuple[str, ...]
        One line per authorization read, with the transaction that pins
        it, for the owner to compare with what was granted, and one
        more for each that was accepted unsigned.
    """

    writes: tuple[RemoteWrite, ...]
    referred: tuple[str, ...]
    summary: tuple[str, ...]


def read_authorizations(
    corpus: Corpus,
    tree: Tree,
    ledger: list[dict[str, Any]],
    idents: tuple[str, ...],
    now: datetime,
    role: str,
    signed: bool,
    verified: bool,
    horizon: timedelta | None = None,
    accept_unsigned: bool = False,
) -> Reading:
    """Return the remote writes that the named authorizations open.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus holding the authorization files.
    tree : Tree
        Snapshot of the same corpus, for the content the ledger pins.
    ledger : list[dict[str, Any]]
        The ledger of the corpus, in order.
    idents : tuple[str, ...]
        Identifiers of the authorizations the owner names.
    now : datetime
        Time of the derivation, aware of its offset.
    role : str
        The role or agent for which the configuration is derived; an
        authorization that does not extend to it is not in force for
        this configuration (GUARD.12).
    signed : bool
        Whether a verified signature is required: for assured work, and
        wherever the corpus holds a signer register.
    verified : bool
        Whether every signature of the ledger verifies.
    horizon : timedelta | None
        The longest time to an expiry that the owner accepts.
    accept_unsigned : bool
        Whether the owner accepts the authorizations unsigned where no
        signature is required (``signed`` false). Without it, the
        derivation is refused there; where ``signed`` holds, it has no
        effect.

    Returns
    -------
    Reading
        The writes opened, the lines still referred, and the summary.

    Raises
    ------
    ValueError
        If an authorization is not in force, or none is required to be
        signed and the owner did not accept them unsigned, with every
        reason.
    """
    if now.utcoffset() is None:
        raise ValueError("the time of the derivation has no UTC offset")
    writes: list[RemoteWrite] = []
    referred: list[str] = []
    summary: list[str] = []
    errors: list[str] = []
    for ident in dict.fromkeys(idents):
        meta, rel, recorded, problems = read_one(
            corpus, ident, now, role, horizon
        )
        found, seq = record_problems(
            ident, rel, tree, ledger, recorded, signed, verified,
            accept_unsigned,
        )
        problems += found
        if problems:
            errors.append(f"{ident} is not in force: " + "; ".join(problems))
            continue
        expires = "" if meta["expires"] == UNTIL_REVOKED else meta["expires"]
        summary.append(
            f"{ident}: pinned by seq {seq}; "
            f"{'standing' if meta['standing'] else 'per action'}; expires "
            f"{expires or 'when revoked'}; "
            + "; ".join(
                f"{', '.join(i['kinds'])} at {i['destination']}"
                + (f" ({', '.join(i['branches'])})" if i["branches"] else "")
                for i in meta["remote_writes"]
            )
        )
        if not signed:
            summary.append(
                f"{ident}: accepted unsigned ({ACCEPT_UNSIGNED}): no signer "
                "register exists, so only the owner's reading of the line "
                f"above shows that the human owner recorded seq {seq}"
            )
        if not meta["standing"]:
            referred.append(
                f"{ident}: per action, so each write it covers is referred "
                "and the human owner's answer confirms it"
            )
            continue
        for item in meta["remote_writes"]:
            for kind in item["kinds"]:
                reason = irrevocable(item, kind)
                if reason:
                    referred.append(
                        f"{ident}: kind {kind} at {item['destination']} "
                        f"opens nothing standing, since {reason}, so it is "
                        "referred"
                    )
                    continue
                if kind not in MATCHED:
                    referred.append(
                        f"{ident}: kind {kind} at {item['destination']} is "
                        "not matched by this adapter, so it is referred"
                    )
                    continue
                branches = item["branches"] if kind == "commit" else []
                writes.append(
                    RemoteWrite(
                        ident,
                        kind,
                        item["destination"],
                        tuple(branches),
                        str(expires),
                    )
                )
    if idents and not signed and not accept_unsigned:
        errors.append(
            "no signer register exists and the work is not assured, so "
            "nothing shows that the human owner, and not an agent that "
            "appended to the ledger, recorded "
            + ", ".join(dict.fromkeys(idents))
            + "; found a signer register (sign found), or pass "
            f"{ACCEPT_UNSIGNED} to rely on each unsigned, and compare the "
            "summary it prints with what was granted before installing"
        )
    if errors:
        raise ValueError(" | ".join(errors))
    return Reading(tuple(writes), tuple(referred), tuple(summary))
