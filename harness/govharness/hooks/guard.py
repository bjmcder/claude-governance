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

A shell command line is read in these respects, and where the reading
is uncertain the line is referred, as the next paragraph says: quotes;
comments, which start at a ``#`` that begins a word and end at the end
of the line; a backslash before a newline, which joins the two lines;
here-documents, whose body is data unless a shell reads it, and in
whose body each command substitution is read where the delimiter is not
quoted, since the shell runs it; command and process substitution; and
compound commands. An operand is resolved without running anything,
against every directory the line may run in, since a ``cd`` within the
line adds one, and, where a ``..`` follows a symbolic link, also where
the system resolves it. A pattern reaches the outcome of each protected
name it may match by name, and of each item it matches when the guard
runs, where that item's links lead. An operand that depends on a value
the guard does not know, such as a variable, is computed: a removal or
write of a computed item is referred, since its items cannot be listed
(STND.DFLT.24), and so is a read of one while the store holds a closed
file. A program the guard does not know is searched for a command it
knows, so that a launcher such as ``timeout`` or ``uv run`` does not
hide a command it knows; the command found is read with the launcher's
standard input,
so that ``echo ... | env sh`` is read as ``echo ... | sh``. A word
``NAME=value`` of a simple command, other than an argument of a program
that takes only text such as ``grep``, is read as an assignment: the
value of a pager or editor variable (``RUN_VARIABLES``) as a command
line, and that of any other variable of git as a text that may hold
one. ``sponge``, ``ed``, and ``ex`` write the files they name.

Where the guard cannot read a construct soundly, it refers the call
rather than let it proceed (QA.8, part A, and the review of unit 0015):
a ``#`` next to an escaped character; a comment or ``case`` inside a
command substitution; a line in which a second, simpler reading of
where commands begin (``command_starts``) finds a program that the
first did not read; a pattern with a POSIX bracket expression; an alias
of git given in the call, which is also read as the command it stands
for; a setting that ``-c`` gives, other than a few that run nothing
(``plain_key``), whose value is read as well; a variable of git set in
the call, other than its pager and editors and those that name no
program (``GIT_PLAIN``: the author, the committer, and three more); an
``ext::`` or ``fd::`` URL, and the program that ``--upload-pack``,
``--receive-pack``, ``--exec``, or clone's ``-u`` names, whose command
is read as well; a write of git's configuration other than a few
settings that run nothing; a subcommand that is not a command of git,
which covers most aliases set earlier; a command that ``xargs`` builds
from its input, unless its program only reads; a shell or ``source``
that runs a computed script, or reads its commands from a pipe or a
substitution, as ``sh < <(...)`` does, also behind a launcher;
``rg --pre``; a ``cd`` to a relative name in a line that sets
``CDPATH``; and a line whose reading needs more than ``MAX_PATHS``
paths or ``TIME_BUDGET`` seconds, so that the guard answers within the
hook's timeout. As a backstop, ``main`` runs the reading in a thread
and refers the call if it does not finish within ``GUARD_WALL`` seconds,
so that a loop that forgets ``Scan.spend`` cannot stall the guard past
the timeout (re-review of unit 0015, R1). Lines nested more than
``MAX_DEPTH`` deep are denied as unreadable.

