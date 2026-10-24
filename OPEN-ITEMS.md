# Open items

Work that the custodian has directed or that a ratified round left open. It replaces the open items of the former HANDOFF.md (see git history). Close an item by doing it and removing its line; the record of the work stays in git and in `review-records/`.

## Harness, in the custodian's order

1. **Faster logic check.** Each transaction runs a full `verify`, and about 20 s of its 22.6 s go to the pure-Python DPLL solver in `harness/govharness/checks/logic/satlib.py`. Its unit propagation rescans every clause. Faster propagation (watched literals, or an index from literals to clauses) is a harness unit of its own, with tests and a review (custodian, 2026-10-24: next, after the round of 2026-10-24).
2. **M-c: unsigned authorizations.** Refuse an unsigned authorization where no signer register exists, unless the owner passes an explicit option. A small unit with tests and a review (custodian, 2026-10-24: now). Source: `review-records/round-2026-10-24/harn-auth/review-security.md`.
3. **QA.8 code review, then installation.** First, a code review of the harness by an agent of another configuration. Then install the derived configuration and run three installation tests, recording the results in unit 0008 (custodian, 2026-10-24: after the QA.8 review):
   - the guard's `allow` for an authorized `git push` or `gh` post against the kept ask rules;
   - the secret store's narrower `allowRead` against its `denyRead` pattern (unit 0007);
   - a shell write to `.git/config` failing under the M-a `denyWrite`.

   The transition of ledger entry 53 for STND.HARN.18 ends when that reviewed harness is installed and its configure entry records it. Whether the entry-53 transition for STND.HARN.26 to .28 has ended is for the custodian to record.
4. **M-b: expiry horizon.** Give `--expiry-horizon` a stated default bound. Later.

## Corpus, for later amendment rounds

- **Shared rules for compiled languages (R17).** Move STND.CXX.16 to .18 and .28 to .31 to STND.CODE, and replace the C reading of STND.STDC by citations (a minor amendment of STND.CODE, STND.CXX, and STND.STDC).
- **One definition of Untrusted input** in STND.CODE, with one reach for every language.
- **One naming rule (R18).** A language standard fixes names only where the language's own convention is checkable; otherwise the repository configuration governs (the STND.LEAN.27 form).
- **Differences among sibling language standards (R6, R16, R23):**
  - an unchecked index from untrusted input, binding in STND.JL.13;
  - checks in shipped builds (STND.CXX.27 against STND.JL.34);
  - counterparts of STND.RUST.13 sentence 2 (panic hook or handler) in STND.CXX and STND.PY;
  - logging as the only visible degradation (STND.PY.22 against STND.JL.15);
  - a committed lock-file default for STND.PY;
  - foreign interfaces in STND.PY and STND.JL;
  - the `#define NDEBUG` case in C source, which STND.CODE.6 does not reach.
- **Order of output in STND.MPI and STND.OMP.** Neither names its form of STND.CONC.30 yet.
- **References in older documents.** The script check of the round of 2026-10-24 (`tools/check_refs.py`, run from `harness/` with `PYTHONPATH=.`; not yet part of the harness) finds 22 places where a document is named without a References row, all in text that predates the round. Extending the harness check g.25 to bare document names would keep the table and the check in agreement.
