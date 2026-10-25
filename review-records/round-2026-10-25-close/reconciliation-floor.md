# Reconciliation review B: modes, floor, and class onsets (closing round of 2026-10-25)

Method. I rehearsed the round (entries 148 to 175). `verify` passes and `check_refs` reports 0 documents with missing rows. I diffed all 54 new or changed provisions against the live corpus, scripted mode against modal and body IDs against `instantiates` plus `refers_to` (no mismatch), and read the Notes, rationales, dispositions, the rulings (entries 103 to 105, 130, 132; `decisions-final.md`), unit 0010, and `a2-language-facts.md`.

## Blocking

1. **STND.HARN.30 rests on a reading of STND.DRAFT.42 that nobody has made.** The second sentence of STND.DRAFT.42 has a provision accept a standing authorization that GUARD.11 allows. HARN.30 refuses to rely on one without a further act of the human owner at each derivation. On its face that is a second owner act that LVL0 does not assign. Reading (a), that the acceptance is part of the grant (GUARD.10), is defensible: it is once per derivation, not per write, and a signer register avoids it. The Notes admit that the flag authenticates nothing, since an agent that runs the derivation can state it. The rationale correctly records no ruling. Fix: ratify only with the reading recorded. If the custodian reads the sentence strictly, apply `OPTION = "c"` in `apply_harn_1_3.py`, which drops HARN.30 and keeps the row. Recommendation: (a), since the custodian directed unit 0010 and the cost is bounded; say that the gain is a stated act, not authentication.
2. **Factual error, STND.CODE Notes (Finite values).** They say the binding form of CODE.21 stays in "STND.CXX.18 for C++, which STND.STDC applies to C in its C reading". After this round STND.STDC has no C reading of STND.CXX.18; STND.STDC.40 states it in its own words. Fix: "STND.CXX.18 for C++ and STND.STDC.40 for C".

## Should-fix

1. **STND.CODE.16 sentence 2: the reach is wider than its argument.** The Notes say a check "under a directive of conditional compilation on a macro that the source defines is removed in the same way", and the sentence binds at every class. Read literally it forbids a check that sits in a branch compiled out together with the code it guards, which leaves no input unchecked and asks more than PRIME.4. Fix: add "in a build that holds the code the check guards" to the second sentence. Also add the per-language statement R22 asks for Rust, Fortran, SystemVerilog `ifdef`, and Lean; the Notes cover only C, C++, Python, and Julia, yet the floor argument says "in any language".
2. **STND.STDC.2 may not bite.** It applies "where C code passes a condition ... to its caller in a result", but the old row said that errno alone is not a return in the result. A report through errno alone is therefore outside the condition, and only CODE.14 and CODE.7 catch it. Fix: "A report of a condition that PRIME.4 lists through errno alone SHALL NOT be taken as passing it to the caller in a result under STND.CODE.14."
3. **CUSTODIAN.md contradicts decision 6 of P1.** It says the high-assurance edition ruling "is for C++ only; it was not extended to C, Fortran, Rust, or Lean". CODE.17, .19, and .20 now reach all languages, and STDC.1 had applied them to C. The disposition puts the reach to the custodian; if approved, amend that line after ratification.
4. **High-assurance onsets are departures that are only stated.** CODE.17 and .19 apply as SHOULD from CSQ1, while the rows of STND.CLASS.10 for DSGN.3 and VV.1 start at CSQ0. CODE.20 applies "wherever such a standard is adopted", which includes CSQ4 and is an obligation above the floor that CSQ4 may omit. Ratified for C++ and C, new for the others. The Notes should call these departures and argue them from that precedent.
5. **CODE Notes (Responses)** name only STND.RUST.13 and STND.CXX for a panic hook or handler. Add STND.PY.32 and STND.CXX.32.
6. **STND.PY.33.** "The lock file of each environment" presupposes one. Where no installer writes one the provision blocks work, unless it reads "where an environment has a lock file".
7. **Edition yields are uneven.** PY.14, JL.1, and CXX.2 yield to CODE.19; the non-blocking newest-release checks (RUST.1 s3, JL.3 s3) do not. Fix: say in the CODE.19 Notes that such a check is not the delivered build. (Overlaps reviewer A.)
8. **Rust naming.** Decision 9 fixes names where the convention is checkable, and a2 fact 5 shows Rust's is. RUST.35 leaves it to the configuration. List it as a departure.

## Binding provisions new, moved, or changed

"More?" asks whether the provision asks more of a language than the instantiated provision, beyond wording or one record.

