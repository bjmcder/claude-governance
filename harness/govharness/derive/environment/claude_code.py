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
# Programs the configuration runs, checked as installed files are.
PROGRAMS = (PYTHON,)
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
        "The sandbox does not protect the work, its records, or its "
        "version control, which lie inside the writable work. Not seen: "
        "a program that removes or moves a location by itself, including "
        "a script, code given inline to an interpreter, and an alias or "
        "function defined earlier; a symbolic link made in the same "
        "command line.",
    ),
    "history-rewrite": (
        PARTIAL,
        "The guard reads git commands as written; git run by a script, "
        "a configured alias, a hook, or a misspelled subcommand that git "
        "corrects is not seen.",
    ),
    "record-entries": (
        PARTIAL,
        "Ledger files are protected from the file tools and from shell "
        "commands that name them; other records are not, and a program "
        "that rewrites a ledger is not seen.",
    ),
    "elevated-privilege": (
        PARTIAL,
        "Commands that elevate are refused; the outcome is enforced in "
        "full only where the agent's account holds no privilege grant, "
        "which the harness does not check.",
    ),
    "write-bounds": (
        PARTIAL,
        "The sandbox confines shell commands. The guard confines the "
        "file tools by the path it checks before the call, so a symbolic "
        "link changed between the check and the write is not seen. "
        "Servers of other tools run outside the sandbox.",
    ),
    "read-bounds": (
        PARTIAL,
        "The guard refers reads by the file tools and by common shell "
        "readers given a path; other programs read unseen.",
    ),
    "network-bounds": (
        PARTIAL,
        "The sandbox confines shell commands to the opened domains and "
        "the guard confines web fetch and search; servers of other tools "
        "run outside the sandbox.",
    ),
    "remote-write": (
        PARTIAL,
        "Known writing commands and unopened tools of other servers are "
        "referred. Not seen: a write by a tool the owner opens, and a "
        "program that writes to an opened domain by itself.",
    ),
    "selective-destruction": (
        PARTIAL,
        "Recursive, pattern, and computed removals by shell commands are "
        "referred; a program that selects items by itself is not seen.",
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
        "not opened. It compares names as the file system spells them, so "
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
    "credential helper, hooks path, transport program, proxy, pushing of "
    "tags, or recursion into submodules, while the guard's environment "
    "sets no variable of git or gh. The text rules that refer every push "
    "and every such post stay, and a permission rule may outrank a "
    "hook's allow; until an installation test shows that the allow "
    "passes, an authorized write may still be referred, and, in an "
    "unattended session, refused. Not seen: a program that changes the "
    "configuration, the refs, or the account's ssh or gh configuration "
    "between the check and the write, such as one started earlier; what "
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
    for write in inputs.remote_writes:
        host = destination_host(write.destination)
        if host not in inputs.domains:
            gap += (
                f" {write.authorization}: {host} is no opened domain, so "
                "the sandbox may refuse the write (network-bounds)."
            )
    return gap


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
    coverage: list[Coverage], installed: dict[PurePosixPath, str]
) -> dict[str, object]:
    """Return the draft entry of STND.DFLT.22 (STND.HARN.20).

    Parameters
    ----------
    coverage : list[Coverage]
        Coverage of each outcome.
    installed : dict[PurePosixPath, str]
        The files to install, by path under ``root/``.

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
            "- the guard answers within its timeout of 10 s; a guard that "
            "does not answer in time lets the call proceed;",
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


def install_notes(inputs: Inputs) -> str:
    """Render the installation steps for the human owner.

    Parameters
    ----------
    inputs : Inputs
        The owner's statement of the environment.

    Returns
    -------
    str
        Markdown text.
    """
    files = (SETTINGS, POLICY, GUARD)
    lines = [
        f"install -o root -g root -m 0644 {path} /{path.relative_to(ROOT)}"
        for path in files
    ]
    return "\n".join(
        [
            "# Installing the Claude Code configuration",
            "",
            "The human owner installs these files from an administrator "
            "account; an agent never does (PRIME.9).",
            "",
            "```sh",
            "install -d -o root -g root -m 0755 /etc/claude-code "
            "/etc/governance",
            *lines,
            "```",
            "",
            "Then, from the agent's account, confirm that the installed "
            "files match and that the account cannot alter them "
            "(STND.HARN.21):",
            "",
            "```sh",
            "python -m govharness environment CORPUS --work "
            f"{inputs.work} --home {inputs.home} --check"
            "  # with the same inputs",
            "```",
            "",
            "Last, review `coverage.md` and `entry-draft.json`, and append "
            "the entry to the work ledger"
            + (
                " with your signature (STND.DFLT.23)."
                if inputs.assured
                else "; for work that is not assured it needs no "
                "signature and displaces no provision (STND.DFLT.22, "
                "STND.DFLT.23)."
            )
            + " Append it with the type `configure` (STND.HARN.7).",
            "",
            *(
                [
                    "The guard lets the remote writes of each authorization "
                    "named here proceed until it expires. After revoking one, "
                    "derive and install the configuration again, since the "
                    "installed policy does not read the ledger "
                    "(STND.HARN.29).",
                    "",
                ]
                if inputs.remote_writes
                else []
            ),
        ]
    )


def render(
    corpus: Corpus, inputs: Inputs, guard_source: str
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
    return {
        **installed,
        COVERAGE: coverage_report(table, coverage, inputs),
        ENTRY: json.dumps(entry_draft(coverage, installed), indent=2) + "\n",
        INSTALL: install_notes(inputs),
    }
