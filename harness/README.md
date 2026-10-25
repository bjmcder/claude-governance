# Governance harness prototype

A plain directory tree holds the governance. One small package, `govharness`, serves it: it fetches what applies to a question, an item with its cross references or the governance on a topic, so that a reader, human or agent, loads only that, and it keeps the corpus consistent. The code is a convenience, not the governance, and no work depends on it. If it is lost, `governance/` remains complete and readable (GOV.38, INTPR.12); the section below on reading without software says how.

## Fetching governance

```bash
python -B -m govharness show governance STND.INSTR.4              # text, what governs it, what it cites, what cites it
python -B -m govharness show governance LVL0#normative-language   # one section of a document
python -B -m govharness show governance STND.DFLT                 # a document: its sections and items, named
python -B -m govharness find governance destructive action        # ranked items and sections, one line each
python -B -m govharness context governance remote write --budget 6000 --in-force
                                                                  # the governance on a topic, within a budget
```

`find` and `context` take keywords: each word matches its other forms ("deleting" finds "deletion"), the items holding every word come first, and where none holds every word, those holding the most. `show --expand` adds the text of what an item cites. Texts are returned whole or named (STND.HARN.1 to STND.HARN.3). An agent uses these commands instead of reading or searching the corpus files; they change nothing.

## Layout

```text
harness/
├── README.md                 this file
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
├── rendered/                 reading copies of six standards (compose --write)
├── govharness/               the harness code, one layered package (decision 0001)
│   ├── __main__.py           python -m govharness <command>
│   ├── core/                 layer 0
│   │   ├── entry.py          entry model, front matter, identifier ↔ path
│   │   ├── corpus.py         reads the corpus (the only module that does), index
│   │   ├── hashing.py        SHA-256 and the canonical JSON the ledger hashes
│   │   ├── locators.py       identifiers, section locators, resolution
│   │   ├── text.py           sentences, quoted mentions, identifiers in text
│   │   ├── tables.py         Markdown tables and sections by heading
│   │   └── report.py         CheckResult and Report, the result model
│   ├── ledger/               layer 1
│   │   ├── transactions.py   transaction types, chain links, signature digest
│   │   ├── chain.py          reads and appends ledger files
│   │   ├── gpg.py            gpg processes and the signer configuration
│   │   ├── register.py       the signer register SIGNR and its text edits
│   │   └── signatures.py     verifies a ledger's signatures against SIGNR
│   ├── checks/               layer 2, reads and writes no file
│   │   ├── base.py           Check, Verdict, CheckContext
│   │   ├── registry.py       the family lists and the runner
│   │   ├── verification.py   verify as data on a snapshot: structural, then
│   │   │                     logic checks
│   │   ├── structure.py      ids, mnemonics, references
│   │   ├── manifests.py      manifests are current
│   │   ├── ledger.py         chain, pins, and signatures
│   │   ├── fields.py         template owner fields, entry status
│   │   ├── logic/            checks 0 and a to f: facts, tiers, wording,
│   │   │                     authority, language, proofs, satlib (DPLL, optional z3),
│   │   │                     solvecache (keys and checks of reused solves)
│   │   ├── lineage/          checks l.1 to l.5: derivation and family
│   │   ├── drafting/         checks g.0 to g.25: tables, context, modals,
│   │   │                     expressions, citations, roles, style, family
│   │   ├── revisions/        checks v.1 to v.11: classes, history, adopters,
│   │   │                     identifiers, family
│   │   └── combination.py    checks m.1 and m.2: profile combination
│   ├── query/                layer 2, read-only: graph (citations, lineage),
│   │                         retrieval (show, find, context),
│   │                         combination (selectors, shared matters, pairs)
│   ├── derive/               layer 2, returns {path: text}, writes nothing
│   │   ├── manifests.py      every MANIFEST.csv
│   │   ├── references.py     each document's References table
│   │   ├── reading_copy.py   the reading copy of each divided standard
│   │   └── environment/      an agent's environment from STND.HARN.18:
│   │                         outcomes, inputs, claude_code (adapter)
│   ├── workflows/            layer 3
│   │   ├── amend.py          amendment primitives: replace text, raise a
│   │   │                     revision, record a transaction and verify
│   │   ├── rehearse.py       run an amendment script on a fresh copy
│   │   ├── verification.py   load a corpus root and verify it
│   │   ├── solve_store.py    the solve cache on disk, outside the corpus
│   │   ├── signers.py        found the signer register, add, close, require
│   │   └── environment.py    check the installed environment files
│   ├── cli/                  layer 4: main.py (parser), reports.py (verify,
│   │                         check), derived.py (manifests, references,
│   │                         compose), query.py (show, find, context, pairs),
│   │                         records.py (ledger append, sign, rehearse),
│   │                         environment.py, arguments.py
│   └── hooks/guard.py        the pre-action guard the environment runs;
│                             standard library only, imports no package code
├── tests/                    tests mirroring the package; equivalence/ holds
│                             the regression guard against the flat tools
└── records/                  units, reviews, decisions, and dependencies of
                              the code; the findings log of entries 1 to 45
```

## Current state

As of ledger entry 175 (2026-10-25). `show governance ID` prints the current text and revision of any document.

