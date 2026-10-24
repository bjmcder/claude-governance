# Governance distribution at ledger entry 109 — handoff for local work

This is the working governance corpus as of 2026-10-24: the snapshot of repository commit `e2b3563` plus ledger entries 46 to 109, all ratified by the custodian and applied with the harness's own commands. `verify` passes. Entries 46 to 109 are **not yet committed** to the repository.

## Contents

| Path | What it is |
| --- | --- |
| `harness/` | The runnable harness: `governance/` (the corpus, system of record), `govharness/` (Python 3.11+, standard library only), `tests/`, `records/` (units, reviews, decisions), `README.md` (its corpus description is stale, about entry 45) |
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
python -B -m unittest discover -s tests -t .     # 16 known failures, see below
```

Last ledger entry: seq 109, `2026-10-24T08:38:00+00:00`, hash prefix `bcac6332a0872122`.

## Committing to the repository

Replace the repository's `governance/`, `govharness/`, `tests/`, and `records/` with those in `harness/`, review the diff against `e2b3563`, and commit with `docs/COMMIT_MSG.txt`. No patch file is shipped; `git diff` after the copy is the patch. Harness code for STND.HARN.26 to .28 (unit 0006) is already in `govharness/`.

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
- **Security constraints (verbatim):** "Never irreversibly delete or overwrite large numbers of files; archive first. If cleanup is needed to free up space, ask for permission." "Never keep authentication credentials; delegating access is my responsibility." "Never disclose secrets, explicitly or implicitly." "Never circumvent paywalls; open alternatives are fine." "Research retrieval is bounded at 10,000 items and 10,000 MB per effort." No workaround after a failed fetch; no mirrors or archives of blocked content.

## Open items

- **Tests:** 16 of 129 fail, the same set before and after entries 100 to 109. They encode expectations of an earlier corpus (pair counts, rendered copies, retrieval budgets, amendment helpers) and need updating to the current corpus.
- **Harness README** describes the corpus at about entry 45; needs a rewrite.
- **STND.HARN.18:** map the optional secret store per file and authorization; the remote-write row remains under the transition of entry 53.
- **HW:** at its next revision, add an informative Note that for a multi-process run the execution path of HW.8 is the whole run (ruled with STND.MPI.6).
- **Next standards, in the custodian's order:** OpenMP (after 6.1 is published), CUDA / accelerator offload (agnostic form), then BUILD (CMake, Automake, Makefiles), C, Rust, Fortran (classic and modern), Verilog/SystemVerilog, and Lean4. Each follows the determinism and agnostic directions above.
