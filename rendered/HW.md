# Execution hardware (HW) 1.3.1

Adopted by The Custodian as revision 1.0 in ledger entry 64 (2026-10-17); revised to 1.0.1 in entry 75 (2026-10-18), 1.0.2 in entry 83 (2026-10-19), 1.1 in entry 89 (2026-10-19), 1.1.1 in entry 110 (2026-10-24), 1.1.2 in entry 168 (2026-10-25), 1.2 in entry 228 (2026-10-28), 1.3 in entry 252 (2026-10-28), and 1.3.1 in entry 303 (2026-10-28). This reading copy is composed from the per-provision files in HW/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This profile holds the obligations of work whose components execute on hardware: general-purpose processors, accelerators, quantum processors, embedded controllers, and realized designs of programmable logic and integrated circuits. Hardware changes results without changing code. It does so through the arithmetic it delivers, the order in which it combines values, the limits it imposes, the faults it meets or misses, and the firmware, drivers, and libraries through which code reaches it. A result that is correct on one machine is therefore able to be silently wrong, or merely different, on another. The profile asks that what each component relies on from its hardware be stated as a contract, supported by evidence, and confirmed before each run. It asks that the boundaries between hardware types and models be stated and checked, and that each alternative execution path be verified against its component's one contract. It asks that the budgets of constrained targets be verified on the target, and that faults, fallbacks, and undetected-fault exposure be visible. It names no language, library, tool, technology, platform, process, or method (GOV.18). The sub-profiles HW.CPU, HW.GPU, HW.QPU, HW.EMBED, HW.FPGA, and HW.ASIC add obligations specific to each hardware type (GOV.27). The design of programmable logic and integrated circuits belongs to HDES; this profile governs execution on a realized design.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Accelerator | A processor that executes only work that a host processor offloads to it, other than a quantum processor, programmable logic, or an integrated circuit. |
| Alternative execution path | One of two or more execution paths of a component, each of which computes the component's results without the others. |
| Capacity | A limit of hardware on memory, storage, buffers, queues, counters, stored energy, or supplied power beyond which an operation fails, loses data, or resets the hardware. A limit at which the hardware only slows execution is not a capacity. |
| Boundary contract | The contract at an interface boundary between execution paths on different hardware types or hardware models. |
| Constrained target | An execution path that has a deadline whose miss is able to change either a result that the path goes on to report or rely on or a command that the path issues to physical hardware, or on which reaching a capacity of its hardware is able to change or lose a result without a halt or visible degradation. |
| Delivered arithmetic | The number formats, rounding, handling of subnormal and non-finite values, fusion and contraction of operations, order in which values are combined, and accuracy of elementary functions that an execution path gives the numerical operations of a component, as its modes, library defaults, options, and choices made at run time set them. |
| Embedded controller | A processor, other than programmable logic or an integrated circuit, that executes firmware to control or monitor a device, with no operating system between the firmware and the device, or with one whose scheduling the firmware's deadlines constrain. |
| Execution path | A component together with a hardware type on which it executes, and the hardware models, firmware, drivers, runtime libraries, and settings that it admits there. |
| General-purpose processor | A processor that executes a stored program, other than an accelerator, a quantum processor, an embedded controller, programmable logic, or an integrated circuit. |
| Hardware execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on a hardware type. |
| Hardware contract | The contract of an execution path: the behavior of its hardware type, hardware models, firmware, drivers, runtime libraries, and settings that the component relies on in its regime of use. |
| Hardware fault | A departure of hardware from its specified behavior: a changed bit in memory, storage, a register, or a link; a wrong result from a processing unit; a lost message; or a loss of power. The noise of a quantum processor that its hardware contract states is not a hardware fault. |
| Hardware model | The design and revision of a hardware device, as its maker or its design record identifies it. |
| Hardware type | One of the kinds of execution hardware for which this profile holds a sub-profile: general-purpose processors, accelerators, quantum processors, embedded controllers, programmable logic, and integrated circuits. |
| Integrated circuit | A device fabricated from a hardware description whose design record the project holds, other than programmable logic. |
| Programmable logic | A configuration of a device whose logic is configured after manufacture. |
| Quantum processor | Hardware that computes a result by executing quantum circuits, or by evolving quantum states under controlled interactions, and returns measured outcomes; a device that measures a physical quantity through quantum states is not a quantum processor. |
| Reference path | The alternative execution path of a component on which the component's obvious implementation executes, taken with that implementation alone, against which its other alternative execution paths are verified (SIMPL.7). Where the alternative execution paths of a component execute one source, the reference path is the path whose delivered arithmetic the component's specification assumes. |
| Runtime library | A library through which a component reaches its hardware and that sets at least one of its delivered arithmetic, its placement of data in memory, its scheduling of concurrent work, or its choice at run time among implementations. |

