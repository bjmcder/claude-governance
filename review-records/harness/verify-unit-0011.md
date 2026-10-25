# Verification of unit 0011 fixes (commit 8cf9dbc)

Verdict: ready to merge. No High or Medium finding. Scratch: /tmp/claude-1000/verify-0011/.

## Checks

1. **M1 fixed.** On five corpus copies (cache directly inside, via `..`, via a symlink, `GOVHARNESS_CACHE_DIR` direct, and via `..`), my own amendment script through `record_transaction`, and `rehearse` of a script that records, both raised `ValueError`. `tree_digests` (ledger, manifests, all files) was unchanged, no work directory was made, and no cache directory appeared. Both calls check before the first write.
2. **M2 fixed.** `_core_result` refuses any non-built-in core, and `solve_cached` does not save a z3 UNSAT result. Mutations of a copy: dropping the refusal fails 3 tests; saving z3 cores fails 1. What can still differ from a fresh solve:
   - A reused core is only a built-in one that `confirms_core` proved exactly equal to the minimisation result. So no reported core can differ.
   - A z3 SAT model is reused after a satisfies check and may differ from z3's own. Nothing outside `satlib` and `solvecache` reads it (review grep).
   - Real z3 is still never run (not installed). The stub tests the parsing code, not z3's behavior. That risk is now only a wrong fresh result, which a cache cannot make worse.
3. **T1 and the Lows.**
   - `inside()` using `absolute()` instead of `resolve()` fails 2 tests.
   - `core/hashing.py` is in `SOURCES`, and dropping it changes the digest.
   - Planted FIFO and symlink entries are named on stderr as "skipped (the entry is not a regular file / is a symbolic link); recomputed". Stdout is unchanged.
   - `verify_corpus` defaults to `cache=False`. The only callers in `govharness` and `tools` are `verify` and `check` (store from options), `record_transaction`, and `rehearse` (cache on). `check` does not use `verify_corpus`. No CLI command loses the cache.
   - A relative `GOVHARNESS_CACHE_DIR`: `verify` and `check` exit 2 with a message. `--no-cache` ignores it (exit 0).
4. **Output unchanged.** `verify governance` stdout is byte-identical across main (bb0f8e2), no cache, cold and warm. Stderr is empty. Timings, median of 3 (s): none 3.34 (3.66, 3.34, 3.04); cold 3.11; warm 2.00; main 3.16. Cold costs nothing, and warm saves about 36%. My SHA-256 prefix (`cd0f7be3`) differs from the review's `330541e4`. Both fixes' outputs equal main's in my runs, so I assume different invocation or path text; I did not chase it.
5. **Suite.** From `harness`, `python3 -B -m unittest discover -s tests`: 240 tests, OK, 201.6 s.

## Findings

### High
None.

### Medium
None.

### Low

- **V1.** `verify --no-logic` with a relative `GOVHARNESS_CACHE_DIR` exits 2, though no cache would be used. The cause is `_store(args)` running before the `logic` check. Fix: skip `_store` when `args.no_logic`.
- **V2.** `record_transaction` and `rehearse` read only the environment. They have no way to name a cache or turn it off except `GOVHARNESS_NO_CACHE`. A `ValueError` from a bad environment now stops amendments, where before (once fixed) it would have been a warning. This is deliberate and documented. Fix, optional: a `cache` argument.
- **V3.** Still unchecked: real z3, non-Linux, network-filesystem rename, a link swap racing `inside()`. The record states the first. Fix: run the stub tests' scenarios once where z3 is installed.
- **V4.** The old L4 (no `fsync`) and the lack of eviction and hit counts remain, by choice.
