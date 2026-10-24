# Cold review: HW 1.1.1 (Note on HW.8 for a multi-process run)

## Findings

### Defect
None found in mechanics (verified: References row sorted between STND.DRAFT and STND.VVUQ; title matches STND.MPI; STND.MPI cited nowhere else in HW; revision "1.1.1"; row and ledger rationale follow the 1.0.1/1.0.2 pattern, including REPRO.5 and QA.7 sentences; anchor sits in "## Notes", so the text is informative).

### Should-fix
1. **Class risk (STND.IDENT.3), HW/_doc.md Notes, new sentence 1.** "the execution path that HW.8 asks to halt ... is the whole run" is a flat statement about who the subject of HW.8 is. The Term "Execution path" is "a component together with a hardware type ... and the hardware models, firmware, drivers, runtime libraries, and settings" and says nothing of a run or of several processes. Read as stated, the sentence (a) equates a defined subject with something the Term does not describe, and (b) extends HW.8 to every multi-process run, MPI or not (process pools, forked workers), where HW.8's text binds only the path that detects the fault. Today only STND.MPI.6 (LVL2, MPI programs) requires the survivors to halt or respond. The MPI Notes say STND.MPI.5/.6 ask nothing beyond PRIME.4 and HW.8, so the reading is defensible, but the Note as written could be taken as a changed scope, which is minor, not editorial. Fix: state it as a reading and bound it, e.g. "For a run of several processes that compute one result together, HW.8 is read as asking the whole run to halt, degrade visibly, or transition to a designed safe state; STND.MPI.6 states this for a program that uses the Message Passing Interface." Then the Note confirms the existing reading instead of defining the path. If the custodian wants the stronger "path is the whole run" meaning, that is a minor amendment.
2. **Overstatement, sentence 2.** "A process that halts alone leaves the others waiting on it" is not always true (independent processes) and does not match STND.MPI.6, which also lets survivors receive notice of the halt and respond as PRIME.4 requires. Fix: "A process that halts while the others wait on it leaves a silent hang."
3. **Revision-history row.** "as STND.MPI reads it" is not what the Note says (it says HW.8 is read this way and that STND.MPI.6 states the halt). Fix: "...is the whole run, citing STND.MPI.6, and References lists STND.MPI; no obligation changes." Mirror in the script's ROW and RATIONALE (the rationale repeats the phrase).

### Optional
4. Sentence 3 covers only STND.MPI.6's first sentence (halt reaches others). Adding "and that the diagnosis is written first" is not needed; leave it.
5. "compute one result together" is broader than the MPI term "parallel execution" (processes of one start of an MPI program). Acceptable once fix 1 scopes it; otherwise use "a run of several processes started together".
6. Ledger rationale could add "Class: editorial, because the Note states a reading that STND.MPI.6 already applies and no obligation changes" (STND.DFLT 1.0.2 precedent, ledger entry 39). HW's own 1.0.1 and 1.0.2 rationales omit it, so not required.

## Checks passed
- Accuracy: Note matches HW.8 (halt, degrade visibly, safe state), PRIME.4, and STND.MPI.6 (halt of one process reaches the others); no misstatement besides finding 2.
- Informative: no SHALL/SHOULD/MAY, no imperative, no drafting narration.
- Prose: American English; no STND.DOCS.9 pattern found; no vendor or tool named beyond the standard's own subject.
- Not checked: script execution (no rehearsal run), the govharness checks, ledger hash.

## Verdict
Not ready as drafted; ready after fixes 1 to 3. The mechanics are sound, but the first sentence reads as redefining the subject of HW.8 and extending it beyond MPI runs, which risks misclassing the change as editorial. Recasting it as a scoped reading that points to STND.MPI.6, and correcting the history row, keeps it editorial.