## Selector

HW.1 states the selector: one attribute, Hardware execution, defined here, which the selector of each sub-profile gives as well (HW.CPU.1, HW.GPU.1, HW.QPU.1, HW.EMBED.1, HW.FPGA.1, HW.ASIC.1, STND.DRAFT.36), so that the hardware types on which the work executes are a matter of its execution paths and not of an attribute each, and path scope alone decides which sub-profile's provisions reach a component. The domain items are execution paths, hardware contracts, boundary contracts, constrained targets, and claims comparing the performance of execution paths. Because each provision names as its subject an execution path, a contract, or a record or claim about one (STND.DRAFT.37, STND.DRAFT.38), a provision about an execution path on one hardware type imposes nothing on a component that has no path on that type. A component that executes only on general-purpose processors meets this profile and HW.CPU for its own path, and the boundary contracts it shares with components on other types; it meets no obligation specific to accelerators, quantum processors, or embedded controllers. The attribute is also true where the classification records that such a component is admitted to execute on a hardware type. No selector tests the type, so a path on a new hardware type revises no attribute; the execution paths of each component are recorded by hardware type where the section Architecture of the constitution names (STND.PROJ.1), outside the classification, so that an agent adds a path on a new type to that record without a decision of the human owner, and the provisions of the sub-profile of that type reach the path from then on. Hardware of a kind that Hardware type does not name is governed by LVL0 and by the nearest of this profile and its sub-profiles applied by analogy, with the choice of analogue recorded (GOV.29). A processor realized in programmable logic is programmable logic. Analog and neuromorphic devices are accelerators where a host offloads work to them, and otherwise fall under GOV.29. Each sub-profile's selector gives the attribute of HW.1.

## Where the rest lives

LVL0, AGENT, NUMER, and STND.VVUQ already govern these matters of execution on hardware, and this profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Hardware limits honored as correctness | GOV.8 |
| Contracts of external components and of hardware, verified in the regime of use | DSGN.5 |
| Schemas, units, and conventions caught at the boundary | DSGN.4 |
| Versioned contracts and announced interface changes | DSGN.6 |
| Concurrent access to shared state under a stated protocol | DSGN.15 |
| Hardware, firmware, drivers, and libraries enumerated as dependencies | REPRO.9 |
| Result-affecting properties of the computational environment recorded as inputs | REPRO.2 |
| Run-to-run variation and its declaration | REPRO.3 |
| Records kept readable after the producing platform is gone | REPRO.12 |
| Loud failure on invalid input, non-convergence, and resource exhaustion | PRIME.4 |
| Commanding, configuring, or powering physical hardware | PRIME.13 |
| Budgets, unknown budgets, observability, and measured optimization | RSRC.1, RSRC.2, RSRC.3, RSRC.4 |
| Cost of supporting machinery, data movement included | RSRC.6 |
| Optimized code verified against the obvious implementation | SIMPL.7 |
| Required precision, working precision, and tolerance basis of numerical results | NUMER.5, NUMER.11, NUMER.12 |
| Approximations introduced by hardware or library defaults | NUMER.16, NUMER.17 |
| Comparison tiers and tolerance brackets for agreement between paths | STND.VVUQ.1, STND.VVUQ.7, STND.VVUQ.8 |
| Parallel work on a shared machine | AGENT.39, AGENT.40 |

