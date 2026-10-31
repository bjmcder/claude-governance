# Round of 2026-10-31 on the cleanup audit: part tech, the profiles and technical standards

This record carries the outcomes of the section "Profiles and technical standards" of `../decisions.md`: S7 (recommendation R7), S8, B8, O3, I2, I6, and I7 of `../findings.md`. The script is `tools/amendment-scripts/apply_audit_tech_2026_10_31.py`, run by the driver `apply_audit_2026_10_31.py` after the part lvl0. Nothing here is in force until the custodian ratifies it and the script runs. Recommendation R7 is not yet ruled; the draft carries the recommended option (a), and it goes to the custodian at ratification with the rest.

## Transactions

Ten transactions, one per document, each a GOV.41 amend by The Custodian, role custodians, through `F.finish`, which adds the revision row and rewrites the References table. The profiles come first, then the standards that cite them:

| k | Document | Revision | Class | Findings |
| --- | --- | --- | --- | --- |
| 0 | CPS | 1.0.2 to 1.1 | Minor | S7 (R7) |
| 1 | NUMER | 1.4.1 to 1.5 | Minor | O3 |
| 2 | ML | 1.0.2 to 1.1 | Minor | I7 |
| 3 | STND.VVUQ | 1.5.1 to 1.5.2 | Editorial | O3 |
| 4 | STND.CODE | 1.7 to 1.8 | Minor | I2 |
| 5 | STND.DEPS | 1.3 to 1.3.1 | Editorial | S8 |
| 6 | STND.DOCS | 1.0.2 to 1.0.3 | Editorial | I6 |
| 7 | STND.CXX | 1.5 to 1.6 | Minor | B8, I6 |
| 8 | STND.PY | 1.5 to 1.5.1 | Editorial | I6 |
| 9 | STND.RUST | 1.5 to 1.5.1 | Editorial | I6 |

ML and NUMER cite each other, and the standards cite each other in cycles, so no order puts every cited document first. The order taken: CPS, which cites none of the others; NUMER, then ML; STND.VVUQ, which cites only profiles among these; STND.CODE, the practice of every language; STND.DEPS and STND.DOCS; then the language standards. The ledger numbers are not fixed here, since they shift when the parts combine.

## S7, CPS.1 (recommendation R7)

**Mechanism.** GOV.12 ends: "A profile MAY require work in its domain to be classified at least as severe as a stated class." STND.CLASS.1 has the human owner set, among the classes it lists, "the class that a selected profile requires (GOV.12)". So the text supports option (a) as R7 states it, and it needs no LVL0 change. No profile used the permission before.

CPS.1 gains a second sentence and GOV.12 in `instantiates`:

> This profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26). Work on a system that commands physical hardware SHALL be classified CSQ3 or a more severe class (GOV.12).

The subject is the work on a system that commands physical hardware, the domain item of CPS (STND.DRAFT.37), and not the project, so that a component that the classification records as isolated from every such system keeps its own class under GOV.13. The CPS term Command already covers configuring and powering. CPS.1 still reaches GOV alone through its lineage, so it stays non-waivable, with rank null and no field `onset`.

The Notes gain, after the sentence on PRIME.13:

> CPS.1 has work on a system that commands physical hardware classified CSQ3 or a more severe class, as GOV.12 lets a profile require of work in its domain: a wrong command is able to damage the hardware it drives, or what that hardware acts on, a loss beyond the author's own time that the consequence test of CSQ3 in STND.CLASS.1 counts, and the minimum keeps CPS.3 to CPS.9 in reach of all such work, the revision of the hazard analysis before an uncovered change first drives the hardware among them. A credible path to injury, or to a major and hard-to-reverse loss, still sets CSQ0 or CSQ1 (STND.CLASS.1), and a component that the classification records as isolated from every system that commands physical hardware keeps the class recorded for it (GOV.13).

and the closing sentence of the class paragraph becomes:

> No provision raises the floor (GOV.11): the minimum class of CPS.1 is the one that GOV.12 lets a profile require, and the floor of GOV.10 holds for such work unchanged.

**Floor argument (GOV.11).** The minimum raises obligations for work on such a system that was CSQ4: CPS.3 to CPS.9, the revision of the hazard analysis under CPS.3 among them. It does not raise the floor:
- The floor is the set of GOV.10, which holds at every class. The minimum leaves it unchanged.
- The minimum places work of a domain in a class by the means that LVL0 itself gives a profile (GOV.12). The obligations it brings are the ones above the floor that GOV.11 proportions to CSQ3.
- It proportions them to the consequence, as GOV.11 and PRIN.9 ask, not to the setting or the hardware of the work. A wrong command is able to damage the hardware it drives. That is a loss beyond the author's own time, which the consequence test of CSQ3 in STND.CLASS.1 counts and which STND.CLASS.2 already counts as met in doubt. So the minimum records what the criteria give for the domain, and removes the doubt.
- It asks no decision of the human owner beyond the classification and the adoption of the hazard analysis under PRIME.13, which LVL0 already assigns (STND.DRAFT.42).

