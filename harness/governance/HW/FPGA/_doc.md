---
id: "HW.FPGA"
level: "LVL1"
kind: "sub-profile"
title: "Field-programmable gate arrays"
status: "adopted"
adopted: "2026-10-19"
revision: "1.2.1"
selector: "Binds with HW, when a component of the work executes, or is admitted to execute, on a hardware type (HW.FPGA.1); its provisions name execution paths on programmable logic."
parent: "HW"
adopted_by: "The Custodian"
---

## Purpose and scope

This sub-profile holds the obligations specific to execution paths on programmable logic. It inherits HW in full and adds only what this hardware type makes likely to go wrong silently (GOV.27): a result that cannot be traced to the configuration it was computed on, above all across a reconfiguration during a run, and a result that relies on a property of the configured design that only analysis or simulation supports. The design of a configuration that the project produces is governed by HDES and HDES.FPGA. This document states outcomes only. The methods, thresholds, sample sizes, schedules, and tools that meet them belong to the project's own instruments (LVL3) and to planned LVL2 standards (GOV.18). It names no language, tool, vendor, or device family.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Configuration | The term that HDES.FPGA defines. |
| Target model | The term that HDES.FPGA defines. |

## Selector

HW.FPGA.1 states the selector: the attribute Hardware execution, which HW defines and which HW.1 gives (STND.DRAFT.36), so that the sub-profile binds with HW and its provisions reach a component through the execution paths of that component, recorded by hardware type where the section Architecture of the constitution names (STND.PROJ.1). Each provision names an execution path on programmable logic, or the record of a result it computes, as its subject (STND.DRAFT.38). A configuration that the project did not produce, a supplier's shell or a purchased block for instance, is identified as its supplier gives it.

## Where the rest lives

HW and the documents it relies on already govern these matters for execution paths on this hardware type, and this sub-profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Design record, contract, verification, equivalence, and configuration identity of a configured design | HDES.3 to HDES.15, HDES.FPGA.3 to HDES.FPGA.5 |
| Execution path record, hardware contract, evidence, and confirmation at each run | HW.3 to HW.7 |
| Kinds of hardware fault, upsets of configuration memory included, and the response to each | HW.4, HW.8, HW.10 |
| Board check before a configuration is first loaded | HDES.FPGA.3 |
| Commanding, configuring, or powering physical hardware | PRIME.7, PRIME.13, CPS.3 to CPS.9 |

## Notes

Programmable logic is the easier of the two realized hardware types to verify, because a configuration can be loaded, observed, and replaced at will. HW.FPGA therefore adds only two things to HW. HW.FPGA.3 makes each result name the configuration it was computed on, including after a reconfiguration during a run, which HW.3 alone does not single out; for a configuration that the project produced, the identity is the one that HDES.FPGA.4 makes it carry. HW.FPGA.4 takes up what HDES leaves open: for each part of the regime of use on which a result relies, a property that the design record marks as resting only on analysis or simulation is either supported by evidence from a device of the target model or stated as resting on analysis alone there. Nothing is blocked: the statement is always available, and how much confirmation the work buys is the project's choice under its class (GOV.11).

Analysis against the target maker's timing and power models rests on those models, and HDES.5 marks the properties that rest on it. Which properties a project confirms on a device, by what test, at which conditions, and with what margin are project matters (LVL3). Upsets of configuration memory are hardware faults of HW.4, with the response of HW.8 and the exposure of HW.10 where they go undetected; mitigation in the design is verified under HDES.15.

A processor realized in programmable logic is programmable logic under HW, so no provision of HW.EMBED reaches its firmware (HW.EMBED.1). Whether the project follows HW.EMBED for that firmware as guidance is a choice for its own instruments (LVL3).

HW.FPGA addresses two matters (HW.FPGA.2): the hardware contract of an execution path, which HW owns, through HW.FPGA.4, which cites HW.6; and the design record of a realized design, which HDES owns, through HW.FPGA.3, which cites HDES.3 and HDES.FPGA.4, and HW.FPGA.4, which cites HDES.5.

Every provision other than the selector and the shared-matters provision instantiates only VV, REPRO, or INTPR, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| GOV | Governance |
| HDES | Hardware design |
| HDES.FPGA | Programmable logic design |
| HW | Execution hardware |
| HW.EMBED | Embedded controllers |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.PROJ | Project constitution template |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-19 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Notes cite HW.EMBED.1, the selector of HW.EMBED, where they state that HW.EMBED does not bind the firmware of a processor realized in programmable logic, and References lists HW.EMBED; no obligation, permission, or defined meaning changes. |
| 1.1 | 2026-10-28 | Minor amendment (GOV.41): the selector of HW.FPGA.1 gives the attribute Hardware execution of HW.1 in place of its own, so that path scope alone decides which provisions reach a component, each provision naming an execution path on programmable logic as its subject (CS9). |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): HW.FPGA.4 applies from CSQ2, the class from which its trigger, a property that the design record marks under HDES.5, exists; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
| 1.2.1 | 2026-10-28 | Editorial amendment (GOV.41): the Notes say that the provisions reach a component through its execution paths, recorded by hardware type where the section Architecture of the constitution names, in place of the paths that the classification lists, as STND.PROJ.1 now has it; no obligation, permission, or defined meaning changes. |