## Notes

Against the two dangers that lower governance serves, this profile is aimed at silent misalignment between what code assumes of its hardware and what the hardware does. A reduced-precision default, a reordered reduction, a kernel chosen at run time, a flushed subnormal, a driver update, a fallback to another device, a weaker memory model, and an undetected memory error each leave the code unchanged and the result different. Every provision is checkable from records, so an agent satisfies it unattended and a reviewer confirms it without re-running the work; none asks the human owner for a decision (STND.DRAFT.42), and none needs elevated privileges: what a path is unable to read without them is recorded as unread (HW.3), and for confirmation an unread item counts as changed while a check of the property itself serves instead (HW.7). No provision halts a run that its hardware has not halted. A run under unconfirmed contract evidence, a run resumed on another node included, proceeds; its results record each unconfirmed property, and no claim of correctness rests on it until the evidence is renewed (HW.7). HW.18 keeps a result off a path whose limit falls short of the result's requirement, which blocks that result only where no other path meets the requirement. The profile costs most once, in the hardware contract and its evidence, which are kept per hardware model and software stack and shared by every path and project that admits them (HW.6), and little per run: an identity comparison, a record the hardware gives, or a self-check of each relied-upon property at start or resumption, and records written by the run itself.

The profile follows the custodian's direction of 2026-10-11 on mixed hardware. A code with parts on general-purpose processors, accelerators, and controllers binds each part by the sub-profile of the hardware it executes on, and joins the parts by the contracts at their boundaries (HW.13, HW.14). The parts on general-purpose processors are not bound by accelerator or controller obligations. Execution paths that cooperate, such as host code and the kernel it launches, are joined by a boundary contract; alternative execution paths, each of which computes the component's results alone, are verified against each other. A component with alternative execution paths, for example one routine with a processor path and an accelerator path, treats each path under its own sub-profile and hardware contract, and verifies each against the component's one contract: at the interface boundary for each property decidable there, and otherwise by comparison with its reference path within a tolerance recorded before the comparison (HW.16). Where the reference path is too slow for part of the regime of use, the comparison covers the part it reaches within a time budget recorded beforehand, and the rest is covered by the trend of the difference with problem size and by full-size checks of properties decidable without the reference, which catch failures that appear only at scale, such as an index overflow or a kernel switch; the extrapolation is judged by a criterion recorded beforehand, and results beyond the compared part record that their agreement rests on it (HW.17). Where a path is unable to meet a property of that contract, the contract states the path's own value as a limit of the path by a recorded decision of the agent responsible that cites evidence of the path's value other than the comparison that found the shortfall, each result computed there records the limit beside its own requirement, and no result that needs more than the limit is computed there (HW.18); a numerical result computed on that path still meets its own required precision (NUMER.5). A fast path of limited accuracy is thus usable without a decision of the human owner wherever its limit suffices. The reference path is the obvious implementation (SIMPL.7). It is usually, though not necessarily, on a general-purpose processor, and its own verification is the anchor the other paths cite (HW.15). It is able to exist only in the verification suite, and is not shipped or maintained for production runs. Where one source runs on several hardware types, the reference path is the one whose delivered arithmetic the component's specification assumes, so no second implementation is written for the purpose. STND.VVUQ.1 gives the default tier of each comparison, from bitwise identity to a tolerance set from rounding or numerical error, and a comparison of the results of a stochastic method is also an acceptance criterion under NUMER.25. A path that differs from the reference by a performance approximation, such as a reduced-precision default, also meets NUMER.17.

