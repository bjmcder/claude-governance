# Cold verification of STND.BUILD, STND.WFLOW, STND.LEAN, STND.SV after the fix passes

Verifier, 2026-10-24. Read: the round brief, the drafting brief, fixpass.md and fixpass-2.md, the diff 0bd2e68..2abe668 for the eleven scripts of the four documents, the four final reading copies, the rehearsed corpus `.scratch/fixpass2/governance-final`, STND.CLASS.10, INTPR, AGENT.25, STND.OFFLD.25, STND.IDENT.18, and the research notes l1 and h1. Scratch: /tmp/claude-1000/verify-final-b/ (pairs-build.md, findings.txt).

## Result

No Defect. One Should-fix (a Notes sentence that overstates a provision). Four Optional items. findings.py on the four documents gives four g.18 review notices (LEAN.21, SV.5, SV.18, WFLOW.7) and no other finding. Each of the four bundles has a Notes sentence saying its sentences apply together, so each notice stays as the brief allows.

## Should-fix

**S1. STND.SV Notes, "adds the content of the language" paragraph, overstates STND.SV.3.** The sentence reads: STND.SV.3 "records with each verification the settings of each simulator that change its verdicts, whether set at that compilation or at the run". STND.SV.3 asks for four-state or two-state mode, the value given to an unknown bit in two-state simulation, the time precision, and each setting that changes how unknown values are evaluated. It does not ask for every verdict-changing setting. A reader would take SV.3 to cover options such as seeds or optimization of the simulator, which it does not, and the sentence reads as a Note stating an obligation that the provision does not hold. Fix: "STND.SV.3 records the mode, the time precision, and the unknown-value settings of each simulator, whether set at that compilation or at the run; STND.BUILD.11 has the repository configuration state every other execution setting of that compilation that is able to change a result."

## Optional

**O1. STND.LEAN Notes, Proof at CSQ0.** The default is described as a theorem "that an independent checker accepts (STND.LEAN.16)", without the condition that LEAN.16 S1 now carries. The next sentences state the no-checker case, so nothing is wrong, but the list reads as unconditional. Fix: "that, where the means of the work include one, an independent checker accepts".

**O2. STND.LEAN Notes, Lean toolchain and upgrades.** The sentences use "build step" and "declared inputs of each build step", but the Terms import only Clean build from STND.BUILD. SV imports Build step. Fix: add "and Build step" to the import sentence. The same sentence says BUILD.1 "counts the Lean toolchain among the declared inputs"; BUILD.1 names "each file, tool, execution setting, and variable", so "counts each tool of the Lean toolchain" is exact.

**O3. MNEM row for LEAN.** STND.IDENT.18 S3 says a mnemonic SHOULD NOT read as a common term of covered work, and S2 asks a letter distance of at least 2 from each mnemonic with the same parent. The reason now argues the first by "reads as the language in covered work", which is a reading. The second holds (I computed the Levenshtein distance from LEAN to each STND mnemonic: the nearest are DEPS, FTN, and HARN at 3) but the row does not say it. Fix: add "letter distance 3 from the nearest mnemonic under STND" to the reason or the rationale. The custodian decides the mnemonic on ratification either way.

**O4. STND.SV Notes, STND.BUILD citation.** "as the Notes of STND.BUILD state" supports the record being HDES.3's design record. The BUILD Notes say the design record is the record of the transformation steps; they do not say that the netlist is an output of a transformation step. The inference is sound. Fix: "as the Notes of STND.BUILD state of the record of transformation steps".

## Item-by-item check (fixpass.md and fixpass-2.md items that touch the four documents)

