# Integrated circuit design (HDES.ASIC) 1.0.2

Adopted by The Custodian as revision 1.0 in ledger entry 74 (2026-10-18); revised to 1.0.1 in entry 87 (2026-10-19) and 1.0.2 in entry 169 (2026-10-25). This reading copy is composed from the per-provision files in HDES/ASIC/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This sub-profile holds the obligations specific to designs realized as integrated circuits, digital, analog, or mixed-signal, up to submission for fabrication. It inherits HDES in full and adds only what this realization makes likely to go wrong silently or irreversibly (GOV.27): a layout that breaks a rule or an electrical limit of its process, a layout whose extracted circuit differs from the one verified or whose parasitic elements change an analog block, an analog block that works at nominal conditions and fails at a corner or never starts, a behavioral model that does not match the circuit it stands for, a signal that crosses between power domains without level shifting or isolation, a manufacturing test whose coverage nobody established or whose test structures alter the function, and a decision to fabricate taken on evidence whose gaps nobody stated or for a layout other than the one checked. Fabrication cannot be undone, so every obligation falls before submission and is checked by analysis or simulation of the design. It names no language, tool, vendor, foundry, process, or design kit (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Process design kit | The rules, device models, and libraries of a fabrication process against which an integrated circuit is designed and checked. |
| Sign-off check | A check of a layout that its process design kit or its fabrication service requires before fabrication. |
| Block | A part of a design that its design record names, with its kind recorded as digital, analog, or mixed-signal. |
| Power domain | The elements of a design supplied by one supply, at one voltage, and powered on and off together. |
| Corner | An operating condition that a design record lists, at an extreme of one or more of the variables of an operating condition that the regime of use admits. |
| Behavioral model | A model of an analog or mixed-signal block, simpler than its circuit, that stands for the block in the verification of the design. |
| Manufacturing test | The test applied to each fabricated device to separate devices with manufacturing defects from the rest. |
| Fault model | A stated set of the faults that manufacturing defects produce in a block, against which the coverage of a manufacturing test is measured. |
| Test structure | Logic or circuitry of a design whose purpose is to control or observe its state during manufacturing test. |
| Fabrication readiness record | The part of a design record that states, before submission for fabrication, the layout and kit revision to be submitted, the evidence on that layout and its status, and each gap in that evidence. |

## Selector

HDES.ASIC.1 states the selector: the attribute Integrated circuit design, which HDES defines and which HDES.1 also gives (STND.DRAFT.36). Each provision names a design, its layout, or its blocks, or a record or verification of one, as its subject (STND.DRAFT.37). The application of manufacturing test to fabricated devices, their characterization, and every other validation after fabrication are outside this sub-profile and are governed by HW and its sub-profile HW.ASIC (HW.6, HW.ASIC.4), and by MEAS where it binds (MEAS.1).

## Where the rest lives

LVL0 and the documents named here already govern these matters of hardware design, and this document does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Design record, contract, verification, equivalence, warnings, timing, crossings, initial state, margins, saturation, mitigation | HDES.3 to HDES.15 |
| Statistical criteria for sampling of variation | NUMER.25, STND.VVUQ.33, STND.VVUQ.34, STND.VVUQ.44 |
| Test, characterization, validation, and use of fabricated devices | HW.6, HW.ASIC |
| Release or deployment, submission for fabrication included, on the human owner's decision | QA.10, GOV.50 |
| Reserved actions, explicit monetary transactions included | PRIME.6 |
| Implicit expenditure and remote writes whose effect is irrevocable | PRIME.7, PRIME.8, GUARD.11 |
| Proportion of verification to the consequence class | GOV.11, GOV.12 |

## Notes

Fabrication is irreversible and costs money and months, so every obligation here falls before submission, and each is decided by analysis or simulation of the design and recorded in its fabrication readiness record. Submission releases the design, and the decision to release is the human owner's (QA.10, GOV.50). Every submission is a remote write whose effect is irrevocable, which an agent performs only under a per-action authorization (PRIME.7, GUARD.11); one that invokes a payment is a reserved action that only the human owner executes (PRIME.6); and one that consumes capacity already paid for proceeds only on an estimate that the human owner authorizes (PRIME.8). The referral of that decision halts only the submission (STND.DRAFT.42). HDES.ASIC.12 gives the owner a fabrication readiness record that names by content the very layout to be submitted and the kit revision, so that a rerun after sign-off cannot slip an unchecked layout through; it states for each property, each check, and the test coverage the evidence and whether it was performed and met, and gathers in one list every gap that HDES and this sub-profile record elsewhere. How much verification is enough is proportioned to the consequence class (GOV.11, GOV.12); a shared run for teaching or a hobby may sit at CSQ3, where every provision here still applies, and work at CSQ4 omits them.

The provisions hold for digital, analog, and mixed-signal circuits alike, whatever the process or kit: a provision about analog or mixed-signal blocks is vacuous for a purely digital design, and HDES.11 and HDES.12 are vacuous for a design with no clock or state element. HDES.10 analyzes the realization, which for an integrated circuit is its layout, so the timing of a digital path is analyzed with the parasitic elements of the layout. HDES.ASIC.3 asks that the layout pass each sign-off check that the kit and the fabrication service require, with the kit's revision that the fabrication uses; a check run against a different revision proves nothing about the fabrication. Checks of design rules, of the agreement of layout and netlist, and of electrical rules are the usual kinds, and the rules of a shared run for its frame and pads are checks of this kind too. Where a service runs its checks on its own systems, sending the layout to them is a remote write whose effect is irrevocable (PRIME.7, GUARD.11), and a step that the service treats as submission falls under the rules for submission above. A violation that the service accepts is excepted and recorded with its acceptance; that acceptance is the service's, not a waiver, which only the human owner gives (GOV.44). HDES.ASIC.4 covers the electrical limits that a kit states whether or not a sign-off check enforces them, among them the current density of conductors that sets their lifetime and the voltage that a device withstands.

A block whose layout is drawn by hand has no netlist after its hand-drawn step, and some sign-off checks do not compare a layout with its netlist or schematic. HDES.ASIC.8 asks that each such block's extracted circuit match the one verified, wherever the design record holds its layout, and HDES.ASIC.9 that each analog or mixed-signal block be verified again with the parasitic elements of its layout, which change the frequency of an oscillator or the stability of an amplifier. A signal that leaves a powered-off domain floats, one that drives a powered-off domain can power it through its inputs, and one that crosses between supply voltages without level shifting overstresses or fails to switch its receiver; HDES.ASIC.10 checks each such crossing against the design record by analysis.

An analog block that meets its contract at the nominal condition can fail at a corner, with the mismatch between devices that should be identical, or by never starting: a simulation that begins at an operating point hides a bias circuit that settles at zero current, or an oscillator that sits at an unstable equilibrium. HDES.ASIC.5 asks for verification at each corner and over the mismatch, with sampling carrying the evidence of NUMER.23 and judged with stated probabilities as NUMER.25 asks, usually as a bound on the fraction of samples that meet the contract, with each failed or unconverged run counted as failing, as STND.VVUQ.44 counts runs for order-statistic limits; where a kit does not model a mismatch the contract relies on, the record says that variation is not verified. Corners include end-of-life conditions where the regime of use admits aging or radiation dose. HDES.ASIC.7 asks for start-up from supply ramps at the fastest and slowest admitted rates, with only device noise to break symmetry, since a symmetric oscillator never starts in a noiseless simulation and a reference circuit can fail to start at one ramp rate. HDES.ASIC.6 closes the commonest silent gap in mixed-signal work: a top-level simulation that leaves a connection between analog and digital blocks unexercised, or that uses a behavioral model of an analog block, passes while the circuit itself behaves otherwise.

Manufacturing test is designed and its coverage established before fabrication, though it is applied after. HDES.ASIC.11 asks the record to state, for each block, the fault model and the patterns or procedures of its test, or that it has none; simulation then states the coverage they reach and the faults they leave undetected, and each test structure is shown to leave the function unchanged while inactive. A design with no manufacturing test, common on a shared run for teaching, meets HDES.ASIC.11 by saying so, and its readiness record shows no coverage. For a digital block the fault model is usually of stuck or slow nodes; for an analog block it is usually a set of defects or of parametric deviations, and its procedure a measurement against the contract. The coverage that is enough is set by the contract and the consequence class, not here. A test interface that exposes internal state is an interface of the design, and its reach by outsiders belongs to the contract (DSGN.5). A prototype in programmable logic shows the logic of a design but not the timing, power, analog behavior, or behavior at power-on of the fabricated process; HDES.ASIC.12 marks each property for which a prototype is the only evidence.

HDES.ASIC addresses four matters (HDES.ASIC.2): the design record of a realized design, which HDES owns, through HDES.ASIC.3, HDES.ASIC.5, HDES.ASIC.10, HDES.ASIC.11, and HDES.ASIC.12, which cite HDES.3; and the convergence and the uncertainty of a computed result and the tolerance basis of a numerical comparison, which NUMER owns, through HDES.ASIC.5, which cites NUMER.11, NUMER.23, and NUMER.25, and HDES.ASIC.6, which cites NUMER.11.

Every provision other than the selector and the shared-matters provision instantiates only VV, REPRO, INTPR, or DSGN, so it inherits their rank and waivability (GOV.17) and is proportioned to class (GOV.11): under the project's class criteria, such as STND.CLASS.10, it applies from the least severe class at which those criteria require an LVL0 obligation it instantiates, and under STND.CLASS.10 work of CSQ4 omits it. Under STND.CLASS.10, every provision other than the selector and the shared-matters provision applies from CSQ3. Some provisions apply at CSQ3 content of obligations that STND.CLASS.10 first asks at CSQ2 or CSQ1: a contract for each external component and for hardware (DSGN.5), a schema for each data structure crossing an interface (DSGN.4), documentation of the limits of validity (INTPR.10), provenance written with each output at production (REPRO.4), and verification of each assembly and of the integrated system (VV.6). Each such provision tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. Here an error found after submission also cannot be corrected on that run. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES | Hardware design |
| HW | Execution hardware |
| HW.ASIC | Application-specific integrated circuits |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Application

#### HDES.ASIC.1 Integrated circuit design selector

. Instantiates GOV.25, GOV.26, GOV.27.

This sub-profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26, GOV.27).

