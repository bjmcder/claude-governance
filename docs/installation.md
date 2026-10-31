# Installing the governance

A project can take up the governance in five ways. Each gives agents and people the same corpus; they differ in what software is involved and in how a revision is pinned. Nothing in the corpus depends on the harness or on the plugin (GOV.38): a project that installs nothing can read and apply the governance from its files alone.

| Option | Suits | Network at install | Pins a revision by |
| --- | --- | --- | --- |
| [1. Claude Code plugin](#1-the-claude-code-plugin) | One person, or a trial, using Claude Code | Yes | A tag or branch after `#` in the marketplace source |
| [2. Plugin in a project's committed settings](#2-the-plugin-in-a-projects-committed-settings) | A team using Claude Code | Yes, on each machine | A tag or branch in `ref`, or a full commit hash in `sha`, in `.claude/settings.json` |
| [3. Harness alone](#3-the-harness-alone) | Any agent or person, with Claude Code or without | Yes, for the clone, and for `setuptools` if you install the package | A tag or commit hash checked out in the clone |
| [4. Vendored copy](#4-a-vendored-copy) | An offline or air-gapped project | No, once the copy is made, when the harness runs without installing | A submodule: a tag or commit hash. A subtree: a tag or branch |
| [5. No software](#5-no-software) | Reading and auditing by hand | No | The copy you read |

## Before you start

The commands on this page use these names:

| Name | Meaning |
| --- | --- |
| `REPO` | Where this repository is cloned from: an `https://` URL ending in `.git`, a `git@host:path` address, or, for a clone on your machine, its path |
| `governance-harness` | The name of the marketplace, from `.claude-plugin/marketplace.json` |
| `governance` | The name of the plugin; its skills appear as `/governance:<skill>` |
| `governance@governance-harness` | The plugin's identifier in Claude Code settings and commands |
| `ledger-324` | A tag of a published state of the corpus, as described below |

The published repository is `https://github.com/bjmcder/claude-governance.git`, and the examples that give a full URL use it. `REPO` stands for that address, or for the address of a fork or mirror you clone instead; a URL in an example is replaced the same way.

The custodian tags each published state of the corpus `ledger-N`, where N is the number of the last ledger entry it includes: `ledger-324` is the state whose ledger, `harness/governance/ledger.jsonl`, ends at entry 324. A project pins the governance by such a tag, or by a full commit hash wherever the mechanism accepts one. `git ls-remote --tags REPO` lists the tags that exist. What each option accepts:

| Option | Pinned by |
| --- | --- |
| 1 and 2, a marketplace source | A tag or branch, in `#ref` or `ref` |
| 2, a plugin source in settings | A full 40-character commit hash, in `sha` ([Pin an exact commit](#pin-an-exact-commit)) |
| 3, a clone | A tag or a commit hash, given to `git checkout` |
| 4, a submodule | A tag or a commit hash, checked out inside the submodule |
| 4, a subtree | A tag or branch, as a ref of the remote |

Requirements:

- git, for every option except the fifth.
- Python 3.11 or later for the harness. It uses the standard library only. If the `z3` solver package is importable, `verify` uses it; otherwise it uses its own solver, with the same results.
- Claude Code with the `claude plugin` commands, for options 1 and 2.
- `pip` or `pipx`, to install the harness package in option 3, with access to the Python Package Index or a locally installed `setuptools`. Without the package, the harness runs from its directory.

## 1. The Claude Code plugin

The plugin is the directory `harness/` of this repository. It holds the corpus (`harness/governance/`), the harness package, and three skills. It also carries the harness's own records (`harness/records/`) and tests (`harness/tests/`), which a project does not use; the records stay with the plugin because entries of the ledger cite them by path. The plugin takes about 4 MB in all. It adds no hooks, no commands, no permission rules, and no agent definitions. Its skills are read-only: they give an agent the commands that retrieve provisions, describe where a project keeps its records, and draft a classification for the human owner. They write nothing.

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
claude plugin marketplace add https://github.com/bjmcder/claude-governance.git#ledger-324
```

The repository's files take about 20 MB, most of them review records that a project does not need. For a marketplace added from a git URL, `--sparse` checks out only the two directories the plugin uses; for a local path it has no effect:

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
PYTHONPATH="<installPath>" python3 -B -P -m govharness show "<installPath>/governance" GOV.38
```

It prints GOV.38, the provision on the harness itself. `-P` keeps the working directory, which is your project, off Python's module search path, so that a file or directory of the project named like a module of the standard library, such as `json/`, is never run in its place. Every form on this page that sets `PYTHONPATH` uses it.

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
claude plugin marketplace add REPO#ledger-324 --scope project
claude plugin install governance@governance-harness --scope project
```

or write the settings directly:

```json
{
  "extraKnownMarketplaces": {
    "governance-harness": {
      "source": {
        "source": "git",
        "url": "https://github.com/bjmcder/claude-governance.git",
        "ref": "ledger-324",
        "sparsePaths": [".claude-plugin", "harness"]
      }
    }
  },
  "enabledPlugins": {
    "governance@governance-harness": true
  }
}
```

For a repository on GitHub, the source is `{"source": "github", "repo": "<owner>/<name>", "ref": "ledger-324"}`. Commit the file.

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
              "url": "https://github.com/bjmcder/claude-governance.git",
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

`git rev-parse 'ledger-324^{commit}'` in a clone prints the commit hash of a tag; without `^{commit}`, it prints the hash of the tag object instead. With this source, each member runs `claude plugin install governance@governance-pinned --scope project` once, since Claude Code does not fetch a plugin with an external source from project settings alone.

### Verify, update, and remove

`claude plugin list` shows the plugin with scope `project`. To move the project to another revision, change `ref` or `sha` and commit; Claude Code fetches the marketplace again when its source in settings changes. A member who wants the plugin off for themselves alone runs `claude plugin disable governance@governance-harness --scope local`. To remove it for everyone, delete the two entries from `.claude/settings.json` and commit, or run `claude plugin uninstall governance@governance-harness --scope project`, which removes it from the shared file.

## 3. The harness alone

The harness is a Python package, `govharness`, with a console script of the same name. It works with any agent that runs shell commands, and for a person at a terminal.

```bash
git clone REPO governance-harness
git -C governance-harness checkout ledger-324
pipx install ./governance-harness/harness
export GOVHARNESS_ROOT="$PWD/governance-harness/harness/governance"
```

The argument of `pipx install` is the path of the directory that holds `pyproject.toml`; a bare name, such as `pipx install harness`, asks the Python Package Index instead. In place of `pipx`, a virtual environment works too:

```bash
python3 -m venv .venv
.venv/bin/pip install ./governance-harness/harness
```

Both installs build the package with `setuptools` 68 or later, which `pip` and `pipx` download from the Python Package Index. Without network access, run the harness without installing it, in the `PYTHONPATH` form below. Where `setuptools` is already installed in the virtual environment, `--no-build-isolation` builds with that copy and reaches no index:

```bash
.venv/bin/pip install --no-build-isolation --no-index ./governance-harness/harness
```

To work on the harness code itself, an editable install from the root of the clone picks up each change without reinstalling: `pip install --no-deps -e harness`, inside a virtual environment.

`GOVHARNESS_ROOT` names the corpus that `show`, `find`, `context`, `pairs`, `onset`, and `verify` read when no corpus is named on the command line. Set it in your shell profile, or, for Claude Code, under `env` in a settings file:

```json
{"env": {"GOVHARNESS_ROOT": "/home/me/src/governance-harness/harness/governance"}}
```

Without installing anything, every command also runs from the clone, with no network access:

```bash
PYTHONPATH=governance-harness/harness python3 -B -P -m govharness show governance-harness/harness/governance GOV.38
```

### Verify

```bash
govharness show GOV.38
govharness verify
```

`show` prints GOV.38. `verify` runs every check of the corpus and passes, printing one warning, g.18, on three provisions of STND.DRAFT whose three modals the custodian reviewed. It writes nothing unless a cache of solver results is named, by `--cache DIR` or by `GOVHARNESS_CACHE`, which must be an absolute path outside the corpus; with a cache, later runs are about a second faster. [operating.md](operating.md#checking-the-corpus) says more about both commands. A subset of the tests runs in under twenty seconds from `governance-harness/harness`:

```bash
python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main tests.test_architecture tests.test_conventions
```

### Update and uninstall

The corpus is the clone's checked-out commit, so updating the governance is a checkout:

```bash
git -C governance-harness fetch --tags
git -C governance-harness checkout <new tag>
pipx install --force ./governance-harness/harness
```

The last command matters only when the harness code changed. To uninstall, run `pipx uninstall govharness`, unset `GOVHARNESS_ROOT`, and delete the clone.

## 4. A vendored copy

A project that works offline, or that wants the governance revision in its own history, keeps a copy of this repository inside its own.

As a git submodule, from the repository's URL:

```bash
git submodule add https://github.com/bjmcder/claude-governance.git vendor/governance-harness
git -C vendor/governance-harness checkout ledger-324
git add .gitmodules vendor/governance-harness
git commit -m "Vendor the governance at ledger-324"
```

In place of `ledger-324`, the `checkout` takes a full commit hash. Git refuses a submodule from a path on your machine by default, because a repository could otherwise use one to copy local files into a clone. For a clone that you trust, allow it for the one command:

```bash
git -c protocol.file.allow=always submodule add /path/to/governance-harness vendor/governance-harness
```

As a subtree, which copies the files into the project's history:

```bash
git subtree add --prefix vendor/governance-harness REPO ledger-324 --squash
```

`git subtree` takes a ref of the remote, so give it a tag or branch. It refuses an abbreviated commit hash, and a full one works only where the server allows fetching by hash.

For an air-gapped machine, make a bundle on a connected one and carry it across:

```bash
git clone --mirror REPO governance-harness.git
git -C governance-harness.git bundle create ../governance-harness.bundle --all
```

On the air-gapped machine, `git clone governance-harness.bundle vendor/governance-harness` makes the copy.

The vendored copy is used through the harness without installing it, which needs no network access:

```bash
PYTHONPATH=vendor/governance-harness/harness python3 -B -P -m govharness show vendor/governance-harness/harness/governance GOV.38
```

With `GOVHARNESS_ROOT` set to the absolute path of `vendor/governance-harness/harness/governance`, the corpus argument can be left out. To install the package instead, use `--no-build-isolation` with a locally installed `setuptools`, as in [option 3](#3-the-harness-alone). With Claude Code, the plugin loads from the copy without network access, either for one session:

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
PYTHONPATH=vendor/governance-harness/harness python3 -B -P -m govharness verify vendor/governance-harness/harness/governance
```

For a submodule, the first prints the vendored commit. For a subtree it prints the project's own commit; the message of the squash commit names the vendored one:

```bash
git log -1 --grep='git-subtree-dir: vendor/governance-harness' --format=%B | grep git-subtree-split
```

The `verify` command passes with the g.18 warning. To update a submodule, fetch and check out another tag inside it and commit the change; for a subtree, run `git subtree pull --prefix vendor/governance-harness REPO <new tag> --squash`. To remove a submodule, run `git rm vendor/governance-harness` and commit; for a subtree, delete the directory and commit.

## 5. No software

The corpus is plain Markdown and needs no program to read. A copy of this repository, or of its `rendered/` directory alone, is enough:

- [`rendered/`](../rendered/README.md) holds a reading copy of every document, named by identifier, and a table of contents, `README.md`. Start with `LVL0.md`.
- [`harness/governance/README.md`](../harness/governance/README.md) maps each identifier to its file: `GOV.38` is `harness/governance/GOV/38.md`.
- [`harness/README.md`](../harness/README.md#reading-and-applying-the-corpus-without-software), in its section on reading and applying the corpus without software, gives each check by hand with `sha256sum`, `sed`, and `gpg`.

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

A project constitution (STND.PROJ) starts as a copy of the template directory `harness/governance/_PROJECT/NAME/`, taken from the revision the project pins. NAME is the project's mnemonic, which its human owner registers in the project's ledger (STND.IDENT.23). The copy lives in the project's repository, and its Records section names where the other records go. `show`, `find`, and the other query commands read the corpus only, never a project's constitution or ledger; `ledger check` and `ledger append` read and append to a project's ledger, as [adoption.md](adoption.md#adopting), step 4, shows. [adoption.md](adoption.md) covers when a project needs a constitution and how the class is recorded.

## Pointing other agents at the governance

Claude Code reads a project's `CLAUDE.md`, and reads `AGENTS.md` when no `CLAUDE.md` exists; a `CLAUDE.md` can include `AGENTS.md` with the line `@AGENTS.md`. Many other coding agents read `AGENTS.md`. A few lines there tell any agent where the governance is:

```markdown
## Governance

This project follows the governance corpus in vendor/governance-harness/harness/governance,
at the commit of that submodule. Its records are in records/ and its working notes in notes/.
The agent instructions are the provisions of STND.INSTR; rendered/STND.INSTR.md in that
repository is a reading copy. From the top of this project, without installing anything,
`PYTHONPATH=vendor/governance-harness/harness python3 -B -P -m govharness show vendor/governance-harness/harness/governance ID`
prints a provision; with `find` or `context` in place of `show`, and words in place of
`ID`, the same command lists or prints the provisions on a topic. Where the harness is installed and
GOVHARNESS_ROOT names that corpus, `govharness show ID`, `govharness find WORDS`, and
`govharness context WORDS --in-force` do the same.
```

Adjust the path to the option the project uses. For a project on the plugin alone, name the plugin instead of a path.

The file directs the project's agents only once the human owner adopts it, by a ledger transaction that names its path and its content (STND.INSTR.11); [adoption.md](adoption.md#adopting), step 5, describes the adoption.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `No module named govharness` | `PYTHONPATH` must name the `harness` directory, the one that contains `govharness/`, not the corpus. With `-P`, the working directory does not count, even inside `harness/` |
| A syntax error on start | Python is older than 3.11; `python3 --version` shows which |
| `error: argument root: ... no such directory`, exit status 2 | The corpus path on the command line is wrong |
| `no corpus root: give ROOT, set GOVHARNESS_ROOT, or run where ./governance exists`, exit status 2 | No corpus is named, `GOVHARNESS_ROOT` is unset, and the working directory has no `governance/` |
| `GOVHARNESS_ROOT=...: no such directory`, exit status 2 | `GOVHARNESS_ROOT` names a directory that does not exist |
| `find` prints "no item holds a word of", exit status 1 | No item uses those words; the corpus's own terms match best, such as "remote write" rather than "push" |
| The `/governance:` skills do not appear | Open the Errors tab of `/plugin`, then run `/reload-plugins`. A project-scope plugin loads only after the workspace trust dialog is accepted |
| "enabled in project settings but isn't installed here" | Run `claude plugin install governance@governance-harness --scope project` once |
| An update changes nothing | Run `claude plugin marketplace update governance-harness` first. With a `#ref` or `ref` pin, only commits on that ref arrive |
| `refused: GOVHARNESS_CACHE must be an absolute path` | Give the cache directory as an absolute path, or unset the variable to run without a cache |
| `refused: the solve cache ... lies inside the corpus` | Name a cache directory outside the corpus, or none |
