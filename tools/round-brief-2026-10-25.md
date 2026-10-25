# Brief for the closing round of 2026-10-25

Every agent of this round reads this brief first. Your task message names your role and your package, and it overrides this brief where the two differ.

## Common

**Repository and corpus.** The repository is `/home/brianm/projects/utils/governance-ledger109` (below, `REPO`). The live corpus is `REPO/harness/governance`, at ledger entry 147.
- Never write to the corpus, to its ledger, or to another agent's files.
- Reading copies of every adopted document are in `REPO/rendered/`.
- The definition of done for this round is `REPO/review-records/round-2026-10-25-close/definition-of-done.md`. Read it.

**Directions and rules.** The custodian's standing process and directions are in `REPO/CUSTODIAN.md`. They bind you: the agnostic and determinism directions, never raising the floor, no restatement, STND.DOCS style, and the security constraints. Then read the Common, Amendment agents, and Review agents sections of `REPO/tools/round-brief-2026-10-24.md`, which hold the drafting rules, the scripts, rehearsal, and the tests of review. Where they conflict, this brief and CUSTODIAN.md win. Note these points in particular:
- No archive copies: git is the recovery path.
- The harness is now fast, so a rehearsal takes seconds.
- `tools/check_refs.py` checks References against bare document names. Run it from `REPO/harness` with `PYTHONPATH=. python3 -B ../tools/check_refs.py <root> [DOC ...]`.

**Scratch and records.**
- Scratch work goes in `REPO/.scratch/<package>/`.
- Scripts go in `REPO/tools/amendment-scripts/`: one per amended document, named `apply_<doc>_<revision>.py`, plus one round script per package, `apply_close_<package>.py`, which applies that package's scripts in order on top of entry 147.
- Records go in `REPO/review-records/round-2026-10-25-close/<package>/`.
- Use `DATE = "2026-10-25"` and placeholder AT times. The lead sets the real times at the coalesce.

**Model scripts.**
- Editorial amendment: `apply_cxx_1_1_1.py`.
- Minor amendment that adds a provision: `apply_conc_1_1.py`.
- Minor amendment that changes text: `apply_jl_1_1.py`.
- Helpers: `replace_text`, `raise_revision`, and `record_transaction` in `REPO/harness/govharness/workflows/amend.py`.
- End each rationale with the fixed tail exactly: " Text authored by an agent, Claude (Anthropic), at the custodian's direction (REPRO.5). Under the ruling of ledger entry 15, this decision is the QA.7 review." Cite no entry of this round by number.

## The custodian's rulings this round carries out

These were ratified on 2026-10-24 with the recommendations of `REPO/review-records/round-2026-10-24/decisions-final.md`, and on 2026-10-25 with those of `REPO/review-records/round-2026-10-24-test-perf/decisions.md`. Read the items cited here.

- **Shared rules for compiled languages (decision 8, R17).** Move STND.CXX.16 to .18 and .28 to .31 to STND.CODE "in the next round", which is this one.
  - Move the language-neutral outcome only. Each language standard keeps the form its language needs and cites STND.CODE for the rest.
  - STND.CODE covers every language, so a moved binding provision reaches Python, Julia, and the others too. Argue for each one that it raises no floor there (GOV.11). A C++ ruling is not extended to another language without its own argument (R22). Where the argument fails for a language, the moved provision is conditioned, or stays in the language standards.
- **One definition of Untrusted input (decision 4).** STND.CODE defines the term once, with one reach.
  - The reach the ruling of 2026-10-23 gave STND.PY and STND.JL, and that decision 4 extended to STND.RUST and STND.FTN, is the arguments of each function of the public interface that the documentation or the repository configuration names, unless the threat model records otherwise.
  - The language standards import the term and delete their own definitions.
- **One naming rule (decision 9, R18).** A language standard fixes names only where the language's own convention is checkable; otherwise the repository configuration governs. This is the STND.LEAN.27 form, with the NUMER.4 notation allowance. The STND.CXX.14 and STND.JL tables stay. No table is added for C.
- **The sibling list (decision 10).** Each item is resolved in this round, either by an amendment or by a reasoned "no change" that the custodian records at ratification:
  - an unchecked index from untrusted input, binding in STND.JL.13, against STND.PY.25;
  - checks in shipped builds, STND.CXX.27 against STND.JL.34;
  - counterparts of STND.RUST.13 sentence 2 (panic hook or handler) in STND.CXX and STND.PY;
  - logging as the only visible degradation, STND.PY.22 against STND.JL.15. Decision 7 keeps both as ruled, so this item closes with no change.
  - a committed lock-file default for STND.PY;
  - foreign interfaces in STND.PY and STND.JL;
  - the `#define NDEBUG` case in C source, which STND.CODE.6 does not reach.
- **STND.OFFLD.31** cites STND.PERF.12 and .14 (decision 7 of 2026-10-25).
- **STND.MPI and STND.OMP** name their form of STND.CONC.30.
- **STND.HARN.30.** Adopt unit 0010's proposal, in `REPO/harness/records/units/0010-unsigned-authorizations.md`, through the standing process. The reading of STND.DRAFT.42 on an owner's acceptance at derivation goes to the custodian as a decision, with both readings and the record's options.
- **References.** Close every gap that `tools/check_refs.py` reports on the live corpus, 22 documents in all.

Each "no change" and each floor argument is a decision for the custodian. List them in your final message, each with a recommendation.
