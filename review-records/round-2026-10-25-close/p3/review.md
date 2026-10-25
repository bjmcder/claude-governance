# Cold review and STND.HARN.28 pair review of package P3 (2026-10-25)

Scratch files: /tmp/claude-1000/review-p3/.

## Verified by script
- Fresh `rehearse governance apply_close_p3.py`: 7 entries, seq 148 to 154. `verify` passes all checks; the one warning is the carried g.18 notice. `findings.py` on RUST, FTN, SV, LEAN: no defect, only 11 carried three-modal review notices (none on a new or changed text). `check_refs`: 0 of 4 documents with missing rows.
- Obligations: I diffed every provision of the live corpus (entry 147) against the rehearsal copy. RUST.13, .14, .15, FTN.18, .29, .31, LEAN.25 differ only by a `refers_to` entry and a citation inside the closing parenthesis. RUST.34, FTN.30, LEAN.5 are byte-identical. Mode, binding_reason, instantiates, and modals are unchanged. No binding provision changes its obligation.
- LEAN.27 differs in text (S1). RUST.35, FTN.37, SV.28 are defaults on INTPR.1 and INTPR.4, on no row of STND.CLASS.10, so CSQ3; their text is STDC.39 with the language word changed.
- Withdrawn identifiers: no citation of STND.CXX.16, .17, .28 to .31 in any provision or Notes of the four documents. They appear only in the history rows that record the retargeting. STND.CXX.18 in the FTN Notes is kept and valid.
- Rationales: all 7 end with the fixed tail once; no entry of this round cited by number.
- Drafting rules on new text: one modal per sentence; titles of 3 to 5 words, distinct.
- New Notes facts: the Rust case lints match a2 fact 5, including the narrowing to static items and "Rust project publishes a convention" left unverified. RUST Notes list a2 as a source. No other new fact needs a source (see O3).

## Judgments asked for
- **Classes (STND.IDENT.3).** RUST 1.1, FTN 1.1, SV 1.1: minor is right (add a default; for RUST and FTN the defined meaning of the term changes). LEAN 1.0.1 editorial holds for LEAN.25 (citation only) and the Notes edits, but not clearly for LEAN.27 (S1).
- **Placement of Untrusted input.** Held. RUST Terms place "each function of the public interface of a crate of library code" and FTN Terms place module-public and BIND procedures, which is the 1.0 placement.
- **Widening (documented functions outside Rust library code; documented Fortran external procedures). The floor argument holds.** The only binding text that gains reach is RUST.15 and FTN.31. Each asks the form of a check that code already makes: RUST.15 sentence 1 and FTN.31 are the forms of STND.CODE.6, which at entry 147 already reaches untrusted input in every language through DSGN.2 and PRIME.4. RUST.15 sentence 2 is conditioned on code that rejects untrusted input and asks an overflow-reporting form. The carve-out for a source that the threat model records as trusted stays. Caveats: the argument rests on the CODE term and CODE.6, so it is one decision with P1's; and the reach is new, so the rationale must not call it ratified (S2). Recommend: accept.
- **Naming rule (R18).** RUST.35, FTN.37, SV.28 are the LEAN.27/STDC.39 form with the NUMER.4 allowance, and add no table. That matches decision 9. The note on Rust is honest but thin (O2).
- **The "six decisions".** dispositions.md numbers twelve items and marks only item 7 as a decision. I took the six that need the custodian: FTN external reach (agree); Rust reach outside library code (agree); FTN.18 kept beneath CODE.21 (O1); RUST.14 kept as the "wider" form (S3); naming rule in RUST, FTN, SV (agree); LEAN.27 editorial (S1).

## Findings

### Defect
None.

### Should-fix
**S1. LEAN.27 as editorial.** "Each name of the Lean source" becomes "Each name that the Lean source of the work declares". A name that the source uses without declaring (a library name, an opened namespace) leaves the SHOULD. STND.IDENT.3 makes a change that alters an obligation minor, and the rationale's argument ("same names as before") is a reading, not a proof. Fix, either one: (a) revert the LEAN.27 text edit and the matching clause in the rationale and the history row, which keeps 1.0.1 editorial and loses only wording parity; or (b) class the amendment as LEAN 1.1 minor, with the rationale saying that the SHOULD narrows to declared names. I recommend (a): decision 9 asks for the LEAN.27 form, and LEAN.27 is already that form.

