# Cold review of part tech: profiles and technical standards

Reviewer worked on a copy (lvl0 then tech applied; scratch under the session scratchpad `review-tech/c/governance`) and read the amended text before the drafter's `decisions.md`. Nothing in the repository was edited except this file.

## Verification results

- `python3 -B -m govharness verify <copy>`: every check PASS (ids, mnemonics, references, manifests, ledger, unpinned, templates, status, checked-by, onset, logic). Only the standing warning g.18 (at most three modals) appears.
- `tools/findings.py <copy> 'CPS|NUMER|ML|STND\.(VVUQ|CODE|DEPS|DOCS|CXX|PY|RUST)'`: 130 findings before and 130 after. The only difference is the text of the existing review finding g.11 on STND.CXX.3 (negated modal over a list), whose list now includes "the dependency". STND.STDC.3 has the same construct. No new finding on CPS.1, CODE.30, CXX.2, NUMER, or ML.
- `pairs` on the copy: CPS (38 pairs, all on CPS.4, which is unchanged), NUMER (92), ML (16, all on ML.5, unchanged), STND.CODE (none). I read the drafter's `pairs-changed.md` (43 pairs, all NUMER); I agree with each verdict. See T4 for the two pairs the drafter flagged for the custodian.
- Outcomes against `decisions.md` ("Profiles and technical standards"): S7, S8, B8, O3, I2, I6, I7 are each carried, and nothing else changes. The only excess is that I6 covers four provisions (DOCS.10, CXX.3, PY.4, RUST.6) where the outcome names two; the outcome says "each GOV.48 provision", so I count it as carried (the drafter documents why VVUQ.83, DFLT.21, INSTR.*, AGENT.11 are left out, and I agree).

## Findings

### T1. Low (Medium if read without STND.CLASS.1). CPS.1 gives the minimum no effect on a recorded lower class, and names narrower scope than the attribute

Identifier: CPS.1.
Quote: "Work on a system that commands physical hardware SHALL be classified CSQ3 or a more severe class (GOV.12)."
Problem: Two gaps.
1. The sentence says what the class "SHALL be" but not who answers for it or what an agent does on finding a lower class recorded. STND.CLASS.1 already has the human owner set "the class that a selected profile requires (GOV.12)", so an owner who records CSQ4 breaches that provision. But CPS.3 to CPS.9 carry `onset` CSQ3, so they do not apply to an agent working under the recorded CSQ4, and nothing in CPS tells the agent to apply them anyway or to refer.
2. The attribute (CPS Terms, PRIME.13) is true when the work "commands, configures, or powers" physical hardware. The new sentence says "commands" alone. The drafter's note says the CPS term Command covers configuring and powering, but the sentence has no capital and no citation, so a reader of CPS.1 alone sees a narrower scope than the selector.
Scenario: a CSQ4 bench project is recorded with Physical hardware control true. It adds a power-sequencing output (powers, does not "command"). An agent reading CPS.1 finds the minimum silent on power sequencing and CPS.5, .6, .7, .9 not applying at the recorded CSQ4. PRIME.13 still holds (hazard analysis before first drive), so this leaves only the CSQ3-onset CPS content unprotected, which is S7's own scenario. Before any classification exists, CPS does not bind, but GOV.13 (as amended by lvl0) bars the presumed CSQ4 from covering driving physical hardware and halts the agent, so the moment before classification is safe.
Proposed fix (CPS.1, second sentence): "Work on a system that commands, configures, or powers physical hardware SHALL be classified CSQ3 or a more severe class, and an agent that finds a less severe class recorded for that work applies the obligations of CSQ3 to it until the human owner records otherwise (GOV.12, STND.CLASS.1)." This is a tightening only (PRIME.15), asks the owner for nothing new, and has two modals. If the custodian prefers the shorter text, change "commands" to "commands, configures, or powers" and add one Notes sentence saying that the recorded class governs for the owner and that STND.CLASS.1 puts the minimum into the owner's decision.

