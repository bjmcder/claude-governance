# Hardware type annex (STND.ANNEX) 1.0

Adopted by The Custodian as revision 1.0 in ledger entry 106 (2026-10-24). This reading copy is composed from the per-provision files in STND/ANNEX/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds one default hardware contract for each hardware type of HW: general-purpose processors, accelerators, quantum processors, embedded controllers, programmable logic, and integrated circuits (STND.ANNEX.5, STND.ANNEX.6, STND.ANNEX.7, STND.ANNEX.8, STND.ANNEX.9, and STND.ANNEX.10). The hardware contract of an execution path adopts the default of its type by citing it with the revision of this standard, in place of stating under HW.4 and HW.5 what the default states (STND.ANNEX.1). The citing contract adds only the statements that the default leaves to it, each property of the path that differs from the default, and each further property on which its component relies (STND.ANNEX.2 and STND.ANNEX.3). A property taken from a default is supported as HW.6 requires, and the citation is no evidence (STND.ANNEX.4). No provision is binding: each is a default (GOV.19), and a project that writes its own hardware contract under HW.4 and HW.5 cites none of them. Each default only tightens the provisions of HW and its sub-profiles on which it rests, and relaxes none (PRIME.15). Where a default is silent, LVL0 and HW govern (GOV.23). At the custodian's direction, the standard is agnostic of platform and vendor: no provision names a language, library, tool, vendor, device, process, or platform, and it leaves those choices to LVL3, one of the levels at which GOV.18 places them (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Capacity, Delivered arithmetic, Execution path, Hardware contract, Hardware fault, Hardware model, Hardware type, and Runtime library have the meanings that HW gives them; Floating-point control state has the meaning that HW.CPU gives it; Offloaded work and Completion status have the meanings that HW.GPU gives them; Calibration record, Error mitigation, and Shot have the meanings that HW.QPU gives them; Configuration and Target model have the meanings that HW.FPGA gives them; Design record, Target, State element, Clock domain, and Operating condition have the meanings that HDES gives them; Corner, Fabrication readiness record, and Manufacturing test have the meanings that HDES.ASIC gives them.

| Term | Definition |
| --- | --- |
| Default contract | The hardware contract that the table of one provision of this standard gives for the execution paths on one hardware type. |
| Citing contract | A hardware contract of an execution path that adopts the default contract for the hardware type of that path by citing it. |

## Notes

Each default contract is the least that a component of its type usually relies on, so that citing it forbids no faster implementation. It admits every reordering, contraction, vectorization, and choice of implementation that the hardware and its software document, and it relies on no timing beyond what the type itself requires. A property that a default marks as not established is one on which the component does not rely; a citing contract that establishes it states the property in place of the default and supports it under HW.6 (STND.ANNEX.2, STND.ANNEX.3). A component that relies on more than its default, on bitwise identity across runs, a stronger ordering, or a timing property, states that reliance in its own contract (STND.ANNEX.2, STND.ANNEX.3). The column Stated by the citing contract holds what the default is unable to know, the number formats and the build settings of the path above all, so that a citation and that column together give everything that HW.4 and HW.5 ask. No default leaves a matter empty: where its source states nothing, the property is not established.

The column Basis names the provision of HW that each row serves. The rows of HW.5, HW.12, and HW.EMBED.4 are completed under STND.ANNEX.2 and the rows of HW.4 under STND.ANNEX.3, so that each obligation starts at the class from which the provision of HW that it serves applies; reliance beyond a default on delivered arithmetic or run-to-run variation is stated under STND.ANNEX.2, and other reliance under STND.ANNEX.3. The rows of HW.6, the Evidence rows of the defaults for programmable logic and integrated circuits, ask nothing of the citing contract beyond what HW.6, HW.FPGA.4, and HW.ASIC.4 already ask. The citation names the revision of this standard, so that a later revision changes no citing contract until that contract cites it; changing the cited revision is a change of contract under DSGN.6, and the evidence of each changed property is renewed as HW.6 asks.

A default contract states properties and is no evidence for them. Each of its properties rests on the documentation of the hardware model and its software, so a citing contract shows that the stated conditions of that documentation hold in its regime of use and confirms its source as HW.6 and VV.2 ask, and marks each property that documentation alone supports (HW.6). A published accuracy is often a maximum found by testing rather than a proven bound, so STND.ANNEX.4 marks it as a tested maximum wherever its documentation does not state the bound as proven, which tells a reviewer where a comparison in units in the last place needs a margin. Each run still confirms the properties it relies on (HW.7), and a path on a general-purpose processor confirms the floating-point control state that its citing contract states, as HW.CPU.3 asks.

