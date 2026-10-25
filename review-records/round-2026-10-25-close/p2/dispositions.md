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

## Review of P2 (review.md), dispositions (2026-10-25)

Rehearsal after the fixes: entry 147 plus `apply_close_p2.py` (P1 0.2 first). `verify` passes all checks. findings.py shows no defect on PY or JL. Its review notices are g.18 only; the new provisions among them are PY.35 and JL.39, each argued in one Notes sentence. check_refs shows 0 missing rows. Reading copies `STND.PY-0.3.md` and `STND.JL-0.3.md`; pairs regenerated (PY 62, JL 66; PY.36, JL.38 and JL.40 rest on DSGN.14 alone and have none).

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | PY.32 floor argument misstates the unraisable case | Fixed. The exception "ends a thread or the program or is dropped". The argument now rests on the last sentence of PRIME.4: a replaced hook that drops a listed condition lets the program end or continue past the error in silence. The Notes state the conditioning: the default hooks print, so PY.32 binds only where the work replaces one. Rationale aligned. |
| S2 | Widening narrated in the Notes | Fixed. PY and JL Notes now read "the reach of the ruling is kept; STND.CODE adds the functions that the documentation or the repository configuration names for use outside the work". The widening, through the ruled PY.25 and JL.13, goes to the custodian as decision 1 below, with its fallback; the rationales record both. |
| S3 | PY.35 rests on an unverified fact | Fixed. The condition is now "Unless the documentation of a foreign interface states that the interface passes a Python exception on", which holds whatever the interface does. The unmarked claim about the C interface of extension modules is removed; the Notes say that what each interface does is unverified. |
| S4 | JL.38 exception rests on an unverified fact | Fixed. The `ccall` exception is dropped. JL.38 now reaches each pointer that the work takes by `pointer` or a like function, which a2 S13 shows needs `GC.@preserve`. The unverified sentence on `ccall` arguments is removed. |
| S5 | JL.39 against JL.16 | Fixed. JL.39 stores an `InterruptException` and throws it again after the foreign call returns, "as STND.JL.16 asks in place of a throw within the callback". refers_to gains STND.JL.16. PY.35 takes the same carve-out for KeyboardInterrupt and SystemExit, with STND.PY.28 in refers_to. |
| S6 | Unmarked facts | Fixed. PY: the extension-module and loader sentences are marked; the finalizer example is removed. JL: the `@fastmath` assumption is marked unverified; "dependencies included" is removed; "each index in every session" is now "under the default setting … emits bounds checks other than inside `@inbounds`" (a2, S12), with array types of packages marked. |
| S7 | Three-modal bundles | Split. PY.34 keeps types and the layout test; new PY.37 holds the arrays. JL.37 keeps types and layout; JL.38 keeps pointers and closures; new JL.40 holds ownership and new JL.41 the arrays. PY.35 and JL.39 keep three sentences, each argued in its Notes as one remedy, since an exception that is caught and neither converted nor stored is discarded (STND.CODE.7). |
| S8 | Contiguity and strides unknowable from a C declaration | Fixed. PY.37 and JL.41 take them from "the documentation of the foreign function", or from "a test of that call", as FTN.28 does. |
| S9 | Notes claim more than the provisions | Fixed. PY.36 and new JL.40 now ask for "one owner that the contract of the interface states", as RUST.27 does. "Stated alike" now reads "take the same steps". |
| O1 | Pinned requirements file | Taken. The PY Notes say that a requirements file pinning each exact revision, transitive dependencies included, is a lock file in the sense of the Term. |
| O2 | asyncio exception handler | Not taken. No source in the repository. |
| O3 | Record the "no change" resolutions | Taken: decisions 2, 5 and 9 below. |

Also fixed: two g.12 findings (a condition after the clause) and two g.16 defects (PRIME.4 named in text only) that the rewording of PY.35 and JL.39 produced first.

## Decisions for the custodian, as they now stand

1. **Untrusted input from STND.CODE.** The reach of the 2026-10-23 ruling is kept. STND.CODE adds the functions that the documentation or the repository configuration names, and that addition reaches the ruled PY.25 and JL.13. *Recommend accepting.* Fallback if declined: delete the documentation clause from the STND.CODE term; PY and JL then hold unchanged.
2. **JL.13 sentence 3 against PY.25: no change.** Built-in sequences raise IndexError in every mode (a2). Whether array libraries do the same is unverified. *Recommend no change.*
3. **JL.36, a default from CSQ1 matching CXX.27.** *Recommend.*
4. **PY.32 binding.** Its floor argument rests on PRIME.4's last sentence (R22). *Recommend binding.*
5. **Logging as the only visible degradation: no change,** by decision 7 of 2026-10-24.
6. **PY.33 lock files, a default.** *Recommend.*
7. **Foreign interfaces: defaults.** PY.34 to PY.37 and JL.37 to JL.41, from CSQ2 for DSGN.4 and DSGN.5 and from CSQ3 for DSGN.14. *Recommend.* The callback steps now appear in four standards; *recommend one STND.CODE provision in a later round.*
8. **The CODE citations, and the CODE.19 clause in PY.14 and JL.1.** *Recommend accepting.*
9. **No JL counterpart of RUST.13 sentence 2.** The sibling item names only CXX and PY, and the repository holds no source for a Julia hook. *Recommend no change.*

