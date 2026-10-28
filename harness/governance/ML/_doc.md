---
id: "ML"
level: "LVL1"
kind: "profile"
title: "Learned models"
status: "adopted"
adopted: "2026-10-19"
revision: "1.0.2"
selector: "Binds when a learned model sits on a path that affects a result the work reports or relies on, or physical hardware (ML.1)."
parent: null
adopted_by: "The Custodian"
---

## Purpose and scope

This profile holds the obligations of work in which a learned model sits on a path that affects a result the work reports or relies on, or that affects physical hardware. Learned models fail silently in recurring ways: a model that nobody can regenerate or identify, an error estimated on data that leaked from training, an error never measured against the reference the model stands in for, inputs outside the data the model was fitted on used without warning, and parameters that change in operation without re-verification. The profile asks for an outcome against each and prescribes no architecture, training method, metric, or detector of out-of-domain inputs. This document states outcomes only. The methods, thresholds, sample sizes, schedules, and tools that meet them belong to the project's own instruments (LVL3) and to planned LVL2 standards (GOV.18). It names no framework, library, or model family.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Learned model | A model whose relation between inputs and outputs is set mainly by parameters fitted to data, rather than by a stated physical, measurement, or mathematical model, together with those parameters. |
| Training data | The data to which a learned model's parameters are fitted, and the data used to choose among models or settings. |
| Evaluation data | The data on which the error of a learned model is estimated. |
| Learned model use | An attribute, true when the classification records that a learned model sits, or is admitted to sit, on a path that affects a result the work reports or relies on, or physical hardware. |

## Selector

ML.1 states the selector: the attribute Learned model use, defined here. The domain items are learned models, their records, their error estimates, and their inputs, and each provision names one of them as its subject (STND.DRAFT.37). A calibration, a regression on a stated model, and an inversion are not learned models: MEAS and NUMER govern them. The models through which agents do the work are governed by the agent practice profile (AGENT) and the Safeguards Article (GUARD), not by this profile. A learned model used as a numerical surrogate is numerical work as well, which NUMER binds where the classification records the attribute Numerical.

## Where the rest lives

LVL0 and the documents named here already govern these matters, and this document does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Verification methods for learned surrogates, and fair comparison of learned and conventional methods | STND.VVUQ.76, STND.VVUQ.77 |
| Comparative performance claims | HW.22 |
| Automated decisions on a path affecting a result or physical hardware | INTPR.11 |
| External pretrained models and libraries as dependencies with contracts | REPRO.9, DSGN.5 |
| Randomness through an explicit, seedable source | DSGN.17 |
| Training data drawn from measurements | MEAS.3 to MEAS.7 |
| Commands from a learned model to physical hardware: hazards, limits, and first operation | CPS.3, CPS.5, CPS.6 |
| Data that identify people, and other secrets | PRIME.10 |

## Notes

ML.3 makes each model identifiable and, where affordable, regenerable: its training data by content, its procedure, settings, seeds, and starting model, or, for a model the project did not fit, its source, revision, and documented training data. A model too costly to refit is identified by the content of its parameters in each result; a hosted model whose parameters are not available is stated as not regenerable. ML.4 rests each error estimate on data kept apart from training at the level at which samples are correlated, whether by subject, time, location, or source, since splitting correlated samples at random leaks the answer; an estimate that cannot be kept apart is labeled, so nothing is blocked.

ML.5 measures the error against the reference the model stands in for, or against independent measurements, with its uncertainty and the part of the regime of use it covers, or says that the error is not estimated. Where the model feeds a numerical result, its error against a computed reference is an approximation listed under NUMER.16, and its error against a real-world referent is model-form uncertainty under NUMER.13.

ML.6 asks for detection only of what is decidable from the input, such as ranges, types, and the support of each feature; it does not ask for a detector of every shift in distribution, which no general method provides. Where the model's output commands physical hardware, an out-of-domain input leads to the response of PRIME.4, not merely to a marked output, and CPS.5 still checks every command against its limits. ML.7 treats each change of parameters as a change to be re-verified, and bounds a model that learns while it operates and monitors an indicator of its error, since a live reference is seldom available.

ML owns two shared matters and addresses two that NUMER owns (ML.2): the uncertainty of a computed result and approximation disclosure, through ML.5, which cites NUMER.13 and NUMER.16.

Every provision other than the selector and the shared-matters provision instantiates only VV, REPRO, DSGN, or INTPR, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because its check runs without a person and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| CPS | Cyber-physical and actuation |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HW | Execution hardware |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-19 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites AGENT and GUARD, which it names as governing the models through which agents do the work, and References lists AGENT and GUARD; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
