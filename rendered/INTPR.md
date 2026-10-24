# Interpretability (INTPR) 

This reading copy is composed from the per-provision files in INTPR/ of the governance harness; the harness files are the system of record.

Systems are read more often than written and operated longer than built, so their value depends on a human understanding what they do, why, and what they are doing now. A broken escalator is a staircase; a broken elevator is a cell. This Article implements PRIN.1, PRIN.4, PRIN.5, PRIN.6, and PRIN.7.

## Provisions

### Code and documentation

#### INTPR.1 Readable code

. Instantiates .

Code is written for the human reader who verifies it: names say what a thing is or does in the domain's vocabulary, and structure mirrors the problem. A human reader with domain knowledge but none of the codebase is able to follow the computation from input to result.

#### INTPR.2 Documentation purpose

. Instantiates .

Comments and documentation are written for human readers first: they let a reader unfamiliar with the code quickly orient to what it does and how to use it, and they record why, what assumptions hold, and what the limits are. Documentation that merely restates the code is removed.

#### INTPR.3 Documentation consistency

. Instantiates .

Documentation and the artifacts it describes are mutually consistent; an inconsistency is a defect (PRIN.7).

#### INTPR.4 Units and conventions

. Instantiates .

Quantities carry their units of measure in name, type, or schema. Sign conventions, normalization choices, index origins, and reference frames are declared once, where every reader passes, and NEVER silently converted.

#### INTPR.5 Working-notes workspace

. Instantiates .

Working notes, plans, and context kept for later recovery, by every actor, are recorded in a designated workspace (GOV.21), separate from human-facing documentation. The workspace is human-readable, carries no instruction authority (PRIME.11), and is NEVER the only record of anything a reader of the code needs.

### Operation

#### INTPR.6 State reporting

. Instantiates .

Whenever an operator is able to act, the operator is able to learn what the system is doing, how far along it is, what it has decided, what resources it consumes, and whether anything is anomalous, in detail suited to the moment. Silence where the operator would act on information is a defect; so is noise that hides the signal (RSRC.10).

#### INTPR.7 Anomalies

. Instantiates .

Stalled progress or convergence, invariant drift, resource trends toward exhaustion, inputs or readings outside expected bounds, and unexpected branch frequencies are detected and reported while intervention is still possible. Each surfaced anomaly is followed to its cause, or recorded as unexplained with its bearing on each result it affects (INTPR.10).

#### INTPR.8 Diagnostics

. Instantiates .

The information needed to diagnose a failure afterward is identified at design time and captured by default, so a failure is understood from its record, without reproduction wherever reproduction is costly or impossible.

#### INTPR.9 Self-describing outputs

. Instantiates .

Every reported output states what it is, what produced it, its units and conventions, and its uncertainty or confidence basis, in a form a human is able to read without the generating software, or is accompanied by a description in such a form.

#### INTPR.10 Visible limits

. Instantiates .

The domain of validity, untested regimes, known approximations, and known defects are documented beside the features and reported to the operator when a run approaches them.

#### INTPR.11 Automated decisions

. Instantiates .

An automated decision on a path affecting a reported result or physical hardware has its inputs, outputs, and rationale recorded, and its effect verified by evidence under VV; its internals MAY remain uninspectable.

### Continuity

#### INTPR.12 Graceful degradation

. Instantiates .

Systems, their records, and their development process are designed so that if automation, agents, or tooling is lost or inoperable, a human skilled in the art is able to grasp the state of the work quickly from the artifacts themselves and resume development with little impediment. No step that a human SHALL be able to perform is encoded only in a form that requires the automation to read or execute it.

#### INTPR.13 Knowledge in artifacts

. Instantiates .

Whatever a successor skilled in the art requires to operate, verify, or change the work is recorded in its artifacts, and is NEVER held only in the memory of one person or agent.