It fits the LVL0 part as drafted. GOV.13 there presumes CSQ4 until a class is recorded, and that presumption never covers driving physical hardware.

**Transition (GOV.42).** A project whose classification records CSQ4 for work on a system that commands physical hardware records CSQ3 or a more severe class for that work before the system next drives the hardware. Until then, work that conforms to revision 1.0.2 is not in defect.

**For the custodian at ratification.**
1. Option (a) of R7 is drafted. Option (b), PRIME.13 carrying the revision duty at every class, amends a prime directive. A third mechanism was weighed and is not recommended: setting the field `onset` of CPS.3, and of CPS.5, CPS.6, and CPS.9, to null, so that they apply at every class. GOV.19 marks these provisions default, and an onset of null for a default above the floor raises the floor at CSQ4, which GOV.11 admits only by a recorded project decision that names the consequence. It also leaves the other CPS provisions at CSQ3, so a CSQ4 bench project would owe the revision of CPS.3 without the command record of CPS.7. The minimum class keeps the profile whole and uses the means that GOV.12 provides. *Recommendation: (a), as drafted.*
2. The subject is the work on a system that commands physical hardware, not the whole project. *Recommendation: keep it.* A project that also holds analysis isolated from its controller keeps CSQ4 for that analysis under GOV.13.

## O3, NUMER and STND.VVUQ

**Verification of the audit's claim.** I read every provision of STND.VVUQ with its `onset` and lineage. The core that applies from CSQ3 is STND.VVUQ.1, .3, .5, .7, .13, .17, .62, .64, and .82.

| NUMER part | Default methods of STND.VVUQ | Their onset | Reach of the core |
| --- | --- | --- | --- |
| NUMER.5, sentence 2 (working precision shown to keep the rounding error within the required precision) | STND.VVUQ.9 (sentence 2), .36, .37, .38 | CSQ2 | None. STND.VVUQ.7 uses the required precision, not the working precision. The hardware contract of HW.5, whose delivered arithmetic the sentence records, and the boundary contract of HW.13 also start at CSQ2. |
| NUMER.7 (order behavior) | STND.VVUQ.20 to .24 | CSQ2 | None |
| NUMER.12 (rounding under conditioning) | STND.VVUQ.36, .37 | CSQ2 | Only through tier 3 of STND.VVUQ.1, whose agreement is "a tolerance set from the rounding error estimated under NUMER.12". The core gives no method for that estimate. |
| NUMER.23, sentence 2 (the statistical uncertainty settles as the samples grow) | STND.VVUQ.61, sentence 2 | CSQ2 | None |
| NUMER.25 (error rates of a statistical criterion) | STND.VVUQ.33, .34, .35, .65 | CSQ2 | Partial. STND.VVUQ.7 places a tolerance within its bracket, with the required precision as the departure to detect, which is the last clause of NUMER.25. STND.VVUQ.64 judges fresh-seed tests under STND.VVUQ.33 to .35, which start at CSQ2, so at CSQ3 such a test is judged by its own stated criterion. |

So the claim holds. The core gives a default method for none of the five parts. Where it reaches NUMER.12 and NUMER.25, it uses an estimate or a relation that it does not supply.

**Gaps.** After the move, nothing that the five parts serve is left unasked at CSQ3:
- VV.1, VV.5, and PRIME.3 apply to work of CSQ3 in full (STND.CLASS.10).
- NUMER.11 still gives every tolerance a recorded basis at CSQ3.
- NUMER.13 still has each uncertainty component marked, "not assessed" among the markings.
- NUMER.26 still bars reseeding to pass at every class.
- Tier 3 of STND.VVUQ.1 still needs a rounding estimate where a comparison at CSQ3 takes that tier. The Notes of STND.VVUQ now say so.

The CSQ3 defaults STND.VVUQ.7 and STND.VVUQ.64 list NUMER.25 in `instantiates`. At CSQ3 they still rest on VV.1 and VV.3, which they also instantiate, so the lineage stays sound. No check compares the onset of a provision with that of its parents, and `verify` passes. So no gap calls for the alternative, and the move is drafted as `../decisions.md` gives it.

