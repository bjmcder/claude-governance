# O4: What the corpus already says about accelerator offload

Role: research agent. Date: 2026-10-24. Read-only on the corpus; no web retrieval. Read in full: rendered/HW.md (1.1.1), HW.GPU.md, HW.CPU.md, NUMER.md (1.2), STND.CONC.md, STND.OMP.md. Read in part: STND.ANNEX (Notes, STND.ANNEX.6), STND.VVUQ (1, 2, 4, 7, 8, 62, 79 to 83), STND.CODE (4, 7, 9), STND.CXX (4, 21, 22), STND.MPI (Notes, 3, 5, 6), STND.DEPS (8 to 10), AGENT (39, 40), and the LVL0 provisions these rest on. STND.PY, STND.JL, and the rest were grepped for device, accelerator, GPU, kernel, offload, host, transfer, stream, queue, launch; they hold no offload rule (the hits are random-number streams and CPU threads). Background: research/openmp-notes/r3-offload.md, research/parallel-models.md, research/concurrency-notes/c1-corpus-gaps.md, HANDOFF.md (direction of 2026-10-24: offload next, agnostic and timeless, no framework annexes, citing STND.CONC). "Inference" marks a reading the corpus does not state.

## 1. Coverage table

Fit: full = an existing provision holds the outcome; partial = held in general terms, an offload form is missing; none = unreached.