| Level | Contents | Status |
| --- | --- | --- |
| LVL0 | 186 provisions in 11 parts, 155 Lexicon terms, the constitution record | Ratified, revision 1.6; pinned by ledger entry 1, amended by entries 2 to 7, 17, 23, 30, and 46 (entry 31 annotates 30) |
| LVL1 | 7 profiles and 8 sub-profiles, each divided into numbered provisions | Adopted |
| LVL2 | 32 standards, each divided into numbered provisions | Adopted |
| Knowledge and tags | `KNOW/` and the seven tag facets of `TAG/` | Planned |
| LVL3 | Template with project constitution, register, and one example each of authorization, waiver, ruling, axiom, hazard, and safe range | Template |

| Document | Revision | Provisions | Title |
| --- | --- | --- | --- |
| AGENT | 1.1 | 47 | Agent practice |
| NUMER | 1.3 | 29 | Numerical computation |
| HW | 1.1.2 | 22 | Execution hardware; sub-profiles CPU (5), GPU (4), QPU (8), EMBED (6), FPGA (4), ASIC (4) |
| HDES | 1.0.2 | 15 | Hardware design; sub-profiles FPGA (5), ASIC (12) |
| CPS | 1.0.1 | 9 | Cyber-physical and actuation |
| MEAS | 1.0 | 7 | Measurement and instrumentation |
| ML | 1.0.1 | 7 | Learned models |
| STND.DRAFT | 1.4 | 42 | Drafting standard |
| STND.IDENT | 1.3.3 | 23 | Identifier scheme and mnemonic register |
| STND.CLASS | 1.3.1 | 12 | Consequence-class criteria (identifiers 8, 9, and 11 to 16 withdrawn) |
| STND.DFLT | 1.5.1 | 31 | Defaults |
| STND.INSTR | 1.4 | 10 | Agent instructions |
| STND.HARN | 1.3 | 30 | Harness specification |
| STND.VVUQ | 1.4 | 83 | Verification, validation, and uncertainty quantification methods |
| STND.CODE | 1.2 | 21 | Coding standard |
| STND.THRT | 1.0 | 9 | Threat-model template |
| STND.KNOW | 1.0.1 | 14 | Knowledge base and tags |
| STND.DEPS | 1.0 | 11 | Dependency policy |
| STND.PROJ | 1.2 | 7 | Project constitution template |
| STND.WPROC | 1.1 | 15 | Work process standard |
| STND.CREW | 1.1 | 23 | Agent roles standard |
| STND.DOCS | 1.0 | 14 | Documentation standard |
| STND.CXX | 1.2 | 27 | C++ standard |
| STND.PY | 1.1 | 37 | Python standard |
| STND.JL | 1.2 | 41 | Julia standard |
| STND.ANNEX | 1.0 | 10 | Hardware type annex |
| STND.MPI | 1.0.1 | 25 | Message Passing Interface standard |
| STND.CONC | 1.1 | 30 | Concurrency standard |
| STND.OMP | 1.0.2 | 33 | OpenMP standard |
| STND.OFFLD | 1.0.1 | 31 | Accelerator offload standard |
| STND.BUILD | 1.0.2 | 26 | Build standard |
| STND.WFLOW | 1.0 | 40 | Workflow and long-run resilience standard |
| STND.STDC | 1.1 | 40 | C standard |
| STND.RUST | 1.1 | 34 | Rust standard |
| STND.FTN | 1.1 | 36 | Fortran standard |
| STND.SV | 1.1 | 28 | Verilog and SystemVerilog standard |
| STND.LEAN | 1.0.1 | 31 | Lean standard |
| STND.PERF | 1.0 | 26 | Performance evaluation standard |
| STND.TEST | 1.0 | 19 | Testing methods standard |

The ledger holds 175 transactions: 48 `adopt`, 101 `amend`, 17 `register`, 3 `review`, 3 `rule`, and 3 `annotate`. The mnemonic register `governance/MNEM/_doc.md` (STND.IDENT.19) holds every mnemonic in use; a new mnemonic, including that of a project or of a kind of LVL3 instrument, is registered by the custodians (STND.IDENT.23).

## Commands

Python 3.11+, standard library only. Run from this directory:

```bash
python -B -m govharness verify governance            # every check; exit 1 on failure
python -B -m govharness verify --no-logic governance # structural checks only
python -B -m govharness check governance --out-dir <scratch>   # logic report
python -B -m govharness verify --no-cache governance # solve every claim afresh
python -B -m govharness manifests governance --check # list stale manifests
python -B -m govharness manifests governance --write # regenerate manifests
python -B -m govharness references governance --check          # References tables
python -B -m govharness references governance --write STND.DRAFT   # write one
python -B -m govharness ledger append governance --type adopt --actor NAME \
    --role custodians --authority GOV.41 --targets STND.DRAFT --scope STND/DRAFT \
    --rationale "Adoption of STND.DRAFT, revision 1.0, ..."
python -B -m govharness sign check governance/ledger.jsonl --ledger-id governance \
    --corpus governance                              # verify signatures
python -B -m govharness compose governance --check   # stale reading copies
python -B -m govharness compose governance --write   # regenerate rendered/
python -B -m govharness rehearse governance amendment.py  # dry run on a copy
python -B -m govharness pairs governance NUMER       # pairs to review before a change (STND.HARN.28)
python -B -m unittest discover -s tests -t .         # every test
```

