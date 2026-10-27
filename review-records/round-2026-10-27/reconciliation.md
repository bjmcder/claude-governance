# Reconciliation of the round of 2026-10-27

## Verified by running

- Rehearsal exits 0 (entries 188 to 197, source unchanged). `verify` and `references --check` pass on a kept copy; the one warning is the existing g.18 warning. `findings.py` lists only STND.CODE.24 and STND.CXX.5 (three modals, review notices).
- I applied the eight modules one at a time and grepped after each. No state cites a withdrawn identifier (STND.CXX.20, .22; STDC.36; PY.33, .34, .36, .37; JL.4, .37, .40, .41). In the final state none remains outside revision rows and the field `withdrawn`. No "foreign function interface" remains outside STND.RUST's own revision row.
- Foreign interface (STND.CODE) and Lock file (STND.DEPS) are each defined in one Terms row. The Lexicon has no such term. The STND.CXX.8 table row "Foreign interface" is a reason, not a definition.
- A regex over fourteen new or cut provisions found no banned word and no more than three modals. Onsets agree with STND.CLASS.10 (DSGN.4 and DSGN.5 rows at CSQ2; DSGN.14 and REPRO.1 have none).
- I read every withdrawn provision against the text after the round. Every outcome stands, with the narrowings listed below. I checked each row of `dispositions.md` against the copy, and all are in the text.

## Defect

None.

## Should-fix

1. **"Resource" in STND.CODE.25 is the Lexicon term in another sense.** LEX.resource is "Compute time, energy, memory, silicon area, money, or human attention". STND.CXX avoids this with its own term Owned resource, and the language-neutral rule dropped that word. Add to the STND.CODE Terms: "| Owned resource | Memory, a file, a lock, a handle that a foreign interface issues, or another facility that code acquires and has to release. |". Read "owned resource" in both sentences of STND.CODE.25 and in STND.RUST.27 ("owns an owned resource under STND.CODE.25"). STND.CXX and STND.STDC then import the term from STND.CODE and drop their rows or their pointer to STND.CXX.

2. **Rationale 197 says what the text does not do.** Text at fault: "STND.CXX.5 changes its citation and not its outcome" and "the resource handle of the work being that object". STND.CXX.20 required a resource handle (copy and move operations defined or deleted). STND.CODE.25 asks "an object of the work that owns it and releases it", and STND.CXX.5 now lets an owning raw pointer sit in any "object that owns a foreign resource". Replacement: "STND.CXX.5 changes its citation, and C++ code no longer needs a resource handle, with its copy and move operations, for a foreign resource: any object that owns it and releases it meets STND.CODE.25, and STND.CXX.5 admits an owning raw pointer in such an object." Or restore the outcome with "only inside the implementation of a resource handle" in STND.CXX.5 (see the question).

3. **Rationale 195 is untrue after the round.** Text at fault: "each of the four keeps Rust content, and STND.JL and STND.PY cite them". Neither cites STND.RUST.24 to .27 after the round; their transactions drop those citations. The true reason is the order of transactions (draft-status). Replacement: "each of the four keeps Rust content."

4. **Rationale 188 omits a narrowing.** The terms of STND.PY, STND.JL, and STND.STDC reached "code written in another language" with no limit. The new term says "in the same process", so a call to another process in another language is no longer a foreign interface. Only the rationale of STND.CXX says so. Add to "They ask this less": "; in Python, Julia, and C, a call to code in another process, which the earlier terms reached as code written in another language."

5. **STND.CODE.22 and .25 are bundles whose first sentence applies alone** (a type with no declared layout; a resource that the interface does not create). STND.DRAFT.28 asks parts "never applied apart"; the Notes now say only that the second "is not applied without the first". Replacement for the Notes: "The second sentence of STND.CODE.22 is the check that makes the first decidable for a layout that the work declares, and is applied with it. The second sentence of STND.CODE.25 names the owner on the side of the work for a resource that the interface creates, and is applied with the first." The ratified STND.PY.34 and STND.JL.37 had the same shape, so the custodian may accept it as it stands.

## Optional

6. STND.PY Notes: "as a requirements file does that pins the exact revision" becomes "as does a requirements file that pins the exact revision of each package that the environment installs, its transitive dependencies included."
7. The scripts fix `DATE = "2026-10-27"` (`fi_common.py`), which feeds the rows, the `adopted` fields, and "ratified by the custodian on 2026-10-27". Change it if ratification falls on another day.
8. Terms. "For STND.CODE.24 alone" is sound as meaning: it is scoped, it feeds the referent of "after the invocation returns", and importers cannot misapply it. Its cost is that STND.CODE.24 cannot be read without the Terms row. Terms elsewhere name provisions, but none restricts a term to one. Moving "or in a structured block of a compiler directive for parallel execution" into the first sentence of STND.CODE.24 would do without it.
9. The prohibition of STND.CXX.20 on releasing a predefined resource survives only as a Note ("has the interface as its owner"). STND.CODE.25's first sentence reaches it when the contract names the owner.

## Checked and sound

- STND.CODE.22 to .26 agree with CODE.7, .12, and .14 (the stored failure is answered by STND.CODE.14), with STND.CONC.5 (STND.CODE.26 is the stricter), and with STND.FTN.27 and .28, STND.CXX.5 and .21, and STND.RUST.24 to .27 and .30. STND.PY.35 and STND.JL.39 ("stored in place of its conversion") override the conversion of STND.CODE.24 explicitly.
- The clause of STND.RUST on an unwinding ABI adds to the contract statement and does not contradict the term. STND.DEPS.12 agrees with STND.DEPS.10 and with the Notes of STND.PY, STND.JL, and STND.RUST.
- No new text restates a held provision. The language Notes that name STND.DEPS.12 describe it without adding to it.
- The ledger form "ratified by the custodian on ..." is the standing form (entries 150 and 176). It is applied only after ratification, and nothing writes a ruling that has not been made.

## Questions for the custodian

1. Dispositions' Review A S1 settled a question that Reviewer A put to you: is a structured block of a parallel directive a foreign interface for STND.CODE.24 alone (as drafted), or for all five rules, or named in the text of STND.CODE.24? It is not on the list of questions, and it should be.
2. Should a C++ owner of a foreign resource be a resource handle (the outcome of STND.CXX.20) or any owning object (as drafted)? (Should-fix 2.)
3. Do you accept that a call between processes leaves the term? (Should-fix 4.)
4. The five listed questions are complete otherwise, and each is stated fairly. Question 5 should add the alternative: amend STND.RUST twice (1.2 and 1.3), the first to drop the citation of STND.JL.4, the second to withdraw STND.RUST.27.