Each kind of hardware fault that a default lists as undetected engages HW.10: the path checks its results by a means able to detect that fault, or states the exposure in the record of each result, which costs one statement. The defaults list these kinds because they exist on most hardware; error-correcting memory corrects and detects only the errors within the capability that its documentation states, and a larger error is missed or miscorrected. A hardware model whose documentation states detection of another kind lets the citing contract state that in place of the default (STND.ANNEX.3). For the response to a detected fault that is not corrected, the defaults for general-purpose processors, accelerators, and quantum processors select a halt, or for offloaded work and jobs a resubmission stated in the record of each result, among the responses that HW.8 allows. HW.8 and HW.GPU.3 instantiate PRIME.4; the defaults refer to them and instantiate neither, so no default is forced to binding.

The accelerator default takes the accuracy that the documentation of the compiler and runtime libraries states for each operation, division and square root included, so that it holds on accelerators whose default settings deliver less than correct rounding. The default selects no setting and forbids no faster one, and it already takes the accuracy that the compiler and runtime libraries document for the settings of the path; where other documentation, that of the hardware model for example, states a stronger accuracy, STND.ANNEX.2 has the citing contract state it in place of the default, so that no path runs slower to fit the default. Its ordering of transfers and of the completion of offloaded work is the documented contract of the runtime libraries, which a boundary contract between the host and the accelerator incorporates under HW.13 for each property that it uses; the rest of that boundary contract, its layout, byte order, precision, and ownership, stays the project's. An analog accelerator is an accelerator under HW, and the noise of its computation varies between runs. The quantum processor default treats the noise that the calibration record reports as the noise of the device and not as a hardware fault, as the Term Hardware fault of HW does, and lists a departure of the device from that record during a job as undetected, so that HW.10 has the path check its results, for example by known-answer instances, or state the exposure. The embedded controller default leaves the response to a detected fault, and the states of outputs that drive physical hardware, to the citing contract, because whether a halt is safe is a question for the hazard analysis of PRIME.13 and the safe state that CPS.4 verifies from those states.

The defaults for programmable logic and integrated circuits point to the design record, which HDES.5 already has state each property, limit, and kind of hardware fault that HW.4 and HW.5 ask for, and add only what the design record leaves open: timing that rests on the target maker's models (HDES.10), the marking of properties that rest only on analysis or simulation until device evidence or measurement supports them (HW.FPGA.4, HW.ASIC.4), the fabrication readiness record (HDES.ASIC.12), upsets of state that go undetected without a detection the design implements and HDES.15 verifies, and manufacturing defects that the test misses (HDES.ASIC.11). A configuration whose design record the project does not hold, a supplier's shell or a purchased block among them, takes its properties from the documentation of its supplier under STND.ANNEX.9. They name no device family, process, method, threshold, sample size, or tool, so they stay valid as the technology changes; the confirmations a project buys, their conditions, and their margins are matters for its own instruments (LVL3). A processor realized in programmable logic is programmable logic under HW, so the firmware that it runs belongs to the path that cites the programmable logic default, and the arithmetic of its compiler and build, which HDES.7 does not cover, is stated as for an embedded controller.

Under STND.CLASS.10, each provision instantiates only DSGN.5, REPRO.2, REPRO.3, and VV.1, and the provisions HW.4, HW.5, HW.6, HW.12, and HW.EMBED.4 that instantiate them. STND.ANNEX.3 instantiates only DSGN.5 and HW.4 and applies from CSQ2, the class from which STND.CLASS.10 applies DSGN.5; every other provision applies from CSQ3; work of CSQ4 omits them. A citing contract at CSQ3 carries the rows of HW.4 by the citation alone, and their undetected kinds of fault engage HW.10, at the cost of one statement in the record of each result, which HW.10 asks at CSQ3 only of a contract that states such a fault. Every obligation of this standard arises only for a contract that cites a default, which is the project's choice; a project that writes its own contract meets HW alone. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| HDES.ASIC | Integrated circuit design |
| HW | Execution hardware |
| HW.ASIC | Application-specific integrated circuits |
| HW.CPU | General-purpose processors |
| HW.EMBED | Embedded controllers |
| HW.FPGA | Field-programmable gate arrays |
| HW.GPU | Accelerators |
| HW.QPU | Quantum processors |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| VV | Correctness |

