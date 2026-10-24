# Dispositions of the reviews of STND.SV 0.1, for draft 0.2

Reviews: `review-cold.md` (cold) and `review-pairs.md` (pairs). Lead decisions of 2026-10-24 numbered L1 to L5 as the lead sent them. Draft 0.2: `draft-0.2.md`; pairs: `pairs-0.2.md` (968 pairs; identical whether or not NUMER 1.3 of this round is applied first). Content module: `tools/amendment-scripts/content_hdl.py`; draft 0.1 module archived at `.scratch/hdl-draft/content_hdl_v01.py`.

Numbering: provisions 1 to 26 keep their numbers. A new STND.SV.27 holds the sentence on seeds across simulators that was the second sentence of STND.SV.26.

## Defects

| Item | Finding | Disposition |
| --- | --- | --- |
| Cold D1 | Onsets of SV.2 s2 and SV.10 s2 at CSQ3 on an argument that does not fit | Taken (L2). SV.2 s2 applies from CSQ2 (DSGN.5, INTPR.10 rows). DSGN.5 dropped from SV.10, which adds to no hardware contract; SV.10 is SIMPL.6 and VV.1, from CSQ3. The claim "as in HDES, because its check runs without a person" is deleted. SV.3 s1, SV.18 s1, SV.20, and SV.21 keep CSQ3 because they add items to the records of HDES.6 and HDES.8, which HDES applies from CSQ3 with the same INTPR.10 content; the Notes state this as a departure from the INTPR.10 row and a decision for the custodian (decision 2 below). |
| Cold D2, pairs C1 | Notes say a simulation race is a data race of STND.CONC and also that simulation processes are not concurrent tasks | Taken (L1). The carve-out is deleted. Notes, paragraph "Concurrency": STND.CONC applies wherever its Term Concurrent task is met (a forked or waiting testbench process; the kernel fits Event loop); a shared variable is a shared mutable object; a simulation race is a data race between simulation processes (Term redefined that way); SV.5 to SV.8 are the form of the protection that STND.CONC.3 asks; a CONC provision with no subject is vacuous; CONC.1 and CONC.2 bind for testbench tasks. STND.CONC.3 is cited in SV.5 and SV.7 (`refers_to`). STND.CONC's Terms are not amended. |
| Cold D3 | SV.13 and the SV.24 delay row rest on "synthesis ignores delays", which h1 marks unverified | Taken (L5). SV.13 s1 now asks only that a behavior of the contract rest on no delay, forced value, or test for an unknown value (h1 answer 8). The ban on delays in the synthesized set is deleted. SV.13 s2 holds the ban on synthesis directives on selection statements. The SV.24 row now reads "a delay in a combinational procedure", which S9 sources. Title changed to "Simulation-only constructs". |

## Should-fix

