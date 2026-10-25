# Reconciliation review A: alignment across documents (closing round of 2026-10-25)

Reviewer A. Scope: terms, no restatement (GOV.31), same question and same answer, the sibling list, citations of withdrawn identifiers, References. Method: rehearsed `apply_round_2026_10_25_close.py` (28 entries, seq 148 to 175, copy `/tmp/rehearsal-6epy_xmt/governance`), composed the amended documents, diffed them against `rendered/`, and checked terms, identifiers, and citations by script.

## What holds

- **Rehearsal checks.** `verify` passes; `findings.py` shows 242 review-class items and no defect; `check_refs.py` reports 48 documents checked, 0 with missing rows.
- **Withdrawn identifiers.** STND.CXX.16, .17, .28 to .31 occur in the rehearsed corpus only in the revision-history rows and the front-matter list of withdrawn identifiers. Every other provision identifier cited in the 16 amended divided documents exists.
- **Terms.**
  - Untrusted input, High-assurance code, and High-assurance coding standard are each defined once, in STND.CODE. The old rows in CXX, STDC, PY, JL, RUST, and FTN are gone, and each document imports the term.
  - Panic (RUST) and Language edition (SV) are byte-identical to the live corpus. Edition in force (CXX) is unchanged.
  - The membership clauses of PY, JL, RUST, and FTN match the per-language list in the CODE Notes.
- **Naming (R18).** LEAN.27, STDC.39, RUST.35, FTN.37, and SV.28 have the same two-sentence form. The CXX.14 and JL.6 tables stay, PY.1 keeps its form, and no C table was added.
- **Foreign interfaces.** PY.34 to .37, JL.37 to .41, RUST.24 to .27, CXX.20 to .22, and STDC.36 agree in mode (default) and in onset (CSQ2 for DSGN.4 and DSGN.5, CSQ3 for DSGN.14).

## Sibling list (definition of done, item 1)

| Item | Status |
| --- | --- |
| Unchecked index, JL.13 against PY.25 | Reasoned no change (PY Notes, Assertions; P2 decision 2). |
| Checks in shipped builds, CXX.27 against JL.34 | Amended: new JL.36. P1 decision 9 still says "no change" (see S9). |
| Counterpart of RUST.13 s2 in CXX and PY | Amended: CXX.32, CXX.33, PY.32. |
| Logging as the only visible degradation | No change, by decision 7 of 2026-10-24 (P2 decision 5). |
| Committed lock file for PY | Amended: PY.33. |
| Foreign interfaces in PY and JL | Amended: PY.34 to .37, JL.37 to .41. |
| `#define NDEBUG` in C source | Amended: CODE.16 s2. |

All seven are resolved. The three "no change" resolutions are in the dispositions, not yet in one decision list (Reviewer C compiles it).

## Blocking

**B1. STND.FTN.18 restates STND.CODE.21 (sentence 1).**
- Both are defaults with the same outcome. P3 decision 3 and the FTN Notes say FTN.18 "adds no other outcome". GOV.31 removes a profile provision that restates a higher one without domain-specific content, and the body names no Fortran construct. Definition of done, item 4 ("no restatement") is not met.
- Fix: withdraw STND.FTN.18 in FTN 1.1 under the STND.CLASS convention, list it in the front matter, and retarget the Purpose range ("STND.FTN.13 to STND.FTN.18"), the Notes (Floating-point exceptions; Class onset) and the history row to STND.CODE.21.
- Alternative: the custodian records the exception at ratification. P3 recommends "keep now, retire later", which leaves the breach.

**B2. STND.RUST.14 restates STND.CODE.15, and the two texts disagree on the relation.**
- RUST.14 names no Rust construct. Its trigger (the means include a compiler or check that diagnoses an ignored value) differs from CODE.15 (the language, a compiler, or a check provides a form of declaration).
- CODE.15 Notes say that reading "lowers the reach that STND.RUST.14 ... gave" and that RUST.14 "keeps its own form". The RUST Notes say CODE.15 "applies to Rust code on its own terms" and RUST.14 "states its Rust form".
- Rust provides `must_use`, so CODE.15 applies without condition. A project whose only means is a blanket check meets RUST.14 and fails CODE.15, and both are binding.
- P1 asked P3 either to cut RUST.14 to its delta or to say so in the Notes. P3 did the latter, and the two Notes still contradict each other.
- Fix: cut RUST.14 to cite CODE.15, or give it Rust content (the `must_use` attribute on the function or on its result type) and reword the CODE.15 Notes to match. The custodian decides, because RUST.14 is a ratified binding provision.

## Should-fix

