# QA.8 review, part A: the guard and the derived environment

Reviewer A. Code at main as found; part: `harness/govharness/hooks/`, `harness/govharness/derive/environment/`, with their tests. Tests run: `tests.hooks.test_guard`, `tests.hooks.test_remote_writes`, `tests.derive.test_environment`, `tests.derive.test_authorizations`: 135 tests, OK (6.6 s). No file edited but this report. Probes are in `/tmp/claude-1000/qa8-a/` (`probe.py` calls `guard.check_call` with the policy of `tests/hooks/test_guard.py`; `slow.py`, `slow2.py` time it). `guard.py:LINE` below is `harness/govharness/hooks/guard.py`.

Each reproduction is a `Bash` call (cwd `/srv/work`) to `guard.check_call` that returned no outcome. I ran the shell side of H1, H2, H6, H7, M2 and M6 in a scratch directory to confirm.

Rating note. The sandbox confines shell writes to the writable set. I rate a miss of a protected thing inside the work (ledger, `.git`, history, privilege) High, since the sandbox does not cover it, and a miss that leaves the work (write, read, network bounds) Medium. Read strictly, M3 to M5 are High.

## High

**H1. Comments and line continuations hide the rest of the command line** (`guard.py:899-911`, `split_commands`). `shlex` keeps its default `commenters = "#"`, and in a word `#` starts a comment, which also swallows the newline. Three forms, all returned `[]`:
- `ls # note\nsudo id` (and `...\ngit push --force origin main`, `...\nrm /srv/work/ledger.jsonl`). A comment line after a command, then a command on the next line, is ordinary agent input. The shell runs both lines.
- `echo a#b; rm /srv/work/ledger.jsonl`, `echo $#; sudo id`, `echo ${#x}; sudo id`. In the shell `a#b`, `$#`, and `${#x}` are words.
- `sud\<newline>o id`, `rm /srv/work/ledg\<newline>er.jsonl`, `git pu\<newline>sh --force origin main`. The shell joins the lines; the guard splits the word at line 909 and reads two harmless commands. (`su\<nl>do id` is caught only by accident, because the first half is a known name.)

Fix: set `lexer.commenters = ""`, remove `\<newline>` outside single quotes before lexing, and cut comments in the code that already tracks quotes (`lift_heredocs` knows where a comment starts). A comment that is read as commands only fails closed. Tests: none holds a comment before a later line (`grep comment tests/hooks/test_guard.py` finds no such case).

**H2. A git alias given in the call hides a push, rebase, or any subcommand** (`guard.py:1540-1600`, `check_git`). `git -c alias.p=push p --force origin main` returned `[]`; so did `git -c alias.p=push p origin +main` and `git -c alias.q=rebase q -i HEAD~3`. I ran the first against a local bare repository: the forced update went through. `git config alias.p push` is also unread (no `config` branch), so two calls do the same. `coverage.md` states "a configured alias ... is not seen", but this alias is written in the call itself, and `check_git` already reads `-c` values (only a `!` alias). Fix: refer any `-c alias.*`, `git config` that writes `alias.*` (or any `git config` write), and any subcommand not in a list of git builtins.

**H3. Substitutions in an unquoted here-document run unseen** (`guard.py:725-830`, `lift_heredocs`; `2378`). The body is lifted out and read only when the program is a shell. `cat <<EOF\n$(sudo id)\nEOF` returned `[]`; so did backticks, `$(rm /srv/work/ledger.jsonl)`, the `<<-EOF` form, and `echo ok <<EOF`. The shell expands an unquoted body. The README and the module docstring claim command substitution is read. Fix: for a delimiter that is not quoted, call `check_line` on each `$(...)` and backtick span of the body. A quoted delimiter (`<<'EOF'`) correctly runs nothing.

**H4. A guard that times out lets the call proceed, and a call can cause the timeout** (`guard.py:58`, `1083-1250`, `2688`; `claude_code.py` `hook_command`, timeout 10). Resolution cost is operands x brace alternatives x directories. With 15 `cd` words, then `rm` and operands like `x/{a,b}{c,d}{e,f}{g,h}{i,j}{k,l}` repeated, the guard took 6.7 s at 10 KB, 21 s at 33 KB, 53 s at 83 KB (`slow2.py`; the 100,000-character cap is no bound). A line that needs more than 10 s, followed by `; sudo id`, gets no answer. The coverage report itself says that a guard that does not answer in time lets the call proceed. For assured work this breaks STND.HARN.23 ("refuse each action for which a program it runs ... fails"), since `|| exit 2` runs only on an exit, not on a kill. Fix: a work budget in the guard (count resolved paths and stop at a limit with `selective-destruction` "too large to read"), `MAX_COMMAND` near 10,000, and `MAX_EXPANSION` x `MAX_DIRECTORIES` x operands capped.

