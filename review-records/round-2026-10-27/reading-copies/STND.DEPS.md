# Dependency policy (STND.DEPS) 1.1

Adopted by The Custodian as revision 1.0 in ledger entry 95 (2026-10-20); revised to 1.1 in entry 189 (2026-10-27). This reading copy is composed from the per-provision files in STND/DEPS/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard is the dependency management mechanism (REPRO.9) that a project constitution adopts by citation or replaces with tighter rules, and the policy for weighing a dependency (SIMPL.4). It states how a dependency is chosen, which revision is pinned and when it is reviewed, how fetched components are verified, what the dependency record holds, and which lock files are kept under version control. STND.DEPS.6 and STND.DEPS.7 instantiate GUARD.17, against the supply-chain row that STND.THRT.2 adds to every threat model, so they are binding and apply at every class; every other provision is a default (GOV.19), which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7). No provision asks the human owner for a decision; selection, pinning, and review are the work of whoever changes the dependency (STND.DRAFT.42). No provision names a tool (GOV.18).

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

The latest revision that its publisher marks as stable is the default at adoption, unless a qualified revision is fixed (STND.DEPS.3). Pinned revisions are reviewed at each release, at most every 12 months, and in the unit of work that changes one (STND.DEPS.4), the cadence that the custodian set for dependency review below LVL0; the last trigger narrows that of STND.DFLT.11, which reviews every direct dependency, to the pinned revision that the unit changes.

STND.DEPS.6 verifies every fetched component against a recorded digest: the publisher's, where the publisher publishes one, and otherwise the digest of the first fetch, so that a later fetch that differs is caught even when no publisher signs the component. Research retrieval brings no fetched component unless the work comes to depend on what it retrieved. STND.DEPS.7 checks advisories before each release, the point at which a vulnerable revision would reach relying parties, and records as unchecked each dependency for which no authorization covers the retrieval or no source publishes advisories, so that neither absence blocks the release or passes silently. Both rest on GUARD.17, against the supply-chain row of STND.THRT.2, and bind at every class; both are normally automatic. For a project whose constitution adopts this standard, they protect more than the default threat model of STND.DFLT.18; the consequence that warrants it is undetected compromise of a fetched component, and the constitution that cites this standard is the recorded decision (GOV.11).

The files that declare a project's packages and their lock files are, in most ecosystems, already the record of the packages they install; STND.DEPS.10 lets them serve as the dependency record when they carry the reason and license identity. A lock file records the revisions that an environment or a build resolved, so that a result is regenerated with the same packages (REPRO.1); STND.DEPS.12 keeps it under version control where the environment or the build produces reported results, and asks for no lock file where the tools write none. A package that other work uses, and whose own environments and builds produce no reported result, leaves its dependents to resolve their own, and STND.DEPS.12 does not reach its lock file. STND.PY, STND.JL, and STND.RUST name the lock files of their languages, the manifest of a Julia environment among them, and STND.RUST.30 adds builds from the revisions that a committed lock file records. Material copied into the work stays apart and carries a record of its origin beside it (STND.DEPS.11), so that its license and origin stay visible after the copy. The revision of each compiler, interpreter, synthesis tool, and process design kit is an input of each result it builds (STND.DEPS.8), which REPRO.1 and REPRO.2 already ask; the provision names those tools so that none is left out.

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
| STND.JL | Julia standard |
| STND.KNOW | Knowledge base and tags |
| STND.PY | Python standard |
| STND.RUST | Rust standard |
| STND.THRT | Threat-model template |
| VV | Correctness |

## Provisions

### Selection

#### STND.DEPS.1 Dependency selection criteria

Default. Instantiates SIMPL.4, REPRO.7.

The decision record of each adoption, replacement, or removal of a dependency SHOULD weigh, against an owned implementation, each criterion of the table of this provision, from the evidence that its row gives (SIMPL.4, REPRO.7).

