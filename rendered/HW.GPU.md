# Accelerators (HW.GPU) 1.0.1

Adopted by The Custodian as revision 1.0 in ledger entry 69 (2026-10-18); revised to 1.0.1 in entry 164 (2026-10-25). This reading copy is composed from the per-provision files in HW/GPU/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This sub-profile holds the obligations specific to execution paths on accelerators. It inherits HW in full and adds only what this hardware type makes likely to go wrong silently or to cost performance unseen (GOV.27): errors in offloaded work that surface after the result has been read, and data movement, on-demand migration, dispatch, and idle time that dominate run time without appearing in it. The mnemonic names the most common accelerator; the sub-profile covers every accelerator in the sense of HW. It names no language, library, tool, vendor, or platform (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Offloaded work | Work that a host processor submits to an accelerator, whose completion the host learns of after the call that submitted it returns. |
| Completion status | The report by which an accelerator or its runtime library tells the host whether offloaded work completed, and with what error. |

## Selector

HW.GPU.1 states the selector: the attribute Accelerator execution, which HW defines and which HW.1 also gives (STND.DRAFT.36). Each provision names an execution path on an accelerator as its subject (STND.DRAFT.38). The calls by which host code submits work to an accelerator and obtains its completion status and results belong to the accelerator's execution path, through its runtime libraries; the rest of the host code is a path on a general-purpose processor, joined to the accelerator's path by a boundary contract (HW.13), and meets HW.CPU (HW.CPU.1), not this sub-profile.

## Where the rest lives

HW and the documents it relies on already govern these matters for execution paths on this hardware type, and this sub-profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Reduced-precision defaults, fused operations, approximate elementary functions, and kernels chosen at run time | HW.5, NUMER.16, NUMER.17 |
| The boundary between host and accelerator: layout, precision, ordering, and ownership | HW.13, HW.14 |
| Run-to-run variation from the order of reductions and from scheduling | HW.12 |
| Exhausted accelerator memory, uncorrected and undetected memory errors | HW.8, HW.10 |
| Fallback to another device or to the host | HW.19 |
| Reference path, alternative paths, and comparison beyond the reference's reach | HW.15, HW.16, HW.17, STND.VVUQ.79 to STND.VVUQ.81 |
| Claims that an accelerator path is faster or more efficient | HW.22 |
| Budgets, resource records, and measured optimization | RSRC.1, RSRC.2, RSRC.3, RSRC.4 |

## Notes

Offloaded work completes after the call that submitted it returns, and an error in it is often reported only at a later synchronization, attributed to whatever call happened to synchronize. A result read before its completion status is obtained can be wrong while no error is raised. HW.GPU.3 obtains the status before a result that depends on the work is reported or relied upon, whether directly or through other paths. Work chained on one or several devices needs no wait between its steps, so the provision costs at most one wait per reported or relied-upon result. An error the status reports, an invalid access or a failed launch as well as a hardware fault, is handled as HW.8 handles a detected fault: halt, visible degradation, or a designed safe state, with an actionable diagnosis. HW.GPU.3 states how PRIME.4 applies to offloaded work and binds at every class, adding nothing to the floor that PRIME.4 does not already hold.

The host and the accelerator are different hardware types, so the host code and the work it offloads are cooperating execution paths joined by a boundary contract (HW.13). A silent narrowing of precision at that boundary, such as a framework default that converts double-precision operands to single precision, is a property of that contract, checked once for each build or compilation in which it is fixed (HW.14).

Many runtime libraries default to reduced-precision inputs or accumulation in matrix units, or to fused and approximate elementary functions. Each is delivered arithmetic under HW.5 and, where retained for speed, a performance approximation verified under NUMER.17. A persisted cache of compiled or autotuned kernels is a setting under HW.3 and HW.7, valid for the hardware model, driver, and runtime libraries under which it was produced.

Data movement, on-demand migration of memory that exceeds the accelerator's capacity, dispatch, and time in which the accelerator waits on the host often dominate the run time of offloaded work. HW.GPU.4 records them in the runs that track resource use while a budget is not yet known (RSRC.2) or that measure it for an optimization (RSRC.4), so that optimization targets the measured bottleneck and claims count them (HW.22). These are development and tuning runs: a production run whose budget is stated and met omits the record and its measurement overhead, keeping only the record its class asks (RSRC.3), and returns to it when a regression or a new optimization calls for it. Where a quantity is measurable only with elevated privileges or with a profiler that the run does not use, the record says so, and nothing more is asked.

Submitting work to a rented accelerator is a remote write, and usually an expenditure, that needs a recorded authorization (PRIME.7, PRIME.8, GUARD.1). Where the provider's service lies within the provisioned environment, a standing authorization with a cost limit (GUARD.11, GUARD.15) spares a referral per job; otherwise each submission transmits data beyond that environment and is authorized per action (GUARD.11). Under STND.HARN.18 and the transition of ledger entry 53, each remote write is referred unless an authorization in force names its destination and kind. Provisioning the rented service as part of the environment is therefore what makes unattended use of it possible.

HW.GPU addresses one matter that HW owns, the hardware contract of an execution path (HW.GPU.2), through HW.GPU.3, which cites HW.8.

HW.GPU.3 instantiates PRIME.4 and binds at every class. Every other provision except the selector and the shared-matters provision instantiates only RSRC, inherits its rank and waivability (GOV.17), and is proportioned to class (GOV.11): under the project's class criteria, such as STND.CLASS.10, it applies from the least severe class at which those criteria require an LVL0 obligation it instantiates, and under STND.CLASS.10 work of CSQ4 omits it. Under STND.CLASS.10, HW.GPU.4 applies from CSQ3, through RSRC.2 and RSRC.4, and only in the runs that track or measure resource use under them. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| RSRC | Resources |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.HARN | Harness specification |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |

## Provisions

### Application

#### HW.GPU.1 Accelerator selector

. Instantiates GOV.25, GOV.26, GOV.27.

This sub-profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26, GOV.27).

| Attribute | Defined by |
| --- | --- |
| Accelerator execution | HW |

#### HW.GPU.2 Accelerator shared matters

. Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Hardware contract of an execution path | HW | HW.GPU.3 |

### Offloaded work

#### HW.GPU.3 Completion of offloaded work

. Instantiates PRIME.4.

Each execution path on an accelerator SHALL obtain the completion status of its offloaded work, and handle each error that status reports as HW.8 requires for a detected fault, before a result that depends on that work, directly or through another execution path, is reported or relied upon (PRIME.4).

### Resources

#### HW.GPU.4 Offload resource record

. Instantiates RSRC.2, RSRC.4.

Where a run of an execution path on an accelerator measures its resource use under RSRC.2 or RSRC.4, the path SHALL record with that resource use each of the following, or that it is unable to measure it without elevated privileges or a profiler that the run does not use: the volume of data moved between the host and the accelerator, that moved on demand by its runtime libraries included, the number of submissions of offloaded work, the fraction of the run's duration in which the accelerator executes that work, and the peak use of accelerator memory (RSRC.2, RSRC.4).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites HW.CPU.1, the selector of the sub-profile that host code outside the accelerator's path meets, and References lists HW.CPU; the Notes name RSRC as the only Article that the provisions other than HW.GPU.3, the selector, and the shared-matters provision instantiate, in place of six Articles of which they instantiate RSRC alone; no obligation, permission, or defined meaning changes. |
