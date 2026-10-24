# Verification of STND.SV draft 0.2 (2026-10-24)

**Verdict: carry to the custodian after a minor revision. No Defect and no blocking item. Six Should-fix items; items 1 to 3 are best fixed before the custodian reads it.**

## Checked by script
- `govharness verify` passes all eight checks on `rehearsed` and on `rehearsed-numer`. `findings.py 'STND\.SV'` gives only the two g.18 review notices (SV.5, SV.18), which the Notes answer (each bundle applies together).
- All 27 provision bodies in `draft-0.2.md` equal the rehearsed files. Every body ID is a listed ID. There is one modal per sentence, titles are distinct corpus-wide, and no banned word appears in the Notes.
- `pairs` regenerated on both rehearsals is identical to `pairs-0.2.md` (968 pairs). Against 0.1: 34 new (SV.24 x 29 on INTPR.10; SV.27 x 5 on REPRO.3) and 12 gone (SV.10 on DSGN.5; SV.26 on REPRO.3). The new pairs share only INTPR.10 or REPRO.3 with the other provision and conflict with none. SV.27 agrees with HW.12 and NUMER.24 (it forbids relying on a shared seed across simulators). SV.24 sentence 2 adds a naming duty and conflicts with HDES.9 and HDES.10 on nothing.

## Findings to status
| Finding | Status in 0.2 |
| --- | --- |
| Cold D1 (onsets SV.2 s2, SV.10 s2) | Carried out. SV.2 s2 is CSQ2, DSGN.5 is off SV.10, and "as in HDES" is gone. The departure for SV.3/18/20/21 is stated; see N4. |
| Cold D2, pairs C1 (CONC carve-out) | Carried out: carve-out deleted, Terms imported, CONC.3 cited in SV.5 and SV.7. New issues N1, N3. |
| Cold D3 (SV.13 delays) | Carried out; the SV.24 row is narrowed. |
| Cold SF1 / pairs Obs 6 | Carried out (SV.25 CSQ2 on VV.1; SV.26 s1 CSQ1; SV.27 new). See N2, N4. |
| SF2 / Obs 10 | Carried out. |
| SF3 / Obs 7 | Carried out for SV.11, 12, 19. The fallback sentence fits SV.11 only (O5). |
| SF4, SF5 | Carried out. |
| SF6 | Carried out. |
| SF7 | Carried out. Every provision and sentence is placed once (checked by hand). |
| SF8 | Carried out. |
| Pairs C2 | Carried out in text. Not carried out for CONC.23 (N1); owner row needs NUMER 1.3 (N6). |
| Pairs C3 / L4 | Carried out: SV.8 and the Notes separate a verdict (defect) from a declared value (variation). |
| Obs 1 | Carried out as a reading; see N5. |
| Obs 2, 3, 4, 8, 11, 12 | Carried out. SV.6 s2 is sourced (h1 table, "ALL"). |
| Obs 5, 9 | Correctly not taken. The "Adopted" header in the reading copy is the composer's, so send it as a draft. |
| Cold optional items | Taken. |

## New findings, ranked
**Should-fix**
1. **N1. SV.23 against STND.CONC.23.** With no carve-out, CONC.23 applies to a testbench that divides a computation among tasks. It keys each stream to a part of the computation "independently of ... the task that computes the part". The language's hierarchical seeding keys by process and object, and the Notes themselves say it is stable only while the structure is. SV.23 neither cites CONC.23 nor says which wins. Fix: add CONC.23 to `refers_to`, and say in the Notes either that the agent or object that a stream drives is the part of the computation, or that using the language's seeding is a departure under REPRO.7.
2. **N2. SV.26 s1 has no availability condition.** SV.24 and SV.25 carry one, as the lead decision requires. At CSQ1 the provision as written faces a project with no second simulator, and the Notes give only PRIME.8 and a REPRO.7 decision. The body also does not say "from the record", although the Notes' QA.9 argument depends on it. Fix: open with "Where a simulator other than the one that decided it is available to the work", or put the no-second-simulator case to the custodian in decision 3.
3. **N3. Unmarked language facts in the Notes.** The Notes' own rule is that an unsupported fact is marked unverified. Unmarked in "Concurrency" and "Scheduling": that the kernel runs ready processes one at a time (fits Event loop); that a testbench starts tasks and waits on others; that a net with several drivers resolves by the language's rules. The pairs review marked the first two unverified, and h1 holds none of the three. Fix: mark them.
4. **N4. Decision 2 argument.** "One record does not carry two onsets" is not applied to SV.2 s2 (design record) or SV.24 s2 (repository configuration), which each hold two onsets. SV.3 s1 cites REPRO.2 for tool settings. Dropping INTPR.10 from its citation removes the departure for that sentence. SV.18 s3 judges a netlist by simulation or proof against the verification of the description, the ground that puts SV.25 at CSQ2, yet it stays CSQ3 with no reason given. Fix: state the SV.18 s3 reason (it resolves a failure of the HDES.8 check, which is CSQ3), and give the custodian the CSQ2 alternative.
5. **N5. Decision 4 (constrained random tests).** The reading is defensible: NUMER's Term "stochastic method" requires an estimate, and a per-property verdict is not one. Two flaws. SV.23 instantiates NUMER.24, a provision of that same scope, while the Notes say the stochastic provisions do not govern the test. And informative Notes cannot narrow binding NUMER.26. Fix: write "are read not to govern", say that NUMER.24 is cited for the construction of streams, and put this to the custodian in decision 4. No provision stops a failed random test being rerun at a new seed until it passes; STND.CODE.8 and STND.CODE.9 hold regression and seed. That is optional, not a defect.
6. **N6. Order dependency.** The Notes say NUMER "owns" the stream matter through NUMER.24. That is true only after NUMER 1.3 adds the NUMER.2 row. The round script alone leaves it false (`rehearsed` against `rehearsed-numer` differ in NUMER.2). Fix: have the lead order the rounds, or write "is to own".

**Optional**
- O1. Table row "a latch that the design record does not state" omits the HDES.9 rule that SV.10 s2 now accepts.
- O2. SV.13 s1 is a three-item negative list in one sentence (STND.DRAFT.15).
- O3. The Term "Combinational process" is used as "combinational procedure" in SV.6, SV.9, SV.10, and SV.24. SV.6 s2 reads against the Term, because a procedure that reads before it writes is not combinational by the Term. Time slot, Immediate assertion, and Four-state simulation appear only in the Terms and Notes.
- O4. Indicative duties in the Notes: "CONC.1 and CONC.2 bind ..." and "a departure ... stated by a decision record".
- O5. The edition fallback ("a comment that states the intended priority") does not fit SV.19.
- O6. CONC.3 asks a stated protection at the declaration or in a record it cites. The Notes should say that the design record names SV.5 to SV.8 as that protection. CONC.26 (varied schedules, CSQ2) now reaches testbench protocols and is unmentioned.

## Class-onset paragraph
Sentence by sentence it is accurate, and each provision and sentence appears once. SV.5 to SV.8 and SV.19 s1 at CSQ3 follow the CONC.3 precedent. SV.2 s2 and SV.24 s2 at CSQ2 follow the DSGN.5 and INTPR.10 rows. SV.25 at CSQ2 on VV.1 and SV.26 s1 at CSQ1 on QA.9 follow the table. SV.26 is stricter than QA.9, which another actor's run on the same tool would meet; the Notes justify that from S11. Decisions 1 and 3 are fairly put. Decision 2 needs N4. Decision 4 needs N5.

## Not checked
IEEE texts and language facts beyond h1 (the pairs review marked these unverified). Wording against STND.DOCS.9 was read by eye only.
