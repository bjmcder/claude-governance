# Round d of 2026-10-28: decisions

Round d carries ruling D1 and the restatement cleanups of the code and systems standards: register entries R6.2 and R6.3, the part of R7.1 that concerns revision numbers in Notes (CS15), and CL21 as far as it is not about onset. The module is `tools/amendment-scripts/apply_round_d_2026_10_28.py`, with the helpers `round_d_code.py`, `round_d_systems.py`, and `round_d_langs.py`. Nothing here is in force until the custodian ratifies it and the scripts run.

## Transactions

There are fifteen transactions, one per document, in citation order. Each document drops its citations of a provision before the document that holds that provision withdraws it. No state of the round cites a withdrawn identifier or a provision not yet added.

| # | Document | Revision | Class | What |
| --- | --- | --- | --- | --- |
| 0 | STND.CODE | 1.3 → 1.4 | Minor | .14 second sentence; .21 binding; new .27 to .35; Terms Library code; Purpose; Notes |
| 1 | STND.BUILD | 1.0.2 → 1.0.3 | Editorial | Notes: STND.CODE.21 forbids, and STND.CXX.18 and STND.STDC.40 state the same |
| 2 | STND.DEPS | 1.1 → 1.2 | Minor | New .13 (builds at locked revisions); Notes on .13 and on STND.DFLT.11 |
| 3 | STND.CONC | 1.1 → 1.1.1 | Editorial | Notes cite STND.CONC and STND.CODE.29 in place of the MPI, PY, and JL copies |
| 4 | STND.PERF | 1.0.1 → 1.1 | Minor | .12 reaches offloaded work; .18 aligned with MEAS.7 |
| 5 | STND.OFFLD | 1.1 → 1.2 | Minor | .31 keeps its first sentence; .27 serves as STND.CONC.24 for device code |
| 6 | STND.MPI | 1.0.2 → 1.1 | Minor | .18, .19, and .24 withdrawn; Purpose names STND.CONC |
| 7 | STND.OMP | 1.0.3 → 1.0.4 | Editorial | Revision numbers leave the Notes |
| 8 | STND.FTN | 1.1.1 → 1.2 | Minor | .29 and .37 withdrawn; .16 and .30 cite STND.CODE.14; revision numbers leave the Notes |
| 9 | STND.LEAN | 1.0.1 → 1.1 | Minor | .25 withdrawn |
| 10 | STND.CXX | 1.3 → 1.4 | Minor | .32 withdrawn; .1, .14, .21, and .25 reduced or reworded |
| 11 | STND.STDC | 1.2 → 1.3 | Minor | .29 and .38 reduced; row of .1; revision numbers leave the Notes |
| 12 | STND.JL | 1.3 → 1.4 | Minor | .21, .23, .24, and .26 withdrawn; .6, .14, .15, and .31 reduced or recited |
| 13 | STND.PY | 1.2 → 1.3 | Minor | .16, .17, .19, .20, and .32 withdrawn; .1, .2, .10, .11, .12, .22, .27, and .30 changed; Terms |
| 14 | STND.RUST | 1.2 → 1.3 | Minor | .13, .30, and .35 withdrawn; .34 binds STND.CODE.34 for Rust; .11 and .31 changed |

STND.CODE and STND.DEPS come first, because the language standards cite their new provisions. STND.BUILD follows STND.CODE at once, so that its Notes describe STND.CODE.21 as binding from the state in which it binds. STND.PERF comes before STND.OFFLD, so that no state leaves the costs of first use of offloaded work unstated. STND.CONC drops its citations of STND.MPI.18, .19, and .24, STND.PY.17, and STND.JL.24 before STND.MPI, STND.PY, and STND.JL withdraw them. STND.FTN drops STND.PY.20 and STND.JL.21 before STND.PY and STND.JL run. STND.CXX and STND.PY drop STND.RUST.13 and STND.RUST.30 before STND.RUST runs last. MEAS is unchanged: STND.PERF.18 is aligned to it.

## Decisions

### 1. Finite values (D1; CL3, in part)

Ruling D1 holds that the finite-value option binds only for checks that the floor requires (PRIME.4), and that elsewhere it is a default, alike in every language. STND.CODE.21 already reached only the checks that STND.CODE.6 or STND.CODE.16 governs. Those are the check of untrusted input and the checks of CPS.5 and CPS.9, so every check it reaches is one that the floor requires. Its first sentence, on the setting, now binds in every language:

> STND.CODE.21 (binding; PRIME.4, DSGN.2), *Finite-value settings near checks*: "Code that holds a check of a floating-point value that STND.CODE.6 or STND.CODE.16 governs SHALL NOT be compiled under an execution setting that, by the documentation of its compiler, lets the compiler assume that floating-point values are finite (PRIME.4, DSGN.2)."

Its former second sentence, on an annotation in the source, is not a compiler option. It becomes the default STND.CODE.27, *Finite-value annotations near checks*, with its text unchanged.

Floor (GOV.11): the rule costs one choice of compiler option for code that holds a check that the floor already requires. It asks for no new check. This is the argument that the custodian ruled for C++ on 2026-10-23 and that the ratification of 2026-10-24 applied to C.

**For the custodian at ratification (1a).** "Elsewhere it is a default" could mean either of two things:
- the annotation, which is not a compiler option (my reading); or
- a new default for checks of floating-point values that the floor does not require.

The second reading would extend the rule to every check of a contract. I recommend the first, which adds no reach.

**For round e (1b).** STND.CXX.18 and STND.STDC.40 now restate STND.CODE.21 for C++ and for C. They stay because the Notes of STND.BUILD cite them. Round d corrects those Notes in an editorial transaction of STND.BUILD 1.0.3, right after STND.CODE (decision 20). Round e can then drop STND.BUILD's citations and withdraw the two.

### 2. STND.CODE.14 carries each language's forms (D1; CL4)

The withdrawals and reductions:
- STND.FTN.29 and STND.LEAN.25 are withdrawn.
- STND.PY.22 keeps only the categories of warnings that the default filters show.
- STND.JL.15 keeps only the levels `Warn` and `Error`.
- STND.RUST.13 is withdrawn whole: its first sentence restated STND.CODE.14, and decisions 5 and 8 move its second and third sentences.

The forms of each language go in the Notes of STND.CODE, under "Responses". A provision of STND.CODE names no language (its Purpose, GOV.18), so the drafting rules allow the forms only there. The Notes list:
- the raised exception and the returned result of Python and Julia;
- the returned result and the panic of Rust;
- the exception, the value, and the argument of C++;
- the value and the argument of C, without errno alone (STND.STDC.2);
- the result of a function and the status argument of Fortran;
- the result type and the monad error of Lean;
- the status at the interface of a hardware description.

These provisions now cite STND.CODE.14 in place of the withdrawn or reduced language provision: STND.FTN.16, STND.FTN.30, STND.JL.14, STND.PY.27, STND.PY.30, and STND.RUST.11. Each binding one asks the same response as before.

### 3. One provision on names (D1; CL5)

The brief calls this CL6. In `corpus-code.md` it is CL5.

> STND.CODE.28 (default; INTPR.1, INTPR.4), *Names under a stated convention*: "Each name that the source of the work declares SHOULD follow the convention of names that the standard of its language gives (INTPR.1). Where the standard of its language gives none, each such name SHOULD follow the convention that the repository configuration names (INTPR.1). Under each convention that this provision or the standard of a language asks a name to follow, a name that the notation documented under NUMER.4 fixes MAY keep the case and the form of its symbol, as STND.DOCS.12 permits (INTPR.4)."

STND.RUST.35 and STND.FTN.37 are withdrawn. STND.PY.1, STND.JL.6, and STND.CXX.14 drop their sentence on names from the notation of NUMER.4, because the third sentence of STND.CODE.28 now holds it under each convention.

STND.DOCS.12 alone does not give that permission for identifiers, so the permission stays as a sentence of STND.CODE.28 and is not dropped. The words "under each convention that … the standard of a language asks" make it prevail over the tables of STND.CXX.14 and STND.JL.6, so the restrictive reading of GOV.9 cannot cancel it.

**For round e (3a).** STND.STDC.39 and STND.LEAN.27 stay, because the Notes of STND.SV cite them. STND.SV.28 repeats the same text. Round e should withdraw all three after STND.SV's Notes cite STND.CODE.28.

### 4. Generators and unstable values (CL6)