| Item | Covered by | Fit | What remains |
| --- | --- | --- | --- |
| Asynchronous completion and errors | HW.GPU.3 (rank 0); STND.CONC.1 (binding); STND.CODE.7 (binding); HW.8; STND.CXX.21 (release calls that report errors, device memory and streams named in its Notes); STND.CONC.29 (pending operations in the record, CSQ1) | Full at the floor; partial above | The floor is complete, at most one wait per reported result (HW.GPU Notes). Not held: attribution of an error found at a later synchronization to the submission that caused it (the HW.GPU Notes name the hazard; HW.8 asks only an "actionable diagnosis"); release or destruction of device resources as a completion point whose status is checked (STND.CXX.21 is C++ only). |
| Failure signaled from inside device code | STND.CONC.2 (binding); PRIME.4; STND.CXX.22 | Partial (inference) | Device code often cannot halt, throw, or log. No provision says how a failure detected in it reaches the host. STND.CONC.2 reaches it only if device threads count as concurrent tasks with the submitting code as parent, which the corpus does not say. |
| Device faults and exhaustion | HW.8 (rank 0); HW.4; HW.9; HW.10; STND.ANNEX.6 (fault and response rows: halt, or resubmit from unaffected inputs and record it) | Full | Residue only: state of a device or context after a reported error, and safety of resubmitting work that wrote device data. |
| Fallback to another path | HW.19 (report at first occurrence, count); HW.9 (record in each affected result); HW.3; HW.15 to HW.17 | Partial | HW.19 applies "where an execution path falls back"; a silent fallback inside a runtime is reported only if the path detects it. No provision asks a project to state its fallback policy (forbidden, allowed and reported, allowed), to confirm placement, or to exercise the fallback path in tests. STND.OMP.23 and STND.OMP.31 are the OpenMP forms. |
| Data crossing host and device | HW.13 (layout, byte order, precision, ownership, ordering, timing); HW.14 (checks per crossing or per build); DSGN.4; NUMER.5; STND.ANNEX.6 (transfer ordering as the runtime documents) | Partial | Held: the static properties of the crossing. Not held: whether a copy is current, which copy is authoritative when, copy-back that does not happen, a host address used on a device, allocation and release balanced on every path, diverging copies of global state, a host write that races an in-flight transfer. STND.OMP.24 to STND.OMP.27 are the OpenMP forms; the model-neutral outcome is unowned. |
| Memory spaces and coherence, unified memory | HW.4 (memory and ordering model); HW.11; HW.13; STND.ANNEX.6; STND.CONC.3 to STND.CONC.5; STND.CONC Scope ("the memory of accelerators belongs to HW.GPU and to the standard for offload") | Partial | Shared address space or on-demand migration is not coherence. Not held: where each object resides and when each side may touch it; synchronization between host and device accesses where memory is shared; reliance on shared memory declared and tested on a device with separate memory (STND.OMP.28). Migration cost is recorded by HW.GPU.4. |
| Atomics and scopes | STND.CONC.3, STND.CONC.4; HW.11; STND.ANNEX.6 (atomics and reductions in unspecified order) | Partial | Nothing names the scope of an atomic or synchronization (the threads it orders against). STND.OMP.29 is the OpenMP form. Waiting among device thread groups that need not run concurrently: STND.CONC.11, second sentence (inference that it reaches them). |
| Delivered arithmetic | HW.5; STND.ANNEX.6 (arithmetic row); NUMER.5, NUMER.16, NUMER.17; STND.CXX.4; STND.VVUQ.4; HW.CPU.3 (CPU only) | Full, one residue | Reduced-precision modes, fusion, approximate functions, run-time kernel choice, flushed subnormals are held (HW.GPU Notes). Residue: HW.CPU.3 confirms floating-point control state at run time; no device counterpart exists (STND.OMP.30 asks only that code not rely on one across the boundary). Decide whether one is wanted. |
| Reproducibility and tolerances against a reference path | HW.12; HW.15 to HW.17; STND.VVUQ.1, .2, .7, .8, .79 to .83; STND.CONC.21, .22; REPRO.3; NUMER.11, NUMER.17 | Full | Nothing to restate. A deterministic mode is already admitted (STND.VVUQ.82). |
| Records of a run | HW.3; REPRO.2; HW.9; HW.19 (fallback count); HW.GPU.4; STND.DEPS.8; STND.OMP.3 (OpenMP form) | Partial | HW.3 covers model, firmware, drivers, runtime libraries, settings. Not held: which devices a run used (not only which it could see), which work ran where, and the persisted kernel cache (the HW.GPU Notes call it a setting under HW.3 and HW.7; no provision lists it). |
| Resource budgets and device memory | RSRC.1 to RSRC.4, RSRC.6; HW.8; HW.4; STND.ANNEX.6 (limits row); HW.GPU.4 (data moved, submissions, busy fraction, peak memory; CSQ3, measuring runs only) | Partial | Held: exhaustion halts or degrades visibly; peak use recorded in measuring runs. Not held: a stated device-memory budget checked before work is submitted; a report like HW.CPU.5 (oversubscription) for device memory exceeded by migration or several processes on one device; checked allocation results (STND.CODE.7 covers it generally). |
| Build targets and binaries for device architectures | STND.CXX.4 (target instruction set, C++); STND.DEPS.8; REPRO.9; HW.3, HW.5, HW.7; HW.GPU Notes (kernel caches) | None for the device case | No provision relates the device architectures a build carries code for to the hardware models a run uses, or covers device code specialized or compiled at run time for a model it was not built for (the arithmetic then changes under HW.5 with no visible build change). |
| Multiple devices | HW.GPU.3 ("one or several devices"); HW.13; HW.5 (same arithmetic on each model); STND.ANNEX.6; AGENT.40; STND.CONC.17, .18 (CPU pools) | Partial | Not held: selection and binding of devices to processes or tasks, transfers between devices, a device shared by several components of one run (the analog of STND.CONC.18), mixed device models. |
| Tests | VV.1; HW.15 to HW.17; STND.CODE.9; STND.CONC.24 to .27; STND.OMP.31 to .33 | Partial | Not held model-neutrally: a run that proves the device was used; a host-only run; an injected device error or allocation failure; more than one device; a problem larger than device memory. HW.16 holds the comparison, STND.VVUQ.1 the tier. |
| Verification tools | STND.CONC.25 to .27 (checks where the means exist; limits of each method stated); STND.OMP.32 | Partial | The STND.OMP Notes record that a race detector sees offloaded regions only when they run on the host and that mapping errors need a separate check. Remainder: tests run under a check of device code or device data state where one exists, and the record states what it does not cover. No tool is named. |
| Performance measurement | HW.22 (claims, data movement and dispatch counted, fraction of peak); HW.GPU.4; RSRC.2, RSRC.4; NUMER.17 | Partial | Not held: timing that covers completion (a timer around a submit measures the submit), one-time costs of a first call (initialization, run-time compilation, migration), warm versus cold state. |
| Remote or rented accelerators; shared machines; throttling; analog devices | PRIME.7, PRIME.8, GUARD.1, GUARD.11, GUARD.15, STND.HARN.18 (HW.GPU Notes); AGENT.39, AGENT.40, RSRC.8; HW Notes (throttling is not a capacity); HW Selector (analog devices are accelerators) | Full | Nothing. |