| Command | Purpose |
| --- | --- |
| `show ROOT ID [--expand]` | Print an item or section (`ID` is an identifier or a locator) with what governs it, what it cites, and what cites it; a document is shown as its lead text and the names of its sections and items |
| `find ROOT WORD... [--limit N] [--in-force]` | List the items and sections holding the most of the words, best first, one line each; exit 1 when none holds any |
| `context ROOT WORD... [--budget N] [--in-force]` | Print the best matches and the items they cite, each whole while the budget of characters lasts, and name the rest |
| `verify [--no-logic] [--no-z3] [--no-cache \| --cache-dir DIR] ROOT` | Run the structural checks and the logic checks; print a summary; exit 1 on a failure; exit 2 when the cache cannot be used, or a file's front matter or a ledger line cannot be read, naming the file; reuse checked solver results from the solve cache unless `--no-cache` (below) |
| `check ROOT [--out-dir DIR] [--no-z3] [--no-cache \| --cache-dir DIR]` | Run the logic checks, one line each; with `--out-dir`, write `logic_report.md`, `logic_facts.json`, and `drafting_punch_list.md` there; the solve cache as for `verify` |
| `manifests ROOT (--check \| --write)` | List the stale manifests, or regenerate them |
| `references ROOT (--check \| --write ID ...)` | Report each adopted document whose References table is wrong, or whose text names a document by bare identifier without citing it (g.25), or write the tables of the named documents (STND.DRAFT.34). `--write` derives a table from the citations only, so a bare name is fixed by citing a provision of the document, or the document in parentheses, and writing the table again |
| `compose ROOT (--check \| --write)` | List the stale reading copies of STND.DFLT, STND.INSTR, STND.DRAFT, STND.IDENT (with the register MNEM), STND.CLASS, and STND.HARN, or write them into `rendered/` beside ROOT; each header names every revision and its ledger entry |
| `ledger append ROOT --type ... --rationale ...` | Check the existing chain (sequence numbers, links, hashes), refuse a broken one, and append one hash-chained transaction, synced to disk, under an exclusive lock of the ledger file; `--sign KEY [--gnupg-home DIR]` signs it; `--ledger-file PATH --ledger-id ID` appends to a work ledger. An entry that would fail `verify` for good is refused, and nothing is written: an unsigned entry whose actor the signer register requires to sign it (use `--sign`), an unsigned transaction whose scope names `SIGNR` while the register exists (the anchor key signs the founding and a listed signer every later change), a register transaction while the register has problems, a scope other than that of an older pin whose content it shares (STND.HARN.9 keeps that pin in force; record the change with its scope), a file name with a control character under the scope, and a line that does not read back as the entry (unit 0016) |
| `sign found ROOT --date ... --role ... --name ... --key-file ...` | Found the signer register SIGNR with its first key |
| `sign add-signer REGISTER --ledger ... --role ... --name ... --key-file ...` | Add a signer and its public key |
| `sign close-signer REGISTER --ledger ... --fingerprint ... --last-entry N` | Set the last entry a key may sign |
| `sign require REGISTER --ledger ... --actor ... --from-entry N` | Require an actor's signature from an entry on |
| `sign check LEDGER --ledger-id ID --corpus ROOT [--signer-config PATH]` | Check the chain and verify the signatures of the corpus ledger and, for a work ledger, of that ledger; fail if the corpus has no signer register, or if the corpus ledger lacks the entry that the head pin of the signer configuration names (below) |
| `environment ROOT --work PATH --home PATH [--open PATH]... [--domain D]... [--tool PATTERN]... [--search] [--unattended] [--assured] [--secret-store] [--secret NAME]... [--authorization ID]... [--role ROLE] [--expiry-horizon DAYS\|none] [--accept-unsigned] (--write OUT \| --check)` | Derive the configuration of an agent's environment from the outcomes of STND.HARN.18 and the protected locations of STND.INSTR.3 (adapter `claude-code`); `--secret-store` states that the human owner provides the store of STND.DFLT.29, and each `--secret NAME` opens one file of it to the agent, so that every other file of the store lies outside the working bounds; each `--authorization ID` names an authorization file of the corpus whose remote writes the guard lets proceed while it is in force for the `--role` (STND.HARN.29), a summary of each is printed, and one not in force exits 1 with the reason: managed settings, the guard and its policy under `OUT/root/`, `coverage.md` (STND.HARN.19), `entry-draft.json` (STND.HARN.20), and `INSTALL.md`; `--check` compares the files installed under `/` with a fresh rendering and reports each missing, differing, or alterable one, and each program the configuration runs (`/usr/bin/python3` for the hook, `/usr/bin/bwrap` and `/usr/bin/socat` for the sandbox) that is missing or alterable (STND.HARN.21); `INSTALL.md` names those programs, says to install from the output directory, and prints the check, from this directory, with the absolute corpus root and every option of the derivation, so that it renders the same files, and the `ledger append` that adds the draft entry to the corpus ledger (unit 0014); where the work is not assured and the corpus holds no signer register and its ledger records none, a derivation that names an authorization exits 1 unless `--accept-unsigned` is given, and then the summary, `coverage.md`, and `entry-draft.json` name each authorization relied on unsigned (unit 0010); where a signature is required, the option has no effect; `--expiry-horizon` bounds the time from the derivation to an authorization's expiry, 90 days unless another whole number of days is given, so that an expiry beyond it, or `until revoked`, exits 1 with the reason, `--expiry-horizon none` lifts the bound, the summary names the horizon in force, and a value that is neither is a usage error (exit 2) (unit 0012); a missing or malformed table, or an input the configuration would misread, exits 1 with a message |
| `pairs ROOT ID [--amends LVL0_ID ...]` | List, as a Markdown table, each pair of provisions that STND.HARN.28 puts to review before a change of the document `ID`: one provision on the changed side (the document, and for a change of LVL0 every provision instantiating a provision named by `--amends`), the other in another document in force, at least one in a profile or sub-profile, given for one matter by the shared-matters tables or instantiating one LVL0 provision outside GOV and PRIN; exit 2 when `ID` is not in the corpus |
| `rehearse ROOT SCRIPT` | Copy the corpus into a new temporary directory, run the script's `apply(root)` on the copy, verify the copy, print the entries the script appended and the verify summary, and fail if any file or directory of the source changed (the root is resolved first, so a script that changes the working directory cannot redirect the comparison) |

