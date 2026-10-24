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
from dataclasses import dataclass, field
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
POLICY_LISTS = (
    "writable",
    "readable",
    "protected",
    "homes",
    "configuration",
    "ledgers",
    "domains",
    "tools",
)


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
    responses: dict[str, str]
    unattended: bool


@dataclass
class Findings:
    """Outcomes that one call reaches, each with its reason.

    Parameters
    ----------
    reached : list[tuple[str, str]]
        Pairs of outcome key and reason, in the order found.
    """

    reached: list[tuple[str, str]] = field(default_factory=list)

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
    """

    policy: Policy
    found: Findings
    cwds: list[str | None]
    home: str
    assigned: set[str] = field(default_factory=set)
    bodies: list[str] = field(default_factory=list)


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
        If a list field is not a list of strings, or a response is
        neither Refuse nor Refer.
    """
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
        responses=responses,
        unattended=bool(data["unattended"]),
    )


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
        if PurePosixPath(name).name in policy.ledgers:
            found.add("record-entries", f"changes or removes ledger {name}")
    # The write lands where the links lead.
    if not within(real, policy.writable):
        found.add("write-bounds", f"writes {real}")


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
            if not within(real, scan.policy.writable):
                scan.found.add("write-bounds", f"writes {real}")


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
    rest = words[1:]
    while rest and rest[0].startswith("-"):
        option = rest[0]
        takes_value = option in {"-C", "-c", "--git-dir", "--work-tree"}
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
    dry = "n" in letters or long_flag(command, "--dry-run")
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
        found.add("remote-write", "git push")
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


def check_remote(words: list[str], found: Findings) -> None:
    """Check one command for a write to a remote system.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    found : Findings
        Receives the outcomes reached.
    """
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
    elif name == "gh" and len(args) >= 2:
        if args[1] in GH_WRITES.get(args[0], set()) or args[0] == "api":
            found.add("remote-write", f"gh {args[0]} {args[1]}")
    elif name in PUBLISHERS and set(args) & PUBLISHERS[name]:
        found.add("remote-write", f"{name} publishes")


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
    words = program_words(words)
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
        check_remote(words, found)
    elif name in READERS:
        check_reads(args, scan)
    elif name in REMOTE_PROGRAMS:
        check_remote(words, found)
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
        The answer, or None when the call reaches no outcome. An outcome
        the policy does not list is refused, so a gap fails closed.
    """
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
