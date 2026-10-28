# Drafting brief: template

A directing agent copies this template into the round's directory, `review-records/<round>/drafting-brief.md`, and completes each part written in angle brackets. The copy in the round is the brief; this file is the template.

## Role and scope

- You draft `<the amendment or the new document>` for the round of `<date>`, recorded in `review-records/<round>/decisions.md`.
- You write only in `<your scratch directory>` and in `tools/amendment-scripts/<content module>.py` and `tools/amendment-scripts/<apply script>.py`.
- You do not write to `harness/governance/`, to another agent's files, or to any record other than your report.
- Network access: `<none, or the authorization that extends to you>`.

## Read first

1. `for-agents/standing-process.md`: the standing process and the directions that hold for every round.
2. `review-records/<round>/decisions.md`: what the custodian decided.
3. The reading copies in `rendered/` of LVL0, STND.DRAFT, STND.IDENT, STND.CLASS, and each document the change touches.
4. A provision of the live corpus: from `harness/`, `python3 -B -m govharness show governance ID`.

## Rules

- STND.DRAFT governs every provision, title, and Note. The self-check is step 2 of the standing process.
- Class onset follows STND.CLASS.10, and no change raises the floor (GOV.11); the standing process, step 3, says how a binding provision is argued.
- The directions of the standing process on agnosticism, restatement, and documentation hold for the text and for the Notes.
- No provision asks a decision of the human owner that LVL0 does not assign (STND.DRAFT.42).

## Building and rehearsing

An amendment is a Python script that applies the primitives of `govharness.workflows.amend` (`replace_text`, `raise_revision`, `record_transaction`) to the root it is given. `tools/amendment-scripts/apply_signers_round_2026_10_28.py` is a recent example of one transaction; `fi_common.py` and `build.py` hold helpers of earlier rounds.

From `harness/`:

```bash
python3 -B -m govharness rehearse governance ../tools/amendment-scripts/<apply script>.py
python3 -B -m govharness verify <copy>
PYTHONPATH=. python3 -B ../tools/findings.py <copy> '<regex of the identifiers drafted>'
```

`rehearse` deletes its copy afterward. To keep one, copy `governance/` into a new directory and call the script's `apply` on that copy.

## Report

Write `review-records/<round>/draft-status.md`: what is drafted, what the drafting decided beyond `decisions.md`, the rehearsal and `verify` results, and each question that only the custodian can answer.