### T2. Low-Medium. NUMER and VVUQ Notes assert VV.1/VV.5/PRIME.3 hold at CSQ3 but never say what a CSQ3 result without the dropped evidence carries

Identifiers: NUMER Notes (class paragraph), STND.VVUQ Notes.
Quote (NUMER): "while VV.1, VV.5, and PRIME.3 hold for such results at CSQ3 in full."
Problem: This is the safety case for the move (PRIME.3, unlabeled wrong results). It is stated, not made operational. VV.5 requires the report to say whether verification was performed and met, but nothing in NUMER says that a CSQ3 result whose rounding bound (NUMER.12), settling of its statistical uncertainty (NUMER.23 s2), or false-rejection and detection rates (NUMER.25) was not produced is reported with that component marked "not assessed" under NUMER.13 and, where it states a correctness claim, with the unverified label. The VVUQ Notes mention "a component of NUMER.13 marked not assessed", but only for how work "meets" a provision, and say nothing about the label.
Scenario: a CSQ3 agent reports a fit with error bars. It computes no rounding estimate, marks numerical error "estimated" from discretization only, and omits "unverified". It follows every provision that applies at CSQ3 and still reports an unlabeled result with an unassessed error source. PRIME.3 forbids this, but the amended Notes do not say how a CSQ3 reader reaches that conclusion, and the removal of NUMER.12's CSQ3 force is the cause.
Proposed fix (NUMER Notes, append to the added sentence): "A result of CSQ3 whose rounding error, settling of statistical uncertainty, or error rates of a statistical criterion the work has not estimated reports that component as not assessed (NUMER.13) and, where the report claims the result correct, carries the label of PRIME.3." (Informative; adds no obligation beyond VV.5, PRIME.3, and NUMER.13.)

Also (Low, same area): NUMER.5 sentence 3 ("the record of the working precision SHALL take that precision from it") keeps CSQ3 while the record it refers to (sentence 2) moves to CSQ2. The drafter's `decisions.md` explains this (sentence 3 governs a record kept by choice); the corpus Notes do not. Add to the NUMER Notes: "Sentence 3 of NUMER.5 keeps CSQ3 and governs a record of the working precision that the work keeps below CSQ2."

### T3. Low. The shared opening clause of the four `binding_reason` fields proves too much and cites a provision that does not say it

Identifiers: STND.DOCS.10, STND.CXX.3, STND.PY.4, STND.RUST.6 (field `binding_reason`).
Quote (all four): "An agent configuration works across projects under the same agent instructions (STND.DFLT.21), so a rule of agent conduct holds alike in each project only where it binds in all;"
Problem:
1. STND.DFLT.21 says only that agent instructions SHALL be the provisions of the agent-instructions standard "where [it] is adopted". It does not say a configuration works across projects. The provision that carries a rule into instructions is STND.INSTR.10 (the Notes of DOCS, PY, RUST, CXX cite it for that).
2. As a reason it applies to every agent rule, so it does not discriminate. GOV.19 asks for "why uniformity across projects requires" this provision. The second clause of each field (the INTPR.1 verification argument in DOCS.10; silent edition loss in CXX.3; reclassification rewrite in PY.4; reviewer without argument in RUST.6) is specific and sound. The first clause is circular ("binds in all" because it must bind in all).
Scenario: a custodian adopting these reads the reason as a template that would justify binding any agent rule, which weakens the record GOV.19 intends and invites the next form-of-work rule to copy it.
Proposed fix: drop the first clause and begin each field at its specific reason, citing GOV.48 and STND.INSTR.10 where uniformity is needed. Example for STND.RUST.6: "Unsafe code that an agent writes without its soundness argument compiles and passes its tests in every project, while it leaves a reviewer nothing to check the code against; STND.INSTR.10 carries one rule into the instructions of every project (GOV.48), so the reviewers of every project rely on finding the argument at agent-written unsafe code, while its form stays each project's (STND.RUST.3 or its alternative)." Keep the Notes citations unchanged.

