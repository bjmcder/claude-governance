# Concurrency in the governance corpus: coverage and gaps

Date: 2026-10-24. I read GOV, PRIME, DSGN, HW and its sub-profiles, CPS, HDES, all of STND.MPI, and the concurrency provisions and Notes of STND.CODE, CXX, PY, JL, VVUQ, ANNEX, and AGENT. I also grepped the whole corpus for concurrency terms, and found nothing on retries, idempotence, file locking, atomic writes, or databases.

## Coverage table

| Item | Covered by | Fit | Notes |
| --- | --- | --- | --- |
| 1. Data-race freedom, memory models | DSGN.15; HW.11; HW.4 (memory and ordering model in the contract); STND.ANNEX.5, .6, .8 (default: language memory model, no stronger ordering); STND.CXX.23; STND.JL.27; STND.MPI.20, .23 | Full at LVL0 and LVL1; language forms for C++ and Julia only | STND.VVUQ _doc calls a true race a correctness defect under DSGN.15 and HW.11. STND.PY has no threading provision. |
| 2. Synchronization protocols, deadlock, livelock, starvation, progress | DSGN.15 and HW.11 (protocol stated, invariants verified); INTPR.7 (stalled progress reported); STND.MPI.12, .13, .17, .25; HDES.11 (clock crossings) | One model only | DSGN.15 asks only for invariants (VV.10), which are safety properties. Lock order, deadlock freedom, and progress are asked only of MPI message protocols (STND.MPI.12). |
| 3. Atomics, lock-free code, memory ordering | HW.4; HW.11; STND.ANNEX.5, .6; STND.CXX.23; STND.CXX.8 (freestanding row); STND.JL.27 | Partial | No provision asks why an ordering weaker than the strongest is correct, or asks evidence for a lock-free or wait-free claim. STND.ANNEX.6 leaves accelerator atomics in an unspecified order. |
| 4. Thread and process lifecycle | HW.CPU.4 (threads, affinity, quota recorded); HW.CPU.5 (oversubscription reported); STND.JL.5 (pool sizes); STND.MPI.2, .3, .10, .16; DSGN.14 (state lifetime); RSRC.8 | Partial | Nothing covers creating, joining, or detaching threads, daemon threads, or who owns a thread or task. Pool sizes are recorded only for Julia (STND.JL.5) and MPI (STND.MPI.2). Oversubscription is reported, not prevented (HW.CPU.5). |
| 5. Asynchronous and event-driven code | HW.GPU.3 (rank 0); STND.ANNEX.6; STND.MPI.5 second sentence (rank 0); STND.MPI.16; STND.CXX.21; STND.MPI.7 (time limit); INTPR.7 | One model only (accelerators and MPI) | Futures, async and await, event loops, and coroutines are not covered. Nothing covers cancellation. Timeouts appear only in STND.MPI.7. The HW term Capacity covers hardware queues under HW.8; no provision gives backpressure for software queues. |
| 6. Failure in concurrent code | PRIME.4; STND.CODE.7; HW.8 and its HW 1.1.1 Note (informative); STND.MPI.5, .6, .7, .9; HW.GPU.3; STND.CXX.16, .22; STND.PY _doc Notes on STND.PY.28; STND.JL.16 | One model only for halting; partial for exceptions | STND.CXX.22 keeps exceptions inside threads that a runtime starts and inside parallel directive blocks. Outside MPI (STND.MPI.6), no provision covers a worker that dies while others wait, or a failed task whose result is never fetched. The HW Note is informative and speaks of processes, not threads. |
| 7. Liveness beyond MPI (G3) | STND.MPI.12, .13, .17, .25 only; INTPR.7 detects stalls | One model only | Nothing covers queues, pipelines, task graphs, actors, or remote calls. |
| 8. Process-global resources of libraries (G4) | DSGN.14 (no hidden global state); STND.MPI.8 to .11; HW.CPU.3; STND.JL.19; STND.PY.15; STND.JL.22; STND.PY.29; STND.PY.21; STND.CXX.23 | Partial | The principle is at LVL0 (DSGN.14). Named forms exist only for MPI, floating-point state, random states, warnings and error settings, and loggers. Nothing names a library that creates or resizes a process-wide thread pool, installs a signal handler, or owns an event loop. |
| 9. Nondeterminism and reproducibility | REPRO.3; HW.12; STND.ANNEX.5, .6, .8 (run-to-run rows); STND.VVUQ.1, .2, .62, .82, .83; DSGN.17; STND.PY.17; STND.JL.24; STND.MPI.15, .18, .19; STND.CODE.9 | Full at a fixed degree of parallelism; one model only across degrees | STND.MPI _doc Notes say that HW.12 and REPRO.3, which are written for identical recorded inputs, do not reach runs that differ in process count. For thread counts, the analogs of STND.MPI.18 and .19 exist only as STND.JL _doc Notes. |
| 10. Testing concurrent code | STND.VVUQ.1 (thread and process counts in tier 1); STND.MPI.24, .25; STND.CXX.26 (race-detecting build); STND.CODE.9; DSGN.3; HW.15 to .17 | One model only (process counts); one language (race detection) | No language-neutral provision asks for tests at several thread counts. Stress tests, model checking, and deterministic replay are not asked for anywhere. STND.PY and STND.JL have no checker provision. |
| 11. Distributed execution beyond MPI | RSRC.8; DSGN.13; HW.8 Note; STND.ANNEX.6, .7 (resubmission from unaffected inputs); STND.VVUQ.2 second sentence (checkpoint state); HW.7 (confirmation at resumption); HW _doc (wall-time limit); STND.MPI.7 | None (fragments) | STND.JL _doc puts distributed computing outside that standard. Nothing covers partial failure, retries, idempotence, workflow frameworks, or job schedulers. |
| 12. Concurrent access to files and shared data | DSGN.15 in general; STND.MPI.21, .22; AGENT.39 and STND.WPROC (agents and process only) | One model only | Atomic writes, file locks, shared file systems outside MPI's parallel input and output, and concurrent database access are not covered. |
| 13. Real-time concurrency | HW.20; HW.21; CPS.8; PRIME.13; HW.EMBED.3, .6; HW.11 (interrupt handlers); STND.ANNEX.8; STND.CXX.23; STND.CXX.8 | Partial | Deadlines and execution-time bounds are covered. Nothing names the scheduling of several tasks, blocking on shared resources, or priority inversion. HW.20 bounds execution time, not response time under interference. |
| 14. Agents in parallel | AGENT.39, .40; STND.CREW; STND.WPROC; STND.VVUQ.83 | Full | This is agent work, not program concurrency. |
| 15. Concurrency rules in language standards | STND.CXX.15, .22, .23, .26; STND.JL.5, .19, .24, .27; STND.PY.17, .29 | Per language | See B. |

