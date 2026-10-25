# Review of harness unit 0015 (guard fixes), commit b0083f8

Independent review against QA.8 part A and the brief's scale. Worktree `.claude/worktrees/agent-ad057d9bd6c7fc7c8`; parent main (fa21303). No file edited but this report. Probes and mutation runs: `/tmp/claude-1000/review-0015/`. Tests: `tests.hooks.test_guard`, `test_remote_writes`, `tests.derive.test_environment`, `test_authorizations`, `tests.test_architecture`, `tests.test_conventions`: 176 tests, OK (19 s).

**Verdict: do not accept as closing H1, H3 and H7.** Every original reproduction of H1 to H7 and M1 to M6 now reaches an outcome, H4 holds, and ordinary work is unchanged except as listed. But new inputs through the same constructs still return no outcome, one of them is a regression from main, and the docstring and README claim more than the code does. Five High findings below.

## High

**N1. A `#` after an escaped character starts a comment in the guard and not in the shell (H1 not closed).** `lift_heredocs` sets `last = piece[-1:]`, and an escape pair is one piece, so `\ `, `\;`, `\(`, `\|`, `\&` leave `last` as a word boundary. All return `[]`; bash runs the second command (confirmed: `bash -c 'echo a\ #x; echo RAN'` prints `a #x` and `RAN`):
- `echo a\ #x; sudo id`, `echo \;#x; sudo id`, `echo \(#x; sudo id`, `echo \ #x; sudo id`, `echo $x\ #c; sudo id`
- `echo a\ #$(sudo id)` (the substitution is in the word, and runs)

Same result on main. Fix: after an escape pair, set `last` to a non-boundary character. Add tests.

**N2. A comment inside a backquoted span hides the rest of the line (H1 not closed).** `lift_heredocs` tracks `'`, `"`, `$(`, `${`, but not the backquote, so a `#` inside one drops the text through the end of the line, closing backquote included. `echo `ls # x`; sudo id`, `x=`ls # y`; sudo id`, and `echo `echo a # x`; rm /srv/work/ledger.jsonl` all return `[]`. Bash: `bash -c 'echo `echo A # x`; echo B'` prints `A` and `B`. The two-line form is caught. Same result on main. Fix: track the backquote; a comment inside ends at the next one.

**N3. Regression from main: a `case` pattern inside `$(...)` hides the command after it.** `echo $(case x in x) sudo id;; esac)` returns `[]` (main: `elevated-privilege`). Also `... in x|y)`, `... in *)`, `... sudo id ;; esac)`, `... rm /srv/work/ledger.jsonl;; esac)`. Cause: `substitutions()` (guard.py about 3775) closes the span at the pattern's first `)`, and the L2 change in `split_commands` (a command goes on after the `)` that closes an interrupted `(`) now makes `sudo id` an argument of `echo`. Related, with the same paren counting and on main as well: the same form inside double quotes, and in a here-document body (`cat <<EOF` / `$(echo hi # )` newline `sudo id)` / `EOF` returns `[]`; the shell runs `sudo id`). Fix: make `substitutions()` read quotes, comments and `case` patterns, or refer a span it cannot close soundly; add a test for each.

**N4. H7 is not closed: POSIX classes and links in a directory part.**
- `echo x > ledger.[[:alpha:]]sonl`, `ledger.[[.j.]]sonl`, `ledger.[[=j=]]sonl`, `ledger.json[[:lower:]]` return `[]`. Bash overwrote `ledger.jsonl` with each (confirmed in scratch). `matches()` (about 1432) uses `fnmatch`, which reads `[[:alpha:]` as a set. Fix: read `[:class:]`, `[.x.]`, `[=x=]` or refer a bracket expression that contains `[:`, `[.`, `[=`.
- With `g2 -> g -> .git` in the work, `echo x > g?/config` returns `[]` (and `g*/config`). Patterns are matched against link names, not what the links lead to. The shell writes `.git/config`. Fix: resolve each matching entry, or refer.

The docstring ("A pattern reaches the outcome of each protected name it may match") and the README say otherwise.

**N5. Bypasses next to the fixes, not in the QA.8 list, left or opened by them.**
- `sh < <(echo sudo id)` returns `[]`. L2 covers `bash <(...)` and `source <(...)`, but the text is in the call here too. `echo sudo id | sh` is caught.
- `rg --pre 'sudo id' foo` and `rg --pre=sudo foo` return `[]` (main too). M4 made `rg` a read-only `XARGS_READERS` member, so `echo x | xargs rg --pre sudo foo` now also returns `[]`; main returned `elevated-privilege`. A regression.
- `git log --output=ledger.jsonl`, `git diff --output=ledger.jsonl`, `git show -o ledger.jsonl`, `git bundle create ledger.jsonl HEAD`, and `git format-patch -o /etc/x HEAD~1` return `[]` (write-bounds and record-entries). M5 handled `git archive --output` only. `git archive -o ledger.jsonl HEAD` is caught.

## Medium

