# Cold review of STND.SV draft 0.1

## Verified by script
- `govharness verify` on the rehearsal: all eight checks PASS. `findings.py 'STND\.SV'`: only two g.18 review notes (three modals in SV.5 and SV.18); the Notes say each bundle applies together, so both stay.
- Every provision body and the Notes in the reading copy match the rehearsed files (0 mismatches).
- All 26 provisions: mode default; titles 2 to 5 words and distinct corpus-wide; one modal per sentence, at most three per provision; every body ID is in `instantiates` or `refers_to`; no lowercase modal or banned qualifier. No capital modal in the Notes. No vendor or product name anywhere (grepped).
- Terms: the imports exist in HDES and STND.CODE. Not used in any provision or in the Notes: Reference model, Clock domain, Execution setting; Constrained random stimulus is defined and never used by that name.
- Notes quotes, figures, and attributions checked against h1 (the "not defined in the language standard", "most worrying thing", X-pessimism, 98 percent, 18,000 hours, seven programs and three crashes, 15 and nine defects, "so inconsistent", "none of these implementations", full_case pitfalls). All present. Counts of 15 and nine are in h1 as digits and words, fine.
- G1 to G4 are covered: G1 by SV.21, G2 by SV.15, G3 by SV.24, G4 by SV.1 and SV.2. SV.18, SV.20, and SV.21 add to HDES.8 and HDES.6 only; HDES.11 is cited and not restated.
- By hand only: onsets, overlaps, the CONC decision, and the unverified-points test.

## Defects

**D1. Class onset: SV.2 (second sentence) and SV.10 (second sentence) apply DSGN.5 content at CSQ3 with an argument that does not fit.**
STND.CLASS.10 gives CSQ3 "every obligation in full except each part in the table", and the table puts the DSGN.5 and INTPR.10 parts at CSQ2. So the CSQ2-only reading is the one the table gives. STND.CONC and STND.OFFLD both follow it: a part that rests on a row applies from the row's class (OFFLD.7, 12.1, 14, 17.2, and 20 on DSGN.5 are CSQ2). The earlier onset is not unlawful in itself. It is above the floor, so GOV.11 is not breached, and PRIME.15 admits a tightening. HDES also does it, but HDES argues it for its own provisions (HDES.4, .12, .15 cite DSGN.5; HDES.6, .8, .9 cite INTPR.10), and HDES.5 alone is CSQ2. The draft's "as in HDES" is right for only part of the list.
- SV.3, SV.18, SV.20, SV.21 add records to HDES.6 or HDES.8, which instantiate INTPR.10 and apply at CSQ3. CSQ3 is correct for these, and the Notes should say that reason.
- SV.2 adds to HDES.3, which cites only REPRO. Its first sentence (construct subset) rests on REPRO.2 and is CSQ3. Its second sentence (constructs a tool documents as unsupported) is a DSGN.5 and INTPR.10 "known defects of the external component" record that no HDES provision carries. It is CSQ2 by CONC and OFFLD practice.
- SV.10 adds to no HDES provision. A latch kept in the design record is SIMPL.6 content, and DSGN.5 is cited without reason.
- The stated reason "its check runs without a person and the failure is silent" is HDES's reason for mechanically checked provisions. SV.2, 3, 18, 20, and 21 are records that a reader checks. The reason does not carry them.

Fix: SV.2 sentence 2 from CSQ2. Drop DSGN.5 from SV.10 and its second sentence (CSQ3 under SIMPL.6). Replace the sentence in the Notes with "SV.3, SV.18, SV.20, and SV.21 add to HDES.6 and HDES.8, which instantiate INTPR.10 and apply from CSQ3, so they add no onset". Delete the claim that SV.2 and SV.10 tighten "as in HDES". If the custodian wants SV.2 sentence 2 at CSQ3, put it to him as a decision with its own argument. Do not write that he ruled it.

