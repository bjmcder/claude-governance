# Round of 2026-10-31 on the cleanup audit: part tech, the profiles and technical standards

This record carries the outcomes of the section "Profiles and technical standards" of `../decisions.md`: S7 (recommendation R7), S8, B8, O3, I2, I6, and I7 of `../findings.md`. The script is `tools/amendment-scripts/apply_audit_tech_2026_10_31.py`, run by the driver `apply_audit_2026_10_31.py` after the part lvl0. Nothing here is in force until the custodian ratifies it and the script runs. Recommendation R7 is not yet ruled; the draft carries the recommended option (a), and it goes to the custodian at ratification with the rest.

## Transactions

Ten transactions, one per document, each a GOV.41 amend by The Custodian, role custodians, through `F.finish`, which adds the revision row and rewrites the References table. The profiles come first, then the standards that cite them:

| k | Document | Revision | Class | Findings |
| --- | --- | --- | --- | --- |
| 0 | CPS | 1.0.2 to 1.1 (CPS.1 amended, CPS.10 new) | Minor | S7 (R7) |
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

CPS.1 gains a second sentence and GOV.12 in `instantiates`, and a new provision, CPS.10 Lower class referral (section Application, `instantiates: ["PRIME.14"]`, `refers_to: ["CPS.1"]`), carries what an agent does where a lower class is recorded:

> This profile SHALL bind a project whose classification makes at least one attribute of the table of this provision true (GOV.25, GOV.26). Work on a system that commands, configures, or powers physical hardware SHALL be classified CSQ3 or a more severe class (GOV.12).

> CPS.10: Where a class less severe than the class that CPS.1 requires is recorded for work on a system that commands, configures, or powers physical hardware, an agent SHALL halt that line of work and refer it to the human owner (PRIME.14).

The subject of CPS.1 is the work on a system that commands, configures, or powers physical hardware, the full reach of the attribute Physical hardware control and of PRIME.13, and the domain item of CPS (STND.DRAFT.37). It is not the whole project, so a component that the classification records as isolated from every such system keeps its own class under GOV.13. The human owner sets the class (STND.CLASS.1). Without CPS.10, CPS.3 to CPS.9, whose onset is CSQ3, would not apply under a recorded lower class. The halt and referral are a provision of their own, not a third sentence of CPS.1, for two reasons. CPS.1 keeps two modals, so the corpus keeps the three-modal warning only on the bundles of STND.DRAFT that the test suite confirms. And the selector keeps its own lineage. CPS.1 still reaches only GOV, so it keeps rank null and stays non-waivable. CPS.10 instantiates PRIME.14, so it derives rank 0 and non-waivability (GOV.17, check l.3). That rank is intended, since the provision is an instance of a prime directive. A binding, non-waivable provision carries no field `onset`. An LVL1 provision carries no mode.

The Notes gain, after the sentence on PRIME.13:

> CPS.1 has work on a system that commands, configures, or powers physical hardware classified CSQ3 or a more severe class, as GOV.12 lets a profile require of work in its domain: a wrong command is able to damage the hardware it drives, or what that hardware acts on, a loss beyond the author's own time that the consequence test of CSQ3 in STND.CLASS.1 counts, and the minimum keeps CPS.3 to CPS.9 in reach of all such work, the revision of the hazard analysis before an uncovered change first drives the hardware among them. The human owner sets that class (STND.CLASS.1); under CPS.10, an agent that finds a less severe class recorded for such work halts that line of work and refers it, so that the CSQ3 content of this profile is not left out under a class that the profile does not admit, and the referral asks the owner only for the classification that STND.CLASS.1 already asks. A credible path to injury, or to a major and hard-to-reverse loss, still sets CSQ0 or CSQ1 (STND.CLASS.1), and a component that the classification records as isolated from every such system keeps the class recorded for it (GOV.13).

The class paragraph opens: "Every provision other than the selector, the shared-matters provision, and CPS.10, which instantiates PRIME.14 and binds at every class, instantiates only VV, …".

and the closing sentence of the class paragraph becomes:

> No provision raises the floor (GOV.11): the minimum class of CPS.1 is the one that GOV.12 lets a profile require, and the floor of GOV.10 holds for such work unchanged.