## Provisions

### Adoption

#### STND.ANNEX.1 Adoption by citation

Default. Instantiates DSGN.5, REPRO.2, HW.4, HW.5.

The hardware contract of an execution path MAY state the properties that the default contract for its hardware type gives by a citation of that default contract that names the revision of this standard that it cites (DSGN.5, REPRO.2, HW.4, HW.5).

#### STND.ANNEX.2 Arithmetic, variation, and output statements

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, VV.1, HW.5, HW.12, HW.EMBED.4.

A citing contract SHALL state each property of its execution path that differs from the default of a row whose basis is HW.5, HW.12, or HW.EMBED.4, in place of that default, and each item that its default contract gives in the column Stated by the citing contract of such a row (DSGN.5, REPRO.2, REPRO.3, VV.1, HW.5, HW.12, HW.EMBED.4). Where the component of a citing contract relies on a property of delivered arithmetic or of run-to-run variation that the default contract does not state, the citing contract SHALL state that property (DSGN.5, REPRO.2, REPRO.3, HW.5, HW.12).

#### STND.ANNEX.3 Other statements of citing contracts

Default. Instantiates DSGN.5, HW.4.

A citing contract SHALL state each property of its execution path that differs from the default of a row whose basis is HW.4, in place of that default, and each item that its default contract gives in the column Stated by the citing contract of such a row (DSGN.5, HW.4). Where the component of a citing contract relies on a property of its execution path, other than one of delivered arithmetic or of run-to-run variation, that the default contract does not state, the citing contract SHALL state that property (DSGN.5, HW.4).

#### STND.ANNEX.4 Evidence for default properties

Default. Instantiates DSGN.5, VV.1, HW.6.

The citation of a default contract SHALL NOT be the evidence that HW.6 asks for a property of a citing contract (DSGN.5, VV.1, HW.6). Where the documentation that supports an accuracy that a citing contract takes from its default contract states no proven bound, the citing contract SHALL mark that accuracy as a tested maximum (VV.1, HW.6).

### Default contracts

#### STND.ANNEX.5 General-purpose processor default contract

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12.

The default contract for execution paths on general-purpose processors SHALL be the table of this provision (DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12).

| Matter | Basis | Default | Stated by the citing contract |
| --- | --- | --- | --- |
| Delivered arithmetic | HW.5 | The number formats that the component uses, evaluated in the formats that the compiler documents for them; basic operations and square root correctly rounded in each format for which the processor documents correct rounding, and otherwise to the accuracy that its documentation states; rounding and the handling of subnormal values as the floating-point control state sets them; non-finite values propagated without traps; fused multiply-add and reordered combination wherever the build admits them, with no result relied upon to be identical across those choices; elementary functions to the accuracy that their library documents, and otherwise not established | The number formats; the rounding and the handling of subnormal values that the floating-point control state sets at the start of a process; each reduced-precision or matrix instruction mode that the path uses, with its formats; each build setting or library default that admits approximation, changes rounding, flushes subnormal values, or enables traps, with its effect |
| Choices made at run time | HW.5 | The range of delivered arithmetic over the implementations that the path chooses at run time not established | Nothing |
| Hardware models | HW.5 | Delivered arithmetic not established as the same on each hardware model that the path admits | Nothing |
| Memory and ordering | HW.4 | The memory model of the language and the synchronization of its libraries, with no stronger ordering relied upon | Nothing |
| Timing | HW.4 | None relied upon | Nothing |
| Limits | HW.4 | The memory and storage that the platform makes available to the process | Each other limit on capacity, timing, or power that the component is able to reach in its regime of use |
| Hardware faults | HW.4 | Errors in memory: corrected and detected within the capability that the documentation of the hardware model states for its error correction, and otherwise undetected; an uncorrected error that the platform reports: detected and not corrected; a changed bit in storage, a register, or a link, a wrong result from a processing unit, and a lost message: undetected; a loss of power: the run ends | Nothing |
| Response to detected faults | HW.4 | The process or the run halts, with an actionable diagnosis that includes what the platform reports, as HW.8 requires | Nothing |
| Run-to-run variation | HW.12 | The order in which values are combined, the scheduling of concurrent work, and the choices made at run time among implementations able to vary between runs on identical recorded inputs | Nothing |

