"""Adapter for Claude Code: governance outcomes as managed settings.

The adapter renders the outcomes of STND.HARN.18 into three files that
the human owner installs where the agent's account is unable to alter
them, and two reports for the owner:

- ``root/etc/claude-code/managed-settings.json``: the managed settings.
  They make the managed permission rules and hooks the only ones that
  apply. They enable the sandbox, which confines shell commands to the
  writable locations and the opened domains. They refuse or refer, as
  text rules, the commands that the outcomes name.
- ``root/etc/governance/environment.json``: the policy of the guard.
- ``root/etc/governance/guard.py``: the guard that the managed hook runs
  before every tool call (``govharness/hooks/guard.py``).
- ``coverage.md``: how far each outcome is enforced (STND.HARN.19).
- ``entry-draft.json``: the draft entry of STND.DFLT.22, naming only the
  outcomes enforced in full (STND.HARN.20).
- ``INSTALL.md``: the owner's steps: the programs the configuration
  runs, the installation, the check with every option of the
  derivation, and the command that appends the entry.

Everything under ``root/`` installs at the same path under ``/``.
Routine actions inside the working bounds are allowed without a prompt,
so that an agent runs unattended. An allow rule is no authorization
(STND.DFLT.16): every reserved action stays refused or referred.

Decision record: the facts relied on about Claude Code are those of its
documentation for settings, permissions, hooks, sandboxing, and
checkpointing (code.claude.com/docs/en). A text rule matches the
command as written, not what it does, so the guard and the sandbox
carry the enforcement and the rules are a second line.
"""

from __future__ import annotations

import json
import shlex
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import PurePosixPath

from govharness.core.corpus import Corpus
from govharness.core.entry import LEDGER_FILE
from govharness.core.hashing import sha256_bytes
from govharness.derive.environment.inputs import Inputs
from govharness.derive.environment.outcomes import (
    NamedTable,
    Outcome,
    read_outcomes,
    read_protected,
)

