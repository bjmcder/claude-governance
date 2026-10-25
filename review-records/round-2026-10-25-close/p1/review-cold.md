# Cold review of package P1 (STND.CODE 1.2, STND.STDC 1.1, STND.CXX 1.2)

## Verified by script
- Fresh rehearsal from `harness/`: three entries (148 to 150) appended, all eight `verify` checks PASS. One g.18 warning.
- `findings.py` on `STND\.(CODE|CXX|STDC)`: no defect class. Review-class items only: g.18 three modals on CODE.4, .13, .16, .19 and CXX.2, .4, .5, .10, .11, .19 to .22 (CODE.16 is new, CODE.19 is the CXX.30 text), and g.11 on CXX.3 (unchanged text).
- `check_refs.py`: 3 documents, 0 with missing rows.
- My own script on all changed or new provisions: one modal per sentence, at most three per provision, no banned word in a body, body IDs equal instantiates plus refers_to.
- Reading copies match the rehearsal text. Fixed tail present and exact on all three rationales; no entry of this round cited by number.
- Classes: Minor is right for all three under STND.IDENT.3 (each adds, alters or removes an obligation, and alters a defined meaning).
- Withdrawal follows STND.CLASS: files removed, the seven identifiers in `withdrawn`, no new provision reuses one. Citations of CXX.16 to .18 and .28 to .31 remain only in the Revision Histories of CODE, CXX and STDC (allowed) and in FTN, LEAN, RUST and BUILD (other packages).

## Defects

1. **CODE.16 sentence 3 binds Fortran where the custodian ratified a default, with no argument of its own (GOV.11, GOV.19, R22).**
   - STND.FTN.18 is a default (SHOULD NOT) on the same option, and its Notes say "no binding provision rests on the hazard". The ratification of 2026-10-24 gave C++ (CXX.18) and C (STDC.2) the binding form, and Fortran the default.
   - The CODE Notes argue that "the license alone makes the check removable". They also say that whether a compiler deletes the test is unverified. So sentence 3 is binding on an unverified hazard, and it is not a check "already required" as the floor sentence claims.
   - It also reaches Julia (a fast-math mode of the compiler) and any compiler of any other language.
   - The CODE rationale does not name this as a raise of FTN.18 from default to binding. It says only that the custodian decides the argument per language.
   - Fix: split sentence 3 into its own provision. Either (a) make it a default from the same onset, with CXX and STDC keeping the binding form for the languages ruled; or (b) keep it binding and state in the rationale and Notes that FTN.18 is overridden, as a decision with a recommendation.

2. **The rationale and Notes of CODE.16 understate what sentences 2 and 3 add to Python and Julia.**
   - Both say STND.CODE.16 "adds to Python and Julia only the checks of CPS.5 and CPS.9". Sentence 2 also forbids any check of untrusted input (and any CPS check) written in a form "that a definition in the source turns off". Sentence 3 reaches a fast-math mode of the Julia compiler.
   - PY.25 and JL.13 forbid only `assert`, `@assert`, `@boundscheck` and the index case. A Python `if DEBUG:` around a check, with `DEBUG` a module constant, or a Julia `const` or `@static if` flag, is newly forbidden. The Notes argue sentence 2 only for C and C++.
   - "A definition in the source" is undefined for languages without a preprocessor, so a reviewer cannot decide it. The cost "of the form of that check" is not shown for these cases.
   - Fix: state the real added reach in rationale and Notes, and narrow sentence 2 to what has a checkable meaning in every language: "a macro definition or condition of compilation in the source". Put the Python and Julia extension to the custodian.

3. **CXX.32 is wider than its stated counterpart, STND.RUST.13 sentence 2.**
   - RUST.13 sentence 2 is conditioned: "Where the work replaces the hook, or defines the handler". CXX.32 has no such condition. It binds every C++ program at every class, so a program with no handler must install one wherever the default writes none. The CXX Notes call this "the cost of one terminate handler" and also say it "asks for no work that PRIME.4 does not".
   - A handler is code, not wording or one record. The claim that the ratification "accepted this argument for RUST.13 sentence 2" holds only for the conditioned form.
   - Fix: either condition it as RUST.13 does ("Where the work sets the terminate handler, that handler SHALL deliver..."), or keep it unconditioned and say in the rationale that it exceeds the RUST.13 precedent and the custodian decides it. The Notes' "or by the default where it writes one" does not appear in the body. Add it ("a diagnosis ... SHALL reach ...") or drop it from the Notes.

## Should-fix

4. **CODE.17, .19, .20 extend a ruling that CUSTODIAN.md limits to C++.** The line "High-assurance C++ ... This ruling is for C++ only; it was not extended to C, Fortran, Rust, or Lean (2026-10-24)" is a standing direction. The provisions are defaults, so GOV.11 is not engaged. But CODE.17 sentence 1 is SHALL for CSQ0 safety-related components in every language, including Python, Julia, Lean and SystemVerilog, which have no published standard. That asks for a standard "of the work's own making" with a deviation procedure. The rationale lists no such decision. Fix: list the extension to languages with no ruling as a decision with a recommendation (keep as defaults, since a project replaces them by record), and say that STDC.1 already extended the rows to C on 2026-10-24.

5. **CODE.19 Notes decide a conflict of defaults that no body decides.** "Where a language standard asks for the newest edition, as STND.CXX.2 does, STND.CODE.19 fixes the edition ... in its place" is stated for every language. Only CXX.2 says so in its body. STND.JL.1 and STND.PY.14 (default, ruled) do not, and the interface file calls the change optional. A Note cannot order two defaults. Fix: have P2 add the "other than for an edition that STND.CODE.19 fixes" clause to JL.1 and PY.14, and limit the Note to C++ until then.

