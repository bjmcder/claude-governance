# The custodian's standing process and directions

This file records how the custodian has the governance corpus worked on, and the directions that hold for every round. It replaces the corresponding sections of the former HANDOFF.md, removed after the round of 2026-10-24 (see git history). The corpus itself, in `harness/governance/`, is the system of record; nothing here overrides it.

## Standing process

1. Draft outcome-based provisions that are minimal, timeless, and checkable (GOV.18). Never block work needlessly. Never require a decision of the human owner beyond what LVL0 assigns (STND.DRAFT.42).
2. Self-check against STND.DRAFT:
   - one modal per sentence, and at most three per provision;
   - each condition before its clause, one per sentence;
   - no expression of class exact in STND.DRAFT.7, and none of its review expressions ("can", "will", "is to", and the rest) where the substitution test of STND.DRAFT.9 finds it excluded;
   - the qualifiers of STND.DRAFT.13 and the quantifiers of STND.DRAFT.17 only as those provisions allow;
   - by the custodian's direction, neither "such as" nor "for example";
   - titles of six words or fewer, not verb-initial, distinct across the corpus;
   - body IDs equal `instantiates` plus `refers_to`;
   - every document named in the text listed in References.
3. Class onset follows STND.CLASS.10. Never raise the floor (GOV.11). A provision becomes binding when its `instantiates` closure reaches PRIME, GUARD, GOV, or a floor ID; argue why it raises no floor and put that argument to the custodian. Never write that the custodian has ruled something the custodian has not ruled.
4. Rehearse on a scratch copy, one transaction per document, in citation order.
5. Review with agents of another configuration: a cold review, and a STND.HARN.28 pair review. Then fixes, and a cold verification.
6. Where a round spans several documents, run a reconciliation review across them before ratification.
7. Present for ratification. Apply only after ratification.
8. Then rebuild the reading copies in `rendered/`, update `OPEN-ITEMS.md`, and update `harness/README.md` where a command or a check that it describes changed.

## Standing directions

- **Agnostic.** Platform, compiler, vendor, implementation, framework, and tool agnostic.
  - No version numbers, products, vendors, or tools in provisions; a provision states the outcome that a tool or a reviewer decides.
  - Notes name a tool or product only to explain a hazard, as an example, without a version.
  - No recommended configuration or tool table. Versions and tools are the project's choice.
  - Timeless practice over current practice.
- **Harness.** The harness is an optional, lightweight, read-only interface through which an agent queries the corpus in a code project, and a check that the corpus stays consistent. It has no enforcement layer: no blocking hook, no permission rules, and no write commands exposed to an agent, and it derives no environment configuration (2026-10-26). No work depends on it (GOV.38). The Claude Code plugin rooted at `harness/` follows the same rule.
- **Offload.** The offload standard stays agnostic and timeless, with no annexes for particular frameworks (2026-10-24).
- **Determinism (STND.VVUQ.82, .83).** Strict determinism is an option where feasible. It is not a requirement unless the acceptance criterion or the consequence class demands it. Known, declared variation within the agreed tolerance is not a defect, and agents do not churn over it. A true race condition is a correctness defect.
- **High-assurance code.** Any coding standard a decision record adopts. The edition follows the toolchain's validation status (2026-10-24, for C++). Since the closing round of 2026-10-25, STND.CODE.17 to .20 hold these rules for high-assurance code in every language, as defaults from CSQ1, and STND.CODE.18 binds every claim of conformance. Outside high-assurance code, the newest-edition rule remains a C++ rule (STND.CXX.2); it was not extended to C, Fortran, Rust, or Lean.
- **No restatement (GOV.31).** Cite the provision that holds an outcome, and add only what the document makes necessary.
- **Documentation (STND.DOCS).**
  - Written for human readers only, with no agent notes, governance, or process records in work documentation.
  - American English everywhere.
  - None of the patterns of the STND.DOCS.9 table.
  - Consistent with itself and with the code.
  - Notes carry no obligations stated in the indicative, and no narration of drafting.
- **Security constraints.**
  - "Never keep authentication credentials; delegating access is my responsibility."
  - "Never disclose secrets, explicitly or implicitly."
  - "Never circumvent paywalls; open alternatives are fine."
  - "Research retrieval is bounded at 10,000 items and 10,000 MB per effort."
  - No workaround after a failed fetch, and no mirrors, caches, or archives of blocked content.
- **Cleanup.** Cleanup needs no permission (2026-10-24). No archive copies are kept; git history is the recovery path, so commit anything worth recovering before deleting it (2026-10-24). This replaces the earlier constraint "Never irreversibly delete or overwrite large numbers of files; archive first."
- **Hosting.** The repository is local, and the size limit of the former online project no longer applies.