ROOT = PurePosixPath("root")
SETTINGS = ROOT / "etc/claude-code/managed-settings.json"
POLICY = ROOT / "etc/governance/environment.json"
GUARD = ROOT / "etc/governance/guard.py"
COVERAGE = PurePosixPath("coverage.md")
ENTRY = PurePosixPath("entry-draft.json")
INSTALL = PurePosixPath("INSTALL.md")
PYTHON = "/usr/bin/python3"
# Programs the configuration runs, checked as installed files are, and
# what each does. On Linux the sandbox of Claude Code needs bubblewrap
# and socat (its documentation for sandboxing); without them, work that
# is not assured runs unsandboxed.
PROGRAM_ROLES = {
    PYTHON: "the interpreter that the hook runs the guard with",
    "/usr/bin/bwrap": "bubblewrap, which the sandbox confines commands with",
    "/usr/bin/socat": "socat, which relays the sandbox's network proxy",
}
PROGRAMS = tuple(PROGRAM_ROLES)
FULL, PARTIAL, NONE = "full", "partial", "none"
RECORDS = "records"  # The directory of STND.DFLT.2.
CHECKPOINTS = (
    (
        "Claude Code checkpoints",
        "change or creation of a file by the Edit, Write, or NotebookEdit "
        "tool of the main session",
    ),
)
# How far this adapter enforces each outcome it knows, and the gap.
COVERAGE_TABLE: dict[str, tuple[str, str]] = {
    "protected-locations": (
        PARTIAL,
        "The guard reads the shell commands and file tools that name a "
        "location, and refers a removal whose items it cannot resolve. "
        "It reads a shell line as the shell does in its quotes, comments, "
        "joined lines, here-documents, substitutions, and compound "
        "commands, and resolves a .. after a symbolic link where the "
        "system resolves it. It refers a line where that reading is "
        "uncertain, as for a comment or case inside a substitution, or "
        "where a second, simpler reading finds a command the first did "
        "not read, and what it cannot read within its bound on paths and "
        "time. The sandbox does "
        "not protect the work, its records, or its version control, which "
        "lie inside the writable work. Not seen: a program that removes "
        "or moves a location by itself, including a script, code given "
        "inline to an interpreter, and an alias or function of the shell "
        "defined earlier; a symbolic link made in the same command line, "
        "or changed between the check and the run; a pattern of the "
        "shell's extglob option.",
    ),
    "history-rewrite": (
        PARTIAL,
        "The guard reads git commands as written. It refers an alias "
        "given in the call, and reads it as the command it stands for; a "
        "setting taken from a variable; a setting given by -c outside a "
        "few that run nothing, whose value it also reads, as it reads a "
        "pager's or an editor's as a command line; a variable of git set "
        "in the call other than those of the author and committer, whose "
        "value it also reads; an ext:: or fd:: URL, and a transport "
        "program named by --upload-pack, --receive-pack, --exec, or "
        "clone's -u, whose command it also reads; a write of git's "
        "configuration other than a few settings that run nothing; and "
        "every subcommand "
        "that is not a command of git, which covers most aliases set "
        "earlier, an external command such as git lfs, and a misspelling "
        "that git corrects. Not seen: git run by a script or a hook, a "
        "program that a configuration written by another program has git "
        "run, and an alias in the configuration named like one of git's "
        "script commands, such as submodule, where that script is not "
        "installed. By the re-review of unit 0015, these stay unseen as "
        "known limits: a -c or --config setting that clone or submodule "
        "gives after the subcommand; the first file of git merge-file "
        "shifted by a valued option; and a git variable set other than "
        "as a literal NAME=value word.",
    ),
    "record-entries": (
        PARTIAL,
        "Ledger files are protected from the file tools and from shell "
        "commands that name them, by name or by a pattern that may match "
        "them, or a pattern whose bracket expression the guard does not "
        "read, which is referred; other records are not, and a program "
        "that rewrites a "
        "ledger is not seen, including an archive extracted over one.",
    ),
    "elevated-privilege": (
        PARTIAL,
        "Commands that elevate are refused; the outcome is enforced in "
        "full only where the agent's account holds no privilege grant, "
        "which the harness does not check.",
    ),
    "write-bounds": (
        PARTIAL,
        "The sandbox confines shell commands. The guard also checks the "
        "destinations of the shell writers it models, among them "
        "redirections, copies and moves, rsync, tar, compressors, the "
        "outputs of curl, wget, sort, zip, unzip, and xxd, the files "
        "that sponge, ed, and ex write, and the "
        "directories and files that git init, clone, worktree, archive, "
        "config, bundle, merge-file, and the output options of its diff, "
        "log, show, and format-patch write. The "
        "guard confines the file tools by the path it checks before the "
        "call, so a symbolic link changed between the check and the "
        "write is not seen. Servers of other tools run outside the "
        "sandbox.",
    ),
    "read-bounds": (
        PARTIAL,
        "The guard refers reads by the file tools and by the shell "
        "programs it reads given a path: common readers, searches by "
        "grep and rg, sed, awk, and their files of patterns, dd, xxd, "
        "openssl, the sources of a copy, rsync, or archive, and the files "
        "that a command run by find takes; other programs read unseen.",
    ),
    "network-bounds": (
        PARTIAL,
        "The sandbox confines shell commands to the opened domains and "
        "the guard confines web fetch and search; servers of other tools "
        "run outside the sandbox.",
    ),
    "remote-write": (
        PARTIAL,
        "Known writing commands are referred, with their options read "
        "in clusters, joined values, and abbreviations: uploads, "
        "publishers, curl's data and methods, git's pushes and mail, ssh "
        "given a command or fed a script, connectors such as nc and "
        "socat, and every command of gh outside a list of reads; so are "
        "unopened tools of other servers. Not seen: a write by a tool the "
        "owner opens, and a program that writes to an opened domain by "
        "itself.",
    ),
    "selective-destruction": (
        PARTIAL,
        "Recursive, pattern, and computed removals by shell commands are "
        "referred, as are a command that xargs builds from its input "
        "unless its program only reads, a shell that runs a computed "
        "script or reads commands from a pipe or a substitution, also "
        "behind a launcher such as env, nice, or timeout, rg --pre, and a "
        "call too large to read within the guard's bound; "
        "a program that selects items by itself is not seen. By the "
        "re-review of unit 0015, these stay unseen as known limits: a "
        "program word that is computed, a glob, a brace, or split by "
        "env -S, including behind a launcher; a command run through an "
        "alias, ed, ex, or vim, or a joined mapfile -C callback; a git "
        "variable or assignment not given as a literal NAME=value word; "
        "and a write by sed's w command or shuf -o.",
    ),
    "enforcing-configuration": (
        PARTIAL,
        "The managed files are out of the account's reach once "
        "`environment --check` passes, and the sandbox keeps shell "
        "commands off the user and project settings. The file tools run "
        "outside the sandbox as the agent's account, which can write "
        "those settings; the guard and the deny rules check the path "
        "before the call, so a symbolic link changed between the check "
        "and the write is not seen.",
    ),
}
# What a provided secret store adds to the gap of an outcome.
STORE_GAPS: dict[str, str] = {
    "read-bounds": (
        "While the sandbox runs, it keeps shell commands from reading the "
        "entries of the secret store other than the opened files, by a "
        "pattern for the entries and a narrower allowance for each opened "
        "file; a program that the guard does not read, such as an "
        "interpreter or an archiver, reaches the store only through the "
        "sandbox. The guard checks the file tools and the shell paths it "
        "reads where their links lead, and refers a Grep, or a copy of a "
        "directory, that takes in the store while the store holds a file "
        "not opened, and a read of a computed operand, as by xargs "
        "or a substitution, while it holds one. It compares names as the "
        "file system spells them, so "
        "on a file system that ignores case another spelling of a closed "
        "file is not seen. A tool of another server reads the store "
        "unseen."
    ),
    "write-bounds": (
        "While the sandbox runs, it denies shell commands every write in "
        "the secret store, so an opened secret is written by the file "
        "tools, which the guard checks by path. A shell command therefore "
        "neither changes the store's permissions nor removes a file of it, "
        "so the agent refers the restoring of the permissions that "
        "STND.DFLT.30 asks for, and the removal of a secret the work no "
        "longer needs. The guard refuses a move or removal that takes in "
        "the store while it holds a file not opened."
    ),
}
# What authorizations of remote writes add to the gap of remote-write.
AUTHORIZED_GAP = (
    "A git push or a tracker post that a standing authorization names "
    "by destination, kind, and branches, compared as whole strings, gets "
    "an allow from the guard (STND.HARN.29) only where the call is one "
    "command of plain words, with no expansion, substitution, "
    "redirection, here-document, or separator; git or gh is named "
    "without a path; no assignment, global option, or option outside a "
    "short list is given; a post carries literal text with no @ and no "
    "file; and, for a push, the command runs inside the work, the first "
    "repository found is the work's own and valid, the remote has one "
    "address, the refspecs name local branches only, the repository "
    "holds no hook, and the git configuration that the guard reads (the "
    "repository's, the worktree's, the account's, and the system's) "
    "rewrites no address and sets no push address, inclusion, alias, "
    "credential helper, hooks path, hook, transport program, proxy, "
    "pushing of tags, recursion into submodules, paging or signing of a "
    "push, key of gpg, policy of protocols, or variant of ssh, while the "
    "guard's environment sets no variable of gh and no variable of git "
    "other than GIT_EDITOR, GIT_SEQUENCE_EDITOR, GIT_PAGER, and "
    "GIT_TERMINAL_PROMPT set to 0 or false, which a push does not read "
    "or reads only to stop a prompt. The text rules that refer every push "
    "and every such post stay, and a permission rule may outrank a "
    "hook's allow; until an installation test shows that the allow "
    "passes, an authorized write may still be referred, and, in an "
    "unattended session, refused. While the sandbox runs, it denies "
    "shell commands every write to the work's .git/config, "
    ".git/config.worktree, and .git/hooks, so a program started earlier "
    "is unable to change them between the check and the push, and git "
    "config and git remote set-url fail in the sandbox. Not seen: a "
    "program that changes the refs, the common configuration of a linked "
    "worktree that lies in a location opened for writing, or the "
    "account's ssh or gh configuration between the check and the write; "
    "what "
    "the remote does with the write, such as a redirection or a "
    "deployment; and the content of a post, which the authorization's "
    "destination alone bounds. The authorization is tested when the "
    "configuration is derived; the guard tests its expiry at each "
    "write, and a revocation takes effect once the configuration is "
    "derived again and installed, which `environment --check` reports "
    "until then."
)
# Text rules by outcome; each goes to "deny" or "ask" by the response.
RULES: dict[str, tuple[str, ...]] = {
    "elevated-privilege": (
        "Bash(sudo *)",
        "Bash(su *)",
        "Bash(doas *)",
        "Bash(pkexec *)",
    ),
    "history-rewrite": (
        "Bash(git push --force *)",
        "Bash(git push -f *)",
        "Bash(git push --force-with-lease *)",
        "Bash(git filter-branch *)",
        "Bash(git filter-repo *)",
        "Bash(git rebase *)",
        "Bash(git commit --amend *)",
    ),
    "record-entries": (f"Edit(**/{LEDGER_FILE})",),
    "remote-write": (
        "Bash(git push *)",
        "Bash(gh issue create *)",
        "Bash(gh issue comment *)",
        "Bash(gh pr comment *)",
    ),
    "selective-destruction": (
        "Bash(rm -r *)",
        "Bash(rm -rf *)",
        "Bash(rm -fr *)",
        "Bash(git clean *)",
    ),
}
ALLOWED_TOOLS = (
    "Agent",
    "Bash",
    "Edit",
    "Glob",
    "Grep",
    "NotebookEdit",
    "Read",
    "TodoWrite",
    "Write",
)


