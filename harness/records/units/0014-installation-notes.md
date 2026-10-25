# Unit 0014: installation notes

The installation-kit check of 2026-10-25 (`review-records/round-2026-10-25-close/install-kit.md`) found five things that stand between the human owner and the installation tests of unit 0008 (`tools/install-tests.md`):

1. Medium: the `--check` line of INSTALL.md kept only `--work` and `--home`, so, run as printed, it reported "differs from its generation".
2. Low: INSTALL.md said neither where to run the install lines nor where to run the check, and it left the corpus root as `CORPUS`.
3. Low: INSTALL.md told the owner to append the entry to "the work ledger", with no command.
4. Low: INSTALL.md named no prerequisite, though the sandbox needs bubblewrap and socat on Linux.
5. The guard referred every push while any `GIT_` variable was set. Claude Code sets `GIT_EDITOR=true` in the agent's shell, so an authorized push could always be referred, which defeats unit 0008.

## Definition of done

1. The check that INSTALL.md prints repeats the corpus root and every option of the derivation that applies, as the derivation was given it: `--open`, `--domain`, `--tool`, `--search`, `--unattended`, `--secret-store`, `--secret`, `--authorization`, `--role`, `--expiry-horizon`, `--accept-unsigned`, and `--assured`. Run as printed against the installed files, it passes.
2. INSTALL.md says to run the install lines in the output directory and the check in `harness/`. It gives the corpus root as an absolute path. It names the programs the configuration runs, taken from what `--check` tests. It gives the `ledger append` command that adds the draft entry to the corpus ledger, which it names, and it no longer says "work ledger".
3. The guard lets an authorized push stand while the environment sets only variables of git that cannot change the destination, the refs pushed, the transport, the configuration read, or the credentials. Every other `GIT_` variable, and every `GH_` variable, refers as before.
4. Each criterion has a test. The admitted variables each pass, and `GIT_DIR`, `GIT_SSH_COMMAND`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_COUNT`, `GIT_PROXY_COMMAND`, and `GIT_EXEC_PATH` still refer. Every earlier test passes, and ruff adds no finding on the changed files.
5. The README, unit 0008, and `tools/install-tests.md` describe the change. `harness/governance/` is unchanged.

## Record

- Done, in `derive/environment/claude_code.py`:
  - `Derivation` carries the harness directory, the absolute corpus root, the options, and the output directory. `render` and `install_notes` take it. A library caller that gives none gets `UNSTATED`, whose placeholders INSTALL.md names. It changes no installed file, so `--check` compares as before.
  - `install_notes` now has four sections. "Before installing" lists `PROGRAM_ROLES`. "Install" starts with `cd` to the output directory. "Check" starts with `cd` to `harness/` and gives `python3 -B -m govharness environment <corpus> <options> --check`, one option to a line, quoted by `shlex`. "Record" gives `ledger append <corpus>` with the type, actor, role, authority, targets, scope, and rationale of the draft entry, plus `--sign KEY` for assured work, and then `verify <corpus>`. It names the corpus ledger `<corpus>/ledger.jsonl`. It asks the owner to name, in the rationale, any transition (GOV.42) that the entry ends. It does not name entry 53, since the adapter does not know the corpus's history. `tools/install-tests.md`, step 15, gives that sentence.
  - `PROGRAMS` was `/usr/bin/python3` alone. It is now built from `PROGRAM_ROLES`, which adds `/usr/bin/bwrap` and `/usr/bin/socat`. So `--check` reports either one if it is missing or alterable, as STND.HARN.21 asks for each program the configuration runs. The fact relied on is Claude Code's documentation for sandboxing: on Linux the sandbox needs bubblewrap and socat. The paths are those of Arch and Debian. A system that installs them elsewhere fails the check, which fails closed. The adapter installs to `/etc/claude-code`, the Linux location, so it does not cover macOS.
  - `AUTHORIZED_GAP` names the paging of a push and the four admitted variables.
- Done, in `cli/environment.py`: `derivation_options` rebuilds the options from the parsed arguments. It keeps the parser's order and the order of repeated options as given, and it makes paths absolute. It names `--expiry-horizon` wherever an authorization is named, or where the horizon is not the default, so that a later change of the default does not change the check. `derivation_of` builds the `Derivation`, and `HARNESS` is the directory that holds the package.
- Done, in `hooks/guard.py`:
  - `GIT_ADMITTED` holds `GIT_EDITOR`, `GIT_SEQUENCE_EDITOR`, `GIT_PAGER`, and `GIT_TERMINAL_PROMPT`. `push_grant` refers a push while any other `GIT_` variable is set, and its reason now names the first such variable in sorted order.
  - `("pager", "push")` joins `GIT_KEYS`.
  - `post_grant` is unchanged: every `GH_` variable refers.
  - The guard still imports nothing from the package.
- The admitted variables, checked against git(1) and git-config(1) of the installed git 2.56.0 (`man git`, `man git-config`):
  - `GIT_EDITOR` overrides `$EDITOR` and `$VISUAL`, "used by several Git commands when, on interactive mode, an editor is to be launched". `git push` launches no editor. Claude Code sets this variable.
  - `GIT_SEQUENCE_EDITOR` is used "when editing the todo list of an interactive rebase". A push makes no todo list.
  - `GIT_PAGER` sets the pager, which git launches only for a command that pages. A push pages only under `--paginate`, a global option, which refers the push ("an option or assignment precedes it"), or under `pager.<cmd>` for `push`, which the guard now refers. So in an allowed push `GIT_PAGER` names a program that does not run. The key was added for this reason. Without it, a configured `pager.push` would run `GIT_PAGER`, or `core.pager`, during the push, as a program the guard does not read.
  - `GIT_TERMINAL_PROMPT`, set false, makes git "not prompt on the terminal (e.g., when asking for HTTP authentication)". It can only stop a prompt. It supplies no credential and names no helper, address, or program.
  - Probe: a push to a local bare repository with all four variables set to a marker script, and no terminal, succeeded, and no marker was written. A probe under a pseudo-terminal was not run, because the session's isolation hook refused it.
  - Unsure: whether a future git reads any of the four in a push. The reasoning holds for git 2.56. A guard with a pinned git version could test this, but this one has none. Also unsure: whether ssh, or the HTTPS helper that git starts, reads `GIT_TERMINAL_PROMPT` for anything other than prompting. Nothing documented says so.
  - Not admitted: display-only variables such as `GIT_PROGRESS_DELAY` and `GIT_ADVICE`. They appear harmless from their documentation, but no environment is known to set them, and each admission is one more claim that must hold in every git to come. The `GIT_TRACE` family is not display-only: `GIT_TRACE_CURL` with `GIT_TRACE_REDACT=0` writes credentials to a file. `GIT_ASKPASS` supplies credentials. Both still refer.
- Security reviews of unit 0008: the review (`review-records/round-2026-10-24/harn-auth/review-security.md`) and its verification (`verify-security.md`) checked that `GIT_DIR`, `GIT_CONFIG_COUNT`, and `GH_REPO` refer, and the tests keep all three. The review's open question was whether the Bash tool's environment is the hook's. That question is unchanged, and the guard still reads its own `os.environ`. An assignment before git (`GIT_SSH_COMMAND=x git push`, or `GIT_EDITOR=x git push`) still refers, since `bare` is false. L-a of the verification lists `HTTPS_PROXY`, `ALL_PROXY`, `SSH_ASKPASS`, and `SSH_AUTH_SOCK`, which are still not modeled, and this unit does not widen that gap. M2 of the review lists `core.pager` among the keys not read. `pager.push` now closes the path by which a pager could run in a push.
- Tests:
  - `tests/derive/test_environment.py`, class `PrintedCheck`:
    - `test_printed_check_passes`: two derivations on a copy of the corpus. One is unattended with an authorization: `--open`, two `--domain`, `--tool`, `--search`, `--unattended`, `--secret-store`, two `--secret` (one of them `.hidden`), `--authorization`, `--role`, `--expiry-horizon 200`, and `--accept-unsigned`, with an expiry 128 days ahead, beyond the default horizon. The other is assured, with `--assured`, `--secret-store`, and `--expiry-horizon none`. The derived files are installed under a temporary root standing for `/`, and the account's reach is simulated as empty, as in `InstalledCheck`. The check is taken from INSTALL.md and split as the shell splits it. The test asserts that its `cd` is the harness directory, runs it through `main`, and expects exit 0 and `environment: PASS`. The check as it was printed before this unit, with only `--work` and `--home`, reports "differs from its generation".
    - `test_notes_name_the_steps`: INSTALL.md names each program of `PROGRAMS`, among them `/usr/bin/socat`. It changes to the output directory, names `<corpus>/ledger.jsonl`, and no longer says "work ledger". Its `ledger append` names the corpus root and carries the draft's rationale and targets, without `--sign` for work that is not assured.
  - `tests/hooks/test_remote_writes.py`:
    - `test_environment_variable_of_git` (changed): `GIT_DIR`, `GIT_SSH_COMMAND`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_COUNT`, `GIT_PROXY_COMMAND`, `GIT_EXEC_PATH`, `GIT_ASKPASS`, `GIT_TRACE`, `GIT_EDITOR_X`, and `GIT_` each refer. With `GIT_EDITOR` set beside one of them, the push is still referred, and the reason names that variable.
    - `test_admitted_variables_of_git` (new): each admitted variable alone, and all four together, leave `git push origin main` allowed, and `git push origin other` referred.
    - `test_environment_variable_of_gh` (new): `GH_REPO`, `GH_HOST`, `GH_TOKEN`, and `GH_CONFIG_DIR` refer an authorized post. `GIT_EDITOR` leaves it allowed.
    - `test_repository_configuration`: `[pager] push = true` and `[Pager] Push = evil` refer.
