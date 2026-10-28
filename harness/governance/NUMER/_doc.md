---
id: "NUMER"
level: "LVL1"
kind: "profile"
title: "Numerical computation"
status: "adopted"
revision: "1.4.1"
adopted: "2026-10-11"
selector: "Binds when the work computes, by a numerical method, a quantity that a mathematical model defines (NUMER.1)."
parent: null
adopted_by: "The Custodian"
---

## Purpose and scope

This profile holds the obligations of work that computes, by a numerical method, quantities that a mathematical model defines: simulation, numerical analysis, inference, optimization, and sampling, whatever the domain or hardware. Numerical work fails quietly; a wrong number looks like a right one. The profile therefore requires evidence where numerical error hides: in the specification fixed before a result is seen, in the verification of methods and the estimation of their error, in the basis of each tolerance, in rounding, in the separate sources of uncertainty, in approximations, in the characteristic failures of inverse, optimization, and stochastic problems, and in the derivatives that sensitivity analysis, inversion, and optimization rely on. It states the outcomes that the evidence establishes and the bounds within which a result is acceptable, and not how the evidence is produced: methods of verification, validation, and uncertainty quantification change as the field advances, and are chosen at LVL2 and LVL3. It names no language, library, tool, technology, platform, process, or method (GOV.18), and each provision cites the LVL0 provisions it instantiates and only tightens them (PRIME.15).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Approximation | A replacement, on the path of a numerical result, of a quantity, relation, or operation of the mathematical model that its numerical specification states by a simpler or cheaper one, other than the discretization, stopping, and rounding that make up its numerical error. |
| Derivative | The rates of change of the outputs of a computation or of a mathematical model with respect to its inputs or parameters, of first or second order, as a gradient, a Jacobian, a Hessian, or the product of one of them with a vector. |
| Discretization | The replacement of a continuous quantity, domain, or operator of a mathematical model by a finite one, set by parameters such as a mesh size, a step size, or a number of basis functions. |
| Inverse problem | A problem whose unknowns are inputs of a mathematical model, inferred from observed or prescribed outputs. |
| Mathematical model | The equations, relations, or probability laws whose solution or value a numerical result approximates. |
| Model-form uncertainty | The part of the difference between a mathematical model's prediction and the system it represents that the model's equations cause, as validation against a real-world referent assesses it (VV.4). |
| Numerical | An attribute, true when the classification records that the work computes, by a numerical method, a quantity that a mathematical model defines and reports that quantity or relies on it. |
| Numerical error | The difference between a numerical result and the exact value of its quantity of interest under its mathematical model, arising from discretization, from stopping a repeated computation before its exact limit, and from rounding. |
| Numerical method | An algorithm that computes or approximates the quantities that a mathematical model defines, including its discretization, solvers, quadrature, sampling, and optimization. |
| Numerical result | A result that is a quantity, or a set of quantities, computed by a numerical method. |
| Numerical specification | The record that states, for a numerical result, its quantity of interest, mathematical model, numerical method, required precision, and the tolerances and acceptance criteria that judge it. |
| Optimization | A problem whose result is the values of variables that extremize an objective, subject to constraints where it has any. |
| Performance approximation | An approximation adopted to meet a budget, or introduced by a default of the executing hardware or software, rather than for the accuracy of the result. |
| Propagated input uncertainty | The uncertainty of a numerical result that uncertainty in its inputs causes, carried through its computation. |
| Quantity of interest | The quantity that a numerical result reports and that its acceptance criteria judge. |
| Required precision | The tolerance on the quantity of interest of a numerical result within which its intended use needs the result to lie. |
| Statistical uncertainty | The uncertainty of an estimate that the finite number of samples from which it is computed causes. |
| Stochastic method | A numerical method that draws on random or pseudo-random numbers and whose result is an estimate. |
| Stopping criterion | A condition on which a computation that repeats or refines a step stops. |
| Working precision | The precision that the arithmetic of a computation delivers, including the effect of hardware modes, library defaults, and compiler options, and the precision in which its operands are stored and exchanged. |

## Selector

NUMER.1 states the selector. The domain items are numerical results, numerical methods, and numerical specifications; a provision about one imposes nothing on work without it (STND.DRAFT.37).

## Where the rest lives