@dataclass(frozen=True)
class Coverage:
    """How far the configuration enforces one outcome.

    Parameters
    ----------
    outcome : Outcome
        The outcome.
    level : str
        ``full``, ``partial``, or ``none``.
    gap : str
        What the configuration leaves to the agent.
    """

    outcome: Outcome
    level: str
    gap: str


@dataclass(frozen=True)
class Locations:
    """The protected locations of one environment.

    Parameters
    ----------
    paths : tuple[str, ...]
        Absolute locations.
    homes : tuple[str, ...]
        Directories whose direct children are home directories.
    unmapped : tuple[str, ...]
        Rows of STND.INSTR.3 that this adapter does not know.
    """

    paths: tuple[str, ...]
    homes: tuple[str, ...]
    unmapped: tuple[str, ...]


@dataclass(frozen=True)
class Derivation:
    """How the configuration was derived, so that INSTALL.md repeats it.

    Parameters
    ----------
    harness : str
        Absolute path of the directory that holds ``govharness``, from
        which ``python3 -m govharness`` runs.
    corpus : str
        Absolute path of the corpus root the derivation read.
    options : tuple[str, ...]
        Every option of the derivation as it was given, with paths made
        absolute, and without ``--write``; ``--check`` with these
        derives the same files.
    out : str
        Absolute path of the output directory, which holds INSTALL.md.
    """

    harness: str
    corpus: str
    options: tuple[str, ...]
    out: str


