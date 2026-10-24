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

```text
harness/
├── README.md                 this file
├── governance/               the corpus (see governance/README.md)
│   ├── MANIFEST.csv          root manifest (lists top-level mnemonics)
│   ├── ledger.jsonl          append-only, hash-chained transactions
│   ├── LVL0/  PRIN/  PRIME/  GUARD/  VV/  REPRO/  INTPR/
│   ├── DSGN/  SIMPL/  RSRC/  QA/  GOV/  LEX/      LVL0, ratified
│   ├── AGENT/ NUMER/ MEAS/ CPS/ ML/ HW/{CPU,GPU,QPU,EMBED,FPGA,ASIC}/   LVL1, planned
│   ├── STND/{DFLT,CLASS,DRAFT,IDENT,INSTR,HARN,KNOW,ANNEX,CODE,DEPS,THRT,PROJ}/   LVL2
│   ├── KNOW/  TAG/{FIELD,PROB,METH,HW,QTY,ACTV,COMP}/
│   └── _PROJECT/NAME/        LVL3 project template
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
│   │   │                     authority, language, proofs, satlib (DPLL, optional z3)
│   │   ├── lineage/          checks l.1 to l.5: derivation and family
│   │   ├── drafting/         checks g.0 to g.25: tables, context, modals,
│   │   │                     expressions, citations, roles, style, family
│   │   └── revisions/        checks v.1 to v.11: classes, history, adopters,
│   │                         identifiers, family
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
│   │   ├── signers.py        found the signer register, add, close, require
│   │   └── environment.py    check the installed environment files
│   ├── cli/                  layer 4: main.py (parser), reports.py (verify,
│   │                         check), derived.py (manifests, references),
│   │                         records.py (ledger append, sign, rehearse),
│   │                         environment.py, arguments.py
│   └── hooks/guard.py        the pre-action guard the environment runs;
│                             standard library only, imports no package code
├── tests/                    tests mirroring the package; equivalence/ holds
│                             the regression guard against the flat tools
├── archive/tools-flat/       the pre-package scripts, unchanged (reference)
└── records/                  units, decisions, and dependencies of the code
```

## Current state

| Part | Contents | Status |
| --- | --- | --- |
| LVL0 | 186 provisions in 11 parts, 155 Lexicon terms, the constitution record | Ratified 2026-10-08, revision 1.5 (2026-10-10); pinned by ledger entry 1, amended by entries 2 to 7, 17, 23, and 30 (entry 31 annotates 30) |
| LVL1 | 6 profiles and 6 HW sub-profiles: selector and scope stated, no provisions yet | Planned |
| LVL2 | 12 standards. Six are adopted and divided into numbered provisions: DRAFT, 34 provisions (revision 1.2.1; reviewed at 0.3 by ledger entry 8, adopted as 1.0 by entry 9, editorial 1.0.1 to 1.0.3 by entries 11, 20, and 26, minor 1.1 by entry 29, minor 1.2 by entry 34, editorial 1.2.1 by entry 44); IDENT, 23 on revision numbers, identifiers, and the mnemonic register (revision 1.3.2; adopted by entry 10, review recorded as entry 12, minor 1.1 to 1.3 by entries 18, 25, and 27, editorial 1.3.1 and 1.3.2 by entries 35 and 45); CLASS, 12 on consequence-class criteria (revision 1.2.2; reviewed at 0.4 by entry 13, adopted by entry 14, amended by entries 16, 21, 22, 24, and 36; identifiers 8, 9, and 11 to 16 withdrawn); DFLT, 26 binding provisions providing the GOV.21 mechanisms, a work ledger signed for assured work, and bounds of reach for work without a project constitution (revision 1.2; adopted by entry 33, editorial 1.0.1 and 1.0.2 by entries 37 and 39, minor 1.1 and 1.2 by entries 40 and 42; drafts 0.1 and 0.2 archived in `archive/`); INSTR, 8 binding provisions of agent practice (revision 1.1; adopted by entry 38, minor 1.1 by entry 41; the undivided draft 0.1 archived). HARN, 25 binding provisions on read-only retrieval, the corpus, the ledgers, signatures, generated content, checks, the optional derived agent environment, and rehearsal (revision 1.0; adopted by entry 43). Five carry existing drafts as one undivided body: ANNEX, CODE, DEPS, THRT, PROJ. One is a stub: KNOW. | Adopted (DRAFT, IDENT, CLASS, DFLT, INSTR, HARN), draft, or planned |
| Knowledge and tags | Roots and the seven tag facets | Planned |
| LVL3 | Template with project constitution, register, and one example each of authorization, waiver, ruling, axiom, hazard, and safe range | Template |

