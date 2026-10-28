# Round d of 2026-10-28: decisions

Round d carries ruling D1 and the restatement cleanups of the code and systems standards: register entries R6.2 and R6.3, the part of R7.1 that concerns revision numbers in Notes (CS15), and CL21 as far as it is not about onset. The module is `tools/amendment-scripts/apply_round_d_2026_10_28.py`, with the helpers `round_d_code.py`, `round_d_systems.py`, and `round_d_langs.py`. Nothing here is in force until the custodian ratifies it and the scripts run.

## Transactions

There are fourteen transactions, one per document, in citation order. Each document drops its citations of a provision before the document that holds that provision withdraws it. No state of the round cites a withdrawn identifier or a provision not yet added.

| # | Document | Revision | Class | What |
| --- | --- | --- | --- | --- |
| 0 | STND.CODE | 1.3 → 1.4 | Minor | .14 second sentence; .21 binding; new .27 to .35; Terms Library code; Purpose; Notes |
| 1 | STND.DEPS | 1.1 → 1.2 | Minor | New .13 (builds at locked revisions); Notes on .13 and on STND.DFLT.11 |
| 2 | STND.CONC | 1.1 → 1.1.1 | Editorial | Notes cite STND.CONC and STND.CODE.29 in place of the MPI, PY, and JL copies |
| 3 | STND.PERF | 1.0.1 → 1.1 | Minor | .12 reaches offloaded work; .18 aligned with MEAS.7 |
| 4 | STND.OFFLD | 1.1 → 1.2 | Minor | .31 keeps its first sentence; .27 serves as STND.CONC.24 for device code |
| 5 | STND.MPI | 1.0.2 → 1.1 | Minor | .18, .19, and .24 withdrawn; Purpose names STND.CONC |
| 6 | STND.OMP | 1.0.3 → 1.0.4 | Editorial | Revision numbers leave the Notes |
| 7 | STND.FTN | 1.1.1 → 1.2 | Minor | .29 and .37 withdrawn; .16 and .30 cite STND.CODE.14; revision numbers leave the Notes |
| 8 | STND.LEAN | 1.0.1 → 1.1 | Minor | .25 withdrawn |
| 9 | STND.CXX | 1.3 → 1.4 | Minor | .32 withdrawn; .1, .14, .21, and .25 reduced or reworded |
| 10 | STND.STDC | 1.2 → 1.3 | Minor | .29 and .38 reduced; row of .1; revision numbers leave the Notes |
| 11 | STND.JL | 1.3 → 1.4 | Minor | .21, .23, .24, and .26 withdrawn; .6, .14, .15, and .31 reduced or recited |
| 12 | STND.PY | 1.2 → 1.3 | Minor | .16, .17, .19, .20, and .32 withdrawn; .1, .2, .10, .11, .12, .22, .27, and .30 changed; Terms |
| 13 | STND.RUST | 1.2 → 1.3 | Minor | .13, .30, .34, and .35 withdrawn; .11 and .31 changed |

STND.CODE and STND.DEPS come first, because the language standards cite their new provisions. STND.PERF comes before STND.OFFLD, so that no state leaves the costs of first use of offloaded work unstated. STND.CONC drops its citations of STND.MPI.18, .19, and .24, STND.PY.17, and STND.JL.24 before STND.MPI, STND.PY, and STND.JL withdraw them. STND.FTN drops STND.PY.20 and STND.JL.21 before STND.PY and STND.JL run. STND.CXX and STND.PY drop STND.RUST.13 and STND.RUST.30 before STND.RUST runs last. MEAS is unchanged: STND.PERF.18 is aligned to it.

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

**For round e (1b).** STND.CXX.18 and STND.STDC.40 now restate STND.CODE.21 for C++ and for C. They stay because the Notes of STND.BUILD cite them. Two other sentences need correcting there:
- STND.BUILD's Notes say STND.CODE.21 "advises against" the setting, but it now binds.
- STND.SV's Notes say the same.

Round e should correct these Notes and then withdraw STND.CXX.18 and STND.STDC.40.

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

