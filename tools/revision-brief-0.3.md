# Revision brief for draft 0.3 (CXX, PY, JL)

Same role, permissions, and drafting rules as `drafting-brief.md` and `revision-brief-0.2.md`. You may read (not write) the other two languages' `verify-0.2.md` and content modules to align shared rules.

## Shared decisions (apply as written)

1. **One PRIME.4 response list per standard.** The provision that states the response (PY.23, JL.15; CXX where it has one) allows: raise or throw an exception; halt with a diagnosis; enter the designed safe state (PRIME.13), where the code commands physical hardware; degrade visibly with a diagnosis; or return the condition in its result. In Python, a warning counts only if its category is one the default warnings filters show. Every other provision that needs a response refers to that provision instead of listing its own.
2. **Out-of-memory handlers (PY.29, JL.14).** "Where a handler catches [MemoryError | OutOfMemoryError] by naming it, a class from which it derives, or no class, it SHALL respond as STND.<X>.<n> requires (PRIME.4)." PY adds: "A suppression context SHALL NOT name MemoryError or a class from which it derives (PRIME.4)." PY may name RecursionError beside MemoryError, as JL names StackOverflowError.
3. **PY.32** becomes the single sentence: "Where code suppresses a warning or an error report that signals a condition that PRIME.4 lists, it SHALL detect each such condition by another means and respond to it as STND.PY.<response provision> requires (PRIME.4)." Scoping of settings stays in PY.31.
4. **Exact comparison.** PY.21 and JL.21 carry the same MAY: "A comparison of exact values, or one that the bitwise tier of STND.VVUQ.1 admits, MAY use the equality operators (VV.3)." No Notes sentence restates it as an obligation.
5. **Random streams.** Library code derives per-part streams from "a spawning, jump-ahead, or counter-based facility of its generator library" and the index of the part (PY.19, JL.24, VVUQ.62).
6. **Performance approximations.** Classifying an option as a performance approximation (NUMER.16, NUMER.17) is stated in the Notes, never as a SHOULD in a body (PY.33 sentence 2; JL already does this).
7. **Custodian judgments.** The Notes never say a judgment is "recorded here" before ratification. List each such judgment (PY.5 floor; the shared "Untrusted input" scope reaching every public function at CSQ4) in your decisions list instead; the Notes state the rule and its reason.
8. **Notes hygiene.** No obligations, no drafting narration ("the research read", "were not run when this standard was drafted"), no unsourced facts. Mark a fact "unverified" only where the research note does not mark it [S]. Facts that a verifier offered "from recollection" go in only if the research note supports them; otherwise mark them unverified or omit.
9. **Size.** Take the merges your verifier lists as losing nothing. Target about 30 provisions.
10. **Ledger.** Final order: DOCS 100 (12:00), INSTR 1.4 101 (12:05), CXX 102 (12:10), PY 103 (12:20), JL 104 (12:30). Use your AT time. The rationale cites no ledger entry numbers, and every provision number and count in it matches 0.3.

## Rehearsal

Fresh copy of `/home/claude/harness/governance` to `/home/claude/scratch-<lang>/governance` (replace the old copy), then `import apply8; apply8.apply(root)` (DOCS 0.4 and INSTR 1.4; `apply7` is superseded), then yours. Run `verify` and `findings.py`. Regenerate `draft.md`.

## Deliverable

Write `/home/claude/scratch-<lang>/dispositions-0.2.md`: one row per verify-0.2 finding with Fixed / Declined (reason). Final message under 500 words: paths, verify result, remaining findings, and the numbered decisions list for the custodian (changes since 0.2 marked).