Every `ROOT` (and `--corpus`) must be an existing directory; any other path is a usage error, exit 2.

The regression guard `tests/equivalence/run_equivalence.py` compares the package with the pre-package scripts in `archive/tools-flat/`. That directory is not part of this repository, so the guard stops with an error here; the unit tests do not depend on it.

### Amendments

An amendment is a short Python script that applies the primitives of `govharness.workflows.amend` to the root it is given: `replace_text(root, path, [(old, new)])` for each text change (each old text occurs exactly once), `raise_revision(root, "STND/DFLT", "1.5", "1.5.1", row)` for each document whose revision changes, and `record_transaction(root, Change(...))`, which appends the unsigned transaction with the actor and role it is given, then rebuilds the manifests, and returns the entry with the verification that follows. Every refusal of the ledger comes before anything is written, and an entry that the signer register requires to be signed is refused: record it with `ledger append --sign` instead (unit 0016). None of them holds a path of its own. Rehearse the script first with `rehearse`, from this directory so that the script can import the package; run it on the live corpus only after the rehearsal verifies and confirms the source unchanged. After an amendment, run `compose governance --write` so that `rendered/` stays current.

## Reading and applying the corpus without software

Nothing in `govharness/` is needed to read, apply, or audit the governance (GOV.38, INTPR.12); each check is the test its provision states, and a person can perform it with `sha256sum`, `sed`, and `gpg`. Commands below run from `governance/`.

1. Start at `governance/README.md`. An identifier is a path: `GOV.12` is `governance/GOV/12.md`, `STND.DRAFT` is `governance/STND/DRAFT/_doc.md`. The front matter lists the fields; the text below it is normative and governs where the fields disagree.
2. To find what applies, read `LVL0/_doc.md` (Normative Language, the parts and their order in GOV.5), then the provision files, then the lower documents. Each provision below LVL0 lists in `instantiates` the higher provisions it makes more specific.
3. To confirm a file is unchanged, compute its SHA-256 and compare with its row in the `MANIFEST.csv` of its directory; a directory row holds the SHA-256 of the subdirectory's manifest.
4. Chain (STND.HARN.8). Each line of `ledger.jsonl` is one transaction, ending at a line feed only (a text field may hold U+2028, U+2029, or U+0085, which are not line ends here), written with sorted keys, no spaces, and UTF-8 unescaped, so deleting its field `hash` from the text leaves what the hash covers. Line N's `hash` must equal the first output below, and its `prev` the `hash` of line N-1 (`null` for line 1); `seq` must be N:

   ```bash
   sed -n "${N}p" ledger.jsonl | sed 's/"hash":"[0-9a-f]*",//' | tr -d '\n' | sha256sum
   ```

5. Content pin (STND.HARN.9). The latest transaction with a given `scope` pins its `corpus_hash`, which must equal the output below, with the scope's paths listed in place of `$SCOPE` (the term Content hash of STND.HARN orders files part by part; byte order gives the same order for this corpus):

   ```bash
   for s in $(printf '%s\n' $SCOPE | LC_ALL=C sort); do
     find "$s" -type f -name '*.md' | LC_ALL=C sort | while read -r f; do
       printf '%s:%s\n' "$f" "$(sha256sum "$f" | cut -c1-64)"; done
   done | head -c -1 | sha256sum
   ```

6. Signatures (STND.HARN.11 to STND.HARN.13). A signature covers the entry digest, the output of step 4 with the second `sed` replaced by `sed 's/"hash":"[0-9a-f]*",//; s/"signature":"[^"]*"/"signature":""/'`. Write that 64-character digest, with no line feed, to a file; write the `signature` value, with each `\n` read as a line feed, to `sig.asc`; import the public keys under the headings of the signer register `SIGNR`; then run `gpg --verify sig.asc digest`. Whether the key may sign that entry is the term Accepted signature of STND.HARN: an open row for `all` accepts the key on every ledger, even where its row for that ledger is closed, so a key meant to be closable is registered per ledger, and `sign add-signer` and `sign close-signer` refuse a row beside an `all` row of the same key and role label (unit 0016). The founding key is the `anchor` fingerprint in `/etc/governance/signer.json`. If that file names a `head`, line `seq` of the ledger must have that `hash`.
7. Configuration (STND.DFLT.22 and STND.DFLT.15). A configuration that a `configure` entry records displaces a provision only for assured work (CSQ0 or CSQ1), and only while operative: confirmed in the current session by a verifier that the agent is unable to alter, such as the human owner. Each file the entry names is present with the SHA-256 it records, and no part of its path is writable by the agent's account. For other work, a configuration displaces nothing. A checkpoint mechanism counts while found installed as the entry states, for assured work by such a verifier. Otherwise the provisions apply.
8. To change the governance, follow GOV.40 and GOV.41: a change is a ledger transaction by the human owner or the custodians, never an edit alone. By hand, edit a copy, check it as above, copy it back, and append a line with the fields of STND.HARN.7, computing `corpus_hash` and `hash` as in steps 5 and 4.