The mnemonic register `governance/MNEM/_doc.md` (STND.IDENT.19) holds every mnemonic in use, 57 rows, seeded by ledger entry 28 (type `register`); the second-level STND mnemonics are final. A new mnemonic, including that of a project or of a kind of LVL3 instrument, is registered by the custodians (STND.IDENT.23).

## Commands

Python 3.11+, standard library only. Run from the repository root:

```bash
python -B -m govharness verify governance            # every check; exit 1 on failure
python -B -m govharness verify --no-logic governance # structural checks only
python -B -m govharness check governance --out-dir <scratch>   # logic report
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
python -B tests/equivalence/run_equivalence.py       # regression guard against archive/tools-flat
```

| Command | Purpose |
| --- | --- |
| `show ROOT ID [--expand]` | Print an item or section (`ID` is an identifier or a locator) with what governs it, what it cites, and what cites it; a document is shown as its lead text and the names of its sections and items |
| `find ROOT WORD... [--limit N] [--in-force]` | List the items and sections holding the most of the words, best first, one line each; exit 1 when none holds any |
| `context ROOT WORD... [--budget N] [--in-force]` | Print the best matches and the items they cite, each whole while the budget of characters lasts, and name the rest |
| `verify [--no-logic] [--no-z3] ROOT` | Run the structural checks and the logic checks; print a summary; exit 1 on a failure |
| `check ROOT [--out-dir DIR] [--no-z3]` | Run the logic checks, one line each; with `--out-dir`, write `logic_report.md`, `logic_facts.json`, and `drafting_punch_list.md` there |
| `manifests ROOT (--check \| --write)` | List the stale manifests, or regenerate them |
| `references ROOT (--check \| --write ID ...)` | Report each adopted document whose References table is wrong, or write the tables of the named documents (STND.DRAFT.34) |
| `compose ROOT (--check \| --write)` | List the stale reading copies of STND.DFLT, STND.INSTR, STND.DRAFT, STND.IDENT (with the register MNEM), and STND.CLASS, or write them into `rendered/` beside ROOT; each header names every revision and its ledger entry |
| `ledger append ROOT --type ... --rationale ...` | Check the existing chain (sequence numbers, links, hashes), refuse a broken one, and append one hash-chained transaction, synced to disk, under an exclusive lock of the ledger file; `--sign KEY [--gnupg-home DIR]` signs it; `--ledger-file PATH --ledger-id ID` appends to a work ledger |
| `sign found ROOT --date ... --role ... --name ... --key-file ...` | Found the signer register SIGNR with its first key |
| `sign add-signer REGISTER --ledger ... --role ... --name ... --key-file ...` | Add a signer and its public key |
| `sign close-signer REGISTER --ledger ... --fingerprint ... --last-entry N` | Set the last entry a key may sign |
| `sign require REGISTER --ledger ... --actor ... --from-entry N` | Require an actor's signature from an entry on |
| `sign check LEDGER --ledger-id ID --corpus ROOT [--signer-config PATH]` | Check the chain and verify the signatures of the corpus ledger and, for a work ledger, of that ledger; fail if the corpus has no signer register |
| `environment ROOT --work PATH --home PATH [--open PATH]... [--domain D]... [--tool PATTERN]... [--search] [--unattended] [--assured] (--write OUT \| --check)` | Derive the configuration of an agent's environment from the outcomes of STND.HARN.18 and the protected locations of STND.INSTR.3 (adapter `claude-code`): managed settings, the guard and its policy under `OUT/root/`, `coverage.md` (STND.HARN.19), `entry-draft.json` (STND.HARN.20), and `INSTALL.md`; `--check` compares the files installed under `/` with a fresh rendering and reports each missing, differing, or alterable one (STND.HARN.21); a missing or malformed table, or an input the configuration would misread, exits 1 with a message |
| `pairs ROOT ID [--amends LVL0_ID ...]` | List, as a Markdown table, each pair of provisions that STND.HARN.28 puts to review before a change of the document `ID`: one provision on the changed side (the document, and for a change of LVL0 every provision instantiating a provision named by `--amends`), the other in another document in force, at least one in a profile or sub-profile, given for one matter by the shared-matters tables or instantiating one LVL0 provision outside GOV and PRIN; exit 2 when `ID` is not in the corpus |
| `rehearse ROOT SCRIPT` | Copy the corpus into a new temporary directory, run the script's `apply(root)` on the copy, verify the copy, print the entries the script appended and the verify summary, and fail if any file or directory of the source changed (the root is resolved first, so a script that changes the working directory cannot redirect the comparison) |

