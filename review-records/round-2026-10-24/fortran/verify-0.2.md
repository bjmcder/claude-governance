# Verification of STND.FTN draft 0.2

**Verdict: adopt after small fixes; no blocking defect.** One factual error in the Notes (N1) and five should-fix items (N2 to N6) remain. No binding provision raises the floor, and none conflicts with another provision.

## Run
- The rehearsed copy composes to draft-0.2.md, and its pair list equals pairs-0.2.md (174).
- `verify` passes all eight checks. Its one g.18 warning does not come from STND.FTN, where every provision has at most two modals.
- `findings.py 'STND\.FTN'` is empty.
- The draft needs the BUILD round applied first. I checked its statements about STND.BUILD.2 to .4 and .11 to .13 against their text, and all are correct.

## Findings to status
| Finding | Status |
| --- | --- |
| Cold D1, D3, S4, S6 to S10, S12 to S14, O15 to O17 | Carried out. D3 has remnants (N6). S8 leaves a residual restatement (O1). |
| Cold D2 (finite-value sentence) | Carried out as default FTN.18; see N1 |
| Cold S5 (CODE.6 reach) | Carried out; see N2, N3 |
| Cold S11 (common block) | Partly; see N4 |
| Pair 1 to 13, 15 | Carried out. Items 2, 3, and 8 leave decisions to the custodian, and the Notes name them. |
| Pair 14 (Notes wording) | Partly: (a), (b), (d) done; narration of the research note remains (N4, N6) |
| Pair 16 to 21 | Carried out. FTN.33 s2 is correctly among the DSGN.3 sentences. |

## Tests of the changed sentences
- **Tighten-only and floor.**
  - FTN.29 has the form of CXX.16, PY.22, and JL.15, with no rider.
  - FTN.30 asks what CODE.7 and PRIME.4 ask, at one status test.
  - FTN.31 stays within CODE.6 and PRIME.4 except for N2. Its floor argument depends on the reach decision (N3).
- **Restatement.** None of CONC, MPI, or OMP is restated. FTN.31 repeats the CODE.6 clause "no execution setting removes", which the assumed-size case and the timing justify.
- **Untrusted input.** The Notes correctly say the ruling of 2026-10-23 was made for PY and JL; both Notes confirm it.
- **Class onset.** I checked each sentence against the instantiations and the CLASS.10 rows. The DSGN.4 group (FTN.6, 12 s1, 24, 27 s2) is complete, and the DSGN.3 and DSGN.15 groups are correct. Each NUMER.5, HW.3, or HW.5 sentence also cites a LVL0 provision. No error found.
- **New pairs.** Three: FTN.18 with CPS.5, CPS.9, and ML.6, all on DSGN.2. None conflicts. The six dropped pairs belong to deleted 0.1 FTN.4, through VV.8.

## New findings, ranked
**N1 (factual error). Notes, Floating-point paragraph.** It says "the Notes of STND.CXX state that hazard for C++ compilers (unverified)". They do not; a grep of CXX, CODE, NUMER, and CPS finds the finite-value assumption only in the text of CXX.18. Fix: delete the clause.

**N2. FTN.31 relaxes CODE.6.** "or, at the latest, before the first use" allows a check after entry, while binding CODE.6 requires it "where untrusted data enters". The Notes limit the later check to bounds known only at the use. Fix: say "at the entry, or where the bounds become known".

**N3. Untrusted input and FTN.31.** Module entities are public by default in Fortran, so "each public procedure of a module" reaches every module procedure not made PRIVATE. In PY and JL, "public" is a declared interface. The Binding paragraph argues "none raises the floor" without saying that FTN.31 depends on the reach decision. Fix: say so in the paragraph, and word the Term "each procedure that a module makes public, by attribute, statement, or default".

**N4. FTN.20 and its Notes.**
- The threadprivate part has no source. In f1 only the clause rule is quoted from S3, and item 14 admits members.
- The Notes cite "S3, as the table gives it" and narrate that f1's "answer in brief ... is the reading that FTN.20 does not follow".
- Fix: restrict FTN.20 to data-sharing clauses, or mark the directive rule unverified. Delete the narration.

**N5. FTN.36.** It says a run "halts at the first of them and reports its location". The Notes quote S1 17.6 that halting "is not precise". Fix: "reports where it halted".

**N6. Halting provisions and indicative Notes.**
- FTN.16 s1 asks every main program to halt on the three exceptions, but FTN.36 and the Notes allow code that relies on continuing. Add the guard "Where the code does not rely on continuing past them".
- FTN.17 s2 steers halting code to quiet comparisons, so a NaN can reach a branch silently. State the case it is meant for.
- Notes remnants: "so the repository configuration names the compilers as well as the revision", "review decides the forms ...", and "which the note does not quote". These are indicative duties or narration.

**Optional**
- O1: FTN.2 s1 names a subset of the settings that BUILD.11 already has stated.
- O2: FTN.12 s2 excepts submodules, which neither f1 nor the Notes support.
- O3: FTN.31 and FTN.35 add substrings, which f1 does not cover.
- O4: FTN.16 s2 sends "a negative answer" to FTN.29, which applies only to a condition PRIME.4 lists.

## Not checked
I did not read the Fortran, MPI, or OpenMP texts, or STND.DRAFT in full. I relied on the brief, the harness checks, and f1's own marks.
