# Open items

Work that the custodian has directed or that a ratified round left open. It replaces the open items of the former HANDOFF.md (see git history). Close an item by doing it and removing its line; the record of the work stays in git and in `review-records/`.

## Harness, in the custodian's order

1. **STND.HARN.30, unsigned reliance (decision).** Unit 0010 (merged) refuses an unsigned authorization where no signer register exists unless the owner passes `--accept-unsigned`, and names it in the coverage report. The unit record proposes a new provision STND.HARN.30 so that the rule is in the corpus and not only in this harness. The custodian decides whether to adopt it, and how STND.DRAFT.42 reads on an owner's acceptance at derivation. Source: `harness/records/units/0010-unsigned-authorizations.md`.
2. **QA.8 code review, then installation.** First, a code review of the harness by an agent of another configuration. Then install the derived configuration and run three installation tests, recording the results in unit 0008 (custodian, 2026-10-24: after the QA.8 review):
   - the guard's `allow` for an authorized `git push` or `gh` post against the kept ask rules;
   - the secret store's narrower `allowRead` against its `denyRead` pattern (unit 0007);
   - a shell write to `.git/config` failing under the M-a `denyWrite`.

   The transition of ledger entry 53 for STND.HARN.18 ends when that reviewed harness is installed and its configure entry records it. Whether the entry-53 transition for STND.HARN.26 to .28 has ended is for the custodian to record.
3. **M-b: expiry horizon.** Give `--expiry-horizon` a stated default bound. Later.

## Corpus, in progress

- **STND.TEST and STND.PERF.** Two new LVL2 standards, all defaults (custodian, 2026-10-24).
  - STND.TEST covers the method of writing, running, and interpreting test suites. The tests run before a merge widen with the level of integration: a subfeature merging into a feature runs fewer tests than a merge into the main line, which runs the full suite. The obligation stays RSRC.11 and RSRC.12.
  - STND.PERF covers the systematic evaluation of absolute, relative, and scaling performance, where a task calls for it or a work is declared performance-sensitive. It names no methods or tools.
  - With them, STND.WPROC.9 and STND.CREW gain citations of STND.TEST.
  - Research is in `research/test-notes/` and `research/perf-notes/`.

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