## Update to P1 0.3 (2026-10-25)

STND.CODE.14 now names an argument that the caller passes to receive the condition. The PY Notes (Assertions) and the JL Notes (Failures) now give its whole clause: "in its result, in an argument that the caller passes to receive it, or by a mechanism of the language, an exception among them, that propagates the condition to the caller". The bodies of PY.22, PY.32 and JL.15 cite STND.CODE.14 by outcome and are unchanged. Rehearsal on P1 0.3: `verify` passes, no defect on PY or JL, check_refs shows 0 missing rows. Reading copies `STND.PY-0.4.md` and `STND.JL-0.4.md`. The pairs are unchanged, since no provision changed. The decisions are unchanged.

## Reconciliation review (A, B, C), dispositions (2026-10-25)

Rehearsal: entry 147 plus `apply_close_p2.py` (P1 0.3 first). `verify` passes, findings.py shows no defect on PY or JL, and check_refs shows 0 missing rows. Reading copies `STND.PY-0.5.md` and `STND.JL-0.5.md`. The pairs are regenerated: PY 62; JL 74, with the eight new pairs of STND.JL.3 (CPS.3, HDES.3, HDES.6, HW.7, HW.CPU.3, HW.EMBED.5, ML.3, ML.7). Each concerns a hardware design, a record, or a test of the delivered arithmetic. The clause only narrows a check that blocks no change, so each pair is compatible.

| # | Item | Disposition |
| --- | --- | --- |
| A S3 | "a2" undefined | Fixed. The first paragraph of the PY and JL Notes names `research/round-addenda/a2-language-facts.md` (a2 below) and its source keys (PY S1 to S10, JL S11 to S14), in the form that STND.RUST uses for a1. |
| A S3 | High-assurance terms | Fixed. PY and JL Terms import High-assurance code and High-assurance coding standard from STND.CODE. |
| A S4, B 6 | PY.33 presupposes a lock file | Fixed. It now opens "Where the tools of the work write a lock file for an environment that produces reported results", and the Notes say that it asks for no lock file where the tools write none. |
| A S4 | "as RUST.30 does" | Fixed. The Notes now state the difference: RUST.30 has no condition on reported results, and it adds builds from the locked revisions that fail on a mismatch. The ledger row and the rationale say so too. |
| A S4 | Lock file defined twice | The PY term now has the wording of the term of STND.RUST, with "an environment" in place of "a set of crates built together", and the Notes give the reason. One shared definition, in STND.DEPS for example, is a later-round item for the lead to put to the custodian. |
| B 7 | JL.3 sentence 3 | Fixed. It opens "Other than for code whose version of Julia STND.CODE.19 fixes", and refers_to gains STND.CODE.19; the Versions Notes say that JL.1 and JL.3 yield. RUST.1 sentence 3 belongs to P3. |
| C S4, A | CXX.27 against JL.34: one resolution | Stated. CXX.27 stays unchanged, and JL.36 is added as its Julia counterpart, in the JL Notes (Checking), the ledger row, and the rationale. Decision 3 below is the one resolution; P1's "no change" refers to the text of CXX.27 alone. |
| A S5 | Foreign-interface rules per language | Recorded as decision 10. |

## Decisions for the custodian, as they now stand

1. **Untrusted input from STND.CODE.** The reach of the ruling is kept. STND.CODE adds the documented functions, which also reach the ruled PY.25 and JL.13. *Recommend accepting.* Fallback: delete the documentation clause from the CODE term.
2. **JL.13 sentence 3 against PY.25: no change.** *Recommend.*
3. **Checks in shipped builds:** CXX.27 unchanged, and JL.36 added as its counterpart, a default from CSQ1. *Recommend.*
4. **PY.32 binding (R22).** *Recommend.*
5. **Logging as the only visible degradation: no change,** by decision 7 of 2026-10-24.
6. **PY.33, a default,** conditioned on a lock file that the tools write. *Recommend.*
7. **Foreign interfaces: defaults.** PY.34 to PY.37 and JL.37 to JL.41. *Recommend.*
8. **The CODE citations, and the CODE.19 clauses** in PY.14, JL.1 and JL.3 sentence 3. *Recommend accepting.*
9. **No JL counterpart of RUST.13 sentence 2.** *Recommend no change.*
10. **Later round:** one STND.CODE provision for the language-neutral foreign-interface outcomes (callback exceptions, one owner, array layout), one definition of Foreign interface, now defined five times, and one definition of Lock file. *Recommend scheduling it.*
