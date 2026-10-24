# Cold review: STND.CONC 0.1

Mechanically checked on the 28 files: modals, forbidden words, title length, title uniqueness, body IDs against instantiates plus refers_to; all pass. Not checked: c1, c3.

## Findings

### Defects

1. **CONC.1 second sentence raises the CSQ4 floor (GOV.11).** PRIME.4 forbids silent continuation past an error; a pending operation at run end is not an error, and the Notes concede the sentence "turns a silent loss into a visible one". Because "Asynchronous operation" includes every concurrent task, a CSQ4 script ending with an unjoined thread must register and report it. That is more than one record. Fix: make it a separate default, or narrow it: "Where a run ends while an asynchronous operation whose result the run reported or relied upon has not completed, the run SHALL report that operation to the operator (PRIME.4)."

2. **CONC.2 first sentence narrows PRIME.4 (PRIME.15) and raises the floor.** PRIME.4 admits halt, visible degradation, or a designed safe state. The sentence admits only "reach the parent" or "end the run", so a task that degrades visibly with a diagnosis meets PRIME.4 and fails CONC.2. A signal or interrupt handler is a concurrent task with no parent. The Notes preserve "every response PRIME.4 admits" only for dependent tasks. Fix: "Where a concurrent task detects a failure of a kind that PRIME.4 lists, the task SHALL answer it as PRIME.4 requires and, where its parent relies on its result, the failure SHALL reach that parent (PRIME.4)."

3. **Notes carry an obligation.** The last sentence of the high-assurance paragraph ("A project of CSQ0 or CSQ1 that adopts such a profile records it...") is a requirement. Reword: "Such a profile is one means of meeting STND.CONC.7, STND.CONC.20, and STND.CONC.28."

### Should-fix

4. **Notes sourcing and DOCS.9.** "widely used operating system" and "well-known planetary lander" are notability patterns; use "the POSIX documentation (unverified; c4 did not retrieve it)" and "the 1997 Pathfinder lander". "A qualifier that marks an object as changed outside the program does not order accesses" is not in c2 (c2 only says never use such qualifiers for synchronization); mark unverified. "the common defect of tasks that capture local variables (c4)" overstates c4 (Kokkos, std::execution, asyncio cases); say "the captured-data lifetime hazard of c4". "A queue without a bound turns a slow consumer into an exhaustion of memory" has only a backpressure quotation behind it in c2; cite or mark unverified.
5. **Narration and stale text.** The first Notes sentence ("direction of 2026-10-24 ... drafted before the OpenMP and offload standards") is drafting narration. "put to the custodian at ratification" is stale in an adopted document. The Purpose names standards that do not exist yet; say "planned".
6. **CONC.10 is broad for routine code.** Every blocking read, queue get, and join needs a stated bound from CSQ3. Fix: restrict to "each wait for another concurrent task of the work, or for a condition that one makes true, that is able to last without bound".
7. **CONC.25 first sentence has no escape for targets without a detector.** Fix: "Where the means of the work include a check that detects data races at run time, the tests of each change ... SHOULD run under it and fail at the first detection."
8. **CONC.8 first sentence is ambiguous.** "wait only ... without reaching a suspension point" may attach to the wait alone. Fix: "...SHOULD call only code whose acquisition of locks it knows, and SHOULD NOT reach a suspension point (DSGN.15)."
9. **Missing c4 hazard 6 (no forward progress between iterations).** Nothing forbids a task waiting on another task of a construct that does not guarantee concurrency. Add to CONC.11: "Where a construct does not guarantee that its tasks run concurrently, a task of it SHOULD NOT wait for another task of the same construct (DSGN.15)." The other c4 hazards are covered or deferred (memory spaces to offload; tool gaps only partly by CONC.27). c2's fifteen rules are all reached.
10. **Class paragraph.** It places the CONC.11 argument under the DSGN.15 CSQ2 row ("verification of the invariants"), but a completion argument is liveness. Move CONC.11 to CSQ3 or justify. For CONC.18, CONC.20, and CONC.21, which instantiate HW provisions absent from CLASS.10, say that onset rests on the RSRC, REPRO, and INTPR chain.

### Optional

11. Title of CONC.20 is gerund-initial; use "Worst-case blocking time".
12. CONC.4's second sentence is not about atomic ordering; move it to CONC.3 or retitle.

## Overlaps

| Draft ID | Existing ID | Verdict |
| --- | --- | --- |
| CONC.1 | HW.GPU.3, STND.MPI.5 | adds content (general form) |
| CONC.2 second sentence | STND.MPI.6 | adds content; MPI.6 becomes a special case |
| CONC.3 second sentence | DSGN.15 | restates in part; one protection beside the object is the added content |
| CONC.4 second sentence | STND.CXX.23, HW.11 | restates; CXX.23 is not cited in the Notes |
| CONC.16 second sentence | STND.JL.27 | restates in general form |
| CONC.22 | STND.VVUQ.2, STND.MPI.19 | adds content (across counts) |
| CONC.23 | STND.PY.17, STND.JL.24, STND.VVUQ.62 | restates the language forms; adds independence from task count |
| CONC.25 | STND.CXX.26 | adds content (lock inversion, deadlock) |
| CONC.6 | STND.CXX.15 | adds content |
| CONC.18, CONC.20 | HW.CPU.5, HW.20 | adds content |
| CONC.21, CONC.24 | STND.MPI.18, STND.MPI.24 | parallel forms; no conflict |
| CONC.28 | STND.CLASS.10 CSQ0 row | adds content; no conflict (model fidelity judgment not verified) |

No conflict with a higher provision other than defects 1 and 2.

## Verdict

Not ready to stand as drafted. Fix defects 1 to 3 first: as binding provisions CONC.1 and CONC.2 fail GOV.11 and PRIME.15, and the Notes argument does not rescue them. Items 4 to 10 are short edits. The other 26 provisions pass the drafting and agnostic checks, are checkable by review or a check, and the class onset agrees with STND.CLASS.10 apart from item 10.
