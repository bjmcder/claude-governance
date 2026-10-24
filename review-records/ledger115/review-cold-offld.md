# Cold review of STND.OFFLD draft 0.1

## Verified by script
- `govharness verify` on the rehearsal: all eight checks PASS. `findings.py`: only two g.18 review notes (three modals in OFFLD.7 and OFFLD.16).
- Reading copy matches the rehearsal files.
- All 31 provisions: mode default; titles at most six words, noun phrases, distinct corpus-wide; body IDs equal instantiates plus refers_to (OFFLD.8 refers to PRIME.4); no banned or retired word from the STND.DRAFT tables; one modal per sentence, at most three per provision. None is binding, so GOV.19 holds. Each instantiates only DSGN, SIMPL, REPRO, RSRC, INTPR, VV, or HW.
- By hand only: conditions, onsets, overlaps, research accuracy.

## Defects
1. **OFFLD.21 has two conditions in one sentence** ("Where a component states a budget", "before it submits"; STND.DRAFT.16). Fix: "Before a run submits the work that a budget of accelerator memory covers, the run SHOULD check that the accelerator memory that the runtime library reports as available meets that budget."
2. **OFFLD.5: the condition follows its clause.** Fix: "Before host code observes the completion of an asynchronous transfer, host code SHOULD NOT write the host storage that the transfer reads."
3. **The onset paragraph leaves OFFLD.17 sentence 2 unplaced.** It cites DSGN.5, so it is CSQ2 by the paragraph's own rule, yet only "the first sentence" is listed and 17 is not in the CSQ3 catch-all. OFFLD.14 and OFFLD.20 have one sentence, so "first sentence" is wrong for them. Fix: list 14, 17, 20 whole as CSQ2, and write "STND.OFFLD.16 (whose three sentences share that onset)" in place of the comma-run "4, 15, 16, whose...".
4. **The OpenMP mapping is wrong in places.** OMP.31 is mapped to OFFLD.26, which has no OpenMP form. OMP.31 maps to OFFLD.2 (proof of device use) and OFFLD.3 (host-only path). OMP.23 sentence 2 maps to OFFLD.1 and OFFLD.3 as well. OMP.32 maps to OFFLD.30, but 30 omits the data-state check (stale or missing data) that OMP.32 and o4 call for. Name the OpenMP-only leftovers (OMP.27 sentence 2; OMP.28 sentence 1, which HW.4 holds model-neutrally).
5. **Notes claims unsupported by o1 to o3 and not marked unverified:**
   - "Device code often has no means to halt, raise an exception, or write a log": only o4 says this, as inference.
   - Migration as a first-submission cost (Notes and OFFLD.31 body): o3 lists first-touch migration as not retrieved.
   - "12 percent of the defects in device code": o1 gives 27 of 217 kernel-execution bugs in five CUDA projects (8.5 percent of all 319).
   - "Deadlocked on every accelerator tested": o1 says at 256 groups, and at 128 on some.
   - Pinned host memory listed as held "across programming models": o1 marks it specific to one runtime, unverified elsewhere.
   - "Generally has no dynamic rounding mode": o2 shows it for one runtime.
   - "Loss of the device" stated flat: o1 rests it on a secondary Vulkan SC extract, concept unverified.
   - "S15 and S16" use o1's numbering, while o3's annotation excludes a different S15. Write "o1 S15" and say the sources differ. No excluded o3 claim is used (checked).

