# Architecture

This page describes how the repository and the harness package are laid out, for someone who maintains either. The commands themselves are in [`harness/README.md`](../harness/README.md), and using them in a project is in [operating.md](operating.md).

## The repository

| Path | What it is |
| --- | --- |
| `harness/` | The Claude Code plugin and the harness: the corpus, the Python package, its tests, the plugin's skills, and the records of the code's development. A plugin installs only the files under this directory |
| `.claude-plugin/marketplace.json` | The marketplace that lists the plugin, with `harness/` as its source |
| `rendered/` | A reading copy of every document, named by identifier, written by `compose governance --all ../rendered` |
| `docs/` | Documentation for people |
| `for-agents/` | Material for agents working on this repository; not part of the plugin |
| `CLAUDE.md`, `AGENTS.md`, `CUSTODIAN.md` | Short pointers to `for-agents/`; `CUSTODIAN.md` keeps the path that earlier records cite |
| `review-records/` | The records of each round of review, and in `review-records/harness/` the reviews of later units of work on the harness |
| `research/` | Research notes that the Notes of the standards cite |
| `tools/` | The amendment scripts that produced the ledger entries (`tools/amendment-scripts/`), `tools/findings.py`, which lists the drafting findings of a corpus copy, and `tools/check_refs.py`, which prints the findings of check g.25 |
| `OPEN-ITEMS.md` | Work the custodian has directed, and items that ratified rounds left open |

## The harness directory

```text
harness/
├── README.md                 the harness reference: commands, checks, checks by hand, tests
├── pyproject.toml            installs the package and the console script govharness
├── .claude-plugin/plugin.json
│                             the plugin manifest
├── skills/                   the plugin's three skills, one directory each
├── governance/               the corpus (see governance/README.md)
│   ├── MANIFEST.csv          root manifest (lists top-level mnemonics)
│   ├── ledger.jsonl          append-only, hash-chained transactions
│   ├── LVL0/  PRIN/  PRIME/  GUARD/  VV/  REPRO/  INTPR/
│   ├── DSGN/  SIMPL/  RSRC/  QA/  GOV/  LEX/                      LVL0
│   ├── AGENT/  NUMER/  MEAS/  CPS/  ML/
│   ├── HW/{CPU,GPU,QPU,EMBED,FPGA,ASIC}/  HDES/{FPGA,ASIC}/       LVL1
│   ├── STND/{DRAFT,IDENT,CLASS,DFLT,INSTR,HARN,VVUQ,CODE,THRT,
│   │        KNOW,DEPS,PROJ,WPROC,CREW,DOCS,CXX,PY,JL,ANNEX,MPI,
│   │        CONC,OMP,OFFLD,BUILD,WFLOW,STDC,RUST,FTN,SV,LEAN,
│   │        PERF,TEST}/                                        LVL2
│   ├── MNEM/                 the mnemonic register
│   ├── KNOW/  TAG/{FIELD,PROB,METH,HW,QTY,ACTV,COMP}/
│   └── _PROJECT/NAME/        LVL3 project template
├── rendered/                 reading copies of six standards, written by compose --write
├── govharness/               the package
├── tests/                    tests mirroring the package
└── records/                  units, reviews 0001 to 0009, decisions, and the
                              dependency record of the code; the findings log
                              of ledger entries 1 to 45
```

`show governance ID` prints the current text and revision of any document, and the ledger records each adoption and amendment, so neither is kept in a table here.

## The package

`govharness` is one package in five layers. A module imports only from its own layer or a lower one, and imports form no cycle. Effects are confined to a few modules:

| Effect | Where |
| --- | --- |
| Reading files | `core/corpus.py` (the corpus), `ledger/chain.py` (ledger files), `ledger/gpg.py` (the signer configuration), `workflows/solve_store.py` (the solve cache), and `cli/` (files named on the command line) |
| Writing files | `ledger/chain.py`, `ledger/gpg.py`, `workflows/`, and `cli/` |
| Running processes | `ledger/gpg.py` only |
| Reading the environment | `cli/arguments.py` (`GOVHARNESS_ROOT`), `workflows/solve_store.py` (`GOVHARNESS_CACHE`), and `ledger/gpg.py` |
| Running other code | `workflows/rehearse.py`, which runs the amendment script it is given |

No module opens a network connection or draws random numbers. `tests/test_architecture.py` holds the package to these rules by reading its source, and holds the modules of `checks/` to a list of the imports and names they may use.

```text
govharness/
├── __main__.py           python -m govharness <command>
├── core/                 layer 0
│   ├── entry.py          entry model, front matter, identifier ↔ path
│   ├── corpus.py         reads the corpus (the only module that does), index
│   ├── hashing.py        SHA-256 and the canonical JSON the ledger hashes
│   ├── locators.py       identifiers, section locators, resolution
│   ├── text.py           sentences, quoted mentions, identifiers in text
│   ├── tables.py         Markdown tables and sections by heading
│   └── report.py         CheckResult and Report, the result model
├── ledger/               layer 1
│   ├── transactions.py   transaction types, chain links, signature digest
│   ├── chain.py          reads and appends ledger files
│   ├── gpg.py            gpg processes and the signer configuration
│   ├── register.py       the signer register SIGNR and its text edits
│   └── signatures.py     verifies a ledger's signatures against SIGNR
├── checks/               layer 2; reads and writes no file
│   ├── base.py           Check, Verdict, CheckContext
│   ├── registry.py       the family lists and the runner
│   ├── verification.py   verify as data on a snapshot: structural, then
│   │                     logic checks
│   ├── structure.py      ids, mnemonics, references
│   ├── manifests.py      manifests are current
│   ├── ledger.py         chain, pins, signatures, unpinned files
│   ├── fields.py         template owner fields, entry status
│   ├── logic/            checks 0 and a to f: facts, tiers, wording,
│   │                     authority, language, proofs, satlib (DPLL, optional z3),
│   │                     solvecache (keys and checks of reused solves)
│   ├── lineage/          checks l.1 to l.5: derivation and family
│   ├── drafting/         checks g.0 to g.25: tables, context, modals,
│   │                     expressions, citations, roles, style, family
│   ├── revisions/        checks v.1 to v.11: classes, history, adopters,
│   │                     identifiers, family
│   └── combination.py    checks m.1 and m.2: profile combination
├── query/                layer 2, read-only: graph (citations, lineage),
│                         retrieval (show, find, context),
│                         combination (selectors, shared matters, pairs)
├── derive/               layer 2, returns {path: text}, writes nothing
│   ├── manifests.py      every MANIFEST.csv
│   ├── references.py     each document's References table
│   └── reading_copy.py   the reading copy of each divided standard, or of every document
├── workflows/            layer 3
│   ├── amend.py          amendment primitives: replace text, raise a
│   │                     revision, record a transaction and verify
│   ├── rehearse.py       run an amendment script on a fresh copy
│   ├── verification.py   load a corpus root and verify it
│   ├── solve_store.py    the solve cache on disk, outside the corpus
│   └── signers.py        found the signer register, add, close, require
└── cli/                  layer 4: main.py (parser), reports.py (verify,
                          check), derived.py (manifests, references,
                          compose), query.py (show, find, context, pairs),
                          records.py (ledger append, sign, rehearse),
                          arguments.py
```

## Tests

`tests/` mirrors the package, one directory per layer, with `tests/test_architecture.py` and `tests/test_conventions.py` at the top. [`harness/README.md`](../harness/README.md#tests) gives the commands that run them.