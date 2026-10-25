# Installation tests of unit 0008

For the human owner. These steps install the derived Claude Code configuration, run the three installation tests that `OPEN-ITEMS.md` item 2 asks for, record them in unit 0008, and append the `configure` entry that ends the transition of ledger entry 53 for STND.HARN.18. The kit was prepared on 2026-10-25 (`review-records/round-2026-10-25-close/install-kit.md`) and revised for unit 0014, which fixes that check's findings 1 to 5. No agent performs any step here.

Set these in each shell you use, the root shell included:

```sh
REPO=/home/brianm/projects/utils/governance-harness
TEST=/home/brianm/install-test          # disposable; delete it afterwards
AGENT_HOME=/home/brianm                 # home of the account Claude Code runs as
HOST=github.com                         # host of the disposable repository you name
OWNER=your-account                      # its owner on that host
TESTREPO=install-test                   # a disposable repository, never a real one
```

## Before you start

1. The QA.8 code review of the harness (definition of done, items 9 and 10) is merged, and so is unit 0014 (`harness/records/units/0014-installation-notes.md`), which these steps assume. Derive from that harness. A later change to the harness changes the hash of `guard.py`, so derive again after it.
2. As root, install `socat` (`pacman -S socat`). On Linux the Claude Code sandbox needs `bubblewrap` and `socat`. `bubblewrap` is present on this machine, but `socat` is not. Without it, Claude Code runs unsandboxed, because work that is not assured does not require the sandbox, and tests 2 and 3 then test nothing. INSTALL.md lists these programs, and the check of step 9 reports `/usr/bin/bwrap` or `/usr/bin/socat` if either is missing or alterable by the agent's account.
3. On `$HOST`, create the disposable repository `$OWNER/$TESTREPO` and open one issue in it, number 1. Use your SSH key for it. Do not use a credential helper: any `credential` key makes the guard refer every push.
4. As the agent's account, `git config --global --name-only -l` lists no key in the sections `credential`, `url`, `include`, `includeif`, `alias`, `hook`, `gpg`, or `protocol`. It also lists none of `core.hookspath`, `core.askpass`, `core.sshcommand`, `core.fsmonitor`, `core.gitproxy`, `http.proxy`, `push.followtags`, `push.recursesubmodules`, or `submodule.recurse`. Nor does it list `pager.push`, `push.gpgsign`, or `ssh.variant`. A `gpg` key set for signing commits counts too, so leave it out of the agent's account for the test. Also, `env | grep -E '^(GIT|GH)_'` prints nothing in the shell where you start Claude Code, other than `GIT_EDITOR`, `GIT_SEQUENCE_EDITOR`, `GIT_PAGER`, or `GIT_TERMINAL_PROMPT` set to `0` or `false`, which the guard admits (unit 0014). Any one of these makes the guard refer the authorized write.

## Derive the test configuration

5. Make the disposable work, with a secret store that holds three dummy files:

```sh
git init -b main "$TEST/work" && cd "$TEST/work"
git commit --allow-empty -m "install test" && git branch other
git remote add origin "git@$HOST:$OWNER/$TESTREPO.git"
mkdir -m 700 secrets
for f in install-test-token key .hidden; do printf 'dummy\n' > "secrets/$f"; done
```

6. Add the test authorization to a **copy** of the corpus, never to the live corpus. Set `expires` within 90 days of today, or the derivation refuses it (unit 0012):

```sh
cp -a "$REPO/harness/governance" "$TEST/corpus" && mkdir -p "$TEST/corpus/INSTT/AUTH"
cat > "$TEST/corpus/INSTT/AUTH/1.md" <<EOF
---
id: "INSTT.AUTH.1"
level: "LVL3"
kind: "auth"
title: "Installation test writes to a disposable repository"
status: "adopted"
recorded: "$(date -u +%F)"
grantor: "The Human Owner"
action_class: "Commits and tracker posts to a disposable test repository"
scope: "Branch main and the tracker of $OWNER/$TESTREPO"
items_or_volume: ""
standing: true
expires: "$(date -u -d '+14 days' +%FT00:00:00+00:00)"
delegable_to: ["Implementing agent"]
spending_envelope: ""
remote_writes: [{"destination": "git@$HOST:$OWNER/$TESTREPO.git", "kinds": ["commit"], "branches": ["main"], "provisioned": true}, {"destination": "https://$HOST/$OWNER/$TESTREPO", "kinds": ["post"], "branches": [], "provisioned": true}]
---

Installation tests of unit 0008 only.
EOF
cd "$REPO/harness"
python3 -B -m govharness ledger append "$TEST/corpus" --type authorize \
    --actor "The Human Owner" --role "human owner" --authority GUARD.10 \
    --targets INSTT.AUTH.1 --scope INSTT/AUTH \
    --rationale "Grant of INSTT.AUTH.1 for the installation tests of unit 0008."
```

