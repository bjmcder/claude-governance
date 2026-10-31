# General-purpose processors (HW.CPU) 1.2.1

Adopted by The Custodian as revision 1.0 in ledger entry 68 (2026-10-18); revised to 1.0.1 in entry 163 (2026-10-25), 1.1 in entry 229 (2026-10-28), 1.2 in entry 254 (2026-10-28), and 1.2.1 in entry 305 (2026-10-28). This reading copy is composed from the per-provision files in HW/CPU/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This sub-profile holds the obligations specific to execution paths on general-purpose processors. It inherits HW in full and adds only what this hardware type makes likely to go wrong silently or to cost performance unseen (GOV.27): floating-point control state that loaded code changes for a whole thread or process, and concurrent work that asks for more hardware threads than its affinity and quota allow, runs on the slower cores of a processor with more than one core design, or pages its memory to storage. It names no language, library, tool, instruction set, or platform (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Floating-point control state | The settings of a general-purpose processor, held for a thread or a process, that select the rounding of floating-point operations, the handling of subnormal values, and the response to floating-point exceptions. |
| Hardware thread | A stream of instructions that a general-purpose processor executes concurrently with others, as its maker counts them. |

## Selector

HW.CPU.1 states the selector: the attribute Hardware execution, which HW defines and which HW.1 gives (STND.DRAFT.36), so that the sub-profile binds with HW and its provisions reach a component through the execution paths of that component, recorded by hardware type where the section Architecture of the constitution names (STND.PROJ.1). Each provision names an execution path on a general-purpose processor as its subject (STND.DRAFT.38), so it imposes nothing on the paths of a component on other hardware types.

## Where the rest lives

HW and the documents it relies on already govern these matters for execution paths on this hardware type, and this sub-profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Delivered arithmetic, including choices among implementations made at run time | HW.5 |
| Confirmation of contract properties at the start or resumption of each run | HW.7 |
| Protocols for shared state under the memory and ordering model of each hardware model a path admits | HW.4, HW.6, HW.11 |
| Run-to-run variation with thread count, scheduling, and run-time choices | HW.12 |
| Reference path, alternative paths, and comparison beyond the reference's reach | HW.15, HW.16, HW.17, STND.VVUQ.79 to STND.VVUQ.81 |
| Retained performance approximations, flushing of subnormal values for speed included | NUMER.16, NUMER.17 |
| Budgets, resource records, and measured optimization | RSRC.1, RSRC.2, RSRC.3, RSRC.4 |
| Parallel work on a shared machine | AGENT.39, AGENT.40 |

## Notes

Code loaded into a process, a library built for speed among it, can change the floating-point control state of every thread, flushing subnormal values to zero or changing rounding, so code that never asked for either computes differently and no error is raised. HW.5 states the delivered arithmetic and HW.7 confirms it at the start of a run; HW.CPU.3 confirms it after loading and again before results are reported, which catches code loaded during the run, and keeps a path from leaking its own changes to code outside its contract. Threads that a library creates and runs are reached by a computation in their pool whose result reveals the state, such as a product that is subnormal under the stated arithmetic. Each check costs almost nothing.

A path whose libraries choose among instruction-set extensions at run time states the range of delivered arithmetic over those choices under HW.5, or that it is not established; fixing the choice is one way to establish it. Subnormal arithmetic is slow on some processors, and flushing subnormal values to zero for speed changes the delivered arithmetic (HW.5) and is a performance approximation (NUMER.17).

A protocol for shared state that relies on the ordering of one processor family can fail under the weaker ordering of another while every test on the first passes. HW already requires the hardware contract to state the memory and ordering model of each hardware model a path admits (HW.4), with evidence (HW.6), and the protocol to be verified under it (HW.11); a path that admits processors of differing ordering verifies under each. A protocol built only from the synchronization of its language or library is verified at that level and is unaffected.

Concurrent work that asks for more computing threads than it may use, often by nesting a threaded library inside a pool of processes, runs many times slower without any error. In a container or under a scheduler, the threads it may use are those its affinity and quota allow, not those of the whole machine. Work placed on the slower cores of a processor with more than one core design, or whose memory is paged to storage, also slows without error. HW.CPU.4 records these in the runs that track resource use while a budget is not yet known (RSRC.2) or that measure it for an optimization (RSRC.4), which is to say during development and tuning; a production run whose budget is stated and met omits them, keeping only the record its class asks (RSRC.3). HW.CPU.5 reports oversubscription when it first occurs, in every run, because the report costs one message; it goes to the operator of a run during which one acts, and otherwise into the record of the run. Threads that wait on input and output do not count. A general-purpose processor usually hosts the reference path (HW.15), but nothing here requires it.

HW.CPU addresses one matter that HW owns, the hardware contract of an execution path (HW.CPU.2), through HW.CPU.3, which cites HW.5 and HW.7.

Each provision other than the selector and the shared-matters provision instantiates only VV, REPRO, INTPR, DSGN, or RSRC, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, the confirmation of HW.CPU.3 with the delivered arithmetic of HW.5 that it confirms, HW.CPU.4 adding to the record that RSRC.2 and RSRC.4 ask only in the runs that keep it, and HW.CPU.5 tightening above CSQ1, from which STND.CLASS.10 applies INTPR.7, at the cost of one message. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| REPRO | Reproducibility |
| RSRC | Resources |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.PROJ | Project constitution template |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Application

#### HW.CPU.1 General-purpose processor selector

Instantiates GOV.25, GOV.26, GOV.27.

This sub-profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26, GOV.27).