### T4. Low. Notes overstate how far the CSQ3 core stops short of NUMER.25 and tier 3

Identifiers: NUMER Notes; STND.VVUQ Notes.
Quote (VVUQ Notes): "a comparison at CSQ3 that takes tier 3 of STND.VVUQ.1 still sets its tolerance from an estimate of rounding error of the kind that NUMER.12 describes."
Problem:
1. "still sets" reads as an obligation in an informative section. STND.VVUQ.1 is a SHOULD (tier choice), and a comparison may take another tier. The text should describe what the tier's agreement column says.
2. The NUMER Notes say the default methods for each moved part "start at CSQ2" beyond the core. The drafter's own table shows the core reaches NUMER.25 partly: STND.VVUQ.7 (CSQ3) instantiates NUMER.25 and places the tolerance within a bracket whose departure is the required precision. Also, STND.VVUQ.1 tier 5 (CSQ3) asks a "stated probability of rejecting a correct result and a stated detection power", which is the content of NUMER.25. The Notes say this nowhere.
3. HW.QPU.6 and HDES.ASIC.5 (both CSQ3) cite NUMER.23 and NUMER.25, so at CSQ3 they reinstate in their domains what NUMER now starts at CSQ2. The drafter filed this for the custodian (O3 item 4); I agree it is a tightening within domain (PRIME.15) and not a conflict, but the NUMER Notes could name it in one clause so a reader does not take NUMER.25 as absent at CSQ3 in every domain.
Proposed fix (VVUQ Notes): replace "still sets its tolerance from" with "takes, as the table of STND.VVUQ.1 gives, a tolerance set from". (NUMER Notes): after "start at CSQ2" add "; STND.VVUQ.7 and tier 5 of STND.VVUQ.1 keep at CSQ3 the part of NUMER.25 that bears on a tolerance bracket and a stated criterion, and HW.QPU.6 and HDES.ASIC.5 keep NUMER.23 and NUMER.25 at CSQ3 for their domains".

### T5. Low. ML: "the model through which an agent does the work" is unbounded for a project that builds or runs an agent

Identifier: ML term Learned model use.
Quote: "A learned model in its use as the model through which an agent does the work does not make the attribute true."
Problem: "the work" is the project's work. A project whose product is an agent (software that meets GOV.51) or that runs a model as a component of its pipeline has a model "through which an agent does" work. Whether that is excluded is not stated. The Selector text says a model that "the work itself places on such a path makes the attribute true", which settles most cases, but the term (the normative place) does not say so, and the term is where I7 asked the exclusion to sit.
Scenario: a project builds a data-triage agent whose model classifies samples. A reader of the term alone can say the model is the one "through which an agent does the work" and drop the attribute, so ML never binds, and the classification is unreported by ML.5 error estimates.
Proposed fix (term): "A learned model in its use as the model through which an agent does the development work of the project does not make the attribute true; a learned model that the work builds or runs as a component of its result path does." (Keeps the Selector text as drafted.)

### T6. Informational. The ledger rationale of entry 326 (CPS 1.1) reads as ratified, while R7 is not ruled