LVL0 and the AGENT profile already govern these matters of numerical work, and this profile does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Acceptance criteria fixed before results are seen, and criteria set afterward | VV.3, QA.12 |
| Tests, their tolerances at the floor, and regression guards | VV.7 |
| Verification and validation, and their status in reports | VV.4, VV.5 |
| Assumptions accepted as axioms | VV.9 |
| Conservation, bounds, monotonicity, and symmetry of the model | VV.10 |
| Verification cost never a reason to skip verification | GOV.7 |
| Hardware precision limits honored as correctness | GOV.8 |
| Non-convergence and invalid input failing loudly | PRIME.4 |
| Results lacking evidence labeled unverified | PRIME.3 |
| Stalled convergence and invariant drift reported during a run | INTPR.7 |
| Domain of validity and known approximations documented | INTPR.10 |
| Units, scaled variables, sign conventions, and normalizations | INTPR.4 |
| External numerical components verified against their contract in the regime of use | DSGN.5 |
| Seeds and the source of randomness | DSGN.17, REPRO.1 |
| Run-to-run variation and its declaration | REPRO.3 |
| Result-affecting arithmetic and environment settings | REPRO.2 |
| Identity and origin of reference data and benchmark solutions | REPRO.6 |
| Behavior declared rather than left to defaults | SIMPL.6 |
| Admitting scale without building it | DSGN.13 |
| Features deferred until required | SIMPL.3 |
| Optimized code verified against the obvious implementation | SIMPL.7 |
| Algorithm and rate of convergence settled before lower-level optimization | RSRC.5 |
| Departures from intent and weakened checks in work reports | AGENT.47 |

## Notes

Against the two dangers that lower governance serves, this profile is aimed at silent misalignment: plausible numbers that are wrong. Its provisions are checkable from records, so an agent satisfies them unattended and a reviewer confirms them without re-deriving the work; none asks the human owner for a decision (STND.DRAFT.42).

The profile sets requirements and bounds them; it names no method (GOV.18). Each provision states what the evidence establishes, such as that a method is verified against an oracle it did not produce, that an error estimate accounts for every source, or that a stochastic acceptance criterion states its rates of false rejection and of detection, and leaves to a LVL2 standard on verification, validation, and uncertainty quantification the methods that establish it by default, and to a project instrument any alternative that meets the same outcome (GOV.19, REPRO.7). A method that becomes obsolete therefore changes the standard, not this profile.

Three requirements guard against evidence that is circular. A method is verified against an oracle exact for its problem or computed without its implementation (NUMER.6), and an error estimate rests on a method so verified (NUMER.8), since an estimate on unverified code is able to converge to a wrong answer. An inverse method is tested on data produced independently of the computation it inverts (NUMER.19), since data made by that same computation flatter it. A failed stochastic comparison is not repeated with new random numbers to obtain a pass (NUMER.26). A result whose numerical-error component NUMER.13 marks not assessed lacks the evidence NUMER.9 requires and is labeled unverified (PRIME.3, GOV.7). Tolerances under NUMER.11 come from the required precision, the estimated error, the statistical uncertainty, or the oracle's uncertainty, and not from the size of the observed discrepancy; the recorded relation shows a tolerance set far above its basis. Forward problems are governed by the general sections; problems built from other numerical results are governed by NUMER.14.

Every provision other than NUMER.1, NUMER.2, and NUMER.26 instantiates only VV, REPRO, INTPR, DSGN, SIMPL, or RSRC, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for a cited source, a stated precision, limit, or sensitivity, a disclosure, a reference oracle, or a report, content that the table of STND.CLASS.10 starts at a more severe class, tightens above the floor (PRIME.15), because each costs one statement, one record, or one message and the error it exposes is silent at every class. NUMER.6 asks at CSQ3 for a reference oracle exact for its problem or computed without the implementation it judges, which STND.CLASS.10 otherwise starts at CSQ2; this tightens above the floor (PRIME.15), because verification against an oracle the implementation produced is circular. NUMER.26 states how PRIME.2 applies to stochastic comparisons and binds at every class, adding nothing to the floor that PRIME.2 does not already hold. NUMER.18 reports a departure from the domain of validity during the run to the operator of a run during which one acts, and otherwise in the record of the run, since an unattended run has no operator to receive a message and its record is what a reader examines afterward (INTPR.7). NUMER.11 and NUMER.25 govern the tolerances of acceptance criteria and correctness evidence above the floor; at the floor VV.7 alone governs a test's tolerance. No provision raises the floor (GOV.11).