#### STND.ANNEX.6 Accelerator default contract

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12.

The default contract for execution paths on accelerators SHALL be the table of this provision (DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12).

| Matter | Basis | Default | Stated by the citing contract |
| --- | --- | --- | --- |
| Delivered arithmetic | HW.5 | The number formats that the component uses; each operation, division and square root included, to the accuracy that the documentation of the compiler and runtime libraries states for the settings of the path, and otherwise not established; subnormal and non-finite values handled as that documentation states for those settings, and otherwise not established; fused operations, reduced-precision modes, and modes of matrix units wherever a setting of the path or a default of a runtime library selects them; elementary functions to the accuracy that their library documents, and otherwise not established | The number formats; each setting and library default that selects a fused operation, a reduced-precision mode, a mode of a matrix unit, an approximate function, or the flushing of subnormal values, with the formats of its inputs and of its accumulation |
| Choices made at run time | HW.5 | The range of delivered arithmetic over the implementations that the path chooses at run time not established | Nothing |
| Hardware models | HW.5 | Delivered arithmetic not established as the same on each hardware model that the path admits | Nothing |
| Memory and ordering | HW.4 | The memory model of the programming model of the accelerator and the synchronization of its runtime libraries; atomic operations and reductions combined in an unspecified order; transfers between the host and the accelerator, and the completion of offloaded work, ordered as the runtime libraries document | Nothing |
| Timing | HW.4 | None relied upon | Nothing |
| Limits | HW.4 | The accelerator memory, and the limits on offloaded work, that the runtime libraries report | Each other limit on capacity, timing, or power that the component is able to reach in its regime of use |
| Hardware faults | HW.4 | Errors in accelerator memory: corrected and detected within the capability that the documentation of the hardware model states for its error correction, and otherwise undetected; a reset of the accelerator, a timeout, and an uncorrected error that the completion status or a runtime library reports: detected and not corrected; a changed bit in storage, a register, or a link, a wrong result from a processing unit, and a lost message: undetected; a loss of power: the run ends | Nothing |
| Response to detected faults | HW.4 | The run halts, or the path submits the offloaded work again from inputs that the fault leaves unaffected and states the event in the record of each result as HW.9 asks, with an actionable diagnosis that includes what the completion status or the runtime library reports, as HW.8 and HW.GPU.3 require | Nothing |
| Run-to-run variation | HW.12 | The order in which values are combined, the scheduling of concurrent work, and the choices made at run time among implementations, and the noise of each analog computation, able to vary between runs on identical recorded inputs | Nothing |

#### STND.ANNEX.7 Quantum processor default contract

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12.

The default contract for execution paths on quantum processors SHALL be the table of this provision (DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12).

| Matter | Basis | Default | Stated by the citing contract |
| --- | --- | --- | --- |
| Delivered arithmetic | HW.5 | For the classical operations that the path performs, the default contract of STND.ANNEX.5; for the classical processing of outcomes that the provider performs, the arithmetic that the provider documents | For the classical operations that the path performs, each item that STND.ANNEX.5 gives in its column Stated by the citing contract; each classical processing of outcomes that the provider performs and does not document |
| Quantum operations | HW.4 | The native operations, connectivity, measurement basis, and limits of the device as its provider or operator documents them at the time of each job; their error rates as the calibration record of each job reports them, as tested values and not as bounds; no noise model relied upon beyond those error rates and the assumptions about device noise that the record of HW.QPU.5 states for the error mitigation in force | Nothing |
| Outcomes | HW.4 | Statistical; no property of an individual shot relied upon | Nothing |
| Choices made at run time | HW.5 | The compilation, assignment of qubits, and error mitigation that the provider chooses for each job, as the record of HW.QPU.3 states them; the output distribution not established as the same across those choices | Nothing |
| Hardware models | HW.5 | Error rates and output distributions not established as the same on each device and calibration that the path admits | Nothing |
| Memory and ordering | HW.4 | None relied upon beyond the outcomes of each job as returned | Nothing |
| Timing | HW.4 | None relied upon | Nothing |
| Limits | HW.4 | The limits on qubits, circuit size or duration, shots, and jobs that the provider or operator documents at the time of each job | Each other limit on capacity, timing, or power that the component is able to reach in its regime of use |
| Hardware faults | HW.4 | A job that the provider reports as failed, canceled, or incomplete: detected and not corrected; a departure of the device from its calibration record during a job: undetected; noise that the calibration record reports: no hardware fault | Nothing |
| Response to detected faults | HW.4 | The path halts the computation of each result that depends on the job, or submits the job again and states the event in the record of each result as HW.9 asks, with an actionable diagnosis that includes what the provider reports, as HW.8 requires | Nothing |
| Run-to-run variation | HW.12 | Outcomes varying from shot to shot; compilation without a recorded seed, assignment of qubits, error mitigation, and calibration able to vary between runs on identical recorded inputs; for the classical operations that the path performs, the variation that STND.ANNEX.5 states | Nothing |

