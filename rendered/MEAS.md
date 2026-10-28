# Measurement and instrumentation (MEAS) 1.0.1

Adopted by The Custodian as revision 1.0 in ledger entry 78 (2026-10-19); revised to 1.0.1 in entry 259 (2026-10-28). This reading copy is composed from the per-provision files in MEAS/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This profile holds the obligations of work whose reported or relied-upon results rest on data measured by instruments, sensors, or human observers: sensor and detector projects, laboratory measurement, characterization of devices, and the analysis of measured datasets. Measured data fail silently in a few recurring ways: raw readings overwritten by their corrections, observations that cannot be traced to the instrument and settings that produced them, a calibration used outside the conditions it holds for, an uncertainty quoted without its basis or with its systematic part folded into its statistical part, and observations dropped by a criterion chosen after the result was seen. The profile asks for an outcome against each and prescribes no method: no uncertainty framework, coverage factor, calibration schedule, or screening rule. This document states outcomes only. The methods, thresholds, sample sizes, schedules, and tools that meet them belong to the project's own instruments (LVL3) and to planned LVL2 standards (GOV.18). It names no instrument, method, or framework.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Observation | A value or record that an instrument, a sensor, or a human observer produces, as acquired. |
| Measured quantity | A quantity whose value is obtained from observations through a measurement model. |
| Measurement model | The relation, with its parameters, by which observations map to a measured quantity. |
| Calibration | The determination of parameters of a measurement model by comparison with a reference. |
| Measurement uncertainty | The dispersion of the values that are able to be attributed to a measured quantity, as the framework that the project chooses states it. |
| Measured data | An attribute, true when the classification records that a result that the work reports or relies on rests, or is admitted to rest, on data measured by instruments, sensors, or human observers. |

## Selector

MEAS.1 states the selector: the attribute Measured data, defined here. The domain items are observations, measured quantities, measurement models, and calibrations, and each provision names one of them, or a record, an exclusion, or a statement about one, as its subject (STND.DRAFT.37). Readings that a system uses only to compute its own commands, inside a control loop, are not the basis of a reported result and are governed by CPS; the same readings become measured data once a result that the work reports rests on them. Where measured quantities enter a numerical result, NUMER binds as well where the classification records the attribute Numerical.

## Where the rest lives

LVL0 and the documents named here already govern these matters, and this document does not restate them (GOV.31).

| Subject | Provisions |
| --- | --- |
| Provenance written at production, and versioned calibration constants and datasets | REPRO.4, REPRO.6 |
| Uncertainty or confidence basis of every reported output | INTPR.9 |
| Readings outside expected bounds, detected and reported | INTPR.7 |
| Propagation of measured inputs into numerical results, and uncertainty by source | NUMER.13, NUMER.15 |
| Inverse problems on measured data | NUMER.20 |
| Validation against a real-world referent, the split of uncertainty by kind, and their methods | VV.4, STND.VVUQ.1, STND.VVUQ.12 |
| Gaps in data from an embedded controller after a reset or stall | HW.EMBED.6 |
| Retention of records | REPRO.12 |
| Observations that identify people, and other secrets | PRIME.10 |
| Commanding, configuring, or powering physical hardware | PRIME.7, PRIME.13, CPS.3 to CPS.9 |

## Notes

MEAS asks five things. Raw observations are kept, or the reduction applied at acquisition is recorded, so that a correction can be redone (MEAS.3); a high-rate detector that triggers or histograms at acquisition meets MEAS.3 by recording the trigger or binning and its parameters. Each observation names its instrument, settings, time, and the conditions its measurement model depends on, in its own record or in the record of the acquisition run, as far as its source records them (MEAS.4); a third-party dataset meets MEAS.4 by stating what its source leaves out. Each calibration and measurement model states where and for how long it holds, or that no limit is established, and observations outside it are marked rather than silently used (MEAS.5), per observation or per interval; the calibration constants themselves carry identity, revision, and origin under REPRO.6.

MEAS.6 is the general directive on measurement uncertainty, stated per measured quantity or channel, not per sample: each measured quantity that is reported or passed on states its uncertainty and the basis of that statement, or says plainly that it is not evaluated. Where the uncertainty has a part that repeated observation averages down and a part that it does not, the two stay separate, because combining them early hides the part that more data cannot fix; a datasheet accuracy that does not separate them is stated as such. A component shared between quantities, a common calibration for instance, is identified so that its correlation is not lost downstream. The split corresponds to the aleatory and epistemic kinds of STND.VVUQ.12 only roughly, and the project states its own correspondence. Which framework, coverage, distribution, and budget a project uses is its own choice (LVL3). Once a measured quantity enters a numerical result, NUMER.15 and NUMER.13 carry its uncertainty forward.

