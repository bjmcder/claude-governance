---
id: "STND.CODE"
level: "LVL2"
kind: "standard"
title: "Coding standard"
status: "adopted"
revision: "1.1"
adopted: "2026-10-20"
adopted_by: "The Custodian"
instantiates: ["GOV.18", "GOV.19"]
rank: null
waivable: false
---

## Purpose and scope

This standard holds the coding practice that applies to source in every language, hardware descriptions included, as outcomes that a tool or a reviewer decides from the source, its repository configuration, and its record of checks. It adds to DSGN, SIMPL, INTPR, REPRO, VV, QA, and PRIME.4 only what makes their outcomes checkable at each change. The language standards of LVL2 add the conventions of each language. STND.CODE.6 and STND.CODE.7 instantiate PRIME.4, so they are binding and apply at every class; every other provision is a default (GOV.19) and a recommendation, which a project replaces by a recorded decision with an alternative that meets the same LVL0 outcome (REPRO.7, PRIN.10). No provision names a language, tool, or method (GOV.18).

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does.

| Term | Definition |
| --- | --- |
| Repository configuration | The versioned files of the work that set how its tools build, check, format, and test it, apart from its governance. |
| Static check | A check of source or of a build that the means of the work make without running the work. |
| Execution setting | An option, flag, or variable of a compiler, interpreter, build, or run that changes which code executes. |

## Notes

Each default provision asks for the cheapest evidence that keeps an outcome of LVL0 from failing silently. A tool that looks for cycles at each change keeps DSGN.7 true as the code grows (STND.CODE.1). Inputs that change between runs, the source of randomness and the run settings included, arrive through the interface, so that DSGN.14, DSGN.16, and DSGN.17 are visible at the call; a named constant, a hardware parameter fixed at synthesis, and a fixed configuration of a constrained target are not such inputs (STND.CODE.2). A contract stated at the declaration, or a citation of the one place that declares its units and conventions, puts DSGN.1 and INTPR.4 where every reader of the interface passes (STND.CODE.3).

The repository configuration names the static checks that the languages of the work offer, and each change passes them; a finding left in place is suppressed where it occurs, with its reason, so that the reason is the decision record of REPRO.7 (STND.CODE.4). A suppression records an accepted finding; it is not a way to pass a check (PRIME.2, AGENT.47). An agent that weakens a check or a setting in the change that the check judges records the two apart (AGENT.5) and states the weakening in its work report (AGENT.47). A layout that a named tool produces and confirms costs the reviewer nothing (STND.CODE.5).

STND.CODE.6 and STND.CODE.7 rest on PRIME.4 and bind at every class, CSQ4 included, a tightening of PRIME.4 at the cost of one look at one location (PRIME.15). A check of untrusted input that an execution setting removes, as an assertion compiled out of an optimized build is, lets invalid input pass silently in the builds that run in production. A failure of a kind that PRIME.4 lists is never discarded (STND.CODE.7). Another failure that code discards carries, at that location, the reason the results stay correct, which a reviewer checks (STND.CODE.12, a default). HW.8 and HDES add the responses that hardware asks for.

A test added for each fixed defect (STND.CODE.8) is a regression guard unless its reference is independent of the code it judges (VV.7); either way it lets VV.8 detect the defect's return. A test whose verdict changes between runs of the same revision, seeds included, gives no evidence, and a test whose reference is local needs no network access, which would otherwise call for an authorization (PRIME.7) (STND.CODE.9). A constant that a measurement, a published reference, or a recorded choice fixes carries its unit, source, and revision once (STND.CODE.10), while a literal of a formula, a loop bound, and an index origin are not such constants; a measured or calibrated constant is also versioned data under REPRO.6 and MEAS. Code disabled by turning it into a comment is neither active nor retired; the source history keeps it (STND.CODE.11, SIMPL.8). The custodian directs that code be laid out by the logical grouping of its instructions, so that a reader follows a computation step by step: a blank line ends a step, and a comment names a step whose purpose its code does not show (STND.CODE.13, INTPR.1).

Under STND.CLASS.10, each default provision instantiates only DSGN, SIMPL, INTPR, REPRO, VV, or QA and applies from CSQ3; work of CSQ4 omits it. No default provision raises the floor (GOV.11). Hardware descriptions are code under this standard; HDES governs what their verification shows.

## References

| Identifier | Title |
| --- | --- |
| AGENT | Agent practice |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| INTPR | Interpretability |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| SIMPL | Simplicity |
| STND.CLASS | Consequence-class criteria |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-20 | Adopted. |
| 1.1 | 2026-10-23 | Minor amendment (GOV.41): new STND.CODE.13 groups the statements of each body into blocks, one step of the computation each, set apart by one blank line and headed by a comment where the step is not evident; the custodian's grouping direction, first given for Python, applies to every language. |