> STND.DEPS.13 (default; REPRO.1), *Builds at locked revisions*: "Other than a check that the standard of its language asks to run against newer revisions, each build of the checks and of each release of the work whose lock file is under version control SHOULD use the revisions that the lock file records, and fail on a lock file that does not match the files that declare its packages (REPRO.1)."

STND.RUST.30 is withdrawn.

**For the custodian (6a).** STND.LEAN.1 stays unchanged, against CL8's proposal to reduce it. It also pins the Lean toolchain and the checkers, and it reaches every Lean work, where STND.DEPS.12 keeps a lock file only for an environment that produces reported results. Reducing it would narrow it for proof work. I recommend keeping STND.LEAN.1 and accepting its overlap with STND.DEPS.13 for Lean packages.

### 7. Restated checks: tolerances, static checks, doctests, warnings (CL18, checked, holds; CL17)

- STND.CODE.31, *Tolerances stated at comparisons*, has the text of STND.PY.20, with "the equality operators of its language". STND.PY.20 and STND.JL.21 are withdrawn.
- STND.CODE.32, *Language provisions in static checks*: "The static checks that the repository configuration names under STND.CODE.4 SHOULD decide each provision of this standard and of the standard of each language of the work whose compliance a static check among the means of the work is able to decide (DSGN.3)." The second sentences of STND.PY.2 and STND.RUST.31 are dropped. STND.CODE.4 already has three modals, so this could not be a sentence of STND.CODE.4.
- The second sentences of STND.PY.12 and STND.JL.31 are dropped. Each restated STND.DOCS.13's comparison within a stated tolerance, and the Notes keep the forms in each language.
- CL17: the second sentence of STND.CXX.25 is dropped, because STND.BUILD.12 holds it. The Notes of STND.CXX and STND.STDC say so.

**For the custodian (7a).** STND.CODE.32 reaches the checks "among the means of the work". STND.RUST.31 reached each provision that "a static check of Rust source is able to decide". That is a narrowing for Rust; I recommend it, since a tool that the work does not have blocks no work.

**For the custodian (7b).** STND.CODE.31 rests on NUMER.11 and VV.3. It is added to the list of exceptions in the class paragraph of STND.CODE, with its onset (CSQ3) in the Notes. STND.CODE.35 is added in the same way. This is the only edit to an onset paragraph that is not a correction for a withdrawn identifier. It keeps that paragraph true until round o replaces it.

### 8. Installed handlers (CL25, checked; holds) and claims of undefined behavior (CL10, checked; holds)

> STND.CODE.33 (binding; PRIME.4), *Diagnoses from installed failure handlers*: "Where the work replaces or installs a hook or a handler that its language or runtime runs on a failure that a mechanism of the language propagates, or is unable to propagate, that hook or handler SHALL deliver to the operator, or to the record of the run, a diagnosis of each condition that PRIME.4 lists, that such a failure carries to it, and that no other response of STND.CODE.14 answers (PRIME.4, STND.CODE.14)."

STND.CODE.33 covers:
- the exception hooks of STND.PY.32, including the unraisable hook;
- the terminate handler of STND.CXX.32;
- the panic hook and the panic handler of STND.RUST.13 (second sentence).

STND.PY.32 and STND.CXX.32 are withdrawn. STND.CXX.33 (default) stays, as C++ content. Floor: the argument that the ratification of 2026-10-24 accepted for the Rust panic hook.

> STND.CODE.34 (binding; PRIME.2), *Claims of absent undefined behavior*: "Each claim, in a report, in the record of a result or of a release, or in a review, that code of the work is free of undefined behavior or of a kind of it, or that no use of an interface of the work is able to cause undefined behavior, SHALL state each means by which that was checked and the code, the code of dependencies included, that each means covered (PRIME.2). Such a claim SHALL NOT extend beyond the code and the executions that those means covered (PRIME.2)."

STND.RUST.34 is withdrawn. STND.STDC.38 keeps only whether the documentation of each means states that means as sound.