| Attribute | Defined by |
| --- | --- |
| Hardware execution | HW |

#### HW.CPU.2 General-purpose processor shared matters

Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Hardware contract of an execution path | HW | HW.CPU.3 |

### Arithmetic

#### HW.CPU.3 Floating-point control state

From CSQ2. Instantiates DSGN.5, REPRO.2, VV.8, INTPR.10.

Each execution path on a general-purpose processor whose delivered arithmetic under HW.5 depends on its floating-point control state SHALL confirm that arithmetic after the code it loads at the start of a run and again before its results are reported, by reading that state, or by a computation whose result reveals it, in each thread or pool of threads that performs those operations (DSGN.5, REPRO.2). Where that confirmation fails, the record of each result of the run SHALL state that its delivered arithmetic is unconfirmed, as HW.7 requires of a failed confirmation (VV.8, INTPR.10). Each execution path on a general-purpose processor that changes its floating-point control state SHALL restore that state before control returns to code that its hardware contract does not cover (DSGN.5).

### Resources

#### HW.CPU.4 Processor thread record

From CSQ3. Instantiates RSRC.2, RSRC.4.

Where a run of an execution path on a general-purpose processor that runs concurrent work measures its resource use under RSRC.2 or RSRC.4, the path SHALL record with that resource use each of the following, or that it is unable to measure it without elevated privileges: the number of hardware threads it uses, the number that its processor affinity and processor-time quota let it use at once, counted by core design for a processor with more than one, the volume of its memory paged to storage, and the placement of its threads and memory that it sets (RSRC.2, RSRC.4).

#### HW.CPU.5 Oversubscription report

From CSQ3. Instantiates INTPR.7, RSRC.2.

Where the concurrent work of a run of an execution path on a general-purpose processor requests more threads computing at once than its processor affinity and processor-time quota let it use, the path SHALL report the excess at its first occurrence in the run, to the operator of a run during which one acts and otherwise in the record of the run (INTPR.7, RSRC.2).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Notes name only the Articles that the provisions other than the selector and the shared-matters provision instantiate, so that the Simplicity Article, which none of them instantiates, is no longer named; no obligation, permission, or defined meaning changes. |
| 1.1 | 2026-10-28 | Minor amendment (GOV.41): the selector of HW.CPU.1 gives the attribute Hardware execution of HW.1 in place of its own, so that path scope alone decides which provisions reach a component, each provision naming an execution path on general-purpose processors as its subject (CS9); HW.CPU.5 reports to the operator of a run during which one acts and otherwise in the record of the run (CS8). |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): HW.CPU.3 applies from CSQ2, with the delivered arithmetic of HW.5 that it confirms; each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields. |
| 1.2.1 | 2026-10-28 | Editorial amendment (GOV.41): the Notes say that the provisions reach a component through its execution paths, recorded by hardware type where the section Architecture of the constitution names, in place of the paths that the classification lists, as STND.PROJ.1 now has it; no obligation, permission, or defined meaning changes. |
