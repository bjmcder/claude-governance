# Round of 2026-10-27: draft status

The text of the round is drafted and rehearsed. Nothing is applied to the live corpus. The custodian's decisions are in `decisions.md`.

## Amendments, in ledger order

| Seq (rehearsed) | Document | Revision | Class | Script | What changes |
| --- | --- | --- | --- | --- | --- |
| 188 | STND.CODE | 1.2 to 1.3 | Minor | `apply_code_1_3.py` | New STND.CODE.22 (types and layouts), .23 (arrays), .24 (failures crossing), .25 (ownership), .26 (objects that foreign code keeps), all defaults; term Foreign interface; Purpose and Notes |
| 189 | STND.DEPS | 1.0 to 1.1 | Minor | `apply_deps_1_1.py` | Term Lock file; new STND.DEPS.12 (default), the lock file of an environment or build that produces reported results under version control; Purpose and Notes |
| 190 to 192 | STND.FTN, STND.MPI, STND.OMP | 1.1 to 1.1.1, 1.0.1 to 1.0.2, 1.0.2 to 1.0.3 | Editorial | `apply_fi_editorial_2026_10_27.py` | Notes cite STND.CODE.22 to .26 in place of STND.CXX.20 and .22 |
| 193 | STND.STDC | 1.1 to 1.2 | Minor | `apply_stdc_1_2.py` | STND.STDC.36 withdrawn; term imported; Notes |
| 194 | STND.PY | 1.1 to 1.2 | Minor | `apply_py_1_2.py` | STND.PY.33, .34, .36, .37 withdrawn; STND.PY.35 cut to the interrupts of the operator; terms imported; Notes |
| 195 | STND.RUST | 1.1 to 1.2 | Minor | `apply_rust_1_2.py` | STND.RUST.24, .25, .27, .30 cut to their Rust content; STND.RUST.10 and the Notes use the imported term; terms imported; no withdrawal |
| 196 | STND.JL | 1.2 to 1.3 | Minor | `apply_jl_1_3.py` | STND.JL.4, .37, .40, .41 withdrawn; STND.JL.38 and .39 cut to their Julia content; terms imported; Notes |
| 197 | STND.CXX | 1.2 to 1.3 | Minor | `apply_cxx_1_3.py` | STND.CXX.20 and .22 withdrawn; STND.CXX.5 cites STND.CODE.25; term imported; Notes |

The scripts are in `tools/amendment-scripts/`, with the helpers of `fi_common.py`; `apply_round_2026_10_27.py` runs them in this order. Rehearsal: `python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_round_2026_10_27.py` appends entries 188 to 197, every check passes with the g.18 warning that the corpus already carries, and the source is unchanged.

## Order

STND.CODE and STND.DEPS come first, since every other amendment cites their new provisions. Each amendment that drops a citation of a provision to be withdrawn comes before the amendment that withdraws it, so that no state of the round cites a withdrawn identifier: STND.PY and STND.RUST drop STND.JL.4 before STND.JL withdraws it, and every document drops STND.CXX.20 and .22 before STND.CXX withdraws them. STND.RUST.27 is kept, cut to its release in a `Drop` implementation, since STND.JL and STND.PY cite STND.RUST.24 to STND.RUST.27 and STND.RUST cites STND.JL.4, which no order of single transactions could otherwise satisfy.

## What the drafting decided that the decisions did not

- The language-neutral rules are five provisions, not one, because STND.DRAFT.28 allows at most three sentences in one provision, and only where they are never applied apart.
- The interrupts of the operator in STND.PY.35 and STND.JL.39 stay as they were ratified: stored in place of their conversion, and raised again after the foreign call returns. STND.CODE.24 has every other failure converted where the interface carries errors.
- STND.CODE.25 adds, for Python and Julia, the pass of a foreign resource to its owner before each other operation that is able to fail, which STND.CXX.20 and STND.RUST.27 asked.
- STND.CODE.24 lets a failure pass on where the contract of the interface carries it on to code of the work, as STND.PY.35 did and STND.RUST.25 did by its unwinding ABI; this relaxes STND.CXX.22 and STND.JL.39.
- STND.DEPS.12 has no permission sentence for a package that other work uses, since the condition on reported results already leaves its lock file out; the Notes say so.

`reading-copies/` holds a reading copy of each changed document, and `pairs/` the pairs of STND.HARN.28 for each; `pairs-changed.md` lists the 130 pairs whose changed side is a changed or new provision. The documents before the round are in `rendered/` at the repository root.

## Harness code

None is owed: the round changes no rule that the harness checks.
