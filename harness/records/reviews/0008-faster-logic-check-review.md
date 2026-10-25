# Review 0008: unit 0009, watched-literal built-in solver

Independent review of `bf53dcf` (branch `worktree-agent-ab815c1af2a24f0c1`; parent is main). Reviewer: Claude (independent review agent), not the author. Reviews live in `harness/records/reviews/`; this is the next number.

## Verdict

The code is correct and behavior-identical as far as I could test. The tests are weaker than the record says: two real bugs in the watch scheme survive them. One defect (tests), no defect in `satlib.py`.

## Method and measurements

- Read the diff, the record, the README paragraph, `proofs.py` callers (`solve`, `prove_entailed`).
- Own fuzz (`/tmp/claude-1000/review-0009/fuzz.py`, seed 20261024): 40,000 clause sets, half up to 60 clauses over up to 30 variables, clauses of 0 to 9 literals, 30% repeat chance per literal, complements, 1% empty, 15% unit. Old `satlib.py` from `HEAD~1` against new, comparing status, model with key order, core, backend. 17,330 satisfiable. 0 differences.
- `verify governance`, old tree (git archive of parent) against new, 3 runs each, no z3 installed: old 11.97, 12.35, 11.82 s (median 11.97); new 3.20, 3.10, 2.97 s (median 3.10). Output byte-identical in all 3 pairs (191 bytes including exit code). The record's 11.31 and 2.88 s agree within machine noise; the README's "about 3 s where about 11 s" holds.
- Full suite, `python3 -B -m unittest discover -s tests`: 197 tests OK, 129.6 s (record: 138.6 s). Architecture and convention tests are in it. Ruff 0.16.10 at 79 columns, check and format: clean.

## Correctness of the scheme (no defect found)

Traced by hand and confirmed by the fuzz:
- Length 0 and 1 are settled in `roots` and never watched; a contradiction among them returns None before search.
- Repeated literal: `[a,a,b]` watches `a` twice; when `a` falls the clause is visited twice, the first visit moves one watch to `b`, the second finds `b` unassigned and assigns it. `[a,a]` conflicts only on a false `a`. A repeat in a non-watched position behaves as the old count-per-occurrence rule.
- Tautology: watches `a` and `not a`; one is always true or unassigned.
- Backtracking: `undo` resets `head`; unprocessed trail entries are discarded and processed ones moved watches only to non-false literals, so no watch undo is needed. The early-return on conflict keeps the unvisited tail (line 283).
- `first_open` start is valid after backtracking because clauses before it were satisfied at the split.
- Latent: `next(...)` at `_dpll` raises `StopIteration` if propagation ever misses a conflict; this is how the surviving mutants below show up. It is a loud failure, which is good.

## Findings

### High
None.

### Medium (defect, tests)

M1. `tests/checks/test_satlib.py:183-202` (`random_clause_set`) is too small to exercise watch maintenance. Formulas have at most 14 clauses, 6 variables, 4 literals. Two mutants of `satlib.py` pass all 34 satlib tests but are caught by my fuzz (`StopIteration` from a missed conflict):
- line 272, delete `kept.append(working)` for the "other watch is true" case (the clause silently loses its watch on `false`);
- line 283, delete `kept.extend(listed[position + 1 :])` on conflict (the unvisited watches are dropped).
The record claims eight mutants are all caught, and does not list these two. Fix: add a second generator to `test_random_formulas` (about 500 sets of 30 to 60 clauses, 10 to 30 variables, 1 to 9 literals, with repeats); the reference `rescanning_model` is fast enough at that size. I checked that my fuzz of that shape catches both. Other mutants I ran are caught: scan from index 3, scan to `len-1`, no swap, watch not re-appended, `head` not reset, roots conflict ignored, true first, first_open skipping.

M2. Two mutants hang instead of fail. I confirmed "watch moved to a false literal" hangs (90 s timeout). A hung suite is a poor failure mode for an amendment gate. Yes, the tests need a guard. Proposal, standard library only, Unix (SIGALRM; the harness runs on Linux). Verified to interrupt a busy loop:

```python
@contextlib.contextmanager
def time_limit(seconds):
    def fire(signum, frame):
        raise TimeoutError(f"no result in {seconds} s")
    old = signal.signal(signal.SIGALRM, fire)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)
```
Wrap each `solve_builtin` call in `check_result` and the long-chain and deep tests (say 10 s each; the longest legitimate one is well under that). Add the numpydoc docstring. If portability matters, `faulthandler.dump_traceback_later(60, exit=True)` in `setUpModule` is the cross-platform fallback, but it kills the run rather than failing one test.

### Low

L1. `satlib.py:185-187`: docstring rewrap left a short line ("The watches need no / undoing"); reflow.
L2. Record, Audit 2 and Tests bullet: "each of eight changes fails these tests" is true of the eight listed but reads as complete; amend after M1.
L3. Record "Review" section still says "Left for the reviewer"; fill in with a pointer to this file.
L4. Record's 3991-call and 3122-search comparisons I did not reproduce (I used a different corpus of random sets plus the live `verify`).

## Preferences, not defects
- Per-search rebuild of the watch lists (`_Search.__init__`) is the dominant remaining cost, as the record notes; reuse is a later unit.
- `values` returned by `_dpll` is the live `search.value`; fine since the search is discarded.

## Could not check
- z3 is not installed, so the z3 backend and its agreement are untested.
- Windows (SIGALRM unavailable) not tried.
- Timing is one machine, 3 runs.
- I did not run `check` with `--out-dir` reports; `verify` output equality was checked instead.
