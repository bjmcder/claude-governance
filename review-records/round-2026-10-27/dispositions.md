# Dispositions of the reviews of the round of 2026-10-27

Reviews: `review-a.md` (STND.CODE, STND.DEPS, STND.STDC, STND.CXX, and the editorial amendments) and `review-b.md` (STND.PY, STND.RUST, STND.JL), by agents of another configuration. Rehearsal after the fixes: entries 188 to 197; `verify` passes with the g.18 warning that the corpus already carries; `references --check` passes; the drafting findings on the changed provisions are the g.18 review notices of STND.CODE.24, argued in the Notes as one remedy, and of STND.CXX.5, unchanged by the round. The reading copies and `pairs/` are regenerated; the pairs are unchanged.

## Review A

| # | Finding | Disposition |
| --- | --- | --- |
| S1 | The structured block of a parallel directive in the term makes STND.CODE.22, .23, .25, and .26 reach every parallel region, where no contract fixes a layout or an owner | Fixed. The term lists three constructs as foreign interfaces, and adds: "For STND.CODE.24 alone, a structured block of a compiler directive for parallel execution is also a foreign interface, which carries no error and whose invocation returns at the end of the block." This keeps the reach that the terms of STND.CXX and STND.STDC gave the block, which only STND.CXX.22 used, and gives the third sentence of STND.CODE.24 its referent (Optional 9). The Notes of STND.CODE and the rationales of STND.STDC, STND.CXX, and STND.RUST say so. |
| S2 | The term reaches calls between processes | Fixed: "code in the same process". The rationale of STND.CXX records it. |
| S3 | The Notes call the sentences of STND.CODE.22 and .25 one rule, though their second sentences apply to fewer cases | Fixed, in the reviewer's form: each second sentence "is not applied without the first". A predefined resource has the interface as its owner (Optional 7). |
| S4 | The rationales understate what C gains | Fixed in the rationales of STND.CODE and STND.STDC: the alignment, the compared layouts, the element type and the strides, and arrays of one dimension; the arrays of STND.CODE.23 in C++ and Rust. |
| S5 | The Purpose of STND.STDC does not name STND.CODE.22 to .26 | Fixed, as STND.CXX does. |
| S6 | An indicative obligation, and STND.LEAN cited for foreign-interface content it does not hold | Fixed: "STND.CODE.22 to STND.CODE.26 apply to the C, Fortran, and Lean source of the work, and to a hardware description, for each foreign interface that it declares, beside what STND.FTN.27 and STND.FTN.28 state." |
| O7 | The ban of STND.CXX.20 on releasing a predefined resource | Fixed in the Notes, with S3. |
| O8 | STND.PY.34 asked a declaration of each type | Taken with B S3. |
| O9 | "after the invocation returns" for a structured block | Fixed with S1. |
| O10 | The import clause of STND.CXX names constructs | Not taken: each language standard names its constructs, as decision 1 has it. |

## Review B

| # | Finding | Disposition |
| --- | --- | --- |
| D1 | The class onset paragraph of STND.RUST still lists STND.RUST.24, .25, and .30 among the provisions of three modals | Fixed, in the reviewer's wording; the revision row and the rationale record it. |
| D2 | STND.RUST.25 narrows: an unwinding ABI no longer takes the place of the catch unless the contract states it | Fixed without the narrowing, so that the question to the custodian is moot: the Terms of STND.RUST read "the declaration of a function of the work with an ABI under which both sides of a foreign interface admit unwinding is a statement of the contract of that interface that it carries a panic on to code of the work, in the sense of STND.CODE.24". The rationale says so. |
| S1 | Retitles not recorded | Fixed in the rows of STND.PY, STND.JL, and STND.RUST. |
| S2 | STND.RUST.27 widened to each resource that the work owns under STND.CODE.25 | Recorded in the rationale. |
| S3 | STND.CODE.22 asks the representation, not a declaration of each type | Recorded in the rationale of STND.PY; the Notes of STND.PY give the declaration as the means where an interface checks no call. |
| O1 | The count of pairs | Fixed: 131. |
| O2 | "as a requirements file is that pins" | Fixed: "does that pins". |

## Questions for the custodian

The drafting made these choices beyond the decisions, and both reviews name them. Each is a default, and none raises the floor.

1. **Five provisions, not one.** Decision 26 of 2026-10-25 named one STND.CODE provision; STND.DRAFT.28 allows at most three sentences, never applied apart, so the rules are STND.CODE.22 to .26.
2. **STND.CODE.24 relaxes STND.CXX.22 and STND.JL.39.** A failure that the contract of the interface carries on to code of the work is left uncaught, as STND.PY.35 and STND.RUST.25 already allowed. The alternative is a catch in every case, which would tighten STND.PY.35 and STND.RUST.25.
3. **STND.CODE.25 adds, for Python and Julia and for the languages newly reached, the pass of a foreign resource to its owner before each other operation that is able to fail**, which STND.CXX.20 and STND.RUST.27 asked.
4. **STND.DEPS.12 has no permission sentence** for a package that other work uses and that produces no reported result. Decision 3 states that such a package may leave its lock file uncommitted; the condition of the provision already leaves it out, and the Notes say so. A sentence "... MAY keep its lock file out of version control" can be added if the custodian wants it stated in the body.
5. **STND.RUST.27 is kept**, cut to the release in a `Drop` implementation, which no order of single transactions could otherwise reach without a state that cites a withdrawn identifier.
