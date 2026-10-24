---
id: "STND.DEPS"
level: "LVL2"
kind: "standard"
title: "Dependency policy"
status: "adopted"
revision: "1.0"
adopted: "2026-10-20"
adopted_by: "The Custodian"
instantiates: ["GOV.19", "GOV.21"]
rank: null
waivable: false
---

## Purpose and scope

This standard is the dependency management mechanism (REPRO.9) that a project constitution adopts by citation or replaces with tighter rules, and the policy for weighing a dependency (SIMPL.4). It states how a dependency is chosen, which revision is pinned and when it is reviewed, how fetched components are verified, and what the dependency record holds. STND.DEPS.6 and STND.DEPS.7 instantiate GUARD.17, against the supply-chain row that STND.THRT.2 adds to every threat model, so they are binding and apply at every class; every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). No provision asks the human owner for a decision; selection, pinning, and review are the work of whoever changes the dependency (STND.DRAFT.42). No provision names a tool (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Dependency record | The enumeration of external components that REPRO.9 requires, with their revisions, license identities, and reasons. |
| Fetched component | An external component that the work depends on and that an actor transfers into the provisioned environment from a system outside it. |
| Integrity digest | A cryptographic hash of the exact content of a component, recorded so that a later copy is checked against it. |
| Advisory | A published notice of a defect or vulnerability in one or more revisions of a component. |
| Qualified revision | A revision of a dependency that the work's evidence, a hardware contract, or a process of fabrication or certification fixes, so that no other revision is admissible without new evidence. |

## Notes

The undivided draft that this standard replaces had dependencies selected with the human owner. That decision is not one LVL0 assigns to the human owner (STND.DRAFT.42), so STND.DEPS.1 makes it a decision record of the actor making the change, weighed on the three criteria of SIMPL.4 from stated evidence. Installing, updating, or removing a dependency is still an action that needs an authorization (PRIME.7); the project constitution template has the agent that drafts a constitution propose a standing authorization for it, bounded by sources, packages, and volume per change, so that routine dependency work proceeds unattended. A thinly supported dependency is not refused; its record states what happens after its support ends (STND.DEPS.2). The records that HDES.3, ML.3, HW.3, and AGENT.22 ask for serve as the decision records and the record of revisions where they hold the content this standard names.

The latest revision that its publisher marks as stable is the default at adoption, unless a qualified revision is fixed (STND.DEPS.3). Pinned revisions are reviewed at each release, at most every 12 months, and in the unit of work that changes one (STND.DEPS.4), the cadence that the custodian set for dependency review below LVL0; the last trigger narrows that of STND.DFLT.11, which reviews every direct dependency, to the pinned revision that the unit changes.

STND.DEPS.6 verifies every fetched component against a recorded digest: the publisher's, where the publisher publishes one, and otherwise the digest of the first fetch, so that a later fetch that differs is caught even when no publisher signs the component. Research retrieval brings no fetched component unless the work comes to depend on what it retrieved. STND.DEPS.7 checks advisories before each release, the point at which a vulnerable revision would reach relying parties, and records as unchecked each dependency for which no authorization covers the retrieval or no source publishes advisories, so that neither absence blocks the release or passes silently. Both rest on GUARD.17, against the supply-chain row of STND.THRT.2, and bind at every class; both are normally automatic. For a project whose constitution adopts this standard, they protect more than the default threat model of STND.DFLT.18; the consequence that warrants it is undetected compromise of a fetched component, and the constitution that cites this standard is the recorded decision (GOV.11).

The files that declare a project's packages and their lock files are, in most ecosystems, already the record of the packages they install; STND.DEPS.10 lets them serve as the dependency record when they carry the reason and license identity. Material copied into the work stays apart and carries a record of its origin beside it (STND.DEPS.11), so that its license and origin stay visible after the copy. The revision of each compiler, interpreter, synthesis tool, and process design kit is an input of each result it builds (STND.DEPS.8), which REPRO.1 and REPRO.2 already ask; the provision names those tools so that none is left out.

This standard names no set of dependencies. A set that served across projects is a knowledge entry of kind dependency set (STND.KNOW.2), held in the workbench until a knowledge base is designated (AGENT.30), and cited in a decision record.

Under STND.CLASS.10, every default provision applies from CSQ3; STND.DEPS.5 asks for something only where a contract of DSGN.5 exists, which STND.CLASS.10 asks from CSQ2. No default provision raises the floor (GOV.11).

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| GUARD | Safeguards |
| HDES | Hardware design |
| HW | Execution hardware |
| ML | Learned models |
| PRIME | Prime Directives |
| QA | Process |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.KNOW | Knowledge base and tags |
| STND.THRT | Threat-model template |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
