# Learned models (ML) 1.0.2

Adopted by The Custodian as revision 1.0 in ledger entry 81 (2026-10-19); revised to 1.0.1 in entry 161 (2026-10-25) and 1.0.2 in entry 260 (2026-10-28). This reading copy is composed from the per-provision files in ML/ of the governance harness; the harness files are the system of record.

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

## Provisions

### Application

#### ML.1 Learned model use selector

Instantiates GOV.25, GOV.26.

This profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26).

| Attribute | Defined by |
| --- | --- |
| Learned model use | ML |

#### ML.2 Learned model use shared matters

Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Record of a learned model | ML | ML.3 |
| Error and domain of a learned model | ML | ML.4, ML.5, ML.6, ML.7 |
| Uncertainty of a computed result | NUMER | ML.5 |
| Approximation disclosure | NUMER | ML.5 |

### Record

#### ML.3 Learned model record

From CSQ3. Instantiates REPRO.1, REPRO.9, REPRO.3.

Each learned model SHALL have a record that identifies its training data by content, its fitting procedure with its settings and seeds, and each pretrained model from which it starts with its revision, or, for a model that the project did not fit, its source, its revision, and its training data as its source documents them (REPRO.1, REPRO.9). Each learned model SHALL be regenerable from that record within a variation that the record declares, or be identified by the content of its parameters in each result that relies on it, or be stated in each such result as not regenerable (REPRO.1, REPRO.3).

### Evaluation

#### ML.4 Evaluation independence

From CSQ3. Instantiates VV.1, VV.5.

Each estimate of the error of a learned model SHALL rest on evaluation data disjoint from its training data at the level at which their samples are correlated, or be labeled as not independent of its training (VV.1, VV.5).

#### ML.5 Learned model error

From CSQ3. Instantiates VV.1, VV.4, INTPR.9, INTPR.10.

Each learned model SHALL carry an estimate of its error against the reference it approximates or against measurements independent of its training, with the uncertainty of that estimate, over evaluation data whose coverage of its regime of use the record states, or a statement in each result that relies on it that its error is not estimated (VV.1, VV.4, INTPR.9). Where an output of a learned model enters a reported numerical result that NUMER governs, its error against a computed reference SHALL enter that result as an approximation listed under NUMER.16, and its error against a real-world referent as model-form uncertainty under NUMER.13 (INTPR.9, INTPR.10).

### Domain

#### ML.6 Out-of-domain inputs

From CSQ3. Instantiates INTPR.10, DSGN.2, INTPR.7.

Each learned model SHALL state its domain of validity (INTPR.10). Each input to a learned model that falls outside the part of that domain decidable from the input SHALL be detected at run time and reported, or the output computed from it marked as outside that domain (DSGN.2, INTPR.7). Where an output of a learned model commands physical hardware, each input of that kind SHALL be detected at run time, with the response that PRIME.4 requires (DSGN.2, INTPR.7).

#### ML.7 Learned model updates

From CSQ3. Instantiates VV.8, INTPR.7.

Each learned model whose parameters change, by refitting, by fine-tuning, or by learning during operation, SHALL be verified under ML.5 before a result relies on the changed parameters, or keep its changes within bounds that its record states and monitor a stated indicator of its error while it operates (VV.8, INTPR.7).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-19 | Adopted. |
| 1.0.1 | 2026-10-25 | Editorial amendment (GOV.41): the informative Selector text cites AGENT and GUARD, which it names as governing the models through which agents do the work, and References lists AGENT and GUARD; no obligation, permission, or defined meaning changes. |
| 1.0.2 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
