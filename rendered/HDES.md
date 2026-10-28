# Hardware design (HDES) 1.0.4

Adopted by The Custodian as revision 1.0 in ledger entry 72 (2026-10-18); revised to 1.0.1 in entry 85 (2026-10-19), 1.0.2 in entry 170 (2026-10-25), 1.0.3 in entry 249 (2026-10-28), and 1.0.4 in entry 299 (2026-10-28). This reading copy is composed from the per-provision files in HDES/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This profile holds the obligations of work that produces a hardware description to be realized as a configuration of programmable logic or as an integrated circuit, from the description to the first loading of a configuration or the submission of a layout for fabrication. A hardware description fails silently in ways software rarely does: a simulation that the transformed logic does not match, a path that no timing constraint covers or that a wrong exception hides, a signal that crosses between clocks without synchronization, a register whose power-on value nobody set, a warning that reported a changed behavior and was ignored, arithmetic narrower than the computation needs or that clamps without a trace, and fault mitigation that a transformation removed. The profile asks for a design record from which each realization is regenerated, a stated contract, verification of the description that runs without a manual step, equivalence of the description and the netlist, closed timing, verified crossings, a defined initial state, visible saturation, and recorded margins. Each provision is satisfied or not on evidence that the design record holds and that an agent or an automated check is able to evaluate. It names no language, tool, vendor, process, design kit, or method (GOV.18); the technology detail belongs in LVL2 standards, STND.SV among them. The sub-profiles HDES.FPGA and HDES.ASIC add what is specific to each realization (GOV.27); the test, validation, and use of a realized device are governed by HW and its sub-profiles HW.FPGA and HW.ASIC.

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

HDES.1 states the selector: one attribute per kind of realization, each defined here, which the sub-profiles HDES.FPGA and HDES.ASIC each give one of (HDES.FPGA.1, HDES.ASIC.1, STND.DRAFT.36). The domain items are designs and their realizations, and each provision names one of them, or a part, representation, record, or verification of one, or a warning of a transformation step that produces one, as its subject (STND.DRAFT.37). The design of board-level electronics is outside this profile and is governed by LVL0 and the nearest profile applied by analogy, with the choice of analogue recorded (GOV.29); fabrication, packaging, and a fabrication process enter as external components (REPRO.9). Where the classification of work that designs hardware also records the attribute Numerical, NUMER binds it as well.

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

Hardware design is carried out with many languages, schematic and layout editors, and tools, open and proprietary, which change faster than the failures they share. Each provision here therefore states an outcome that holds whatever the language, tool, or process, and is checked from the design record: a record that is present or absent, a check that ran or did not, a verdict, a coverage figure, or a list of what is not verified. The checks themselves, and the representations they read, are left to the work and to LVL2 standards, STND.SV among them. A step that no available check reads is not forbidden; it is named as unverified (HDES.8), and the gap travels with the design.

HDES.4 asks for the contract against which everything else is verified: behavior at the interfaces, timing relations, limits, the shortest asynchronous pulse captured, and the regime of use, supply ramp rates included, stated before verification judges the design (VV.3). Where a realization is part of an execution path under HW, HDES.5 adds what HW.4, HW.5, and HW.13 ask, and marks which properties rest only on analysis or simulation. HW.FPGA.4 and HW.ASIC.4 then have each such property confirmed on devices or stated as unconfirmed in each result that relies on it. The fault kinds include upsets of state by radiation where the regime of use exposes the device to them.

HDES.6 asks that verification run from the design record without a manual step and give a verdict per property, so that each change is re-verified against the evidence it is able to affect (VV.8) by rerunning it, and an agent or an automated check reads the result without judgment. A bounded proof, a timeout, or an aborted run is inconclusive, and leaves its property uncovered rather than passed. A waveform inspected by eye is a diagnostic aid, not a verdict. The reference model is the obvious implementation of the contract (SIMPL.7). From CSQ2 it is produced without the hardware description (VV.1, STND.CLASS.10); at CSQ3 it may be derived from the description, and a comparison only with the design's earlier outputs is a regression guard, labeled as one (VV.7). The same model can serve as the reference path of HW.15 when a realized design is an alternative execution path.

A simulation can pass while the transformed logic differs, through a sensitivity, an initial value, or an unknown value that simulation treats optimistically; HDES.8 closes that gap by repeating the verification on the netlist or by a check of equivalence, and names as unverified each part that the check leaves uncompared and each step after the netlist it reads. An equivalence check reads the description as the transformation does, so it settles a mismatch of simulation only where it interprets the description as the verification did, which is why HDES.9 accepts its evidence only on that condition. Later steps that change the netlist produce netlists too, under the Netlist Term. A transformation can warn of an inferred storage element, a truncation, or a signal with several drivers; HDES.9 has each warning resolved, covered by evidence, or matched by a recorded rule, so that the many routine warnings of a library are dismissed once, by kind and source, and not one by one.

