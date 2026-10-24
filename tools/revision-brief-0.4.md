# Revision brief for draft 0.4 (CXX, PY, JL): the custodian's rulings of 2026-10-23

Same role, permissions, and drafting rules as the earlier briefs. This brief overrides them where they differ.

## Rulings (the custodian's words in quotation marks)

**Floor judgments: all agreed.** The agent-only rules (DOCS.10, CXX.3, PY.5), the PRIME.4 response rules, and the reach of "Untrusted input" raise no floor. The Notes may now state each as "the custodian's ruling of 2026-10-23 (PRIN.10)".

**Agreed, keep as drafted:** the Python notebook exclusion and annotation-only parameter types; the Julia underscore naming; the C++ naming rows; numpydoc style; tests and scripts type-checked; the Julia manual's docstring headings; a log record at `Warn` or `Error` as visible degradation.

**Shared rule for all three: "we are platform and compiler agnostic"; "versions and tools can be selected by the project owner".**
- No provision names a version number, a compiler, a platform, a library to depend on, or a tool. State the outcome a tool or reviewer decides (GOV.18).
- The Notes carry no recommended configuration, no tool table, and no rule map for a named tool. A Note may name a tool, compiler, or library only where it is needed to explain a hazard that a provision guards against, and then as an example, without a version.
- Where a number is configuration (a line length, a time window, a version floor), the provision refers to what the repository configuration or a project instrument sets, or to STND.DEPS.
- Do not require a decision of the human owner (STND.DRAFT.42). "Project owner" choices are made in the repository configuration or a project instrument.

**CXX**
1. "Make the high assurance general enough to accept any standard as appropriate." "Don't name C++17 or MISRA, as these are not fixed or constant." High-assurance code conforms to the high-assurance coding standard that a decision record of the work adopts (REPRO.7). The record names the standard, its revision, and its deviation procedure. Conformance is claimed only as far as it was checked, and the record states by what means (PRIME.2). Keep SHALL for safety-related components of CSQ0 work and SHOULD for other high-assurance code.
2. Remove the Power of 10 restriction table from the provisions; it fixes one standard. The Notes may describe in general terms what such standards restrict.
3. "For high assurance, the validation status is more important than the language standard." The edition of high-assurance code is one that the adopted standard covers and for which the toolchain has the validation or qualification that the work requires. Name no edition.
4. "For everything else, use the latest possible that's supported by the compiler." The edition is the newest that each compiler of the toolchain documents as supported; keep the admission of later features one at a time.
5. "I don't have or intend to get any licenses for MISRA. Strike this or generalize it to be timeless and agnostic." Remove all licensing and purchase text.
6. Transition period: "not necessary." The rationale says "Transition (GOV.42): none."
7. GSL: "strike this; we are platform and compiler agnostic." State the owning-pointer outcome without naming a library: an owning raw pointer is marked by a type alias that the checks of the work recognize.

**PY**
8. Version floors, line lengths, and named tools: "strike this, it is too prescriptive." Supported Python and package versions follow STND.DEPS and the repository configuration; keep PY.15's oldest and newest combinations of what the work declares. Line length is what the repository configuration sets. The type checker, linter, formatter, and docstring validator are the project's choice; the provisions state what each must decide.
9. Remove PY.3. Its rule moves to STND.CODE.13 (below), which the Notes cite. Renumber.

**JL**
10. "Don't pin the version or tools; use the latest." The Julia version that the work declares and checks on is the latest stable release, consistent with the rest of the environment (DEPS.3). Name no version, no day count, and no package or tool. Keep the qualified-revision exception.

## Grouping (new STND.CODE.13)

"Agree, make an amendment if possible so it's more general." I am amending STND.CODE to 1.1 with CODE.13 "Statements grouped by step" (default, INTPR.1): blocks that each carry out one step, one blank line between blocks, none inside a block other than those a layout tool of STND.CODE.5 inserts, and a heading comment where the step is not evident. Content: `/home/claude/pkg/content9.py`; apply: `/home/claude/pkg/apply9.py`. Do not edit them. Cite STND.CODE.13 where your standard needs it.

## Ledger order

DOCS 100 (12:00), INSTR 1.4 101 (12:05), CODE 1.1 102 (12:07), CXX 103 (12:10), PY 104 (12:20), JL 105 (12:30). The rationale cites no ledger entry numbers, and its counts match the draft.

## Rehearsal and deliverable

Fresh copy of `/home/claude/harness/governance`; then `apply8.apply(root)`, `apply9.apply(root)`, then yours. Run `verify` and `findings.py`; regenerate `draft.md` (title it draft 0.4). Update `decisions.md` to list only what is still open. Add a "Rulings of 2026-10-23" section to `dispositions-0.2.md`, one row per ruling. Reply in under 300 words.