The guard sees only what a call names, and reads each program word and
assignment as the literal text given. A program that deletes, writes,
or connects by itself, whether a script, code given inline to an
interpreter, or an alias or function of the shell defined earlier, is
not seen, nor what the members of an archive overwrite, a pattern of
the shell's ``extglob`` option, a symbolic link made in the same line or
changed after the check, or an alias in git's configuration that has
the name of one of git's script commands (such as ``submodule`` or
``mergetool``) where that script is not installed. Nor, as the
re-review of unit 0015 found and the custodian left as known limits
(R2 to R9), does it read a program word that is computed, a glob, a
brace, or split by ``env -S``, including behind a launcher; a git
variable or assignment given other than as a literal ``NAME=value``
word (``NAME+=``, a bare ``export NAME``, ``printf -v``, ``read``, or a
computed word in ``env`` or ``export``); a setting that ``git clone``
or ``submodule`` gives by ``-c`` or ``--config`` after the subcommand;
the shifted first file of ``git merge-file`` behind a valued option; a
script that ``ed``, ``ex``, or ``vim`` runs; an alias used after
``shopt -s expand_aliases``, or a joined ``mapfile -C`` callback; and a
write by ``sed``'s ``w`` command or ``shuf -o``. The coverage report of
the adapter states each such gap (STND.HARN.19). The file uses the
standard library
alone and imports nothing from the package, because it is installed
outside the work, where the agent's account is unable to alter it.
"""

from __future__ import annotations

import fnmatch
import itertools
import json
import os
import re
import shlex
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

DENY = "deny"
ASK = "ask"
RESPONSES = {"Refuse": DENY, "Refer": ASK}
# A longer command line is not read but referred: the guard must answer
# within the hook's timeout of 10 s. A here-document's body is lifted
# out unread, so a file written by one is cheap at this length.
MAX_COMMAND = 100_000
# The bound on the work of reading one call (QA.8, H4): the paths it
# resolves, and the seconds it spends. Past either, the call is
# referred as too large to read, so that the guard never runs into the
# hook's timeout, which lets the call proceed. A pass over a line of
# MAX_COMMAND characters takes under a second, so the answer comes
# well inside the timeout.
MAX_PATHS = 20_000
TIME_BUDGET = 3.0
# A hard wall on the reading, enforced in ``main`` by a thread the
# reading runs in: past it the call is referred, whatever the reading
# is doing, so that no loop that forgets ``Scan.spend`` can stall the
# guard past the hook's timeout of 10 s (re-review of unit 0015, R1).
# It is above ``TIME_BUDGET``, the bound the reading aims for, and well
# below the hook's timeout.
GUARD_WALL = 7.0
# Most command lines nested in one another, by substitution or ``bash
# -c``; a deeper call is unreadable and denied, as one whose nesting
# exceeds the interpreter's was before (review 0005).
MAX_DEPTH = 64
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
# CDPATH is not known, but a line that sets it sends a ``cd`` elsewhere.
KNOWN_VARIABLES = ("HOME", "PWD")
SET_VARIABLE_RE = re.compile(r"(?<![\w${])(HOME|PWD|CDPATH)\b(?!})")
SHELLS = {"bash", "dash", "ksh", "sh", "zsh"}
# Programs of the shell that run a file's commands in the shell itself.
SOURCERS = {".", "source"}
# Names of standard input, which a shell given one reads its commands
# from.
STDIN_NAMES = {"-", "/dev/fd/0", "/dev/stdin", "/proc/self/fd/0"}
# The word that stands for the file a process substitution names: it
# counts as computed, as its path is.
PROCESS_FILE = "/dev/fd/$(...)"
# A comment or a case in a command substitution, whose end the guard
# does not find soundly (review of unit 0015, N3).
UNCERTAIN_RE = re.compile(r"(?:^|[\s;&|(`])(?:#|case\s)")
ELEVATORS = {"doas", "pkexec", "run0", "runuser", "su", "sudo"}
REMOVERS = {"rm", "rmdir", "shred", "unlink"}
# Removers that remove files only, so that no pattern of theirs empties
# a directory.
FILE_REMOVERS = {"shred", "unlink"}
COPIERS = {"cp", "install", "ln"}
CREATORS = {"mkdir", "touch", "truncate"}
# Programs whose operands are all files they read.
READERS = {
    "b2sum",
    "base64",
    "bzcat",
    "cat",
    "cksum",
    "cmp",
    "comm",
    "diff",
    "du",
    "file",
    "head",
    "hexdump",
    "less",
    "ls",
    "md5sum",
    "more",
    "nl",
    "od",
    "paste",
    "rev",
    "sha1sum",
    "sha256sum",
    "sha512sum",
    "stat",
    "strings",
    "tac",
    "tail",
    "wc",
    "xzcat",
    "zcat",
}
# Programs that search files: the first operand is the pattern unless
# an option gives one.
SEARCHERS = {"egrep", "fgrep", "grep", "rg"}
# Programs whose arguments are text, never a command they run.
TEXT_PROGRAMS = {"echo", "printf"} | SEARCHERS
# Programs that ``xargs`` may give its input to as arguments: each only
# reads files or prints text, so computed arguments write nothing. The
# files they read may be the store's, which is referred while the
# store holds a closed file (review of unit 0015, N7). rg is left out,
# since an argument ``--pre`` makes it run a program (N5).
XARGS_READERS = (
    READERS
    | TEXT_PROGRAMS
    | {"basename", "dirname", "readlink", "realpath"}
) - {"less", "more", "rg"}
# Compressors replace each operand by a compressed or decompressed
# file, unless they write to standard output or keep it.
COMPRESSORS = {
    "bunzip2",
    "bzip2",
    "compress",
    "gunzip",
    "gzip",
    "lzma",
    "uncompress",
    "unlzma",
    "unxz",
    "unzstd",
    "xz",
    "zstd",
}
COMPRESSED_RE = re.compile(r"\.(?:bz2|gz|lzma|tbz2?|tgz|txz|xz|Z|zst)$")
REMOTE_COPIERS = {"ftp", "scp", "sftp"}
# Programs that open a connection and send what they are given.
CONNECTORS = {"nc", "ncat", "netcat", "socat", "telnet"}
PUBLISHERS = {
    "cargo": {"publish"},
    "docker": {"push"},
    "flit": {"publish"},
    "gem": {"push"},
    "gradle": {"publish"},
    "gradlew": {"publish"},
    "hatch": {"publish"},
    "helm": {"push"},
    "mvn": {"deploy"},
    "npm": {"publish"},
    "pnpm": {"publish"},
    "podman": {"push"},
    "poetry": {"publish"},
    "twine": {"upload"},
    "uv": {"publish"},
    "yarn": {"publish"},
}
# Commands of ``gh`` that only read; every other one is referred as a
# remote write (QA.8, M3), by command group and subcommand, then the
# commands of one word.
GH_READS = {
    "alias": {"list"},
    "auth": {"status"},
    "attestation": {"verify"},
    "cache": {"list"},
    "codespace": {"list"},
    "config": {"get", "list"},
    "extension": {"browse", "list", "search"},
    "gist": {"list", "view"},
    "issue": {"list", "status", "view"},
    "label": {"list"},
    "org": {"list"},
    "pr": {"checkout", "checks", "diff", "list", "status", "view"},
    "project": {"field-list", "item-list", "list", "view"},
    "release": {"download", "list", "view"},
    "repo": {"clone", "list", "view"},
    "ruleset": {"check", "list", "view"},
    "run": {"download", "list", "view", "watch"},
    "search": {"code", "commits", "issues", "prs", "repos"},
    "secret": {"list"},
    "variable": {"get", "list"},
    "workflow": {"list", "view"},
}
GH_READ_COMMANDS = {
    "--help",
    "--version",
    "-h",
    "browse",
    "completion",
    "help",
    "status",
    "version",
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
# Options of curl that take a value, short and long. A short one may
# be joined to its value and close a cluster, as ``-sd x`` or ``-dx``;
# a long one may be abbreviated (QA.8, M3).
CURL_VALUED = "AbcCdDeEFHKmoPQrtTuUwxXyYz"
# Options of curl that send data, give a method, or read options or
# server commands from elsewhere; a write by each is referred.
CURL_SENDS = {
    "--config",
    "--data",
    "--data-ascii",
    "--data-binary",
    "--data-raw",
    "--data-urlencode",
    "--form",
    "--form-string",
    "--json",
    "--mail-rcpt",
    "--quote",
    "--request",
    "--upload-file",
    "-F",
    "-K",
    "-Q",
    "-T",
    "-X",
    "-d",
}
# Options of curl that name a file it writes.
CURL_OUTPUTS = {
    "--cookie-jar",
    "--dump-header",
    "--etag-save",
    "--libcurl",
    "--output",
    "--output-dir",
    "--stderr",
    "--trace",
    "--trace-ascii",
    "-D",
    "-c",
    "-o",
}
WGET_VALUED = "aABDeiIloOPQRtTUwX"
WGET_OUTPUTS = {
    "--append-output",
    "--directory-prefix",
    "--output-document",
    "--output-file",
    "-O",
    "-P",
    "-a",
    "-o",
}
REMOTE_PROGRAMS = (
    REMOTE_COPIERS
    | CONNECTORS
    | {"curl", "gh", "rsync", "ssh", "wget"}
    | set(PUBLISHERS)
)
# Every program the guard reads; a launcher is searched for one.
KNOWN = (
    SHELLS
    | SOURCERS
    | ELEVATORS
    | REMOVERS
    | COPIERS
    | CREATORS
    | READERS
    | SEARCHERS
    | COMPRESSORS
    | REMOTE_PROGRAMS
    | {"awk", "cd", "chgrp", "chmod", "chown", "dd", "eval", "find", "gawk"}
    | {"git", "mv", "perl", "pushd", "sed", "setcap", "sort", "tar", "tee"}
    | {"openssl", "uniq", "unzip", "xargs", "xxd", "zip"}
    | {"ed", "ex", "sponge"}
)
HISTORY_REWRITES = {
    "fast-import",
    "filter-branch",
    "filter-repo",
    "history",
    "rebase",
    "replace",
    "replay",
}
# The commands of git 2.56 (``git help -a``) whose effect the guard
# reads, or which change nothing it guards. Any other word in the place
# of the subcommand is referred (QA.8, H2): an alias, which may stand
# for any of them; an external command such as ``git lfs``; and a
# command that runs a program or a server, or reads a credential.
GIT_COMMANDS = {
    "add", "am", "annotate", "apply", "archive", "backfill", "bisect",
    "blame", "branch", "bugreport", "bundle", "cat-file", "check-attr",
    "check-ignore", "check-mailmap", "check-ref-format", "checkout",
    "checkout-index", "cherry", "cherry-pick", "clean", "clone",
    "column", "commit", "commit-graph", "commit-tree", "config",
    "count-objects", "describe", "diagnose", "diff", "diff-files",
    "diff-index", "diff-pairs", "diff-tree", "difftool", "fast-export",
    "fetch", "fetch-pack", "fmt-merge-msg", "for-each-ref",
    "format-patch", "fsck", "gc", "get-tar-commit-id", "grep",
    "hash-object", "help", "index-pack", "init", "interpret-trailers",
    "last-modified", "log", "ls-files", "ls-remote", "ls-tree",
    "mailinfo", "mailsplit", "maintenance", "merge", "merge-base",
    "merge-file", "merge-index", "merge-tree", "mergetool", "mktag",
    "mktree", "multi-pack-index", "mv", "name-rev", "notes",
    "pack-objects", "pack-redundant", "pack-refs", "patch-id", "prune",
    "prune-packed", "pull", "push", "range-diff", "read-tree", "reflog",
    "refs", "remote", "repack", "repo", "request-pull", "rerere",
    "reset", "restore", "rev-list", "rev-parse", "revert", "rm",
    "send-email", "send-pack", "shortlog", "show", "show-branch",
    "show-index", "show-ref", "sparse-checkout", "stash", "status",
    "stage", "stripspace", "submodule", "switch", "symbolic-ref", "tag",
    "unpack-file", "unpack-objects", "update-index", "update-ref",
    "update-server-info", "var", "verify-commit", "verify-pack",
    "verify-tag", "version", "whatchanged", "worktree", "write-tree",
}
# Commands of git that take the output options of the diff family, or
# write a file or directory by ``-o``.
GIT_OUTPUT_COMMANDS = {
    "archive",
    "bugreport",
    "diagnose",
    "diff",
    "diff-files",
    "diff-index",
    "diff-tree",
    "format-patch",
    "log",
    "range-diff",
    "show",
    "stash",
    "whatchanged",
}
# Variables whose value is a command line that git or another program
# runs: it is read, not referred (second review of unit 0015).
RUN_VARIABLES = {
    "EDITOR",
    "GIT_EDITOR",
    "GIT_PAGER",
    "GIT_SEQUENCE_EDITOR",
    "PAGER",
    "SSH_ASKPASS",
    "VISUAL",
}
# Variables of git that name no program, transport, or configuration.
GIT_PLAIN = {
    "GIT_AUTHOR_DATE",
    "GIT_AUTHOR_EMAIL",
    "GIT_AUTHOR_NAME",
    "GIT_COMMITTER_DATE",
    "GIT_COMMITTER_EMAIL",
    "GIT_COMMITTER_NAME",
    "GIT_MERGE_AUTOEDIT",
    "GIT_OPTIONAL_LOCKS",
    "GIT_TERMINAL_PROMPT",
}
# Settings of ``git -c`` whose value is a command line, read as one.
RUN_KEYS = {"core.editor", "core.pager", "sequence.editor"}
# Settings of ``git -c`` that run nothing, by prefix.
PLAIN_PREFIXES = (
    "advice.",
    "color.",
    "core.quotepath",
    "safe.directory",
    "user.",
)
# Commands of git that send to another system.
GIT_SENDS = {"send-email", "send-pack"}
# Options of ``git config`` that change a setting, and the subcommands
# of its newer form that do.
CONFIG_WRITES = {
    "--add",
    "--edit",
    "--remove-section",
    "--rename-section",
    "--replace-all",
    "--unset",
    "--unset-all",
    "-e",
    "edit",
    "remove-section",
    "rename-section",
    "set",
    "unset",
}
# Options of ``git config`` that take the next word.
CONFIG_VALUED = {"--blob", "--comment", "--default", "--file", "--type", "-f"}
# Settings that ``git config`` may write without a referral: none runs
# a program, sends a push elsewhere, or defines an alias.
CONFIG_PLAIN = {
    "color.ui",
    "core.autocrlf",
    "core.filemode",
    "init.defaultbranch",
    "pull.ff",
    "pull.rebase",
    "user.email",
    "user.name",
}
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
# section and key, then keys of each remote. Sections ``hook`` (hooks
# defined in the configuration, which run in a push like those of the
# hooks directory), ``gpg`` (the programs of a signed push), and
# ``protocol`` (which transports git may use) are referred whole, since
# the guard does not model them (review of unit 0014, M1 and L3).
GIT_SECTIONS = {
    "alias",
    "credential",
    "gpg",
    "hook",
    "include",
    "includeif",
    "protocol",
    "url",
}
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
    # Signs a push, which then runs the program of gpg.
    ("push", "gpgsign"),
    ("push", "recursesubmodules"),
    # Changes how git calls the ssh program of the transport.
    ("ssh", "variant"),
    ("submodule", "recurse"),
}
# The variables of git that leave an authorized push unreferred; every
# other variable of git refers it (unit 0014). A push launches no
# editor, so it reads neither GIT_EDITOR nor GIT_SEQUENCE_EDITOR. It
# runs GIT_PAGER only when paged, by ``--paginate``, which no admitted
# push takes, or by ``pager.push``, which GIT_KEYS refers.
# GIT_TERMINAL_PROMPT, set false, only stops git asking on the terminal
# for a credential; it supplies none (git(1), Environment Variables), so
# it stands only with a value in PROMPT_OFF, and any other value refers.
# Claude Code sets GIT_EDITOR in the shell of the agent.
GIT_ADMITTED = frozenset(
    {"GIT_EDITOR", "GIT_PAGER", "GIT_SEQUENCE_EDITOR", "GIT_TERMINAL_PROMPT"}
)
PROMPT_OFF = {"0", "false"}
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
        Names of ``KNOWN_VARIABLES``, and ``CDPATH``, that the line
        sets, whose value the guard therefore does not know.
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
    paths : int
        Paths resolved so far, over every pass.
    depth : int
        Command lines open around the one being read.
    expanded : set[int]
        Indexes of the bodies whose delimiter is not quoted, which the
        shell expands.
    programs : set[str]
        Every program word read so far, as the line gives it.
    deadline : float
        Time of ``time.monotonic`` past which the reading stops.
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
    paths: int = 0
    depth: int = 0
    expanded: set[int] = field(default_factory=set)
    programs: set[str] = field(default_factory=set)
    deadline: float = float("inf")

    def spend(self, count: int = 1) -> None:
        """Count resolved paths against the bound on the reading's work.

        Parameters
        ----------
        count : int
            Paths resolved; 0 checks the time alone.

        Raises
        ------
        TooLarge
            If the reading has resolved more than ``MAX_PATHS`` paths
            or passed its deadline.
        """
        self.paths += count
        if self.paths > MAX_PATHS:
            raise TooLarge(f"more than {MAX_PATHS} paths")
        if time.monotonic() > self.deadline:
            raise TooLarge(f"more than {TIME_BUDGET:g} s")


class TooLarge(Exception):
    """The reading of a call has passed the bound on its work (H4)."""


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


def named_paths(joined: str) -> list[str]:
    """Return the paths a name may stand for, read lexically and by the system.

    The system resolves ``l/..`` as the parent of the place the link
    ``l`` leads, not as the directory that holds ``l`` (QA.8, H6), while
    ``cd l/..`` in the shell reads it lexically. Both are kept, so that
    each check sees both.

    Parameters
    ----------
    joined : str
        Absolute path, not normalized.

    Returns
    -------
    list[str]
        The normalized path; then, where a ``..`` follows a symbolic
        link, the path the system resolves it to, as it is when the
        guard runs.
    """
    lexical = normalize(joined)
    if ".." not in joined.split("/") or joined.startswith("/dev/"):
        return [lexical]
    physical = os.path.realpath(joined)
    return [lexical] if physical == real_path(lexical) else [lexical, physical]


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


def lift_heredocs(
    text: str,
    bodies: list[str],
    expanded: list[int],
    doubts: list[str],
    scan: Scan | None = None,
) -> tuple[str, str]:
    """Replace each here-document by a here-string that names its body.

    The lines after ``cmd <<EOF``, up to the line ``EOF``, are data for
    the command, not commands, unless the command is a shell. Each
    operator becomes ``<<< MARK n MARK`` and its body goes to
    ``bodies[n]``, so that a shell's body is read as a here-string's
    text would be. A ``<<`` that is quoted, in a comment, in ``${...}``,
    or in arithmetic is no operator and stays. Where the reading could
    differ from the shell's, the lines stay and are read as commands:
    a body whose end line never comes is read as commands too.

    The line is also made plain for the lexer, as the shell reads it
    (QA.8, H1). A comment, which starts at a ``#`` that begins a word
    and ends at the end of its line, is dropped, so that the lexer reads
    a ``#`` elsewhere, as in ``a#b``, ``$#``, or ``a\\ #b``, as part of
    a word. A backslash before a newline outside single quotes and
    ``$'...'`` joins the two lines. Where this reading is uncertain, a
    reason goes to ``doubts`` and the line is referred (review of unit
    0015, N1 to N3): a ``#`` next to an escaped character, a comment
    inside a command substitution, which in backquotes ends at the next
    backquote, and ``case`` inside one, whose patterns end in ``)``.

    Parameters
    ----------
    text : str
        A shell command line.
    bodies : list[str]
        Receives each body.
    expanded : list[int]
        Receives the index of each body whose delimiter is not quoted,
        in which the shell runs each command substitution.
    doubts : list[str]
        Receives the reason for each place the reading is uncertain.
    scan : Scan | None
        The reading so far, whose ``spend`` is called in the loop so
        that a long or deeply nested line is stopped at the time bound
        (re-review of unit 0015, R1); None where the caller holds no
        scan, as a test does.

    Returns
    -------
    tuple[str, str]
        The line without the bodies and the comments; and the line
        without the bodies only, for a second reading of where commands
        begin (``command_starts``).
    """
    out: list[str] = []
    kept: list[str] = []
    pending: list[tuple[str, bool, int]] = []
    # Open contexts: quotes ' " $', "{" for ${, "(" for a group, "$("
    # and "`" for a command substitution, "#(" for arithmetic.
    stack: list[str] = []
    # How many ``$(`` and backquote contexts the stack holds, counted
    # beside it so that the test is not a scan of the whole stack on
    # each character, which was quadratic (re-review of unit 0015, R1).
    subs = 0
    ticks = 0
    index = 0
    # The last character kept, which tells whether a "#" begins a word.
    last = ""
    while index < len(text):
        if scan is not None and index % 256 == 0:
            scan.spend(0)
        char = text[index]
        context = stack[-1] if stack else ""
        step, piece = 1, None
        boundary = not last or last in " \t\n;&|("
        substituted = subs > 0 or ticks > 0
        if context == "'":
            if char == "'":
                stack.pop()
        elif char == "\\" and text.startswith("\n", index + 1):
            # Within $'...' the pair stays; elsewhere it joins lines.
            step, piece = 2, (None if context == "$'" else "")
        elif char == "\\":
            step = 2
            if "#" in text[index + 1 : index + 3] and context != "$'":
                doubts.append("a # next to an escaped character")
        elif context in {'"', "$'"}:
            if char == ("'" if context == "$'" else '"'):
                stack.pop()
            elif context == '"' and text.startswith("$(", index):
                marker = "#(" if text.startswith("$((", index) else "$("
                stack.append(marker)
                subs += marker == "$("
                step = 2
            elif context == '"' and char == "`":
                stack.append("`")
                ticks += 1
            elif context == '"' and text.startswith("${", index):
                stack.append("{")
        else:
            arithmetic = context in {"#(", "{"}
            match = None
            if char == "<" and not arithmetic:
                match = DELIMITER_RE.match(text, index)
            if text.startswith("<<<", index):
                step = 3
            elif text.startswith(("$((", "(("), index):
                stack += ["#(", "#("]
                step = 3 if char == "$" else 2
            elif text.startswith("$(", index):
                stack.append("$(")
                subs += 1
                step = 2
            elif text.startswith("$'", index):
                stack.append("$'")
                step = 2
            elif text.startswith("${", index):
                stack.append("{")
                step = 2
            elif char == "`":
                if context == "`":
                    stack.pop()
                    ticks -= 1
                else:
                    stack.append("`")
                    ticks += 1
            elif char in {"'", '"'}:
                stack.append(char)
            elif char == "(":
                stack.append("#(" if arithmetic else "(")
            elif char == ")" and context in {"(", "$(", "#("}:
                subs -= stack.pop() == "$("
            elif char == "}" and context == "{":
                stack.pop()
            elif char == "#" and not arithmetic and boundary:
                end = text.find("\n", index)
                end = len(text) if end < 0 else end
                tick = text.find("`", index, end)
                if "`" in stack and tick >= 0:
                    end = tick
                if substituted:
                    doubts.append("a comment inside a command substitution")
                step, piece = end - index, ""
            elif (
                substituted
                and boundary
                and re.match(r"case\s", text[index : index + 5])
            ):
                doubts.append("case inside a command substitution")
            elif match:
                raw = match.group(2)
                if not re.search(r"""['"\\]""", raw):
                    expanded.append(len(bodies))
                delimiter = re.sub(r"""['"]|\\(?=.)""", "", raw)
                pending.append((delimiter, match.group(1) == "-", len(bodies)))
                bodies.append("")
                step = match.end() - index
                piece = f"<<< {MARK}{len(bodies) - 1}{MARK}"
            elif char == "\n" and pending:
                start = len(out)
                out.append(char)
                index = read_bodies(text, index + 1, pending, bodies, out)
                kept.extend(out[start:])
                pending = []
                last = out[-1][-1:] or "\n"
                continue
        original = text[index : index + step]
        piece = original if piece is None else piece
        out.append(piece)
        kept.append(piece or original)
        if char == "`" and context != "'":
            # An opening backquote begins a word; a closing one does not.
            last = " " if stack and stack[-1] == "`" else "a"
        elif char == "\\" and step == 2:
            # An escaped character is part of a word, even a blank.
            last = last if not piece else "a"
        else:
            last = piece[-1:] or last
        index += step
    return "".join(out), "".join(kept)


def command_starts(text: str, scan: Scan | None = None) -> list[str]:
    """Return the program word of each command, read a second, simpler way.

    This reading knows only quotes, backslashes, comments, and where a
    command begins: after ``;``, ``&``, ``|``, a newline, a parenthesis,
    a backquote, ``$(``, and the reserved words and assignments in front
    of a program. A comment ends at the newline, or in backquotes at the
    next backquote. Where it finds a program the guard knows that the
    first reading did not read, the line is referred (review of unit
    0015, design rule).

    Parameters
    ----------
    text : str
        A command line, its here-document bodies lifted out and its
        comments kept.
    scan : Scan | None
        The reading so far, whose ``spend`` is called in the loop to
        hold the time bound (re-review of unit 0015, R1); None where the
        caller holds no scan, as a test does.

    Returns
    -------
    list[str]
        The first word of each command, its quotes and backslashes
        removed.
    """
    starts: list[str] = []
    stack: list[str] = []
    current: list[str] | None = None
    expect = True
    inword = False
    comment = False
    index = 0
    while index <= len(text):
        if scan is not None and index % 256 == 0:
            scan.spend(0)
        char = text[index] if index < len(text) else "\n"
        top = stack[-1] if stack else ""
        ends = char in " \t\n;&|()`" and top in {"", "(", "`"}
        if comment:
            if char == "\n" or (char == "`" and "`" in stack):
                comment = False
            else:
                index += 1
                continue
        if ends or (
            top == '"' and (char == "`" or text.startswith("$(", index))
        ):
            if current is not None:
                word = "".join(current)
                current = None
                if word in KEYWORDS or re.match(r"[A-Za-z_]\w*\+?=", word):
                    expect = True
                else:
                    starts.append(word)
            inword = False
        if top == "'":
            if char == "'":
                stack.pop()
            elif current is not None:
                current.append(char)
        elif char == "\\":
            following = text[index + 1 : index + 2]
            if following != "\n":
                if current is None and expect and not inword:
                    current, expect = [], False
                if current is not None:
                    current.append(following)
                inword = True
            index += 1
        elif top == '"':
            if char == '"':
                stack.pop()
            elif char == "`" or text.startswith("$(", index):
                stack.append("`" if char == "`" else "(")
                index += 0 if char == "`" else 1
                expect = True
            elif current is not None:
                current.append(char)
        elif char == "#" and not inword:
            comment = True
        elif char in " \t":
            pass
        elif char in "\n;&|()`":
            if char == "(":
                stack.append("(")
            elif char == ")" and top == "(":
                stack.pop()
            elif char == "`":
                if top == "`":
                    stack.pop()
                else:
                    stack.append("`")
            expect = True
        else:
            if current is None and expect and not inword:
                current, expect = [], False
            inword = True
            if char in "'\"":
                stack.append(char)
            elif current is not None:
                current.append(char)
        index += 1
    return starts


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
    each start a new one, and the command that a ``(`` interrupted goes
    on after its ``)``. A process substitution also leaves the word
    ``PROCESS_FILE`` in the command it is part of, which stands for the
    file it names, so that ``bash <(...)`` runs a computed script.

    Parameters
    ----------
    line : str
        The command line, here-documents and comments lifted.

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
    # Comments are gone; a "#" left is part of a word (QA.8, H1).
    lexer.commenters = ""
    commands: list[tuple[list[str], bool]] = [([], False)]
    # The command that receives words, and those a "(" interrupted.
    current = 0
    opened: list[int] = []
    for token in lexer:
        if token and set(token) <= set(PUNCTUATION) and token not in REDIRECTS:
            for at, char in enumerate(token):
                before = token[at - 1] if at else ""
                if char == "(":
                    if before in {"<", ">"}:
                        commands[current][0].append(PROCESS_FILE)
                    opened.append(current)
                elif char == ")" and opened:
                    current = opened.pop()
                    continue
                elif char not in "();&|" or before in {";", "&", "|"}:
                    continue
                run = re.match(r"[;&|]*", token[at:]).group(0)
                commands.append(([], "|" in run and run != "||"))
                current = len(commands) - 1
            continue
        # Newlines are left in tokens so that quoted ones survive; an
        # unquoted newline separates commands as ";" does.
        first, *rest = token.split("\n")
        commands[current][0].append(first)
        for part in rest:
            commands.append(([part], False))
            current = len(commands) - 1
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


def matches(name: str, pattern: str) -> bool:
    """Return whether a shell pattern may match a name.

    Parameters
    ----------
    name : str
        A name or path.
    pattern : str
        A shell pattern.

    Returns
    -------
    bool
        Whether it matches as ``fnmatch`` reads it, with ``[^...]``
        read as the shell's negation ``[!...]``. A ``*`` here also
        matches a leading ``.`` and a ``/``, so the answer may be yes
        where the shell's is no, never the other way.
    """
    return fnmatch.fnmatchcase(name, pattern.replace("[^", "[!"))


def may_select(pattern: str, location: str) -> bool:
    """Return whether a pattern may name a location or an item under it.

    Parameters
    ----------
    pattern : str
        Absolute, normalized pattern.
    location : str
        Absolute, normalized location.

    Returns
    -------
    bool
        Whether each part of the pattern, up to the depth of the
        location, may match the location's part; a part with ``**``
        may match any number of parts.
    """
    want = PurePosixPath(location).parts
    have = PurePosixPath(pattern).parts
    for index, part in enumerate(have):
        if "**" in part or index >= len(want):
            return True
        if not matches(want[index], part):
            return False
    return len(have) >= len(want)


def pattern_items(pattern: str, scan: Scan) -> list[str]:
    """Return the items that exist now and that a pattern may match.

    Parameters
    ----------
    pattern : str
        Absolute, normalized pattern.
    scan : Scan
        The reading so far. A pattern with a POSIX bracket expression,
        ``[:class:]``, ``[.x.]``, or ``[=x=]``, which ``matches`` does
        not read, is referred (review of unit 0015, N4).

    Returns
    -------
    list[str]
        Each path, part by part as ``matches`` reads the pattern, that
        names an item now; the caller checks each where its links lead,
        so that ``g?/config``, where ``g`` is a link to ``.git``, is a
        write of ``.git/config``.

    Raises
    ------
    TooLarge
        If the reading passes the bound on its work.
    """
    if re.search(r"\[[:.=]", pattern):
        reason = f"pattern {pattern} holds a bracket expression not read"
        scan.found.add("selective-destruction", reason)
    found = ["/"]
    for part in PurePosixPath(pattern).parts[1:]:
        following: list[str] = []
        for base in found:
            names = [part]
            if has_glob(part):
                try:
                    names = [n for n in os.listdir(base) if matches(n, part)]
                except OSError:
                    names = []
            for name in sorted(names):
                scan.spend()
                following.append(f"{base.rstrip('/')}/{name}")
        found = following
    return [path for path in found if os.path.lexists(path)]


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
        Normalized paths, which may be patterns, with the path the
        system resolves where a ``..`` follows a link (``named_paths``);
        None when the operand is computed: it holds a value the guard
        does not know, such as a variable, a substitution, or the ``{}``
        of ``find``.

    Raises
    ------
    TooLarge
        If the reading passes the bound on its work.
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
                scan.spend()
                paths += named_paths(text)
                continue
            for cwd in scan.cwds:
                if cwd is None:
                    return None
                scan.spend()
                paths += named_paths(f"{cwd}/{text}")
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


def abbreviates(stem: str, names: tuple[str, ...] | set[str]) -> bool:
    """Return whether a long option as given may stand for one of these.

    Parameters
    ----------
    stem : str
        The option as given, without its ``=VALUE``.
    names : tuple[str, ...] | set[str]
        Long options, such as ``--output``.

    Returns
    -------
    bool
        Whether it is a prefix of one of them of three characters or
        more, as GNU programs, git, and curl accept.
    """
    return len(stem) > 2 and any(name.startswith(stem) for name in names)


def option_values(
    words: list[str], valued: str, names: set[str]
) -> list[tuple[str, str]]:
    """Return each option of a set that a command gives, with its value.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    valued : str
        Every short option of the program that takes a value, so that a
        cluster such as ``-sSo FILE`` is read as the program reads it:
        the first such letter takes the rest of the cluster, or else the
        next word.
    names : set[str]
        The options wanted, short (``-o``) and long (``--output``). A
        long one may be given as ``--name=VALUE`` or ``--name VALUE``,
        and abbreviated to a prefix of three characters or more, which
        counts for each option it may stand for.

    Returns
    -------
    list[tuple[str, str]]
        The option, by its full name, and its value, before ``--``.
    """
    found: list[tuple[str, str]] = []
    index = 1
    while index < len(words):
        word = words[index]
        index += 1
        if word == "--":
            break
        if word.startswith("--"):
            stem, equals, value = word.partition("=")
            full = sorted(n for n in names if abbreviates(stem, (n,)))
            if full and not equals:
                value = words[index] if index < len(words) else ""
                index += 1
            found += [(name, value) for name in full]
        elif word.startswith("-") and len(word) > 1:
            for at, letter in enumerate(word[1:], start=2):
                if letter not in valued:
                    continue
                value = word[at:]
                if not value:
                    value = words[index] if index < len(words) else ""
                    index += 1
                if f"-{letter}" in names:
                    found.append((f"-{letter}", value))
                break
    return found


@dataclass(frozen=True)
class Syntax:
    """How a program that takes a script or a pattern reads its arguments.

    Parameters
    ----------
    scripts : str
        Short options that give the script or pattern, so that every
        operand is then a file.
    valued : str
        Other short options that take a value.
    optional : str
        Short options whose value, if any, is the rest of the cluster.
    long_scripts : tuple[str, ...]
        Long options that give the script or pattern.
    long_valued : tuple[str, ...]
        Other long options that take a value.
    script : bool
        Whether the first operand is the script where no option gives
        one; False for a program whose operands are all files.
    """

    scripts: str
    valued: str
    optional: str = ""
    long_scripts: tuple[str, ...] = ()
    long_valued: tuple[str, ...] = ()
    script: bool = True


SED = Syntax("ef", "l", "i", ("--expression", "--file"), ("--line-length",))
PERL = Syntax("eE", "", "i")
AWK = Syntax(
    "efE",
    "Fvil",
    "",
    ("--exec", "--file", "--source"),
    ("--assign", "--field-separator", "--include", "--load"),
)
GREP = Syntax(
    "ef",
    "ABCDdm",
    "",
    ("--file", "--regexp"),
    (
        "--after-context",
        "--before-context",
        "--binary-files",
        "--context",
        "--devices",
        "--directories",
        "--exclude",
        "--exclude-dir",
        "--exclude-from",
        "--group-separator",
        "--include",
        "--label",
        "--max-count",
    ),
)
RG = Syntax(
    "ef",
    "ABCdEgjMmrTt",
    "",
    ("--file", "--regexp"),
    (
        "--after-context",
        "--before-context",
        "--context",
        "--encoding",
        "--glob",
        "--iglob",
        "--max-columns",
        "--max-count",
        "--max-depth",
        "--replace",
        "--threads",
        "--type",
        "--type-not",
    ),
)

SORT = Syntax(
    "",
    "kotST",
    "",
    (),
    (
        "--batch-size",
        "--buffer-size",
        "--compress-program",
        "--field-separator",
        "--files0-from",
        "--key",
        "--output",
        "--parallel",
        "--temporary-directory",
    ),
    script=False,
)
UNIQ = Syntax(
    "",
    "fsw",
    "",
    (),
    ("--check-chars", "--skip-chars", "--skip-fields"),
    script=False,
)
# Options of tar that take a value, and those that name a program it
# runs.
TAR_VALUED = "bCfFgHIKLNTVX"
TAR_RUNS = {
    "--checkpoint-action",
    "--info-script",
    "--new-volume-script",
    "--rsh-command",
    "--to-command",
    "-F",
}
TAR_COMPRESSORS = {"--use-compress-program", "-I"}
# Options of xxd that take the next word.
XXD_VALUED = {
    "-c",
    "-cols",
    "-g",
    "-groupsize",
    "-l",
    "-len",
    "-n",
    "-name",
    "-o",
    "-offset",
    "-s",
    "-seek",
}


def check_script_files(words: list[str], syntax: Syntax, scan: Scan) -> None:
    """Check the files that ``-f`` or ``--file`` names, as reads (N7).

    Parameters
    ----------
    words : list[str]
        The program and its arguments.
    syntax : Syntax
        How the program reads them.
    scan : Scan
        The reading so far.
    """
    letters = syntax.scripts + syntax.valued
    files = option_values(words, letters, {"--file", "-f"})
    check_reads([value for _, value in files], scan)


def script_files(words: list[str], syntax: Syntax) -> list[str]:
    """Return the files that a program taking a script or pattern names.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    syntax : Syntax
        How the program reads them.

    Returns
    -------
    list[str]
        The operands, and every argument after ``--``; the first
        operand is left out as the script unless an option gives one,
        as ``-e``, ``-es/a/b/``, or ``--expression=...`` does (QA.8, M1).
        A value the reading does not take for one is kept as a file,
        which errs toward a check.
    """
    files: list[str] = []
    given = False
    index = 1
    ended = False
    while index < len(words):
        word = words[index]
        index += 1
        if ended or word == "-" or not word.startswith("-"):
            files.append(word)
        elif word == "--":
            ended = True
        elif word.startswith("--"):
            stem, equals, _ = word.partition("=")

            if abbreviates(stem, syntax.long_scripts):
                given = True
                index += 0 if equals else 1
            elif abbreviates(stem, syntax.long_valued) and not equals:
                index += 1
        else:
            for at, letter in enumerate(word[1:], start=2):
                if letter in syntax.optional:
                    break
                if letter in syntax.scripts + syntax.valued:
                    given = given or letter in syntax.scripts
                    index += 0 if word[at:] else 1
                    break
    return files if given or not syntax.script else files[1:]


def mode_and_files(words: list[str]) -> tuple[str, list[str]]:
    """Return the mode or owner that chmod, chown, or chgrp sets, and files.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.

    Returns
    -------
    tuple[str, list[str]]
        The first argument that is neither an option nor ``--``, which
        may start with ``-`` as the mode ``-w`` does, and the files
        after it; with ``--reference``, no mode and every such argument
        as a file (QA.8, M1).
    """
    flags = set("Rcfv") | (set("HLPh") if words[0] != "chmod" else set())
    named: list[str] = []
    reference = False
    index = 1
    ended = False
    while index < len(words):
        word = words[index]
        index += 1
        if ended:
            named.append(word)
        elif word == "--":
            ended = True
        elif word.startswith("--"):
            if word.startswith("--reference"):
                reference = True
                index += 0 if "=" in word else 1
        elif word.startswith("-") and len(word) > 1 and set(word[1:]) <= flags:
            continue
        else:
            named.append(word)
    if reference:
        return "", named
    return (named[0], named[1:]) if named else ("", [])


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
        if any(matches(name, pattern) for name in names):
            found.add("protected-locations", f"takes {location} out of use")
    location = protected_target(base, policy)
    # A pattern of wildcards alone, such as "*" or ".*", selects every
    # item of its directory.
    if directories and location == base and not re.search(r"\w", rest):
        found.add("protected-locations", f"empties {location}")
    if any(
        matches(ledger, PurePosixPath(pattern).name)
        for ledger in policy.ledgers
    ):
        found.add("record-entries", f"pattern {pattern} selects a ledger")
    check_written(base, policy, found)
    if holds_secrets(real_path(base), policy):
        found.add("write-bounds", f"pattern {pattern} selects the store")
    for item in pattern_items(pattern, scan):
        location = protected_target(real_path(item), policy)
        if location:
            found.add("protected-locations", f"takes {location} out of use")
        check_written(item, policy, found)


def check_pattern_written(pattern: str, scan: Scan, append: bool) -> None:
    """Check a write whose target is a pattern (QA.8, H7).

    The shell expands a pattern in a redirection when one file matches,
    and in an operand to every file that matches, so the write reaches
    each outcome of an item that the pattern may match.

    Parameters
    ----------
    pattern : str
        Absolute, normalized pattern.
    scan : Scan
        The reading so far.
    append : bool
        Whether the command only appends, which changes no ledger entry.
    """
    policy, found = scan.policy, scan.found
    base = pattern_base(pattern)
    check_written(base, policy, found)
    for location in policy.configuration:
        if may_select(pattern, location):
            reason = f"pattern {pattern} may change {location}"
            found.add("enforcing-configuration", reason)
    if any(matches(".git", part) for part in PurePosixPath(pattern).parts):
        reason = f"pattern {pattern} may write version-control files"
        found.add("history-rewrite", reason)
    if not append and any(
        matches(ledger, PurePosixPath(pattern).name)
        for ledger in policy.ledgers
    ):
        found.add("record-entries", f"pattern {pattern} may change a ledger")
    if holds_secrets(real_path(base), policy):
        found.add("write-bounds", f"pattern {pattern} may write the store")
    for item in pattern_items(pattern, scan):
        check_target(item, scan, append)


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
            if has_glob(path):
                check_pattern_written(path, scan, append)
            else:
                check_target(path, scan, append)


def check_target(path: str, scan: Scan, append: bool) -> None:
    """Check one path that a command writes.

    Parameters
    ----------
    path : str
        Absolute, normalized path, no pattern.
    scan : Scan
        The reading so far.
    append : bool
        Whether the command only appends, which changes no ledger entry.
    """
    if not append:
        check_written(path, scan.policy, scan.found)
        return
    real = real_path(path)
    if within(path, scan.policy.configuration):
        scan.found.add("enforcing-configuration", f"changes {path}")
    if any(".git" in PurePosixPath(n).parts for n in (path, real)):
        # An appended line still adds a setting or a hook.
        scan.found.add("history-rewrite", f"writes version-control {path}")
    if not within(real, scan.policy.writable):
        scan.found.add("write-bounds", f"writes {real}")
    elif secret_file(real, scan.policy):
        scan.found.add("write-bounds", f"writes secret store file {real}")


def check_reads(targets: list[str], scan: Scan) -> None:
    """Check the operands that a command reads.

    Parameters
    ----------
    targets : list[str]
        Operands as the line gives them. A computed one is left to the
        sandbox, since a read changes nothing, except while the store
        holds a closed file, which it may name, as in ``cat $(find
        secrets)`` (review of unit 0015, N7).
    scan : Scan
        The reading so far.
    """
    for target in targets:
        paths = resolve(target, scan)
        if paths is None and store_closed(scan.policy):
            reason = f"reads computed {target} while the store is closed"
            scan.found.add("read-bounds", reason)
        for path in paths or []:
            check_read(path, scan.policy, scan.found)


def store_closed(policy: Policy) -> bool:
    """Return whether the store holds a file not opened to the agent.

    Parameters
    ----------
    policy : Policy
        The policy.

    Returns
    -------
    bool
        Whether a store is provided and holds such a file.
    """
    store = policy.store
    return bool(store) and holds_secrets(real_path(store), policy)


def check_copied(sources: list[str], scan: Scan, verb: str = "copies") -> None:
    """Check the sources of a copy or search for a directory holding the store.

    Parameters
    ----------
    sources : list[str]
        Operands as the line gives them; a computed one is left to the
        sandbox, as for other reads.
    scan : Scan
        The reading so far.
    verb : str
        What the command does with them, for the reason.
    """
    for source in sources:
        for path in resolve(source, scan) or []:
            if holds_secrets(real_path(path), scan.policy):
                scan.found.add("read-bounds", f"{verb} the store: {path}")


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
        one of ``DRY_VALUED`` and holds no ``=``. Before ``--`` only. An
        option ``--no-...`` may undo the flag, as ``--no-dry-run`` does
        (QA.8, M6), so with one it is no dry run.
    """
    words = args[: args.index("--")] if "--" in args else args
    if not {"-n", "--dry-run"} & set(words):
        return False
    for word in words:
        if word.startswith("--no-"):
            return False
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
        ``core.pager`` runs one; ``-C`` adds a directory. A setting that
        ``--config-env`` takes from a variable, and a subcommand outside
        ``GIT_COMMANDS``, which covers most aliases, are referred: the
        guard does not read what git runs for them (QA.8, H2). An alias
        that ``-c`` gives is referred too, and where the subcommand is
        its name, the command it stands for is read in its place as
        well, since git takes an alias where no command of that name is
        installed (review of unit 0015, N8).
    """
    found = scan.found
    bare = scan.bare
    rest = words[1:]
    options: list[str] = []
    # Each option with its value, and each alias by name, with its
    # value and the place of its option.
    pairs: list[list[str]] = []
    aliases: dict[str, tuple[str, int]] = {}
    while rest and rest[0].startswith("-"):
        option = rest[0]
        options.append(option)
        takes_value = option in GIT_VALUED
        value = rest[1] if takes_value and len(rest) > 1 else ""
        pairs.append(rest[:2] if takes_value else rest[:1])
        rest = rest[2:] if takes_value else rest[1:]
        if option == "-c":
            key, _, setting = value.partition("=")
            if key.lower().startswith("alias."):
                alias = key[len("alias.") :]
                aliases[alias.lower()] = (setting, len(pairs) - 1)
                reason = f"git alias {alias} given in the call"
                found.add("selective-destruction", reason)
            elif key.lower() in RUN_KEYS or key.lower().startswith("pager."):
                # The value is a command line, read as one.
                check_line(setting, scan)
            elif not plain_key(key.lower()):
                reason = f"git setting {key} given in the call"
                found.add("selective-destruction", reason)
            check_line(setting.lstrip("!"), scan, False)
        elif option.partition("=")[0] == "--config-env":
            reason = "git setting taken from a variable"
            found.add("selective-destruction", reason)
        elif option == "-C":
            enter_directory(value, scan)
    if not rest:
        return
    sub, args = rest[0], rest[1:]
    command = ["git", *args]
    flags = set(args)
    letters = short_flags(command)
    named = operands(command)
    dry = dry_run(sub, args)
    if sub.lower() in aliases and not aliases[sub.lower()][0].startswith("!"):
        setting, place = aliases[sub.lower()]
        try:
            stands_for = shlex.split(setting)
        except ValueError:
            stands_for = []
        kept = [w for i, pair in enumerate(pairs) if i != place for w in pair]
        if stands_for:
            check_git([words[0], *kept, *stands_for, *args], scan)
    check_git_outputs(sub, command, scan)
    check_transport(sub, command, scan)
    if sub not in GIT_COMMANDS | HISTORY_REWRITES:
        reason = f"git {sub} is no command the guard reads, such as an alias"
        found.add("selective-destruction", reason)
    elif sub == "push" and not dry:
        forced = long_flag(
            command,
            "--force",
            "--force-with-lease",
            "--force-if-includes",
            "--mirror",
            "--delete",
            "--prune",
        ) or any(a.startswith(("+", ":")) for a in named)
        if forced or {"f", "d"} & letters:
            found.add("history-rewrite", "forced or deleting push")
        grant, reason = push_grant(words[0], options, args, scan, bare)
        if grant is None:
            found.add("remote-write", reason)
        else:
            scan.permitted.append((reason, grant))
    elif sub in GIT_SENDS:
        found.add("remote-write", f"git {sub}")
    elif sub in HISTORY_REWRITES | {"update-ref"}:
        found.add("history-rewrite", f"git {sub}")
    elif sub == "symbolic-ref" and (
        len(named) > 1 or "d" in letters or long_flag(command, "--delete")
    ):
        found.add("history-rewrite", "git symbolic-ref moves or deletes a ref")
    elif sub == "commit" and long_flag(command, "--amend"):
        found.add("history-rewrite", "git commit --amend")
    elif sub == "reflog" and flags & {"expire", "delete"}:
        found.add("history-rewrite", "git reflog expire or delete")
    elif sub == "branch" and (
        {"D", "f", "M", "C", "m"} & letters
        or long_flag(command, "--force", "--move")
    ):
        found.add("history-rewrite", "forced branch change or rename")
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
    elif sub == "reset":
        check_reset(command, scan)
    elif sub == "clean" and not dry:
        found.add("selective-destruction", "git clean")
    elif sub == "stash" and flags & {"drop", "clear"}:
        found.add("selective-destruction", "git stash drop or clear")
    elif (sub == "checkout" and flags & {"--", "."}) or (
        sub == "restore"
        and (
            "W" in letters
            or long_flag(command, "--worktree")
            or not ("S" in letters or long_flag(command, "--staged"))
        )
    ):
        found.add("selective-destruction", f"git {sub} overwrites files")
    elif sub == "rm" and not dry and not long_flag(command, "--cached"):
        recursive = "r" in letters
        if recursive:
            found.add("selective-destruction", "recursive removal")
        check_removal(named, scan, directories=recursive)
    elif sub == "mv" and not dry:
        sources, destination = target_split(command, named)
        check_removal(sources, scan)
        check_writes([destination] if destination else [], scan, False)
    elif sub == "config":
        check_config(command, scan)
    elif sub == "init" or (sub == "clone" and len(named) > 1):
        # The directory made, which is the last operand.
        check_writes(named[-1:], scan, False)
    elif sub == "worktree" and named[:1] == ["add"]:
        # The path, and any branch or commit, which errs toward a check.
        check_writes(named[1:], scan, False)
    elif sub == "submodule" and "foreach" in args:
        check_line(" ".join(args[args.index("foreach") + 1 :]), scan)
    elif sub == "bisect" and args[:1] == ["run"]:
        check_simple(args[1:], False, scan)


def plain_key(key: str) -> bool:
    """Return whether a setting given by ``git -c`` runs nothing.

    Parameters
    ----------
    key : str
        The setting, in lower case.

    Returns
    -------
    bool
        Whether it is one of ``CONFIG_PLAIN`` or starts with one of
        ``PLAIN_PREFIXES``; every other setting given in the call is
        referred, since many name a program or a transport.
    """
    return key in CONFIG_PLAIN or key.startswith(PLAIN_PREFIXES)


def check_transport(sub: str, command: list[str], scan: Scan) -> None:
    """Check the transports and transport programs a git command names.

    Parameters
    ----------
    sub : str
        The subcommand.
    command : list[str]
        ``git`` and the arguments of the subcommand.
    scan : Scan
        The reading so far. A URL ``ext::`` runs the command it holds,
        and ``fd::`` talks to a descriptor the guard cannot follow; each
        is referred, and the command of ``ext::`` is read as well. So is
        the program that ``--upload-pack``, ``--receive-pack``,
        ``--exec``, or clone's ``-u`` names (second review of unit 0015).
    """
    for word in command[1:]:
        url = word.partition("=")[2] if word.startswith("-") else word
        if url.lower().startswith(("ext::", "fd::")):
            reason = f"git transport {url.split('::')[0]}:: runs a program"
            scan.found.add("selective-destruction", reason)
            if url.lower().startswith("ext::"):
                text = url[len("ext::") :].replace("% ", " ")
                check_line(text, scan, strict=False)
    names = {"--exec", "--receive-pack", "--upload-pack"}
    if sub == "clone":
        names.add("-u")
    short = "u" if sub == "clone" else ""
    for option, value in option_values(command, short, names):
        reason = f"git {option} names the program of the transport"
        scan.found.add("selective-destruction", reason)
        check_line(value, scan, strict=False)


def check_git_outputs(sub: str, command: list[str], scan: Scan) -> None:
    """Check the files and directories that a git command writes (M5, N5).

    Parameters
    ----------
    sub : str
        The subcommand.
    command : list[str]
        ``git`` and the arguments of the subcommand.
    scan : Scan
        The reading so far. From git-diff(1), git-log(1), and the pages
        of the commands named here: ``--output`` of the diff options,
        which ``diff``, ``log``, ``show``, and the commands that take them
        read; ``-o`` and ``--output-directory`` of ``format-patch``,
        ``bugreport``, and ``diagnose``; ``-o`` and ``--output`` of
        ``archive``; the file of ``bundle create``; the first file of
        ``merge-file``, which it overwrites unless ``-p``; the file of
        ``--export-marks``; and ``--separate-git-dir`` of ``init`` and
        ``clone``. A ``-o`` of another of these is taken as an output
        too, which errs toward a check.
    """
    named = operands(command)
    letters = short_flags(command)
    names: set[str] = set()
    if sub in GIT_OUTPUT_COMMANDS:
        names = {"--output", "--output-directory", "-o"}
    elif sub in {"fast-export", "fast-import"}:
        names = {"--export-marks"}
    elif sub in {"clone", "init"}:
        names = {"--separate-git-dir"}
    outputs = [value for _, value in option_values(command, "o", names)]
    if sub == "bundle" and named[:1] == ["create"]:
        outputs += named[1:2]
    if sub == "merge-file" and not (
        "p" in letters or long_flag(command, "--stdout")
    ):
        outputs += named[:1]
    check_writes(outputs, scan, False)


def check_reset(command: list[str], scan: Scan) -> None:
    """Check ``git reset``, which moves the branch or unstages paths.

    Parameters
    ----------
    command : list[str]
        ``git`` and the arguments of ``reset``.
    scan : Scan
        The reading so far. A first operand before ``--`` other than
        ``HEAD`` moves the branch to it where it names a commit (QA.8,
        M6), and is referred. It is not refused as a history rewrite:
        the commits it leaves stay in the reflog, as those of ``git
        reset --hard HEAD~1`` did before unit 0015, which was referred,
        and STND.HARN.18 does not settle whether moving a local branch
        rewrites history. A plain name may also be a path.
    """
    found = scan.found
    words = command[1:]
    head = words[: words.index("--")] if "--" in words else words
    named = [w for w in head if not w.startswith("-")]
    if long_flag(command, "--hard"):
        found.add("selective-destruction", "git reset --hard")
    target = named[0] if named else "HEAD"
    path = target in {".", ".."} or target.startswith(("./", "../", ":/"))
    if target in {"@", "HEAD"} or path or target.endswith("/"):
        # HEAD, or a name only a path has: it unstages.
        return
    if re.search(r"[~^@]", target) or re.fullmatch(r"[0-9a-f]{7,64}", target):
        reason = f"git reset moves the branch to {target}"
    else:
        reason = f"git reset {target}, which may name a commit"
    found.add("selective-destruction", reason)


def check_config(command: list[str], scan: Scan) -> None:
    """Check ``git config``, which may set what git runs later.

    Parameters
    ----------
    command : list[str]
        ``git`` and the arguments of ``config``.
    scan : Scan
        The reading so far. A read passes. A write is referred unless it
        sets a key of ``CONFIG_PLAIN`` in the repository's own file,
        since an alias, a pager, or a hook set now runs at a later call
        (QA.8, H2); the file it writes, by ``--file``, ``--global``, or
        ``--system``, is checked as a write (M5).
    """
    words = command[1:]
    files: list[str] = []
    named: list[str] = []
    index = 0
    while index < len(words):
        word = words[index]
        index += 1
        if word in CONFIG_VALUED:
            if word in {"--file", "-f"} and index < len(words):
                files.append(words[index])
            index += 1
        elif word.startswith("--file="):
            files.append(word.partition("=")[2])
        elif word == "--global":
            files.append("~/.gitconfig")
        elif word == "--system":
            files.append(GIT_SYSTEM_CONFIG)
        elif not word.startswith("-"):
            named.append(word)
    reads = {
        "--get",
        "--get-all",
        "--get-color",
        "--get-colorbool",
        "--get-regexp",
        "--get-urlmatch",
        "--list",
        "-l",
        "get",
        "list",
    }
    writes = bool(CONFIG_WRITES & set(words)) or (
        not reads & set(words) and len(named) > 1
    )
    if not writes:
        return
    keys = named[1:] if named[:1] and named[0] in CONFIG_WRITES else named
    key = keys[0].lower() if keys else ""
    if files or key not in CONFIG_PLAIN:
        reason = f"git config sets {key or 'a setting'}"
        scan.found.add("selective-destruction", reason)
    check_writes(files, scan, False)


def check_find(words: list[str], scan: Scan) -> None:
    """Check one find command.

    Parameters
    ----------
    words : list[str]
        ``find`` and its arguments; a ``;`` ending an ``-exec`` has
        already ended the command.
    scan : Scan
        The reading so far. A command that ``-exec`` or ``-ok`` runs is
        read, and with one, a root that holds the store reaches
        read-bounds, since the command may read each file it finds
        (QA.8, M4); the file of ``-fprint`` and its kind is a write
        (M5).
    """
    roots = []
    for word in words[1:]:
        if word.startswith(("-", "(", "!")):
            break
        roots.append(word)
    deletes = "-delete" in words
    runs = False
    outputs: list[str] = []
    for index, word in enumerate(words):
        if word in {"-exec", "-execdir", "-ok", "-okdir"}:
            runs = True
            segment = words[index + 1 :]
            if "+" in segment:
                segment = segment[: segment.index("+")]
            if segment and PurePosixPath(segment[0]).name in REMOVERS | {
                "mv"
            }:
                deletes = True
            if segment:
                check_simple(segment, False, scan)
        elif word in {"-fls", "-fprint", "-fprint0", "-fprintf"}:
            outputs += words[index + 1 : index + 2]
    check_writes(outputs, scan, False)
    for root in roots or ["."]:
        paths = resolve(root, scan)
        if paths is None:
            if deletes:
                scan.found.add("selective-destruction", f"computed {root}")
            continue
        for path in paths:
            if not deletes:
                check_read(path, scan.policy, scan.found)
                if runs and holds_secrets(real_path(path), scan.policy):
                    reason = f"runs a command on the files of the store {path}"
                    scan.found.add("read-bounds", reason)
                continue
            location = protected_target(path, scan.policy)
            if location:
                scan.found.add(
                    "protected-locations", f"removes within {location}"
                )
            check_written(path, scan.policy, scan.found)
    if deletes:
        scan.found.add("selective-destruction", "find selects items to remove")


def check_remote(words: list[str], scan: Scan, fed: bool = False) -> None:
    """Check one command for a write to a remote system.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    scan : Scan
        The reading so far; receives the outcomes reached.
    fed : bool
        Whether a pipe, a redirection, or a here-document feeds its
        standard input, which ``ssh`` runs on the remote system.
    """
    found = scan.found
    name = PurePosixPath(words[0]).name
    args = words[1:]
    if name in REMOTE_COPIERS:
        found.add("remote-write", name)
    elif name in CONNECTORS:
        found.add("remote-write", f"{name} sends to another system")
    elif name == "ssh" and (len(operands(words)) > 1 or fed):
        found.add("remote-write", "command run on a remote system")
    elif name == "rsync" and any(
        ":" in a and not a.startswith("-") for a in args[-1:]
    ):
        found.add("remote-write", "rsync to a remote system")
    elif name == "curl":
        check_curl(words, scan)
    elif name == "wget":
        if any(a.startswith(("--post", "--method", "--body")) for a in args):
            found.add("remote-write", "wget sends data")
        outputs = option_values(words, WGET_VALUED, WGET_OUTPUTS)
        check_writes([value for _, value in outputs], scan, False)
    elif name == "gh":
        check_gh(words, scan)
    elif name in PUBLISHERS and set(args) & PUBLISHERS[name]:
        found.add("remote-write", f"{name} publishes")


def check_curl(words: list[str], scan: Scan) -> None:
    """Check one curl command: what it sends, and the files it writes.

    Parameters
    ----------
    words : list[str]
        ``curl`` and its arguments, read with ``option_values``, so that
        a joined value, a cluster, and an abbreviation count (QA.8, M3).
    scan : Scan
        The reading so far.
    """
    values = option_values(words, CURL_VALUED, CURL_SENDS | CURL_OUTPUTS)
    for option, value in values:
        if option in {"-X", "--request"}:
            if value.upper() not in {"GET", "HEAD"}:
                scan.found.add("remote-write", f"curl {option} {value}")
        elif option in CURL_SENDS:
            reason = f"curl {option} sends data or reads its options"
            scan.found.add("remote-write", reason)
    outputs = [value for option, value in values if option in CURL_OUTPUTS]
    check_writes(outputs, scan, False)


def check_gh(words: list[str], scan: Scan) -> None:
    """Check one gh command.

    Parameters
    ----------
    words : list[str]
        ``gh`` and its arguments.
    scan : Scan
        The reading so far. A command of ``GH_WRITES`` may be one that an
        authorization names; every command that is not one of
        ``GH_READS`` or ``GH_READ_COMMANDS`` is referred as a remote
        write (QA.8, M3).
    """
    found = scan.found
    args = words[1:]
    if args and args[0].startswith("-") and args[1:]:
        found.add("remote-write", "gh with an option before its command")
    elif len(args) >= 2 and args[0] in GH_WRITES and args[1].startswith("-"):
        found.add("remote-write", f"gh {args[0]} with an option first")
    elif len(args) >= 2 and args[1] in GH_WRITES.get(args[0], set()):
        grant, reason = post_grant(words[0], args, scan, scan.bare)
        if grant is None:
            found.add("remote-write", reason)
        else:
            scan.permitted.append((reason, grant))
    elif len(args) >= 2 and args[0] == "api":
        found.add("remote-write", f"gh {args[0]} {args[1]}")
    elif not (
        not args
        or args[0] in GH_READ_COMMANDS
        or (len(args) == 1 and args[0] in GH_READS)
        or (len(args) >= 2 and args[1] in GH_READS.get(args[0], set()))
    ):
        reason = f"gh {' '.join(args[:2])}, which the guard does not read"
        found.add("remote-write", reason)


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
    prompt = os.environ.get("GIT_TERMINAL_PROMPT")
    if prompt is not None and prompt not in PROMPT_OFF:
        unadmitted.insert(0, "GIT_TERMINAL_PROMPT")
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
    words: list[str],
    piped: bool,
    given: str | None,
    scan: Scan,
    unknown_input: bool = False,
) -> None:
    """Check a shell started by a command, or a file it sources.

    Parameters
    ----------
    words : list[str]
        The shell, or ``source`` or ``.``, and its arguments.
    piped : bool
        Whether a pipe feeds its standard input.
    given : str | None
        Text of a here-string or here-document on its standard input.
    scan : Scan
        The reading so far. A script named as standard input is read
        from what feeds it, and a script whose name is computed, such as
        the file of a process substitution in ``bash <(...)``, is
        referred (QA.8, L2).
    unknown_input : bool
        Whether standard input is the output of a command or a value
        the guard does not know; a shell that reads its commands from
        it is referred, as ``sh < <(...)`` (review of unit 0015, N5).
    """
    letters = short_flags(words)
    args = operands(words)
    reads_input = not args or args[0] in STDIN_NAMES or "s" in letters
    if unknown_input and reads_input and "c" not in letters:
        reason = "a shell runs commands that a substitution or variable gives"
        scan.found.add("selective-destruction", reason)
    if "c" in letters and words[0] not in SOURCERS:
        # The command is the first operand that no option takes; each
        # is read, since a later one is only a positional parameter.
        for index, script in enumerate(args):
            check_line(script, scan, strict=index == 0)
    elif args and "s" not in letters and args[0] not in STDIN_NAMES:
        if computed(args[0], scan):
            reason = f"a shell runs the computed script {args[0]}"
            scan.found.add("selective-destruction", reason)
        # Otherwise a script file: a program that acts by itself.
    elif given is not None:
        check_line(given, scan)
    elif piped:
        scan.found.add(
            "selective-destruction", "a shell runs commands from a pipe"
        )