A path that no constraint covers is never analyzed, and a wrong exception hides a failing path, so HDES.10 asks for rules that name their paths and for each exception to be checked against the description; an exception on a crossing between clock domains is checked by the evidence of HDES.11. Paths from port to port are among the paths analyzed. Where the timing models of a target do not cover a condition, the analysis says so rather than claiming it. A signal that crosses between clocks, or an external input sampled without synchronization, fails rarely and irreproducibly. HDES.11 asks for a stated synchronization, or a protocol that holds a quasi-static input stable while it is sampled, and an analysis of the netlist, because a transformation can retime, merge, or pack a synchronizer while equivalence still holds. The output of a comparator or other analog block sampled by a clock is an asynchronous input of this kind. A register whose power-on value nobody set behaves one way in a simulator that zeroes it and another in hardware; HDES.12 verifies from every state, by proof, or from a recorded number of random states.

A transformation can merge triplicated registers or strip a safe encoding while equivalence passes, so HDES.15 verifies each stated mitigation that the design's logic implements on the netlist, by fault injection or proof; mitigation inside a fixed block of the target, a memory's error correction for instance, rests on the target's documentation under HW.6. HDES owns the design record as a shared matter, which HW.FPGA and HW.ASIC address (HW.FPGA.2, HW.ASIC.2). A processor realized in programmable logic is programmable logic under HW, so its firmware is not bound by HW.EMBED (HW.EMBED.1); HW.FPGA leaves its treatment to the project's own instruments (LVL3).

Arithmetic in hardware is usually fixed point. HDES.7 has the record state the delivered arithmetic that HW.5 asks, and verifies at two levels: the description bit for bit against a model of that arithmetic, and that model within a precision that the record derives from the required precision of the results it feeds, by a tolerance fixed before the comparison. The stated arithmetic rounds the real-valued computation, which is numerical error under NUMER.5, and may also approximate it, as a truncated multiplier or a table in place of a function does; each such approximation is a retained performance approximation, listed under NUMER.16 and verified as NUMER.17 asks, at each reported numerical result it affects. Where the outputs of the design are themselves reported numerical results, the comparison of HDES.7 is that verification; where they feed a later computation, NUMER.17 applies at the result that computation reports. A converter between analog values and a number format is verified against its contract under HDES.6, not bit for bit.

Saturation and wrap-around other than the function an operation is specified to compute are silent clamping, which PRIME.4 forbids at every class; HDES.14 makes each occurrence visible, typically by a flag per operation or group that holds until it is read, at the cost of a register. A counter that the specification states as modular, a limiter, and the rail saturation that forms an analog characteristic compute their specified function and fall outside HDES.14; saturation at a limit of a number format falls within it even where the specification states it. For a path executing on the design, a set flag is a reached limit of its hardware under HW.9.

Submitting a design for fabrication releases it, and the decision to release is the human owner's (QA.10, GOV.50); HDES.ASIC gives the owner the record on which to decide (HDES.ASIC.12). Every submission is a remote write whose effect is irrevocable, which an agent performs only under a per-action authorization (PRIME.7, GUARD.11); one that invokes a payment is a reserved action that only the human owner executes (PRIME.6); and one that consumes capacity already paid for proceeds only on an estimate that the human owner authorizes (PRIME.8). Loading a configuration into a device that commands, configures, or powers physical hardware needs the authorization of PRIME.7 and the owner-adopted hazard analysis and verified safe state of PRIME.13, and a load that the hazard analysis marks as hazardous or irreversible is reserved (PRIME.6).

HDES owns one shared matter, the design record of a realized design, and addresses four that other profiles own (HDES.2): the hardware contract of an execution path, through HDES.5, which cites HW.4, HW.5, and HW.6, and HDES.7, which cites HW.5; the boundary contract between execution paths, through HDES.5, which cites HW.13; and the precision a result requires and the tolerance basis of a numerical comparison, through HDES.7, which cites NUMER.5 and NUMER.11.

HDES.14 states how PRIME.4 applies to saturation and overflow, and binds at every class, adding nothing to the floor that PRIME.4 does not already hold. Every other provision except HDES.1 and HDES.2 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES.ASIC | Integrated circuit design |
| HDES.FPGA | Programmable logic design |
| HW | Execution hardware |
| HW.ASIC | Application-specific integrated circuits |
| HW.EMBED | Embedded controllers |
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
| STND.SV | Verilog and SystemVerilog standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Application