| Criterion | Evidence |
| --- | --- |
| Applicability | The part of the dependency that the work uses, and the part of the regime of use that its stated behavior covers |
| Active support | The dates of its recent revisions, its responses to reports of defects and vulnerabilities, and the number of people whom its record shows supporting it |
| Carrying cost | Its exposure of the work to compromise through its supply chain, its footprint on constrained targets, its expected life, the fit of its license terms to the work's use and distribution, and the readability of the work without it |

#### STND.DEPS.2 Thinly supported dependencies

Default. Instantiates SIMPL.4.

Where the record of a dependency's revisions and responses shows at most one person supporting it, its decision record SHOULD state how the work continues after that support ends (SIMPL.4).

### Revisions

#### STND.DEPS.3 Initial revision choice

Default. Instantiates REPRO.9.

Where the work fixes no qualified revision of a dependency, the revision that the work adopts SHOULD be the most recent one that its publisher marks as stable and that is consistent with the rest of the computational environment (REPRO.9).

#### STND.DEPS.4 Pinned revision review

Default. Instantiates REPRO.9, REPRO.7.

At each release, at intervals of at most 12 months, inclusive, and in each unit of work that changes a pinned revision, each pinned revision SHOULD be reviewed (REPRO.9). Each review SHOULD record why each dependency that it leaves at its revision stays there (REPRO.7, REPRO.9).

#### STND.DEPS.5 Contract tests on update

Default. Instantiates DSGN.5, VV.8.

Before a change of the pinned revision of a dependency is relied upon, the tests that verify the work's contract with that dependency SHOULD pass on the new revision (DSGN.5, VV.8).

### Integrity

#### STND.DEPS.6 Fetched component integrity

Binding. Instantiates GUARD.17.

Before an actor uses a fetched component, it SHALL verify the component against the integrity digest recorded for it (GUARD.17). Where the publisher of a fetched component publishes an integrity digest, the digest recorded for the component SHALL be that one (GUARD.17). Where the publisher publishes none, the actor that first fetches the component SHALL record the digest of the component as fetched (GUARD.17).

#### STND.DEPS.7 Advisories before release

Binding. Instantiates GUARD.17, PRIME.2, QA.4.

Before each release, the actor that prepares it SHALL check the published advisories of each pinned dependency for which an authorization in force covers the retrieval and a source publishes advisories (GUARD.17). That actor SHALL record each other pinned dependency as unchecked in the record of the release (GUARD.17, PRIME.2). Each advisory that applies to a pinned revision and to a feature that the work uses SHALL be recorded in defect tracking (GUARD.17, QA.4).

### Records

#### STND.DEPS.8 Toolchain revisions as inputs

Default. Instantiates REPRO.1, REPRO.2.

The revision of each compiler, interpreter, synthesis tool, and process design kit that builds or runs the work SHALL be recorded as an input of each result it helps produce (REPRO.1, REPRO.2).

#### STND.DEPS.9 Development tool record

Default. Instantiates REPRO.9.

Each tool on which the development of the work depends and on whose output no result relies SHOULD be listed in the dependency record with its revision, license identity, and reason (REPRO.9).

#### STND.DEPS.10 Package files as record

Default. Instantiates REPRO.9.

Where the files that declare the work's packages, with their lock files, give each package's exact revision, reason, and license identity, those files MAY serve as the dependency record of the packages they install (REPRO.9).

#### STND.DEPS.11 Incorporated external material

Default. Instantiates REPRO.9.

Each piece of external code, data, or text that the work incorporates SHOULD be kept apart from the work's own material, with a record beside it of its origin, revision, and license identity (REPRO.9).

#### STND.DEPS.12 Lock files under version control

Default. Instantiates REPRO.1, REPRO.9.

Where the tools of the work write a lock file for an environment or a build that produces reported results, that lock file SHOULD be under version control with the source that it resolves (REPRO.1, REPRO.9).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.1 | 2026-10-27 | Minor amendment (GOV.41): Terms define Lock file once, for an environment or a set of packages installed or built together; new STND.DEPS.12 (default, REPRO.1 and REPRO.9) keeps under version control the lock file that the tools of the work write for an environment or a build that produces reported results, the rule that STND.PY.33 and STND.JL.4 held for their languages and the first two sentences of STND.RUST.30 for Rust; the Purpose and the Notes name it. |
