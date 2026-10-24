# Dispositions: STND.BUILD draft 0.1 to draft 0.2

Reviews answered: `review-cold.md` (cold) and `review-pairs.md` (pairs), with the lead's decisions 1 to 6 of 2026-10-24. Provision numbers are unchanged from draft 0.1. Draft 0.2: `draft-0.2.md`; pair list: `pairs-0.2.md` (284 pairs, down from 314 because STND.BUILD.12 no longer instantiates INTPR.10).

## Defects

| Finding | Disposition |
| --- | --- |
| Cold D1: BUILD.3 allows variation that the record has no place to declare | Accepted. The Declared variation row of BUILD.25 now reads "Each output that differs between builds from the same declared inputs, with the kinds of build between which it differs, its source, and its extent", so the variation of BUILD.3 has a place. The Notes say that a declared difference is not a defect, and that an undeclared one is a defect under REPRO.3. |
| Pairs C3: the Environment row against PRIME.10 | Accepted. The row asks for each variable read that is able to change an output, with its value, "other than a variable that holds a secret, which the record names without its value (PRIME.10)"; PRIME.10 is added to refers_to. BUILD.23 keys on "a digest of the value" of such variables, and a new second sentence keeps the outputs of a step that reads a secret out of the cache, since a complete key would hold the secret or its digest. The Notes give the reason. |

## Should-fix

| Finding | Disposition |
| --- | --- |
| Cold SF1: BUILD.12 S2 on INTPR.10, and not operable as written | Accepted as option (a), per lead decision 5. The sentence now reads "The build description that a release archive holds SHOULD make a warning fail a build only under a toolchain on which the checks of that release ran (SIMPL.6)". It drops "by default" and applies from CSQ3. |
| Cold SF2(a): BUILD.21 on REPRO.10, CSQ2 | Accepted, per lead decision 5. BUILD.21 instantiates REPRO.10 and QA.7 and applies from CSQ2. |
| Cold SF2(b): BUILD.24 S2 and QA.14 | Argued in the Notes: it rebuilds what a found fault reaches, as QA.13 asks, and asks for no mechanism that tracks dependencies automatically, so CSQ3. Decision D1 below. |
| Cold SF2(c): BUILD.10 and DSGN.5 | Argued in the Notes: it declares the target set (SIMPL.6) and states no behavior of hardware relied upon, so CSQ3. Decision D2 below. A clause on QA.9 is added to the comparisons sentence. |
| Cold SF3: overlap with STND.WFLOW | Answered by lead decision 1. The rule is in the Purpose and the Notes. The Terms no longer call a build a workflow; the Notes say REPRO.10 governs it at LVL0. In 1.0 the rule names the workflow standard in words; 1.0.1 cites STND.WFLOW and names BUILD.23 as the build form of STND.WFLOW.6 (see For the coalesce). The other pairs (WFLOW.1, .2, .37) are settled by the rule, without citation. |
| Cold SF4, pairs Obs 3: BUILD.11 and .12 against CXX.4 and .25 | Answered by lead decision 2. The Purpose and Notes name CXX.4 and CXX.25 as the C++ forms, and say that the BUILD rules are the wider and why. No CXX text is drafted. |
| Cold SF5, pairs Obs 12: "reports results" against CXX.26 | Answered by lead decision 4. New term Reporting build: "A build from which the work reports a result other than the verdict of a test, or makes a release". Checking build, BUILD.13 and BUILD.25 S1 use it. The Notes cite CXX.26 and CXX.27. |
| Cold SF6, lead decision 6: narration in the Notes | Accepted. The sentences on the custodian's directions and on retrieval extracts are removed. One line remains: "Facts that the research note marks unverified do not appear in a provision." |
| Cold SF7, lead decision 3: Fortran, Rust, C | Accepted. BUILD.2 covers "files, modules, or other units that its source names", with the inputs "derived from the source at each run, by the tool that reads it or by a tool that scans it". Generated file now includes "the interface of a unit that source names" (module and crate interface files). BUILD.9 S2 covers "code that a compiler loads and runs during compilation". The Build script term includes that code. BUILD.21 is retitled "Build scripts as code" and covers each build script of the work, hand-written or generated. The Notes say that build-time code of a dependency falls under STND.DEPS. |
| Cold SF8: gaps against b1 | Accepted. The start-time check is cited to HW.7. Isolation beyond network is stated as a means that the standard does not ask for. REPRO.2 is cited as where the project states what the build environment holds. |
| Pairs C1: BUILD.5 and BUILD.20 S2 fail on declared variation | Accepted, per the lead. Both now fail "on each difference ... that the build record does not declare as variation (VV.8, REPRO.3)", and REPRO.3 is added to their instantiates. |
| Pairs C2: BUILD.14 to 18 admit only removal | Accepted, per the lead. Each provision now offers the alternative, "or be declared in the build record as a variation of that output", inside one obligation, so no second condition is added. The Notes say that each admits the two outcomes of REPRO.3 that apply to a build. |
| Pairs C4: "discard that cache whole" against GUARD.5 and PRIME.6 | Accepted, per the lead. The sentence now reads "stop taking outputs from that cache, keep the cache until each output that relied on it is identified, and build again ...". The Notes say that disposal is irrecoverable under GUARD.5, reserved to the human owner (PRIME.6), and comes after an archive. |
| Pairs Obs 1: no extent in the record row | Accepted (see D1). |
| Pairs Obs 2, lead decision 6: VVUQ.82 and .83 misdescribed | Accepted. The Notes now describe VVUQ.82 sentence 1 and sentence 3, and VVUQ.83 sentence 1. "As STND.VVUQ.82 treats a true race" is removed. |
| Pairs Obs 6: BUILD.6 forbids the update of a held generated file | Accepted. BUILD.6 opens with "Other than the update of a generated file that the version history holds, made by running its generator". |
| Pairs Obs 10: BUILD.10 S2 stops a build that takes its set from the host | Accepted. The build stops only where the configuration states "neither such a hardware model nor a rule that takes the hardware models from the accelerators of the build host". The Notes say that a target often names a family of hardware models. |
| Pairs Obs 11: BUILD.26 S2 and the interior of a range | Answered in the Notes: a declared range whose ends a build configuration builds is stated once, as checked at its ends. |