| Item | Finding | Disposition |
| --- | --- | --- |
| Cold SF1, pairs Obs 6 | SV.25 and SV.26 at CSQ1 on QA.9 | Taken (L2). SV.25 instantiates VV.1 only and applies from CSQ2 on the VV.1 row: the netlist is judged against the verdicts of the description, a reference produced without the netlist. SV.26 is split: s1 (second simulator) rests on QA.9, from CSQ1; s2 is a MAY that admits a proof in its place, applying with s1. The old s2 (seeds across simulators) becomes SV.27, REPRO.3, from CSQ3. |
| Cold SF2, pairs Obs 10 | SV.14 cites HDES.7 outside its scope | Taken (L5). HDES.7 is removed from SV.14; the Notes say that SIMPL.6 holds the wider reach and that HDES.7 and HDES.14 keep their own scope. |
| Cold SF3, pairs Obs 7 | SV.11, SV.12 s2, and SV.19 lack the edition condition | Taken (L5). Each now opens "Where the edition in force provides ...". The Notes give what remains at an earlier edition (a comment that states the priority, and a check in the testbench). |
| Cold SF4 | SV.24 is able to block work | Taken (L5). S1 reports each class "that a tool available to the work reports". A new s2 (INTPR.10, from CSQ2) has the repository configuration name each class that no available tool reports. |
| Cold SF5 | SV.25 wording; it is able to block work | Taken (L5). The condition is now "Where a simulator available to the work reads the netlist that a check of equivalence under HDES.8 compares", with tests "of the verification of HDES.6 that the record of that verification lists". |
| Cold SF6 | SV.20 s1 rests on the unverified vacuity point | Taken (L5). The clock and the disabling condition are removed. S1 records only whether an assertion decides in simulation, in proof, or in both (S2, S7). The Notes say why. |
| Cold SF7 | The onset paragraph is not given per sentence | Taken (L2). The paragraph "Class onset" places every provision and sentence once, as STND.OFFLD does. |
| Cold SF8 | SV.9 s2 is not checkable | Taken. It now reads "a form of sensitivity that includes each variable that the procedure reads". |
| Pairs C2 | SV.23 against STND.VVUQ.62 | Taken (L3). SV.23 s1 now reads "by the hierarchical seeding that the language definition gives it or by a derivation that STND.VVUQ.62 recommends". It instantiates NUMER.24 and refers to STND.VVUQ.62. The Notes say: the streams of a testbench are the matter that NUMER owns through NUMER.24 (NUMER 1.3); the width of the seed is unverified; a narrower seed is a departure from VVUQ.62, recorded under REPRO.7. |
| Pairs Obs 1 | Scope of STND.VVUQ.64 and .65 for constrained random tests | Taken. The Notes treat a constrained random test of a deterministic design as judging a verdict, not a stochastic result, so VVUQ.64, VVUQ.65, and NUMER.26 do not govern it. SV.23 s2 now says "a test that runs at that seed". This is decision 4. |
| Pairs Obs 2 | SV.24 directive row too broad; read-before-write row has no provision | Taken (L5). The row is narrowed to "a synthesis directive on a selection statement", and the Notes say that the directives HDES.11 and HDES.15 rely on are outside it. Read-before-write is now SV.6 s2 (S9); SV.6 is retitled "Writing processes and reads". |
| Pairs Obs 3 | SV.10 s2 against the grain of HDES.9 | Taken. A latch may now be stated "by a rule of HDES.9 that names that procedure" (`refers_to` HDES.9). |
| Pairs Obs 4 | The SV.17 quotation reads against HDES.12 | Taken. The Notes say that the quotation limits what counts as the check of SV.17 and leaves HDES.12 as it stands. |
| L4, pairs C3 | SV.8 against STND.VVUQ.82 and HW.12 | Taken. SV.8 s1 now opens "Other than a reported value whose dependence the record of the simulation declares as STND.VVUQ.82 provides". The Notes separate the two cases. A dependence of a verdict on order is a race, a defect. A declared dependence of a value within the agreement fixed beforehand is variation under HW.12 and VVUQ.82, and STND.VVUQ.83 is cited for agents. |

## Optional items taken

