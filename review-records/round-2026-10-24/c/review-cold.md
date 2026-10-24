# Cold review of STND.STDC draft 0.1

## Verified by script
- `govharness verify` on the rehearsal: eight checks PASS, plus one corpus-level `g.18` atomicity warning I did not trace. `findings.py 'STND\.STDC'` prints nothing.
- Reading copy: all 40 bodies match the rehearsed files.
- Four binding (.2, .3, .28, .29), each on PRIME.4, PRIME.2, or GOV.48; the rest default. Titles at most six words, noun phrases, unique corpus-wide. One modal per sentence, at most two per provision, at most one condition per sentence, no word from the tables of STND.DRAFT.7, .13, .17, .29, .33. No compiler, tool, version, or coding standard in any body.
- By hand only: the C reading, floors, onsets, Notes against c1, overlaps.

## Defects
1. **STDC.29 (binding) rests on facts c1 lacks and fixes no order.** c1 says nothing on the persistence of a stream's error indicator or on what closing reports; the Notes state both flatly. The body gives no order, and a test of the indicator after the close is a use after the end of the stream's lifetime (STDC.9). Fix: "SHALL test the error indicator of that stream before it closes the stream, and the result of the call that flushes or closes it". Mark the two facts unverified, or cite the standard's text once checked.
2. **The floor argument for STDC.29 and the CERT resolution say PRIME.4 lists "a failed write of a result".** PRIME.4 lists four kinds: invalid input, precondition violations, non-convergence, resource exhaustion. A full disk is the nearest; an I/O error is unlisted. The resolution still holds (CODE.7 prevails for listed kinds, CODE.12 governs the rest) but not on this premise. Fix: argue STDC.29 from the last sentence of PRIME.4 (silent continuation past an error), present it as a decision, and drop the phrase.
3. **"Foreign interface" has no C reading.** STDC.1 applies CXX.4, whose second sentence uses it. By substitution it reads "code that does not follow the C rules ... a C or vendor library interface", which is circular, and Terms do not import it. Fix: define it in Terms: an interface between C source and code of another language, a callback or thread that a runtime of another language starts, and a structured block of a compiler directive.

## Should-fix
1. **The C reading mechanism.** Verdict: a citation, not a restatement (GOV.31 prunes text; this adds a table of changes), and STND.DRAFT does not bar it; DRAFT.20 holds. Weaknesses:
   - A provision is the unit of replacement (REPRO.7), so dropping one row of STDC.1 means replacing 14. Row onsets run from CSQ1 to CSQ3 and live only in the Notes. Fix: an "Applies from" column, or split STDC.1 by onset (CSQ1: CXX.24, .27, .28, .30, .31; CSQ2: CXX.7, .26; CSQ3: the rest).
   - "Follows the revision of STND.CXX in force" is in the Notes. Put it in the Terms definition of "C reading".
   - "SHALL apply ... each sentence with its modal" puts a SHALL over SHOULD sentences. Say "each sentence keeps its modal and the mode of its provision".