#### STND.ANNEX.8 Embedded controller default contract

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12.

The default contract for execution paths on embedded controllers SHALL be the table of this provision (DSGN.5, REPRO.2, REPRO.3, HW.4, HW.5, HW.12).

| Matter | Basis | Default | Stated by the citing contract |
| --- | --- | --- | --- |
| Delivered arithmetic | HW.5 | The number formats that the component uses, with the rounding and the handling of subnormal and non-finite values that the documentation of the compiler and its runtime library states for the target and the build settings, software floating point included for each format without hardware support, and otherwise not established; fused and contracted operations wherever the build admits them; elementary functions to the accuracy that their library documents, and otherwise not established | The number formats; each build setting that changes their arithmetic |
| Choices made at run time | HW.5 | The range of delivered arithmetic over the implementations that the path chooses at run time not established | Nothing |
| Hardware models | HW.5 | Delivered arithmetic not established as the same on each model of controller that the path admits | Nothing |
| Memory and ordering | HW.4 | The memory map of the build; the memory model of the language and the synchronization of its libraries, for the firmware and its interrupt handlers; the ordering of interrupts, and of accesses to memory-mapped devices, that the documentation of the controller states | Nothing |
| Timing | HW.4 | The deadlines that the component states under HW.20; the accuracy of each clock source that the documentation of the controller states, and otherwise not established | Each clock source, period, and latency on which the component relies |
| Limits | HW.4 | The memory that the memory map of the build gives; the endurance of writable memory and the limits of supply that the documentation of the controller states | Each other limit on capacity, timing, or power that the component is able to reach in its regime of use |
| Hardware faults | HW.4 | A reset by brown-out or by watchdog, and a loss of power: detected by firmware that reads the cause of each reset, and otherwise undetected; a changed bit in memory, a register, or a link, a wrong result from a processing unit, and a lost message: undetected | Nothing |
| Response to detected faults | HW.4 | The response that the citing contract states, as HW.8 requires | The response to each detected fault that is not corrected |
| Outputs at reset and halt | HW.EMBED.4 | Not established | For each output commanding, configuring, or powering physical hardware, its states and their evidence as HW.EMBED.4 asks |
| Run-to-run variation | HW.12 | The order in which values are combined, the timing of interrupts relative to the code they interrupt, and the scheduling of concurrent work able to vary between runs on identical recorded inputs | Nothing |

#### STND.ANNEX.9 Programmable logic default contract

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, VV.1, HW.4, HW.5, HW.6, HW.12.

The default contract for execution paths on programmable logic SHALL be the table of this provision (DSGN.5, REPRO.2, REPRO.3, VV.1, HW.4, HW.5, HW.6, HW.12). For a configuration whose design record the project does not hold, each entry of that table that rests on the design record SHALL be read as resting on the documentation that the supplier of the configuration gives, and each other property that this documentation does not state, other than a kind of hardware fault, as not established (DSGN.5, VV.1, HW.4, HW.5, HW.6).

