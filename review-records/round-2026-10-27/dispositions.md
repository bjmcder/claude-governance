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

## Verification (`verify.md`) and reconciliation (`reconciliation.md`)

Rehearsal after these fixes: entries 188 to 197; `verify` and `references --check` pass, with the g.18 warning that the corpus already carries; the drafting findings on the changed provisions are unchanged. Both reviews applied the modules one at a time and found no state of the round that cites a withdrawn identifier.

| # | Finding | Disposition |
| --- | --- | --- |
| V1 | The fix of B O2 is still ungrammatical | Fixed: "as a requirements file that pins the exact revision of each package that the environment installs, its transitive dependencies included, does." |
| V2, R1 | "Resource" in STND.CODE.25 and STND.RUST.27 is LEX.resource in another sense | Fixed by the reconciler's form: STND.CODE defines Owned resource, in the words of the term of STND.CXX, and STND.CODE.25 and STND.RUST.27 use it; STND.CXX drops its definition, and STND.CXX, STND.STDC, STND.PY, and STND.RUST import it from STND.CODE. |
| V3 | The rationale of STND.RUST hides a narrowing ("the word only") | Fixed: "with the release limited to the owner that the contract states, where STND.RUST.27 let the side and the allocator that the contract names release it". |
| V4 | The rationale of STND.CXX does not say that the block leaves the term for STND.CXX.4, .6, .8, .10 | Fixed, in the rationale. |
| V5, R O3 | Move the structured block from the term into the text of STND.CODE.24 | Not taken; question 6 below. The reconciler judges the clause sound as a term. Written into STND.CODE.24, the block has no interface for its second and third sentences to test, so the clause would move into the provision with its two readings. |
| V6 | "a panic" names a construct of a language | Not taken: GOV.18 and the Purpose of STND.CODE exclude a language, a tool, or a method, and a panic, like an exception, is a kind of failure that several languages have. |
| V7 | "Same process" and hardware descriptions | Not taken: a simulator that loads code of another language into its process is reached; an instance of a block in another description language is not a call between languages of different rules. |
| V8 | STND.FTN and STND.LEAN name no constructs | Not taken: the Notes of STND.CODE no longer say that each standard names them; STND.FTN.27 names the BIND attribute. |
| V9 | What the contract includes rests on a Note | Fixed: the term Foreign interface says "The contract of a foreign interface includes the declaration of each of its functions in its own language and the documentation of the interface", and the Note is removed. |
| R2 | The rationale of STND.CXX says that STND.CXX.5 keeps its outcome, though a resource handle is no longer asked | Fixed: the rationale states the narrowing; question 7 below. |
| R3 | The rationale of STND.RUST says that STND.JL and STND.PY cite STND.RUST.24 to .27 | Fixed: STND.JL cites STND.RUST.27 until its own amendment, which follows STND.RUST's because STND.RUST drops its citation of STND.JL.4; `draft-status.md` likewise. |
| R4 | The rationale of STND.CODE omits that a call to another process leaves the term | Fixed, in the rationale; question 8 below. |
| R5 | STND.CODE.22 and .25 are bundles whose first sentence applies alone | Not changed: the Notes argue each second sentence as never applied without the first, the form of the ratified STND.PY.34 and STND.JL.37; question 1 below. |
| R O2 | The scripts fix the date 2026-10-27 | Noted: `fi_common.DATE` is changed before application if ratification falls on another day. |
| R O4 | The ban on releasing a predefined resource survives only as a Note | Not changed: the first sentence of STND.CODE.25 has each owned resource released only by its owner, and the Note names the interface as the owner of what it predefines. |

## Questions for the custodian

The drafting made these choices beyond the decisions; the reviews name them. Each concerns a default, and none raises the floor.

1. **Five provisions, not one.** Decision 26 of 2026-10-25 named one STND.CODE provision; STND.DRAFT.28 allows at most three sentences, never applied apart, so the rules are STND.CODE.22 to .26. The second sentences of STND.CODE.22 and .25 apply to fewer cases than their first, and are argued as never applied without them.
2. **STND.CODE.24 relaxes STND.CXX.22 and STND.JL.39.** A failure that the contract of the interface carries on to code of the work is left uncaught, as STND.PY.35 and STND.RUST.25 already allowed. The alternative is a catch in every case, which would tighten STND.PY.35 and STND.RUST.25.
3. **STND.CODE.25 adds the pass of a foreign resource to its owner before each other operation that is able to fail** for Python and Julia and the languages newly reached, as STND.CXX.20 and STND.RUST.27 asked.
4. **STND.DEPS.12 has no permission sentence** for a package that other work uses and that produces no reported result; the condition of the provision already leaves it out, and the Notes say so. A sentence "... MAY keep its lock file out of version control" can be added. For Rust this narrows the first sentence of STND.RUST.30, as decision 3 asks.
5. **STND.RUST.27 is kept**, cut to the release in a `Drop` implementation, and now reaches each owned resource that the work owns under STND.CODE.25, not only one that a foreign interface creates. The alternative, its withdrawal, needs a second amendment of STND.RUST in this round, after STND.JL.
6. **The structured block of a parallel directive** is a foreign interface for STND.CODE.24 alone, by a clause of the term, which keeps the one use that STND.CXX and STND.STDC made of it. The alternatives: a foreign interface for all five rules, or named in the text of STND.CODE.24.
7. **A C++ owner of a foreign resource** was a resource handle under STND.CXX.20, with its copy and move operations defined or deleted; STND.CODE.25 asks an object that owns it and releases it, and STND.CXX.5 its release in the destructor. Accept the narrowing, or keep the resource handle in STND.CXX.
8. **A call to code in another process** leaves the term Foreign interface, which the words "code written in another language" of STND.PY, STND.JL, and STND.STDC reached.
9. **The reading of an unwinding ABI in STND.RUST.** The Terms of STND.RUST read a declaration with an ABI under which both sides admit unwinding as the statement of the contract that STND.CODE.24 asks, so that STND.RUST.25 keeps its alternative to the catch.
10. **The declared types of STND.PY.34.** STND.CODE.22 asks the representation that the contract fixes, and the Notes of STND.PY give the declaration of each type as the means where an interface checks no call; the declaration is no longer asked in the body.
11. **The reach.** Under decision 4, STND.CODE.22 to .24 apply from CSQ2 to C++ layouts and to C, Fortran, Lean, and hardware descriptions, and STND.CODE.25 and .26 from CSQ3.
12. **Ratification.** After one more cold verification of these fixes, if it finds no defect.
