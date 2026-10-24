# Unit 0001: restructure the harness code as a layered package

Definition of done and acceptance criteria, committed before the first attempt (STND.DFLT.7, VV.3). The record of the unit (STND.DFLT.8) is appended below them when the unit closes.

## Purpose

The harness code is software that implements governance and is governed as software (GOV.38). This unit restructures the flat `tools/` scripts into one layered package, `govharness`, without changing what any check reports.

## Definition of done

1. `governance/` is byte-identical to the baseline commit.
2. The package follows `records/decisions/0001-package-layout.md`. A test asserts that no module imports from a higher layer.
3. Only the modules that the decision record names perform input or output, start processes, or read the environment (DSGN.16). A test asserts this.
4. The old and the new code give byte-identical results on the same inputs. This covers `verify` stdout and exit code; `check --out-dir` files and exit code; `manifests --check`; and `references --check`. The inputs are the live corpus and one damaged copy for each family: structure, manifests, ledger chain, signature, lineage, drafting, revision, identifier, and logic. The unit record lists each command and the SHA-256 of each output (VV.1, SIMPL.7).
5. Every test of the three existing suites is ported and passes. Each test states the behavior it fixes and its reference. A test that compares only with earlier output is labeled a regression guard (VV.7).
6. Every function and class has type annotations and a NumPy-style docstring. `ruff check --select E,F,W,I,UP --line-length 79` reports nothing.
7. `tools/` holds only thin entry points for the commands that current documents name: `verify.py`, `check_logic.py`, `references.py`, `ledger.py`, and `signatures.py`. Each delegates to the package, and each is to be removed once those documents cite the package's commands (DSGN.6).
8. The pre-package code is kept unchanged under `archive/tools-flat/` as the reference for criterion 4 (SIMPL.8).
9. `README.md` states the layout, every command, and how a reader with no software applies the corpus (INTPR.12). `records/dependencies.md` lists each dependency with its reason (REPRO.9).
10. Every change is a commit whose message identifies an agent author (REPRO.5). A behavior-preserving restructure and a change of behavior are never in the same commit.

## Out of scope

The environment derivation, the agent brief, and every amendment to `governance/` are out of scope. They belong to later units and to the STND.HARN draft.


## Record

Appended when the unit closed (STND.DFLT.8). Author: Claude, agent (REPRO.5).

### Plan

1. Keep the flat tools unchanged under `archive/tools-flat/` as the reference (criterion 8).
2. Build the package of decision 0001 beside the flat tools, with the structural checks of `verify` as registered checks reporting through `core/report.py`, the corpus model in one place (`core/corpus.py`), and the drafting checks split by concern.
3. Write the equivalence harness, a regression guard, and compare old and new on the live corpus and one damaged copy per family until every output is identical (criterion 4).
4. Port the three mutation suites, and add tests of the layers, the effects, the registry, and the conventions (criteria 2, 3, 5, 6).
5. Reduce `tools/` to shims; update `README.md` and `records/dependencies.md` (criteria 7, 9).
6. Audit each criterion and commit this record (criterion 10).

### What was done

| Commit | Content | Kind |
| --- | --- | --- |
| `16c1048` | The 24 flat files copied byte for byte to `archive/tools-flat/` | Restructure |
| `0eb774f` | Package `govharness` (core, ledger, checks, derive, workflows, cli), `tests/` with the ported suites, the architecture test, and the equivalence harness; decision 0001 refined in its new section "Adjustments made while implementing unit 0001" | Restructure |
| `98577e2` | `tools/` reduced to the five shims; `README.md` and `records/dependencies.md` updated | Restructure |
| this commit | The conventions test and this record | Restructure |