**N6. The tests do not hold four of the fixes (mutations on a scratch copy).** I ran 28 mutations of `guard.py` against `tests.hooks.test_guard`: 22 are killed (one of them only by a syntax error of mine) (comment rules, `[^`, quoted delimiters, `-I`, `reset`, `--no-`, CDPATH, backquotes, the deadline and path count, the TooLarge referral, `--assured`, setuid forms, `restore`, the unknown-subcommand referral, `CONFIG_PLAIN`, `PROCESS_FILE`). Survivors (six; the sixth, `MAX_DEPTH` raised to 64 000, is equivalent, since a recursion fault is also denied):
- the join of `\<newline>` in an unquoted here-document body (`.replace("\\\n", "")` removed): `cat <<EOF` / `$\` newline `(sudo id)` / `EOF` would then bypass, and no test says otherwise;
- the replace string of `xargs -i` and of `--replace` (only `-I` is tested): `echo hmod | xargs -iat cat u+s f` runs `chmod u+s f`;
- `named_paths` keeping only the physical path, which the record says `cd l/..` needs.

**N7. Reads of the store that the readers list lets through.** With a store holding `key`: `find secrets | xargs cat`, `cat $(find secrets -type f)`, `zip -r /tmp/z secrets`, `xxd secrets/key`, `grep -f secrets/key f`, `sed -f secrets/key f`, `awk -f secrets/key`, `openssl enc -in secrets/key`: all `[]`. `XARGS_READERS` says "computed arguments change nothing", which holds for write outcomes but not for read-bounds. The record says `xxd` is left out for another reason; that is a choice, but `xxd secrets/key` is then unread. Same on main.

**N8. The record and docs overstate the git rule.** Git runs an external `git-<name>` before an alias, so an alias hides no command that exists, but one that is absent can be aliased. `git --list-cmds=builtins` omits `send-email`, `request-pull`, `mergetool`, `filter-branch`, `submodule` from `GIT_COMMANDS`. Where `git-email` is not installed (a separate package on Debian), `git -c alias.send-email=push send-email --force origin main` runs a forced push and the guard reaches `remote-write` (Refer) only, with no `history-rewrite`. The scripts exist on this host, so I did not demonstrate it. Fix: refer a `-c alias.*`, or drop the non-builtin names.

## Low

- **Friction, judged.** About 260 everyday commands (build, test, lint, git inspection and commit, grep, `sed -n`, here-document commit messages, comments in scripts, file edits) were run against main and the worktree. Eleven changed outcome, all in the record's list, plus `tee >(cat) < f` (now referred) and `[[ abc =~ ^(a|b)c$ ]]` (now passes). Justified: `git config --global`, `git worktree add ../wt`, `xargs sed -i`, the unknown-subcommand referral, `git reset file.txt` (ambiguous with a branch). Doubtful: `git reset HEAD~1` and `--soft HEAD^` are Refuse; QA.8 suggested a referral, and undoing one's own unpushed commit is common. The record should say why Refuse. Also referred now: `git diff --name-only | xargs ruff check` (and `black`), and `git reset .`, `git reset src/`. `cd src && rm a.o` and `cd src && echo x > out.txt` are referred on main too (checked); the record is right.
- Unread on main as well: `git clone 'ext::sudo id'`, `GIT_SSH_COMMAND='sudo id' git fetch`, `echo sudo id | env sh`, `echo x | sponge ledger.jsonl`.

## What I checked and found sound

- **Findings.** All H1 to H7 and M1 to M6 reproductions in the report, plus about 40 variants, reach an outcome. Held under variants: H1 comments after `$(`, in `$(...)`, `${#x}`, `$#`, joined lines; H2 `-c alias`, `--config-env`, `GIT_CONFIG_*`, config forms; H3 nested bodies, `<<-`, quoted delimiters; H5 40 xargs option forms; H6 link chains, `cd l/..`, `$PWD/l/..`, the Write tool; H7 `[^`, `[!`, ranges, brace plus glob, `**`, every writing program I tried.
- **H4.** The reviewer's `slow2.py` input (83 KB) is referred in 0.43 s; 47 hand-built families (30 000 lines, 3 000 here-documents, 10 000 substitutions, 63-deep nesting, brace nests, `{1..99999999}`) answer in under 0.5 s; a fuzz of 394 program names against 13 argument patterns at about 90 KB had a worst case of 0.82 s. Depth 65 raises, and `main` turns it into a denial. The deadline and path count are killed by mutation, and `--assured` gives `ask` or `deny` (tested, mutation killed).
- **Documentation not contradicted by the code:** the `coverage.md` condition on the timeout, the `xargs` and gh-reads statements, the Not-seen list, and the Open list in the record, including `cd src && rm a.o`.

## Note on my own run

A stray `EOF` in one scratch command made a list of probe lines run in my shell, in `/tmp/claude-1000/review-0015`. Almost all failed (no network, credentials, permission, or file). `git config --global alias.p push` succeeded; I removed it with `--unset`, and `~/.gitconfig` holds only `[user]` again.