def check_launched(
    words: list[str],
    scan: Scan,
    piped: bool = False,
    inputs: list[str] | None = None,
) -> None:
    """Check a program the guard does not know for a command it runs.

    Parameters
    ----------
    words : list[str]
        Program name and its arguments.
    scan : Scan
        The reading so far.
    piped : bool
        Whether a pipe feeds the program's standard input.
    inputs : list[str] | None
        The redirections of its standard input, as operator and target
        words. A launcher such as ``env``, ``nice``, or ``timeout`` hands
        its standard input to the program it runs, so that ``echo ... |
        env sh`` runs what the pipe gives; the command found is read
        with them (second review of unit 0015).
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
            check_simple([*words[index:], *(inputs or [])], piped, scan)
            return


def enter_directory(target: str, scan: Scan) -> None:
    """Add the directory a ``cd`` or ``-C`` moves to.

    Parameters
    ----------
    target : str
        The directory as the line gives it; empty for the home.
    scan : Scan
        The reading so far; every earlier directory stays, since the
        guard does not follow which commands a move reaches. Where the
        line sets ``CDPATH``, a relative name may lead to any directory
        it lists, so the directory is one the guard cannot tell (QA.8,
        L1).
    """
    searched = "CDPATH" in scan.assigned and not target.startswith(
        ("/", ".", "~", "$")
    )
    unknown = target == "-" or (searched and target != "")
    paths = None if unknown else resolve(target or "~", scan)
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

    Raises
    ------
    TooLarge
        If the reading passes the bound on its work.
    """
    found = scan.found
    scan.spend(0)
    scan.commands += 1
    words, redirections = strip_redirections(words)
    given = None
    fed = piped
    # Whether standard input is the output of a command or a value the
    # guard does not know, which a shell would run (review of unit 0015,
    # N5): a redirection from a process substitution or a computed
    # file, or a here-string or unquoted body that a substitution fills.
    unknown_input = False
    for operator, target in redirections:
        if operator == "<<<":
            mark = MARK_RE.match(target)
            given = scan.bodies[int(mark.group(1))] if mark else target
            fed = True
            expands = mark is None or int(mark.group(1)) in scan.expanded
            unknown_input = expands and ("`" in given or "$(" in given)
            continue
        if operator in READ_REDIRECTS:
            fed = True
            unknown_input = unknown_input or computed(target, scan)
            check_reads([target], scan)
        if operator == ">&" and (target.isdigit() or target == "-"):
            continue
        if operator in WRITE_REDIRECTS - {"<"}:
            check_writes([target], scan, append=False)
        elif operator in APPEND_REDIRECTS:
            check_writes([target], scan, append=True)
    inputs = [
        word
        for operator, target in redirections
        if operator in READ_REDIRECTS | {"<<<", "<&"}
        for word in (operator, target)
    ]
    program = program_words(words)
    # The arguments of a program that takes only text, such as grep,
    # assign nothing; those of any other program may, as env's do.
    texts = program and PurePosixPath(program[0]).name in TEXT_PROGRAMS
    leading = words[: len(words) - len(program)]
    check_assignments(leading if texts else words, scan)
    scan.bare = len(program) == len(words)
    words = program
    if not words:
        return
    name = PurePosixPath(words[0]).name
    scan.programs.add(words[0])
    if computed(words[0], scan):
        found.add("selective-destruction", f"runs computed {words[0]}")
        return
    args = operands(words)
    letters = short_flags(words)
    in_place = "i" in letters or long_flag(words, "--in-place")
    if name in ELEVATORS:
        found.add("elevated-privilege", name)
        check_launched(words, scan, piped, inputs)
    elif name in SHELLS or words[0] in SOURCERS:
        check_shell(words, piped, given, scan, unknown_input)
    elif name == "eval":
        check_line(" ".join(words[1:]), scan)
    elif name in {"cd", "pushd"}:
        enter_directory(args[0] if args else "", scan)
    elif name == "xargs":
        check_xargs(words, scan)
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
        if name in {"cp", "install"}:
            check_reads(sources, scan)
            check_copied(sources, scan)
    elif name in CREATORS:
        check_writes(args, scan, append=False)
    elif name in {"awk", "gawk", "sed"}:
        syntax = SED if name == "sed" else AWK
        check_script_files(words, syntax, scan)
        files = script_files(words, syntax)
        if (name == "sed" and in_place) or (
            name != "sed" and any(w.endswith("inplace") for w in words[1:])
        ):
            check_writes(files, scan, append=False)
        else:
            check_reads(files, scan)
        # A script may run a command, as sed's e does; its text is read.
        check_launched(words, scan)
    elif name == "perl" and in_place:
        check_writes(script_files(words, PERL), scan, append=False)
    elif name in SEARCHERS:
        check_search(words, scan)
    elif name == "tee":
        append = "a" in letters or long_flag(words, "--append")
        check_writes(args, scan, append=append)
    elif name == "dd":
        check_reads([w[3:] for w in words[1:] if w.startswith("if=")], scan)
        targets = [w[3:] for w in words[1:] if w.startswith("of=")]
        check_writes(targets, scan, append=False)
    elif name in {"chmod", "chown", "chgrp"}:
        mode, files = mode_and_files(words)
        if name == "chmod" and grants_privilege(mode):
            found.add("elevated-privilege", f"{name} grants privilege")
        check_writes(files, scan, append=False)
    elif name == "setcap":
        found.add("elevated-privilege", f"{name} grants privilege")
        check_writes(args[1:], scan, append=False)
    elif name == "git":
        check_git(words, scan)
    elif name == "find":
        check_find(words, scan)
    elif name == "rsync":
        check_rsync(words, scan, fed)
    elif name == "tar":
        check_tar(words, scan)
    elif name == "sort":
        check_reads(script_files(words, SORT), scan)
        outputs = option_values(words, "kotST", {"--output", "-o"})
        check_writes([value for _, value in outputs], scan, False)
    elif name == "uniq":
        files = script_files(words, UNIQ)
        check_reads(files[:1], scan)
        check_writes(files[1:2], scan, False)
    elif name in COMPRESSORS:
        check_compressed(words, scan)
    elif name in {"openssl", "unzip", "xxd", "zip"}:
        check_archived(words, scan)
    elif name in READERS:
        check_reads(args, scan)
    elif name in REMOTE_PROGRAMS:
        check_remote(words, scan, fed)
        if name in PUBLISHERS:
            # Many also launch a program, as ``uv run`` does.
            check_launched(words, scan)
    elif name in {"ed", "ex", "sponge"}:
        # Each writes the files it names (second review of unit 0015).
        append = name == "sponge" and "a" in letters
        check_writes(args, scan, append=append)
    elif name not in TEXT_PROGRAMS:
        check_launched(words, scan, piped, inputs)