Duplication removed: the corpus model (`govlib.Entry`, `govlib.load_corpus`, and `logic_facts.Corpus`) is one `core/corpus.py`; table reading (in `drafting_tables`, used by five modules) is `core/tables.py`; the drafting checks no longer import the references command-line module, because the References derivation is `derive/references.py` and the check g.25 compares with it; the chain link test of `verify` is `ledger/transactions.link_problems`; the manifest builder serves both the check and the command (`derive/manifests.py`). `drafting_checks.py` (1131 lines) became `checks/drafting/` with `tables`, `context`, `modals`, `expressions`, `citations`, `roles`, `style`, and `family`. Code with no consumer in the active package was left in the archive only: `govlib.id_to_path`, `govlib.dump_entry`, `Corpus.part_of`, `logic_checks.TIER_NAMES`, the unused fields `facts` and `standard` of the drafting context, and the always-empty second value returned by `check_signatures`.

### Audit of the criteria

1. **`governance/` is byte-identical to the baseline commit.** `git diff --stat 99d9a78 -- governance` prints nothing at each commit of the unit. Met.
2. **The package follows decision 0001; a test asserts that no module imports from a higher layer.** `tests/test_architecture.py`: `test_every_module_has_a_layer`, `test_no_import_from_a_higher_layer`, `test_no_import_cycle`, with `test_cycle_detection_finds_a_cycle` as evidence that the search can fail. Where implementing the decision refined it, the decision record says how and why. Met.
3. **Only the modules the decision names perform input or output, start processes, or read the environment.** `test_effects_are_confined` scans every module with `ast` for reads, writes, processes, the environment, temporary directories, copies, printing, the clock, and the interpreter state, against the places the refined decision allows; `test_effect_scan_finds_effects` is the evidence that the scan sees each kind. `checks/` and `derive/` read and write nothing. Met.
4. **Old and new give byte-identical results.** Regression guard `tests/equivalence/run_equivalence.py`, run as `TMPDIR=<scratch> python3 -B tests/equivalence/run_equivalence.py --work <scratch>/eq-u1`: 135 outputs compared, 0 differ. Inputs: the live corpus and ten damaged copies (structure: an `id` that differs from its path and a directory `Bad1`; manifests: a stale row in `STND/DRAFT/MANIFEST.csv`; ledger chain: entry 5 altered and entry 7 relinked; signature: a garbled signature on entry 12 with the chain recomputed, and a register founded by an owner key followed by an entry an intruder key signs; lineage: STND.DRAFT.19 marked waivable; drafting: an excluded expression in STND.DRAFT.2 and a References row dropped from STND.CLASS; revision: LVL0 at 1.0.9; identifier: a narrowed grade scale and a malformed `refers_to`; logic: VV ranked twice and a GUARD provision that MAY be waived). Each damaged copy fails the checks of its family under both codes. Commands, with `ROOT` the copy and old and new run on the same path:

   | Command (new) | Flat tool (old) |
   | --- | --- |
   | `python3 -B -m govharness verify ROOT` | `python3 -B archive/tools-flat/verify.py ROOT` |
   | `python3 -B -m govharness verify --no-z3 ROOT` (live, logic) | `python3 -B archive/tools-flat/verify.py ROOT --no-z3` |
   | `python3 -B -m govharness check ROOT --out-dir OUT/new [--no-z3]` | `python3 -B archive/tools-flat/check_logic.py ROOT --out-dir OUT/old [--no-z3]` |
   | `python3 -B -m govharness manifests ROOT --check` | `python3 -B archive/tools-flat/build_manifests.py ROOT --check` |
   | `python3 -B -m govharness references ROOT --check` | `python3 -B archive/tools-flat/references.py ROOT --check` |

   The SHA-256 of each output follows (the exit code is shown as the value itself). The signature-forged input is built with fresh keys on each run, so its digests change from run to run while old and new still agree; every other digest is reproducible. Met.

   | Input | Command | Output | SHA-256 | Identical |
   | --- | --- | --- | --- | --- |
   | live | `verify` | stdout | 6b8f7ae3c7863c62d7614684cdc4d72e5f20dbccb80b88590a7c77dc743807ad | yes |
   | live | `verify` | exit | 0 | yes |
   | live | `verify --no-z3` | stdout | 6b8f7ae3c7863c62d7614684cdc4d72e5f20dbccb80b88590a7c77dc743807ad | yes |
   | live | `verify --no-z3` | exit | 0 | yes |
   | live | `check --out-dir` | stdout | 093410888bb88363ec979b119fd78f81366d1ab6089034a7924cc563277aa4ef | yes |
   | live | `check --out-dir` | exit | 0 | yes |
   | live | `check --out-dir` | logic_report.md | 99213782ad6cfaa93fe54067f0792399e31732a5717128c1b1c2437973a73268 | yes |
   | live | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | live | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | live | `check --out-dir --no-z3` | stdout | ab7848890634f04ec714cecaa62174b4f6f53bc6e2a51ee3e3dbc5289978ae42 | yes |
   | live | `check --out-dir --no-z3` | exit | 0 | yes |
   | live | `check --out-dir --no-z3` | logic_report.md | 93ef3b797ccfe3289acf7292fb9734f4c4429e70184754d4be5636065f48f8ca | yes |
   | live | `check --out-dir --no-z3` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | live | `check --out-dir --no-z3` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | live | `manifests --check` | stdout | 5c5d4ba67c85f116968032f839fb54bf6757518acd08c481b2f1c95c755decb8 | yes |
   | live | `manifests --check` | exit | 0 | yes |
   | live | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | live | `references --check` | exit | 0 | yes |
   | structure | `verify` | stdout | 7736679901256e47ad228a904df73b953cb3bd1c3ae503c55b40df19489c6684 | yes |
   | structure | `verify` | exit | 1 | yes |
   | structure | `check --out-dir` | stdout | 13f84d2b40d6e01dde0432bb6898b1b09346378b6b130b99b60aad6a0c142f23 | yes |
   | structure | `check --out-dir` | exit | 1 | yes |
   | structure | `check --out-dir` | logic_report.md | a4f65cb03097789ffba05cf038bc1175b2e2cbcdd796af175a5a20e1a2c21d9b | yes |
   | structure | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | structure | `check --out-dir` | drafting_punch_list.md | c51bccc8ef76c1dd912b8c80afd1eaac7848a4eed475dc0eca6c533a81d50dbe | yes |
   | structure | `manifests --check` | stdout | 7840b9396192a08e8c0dceac339c7939758fd7fc31ea07d1f15a1289bb0d0b79 | yes |
   | structure | `manifests --check` | exit | 1 | yes |
   | structure | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | structure | `references --check` | exit | 0 | yes |
   | manifests | `verify` | stdout | 05823e4ff76436dd91e14c0a3211bdb69fc01fd8da660802c8e02c9da2626fac | yes |
   | manifests | `verify` | exit | 1 | yes |
   | manifests | `check --out-dir` | stdout | 093410888bb88363ec979b119fd78f81366d1ab6089034a7924cc563277aa4ef | yes |
   | manifests | `check --out-dir` | exit | 0 | yes |
   | manifests | `check --out-dir` | logic_report.md | 8797e6d1e6aa5970ce7b8807a6b4d234d2b3eefc55e7957f28e8a61ca2d7368c | yes |
   | manifests | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | manifests | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | manifests | `manifests --check` | stdout | c76d3c41f12e6c494189152ab44676bda24dce20ac87c1126d255e32e0032886 | yes |
   | manifests | `manifests --check` | exit | 1 | yes |
   | manifests | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | manifests | `references --check` | exit | 0 | yes |
   | ledger-chain | `verify` | stdout | 1d5052e2d926e2ac3e892c0d79cf9accc85378421d6077b37fe24d1a434c6947 | yes |
   | ledger-chain | `verify` | exit | 1 | yes |
   | ledger-chain | `check --out-dir` | stdout | 093410888bb88363ec979b119fd78f81366d1ab6089034a7924cc563277aa4ef | yes |
   | ledger-chain | `check --out-dir` | exit | 0 | yes |
   | ledger-chain | `check --out-dir` | logic_report.md | b8cc3a3951d8417a380c2711144f68a38a6af095216d71dc46a7a293592c3ea4 | yes |
   | ledger-chain | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | ledger-chain | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | ledger-chain | `manifests --check` | stdout | 5c5d4ba67c85f116968032f839fb54bf6757518acd08c481b2f1c95c755decb8 | yes |
   | ledger-chain | `manifests --check` | exit | 0 | yes |
   | ledger-chain | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | ledger-chain | `references --check` | exit | 0 | yes |
   | signature-unregistered | `verify` | stdout | 3d7891d8f25a0fa5e2486b641674431cbfee3ed12135dbc541870912bbaedd28 | yes |
   | signature-unregistered | `verify` | exit | 1 | yes |
   | signature-unregistered | `check --out-dir` | stdout | 093410888bb88363ec979b119fd78f81366d1ab6089034a7924cc563277aa4ef | yes |
   | signature-unregistered | `check --out-dir` | exit | 0 | yes |
   | signature-unregistered | `check --out-dir` | logic_report.md | 24128c8901369a4872f743a2df0c7e1987bebbc0865f36f7f1d2c39794116fcc | yes |
   | signature-unregistered | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | signature-unregistered | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | signature-unregistered | `manifests --check` | stdout | 5c5d4ba67c85f116968032f839fb54bf6757518acd08c481b2f1c95c755decb8 | yes |
   | signature-unregistered | `manifests --check` | exit | 0 | yes |
   | signature-unregistered | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | signature-unregistered | `references --check` | exit | 0 | yes |
   | signature-forged | `verify` | stdout | c191c93924b21e3d91609e375dff3641a0f7d386b52b89ad23c5e5c84f03e508 | yes |
   | signature-forged | `verify` | exit | 1 | yes |
   | signature-forged | `check --out-dir` | stdout | 093410888bb88363ec979b119fd78f81366d1ab6089034a7924cc563277aa4ef | yes |
   | signature-forged | `check --out-dir` | exit | 0 | yes |
   | signature-forged | `check --out-dir` | logic_report.md | d1814397041e675d1f8810f352174425ce5a98ebcbf66548b01bcc34f8fd1e12 | yes |
   | signature-forged | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | signature-forged | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | signature-forged | `manifests --check` | stdout | 5c5d4ba67c85f116968032f839fb54bf6757518acd08c481b2f1c95c755decb8 | yes |
   | signature-forged | `manifests --check` | exit | 0 | yes |
   | signature-forged | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | signature-forged | `references --check` | exit | 0 | yes |
   | lineage | `verify` | stdout | 477c5d05650a32d15262e798b1b6efdfb182e5f6800cc19e7615144fc0e59d6c | yes |
   | lineage | `verify` | exit | 1 | yes |
   | lineage | `check --out-dir` | stdout | 5726fa7e599600b39f151e2d97849f246bae62058294110534c3f0725a3bbe1c | yes |
   | lineage | `check --out-dir` | exit | 1 | yes |
   | lineage | `check --out-dir` | logic_report.md | d4bbb1897f0a4122ecf1bc4cdf856e9842a8c3fb125bd553aac398669a562a96 | yes |
   | lineage | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | lineage | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | lineage | `manifests --check` | stdout | bd753d8b2bda35fe3d11c46679af7390ef337ab302166a96c06093b752828cd5 | yes |
   | lineage | `manifests --check` | exit | 1 | yes |
   | lineage | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | lineage | `references --check` | exit | 0 | yes |
   | drafting | `verify` | stdout | 6202efc3dd509baec00b57d945d50c8536042da6ea19a6b6bba8a366202b565a | yes |
   | drafting | `verify` | exit | 1 | yes |
   | drafting | `check --out-dir` | stdout | 4fc2777a4716bc12815ecd590dde32c89c932ef0a3662e7f4141d6690cc747f5 | yes |
   | drafting | `check --out-dir` | exit | 1 | yes |
   | drafting | `check --out-dir` | logic_report.md | dc6f55f3b533ca04b43fa28b11e3642c78d78797d66584bf35943e32b970aa60 | yes |
   | drafting | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | drafting | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | drafting | `manifests --check` | stdout | c744e96fb003f09fb534bd467239b814d82f8faa397ac15a22955ec48951a0e6 | yes |
   | drafting | `manifests --check` | exit | 1 | yes |
   | drafting | `references --check` | stdout | f4a40b2613827e9ccc8695877a5ad801fdc94b09f9264df829c7bc1b7d06d77b | yes |
   | drafting | `references --check` | exit | 1 | yes |
   | revision | `verify` | stdout | 49d247e042c7fb26af88fef27380c87f9a670e25b8689e2c98ab88baa434229c | yes |
   | revision | `verify` | exit | 1 | yes |
   | revision | `check --out-dir` | stdout | 9a73210e1bc6db66dc0aa3b7c22ac853061070dfbec389b15c4aa57250b74253 | yes |
   | revision | `check --out-dir` | exit | 1 | yes |
   | revision | `check --out-dir` | logic_report.md | 72c4c182b418ba80d6999bef0505728e345368840f5c7bc968e7b82019843f78 | yes |
   | revision | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | revision | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | revision | `manifests --check` | stdout | e6f155d558b3759d80008a4af9ab5888c97280d5060145b1e45653ce56ddde67 | yes |
   | revision | `manifests --check` | exit | 1 | yes |
   | revision | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | revision | `references --check` | exit | 0 | yes |
   | identifier | `verify` | stdout | 703f3b100963a0e7e0ed25ff394b192fbaabca767c2da03e6b4e39c474585ad4 | yes |
   | identifier | `verify` | exit | 1 | yes |
   | identifier | `check --out-dir` | stdout | bd69866d2cd83b97a2803be6c9b65f75a21c9ba2249299cd7661effa481e0244 | yes |
   | identifier | `check --out-dir` | exit | 1 | yes |
   | identifier | `check --out-dir` | logic_report.md | d5c6be0ee7a2aabb9f6b60e23912510452497b95063cede7bab728b85fc39f8f | yes |
   | identifier | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | identifier | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | identifier | `manifests --check` | stdout | bbde0caa4a8fa8a9f063196478c29090a98980be6334bebf7a6f23eafea483a4 | yes |
   | identifier | `manifests --check` | exit | 1 | yes |
   | identifier | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | identifier | `references --check` | exit | 0 | yes |
   | logic | `verify` | stdout | 721e034600953a66e7f7c146b9a589b8e8ece316d2fffd5de1919b033aaebadf | yes |
   | logic | `verify` | exit | 1 | yes |
   | logic | `verify --no-z3` | stdout | 721e034600953a66e7f7c146b9a589b8e8ece316d2fffd5de1919b033aaebadf | yes |
   | logic | `verify --no-z3` | exit | 1 | yes |
   | logic | `check --out-dir` | stdout | e2af84d1901bb31f97d169fd82b89325a42fd2f87e4314ee26c4b5ca0149198a | yes |
   | logic | `check --out-dir` | exit | 1 | yes |
   | logic | `check --out-dir` | logic_report.md | 3c857f110df48d208196b83f020ac78a364c41f7b670be5dab375b34e24341cb | yes |
   | logic | `check --out-dir` | logic_facts.json | c734b369a5f2a2a76c7085bfff188c726c292c7a83706490f98b749eed93e148 | yes |
   | logic | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | logic | `check --out-dir --no-z3` | stdout | 4421a33e249be966b8f058ed8460ebbf8f5c99f298440738e1b2a6daf5e2c122 | yes |
   | logic | `check --out-dir --no-z3` | exit | 1 | yes |
   | logic | `check --out-dir --no-z3` | logic_report.md | cc2fb4a61bc51f10f06912eb768a4ccfb41dbccf52f3bfd033c194c44d0dbcfb | yes |
   | logic | `check --out-dir --no-z3` | logic_facts.json | c734b369a5f2a2a76c7085bfff188c726c292c7a83706490f98b749eed93e148 | yes |
   | logic | `check --out-dir --no-z3` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | logic | `manifests --check` | stdout | 183e19245240475fbcb229c48b4b27b5e58f858fa43edc310a6b2376a5621d66 | yes |
   | logic | `manifests --check` | exit | 1 | yes |
   | logic | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | logic | `references --check` | exit | 0 | yes |