| Item | Verdict |
| --- | --- |
| fp1 #1 LEAN "Lean toolchain" | Done. No bare "toolchain" is left in the LEAN final copy except in quoted BUILD context. BUILD's Toolchain term is a different term and is untouched. |
| fp1 #2 References (BUILD HDES.3; WFLOW AGENT.25 and OFFLD.25; SV DOCS.11; LEAN CODE.7) | Done. Each cited ID is in the derived References of its document (BUILD lists HDES; WFLOW lists AGENT and STND.OFFLD; SV and LEAN list STND.DOCS and STND.CODE). AGENT.25 says each record is written before the next action other than writing records, which is what the WFLOW sentence says. OFFLD.25 is the record of the results of offloaded work, as WFLOW says. |
| fp1 #4 BUILD.13 INTPR.10 | Done and correct; see the next section. |
| fp1 #5 WFLOW class paragraph | WFLOW.36 from CSQ3 is argued: the CSQ0 row of STND.CLASS.10 is a recorded exercise, which WFLOW.36 does not ask, and STND.CLASS.10 applies the rest of an Article obligation from CSQ3. The WFLOW.35 S2 bundle at CSQ2 is stated as a departure with its reason (provenance and the form in which a person reads it start together). The departure moves a default earlier, not the floor. The no-row list now omits INTPR.12 and names DSGN.3 correctly. |
| fp1 #6 LEAN.3, LEAN.16 | Both now carry a condition first ("Where the means of the work include an independent checker, it SHOULD accept..."), one modal per sentence, and LEAN.3 offers the stated-record alternative. This narrows only. The Notes, the Checkers row, and the rationale agree. |
| fp1 #7 rationales | Each of the four attributes to the custodian only the order of standards and the standing directions, and puts the design in "the drafters' design". The BUILD list "CMake, Automake, and Makefiles" matches the order in HANDOFF.md. No sentence attributes a ruling the custodian has not made. The only ruling cited in the four is the LEAN Notes sentence "the custodian's ruling of 2026-10-23 ... was made for STND.JL", which the Notes of STND.JL support (it rules that JL.14 and JL.15 raise no floor). |
| fp1 #8 SV and LEAN pending-decision phrases | Arguments now stand in place of the decisions. The two SV onset departures are argued, and HDES's Notes, which I read, apply the same INTPR.10 content at CSQ3 under PRIME.15. |
| fp1 #9 DSGN.3 reading (BUILD.12 S1, WFLOW) | Consistent with BUILD.12 instantiating DSGN.3 and with no WFLOW provision instantiating it. |
| fp1 #11 LEAN.25 | The body names no type or operation. The Notes mark `Except`, `Option`, `throw` unverified in l1 (a grep of l1 finds none of them). No provision rests on them. |
| fp1 #12 SV NUMER.26 | The reasoning is consistent with NUMER.26, STND.VVUQ.64, and STND.VVUQ.65 (a stochastic comparison). The remark that a later passing seed leaves a failed seed's defect in place agrees with the determinism direction (a true race is a defect). |
| fp1 #10 SV.17 | Conditional on the means; the Notes say work without them is not blocked. Modals: one per sentence. |
| fp1 #13 WFLOW Terms | Consistent with the STND.CONC definitions of Concurrent task and Asynchronous operation. A manual step is outside both. |
| fp2 #2 LEAN panic | The kernel-defect fact traces to l1 line 51 (S5). The result-type, message, and runtime-setting facts are marked unverified. LEAN.24 does not rest on them. |
| fp2 #3 SV Language edition | All uses renamed. No "Edition in force" is left except the sentence that declines to import it. SV.1's title has four words. |
| fp2 #6 LEAN and SV cite BUILD | Cited and in References. BUILD.1, BUILD.11, and BUILD.23 say what the sentences claim, except for S1 and O2/O4 above. |
| fp2 #8 WFLOW "checkpoint" sentence | Consistent with the WFLOW Restart state row and the reworded STND.VVUQ.2. |
| fp2 #4 MNEM LEAN | See O3. |

## BUILD.13 and INTPR.10

Instantiates reads SIMPL.6, VV.1, INTPR.10, and the body cites exactly those. Sentence 2 cites (VV.1, INTPR.10), so body IDs equal instantiates. The INTPR.10 text ("domain of validity, untested regimes ... are documented") is what sentence 2 asks of a checking build. Mode stays default; INTPR.10 is an Article. The CSQ2 onset follows the CSQ2 row for INTPR.10 and matches STND.CONC.27. The old BUILD.26 contrast sentence was removed, and no stale mention remains: STND.CONC, STDC, and FTN cite BUILD.13 consistently.

`pairs` for STND.BUILD gives 297 pairs; 29 of them are BUILD.13 against a provision on a shared basis INTPR.10 (AGENT.41, HDES.5, .6, .8, .9, .10, HDES.ASIC.3, .5, .11, .12, HW.10, .17, .18, .7, HW.ASIC.4, HW.CPU.3, HW.EMBED.6, HW.FPGA.4, HW.QPU.5, .7, .8, MEAS.5, .6, ML.5, .6, NUMER.12, .16, .18, .20). I read the nine that name HDES, AGENT.41, and HDES.ASIC provisions. Each asks a record to state a limit, uncovered part, or unverified claim; BUILD.13's second sentence asks the same of a checking build, and the two are compatible and do not restate each other (BUILD.13 is about unchecked parts of linked code). I found no conflict.

## Rule checks passed

One modal per sentence and at most three per provision (findings.py: no g.6 or g.11 on these documents). Conditions first. Titles of six words or fewer. Banned words absent from the changed bodies. American spelling and no drafting narration in Notes (grep for "this round", "now reads", "previously", British spellings, em dashes found none). Each rationale ends with the fixed tail (TAIL in apply_build, apply_wflow, apply_lean, apply_hdl; the same two sentences in apply_build_1_0_1 and apply_mnem_lean). No change raises the floor; every changed provision is a default except LEAN.5 and LEAN.25, which keep their stated floor arguments. LEAN.25 now names no type, which narrows nothing.

## Not checked

- The remaining 20 INTPR.10 pairs of BUILD.13 (HW, MEAS, ML, NUMER, HW.*): from their titles, they are documentation duties; I did not read them.
- A fresh rehearsal: I used the rehearsed copy as given and did not rerun `rehearse` or `verify`.
- The research notes beyond the facts the changed sentences cite. The unverified marks in LEAN on the panic and `Except` facts are the notes' own and I did not test them against Lean documentation.
- The ledger rationale "ratified by the custodian" opening is a template that the lead sets at coalescing.
- apply_build_1_0_1.py is unchanged in the diff; I read its tail only.