## A. Uncovered, or covered for one model or language only

**Uncovered:**
- Thread and task lifecycle: creation, joining, detaching, and ownership (item 4).
- Futures, event loops, and coroutines; cancellation and backpressure (item 5).
- Distributed execution beyond MPI: partial failure, retries, idempotence, workflow and scheduler semantics (item 11).
- Atomic writes, file locking, and concurrent database access (item 12).
- Justification of memory orderings and evidence for lock-free claims (item 3).
- Stress testing, model checking, and deterministic replay (item 10).
- Priority inversion and multitask response time (item 13).

**Covered for one model only:**
- Completion of asynchronous operations: accelerators (HW.GPU.3) and MPI (STND.MPI.5, .16).
- Halting a whole parallel run: MPI only (STND.MPI.6). The HW Note on HW.8 is informative.
- Liveness of protocols: MPI only (STND.MPI.12, .13, .17, .25).
- Process-global resources of libraries: MPI only (STND.MPI.8 to .11), plus fragments (HW.CPU.3, STND.PY.15, .29, STND.JL.22).
- Declared dependence on the number of workers, and bitwise identity across worker counts: processes only (STND.MPI.18, .19).
- Tests across worker counts and runtime checkers: MPI only (STND.MPI.24, .25).
- Shared-file protocols: MPI's parallel input and output only (STND.MPI.21).
- Timeouts: STND.MPI.7 only.

**Covered for one or two languages only:**
- Race detection in tests: C++ only (STND.CXX.26).
- Stated synchronization: C++ and Julia (STND.CXX.23, STND.JL.27).
- Thread safety stated in each declaration's contract: C++ only (STND.CXX.15).
- Exceptions crossing thread or runtime boundaries: C++ (STND.CXX.22), with a Python Note only (STND.PY _doc on STND.PY.28).
- Recording of thread-pool sizes: Julia only (STND.JL.5).

**Covered model-neutrally:**
- Freedom from data races as a stated, verified protocol (DSGN.15, HW.11).
- Declared variation (REPRO.3, HW.12, STND.VVUQ.82, .83).
- Oversubscription (HW.CPU.5).
- Reporting of stalls (INTPR.7).
- Agents (AGENT.39, .40).

