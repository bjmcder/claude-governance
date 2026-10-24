# Review brief: STND.ANNEX 1.0 and STND.MPI 0.1 (2026-10-23)

You are a read-only reviewer at delegation depth 1. No network. Create only your one report file. Read-only scans (grep, python that only reads) are fine.

## Material
- Rehearsed corpus: `/home/claude/scratch-r6/governance` (live ledger 105, then STND.ANNEX 1.0 as 106, the MNEM row MPI as 107, STND.MPI 0.1 as 108). `verify` passes.
- Reading copies: `/home/claude/scratch-r6/rc/annex-1.0-draft.md`, `/home/claude/scratch-r6/rc/mpi-0.1-draft.md`. Provision files: `governance/STND/ANNEX/`, `governance/STND/MPI/`. Rationales: `/home/claude/pkg/apply_annex.py`, `/home/claude/pkg/apply_mpi.py`.
- Constitution: `/home/claude/tools/lvl0.txt`. Drafting rules: `governance/STND/DRAFT/`. Class onset: `governance/STND/CLASS/10.md`.
- Research behind STND.MPI: `/home/claude/research/parallel-models.md`.
- Pair lists (STND.HARN.28): `/home/claude/scratch-r6/pairs-STND.ANNEX.txt` (404 pairs), `/home/claude/scratch-r6/pairs-STND.MPI.txt` (226 pairs).

## Rules the drafts must meet
- Binding vs default (GOV.19): binding when the `instantiates` closure reaches PRIME, GUARD, GOV, or a floor ID (REPRO.5, QA.1, INTPR.2, VV.7). A binding provision must not raise the floor at CSQ4 (GOV.11): it may ask only what PRIME, GUARD, GOV, or the floor already require, at the cost of wording or a record.
- Drafting: one modal per sentence, at most three per provision; each condition before its clause, one per sentence; bodies avoid "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any"; titles at most six words, not verb-initial, distinct; body IDs equal instantiates ∪ refers_to; Notes hold no obligations and no drafting narration; American English; none of the STND.DOCS.9 patterns.
- The custodian's standing rulings: platform, compiler, vendor, implementation, and tool agnostic (no version numbers, product, or tool names in provisions; Notes name them only to explain a hazard, as examples). Never require a decision of the human owner beyond LVL0 (STND.DRAFT.42). Never block work needlessly.
- Custodian's MPI directions: scope is MPI including its threading (point-to-point, collectives, one-sided, parallel I/O, error handling, library conduct, testing, thread level); GPU-aware transfers stay under HW.GPU; C++ interface rules stay in STND.CXX. Reproducibility: results depending on process count or reduction order are declared and tests compare several process counts within a stated tolerance; where bitwise identity across process counts is an acceptance criterion, collective reductions use a fixed or order-independent combination.
- Custodian's ANNEX directions: default contracts general and not performance-limiting; HW.FPGA and HW.ASIC defaults timeless and unconstrained; a default only tightens what the profiles require.

## Report
At most 900 words, to the path given in your task. Sections: Findings (Defect / Should-fix / Optional, each with location and a concrete fix), Verdict. Report only what you verified; mark anything you could not check.
