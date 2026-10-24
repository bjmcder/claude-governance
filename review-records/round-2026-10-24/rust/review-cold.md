# Cold review of STND.RUST draft 0.1

## Verified by script
- `govharness verify` on the rehearsal: all eight checks PASS. `findings.py 'STND\.RUST'`: ten g.18 notices only (.8, .12, .22, .23, .25, .26, .27, .29, .31, .33), the ten the onset paragraph lists. No defect-class finding.
- All body lines of the 36 rehearsal files appear verbatim in the reading copy. Binding set is .7, .14, .15, .16, .36.
- Titles at most six words ; one modal per sentence; no tool, product, or version named; no STND.DOCS.9 form in the Notes; all Terms used.
- Every S-number cited exists in rs1; none is S17, S20, or S27. Spot checks (Rudra 264, over 75% call chain, 19 properties over 416 APIs, Xu, poisoning, target-dependent panic default) agree.

## Defects
1. **The Notes attribute a direction the brief does not hold.** "The direction of 2026-10-24 for this standard asks for ..." reads as a ruling specific to this standard. The brief holds general standing directions only. Fix: "The custodian's standing directions keep it agnostic ..." and move "citing STND.CONC ..." into the drafter's statement of method.
2. **STND.RUST.14 sentence 2 raises the floor; the Floor paragraph says it does not.** STND.CXX.16, STND.PY.22, and STND.JL.13 have no counterpart. "SHALL deliver the message and the location of each panic", at every class, reaches (a) panics that answer no condition PRIME.4 lists, (b) a panic that sentence 1 lets the work catch and answer by "degrade visibly with a diagnosis" of its own, and (c) payloads with no message. It also fixes the content of the diagnosis, where PRIME.4 says "actionable". "Only keeps the actionable diagnosis" does not hold. Fix: either narrow it ("a panic that the work does not answer by another response of this provision SHALL still reach the operator or the record with a diagnosis") or make it a default (INTPR.8) and send the binding form to the custodian with the argument.
3. **STND.RUST.36 contradicts STND.RUST.3 as written and outruns STND.CXX.29.** "Each claim that code of the work is free of undefined behavior" includes every safety argument that .3 asks for, so a binding SHALL makes each comment name "each means by which that was checked". CXX.29 is limited to conformance claims about high-assurance code. PRIME.2 forbids misrepresenting evidence, and does not require every statement to list its means. Fix: limit to a claim "in a report, a record of a result or release, or a review", and say in the Notes that a safety argument is not such a claim. Keep the floor argument as a decision.

## Should-fix
4. **STND.RUST.15 is narrower in mechanism than STND.CXX.17 and so raises the floor.** CXX.17 admits "the compiler or a static check"; RUST.15 admits the compiler only. A Boolean-returning function checked by a static check fails .15 and passes CXX.17. Fix: add "or a static check". The `must_use` mark on `Result` is unverified in rs1; with the fix, the provision no longer rests on it.
5. **STND.RUST.16 sentence 1 is narrower than CXX.18, from which it takes the CPS reach.** CXX.18 requires each CPS.5/CPS.9 check to "run in every build". RUST.16 names two constructs, so a CPS check gated by `cfg(debug_assertions)`, or enforced only by an overflow panic, passes. Fix: add "or by a condition that an execution setting decides", and extend sentence 2 to the CPS checks. The reach itself copies adopted CXX.18 and is not new content or a raised floor. Untrusted-input checks stay covered by STND.CODE.6.
6. **Untrusted input reaches every `pub` function of a library crate.** In a workspace, each `pub` argument of an internal crate is untrusted, and binding .16 forbids `debug_assert!` on its preconditions. STND.JL's reach (`export`, `public`) is narrower, and the Notes are silent. Fix: reach "the functions that the documentation or the repository configuration names as the public interface of the crate", or send the reach to the custodian.
7. **STND.RUST.25 shows no single onset.** Sentence 2 cites DSGN.3 and DSGN.4; sentence 3 cites DSGN.4 and DSGN.2. DSGN.4 is a CSQ2 row; DSGN.2 and DSGN.3 start at CSQ3 (CSQ0 for mechanical contract checks). Fix: cite DSGN.4 alone in sentences 2 and 3, or say which ancestor decides.
8. **The onset sentence on .2 and .21 says they "tighten above the floor (PRIME.15)".** They are CSQ3 defaults, as STND.CXX.4 and STND.JL.34 are. Fix: use the STND.JL wording ("the part that rests on HW.5 or HW.7 applies only to work that HW binds").
9. **STND.RUST.22 sentence 3 restates STND.CONC.3 and .9**: a check-then-act that another task can break is what a stated protection excludes, and it has nothing to do with `Send` or `Sync`. Fix: delete it, or let the Notes say it is why sentence 1 names the protection.
10. **Unverified or narrated material in the Notes.** (a) "A drop that the language runs asynchronously is unstable, and its status moves": rs1 lists it as unconfirmed, and it is unmarked and not timeless; delete. (b) The 2026-08-20 incident (three packages): marked unverified, but PRIME.2 names citing an unconfirmed source, and GUARD.17 with STND.DEPS.6/.7 hold the point; delete. (c) "read as extracts that a retrieval tool wrote" and "a fact that rs1 does not support is marked unverified" narrate the research; move to the delivery message.
11. **STND.RUST.33 sentence 1 requires "a linter that reports" two specific conditions**, whose descriptions rs1 lists as unverified. Fix: "a check that reports ...".
12. **Proportion.** 36 provisions against 31, 31, 35 (CXX, PY/OFFLD, JL) and 4,955 words of Notes (CXX about 3,000). Candidates: .22 sentence 3, .13 (adds little to CONC.8), and the BUILD overlap below.

