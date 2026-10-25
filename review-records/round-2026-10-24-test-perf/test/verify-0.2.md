# Cold verification of STND.TEST 0.2, STND.WPROC 1.1, STND.CREW 1.1 (2026-10-25)

**Verdict: not ready.** One Defect (mechanical) and eleven Should-fix items, none large. The ruling is carried out in the text. No conflict or unowned matter found.

Fresh rehearsal: `verify` 8 of 8 PASS (the g.18 warn is the old bundle notice). `findings.py` gives nothing on STND.TEST, WPROC.9, CREW.9, CREW.15. Modals, banned words, body IDs against front matter, titles, and the rationale tails are clean.

## Dispositions

- **D1, strict full-suite run: holds, with S1 and S2.** The Term executes each test and lets no earlier verdict stand. TEST.8 limits reuse to a test "in a selection". TEST.10 exempts only a TEST.6 run. WPROC.9 defers a check to a run, not past it.
- **D2: holds, with S3.**
- **D3: holds.** WPROC.9 matches TEST.3 s2, TEST.5, TEST.9 (Omitted tests), and TEST.13. WPROC.11 is unchanged and still reads WPROC.9 as met. WPROC.12 and .13 are untouched.
- **D4: holds.** Traced: development line 0, its child 1, fix branch 1; an update merge takes its target's depth; a main-line merge is a release (TEST.6).
- **Hardware inputs: holds, with O1.** The Term, the TEST.4 row, and the TEST.9 Revision row agree.
- **Secrets:** TEST.8 and the Term agree with STND.BUILD.23 s2 and PRIME.10. TEST.11 does not (S5).
- **Pair 160 (now 161): resolved.** The Term says "not a reference oracle", and the Notes set the line at shared code, data, or method. NUMER.6 and STND.VVUQ.18 still bind the method (O3).

## Defect

**X1. STND.DEPS is named and absent from References.** The Terms import "Integrity digest" from STND.DEPS; the derived References list 17 documents without it. `verify` passes because it reads cited IDs. Fix: cite one STND.DEPS provision in the text, or define the term locally. STND.BUILD lists STND.DEPS.

## Should-fix

- **S1. Skipped or disabled tests escape the run.** An agent that disables a test shrinks the full-suite run. Fix: the Term excludes "a test that a work report states under AGENT.47 as skipped or disabled", so each exclusion reaches the human owner through WPROC.13.
- **S2. Nothing limits a pre-merge run to its selection.** TEST.10 exempts "a run before a merge", and TEST.5 bars no full run at a merge. Fix: TEST.5 adds "Each run before that merge SHOULD hold only that selection, and its record SHOULD state the reason for any other test (RSRC.11)." RSRC.11 already asks this.
- **S3. TEST.5 does not carve out TEST.4 s2** ("from every tier"). Only the Notes settle it. Fix: TEST.5 s1 adds "other than the tests of the second sentence of STND.TEST.4".
- **S4. TEST.3 s1 catches a full-suite run,** which omits skipped tests and so "holds fewer than every test of the full suite". Fix: "Where a run of tests is not a full-suite run".
- **S5. TEST.11 against PRIME.10.** The kept "output that the assertion judged" can hold a secret. Fix: add "other than a secret (PRIME.10)", with PRIME.10 in refers_to.
- **S6. CREW.9 cites a provision that does not select.** TEST.10 limits runs and defers to TEST.3 and TEST.4, and it exempts "a run before a merge", so a self-review run may fall outside it. Fix: "the tests that STND.TEST.3 and STND.TEST.4 select for the change", in the body, Notes, and rationale.
- **S7. Notes fact.** "10 of 32 concurrency cases were defects of the code under test"; t2 H3 says "non-determinism in the code under test". Use t2's words.
- **S8. Onset sentence contradicts itself.** TEST.15 s2 is placed at CSQ2 (INTPR.10), then "STND.TEST.15" is listed among those from CSQ3. Fix: "the first sentence of STND.TEST.15".
- **S9. Indicative obligations in Notes.**
  - TEST: "Quarantine is for a test that the change under review did not make flaky" (no body says it). Cut it and keep "QA.6 still has an actor restore ...".
  - WPROC: "is deferred under RSRC.12 ... to the first merge nearer". Use "STND.TEST.3 and STND.TEST.5 have such a test run at the first merge ...".
  - CREW: "It also receives the record". Use "STND.CREW.15 has it receive".
- **S10. CREW.15 list grammar.** The list "the departures, the skipped or weakened checks, and the ambiguous instructions ... states under AGENT.47, the record of STND.TEST.9 ..., and only the other context" has two "and" joins. Fix: put the record before "and the ambiguous instructions".
- **S11. TEST.19 s1 omits quarantine** (pair 82). Add "places in quarantine", or say in the Notes that quarantine is a disabled check under AGENT.47.
- **S12. Rationales.** WPROC: "loses the merge without a decision of the human owner that STND.WPROC.11 gives" should read "loses the authority of STND.WPROC.11 to merge without a decision". Both rationales justify class by "the text of a default changes", while IDENT.3 asks whether the change "adds, alters, or removes an obligation or permission". Cite that test and drop "no obligation grows" for WPROC.

## Optional

- O1. Add "and of the reference path whose results it compares" to the Verdict input Term, so a reference-path change voids a reused verdict as the TEST.4 row selects.
- O2. TEST.8 s2 joins three conditions with "or". Split it if STND.DRAFT.16 is read strictly. Two TEST.4 table cells end in a trailing "where".
- O3. Add that a test judged by a partial oracle is not method verification under NUMER.6.
- O4. "the studies show a selector to miss" names no source; give t1 H1.

## Class and onsets

- **Minor is right for both.** WPROC.9 widens an exception (a permission); CREW.9 adds a run, and CREW.15 adds an item. Editorial fails the IDENT.3 test. Neither touches a prime directive or principle, so neither is major.
- **No floor raised.** The provisions stay defaults, rest on VV.8, RSRC.11, RSRC.12, QA.2, QA.7, and QA.8, and ask a cited run or record.
- **Onsets hold, with S8.** The reading of TEST.2 against the QA.14 row stands only through its third source, a statement of the repository configuration, which is no mechanism. A tool that derives the inputs is the mechanism QA.14 asks from CSQ2. Say so in the Notes and keep it as decision 4.

## Pair review (by script)

- **Delta:** 374 pairs against 373. The only addition is pair 82 (TEST.13 / AGENT.5, QA.6), and nothing is removed or rebased. The listed 0.2 pairs equal the rehearsed list. No conflict; owner AGENT.5. Gap S11.
- **Amended, 13, each once:** WPROC.9 with CPS.3, HDES.6, HW.7, HW.CPU.3, HW.EMBED.5, ML.7 (42 to 47); CREW.9 with AGENT.28, CPS.3, HDES.6, HW.7, HW.CPU.3, HW.EMBED.5, ML.7 (54 to 60). All match the rehearsed rows. The profile provisions bind evidence before reliance, first drive, fabrication, or a result; a deferral or quarantine at a merge reaches none and relaxes none. No conflict; owner is the profile. AGENT.28 is unrelated. CREW.15 has no profile pair.

## Rationales

Each matches its text and ends with the fixed tail, as entries 138 to 141 do. See S6 and S12.

## Not checked

- Primary sources behind t1 and t2. The Notes figures I traced match the notes (65 percent, 27 bugs, 111 of 665, 170 and 10,000, five systems).
- STND.DRAFT.16 verbatim (I used CUSTODIAN.md).
- Whether the live corpus ends at entry 141. The rehearsal assigns 142 to 145.