| Attribute | Defined by |
| --- | --- |
| Integrated circuit design | HDES |

#### HDES.ASIC.2 Integrated circuit design shared matters

. Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Design record of a realized design | HDES | HDES.ASIC.3, HDES.ASIC.5, HDES.ASIC.10, HDES.ASIC.11, HDES.ASIC.12 |
| Convergence of a computed result | NUMER | HDES.ASIC.5 |
| Uncertainty of a computed result | NUMER | HDES.ASIC.5 |
| Tolerance basis of a numerical comparison | NUMER | HDES.ASIC.5, HDES.ASIC.6 |

### Process rules

#### HDES.ASIC.3 Sign-off checks

. Instantiates VV.1, DSGN.5, VV.5, INTPR.10.

Before a design is submitted for fabrication, its layout SHALL show no violation, other than one that its fabrication service accepts, of each sign-off check that its process design kit and its fabrication service require, run with the revision of the kit that the fabrication uses (VV.1, DSGN.5). Where the fabrication service accepts a violation of such a check, the fabrication readiness record in the design record under HDES.3 SHALL state the violation and the record of its acceptance (VV.5, INTPR.10).

#### HDES.ASIC.4 Electrical limits of the process

. Instantiates VV.1, DSGN.5.

Before a design is submitted for fabrication, an analysis of its layout SHALL show each device and each conductor within each limit of voltage, current, and current density that its process design kit states for it, at the operating conditions of its regime of use (VV.1, DSGN.5).

