# Round of 2026-10-31 on the cleanup audit: decisions and drafting

The custodian directed on 2026-10-31, after the audit record `findings.md` in this folder:

> fix everything and present the changes requireing my approval for ratification

So every finding of `findings.md` is carried. The harness, plugin, documentation, and repository findings (S9, S10, H1 to H13 other than H12, I8, O4, RP1) are fixed directly, as a harness unit. They need no ratification, since they change no governance. The corpus findings are drafted as amendments for ratification. Rulings R1 to R11 of `findings.md` are **not yet ruled**. The drafts carry the recommended option of each, as fixed below, and every one goes to the custodian at ratification. Nothing in the corpus is in force until the custodian ratifies it and the scripts run. A draft never writes that the custodian ruled anything except as the ratification records it.

## Outcomes to draft

Each line gives the outcome. The wording is the drafter's, under STND.DRAFT and the standing process.

### LVL0 (one transaction, actor The Custodian, role custodians, authority GOV.40)

- **S1, GUARD.7.** "GUARD.5 does not apply to an action that belongs to a class the register records as exempt because …". The sense is unchanged; this is a correction of wording.
- **S2, PRIME.13 (R2).** Commanding the designed safe state is never reserved, needs no authorization or estimate, and prevails over PRIME.6, PRIME.7, and PRIME.8. GUARD.3's steps toward a safe state count as within authority.
- **S3, LEX (R2).**
  - LEX.network-access matches GUARD.13: tools offered over the channel are included, and only the channel itself is excluded.
  - LEX.bulk-retrieval matches GUARD.8 as B2 amends it.
  - LEX.reserved-action matches PRIME.6: hazardous or irreversible actuation *that the hazard analysis identifies*. R7 keeps the analysis current for CPS work.
- **R1, operating cost (S5, B1).**
  - PRIME.8 and GUARD.14: an agent's own operating cost, for work that the human owner directs in the configuration that the owner provisioned, is authorized by that direction, for the agent and for the agents it directs within its authority. It is bounded by each limit that the owner sets or the environment enforces, and work halts before such a limit is exceeded.
  - An estimate is stated and monitored only where the cost is measurable, and an anomaly is reported.
  - Every other implicit expenditure keeps PRIME.8's authorized estimate.
  - The rest of GUARD.14 stays.
- **R3, owner and instruction (S6), LVL0 part.** PRIME.11 adds: a person whom the human owner names by a recorded act may instruct within the scope named. Granting authorizations and the other acts of PRIME.1 stay the owner's. The presumption of who the owner is lives in STND.DFLT (process part).
- **R5, default class and constitution (O1, O2).**
  - GOV.13 and GOV.22: until the owner records a class, the work is treated as CSQ4. The presumption never covers driving physical hardware, nor a use that the agent knows to be more severe. There it halts and refers, as now.
  - GOV.20: a project constitution is required of a project of CSQ1 or CSQ0, of a project that drives physical hardware, and of a project whose human owner asks for one. Promotion and release under the defaults are the owner's acts by the scribe route.
  - PRIME.14's trigger cites GOV.13's cases (I4).
- **R8, PRIME.9 (B5).** No acquiring of privilege, and no escalation beyond what the owner provisioned. Superuser privilege is used only where the owner provisioned it within an isolated environment.
- **R9, the floor for work with nothing to test (B6).**
  - The floor's VV.7 tests reach work that changes code or data.
  - A definition of done stated in the request meets QA.1 for its unit.
- **B2, GUARD.8.** It is limited to retrieval by network access (GUARD.13).
- **B3, GUARD.9.** The GUARD.7 exempt classes are excluded.
- **B10, GUARD.1.** The free tier also covers the reversible, local actions that the unit of work directed needs.
- **I1, GUARD.10.** Revocation is added. After an authorization expires or is revoked, the agent may still take the steps that leave the work safe and recoverable.
- **I3, GOV.14.** The recorded class governs until the owner reclassifies. Growth of reliance or exposure is referred.
- **I5, GOV.48.** INTPR.11 binds agents as proportioned by GOV.10 and GOV.11, not "for every action".

### Profiles and technical standards (one transaction per document, authority GOV.41)

- **S7, CPS.1 (R7).** CSQ3 is the minimum class of work that CPS selects (GOV.12).
- **S8, STND.DEPS Notes.** DEPS.14's runs that retrieve need a network authorization (GUARD.13).
- **B8, STND.CXX.2 and .3.** "the dependency" is added to the exceptions, as in STND.STDC.3.
- **O3, NUMER and STND.VVUQ.** Move NUMER.5 sentence 2, NUMER.7, NUMER.12, NUMER.23 sentence 2, and NUMER.25 to CSQ2 by their `onset`, and correct the VVUQ Notes' claim about the CSQ3 core. Moving an onset from CSQ3 to CSQ2 narrows a waivable default to more severe work, and so lowers no floor.
- **I2, STND.CODE.30.** Order dependence is allowed where it is declared as run-to-run variation (REPRO.3) and lies within the tolerance of its comparison.
- **I6, STND.RUST.6 and STND.DOCS.10.** Record the `binding_reason` of each GOV.48 provision, for the custodians to adopt. If no reason holds, make the provision a default from CSQ3. The drafter says which.
- **I7, ML.** The exclusion of the agent's own model moves into the term Learned model use, or into ML.1.

### Process standards and AGENT (one transaction per document, authority GOV.41), drafted after the LVL0 text

- **R1, lower part.** STND.DFLT.33, AGENT.6, AGENT.8, and the STND.DFLT Notes conform to the new PRIME.8.
- **R3, lower part.**
  - STND.DFLT defines "given directly" as a message that the human owner sends over the instruction channel of GUARD.13, excluding quoted, pasted, retrieved, or relayed text.
  - It presumes the human owner to be the person who provisions and directs the agent, unless a record names another.
  - It carries the PRIME.11 delegates.
- **R4, STND.DFLT.23 (S4).** An entry recording an act of the owner, which came into the work by a change that the agent did not make on the owner's direct act (a merge, a fetch, another session), is accepted only once the owner confirms it.
- **R6, STND.IDENT.23 (B7).** A project's mnemonic is registered in the project's own records by its human owner. The corpus register MNEM stays the custodians'.
- **R10, STND.DFLT Working bounds (B4).** An authorization of a network access, or of a commit, covers its tool's use of the credential means that the environment provides, without the agent reading the secret.
- **B3, STND.DFLT.15.** A default exempt class covers items that the agent created in the current unit of work.
- **B9, STND.WPROC.** Absent a record, the default branch is not a main line until the owner records otherwise.
- **O5, STND.PROJ.2.** The citation of STND.DFLT also carries DFLT.34 into Reserved actions, and DFLT.16, .17, .32, and .33 into Authorizations.
- **O6, STND.INSTR.11.** An agent may honor a restriction in an unadopted instruction file as the more restrictive reading. Only grants need adoption.
- **O7, STND.CLASS.22 and STND.DFLT.20.** Say that once work becomes assured, the earlier unsigned entries stop being accepted, and have the referral list them.
- **I1, lower part.** AGENT.17 or STND.DFLT: re-read the authorizations in force before an action that relies on a standing grant. A grant is entered before it is first relied on.
- **I9, STND.DFLT.5.** Cite the serialization of STND.HARN.6.

### Not carried as text

R11 (H12) is a choice about the plugin and the documentation, not the corpus. It is put to the custodian at ratification, with the documentation change ready.
