---
id: "HDES"
level: "LVL1"
kind: "profile"
title: "Hardware design"
status: "adopted"
adopted: "2026-10-18"
revision: "1.0.1"
selector: "Binds when the work produces, or is admitted to produce, a hardware description to be realized as a configuration of programmable logic or as an integrated circuit (HDES.1)."
parent: null
adopted_by: "The Custodian"
---

## Purpose and scope

This profile holds the obligations of work that produces a hardware description to be realized as a configuration of programmable logic or as an integrated circuit, from the description to the first loading of a configuration or the submission of a layout for fabrication. A hardware description fails silently in ways software rarely does: a simulation that the transformed logic does not match, a path that no timing constraint covers or that a wrong exception hides, a signal that crosses between clocks without synchronization, a register whose power-on value nobody set, a warning that reported a changed behavior and was ignored, arithmetic narrower than the computation needs or that clamps without a trace, and fault mitigation that a transformation removed. The profile asks for a design record from which each realization is regenerated, a stated contract, verification of the description that runs without a manual step, equivalence of the description and the netlist, closed timing, verified crossings, a defined initial state, visible saturation, and recorded margins. Each provision is satisfied or not on evidence that the design record holds and that an agent or an automated check is able to evaluate. It names no language, tool, vendor, process, design kit, or method (GOV.18); the technology detail belongs in planned LVL2 standards. The sub-profiles HDES.FPGA and HDES.ASIC add what is specific to each realization (GOV.27); the test, validation, and use of a realized device are governed by HW and its sub-profiles HW.FPGA and HW.ASIC.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Hardware description | A description of a design, in a language for hardware, as a schematic, or as a drawn layout, from which a configuration of programmable logic or the layout of an integrated circuit is produced. |
| Design | A hardware description together with its constraints, its contract, and its design record. |
| Design record | The record of a design that identifies everything from which each realization is produced, and holds its contract and its verification evidence. |
| Target | The model of programmable logic device, or the fabrication process, for which a realization is produced. |
| Realization | A configuration of programmable logic, or a layout of an integrated circuit, produced from a design. |
| Transformation step | A step, automated or manual, that produces from a representation of a design another representation closer to its realization. |
| Netlist | A representation of a design, produced by a transformation step, as the interconnection of the primitive elements of its target. |
| Reference model | An executable model of a design's contract against which its hardware description is verified. |
| State element | An element of a design that holds a value from one clock edge or event to the next. |
| Clock domain | The state elements of a design that are clocked by one clock, or by clocks in a fixed relation of phase. |
| Operating condition | A combination of manufacturing variation, supply voltage, temperature, clock frequency, aging, and accumulated radiation dose that the regime of use of a realization admits. |
| Programmable logic design | An attribute, true when the classification records that the work produces, or is admitted to produce, a hardware description to be realized as a configuration of programmable logic. |
| Integrated circuit design | An attribute, true when the classification records that the work produces, or is admitted to produce, a hardware description to be realized as an integrated circuit. |

## Selector

HDES.1 states the selector: one attribute per kind of realization, each defined here, which the sub-profiles HDES.FPGA and HDES.ASIC each give one of (STND.DRAFT.36). The domain items are designs and their realizations, and each provision names one of them, or a part, representation, record, or verification of one, or a warning of a transformation step that produces one, as its subject (STND.DRAFT.37). The design of board-level electronics is outside this profile and is governed by LVL0 and the nearest profile applied by analogy, with the choice of analogue recorded (GOV.29); fabrication, packaging, and a fabrication process enter as external components (REPRO.9). Where the classification of work that designs hardware also records the attribute Numerical, NUMER binds it as well.

## Where the rest lives