HW owns five shared matters (HW.2): the hardware contract of an execution path, including its delivered arithmetic, the hardware side of what NUMER calls working precision, which the NUMER 1.0 review recorded as unallocated; the boundary contract between execution paths; agreement between the alternative execution paths of a component; the budgets of constrained targets; and comparative performance claims, which STND.VVUQ.77 also addresses for learned methods and cites at its next amendment. It addresses three matters that NUMER owns: the precision a result requires and approximation disclosure, through HW.16, which cites NUMER.17; and the tolerance basis of a numerical comparison, through HW.16 and HW.22, which cite NUMER.11. This split refines the allocation proposed by the cold review of STND.VVUQ 1.0, which gave the tolerance for agreement across runs, execution paths, and arithmetic settings to NUMER: NUMER keeps the basis of each tolerance, and HW keeps the obligation to compare paths. NUMER 1.1, a conforming amendment adopted with HW, gives in NUMER.2 the matter "Tolerance basis of a numerical comparison", owned by NUMER and given by NUMER.11 and NUMER.25, and the two HW matters that NUMER.5 addresses, "Hardware contract of an execution path" and "Boundary contract between execution paths", each given by NUMER.5; and NUMER.5 cites HW.5 for the delivered arithmetic and HW.13 for the precision of exchanged operands (STND.DRAFT.39, STND.DRAFT.40). HDES addresses the hardware contract for realized designs by citing HW: where a realization is part of an execution path, its design record states what HW.4, HW.5, and HW.13 ask and marks each property whose evidence comes only from analysis or simulation, for the evidence that HW.6 asks (HDES.5).

Computing hardware protected by its own operating system and onboard circuitry is not physical hardware in the sense of PRIME.13. Executing on it engages this profile, not CPS. An embedded controller that commands, configures, or powers physical hardware engages both, and CPS owns the coverage of the hazard analysis and the verification of the safe state (CPS.3, CPS.4). Where a constrained target is in a control loop, CPS.8 states each deadline of the loop whose miss is hazardous, and HW.20 asks for a bound on worst-case execution time that meets it; for every other deadline, a bound or run-time detection of each miss, stated in the record of each command or result it changes, suffices, so that a loop on a host without real-time guarantees is not held to a bound that its hardware cannot give.

A documented specification of hardware or its software is evidence once its stated conditions are shown to hold and its source is confirmed under VV.2 as the project's class applies it (VV.1). The per-job calibration record that the provider of a quantum processor gives is a record of the property that its hardware gives for the run, and confirms it under HW.7. A published accuracy is often a maximum found by testing rather than a proven bound. HW.6 therefore marks properties resting on documentation, and documented accuracies that are tested maxima, which tells a reviewer which properties carry measured support and which comparisons in units in the last place need a margin (STND.VVUQ.4). Evidence for a contract is not tied to the run that gathered it. Once established for a set of hardware models, firmware, drivers, runtime libraries, and settings, it holds until one of them changes, and HW.7 has each run confirm the properties it relies on, by comparing what it reads of that identity or by checking the property directly, whichever is cheaper. Only runtime libraries in the defined sense are part of a contract, so an update of a dependency that sets no delivered arithmetic, memory placement, scheduling, or implementation choice renews nothing. The kinds of hardware fault are bounded by the Term. Silent data corruption is addressed by HW.4 and HW.10: the contract states which kinds its hardware does not detect, and a path exposed to one either checks for it or says so in the record of each result. The noise of a quantum processor belongs to its noise model, in its hardware contract and its uncertainty statement, not to its faults. Limits at which hardware only slows, power and thermal throttling included, are neither capacities nor grounds for a constrained target, while a limit on supplied power that resets the hardware is a capacity; so a processor running at its power limit by design engages none of HW.8, HW.9, HW.20, or HW.21 by reason of that limit alone; a cluster's limit on wall time halts the run and engages none of them either.