def check_assignments(words: list[str], scan: Scan) -> None:
    """Check the variables a command sets that name a program to run.

    Parameters
    ----------
    words : list[str]
        Words of one simple command, so that an assignment before the
        program, an argument of ``env``, and one of ``export`` all
        count.
    scan : Scan
        The reading so far. The value of a variable that names a pager
        or an editor (``RUN_VARIABLES``) is read as a command line. Any
        other variable of git is referred unless it names only an author
        or committer (``GIT_PLAIN``), since git runs a program that
        ``GIT_SSH_COMMAND``, ``GIT_PROXY_COMMAND``, ``GIT_EXTERNAL_DIFF``,
        or ``GIT_ASKPASS`` names, takes settings from
        ``GIT_CONFIG_PARAMETERS``, and allows transports by
        ``GIT_ALLOW_PROTOCOL`` (second review of unit 0015). Unit 0014
        admits the pager and editors of git in the guard's own
        environment; set in the call, their values are read instead.
    """
    for word in words:
        match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)=(.*)", word, re.DOTALL)
        if match is None:
            continue
        name, value = match.groups()
        if name in RUN_VARIABLES:
            check_line(value, scan)
        elif name.startswith("GIT_") and name not in GIT_PLAIN:
            reason = f"git variable {name} set in the call"
            scan.found.add("selective-destruction", reason)
            check_line(value, scan, strict=False)


