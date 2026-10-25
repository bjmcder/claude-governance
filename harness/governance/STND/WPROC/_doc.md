---
id: "STND.WPROC"
level: "LVL2"
kind: "standard"
title: "Work process standard"
status: "adopted"
revision: "1.1"
adopted: "2026-10-21"
adopted_by: "The Custodian"
instantiates: ["GOV.19", "GOV.21"]
rank: null
waivable: false
---

## Purpose and scope

This standard is the part of a work process (QA.2) that the version history carries, for covered work under version control. It records each unit of work, from the roadmap down to the smallest fix, beside its change, and keeps the records shared across units on the development line; carries each unit on its own branch; integrates concurrent work up the branch hierarchy, each merge preceded by an update from the parent, the checks the change affects, and its review; and makes each advance of the main line a release that the human owner decides. The agent roles standard gives the planning, review, and audit stages that complete the work process. STND.WPROC.12 and STND.WPROC.13 instantiate GOV.50 or a prime directive and are binding at every class, the second asking only what the release decision and AGENT.47 already rest on; every other provision is a default (GOV.19), which a project instrument replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). The defaults apply to work with or without a project constitution; for work without one, STND.DFLT.7 to STND.DFLT.10 still give the definition of done, the contents of records, the stopping bound, and the defect schedule, which these provisions complement. Below the release, no provision asks the human owner for a decision (STND.DRAFT.42). The standard uses the concepts of branch and merge that version-control systems share and names no system or tool (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Unit of work, Release, and Review have the meanings the Lexicon gives them; Agent configuration has the meaning that STND.CLASS gives it; Work report has the meaning that AGENT gives it.

| Term | Definition |
| --- | --- |
| Branch | A line of the version history of the work that changes apart from the others until it is merged. |
| Merge | The combination of the changes of one branch into another so that the history of the target contains every commit of the source, recorded in that history without rewriting it. |
| Main line | Each branch from which the work is released or deployed. |
| Development line | The branch, made from the main line, into which completed units of work are integrated before a release, and whose update makes no revision available for use beyond development. |
| Unit branch | The branch on which one unit of work is carried out. |
| Parent branch | The branch from which another branch was made. |
| Roadmap | The recorded, ordered set of milestones of the work, each with its definition of done. |
| Milestone | A unit of work that the roadmap names, whose completion a release delivers. |
| Feature | A unit of work within a milestone or within another feature. |
| Release record | The record on which the human owner decides a release, with the content that STND.WPROC.13 and STND.WPROC.14 give. |
| Permanent name | A name for one revision that is never moved to another revision or reused. |

## Notes

The work breakdown and the branch hierarchy are one structure. The roadmap names milestones; a milestone divides into features, and a feature into features of its own, to whatever depth the work needs; each unit that changes the work has a branch made from its parent unit's branch, or from the development line where the parent has none (STND.WPROC.5), and is merged back only into that branch, one merge at a time (STND.WPROC.7). Concurrent units therefore meet only at their common parent: siblings never merge into each other, and each picks up its siblings' merged work by merging its parent into itself (STND.WPROC.8). The branch hierarchy, with one merge at a time into each branch, is the protocol for concurrent change that DSGN.15 and AGENT.39 ask for; its invariant, that every branch's history contains its parent's state at its last update, is read from the history itself. The history is not linear where concurrent work merges. Rewriting or force-overwriting history is reserved to the human owner (GUARD.5, PRIME.6), so agents combine work by merges, never by rewriting branches, and a merge keeps every commit of its source, so the attribution of STND.WPROC.2 survives. Merged branches stay; the deletion of a remote branch or of a permanent name is outside the standing authorizations that STND.PROJ.3 proposes.

Records follow the work they concern (STND.WPROC.4). A unit's record, created on its parent's branch before the unit branch is made (on the unit branch itself for a fix made from a main line), travels with the branch, so the unit's agents read it, its research notes, and its records of AGENT.22 to AGENT.25 where they work, and the records reach the development line by the merges that carry the work; each directing agent writes the records of the units it directs on its own branch (AGENT.21). Only the records shared across units, and the records of a unit that has no branch, are kept on the development line, the shared records changed there one change at a time: the ledger, whose hash chain would fork if two branches appended to it (PRIME.5, GOV.36), the roadmap, defect tracking, and the record of decisions awaiting the human owner. A unit record holds dated entries, so its status changes by a new entry rather than an edit (STND.WPROC.1), and it is read from the repository itself, without a separate tracker, surviving the loss of every tool (INTPR.12). A project that uses a tracker as well records its identifiers in the unit record. A halted unit's record states the halt and its reason (GUARD.3).

A fix branches from the most upstream branch that its defect affects: a defect in a released revision is fixed from the main line, released, and reaches the development line and each branch below it as each merges its parent into itself, while the development line continues on its other work meanwhile (AGENT.15); a defect found only in a unit's own change is fixed on that unit's branch (STND.WPROC.6).

Before a branch is merged into its parent, the parent's current state is merged into it, which is where conflicts are resolved; a resolution is part of the change that the checks and the review then judge (STND.WPROC.8 to STND.WPROC.10). A conflict that the records of the two units do not decide goes to the lead agent, which refers it only where it needs a decision of the human owner. If the parent moves again before the merge by a change to its work rather than to the shared records, the update and checks are repeated, and the repeated review concerns what the new update changed, a conflict resolution above all. A check too costly for every merge, such as a long stochastic run or a synthesis, is deferred to the release under RSRC.12, recorded in the unit record, and run on the revision released. STND.TEST.3 and STND.TEST.5 have a test of a tier that the selection of a merge does not draw on run at the first merge nearer the development line whose depth draws on its tier, and at the latest at the merge into the development line, a deferral under RSRC.12 like the one to the release; a test in quarantine under STND.TEST.13 is one on whose verdict no merge relies, and QA.6 still has an actor restore a check that its own change broke. STND.WPROC.9 has the unit record state each such test, or cite the record of the run under STND.TEST.9 that states it. STND.TEST holds the selection of the checks that a change is able to affect, and the full-suite run before a release. The review of each merge is recorded with its reviewer and configuration, at the agent rows of STND.CLASS.18: the CSQ2 row for work of CSQ2 and more severe classes, the CSQ3 row otherwise. The human reviews that the CSQ1 and CSQ0 rows add fall before the release, which QA.7 requires, and the release record carries them (STND.WPROC.14), so that no merge below the release waits on a human. Each finding is resolved and confirmed by the reviewer, or recorded in defect tracking with whether it blocks release, before the merge.

An agent then merges into each parent other than a main line without a decision of the human owner (STND.WPROC.11). A project that wants per-merge approval at some class states it as a tighter project rule. Pushing a merge to a remote repository is a remote write that proceeds under a standing authorization of the kind STND.PROJ.3 proposes, where the human owner has granted one; otherwise only the push is referred.

Advancing a main line releases a revision, because a main line is a branch from which the work is used beyond its development; a branch that supports an older release is a main line too. The human owner decides each advance at every class (GOV.50, QA.10, STND.WPROC.12). The revision exists before it is named and contains the main line's current state, so that no advance overwrites history (GUARD.5, PRIME.6): it is made on the development line or on a fix branch after that branch merged the main line into itself (STND.WPROC.8), so that the advance moves the main line to it without creating a revision that no one approved; the first revision of a new main line is not an advance. The decision is recorded, names the revision, and, where an agent carries it out, is the per-action authorization that GUARD.11 asks for the advance, its permanent name, and their publication where the work has a remote repository. A blocking defect recorded or a waiver expired after the decision stops the advance, as QA.10 asks. The custodian's first model had the human owner execute the merge at CSQ2 and above; the decision that names the revision keeps the same control at the cost of one record, and the human owner remains free to execute it.

The proposal states, at every class, the revision and what the work reports of its units state under AGENT.47 (STND.WPROC.13), because the release decision is the human owner's (GOV.50) and AGENT.47 instantiates PRIME.2, so that no release rests on an unstated basis. From CSQ3, the release record puts first the items on which the decision turns and gives the rest of what QA.10 asks (STND.WPROC.14); among the records that other provisions require for the release are the dependencies left unchecked under STND.DEPS.7, the human reviews of the CSQ1 and CSQ0 rows of STND.CLASS.18, the analysis of STND.CLASS.17 at CSQ0, and a record that a profile requires, such as that of HDES.ASIC.12, each cited or stated. The release record and the decision entry follow the named revision on the development line, so the released revision does not contain them. Each release carries a permanent name in the history (STND.WPROC.15).

Under STND.CLASS.10, each default provision instantiates only provisions of the Articles that STND.CLASS.10 applies in full from CSQ3, and applies from CSQ3, except that the verification of the invariants of a protocol for shared state, which DSGN.15 asks and STND.WPROC.7 and STND.WPROC.8 instantiate, applies from CSQ2; work of CSQ4 omits them. STND.WPROC.12 and STND.WPROC.13 apply at every class through GOV.50 and AGENT.47 and ask nothing that those provisions do not already rest on. No provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES.ASIC | Integrated circuit design |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| STND.CLASS | Consequence-class criteria |
| STND.DEPS | Dependency policy |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.PROJ | Project constitution template |
| STND.TEST | Testing methods standard |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-21 | Adopted. |
| 1.1 | 2026-10-25 | Minor amendment (GOV.41): STND.WPROC.9 excepts from the checks that pass before a merge a check deferred under RSRC.12 to a later merge or to the release, and a test in quarantine under STND.TEST.13, each recorded in the unit record or in a record of STND.TEST.9 that the unit record cites, where it excepted a check deferred to the release only; the Notes say how STND.TEST.5 defers the tests of a tier to a nearer merge, that QA.6 still applies to a check that the change broke, and that STND.TEST governs the selection and the full-suite run; References lists STND.TEST. |
