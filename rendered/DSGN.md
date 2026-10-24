# Design (DSGN) 

This reading copy is composed from the per-provision files in DSGN/ of the governance harness; the harness files are the system of record.

A system is correct only to the extent that its parts have stated obligations and are held to them. This Article implements PRIN.3, PRIN.5, and PRIN.6.

## Provisions

### Contracts

#### DSGN.1 Contracts

. Instantiates .

Every interface is a contract: a component declares what it requires, guarantees, and preserves. Behavior under an unrejected precondition violation is unspecified and SHALL NOT be relied upon.

#### DSGN.2 Contract checking

. Instantiates .

Preconditions are checked, and violations rejected, where untrusted data enters; postconditions and invariants are checked wherever checking is cheap relative to a wrong result propagating. Checks too costly for production are retained for verification while what they check exists.

#### DSGN.3 Mechanical checking

. Instantiates .

Contracts, schemas, and units of measure SHOULD be checked mechanically wherever the means allows; the means is the implementer's choice.

#### DSGN.4 Schemas

. Instantiates .

Every data structure crossing an interface declares its shape and validity range and, where applicable, its units and coordinate convention. Unit and convention errors are contract violations caught at the boundary.

#### DSGN.5 External contracts

. Instantiates .

Wherever a system relies on an external component, or drives, reads, or executes on hardware, and its behavior affects the result, a contract states the behavior relied upon in the regime of use. The system depends on the contract, so the logic above is verified without the dependency, and the dependency is verified against the contract in that regime (VV.1). Its known defects are tracked (INTPR.10).

#### DSGN.6 Interface change

. Instantiates .

Interfaces change as understanding improves. Contracts are versioned, so a dependent always knows which contract it relies on. A change to an interface that others rely on is announced to its dependents with a migration path, and the prior form remains available, or the break is declared, until each dependent has migrated or is recorded as retired.

### Structure

#### DSGN.7 Dependency structure

. Instantiates .

Each component depends only on the stated contracts of the components it uses, and NEVER on knowledge of a component that depends on it; dependencies form no cycle. The structure is chosen per system and recorded (REPRO.7).

#### DSGN.8 Separation of concerns

. Instantiates .

Concerns that change for different reasons are held in different components, so a change to one does not require changing the other.

#### DSGN.9 Separability

. Instantiates .

Every component SHALL be exercisable in isolation with stand-ins for its dependencies, and is replaceable and understandable on its own. A component testable only through the whole system is not yet designed.

#### DSGN.10 Composition

. Instantiates .

Components SHOULD be built by composing independent parts rather than by inheriting from one another, unless inheritance is the most logically intuitive structure for the work at hand.

#### DSGN.11 Extension points

. Instantiates .

New models, methods, hardware targets, and data formats are added without altering code whose verification they do not otherwise affect. A change that requires editing verified core code to add a variant reveals a missing extension point; the response adds the point, not the special case.

#### DSGN.12 Present-need abstraction

. Instantiates .

An abstraction is introduced for a present or certain need, NEVER speculatively (SIMPL.3). A single-use abstraction is excess complexity under SIMPL, except the contracts DSGN.5 requires and the stand-ins DSGN.9 requires, whose second case is the test.

#### DSGN.13 Room to scale

. Instantiates .

Design choices SHOULD NOT preclude scaling the work is plausibly expected to need, so that it is admitted later without costly rework. Admitting scale is distinct from building it (SIMPL.3, RSRC.8).

### State and effects

#### DSGN.14 State

. Instantiates .

Every piece of mutable state belongs to one component, has a stated lifetime, and is mutated visibly at the interface. Hidden global state SHALL NOT exist; hidden coupling through shared state is a design defect.

#### DSGN.15 Concurrency

. Instantiates .

Concurrent access to shared state follows a stated protocol whose invariants are verified (VV.10).

#### DSGN.16 Effects

. Instantiates .

Input/output, timing, hardware access, randomness, and mutation of shared state are confined to declared places, so computation is testable apart from them.

#### DSGN.17 Randomness

. Instantiates .

Randomness enters through an explicit source identified at the boundary, seedable wherever reproducibility requires (REPRO.1, REPRO.3).
