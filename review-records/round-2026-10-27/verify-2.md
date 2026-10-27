# Second cold verification of the fixes, round of 2026-10-27

## What I ran

- Kept a rehearsed copy (`/tmp/claude-1000/verify2-2026-10-27/c`): entries 188 to 197; `verify` passes with the existing g.18 warning; `references --check` passes.
- Applied the eight modules one at a time (`/tmp/claude-1000/verify2-2026-10-27/step.py`), ran `verify` after each, and listed the Terms rows of Foreign interface, Owned resource, Lock file, and Foreign function interface. `verify` passes at every step, so no check rejects a state. Final state: each term is defined once (STND.CODE, STND.CODE, STND.DEPS). Intermediate states define Foreign interface up to five times and Owned resource twice (STND.CXX until entry 197), which is the transient order of the round and rejected by no check.
- `findings.py` on the copy: the changed provisions give only the g.18 notices of STND.CODE.24 and STND.CXX.5. Read rationales 188 and 193 to 197 and the Terms and Notes of the five standards.
- Dispositions V1 to V4, V9, R2 to R4: V1, V2/R1, V3, V4, V9, R3, R4 hold in the text; R2 in part (Should-fix 2); V8 not (Should-fix 3).

## Defect

None.

## Should-fix

1. **Stale "foreign resource" after the term Owned resource.** STND.CXX.5, second sentence: "or of an object that owns a foreign resource under STND.CODE.25". Replace with "or of an object that owns an owned resource under STND.CODE.25". Likewise in the STND.CXX Notes ("owns a foreign resource"; "puts a resource that a foreign function returns") and the STND.RUST Notes ("owns a foreign resource releases it"). "Foreign resource" is defined nowhere. The title "Foreign resources released in Drop" of STND.RUST.27 no longer matches its text; retitle "Owned resources released in Drop" (six words or fewer) in the title, row 1.2, and rationale 195.
2. **Rationale 197 still contradicts itself.** "the resource handle of the work being that object" stands beside "no longer asks it to be a resource handle". Replace the first with "an object of the work that owns it being that object". Also "the release of no resource that the interface predefines" becomes "the release of no owned resource that the interface predefines".
3. **Disposition V8 is not true of the Notes.** STND.CODE Notes: "the language standards import them, the term Foreign interface each naming the constructs of its language that are foreign interfaces". STND.STDC, STND.FTN, and STND.LEAN name none. Replace with "the language standards that use them import them, and those with constructs of their own name the constructs of their language that are foreign interfaces".
4. **Broken list in the Terms of STND.RUST.** "...; Owned resource has the meaning that STND.CODE gives it; and the declaration of a function of the work with an ABI ... in the sense of STND.CODE.24; Dependency record and Lock file ..." The "and" closes a list that continues. Replace "; and the declaration of" with "; the declaration of".

## Optional

5. STND.RUST.27, "owns an owned resource under STND.CODE.25": replace with "holds an owned resource that STND.CODE.25 reaches".

## Questions for the custodian: complete and fair?

Each of the twelve is stated fairly. Missing:

- **A.** STND.CODE now defines Owned resource for every language, taken from STND.CXX; STND.CXX, STND.STDC, STND.PY, and STND.RUST import it (V2/R1). This is a drafting choice beyond decisions 1 to 4 and is not asked. Add: "Owned resource moves from STND.CXX to STND.CODE, in the same words. The alternative is the word facility in STND.CODE.25 and a Resource-free STND.CXX."
- **B.** Question 12 is a process step, not a question.