#### HDES.1 Hardware design selector

. Instantiates GOV.25, GOV.26.

This profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26).

| Attribute | Defined by |
| --- | --- |
| Programmable logic design | HDES |
| Integrated circuit design | HDES |

#### HDES.2 Hardware design shared matters

. Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Design record of a realized design | HDES | HDES.3, HDES.4, HDES.5, HDES.6, HDES.7, HDES.8, HDES.11, HDES.13 |
| Hardware contract of an execution path | HW | HDES.5, HDES.7 |
| Boundary contract between execution paths | HW | HDES.5 |
| Precision a result requires | NUMER | HDES.7 |
| Tolerance basis of a numerical comparison | NUMER | HDES.7 |

### Design record

#### HDES.3 Design record

From CSQ3. Instantiates REPRO.1, REPRO.2, REPRO.9, REPRO.3.

Each design SHALL keep a design record that identifies its hardware description, its constraints, each external component that it incorporates with its revision and license identity, and each transformation step that produces a realization from it, with the revision, settings, and seeds of the tool that performs each automated step and the stored output of each manual step (REPRO.1, REPRO.2, REPRO.9). Each realization SHALL be regenerable from its design record, identical or with each difference declared (REPRO.1, REPRO.3).

#### HDES.4 Design contract

From CSQ3. Instantiates DSGN.5, VV.3.

Before the verification of HDES.6 judges a design, its design record SHALL state a contract that states the behavior of the design at each of its interfaces, the timing relations of each interface, each limit of its inputs, outputs, and supplies, the shortest pulse and the shortest interval between pulses of each asynchronous input whose pulses it captures, and its regime of use, the ramp rates of its supplies included (DSGN.5, VV.3).

#### HDES.5 Contract of a realization

From CSQ2. Instantiates DSGN.5, INTPR.10.

Where a realization of a design is part of an execution path whose behavior affects a reported result, the design record SHALL state each property, limit, and kind of hardware fault that HW.4 and HW.5 ask the hardware contract of that path to state, and each property of its interfaces that HW.13 asks a boundary contract to state (DSGN.5). Where a realization of a design is part of such an execution path, the design record SHALL mark, for the evidence that HW.6 asks, each property of the contracts of HDES.4 and of this provision whose evidence comes only from analysis or simulation of the design (DSGN.5, INTPR.10).

### Verification

#### HDES.6 Verification of the description

From CSQ3. Instantiates VV.6, VV.1, SIMPL.7, VV.5, INTPR.10, VV.8.

Before a realization of a design is first relied upon or submitted for fabrication, its hardware description SHALL be verified against its contract under HDES.4, by simulation against a reference model or by proof of properties that the contract states, with each property of the contract mapped to the evidence that covers it (VV.6, VV.1, SIMPL.7). The record of that verification SHALL state the coverage that its evidence reaches, by a measure that it names, of the properties of the contract and of the behavior of the description, and each property that it leaves uncovered (VV.5, INTPR.10). That verification SHALL run from the design record without a manual step and report, for each property that it covers, a verdict of pass, fail, or inconclusive, each inconclusive verdict leaving its property uncovered (VV.8).

#### HDES.7 Arithmetic of a design

From CSQ3. Instantiates DSGN.5, REPRO.2, VV.1.

Where a design performs operations on values in a number format that approximate a real-valued computation, its design record SHALL state each property of the delivered arithmetic of those operations that HW.5 asks, their number format, rounding, and overflow behavior among them (DSGN.5, REPRO.2). Where a design performs operations of that kind, its verification SHALL show its outputs identical bit for bit to those of a reference of that stated arithmetic, over inputs whose coverage its record states by a named measure, or by proof (VV.1). Where a design performs operations of that kind, its verification SHALL show the outputs of that reference within a precision that the design record states for them and derives from the required precision under NUMER.5 of each reported numerical result that they feed and from the limits of its contract under HDES.4, against the computation without that arithmetic, over inputs whose coverage of its regime of use its record states by a named measure, or by proof, by a tolerance recorded before the comparison with a basis under NUMER.11 (VV.1).

#### HDES.8 Realization equivalence

From CSQ3. Instantiates VV.6, VV.1, VV.5, INTPR.10.