HW.8 states how PRIME.4 applies to detected, uncorrected hardware faults and to exhausted capacity, and binds at every class, adding nothing to the floor that PRIME.4 does not already hold. For a run of several processes that compute one result together, HW.8 is read as asking the whole run to halt, degrade visibly, or transition to a designed safe state. A process that halts while the others wait on it leaves a silent hang. STND.MPI.6 states how the halt of one process reaches the others in a program that uses the Message Passing Interface. Every other provision except HW.1 and HW.2 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, so that the hardware contract of HW.4 and the delivered arithmetic, the evidence, and the currency with which HW.5 to HW.7 fill it start together at CSQ2, with the contract that DSGN.5 asks, while the identity record of HW.3 and the variation declaration of HW.12, which cost one record each and which a later reclassification needs, start at CSQ3, and a field that gives CSQ3 for a report, a stated limit or exposure, or the verification of a path, content that the table of STND.CLASS.10 starts at a more severe class, tightens above the floor (PRIME.15) at the cost of one message, one statement, or one run, because a fallback, a limit, or an exposure that a reader does not see is a silent misalignment at every class. A silent fallback or an unmonitored overrun is a silent misalignment, and a fallback found only after a long run wastes the run. From CSQ3, HW.3 and HW.9 put each fallback in the record of each result it affects, HW.19 reports it to the operator at its first occurrence, and the record of the run's resource use counts fallbacks, because a fallback is a regression in resource use that RSRC.2 makes visible from the first run; HW.21 monitors budgets and reports overruns from the class at which RSRC.2 applies. Both reports therefore tighten above the class at which INTPR.7 applies, at the cost of one message each; each goes to the operator of a run during which one acts, and otherwise into the record of the run, since an unattended run has no operator to receive a message and its record is what a reader examines afterward. Where the classification records an expected class, STND.CLASS.21 has the design not preclude the hardware, the reference path (HW.15), the reduction order, and the bounds (HW.20) that the obligations of that class ask of the work, with the reason for each such choice in a decision record, and asks no other record of that class before the reclassification than the records of STND.CLASS.23. Because nearly all computational work executes on general-purpose processors, this profile binds widely, and most of its obligations are light at the less severe classes. The type detail that a sub-profile does not hold sits in the hardware annex (STND.ANNEX).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| HW.ASIC | Application-specific integrated circuits |
| HW.CPU | General-purpose processors |
| HW.EMBED | Embedded controllers |
| HW.FPGA | Field-programmable gate arrays |
| HW.GPU | Accelerators |
| HW.QPU | Quantum processors |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.ANNEX | Hardware type annex |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.MPI | Message Passing Interface standard |
| STND.PROJ | Project constitution template |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Application

#### HW.1 Execution hardware selector

. Instantiates GOV.25, GOV.26.

This profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26).

| Attribute | Defined by |
| --- | --- |
| Hardware execution | HW |

#### HW.2 Hardware shared matters

. Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Hardware contract of an execution path | HW | HW.4, HW.5, HW.6, HW.7, HW.8, HW.9, HW.10, HW.11, HW.12 |
| Boundary contract between execution paths | HW | HW.13, HW.14 |
| Agreement between the alternative execution paths of a component | HW | HW.15, HW.16, HW.17, HW.18, HW.19 |
| Budgets of a constrained target | HW | HW.20, HW.21 |
| Comparative performance claims | HW | HW.22 |
| Precision a result requires | NUMER | HW.16 |
| Approximation disclosure | NUMER | HW.16 |
| Tolerance basis of a numerical comparison | NUMER | HW.16, HW.22 |

### Execution paths

#### HW.3 Execution path record

From CSQ3. Instantiates REPRO.1, REPRO.2.

Each execution path that computes a reported result SHALL be identified in the record of that result, with each item of its hardware model, firmware, drivers, runtime libraries, and settings that is able to affect the result and that the path reads without elevated privileges (REPRO.1, REPRO.2). The record of that result SHALL name each item of that kind able to affect the result that the path is unable to read without elevated privileges (REPRO.2).

### Hardware contracts

#### HW.4 Hardware contract

From CSQ2. Instantiates DSGN.5.

Each execution path whose behavior affects a reported result SHALL have a hardware contract that states, for its regime of use, each property of the path on which the component relies, and, for each of its delivered arithmetic, its memory and ordering model, and its timing, either the property relied upon or that the component relies on none (DSGN.5). The hardware contract SHALL state each limit of its hardware on capacity, timing, or power that the component is able to reach in its regime of use (DSGN.5). The hardware contract SHALL state each kind of hardware fault able to change a reported result, whether its hardware detects that kind and whether it corrects it, and the response of the path to each detected fault that is not corrected (DSGN.5).