**D2. The CONC decision is inconsistent with STND.CONC's Terms and Scope, and the Notes carve out a part of CONC.**
- CONC's Concurrent task is "a thread, task, coroutine, process, ... or other sequence of execution of the work that runs, or is able to run, while another of the same run has not completed". CONC's Scope covers "every language", event loops, and the processes of one run. Testbench processes, forked threads, and event-driven simulation processes meet the definition.
- The Notes say a simulation race "is the form that a data race of STND.CONC takes" and also that simulation processes are not concurrent tasks. A data race is defined only between concurrent tasks, so the two statements contradict each other.
- A testbench that forks, or uses a semaphore or mailbox, has parents, failures, and locks. STND.CONC.1 and STND.CONC.2 bind at every class and have a subject there. A carve-out in an LVL2 Note cannot narrow them, and PRIME.15 forbids narrowing scope.
- The reason given, "no subject for pools and locks", is not an exclusion. A provision with no subject in a work is vacuous there, as CONC's own Notes treat such cases.

Fix: delete "this standard does not make each simulation process a concurrent task". Say that STND.CONC applies to each sequence of execution that meets its definition, among them processes of a testbench and of a simulation, that SV.5 to SV.8 are the form STND.CONC.3 takes for the ordering that the language gives, and that a provision of CONC with no subject in a given work is vacuous. Add STND.CONC.3 to `refers_to` of SV.5 and SV.7 if the form is claimed.

**D3. SV.13 rests on a claim h1 marks unverified.**
h1 supports only that one simulator ignores timing checks and reads min:typ:max as typical. "Synthesis ignores delays" is general knowledge, marked `[unverified]`. The Notes say so, yet SV.13 sentence 1 ("a delay ... not being among them") and sentence 2 ("no delay in a procedure") depend on it. The same row feeds SV.24 (Scheduling, "a delay in a procedure of the synthesized set").
Fix: keep outside the provisions. Restate SV.13 to what is sourced: "Each behavior that the contract states SHOULD NOT rest on a delay, a forced value, or a test for an unknown value (VV.1)", and delete sentence 2's delay ban (the ban on a delay used to order processes stays in SV.7). Remove the delay finding from the table in SV.24 or limit it to a delay in a combinational procedure, which h1 sources to a tool's documented behavior (S9).

## Should-fix

1. **SV.25 and SV.26 onset (CSQ1 on QA.9).** The analogy is unsound for SV.25. QA.9 asks that a reported result or a release deployment to hardware be regenerated from its record by another actor or system. SV.25 produces a new verdict on a different artifact (the netlist) and compares it with the verdict on the description. That is VV.1 evidence against a reference produced without the thing it judges, which is the VV.1 row of CLASS.10 and applies from CSQ2. HDES.8 itself accepts a netlist simulation alone at CSQ3, so a CSQ1 onset for SV.25 is not proportioned. For SV.26 the analogy holds only for its simulator route (another system re-decides a verdict from its record; submission for fabrication resembles a release to hardware). The proof route is not regeneration. Fix: SV.25 from CSQ2 under the VV.1 row. For SV.26, either CSQ2 under VV.1 or split the sentence by route and state in the Notes that only the simulator route rests on QA.9. Put the chosen onset to the custodian. SV.26 sentence 2 (REPRO.3) needs its own onset stated; CSQ3 is natural.
2. **SV.14 cites HDES.7 outside its scope.** HDES.7 applies "where a design performs operations ... that approximate a real-valued computation". SV.14 covers every extension, truncation, and sign change. Drop HDES.7 from `instantiates` and from the body. SIMPL.6 holds the outcome.
3. **Edition-conditional text missing.** SV.11 (`unique` and `priority` qualifiers) and SV.19 (concurrent assertions) cannot be met in an edition that lacks the construct. SV.9 and SV.7 carry "where the edition in force provides". Add the same condition to SV.11 and SV.19.
4. **SV.24 can block work.** It asks that the named static checks "report each finding of each class" with no condition. Add "that a tool available to the work reports" and have the design record name any class no tool reports (STND.DEPS and STND.CODE.4 already work this way).
5. **SV.25 wording.** "A set of the tests of HDES.6 that the design record states": HDES.6 states no list of tests in the record. Say "a set of tests of the verification of HDES.6 that the record of that verification lists", and add "where a simulation of the netlist is available to the work", so the default does not block work.
6. **SV.20 sentence 1 (clock, disabling condition) rests on h1 answer 18**, whose vacuity half the note says "rests on general knowledge" `[unverified]`. The Notes argue only the proof-constraint half. Either cite the support for the clock and disabling condition, or cut sentence 1 to the simulation, proof, or both record that S2 and S7 support. A disabling condition is where vacuity enters, so keeping it makes the "no provision on vacuity" statement doubtful.
7. **Onset paragraph is not sentence-level as in OFFLD.** It does not place SV.2 s1 against s2, SV.18 s3, SV.23 s2, SV.26 s2, or SV.24 (DSGN.3). State each once, as OFFLD's paragraph does.
8. **SV.9 sentence 2** ("the form of the language that includes them all") names no construct and is not checkable by a reviewer reading only the provision. Say "a form of sensitivity that includes each variable the procedure reads".