Before a realization of a design is first relied upon or submitted for fabrication, the netlist closest to that realization that a check available to the work reads SHALL be shown to implement the verified hardware description, by a check of equivalence between the two or by repeating on that netlist the verification of HDES.6 (VV.6, VV.1). The design record SHALL name as unverified, with no claim of correctness resting on it, each part of the design that the check leaves uncompared, each transformation step that follows the netlist so shown and whose output no check that the design record holds compares with that netlist, and every transformation step of a realization of which no netlist is so shown (VV.5, INTPR.10).

#### HDES.9 Transformation warnings

From CSQ3. Instantiates VV.1, INTPR.10.

Before a realization of a design is first relied upon or submitted for fabrication, each warning that a transformation step reported while producing it SHALL be resolved, shown to leave the behavior of the realization unchanged by evidence of HDES.8 that interprets the description as its verification under HDES.6 did, or matched by kind and source by a recorded rule that states why the warnings it matches leave that behavior unchanged (VV.1, INTPR.10).

### Timing and domains

#### HDES.10 Timing closure

From CSQ3. Instantiates DSGN.5, VV.1, INTPR.10.

Each realization of a design SHALL meet the timing of its contract on each path between its state elements and ports, at each operating condition of its regime of use that the timing models of its target cover, shown by an analysis in which each such path is constrained or exempt by a recorded rule that names the paths it covers and its reason (DSGN.5, VV.1). Each exception to a timing constraint of a design SHALL be verified against the behavior of its hardware description, or, for an exception on a path between clock domains, by the analysis of HDES.11 (VV.1). Where the timing models of a target do not cover an operating condition of the regime of use, the record of the analysis SHALL state that condition as not analyzed (INTPR.10).

#### HDES.11 Clock and reset crossings

From CSQ3. Instantiates DSGN.4, DSGN.15, VV.1.

Each signal of a design that crosses between clock domains, each input that a clock domain samples asynchronously, and each release of a reset asynchronous to the clock domain it releases SHALL pass through a synchronization, or follow a protocol that holds it stable while it is sampled, that the design record states (DSGN.4, DSGN.15). An analysis of the netlist that HDES.8 shows for each realization, or of its hardware description for a realization of which HDES.8 shows no netlist, SHALL verify that synchronization, or the gating on which that protocol relies, for each such crossing, input, and release (VV.1, DSGN.15).

#### HDES.12 Defined initial state

From CSQ3. Instantiates DSGN.5, VV.1.

Each state element of a design whose value after power-on or reset a behavior of its contract relies on SHALL have that value set by the design and verified (DSGN.5, VV.1). The verification of that value SHALL start from states in which each other state element is unconstrained, by proof over all its values or by simulation from each of a recorded number of random states (VV.1).

### Budgets

#### HDES.13 Resource and power margins

From CSQ3. Instantiates RSRC.1.

The design record SHALL state, for each realization of a design, its use of each limit of its target, power included, and its margin to each, each figure marked as reported by an analysis of the realization or as estimated (RSRC.1).

### Arithmetic behavior

#### HDES.14 Visible saturation and overflow

. Instantiates PRIME.4.

Where an operation of a design is able, over the inputs that its contract admits, to saturate a value at a limit of its number format, or otherwise to saturate or wrap a value other than as the function that its specification states for that operation, the design SHALL make each occurrence visible at its interface, or in a status that its interface exposes, by operation or by group of operations (PRIME.4).

### Fault behavior

#### HDES.15 Fault mitigation

From CSQ3. Instantiates VV.1, DSGN.5.

Where the contract of a design states a detection or correction of a hardware fault that the logic of the design implements, verification on the netlist that HDES.8 shows for each realization, or on its hardware description for a realization of which HDES.8 shows no netlist, SHALL show that detection or correction for each kind of fault that the contract states (VV.1, DSGN.5).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative text describes HW.FPGA and HW.ASIC as adopted, citing HW.FPGA.2, HW.FPGA.4, HW.ASIC.2, and HW.ASIC.4; no obligation changes. |
| 1.0.2 | 2026-10-25 | Editorial amendment (GOV.41): the informative text cites HDES.FPGA.1 and HDES.ASIC.1, the selectors of its sub-profiles, HW.EMBED.1, the selector of HW.EMBED, and HDES.ASIC.12, the fabrication readiness record on which the human owner decides a submission, and References lists HDES.ASIC, HDES.FPGA, and HW.EMBED; no obligation, permission, or defined meaning changes. |
| 1.0.3 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
| 1.0.4 | 2026-10-28 | Editorial amendment (GOV.41): the Purpose and the Notes name STND.SV among the LVL2 standards that hold the detail of a technology, in place of planned standards, and References lists it; no obligation, permission, or defined meaning changes. |
