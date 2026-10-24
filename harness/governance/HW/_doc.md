---
id: "HW"
level: "LVL1"
kind: "profile"
title: "Execution hardware"
status: "adopted"
adopted: "2026-10-17"
revision: "1.1.1"
selector: "Binds when a component of the work executes, or is admitted to execute, on a hardware type that HW.1 names (HW.1)."
parent: null
adopted_by: "The Custodian"
---

## Purpose and scope

This profile holds the obligations of work whose components execute on hardware: general-purpose processors, accelerators, quantum processors, embedded controllers, and realized designs of programmable logic and integrated circuits. Hardware changes results without changing code. It does so through the arithmetic it delivers, the order in which it combines values, the limits it imposes, the faults it meets or misses, and the firmware, drivers, and libraries through which code reaches it. A result that is correct on one machine is therefore able to be silently wrong, or merely different, on another. The profile asks that what each component relies on from its hardware be stated as a contract, supported by evidence, and confirmed before each run. It asks that the boundaries between hardware types and models be stated and checked, and that each alternative execution path be verified against its component's one contract. It asks that the budgets of constrained targets be verified on the target, and that faults, fallbacks, and undetected-fault exposure be visible. It names no language, library, tool, technology, platform, process, or method (GOV.18). The sub-profiles HW.CPU, HW.GPU, HW.QPU, HW.EMBED, HW.FPGA, and HW.ASIC add obligations specific to each hardware type (GOV.27). The design of programmable logic and integrated circuits belongs to HDES; this profile governs execution on a realized design.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Accelerator | A processor that executes only work that a host processor offloads to it, other than a quantum processor, programmable logic, or an integrated circuit. |
| Accelerator execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on an accelerator. |
| Alternative execution path | One of two or more execution paths of a component, each of which computes the component's results without the others. |
| Capacity | A limit of hardware on memory, storage, buffers, queues, counters, stored energy, or supplied power beyond which an operation fails, loses data, or resets the hardware. A limit at which the hardware only slows execution is not a capacity. |
| Boundary contract | The contract at an interface boundary between execution paths on different hardware types or hardware models. |
| Constrained target | An execution path that has a deadline whose miss is able to change either a result that the path goes on to report or rely on or a command that the path issues to physical hardware, or on which reaching a capacity of its hardware is able to change or lose a result without a halt or visible degradation. |
| Delivered arithmetic | The number formats, rounding, handling of subnormal and non-finite values, fusion and contraction of operations, order in which values are combined, and accuracy of elementary functions that an execution path gives the numerical operations of a component, as its modes, library defaults, options, and choices made at run time set them. |
| Embedded controller | A processor, other than programmable logic or an integrated circuit, that executes firmware to control or monitor a device, with no operating system between the firmware and the device, or with one whose scheduling the firmware's deadlines constrain. |
| Embedded controller execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on an embedded controller. |
| Execution path | A component together with a hardware type on which it executes, and the hardware models, firmware, drivers, runtime libraries, and settings that it admits there. |
| General-purpose processor | A processor that executes a stored program, other than an accelerator, a quantum processor, an embedded controller, programmable logic, or an integrated circuit. |
| General-purpose processor execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on a general-purpose processor. |
| Hardware contract | The contract of an execution path: the behavior of its hardware type, hardware models, firmware, drivers, runtime libraries, and settings that the component relies on in its regime of use. |
| Hardware fault | A departure of hardware from its specified behavior: a changed bit in memory, storage, a register, or a link; a wrong result from a processing unit; a lost message; or a loss of power. The noise of a quantum processor that its hardware contract states is not a hardware fault. |
| Hardware model | The design and revision of a hardware device, as its maker or its design record identifies it. |
| Hardware type | One of the kinds of execution hardware for which the selector table of HW.1 gives an attribute. |
| Integrated circuit | A device fabricated from a hardware description whose design record the project holds, other than programmable logic. |
| Integrated circuit execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on an integrated circuit. |
| Programmable logic | A configuration of a device whose logic is configured after manufacture. |
| Programmable logic execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on programmable logic. |
| Quantum processor | Hardware that computes a result by executing quantum circuits, or by evolving quantum states under controlled interactions, and returns measured outcomes; a device that measures a physical quantity through quantum states is not a quantum processor. |
| Quantum processor execution | An attribute, true when the classification records that a component of the work whose behavior affects a result the work reports or relies on executes, or is admitted to execute, on a quantum processor. |
| Reference path | The alternative execution path of a component on which the component's obvious implementation executes, taken with that implementation alone, against which its other alternative execution paths are verified (SIMPL.7). Where the alternative execution paths of a component execute one source, the reference path is the path whose delivered arithmetic the component's specification assumes. |
| Runtime library | A library through which a component reaches its hardware and that sets at least one of its delivered arithmetic, its placement of data in memory, its scheduling of concurrent work, or its choice at run time among implementations. |

