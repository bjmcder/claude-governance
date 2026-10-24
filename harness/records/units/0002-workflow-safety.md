# Unit 0002: safe ledger workflows and generated reading copies

Definition of done, committed before the first attempt (STND.DFLT.7, VV.3). This unit starts after unit 0001 closes and changes behavior on purpose. Each change is its own commit.

## Definition of done

1. `ledger append` checks the existing chain before appending. It verifies sequence numbers, `prev` links, and entry hashes, and refuses to append to a broken chain. It writes one line, then flushes and syncs the file. A test damages a ledger copy and asserts the refusal.
2. `govharness.workflows.amend` provides amendment primitives:
   - replace an exact text that occurs once in a corpus file;
   - raise a revision and add a history row;
   - record a transaction, which rebuilds the manifests, appends the entry, and runs `verify`.

   Each primitive takes the corpus root as a parameter and holds no path of its own.
3. `govharness.workflows.rehearse` runs an amendment script against a fresh copy of the corpus in a new temporary directory and runs `verify` there. It reports the entries the script appended. It asserts that the ledger and every file of the source corpus are byte-identical before and after. A test runs a script that appends an entry, then asserts that the source is unchanged and that the copy gained the entry.
4. `govharness.derive.reading_copy` composes the reading copy of each divided standard from the corpus. The header names each revision and its ledger entry, taken from the ledger. `compose --write` writes the copies to `rendered/`, and `compose --check` reports each stale copy. The current reading copies move to `rendered/` and are regenerated.
5. The criteria of unit 0001 still hold. Criterion 4 of unit 0001 applies only to commands whose behavior this unit does not change.


## Record

Appended when the unit closed (STND.DFLT.8). Author: Claude, agent (REPRO.5).

### Plan

1. Check the chain in `ledger append` and sync the write (criterion 1).
2. Make `verify` callable as data, so that the workflows call it directly, without a subprocess (a restructure, committed apart).
3. Port the scratch helper `amend.py` to `workflows/amend.py` with the root, actor, and role as parameters (criterion 2).
4. Add `workflows/rehearse.py` and the command `rehearse` (criterion 3).
5. Move the reading copies to `rendered/` (a move, committed apart), port the scratch helper `compose.py` to `derive/reading_copy.py`, add `compose`, and regenerate the copies (criterion 4).
6. Rerun the tests, ruff, the architecture test, and the equivalence harness (criterion 5).

### What was done

| Commit | Content | Kind |
| --- | --- | --- |
| `7c39599` | `ledger append` checks sequence numbers, `prev` links, and entry hashes of the existing ledger (`ledger.transactions.chain_problems`), refuses a broken chain with exit 1 and a message, and writes one line, flushed and synced; `tests/ledger/test_chain.py` | Behavior change (criterion 1) |
| `124647c` | `checks/verification.py` (`verify_corpus`, `Verification`); `verify` renders it; `ledger.transactions.revision_named` | Restructure; `verify` output unchanged |
| `485b954` | `workflows/amend.py`: `replace_text`, `raise_revision`, `record_transaction` with a `Change` value; `tests/workflows/test_amend.py` | New feature (criterion 2) |
| `3446c01` | `workflows/rehearse.py` and `python -m govharness rehearse ROOT SCRIPT`; `tests/workflows/test_rehearse.py` | New feature (criterion 3) |
| `4ceed2e` | The five reading copies moved, unchanged, to `rendered/` | Move |
| `3804541` | `derive/reading_copy.py`, `python -m govharness compose ROOT (--check \| --write)`, the five copies regenerated; `tests/derive/test_reading_copy.py` | New feature and content change (criterion 4) |
| this commit | This record, and a correction appended to the record of unit 0001 | Record |

### Audit of the criteria