5. **Every test of the three suites is ported and passes; each states its behavior and reference; comparisons with earlier output are regression guards.** The 15 test methods of `test_logic.py` (2), `test_drafting.py` (4), and `test_revisions.py` (9) are in `tests/checks/test_logic.py`, `tests/checks/test_drafting.py`, `tests/checks/test_revisions.py` (4), `tests/checks/test_structure.py` (2), `tests/checks/test_ledger.py` (1), and `tests/ledger/test_signatures.py` (2), with every mutation case (12, 41, and 42 cases, and 7 signature cases). Each docstring states the behavior and the reference, the injected defect; the equivalence harness is labeled a regression guard. `TMPDIR=<scratch> python3 -B -m unittest discover -s tests -t .`: 26 tests, OK, in 52 s. Met.
6. **Annotations and NumPy-style docstrings on every function and class; ruff reports nothing.** `tests/test_conventions.py` audits every definition in `govharness/`, `tests/`, and `tools/`; `ruff check --select E,F,W,I,UP --line-length 79 govharness tests tools` prints "All checks passed!". The archive is the unchanged reference and is not reformatted. Met.
7. **`tools/` holds only the five thin entry points.** `ls tools`: `check_logic.py ledger.py references.py signatures.py verify.py`; each puts the repository root on the path and calls `govharness.cli.main.main` with the subcommand and the old arguments, and its docstring says it goes once documents cite the package command (DSGN.6). Met.
8. **The pre-package code is kept unchanged under `archive/tools-flat/`.** `git diff 99d9a78:tools 16c1048:archive/tools-flat` is empty. Met.
9. **`README.md` states the layout, every command, and how a reader with no software applies the corpus; `records/dependencies.md` lists each dependency with its reason.** README sections: the layout tree, "Commands" (a table with one line per command), and "Reading and applying the corpus without software"; the Current state table and the findings log keep their content, with tool names updated. The dependency record names the revisions in use. Met.
10. **Every change is a commit with an agent author; no commit mixes a restructure with a change of behavior.** Author "Claude (agent)" with the session trailer on every commit; the four commits above restructure only. Met.