6. **CODE.16 is a bundle that can be applied apart.** Three sentences with three different reaches and three different floor arguments. g.18 asks to confirm the bundle is never applied apart, and the Notes do not. Splitting the sentences (see defects 1 and 2) resolves it. Otherwise argue it in the Notes.

7. **CODE.14 adds a requirement that none of the five ratified language provisions has.** It asks that a result carrying a passed condition be one "that the contract of the code names". PY.22, JL.15, RUST.13, FTN.29, LEAN.25 and CXX.16 say only "return the condition in its result". A function that returns an undocumented sentinel now fails, and CODE.3 is only a default. The Notes say CODE.14 "states" those first sentences, so this is a tightening presented as a restatement. Fix: drop "that the contract of the code names for it" (STDC.2 already adds the contract rule for C), or argue it in the Notes.

8. **The term Untrusted input is not exactly the union of the ratified reaches.**
   - Wider: any function the documentation or configuration names, outside what the language places. For Python, a documented underscore name or a non-library function; for FTN, an external procedure, which the interface file says is excluded today; for Rust, a function of a non-library crate; for Julia, a documented function not exported.
   - Narrower: "function". FTN ratified "each procedure ... that a module makes public" and BIND procedures, which include subroutines. A strict reading of "function" leaves out Fortran subroutines.
   - Whether the wider reading is intended is not recorded; it follows the wording of decision 4, but it was ratified only as a union with the language placements.
   - Fix: define "function" in the Terms as "function, procedure, subroutine, or method", and say in the Notes that the documentation clause widens each language by the functions that the language standard does not place. Keep the exclusion of external procedures, or record its removal.

9. **What the term newly makes binding through CODE.6.** For C and C++: an `assert` on an argument of a documented function (common in contract-style code) is newly a non-compliant check. STDC 1.0 reached only data from outside. For Lean and hardware descriptions the Notes say only "the argument is the one just given". A hardware description has no "function of the public interface" in the ratified sense (ports), and Lean functions with proved preconditions carry no run-time check. Fix: one sentence each in the CODE Notes on what is reached, or that nothing is.

10. **Notes facts unmarked.**
    - CODE and CXX Notes state flatly that a definition of NDEBUG in the source turns `assert` off. The STDC Notes mark it "unverified in c1", and c1 does not hold it. Mark it in CODE and CXX too.
    - The CXX.27 "no change" reason ("Julia and safe Rust check each index in every build") is wrong for Julia. A `--check-bounds` execution setting and `@inbounds` remove the check (julia.md; JL.13 and JL.34 assume it). RUST.20 concerns overflow checks and debug assertions, not index checks. The same sentence is in the CXX rationale. Fix: "in the default build", cite JL.13 for the index of untrusted input, and mark the Rust claim.
    - "A static check that reports every ignored result is not such a form" (CODE.15 Notes) is the drafter's reading. It narrows STDC and RUST.14, which accept such a check. It is harmless (it only lowers the reach), but say so.

## Optional
- CODE.15 narrows the condition of RUST.14 (a form of declaration, against any diagnosing compiler or static check). No floor risk. Note it for P3.
- The CODE Notes restate the term's content in the "Untrusted input" paragraph (GOV.31). Trim to the reach and the floor argument.
- CODE Notes use "any" twice; the banned list covers bodies only.
- Notes in CXX that state the reach of the high-assurance provisions as indicative ("are required for the safety-related components") are inherited; leave.
- STDC.2 keeps its identifier with a new title and a narrower body. Defensible (the errno rule is the part that survives), but say in the Revision History that no identifier is reused.
- The Rust `panic` fits CODE.14 under "halt with a diagnosis"; say so in one line, since CODE.14 does not list it as RUST.13 does.

## Floor summary by provision (GOV.11, GOV.19)
| Provision | Verdict |
| --- | --- |
| CODE.6 with the term | Not a floor raise for PY, JL, RUST, FTN as ratified. Newly binds C, C++ (item 9). |
| CODE.14 | First sentences of PY.22, JL.15, RUST.13, FTN.29, LEAN.25 plus the contract clause (item 7). Otherwise no raise. |
| CODE.15 | Conditioned on a declaration form, so asks nothing of PY, JL, FTN, LEAN, SV. Sound. |
| CODE.16 s1 | New for PY, JL, FTN, LEAN, SV, HDL (CPS checks). Argued; custodian decision, as drafted. |
| CODE.16 s2 | Defect 2. |
| CODE.16 s3 | Defect 1. |
| CODE.17, .19, .20 | Defaults; item 4. |
| CODE.18 | Language-independent, high-assurance code only; the argument holds. |
| STDC.2, STDC.39 | Sound. STDC.39 matches LEAN.27. |
| CXX.32 | Defect 3. |

## Decisions of the drafter
- 1 (term): item 8. 2 (CODE.14): item 7. 3 (CODE.15): sound. 4 (CODE.16): defects 1 and 2. 5 (CODE.18): sound. 6 (CODE.17, .19, .20): items 4 and 5. 7 (CXX.32): defect 3. 8 (CXX.27 no change): item 10; the conclusion can stand after the wording fix. 9 (STDC.2): sound. 10 (STDC.39): sound. 11 (withdrawal): correct.

## Not checked
- Primary sources (ISO text, compiler manuals): only the research notes were read, and several facts (NDEBUG, terminate default, nodiscard on result types) are unverified.
- The STND.HARN.28 pair lists beyond their headers.
- FTN, RUST, LEAN, BUILD citations of withdrawn identifiers: other packages.
- Whether P2 and P3 keep the language placements of public interfaces; item 8 depends on it.
