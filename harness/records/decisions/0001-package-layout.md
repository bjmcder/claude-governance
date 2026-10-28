# Decision 0001: layered package `govharness`

Status: accepted for unit 0001 (REPRO.7). Author: Claude, agent.

Since unit 0018 the package has no `govharness.hooks` and no `derive/environment/`; the rows below that name them are history.

## Context

Twenty-three flat scripts import one another freely. The corpus model sits in `govlib.py` and also in `logic_facts.py`. The drafting checks import a command-line script (`references.py`). `verify.py` and `check_logic.py` each report results in their own format. A mistaken tools path once let a rehearsal append to the live ledger. That error is recorded as ledger entries 30 and 31.

## Decision

The package has five layers. A module imports only from its own layer or from layers below it (DSGN.7). No import cycles are allowed.

| Layer | Package | Holds | Effects allowed |
| --- | --- | --- | --- |
| 0 | `govharness.core` | Entry model, front matter, identifier and path mapping, hashing, corpus loading and index, text and table reading, the result model | Reading corpus files, in `core/corpus.py` only |
| 1 | `govharness.ledger` | Transaction types, hash chain, signer register, signature checking | Ledger reads and appends in `ledger/chain.py`; gpg processes, the signer config, and the environment in `ledger/gpg.py` |
| 2 | `govharness.checks` | Check registry and one module or subpackage per family: structure, manifests, ledger, lineage (l), drafting (g), revisions and identifiers (v), logic (a to f) | None |
| 2 | `govharness.derive` | Generated artifacts: manifests, references tables, reading copies. Each function returns `{path: text}` and writes nothing. | None |
| 3 | `govharness.workflows` | Multi-step procedures: amendment primitives and rehearsal in an isolated copy | File writes under the root passed to them; the copy's temporary directory |
| 4 | `govharness.cli` | One `argparse` entry point with a subcommand for each command; `python -m govharness` | Printing, exit codes, writing what `derive` returns |

## Rules

- **Check registry (DSGN.11).** Each check is a `Check` value with the fields `key`, `family`, `title`, `enforces`, and `run`. Each family module exports a tuple named `CHECKS`. The registry lists the family modules explicitly, with no discovery (SIMPL.6). Adding a family means adding one module and one line in the registry. Check keys never change, because `checked_by` fields cite them.
- **Explicit roots (DSGN.14).** Every function takes the corpus root, or the loaded corpus, as a parameter. No module holds a path to a particular corpus. The default signer config path, `/etc/governance/signer.json`, is a named constant that a parameter can override.
- **One result model.** `core/report.py` holds `CheckResult` and `Report`. The structural checks of `verify` report through it. Rendering keeps the current output byte for byte (unit 0001, criterion 4).
- **Tests** live in `tests/` and mirror the package. Mutation tests are evidence of detection against a known injected defect. Comparisons with earlier output are labeled regression guards (VV.7).
- **Retired from the active package (SIMPL.8):** `import_lvl0.py`, `scaffold.py`, and `scaffold_spec.json`. Their one-time work is done. They stay in `archive/tools-flat/`.

## Alternatives weighed

| Alternative | Reason rejected |
| --- | --- |
| Keep flat scripts and fix the imports | Leaves no stated structure for a mechanical check to enforce (DSGN.3, DSGN.7). |
| Plugin discovery by entry points or a scan | Hidden behavior (SIMPL.6); one consumer, the registry list, is enough. |
| A third-party CLI or packaging framework | Adds a dependency with no present need (SIMPL.4). |

## Adjustments made while implementing unit 0001

Each rule below refines the decision where implementing it showed the text to be incomplete. None loosens a layer rule. `tests/test_architecture.py` enforces the rules as refined.

| Rule as first written | Refinement | Reason |
| --- | --- | --- |
| `ledger/gpg.py` runs `gpg` processes, reads the signer config and the environment | It also writes the digest and the signature into its own throwaway keyring directory | `gpg --verify` reads both from files; the directory is created and removed inside one call |
| Reading corpus files in `core/corpus.py` only | `core/corpus.py` takes a snapshot of every file under a root (`read_tree`), so checks and derivations compute on data. The ledger file is read in `ledger/chain.py`, and the CLI reads the files named on its command line (a key file) | The checks of `verify` and the manifests need the whole tree; one read keeps them pure (DSGN.16). The ledger and the key file are not corpus files |
| Effects listed per layer | Withdrawn by review 0001: the built-in solver raised the interpreter's recursion limit in `checks/logic/satlib.py` | DPLL recursed once per case split. Review 0001 made the search iterative, so no module changes the interpreter state, and the architecture test allows that effect nowhere |
| One module or subpackage per family | A family may span modules, and the registry lists modules, not families: `structure` is `checks/structure.py` (ids, mnemonics, references) and `checks/fields.py` (templates, status); `logic` is `checks/logic/authority.py`, `language.py`, and `proofs.py` | The registry order is the report order, and both `verify` and `check` print in the order they always have: the proofs (f) come after the revision checks (v) |
| `Check` fields `key`, `family`, `title`, `enforces`, `run` | `run` takes the run's `CheckContext` and returns a `Verdict`, or `None` when the check does not apply (g.0, the f claims). A title may hold placeholders, filled from the verdict (a.1, b.1, f.2, f.4, f.8). `enforces` names provisions or, for g and v, the standard, whose provisions' `checked_by` fields carry the finer mapping that g.23 and v.7 check | Some titles name what the corpus holds, and some checks report only when the corpus gives them material; the mapping of g and v checks to provisions already lives in the corpus |
| Shared work | `CheckContext.shared` computes a value that several checks use (the facts, the drafting findings, the clause set) once per run | The flat code computed each once; computing it per check would change nothing but the time |
| `tests/` mirrors the package | `tests/equivalence/run_equivalence.py` is the regression guard of unit 0001 criterion 4; `tests/gpgkeys.py` makes throwaway keyrings whose agent socket paths fit in 107 bytes | Signature tests need a key in a short directory, wherever the temporary directory is |