7. Derive, from `$REPO/harness`. Do not pass `--unattended`, which turns every prompt into a refusal. For GitHub, the second domain is `api.github.com`; for another host, give the host that `gh` calls.

```sh
OPTS=(--work "$TEST/work" --home "$AGENT_HOME" --secret-store --secret install-test-token
      --authorization INSTT.AUTH.1 --role "Implementing agent" --accept-unsigned
      --domain "$HOST" --domain "api.$HOST")
python3 -B -m govharness environment "$TEST/corpus" "${OPTS[@]}" --write "$TEST/out"
```

Read the printed `authorization:` lines. They must name the commit at `git@$HOST:$OWNER/$TESTREPO.git` (branch `main`) and the post at `https://$HOST/$OWNER/$TESTREPO`, under the 90-day horizon and accepted unsigned. Nothing else confirms that you granted what the ledger pins (unit 0010).

## Install, as root

8. Run the block under "Install" in `$TEST/out/INSTALL.md` from a root shell. It begins with `cd` to `$TEST/out`, since its paths are relative to that directory:

```sh
cd "$TEST/out"
install -d -o root -g root -m 0755 /etc/claude-code /etc/governance
install -o root -g root -m 0644 root/etc/claude-code/managed-settings.json /etc/claude-code/managed-settings.json
install -o root -g root -m 0644 root/etc/governance/environment.json /etc/governance/environment.json
install -o root -g root -m 0644 root/etc/governance/guard.py /etc/governance/guard.py
```

9. As the agent's account (not root), check the installation. Run the block under "Check" in `$TEST/out/INSTALL.md` as printed. It changes to `$REPO/harness` and names the corpus root and every option of step 7, with paths made absolute. This command is the same check:

```sh
cd "$REPO/harness" && python3 -B -m govharness environment "$TEST/corpus" "${OPTS[@]}" --check
```

Expected: `environment: PASS`. A check with fewer options fails with "differs from its generation". Run it within the expiry horizon of the derivation and before `INSTT.AUTH.1` expires, since the check derives again at that moment.

## Run the tests

10. As the agent's account, run `claude --version` and note the version. Then start a session in the work: `cd "$TEST/work" && claude`. Ask Claude to run each command below exactly as written, as the only command of its call, with no `cd` or `&&`. The guard allows an authorized write only as one plain command. Type HOST, OWNER, and TESTREPO as literal values: the guard refers a command that holds a variable.
11. Sandbox probe: `python3 -c "open('/home/brianm/sandbox-probe', 'w')"` must fail. If it succeeds, the sandbox is not running. Stop and fix step 2 first.

### Test 1: an authorized write proceeds and the ask rules stay

Precondition: `grep -cF 'Bash(git push *)' /etc/claude-code/managed-settings.json` prints 1. The rules for `gh issue create`, `gh issue comment`, and `gh pr comment` are present too.

| Step | Command | Expected |
| --- | --- | --- |
| 1a | `git push origin main` | Runs with no permission prompt. The push itself may still fail on the network or the key inside the sandbox. That is not this test, but note git's output. |
| 1b | `git push origin other` | A prompt whose reason begins "Governance outcome remote-write referred: git push, referred because no authorization in force names". Answer no. |
| 1c | `gh issue comment 1 --repo HOST/OWNER/TESTREPO --body "Installation test of unit 0008"` | Runs with no prompt. |
| 1d | `gh issue comment 1 --repo HOST/OWNER/other-repo --body "Installation test of unit 0008"` | A prompt naming "no authorization in force names". Answer no. |

What a failure means:

- If 1a or 1c is prompted by Claude Code's own permission prompt, with no "Governance" reason, then the ask rule outranks the hook's `allow`. Authorized writes then stay referred: that is safe, but the authorization gains nothing.
- If the prompt carries the guard's reason, read it. "The environment sets a variable of git, NAME" means the session passes that `GIT_` variable to the hook. Claude Code sets `GIT_EDITOR=true` in the agent's shell, but the guard admits it and three others (unit 0014), so the reason names some other variable. Note its name. Test 1a then cannot settle the question, so 1c decides it. Record the variable: it may be one more for the guard to admit.
- If 1b or 1d proceeds without a prompt, the referral is not in force. Remove the installed files and record a defect.

