---
id: "STND.ANNEX"
level: "LVL2"
kind: "standard"
title: "Hardware type annex"
status: "adopted"
revision: "1.0"
adopted: "2026-10-24"
adopted_by: "The Custodian"
instantiates: ["GOV.18", "GOV.19"]
rank: null
waivable: false
---

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

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-24 | Adopted. |