- Mutations, each patched in turn:
  - Admitting no variable fails `test_admitted_variables_of_git`.
  - Admitting `GIT_DIR` and `GIT_SSH_COMMAND` fails `test_environment_variable_of_git`.
  - Dropping `pager.push` from `GIT_KEYS` fails `test_repository_configuration`.
  - Dropping any one of the twelve options from `derivation_options` fails `test_printed_check_passes`. The cases were chosen for this. `--secret-store` matters only without `--secret`, so the assured case has it alone. `--expiry-horizon` matters only where the default would refuse, so the expiry lies beyond 90 days.
- Suite: `cd harness && python3 -B -m unittest discover -s tests` ran 251 tests, OK (198 s). Unit 0012 ended at 247, and this unit adds four. After the last edits, which changed only a docstring and a help text, `tests.derive.test_environment`, `tests.hooks.test_remote_writes`, and `tests.test_architecture` were run again: 62 tests, OK.
- Ruff 0.16.10, with the settings it resolves for the tree, on `derive/environment/claude_code.py`, `cli/environment.py`, `hooks/guard.py`, `tests/derive/test_environment.py`, and `tests/hooks/test_remote_writes.py`:
  - These files had 30 findings at 74c7044, where this unit starts. They now have 25. The difference is ISC004 on `claude_code.py`, down from 21 to 16, because `install_notes` now puts each paragraph in parentheses. No finding is new.
  - With `--line-length 79 --select E501`, the count is the same as at 74c7044, and the lines this unit adds are within 79 columns.