LVL0 and the documents named here already govern these matters of hardware design, and this document does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Execution on a realized design: its hardware contract, evidence, and confirmation | HW.4, HW.6, HW.FPGA, HW.ASIC |
| Test, characterization, and validation of a configured or fabricated device | HW.6, HW.FPGA, HW.ASIC |
| Contracts of external components, intellectual-property blocks and fabrication services included | DSGN.5, REPRO.9 |
| Verification against an oracle produced without the implementation, and validation against the real world | VV.1, VV.4, STND.CLASS.10 |
| Re-verification of each change against the evidence it is able to affect | VV.8 |
| Required precision and the tolerance basis of numerical comparisons | NUMER.5, NUMER.11 |
| Comparison tiers, bitwise identity included | STND.VVUQ.1, STND.VVUQ.2 |
| Release or deployment, submission for fabrication included, on the human owner's decision | QA.10, GOV.50 |
| Reserved actions, explicit monetary transactions included | PRIME.6 |
| Implicit expenditure and remote writes whose effect is irrevocable | PRIME.7, PRIME.8, GUARD.11 |
| Configuring or powering physical hardware | PRIME.7, PRIME.13 |

## Notes

Hardware design is carried out with many languages, schematic and layout editors, and tools, open and proprietary, which change faster than the failures they share. Each provision here therefore states an outcome that holds whatever the language, tool, or process, and is checked from the design record: a record that is present or absent, a check that ran or did not, a verdict, a coverage figure, or a list of what is not verified. The checks themselves, and the representations they read, are left to the work and to planned LVL2 standards. A step that no available check reads is not forbidden; it is named as unverified (HDES.8), and the gap travels with the design.

HDES.4 asks for the contract against which everything else is verified: behavior at the interfaces, timing relations, limits, the shortest asynchronous pulse captured, and the regime of use, supply ramp rates included, stated before verification judges the design (VV.3). Where a realization is part of an execution path under HW, HDES.5 adds what HW.4, HW.5, and HW.13 ask, and marks which properties rest only on analysis or simulation. HW.FPGA.4 and HW.ASIC.4 then have each such property confirmed on devices or stated as unconfirmed in each result that relies on it. The fault kinds include upsets of state by radiation where the regime of use exposes the device to them.

HDES.6 asks that verification run from the design record without a manual step and give a verdict per property, so that each change is re-verified against the evidence it is able to affect (VV.8) by rerunning it, and an agent or an automated check reads the result without judgment. A bounded proof, a timeout, or an aborted run is inconclusive, and leaves its property uncovered rather than passed. A waveform inspected by eye is a diagnostic aid, not a verdict. The reference model is the obvious implementation of the contract (SIMPL.7). From CSQ2 it is produced without the hardware description (VV.1, STND.CLASS.10); at CSQ3 it may be derived from the description, and a comparison only with the design's earlier outputs is a regression guard, labeled as one (VV.7). The same model can serve as the reference path of HW.15 when a realized design is an alternative execution path.

A simulation can pass while the transformed logic differs, through a sensitivity, an initial value, or an unknown value that simulation treats optimistically; HDES.8 closes that gap by repeating the verification on the netlist or by a check of equivalence, and names as unverified each part that the check leaves uncompared and each step after the netlist it reads. An equivalence check reads the description as the transformation does, so it settles a mismatch of simulation only where it interprets the description as the verification did, which is why HDES.9 accepts its evidence only on that condition. Later steps that change the netlist produce netlists too, under the Netlist Term. A transformation can warn of an inferred storage element, a truncation, or a signal with several drivers; HDES.9 has each warning resolved, covered by evidence, or matched by a recorded rule, so that the many routine warnings of a library are dismissed once, by kind and source, and not one by one.

A path that no constraint covers is never analyzed, and a wrong exception hides a failing path, so HDES.10 asks for rules that name their paths and for each exception to be checked against the description; an exception on a crossing between clock domains is checked by the evidence of HDES.11. Paths from port to port are among the paths analyzed. Where the timing models of a target do not cover a condition, the analysis says so rather than claiming it. A signal that crosses between clocks, or an external input sampled without synchronization, fails rarely and irreproducibly. HDES.11 asks for a stated synchronization, or a protocol that holds a quasi-static input stable while it is sampled, and an analysis of the netlist, because a transformation can retime, merge, or pack a synchronizer while equivalence still holds. The output of a comparator or other analog block sampled by a clock is an asynchronous input of this kind. A register whose power-on value nobody set behaves one way in a simulator that zeroes it and another in hardware; HDES.12 verifies from every state, by proof, or from a recorded number of random states.

