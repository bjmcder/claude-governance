# Round c of 2026-10-28: cold verification

## What I ran

Rounds a, d, and c applied to a fresh copy, `/tmp/claude-1000/rvc2/governance` (entries 203 to 243):
- `verify` passes, with only the g.18 warning the corpus already carries;
- `compose --all`: 35 of 71 copies differ from `rendered/`; 12 differ from my first copy, all revised text;
- `pairs` is unchanged for STND.CLASS, STND.CREW, AGENT, HW, STND.CODE, and STND.CONC.

## Defects

All five are closed.

- **D1, GOV.14 before reliance.** STND.CLASS.22 meets the obligations before reliance, and the review runs against the new class. The one deferral is a form or style default "on whose outcome no reliance at the new class turns".
- **D2.** The old sentences are restored, and the STND.CLASS.22 clause is appended.
- **D3.** "first relied upon at that class": the audit falls once per move.
- **D4.** STND.CREW.23 now reads "For this provision", and *Session* is AGENT's "one continuous run". A reset inside the authoring run is still the author's session, so a CSQ3 author never reviews its own work.
- **D5.** Below CSQ2 there is no stated amount, so the cost limb fails and STND.CLASS.2 does not reach it.

## Should-fix

S1 to S7 are done.

## Findings

**V1 (Defect, from my S1 text).** In STND.CLASS.22, item 2's "each such result" picks up item 1's "whose record lacks an input of REPRO.1".
- Text: "the label unverified on each such result judged against criteria set after it was seen (QA.12);"
- Replacement: "the label unverified on each result to be relied upon at the new class that was judged against criteria set after it was seen (QA.12);"

**V2 (Optional, from my D4 text).** In the CSQ3 row of STND.CLASS.18, "whose" can attach to "the author".
- Text: "in a session other than each session of the author whose context holds nothing of those sessions"
- Replacement: "in a session, other than each session of the author, whose context holds nothing of the author's sessions"

**V3 (Should-fix).** Readings 1, 2, 3, and 5 are true open choices. Reading 4, the CS9 residual, is not: its text says "nothing in this round decides it", and "Left to the lead" already holds it.
- Text: "these five are the choices the rulings leave open"
- Replacement: "these four are the choices the rulings leave open"
- Also: move item 4 to "Left to the lead", and renumber.