**Drafted fields.** NUMER.7, NUMER.12, NUMER.25: `onset: "CSQ2"`. NUMER.5, NUMER.23: `onset: ["CSQ3", ["sentence 2", "CSQ2"]]`, in the form of the existing fields (STND.CODE.22, STND.MPI.7, and others). Under STND.CLASS, a part that asks for no item of the table of STND.CLASS.10 applies from CSQ3. These fields depart from that rule, so the Notes of NUMER give the reason that the Notes of STND.CLASS admit, methods of a standard beyond its core. The sentence added after the class sentence of the NUMER Notes:

> NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23 apply from CSQ2, a departure from the rule of STND.CLASS: an order test, an estimate of rounding error under conditioning, a showing that the working precision keeps that error within the required precision, evidence that a statistical uncertainty has settled as the samples grow, and the error rates of a statistical criterion each cost an analysis or added computations rather than one statement, and the default methods for each are those of STND.VVUQ beyond its core, which start at CSQ2, while VV.1, VV.5, and PRIME.3 hold for such results at CSQ3 in full.

The STND.VVUQ Notes replace "so that work of CSQ3 meets NUMER through the core, while the obligations of LVL0 that the other provisions serve apply to it in full" with:

> as do NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23, whose default methods are among them. Work of CSQ3 meets each other provision of NUMER through the core where the core reaches it, and otherwise by a method that the work chooses or by the statement that the provision admits, a component of NUMER.13 marked not assessed among them, while the obligations of LVL0 that the other provisions serve apply to it in full; a comparison at CSQ3 that takes tier 3 of STND.VVUQ.1 still sets its tolerance from an estimate of rounding error of the kind that NUMER.12 describes.

**Floor argument (GOV.11).** Moving an onset from CSQ3 to CSQ2 narrows a waivable default to more severe work. It lowers no floor and raises none. VV.1, VV.5, and PRIME.3, which these parts serve, apply at CSQ3 in full.

**For the custodian at ratification.**
1. **The alternative of `findings.md`.** Have "not assessed", with the unverified label of PRIME.3, meet these parts at CSQ3, leaving them at CSQ3. The draft would add a sentence to the class paragraph of the NUMER Notes, keep the five fields at CSQ3, and give NUMER.12 and NUMER.23 a permission. NUMER.12, in one form, would gain: "Where the work is of CSQ3, the estimate MAY be marked not assessed under NUMER.13, and the result reported as unverified (PRIME.3) (VV.5, INTPR.9)." It is not recommended. It writes a class into a provision body, which the field `onset` exists to keep out, and it keeps an unverified label on every CSQ3 result that uses floating point. *Recommendation: the move, as drafted.*
2. **The third sentence of NUMER.5** asks the record of the working precision to take an exchanged precision from a boundary contract of HW.13. It stays at CSQ3 as `../decisions.md` gives it. At CSQ3 it governs only a record that the work keeps by choice, since the boundary contract starts at CSQ2. Moving it with sentence 2 (`["CSQ3", ["sentence 2", "CSQ2"], ["sentence 3", "CSQ2"]]`) changes nothing in practice. *Recommendation: leave it.*
3. **The first sentence of NUMER.23**, evidence that the samples represent their distribution, keeps CSQ3. Its default methods (STND.VVUQ.58, .60, and the first sentence of .61) also start at CSQ2. The same holds for NUMER.22 (STND.VVUQ.57). The audit did not raise them, and `../decisions.md` does not move them. Each follows the rule of STND.CLASS, and work of CSQ3 meets each by a method of its choice. *Recommendation: no change in this round.*
4. **HW.QPU.6 and HDES.ASIC.5** cite NUMER.23 and NUMER.25 and keep their content at CSQ3 for quantum-processor sampling across calibrations and for sampled device variation. The move does not reach them. Each is a tightening above the floor within its domain (PRIME.15). *Recommendation: leave them.*

## I7, ML term Learned model use

The term gains a sentence, and the Selector text now cites the term rather than stating the exclusion alone:

> | Learned model use | An attribute, true when the classification records that a learned model sits, or is admitted to sit, on a path that affects a result the work reports or relies on, or physical hardware. A learned model in its use as the model through which an agent does the work does not make the attribute true. |

> The term Learned model use leaves out the model through which an agent does the work, which the agent practice profile (AGENT) and the Safeguards Article (GUARD) govern; a learned model that the work itself places on such a path makes the attribute true, whatever else it is used for.