Every `ROOT` (and `--corpus`) must be an existing directory; any other path is a usage error, exit 2.

The retired one-time scripts that built the corpus (`import_lvl0.py`, `scaffold.py`, `scaffold_spec.json`) and the flat code they belonged to are kept in `archive/tools-flat/`; run from there, they rebuild the empty corpus of ledger entry 1:

```bash
cd archive/tools-flat
python import_lvl0.py <ratified-lvl0.md> ../../governance
python scaffold.py ../../governance <drafts-dir>
python ledger.py ../../governance --type adopt --actor "" --role custodians \
    --authority GOV.40,GOV.41 --targets LVL0 \
    --scope LVL0,PRIN,PRIME,GUARD,VV,REPRO,INTPR,DSGN,SIMPL,RSRC,QA,GOV,LEX \
    --rationale "Ratification of LVL0 Revision 1.0." --at 2026-10-08T00:00:00+00:00
python build_manifests.py ../../governance
```

An amendment is a short Python script that applies the primitives of `govharness.workflows.amend` to the root it is given: `replace_text(root, path, [(old, new)])` for each text change (each old text occurs exactly once), `raise_revision(root, "STND/DFLT", "1.1", "1.1.1", row)` for each document whose revision changes, and `record_transaction(root, Change(...))`, which rebuilds the manifests, appends the unsigned transaction with the actor and role it is given, and returns the entry with the verification that follows. None of them holds a path of its own. Rehearse the script first with `rehearse`, from the repository root so that the script can import the package; run it on the live corpus only after the rehearsal verifies and confirms the source unchanged.

This needs the revision 1.0 export of LVL0; it writes STND.DRAFT, STND.IDENT, and STND.CLASS as planned stubs and does not replay transactions 2 to 14. To restore the current corpus, copy `governance/` with `ledger.jsonl` and run `verify`. The scaffold never overwrites a standard that is past planned.

## Reading and applying the corpus without software

Nothing in `govharness/` is needed to read, apply, or audit the governance (GOV.38, INTPR.12); each check is the test its provision states, and a person can perform it with `sha256sum`, `sed`, and `gpg`. Commands below run from `governance/`.

1. Start at `governance/README.md`. An identifier is a path: `GOV.12` is `governance/GOV/12.md`, `STND.DRAFT` is `governance/STND/DRAFT/_doc.md`. The front matter lists the fields; the text below it is normative and governs where the fields disagree.
2. To find what applies, read `LVL0/_doc.md` (Normative Language, the parts and their order in GOV.5), then the provision files, then the lower documents. Each provision below LVL0 lists in `instantiates` the higher provisions it makes more specific.
3. To confirm a file is unchanged, compute its SHA-256 and compare with its row in the `MANIFEST.csv` of its directory; a directory row holds the SHA-256 of the subdirectory's manifest.
4. Chain (STND.HARN.8). Each line of `ledger.jsonl` is one transaction, written with sorted keys, no spaces, and UTF-8 unescaped, so deleting its field `hash` from the text leaves what the hash covers. Line N's `hash` must equal the first output below, and its `prev` the `hash` of line N-1 (`null` for line 1); `seq` must be N:

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