## Optional findings taken

Pairs Obs 4 (NUMER.11 for a numerical tolerance), 5 (traceability sentence softened), 8 (the HDES design record as the record of a realization), 9 (one statement serves HW.5 and BUILD.11), 13 (interpreted runs: STND.JL.5), 14 (RSRC.12 for BUILD.5), 15 (one scope for environment variables in BUILD.1, .23, and .25), 16 (Integrity digest used of build inputs and outputs; the Fetched component term of STND.DEPS decides whether DEPS.6 also applies to a remote cache's output), 17 (BUILD.22 has effect where test data is marked), and 19 (CODE.4 suppressions). Cold optional: a Terms sentence relating Toolchain to the toolchain matrix of STND.CXX.

Not taken: shortening the BUILD.25 table with "where there is one", since the rows already apply only where their item exists. Pairs Obs 7 and 18 are outside this draft. Obs 20 (the reading copy says "Adopted ... 1.0") is how the harness composes a rehearsed adoption.

## Decisions for the custodian

- D1. BUILD.24 sentence 2 applies from CSQ3 on QA.13, not from CSQ2 on QA.14. Recommended: CSQ3, because it asks for no automatic tracking mechanism.
- D2. BUILD.10 applies from CSQ3 on SIMPL.6, not from CSQ2 as a contract of DSGN.5. Recommended: CSQ3, because it declares targets and no hardware behavior.

## For the coalesce

- Corrected order, per the coordinator: `apply_build_round.py` (MNEM, then STND.BUILD 1.0), then `apply_wflow_round.py` (WFLOW 0.2, which cites STND.BUILD.1, .3, .23, and .25), then `apply_build_1_0_1.py`. STND.BUILD 1.0 states the boundary in words ("the standard for computational workflows governs the publication, retry, restart, storage, and resumption around them") and does not carry the identifier STND.WFLOW.
- `apply_build_1_0_1.py` (editorial, GOV.41, AT 2026-10-24T21:20:00+00:00, placeholder rationale) puts the citations back: STND.WFLOW in the Purpose and Notes, and STND.BUILD.23 named as the build form of STND.WFLOW.6. It rewrites the References table, raises the revision to 1.0.1, and adds its history row. No obligation changes.
- Rehearsed with `.scratch/build-draft/rehearse_build_wflow_101.py` (entries 117 to 121): all checks pass. The only finding left is the g.18 review notice that was already on STND.WFLOW.7. STND.BUILD 1.0 alone also verifies.
- Reading copies: `draft-0.2.md` (1.0 as adopted) and `draft-0.2-with-1.0.1.md` (after the amendment). Pair list: `pairs-0.2.md` (284 pairs).

# Dispositions: STND.BUILD draft 0.2 to draft 0.3

Answers `verify-0.2.md`. Provision numbers are unchanged. Draft: `draft-0.3.md` (1.0) and `draft-0.3-with-1.0.1.md`. Pair list: `pairs-0.3.md` (284 pairs, identical to `pairs-0.2.md`).

| Finding | Disposition |
| --- | --- |
| SF1: BUILD.25 Configuration row and PRIME.10 | Accepted. The row now reads "each option that the build was given, with its value, other than an option that holds a secret, which the record names without its value (PRIME.10)". |
| SF2: 1.0.1 rationale says "ratified" | Accepted. `apply_build_1_0_1.py` now says "proposed for ratification by the custodian on 2026-10-24". The rationales of `apply_build.py` and `apply_mnem_build.py` never claimed a ratification. |
| SF3: BUILD.24 Notes and STND.DFLT.15 | Accepted. Disposal, "after an archive of it, is an irrecoverable action under GUARD.5, reserved to the human owner (PRIME.6), unless an exempt class of STND.DFLT.15 applies to it". |
| SF4: last onset sentence overclaims | Accepted. Each provision "is a default that asks only what REPRO, DSGN, SIMPL, RSRC, INTPR, VV, QA, or HW.5 already ask, at the cost of wording, a setting, a check, or one record". The three already-binding citations (STND.DEPS.6, PRIME.7, PRIME.10) stay. |
| Opt 1: BUILD.13 S2 against BUILD.26 S2 | Taken. One clause: BUILD.13 S2 asks for neither a reference oracle nor a proof, which the rows of VV.1 cover; BUILD.26 S2 documents an uncovered regime, which is the INTPR.10 row. |
| Opt 2: BUILD.23 S2 "serve" only | Taken, in positive form to avoid a g.11 negated list: "the outputs of that step SHOULD be kept out of each build cache, neither stored in it nor served from it". |
| Opt 3: BUILD.12 Notes hard to parse | Taken. Both sentences rewritten; the second now says what the provision does, limiting failure on a warning to the toolchains on which the checks of the release ran. |
| Opt 4: BUILD.26 range exception only in the Notes | Taken into the provision: "or state the declared range that holds it and whose oldest and newest members a build configuration builds". The Notes point to it. |
| Opt 5: citation of STND.FTN.4 | Removed from the 0.2 dispositions above. No FTN provision is cited anywhere. |
| Opt 6: placeholder times not monotone | Left to the lead, who sets the times at the coalesce. |

Rehearsal: `.scratch/build-draft/rehearse_build_wflow_101.py` (BUILD round, then the WFLOW round, then BUILD 1.0.1; entries 117 to 121). `verify`: all eight checks PASS. `findings.py 'STND\.BUILD'`: none. The only WFLOW finding is the g.18 notice already on STND.WFLOW.7. STND.BUILD 1.0 alone also verifies.
