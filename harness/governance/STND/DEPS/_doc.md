---
id: "STND.DEPS"
level: "LVL2"
kind: "standard"
title: "Dependency policy"
status: "adopted"
revision: "1.3.1"
adopted: "2026-10-20"
adopted_by: "The Custodian"
instantiates: ["GOV.19", "GOV.21"]
rank: null
waivable: false
---

## Purpose and scope

This standard is the dependency management mechanism (REPRO.9) that a project constitution adopts by citation or replaces with tighter rules, and the policy for weighing a dependency (SIMPL.4). It states how a dependency is chosen, which revision is pinned and when it is reviewed, how fetched components are verified, what the dependency record holds, which lock files are kept under version control, which revisions the builds of the checks and of the releases use, and on which revisions of a declared range the checks of a release run. STND.DEPS.6 and STND.DEPS.7 instantiate GUARD.17, against the supply-chain row that STND.THRT.2 adds to every threat model, so they are binding and apply at every class; every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). No provision asks the human owner for a decision; selection, pinning, and review are the work of whoever changes the dependency (STND.DRAFT.42). No provision names a tool (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Dependency record | The enumeration of external components that REPRO.9 requires, with their revisions, license identities, and reasons. |
| Fetched component | An external component that the work depends on and that an actor transfers into the provisioned environment from a system outside it. |
| Integrity digest | A cryptographic hash of the exact content of a component, recorded so that a later copy is checked against it. |
| Lock file | The file that records, for an environment or a set of packages that the work installs or builds together, the exact revision of each package that their resolution selects and, where the source of a package gives one, its integrity digest. |
| Advisory | A published notice of a defect or vulnerability in one or more revisions of a component. |
| Qualified revision | A revision of a dependency that the work's evidence, a hardware contract, or a process of fabrication or certification fixes, so that no other revision is admissible without new evidence. |

## Notes

The undivided draft that this standard replaces had dependencies selected with the human owner. That decision is not one LVL0 assigns to the human owner (STND.DRAFT.42), so STND.DEPS.1 makes it a decision record of the actor making the change, weighed on the three criteria of SIMPL.4 from stated evidence. Installing, updating, or removing a dependency is still an action that needs an authorization (PRIME.7); the project constitution template has the agent that drafts a constitution propose a standing authorization for it, bounded by sources, packages, and volume per change, so that routine dependency work proceeds unattended. A thinly supported dependency is not refused; its record states what happens after its support ends (STND.DEPS.2). The records that HDES.3, ML.3, HW.3, and AGENT.22 ask for serve as the decision records and the record of revisions where they hold the content this standard names.

The latest revision that its publisher marks as stable is the default at adoption, unless a qualified revision is fixed (STND.DEPS.3). Pinned revisions are reviewed at each release, at most every 12 months, and in the unit of work that changes one (STND.DEPS.4), the cadence that the custodian set for dependency review below LVL0; the last trigger is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit changes. Each review records a reason for each direct dependency that it leaves at its revision, one reason serving a group of dependencies that share it, since a transitive dependency stays where the direct dependency that needs it holds it (STND.DEPS.4).

A declared range of revisions that no check confirms drifts from the code: a dependent that resolves the oldest revision that the range admits meets a failure that the builds of the work never saw. STND.DEPS.14 runs the checks of each release on the oldest revisions that the declared ranges admit, together, and on the newest revisions that are consistent with one another, and runs a check at an interval, without blocking a change, on the newest revisions, so that a break that a new release of the language or of a dependency brings is seen before a release relies on it. The checks across the range run at release, the latest point at which their result is needed, since dependents rely on a declared range through a release (RSRC.12). Work that declares no range, as an application whose environment a lock file fixes, owes nothing under STND.DEPS.14. A revision that a declared range admits is one the configuration names, so a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts; a run of such a check that retrieves a revision from outside the provisioned environment is also network access, which needs its own authorization (GUARD.13), as the Notes of STND.DFLT say of every install that retrieves. STND.PY, STND.JL, and STND.RUST keep only what their languages add: the declaration of the oldest releases of a Python package, the reference version and the newest prerelease of Julia, and the edition and the oldest supported toolchain that the metadata of a Rust crate states.

STND.DEPS.6 verifies every fetched component against a recorded digest: the publisher's, where the publisher publishes one, and otherwise the digest of the first fetch, so that a later fetch that differs is caught even when no publisher signs the component. Research retrieval brings no fetched component unless the work comes to depend on what it retrieved. STND.DEPS.7 checks advisories before each release, the point at which a vulnerable revision would reach relying parties, and records as unchecked each dependency for which no authorization covers the retrieval or no source publishes advisories, so that neither absence blocks the release or passes silently. Both rest on GUARD.17, against the supply-chain row of STND.THRT.2, and bind at every class; both are normally automatic. For a project whose constitution adopts this standard, they protect more than the default threat model of STND.DFLT.18; the consequence that warrants it is undetected compromise of a fetched component, and the constitution that cites this standard is the recorded decision (GOV.11).

The files that declare a project's packages and their lock files are, in most ecosystems, already the record of the packages they install; STND.DEPS.10 lets them serve as the dependency record when they carry the reason and license identity. A lock file records the revisions that an environment or a build resolved, so that a result is regenerated with the same packages (REPRO.1); STND.DEPS.12 keeps it under version control where the environment or the build produces reported results, and asks for no lock file where the tools write none. A package that other work uses, and whose own environments and builds produce no reported result, leaves its dependents to resolve their own, and STND.DEPS.12 does not reach its lock file. STND.PY, STND.JL, and STND.RUST name the lock files of their languages, the manifest of a Julia environment among them. STND.DEPS.13 has each build of the checks and of each release use the revisions that a committed lock file records, so that what the checks judged is what the release builds; the checks of STND.DEPS.14, on the oldest and the newest revisions that a declared range admits, and those that a language standard runs at other revisions, on the newest prerelease of Julia that STND.JL.3 asks, leave the lock file. STND.LEAN.1 adds the revisions of the Lean toolchain and of each checker, which no lock file of packages records. Material copied into the work stays apart and carries a record of its origin beside it (STND.DEPS.11), so that its license and origin stay visible after the copy. The revision of each compiler, interpreter, synthesis tool, and process design kit is an input of each result it builds (STND.DEPS.8), which REPRO.1 and REPRO.2 already ask; the provision names those tools so that none is left out.

This standard names no set of dependencies. A set that served across projects is a knowledge entry of kind dependency set (STND.KNOW.2), held in the workbench until a knowledge base is designated (AGENT.30), and cited in a decision record.

Under STND.CLASS.10, every default provision applies from the class that its field `onset` gives, which work of CSQ4 may omit, STND.DEPS.5 asking for something only where a contract of DSGN.5 exists, and STND.DEPS.10, a permission, carries the value null. No default provision raises the floor (GOV.11).

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
| RSRC | Resources |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| STND.CODE | Coding standard |
| STND.DFLT | Defaults |
| STND.DRAFT | Drafting standard |
| STND.JL | Julia standard |
| STND.KNOW | Knowledge base and tags |
| STND.LEAN | Lean standard |
| STND.PY | Python standard |
| STND.RUST | Rust standard |
| STND.THRT | Threat-model template |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.1 | 2026-10-27 | Minor amendment (GOV.41): Terms define Lock file once, for an environment or a set of packages installed or built together; new STND.DEPS.12 (default, REPRO.1 and REPRO.9) keeps under version control the lock file that the tools of the work write for an environment or a build that produces reported results, the rule that STND.PY.33 and STND.JL.4 held for their languages and the first two sentences of STND.RUST.30 for Rust; the Purpose and the Notes name it. |
| 1.2 | 2026-10-28 | Minor amendment (GOV.41): new STND.DEPS.13 (default, REPRO.1) has each build of the checks and of each release of work whose lock file is under version control use the revisions that the lock file records, and fail on a lock file that does not match the files that declare its packages, other than a check that the standard of its language runs at revisions other than those that the lock file records, the rule that STND.RUST.30 held for Rust, for every language; the Purpose names it; the Notes cite it in place of STND.RUST.30, and describe STND.DFLT.11 as STND.DFLT 1.6 reads it, reviewing each dependency that the unit changes; References list STND.LEAN. |
| 1.2.1 | 2026-10-28 | Editorial amendment (GOV.41): each provision proportioned to class carries the field onset, with the class from which it applies under STND.CLASS.10, and the Notes on class onset become one sentence citing STND.CLASS.10 and the fields; no obligation, permission, or defined meaning changes. |
| 1.3 | 2026-10-28 | Minor amendment (GOV.41): new STND.DEPS.14 (default) runs the checks of each release of work that declares a range of revisions of its language or of a dependency on the oldest revisions that the ranges admit and on the newest consistent ones, and a check at an interval, without blocking a change, on the newest revisions, high-assurance code apart, in place of three cadences in STND.PY.14, STND.JL.3, and STND.RUST.1; STND.DEPS.13 excepts those checks from the locked revisions; STND.DEPS.4 records a reason for each direct dependency that a review leaves at its revision, one reason serving a group; the Purpose and the Notes follow. |
| 1.3.1 | 2026-10-31 | Editorial amendment (GOV.41): the Notes on STND.DEPS.14 say that a run of its checks that retrieves a revision from outside the provisioned environment is also network access, which needs its own authorization (GUARD.13); no obligation, permission, or defined meaning changes. |