## B. Do the binding MPI provisions and the language rules recur in a model-neutral form?

**The recurrence is real:**
- STND.MPI.5, second sentence: complete each nonblocking operation by a call that returns its errors before relying on it. This is the same outcome as HW.GPU.3 (offloaded work), and both instantiate PRIME.4 at rank 0. STND.CXX.21 holds a third form for release calls that report errors of asynchronous work (STND.CXX _doc).
- STND.MPI.6 (the other units halt, or are told and respond) has a model-neutral reading already: the HW 1.1.1 Note on HW.8 reads it for any run of several processes. That Note is informative.
- The liveness argument of STND.MPI.12 has a hardware analog in HDES.11, and no thread or task form.
- The library rules STND.MPI.8 to .11 instantiate DSGN.14, and so do STND.PY.15, .29 and STND.JL.22.
- The language rules repeat one another:
  - STND.PY.17 and STND.JL.24 are word for word the same except "generator" and "stream", and both restate STND.VVUQ.62 plus "index of the part".
  - STND.CXX.23 and STND.JL.27 are one DSGN.15 rule in two languages.
  - The run records STND.JL.5, HW.CPU.4, and STND.MPI.2 overlap.
  - STND.CXX.26 and STND.MPI.25 are one dynamic-check rule.

Each planned C, Rust, Fortran, and OpenMP standard would repeat three to six of these rules.

**For a LVL1 profile on concurrent and distributed execution:**
- Liveness and the propagation of a software failure are not hardware matters. HW states its purpose as how hardware changes results (HW _doc), and STND.MPI.6 rests on PRIME.4 as well as HW.8.
- DSGN.15 reaches only shared state and invariants. The STND.MPI _doc Notes say a message protocol "shares no state", so DSGN.15 and HW.11 do not clearly ask for completion.
- A selector such as "a component executes as more than one concurrent unit" is decidable under GOV.26.

**Against a LVL1 profile:**
- A binding LVL2 provision is able to instantiate PRIME.4 directly (GOV.19), as STND.MPI.5, .6, STND.CODE.7, STND.CXX.16, and STND.PY.22 do. So LVL1 is not needed to make anything binding.
- The new domain content is about four outcomes: asynchronous completion, execution-wide halt, liveness, and dependence on the degree of parallelism. Everything else is already held by DSGN.14, DSGN.15, PRIME.4, REPRO.3, INTPR.7, HW.8, HW.11, HW.12, HW.CPU.4, and HW.CPU.5. GOV.31 would prune a restatement of those, as the research note's section 5 already concluded.
- HW already owns the concurrency matters of execution paths: HW.11, HW.12, HW.CPU.4, HW.CPU.5, and the default contracts STND.ANNEX.5 to .8. A second profile would need shared-matters tables (GOV.26) and would split those matters between two profiles.
- The methods that make most items checkable are race detectors, model checking, stress tests, deterministic replay, idempotent retry, and atomic rename. GOV.18 bars all of them from LVL1.

**For a model-neutral LVL2 standard:**
- STND.CODE is the precedent: a language-neutral LVL2 standard that the language standards add to (STND.CODE _doc).
- At LVL2 the methods are allowed (GOV.18).
- It can carry binding provisions grounded in PRIME.4 and HW.8, as STND.MPI.5 and .6 are.
- It gives one home to rules that are now repeated or missing: STND.PY.17 and STND.JL.24; STND.CXX.23 and STND.JL.27; STND.CXX.26 and STND.MPI.25.
- It covers the many models that will never get their own standard: futures, event loops, process pools, and workflow frameworks (items 5, 11, 12).

**Against a model-neutral LVL2 standard:**
- STND.MPI is adopted and already holds MPI forms. The new standard must hold only the generic outcome and leave the MPI forms in place.
- LVL2 provisions never instantiate one another; every `instantiates` field in STND points upward. Model standards would reach it only through `refers_to`.
- Its scope partly overlaps STND.CODE.

**Verdict:** The evidence supports a model-neutral LVL2 standard, plus two small LVL1 amendments where an outcome is truly about execution paths. It does not support a LVL1 profile now.

## C. Candidate documents and amendments