## 2. What the offload standard must not restate

Each line gives the provision that holds the matter (GOV.31).

- Completion status before reliance, errors handled as a detected fault: HW.GPU.3, STND.CONC.1, PRIME.4, HW.8. Failures reaching the parent and halts reaching dependents: STND.CONC.2. Discarded failures: STND.CODE.7. Status and release failures in C++: STND.CXX.21.
- Fault kinds, limits, response to exhausted capacity, undetected faults: HW.4, HW.8, HW.10; the default accelerator contract: STND.ANNEX.6.
- Fallback reported and counted, recorded in each result: HW.19, HW.9.
- Delivered arithmetic and run-time choice of implementation: HW.5; approximations and performance approximations: NUMER.16, NUMER.17; required and working precision: NUMER.5, NUMER.12.
- Layout, precision, byte order, ownership, ordering, timing, and checks at the boundary: HW.13, HW.14, DSGN.4.
- Reference path, verification of alternative paths, comparison beyond reach, path limits: HW.15 to HW.18, STND.VVUQ.79 to .81; tiers and tolerances: STND.VVUQ.1, .7, .8, NUMER.11; bitwise identity: STND.VVUQ.2, STND.CONC.22; declared variation: HW.12, REPRO.3, STND.CONC.21, STND.VVUQ.82, .83.
- Identity and settings of a path in each result, contract evidence and currency, toolchain revisions: HW.3, HW.6, HW.7, REPRO.2, STND.DEPS.8.
- Budgets, measured optimization, the offload resource record, performance claims: RSRC.1 to RSRC.4, HW.GPU.4, HW.22.
- Shared-state protocols, atomic ordering, lifetimes, bounded waits, queues, cancellation, task-count tests, race detectors, varied schedules, stated limits of verification, pending operations: DSGN.15, HW.11, STND.CONC.3 to .5, .10 to .14, .24 to .27, .29.
- Authorization of rented accelerators: PRIME.7, PRIME.8, GUARD.1, GUARD.11, GUARD.15, STND.HARN.18. Machine sharing among agents: AGENT.39, AGENT.40.
- Anything specific to directive-based offload: STND.OMP. The standard names no directive, clause, routine, framework, compiler, library, tool, or vendor (GOV.18).

## 3. Owners in the shared-matters tables

Only profiles and sub-profiles carry shared-matters tables (STND.DRAFT.39); STND.CONC and STND.OMP carry none. The offload standard needs none, but must cite the adopted provisions of an owner on which it builds (STND.DRAFT.39, STND.DRAFT.40).

| Matter | Owner | Provisions |
| --- | --- | --- |
| Hardware contract of an execution path | HW | HW.4 to HW.12 (HW.GPU.2 gives HW.GPU.3; NUMER.5 addresses it) |
| Boundary contract between execution paths | HW | HW.13, HW.14 (NUMER.5 addresses it) |
| Agreement between the alternative execution paths of a component | HW | HW.15 to HW.19 |
| Budgets of a constrained target | HW | HW.20, HW.21 |
| Comparative performance claims | HW | HW.22 |
| Precision a result requires; approximation disclosure; tolerance basis of a numerical comparison | NUMER | NUMER.5, .12, .17; NUMER.16, .17; NUMER.11, .25 (HW.16, HW.22 address) |

Offload matters that no table names: asynchronous completion and error attribution (HW.GPU.3 holds the accelerator case under "Hardware contract", STND.CONC.1 the general case); residency and currency of data across host and device (HW.13 and HW.14 hold only its static properties); placement and fallback policy of a run (HW.19 sits under "Agreement between the alternative execution paths"); resource records of runs (RSRC at LVL0; HW.GPU.4 has no matter); build targets for device architectures; multiple devices; checking tools for device code; timing method. Because LVL2 has no tables, any owner would have to be HW or HW.GPU at a later revision. That is a question for the custodian; the offload standard works without it.