| Matter | Basis | Default | Stated by the citing contract |
| --- | --- | --- | --- |
| Delivered arithmetic | HW.5 | As the design record states under HDES.5 and HDES.7; for firmware that a processor realized in the configuration runs, the delivered arithmetic of the default contract of STND.ANNEX.8 | For firmware that a processor realized in the configuration runs, each item that STND.ANNEX.8 gives for delivered arithmetic in its column Stated by the citing contract |
| Choices made at run time | HW.5 | The range of delivered arithmetic over the configurations that the path loads during a run not established | Nothing |
| Hardware models | HW.5 | As the design record states for each target model that the path admits | Nothing |
| Memory and ordering | HW.4 | As the contract of the design record states under HDES.4 and HDES.5 | Nothing |
| Timing | HW.4 | Of interfaces, as the contract of HDES.4 states; of internal paths, as the analysis of HDES.10 shows at each operating condition that the timing models of the target cover, resting on those models; not established at each operating condition that the record of that analysis states as not analyzed | Nothing |
| Limits | HW.4 | As the design record states under HDES.4 and HDES.5 | For a configuration whose design record the project does not hold, each limit on capacity, timing, or power that the component is able to reach in its regime of use and that the documentation of its supplier does not state |
| Evidence | HW.6 | Each property that the design record marks under HDES.5 as resting only on analysis or simulation marked so in the citing contract, in each part of the regime of use that evidence under HW.FPGA.4 from a device of the target model does not cover | Nothing |
| Hardware faults | HW.4 | Upsets of configuration memory and of state elements: undetected, other than by a detection or correction that the design implements and the verification of HDES.15 shows, or that the documentation of the target model states; every other kind: as the design record states under HDES.5, and otherwise undetected | Nothing |
| Response to detected faults | HW.4 | As the design record states under HDES.5, as HW.8 requires | Each response that neither the design record nor the documentation of the supplier of the configuration states |
| Run-to-run variation | HW.12 | The configurations that the path loads during a run, the value after power-on of each state element that the design leaves unset under HDES.12, and each order of combination and each crossing between clock domains that the contract of HDES.4 does not fix, able to vary between runs on identical recorded inputs; for firmware that a processor realized in the configuration runs, the variation that STND.ANNEX.8 states | Nothing |

#### STND.ANNEX.10 Integrated circuit default contract

Default. Instantiates DSGN.5, REPRO.2, REPRO.3, VV.1, HW.4, HW.5, HW.6, HW.12.

The default contract for execution paths on integrated circuits SHALL be the table of this provision (DSGN.5, REPRO.2, REPRO.3, VV.1, HW.4, HW.5, HW.6, HW.12).

| Matter | Basis | Default | Stated by the citing contract |
| --- | --- | --- | --- |
| Delivered arithmetic | HW.5 | As the design record states under HDES.5 and HDES.7 | Nothing |
| Choices made at run time | HW.5 | As the design record states under HDES.5 | Nothing |
| Hardware models | HW.5 | As the design record states for the design revision of the device | Nothing |
| Memory and ordering | HW.4 | As the contract of the design record states under HDES.4 and HDES.5 | Nothing |
| Timing | HW.4 | Of interfaces, as the contract of HDES.4 states; of internal paths, as the analysis of HDES.10 shows on the layout at each operating condition that the timing models of the target cover, resting on those models; not established at each operating condition that the record of that analysis states as not analyzed | Nothing |
| Analog and mixed-signal behavior | HW.4 | As the design record states under HDES.5, at each corner of HDES.ASIC.5 | Nothing |
| Limits | HW.4 | As the design record states under HDES.4 and HDES.5 | Nothing |
| Evidence | HW.6 | The evidence before fabrication that the fabrication readiness record of HDES.ASIC.12 states, where the design record holds one; each property that the design record marks under HDES.5 as resting only on analysis or simulation, and each property whose only evidence the fabrication readiness record marks as a realization in programmable logic, marked so in the citing contract until measurement under HW.ASIC.4 supports it; no property relied upon to hold alike on every fabricated device beyond the spread that HW.ASIC.4 records | Nothing |
| Hardware faults | HW.4 | Upsets of state elements: undetected, other than by a detection or correction that the design implements and the verification of HDES.15 shows; a manufacturing defect that the coverage of HDES.ASIC.11 leaves undetected: undetected; every other kind: as the design record states under HDES.5, and otherwise undetected | Nothing |
| Response to detected faults | HW.4 | As the design record states under HDES.5, as HW.8 requires | Nothing |
| Run-to-run variation | HW.12 | The choices made at run time that the design record states, the value after power-on of each state element that the design leaves unset under HDES.12, the noise of each analog or mixed-signal block, and each order of combination and each crossing between clock domains that the contract of HDES.4 does not fix, able to vary between runs on identical recorded inputs | Nothing |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