**Floor argument (GOV.11).** The minimum raises obligations for work on such a system that was CSQ4: CPS.3 to CPS.9, the revision of the hazard analysis under CPS.3 among them. It does not raise the floor:
- The floor is the set of GOV.10, which holds at every class. The minimum leaves it unchanged.
- The minimum places work of a domain in a class by the means that LVL0 itself gives a profile (GOV.12). The obligations it brings are the ones above the floor that GOV.11 proportions to CSQ3.
- It proportions them to the consequence, as GOV.11 and PRIN.9 ask, not to the setting or the hardware of the work. A wrong command is able to damage the hardware it drives. That is a loss beyond the author's own time, which the consequence test of CSQ3 in STND.CLASS.1 counts and which STND.CLASS.2 already counts as met in doubt. So the minimum records what the criteria give for the domain, and removes the doubt.
- It asks no decision of the human owner beyond the classification and the adoption of the hazard analysis under PRIME.13, which LVL0 already assigns (STND.DRAFT.42). The referral of CPS.10 asks only for the classification that STND.CLASS.1 already requires. CPS.10 instantiates PRIME.14, which holds at every class, so it adds nothing to the floor.

It fits the LVL0 part as drafted. GOV.13 there presumes CSQ4 until a class is recorded, and that presumption never covers driving physical hardware.

**Transition (GOV.42).** A project whose classification records CSQ4 for work on a system that commands, configures, or powers physical hardware records CSQ3 or a more severe class for that work before the system next drives the hardware. An agent's referral under CPS.10 is the occasion for that record. Until the class is recorded, work that conforms to revision 1.0.2 is not in defect.

**For the custodian at ratification.**
1. Option (a) of R7 is drafted. Option (b), PRIME.13 carrying the revision duty at every class, amends a prime directive. A third mechanism was weighed and is not recommended: setting the field `onset` of CPS.3, and of CPS.5, CPS.6, and CPS.9, to null, so that they apply at every class. GOV.19 marks these provisions default, and an onset of null for a default above the floor raises the floor at CSQ4, which GOV.11 admits only by a recorded project decision that names the consequence. It also leaves the other CPS provisions at CSQ3, so a CSQ4 bench project would owe the revision of CPS.3 without the command record of CPS.7. The minimum class keeps the profile whole and uses the means that GOV.12 provides. *Recommendation: (a), as drafted.*
2. The subject is the work on such a system, not the whole project. *Recommendation: keep it.* A project that also holds analysis isolated from its controller keeps CSQ4 for that analysis under GOV.13.

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

**Gaps.** The audit overstated the gap at CSQ3. Tiers 3 and 5 of VVUQ.1 and VVUQ.7, all in the core, keep at CSQ3 the agreement on rounding and on stated error rates that a comparison takes. HW.QPU.6 and HDES.ASIC.5 keep NUMER.23 and NUMER.25 at CSQ3 within their domains. The NUMER Notes now say both. After the move, nothing that the five parts serve is left unasked at CSQ3:
- VV.1, VV.5, and PRIME.3 apply to work of CSQ3 in full (STND.CLASS.10).
- NUMER.11 still gives every tolerance a recorded basis at CSQ3.
- NUMER.13 still has each uncertainty component marked, "not assessed" among the markings.
- NUMER.26 still bars reseeding to pass at every class.
- A result of CSQ3 that lacks the evidence a moved part would supply has the component marked not assessed (NUMER.13). Where it lacks the evidence that VV requires, it is labeled unverified (PRIME.3). The NUMER Notes say so.
- For a comparison at CSQ3 that takes tier 3 or tier 5, the table of STND.VVUQ.1 gives the agreement. The Notes of STND.VVUQ describe it without stating an obligation.

The CSQ3 defaults STND.VVUQ.7 and STND.VVUQ.64 list NUMER.25 in `instantiates`. At CSQ3 they still rest on VV.1 and VV.3, which they also instantiate, so the lineage stays sound. No check compares the onset of a provision with that of its parents, and `verify` passes. So no gap calls for the alternative, and the move is drafted as `../decisions.md` gives it.

**Drafted fields.** NUMER.7, NUMER.12, NUMER.25: `onset: "CSQ2"`. NUMER.5, NUMER.23: `onset: ["CSQ3", ["sentence 2", "CSQ2"]]`, in the form of the existing fields (STND.CODE.22, STND.MPI.7, and others). Under STND.CLASS, a part that asks for no item of the table of STND.CLASS.10 applies from CSQ3. These fields depart from that rule, so the Notes of NUMER give the reason that the Notes of STND.CLASS admit, methods of a standard beyond its core. The sentence added after the class sentence of the NUMER Notes:

> NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23 apply from CSQ2, a departure from the rule of STND.CLASS: an order test, an estimate of rounding error under conditioning, a showing that the working precision keeps that error within the required precision, evidence that a statistical uncertainty has settled as the samples grow, and the error rates of a statistical criterion each cost an analysis or added computations rather than one statement, and STND.VVUQ gives its default method for each only from CSQ2. The core of STND.VVUQ still reaches two of them at CSQ3: STND.VVUQ.7 places a tolerance within its bracket, with the required precision as the departure to detect, and tiers 3 and 5 of the table of STND.VVUQ.1 rest the agreement of a comparison on an estimate of rounding error and on a criterion with stated error rates; HW.QPU.6 and HDES.ASIC.5 keep the content of NUMER.23 and NUMER.25 at CSQ3 within their domains. VV.1, VV.5, NUMER.13, and PRIME.3 hold for these results at CSQ3 in full, so a result of CSQ3 that lacks the evidence that a moved part would supply has the component concerned marked not assessed under NUMER.13, and carries the label unverified of PRIME.3 where it lacks the evidence that VV requires. The third sentence of NUMER.5 keeps CSQ3 and governs a record of the working precision that work below CSQ2 keeps by choice.

The STND.VVUQ Notes replace "so that work of CSQ3 meets NUMER through the core, while the obligations of LVL0 that the other provisions serve apply to it in full" with:

> as do NUMER.7, NUMER.12, NUMER.25, and the second sentences of NUMER.5 and NUMER.23, whose default methods are among them. Work of CSQ3 meets each other provision of NUMER through the core where the core reaches it, and otherwise by a method that the work chooses or by the statement that the provision admits, a component of NUMER.13 marked not assessed among them, while the obligations of LVL0 that the other provisions serve apply to it in full. For a comparison that takes tier 3, the table of STND.VVUQ.1 gives a tolerance set from an estimate of rounding error of the kind that NUMER.12 describes, and for one that takes tier 5, a criterion with a stated probability of rejecting a correct result and a stated detection power, the content of NUMER.25.

**Floor argument (GOV.11).** Moving an onset from CSQ3 to CSQ2 narrows a waivable default to more severe work. It lowers no floor and raises none. VV.1, VV.5, and PRIME.3, which these parts serve, apply at CSQ3 in full.

**For the custodian at ratification.**
1. **The alternative of `findings.md`.** Have "not assessed", with the unverified label of PRIME.3, meet these parts at CSQ3, leaving them at CSQ3. The draft would add a sentence to the class paragraph of the NUMER Notes, keep the five fields at CSQ3, and give NUMER.12 and NUMER.23 a permission. NUMER.12, in one form, would gain: "Where the work is of CSQ3, the estimate MAY be marked not assessed under NUMER.13, and the result reported as unverified (PRIME.3) (VV.5, INTPR.9)." It is not recommended. It writes a class into a provision body, which the field `onset` exists to keep out, and it keeps an unverified label on every CSQ3 result that uses floating point. *Recommendation: the move, as drafted.*
2. **The third sentence of NUMER.5** asks the record of the working precision to take an exchanged precision from a boundary contract of HW.13. It stays at CSQ3 as `../decisions.md` gives it. Below CSQ2 it governs only a record that the work keeps by choice, since the boundary contract starts at CSQ2, and the NUMER Notes now say so. Moving it with sentence 2 (`["CSQ3", ["sentence 2", "CSQ2"], ["sentence 3", "CSQ2"]]`) changes nothing in practice. *Recommendation: leave it.*
3. **The first sentence of NUMER.23**, evidence that the samples represent their distribution, keeps CSQ3. Its default methods (STND.VVUQ.58, .60, and the first sentence of .61) also start at CSQ2. The same holds for NUMER.22 (STND.VVUQ.57). The audit did not raise them, and `../decisions.md` does not move them. Each follows the rule of STND.CLASS, and work of CSQ3 meets each by a method of its choice. *Recommendation: no change in this round.*
4. **HW.QPU.6 and HDES.ASIC.5** cite NUMER.23 and NUMER.25 and keep their content at CSQ3 for quantum-processor sampling across calibrations and for sampled device variation. The move does not reach them. Each is a tightening above the floor within its domain (PRIME.15). *Recommendation: leave them.*