#### HW.5 Delivered arithmetic

From CSQ2. Instantiates DSGN.5, REPRO.2.

The hardware contract of each execution path that performs a numerical operation of its component SHALL state each property of its delivered arithmetic on which the working precision of a reported result depends, and its handling of non-finite values, with each mode, library default, or option that sets them (DSGN.5, REPRO.2). Where the path chooses at run time among implementations that differ in delivered arithmetic, the hardware contract SHALL state the range of delivered arithmetic over those choices, or that the range is not established (DSGN.5). Where the path admits more than one hardware model, the hardware contract SHALL state whether its delivered arithmetic is established as the same on each (REPRO.2).

#### HW.6 Contract evidence

From CSQ2. Instantiates DSGN.5, VV.1.

Each property of a hardware contract on which a reported result relies SHALL be supported by evidence that records the property, the hardware model, firmware, drivers, runtime libraries, and settings on which it was obtained, the regime it covers, and its outcome, or by a documented specification of the hardware or its software whose stated conditions are shown to hold in the regime of use and whose confirmation meets VV.2 as the project's class applies it (DSGN.5, VV.1). The hardware contract SHALL mark each property that a documented specification alone supports as resting on documentation, and each documented accuracy that is a tested maximum rather than a proven bound as such (VV.1). The evidence for a property MAY be evidence obtained once for a hardware model, firmware, drivers, runtime libraries, and settings, and shared by each execution path, in every project, that admits them and whose regime of use the recorded regime includes (DSGN.5, VV.1).

#### HW.7 Contract currency

From CSQ2. Instantiates VV.8, DSGN.5, REPRO.2, INTPR.10.

Before a claim of correctness of a result rests on a property of the hardware contract of an execution path, the path SHALL hold evidence for that property obtained under its current hardware model, firmware, drivers, runtime libraries, and settings, or a record that each difference from those under which the evidence was obtained is unable to affect that property (VV.8, DSGN.5). At the start or resumption of each run, each execution path SHALL confirm each property of its hardware contract on which its results rely, by checking the property itself, by a record of the property that its hardware gives for the run, or by comparing each item on which the property depends with the item recorded with the evidence, an item that the path is unable to read counting as a failed comparison (VV.8, REPRO.2). Where that confirmation fails for a property, the record of each result of the run that relies on that property SHALL state that the property is unconfirmed and that no claim of correctness of the result rests on it (VV.8, INTPR.10).

#### HW.8 Faults and exhaustion

. Instantiates PRIME.4.

Where an execution path detects a hardware fault that its hardware does not correct, receives notice of one through its interface to that hardware, or exhausts a capacity of its hardware, the path SHALL halt, degrade visibly, or transition to a designed safe state, with an actionable diagnosis (PRIME.4).

#### HW.9 Results across hardware events

From CSQ3. Instantiates INTPR.9.

Each execution path that computes a reported result across a hardware fault, an exhausted capacity, a fallback to another execution path, or a reached limit of its hardware that is able to change that result SHALL state the event and the response taken in the record of that result (INTPR.9).

#### HW.10 Undetected fault exposure

From CSQ3. Instantiates VV.1, INTPR.10.

Where the hardware contract of an execution path states that a fault able to change a reported result goes undetected by its hardware, the path SHALL check its results by a means able to detect that fault, or state that exposure in the record of each reported result it computes (VV.1, INTPR.10).

#### HW.11 Memory model verification

From CSQ2. Instantiates DSGN.15.

Each execution path whose component's own code accesses shared state concurrently, an interrupt handler and the code it interrupts included, SHALL verify the protocol for that state under the memory and ordering model that its hardware contract states, or under that of its language or library for a protocol that uses only their synchronization (DSGN.15).

#### HW.12 Path variation

From CSQ3. Instantiates REPRO.3.

Each execution path SHALL state, in the declaration of its run-to-run variation, whether the order in which it combines values, the scheduling of its concurrent work, and its choices made at run time among implementations vary between runs on identical recorded inputs (REPRO.3).

### Interface boundaries

#### HW.13 Boundary contract