- Not changed:
  - `harness/governance/`.
  - Decision 0002. Its row on remote writes says that nothing the guard reads, variables of git among them, "may send it elsewhere or add to it". That still holds, since the admitted variables do neither.
  - `OPEN-ITEMS.md`.
  - The coverage report and the draft entry, beyond the remote-write gap text.
- Open:
  - Whether a work ledger, beside the corpus ledger, should also hold the `configure` entry (install-kit finding 3). That is for the custodian.
  - Whether the hook's environment equals the Bash tool's (security review of unit 0008, open question). This unit makes the answer matter less for `GIT_EDITOR`, but the guard still cannot see a variable that an agent exports in an earlier call.
  - The INSTALL.md that a check renders names `OUT` as its output directory, since `--check` writes nothing. Nobody reads that file.
- Audit:
  1. Met: `test_printed_check_passes`.
  2. Met: `test_notes_name_the_steps`, and `test_printed_check_passes` for the directory of the check.
  3. Met: `test_admitted_variables_of_git`, `test_environment_variable_of_git`, `test_environment_variable_of_gh`, `test_repository_configuration`.
  4. Met: see the tests, mutations, suite, and ruff items above.
  5. Met: README (the environment row and the bullet on remote writes), unit 0008 ("Revision by unit 0014"), and `tools/install-tests.md` (header, steps 1, 2, 4, 8, 9, 14, and 15, and the failure meanings of test 1).

## Review

- The security review of commit 6e9086c (`review-records/harness/review-unit-0014.md`) found no High finding, two Medium (M1, M2), and four Low (L1 to L4). Each is addressed in the section below.

## Revision after review

This section supersedes the statements above where they differ.

