# Independent review of unit 0016 (ledger fixes of QA.8 part B)

Reviewer: independent, under the QA.8 brief. Code: commits bc65b95 and ae7a8f5, worktree `agent-a9306c12d9a1ac6ec`. Probes, a scratch keyring, and mutated copies are under `/tmp/claude-1000/review-0016/`. Nothing but this report was written; `~/.gnupg` was not touched.

**Verdict: accept with two Medium findings (M-A, M-B), both small. No High.** Every High and Medium finding of the part B report is closed or handled as ruled.

## What I ran

- The listed tests: `tests.ledger.test_chain`, `test_signatures`, `tests.workflows.test_amend`, `test_rehearse`, `tests.cli.test_main`, `tests.checks.test_ledger`, `tests.derive.test_environment`, `test_authorizations`. 108 tests, OK (28 s).
- `verify governance` on the live corpus: every check PASS, logic PASS, the one g.18 warning as before. `governance/` is unchanged, and so are the hashes of all 175 entries (each re-hashes to its recorded hash). The latest pin of every scope tuple matches, which is what `verify` compares.
- Closing-round rehearsal: a scratch git worktree of 6943e9a with the unit's `govharness/` copied over its own. `rehearse governance ../tools/amendment-scripts/apply_round_2026_10_25_close.py` applied seq 148 to 175 (28 transactions), every check PASS, "source unchanged". The scratch worktree is removed (`git worktree remove`).
- 30 mutations of the fixes, one process at a time on a copy (`mut/run.py`, `mut/out.txt`). 27 killed, 3 survived (below).

## 1. The findings

| Finding | Status |
| --- | --- |
| H1 | Closed. Appended ` `, ` `, `\x85`, `\x0b`, `\x0c`, `\x1c` to `\x1e`, `\r`, `\n`, BOM, and zero-width space in a rationale; all 12 append, read back, and `ledger_problems` is `[]`. The JSON writer escapes every other control character, so only the three that `ensure_ascii=False` leaves raw mattered. No other reader of `ledger.jsonl` uses `splitlines`. A torn line names file and line. |
| H2 | Closed. With an anchor: `SIGNR` removed gives the new line; a chain rebuilt without its register entries plus a skeleton or empty `SIGNR/_doc.md` gives "SIGNR is not founded by a transaction"; `_doc.md` removed gives the new line. |
| H3 | Closed as far as the design reaches. 17 head values probed: `None` passes; float, string, list, `{}`, `0`, `False`, `true`, `0`, `-1`, a non-string hash, and an upper-case hash fail; seq past the end says "entries were cut"; a wrong hash says "rewritten". Empty and blank-only ledgers fail where the tree holds Markdown. `sign check` with the ledger file removed exits 1 with a failure line. |
| M1 | Handled as ruled. `_valid_for` is unchanged and the helpers refuse the row that seemed to close an `all` key. The refusals are all killed by `test_no_row_beside_an_all_row`. |
| M2 | Closed. With a bogus type, with a control-character file name in scope, and with no `ledger.jsonl`, `record_transaction` raises with `tree_digests` equal before and after (and no file created). |
| M3 | Closed for the required-signature and register-problems cases; see M-A for the sibling case that is not. |
| M4 | Handled as ruled; see M-B for a test gap. |
| M5 | Closed. `scope_hash` refuses a Cc character in an included name; `record_transaction` raises with the tree unchanged; the ledger check turns it into a failure line. |
| M6 | Tests added; two mutations still survive (M-B, M-C). |

## 2. Bypasses of the fixes

### Medium

**M-A. An unsigned register change is still accepted by `append`, and then the ledger fails `verify` for good.** `ledger/chain.py` `_refusals` refuses an unsigned entry only where a `Required` row covers the actor, and a register that has problems. The signature check also demands that "every change to the register after its founding is signed" (`signatures.py`, `_register_change`), and `append` does not look at that.
Repro (`p/m3.py`): `signed_corpus`, then `add_signer` for a second key, then `append(root, register_entry(root, "SIGNR"))` with no signer. It returns an entry, and `ledger_problems` is `seq 178: changes SIGNR without the signature of a signer listed before the change`. The entry is immutable, so no later transaction repairs it.
This is the case the original M3 and the lead's brief name ("register transactions"): the unit's own reason for the M3 refusal (an entry that would fail `verify` for good) applies. Workaround: none after the fact; before, use `--sign`.
Fix: in `_refusals`, when `ledger == GOVERNANCE`, `unsigned`, a register exists, and `SIGNR` is in the scope with a register change (any scope of `SIGNR` after the founding), refuse naming `ledger append --sign`. The README line on `ledger append` should list it.