A transformation can merge triplicated registers or strip a safe encoding while equivalence passes, so HDES.15 verifies each stated mitigation that the design's logic implements on the netlist, by fault injection or proof; mitigation inside a fixed block of the target, a memory's error correction for instance, rests on the target's documentation under HW.6. HDES owns the design record as a shared matter, which HW.FPGA and HW.ASIC address (HW.FPGA.2, HW.ASIC.2). A processor realized in programmable logic is programmable logic under HW, so its firmware is not bound by HW.EMBED; HW.FPGA leaves its treatment to the project's own instruments (LVL3).

Arithmetic in hardware is usually fixed point. HDES.7 has the record state the delivered arithmetic that HW.5 asks, and verifies at two levels: the description bit for bit against a model of that arithmetic, and that model within a precision that the record derives from the required precision of the results it feeds, by a tolerance fixed before the comparison. The stated arithmetic rounds the real-valued computation, which is numerical error under NUMER.5, and may also approximate it, as a truncated multiplier or a table in place of a function does; each such approximation is a retained performance approximation, listed under NUMER.16 and verified as NUMER.17 asks, at each reported numerical result it affects. Where the outputs of the design are themselves reported numerical results, the comparison of HDES.7 is that verification; where they feed a later computation, NUMER.17 applies at the result that computation reports. A converter between analog values and a number format is verified against its contract under HDES.6, not bit for bit.

Saturation and wrap-around other than the function an operation is specified to compute are silent clamping, which PRIME.4 forbids at every class; HDES.14 makes each occurrence visible, typically by a flag per operation or group that holds until it is read, at the cost of a register. A counter that the specification states as modular, a limiter, and the rail saturation that forms an analog characteristic compute their specified function and fall outside HDES.14; saturation at a limit of a number format falls within it even where the specification states it. For a path executing on the design, a set flag is a reached limit of its hardware under HW.9.

Submitting a design for fabrication releases it, and the decision to release is the human owner's (QA.10, GOV.50); HDES.ASIC gives the owner the record on which to decide. Every submission is a remote write whose effect is irrevocable, which an agent performs only under a per-action authorization (PRIME.7, GUARD.11); one that invokes a payment is a reserved action that only the human owner executes (PRIME.6); and one that consumes capacity already paid for proceeds only on an estimate that the human owner authorizes (PRIME.8). Loading a configuration into a device that commands, configures, or powers physical hardware needs the authorization of PRIME.7 and the owner-adopted hazard analysis and verified safe state of PRIME.13, and a load that the hazard analysis marks as hazardous or irreversible is reserved (PRIME.6).

HDES owns one shared matter, the design record of a realized design, and addresses four that other profiles own (HDES.2): the hardware contract of an execution path, through HDES.5, which cites HW.4, HW.5, and HW.6, and HDES.7, which cites HW.5; the boundary contract between execution paths, through HDES.5, which cites HW.13; and the precision a result requires and the tolerance basis of a numerical comparison, through HDES.7, which cites NUMER.5 and NUMER.11.

HDES.14 states how PRIME.4 applies to saturation and overflow, and binds at every class, adding nothing to the floor that PRIME.4 does not already hold. Every other provision except HDES.1 and HDES.2 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC, inherits their rank and waivability (GOV.17), and is proportioned to class (GOV.11): under the project's class criteria, such as STND.CLASS.10, it applies from the least severe class at which those criteria require an LVL0 obligation it instantiates, and under STND.CLASS.10 work of CSQ4 omits it. Under STND.CLASS.10, HDES.5 applies from CSQ2, and every other such provision from CSQ3. Some provisions apply at CSQ3 content of obligations that STND.CLASS.10 first asks at CSQ2 or CSQ1: a contract for each external component and for hardware (DSGN.5), a schema for each data structure crossing an interface (DSGN.4), verification of the invariants of each protocol for shared state (DSGN.15), documentation of the limits of validity (INTPR.10), and verification of each assembly and of the integrated system (VV.6). Each such provision tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| HW.ASIC | Application-specific integrated circuits |
| HW.FPGA | Field-programmable gate arrays |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative text describes HW.FPGA and HW.ASIC as adopted, citing HW.FPGA.2, HW.FPGA.4, HW.ASIC.2, and HW.ASIC.4; no obligation changes. |