Register entry R6.2 confirms CL6. Two new defaults:
- STND.CODE.29, *Seeded random generators*, holds the text of STND.PY.16 and STND.PY.17 for every language.
- STND.CODE.30, *Hash values outside results*, generalizes STND.PY.19 and STND.JL.26 to any hash function or collection whose documentation leaves its values or order free to change between runs or releases.

STND.PY.16, .17, and .19 and STND.JL.23, .24, and .26 are withdrawn. STND.PY.15 and STND.JL.22 keep the language construct, the parameter that carries the generator. The Notes name the Python and Julia hashes and collections as examples.

The text of STND.CODE.30 as drafted:

> "Where the documentation of a hash function leaves the values that it returns free to change between runs or between releases, each output, each record of data, and each test reference of the work SHOULD exclude those values (REPRO.3, REPRO.6). Where the documentation of a collection leaves its order of iteration free to change between runs or between releases, each reported result on whose path the collection lies SHOULD be independent of that order (REPRO.3)."

**For the custodian (4a).** The reach is new for C, C++, Rust, Fortran, and Lean. A hash map whose order is left unspecified, as some standard libraries leave it, is now reached. I recommend accepting this: it is the "one provision per outcome, for every language" of D1, and the provision is a default from CSQ3.

### 5. A library log record is never the only visible sign (D1; CL23)

> STND.CODE.14, added second sentence: "A record that library code writes to a log SHALL NOT be the only visible degradation (PRIME.4)."

The Terms of STND.CODE define Library code. In a language whose standard defines the term (Python, Julia, Rust), it reads as that standard defines it. The second sentence of STND.PY.22 and the third of STND.RUST.13 had this text, so the outcome is unchanged for Python and Rust.

For Julia, this replaces the reading of 2026-10-23 that a library record at `Warn` counts, which was CL23's custodian question. D1 answers that question. STND.JL.15 keeps the levels for records that code other than library code writes.

Floor (GOV.11): the sentence asks for no response beyond PRIME.4. It only keeps out a form that may stay unseen.

### 6. Builds at locked revisions (CL8, checked; holds)

> STND.DEPS.13 (default; REPRO.1), *Builds at locked revisions*: "Other than a check that the standard of its language asks to run at revisions other than those that the lock file records, each build of the checks and of each release of the work whose lock file is under version control SHOULD use the revisions that the lock file records, and fail on a lock file that does not match the files that declare its packages (REPRO.1)."

STND.RUST.30 is withdrawn. The exception covers each check that a language standard runs off the lock file: the oldest declared releases of STND.PY.14 and of STND.RUST.1, and the newer revisions of STND.RUST.1 and STND.JL.3 (review finding 1).

**For the custodian (6a).** STND.LEAN.1 stays unchanged, against CL8's proposal to reduce it. It also pins the Lean toolchain and the checkers, and it reaches every Lean work, where STND.DEPS.12 keeps a lock file only for an environment that produces reported results. Reducing it would narrow it for proof work. I recommend keeping STND.LEAN.1 and accepting its overlap with STND.DEPS.13 for Lean packages.

### 7. Restated checks: tolerances, static checks, doctests, warnings (CL18, checked, holds; CL17)

- STND.CODE.31, *Tolerances stated at comparisons*, has the text of STND.PY.20, with "the equality operators of its language". STND.PY.20 and STND.JL.21 are withdrawn.
- STND.CODE.32, *Language provisions in static checks*: "The static checks that the repository configuration names under STND.CODE.4 SHOULD decide each provision of the standard of each language of the work whose compliance a static check among the means of the work is able to decide (DSGN.3)." The reach is what STND.PY.2 and STND.RUST.31 held for their own standards, and does not include the provisions of STND.CODE (review finding 2). The second sentences of STND.PY.2 and STND.RUST.31 are dropped. STND.CODE.4 already has three modals, so this could not be a sentence of STND.CODE.4.
- The second sentences of STND.PY.12 and STND.JL.31 are dropped. Each restated STND.DOCS.13's comparison within a stated tolerance, and the Notes keep the forms in each language.
- CL17: the second sentence of STND.CXX.25 is dropped, because STND.BUILD.12 holds it. The Notes of STND.CXX and STND.STDC say so.

