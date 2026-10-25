# QA.8 review, part B: ledger, core, cli, workflows, derive, query

Reviewer B. Code at main as copied on 2026-10-25; all probes ran on copies under `/tmp/claude-1000/qa8-b/` (helper `scripts/signed.py` builds a signed ledger with a throwaway keyring). Nothing under the repository was written except this report. The part-B tests (`tests.ledger.*`, `tests.workflows.*`, `tests.query.test_retrieval`, `tests.cli.test_main`, `tests.derive.test_reading_copy`) pass: 56 tests, OK.

Result: 3 High, 6 Medium, 8 Low.

## High

**H1. A ledger entry whose text holds U+2028, U+2029 or U+0085 bricks the ledger.**
`ledger/transactions.py:54` parses with `text.splitlines()`, but `core/hashing.py:canonical_json` writes with `ensure_ascii=False`, so these three characters go into the file raw and split the entry's line on the next read.
Repro: `ledger append g --type annotate --actor X --role r --rationale $'a b'` succeeds (entry 176). The next `ledger append` and `verify` both exit nonzero with `refused: Unterminated string starting at ...`. The chain cannot be repaired by editing, since editing the line changes its hash.
`record_transaction` hits the same wall: the append succeeds, then its own `verify_corpus` raises.
Fix: `[json.loads(l) for l in text.split("\n") if l.strip()]`. Also have `append` refuse, or escape, a line that does not round-trip through `parse_ledger`. Add a test with each of the three characters.

**H2. `verify` passes a ledger rewritten without signatures once `SIGNR` is removed, even when the owner's signer configuration names an anchor.**
`checks/ledger.py:72-78` reads the register only if the file exists; `ledger/signatures.py:338-342` then returns `[]` for `register is None` unless some entry is signed. `SignerConfig.anchor` is not consulted. Unit 0010 closed this for `environment` (`register_trace`), not for `verify`.
Repro (`scripts/signed.py`): found `SIGNR`, sign two register entries with the anchor key, `rm -r SIGNR`, rebuild the whole chain with the signatures and the register entries dropped plus a forged unsigned entry. `ledger_problems(tree, ledger, SignerConfig(anchor=fpr))` returns `[]`.
Fix: in `ledger_problems`, when `config.anchor` is set and the tree has no `SIGNR/_doc.md`, report "the signer configuration names an anchor but the corpus holds no SIGNR". The config lives where the agent cannot write, so this is the right place for the trust.

**H3. Nothing pins the head of the ledger, so the tail can be cut and `verify` passes.**
Any prefix of a valid chain is a valid chain. The pins in `checks/ledger.py` only bite when a cut entry changed content under a scope. Entries with an empty scope (`authorize`, `revoke`, `rule`, `review`, `annotate`) can be dropped from the end, signed or not.
Repro: signed `register`, `authorize`, `revoke` (scope `[]`); delete the last line; `ledger_problems` returns `[]`, 177 entries. `environment --authorization` then finds the authorization un-revoked. Check v.4 catches a cut `adopt` or `amend` (it needs the logic run), not these types.
Fix: record the head `(seq, hash)` where the agent cannot write (the signer configuration, or a file `read_config` already guards) and have `verify` and `sign check` compare it. Without that, document that a revocation is only as durable as the agent's inability to write `ledger.jsonl`.
Related and smaller: a missing or empty `ledger.jsonl` gives `ledger: PASS` (`chain.py:89-90`; `verify --no-logic` on a copy with the file removed passes every structural check). A corpus whose pins are expected should fail with no ledger.

## Medium

**M1. A closed key stays valid through an `all` row.**
`ledger/signatures.py:279-288` accepts a key if any row applies. `ledger/register.py:116-125` forbids closing an `all` row and the module docstring says to "close" it by adding a closed row per ledger. The open `all` row still matches.
Repro: rows `all|R|K|none` and `governance|R|K|5`; `_valid_for(reg, K, {"actor":"R","seq":10}, "governance")` is True. A compromised `all` key cannot be retired, and a signature past the window passes `verify`.
Fix: a ledger-specific row for the same fingerprint and role overrides the `all` row for that ledger (use the narrowest match), or refuse `all` signer rows.
Test gap: nothing tests "Last entry" at all (M6).