def xargs_command(words: list[str]) -> tuple[list[str], str | None]:
    """Return the command that xargs runs, and its replace string.

    Parameters
    ----------
    words : list[str]
        ``xargs`` and its arguments.

    Returns
    -------
    tuple[list[str], str | None]
        The words from the program on, after the options of GNU xargs
        and their values; empty where xargs runs ``echo``. The replace
        string of ``-I``, ``-i``, or ``--replace``, or None.
    """
    replace = None
    index = 1
    while index < len(words):
        word = words[index]
        if word == "--":
            index += 1
            break
        if not word.startswith("-") or word == "-":
            break
        index += 1
        if word.startswith("--"):
            stem, equals, value = word.partition("=")
            if abbreviates(stem, ("--replace",)):
                replace = value if equals else "{}"
            elif not equals and abbreviates(
                stem,
                (
                    "--arg-file",
                    "--delimiter",
                    "--max-args",
                    "--max-chars",
                    "--max-procs",
                    "--process-slot-var",
                ),
            ):
                index += 1
            continue
        for at, letter in enumerate(word[1:], start=2):
            if letter in "eil":
                # The value, if any, is the rest of the cluster.
                if letter == "i":
                    replace = word[at:] or "{}"
                break
            if letter in "adEILnPs":
                value = word[at:]
                if not value:
                    value = words[index] if index < len(words) else ""
                    index += 1
                if letter == "I":
                    replace = value
                break
    return words[index:], replace