## 4. Binding and default provisions, and class onsets

LVL1 provisions carry a rank and waivability; "mode" belongs to LVL2. SHALL is used in both. Under GOV.19 an LVL2 provision is binding only where it instantiates a prime directive, GUARD, or a floor obligation, or the custodians record why uniformity is required.

| Provision | Strength | Onset |
| --- | --- | --- |
| HW.GPU.3, HW.8 | SHALL, rank 0, not waivable (PRIME.4) | Every class; add nothing to the PRIME.4 floor |
| STND.CONC.1, STND.CONC.2, STND.CODE.7, STND.MPI.5, STND.MPI.6 | Binding | Every class |
| STND.VVUQ.83 | Binding, on agents | Every class |
| HW.4, HW.11, HW.13, HW.14 | SHALL, waivable (rank 5) | CSQ2 (HW Notes) |
| HW.3, HW.5, HW.6, HW.7, HW.9, HW.10, HW.12, HW.15 to HW.19, HW.22 | SHALL, waivable (ranks 2 to 6) | CSQ3; HW.10 only where a contract states an undetected fault; HW.9 and HW.19 tighten above INTPR.7 (CSQ1) at the cost of one message |
| HW.GPU.4 | SHALL, waivable (rank 7) | CSQ3, and only in runs that track or measure resource use (RSRC.2, RSRC.4) |
| HW.CPU.3 to HW.CPU.5 (parallel) | SHALL, waivable | CSQ3 |
| STND.CONC.3 to .9, .11 to .18, .20 to .24 | Default | CSQ3 |
| STND.CONC.19, .25, .26, .27 | Default | CSQ2 |
| STND.CONC.10 (report of a reached bound), STND.CONC.29 | Default | CSQ1 |
| STND.CONC.28 | Default | CSQ0, safety-related components |
| STND.ANNEX.3; other STND.ANNEX provisions | Default | CSQ2; CSQ3 |
| STND.CXX.4, STND.DEPS.8 | Default | CSQ3 |

STND.CLASS.10 (a default) lets CSQ4 omit every obligation above the floor and applies the rest from CSQ3 except the rows of its table: CSQ2 for DSGN.4, DSGN.5, DSGN.15, INTPR.10, RSRC.3, REPRO.4, and reference-oracle comparison under VV.1; CSQ1 for INTPR.6 to INTPR.8, VV.6, VV.10; CSQ0 for proof or exhaustive checking of safety-related components. A part of a provision that rests on a row takes the onset of that row; otherwise CSQ3, as the STND.OMP Notes apply it. Consequences:

- Only the floor outcome is binding, and HW.GPU.3 with STND.CONC.1 holds it. The offload standard should have no binding provision unless it shows a new PRIME or GUARD instantiation. STND.OMP has none.
- Data-crossing rules (DSGN.4, DSGN.5, HW.13, HW.14) apply from CSQ2, as STND.OMP.25 and .26 do. Placement, fallback, and test rules (HW.3, HW.9, HW.15, HW.19, VV.1) apply from CSQ3, as STND.OMP.23 and .31 do. A statement resting on DSGN.5 is CSQ2 even where it also cites HW.5 (STND.OMP.30).
- Match each onset to that of the OpenMP rule it will serve (section 5).

## 5. The rules STND.OMP leaves to the planned offload standard

STND.OMP Notes, offload paragraph, last sentence: "Most of these rules are specific to the directive model of OpenMP. Completion before results are read, the movement of data, and device arithmetic hold for every offload model, and belong to the planned standard for offload." Its Purpose says the model-neutral rules of accelerator offload belong to a planned standard. HANDOFF.md: once the offload standard is adopted, STND.OMP at its next revision cites it for those rules.

