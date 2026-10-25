# Re-review of harness unit 0015 (guard fixes), commits b0083f8, 78430a1, 9b57626

Independent re-review against the QA.8 brief's scale. Worktree `.claude/worktrees/agent-ad057d9bd6c7fc7c8`, branch head 9b57626. Scripts: `/tmp/claude-1000/rereview-0015/`. Tests (`test_guard`, `test_remote_writes`, `test_environment`, `test_authorizations`, `test_architecture`, `test_conventions`): 193 OK in 7 s. I edited no file but this report.

**Verdict: do not accept.** Every input of N1 to N8 and H1 to H7, M1 to M6 now reaches an outcome (35 N inputs rerun, the unit's probes rerun, 1 423 old inputs compared). The second pass is sound against the shell on what I fuzzed. But the second pass added a quadratic that reopens H4 (a regression from main), and the third pass's claims about launchers, `env -S`, git variables and `-c` settings are broken by short inputs. I confirmed each High below in bash with a fake `sudo` on PATH in a scratch directory and a throwaway HOME.

## High

**R1. H4 is open again: `lift_heredocs` is quadratic (regression).** `substituted = "$(" in stack or "`" in stack` (guard.py about 1160) scans the whole stack for each character, and `(`, `((`, `${` grow the stack. `scan.spend` is not called there, so `TIME_BUDGET` never fires. `check_call` took, on a 100 KB line (under `MAX_COMMAND`):
- `"(" * 99990`: 19.5 s; `echo ` + `"( " * 45000`: 13 s; `"((" * 45000`: 16 s; `"${" * 45000`: 6.7 s. Main: 0.05 s for the first.
- Growth is quadratic (10 KB 0.17 s, 20 KB 0.67 s, 40 KB 2.6 s).
The hook's timeout is 10 s and a timed-out guard lets the call proceed, so `echo ( ( ... ; sudo id` goes unguarded, `--assured` included (`|| exit 2` does not run on a kill). `coverage.md` ("ends well inside the timeout"), the docstring and the README claim otherwise. No test builds a deep-opener line, and no mutation of `TIME_BUDGET` is killed (it is patched). Fix: count `$(` and backquotes beside the stack, call `scan.spend` in the loop, and test 90 KB of `(`.

**R2. A computed word after a launcher is not referred, which also defeats the `GIT_` rule (main too).** Bare `$x id` is referred, but behind a launcher it is not: `x=sudo; env $x id`, `command $x id`, `exec "$x" id`, `nohup`/`timeout 1`/`setsid`/`stdbuf -o0`/`nice`/`time $x id`, all `[]` and all run `sudo` in bash. The assignment rule falls the same way: `env $(echo GIT_SSH_COMMAND=sudo) git ls-remote git@host:r`, `export $(cat e.env)`, `x=GIT_SSH_COMMAND=sudo; env $x git ...`, `export $x=sudo; git ...` return `[]`, and `sudo` ran. `check_assignments` sees only literal `NAME=value` words, and `echo`/`grep`/`printf` in a substitution are text programs. Fix: refer a computed word in those positions.

**R3. `env -S` in its attached and escaped forms (main too).** `check_launched` reads a word only if it holds a blank or `;&|`. All return `[]`, and `sudo` ran: `env -S'sudo\_id'`, `env -S 'sudo\_id'`, `env --split-string 'sudo\_id'`, `env -S"sudo\_id"`, `nice env -S'sudo\_id'`. Also `[]` (the program is split by `env`): `env --split-string='sudo id'`, `env -S"sudo id"`, `env -Ssudo id`. Fix: read the value of `-S`/`--split-string` as a command line, with `\_` as a blank.

**R4. A glob or a brace in the program word (main too).** `../bin/sud? id`, `/usr/bin/su[d]o id`, `../bin/s*o id`, `../bin/*udo id`, `{sudo,id}`, `s{u,u}do id`, `{su,}do id`, `{bash,-c,'sudo id'}`, `{env,sudo,id}`, `env ../bin/sud? id` all return `[]` and `sudo` ran (`../b?n/sudo` is caught only because the base name is literal). The same holds for `rm` and `git`, so it bypasses every Refuse. Fix: refer a program word that has a glob character or a brace.

**R5. `git clone -c KEY=VALUE` and `--config` bypass the new `-c` rule.** `git clone -c core.sshCommand=sudo git@host:r d`, `--config core.sshCommand=...`, `--config=...` return `[]` and ran `sudo` (the attached `-ccore...` is referred only by luck). `check_git` reads `-c` only before the subcommand. The docstring and `coverage.md` say a setting given by `-c` outside the plain list is referred.

**R6. Assignment forms the regex skips.** `GIT_SSH_COMMAND+='sudo id' git ls-remote git@host:r` returns `[]` and ran `sudo`. So do `printf -v GIT_SSH_COMMAND %s 'sudo id'; export GIT_SSH_COMMAND; git ls-remote ...` and `read GIT_SSH_COMMAND <<< ...; export GIT_SSH_COMMAND` (`export NAME` has no `=`). `export`, `declare`, `local`, `readonly`, `typeset`, `env -S 'GIT_X=..'` with a literal `NAME=value` are caught; `+=` is not. Fix: match `NAME+=`, and refer `export`/`declare -x` of a bare `GIT_*` name, `printf -v` and `read` into one.

## Medium

**R7. `git merge-file` operand shifted by a valued option.** `git merge-file -L x ledger.jsonl a b`, `--label x`, `--marker-size 5`, `--diff-algorithm patience` return `[]` (`--marker-size=5`, `-q`, `-Lx` are caught). git overwrites the first file (shown in scratch). The N5 fix takes `named[:1]` of operands, which count the value of `-L` as the file. Ledger overwritten: record-entries (Refuse) is missed.

**R8. `ed` and `ex` scripts are not read.** The unit adds them as writers of the files they name, but `ed -s a.txt <<< '!sudo id'`, `printf 'w ledger.jsonl\nq\n' | ed -s a.txt`, `ex -sc '!sudo id|q' a.txt`, `ex -sc 'w ledger.jsonl|q' a.txt` all return `[]`. Not run (`ed` and `ex` are not installed here); `!` and `w FILE` are their documented commands. `vim -es -c wq` and `sed 'w ledger.jsonl'` are also `[]`.

**R9. Aliases and callbacks (main too).** `shopt -s expand_aliases` / newline / `alias a=sudo` / newline / `a id` returns `[]` and ran `sudo`. `mapfile -Csudo -c1 a <<< x` and `-c1 -Csudo` return `[]` (the spaced `-C sudo` is caught).

**R10. Tests that do not hold what the record claims (surviving mutants on a scratch copy, 52 run, one at a time).** Killed: 41. Survivors that matter:
- `check_launched` with `word in KNOWN` instead of the base name: `timeout 5 /usr/bin/sudo id` is unheld.
- `GIT_CONFIG_PARAMETERS` added to `GIT_PLAIN`: the record names it as covered; no test.
- `key.startswith("hook")` made plain: `git -c hook.x.command=...` unheld.
- `sponge` or `ex` dropped from `KNOWN`: `nice sponge ledger.jsonl` unheld.
- `os.path.lexists` to `exists` in `pattern_items`: a dangling link into a ledger is unheld.
- `reset` target `@`; upper-case `EXT::`; `MAX_COMMAND`; the timing of R1.
The rest of the escape, backquote, comment, `case`, second-reading, POSIX class, output-operand, `ext::`/`fd::`, alias, `-c`, shell-fed, `MAX_PATHS`, CDPATH and store-read mutations were killed; the `scan.programs` variant, `pager.` and `sequence.editor` are equivalent.

## Low

- **Documentation.** The docstring, README and `coverage.md` claim more than the code: the timeout (R1), "a launcher does not hide one" (R2 to R4), "a variable of git set in the call is referred" (R2, R6), "a setting that `-c` gives is referred" (R5).
- `shred -u L`, `L` a link to `ledger.jsonl`, overwrites the ledger and returns `[]` (main too).
- Unseen, main too: `git submodule add u /etc/x`, `git checkout -f`, `git pull --rebase`.
- `case` and `#` doubts also refer harmless text: `grep -rn "\#include" src`.

## Closure and what held

- **Closure.** All 35 N1 to N8 inputs and the unit's probe and probe3 inputs reach an outcome.
- **Fuzz against bash.** About 56 000 random lines (escapes, `#`, backquotes, `$(`, `case`, here-documents, `$'`, `${`, `$((`, `\<newline>`) run in bash with fake `sudo`, `rm` and `git`: whenever a fake ran, the guard reached an outcome. About 85 hand-built comment, escape, backquote and `case` lines: none.
- **Second reading.** Sound as a backstop for slips in the first reading. It cannot help where both read the same wrong thing (R2 to R4). Its `word not in scan.programs` test is call-wide, so an earlier `sudo` masks a missed later one.
- **Links and globs.** 138 forms over links, `..`, `[[:class:]]`, braces and absolute globs: one miss (`shred -u L`). About 70 launcher forms behind pipes and substitutions held.
- **`git -c` and the plain list.** No key on `CONFIG_PLAIN` or `PLAIN_PREFIXES` runs a program; `include.path`, `core.fsmonitor`, `url.*.insteadOf`, `core.hooksPath`, `gpg.program` and case variants are referred. `ext::` and `fd::` in `remote add`, `ls-remote`, `fetch`, `--origin` and `%s` forms are referred; a computed URL is not, but git blocks `ext` by default (not run).
- **H4 otherwise.** 47 families of mine answer in under 0.4 s; only R1's openers pass the timeout.
- **Friction.** The 244 inputs of `e1`/`e3` and about 190 of mine changed from main as follows:
  - `git reset HEAD~1` and `--soft HEAD~1`: referred (justified; the corpus does not settle it).
  - `xargs ruff check`, `xargs black`, `xargs sed -n` after a pipe: referred, though the program only reads (Low friction of H5's rule).
  - `xargs sed -i`, `git config --global`, `git worktree add ../wt`, `awk ... /etc/passwd`, `git lfs pull`, `tee >(cat)`: referred (justified).
  - `grep -rn "\#include" src`: referred (overbroad, Low).
  - `[[ abc =~ ^(a|b)c$ ]]` now passes (better).
  Commits with a quoted here-document, comment lines and continuations pass.

## Note on my own run

My first case file used a here-document whose body held a line `EOF`, so the rest of its lines ran in my shell in the scratch directory. They failed there (no repository or network; one `sudo` was refused); I removed four stray files. `~/.gitconfig` holds only `[user]`. Later lines ran only through `env -i` with a throwaway HOME and a fake PATH.