def check_xargs(words: list[str], scan: Scan) -> None:
    """Check an xargs command, which gives its input to a program.

    Parameters
    ----------
    words : list[str]
        ``xargs`` and its arguments.
    scan : Scan
        The reading so far. The input becomes arguments that the guard
        cannot list, so the command is referred unless its program only
        reads files or prints text (``XARGS_READERS``), and a program
        named by the replace string is referred (QA.8, H5). The command
        as written is read as well.
    """
    command, replace = xargs_command(words)
    if not command:
        return
    inner = PurePosixPath(command[0]).name
    if replace and replace in command[0]:
        reason = "xargs builds its program from its input"
        scan.found.add("selective-destruction", reason)
    elif inner in REMOVERS | {"mv"}:
        scan.found.add("selective-destruction", "xargs computes items")
    elif inner not in XARGS_READERS:
        reason = f"xargs computes the arguments of {inner}"
        scan.found.add("selective-destruction", reason)
    elif store_closed(scan.policy):
        # The files it reads are computed, and may be the store's (N7).
        reason = f"xargs gives {inner} files it computes"
        scan.found.add("read-bounds", reason)
    check_simple(command, False, scan)


def check_search(words: list[str], scan: Scan) -> None:
    """Check a search of files by grep or rg (QA.8, M4).

    Parameters
    ----------
    words : list[str]
        The program and its arguments.
    scan : Scan
        The reading so far. Each file is a read; a recursive search, as
        rg's always is, reaches read-bounds where a directory it takes
        holds the store, as the Grep tool does (STND.DFLT.31). A file
        of patterns is a read, and ``rg --pre``, which runs a program, is
        referred.
    """
    rg = PurePosixPath(words[0]).name == "rg"
    syntax = RG if rg else GREP
    if rg and any(w == "--pre" or w.startswith("--pre=") for w in words):
        # rg runs the program of --pre on each file (review of unit
        # 0015, N5).
        scan.found.add("selective-destruction", "rg --pre runs a program")
    check_script_files(words, syntax, scan)
    files = script_files(words, syntax)
    recursive = rg or bool({"r", "R"} & short_flags(words)) or long_flag(
        words, "--recursive", "--dereference-recursive"
    )
    if recursive:
        files = files or ["."]
        check_copied(files, scan, "searches")
    check_reads(files, scan)