- M1: git 2.56 runs a hook defined in the configuration (`hook.<friendly-name>.command` with `.event`, git-config(1)) in a push, and the guard did not read it. The reviewer's probe ran one, and the guard answered `allow`. `hook` now joins `GIT_SECTIONS`, so any key of that section, in the repository's, the worktree's, the account's, or the system's configuration, refers the push. Tests:
  - `test_hook_defined_in_configuration` reproduces the case with a pre-push hook in each of the four files, the hooks directory empty, and expects a referral that names the section.
  - `test_repository_configuration` adds `[hook "h"]`, `[hook.h]`, and `[hook] jobs`.
  - The README and unit 0008 no longer say that the repository's hooks are fully modeled. The README says "hooks directories" and states the change, and unit 0008 has a correction.
- M2: the tests now hold the admitted list closed.
  - `GIT_VARIABLES` in `tests/hooks/test_remote_writes.py` holds, as data, every name in the section Environment Variables of git(1) of the installed git 2.56.0. It also holds those of git-config(1) (`GIT_CONFIG`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0`, `GIT_CONFIG_VALUE_0`), names git reads without listing there (`GIT_CONFIG_PARAMETERS`, `GIT_PROXY_COMMAND`, `GIT_TEMPLATE_DIR`, `GIT_PAGER_IN_USE`), and two look-alikes. That makes 84 names.
  - `test_environment_variable_of_git` sets each name not in a fixed `ADMITTED` of the four, to a word and to the empty string. It expects a referral, also beside `GIT_EDITOR`, with the name in the reason.
  - `test_admitted_list_is_closed` asserts that `guard.GIT_ADMITTED` equals the four, and that each of them is one that git(1) lists.
  - Mutants, each patched in turn and the test file run: admitting any one of the eight that survived the review (`GIT_CONFIG_PARAMETERS`, `GIT_SSH`, `GIT_NAMESPACE`, `GIT_TEMPLATE_DIR`, `GIT_ALLOW_PROTOCOL`, `GIT_PROTOCOL_FROM_USER`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_WORK_TREE`) now fails five subtests or more. So does admitting one of the six the review found caught, or `GIT_PROGRESS_DELAY`. No mutant survives.
- L1: `GIT_TERMINAL_PROMPT` stands only with a value in `PROMPT_OFF`, which is `0` or `false`. git(1) calls it a Boolean whose false value stops the prompt. git-config(1) also reads `no`, `off`, and the empty string as false, but these refer, which fails closed. Any other value refers, and the reason names the variable. `test_admitted_variables_of_git` allows `0` and `false` and refers `1`, `true`, `yes`, the empty string, `FALSE`, `no`, `off`, and `00`. Mutants that admit any value, or only `0`, fail.
- L2: the record above already states that the reasoning holds for git 2.56. The values of `GIT_EDITOR`, `GIT_SEQUENCE_EDITOR`, and `GIT_PAGER` are still not checked, since no allowed push runs them. Hooks and credential helpers inherit the variables, but every hook, now including those in the configuration, refers.
- L3: the guard now refers a push where the configuration sets any key of the sections `gpg` and `protocol`, or `push.gpgSign` or `ssh.variant`, since it does not model them. `gpg.program` and `gpg.<format>.program` name programs of a signed push, `protocol.*` changes which transports git may use, and `ssh.variant` changes how git calls ssh. The cases are in `test_repository_configuration`, and a mutant that drops any of them fails. **This is stricter.** An authorized push that the configuration signs (`push.gpgSign`) is now referred. So is any push from an account with a `gpg` key set, such as `gpg.format = ssh` for signing commits, even where the push itself is not signed. An owner who signs gains nothing from a push authorization until the guard models signing. `AUTHORIZED_GAP`, the README, unit 0008, and `tools/install-tests.md` (step 4) say so.
- L4: left as is. INSTALL.md names the harness directory of the checkout that derived it. If that checkout is a worktree that is later removed, the printed `cd` fails, and the check does not run. It never passes wrongly. The owner derives from the main checkout, as `tools/install-tests.md` does.
- Suite: `cd harness && python3 -B -m unittest discover -s tests` ran 253 tests, OK (201 s). That is two more than before this revision: `test_admitted_list_is_closed` and `test_hook_defined_in_configuration`.
- Ruff 0.16.10 on `hooks/guard.py`, `derive/environment/claude_code.py`, and `tests/hooks/test_remote_writes.py` reports the same findings as before this revision: the 7 earlier ones on the guard and 16 ISC004 on the adapter. With `--line-length 79 --select E501`, the only findings are on lines this unit did not write.