Taken literally, the old term was true of every project in which an agent works. "In its use as" keeps a learned model that the work itself places on a result path, of whatever kind, under ML. **Floor:** no obligation is raised, and the selector narrows to the reach that its Notes always gave it. The agent's model stays under GOV.48, AGENT, and GUARD. The term is in the profile's Terms, so the fix sits in the term, not in ML.1, whose body only tests the attribute.

## I2, STND.CODE.30

The second sentence becomes:

> Where the documentation of a collection leaves its order of iteration free to change between runs or between releases, each reported result on whose path the collection lies SHOULD be independent of that order, or have its dependence on that order declared as run-to-run variation and lie within the tolerance of each comparison that judges it (REPRO.3).

The Notes gain:

> Its second sentence asks no bitwise identity: a result that depends on such an order meets it once that dependence is declared as run-to-run variation and lies within the tolerance of each comparison that judges the result, as STND.BUILD.15 admits for the output of a build step, and STND.VVUQ.82 then treats the difference as no defect.

The wording follows STND.BUILD.15 and REPRO.3, and STND.VVUQ.82 covers the judging. "Each comparison that judges it" is empty where no comparison judges the result, and the declaration that REPRO.3 asks then suffices. **Floor:** the change widens a waivable default from CSQ3 and raises nothing. Undeclared variation stays a defect (REPRO.3).

## S8, STND.DEPS Notes

The Notes on STND.DEPS.14 become:

> A revision that a declared range admits is one the configuration names, so a check of STND.DEPS.14 installs it under STND.DFLT.34 and adds nothing that STND.DFLT.35 halts; a run of such a check that retrieves a revision from outside the provisioned environment is also network access, which needs its own authorization (GUARD.13), as the Notes of STND.DFLT say of every install that retrieves.

The wording is the one that the STND.DFLT Notes already use for an install that retrieves. Only the Notes change, as `../decisions.md` gives it. GUARD.13 itself holds the obligation, and DEPS.14 would restate it.

## B8, STND.CXX.2 and STND.CXX.3

STND.CXX.2, first sentence: "Other than for an edition that STND.CODE.19, a dependency, a hardware contract, or a qualification of the toolchain fixes, …".

STND.CXX.3 becomes:

> Other than in a change whose decision record names the compiler, the dependency, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain that requires it, an agent SHALL NOT lower the edition in force for a translation unit (GOV.48, DSGN.3). Other than in a change whose decision record names the compiler, the dependency, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain that requires it, an agent SHALL NOT state for a translation unit that it creates an edition older than the edition that STND.CXX.2, or the alternative that a project instrument adopts in its place, gives (GOV.48, DSGN.3).

The Notes gain, after "costs one sentence":

> That record names the cause among those that STND.STDC.3 admits for C: the compiler, a dependency whose source does not compile at the edition in force, the high-assurance coding standard, the hardware contract, or the qualification of the toolchain; STND.CXX.2 leaves out of its recommendation the edition that a dependency fixes.

The order of the causes follows STND.STDC.3. **Floor:** a binding prohibition gains an exception. The exception costs the one decision record that the provision already asks, and the custodian's ruling of 2026-10-23 that STND.CXX.3 raises no floor is unchanged. The prohibition relaxes no higher provision, since neither GOV.48 nor DSGN.3 asks for the newest edition.

## I6, the binding reason of each instantiator of GOV.48

**Reading.** GOV.19: "A provision is marked binding only where it instantiates a prime directive, GUARD, or a floor obligation (GOV.10), or where the custodians record why uniformity across projects requires it; every other LVL2 provision, including every provision of form or style, is a default." GOV.10 puts GOV in the floor, so an instantiator of GOV.48 meets the first limb. The check l.4 counts it as forced, so it needs no `binding_reason` to verify. The audit reads GOV.19 the other way: a provision of form or style is a default unless the custodians record the reason. Recording the reason meets GOV.19 on both readings and keeps the corpus verifying. A forced binding provision with a recorded reason has precedent: each of STND.DRAFT.35 to STND.DRAFT.41 reaches GOV and carries the field. Making a provision a default from CSQ3 would mean dropping GOV.48 from its `instantiates`, since l.4 fails a non-waivable default. That changes its lineage, and it lets work of CSQ4 omit a rule that guards against a silent loss at every class. It would also undo the custodian's ruling of 2026-10-23 on STND.PY.4 and STND.CXX.3. So a reason is drafted for each of the four GOV.48 provisions of this part's documents that rest on GOV.48 alone among PRIME, GUARD, and the floor. None becomes a default. Each field holds a draft for the custodians to adopt at ratification.

