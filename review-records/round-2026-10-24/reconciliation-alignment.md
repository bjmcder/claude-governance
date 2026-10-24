# Reconciliation review A: alignment across documents (round of 2026-10-24)

Method. I used the rehearsed copy `.scratch/amendments/round/governance` (139 entries; no script or harness file is newer than its ledger; `verify` passes, g.18 notices only). I composed reading copies of every STND document and NUMER from it (scratch: `/tmp/claude-1000/ra/rc`) and checked by script: document titles, the MNEM rows (order, letter distance, reasons), Terms tables across the corpus, and References against every document name in each text (bare names included). The remainder is by reading. Not checked: R8, R10, R19 (reviewer B); R24 and the rationales (reviewer C).

## Blocking

1. **STND.LEAN Terms: Toolchain clashes with STND.BUILD.** LEAN defines Toolchain as "the compiler, kernel, build tool, and core library of Lean of one release"; BUILD defines it, of a build step, as the tools the step runs with the system root. LEAN does not import BUILD's term. Fix: rename LEAN's to "Lean toolchain" (LEAN.1's title already says so) and update its uses. (R12, R15)
2. **References incomplete (R11), by script on bare names.** The harness check g.25 derives only from locators, so it passes. Missing from the table:
   - STND.WFLOW: AGENT, STND.OFFLD.
   - STND.STDC: STND.JL, STND.PY.
   - STND.RUST, STND.FTN, STND.SV: STND.DOCS.
   - STND.LEAN: STND.CODE.
   - STND.HARN: STND.IDENT.
   - STND.CXX, STND.BUILD: HDES.
   - STND.PY, STND.JL: GUARD. (The last two groups predate the round, but the brief's test fails them.)

   Fix: add the rows in the round scripts. Recommend extending g.25 to bare document names, so the table and the check agree.

## Should-fix

3. **R3 stays open.** BUILD.12 S1 and CXX.25 S2 say the same thing (every warning of the work's own source fails the checks); BUILD's Notes name CXX as the C++ form, but CXX 1.1 says nothing of BUILD. The queue's chosen option needs "a later CXX revision cites BUILD", and nothing records it. Fix: one Notes sentence in CXX 1.1 naming BUILD.11 and BUILD.12 as the general rules (editorial inside a minor amendment), or put the later revision on the open list.
4. **R5/R12: CXX.27 does not use the BUILD term.** CXX.27 says "each build from which the work reports a result or makes a release"; BUILD's Reporting build excludes a test verdict, and BUILD's Notes explain why. Fix: CXX 1.1 Notes tie CXX.27 to Reporting build. STND.FTN's Notes use "checking build" (FTN.35 context) but its Terms import only Compilation unit; import Checking build.
5. **R12: CONC Purpose uses "checkpoints" for restart state.** WFLOW's Terms refuse the word because STND.DFLT defines Checkpoint as a copy of prior state. Fix: CONC 1.0.1 Purpose says "restart state". STND.VVUQ.2 and its table row (line "restarts from a checkpoint") still use the word in the other sense: list it as an open item for a later editorial VVUQ revision.
6. **R12/R15: Panic is undefined and has two senses.** STND.RUST uses panic (unwinds or aborts; Terms define only Panic strategy). STND.LEAN uses panic (continues with a default value). Fix: a Panic term in RUST, one sentence in LEAN's Terms or Notes.
7. **R9: FTN Terms narrow the CONC term in wording.** FTN says an iteration of DO CONCURRENT "that a compiler executes in parallel with another" is a concurrent task. CONC's term covers a sequence that "is able to run" while another has not completed, and FTN's own Notes use CONC.11 on the iterations because the construct promises no parallelism. Fix: "each iteration of a DO CONCURRENT construct is a concurrent task". No other new standard narrows CONC; SV dropped its carve-out and WFLOW, STDC, RUST widen only.
8. **R1: SV.5 to SV.8 as the CONC.3 protection.** CONC's Notes and SV's Notes call SV.5 to .8 the form of CONC.3. SV.5 and SV.7 cite CONC.3; SV.6 (one writer) and SV.8 (start-up order) do not. Fix: say "SV.5 to SV.7" in CONC's Notes, or cite CONC.3 in SV.6 and SV.8.
9. **Edition term: "Edition in force" is defined by CXX and again by SV** (different scope: translation unit, source file); FTN says "Revision in force", JL "Reference version". Fix: SV and FTN import CXX's pattern by name or qualify theirs ("Verilog edition in force"); at least state the choice.
10. **R6/R16 gaps among siblings** (details below): RUST.13 S2 (hook or handler) has no counterpart in CXX.16, PY.22, JL.15; PY and JL have no foreign-interface provision; C has no counterpart of PY.25, JL.13, RUST.15 (a check of untrusted input removed by NDEBUG); PY has no committed-lock-file default (JL.4, RUST.30).
11. **PY.17 and JL.24 are word-for-word alike and restate CONC.23 in part** (GOV.31). The amendment keeps them, with the Notes naming CONC.23; already put to the custodian. Keep as a decision (D7).
12. **Mnemonic LEAN** reads as a common word (lean development); the register reason gives only the language name. Add "reads as the language" or accept. SV is at distance 2 from JL and PY (allowed, "at least 2"); all others are at 3 or more.

## Verified, no finding

- Titles: all document titles distinct; no provision title of the new standards repeats another in the corpus.
- MNEM rows: BUILD, WFLOW, STDC, RUST, FTN, SV, LEAN follow OFFLD in ledger order (entries 122, 124, 127, 129, 131, 133, 135, each before its standard); form (2 to 5 uppercase) and reasons meet IDENT.17 and .18; the STDC reason (prefix of ISO C predefined macros and pragmas) and the SV reason are accurate.
- Terms: no duplicate of a Lexicon term. Foreign interface in STDC is the substitution that the "C reading" Term announces. Step, Job, Scheduler, Generation, Restart state, Build, Reporting build, Soundness argument (with Safety kept for hazard) each defined once.
- R1: every other citation in CONC 1.0.1's Notes checked against the text of the cited provision (OFFLD.5, .8, .18, .30; OMP.7, .8, .19, .32; RUST.21, .22, .23, .33; STDC.35, .38; FTN.11; BUILD.13 S2; LEAN.4 row "Code that runs", LEAN.19; SV.23; WFLOW.32; OFFLD.9 to .12, .21 to .23). No "planned" remains in OMP, CONC, or the amended documents. Order: STND.CONC 1.0.1 at 137 after all new standards; BUILD 1.0.1 (126) after WFLOW (125).
- R2: the boundary rule appears in both Notes and in BUILD's Purpose; BUILD.23 is named the build form of WFLOW.6; each overlapping pair is resolved by citation in one direction (WFLOW to BUILD) and BUILD.1, .3, .23, .25 are named in WFLOW's Notes.
- R4, R13: BUILD Terms cover modules, compiler-loaded code, and hand-written build scripts; RUST.2, .29, FTN.2 cite BUILD in the body; FTN and STDC Notes cite BUILD.2, .3, .4, .12, .13. STND.LEAN and STND.SV cite BUILD nowhere (see D6).
- R7, R20, R21: closed. STDC.1 and STDC.2 lists equal the union of the cited CXX provisions; the C readings of CXX.15 and CXX.23 match CXX 1.1.

## Comparison of the language standards (R6, R16, R18, R22, R23)

| Question | CXX | PY | JL | STDC | RUST | FTN | LEAN | SV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Newest edition | CXX.2 default, CXX.3 agents | none (oldest and newest tested, PY.14) | JL.1 latest stable | none (Notes) | none (RUST.1 as PY.14) | none (Notes) | pinned (LEAN.1) | stated (SV.1) |
| Unsafe or unchecked | CXX.24 check or proof | none | JL.18 statement | STDC.8 etc. | RUST.3 argument, RUST.6 agents | none | LEAN.26 statement | none |
| Responses, logging | CXX.16 none | PY.22 S3 logger not alone | JL.15 S2 Warn or Error | by CXX.16 | RUST.13 S2 hook, S3 as PY | FTN.29 none | LEAN.25 none | none |
| Ignored results | CXX.17 binding | none | none | STDC.2 | RUST.14 binding | FTN.30 status | none | none |
| Untrusted input reach | none | public interface | exported | none | public interface | public procedures | none | none |
| Foreign interfaces | CXX.20, .22 | none | none | STDC.36 only | RUST.24 to .27 | FTN.27, .28 | LEAN.18, .26 | none |
| Lock files | none | none (DEPS.10) | JL.4 | none | RUST.30 | none | LEAN.1 | none |
| Checks in shipped builds | CXX.27 on | none | JL.34 tests only | CXX.27 by reading | RUST.20 tests only | FTN.35 tests only | none | none |
| Naming | CXX.14 table | PY.1 baseline | JL.6 table | Notes only | none | none | LEAN.27 by configuration | none |
| Random streams | none | PY.15 to .19 | JL.22 to .26 | none | none | none | none | SV.23 |

Recommendations (the custodian decides; none is made in the round unless stated):

- **R22.** Do not extend the newest-edition rule or CXX.3 to C, Fortran, Rust, or Lean; STDC and FTN say why. RUST.1 gives no reason for omitting it; add one sentence to RUST's Notes (toolchain and edition move together) before adoption.
- **R23.** Align the adopted PY and JL later, not in this round: JL.15 S2 (level) and PY.22 S3 (logger) both rule out an unseen record, by different means, and RUST.13 S3 follows PY. JL.13 and PY.25 are alike in force; PY lacks a committed-lock rule; CXX.27 has no counterpart in JL or RUST because safe indexing is checked in every build (RUST Notes say so).
- **R16.** Either give RUST.13 S2 counterparts in CXX.16 (terminate handler) and PY.22 (exception hooks) in a later minor amendment, or make it a default. Add a C form of the NDEBUG case to STDC (default).
- **R18.** One rule for all: the LEAN.27 form (the repository configuration names the convention; the NUMER.4 exemption) in RUST, STDC, FTN, and SV, keeping the CXX and JL tables as they stand. This adds no table and names no tool.
- **R17.** Keep the C reading. It cites and restates nothing; a move to STND.CODE is a later minor amendment of CODE and CXX.
- **R14.** Leave FTN.26. CONC 1.0.1 stays editorial; record "model-neutral rule on the order of output from concurrent tasks" for CONC's next minor revision (the gap also touches STND.MPI and STND.OMP output).

## Decisions for the custodian from this review

- D1 Untrusted input: one reach in every language (R15). Recommend: the PY/JL/RUST/FTN reach (arguments of the public interface), extended to CXX, STDC, and LEAN by a later amendment of STND.CODE that defines the term once; until then RUST and FTN keep their own definitions.
- D2 CXX citation of BUILD (item 3). Recommend: Notes sentence in CXX 1.1.
- D3 R22 and R23 as above. D4 R16 and R18 as above. D5 R14 and R17 as above.
- D6 Name BUILD in the Purpose or Notes of LEAN (LEAN.2 asks a clean build; use the BUILD term) and SV (SV.3, SV.25). Recommend yes.
- D7 PY.17 and JL.24: cite CONC.23 from the body (makes PY and JL minor) or leave. Recommend: a later amendment.

## Queue status

Closed: R1 (with items 5, 8), R2, R4, R5 (with item 4), R7, R13, R20, R21. Closed with the fix named: R9 (item 7), R11 (item 2), R12 (items 1, 5, 6), R15 (items 1, 6; D1). Decision stated: R3, R6, R14, R16, R17, R18, R22, R23. Other reviewers: R8, R10, R19, R24.
