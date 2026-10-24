# Governance distribution at ledger entry 109 — handoff for local work

This is the working governance corpus as of 2026-10-24: the snapshot of repository commit `e2b3563` plus ledger entries 46 to 114, all ratified by the custodian and applied with the harness's own commands. Entries 110 (HW 1.1.1), 111 (MNEM row CONC), 112 (STND.CONC 1.0), 113 (MNEM row OMP), and 114 (STND.OMP 1.0) were applied in the local repository; their review records are in `review-records/ledger110/`, `review-records/ledger111/`, and `review-records/ledger113/`. `verify` passes. Entries 46 to 109 are committed to a local git repository rooted at this directory; history before the snapshot of `e2b3563` did not carry over.

## Contents

| Path | What it is |
| --- | --- |
| `harness/` | The runnable harness: `governance/` (the corpus, system of record), `govharness/` (Python 3.11+, standard library only), `tests/`, `records/` (units, reviews, decisions, and the findings log of entries 1 to 45), `rendered/` (the six reading copies of `compose`), `README.md` |
| `rendered/` | A reading copy of each document, composed by `govharness.derive.reading_copy.compose` (one file per document; the `_PROJECT` templates have none) |
| `docs/COMMIT_MSG.txt` | Commit message for entries 46 to 109 |
| `docs/CORPUS.md`, `docs/adoption-README.md`, `docs/scientific-software-constitution.md` | The project's corpus guide, adoption-folder note, and pointer document, as they stand in the claude.ai project |
| `research/` | Research notes behind the C++, Python, Julia, and MPI standards (`parallel-models.md` is cited by STND.MPI) |
| `review-records/` | Review records for entries 100 to 105 and 106 to 109 (tar.xz; the project holds base64 copies) |
| `tools/` | Drafting, revision, and review briefs; `lvl0.txt` (compact LVL0); `findings.py`; `amendment-scripts/` (the content modules and apply scripts that produced the entries, kept as worked examples; they hard-code `/home/claude/...` paths) |

## Quick check

```bash
cd harness
python -B -m govharness verify governance        # every check passes
python -B -m govharness check --out-dir /tmp/r governance
python -B -m unittest discover -s tests -t .     # all 129 pass
```

Last ledger entry: seq 114, `2026-10-24T14:23:53+00:00`, hash prefix `229e01bcf89c71b7` (STND.OMP 1.0).

## Repository

The repository is local. Its first commit is the handoff snapshot (`e2b3563` plus entries 46 to 109) with `docs/COMMIT_MSG.txt` as its message; later commits update the harness tests and README to the current corpus, add unit 0007 (the secret store in the derived environment), and apply HW 1.1.1, STND.CONC 1.0, and STND.OMP 1.0. `SHA256SUMS` lists the files as delivered. Harness code for STND.HARN.26 to .28 (unit 0006) is in `govharness/`.

## How the work has been run (the custodian's standing process)

1. Draft outcome-based provisions that are minimal, timeless, and checkable (GOV.18); never block work needlessly; never require a decision of the human owner beyond what LVL0 assigns (STND.DRAFT.42).
2. Self-check against STND.DRAFT: one modal per sentence and at most three per provision; each condition before its clause, one per sentence; no banned body words ("such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any"); titles of six words or fewer, not verb-initial, distinct across the corpus; body IDs equal `instantiates` plus `refers_to`.
3. Class onset follows STND.CLASS.10; never raise the floor (GOV.11). A provision becomes binding when its `instantiates` closure reaches PRIME, GUARD, GOV, or a floor ID; argue why it raises no floor and put that to the custodian.
4. Rehearse on a scratch copy, one transaction per document, in citation order; then a cold review and a STND.HARN.28 pair review by agents of another configuration, fixes, and a cold verification.
5. Present for ratification; apply only after ratification; then rebuild copies, bundle, and the project docs, archiving whatever is replaced.

## The custodian's standing directions (summary)

- **Agnostic:** platform, compiler, vendor, implementation, and tool agnostic. No version numbers, products, or tools in provisions; Notes name them only to explain a hazard, as examples. Versions and tools are the project's choice.
- **Documentation (STND.DOCS):** written for human readers only; no agent notes, governance, or process records in work documentation; American English everywhere; none of the "Signs of AI writing" patterns; consistent with itself and the code.
- **Determinism (STND.VVUQ.82, .83):** strict determinism is an option where feasible, not a requirement unless the acceptance criterion or the consequence class demands it. Known, declared jitter within the agreed tolerance is not a defect, and agents do not churn over it. A true race condition is a correctness defect.
- **High-assurance C++:** any coding standard a decision record adopts; the edition follows the toolchain's validation status; elsewhere the newest edition the compiler supports.
- **Security constraints (verbatim):** "Never irreversibly delete or overwrite large numbers of files; archive first." (Since 2026-10-24, cleanup no longer needs the custodian's permission.) "Never keep authentication credentials; delegating access is my responsibility." "Never disclose secrets, explicitly or implicitly." "Never circumvent paywalls; open alternatives are fine." "Research retrieval is bounded at 10,000 items and 10,000 MB per effort." No workaround after a failed fetch; no mirrors or archives of blocked content.

## Open items

- **STND.HARN.18:** the remote-write row remains under the transition of entry 53; letting a write that an authorization names by destination and kind proceed without referral needs an authorization format that STND.PROJ does not yet fix. (The secret store is mapped per file and authorization by unit 0007; confirm on installation that the narrower `allowRead` wins over the store's `denyRead` pattern.)
- **NUMER.2:** at NUMER's next revision, add a row to its shared-matters table giving NUMER the keying and construction of random streams for a computation divided among tasks (STND.CONC.23, NUMER.24), as the custodian assigned at the adoption of STND.CONC.
- **STND.OMP:** once the offload standard is adopted, STND.OMP at its next revision cites it for the rules that hold for every offload model (completion before results are read, the movement of data, device arithmetic), as its Notes say.
- **Language standards:** at their next revisions, STND.CXX (15, 23, 26), STND.PY (17), and STND.JL (24, 27) can cite STND.CONC for the model-neutral part of their concurrency rules.
- **Next standards, in the custodian's order (revised 2026-10-24):** STND.CONC is adopted (entry 112; the custodian ruled that no amendment of HW.12, HW.20, or STND.CODE.3 is needed, since STND.CONC holds those rules); STND.OMP is adopted (entry 114: 33 defaults, citing STND.CONC; the rules of offload that hold for every model wait for the offload standard, which STND.OMP's Notes name as planned); next CUDA / accelerator offload (agnostic form, with annexes for HIP, SYCL, OpenCL, and OpenACC), citing STND.CONC; then a separate standard for workflows and long-run resilience; then BUILD (CMake, Automake, Makefiles), C, Rust, Fortran (classic and modern), Verilog/SystemVerilog, and Lean4. Language standards later gain concurrency amendments that cite STND.CONC. Kokkos, OpenACC, and SYCL get their own standards only when a project adopts them; other parallel libraries come in through STND.DEPS. No LVL1 profile on concurrency for now. Each follows the determinism and agnostic directions above. Research: `research/openmp-notes/` and `research/concurrency-notes/`.
