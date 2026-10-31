# Reproducibility (REPRO) 

This reading copy is composed from the per-provision files in REPRO/ of the governance harness; the harness files are the system of record.

A result that cannot be regenerated has no standing, and a result whose origin is untraceable is neither trustworthy nor correctable. PRIME.5 states the non-waivable preservation of history; this Article states the rest. It implements PRIN.1, PRIN.2, PRIN.4, and PRIN.7.

## Provisions

### Inputs

#### REPRO.1 Recorded inputs

Every result is regenerable from recorded inputs: the source at a specific revision, the parameters, the data and its revision, the random seeds, and the identity of the computational environment. A result whose record lacks at least one of its inputs is not reproducible and SHALL NOT be reported as one.

#### REPRO.2 Computational environment

Properties of the computational environment that affect results are recorded as inputs. The method of recording is the implementer's choice; the obligation to record is not.

#### REPRO.3 Determinism

Given identical recorded inputs, the system produces bitwise identical outputs, or outputs identical within a declared tolerance, or declares exactly which outputs vary, by how much, and why. Undeclared variation is a defect.

### Records

#### REPRO.4 Provenance

Provenance is written into or alongside every output at production, by the producing software or, for a manual or instrument step, by the person or system performing it. Provenance reconstructed afterward is labeled reconstructed, and its result is not reproducible under REPRO.1 until regenerated.

#### REPRO.5 Source history

Every change to code, data, workflow, or governance is recorded and attributed to its author, with its rationale where it affects a reported result or a contract. A change authored by an agent is identified as such.

#### REPRO.6 Versioned data

Reference data, calibration constants, benchmark solutions, measured datasets, and generated test oracles each have an identity, a revision, and a recorded origin. A data change is a result change and is reviewed as such.

#### REPRO.7 Decision records

A choice of method, tolerance, approximation, or trade-off that affects a reported result or a contract is recorded when made, with the alternatives weighed and the reason for rejection; the record MAY be a comment at the point of implementation. A human reader SHALL be able to answer "why is it this way?" without asking the author.

#### REPRO.8 Dissent

Dissent raised against a decision, and how it was resolved, is recorded with the decision (PRIN.2).

### Dependencies and workflows

#### REPRO.9 Dependency management

Every project has a dependency management mechanism (GOV.21). It enumerates each external component the work depends on, including incorporated external code, data, and text, with its exact revision and license identity; records why each is carried; and reviews pinned revisions on a cadence the project sets. A dependency with no recorded reason, or whose recorded reason names no present use in the work, is removed.

#### REPRO.10 Workflows

A sequence of steps that produces a result is itself a versioned, reviewed, reproducible artifact with the same obligations as the software it orchestrates. A result from unrecorded manual steps is unreproducible.

#### REPRO.11 Agent steps

Steps an agent performs are recorded as a workflow, with the agent's identity, configuration, and instruction revision and the actions it took, so they are able to be reviewed and repeated.

### Retention

#### REPRO.12 Retention

Every project sets the retention of its records (GOV.21). Records and results are kept in formats readable without the producing tool for as long as anything relies on them, including after the tools, platforms, and people that produced them are gone.

#### REPRO.13 Preservation

Irreplaceable data is protected against loss by a recoverable copy independent of the original.

#### REPRO.14 Project retirement

A retired project is archived with its records, and its dependents are notified.
