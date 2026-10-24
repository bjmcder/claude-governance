# Cold verification of STND.OFFLD 0.2 (2026-10-24)

**Verdict: not ready.** Four blocking items, all small and mechanical (B1 to B4 below). No conflict and no unowned matter found.

Checked by script: `verify` passes eight of eight; `findings.py` gives only the expected g.18 notice for OFFLD.7. Bodies match the reading copy. Modals, banned words, titles, body IDs against front matter, and LVL0 ancestors are clean. Primary sources not read.

## Findings to status

| Finding | Status |
| --- | --- |
| Cold D1 (OFFLD.21), D2 (OFFLD.5) | Verified, text as suggested |
| D3 (onset paragraph) | Verified. Every provision is placed once. "whose three sentences share that onset" for OFFLD.7 comes before any onset is named (should-fix 4) |
| D4 (OMP mapping) | Verified against OMP.23 to .32, and the onsets match |
| D5 (Notes claims) | Partly. The eight listed items are fixed, but the same kinds of error remain elsewhere in the Notes (B1, B2) |
| S1 to S3, S5, S6 | Verified. OFFLD.16 has two modals. OFFLD.7 is kept as a bundle and argued in the Notes |
| S4 (error state) | Verified in the body. The Notes say "processes" share contexts, but a Context is one process's (should-fix 3) |
| S7 | Partly. OFFLD.10 is fixed. The Notes call OFFLD.5 "the instance of STND.CONC.3" while saying the transfer is not a concurrent task (should-fix 2) |
| S8, optionals | Verified for 22 and 23 and for the atomics and no-groups notes. "the offload form of STND.CONC.11" stays on OFFLD.18 |
| Pair obs. 1, 3, 5, 7 to 11, 13, 15, 16 | Verified |
| Pair obs. 4 | Partly. It is done in the Notes but in the indicative (B4) |
| Pair obs. 2, 6, 12, 14 | Verified (obs. 14 is in HANDOFF.md line 54) |

## Delta pairs (3)

- 104 OFFLD.17 / AGENT.39: no conflict, not unowned. AGENT.39 concerns units of agent work; same ruling as 71 and 98.
- 109 OFFLD.17 / HDES.11: no conflict, not unowned. HDES owns clock and reset crossings in a hardware design. They share DSGN.15 only.
- 121 OFFLD.17 / HW.11: no conflict, not unowned. The binding HW.11 has the protocol verified under the memory and ordering model; sentence 1 of OFFLD.17 is a default on what the protocol names and does not relax it. Owner HW (HW.2, row 1), as for pair 73.

I recomputed the set: the 523 of 0.1 plus exactly these three.

## Blocking

- **B1. Factual error in the Notes.** "Work within one queue is ordered" is flat. o1 (H1) says an in-order queue is ordered, and an out-of-order queue (OpenCL) and the SYCL default are not. Write "within an in-order queue".
- **B2. Notes claims beyond the research, not marked.**
  - OFFLD.22: "the run continues at a fraction of its speed with no error" is not in o1. o1 H4 says only "thrashes" and, on legacy systems, "cannot allocate more". Mark it an inference or cut it.
  - "A persisted cache ... is kept for each account of the host and is of limited size" is flat. o3 says the cache is one vendor's, with a common pattern. Write "In one runtime library".
  - "a check for non-finite values alone misses most corruption" is an inference from 1.01 percent. Mark it.
- **B3. Two conditions in one sentence (STND.DRAFT.16).** Same pattern as D1 and D2; the 0.1 review missed it.
  - OFFLD.7 S1: "Where ... states ..., ... no submission through that context after that error". Use "After an error that the documentation of a runtime library states leaves a context or an accelerator unusable, the execution path SHOULD make no submission through that context."
  - OFFLD.10: "after the completion of the last offloaded work that uses it" trails the clause. STND.OMP.24 has the same trailing form, so the custodian may rule it an attribute and not a condition. Otherwise move it to the front.
- **B4. Obligation in the indicative.** The Notes say a resubmission after such an error "goes through a new context or a new process, from inputs held on the host". No provision says this, and the sentence before it says that whether a new context suffices is unverified. Restate it as a consequence of OFFLD.7 ("a resubmission that complies with it cannot use that context") and keep sufficiency of a new context unverified.

## Should-fix

1. OFFLD.5 Notes: o1's OpenCL rule concerns a host buffer that a read writes, not host storage a transfer reads. Mark the source-side hazard.
2. "Instance of STND.CONC.3 ... whose reading side the host does not see as a concurrent task" contradicts the imported Terms, where only device threads are concurrent tasks. Say "the counterpart".
3. Notes: "their errors share its contexts" for processes. Restrict it to components and libraries of one process.
4. Onset paragraph: "STND.OFFLD.7, whose three sentences share that onset" reads before the onset appears. Write "STND.OFFLD.7 (whose three sentences share one onset)".
5. OFFLD.17 S2: "confirm at run time the number that its build fixes" does not say against what. Add "against what the runtime library reports".
6. Notes: "operations ... name their participants for that reason" generalizes one vendor's mask practice (o1). Limit it.

## Optional

- Relabel "the offload form of STND.CONC.11" as "by analogy", as was done for 22.

## Class onsets, bundle, and the RATIONALE

Every provision and sentence is placed once, in agreement with STND.CLASS.10, the Notes of HW, and the OMP forms. OFFLD.7's three sentences rest on DSGN.5 and follow from one event, so the bundle holds. No floor is raised.

The RATIONALE matches 0.2 and the review records, with one stale phrase: "released once after their last use" (OFFLD.10 now reads "after the completion of the last offloaded work that uses it"). Its claim of no conflict agrees with my reading.
