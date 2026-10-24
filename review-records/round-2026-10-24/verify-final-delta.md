# Final delta verification (cold), 2026-10-24

Copy: `.scratch/fixpass3/governance-final`. `verify`: 8 of 8 PASS, one existing g.18 warning. `findings.py` on the changed provisions: one finding, g.18 on STND.RUST.13 (three modals; its Notes say the three sentences define a response together). References check: 0 missing for the nine changed documents. Rationales 117 to 141: all end with the fixed tail; no em dash or banned word. Scratch tables: `/tmp/claude-1000/verify-final-d/part2-vvuq63.md`, `part3-build13.md`, script `pairreview.py`.

## Part 1, the delta (items 1 to 9 of fixpass-3.md)

All items do what the findings asked. No floor is raised, and none of the changed provisions has a modal, condition, or ID defect. The MNEM LEAN distance claim holds (DEPS, FTN, HARN at 3, the rest at 4 or more). The STND.CXX 1.1.1 sentence is true, since Reporting build is a subset of the builds of CXX.27, and it stays editorial. The SV.3 Notes match SV.3 and BUILD.11.

**Defect**
- None.

**Should-fix**
1. STDC.28 Notes are too narrow (Part 4): fix in Part 4.
2. All 25 rationales say "ratified by the custodian on 2026-10-24", and the RUST and HARN rationales also say the custodian decides on ratification. These contradict each other, and the ruling is not yet made. Fix: "Proposed for ratification by the custodian" until the custodian rules (V-C optional 6, left open).
3. CONC Notes: "STND.FTN.26 is the Fortran case of STND.CONC.30 in which no protocol fixes the order". FTN.26 also says "SHOULD NOT rely" on the record order across images, where synchronization can fix an order. Fix: say FTN.26 is stricter for images, which can fix an order by synchronization.
4. VVUQ Notes: "BigCrush ... is the most demanding of those of the TestU01 library" cites nothing. No research note supports it (they only say counter-based generators pass BigCrush). I believe it is true (SmallCrush, Crush, BigCrush) but did not check it. Fix: cite the TestU01 paper in a research addendum, or say "the largest".

**Optional**
- RUST rationale: "The custodian decides on ratification these floor arguments" is ungrammatical. Fix: "The custodian decides these floor arguments on ratification".
- RUST Notes call the second sentence "the diagnosis ... of a panic that ends in a halt"; the provision covers each panic no other response answers. Align the wording.

## Part 2, STND.VVUQ.63

- Checkable (GOV.18): mostly. The strength clause hands the reviewer a criterion, but "the use of the generator requires" is stated nowhere in the record. Optional fix: "as the record of the work states that the use requires".
- Agnostic: the provision names no tool. The Notes name TestU01 and BigCrush without a version, as an example, which the brief permits.
- Class: minor is right under the first matching row of STND.IDENT.3 (it alters what a default asks). GOV.41 is "Adoption" and holds no class table, so cite STND.IDENT.3 and STND.IDENT.4 for the class. No floor: it is a default, and the text is at most as demanding as the old BigCrush text.
- Pair review: 59 pairs (nos. 3661 to 3719 of 4921), each covered once by script (missing 0, extra 0, repeated 0). Conflicts: 0. Unowned matters: 0. Only NUMER.24 is the same matter, owned by NUMER, and it agrees: 63 is the default means and uses the same "affects the result" test. Three pairs share REPRO.3 only (HW.12, HDES.3, ML.3); the other 55 share VV.1.

## Part 3, STND.BUILD.13 on INTPR.10

19 pairs with HW (11, sub-profiles included), MEAS (2), ML (2), and NUMER (4): nos. 47, 50, 51, 54, 55, 56, 59, 60, 61, 63, 64, 65, 66, 68, 69, 71, 74, 76, 78. Each is covered once by script. Conflicts: 0. Unowned: 0. No shared-matters table lists a BUILD provision. HW.7 and HW.CPU.3 are supportive: a named checking build and a record of the checks it adds make the evidence of a checking build identifiable. The rest concern statements in the record of a result or another hardware type, and share INTPR.10 only.

## Part 4, retrieval (3 items, about 4.1 MB; curl only, no failure)

**std::panic::set_hook**: "The panic hook is invoked when a thread panics, but before the panic runtime is invoked. As such, the hook will run with both the aborting and unwinding runtimes." Confirmed (page footer: std 1.99.1).

**Reference, Panic chapter**: "Linking a no_std binary, dylib, cdylib, or staticlib will require specifying your own panic handler." Also "There must be a single panic_handler function in the dependency graph", with signature `fn(&PanicInfo) -> !`. The Notes of RUST.13 match both pages, and a1's quotations agree with the raw text.

**N3220, 7.23.3 paragraph 12**: "The byte output functions write characters to the stream as if by successive calls to the fputc function." 7.23.1 lists the byte output functions as including fprintf, fputc, fputs, fwrite, putc, putchar, and puts. 7.23.7.3: "If a write error occurs, the error indicator for the stream is set and fputc returns EOF." So fputs, fwrite, and fprintf set the indicator through an as-if equivalence, though their own descriptions say only "returns EOF" or "a negative value".

**Should-fix 1, detail**: the STDC.28 Notes are too narrow. They say that for these four functions the test "is not stated to receive a failure that the call itself returns", but the indicator test of the second sentence of STDC.28 receives it. Fix: cite 7.23.3 paragraph 12 and 7.23.1, say the indicator is set as if by fputc, and delete the limit. The first sentence of the Streams paragraph can say that these functions' own descriptions name only the return value. The STDC.28 text and mode stand. Earlier editions and a literal reading of "as if" stay unverified.

## Not checked

No earlier editions of C or Fortran. The TestU01 claim. Whether the custodian has ruled on ratification.