| Provision | Instantiates | Origin | More? |
| --- | --- | --- | --- |
| CODE.6 | PRIME.4, DSGN.2 | Term Untrusted input, widened reach | Form only; one threat-model record is the exit. Reach unruled (below) |
| CODE.14 | PRIME.4 | CXX.16, forms of PY.22, JL.15, RUST.13, FTN.29, LEAN.25 | No. The pass to the caller is ruled or ratified for C++, PY, JL, RUST, FTN, LEAN, C; new only for HDL |
| CODE.15 | PRIME.4 | CXX.17 | No. It is narrower than CXX.17, STDC.2's row, and RUST.14: a static check that reports every ignored result no longer counts. Disclosed as a lowering |
| CODE.16 | PRIME.4, DSGN.2, CPS.5, CPS.9 | CXX.18 s1, new s2 | S1 no (form of an existing check; in PY/JL the `assert` and `@boundscheck` forms). S2: see Should-fix 1 |
| CODE.18 | PRIME.2 | CXX.29 | No. One sentence per claim, in any language |
| CXX.18 | PRIME.4 and others | s2 only | No. Unchanged ruled text |
| CXX.32 | PRIME.4 | New | No; conditioned on a handler the work installs. No ruling |
| STDC.2, STDC.40 | PRIME.4 (and DSGN.2, CPS.5, CPS.9) | STDC.2 table of 1.0 | No. STDC.40 is the ratified C form. See Should-fix 2 |
| PY.32 | PRIME.4 | New | No; binds only a replaced hook. No ruling |
| PY.22, PY.25, JL.13, JL.15, RUST.13 to .15, FTN.29, FTN.31, LEAN.25 | PRIME.4 | Citations added | Text unchanged |
| HARN.29 row Signature | GOV.48, GUARD.2, GUARD.11, GUARD.12 | Unit 0010 | Narrows what proceeds without referral |
| HARN.30 | GUARD.10, PRIME.7 | Unit 0010 | See Blocking 1 |

## High-assurance defaults, CODE.17, .19, .20

They are defaults, so a project may replace them (GOV.19), and none blocks a language without a published standard: the term admits a standard of the work's own making, and the record may state that no validation is required. The floor is not at stake; what is open is extending a C++ ruling (R22). The argument is given once, generically, which is adequate for defaults. CODE.18 is the only binding one, and its argument holds by construction. Recommend yes, with Should-fix 3 and 4.

## Reach of Untrusted input

The reach through CODE.6 binds at every class and is new to C, C++, Lean, HDL, and to documented functions in every language. The cost is the form of a check that code already makes: an `assert` on an argument of a documented function in C or C++ becomes a test with a response. The exit is one threat-model record that the source is trusted (GUARD.16). That meets the allowed cost, wording or one record. The Notes state per language what is reached and say that no ruling covers it. Verified:
- **PY.25, JL.13.** The ruled reach is kept: public interface of library code, and `export` or `public` functions. Documented functions outside it are the addition.
- **RUST.15.** Documented functions outside library crates are added, argued in the Notes.
- **FTN.31.** Documented external procedures are added and argued; undocumented ones stay out.
- **C and C++.** Contract-style `assert` is common, so the reach matters most here.
- **Lean.** Nothing is added, since a proved precondition has no run-time check.
- **HDL.** Top-level ports and documented functions or tasks; the check must be logic, not a simulation-only assertion.

The widening also reaches the defaults FTN.15, JL.17, RUST.18, STDC.21, and STDC.27, which the Notes do not name. Recommend the union.

## Class onsets

Agree with STND.CLASS.10: CODE.14, .15, .16, .18, CXX.32, STDC.2, STDC.40, PY.32; CODE.21 (DSGN.2 base, CSQ3); CXX.33 (INTPR.8 row, CSQ1); JL.36 (DSGN.2 row, CSQ1, as CXX.27); PY.34, .35, .37 and JL.37, .39, .41 (DSGN.4 or DSGN.5, CSQ2); PY.33, PY.36, JL.38, JL.40, STDC.39, RUST.35, FTN.37, SV.28 (no row, CSQ3); OFFLD.31 (CSQ3, as PERF.12 and PERF.14). Departures: only Should-fix 4.

## Tools, owner decisions, rulings

- **Tools.** CODE.15 is conditioned on a form of declaration, and the foreign-interface defaults on a case or a test. Only PY.33 is open (Should-fix 6).
- **Owner decisions.** Only HARN.30 (Blocking 1).
- **Rulings.** Every attribution I checked was made: 2026-10-23 for CXX.3, .16, .17, .18, .29 and the PY and JL reach; 2026-10-24 for the RUST and FTN reach, LEAN.25, STDC.2, RUST.13 sentence 2, and decision 9. The rationales say "no ruling covers it" for CXX.32, PY.32, and the documentation reach.

## Decisions for the custodian, with recommendations

1. Reading of STND.DRAFT.42 for HARN.30: (a).
2. Reach of Untrusted input by documentation and into C, C++, Lean, HDL: the union.
3. CODE.16 s1 for languages without a ruling and s2 for all: yes, after Should-fix 1.
4. CODE.15 lowered to the declaration form: yes.
5. CODE.17, .19, .20 for every language, with CUSTODIAN.md amended: yes.
6. CXX.32 and PY.32 as binding, conditioned: yes.
7. No change for CXX.27 against JL.34 and for the Python counterpart of JL.13 sentence 3: yes.
8. Rust naming left to the configuration: yes.

## Not checked

The harness suite, the verification of the last fixes (reviewer C), and external facts beyond `a1` and `a2`.