## What `verify` checks

1. Every file's `id` matches its path.
2. Every top-level directory is a well-formed mnemonic.
3. Every cited identifier or section locator (`cites`, `governed_by`, `instantiates`, `refers_to`) resolves. A locator is a document identifier, a number sign, and a heading slug (`LVL0#normative-language`). A bare LVL0 section name, as the Lexicon's governing column uses, resolves against the LVL0 headings; any other unknown or malformed reference fails.
4. Every manifest is current.
5. The ledger chain is intact (each entry's sequence number is its position, its `prev` is the hash of the entry before it, and its `hash` is its own), and the content each transaction pinned is unchanged. An edit made outside the ledger fails this check (GOV.36). Any transaction may pin a subpath such as `STND/DRAFT`; the content is compared with the latest transaction of the same scope, so a pin holds until the next transaction of that scope (STND.HARN.9), even where another scope covers the same files. So `ledger append` and `record_transaction` refuse, before writing, a scope that shares content with the pin of another scope, naming it: record the change with that scope. Two scopes over the same files, once both pinned, would leave no transaction that records a change of them without staling the other (unit 0016). A file name with a control character under a scope in force fails, since the content hash joins names with line feeds. A ledger that is missing or empty fails where the corpus holds Markdown. A `review` transaction (QA.7) records an independent review; it is not a revision, so check v.4 ignores it. A scope that names no directory of the corpus (or leaves it, through `..` or an absolute path) is refused by `ledger append` and reported by this check.

   The signer configuration, `/etc/governance/signer.json`, which only the human owner writes, is trusted over the corpus. Where the running account could alter it, its anchor and head pin are ignored, and `verify` and `sign check` fail and name the file, so that a pin is never dropped without a word. Where it names an `anchor`, a corpus without `SIGNR` fails, so a ledger rewritten without its signatures after `SIGNR` was removed does not pass. So the owner founds `SIGNR` (`sign found`, then its register transaction, signed by the anchor key) and sets `anchor` together, the register first: with either alone `verify` fails, the founding for want of the anchor, or the corpus for want of the register. Where it names a `head`, `{"seq": N, "hash": "<hash of entry N>"}`, a ledger whose entry N is missing or has another hash fails `verify` and `sign check`. Any prefix of an intact chain is itself intact, and only the head pin shows a cut: without one, any entries at the end of the ledger can be removed by an account that can write `ledger.jsonl` and `verify` still passes, a `revoke` or a `register` change among them. With one, the entries up to N are held, and those after N can still be cut. So a revocation is durable only once the owner has pinned the head at or after it. To pin the head, after `verify` passes, take `seq` and `hash` from the last line of `ledger.jsonl`, for example `tail -n 1 governance/ledger.jsonl | python3 -c 'import json,sys; e=json.load(sys.stdin); print(json.dumps({"seq": e["seq"], "hash": e["hash"]}))'`, and set them as `head` in the configuration. Move the pin forward after each transaction that must not be lost.

   A crash during an append can leave the last line cut short. Every later append and `verify` then refuse, naming the file and the line. The cut entry was never synced whole, so its append did not return: remove the partial last line, after checking that it does not parse as JSON, and append the transaction again.
6. Every owner field of a project template names a role (STND.IDENT).
7. Every entry carries the status of the `_doc.md` in its directory, and an entry of an adopted or ratified document carries an adoption date, so that adopting a document cannot leave its provisions at draft.
8. The logic checks (`check`). Only a `FAIL` fails the run; `WARN` findings are printed. Use `--no-logic` to skip them and `--no-z3` to force the built-in solver.

## What the logic checks cover

Facts are read from the provision text and front matter, never from a hand-kept list. Each structural role (precedence, waiver, non-waivable, and so on) is a configured identifier confirmed against its title, with a title search as fallback, so renumbering does not break the checks.

| Check | Claim established |
| --- | --- |
| 0 | Every structural role resolves to a provision |
| a.1 to a.3 | GOV.5 is a strict total order; every part is ranked or declared unranked; front-matter `rank` agrees with the text |
| b.1 to b.6 | GOV.45's named items exist; `waivable` flags agree with GOV.45; no part is both waivable (GOV.44) and non-waivable; PRIME.15 cites the amendment and waiver procedures; self-grant prohibitions resolve; the amendment and waiver procedures are themselves non-waivable |
| c.1 to c.5 | No sentence puts one action in two incompatible authority tiers; `cites` matches the identifiers in the text of each LVL0 provision; loud failure links to the safe state; back-links from the reserved classes; no standing authorization covers an excluded action |
| d.0 to d.6 | Expressions LVL0 bars are unused (FAIL); SHOULD and prefer are listed; Lexicon definitions carry no capitalized normative word; d.5 lists normative-table words that no provision uses, and d.2 is unused. Table rows are data and are not scanned. The drafting standard's own expression lists are checked by g.5 and g.6 |
| e.1 to e.4 | Lexicon terms are complete, resolve, and are unique; unused terms are listed |
| l.1 to l.5 | Every provision below LVL0 instantiates something that resolves, reaches LVL0 directly, acyclically, and only upward; stored `rank` and `waivable` agree with the values derived from the ancestors; every LVL2 provision is marked binding or default consistently with its lineage; a prime directive's instantiators are non-waivable. These fail for every provision (PRIME.15, GOV.17, GOV.19) |
| g.1 to g.24 | The drafting standard, below |
| g.25 | Each document below LVL0 holds the References table derived from its citations: the identifiers and locators in its text, its provisions, and their reference fields (STND.DRAFT.34). A document at LVL1 to LVL3 also cites each document its text names by a bare identifier ("HDES", "STND.DOCS"); a bare name without a citation is a defect, whose fix is a citation, from which the row is derived. Not read for bare names: LVL0 and entries of no level, the Revision History, every row of a table whose header names a column Example, quoted spans, and code (unit 0013; `tools/check_refs.py` prints the findings) |
| v.1 to v.8 | Revision numbers and withdrawn identifiers (STND.IDENT): every document carries a well-formed `revision` that agrees with its status; the revision history steps by the class of each change and ends at the `revision` field; the ledger holds one transaction of the right type for each revision; adopter fields name a Lexicon role; the table of revision classes is present; provisions and checks refer to each other. These fail, except that a date mismatch in v.4 warns. `verify` also checks the owner fields of the project template, which the corpus view leaves out; v.8 fails on a gap in a document's numbering that its field `withdrawn` does not list, or on a listed identifier in use |
| v.9 to v.11 | Identifiers and the mnemonic register (STND.IDENT.15 to STND.IDENT.23): v.9 fails on an identifier or locator not in the form for its kind, or a Lexicon slug that differs from its term; v.10 fails on a malformed or duplicated register row and on an inactive or unregistered mnemonic or grade in the identifier of an item that is not retired, and lists for a reader sibling mnemonics at a letter distance of 1 that are not established acronyms; v.11 fails on a transaction with the scope MNEM that is not of type `register` by the custodians |
| m.1, m.2 | Profile combination (STND.HARN.26, STND.HARN.27): m.1 fails on an attribute of the selector table of a profile or sub-profile in force that the document its Defined by column names does not define in its Terms; m.2 fails on a shared matter with more than one owning profile, on a provision that a shared-matters table gives for another profile's matter and that cites no provision of that profile, and on a listed provision that does not exist |
| f.1 to f.8 | The facts and axioms are jointly satisfiable, and each structural claim is proved by refuting its negation, or shown not to be forced |

The built-in DPLL solver needs no installation. Its unit propagation watches two literals of each clause, so it visits only the clauses that an assignment can make unit or false, and it splits in a fixed order: the first unassigned variable of the first clause not yet satisfied, in the order the clauses are built, false before true. Propagation reaches the same assignment, or a conflict, in whatever order it visits the clauses, so the solver gives the same statuses, models, and cores as the solver it replaced, which rescanned every clause on each pass (unit 0009); `tests/checks/test_satlib.py` compares it with brute force and with that solver on 3000 seeded random formulas. With it, `verify` of the corpus takes about 3 s where it took about 11 s on the same machine (unit 0009). `z3` is used only if it is already importable; both give the same statuses.

The solve cache (unit 0011) keeps the result of each solve under a SHA-256 key of everything the result depends on: every clause in order, with its name and its literals in order (the claim enters as the clause of its negation), the backend and z3's version, and a digest of the source of `satlib.py`, `solvecache.py`, and `core/hashing.py`. A change of any of them is a new key and a full solve, so a transaction that leaves the authority-tier statements and LVL0's precedence and waivers as they were reuses every result, across rehearsal copies too. An entry holds the status, the backend, the model as bits, and the core as positions in the clause set, and no corpus text. It is reused only after a check against the clause set, so a planted or damaged entry can change no verdict: a model must satisfy every clause, and a core must be exactly the one the built-in solver's minimisation finds, which takes one search per core fact instead of one per fact. A core found by z3 is neither saved nor reused: it cannot be checked to be the one a fresh z3 run would list, and z3 finds it again quickly; a z3 model is reused after the same check as any model. An entry that fails, or a file that is no plain entry (a link, a pipe, too large), is named on the standard error and recomputed; the standard output is the same with a cold cache, a warm one, or none. The cache lies in `--cache-dir DIR`, else `$GOVHARNESS_CACHE_DIR`, else `govharness/solves` under `$XDG_CACHE_HOME` or `~/.cache`; `--no-cache` or `GOVHARNESS_NO_CACHE=1` (which also reaches `rehearse` and amendment scripts) turns it off. A directory inside the corpus, through `..` or a link too, and a relative `GOVHARNESS_CACHE_DIR` are refused, by `record_transaction` and `rehearse` before they write anything; a relative `--cache-dir` is taken from the working directory. `verify`, `check`, `rehearse`, and `record_transaction` use the cache; a library call of `verify_corpus` does not unless passed `cache=True`. Deleting it costs only time. With a warm cache, `verify` of the corpus takes about 2.0 s where it takes about 3.0 s without (unit 0011). `tests/checks/test_logic.py` damages an in-memory copy of the corpus in 13 ways and asserts the named check fails, so a passing run means the checks can fail.

### Provisions below LVL0

A provision below LVL0 is one file with these fields besides the common ones:

| Field | Meaning |
| --- | --- |
| `instantiates` | Higher provisions it makes more specific, by identifier or section locator; at least one is a LVL0 node (PRIME.15) |
| `refers_to` | Provisions it names without instantiating them |
| `rank`, `waivable` | Derived, not chosen: the highest rank among the LVL0 provisions reached, and waivable only when every one reached is waivable; a section, a document, or a Lexicon term is not waivable (GOV.5, GOV.17). The harness verifies the stored values |
| `mode` (LVL2) | `binding` or `default` (GOV.19). A provision whose derived waivability is false is binding |
| `binding_reason` (LVL2) | Required for a binding provision that reaches no prime directive, GUARD provision, GOV provision, or floor obligation (GOV.10 places PRIME, GUARD, and GOV in the floor; this part list is the one hand-kept list) |
| `defines` | Name of a table the provision holds; the harness reads each table it uses by this name and its column headings, as for the drafting standard tables, `revision-classes`, `environment-outcomes`, `selector`, and `shared-matters` |
| `checked_by` | Check keys that verify it; `review` means a reader decides |

Text identifiers must equal `instantiates` plus `refers_to` (g.16).

### The drafting standard (g family)

The engine reads the tables of STND.DRAFT (modal set, excluded expressions, vague qualifiers, quantifiers, role words, person words, spelling), expands every expression to its inflections, and scans four groups of subjects. A finding of class defect is certain by the standard's own words; one of class review is a candidate for a reader.

| Group | Subjects | Result |
| --- | --- | --- |
| self | STND.DRAFT itself | defect fails, review warns |
| lower | other numbered provisions below LVL0 | defect fails when the standard is adopted and the provision enforced is binding, warns otherwise; review is listed |
| draft | standards not yet divided into numbered provisions | listed in the punch list, never fails |
| lvl0 | LVL0 provisions, to which the standard does not apply | listed as an advisory list for amendment, never fails |

A provision with exactly three modals is a review finding of g.18, so `verify` warns on STND.DRAFT.35, STND.DRAFT.39, and STND.DRAFT.42, whose bundles were reviewed and ratified as never applied apart. `check --out-dir DIR` writes `drafting_punch_list.md` with every listed finding. `tests/checks/test_drafting.py` damages an in-memory copy in 41 ways and asserts the named check reaches its severity; it also asserts the clean corpus has no failure or warning in the l and g families other than those three. g.23 verifies that every provision names its checks and every check enforces a provision.

### Revisions (STND.IDENT)

A revision number is `major.minor` or `major.minor.editorial`, as in 1.0 or 1.0.3. The editorial segment is shown only when above zero. A change takes the first class of the table in STND.IDENT.3 whose test it meets: **major** alters a prime directive or governing principle in its fundamental motivation or intent, or restructures the articles wholesale (raises the major segment); **minor** is an ordinary amendment that leaves the fundamental motivation and intent as they were (raises the minor segment); **editorial** alters no obligation, permission, or defined meaning (raises the editorial segment). A step raises one segment by one and resets those to its right. A document is below 1.0 until first adopted. Each revision is a row of the document's revision history, whose change entry opens with the class words, and one ledger transaction whose reason text names the revision. A document of kind constitution, profile, sub-profile, or standard carries the field `revision` and names its adopter by role label in `adopted_by` (`ratified_by` for the constitution), as in The Custodian. Project template owner fields read The Human Owner.

## Not yet built

- Trigger and tag fields are empty, and the knowledge base and tag vocabulary are planned.
- There is no agent context manifest (agent brief) or action-class index.
- `find` and `context` match words, not meanings: "push" finds the items that say "push", not the definition of remote write, and a question in full sentences matches its common words; give the corpus's own terms.
- The environment adapter for Claude Code enforces none of the ten outcomes of STND.HARN.18 in full and all ten in part, so its draft entry of STND.DFLT.22 settles no provision; `coverage.md` states each gap.
- The guard (`govharness/hooks/guard.py`) reads a shell command line's quotes, comments, joined lines, here-documents (with the substitutions of a body whose delimiter is not quoted), substitutions, and compound commands; it resolves a `..` after a symbolic link where the system does, and reads a pattern as reaching every protected name it may match and every item it matches when it runs, where that item's links lead. Where that reading is uncertain it refers the line: a `#` next to an escaped character, a comment or `case` inside a command substitution, a POSIX bracket expression in a pattern, and a line in which a second, simpler reading of where commands begin finds a command the first did not read. It reads `sponge`, `ed`, and `ex` as writers of the files they name. It also refers what it cannot read soundly: an alias of git given in the call (which it reads as the command it stands for as well), a setting given by `git -c` other than a few plain ones, a variable of git set in the call other than its pager, its editors, and those of the author and committer and three more that name no program, an `ext::` or `fd::` URL, a transport program named by `--upload-pack`, `--receive-pack`, `--exec`, or clone's `-u` (it reads as well the value of each such setting and variable, and the command of an `ext::` URL or a transport program; the value of a pager or editor setting or variable it reads as a command line), a write of git's configuration other than a few plain settings, a subcommand that is not a command of git, a command that `xargs` builds from its input unless its program only reads, a shell or `source` that runs a computed script or reads its commands from a pipe or a substitution, also behind a launcher such as `env`, `nice`, or `timeout`, `rg --pre`, and a call whose reading would take more than 20 000 paths or 3 s, or, as a backstop, more than a hard wall of 7 s, so that it answers inside the hook's timeout of 10 s (unit 0015 and its reviews, from the QA.8 review of the guard). A program that acts by itself, such as a script or an interpreter given code, is still not seen, nor an alias in git's configuration named like one of git's script commands where that script is not installed. By the re-review of unit 0015, these stay unseen as known limits: a program word that is computed, a glob, a brace, or split by `env -S`, including behind a launcher; a git variable or assignment not given as a literal `NAME=value` word; a `-c` setting that `git clone` or `submodule` gives after the subcommand; the first file of `git merge-file` behind a valued option; a script that `ed`, `ex`, or `vim` runs; an alias used after `shopt -s expand_aliases` or a joined `mapfile -C` callback; and a write by `sed`'s `w` command or `shuf -o`. The module's docstring and `coverage.md` list what is not read.
- Remote writes named by an authorization (unit 0008; STND.HARN.29, STND.PROJ.6, and STND.PROJ.7, adopted as STND.PROJ 1.2 and STND.HARN 1.2 in ledger entries 140 and 141; a QA.8 code review is owed before installation). `--authorization ID` with `--role ROLE` opens the writes of a standing authorization in force that extends to that role, and `--expiry-horizon DAYS` sets the owner's bound on the time from the derivation to its expiry. The bound is 90 days unless the owner gives another, since an expiry also bounds how long an installed configuration keeps relying on an authorization after a revocation it does not see; under a bound, an authorization whose expiry lies beyond it, or that lapses only when revoked, is refused with the reason, and `--expiry-horizon none` lifts the bound. The summary names the horizon in force, and `--check` needs the horizon its derivation was given, since it derives the configuration afresh (unit 0012). A signature verified by the signer register is required for assured work and wherever a signer register exists. Elsewhere an agent is able to append an `authorize` naming the human owner and recompute the chain, so the derivation is refused unless the owner passes `--accept-unsigned`; the printed summary, the coverage report, and the draft entry then name each authorization accepted unsigned, and the owner's reading of the summary is the only check that the owner granted what it pins (unit 0010). Where the corpus holds no `SIGNR` but the ledger records a register (a signed entry, or a transaction pinning `SIGNR`), or the signer configuration under `/etc` names the anchor key that founds one, the signature stays required and the derivation is refused; a ledger entry whose shape the command cannot read counts as such a record and is named in the reason. Without an anchor configured, an agent that rewrites the whole ledger from the founding entry on, with the chain recomputed, and removes `SIGNR` is not detected (unit 0010). Since no signer register is founded yet, every derivation that names an authorization in this corpus needs the option. The guard answers `allow` only for two kinds it reads, compared as whole strings: a `git push` of local branches to the remote's one configured address, or to that address given whole, from inside the work's own valid repository, and a `gh issue create`, `gh issue comment`, or `gh pr comment` with `--repo HOST/OWNER/REPO` and literal text; each only as one command of plain words, with no expansion, substitution, redirection, or here-document, and only while the git configuration, the repository's hooks directories, and the environment hold nothing the guard does not model. Until unit 0014's review, a hook defined in the configuration (`hook.<name>.command` with `hook.<name>.event`) was not read and could run in an allowed push; now any key of the sections `hook`, `gpg`, and `protocol`, and `push.gpgSign` and `ssh.variant`, refers the push, so a push that the configuration signs stays referred. Of the variables of git, only `GIT_EDITOR` (which Claude Code sets in the agent's shell), `GIT_SEQUENCE_EDITOR`, `GIT_PAGER`, and `GIT_TERMINAL_PROMPT` set to `0` or `false` leave a push unreferred, since a push launches no editor, pages only under `--paginate` or `pager.push` (both referred), and the last only stops a prompt; every other `GIT_` variable, and every `GH_` variable, refers the write, and the reason names the variable (unit 0014). Every other remote write is referred as far as the guard recognizes the command; a program it does not read writes unseen, as before. The text rules that refer every push and every such post stay, so whether the guard's `allow` outranks them is for an installation test (unit 0008); until it passes, an authorized write may still be referred. A `credential.helper`, or any other key of the `credential` section, in the git configuration makes every push referred, since the guard reads that section as one that may redirect a push; an owner who uses a credential helper gains nothing from a push authorization until the guard models it. A revocation takes effect once the configuration is derived again and installed; the guard checks the expiry at each call. Whether the sandbox's narrower `allowRead` for an opened secret wins over the store's `denyRead` pattern is not settled by the documentation either, and waits on the installation test of unit 0008.
- No signer register is founded yet, so every `signature` field is blank.
- Authority tiers are classified per sentence by wording. Cross-provision action classes (the same action named in two provisions) are not compared.
- Imperative sentences are found by a verb list, not a parse (g.8, review).
- Whether a quoted expression is mentioned or used, whether a qualifier has a criterion, and whether a citation names something the provision really makes more specific are left to a reader (`checked_by: review`).

All of these belong to STND.HARN.