**H5. A command fed through `xargs` is not read** (`guard.py:2408-2415`). Only a known program among the arguments is checked. `echo sudo id | xargs env`, `echo sudo | xargs -I@ @ id`, `echo "rm /srv/work/ledger.jsonl" | xargs env`, `... | xargs nice` all returned `[]`. Fix: refer an `xargs` whose program is unknown or is a launcher (`env`, `nice`, `command`, `time`, `sh`), or that takes `-I`.

**H6. A symbolic link plus `..` is resolved lexically** (`guard.py:584-598`, `normalize`, then `real_path` at `601`). `normalize` removes `l/..` before `realpath` can follow the link `l`. With `work/l -> outside/deep` in a scratch work directory, `echo x > l/../evil`, `touch l/../evil`, `rm l/../evil`, `cp a l/../evil` all returned `[]`; the shell wrote `outside/evil`. The link is made by an earlier call (`ln -s /usr/lib l` reaches no outcome: sources of `ln` are not read), so the "same command line" gap in the coverage text is not the only case. Fix: call `os.path.realpath` on the un-normalized joined path (as `real_path` already does for the link step), and refer a path with a `..` after a segment that is a link.

**H7. A glob in a write target is never expanded against the protected names** (`guard.py:1407-1445`, `check_writes`; `check_written` at `1359`). Bash expands a glob in a redirection when exactly one file matches. `echo x > /srv/work/ledger.json?`, `cp /dev/null /srv/work/ledger.jso[n]l`, `tee /srv/work/ledg*.jsonl`, `echo x > /srv/work/.gi?/config`, `echo x > /srv/work/.g*/hooks/pre-push` all returned `[]` (record-entries and history-rewrite are Refuse). I confirmed in a scratch directory that `echo hi > ledger.json?` overwrote `ledger.jsonl`. `rm` has `check_pattern`; the write path has nothing. Fix: for a pattern in a write target, call `check_pattern` or refer it as computed.

## Medium

**M1. Operand-position guesses drop the real target** (`guard.py:2436-2449`). `sed -i --expression=s/a/b/ /etc/passwd` and `sed -i -es/a/b/ /etc/passwd` returned `[]`: `args[1:]` drops the first operand as the script. `chmod --reference=a /etc/passwd` drops the target as the mode. Fix: parse `-e`, `-f`, `--expression`, `--file`, `--reference` first, or check every operand.

**M2. `grants_privilege` misses real setuid forms** (`guard.py:2471-2488`). `chmod 04755 f` (five digits), `chmod u+rs f`, `chmod u+xs f` returned `[]` (`+s` must be a substring; the length must be 4). Shell check: both set the bit. Fix: parse the symbolic clauses; for an octal mode, take the last four digits.

**M3. Remote-write recognition misses common spellings** (`guard.py:1654-1700`, `CURL_WRITES` at `141`). Returned `[]`: `curl -dx URL`, `curl -sd x URL`, `curl -XPOST URL`, `curl -Fa=@f`, `curl -Tf`, `curl --form-string`, `curl -K cfg`; `ssh host < script.sh`; `nc`, `socat`; `gh secret set`, `gh label create`; `poetry publish`, `uv publish`, `git send-email`, `git lfs push`. Fix: read short clusters and joined values for curl, refer `ssh` with stdin, and refer a network program not on a read-only list.

**M4. Reads by programs outside `READERS`, and whole-store reads, are unseen** (`guard.py:106-121`, `2463`; copies at `1461` only for `cp`). With a real store holding `key` and `open.txt`, these returned `[]`: `grep x store/key`, `grep -r x store`, `sed p`, `awk 1`, `base64`, `dd if=`, `find store -exec cat {} +`, `tar cf x.tar store`, `rsync -a store/ /tmp/k`, `install -D store/key /tmp/k`. `TEXT_PROGRAMS` holds `grep` and `rg`, which read files. Fix: apply `check_reads` and `check_copied` to the operands of these programs and to `dd if=`.

