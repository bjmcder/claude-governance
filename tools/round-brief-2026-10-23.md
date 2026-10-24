# Brief for the LVL2 round of 2026-10-23: STND.ANNEX 1.0 and STND.MPI 1.0

Read `/home/claude/tools/drafting-brief.md` first for the role, corpus layout, modes, class onset, drafting rules, and build helpers. This brief overrides it where they differ.

## What changed since that brief

- The live corpus is `/home/claude/harness/governance`, at ledger entry 105. STND.DOCS, STND.CODE 1.1 (with STND.CODE.13), STND.CXX, STND.PY, and STND.JL are adopted. Read their reading copies in `/home/claude/out105/downstream/` and the corpus copies in `/home/claude/out105/copies/`.
- Your own text follows STND.DOCS (adopted): American English, no patterns of STND.DOCS.9, Notes without obligations or drafting narration.
- Model your content module on `/home/claude/pkg/content_cxx.py` and your apply script on `/home/claude/pkg/apply_cxx.py` (current helpers and rationale form). The rationale cites no ledger entry numbers. Its review record is `claude/drafts/review-records-ledger106-108.md`. Its transition sentence is your recommendation.
- Planned ledger order: STND.ANNEX 106 (AT `2026-10-23T18:00:00+00:00`), MNEM register of MPI 107 (`/home/claude/pkg/apply_mnem_mpi.py`, AT 18:05; already written, do not edit), STND.MPI 108 (AT 18:10). DATE is `"2026-10-23"`.

## The custodian's standing rulings (apply to both)

- "We are platform and compiler agnostic"; versions and tools are the project's choice. No provision names a version number, compiler, platform, vendor, library to depend on, or tool. State the outcome a tool or reviewer decides (GOV.18). The Notes carry no recommended configuration or tool table. A Note may name a tool, product, or library only where needed to explain a hazard a provision guards against, as an example, without a version.
- Never raise the floor (GOV.11). A binding provision asks only what PRIME, GUARD, GOV, or a floor provision already requires, at the cost of wording or one record. Where a provision must bind, the Notes argue why it raises no floor, and the argument goes to the custodian as a decision; never write that the custodian has ruled.
- Never require a decision of the human owner that LVL0 does not assign (STND.DRAFT.42). Never block work needlessly.
- Class onset per STND.CLASS.10; state it in the Notes.

## Rehearsal

Fresh copy of the live corpus into your scratch directory; apply only what your document needs (ANNEX: yours alone; MPI: `apply_mnem_mpi.apply(root)`, then yours); run `verify` and `findings.py`; compose your reading copy to `draft.md` in your scratch directory with `compose(read_corpus(root), read_ledger(root), ReadingCopy(id, name))` (imports: `govharness.derive.reading_copy`, `govharness.cli.derived.read_corpus`, `govharness.ledger.chain.read_ledger`), titled draft 0.1.

## Deliverable

Final message under 500 words: paths; verify result and remaining findings; numbered decisions for the custodian, each with your recommendation and reason; facts left unverified.