**M2. `record_transaction` writes the manifests before anything can refuse the entry.**
`workflows/amend.py:245-248` rewrites the stale manifests, then calls `append`, which raises for an unknown type, a broken chain, another ledger's entries, or a bad JSON line.
Repro: after an edit to `STND/DFLT/1.md`, `Change("bogus-type", ...)` raises `ValueError` and three `MANIFEST.csv` files have changed. The docstring and README claim "checked before anything is written" for the scope and cache only, but the user reads that as all failures.
Fix: validate the type, and read and chain-check the ledger, before writing the manifests; or write the manifests after the append. `tests/workflows/test_amend.py` has only the missing-scope case; add one with a bad type and a broken chain that compares the whole tree.

**M3. `record_transaction` appends an unsigned entry where the register requires a signature, and the corpus never verifies again.**
`workflows/amend.py:248-263` has no look at `SIGNR`. Repro (signed register requiring `The Custodian` from 177): the append succeeds; `verification.sections()["ledger"]` is `seq 178: The Custodian must sign from entry 177`; a later signed entry does not repair it, since the entry is immutable.
Fix: before appending, run `check_signatures` on the ledger plus the new entry and refuse, naming `ledger append --sign`. The same applies to a register transaction with `SIGNR` in scope when the register has problems (`ledger/chain.py:198-200` ignores `register.problems`).

**M4. A pin goes stale when a later transaction of a different scope covers the same directory.**
`checks/ledger.py:67-71` keys the latest pin by the whole scope tuple. Valid transaction `scope=["STND/DFLT","STND/PY"]` after an earlier one with `["STND/DFLT"]`: `record_transaction` ends with `content changed outside the ledger since seq 159: STND/DFLT`. The fix is another transaction with the old tuple, but the corpus fails `verify` until then. The converse (a narrower scope after a wider one) fails the same way.
Fix: keep the latest pin per directory (or per file), not per tuple; or make `append` refuse a scope that would stale an older pin.

**M5. `scope_hash` is ambiguous between files.**
`core/corpus.py:366-374` joins `path:digest` lines with `\n` and does not escape file names. A file named `D/a.md:<sha of a>\nD/b.md` with b's content gives the same hash as `D/a.md` plus `D/b.md` (checked, True). In a full corpus the `ids` check flags the stray name, so `verify` fails on other grounds; the pin by itself no longer distinguishes the trees. A target in a README or template directory (which `ids` skips) would not be flagged.
Fix: hash `canonical_json` of the sorted `[path, digest]` pairs, or refuse file names with control characters.

**M6. Tests do not hold the signature rules they name.** Surviving mutations, each on a copy:
- Deleting the key-window clause from `_valid_for` (`signatures.py:283-286`): `tests.ledger.test_signatures` passes. No test uses `close_signer`, "Last entry", or an `all` row.
- Dropping `not actor.isascii()` (`signatures.py:394`): passes. The only look-alike case is a trailing space, which `_spoofed` catches.
- Removing the `unalterable` gate from `gpg.read_config`, the rule that an anchor from a file the account can alter is ignored: `tests.ledger.*`, `tests.derive.test_environment`, `tests.cli.test_main`, `tests.workflows.test_amend`, `tests.workflows.test_rehearse` pass (46 tests). Every caller patches `read_config`.
- No test covers H2, H3, or the ledger-less corpus.

## Low

