# Deep review of 2026-10-28: shared brief

Every reviewer reads this brief first. You are an agent of another configuration than the author of the corpus, and you read cold.

## The repository

- REPO is `/home/brianm/projects/utils/governance-harness`, branch `deep-review-2026-10-28`.
- The corpus, the system of record, is `REPO/harness/governance/`: one directory per document, one file per provision, a `_doc.md` per document, and the hash-chained ledger `ledger.jsonl` (202 entries).
- A reading copy of each document is `REPO/rendered/<ID>.md`. Read those; go to the source only for front matter.
- The harness is `REPO/harness/govharness/`, Python 3.11 or later, standard library only. From `REPO/harness/`, these commands are read-only:
  - `python3 -B -m govharness show governance ID`
  - `python3 -B -m govharness find governance WORDS`
  - `python3 -B -m govharness context governance WORDS`
  - `python3 -B -m govharness verify governance`
  - `python3 -B -m govharness pairs governance ID`
- `REPO/CUSTODIAN.md` holds the custodian's standing process and directions. Read it: the directions on agnosticism, no restatement (GOV.31), and documentation hold for every proposal you make.

## What the custodian wants

1. **Human interactivity only when warranted.** The human owner and operators should need a high level of interactivity only when they ask for it, or when the work is of consequence class CSQ1 or CSQ0 (CSQ0 is the most severe, CSQ4 the least; STND.CLASS).
   - Report every place where work of CSQ2, CSQ3, or CSQ4 needs a decision, approval, record, signature, review, or attention of a human that the human did not ask for. "Each X is recorded and adopted by the human owner" at every class is the kind of thing to find.
   - The floor (GOV.11) and the prime directives (PRIME) hold at every class. A burden that a floor provision imposes is still reportable, but say that the fix touches the floor.
   - **Most work is CSQ3 or CSQ4** (custodian, 2026-10-28). Weigh every finding by its effect on CSQ3 and CSQ4 work first: the defaults, onsets, and burdens that those classes meet are what matter most. Machinery that reaches only CSQ1 and CSQ0 is lower priority, unless it leaks into CSQ3 and CSQ4.
   - **Work is promoted rather than begun at a severe class.** It usually starts at CSQ3 or CSQ4 and is promoted to a more severe class later, rather than being developed at that class from the start.
     - This is a common pattern, not a rule: some work starts at a severe class.
     - Where a promotion is known in advance, design decisions take it into account. Check whether the corpus lets a project record an expected class, and whether design-level provisions (DSGN, STND.CODE, and the language and hardware standards) then ask the design to anticipate it, without imposing the severe class's records before the promotion.

     So the promotion path is in scope:
     - what a promotion owes, retroactively, of work done at the lower class;
     - whether CSQ3 and CSQ4 work keeps the few cheap records that make a later promotion possible without rework;
     - whether the promotion rules (GOV, STND.CLASS, the `promote` transaction) are clear, proportionate, and free of blockers.
2. **No blockers.** Report anything that halts or deadlocks an agent:
   - circular or unsatisfiable requirements;
   - a referral or halt with no one to resolve it;
   - an undefined term on which an obligation turns;
   - a check that no one is able to perform.
3. **No needless complexity.**
   - Restatement or duplication across documents (GOV.31).
   - Overlapping or conflicting provisions.
   - Provisions that no reader is able to apply.
   - Tables or machinery out of proportion to their purpose.
4. **Gaps, inconsistencies, defects.** Missing coverage that a reader would expect, contradictions between documents, wrong or stale citations, and text that no longer matches the corpus around it.
5. **The harness is an optional convenience.** It is a lightweight interface that an agent uses to query the corpus. It is installed in code projects and has no enforcement layer: since unit 0018 it derives no environment configuration and installs no hook. No work depends on it (GOV.38). A provision that makes conformance depend on running the harness is a finding.

## Out of scope

- The g.18 warning that `verify` prints.
- The signature feature: the signer register, the anchor file, and STND.HARN.10 to .13. It is deliberately unadopted, so report on it only where it burdens work that has founded no register.
- Drafting-style nits that change no meaning.
- Per-framework annexes for offloading, which the custodian rejected.

## Rules

- Write only your report. Edit no other file in REPO.
- Keep scratch files in a new subdirectory of `/tmp/claude-1000/`.
- Use no network unless your own brief allows it.
- Never keep credentials, disclose secrets, or circumvent a paywall. After a failed fetch, try no workaround and use no mirror or cache.

## Report format

Write `REPO/review-records/deep-review-2026-10-28/<your name>.md`:

1. **Scope and method**, at most 150 words: what you read and ran.
2. **Findings**, at most 40, most severe first, as a table with columns:
   - **ID:** your prefix and a number.
   - **Severity:** Blocker, High, Medium, or Low.
   - **Kind:** burden, blocker, complexity, gap, inconsistency, or defect.
   - **Location:** provision or file identifiers.
   - **Evidence:** the exact text at fault, short.
   - **Proposed fix:** exact replacement text where it is short, or a precise direction.
   - **Custodian decision:** "no", or the one question that only the custodian can answer.
3. **Systemic observations**, at most 300 words: patterns that cut across findings.

Prefer fewer, well-evidenced findings over many weak ones. Check each finding against the text before you report it. Then return a summary of at most 150 words: counts by severity, and the five most important findings by ID.