| STND.OMP | Model-neutral outcome | OpenMP form that stays |
| --- | --- | --- |
| .23 | A run that relies on work running on a device confirms that it did or ends where none is available; the host path of conditional offload is stated and tested | Mandatory offload; the if clause |
| .24 | Devices chosen are checked against those that exist; device allocations are checked and released once on every path | Device numbers; paired allocate and free routines |
| .25, .26 | Data a result depends on is on the device before use and copied back by a means that cannot be suppressed; each acquisition ended once on every path; a pointer valid in the other memory space | Map clauses, structure and pointer mapping, reference counts, present, always, update |
| .27 | Copies of global state synchronized before the other copy is read; static data used on a device declared | declare target |
| .28 | Reliance on shared memory declared, tested on a device without it, answered where none qualifies; shared memory still needs synchronization | requires directive |
| .29 | An operation ordering host and device accesses has a scope that includes both | Memory scope of atomic |
| .30 | No reliance on floating-point state across the boundary | Possibly only a citation |
| .31, .32 | Tests prove device use, run the host-only path, compare with a reference at the tier of STND.VVUQ.1, and run under a check of device data state where one exists | Mandatory offload runs; the mapping check |
| .3 (last clause) | Record of devices used and placement policy | Internal control variables |

How to take them over:

1. Write each offload provision as the outcome, instantiating the same LVL0 and HW provisions its OpenMP counterpart instantiates (DSGN.4, DSGN.5, DSGN.14, DSGN.15, HW.13, HW.14, HW.15, HW.19, VV.1). Corpus practice is that an LVL2 provision instantiates LVL0 or LVL1 provisions only and names another standard in `refers_to` and the Notes ("the OpenMP form of STND.CONC.16"). Follow it.
2. Give each the onset of its OpenMP counterpart, so a citation moves no OpenMP rule to another class.
3. Keep every provision a default, as in STND.OMP.
4. At its next revision (a minor amendment under GOV.41, no renumbering), STND.OMP keeps its directive and clause rules, drops any sentence that only restates the outcome, adds the offload standard to its References, cites the matching offload provision in its Notes, and changes "planned" in its Purpose and Notes to a citation. Where an OpenMP rule is the offload rule exactly (.30 may be), replace it by a citation (GOV.31).
5. Put the provision-to-provision mapping in the offload standard's Notes so a reviewer can see nothing was lost, as STND.CONC does for STND.MPI and the language standards.
6. Cite STND.CONC for asynchronous operation, concurrent task, parent, and pending operations. STND.CONC already says the planned standards "hold theirs once adopted".

## 6. Terms to reuse (GOV.26: define own terms without redefining)

- HW: Accelerator, Accelerator execution, Execution path, Alternative execution path, Reference path, Hardware contract, Boundary contract, Hardware model, Hardware type, Hardware fault, Capacity, Delivered arithmetic, Runtime library, Constrained target.
- HW.GPU: Offloaded work (work a host submits to an accelerator, whose completion the host learns of after the submitting call returns) and Completion status. They are the base of the standard.
- STND.CONC: Asynchronous operation, Concurrent task, Parent, Shared mutable object, Protection, Data race, Pool. That offloaded work is an asynchronous operation and device threads are concurrent tasks is an inference; state it once in Terms or Notes.
- NUMER: Working precision, Required precision, Performance approximation, Approximation, Numerical result, Numerical specification.
- STND.ANNEX: Default contract, Citing contract; the accelerator default is STND.ANNEX.6.
- Not to reuse: STND.OMP terms (Offload policy, Mandatory offload, Device, Host device, Target region, Map) are OpenMP's. HW.CPU's Floating-point control state and Hardware thread are defined for general-purpose processors; a device counterpart needs a new term.
- New terms likely needed (none exist): Device (a hardware model of an accelerator, or the host, as a run sees it), Residency or copy of data, Placement, Memory scope, Fallback policy. Check each against the HW Alternative execution path and HW.19 before adding.

## Main gaps

1. Currency and residency of data across host and device (model-neutral STND.OMP.24 to .27).
2. Confirmed placement and a stated fallback policy (STND.OMP.23, .31).
3. Scope of atomics and synchronization across host and device; reliance on shared memory (STND.OMP.28, .29).
4. Build targets versus run-time hardware model, run-time specialization, kernel caches in the record.
5. Device memory as a budget, with an oversubscription report like HW.CPU.5; several components on one device; multiple devices.
6. How a failure in device code reaches the host; attribution of late-reported errors.
7. Test and measurement method: proof of device use, injected errors, timing that covers completion and first-call costs, coverage of tools on device code.
