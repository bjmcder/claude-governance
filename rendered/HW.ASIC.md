# Application-specific integrated circuits (HW.ASIC) 1.2.1

Adopted by The Custodian as revision 1.0 in ledger entry 80 (2026-10-19); revised to 1.1 in entry 234 (2026-10-28), 1.2 in entry 253 (2026-10-28), and 1.2.1 in entry 304 (2026-10-28). This reading copy is composed from the per-provision files in HW/ASIC/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This sub-profile holds the obligations specific to execution paths on integrated circuits, which HW defines as devices fabricated from a design whose record the project holds. It inherits HW in full and adds only what this hardware type makes likely to go wrong silently (GOV.27): a result that cannot be traced to the device and design revision it was computed on, and a result that relies on a property that only analysis or simulation before fabrication supports, or that was measured on too few devices to show how it varies among them. Fabricated devices vary widely with process, design, and use, so the sub-profile states two outcomes and nothing more. The design up to submission is governed by HDES and HDES.ASIC. This document states outcomes only. The methods, thresholds, sample sizes, schedules, and tools that meet them belong to the project's own instruments (LVL3) and to planned LVL2 standards (GOV.18). It names no language, tool, vendor, foundry, process, or design kit.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Integrated circuit | The term that HW defines. |

## Selector

HW.ASIC.1 states the selector: the attribute Hardware execution, which HW defines and which HW.1 gives (STND.DRAFT.36), so that the sub-profile binds with HW and its provisions reach a component through the execution paths of that component, recorded by hardware type where the section Architecture of the constitution names (STND.PROJ.1). Each provision names an execution path on an integrated circuit, or the record of a result it computes, or evidence about one, as its subject (STND.DRAFT.38). A device fabricated from a design that the project does not hold is not an integrated circuit under HW, and no provision of this sub-profile reaches it.

## Where the rest lives

HW and the documents it relies on already govern these matters for execution paths on this hardware type, and this sub-profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Design record, contract, verification, manufacturing test coverage, and fabrication readiness record | HDES.3 to HDES.15, HDES.ASIC.3 to HDES.ASIC.12 |
| Execution path record, hardware contract, evidence, and confirmation at each run | HW.3 to HW.7 |
| Kinds of hardware fault and the response to each | HW.4, HW.8, HW.10 |
| Observations, calibration, and measurement uncertainty of a characterization | MEAS.3 to MEAS.7 |
| Commanding, configuring, or powering physical hardware | PRIME.7, PRIME.13, CPS.3 to CPS.9 |

## Notes

HW.ASIC.3 makes each result name the device it was computed on: the design revision of the part the project designed, which on a die shared among several projects is its own part, traced to its design record, whose fabrication readiness record under HDES.ASIC.12 holds the evidence before fabrication where the project's class asked for one, and the individual identity of the device where it carries one or its fabricator gives one. HW.ASIC.4 takes up what HDES leaves open: for each part of the regime of use on which a result relies, a property marked as resting only on analysis or simulation before fabrication is either measured on fabricated devices or stated as resting on analysis alone there; measured evidence states the number and identity of the devices it rests on and how the property spread among them, apart from the uncertainty of each measurement. Nothing is blocked; a single prototype measured once is admissible evidence that says what it is.

Characterization of fabricated devices is measurement: where MEAS binds the work, its observations, calibration, and uncertainty follow MEAS. The application of manufacturing test, screening, burn-in, sample sizes, and acceptance limits are project matters (LVL3).

HW.ASIC addresses two matters (HW.ASIC.2): the hardware contract of an execution path, which HW owns, through HW.ASIC.4, which cites HW.6; and the design record of a realized design, which HDES owns, through HW.ASIC.3, which cites HDES.3, and HW.ASIC.4, which cites HDES.5.

Every provision other than the selector and the shared-matters provision instantiates only VV, REPRO, or INTPR, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| GOV | Governance |
| HDES | Hardware design |
| HDES.ASIC | Integrated circuit design |
| HW | Execution hardware |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.PROJ | Project constitution template |
| VV | Correctness |

## Provisions

### Application

#### HW.ASIC.1 Integrated circuit execution selector

. Instantiates GOV.25, GOV.26, GOV.27.

This sub-profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26, GOV.27).

| Attribute | Defined by |
| --- | --- |
| Hardware execution | HW |

#### HW.ASIC.2 Integrated circuit execution shared matters

. Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Hardware contract of an execution path | HW | HW.ASIC.4 |
| Design record of a realized design | HDES | HW.ASIC.3, HW.ASIC.4 |

### Identity

#### HW.ASIC.3 Device in each result

From CSQ3. Instantiates REPRO.1, REPRO.2.

The record of each result that an execution path on an integrated circuit computes SHALL identify the design revision of the part of the device that the project designed, traced to its design record under HDES.3 (REPRO.1, REPRO.2). Where the device carries an individual identity, or its fabricator gives it one, that record SHALL also identify the device by it (REPRO.1).

### Evidence

#### HW.ASIC.4 Fabricated-device evidence

From CSQ2. Instantiates VV.1, INTPR.10.

Where a reported result relies on a property of the hardware contract of an execution path on an integrated circuit that its design record marks under HDES.5 as resting only on analysis or simulation, the path SHALL hold, for each part of the regime of use on which that result relies, evidence under HW.6 obtained by measurement of fabricated devices of that design revision, or a statement in the record of that result that the property rests on analysis or simulation alone in that part (VV.1, INTPR.10). Evidence obtained by measurement of fabricated devices SHALL state the number and identity of the devices measured and the spread of the property among them, or that one device was measured, kept apart from the uncertainty of each measurement (VV.1, INTPR.10).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-19 | Adopted. |
| 1.1 | 2026-10-28 | Minor amendment (GOV.41): the selector of HW.ASIC.1 gives the attribute Hardware execution of HW.1 in place of its own, so that path scope alone decides which provisions reach a component, each provision naming an execution path on integrated circuits as its subject (CS9). |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): HW.ASIC.4 applies from CSQ2, the class from which its trigger, a property that the design record marks under HDES.5, exists; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
| 1.2.1 | 2026-10-28 | Editorial amendment (GOV.41): the Notes say that the provisions reach a component through its execution paths, recorded by hardware type where the section Architecture of the constitution names, in place of the paths that the classification lists, as STND.PROJ.1 now has it; no obligation, permission, or defined meaning changes. |
