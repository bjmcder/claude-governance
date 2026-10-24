# Review 0001: the package `govharness` after units 0001 and 0002

Independent review (QA.7). Record contents per STND.DFLT.8: revision reviewed, reviewer, findings, and verdict.

| Item | Value |
| --- | --- |
| Revision reviewed | `840f3ca` ("Unit 0002: close with its record"), against the baseline `99d9a78` and the reference code `archive/tools-flat/` |
| Reviewer | Claude (independent review agent); not the author of units 0001 and 0002 |
| Scope | `govharness/`, `tests/`, `tools/`, `README.md`, `records/`; against DSGN, SIMPL, INTPR.1 to INTPR.3, VV.7, REPRO.5, REPRO.7, GOV.35 to GOV.39, and decision 0001 |
| Fixes | Commits `8dc10b2` to the commit of this record, each one kind of change (behavior change, fix of new code, or restructure), by the agent author |
| `governance/` | Unchanged: `git diff --stat 99d9a78 -- governance` prints nothing |

## Method

1. Read the records, the decision, the governance named above, the package, the tests, and the flat code.
2. Ran, old against new, every code path the equivalence harness did not exercise: `sign found`, `add-signer`, `close-signer`, `require`, `check` (governance and work ledger, a replayed ledger identifier, no register), and `ledger append` with `--sign`, a `SIGNR` scope, `--ledger-file`/`--ledger-id`, a wrong ledger identifier, an unknown type, and a missing scope. Output and files agreed (signatures and hashes masked), except the messages of refusals that unit 0002 made deliberate (`refused: ...` instead of a traceback).
3. Probed each listed defect of the flat code and each robustness question with a failing case first, then fixed it with a test that fails on the code before the fix.
4. Reran the full suite, ruff, the live corpus, and the equivalence harness after the fixes.

## Findings

Severity: High, a check that a governance safeguard relies on can be passed by a damaged or forged input; Medium, a stated property of the code or a decision does not hold; Low, a local defect, inconsistency, or excess.

