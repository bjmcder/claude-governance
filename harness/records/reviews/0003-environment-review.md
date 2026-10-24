# Review 0003: unit 0003, the environment derived from governance

Independent review (QA.7). Record contents per STND.DFLT.8: revision reviewed, reviewer, findings, and verdict.

| Item | Value |
| --- | --- |
| Revision reviewed | `8736dc3` ("Unit 0003: derive an agent's environment from governance"), against its parent `f23c87b` |
| Reviewer | Claude (independent review agent); not the author of unit 0003 |
| Scope | `govharness/hooks/guard.py`; `govharness/derive/environment/`; `govharness/workflows/environment.py`; `govharness/cli/environment.py`, `cli/arguments.py`, and the registration in `cli/main.py`; `tests/hooks/test_guard.py`, `tests/derive/test_environment.py`, and the changes to `tests/test_architecture.py`; decision 0002 and the record of unit 0003. Against STND.HARN.21 to STND.HARN.24, STND.INSTR.3 and STND.INSTR.4, STND.DFLT.15 and STND.DFLT.22 to STND.DFLT.25 with the term Working bounds, PRIME.5, 7, 9, 12, and 14, GUARD.2, 6, 7, 11, and 13, SIMPL.3, SIMPL.5, INTPR.2, INTPR.3, and VV.7 |
| Fixes | Commits `68865b1` to the commit of this record, by the reviewer, each one fix or one coherent group |
| `governance/` | Unchanged: `git diff --stat 8736dc3 -- governance` prints nothing. The STND.HARN draft text is reviewed separately |

## Method

1. Read the governance named above, the unit's code, tests, and records, and the Claude Code facts given for the review (permissions, managed settings, sandbox, hooks, checkpoints).
2. Gave the guard's parser shell command lines in the forms bash accepts (quoting, compound commands, launchers, substitutions, here-documents, redirections, variables, braces, globs, `cd`, git options) and recorded which outcome each reached. The parser only reads these strings; nothing was run. Each false negative or false positive found became a test that fails on `8736dc3`.
3. Read the generated settings against the stated precedence (deny, ask, allow), the sandbox's reach (shell only), and the hook protocol (exit 0 with JSON, exit 2 blocks, any other exit is a non-blocking error).
4. Checked each coverage claim against what the configuration can and cannot see.
5. Reran the full suite, ruff, and `verify` on the live corpus after the fixes.

## Findings

Severity: Critical, an outcome the guard claims to enforce is evaded by an ordinary shell form; High, a protected location or the enforcing configuration can be reached without the outcome being reached, or the record overstates enforcement; Medium, a stated property does not hold, or routine work is stopped; Low, a local defect, inconsistency, or excess.