## I7, ML term Learned model use

The term gains a sentence, and the Selector text now cites the term rather than stating the exclusion alone:

> | Learned model use | An attribute, true when the classification records that a learned model sits, or is admitted to sit, on a path that affects a result the work reports or relies on, or physical hardware. A learned model in its use as the model through which an agent does the work does not make the attribute true. That exclusion does not reach a learned model that the work builds, trains, or runs as part of what it delivers, even when it is the model of an agent. |

> The term Learned model use leaves out the model through which an agent does the work, which the agent practice profile (AGENT) and the Safeguards Article (GUARD) govern, and keeps a learned model that the work builds, trains, or runs as part of what it delivers, even when an agent uses that model too.

Taken literally, the old term was true of every project in which an agent works. The exclusion is bounded. Only the model through which an agent does the work is excluded. A learned model that the work builds, trains, or runs as part of what it delivers stays under ML, even when it is the model of an agent, as in a project that builds a data-triage agent. **Floor:** no obligation is raised, and the selector narrows to the reach that its Notes always gave it. The agent's model stays under GOV.48, AGENT, and GUARD. The term is in the profile's Terms, so the fix sits in the term, not in ML.1, whose body only tests the attribute.

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

**Reading.** GOV.19: "A provision is marked binding only where it instantiates a prime directive, GUARD, or a floor obligation (GOV.10), or where the custodians record why uniformity across projects requires it; every other LVL2 provision, including every provision of form or style, is a default." GOV.10 puts GOV in the floor, so an instantiator of GOV.48 meets the first limb. The check l.4 counts it as forced, so it needs no `binding_reason` to verify. The audit reads GOV.19 the other way: a provision of form or style is a default unless the custodians record the reason. Recording the reason meets GOV.19 on both readings and keeps the corpus verifying. A forced binding provision with a recorded reason has precedent: each of STND.DRAFT.35 to STND.DRAFT.41 reaches GOV and carries the field. Making a provision a default from CSQ3 would mean dropping GOV.48 from its `instantiates`, since l.4 fails a non-waivable default. That changes its lineage, and it lets work of CSQ4 omit a rule that guards against a silent loss at every class. It would also undo the custodian's ruling of 2026-10-23 on STND.PY.4 and STND.CXX.3. So a reason is drafted for each of the four GOV.48 provisions of this part's documents that rest on GOV.48 alone among PRIME, GUARD, and the floor. Each reason opens with what that provision guards against. It then says how the binding mark reaches every project: STND.INSTR.10 has an agent meet each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48). The reason does not rest on agent instructions in general, which would justify binding any agent rule. None becomes a default. Each field holds a draft for the custodians to adopt at ratification.

| Provision | Drafted `binding_reason` |
| --- | --- |
| STND.DOCS.10 | The human owner and the reviewers of every project verify the text that an agent writes against the work (INTPR.1), and inflated or generic prose, notes about the agent, and known false statements defeat that check at every class; as a binding provision it reaches every agent in every project, since STND.INSTR.10 has an agent meet each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48), so each reader relies on agent-written text without first learning the class of the work, while the spelling, content, and patterns stay each project's through the alternatives it adopts. |
| STND.CXX.3 | An agent that meets a compiler error in any project is able to clear it by lowering the edition, which loses the edition in force silently; as a binding provision it reaches every agent in every project, since STND.INSTR.10 has an agent meet each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48), so each lowering is visible in a decision record in every project, at the cost of one sentence, while the edition itself stays each project's (STND.CXX.2 or its alternative). |
| STND.PY.4 | Code that an agent writes moves between projects and between classes, and an annotation costs the agent only the form of that code while its absence costs a rewrite at each reclassification; as a binding provision it reaches every agent in every project, since STND.INSTR.10 has an agent meet each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48), so agent-written Python is ready in every project for the checker that the project adopts, while the form stays each project's through the alternative it adopts in place of STND.PY.3. |
| STND.RUST.6 | Unsafe code that an agent writes without its soundness argument compiles and passes its tests in every project, while it leaves a reviewer nothing to check the code against; as a binding provision it reaches every agent in every project, since STND.INSTR.10 has an agent meet each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48), so the reviewers of every project find the argument at agent-written unsafe code, while its form stays each project's (STND.RUST.3 or its alternative). |

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
| CPS.1 | 2 | none | none | GOV.25, GOV.26, GOV.12 | none (non-waivable, rank null) |
| CPS.10 (new; title of three words, distinct) | 1 | yes | none | PRIME.14, CPS.1 | none (binding, rank 0) |
| STND.CODE.30 | 2 | yes | none | REPRO.3, REPRO.6 | CSQ3, unchanged |
| STND.CXX.2 | 3, unchanged | yes | none | unchanged | CSQ3, unchanged |
| STND.CXX.3 | 2 | yes | none | GOV.48, DSGN.3, STND.CXX.2 | none (binding) |
| NUMER.5, .7, .12, .23, .25 | unchanged | unchanged | unchanged | unchanged | as drafted |

