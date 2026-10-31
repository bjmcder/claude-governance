# Round of 2026-10-31: shared brief for drafting agents

You draft one part of the amendments that carry the corpus findings of the cleanup audit of 2026-10-31. Read this brief whole, then the part assigned to you below.

REPO is `/home/brianm/projects/utils/governance-harness`, branch `audit-2026-10-31`. Run the harness from `REPO/harness/`.

## Read first

1. `REPO/for-agents/standing-process.md`: the standing process and directions. Its drafting rules, agnosticism, no restatement (GOV.31), floor argument, and documentation directions bind every word you draft.
2. `REPO/review-records/audit-2026-10-31/decisions.md`: the outcomes to draft. Draft each outcome given there, no more and no less.
3. `REPO/review-records/audit-2026-10-31/findings.md`: the findings, with evidence and scenarios. Check each against the current text before you draft; the audit's wording is a starting point.
4. Examples of a finished round:
   - `REPO/tools/amendment-scripts/apply_constitution_round_2026_10_28.py`, a LVL0 amendment followed by a STND.DFLT amendment, with its record `REPO/review-records/round-2026-10-28-constitution/decisions.md`;
   - `REPO/tools/amendment-scripts/apply_round_a_2026_10_28.py` and the modules it imports, for several documents;
   - `REPO/review-records/rounds-2026-10-28/round-a/decisions.md`, a round record.
5. The reading copies in `REPO/rendered/` of LVL0, STND.DRAFT, STND.IDENT, STND.CLASS, and each document you touch. They carry a stray ". Instantiates ." line that the harness fix is removing, so ignore it. Before you change a provision, read its live file: `python3 -B -m govharness show governance ID`.

## What you write

- **Your part module**, `REPO/tools/amendment-scripts/apply_audit_<part>_2026_10_31.py`. The driver `apply_audit_2026_10_31.py` runs the parts in the order lvl0, tech, process.
  - It defines `apply(root)`, a module constant `AT` (the driver overwrites it before calling `apply`), and `TRANSACTIONS`, the number of ledger transactions it records.
  - Transaction k (counting from 0) takes the time `AT` plus k seconds, and each revision row is dated by its transaction.
  - Record one transaction per document, in citation order.
  - Use `rounds_common` (as `F`) for `swap_para`, `set_body`, `withdraw`, `check_fields`, `finish`, and `AUTHOR`, and `govharness.workflows.amend.replace_text`, in which each old text occurs exactly once.
  - Helper modules of your own are fine. Name them `audit_<part>_*.py`.
  - Set `RECORD = "review-records/audit-2026-10-31/decisions.md"` in your module; do not use `F.RECORD`.
- **Revision rows and rationales** in the form of the examples. Each rationale states:
  - the reading;
  - the class under STND.IDENT.3;
  - the floor argument (GOV.11);
  - the onset, where one changes;
  - "Transition (GOV.42): …".
  It cites the finding IDs and the ruling as "recommendation R<n> of review-records/audit-2026-10-31/findings.md, put to the custodian at ratification", and ends with `F.AUTHOR`. A rationale may say "ratified by the custodian on <date>", since the script runs only after ratification. It never says that the custodian ruled a recommendation.
- **Your record**, `REPO/review-records/audit-2026-10-31/<part>/decisions.md`. It holds:
  - each outcome carried, with the drafted text quoted;
  - the floor argument for each provision that binds;
  - each point where you chose a reading that `decisions.md` does not fix, marked "For the custodian at ratification" and stated as a choice with your recommendation.

## What you must not do

- Edit `REPO/harness/governance/`. It changes only when the custodian ratifies.
- Edit harness code, the docs, or another part's files. A harness agent is working in a separate worktree.
- Name a tool, product, vendor, or version in a provision.
- Restate a provision that another holds. Cite it instead.
- Raise the floor (GOV.11).
- Commit. The lead commits.

## Checks before you return

1. **Rehearse** on top of the parts that precede yours:

   ```bash
   PARTS=<earlier parts>,<yours> python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_audit_2026_10_31.py
   ```

   Every check must pass with only the g.18 warning that the corpus already carries. A new warning is either fixed or explained in your record.
2. **On a kept copy**, make `<dir>` under `/tmp/claude-1000/-home-brianm-projects-utils-governance-harness/dd5b6543-26b0-461c-b4d2-a83cf831ff9f/scratchpad/<part>/` and copy `governance/` into it, then run `PARTS=... python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_audit_2026_10_31 as R; R.apply('<dir>/governance')"`. On that copy:
   - run `references <dir>/governance --check` and `compose <dir>/governance --check`;
   - for each changed document, run `pairs <dir>/governance ID` (with `--amends` for each LVL0 provision that you amend). Write the pairs whose changed side is a provision you changed to `<part>/pairs-changed.md`, each with your verdict: conflict or none;
   - for each changed document, run `PYTHONPATH=. python3 -B ../tools/findings.py <dir>/governance '<regex>'`, and fix or explain each new finding.
3. **Self-check** every provision you drafted against step 2 of the standing process.

Return a summary of at most 250 words:
- the documents and revisions;
- the transactions;
- the readings put to the custodian;
- the check results;
- anything you could not carry, and why.