**S2. Rationale overclaims a ruling (RUST 151 and FTN 152).** Both say the reach of CODE is "the one reach that the ratification of 2026-10-24 gave the term in every language". Decision 4 of decisions-final.md ratified RUST.15 (library crate) and FTN.31 (module-public) "as drafted", not the documentation-named reach. The same sentence then says the reach is new outside library code, so the text contradicts itself. This breaks "never write that the custodian has ruled something the custodian has not ruled". Fix: replace the clause with "the reach that STND.CODE 1.2 gives the term in every language" and drop "that the ratification of 2026-10-24 gave". The Notes already put the new part to the custodian correctly.

**S3. RUST Notes on RUST.14 against CODE.15 contradict themselves.** The Notes call RUST.14 "kept as ratified, with its wider condition" and then say "the two ask one outcome". CODE.15 applies wherever the language provides a declaration form, and Rust does, so CODE.15 binds Rust unconditionally while RUST.14's condition (the means include a diagnosing check) is the narrower. "Wider" is wrong or at least unproved. Fix: say "RUST.14 is kept as ratified. Rust provides a form of declaration, so STND.CODE.15 applies to Rust code on its own terms, and RUST.14 states its Rust form", and drop "wider".

### Optional
**O1. FTN.18 against CODE.21.** FTN.18 now restates the first sentence of CODE.21 (GOV.31), kept only because the lead directed it. Its added value is the per-source-file wording. Fix: say so in one Notes sentence, or recommend retiring FTN.18 at the next FTN amendment. The custodian decides.

**O2. RUST naming note.** Rust is the one language here whose case convention is checkable (a2 fact 5), so decision 9 would allow a Rust table. The Notes give no reason for leaving it to the configuration. Fix: add "the lints warn by default and STND.BUILD.12 fails a change on a warning, so the configuration names the convention at no added cost; a fixed table adds nothing". Also "STND.BUILD.12 fails a change" is indicative for a default; write "asks that a change fail".

**O3. FTN and SV Notes, "The research note holds no convention of names...".** This is a negative about the research, not about the language. Fix: use the corpus's own form, "The research note retrieved no convention of names that the language definition fixes", and mark it unverified.

**O4. SV Purpose** says "in every build"; CODE.16 says "execution setting". Fix: use that.

**O5. FTN.29 and a status argument.** CODE.14 admits "its result or a mechanism of its language"; a status argument is a convention. The Notes cover it. Cross-package: P1 could add "or in an argument that the caller passes to receive it".

## Pair review
- Coverage by script: regenerated the pair lists on the fresh rehearsal for RUST (268), FTN (175), SV (942), LEAN (1046); each equals the delivered pairs-STND.<ID>.md. Filtering the changed and new provisions (RUST.13, 14, 15, 35; FTN.18, 29, 31, 37; SV.28; LEAN.25, 27) gives 31 pairs, equal as a set to pairs-changed.md, no repeat, none missing. I covered each once.
- Result by group, with no conflict and no unowned matter found:
  - RUST.13, .14, .15, FTN.29, .31, LEAN.25 against HDES.14, HW.8, HW.GPU.3 (PRIME.4), 18 pairs: response lists agree or nest; a returned fault leaves the response to the path as a whole, as HW.8 reads.
  - RUST.15, FTN.31, FTN.18 against CPS.5, CPS.9, ML.6 (DSGN.2), 9 pairs: they keep the required check from removal; consistent.
  - RUST.35, FTN.37, SV.28, LEAN.27 against NUMER.4 (INTPR.1), 4 pairs: the MAY keeps a symbol's case; consistent.
- Read without pairs: RUST.35, FTN.37, SV.28 match STDC.39 in form; CODE holds no naming provision; no existing RUST, FTN, or SV provision fixes names (grep); SV.28's "verification set" is defined in SV. No conflict.

## Could not check
Primary sources behind a2 (I read a2, not the pages). The Rust, Fortran, and Verilog statements that no convention is fixed by the language definition. `compose --check` and the rendering of the reading copies. The reading copies <ID>-0.2.md were not compared byte for byte to the rehearsal (I compared the rehearsal files to the live corpus). The baseline was the live corpus at entry 147, not `git diff HEAD~3`.