### Differences that criterion 4 does not cover

- A malformed invocation now gets the `argparse` usage message and exit code 2 from every command; the flat `verify.py` printed its docstring and exited 1. Valid invocations behave as before.

### Defects found in the flat code, kept as they were

Unit 0001 changes no behavior, so these are reported, not fixed:

1. Check b.2: the branch for a LVL0 provision without a `waivable` field tests `level != "LVL0"` inside a branch reached only at LVL0, so such a provision is never reported. The dead test is removed; the behavior is unchanged.
2. Check g.23 counts as known every key reported earlier in the same run, so its verdict depends on which families ran first: a drafting provision that cites a v or f key is reported as citing an unknown check.
3. `signatures.py check` (now `sign check`) ends in a traceback when the corpus has no signer register, instead of a message.
4. `verify` on a root that does not exist reports `entries: 0` and a few failures rather than an error.
5. The built-in solver raises the interpreter's recursion limit for the rest of the process (declared in the decision record).
6. `ledger.py` (now `ledger append`) appends without checking the existing chain; unit 0002 criterion 1 adds the check.
7. `README.md` said the drafting suite damages the corpus in 39 ways (it has 41 cases) and that there was no signature scheme; both corrected.
8. `governance/README.md` says the tools in `../tools/` regenerate manifests; manifests are now regenerated by `python -m govharness manifests`. The corpus is out of scope for this unit, so the sentence awaits an amendment.


### Correction, made at the close of unit 0002

The audit of criterion 4 above says that every digest but those of the signature-forged input is reproducible. That is wrong for `logic_report.md`: its header names the corpus path, which lies under the work directory of the run, so its digest changes with that directory. Old and new still agree in every run. The rerun at the close of unit 0002 (work directory `eq-u2`) reproduces every other digest of the table above.