- **L1.** `ledger_problems` indexes `entry["corpus_hash"]` and `entry["seq"]` (`checks/ledger.py:69-70`); an entry with a scope and no `corpus_hash` ends in a `KeyError` traceback instead of a failure line.
- **L2.** `verify` maps every `ValueError` to `refused: ...`, exit 2, the code documented for a cache refusal (`cli/reports.py:159`). A front-matter error names no file (`core/entry.py:503-509`, `core/corpus.py:136`): `GOV/36.md` without front matter prints only `refused: missing front matter`. A bad ledger line is the same.
- **L3.** Not pinned by any scope: `STND/_doc.md`, `TAG/`, `KNOW/` (`planned`, non-governing). An edit there followed by `manifests --write` (or any `record_transaction`) gives `verify` PASS, as checked on a copy.
- **L4.** The hash covers the parsed entry, not its bytes: whitespace, key order, and a duplicate earlier key (last wins in `json.loads`) can change in the file with `verify` unchanged. `NaN` is accepted. A tool that reads the first duplicate sees something else.
- **L5.** `append` opens `a+`, so a mistyped `--ledger-file` creates an empty file; a torn last line (a crash during the write) makes every later append and `verify` refuse until it is cut by hand (`chain.py:132-138`). The refusal is safe, but the recovery is not described.
- **L6.** `Corpus` text goes through `decode` (CRLF to LF) in `manifests --check` and `compose --check`, so a CRLF file counts as fresh while the bytes differ (`derive/manifests.py:stale_manifests`, `cli/derived.py:127`).
- **L7.** Corpus writes are `write_text` (truncate then write) and are not atomic: `replace_text`, `raise_revision`, `write_files`, the manifest rewrite. `raise_revision` counts `revision: "x"` over the whole file, so a quoted example in the body can be edited in place of the front matter. `rehearse` runs `shutil.copytree` outside its `try` (`rehearse.py:428`), so a `work` directory inside the root (library use only) modifies the source and is not reported. `tree_digests` ignores modes and symbolic-link targets.
- **L8.** `register.with_signer` and `close_signer` splice `role` and `name` into a table row without refusing `|` or a newline; owner-run only. A key that expires or is revoked makes every earlier signature fail (`EXPKEYSIG`, `REVKEYSIG`), not only those past a window.

## Checked and found sound

- **Signatures against forgery.** `gpg --verify` of a clearsigned or inline-signed message by a registered key is not accepted for another digest (tried both). A wrong digest, an intruder key, a signature moved to another entry or ledger, and an actor out of window or with a non-ASCII label all fail; the digest covers `seq`, `prev`, `signers`, and `ledger`. `parse_status` needs exactly one `GOODSIG` and one `VALIDSIG` and no rejected status. A key block under the wrong heading is a register problem. A register change must be signed by a key listed before it, and the founding by the anchor.
- **Chain.** The checks for seq equals position, `prev`, and hash hold; a renumbered entry fails. `flock` is held from the read to the `fsync`.
- **Solve store.** Entries are opened relative to a `O_NOFOLLOW` directory with `O_NONBLOCK`; non-regular, oversized, and linked entries are skipped and named; a model must satisfy every clause and a core must be confirmed before reuse; the key holds the solver source digest. `usable_store` refuses a store inside the corpus (symbolic links followed) and a relative directory, before `record_transaction` and `rehearse` write. Left to part C: the soundness of `confirms_core` and `satisfies`.
- **`rehearse`.** The source is compared in a `finally` by content digest, an absolute root survives `chdir`, and a script's own exception is replaced by `SourceChanged` when it wrote to the source (reported, not prevented, as documented).
- **Expiry horizon.** `parse_horizon` accepts only 1 to 9 ASCII digits or `none`; the horizon is compared by difference, so no overflow; a zero is refused. Default 90 days applies to `until-revoked`.
- **Unit 0010 trace.** `authorized` reads the shape, the signatures, the `SIGNR` scopes, and the anchor before it trusts `--accept-unsigned`; the assured case with no register still needs a signature. The residual (a whole-ledger rewrite without an anchor) is as documented; H2 is the anchored case the unit left to `environment` only.
- **Retrieval and combination.** `find`, `context`, `show`, `review_pairs`, and the graph build were read; unresolved references are dropped by the graph; no defect found. `query/combination.py` has no part-B test of its own.