def check_rsync(words: list[str], scan: Scan, fed: bool) -> None:
    """Check one rsync command.

    Parameters
    ----------
    words : list[str]
        ``rsync`` and its arguments.
    scan : Scan
        The reading so far. A local destination is a write, and the
        sources are reads, so that a copy of the store is seen (QA.8, M4
        and M5); a value of an option may be read as a source too,
        which errs toward a check.
    fed : bool
        Whether its standard input is fed.
    """
    found = scan.found
    args = operands(words)
    letters = short_flags(words)
    dry = "n" in letters or long_flag(words, "--dry-run")
    if not dry and long_flag(words, "--delete", "--remove-source-files"):
        found.add("selective-destruction", "rsync removes items")
        for path in (resolve(args[-1], scan) or []) if args else []:
            location = protected_target(path, scan.policy)
            if location:
                found.add("protected-locations", f"empties {location}")
    if len(args) > 1:
        if not dry and ":" not in args[-1]:
            check_writes(args[-1:], scan, False)
        check_reads(args[:-1], scan)
        check_copied(args[:-1], scan)
    check_remote(words, scan, fed)


def check_tar(words: list[str], scan: Scan) -> None:
    """Check one tar command (QA.8, M4 and M5).

    Parameters
    ----------
    words : list[str]
        ``tar`` and its arguments. In the old form, as ``tar cf x.tar
        dir``, the first word bundles the options and their values
        follow in order.
    scan : Scan
        The reading so far. Creating an archive writes it and reads its
        members, so that a copy of the store is seen; extracting one
        reads it and writes into the directory of ``-C``. What the
        members of an archive overwrite is not seen. An option that runs
        a program is referred, but a compressor's name is read as a
        command.
    """
    if len(words) > 1 and not words[1].startswith("-"):
        bundled, rest = [words[0]], list(words[2:])
        for letter in words[1]:
            bundled.append(f"-{letter}")
            if letter in TAR_VALUED and rest:
                bundled.append(rest.pop(0))
        words = bundled + rest
    names = {"--directory", "--file", "-C", "-f"} | TAR_RUNS | TAR_COMPRESSORS
    values = option_values(words, TAR_VALUED, names)
    for option, value in values:
        if option in TAR_RUNS:
            reason = f"tar {option} runs a program"
            scan.found.add("selective-destruction", reason)
        elif option in TAR_COMPRESSORS:
            check_line(value, scan, strict=False)
    archives = [v for o, v in values if o in {"--file", "-f"} and v != "-"]
    directories = [v for o, v in values if o in {"--directory", "-C"}]
    taken = {value for _, value in values}
    members = [a for a in operands(words) if a not in taken]
    letters = short_flags(words)
    if set("Acru") & letters or long_flag(
        words, "--append", "--catenate", "--concatenate", "--create",
        "--update",
    ):
        check_writes(archives, scan, False)
        check_reads(members, scan)
        check_copied(members, scan)
    elif "x" in letters or long_flag(words, "--extract", "--get"):
        check_reads(archives, scan)
        check_writes(directories or ["."], scan, False)
    else:
        check_reads(archives, scan)