# What INSTALL.md names where the caller gives no derivation.
UNSTATED = Derivation("HARNESS", "CORPUS", ("OPTIONS",), "OUT")


LocationRule = Callable[[Inputs], tuple[tuple[str, ...], tuple[str, ...]]]
LOCATION_RULES: dict[str, LocationRule] = {
    "The root of a file system": lambda i: (("/",), ()),
    "The home directory of an account": lambda i: (
        (i.home, "/root"),
        ("/home",),
    ),
    "The top directory of the primary copy of the work": lambda i: (
        (i.work,),
        (),
    ),
    "The directory of STND.DFLT.2": lambda i: ((f"{i.work}/{RECORDS}",), ()),
    "The version-control metadata of the work": lambda i: (
        (f"{i.work}/.git",),
        (),
    ),
}


def protected_locations(table: NamedTable, inputs: Inputs) -> Locations:
    """Map the rows of STND.INSTR.3 to the locations of one environment.

    Parameters
    ----------
    table : NamedTable
        The table of protected locations.
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    Locations
        The locations, and the rows that no rule maps.
    """
    paths: list[str] = []
    homes: list[str] = []
    unmapped: list[str] = []
    for row in table.rows:
        rule = LOCATION_RULES.get(row["Location"])
        if rule is None:
            unmapped.append(row["Location"])
            continue
        found_paths, found_homes = rule(inputs)
        paths += found_paths
        homes += found_homes
    return Locations(tuple(paths), tuple(homes), tuple(unmapped))


def configuration_locations(inputs: Inputs) -> tuple[str, ...]:
    """Return the locations whose change would alter the configuration.

    Parameters
    ----------
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    tuple[str, ...]
        The installed files' directories, and the user and project
        settings and server lists, which can widen the sandbox or start
        a program outside it.
    """
    return (
        "/etc/claude-code",
        "/etc/governance",
        f"{inputs.home}/.claude",
        f"{inputs.home}/.claude.json",
        f"{inputs.work}/.claude",
        f"{inputs.work}/.mcp.json",
    )


def edit_rule(location: str) -> str:
    """Return the Edit rule that covers a location.

    Parameters
    ----------
    location : str
        Absolute path of a file (``.json``) or a directory.

    Returns
    -------
    str
        The rule; ``//`` starts an absolute path, and ``/**`` takes a
        directory's contents.
    """
    suffix = "" if location.endswith(".json") else "/**"
    return f"Edit(/{location}{suffix})"


def assess(
    outcomes: list[Outcome], locations: Locations, inputs: Inputs
) -> list[Coverage]:
    """Return the coverage of each outcome (STND.HARN.19).

    Parameters
    ----------
    outcomes : list[Outcome]
        Outcomes of STND.HARN.18.
    locations : Locations
        The protected locations as mapped.
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    list[Coverage]
        One entry per outcome; an outcome this adapter does not know is
        enforced not at all.
    """
    found: list[Coverage] = []
    for outcome in outcomes:
        level, gap = COVERAGE_TABLE.get(
            outcome.key, (NONE, "This adapter does not know the outcome.")
        )
        if outcome.key == "protected-locations" and locations.unmapped:
            level = PARTIAL if locations.paths else NONE
            gap += " Rows not mapped: " + "; ".join(locations.unmapped) + "."
        if inputs.store and outcome.key in STORE_GAPS:
            gap += " " + STORE_GAPS[outcome.key]
        if outcome.key == "remote-write":
            gap += authorization_gap(inputs)
        found.append(Coverage(outcome, level, gap))
    return found