| # | Severity | Finding | Disposition | Commit |
| --- | --- | --- | --- | --- |
| 1 | Critical | A command inside a compound command reached no outcome: `if ...; then rm -rf WORK; fi`, `while ...; do ...; done`, `{ ...; }`, and `! ...` | Fixed: reserved words are skipped before the program name | `68865b1` |
| 2 | High | A launcher hid the command it runs when an option took a value (`timeout -s KILL 5`, `env -u X`, `exec -a`) or when the launcher was outside a fixed list (`busybox`, `uv run`, `watch '...'`); `env -C DIR` changed the directory unseen | Fixed: a program the guard does not know is searched for one it knows, a text argument that may be a command line is read, and `-C`/`--chdir` adds a directory | `68865b1` |
| 3 | High | Relative operands were resolved against the starting directory only, so `cd .. && rm -rf work` and `(cd records && ls); rm -r .git` reached no protected-locations | Fixed: every directory the line may run in is tracked, and the line is read again until that set settles; an unknown directory makes relative items computed | `68865b1` |
| 4 | High | Operands were taken literally: `mv $HOME /tmp/x` reached nothing; `rm -rf $HOME`, `rm -rf ~+`, `rm -rf WORK/{records,x}`, and `mv /srv/wor? /tmp/x` reached only a referral; `mv -t DIR SRC` treated the protected source as the destination | Fixed: the tilde, `$HOME`, `$PWD`, and braces are expanded, a pattern is matched against each protected location and its parents, and `-t`/`--target-directory` name the destination. An operand with any other value is computed and referred (STND.DFLT.24) | `68865b1` |
| 5 | High | Process substitution (`cat <(...)`), a here-string to a shell, a shell fed by a pipe, a computed program name (`$X -rf ...`), `xargs` with option values, and `find -exec sh -c` reached no outcome | Fixed: every operator run separates commands, a shell's here-string or here-document is read, a pipe into a shell and a computed program are referred | `68865b1` |
| 6 | High | The sandbox allowed writes to the whole work, which holds `.claude/` and `.mcp.json`. A program run by the shell, naming no path, could rewrite the project settings, which merge sandbox paths and domains and can name commands that run outside the sandbox | Fixed: `sandbox.filesystem.denyWrite` lists every configuration location, now including `~/.claude.json` and `<work>/.mcp.json` | `981908b` |
| 7 | High | `enforcing-configuration` was reported full, so the draft entry would have let STND.DFLT.22 settle it. The file tools run outside the sandbox as the agent's account, which can write `~/.claude` and `<work>/.claude`; only path checks before the call keep them off, and a symbolic link changed in between defeats those | Fixed: reported partial with that gap; the draft entry names no outcome | `987bf9c` |
| 8 | Medium | A here-document's body was read as commands. In Claude Code's own commit form, `git commit -m "$(cat <<'EOF' ... EOF)"`, an apostrophe in the message made the line unreadable, and an unattended session refused the commit | Fixed: bodies are lifted out; a shell's body is read, any other is data, and an unterminated one is read as commands too | `68865b1` |
| 9 | Medium | git forms escaped history-rewrite: abbreviated long options (`--forc`, `--am`), `push --prune`, `branch -f/-M/-C`, `tag -f/-d`, `update-ref` without `-d`, `checkout -B`, `switch -C`. `git rm -r records` and `git mv records old` reached nothing, nor did a command set through `git -c alias.x='!...'` | Fixed | `8a2d465` |
| 10 | Medium | The dry runs that STND.INSTR.4 requires first (`git clean -n`, `rsync -n --delete`, `push --dry-run`) were referred, which blocked the step they precede | Fixed: a dry run reaches no outcome | `8a2d465` |
| 11 | Medium | Redirections: `>& FILE` was not read as a write; the descriptor of `2>/dev/null` became an operand, so `cp a /etc/x 2>/dev/null` checked `2` as the destination; `< FILE` and relative reads (`../../etc/...`) were not checked; `rm --rec` (GNU abbreviation) was not recursive | Fixed | `68865b1` |
| 12 | Medium | Malformed input did not fail closed: an Edit with no `file_path` was checked as the working directory and passed, a command given as a list was parsed as its text, a relative `cwd` defeated every location check, and a policy list given as a string became a tuple of characters. No size limit kept the guard within the hook's 10 s timeout. A Glob pattern outside the bounds was not checked. A subagent's `tool_input.cwd` was ignored | Fixed: each is a fault and denied (PRIME.4); a command over 100 000 characters is referred unread; Glob patterns and `tool_input.cwd` are read. Policy validation and the following of existing symbolic links landed in `68865b1` | `f038336`, `68865b1` |
| 13 | Medium | The hook failed open when its interpreter could not start: exit 127 is a non-blocking error, so the call proceeded | Fixed: the hook command ends in `\|\| exit 2` | `981908b` |
| 14 | Medium | `--home` defaulted to the running account's home. Generated from the owner's administrator account, the configuration protected the wrong `.claude`, and `--check` from the agent's account reported every file as differing | Fixed: `--home` is required; INSTALL.md passes it | `0429777` |
| 15 | Medium | The gap texts left things unsaid: the sandbox does not protect the work's records or version control, inline interpreter code, aliases, and functions are unseen, a tool the owner opens writes unchecked, and a guard that misses its timeout lets the call proceed | Fixed in `coverage.md` and the README | `987bf9c` |
| 16 | Low | A corpus without the outcome or protected-location table ended `environment` in a traceback | Fixed: message, exit 1 | `0429777` |
| 17 | Low | `environment --check` judged an installed symbolic link by its own directories, not by where it leads | Fixed in `ledger.gpg.unalterable`, which also hardens the signer configuration check | `e2b12a7` |
| 18 | Low | An upper-case domain never matched the guard's lower-case host; a tool pattern outside `mcp__` became an allow rule the guard never checks, and one with parentheses is skipped by the settings | Fixed: inputs refuse them | `981908b` |
| 19 | Low | `rm *.o` at the top of the work was refused as emptying the work, though `rm` without recursion removes files alone | Fixed: a non-recursive pattern empties no directory; a pattern of wildcards alone, recursive, still does | `68865b1` |
| 20 | Low | Speculative generality: an adapter registry and `--adapter` with one entry, `--install-root` with no consumer and no documentation (SIMPL.3, SIMPL.5) | Removed | `0429777` |
| 21 | Low | The unit's tests stated no behavior or reference (VV.7) | Fixed | `f1a805f` |
| 22 | Low | The README tree drew `cli/` as the last entry; decision 0002 no longer matched the code after the fixes (INTPR.3) | Fixed. The architecture test's write grant to hooks is kept, since its scan counts `open()` as a write; the grant now says so | `08a78a8`, `885b107` |
| 23 | None | `Edit(**/ledger.jsonl)` does not block the harness's own append, which writes in Python; it does deny a shell redirection to a ledger, which the guard alone would allow | No change; the test states it | `f1a805f` |
| 24 | None | `dontAsk` with the allow list gives unattended work without prompts; an ask rule is then a denial, as the guard's unattended referral is. The deny rules on `.claude` leave the work editable; Claude Code writes its own state there without the file tools | No change | |
| 25 | Low | The guard accepts a subdomain of an opened domain for WebFetch; the sandbox's `allowedDomains` matches exactly. Not a bypass: the stricter one applies to the shell | Open; for the owner to decide whether a domain includes its subdomains | |