### Test 2: the opened secret is readable, the others are not

| Step | Command | Expected |
| --- | --- | --- |
| 2a | `cat secrets/install-test-token` | Prints `dummy`, with no prompt. |
| 2b | `cat secrets/key`, then `cat secrets/.hidden` | The guard prompts (read-bounds). Answer yes, so that the sandbox decides. Both fail, with permission denied or no such file. |
| 2c | `python3 -c "print(open('secrets/key').read())"` | No prompt, and it fails. |
| 2d | `ls -la secrets`, then `stat -c '%a %U' secrets` | Lists the three names, then prints `700` and your account. |

What a failure means:

- If 2a fails, the store's `denyRead` pattern wins over the narrower `allowRead`. The shell cannot read an opened secret: the configuration fails closed, but `--secret` is useless for shell reads.
- If 2b or 2c prints `dummy`, the sandbox does not close the store. Put no real secret in a store, and record a defect.

### Test 3: a shell write to `.git/config` fails under the M-a `denyWrite`

Precondition: `grep -cF "\"$TEST/work/.git/config\"" /etc/claude-code/managed-settings.json` prints 1. The rule is present only while a commit is authorized.

| Step | Command | Expected |
| --- | --- | --- |
| 3a | `python3 -c "open('.git/config', 'a')"` | Fails with an `OSError`, either read-only file system or permission denied. |
| 3b | `git config user.name install-test` | Fails, because git cannot write the configuration. |
| 3c | `git commit --allow-empty -m "sandbox control"` | Succeeds, because commits still write objects and refs. |

What a failure means: if 3a or 3b succeeds, a program is able to rewrite the git configuration between the guard's check and a push. Do not rely on any authorization of kind commit, and record a defect.

## Record the results in unit 0008

12. Append this section to the end of `harness/records/units/0008-remote-write-authorizations.md`:

```markdown
## Installation tests (YYYY-MM-DD)

Run by the human owner under `tools/install-tests.md`. Claude Code VERSION; `uname -sr`: ...;
harness commit `git -C $REPO rev-parse --short HEAD`: ...

| Step | Observed | Result |
| --- | --- | --- |
| 1a | ... | pass / fail |
| ... (one row per step, 1a to 3c) | | |

Test 1 settles "Installation tests, open" (1) of the Revision after review. Test 2 settles item (2)
there and "Open, from unit 0007". Test 3 settles "Installation test, open" of the Revision after
re-verification.
```

13. Delete `$TEST` and the disposable repository. The test authorization existed only in the copy of the corpus.

## Install the configuration and record it

14. Derive the configuration you mean to keep from the live corpus. Use the options you want, but no `--authorization` unless the custodians have added one to the live corpus under a registered project (STND.IDENT.23):

```sh
cd "$REPO/harness"
python3 -B -m govharness environment governance --work "$REPO" --home "$AGENT_HOME" --write "$REPO/.scratch/install-kit/final"
```

Install it as in step 8, from the block of `final/INSTALL.md`. Check it as in step 9, with the block under "Check" of `final/INSTALL.md`, which names the live corpus and the options of this derivation.

15. Append the `configure` entry to the corpus ledger, `harness/governance/ledger.jsonl`, which holds entry 53. The block under "Record" of `final/INSTALL.md` gives this command, with the corpus ledger named and the fields of `final/entry-draft.json` filled in. Before you run it, add the last sentence below to its rationale, since entry 53's transition ends with this entry. In outline:

```sh
cd "$REPO/harness"
python3 -B -m govharness ledger append governance --type configure \
    --actor "The Human Owner" --role "human owner" \
    --authority STND.DFLT.15,STND.DFLT.22,STND.DFLT.23 \
    --targets STND.DFLT.15 --scope STND/DFLT,STND/HARN,STND/INSTR \
    --rationale "<rationale of entry-draft.json> This configuration is derived by the harness reviewed under QA.8 (harness/records/reviews/<record>), which implements STND.HARN.29, and tested as unit 0008 records; with this entry the transition of ledger entry 53 for STND.HARN.18 ends (GOV.42)."
python3 -B -m govharness verify governance
```

The README describes this command in its Commands section (`ledger append`, which checks the chain and appends one hash-chained transaction). It describes the same append by hand in step 8 of "Reading and applying the corpus without software". For assured work, add `--sign KEY` (STND.DFLT.23).
