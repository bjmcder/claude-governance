# Installation kit (definition of done, part C, items 11 and 12)

Prepared on 2026-10-25 by Claude, agent, at the lead's direction. Nothing was installed, nothing under `/etc` was written, no root access was used, and no Claude Code session ran under the configuration. The live corpus is unchanged: `harness/governance/ledger.jsonl` still holds 147 entries. The owner's steps are in `tools/install-tests.md`.

## Derivation (item 11)

Run from `harness/`:

```sh
python3 -B -m govharness environment governance \
    --work /home/brianm/projects/utils/governance-ledger109 \
    --home /home/brianm/projects/utils/governance-ledger109/.scratch/install-kit/home \
    --secret-store --secret install-test-token \
    --write /home/brianm/projects/utils/governance-ledger109/.scratch/install-kit/out
```

It exited 0 and printed `written: 6 files`. `install-test-token` is an invented name, and no secret exists. The derivation names no authorization: the corpus holds none, and none was created in it. The home is a scratch directory, so this output is for checking only and is not to be installed. The owner derives again with the real home (`tools/install-tests.md`, steps 7 and 14).

Files written, all mode 0644 (directories 0755):

| File | SHA-256 |
| --- | --- |
| `root/etc/claude-code/managed-settings.json` | 2df652929aa0df1f91bbc2ab46c49ea9001d4d189ac6c3e63c91677167cd6cca |
| `root/etc/governance/environment.json` | 88b08e9ab9da13355327e63c248c011e8013fba1dd6f7bf4780bd7d6122e9550 |
| `root/etc/governance/guard.py` | 5922ea8a7409332e56ed5cff277b1a9b5e214858e951e40d6770f055d98b4af0 (byte for byte `harness/govharness/hooks/guard.py`) |
| `coverage.md` | report |
| `entry-draft.json` | draft `configure` entry; its three hashes equal those above |
| `INSTALL.md` | installation steps |

## INSTALL.md against the files written

Every file that INSTALL.md says to install exists in `out/` under the stated `root/...` path. Each one installs to the stated path under `/`, as root:root with mode 0644, after `install -d -m 0755` of both directories. Mode 0644 suits `guard.py`, because the hook runs it through `/usr/bin/python3` and does not execute the file itself. Nothing written is left out. The three files under `root/` are all that INSTALL.md installs, and the last step names `coverage.md` and `entry-draft.json`. `environment --check`, run now, reports the three files missing and nothing else, so the hook's interpreter `/usr/bin/python3` (a link to `python3.14`) passes the test that the agent's account cannot alter it.

Findings:

1. **Medium, fails safe. The `--check` command drops the derivation's options.** INSTALL.md prints `python -m govharness environment CORPUS --work ... --home ... --check  # with the same inputs`. It omits `--secret-store` and `--secret` here, and in general every option other than `--work` and `--home` (`--open`, `--domain`, `--tool`, `--search`, `--unattended`, `--assured`, `--authorization`, `--role`, `--expiry-horizon`, `--accept-unsigned`). I rendered with only the printed options, into `.scratch/install-kit/out-literal-check`. That rendering's `managed-settings.json` and `environment.json` differ from the derived ones, so the printed check, run as written, fails with "differs from its generation". It fails closed: it never passes a wrong installation. The comment is the only hint. The kit gives the full option set (steps 9 and 14). The cause is `install_notes` in `derive/environment/claude_code.py`, which renders only `inputs.work` and `inputs.home`. Not fixed here.
2. **Low.** The install lines use paths relative to the output directory, but INSTALL.md does not say to run them from there. The `--check` line also does not say that `python -m govharness` must run from `harness/`, and it leaves `CORPUS` as a placeholder. The kit states all three (steps 8 and 9).
3. **Low.** INSTALL.md says to append the entry to "the work ledger" and gives no command. `entry-draft.json` holds only the fields that `ledger append` takes as options, and no option reads a draft file. The transition of entry 53 lives in the corpus ledger. The kit appends there, with the full command (step 15), which I rehearsed on a scratch copy: the chain verifies. Whether a separate work ledger should also hold the entry is for the custodian.
4. **Low.** INSTALL.md names no prerequisite. On Linux the Claude Code sandbox needs `bubblewrap` and `socat`. This machine has `/usr/bin/bwrap` but no `socat`. Since the work is not assured, `failIfUnavailable` is false, so Claude Code would start without the sandbox. Tests 2 and 3 would then test nothing. The kit makes installing `socat` its step 2.

