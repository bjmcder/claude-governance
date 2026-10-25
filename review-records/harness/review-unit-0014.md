# Security review of unit 0014 (commit 6e9086c)

Reviewer: independent, cold. Suite: `python3 -B -m unittest discover -s tests` in WT/harness, 251 tests, OK (201 s). The architecture test passes: the guard imports nothing from the package.

## Verdict

The four admitted variables are safe for git 2.56 push. No High finding. One Medium gap in the guard (older than this unit, but the unit's claim about hooks rests on it), and one Medium weakness in the tests.

## Findings

### Medium

**M1. Config-defined hooks run in a push and are not referred.** `guard.py`, `GIT_SECTIONS` (line 196) and `hooks_present` (line 1914). `git-config(1)` of the installed 2.56 documents `hook.<friendly-name>.command` and `.event`. `hooks_present` reads only the `hooks` directories, and `hook` is not a referred section. Probe: in a scratch repo, `git config hook.h.event pre-push; git config hook.h.command 'touch HOOKRAN'; git push origin main` created HOOKRAN. The guard probe (`/tmp/claude-1000/review-0014/probe.py`) with `[hook "h"] event = pre-push command = evil` in the repository config answered `allow`. A program therefore runs in an "authorized" push that the guard did not read. The README and unit 0008 say an allow holds "only while ... the repository's hooks ... hold nothing the guard does not model"; that is false for config hooks. Reach: it needs a write to `.git/config` or `~/.gitconfig`; the derived sandbox denies the former (M-a), so the risk is bounded by the sandbox, not by the guard. Fix: add `hook` to `GIT_SECTIONS`, with a test. Also consider `gpg`, `protocol`, `ssh`, and `core.editor`/`core.pager` (see L3).

**M2. The tests do not hold the allow list closed.** `tests/hooks/test_remote_writes.py`, `test_environment_variable_of_git`. I patched `GIT_ADMITTED` in a copy with one extra name at a time. The suite still passed for `GIT_CONFIG_PARAMETERS`, `GIT_SSH`, `GIT_NAMESPACE`, `GIT_TEMPLATE_DIR`, `GIT_ALLOW_PROTOCOL`, `GIT_PROTOCOL_FROM_USER`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, and `GIT_WORK_TREE`. It failed for `GIT_DIR`, `GIT_SSH_COMMAND`, `GIT_ASKPASS`, `GIT_EXEC_PATH`, `GIT_TRACE`, and `GIT_CONFIG_COUNT`. The unit's definition of done lists only six as tested. Fix: assert `guard.GIT_ADMITTED == {the four}`, and loop the refer test over every variable in git(1)'s Environment Variables section.

### Low

**L1. `GIT_TERMINAL_PROMPT` is admitted whatever its value.** `=1` is admitted as well as `=0`. git(1): "If this Boolean environment variable is set to false, git will not prompt on the terminal (e.g., when asking for HTTP authentication)". A true value can only allow a prompt that a human answers, and no credential helper is configured, so I rate it harmless. Still, it is wider than the comment claims ("set false"). Fix: admit only `0`/`false`, or word the comment as "any value".

**L2. Nothing is checked on the values of `GIT_EDITOR`, `GIT_SEQUENCE_EDITOR`, and `GIT_PAGER`.** The reasoning holds only because git 2.56 push does not start them. `git-push(1)` mentions neither. `pager.<cmd>` (git-config(1)): "turns on pagination ... when writing to a tty", and "To disable pagination for all commands, set core.pager or GIT_PAGER to cat". The pager path is closed by `pager.push` in `GIT_KEYS`, and `--paginate`, `-c`, and an assignment before git are referred (tested). The unit already records the version dependence. I could not run the pseudo-terminal probe either; I confirmed only that a non-tty push to a local bare repository ran no pager. Hooks and helpers inherit the variables, but every hook and credential section is referred, except M1.

**L3. Other config keys that run programs on a push are unmodeled** (pre-existing, not this unit): `gpg.program` with `push.gpgSign`, `protocol.*`, `ssh.variant`. I could not run a signed push (the local bare remote lacks `--signed` support), so I did not confirm that `gpg.program` runs. Fix: refer the `gpg`, `protocol`, `ssh`, and `hook` sections.

**L4. INSTALL.md embeds the harness path of the deriving checkout.** Derived from a worktree, the printed `cd` names that worktree, which `git worktree remove` would delete. The check then fails to run; it never passes wrongly. Fix: say so in INSTALL.md or print a relative form.

## Checks answered

1. **Admitted variables.** `GIT_EDITOR`: "used by several Git commands when, on interactive mode, an editor is to be launched"; push has none. `GIT_SEQUENCE_EDITOR`: "when editing the todo list of an interactive rebase". `GIT_PAGER`: overrides `$PAGER`; runs only for a paged command. `GIT_TERMINAL_PROMPT`: stops a prompt. None changes destination, refs, transport, configuration, or credentials. Pre-push hooks: `hooks_present` refers any non-`.sample` file in either hooks directory (code read; `core.hooksPath` also refers), but not config hooks (M1). Credential helpers, `url.*`, `alias`, `include`, `core.sshCommand`, and `http.proxy` all refer (probe). `--signed` is outside `PUSH_OPTIONS`. In this shell `env | grep -i ^GIT` shows only `GIT_EDITOR=true`, so nothing else would refer every push here.
2. **Fail-closed.** With `GIT_EDITOR=true` also set, each of `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0`, `GIT_SSH`, `GIT_SSH_COMMAND`, `GIT_ASKPASS`, `GIT_EXEC_PATH`, `GIT_TEMPLATE_DIR`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE`, `GIT_PROTOCOL_FROM_USER`, `GIT_ALLOW_PROTOCOL`, `GIT_TRACE`, `GIT_PAGER_IN_USE`, `GIT_Editor`, `GIT_EDITOR_X`, and `GIT_`, set to `x` or empty, answered `ask`. Lowercase `git_dir` answered `allow`; git does not read it on Linux. An empty-valued admitted variable is allowed. Mutations: see M2.
3. **INSTALL.md.** I derived from a corpus copy; the printed check repeats the root and options and is exercised by `test_printed_check_passes`. The ledger append command is well formed. No secret appears: `--secret` takes a file name only. `--check` reported `program missing or alterable: /usr/bin/socat` here, and `missing:` for each file: it fails closed. Paths are Arch/Debian only (stated).
4. **Records.** The record, README, and unit 0008 agree with the code, except the hook claim in M1.

## Not checked

The pseudo-terminal probe, a real signed push, a remote over ssh or https, the hook's inherited environment in a live session, and macOS.
