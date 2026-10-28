# Installing the governance

A project can take up the governance in five ways. Each gives agents and people the same corpus; they differ in what software is involved and in how a revision is pinned. Nothing in the corpus depends on the harness or on the plugin (GOV.38): a project that installs nothing can read and apply the governance from its files alone.

| Option | Suits | Network at install | Pins a revision by |
| --- | --- | --- | --- |
| [1. Claude Code plugin](#1-the-claude-code-plugin) | One person, or a trial, using Claude Code | Yes | Tag or branch in the marketplace source |
| [2. Plugin in a project's committed settings](#2-the-plugin-in-a-projects-committed-settings) | A team using Claude Code | Yes, on each machine | Tag, branch, or commit in `.claude/settings.json` |
| [3. Harness alone](#3-the-harness-alone) | Any agent or person, with Claude Code or without | Yes, for the clone | The checked-out commit of the clone |
| [4. Vendored copy](#4-a-vendored-copy) | An offline or air-gapped project | No, once the copy is made | The commit of the submodule or subtree |
| [5. No software](#5-no-software) | Reading and auditing by hand | No | The copy you read |

## Before you start

The commands on this page use these names:

| Name | Meaning |
| --- | --- |
| `REPO` | Where this repository is cloned from: an `https://` URL ending in `.git`, a `git@host:path` address, or, for a clone on your machine, its path |
| `governance-harness` | The name of the marketplace, from `.claude-plugin/marketplace.json` |
| `governance` | The name of the plugin; its skills appear as `/governance:<skill>` |
| `governance@governance-harness` | The plugin's identifier in Claude Code settings and commands |
| `ledger-202` | An example tag. A tag names a commit of this repository; `git ls-remote --tags REPO` lists the tags that exist |

Requirements:

- git, for every option except the fifth.
- Python 3.11 or later for the harness. It uses the standard library only. If the `z3` solver package is importable, `verify` uses it; otherwise it uses its own solver, with the same results.
- Claude Code with the `claude plugin` commands, for options 1 and 2.
- `pip` or `pipx`, for option 3.

## 1. The Claude Code plugin

The plugin is the directory `harness/` of this repository. It holds the corpus (`harness/governance/`), the harness package, and three skills. It adds no hooks, no commands, no permission rules, and no agent definitions. Its skills are read-only: they give an agent the commands that retrieve provisions, describe where a project keeps its records, and draft a classification for the human owner. They write nothing.

### Add the marketplace

The repository root is a marketplace. In a Claude Code session:

```text
/plugin marketplace add REPO
```

From a shell:

```bash
claude plugin marketplace add REPO
```

To follow a tag or branch rather than the default branch, append it with `#`:

```bash
claude plugin marketplace add https://git.example.org/governance-harness.git#ledger-202
```

The repository's files take about 19 MB, most of them review records that a project does not need. From a shell, `--sparse` checks out only the two directories the plugin uses:

```bash
claude plugin marketplace add REPO --sparse .claude-plugin harness
```

A marketplace added from a local path, such as `claude plugin marketplace add ~/src/governance-harness`, is read in place: the plugin loads from that directory, an edit there takes effect at the next session or `/reload-plugins`, and nothing is pinned. This suits the custodian's own work on the corpus.

### Install at a scope

In a session, `/plugin install governance@governance-harness` opens the plugin's details, where you choose a scope. From a shell:

```bash
claude plugin install governance@governance-harness --scope user
```

| Scope | Setting written | Who gets the plugin |
| --- | --- | --- |
| `user` (the default) | `~/.claude/settings.json` | You, in every project on this machine |
| `project` | `.claude/settings.json`, which the project commits | Everyone who works in the repository; see option 2 |
| `local` | `.claude/settings.local.json`, which git ignores | You, in this repository only; suits a trial |

### Verify

```bash
claude plugin list
```

The list shows `governance@governance-harness` with its version, scope, and status. Because the plugin's manifest has no `version` field, the version is the commit it was installed from.

In a session, type `/` and look for `/governance:consulting-governance`, `/governance:orienting-to-governance`, and `/governance:classifying-work`.

To confirm that the harness runs against the installed corpus, take `installPath` from `claude plugin list --json` and run:

```bash
PYTHONPATH="<installPath>" python3 -B -m govharness show "<installPath>/governance" GOV.38
```

It prints GOV.38, the provision on the harness itself.

### Update

With no `version` field, every new commit of the marketplace is a new version. To update now:

```bash
claude plugin marketplace update governance-harness
claude plugin update governance@governance-harness
```

A marketplace added with `#ref` updates to the latest commit of that ref. Auto-update is off by default for this marketplace; the Marketplaces tab of `/plugin` turns it on or off. A running session keeps the version it loaded until `/reload-plugins` or the next session. Claude Code removes the previous version's directory 14 days after an update.

### Uninstall

```bash
claude plugin uninstall governance@governance-harness --scope user
claude plugin marketplace remove governance-harness
```

Use the scope the plugin was installed at. Removing the marketplace also uninstalls every plugin installed from it.

## 2. The plugin in a project's committed settings

A project can commit the marketplace and the plugin to its `.claude/settings.json`, so that every member who opens the repository in Claude Code gets the same revision. Either run the two commands of option 1 with `--scope project`:

```bash
claude plugin marketplace add REPO#ledger-202 --scope project
claude plugin install governance@governance-harness --scope project
```

or write the settings directly:

```json
{
  "extraKnownMarketplaces": {
    "governance-harness": {
      "source": {
        "source": "git",
        "url": "https://git.example.org/governance-harness.git",
        "ref": "ledger-202",
        "sparsePaths": [".claude-plugin", "harness"]
      }
    }
  },
  "enabledPlugins": {
    "governance@governance-harness": true
  }
}
```

For a repository on GitHub, the source is `{"source": "github", "repo": "<owner>/<name>", "ref": "ledger-202"}`. Commit the file.

When a member opens the repository and accepts the workspace trust dialog, Claude Code clones the declared marketplace in the background, and the plugin loads from it. If the Errors tab of `/plugin` says the plugin "is enabled in project settings but isn't installed here", the member runs, once:

```bash
claude plugin install governance@governance-harness --scope project
```

Cloud sessions do not add marketplaces from a repository's settings, so the plugin is not available there.

### Pin an exact commit

A tag or branch can move. To pin one commit, declare the marketplace inline with a `settings` source whose plugin has a `git-subdir` source and a full 40-character commit hash:

```json
{
  "extraKnownMarketplaces": {
    "governance-pinned": {
      "source": {
        "source": "settings",
        "name": "governance-pinned",
        "owner": {"name": "<project>"},
        "plugins": [
          {
            "name": "governance",
            "source": {
              "source": "git-subdir",
              "url": "https://git.example.org/governance-harness.git",
              "path": "harness",
              "sha": "<40-character commit hash>"
            }
          }
        ]
      }
    }
  },
  "enabledPlugins": {
    "governance@governance-pinned": true
  }
}
```

`git rev-parse ledger-202` in a clone prints the hash of a tag. With this source, each member runs `claude plugin install governance@governance-pinned --scope project` once, since Claude Code does not fetch a plugin with an external source from project settings alone.

### Verify, update, and remove

`claude plugin list` shows the plugin with scope `project`. To move the project to another revision, change `ref` or `sha` and commit; Claude Code fetches the marketplace again when its source in settings changes. A member who wants the plugin off for themselves alone runs `claude plugin disable governance@governance-harness --scope local`. To remove it for everyone, delete the two entries from `.claude/settings.json` and commit, or run `claude plugin uninstall governance@governance-harness --scope project`, which removes it from the shared file.

## 3. The harness alone

The harness is a Python package, `govharness`, with a console script of the same name. It works with any agent that runs shell commands, and for a person at a terminal.

```bash
git clone REPO governance-harness
git -C governance-harness checkout ledger-202
pipx install ./governance-harness/harness
export GOVHARNESS_ROOT="$PWD/governance-harness/harness/governance"
```

In place of `pipx`, a virtual environment works too:

```bash
python3 -m venv .venv
.venv/bin/pip install ./governance-harness/harness
```

`GOVHARNESS_ROOT` names the corpus that `show`, `find`, `context`, `pairs`, and `verify` read when no corpus is named on the command line. Set it in your shell profile, or, for Claude Code, under `env` in a settings file:

```json
{"env": {"GOVHARNESS_ROOT": "/home/me/src/governance-harness/harness/governance"}}
```

Without installing anything, every command also runs from the clone:

```bash
PYTHONPATH=governance-harness/harness python3 -B -m govharness show governance-harness/harness/governance GOV.38
```

### Verify

```bash
govharness show GOV.38
govharness verify
```

`show` prints GOV.38. `verify` runs every check of the corpus and passes, printing one warning, g.18, on three provisions of STND.DRAFT whose three modals the custodian reviewed. By default `verify` keeps a cache of solver results under `~/.cache/govharness/`; `--no-cache` runs without it. A two-second subset of the tests runs from `governance-harness/harness`:

```bash
python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main
```

### Update and uninstall

The corpus is the clone's checked-out commit, so updating the governance is a checkout:

```bash
git -C governance-harness fetch --tags
git -C governance-harness checkout <new tag>
pipx install --force ./governance-harness/harness
```

The last command matters only when the harness code changed. To uninstall, run `pipx uninstall` with the name that `pipx list` shows, unset `GOVHARNESS_ROOT`, and delete the clone.

## 4. A vendored copy

A project that works offline, or that wants the governance revision in its own history, keeps a copy of this repository inside its own.

As a git submodule:

```bash
git submodule add REPO vendor/governance-harness
git -C vendor/governance-harness checkout ledger-202
git add .gitmodules vendor/governance-harness
git commit -m "Vendor the governance at ledger-202"
```

As a subtree, which copies the files into the project's history:

```bash
git subtree add --prefix vendor/governance-harness REPO ledger-202 --squash
```

For an air-gapped machine, make a bundle on a connected one and carry it across:

```bash
git clone --mirror REPO governance-harness.git
git -C governance-harness.git bundle create ../governance-harness.bundle --all
```

On the air-gapped machine, `git clone governance-harness.bundle vendor/governance-harness` makes the copy.

The vendored copy is used through the harness, as in option 3, with `GOVHARNESS_ROOT` set to `vendor/governance-harness/harness/governance` or the `PYTHONPATH` form. With Claude Code, the plugin loads from the copy without network access, either for one session:

```bash
claude --plugin-dir vendor/governance-harness/harness
```

or as a local marketplace, read in place:

```bash
claude plugin marketplace add ./vendor/governance-harness --scope local
claude plugin install governance@governance-harness --scope local
```

### Verify, update, and remove

```bash
git -C vendor/governance-harness log -1 --format='%H %d'
PYTHONPATH=vendor/governance-harness/harness python3 -B -m govharness verify vendor/governance-harness/harness/governance
```

The first prints the vendored commit; the second passes with the g.18 warning. To update a submodule, check out another tag inside it and commit the change; for a subtree, run `git subtree pull --prefix vendor/governance-harness REPO <new tag> --squash`. To remove a submodule, run `git rm vendor/governance-harness` and commit; for a subtree, delete the directory and commit.

## 5. No software

The corpus is plain Markdown and needs no program to read. A copy of this repository, or of its `rendered/` directory alone, is enough:

- [`rendered/`](../rendered/LVL0.md) holds a reading copy of every document, named by identifier. Start with `LVL0.md`.
- [`harness/governance/README.md`](../harness/governance/README.md) maps each identifier to its file: `GOV.38` is `harness/governance/GOV/38.md`.
- [`harness/README.md`](../harness/README.md), in its section on reading and applying the corpus without software, gives each check by hand with `sha256sum`, `sed`, and `gpg`.

To confirm that a file is unchanged, compare its hash with its row in the manifest of its directory:

```bash
sha256sum harness/governance/GOV/38.md
grep '^GOV.38,' harness/governance/GOV/MANIFEST.csv
```

The two hashes match.

## Where a project keeps its own records

A project's records belong in the project's own version control, never in the plugin. Claude Code replaces the plugin's directory on every update, and a clone or vendored copy of this repository is the custodian's corpus, not the project's.

Under the defaults of STND.DFLT, which apply to a project without a project constitution, the locations are fixed:

| What | Where, at the top of the project | Provision |
| --- | --- | --- |
| Every record, including the classification and authorizations | `records/`, or a path that a file in it names | STND.DFLT.2 |
| The project's ledger | `records/ledger.jsonl` | STND.DFLT.5 |
| Working notes | `notes/` | STND.DFLT.6 |
| The workbench | `records/workbench/` | STND.DFLT.28 |
| The store of non-credential secrets, if one is provided | `secrets/`, excluded from version control | STND.DFLT.29 |

A project constitution (STND.PROJ) starts as a copy of the template directory `harness/governance/_PROJECT/NAME/`, taken from the revision the project pins. The copy lives in the project's repository, and its Records section names where the other records go. The harness reads the corpus only: `show` and `find` do not read a project's constitution or ledger. [adoption.md](adoption.md) covers when a project needs a constitution and how the class is recorded.

## Pointing other agents at the governance

Claude Code reads a project's `CLAUDE.md`, and reads `AGENTS.md` when no `CLAUDE.md` exists; a `CLAUDE.md` can include `AGENTS.md` with the line `@AGENTS.md`. Many other coding agents read `AGENTS.md`. A few lines there tell any agent where the governance is:

```markdown
## Governance

This project follows the governance corpus in vendor/governance-harness/harness/governance,
at the commit of that submodule. Its records are in records/ and its working notes in notes/.
The agent instructions are the provisions of STND.INSTR; rendered/STND.INSTR.md in that
repository is a reading copy. `govharness show ID`, `govharness find WORDS`, and
`govharness context WORDS --in-force` read the corpus that GOVHARNESS_ROOT names.
```

Adjust the path to the option the project uses. For a project on the plugin alone, name the plugin instead of a path.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `No module named govharness` | `PYTHONPATH` must name the `harness` directory, the one that contains `govharness/`, not the corpus |
| A syntax error on start | Python is older than 3.11; `python3 --version` shows which |
| `error: argument root: ... no such directory`, exit status 2 | The corpus path is wrong, or `GOVHARNESS_ROOT` is unset where no root is given |
| `find` prints "no item holds a word of", exit status 1 | No item uses those words; the corpus's own terms match best, such as "remote write" rather than "push" |
| The `/governance:` skills do not appear | Open the Errors tab of `/plugin`, then run `/reload-plugins`. A project-scope plugin loads only after the workspace trust dialog is accepted |
| "enabled in project settings but isn't installed here" | Run `claude plugin install governance@governance-harness --scope project` once |
| An update changes nothing | Run `claude plugin marketplace update governance-harness` first. With a `#ref` or `ref` pin, only commits on that ref arrive |
| `verify` writes under `~/.cache/govharness/` | That is its solver cache; `--no-cache` turns it off, and deleting the directory costs only time |