## Should-fix
1. **Terms.** "Parent" and "Boundary contract" are imported and never used. The Terms make device threads concurrent tasks, which brings binding STND.CONC.1 and CONC.2 onto them with no parent named. Add "The code that makes a submission is the parent of the concurrent tasks that execute it," say in the Notes that the reach is intended, and drop Boundary contract.
2. **OFFLD.17.** Sentence 1 has no condition, so it binds all device code. Use "Where device code depends on the number of threads that execute together, ...". Sentence 2 restates the ANNEX.6 limits row; drop it or keep it as the use obligation.
3. **OFFLD.22** says "beyond the capacity of the accelerator", but HW defines a limit that only slows execution as not a capacity. Say "beyond the memory that the accelerator holds".
4. **OFFLD.23.** The Notes say errors share contexts, but the body asks only about memory and queues. Add "and the ownership of its error state" (o1 practice 15).
5. **OFFLD.30.** The race clause restates STND.CONC.25. Restricting races to "memory local to a group" encodes a checker limit that o3 says moves. Use: "invalid accesses to memory, data missing from or stale on an accelerator, or barriers that at least one thread of a group does not reach".
6. **Bundles.** OFFLD.16: naming participants is a remedy a project could adopt alone, so "never applied apart" is not met. Split it, or argue it in the Notes. OFFLD.7 is defensible (three consequences of one event); say so in one Notes sentence.
7. **OFFLD.5** overlaps STND.CONC.3; say in the Notes that it is the transfer instance. **OFFLD.10**: "after its last use" should mean after the completion of the last offloaded work that uses the memory (o1 practice 13).
8. **"Offload form of" labels.** OFFLD.22 / HW.CPU.5 and OFFLD.23 / STND.CONC.18 are analogies. "Each provision takes the onset of its OpenMP form" holds only for mapped provisions: OFFLD.22 is CSQ1 and HW.CPU.5 is CSQ3. Say "by analogy" and limit the sentence.

## Optional
- Note that floating-point accumulation by atomics in unspecified order is declared variation (HW.12, ANNEX.6), not a race, so OFFLD.13 is not misread (o2 practice 9; matches the custodian's direction).
- State that OFFLD.15 to 19 are vacuous where a model has no groups.
- Omitted research items, possibly deliberate: peer access (o1 #15), tests per supported architecture (o3 #8), startup stack check (o3 #16), checked release status (o4), litmus tests (o1 #11).

## Overlaps
| Provision | Existing provision | Verdict |
| --- | --- | --- |
| 1, 2, 3 | HW.19, HW.9, SIMPL.6, VV.8 | Adds policy, confirmation, test; no restatement |
| 4 s1 | HW.4, DSGN.15 | Partial restatement; s2 new |
| 5 | CONC.3, HW.13 | Partial; justify |
| 6, 7 | HW.GPU.3, HW.8, ANNEX.6 | Adds attribution and context state |
| 8 | CONC.2, PRIME.4 | Adds mechanism; acceptable |
| 9, 11 | HW.13, HW.14 | Adds currency and address validity |
| 13 | CONC.3, CONC.4, HW.11 | Adds scope |
| 14 | HW.5, HW.CPU.3 | Adds device side |
| 17 s2 | ANNEX.6 limits, HW.4 | Partial restatement |
| 18 | CONC.11 s2 | Adds permitted route; keep |
| 21, 22 | RSRC.1, HW.8, HW.GPU.4 | Adds pre-check and report |
| 24, 25 | HW.3, REPRO.2 | Adds content |
| 29 | HW.5, STND.VVUQ.4, NUMER.5 | Adds test inputs |
| 30 | CONC.25, OMP.32 | Race clause restates; rest new |
| 31 | HW.22, RSRC.4, HW.GPU.4 | Adds method |
| (cited only) | NUMER.16, NUMER.17, STND.VVUQ.82, HW.12 | No restatement |

## Other checks
- **Floor and tighten-only:** all defaults, no raise. CSQ1 for OFFLD.6 and 22 equals the INTPR.8 and INTPR.7 rows. Other onsets are right except item 3.
- **Agnosticism:** no product, vendor, version, or tool named. The new Terms do not clash with HW, HW.GPU, CONC, or the Lexicon.
- **Timeless:** moving areas are stated as outcomes; only OFFLD.30's list is tied to current tools.
- **Not checkable:** primary sources (the research is extract-based).

## Verdict
Adopt after fixes: five defects, none structural.
