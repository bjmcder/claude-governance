---
id: "CPS"
level: "LVL1"
kind: "profile"
title: "Cyber-physical and actuation"
status: "adopted"
adopted: "2026-10-19"
revision: "1.1"
selector: "Binds when the work commands, configures, or powers physical hardware (CPS.1)."
parent: null
adopted_by: "The Custodian"
---

## Purpose and scope

This profile holds the obligations of work whose systems command, configure, or power physical hardware. PRIME.13 already requires, at every class, a hazard analysis that the human owner adopts, a designed safe state verified before the hardware is first driven, and actuation by an agent, other than commanding the designed safe state, only within an authorized safe range and while a human can stop it. This profile adds what makes those effective, without dictating how: what the hazard analysis covers, a safe state verified against the losses that call for it, command limits that the commanding logic cannot bypass, a staged first operation, a record of commands, control loops whose timing and behavior are stated and verified, and observations checked for plausibility and staleness. Hazard-analysis methods, safety standards, integrity levels, and margins are the project's (LVL3). This document states outcomes only. The methods, thresholds, sample sizes, schedules, and tools that meet them belong to the project's own instruments (LVL3) and to planned LVL2 standards (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Command | An output of a system that sets the state, motion, configuration, or power of physical hardware. |
| Command limit | A limit on a commanded quantity that the hazard analysis of the system states. |
| Closed loop | A system that computes commands from observations of the hardware it commands. |
| Observation | The term that MEAS defines. |
| Physical hardware control | An attribute, true when the classification records that the work commands, configures, or powers physical hardware, or is admitted to. |

## Selector

CPS.1 states the selector: the attribute Physical hardware control, defined here. The domain items are systems that command physical hardware, their commands, and their closed loops, and each provision names one of them, or a record, verification, or observation of one, as its subject (STND.DRAFT.37). An embedded controller that commands, configures, or powers physical hardware (PRIME.13) engages both this profile and HW.EMBED. Observations used only to compute commands are governed here; MEAS binds them as well once a reported result rests on them (MEAS.1).

## Where the rest lives

LVL0 and the documents named here already govern these matters, and this document does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Hazard analysis adopted by the human owner, the designed safe state, the safe range of actuation, and a human-reachable stop | PRIME.13 |
| Authorization to actuate, and reserved actuation | PRIME.6, PRIME.7 |
| Halting, visible degradation, or the safe state on invalid input or fault | PRIME.4, HW.8 |
| Deadlines, worst-case execution time, and budgets of a constrained target | HW.20, HW.21 |
| Outputs of an embedded controller at reset, halt, and stall | HW.EMBED.4 |
| Board check before loading a configuration of programmable logic | HDES.FPGA.3 |
| Incidents | QA.15 |

## Notes

PRIME.13 holds at every class and is not restated here; CPS adds the evidence and content that make it effective, proportioned to class, and cites PRIME.13 without instantiating it, so that the floor stays where LVL0 puts it. CPS.1 has work on a system that commands, configures, or powers physical hardware classified CSQ3 or a more severe class, as GOV.12 lets a profile require of work in its domain: a wrong command is able to damage the hardware it commands, or what that hardware acts on, a loss beyond the author's own time that the consequence test of CSQ3 in STND.CLASS.1 counts, and the minimum keeps CPS.3 to CPS.9 in reach of all such work, the revision of the hazard analysis before an uncovered change first drives the hardware among them. The human owner sets that class (STND.CLASS.1); under CPS.10, an agent that finds a less severe class recorded for such work halts that line of work and refers it, so that the CSQ3 content of this profile is not left out under a class that the profile does not admit, and the referral asks the owner only for the classification that STND.CLASS.1 already asks. A credible path to injury, or to a major and hard-to-reverse loss, still sets CSQ0 or CSQ1 (STND.CLASS.1), and a component that the classification records as isolated from every such system keeps the class recorded for it (GOV.13). CPS.3 says what the hazard analysis covers, each commanded quantity able to cause a hazard with its limits and each failure able to cause one, and has it revised before an uncovered change first drives the hardware; the revision is adopted by the human owner as PRIME.13 requires of the analysis itself. CPS.4 says what the verification of the safe state covers: each loss the hazard analysis identifies, from each operating mode, reaching the safe state or the designed response to that loss, since some safe states need power and some losses call for a response other than the safe state; it rests on the output states of HW.EMBED.4 for an embedded controller and on the board check of HDES.FPGA.3 for programmable logic that the project designed, and otherwise on what the supplier documents or the hardware shows.

CPS.5 places each command limit where the command reaches the hardware, in a check separate from the logic that computes the command, so that a defect in that logic cannot carry a command past its limit. A separate function in the same firmware meets it; whether the check is also separate hardware is for the hazard analysis and the project to decide. A rejected or replaced command is never silent (PRIME.4); a count of replacements reported per interval meets that at loop rate. CPS.6 stages the first operation of control software that is new or changed in a way able to affect its commands, against a model or within the safe range of actuation; it confers no authorization, which PRIME.7 and PRIME.13 govern. CPS.7 records commands, or a stated reduction of them where they are too fast to keep, so that an incident can be reconstructed (QA.15).

CPS.8 has each closed loop state its period or triggering event, its latencies, and the behavior its hazard analysis relies on, its stability or boundedness for instance, and verifies that behavior against a model or on the hardware within limits. CPS.8 adds a stated deadline only where its miss is hazardous; every other deadline of a constrained target remains under HW.20. CPS.9 checks each observation that a loop relies on for range, rate of change, and age, so that a failed or frozen sensor, or a stale reading on a host that is not real-time, leads to the response of PRIME.4 rather than to a wrong command.

CPS owns three shared matters and addresses three that other profiles own (CPS.2): the hardware contract of an execution path, through CPS.4, which cites HW.4 and HW.EMBED.4; the budgets of a constrained target, through CPS.8, which cites HW.20; and the design record of a realized design, through CPS.4, which cites HDES.3 and HDES.FPGA.3.

Every provision other than the selector, the shared-matters provision, and CPS.10, which instantiates PRIME.14 and binds at every class, instantiates only VV, REPRO, DSGN, INTPR, or QA, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because the failure that such content prevents reaches physical hardware at every class, where PRIME.13 and PRIME.4 hold. No provision raises the floor (GOV.11): the minimum class of CPS.1 is the one that GOV.12 lets a profile require, and the floor of GOV.10 holds for such work unchanged.

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| HDES.FPGA | Programmable logic design |
| HW | Execution hardware |
| HW.EMBED | Embedded controllers |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-19 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites MEAS.1, the selector by which MEAS binds observations once a reported result rests on them, and References lists MEAS, whose term Observation the Terms import; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
| 1.1 | 2026-10-31 | Minor amendment (GOV.41): CPS.1 has work on a system that commands, configures, or powers physical hardware classified CSQ3 or a more severe class, as GOV.12 lets a profile require of work in its domain, so that CPS.3 to CPS.9, and with them the revision of the hazard analysis before an uncovered change first drives the hardware, reach all such work, and new CPS.10 has an agent that finds a less severe class recorded for such work halt that line of work and refer it (PRIME.14); the Notes give the reason and the floor argument, the Purpose excepts commanding the designed safe state as PRIME.13 does, and the Selector text names the reach of PRIME.13 for an embedded controller. |