Derivatives are supported and not required. NUMER.27 asks only that a method's design not rule out computing first and second derivatives, which admits the capability without building it; a design that does rule them out records why (PRIN.10). NUMER.27 asks for no abstraction built ahead of need (DSGN.12, SIMPL.3); it is met by design choices that cost nothing now, such as effects kept apart from computation and no hidden state. Once an error in a derivative is able to change a result, NUMER.28 requires the derivative verified against an evaluation independent of its computation; a derivative that affects only cost, such as one inside a solve that stops on the true residual, is exempt. NUMER.29 requires each derivative relied upon to say what it is the derivative of, since the derivative of the implemented computation, of the discrete equations at their exact solution, and of the model differ by the discretization and the stopping of repeated computations. A derivative estimated by a stochastic method is also a result of that method under NUMER.22 to NUMER.26. The methods that compute derivatives and the checks that verify them belong to the LVL2 standard on verification, validation, and uncertainty quantification.

NUMER owns seven shared matters and addresses two that HW owns and one that MEAS owns (NUMER.2). Where HW also binds the work, NUMER states the precision a result requires and HW states what the hardware delivers: NUMER.5 records the delivered arithmetic that HW.5 states, and takes the precision of exchanged operands from the boundary contract of HW.13 wherever one states it (STND.DRAFT.39, STND.DRAFT.40), and HDES supplies the contract of a realized design through HW (HDES.5) and derives the precision of its arithmetic from the required precision of the results it feeds (HDES.7). The tolerance basis of every numerical comparison is NUMER's (NUMER.11, NUMER.25), and HW keeps the obligation to compare the alternative execution paths of a component (HW.16). Where a measured quantity is an input, NUMER.15 states what the propagation uses, taking the measurement uncertainty that MEAS.6 states where MEAS binds the work; NUMER.2 lists that MEAS matter (STND.DRAFT.39). Where an inverse problem's data are measured, MEAS owns the measurement model and calibration, and NUMER owns the inversion, its recovery test, and its computed uncertainty. ML.5 enters the error of a learned model into each numerical result it feeds, as an approximation listed under NUMER.16 against a computed reference and as model-form uncertainty under NUMER.13 against a real-world referent. This profile absorbs the NUMER problem-type entries of the hardware type annex (STND.ANNEX), which are removed from it on adoption. NUMER owns the random streams of a computation divided among concurrent tasks, as the custodian assigned at the adoption of STND.CONC: NUMER.24 has the record of a stochastic method that draws from more than one source hold evidence that the sources are free of dependence that affects the result, and the LVL2 standards give the default means, STND.CONC.23 keying each stream to a part of the computation defined independently of the number of tasks and of the task that computes it, and STND.VVUQ.62 the construction of the streams. The row of NUMER.2 assigns the matter and adds no obligation of the work, so it raises no floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| HDES | Hardware design |
| HW | Execution hardware |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| ML | Learned models |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.ANNEX | Hardware type annex |
| STND.CLASS | Consequence-class criteria |
| STND.CONC | Concurrency standard |
| STND.DRAFT | Drafting standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-11 | Adopted. |
| 1.1 | 2026-10-17 | Minor amendment (GOV.41), conforming on the adoption of HW: NUMER.2 gains the matter Tolerance basis of a numerical comparison, owned by NUMER and given by NUMER.11 and NUMER.25, and the HW matters that NUMER.5 addresses; NUMER.5 records the working precision with the delivered arithmetic of HW.5, and takes exchanged precision from HW.13 wherever a boundary contract states it; the Notes list statistical uncertainty among the bases of NUMER.11. |
| 1.1.1 | 2026-10-18 | Editorial amendment (GOV.41): the Notes describe HDES as adopted, citing HDES.5 and HDES.7, in place of a clause that its adoption made stale; no obligation changes. |
| 1.2 | 2026-10-19 | Minor amendment (GOV.41), conforming on the adoption of MEAS: NUMER.2 lists the MEAS matter Measurement uncertainty of a measured quantity, given by NUMER.15; NUMER.15 takes the uncertainty of a measured input from MEAS.6 where MEAS binds; the Notes describe MEAS and ML as adopted. |
| 1.3 | 2026-10-24 | Minor amendment (GOV.41), conforming on the adoption of STND.CONC: NUMER.2 gains the matter Random streams of a computation divided among concurrent tasks, owned by NUMER and given by NUMER.24, as the custodian assigned at the adoption of STND.CONC; the Notes count seven owned matters and cite STND.CONC.23 and STND.VVUQ.62 for the keying and construction of the streams; References lists STND.CONC and STND.VVUQ. |
| 1.4 | 2026-10-28 | Minor amendment (GOV.41): NUMER.18 reports a departure from the domain of validity to the operator of a run during which one acts and otherwise in the record of the run (CS8). |
| 1.4.1 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