### Analog and mixed-signal

#### HDES.ASIC.5 Variation across corners

. Instantiates VV.1, DSGN.5, VV.5, INTPR.10.

Each analog or mixed-signal block of a design whose circuit the design record holds SHALL be verified at each corner of its regime of use, the process extremes that its process design kit models and each end-of-life condition that its regime of use admits included, and over the variation between matched devices on which its contract relies and that its process design kit models, within tolerances that its contract states before the verification with a basis under NUMER.11 (VV.1, DSGN.5). Where that verification estimates the variation by sampling, its samples SHALL carry the evidence of NUMER.23 and its acceptance be judged by a criterion that states its probabilities as NUMER.25 asks (VV.1). Where its process design kit does not model a variation between matched devices on which its contract relies, the fabrication readiness record in the design record under HDES.3 SHALL state that variation as not verified, with no claim of correctness resting on it (VV.5, INTPR.10).

#### HDES.ASIC.6 Mixed-signal verification models

. Instantiates VV.6, VV.1.

Where a design joins analog and digital blocks, its verification under HDES.6 SHALL exercise each connection between an analog and a digital block, with each analog block represented by its circuit or by a behavioral model (VV.6, VV.1). Each behavioral model that the verification of a design uses for a block whose circuit the design record holds SHALL be verified against the circuit-level simulation of that block at each corner of HDES.ASIC.5, within tolerances with a basis under NUMER.11 that the record of the model states before the comparison (VV.1, VV.6).

