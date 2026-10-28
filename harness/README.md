# Governance harness

The harness is `govharness`, a Python package that uses the standard library alone, retrieves provisions from the governance corpus in [`governance/`](governance/README.md), and checks that the corpus agrees with its manifests and its ledger. It is optional and read-only for an agent: it installs no hook and sets no permission, and the corpus is complete and readable without it (GOV.38, INTPR.12).

[docs/installation.md](../docs/installation.md) covers installing the harness, [docs/operating.md](../docs/operating.md) covers looking up provisions with it, and [docs/architecture.md](../docs/architecture.md) describes the layout of the repository and of the package. This file is the reference for the custodian and for developers of the harness: every command, every check, the checks by hand, and the tests.

## Commands

Run from this directory, a command names the corpus `governance`. Installed (`pipx install ./harness` from the repository root; the argument is the directory that holds `pyproject.toml`, and a bare `harness` would name a package of the Python Package Index), the same command is `govharness <command>`. The installed package holds no corpus: `GOVHARNESS_ROOT` or a `ROOT` argument names a checkout of `governance/`. Where `ROOT` is in brackets it may be omitted: it is then `$GOVHARNESS_ROOT`, else `./governance` where that exists, as [docs/operating.md](../docs/operating.md#what-the-commands-return) describes; for `find` and `context`, the first argument is the root only where that directory holds `LVL0/_doc.md`, and a word naming another directory stays a word. The querying commands `show`, `find`, and `context`, with the questions they answer, are in that guide.

| Command | Purpose |
| --- | --- |
| `show [ROOT] ID [--expand] [--all]` | Print an item or section (`ID` is an identifier or a locator, in any case), with the onset of a provision beside its mode, and with what governs it, what it cites, and what cites it, each citing provision, term, entry, and tag on its own line and the citing lead texts and sections folded into one line per heading (`Notes of: AGENT, CPS, …`); a document is shown as its lead text and the names of its sections and items, and with `--all` each item it holds follows, whole, in id order, under its own heading, a part of LVL0 opened and a standard under STND named only; exit 1 when no item has the identifier |
| `find [ROOT] WORD... [--limit N] [--in-force]` | List the items and sections holding the most of the words, best first, one line each: provisions, terms, entries, and tags before Terms sections, before Notes and other prose; a document identifier among the words matches what lies below it; exit 1 when none holds any |
| `context [ROOT] WORD... [--budget N] [--in-force]` | Print the best matches and the items they cite, each whole while the budget of characters lasts, and name the rest, a section larger than the budget among them (STND.HARN.3); exit 1 when no item holds a word |
| `verify [--no-logic] [--no-z3] [--cache DIR] [ROOT]` | Run the structural checks and the logic checks; print a summary; exit 1 on a failure; exit 2 when no root is known, the cache cannot be used, or a file's front matter or a ledger line cannot be read, naming the file; reuse checked solver results from the solve cache only where `--cache DIR` or `GOVHARNESS_CACHE` names one (below), and otherwise write nothing |
| `check ROOT [--out-dir DIR] [--no-z3] [--cache DIR]` | Run the logic checks, one line each; with `--out-dir`, write `logic_report.md`, `logic_facts.json`, and `drafting_punch_list.md` there; the solve cache as for `verify` |
| `manifests ROOT (--check \| --write)` | List the stale manifests, or regenerate them |
| `references ROOT (--check \| --write ID ...)` | Report each adopted document whose References table is wrong (g.25), or write the tables of the named documents (STND.DRAFT.34). The table holds a row for each cited document, a document that the text names by its bare identifier included (the term Cited document of STND.DRAFT), and a citation of a withdrawn provision counts for the document that withdrew it |
| `compose ROOT (--check \| --write)` | List the stale reading copies of STND.DFLT, STND.INSTR, STND.DRAFT, STND.IDENT (with the register MNEM), STND.CLASS, and STND.HARN, or write them into `rendered/` beside ROOT; each header names every revision and its ledger entry |
| `compose ROOT --all DIR [--check]` | Write a reading copy `<ID>.md` of every document into DIR, or with `--check` list the stale ones; a Markdown file of DIR that no document produces is named as an orphan, never removed, and fails the check; the repository's `rendered/` is this set, rebuilt after each round ([custodian's guide](../docs/custodian-guide.md#checking-the-corpus-after-a-round)) |
| `ledger append ROOT --type ... --rationale ...` | Check the existing chain (sequence numbers, links, hashes), refuse a broken one, and append one hash-chained transaction, synced to disk, under an exclusive lock of the ledger file; `--sign KEY [--gnupg-home DIR]` signs it; `--ledger-file PATH --ledger-id ID` appends to a work ledger. An entry that would fail `verify` for good is refused, and nothing is written: an unsigned entry whose actor the signer register requires to sign it (use `--sign`), an unsigned transaction whose scope names `SIGNR` while the register exists (the anchor key signs the founding and a listed signer every later change), a register transaction while the register has problems, a scope other than that of an older pin whose content it shares (STND.HARN.9 keeps that pin in force; record the change with its scope), a file name with a control character under the scope, and a line that does not read back as the entry |
| `sign found ROOT --date ... --role ... --name ... --key-file ...` | Found the signer register SIGNR with its first key |
| `sign add-signer REGISTER --ledger ... --role ... --name ... --key-file ...` | Add a signer and its public key |
| `sign close-signer REGISTER --ledger ... --fingerprint ... --last-entry N` | Set the last entry a key may sign on a ledger, closing each open row of that key and ledger |
| `sign require REGISTER --ledger ... --actor ... --from-entry N` | Require an actor's signature from an entry on |
| `sign check LEDGER --ledger-id ID --corpus ROOT [--signer-config PATH]` | Check the chain and verify the signatures of the corpus ledger and, for a work ledger, of that ledger; fail if the corpus has no signer register, or if the corpus ledger lacks the entry that the head pin of the signer configuration names (below) |
| `pairs [ROOT] ID [--with ID ...] [--amends LVL0_ID ...]` | List, as a Markdown table, each pair of provisions that STND.HARN.28 puts to review before a change of the documents or provisions named: one provision on the changed side (each provision of a document named, each provision named, and for a change of LVL0, named by its article as `ID`, every provision instantiating a provision named by `--amends`), the other in another document, at least one in a profile or sub-profile, given for one matter by the shared-matters tables, or, where both lie in documents named or in documents of provisions named, instantiating one LVL0 provision outside GOV and PRIN; exit 1, with one line on the standard error, when an `ID` names no document or provision below LVL0 (a LVL0 article only with `--amends`), an `--amends` identifier names no LVL0 provision, or no pair is listed |
| `onset [ROOT] CSQn` | List, one line each, the provisions and the parts of provisions that apply from the class CSQn (CSQ0 to CSQ3) by their field `onset`, which is what a reclassification to CSQn adds: a whole provision, or a provision with a named part (`STND.CODE.22, sentence 2`), each with its title, and a provision whose other parts start at a more severe class with its full onset after the title; the list does not filter by status, so a provision of a draft or planned document is listed too; exit 1 when nothing applies from the class |
| `rehearse ROOT SCRIPT` | Copy the corpus into a new temporary directory, run the script's `apply(root)` on the copy, verify the copy, print the entries the script appended and the verify summary, and fail if any file or directory of the source changed (the root is resolved first, so a script that changes the working directory cannot redirect the comparison) |

Every `ROOT` (and `--corpus`) must be an existing directory; any other path is a usage error, exit 2. `show`, `find`, `context`, `pairs`, and `onset` exit 0 when something was found, 1 when nothing was, with the message on the standard error, and 2 for a usage error.

Examples, from this directory:

```bash
python3 -B -m govharness verify governance            # every check; exit 1 on failure
python3 -B -m govharness verify --no-logic governance # structural checks only
python3 -B -m govharness check governance --out-dir <scratch>   # logic report
python3 -B -m govharness verify governance --cache <dir>  # reuse checked solver results
python3 -B -m govharness manifests governance --check # list stale manifests
python3 -B -m govharness manifests governance --write # regenerate manifests
python3 -B -m govharness references governance --check          # References tables
python3 -B -m govharness references governance --write STND.DRAFT   # write one
python3 -B -m govharness ledger append governance --type adopt --actor NAME \
    --role custodians --authority GOV.41 --targets STND.DRAFT --scope STND/DRAFT \
    --rationale "Adoption of STND.DRAFT, revision 1.0, ..."
python3 -B -m govharness sign check governance/ledger.jsonl --ledger-id governance \
    --corpus governance                              # verify signatures
python3 -B -m govharness compose governance --check   # stale copies in rendered/
python3 -B -m govharness compose governance --write   # regenerate rendered/
python3 -B -m govharness compose governance --all ../rendered --check  # every document's copy
python3 -B -m govharness rehearse governance amendment.py  # dry run on a copy
python3 -B -m govharness pairs governance NUMER       # pairs to review before a change (STND.HARN.28)
```

### Amendments

An amendment is a short Python script that applies the primitives of `govharness.workflows.amend` to the root it is given: `replace_text(root, path, [(old, new)])` for each text change (each old text occurs exactly once), `raise_revision(root, "STND/DFLT", "1.5", "1.5.1", row)` for each document whose revision changes, and `record_transaction(root, Change(...))`, which appends the unsigned transaction with the actor and role it is given, then rebuilds the manifests, and returns the entry with the verification that follows. Every refusal of the ledger comes before anything is written, and an entry that the signer register requires to be signed is refused: record it with `ledger append --sign` instead. None of them holds a path of its own. Rehearse the script first with `rehearse`, from this directory so that the script can import the package; run it on the live corpus only after the rehearsal verifies and confirms the source unchanged. After an amendment, run `compose governance --write` so that `rendered/` stays current.

## Reading and applying the corpus without software

Nothing in `govharness/` is needed to read, apply, or audit the governance (GOV.38, INTPR.12); each check is the test its provision states, and a person can perform it with `sha256sum`, `sed`, and `gpg`. Commands below run from `governance/`.

1. Start at `governance/README.md`. An identifier is a path: `GOV.12` is `governance/GOV/12.md`, `STND.DRAFT` is `governance/STND/DRAFT/_doc.md`. The front matter lists the fields; the text below it is normative and governs where the fields disagree.
2. To find what applies, read `LVL0/_doc.md` (Normative Language, the parts and their order in GOV.5), then the provision files, then the lower documents. Each provision below LVL0 lists in `instantiates` the higher provisions it makes more specific.
3. To confirm a file is unchanged, compute its SHA-256 and compare with its row in the `MANIFEST.csv` of its directory; a directory row holds the SHA-256 of the subdirectory's manifest.
4. Chain (STND.HARN.8). Each line of `ledger.jsonl` is one transaction, ending at a line feed only (a text field may hold U+2028, U+2029, or U+0085, which are not line ends here), written with sorted keys, no spaces, and UTF-8 unescaped, so deleting its field `hash` from the text leaves what the hash covers. Line N's `hash` must equal the first output below, and its `prev` the `hash` of line N-1 (`null` for line 1); `seq` must be N:

   ```bash
   sed -n "${N}p" ledger.jsonl | sed 's/"hash":"[0-9a-f]*",//' | tr -d '\n' | sha256sum
   ```

5. Content pin (STND.HARN.9). Each pin in force, a transaction with a `scope` that no later transaction's `scope` reaches whole (each of its paths named, or under a directory named), pins its `corpus_hash`, which must equal the output below, with the scope's paths, directories or `.md` files, listed in place of `$SCOPE` (the term Content hash of STND.HARN lists each file once and orders files part by part; byte order gives the same order for this corpus, whose scopes do not overlap):

   ```bash
   for s in $(printf '%s\n' $SCOPE | LC_ALL=C sort); do
     find "$s" -type f -name '*.md' | LC_ALL=C sort | while read -r f; do
       printf '%s:%s\n' "$f" "$(sha256sum "$f" | cut -c1-64)"; done
   done | head -c -1 | sha256sum
   ```

6. Signatures (STND.HARN.11 to STND.HARN.13). A signature covers the entry digest, the output of step 4 with the second `sed` replaced by `sed 's/"hash":"[0-9a-f]*",//; s/"signature":"[^"]*"/"signature":""/'`. Write that 64-character digest, with no line feed, to a file; write the `signature` value, with each `\n` read as a line feed, to `sig.asc`; import the public keys under the headings of the signer register `SIGNR`; then run `gpg --verify sig.asc digest`. Whether the key may sign that entry is the term Accepted signature of STND.HARN, read against the rows of `SIGNR`. STND.HARN.10 sets what a row names, and `sign add-signer` and `sign close-signer` refuse `--ledger all`, in any case. STND.HARN.7 and STND.HARN.13 state which keys the field `signers` of a register transaction lists. The founding key is the `anchor` fingerprint in `/etc/governance/signer.json`. If that file names a `head`, line `seq` of the ledger must have that `hash`.
7. Configuration. STND.DFLT.22 and STND.DFLT.23 state when a recorded configuration displaces a provision: `show governance STND.DFLT.22`, or `STND/DFLT/22.md`.
8. To change the governance, follow GOV.40 and GOV.41: a change is a ledger transaction by the human owner or the custodians, never an edit alone. By hand, edit a copy, check it as above, copy it back, and append a line with the fields of STND.HARN.7, computing `corpus_hash` and `hash` as in steps 5 and 4.

## What `verify` checks

1. Every file's `id` matches its path.
2. Every top-level directory is a well-formed mnemonic, two to five uppercase letters, or a grade that the register MNEM lists for an ordinal scale, such as `LVL0` (STND.IDENT.17, GOV.37).
3. Every cited identifier or section locator (`cites`, `governed_by`, `instantiates`, `refers_to`) resolves. A locator is a document identifier, a number sign, and a heading slug (`LVL0#normative-language`). A bare LVL0 section name, as the Lexicon's governing column uses, resolves against the LVL0 headings; any other unknown or malformed reference fails.
4. Every manifest is current.
5. The ledger chain is intact (each entry's sequence number is its position, its `prev` is the hash of the entry before it, and its `hash` is its own), and the content each transaction pinned is unchanged. An edit made outside the ledger fails this check (GOV.36). Any transaction may pin a subpath such as `STND/DRAFT`, or a `.md` file such as `README.md` (STND.HARN.7); a pin holds until a later transaction's scope reaches each of its paths (STND.HARN.9, the terms Pin in force and Reach), so a wider scope ends it and a narrower one does not. So `ledger append` and `record_transaction` refuse, before writing, a scope that shares content with a pin in force without reaching each of its paths, naming it: record the change with a scope that reaches the whole pin. Two such scopes, once both pinned, would leave no transaction that records a change of the shared content without staling one of them. A file name with a control character under a scope in force fails, since the content hash joins names with line feeds. A ledger that is missing or empty fails where the corpus holds Markdown. A `review` transaction (QA.7) records an independent review; it is not a revision, so check v.4 ignores it. A scope that names neither a directory nor a `.md` file of the corpus (or leaves it, through `..` or an absolute path) is refused by `ledger append` and reported by this check.

   The signer configuration, `/etc/governance/signer.json`, which only the human owner writes, is trusted over the corpus. Where the running account could alter it, its anchor and head pin are ignored, and `verify` and `sign check` fail and name the file, so that a pin is never dropped without a word. Where it names an `anchor`, a corpus without `SIGNR` fails, so a ledger rewritten without its signatures after `SIGNR` was removed does not pass. So the owner founds `SIGNR` (`sign found`, then its register transaction, signed by the anchor key) and sets `anchor` together, the register first: with either alone `verify` fails, the founding for want of the anchor, or the corpus for want of the register. Where it names a `head`, `{"seq": N, "hash": "<hash of entry N>"}`, a ledger whose entry N is missing or has another hash fails `verify` and `sign check`. Any prefix of an intact chain is itself intact, and only the head pin shows a cut: without one, any entries at the end of the ledger can be removed by an account that can write `ledger.jsonl` and `verify` still passes, a `revoke` or a `register` change among them. With one, the entries up to N are held, and those after N can still be cut. So a revocation is durable only once the owner has pinned the head at or after it. To pin the head, after `verify` passes, take `seq` and `hash` from the last line of `ledger.jsonl`, for example `tail -n 1 governance/ledger.jsonl | python3 -c 'import json,sys; e=json.load(sys.stdin); print(json.dumps({"seq": e["seq"], "hash": e["hash"]}))'`, and set them as `head` in the configuration. Move the pin forward after each transaction that must not be lost.

   The check `unpinned` fails on each Markdown file that no scope of any transaction reaches, naming a directory none of whose files is reached once (`KNOW/ (1 file)`), since STND.HARN.9 compares only the scopes that transactions name (STND.HARN.31). Entries 183 to 187 pin `KNOW`, `TAG`, `_PROJECT`, `STND/_doc.md`, and `README.md`, each with its own scope, so that each changes on its own. A new top-level file or directory needs a transaction whose scope reaches it.

   A crash during an append can leave the last line cut short. Every later append and `verify` then refuse, naming the file and the line. The cut entry was never synced whole, so its append did not return: remove the partial last line, after checking that it does not parse as JSON, and append the transaction again.
6. Every owner field of a project template names a role (STND.IDENT).
7. Every entry carries the status of the `_doc.md` in its directory, and an entry of an adopted or ratified document carries an adoption date, so that adopting a document cannot leave its provisions at draft.
8. Every field `onset` is well formed, sits on a waivable provision below LVL0, and names only sentences of the provision's body and rows that exactly one row of its tables opens with (`onset`; STND.CLASS.10 and STND.DRAFT#representation-in-the-harness). A binding provision, a provision of LVL0, and an item that is not a provision carry none. The value `null` marks a waivable provision that applies at every class, or a permission. While no entry carries the field, a provision without it passes; once one does, each waivable provision below LVL0 without it fails, so that an omitted field is never read as an onset.
9. The logic checks (`check`). Only a `FAIL` fails the run; `WARN` findings, of the structural checks and of the logic checks, are printed. Use `--no-logic` to skip them and `--no-z3` to force the built-in solver.

## What the logic checks cover

Facts are read from the provision text and front matter, never from a hand-kept list. Each structural role (precedence, waiver, non-waivable, and so on) is a configured identifier confirmed against its title, with a title search as fallback, so renumbering does not break the checks.

| Check | Claim established |
| --- | --- |
| 0 | Every structural role resolves to a provision |
| a.1 to a.3 | GOV.5 is a strict total order; every part is ranked or declared unranked; front-matter `rank` agrees with the text |
| b.1 to b.6 | GOV.45's named items exist; `waivable` flags agree with GOV.45; no part is both waivable (GOV.44) and non-waivable; PRIME.15 cites the amendment and waiver procedures; self-grant prohibitions resolve; the amendment and waiver procedures are themselves non-waivable |
| c.1 to c.5 | No sentence puts one action in two incompatible authority tiers; `cites` matches the identifiers in the text of each LVL0 provision; loud failure links to the safe state; back-links from the reserved classes; no standing authorization covers an excluded action |
| d.0 to d.6 | Expressions LVL0 bars are unused (FAIL); SHOULD and prefer are listed; Lexicon definitions carry no capitalized normative word; d.5 lists normative-table words that no provision uses, and d.2 is unused. d.1 reads the table rows of a provision as prose, since the body of a numbered provision, including a table it contains, is normative; a table that the provision names in `defines`, and every table outside a provision, is data and is not scanned. The drafting standard's own expression lists are checked by g.5 and g.6 |
| e.1 to e.4 | Lexicon terms are complete, resolve, and are unique; unused terms are listed |
| l.1 to l.5 | Every provision below LVL0 instantiates something that resolves, reaches LVL0 directly, acyclically, and only upward; stored `rank` and `waivable` agree with the values derived from the ancestors; every LVL2 provision is marked binding or default consistently with its lineage; a prime directive's instantiators are non-waivable. These fail for every provision (PRIME.15, GOV.17, GOV.19) |
| g.1 to g.24 | The drafting standard, below |
| g.25 | Each document below LVL0 holds the References table derived from its citations: the identifiers and locators in its text, its provisions, and their reference fields (STND.DRAFT.34). A document at LVL1 to LVL3 also cites each document its text names by a bare identifier ("HDES", "STND.DOCS"), and the derived table holds its row (the term Cited document of STND.DRAFT); a citation of a withdrawn provision counts for the document that withdrew it. Not read for bare names: LVL0 and entries of no level, the Revision History, every row of a table whose header names a column Example, quoted spans, and code (`../tools/check_refs.py` prints the findings) |
| v.1 to v.8 | Revision numbers and withdrawn identifiers (STND.IDENT): every document carries a well-formed `revision` that agrees with its status; the revision history steps by the class of each change and ends at the `revision` field; the ledger holds one transaction of the right type for each revision; the adopter field of each kind, `ratified_by` for the constitution and `adopted_by` for the others, is present where the document is adopted or ratified, and names a Lexicon role wherever present (STND.IDENT.12); the table of revision classes is present; provisions and checks refer to each other. These fail, except that a date mismatch in v.4 warns. `verify` also checks the owner fields of the project template, which the corpus view leaves out; v.8 fails on a gap in a document's numbering that its field `withdrawn` does not list (for the constitution, a gap in the numbering of each part that the field `withdrawn` of LVL0 does not list; STND.IDENT.24), on a listed identifier in use, and on a numbered identifier that a body or a front-matter field cites, whose first mnemonic the corpus uses, and that is neither an entry nor listed as withdrawn, so that the withdrawal of a document's highest-numbered provision is caught while anything cites it; a body is read as g.25 reads it for bare names |
| v.9 to v.11 | Identifiers and the mnemonic register (STND.IDENT.15 to STND.IDENT.23): v.9 fails on an identifier or locator not in the form for its kind, or a Lexicon slug that differs from its term; v.10 fails on a malformed or duplicated register row and on an inactive or unregistered mnemonic or grade in the identifier of an item that is not retired, and lists for a reader sibling mnemonics at a letter distance of 1 that are not established acronyms; v.11 fails on a transaction with the scope MNEM that is not of type `register` by the custodians |
| unpinned | Fails on each Markdown file, listed by directory, that no scope of any ledger transaction reaches (STND.HARN.31) |
| checked-by | Fails on each key of a field `checked_by` that is neither `review` nor the key of a registered check (STND.HARN.32) |
| m.1, m.2 | Profile combination (STND.HARN.26, STND.HARN.27): m.1 fails on an attribute of the selector table of a profile or sub-profile in force that the document its Defined by column names does not define in its Terms; m.2 fails on a shared matter with more than one owning profile, on a provision that a shared-matters table gives for another profile's matter and that cites no provision of that profile, and on a listed provision that does not exist |
| f.1 to f.8 | The facts and axioms are jointly satisfiable, and each structural claim is proved by refuting its negation, or shown not to be forced |

The fields of a provision below LVL0 that these checks read, `instantiates`, `refers_to`, `rank`, `waivable`, `mode`, `binding_reason`, `defines`, and `checked_by`, and the field `onset` that `verify` checks, are those of STND.DRAFT#representation-in-the-harness. The harness derives `rank` and `waivable` from the LVL0 provisions reached and verifies the stored values (l.3), and the identifiers in a provision's text must equal `instantiates` plus `refers_to` (g.16). The revision classes that the v checks apply are the table of STND.IDENT.3.

The built-in DPLL solver needs no installation. Its unit propagation watches two literals of each clause, so it visits only the clauses that an assignment can make unit or false, and it splits in a fixed order: the first unassigned variable of the first clause not yet satisfied, in the order the clauses are built, false before true. Propagation reaches the same assignment, or a conflict, in whatever order it visits the clauses, so the statuses, models, and cores do not depend on that order. `tests/checks/test_satlib.py` compares the solver with brute force, and with a solver that rescans every clause on each pass, on 3000 seeded random formulas. With it, `verify` of the corpus takes a few seconds. `z3` is used only if it is already importable; both give the same statuses.

The solve cache keeps the result of each solve under a SHA-256 key of everything the result depends on: every clause in order, with its name and its literals in order (the claim enters as the clause of its negation), the backend and z3's version, and a digest of the source of `satlib.py`, `solvecache.py`, and `core/hashing.py`. A change of any of them is a new key and a full solve, so a transaction that leaves the authority-tier statements and LVL0's precedence and waivers as they were reuses every result, across rehearsal copies too. An entry holds the status, the backend, the model as bits, and the core as positions in the clause set, and no corpus text. It is reused only after a check against the clause set, so a planted or damaged entry can change no verdict: a model must satisfy every clause, and a core must be exactly the one the built-in solver's minimization finds, which takes one search per core fact instead of one per fact. A core found by z3 is neither saved nor reused: it cannot be checked to be the one a fresh z3 run would list, and z3 finds it again quickly; a z3 model is reused after the same check as any model. An entry that fails, or a file that is no plain entry (a link, a pipe, too large), is named on the standard error and recomputed; the standard output is the same with a cold cache, a warm one, or none. The cache is opt-in: it lies in `--cache DIR`, else `$GOVHARNESS_CACHE` (which also reaches `rehearse` and amendment scripts), and where neither names a directory there is none, so a read-only command writes nothing anywhere, whatever the home directory holds. A directory inside the corpus, through `..` or a link too, and a relative `GOVHARNESS_CACHE` are refused, by `record_transaction` and `rehearse` before they write anything; a relative `--cache` is taken from the working directory. `verify`, `check`, `rehearse`, and `record_transaction` use the cache; a library call of `verify_corpus` does not unless passed `cache=True`. Deleting it costs only time; a warm cache saves about a second of `verify`.

`tests/checks/test_logic.py` damages an in-memory copy of the corpus in many ways and asserts that the named check fails, so a passing run means the checks can fail. Its class `HeldBehavior` also holds the details of b.3 and c.4, the d checks that only list, and the proofs f.2 to f.8, each shown to fail once the clause that forces it is removed.

### The drafting standard (g family)

The engine reads the tables of STND.DRAFT (modal set, excluded expressions, vague qualifiers, quantifiers, role words, person words, spelling), expands every expression to its inflections, and scans four groups of subjects. The cells of a table in a provision are read as prose, other than the cells of a mention column (the term of STND.DRAFT 1.6), which the harness finds by the headings that STND.DRAFT names: Modal, Normative Language entry, Expression, Read as, Qualifier, Word, British, American, Not used, Used, and Opening words (`MENTION_COLUMNS` in `checks/drafting/tables.py`). A table that a provision names in `defines` is read so too, without its header row, whose headings are data; a quoted span is a mention there as elsewhere (STND.DRAFT.3). A new table whose column is mentioned under another heading adds that heading to the list. The logic checks still read no cell of a defining table (`checks/logic/wording.py`). A sentence ends at terminal punctuation (the term Sentence of STND.DRAFT), so two clauses joined by a semicolon or a colon are one sentence, for g.4 and every other drafting check. g.21 knows the apostrophe written straight or typographic. A finding of class defect is certain by the standard's own words; one of class review is a candidate for a reader.

| Group | Subjects | Result |
| --- | --- | --- |
| self | STND.DRAFT itself | defect fails, review warns |
| lower | other numbered provisions below LVL0 | defect fails when the standard is adopted and a binding provision of it names the check, warns otherwise; review is listed |
| draft | standards not yet divided into numbered provisions | listed in the punch list, never fails |
| lvl0 | LVL0 provisions, to which the standard does not apply | listed as an advisory list for amendment, never fails |

A provision with exactly three modals is a review finding of g.18, so `verify` warns on STND.DRAFT.35, STND.DRAFT.39, and STND.DRAFT.42, whose bundles were reviewed and ratified as never applied apart. `check --out-dir DIR` writes `drafting_punch_list.md` with every listed finding. `tests/checks/test_drafting.py` damages an in-memory copy in many ways and asserts the named check reaches its severity; it also asserts the clean corpus has no failure or warning in the l and g families other than those three. g.23 verifies that every provision names its checks and every check enforces a provision.

## Tests

From this directory, the fast subset runs in about ten seconds:

```bash
python3 -B -m unittest tests.query.test_retrieval tests.cli.test_main tests.test_architecture tests.test_conventions
```

The full suite takes about six minutes:

```bash
python3 -B -m unittest discover -s tests -t .
```

[docs/architecture.md](../docs/architecture.md#tests) describes the layout of `tests/`.

## Not yet built

- Trigger and tag fields are empty, and the knowledge base and tag vocabulary are planned.
- There is no agent context manifest (agent brief) or action-class index.
- `find` and `context` match words, not meanings: "push" finds the items that say "push", not the definition of remote write, and a question in full sentences matches its common words; give the corpus's own terms.
- No signer register is founded, so every `signature` field is blank, and the signature feature is not adopted.
- Authority tiers are classified per sentence by wording. Cross-provision action classes (the same action named in two provisions) are not compared.
- Imperative sentences are found by a verb list, not a parse (g.8, review); a listed verb alone without terminal punctuation, a label in a table cell, is not one.
- Whether a quoted expression is mentioned or used, whether a qualifier has a criterion, and whether a citation names something the provision really makes more specific are left to a reader (`checked_by: review`).

All of these belong to STND.HARN.