6. Signatures (STND.HARN.11 to STND.HARN.13). A signature covers the entry digest, the output of step 4 with the second `sed` replaced by `sed 's/"hash":"[0-9a-f]*",//; s/"signature":"[^"]*"/"signature":""/'`. Write that 64-character digest, with no line feed, to a file; write the `signature` value, with each `\n` read as a line feed, to `sig.asc`; import the public keys under the headings of the signer register `SIGNR`; then run `gpg --verify sig.asc digest`. Whether the key may sign that entry is the term Accepted signature of STND.HARN. The founding key is the `anchor` fingerprint in `/etc/governance/signer.json`.
7. Configuration (STND.DFLT.22 and STND.DFLT.15, revision 1.2). A configuration that a `configure` entry records displaces a provision only for assured work (CSQ0 or CSQ1), and only while operative: confirmed in the current session by a verifier that the agent is unable to alter, such as the human owner. Each file the entry names is present with the SHA-256 it records, and no part of its path is writable by the agent's account. For other work, a configuration displaces nothing. A checkpoint mechanism counts while found installed as the entry states, for assured work by such a verifier. Otherwise the provisions apply.
8. To change the governance, follow GOV.40 and GOV.41: a change is a ledger transaction by the human owner or the custodians, never an edit alone. By hand, edit a copy, check it as above, copy it back, and append a line with the fields of STND.HARN.7, computing `corpus_hash` and `hash` as in steps 5 and 4.

## What `verify` checks

