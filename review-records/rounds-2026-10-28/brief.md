# Rounds of 2026-10-28: shared brief for drafting agents

You draft one round of amendments to the governance corpus that carries the custodian's rulings on the deep review of 2026-10-28. Read this brief whole, then your round's own brief.

## Read first

1. `REPO/for-agents/standing-process.md`: the custodian's standing process and directions. Its drafting rules, agnosticism, no restatement (GOV.31), floor argument, and documentation directions bind every word you draft.
2. `REPO/review-records/deep-review-2026-10-28/rulings.md`: the rulings. Its last section, "Rulings of the custodian, 2026-10-28", quotes each ruling and gives the reading on which you draft. Draft that reading, no more and no less.
3. `REPO/review-records/deep-review-2026-10-28/register.md`: the verified entries, with the proposed text and the source finding IDs. The source reports in the same folder (`corpus-core.md` CC, `corpus-process.md` CP, `corpus-code.md` CL, `corpus-systems.md` CS, `anthropic-docs.md` AD, `harness.md` HR) hold the exact proposed wording. Check each proposal against the current text before you use it: the reviewers' wording is a starting point, not ratified text.
4. An example of a finished round: `REPO/tools/amendment-scripts/apply_tables_round_2026_10_27.py`, and its record `REPO/review-records/round-2026-10-27-tables/decisions.md`. For several documents, see `apply_round_2026_10_27.py` and the modules it lists.

REPO is `/home/brianm/projects/utils/governance-harness`, branch `rounds-2026-10-28`. The harness is run from `REPO/harness/`.

## What you write

- **Your round module**, `REPO/tools/amendment-scripts/apply_round_<x>_2026_10_28.py`, with `<x>` as your round brief gives it.
  - It defines `apply(root)`, a module constant `AT`, which the driver overwrites, and `TRANSACTIONS`, the number of ledger transactions it records.
  - Use `rounds_common` (import it as `F`) for its helpers: `swap_para`, `set_body`, `withdraw`, `check_fields`, `finish`, `DATE`, `RECORD`, `AUTHOR`.
  - Also use `govharness.workflows.amend.replace_text`. Each old text must occur exactly once.
  - Record one transaction per document, in citation order, so that no state of the round cites a withdrawn identifier or a provision not yet added. A transaction k of the module (counting from 0) takes the time `AT` plus k seconds.
  - Helper modules of your own are fine. Name them `round_<x>_*.py`.
- **Revision rows and rationales** in the form of the earlier rounds:
  - "Minor amendment of STND.X, revision N, ratified by the custodian on 2026-10-28: READING. The change is minor under STND.IDENT.3 because …", then the floor argument (GOV.11), the class onset where one changes, and "Transition (GOV.42): …";
  - the rulings relied on, as "Ruling A2 of review-records/deep-review-2026-10-28/rulings.md", and the register entry;
  - then `F.AUTHOR`.

  The script is applied only after ratification, so "ratified by the custodian on" is true when it runs. Choose the class by STND.IDENT.3. An amendment of LVL0 (GOV, QA, PRIME, GUARD, and the other LVL0 documents) is recorded as the earlier LVL0 amendments are; find one in `harness/governance/ledger.jsonl` and follow its form.
- **Your round record**, `REPO/review-records/rounds-2026-10-28/round-<x>/decisions.md`:
  - the rulings carried, each with the drafted text quoted;
  - each register entry carried, with its source IDs;
  - the floor argument for each provision that binds;
  - every point where you had to choose a reading that the ruling did not fix. Mark each "For the custodian at ratification". These are the questions that will go to the custodian, so state each as a choice with your recommendation.
- **Harness code**, only where your round brief says the text needs it.
  - Use the unit number your brief gives, a record at `REPO/harness/records/units/00NN-*.md` in the form of unit 0022, tests for each change, and the architecture and conventions tests kept.
  - No check's verdict on the live corpus may change, except where your round's text asks for it. Say so in the record.

## What you must not do

- Edit `REPO/harness/governance/` directly. The live corpus changes only when the custodian ratifies and the scripts run.
- Write that the custodian ruled anything beyond the quoted rulings. A reading the rulings do not fix is drafted "for ratification".
- Name a tool, product, vendor, or version in a provision.
- Restate a provision that another holds. Cite it instead.
- Raise the floor (GOV.11) without a recorded project decision naming the consequence. Ruling C4 relies on the human owner's entry of an expected class as that decision; see its reading.
- Commit. The lead commits. Another round may be drafted at the same time in the same working tree, so touch only your own module, your own record folder, and your own unit's code.

## Checks before you return

1. **Rehearse** on top of the finished rounds:

   ```bash
   ROUNDS=<finished rounds>,<yours> python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py
   ```

   Your brief names the finished rounds. Every check must pass, with only the g.18 warning that the corpus already carries. A new warning is either fixed or explained in your record.
2. **On a kept copy** (make `<dir>` under `/tmp/claude-1000/`, copy `governance/` into it, then run `ROUNDS=... python3 -B -c "import sys; sys.path.insert(0,'../tools/amendment-scripts'); import apply_rounds_2026_10_28 as R; R.apply('<dir>/governance')"`):
   - `python3 -B -m govharness references <dir>/governance --check`;
   - `python3 -B -m govharness compose <dir>/governance --check`;
   - `python3 -B -m govharness pairs <dir>/governance ID` for each changed document. Write the pairs whose changed side is a provision you changed to `round-<x>/pairs-changed.md`, each with your verdict: conflict or none;
   - `PYTHONPATH=. python3 -B ../tools/findings.py <dir>/governance '<regex>'` for each changed document, with a new finding fixed or explained.
3. **Self-check every provision you drafted** against the drafting rules of the standing process:
   - one modal per sentence, and at most three per provision;
   - conditions before clauses;
   - none of the banned body words;
   - titles of six words or fewer;
   - body identifiers equal to `instantiates` plus `refers_to`.
4. **Code:** if you changed harness code, run its targeted tests and the fast subset (`harness/README.md`).

Return a summary of at most 250 words:
- the documents and revisions;
- the transactions;
- the readings put to the custodian;
- the check results;
- anything you could not carry, and why.