## Optional
- Term "Language definition" names IEEE 1364 and 1800. They are not versions, but "the published definitions of Verilog and SystemVerilog" meets the no-numbers direction with no loss.
- Remove the three unused imported terms and the unused "Constrained random stimulus", or use them.
- SV.22 basis is "derived from S3" (h1 row "Functional coverage"); the Notes say so. Acceptable as a default. Soften "measures the stimulus and not the design" to "can measure".
- Notes: "simulation of one seed across simulators is meaningless" is stronger than h1 (S8 plus unverified summaries). Use "does not compare".
- Notes: "a simulation race is a true race, which is a defect" reads as an obligation in the indicative. Rephrase to cite STND.VVUQ.83 for the rule.
- Notes run to about 2,900 words in a dense paragraph style. Splitting by group (as OFFLD does) would ease review.

## Unverified points held out of provisions
Checked: vacuity, state machines, interfaces, packages, parameters and generate, and reset styles hold no provision. SV.8 mentions resets only for time-zero ordering (S1). The only leak is D3 (delays) and, partly, SV.20 (Should-fix 6).

## Mnemonic
SV is the established abbreviation (file extension of SystemVerilog). It has letter distance 2 from JL and PY and at least 3 from the rest, so STND.IDENT.18 holds on either test. Sievert: the corpus text has no use of "Sv" for the unit (grepped), and as an identifier `STND.SV` it cannot be read as a unit. Risk is low. SV omits plain Verilog; the draft's alternative is a decision for the custodian.

## Overlaps with HDES (table)
| SV | Holder | Verdict |
|---|---|---|
| 3 | HDES.3 (settings and seeds of tools) | Adds four-state or two-state, precision, unknown-value options; no restatement |
| 15 | HDES.12 | Adds only what counts as evidence (G2) |
| 18 | HDES.8, HDES.9 | Adds the mode and the failure analysis; no restatement |
| 21, 22 | HDES.6 (named measure, contract mapping) | 21 adds what a measure counts. 22 is partly HDES.6's "properties of the contract"; the addition is "apart from stimulus code" |
| 24 | STND.CODE.4, HDES.9 | Adds the classes; condition missing (SF 4) |
| 23 | STND.CODE.9, STND.VVUQ.64 | Adds derivation of streams and the record of a change |
| 14 | HDES.7, HDES.14 | HDES.7 does not apply (SF 2); HDES.14 untouched |

Not checked: the revision-history claims about declaration initializers at time zero (Notes, SV.8) and the signed-extension test, beyond their presence in h1; IEEE texts, which h1 did not retrieve.

## Verdict
Revise. The text is sound and well sourced and the rules hold, but D1 (onset), D2 (CONC carve-out), and D3 (unverified delay claim in SV.13) are broken rules. Fix the three defects and the first six should-fix items, then re-verify. No second cold review is needed unless the onsets of SV.25 and SV.26 change from what is proposed here.
