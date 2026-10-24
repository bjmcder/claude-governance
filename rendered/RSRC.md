# Resources (RSRC) 

This reading copy is composed from the per-provision files in RSRC/ of the governance harness; the harness files are the system of record.

Compute time, energy, memory, silicon, money, and human attention are finite, and spending them without measurement or need is waste. PRIME.8 states the non-waivable bound on spending; this Article states the rest. It implements PRIN.3, PRIN.4, PRIN.6, and PRIN.9.

## Provisions

### Budgets

#### RSRC.1 Budgets

. Instantiates .

Each component whose resource use is material to a run states its material budgets; the system as a whole states its time, memory, energy, and cost budget, each with the problem size at which it SHALL be met.

#### RSRC.2 Unknown budgets

. Instantiates .

Where a budget is unknown or unknowable in advance, that is stated, resource use is measured and tracked from the first run so trends and regressions are visible, and a budget is stated as soon as the record supports one. Without a stated budget or a tracked record, no claim of adequacy or inadequacy SHALL be made.

#### RSRC.3 Resource observability

. Instantiates .

Time, memory, energy where measurable, and monetary cost of a run are recorded with the run (REPRO.4) so trends are visible and regressions caught.

### Optimization

#### RSRC.4 Measured optimization

. Instantiates .

Optimization is undertaken only against a measured shortfall from a stated budget or an adverse trend in the tracked record, targets the measured bottleneck, and is retained only if measurement shows it closed the gap without violating VV.

#### RSRC.5 Algorithm first

. Instantiates .

Asymptotic complexity, rate of convergence where one applies, and choice of representation are settled before every lower-level optimization.

#### RSRC.6 Supporting machinery

. Instantiates .

Supporting machinery consumes time and energy at every invocation and SHALL justify itself against the work it supports. Machinery costing more than the computation it enables is excess under SIMPL, unless a higher-ranked Article requires it (GOV.5).

#### RSRC.7 Reuse or recompute

. Instantiates .

Whether to reuse or recompute results, intermediate quantities, and expensive setup is decided on measured cost. Reuse MAY occur only where it preserves correctness and reproducibility, and is recorded where it affects a budget.

#### RSRC.8 Scale

. Instantiates .

Parallelism, distributed execution, specialized hardware, and purchased capacity are adopted when a measured baseline at the smallest feasible scale shows they are necessary, or by a recorded decision of the human owner in anticipation of scale; their overhead and efficiency are measured against that baseline. Where the hardware or the scale is the object of the work rather than its means, the baseline serves comparison, not justification.

### Human time and attention

#### RSRC.9 Human time

. Instantiates .

Design choices that save machine time at the cost of comprehension, verification effort, or maintenance are accepted only when the saving is measured, needed, and documented.

#### RSRC.10 Human attention

. Instantiates .

Information presented to a human during development and operation is concise, prioritized, and proportionate to the decision at hand. Volume that buries what matters is a defect, as is silence where action is needed.

### Effort

#### RSRC.11 Targeted verification

. Instantiates .

Each verification step runs the smallest set of checks that establishes the evidence the change requires (VV.8); broader checking runs where the change's reach requires it or at release.

#### RSRC.12 Deferred verification

. Instantiates .

Verification is queued or deferred to the latest decision point at which its result is still needed, such as before reliance, promotion, release, or deployment, so that resources are not spent on evidence that later changes would invalidate. Deferral NEVER becomes omission (GOV.7).
