---
id: "HW.EMBED"
level: "LVL1"
kind: "sub-profile"
title: "Embedded controllers"
status: "adopted"
adopted: "2026-10-18"
revision: "1.0.1"
selector: "Binds when a component of the work executes, or is admitted to execute, on an embedded controller (HW.EMBED.1)."
parent: "HW"
adopted_by: "The Custodian"
---

## Purpose and scope

This sub-profile holds the obligations specific to execution paths on embedded controllers. It inherits HW in full and adds only what this hardware type makes likely to go wrong silently (GOV.27): memory that overflows into other memory without an error, outputs whose state before and between the firmware's control is the hardware's rather than the firmware's, an image on the target that is not the one verified, and resets and stalls that leave gaps in data. It names no language, library, tool, vendor, device, or platform (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Image | The firmware, with its configuration data and each non-volatile setting of the embedded controller outside the firmware on which its behavior depends, as written to the controller. |
| Stall | An interval, while an embedded controller is powered, in which its firmware fails to make the progress that its design requires. |

## Selector

HW.EMBED.1 states the selector: the attribute Embedded controller execution, which HW defines and which HW.1 also gives (STND.DRAFT.36). Each provision names an execution path on an embedded controller as its subject (STND.DRAFT.38). The host that receives a controller's data is a path on another hardware type, joined to the controller's path by a boundary contract (HW.13). The checks by which the host confirms the controller's image and contract properties, and detects its resets and stalls, belong to the controller's execution path.

## Where the rest lives

HW and the documents it relies on already govern these matters for execution paths on this hardware type, and this sub-profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Deadlines, worst-case execution time or detection of missed deadlines, budgets, and their monitoring | HW.20, HW.21 |
| Interrupt handlers and the code they interrupt, as concurrent access to shared state | HW.11 |
| Kinds of hardware fault, a loss of power included, and exhausted capacities, the endurance of writable memory included | HW.4, HW.8 |
| Compiler options that set delivered arithmetic | HW.5 |
| The link to a host: layout, byte order, precision, timing | HW.13, HW.14 |
| Hazard analysis, the designed safe state, and actuation of physical hardware | PRIME.13 |

## Notes

On most embedded controllers a stack that overflows, or a heap that grows into it, writes over other memory with no error, and the firmware goes on computing with corrupted state. HW.EMBED.3 asks for a bound that includes interrupt handlers at their deepest nesting, by analysis of the build or by a test that forces that nesting at the point of greatest stack use of the interrupted code, or for detection before other memory changes, by a guard region that the hardware enforces or a check that runs first. A high-water mark measured in testing is not a bound, because the deepest nesting of interrupts is rare in tests. For a constrained target the margin is that of HW.20, whose on-target evidence and monitoring still apply.

From power-on until the firmware configures it, during each reset, and while the firmware is stalled, an output takes the state that the hardware or the last write gives it, not the state the firmware would choose; a heater left on by a stalled loop is the common case. Where the output commands, configures, or powers physical hardware, those intervals are part of what PRIME.13 asks to be safe. HW.EMBED.4 states each state with evidence, from the target or from the controller's documented specification and the circuit's design record, so that no instrument or human is needed where the documents settle it. PRIME.13 governs the safe state itself at every class; CPS owns the coverage of the hazard analysis and the verification of the safe state, and CPS.4 rests that verification on the output states that this provision states.

A build that differs from the one verified, from a stale file, a wrong target, or a changed non-volatile setting such as a clock divider, runs without error. HW.EMBED.5 has the target report the identity of its image, those settings included, typically at start, and compares it with the identity that the verification cites; the cost is one message. Writing an image to a controller that commands, configures, or powers physical hardware configures that hardware, and needs the authorization that PRIME.7 and PRIME.13 require.

A watchdog that resets a stalled controller keeps it running and hides that data were lost. HW.EMBED.6 detects each reset and stall and states the gaps they leave in each result, as HW.9 does for hardware events; a cause of reset that the hardware reports, or a counter of starts, usually suffices.

A clock whose accuracy and drift a result depends on is a property of the hardware contract (HW.4). The endurance of writable memory is a capacity in the sense of HW, so a design that writes it repeatedly states that limit under HW.4 and responds to its exhaustion under HW.8. Each response to a detected fault that the contract states is verified as other behavior is (VV.1), by injecting the fault where the target cannot produce it on demand.

Each provision has a route that costs the target at most one reported identity at run time, or a periodic sign of life where the data carry none and the budgets allow it, and none turns a design that meets its budgets into one that does not: a bound by analysis of the build, or a test that forces the deepest nesting, in place of run-time detection (HW.EMBED.3); documentation and the circuit's design record as evidence of output states (HW.EMBED.4); an identity read from the target's memory, or the read-back record of the write that programmed it where the memory is protected against reading, in place of one the firmware reports (HW.EMBED.5); and detection of resets and stalls by the host, from sequence numbers or timestamps the data already carry, or a statement that they go undetected where detection would exceed a budget (HW.EMBED.6). Evidence gathered on an instrumented build supports the image deployed where the record shows the instrumentation leaves the verified behavior unchanged; otherwise HW.EMBED.5 asks that the deployed image itself be the one verified, which is what keeps an instrumented test build from standing in for a different release. The checks of HW that run during a run have similar routes. HW.7 is met by the host comparing an identity of the controller, or, where none is available without code on the target, by marking the results unconfirmed, which costs the target nothing. HW.14 moves to verification each check whose cost on each crossing exceeds the budget that the boundary contract states, and HW.20 and HW.21 accept a bound established before first reliance in place of run-time detection and monitoring.

HW.EMBED addresses two matters that HW owns (HW.EMBED.2): the hardware contract of an execution path, through HW.EMBED.3, which cites HW.8, HW.EMBED.4, which cites HW.4 and HW.8, and HW.EMBED.6, which cites HW.9; and the budgets of a constrained target, through HW.EMBED.3 and HW.EMBED.6, which cite HW.20.

Each provision other than the selector and the shared-matters provision instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC. Each such provision inherits their rank and waivability (GOV.17) and is proportioned to class (GOV.11): under the project's class criteria, such as STND.CLASS.10, it applies from the least severe class at which those criteria require an LVL0 obligation it instantiates, and under STND.CLASS.10 work of CSQ4 omits it. Under STND.CLASS.10, HW.EMBED.3 to HW.EMBED.6 apply from CSQ3; HW.EMBED.6 instantiates INTPR.10, which STND.CLASS.10 applies from CSQ2, and so tightens above the floor at the cost of one statement in a record. HW.EMBED.4 applies from CSQ3 although HW.4 applies from CSQ2, and so tightens above the floor (PRIME.15) for outputs that drive physical hardware. At every class, PRIME.13 holds for outputs that drive physical hardware. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| RSRC | Resources |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative Notes describe CPS as adopted, citing CPS.4; no obligation changes. |