MEAS.7 keeps selection honest: an exclusion follows a criterion fixed before the result was seen, or is recorded as set afterward, which QA.12 then treats as unverified; excluded observations remain recoverable, or the exclusion was a recorded reduction at acquisition. Outlier rejection, quality cuts, and fiducial selections are all exclusions.

Observations by human observers are measurements under MEAS. Observations that identify people are secrets where they pose a privacy risk (PRIME.10); they are kept where PRIME.10 permits secrets to be kept, and the records of MEAS.4 refer to observers by references that are not themselves secrets.

MEAS owns four shared matters (MEAS.2): observations and their acquisition, calibration of a measurement, measurement uncertainty of a measured quantity, and selection of observations for analysis. NUMER.15 addresses the measurement-uncertainty matter, and NUMER.2 lists it (STND.DRAFT.39).

Every provision other than the selector and the shared-matters provision instantiates only VV, REPRO, INTPR, or QA, inherits their rank and waivability (GOV.17), and applies from the class that its field `onset` gives under STND.CLASS.10, where a field that gives CSQ3 for content that the table of STND.CLASS.10 starts at a more severe class tightens above the floor (PRIME.15), because each costs a record and the failure it prevents is silent at every class. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| CPS | Cyber-physical and actuation |
| GOV | Governance |
| HW.EMBED | Embedded controllers |
| INTPR | Interpretability |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| STND.CLASS | Consequence-class criteria |
| STND.DRAFT | Drafting standard |
| STND.VVUQ | Verification, validation, and uncertainty quantification methods |
| VV | Correctness |

## Provisions

### Application

#### MEAS.1 Measurement selector

. Instantiates GOV.25, GOV.26.

This profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26).

| Attribute | Defined by |
| --- | --- |
| Measured data | MEAS |

#### MEAS.2 Measurement shared matters

. Instantiates GOV.26.

Each matter of the table of this provision SHALL be governed in this document by the provisions that the table gives for it (GOV.26).

| Matter | Owning profile | Provisions |
| --- | --- | --- |
| Observations and their acquisition | MEAS | MEAS.3, MEAS.4 |
| Calibration of a measurement | MEAS | MEAS.5 |
| Measurement uncertainty of a measured quantity | MEAS | MEAS.6 |
| Selection of observations for analysis | MEAS | MEAS.7 |

### Observations

#### MEAS.3 Raw observations

From CSQ3. Instantiates REPRO.4, REPRO.6.

Each observation SHALL be kept as acquired or as received from its source, with each reduction, correction, or calibration applied before it was kept recorded with its parameters, or stated as unrecorded where its source does not record it (REPRO.4, REPRO.6). Each measured quantity SHALL be traceable to the observations from which it comes and to each correction and calibration that the work applies to them (REPRO.4, REPRO.6).

#### MEAS.4 Acquisition record

From CSQ3. Instantiates REPRO.1, REPRO.4.

The record of each observation, or of the acquisition that produced it, SHALL identify, as far as the source of the observation records them, the instrument, sensor, or observer, its settings, the time of acquisition, and each condition that the measurement model states as affecting the observation, and state each of them that the source does not record (REPRO.1, REPRO.4).

### Calibration

#### MEAS.5 Calibration validity

From CSQ3. Instantiates REPRO.6, INTPR.10.

Each calibration and each measurement model SHALL state the conditions and the interval of time over which it holds, or that no limit of that kind is established (REPRO.6, INTPR.10). Each observation acquired outside those conditions or that interval SHALL be marked as such in its record (INTPR.10).

### Uncertainty

#### MEAS.6 Measurement uncertainty

From CSQ3. Instantiates INTPR.9, INTPR.10.

Each measured quantity that the work reports or passes to a computation SHALL state its measurement uncertainty with the basis of that statement, or that its uncertainty is not evaluated (INTPR.9, INTPR.10). Where that uncertainty has components that repeated observation reduces and components that it does not, the statement SHALL keep them separate, or state that its basis does not separate them (INTPR.9). Where a component of that uncertainty is shared with another measured quantity, the statement SHALL identify it as shared (INTPR.9).

### Analysis

#### MEAS.7 Selection of observations

From CSQ3. Instantiates VV.3, QA.12, REPRO.6.

Each exclusion of observations from an analysis SHALL follow a criterion recorded before the result of that analysis was seen, or be recorded, with its criterion and when it was set, as a criterion set after that result was seen (VV.3, QA.12). Each excluded observation SHALL remain recoverable from the record that MEAS.3 keeps, or its exclusion be a reduction at acquisition recorded with its parameters (REPRO.6).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-19 | Adopted. |
| 1.0.1 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