| # | Severity | Finding | Disposition | Commit |
| --- | --- | --- | --- | --- |
| 1 | High | `verify` compared links and hashes but no sequence number with its position, and `sign check` checked no chain. A key window (`Last entry`) and a required signature (`From entry`) compare the `seq` an entry claims, so an unsigned entry renumbered below the entry from which its actor must sign, with its hash rebuilt, passed both: a required-signature bypass, inherited from the flat code. `ledger append` already refused such a chain | Fixed: both use the chain check of `append` (`transactions.entry_problems`, `chain_problems`); tests show the bypass passed before | `5ab680f` |
| 2 | Medium | The architecture test scanned each module's own source only. It missed `import os as o`, relative imports, and effects reached by calling another module: `checks/ledger.py` read pins, scopes, and the register from disk and read the owner's signer configuration, `checks/verification.py` loaded the corpus, and `ledger.signatures.check_signatures` read `/etc` by default. Decision 0001 gives the checks layer no effect, and the unit 0001 audit (criterion 3) recorded that `checks/` reads nothing | Fixed: the checks compute on the snapshot; loading moved to `workflows/verification.py`; the signer configuration is an explicit parameter; the test resolves aliases, refuses relative imports, adds random, network, and execute, and follows calls by name. Calls through values (a check's `run`) are still not followed; the test states this limit | `2767a2d` |
| 3 | Medium | The source-hash assertion of `rehearse` could be evaded: with a relative root, a script that wrote to the source and then changed directory made the second snapshot read another tree (the copy). Added or removed empty directories were not compared. A script without `apply` ended in a traceback | Fixed: paths made absolute before the script runs, directories compared (`core.corpus.tree_digests`), refusals reported; three tests fail before | `4b4eefa`, `0f4f835` |
| 4 | Medium | `ledger append` had no protocol for concurrent appends (DSGN.15): two at once could take the same number and break the chain (eight threads broke it in 3 of 3 runs). A ledger whose last line lacked its newline received the new entry on the same line | Fixed: an exclusive `flock` from reading the chain to syncing the line; a missing final newline is supplied | `26c81c0` |
| 5 | Medium | Defect 1 of unit 0001: b.2 never reported a non-waivable LVL0 provision without a `waivable` field (dead branch) | Fixed; test case "unflagged prime". Live corpus: every one of the 186 LVL0 provisions carries the flag, so b.2 still passes, which is correct | `8dc10b2` |
| 6 | Medium | Defect 2 of unit 0001: g.23 counted as known only keys reported earlier in the run, so a drafting provision citing a v or f key failed, and the verdict depended on the families run | Fixed: `run_checks` gives every registered key (`CheckContext.known_keys`). Live corpus: STND.DRAFT cites g, l, and `review` keys only, all known before, so g.23 still passes, which is correct | `3d742aa` |
| 7 | Low | Defect 3 of unit 0001: `sign check` without a register ended in a traceback | Fixed: one failure line, exit 1 (fails closed) | `d9387e9` |
| 8 | Low | Defect 4 of unit 0001: `verify` on a missing root printed `entries: 0`. The record said the flat code did so; in fact the flat `verify.py` raised `FileNotFoundError`, so the package had already diverged, unrecorded | Fixed: every `ROOT` and `--corpus` must be a directory; else usage error, exit 2 | `c97b070` |
| 9 | Low | Defect 5 of unit 0001: the built-in solver raised the recursion limit for the whole process | Fixed: iterative DPLL in the same search order; `check --no-z3` output byte-identical to the flat code; decision 0001 refinement withdrawn | `803e0d6` |
| 10 | Low | A ledger scope could leave the root (`..`, an absolute path); `ledger append` pinned the hash of files outside the corpus | Fixed: `core.corpus.inside_root`; refused by append and `record_transaction`, reported by `verify` | `cad7495` |
| 11 | Low | `raise_revision` searched for the last numbered row anywhere after the Revision History heading, contrary to the unit 0002 record | Fixed: bounded by the next heading. No live document is affected | `f76b37a` |
| 12 | Low | `compose . --write` inside the corpus wrote `rendered/` into it (`Path(".").parent`) | Fixed: the root is resolved | `fa898c7` |
| 13 | Low | The equivalence harness exercised none of the changed behaviors and no `sign` command, and would not notice an intended change silently undone | Fixed: `sign check` on every input, one input per intended change, and an `INTENDED` table; an intended pair must differ, every other output must agree | `4185c49` |
| 14 | Low | `check_signatures` 63 lines; "## Revision History" defined three times; `ledger/__init__.py` called `register` and `signatures` pure; README named g.1 to g.24 (INTPR.3) | Fixed | `8a5baa2` |
| 15 | Low | Options with no consumer (SIMPL.5): `rehearse(use_z3)`, `record_transaction(use_z3)`, `verify_corpus(signer_config)`; `core.corpus.read_corpus` unused while its body was repeated in the cli; `CheckContext.root` dead after finding 2 | Fixed | `bac5490`, `2767a2d` |
| 16 | Low | Regression introduced by this review: `4b4eefa` used `Path.resolve()` in `workflows/rehearse.py`, a read effect; the architecture test failed at that commit | Fixed in the next commit with `Path.absolute()` | `0f4f835` |
| 17 | Low | `governance/README.md` says the tools in `../tools/` regenerate manifests (defect 8 of unit 0001) | Open: a corpus amendment; `governance/` is out of scope for this review and unchanged | none |
| 18 | Low | `rehearse` runs the script in process with the user's rights: it detects a change to the source tree after the fact but cannot prevent a write elsewhere, or a script that patches the package in memory | Open, as the unit 0002 record states; a subprocess with a separate working directory would narrow it | none |
| 19 | Low | The equivalence harness compares standard output, exit codes, and files, not standard error; refusal and usage messages are not compared | Open; the probe of method step 2 covered them once | none |
| 20 | Info | When the verifier runs as root, as in this environment, `unalterable` is always false, so no signer configuration is trusted and every register fails its founding check. This fails closed and matches the flat code; the anchor path was exercised only through an injected `SignerConfig` in the tests | Noted for the deployment: run `verify` as an account that cannot write `/etc/governance/signer.json` | none |

Checked and found sound: the signature path matches the flat code line for line (anchor only from an unalterable file and binary, `gpg` at a fixed path with `PATH=/usr/bin:/bin` and `LC_ALL=C` against a throwaway keyring of the registered keys, the ledger identifier in the digest of a work-ledger entry against replay, NFKC and case folding against look-alike actors, `REVKEYSIG`, `KEYREVOKED`, `EXPKEYSIG` and the others rejected, exactly one good and valid signature); the layer imports; ruff; annotations and NumPy docstrings; the labeling of the one regression-guard test and of the harness (VV.7); names of at most three words; `tools/` shims.

## Results after the fixes

| Check | Result |
| --- | --- |
| Tests: `TMPDIR=<scratch> python3 -B -m unittest discover -s tests -t .` | 61 tests, OK (44 before the review) |
| `ruff check --select E,F,W,I,UP --line-length 79 govharness tests tools` | All checks passed |
| `python3 -B -m govharness verify governance` (and `--no-z3`) | `entries: 492`; ids, mnemonics, references, manifests, ledger, templates, status, logic: PASS; exit 0; no warning |
| `manifests --check`, `references --check`, `compose --check` on `governance` | stale: 0; references: PASS; stale: 0 |
| Equivalence harness, `--work <scratch>/eq-final` | 209 outputs; 33 differ, all listed in `INTENDED` (findings 1, 5, 6, 7, 8); 0 not intended; every intended pair seen. The 135 outputs of the original eleven inputs and four commands are identical to the flat code, and `sign check` agrees on the signature-forged input |

## Verdict

Accepted, with findings 17 to 19 open and recorded. After the fixes, every check of the live corpus passes as before, the package keeps decision 0001 as amended in its section "Adjustments made by review 0001", and each change of behavior is tested and shown by the equivalence harness. Finding 1 should be weighed by the custodians: the governance ledger has no signer register yet, so no entry relied on the bypassed rule, but any work done with an earlier `verify` on a ledger with a register should be rechecked.