**For the custodian (7a).** STND.CODE.32 reaches the checks "among the means of the work". STND.RUST.31 reached each provision that "a static check of Rust source is able to decide". That is a narrowing for Rust; I recommend it, since a tool that the work does not have blocks no work.

**For the custodian (7b).** STND.CODE.31 rests on NUMER.11 and VV.3. It is added to the list of exceptions in the class paragraph of STND.CODE, with its onset (CSQ3) in the Notes. STND.CODE.34 and STND.CODE.35 are added in the same way. STND.CODE.21 leaves that list of defaults, and the paragraph says that it binds at every class (review finding 3). This is the only edit to an onset paragraph that is not a correction for a withdrawn identifier. It keeps that paragraph true until round o replaces it.

### 8. Installed handlers (CL25, checked; holds) and claims of undefined behavior (CL10, checked; holds)

> STND.CODE.33 (binding; PRIME.4), *Diagnoses from installed failure handlers*: "Where the work replaces or installs a hook or a handler that its language or runtime runs on a failure that a mechanism of the language propagates, or is unable to propagate, that hook or handler SHALL deliver to the operator, or to the record of the run, a diagnosis of each condition that PRIME.4 lists, that such a failure carries to it, and that no other response of STND.CODE.14 answers (PRIME.4, STND.CODE.14)."

STND.CODE.33 covers:
- the exception hooks of STND.PY.32, including the unraisable hook;
- the terminate handler of STND.CXX.32;
- the panic hook and the panic handler of STND.RUST.13 (second sentence).

STND.PY.32 and STND.CXX.32 are withdrawn. STND.CXX.33 (default) stays, as C++ content. Floor: the argument that the ratification of 2026-10-24 accepted for the Rust panic hook.

> STND.CODE.34 (default; INTPR.10, VV.1), *Claims of absent undefined behavior*: "Each claim, in a report, in the record of a result or of a release, or in a review, that code of the work is free of undefined behavior or of a kind of it, or that no use of an interface of the work is able to cause undefined behavior, SHOULD state each means by which that was checked and the code, the code of dependencies included, that each means covered (INTPR.10, VV.1). Such a claim SHOULD NOT extend beyond the code and the executions that those means covered (INTPR.10, VV.1)."

> STND.RUST.34 (binding; PRIME.2), *Claims of soundness*, reworded: "Each claim that STND.CODE.34 governs and that concerns Rust code of the work SHALL meet STND.CODE.34 (PRIME.2)."

Each language keeps the strength it had:
- Rust stays bound, through STND.RUST.34, in one sentence that cites STND.CODE.34 and does not restate it.
- C keeps a default from CSQ2: STND.CODE.34 rests on INTPR.10, as STND.STDC.38 did. STND.STDC.38 keeps only whether the documentation of each means states that means as sound, and the Notes of STND.STDC read the record of a verification as a record of a result under STND.CODE.34 (review finding 9).
- The other languages had no such rule. They gain a default from CSQ2, the "one provision per outcome, for every language" of D1.