1. Every file's `id` matches its path.
2. Every top-level directory is a well-formed mnemonic.
3. Every cited identifier or section locator (`cites`, `governed_by`, `instantiates`, `refers_to`) resolves. A locator is a document identifier, a number sign, and a heading slug (`LVL0#normative-language`). A bare LVL0 section name, as the Lexicon's governing column uses, resolves against the LVL0 headings; any other unknown or malformed reference fails.
4. Every manifest is current.
5. The ledger chain is intact (each entry's sequence number is its position, its `prev` is the hash of the entry before it, and its `hash` is its own), and the content each transaction pinned is unchanged. An edit made outside the ledger fails this check (GOV.36). Any transaction may pin a subpath such as `STND/DRAFT`; the content is compared with the latest transaction of the same scope, so a pin holds until the next transaction of that scope. A `review` transaction (QA.7) records an independent review; it is not a revision, so check v.4 ignores it. A scope that names no directory of the corpus (or leaves it, through `..` or an absolute path) is refused by `ledger append` and reported by this check.

6. Every owner field of a project template names a role (STND.IDENT).

7. Every entry carries the status of the `_doc.md` in its directory, and an entry of an adopted or ratified document carries an adoption date, so that adopting a document cannot leave its provisions at draft.

8. The logic checks (`check`). Only a `FAIL` fails the run; `WARN`
   findings are printed. Use `--no-logic` to skip them and `--no-z3` to
   force the built-in solver.

## What the logic checks cover

Facts are read from the provision text and front matter, never from a
hand-kept list. Each structural role (precedence, waiver, non-waivable,
and so on) is a configured identifier confirmed against its title, with a
title search as fallback, so renumbering does not break the checks.

| Check | Claim established |
| --- | --- |
| 0 | Every structural role resolves to a provision |
| a.1 to a.3 | GOV.5 is a strict total order; every part is ranked or declared unranked; front-matter `rank` agrees with the text |
| b.1 to b.6 | GOV.45's named items exist; `waivable` flags agree with GOV.45; no part is both waivable (GOV.44) and non-waivable; PRIME.15 cites the amendment and waiver procedures; self-grant prohibitions resolve; the amendment and waiver procedures are themselves non-waivable |
| c.1 to c.5 | No sentence puts one action in two incompatible authority tiers; `cites` matches the identifiers in the text of each LVL0 provision; loud failure links to the safe state; back-links from the reserved classes; no standing authorization covers an excluded action |
| d.0 to d.6 | Expressions LVL0 bars are unused (FAIL); SHOULD and prefer are listed; Lexicon definitions carry no capitalized normative word. Table rows are data and are not scanned. The drafting standard's own expression lists are checked by g.5 and g.6 |
| e.1 to e.4 | Lexicon terms are complete, resolve, and are unique; unused terms are listed |
| l.1 to l.5 | Every provision below LVL0 instantiates something that resolves, reaches LVL0 directly, acyclically, and only upward; stored `rank` and `waivable` agree with the values derived from the ancestors; every LVL2 provision is marked binding or default consistently with its lineage; a prime directive's instantiators are non-waivable. These fail for every provision (PRIME.15, GOV.17, GOV.19) |
| g.1 to g.25 | The drafting standard, below |
| v.1 to v.8 | Revision numbers and withdrawn identifiers (STND.IDENT): every document carries a well-formed `revision` that agrees with its status; the revision history steps by the class of each change and ends at the `revision` field; the ledger holds one transaction of the right type for each revision; adopter fields name a Lexicon role; the table of revision classes is present; provisions and checks refer to each other. These fail, except that a date mismatch in v.4 warns. `verify` also checks the owner fields of the project template, which the corpus view leaves out; v.8 fails on a gap in a document's numbering that its field `withdrawn` does not list, or on a listed identifier in use |
| m.1, m.2 | Profile combination (STND.HARN.26, STND.HARN.27): m.1 fails on an attribute of the selector table of a profile or sub-profile in force that the document its Defined by column names does not define in its Terms; m.2 fails on a shared matter with more than one owning profile, on a provision that a shared-matters table gives for another profile's matter and that cites no provision of that profile, and on a listed provision that does not exist |
| v.9 to v.11 | Identifiers and the mnemonic register (STND.IDENT.15 to STND.IDENT.23): v.9 fails on an identifier or locator not in the form for its kind, or a Lexicon slug that differs from its term; v.10 fails on a malformed or duplicated register row and on an inactive or unregistered mnemonic or grade in the identifier of an item that is not retired, and lists for a reader sibling mnemonics at a letter distance of 1 that are not established acronyms; v.11 fails on a transaction with the scope MNEM that is not of type `register` by the custodians |
| f.1 to f.8 | The facts and axioms are jointly satisfiable, and each structural claim is proved by refuting its negation, or shown not to be forced |

### Provisions below LVL0

A provision below LVL0 is one file with these fields besides the common ones:

| Field | Meaning |
| --- | --- |
| `instantiates` | Higher provisions it makes more specific, by identifier or section locator; at least one is a LVL0 node (PRIME.15) |
| `refers_to` | Provisions it names without instantiating them |
| `rank`, `waivable` | Derived, not chosen: the highest rank among the LVL0 provisions reached, and waivable only when every one reached is waivable; a section, a document, or a Lexicon term is not waivable (GOV.5, GOV.17). The harness verifies the stored values |
| `mode` (LVL2) | `binding` or `default` (GOV.19). A provision whose derived waivability is false is binding |
| `binding_reason` (LVL2) | Required for a binding provision that reaches no prime directive, GUARD provision, GOV provision, or floor obligation (GOV.10 places PRIME, GUARD, and GOV in the floor; this part list is the one hand-kept list) |
| `defines` | Name of a table the provision holds; the harness reads the table by this name and its column headings (drafting standard tables and `revision-classes`) |
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

`check --out-dir DIR` writes `drafting_punch_list.md` with every listed finding. `tests/checks/test_drafting.py` damages an in-memory copy in 41 ways and asserts the named check reaches its severity; it also asserts the clean corpus has no failure or warning in the l and g families. g.23 verifies that every provision names its checks and every check enforces a provision.

The built-in DPLL solver needs no installation. `z3` is used only if it is
already importable; both give the same statuses. `tests/checks/test_logic.py` damages
an in-memory copy of the corpus in thirteen ways and asserts the named check
fails, so a passing run means the checks can fail.

Ported from the retired analysis toolkit with changes: Roman-numeral
parsing is gone; the old d.5 check (titles without an obligation verb) is
dropped because LVL0 provision titles are informative labels, d.5 now
lists normative-table words that no provision uses, and d.2 is unused; checks b.1,
b.2, c.2, d.6, and e.2 are new or recast for the one-file-per-provision
corpus.

### Revisions (STND.IDENT)

A revision number is `major.minor` or `major.minor.editorial`, as in 1.0 or 1.0.3. The editorial segment is shown only when above zero. A change takes the first class of the table in STND.IDENT.3 whose test it meets: **major** alters a prime directive or governing principle in its fundamental motivation or intent, or restructures the articles wholesale (raises the major segment); **minor** is an ordinary amendment that leaves the fundamental motivation and intent as they were (raises the minor segment); **editorial** alters no obligation, permission, or defined meaning (raises the editorial segment). A step raises one segment by one and resets those to its right. A document is below 1.0 until first adopted. Each revision is a row of the document's revision history, whose change entry opens with the class words, and one ledger transaction whose reason text names the revision. A document of kind constitution, profile, sub-profile, or standard carries the field `revision` and names its adopter by role label in `adopted_by` (`ratified_by` for the constitution), as in The Custodian. Project template owner fields read The Human Owner.

## Findings log

- STND.DRAFT 1.2.1 and STND.IDENT 1.3.2 (entries 44 and 45) name the
  package commands in their Checks sections, so the entry-point scripts in
  `tools/` are removed (DSGN.6; unit 0001 criterion 7).

- STND.DFLT 1.2 (entry 42) proportions assurance to class: signatures,
  confirmation by a verifier, and a configuration that displaces a
  provision apply only to assured work (CSQ0, CSQ1); for other work an
  unsigned owner entry or an agent's record of a grant is accepted, and a
  recorded configuration or checkpoint mechanism counts only while found
  installed in the session (Terms: Assured work, Operative).

- STND.DFLT 1.1 (entry 40) adds a fifth exempt class: a change or removal
  covered by a checkpoint whose mechanism and actions a signed entry
  records; the Terms define Checkpoint. STND.INSTR 1.1 (entry 41) names no
  tool or method (GOV.18) and defines Dry run; environment means are to be
  derived from the standards and recorded under STND.DFLT.22.

- STND.INSTR 1.0 was adopted on 2026-10-10 (entry 38): eight binding
  provisions of agent practice; the old draft's restatements of LVL0 and its
  default standing authorization were dropped. `test_ledger_pins` then edited
  STND/ANNEX, which no transaction pinned; since the adoption of STND.ANNEX
  1.0 (2026-10-23) it edits TAG.

- STND.DRAFT 1.2 (entry 34) adds STND.DRAFT.34: each document below LVL0
  holds a References table of the documents it cites, derived and checked
  by `references` and g.25. STND.IDENT 1.3.1, STND.CLASS 1.2.2, and
  STND.DFLT 1.0.1 (entries 35 to 37) conform; undivided drafts conform on
  re-derivation.

- STND.DFLT 1.0 was adopted on 2026-10-10 (entry 33), after LVL0 1.5
  (GUARD.7 temporary items, Lexicon Temporary item; entry 30) and the MNEM
  row SIGNR (entry 32). Entry 30 was appended by an agent error before the
  1.5 text reached the corpus: a rehearsal script ran the live ledger tool,
  so entry 30 pins revision 1.4. Entry 31 (type `annotate`) records the
  error and pins revision 1.5; entry 30 is not edited. The amendment
  primitives (`govharness.workflows.amend`) now take the corpus root as
  a parameter, and `rehearse` fails when a script changes the source.

- STND.DFLT 0.2 (2026-10-10) applies the custodian's rulings: no numeric
  bulk size and no time limits; listed scope, bounds of reach, and owner
  signatures. The harness signs ledger entries (`ledger append --sign`,
  `--ledger-id`) and verifies them against SIGNR with an anchor from
  `/etc/governance/signer.json` (`sign check`, `verify`). LVL0 1.5
  (GUARD.7, Temporary item) and the MNEM row SIGNR await ratification
  (`drafts/lvl0-1.5-proposal.md`).

- STND.DFLT 0.1 was drafted on 2026-10-10 and revised after two rounds of
  independent review; it sits in the corpus as a draft awaiting the QA.7
  review. The logic facts no longer read "reserved-action register" as a
  reservation.

- STND.IDENT part two was ratified on 2026-10-10 after an aggressive
  review for padding, atomicity, and consistency: STND.IDENT 1.3 (entry 27,
  STND.IDENT.15 to STND.IDENT.23 and checks v.9 to v.11), the initial
  register MNEM (entry 28, type `register`, 57 rows), and STND.DRAFT 1.1
  (entry 29, the term Locator defers to STND.IDENT.15 and STND.IDENT.16).
  The draft and its build scripts are kept in `drafts/`.

- Every remaining defect in the adopted documents was fixed on 2026-10-10
  by one amendment each, in order: STND.DRAFT 1.0.2 (entry 20, reviewer
  leaves the undefined role words), STND.CLASS 1.1.1 (entry 21, CSQ3
  auditor wording), STND.CLASS 1.2 (entry 22, a credible consequence
  includes foreseeable misuse), LVL0 1.4 (entry 23, Review keeps its
  ordinary meaning outside changes), STND.CLASS 1.2.1 (entry 24, field
  `withdrawn`), and STND.IDENT 1.2 (entry 25, STND.IDENT.14 and check
  v.8). Entry 19 (type `annotate`) records The Custodian as the actor of
  entries 1 to 18 and the agent authorship of their text (REPRO.5); from
  entry 19 every transaction names its actor.

- The global consistency review's governance findings are resolved. The
  custodian ruled under GOV.3 (entry 15, type `rule`) that the adopter's
  recorded decision satisfies the QA.7 review of a revision. Three minor
  amendments followed in order: STND.CLASS 1.1 (entry 16: reliance tests
  follow GOV.12, review drops its CSQ4 row, new STND.CLASS.20 ties the
  proportionality judgment to the classification), LVL0 1.3 (entry 17:
  Reviewer and Standards owner in the Lexicon, Promotion, Amendment, and
  Auditor redefined, NEVER in the list of capitalized words), and
  STND.IDENT 1.1 (entry 18: new STND.IDENT.13 states the ruling, and
  STND.IDENT.6 fixes how amendments are cited). Check e.2 now accepts
  LVL0 section locators in `governed_by`.

- STND.CLASS 0.4 (11 provisions) was reviewed by the custodian under QA.7
  (ledger entry 13, type `review`, scope STND/CLASS) and adopted as
  revision 1.0 (entry 14, type `adopt`, authority GOV.41, scope
  STND/CLASS); adoption changed only the status, revision, adoption dates,
  and revision history. A global consistency review followed; its
  harness and documentation findings are fixed, and its governance
  findings await amendments (see claude/reviews/global-review-2026-10-09.md).

- STND.DRAFT 0.3 (33 provisions) passes its own checks at FAIL severity.
  It was re-derived from the review of 0.1 as 0.2; the SHOULD NOT row of
  its modal table (0.3) follows LVL0 revision 1.1. The custodian reviewed
  0.3 under QA.7, and ledger entry 8 (type `review`, scope STND/DRAFT) pins
  the content reviewed: a later edit to STND/DRAFT fails the ledger check
  until a later transaction with the same scope pins the new content. The review accepts that provisions 3, 14, and
  23 are checked by the reader and that review-class flags remain. The
  custodian then ratified STND.DRAFT: revision 1.0 (ledger entry 9, type
  `adopt`, authority GOV.41, scope STND/DRAFT) changes only the status,
  revision, adoption date, and revision history of 0.3. The scope is the
  one standard, so edits to other standards stay free of its pin. From
  adoption, a defect in a binding numbered provision below LVL0 fails the
  checks; none exists now. STND.IDENT was adopted as 1.0 (ledger entry 10, scope STND/IDENT) with revision numbers only. The six undivided drafts
  are still drafts, and the undivided ones are listed in the g.24 punch
  list.

- Resolved: the lineage check l.4 counted only the prime directives,
  GUARD, and the four named floor obligations as forcing a binding mark,
  although GOV.10 places GOV in the floor too. GOV now forces the mark,
  so a LVL2 provision that instantiates a GOV provision is binding
  without a recorded reason (GOV.19). The drafting of STND.CLASS, whose
  criteria instantiate GOV.12 to GOV.24, exposed it.

- Resolved: the adoption of STND.DRAFT (entry 9) set the status of the
  standard but left its 33 provisions at draft. STND.DRAFT revision 1.0.1
  (entry 11, editorial, approved by the custodian) gives each provision
  the status adopted and the adoption date. The new `status` check of
  `verify` fails when an entry's status differs from its document's,
  so the slip cannot recur. The custodian's review of STND.IDENT under
  QA.7, implicit in its ratification, is recorded as entry 12.

- Resolved: LVL0 did not conform to the drafting standard. Revision 1.1
  (ledger entry 5, minor) added SHOULD NOT to Normative Language. Revision
  1.2 (entry 6, minor) made 42 edits in 40 provisions: excluded expressions
  (DSGN.14, GOV.18, GOV.32, GUARD.7, INTPR.11, INTPR.12, PRIME.4, PRIME.14,
  RSRC.7, RSRC.8, SIMPL.1, VV.4), the review-class words "could" and
  "considered", and the quantifier "any" wherever a plainer word served.
  The one edit that adds meaning is GUARD.18, which now names the human
  owner as the party who records what is practical. Revision 1.2.1 (entry
  7, editorial) replaced four "at will" phrasings of 1.2, which the
  standard reads as SHALL. The lvl0 group of the punch list now holds four
  items for the reader: "sufficient" in GOV.38 and PRIME.14 (the criterion
  is stated), "to the extent" in GUARD.18 (a decider and a record now
  stand with it), and "avoid" in PRIN.8 (a false positive: it is part of
  the obligation SHALL avoid harm).

- Resolved: `LEX.index` contained a capitalized NEVER (check d.6).
  Amended by ledger transaction 2 (GOV.40) as LVL0 revision 1.0.1; the
  logic checks now report no warning. A rebuild from scratch imports the
  current text and then replays the transactions.

- Resolved: owner fields were blank or lower case. `ratified_by` of LVL0
  and every `adopted_by` now name a role (LVL0 revision 1.0.3, ledger
  transaction 4, editorial); the project template names The Human Owner.
  Ledger transactions 1 to 3 keep their blank `actor`, because the ledger
  is append-only (PRIME.5).

- Resolved: the field `version` of profiles and standards was renamed
  `revision`, so every document uses one field (STND.IDENT.7).

- Resolved: provisions used three roles the Lexicon did not define. LVL0
  revision 1.0.2 (ledger transaction 3, GOV.40, editorial) adds `LEX.author`
  (REPRO.5, QA.7, GOV.34), `LEX.adopter` (GOV.41, GOV.42, GOV.46, GOV.49),
  and `LEX.auditor` (QA.2, GOV.47). The three words leave the undefined list
  of STND.DRAFT.29; g.19 now treats them as defined roles.

## Not yet built

- Trigger and tag fields are empty.
- There is no agent context manifest (agent brief) or action-class index.
- `find` and `context` match words, not meanings: "push" does not find
  "remote write", and a question in full sentences matches its common
  words; give the corpus's own terms.
- The environment adapter for Claude Code enforces no outcome in full and
  ten in part, so its draft entry of STND.DFLT.22 settles no provision;
  `coverage.md` states each gap.
- No signer register is founded yet, so every `signature` field is blank.
- Authority tiers are classified per sentence by wording. Cross-provision
  action classes (the same action named in two provisions) are not
  compared.
- Imperative sentences are found by a verb list, not a parse (g.8, review).
- Whether a quoted expression is mentioned or used, whether a qualifier
  has a criterion, and whether a citation names something the provision
  really makes more specific are left to a reader (`checked_by: review`).
- The six other draft standards are not yet divided into numbered
  provisions, so they are scanned as whole bodies for the punch list only.

All of these belong to STND.HARN.