## Adjustments made by review 0001

| Rule as refined above | Adjustment | Reason |
| --- | --- | --- |
| Checks and derivations compute on the snapshot; `checks/` performs no effect | The ledger check takes the pins, the scopes, and the signer register from the snapshot (`core.corpus.scope_hash`, `has_directory`), not from the disk. Loading a root for `verify` moved from `checks/verification.py` to `workflows/verification.py`, which also reads the signer configuration; `checks/verification.verify_snapshot` runs on data, and a context with no signer configuration has no anchor. `ledger.signatures.check_signatures` takes the configuration as a required parameter. The ledger check still verifies signatures, and so runs `gpg`, through `ledger/gpg.py`; it is the one check that does | The checks layer read files and the owner's configuration through calls into `core.corpus` and `ledger.gpg`, which the architecture test, scanning each module's own source, did not see |
| `tests/test_architecture.py` enforces the effects column | The test resolves import aliases, refuses relative imports, adds the effects random, network, and execute (allowed only to `workflows/rehearse.py`, which runs the amendment script), and follows calls by name into the package: a module's effects include those of the package functions it calls, and a call into `ledger/gpg.py` counts as `gpg` or `config`. Calls through values, such as a check's `run`, are not followed | The direct scan could be passed by `import os as o`, by a relative import, or by calling an effectful function of another module |

## Adjustment made by unit 0003

| Rule as refined above | Adjustment | Reason |
| --- | --- | --- |
| Five layers, `core` to `cli` | `govharness.hooks` holds programs that the environment runs, such as `hooks/guard.py`; they are at layer 4, import nothing from the package, and may read their input, the environment, and their policy file and print their answer. The CLI reads the guard's source to install it and never imports it | A hook is installed outside the work, where the package is not; `tests/test_architecture.py` asserts that a hook stands alone |

## Adjustment made by unit 0008

| Rule as refined above | Adjustment | Reason |
| --- | --- | --- |
| Only the CLI reads the clock | `govharness.hooks` may read the clock too: the guard compares the expiry of each authorization in its policy with the time of the call. The derivation still takes the time from the CLI as a parameter | An expiry checked only when the configuration is derived would let an authorization outlast its duration until the owner derives again (STND.HARN.29) |

## Adjustment made by unit 0011

| Rule as refined above | Adjustment | Reason |
| --- | --- | --- |
| Files are read in `core/corpus.py`, `ledger/chain.py`, `ledger/gpg.py`, and the CLI; the environment is read in `ledger/gpg.py` and the hooks | `workflows/solve_store.py` also reads and writes the solve cache, a directory outside the corpus; reads the source of `checks/logic/satlib.py` and `checks/logic/solvecache.py` to version its entries; and reads the variables `GOVHARNESS_CACHE_DIR`, `GOVHARNESS_NO_CACHE`, and `XDG_CACHE_HOME`. It encapsulates the cache as `ledger/gpg.py` encapsulates gpg: a call into it from another module counts as the effect `cache`, which the workflows, the CLI, and `__main__` may perform | Every amendment transaction verifies, and most of its time went to solves whose clause sets had not changed; the store is the one module that touches the cache's files and settings |
| `checks` reads and writes no file | Unchanged: the checks never call the store. `checks/logic/proofs.planned_keys` names the keys of a run's solves before the run; the workflow loads those entries into `CheckContext.solve_cache` as data; the proofs reuse an entry only after `checks/logic/solvecache` checks it against the clause set; and the workflow saves the entries the run computed (`workflows/verification.run_logic`) | A store injected into the context would let the checks perform file effects through a value, which the architecture test does not follow (the limit review 0001 named); loading by planned keys keeps the checks on data |

## Adjustment made by unit 0022

| Rule as refined above | Adjustment | Reason |
| --- | --- | --- |
| The environment is read in `ledger/gpg.py` and `workflows/solve_store.py` | `cli/arguments.py` also reads `GOVHARNESS_ROOT`, the default corpus root of the read-only commands and of `verify`; the other CLI modules take the root through its `default_root`, so the environment effect reaches the CLI only by that call. `workflows/solve_store.py` now reads `GOVHARNESS_CACHE` alone: the cache is opt-in, and no module reads `XDG_CACHE_HOME` or the home directory | An installed `govharness` is typed without a root (review HR-5 of 2026-10-28), and a read-only command writes nothing by default (HR-4). `tests/test_architecture.py` lists `cli/arguments.py` for the environment effect and admits it to the CLI transitively |
| Dead code | `checks/verification.verify_snapshot`, `core/corpus.is_directory`, `core/corpus.has_directory`, and `core/text.sentences_of`, named in the adjustment of review 0001 above, are deleted; the ledger check reaches the snapshot through `has_scope_path` | Each was defined, never called, and never tested (HR-13) |
