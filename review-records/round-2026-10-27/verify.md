# Verification of the round of 2026-10-27

## Verified by running

- `rehearse` of `apply_round_2026_10_27.py`: entries 188 to 197, every check PASS, the one g.18 warning, source unchanged. On a kept copy: `verify`, `references --check`, `manifests --check` pass. The warning list gains only STND.CODE.24 and loses STND.CXX.20, .22, STND.PY.35, STND.JL.39.
- Applied the eight modules one at a time and searched the text after each step for every identifier withdrawn so far, outside revision rows and `withdrawn`: no state cites one. The claim of `draft-status.md` on the order holds.
- The same search on the final copy: no citation of STND.CXX.20, .22, STND.STDC.36, STND.PY.33, .34, .36, .37, STND.JL.4, .37, .40, .41; no "foreign function interface"; Foreign interface is defined once (STND.CODE), Lock file once (STND.DEPS); neither clashes with a term of `LEX/` (Resource, Contract, Component, Interface boundary, read for Finding 2).
- Pairs per document, filtered to the 15 changed provisions: 131 rows, identical to `pairs-changed.md`. Banned body words: none in the 14 changed or new provisions. Reading copies contain every changed provision and Note line.
- Every row of `dispositions.md` checked on the copy. All hold, except O2 (Defect 1).

## Defect

1. **The fix for B-O2 is still ungrammatical.** STND.PY Notes, Versions: "as a requirements file does that pins the exact revision of each package that the environment installs, its transitive dependencies included." Replace with: "as a requirements file that pins the exact revision of each package that the environment installs, its transitive dependencies included, does."

## Should-fix

2. **"Resource" in STND.CODE.25 is the Lexicon's term in another sense.** LEX.resource is "compute time, energy, memory, silicon area, money, or human attention". STND.CXX and STND.STDC avoid the clash with the term Owned resource; STND.CODE.25 and STND.RUST.27 do not. Replace the two sentences of STND.CODE.25 with: "Each memory, file, lock, handle, or other facility that code acquires and has to release, and that crosses a foreign interface, SHOULD have one owner that the contract of the interface states, and be released only by that owner, through the function and the allocator that the contract names for it (DSGN.14). Each such facility that a foreign interface creates for the work SHOULD pass to an object of the work that owns it and releases it, before each other operation that is able to fail (DSGN.14)." Follow with "foreign resource" in STND.RUST.27 and the Notes, or, if the custodian prefers a term, define Owned resource once in STND.CODE and have STND.CXX import it.
3. **Rationale 195 is cryptic and hides a narrowing.** "with the word only added to the release by the owner". Replace with: "with the release limited to the owner that the contract states (first sentence of STND.CODE.25), where STND.RUST.27 let the side and allocator that the contract names release".
4. **Rationale 197 and the Notes of STND.CXX do not say what the term-clause loses.** STND.CXX.4, .6, .8, and .10 use "foreign interface"; the old term of STND.CXX included the structured block, and the term of STND.CODE reaches it for STND.CODE.24 alone. Add to rationale 197: "A structured block of a parallel directive is no longer a foreign interface for STND.CXX.4, STND.CXX.6, STND.CXX.8, or STND.CXX.10, which did not use it."

## Optional

5. **Term "For STND.CODE.24 alone".** A term with a meaning that varies by provision is unusual, and every language standard imports it with "has the meaning". Alternative with one meaning: delete the third sentence of the term; in STND.CODE.24 write "each failure raised in code of the work that the interface invokes, or in a structured block of a compiler directive for parallel execution, and propagated by ..." and "stored in an object ... after the invocation or the block returns". Then Notes "The structured block ... is a foreign interface for STND.CODE.24 alone" becomes "STND.CODE.24 also reaches the structured block of a parallel directive". Custodian's choice.
6. **STND.CODE.24 names a language construct.** "an exception or a panic among them" while Purpose says "No provision names a language, tool, or method (GOV.18)". Replace with "an exception among them", as STND.CODE.14 does; the Notes keep the panic.
7. **"Same process" for a hardware description.** An instance of a block in another description language is not a foreign interface under the term; the Notes say STND.CODE.22 to .26 apply to a hardware description. Replace the Notes sentence ending "for each foreign interface that it declares" with "... for each foreign interface that it declares, a simulator interface among them".
8. **STND.FTN and STND.LEAN name no constructs of the term**, though the Notes say each language standard does. Accept, or add one clause to each Terms: "a procedure with the BIND attribute is a foreign interface" (FTN).
9. **Notes of STND.CODE:** "The declaration of a foreign function in its own language, and the documentation of the interface, are parts of its contract" fixes a meaning in an informative part, and decidability of STND.CODE.22, .23, and .25 rests on it. Consider adding it to the term Foreign interface: "The contract of a foreign interface includes the declaration of the function in its own language and the documentation of the interface."

## Questions for the custodian

`dispositions.md` omits these drafting choices; each narrows, widens, or leaves open:

1. The structured block belongs to the term for STND.CODE.24 alone (Finding 5).
2. STND.RUST Terms read an unwinding ABI as a statement of the contract that a panic is carried on, so STND.RUST.25 does not narrow.
3. STND.PY.34 asked a declaration of each type in the source; STND.CODE.22 asks the representation, the declaration being left to the Notes.
4. For Rust, STND.DEPS.12 no longer asks a committed lock file for builds that produce no reported result (decision 3, but a narrowing of the first sentence of STND.RUST.30, stated only in rationales 189 and 195).
5. STND.RUST.27 widens to each resource under STND.CODE.25.
6. STND.CODE.22 to .24 reach C++ layouts, C, Fortran, Lean, and hardware descriptions from CSQ2.

Questions 1 to 5 of `dispositions.md` are stated fairly.