#### HDES.ASIC.7 Analog start-up from power-on

. Instantiates VV.1, DSGN.5.

Each analog or mixed-signal block of a design whose circuit the design record holds and whose contract relies on a state that it reaches after power-on SHALL be verified to reach that state from a ramp of its supply at the fastest and slowest rates that its regime of use admits, from zero charge on each node, with no excitation other than that ramp, the noise of its devices or sources that represent that noise, and the inputs that its contract states for start-up, at each corner of HDES.ASIC.5 (VV.1, DSGN.5).

### Layout verification

#### HDES.ASIC.8 Extracted layout match

. Instantiates VV.1, VV.6.

Before a design is submitted for fabrication, the circuit extracted from the layout of each block whose layout the design record holds and that no check of HDES.ASIC.3 compares with its netlist or schematic SHALL be shown to match the netlist or schematic that its verification used (VV.1, VV.6).

#### HDES.ASIC.9 Verification with parasitic elements

. Instantiates VV.1.

Before a design is submitted for fabrication, each analog or mixed-signal block whose layout the design record holds SHALL be verified, within the tolerances of HDES.ASIC.5 at each of its corners, on the circuit extracted from its layout with its parasitic elements (VV.1).

#### HDES.ASIC.10 Power domain crossings

. Instantiates DSGN.4, VV.1.

Each signal of a design that crosses between power domains at different voltages, or between a power domain able to be powered off and another power domain, SHALL pass through the level shifting or isolation that its design record under HDES.3 states (DSGN.4). Before a design is submitted for fabrication, an analysis of the netlist that HDES.8 shows, or of the circuit extracted from its layout, SHALL verify that level shifting or isolation for each such signal (VV.1).

### Testability

#### HDES.ASIC.11 Manufacturing test coverage

. Instantiates VV.1, VV.6, VV.5, INTPR.10.

The design record under HDES.3 of each design SHALL state, for each block, the fault model against which its manufacturing test is measured and the test patterns or procedures that the test applies, or that the block has no manufacturing test (VV.1, VV.6). Before a design is submitted for fabrication, simulation of those patterns or procedures on the netlist that HDES.8 shows, or on the circuit extracted from its layout, SHALL show the coverage that they reach of each fault model and, by block, the faults that they leave undetected (VV.5, INTPR.10). Before a design is submitted for fabrication, each test structure of the design SHALL be shown, on the netlist that HDES.8 shows or on the circuit extracted from its layout, to leave the behavior of its contract unchanged while the structure is inactive (VV.1).

### Submission

#### HDES.ASIC.12 Fabrication readiness record

. Instantiates VV.5, REPRO.4, REPRO.1, INTPR.10, VV.1.

Before a design is submitted for fabrication, its design record under HDES.3 SHALL hold a fabrication readiness record that identifies by content the layout to be submitted and the revision of its process design kit, and states, for each property of its contract, each check of HDES.ASIC.3, each analysis of HDES.ASIC.4, and the coverage of HDES.ASIC.11, the evidence that applies to that layout, with the checks of HDES.8, HDES.ASIC.3, and HDES.ASIC.8 that carry to that layout the evidence obtained on the hardware description or a netlist, and whether each was performed and met (VV.5, REPRO.4, REPRO.1). The fabrication readiness record SHALL list each property that HDES.6 leaves uncovered, each part and step that HDES.8 names as unverified, each rule of HDES.9, each condition that HDES.10 states as not analyzed, and each variation that HDES.ASIC.5 states as not verified, each block whose evidence rests only on the contract of an external component (VV.5, INTPR.10). Where evidence for a design comes from a realization in programmable logic, the fabrication readiness record SHALL mark each property for which that realization is the only evidence (VV.1, INTPR.10).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative Selector text describes HW.ASIC and MEAS as adopted; no obligation changes. |
| 1.0.2 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites HW.6 and HW.ASIC.4, which govern the evidence obtained from fabricated devices, and MEAS.1, the selector of MEAS, and References lists HW.ASIC and MEAS; no obligation, permission, or defined meaning changes. |