def authorization_gap(inputs: Inputs) -> str:
    """Return what the authorizations add to the gap of remote-write.

    Parameters
    ----------
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    str
        Empty without authorizations; otherwise the conditions of a
        write passing, each authorization still referred, and each
        destination whose host is no opened domain.
    """
    if not inputs.remote_writes and not inputs.referred:
        return ""
    gap = " " + AUTHORIZED_GAP if inputs.remote_writes else ""
    for line in inputs.referred:
        gap += f" Referred: {line}."
    if inputs.unsigned:
        gap += " " + unsigned_note(inputs.unsigned)
    for write in inputs.remote_writes:
        host = destination_host(write.destination)
        if host not in inputs.domains:
            gap += (
                f" {write.authorization}: {host} is no opened domain, so "
                "the sandbox may refuse the write (network-bounds)."
            )
    return gap


def unsigned_note(unsigned: tuple[str, ...]) -> str:
    """Return the sentence that names authorizations relied on unsigned.

    Parameters
    ----------
    unsigned : tuple[str, ...]
        Identifiers of the authorizations, not empty.

    Returns
    -------
    str
        One sentence for the coverage report and the draft entry.
    """
    return (
        "Relied on unsigned, as the human owner accepted with "
        "--accept-unsigned where no signer register exists: "
        f"{', '.join(unsigned)}; nothing but that acceptance shows that "
        "the human owner, and not an agent, recorded them (unit 0010)."
    )


def destination_host(destination: str) -> str:
    """Return the host of a destination address.

    Parameters
    ----------
    destination : str
        An address that ``authorizations`` admitted.

    Returns
    -------
    str
        Its host, without user or port.
    """
    rest = destination.split("://", 1)[-1]
    authority = rest.split("/", 1)[0].split(":", 1)[0]
    return authority.rsplit("@", 1)[-1]


def guard_policy(
    outcomes: list[Outcome], locations: Locations, inputs: Inputs
) -> dict[str, object]:
    """Return the policy file of the guard.

    Parameters
    ----------
    outcomes : list[Outcome]
        Outcomes of STND.HARN.18.
    locations : Locations
        The protected locations.
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    dict[str, object]
        The policy, in the form ``hooks/guard.py`` reads.
    """
    return {
        "work": inputs.work,
        "writable": list(inputs.writable),
        "readable": list(inputs.readable),
        "protected": list(locations.paths),
        "homes": list(locations.homes),
        "configuration": list(configuration_locations(inputs)),
        "ledgers": [LEDGER_FILE],
        "domains": list(inputs.domains),
        "search": inputs.search,
        "tools": list(inputs.tools),
        "store": inputs.store or "",
        "secrets": list(inputs.secret_paths),
        "remote_writes": [
            {
                "authorization": w.authorization,
                "kind": w.kind,
                "destination": w.destination,
                "branches": list(w.branches),
                # Null for one that lapses only when revoked.
                "expires": w.expires or None,
            }
            for w in inputs.remote_writes
        ],
        "responses": {o.key: o.response for o in outcomes},
        "unattended": inputs.unattended,
    }


# What the hook prints when the guard cannot run for work that is not
# assured: the call proceeds, and the owner and the agent are told.
UNGUARDED = json.dumps(
    {
        "systemMessage": (
            "Governance guard did not run; this call proceeds unguarded and "
            "every provision applies in full (STND.HARN.23)."
        ),
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": (
                "Governance guard did not run; every provision applies in "
                "full (STND.HARN.23)."
            ),
        },
    }
)


def hook_command(assured: bool) -> str:
    """Return the hook command that runs the guard (STND.HARN.23).

    Parameters
    ----------
    assured : bool
        Whether the work is assured (CSQ0 or CSQ1).

    Returns
    -------
    str
        The command. The guard answers with exit 0. Any other exit, such
        as a missing interpreter, becomes exit 2, which blocks the call,
        for assured work, and a printed notice that lets it proceed for
        other work.
    """
    guard = f"/{GUARD.relative_to(ROOT)}"
    run = f"{PYTHON} -I -B {guard} /{POLICY.relative_to(ROOT)}"
    if assured:
        return f"{run} --assured || exit 2"
    return f"{run} || printf '%s\\n' {shlex.quote(UNGUARDED)}"


def git_metadata(inputs: Inputs) -> tuple[str, ...]:
    """Return the git files of the work that a push reads and the guard checks.

    Parameters
    ----------
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    tuple[str, ...]
        The repository's and the worktree's configuration and its hooks
        directory, under ``<work>/.git``. A ``core.hooksPath`` needs no
        entry: the guard refers every push while one is set, and the
        sandbox keeps shell commands from setting one in these files.
    """
    git = f"{inputs.work.rstrip('/')}/.git"
    return (f"{git}/config", f"{git}/config.worktree", f"{git}/hooks")


