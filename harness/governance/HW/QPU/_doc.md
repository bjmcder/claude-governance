---
id: "HW.QPU"
level: "LVL1"
kind: "sub-profile"
title: "Quantum processors"
status: "adopted"
adopted: "2026-10-18"
revision: "1.0.2"
selector: "Binds when a component of the work executes, or is admitted to execute, on a quantum processor (HW.QPU.1)."
parent: "HW"
adopted_by: "The Custodian"
---

## Purpose and scope

This sub-profile holds the obligations specific to execution paths on quantum processors. It inherits HW in full and adds only what this hardware type makes likely to go wrong silently (GOV.27). Its aim is the greatest provenance and reproducibility that the device allows, not a precision that device noise forbids: each result records what was executed and under which calibration and defaults; device noise that biases an estimate is stated beside the sampling noise; error mitigation states its assumptions and whether they are established; samples pooled across calibrations carry their variation; compilation is checked where checking is affordable; and a result whose required precision the device cannot reach within budget is reported with the precision achieved, without further spending on refinement that cannot close the gap. Every provision has an exit that the device and its provider leave open: not assessed, not established, not disclosed, unchecked, or variation carried in the uncertainty. It names no language, library, tool, vendor, device, or qubit technology (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Executed circuit | The circuit, or the sequence of controlled interactions, as the quantum processor executes it, after compilation, assignment to physical qubits, and scheduling. |
| Calibration record | The record, given by a quantum processor or its provider, of the measured properties of the device in force when a job runs. |
| Error mitigation | A method that reduces the effect of device noise on an estimate by processing measured outcomes or by modifying and repeating executions, without encoding the computation in an error-correcting code. |
| Shot | One execution and measurement of an executed circuit. |

## Selector

HW.QPU.1 states the selector: the attribute Quantum processor execution, which HW defines and which HW.1 also gives (STND.DRAFT.36). Each provision names an execution path on a quantum processor as its subject (STND.DRAFT.38). The calls by which host code submits work to a quantum processor and retrieves its outcomes, and the processing of those outcomes by error mitigation, belong to the quantum processor's execution path, through its runtime libraries. An ideal or noisy simulation of a quantum computation is an execution path on the general-purpose processor or accelerator that runs it, and meets HW.CPU or HW.GPU (HW.CPU.1, HW.GPU.1), not this sub-profile.

## Where the rest lives

HW and the documents it relies on already govern these matters for execution paths on this hardware type, and this sub-profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Which kind of path produced each result: hardware execution, or ideal or noisy simulation, with its noise model | HW.3, INTPR.9 |
| The native operations, error rates, and noise model of the device, in the hardware contract | HW.4, HW.6 |
| Confirmation of contract properties by the calibration record of each job | HW.7 |
| Reference path, usually a classical simulation, and comparison beyond its reach | HW.15, HW.16, HW.17, STND.VVUQ.79 to STND.VVUQ.81 |
| Results that lack the evidence VV requires | PRIME.3 |
| Uncertainty by source, sampling reliability, and statistical acceptance criteria | NUMER.13, NUMER.23, NUMER.25 |
| Statistical methods for stochastic results | STND.VVUQ.33, STND.VVUQ.57 to STND.VVUQ.65 |

## Notes

One source circuit gives different results after different compilation, qubit assignment, and calibration, a compiler's randomized choices differ between runs unless seeded, and providers apply error mitigation and suppression by default. HW.QPU.3 records what was executed and under which settings, so that a result can be regenerated or its difference explained (REPRO.1, REPRO.2). Where a provider withholds any of these, the record names what is withheld, as HW.3 does for items unreadable without elevated privileges.

Device noise left after error mitigation biases an estimate. NUMER.13 has no component for it: numerical error in the sense of NUMER covers discretization, stopping, and rounding, and statistical uncertainty covers sampling. HW.QPU.4 states the bias as a component of its own, marked estimated, bounded, or not assessed as NUMER.13 marks a component, so that a small sampling error does not hide a large bias. Shot noise, as error mitigation enlarges it, is the statistical uncertainty of NUMER.13.

Error mitigation rests on assumptions about the device's noise that hold for some calibrations and not others, and some cannot be checked at all. HW.QPU.5 asks for the method, its assumptions, and for each assumption either evidence that it holds or a statement that it is not established; an estimate of the bias that rests on an unestablished assumption is no estimate, so the bias is then estimated or bounded by other evidence, such as known-answer instances, or marked not assessed under HW.QPU.4.

Calibrations change within hours. Samples from jobs under calibrations that differ in the qubits or operations a circuit uses come from different distributions, and a pooled estimate describes neither unless the estimates from each agree within the precision the result requires. HW.QPU.6 asks for that evidence under NUMER.23, judged by a criterion with the error rates of NUMER.25, before samples are combined, or for the variation among the per-calibration estimates to be carried in the pooled result's statistical uncertainty; otherwise each calibration's samples give a separate result. A change in qubits the circuit does not use does not engage it.

Device noise hides miscompilation: a wrong qubit assignment or a faulty compiler pass changes the distribution by less than the noise does, and a comparison with the reference path under a statistical tolerance passes. HW.QPU.7 compares the executed circuits with the source circuit without noise wherever classical simulation is affordable, under the initial and final qubit assignments that routing produces and after the classical correction that measurement randomization needs. Circuits that differ only in parameter values or in randomized mitigation are simulated once, so the check costs little for the circuit sizes at which it applies. The check runs on a classical computer, not on the device, so device noise does not make it unsatisfiable; where the provider does not disclose the executed circuits, or the circuits are too large to simulate, the record says the check was not made, and nothing more is asked. A compiler that approximates by design, by a provider default included, lists that approximation under NUMER.16 with its estimated or bounded effect, and the check allows that effect; an approximation whose effect is not assessed leaves the equivalence unchecked. A simulation that runs and finds a difference beyond those allowances is a failed verification, not an unchecked one.

The reference path of a quantum computation is usually a classical simulation, which becomes infeasible as the problem grows. HW.17 governs the comparison beyond its reach, with STND.VVUQ.80 and STND.VVUQ.81 as its default extrapolation criterion for stochastic results, fitted against the extrapolation abscissa, which is the count of operations where the contract states an error rate per operation. Checks that need no simulation, such as known-answer instances, symmetries, and conservation laws, serve as the full-size checks of HW.17. Where no criterion is met, the result lacks the evidence VV requires and is labeled unverified (PRIME.3). Fixed-seed tests (STND.VVUQ.64) apply to the compiler and to simulation paths; shots on a device are not reproducible by seed.

HW.5 governs the classical numerical operations of a path on a quantum processor. For its quantum operations, the hardware contract states the native operations, their error rates, and the noise model on which the component relies (HW.4), and that noise is not a hardware fault (HW). The calibration record of each job serves as a record of those properties that the hardware gives for the run (HW.7).

Submitting a job to a remote quantum processor is a remote write, and usually an expenditure, that needs a recorded authorization (PRIME.7, PRIME.8, GUARD.1); an access credential is used only as the provisioned environment allows and is never written where it persists (AGENT.45). Where the provider's service lies within the provisioned environment, a standing authorization with a cost limit (GUARD.11, GUARD.15) spares a referral per job; otherwise each submission transmits data beyond that environment and is authorized per action (GUARD.11). A submission that no authorization in force covers is one that PRIME.7 and PRIME.14 have the agent halt and refer.

Device noise often sets a floor below which more shots, mitigation, or recompilation do not lower the uncertainty of an estimate. HW.QPU.8 has such a result reported with the uncertainty it achieved and the shortfall from its required precision, and stops spending on more shots, mitigation, or recompilation once a recorded trend of the uncertainty against what was tried shows the floor; the result then does not meet its required precision, and says so (NUMER.5, PRIME.3), rather than being refined without end. That stop is a stopping criterion in the sense of NUMER.10. Where the path is an alternative execution path, the recorded trend is the kind of evidence, other than the comparison, on which a path-specific limit under HW.18 rests. A different algorithm, a shallower circuit, or another device remains open, as a new path or a new result.

HW.QPU addresses four matters that NUMER owns (HW.QPU.2): the precision a result requires, through HW.QPU.6 and HW.QPU.8, which cite NUMER.5; the uncertainty of a computed result, through HW.QPU.4, which cites NUMER.13, HW.QPU.6, which cites NUMER.23, and HW.QPU.8, which cites NUMER.13; approximation disclosure, through HW.QPU.7, which cites NUMER.16; and the tolerance basis of a numerical comparison, through HW.QPU.6, which cites NUMER.25.

Each provision other than the selector and the shared-matters provision instantiates only VV, REPRO, INTPR, or RSRC. Each such provision inherits their rank and waivability (GOV.17) and is proportioned to class (GOV.11): under the project's class criteria, such as STND.CLASS.10, it applies from the least severe class at which those criteria require an LVL0 obligation it instantiates, and under STND.CLASS.10 work of CSQ4 omits it. Under STND.CLASS.10, HW.QPU.3 to HW.QPU.8 apply from CSQ3. HW.QPU.5, HW.QPU.7, and HW.QPU.8 apply from CSQ3 although STND.CLASS.10 applies INTPR.10 from CSQ2, and so tighten above the floor (PRIME.15) at the cost of one statement in a record. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| HW.CPU | General-purpose processors |
| HW.GPU | Accelerators |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| RSRC | Resources |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-18 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites HW.CPU.1 and HW.GPU.1, the selectors of the sub-profiles that a simulation of a quantum computation meets, and References lists HW.CPU and HW.GPU; the Notes name only the Articles that the provisions other than the selector and the shared-matters provision instantiate, so that the Design and Simplicity Articles, which none of them instantiates, are no longer named; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-26 | Editorial amendment (GOV.41): the Notes state the referral of a submission that no authorization covers by PRIME.7 and PRIME.14, in place of the provision of STND.HARN on a derived configuration, which STND.HARN 1.4 withdraws; no obligation, permission, or defined meaning changes. |
