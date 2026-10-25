"""Pre-action guard of an agent's environment (STND.HARN.18).

The environment runs this file before each tool call of an agent. It
reads the call as JSON on standard input and a policy file named on the
command line, and answers on standard output with a decision for the
calls that reach an outcome of the policy:

- ``deny`` for an outcome whose response is Refuse, and for every
  outcome in an unattended session, where nobody is there to decide;
- ``ask`` for an outcome whose response is Refer.

A call that reaches no outcome gets no answer, and the environment's own
permission rules decide it. A call the guard is unable to read, or that
makes it fail, is denied at every class. A policy the guard is unable
to read is never silent (PRIME.4): for assured work, named by the flag
``--assured``, the call is denied; for other work, the call proceeds and
the human owner and the agent are told that it went unguarded
(STND.HARN.23).

A shell command line is read as the shell reads it: quotes, comments,
here-documents, command and process substitution, and compound
commands. An operand is resolved without running anything, against
every directory the line may run in, since a ``cd`` within the line
adds one. An operand that depends on a value the guard does not know,
such as a variable, is computed: a removal or write of a computed item
is referred, since its items cannot be listed (STND.DFLT.24). A program
the guard does not know is searched for a command it knows, so that a
launcher such as ``timeout`` or ``uv run`` does not hide one.

The guard sees only what a call names. A program that deletes, writes,
or connects by itself, whether a script, code given inline to an
interpreter, or an alias or function defined earlier, is not seen; the
coverage report of the adapter states each such gap (STND.HARN.19). The
file uses the standard library alone and imports nothing from the
package, because it is installed outside the work, where the agent's
account is unable to alter it.
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import shlex
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

DENY = "deny"
ASK = "ask"
RESPONSES = {"Refuse": DENY, "Refer": ASK}
# A longer command line is not read but referred: the guard must answer
# within the hook's timeout, and no routine command comes near this.
MAX_COMMAND = 100_000
# Most directories one line may run in before relative paths count as
# computed; each ``cd`` can double them.
MAX_DIRECTORIES = 16
# Most words one brace expansion may produce before it counts as
# computed.
MAX_EXPANSION = 64
PUNCTUATION = ";&|()<>"
WRITE_REDIRECTS = {">", ">|", "&>", "<>", ">&"}
APPEND_REDIRECTS = {">>", "&>>"}
READ_REDIRECTS = {"<", "<>"}
REDIRECTS = WRITE_REDIRECTS | APPEND_REDIRECTS | READ_REDIRECTS | {
    "<<<",
    "<&",
}
# Reserved words that open or close a compound command; the command
# that follows one still runs.
KEYWORDS = {
    "!",
    "{",
    "}",
    "do",
    "done",
    "elif",
    "else",
    "fi",
    "if",
    "then",
    "until",
    "while",
}
# A here-document's body is stored aside and named by this mark.
MARK = "\0"
MARK_RE = re.compile(r"^\0(\d+)\0$")
DELIMITER_RE = re.compile(
    r"""<<(-?)[ \t]*((?:[^\s;&|()<>'"\\]|\\.|'[^']*'|"[^"]*")+)"""
)
# Names whose value the guard knows; a bare one means the line sets it.
KNOWN_VARIABLES = ("HOME", "PWD")
SET_VARIABLE_RE = re.compile(r"(?<![\w${])(HOME|PWD)\b(?!})")
SHELLS = {"bash", "dash", "ksh", "sh", "zsh"}
ELEVATORS = {"doas", "pkexec", "run0", "runuser", "su", "sudo"}
REMOVERS = {"rm", "rmdir", "shred", "unlink"}
# Removers that remove files only, so that no pattern of theirs empties
# a directory.
FILE_REMOVERS = {"shred", "unlink"}
COPIERS = {"cp", "install", "ln"}
CREATORS = {"mkdir", "touch", "truncate"}
READERS = {
    "cat",
    "diff",
    "du",
    "file",
    "head",
    "less",
    "ls",
    "more",
    "stat",
    "tail",
    "tar",
    "wc",
}
# Programs whose arguments are text, never a command they run.
TEXT_PROGRAMS = {"echo", "egrep", "fgrep", "grep", "printf", "rg"}
REMOTE_COPIERS = {"ftp", "scp", "sftp"}
PUBLISHERS = {
    "cargo": {"publish"},
    "docker": {"push"},
    "npm": {"publish"},
    "pnpm": {"publish"},
    "twine": {"upload"},
    "yarn": {"publish"},
}
GH_WRITES = {
    "alias": {"delete", "import", "set"},
    "extension": {"exec", "install", "remove", "upgrade"},
    "gist": {"create", "delete", "edit"},
    "issue": {"close", "comment", "create", "delete", "edit", "reopen"},
    "pr": {"close", "comment", "create", "edit", "merge", "review"},
    "release": {"create", "delete", "edit", "upload"},
    "repo": {"archive", "create", "delete", "edit", "rename"},
    "workflow": {"disable", "enable", "run"},
}
CURL_WRITES = {
    "--data",
    "--data-binary",
    "--data-raw",
    "--data-urlencode",
    "--form",
    "--json",
    "--upload-file",
    "-F",
    "-T",
    "-d",
}
REMOTE_PROGRAMS = (
    REMOTE_COPIERS | {"curl", "gh", "rsync", "ssh", "wget"} | set(PUBLISHERS)
)
# Every program the guard reads; a launcher is searched for one.
KNOWN = (
    SHELLS
    | ELEVATORS
    | REMOVERS
    | COPIERS
    | CREATORS
    | READERS
    | REMOTE_PROGRAMS
    | {"cd", "chgrp", "chmod", "chown", "dd", "eval", "find", "git"}
    | {"mv", "perl", "pushd", "sed", "setcap", "tee", "xargs"}
)
HISTORY_REWRITES = {"filter-branch", "filter-repo", "rebase", "replace"}
GLOB_CHARS = set("*?[")
# The authority of a URL ends at the first slash, backslash, query, or
# fragment; a backslash counts because fetchers read it as a slash.
AUTHORITY_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://([^/\\?#]*)")
HOST_RE = re.compile(r"^[a-z0-9.-]+$")
EDIT_TOOLS = {"Edit", "MultiEdit", "NotebookEdit", "Write"}
READ_TOOLS = {"Glob", "Grep", "LS", "Read"}
# The kinds of write of STND.PROJ.7 whose destination the guard reads.
GRANT_KINDS = {"commit", "post"}
GRANT_FIELDS = {"authorization", "kind", "destination", "branches", "expires"}
# Options of ``git push`` that change neither what is pushed nor where;
# every other option leaves an authorized push referred.
PUSH_OPTIONS = {
    "--atomic",
    "--no-progress",
    "--porcelain",
    "--progress",
    "--quiet",
    "--set-upstream",
    "--verbose",
    "-q",
    "-u",
    "-v",
}
# Git configuration that sends a push elsewhere, adds to what it
# pushes, or runs a program for the transport: sections, then keys by
# section and key, then keys of each remote.
GIT_SECTIONS = {"alias", "credential", "include", "includeif", "url"}
GIT_KEYS = {
    ("core", "askpass"),
    ("core", "fsmonitor"),
    ("core", "gitproxy"),
    ("core", "hookspath"),
    ("core", "sshcommand"),
    ("extensions", "refstorage"),
    ("http", "proxy"),
    # Pages a push, which then runs GIT_PAGER (GIT_ADMITTED).
    ("pager", "push"),
    ("push", "followtags"),
    ("push", "recursesubmodules"),
    ("submodule", "recurse"),
}
# The variables of git that leave an authorized push unreferred; every
# other variable of git refers it (unit 0014). A push launches no
# editor, so it reads neither GIT_EDITOR nor GIT_SEQUENCE_EDITOR. It
# runs GIT_PAGER only when paged, by ``--paginate``, which no admitted
# push takes, or by ``pager.push``, which GIT_KEYS refers.
# GIT_TERMINAL_PROMPT, set false, only stops git asking on the terminal
# for a credential; it supplies none (git(1), Environment Variables).
# Claude Code sets GIT_EDITOR in the shell of the agent.
GIT_ADMITTED = frozenset(
    {"GIT_EDITOR", "GIT_PAGER", "GIT_SEQUENCE_EDITOR", "GIT_TERMINAL_PROMPT"}
)
# Options of git subcommands that take the next word, so that a ``-n``
# after one is its value, not a dry run.
DRY_VALUED = {"--exclude", "--pathspec-from-file", "-e", "-o"}
REMOTE_KEYS = {"mirror", "proxy", "pushurl", "receivepack", "vcs"}
# The system's git configuration file.
GIT_SYSTEM_CONFIG = "/etc/gitconfig"
GIT_SECTION_RE = re.compile(
    r'\[\s*([A-Za-z0-9.-]+)(?:\s+"((?:[^"\\\n]|\\.)*)")?\s*\]\s*(?:[#;].*)?'
)
GIT_KEY_RE = re.compile(r"([A-Za-z][A-Za-z0-9-]*)\s*(?:=\s*(.*))?")
REMOTE_NAME_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._-]*")
# A tracker post of ``gh``: the subcommands, and the options each takes
# with a value; every other option leaves it referred.
GH_POSTS = {
    ("issue", "create"): {"--body", "--repo", "--title", "-R", "-b", "-t"},
    ("issue", "comment"): {"--body", "--repo", "-R", "-b"},
    ("pr", "comment"): {"--body", "--repo", "-R", "-b"},
}
# A call that carries an authorized write holds only these characters:
# no expansion, substitution, redirection, here-document, pattern,
# comment, or separator that the sole-command rule would have to read.
PLAIN_RE = re.compile(r"[A-Za-z0-9 _./:@=,+'\"-]*")
# Options of git before its subcommand that take the next word.
GIT_VALUED = {"-C", "-c", "--config-env", "--git-dir", "--namespace",
              "--super-prefix", "--work-tree"}
GH_REPO_RE = re.compile(
    r"([a-z0-9-]+(?:\.[a-z0-9-]+)+)/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)"
)
POLICY_LISTS = (
    "writable",
    "readable",
    "protected",
    "homes",
    "configuration",
    "ledgers",
    "domains",
    "tools",
    "secrets",
)


@dataclass(frozen=True)
class Grant:
    """One remote write that the environment lets proceed.

    Parameters
    ----------
    authorization : str
        Identifier of the authorization that names it.
    kind : str
        ``commit`` or ``post``.
    destination : str
        Address of the destination, compared as a whole.
    branches : tuple[str, ...]
        Branches a ``commit`` may update.
    expires : float
        Seconds since the epoch at which the authorization lapses.
    """

    authorization: str
    kind: str
    destination: str
    branches: tuple[str, ...]
    expires: float


@dataclass(frozen=True)
class Policy:
    """What the environment opens to the agent and how it responds.

    Parameters
    ----------
    work : str
        Top directory of the primary copy of the work.
    writable : tuple[str, ...]
        Locations the agent may write.
    readable : tuple[str, ...]
        Locations the agent may read, besides the writable ones.
    protected : tuple[str, ...]
        Locations of STND.INSTR.3 that no action takes out of use.
    homes : tuple[str, ...]
        Directories whose direct children are home directories.
    configuration : tuple[str, ...]
        Locations of the configuration that enforces the outcomes.
    ledgers : tuple[str, ...]
        File names of ledgers.
    domains : tuple[str, ...]
        Network domains the agent may reach.
    search : bool
        Whether web search is a retrieval scope of the agent.
    tools : tuple[str, ...]
        Patterns of the tools of other servers the agent may call.
    store : str
        Directory of STND.DFLT.29, or empty where the work keeps none.
    secrets : tuple[str, ...]
        Files of the store that the agent may read and write.
    grants : tuple[Grant, ...]
        Remote writes that a standing authorization in force names by
        destination and kind (STND.HARN.29).
    responses : dict[str, str]
        Decision by outcome key, ``deny`` or ``ask``.
    unattended : bool
        Whether nobody is there to answer a referral.
    """

    work: str
    writable: tuple[str, ...]
    readable: tuple[str, ...]
    protected: tuple[str, ...]
    homes: tuple[str, ...]
    configuration: tuple[str, ...]
    ledgers: tuple[str, ...]
    domains: tuple[str, ...]
    search: bool
    tools: tuple[str, ...]
    store: str
    secrets: tuple[str, ...]
    grants: tuple[Grant, ...]
    responses: dict[str, str]
    unattended: bool


@dataclass
class Findings:
    """Outcomes that one call reaches, each with its reason.

    Parameters
    ----------
    reached : list[tuple[str, str]]
        Pairs of outcome key and reason, in the order found.
    permitted : list[tuple[str, str]]
        Remote writes that an authorization names, by reason and the
        authorization, kept only where the call is one plain command.
    """

    reached: list[tuple[str, str]] = field(default_factory=list)
    permitted: list[tuple[str, str]] = field(default_factory=list)

    def add(self, outcome: str, reason: str) -> None:
        """Record that the call reaches an outcome, once per reason.

        Parameters
        ----------
        outcome : str
            Key of the outcome.
        reason : str
            What in the call reaches it.
        """
        if (outcome, reason) not in self.reached:
            self.reached.append((outcome, reason))


@dataclass
class Scan:
    """What the reading of one shell command line knows so far.

    Parameters
    ----------
    policy : Policy
        The policy.
    found : Findings
        Receives the outcomes reached.
    cwds : list[str | None]
        Every directory the line may run in; None stands for one the
        guard cannot tell, which makes each relative path computed.
    home : str
        Home directory that ``~`` and ``$HOME`` name.
    assigned : set[str]
        Names of ``KNOWN_VARIABLES`` that the line sets, whose value the
        guard therefore does not know.
    bodies : list[str]
        Bodies of the line's here-documents, by the index of their mark.
    commands : int
        Simple commands read in this pass, nested ones included.
    bare : bool
        Whether the simple command being read has no assignment or
        reserved word before its program.
    permitted : list[tuple[str, str]]
        Remote writes an authorization names, by reason and the
        authorization; each stands only while the line holds no other
        command.
    """

    policy: Policy
    found: Findings
    cwds: list[str | None]
    home: str
    assigned: set[str] = field(default_factory=set)
    bodies: list[str] = field(default_factory=list)
    commands: int = 0
    bare: bool = True
    permitted: list[tuple[str, str]] = field(default_factory=list)


def read_policy(data: dict[str, Any]) -> Policy:
    """Build a policy from its JSON form.

    Parameters
    ----------
    data : dict[str, Any]
        The parsed policy file.

    Returns
    -------
    Policy
        The policy.

    Raises
    ------
    KeyError
        If a field is missing.
    ValueError
        If a list field is not a list of strings, the store is no
        string, ``remote_writes`` is no list, or a response is neither
        Refuse nor Refer. A malformed entry of ``remote_writes`` is left
        out, so that the write it would name is referred.
    """
    if not isinstance(data["store"], str):
        raise ValueError("policy field store is no string")
    if not isinstance(data["remote_writes"], list):
        raise ValueError("policy field remote_writes is no list")
    for name in POLICY_LISTS:
        values = data[name]
        if not isinstance(values, list) or not all(
            isinstance(v, str) for v in values
        ):
            raise ValueError(f"policy field {name} is no list of strings")
    responses = {}
    for key, response in data["responses"].items():
        if response not in RESPONSES:
            raise ValueError(f"unknown response {response!r} for {key}")
        responses[key] = RESPONSES[response]
    return Policy(
        work=str(data["work"]),
        writable=tuple(data["writable"]),
        readable=tuple(data["readable"]),
        protected=tuple(data["protected"]),
        homes=tuple(data["homes"]),
        configuration=tuple(data["configuration"]),
        ledgers=tuple(data["ledgers"]),
        domains=tuple(data["domains"]),
        search=bool(data["search"]),
        tools=tuple(data["tools"]),
        store=str(data["store"]),
        secrets=tuple(data["secrets"]),
        grants=tuple(
            g for g in map(read_grant, data["remote_writes"]) if g is not None
        ),
        responses=responses,
        unattended=bool(data["unattended"]),
    )


def read_grant(data: Any) -> Grant | None:
    """Return one entry of the policy's ``remote_writes``, if well formed.

    Parameters
    ----------
    data : Any
        The entry as the policy holds it.

    Returns
    -------
    Grant | None
        The grant; None for an entry of another form, an unknown kind, a
        ``commit`` without branches, or an expiry that is neither null
        (until revoked) nor a time with a UTC offset, so that the write
        it would name is referred.
    """
    if not isinstance(data, dict) or set(data) != GRANT_FIELDS:
        return None
    branches = data["branches"]
    if (
        data["kind"] not in GRANT_KINDS
        or not isinstance(data["authorization"], str)
        or not isinstance(data["destination"], str)
        or not data["destination"]
        or not isinstance(branches, list)
        or not all(isinstance(b, str) and b for b in branches)
        or (data["kind"] == "commit") != bool(branches)
        or not (data["expires"] is None or isinstance(data["expires"], str))
    ):
        return None
    if data["expires"] is None:
        # Until revoked: the revocation reaches the policy when the
        # configuration is derived again.
        return Grant(
            data["authorization"],
            data["kind"],
            data["destination"],
            tuple(branches),
            float("inf"),
        )
    try:
        expires = datetime.fromisoformat(data["expires"])
    except ValueError:
        return None
    if expires.utcoffset() is None:
        return None
    return Grant(
        data["authorization"],
        data["kind"],
        data["destination"],
        tuple(branches),
        expires.timestamp(),
    )


def granted(
    policy: Policy, kind: str, destination: str, branches: list[str]
) -> str | None:
    """Return the authorization that names a remote write, if one does.

    Parameters
    ----------
    policy : Policy
        The policy.
    kind : str
        ``commit`` or ``post``.
    destination : str
        The destination as the command names it.
    branches : list[str]
        Branches the write updates; empty for a post.

    Returns
    -------
    str | None
        The identifier of an authorization not yet expired whose kind
        and destination equal the write's, as whole strings, and that
        covers every branch; None otherwise.
    """
    now = time.time()
    for grant in policy.grants:
        if (
            grant.kind == kind
            and grant.destination == destination
            and set(branches) <= set(grant.branches)
            and now < grant.expires
        ):
            return grant.authorization
    return None


def normalize(path: str) -> str:
    """Return an absolute path with ``.`` and ``..`` resolved lexically.

    Parameters
    ----------
    path : str
        Absolute path.

    Returns
    -------
    str
        The path with one leading slash; POSIX keeps a leading ``//``,
        which names the same root here.
    """
    return "/" + os.path.normpath(path).lstrip("/")


def real_path(path: str) -> str:
    """Return the path a name leads to through symbolic links.

    Parameters
    ----------
    path : str
        Absolute, normalized path.

    Returns
    -------
    str
        The path with each existing symbolic link resolved, as it is
        when the guard runs. Device files keep their name, since a
        terminal or ``/dev/null`` resolves to a changing device.
    """
    return path if path.startswith("/dev/") else os.path.realpath(path)


def within(path: str, roots: tuple[str, ...]) -> bool:
    """Return whether a path is one of the roots or lies under one.

    Parameters
    ----------
    path : str
        Absolute, normalized path.
    roots : tuple[str, ...]
        Absolute, normalized locations.

    Returns
    -------
    bool
        Whether the path is inside a root.
    """
    return any(
        path == root or path.startswith(root.rstrip("/") + "/")
        for root in roots
    )


def secret_file(path: str, policy: Policy) -> bool:
    """Return whether a path is a file of the store not opened to the agent.

    Parameters
    ----------
    path : str
        Absolute, normalized path, with its links resolved.
    policy : Policy
        The policy.

    Returns
    -------
    bool
        Whether the path lies under the store and is no opened file; the
        directory itself, whose names hold no secret, is not one
        (STND.DFLT.29). The store and the opened files are compared
        where their links lead, as the path is.
    """
    if not policy.store:
        return False
    store = real_path(policy.store)
    opened = tuple(real_path(s) for s in policy.secrets)
    return (
        within(path, (store,))
        and path != store
        and not within(path, opened)
    )


def holds_secrets(path: str, policy: Policy) -> bool:
    """Return whether an action on a directory would reach a closed secret.

    Parameters
    ----------
    path : str
        Absolute, normalized directory that a search, copy, move, or
        removal takes whole, with its links resolved.
    policy : Policy
        The policy.

    Returns
    -------
    bool
        Whether the directory is the store or holds it, and the store
        holds an entry that is no opened file (STND.DFLT.31). A store
        that exists but cannot be listed counts as holding one.
    """
    if not policy.store:
        return False
    store = real_path(policy.store)
    if not within(store, (path,)):
        return False
    try:
        names = os.listdir(store)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return any(secret_file(real_path(f"{store}/{n}"), policy) for n in names)


def protected_target(path: str, policy: Policy) -> str | None:
    """Return the protected location an action on a path takes out of use.

    Parameters
    ----------
    path : str
        Absolute, normalized path that a removal or move names.
    policy : Policy
        The policy.

    Returns
    -------
    str | None
        The protected location that the path is, or holds, else None.
    """
    for location in policy.protected:
        if within(location, (path,)):
            return location
    for parent in policy.homes:
        if path == parent or str(PurePosixPath(path).parent) == parent:
            return path
    return None


def lift_heredocs(text: str, bodies: list[str]) -> str:
    """Replace each here-document by a here-string that names its body.

    The lines after ``cmd <<EOF``, up to the line ``EOF``, are data for
    the command, not commands, unless the command is a shell. Each
    operator becomes ``<<< MARK n MARK`` and its body goes to
    ``bodies[n]``, so that a shell's body is read as a here-string's
    text would be. A ``<<`` that is quoted, in a comment, in ``${...}``,
    or in arithmetic is no operator and stays. Where the reading could
    differ from the shell's, the lines stay and are read as commands:
    a body whose end line never comes is read as commands too.

    Parameters
    ----------
    text : str
        A shell command line.
    bodies : list[str]
        Receives each body.

    Returns
    -------
    str
        The line without the bodies.
    """
    out: list[str] = []
    pending: list[tuple[str, bool, int]] = []
    # Open contexts: quotes ' " $', "{" for ${, "(" for a group in
    # which a here-document may start, "#(" for arithmetic.
    stack: list[str] = []
    index = 0
    while index < len(text):
        char = text[index]
        context = stack[-1] if stack else ""
        if context == "'":
            if char == "'":
                stack.pop()
            out.append(char)
            index += 1
            continue
        if char == "\\":
            out.append(text[index : index + 2])
            index += 2
            continue
        if context in {'"', "$'"}:
            if char == ("'" if context == "$'" else '"'):
                stack.pop()
            elif context == '"' and text.startswith("$(", index):
                opened = "#(" if text.startswith("$((", index) else "("
                stack.append(opened)
                out.append("$(")
                index += 2
                continue
            elif context == '"' and text.startswith("${", index):
                stack.append("{")
            out.append(char)
            index += 1
            continue
        arithmetic = context in {"#(", "{"}
        match = None
        if char == "<" and not arithmetic:
            match = DELIMITER_RE.match(text, index)
        if text.startswith("<<<", index):
            step = 3
        elif text.startswith(("$((", "(("), index):
            stack += ["#(", "#("]
            step = 3 if char == "$" else 2
        elif text.startswith("$'", index):
            stack.append("$'")
            step = 2
        elif text.startswith("${", index):
            stack.append("{")
            step = 2
        elif char in {"'", '"'}:
            stack.append(char)
            step = 1
        elif char == "(":
            stack.append("#(" if arithmetic else "(")
            step = 1
        elif char == ")" and context in {"(", "#("}:
            stack.pop()
            step = 1
        elif char == "}" and context == "{":
            stack.pop()
            step = 1
        elif char == "#" and (index == 0 or text[index - 1] in " \t\n;&|("):
            end = text.find("\n", index)
            step = (len(text) if end < 0 else end) - index
        elif match:
            delimiter = re.sub(r"""['"]|\\(?=.)""", "", match.group(2))
            pending.append((delimiter, match.group(1) == "-", len(bodies)))
            bodies.append("")
            out.append(f"<<< {MARK}{len(bodies) - 1}{MARK}")
            index = match.end()
            continue
        elif char == "\n" and pending:
            out.append(char)
            index = read_bodies(text, index + 1, pending, bodies, out)
            pending = []
            continue
        else:
            step = 1
        out.append(text[index : index + step])
        index += step
    return "".join(out)


def read_bodies(
    text: str,
    index: int,
    pending: list[tuple[str, bool, int]],
    bodies: list[str],
    out: list[str],
) -> int:
    """Move the bodies of the pending here-documents out of a line.

    Parameters
    ----------
    text : str
        The command line.
    index : int
        Position of the first body line.
    pending : list[tuple[str, bool, int]]
        Delimiter, whether leading tabs are stripped, and body index of
        each here-document whose body starts here, in order.
    bodies : list[str]
        Receives each body.
    out : list[str]
        Receives the text of a body whose end line never comes, so that
        it is read as commands too.

    Returns
    -------
    int
        Position after the last end line.
    """
    for delimiter, strip_tabs, slot in pending:
        lines: list[str] = []
        while index < len(text):
            end = text.find("\n", index)
            end = len(text) if end < 0 else end
            line = text[index:end]
            index = end + 1
            if (line.lstrip("\t") if strip_tabs else line) == delimiter:
                break
            lines.append(line)
        else:
            out.append("\n".join(lines))
        bodies[slot] = "\n".join(lines)
    return index


def split_commands(line: str) -> list[tuple[list[str], bool]]:
    """Split a shell command line into its simple commands.

    Every run of operator characters that is no redirection separates
    commands, so that ``(``, ``<(``, ``>(``, ``((``, ``;;``, and ``|&``
    each start a new one.

    Parameters
    ----------
    line : str
        The command line, here-documents lifted.

    Returns
    -------
    list[tuple[list[str], bool]]
        Words of each simple command, separators removed, and whether a
        pipe feeds it.

    Raises
    ------
    ValueError
        If the line does not tokenize, such as an unclosed quote.
    """
    lexer = shlex.shlex(line, posix=True, punctuation_chars=PUNCTUATION)
    lexer.whitespace_split = True
    lexer.whitespace = " \t\r"
    commands: list[tuple[list[str], bool]] = [([], False)]
    for token in lexer:
        if token and set(token) <= set(PUNCTUATION) and token not in REDIRECTS:
            commands.append(([], token in {"|", "|&"}))
            continue
        # Newlines are left in tokens so that quoted ones survive; an
        # unquoted newline separates commands as ";" does.
        first, *rest = token.split("\n")
        commands[-1][0].append(first)
        commands.extend(([part], False) for part in rest)
    return [
        ([w for w in words if w], piped)
        for words, piped in commands
        if any(words)
    ]


def strip_redirections(
    words: list[str],
) -> tuple[list[str], list[tuple[str, str]]]:
    """Separate the redirections of a simple command from its words.

    Parameters
    ----------
    words : list[str]
        Words of one simple command.

    Returns
    -------
    tuple[list[str], list[tuple[str, str]]]
        The remaining words, and each redirection as (operator, target).
        A number just before an operator is its file descriptor, as in
        ``2>/dev/null``, and is dropped.
    """
    kept: list[str] = []
    redirections: list[tuple[str, str]] = []
    index = 0
    while index < len(words):
        word = words[index]
        if word in REDIRECTS:
            if kept and kept[-1].isdigit():
                kept.pop()
            target = words[index + 1] if index + 1 < len(words) else ""
            redirections.append((word, target))
            index += 2
            continue
        kept.append(word)
        index += 1
    return kept, redirections


def program_words(words: list[str]) -> list[str]:
    """Drop assignments and reserved words in front of the program.

    Parameters
    ----------
    words : list[str]
        Words of one simple command, redirections removed.

    Returns
    -------
    list[str]
        The words from the program name on.
    """
    index = 0
    while index < len(words) and (
        words[index] in KEYWORDS
        or re.match(r"^[A-Za-z_][A-Za-z0-9_]*\+?=", words[index])
    ):
        index += 1
    return words[index:]


def operands(words: list[str]) -> list[str]:
    """Return the arguments of a program that are not options.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.

    Returns
    -------
    list[str]
        Every argument after the name that does not start with ``-``,
        and every argument after ``--``.
    """
    found: list[str] = []
    ended = False
    for word in words[1:]:
        if ended or not word.startswith("-") or word == "-":
            found.append(word)
        elif word == "--":
            ended = True
    return found


def short_flags(words: list[str]) -> set[str]:
    """Return every single-letter flag of a program's arguments.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.

    Returns
    -------
    set[str]
        Letters of the arguments of the form ``-abc``.
    """
    letters: set[str] = set()
    for word in words[1:]:
        if word == "--":
            break
        if word.startswith("-") and not word.startswith("--"):
            letters |= set(word[1:])
    return letters


def long_flag(words: list[str], *names: str) -> bool:
    """Return whether an argument is one of the long options named.

    GNU and git options may be abbreviated to any unambiguous prefix,
    as ``--rec`` for ``--recursive``, so a prefix of three characters
    or more counts.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    *names : str
        Long options, such as ``--force``.

    Returns
    -------
    bool
        Whether an argument before ``--`` is a prefix of one of them.
    """
    for word in words[1:]:
        if word == "--":
            break
        stem = word.split("=", 1)[0]
        if stem.startswith("--") and len(stem) > 2:
            if any(name.startswith(stem) for name in names):
                return True
    return False


def has_glob(word: str) -> bool:
    """Return whether a word is a shell pattern.

    Parameters
    ----------
    word : str
        One word.

    Returns
    -------
    bool
        Whether it holds a wildcard character.
    """
    return bool(GLOB_CHARS & set(word))


def pattern_base(pattern: str) -> str:
    """Return the directory of an absolute pattern before its wildcard.

    Parameters
    ----------
    pattern : str
        An absolute shell pattern.

    Returns
    -------
    str
        The deepest directory that holds every item the pattern selects.
    """
    head = pattern[: min(pattern.index(c) for c in GLOB_CHARS if c in pattern)]
    return head.rsplit("/", 1)[0] or "/"


def expand_braces(word: str) -> list[str] | None:
    """Return the words a brace expansion produces.

    Parameters
    ----------
    word : str
        One word.

    Returns
    -------
    list[str] | None
        Each word ``{a,b}`` produces; a sequence such as ``{1..9}``
        becomes the wildcard ``*``. None when more than
        ``MAX_EXPANSION`` words result.
    """
    todo, done = [word], []
    while todo:
        current = todo.pop()
        span = brace_span(current)
        if span is None:
            done.append(current)
        else:
            start, end, parts = span
            todo += [current[:start] + p + current[end + 1 :] for p in parts]
        if len(todo) + len(done) > MAX_EXPANSION:
            return None
    return done


def brace_span(word: str) -> tuple[int, int, list[str]] | None:
    """Return the first brace expression of a word that expands.

    Parameters
    ----------
    word : str
        One word.

    Returns
    -------
    tuple[int, int, list[str]] | None
        Positions of ``{`` and its ``}``, and the alternatives; None
        when no brace expands. ``${`` opens a parameter, not a brace.
    """
    for start, char in enumerate(word):
        if char != "{" or word[start - 1 : start] == "$":
            continue
        depth, parts, piece = 0, [], start + 1
        for end in range(start + 1, len(word)):
            if word[end] == "{":
                depth += 1
            elif word[end] == "}" and depth:
                depth -= 1
            elif word[end] == "," and not depth:
                parts.append(word[piece:end])
                piece = end + 1
            elif word[end] == "}":
                inside = word[start + 1 : end]
                if parts:
                    return start, end, [*parts, word[piece:end]]
                if re.fullmatch(r"-?\w+\.\.-?\w+(\.\.-?\d+)?", inside):
                    return start, end, ["*"]
                break
    return None


def expand_known(word: str, scan: Scan) -> list[str] | None:
    """Expand the tilde and the variables whose value the guard knows.

    Parameters
    ----------
    word : str
        One word, braces expanded.
    scan : Scan
        The reading so far.

    Returns
    -------
    list[str] | None
        The word for each directory the line may run in; None when the
        word depends on a value the guard does not know.
    """
    if word == "~-" or word.startswith("~-/"):
        return None
    if word == "~+" or word.startswith("~+/"):
        words = [f"$PWD{word[2:]}"]
    elif word == "~" or word.startswith("~/"):
        words = [f"$HOME{word[1:]}"]
    elif word.startswith("~"):
        words = [os.path.expanduser(word)]
    else:
        words = [word]
    for name in KNOWN_VARIABLES:
        pattern = re.compile(rf"\$(?:\{{{name}\}}|{name}(?!\w))")
        if not any(pattern.search(w) for w in words):
            continue
        values = scan.cwds if name == "PWD" else [scan.home]
        if name in scan.assigned or None in values:
            return None
        words = [
            pattern.sub(lambda _: str(value), w)
            for w in words
            for value in values
        ]
    return words


def computed(word: str, scan: Scan) -> bool:
    """Return whether a word holds a value the guard does not know.

    Parameters
    ----------
    word : str
        One word, such as a program name.
    scan : Scan
        The reading so far.

    Returns
    -------
    bool
        Whether a substitution or a variable other than a known one
        remains once the known ones are expanded.
    """
    if "`" in word or "$(" in word:
        return True
    expanded = expand_known(word, scan)
    return expanded is None or any("$" in w for w in expanded)


def resolve(word: str, scan: Scan) -> list[str] | None:
    """Return every absolute path an operand may name.

    Parameters
    ----------
    word : str
        The operand as the line gives it, quotes removed.
    scan : Scan
        The reading so far.

    Returns
    -------
    list[str] | None
        Normalized paths, which may be patterns; None when the operand
        is computed: it holds a value the guard does not know, such as
        a variable, a substitution, or the ``{}`` of ``find``.
    """
    if "{}" in word or "`" in word or "$(" in word:
        return None
    alternatives = expand_braces(word)
    if alternatives is None:
        return None
    paths: list[str] = []
    for alternative in alternatives:
        expanded = expand_known(alternative, scan)
        if expanded is None:
            return None
        for text in expanded:
            if "$" in text:
                return None
            if text.startswith("/"):
                paths.append(normalize(text))
                continue
            for cwd in scan.cwds:
                if cwd is None:
                    return None
                paths.append(normalize(f"{cwd}/{text}"))
    return paths


def target_split(words: list[str], args: list[str]) -> tuple[list[str], str]:
    """Split the operands of a copy or move into sources and destination.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    args : list[str]
        Its operands.

    Returns
    -------
    tuple[list[str], str]
        The sources and the destination; ``-t DIR`` and
        ``--target-directory=DIR`` name the destination, and otherwise
        it is the last operand. The destination is empty when there is
        none.
    """
    for index, word in enumerate(words[1:], start=1):
        if word == "--":
            break
        if word.startswith("--target-directory"):
            value = word.partition("=")[2]
            if not value and index + 1 < len(words):
                value = words[index + 1]
            return [a for a in args if a != value], value
        if word.startswith("-") and not word.startswith("--") and "t" in word:
            value = word[word.index("t") + 1 :]
            if not value and index + 1 < len(words):
                value = words[index + 1]
            return [a for a in args if a != value], value
    return args[:-1], (args[-1] if args else "")


def check_removal(
    targets: list[str], scan: Scan, directories: bool = True
) -> None:
    """Check the items that a removal or move names.

    Parameters
    ----------
    targets : list[str]
        Operands naming the items.
    scan : Scan
        The reading so far.
    directories : bool
        Whether the action can take a directory out of use; ``rm``
        without recursion removes files alone.
    """
    found = scan.found
    for target in targets:
        paths = resolve(target, scan)
        if paths is None:
            found.add("selective-destruction", f"computed item {target}")
            continue
        for path in paths:
            if has_glob(path):
                check_pattern(path, scan, directories)
                continue
            location = protected_target(path, scan.policy)
            location = location or protected_target(
                real_path(path), scan.policy
            )
            if location:
                found.add(
                    "protected-locations", f"takes {location} out of use"
                )
            check_written(path, scan.policy, found)
            if holds_secrets(real_path(path), scan.policy):
                reason = f"moves or removes the store: {path}"
                found.add("write-bounds", reason)


def check_pattern(pattern: str, scan: Scan, directories: bool) -> None:
    """Check a removal or move whose items a pattern selects.

    Parameters
    ----------
    pattern : str
        Absolute, normalized pattern.
    scan : Scan
        The reading so far.
    directories : bool
        Whether the action can take a directory out of use.
    """
    policy, found = scan.policy, scan.found
    found.add("selective-destruction", f"pattern {pattern}")
    base = pattern_base(pattern)
    rest = re.sub(r"\[[^]]*\]", "", pattern[len(base) :])
    for location in policy.protected:
        names = [location, *map(str, PurePosixPath(location).parents)]
        if any(fnmatch.fnmatchcase(name, pattern) for name in names):
            found.add("protected-locations", f"takes {location} out of use")
    location = protected_target(base, policy)
    # A pattern of wildcards alone, such as "*" or ".*", selects every
    # item of its directory.
    if directories and location == base and not re.search(r"\w", rest):
        found.add("protected-locations", f"empties {location}")
    if any(
        fnmatch.fnmatchcase(ledger, PurePosixPath(pattern).name)
        for ledger in policy.ledgers
    ):
        found.add("record-entries", f"pattern {pattern} selects a ledger")
    check_written(base, policy, found)
    if holds_secrets(real_path(base), policy):
        found.add("write-bounds", f"pattern {pattern} selects the store")


def check_written(path: str, policy: Policy, found: Findings) -> None:
    """Check one path that an action changes or removes.

    Parameters
    ----------
    path : str
        Absolute, normalized path.
    policy : Policy
        The policy.
    found : Findings
        Receives the outcomes reached.
    """
    real = real_path(path)
    for name in {path, real}:
        if within(name, policy.configuration):
            found.add("enforcing-configuration", f"changes {name}")
        if ".git" in PurePosixPath(name).parts:
            # Only git itself writes its metadata: a direct write can
            # move a ref, add a hook, or plant a configuration.
            found.add("history-rewrite", f"writes version-control {name}")
        if PurePosixPath(name).name in policy.ledgers:
            found.add("record-entries", f"changes or removes ledger {name}")
    # The write lands where the links lead.
    if not within(real, policy.writable):
        found.add("write-bounds", f"writes {real}")
    elif secret_file(real, policy):
        found.add("write-bounds", f"writes secret store file {real}")


def check_read(path: str, policy: Policy, found: Findings) -> None:
    """Check one path that an action reads.

    Parameters
    ----------
    path : str
        Absolute, normalized path.
    policy : Policy
        The policy.
    found : Findings
        Receives the outcomes reached.
    """
    real = real_path(path)
    if not within(real, policy.readable + policy.writable):
        found.add("read-bounds", f"reads {real}")
    elif secret_file(real, policy):
        found.add("read-bounds", f"reads secret store file {real}")


def check_writes(targets: list[str], scan: Scan, append: bool) -> None:
    """Check the operands or redirection targets that a command writes.

    Parameters
    ----------
    targets : list[str]
        Operands as the line gives them.
    scan : Scan
        The reading so far.
    append : bool
        Whether the command only appends, which adds to a ledger and
        changes no entry.
    """
    for target in targets:
        paths = resolve(target, scan)
        if paths is None:
            scan.found.add(
                "selective-destruction", f"writes computed {target}"
            )
            continue
        for path in paths:
            if not append:
                check_written(path, scan.policy, scan.found)
                continue
            real = real_path(path)
            if within(path, scan.policy.configuration):
                scan.found.add("enforcing-configuration", f"changes {path}")
            if any(".git" in PurePosixPath(n).parts for n in (path, real)):
                # An appended line still adds a setting or a hook.
                scan.found.add("history-rewrite", f"writes version-control {path}")
            if not within(real, scan.policy.writable):
                scan.found.add("write-bounds", f"writes {real}")
            elif secret_file(real, scan.policy):
                scan.found.add(
                    "write-bounds", f"writes secret store file {real}"
                )


def check_reads(targets: list[str], scan: Scan) -> None:
    """Check the operands that a command reads.

    Parameters
    ----------
    targets : list[str]
        Operands as the line gives them; a computed one is left to the
        sandbox, since a read changes nothing.
    scan : Scan
        The reading so far.
    """
    for target in targets:
        for path in resolve(target, scan) or []:
            check_read(path, scan.policy, scan.found)


def check_copied(sources: list[str], scan: Scan) -> None:
    """Check the sources of a copy for a directory that holds the store.

    Parameters
    ----------
    sources : list[str]
        Operands as the line gives them; a computed one is left to the
        sandbox, as for other reads.
    scan : Scan
        The reading so far.
    """
    for source in sources:
        for path in resolve(source, scan) or []:
            if holds_secrets(real_path(path), scan.policy):
                scan.found.add("read-bounds", f"copies the store: {path}")


def dry_run(sub: str, args: list[str]) -> bool:
    """Return whether a git subcommand runs as a dry run, read strictly.

    Parameters
    ----------
    sub : str
        The subcommand, such as ``push`` or ``clean``.
    args : list[str]
        Its arguments.

    Returns
    -------
    bool
        Whether ``-n`` or ``--dry-run`` is an argument of its own, and,
        so that no option's value is misread as the flag, every other
        option is one that takes no value: for ``push``, one of
        ``PUSH_OPTIONS``; for another subcommand, any option that is not
        one of ``DRY_VALUED`` and holds no ``=``. Before ``--`` only.
    """
    words = args[: args.index("--")] if "--" in args else args
    if not {"-n", "--dry-run"} & set(words):
        return False
    for word in words:
        if not word.startswith("-") or word in {"-n", "--dry-run"}:
            continue
        if sub == "push" and word not in PUSH_OPTIONS:
            return False
        if "=" in word or word in DRY_VALUED or any(
            word.startswith(v) and not v.startswith("--") for v in DRY_VALUED
        ):
            return False
    return True


def check_git(words: list[str], scan: Scan) -> None:
    """Check one git command.

    Parameters
    ----------
    words : list[str]
        ``git`` and its arguments.
    scan : Scan
        The reading so far. A ``-c`` value is read as a command line,
        since an alias that starts with ``!`` or a setting such as
        ``core.pager`` runs one; ``-C`` adds a directory.
    """
    found = scan.found
    bare = scan.bare
    rest = words[1:]
    options: list[str] = []
    while rest and rest[0].startswith("-"):
        option = rest[0]
        options.append(option)
        takes_value = option in GIT_VALUED
        value = rest[1] if takes_value and len(rest) > 1 else ""
        rest = rest[2:] if takes_value else rest[1:]
        if option == "-c":
            check_line(value.partition("=")[2].lstrip("!"), scan, False)
        elif option == "-C":
            enter_directory(value, scan)
    if not rest:
        return
    sub, args = rest[0], rest[1:]
    command = ["git", *args]
    flags = set(args)
    letters = short_flags(command)
    dry = dry_run(sub, args)
    if sub == "push" and not dry:
        forced = long_flag(
            command,
            "--force",
            "--force-with-lease",
            "--force-if-includes",
            "--mirror",
            "--delete",
            "--prune",
        ) or any(a.startswith(("+", ":")) for a in operands(command))
        if forced or {"f", "d"} & letters:
            found.add("history-rewrite", "forced or deleting push")
        grant, reason = push_grant(words[0], options, args, scan, bare)
        if grant is None:
            found.add("remote-write", reason)
        else:
            scan.permitted.append((reason, grant))
    elif sub in HISTORY_REWRITES | {"update-ref"}:
        found.add("history-rewrite", f"git {sub}")
    elif sub == "commit" and long_flag(command, "--amend"):
        found.add("history-rewrite", "git commit --amend")
    elif sub == "reflog" and flags & {"expire", "delete"}:
        found.add("history-rewrite", "git reflog expire or delete")
    elif sub == "branch" and (
        {"D", "f", "M", "C"} & letters or long_flag(command, "--force")
    ):
        found.add("history-rewrite", "forced branch change")
    elif sub == "tag" and (
        {"f", "d"} & letters or long_flag(command, "--force", "--delete")
    ):
        found.add("history-rewrite", "tag moved or deleted")
    elif (sub == "checkout" and "B" in letters) or (
        sub == "switch"
        and ("C" in letters or long_flag(command, "--force-create"))
    ):
        found.add("history-rewrite", f"git {sub} resets a branch")
    elif sub in {"gc", "prune"} and (
        sub == "prune" or long_flag(command, "--prune")
    ):
        found.add("history-rewrite", f"git {sub} pruning")
    elif sub == "reset" and long_flag(command, "--hard"):
        found.add("selective-destruction", "git reset --hard")
    elif sub == "clean" and not dry:
        found.add("selective-destruction", "git clean")
    elif sub == "stash" and flags & {"drop", "clear"}:
        found.add("selective-destruction", "git stash drop or clear")
    elif (sub == "checkout" and flags & {"--", "."}) or (
        sub == "restore" and "--staged" not in flags
    ):
        found.add("selective-destruction", f"git {sub} overwrites files")
    elif sub == "rm" and not dry and not long_flag(command, "--cached"):
        recursive = "r" in letters
        if recursive:
            found.add("selective-destruction", "recursive removal")
        check_removal(operands(command), scan, directories=recursive)
    elif sub == "mv" and not dry:
        sources, destination = target_split(command, operands(command))
        check_removal(sources, scan)
        check_writes([destination] if destination else [], scan, False)


def check_find(words: list[str], scan: Scan) -> None:
    """Check one find command.

    Parameters
    ----------
    words : list[str]
        ``find`` and its arguments; a ``;`` ending an ``-exec`` has
        already ended the command.
    scan : Scan
        The reading so far.
    """
    roots = []
    for word in words[1:]:
        if word.startswith(("-", "(", "!")):
            break
        roots.append(word)
    deletes = "-delete" in words
    for index, word in enumerate(words):
        if word in {"-exec", "-execdir", "-ok", "-okdir"}:
            segment = words[index + 1 :]
            if "+" in segment:
                segment = segment[: segment.index("+")]
            if segment and PurePosixPath(segment[0]).name in REMOVERS | {
                "mv"
            }:
                deletes = True
            if segment:
                check_simple(segment, False, scan)
    for root in roots or ["."]:
        paths = resolve(root, scan)
        if paths is None:
            if deletes:
                scan.found.add("selective-destruction", f"computed {root}")
            continue
        for path in paths:
            if not deletes:
                check_read(path, scan.policy, scan.found)
                continue
            location = protected_target(path, scan.policy)
            if location:
                scan.found.add(
                    "protected-locations", f"removes within {location}"
                )
            check_written(path, scan.policy, scan.found)
    if deletes:
        scan.found.add("selective-destruction", "find selects items to remove")


def check_remote(words: list[str], scan: Scan) -> None:
    """Check one command for a write to a remote system.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    scan : Scan
        The reading so far; receives the outcomes reached.
    """
    found = scan.found
    bare = scan.bare
    name = PurePosixPath(words[0]).name
    args = words[1:]
    if name in REMOTE_COPIERS:
        found.add("remote-write", name)
    elif name == "ssh" and len(operands(words)) > 1:
        found.add("remote-write", "command run on a remote system")
    elif name == "rsync" and any(
        ":" in a and not a.startswith("-") for a in args[-1:]
    ):
        found.add("remote-write", "rsync to a remote system")
    elif name == "curl" and (
        any(a.split("=")[0] in CURL_WRITES for a in args)
        or any(
            a in {"-X", "--request"}
            and index + 1 < len(args)
            and args[index + 1].upper() not in {"GET", "HEAD"}
            for index, a in enumerate(args)
        )
    ):
        found.add("remote-write", "curl sends data or a writing method")
    elif name == "wget" and any(
        a.startswith(("--post", "--method", "--body")) for a in args
    ):
        found.add("remote-write", "wget sends data")
    elif name == "gh" and args and args[0].startswith("-") and args[1:]:
        found.add("remote-write", "gh with an option before its command")
    elif name == "gh" and len(args) >= 2 and args[0] in GH_WRITES:
        if args[1].startswith("-"):
            found.add("remote-write", f"gh {args[0]} with an option first")
        elif args[1] in GH_WRITES[args[0]]:
            grant, reason = post_grant(words[0], args, scan, bare)
            if grant is None:
                found.add("remote-write", reason)
            else:
                scan.permitted.append((reason, grant))
    elif name == "gh" and len(args) >= 2 and args[0] == "api":
        found.add("remote-write", f"gh {args[0]} {args[1]}")
    elif name in PUBLISHERS and set(args) & PUBLISHERS[name]:
        found.add("remote-write", f"{name} publishes")


def git_value(raw: str) -> str:
    """Return a value of a git configuration line as git reads it.

    Parameters
    ----------
    raw : str
        The text after ``=``, leading blanks removed.

    Returns
    -------
    str
        The value: quotes removed, escapes read, a comment outside
        quotes dropped, and unquoted blanks at its end trimmed.

    Raises
    ------
    ValueError
        If the value continues on the next line, holds an unknown escape,
        or leaves a quote open.
    """
    escapes = {"n": "\n", "t": "\t", "b": "\b", "\\": "\\", '"': '"'}
    out: list[tuple[str, bool]] = []
    quoted = False
    index = 0
    while index < len(raw):
        char = raw[index]
        if char == "\\":
            following = raw[index + 1 : index + 2]
            if following not in escapes:
                raise ValueError("a continued line or an unknown escape")
            out.append((escapes[following], True))
            index += 2
            continue
        if char == '"':
            quoted = not quoted
        elif char in "#;" and not quoted:
            break
        else:
            out.append((char, quoted))
        index += 1
    if quoted:
        raise ValueError("an open quote")
    while out and out[-1][0] in " \t" and not out[-1][1]:
        out.pop()
    return "".join(char for char, _ in out)


def git_values(text: str) -> list[tuple[str, str, str, str]]:
    """Return every value of a git configuration file.

    Parameters
    ----------
    text : str
        The file's text.

    Returns
    -------
    list[tuple[str, str, str, str]]
        Section and key in lower case, subsection as written (in lower
        case for the old form ``[section.sub]``), and value; a key with
        no ``=`` is true.

    Raises
    ------
    ValueError
        If a line is of a form this reading does not know, such as a key
        on the line of its section, so that the push is referred.
    """
    found: list[tuple[str, str, str, str]] = []
    section = subsection = ""
    for raw in text.split("\n"):
        line = raw.strip()
        if not line or line[0] in "#;":
            continue
        heading = GIT_SECTION_RE.fullmatch(line)
        if heading:
            name, quoted = heading.group(1), heading.group(2)
            if quoted is not None:
                section = name.lower()
                subsection = re.sub(r"\\(.)", r"\1", quoted)
            else:
                section, _, subsection = name.lower().partition(".")
            continue
        entry = GIT_KEY_RE.fullmatch(line)
        if entry is None or not section:
            raise ValueError(f"unreadable git configuration line {line!r}")
        value = entry.group(2)
        found.append(
            (
                section,
                subsection,
                entry.group(1).lower(),
                "true" if value is None else git_value(value),
            )
        )
    return found


def read_small(path: str) -> str | None:
    """Return a small file's text, or None where it does not exist.

    Parameters
    ----------
    path : str
        Absolute path.

    Returns
    -------
    str | None
        The text, up to a million characters; None for a missing file.

    Raises
    ------
    OSError
        If the file exists but cannot be read.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read(1_000_000)
    except FileNotFoundError:
        return None


def work_repository(cwd: str, policy: Policy) -> tuple[str, str] | None:
    """Return the git and common directories of the work's repository.

    Parameters
    ----------
    cwd : str
        Absolute directory the command runs in.
    policy : Policy
        The policy.

    Returns
    -------
    tuple[str, str] | None
        The git directory and the common directory, where the command
        runs inside the work, by the paths its links lead to, the first
        ``.git`` entry at or above it is the work's own, and that entry
        is a valid git directory or the ``gitdir:`` file of a linked
        worktree whose directories are valid. None otherwise, so that
        the push is referred: a ``.git`` nearer the command, which git
        may or may not take, is never read in place of the work's.

    Raises
    ------
    OSError
        If a ``.git`` file or ``commondir`` exists but cannot be read.
    """
    work = os.path.realpath(policy.work)
    path = os.path.realpath(cwd)
    if not within(path, (work,)):
        return None
    while path != work:
        if os.path.lexists(f"{path}/.git"):
            return None
        path = str(PurePosixPath(path).parent)
    dot = f"{work}/.git"
    if os.path.isdir(dot) and not os.path.islink(dot):
        gitdir = dot
    elif os.path.isfile(dot) and not os.path.islink(dot):
        text = read_small(dot) or ""
        if not text.startswith("gitdir: "):
            return None
        target = text[len("gitdir: ") :].strip()
        gitdir = os.path.realpath(
            target if target.startswith("/") else f"{work}/{target}"
        )
    else:
        return None
    common = gitdir
    text = read_small(f"{gitdir}/commondir")
    if text is not None:
        target = text.strip()
        common = os.path.realpath(
            target if target.startswith("/") else f"{gitdir}/{target}"
        )
    valid = (
        os.path.isfile(f"{gitdir}/HEAD")
        and os.path.isdir(f"{common}/objects")
        and os.path.isdir(f"{common}/refs")
    )
    return (gitdir, common) if valid else None


def git_configuration(
    dirs: tuple[str, str], home: str
) -> list[tuple[str, str, str, str]]:
    """Return the values of every git configuration file a push reads.

    Parameters
    ----------
    dirs : tuple[str, str]
        The git directory and the common directory.
    home : str
        The account's home directory.

    Returns
    -------
    list[tuple[str, str, str, str]]
        Values of the repository's, the worktree's, the account's, and
        the system's files, as ``git_values`` gives them.

    Raises
    ------
    OSError
        If a file exists but cannot be read.
    ValueError
        If a file holds a line this reading does not know.
    """
    gitdir, common = dirs
    xdg = os.environ.get("XDG_CONFIG_HOME") or f"{home}/.config"
    values: list[tuple[str, str, str, str]] = []
    for path in (
        f"{common}/config",
        f"{gitdir}/config.worktree",
        f"{home}/.gitconfig",
        f"{xdg}/git/config",
        GIT_SYSTEM_CONFIG,
    ):
        text = read_small(path)
        if text is not None:
            values += git_values(text)
    return values


def hooks_present(dirs: tuple[str, str]) -> bool:
    """Return whether the repository holds a hook that git may run.

    Parameters
    ----------
    dirs : tuple[str, str]
        The git directory and the common directory.

    Returns
    -------
    bool
        Whether a ``hooks`` directory of either holds an entry other
        than a ``.sample`` file; one that cannot be listed counts.
    """
    for folder in {f"{dirs[0]}/hooks", f"{dirs[1]}/hooks"}:
        try:
            names = os.listdir(folder)
        except FileNotFoundError:
            continue
        except OSError:
            return True
        if any(not name.endswith(".sample") for name in names):
            return True
    return False


def ref_exists(dirs: tuple[str, str], ref: str) -> bool:
    """Return whether the repository holds a ref, loose or packed.

    Parameters
    ----------
    dirs : tuple[str, str]
        The git directory and the common directory.
    ref : str
        A full ref name, such as ``refs/heads/main``.

    Returns
    -------
    bool
        Whether it is a loose ref of either directory or a line of the
        packed refs; packed refs that cannot be read count as holding it.
    """
    if any(os.path.lexists(f"{d}/{ref}") for d in dirs):
        return True
    try:
        text = read_small(f"{dirs[1]}/packed-refs") or ""
    except OSError:
        return True
    return any(line.endswith(f" {ref}") for line in text.split("\n"))


def branch_source(dirs: tuple[str, str], name: str) -> bool:
    """Return whether a short source name is a local branch alone.

    Parameters
    ----------
    dirs : tuple[str, str]
        The git directory and the common directory.
    name : str
        A short ref name.

    Returns
    -------
    bool
        Whether ``refs/heads/NAME`` exists and no other ref that git
        tries for a short name does (``refs/NAME``, a tag, a remote, or a
        remote's ``HEAD``), so that the push sends that branch.
    """
    others = (
        f"refs/{name}",
        f"refs/tags/{name}",
        f"refs/remotes/{name}",
        f"refs/remotes/{name}/HEAD",
    )
    return ref_exists(dirs, f"refs/heads/{name}") and not any(
        ref_exists(dirs, ref) for ref in others
    )


def short_ref(name: str) -> bool:
    """Return whether a name is a plain branch name.

    Parameters
    ----------
    name : str
        A name without ``refs/``.

    Returns
    -------
    bool
        Whether each part between slashes is of the plain form.
    """
    return bool(name) and all(
        REMOTE_NAME_RE.fullmatch(part) and ".." not in part
        for part in name.split("/")
    )


def push_branches(
    refspecs: list[str], dirs: tuple[str, str]
) -> tuple[list[str], str]:
    """Return the branches a push's refspecs update, or why it is unclear.

    Parameters
    ----------
    refspecs : list[str]
        The refspecs, at least one.
    dirs : tuple[str, str]
        The git directory and the common directory.

    Returns
    -------
    tuple[list[str], str]
        The branch names and an empty reason; or no branch and the
        reason. A refspec is read only in the forms ``NAME``,
        ``SOURCE:NAME``, and ``SOURCE:refs/heads/NAME``, where a short
        ``NAME`` is a local branch and no other local ref of that name,
        and ``SOURCE`` is ``HEAD``, ``refs/heads/B``, or a short branch
        name of the same kind.
    """
    branches: list[str] = []
    for spec in refspecs:
        source, colon, target = spec.partition(":")
        if not colon:
            if not short_ref(source) or not branch_source(dirs, source):
                return [], f"refspec {spec} is no local branch alone"
            branches.append(source)
            continue
        if source == "HEAD":
            pass
        elif source.startswith("refs/heads/"):
            if not short_ref(source[len("refs/heads/") :]) or not ref_exists(
                dirs, source
            ):
                return [], f"refspec {spec} has no local branch for source"
        elif not short_ref(source) or not branch_source(dirs, source):
            return [], f"refspec {spec} has no local branch for source"
        if target.startswith("refs/heads/"):
            branch = target[len("refs/heads/") :]
        else:
            branch = target
            if not short_ref(branch) or any(
                ref_exists(dirs, ref)
                for ref in (f"refs/tags/{branch}", f"refs/{branch}")
            ):
                return [], f"refspec {spec} may name a ref other than a branch"
        if not short_ref(branch):
            return [], f"refspec {spec} names no branch"
        branches.append(branch)
    return branches, ""


def push_grant(
    program: str, options: list[str], args: list[str], scan: Scan, bare: bool
) -> tuple[str | None, str]:
    """Return the authorization a push matches exactly, if one does.

    Parameters
    ----------
    program : str
        The program word as the command gives it.
    options : list[str]
        Options of git before the subcommand.
    args : list[str]
        Arguments of ``push``.
    scan : Scan
        The reading so far.
    bare : bool
        Whether no assignment or reserved word precedes git.

    Returns
    -------
    tuple[str | None, str]
        The identifier of the authorization, or None; and the reason the
        push gives, which states why it is referred where the policy
        holds an authorization that might have covered it.
    """
    if not scan.policy.grants:
        return None, "git push"

    def refer(why: str) -> tuple[None, str]:
        """Return the answer for a push left referred.

        Parameters
        ----------
        why : str
            Why it is referred.

        Returns
        -------
        tuple[None, str]
            No authorization, and the reason.
        """
        return None, f"git push, referred because {why}"

    if program != "git":
        return refer("the program is named by a path")
    if options or not bare:
        return refer("an option or assignment precedes it")
    unadmitted = sorted(
        k for k in os.environ if k.startswith("GIT_") and k not in GIT_ADMITTED
    )
    if unadmitted:
        why = f"the environment sets a variable of git, {unadmitted[0]}"
        return refer(why)
    if any(a.startswith("-") and a not in PUSH_OPTIONS for a in args):
        return refer("it takes an option outside the short list")
    named = [a for a in args if not a.startswith("-")]
    if len(named) < 2:
        return refer("it names no repository and refspec")
    if len(set(scan.cwds)) != 1 or scan.cwds[0] is None:
        return refer("its directory is not known")
    try:
        dirs = work_repository(scan.cwds[0], scan.policy)
        if dirs is None:
            return refer("the work's own repository is not the one found")
        values = git_configuration(dirs, scan.home)
        hooked = hooks_present(dirs)
    except (OSError, ValueError) as error:
        return refer(f"the git configuration is unreadable: {error}")
    if hooked:
        return refer("the repository holds a hook that git may run")
    repository = named[0]
    for section, sub, key, _ in values:
        if (
            section in GIT_SECTIONS
            or (section, key) in GIT_KEYS
            or (section == "remote" and sub == repository and key in REMOTE_KEYS)
        ):
            return refer(f"the git configuration sets {section}.{key}")
    destination = repository
    if REMOTE_NAME_RE.fullmatch(repository):
        urls = [
            v
            for s, sub, k, v in values
            if s == "remote" and sub == repository and k == "url"
        ]
        if len(urls) != 1:
            return refer(f"remote {repository} has no single address")
        destination = urls[0]
    branches, why = push_branches(named[1:], dirs)
    if why:
        return refer(why)
    grant = granted(scan.policy, "commit", destination, branches)
    if grant is None:
        return refer(
            f"no authorization in force names {destination} and "
            f"{', '.join(branches)}"
        )
    return grant, "git push"


def post_grant(
    program: str, args: list[str], scan: Scan, bare: bool
) -> tuple[str | None, str]:
    """Return the authorization a tracker post of ``gh`` matches, if any.

    Parameters
    ----------
    program : str
        The program word as the command gives it.
    args : list[str]
        Arguments of ``gh``, the subcommand first.
    scan : Scan
        The reading so far.
    bare : bool
        Whether no assignment or reserved word precedes gh.

    Returns
    -------
    tuple[str | None, str]
        The identifier of the authorization, or None; and the reason the
        write gives. A post names its repository with ``--repo
        HOST/OWNER/REPO``, the address ``https://HOST/OWNER/REPO``, and
        carries its title and body as literal words without ``@``, so
        that it sends no file and notifies no one it names.
    """
    reason = f"gh {args[0]} {args[1]}"
    allowed = GH_POSTS.get((args[0], args[1]))
    if not scan.policy.grants or allowed is None:
        return None, reason

    def refer(why: str) -> tuple[None, str]:
        """Return the answer for a post left referred.

        Parameters
        ----------
        why : str
            Why it is referred.

        Returns
        -------
        tuple[None, str]
            No authorization, and the reason.
        """
        return None, f"{reason}, referred because {why}"

    if program != "gh":
        return refer("the program is named by a path")
    if not bare:
        return refer("an assignment or reserved word precedes it")
    if any(k.startswith("GH_") for k in os.environ):
        return refer("the environment sets a variable of gh")
    repos: list[str] = []
    positional: list[str] = []
    rest = args[2:]
    index = 0
    while index < len(rest):
        word = rest[index]
        if not word.startswith("-"):
            positional.append(word)
            index += 1
            continue
        if word.startswith("--") and "=" in word:
            name, value = word.split("=", 1)
            index += 1
        elif word.startswith("--") or len(word) == 2:
            if index + 1 >= len(rest):
                return refer(f"option {word} has no value")
            name, value = word, rest[index + 1]
            index += 2
        else:
            name, value = word[:2], word[2:]
            index += 1
        if name not in allowed:
            return refer(f"it takes option {name}")
        if name in {"-R", "--repo"}:
            repos.append(value)
        elif "@" in value or value.startswith("-"):
            return refer("its text names someone or reads as an option")
    if len(repos) != 1 or not GH_REPO_RE.fullmatch(repos[0]):
        return refer("it names no single --repo HOST/OWNER/REPO")
    if args[1] == "create" and positional:
        return refer("it takes an operand")
    if args[1] == "comment" and (
        len(positional) != 1 or not re.fullmatch(r"[0-9]+", positional[0])
    ):
        return refer("it names no single number")
    destination = f"https://{repos[0]}"
    grant = granted(scan.policy, "post", destination, [])
    if grant is None:
        return refer(f"no authorization in force names {destination}")
    return grant, reason


def check_shell(
    words: list[str], piped: bool, given: str | None, scan: Scan
) -> None:
    """Check a shell started by a command.

    Parameters
    ----------
    words : list[str]
        The shell and its arguments.
    piped : bool
        Whether a pipe feeds its standard input.
    given : str | None
        Text of a here-string or here-document on its standard input.
    scan : Scan
        The reading so far.
    """
    letters = short_flags(words)
    args = operands(words)
    if "c" in letters:
        # The command is the first operand that no option takes; each
        # is read, since a later one is only a positional parameter.
        for index, script in enumerate(args):
            check_line(script, scan, strict=index == 0)
    elif args and "s" not in letters:
        return  # A script file: a program that acts by itself.
    elif given is not None:
        check_line(given, scan)
    elif piped:
        scan.found.add(
            "selective-destruction", "a shell runs commands from a pipe"
        )


def check_launched(words: list[str], scan: Scan) -> None:
    """Check a program the guard does not know for a command it runs.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    scan : Scan
        The reading so far.
    """
    for index, word in enumerate(words[1:], start=1):
        if word.startswith("--chdir="):
            enter_directory(word.partition("=")[2], scan)
        elif word in {"-C", "--chdir"} and index + 1 < len(words):
            enter_directory(words[index + 1], scan)
        elif re.search(r"[\s;&|]", word):
            # A text such as the argument of ``watch``, ``su -c``, or
            # ``env -S`` may be a command line; code of another language
            # is read too, and a text that does not tokenize is skipped.
            check_line(word, scan, strict=False)
    for index, word in enumerate(words[1:], start=1):
        if PurePosixPath(word).name in KNOWN:
            check_simple(words[index:], False, scan)
            return


def enter_directory(target: str, scan: Scan) -> None:
    """Add the directory a ``cd`` or ``-C`` moves to.

    Parameters
    ----------
    target : str
        The directory as the line gives it; empty for the home.
    scan : Scan
        The reading so far; every earlier directory stays, since the
        guard does not follow which commands a move reaches.
    """
    paths = None if target == "-" else resolve(target or "~", scan)
    for path in paths if paths is not None else [None]:
        if len(scan.cwds) >= MAX_DIRECTORIES:
            path = None
        if path not in scan.cwds:
            scan.cwds.append(path)


def check_simple(words: list[str], piped: bool, scan: Scan) -> None:
    """Check one simple command of a shell command line.

    Parameters
    ----------
    words : list[str]
        Words of the command, redirections included.
    piped : bool
        Whether a pipe feeds its standard input.
    scan : Scan
        The reading so far.
    """
    policy, found = scan.policy, scan.found
    scan.commands += 1
    words, redirections = strip_redirections(words)
    given = None
    for operator, target in redirections:
        if operator == "<<<":
            mark = MARK_RE.match(target)
            given = scan.bodies[int(mark.group(1))] if mark else target
            continue
        if operator in READ_REDIRECTS:
            check_reads([target], scan)
        if operator == ">&" and (target.isdigit() or target == "-"):
            continue
        if operator in WRITE_REDIRECTS - {"<"}:
            check_writes([target], scan, append=False)
        elif operator in APPEND_REDIRECTS:
            check_writes([target], scan, append=True)
    program = program_words(words)
    scan.bare = len(program) == len(words)
    words = program
    if not words:
        return
    name = PurePosixPath(words[0]).name
    if computed(words[0], scan):
        found.add("selective-destruction", f"runs computed {words[0]}")
        return
    args = operands(words)
    letters = short_flags(words)
    if name in ELEVATORS:
        found.add("elevated-privilege", name)
        check_launched(words, scan)
    elif name in SHELLS:
        check_shell(words, piped, given, scan)
    elif name == "eval":
        check_line(" ".join(words[1:]), scan)
    elif name in {"cd", "pushd"}:
        enter_directory(args[0] if args else "", scan)
    elif name == "xargs":
        for index, word in enumerate(words[1:], start=1):
            inner = PurePosixPath(word).name
            if inner in KNOWN:
                if inner in REMOVERS | {"mv"}:
                    found.add("selective-destruction", "xargs computes items")
                check_simple(words[index:], False, scan)
                break
    elif name in REMOVERS:
        recursive = bool({"r", "R"} & letters) or long_flag(
            words, "--recursive"
        )
        if name == "rm" and recursive and args:
            found.add("selective-destruction", "recursive removal")
        files_only = name in FILE_REMOVERS or (name == "rm" and not recursive)
        check_removal(args, scan, directories=not files_only)
    elif name == "mv":
        sources, destination = target_split(words, args)
        check_removal(sources, scan)
        check_writes([destination] if destination else [], scan, False)
    elif name in COPIERS:
        sources, destination = target_split(words, args)
        check_writes([destination] if destination else [], scan, False)
        if name == "cp":
            check_reads(sources, scan)
            check_copied(sources, scan)
    elif name in CREATORS:
        check_writes(args, scan, append=False)
    elif name in {"sed", "perl"} and (
        "i" in letters or long_flag(words, "--in-place")
    ):
        check_writes(args[1:], scan, append=False)
    elif name == "tee":
        append = "a" in letters or long_flag(words, "--append")
        check_writes(args, scan, append=append)
    elif name == "dd":
        targets = [w[3:] for w in words[1:] if w.startswith("of=")]
        check_writes(targets, scan, append=False)
    elif name in {"chmod", "chown", "chgrp", "setcap"}:
        if name == "setcap" or (name == "chmod" and grants_privilege(args)):
            found.add("elevated-privilege", f"{name} grants privilege")
        check_writes(args[1:], scan, append=False)
    elif name == "git":
        check_git(words, scan)
    elif name == "find":
        check_find(words, scan)
    elif name == "rsync":
        dry = "n" in letters or long_flag(words, "--dry-run")
        if not dry and long_flag(words, "--delete", "--remove-source-files"):
            found.add("selective-destruction", "rsync removes items")
            for path in (resolve(args[-1], scan) or []) if args else []:
                location = protected_target(path, policy)
                if location:
                    found.add("protected-locations", f"empties {location}")
        check_remote(words, scan)
    elif name in READERS:
        check_reads(args, scan)
    elif name in REMOTE_PROGRAMS:
        check_remote(words, scan)
    elif name not in TEXT_PROGRAMS:
        check_launched(words, scan)


def grants_privilege(args: list[str]) -> bool:
    """Return whether a chmod mode sets the set-user or set-group bit.

    Parameters
    ----------
    args : list[str]
        Operands of ``chmod``; the first is the mode.

    Returns
    -------
    bool
        Whether the mode adds ``s`` or is an octal mode whose leading
        digit of four sets bit 4 or bit 2.
    """
    mode = args[0] if args else ""
    if mode.isdigit() and len(mode) == 4:
        return bool(int(mode[0], 8) & 0o6)
    return "+s" in mode or ("=" in mode and "s" in mode.split("=", 1)[1])


def check_line(line: str, scan: Scan, strict: bool = True) -> None:
    """Check every simple command of a shell command line.

    Parameters
    ----------
    line : str
        The command line.
    scan : Scan
        The reading so far.
    strict : bool
        Whether a line that does not tokenize is referred; False for a
        text that may not be a command line at all.
    """
    line = lift_heredocs(line, scan.bodies)
    if "`" in line or "$(" in line:
        for inner in substitutions(line):
            check_line(inner, scan, strict)
    try:
        commands = split_commands(line)
    except ValueError as error:
        if strict:
            scan.found.add(
                "selective-destruction", f"command not readable: {error}"
            )
        return
    for words, piped in commands:
        check_simple(words, piped, scan)


def check_command(command: str, cwd: list[str], scan: Scan) -> None:
    """Check a shell command line until the directories it uses settle.

    A ``cd`` late in the line, or in a substitution read first, adds a
    directory that earlier commands may also run in, so the line is
    read again while that set grows.

    Parameters
    ----------
    command : str
        The command line.
    cwd : list[str]
        Directories the call starts in.
    scan : Scan
        Receives the outcomes; its directories start as ``cwd``.
    """
    scan.cwds = list(cwd)
    while True:
        known = len(scan.cwds)
        scan.bodies = []
        scan.commands = 0
        scan.permitted = []
        check_line(command, scan)
        if len(scan.cwds) == known:
            return


def substitutions(line: str) -> list[str]:
    """Return the text of each command substitution in a command line.

    Parameters
    ----------
    line : str
        The command line.

    Returns
    -------
    list[str]
        Contents of each ``$(...)`` and each backquoted span, outermost
        first; nested ones are found when their contents are checked.
    """
    found: list[str] = []
    index = 0
    while index < len(line):
        if line.startswith("$(", index):
            depth, start = 1, index + 2
            index = start
            while index < len(line) and depth:
                depth += {"(": 1, ")": -1}.get(line[index], 0)
                index += 1
            found.append(line[start : index - 1])
        elif line[index] == "`":
            end = line.find("`", index + 1)
            end = len(line) if end < 0 else end
            found.append(line[index + 1 : end])
            index = end + 1
        else:
            index += 1
    return found


def url_host(url: str) -> str:
    """Return the host a URL names, or an empty string.

    Parameters
    ----------
    url : str
        The URL.

    Returns
    -------
    str
        The host in lower case, without user information or port; empty
        when the URL names none or the host holds characters a domain
        name does not, so that an odd URL fails closed.
    """
    match = AUTHORITY_RE.match(url.strip())
    if match is None:
        return ""
    host = match.group(1).rsplit("@", 1)[-1].lower()
    host = host.rsplit(":", 1)[0] if host.count(":") == 1 else host
    return host if HOST_RE.match(host) else ""


def check_web(
    tool: str, data: dict[str, Any], policy: Policy, found: Findings
) -> None:
    """Check a web fetch or search.

    Parameters
    ----------
    tool : str
        ``WebFetch`` or ``WebSearch``.
    data : dict[str, Any]
        The tool input.
    policy : Policy
        The policy.
    found : Findings
        Receives the outcomes reached.
    """
    if tool == "WebSearch":
        if not policy.search:
            found.add("network-bounds", "web search is no retrieval scope")
        return
    host = url_host(str(data.get("url", "")))
    if not host or not any(
        host == domain or host.endswith("." + domain)
        for domain in policy.domains
    ):
        found.add("network-bounds", f"fetches from {host or 'no host'}")


def tool_path(text: str, cwd: str) -> str:
    """Return the absolute path a file tool's input names.

    Parameters
    ----------
    text : str
        The path as given; ``~`` names the account's home.
    cwd : str
        Directory a relative path starts from.

    Returns
    -------
    str
        The absolute, normalized path.
    """
    text = os.path.expanduser(text)
    return normalize(text if text.startswith("/") else f"{cwd}/{text}")


def check_call(event: dict[str, Any], policy: Policy) -> Findings:
    """Return the outcomes that one tool call reaches.

    Parameters
    ----------
    event : dict[str, Any]
        The hook input: ``tool_name``, ``tool_input``, and ``cwd``.
    policy : Policy
        The policy.

    Returns
    -------
    Findings
        Every outcome reached, with its reason.

    Raises
    ------
    ValueError
        If the input is not of the form the tool defines, so that the
        caller denies it.
    """
    if not isinstance(event, dict):
        raise ValueError("the call is no JSON object")
    found = Findings()
    tool = event.get("tool_name")
    data = event.get("tool_input", {})
    cwd = event.get("cwd") or policy.work
    if not isinstance(tool, str) or not isinstance(data, dict):
        raise ValueError("tool_name or tool_input of the wrong type")
    if not isinstance(cwd, str) or not cwd.startswith("/"):
        raise ValueError(f"cwd {cwd!r} is no absolute path")
    cwds = [normalize(cwd)]
    # A subagent may run in another directory than the session.
    if isinstance(data.get("cwd"), str) and data["cwd"].startswith("/"):
        cwds.append(normalize(data["cwd"]))
    if tool == "Bash":
        command = text_field(data, "command")
        if len(command) > MAX_COMMAND:
            found.add("selective-destruction", "command too long to read")
            return found
        assigned = set(SET_VARIABLE_RE.findall(command))
        scan = Scan(policy, found, cwds, os.path.expanduser("~"), assigned)
        check_command(command, cwds, scan)
        if scan.commands == 1 and PLAIN_RE.fullmatch(command):
            found.permitted = list(scan.permitted)
        else:
            # Another command, or an expansion the shell performs, may
            # change what the write reaches after the guard read it.
            for reason, grant in scan.permitted:
                found.add(
                    "remote-write",
                    f"{reason}, which {grant} covers only as one plain "
                    "command, the call's only one",
                )
    elif tool in EDIT_TOOLS:
        key = "notebook_path" if tool == "NotebookEdit" else "file_path"
        for base in cwds:
            path = tool_path(text_field(data, key), base)
            check_written(path, policy, found)
    elif tool == "Read":
        for base in cwds:
            path = tool_path(text_field(data, "file_path"), base)
            check_read(path, policy, found)
    elif tool in READ_TOOLS:
        for base in cwds:
            path = tool_path(str(data.get("path") or base), base)
            pattern = data.get("pattern") if tool == "Glob" else None
            if isinstance(pattern, str) and has_glob(pattern):
                path = pattern_base(tool_path(pattern, path))
            check_read(path, policy, found)
            if tool == "Grep" and holds_secrets(real_path(path), policy):
                reason = f"searches the secret store from {path}"
                found.add("read-bounds", reason)
    elif tool in {"WebFetch", "WebSearch"}:
        check_web(tool, data, policy, found)
    elif tool.startswith("mcp__") and not any(
        fnmatch.fnmatchcase(tool, pattern) for pattern in policy.tools
    ):
        found.add("remote-write", f"{tool} is not opened by the record")
    return found


def text_field(data: dict[str, Any], key: str) -> str:
    """Return a field of a tool input that must be a non-empty string.

    Parameters
    ----------
    data : dict[str, Any]
        The tool input.
    key : str
        The field.

    Returns
    -------
    str
        Its value.

    Raises
    ------
    ValueError
        If the field is missing, empty, or not a string.
    """
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"tool_input.{key} is no non-empty string")
    return value


def decide(findings: Findings, policy: Policy) -> dict[str, Any] | None:
    """Return the hook answer for the outcomes a call reaches.

    Parameters
    ----------
    findings : Findings
        Outcomes reached.
    policy : Policy
        The policy.

    Returns
    -------
    dict[str, Any] | None
        The answer: ``allow`` for a call whose only effect the guard
        reads is a remote write that an authorization names, so that a
        permission rule that refers every such write is outranked where
        the environment lets a hook do so, and refers it otherwise; None
        when the call reaches no outcome. An outcome the policy does not
        list is refused, so a gap fails closed.
    """
    if not findings.reached and findings.permitted:
        reason, grant = findings.permitted[0]
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": (
                    f"Governance: {reason} is named by {grant} "
                    "(STND.HARN.29)."
                ),
            }
        }
    if not findings.reached:
        return None
    decisions = [
        (policy.responses.get(outcome, DENY), outcome, reason)
        for outcome, reason in findings.reached
    ]
    denied = [d for d in decisions if d[0] == DENY]
    response, outcome, reason = (denied or decisions)[0]
    verb = "refused" if response == DENY else "referred"
    decision, note = response, ""
    if response == ASK and policy.unattended:
        # Nobody is there to decide, so the referral stops the action.
        decision = DENY
        note = (
            " Nobody is there to decide: halt this line of work and "
            "refer it to the human owner (PRIME.14)."
        )
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": (
                f"Governance outcome {outcome} {verb}: {reason}.{note}"
            ),
        }
    }


def denial(reason: str) -> dict[str, Any]:
    """Return the answer that denies a call.

    Parameters
    ----------
    reason : str
        Why, as the agent reads it.

    Returns
    -------
    dict[str, Any]
        The hook answer.
    """
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": DENY,
            "permissionDecisionReason": reason,
        }
    }


def fault_answer(error: Exception, assured: bool) -> dict[str, Any]:
    """Return the answer to a policy the guard cannot read (STND.HARN.23).

    Parameters
    ----------
    error : Exception
        The fault.
    assured : bool
        Whether the work is assured (CSQ0 or CSQ1).

    Returns
    -------
    dict[str, Any]
        A denial for assured work; for other work, no decision, with a
        warning to the human owner and context for the agent.
    """
    if assured:
        return denial(f"Guard fault: {error!r}.")
    notice = (
        f"Governance guard fault: {error!r}. This call proceeds unguarded; "
        "every provision applies in full (STND.HARN.23)."
    )
    return {
        "systemMessage": notice,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": notice,
        },
    }


def main(argv: list[str]) -> int:
    """Read a call and a policy, and print the decision.

    Parameters
    ----------
    argv : list[str]
        Command-line arguments: the policy file, then ``--assured`` for
        assured work.

    Returns
    -------
    int
        Always 0. A call that the guard cannot read, or whose reading
        faults, is denied at every class, since it is untrusted input
        (DSGN.2); a policy it cannot read is answered as
        ``fault_answer`` states.
    """
    assured = "--assured" in argv[2:]
    try:
        with open(argv[1], encoding="utf-8") as handle:
            policy = read_policy(json.load(handle))
    except Exception as error:  # noqa: BLE001 - no fault passes silently
        print(json.dumps(fault_answer(error, assured)))
        return 0
    try:
        event = json.load(sys.stdin)
        answer = decide(check_call(event, policy), policy)
    except Exception as error:  # noqa: BLE001 - a call never passes a fault
        # The policy was read, so the call brought the fault about, such
        # as a malformed input or a nesting too deep to parse. Letting it
        # proceed would let a call choose to go unguarded.
        answer = denial(f"Unreadable call: {error!r}.")
    if answer is not None:
        print(json.dumps(answer))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