1. **`ledger append` checks the chain before appending and refuses a broken one; it writes one line, flushes, and syncs; a test damages a ledger copy and asserts the refusal.** `govharness/ledger/chain.py` (`append`: `chain_problems`, then `handle.flush()` and `os.fsync`). `tests/ledger/test_chain.py`: four injected breaks (an altered entry, a dropped entry, a false link, and a renumbered entry with its links rebuilt, which only the sequence check sees) each raise and leave the file byte-identical; the command exits 1 with "broken chain" and writes nothing; an intact copy gains exactly one chained line. Met.
2. **`govharness.workflows.amend` provides the three primitives, each taking the corpus root and holding no path.** `replace_text(root, rel, pairs)` refuses a text that does not occur exactly once and a path outside the root; `raise_revision(root, document, old, new, row)` refuses a stale revision and a document without a history; `record_transaction(root, change)` rebuilds the manifests, appends through `ledger.chain.append` (so the chain check applies), and returns the entry with `verify_corpus` run in process. The actor and role are fields of `Change`. `tests/workflows/test_amend.py` (4 tests) applies an editorial amendment of STND.INSTR to a copy and verifies it with no failure. Met.
3. **`rehearse` runs a script on a fresh copy in a new temporary directory, runs `verify` there, reports the appended entries, and asserts the source is byte-identical before and after; a test appends an entry and checks both.** `govharness/workflows/rehearse.py` compares the SHA-256 of every file under the source root, ledger included, before and after, and raises `SourceChanged` naming the files. `tests/workflows/test_rehearse.py` (3 tests): the amendment script gains the copy one entry while the source digests stay equal; a script that appends to the source ledger is reported with `ledger.jsonl` named; the command prints the copy, `appended: 1`, the verify summary, and `source unchanged: N files`. Met.
4. **`derive.reading_copy` composes each divided standard; the header names each revision and its ledger entry from the ledger; `compose --write` writes to `rendered/`; `compose --check` reports each stale copy; the copies move to `rendered/` and are regenerated.** `tests/derive/test_reading_copy.py` (7 tests): the STND.DFLT header names entries 33, 37, 39, and 40 with their dates; an injected entry 42 appears in the header; every provision appears once under its section; the register MNEM follows the history of STND.IDENT; `--write` then `--check` pass on a copy and an edited provision makes `rendered/defaults.md` stale; and `rendered/` in the repository is current (regression guard). `python -m govharness compose governance --check` prints `stale: 0`. Against the moved copies, only the title spelling (taken from the corpus), the header, and the section headings of STND.DRAFT changed; every provision body, history, and the register are byte for byte as before. `constitution-lvl0.md` stays where it was and is not composed. Met.
5. **The criteria of unit 0001 still hold.** `git diff --stat 99d9a78 -- governance` prints nothing (1). `tests/test_architecture.py` passes with the new modules; the only new effects are the sync in `ledger/chain.py` and the temporary copy of `workflows/rehearse.py`, both allowed by decision 0001 (2, 3). The equivalence harness, rerun on `verify`, `check`, `manifests --check`, and `references --check`, whose behavior this unit does not change: 135 outputs, 0 differ (4; table below). Every test passes: `TMPDIR=<scratch> python3 -B -m unittest discover -s tests -t .`, 44 tests, OK, in 70 s (5). `tests/test_conventions.py` passes and ruff prints "All checks passed!" (6). `tools/` holds the five shims (7). `archive/tools-flat/` is unchanged (8). `README.md` names `compose`, `rehearse`, the amendment primitives, and `rendered/` (9). Each commit above is one kind of change, by the agent author (10). Met.

   Rerun of the regression guard, `TMPDIR=<scratch> python3 -B tests/equivalence/run_equivalence.py --work <scratch>/eq-u2` (the SHA-256 of each output, or the exit code):

   | Input | Command | Output | SHA-256 | Identical |
   | --- | --- | --- | --- | --- |
   | live | `verify` | stdout | 6b8f7ae3c7863c62d7614684cdc4d72e5f20dbccb80b88590a7c77dc743807ad | yes |
   | live | `verify` | exit | 0 | yes |
   | live | `verify --no-z3` | stdout | 6b8f7ae3c7863c62d7614684cdc4d72e5f20dbccb80b88590a7c77dc743807ad | yes |
   | live | `verify --no-z3` | exit | 0 | yes |
   | live | `check --out-dir` | stdout | 093410888bb88363ec979b119fd78f81366d1ab6089034a7924cc563277aa4ef | yes |
   | live | `check --out-dir` | exit | 0 | yes |
   | live | `check --out-dir` | logic_report.md | 78016420168642dccadf0d4d12bf0ba42cfb7196356edbf419ae687f212ef4b4 | yes |
   | live | `check --out-dir` | logic_facts.json | 87a284677d850e2c7e3c7ed10699a2cb57fd4214b342ec693d4867e3bb4974ea | yes |
   | live | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | live | `check --out-dir --no-z3` | stdout | ab7848890634f04ec714cecaa62174b4f6f53bc6e2a51ee3e3dbc5289978ae42 | yes |
   | live | `check --out-dir --no-z3` | exit | 0 | yes |
   | live | `check --out-dir --no-z3` | logic_report.md | 32e7d1a26f3a120ee5d6dd1181b5f34adb02332ddc0a65354b7c5755e42bba05 | yes |
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
   | structure | `check --out-dir` | logic_report.md | 9af407903fe0ed04bf01ebbae4c3cc7a9cfc5cbac67a81f7791a9b8b38c3b40f | yes |
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
   | manifests | `check --out-dir` | logic_report.md | ec2fb18b0a0ff8e27a7c71444b6850ed40ede7c526db111a744ce9dd444b389a | yes |
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
   | ledger-chain | `check --out-dir` | logic_report.md | 2cee7243f4d4fdf03a422bd2d11b156efbc8cfc94d9700154ffed7b348f9ca78 | yes |
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
   | signature-unregistered | `check --out-dir` | logic_report.md | a6e52a9d1e6927db5b3133353f505dcbd945d0d85025d167e29621898fed0936 | yes |
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
   | signature-forged | `check --out-dir` | logic_report.md | 7c61358f7294203713f8ec6d90bae904ae3ec3e441512832b27a1f39076a3e9e | yes |
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
   | lineage | `check --out-dir` | logic_report.md | db81d9e62539a2e8347c157bc54962384c3f8082537ef6ef188e8fdc10eb9aad | yes |
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
   | drafting | `check --out-dir` | logic_report.md | dbabbf40ebe6a535cf1ccefc5dcb426b1ea033655bc4adb7db42645549f25612 | yes |
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
   | revision | `check --out-dir` | logic_report.md | f6fea1deb1a0ef800e2e87fa0aed7e0ce8866ff3ce1acc9a5cf710d010aaf27a | yes |
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
   | identifier | `check --out-dir` | logic_report.md | fa46defe106715a8dad0ddbfaf02944d56b8c69561a451da4b5b43b230c0c3ce | yes |
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
   | logic | `check --out-dir` | logic_report.md | 39a2cd1a0c32dd2382a735431489571b8ac44c3d154e8d2250f8d3a150f8b0c4 | yes |
   | logic | `check --out-dir` | logic_facts.json | c734b369a5f2a2a76c7085bfff188c726c292c7a83706490f98b749eed93e148 | yes |
   | logic | `check --out-dir` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | logic | `check --out-dir --no-z3` | stdout | 4421a33e249be966b8f058ed8460ebbf8f5c99f298440738e1b2a6daf5e2c122 | yes |
   | logic | `check --out-dir --no-z3` | exit | 1 | yes |
   | logic | `check --out-dir --no-z3` | logic_report.md | 5d96686c5eb25ac20507171b954d2675b181edf1c9417d32d99152d75ae21cdc | yes |
   | logic | `check --out-dir --no-z3` | logic_facts.json | c734b369a5f2a2a76c7085bfff188c726c292c7a83706490f98b749eed93e148 | yes |
   | logic | `check --out-dir --no-z3` | drafting_punch_list.md | d8bbb9f8fd39be11a745ba90cf5e71646eeb29b958a3cfddcdf1083da5e92822 | yes |
   | logic | `manifests --check` | stdout | 183e19245240475fbcb229c48b4b27b5e58f858fa43edc310a6b2376a5621d66 | yes |
   | logic | `manifests --check` | exit | 1 | yes |
   | logic | `references --check` | stdout | e48cc0c6bd729e84637114cecd0e3c3edfcc7d19c73045ab1113282da02070df | yes |
   | logic | `references --check` | exit | 0 | yes |

### Defects

Fixed here, because the unit's criteria cover it: `ledger append` no longer appends to a broken chain (defect 6 of unit 0001).

Still open, and outside this unit: defects 1 to 5 and 8 of the record of unit 0001. Found in this unit:

1. The scratch helper `amend.py` found the last history row anywhere in the document; `raise_revision` searches only under the Revision History heading, so a numbered row of another table can no longer receive the row.
2. A rehearsal script runs with the full rights of the user; `rehearse` detects a change to the source after the fact but cannot prevent a write outside both trees. The copy is kept in the temporary directory for inspection and is not removed.