def settings(outcomes: list[Outcome], inputs: Inputs) -> dict[str, object]:
    """Return the managed settings.

    Parameters
    ----------
    outcomes : list[Outcome]
        Outcomes of STND.HARN.18.
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    dict[str, object]
        The settings, as Claude Code reads them.
    """
    deny: list[str] = []
    ask: list[str] = []
    for outcome in outcomes:
        rules = RULES.get(outcome.key, ())
        (deny if outcome.response == "Refuse" else ask).extend(rules)
    deny += [edit_rule(loc) for loc in configuration_locations(inputs)]
    allow = [*ALLOWED_TOOLS]
    allow += [f"WebFetch(domain:{domain})" for domain in inputs.domains]
    allow += ["WebSearch"] if inputs.search else []
    allow += list(inputs.tools)
    command = hook_command(inputs.assured)
    filesystem: dict[str, list[str]] = {
        "allowWrite": [inputs.work, *inputs.open_paths],
        # The work holds its own settings; a program run by the shell
        # must not rewrite them.
        "denyWrite": list(configuration_locations(inputs)),
    }
    if inputs.store:
        # Read rules take wildcards and the narrower path wins; write
        # rules take no wildcards on Linux, and the documentation does
        # not say that a narrower path reopens one for writing.
        filesystem["denyRead"] = [f"{inputs.store}/*", f"{inputs.store}/.*"]
        filesystem["allowRead"] = list(inputs.secret_paths)
        filesystem["denyWrite"].append(inputs.store)
    if any(w.kind == "commit" for w in inputs.remote_writes):
        # The guard reads these at the call; a program started earlier
        # must not swap them before the push (security review M-a).
        filesystem["denyWrite"] += list(git_metadata(inputs))
    return {
        "allowManagedHooksOnly": True,
        "allowManagedPermissionRulesOnly": True,
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "*",
                    "hooks": [
                        {"type": "command", "command": command, "timeout": 10}
                    ],
                }
            ]
        },
        "permissions": {
            "defaultMode": "dontAsk" if inputs.unattended else "acceptEdits",
            "disableBypassPermissionsMode": "disable",
            "allow": allow,
            "ask": ask,
            "deny": deny,
        },
        "sandbox": {
            "enabled": True,
            # Assured work does not run without the sandbox; other work
            # runs, and Claude Code says that the sandbox is unavailable.
            "failIfUnavailable": inputs.assured,
            "allowUnsandboxedCommands": False,
            "autoAllowBashIfSandboxed": True,
            "filesystem": filesystem,
            "network": {"allowedDomains": list(inputs.domains)},
        },
    }


def digest(text: str) -> str:
    """Return the SHA-256 of a text as UTF-8.

    Parameters
    ----------
    text : str
        File content.

    Returns
    -------
    str
        Hexadecimal digest.
    """
    return sha256_bytes(text.encode("utf-8"))


def entry_draft(
    coverage: list[Coverage],
    installed: dict[PurePosixPath, str],
    unsigned: tuple[str, ...] = (),
) -> dict[str, object]:
    """Return the draft entry of STND.DFLT.22 (STND.HARN.20).

    Parameters
    ----------
    coverage : list[Coverage]
        Coverage of each outcome.
    installed : dict[PurePosixPath, str]
        The files to install, by path under ``root/``.
    unsigned : tuple[str, ...]
        Authorizations relied on unsigned, which the rationale names.

    Returns
    -------
    dict[str, object]
        Fields of the transaction for the human owner to review, sign,
        and append; it names only the outcomes enforced in full.
    """
    full = [c.outcome for c in coverage if c.level == FULL]
    files = "; ".join(
        f"/{path.relative_to(ROOT)} sha256 {digest(text)}"
        for path, text in sorted(installed.items())
    )
    checkpoints = "; ".join(f"{m}: {a}" for m, a in CHECKPOINTS)
    named = ", ".join(f"{o.key} ({o.source})" for o in full) or "none"
    return {
        "type": "configure",
        "actor": "The Human Owner",
        "role": "human owner",
        "authority": ["STND.DFLT.15", "STND.DFLT.22", "STND.DFLT.23"],
        "targets": sorted({o.source for o in full} | {"STND.DFLT.15"}),
        "scope": ["STND/DFLT", "STND/HARN", "STND/INSTR"],
        "rationale": (
            "Record of the Claude Code environment configuration "
            "(STND.DFLT.22). Outcomes enforced in full by configuration "
            f"the agent is unable to alter: {named}. Files: {files}. "
            "Checkpoint mechanism and the actions it covers "
            f"(STND.DFLT.15): {checkpoints}. Every other outcome stays "
            "with the agent, and the provision it comes from applies."
            + (" " + unsigned_note(unsigned) if unsigned else "")
        ),
    }