**M5. Write destinations of programs the guard does not model** (write-bounds; sandbox backstop). Returned `[]` for a destination outside the work: `rsync a /etc/x`, `tar xf a.tar -C /etc`, `curl -o /etc/x URL`, `wget -O`, `sort -o`, `git archive --output=`, `git config --file /etc/x`, `git config --global alias.p push`, `git init /etc/foo`, `git clone URL /etc/foo`, `git worktree add`, `find -fprint`. Inside the work, `gzip /srv/work/ledger.jsonl` replaces the ledger and returned `[]`. Fix: a list of path-taking write options per program.

**M6. Destructive git forms slip past `dry_run` and the list** (`guard.py:1478-1510`, `1590-1600`). `git clean -n --no-dry-run -f` returned `[]` (I ran it: it removed an untracked file; the last option wins). `git restore --staged --worktree .` returned `[]` (the `--staged` test skips it). `git reset --keep HEAD~5`, `git branch -m a b`, `git symbolic-ref HEAD refs/heads/x`, `git fast-import` also return `[]`. Fix: in `dry_run`, treat any `--no-*` as not dry; test `--worktree` in `restore`; refer `reset` with a ref and `symbolic-ref`.

**M7. The tests do not hold what the module says** (`tests/hooks/test_guard.py`). The docstring claims a line is read "as the shell reads it: quotes, comments, here-documents, command and process substitution". No test has a comment before a later line, `#` or `\<newline>` inside a word, an expansion in an unquoted here-document, a joined `sed -e`, a five-digit chmod, `--no-dry-run`, a glob in a write target, `link/..`, or an `xargs` fed command. The suite passes while H1 to H7 return `[]`. Add one test per input here.

## Low

- L1. `CDPATH` is not modeled: `CDPATH=/etc:. ; cd ssl; echo x > cert` is read in the work. `enter_directory` (`2340`) could refer a `cd` when the line assigns `CDPATH`.
- L2. `source`/`.` is unread, including `. /dev/stdin <<< 'sudo id'` and `bash <(echo sudo id)`, whose text is in the call.
- L3. `coverage.md` (`COVERAGE_TABLE`) names none of H1 to H7; the module docstring's "read as the shell reads it" should list what is not read.

## What I tried that held

- Privilege and quoting: `sudo`/`su`/`doas` through quotes, paths, assignments, compound commands, `time`, `exec`, `command`, `nice`, `env`, `bash -c` in all option forms and nested, `eval`, `find -exec`, `xargs sudo`, `$(...)`, backticks, `<(...)`, computed names (`$cmd`, `s${x}udo`, `$'sudo'`): refused or referred.
- Removals of `/`, `~`, `$HOME`, `.`, `..`, `*`, `.git`, `records`, in brace, glob, `//` and `..` forms, `find -delete`, `git rm`, `git mv`: held.
- Ledger writes by every redirection form, `tee`, `dd of=`, `sed -i`, `perl -pi`, `truncate`, `shred`, `cp`, `mv`, `ln -sf`, `install`, when the name is literal.
- Forced push forms, including option abbreviations (`--force-w`, `--del`), `+ref`, `:ref`, `-f`, `git -C dir push`: held.
- Web URL reading (`pypi.org.evil.com`, `\@`, `#@`, `%2f@`, userinfo, ports, IP literals) held.
- Malformed input (non-JSON, empty, a list, a non-string command, a relative or missing `cwd`, NUL, an over-long line): denied or read.
- Push grants: I found no path to an `allow`. The `PLAIN_RE` and single-command rule dropped it for separators, comments, launchers, `-c`, `-C`, assignments, a path to git, unknown options, `--tags`, `-o`, `--receive-pack`.
- Derived configuration: `settings()`, `guard_policy`, `hook_command` (assured `|| exit 2`), INSTALL.md (quoting, the check repeats every option), the entry draft, and `authorizations.py` against STND.HARN.29 rows Status, Grantor, Extension, Record, Signature, Dates, Standing, Form held. An outcome key missing from `COVERAGE_TABLE` gets `none`, and the guard denies a key the policy omits. The one point against HARN.23 is H4.

## Not checked

The installed hook under a real Claude Code session (so whether a hook timeout blocks or proceeds is taken from the coverage text); macOS; a signed push; the signer register path (part B).