- Unused Terms removed: Reference model, Clock domain, Execution setting, and Constrained random stimulus. The STND.CONC Terms are imported for the Notes.
- No IEEE numbers in Terms (L5). Language definition is now "the published definitions of Verilog and SystemVerilog, in each of their revisions"; the Notes no longer name the standards either.
- Wording changes: "measures the stimulus" becomes "is able to measure the stimulus rather than the design"; "meaningless" becomes "does not compare stimulus drawn from one seed"; the indicative "a true race, which is a defect" now cites the Notes of STND.CONC and STND.VVUQ.83.
- Notes split into labeled paragraphs by group.
- Pairs Obs 11 (HW.6 for the target's power-on property) and Obs 12 (the synthesized set and the verification set now include "the parts of files") taken. Pairs Obs 8: the Notes put a net with several drivers outside SV.6. The two-port memory idiom is not drafted, because it is not in h1.
- Not taken: pairs Obs 5 (HDES.2 rows) is a matter for HDES. Pairs Obs 9 (the composer prints "Adopted") cannot be changed in the composer. The draft files are drafts, and the custodian has ruled nothing.

## Result

`govharness verify` passes every check on the rehearsal of the round script alone, and on a rehearsal of NUMER 1.3 followed by the round script. `findings.py 'STND\.SV'` gives two g.18 review notices, on SV.5 and SV.18; the Notes say that each bundle applies together.

## Decisions for the custodian

1. Mnemonic SV (alternative HDL), unchanged from 0.1.
2. SV.3 s1, SV.18 s1, SV.20, and SV.21 apply their INTPR.10 content from CSQ3, the onset of the HDES.6 and HDES.8 records they add to. This departs from the INTPR.10 row (CSQ2) as a tightening above the floor (PRIME.15). Recommended, so that one record does not carry two onsets.
3. SV.26 s1 rests on QA.9 (CSQ1). Its proof alternative is a MAY that applies with it. Recommended; the alternative is CSQ2 on VV.1.
4. Constrained random tests of a deterministic design are not tests of stochastic results under STND.VVUQ.64 and .65. Recommended, because their verdict is per property and coverage under HDES.6 bounds their runs.

# Dispositions of the verification of 0.2 (`verify-0.2.md`), for draft 0.3

Draft 0.3: `draft-0.3.md`; pairs: `pairs-0.3.md` (941 pairs; 27 fewer than 0.2 because SV.3 s1 no longer cites INTPR.10). Rehearsed with NUMER 1.3 first (`.scratch/hdl-draft/rehearse_with_numer.py`); verify passes all eight checks; findings are the two g.18 notices on SV.5 and SV.18, answered in the Notes. Draft 0.2 module archived at `.scratch/hdl-draft/content_hdl_v02.py`.

| Item | Disposition |
| --- | --- |
| N1 SV.23 and STND.CONC.23 | Taken. SV.23 s1 now keys each stream to the part of the stimulus that it generates, as STND.CONC.23 asks, and derives it from the recorded seed by the language's hierarchical seeding or by a derivation of STND.VVUQ.62. STND.CONC.23 is in `refers_to`. The Notes say that the hierarchical seeding meets CONC.23 where each process or object generates one part of the stimulus and keeps its place whatever the number of tasks; otherwise the VVUQ.62 derivation from a key of the part is the remaining form. |
| N2 SV.26 s1 availability | Taken. S1 now opens "Where a simulator other than the one that decided a property ... is available to the work", and it decides "from the record of that verification". The Notes say a work with no second simulator is outside s1. |
| N3 unmarked language facts | Taken. Three facts are marked unverified in the Notes: that the kernel runs ready processes one at a time, that a testbench starts tasks and waits on others, and that a net with several drivers resolves by the rules of the language. |
| N4 decision 2 | Taken. INTPR.10 is dropped from SV.3 s1, which rests on REPRO.2 from CSQ3. The departure is now stated narrowly for five sentences (SV.18 s1, SV.20 s1 and s2, SV.21 s1 and s2), on the ground that each completes the reading of a verdict or figure that HDES.6 or HDES.8 asks at CSQ3. The Notes say that SV.2 s2 and SV.24 s2 follow the row. SV.18 s3 keeps CSQ3 because it resolves a failure of the HDES.8 check and adds no second route; CSQ2 on VV.1 is put to the custodian. |
| N5 decision 4 | Taken. The Notes now say that VVUQ.64, .65 and NUMER.26 "are read not to govern" a constrained random test of a deterministic design, that the reading goes to the custodian, and that the Notes do not narrow NUMER.26, which applies wherever its own terms are met. NUMER.24 is cited for the construction of independent streams, which holds whether or not the reading stands. |
| N6 order | Handled by the coalesce order (NUMER 1.3 before STND.SV), which the rehearsal wrapper states. The Notes now say that NUMER.2 gives NUMER the matter "from revision 1.3 of NUMER, which this round applies before STND.SV". |
| O1 | Taken. The SV.24 row now reads "a latch that neither the design record nor a rule of HDES.9 states" (`refers_to` HDES.9). |
| O2 | Taken. SV.13 s1 now reads "SHOULD be independent of each delay, each forced value, and each test for an unknown value in the source". |
| O3 | Taken. The Term Combinational process is now "A simulation process that describes logic without storage", so SV.6 s2 no longer reads against it. The Terms used only in other Terms and in the Notes (Time slot, Immediate assertion) stay; Four-state simulation is used in SV.3. |
| O4 | Taken. "bind for" becomes "reach", and "stated by a decision record" becomes "a departure from that default under REPRO.7". |
| O5 | Taken. The fallback is split: a comment and a testbench check for SV.11 and SV.12, and a recorded decision under REPRO.7 for SV.19. |
| O6 | Taken. The Notes say that a design record naming SV.5 to SV.8 as the protection is a record that a declaration is able to cite under STND.CONC.3, and that STND.CONC.26 reaches the protocols of testbench tasks. |

## Decisions for the custodian (as of 0.3)

1. Mnemonic SV (alternative HDL).
2. (a) SV.18 s1, SV.20, and SV.21 apply their INTPR.10 content from CSQ3. Recommended, because they complete the reading of HDES.6 and HDES.8 verdicts at CSQ3. (b) SV.18 s3 applies from CSQ3. Recommended; the alternative is CSQ2 on VV.1.
3. SV.26 s1 from CSQ1 on QA.9, where a second simulator is available, with proof admitted in its place.
4. The reading that STND.VVUQ.64, .65 and NUMER.26 do not govern constrained random tests of a deterministic design.