## Bundles (the ten notices)
- Hold: **.8** (three rests-on clauses, DSGN.1; one sentence with a list would drop the notice), **.26** (copies adopted CXX.22), **.23** (DSGN.1/.14, REPRO.7, all CSQ3), **.33** (all DSGN.3).
- One onset, weak on "never applied apart": **.12** (STND.CXX.21 bundles the same pair, so precedent), **.27** (ABI, catching, nonlocal jump are three hazards), **.29** (confinement, declared reads, no network), **.31** (additive-feature rule against combination tests). Fix: state that a replacement by decision replaces the bundle whole, or split .27 and .29.
- **.22** fails (item 9); **.25** unproven (item 7).

## Notes against the corpus and rs1
- Binding provisions against counterparts: **.7** has the shape and cost of STND.PY.4 and raises no floor beyond it. **.16**'s CPS reach copies CXX.18 and is not new (item 5 narrows it). **.14** sentence 2 and **.15** raise it (items 2, 4). **.36** is item 3.
- Overlaps: .17 parallels CXX.19; .19 parallels JL.17; .21 parallels JL.34; .24 adds a static check to CONC.8 (acceptable); .23 sentence 2 overlaps CONC.13 on releasing resources at cancellation (the increment is the drop point); .32 parallels JL.4 but removes the library exemption, which the Notes defend.
- Terms: "Safety condition" and "Safety argument" use "safety" where the corpus uses it for hazards (Safety-related component, PRIME.13); add "not an argument of the hazard analysis". "Feature" and "Foreign interface" are defined elsewhere (STND.OMP/WPROC, STND.CXX); a mixed C++/Rust project selects two foreign-interface terms; say so in one Notes sentence. "Unsafe attribute" is circular; define it by the marking the language requires.
- Class onset: right on .11 (CSQ1/CSQ3), .35 (CSQ2), .26/.27 (CSQ2); items 7 and 8 otherwise.
- Coverage: every rs1 gap is covered or left to NUMER and CONC on purpose.
- Optional: .12 sentence 1 "without a panic on every path" cannot hold for a `Drop` that deallocates; "without a panic that the implementation causes" can be checked.

## Overlap with STND.BUILD (parallel draft)
- **.29**: confinement of writes is BUILD.6, declared reads BUILD.1, the network BUILD.7. Keep a Rust sentence only for build-time code of dependencies, which runs with the builder's authority (.30 already does), and cite BUILD.
- **.33 sentence 3** (a warning fails the checks) is BUILD.12 and CXX.25 sentence 2; cite BUILD.12.
- **.2** against BUILD.11 (settings in one place for each compilation unit): keep the Rust list; cite BUILD.11.
- **.32** and **.1** may meet BUILD.20 and BUILD.25; recheck at the coalesce.

## Not checked
rs1 claims beyond the sample; the full STND.DRAFT word tables beyond `findings.py`; whether any PRIN.10 ruling of 2026-10-23 reaches STND.RUST (none found naming it).

## Verdict
**Revise before adoption.** Three defects (1 to 3). Items 4 and 5 also touch binding floors and belong in the same pass. The rest is wording, proportion, and the BUILD overlap. With 1 to 5 fixed, .7 and the CPS reach of .16 rest on adopted precedent (STND.PY.4, STND.CXX.18) and the five binding provisions meet GOV.11.