**C1. New LVL2 standard: concurrent and distributed execution (working name STND.CONC). Recommended.**
- Scope: threads, tasks, asynchronous operations, process pools, and distributed and workflow execution, in every language and model. Model standards (STND.MPI, the planned OpenMP and offload standards) and language standards add only their own forms.
- Binding provisions:
  - (a) The completion status of each asynchronous operation is obtained, and its error answered, before reliance; no operation is left unobserved at exit (PRIME.4). Closes G2 beyond accelerators and MPI.
  - (b) When one cooperating unit halts on a condition PRIME.4 lists or a fault HW.8 governs, the others halt or are told and respond, and the diagnosis is written first (PRIME.4, HW.8). Closes G1 beyond MPI.
- Default provisions:
  - (c) Liveness: a stated lock order or completion argument, or a bounded wait that reports to the operator (DSGN.15, DSGN.5, INTPR.7). Closes G3 beyond MPI.
  - (d) Libraries take thread pools and executors from their caller, and do not install signal handlers or change process-wide threading settings unless their contract says so (DSGN.14). Closes G4.
  - (e) Each thread or task has an owner that joins or cancels it; cancellation and timeouts are stated; queues are bounded (DSGN.14, DSGN.1, PRIME.4).
  - (f) The dependence of results on the number of workers is declared; partitions independent of the worker count are used where bitwise identity is the criterion; random streams are keyed to the part (REPRO.3, HW.12). This absorbs STND.PY.17 and STND.JL.24.
  - (g) Tests at several worker counts, one among them, and under a race or deadlock checker where the means exists; model checking or deterministic replay at CSQ1 and CSQ0 (VV.1, DSGN.3, DSGN.15).
  - (h) Retries only of idempotent work, recorded under HW.9 and INTPR.9; partial failure recorded; restart from a consistent checkpoint.
  - (i) Results written by atomic replacement; one writer or a stated lock protocol for each shared file or database (DSGN.15).
- Must not restate:
  - PRIME.4, STND.CODE.7, DSGN.14, DSGN.15, HW.8, HW.11, HW.12, REPRO.3, INTPR.7, HW.CPU.4, HW.CPU.5, STND.VVUQ.1, .2, .62, .82, .83, STND.CODE.9.
  - HW.GPU.3 and STND.MPI.5 to .25, which it cites as instances.

**C2. HW amendment (LVL1): promote the HW 1.1.1 Note on HW.8 into HW.8.**
- Amend HW.8 so that, for an execution path of several units computing one result, the path is all the units.
- Closes G1 for hardware faults and exhaustion in every model.
- Must name no technology (GOV.18), and must not restate PRIME.4 beyond the multi-unit reading. Software errors stay with C1(b).

**C3. HW.12 amendment (LVL1).**
- The declaration states which results change with the number of threads or processes that the path records, and by how much.
- This closes the reach gap that the STND.MPI _doc Notes name. STND.MPI.18 then becomes its MPI form.
- Must not restate REPRO.3.

**C4. HW.EMBED amendment (LVL1).**
- Where tasks or handlers share a processor or a resource, the bound of HW.20 includes their interference and blocking.
- Closes the priority-inversion and response-time gap of item 13.
- Must name no scheduling protocol (GOV.18), and must not restate HW.20, HW.11, or CPS.8.

**C5. STND.CODE.3 amendment (LVL2).**
- Each interface states whether concurrent calls are safe. This generalizes STND.CXX.15.
- Must not restate DSGN.1. The thread-safety clause of STND.CXX.15 then becomes redundant.

**C6. STND.VVUQ.62 amendment (LVL2).**
- Streams are keyed to the part, not the worker. STND.PY.17 and STND.JL.24 then reduce to their language facility. This is an alternative to placing the rule in C1(f).
- Must not restate DSGN.17.

**C7. Planned OpenMP and offload standards (LVL2).**
- They give only directive and offload forms of C1(a) to (g):
  - Exceptions inside regions: they cite STND.CXX.22.
  - Thread counts: they cite HW.CPU.4 and HW.CPU.5.
  - Completion of offloaded work: they cite HW.GPU.3.
- They must not restate DSGN.15, HW.11, HW.12, STND.VVUQ.2, or C1.

**Not recommended now: a LVL1 profile, and an amendment to DSGN.15 for liveness.**
- The profile fails GOV.31 on its present content, as B shows.
- The DSGN.15 amendment would change LVL0. C1(c) holds liveness at LVL2 through DSGN.15 and INTPR.7.
- Revisit both if C1 shows that liveness or failure propagation needs LVL1 ground that PRIME.4 and HW.8 do not give.