From CSQ2. Instantiates DSGN.4, DSGN.5.

Where execution paths on different hardware types or hardware models exchange data or control, the boundary contract between them SHALL state the layout, byte order, precision, and ownership of what crosses the boundary, and its ordering and timing or that neither path relies on them (DSGN.4, DSGN.5). A boundary contract MAY incorporate the documented contract of the library that performs the exchange, for each property that the documented contract states under conditions shown to hold in the regime of use (DSGN.5).

#### HW.14 Boundary checks

From CSQ2. Instantiates DSGN.4.

Each property of a boundary contract that is decidable from what crosses the boundary SHALL be checked at the boundary, on each crossing, or once for each build or compilation whose record shows that property fixed for every hardware model that the joined paths admit (DSGN.4). Where the boundary contract records that a check on each crossing exceeds the budget it states for the crossing, that property SHALL be checked at the boundary in the verification of each execution path that the boundary joins (DSGN.4).

### Alternative execution paths

#### HW.15 Reference path

From CSQ3. Instantiates SIMPL.7, VV.1.

Each alternative execution path SHALL name the reference path of its component in the record of its verification (SIMPL.7). The verification of each alternative execution path other than the reference path SHALL cite the evidence that verifies the reference path against the component's contract (VV.1).

#### HW.16 Alternative path verification

From CSQ3. Instantiates VV.6, VV.3, VV.1, SIMPL.7.

Each alternative execution path other than the reference path of its component SHALL be verified against the component's contract, at the component's interface boundary for each property decidable there, and otherwise by comparison with the reference path in the regime of use, or in the part of it that HW.17 gives, within a tolerance recorded before the comparison (VV.6, VV.3). Where the compared output is a numerical result, that tolerance SHALL rest on a basis that NUMER.11 gives (VV.1). Where an alternative execution path differs from its reference path by a performance approximation, its verification SHALL also meet NUMER.17 (SIMPL.7, VV.1).

#### HW.17 Comparison beyond reference reach

From CSQ3. Instantiates VV.6, VV.1, VV.3, INTPR.10.

Where the reference path of a component is unable to run a part of the regime of use within the time budget that the verification records before the comparison, the comparison of HW.16 SHALL cover the part of the regime that the reference path runs within that budget, as recorded before the comparison (VV.6, VV.3). Where that comparison covers only part of the regime of use, the verification SHALL also carry evidence, judged by a criterion recorded before the comparison, that the difference from the reference path, extrapolated with problem size, stays within the tolerance of HW.16 over the rest of the regime, and a check at full size of each property of the component's contract that is decidable without the reference path (VV.1, VV.3). Where that comparison covers only part of the regime of use, the record of each result computed in the rest of the regime SHALL state that its agreement with the reference path rests on extrapolation (INTPR.10).

#### HW.18 Path-specific limits

From CSQ3. Instantiates DSGN.5, VV.3, INTPR.10.

Where an alternative execution path is unable to meet a property of its component's contract, the component's contract SHALL state the path's own value of that property as a limit of the path, by a recorded decision that leaves the prior value in the record and cites evidence of that value other than the comparison that found the shortfall (DSGN.5, VV.3). The record of each reported result computed on that path SHALL state that limit beside the result's own requirement on that property (INTPR.10). A result that requires that property beyond that limit SHALL NOT be computed on that path (VV.3).

#### HW.19 Execution path fallback

From CSQ3. Instantiates INTPR.7, RSRC.2.

Where an execution path falls back to another execution path during a run, the path SHALL report the fallback at its first occurrence in the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.7). The record of the resource use of the run SHALL hold the count of fallbacks of each kind in the run (RSRC.2).

### Constrained targets

#### HW.20 Constrained target budgets

From CSQ3. Instantiates RSRC.1, VV.1, INTPR.9.