No language changes mode, so no floor is raised (GOV.11). This replaces the earlier draft, which made STND.CODE.34 binding in every language (review finding 7; coordinator's guidance).

STND.CODE.33 also reaches C: a handler that C work installs for the signal that `abort` raises is reached where that signal carries a listed condition. The Notes say so (review finding 4), and the floor argument already covers it.

### 9. Failure results of dependencies (CL13, checked; holds)

> STND.CODE.35 (default; DSGN.5), *Dependency failure results diagnosed*: "Where the language, or a compiler or a static check among the means of the work, provides a form of declaration of STND.CODE.15, each function of a dependency that reports in its result a failure of a kind that PRIME.4 lists SHOULD be called through a declaration in such a form, its own or that of a function of the work that wraps it (DSGN.5)."

The first sentences of STND.STDC.29 and STND.CXX.21 are dropped. In C++, a declaration of the library now meets the outcome where a wrapper alone did, which is a relaxation. STND.CXX.21 keeps its release operation and destructor rule, instantiates DSGN.1 alone, and is retitled *Reported release failures*. STND.STDC.29 keeps the suppression at a call whose failure a test or handler receives, and is retitled *Suppressions where tests receive failures*. The onset paragraphs of STND.CXX and STND.STDC drop the CSQ2 onset of the moved first sentences. Each is a correction that the merge forces, not a new reading.

### 10. Named documents move to the repository configuration (D1; CL14)

- STND.CXX.1, *Reference guide of C++ practice*: "The repository configuration SHOULD name a published guide of C++ practice, at a recorded revision, as the reference for the C++ practice of the work …". STND.CXX.25 and the row of STND.CXX.25 in STND.STDC.1 name "the guide of STND.CXX.1".
- In STND.PY, the Terms replace Style PEPs and Numpydoc standard by Style guide and Docstring format, "the published … that the repository configuration names". STND.PY.1, .2, .10, and .11 use them.
- STND.PY.11 asks the type of a returned value "where the docstring format has a position for" it, because not every format has one.

The Notes keep the Core Guidelines, the style PEPs, and numpydoc as examples without a version, and record that the custodian's directions of 2026-10-22 name them.

**For the custodian (10a).** I left these unchanged, reading them as the definition of the language or model and not as third-party documents:
- STND.JL.22's "style guide of the reference manual";
- STND.PY's typing specification;
- the "OpenMP specification" of STND.OMP.

I recommend accepting that reading.

### 11. MPI copies of STND.CONC (R6.3; CS7)

I checked that STND.CONC holds each outcome for MPI:
- the term Concurrent task names a process;
- STND.CONC.21 declares the dependence on the number, the division, and the order of combining, which covers a reduction and concurrent accumulate operations;
- STND.CONC.22 is STND.MPI.19 with parts in place of blocks;
- STND.CONC.24 is STND.MPI.24 with the numbers that a component admits.

STND.MPI.18, .19, and .24 are withdrawn. The MPI Purpose names STND.CONC, and the Notes of STND.MPI and STND.CONC cite the STND.CONC provisions. STND.MPI.6 and .12, also named in CS7, are outside R6.3 and stay.

### 12. STND.OFFLD.31 and STND.PERF.12 (R6.3; CS14)

The first sentence of STND.OFFLD.31 stays: "Each measurement of the time of offloaded work SHOULD end at an observed completion of that work (RSRC.4, STND.PERF.14)." Its second sentence is withdrawn. STND.PERF.12 drops "Other than for offloaded work, which STND.OFFLD.31 holds," and so now reaches offloaded work in a performance evaluation. The Notes of STND.OFFLD cite STND.PERF.12.

STND.PERF.14 keeps its carve-out, because the first sentence of STND.OFFLD.31 still holds completion for offloaded work. Outside a performance evaluation, a measurement of offloaded work no longer states the costs of first use. The register accepts that narrowing (R6.3, and the refuted part of CS14).

### 13. STND.PERF.18 and MEAS.7 (R6.3; CS16)

> STND.PERF.18, second sentence: "… or be recorded, with its criterion and when it was set, as a criterion set after the summary was seen (VV.3, QA.12)."

**For the custodian (13a).** QA.12 is cited in `refers_to`, not in `instantiates`. Instantiating it would make false the class paragraph of STND.PERF ("instantiates only VV, REPRO, INTPR, SIMPL, RSRC, or AGENT.40"), and round o owns onsets. I recommend leaving it in `refers_to`; round o may move it.

### 14. STND.OFFLD.27 and STND.CONC.24 (R6.3; CS19)

> STND.OFFLD.27, added third sentence: "Tests that meet the two sentences above MAY serve, for device code, as the tests across numbers of tasks that STND.CONC.24 asks (VV.1)."

The Notes now call STND.OFFLD.27 the form of STND.CONC.24 for device code, and the third sentence of STND.CONC.24 still sets the tier of the comparison. The three modals form one bundle: the permission is not applied without the first two sentences.

**For the custodian (14a).** The permission relaxes STND.CONC.24 for device code. I recommend it, since the problem and group sizes are how device code varies its number of tasks.

### 15. Revision numbers leave the Notes (D1; CS15)

The Notes now name revisions by their order: "an earlier revision", "the revision after it", "the latest published revision that the research read", and "the next revision". The changes, document by document:
- STND.OMP: nine places.
- STND.FTN: "2018", "2023" (four places), and "Fortran 90", which becomes "the revision that introduced free source form".
- STND.STDC: "2024 edition" and "WG14 N3220", a draft number, which become "the working draft of C that the note read"; the clause numbers stay.
- STND.JL: "Julia 1.11".

Clause and section numbers, PEP numbers, and the revisions of the corpus's own documents are not revision numbers of a specification, and stay.

### 16. Kept because a document outside the scope cites them (for round e)

| Kept provision | Cited by | Restates |
| --- | --- | --- |
| STND.CXX.18 | Notes of STND.BUILD | STND.CODE.21 |
| STND.STDC.40 | Notes of STND.BUILD | STND.CODE.21 |
| STND.STDC.39 | Notes of STND.SV | STND.CODE.28 |
| STND.LEAN.27 | Notes of STND.SV | STND.CODE.28 |
| STND.PY.14 | Notes of STND.BUILD | (CL7, not carried; decision 18) |

One more item for round e: STND.SV.28 repeats STND.CODE.28. The Notes of STND.BUILD are corrected in this round (decision 20).

### 17. CL21: no change

CL21 has three parts:
- Its claim that a default may not use "SHALL" is refuted in the register (STND.DRAFT sets no modal for defaults).
- Its proposed Notes sentence, and the ambiguity of "CSQ4 included, though STND.CLASS.10 lets work of CSQ4 omit", are about the onset of STND.CODE.20, which ruling C2 gives to round c.
- I found no other defect in the Notes on STND.CODE.20.

So round d changes nothing there.

**For the custodian (17a).** I recommend confirming that CL21 is wholly round c's.

### 18. Unchecked entries not carried

| Entry | Holds? | Why it is not carried | Recommendation |
| --- | --- | --- | --- |
| CL7 | Yes | Carrying it needs a cadence that the ruling does not fix: at each release (Python) or at each change (Rust, Julia). STND.PY.14 also cannot be withdrawn this round (STND.BUILD cites it). | **For the custodian:** one default in STND.DEPS, at each release, or at each change where the configuration states it, carried in round e. |
| CL16 | No | STND.LEAN.31 also fails a build on a deprecation that a Lean package raises, where STND.BUILD.12 reaches only the work's own source at a recorded set. STND.JL.35 concerns run-time deprecations, which are Julia content. | None. |
| CL24 | In part | The Notes of STND.STDC give the reason: STND.CXX.3 depends on the newest-edition rule of STND.CXX.2, which the standing directions keep a C++ rule. | **For the custodian:** leave the two modes as they are. |

### 19. The Notes of STND.DEPS on STND.DFLT.11 (depends on round a)

At the coordinator's direction, the Notes of STND.DEPS now say that the last trigger of STND.DEPS.4 "is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit changes". The old Notes said it "narrows that of STND.DFLT.11, which reviews every direct dependency". The new sentence is true only once round a's STND.DFLT 1.6 applies (register R1.6, CC13). The rounds are ratified and applied together, and round a runs before round d in the driver, so this is acceptable (coordinator's ruling on review finding 5). The rationale of STND.DEPS 1.2 states the dependency. If round a is not ratified, this sentence reverts.

### 20. The Notes of STND.BUILD (review finding 6)

STND.BUILD 1.0.3 is an editorial transaction placed right after STND.CODE 1.4. Its Notes say that STND.CODE.21 "forbids", in place of "advises against", the setting near a required check, and that STND.CXX.18 and STND.STDC.40 "state" the same for C++ and C, in place of binding it alone. Contrary to the earlier decision 1b, the Notes of STND.SV do not cite STND.CODE.21 and need no change.

## Floor arguments of the provisions that bind

| Provision | Rests on | Argument |
| --- | --- | --- |
| STND.CODE.14 (second sentence) | PRIME.4 | Keeps out one form of response that may stay unseen. It asks no response beyond PRIME.4. |
| STND.CODE.21 | PRIME.4, DSGN.2 | One choice of compiler option for code that holds a check that the floor requires. It adds no check. |
| STND.CODE.33 | PRIME.4 | Only the diagnosis that PRIME.4 names, from a handler that the work writes. |
| STND.RUST.34 | PRIME.2 | Binds STND.CODE.34 for Rust as before: one sentence for each claim, which PRIME.2 already asks. STND.CODE.34 itself is a default. |

Every other provision that the round adds or changes is a default that a recorded decision replaces (GOV.19), so none raises the floor (GOV.11).

## Checks

The brief's checks were rerun after the review, with round a underneath (`ROUNDS=apply_round_a_2026_10_28,apply_round_d_2026_10_28`).

1. **Rehearsal.** 20 entries are appended: 5 from round a and 15 from round d. Every check passes, and the only warning is g.18, which the corpus already carries. Round d alone also rehearses with g.18 alone.
2. **Kept copy, rounds a and d.**
   - `references --check` passes.
   - `compose --check` reports 3 stale copies: `defaults.md`, `agent-instructions.md`, and `harness-specification.md`. These are round a's documents. With round d alone it reports 0 stale.
   - `pairs` was run for all fifteen documents. The 403 pairs whose changed side is a provision of this round are in `pairs-changed.md`, none a conflict. Within LVL2, the copies of decision 16 duplicate the new provisions word for word and do not conflict.
3. **New findings** of `tools/findings.py` on the changed documents, each a review finding, not a defect:
   - **g.12 on STND.PERF.18.** "After the summary was seen" describes the criterion and is no condition. MEAS.7 has the same finding.
   - **g.18 on STND.CODE.28, STND.CODE.29, STND.CODE.31, and STND.OFFLD.27.** Each has three modals that form one bundle. The permission of STND.CODE.28 qualifies its two sentences. STND.CODE.29 concerns one generator and its seed. STND.CODE.31 is one comparison, as STND.PY.20 was. In STND.OFFLD.27, the permission rests on the first two sentences.
4. **Drafting self-check.** For every provision drafted:
   - at most three modals, one modal per sentence;
   - conditions before clauses;
   - titles of six words or fewer, none verb-initial, and distinct;
   - body identifiers equal to `instantiates` plus `refers_to`;
   - no "such as" or "for example" in any provision.
5. **Harness code.** None was changed, so unit 0026 is not used and no verdict of a check on the live corpus changes.

## Review and dispositions

The cold review is `review.md` in this folder. Every Defect and Should-fix is fixed, and every Optional item is taken.

| # | Kind | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Defect | STND.DEPS.13 forbade the oldest-release run of STND.PY.14 | Fixed. The exception reads "a check that the standard of its language asks to run at revisions other than those that the lock file records"; the row and the Notes follow (decision 6). |
| 2 | Should-fix | STND.CODE.32 widened the reach to STND.CODE's own provisions | Fixed. It now reaches "each provision of the standard of each language of the work", as the withdrawn provisions held (decision 7). |
| 3 | Should-fix | The class paragraph counted STND.CODE.21 among the defaults | Fixed. STND.CODE.21 leaves both lists, and the paragraph says that it binds at every class (decision 7b). |
| 4 | Should-fix | STND.CODE.33 reaches C while the Notes denied it | Fixed with the reviewer's sentence on the handler of the signal that `abort` raises (decision 8). |
| 5 | Should-fix | The STND.DEPS Notes depend on round a | Kept, on the coordinator's ruling that the rounds apply together. The dependency is stated in the rationale (decision 19). |
| 6 | Should-fix | The STND.BUILD Notes are false after STND.CODE.21 binds | Fixed by the editorial transaction STND.BUILD 1.0.3, right after STND.CODE. Decision 1b's claim about STND.SV is corrected (decision 20). |
| 7 | Should-fix | STND.CODE.34 raised the mode for seven languages | Fixed. STND.CODE.34 is a default from CSQ2, and STND.RUST.34 binds it for Rust in one sentence, so each language keeps its strength. Reading 8a is withdrawn (decision 8). |
| 8 | Optional | STND.OFFLD.27 misdescribed STND.CONC.24 | Taken: "the tests across numbers of tasks that STND.CONC.24 asks". |
| 9 | Optional | STND.STDC.38 could reach less than before | Taken: the Notes of STND.STDC read the record of a verification as a record of a result under STND.CODE.34. |
| 10 | Optional | The revision row of STND.CODE omitted the changes to References | Taken for every changed document: each row now names the References rows that it adds or drops. |

The review's verdicts on the readings put to the custodian:
- It resolves these: 1a (first reading), 4a, 6a, 7a, 7b, 10a, 13a, 14a, and 17a. I agree with each, and they stay in this record as readings for ratification, with the reviewer's agreement noted.
- It keeps three open: 8a, now moot (finding 7), CL7's cadence, and CL24's modes.
