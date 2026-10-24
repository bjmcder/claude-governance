# Brief: final cold verification before ratification

You are a read-only verifier at delegation depth 1. No network. Do not change any file except your one report file. Run no scripts that write; read-only scans (grep, python that only reads) are fine.

## Context
- The combined rehearsal applies, on a scratch copy at `/home/claude/scratch-all/governance`: STND.DOCS 0.4 (entry 100), STND.INSTR 1.4 (101), STND.CXX 0.3 (102), STND.PY 0.3 (103), STND.JL 0.3 (104). `verify` passes; only g.18 (three-modal bundle) review findings remain, plus g.14 notes on numbers in names.
- Reading copies: `/home/claude/scratch-all/rc/`. Provision files: `/home/claude/scratch-all/governance/STND/<MNEM>/`. Constitution: `/home/claude/tools/lvl0.txt`. Drafting rules: `governance/STND/DRAFT/`. Class onset: `governance/STND/CLASS/10.md`.
- Each draft answers a prior cold verification. For each, compare the draft against that verification and the drafter's disposition file.

## Rules to check against
- Binding vs default (GOV.19): mode is forced to binding when the `instantiates` closure reaches PRIME, GUARD, GOV, or a floor ID (REPRO.5, QA.1, INTPR.2, VV.7). Binding provisions at CSQ4 must not raise the floor (GOV.11): each must ask only what PRIME/GUARD/floor already require, or cost only wording (agent-only rules under GOV.48).
- Drafting: one modal per sentence, at most three per provision; each condition before its clause, one per sentence; no "such as", "for example", "can", "will", "must", "is to", "need not", "significant", "any" in bodies; titles at most six words, not verb-initial, distinct; body IDs equal instantiates ∪ refers_to; Notes hold no obligations and no drafting narration; American English; no STND.DOCS.9 patterns in the drafts' own prose.
- Shared rules across the three language standards (`/home/claude/tools/revision-brief-0.3.md`) must match in substance.
- Never require a decision of the human owner that LVL0 does not assign (STND.DRAFT.42).

## Report
Write your report (at most 900 words) to the path given in your task. Sections: Findings (Defect / Should-fix / Optional, each with location and a concrete fix), Prior findings (one table row per prior finding: Resolved / Partly / Not), Verdict (ready to present for ratification, or not, and why). Report only what you verified; mark anything you could not check. Your final message is the report text.
