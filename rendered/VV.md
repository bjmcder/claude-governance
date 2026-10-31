# Correctness (VV) 

This reading copy is composed from the per-provision files in VV/ of the governance harness; the harness files are the system of record.

A result without evidence of its correctness has no standing. PRIME.2, PRIME.3, and PRIME.4 state the non-waivable core of correctness; this Article states the rest. It implements PRIN.1, PRIN.2, PRIN.3, PRIN.4, and PRIN.5.

## Provisions

### Evidence

#### VV.1 Evidence

Every claim of correctness rests on evidence, not assertion. Evidence is a reproducible comparison against a reference of known provenance, a formal proof or derivation that the implementation meets its specification, or a citation of a source confirmed under VV.2, with its assumptions stated and shown to be met.

#### VV.2 Citations

A cited source is retrieved and confirmed to support the specific claim it is cited for, and who confirmed it is recorded.

#### VV.3 Acceptance criteria

The tolerances, comparison metrics, and checks that judge a result are fixed and recorded before the result is seen. Changing them afterward is a recorded decision (REPRO.7) that leaves the original criteria in the record.

### Verification and validation

#### VV.4 Verification and validation

Verification shows that the implementation meets its specification; validation shows that the specification meets its intended use, judged against a real-world referent where one exists. Both SHALL be performed, and passing one is NEVER evidence of the other.

#### VV.5 Verification and validation status

Every reported result states, separately for verification and for validation, whether each was performed and whether it was met. Where either was not performed, does not apply for want of a real-world referent, or was not met, the report says so.

#### VV.6 Hierarchical verification

Each component is verified against its contract, each assembly of components against its model or design, and the integrated system against end-to-end references. A higher-level failure SHALL be localized to the lowest level where it is detectable.

#### VV.7 Tests

Each test states the behavior it fixes, its reference, and a justified tolerance or metric of agreement. A test that only confirms the code does what the code does is a regression guard, not correctness evidence, and SHALL be labeled as such.

#### VV.8 Maintained correctness

Every change is re-verified, before release, against the evidence it is able to affect, identified from the record (RSRC.11). Failing evidence is repaired, or the claim it supported is withdrawn.

### Assumptions and invariants

#### VV.9 Axioms

The human owner MAY declare an axiom, an assumption accepted without demonstration, as circumstances warrant. Each axiom is recorded, labeled as such wherever it bears on a result, and open to review.

#### VV.10 Invariants

Properties that the governing model, logic, or specification requires to be conserved, bounded, monotone, or symmetric are asserted, at run time where checking is cheap and at test time always. Their violation is a defect.
