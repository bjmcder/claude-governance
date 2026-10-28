# Round c of 2026-10-28: cold review

## What I ran

Copy at `/tmp/claude-1000/rvc/governance` with rounds a, d, c (entries 203 to 243; this round 223 to 243). `verify` PASS (the corpus's g.18 warning); `compose --all`: 35 of 71 copies differ, this round's 21 among them; `show` on all 33 changed items; `pairs` for eleven documents and `--amends` GOV.13, QA.11 (none); `findings.py`: nothing new.

GOV.10 to .12, GOV.14, QA.1, QA.12, PRIME.13 are unchanged. Entry 223 follows entries 30 and 46; "minor" is right. GOV.13 narrows one floor halt to four events, as C1(a) rules; nothing else moves the floor. Modals, banned words, titles, identifiers pass. Nothing is written as ruled that was not.

## Defect

**D1. GOV.14 is not intact in STND.CLASS.22.**
- **Fault.** The text says "the obligations of that class SHALL be met … by these steps", and the Notes add "and no more". Past code never gets the new class's contracts or schemas, and the last step falls after the reliance.
- **Fix.**
  - Lead-in: "Before work is relied upon at a more severe class, the work done at the less severe class SHALL meet the obligations of that class through these steps (GOV.14):".
  - Item 3: after "taken as one change", add ", against the obligations of the new class".
  - Last item: make it its own sentence, "Existing source SHALL conform to each default of form or style that the new class first applies to it at the next change that touches that source (GOV.42)."
  - Notes: delete ", and no more".

**D2. The language Notes cite STND.CLASS.22 where it does not apply.**
- **Fault.** STND.CLASS.22 governs reliance at a more severe class, not adoption of a standard. The new sentences also cut the recorded transition ("conforms to the default provisions when a change next touches it") to defaults of form or style, so other defaults reach existing CSQ3 source at once: heavier, not editorial.
- **Fix.** Restore each old sentence and append "; on a reclassification, STND.CLASS.22 governs."

**D3. STND.CLASS.19 now asks for an audit before every reliance.**
- **Fault.** "Before work is relied upon at CSQ2 or a more severe class" loses the old relative sense of "a more severe class".
- **Fix.** "Before work moved to CSQ2 or a more severe class is relied upon at that class, the project SHALL be audited by the auditor of that class (GOV.47)."

**D4. A CSQ3 author can self-review after a context reset.**
- **Fault.**
  - STND.CREW.23 says "A context that holds none of the retrieved content … SHALL count as a session other than that one", unscoped, against AGENT's *Session* ("one continuous run"), so the CSQ3 row of STND.CLASS.18 can count a reset inside the authoring run.
  - *Agent session* ("holds nothing of another run") excludes every agent that loads a tool memory store.
- **Fix.**
  - STND.CREW.23: begin the sentence "For this provision, a context …", in CP14's own words.
  - STND.CLASS Terms: replace *Agent session* with "Session has the meaning that AGENT gives it."
  - CSQ3 row: "An actor other than the author: a human, or an agent, of the author's agent configuration or another, in a session other than each session of the author whose context holds nothing of those sessions except what it reads from the records of the work (QA.7)."

**D5. CSQ3 work falls into CSQ1 by doubt.**
- **Fault.** With no amount stated below CSQ2, "a cost above the amount of STND.CLASS.3" is in doubt for every loss, and STND.CLASS.2 counts it met. "Records CSQ2" also matches an expected CSQ2.
- **Fix.**
  - STND.CLASS.1: "a cost above the amount that STND.CLASS.3 has the classification state".
  - STND.CLASS.3 condition: "Where the class of the project or of a component is CSQ2 or a more severe class,".

## Should-fix

**S1. STND.CLASS.22, items 1 and 2.** Replace "each result whose record lacks" with "each result to be relied upon at the new class whose record lacks", and "each result judged" with "each such result judged".

**S2. STND.CLASS.23: two conditions (STND.DRAFT.16).** Replace with "Where the classification records an expected class, work of CSQ4 SHOULD keep each record of the table of this provision that the provision beside it would ask of the work at that class, as that provision describes it (…)."

**S3. Three Notes are stale after CS9.**
- HW: "a kind that no attribute names" becomes "a kind that Hardware type does not name".
- HW.FPGA: "so HW.EMBED does not bind its firmware" becomes "so no provision of HW.EMBED reaches its firmware".
- HW.ASIC: "and this sub-profile does not bind it" becomes "and no provision of this sub-profile reaches it".

Otherwise the selectors are correct and complete (every sub-profile provision is path-scoped).

**S4. "and owes no record of that class before the reclassification"** in the HW, STND.CODE, and STND.CONC Notes conflicts with STND.CLASS.21 and .23. Replace with "and asks no other record of that class before the reclassification than the records of STND.CLASS.23".

**S5. CLASS_READING credits Agent session and Team to C1.** Move ", and the Terms define Team" into the C5 clause. Under D4, the Agent session clause goes.

**S6. AGENT Notes.**
- "for AGENT.39 the question is closed" becomes "for AGENT.39 the question no longer affects the burden".
- "the authorization relied on and the access descriptor among them, hold for every access of the session and are stated once" becomes "are stated once where they hold for every access of the session, and beside the access otherwise".

**S7. STND.CLASS.7 (CP19).** "before the work is next promoted, released, or relied upon" becomes "before a result of the work is next promoted, or the work is next released or relied upon".

## Optional

- **O1.** "Design for the expected class" can read as an instruction. Use "Expected class in design".
- **O2.** STND.CREW.10: "present to the human owner together, in its next report, the reports of those defects that QA.5 asks".
- **O3.** The Main line exclusion repeats *Development line*; the Notes suffice.

## Promotion path

**CSQ4 project with an expected class of CSQ2.**
- **At CSQ4:** one owner act; the STND.CLASS.23 records; a decision record per choice the expected class drives (.21); no review, audit, or (after D5) threshold.
- **On reclassification:** STND.CLASS.22 with the CSQ2 audit and review.
- **Verdict:** minimal and not circular; no CSQ1 or CSQ0 machinery leaks (an expected CSQ1 adds a design default and the STND.CODE.20 marker). D5 is the one blocker.

**CSQ3 project with no expected class.**
Lighter in promotion, team, reviewer, audit, AGENT.23, .39, STND.THRT.6, STND.CREW.3, .10; heavier only by D2 and STND.CREW.23's SHALL (offset by the fresh-context rule).

## Readings for the custodian

| # | Verdict |
| --- | --- |
| 1 | Keep |
| 2 | Keep |
| 3 | Keep; CSQ2 reliance then means undirected actors or unverified paths |
| 4 | Keep |
| 5 | Keep |
| 6 | Keep, with the custodian's confirmation |
| 7 | Resolve: reclassification only (D2) |
| 8 | Keep; it is the one deferral past reliance (D1) |
| 9 | Keep, with S2 |
| 10 | Resolve as in D4 |
| 11 | Keep |
| 12 | Keep, with S6 |
| 13 | Keep, with S3 |
| 14 | Keep |
| 15 | Keep SHALL, scoped as D4; heavier |
| 16 | Keep |
| 17 | Merge into the record; no choice |

## Pairs

No conflicts beyond D4 (STND.CREW.23 against AGENT) and S6 (AGENT.23 against STND.DFLT.27).
