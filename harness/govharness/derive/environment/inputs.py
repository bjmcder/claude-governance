"""What the human owner states about one environment.

Governance states the outcomes; the owner states where the work is and
what the environment opens to the agent. These inputs become part of
the working bounds only once a configuration that the agent is unable
to alter, or an entry that STND.DFLT.23 accepts, opens them (STND.DFLT,
term "Working bounds").
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Installed software, which the working bounds open for reading by
# default (STND.DFLT, term "Working bounds").
SOFTWARE_LOCATIONS = ("/usr", "/lib", "/lib64", "/bin", "/sbin", "/opt")
# Device files that every shell writes to; writing them changes nothing.
NULL_DEVICES = ("/dev/null", "/dev/stdout", "/dev/stderr", "/dev/tty")
# The directory of STND.DFLT.29, at the top of the work.
STORE = "secrets"


@dataclass(frozen=True)
class RemoteWrite:
    """One remote write that a standing authorization in force names.

    Parameters
    ----------
    authorization : str
        Identifier of the authorization file (STND.PROJ.6).
    kind : str
        Kind of write of the table of STND.PROJ.7 that the guard matches,
        ``commit`` or ``post``.
    destination : str
        The destination's address in full, compared as a whole.
    branches : tuple[str, ...]
        For ``commit``, the branches the authorization covers there;
        empty for ``post``.
    expires : str
        Timestamp at which the authorization lapses, which the guard
        compares with its clock at every call; empty for one that lapses
        only when revoked.
    """

    authorization: str
    kind: str
    destination: str
    branches: tuple[str, ...]
    expires: str


@dataclass(frozen=True)
class Inputs:
    """The owner's statement of one environment.

    Parameters
    ----------
    work : str
        Absolute path of the top directory of the primary copy of the
        work.
    home : str
        Absolute path of the home directory of the agent's account.
    open_paths : tuple[str, ...]
        Further absolute locations opened for reading and writing, such
        as a temporary location.
    domains : tuple[str, ...]
        Network domains opened to the agent.
    search : bool
        Whether web search is opened as a retrieval scope.
    tools : tuple[str, ...]
        Patterns of the tools of other servers opened to the agent.
    unattended : bool
        Whether nobody is there to answer a referral.
    assured : bool
        Whether the classification records the work as CSQ0 or CSQ1
        (STND.DFLT, term "Assured work").
    secret_store : bool
        Whether the human owner provides the store of STND.DFLT.29.
    secrets : tuple[str, ...]
        Names of the files of that store whose secrets an authorization
        permits the agent to handle; naming one provides the store.
    remote_writes : tuple[RemoteWrite, ...]
        Remote writes that a standing authorization in force names by
        destination and kind, read by ``authorizations``; each other
        remote write is referred.
    referred : tuple[str, ...]
        One line per authorization the owner named whose writes stay
        referred, such as one per action, with the reason.
    """

    work: str
    home: str
    open_paths: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    search: bool = False
    tools: tuple[str, ...] = ()
    unattended: bool = False
    assured: bool = False
    secret_store: bool = False
    secrets: tuple[str, ...] = ()
    remote_writes: tuple[RemoteWrite, ...] = ()
    referred: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Reject an input the configuration would misread.

        A relative path would move with the caller; a domain in another
        case never matches the guard's lower-case host; a tool pattern
        outside ``mcp__`` would allow a built-in tool unchecked; a secret
        name with a slash, or ``.`` or ``..``, would open a location
        other than one file of the store.

        Raises
        ------
        ValueError
            If a path is not absolute, a domain is no lower-case domain
            name, a tool pattern names no tool of another server, or a
            secret name is no file name.
        """
        for path in (self.work, self.home, *self.open_paths):
            if not path.startswith("/"):
                raise ValueError(f"{path}: not an absolute path")
        for domain in self.domains:
            if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", domain):
                raise ValueError(f"{domain}: not a lower-case domain name")
        # The guard matches a pattern against tools of other servers
        # only, and settings skip such a rule with parentheses.
        for tool in self.tools:
            if not tool.startswith("mcp__") or "(" in tool:
                raise ValueError(f"{tool}: not a pattern of mcp__ tools")
        for name in self.secrets:
            if name in {"", ".", ".."} or "/" in name:
                raise ValueError(f"{name!r}: not a file name of the store")

    @property
    def store(self) -> str | None:
        """Return the directory of STND.DFLT.29, where one is provided.

        Returns
        -------
        str | None
            Its absolute path, or None without a store.
        """
        if self.secret_store or self.secrets:
            return f"{self.work.rstrip('/')}/{STORE}"
        return None

    @property
    def secret_paths(self) -> tuple[str, ...]:
        """Return the files of the store opened to the agent.

        Returns
        -------
        tuple[str, ...]
            Absolute paths, one per named secret.
        """
        store = self.store
        return tuple(f"{store}/{name}" for name in self.secrets)

    @property
    def writable(self) -> tuple[str, ...]:
        """Return the locations the agent may write.

        Returns
        -------
        tuple[str, ...]
            The work, the opened locations, and the null devices.
        """
        return (self.work, *self.open_paths, *NULL_DEVICES)

    @property
    def readable(self) -> tuple[str, ...]:
        """Return the locations the agent may read but not write.

        Returns
        -------
        tuple[str, ...]
            The installed software.
        """
        return SOFTWARE_LOCATIONS