| Provision | Drafted `binding_reason` |
| --- | --- |
| STND.DOCS.10 | An agent configuration works across projects under the same agent instructions (STND.DFLT.21), so a rule of agent conduct holds alike in each project only where it binds in all; the human owner and the reviewers of every project verify the text that an agent writes against the work (INTPR.1), and inflated or generic prose, notes about the agent, and known false statements defeat that check at every class, so one rule for every agent lets each reader rely on agent-written text without first learning the class of the work, while the spelling, content, and patterns stay each project's through the alternatives it adopts. |
| STND.CXX.3 | An agent configuration works across projects under the same agent instructions (STND.DFLT.21), so a rule of agent conduct holds alike in each project only where it binds in all; an agent that meets a compiler error in any project is able to clear it by lowering the edition, which loses the edition in force silently, so one rule for every agent keeps each lowering visible in a decision record, at the cost of one sentence, while the edition itself stays each project's (STND.CXX.2 or its alternative). |
| STND.PY.4 | An agent configuration works across projects under the same agent instructions (STND.DFLT.21), so a rule of agent conduct holds alike in each project only where it binds in all; code that an agent writes moves between projects and between classes, and an annotation costs the agent only the form of that code while its absence costs a rewrite at each reclassification, so one rule for every agent keeps agent-written Python ready for the checker that a project of every class is able to adopt, while the form stays each project's through the alternative it adopts in place of STND.PY.3. |
| STND.RUST.6 | An agent configuration works across projects under the same agent instructions (STND.DFLT.21), so a rule of agent conduct holds alike in each project only where it binds in all; unsafe code that an agent writes without its soundness argument compiles and passes its tests in every project, while it leaves a reviewer nothing to check the code against, so one rule for every agent lets the reviewers of every project rely on finding the argument at agent-written unsafe code, while its form stays each project's (STND.RUST.3 or its alternative). |

The Notes of each standard add, where they say that the provision binds by its own force (GOV.48), "for the reason of uniformity across projects that its field `binding_reason` records (GOV.19)".

**Not drafted, with the reason.**
- STND.VVUQ.83 instantiates PRIME.2, so a prime directive forces its binding, and it needs no reason.
- STND.DFLT.21, STND.INSTR.1 to STND.INSTR.11, and AGENT.11 also instantiate GOV.48. AGENT.11 is at LVL1 and carries no mode. The others are the agent instructions themselves, which the first clause of GOV.48 asks for, not provisions of form or style. Several reach GUARD or a prime directive as well. Their documents belong to the process part of this round.

**For the custodian at ratification.**
1. Record the four reasons, rather than making the provisions defaults from CSQ3. *Recommendation: record them, as drafted.*
2. Whether the process-part instantiators of GOV.48 that reach only GOV, QA, or INTPR (STND.DFLT.21, STND.INSTR.1, .7, .8, .9, and .10) should also carry a reason. *Recommendation: no.* They are governance of agents, not form, and they meet the first limb of GOV.19.

## Self-check (step 2 of the standing process)

| Provision | Modals | Conditions first | Excluded expressions, qualifiers, quantifiers | Body IDs equal `instantiates` plus `refers_to` | `onset` |
| --- | --- | --- | --- | --- | --- |
| CPS.1 | 2 | none | none | GOV.25, GOV.26, GOV.12 | none (non-waivable) |
| STND.CODE.30 | 2 | yes | none | REPRO.3, REPRO.6 | CSQ3, unchanged |
| STND.CXX.2 | 3, unchanged | yes | none | unchanged | CSQ3, unchanged |
| STND.CXX.3 | 2 | yes | none | GOV.48, DSGN.3, STND.CXX.2 | none (binding) |
| NUMER.5, .7, .12, .23, .25 | unchanged | unchanged | unchanged | unchanged | as drafted |

No title changes. "Such as" and "for example" appear in no drafted text. The References tables are rewritten by `F.finish`, and `references --check` passes. No provision names a tool, product, vendor, or version.

## Checks

- `PARTS=apply_audit_tech_2026_10_31 … rehearse`: every check passes, with only the warning g.18 that the corpus already carries.
- `PARTS=apply_audit_lvl0_2026_10_31,apply_audit_tech_2026_10_31 … rehearse`, on the lvl0 part as it stood when this record was written: every check passes, with only g.18.
- On a kept copy: `references --check` passes, and `compose --check` reports nothing stale.
- `pairs`: see `pairs-changed.md`. Only the NUMER provisions have pairs on their changed side, and no pair is a conflict.
- `findings.py` over the ten documents: the only difference from before is the text of the existing review finding g.11 on STND.CXX.3 (a negated modal over a list), whose list gains "the dependency". It is the same construct as before, and STND.STDC.3 has it too.