Each constrained target SHALL state each of its budgets with its margin, and evidence that it meets each budget within that margin under the power, thermal, and contention conditions of its regime of use, consisting of evidence obtained on that target before the component is first relied upon there and, for each such condition that the work is unable to produce on the target, a documented specification of the hardware whose stated conditions include it (RSRC.1, VV.1). Where the hazard analysis of PRIME.13 identifies the miss of a deadline as able to cause a hazard, the constrained target SHALL have a bound on its worst-case execution time that meets that deadline within its margin (RSRC.1, VV.1). Where the miss of another deadline is able to change a command that the target issues or a result that the work reports or relies on, the constrained target SHALL have such a bound, or detect each missed deadline at run time and state it in the record of each command or result that the miss is able to change (RSRC.1, VV.1, INTPR.9).

#### HW.21 Budget monitoring

From CSQ3. Instantiates RSRC.2, RSRC.3, INTPR.7.

Each constrained target SHALL monitor during runs each of its budgets for which no bound, established before the component is first relied upon there, holds for every run in its regime of use, and report each overrun to the operator of a run during which one acts and otherwise in the record of the run (RSRC.2, RSRC.3, INTPR.7).

### Performance claims

#### HW.22 Comparative performance claims

From CSQ3. Instantiates RSRC.4, RSRC.6, SIMPL.7.

Each claim that one execution path is faster or more efficient than another, stated in a reported result or a release, SHALL rest on measurements of both at a stated problem size, under stated conditions of contention, power, and thermal state, with data movement between hardware types and dispatch counted, at an accuracy that the results of both are shown to meet (RSRC.4, RSRC.6, SIMPL.7). Where the compared results are numerical results, that accuracy SHALL be judged within a tolerance that rests on a basis that NUMER.11 gives (RSRC.4, SIMPL.7). Where the hardware of the comparator of such a claim states a peak rate for the operations or data movement that limit the comparator, the claim SHALL state the rate of the comparator, measured or counted from the operations it performs, as a fraction of that peak rate (RSRC.4, SIMPL.7).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-17 | Adopted. |
| 1.0.1 | 2026-10-18 | Editorial amendment (GOV.41): the Notes describe HDES as adopted, citing HDES.5, in place of a clause that its adoption made stale; no obligation changes. |
| 1.0.2 | 2026-10-19 | Editorial amendment (GOV.41): the informative Notes describe the sub-profiles and CPS as adopted, citing CPS.3, CPS.4, and CPS.8; no obligation changes. |
| 1.1 | 2026-10-19 | Minor amendment (GOV.41): HW.20 asks for a bound on worst-case execution time only for a deadline whose miss the hazard analysis of PRIME.13 identifies as hazardous, and accepts a bound or detection of each miss, stated in the record, for every other deadline that changes a command or a result; the Notes state the same. |
| 1.1.1 | 2026-10-24 | Editorial amendment (GOV.41): the informative Notes state that, for a run of several processes that compute one result together, HW.8 is read as asking the whole run to halt, degrade visibly, or transition to a designed safe state, citing STND.MPI.6, and References lists STND.MPI; no obligation changes. |
| 1.1.2 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites the selectors of the six sub-profiles that the Purpose names, each of which gives one attribute of HW.1 (STND.DRAFT.36), and References lists HW.ASIC, HW.CPU, HW.EMBED, HW.FPGA, HW.GPU, and HW.QPU; no obligation, permission, or defined meaning changes. |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): HW.1 gives one attribute, Hardware execution, which the Terms define and the selector of each sub-profile gives as well, in place of one attribute per hardware type, and Hardware type names the kinds for which the profile holds a sub-profile (CS9); HW.19 and HW.21 report to the operator of a run during which one acts and otherwise in the record of the run (CS8); the Notes cite STND.CLASS.21 for the design of work with a recorded expected class. |
| 1.3 | 2026-10-28 | Minor amendment (GOV.41): HW.5, HW.6, and HW.7 apply from CSQ2, with the contract of HW.4 that they fill, and HW.3 and HW.12 stay at CSQ3; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
| 1.3.1 | 2026-10-28 | Editorial amendment (GOV.41): the Notes say that the execution paths are recorded by hardware type where the section Architecture names, outside the classification, as STND.PROJ.1 now has it; no obligation, permission, or defined meaning changes. |