## Selector

HW.1 states the selector: one attribute per hardware type, each defined here. The domain items are execution paths, hardware contracts, boundary contracts, constrained targets, and claims comparing the performance of execution paths. Because each provision names as its subject an execution path, a contract, or a record or claim about one (STND.DRAFT.37, STND.DRAFT.38), a provision about an execution path on one hardware type imposes nothing on a component that has no path on that type. A component that executes only on general-purpose processors meets this profile and HW.CPU for its own path, and the boundary contracts it shares with components on other types; it meets no obligation specific to accelerators, quantum processors, or embedded controllers. Each attribute is also true where the classification records that a component whose behavior affects a result the work reports or relies on is admitted to execute on that type. Adding a hardware type otherwise revises the classification, which the human owner adopts (GOV.24, GOV.50); a classification that admits the hardware types the work plans to use lets an agent add a path on an admitted type without a further decision of the human owner, and costs nothing before the path exists. Hardware of a kind that no attribute names is governed by LVL0 and by the nearest of this profile and its sub-profiles applied by analogy, with the choice of analogue recorded (GOV.29). A processor realized in programmable logic is programmable logic. Analog and neuromorphic devices are accelerators where a host offloads work to them, and otherwise fall under GOV.29. Each sub-profile's selector restates its attribute from HW.1.

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

HW.8 states how PRIME.4 applies to detected, uncorrected hardware faults and to exhausted capacity, and binds at every class, adding nothing to the floor that PRIME.4 does not already hold. For a run of several processes that compute one result together, HW.8 is read as asking the whole run to halt, degrade visibly, or transition to a designed safe state. A process that halts while the others wait on it leaves a silent hang. STND.MPI.6 states how the halt of one process reaches the others in a program that uses the Message Passing Interface. Every other provision except HW.1 and HW.2 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC. Each such provision inherits their rank and waivability (GOV.17) and is proportioned to class (GOV.11): under the project's class criteria, such as STND.CLASS.10, it applies from the least severe class at which those criteria require an LVL0 obligation it instantiates, and under STND.CLASS.10 work of CSQ4 omits it. Where a provision applies from a less severe class than one it builds on, it tightens above the floor (PRIME.15). Under STND.CLASS.10, HW.4, HW.11, HW.13, and HW.14 apply from CSQ2, and every other provision except HW.8 from CSQ3. At CSQ3 a hardware contract therefore holds what HW.5, HW.6, and HW.7 ask of it, the delivered arithmetic and the evidence for each property relied upon, and not yet the full statement of HW.4; HW.10 binds there only where a contract states an undetected fault, which at CSQ3 it is not yet asked to do. A silent fallback or an unmonitored overrun is a silent misalignment, and a fallback found only after a long run wastes the run. From CSQ3, HW.3 and HW.9 put each fallback in the record of each result it affects, HW.19 reports it to the operator at its first occurrence, and the record of the run's resource use counts fallbacks, because a fallback is a regression in resource use that RSRC.2 makes visible from the first run; HW.21 monitors budgets and reports overruns from the class at which RSRC.2 applies. Both reports therefore tighten above the class at which INTPR.7 applies, at the cost of one message each. Because nearly all computational work executes on general-purpose processors, this profile binds widely, and most of its obligations are light at the less severe classes. The type detail that a sub-profile does not hold sits in the hardware annex (STND.ANNEX).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
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
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-17 | Adopted. |
| 1.0.1 | 2026-10-18 | Editorial amendment (GOV.41): the Notes describe HDES as adopted, citing HDES.5, in place of a clause that its adoption made stale; no obligation changes. |
| 1.0.2 | 2026-10-19 | Editorial amendment (GOV.41): the informative Notes describe the sub-profiles and CPS as adopted, citing CPS.3, CPS.4, and CPS.8; no obligation changes. |
| 1.1 | 2026-10-19 | Minor amendment (GOV.41): HW.20 asks for a bound on worst-case execution time only for a deadline whose miss the hazard analysis of PRIME.13 identifies as hazardous, and accepts a bound or detection of each miss, stated in the record, for every other deadline that changes a command or a result; the Notes state the same. |
| 1.1.1 | 2026-10-24 | Editorial amendment (GOV.41): the informative Notes state that, for a run of several processes that compute one result together, HW.8 is read as asking the whole run to halt, degrade visibly, or transition to a designed safe state, citing STND.MPI.6, and References lists STND.MPI; no obligation changes. |