def coverage_report(
    table: NamedTable, coverage: list[Coverage], inputs: Inputs
) -> str:
    """Render the coverage report (STND.HARN.19).

    Parameters
    ----------
    table : NamedTable
        The table of outcomes as read.
    coverage : list[Coverage]
        Coverage of each outcome.
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    str
        Markdown text.
    """
    rows = [
        f"| {c.outcome.key} | {c.outcome.source} | {c.outcome.response} "
        f"| {c.level} | {c.gap} |"
        for c in coverage
    ]
    return "\n".join(
        [
            "# Coverage of the Claude Code configuration",
            "",
            f"Outcomes read from {table.holder} (status {table.status}). "
            f"Work: `{inputs.work}`. Unattended: "
            f"{'yes' if inputs.unattended else 'no'}. Assured work: "
            f"{'yes' if inputs.assured else 'no'}. Authorizations of "
            "remote writes honored: "
            + (
                ", ".join(
                    f"{w.authorization} ({w.kind} at {w.destination}"
                    + (f", {', '.join(w.branches)}" if w.branches else "")
                    + f", until {w.expires or 'revoked'})"
                    for w in inputs.remote_writes
                )
                or "none"
            )
            + ".",
            "",
            "| Key | Source | Response | Coverage | Gap |",
            "| --- | --- | --- | --- | --- |",
            *rows,
            "",
            "The coverage holds only while every condition holds:",
            "",
            "- the files under `root/` are installed as INSTALL.md states, "
            "and `environment --check` passes;",
            "- the sandbox is available; for assured work the settings "
            "refuse to run without it, and for other work Claude Code runs "
            "and says that it is unavailable;",
            "- the guard answers within its timeout of 10 s; it refers a "
            "call it cannot read within its own bound on paths and time, "
            "and, as a backstop, refers any reading that passes a hard "
            "wall of 7 s, so a stalled reading is referred rather than "
            "left to time out;",
            "- the agent's account holds no privilege grant.",
            "",
            "In an unattended session the guard refuses what it would "
            "refer, so the agent halts that line of work and refers it "
            "(PRIME.14).",
            "",
            "Where the guard cannot run or cannot read its policy, assured "
            "work refuses the call; other work lets it proceed and tells "
            "the human owner and the agent (STND.HARN.23). A call the "
            "guard cannot read is refused at every class.",
            "",
        ]
    )


def shell_command(groups: list[list[str]]) -> str:
    """Render one shell command, a group of words to a line.

    Parameters
    ----------
    groups : list[list[str]]
        Words of the command, grouped as the lines should hold them,
        such as an option with its value; an empty group is skipped.

    Returns
    -------
    str
        The command, each word quoted for the shell where it needs it,
        and each line after the first continued and indented.
    """
    return " \\\n    ".join(shlex.join(words) for words in groups if words)


def option_groups(options: tuple[str, ...]) -> list[list[str]]:
    """Group options with their values, one option to a line.

    Parameters
    ----------
    options : tuple[str, ...]
        Options as the command takes them.

    Returns
    -------
    list[list[str]]
        Each option with the words that follow it up to the next one.
    """
    groups: list[list[str]] = []
    for word in options:
        if word.startswith("--") or not groups:
            groups.append([word])
        else:
            groups[-1].append(word)
    return groups