Identifier: ledger entry 326 (rationale), as written by the script.
Quote: "Minor amendment of CPS, revision 1.1, ratified by the custodian on 2026-10-31: …"; later "recommendation R7 … put to the custodian at ratification".
Problem: This is the template of every earlier amendment entry (e.g. 322, 323, 324), so it is not a defect of the draft. But the CPS transaction carries recommended option (a) of an unruled recommendation. The script must run only after the custodian rules R7; if the custodian chooses option (b) or another, entry 326 and CPS 1.1 are wrong as written. The drafter's `decisions.md` says so; I note it so the driver does not run the part without the ruling.
No claim in any revision row or rationale that the custodian ruled anything is untrue: the cited rulings (PRIN.10, the custodian's ruling of 2026-10-23 in the PY and CXX Notes) already exist in the corpus.

## Checked and sound

Safety (item 1)
- CPS minimum class: CPS binds only when the classification makes the attribute true; before any class is recorded, PRIME.13 (every class) and the amended GOV.13 (the presumed CSQ4 never covers driving physical hardware; the agent halts and refers) cover the moment before classification. CPS.1 does not lower PRIME.13 or GUARD. The "isolated component" carve-out (GOV.13) is kept in the Notes. The change raises no floor (GOV.10 unchanged; GOV.12 expressly permits the profile minimum; STND.CLASS.1 already lists "the class that a selected profile requires").
- NUMER onsets: every moved part is waivable and its parent obligations (VV.1, VV.5, PRIME.3, NUMER.11, NUMER.13, NUMER.26) still apply at CSQ3; the move narrows a waivable default to more severe work. Only T2 asks that the label consequence be written down. The cross-reference from NUMER.5 sentence 2 to NUMER.12 is class-consistent (both CSQ2), and HW.5 and HW.13, whose content sentence 2 records, also start at CSQ2. The default methods named in the Notes (STND.VVUQ.9, .20 to .24, .33 to .38, .61, .65) all carry `onset` CSQ2, as the Notes say.
- STND.CODE.30: relaxes only the second sentence; undeclared variation stays a defect under REPRO.3; the hash-value sentence is unchanged; consistent with STND.VVUQ.82 (declared sources, within agreed agreement) and STND.VVUQ.83, and follows STND.BUILD.15.
- STND.CXX.3 exception ("the dependency"): matches STND.STDC.3 word for word in order; costs the one decision record the provision already asks; the prohibition is on an agent and relaxes no higher provision (GOV.48 and DSGN.3 do not demand the newest edition).
- STND.DEPS Notes: the added clause only restates GUARD.13 as the STND.DFLT Notes say it, and closes the reading of "adds nothing that STND.DFLT.35 halts" as leave to fetch.

Burden (item 2)
- No change adds an owner decision or ceremony at CSQ3 or CSQ4 beyond what LVL0 already assigns. CPS.1 relies on the classification and the PRIME.13 hazard analysis the owner already makes (STND.DRAFT.42). NUMER onset moves reduce work at CSQ3. The four `binding_reason` fields add no obligation. The CXX.3 exception reduces halts.

Consistency (item 3)
- GOV.12 (minimum class), GOV.19 (binding_reason as an instance of "custodians record why uniformity"; the field is marked "for the custodians to adopt" and nothing says the custodian has ruled), PRIME.15 (CPS.1 tightens; the NUMER moves narrow; CODE.30 and CXX.3 loosen their own default or exception, not a higher provision), STND.VVUQ.82 and .83, and the STND.CLASS.10 onset rule (list form `["CSQ3", ["sentence 2", "CSQ2"]]` matches STND.CODE.22, STND.WFLOW.2, STND.OMP.2; "sentence 2" counted at terminal punctuation fits NUMER.5 and NUMER.23) are all met.
- Pairs: the 43 drafter verdicts hold. The CPS, ML, and STND.CODE pairs have no changed side; the document-level lists of DEPS, DOCS, PY, RUST are empty.

Drafting (item 4)
- One modal per sentence and at most three per provision in CPS.1 (2), STND.CODE.30 (2), STND.CXX.2 (3, unchanged), STND.CXX.3 (2). Conditions precede clauses. No "such as" or "for example" in any new text. No tool, vendor, or version is named. Body identifiers equal `instantiates` plus `refers_to` (CPS.1 gains GOV.12 in `instantiates` and the body cites it; `verify` logic and onset PASS). `onset` values are well formed. Revision numbers follow the minor/editorial classes the revision rows state (additions of an obligation or a meaning are minor; Notes-only and field-only are editorial). References tables gain STND.BUILD (CODE) and STND.STDC (CXX), matching the new citations.
- Rationale and revision rows describe the diffs accurately; the Notes follow each change.
- No new "such as"-type, qualifier, or atomicity finding from `findings.py`.
