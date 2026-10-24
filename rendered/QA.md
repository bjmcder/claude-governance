# Process (QA) 

This reading copy is composed from the per-provision files in QA/ of the governance harness; the harness files are the system of record.

Work is done in bounded units, judged against criteria fixed in advance, reviewed by others, and corrected in the open. Process ranks last (GOV.5) because it is able to flex to serve every Article above it. This Article implements PRIN.1, PRIN.2, PRIN.4, and PRIN.6.

## Provisions

### Units of work

#### QA.1 Definition of done

. Instantiates .

Projects MAY be open-ended; their units of work are not. Every unit of work has a definition of done and acceptance criteria (VV.3), recorded before the work is executed.

#### QA.2 Work process

. Instantiates .

Every project has a defined work process (GOV.21), in a form the project chooses, in which each unit of work is planned, executed, reviewed, and audited against its definition of done. Each stage leaves a record from which an auditor is able to reconstruct what was intended, what was done, and how it was judged.

#### QA.3 Stopping rule

. Instantiates .

Every project defines at inception a stopping rule (GOV.21) that bounds the effort, time, or cost spent on a unit of work without progress toward its definition of done. When the bound is reached, work on that unit halts and is reported to the human owner; an agent halts under GUARD.3. A unit of work created to continue halted work inherits the halted unit's bound. Only the human owner changes the rule or extends a bound, whenever the owner chooses, and the change is recorded.

### Defects

#### QA.4 Defect tracking

. Instantiates .

Every project tracks its defects (GOV.21). Each defect is recorded with what it affects and whether it is blocking, and a tracked defect is resolved on a recorded schedule.

#### QA.5 Defects found

. Instantiates .

An actor that finds a defect outside its unit of work records it in defect tracking. The actor fixes it only if the fix is small, self-contained, within its scope and authority, and touches no work another actor is changing; otherwise it reports the defect to the human owner and to whoever is responsible for the affected work, and leaves the fix to them.

#### QA.6 Broken checks

. Instantiates .

An actor whose change breaks a test or other check restores it before the change is relied upon, by correcting the change or, where the check itself is wrong, by a recorded decision (REPRO.7) that leaves the original in the record (PRIME.2). Where the check lies outside the actor's area, it seeks the help of whoever is responsible for that area or a domain expert, through the human owner where needed.

### Review and release

#### QA.7 Review

. Instantiates .

Every project has a review mechanism (GOV.21). Every change to code, data, workflow, or governance is reviewed, before release, against this document and the applicable lower governance by an actor other than its author, and the review is recorded.

#### QA.8 Review independence

. Instantiates .

Independence of review is proportioned to the consequence class (GOV.12). The independence each class requires is set by LVL2 standards and the project constitution.

#### QA.9 Regeneration

. Instantiates .

Reported results and release deployments to hardware are regenerated from their records by an actor or system other than their producer before they are relied upon, and the regeneration is recorded.

#### QA.10 Release

. Instantiates .

A release proceeds only on the decision of the human owner, with no open blocking defect, no expired waiver relied upon, and evidence current for the released revision.

#### QA.11 Promotion

. Instantiates .

A result SHALL NOT be reported before promotion: a recorded act by which the human owner adopts the proportionality judgment for its intended use (GOV.11) and confirms that the result, regenerated where that judgment requires, meets the acceptance criteria recorded before it was seen (VV.3), under VV and REPRO at the level the judgment sets; or, where the evidence VV requires is absent, confirms that the result is labeled unverified (PRIME.3) and that the gap is recorded. An agent MAY propose a promotion. Reporting an unpromoted result, or relying on one beyond its author, is a blocking defect.

#### QA.12 Post-hoc criteria

. Instantiates .

A result judged against criteria set after it was seen is promoted only as unverified (PRIME.3), with the criteria and when they were set recorded. Criteria chosen to fit the result are pathological evidence (PRIME.2).

### Correction

#### QA.13 Correction propagation

. Instantiates .

Every project provides for correction propagation (GOV.21). When a result, dataset, component, knowledge entry, or decision is found wrong, everything that depends on it is identified from the record (REPRO.4), every known relying party, inside or outside the project, is notified, and each dependent is re-verified, corrected, or withdrawn (VV.8). The record is amended, NEVER silently replaced, and the correction is itself recorded.

#### QA.14 Dependency tracking

. Instantiates .

Dependencies between results SHOULD be tracked by a mechanism that identifies affected dependents automatically, so propagation does not rely on memory.

#### QA.15 Incidents

. Instantiates .

Every project has an incident mechanism (GOV.21). An incident is recorded with its root cause, the evidence added so that it is detected next time, and whether governance failed; a governance failure is reported to the custodians (GOV.47).