def install_notes(
    inputs: Inputs,
    draft: dict[str, object],
    derivation: Derivation = UNSTATED,
) -> str:
    """Render the installation steps for the human owner.

    Parameters
    ----------
    inputs : Inputs
        The owner's statement of the environment.
    draft : dict[str, object]
        The draft entry, whose fields the command that appends it
        repeats.
    derivation : Derivation
        How the configuration was derived; without it, the steps name
        placeholders.

    Returns
    -------
    str
        Markdown text. The check repeats the corpus root and every
        option of the derivation, so that it renders the same files
        (unit 0014).
    """
    files = (SETTINGS, POLICY, GUARD)
    install = [
        f"install -o root -g root -m 0644 {path} /{path.relative_to(ROOT)}"
        for path in files
    ]
    module = ["python3", "-B", "-m", "govharness"]
    check = shell_command(
        [
            [*module, "environment", derivation.corpus],
            *option_groups(derivation.options),
            ["--check"],
        ]
    )

    def field(name: str) -> str:
        """Return a field of the draft as ``ledger append`` takes it.

        Parameters
        ----------
        name : str
            Name of the field.

        Returns
        -------
        str
            Its value; a list's items separated by commas.
        """
        value = draft[name]
        return ",".join(value) if isinstance(value, list) else str(value)

    append = shell_command(
        [
            [*module, "ledger", "append", derivation.corpus],
            ["--type", field("type")],
            ["--actor", field("actor")],
            ["--role", field("role")],
            ["--authority", field("authority")],
            ["--targets", field("targets")],
            ["--scope", field("scope")],
            ["--sign", "KEY"] if inputs.assured else [],
            ["--rationale", field("rationale")],
        ]
    )
    programs = [f"- `{path}`: {role}." for path, role in PROGRAM_ROLES.items()]
    placeholders = [
        (
            "HARNESS, CORPUS, OPTIONS, and OUT are placeholders: the "
            "directory that holds `govharness`, the corpus root, every "
            "option of the derivation but `--write`, and the directory "
            "that holds this file."
        ),
        "",
    ]
    signature = (
        ", with your signature (STND.DFLT.23); KEY is your signing key."
        if inputs.assured
        else "; for work that is not assured it needs no signature and "
        "displaces no provision (STND.DFLT.22, STND.DFLT.23)."
    )
    revocation = [
        (
            "The guard lets the remote writes of each authorization named "
            "here proceed until it expires. After revoking one, derive and "
            "install the configuration again, since the installed policy "
            "does not read the ledger (STND.HARN.29)."
        ),
        "",
    ]
    return "\n".join(
        [
            "# Installing the Claude Code configuration",
            "",
            (
                "The human owner installs these files from an administrator "
                "account; an agent never does (PRIME.9)."
            ),
            "",
            *(placeholders if derivation == UNSTATED else []),
            "## Before installing",
            "",
            (
                "The configuration runs these programs, and the check below "
                "reports each one that is missing or that the agent's "
                "account is able to alter (STND.HARN.21):"
            ),
            "",
            *programs,
            "",
            (
                "Install any that is missing, at that path, from the "
                "system's packages. Without the sandbox's programs Claude "
                "Code does not start assured work, and runs other work "
                "unsandboxed, saying that the sandbox is unavailable."
            ),
            "",
            "## Install",
            "",
            (
                "From a root shell, inside the output directory of the "
                "derivation, which holds this file, since the paths of the "
                "files are relative to it:"
            ),
            "",
            "```sh",
            shlex.join(["cd", derivation.out]),
            "install -d -o root -g root -m 0755 /etc/claude-code"
            + " /etc/governance",
            *install,
            "```",
            "",
            "## Check",
            "",
            (
                "Then, from the agent's account (not root), confirm that "
                "the installed files match and that the account cannot "
                "alter them or the programs above (STND.HARN.21). Run the "
                "check from the directory that holds `govharness`, as "
                "below. It names the corpus root that the derivation read, "
                f"`{derivation.corpus}`, and every option the derivation "
                "was given; a check with other options renders other files "
                "and reports that they differ from their generation."
            ),
            "",
            "```sh",
            shlex.join(["cd", derivation.harness]),
            check,
            "```",
            "",
            "Expected: `environment: PASS`.",
            "",
            "## Record",
            "",
            (
                "Last, review `coverage.md` and `entry-draft.json`, and "
                "append the entry, with the type `configure` "
                "(STND.HARN.7), to the corpus ledger, "
                f"`{derivation.corpus}/{LEDGER_FILE}`{signature} The "
                "command below repeats the fields of `entry-draft.json`. "
                "Where the entry ends a transition (GOV.42) that waits on "
                "an installed configuration, name that ledger entry in the "
                "rationale before appending. From the directory that holds "
                "`govharness`:"
            ),
            "",
            "```sh",
            shlex.join(["cd", derivation.harness]),
            append,
            shlex.join([*module, "verify", derivation.corpus]),
            "```",
            "",
            *(revocation if inputs.remote_writes else []),
        ]
    )


def render(
    corpus: Corpus,
    inputs: Inputs,
    guard_source: str,
    derivation: Derivation = UNSTATED,
) -> dict[PurePosixPath, str]:
    """Render every file of the Claude Code configuration.

    Parameters
    ----------
    corpus : Corpus
        Indexed corpus holding STND.HARN.18 and STND.INSTR.3.
    inputs : Inputs
        The owner's statement of the environment.
    guard_source : str
        Text of ``govharness/hooks/guard.py``.
    derivation : Derivation
        How the command derived the configuration, which INSTALL.md
        repeats; it changes no installed file.

    Returns
    -------
    dict[PurePosixPath, str]
        Text by path relative to the output directory.

    Raises
    ------
    LookupError
        If a table of governance is missing or malformed.
    ValueError
        If the outcomes table is inconsistent.
    """
    table, outcomes = read_outcomes(corpus)
    locations = protected_locations(read_protected(corpus), inputs)
    coverage = assess(outcomes, locations, inputs)
    installed = {
        SETTINGS: json.dumps(settings(outcomes, inputs), indent=2) + "\n",
        POLICY: json.dumps(
            guard_policy(outcomes, locations, inputs), indent=2
        )
        + "\n",
        GUARD: guard_source,
    }
    draft = entry_draft(coverage, installed, inputs.unsigned)
    return {
        **installed,
        COVERAGE: coverage_report(table, coverage, inputs),
        ENTRY: json.dumps(draft, indent=2) + "\n",
        INSTALL: install_notes(inputs, draft, derivation),
    }
