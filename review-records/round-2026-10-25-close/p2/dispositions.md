# P2 dispositions: update to STND.CODE 1.2 interface 0.2 (2026-10-25)

Sources: `p1/code-interface.md` 0.2, `p1/for-p2-p3.md`, `research/round-addenda/a2-language-facts.md`. Rehearsal: entry 147 plus `apply_close_p2.py` (P1 0.2, then STND.PY 1.1, then STND.JL 1.2). `verify` passes every check; findings.py shows no defect on PY or JL, only g.18 notices for three modals, the new PY.34, PY.35, JL.37, JL.38 and JL.39 among them; check_refs shows 0 missing rows. Reading copies `STND.PY-0.2.md`, `STND.JL-0.2.md`; pairs regenerated (PY 57, JL 61).

| # | Item | Disposition |
| --- | --- | --- |
| 1 | Term wording (F4): "interface for outside use"; "places in its public interface" | Fixed. PY's row Public interface and JL's Terms lead now say that their functions belong to "the public interface that the term Untrusted input of STND.CODE takes in". The Notes and rationales name the documentation clause as a widening that the Notes of STND.CODE put to the custodian, and no longer say that the reach is unchanged. |
| 2 | "function" includes procedures and methods | No change needed. |
| 3 | STND.CODE.14 "in its result" | No change needed: PY.22, PY.32 and JL.15 cite the outcome. The Notes add that a raised (Python) or thrown (Julia) exception is the pass to the caller. PY.22 s1 and JL.15 s1 keep the ruled wording. They are not cut to a delta, because they are ruled language forms that name the mechanism. |
| 4 | STND.CODE.16 split; new STND.CODE.21 | PY Relaxed checks now cite STND.CODE.21 (a default) in place of the excluded option. JL Arithmetic adds that STND.CODE.21 recommends against `@fastmath` in code holding a governed check. Citations of STND.CODE.16 are of sentence 1 (CPS.5, CPS.9) only. |
| 5 | STND.CODE.19 changed; clause in JL.1 and PY.14 (cold item 5) | Applied. JL.1 s2 and PY.14 open with "Other than for a version (release) that STND.CODE.19 fixes", and refers_to gains STND.CODE.19. The Versions Notes of both say each yields by its own text. Both stay defaults; the clause narrows them. |
| 6 | a2 1a, hooks | PY Notes: "raised and not caught … just before the program exits", not "main thread"; SystemExit exempt; the threading hook for `Thread.run`; the unraisable hook of sys. The marks are removed and a2 S1, S2 cited. The PY.32 body now also reaches the hook for an exception that the interpreter is unable to raise. |
| 7 | a2 1b, 1c, optimizing mode and indexes | Cited (S3, S5, S6, S7). Negative indexes run from minus the length to minus one; slices never raise. The mark stays for array libraries and compilers. |
| 8 | a2 1d, ctypes | Signature, argument count and int-result facts cited (S8). Pointer truncation keeps its mark. The callback-exception mechanism is removed from the Notes. PY.35 states the outcome only, for "a foreign interface that does not pass a Python exception on", and its Notes say that what each interface does is unverified. The rationale never relied on it. Callback references cited (S8); buffers keep their mark. |
| 9 | a2 1e, PEP 751 | Cited as Final, file pylock.toml (S9, S10). Installer support keeps its mark. |
| 10 | a2 2a, `--check-bounds` | Cited in the JL Failures Notes (S11, S12). |
| 11 | a2 2b, `ccall` | "indeterminate results" and "no C header files" wording used (S13). `Cint` is `Int32` on every system; `Clong` and `Cwchar_t` differ. The `sizeof`/`fieldoffset` and column-major/stride facts keep their marks. |
| 12 | a2 2c, `GC.@preserve`, closure lifetime | Cited (S11, S13). That `ccall` keeps its own arguments alive keeps its mark. |
| 13 | a2 2d, `@cfunction` | Uses the manual's wording, "should not throw errors … undefined state" (S13), in place of "unwinds through frames". |
| 14 | a2 2e, `public` from Julia 1.11 | Stated in the JL Failures Notes (S14), and "an exported name is public" is marked as this standard's reading. |
| 15 | for-p2-p3 item 6, CXX Notes on JL.36 | Information only. It also resolves P2's earlier `for-p1.md` point. |
