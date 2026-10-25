# Verification of the fixes to unit 0014 (commit 3dc588d)

Verifier: cold, no stake. Worktree WT = `.claude/worktrees/agent-a8fa8207c3c0d0edb`, git 2.56.0. Scratch: `/tmp/claude-1000/verify-0014/` (`probe.py`, `mut/`, `suite.txt`). No file was edited except this report.

## Verdict

Ready to merge. No High, no Medium. The fixes close M1, M2, L1, and L3. Three Low notes remain.

## Checks

**1. M1 (config hooks).** Real git first: `hook.<name>.event=pre-push` with `.command` ran in a push from the local config, `config.worktree`, the global file through a scratch HOME, an included file with `[HOOK "h"]`/`EVENT`/`COMMAND`, and a name with dots (`hook.a.b`). That is five placements, all RAN. The guard (probe through the suite's own `Repository`) answered `ask`, reason "sets hook.event" or "hook.command", for:
- local, worktree, global, XDG, and system files;
- dotted name in both forms (`[hook "a.b.c"]`, `[hook.a.b]`);
- mixed-case section and key (`[HoOk "h"]`, `COMMAND`);
- `[include]` and `[includeIf]`/`[INCLUDEIF]`, which refer by their own sections;
- `[hook] jobs`.

A one-line `[hook "h"] event = x` is unreadable and refers.

**2. M2 (closed list).** I copied the harness and patched `GIT_ADMITTED` with one extra name at a time. I ran `tests.hooks.test_remote_writes`, which passes unmutated.
- 19 names, including all 8 that survived the review, `GIT_DIR`, `GIT_SSH_COMMAND`, `GIT_CONFIG_GLOBAL`, `GIT_PROXY_COMMAND`, and `GIT_PROGRESS_DELAY`, each failed 5 subtests.
- `GIT_CURL_VERBOSE` failed 1 subtest. That is enough to kill it, but it is covered less than the rest.
- Refer-logic mutants all failed: `hook`, `gpg`, or `protocol` dropped from `GIT_SECTIONS`; `push.gpgsign` or `ssh.variant` dropped from `GIT_KEYS`; `PROMPT_OFF` widened to `1` or narrowed to `0`; the prompt check removed; a name exempted from the loop; the hook branch removed from the section test. No mutant survived.

**3. L1 and L3.** `GIT_TERMINAL_PROMPT` is allowed as `0` and `false`. It is referred as `1`, `true`, the empty string, `False`, and ` 0`. Referred with a reason that names the key: `gpg`, `GPG`, `[gpg "ssh"]`, `[gpg.ssh]`, `protocol`, `[protocol "file"]`, `[protocol.file]`, `[PROTOCOL "File"]`, `push.gpgSign` in any case or with no value, and `ssh.variant` in any case. An unlisted `ssh.other` and `push.default` still allow, so nothing is over-broad.

**4. No widening.** `git diff main 3dc588d -- guard.py` shows only additions to the refer sets and one replacement: "any GIT_ variable refers" became "any GIT_ variable outside four names refers, and `GIT_TERMINAL_PROMPT` only as `0`/`false`". Nothing else is allowed that main did not. Full suite in WT/harness: 253 tests, OK (199 s).

## Findings

### High
None.

### Medium
None.

### Low

**L-a. The M1 test covers fewer placements than the claim.** `test_hook_defined_in_configuration` writes to local, global, XDG, and system, not to `config.worktree`, an included file, or a dotted name. The code refers on the section alone, so all of these pass today (probed). Fix: add `config.worktree` and `[hook "a.b"]` to the loop.

**L-b. `GIT_CURL_VERBOSE` is killed by one subtest.** The refer loop is strong, but this name has little cover. Fix: none needed; check that the list holds the git(1) names it should.

**L-c. Stricter for signers.** As the record says, any account with a `gpg.*` key, such as `gpg.format = ssh`, has every authorized push referred. This is fail-closed and documented, but the owner will meet it at once. Fix: model signing later, or say so in INSTALL.md (the record says it is in `install-tests.md` step 4). I could not run a signed push; the local bare remote refuses `--signed`.

L4 (a worktree path in INSTALL.md) stays open by decision. It fails safe.

## Not checked
A pseudo-terminal pager probe, a real signed push, ssh or https remotes, macOS.
