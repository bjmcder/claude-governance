# Cold verification of STND.PERF 0.3 (2026-10-25)

**Verdict: ready for ratification.** No Defect. One Should-fix and two Optional, all in the Notes or in clarity, none touching a provision's obligation.

## Checked by script
- `rehearse` of `apply_perf_round.py` (copy `/tmp/rehearsal-28uck8lj/governance`): appended 2 entries; `verify` passes all eight checks; one g.18 warning.
- `findings.py 'STND\.PERF'`: one review notice, g.18 on STND.PERF.23 (three modals). Nothing else.
- All 26 bodies in the copy appear verbatim in `draft-0.3.md`. Per body: at most one modal per sentence, at most three per provision, no banned word, body IDs equal `instantiates` plus `refers_to`. The `_doc.md` text has no banned word.
- Diff of `content_perf.py` and `apply_perf.py` is the 0.2 to 0.3 change; `instantiates`, `refers_to`, numbers and titles are unchanged.
- The ledger rationale ends with the fixed tail (REPRO.5, ledger entry 15).

## Dispositions
Each does what it says.
- **D1:** the HW.9 sentence is now a reason (it points to PERF.18 and PERF.13). The VVUQ.82 sentence marks the analogy as open in p1 and not adopted (p1 line 45 confirms "Open"). The sequencing sentence is cut.
- **D2:** PERF.21 s2 reads as suggested, with one condition.
- **D3 and S2:** PERF.23 s2 and s3 open with "Where", one condition each. s3 says "check", not "guard".
- **S1, S3, S4, S6, optionals:** the Term, the onset paragraph (PERF.11, 13, 16 together), the citations and marks, "are models for them", "Where a source was read", the PERF.13 and PERF.5 and PERF.4 wording, and the dropped Term are all in the text.
- **S5:** the rationale cites VVUQ.77 in the Notes only. I confirmed that no provision cites it, and that provisions 2, 5, 12, 14 and 26 carry HW.20, HW.22, OFFLD.31 and AGENT.40. The PERF.21 exception is stated.

## The rules in the changed text
- Every named document is in References (verify: references PASS).
- No method, tool, event, product, or version appears in a provision. The means (interleaving, randomizing) are in the Notes only, as p1's means.
- No narration of drafting in the added Notes text.

## g.18 on STND.PERF.23: acceptable
- s1 requires a guard, s2 and s3 say how it judges, under complementary conditions (history shows variation, or is too short). None is applied apart.
- The Notes say "the three sentences of STND.PERF.23 apply together". That meets the round-brief rule.

## Findings
**Should-fix**
1. **Notes, PERF.26 paragraph:** "so other units do not start on it while the measurements run" is an indicative statement of an obligation that AGENT.40 holds as SHALL NOT. Fix: "so AGENT.40 bars the start of another unit that the free resources cannot serve while the measurements run", or end the sentence at "not left free in that sense".

**Optional**
2. **PERF.23 s1 and s3:** s1 still says the verification SHOULD include a guard, while s3 substitutes a check for a short history. Reading s1 to s3 together resolves it, as the Notes say. Fix: s3 begins "Where the performance history is too short to show that variation, the verification SHOULD check ... in place of that guard".
3. **Notes:** the g.18 note says "apply together". The brief's wording is "never applied apart". Fix: add "and none applies apart from the others".

## Could not check
- Primary sources behind p1 and p2.
- Pairs: no change to citations, so I did not regenerate `pairs-0.2.md`.
