# Simplicity (SIMPL) 

This reading copy is composed from the per-provision files in SIMPL/ of the governance harness; the harness files are the system of record.

Complexity is the primary carrier of defects, cost, and misunderstanding, so every element of a system bears the burden of justifying its existence. This Article implements PRIN.3.

## Provisions

### 

#### SIMPL.1 Simplest sufficient design

Among designs that meet the stated requirements, the simplest SHOULD be chosen. Simplicity is measured by what a competent human reader holds in mind to understand, verify, and change the system, not by its size or the sophistication of its construction.

#### SIMPL.2 Essential and accidental complexity

The governing model, mathematics, physics, and hardware constraints are as complex as they are, and that essential complexity is accepted. Everything added on top is accidental and bears the burden of proof.

#### SIMPL.3 No speculative building

Features, generality, configurability, and performance beyond the current, stated requirement are deferred until the requirement is real or the human owner records it as a requirement. Anticipated needs are recorded as notes, not implemented as code.

#### SIMPL.4 Dependency cost

Adopting, replacing, or removing a dependency is a recorded decision (REPRO.7), made under the project's dependency management (REPRO.9), that weighs the dependency's applicability to the problem, its active support, and the cost of carrying it against the alternative of an owned implementation.

#### SIMPL.5 Indirection

Every layer, wrapper, plugin mechanism, and configuration option exists for a specific, present consumer; one with none is removed.

#### SIMPL.6 Explicit behavior

Behavior SHOULD be declared rather than left to defaults, inference, convention, or environment. Where predicting the outcome requires a hidden rule, the rule is made visible in the code or the interface.

#### SIMPL.7 Obvious implementation

A clear, direct implementation is the reference against which each optimized or generalized replacement is verified, and the replacement SHALL demonstrate by measurement that it is needed.

#### SIMPL.8 Deletion

Code, options, data, and documentation that no longer serve a present purpose are removed from the active system. Anything a reported result depends on is retained in the record (REPRO.1, REPRO.12).

#### SIMPL.9 Component retirement

Retirement of a component or result is announced to its dependents and recorded (REPRO.7).

#### SIMPL.10 Scope

The purpose of a component or project is recorded. Work outside it is refused or spun off, NEVER quietly absorbed.

#### SIMPL.11 Isolated complexity

Irreducible essential complexity is confined to the smallest possible part of the system, documented in place, and guarded by evidence under VV proportionate to its difficulty.
