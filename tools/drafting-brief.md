# Brief for drafting a LVL2 language standard

## Role

- You are a planning and implementing agent at delegation depth 1, working for the lead agent.
- Network access is not authorized for you. Work only from the local files named here. The research is already done by research agents.
- Do not write to the live corpus `/home/claude/harness/governance`, to `/home/claude/scratch/`, or to another agent's directory.
- You may create and change files only in two places:
  - your own scratch directory, `/home/claude/scratch-<lang>/`;
  - your own content module and apply script, `/home/claude/pkg/content_<lang>.py` and `/home/claude/pkg/apply_<lang>.py`.

## The corpus

**Levels.**

- LVL0 is the constitution. Compact text is in `/home/claude/tools/lvl0.txt`.
- LVL1 holds the profiles: AGENT, NUMER, HW (with its sub-profiles), HDES, CPS, MEAS, and ML.
- LVL2 holds the standards (STND.*).
- LVL3 holds the project instruments.

**Layout.** Each document is a directory `governance/<MNEM>/` (for example `governance/STND/CODE/`) with `_doc.md` and one file per provision, `<n>.md`. Read examples from `/home/claude/harness/governance/STND/CODE/` and `/home/claude/harness/governance/STND/WPROC/`. The standard STND.DOCS, in draft 0.2, is at `/home/claude/scratch/governance/STND/DOCS/`; its reading copy is `/home/claude/scratch/docs-0.2-draft.md`. Read that copy: your standard sits under it.

**Mode.** Each LVL2 provision is either binding or default (GOV.19).

- Mode is forced to binding when its `instantiates` closure reaches PRIME, GUARD, GOV, or a floor ID: REPRO.5, QA.1, INTPR.2, or VV.7.
- A default must therefore not instantiate those. It instantiates provisions of the Articles (VV, REPRO, INTPR, DSGN, SIMPL, RSRC, QA) or of LVL1 profiles.
- `rank` and `waivable` are derived by the harness. Do not set them.

**Class onset (STND.CLASS.10).**

- Obligations of the Articles above the floor apply in full from CSQ3, except the parts in the CLASS.10 table. Work of CSQ4 may omit them.
- Lower governance never raises the floor (GOV.11).
- A provision that instantiates a prime directive is non-waivable at every class.
- State the onset of the defaults in the Notes, as STND.CODE and STND.DOCS do.

**GOV.18.** LVL2 may name languages, libraries, tools, and methods. Keep provisions outcome-based and checkable, though.

- A provision states the outcome a tool or a reviewer decides, for example "a formatter that enforces PEP 8 runs on each change and the change passes it."
- Name a tool only where the outcome cannot be stated without it.
- Put current tool choices in the Notes as the configuration the custodian recommends today, because tools change faster than standards. The custodian's rule is that a project has a linter (governance), and which linter is configuration.

**Other rules.**

- A limit on the number of agents, on the depth of delegation, or on research network access belongs at LVL3 alone.
- Never require a decision of the human owner that LVL0 does not assign (STND.DRAFT.42). Never block work needlessly.

## Drafting rules (STND.DRAFT)

The full rules are in `governance/STND/DRAFT/`. Self-check every provision against them.

- **Modals:** SHALL, SHALL NOT, SHOULD, SHOULD NOT, MAY. Use one modal per sentence and at most three per provision. A provision with three is a bundle that is never applied apart.
- **Conditions:** each condition comes before its clause, one condition per sentence. Write "Where X, A SHALL Y", not "A SHALL Y where X". Avoid trailing "where", "when", "unless", and "other than" clauses.
- **Banned words in bodies:** "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any". Also avoid "some", "several", and "many".
- **Titles:** six words or fewer, not starting with a verb, distinct across the whole corpus. Check with `grep -rh '^title:' /home/claude/harness/governance /home/claude/scratch/governance/STND/DOCS`.
- **Identifiers:** the IDs cited in a body equal `instantiates` ∪ `refers_to`.
  - Same-level IDs (STND.*) go in `refers_to`.
  - Citations to other provisions go in parentheses at the end of each sentence.
  - Do not cite ranges ("STND.X.1 to STND.X.4") in bodies; list each ID.
- **Lists:** a negated modal over an "or" list is flagged for review. Prefer a positive form where you can.
- **Spelling and style:** American spelling throughout. Your own text (Purpose, Notes, provisions) follows STND.DOCS 0.2: plain, specific, and without the patterns in its STND.DOCS.6 table. No "crucial", "robust" as praise, "leverage", "ensure" tails, negative parallelisms, or em dashes.
- **Document sections:**
  - "Purpose and scope", which lists the binding provisions and states that every other provision is a default;
  - "Normative and informative parts" (use NORMATIVE);
  - "Terms" (use TERMS_LEAD plus imports and a table);
  - "Notes", which explain each choice, the custodian's directions, the class onset, and why no binding provision raises the floor.
  The References table is derived; do not write it.

## How to build

- Write a Python content module modeled on `/home/claude/pkg/content7.py` (STND.DOCS). Use `from content3 import P, NORMATIVE, TERMS_LEAD`, with `P(n, title, section, body, instantiates, refs=[...], mode="default"|"binding", defines=[...])`.
- Define a dict with `id`, `title`, `instantiates` (use `["GOV.19", "GOV.48"]` or as fits), `sections`, and `provisions`. Define `NEW_DOCS_<LANG> = [dict]` and `DATE = "2026-10-22"`.
- Write an apply script modeled on `/home/claude/pkg/apply7.py`, with your own `RATIONALE` and `AT` (use the times given in your task).

To rehearse:
1. Copy `/home/claude/harness/governance` to `/home/claude/scratch-<lang>/governance`.
2. Apply STND.DOCS first: `import apply7; apply7.apply(root)`.
3. Apply yours.
4. Run `cd /home/claude/harness && python -B -m govharness verify /home/claude/scratch-<lang>/governance`.
5. Run `python -B /home/claude/tools/findings.py /home/claude/scratch-<lang>/governance 'STND\.<MNEM>'`.

Each `record_transaction` takes about 25 seconds, so run with a long timeout. Fix every finding of class defect, and every review finding you can. Then generate a reading copy with `govharness.derive.reading_copy.compose` (see how `/home/claude/scratch/docs-0.2-draft.md` was made: `compose(corpus, ledger, ReadingCopy(id, name))`). Write it to `/home/claude/scratch-<lang>/draft.md`.

## Deliverable

Your final message:

- the paths of your content module, apply script, and reading copy;
- the verify result and the remaining drafting findings;
- a list of decisions for the custodian, each with your recommendation and reason, numbered and short;
- open questions where the research note left something unverified.

Keep the message under 700 words.