**S1. CODE Notes lag the round.**
- (a) The Responses paragraph names "STND.RUST.13 and STND.CXX" for a panic hook and a terminate handler, and the later list repeats "the panic hook of STND.RUST.13 ... the terminate handler that STND.CXX governs". Both omit the Python hook (STND.PY.32). The IDs do not exist at entry 148, so say "the hook of STND.PY" in words, or add the IDs in a later editorial.
- (b) The Finite values paragraph says STND.CXX.18 is the form "which STND.STDC applies to C in its C reading". STND.STDC.40 now states it in its own words.
- (c) The CXX Notes say "STND.JL.34 and STND.RUST.20 have no counterpart of STND.CXX.27" and then give the Julia default in words. JL.36 is that counterpart, so say so.

**S2. STND.CXX Purpose omits STND.CXX.33.** Add it to the failures list (it is in the Notes and the history row).

**S3. PY and JL cite "a2" without saying what it is.**
- PY has four citations and JL three, with no sources sentence. CXX, STDC, RUST, and FTN each define their keys.
- PY and JL Notes also use "high-assurance code" and "high-assurance coding standard" (Versions) without importing the terms in Terms. CXX, STDC, and SV import them.
- Fix: one sentence in each Notes, and the import.

**S4. Lock files are not aligned.**
- "Lock file" is a term in PY and in RUST with different wording. JL uses "manifest file" with no term. Define it once (STND.DEPS or STND.CODE) or cite one definition.
- RUST.30 has no "where the work reports results" condition, and it adds a third sentence (build from the locked revisions; fail on mismatch). PY.33 and JL.4 carry the condition and no third sentence.
- The PY Notes say PY.33 keeps the file under version control "wherever the work reports results, as STND.JL.4 does ... and STND.RUST.30 for a Rust lock file". That misdescribes RUST.30. State the difference in the PY and RUST Notes.

**S5. Shared foreign-interface rules are stated per language.**
- The callback rule is in four standards (CXX.22, RUST.25, PY.35, JL.39). The "one owner" rule is in four (CXX.20, RUST.27, PY.36, JL.40). The array and layout rules are in three or four. Each carries language content (KeyboardInterrupt, ABI, `@cfunction`), so GOV.31 is not broken.
- The language-neutral outcome is the very thing R17 moved to STND.CODE for other rules. "Foreign interface" is also defined five times (CXX, STDC, PY, JL, and RUST as "Foreign function interface").
- P2 recommends one STND.CODE provision in a later round. Record that as a custodian decision, not only a P2 note.

**S6. Language response provisions repeat the CODE.14 list.**
- PY.22 s1, JL.15 s1, RUST.13 s1, FTN.29, and LEAN.25 each restate "halt with a diagnosis, enter the designed safe state, degrade visibly, or return" and add a mechanism.
- Several omit CODE.14's "in an argument that the caller passes to receive it". They are narrower than CODE.14, and all are binding. Their sentences are ruled or ratified, so any cut needs the custodian. Cutting each to a citation plus its delta is a later round.

**S7. STND.STDC.40 restates STND.CXX.18 by design** ("in the words of", so a later change of CXX.18 does not change C). Record this as a decision. STND.BUILD 1.0.2 says CXX.18 "binds for C++" and omits C (two places in the Notes). Add STND.STDC.40 or "C and C++".

**S8. Two gaps in same question, same answer.**
- Checks in shipped builds: FTN gives no reason for having no counterpart of CXX.27 or JL.36. FTN.35 covers tests only. RUST.20 and PY are reasoned.
- STND.FTN.26 ("SHOULD NOT rely on the order of records") is a form of STND.CONC.30, as the MPI and OMP amendments now say for their models. CONC.30 allows a protocol that fixes the order. FTN.26 neither cites it nor allows it. Add a citation and the clause.

**S9. Terminate handlers and hooks.**
- JL, C, FTN, LEAN, and SV have no counterpart. The only reason (no Julia hook source) is in P2 decision 9, in no standard.
- State once in the CODE Notes that a language with no replaceable hook or handler has no counterpart.
- Records: P1 decision 9 ("CXX.27 against JL.34: no change") now contradicts P2 decision 3 (new JL.36).

**S10. OFFLD.31 against PERF.12.** The OFFLD Notes say the second sentences of PERF.12 and PERF.14 "hold the same outcomes". PERF.12 lists "the first filling of caches and memory" among the costs of first use, and OFFLD.31 does not. This is P4 decision 2. Either widen OFFLD.31 or soften the Notes.

**S11. Optional.**
- JL Terms narrow the imported term with an index carve-out (`eachindex`, `axes`, `CartesianIndices`). The carve-out holds in every language, so it is better placed in STND.CODE, or stated as Julia-only.
- RUST says nothing of how CODE.19's "edition" relates to a Rust edition or toolchain release. CXX, JL, and PY say they yield.
- The "reach of the ruling is kept" paragraph is repeated in five standards' Notes. The CODE Notes could hold it once.

## Not checked

The correctness of the floor arguments, the class onsets, and the rulings attributed to the custodian (Reviewer B). Rationale tails, history rows, and revision numbers (Reviewer C). The a1 and a2 facts were taken as stated.