**M-B. Two untested behaviors that the record claims.**
- `chain.py` `_shared_pins`: mutating `covers(a, b) or covers(b, a)` to `covers(b, a)` survives all of `tests.checks.test_ledger`. The record says a scope is refused when a path of one lies "above or below" a path of the other. `test_narrower_scope_after_wider` uses a tuple that shares a path (`STND/DFLT`) with the older one, so the direction never matters. Untested: an old `["HW"]` and a new `["HW/CPU"]` (I ran it: refused, correctly) and the reverse. Add both, with the tree compared.
- `cli/records.py` `_check_signatures`: replacing `read_ledger(args.corpus)` with `read_ledger_file(args.corpus / LEDGER_FILE)` survives `tests.ledger.test_signatures` and `tests.cli.test_main`. The record says a corpus with a register and no ledger file is "a failure line, not a `FileNotFoundError`". It does behave so now (exit 1, `SIGNR is not founded by a transaction`), but nothing holds it. Add a test of `sign check` with the file removed.

### Low

- **L-a. M5, third mutation.** Replacing `unicodedata.category(c) == "Cc"` by `c == "\n"` survives. It is still sound (only the line feed makes the encoding ambiguous), so the Cc rule is stricter than needed; the test uses a line feed only. Either test a second control character or say in the record that Cc is wider than the need.
- **L-b. A head pin in an alterable file vanishes silently.** `read_config` gives `SignerConfig()` and nothing says the pin was dropped. An anchor in the same file fails closed (the founding check fails) but a pin does not. The README says the file "is ignored where the running account could alter it"; a one-line `verify` note would make it visible. Not required.
- **L-c. `scope_hash` now raises in `authorizations.py:446`** (the `environment` path) for a control-character name in an authorization's scope, where it used to return a mismatched hash. `cli/environment.py` catches `ValueError`, so I expect a refusal and not a traceback; I did not run it.
- **L-d. README: the order for the owner.** The record's Open says "an owner who sets `anchor` before founding `SIGNR` sees `verify` fail until the register is founded". The README says "a corpus without `SIGNR` fails" but does not tell the owner to found the register first, and does not say that the pin must be moved forward by hand after each transaction that matters beyond the one command it gives. The second is there ("Move the pin forward…"); the first is only in the record. Add one sentence to the README.

### Checked, found sound

- **H3 head pin.** A cut at seq N with the tail after N removed passes by design and the README says so ("those after N can still be cut"). A tail cut below N, a rewrite of N with its links rebuilt, a malformed pin, and a pin in an alterable file (ignored, L-b) were each tried or read in `head_problems` and `read_config`.
- **H1.** A line that round-trips but splits elsewhere cannot occur: `append` checks `parse_ledger(line) == [written]`, and `parse_ledger` splits on `"\n"`, which `canonical_json` never emits raw.
- **M3 paths.** `ledger append`, `record_transaction`, and a work ledger all go through `chain.append`; the `unsigned` flag is `signer is None`.
- **M4 against the live ledger.** Scopes tried against the live pins: `["HW"]` again (passes), `["HW","HDES"]`, `["HW/CPU"]`, `["HW/"]`, `["HW","HW"]`, `["./HW"]`, `["STND"]`, `["GOV"]` (refused: the older pin is the 13-directory tuple of entry 46, so a change to GOV must be recorded with that tuple, as before), `["MNEM","STND/NEWX"]` (refused: MNEM has its own pin at 144, so adoption plus its MNEM row is two transactions, as the ledger already does). The 13-directory tuple in another order passes. The refusals are conservative but each is recoverable by recording with the tuple that pins the content. A change that spans two tuples leaves `verify` failing between its two transactions and passing after the second; this is the rehearsed round's pattern. I found no valid sequence of single-tuple transactions that leaves the corpus failing `verify`.
- **What M4 cannot do for the live corpus.** It cannot restructure scopes (merge `["HW"]` and `["HDES"]` into one tuple, or split a family) until STND.HARN.9 is amended; the unit's Open section says so, and it is the ruling.
- **M2.** The refusal list of `append` all comes before the manifest write; `usable_store` writes nothing in the corpus.
- **M5 routes.** `record_transaction`, `ledger append` (`records.py:135` computes the hash before `append`), and the ledger check all see the `ValueError`.

## 3. Compatibility

- `verify governance` PASS on the live corpus; the ledger file is unchanged and all hashes re-verify; `scope_hash` encoding is unchanged.
- The closing round's 28 transactions apply and verify against 6943e9a with the unit's harness (above). Its scopes are the family scopes (`HW`, `HDES`, `STND/*`) and each repeats the tuple that pins its content.

## 4. Tests

Surviving mutations (the brief's Medium for a test that does not hold a claim): the two of M-B, and the Cc one (L-a). The other 27 are killed, among them every H1, H2, H3, M1, M3, M5, L1, L2, L5, and `isascii` mutation, and the `read_config` head mutation. The author's own list of 21 matches what I tried; I added the `covers` direction, `scope_key` sorting, the `seq < 1`, bool, and hash-type parts of the pin, and the `sign check` reader.

## 5. Documentation

The record, README, and docstrings agree with the code, with these exceptions: the README `ledger append` row does not list the unsigned register change (M-A, once fixed), and the owner's order (found `SIGNR`, then set `anchor`; move `head` after each transaction that matters) is stated in the record's Open section and only partly in the README (L-d). Both say plainly that without a head pin a cut tail passes, and that the pin is the human owner's to set in `/etc/governance/signer.json`; no configuration was created.