No title changes. "Such as" and "for example" appear in no drafted text. The References tables are rewritten by `F.finish`, and `references --check` passes. No provision names a tool, product, vendor, or version.

## Checks

- `PARTS=apply_audit_tech_2026_10_31 … rehearse`: every check passes, with only the warning g.18 that the corpus already carries.
- `PARTS=apply_audit_lvl0_2026_10_31,apply_audit_tech_2026_10_31 … rehearse`, on the lvl0 part as it stood after the review revisions: every check passes, with only g.18.
- On a kept copy: `references --check` passes, and `compose --check` reports nothing stale.
- `pairs`: see `pairs-changed.md`. Only the NUMER provisions have pairs on their changed side, and no pair is a conflict.
- `findings.py` over the ten documents: the only difference from before is the text of the existing review finding g.11 on STND.CXX.3 (a negated modal over a list), whose list gains "the dependency". It is the same construct as before, and STND.STDC.3 has it too. No new g.18 finding. In `verify`, g.18 warns only on STND.DRAFT.35, .39, and .42, as before.
- `pairs` on CPS.1 and CPS.10 after the revision: no pair.

## Review and dispositions

The cold review is `review.md` in this folder.

| Finding | Disposition | Reason |
| --- | --- | --- |
| T1, CPS.1 scope and a recorded lower class | Fixed | CPS.1 names the full reach of the attribute: "commands, configures, or powers". New CPS.10 has an agent that finds a less severe class recorded for such work halt that line of work and refer it (PRIME.14), as directed. It is a provision of its own, so that CPS.1 keeps two modals and adds no g.18 finding. The review proposed instead that the agent apply the CSQ3 obligations; that was not taken, since it would have the agent override a classification that is the owner's act. The Notes (including the class paragraph, which now excepts CPS.10), the rationale, and the transition follow. |
| T2, the CSQ3 consequence, and sentence 3 of NUMER.5 | Fixed | The NUMER Notes say that a result of CSQ3 lacking the evidence a moved part would supply has the component marked not assessed (NUMER.13), and carries the label unverified where it lacks the evidence that VV requires (PRIME.3). They also say that sentence 3 of NUMER.5 keeps CSQ3 and governs a record kept by choice below CSQ2. |
| T3, the circular opening of the binding reasons | Fixed | The shared opening, which cited STND.DFLT.21 for something that provision does not say, is gone. Each field opens with its own reason, then states what holds: STND.INSTR.10 has an agent meet each binding provision of an adopted standard whose sentence names an agent as its actor (GOV.48). |
| T4, Notes overstatement | Fixed | The STND.VVUQ Note now describes what the table of STND.VVUQ.1 gives for tiers 3 and 5, with no indicative obligation. The NUMER Notes name what the core keeps at CSQ3 (STND.VVUQ.7, and tiers 3 and 5 of STND.VVUQ.1) and the domain tightenings of HW.QPU.6 and HDES.ASIC.5. |
| T5, ML exclusion unbounded | Fixed | The term adds: "That exclusion does not reach a learned model that the work builds, trains, or runs as part of what it delivers, even when it is the model of an agent." The Selector text and the rationale follow. |
| T6, CPS rationale reads as ratified while R7 is unruled | Not fixed | This is by design. Every amendment script runs only after ratification, and the rationale's "ratified by the custodian on" is then true. R7 goes to the custodian at ratification. If the custodian chooses option (b), the CPS transaction is withdrawn from the part and PRIME.13 is amended in the lvl0 part instead. |