2. **Rows under both revisions of CXX.** CXX.15 row: under 1.0 it drops the concurrent-calls item, under 1.1 it fits, and "C++ exception" becomes "C exception". Write "without the words reference, view, iterator, and C++ exception". CXX.23 row says the type "is" volatile sig_atomic_t and loses the lock-free atomic alternative of both revisions. CXX.28 row is redundant (the term is already read for C). Instantiates: STDC.1 omits HW.11 (CXX.23 1.0); STDC.2 omits DSGN.2, CPS.5, CPS.9 (CXX.18) (DRAFT.19, .23).
3. **CXX.7, .9, .12 against c1.** CXX.12: sound, and the Notes disclose c1's contradiction. CXX.9: c1 lists .8 to .10 as not carrying and the Notes never say so; give the reason (C library results that the implementation defines) and move the examples out of the unverified clause. CXX.7: the Notes cite c1 for "holds as written", but c1 says only the register-layer idea carries. Sentence 1 (a pointer type distinct from a host pointer) is unaddressed; a typedef is not distinct in C, a volatile-qualified pointer is, and an accelerator pointer needs a wrapper structure. Fix: a CXX.7 row that says how sentence 1 is met.
4. **STDC.3 and STDC.2 extend C++ rulings.** The "latest edition" direction and the no-floor rulings of 2026-10-23 concern C++. The Notes rightly call the extension a decision, but the argument for STDC.3 ("the direction is lost silently") has no custodian direction for C behind it, and c1 practice 1 says "a stated edition". Fix: argue from GOV.48 alone and ask whether "newest edition" is meant for C, or make STDC.3 a default.
5. **STDC.28 adds nothing binding.** CXX.16 (STDC.2) lists the responses, and "return the condition in its result" excludes errno alone. "Which PRIME.4 forbids" overstates, since errno alone is not silent if read. Fix: put the reading in the Notes of STDC.2 and drop the fourth binding provision, or make it a default. It also sits against STDC.32 sentence 1 ("an object that its contract names").
6. **STDC.8 and STDC.11 cost too much.** Each subscript and each signed operation needs a check or a comment; a static check's proof does not qualify. c1 practice 2 limits the range argument to operands from outside the function. Fix: limit STDC.11 to such operands, and add "or by a static check" to both.
7. **STDC.5 sentence 2** mandates a mechanism (one sequence written once in the function) while the Notes say a wrapper that owns the release also meets it. Add "or by a function of the work that owns the release".
8. **Onset of DSGN.2 provisions.** CXX.24 and .27 take DSGN.2 from CSQ1 (CXX Notes); STDC.11, .13, .18, .21, .22, .27 take it from CSQ3 as "preconditions". DSGN.2 requires precondition checks only where untrusted data enters; the rest is "where cheap" (CSQ1). Argue the split, or move STDC.11, .13, .18 to CSQ1.
9. **Build overlap.** The Purpose says STDC holds no provision on building, yet STDC.16 s2, .25, .26 s2, and .38 name builds and warning sets. Against STND.BUILD: CXX.4 s3 (via STDC.1) repeats BUILD.11; CXX.25 s2 repeats BUILD.12. STDC.16 s2 is test evidence (VV.1), not a build duty, and may stay; it needs BUILD.13 (checking builds named apart, parts linked without the check recorded) and should cite it once adopted.
10. **Proportion.** 40 provisions and about 8,400 words, against 31 to 35 and 5,300 to 7,200 for CXX, PY, JL, OMP, OFFLD. Merge STDC.38 and .39 into the C reading of CXX.25 and CXX.26. STDC.31 repeats STDC.29 on close. Also candidates: STDC.11 with .12, .34 with .35.
11. **Notes.** The version-macro duty ("names an edition ... by the value of the version macro") is an indicative obligation with no provision. The standing-direction and S24 sentences narrate drafting (DOCS.9); "offers" and "rather than" are listed patterns. The "40 percent" figure covers unstable code in general, not the pointer-wraparound test it is paired with.

## Optional
- Unverified points of c1 (errno per thread, jumps across frames, consume ordering, provenance specification, `defer`, library qualifiers, the 221 count) stay out of provisions and are marked in Notes.

## Overlaps
| Provision | Existing | Verdict |
| --- | --- | --- |
| 1, 2, 3 | CXX.2 to .31, GOV.48 | Citation; Should-fix 1, 4, 5 |
| 5, 6 | CXX.15, MPI.11, DSGN.14 | Adds release path and function |
| 8 to 10 | CXX.6, DSGN.1, DSGN.14 | Adds C classes |
| 11 to 13 | DSGN.2 | Adds operations; cost, see 6 |
| 19, 21 | CODE.6, DSGN.2 | Partial repeat between 19 s1 and 21 s2 |
| 28, 29, 31 | CODE.7, CXX.16, CXX.17 | 28 is CXX.16 read; 29 and 31 overlap on close |
| 30 | CXX.17, CXX.21 | Adds dependency wrapper |
| 36 | CONC.3 | Adds the unit (adjacent bit-fields) |
| 38, 39 | CXX.25, CXX.26 | Mostly repeats; merge |
| 40 | CONC.27, CXX.29, VV.1 | Adds analyzer soundness |
| 16, 25, 26 | BUILD.11 to .13 | Cite BUILD.13 |

## Not checked
The ISO text (stream indicator, `fclose`); the pair list; STDC.40 onset beyond the INTPR.10 row; custodian rulings beyond what the Notes of CXX record.

## Verdict
Revise. The mechanism is admissible, coverage of c1 is complete, and the drafting rules pass. Defects 1 to 3 must be fixed before adoption; Should-fix 4 and 5 change what binds.
