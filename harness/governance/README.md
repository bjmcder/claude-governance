# Governance corpus

This directory is the authoritative text of the governance (GOV.35). You can read it with no software at all.

## Find anything by its identifier

An identifier maps to a path by turning dots into slashes:

| Identifier | File |
| --- | --- |
| `PRIME.6` | `PRIME/6.md` |
| `GOV.12` | `GOV/12.md` |
| `HW.FPGA` (a document) | `HW/FPGA/_doc.md` |
| `HW.FPGA.2` (a provision) | `HW/FPGA/2.md` |
| `LEX.agent` (a Lexicon term) | `LEX/agent.md` |
| `STND.DRAFT` (a standard) | `STND/DRAFT/_doc.md` |
| `STND.DRAFT.7` (a provision of a standard) | `STND/DRAFT/7.md` |
| `LVL0#normative-language` (a section locator: document, `#`, heading in lowercase with hyphens) | the "Normative Language" heading of `LVL0/_doc.md` |

Each directory's `_doc.md` describes the document itself. That is its title, level, status, and opening text. Each other file is one provision, term, or entry.

## Every file has the same shape

A front-matter block between `---` lines holds the fields, one per line, written as JSON values. The provision text follows it in Markdown. Only the text is normative. The fields are an index, and where they disagree with the text, the text governs.

## The three kinds of support file

- **`MANIFEST.csv`** (one per directory) lists every entry and subdirectory, with its title, status, and SHA-256 hash. The root manifest lists the top-level directories; it is not the mnemonic register, which is `MNEM/_doc.md`. Manifests are generated and informative only (GOV.39). Never edit one by hand.
- **`ledger.jsonl`** (at the root) is the append-only, hash-chained history of every governance transaction (GOV.36). Each line pins the hash of the content it adopted or reviewed. Any change to that content made outside the ledger is therefore detectable.
- **`README.md`** files are orientation only.

## Layout

| Path | Level | Holds |
| --- | --- | --- |
| `LVL0/` | LVL0 | Constitution record: Preamble, Normative Language, revision history |
| `PRIN/`, `PRIME/` | LVL0 | Governing Principles; prime directives |
| `GUARD/`, `VV/`, `REPRO/`, `INTPR/`, `DSGN/`, `SIMPL/`, `RSRC/`, `QA/` | LVL0 | General Articles |
| `GOV/` | LVL0 | Governance Article |
| `LEX/` | LVL0 | Lexicon, one file per term |
| `AGENT/`, `NUMER/`, `MEAS/`, `CPS/`, `ML/`, `HW/` (with `CPU/`, `GPU/`, `QPU/`, `EMBED/`, `FPGA/`, `ASIC/`), `HDES/` (with `FPGA/`, `ASIC/`) | LVL1 | Profiles and sub-profiles |
| `STND/` | LVL2 | Standards, one subdirectory each |
| `KNOW/` | none | Knowledge base; informs, never governs (GOV.32) |
| `TAG/` | none | Tag vocabulary, one subdirectory per facet |
| `MNEM/` | none | Mnemonic register (GOV.37, STND.IDENT.19); changed only by ledger transactions of type `register` (STND.IDENT.20) |
| `<NAME>/` | LVL3 | One directory per project, copied from `_PROJECT/NAME/` |
| `_PROJECT/` | none | Project template; directories starting with `_` are not part of the corpus |

## Making a change

Every change is a ledger transaction (GOV.36). Only the human owner or the custodians adopt (PRIME.1). Agents draft and propose. The harness (`python -m govharness`, run from `..`) fetches governance (`show`, `find`, `context`), regenerates manifests, appends transactions, and verifies the corpus. Without it, `../README.md` shows how to perform each check by hand.
