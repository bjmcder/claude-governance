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
    """

    work: str
    home: str
    open_paths: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    search: bool = False
    tools: tuple[str, ...] = ()
    unattended: bool = False
    assured: bool = False

    def __post_init__(self) -> None:
        """Reject an input the configuration would misread.

        A relative path would move with the caller; a domain in another
        case never matches the guard's lower-case host; a tool pattern
        outside ``mcp__`` would allow a built-in tool unchecked.

        Raises
        ------
        ValueError
            If a path is not absolute, a domain is no lower-case domain
            name, or a tool pattern names no tool of another server.
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
