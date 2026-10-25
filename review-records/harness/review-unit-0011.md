# Review of unit 0011 (solve cache), commit 26886e3

Verdict: the claims hold. One defect (M1), one unverifiable path (M2), some test gaps. Nothing I tried changed a verdict or an output byte. Scratch: /tmp/claude-1000/review-0011/.

## Checked

1. **Key.** SHA-256 of `[tag, format, version, backend]` plus one canonical-JSON line per clause, in order. JSON escapes line feeds, so lines delimit clauses. I found no way for different ordered sets, claims (the `NEG[...]` clause), backends, or z3 versions to share a key. The full 64 digits name the file. `proofs.py` and `facts.py` can change a result only through the clause set or claim, both keyed; what they do with a result is not cached.
2. **Integrity.**
   - Fuzz: 3000 random sets, 20 planted entries each. 6406 were accepted, all equal to a fresh solve in status, core, and positions.
   - On the real corpus via `check --out-dir`: all 8 entries flipped SAT/UNSAT: 8 refused. A core with a fact removed: refused. Truncated: refused. A named pipe, a link to /etc/passwd, a 5 MB file: skipped. In every case stdout and the three output files were identical, and the entries healed on the next run.
   - Four concurrent cold processes: identical output, no stderr, 8 entries, no temporary files left.
   - Residual: a different valid SAT model is accepted, but nothing reads `.model` outside `satlib` and `solvecache` (grep), so no output can change. A planted z3 core that refutes but differs could change listed core facts, never a verdict.
3. **Purity.** No file, `os`, environment, or process call under `govharness/checks` (grep). The architecture test passes. A cache directory inside the corpus is refused (exit 2) for a direct path, `..`, a symlink to the corpus, a symlink as the cache directory, and the environment variable. A shard directory replaced by a link into the corpus was not followed; `diff -r` showed the corpus unchanged.
4. **Measurements** (`verify governance`, median of 3, my cache):

   | Case | Runs | Median |
   | --- | --- | --- |
   | none | 3.12, 3.44, 2.99 s | 3.12 s |
   | cold | 3.06, 2.99, 3.02 s | 3.02 s |
   | warm | 1.95, 2.10, 1.91 s | 1.95 s |

   Output was identical 9 of 9 times, and equal to the parent commit (SHA-256 `330541e4...`). `check --out-dir` files match across none, warm, and parent, apart from the corpus path I passed. The record's figures agree.
5. **Tests.** Full suite: 233 OK in 198 s. Mutations of the two new test files:
   - exact-core search removed: 5 fail;
   - `satisfies` always true: 3 fail;
   - backend dropped from the key: 1 fails;
   - literals sorted in the key: 1 fails;
   - rename skipped: 6 fail;
   - `inside()` without `resolve()`: **all pass** (T1).
6. **Record and README.** Both agree with the code: key, entry format, options, exit code, test counts (13 and 10), entry sizes (154 to 1,456 bytes), and timings.

## Findings

### Medium

**M1. Defect: the ledger entry is appended before the cache check can fail.** `workflows/amend.py:259` runs `verify_corpus(root)` after `append(...)`. It raises `ValueError` when the cache directory lies inside the corpus (`workflows/verification.py:117`, `78`). Reproduced on a copy: with `GOVHARNESS_CACHE_DIR=<corpus>/qq`, `record_transaction` raised and the ledger went from 147 to 148 lines, with no `Recorded` returned. The docstring's `Raises` does not list this. `rehearse.py:164` is exposed the same way when a script records a transaction. Fix: call `usable_store` at the start of `record_transaction` and `rehearse`, before any write. Or treat an environment-named directory inside the corpus as cache off, with a warning.

**M2. The z3 path is unexecuted.** z3 is not installed here, so the new core-position parsing in `solve_z3` and the soundness-only core check never ran. The record admits this. Fix: run these tests once where z3 exists, or reuse only built-in results.

### Low

- **T1 (test gap).** No test uses a symlink or `..` cache path (`tests/workflows/test_solve_store.py:276-295`). Add both.
- **L1.** `SOURCES` (`solve_store.py:52`) omits `core/hashing.py`, whose `canonical_json` builds every key. Not exploitable, since a changed encoder only changes keys, but add it.
- **L2.** Non-regular, linked, or oversized entries are skipped silently (`_read_entry`), unlike refused ones, which are named on stderr. Harmless; they are replaced on save.
- **L3 (preference).** `verify_corpus` defaults to `cache=True` (`verification.py:90`), so library callers write to the user's cache without asking. A relative `GOVHARNESS_CACHE_DIR` follows the working directory at open time. There is no hit-count output and no eviction (the record notes the latter).
- **L4.** No `fsync`: a crash can leave an empty entry. It is refused and recomputed (tested).

## Could not check

- Anything with z3.
- Non-Linux systems (`supported()` turns the cache off without `dir_fd`).
- Rename atomicity on network filesystems.
- A link swapped in between the `inside()` check and a later write. The shard directories are opened with `O_NOFOLLOW`, but I did not race it.