**For the custodian (8a).** STND.CODE.34 binds in every language a rule that bound only Rust. For C, the statement of the means was a default from CSQ2 (STND.STDC.38). The floor argument is the Rust one: PRIME.2 already forbids misrepresenting evidence, the cost is one sentence for each claim, and work that makes no such claim owes nothing. Ruling D1 fixes one provision per outcome but not this mode. I recommend binding, because it follows the adopted Rust rule and the pattern of STND.CODE.18. The alternative is a default for every language, which would lower Rust.

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

> STND.OFFLD.27, added third sentence: "Tests that meet the two sentences above MAY serve, for device code, as the tests at more than one number of tasks that STND.CONC.24 asks (VV.1)."

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

Two more items for round e:
- The Notes of STND.BUILD say that STND.CODE.21 "advises against" the setting. It now binds.
- STND.SV.28 repeats STND.CODE.28.

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

At the coordinator's direction, the Notes of STND.DEPS now say that the last trigger of STND.DEPS.4 "is that of STND.DFLT.11, which reviews the pinned revision of each dependency that the unit changes". The old Notes said it "narrows that of STND.DFLT.11, which reviews every direct dependency". The new sentence is true only once round a's STND.DFLT 1.6 applies (register R1.6, CC13), and round a runs before round d in the order of the driver. If round a is not ratified, this sentence reverts.

## Floor arguments of the provisions that bind

| Provision | Rests on | Argument |
| --- | --- | --- |
| STND.CODE.14 (second sentence) | PRIME.4 | Keeps out one form of response that may stay unseen. It asks no response beyond PRIME.4. |
| STND.CODE.21 | PRIME.4, DSGN.2 | One choice of compiler option for code that holds a check that the floor requires. It adds no check. |
| STND.CODE.33 | PRIME.4 | Only the diagnosis that PRIME.4 names, from a handler that the work writes. |
| STND.CODE.34 | PRIME.2 | One sentence for each claim. PRIME.2 already forbids misstated evidence. |

Every other provision that the round adds or changes is a default that a recorded decision replaces (GOV.19), so none raises the floor (GOV.11).

## Checks

1. **Rehearsal.** `ROUNDS=apply_round_d_2026_10_28 python3 -B -m govharness rehearse governance ../tools/amendment-scripts/apply_rounds_2026_10_28.py` appends 14 entries, and every check passes. The only warning is g.18, which the corpus already carries. A rehearsal of rounds a and d together also passes with g.18 alone.
2. **Kept copy.** On the kept copy:
   - `references --check` passes;
   - `compose --check` reports 0 stale, with `rendered/` copied beside the copy;
   - `pairs` was run for all 14 documents, and the 334 pairs whose changed side is a provision of this round are in `pairs-changed.md`, none a conflict. `pairs` lists only pairs across documents of other levels. Within LVL2, the copies of decision 16 duplicate the new provisions word for word and do not conflict.
3. **New findings** of `tools/findings.py` on the changed documents, each a review finding, not a defect:
   - **g.12 on STND.PERF.18.** "After the summary was seen" describes the criterion and is no condition. MEAS.7 has the same finding.
   - **g.18 on STND.CODE.28, STND.CODE.29, STND.CODE.31, and STND.OFFLD.27.** Each has three modals that form one bundle. The permission of STND.CODE.28 qualifies its two sentences. STND.CODE.29 concerns one generator and its seed. STND.CODE.31 is one comparison, as STND.PY.20 was. In STND.OFFLD.27, the permission rests on the first two sentences.
4. **Drafting self-check.** For every provision drafted:
   - at most three modals, one modal per sentence;
   - conditions before clauses;
   - titles of six words or fewer, none verb-initial, and distinct;
   - body identifiers equal to `instantiates` plus `refers_to`;
   - no "such as" or "for example" in any provision.

   The two g.13 defects found in drafting are fixed: "any" in STND.CODE.28 and "several" in STND.OFFLD.27.
5. **Harness code.** None was changed, so unit 0026 is not used and no verdict of a check on the live corpus changes.
