# P2 cold review and STND.HARN.28 pair review: STND.PY 1.1, STND.JL 1.2 (2026-10-25)

## Verified by script
- Fresh `rehearse governance apply_close_p2.py` gives seq 148-152 (P1 three, PY 1.1, JL 1.2). `verify`: all checks PASS. `findings.py 'STND\.(PY|JL)'`: no defect, only g.18 notices. `check_refs` on STND.PY and STND.JL: 0 missing rows (other documents still have gaps: P5's work).
- **Rulings unchanged.** Diffed against the live corpus: PY.22, PY.25, JL.13 and JL.15 change only `refers_to` and one added citation in the body; modals and obligations are identical. PY.14 and JL.1 differ only by the CODE.19 clause.
- Reading copies match the rehearsed files. Both rationales end with the exact fixed tail and cite no round entry. Body IDs equal `instantiates` plus `refers_to` for all 15 touched provisions; one modal per sentence; titles at most six words; no banned word in the new Notes text.
- Class: minor under STND.IDENT.3 is right.
- **Pairs.** I regenerated both lists from my rehearsal: PY 57 and JL 61 pairs, identical to the drafter's.

## Defects
None.

## Should-fix
1. **PY.32 floor argument misstates a fact.** The Notes say the exception "already ends a thread or the program". That is false for the unraisable hook, which the body now reaches: the exception is dropped and the program continues. Fix: argue from the last sentence of PRIME.4 ("silent continuation past an error SHALL NOT occur"), which a replaced hook that drops a listed condition breaks directly. Say "ends a thread or the program, or is dropped". The conditioning is right: PY.32 opens "Where the work replaces a hook", as RUST.13 sentence 2 and CXX.32 ("Where the work installs a terminate handler") do. It should be, because the default hooks already print the exception, so an unconditioned rule would raise the floor.
2. **The widening is narrated in the binding provisions' Notes.** PY and JL Notes say "the reach of the ruling stays" and then "a widening that the Notes of STND.CODE put to the custodian". These contradict each other, and the second is process narration, stale at ratification. The widening reaches the ruled binding PY.25 and JL.13 to documented functions. Fix: "the reach of the ruling is kept; STND.CODE adds the interface for outside use". Record the fallback if the custodian declines: delete the documentation clause from the CODE term; PY and JL then hold.
3. **PY.35 depends on an unverified fact.** Its condition ("an interface that does not pass a Python exception on") is, by the Notes, unverified for each interface. The Notes state flatly that "the C interface of an extension module" passes exceptions on (no source, no mark). Fix: say the project decides the condition from the interface's documentation, and mark that sentence `(unverified)`.
4. **JL.38 rests on an unverified fact.** Its exception "other than an argument that a `ccall` converts for the duration of that call" depends on "a `ccall` keeps its own arguments alive", which the Notes mark unverified (a2 2c). Fix: cite the manual after checking, or drop the exception.
5. **JL.39 conflicts with JL.16 sentence 2 as written.** JL.16 has a `catch` block that receives an `InterruptException` throw it again. JL.39 has the callback catch each exception and not throw. The Notes reconcile them only by rethrowing after the call, in other code. Fix: add to JL.39 "other than an `InterruptException`, which is stored and thrown again after the call returns (STND.JL.16)" and give `refers_to` JL.16.
6. **Unmarked facts in the Notes.**
   - PY: "a compiled extension module ... its compiler checks the types of each call"; "a library that loads a shared library ... reads no declaration" (a declaration written for the loader is a counterexample); the finalizer example for the unraisable hook (a2 S1 says only "no way to handle it").
   - JL: "Because `@fastmath` assumes finite values" (a2 section 4 covers two C compilers); "dependencies included" (a2 S12 does not say so); "each index in every session" holds for built-in arrays only.
   Fix: cite or mark each.
7. **Three-modal bundles.** PY.34, JL.37 and JL.38 bundle separable remedies (types, a layout test, array form; pointers, closures, release). A project could adopt one alone, so "never applied apart" is not met (the OFFLD.16 precedent). Fix: one Notes sentence arguing each bundle, or split (CXX.20 and RUST.24 carry the same notice).
8. **PY.34 sentence 3 and JL.37 sentence 3 cannot be met as written.** A C declaration of `T*` states no "contiguity", "order of dimensions" or "strides". FTN.28 tests them instead. Fix: "that the documentation of the foreign function states", or a test as in FTN.28.
9. **The Notes claim more than the provisions.** "Memory with one owner" is said to be given for PY and JL, but PY.36 and JL.38 never ask for one owner (compare RUST.27 sentence 1). "Stated alike for C++, Rust, Python, and Julia" is not so: PY.35 is conditioned, RUST.25 allows an unwinding ABI, JL.39 is unconditioned. Fix: add "with one owner that the contract states" to PY.36 and JL.38, or reword the Notes to "in the same steps".

## Optional
- PY.33 asks for a committed lock file but no installer creates one by default. Say in the Notes that a pinned requirements file is a lock file by the Term.
- PY.32 does not reach the asyncio exception handler (unchecked).
- "No change" resolutions for the custodian to record: no PY counterpart of JL.13 sentence 3 (array libraries unverified); logging as the only visible degradation (decision 7); no JL counterpart of RUST.13 sentence 2 (the sibling item names only CXX and PY).

## Other tests
- **New defaults.** PY.33 to .36 and JL.36 to .39 are defaults (`forced` false) with onsets that follow STND.CLASS.10: CSQ2 for DSGN.4 and DSGN.5 (PY.34, PY.35, JL.37, JL.39); CSQ3 for DSGN.14 and REPRO.1/.9 (PY.33, PY.36, JL.38); CSQ1 for JL.36, as CXX.27 (same instantiates). Facts: see Should-fix 3, 4, 6.
- **Untrusted input.** PY's Public interface and JL's `export` and `public` names are kept as Terms, so the ruled reach is preserved. "An exported name is public" is marked as this standard's reading.
- **CODE.19 clause.** Present in PY.14 and JL.1, `refers_to` updated, both still defaults.
- **Siblings.** Consistent with CXX.20, CXX.22, RUST.24 to .27, FTN.27, FTN.28, JL.4, RUST.30 and DEPS.10. PY.34 lacks FTN.27's "declared once" and RUST.24's null rule (Optional). STND.CODE holds no foreign-interface provision, so nothing is restated. I agree with the dispositions.

## Pair review (each pair once)
No pair conflicts and none leaves an unowned matter. I read each other provision in full.

| Pairs | Provisions | Verdict |
| --- | --- | --- |
| PY 1-6; JL 1-11 | PY.14 and JL.1 with CPS, HDES, HW, ML, NUMER provisions | The clause only narrows a default; the others concern records or hardware designs. Share VV.8 or REPRO.2/.9 only. |
| PY 7-9, 12-14, 16-18; JL 14-16, 18-20 | PY.22/.25/.32, JL.13/.15 with HDES.14, HW.8, HW.GPU.3 | Compatible. The visible-diagnosis rules agree, and PY.32 supplies the diagnosis HW.8 asks. |
| PY 10-11, 15; JL 12-13, 17, 22-23, 28 | PY.25, JL.13, JL.36 with CPS.5, CPS.9, ML.6 | Compatible. CODE.6 and CODE.16 keep the checks in every build, and JL.36 keeps bounds checks on. |
| PY 19-28 | PY.33 with HDES, HW, MEAS, ML record provisions | Compatible. The committed lock file serves HW.3 and ML.3; the rest concern other hardware or data. |
| PY 29-33; JL 33-37 | PY.34, JL.37 with HDES.11, HDES.ASIC.10, HDES.FPGA.3, HW.13, HW.14 | HW.13 and HW.14 own boundaries between hardware types; a foreign call between languages is not one. If an accelerator is involved, one statement serves both. |
| PY 34-57; JL 38-61 | PY.35, JL.39 with CPS, HDES, HW, NUMER provisions | Unrelated; they share DSGN.5 only. |
| JL 21, 24-27, 29-32 | JL.36 with AGENT.22, HW.22, HW.CPU.4, HW.GPU.4, HW.QPU.8, NUMER.3/.16/.17 | Compatible. The cost measurement of JL.36 is an RSRC.4 measurement, so HW.CPU.4 and HW.GPU.4 add their records; HW.22 claims state the checking setting. Turning checks off is no approximation (NUMER.17). |

Coverage by script: PY 57 of 57, JL 61 of 61; every number appears in exactly one row (PY.36 and JL.38 have no pair).

## Not checked
- The a2 sources were not re-fetched.
- ctypes callback behavior, array-library bounds checks, and Julia `@fastmath` semantics: no source in the repository.
- STND.CODE's Notes on the widening (P1's), and the cold verification after fixes.