## Kit check on a scratch copy (not the live corpus)

To check the kit's steps for the authorized derivation, I copied the corpus to `.scratch/install-kit/preview/corpus` and `kitrun/corpus`. In each copy I added `INSTT/AUTH/1.md` (a commit at `git@github.com:example-owner/install-test.git` on branch `main`, and a post at `https://github.com/example-owner/install-test`). I appended its `authorize` to the copy's ledger and derived with `--authorization INSTT.AUTH.1 --role "Implementing agent" --accept-unsigned`. Steps 5 to 7 of the kit ran verbatim (`.scratch/install-kit/kitrun.sh`). The derivation printed the two summary lines and the unsigned acceptance. Its settings keep the ask rules for `git push` and the three `gh` posts, and add `<work>/.git/config`, `config.worktree`, and `hooks` to `denyWrite` (M-a). `verify --no-logic` on the copy passes every check except the copy's three stale manifests.

I ran the derived guard on each test command, as the hook would and with no session, from the test work directory:

| Command | Guard |
| --- | --- |
| `git push origin main` | allow (INSTT.AUTH.1) |
| `git push origin other` | ask: no authorization names the branch |
| the same push after `cd ... &&` | ask: covered only as the call's one plain command |
| `gh issue comment 1 --repo github.com/example-owner/install-test --body "..."` | allow |
| the same, to `other-repo` | ask |
| `cat secrets/install-test-token` | no answer; left to the rules and the sandbox |
| `cat secrets/key`, `cat secrets/.hidden` | ask (read-bounds) |
| `python3 -c "print(open('secrets/key').read())"`, `ls -la secrets`, `stat` | no answer; the sandbox decides |
| `python3 -c "open('.git/config', 'a')"`, `git config user.name x` | no answer; the sandbox decides (test 3 tests it alone) |
| `printf x >> .git/config` | deny (history-rewrite) |

5. **Finding for the harness, possibly blocking test 1a.** The guard refers every push while any `GIT_` variable is in its environment. This agent's shell, under the Claude Code extension 2.1.309, carries `GIT_EDITOR=true`. With that variable set, the guard answers `git push origin main` with "referred because the environment sets a variable of git". If the hook inherits the variable in the owner's session, test 1a cannot show whether the hook's `allow` outranks the ask rule, and the `gh` post (1c) decides it. The kit says how to tell the two cases apart. Not fixed here. A harness unit could exempt `GIT_EDITOR`, which does not redirect a push.

## What remains for the owner

- After the QA.8 review is merged (items 9 and 10), work through `tools/install-tests.md`: install `socat`; derive the test configuration on a disposable copy of the corpus and a disposable work, with a remote the owner names; install it as root; run `--check` with the full options; then run tests 1 to 3 and record them in unit 0008.
- Derive, install, and check the configuration to keep, and append its `configure` entry to the corpus ledger. That entry ends the transition of ledger entry 53 for STND.HARN.18.
- Record whether the entry-53 transition for STND.HARN.26 to .28 has ended (`OPEN-ITEMS.md`, item 2).
- A production authorization of remote writes needs a project directory with a registered mnemonic in the live corpus (STND.IDENT.23), which is a custodians' step. Without one, the kept configuration refers every remote write, as STND.HARN.18 allows.

Scratch: `.scratch/install-kit/` holds `out/` (the derivation above), `out-literal-check/` (finding 1), `preview/` and `kitrun/` (corpus copies, test works, derivations, and the guard runner `preview/run_guard.py`), and `kitrun.sh`. All of it is disposable.