def check_archived(words: list[str], scan: Scan) -> None:
    """Check zip, unzip, xxd, or openssl (review of unit 0015, N7).

    Parameters
    ----------
    words : list[str]
        The program and its arguments.
    scan : Scan
        The reading so far. zip writes its archive, its first operand,
        and reads its members; unzip reads its archive and writes into
        the directory of ``-d``; xxd and openssl as ``check_named_files``
        reads them. Each may also run a program, as zip's
        ``--unzip-command`` does, so its texts are read as a launcher's.
    """
    name = PurePosixPath(words[0]).name
    args = operands(words)
    if name == "zip":
        check_writes(args[:1], scan, False)
        check_reads(args[1:], scan)
        check_copied(args[1:], scan)
    elif name == "unzip":
        check_reads(args[:1], scan)
        outputs = [value for _, value in option_values(words, "d", {"-d"})]
        check_writes(outputs or ["."], scan, False)
    else:
        check_named_files(words, scan)
    check_launched(words, scan)


def check_named_files(words: list[str], scan: Scan) -> None:
    """Check the files of xxd or openssl, whose options are whole words.

    Parameters
    ----------
    words : list[str]
        The program and its arguments.
    scan : Scan
        The reading so far. xxd reads its first operand and writes its
        second; openssl reads the file of ``-in``, ``-inkey``, ``-key``,
        and ``-kfile``, and writes that of ``-out`` (review of unit
        0015, N7).
    """
    reads: list[str] = []
    writes: list[str] = []
    if PurePosixPath(words[0]).name == "xxd":
        files: list[str] = []
        index = 1
        while index < len(words):
            word = words[index]
            index += 1
            if word in XXD_VALUED:
                index += 1
            elif word == "-" or not word.startswith("-"):
                files.append(word)
        reads, writes = files[:1], files[1:2]
    else:
        for word, value in itertools.pairwise(words[1:]):
            if word in {"-in", "-inkey", "-key", "-kfile"}:
                reads.append(value)
            elif word == "-out":
                writes.append(value)
    check_reads(reads, scan)
    check_copied(reads, scan)
    check_writes(writes, scan, False)


def check_compressed(words: list[str], scan: Scan) -> None:
    """Check a compressor, which replaces each file it names (QA.8, M5).

    Parameters
    ----------
    words : list[str]
        The program and its arguments.
    scan : Scan
        The reading so far. Each operand is removed, unless the program
        keeps it or writes to standard output, and a decompressed one is
        written under its name without the suffix.
    """
    name = PurePosixPath(words[0]).name
    letters = short_flags(words)
    if {"c", "l", "t"} & letters or long_flag(
        words, "--list", "--stdout", "--test", "--to-stdout"
    ):
        return
    files = operands(words)
    keep = "k" in letters or long_flag(words, "--keep")
    if name in {"unzstd", "zstd"}:
        keep = not long_flag(words, "--rm")
        outputs = option_values(words, "oDT", {"-o"})
        check_writes([value for _, value in outputs], scan, False)
    decompress = (
        "d" in letters
        or long_flag(words, "--decompress", "--uncompress")
        or name.startswith("un")
        or name in {"bunzip2", "gunzip"}
    )
    targets = [] if keep else list(files)
    if decompress:
        targets += [COMPRESSED_RE.sub("", f) for f in files]
    check_writes(targets, scan, False)


def grants_privilege(mode: str) -> bool:
    """Return whether a chmod mode sets the set-user or set-group bit.

    Parameters
    ----------
    mode : str
        The mode argument of ``chmod``.

    Returns
    -------
    bool
        Whether an octal mode, of any length, sets bit 04000 or 02000,
        or a symbolic clause adds or sets ``s``, as ``u+s``, ``u+xs``,
        ``g=rws``, or ``+s`` do (QA.8, M2).
    """
    if re.fullmatch(r"[0-7]+", mode):
        return bool(int(mode, 8) & 0o6000)
    return any("s" in perms for perms in re.findall(r"[+=]([^,+=-]*)", mode))


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

    Raises
    ------
    TooLarge
        If the reading passes the bound on its work.
    ValueError
        If more than ``MAX_DEPTH`` lines are nested, so that the call is
        denied as unreadable.
    """
    scan.spend(0)
    if scan.depth >= MAX_DEPTH:
        raise ValueError(f"command lines nested more than {MAX_DEPTH} deep")
    scan.depth += 1
    try:
        read_line(line, scan, strict)
    finally:
        scan.depth -= 1


def read_line(line: str, scan: Scan, strict: bool) -> None:
    """Read the simple commands of one command line, for ``check_line``.

    Parameters
    ----------
    line : str
        The command line.
    scan : Scan
        The reading so far.
    strict : bool
        Whether a line that does not tokenize is referred.
    """
    expanded: list[int] = []
    doubts: list[str] = []
    line, kept = lift_heredocs(line, scan.bodies, expanded, doubts, scan)
    for slot in expanded:
        # The shell runs each substitution of a body whose delimiter is
        # not quoted (QA.8, H3). The span of one that holds a comment or
        # a case is not found soundly by ``substitutions`` (N3).
        scan.expanded.add(slot)
        for inner in substitutions(scan.bodies[slot].replace("\\\n", "")):
            if UNCERTAIN_RE.search(inner):
                doubts.append("a comment or case in a body's substitution")
            check_line(inner, scan, strict)
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
    if not strict:
        return
    # A second, simpler reading of where commands begin; a program it
    # finds that the first reading did not read is a disagreement.
    missed = [
        word
        for word in command_starts(kept, scan)
        if PurePosixPath(word).name in KNOWN and word not in scan.programs
    ]
    if missed:
        doubts.append(f"a second reading finds the command {missed[0]}")
    for doubt in doubts:
        reason = f"line not read soundly: {doubt}"
        scan.found.add("selective-destruction", reason)


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
        scan.expanded = set()
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


def tool_paths(text: str, cwd: str) -> list[str]:
    """Return every path a file tool's input may lead to.

    Parameters
    ----------
    text : str
        The path as given; ``~`` names the account's home.
    cwd : str
        Directory a relative path starts from.

    Returns
    -------
    list[str]
        The normalized path, and the path the system resolves where a
        ``..`` follows a symbolic link (``named_paths``).
    """
    text = os.path.expanduser(text)
    return named_paths(text if text.startswith("/") else f"{cwd}/{text}")


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
        scan.deadline = time.monotonic() + TIME_BUDGET
        try:
            check_command(command, cwds, scan)
        except TooLarge as error:
            # The answer must come within the hook's timeout, and an
            # unread call is referred, never let through (QA.8, H4).
            reason = f"command too large to read: {error}"
            found.add("selective-destruction", reason)
            return found
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
            for path in tool_paths(text_field(data, key), base):
                check_written(path, policy, found)
    elif tool == "Read":
        for base in cwds:
            for path in tool_paths(text_field(data, "file_path"), base):
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


def read_within_wall(event: dict[str, Any], policy: Policy) -> Findings:
    """Read a call, but refer it if the reading passes ``GUARD_WALL``.

    The reading runs in a daemon thread. Where it does not finish within
    ``GUARD_WALL`` seconds, the thread is left to die with the process
    and the call is referred as too large to read, so that no reading,
    however it loops, stalls the guard past the hook's timeout (QA.8,
    H4; re-review of unit 0015, R1). The referral is a referral like any
    other, so an unattended session denies it and ``--assured`` asks.

    Parameters
    ----------
    event : dict[str, Any]
        The hook input.
    policy : Policy
        The policy.

    Returns
    -------
    Findings
        The outcomes read, or a lone referral where the wall is hit.

    Raises
    ------
    Exception
        Whatever the reading raised, so that the caller denies the call.
    """
    box: dict[str, Any] = {}

    def run() -> None:
        """Read the call in the thread, storing the result or the fault."""
        try:
            box["found"] = check_call(event, policy)
        except BaseException as error:  # noqa: BLE001 - re-raised below
            box["error"] = error

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(GUARD_WALL)
    if thread.is_alive():
        found = Findings()
        reason = f"command too large to read: more than {GUARD_WALL:g} s"
        found.add("selective-destruction", reason)
        return found
    if "error" in box:
        raise box["error"]
    return box["found"]


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
        answer = decide(read_within_wall(event, policy), policy)
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