## Gaps left as documented

These remain partial, and `coverage.md` states them:

- A program that acts by itself: a script, code given inline to an interpreter (`python -c`, `perl -e`), `make`, a git alias or hook from the configuration, `git --exec-path`, a misspelled subcommand that git corrects, an alias or function defined earlier or in the shell snapshot. The sandbox bounds its writes to the work and the opened paths, but it does not protect the work's records or version control, which lie inside the work.
- An operand whose value the guard does not know (`${X:-/}`, `"$f"`, `{}`) is referred as computed, not refused, even where it could name a protected location. In an unattended session a referral is a denial.
- A symbolic link made in the same command line, and a link changed between the guard's check and a file tool's write.
- The guard reads quoting as bash does for the forms tested. Where the two could differ, such as nested backquotes, lines stay commands rather than becoming data.
- A guard that does not answer within its timeout lets the call proceed. The size limit keeps the guard far below it.
- Reads by programs other than the common readers; writes by tools the owner opens; elevation through a privilege grant the account holds (for example membership of the docker group), which the harness does not check.

## For the STND.HARN text (reported, not edited)

1. STND.DFLT.22 lifts only provisions "of this standard", that is STND.DFLT. Most sources in the table of STND.HARN.21 are PRIME, GUARD, or STND.INSTR provisions, which an entry of STND.DFLT.22 cannot settle even when the outcome is enforced in full. STND.HARN.23 should say which provisions the entry's targets may name.
2. The response to a Refer outcome when nobody can answer, a denial with a referral under PRIME.14, is decided in code and in decision 0002 only. STND.HARN.21 should state it.
3. No outcome covers an action whose items or commands cannot be read (computed items, a shell fed by a pipe, an unreadable line). The code routes them to selective-destruction. The table could name the response.
4. STND.HARN.24 covers installed files only. The configuration also depends on the hook's interpreter and on the user and project settings the agent's account can write. The provision could require a report of each.
5. STND.HARN.22 has no place for conditions. Coverage here holds only while the sandbox is available, the guard answers in time, and the account holds no privilege grant. The provision could require the conditions to be stated with the levels.

## Verdict

Accepted with the fixes above. At `8736dc3` the guard could be passed by ordinary shell forms for every outcome it claims to cover, and the coverage report claimed one outcome in full that was not enforced. After the fixes, the guard catches the forms tested; the settings keep shell programs off the agent's settings and fail closed when the hook cannot run; and no outcome is claimed in full. The configuration is therefore a partial control. Its draft entry settles no provision, so each provision keeps binding the agent, as GUARD.2 requires. Criterion 6 of unit 0003, the passing case of `--check`, still needs confirmation from an unprivileged account on installation.

Results at the commit of this record: `python3 -B -m unittest discover -s tests -t .` passes 111 tests; `ruff check --select E,F,W,I,UP --line-length 79 govharness tests tools` is clean; `python3 -B -m govharness verify governance` passes. The signature tests need a short `TMPDIR`, because gpg's socket path is limited in length.
