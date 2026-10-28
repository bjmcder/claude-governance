# Round d of 2026-10-28: cold review

Reviewer: an agent of another configuration, reading cold. Read: the standing process; `rulings.md` (D1 and the rulings); `register.md` R6.2 and R6.3 with their source entries; `decisions.md`; the four modules; the fourteen reading copies.

## What I ran

Copied `harness/governance` to `/tmp/claude-1000/rvd/governance` and applied `apply_round_d_2026_10_28` alone: entries 203 to 216. `verify`: every check PASS, the one warning g.18 (three modals in STND.CODE.28, .29, .31, STND.OFFLD.27; within the limit). `compose --all`: exactly the fourteen changed documents differ from `rendered/`; I read each diff at provision level and word level. `show` on every new, changed, and kept provision. `pairs` for all fourteen (243 to 1043 pairs each). Grepped the copy, harness docs, and skills for the twenty withdrawn identifiers: cited only in `withdrawn` fields and revision rows. Counted modals per sentence; searched new bodies for the words of STND.DRAFT.7, .13, .17; checked titles and body identifiers.

## Findings

### Defect

1. **STND.DEPS.13 conflicts with STND.PY.14.** STND.PY.14 runs the checks of a release "on the oldest declared release of Python with the oldest declared release of each dependency"; that build leaves the lock file and is no check "against newer revisions", so the new default forbids it. Replace "Other than a check that the standard of its language asks to run against newer revisions," with "Other than a check that the standard of its language asks to run at revisions other than those that the lock file records,". Amend the 1.2 row to match.

### Should-fix

2. **STND.CODE.32 widens the outcome.** STND.PY.2 and STND.RUST.31 asked the checks to decide the provisions of their own standard; the new text adds STND.CODE's, which no ruling covers and the Purpose does not describe. Replace "decide each provision of this standard and of the standard of each language of the work" with "decide each provision of the standard of each language of the work".

3. **The class paragraph calls STND.CODE.21 a default.** In "each default provision other than STND.CODE.17, STND.CODE.19, STND.CODE.20, STND.CODE.21, STND.CODE.22, ..." and "The onsets of STND.CODE.17, ..., STND.CODE.21, ... are stated above", drop STND.CODE.21; it binds at every class.

4. **STND.CODE.33 reaches C by its words while the Notes deny it.** A handler that C work installs for the signal that `abort` raises is a handler the runtime runs on a failure the language cannot propagate. Replace "and C, Fortran, Lean, and SystemVerilog." with "and Fortran, Lean, and SystemVerilog; in C, a handler that the work installs for the signal that abort raises is reached where that signal carries a listed condition." The floor argument already covers it.

5. **STND.DEPS depends on round a.** With round d alone, STND.DFLT.11 still reads "every direct dependency", so "the last trigger is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit changes" and the row's "describe STND.DFLT.11 as STND.DFLT 1.6 reads it" are false. Replace the sentence with "the last trigger is that of STND.DFLT.11." and drop the row clause.

6. **STND.BUILD's Notes become false in this round.** "STND.CODE.21 advises against compiling code" and "STND.CODE.21 advises against it for code" describe a provision that now binds, and "which STND.CXX.18 binds for C++ and STND.STDC.40 for C" reads as if they alone bind. Add an editorial transaction of STND.BUILD to round d: "advises against" to "forbids" in both places, "binds for C++" to "states for C++". Decision 1b says STND.SV's Notes say the same; they do not cite STND.CODE.21.

7. **STND.CODE.34 raises the mode for seven languages.** The claim rule bound Rust alone; D1 fixes the mode only for finite values. Decision 8a puts it to the custodian, rightly; name it as a mode change beside the floor table.

### Optional

8. STND.OFFLD.27: "as the tests at more than one number of tasks that STND.CONC.24 asks" misdescribes STND.CONC.24 (three or more). Replace with "as the tests across numbers of tasks that STND.CONC.24 asks".

9. STND.STDC.38 now asks nothing of a verification record that is no claim in a place STND.CODE.34 names. Add to the Notes of STND.STDC: "The record of a verification is a record of a result under STND.CODE.34."

10. The 1.4 row of STND.CODE omits "References lists NUMER and STND.VVUQ and drops STND.LEAN".

Everything else holds: each new provision is an outcome a withdrawn provision held; every withdrawn outcome is still held; the kept copies are cited by STND.BUILD and STND.SV; provisions name no tool or version, and Notes name documents and functions only as examples; revision classes follow STND.IDENT.3; Library code is defined once and used once; no pair across levels conflicts.

## The readings put to the custodian

| Reading | Verdict |
| --- | --- |
| 1a "elsewhere a default" | Resolve: D1's "only for" bounds the binding form and creates nothing. First reading. |
| 1b, 3a kept copies | Keep for round e; finding 6 fixes STND.BUILD now. |
| 4a STND.CODE.30 reach | Resolve: R6.2 confirms CL6 and D1 rules one provision for every language; a default. Name the reach in the ratification note. |
| 6a STND.LEAN.1 kept | Resolve: keep; its subject is the Lean toolchain and checkers, the overlap one sentence. |
| 7a Rust narrowing | Resolve: "among the means of the work" is the condition of STND.CODE.4 and blocks nothing. |
| 7b class paragraph | Resolve: drafting; see finding 3. |
| 8a STND.CODE.34 mode | Keep: truly open; binding is sound under GOV.19 and the Rust floor argument. |
| 10a typing specification, Julia manual, OpenMP | Resolve: definitions of a language or model, not products. |
| 13a QA.12 in refers_to | Resolve: the sentence names a consequence QA.12 already imposes. |
| 14a STND.OFFLD.27 | Resolve: R6.3 confirms CS19, which asked this; apply finding 8. |
| 17a CL21 | Resolve: onset, ruled C2 for round c. |
| 18 CL7 cadence | Keep for round e; the cadence needs the custodian. |
| 18 CL24 modes | Keep: the register routed CL24 to Q12. |
